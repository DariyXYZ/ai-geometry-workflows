# AI Geometry Construction Workplan

Этот repo фиксирует переход от R&D экспериментов к повторяемому AI-assisted
geometry workflow для architectural CAD, Rhino, Grasshopper и CAD-as-code.

## Goal

Собрать практический toolchain, где:

- AI interprets inputs and proposes parameters;
- semantic sketch layer сохраняет parts/anchors/controls до CAD;
- deterministic CAD/Rhino/build123d tools create geometry;
- validation gates decide whether a model can be accepted;
- successful workflows become templates, modules, or supported tools.

## Working Principle

Не оптимизировать под одну впечатляющую модель. Оптимизировать под repeatable
cases со сохраненными inputs, parameters, scripts, validation, captures и
handoff notes.

Core pipeline:

```text
intake -> extract -> plan -> build -> validate -> handoff
```

## Scenario 1 - Reference To Model

Product direction:

This scenario is intended for integration into the broader AI platform. The
platform already has multiple image-generation models available, so the goal is
to build a reliable local engine first, likely through Rhino, and later translate
that engine into the platform format.

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

`text-to-cad` relationship:

`text-to-cad` is a useful reference for this direction, but the architecture
engine needs additions from our Rhino/Aurox lessons: source authority, facades,
plans, elevations, generated references, architectural stage gates, and richer
model assembly rules.

Status: platform-facing direction. Build and stabilize the engine locally first;
platform integration comes later.

Spellshape / Live OBJ relationship:

Spellshape is not a replacement for `text-to-cad`. It is a useful source for an
upstream semantic sketch format:

```text
reference / prompt
-> Live OBJ-like semantic parts
-> normalized part table
-> build123d / Rhino script
-> STEP / 3DM validation
```

See `docs/research/spellshape-live-obj-direction.md`.

## Scenario 2 - Complex Rhino Model To Simplified Analysis Geometry

Product direction:

This scenario is mostly for internal Rhino-based production work. The immediate
use case is preparing architect models for wind comfort analysis, then later
other analysis workflows.

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

Status: first active engineering MVP. Keep it Rhino-first unless a later
connector/plugin boundary is justified.

## Scenario 3 - Massing From TEPs And Revisions

Product direction:

This scenario is also mainly Rhino-first. Typical input is an existing scene
with context, red lines, an underlay, a rough/black massing option, or some
partial project geometry. The tool should revise or regenerate massing from new
TEPs, constraints, and user requests. It can overlap with Scenario 1 when a
reference image drives a new massing form, but the operating context is the
active Rhino scene.

Input:

- site boundary;
- Rhino scene context;
- red lines / constraints;
- underlay or reference geometry;
- existing rough massing or black option;
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

Status: Rhino-first production direction. Strong candidate for a supported tool
after readback, validation, and parameter-delta workflows are stable.

Semantic OBJ note:

Scenario 3 can use a Live OBJ-like layer for rough massing variants before they
become strict Rhino/build123d candidates. The useful artifact is not a final OBJ
mesh, but extracted named parts, bbox, anchors, params and controls.

## Route For This Iteration

### Step 0 - Restore State

Done. Read Obsidian project notes, decisions, research, and local repos.

Key restored decisions:

- use stage gates for reference modeling;
- do not accept `isSolid=True` without source fidelity;
- use part-aware reconstruction for complex architectural sources;
- use `text-to-cad` as CAD-as-code backend, not as Rhino replacement.

Context rails added:

- `docs/context-system.md`
- `docs/project-data-map.md`
- `docs/development-state.md`
- `docs/error-ledger.md`

### Step 1 - Create Runnable Orchestration Layer

Done initial MVP:

- `ai_geometry_toolkit new-case`
- `validate-case`
- `route`
- `classify-scan`
- `audit-scan`
- `link-backend`

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

### Step 6 - Semantic OBJ / Live OBJ Import

New research route:

- use `StepanKukharskiy/live-obj` as source reference;
- parse OBJ objects and `#@` metadata;
- write `reports/semantic_parts.json`;
- convert semantic parts into Rhino/build123d candidate scripts;
- keep STEP/3DM validation as the acceptance gate.

This is intentionally upstream of CAD. It should improve planning and control
extraction without replacing the CAD backend.

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
5. Whether `semantic_obj` should be a small importer command or a formal case backend type.
