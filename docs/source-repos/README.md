# Source Repositories

This folder is the compressed memory of external repositories we studied.

Purpose: a new chat or a new computer should not need to reread every GitHub
repo before continuing the workflow.

## Index

| Source | Local card | Role in our pipeline |
| --- | --- | --- |
| `StepanKukharskiy/live-obj` | `live-obj.md` | Semantic OBJ metadata, decomposed planner, validation ops, surgical patching, Rhino/GH rendering ideas. |
| `StepanKukharskiy/2DPlanTo3D` | `2d-plan-to-3d.md` | Plan/image to contour/profile extraction. |
| `StepanKukharskiy/spellshape-three`, `spellshape-format` | `spellshape-three-format.md` | Expression, distribution, repetition, and `.spell` format ideas. |
| `earthtojake/text-to-cad` | `text-to-cad.md` | STEP-first build123d backend reference. |

## Use Rule

```text
read local source card
-> use external GitHub only for missing implementation detail
-> update local source card after learning something durable
```

## External Links

- https://github.com/StepanKukharskiy/live-obj
- https://github.com/StepanKukharskiy/2DPlanTo3D
- https://github.com/StepanKukharskiy/spellshape-three
- https://github.com/StepanKukharskiy/spellshape-format
- https://github.com/StepanKukharskiy/spellshape
- https://github.com/StepanKukharskiy/spellshape-webapp
- https://github.com/StepanKukharskiy/spellshape-agent
- https://github.com/StepanKukharskiy?tab=repositories
- https://github.com/earthtojake/text-to-cad

## What Not To Do

- Do not vendor whole external repos into this repo by default.
- Do not import web runtimes just because the idea is useful.
- Do not treat external code as production dependency until we have a local
  adapter, tests, and a clear owner.
- Do not reread broad GitHub profiles when a source card already answers the
  task.
