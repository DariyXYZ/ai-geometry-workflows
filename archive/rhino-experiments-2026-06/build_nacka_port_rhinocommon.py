import json
import os

import Rhino
import scriptcontext as sc
from System.Drawing import Color

doc = Rhino.RhinoDoc.ActiveDoc

FLOOR_H = 3.3
BAY = 3.6

LAYERS = {
    "NP_Site_Base": Color.FromArgb(235, 235, 230),
    "NP_Massing_Wood": Color.FromArgb(126, 93, 65),
    "NP_Massing_Light": Color.FromArgb(214, 214, 208),
    "NP_Facade_Frames": Color.FromArgb(198, 176, 145),
    "NP_Glass_Dark": Color.FromArgb(72, 82, 84),
    "NP_Terraces": Color.FromArgb(154, 119, 82),
    "NP_Section_Cuts": Color.FromArgb(35, 35, 35),
    "NP_Context_Detail": Color.FromArgb(108, 132, 100),
}


def clear_scene():
    ids = [obj.Id for obj in doc.Objects]
    for oid in ids:
        doc.Objects.Delete(oid, True)
    for layer in doc.Layers:
        if layer is not None:
            layer.IsVisible = True
            layer.IsLocked = False
    return len(ids)


def layer_index(name):
    idx = doc.Layers.FindByFullPath(name, -1)
    if idx >= 0:
        return idx
    layer = Rhino.DocObjects.Layer()
    layer.Name = name
    layer.Color = LAYERS.get(name, Color.White)
    return doc.Layers.Add(layer)


def attrs(layer, name=None, color=None):
    a = Rhino.DocObjects.ObjectAttributes()
    a.LayerIndex = layer_index(layer)
    if name:
        a.Name = name
    if color is not None:
        a.ObjectColor = color
        a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
    return a


def box(layer, name, x, y, z, sx, sy, sz, color=None):
    bb = Rhino.Geometry.BoundingBox(
        Rhino.Geometry.Point3d(x, y, z),
        Rhino.Geometry.Point3d(x + sx, y + sy, z + sz),
    )
    brep = Rhino.Geometry.Brep.CreateFromBox(bb)
    return doc.Objects.AddBrep(brep, attrs(layer, name, color))


def volume(name, x, y, floors, w, d, layer="NP_Massing_Wood"):
    box(layer, name, x, y, 0, w, d, floors * FLOOR_H)


def grid_south(prefix, x, y, w, floors, z0=0):
    eps = 0.14
    frame = 0.16
    n = int(round(w / BAY))
    for k in range(n + 1):
        xx = x + min(w, k * BAY)
        box("NP_Facade_Frames", "%s_v%02d" % (prefix, k), xx - frame / 2, y - eps, z0, frame, eps, floors * FLOOR_H)
    for f in range(floors + 1):
        zz = z0 + f * FLOOR_H
        box("NP_Facade_Frames", "%s_h%02d" % (prefix, f), x, y - eps, zz - frame / 2, w, eps, frame)


def grid_north(prefix, x, y, w, d, floors):
    grid_south(prefix, x, y + d, w, floors)


def grid_east(prefix, x, y, d, floors, z0=0):
    eps = 0.14
    frame = 0.16
    n = int(round(d / BAY))
    for k in range(n + 1):
        yy = y + min(d, k * BAY)
        box("NP_Facade_Frames", "%s_v%02d" % (prefix, k), x, yy - frame / 2, z0, eps, frame, floors * FLOOR_H)
    for f in range(floors + 1):
        zz = z0 + f * FLOOR_H
        box("NP_Facade_Frames", "%s_h%02d" % (prefix, f), x, y, zz - frame / 2, eps, d, frame)


def grid_west(prefix, x, y, d, floors):
    grid_east(prefix, x - 0.14, y, d, floors)


def terrace(name, x, y, floors, w, d):
    z = floors * FLOOR_H
    box("NP_Terraces", name, x, y, z + 0.04, w, d, 0.22)
    rail = 0.18
    box("NP_Facade_Frames", name + "_rail_s", x, y, z + 0.35, w, rail, 0.35)
    box("NP_Facade_Frames", name + "_rail_n", x, y + d - rail, z + 0.35, w, rail, 0.35)
    box("NP_Facade_Frames", name + "_rail_w", x, y, z + 0.35, rail, d, 0.35)
    box("NP_Facade_Frames", name + "_rail_e", x + w - rail, y, z + 0.35, rail, d, 0.35)


def dark_panels(prefix, x, y, w, floors):
    n = int(round(w / BAY))
    for f in range(2, floors, 3):
        for k in range(n):
            if (k + f) % 3 == 0:
                xx = x + k * BAY + 0.55
                zz = f * FLOOR_H + 0.55
                box("NP_Glass_Dark", "%s_%02d_%02d" % (prefix, f, k), xx, y - 0.18, zz, BAY - 1.1, 0.08, FLOOR_H - 1.0)


def section_stack():
    x, y, w, d = -4, -13, 20, 1.0
    for f in range(9):
        box("NP_Section_Cuts", "section_slab_%02d" % f, x, y, f * FLOOR_H, w, d, 0.2)
    box("NP_Section_Cuts", "section_wall_w", x, y, 0, 0.25, d, 8 * FLOOR_H)
    box("NP_Section_Cuts", "section_wall_e", x + w - 0.25, y, 0, 0.25, d, 8 * FLOOR_H)


def people_trees():
    for i, (x, y) in enumerate([(-22, -31), (0, -30), (22, -28), (45, -28), (66, -24)]):
        box("NP_Context_Detail", "person_%02d" % i, x, y, 0, 0.35, 0.35, 1.75, Color.FromArgb(245, 245, 238))
    for i, (x, y) in enumerate([(-42, -24), (-18, -35), (28, -31), (57, -28), (75, -20)]):
        box("NP_Context_Detail", "tree_trunk_%02d" % i, x - 0.15, y - 0.15, 0, 0.3, 0.3, 2.7, Color.FromArgb(92, 72, 52))
        box("NP_Context_Detail", "tree_crown_%02d" % i, x - 1.2, y - 1.2, 2.6, 2.4, 2.4, 3.2, Color.FromArgb(105, 132, 96))


def build():
    deleted = clear_scene()
    for name in LAYERS:
        layer_index(name)

    box("NP_Site_Base", "site_plinth", -70, -45, -1.0, 155, 105, 1.0)

    # Main Nacka Port massing: two high towers, low public plinth, central stepped valley.
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

    # White context blocks from model photos/sections.
    volume("context_white_east_6F", 84, -14, 6, 28, 22, "NP_Massing_Light")
    volume("context_white_west_6F", -72, -12, 6, 18, 18, "NP_Massing_Light")
    volume("context_low_south_5F", -61, -31, 5, 25, 14, "NP_Massing_Light")

    # Characteristic grid, focused on primary readable facades.
    grid_south("left_main_s", -38, -3, 23, 31)
    grid_west("left_main_w", -38, -3, 25, 31)
    grid_north("left_main_n", -38, -3, 23, 25, 31)
    grid_south("right_main_s", 25, -4, 24, 34)
    grid_east("right_main_e", 49, -4, 26, 34)
    grid_north("right_main_n", 25, -4, 24, 26, 34)
    grid_south("podium_s", -42, -26, 72, 8)
    grid_south("court_s", -12, -3, 34, 8)
    grid_south("right_wing_s", 49, -4, 31, 8)
    grid_south("context_east_s", 84, -14, 28, 6)

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
    section_stack()
    people_trees()

    doc.Views.Redraw()
    report = {
        "deleted_before_build": deleted,
        "floor_to_floor_m": FLOOR_H,
        "facade_bay_m": BAY,
        "left_tower_floors": 31,
        "right_tower_floors": 34,
        "left_tower_height_m": round(31 * FLOOR_H, 1),
        "right_tower_height_m": round(34 * FLOOR_H, 1),
        "overall_site_board_m": [155, 105],
        "main_complex_estimated_bbox_m": [152, 82, round(34 * FLOOR_H, 1)],
        "object_count": doc.Objects.Count,
    }
    out = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\nacka_port_report.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("Built Nacka Port model. Objects: %d" % doc.Objects.Count)


build()
