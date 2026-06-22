# Grasshopper C# SetSource IO Case - 2026-06-22

Status: promoted to error rule.

## Context

Task:

Create a Grasshopper C# Script setup for a parametric spiral tower through
RhinoMCP.

Environment:

```yaml
rhino_version: 8.30.26103.11001
slot: armadillo
units_before: Millimeters
units_after: Meters
grasshopper_doc_objects_before: 0
component_type: RhinoCodePluginGH.Components.CSharpComponent
```

## What Worked

- `g1_start` opened Grasshopper.
- `g1_place_component` placed the modern Rhino 8 `C# Script` component.
- Python access to the Grasshopper .NET API worked after
  `clr.AddReference("Grasshopper")`.
- The component exposed `SetSource`, `TryGetSource`,
  `SetParametersFromScript`, and `SetParametersToScript`.
- Slider creation through `GH_NumberSlider` worked after using
  `Decimal.Parse(..., CultureInfo.InvariantCulture)`.

## What Failed

`SetSource(...)` accepted a classic `GH_ScriptInstance` source body, but the
component kept default IO:

```text
inputs: x, y
outputs: out, a
```

`TryGetSource(...)` showed that the source had been rewritten to:

```text
private void RunScript(object x, object y, ref object a)
```

The intended typed signature was not preserved.

## Lesson

Do not assume programmatic `SetSource(...)` into Rhino 8
`RhinoCodePluginGH.Components.CSharpComponent` is equivalent to manually pasting
code into the script editor.

Required gate:

```text
SetSource
-> SetParametersFromScript
-> TryGetSource
-> inspect Params.Input / Params.Output
-> solve tiny script
```

If input/output names remain default, stop and use paste-ready code or another
source assignment route.

## Promoted Docs

- `docs/tools/grasshopper-csharp-script-nodes.md`
- `docs/errors/grasshopper-mcp-error-library.md`
- `docs/libraries/grasshopper-pattern-library.md`
