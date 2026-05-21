# Team Update: AI Geometry / Scenario 2

Date: 2026-05-21  
Repo: `DariyXYZ/ai-geometry-workflows`  
Local benchmark: `test_data_2.3dm`

## Short Version

We are moving from ad hoc "Codex to Rhino model" attempts to a case-based,
validation-first toolchain.

The current direction is:

```text
source geometry -> classify architectural parts -> reconstruct closed simplified parts -> validate by sections/views
```

This is now backed by a first runnable CLI: `ai_geometry_toolkit`.

## What Changed

The benchmark changed from a single tower (`22.3dm`) to a full complex model
(`test_data_2.3dm`) containing:

- high-rise tower;
- oval podium;
- small rounded podium block;
- connector/plinth slab;
- supports/columns;
- facade ribs, slabs, bands, and crown detail.

This confirmed that the scene is a set of architectural systems, not one
continuous skin. A single global repair/reduction strategy is not enough.

## Results So Far

`test_data2_v1_direct_45000`

- Direct mesh decimation.
- Preserved the overall shape better than earlier hull/loft experiments.
- Still open and not CAD-clean.

`test_data2_v1_direct_28000`

- Became visibly holey/skeletal after Rhino cleanup.
- Root cause: `CombineIdentical` collapses close parallel facade layers and rib geometry.

`test_data2_v2_preserve_45000`

- Avoided `CombineIdentical`.
- Better diagnostic overlay, but still open/holey.
- Not acceptable as final geometry.

`test_data2_v3_clean_massing`

- First closed clean baseline.
- Uses separate closed primitive parts for the tower, podiums, connector slabs,
  rounded tower corner, side bands, fins, and roof/crown steps.
- Good direction, but too abstract. Needs proportional refinement against source.

## Decision

Use `v3_clean_massing` as the baseline for refinement.

Do not continue with:

- global direct decimation as final output;
- Poisson, voxel, MeshFix, or ShrinkWrap as the primary repair path;
- `CombineIdentical` on dense facade meshes;
- one section loft through the full building;
- one hull/envelope for the full building;
- invented crown slabs or facade systems not visible in the source.

## New Tooling Added

The repo now has `ai_geometry_toolkit`, a first orchestration CLI.

Current commands:

- `new-case` - creates a reproducible case folder;
- `validate-case` - checks manifest and params;
- `route` - writes the scenario-specific development route;
- `classify-scan` - classifies scan report objects into architectural groups;
- `audit-scan` - writes a compact scan audit report.

Smoke result on existing `tower_bbox_classification.json`:

```text
primary_envelope=1
podium_base=11
supports=41
large_bands=3
crown_roof=207
facade_detail=1627
noise=671
```

This is heuristic and not final architectural truth, but it is enough to route
the next step: review major groups before section extraction and candidate build.

## Next Work

Build `v4_refined_clean_massing` through the toolchain:

1. Create a cleanup case.
2. Scan source with hidden/locked objects included.
3. Classify architectural parts.
4. Extract sections per part.
5. Refine tower footprint, rounded corner, height, crown steps, and side bands.
6. Refine oval podium and small rounded podium proportions.
7. Keep facade ribs/bands as optional simplified guide geometry.
8. Validate with fixed captures: perspective, front, side, top.
9. Add bbox/section delta report before accepting the model.

## Useful Files

- Source export: `C:\temp\claude_to_cad\test_data2_current.obj`
- Status file: `C:\VS Code\workfiles\cad_mesh_reconstruction_status.json`
- v3 builder: `C:\VS Code\workfiles\build_test_data2_clean_massing_v3.py`
- v3 Rhino layer: `CTR_TestData2_CleanMassing_v3`
- v3 shifted review capture: `C:\temp\claude_to_cad\test_data2_v3_clean_massing_shifted_review.png`
- Toolkit docs: `TOOLKIT.md`
