# External Repo Constructor Map

Дата: 2026-05-28  
Назначение: быстрый индекс внешних репозиториев StepanKukharskiy, чтобы не
перечитывать их заново в поиске полезных элементов для нашего geometry pipeline.

## Primary Source Set

Профиль:

- https://github.com/StepanKukharskiy?tab=repositories

Локальный research checkout:

```text
C:\Users\dariy.n\AppData\Local\Temp\spellshape-research
```

Ключевые repos:

- https://github.com/StepanKukharskiy/live-obj
- https://github.com/StepanKukharskiy/2DPlanTo3D
- https://github.com/StepanKukharskiy/spellshape-three
- https://github.com/StepanKukharskiy/spellshape-format
- https://github.com/StepanKukharskiy/spellshape-webapp
- https://github.com/StepanKukharskiy/spellshape-agent

## What To Reuse Now

### 1. Live OBJ semantic metadata

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local files:

```text
live-obj/README.md
live-obj/AGENTS.md
live-obj/src/lib/server/llm/liveObjSystemPrompt.ts
live-obj/src/lib/server/llm/liveObjChat.ts
live-obj/project_live_obj_files/*.live.obj
live-obj/project_live_obj_files/*.raw.obj
```

Reusable ideas:

- `#@params` for dimensions and design variables.
- `#@controls` for editable UI knobs.
- `#@bbox` for expected part extents.
- `#@anchor` for connection points.
- `#@constraint` for soft relationships.
- `#@lock` for preserving footprint, position, silhouette, material, etc.
- `#@hidden: true` for guide paths, construction curves, cutters, and non-final helper objects.
- `#@source` values: `procedural`, `llm_mesh`, `assembly`, `sdf`, `simulation`, `recipe`.

How it fits us:

```text
semantic_obj importer
-> reports/semantic_parts.json
-> build123d/Rhino candidate script
-> validation
```

Already partly integrated:

- `import-semantic-obj` command.
- `tests/fixtures/office_tower_semantic.live.obj`.
- `reports/semantic_validation.md` with allowed `#@` metadata and post-op checks.
- `reports/semantic_plan.json` with decomposed part build plan.

### 2. Decomposed generation planner

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local files:

```text
live-obj/grasshopper_decomposed_builder_ghpython.py
live-obj/src/lib/server/llm/liveObjChat.ts
live-obj/src/lib/server/liveObj/iterative.ts
live-obj/src/lib/server/liveObj/iterative.spec.ts
```

Reusable idea:

```text
do not generate the whole building at once
first create a part plan
then generate/build one semantic part at a time
```

Planner output shape worth copying:

```json
{
  "scene": "short scene description",
  "units": "meters",
  "up": "y",
  "materials": [],
  "parts": [
    {
      "id": "stable_part_id",
      "role": "what this part contributes",
      "method": "llm_mesh",
      "dependencies": ["prior_part_id"],
      "prompt": "specific instructions for only this part",
      "controls": [],
      "controlPostOps": [],
      "validationHints": []
    }
  ],
  "notes": []
}
```

Adaption for us:

- Replace `method=llm_mesh` with our supported build modes:
  `semantic_obj`, `rhino_preview`, `build123d_step`, `guide_only`.
- Keep `dependencies`, `controls`, and `validationHints`.

### 3. Raw post operations and validation

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local files:

```text
live-obj/src/lib/liveObj/rawPostValidation.ts
live-obj/src/routes/api/executor/raw_obj_post_executor.py
live-obj/test_raw_obj_post_executor.py
```

Supported post ops:

- `transform`
- `symmetrize`
- `mirror`
- `array`
- `deform`
- `subdivide`
- `smooth`
- `simplify`
- `snap_to_ground`
- `center_origin`
- `material`
- `tag`

Reusable idea:

Keep a small, explicit operation vocabulary. Validate unknown operations before
any geometry build.

Adaption for us:

- Add a `semantic_obj` validation gate for allowed metadata keys and operations.
- Prevent invented operations from silently entering build scripts.

### 4. Rhino / Grasshopper Live OBJ renderer

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local files:

```text
live-obj/grasshopper_live_obj_render_ghpython.py
live-obj/grasshopper_live_obj_render_csharp_node.cs
live-obj/grasshopper_canvas_panels.md
live-obj/static/downloads/spellshape-grasshopper.gh
```

Reusable ideas:

- Local-only render path: no network, no telemetry.
- Read OBJ + `#@params` + `#@controls`.
- Apply `#@post` operations.
- Convert Y-up source scenes to Rhino Z-up.
- Auto-create controls in Grasshopper.

Adaption for us:

- Our current `scripts/build_semantic_smoke_rhino.py` is a smaller repo-native
  version.
- Later, port useful renderer pieces into `ai_geometry_toolkit` only when needed.

### 5. Live OBJ executor with CadQuery hooks

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local files:

```text
live-obj/src/routes/api/executor/live_obj_executor_v02.py
live-obj/src/routes/api/executor/live_obj_executor_ghpython.py
live-obj/src/routes/api/executor/live_obj_executor_blender.py
live-obj/src/lib/server/liveObj/pipeline.ts
```

Capabilities:

- Parses Live OBJ metadata.
- Expands procedural objects.
- Handles simple SDF / simulation / assembly concepts.
- Has optional CadQuery paths for primitives, profile ops, booleans, bevel/chamfer/shell.

Important limit:

This executor mostly emits tessellated OBJ/cache. It is not our final STEP-first
CAD backend.

Adaption for us:

- Use parser/execution vocabulary as reference.
- Keep final B-rep/STEP generation in `text-to-cad` / build123d.

### 6. Surgical patching

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local files:

```text
live-obj/src/lib/server/liveObj/surgicalPatch.ts
live-obj/src/lib/server/liveObj/surgicalPatch.spec.ts
live-obj/src/lib/server/llm/liveObjChat.ts
```

Reusable idea:

For iterative model edits, ask LLM for exact text patches:

```json
{
  "summary": "short edit summary",
  "edits": [
    {
      "find": "exact unique source text",
      "replace": "replacement text"
    }
  ]
}
```

Benefits:

- Preserve unrelated source exactly.
- Avoid full scene rewrite.
- Require `find` to match exactly once.

Adaption for us:

- Use for `semantic_parts.json`, `.live.obj`, and future build scripts when
  applying small parameter/metadata edits.

### 7. Prompt / generation budget rules

Repo:

- https://github.com/StepanKukharskiy/live-obj

Useful local file:

```text
live-obj/src/lib/server/llm/liveObjChat.ts
```

Rules worth copying:

- Start from simplified modular 3D interpretation, not pixel-by-pixel reconstruction.
- Keep first pass compact.
- Use arrays/modules for repeated windows, rooms, panels, columns, floors.
- Capture massing, proportions, colors, material families and distinctive motifs first.
- Avoid dense per-window/per-brick/per-cell geometry unless explicitly requested.
- Patch only named object blocks when editing, not whole scenes.
- Use hidden construction curves/paths/cutters rather than rendering everything.

Adaption for us:

- Add these as prompts/rules for Scenario 1 and Scenario 3.
- Treat facade grids as guides until massing passes validation.

### 8. 2D plan to contours

Repo:

- https://github.com/StepanKukharskiy/2DPlanTo3D

Useful local files:

```text
2DPlanTo3D/src/lib/contour-tracer.js
2DPlanTo3D/src/routes/+page.svelte
2DPlanTo3D/src/routes/images/+server.js
2DPlanTo3D/src/lib/components/Canvas3D.svelte
```

Useful pipeline:

```text
image
-> canvas
-> binary threshold
-> Moore contour tracing
-> RDP simplification
-> normalized profile polygons
```

Adaption for us:

- Create a Python/OpenCV equivalent for plan/elevation footprint extraction.
- Output footprint polygons for Scenario 1.
- Use only after source authority is known: plan vs facade vs load diagram vs core marker.

### 9. `.spell` expression and distribution system

Repo:

- https://github.com/StepanKukharskiy/spellshape-three
- https://github.com/StepanKukharskiy/spellshape-format

Useful local files:

```text
spellshape-three/src/modules/interpreter/evaluator.js
spellshape-three/src/modules/plugins/distribution.js
spellshape-three/src/modules/interpreter/processor.js
spellshape-three/src/modules/interpreter/validator.js
spellshape-three/src/modules/interpreter/helpers2d.js
spellshape-three/src/modules/interpreter/helpers3d.js
spellshape-three/src/modules/interpreter/helpers3d_extended.js
spellshape-three/src/modules/interpreter/helpers3d_core.js
spellshape-format/README.md
```

Reusable ideas:

- Small expression language for params.
- `$parameter` references.
- `sin`, `cos`, `clamp`, `lerp`, etc.
- Linear/grid/radial distribution.
- Repeating floors, panels, modules.
- Twist/taper/deform helpers.

Adaption for us:

- Add a safe expression evaluator only if needed.
- Start with very small expressions:
  `floors * floor_height`, `width / 2`, `podium_height + tower_height`.
- Do not import the whole web runtime.

## Repo-by-Repo Usefulness

Scenario-specific fit is tracked separately in `docs/research/development-directions-repo-fit.md`.

| Repo | Usefulness | Why |
| --- | --- | --- |
| `live-obj` | High | Main source for semantic metadata, planning, executors, GH renderer, patching rules |
| `2DPlanTo3D` | Medium | Good contour extraction idea for plans/footprints |
| `spellshape-three` | Medium | Good expression/distribution/interpreter reference |
| `spellshape-format` | Medium | Useful format rationale, less current than Live OBJ |
| `spellshape-webapp` | Low/Medium | UI/editor reference; likely not needed directly |
| `spellshape-agent` | Low | API SDK pattern, not useful without depending on external API |
| `procedural_city` | Low | Interesting procedural city/art reference, not immediately relevant |
| `me`, `archweekend`, `weekend-arch`, `diffusion-workflow`, `together-api`, `fastapi`, `ml-api` | Low | General experiments / app shells, not geometry core for our pipeline |

## Immediate Integration Backlog

1. `semantic_obj` validation:
   - allowed `#@` keys;
   - allowed `#@post` ops;
   - missing bbox/params warnings;
   - guide-only vs solid-candidate separation.
   - Status: integrated in `import-semantic-obj`.
2. `semantic_parts.json -> candidate script`:
   - generate Rhino Python preview script;
   - generate build123d STEP script for simple extrude/box/oval cases.
3. Planner schema:
   - copy decomposed planner shape;
   - adapt `method` values to our pipeline.
   - Status: integrated as `reports/semantic_plan.json`.
4. Plan contour extraction:
   - port contour-tracer idea to Python/OpenCV;
   - output footprint polygons and confidence.
5. Surgical edits:
   - exact-match patching for `.live.obj` / `semantic_parts.json`.
