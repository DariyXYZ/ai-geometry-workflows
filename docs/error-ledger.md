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

### Plan Drawings Are Not Always Exterior Envelopes

Structural/load/core plans can be narrower than the exterior massing envelope.
Classify source authority before using plan dimensions as final footprint.

## Context Management

### Loose Scripts Hide Decisions

Versioned scripts like `add_test_data2_v12_*` are useful evidence, but they are
not a system. Promote lessons into `docs/`, `decisions/`, or case reports before
continuing.

### Chat Memory Is Not Durable

If a route, boundary, or failure matters, write it into repo docs or Obsidian.
Do not rely on a future chat remembering it.
