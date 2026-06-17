import json
import math
import os
import subprocess
import sys
import tempfile

CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"

FLOOR_H = 3.3
GRID = 3.6

LAYERS = {
    "NP_Site_Base": (235, 235, 230),
    "NP_Massing_Wood": (126, 93, 65),
    "NP_Massing_Light": (210, 210, 205),
    "NP_Facade_Frames": (198, 176, 145),
    "NP_Glass_Dark": (72, 82, 84),
    "NP_Terraces": (154, 119, 82),
    "NP_Section_Cuts": (35, 35, 35),
    "NP_Trees_People": (95, 120, 92),
}


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


def safe_delete(oid):
    try:
        call("delete_object", {"object_id": oid})
    except Exception:
        pass


def ensure_layer(name, color):
    try:
        call("add_layer", {"name": name, "color": list(color)})
    except Exception:
        pass


def cleanup_layer(name):
    try:
        ids = call("filter_objects", {"layer": name}).get("ids", [])
        for oid in ids:
            safe_delete(oid)
        return len(ids)
    except Exception:
        return 0


def set_props(oid, layer, name, color):
    call("set_object_layer", {"object_id": oid, "layer": layer})
    call("set_object_name", {"object_id": oid, "name": name})
    call("set_object_color", {"object_id": oid, "color": list(color)})


def add_box(layer, name, x, y, z, sx, sy, sz, color=None):
    color = color or LAYERS[layer]
    oid = call("add_box", {"corner": [x, y, z], "x": sx, "y": sy, "z": sz})["id"]
    set_props(oid, layer, name, color)
    return oid


def face_grid_x(layer_prefix, name, x, y, z, width, floors, side, bay=GRID, floor_h=FLOOR_H):
    """Grid on a face parallel to X/Z at y side."""
    layer = "NP_Facade_Frames"
    col = LAYERS[layer]
    eps = 0.16
    frame = 0.18
    y0 = side - eps / 2.0
    # vertical mullions
    n = int(round(width / bay))
    for k in range(n + 1):
        xx = x + min(width, k * bay)
        add_box(layer, "%s_v_%02d" % (name, k), xx - frame / 2.0, y0, z, frame, eps, floors * floor_h, col)
    # horizontal floor bands
    for f in range(floors + 1):
        zz = z + f * floor_h
        add_box(layer, "%s_h_%02d" % (name, f), x, y0, zz - frame / 2.0, width, eps, frame, col)


def face_grid_y(layer_prefix, name, x, y, z, depth, floors, side, bay=GRID, floor_h=FLOOR_H):
    """Grid on a face parallel to Y/Z at x side."""
    layer = "NP_Facade_Frames"
    col = LAYERS[layer]
    eps = 0.16
    frame = 0.18
    x0 = side - eps / 2.0
    n = int(round(depth / bay))
    for k in range(n + 1):
        yy = y + min(depth, k * bay)
        add_box(layer, "%s_v_%02d" % (name, k), x0, yy - frame / 2.0, z, eps, frame, floors * floor_h, col)
    for f in range(floors + 1):
        zz = z + f * floor_h
        add_box(layer, "%s_h_%02d" % (name, f), x0, y, zz - frame / 2.0, eps, depth, frame, col)


def add_volume(name, x, y, floors, w, d, layer="NP_Massing_Wood", color=None, grid_faces=True):
    h = floors * FLOOR_H
    add_box(layer, name, x, y, 0.0, w, d, h, color or LAYERS[layer])
    if grid_faces:
        face_grid_x("", name + "_south", x, y, 0.0, w, floors, y)
        face_grid_x("", name + "_north", x, y, 0.0, w, floors, y + d)
        face_grid_y("", name + "_west", x, y, 0.0, d, floors, x)
        face_grid_y("", name + "_east", x, y, 0.0, d, floors, x + w)
    return h


def add_terrace(x, y, z, w, d, name):
    add_box("NP_Terraces", name, x, y, z + 0.06, w, d, 0.22, LAYERS["NP_Terraces"])
    # parapet/edge rails
    rail = 0.18
    add_box("NP_Facade_Frames", name + "_rail_s", x, y, z + 0.35, w, rail, 0.35, LAYERS["NP_Facade_Frames"])
    add_box("NP_Facade_Frames", name + "_rail_n", x, y + d - rail, z + 0.35, w, rail, 0.35, LAYERS["NP_Facade_Frames"])
    add_box("NP_Facade_Frames", name + "_rail_w", x, y, z + 0.35, rail, d, 0.35, LAYERS["NP_Facade_Frames"])
    add_box("NP_Facade_Frames", name + "_rail_e", x + w - rail, y, z + 0.35, rail, d, 0.35, LAYERS["NP_Facade_Frames"])


def add_tower_with_stepped_side(name, x, y, w, d, full_floors, side, steps):
    add_volume(name + "_main", x, y, full_floors, w, d, "NP_Massing_Wood")
    # steps are additive blocks on the inner/courtyard side, like the model photos.
    for idx, s in enumerate(steps):
        sx, sy, sw, sd, floors = s
        z_top = floors * FLOOR_H
        add_box("NP_Massing_Wood", "%s_step_%02d" % (name, idx + 1), sx, sy, 0.0, sw, sd, z_top, LAYERS["NP_Massing_Wood"])
        face_grid_x("", "%s_step_%02d_s" % (name, idx + 1), sx, sy, 0.0, sw, floors, sy)
        face_grid_x("", "%s_step_%02d_n" % (name, idx + 1), sx, sy, 0.0, sw, floors, sy + sd)
        face_grid_y("", "%s_step_%02d_e" % (name, idx + 1), sx, sy, 0.0, sd, floors, sx + sw)
        add_terrace(sx, sy, z_top, sw, sd, "%s_terrace_%02d" % (name, idx + 1))


def add_window_panels(name, x, y, z, w, floors, side):
    # Sparse dark panels behind frame grid, enough to read as residential facade without thousands of objects.
    layer = "NP_Glass_Dark"
    eps = 0.08
    bay = GRID
    n = int(round(w / bay))
    for f in range(1, floors):
        if f % 2 == 0:
            continue
        zz = z + f * FLOOR_H + 0.65
        for k in range(n):
            if (k + f) % 3 == 0:
                xx = x + k * bay + 0.65
                add_box(layer, "%s_panel_%02d_%02d" % (name, f, k), xx, side - eps / 2.0, zz, bay - 1.3, eps, FLOOR_H - 1.2, LAYERS[layer])


def add_context_building(name, x, y, floors, w, d):
    add_volume(name, x, y, floors, w, d, "NP_Massing_Light", LAYERS["NP_Massing_Light"], grid_faces=True)


def add_people_and_trees():
    for idx, (x, y) in enumerate([(-20, -24), (2, -28), (18, -22), (36, -25), (58, -21), (-44, -20)]):
        add_box("NP_Trees_People", "person_%02d" % idx, x, y, 0, 0.35, 0.35, 1.8, (245, 245, 238))
    for idx, (x, y, h) in enumerate([(-34, -18, 6), (-12, -30, 5), (24, -28, 7), (52, -24, 6), (72, -20, 5)]):
        add_box("NP_Trees_People", "tree_trunk_%02d" % idx, x - 0.18, y - 0.18, 0, 0.36, 0.36, h * 0.45, (92, 72, 52))
        add_box("NP_Trees_People", "tree_crown_%02d" % idx, x - 1.2, y - 1.2, h * 0.45, 2.4, 2.4, h * 0.55, (100, 130, 98))


def add_section_cut():
    # Black section-like slabs echo the AA/BB drawings and help show scale/floor rhythm.
    x = -6
    y = -10
    w = 22
    d = 1.0
    for f in range(0, 9):
        add_box("NP_Section_Cuts", "section_slab_%02d" % f, x, y, f * FLOOR_H, w, d, 0.18, LAYERS["NP_Section_Cuts"])
    add_box("NP_Section_Cuts", "section_wall_w", x, y, 0, 0.25, d, 8 * FLOOR_H, LAYERS["NP_Section_Cuts"])
    add_box("NP_Section_Cuts", "section_wall_e", x + w - 0.25, y, 0, 0.25, d, 8 * FLOOR_H, LAYERS["NP_Section_Cuts"])


def main():
    for layer, color in LAYERS.items():
        ensure_layer(layer, color)
        removed = cleanup_layer(layer)
        print("cleanup %s %d" % (layer, removed))

    # Site plinth, lightly sloped-looking base is simplified as a large board.
    add_box("NP_Site_Base", "site_plinth", -70, -45, -1.0, 155, 105, 1.0, LAYERS["NP_Site_Base"])

    # Main complex dimensions, inferred from sections and model photos.
    # Floor-to-floor: 3.3 m. Tall tower: 34F. Left tower: 31F.
    add_tower_with_stepped_side(
        "left_tower",
        -38, -3, 23, 25, 31,
        "east",
        [
            (-15, -3, 14, 25, 25),
            (-1, -3, 10, 25, 20),
            (9, -3, 8, 25, 15),
            (17, -3, 7, 25, 11),
            (24, -3, 7, 25, 8),
        ],
    )
    add_tower_with_stepped_side(
        "right_tower",
        25, -4, 24, 26, 34,
        "west",
        [
            (10, -4, 15, 26, 23),
            (0, -4, 10, 26, 17),
            (-8, -4, 8, 26, 12),
            (-15, -4, 7, 26, 8),
        ],
    )

    # Courtyard/podium pieces between and around towers.
    add_volume("front_market_podium", -42, -26, 8, 72, 23, "NP_Massing_Wood")
    add_volume("central_courtyard_block", -12, -3, 8, 34, 27, "NP_Massing_Wood")
    add_volume("rear_link_block", -6, 22, 10, 36, 15, "NP_Massing_Wood")
    add_volume("right_low_wing", 49, -4, 8, 31, 25, "NP_Massing_Wood")
    add_volume("left_rear_midrise", -61, 3, 14, 18, 23, "NP_Massing_Wood")

    # Context blocks visible in the model/photos.
    add_context_building("context_white_east_block", 84, -14, 6, 28, 22)
    add_context_building("context_small_west_block", -72, -12, 6, 18, 18)
    add_context_building("context_low_south_block", -61, -31, 5, 25, 14)

    # Key roof terraces and stepped deck surfaces.
    for i, (x, y, w, d, floors) in enumerate([
        (-42, -26, 72, 23, 8),
        (-12, -3, 34, 27, 8),
        (-6, 22, 36, 15, 10),
        (49, -4, 31, 25, 8),
        (-61, 3, 18, 23, 14),
    ]):
        add_terrace(x, y, floors * FLOOR_H, w, d, "roof_deck_%02d" % (i + 1))

    # Selective dark glazing panels on main front faces.
    add_window_panels("left_tower_south", -38, -3, 0, 23, 31, -3)
    add_window_panels("right_tower_south", 25, -4, 0, 24, 34, -4)
    add_window_panels("front_podium_south", -42, -26, 0, 72, 8, -26)

    add_section_cut()
    add_people_and_trees()

    report = {
        "scale_assumptions": {
            "floor_to_floor_m": FLOOR_H,
            "facade_bay_m": GRID,
            "left_tower_floors": 31,
            "right_tower_floors": 34,
        },
        "main_dimensions_m": {
            "overall_site_board": [155, 105],
            "complex_approx_bbox": [152, 82, 112.2],
            "left_tower": [23, 25, round(31 * FLOOR_H, 1)],
            "right_tower": [24, 26, round(34 * FLOOR_H, 1)],
            "front_podium": [72, 23, round(8 * FLOOR_H, 1)],
        },
        "layers": list(LAYERS.keys()),
    }
    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\nacka_port_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("built Nacka Port approximation")
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
