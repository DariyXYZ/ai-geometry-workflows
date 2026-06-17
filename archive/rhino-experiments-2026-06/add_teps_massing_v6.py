import importlib.util
import json
import math

SPEC = importlib.util.spec_from_file_location(
    "teps_base",
    r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\build_teps_massing_variants.py",
)
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)

LAYER = "TEP_Massing_V6_Cascade_Towers"
COLOR = (118, 166, 132)
PODIUM_COLOR = (132, 154, 126)
CONTOUR_COLOR = (45, 95, 62)
TERRACE_COLOR = (86, 132, 78)
FLOOR_H = 3.6
PODIUM_FLOORS = 2
PODIUM_H = PODIUM_FLOORS * FLOOR_H

PODIUMS = [
    {
        "name": "V6_Podium_West_Court",
        "poly": [(-25.0, 686.0), (-8.0, 654.0), (16.0, 645.0), (55.0, 664.0), (49.0, 683.0), (14.0, 696.0), (-14.0, 694.0)],
    },
    {
        "name": "V6_Podium_Central_Link",
        "poly": [(22.0, 674.0), (55.0, 688.0), (67.0, 701.0), (52.0, 714.0), (24.0, 703.0), (8.0, 690.0)],
    },
    {
        "name": "V6_Podium_River_Amenity",
        "poly": [(62.0, 704.0), (86.0, 706.0), (122.0, 722.0), (113.0, 747.0), (78.0, 734.0), (57.0, 716.0)],
    },
]

TOWERS = [
    {"name": "V6_West_Cascade_Tower", "cx": 6.0, "cy": 676.0, "length": 50.0, "depth": 18.0, "angle": 24.0, "floors": 12, "shift": (-0.35, -0.20)},
    {"name": "V6_Central_View_Tower", "cx": 39.0, "cy": 690.0, "length": 48.0, "depth": 17.0, "angle": 24.0, "floors": 16, "shift": (-0.35, -0.20)},
    {"name": "V6_River_Cascade_Tower", "cx": 88.0, "cy": 720.0, "length": 42.0, "depth": 16.0, "angle": 24.0, "floors": 11, "shift": (-0.35, -0.20)},
]


def rect(cx, cy, length, depth, angle):
    a = math.radians(angle)
    ca = math.cos(a)
    sa = math.sin(a)
    hl = length / 2.0
    hd = depth / 2.0
    pts = []
    for x, y in [(-hl, -hd), (hl, -hd), (hl, hd), (-hl, hd)]:
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def scale(poly, f, sx, sy):
    c = b.Polygon(poly).centroid
    return [(c.x + (x - c.x) * f + sx, c.y + (y - c.y) * f + sy) for x, y in poly]


def tower_plate(tower, floor_index):
    base = rect(tower["cx"], tower["cy"], tower["length"], tower["depth"], tower["angle"])
    f = 1.0 - 0.010 * floor_index
    sx = tower["shift"][0] * floor_index
    sy = tower["shift"][1] * floor_index
    return scale(base, f, sx, sy)


def make_slab(poly, z0, z1, name, color):
    ids = []
    for z in [z0, z1]:
        ids.append(b.call("add_polyline", {"points": b.section_points(poly, z)})["id"])
    sid = b.call("add_loft", {"ids": ids})["ids"][0]
    for cid in ids:
        b.safe_delete(cid)
    b.set_props(sid, LAYER, name, color)
    return sid


def validate_poly(poly, name):
    p = b.Polygon(poly)
    if not p.is_valid:
        raise ValueError("%s invalid polygon" % name)
    if not b.SITE_POLY.buffer(0.02).covers(p):
        raise ValueError("%s outside redline" % name)


def main():
    b.ensure_layer(LAYER, COLOR)
    removed = b.cleanup_layer(LAYER)
    print("cleanup %s %d" % (LAYER, removed))

    gross = 0.0
    all_points = []
    max_h = 0.0

    for podium in PODIUMS:
        validate_poly(podium["poly"], podium["name"])
        for f in range(PODIUM_FLOORS):
            z0 = f * FLOOR_H
            z1 = (f + 1) * FLOOR_H
            make_slab(podium["poly"], z0, z1, "%s_floor_%02d" % (podium["name"], f + 1), PODIUM_COLOR)
            gross += b.Polygon(podium["poly"]).area
            max_h = max(max_h, z1)
        b.add_contour(LAYER, "%s_roof_contour" % podium["name"], podium["poly"], PODIUM_H, CONTOUR_COLOR)
        all_points.extend(podium["poly"])

    tower_reports = []
    for tower in TOWERS:
        plates = []
        for i in range(tower["floors"]):
            poly = tower_plate(tower, i)
            validate_poly(poly, "%s_floor_%02d" % (tower["name"], i + 1))
            plates.append(poly)

        for i, poly in enumerate(plates):
            z0 = PODIUM_H + i * FLOOR_H
            z1 = PODIUM_H + (i + 1) * FLOOR_H
            make_slab(poly, z0, z1, "%s_res_floor_%02d" % (tower["name"], i + 1), COLOR)
            b.add_contour(LAYER, "%s_contour_F%02d" % (tower["name"], i + 1), poly, z0, CONTOUR_COLOR)
            gross += b.Polygon(poly).area
            max_h = max(max_h, z1)
            all_points.extend(poly)

        for i in range(len(plates) - 1):
            lower = b.Polygon(plates[i])
            upper = b.Polygon(plates[i + 1])
            terrace = lower.difference(upper)
            z = PODIUM_H + (i + 1) * FLOOR_H
            geoms = list(terrace.geoms) if hasattr(terrace, "geoms") else [terrace]
            for j, geom in enumerate(geoms):
                if geom.area > 2.0:
                    b.add_contour(
                        LAYER,
                        "%s_terrace_F%02d_%02d" % (tower["name"], i + 1, j + 1),
                        list(geom.exterior.coords)[:-1],
                        z,
                        TERRACE_COLOR,
                    )

        tower_reports.append({
            "name": tower["name"],
            "floors": tower["floors"],
            "typical_plate_m2": round(tower["length"] * tower["depth"], 1),
            "nominal_depth_m": tower["depth"],
            "height_m": round(PODIUM_H + tower["floors"] * FLOOR_H, 1),
        })

    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    report = {
        "V6": {
            "layer": LAYER,
            "description": "fragmented eco-residential massing: three slim cascading towers on a broken two-floor stylobate, with view gaps and river-facing terraces",
            "gross_area_m2": round(gross, 1),
            "height_m": round(max_h, 1),
            "floors_by_contour": int(round(max_h / FLOOR_H)),
            "dimensions_m": [round(max(xs) - min(xs), 1), round(max(ys) - min(ys), 1), round(max_h, 1)],
            "bbox": [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)],
            "podium_floors": PODIUM_FLOORS,
            "towers": tower_reports,
        }
    }
    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\teps_massing_v6_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("report V6 area %.1f height %.1f" % (gross, max_h))
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
