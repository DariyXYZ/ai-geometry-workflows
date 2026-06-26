# Moscow BC Site Zoning Patterns

This note defines the missing layer between constraints and massing geometry:
site zoning. It should be read before generating new Moscow business-center
massing variants from TEPs.

The main lesson from the 2026-06-16 tests is blunt: a model can be under the
INSO envelope and still be a bad business center because it blocks movement,
creates leftover slots, and has no address logic.

## Scenario 3 Subtype Fit

Read `docs/workflows/massing/tep-massing-scenario-subtypes.md` first.

This zoning workflow applies most strongly to `3B`, when only the plot,
entries/access, constraints, and TEP are given. In that case the first output is
a zoning/footprint proposal, not final architecture.

For `3A`, where footprints, entries, and zoning are already given, treat those
inputs as source authority. Use this note only as a validation checklist; do not
invent a new site plan.

For `3C`, where an existing massing iteration is given, use the existing
massing as the TEP/gabarit anchor. Use this note to diagnose and repair movement
or gap problems, but keep the task centered on image/form revision unless the
user asks for a full rezoning.

## Required Output Before Geometry

Before any volume is created, generate a zoning skeleton with these fields:

```yaml
site_zoning:
  primary_public_spine:
    path: required
    clear_width_m: 16-20
    must_not_be_crossed_by_solid_bars: true
  main_entry_or_address_node:
    position: required
    connected_to_spine: true
  service_and_fire_edge:
    path: required
    clear_width_m: 6-8
    separated_from_main_public_spine: preferred
  open_space:
    type: [linear_spine, courtyard, plaza, campus_field, gate_sequence]
    minimum_clear_width_m: 24-30 for primary courtyard/plaza
  buildable_bands:
    - name
    - role
    - max_depth_m
    - allowed_height_range
  height_anchors:
    - position
    - reason
    - envelope_limit
  forbidden_zones:
    - public_spine
    - entry_plaza
    - service_turning_or_fire_access
    - narrow_leftover_slots
```

The massing generator should consume this zoning skeleton. It must not infer it
after the buildings have already been placed.

## How Modern BC And Residential Sites Usually Organize Territory

### 1. Public Spine First

Contemporary business-center and mixed-use campuses often start with a clear
pedestrian route: from transit/drop-off/street to lobby, courtyard, food/retail,
or a second exit. This spine can be straight, diagonal, or gently curved, but it
must be legible.

Rules:

- keep the main public spine free of solid building volumes;
- let buildings frame it from the side;
- place lobbies and active ground floors on it;
- use bridges/gates only when the opening is explicit and generous;
- avoid "threading" people through narrow leftovers between unrelated masses.

For Moscow BC massing, a main spine should normally be at least 16-20 m clear
when it is the primary outdoor movement and address space.

### 2. Open Space Is Designed, Not Left Over

Modern residential quarters often work with a public-to-private gradient:
street/public edge -> entrance court -> semi-private yard -> private/service
edges. Business centers use a similar gradient:

```text
city edge / drop-off
-> address plaza
-> lobby/public spine
-> inner courtyard or campus field
-> service/back-of-house edge
```

Rules:

- a courtyard or plaza should be a named space with clear dimensions;
- leftover slots between plates are not courtyards;
- if a space is too narrow, classify it as service/setback or delete the cause;
- active first-floor fronts should face the public spine or plaza.

### 3. Buildings Frame Routes Instead Of Blocking Them

Long bars are useful only when they form an edge, acoustic screen, street wall,
or courtyard side. They fail when they cut across the route people naturally
want to take.

Rules:

- align bars with site edges, street lines, or the public spine;
- do not place long bars perpendicular to the primary pedestrian route unless
  they are raised/perforated as a gate;
- keep bars shallow enough for office daylight;
- separate parallel plates enough to make a real street/court, not a slot.

### 4. Towers Need Address And Ground Logic

A tower is not just an area-recovery tool. It should help orientation.

Good tower anchors:

- beside the main entry or address plaza;
- at an urban corner or visible approach;
- along a view axis without blocking it;
- in the deepest or highest-envelope zone if it frees public ground;
- on a clear stylobate/base, not colliding with a random bar.

Bad tower anchors:

- in the middle of the main pedestrian spine;
- inside a residual pocket;
- partly embedded in a low bar with no podium logic;
- next to another plate across a narrow shadow slot.

### 5. Service Is A Real Layer

Business centers need loading, fire access, parking access, waste, technical
rooms, and maintenance. If service is not assigned early, it later damages the
first floor and public space.

Rules:

- reserve a service/fire edge before placing public volumes;
- do not mix loading with the main public entry unless the brief requires it;
- service lanes need 6-8 m clear width as a planning placeholder;
- avoid dead-end public pockets created by service backs.

### 6. Architectural Operators Must Have A Site Reason

The generator must use at least one architectural operator per variant, but the
operator cannot be decoration only.

Useful operator-to-site mappings:

| Site condition | Operator |
| --- | --- |
| red-line kink or acute corner | chamfer/cut corner toward plaza or gate |
| curved/diagonal pedestrian spine | rotate plates or soften corners along route |
| INSO height falloff | step down, taper, or setback upper floors |
| main entry node | void, gate, raised notch, or widened base |
| sensitive/context edge | lower terrace, setback, or smaller plate depth |
| need for skyline marker | tower with softened/chamfered top, not a plain prism |

## Recommended Pattern Families

### Pattern A: Linear Public Spine With Side Plates

Use when the plot is elongated or irregular and there is a clear desire line.

```text
public spine through plot
buildable bands on both sides
height anchors beside spine
low bars parallel to spine
no solid bar crossing the spine
```

This is the safest next pattern for the current Moscow BC site.

### Pattern B: Courtyard/Plaza With Framing Bars

Use when the site can support one strong outdoor room.

```text
entry plaza
3-sided frame or two bars plus tower
24-30 m minimum primary open-space width
service on back edge
clear gates in the frame
```

Do not close the courtyard so tightly that it becomes a shaft.

### Pattern C: Stylobate Plus Towers

Use when density is high and INSO allows concentrated height.

```text
continuous public base
towers sit fully on base
base contains lobbies/retail/service/parking logic
tower spacing produces light and air
no accidental bar/tower collisions
```

A stylobate is not any low rectangle. It must read as one public/technical
ground system.

### Pattern D: Terraced Envelope Field

Use when the INSO envelope strongly slopes across the site.

```text
high anchors in high-envelope zones
mid volumes step down
low volumes near sensitive/low-envelope edge
open spine remains continuous
roofscape/terraces face the useful public or view side
```

This pattern should not become scattered boxes; it still needs a spine,
fronts, and named open spaces.

## Current Moscow BC Site Diagnosis

Based on the Rhino scene and the marked-up review images, the current site is
an irregular elongated polygon with a strong diagonal movement opportunity.
The INSO envelope allows more height toward the west/southwest and drops toward
the east/northeast.

Working zoning hypothesis:

1. Reserve a continuous diagonal/curved public spine from the southwest/lower
   entry side toward the northeast/top side.
2. Do not cross this spine with solid low bars.
3. Put taller volumes beside the spine, not on top of it, mainly in the western
   and southwestern higher-envelope zones.
4. Put lower volumes and terraces toward the east/northeast where the envelope
   is lower.
5. Use bars only as edges to the spine/courtyard, ideally parallel or oblique
   to the route, not as walls across it.
6. Define a service/fire edge separately; do not force service through the main
   public spine.
7. Give every variant at least one named operator:
   - chamfered/rounded corners facing the spine;
   - rotated plates following the site diagonal;
   - cut-through gate/void at the main passage;
   - upper-level setbacks responding to INSO.

## Simple Generation Algorithm

```text
1. Read plot boundary and INSO.
2. Classify the long/diagonal site axis.
3. Reserve public spine polyline and buffer it by 8-10 m each side.
4. Reserve service/fire edge.
5. Compute buildable polygons as boundary minus public/service reservations.
6. Pick 2-4 buildable bands, each with role:
   address bar, tower anchor, mid plate, low terrace, service edge.
7. Place volumes inside bands only.
8. Apply one site-reasoned operator to each variant.
9. Validate:
   boundary, INSO, floor module, GFA,
   no spine crossing,
   min public gap width,
   no accidental intersections,
   no box-only variant.
10. Only then write Rhino geometry.
```

## Pre-Rhino Acceptance Checklist

- [ ] A public spine is named and dimensioned.
- [ ] No solid low bar crosses the public spine.
- [ ] Service/fire access is assigned.
- [ ] Every gap has a role: public, courtyard, service, or setback.
- [ ] No public gap is below 12 m.
- [ ] No primary courtyard/plaza is below 24 m clear width.
- [ ] Tower/base relationships are explicit.
- [ ] At least one architectural operator is used and justified.
- [ ] GFA/INSO checks are run after, not before, the zoning skeleton.
