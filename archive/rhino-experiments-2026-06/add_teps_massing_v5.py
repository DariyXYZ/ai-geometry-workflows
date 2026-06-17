import importlib.util
import json

SPEC = importlib.util.spec_from_file_location(
    "teps_base",
    r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\build_teps_massing_variants.py",
)
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)

FLOORS = 16
FLOOR_H = 3.6
LAYER = "TEP_Massing_V5_BIG_River_Cascade"
COLOR = (145, 176, 128)
CONTOUR_COLOR = (72, 112, 72)
TERRACE_COLOR = (96, 138, 86)

BASE = [
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


def plate(i):
    pts = []
    for idx, (x, y) in enumerate(BASE):
        if idx in [0, 1, 2, 9]:
            dx, dy = (0.18 * i, 0.06 * i)
        elif idx == 3:
            dx, dy = (-0.15 * i, 0.20 * i)
        elif idx == 4:
            dx, dy = (-0.45 * i, 0.35 * i)
        elif idx == 5:
            dx, dy = (-0.70 * i, 0.05 * i)
        elif idx in [6, 7]:
            dx, dy = (-1.65 * i, -0.95 * i)
        elif idx == 8:
            dx, dy = (-0.75 * i, -0.45 * i)
        pts.append((x + dx, y + dy))
    return pts


def make_slab(poly, z0, z1, name):
    ids = []
    for z in [z0, z1]:
        ids.append(b.call("add_polyline", {"points": b.section_points(poly, z)})["id"])
    sid = b.call("add_loft", {"ids": ids})["ids"][0]
    for cid in ids:
        b.safe_delete(cid)
    b.set_props(sid, LAYER, name, COLOR)
    return sid


def validate_plates(plates):
    for i, poly in enumerate(plates):
        p = b.Polygon(poly)
        if not p.is_valid:
            raise ValueError("V5 invalid floor polygon %02d" % (i + 1))
        if not b.SITE_POLY.buffer(0.02).covers(p):
            raise ValueError("V5 floor %02d outside redline" % (i + 1))


def main():
    b.ensure_layer(LAYER, COLOR)
    removed = b.cleanup_layer(LAYER)
    print("cleanup %s %d" % (LAYER, removed))

    plates = [plate(i) for i in range(FLOORS)]
    validate_plates(plates)

    gross = 0.0
    all_points = []

    for i, poly in enumerate(plates):
        z0 = i * FLOOR_H
        z1 = (i + 1) * FLOOR_H
        make_slab(poly, z0, z1, "V5_residential_floor_%02d" % (i + 1))
        b.add_contour(LAYER, "V5_contour_F%02d" % (i + 1), poly, z0, CONTOUR_COLOR)
        area = b.Polygon(poly).area
        gross += area
        all_points.extend(poly)

    for i in range(FLOORS - 1):
        lower = b.Polygon(plates[i])
        upper = b.Polygon(plates[i + 1])
        terrace = lower.difference(upper)
        z = (i + 1) * FLOOR_H
        geoms = list(terrace.geoms) if hasattr(terrace, "geoms") else [terrace]
        for j, geom in enumerate(geoms):
            if geom.area > 4.0:
                b.add_contour(
                    LAYER,
                    "V5_river_terrace_band_F%02d_%02d" % (i + 1, j + 1),
                    list(geom.exterior.coords)[:-1],
                    z,
                    TERRACE_COLOR,
                )

    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    height = FLOORS * FLOOR_H
    report = {
        "V5": {
            "layer": LAYER,
            "description": "calm BIG-inspired eco-residential cascade: regular floor plates, continuous river-facing balcony terraces, no twisted facades",
            "gross_area_m2": round(gross, 1),
            "floors_by_contour": FLOORS,
            "height_m": round(height, 1),
            "dimensions_m": [
                round(max(xs) - min(xs), 1),
                round(max(ys) - min(ys), 1),
                round(height, 1),
            ],
            "bbox": [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)],
            "avg_floor_plate_m2": round(gross / FLOORS, 1),
            "top_floor_plate_m2": round(b.Polygon(plates[-1]).area, 1),
            "base_floor_plate_m2": round(b.Polygon(plates[0]).area, 1),
        }
    }
    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\teps_massing_v5_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("report V5 area %.1f height %.1f" % (gross, height))
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
