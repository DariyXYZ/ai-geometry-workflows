import json
import math
import os
import subprocess
import sys
import tempfile


# Legacy Aurox variant builder. New Scenario 3 builds should use RhinoMCP first.
CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"
PARAMS = r"c:\VS Code\workfiles\ai-geometry-workflows\scripts\moscow_bc_massing\variants_2026_06_16.json"


def call(command, params):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(params, tmp)
    tmp.close()
    try:
        result = subprocess.run(
            [sys.executable, CLIENT, "call", command, "--params-file", tmp.name, "--raw"],
            capture_output=True,
            text=True,
            timeout=60,
        )
    finally:
        os.unlink(tmp.name)
    if result.returncode != 0:
        raise RuntimeError("FAIL %s: %s" % (command, result.stderr[-800:]))
    return json.loads(result.stdout)


def safe_call(command, params):
    try:
        return call(command, params)
    except Exception:
        return None


def height_from_floors(floors):
    return 4.2 + (int(floors) - 1) * 3.6


def rect_points(part):
    cx = float(part["cx"])
    cy = float(part["cy"])
    w = float(part["w"])
    d = float(part["d"])
    rot = math.radians(float(part.get("rot", 0)))
    c = math.cos(rot)
    s = math.sin(rot)
    raw = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    return [[cx + dx * c - dy * s, cy + dx * s + dy * c] for dx, dy in raw]


def prism_mesh(part):
    h = height_from_floors(part["floors"])
    pts = rect_points(part)
    vertices = [[x, y, 0.0] for x, y in pts] + [[x, y, h] for x, y in pts]
    faces = [
        [0, 3, 2, 1],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7],
    ]
    return vertices, faces, h


def object_id(response):
    return response.get("id") or response.get("object_id") or (response.get("ids") or [None])[0]


def cleanup_layer(layer):
    found = safe_call("filter_objects", {"layer": layer})
    ids = (found or {}).get("ids", [])
    deleted = 0
    for oid in ids:
        if safe_call("delete_object", {"object_id": oid}) is not None:
            deleted += 1
    return deleted


def hide_old_generated_layers(target_layers):
    layers = call("get_layers", {})
    hidden = []
    for item in layers.get("layers", layers if isinstance(layers, list) else []):
        name = item.get("name") if isinstance(item, dict) else str(item)
        if not name:
            continue
        if name.startswith("AI_BC_20260616") or name in target_layers:
            safe_call("set_layer_visibility", {"name": name, "visible": False})
            hidden.append(name)
    return hidden


def main():
    params = json.load(open(PARAMS, "r"))
    target_layers = [v["layer"] for v in params["variants"]]
    hidden = hide_old_generated_layers(target_layers)
    created = []
    cleanup = {}

    for variant in params["variants"]:
        layer = variant["layer"]
        color = variant.get("color", [120, 120, 120])
        safe_call("add_layer", {"name": layer, "color_r": color[0], "color_g": color[1], "color_b": color[2]})
        safe_call("set_layer_color", {"name": layer, "r": color[0], "g": color[1], "b": color[2]})
        cleanup[layer] = cleanup_layer(layer)
        safe_call("set_layer_visibility", {"name": layer, "visible": True})

        for part in variant["parts"]:
            vertices, faces, h = prism_mesh(part)
            response = call("create_mesh", {"vertices": vertices, "faces": faces})
            oid = object_id(response)
            if not oid:
                raise RuntimeError("create_mesh returned no object id for %s" % part["name"])
            call("set_object_layer", {"object_id": oid, "layer": layer})
            call("set_object_name", {"object_id": oid, "name": part["name"]})
            call("set_user_text", {"object_id": oid, "key": "massing_variant", "value": layer})
            call("set_user_text", {"object_id": oid, "key": "floors", "value": str(part["floors"])})
            call("set_user_text", {"object_id": oid, "key": "height_m", "value": "%.3f" % h})
            created.append({"layer": layer, "name": part["name"], "id": oid, "height": round(h, 3)})

    print(json.dumps({
        "hidden_old_layers": hidden,
        "cleanup_deleted": cleanup,
        "created_count": len(created),
        "created_by_layer": dict((layer, len([x for x in created if x["layer"] == layer])) for layer in target_layers),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
