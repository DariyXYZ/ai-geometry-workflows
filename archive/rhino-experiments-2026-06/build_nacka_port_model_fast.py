import json
import os
import subprocess
import sys
import tempfile

CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"
FLOOR_H = 3.3
BAY = 3.6

LAYERS = {
    "NP_Site_Base": (235, 235, 230),
    "NP_Massing_Wood": (126, 93, 65),
    "NP_Massing_Light": (210, 210, 205),
    "NP_Facade_Frames": (198, 176, 145),
    "NP_Glass_Dark": (72, 82, 84),
    "NP_Terraces": (154, 119, 82),
    "NP_Section_Cuts": (35, 35, 35),
}

MAJOR_NAMES = set()


def call(command, params):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(params, tmp)
    tmp.close()
    r = subprocess.run(
        [sys.executable, CLIENT, "call", command, "--params-file", tmp.name],
        capture_output=True,
        text=True,
    )
    os.unlink(tmp.name)
    if r.returncode != 0:
        raise RuntimeError("FAIL %s: %s" % (command, r.stderr[-800:]))
    return json.loads(r.stdout)


def ensure_layer(name, color):
    try:
        call("add_layer", {"name": name, "color": list(color)})
    except Exception:
        pass


def cleanup_layer(name):
    try:
        ids = call("filter_objects", {"layer": name}).get("ids", [])
        for oid in ids:
            try:
                call("delete_object", {"object_id": oid})
            except Exception:
                pass
        return len(ids)
    except Exception:
        return 0


def set_layer(oid, layer, name=None):
    call("set_object_layer", {"object_id": oid, "layer": layer})
    if name and name in MAJOR_NAMES:
        call("set_object_name", {"object_id": oid, "name": name})


def box(layer, name, x, y, z, sx, sy, sz):
    oid = call("add_box", {"corner": [x, y, z], "x": sx, "y": sy, "z": sz})["id"]
    set_layer(oid, layer, name)
    return oid


def volume(name, x, y, floors, w, d, layer="NP_Massing_Wood"):
    MAJOR_NAMES.add(name)
    return box(layer, name, x, y, 0, w, d, floors * FLOOR_H)


def grid_south(name, x, y, w, floors, z0=0):
    eps = 0.16
    frame = 0.18
    n = int(round(w / BAY))
    for k in range(n + 1):
        xx = x + min(w, k * BAY)
        box("NP_Facade_Frames", "%s_v%02d" % (name, k), xx - frame / 2, y - eps / 2, z0, frame, eps, floors * FLOOR_H)
    for f in range(floors + 1):
        zz = z0 + f * FLOOR_H
        box("NP_Facade_Frames", "%s_h%02d" % (name, f), x, y - eps / 2, zz - frame / 2, w, eps, frame)


def grid_east(name, x, y, d, floors, z0=0):
    eps = 0.16
    frame = 0.18
    n = int(round(d / BAY))
    for k in range(n + 1):
        yy = y + min(d, k * BAY)
        box("NP_Facade_Frames", "%s_v%02d" % (name, k), x - eps / 2, yy - frame / 2, z0, eps, frame, floors * FLOOR_H)
    for f in range(floors + 1):
        zz = z0 + f * FLOOR_H
        box("NP_Facade_Frames", "%s_h%02d" % (name, f), x - eps / 2, y, zz - frame / 2, eps, d, frame)


def grid_west(name, x, y, d, floors, z0=0):
    grid_east(name, x, y, d, floors, z0)


def terrace(name, x, y, floors, w, d):
    z = floors * FLOOR_H
    box("NP_Terraces", name, x, y, z + 0.05, w, d, 0.24)
    rail = 0.18
    box("NP_Facade_Frames", name + "_rs", x, y, z + 0.35, w, rail, 0.35)
    box("NP_Facade_Frames", name + "_rn", x, y + d - rail, z + 0.35, w, rail, 0.35)
    box("NP_Facade_Frames", name + "_rw", x, y, z + 0.35, rail, d, 0.35)
    box("NP_Facade_Frames", name + "_re", x + w - rail, y, z + 0.35, rail, d, 0.35)


def dark_panels(name, x, y, w, floors):
    eps = 0.08
    n = int(round(w / BAY))
    for f in range(2, floors, 4):
        for k in range(0, n, 3):
            xx = x + k * BAY + 0.75
            zz = f * FLOOR_H + 0.7
            box("NP_Glass_Dark", "%s_p_%02d_%02d" % (name, f, k), xx, y - eps / 2, zz, BAY - 1.5, eps, FLOOR_H - 1.3)


def section_slab_stack():
    x, y, w, d = -4, -12, 20, 1.1
    for f in range(9):
        box("NP_Section_Cuts", "section_floor_%02d" % f, x, y, f * FLOOR_H, w, d, 0.2)
    box("NP_Section_Cuts", "section_wall_w", x, y, 0, 0.25, d, 8 * FLOOR_H)
    box("NP_Section_Cuts", "section_wall_e", x + w - 0.25, y, 0, 0.25, d, 8 * FLOOR_H)


def main():
    for layer, color in LAYERS.items():
        ensure_layer(layer, color)
        print("cleanup %s %d" % (layer, cleanup_layer(layer)))

    volume("site_plinth", -70, -45, 0.3, 155, 105, "NP_Site_Base")

    # Main massing, estimated from sections/model images.
    volume("left_tower_main_31F", -38, -3, 31, 23, 25)
    volume("left_step_25F", -15, -3, 25, 14, 25)
    volume("left_step_20F", -1, -3, 20, 10, 25)
    volume("left_step_15F", 9, -3, 15, 8, 25)
    volume("left_step_11F", 17, -3, 11, 7, 25)
    volume("left_step_8F", 24, -3, 8, 7, 25)

    volume("right_tower_main_34F", 25, -4, 34, 24, 26)
    volume("right_step_23F", 10, -4, 23, 15, 26)
    volume("right_step_17F", 0, -4, 17, 10, 26)
    volume("right_step_12F", -8, -4, 12, 8, 26)
    volume("right_step_8F", -15, -4, 8, 7, 26)

    volume("front_market_podium_8F", -42, -26, 8, 72, 23)
    volume("central_courtyard_8F", -12, -3, 8, 34, 27)
    volume("rear_link_10F", -6, 22, 10, 36, 15)
    volume("right_low_wing_8F", 49, -4, 8, 31, 25)
    volume("left_rear_midrise_14F", -61, 3, 14, 18, 23)

    volume("context_white_east_6F", 84, -14, 6, 28, 22, "NP_Massing_Light")
    volume("context_white_west_6F", -72, -12, 6, 18, 18, "NP_Massing_Light")
    volume("context_low_south_5F", -61, -31, 5, 25, 14, "NP_Massing_Light")

    # Facade grids on the faces that define the image reading.
    grid_south("left_main_south", -38, -3, 23, 31)
    grid_west("left_main_west", -38, -3, 25, 31)
    grid_south("right_main_south", 25, -4, 24, 34)
    grid_east("right_main_east", 49, -4, 26, 34)
    grid_south("front_podium", -42, -26, 72, 8)
    grid_south("central_court", -12, -3, 34, 8)
    grid_south("right_low_wing", 49, -4, 31, 8)
    grid_south("context_east", 84, -14, 28, 6)

    for name, x, y, floors, w, d in [
        ("terrace_left_25", -15, -3, 25, 14, 25),
        ("terrace_left_20", -1, -3, 20, 10, 25),
        ("terrace_left_15", 9, -3, 15, 8, 25),
        ("terrace_left_11", 17, -3, 11, 7, 25),
        ("terrace_right_23", 10, -4, 23, 15, 26),
        ("terrace_right_17", 0, -4, 17, 10, 26),
        ("terrace_right_12", -8, -4, 12, 8, 26),
        ("terrace_podium", -42, -26, 8, 72, 23),
        ("terrace_court", -12, -3, 8, 34, 27),
    ]:
        terrace(name, x, y, floors, w, d)

    dark_panels("left_dark", -38, -3, 23, 31)
    dark_panels("right_dark", 25, -4, 24, 34)
    dark_panels("podium_dark", -42, -26, 72, 8)
    section_slab_stack()

    report = {
        "floor_to_floor_m": FLOOR_H,
        "facade_bay_m": BAY,
        "left_tower_floors": 31,
        "right_tower_floors": 34,
        "left_tower_height_m": round(31 * FLOOR_H, 1),
        "right_tower_height_m": round(34 * FLOOR_H, 1),
        "overall_bbox_estimate_m": [155, 105, round(34 * FLOOR_H, 1)],
        "notes": "Approximate reconstruction from provided model image and sections; facade grid is simplified on key visible faces.",
    }
    out = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\nacka_port_report.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("built fast Nacka Port model")
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
