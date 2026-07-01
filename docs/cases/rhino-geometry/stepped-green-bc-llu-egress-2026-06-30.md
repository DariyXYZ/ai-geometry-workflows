# Stepped Green BC LLY Egress And Roof Cleanup 2026-06-30

## AI Extraction Summary

```yaml
case_family: rhino-geometry
status: "accepted after user-corrected rules"
use_when: "Scenario 3A business-center massing with stepped terraces, operated roofs, visible LLY/core zones, and a first-floor facade grid"
source_authority: "user-approved footprint and user-corrected Rhino model state"
geometry_grammar: "fixed footprint -> stepped floor-stack massing -> code/project core-count gate -> service-zone core layout -> roof-fit LLY shifts -> roof access volumes -> minimal LLY exits integrated into first-floor grid -> setback continuous parapet rings"
effective_rhino_gh_route: "McNeel RhinoMCP slot + RhinoCommon Python edits"
key_parameters:
  units: meters
  source_footprint_m2: 3737.9
  floors: 13
  top_height_m: 44.1
  core_strategy: "first decide required/plausible core count from SP/fire/evacuation/project logic; if 2 LLY cores are selected, divide the first-floor plate into serviced zones as a planning aid, often near equal area but not as a legal rule"
  roof_guard_strategy: "DupBorder -> inward setback -> Offset x 2 -> Extrude closed solid rings"
  parapet_default: "0.55 m edge setback, 0.32-0.42 m thickness, 1.18-1.2 m height for operated roofs"
  llu_exit_strategy: "4 minimal exits, two per core, aligned with LLY routes and the first-floor facade grid"
  facade_readability_strategy: "window/entry panels may get a tiny 0.06-0.10 m local-normal outset after they are correctly coplanar, so they read in Rhino without becoming floating boxes"
promoted_rules:
  - "Do not add dense facade/window/storefront detail before massing approval."
  - "For stepped/irregular roofs, build guards/parapets as continuous closed rings from roof borders, an inward edge setback, and two offsets; never assemble them from independent edge boxes."
  - "Decide core count from plate area, length, floor count, and core-to-glass depth before placing roof access volumes."
  - "Do not treat 50/50 area split as a norm. Core count comes first from SP/fire/evacuation strategy, people load, travel distance, floor plate, height, and project requirements."
  - "If two LLY cores are required or selected, divide the first-floor plan into rational serviced zones before placing cores; equal-area split is only a first-pass heuristic, not a hard rule."
  - "After choosing approximate core centers, compare them with the top roof/terrace footprint: either stop/cut the core at terrace level or shift it internally so the core reaches an operated roof."
  - "Roof access boxes must align with core zones; do not place one box on every terrace."
  - "LLY emergency exits are not public entrance portals. They should be minimal, direct, and tied to the core/service zone."
  - "Door/opening panels and frames must be generated from the local facade plane first; only after validation may they receive a tiny local-normal visual outset."
  - "Threshold pads/aprons may project outward; they are the only ground element that should visibly leave the facade plane."
  - "At first-floor detail stage, LLY exits must occupy clean facade-grid bays; move/adjust neighboring ground-floor windows instead of leaving windows behind exits."
  - "First-floor BC storefront/cafe glazing should be taller and closer to floor level than typical office windows."
failure_gates:
  - "Early dense facade detail hides unresolved massing decisions."
  - "Segment-box roof guards create broken corners on non-orthogonal roofs."
  - "Parapets placed on the exact roof edge make the roof edge disappear and can crawl onto the facade; use a small inward setback first."
  - "Random roof access boxes create bad floor fragments and do not prove egress."
  - "Decorative public entrance portals are a wrong answer when the issue is emergency egress from LLY."
  - "Facade elements modeled as large protruding boxes read as pasted-on objects, not openings."
  - "Facade panels with no visual offset can disappear into same-color massing in Rhino shaded views; use a tiny controlled offset, not a deep box."
  - "LLY exits that ignore the ground-floor window grid look accidental."
validation: "User accepted the final result after core count/layout logic was separated from the equal-area placement heuristic, exits were tied to LLY routes and facade bays, windows/entries received only tiny local-normal outsets, and parapets became inset continuous solid rings."
read_more_when: "building or cleaning BC/office massing with stepped terraces, roof guards, core/headhouse logic, and ground-floor egress markers"
related_error_rules:
  - "MBC-E17"
  - "MBC-E18"
  - "MBC-E19"
  - "MBC-E20"
```

## Goal

Refine a stepped green business-center massing so it remains a clean massing
review model while still showing the minimum architectural logic required for
operated roofs and evacuation.

The final requirement was not to create decorative public entrances. The
entrance-like marks had to be emergency exits directly from LLY/core zones,
shown minimally and integrated into the first-floor facade rhythm.

## What Failed

1. Dense facade detail appeared before the large form was fully accepted.
   This spent object count and attention on windows while massing questions were
   still active.

2. Roof guards were first made from independent edge boxes. On angled/stepped
   corners this created gaps, diagonal caps, and broken corner conditions.

3. Roof access volumes were initially scattered on terraces. They looked like
   random roof boxes rather than a core/service strategy.

4. A later attempt treated the request as public entrance design. It added
   portal/canopy/plaza accents, but the real requirement was emergency exits
   from LLY.

5. Minimal exit panels were then modeled as protruding boxes. The user corrected
   that openings and facade elements must lie in the facade plane.

6. Even coplanar exits are not enough if they ignore the first-floor grid. The
   user moved ground-floor windows so the exits occupy clean facade bays.

7. Later parapets followed the roof border but sat directly on the edge. The
   user corrected that operated-roof parapets should be inset from the edge so
   the roof slab/kromka remains visible and the parapet does not read as a
   facade cap.

8. Window and entry panels were technically in the facade plane, but in shaded
   Rhino they visually merged with the green mass. The acceptable fix was a
   very small local-normal outset after the facade-plane rule was satisfied,
   not a new protruding box grammar.

## Rules Promoted

### Massing Before Detail

At massing stage, dense windows, mullions, storefronts, and facade panels must
stay hidden until the user accepts the large form. Coarse facade intent may be
visible only when it helps read the massing.

### Roof Guards

For operated stepped roofs:

```text
DupBorder
-> setback inward from exposed roof edge
-> Offset x 2
-> Extrude
-> one continuous closed guard/parapet strip
```

Do not build guards as separate segment boxes on non-rectangular or stepped
roofs unless corner joining is explicitly solved.

For final review massing, keep an inset edge before the parapet. A useful
default from this case is:

```text
edge setback: 0.55 m
parapet thickness: 0.32-0.42 m
height: 1.18-1.20 m for operated roofs
```

The outer parapet line should sit inside the roof border, leaving a readable
roof edge/coping band outside the guard.

### Core And Roof Access

For an elongated office plate around `3700 m2` and `13F`, a two-core strategy
can be a plausible massing assumption, but it is not proven by area alone. Do
not turn this into a universal "from this area, add a second core" rule. The
actual count must be checked against SP/fire/evacuation strategy, people load,
travel distances, height/fire category, and project requirements. Show roof
access/headhouse volumes only where a core zone actually reaches an operated
roof.

Use this planning sequence before drawing roof access boxes:

```text
first-floor footprint
-> decide core count from SP/fire/evacuation strategy, people load, travel
   distance, floor plate size/length, height, and project requirements; do not
   use a single "second core from N m2" rule unless it is verified for this
   exact functional/fire-safety scenario
-> if 2+ cores are required/selected, split the plan into rational serviced
   zones; equal-area split is a first-pass heuristic only
-> place LLY cores near the functional center of each serviced zone
-> check the highest roof / top-floor footprint
-> either trim/stop the core at a terrace or shift it internally so the core can
   reach the operated roof
-> add roof access volume only above the accepted core position
```

Keep the service-zone split line, initial core markers, core shifts, and
core-to-exit routes on a helper/route layer. They are useful for audit and can
be hidden for final presentation.

### LLY Emergency Exits

LLY exits are egress markers, not public entrance design. For two core zones,
four minimal exits are a good massing default when two directions per core are
plausible.

Each exit should use:

- a small dark recessed panel;
- thin frame/opening markers;
- a modest threshold pad/apron.

The panel and frame must first be generated in the local facade plane. If the
same-color Rhino view makes them disappear, add only a tiny controlled outward
offset along the local facade normal, around `0.06-0.10 m`. This is a visual
readability offset, not permission to create a thick portal block. Only the
threshold pad projects outward horizontally.

### First-Floor Grid Coordination

When facade detail is visible, LLY exits must occupy clean first-floor facade
bays. Do not leave windows behind the exit or let the exit cut across a random
module. Move, remove, or adjust neighboring ground-floor windows so the exit
becomes part of the grid.

First-floor storefront/cafe windows should be visibly taller than typical
office windows and closer to floor level. In this case the first-floor layer
needed large retail/cafe glazing while the upper floors kept smaller repeated
office windows.

## Final Layer Logic

Visible review layers:

- final massing;
- roof/terrace/parapet/access volumes;
- LLY emergency exits;
- compact horizontal ground label.

Hidden review layers:

- source guides;
- core-route guides;
- future dense window grids and storefront/detail layers until approved;
- metrics/debug layers.

## Related Files

- `docs/errors/massing/moscow-bc-massing-error-library.md`
- `docs/workflows/massing/tep-massing-scenario-subtypes.md`
- `docs/libraries/standards/moscow-building-dimensional-library-2026.md`
- `docs/case-digest.md`
