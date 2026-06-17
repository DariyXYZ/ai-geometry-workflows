# Form Operator Library

This is a compact repo version of the Obsidian research note:

```text
50 Research\Moscow Massing\Form Operator Library 2026.md
```

Use it in Scenario 3 when a massing variant risks becoming a plain box, a
random sculpture, or a numerically valid but architecturally weak object.

## Operator Selection Rule

Do not apply operators as decoration. Each operator must answer at least one
site, TEP, view, movement, daylight, approval, or constructability reason.

```text
constraint / site intent
-> base footprint
-> one primary operator
-> one secondary operator only if needed
-> TEP and height validation
-> movement/open-space validation
```

## Core Operators

| Operator | Use when | Geometry logic | Main risk |
| --- | --- | --- | --- |
| Chamfered edge | Need to soften a corner, open a view, respect boundary, or reduce collision | Cut one or more footprint corners by a controlled diagonal | Random chamfers that do not relate to entries/views |
| Rotated volume | Need orientation to a street, view corridor, or public spine | Rotate a block/tower around a clear anchor while preserving usable floor depth | Creating leftover triangular gaps |
| Rounded / soft corner | Need public-facing softness or premium office image | Fillet corners or use rounded rectangle footprint within buildable band | Organic blob, hard-to-build facade |
| Setback / terrace cascade | Need height step-down, daylight, roof terraces, or INSO compliance | Reduce upper floor plates in repeated steps | Losing TEP or stepping inward away from the useful side |
| Taper / narrowing upward | Need lighter skyline, wind/daylight response, or dominant silhouette | Upper plates shrink along one or two axes | Over-sculpted tower, inefficient core-to-plate ratio |
| Vertical notch / slot | Need permeability, entry marker, sky gap, or mass reduction | Subtract a vertical void from a larger volume | Fake slit that does not create real space or light |
| Podium cutout / courtyard | Need public court, drop-off, or internal open space | Remove a void from podium or split podium around court | Courtyard becomes narrow residual shaft |
| Crown accent | Need visible top and skyline identity | Change top floors by step, cut, frame, or cap | Decorative hat unrelated to tower logic |
| Base arcade / active edge | Need public ground floor activation | Recess or articulate ground-floor edge while preserving mass above | Over-modeling detail in massing stage |
| Split mass / shadow joint | Need to avoid accidental collision of podium and tower | Separate volumes by clean gap or explicit vertical joint | Uncontrolled intersection reads as geometry error |
| Bridged pair | Need connection between two blocks | Add a controlled connector above a clear public path | Bridge blocks movement or creates dark leftover space |
| Perimeter block with dominant | Need urban block logic plus landmark | Create lower edge-forming mass and one taller anchor | Closed wall that blocks site permeability |
| Compact podium plus tower | Need office TEP efficiency and clear hierarchy | Podium handles public/base program; tower rises from clear anchor | Podium becomes too wide and consumes landscape |
| Skyline cluster | Need multiple height anchors | Group 2-3 towers with stepped heights and shared base logic | Random tower scatter |
| Low-midrise contextual block | Need quiet insertion near sensitive context | Keep 4-8 floor volumes, courtyards, setbacks | Too generic without one site-reasoned operator |

## Operator Gates

Before Rhino modeling, declare:

- primary operator;
- why it belongs on this site;
- which edge/axis/view/entry controls it;
- how TEP is preserved;
- how movement remains continuous;
- how the operator stays below height/INSO constraints.

## Anti-Patterns

- Box-only massing with no architectural move.
- Decorative chamfers, rotations, or curves with no site reason.
- Operator applied before zoning.
- Multiple operators competing in one small variant.
- Accidental intersections presented as podium/tower composition.
- Long low bars cutting pedestrian continuity.
- Tiny leftover gaps that are too narrow to be public space.

## Minimal Scenario 3B Use

For plot-plus-entries tasks:

```text
entries
-> public spine / service edge
-> buildable bands
-> footprint families
-> choose one operator per family
-> generate simple volumes
-> validate movement and open space before image refinement
```
