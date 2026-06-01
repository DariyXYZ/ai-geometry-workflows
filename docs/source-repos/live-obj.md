# Source Card - live-obj

Repo: https://github.com/StepanKukharskiy/live-obj

Status in our pipeline: high-value reference, partial local integration.

Do not treat it as a required runtime dependency. Reuse the patterns.

## What It Gives Us

`live-obj` shows how an ordinary OBJ-like scene can carry semantic metadata in
comments. This is useful for our `semantic_obj` layer: the mesh/preview can stay
simple while metadata stores intent, dimensions, anchors, controls, constraints,
and validation hints.

## Useful Concepts

Metadata keys worth preserving:

- `#@params` - dimensions and design variables.
- `#@controls` - editable UI knobs or revision handles.
- `#@bbox` - expected part extents.
- `#@anchor` - connection points and alignment handles.
- `#@constraint` - soft relationships.
- `#@lock` - preserve footprint, position, silhouette, material, or other facts.
- `#@hidden: true` - guide paths, construction curves, cutters, non-final helpers.
- `#@source` - procedural, llm_mesh, assembly, sdf, simulation, recipe.

Planner idea:

```text
do not generate whole building at once
-> create semantic part plan
-> build one part at a time
-> validate each part against source hints
```

Patch idea:

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

This is useful for small, controlled edits to `.live.obj`, `semantic_parts.json`,
or generated scripts.

## Already Integrated Locally

- `import-semantic-obj` command.
- `tests/fixtures/office_tower_semantic.live.obj`.
- `reports/semantic_parts.json`.
- `reports/semantic_plan.json`.
- `reports/semantic_validation.md`.

## Useful Source Files In That Repo

```text
README.md
AGENTS.md
src/lib/server/llm/liveObjSystemPrompt.ts
src/lib/server/llm/liveObjChat.ts
src/lib/liveObj/rawPostValidation.ts
src/lib/server/liveObj/surgicalPatch.ts
src/routes/api/executor/raw_obj_post_executor.py
grasshopper_live_obj_render_ghpython.py
grasshopper_decomposed_builder_ghpython.py
project_live_obj_files/*.live.obj
```

## How To Use In Our Scenarios

Scenario 1 - Reference to model:

- Use semantic metadata to name parts, dimensions, anchors, and controls before
  Rhino/build123d generation.
- Keep hidden construction objects explicit.

Scenario 2 - Complex model cleanup:

- Use only as vocabulary for tags/parts/validation.
- Do not use it as mesh repair.

Scenario 3 - Massing and revisions:

- Use controls, params, and surgical patching ideas for small revisions and
  variant deltas.

## Do Not Reuse Blindly

- Do not import the full runtime.
- Do not use tessellated OBJ output as final CAD.
- Do not let unknown post-ops enter build scripts.
- Do not replace source-derived Rhino validation with semantic claims.
