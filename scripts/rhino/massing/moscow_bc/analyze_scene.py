import json
import math

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc


LAYERS = [
    "plot boundary",
    "ИНСО ИД",
    "project geometry",
    "context geometry",
]


def pt3(p):
    return [round(float(p.X), 3), round(float(p.Y), 3), round(float(p.Z), 3)]


def bbox_payload(bbox):
    return {
        "min": pt3(bbox.Min),
        "max": pt3(bbox.Max),
        "size": [
            round(float(bbox.Max.X - bbox.Min.X), 3),
            round(float(bbox.Max.Y - bbox.Min.Y), 3),
            round(float(bbox.Max.Z - bbox.Min.Z), 3),
        ],
    }


def curve_points(curve, oid=None):
    if oid:
        raw = rs.CurvePoints(oid)
        if raw:
            return [pt3(p) for p in raw]
    pts = []
    count = 80
    for i in range(count + 1):
        t = curve.Domain.ParameterAt(float(i) / float(count))
        pts.append(pt3(curve.PointAt(t)))
    return pts


def polygon_area_xy(points):
    if len(points) < 3:
        return 0.0
    area = 0.0
    for i in range(len(points)):
        x1, y1 = points[i][0], points[i][1]
        x2, y2 = points[(i + 1) % len(points)][0], points[(i + 1) % len(points)][1]
        area += x1 * y2 - x2 * y1
    return abs(area) * 0.5


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


def floor_count_from_height(h):
    if h < 4.2:
        return 0
    return int(round((h - 4.2) / 3.6 + 1.0))


def height_from_floors(floors):
    if floors <= 0:
        return 0.0
    return 4.2 + (floors - 1) * 3.6


def mesh_from_geometry(geo):
    if isinstance(geo, Rhino.Geometry.Mesh):
        return geo.DuplicateMesh()
    if isinstance(geo, Rhino.Geometry.Brep):
        meshes = Rhino.Geometry.Mesh.CreateFromBrep(geo, Rhino.Geometry.MeshingParameters.Coarse)
        if not meshes:
            return None
        out = Rhino.Geometry.Mesh()
        for m in meshes:
            out.Append(m)
        out.Normals.ComputeNormals()
        out.Compact()
        return out
    return None


def mesh_vertical_hits(mesh, x, y, zmin, zmax):
    line = Rhino.Geometry.Line(Rhino.Geometry.Point3d(x, y, zmin), Rhino.Geometry.Point3d(x, y, zmax))
    hits = Rhino.Geometry.Intersect.Intersection.MeshLine(mesh, line)
    zs = []
    if hits:
        for t in hits:
            if 0.0 <= t <= 1.0:
                zs.append(zmin + (zmax - zmin) * t)
    return zs


def brep_vertical_hits(brep, x, y, zmin, zmax):
    tol = sc.doc.ModelAbsoluteTolerance
    line = Rhino.Geometry.LineCurve(
        Rhino.Geometry.Point3d(x, y, zmin),
        Rhino.Geometry.Point3d(x, y, zmax),
    )
    zs = []
    try:
        ok, curves, points = Rhino.Geometry.Intersect.Intersection.CurveBrep(line, brep, tol)
        if ok and points:
            for p in points:
                zs.append(float(p.Z))
    except Exception:
        pass
    return zs


def object_record(oid):
    obj = sc.doc.Objects.Find(oid)
    geo = obj.Geometry
    bbox = geo.GetBoundingBox(True)
    rec = {
        "id": str(oid),
        "name": rs.ObjectName(oid) or "",
        "type": str(rs.ObjectType(oid)),
        "bbox": bbox_payload(bbox),
    }
    if isinstance(geo, Rhino.Geometry.Curve):
        rec["is_closed"] = bool(geo.IsClosed)
        rec["points"] = curve_points(geo, oid)
        rec["area_xy"] = round(polygon_area_xy(rec["points"]), 3)
    if isinstance(geo, Rhino.Geometry.Brep):
        rec["is_solid"] = bool(geo.IsSolid)
        vmp = Rhino.Geometry.VolumeMassProperties.Compute(geo)
        if vmp:
            rec["volume"] = round(float(vmp.Volume), 3)
    if isinstance(geo, Rhino.Geometry.Mesh):
        rec["mesh_vertices"] = int(geo.Vertices.Count)
        rec["mesh_faces"] = int(geo.Faces.Count)
        rec["is_closed"] = bool(geo.IsClosed)
    return rec


def layer_records(layer):
    objs = rs.ObjectsByLayer(layer) or []
    return [object_record(oid) for oid in objs]


def project_metrics(records):
    solids = []
    total_gfa = 0.0
    total_footprint = 0.0
    max_h = 0.0
    for rec in records:
        size = rec["bbox"]["size"]
        h = max(0.0, float(size[2]))
        if h < 1.0:
            continue
        dx = max(0.0, float(size[0]))
        dy = max(0.0, float(size[1]))
        footprint = None
        if rec.get("volume") and h > 0.0:
            footprint = float(rec["volume"]) / h
        else:
            footprint = dx * dy
        floors = max(1, floor_count_from_height(h))
        gfa = footprint * floors
        total_gfa += gfa
        total_footprint += footprint
        max_h = max(max_h, h)
        solids.append({
            "name": rec.get("name", ""),
            "height": round(h, 3),
            "module_floors_nearest": floors,
            "module_height_nearest": round(height_from_floors(floors), 3),
            "footprint": round(footprint, 3),
            "gfa": round(gfa, 3),
            "bbox": rec["bbox"],
        })
    return {
        "solid_like_count": len(solids),
        "footprint_sum": round(total_footprint, 3),
        "gfa_sum": round(total_gfa, 3),
        "max_height": round(max_h, 3),
        "max_floors_nearest": floor_count_from_height(max_h),
        "parts": solids,
    }


def envelope_samples(boundary_pts, inso_layer):
    objs = rs.ObjectsByLayer(inso_layer) or []
    meshes = []
    breps = []
    bbox = Rhino.Geometry.BoundingBox.Empty
    for oid in objs:
        obj = sc.doc.Objects.Find(oid)
        if not obj:
            continue
        geo = obj.Geometry
        bbox.Union(geo.GetBoundingBox(True))
        if isinstance(geo, Rhino.Geometry.Brep):
            breps.append(geo)
        mesh = mesh_from_geometry(geo)
        if mesh:
            meshes.append(mesh)
    if not boundary_pts or not meshes:
        return {"samples": [], "bbox": bbox_payload(bbox) if bbox.IsValid else None}

    xs = [p[0] for p in boundary_pts]
    ys = [p[1] for p in boundary_pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    zmin = (bbox.Min.Z if bbox.IsValid else -10.0) - 20.0
    zmax = (bbox.Max.Z if bbox.IsValid else 300.0) + 20.0
    samples = []
    for ix in range(6):
        for iy in range(6):
            x = minx + (maxx - minx) * (ix + 0.5) / 6.0
            y = miny + (maxy - miny) * (iy + 0.5) / 6.0
            if not point_in_poly_xy(x, y, boundary_pts):
                continue
            zs = []
            for brep in breps:
                zs.extend(brep_vertical_hits(brep, x, y, zmin, zmax))
            for mesh in meshes:
                zs.extend(mesh_vertical_hits(mesh, x, y, zmin, zmax))
            if zs:
                samples.append({"x": round(x, 3), "y": round(y, 3), "z_max": round(max(zs), 3), "z_min": round(min(zs), 3)})
    return {"samples": samples, "bbox": bbox_payload(bbox) if bbox.IsValid else None}


def main():
    payload = {
        "units": rs.UnitSystemName(),
        "layer_counts": {},
    }
    for layer in LAYERS:
        payload["layer_counts"][layer] = len(rs.ObjectsByLayer(layer) or [])

    boundary_records = layer_records("plot boundary")
    boundary = max(boundary_records, key=lambda r: r.get("area_xy", 0.0)) if boundary_records else None
    boundary_pts = boundary.get("points", [])[:-1] if boundary and boundary.get("points") else []
    payload["boundary"] = {
        "area": round(polygon_area_xy(boundary_pts), 3),
        "points": boundary_pts,
        "bbox": boundary["bbox"] if boundary else None,
    }
    payload["project_metrics"] = project_metrics(layer_records("project geometry"))
    if payload["boundary"]["area"] > 0:
        payload["project_metrics"]["far_approx"] = round(
            payload["project_metrics"]["gfa_sum"] / payload["boundary"]["area"], 3
        )
    payload["inso"] = envelope_samples(boundary_pts, "ИНСО ИД")
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


main()
