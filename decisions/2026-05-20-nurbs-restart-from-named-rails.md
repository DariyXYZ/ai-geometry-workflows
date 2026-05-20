# Decision: NURBS Restart from Named Architectural Rails

Date: 2026-05-20
Status: active direction
Context: Scenario 2 (simplified model from complex source)

## Problem

After 12 iterations (v8–v20) of Python mesh-simplification scripts, mesh-primitive approaches failed to produce usable architectural massing:

- Point envelopes (v9/v10): organic surface following facade rib noise, not architectural intent
- Prism/convex blockout (v11): too abstract, loses actual form decisions
- Concave hull parts (v12/v13): correct concept but incorrect form reading — missed the two major overlapping volumes
- Named primitive slabs (v14/v15): invented geometry (crown_slab_solid_01..03) not present in source
- Sloped halves (v16/v17): correct form interpretation but wrong implementation — perimeter-only concave hulls create false voids in plan

The missing layer is not a better hull algorithm. It is architectural correspondence:
- Which vertical edges run continuously from base to top?
- Which silhouette curves define each face family?
- Where are the major form transitions, and how do they relate across views?

## Decision

Restart Scenario 2 with a NURBS/Brep approach built on **named architectural rails**.

Do NOT start with: `Loft(all horizontal sections)`, `Patch(scatter points)`, `NetworkSrf(noisy ribs)`.

START with 8 named rails extracted from the source:

1. `front_left_edge` — vertical major edge, front-left corner
2. `front_right_edge` — vertical major edge, front-right corner
3. `rear_left_edge` — vertical major edge, rear-left corner
4. `rear_right_edge` — vertical major edge, rear-right corner
5. `central_valley_or_seam` — central vertical seam between the two mass halves
6. `left_top_cut` — sloped top silhouette, left side
7. `right_top_cut` — sloped top silhouette, right side
8. `rounded_side_rail` — profile of the rounded/curved side volume

## Implementation Sequence

1. Extract rails: fit from long vertical feature lines, high-Z silhouette edges, plan footprint rails
2. Import as Rhino diagnostic curves on named layers (N00_Source_Sections, N01_Facade_Rails, N02_Top_Cut_Rails, N03_Plan_Footprint_Rails)
3. Capture front/top/side views and verify each rail matches the source
4. Build surfaces by patch type: EdgeSrf for flat facades, Sweep1 for rounded side, ruled surface for sloped cuts
5. Join/cap only after surface boundaries coincide
6. Validate: front silhouette, top footprint, section deltas, no invented crown slabs

## Why NURBS

The output must be Rhino-editable. A triangulated mesh of ~1000 faces cannot be pushed/pulled in Rhino the way a designer works. NURBS surfaces with clean boundaries can be modified individually — each face family is one surface.

## Non-Goals

- Do not produce a beautiful quad mesh from scratch
- Do not try to solve the whole scene in one run
- Do not loft through section topology changes
- Do not accept isClosed=True if the large form is architecturally wrong

## Previous Decision

See `2026-05-19-feature-preserving-mesh-reconstruction.md` — CGAL-based approach is still valid as a research direction but requires more setup time. The NURBS rails approach is a faster path to a designer-usable result.
