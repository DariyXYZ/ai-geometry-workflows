# Grasshopper Scripts

Reusable Grasshopper script bodies and graph-builder utilities live here.

## Folders

```text
scripts/grasshopper/examples/       paste-ready C# / Python script bodies
scripts/grasshopper/graph_builders/ future RhinoMCP graph builder scripts
scripts/grasshopper/smoke/          tiny smoke tests and selectors
```

## Rules

- Keep meaningful script component bodies in source control.
- Prefer C# 9.0-compatible Rhino 8 code for C# Script components.
- Prefer Python 3 for Rhino 8 Python Script components.
- Avoid hidden chat-only code.
- Include comments that state required inputs and outputs.
- When a script uses RhinoCommon, follow the Grasshopper script-node skill
  gotchas: `Surface.CreateExtrusion(...).ToBrep().CapPlanarHoles(...)`, include
  `using Rhino;` when using `RhinoDoc`, and treat `Curve.DivideByCount` as
  returning parameters.
