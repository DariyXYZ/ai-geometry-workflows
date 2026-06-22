# Grasshopper Scripts

Reusable Grasshopper script bodies and graph-builder utilities live here.

## Folders

```text
scripts/grasshopper/examples/       paste-ready C# / Python script bodies
scripts/grasshopper/graph_builders/ future RhinoMCP graph builder scripts
scripts/grasshopper/smoke/          tiny smoke tests and selectors
```

## Active Examples

| Script | Use |
| --- | --- |
| `examples/point_sum_csharp.cs` | Minimal C# Script smoke body. |
| `examples/spiral_tower_csharp.cs` | First architecture case: parametric spiral skyscraper massing. |

## Rules

- Keep meaningful script component bodies in source control.
- Read `docs/tools/grasshopper-csharp-script-nodes.md` before writing C# Script
  code for Grasshopper.
- Prefer C# 9.0-compatible Rhino 8 code for C# Script components.
- Prefer Python 3 for Rhino 8 Python Script components.
- Avoid hidden chat-only code.
- Include comments that state required inputs and outputs.
- When a script uses RhinoCommon, follow the Grasshopper script-node skill
  gotchas: `Surface.CreateExtrusion(...).ToBrep().CapPlanarHoles(...)`, include
  `using Rhino;` when using `RhinoDoc`, and treat `Curve.DivideByCount` as
  returning parameters.
- Programmatic `SetSource(...)` is not enough by itself. After any automated
  source assignment, inspect the component input/output names and solve a tiny
  script before trusting the graph.
