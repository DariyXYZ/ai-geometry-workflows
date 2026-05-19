# Scenario 2: Mesh Simplification — Approach Log

**Building:** high-rise tower with ribbed panel facade + oval low-rise + curved podium
**Source:** high-poly Rhino mesh / polysurface (22.3dm)
**Goal:** clean massing model — sharp edges, flat surfaces, correct form, watertight

---

## Summary Table

| Approach | Status | Key Failure | Key Learning |
|---|---|---|---|
| ShrinkWrap / Marching Cubes | ❌ | Soapy topology, no sharp edges | Wrong tool class for architecture |
| v1–v2: Vertex slabs + BBox | ❌ | Facade ribs bias PCA/normal histograms | Vertex density ≠ mass envelope |
| v3: World XY BBox envelopes | ❌ | Closed but architecturally wrong box | BBox destroys chamfers, angles, facade logic |
| v5: True mesh-plane sections + RDP | ⚠️ | Crooked/twisted — per-section RDP breaks correspondence | True sections necessary but not sufficient |
| v6: Template contour + scale per Z | ⚠️ | Height fixed, twist reduced but present | Correspondence partially fixed via template |
| VSA (planar patch segmentation) | 🔬 | No Rhino plugin; CGAL required | Best for planar parts; script written |
| Feature line extraction | 🔬 | Sensitive to mesh noise; needs MeshLab | Correct primitive for ribbed facades |
| **v7: Outer envelope + corner labels + zone split** | 📋 | — | Planned next iteration |

---

## Detailed Approach History

### Baseline: ShrinkWrap / Marching Cubes

**Method:** Rhino ShrinkWrap or Cocoon (marching cubes) to merge geometry into one mesh.

**Result:** ❌ FAILED

**Failures:**
- "Soapy" topology — all edges are rounded, no hard architectural corners
- Grid quality is poor — irregular triangles, no quad structure
- Output cannot be re-meshed to recover sharp edges
- Slow and unstable on complex models

**Learning:** Voxel/marching cubes is a wrong tool class for architecture. Buildings are not organic forms. They are collections of flat faces with sharp edges — voxel methods do not model this.

---

### v1–v2: Vertex Slabs + PCA/Normal Histograms

**Method:** For each Z level, collect vertices within a tolerance band → compute envelope via PCA or dominant normal histogram.

**Result:** ❌ FAILED

**Failures:**
- The source tower has dense repeated rib/panel geometry
- Vertex and face density is NOT uniform across the mass envelope
- PCA is dominated by facade rib distribution, not actual massing planes
- Produces bloated envelopes biased toward rib direction

**Learning:**
> Vertex density ≠ mass envelope. Facade ribs are surface detail inside the envelope, not the envelope itself. Any method that samples from all vertices will be biased by them.

---

### v3: World XY BBox Envelopes per Section

**Method:** For each Z level, compute min/max XY bounding box from section vertices → extrude rectangular envelope.

**Result:** ❌ FAILED (technically closed, architecturally wrong)

**Evidence:**
```
Mesh: 34 vertices, 64 faces, isClosed=True
Visual: crude box with chopped/wedged top
```

**Failures:**
- BBox destroys chamfered corners, angled sides, facade plane logic
- Independent per-section envelopes have no side/corner correspondence
- Top section collapsed from 44.3 m → 18.7 m width without zone split → creates diagonal chopped roof
- `isClosed=True` ≠ architecturally correct

**Learning:**
> Closed mesh is a necessary condition, not a success criterion. A box is always closed but architecturally useless.

---

### v5: True Mesh-Plane Intersections + RDP Simplification

**Method:** `trimesh.section()` with horizontal planes → get true contour polylines → simplify with Ramer-Douglas-Peucker → resample by arclength → loft.

**Result:** ⚠️ PARTIAL — better than BBox, but still crooked/twisted

**What worked:**
- True sections are not random vertex clusters — they represent real building outline
- Form is no longer a pure box — faceted plan outline visible
- Correct Z range (mostly)

**What failed:**
- Each contour simplified independently via RDP
- RDP keeps different local details on different levels (facade ribs, protrusions)
- Arclength resampling redistributes vertices around different perimeter features at each Z
- Lofting connects mismatched points → diagonal/creased surfaces → twist

**Root cause:**
> True contours are necessary but not sufficient. The missing step is **architectural correspondence** — point 0 on level A must be the same architectural corner as point 0 on level B.

---

### v6: Template Contour + Scale per Z

**Method:** Choose one representative mid-shaft contour → simplify once → use as fixed template for all shaft levels → scale/offset per Z using source width/depth/center metrics.

**Result:** ⚠️ PARTIAL — height fixed, BBox correct, twist reduced

**What changed vs v5:**
- Full source height restored
- XY BBox matches source
- Fewer per-section RDP artifacts

**What still fails:**
- Template scaling doesn't eliminate facade rib geometry that leaked into the template contour
- Crown/top is a placeholder — reuses last shaft footprint
- Twist reduced but not eliminated

**Evidence:**
```
Mesh: 226 vertices, 448 faces, isClosed=True
Bbox min: [-2962.53, 183200.61, 25689.6]
Bbox max: [-2918.20, 183262.77, 25871.3]
```

**Learning:**
> Template correspondence is the right direction. But template must be derived from OUTER ENVELOPE (alpha shape), not from raw RDP-simplified section contour that still contains rib noise.

---

### VSA — Variational Shape Approximation

**Method:** Segment mesh faces into planar patches via region growing (minimize distortion = 1 − dot(face_normal, proxy_normal)²). Each cluster → one proxy plane → cluster boundaries = sharp feature edges.

**Status:** 🔬 IN RESEARCH — script implemented, not yet tested on this building

**Script:** `C:\VS Code\tools\cad-mesh-tools\vsa_simplify.py`

**Expected output:**
- `_segmented.obj` — mesh colored by cluster
- `_edges.obj` — sharp feature edges
- `_proxies.csv` — normal + centroid per planar region
- `_simplified.obj` — reconstructed simplified mesh

**Strong points for architecture:**
- Buildings ARE collections of flat faces → VSA naturally finds them
- Works with any mesh topology (no UV required)
- Robust to facade rib repetition if proxy count is tuned correctly

**Failure modes:**
- Curved surfaces (oval building) need many proxies
- No Rhino plugin — requires Python pipeline
- Reconstruction (convex hull per patch) loses concave details

**Recommended proxy counts for this model:**
- Tower shaft: 20–30 proxies (4–6 main faces × taper zones)
- Oval low-rise: 30–40 proxies
- Full scene: 80–100 proxies

---

### Feature Line Extraction (Ridge/Valley + Sharp Edges)

**Method:** Extract lines where surface curvature is extremal (ridge/valley lines) or where dihedral angle > threshold (sharp edges). These lines ARE the form — use as rails for NetworkSrf/Sweep2, not sections.

**Status:** 🔬 IN RESEARCH

**Why correct for ribbed facade:**
- Each facade rib IS a ridge/valley line pair
- Extracting them directly gives the exact geometric feature, not an approximation
- No loft interpolation error between mismatched sections

**Tools:**
- MeshLab: Filters → Quality Measure → Extract Feature Lines → export curves
- libigl (Python): `igl.principal_curvature` → threshold ridges/valleys
- Rhino native: `_Silhouette` (view-dependent), `_CurvatureAnalysis` (visual only)

**Failure modes:**
- Sensitive to mesh noise — pre-smoothing required (bilateral filter)
- Dense ribbed facade: each rib produces a ridge line — need to filter by curvature magnitude
- MeshLab path manual; not yet automated in pipeline

---

## Planned: v7 — Outer Envelope + Corner Labels + Zone Split

**Core changes vs v6:**

### 1. Outer envelope instead of RDP contour

```python
# Instead of: rdp(section_polyline, tolerance)
# Use: alpha_shape(section_polyline.vertices, alpha=2.0)
```

Alpha shape with alpha=1.5–3.0 m captures outer hull of section while ignoring internal rib geometry. ConvexHull is too aggressive (removes concave corners). Alpha shape preserves chamfered corners.

### 2. Corner label correspondence

```python
from scipy.spatial import KDTree
# ref_corners: convex hull vertices of reference (mid-shaft) section
# new_contour: alpha shape of target section
tree = KDTree(new_contour)
corner_indices = tree.query(ref_corners)[1]
# Reorder new_contour starting at corner_indices[0]
```

This guarantees front-left-corner on level A → front-left-corner on level B. Eliminates loft twist.

### 3. Zone detection + split

```python
areas = [section_area(z) for z in z_levels]
diffs = np.diff(areas) / areas[:-1]
zone_breaks = np.where(np.abs(diffs) > 0.15)[0]
# Zones: lower_shaft / mid_shaft / upper_shaft / crown_shoulder / roof_cap
```

Loft only within one zone. Crown = separate loft from own sections. Roof cap = flat planar polygon.

### Target parameters for this building

| Parameter | Value |
|-----------|-------|
| Z section step | 2–3 m in shaft, 1 m in crown |
| Alpha shape alpha | 2.0 m (tune visually) |
| Target corner count | 8–12 points per section |
| Zone break threshold | 15% area change |
| Seam start | max-X corner (rightmost) — stable reference |

### Expected result

- No twist (corner labels fix correspondence)
- No box artifacts (alpha shape preserves chamfers)
- Correct height (shaft + crown zone split)
- Correct roof cap (planar, not loft-through-collapse)
- Closed=True + architecturally valid

---

## Form Reading Research (2026-05-19)

Separate research track on how to accurately READ form from dense geometry before reconstruction.

**Root cause of section distortion:**
Uniform Z-sections waste budget on flat shaft regions, skip transition zones. Loft between incorrectly-spaced sections interpolates incorrectly → form distortion.

**Top strategies:**

| Strategy | Best for | Tools |
|---|---|---|
| Curvature-guided adaptive sections | Overall form capture | GH Mesh Curvature + Loft Tight |
| Feature line extraction | Ribbed facade | MeshLab / libigl |
| RANSAC plane segmentation | Flat walls, slabs | Open3D |
| Alpha shape outer envelope | Section cleanup | scipy / shapely |

**Key fix for loft seam twist:**
Run `_CurveSeam` in Rhino to align seam points on all section curves before lofting. Misaligned seams are one of the main causes of loft twisting independently of correspondence.

Full research note: `50 Research/Claude CAD Geometry 2026-04-28/form-reading-strategies-2026-05-19.md` in Obsidian vault.
