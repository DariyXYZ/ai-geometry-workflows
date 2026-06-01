# AI Geometry Toolkit

`ai_geometry_toolkit` is the first orchestration layer for the three AI geometry
workflows. It does not replace Rhino/Aurox or `text-to-cad`; it coordinates
cases, parameters, routes, validation reports, and scan-derived classifications.

## Why This Exists

The previous experiments got stuck because every run mixed interpretation,
geometry generation, visual review, and repair in one long chat loop. The tool
separates those responsibilities:

- AI/Codex creates and updates case state.
- Rhino/Aurox reads or builds scene geometry.
- build123d/text-to-cad can generate source-controlled STEP geometry where that
  backend is a better fit.
- The case folder stores the reproducible state and validation evidence.

## Context Rails

Before adding new durable project data, check:

- `docs/context-system.md` - where to save context, cases, decisions, errors, and reports.
- `docs/project-data-map.md` - which local folder or external repo owns each kind of data.
- `docs/development-state.md` - current active lane and next implementation steps.
- `docs/error-ledger.md` - known failures that should shape new implementation.
- `docs/reference-modeling-gates.md` - Scenario 1 source authority, constructive grammar, and missing-view checks.
- `docs/external-repo-constructor-map.md` - quick map of reusable constructor pieces from Spellshape / Live OBJ related repositories.

## Commands

```powershell
python -m ai_geometry_toolkit new-case --scenario cleanup --name test_data_2_mvp --source test_data_2.3dm --units m
python -m ai_geometry_toolkit validate-case .\cases\<case_id>
python -m ai_geometry_toolkit route .\cases\<case_id>
python -m ai_geometry_toolkit classify-scan .\cases\<case_id> --scan path\to\scene_scan.json
python -m ai_geometry_toolkit audit-scan .\cases\<case_id> --scan path\to\scene_scan.json
python -m ai_geometry_toolkit validate-candidate .\cases\<case_id> --source-scan path\to\source_scan.json --candidate-scan path\to\candidate_scan.json
python -m ai_geometry_toolkit link-backend .\cases\<case_id> --backend text-to-cad --repo "C:\VS Code\text-to-cad"
python -m ai_geometry_toolkit import-semantic-obj .\cases\<case_id> --source path\to\model.live.obj
```

## Semantic OBJ Smoke Test

`import-semantic-obj` reads Live OBJ-style `#@` metadata and writes:

- `reports/semantic_parts.json` - machine-readable part table;
- `reports/semantic_parts.md` - CAD route hints and acceptance gate notes.
- `reports/semantic_plan.json` - decomposed part planner for the next build step;
- `reports/semantic_validation.md` - metadata/post-op validation gate.

Minimal smoke fixture:

```powershell
python -m ai_geometry_toolkit new-case --scenario reference --name "office tower semantic smoke" --root .tmp_cases --units m
python -m ai_geometry_toolkit import-semantic-obj .\.tmp_cases\<case_id> --source tests\fixtures\office_tower_semantic.live.obj
```

Optional Rhino preview when Aurox is running:

```powershell
python scripts\build_semantic_smoke_rhino.py .\.tmp_cases\<case_id>\reports\semantic_parts.json
```

This preview is a smoke artifact only. It creates massing boxes, an oval podium
loft, and facade guide curves in Rhino. It is not final CAD validation.

## Scenario 2 MVP Route

1. Create a cleanup case.
2. Run Rhino/Aurox `scan_scene.py` on the source model.
3. Put `scene_scan.json` into `reports/`.
4. Run `classify-scan`.
5. Review `source_classification.json`.
6. Extract sections per major architectural part.
7. Validate section correspondence before any loft/build.
8. Build closed simplified parts.
9. Run `validate-candidate` for first bbox/center deltas.
10. Produce section deltas and fixed captures before acceptance.

## Backend Strategy

Use Rhino/Aurox when:

- the source is `.3dm`, Rhino layers, existing scene objects, or messy meshes;
- visual validation in Rhino is part of acceptance;
- output is Brep, mesh, or closed shell set for analysis.

Use `text-to-cad` / build123d when:

- the task starts from a clean parametric description;
- source-controlled STEP generation is the main deliverable;
- deterministic CAD-as-code is more important than existing Rhino scene context.

Attach a local `text-to-cad` checkout to a case with `link-backend`. The command
validates the expected CAD skill and render viewer files, then writes:

- `reports/backend_text_to_cad.md` - human-readable backend contract;
- `reports/backend_text_to_cad.json` - machine-readable paths and role;
- `case.json` / `params.json` backend entries for reproducible follow-up runs.

For Scenario 2, keep the boundary explicit: Rhino/Aurox owns `.3dm` scan,
classification, source overlays, and section extraction; `text-to-cad` owns
clean parameter-driven STEP candidates after the route is accepted.

## Near-Term Missing Pieces

- Rhino-backed `scan_scene` integration inside this repo.
- `extract_sections` output normalization.
- Section/profile-aware `validate_candidate_vs_source` metrics beyond bbox.
- `semantic_plan.json -> build123d/Rhino candidate script` generator.
- Scenario 3 variant generator and metrics writer.
- Scenario 1 reference package template with source image/drawing authority.
