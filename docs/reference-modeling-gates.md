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

- build one part and mirror/repeat;
- loft sections through known datums;
- extrude a footprint;
- array floor/bay modules;
- use guide curves only;
- postpone detail.

Do not model one outer envelope when the building is visibly composed from
repeated or mirrored parts.

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

