"""Generate a residential complex massing with three blocks and an OKN house.

The script is dependency-free and writes a lightweight OBJ/MTL preview plus a
JSON metrics report. It is intended as a Rhino massing source: import the OBJ
or port the same dimensions into RhinoCommon if a live Rhino slot is available.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "exports" / "residential-okn-massing"
OBJ_PATH = OUT_DIR / "residential_okn_massing_v1.obj"
MTL_PATH = OUT_DIR / "residential_okn_massing_v1.mtl"
REPORT_PATH = OUT_DIR / "residential_okn_massing_v1_report.json"

ROT_DEG = -32.0
VISUAL_LIFT_M = 0.001

F2F_RES = 3.15
GROUND_FLOOR = 4.2
TOP_FLOOR = 3.3


MATERIALS = {
    "site": (0.96, 0.94, 0.90),
    "residential_base": (0.72, 0.79, 0.86),
    "residential_body": (0.64, 0.72, 0.80),
    "residential_top": (0.52, 0.62, 0.72),
    "okn_brick": (0.86, 0.36, 0.16),
    "okn_roof": (0.42, 0.16, 0.09),
    "public_space": (0.66, 0.80, 0.58),
    "paving": (0.70, 0.70, 0.68),
}


@dataclass(frozen=True)
class BoxSpec:
    name: str
    cx: float
    cy: float
    lx: float
    ly: float
    z0: float
    height: float
    material: str


@dataclass(frozen=True)
class ResidentialBar:
    name: str
    cx: float
    cy: float
    lx: float
    ly: float
    floors: int
    material: str = "residential_body"
    top_setback: float = 1.8
    top_floors: int = 2

    @property
    def height(self) -> float:
        if self.floors <= 1:
            return GROUND_FLOOR
        return GROUND_FLOOR + (self.floors - 2) * F2F_RES + TOP_FLOOR

    @property
    def main_height(self) -> float:
        return max(GROUND_FLOOR, self.height - self.top_floors * TOP_FLOOR)

    @property
    def footprint_area(self) -> float:
        return self.lx * self.ly

    @property
    def approximate_gfa(self) -> float:
        return self.footprint_area * self.floors


class ObjWriter:
    def __init__(self) -> None:
        self.vertices: list[tuple[float, float, float]] = []
        self.faces: list[tuple[str, list[int]]] = []

    def add_vertex(self, point: tuple[float, float, float]) -> int:
        self.vertices.append(point)
        return len(self.vertices)

    def add_face(self, material: str, indexes: list[int]) -> None:
        self.faces.append((material, indexes))

    def write(self, obj_path: Path, mtl_path: Path) -> None:
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        with mtl_path.open("w", encoding="utf-8") as f:
            for name, rgb in MATERIALS.items():
                f.write(f"newmtl {name}\n")
                f.write(f"Kd {rgb[0]:.4f} {rgb[1]:.4f} {rgb[2]:.4f}\n")
                f.write("Ka 0.0500 0.0500 0.0500\n")
                f.write("Ks 0.0800 0.0800 0.0800\n\n")

        with obj_path.open("w", encoding="utf-8") as f:
            f.write(f"mtllib {mtl_path.name}\n")
            for x, y, z in self.vertices:
                f.write(f"v {x:.3f} {y:.3f} {z:.3f}\n")
            last_mat = None
            for material, indexes in self.faces:
                if material != last_mat:
                    f.write(f"usemtl {material}\n")
                    last_mat = material
                f.write("f " + " ".join(str(i) for i in indexes) + "\n")


def rotate_xy(x: float, y: float, deg: float = ROT_DEG) -> tuple[float, float]:
    a = math.radians(deg)
    return (
        x * math.cos(a) - y * math.sin(a),
        x * math.sin(a) + y * math.cos(a),
    )


def transform_points(points: list[tuple[float, float]], deg: float = ROT_DEG) -> list[tuple[float, float]]:
    return [rotate_xy(x, y, deg) for x, y in points]


def add_prism(writer: ObjWriter, name: str, points: list[tuple[float, float]], z0: float, z1: float, material: str) -> None:
    del name
    bottom = [writer.add_vertex((x, y, z0)) for x, y in points]
    top = [writer.add_vertex((x, y, z1)) for x, y in points]

    n = len(points)
    writer.add_face(material, list(reversed(bottom)))
    writer.add_face(material, top)
    for i in range(n):
        writer.add_face(material, [bottom[i], bottom[(i + 1) % n], top[(i + 1) % n], top[i]])


def rect_points(cx: float, cy: float, lx: float, ly: float) -> list[tuple[float, float]]:
    hx = lx / 2
    hy = ly / 2
    return [
        (cx - hx, cy - hy),
        (cx + hx, cy - hy),
        (cx + hx, cy + hy),
        (cx - hx, cy + hy),
    ]


def add_box(writer: ObjWriter, spec: BoxSpec) -> None:
    add_prism(
        writer,
        spec.name,
        transform_points(rect_points(spec.cx, spec.cy, spec.lx, spec.ly)),
        spec.z0,
        spec.z0 + spec.height,
        spec.material,
    )


def add_residential_bar(writer: ObjWriter, bar: ResidentialBar) -> None:
    add_box(
        writer,
        BoxSpec(
            f"{bar.name}_active_ground",
            bar.cx,
            bar.cy,
            bar.lx,
            bar.ly,
            0.0,
            GROUND_FLOOR,
            "residential_base",
        ),
    )

    add_box(
        writer,
        BoxSpec(
            f"{bar.name}_main_body",
            bar.cx,
            bar.cy,
            bar.lx,
            bar.ly,
            GROUND_FLOOR,
            max(0.0, bar.main_height - GROUND_FLOOR),
            bar.material,
        ),
    )

    top_lx = max(4.0, bar.lx - 2 * bar.top_setback)
    top_ly = max(4.0, bar.ly - 2 * bar.top_setback)
    add_box(
        writer,
        BoxSpec(
            f"{bar.name}_setback_top",
            bar.cx,
            bar.cy,
            top_lx,
            top_ly,
            bar.main_height,
            bar.height - bar.main_height,
            "residential_top",
        ),
    )


def add_gable_house(writer: ObjWriter, name: str, cx: float, cy: float, lx: float, ly: float) -> dict:
    wall_h = 6.8
    ridge_h = 10.8
    pts = transform_points(rect_points(cx, cy, lx, ly))
    add_prism(writer, f"{name}_brick_body", pts, 0.0, wall_h, "okn_brick")

    local = [
        (cx - lx / 2, cy - ly / 2),
        (cx + lx / 2, cy - ly / 2),
        (cx + lx / 2, cy + ly / 2),
        (cx - lx / 2, cy + ly / 2),
    ]
    roof_bottom = transform_points(local)
    ridge_a = rotate_xy(cx, cy - ly / 2)
    ridge_b = rotate_xy(cx, cy + ly / 2)
    v0, v1, v2, v3 = [writer.add_vertex((x, y, wall_h)) for x, y in roof_bottom]
    r0 = writer.add_vertex((ridge_a[0], ridge_a[1], ridge_h))
    r1 = writer.add_vertex((ridge_b[0], ridge_b[1], ridge_h))
    writer.add_face("okn_roof", [v0, v1, r0])
    writer.add_face("okn_roof", [v3, r1, v2])
    writer.add_face("okn_roof", [v0, r0, r1, v3])
    writer.add_face("okn_roof", [v1, v2, r1, r0])
    return {"name": name, "length_m": lx, "depth_m": ly, "wall_h_m": wall_h, "ridge_h_m": ridge_h}


def add_site_surfaces(writer: ObjWriter) -> None:
    site = [
        (-92, -62),
        (-64, -78),
        (-12, -70),
        (8, -86),
        (78, -52),
        (92, 12),
        (66, 44),
        (82, 72),
        (10, 86),
        (-84, 52),
        (-72, 12),
        (-96, -28),
    ]
    add_prism(writer, "site_boundary_plate", transform_points(site), -0.08, 0.0, "site")

    courtyard = [(-47, -10), (-8, -30), (14, 21), (-24, 40)]
    add_prism(writer, "central_courtyard_green", transform_points(courtyard), VISUAL_LIFT_M, 0.05, "public_space")

    public_spine = [(-72, -28), (-55, -38), (55, 30), (46, 46)]
    add_prism(writer, "diagonal_public_spine", transform_points(public_spine), VISUAL_LIFT_M, 0.04, "paving")

    okn_plaza = [(-88, -55), (-42, -72), (-35, -53), (-80, -36)]
    add_prism(writer, "okn_public_plaza", transform_points(okn_plaza), VISUAL_LIFT_M * 2, 0.06, "paving")


def build() -> dict:
    writer = ObjWriter()
    add_site_surfaces(writer)

    bars = [
        ResidentialBar("north_west_long_bar", -48, 22, 24, 116, 14),
        ResidentialBar("north_top_bar", -6, 68, 92, 24, 16),
        ResidentialBar("north_east_short_bar", 36, 40, 24, 72, 15),
        ResidentialBar("east_long_bar", 55, -8, 86, 22, 13),
        ResidentialBar("east_south_wing", 78, -38, 22, 44, 15),
        ResidentialBar("south_west_bar", -4, -58, 58, 21, 10),
        ResidentialBar("south_east_bar", 34, -48, 22, 52, 11),
    ]

    for bar in bars:
        add_residential_bar(writer, bar)

    okn = add_gable_house(writer, "okn_public_brick_house", -76, -55, 34, 16)

    total_footprint = sum(bar.footprint_area for bar in bars)
    total_gfa = sum(bar.approximate_gfa for bar in bars)
    max_height = max(bar.height for bar in bars)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    writer.write(OBJ_PATH, MTL_PATH)

    report = {
        "case_id": "residential-okn-three-block-massing-2026-06-26",
        "units": "meters",
        "source_authority": {
            "image": "user sketch: red plot, three blue residential footprints, orange OKN block",
            "scale": "inferred first-pass metric scale; replace with survey/CAD dimensions when available",
        },
        "scenario_subtype": "3A",
        "design_intent": {
            "program": "modern residential complex with public OKN house",
            "site_logic": "three residential blocks frame a diagonal public spine and central courtyard; OKN receives a small public plaza",
            "primary_operator": "height stepping and setback top floors",
            "secondary_operator": "courtyard/public-spine preservation",
        },
        "standards_used": {
            "residential_f2f_m": F2F_RES,
            "ground_floor_m": GROUND_FLOOR,
            "top_floor_m": TOP_FLOOR,
            "residential_height_band": "9-17 floors, below 75 m high-rise residential threshold",
        },
        "residential_bars": [
            {
                "name": bar.name,
                "floors": bar.floors,
                "length_m": bar.lx,
                "depth_m": bar.ly,
                "height_m": round(bar.height, 2),
                "footprint_area_m2": round(bar.footprint_area, 1),
                "approx_gfa_m2": round(bar.approximate_gfa, 1),
            }
            for bar in bars
        ],
        "okn": okn,
        "totals": {
            "residential_footprint_area_m2": round(total_footprint, 1),
            "residential_approx_gfa_m2": round(total_gfa, 1),
            "max_residential_height_m": round(max_height, 2),
            "visual_lift_m": VISUAL_LIFT_M,
        },
        "outputs": {
            "obj": str(OBJ_PATH.relative_to(ROOT)).replace("\\", "/"),
            "mtl": str(MTL_PATH.relative_to(ROOT)).replace("\\", "/"),
        },
        "warnings": [
            "No surveyed plot dimensions were provided; boundary and footprint sizes are inferred from image proportions.",
            "INSO, fire access, parking, daylight, and code compliance are not validated in this first massing pass.",
            "OKN protection zone and exact heritage envelope must be checked against source CAD/legal data.",
        ],
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    data = build()
    print(json.dumps(data["totals"], indent=2))
    print(f"Wrote {OBJ_PATH}")
    print(f"Wrote {REPORT_PATH}")

