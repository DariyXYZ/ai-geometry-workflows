# Repository Map

This file tells a new user or AI agent what to read and what to ignore.

## Read First

| File | Purpose |
| --- | --- |
| `AI_NAVIGATOR.md` | Portable first page for any AI agent using this repo as architecture/geometry memory. |
| `AGENTS.md` | Minimal agent instructions and non-negotiable rules. |
| `docs/START_HERE.md` | Main loading path for fresh chats and new computers. |
| `NEWS.md` | Chronological project memory, newest entries first. |
| `README.md` | Project overview and runnable CLI commands. |
| `docs/development-state.md` | Current technical state and next engineering steps. |

## Workflow Rules

| File | Purpose |
| --- | --- |
| `docs/scenarios/reference-modeling-gates.md` | Scenario 1 gates: source authority, constructive grammar, missing views, geometry. |
| `docs/library-index.md` | Index of strategy, pattern, source-repo, tool, and data libraries. |
| `docs/case-library.md` | Index of successful, partial, failed, source-correction, and tooling cases. |
| `docs/obsidian-knowledge-map.md` | Map of useful Obsidian research, tests, errors, decisions, and import backlog. |
| `docs/error-ledger.md` | Known failure modes and fixes. |
| `docs/scenarios/tep-massing-scenario-subtypes.md` | Scenario 3 split into 3A fixed zoning, 3B plot-plus-entries zoning proposal, 3C existing-massing image/form revision, and 3D checklist review. |
| `docs/scenarios/architecture-compliance-check.md` | Scenario 3D workflow for Rhino evidence collection and architecture approval checklist review. |
| `docs/libraries/massing-decision-library.md` | Scenario 3 massing decision order, footprint families, massing families, risk checks, and generator output schema. |
| `docs/libraries/form-operator-library.md` | Reusable form operators for early massing: chamfer, rotation, rounding, setbacks, voids, taper, podium/tower logic. |
| `docs/libraries/moscow-architecture-approval-checklist.md` | Compact checklist criteria from the 2026-06-13 DGP architecture evaluation PDF. |
| `docs/errors/moscow-bc-massing-error-library.md` | Moscow BC massing failure modes: site fail despite numeric pass, cut routes, box-only variants, accidental intersections. |
| `docs/libraries/moscow-bc-site-zoning-patterns.md` | Zoning patterns and pre-geometry gates for BC/residential massing: public spine, service edge, buildable bands, height anchors. |
| `docs/cases/recent-rhino-case-lessons.md` | Recent Rhino/Aurox case results, video replay scripts, and fresh modeling rules. |
| `docs/context-system.md` | Where to store decisions, cases, reports, and temporary work. |
| `docs/repo-maintenance-guide.md` | How to add reusable strategies, patterns, cases, errors, and source findings without clutter. |
| `docs/project-data-map.md` | Where source data and related repos live. |
| `docs/tools/rhino-common-helper.md` | Native RhinoCommon helper layer through Aurox `execute_csharp`. |
| `decisions/` | Dated accepted decisions. Read relevant files only. |

## External Repo Library

| File | Purpose |
| --- | --- |
| `docs/source-repos/README.md` | Index of external repositories and what they contribute. |
| `docs/source-repos/live-obj.md` | Semantic OBJ metadata, planner, patching, Grasshopper/Rhino ideas. |
| `docs/source-repos/2d-plan-to-3d.md` | Plan/image to contour extraction pattern. |
| `docs/source-repos/spellshape-three-format.md` | Expression, distribution, and `.spell` ideas. |
| `docs/source-repos/text-to-cad.md` | STEP-first build123d backend role. |
| `docs/research/external-repo-constructor-map.md` | Long-form external repo map. |
| `docs/research/development-directions-repo-fit.md` | Which repo pieces fit which product vector. |

## Runnable Code

| Path | Purpose |
| --- | --- |
| `ai_geometry_toolkit/` | Case-based CLI and orchestration code. |
| `tests/` | Unit tests and fixtures. |
| `scripts/` | Utility scripts when promoted out of experiments, including RhinoCommon helpers. |
| `TOOLKIT.md` | CLI contract and command notes. |

## Usually Do Not Read First

| Path | Why |
| --- | --- |
| `.tmp_cases/` | Local ignored experiments; useful only when the user names a specific run. |
| `archive/reports/ai-geometry-research.html`, `archive/reports/index.html` | Report/presentation outputs, not primary working memory. |
| Old team updates | Useful for history, but `NEWS.md` and `development-state.md` are faster. |

## Scenario Read Sets

### Reference To Model

Read:

- `docs/START_HERE.md`
- `docs/scenarios/reference-modeling-gates.md`
- `docs/error-ledger.md`
- `docs/cases/recent-rhino-case-lessons.md`
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

- `docs/scenarios/tep-massing-scenario-subtypes.md`
- `docs/scenarios/architecture-compliance-check.md`
- `docs/libraries/moscow-architecture-approval-checklist.md`
- `docs/errors/moscow-bc-massing-error-library.md`
- `docs/libraries/moscow-bc-site-zoning-patterns.md`
- `docs/development-state.md`
- `docs/research/development-directions-repo-fit.md`
- `docs/source-repos/live-obj.md`
- `docs/source-repos/spellshape-three-format.md`

## Rule For Future Agents

Prefer the smallest read set that matches the task. Do not load the whole
repository by default. If a task changes the workflow, update the matching rule
file before finishing.
