# Decision - Constructive Grammar Before Reference Modeling

Date: 2026-05-28

## Status

Accepted.

## Context

During the Karlatornet text+image modeling test, the first Rhino blockout failed
because it treated the tower as one guessed outer envelope. The result used some
correct numeric anchors, but the geometry logic was wrong.

The correct route was:

```text
1. Identify four square shafts in plan.
2. Use the 33 x 33 m footprint, total height, and gaps between volumes.
3. Read facade screenshots for height datums where twisting starts/ends.
4. Build twist sections and loft the form.
5. Mirror/repeat into four parts.
6. Build the inner cross to complete facades.
7. Compare against reference.
```

The failure was a missing reasoning gate in the pipeline, not only a bad
parameter choice.

## Decision

For Scenario 1 reference modeling, do not build Rhino/build123d geometry until
the constructive grammar is stated.

Required sequence:

```text
text/images
-> source authority table
-> constructive grammar
-> section/repetition strategy
-> missing-view check
-> geometry
-> compare
```

Before modeling, capture:

- repeated primitives or modules;
- plan grammar and hard footprint anchors;
- vertical datums where the form changes;
- which part can be built once and mirrored/arrayed;
- what views are missing or ambiguous;
- what will be omitted until the massing gate passes.

If the available views do not prove the grammar, ask for more views instead of
inventing a plausible envelope.

## Consequences

- A simple blockout can still be wrong if it uses the wrong construction logic.
- Semantic parts must describe construction, not only visible appearance.
- `semantic_plan.json` should include build strategy: `loft_sections`,
  `mirror_quadrants`, `array_modules`, `guide_only`, etc.
- `2DPlanTo3D` contour extraction is not enough by itself; contours need source
  authority and grammar interpretation.
- Facade detail remains blocked until massing and constructive grammar are
  accepted.

## Karlatornet Rule

Karlatornet should be modeled as:

```text
four square shafts + central cross/gaps + facade-derived twist datums
+ section lofts + mirrored/repeated quadrants
```

Not as:

```text
one guessed continuous tower envelope with a generic twist
```

