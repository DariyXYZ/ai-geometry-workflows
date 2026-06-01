# Start Here

This is the entry point for reopening the project on another computer or in a
fresh AI chat.

The repository is a compact memory system for AI-assisted geometry workflows:
Rhino/Aurox modeling, reference-to-model reconstruction, CAD-as-code candidates,
semantic OBJ experiments, and analysis-geometry cleanup.

## Fast Load In 5 Minutes

Read:

1. `NEWS.md` - newest rules and project changes.
2. `docs/reference-modeling-gates.md` - how to think before modeling.
3. `docs/error-ledger.md` - mistakes that must not repeat.
4. `docs/repository-map.md` - where everything lives.
5. `docs/source-repos/README.md` - compressed memory of external repositories.

If using an AI agent, point it at `AGENTS.md` first.

## Choose The Scenario

### Scenario 1 - Reference To Model

Use when the task is: build a Rhino/CAD model from text, photos, plans,
facades, elevations, dimensions, or underlays.

Read:

- `docs/reference-modeling-gates.md`
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
- Grove at Grand Bay: for rotating orthogonal floor plates, derive intermediate
  floors by Rhino `Contour` from temporary lofts. Use contour curves as slab
  edges, offset glass inward, and give slabs thickness.

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

Use when the task is: generate or revise early massing from TEP, GFA/FAR,
height, underlays, redlines, and user edits.

Read:

- `docs/development-state.md`
- `docs/development-directions-repo-fit.md`
- `docs/source-repos/live-obj.md`
- `docs/source-repos/spellshape-three-format.md`

Mandatory flow:

```text
scene/context
-> constraints and TEP
-> named parts and parameters
-> generated variants
-> proxy metrics
-> surgical revisions
```

## Rhino/Aurox Modeling Rules

- Work in the scene units. If drawings are in feet and Rhino is in meters,
  convert explicitly and write the conversion in the note/report.
- Do not place reference slabs, underlays, or helper mass above floor 1 unless
  they are real building geometry.
- Build massing first, detail second.
- Validate with source-derived dimensions, section datums, and screenshots.
- Preserve user-created source geometry and hidden references.

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

- update `NEWS.md`;
- add or update one rule in `docs/`;
- add a decision if a tradeoff became policy;
- add source-repo notes if an external repo taught us something reusable;
- keep `.tmp_cases/` disposable and out of git unless promoting a case.
