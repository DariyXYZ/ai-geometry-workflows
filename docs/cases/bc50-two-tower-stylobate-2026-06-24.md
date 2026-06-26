# BC50 Two-Tower Stylobate Case 2026-06-24

Status: accepted workflow precedent

Scenario: Scenario 3A/3C style massing revision with fixed stylobate and tower
footprint intent.

## AI Extraction Summary

```yaml
use_when: "high-rise business-center massing with towers on a stylobate, especially Scenario 3A/3C revisions"
source_authority: "fixed stylobate/tower intent plus source-controlled Rhino generator"
geometry_grammar: "continuous stylobate -> exploited roof/courtyard/bridge -> recessed transfer floors -> two tapered/twisted towers -> straight roof cores"
effective_rhino_gh_route: "RhinoMCP slot scan + RhinoCommon Python generator; contour/offset roof curves drive roofs and parapets"
key_parameters:
  units: meters
  towers: 2
  floors_per_tower: 50
  typical_f2f_m: 4.05
  podium_roof_m: 14.4
  tower_roof_m: 216.9
  office_plate_m2: 2200
promoted_rules:
  - "derive roof finishes and parapets from actual contours, not separate rectangles"
  - "keep roof cores/headhouses straight, not twisted with facade massing"
  - "use translucent glass massing when floor/datum guides must remain visible"
  - "use VISUAL_LIFT_M = 0.001 for thin coplanar finish surfaces"
failure_gates:
  - "fake inner roof parapet"
  - "floating courtyard green"
  - "horizontal metric text intersecting model"
  - "bridge without explicit guardrail/edge logic"
validation: "meters, object/layer audit, bbox/Z-level audit, TEP metric board, visual roof/courtyard/bridge review"
read_more_when: "building BC-style tower+podium massing, roof/parapet logic, sunken courtyard, or RhinoCommon generator baseline"
related_scripts:
  - "scripts/rhino/massing/two_tower_bc_50f_stylobate.py"
```

Source / file:

- generator: `scripts/rhino/massing/two_tower_bc_50f_stylobate.py`
- prior local Rhino output was kept under ignored `outputs/rhino/` and is not
  part of the active repo contract
- current reproducible generator baseline after presentation polish: `BC50_v7`
- branch: `codex/grasshopper-workflow`

## Goal

Build a 1:1 meter-scale business-center massing: two 50-floor office towers on
an exploited stylobate, with a recessed transfer floor above the stylobate roof
to create an overhang and shadow joint.

## What Worked

- Standard McNeel RhinoMCP plus RhinoCommon Python was enough for the full
  workflow: version/unit scan, cleanup, layer rebuild, lofted tower massing,
  contour-derived roof/parapet geometry, and numeric audits.
- The accepted massing family is `podium + tower`: a continuous stylobate,
  two dynamic tapered/twisted office shafts, recessed transfer floors, straight
  core overruns, roof equipment pads, and a sunken courtyard with a bridge.
- Tower roof parapets and stylobate roof parapets should be derived from the
  actual contour/offset curves. Do not draw separate rectangular parapets on
  top of a non-rectangular or chamfered outline.
- Roof cores should continue as straight vertical service/headhouse volumes.
  They should not twist with the facade envelope.
- A vertical metric board outside the site is a cleaner way to keep TEP and
  validation data in the scene than placing long text on the ground plane.
- A translucent blue glass material improved readability of dynamic tower
  geometry while keeping floor/datum lines visible.

## What Failed During Iteration

- Initial roof/parapet details drifted because they were drawn as separate
  rectangles instead of being driven by the roof contours.
- An inner tower roof parapet read as a fake second parapet. The roof needs an
  outer parapet plus a straight core/headhouse, not a decorative inner ring.
- Text placed in the horizontal XY plane became hard to read and visually
  intersected the model in perspective views.
- The courtyard green surface appeared to float when it was left near the
  stylobate roof plane. For this case it needed to be lowered into the sunken
  courtyard.
- The bridge looked like it cut the courtyard if no dedicated guardrails were
  modeled along both sides.
- Coplanar finish surfaces can flicker in Rhino shaded/rendered views. Finish
  layers such as roof coatings, paving, green surfaces, facade overlays, and
  thin graphic strips should be raised at least `0.001 m` above the surface
  they visually sit on.

## Promoted Rules

1. Use `VISUAL_LIFT_M = 0.001` or an equivalent named offset for thin visual
   finishes that sit on top of larger blocks.
2. Use semi-transparent material for glass tower massing when facade/floor
   guide lines need to remain visible.
3. Keep roof build-up logic contour-driven:

   ```text
   roof contour
   -> offset contour
   -> roof surface / finish
   -> parapet ring
   -> core overrun / roof access
   -> equipment pads
   ```

4. For exploited stylobate courtyards, classify each surface level:

   ```text
   stylobate roof finish
   bridge / deck
   sunken courtyard floor or green
   parapet / guardrail
   ```

5. Bridge guardrails should run along the bridge edges. Do not let a crossing
   deck visually slice through a continuous courtyard parapet without a clear
   rail/edge logic.

## Reusable Workflow

```text
RhinoMCP slot + units/version scan
-> delete old generated BC50 layers
-> build site and stylobate blockout
-> derive exploited roof, courtyard, promenade, and bridge from contours
-> build recessed transfer floors and dynamic tower lofts
-> add floor reveals and datum contours
-> add straight cores and roof overruns
-> apply transparent glass material to tower masses
-> apply 1 mm visual lift to thin finish surfaces
-> place metric board outside model
-> audit layers, bbox, object counts, and key Z levels
-> save versioned `.3dm`
```

## Validation Snapshot

- Rhino: 8.30
- Units: meters
- Towers: 2
- Floors per tower: 50
- Typical F2F: 4.05 m
- Podium roof: 14.4 m
- Tower roof: 216.9 m
- Typical office plate: 44 m x 50 m = 2200 m2
- Core placeholder: 18 m x 24 m = 432 m2, about 19.6 percent of the plate
- Latest accepted Rhino output before manual presentation polish: `BC50_v6`
- Source-controlled generator baseline after promoting polish rules: `BC50_v7`

## Links

- `docs/case-library.md`
- `docs/errors/moscow-bc-massing-error-library.md`
- `docs/libraries/moscow-building-dimensional-library-2026.md`
- `scripts/rhino/massing/two_tower_bc_50f_stylobate.py`
