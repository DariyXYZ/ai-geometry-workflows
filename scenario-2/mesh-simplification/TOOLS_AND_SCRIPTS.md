# Scenario 2: Tools and Scripts

All tools, scripts, and libraries used or evaluated for mesh simplification.

---

## Active Scripts

### vsa_simplify.py

**Path:** `C:\VS Code\tools\cad-mesh-tools\vsa_simplify.py`
**Purpose:** Variational Shape Approximation — segment mesh into planar patches

```bash
python vsa_simplify.py building.obj out/building --proxies 60 --reconstruct
```

**Outputs:**
- `_segmented.obj` — mesh colored by cluster (visualization)
- `_edges.obj` — sharp feature edges between clusters
- `_proxies.csv` — normal + centroid per planar region
- `_simplified.obj` — reconstructed simplified mesh (convex hull per patch)

**Status:** Implemented. Not yet tested on this building — pending OBJ export from Rhino.

---

### rhino_export_for_vsa.py

**Path:** `C:\VS Code\tools\cad-mesh-tools\rhino_export_for_vsa.py`
**Purpose:** Export Rhino document mesh to OBJ for VSA processing

**Run inside Rhino:** `Tools → Python Script → Run`

**Output:** `C:\temp\vsa_input.obj`

**Also includes:** `import_edges_from_obj()` function to bring feature edges back as Rhino curves on layer `VSA_FeatureEdges`.

---

## Python Libraries

| Library | Purpose | Status |
|---------|---------|--------|
| trimesh | Mesh loading, section extraction, export | ✅ Active |
| numpy | Array math, normals, curvature | ✅ Active |
| scipy | KDTree (corner matching), ConvexHull | ✅ Active |
| shapely | Alpha shape, polygon ops | 📋 Needed for v7 |
| matplotlib | Cluster coloring | ✅ Active |
| Open3D | RANSAC plane segmentation, point cloud | 🔬 Evaluated |
| libigl | Principal curvature, feature edges | 🔬 Evaluated |

**Install:**
```bash
pip install trimesh numpy scipy shapely matplotlib open3d
```

---

## Rhino / GH Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `_Mesh` | Convert BREP → mesh | Use before OBJ export |
| `_CurvatureAnalysis` | False-color curvature map | Visual form reading |
| `_Silhouette` | View-dependent silhouette curves | View-dependent |
| `_CurveSeam` | Align seam point on section curves | MANDATORY before loft |
| `_Unweld 25` | Hard edges on generated mesh | Display fix |
| `QuadRemesh` | Rhino 8 quad remeshing with crease detection | Fallback |
| Mesh Curvature (GH) | Gaussian/Mean curvature per vertex | Form reading in GH |

---

## External Tools (Evaluated)

### MeshLab

**Use:** Filters → Quality Measure → Extract Feature Lines

Extracts ridge/valley lines and sharp edges from mesh. Export as curves → import into Rhino. Most practical path for feature line extraction without Python.

**Limitations:** Manual workflow, not scriptable from pipeline.

---

### CGAL VSA

**Use:** CGAL Polygonal Surface Reconstruction / VSA

C++ library with Python bindings (cgal-python). State-of-art for architectural mesh segmentation.

**Status:** Not integrated. Python bindings have limited documentation. Long-term option if custom pipeline is needed.

---

## Pending Tools for v7

### alpha_shape (shapely / custom)

Alpha shape from 2D point set (section vertices projected to XY). Gives outer hull that ignores interior rib points.

```python
# Option 1: via shapely + Delaunay
from shapely.ops import cascaded_union
from shapely.geometry import MultiPoint
# alpha_shape(points, alpha) → Polygon

# Option 2: scikit-learn AlphaShape (if available)
# Option 3: custom Delaunay edge filtering
```

---

## Codex Prompt

**Path:** `C:\VS Code\tools\cad-mesh-tools\CODEX_PROMPT.md`

Self-contained prompt for Codex or any AI agent to execute the full pipeline end-to-end. Includes step-by-step instructions, parameters, success criteria, and troubleshooting.
