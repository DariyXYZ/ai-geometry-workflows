# Error Ledger

This file records known failure modes so future work does not repeat them.

## Scenario 2 Mesh Cleanup

### `isSolid=True` Is Not Acceptance

A candidate can be technically closed and still architecturally wrong. Acceptance
requires source-derived validation: bbox, sections, proportions, part grouping,
and fixed view/capture review.

### Global Mesh Reduction Is Diagnostic Only

Direct decimation preserved some visual outline but produced open or skeletal
results after cleanup. It can be useful as an overlay, not as the final analysis
geometry method.

### `CombineIdentical` Can Destroy Facade Detail

On dense facade/rib geometry, `CombineIdentical` collapsed close parallel layers
and made the model visibly holey. Do not use it blindly in Scenario 2 cleanup.

### VSA Is Not Solidification

Variational shape approximation helped identify clusters, proxy planes, and
feature edges, but did not produce a watertight simplified solid. Treat VSA as
diagnostic input only.

### One Global Loft Is Wrong For Complex Buildings

Raw section lofting through the whole model failed when side/corner
correspondence changed by height. Split by architectural parts and zones before
building.

### Section Collapse Must Be Rejected

Tower-only section-solid attempts produced diagonal roof cutoffs when high-Z
sections collapsed or represented slab vertices rather than real contours.
Reject abrupt section collapse unless the source explicitly shows it.

### Do Not Invent Detail

Crown slabs, facade systems, and roof elements must come from source evidence or
an explicit simplification rule. Busy invented geometry is worse than a clean
admitted omission.

## Reference Modeling

### Massing Before Detail

Reference-driven architecture must pass massing/proportion gates before facade
detail. Detail cannot rescue a wrong silhouette.

### Do Not Guess One Envelope When The Building Has A Constructive Grammar

Karlatornet showed a specific failure mode: treating a tower as one guessed
continuous envelope produced a plausible but wrong form. The correct route was
to identify the building grammar first: four square shafts in plan, central
cross/gaps, facade-derived twist start/end datums, lofted twist sections, and
mirrored/repeated quadrants.

Before modeling reference architecture, ask:

- What repeated primitives does the building appear to be made from?
- Which view proves the plan grammar?
- Which facade marks the vertical datums where the form changes?
- Can one part be built from sections and then mirrored/arrayed?

If the available views do not prove this, ask for more views instead of
inventing an envelope.

### Do Not Force Horizontal Sections Onto A Vertical-Profile Problem

The later Karlatornet correction showed that a twist is not always best modeled
from horizontal floor sections. If the form is made from repeated vertical
primitives and the deformation is readable as a surface between vertical edge
or facade curves, build from vertical guides, loft the face/transition, then
mirror or repeat the solved part.

Forcing this family into horizontal slices can create unnecessary corner
correspondence problems and a wrong mental model. Decide the section direction
from the building grammar:

- Grove at Grand Bay: horizontal contour floor plates.
- Karlatornet-like four-shaft tower: vertical guide curves, loft, mirror.

### Plan Drawings Are Not Always Exterior Envelopes

Structural/load/core plans can be narrower than the exterior massing envelope.
Classify source authority before using plan dimensions as final footprint.

### Do Not Reconstruct Orthogonal Floor Plates From Resampled Corners

Grove at Grand Bay exposed a repeatable failure mode: when a tower twists
between orthogonal rectangular floor plates, resampling source rectangles and
aligning arbitrary curve parameters can create warped, non-orthogonal
intermediate floors. That is wrong even if the overall twist silhouette looks
plausible.

Correct workflow for this family:

1. Loft only the authoritative control sections, for example floor 1, floor 14,
   and roof.
2. Use Rhino `Contour` on that temporary lofted surface/polysurface to generate
   horizontal floor-section curves at the required elevations.
3. Hide or delete the temporary loft mass.
4. Build slabs, balcony edges, rails, and glass lines directly from the
   resulting contour curves.

Do not rebuild those contour curves from guessed corners, bbox rectangles, or
newly sampled point order. The contour curves are the source of truth.

### User-Prepared Rhino Curves Override Approximate Parametric Sections

Infinity Tower/SOM exposed a related failure mode: when the user has already
drawn the actual floor contour, core curve, and height axis in Rhino, those
curves are the source authority. Do not replace them with a simplified square,
rectangle, or generic chamfered section just because the building can be
described as "one section rotating with height."

Correct workflow:

1. Read the visible source curves from Rhino.
2. Classify them as floor contour, core, and height/twist axis.
3. Verify units and height from the axis.
4. Transform copies of the exact floor contour through height.
5. Build loft/floor/facade guides from those transformed copies.

Approximate parametric sections are only acceptable when no source curve exists.

### Do Not Turn A Cut-Out Section Into An Organic Blob

The Shanghai Tower-style twist case exposed another source-grammar failure: a
soft triangular floor plate with a corner cut-out must not be modeled as a
round/polar blob with a radial dent. The reference grammar is closer to:

```text
soft triangle
minus rotated square/diamond cutter at one corner
-> cutter depth changes by height
-> four control sections
-> loft validation
-> Contour floors only after the form is accepted
```

If the cut-out is represented only as a smooth radial depression, the tower
becomes a "dumpling" shape and loses the triangular plan logic. Build the
section as a constructive 2D profile first, with explicit cutter lips and inner
cut edges. Then rotate/taper the whole profile through height.

### Construction Curves Must Actually Drive The Cut

The next Shanghai Tower iteration improved the massing by using four soft
triangular control sections over 632 m with a 180 degree twist. The section
read correctly as triangular again, and the corner cut became sharp enough to
produce the intended spiral groove.

The remaining error was subtler: rotated square cutters were drawn next to the
sections, but the notch itself was still produced by separate scripted points.
That makes the square a diagram, not a source authority. If the intended
grammar is:

```text
soft triangle minus rotated square
```

then the final section curve must be derived from that operation. Use a real
2D boolean/trim/intersection workflow where possible, or compute the same
intersection explicitly. Do not show a cutter while using unrelated notch
coordinates, because the model can look close while encoding the wrong rule.

### Do Not Draw Primitive Logic As A Point Cloud

A broader modeling mistake behind the same case was trying to hand-draw the
final section with many coordinates. That loses the logic of the model. In CAD
and Rhino workflows, the strongest path is often to build with primitives and
operations:

```text
triangle / rectangle / circle / guide primitive
-> NURBS smoothing or rebuild
-> trim / boolean / split / offset
-> loft / sweep / contour / array
```

Use points to define primitives, control curves, or resample proven source
geometry. Do not use raw point lists as a substitute for a known primitive
operation such as "square cuts triangle" or "offset glass from slab edge."

### Do Not Put Glass On The Slab Edge For Balcony Towers

Grove at Grand Bay exposed a second failure after the contour workflow was
fixed: the glass plane was placed flush with the exterior contour. That erased
the balcony depth even though the floor outlines were correct.

Correct interpretation:

- contour curve = exterior slab / balcony edge;
- floor slab = real thickness, not a zero-thickness surface;
- glass facade = inward offset from the contour;
- rail / edge profile = outer contour or near outer contour.

For buildings with projecting balconies, always model slab edge, glass line,
and railing as separate systems.

### Do Not Add Secondary Elements Before Shell Fit And Support Are Accepted

The Flock chapel shell case produced a medium-success massing: the roof read as
a wave/ribbon concrete shell with alternating crests and valleys. That was the
right family of form.

The failed gates were:

1. Secondary elements were premature. Glass, posts, and mullions were generated
   before the shell was accepted. They protruded below the shell, did not follow
   the real envelope, and made the model look less trustworthy.
2. Plan fit was off. The shell was too long relative to the scaled Rhino
   underlay. A scaled plan is source authority for footprint and must be checked
   before capture or detail.
3. Support logic was missing. The shell should bear on the concrete folded
   plinth/support elements visible in plan and sections. It must not read as
   floating above the ground plane.

Correct order for similar shell cases:

```text
scaled plan footprint
-> section-derived crest/valley heights
-> shell surface only
-> fit check against plan underlay
-> concrete folds / plinth supports at contact lines
-> thickness / rim
-> glass and posts after shell/support acceptance
```

If secondary elements appear below the shell or outside the accepted envelope,
delete them and return to the massing/support gate.

## Context Management

### Loose Scripts Hide Decisions

Versioned scripts like `add_test_data2_v12_*` are useful evidence, but they are
not a system. Promote lessons into `docs/`, `decisions/`, or case reports before
continuing.

### Chat Memory Is Not Durable

If a route, boundary, or failure matters, write it into repo docs or Obsidian.
Do not rely on a future chat remembering it.
