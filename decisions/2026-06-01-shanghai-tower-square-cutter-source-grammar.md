# 2026-06-01 - Shanghai Tower square cutter as source grammar

## Context

The user asked for a Shanghai Tower-style model in Rhino/Aurox:

- height: 632 m;
- floors: 128 above grade;
- total section rotation: 180 degrees from base to top;
- primary geometry: soft triangular floor sections;
- one corner has a cut/gouge that strengthens upward and produces the spiral
  line on the facade;
- workflow: build a few control sections, loft, validate, then generate floors
  with Contour only after the form is accepted.

Several attempts failed because the section was treated as an organic rounded
blob with a dent. The user clarified the intended construction:

```text
draw triangle
-> soften / round the triangle
-> place a rotated square at the target corner
-> cut the square out of the triangle
-> repeat the section through height with rotation and taper
```

## What improved

The v5 attempt switched back to the right family of form:

- four control sections only;
- section remains legibly triangular;
- the corner cut is angular instead of a smooth radial depression;
- the shaft twists 180 degrees over 632 m;
- the result is good enough as a massing direction check, not as a final
  accepted section rule.

This was a meaningful improvement over the "dumpling" failure mode.

## Remaining failure

The square cutters were drawn as construction curves, but they did not actually
perform the cut. The notch was generated from separate hand-coded points. That
means the model looked closer while still encoding the wrong source authority.

For this case, the cutter is not annotation. It is the constructive operation.

## Rule

When the user describes a section as:

```text
soft triangle minus rotated square
```

the generated section must be derived from the square/triangle trim:

1. create the raw triangle frame;
2. create the softened triangle curve;
3. create the rotated square cutter;
4. compute the actual intersection/trim/boolean;
5. use the resulting trimmed curve as the loft section;
6. keep the square as a visible or hidden construction object only if it matches
   the actual cut used.

Do not draw construction cutters that are disconnected from the generated
profile.

## Broader modeling lesson

Do not try to draw every final shape with a dense list of points. For this
workflow, points should define primitives, control frames, source-derived
curves, or resampling steps. The actual modeling strength comes from Rhino/CAD
operations:

```text
primitive
-> NURBS smoothing / rebuild
-> trim / boolean / split / offset
-> loft / sweep / contour / array
```

In this case, a better first step would have been:

```text
6-point triangle control polygon
-> closed NURBS curve for soft corners
-> rotated square cutter
-> actual curve trim
```

That preserves the architectural grammar and avoids "painting" a plausible
outline with arbitrary coordinates.

## Next modeling step

Rebuild a minimal version with one section first:

```text
triangle frame
soft triangle curve
rotated square cutter
actual trimmed output curve
```

Only after that one section is proven should the model create the four control
sections and loft them. This avoids hiding a wrong section rule inside a tall
twisted tower.
