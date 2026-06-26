# Source Card - spellshape-three / spellshape-format

Repos:

- https://github.com/StepanKukharskiy/spellshape-three
- https://github.com/StepanKukharskiy/spellshape-format

Status in our pipeline: medium-value reference for expressions, distributions,
and repeated modules.

## What They Give Us

These repos are useful as a pattern for lightweight parametric expressions and
module distribution:

- `$parameter` references;
- arithmetic expressions;
- `sin`, `cos`, `clamp`, `lerp`;
- linear, grid, and radial distribution;
- repeated floors, facade panels, modules, columns, and bays;
- simple twist/taper/deform helpers.

## Useful Source Files

```text
spellshape-three/src/modules/interpreter/evaluator.js
spellshape-three/src/modules/plugins/distribution.js
spellshape-three/src/modules/interpreter/processor.js
spellshape-three/src/modules/interpreter/validator.js
spellshape-three/src/modules/interpreter/helpers2d.js
spellshape-three/src/modules/interpreter/helpers3d*.js
spellshape-format/README.md
```

## How To Use In Our Scenarios

Scenario 1 - Reference to model:

- Use distribution ideas for repeated facade modules after massing is approved.
- Use simple expressions for height, floor count, and bay dimensions.

Scenario 2 - Complex model cleanup:

- Not a primary tool.
- Can describe repeated reconstruction patterns after classification.

Scenario 3 - Massing and revisions:

- Strong fit for variant parameters and repeated blocks.
- Useful for small formula-based TEP changes.

## Local Rule

Start with a tiny safe expression subset:

```text
floors * floor_height
width / 2
podium_height + tower_height
lerp(a, b, t)
clamp(x, min, max)
```

Do not import the full web runtime until there is a clear local adapter and
tests.
