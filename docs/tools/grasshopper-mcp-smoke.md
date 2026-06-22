# Grasshopper MCP Smoke Workflow

Status: active test pattern.

Use this before relying on Grasshopper automation through RhinoMCP.

## Capability Scan

```text
mcp__rhino.list_slots
-> mcp__rhino.run_python for Rhino version, units, object count
-> mcp__rhino.get_commands for Grasshopper, Script, Python
-> mcp__rhino.g1_search_components for required GH objects
```

Useful component searches:

```text
Python
C#
Script
A+B
Construct Point
Panel
```

## Smoke Graph

Build this graph first:

```text
Number Slider A
Number Slider B
Number Slider Z
-> Construct Point
-> g1_solve_graph
```

Then test script-component placement:

```text
Number Slider A
Number Slider B
-> C# Script component inputs x/y
```

At the current tool level, placing and wiring a C# Script component works. A
dedicated script-source setter is not exposed yet, so keep script bodies in
repo examples such as:

```text
scripts/grasshopper/examples/point_sum_csharp.cs
```

## Known Tool Notes

- `g1_start` can time out on an already-busy Rhino command queue. If this
  happens, use a fresh Rhino slot for the smoke test instead of closing a user's
  active work file.
- `g1_apply_graph` can fail with a generic error. Place and wire objects one by
  one to get actionable diagnostics.
- `Panel` may behave as a value source for wiring in this MCP surface. Use
  visible preview components such as `Construct Point` for the first smoke.
- Grasshopper preview geometry is not a Rhino document object; a Rhino viewport
  capture can report an empty document even when GH solved correctly.
