# AI Geometry Workflows

Working repository for AI-assisted CAD and architectural geometry workflows.

The project is moving from one-off "Codex to Rhino model" experiments toward a
repeatable, validation-first toolchain for real modeling tasks.

## Current Direction

Use AI for interpretation, parameter extraction, code generation, routing, and
iteration control. Use deterministic CAD/Rhino/build123d tools for geometry.
No result is accepted until it passes source-derived validation gates.

Core pipeline:

```text
intake -> extract -> plan -> build -> validate -> handoff
```

## Three Scenarios

1. **Reference to model**  
   Build a model from images, plans, elevations, drawings, descriptions, and
   known dimensions. This is the future AI-platform scenario: first build a
   stable engine locally, likely through Rhino, then translate it into the
   platform format where image-generation models and reference packages are
   already available. `text-to-cad` is a strong reference for this direction,
   but the architecture version needs more support for facades, plans,
   elevations, generated references, and source-authority gates.

2. **Complex model to simplified analysis geometry**  
   Convert detailed Rhino geometry into simplified closed shells or watertight
   analysis geometry. This is mostly an internal Rhino workflow for preparing
   architect models before wind comfort and later other analyses. The current
   rule is part-aware reconstruction, not global mesh repair.

3. **Massing and revisions from TEPs**  
   Generate massing variants from description, site constraints, TEPs, FAR/GFA,
   Rhino scene context, red lines, underlays, existing rough volumes, and user
   revisions. This is also mainly Rhino-first: automate early project massing
   changes, revise geometry from new constraints, and sometimes create a new
   massing form from a reference.

## MVP Tool

The repo now includes a first runnable orchestration layer:

```powershell
python -m ai_geometry_toolkit --help
```

Create a real case folder:

```powershell
python -m ai_geometry_toolkit new-case `
  --scenario cleanup `
  --name test_data_2_mvp `
  --source test_data_2.3dm `
  --units m `
  --downstream Ladybug
```

Validate and route the case:

```powershell
python -m ai_geometry_toolkit validate-case .\cases\<case_id>
python -m ai_geometry_toolkit route .\cases\<case_id>
```

Classify a Rhino `scan_scene` report:

```powershell
python -m ai_geometry_toolkit classify-scan .\cases\<case_id> `
  --scan "C:\VS Code\workfiles\rhino\workflow-kit\rhino_workflow_kit\reports\tower_bbox_classification.json"
```

Attach the local `text-to-cad` checkout as a STEP-first backend:

```powershell
python -m ai_geometry_toolkit link-backend .\cases\<case_id> `
  --backend text-to-cad `
  --repo "C:\VS Code\text-to-cad"
```

The output is a reproducible case folder with:

- `case.json`
- `params.json`
- `intake.md`
- `reports/development_route.md`
- `reports/source_classification.json`
- `reports/backend_text_to_cad.md`
- `reports/validation.md`

## Repository Map

- `ai_geometry_toolkit/` - runnable orchestration CLI.
- `docs/context-system.md` - rules for where project context, cases, errors, and decisions live.
- `docs/project-data-map.md` - active data/source map across this repo, Rhino workfiles, Obsidian, and `text-to-cad`.
- `docs/development-state.md` - current development status and next engineering steps.
- `docs/error-ledger.md` - known failure modes and lessons not to repeat.
- `ai_geometry_workplan.md` - project plan and development route.
- `TEAM_UPDATE_2026-05-21.md` - current team-facing status.
- `NEWS.md` - chronological project updates.
- `decisions/` - accepted technical decisions.
- `ai_geometry_research.html` - public/team report page.

## Current Status

As of 2026-05-21, Scenario 2 is the first active engineering MVP on
`test_data_2.3dm`, but the project deliberately tracks all three vectors.

Accepted direction:

```text
source geometry -> classify architectural parts -> reconstruct closed simplified parts -> validate by sections/views
```

Do not continue with global decimation, ShrinkWrap, Poisson, one global loft, or
one hull/envelope as the final method. Direct mesh reduction remains useful only
as diagnostic overlay.

## Context And Data Rules

Use `docs/context-system.md` before adding new data, ideas, errors, or generated
runs. The short version:

- shared truth goes into repo docs;
- one modeling run goes into a case folder;
- local smoke tests go into `.tmp_cases/`;
- personal cross-repo memory goes into Obsidian;
- known failures go into `docs/error-ledger.md`;
- durable decisions go into `decisions/`.
- GitHub work items should use the engineering task or failure/lesson issue templates.
