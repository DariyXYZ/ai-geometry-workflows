# RhinoCommon Helper Layer

Status: initial runnable bridge.

## Purpose

Aurox is the bridge into the active Rhino scene. It is good for readback,
layers, simple geometry, and captures, but its typed MCP tools are not the full
Rhino modeling surface.

The RhinoCommon helper layer lets the repository call native RhinoCommon code
inside Rhino through Aurox `execute_csharp`.

```text
Codex / repo workflow
-> Aurox connection
-> execute_csharp
-> RhinoCommon operations in the active Rhino document
```

This is the route for maximum Rhino-native modeling without waiting for every
Rhino command to become a first-class MCP tool.

## Script

```text
scripts/rhino_common_helper.py
```

The script is a small local runner. It generates or reads C# code, sends it to
Aurox `execute_csharp`, and prints the result.

Requirements:

- Rhino is open;
- Aurox MCP is running in Rhino with the `AuroxMcp` command;
- the Python bridge can reach `rhino_aurox_client.py`.

The helper path can be overridden:

```powershell
$env:AUROX_CLIENT="C:\path\to\rhino_aurox_client.py"
```

## Commands

List available helper operations:

```powershell
python scripts\rhino_common_helper.py list-ops
```

Print visible curves from the active Rhino document:

```powershell
python scripts\rhino_common_helper.py read-visible-curves
```

Create a soft closed NURBS/control-point curve:

```powershell
python scripts\rhino_common_helper.py make-soft-closed-curve `
  --points "[[0,0,0],[8,0,0],[10,5,0],[5,9,0],[0,5,0]]" `
  --degree 3 `
  --layer RC_HELPER_curves `
  --name soft_profile
```

Run a 2D curve difference from point loops:

```powershell
python scripts\rhino_common_helper.py curve-difference-2d `
  --boundary "[[0,0,0],[10,0,0],[10,10,0],[0,10,0]]" `
  --cutter "[[6,4,0],[12,4,0],[12,8,0],[6,8,0]]" `
  --layer RC_HELPER_curves `
  --name trimmed_profile
```

Contour a Brep by Z interval:

```powershell
python scripts\rhino_common_helper.py contour-brep `
  --object-id "<rhino-object-guid>" `
  --z-min 0 `
  --z-max 300 `
  --interval 3.2 `
  --layer RC_HELPER_contours
```

Run custom C# inside Rhino:

```powershell
python scripts\rhino_common_helper.py run-csharp .\scripts\my_rhino_operation.cs
```

For review without Rhino execution:

```powershell
python scripts\rhino_common_helper.py --dry-run read-visible-curves
```

## Modeling Rule

Use this helper whenever the building grammar is a native CAD operation:

```text
primitive
-> NURBS rebuild / smoothing
-> split / trim / boolean / offset
-> loft / sweep / contour
```

Do not replace these operations with dense point drawing unless the points come
from source geometry or a final resampling step.

## Next Helper Operations

Add these as soon as a case needs them:

- `trim_curve_with_curve`
- `split_curve_at_intersections`
- `loft_closed_sections_with_seam`
- `fit_curve_to_plan_bbox`
- `extract_selected_curves`
- `extract_visible_source_curves`
- `make_shell_from_control_grid`
- `create_concrete_fold_supports`
- `section_brep_at_planes`
- `offset_glass_inward_from_slab_edge`

Each helper should be small, named, testable by `--dry-run`, and validated in
Rhino with a bbox/capture review.
