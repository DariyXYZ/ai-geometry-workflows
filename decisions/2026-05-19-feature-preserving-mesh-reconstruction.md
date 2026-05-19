# Decision: Feature-Preserving Mesh Reconstruction Path

Date: 2026-05-19
Status: accepted for testing

## Context

Scenario 2 is the conversion of a high-poly fragmented Rhino architectural model into a simplified solid model without losing the major form decisions of the building.

The current section-stack approach remains useful, but it has shown limits:

- raw section lofting can deform the tower if seams and side/corner correspondence are not aligned;
- `isClosed` / `isSolid` is not enough if the large form is wrong;
- VSA produced useful plane clusters and feature edges, but not a watertight solid reconstruction;
- Rhino ShrinkWrap solves closure but tends to soften sharp corners and produce poor optimization/topology;
- pure quad remeshing does not infer missing architectural topology or clean massing intent.

## Decision

The next primary test path is:

> Plane / primitive-based polygonal surface reconstruction from mesh-derived point clouds.

The first serious candidate stack is:

- CGAL Shape Detection / Efficient RANSAC for plane and primitive extraction;
- CGAL Polygonal Surface Reconstruction for compact watertight polygonal output;
- CGAL 3D Alpha Wrapping as a ShrinkWrap-style baseline;
- Rhino QuadRemesh / Instant Meshes / QuadriFlow only as secondary post-processes after solid/fidelity validation.

## Reasoning

The desired output is not merely a smaller mesh or a nice quad grid. It must satisfy three separate gates:

1. **Topology**: closed / watertight / manifold.
2. **Architectural fidelity**: tower, podium, low-rise, crown, large transitions, sharp edges, and flat faces are preserved.
3. **Editability / topology quality**: quad-dominant or clean polygonal mesh where useful.

Architecture is often piecewise planar or piecewise primitive, so plane/primitive reconstruction is a better match than marching cubes, ShrinkWrap, Poisson reconstruction, or pure quad remeshing.

## First Experiment

Use a subset of `22.3dm`, not the whole file:

1. Select tower-only or tower + podium source group.
2. Export OBJ/PLY.
3. Sample/downsample to point cloud.
4. Estimate normals.
5. Detect major planes/primitives.
6. Build polygonal watertight candidate.
7. Import candidate into Rhino.
8. Validate:
   - closed/watertight/manifold state;
   - bbox per major volume;
   - multi-Z section width/depth/center deltas;
   - top/front/side overlays;
   - preservation of sharp corners and major transitions.

## Non-Goals For The First Test

- Do not solve the whole `22.3dm` scene in one run.
- Do not optimize for beautiful quad layout first.
- Do not treat VSA feature edges as a solid reconstruction.
- Do not accept a closed wrapper if the architectural form is wrong.

## Success Criteria

The approach is promising if it produces a compact closed mesh that:

- keeps large walls/roofs/podium faces flat;
- preserves sharp building corners and major transitions;
- reduces facade ribs/panel noise into larger faces;
- has lower face count than the source by at least one order of magnitude;
- passes section delta checks against the source.

## Implementation Notes

The likely prototype should live alongside `rhino_workflow_kit` as a mesh/point-cloud reconstruction track:

- `sample_mesh_points`
- `detect_planes`
- `reconstruct_polygonal_surface`
- `validate_reconstruction`
- `import_candidate_to_rhino`

The existing section-stack workflow remains as fallback and validation support.
