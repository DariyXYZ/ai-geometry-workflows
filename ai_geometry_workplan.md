# AI Geometry Construction Workplan

This repo tracks the transition from R&D experiments to a repeatable AI-assisted
geometry workflow for architectural CAD, Rhino, Grasshopper, and CAD-as-code.

## Goal

Build a practical toolchain where:

- AI interprets inputs and proposes parameters;
- deterministic CAD/Rhino/build123d tools create geometry;
- validation gates decide whether a model can be accepted;
- successful workflows become templates, modules, or supported tools.

## Working Principle

Do not optimize for one impressive model. Optimize for repeatable cases with
stored inputs, parameters, scripts, validation, captures, and handoff notes.

Core pipeline:

```text
intake -> extract -> plan -> build -> validate -> handoff
```

## Scenario 1 - Reference To Model

Input:

- images;
- plans;
- facades/elevations;
- drawings;
- description;
- known dimensions.

MVP output:

- parameter table;
- blockout/massing model;
- top/front/side validation;
- detail only after blockout approval.

Development route:

1. Classify every source by authority: exterior plan, structural plan, facade,
   side view, perspective, diagram.
2. Extract dimensions and assumptions.
3. Build blockout only.
4. Validate plan/elevation/side proportions.
5. Add detail after approval.

Status: template/R&D. Stable enough for controlled blockout, not final
photo-to-CAD automation.

## Scenario 2 - Complex Rhino Model To Simplified Analysis Geometry

Input:

- existing Rhino scene, `.3dm`, OBJ, or scan report;
- source layers and object groups;
- downstream analysis target.

MVP output:

- classified architectural parts;
- section report;
- closed simplified parts or watertight mesh;
- bbox/section delta report;
- fixed captures.

Current benchmark: `test_data_2.3dm`.

Accepted route:

1. Scan scene including hidden and locked objects.
2. Classify source into tower, podium, low blocks, supports, large bands, facade detail, noise.
3. Extract sections per major part.
4. Validate section correspondence before loft/build.
5. Build closed simplified parts.
6. Add only analysis-relevant detail.
7. Validate source/candidate deltas and fixed captures.

Status: primary MVP. This is the first workflow to make testable as a real tool.

## Scenario 3 - Massing From TEPs And Revisions

Input:

- site boundary;
- GFA/FAR/height/floor count;
- massing rules;
- user revision requests.

MVP output:

- 5-10 variants generated in one run;
- metrics per variant;
- comparison captures;
- revision log as parameter deltas.

Development route:

1. Convert TEPs and description into `params.json`.
2. Generate all variants in one script.
3. Compute GFA/footprint/height/FAR proxy.
4. Apply revisions as parameter deltas.
5. Preserve scripts and metrics.

Status: strong candidate for a supported tool after Scenario 2 readback/validation
is stable.

## Route For This Iteration

### Step 0 - Restore State

Done. Read Obsidian project notes, decisions, research, and local repos.

Key restored decisions:

- use stage gates for reference modeling;
- do not accept `isSolid=True` without source fidelity;
- use part-aware reconstruction for complex architectural sources;
- use `text-to-cad` as CAD-as-code backend, not as Rhino replacement.

### Step 1 - Create Runnable Orchestration Layer

Done initial MVP:

- `ai_geometry_toolkit new-case`
- `validate-case`
- `route`
- `classify-scan`
- `audit-scan`

### Step 2 - Connect Rhino/Aurox Readback

Next implementation:

- normalize `scan_scene.py` output into case reports;
- copy the working scripts from `workfiles/rhino/workflow-kit` into this repo;
- add a command that runs scan through Aurox when Rhino is open;
- keep offline scan classification available for CI and review.

### Step 3 - Scenario 2 Real Test

Target: `test_data_2.3dm`.

Run:

1. create cleanup case;
2. scan source;
3. classify groups;
4. extract sections for tower/podium/low block/support groups;
5. build `v4_refined_clean_massing`;
6. validate by section deltas and fixed captures.

Acceptance:

- source object groups visible in report;
- major closed parts preserved;
- final output can be multiple closed shells;
- no global repair is accepted without source fidelity.

### Step 4 - Scenario 3 Variant Engine

Add:

- `generate-variants`;
- `variant_metrics.csv`;
- `revision_log.md`;
- sample case.

### Step 5 - Scenario 1 Controlled Reference Workflow

Add:

- source package template;
- image/drawing authority table;
- blockout-only build route;
- proportion checklist.

## Definition Of Done For MVP

The tool is testable on real tasks when a user can run:

```powershell
python -m ai_geometry_toolkit new-case --scenario cleanup --name test_data_2 --source test_data_2.3dm --units m
python -m ai_geometry_toolkit classify-scan .\cases\<case_id> --scan .\cases\<case_id>\reports\scene_scan.json
python -m ai_geometry_toolkit route .\cases\<case_id>
```

and receive:

- case folder;
- parameter table;
- classification;
- development route;
- validation report stub;
- clear next Rhino build command.

## Open Decisions

1. Whether final Scenario 2 output must be one watertight mesh or may be multiple closed Brep/shell parts.
2. Whether to package the Rhino side as scripts first or a Rhino plugin/connector.
3. Which Scenario 1 benchmark should become the first public example.
4. Who approves promotion from R&D to supported tool.
