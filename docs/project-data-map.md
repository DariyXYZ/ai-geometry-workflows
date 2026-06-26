# Project Data Map

This map explains where active data, source memory, external repos, and
historical artifacts live. It is an index, not a full dump of the project.

## Active Repository

Root:

```text
C:\VS Code\ai-geometry-workflows
```

| Path | Role | Status |
| --- | --- | --- |
| `AI_NAVIGATOR.md` | Portable first page for AI agents | Active |
| `AGENTS.md` | Compact agent instructions | Active |
| `README.md` | Human-facing overview | Active |
| `NEWS.md` | Chronological project change log | Active |
| `TOOLKIT.md` | Runnable command reference | Active |
| `ai_geometry_toolkit/` | Python CLI orchestration package | Active |
| `tests/` | Unit tests and fixtures | Active |
| `scripts/rhino_common_helper.py` | Optional backend-specific RhinoCommon helper; current implementation uses Aurox `execute_csharp` | Active |
| `scripts/moscow_bc_massing/` | Current Moscow BC massing scripts and candidate data | Active project folder |
| `decisions/` | Accepted dated technical decisions | Active |
| `docs/` | Shared knowledge library | Active |
| `archive/` | Old reports and one-off experiments | Historical |
| `.tmp_cases/` | Local smoke cases | Ignored |
| `cases/` | Shareable real cases when consciously promoted | Ignored by default |

## Active Docs Structure

| Path | Role |
| --- | --- |
| `docs/START_HERE.md` | Scenario read sets |
| `docs/task-read-maps.md` | Concrete task-to-read-set router |
| `docs/repository-map.md` | Repo structure |
| `docs/library-index.md` | Strategy, pattern, source, and tool index |
| `docs/case-library.md` | Reusable case memory |
| `docs/error-ledger.md` | Cross-scenario failure modes |
| `docs/experience-capture-format.md` | Standard format for promoting case experience |
| `docs/obsidian-knowledge-map.md` | Obsidian research and import backlog |
| `docs/scenarios/` | Workflow gates and scenario-specific strategy |
| `docs/libraries/` | Architectural and massing pattern libraries |
| `docs/cases/` | Detailed case lessons and handoffs |
| `docs/errors/` | Domain-specific anti-pattern libraries |
| `docs/tools/` | Tool/backend notes |
| `docs/research/` | Compressed research and direction synthesis |
| `docs/source-repos/` | External repository cards |

## External Backend: text-to-cad

```text
C:\VS Code\text-to-cad
```

Role: clean external checkout of `earthtojake/text-to-cad`, used as a
STEP-first CAD-as-code backend and reference implementation.

Important paths:

- `skills/cad/SKILL.md`
- `skills/cad/scripts/step`
- `skills/cad/scripts/inspect`
- `skills/render/scripts/viewer`

Boundary:

- For Scenario 1, use it as a reference for text/reference-to-CAD mechanics,
  then extend it with source-authority gates and architectural grammar.
- For Scenario 2, use it only after RhinoMCP has produced validated
  parameters or sections for a clean candidate.
- For Scenario 3, use it only where clean parametric massing candidates are
  useful; Rhino remains the active scene context.

It is not a direct mesh cleanup engine.

## External Research: Spellshape / Live OBJ

Primary sources:

- https://spellshape.com/
- https://github.com/StepanKukharskiy/live-obj

Related sources:

- https://github.com/StepanKukharskiy/spellshape
- https://github.com/StepanKukharskiy/spellshape-format
- https://github.com/StepanKukharskiy/spellshape-webapp
- https://github.com/StepanKukharskiy/spellshape-three
- https://github.com/StepanKukharskiy/spellshape-agent
- https://github.com/StepanKukharskiy/2DPlanTo3D

Role: source for the `semantic_obj` / Live OBJ direction. It should inform the
intermediate representation, not become a hard dependency.

Repo summaries:

- `docs/research/spellshape-live-obj-direction.md`
- `docs/research/external-repo-constructor-map.md`
- `docs/research/development-directions-repo-fit.md`
- `docs/source-repos/`

## Rhino Source And Evidence

```text
C:\VS Code\workfiles\rhino\workflow-kit
```

Role: older Rhino workflow kit. Scripts here should be migrated or wrapped into
`ai_geometry_toolkit` instead of copied ad hoc.

Useful paths:

- `rhino_workflow_kit/scripts/scan_scene.py`
- `rhino_workflow_kit/scripts/extract_sections.py`
- `rhino_workflow_kit/scripts/fit_architectural_sections.py`
- `rhino_workflow_kit/reports/tower_bbox_classification.json`

```text
C:\VS Code\workfiles\rhino\cad-mesh-reconstruction
```

Role: Scenario 2 attempt history and failure evidence.

Useful paths:

- `build_test_data2_clean_massing_v3.py`
- `add_test_data2_v*_*.py`
- `cad_mesh_reconstruction_status.json`

Do not delete these until their lessons are captured in repo docs or dated
decisions.

## Obsidian Vault

```text
C:\Users\dariy.n\Documents\Obsidian Vault
```

Use Obsidian for branch-independent context and raw research memory. Use repo
docs for portable operating memory.

Start with:

- `docs/obsidian-knowledge-map.md`

## Archive

| Path | Role |
| --- | --- |
| `archive/reports/` | Old public/team reports and roadmap snapshots |
| `archive/rhino-experiments-2026-06/` | One-off Rhino scripts and generated PNG/JSON outputs |

Archive files are not part of the normal AI read path. Promote useful lessons
into `docs/`, `decisions/`, or `NEWS.md`.
