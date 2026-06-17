# Moscow BC Massing Error Library

This library records repeated massing failures from the Moscow business-center
tests. It is a pre-generation checklist: a variant that hits GFA, FAR, boundary,
and height envelope can still fail if it makes the site unusable or reads as a
random set of boxes.

## Current Case: 2026-06-16 V01-V03

The generated layers `AI_BC_V01`, `AI_BC_V02`, and `AI_BC_V03` passed the
numeric precheck:

| Variant | Strategy | Approx GFA vs project geometry | INSO check |
| --- | --- | ---: | --- |
| `AI_BC_V01` | envelope-following field | 0.984x | pass |
| `AI_BC_V02` | urban frame with accents | 0.970x | pass |
| `AI_BC_V03` | compact base with moderated dominant | 0.980x | pass |

User review still rejected them for site and architectural reasons:

- V01 and V03: low volumes cut across the plot and make movement impossible or
  ugly; all blocks are too simple and box-like.
- V02: site organization is strange; buildings intersect accidentally; narrow
  passages and leftover gaps make pedestrian movement weak.
- All variants: at least one architectural operator is needed, for example
  rounded corners, rotation, chamfers, cut-outs, voids, setbacks, or a controlled
  top-shape change.

## Error Codes

### `MBC-E01` Numeric Pass, Site Fail

Symptom: the variant passes plot boundary, INSO, floor module, and GFA checks,
but the plan cannot support normal movement, entry, service, or public space.

Detection:

- no reserved pedestrian spine before geometry;
- public route is crossed by long low bars;
- the remaining open space is residual rather than designed;
- no declared main entry, service edge, courtyard, or plaza.

Correction:

```text
zoning skeleton first
-> no-build movement corridors
-> buildable zones
-> massing footprints
-> TEP/INSO validation
```

### `MBC-E02` Low Bars Cut The Plot

Symptom: low horizontal volumes are used to recover GFA but behave like walls.
They split the site into disconnected pockets and block the natural desire line.

Detection:

- any bar longer than about 60 m crosses the primary pedestrian spine;
- pedestrian movement must make an awkward detour around a low block;
- two bars create a corridor without a clear destination.

Correction:

- Long bars may define the edge of a public space, not cross it.
- If a bar must cross a route, it must become a gate/bridge/arcade with a
  real opening, not a solid slab.
- Reserve a continuous public spine first, normally 16-20 m wide for this
  scale; keep service lanes separate.

### `MBC-E03` Box-Only Architecture

Symptom: the result is a set of plain rectangular prisms. It may be clean CAD,
but it has no architectural decision.

Detection:

- all footprints are axis-aligned rectangles;
- all towers extrude unchanged to the roof;
- no corner treatment, taper, setback, void, rotation, cut-out, or roof
  expression exists;
- the form operator is not tied to a site reason.

Correction:

Every accepted variant must use at least one explicit architectural operator:

- rounded or softened office-plate corners;
- controlled rotation that follows a site edge, view, or entry axis;
- chamfered corner toward a gate, plaza, or red-line kink;
- courtyard or public void cut from a larger base;
- setback/taper responding to INSO or context;
- roof/upper-floor step-down toward sensitive edges.

The operator must be named in metadata or the report.

### `MBC-E04` Accidental Intersections

Symptom: a tower and bar overlap as if they were a stylobate relationship, but
the geometry reads as accidental collision or objects pushed into one another.

Detection:

- tower footprint only partially overlaps the base;
- bar cuts through a tower side without an architectural joint;
- no shared base outline, podium edge, shadow joint, or deliberate connection;
- objects are too close to be separate and too uncoordinated to be one building.

Correction:

Choose one relationship before modeling:

```text
tower_on_stylobate: tower sits fully on base, base reads as one public layer
separate_blocks: keep full pedestrian/fire/service spacing between objects
bridge_or_gate: crossing volume is elevated or perforated with a clear opening
```

Do not mix these relationships accidentally.

### `MBC-E05` Narrow Residual Gaps

Symptom: gaps between buildings are technically empty but too narrow, dark, or
directionless to work as outdoor rooms or passages.

Detection:

- public passage below 12 m;
- main public/courtyard space below 24-30 m clear width;
- service/fire lane below 6-8 m;
- parallel office plates face each other across a leftover slot;
- the gap does not connect two meaningful destinations.

Correction:

- Classify every gap as public passage, courtyard/plaza, service/fire lane, or
  private setback.
- Delete or merge volumes that create unclassified leftover space.
- Treat narrow unprogrammed slots as failure, not as landscape.

### `MBC-E06` No Zoning Before Massing

Symptom: buildings are placed first and circulation is rationalized later.

Detection:

- no drawing or parameter set exists for public spine, entries, service, open
  space, and buildable zones before volume generation;
- tower anchors are chosen by envelope height only;
- form family is selected before site edges and movement.

Correction:

Before any Rhino geometry, define:

- primary public edge;
- entry point(s);
- public spine or courtyard;
- service/fire edge;
- buildable bands;
- tower anchors;
- low/no-build zones;
- view/context orientation.

### `MBC-E07` Towers As Area Recovery Only

Symptom: tower placement is used only to recover GFA after bars and setbacks,
not to mark an entry, view axis, urban corner, or public space.

Detection:

- tower sits in a leftover pocket;
- tower blocks the main courtyard or spine;
- tower has no base/address relationship;
- height does not help orientation.

Correction:

Height must do at least one of:

- mark the main address or entry;
- sit beside, not inside, the main public spine;
- use the highest INSO zone without blocking movement;
- strengthen a view or context edge;
- free ground by consolidating area into a smaller footprint.

### `MBC-E08` TEP/INSO Validation Treated As Acceptance

Symptom: the workflow stops after "inside boundary, below INSO, close GFA".

Detection:

- no post-check for movement, open-space quality, gap widths, tower/base
  relationship, or architectural operator.

Correction:

Numerical constraints are only the first gate. The acceptance order is:

```text
hard constraints
-> zoning and movement
-> footprint relationships
-> massing grammar/operator
-> TEP/GFA balancing
-> final clean Rhino layers
```

## Mandatory Prebuild Gate

No new Moscow BC variant should be generated until this table is filled:

| Gate | Required answer |
| --- | --- |
| Primary public spine | Where is it, and what clear width is reserved? |
| Service/fire edge | Where does non-public movement happen? |
| Main entry/address | Which edge or node gives the BC its address? |
| Open-space type | Courtyard, plaza, linear spine, campus field, or gate? |
| Buildable bands | Which zones can receive mass without blocking movement? |
| Height anchors | Where can height help instead of harm? |
| Variant operator | What architectural move makes this more than boxes? |
| Gap classification | Are all gaps public, service, courtyard, or setback? |

If one row is missing, do not generate geometry.
