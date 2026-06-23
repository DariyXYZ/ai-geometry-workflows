# Grasshopper C# Script Nodes

Status: active repo-native rules, promoted from the local
`grasshopper-script-nodes` skill.

Use this file before writing or automating C# code for a Grasshopper Script
component.

## Source Of Truth

This repository is the portable source of truth for Grasshopper C# Script
generation rules. The original local Codex skill was used as seed material, but
future agents should be able to work from the repo alone.

Required read order for C# Script tasks:

```text
docs/tools/grasshopper-workflow.md
-> docs/tools/grasshopper-csharp-script-nodes.md
-> docs/tools/grasshopper-csharp-performance.md
-> docs/errors/grasshopper-mcp-error-library.md
-> scripts/grasshopper/README.md
-> scripts/grasshopper/examples/
```

## Environment Preflight

Before writing code:

1. Detect Rhino and Grasshopper version.
2. Confirm model units.
3. Search for script components with `g1_search_components`.
4. Prefer the dedicated modern `C# Script` component for Rhino 8 when the user
   will edit/paste code manually.
5. Prefer a proven source-assignment route only after a smoke test proves that
   inputs and outputs are created correctly.

Safe baseline:

```text
Rhino 8
Grasshopper on Rhino 8
C# 9.0-compatible syntax
RhinoCommon for non-trivial geometry
```

## Paste-Ready C# Shape

Use the classic Grasshopper C# script structure unless a newer Script component
format is explicitly proven:

```csharp
#region Usings
using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
#endregion

public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(double Width, double Height, ref object Geometry, ref object Info)
  {
    Geometry = null;
    Info = "Ready";
  }
}
```

Rules:

- Include `using Rhino;` whenever the script uses `RhinoDoc`.
- Put meaningful input and output names directly in `RunScript`.
- Prefer typed inputs such as `double`, `int`, `bool`, `Curve`, `Brep`, and
  `List<Brep>` when the access shape is known.
- Use `ref object` outputs with clear names.
- Initialize outputs before validation so disconnected inputs stay neutral.
- Keep helper methods inside the same script node.
- Avoid advanced C# syntax unless the local runtime proves support.

## Automatic IO Contract

Prefer automatic inputs and outputs through the `RunScript` signature whenever
the script will be pasted manually into the Rhino 8 C# Script editor:

```csharp
private void RunScript(
  int Floors,
  double FloorHeight,
  double Width,
  List<Curve> SourceCurves,
  ref object FloorPlates,
  ref object Rails,
  ref object Info)
```

Rules:

- Use semantic parameter names; avoid `x`, `y`, `a`, and `out` in production
  scripts.
- Encode the intended access shape in types: scalar inputs as `double`/`int`,
  list inputs as `List<T>`, and tree inputs only when the script really needs
  branch structure.
- Keep optional numeric inputs idle-safe by assigning practical defaults when
  values are missing, zero, negative, or otherwise invalid for the algorithm.
- Initialize every output before validation.
- Keep diagnostic text in a named output such as `Info`; do not depend on the
  default `out` unless the task is a tiny smoke test.

Important automation caveat:

- Programmatic `SetSource(...)` on the modern Rhino 8 component can keep the
  default `x/y/out/a` contract. Treat automatic IO from the signature as a
  manual-paste feature unless the source-assignment route has just passed the
  inspection gate below.

## RhinoCommon Geometry Gotchas

Use conservative, locally proven RhinoCommon calls:

```csharp
Surface extrusionSurface = Surface.CreateExtrusion(loop, direction);
Brep openBrep = extrusionSurface != null ? extrusionSurface.ToBrep() : null;
Brep capped = openBrep != null ? openBrep.CapPlanarHoles(tolerance) : null;
```

Do not use these without local verification:

- `Brep.CreateFromExtrusion`
- `Extrusion.CreateExtrusion` typed as `Extrusion`
- `Brep.RebuildEdges`
- `Curve.DivideByCount` as if it returned points
- ambiguous intersection/projection overloads

Known rules:

- `Curve.DivideByCount(count, includeEnds)` returns curve parameters in the
  target workflow; call `curve.PointAt(t)`.
- `Intersection.MeshRay` returns the first hit parameter, not all hits.
- `Intersection.MeshLineSorted(mesh, line, out int[] faceIds)` needs the
  `out` face-id overload in the observed Rhino 8 environment.
- `Line.ClosestParameter(point)` returns a double directly, not a Try-pattern
  with an out parameter.
- Never reassign a `foreach` iteration variable; use a separate local variable.
- In Rhino 8 C# runner smoke scripts, use `TextEntity.PlainText` instead of
  obsolete `TextEntity.Text`.
- Use `RhinoApp.WriteLine(string.Format(...))`; do not assume `WriteLine`
  accepts a format string plus multiple arguments.

## Script Component Automation Rules

There are two separate operations:

```text
place/wire component through RhinoMCP
set the script source and IO contract
```

The first is available through `g1_*` tools. The second is version-sensitive.

Observed Rhino 8 component type:

```text
RhinoCodePluginGH.Components.CSharpComponent
```

It exposes:

```text
SetSource(string)
TryGetSource(out string)
SetParametersFromScript()
SetParametersToScript()
```

But this does not guarantee that a classic `GH_ScriptInstance` body will create
the intended inputs and outputs when assigned programmatically. In the
2026-06-22 smoke attempt, `SetSource` accepted the source but the component kept
default `x`, `y`, `out`, and `a` parameters and rewrote `RunScript`.

Gate:

```text
after SetSource
-> TryGetSource
-> inspect Params.Input and Params.Output
-> solve a tiny script
-> only then use the route for production
```

If the IO contract is wrong, stop and use one of these paths:

- paste-ready code stored in `scripts/grasshopper/examples/`;
- manual paste into the component editor;
- legacy C# component only after a separate smoke test proves source and IO;
- a dedicated graph-builder script once the component source format is known.

## Good Script Node Defaults

For generated scripts:

- use practical non-zero default values inside the script;
- do not invent placeholder Rhino geometry;
- expose dimensions, counts, tolerances, and modes as inputs;
- output geometry plus a short `Info` summary;
- keep output object counts controlled;
- store meaningful examples in `scripts/grasshopper/examples/`.

For architecture/massing:

- model in meters unless the source model says otherwise;
- output blockout/massing first, detail later;
- report height, floor count, footprint dimensions, twist/taper, and units;
- avoid baking until the preview graph passes.

## Related Performance Rules

For list access, parallel computation, caching, and large geometry generation,
read:

```text
docs/tools/grasshopper-csharp-performance.md
```
