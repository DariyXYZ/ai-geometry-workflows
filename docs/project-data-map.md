# Project Data Map

This map explains where active data lives and what each folder means. It is a
working index, not an exhaustive dump.

## Active Repository

`C:\VS Code\workfiles\ai-geometry-workflows`

| Path | Role | Status |
| --- | --- | --- |
| `ai_geometry_toolkit/` | Python CLI orchestration package | Active |
| `tests/` | Unit tests and fixtures | Active |
| `decisions/` | Accepted technical decisions | Active |
| `docs/` | Shared context system and data map | Active |
| `.tmp_cases/` | Local smoke cases | Ignored |
| `cases/` | Shareable real cases | Ignored until consciously promoted |
| `README.md` | GitHub landing page | Active |
| `TOOLKIT.md` | Runnable command reference | Active |
| `NEWS.md` | Chronological updates | Active |
| `ai_geometry_workplan.md` | Scenario roadmap | Active |
| `TEAM_UPDATE_2026-05-21.md` | Team-facing status snapshot | Active |

## External Backend

`C:\VS Code\text-to-cad`

Role: clean external checkout of `earthtojake/text-to-cad`, used as a STEP-first
CAD-as-code backend.

Important paths:

- `skills/cad/SKILL.md`
- `skills/cad/scripts/step`
- `skills/cad/scripts/inspect`
- `skills/render/scripts/viewer`

Boundary: this backend is not a mesh cleanup engine. It should generate clean
parametric candidates after source readback and section/classification gates.

## Rhino Source And Evidence

`C:\VS Code\workfiles\rhino\workflow-kit`

Role: older working Rhino workflow kit. Scripts here should be migrated or
wrapped into `ai_geometry_toolkit` instead of copied ad hoc.

Useful paths:

- `rhino_workflow_kit/scripts/scan_scene.py`
- `rhino_workflow_kit/scripts/extract_sections.py`
- `rhino_workflow_kit/scripts/fit_architectural_sections.py`
- `rhino_workflow_kit/reports/tower_bbox_classification.json`

`C:\VS Code\workfiles\rhino\cad-mesh-reconstruction`

Role: Scenario 2 attempt history and failure evidence.

Useful paths:

- `build_test_data2_clean_massing_v3.py` - closed baseline, too abstract.
- `add_test_data2_v*_*.py` - failed/diagnostic reconstruction attempts.
- `cad_mesh_reconstruction_status.json` - historical status.

Do not delete these until their lessons are captured in `docs/error-ledger.md`
or a dated decision.

## Shared Docs

`C:\VS Code\workfiles\computational-design-docs`

Role: team-facing reports and broader computational-design documentation.

Relevant files:

- `ai_geometry_research.html`
- `ai_geometry_workplan.md`
- `README.md`
- `index.html`

## Durable Personal Context

`C:\Users\dariy.n\Documents\Obsidian Vault`

Primary notes:

- `01 Dashboard/Codex Workspace Control Center.md`
- `30 Projects/Skills and Publishing/Rhino Aurox Modeling/Project - Rhino Aurox Modeling Skill.md`
- `30 Projects/Skills and Publishing/Rhino Aurox Modeling/AI Geometry Tool Iteration 2026-05-21.md`
- `40 Decisions/Decision - Feature Preserving Mesh Reconstruction Path.md`
- `40 Decisions/Decision - Rhino Reference Modeling Stage Gates.md`

Use Obsidian for branch-independent context and reload instructions. Use repo
docs for shared project truth.
