import json
import math
import os
import subprocess
import sys
import tempfile

from shapely.geometry import box
from shapely.ops import unary_union

CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"

PITCH = 6.0
BLOCK = 5.7
FLOOR_H = 3.6
PROJECT_LAYERS = [
    "Voxel_6m_Columns",
    "Voxel_6m_Terrace_Caps",
    "Voxel_6m_Level_Contours",
    "Voxel_6m_Ground_Grid",
]


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


def cleanup_layer(layer):
    try:
        ids = call("filter_objects", {"layer": layer}).get("ids", [])
        for oid in ids:
            safe_delete(oid)
        return len(ids)
    except Exception:
        return 0


def set_props(oid, layer, name, color):
    call("set_object_layer", {"object_id": oid, "layer": layer})
    call("set_object_name", {"object_id": oid, "name": name})
    call("set_object_color", {"object_id": oid, "color": list(color)})


def add_box(layer, name, corner, size, color):
    oid = call("add_box", {"corner": list(corner), "x": size[0], "y": size[1], "z": size[2]})["id"]
    set_props(oid, layer, name, color)
    return oid


def add_polyline(layer, name, pts, color):
    oid = call("add_polyline", {"points": pts})["id"]
    set_props(oid, layer, name, color)
    return oid


def column_height_floors(i, j):
    if abs(i) + abs(j) > 8:
        return None
    if i <= -5 and j >= 3:
        return None
    if i >= 5 and j <= -3:
        return None
    if (i, j) in [(2, -2), (2, -1), (-3, 2)]:
        return None

    u = abs(i)
    v = abs(j)
    h = 50 - 4.0 * u - 3.2 * v
    if i > 1 and j > 0:
        h -= 5
    if i < -2 and j > 1:
        h -= 4
    if i < 0 and j < 0:
        h += 2
    if i == 0 and j == 0:
        h = 50
    return max(7, min(50, int(round(h / 2.0) * 2)))


def make_cells():
    cells = []
    for i in range(-5, 6):
        for j in range(-4, 5):
            h = column_height_floors(i, j)
            if h is not None:
                cells.append({"i": i, "j": j, "floors": h})
    return cells


def color_for_height(floors):
    t = (floors - 16.0) / (50.0 - 16.0)
    t = max(0.0, min(1.0, t))
    r = int(86 + 74 * t)
    g = int(126 + 52 * t)
    b = int(154 + 64 * t)
    return (r, g, b)


def cell_bounds(i, j):
    x = i * PITCH - BLOCK / 2.0
    y = j * PITCH - BLOCK / 2.0
    return x, y, x + BLOCK, y + BLOCK


def cell_corner(i, j):
    x0, y0, x1, y1 = cell_bounds(i, j)
    return x0, y0, 0.0


def add_level_contours(cells, levels):
    for level in levels:
        polys = []
        for c in cells:
            if c["floors"] >= level:
                x0, y0, x1, y1 = cell_bounds(c["i"], c["j"])
                polys.append(box(x0, y0, x1, y1))
        if not polys:
            continue
        geom = unary_union(polys)
        geoms = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
        z = level * FLOOR_H
        for k, g in enumerate(geoms):
            coords = list(g.exterior.coords)
            pts = [[x, y, z] for x, y in coords]
            add_polyline(
                "Voxel_6m_Level_Contours",
                "Contour_F%02d_%02d" % (level, k + 1),
                pts,
                (35, 58, 72),
            )


def add_ground_grid(cells):
    for c in cells:
        x0, y0, x1, y1 = cell_bounds(c["i"], c["j"])
        pts = [[x0, y0, 0.02], [x1, y0, 0.02], [x1, y1, 0.02], [x0, y1, 0.02], [x0, y0, 0.02]]
        add_polyline(
            "Voxel_6m_Ground_Grid",
            "Grid_%+d_%+d" % (c["i"], c["j"]),
            pts,
            (85, 92, 96),
        )


def add_terrace_caps(cells):
    heights = {(c["i"], c["j"]): c["floors"] for c in cells}
    count = 0
    for c in cells:
        i = c["i"]
        j = c["j"]
        h = c["floors"]
        higher_neighbor = False
        for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if heights.get((ni, nj), 0) >= h + 6:
                higher_neighbor = True
        if higher_neighbor and h >= 18:
            x0, y0, x1, y1 = cell_bounds(i, j)
            add_box(
                "Voxel_6m_Terrace_Caps",
                "Green_Roof_%+d_%+d_F%02d" % (i, j, h),
                (x0 + 0.35, y0 + 0.35, h * FLOOR_H + 0.05),
                (BLOCK - 0.7, BLOCK - 0.7, 0.18),
                (82, 132, 89),
            )
            count += 1
    return count


def main():
    layer_colors = {
        "Voxel_6m_Columns": (112, 150, 178),
        "Voxel_6m_Terrace_Caps": (82, 132, 89),
        "Voxel_6m_Level_Contours": (35, 58, 72),
        "Voxel_6m_Ground_Grid": (85, 92, 96),
    }
    for layer in PROJECT_LAYERS:
        ensure_layer(layer, layer_colors[layer])
        removed = cleanup_layer(layer)
        print("cleanup %s %d" % (layer, removed))

    cells = make_cells()
    for c in cells:
        i = c["i"]
        j = c["j"]
        floors = c["floors"]
        add_box(
            "Voxel_6m_Columns",
            "Voxel_Stack_%+d_%+d_%02dF" % (i, j, floors),
            cell_corner(i, j),
            (BLOCK, BLOCK, floors * FLOOR_H),
            color_for_height(floors),
        )

    terrace_count = add_terrace_caps(cells)
    add_level_contours(cells, [10, 20, 30, 40, 50])
    add_ground_grid(cells)

    heights = [c["floors"] for c in cells]
    xs = []
    ys = []
    for c in cells:
        x0, y0, x1, y1 = cell_bounds(c["i"], c["j"])
        xs += [x0, x1]
        ys += [y0, y1]
    report = {
        "cell_pitch_m": PITCH,
        "solid_cell_size_m": BLOCK,
        "floor_height_m": FLOOR_H,
        "max_floors": max(heights),
        "max_height_m": round(max(heights) * FLOOR_H, 1),
        "voxel_stacks": len(cells),
        "terrace_caps": terrace_count,
        "gross_area_m2": round(sum(heights) * PITCH * PITCH, 1),
        "bbox_m": [round(min(xs), 1), round(min(ys), 1), 0.0, round(max(xs), 1), round(max(ys), 1), round(max(heights) * FLOOR_H, 1)],
        "dimensions_m": [round(max(xs) - min(xs), 1), round(max(ys) - min(ys), 1), round(max(heights) * FLOOR_H, 1)],
    }
    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\voxel_skyscraper_6m_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("report area %.1f height %.1f cells %d" % (report["gross_area_m2"], report["max_height_m"], report["voxel_stacks"]))
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
