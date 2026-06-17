import importlib.util
import json

SPEC = importlib.util.spec_from_file_location(
    "teps_base",
    r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\build_teps_massing_variants.py",
)
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


def make_v4():
    podium = [
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
    high_spine = [
        (-22.0, 682.0),
        (0.0, 653.0),
        (39.0, 670.0),
        (35.0, 695.0),
        (-12.0, 693.0),
    ]
    mid_terrace = [
        (20.0, 669.0),
        (63.0, 688.0),
        (63.0, 711.0),
        (28.0, 704.0),
        (6.0, 689.0),
    ]
    river_terrace = [
        (58.0, 704.0),
        (88.0, 708.0),
        (126.0, 722.0),
        (116.0, 747.0),
        (78.0, 734.0),
        (57.0, 715.0),
    ]

    return {
        "key": "V4",
        "layer": "TEP_Massing_V4_River_Terraces",
        "color": (190, 135, 215),
        "description": "premium residential cascade: high city-side spine, stepped river terraces, open view slot to the Moskva river",
        "parts": [
            {
                "name": "V4_Public_Podium",
                "sections": [
                    {"z": 0.0, "poly": podium},
                    {"z": 10.8, "poly": b.scale_about(podium, 0.96, (1.0, 1.0))},
                ],
            },
            {
                "name": "V4_City_Side_High_Spine",
                "sections": [
                    {"z": 10.8, "poly": high_spine},
                    {"z": 43.2, "poly": b.scale_about(high_spine, 0.78, (5.0, 4.0))},
                    {"z": 68.4, "poly": b.scale_about(high_spine, 0.58, (9.0, 8.0))},
                ],
            },
            {
                "name": "V4_Middle_Terrace_Body",
                "sections": [
                    {"z": 10.8, "poly": mid_terrace},
                    {"z": 32.4, "poly": b.scale_about(mid_terrace, 0.86, (4.0, 5.0))},
                    {"z": 54.0, "poly": b.scale_about(mid_terrace, 0.62, (8.0, 8.0))},
                ],
            },
            {
                "name": "V4_River_Front_Terrace_Body",
                "sections": [
                    {"z": 0.0, "poly": river_terrace},
                    {"z": 18.0, "poly": b.scale_about(river_terrace, 0.90, (-2.0, 1.0))},
                    {"z": 36.0, "poly": b.scale_about(river_terrace, 0.74, (-5.0, 2.0))},
                ],
            },
        ],
    }


def build_variant(variant):
    b.validate_variant(variant)
    b.ensure_layer(variant["layer"], variant["color"])
    removed = b.cleanup_layer(variant["layer"])
    print("cleanup %s %d" % (variant["layer"], removed))

    for part in variant["parts"]:
        b.loft_part(variant["layer"], part, variant["color"])

    metrics = b.variant_metrics(variant)
    contour_color = tuple(max(0, int(c * 0.62)) for c in variant["color"])
    for floor, z, area in metrics["floor_rows"]:
        polys = []
        for part in variant["parts"]:
            if part["sections"][0]["z"] <= z < part["sections"][-1]["z"] - 0.001:
                polys.append(b.Polygon(b.interp_poly(part["sections"], z)))
        unioned = b.unary_union(polys)
        geoms = list(unioned.geoms) if hasattr(unioned, "geoms") else [unioned]
        for j, geom in enumerate(geoms):
            if geom.area > 0.01:
                b.add_contour(
                    variant["layer"],
                    "%s_contour_F%02d_%02d" % (variant["key"], floor, j + 1),
                    list(geom.exterior.coords)[:-1],
                    z,
                    contour_color,
                )

    bbox = metrics["bbox"]
    report = {
        variant["key"]: {
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
    }
    out_path = r"C:\VS Code\workfiles\ai-geometry-workflows\scripts\teps_massing_v4_report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print("report V4 area %.1f height %.1f" % (metrics["gross_area"], metrics["height"]))
    print("wrote %s" % out_path)


if __name__ == "__main__":
    build_variant(make_v4())
