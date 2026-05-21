# Development State

Updated: 2026-05-21

## Current Status

The project has moved from loose Rhino reconstruction experiments into a
case-based orchestration tool.

Active repo:

```text
C:\VS Code\workfiles\ai-geometry-workflows
https://github.com/DariyXYZ/ai-geometry-workflows
```

Current base commit:

```text
99d1999 Add AI geometry workflow toolkit MVP
```

Current uncommitted work:

- `link-backend` command for registering a local `text-to-cad` checkout.
- Repo docs for context normalization and data maps.

## Active MVP

Scenario 2 is the active MVP:

```text
complex Rhino source -> classified architectural parts -> reconstructed closed simplified parts -> section/view validation
```

Benchmark:

```text
test_data_2.3dm
```

Accepted baseline:

```text
test_data2_v3_clean_massing
```

Baseline is closed and useful, but too abstract. Next candidate is
`v4_refined_clean_massing`, built as a reproducible case rather than a loose
Rhino script.

## Implemented

CLI:

- `new-case`
- `validate-case`
- `route`
- `classify-scan`
- `audit-scan`
- `link-backend`

Case artifacts:

- `case.json`
- `params.json`
- `intake.md`
- `reports/development_route.md`
- `reports/source_classification.json`
- `reports/scan_audit.md`
- `reports/backend_text_to_cad.md`
- `reports/validation.md`

Validation:

```powershell
python -m unittest discover -s tests
```

Last result: 3 tests passed.

## Next Engineering Steps

1. Commit the context-system and `link-backend` work.
2. Migrate Rhino `scan_scene.py` into this repo.
3. Migrate or wrap `extract_sections.py` into this repo.
4. Normalize section output into `reports/sections.json` and `reports/sections.csv`.
5. Add `validate_candidate_vs_source`.
6. Build `v4_refined_clean_massing` as a real case.
7. Add GitHub issues or project tracking only after these steps are stable enough to be assigned.

## Not Active Right Now

- Scenario 1 final reference-to-CAD automation.
- Scenario 3 massing variant engine.
- Direct global mesh repair.
- Packaging as Rhino plugin.
- Public examples.

These remain planned directions, not the current implementation lane.
