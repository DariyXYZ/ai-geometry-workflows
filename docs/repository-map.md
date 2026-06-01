# Repository Map

This file tells a new user or AI agent what to read and what to ignore.

## Read First

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Minimal agent instructions and non-negotiable rules. |
| `docs/START_HERE.md` | Main loading path for fresh chats and new computers. |
| `NEWS.md` | Chronological project memory, newest entries first. |
| `README.md` | Project overview and runnable CLI commands. |
| `docs/development-state.md` | Current technical state and next engineering steps. |

## Workflow Rules

| File | Purpose |
| --- | --- |
| `docs/reference-modeling-gates.md` | Scenario 1 gates: source authority, constructive grammar, missing views, geometry. |
| `docs/error-ledger.md` | Known failure modes and fixes. |
| `docs/context-system.md` | Where to store decisions, cases, reports, and temporary work. |
| `docs/project-data-map.md` | Where source data and related repos live. |
| `decisions/` | Dated accepted decisions. Read relevant files only. |

## External Repo Library

| File | Purpose |
| --- | --- |
| `docs/source-repos/README.md` | Index of external repositories and what they contribute. |
| `docs/source-repos/live-obj.md` | Semantic OBJ metadata, planner, patching, Grasshopper/Rhino ideas. |
| `docs/source-repos/2d-plan-to-3d.md` | Plan/image to contour extraction pattern. |
| `docs/source-repos/spellshape-three-format.md` | Expression, distribution, and `.spell` ideas. |
| `docs/source-repos/text-to-cad.md` | STEP-first build123d backend role. |
| `docs/external-repo-constructor-map.md` | Long-form external repo map. |
| `docs/development-directions-repo-fit.md` | Which repo pieces fit which product vector. |

## Runnable Code

| Path | Purpose |
| --- | --- |
| `ai_geometry_toolkit/` | Case-based CLI and orchestration code. |
| `tests/` | Unit tests and fixtures. |
| `scripts/` | Utility scripts when promoted out of experiments. |
| `TOOLKIT.md` | CLI contract and command notes. |

## Usually Do Not Read First

| Path | Why |
| --- | --- |
| `.tmp_cases/` | Local ignored experiments; useful only when the user names a specific run. |
| `ai_geometry_research.html`, `index.html` | Report/presentation outputs, not primary working memory. |
| Old team updates | Useful for history, but `NEWS.md` and `development-state.md` are faster. |

## Scenario Read Sets

### Reference To Model

Read:

- `docs/START_HERE.md`
- `docs/reference-modeling-gates.md`
- `docs/error-ledger.md`
- `decisions/2026-05-28-constructive-grammar-before-reference-modeling.md`
- `decisions/2026-06-01-grove-contour-derived-floor-plates.md`

Optional:

- `docs/source-repos/live-obj.md`
- `docs/source-repos/2d-plan-to-3d.md`

### Complex Model Cleanup

Read:

- `docs/development-state.md`
- `docs/error-ledger.md`
- `docs/context-system.md`
- `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`
- `decisions/2026-05-20-nurbs-restart-from-named-rails.md`

### Massing And Revisions

Read:

- `docs/development-state.md`
- `docs/development-directions-repo-fit.md`
- `docs/source-repos/live-obj.md`
- `docs/source-repos/spellshape-three-format.md`

## Rule For Future Agents

Prefer the smallest read set that matches the task. Do not load the whole
repository by default. If a task changes the workflow, update the matching rule
file before finishing.
