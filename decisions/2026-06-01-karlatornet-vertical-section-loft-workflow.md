# Karlatornet Vertical Section Loft Workflow

Date: 2026-06-01

## Decision

For Karlatornet-like twisted shaft towers, do not start by generating a stack of
horizontal sections unless the source proves that floor plates are the
controlling geometry.

Use the vertical-profile workflow:

```text
primitive shaft blocks
-> vertical guide/profile curves
-> lofted transition surfaces
-> mirror/repeat the solved part
-> complete central gaps and facade parts
```

## Reason

The building is easier to understand as repeated vertical shafts whose side
faces twist through a middle zone. Horizontal sections add unnecessary
correspondence problems and can make the model feel mathematically plausible
while missing the constructive grammar.

## Boundary

This does not replace the Grove at Grand Bay workflow. Grove remains a
horizontal contour problem because its authoritative inputs are rotated
orthogonal floor plates:

```text
control floor sections -> temporary loft -> Rhino Contour -> final floor plates
```

The deciding question is: does the source describe vertical face deformation or
floor-plate rotation?
