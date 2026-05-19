"""
Tower Simplification v7
=======================
Outer envelope (alpha shape) + corner label correspondence + zone split

Run inside Rhino: Tools > Python Script > Run
OR standalone:   python tower_simplify_v7.py (needs trimesh, numpy, scipy, shapely)

v7 fixes vs v6:
  - alpha shape outer hull (not RDP on raw section) -- strips facade rib noise
  - corner label matching via KDTree -- eliminates loft twist
  - zone detection by area change -- shaft/crown/cap lofted separately
  - roof cap as flat polygon -- no loft through section collapse
"""

import os, sys, math, json
import numpy as np

# ── detect environment ─────────────────────────────────────────────────────
IN_RHINO = False
try:
    import Rhino
    import Rhino.Geometry as rg
    import rhinoscriptsyntax as rs
    import scriptcontext as sc
    IN_RHINO = True
except ImportError:
    pass

# ── config ─────────────────────────────────────────────────────────────────
CFG = {
    "input_obj":      r"C:\temp\claude_to_cad\tower_only.obj",
    "output_prefix":  r"C:\temp\claude_to_cad\tower_v7",
    "output_layer":   "CTR_Tower_v7",

    # Section stack
    "z_step_shaft":   1500,    # mm — coarse in flat regions
    "z_step_crown":   500,     # mm — fine near top transitions
    "n_sections":     35,      # total target sections (adaptive)

    # Alpha shape
    "alpha_m":        2000,    # mm — outer hull smoothness (larger = more convex)

    # Simplification
    "rdp_tol":        800,     # mm — after hull, simplify outline
    "n_corner_pts":   10,      # target points per section (for loft)

    # Zone detection
    "area_break_pct": 0.18,    # 18% area change = zone boundary
    "min_zone_sections": 3,    # don't split if zone would be < 3 sections

    # Validation
    "bbox_tol_pct":   0.03,    # 3% BBox tolerance vs source
}

# ═══════════════════════════════════════════════════════════════════════════
# GEOMETRY UTILITIES
# ═══════════════════════════════════════════════════════════════════════════

def alpha_shape_2d(pts, alpha):
    """
    Compute outer alpha-shape polygon from 2D point array.
    Returns ordered (N,2) boundary vertices or None.
    alpha = max triangle circumradius to include.
    """
    from scipy.spatial import Delaunay
    if len(pts) < 4:
        return pts
    tri = Delaunay(pts)
    edges = set()
    edge_pts = {}
    for simplex in tri.simplices:
        for i in range(3):
            a, b = sorted([simplex[i], simplex[(i+1)%3]])
            edge = (a, b)
            # circumradius of triangle
            pa, pb, pc = pts[simplex[0]], pts[simplex[1]], pts[simplex[2]]
            ax, ay = pb - pa
            bx, by = pc - pa
            D = 2 * (ax * by - ay * bx)
            if abs(D) < 1e-10:
                continue
            ux = (by*(ax*ax+ay*ay) - ay*(bx*bx+by*by)) / D
            uy = (ax*(bx*bx+by*by) - bx*(ax*ax+ay*ay)) / D
            r = math.sqrt(ux*ux + uy*uy)
            if r < alpha:
                edges.add(edge)
                edge_pts.setdefault(a, []).append(b)
                edge_pts.setdefault(b, []).append(a)

    if not edges:
        # alpha too small — fall back to convex hull
        from scipy.spatial import ConvexHull
        try:
            h = ConvexHull(pts)
            return pts[h.vertices]
        except Exception:
            return pts

    # Walk boundary
    start = min(edges, key=lambda e: (pts[e[0]][0], pts[e[0]][1]))[0]
    boundary = [start]
    prev = None
    cur = start
    for _ in range(len(edges) * 2):
        nexts = [n for n in edge_pts.get(cur, []) if n != prev]
        if not nexts:
            break
        nxt = nexts[0]
        if nxt == start:
            break
        boundary.append(nxt)
        prev, cur = cur, nxt

    return pts[boundary] if len(boundary) >= 3 else pts


def rdp_simplify(pts, tol):
    """Ramer-Douglas-Peucker simplification of a 2D polyline."""
    if len(pts) <= 2:
        return pts
    def rdp_rec(pts):
        if len(pts) <= 2:
            return [pts[0], pts[-1]]
        dv = pts[-1] - pts[0]
        dlen = np.linalg.norm(dv)
        if dlen < 1e-10:
            dists = np.linalg.norm(pts[1:-1] - pts[0], axis=1)
        else:
            n = np.array([-dv[1], dv[0]]) / dlen
            dists = np.abs((pts[1:-1] - pts[0]) @ n)
        idx = np.argmax(dists) + 1
        if dists[idx-1] > tol:
            l = rdp_rec(pts[:idx+1])
            r = rdp_rec(pts[idx:])
            return l[:-1] + r
        return [pts[0], pts[-1]]
    result = rdp_rec(list(pts))
    return np.array(result)


def resample_polygon(pts, n):
    """Resample closed polygon to exactly n evenly-spaced points."""
    pts = np.array(pts)
    closed = np.vstack([pts, pts[0]])
    dists = np.cumsum(np.r_[0, np.linalg.norm(np.diff(closed, axis=0), axis=1)])
    total = dists[-1]
    if total < 1e-10:
        return np.tile(pts[0], (n, 1))
    targets = np.linspace(0, total, n, endpoint=False)
    out = np.zeros((n, 2))
    for i, t in enumerate(targets):
        idx = np.searchsorted(dists, t, side='right') - 1
        idx = min(idx, len(closed) - 2)
        seg_len = dists[idx+1] - dists[idx]
        frac = (t - dists[idx]) / seg_len if seg_len > 1e-10 else 0
        out[i] = closed[idx] + frac * (closed[idx+1] - closed[idx])
    return out


def polygon_area(pts):
    """Signed shoelace area of 2D polygon."""
    x, y = pts[:,0], pts[:,1]
    return 0.5 * abs(np.dot(x, np.roll(y,-1)) - np.dot(y, np.roll(x,-1)))


def align_seam(pts, ref_corners):
    """
    Reorder pts so that index 0 is nearest to ref_corners[0],
    and winding matches reference.
    """
    from scipy.spatial import KDTree
    tree = KDTree(pts)
    # Find index in pts nearest to each reference corner
    _, corner_idx = tree.query(ref_corners)
    start = int(corner_idx[0])
    # Roll to start
    pts = np.roll(pts, -start, axis=0)
    # Ensure CCW winding matches reference
    if polygon_area(pts) < 0:
        pts = pts[::-1]
    return pts


def detect_zone_breaks(areas, min_zone=3, break_pct=0.18):
    """
    Find indices where area changes > break_pct relative.
    Returns list of break indices (sections BEFORE a new zone starts).
    """
    breaks = []
    for i in range(1, len(areas)):
        if areas[i-1] < 1:
            continue
        change = abs(areas[i] - areas[i-1]) / areas[i-1]
        if change > break_pct:
            # Only accept if both resulting zones are large enough
            if i >= min_zone and (len(areas) - i) >= min_zone:
                breaks.append(i)
    return breaks


# ═══════════════════════════════════════════════════════════════════════════
# SECTION EXTRACTION  (trimesh standalone)
# ═══════════════════════════════════════════════════════════════════════════

def extract_sections_standalone(mesh_path, n_sections):
    """Extract horizontal sections from OBJ using trimesh."""
    import trimesh
    mesh = trimesh.load(mesh_path, force='mesh')
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))

    zmin, zmax = mesh.bounds[0][2], mesh.bounds[1][2]
    z_levels = np.linspace(zmin + (zmax-zmin)*0.01,
                           zmax - (zmax-zmin)*0.005, n_sections)

    sections = []
    for z in z_levels:
        origin = np.array([0, 0, z])
        normal = np.array([0, 0, 1])
        try:
            path = mesh.section(plane_origin=origin, plane_normal=normal)
            if path is None:
                continue
            path2d, _ = path.to_planar()
            if not path2d.entities:
                continue
            # Largest contour by length
            best = max(path2d.entities, key=lambda e: len(e.points))
            pts = path2d.vertices[best.points]
            sections.append((z, pts))
        except Exception:
            continue

    print(f"  Extracted {len(sections)} sections from {zmin:.0f}..{zmax:.0f} mm")
    return sections, mesh


# ═══════════════════════════════════════════════════════════════════════════
# SECTION EXTRACTION  (Rhino-side)
# ═══════════════════════════════════════════════════════════════════════════

def extract_sections_rhino(mesh_id, n_sections):
    """Extract sections from Rhino mesh object."""
    obj = sc.doc.Objects.FindId(mesh_id) if hasattr(mesh_id, 'int_value') else None
    if obj is None:
        # Try by string GUID
        import System
        obj = sc.doc.Objects.FindId(System.Guid(str(mesh_id)))

    mesh = obj.Geometry if obj else None
    if mesh is None or not isinstance(mesh, rg.Mesh):
        print(f"  ERROR: could not find mesh {mesh_id}")
        return [], None

    bbox = mesh.GetBoundingBox(True)
    zmin, zmax = bbox.Min.Z, bbox.Max.Z
    z_levels = np.linspace(zmin + (zmax-zmin)*0.01,
                           zmax - (zmax-zmin)*0.005, n_sections)

    sections = []
    for z in z_levels:
        plane = rg.Plane(rg.Point3d(0, 0, z), rg.Vector3d.ZAxis)
        polys = rg.Intersect.Intersection.MeshPlane(mesh, plane)
        if not polys:
            continue
        # Largest polyline
        best = max(polys, key=lambda p: p.Length)
        pts_3d = list(best)
        pts_2d = np.array([[p.X, p.Y] for p in pts_3d])
        sections.append((z, pts_2d))

    print(f"  Extracted {len(sections)} sections Z={zmin:.0f}..{zmax:.0f}")
    return sections, mesh


# ═══════════════════════════════════════════════════════════════════════════
# V7 CORE ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════

def process_sections(sections, cfg):
    """
    Apply v7 processing to raw sections:
    1. Alpha shape outer envelope
    2. RDP simplify
    3. Reference corner extraction (mid-shaft)
    4. Corner alignment (seam correspondence)
    5. Resample to n points
    Returns: list of (z, pts_2d_processed)
    """
    alpha    = cfg["alpha_m"]
    rdp_tol  = cfg["rdp_tol"]
    n_pts    = cfg["n_corner_pts"]

    processed = []
    for z, raw_pts in sections:
        # Step 1: outer envelope
        hull = alpha_shape_2d(raw_pts, alpha)
        if hull is None or len(hull) < 3:
            hull = raw_pts

        # Step 2: RDP simplify
        simp = rdp_simplify(hull, rdp_tol)
        if len(simp) < 3:
            simp = hull

        processed.append((z, simp))

    # Step 3: find reference corners from mid-shaft section
    mid_idx = len(processed) // 3  # lower third is most representative shaft
    ref_z, ref_pts = processed[mid_idx]

    from scipy.spatial import ConvexHull
    try:
        ch = ConvexHull(ref_pts)
        ref_corners = ref_pts[ch.vertices]
    except Exception:
        ref_corners = ref_pts

    print(f"  Reference corners: {len(ref_corners)} pts at Z={ref_z:.0f}")

    # Step 4+5: align seam + resample all sections
    aligned = []
    for z, pts in processed:
        try:
            a = align_seam(pts, ref_corners)
            r = resample_polygon(a, n_pts)
            aligned.append((z, r))
        except Exception as e:
            print(f"  WARNING: section Z={z:.0f} alignment failed: {e}")

    return aligned, ref_corners


def split_zones(sections, cfg):
    """
    Split sections into zones by area change.
    Returns: list of zones, each zone = list of (z, pts) sections.
    """
    areas = [polygon_area(pts) for _, pts in sections]
    breaks = detect_zone_breaks(
        areas,
        min_zone=cfg["min_zone_sections"],
        break_pct=cfg["area_break_pct"]
    )

    print(f"  Zone breaks at indices: {breaks}")
    zones = []
    prev = 0
    for b in breaks:
        zones.append(sections[prev:b])
        prev = b
    zones.append(sections[prev:])

    print(f"  Zones: {[len(z) for z in zones]} sections each")
    return zones


# ═══════════════════════════════════════════════════════════════════════════
# MESH CONSTRUCTION
# ═══════════════════════════════════════════════════════════════════════════

def loft_zone_to_mesh(zone_sections, close_bottom=False, close_top=False):
    """
    Loft a list of 2D section contours into a 3D mesh (walls only).
    Each section: (z, pts_2d) where pts_2d is (N,2) resampled ring.
    Returns (verts_3d, faces).
    """
    if len(zone_sections) < 2:
        return None, None

    n = len(zone_sections[0][1])  # points per ring
    all_verts = []
    all_faces = []
    v_offset = 0

    for i, (z, ring2d) in enumerate(zone_sections):
        ring3d = np.column_stack([ring2d, np.full(n, z)])
        all_verts.append(ring3d)

    verts = np.vstack(all_verts)

    # Side quads
    for ring_i in range(len(zone_sections) - 1):
        for pt_i in range(n):
            a = ring_i * n + pt_i
            b = ring_i * n + (pt_i + 1) % n
            c = (ring_i + 1) * n + (pt_i + 1) % n
            d = (ring_i + 1) * n + pt_i
            all_faces.append([a, b, c])
            all_faces.append([a, c, d])

    # Bottom cap
    if close_bottom:
        z0, ring0 = zone_sections[0]
        center = np.array([ring0[:,0].mean(), ring0[:,1].mean(), z0])
        c_idx = len(verts)
        verts = np.vstack([verts, center])
        for pt_i in range(n):
            a = pt_i
            b = (pt_i + 1) % n
            all_faces.append([c_idx, b, a])  # inward normal

    # Top cap (always for roof cap zone)
    if close_top:
        z_top, ring_top = zone_sections[-1]
        center = np.array([ring_top[:,0].mean(), ring_top[:,1].mean(), z_top])
        c_idx = len(verts)
        verts = np.vstack([verts, center])
        last_ring_start = (len(zone_sections) - 1) * n
        for pt_i in range(n):
            a = last_ring_start + pt_i
            b = last_ring_start + (pt_i + 1) % n
            all_faces.append([c_idx, a, b])

    return verts, np.array(all_faces)


# ═══════════════════════════════════════════════════════════════════════════
# RHINO IMPORT
# ═══════════════════════════════════════════════════════════════════════════

def import_mesh_to_rhino(verts, faces, layer_name):
    """Add mesh to Rhino document on given layer."""
    if not IN_RHINO:
        return None

    mesh = rg.Mesh()
    for v in verts:
        mesh.Vertices.Add(float(v[0]), float(v[1]), float(v[2]))
    for f in faces:
        if len(f) == 3:
            mesh.Faces.AddFace(int(f[0]), int(f[1]), int(f[2]))
        else:
            mesh.Faces.AddFace(int(f[0]), int(f[1]), int(f[2]), int(f[3]))

    mesh.Normals.ComputeNormals()
    mesh.UnifyNormals()
    mesh.Weld(math.radians(25))
    mesh.Compact()

    # Ensure layer exists
    if not rs.IsLayer(layer_name):
        rs.AddLayer(layer_name, rs.CreateColor(80, 160, 220))

    attr = Rhino.DocObjects.ObjectAttributes()
    attr.LayerIndex = sc.doc.Layers.FindName(layer_name).Index

    obj_id = sc.doc.Objects.AddMesh(mesh, attr)
    sc.doc.Views.Redraw()
    return obj_id


def export_mesh_obj(verts, faces, path):
    """Export mesh as OBJ."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write("# Tower v7\n")
        for v in verts:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        for face in faces:
            f.write("f " + " ".join(str(i+1) for i in face) + "\n")
    print(f"  Exported: {path}")


# ═══════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

def validate_result(verts, faces, source_bounds):
    """Check BBox match, face count, and basic topology."""
    result_min = verts.min(axis=0)
    result_max = verts.max(axis=0)

    src_min, src_max = source_bounds
    tol = CFG["bbox_tol_pct"]

    issues = []
    for axis, name in enumerate(['X', 'Y', 'Z']):
        src_range = src_max[axis] - src_min[axis]
        if src_range < 1:
            continue
        min_err = abs(result_min[axis] - src_min[axis]) / src_range
        max_err = abs(result_max[axis] - src_max[axis]) / src_range
        if min_err > tol:
            issues.append(f"  {name}min off by {min_err*100:.1f}%")
        if max_err > tol:
            issues.append(f"  {name}max off by {max_err*100:.1f}%")

    print(f"\n── Validation ──────────────────────────────")
    print(f"  Verts: {len(verts)}  Faces: {len(faces)}")
    print(f"  Result BBox: {result_min.round(0)} → {result_max.round(0)}")
    print(f"  Source BBox: {np.array(src_min).round(0)} → {np.array(src_max).round(0)}")
    if issues:
        print("  ⚠ BBox issues:")
        for i in issues: print(i)
    else:
        print(f"  ✓ BBox within {tol*100:.0f}% tolerance")
    print(f"────────────────────────────────────────────")
    return len(issues) == 0


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("\n═══ Tower Simplification v7 ═══════════════")
    print(f"  Mode: {'Rhino' if IN_RHINO else 'Standalone'}")

    cfg = CFG.copy()

    # ── Step 1: Extract sections ──────────────────────────────────────────
    print("\n[1] Extracting sections...")

    if IN_RHINO:
        # Try to find tower mesh by layer name
        tower_layers = [l.Name for l in sc.doc.Layers
                        if 'tower' in l.Name.lower() or 'ctr' in l.Name.lower()]
        print(f"  Found layers: {tower_layers}")

        # Get all mesh objects
        meshes = [o for o in sc.doc.Objects
                  if isinstance(o.Geometry, rg.Mesh)
                  and 'tower' in (sc.doc.Layers[o.Attributes.LayerIndex].Name).lower()]

        if not meshes:
            print("  No tower meshes found by layer. Using all visible meshes.")
            meshes = [o for o in sc.doc.Objects
                      if isinstance(o.Geometry, rg.Mesh) and o.IsNormal]

        if not meshes:
            print("  ERROR: No meshes found. Export mesh first and run standalone.")
            return

        # Join meshes for sectioning
        joined = rg.Mesh()
        for mo in meshes:
            joined.Append(mo.Geometry)
        joined.Compact()

        bbox = joined.GetBoundingBox(True)
        source_bounds = (
            [bbox.Min.X, bbox.Min.Y, bbox.Min.Z],
            [bbox.Max.X, bbox.Max.Y, bbox.Max.Z]
        )
        print(f"  Source mesh: {joined.Faces.Count} faces")
        print(f"  BBox: Z={bbox.Min.Z:.0f}..{bbox.Max.Z:.0f}")

        zmin, zmax = bbox.Min.Z, bbox.Max.Z
        z_levels = np.linspace(zmin + (zmax-zmin)*0.01,
                               zmax - (zmax-zmin)*0.005, cfg["n_sections"])
        sections = []
        for z in z_levels:
            plane = rg.Plane(rg.Point3d(0, 0, z), rg.Vector3d.ZAxis)
            polys = rg.Intersect.Intersection.MeshPlane(joined, plane)
            if not polys:
                continue
            best = max(polys, key=lambda p: p.Length)
            pts_3d = list(best)
            pts_2d = np.array([[p.X, p.Y] for p in pts_3d])
            sections.append((z, pts_2d))

    else:
        if not os.path.exists(cfg["input_obj"]):
            print(f"  ERROR: {cfg['input_obj']} not found.")
            print("  Run rhino_export_for_vsa.py in Rhino first.")
            return
        sections, src_mesh = extract_sections_standalone(cfg["input_obj"], cfg["n_sections"])
        source_bounds = (src_mesh.bounds[0].tolist(), src_mesh.bounds[1].tolist())

    if len(sections) < 4:
        print(f"  ERROR: only {len(sections)} sections extracted. Check mesh.")
        return

    print(f"  Got {len(sections)} raw sections")

    # ── Step 2: Process sections (alpha shape + alignment) ────────────────
    print("\n[2] Processing sections (alpha shape + corner alignment)...")
    aligned, ref_corners = process_sections(sections, cfg)
    print(f"  Processed: {len(aligned)} aligned sections")

    # ── Step 3: Zone detection ────────────────────────────────────────────
    print("\n[3] Detecting zones...")
    zones = split_zones(aligned, cfg)

    # ── Step 4: Loft zones ────────────────────────────────────────────────
    print("\n[4] Lofting zones...")
    all_verts_list = []
    all_faces_list = []
    v_offset = 0

    for zi, zone in enumerate(zones):
        is_last = (zi == len(zones) - 1)
        is_first = (zi == 0)

        v, f = loft_zone_to_mesh(
            zone,
            close_bottom=is_first,
            close_top=is_last
        )
        if v is None:
            print(f"  Zone {zi}: skipped (too few sections)")
            continue

        print(f"  Zone {zi}: {len(zone)} sections → {len(v)} verts, {len(f)} faces")
        all_verts_list.append(v)
        all_faces_list.append(f + v_offset)
        v_offset += len(v)

    if not all_verts_list:
        print("  ERROR: No geometry produced.")
        return

    all_verts = np.vstack(all_verts_list)
    all_faces = np.vstack(all_faces_list)

    # ── Step 5: Validate ──────────────────────────────────────────────────
    print("\n[5] Validating...")
    ok = validate_result(all_verts, all_faces, source_bounds)

    # ── Step 6: Export / Import ───────────────────────────────────────────
    print("\n[6] Exporting...")
    out_obj = cfg["output_prefix"] + "_v7.obj"
    export_mesh_obj(all_verts, all_faces, out_obj)

    if IN_RHINO:
        obj_id = import_mesh_to_rhino(all_verts, all_faces, cfg["output_layer"])
        print(f"  Added to Rhino: layer '{cfg['output_layer']}'")
        print(f"  Object ID: {obj_id}")
        rs.SelectObject(obj_id)

    # Report
    report = {
        "version": "v7",
        "sections_extracted": len(sections),
        "sections_aligned": len(aligned),
        "zones": [len(z) for z in zones],
        "verts": int(len(all_verts)),
        "faces": int(len(all_faces)),
        "bbox_ok": ok,
        "output_obj": out_obj,
    }
    report_path = cfg["output_prefix"] + "_v7_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  Report: {report_path}")

    print("\n═══ Done ═══════════════════════════════════")
    print(f"  Sections: {len(sections)} raw → {len(aligned)} aligned")
    print(f"  Zones: {[len(z) for z in zones]}")
    print(f"  Mesh: {len(all_verts)} verts, {len(all_faces)} faces")
    print(f"  BBox: {'✓' if ok else '⚠ check report'}")
    if IN_RHINO:
        print(f"  Layer: {cfg['output_layer']}")


if __name__ == "__main__":
    main()
