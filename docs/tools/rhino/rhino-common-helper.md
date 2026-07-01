# Legacy RhinoCommon Helper Layer

Status: legacy optional backend-specific bridge.

## Purpose

The default Rhino transport for this repository is standard McNeel RhinoMCP.
For new modeling, use `mcp__rhino.run_python` or `mcp__rhino.run_csharp`
directly and choose the operation sequence from
`docs/tools/rhino/rhino-mcp-command-library.md`.

This helper is not the default path. It is a legacy optional
backend-specific route for operations that need direct RhinoCommon execution
through a non-standard backend.

Rule: when a user selects any third-party Rhino MCP/plugin backend, use a
RhinoCommon execution route (`run_python`, `run_csharp`, `execute_csharp`, or
the backend equivalent) for non-trivial geometry. Do not rely on a proprietary
helper surface until its schemas and a smoke run have been checked.

The current implementation calls native RhinoCommon code inside Rhino through
Aurox `execute_csharp`. Use it only when the user asks for Aurox, when replaying
a legacy Aurox case, or when standard RhinoMCP cannot expose the required
native operation and the workaround is stated explicitly.

```text
Codex / repo workflow
-> selected Rhino backend
-> execute_csharp
-> RhinoCommon operations in the active Rhino document
```

For current RhinoMCP work, the equivalent route is simpler:

```text
Codex / repo workflow
-> mcp__rhino.run_python or mcp__rhino.run_csharp
-> RhinoCommon operations in the active Rhino document
```

## Script

```text
scripts/rhino/common/rhino_common_helper.py
```

The script is a small local runner. It generates or reads C# code, sends it to
the configured backend-specific `execute_csharp` route, and prints the result.

Legacy helper requirements:

- Rhino is open;
- a backend with `execute_csharp` support is running in Rhino;
- the Python bridge can reach `rhino_aurox_client.py`.

The helper path can be overridden:

```powershell
$env:AUROX_CLIENT="C:\path\to\rhino_aurox_client.py"
```

## Commands

List available helper operations:

```powershell
python scripts\rhino\common\rhino_common_helper.py list-ops
```

Print visible curves from the active Rhino document:

```powershell
python scripts\rhino\common\rhino_common_helper.py read-visible-curves
```

Create a soft closed NURBS/control-point curve:

```powershell
python scripts\rhino\common\rhino_common_helper.py make-soft-closed-curve `
  --points "[[0,0,0],[8,0,0],[10,5,0],[5,9,0],[0,5,0]]" `
  --degree 3 `
  --layer RC_HELPER_curves `
  --name soft_profile
```

Run a 2D curve difference from point loops:

```powershell
python scripts\rhino\common\rhino_common_helper.py curve-difference-2d `
  --boundary "[[0,0,0],[10,0,0],[10,10,0],[0,10,0]]" `
  --cutter "[[6,4,0],[12,4,0],[12,8,0],[6,8,0]]" `
  --layer RC_HELPER_curves `
  --name trimmed_profile
```

Contour a Brep by Z interval:

```powershell
python scripts\rhino\common\rhino_common_helper.py contour-brep `
  --object-id "<rhino-object-guid>" `
  --z-min 0 `
  --z-max 300 `
  --interval 3.2 `
  --layer RC_HELPER_contours
```

Run custom C# inside Rhino:

```powershell
python scripts\rhino\common\rhino_common_helper.py run-csharp .\scripts\my_rhino_operation.cs
```

For review without Rhino execution:

```powershell
python scripts\rhino\common\rhino_common_helper.py --dry-run read-visible-curves
```

## Modeling Rule For New Work

Use RhinoCommon through standard RhinoMCP whenever the building grammar is a
native CAD operation:

```text
primitive
-> NURBS rebuild / smoothing
-> split / trim / boolean / offset
-> loft / sweep / contour
```

Do not replace these operations with dense point drawing unless the points come
from source geometry or a final resampling step. Use this legacy helper only
when the selected backend is not standard RhinoMCP.

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
