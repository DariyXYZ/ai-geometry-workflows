# 2026-06-01 - Infinity Tower user Rhino curves as source authority

## Status

Accepted as a near-successful Scenario 1 reference-to-model case.

## Context

The Infinity Tower / SOM test started with unusually strong Rhino scene
evidence:

- the drawing was already placed in Rhino at 1:1 scale;
- the scene units were meters;
- the user stated the total height was 300 m;
- the user had prepared three visible source curves:
  - floor contour;
  - circular core;
  - vertical height/twist axis.

The initial generated model failed because it replaced the floor contour with a
generic square/chamfered parametric section. That was a source-authority error,
not a geometry-tool limitation.

After correction, the build read the visible Rhino curves, verified the 300 m
axis, and generated the tower by rotating exact copies of the user floor contour
through height. This produced a recognizable twisting shaft and preserved the
prepared core/contour evidence.

## Decision

When a user prepares Rhino curves for a reference-modeling case, those curves
outrank descriptive approximations and screenshot interpretation.

Required workflow:

```text
visible Rhino source curves
-> classify floor contour / core / height axis
-> verify scene units and axis height
-> use the exact floor contour as the repeated section
-> rotate/transform copies through Z
-> loft primary form and derive floor/facade guides from those copies
-> compare with photos/drawing
```

Do not replace a user-prepared contour with a parametric rectangle, square,
trapezoid, or generic polygon unless the user explicitly asks for an
approximation.

## Source Authority Table

| Source | Authority |
| --- | --- |
| User text | Building identity, total height 300 m, grammar: one section rotates with height. |
| Rhino scene units | Meters; no unit conversion needed. |
| User floor contour curve | Exact repeated floor plate shape for this modeling pass. |
| User circular core curve | Core location and approximate core radius. |
| User vertical line | Height axis and hard 300 m datum. |
| Photos | Recognition check: twist direction/reading, facade density, crown openness. |
| Sheet image | Confirms the idea of repeated plan types and tower section but is secondary after the user-prepared Rhino curves. |

## Consequences

- A "single rotating section" is not permission to invent the section.
- Rhino readback must inspect visible curves before building.
- If source curves exist, generated floor plates and facade guide curves should
  be transformed from those curves, not rebuilt from bbox corners.
- The corrected result is a valid massing/detail-guide pass, but final
  acceptance still needs user visual approval and, if required, facade/crown
  refinement.

