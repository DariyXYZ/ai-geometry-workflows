# Start Here

This is the entry point for reopening the project on another computer or in a
fresh AI chat.

The repository is a compact memory system for AI-assisted geometry workflows:
Rhino/Aurox modeling, reference-to-model reconstruction, CAD-as-code candidates,
semantic OBJ experiments, and analysis-geometry cleanup.

## Fast Load In 5 Minutes

Read:

1. `AI_NAVIGATOR.md` - portable entrypoint for any AI agent.
2. `NEWS.md` - newest rules and project changes.
3. `docs/library-index.md` - reusable strategy, pattern, source, and tool libraries.
4. `docs/case-library.md` - successful, partial, and failed cases.
5. `docs/scenarios/reference-modeling-gates.md` - how to think before modeling.
6. `docs/error-ledger.md` - mistakes that must not repeat.
7. `docs/obsidian-knowledge-map.md` - useful Obsidian research, tests, and errors
   not fully migrated into compact repo pages.
8. `docs/cases/recent-rhino-case-lessons.md` - recent Rhino/Aurox case results,
   video scripts, and fresh mistakes.
9. `docs/repository-map.md` - where everything lives.
10. `docs/source-repos/README.md` - compressed memory of external repositories.

If using an AI agent, point it at `AGENTS.md` first.

## Choose The Scenario

### Scenario 1 - Reference To Model

Use when the task is: build a Rhino/CAD model from text, photos, plans,
facades, elevations, dimensions, or underlays.

Read:

- `docs/scenarios/reference-modeling-gates.md`
- `docs/error-ledger.md`
- `decisions/2026-05-28-constructive-grammar-before-reference-modeling.md`
- `decisions/2026-06-01-grove-contour-derived-floor-plates.md`
- `docs/source-repos/2d-plan-to-3d.md`
- `docs/source-repos/live-obj.md`

Mandatory flow:

```text
source authority
-> constructive grammar
-> section/repetition strategy
-> missing-view check
-> geometry
-> source-derived comparison
```

Current hard lessons:

- Karlatornet: do not guess one envelope; identify repeated shafts, gaps,
  twist datums, loft sections, and mirror/repeat logic.
- Karlatornet update: if the form reads as repeated vertical shafts with
  twisting facade faces, start from primitive shafts plus vertical guide curves,
  loft the transition surface, then mirror/repeat. Do not force a horizontal
  section stack unless floor plates are proven to control the geometry.
- Grove at Grand Bay: for rotating orthogonal floor plates, derive intermediate
  floors by Rhino `Contour` from temporary lofts. Use contour curves as slab
  edges, offset glass inward, and give slabs thickness.
- Recent video/reference cases: read `docs/cases/recent-rhino-case-lessons.md` for
  the Infinity, Shanghai-style twist, Flock shell, symmetric stepped tower,
  Aqua Tower, and Absolute World lessons before modeling or replaying them.

### Scenario 2 - Complex Model To Simplified Analysis Geometry

Use when the task is: take an existing Rhino/architecture model and make clean
analysis geometry for wind comfort or related simulations.

Read:

- `docs/development-state.md`
- `docs/error-ledger.md`
- `docs/context-system.md`
- `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`
- `decisions/2026-05-20-nurbs-restart-from-named-rails.md`

Mandatory flow:

```text
scan source
-> classify architectural parts
-> reconstruct by parts/zones
-> validate with sections/views
-> handoff
```

Avoid:

- global decimation as final geometry;
- ShrinkWrap/Poisson as a trusted solution;
- one global hull/envelope;
- claiming success only because geometry is closed.

### Scenario 3 - Massing And Revisions From TEPs

Use when the task is: generate, revise, or review early massing/building
proposals from TEP, GFA/FAR, height, underlays, redlines, user edits, or city
approval checklist criteria.

Read:

- `docs/scenarios/tep-massing-scenario-subtypes.md`
- `docs/scenarios/architecture-compliance-check.md`
- `docs/libraries/massing-decision-library.md`
- `docs/libraries/form-operator-library.md`
- `docs/libraries/moscow-architecture-approval-checklist.md`
- `docs/errors/moscow-bc-massing-error-library.md`
- `docs/libraries/moscow-bc-site-zoning-patterns.md`
- `docs/development-state.md`
- `docs/research/development-directions-repo-fit.md`
- `docs/source-repos/live-obj.md`
- `docs/source-repos/spellshape-three-format.md`

Mandatory flow:

```text
scene/context
-> classify Scenario 3 subtype
-> if 3A/3B/3C: zoning / constraints / TEP / operators / variants
-> if 3D: Rhino evidence / views / checklist criteria / approval risks
-> movement/open-space/visual checks
-> optional TEP/norm checks only when requested and sourced
-> surgical revisions or compliance report
```

For Moscow BC-style sites, do not generate geometry until the public spine,
service edge, open-space type, buildable bands, height anchors, and at least one
site-reasoned architectural operator are declared.

Subscenario split:

- `3A`: zoning, footprints, and entries are already given. Keep zoning as source
  authority and work on form, height, TEP, and constraints.
- `3B`: only plot and entries/access are given. First propose zoning and
  tentative footprints, then wait for zoning approval before architecture.
- `3C`: plot plus existing massing iteration are given. Use source massing as
  TEP/gabarit anchor and improve image/form in roughly the same scale.
- `3D`: existing building/massing/proposal needs review against an architecture
  approval checklist. Inspect Rhino evidence and score criteria before
  redesigning.

## Rhino/Aurox Modeling Rules

- Work in the scene units. If drawings are in feet and Rhino is in meters,
  convert explicitly and write the conversion in the note/report.
- Do not place reference slabs, underlays, or helper mass above floor 1 unless
  they are real building geometry.
- Build massing first, detail second.
- Validate with source-derived dimensions, section datums, and screenshots.
- Preserve user-created source geometry and hidden references.
- Use `scripts/rhino_common_helper.py` for native Rhino operations that should
  not be approximated with point drawing: trim, split, boolean, intersections,
  contours, NURBS rebuild, and custom RhinoCommon C#.
- For video/replay modeling, preserve the user-selected camera unless asked,
  slow down visible construction, keep the model grounded, and remove obsolete
  helper lines before the final pass.

## External Repositories

The external repos are not vendored into this repository. Their useful ideas
are compressed into `docs/source-repos/`. Start there before opening GitHub.

Use this rule:

```text
local source card first
-> external repo only if implementation detail is missing
-> update source card after learning something durable
```

## When Updating This Repository

Every meaningful session should leave the repo better for the next fresh chat:

- follow `docs/repo-maintenance-guide.md`;
- update `NEWS.md`;
- add or update one rule in `docs/`;
- add a decision if a tradeoff became policy;
- add source-repo notes if an external repo taught us something reusable;
- keep `.tmp_cases/` disposable and out of git unless promoting a case.
