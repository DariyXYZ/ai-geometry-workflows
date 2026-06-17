import json
import math
import os
import subprocess
import sys
import tempfile

from shapely.geometry import Polygon
from shapely.ops import unary_union

CLIENT = r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py"

SITE = [
    (-39.220, 695.784),
    (124.755, 757.214),
    (138.773, 721.042),
    (76.720, 697.005),
    (73.911, 694.218),
    (83.445, 672.311),
    (75.617, 664.102),
    (11.753, 633.935),
    (-4.868, 634.724),
    (-22.845, 651.573),
]
SITE_POLY = Polygon(SITE)
FLOOR_H = 3.6
MAX_H = 70.0


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


def cleanup_layer(layer):
    try:
        ids = call("filter_objects", {"layer": layer}).get("ids", [])
        for oid in ids:
            safe_delete(oid)
        return len(ids)
    except Exception:
        return 0


def ensure_layer(name, color):
    try:
        call("add_layer", {"name": name, "color": list(color)})
    except Exception:
        pass


def set_props(oid, layer, name, color):
    call("set_object_layer", {"object_id": oid, "layer": layer})
    call("set_object_name", {"object_id": oid, "name": name})
    call("set_object_color", {"object_id": oid, "color": list(color)})


def centroid(poly):
    p = Polygon(poly).centroid
    return (p.x, p.y)


def scale_about(poly, factor, shift=(0.0, 0.0)):
    cx, cy = centroid(poly)
    return [
        (cx + (x - cx) * factor + shift[0], cy + (y - cy) * factor + shift[1])
        for x, y in poly
    ]


def rotate_about(poly, deg, shift=(0.0, 0.0)):
    cx, cy = centroid(poly)
    rad = math.radians(deg)
    c = math.cos(rad)
    s = math.sin(rad)
    out = []
    for x, y in poly:
        dx = x - cx
        dy = y - cy
        out.append((cx + dx * c - dy * s + shift[0], cy + dx * s + dy * c + shift[1]))
    return out


def section_points(poly, z):
    return [[x, y, z] for x, y in poly] + [[poly[0][0], poly[0][1], z]]


def loft_part(layer, part, color):
    curve_ids = []
    for sec in part["sections"]:
        r = call("add_polyline", {"points": section_points(sec["poly"], sec["z"])})
        curve_ids.append(r["id"])
    solid = call("add_loft", {"ids": curve_ids})["ids"][0]
    for cid in curve_ids:
        safe_delete(cid)
    set_props(solid, layer, part["name"], color)
    return solid


def add_contour(layer, name, poly, z, color):
    r = call("add_polyline", {"points": section_points(poly, z)})
    cid = r["id"]
    set_props(cid, layer, name, color)
    return cid


def interp_poly(sections, z):
    if z <= sections[0]["z"]:
        return sections[0]["poly"]
    if z >= sections[-1]["z"]:
        return sections[-1]["poly"]
    for a, b in zip(sections[:-1], sections[1:]):
        if a["z"] <= z <= b["z"]:
            span = b["z"] - a["z"]
            t = 0.0 if span == 0 else (z - a["z"]) / span
            return [
                (pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t)
                for pa, pb in zip(a["poly"], b["poly"])
            ]
    return sections[-1]["poly"]


def validate_variant(variant):
    for part in variant["parts"]:
        for sec in part["sections"]:
            if sec["z"] < -0.001 or sec["z"] > MAX_H + 0.001:
                raise ValueError("%s exceeds height limit" % part["name"])
            p = Polygon(sec["poly"])
            if not SITE_POLY.buffer(0.02).covers(p):
                raise ValueError("%s outside redline at z %.1f" % (part["name"], sec["z"]))


def floor_union_area(parts, z):
    polys = []
    for part in parts:
        z0 = part["sections"][0]["z"]
        z1 = part["sections"][-1]["z"]
        if z0 <= z < z1 - 0.001:
            polys.append(Polygon(interp_poly(part["sections"], z)))
    if not polys:
        return 0.0
    return unary_union(polys).area


def variant_metrics(variant):
    max_z = max(part["sections"][-1]["z"] for part in variant["parts"])
    floors = int(math.ceil(max_z / FLOOR_H - 1e-6))
    floor_rows = []
    total = 0.0
    for i in range(floors):
        z = i * FLOOR_H
        area = floor_union_area(variant["parts"], z)
        if area > 0.01:
            floor_rows.append((i + 1, z, area))
            total += area
    all_points = []
    for part in variant["parts"]:
        for sec in part["sections"]:
            all_points.extend(sec["poly"])
    xs = [p[0] for p in all_points]
    ys = [p[1] for p in all_points]
    return {
        "gross_area": total,
        "floors": len(floor_rows),
        "height": max_z,
        "bbox": (min(xs), min(ys), max(xs), max(ys)),
        "floor_rows": floor_rows,
    }


def make_variants():
    v1_base = [
        (-28.0, 688.0),
        (-12.0, 654.0),
        (18.0, 642.0),
        (68.0, 666.0),
        (70.0, 674.0),
        (62.0, 690.0),
        (118.0, 721.0),
        (105.0, 744.0),
    ]
    v1_mid = scale_about(v1_base, 0.84, (6.0, 5.0))
    v1_top = scale_about(v1_base, 0.52, (16.0, 10.0))

    v2_w = [
        (-30.0, 684.0),
        (-13.0, 657.0),
        (13.0, 647.0),
        (53.0, 671.0),
        (46.0, 692.0),
        (-16.0, 695.0),
    ]
    v2_e = [
        (48.0, 685.0),
        (76.0, 697.0),
        (127.0, 718.0),
        (116.0, 746.0),
        (72.0, 730.0),
        (58.0, 708.0),
    ]
    v2_p = [
        (-22.0, 681.0),
        (0.0, 650.0),
        (57.0, 676.0),
        (61.0, 689.0),
        (37.0, 700.0),
        (-18.0, 694.0),
    ]

    v3_w = [
        (-21.0, 681.0),
        (1.0, 655.0),
        (37.0, 671.0),
        (33.0, 696.0),
        (-10.0, 694.0),
    ]
    v3_e = [
        (68.0, 700.0),
        (94.0, 708.0),
        (126.0, 721.0),
        (116.0, 748.0),
        (80.0, 735.0),
        (59.0, 710.0),
    ]
    v3_low_w = [
        (-25.0, 683.0),
        (-5.0, 650.0),
        (51.0, 675.0),
        (44.0, 692.0),
        (-18.0, 694.0),
    ]
    v3_low_e = [
        (76.0, 698.0),
        (95.0, 705.0),
        (129.0, 721.0),
        (118.0, 747.0),
        (80.0, 734.0),
    ]

    return [
        {
            "key": "V1",
            "layer": "TEP_Massing_V1_River_Fan",
            "color": (230, 110, 70),
            "description": "single tapered fan volume, terraces and prow pulled toward the river",
            "parts": [
                {
                    "name": "V1_River_Fan_main",
                    "sections": [
                        {"z": 0.0, "poly": v1_base},
                        {"z": 14.4, "poly": scale_about(v1_base, 0.94, (3.0, 2.0))},
                        {"z": 43.2, "poly": v1_mid},
                        {"z": 64.8, "poly": v1_top},
                    ],
                }
            ],
        },
        {
            "key": "V2",
            "layer": "TEP_Massing_V2_Terraced_Crescent",
            "color": (70, 150, 210),
            "description": "two terraced wings frame a central river-view court",
            "parts": [
                {
                    "name": "V2_Low_public_plinth",
                    "sections": [
                        {"z": 0.0, "poly": v2_p},
                        {"z": 10.8, "poly": scale_about(v2_p, 0.95, (2.0, 2.0))},
                    ],
                },
                {
                    "name": "V2_West_terrace_wing",
                    "sections": [
                        {"z": 10.8, "poly": v2_w},
                        {"z": 32.4, "poly": scale_about(v2_w, 0.86, (2.0, 4.0))},
                        {"z": 50.4, "poly": scale_about(v2_w, 0.68, (7.0, 8.0))},
                    ],
                },
                {
                    "name": "V2_River_gallery_wing",
                    "sections": [
                        {"z": 0.0, "poly": v2_e},
                        {"z": 21.6, "poly": scale_about(v2_e, 0.88, (-2.0, 1.5))},
                        {"z": 39.6, "poly": scale_about(v2_e, 0.70, (-5.0, 2.0))},
                    ],
                },
            ],
        },
        {
            "key": "V3",
            "layer": "TEP_Massing_V3_Twin_Beacons",
            "color": (120, 185, 95),
            "description": "two slender markers leave a clear view slot to the river",
            "parts": [
                {
                    "name": "V3_West_low_base",
                    "sections": [
                        {"z": 0.0, "poly": v3_low_w},
                        {"z": 10.8, "poly": scale_about(v3_low_w, 0.92, (2.0, 2.0))},
                    ],
                },
                {
                    "name": "V3_River_low_base",
                    "sections": [
                        {"z": 0.0, "poly": v3_low_e},
                        {"z": 10.8, "poly": scale_about(v3_low_e, 0.90, (-2.0, 2.0))},
                    ],
                },
                {
                    "name": "V3_West_beacon",
                    "sections": [
                        {"z": 10.8, "poly": v3_w},
                        {"z": 39.6, "poly": rotate_about(scale_about(v3_w, 0.76, (3.0, 4.0)), -5.0)},
                        {"z": 57.6, "poly": rotate_about(scale_about(v3_w, 0.58, (8.0, 7.0)), -8.0)},
                    ],
                },
                {
                    "name": "V3_River_beacon",
                    "sections": [
                        {"z": 10.8, "poly": v3_e},
                        {"z": 43.2, "poly": rotate_about(scale_about(v3_e, 0.72, (-3.0, 2.0)), 4.0)},
                        {"z": 68.4, "poly": rotate_about(scale_about(v3_e, 0.52, (-8.0, 4.0)), 7.0)},
                    ],
                },
            ],
        },
    ]


def main():
    variants = make_variants()
    report = {}
    for variant in variants:
        validate_variant(variant)
        ensure_layer(variant["layer"], variant["color"])
        removed = cleanup_layer(variant["layer"])
        print("cleanup %s %d" % (variant["layer"], removed))
        for part in variant["parts"]:
            loft_part(variant["layer"], part, variant["color"])

        metrics = variant_metrics(variant)
        contour_color = tuple(max(0, int(c * 0.62)) for c in variant["color"])
        for floor, z, area in metrics["floor_rows"]:
            polys = []
            for part in variant["parts"]:
                if part["sections"][0]["z"] <= z < part["sections"][-1]["z"] - 0.001:
                    polys.append(Polygon(interp_poly(part["sections"], z)))
            unioned = unary_union(polys)
            geoms = list(unioned.geoms) if hasattr(unioned, "geoms") else [unioned]
            for j, geom in enumerate(geoms):
                if geom.area > 0.01:
                    add_contour(
                        variant["layer"],
                        "%s_contour_F%02d_%02d" % (variant["key"], floor, j + 1),
                        list(geom.exterior.coords)[:-1],
                        z,
                        contour_color,
                    )
        bbox = metrics["bbox"]
        report[variant["key"]] = {
            "layer": variant["layer"],
            "description": variant["description"],
            "gross_area_m2": round(metrics["gross_area"], 1),
            "floors_by_contour": metrics["floors"],
            "height_m": round(metrics["height"], 1),
            "dimensions_m": [
                round(bbox[2] - bbox[0], 1),
                round(bbox[3] - bbox[1], 1),
                round(metrics["height"], 1),
            ],
            "bbox": [round(v, 1) for v in bbox],
        }
        print("report %s area %.1f height %.1f" % (variant["key"], metrics["gross_area"], metrics["height"]))

    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\teps_massing_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
