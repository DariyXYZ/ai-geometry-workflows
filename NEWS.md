# News

## 2026-05-21 - Context Rails Added

Added repo-level context normalization docs:

- `docs/context-system.md`
- `docs/project-data-map.md`
- `docs/development-state.md`
- `docs/error-ledger.md`
- `.github/ISSUE_TEMPLATE/engineering-task.yml`
- `.github/ISSUE_TEMPLATE/failure-lesson.yml`

These files define where to save project state, case data, generated runs,
errors, decisions, and personal Obsidian continuity. The goal is to make future
development reloadable from the repo instead of from mixed chat history.

## 2026-05-21 - text-to-cad Backend Linked

Added `link-backend` to register a local `earthtojake/text-to-cad` checkout on a
case. The command validates the expected CAD skill files, writes
`reports/backend_text_to_cad.md` / `.json`, and records the backend in
`case.json` and `params.json`.

The boundary is explicit: Rhino/Aurox owns `.3dm` scan, source overlays,
classification, and section extraction; `text-to-cad` owns clean STEP-first
parametric candidates after a route is accepted.

## 2026-05-21 - First Runnable Orchestration MVP

Added `ai_geometry_toolkit`, a case-based CLI for the AI Geometry Workflows repo.

Commands now available:

- `new-case`
- `validate-case`
- `route`
- `classify-scan`
- `audit-scan`
- `link-backend`

The first smoke test created a Scenario 2 cleanup case and classified an existing
Rhino scan-like report into:

```text
primary_envelope=1
podium_base=11
supports=41
large_bands=3
crown_roof=207
facade_detail=1627
noise=671
```

This is not final architectural truth. It is the first stable routing layer:
before building, the system can create a case, store parameters, classify source
objects, and write the development route.

## 2026-05-21 - Scenario 2 Direction Fixed

Moved from one-tower benchmark `22.3dm` to complex benchmark `test_data_2.3dm`.

The source includes tower, oval podium, small rounded podium, connector slab,
supports, facade ribs, bands, and crown detail.

Accepted direction:

```text
source mesh -> classify architectural parts -> reconstruct closed simplified parts -> validate by views/sections
```

Do not treat the whole model as one mesh to decimate, repair, loft, shrinkwrap,
or convert into a single watertight shell.

`test_data2_v3_clean_massing` is the current closed baseline. It is useful but
too abstract. The next iteration is `v4_refined_clean_massing` through part-aware
reconstruction and validation.

## 2026-05-20 - NURBS Restart From Named Rails

After 12 mesh simplification iterations, the mesh-primitive approach did not
produce architecturally correct results.

Active direction for complex tower reconstruction:

- extract named architectural rails;
- verify rails in front/top/side views;
- build Brep/NURBS surfaces from rails;
- avoid raw global lofting through topology changes.

## 2026-05-19 - Feature-Preserving Mesh Reconstruction Decision

Accepted research path for Scenario 2:

- CGAL Shape Detection / Efficient RANSAC;
- CGAL Polygonal Surface Reconstruction;
- CGAL Alpha Wrapping as baseline;
- quad remeshing only after solid/fidelity validation.

VSA remains diagnostic only: useful for plane families and feature edges, not a
complete solidification pipeline.

## 2026-05-18 - Workflow Kit Created

Created the first workflow kit with:

- three intake templates;
- three JSON schemas;
- `scan_scene.py`;
- `extract_sections.py`;
- `rhino_runner.py`.

Key lesson: section extraction is not section correspondence. Before lofting,
sections need stable side/corner anchors, consistent seams, and zone splits.
