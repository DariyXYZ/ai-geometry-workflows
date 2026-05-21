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
   known dimensions. The first accepted output is blockout/massing; detail comes
   only after top/front/side proportion gates pass.

2. **Complex model to simplified analysis geometry**  
   Convert detailed Rhino geometry into simplified closed shells or watertight
   analysis geometry. The current rule is part-aware reconstruction, not global
   mesh repair.

3. **Massing and revisions from TEPs**  
   Generate massing variants from description, site constraints, TEPs, FAR/GFA,
   and user revisions. Revisions are parameter deltas, not manual geometry drift.

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

The output is a reproducible case folder with:

- `case.json`
- `params.json`
- `intake.md`
- `reports/development_route.md`
- `reports/source_classification.json`
- `reports/validation.md`

## Repository Map

- `ai_geometry_toolkit/` - runnable orchestration CLI.
- `ai_geometry_workplan.md` - project plan and development route.
- `TEAM_UPDATE_2026-05-21.md` - current team-facing status.
- `NEWS.md` - chronological project updates.
- `decisions/` - accepted technical decisions.
- `ai_geometry_research.html` - public/team report page.

## Current Status

As of 2026-05-21, the priority is Scenario 2 on `test_data_2.3dm`.

Accepted direction:

```text
source geometry -> classify architectural parts -> reconstruct closed simplified parts -> validate by sections/views
```

Do not continue with global decimation, ShrinkWrap, Poisson, one global loft, or
one hull/envelope as the final method. Direct mesh reduction remains useful only
as diagnostic overlay.
