# Source Card - text-to-cad

Repo: https://github.com/earthtojake/text-to-cad

Status in our pipeline: STEP-first CAD backend reference.

## What It Gives Us

`text-to-cad` is useful as a build123d/CAD-as-code backend reference for clean,
parametric geometry that should export to STEP.

It is not a Rhino scene understanding layer and not a replacement for
reference-source validation.

## How It Fits

```text
prompt / reference / semantic plan
-> named parts and parameters
-> build123d candidate
-> STEP export
-> RhinoMCP review and validation
```

## How To Use In Our Scenarios

Scenario 1 - Reference to model:

- Good for precise, clean parametric candidates after source authority and
  constructive grammar are known.
- Especially useful for extrusions, boxes, profiles, booleans, chamfers, and
  repeatable CAD parts.

Scenario 2 - Complex model cleanup:

- Secondary backend only.
- RhinoMCP remains responsible for reading and classifying existing `.3dm`
  sources.

Scenario 3 - Massing and revisions:

- Useful for reproducible massing candidates when the inputs are already
  parameterized.

## Boundary

Use `text-to-cad` / build123d for:

- clean B-rep style candidates;
- deterministic generation;
- STEP-first export;
- reproducibility.

Do not use it for:

- reading arbitrary Rhino scenes;
- interpreting messy images alone;
- replacing source comparison;
- repairing complex meshes globally.
