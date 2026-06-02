# Reference Modeling Gates

Дата: 2026-05-28

Этот документ задает обязательный порядок мышления для Scenario 1: модель из
текста, картинок, планов, фасадов и референсов.

## Gate 0 - Source Authority

Перед построением нужно записать, что доказывает каждый источник:

| Source | Authority |
| --- | --- |
| Text | numeric facts, program, explicit constraints |
| Plan/top view | footprint, axes, repeated parts, gaps, core/void positions |
| Elevation/facade | height, vertical datums, setbacks, twist start/end, crown zones |
| Section/structural image | cores, outriggers, slabs, belts, structural logic |
| Perspective/photo | silhouette reading, material/rhythm hints, visual check |

If a source is not authoritative for a dimension, do not use it as that
dimension's hard anchor.

## Gate 1 - Constructive Grammar

Before geometry, state what the object is made from.

Examples:

```text
four square shafts around a cross
stacked stepped podium + tapered tower
single core + perimeter columns + outrigger belts
repeated floor plates + rotated middle zone
```

If the grammar is unknown, stop and ask for more views or declare assumptions.

## Gate 2 - Section And Repetition Strategy

Pick the build strategy before scripting:

- compose primitives and use modeling operations: trim, boolean, offset, loft,
  sweep, contour, mirror, array;
- build one part and mirror/repeat;
- loft sections through known datums;
- extrude a footprint;
- array floor/bay modules;
- use guide curves only;
- postpone detail.

Do not model one outer envelope when the building is visibly composed from
repeated or mirrored parts.

Do not draw a complex architectural section as a blind point cloud when it can
be built from primitives. A stronger modeling sequence is usually:

```text
primitive frame
-> curve/surface smoothing if needed
-> trim/boolean/cut with explicit cutters
-> transform/repeat/loft
```

Point-by-point construction is acceptable for final resampling or for curves
extracted from a source, but it should not replace the building's constructive
operations.

## Gate 3 - Missing View Check

Ask for more references if any of these are unresolved:

- footprint shape or dimensions;
- gap/void locations;
- side depth;
- twist direction;
- start/end levels of major shape change;
- whether a visible line is facade, structure, shadow, or internal core.

The correct action is to request a view, not to invent a plausible form.

## Gate 4 - Geometry

Only after Gates 0-3:

```text
semantic parts
-> section/repetition plan
-> Rhino/build123d script
-> capture
-> compare
```

## Karlatornet Lesson

The first Karlatornet blockout failed because it skipped Gate 1. It built a
single guessed envelope. The correct constructive grammar is:

```text
33 x 33 m plan
4 square shafts
central cross/gaps
facade-derived twist datums
lofted twist sections
mirror/repeat into four quadrants
inner cross/facade completion
```

This is the required mental model for similar reference-driven towers.

### Vertical Section Strategy

Karlatornet-like twisted shaft forms should not be forced into horizontal
section stacks when the visible grammar is four vertical primitives whose side
faces twist through a middle zone. For this family, the simpler and more
faithful route is:

```text
primitive shaft blocks
-> vertical guide/profile curves on one shaft or facade side
-> loft the transition surface between lower and upper vertical profiles
-> mirror/repeat the solved part into the other quadrants
-> complete the central cross/gaps
```

Use horizontal contours for validation or floor/facade checking only after the
vertical face logic is understood. If the source proves that floor plates are
the controlling geometry, use a horizontal-contour workflow instead.

Rule of thumb:

```text
Grove at Grand Bay = horizontal floor contour problem
Karlatornet = vertical face/profile loft problem
```

## Grove at Grand Bay Lesson

For towers where the source gives several rotated orthogonal floor sections,
the correct intermediate-floor strategy is:

```text
authoritative floor sections
-> temporary loft
-> Rhino Contour at floor elevations
-> hide loft
-> build final slabs from contour curves
```

This avoids the common error of creating warped intermediate floors by
resampling corners or interpolating curve parameters manually. The final model
must treat the contour curves as exact floor plates. Any podium, underlay, or
reference plate must stay below the first-floor datum and must not compress or
occlude the tower.

### Slab Edge Is Not Glass Line

For balcony towers such as Grove at Grand Bay, the section contour usually
describes the exterior slab or balcony edge, not the glazing line. The build
order must keep these separate:

```text
Contour curve
-> thick floor slab / balcony plate
-> inward-offset glass plane
-> exterior rail / edge profile
```

If the glass is placed coplanar with the contour edge, the balconies disappear
and the facade reads as a flat box. Scripts must preserve slab thickness and
balcony offset before adding facade transparency.

## Infinity Tower Lesson

When the user has already prepared Rhino curves for a reference case, those
curves are the highest source authority for the parts they represent. For
Infinity Tower / SOM, the user supplied:

```text
floor contour curve
core circle
vertical 300 m axis
```

The correct constructive grammar is:

```text
one exact floor contour
-> repeated through height
-> rotated around the core/axis
-> lofted primary shaft
-> floor/facade guides derived from the same transformed contours
```

Do not replace the supplied contour with an approximate square, rectangle,
trapezoid, or generic chamfered section. The phrase "one section rotates with
height" describes the transformation, not permission to invent the section.

Required pre-build readback for similar Rhino-prepared cases:

1. list visible curves;
2. classify floor/core/axis;
3. verify units and axis height;
4. only then generate transformed copies and loft.

## Shanghai Tower-Style Cut Section Lesson

For a Shanghai Tower-style twisting shaft, the plan grammar is not a rounded
blob. Treat the source as a small constructive sequence:

```text
triangle frame
-> softened triangular floor plate
-> rotated square cutter at one corner
-> square subtracts the corner cut
-> 4 primary control sections
-> 180 degree twist over 632 m
-> loft validation
-> Contour floors only after the form is accepted
```

Gate requirement: if a cutter is part of the grammar, it must drive the final
curve. A visible square beside the section is not enough. The section outline
must come from `soft triangle minus square`, either with Rhino trim/boolean
operations or an explicit 2D intersection algorithm. Separate hand-authored
notch points are only acceptable as a temporary sketch and must be labelled as
such.

## Flock Chapel Shell Lesson

For low shell buildings with a scaled plan underlay and section datums, the
source authority split is:

```text
plan = footprint, shell length/depth, support/plinth locations
sections = crest and valley heights, ground/contact logic
photos = visual reading of wave shell, material, rim thickness
```

Do not add glass, mullions, timber posts, stairs, or other secondary elements
until the shell passes the footprint and support gates. The acceptance order is:

```text
fit shell to scaled plan
-> validate crest/valley heights from sections
-> place concrete folds / plinth supports under low contact lines
-> add shell thickness and rim
-> only then add glass/posts under the accepted shell
```

A shell that reads visually close but is too long on the plan or floats above
its folded concrete supports is a medium-success massing, not an accepted model.
