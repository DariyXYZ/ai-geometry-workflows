import json
import math
import os
import subprocess
import sys
import tempfile
import time

# Legacy Aurox demo. New Rhino work should use standard RhinoMCP first.
CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"
LAYER = "AI_Loft_Chair_01"
COLOR = [190, 190, 185]


def call(command, params):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(params, tmp)
    tmp.close()
    try:
        result = subprocess.run(
            [sys.executable, CLIENT, "call", command, "--params-file", tmp.name],
            capture_output=True,
            text=True,
        )
    finally:
        os.unlink(tmp.name)
    if result.returncode != 0:
        raise RuntimeError("FAIL %s: %s" % (command, result.stderr[-800:]))
    return json.loads(result.stdout)


def ensure_layer(name, color):
    try:
        call("add_layer", {"name": name, "color": color})
    except Exception:
        pass


def set_props(oid, layer, name, color):
    call("set_object_layer", {"object_id": oid, "layer": layer})
    call("set_object_name", {"object_id": oid, "name": name})
    call("set_object_color", {"object_id": oid, "color": color})


def smooth_profile(y, bulge, lift, twist):
    # One S-like side profile: front runner, seat dip, lumbar turn, high back.
    base = [
        [-8.0, y, 0.0],
        [2.0, y, 1.2 + lift * 0.15],
        [12.0, y, 6.5 - lift * 0.25],
        [22.0, y, 10.5 + lift * 0.2],
        [29.0, y, 21.0 + lift],
        [31.5, y, 34.0 + lift * 0.6],
        [28.0, y, 42.0 + lift * 0.35],
    ]
    pts = []
    for i, p in enumerate(base):
        wave = math.sin(i * 0.9 + y * 0.08) * bulge
        pts.append([p[0] + wave + twist * (i / 6.0), p[1], p[2]])
    return pts


def main():
    ensure_layer(LAYER, COLOR)

    sections = []
    y_values = [-17.0, -11.0, -5.0, 0.0, 5.0, 11.0, 17.0]

    for index, y in enumerate(y_values):
        side_factor = abs(y) / max(abs(v) for v in y_values)
        bulge = 1.0 + side_factor * 2.2
        lift = math.cos(y * 0.18) * 1.4
        twist = y * 0.10
        pts = smooth_profile(y, bulge, lift, twist)
        curve_id = call("add_polyline", {"points": pts})["id"]
        set_props(curve_id, LAYER, "loft_section_%02d" % (index + 1), [80, 80, 80])
        sections.append(curve_id)
        time.sleep(1.2)

    time.sleep(2.0)

    loft_id = call("add_loft", {"ids": sections})["ids"][0]
    set_props(loft_id, LAYER, "ai_loft_ribbon_chair", COLOR)

    time.sleep(2.5)

    edge_sets = [
        [smooth_profile(y_values[0], 3.2, -1.3, -1.7)[0], smooth_profile(y_values[-1], 3.2, -1.3, 1.7)[0]],
        [smooth_profile(y_values[0], 3.2, -1.3, -1.7)[-1], smooth_profile(y_values[-1], 3.2, -1.3, 1.7)[-1]],
    ]
    for index, pts in enumerate(edge_sets):
        rail_id = call("add_polyline", {"points": pts})["id"]
        set_props(rail_id, LAYER, "soft_edge_rail_%02d" % (index + 1), [55, 55, 55])
        time.sleep(1.0)

    print("Created loft chair on layer %s" % LAYER)


if __name__ == "__main__":
    main()
