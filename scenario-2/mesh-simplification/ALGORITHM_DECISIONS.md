# Scenario 2: Algorithm Decisions

Key decisions made during mesh simplification R&D. Each decision records what was chosen, why, and what was ruled out.

---

## D-01: Section method — true intersections, not vertex slabs

**Decision:** Use `trimesh.section()` (true mesh-plane intersection) for all section extraction.

**Ruled out:** vertex slabs (collect vertices within Z tolerance band)

**Why:**
- Vertex slabs are not architectural sections — they include facade rib vertices, roof fragments, partial edges
- At upper levels, vertex distribution is not a closed architectural section
- True `trimesh.section()` gives a closed or near-closed contour polyline representing actual building outline

**Rule:**
> Never use vertex sampling to approximate a section. Always intersect the mesh with a plane.

---

## D-02: Section simplification — alpha shape outer envelope, not RDP

**Decision:** Compute outer alpha shape of section vertices as the simplification primitive.

**Ruled out:** Ramer-Douglas-Peucker (RDP) on the raw contour polyline

**Why:**
- RDP simplifies the contour path — it may keep or discard facade rib points inconsistently between Z levels
- Alpha shape computes the outer hull of the point set, ignoring internal structure
- Facade ribs are INSIDE the mass envelope — alpha shape boundary excludes them
- Alpha parameter (1.5–3.0 m) controls concavity tolerance: larger = more convex (smoother), smaller = more detailed

**Implementation:**
```python
from shapely.ops import unary_union
from shapely.geometry import MultiPoint
# alpha_shape via Delaunay triangulation edge length filtering
```

---

## D-03: Correspondence method — corner label matching via nearest-neighbour

**Decision:** Extract convex hull corners of reference section → nearest-neighbour match on all other sections → reorder to align front-left-corner at all Z levels.

**Ruled out:** arclength-based resampling (uniform points along perimeter)

**Why:**
- Arclength resampling places point N at a fixed fraction of total perimeter
- Different sections have different perimeter features at that fraction → mismatched connections
- Corner matching is stable: major plan corners are present at all shaft levels regardless of local variations

**Algorithm:**
```python
# Reference section corners (mid-shaft convex hull vertices)
ref_corners = convex_hull_vertices(reference_section)
# For each target section, find nearest points to reference corners
tree = KDTree(target_section_points)
corner_idx = tree.query(ref_corners)[1]
# Reorder target section starting at corner_idx[0], same winding direction
```

---

## D-04: Zone split — detect by area change threshold

**Decision:** Detect zone boundaries by relative cross-sectional area change > 15% between adjacent Z levels.

**Ruled out:** single loft through all Z levels

**Why:**
- Single loft through dramatic area change creates diagonal faces and chopped geometry
- Area drop 44.3 m → 18.7 m in one step (confirmed in v3) creates the "wedged roof" artifact
- Zone split allows each zone to have its own template and correspondence setup

**Zones for this tower:**
```
lower_shaft    → base to first taper
mid_shaft      → main bulk
upper_shaft    → tapering zone
crown_shoulder → shoulder/setback geometry  
roof_cap       → flat or domed cap (planar polygon, not loft)
```

**Threshold formula:**
```python
area_change = abs(area[z+1] - area[z]) / area[z]
if area_change > 0.15:
    # zone boundary
```

---

## D-05: Loft geometry — avoid Boolean union

**Decision:** Use appended Brep shells (multiple closed meshes) as output. Do not perform Boolean union.

**Ruled out:** `BooleanUnion` to merge zone lofts into single solid

**Why (confirmed in Clear Model 4 postmortem):**
- Boolean union silently removes large masses at complex intersections
- Produces unpredictable results on near-tangent zone boundaries
- Appended shells are visually correct and geometrically valid
- Boolean union can be applied manually if needed — it is reversible; data loss is not

---

## D-06: Normal display — unweld sharp edges after export

**Decision:** After generating mesh, apply `Unweld` / `UnweldEdge` with `ModifyNormals=Yes` on edges with dihedral angle > 25°.

**Why:**
- Welded mesh with averaged normals looks smooth/soapy in rendered display even when topology is planar
- Unwelding creates coincident vertices with face-specific normals → hard edge appearance in Rhino
- This is a display fix only — topology unchanged

**Rhino command:** `_Unweld 25 ModifyNormals=Yes`

---

## D-07: Success criteria — architectural, not topological

**Decision:** Accept a reconstruction only when ALL of:
1. `isClosed=True` (topological)
2. BBox matches source within 2% tolerance (metric)
3. No adjacent sections collapse >15% without explicit zone split (topological)
4. Major plan corners visible and consistent across Z levels (architectural)
5. No diagonal cross-connections or twisted faces visible in Perspective view (visual)

**Ruled out:** `isClosed=True` alone as acceptance gate

**Why:**
- A rectangular box always passes `isClosed=True`
- The test model demonstrates that closed ≠ correct
- Architectural validity requires human visual review of Perspective + Top views

---

## D-08: Facade ribs — filter before section analysis

**Decision:** Before computing section correspondence, filter facade rib geometry from sections.

**Method:**
- Detect rib vertices as points that are not on the mass outer hull (alpha shape boundary)
- OR: sample only vertices from structural mesh layers, not detail layers
- OR: use source mesh bounding hull filtered by ridge/valley line proximity

**Why:**
- Facade ribs dominate vertex counts in the source model
- They bias PCA, normal histograms, and contour simplification
- The mass envelope EXISTS and is readable — it is just obscured by rib noise

**Status:** Partial fix via alpha shape (D-02). Full rib filtering not yet implemented.
