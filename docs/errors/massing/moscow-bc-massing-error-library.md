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

### `MBC-E09` Coplanar Finish Flicker

Symptom: roof finishes, green surfaces, paving strips, facade overlays, or
graphic guide surfaces visually shimmer or disappear in Rhino shaded/rendered
views even though their coordinates are correct.

Cause: a thin finish surface is exactly coplanar with the block, roof, slab, or
ground surface below it. Rhino viewport z-buffering cannot reliably decide which
surface to display.

Detection:

- two planar surfaces share the same Z level and overlap in XY;
- the issue appears as view-dependent flicker, moire, or broken patches;
- the geometry is otherwise numerically aligned.

Correction:

- Use a named micro-offset such as `VISUAL_LIFT_M = 0.001`.
- Raise visual finish surfaces at least `0.001 m` above the structural/blocking
  surface they sit on.
- Keep the lift small enough that it reads as representation, not physical
  thickness.
- Write this offset into the generator instead of manually nudging surfaces in
  Rhino.

### `MBC-E10` Presentation Materials Not Encoded In Generator

Symptom: the model looks good after manual Rhino styling, but rerunning the
generator loses the intended glass/readability setup.

Cause: important visual decisions such as transparent glass material, line
contrast, or surface lifts exist only in the active Rhino document, not in the
source-controlled script.

Detection:

- tower masses are opaque color blocks after rerun;
- facade/floor guide lines become harder to read;
- manual material edits are not represented by a material or attribute helper
  in the script.

Correction:

- Create named Rhino materials from the generator for repeated presentation
  decisions, for example translucent blue tower glass.
- Apply materials through object attributes, not only object colors.
- Treat manual presentation polish as source feedback: promote it into the
  script and case notes before the next variant.

### `MBC-E11` Zoning Stage Overbuilt Into Massing

Symptom: during Scenario 3B the user asks for preliminary zoning and proposed
footprints, but the generator jumps ahead and creates volumetric massing,
floor counts, heights, cores, or facade-like preview objects before the zoning
is approved.

Detection:

- the deliverable contains extruded buildings when the requested stage is only
  zoning / footprint proposal;
- tower cores, floor counts, roof marks, or high-rise placeholders are modeled
  before the user has accepted the footprint locations;
- the preview volumes are large enough to dominate the site and suppress the
  open-space/buffer/bлагоустройство discussion;
- a core placeholder sits on or near the facade instead of remaining an internal
  planning note;
- token/time budget is spent refining an unapproved massing option.

Correction:

- For Scenario 3B, stop at a zoning drawing unless the user explicitly approves
  moving to massing.
- Build only:
  - plot/source references;
  - public spine / entry / plaza / landscape zones;
  - service and fire access zones;
  - two-dimensional proposed building footprints;
  - dimension labels and area metrics.
- Do not create extrusions, cores, floor stacks, roof terraces, or facade
  previews until the user accepts the zoning and asks for massing.
- Keep open-space capacity visible: footprint area should not crowd out the
  primary landscape/public-room logic.
- If a tower footprint is proposed, validate that the likely core can sit inside
  the plate, but represent it as an annotation or optional 2D guide only.

### `MBC-E12` Visible Core Placeholder Reads As Facade Mass

Symptom: core placeholders are generated as visible vertical blocks that sit on
or near the facade, pop through roof terraces, or read as separate penthouses /
service towers instead of internal planning information.

Detection:

- a core block is visible from the primary review camera as a facade object;
- a core touches or nearly touches the external envelope instead of sitting
  clearly inside the office plate;
- a roof terrace or crown is dominated by exposed core geometry;
- the user reads the core as an unintended tower, chimney, or facade volume;
- the core layer remains visible in the final review view without explicit
  request.

Correction:

- At massing stage, treat cores as internal validation helpers, not presentation
  massing.
- Place core placeholders fully inside the plate with a minimum visual buffer
  from the facade; if that is impossible, report the floor plate as too tight
  instead of forcing the core onto the facade.
- Keep core geometry on a dedicated helper layer and hide it before final
  review unless the user asks to inspect planning efficiency.
- For tower plates, prefer a 2D plan guide or transparent internal marker over
  a full-height opaque core block during architectural form review.
- Do not let the core control the skyline/crown unless the design explicitly
  calls for a visible service/headhouse volume.

### `MBC-E13` Final View Polluted By Construction Layers

Symptom: after a generator finishes, the user sees source copies, datums, view
guides, core helpers, labels, old variants, or other construction geometry at
the same time as the intended final massing. The result looks messy even when
the main form is usable.

Detection:

- final viewport contains helper lines, source curves, floor datum curves, view
  rays, metric boards, core placeholders, or previous variants;
- layer names such as `source`, `guide`, `datum`, `core`, `metrics`, `debug`,
  `construction`, or old generated prefixes remain visible after the build;
- the user has to manually hide helper layers before judging the form;
- screenshots/review cameras show more explanatory scaffolding than building
  mass.

Correction:

- End every Rhino generation with a visibility cleanup pass.
- Leave visible by default only the layers needed for immediate review:
  final massing, main roof/terrace surfaces, site boundary/context if useful,
  and approved source footprints when they help compare fit.
- Hide helper layers by default: source copies, construction curves, floor
  datums, view guides, metric boards, core placeholders, debug geometry, and
  older generated variants.
- If helper evidence is important, keep it in the file but hidden, and mention
  the layer names in the report.
- If a visible label is needed for review, place it as a short horizontal
  ground annotation in the XY plane outside the main building footprint; do not
  leave vertical text boards or long metric panels in the camera view.
- After cleanup, zoom to the final visible massing layer and print visible
  generated layer names, hidden helper layer names, object count, min/max Z, and
  boundary check result.

### `MBC-E14` Unsupported Overhang Between Tower And Stylobate

Symptom: an upper tower/office volume shifts, tapers, or rotates so far that it
visibly hangs off the stylobate/base edge. The form reads as a slipping block
or accidental collision instead of a deliberate podium-tower relationship.

Detection:

- an upper volume footprint is not clearly supported by the base below;
- a tower or slab overhangs the stylobate edge without a transfer floor,
  shoulder, frame, cantilever logic, or structural explanation;
- the base and upper volume meet through a hard accidental edge, with no
  shadow joint or transition layer;
- the user reads the condition as "the block is sliding off the base";
- a tower-on-stylobate scheme lacks a readable transfer/connector volume between
  the low base and tall shaft.

Correction:

- For tower-on-stylobate massing, model a clear transition zone:
  transfer floor, recessed shoulder, bridge/connector, sky lobby, or framed
  joint between base and tower.
- Keep upper-floor offsets within a controlled support band unless the brief
  explicitly asks for a cantilever; if a cantilever is used, make it deliberate
  and limited.
- Validate each major vertical zone against the zone directly below it:
  `base footprint -> transfer/shoulder -> tower shaft -> crown`.
- Do not use taper/rotation before proving the tower remains visually and
  structurally seated on the stylobate.
- When two buildings share a stylobate or public base, add a legible connecting
  element or common terrace/deck so the pair reads as one complex, not two
  unrelated masses.

### `MBC-E15` Unreadable Annotation Placement In Review View

Symptom: the building massing is acceptable, but explanatory text is hard to
read because it is vertical, tilted toward a camera, too long, too far away, or
floating like a metric board. The user has to rotate/zoom around annotations
instead of judging the model.

Detection:

- review text is a vertical billboard, camera-facing panel, or tilted object;
- label text competes with the building form or blocks site/context geometry;
- the label contains long prose or too many metrics for one viewport;
- label layers are named as hidden/helper/metric layers but remain visible;
- text is not clearly located on the ground plane outside the main footprint.

Correction:

- Default to no visible text in final massing review unless the annotation
  materially helps the user judge the option.
- If text is needed, use a compact ground label on the XY plane, slightly above
  grade to avoid z-fighting, outside the model footprint and preferably along a
  road/site edge.
- Keep the label short: project/version, 2-3 main fixes, and only critical
  heights/metrics.
- Put visible labels on a dedicated final label layer, for example
  `*_final_ground_labels`, not on hidden metrics/helper layers.
- Hide old metric boards, debug labels, source labels, and explanatory panels
  before final review.

### `MBC-E16` Detached Connector And Competing Tower Pair

Symptom: two office volumes sit on separate stylobates, but the connector reads
as a random dark plug, coffin, puck, or bridge object placed between them. The
towers are individually smooth, yet their sloped sides/orientations do not work
together; the pair does not create one river-facing silhouette.

Detection:

- the inter-block link is a small detached object rather than part of the
  stylobate/base grammar;
- the connector is dark/heavy and visually reads as a coffin-like insert;
- rounded tower walls collide with, flare into, or awkwardly expand from the
  stylobate without a shadow reveal;
- the two tower lean/taper directions are arbitrary or visually compete;
- from elevation, the towers do not form a shared upward gesture or view-facing
  composition.

Correction:

- Put a deliberate shadow setback/reveal between rounded tower mass and massive
  stylobate. This lets the tower have a freer form without fighting the base.
- For paired stylobates, make the connector a monolithic transfer volume that
  belongs to the base system, then cut a clear passage through it.
- If the stylobate is four floors, a connector may deliberately link only two
  floors; name that as a two-story transfer/bridge condition instead of modeling
  a full-height plug.
- Aim sloped tower sides toward the key site attractor, such as the river, and
  rotate the pair so the sides visually converge upward.
- Validate the pair from elevation: the silhouette should read as one system
  with two parts, not two unrelated smooth objects.

### `MBC-E17` Facade Detail Added Before Massing Approval

Symptom: the user asks for a massing/form option, but the generator starts
building window grids, detailed mullions, balcony rails, facade panels, or
storefront details before the large form is approved. The result may look
impressive, but it spends tokens and geometry budget on detail that may need to
be thrown away.

Detection:

- dense window grids, mullions, facade panels, railings, balcony guards, or
  storefront modules are visible before the user accepts the massing;
- facade rhythm is used to make a weak large form look finished;
- the user gives feedback about silhouette, terraces, roof, setbacks, or
  overall mass while the model is already full of small facade objects;
- object count is dominated by facade/detail layers during a massing review;
- review layers do not distinguish approved massing from optional future
  facade detail.

Correction:

- During the massing approval stage, show only large form, primary terraces,
  roofscape, main voids/passages, roof access volumes, and coarse facade intent
  if needed.
- Keep dense facade grids, windows, mullions, balcony rails, and storefront
  modules hidden on a future-detail layer until the user accepts the massing.
- Do not use facade detail to compensate for unresolved stepped form, roof
  logic, tower/base relationship, or silhouette.
- If a reference image has a strong facade system, translate it first into a
  massing grammar, for example `floor-stack clipped plates`, `stepped roof
  terraces`, or `regular facade grid intent`, then wait for approval before
  adding the full window grid.

### `MBC-E18` Ragged Roof Guards And Missing Roof Access Volumes

Symptom: roof terraces appear in the massing, but their guardrails are thin,
broken, random, or placed on/through the facade. Operated roofs lack visible
LLY/stair-core exits, so the roof reads as a graphic cap rather than an
accessible terrace.

Detection:

- guardrail/parapet pieces are individual short sticks or random boxes instead
  of continuous edges;
- guard corners are assembled from separate segment boxes and create gaps,
  diagonal cuts, overlaps, or twisted corner caps;
- guards overlap facade windows, sit below the roof edge, or float away from
  the roof border;
- guards are created from segment guesses instead of from the roof border;
- accessible roofs/terraces have no stair/lift lobby exit volume;
- roof exits appear as full-height visible cores rather than small roof-access
  volumes.

Correction:

- Build roof guards from the actual roof border: `DupBorder -> Offset x 2 ->
  Extrude` or the RhinoCommon equivalent of border curve plus two controlled
  offsets creating a continuous parapet/guard strip.
- Do not approximate roof guards with independent boxes per edge unless the
  roof is strictly rectangular and corners are explicitly joined. For
  non-orthogonal or stepped roofs, the final guard/parapet must be a continuous
  closed strip made from nested closed roof-border curves.
- Put roof guards on roof/terrace layers, not facade-detail layers.
- Keep guards inside or exactly on the roof edge and validate they do not cross
  the facade plane.
- For operated roofs, add small LLY/stair-core roof access volumes during the
  massing stage. They should be visible roofscape elements, not hidden planning
  notes.
- Size roof access volumes as massing placeholders and keep them set back from
  terrace edges; do not expose a full core tower unless specifically requested.

### `MBC-E19` Random Core Or Roof Access Placement

Symptom: roof access/headhouse boxes are scattered across terraces as if every
terrace needs an independent core. The boxes sit in arbitrary positions,
consume usable roof area, create awkward office floor fragments below, or sit
too close to the facade.

Detection:

- one roof access box appears on each terrace without a clear vertical core
  strategy;
- core/headhouse boxes are placed by roof centroid only, not by office plate
  planning logic;
- a core zone creates narrow leftover office strips, blocks the best facade
  depth, or touches the facade;
- the number of cores is not justified against floor plate area, length, floor
  count, and core-to-glass depth;
- roof exits do not align with a plausible vertical circulation zone below.

Correction:

- Decide core count before placing roof access volumes. For office massing, use
  floor plate area, building length, floor count, and core-to-glass depth as
  the first-pass basis.
- Use the dimensional defaults from
  `docs/libraries/standards/moscow-building-dimensional-library-2026.md`:
  efficient office tower plates are roughly `900-1800 m2`, large low-rise /
  podium office plates are roughly `1500-3000 m2`, and office core-to-glass
  should normally stay around `12.5-14.0 m`.
- For an elongated office plate above roughly `3000 m2`, or a long stepped
  plate where one core would create poor travel distances and deep leftovers,
  consider two core zones rather than many small random roof boxes.
- Place core zones in broad internal bands, set back from the facade and terrace
  edges. A core may create one organized service/corridor zone; it must not
  leave unusable slivers around it.
- Show only the small roof access/headhouse volume at the highest roof that
  each core actually reaches. Keep larger core planning guides hidden unless
  the user asks to review plan efficiency.

### `MBC-E20` Missing Or Misread LLY Emergency Exits

Symptom: the massing has planned LLY/core zones, but the ground floor does not
show direct emergency exits from those zones. The model may instead show a
decorative public entrance, canopy, or storefront-like portal that does not
solve evacuation logic.

Detection:

- no direct ground-level exit is shown from a visible or implied LLY/core zone;
- the model uses decorative public entrance portals or storefront accents when
  the issue is emergency egress from stairs/LLY;
- exit accents are placed on arbitrary facade points instead of being aligned
  with the core/service zone behind them;
- door/opening panels, frames, or other facade elements protrude as boxes
  instead of lying in the local facade plane;
- emergency exit panels cut across the ground-floor window/module grid instead
  of occupying a clear facade bay;
- ground-floor windows remain behind or immediately collide with the LLY exit
  marker;
- one core zone has only one visible exit direction when the plan clearly needs
  paired evacuation directions;
- exits become detailed doors, signage, mullions, or shopfronts before massing
  approval.

Correction:

- For each planned LLY/core zone, place minimal ground-level emergency exits
  directly from that zone to the exterior. A useful early massing default is two
  exit directions per core when the plan allows it.
- For a two-core elongated office slab, show four minimal exits: two tied to
  the main core zone and two tied to the secondary core zone.
- Keep exits in the project's massing language: small dark recessed panels,
  thin frames, and modest threshold pads are enough. Do not create a decorative
  public portal unless the user asks for entrance hierarchy.
- Door/opening panels and frames must be coplanar with the local facade plane.
  They may have only a tiny visual thickness; do not model them as perpendicular
  attached boxes. Horizontal threshold pads/aprons may project outward.
- Coordinate LLY exits with the ground-floor facade module. The exit should
  replace or occupy one clean bay in the window/grid rhythm; adjust neighboring
  first-floor windows locally instead of letting a window sit behind the exit.
- Align exits with the core/service zone behind them. If the nearest facade
  point is not viable, move the core guide or report the plan conflict rather
  than placing a random facade accent.
- Put LLY exit geometry on a final entry/egress layer and keep any core-route
  construction guides hidden at the end.

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
