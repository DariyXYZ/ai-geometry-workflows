# Moscow River BC Two-Footprint Massing 2026-06-29

## AI Extraction Summary

```yaml
case_family: rhino-geometry
status: "medium-success / user-corrected direction"
use_when: "Scenario 3A business-center massing on user-approved footprints near a river/view edge"
source_authority: "user-created purple Rhino footprint curves + plot, river, and road context layers"
geometry_grammar: "fixed footprints -> massive shared stylobate -> shadow reveals below rounded towers -> two-story monolithic cut-through connector -> paired river-facing tower slopes -> hidden helpers"
effective_rhino_gh_route: "McNeel RhinoMCP slot aardvark + RhinoCommon Python generator"
key_parameters:
  units: meters
  wide_footprint_m2: 1944.1
  tower_footprint_m2: 1422.7
  wide_base_m: 17.55
  wide_top_m: 33.75
  tower_top_m: 90.45
  tower_crown_m: 94.95
promoted_rules:
  - "Do not show 3D core helpers in final massing review; keep cores as hidden 2D plan guides unless requested."
  - "Hide helper/source/datum/view/metric/debug layers at the end; the viewport must show the final review massing."
  - "Tower-on-stylobate needs a transfer shoulder, sky-lobby step, connector deck, or other supported transition."
  - "Use user footprints as source authority; do not replace them with generic rectangles."
  - "If a label is visible, make it a compact horizontal ground label in XY; hide vertical/long metric boards."
  - "Use shadow setbacks/reveals between rounded towers and a massive stylobate so the tower form can be freer without awkward base swelling."
  - "Do not make a detached black connector object; join stylobates with a monolithic two-story transfer volume and cut a passage through it."
  - "Rotate/aim sloped tower sides toward the river and toward each other so the pair reads as one upward silhouette system."
failure_gates:
  - "Visible core placeholders read as facade towers, penthouses, or service shafts."
  - "Upper mass slips off or hangs from the edge of the base/stylobate."
  - "Final view exposes too much helper geometry and makes the user inspect construction waste."
  - "Review labels are vertical, overly long, or remain visible on hidden metric/helper layers."
  - "A connector reads as a detached black coffin/plug instead of part of the shared stylobate."
  - "Two rounded towers have arbitrary lean/orientation and visually argue instead of forming one river-facing silhouette."
validation: "V02 user rated 4/5. Codex V03 became smoother but failed connector/tower-composition gates. User-remodeled V03 promoted the durable rules: shadow reveals, monolithic cut-through connector, and converging river-facing tower slopes."
read_more_when: "building BC massing on two fixed footprints with a lower block and a tower responding to river/view edge"
related_scripts: []
```

## Goal

Create a business-center massing on two user-approved footprints: one wider and
lower block, one more tower-like block. The architectural task was to make the
large form work toward the river with view-oriented massing, while staying at
the large-form stage rather than jumping into facade detail.

## Source Geometry

- Plot, river, and road layers existed in Rhino and were treated as context.
- Two purple user-created closed curves defined the building footprints and
  were treated as source authority.
- The wide block footprint was about `1944.1 m2`.
- The tower footprint was about `1422.7 m2`.

## What Worked In V02

- The tower and lower block were kept as distinct volumes instead of competing
  oversized blocks.
- Upper tower massing was seated on a transfer shoulder instead of hanging from
  the stylobate edge.
- The lower block used a lower base plus a stepped river-oriented upper volume,
  giving it a calmer scale next to the tower.
- A shared transfer connector deck linked the tower and wide block so the
  stylobate relationship reads as intentional.
- Core guides were kept hidden and did not appear as accidental facade masses.
- Helper/source/metric layers were hidden after generation, leaving a clean
  review state.
- After feedback, the long visible metric board was replaced with a compact
  horizontal ground label near the road/site edge.

## User-Remodeled V03 Lessons

The user remodeled the smoother V03 and promoted three stronger architectural
rules:

- Add a shadow setback/reveal between the rounded tower masses and the massive
  stylobate. This frees the tower geometry and prevents the tower from looking
  like it grows awkwardly out of a swollen base.
- Treat the link between blocks as a large monolithic transfer/stylobate piece,
  then cut a passage through it. In this case the connector works as a
  two-story bridge linking two of the four stylobate floors, not as a small
  object placed between buildings.
- Aim and rotate the sloped tower sides toward the water and toward each other.
  The two towers then visually converge upward and read as two parts of one
  building system, not as unrelated rounded objects.

## What Failed Before V02

- Earlier versions showed strange 3D core placeholders that read as towers on
  the facade.
- One sloped/upper block appeared to slip off the base edge, creating an
  unsupported overhang condition.
- Construction and guide layers remained visible, making the scene look messy
  and undermining trust in the generated result.
- The first text note was too hard to read as a long visible metric board; any
  needed label should be horizontal on the ground plane.
- In an earlier zoning attempt, modeling began before the user approved the
  zoning/footprints, which wasted tokens and broke the staged Scenario 3B
  workflow.
- Codex V03 used a connector that read as a dark coffin-like object between
  blocks instead of a monolithic stylobate connection with a cut-through.
- Codex V03 made the towers smoother, but their orientation and base transitions
  still did not create a coherent upward pair/silhouette.

## Promoted Rules

1. Scenario 3A starts from user-approved footprints. Preserve them unless the
   user explicitly asks for a zoning revision.
2. Large form comes before facade detail, but the massing must still have an
   architectural relationship to context: river frontage, view terraces, tower
   emphasis, and open-space logic.
3. Tower-on-stylobate transitions must be supported by an explicit architectural
   element: transfer shoulder, recessed sky-lobby band, bridge/deck, or clear
   shadow joint.
4. Cores can guide planning, but visible 3D core placeholders are not final
   massing unless the user asks to expose service volumes.
5. After generation, hide helper/source/debug layers and show only final review
   geometry plus necessary context.
6. If a visible text note is needed, make it a compact horizontal label on the
   ground plane outside the main footprint; avoid vertical boards and long
   metric paragraphs in the review camera.
7. For rounded towers on a massive stylobate, create a deliberate shadow
   reveal/recess between tower and base. Do not let the tower wall flare or
   collide directly into the stylobate edge.
8. A bridge between two blocks should be part of the stylobate grammar:
   monolithic enough to connect floors, but cut-through enough to preserve a
   passable ground-level opening.
9. Paired towers must share an orientation logic. In this river case, their
   sloped sides should face the water and visually converge upward.

## Reusable Workflow

```text
classify as Scenario 3A
-> read plot, river, road, and approved footprint curves
-> measure footprint areas and bbox proportions
-> choose base / transfer / tower / lower-block heights from dimensional library
-> generate base/stylobate masses inside source footprints
-> add recessed transfer shoulders so upper volumes are visibly supported
-> add shadow reveals between rounded tower masses and massive stylobate
-> join the two bases with a monolithic two-story connector, then cut a passage
-> orient tower taper, decks, and terraces toward river/view edge
-> rotate/aim sloped tower sides so the pair forms one upward river-facing silhouette
-> keep core guides hidden or 2D-only
-> hide helper layers and leave final review layers visible
-> replace visible metric boards with compact horizontal ground labels if needed
-> validate minZ, maxZ, object count, and plot containment
```

## Validation Snapshot

- User rating: `4/5`; accepted as a useful direction, not a final architectural
  solution.
- Generated non-text object count: `13`.
- Height range: `0.0 m` to `94.95 m`.
- Plot containment check: passed for generated visible volume vertices.
- Old generated layers were hidden before review.
- Old long metric text was hidden; visible text was moved to
  `AI_BC_RIVER_FORM_V02::04_final_ground_labels` as a horizontal XY ground
  label.
- User-remodeled V03 corrected the connector and tower orientation: shadow
  reveals separate rounded towers from the stylobate, the inter-block connection
  is a monolithic two-story cut-through, and the tower slopes visually converge
  toward the river/upward silhouette.

## Links

- Error rules: `docs/errors/massing/moscow-bc-massing-error-library.md`
- Scenario routing: `docs/workflows/massing/tep-massing-scenario-subtypes.md`
- Dimensional defaults: `docs/libraries/standards/moscow-building-dimensional-library-2026.md`
