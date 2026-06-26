import json
import math

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc


BOUNDARY_LAYER = "plot boundary"
INSO_LAYER = "ИНСО ИД"
PARAMS_JSON = r'''
{
  "target_gfa": 228917.306,
  "variants": [
    {
      "layer": "AI_BC_V01",
      "strategy": "envelope_following_field",
      "parts": [
        {"name": "V01_SW_high_plate", "cx": 248, "cy": 4378, "w": 28, "d": 42, "rot": 0, "floors": 32},
        {"name": "V01_south_mid_high", "cx": 318, "cy": 4414, "w": 30, "d": 42, "rot": 0, "floors": 42},
        {"name": "V01_west_mid_high", "cx": 190, "cy": 4422, "w": 26, "d": 36, "rot": 0, "floors": 36},
        {"name": "V01_central_plate", "cx": 263, "cy": 4500, "w": 28, "d": 40, "rot": 0, "floors": 26},
        {"name": "V01_mid_terrace", "cx": 349, "cy": 4518, "w": 36, "d": 38, "rot": 0, "floors": 18},
        {"name": "V01_inner_low_plate", "cx": 382, "cy": 4453, "w": 24, "d": 40, "rot": 0, "floors": 12},
        {"name": "V01_east_low_block", "cx": 443, "cy": 4516, "w": 34, "d": 34, "rot": 0, "floors": 8},
        {"name": "V01_north_low_bar", "cx": 440, "cy": 4584, "w": 30, "d": 38, "rot": 0, "floors": 14},
        {"name": "V01_public_base_west", "cx": 275, "cy": 4448, "w": 120, "d": 22, "rot": 0, "floors": 2},
        {"name": "V01_public_base_east", "cx": 382, "cy": 4555, "w": 118, "d": 22, "rot": 0, "floors": 2}
      ]
    },
    {
      "layer": "AI_BC_V02",
      "strategy": "urban_frame_with_accents",
      "parts": [
        {"name": "V02_south_address_bar", "cx": 275, "cy": 4415, "w": 140, "d": 18, "rot": 0, "floors": 12},
        {"name": "V02_central_frame_bar", "cx": 328, "cy": 4490, "w": 126, "d": 20, "rot": 0, "floors": 12},
        {"name": "V02_north_frame_bar", "cx": 360, "cy": 4575, "w": 110, "d": 18, "rot": 0, "floors": 10},
        {"name": "V02_east_low_bar", "cx": 430, "cy": 4534, "w": 76, "d": 18, "rot": 0, "floors": 8},
        {"name": "V02_SW_accent", "cx": 240, "cy": 4382, "w": 30, "d": 42, "rot": 0, "floors": 48},
        {"name": "V02_south_mid_accent", "cx": 315, "cy": 4410, "w": 30, "d": 40, "rot": 0, "floors": 38},
        {"name": "V02_north_marker", "cx": 350, "cy": 4570, "w": 26, "d": 36, "rot": 0, "floors": 13},
        {"name": "V02_east_low_marker", "cx": 470, "cy": 4546, "w": 28, "d": 22, "rot": 0, "floors": 7},
        {"name": "V02_public_base", "cx": 345, "cy": 4520, "w": 146, "d": 28, "rot": 0, "floors": 2}
      ]
    },
    {
      "layer": "AI_BC_V03",
      "strategy": "compact_base_moderated_dominant",
      "parts": [
        {"name": "V03_moderated_dominant", "cx": 230, "cy": 4385, "w": 32, "d": 42, "rot": 0, "floors": 50},
        {"name": "V03_secondary_high", "cx": 325, "cy": 4418, "w": 32, "d": 42, "rot": 0, "floors": 38},
        {"name": "V03_central_shoulder", "cx": 260, "cy": 4495, "w": 36, "d": 42, "rot": 0, "floors": 26},
        {"name": "V03_mid_shoulder", "cx": 355, "cy": 4525, "w": 38, "d": 38, "rot": 0, "floors": 17},
        {"name": "V03_north_low_volume", "cx": 445, "cy": 4580, "w": 30, "d": 38, "rot": 0, "floors": 9},
        {"name": "V03_compact_base_west", "cx": 300, "cy": 4450, "w": 150, "d": 24, "rot": 0, "floors": 4},
        {"name": "V03_compact_base_north", "cx": 375, "cy": 4560, "w": 120, "d": 24, "rot": 0, "floors": 4},
        {"name": "V03_compact_base_east", "cx": 440, "cy": 4525, "w": 54, "d": 28, "rot": 0, "floors": 4}
      ]
    }
  ]
}
'''


def height_from_floors(floors):
    return 4.2 + (int(floors) - 1) * 3.6


def pt_xy(p):
    return [float(p.X), float(p.Y)]


def point_in_poly_xy(x, y, pts):
    inside = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i][0], pts[i][1]
        xj, yj = pts[j][0], pts[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi):
            inside = not inside
        j = i
    return inside


def get_boundary():
    best = None
    best_area = -1.0
    for oid in rs.ObjectsByLayer(BOUNDARY_LAYER) or []:
        pts = rs.CurvePoints(oid) or []
        poly = [pt_xy(p) for p in pts]
        if len(poly) > 1 and poly[0] == poly[-1]:
            poly = poly[:-1]
        area = 0.0
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]
            area += x1 * y2 - x2 * y1
        area = abs(area) * 0.5
        if area > best_area:
            best = poly
            best_area = area
    return best, best_area


def get_inso_breps():
    breps = []
    bbox = Rhino.Geometry.BoundingBox.Empty
    for oid in rs.ObjectsByLayer(INSO_LAYER) or []:
        obj = sc.doc.Objects.Find(oid)
        if not obj:
            continue
        geo = obj.Geometry
        bbox.Union(geo.GetBoundingBox(True))
        if isinstance(geo, Rhino.Geometry.Brep):
            breps.append(geo)
    return breps, bbox


def envelope_z_at(breps, x, y, zmin, zmax):
    tol = sc.doc.ModelAbsoluteTolerance
    line = Rhino.Geometry.LineCurve(
        Rhino.Geometry.Point3d(x, y, zmin),
        Rhino.Geometry.Point3d(x, y, zmax),
    )
    zs = []
    for brep in breps:
        try:
            ok, curves, points = Rhino.Geometry.Intersect.Intersection.CurveBrep(line, brep, tol)
            if ok and points:
                for p in points:
                    zs.append(float(p.Z))
        except Exception:
            pass
    if not zs:
        return None
    return max(zs)


def rect_points(part):
    cx = float(part["cx"])
    cy = float(part["cy"])
    w = float(part["w"])
    d = float(part["d"])
    rot = math.radians(float(part.get("rot", 0)))
    c = math.cos(rot)
    s = math.sin(rot)
    raw = [(-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)]
    pts = []
    for dx, dy in raw:
        pts.append([cx + dx * c - dy * s, cy + dx * s + dy * c])
    return pts


def sample_points(poly):
    pts = list(poly)
    for i in range(len(poly)):
        a = poly[i]
        b = poly[(i + 1) % len(poly)]
        pts.append([(a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0])
    cx = sum(p[0] for p in poly) / float(len(poly))
    cy = sum(p[1] for p in poly) / float(len(poly))
    pts.append([cx, cy])
    return pts


def main():
    params = json.loads(PARAMS_JSON)
    boundary, boundary_area = get_boundary()
    breps, bbox = get_inso_breps()
    zmin = bbox.Min.Z - 20.0
    zmax = bbox.Max.Z + 20.0
    out = {
        "boundary_area": round(boundary_area, 3),
        "target_gfa": params["target_gfa"],
        "variants": [],
    }
    for variant in params["variants"]:
        gfa = 0.0
        min_clearance = 999999.0
        errors = []
        for part in variant["parts"]:
            h = height_from_floors(part["floors"])
            area = float(part["w"]) * float(part["d"])
            gfa += area * int(part["floors"])
            poly = rect_points(part)
            for p in sample_points(poly):
                if not point_in_poly_xy(p[0], p[1], boundary):
                    errors.append(part["name"] + " outside_boundary")
                ez = envelope_z_at(breps, p[0], p[1], zmin, zmax)
                if ez is None:
                    errors.append(part["name"] + " no_inso_hit")
                    continue
                clearance = ez - h
                min_clearance = min(min_clearance, clearance)
                if clearance < 0.0:
                    errors.append(part["name"] + " above_inso %.2f" % clearance)
        out["variants"].append({
            "layer": variant["layer"],
            "strategy": variant["strategy"],
            "part_count": len(variant["parts"]),
            "gfa": round(gfa, 1),
            "gfa_ratio": round(gfa / params["target_gfa"], 3),
            "min_inso_clearance": round(min_clearance, 2),
            "ok": len(errors) == 0,
            "errors": sorted(list(set(errors)))[:20],
        })
    print(json.dumps(out, sort_keys=True))


main()
