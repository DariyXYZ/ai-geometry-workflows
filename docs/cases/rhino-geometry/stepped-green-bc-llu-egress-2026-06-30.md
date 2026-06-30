# Stepped Green BC LLY Egress And Roof Cleanup 2026-06-30

## AI Extraction Summary

```yaml
case_family: rhino-geometry
status: "medium-success / user-corrected rules"
use_when: "Scenario 3A business-center massing with stepped terraces, operated roofs, visible LLY/core zones, and a first-floor facade grid"
source_authority: "user-approved footprint and user-corrected Rhino model state"
geometry_grammar: "fixed footprint -> stepped floor-stack massing -> continuous roof guard rings -> planned core zones -> roof access volumes -> minimal LLY emergency exits integrated into first-floor grid"
effective_rhino_gh_route: "McNeel RhinoMCP slot + RhinoCommon Python edits"
key_parameters:
  units: meters
  source_footprint_m2: 3737.9
  floors: 13
  top_height_m: 44.1
  core_strategy: "2 core zones for elongated office plate"
  roof_guard_strategy: "DupBorder -> Offset x 2 -> Extrude closed rings"
  llu_exit_strategy: "4 minimal exits, two per core, coplanar with local facade plane"
promoted_rules:
  - "Do not add dense facade/window/storefront detail before massing approval."
  - "For stepped/irregular roofs, build guards as continuous closed rings from roof borders and offsets, not as independent edge boxes."
  - "Decide core count from plate area, length, floor count, and core-to-glass depth before placing roof access volumes."
  - "Roof access boxes must align with core zones; do not place one box on every terrace."
  - "LLY emergency exits are not public entrance portals. They should be minimal, direct, and tied to the core/service zone."
  - "Door/opening panels and frames must lie in the local facade plane; only threshold pads/aprons project outward."
  - "At first-floor detail stage, LLY exits must occupy clean facade-grid bays; move/adjust neighboring ground-floor windows instead of leaving windows behind exits."
failure_gates:
  - "Early dense facade detail hides unresolved massing decisions."
  - "Segment-box roof guards create broken corners on non-orthogonal roofs."
  - "Random roof access boxes create bad floor fragments and do not prove egress."
  - "Decorative public entrance portals are a wrong answer when the issue is emergency egress from LLY."
  - "Facade elements modeled as protruding boxes read as pasted-on objects, not openings."
  - "LLY exits that ignore the ground-floor window grid look accidental."
validation: "User rejected public-entry portal approach, corrected that exits must come directly from LLY. Final lesson: four minimal exits tied to two core zones, coplanar with facade and coordinated with first-floor window grid."
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

## Rules Promoted

### Massing Before Detail

At massing stage, dense windows, mullions, storefronts, and facade panels must
stay hidden until the user accepts the large form. Coarse facade intent may be
visible only when it helps read the massing.

### Roof Guards

For operated stepped roofs:

```text
DupBorder
-> Offset x 2
-> Extrude
-> one continuous closed guard/parapet strip
```

Do not build guards as separate segment boxes on non-rectangular or stepped
roofs unless corner joining is explicitly solved.

### Core And Roof Access

For an elongated office plate around `3700 m2` and `13F`, a two-core strategy is
more plausible than one central core or one small box per terrace. Show roof
access/headhouse volumes only where a core zone actually reaches an operated
roof.

### LLY Emergency Exits

LLY exits are egress markers, not public entrance design. For two core zones,
four minimal exits are a good massing default when two directions per core are
plausible.

Each exit should use:

- a small dark recessed panel;
- thin frame/opening markers;
- a modest threshold pad/apron.

The panel and frame must lie in the local facade plane. Only the threshold pad
projects outward horizontally.

### First-Floor Grid Coordination

When facade detail is visible, LLY exits must occupy clean first-floor facade
bays. Do not leave windows behind the exit or let the exit cut across a random
module. Move, remove, or adjust neighboring ground-floor windows so the exit
becomes part of the grid.

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
