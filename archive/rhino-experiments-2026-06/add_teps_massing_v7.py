import importlib.util
import json
import math

SPEC = importlib.util.spec_from_file_location(
    "teps_base",
    r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\build_teps_massing_variants.py",
)
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)

LAYER = "TEP_Massing_V7_Unity_River_Cascade"
BODY_COLOR = (153, 178, 138)
PLATFORM_COLOR = (128, 151, 119)
CONTOUR_COLOR = (46, 92, 61)
TERRACE_COLOR = (99, 138, 83)
FLOOR_H = 3.6
PLATFORM_FLOORS = 1
PLATFORM_H = PLATFORM_FLOORS * FLOOR_H

PLATFORM = [
    (-26.0, 686.0),
    (-7.0, 652.0),
    (17.0, 642.0),
    (66.0, 665.0),
    (72.0, 680.0),
    (60.0, 704.0),
    (100.0, 724.0),
    (92.0, 743.0),
    (36.0, 720.0),
    (-14.0, 695.0),
]

BARS = [
    {"name": "V7_Cascade_Slice_01_CityHigh", "cx": 0.0, "cy": 670.0, "length": 36.0, "depth": 15.0, "angle": 114.0, "floors": 15},
    {"name": "V7_Cascade_Slice_02", "cx": 22.0, "cy": 680.0, "length": 42.0, "depth": 15.0, "angle": 114.0, "floors": 14},
    {"name": "V7_Cascade_Slice_03", "cx": 45.0, "cy": 692.0, "length": 46.0, "depth": 15.0, "angle": 114.0, "floors": 13},
    {"name": "V7_Cascade_Slice_04", "cx": 63.0, "cy": 708.0, "length": 32.0, "depth": 14.0, "angle": 114.0, "floors": 11},
    {"name": "V7_Cascade_Slice_05_River", "cx": 92.0, "cy": 724.0, "length": 30.0, "depth": 14.0, "angle": 114.0, "floors": 9},
    {"name": "V7_Cascade_Slice_06_RiverLow", "cx": 112.0, "cy": 733.0, "length": 24.0, "depth": 12.0, "angle": 114.0, "floors": 7},
]


def rect(cx, cy, length, depth, angle):
    a = math.radians(angle)
    ca = math.cos(a)
    sa = math.sin(a)
    hl = length / 2.0
    hd = depth / 2.0
    return [
        (cx + x * ca - y * sa, cy + x * sa + y * ca)
        for x, y in [(-hl, -hd), (hl, -hd), (hl, hd), (-hl, hd)]
    ]


def plate(bar, floor_index):
    # Higher floors step back from the river side, making visible roof/balcony terraces.
    return rect(
        bar["cx"] - 0.32 * floor_index,
        bar["cy"] - 0.20 * floor_index,
        bar["length"] - 0.10 * floor_index,
        bar["depth"] - 0.16 * floor_index,
        bar["angle"],
    )


def validate_poly(poly, name):
    p = b.Polygon(poly)
    if not p.is_valid:
        raise ValueError("%s invalid polygon" % name)
    if not b.SITE_POLY.buffer(0.02).covers(p):
        raise ValueError("%s outside redline" % name)


def make_slab(poly, z0, z1, name, color):
    ids = []
    for z in [z0, z1]:
        ids.append(b.call("add_polyline", {"points": b.section_points(poly, z)})["id"])
    sid = b.call("add_loft", {"ids": ids})["ids"][0]
    for cid in ids:
        b.safe_delete(cid)
    b.set_props(sid, LAYER, name, color)
    return sid


def add_terrace_band(name, lower_poly, upper_poly, z):
    terrace = b.Polygon(lower_poly).difference(b.Polygon(upper_poly))
    geoms = list(terrace.geoms) if hasattr(terrace, "geoms") else [terrace]
    for j, geom in enumerate(geoms):
        if geom.area > 2.0:
            b.add_contour(
                LAYER,
                "%s_terrace_%02d" % (name, j + 1),
                list(geom.exterior.coords)[:-1],
                z,
                TERRACE_COLOR,
            )


def main():
    b.ensure_layer(LAYER, BODY_COLOR)
    removed = b.cleanup_layer(LAYER)
    print("cleanup %s %d" % (LAYER, removed))

    validate_poly(PLATFORM, "V7_Platform")
    make_slab(PLATFORM, 0.0, PLATFORM_H, "V7_Simple_Landscape_Platform", PLATFORM_COLOR)
    b.add_contour(LAYER, "V7_platform_roof_contour", PLATFORM, PLATFORM_H, CONTOUR_COLOR)

    gross = b.Polygon(PLATFORM).area * PLATFORM_FLOORS
    all_points = list(PLATFORM)
    max_h = PLATFORM_H
    bar_reports = []

    for bar in BARS:
        plates = []
        for i in range(bar["floors"]):
            poly = plate(bar, i)
            validate_poly(poly, "%s_floor_%02d" % (bar["name"], i + 1))
            plates.append(poly)

        for i, poly in enumerate(plates):
            z0 = PLATFORM_H + i * FLOOR_H
            z1 = PLATFORM_H + (i + 1) * FLOOR_H
            make_slab(poly, z0, z1, "%s_res_floor_%02d" % (bar["name"], i + 1), BODY_COLOR)
            b.add_contour(LAYER, "%s_contour_F%02d" % (bar["name"], i + 1), poly, z0, CONTOUR_COLOR)
            gross += b.Polygon(poly).area
            max_h = max(max_h, z1)
            all_points.extend(poly)

        for i in range(len(plates) - 1):
            add_terrace_band("%s_F%02d" % (bar["name"], i + 1), plates[i], plates[i + 1], PLATFORM_H + (i + 1) * FLOOR_H)

        bar_reports.append({
            "name": bar["name"],
            "floors": bar["floors"],
            "nominal_depth_m": bar["depth"],
            "base_plate_m2": round(bar["length"] * bar["depth"], 1),
            "height_m": round(PLATFORM_H + bar["floors"] * FLOOR_H, 1),
        })

    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    report = {
        "V7": {
            "layer": LAYER,
            "description": "unified BIG-like eco cascade: one simple low landscape platform plus a rhythmic chain of shallow residential slices stepping down toward the river",
            "gross_area_m2": round(gross, 1),
            "height_m": round(max_h, 1),
            "floors_by_contour": int(round(max_h / FLOOR_H)),
            "dimensions_m": [round(max(xs) - min(xs), 1), round(max(ys) - min(ys), 1), round(max_h, 1)],
            "bbox": [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)],
            "platform_floors": PLATFORM_FLOORS,
            "bars": bar_reports,
        }
    }
    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\teps_massing_v7_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("report V7 area %.1f height %.1f" % (gross, max_h))
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
