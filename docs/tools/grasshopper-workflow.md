# Grasshopper Workflow

Status: active working layer.

Use this file when the task should produce, inspect, or automate a Grasshopper
definition through RhinoMCP.

## Goal

Make Grasshopper work fast without guessing the environment:

```text
capability scan
-> minimal smoke graph
-> choose graph strategy
-> build incrementally
-> solve and validate
-> record reusable script/graph pattern
```

## First 90 Seconds

Always start with the same preflight:

1. `mcp__rhino.list_slots`
   - If no slot is present, ask the user to run `MCPStart` in Rhino (see GH-010;
     the command is `MCPStart`, not `MCPConnect`).
   - Do not launch Rhino or Grasshopper automatically unless the user explicitly
     asks for it.
2. `mcp__rhino.run_python` for:
   - Rhino version
   - document name
   - units
   - document object count
3. `mcp__rhino.get_commands` for:
   - `Grasshopper`
   - `Script`
   - `Python`
4. Component lookup: do NOT call `g1_search_components` on a user-started
   (adopted) slot — it crashes Rhino (see GH-009). Query the GH component server
   from `run_python`, or rely on documented GUIDs.
5. Confirm Grasshopper access by asking the user to open Grasshopper manually.
6. Validate geometry logic with `run_python` smoke scripts whenever possible.
   Do not lead with `run_csharp`; it can wedge the plugin handler (GH-012).
   Reserve `g1_*` canvas automation for slots the user explicitly asked to
   spawn, and reserve C# source automation for routes that passed a disposable
   smoke test in the same Rhino/GH version.

Do not start with a large graph. A failed five-node graph is cheap. A failed
hundred-node graph is a fog machine.

## Standard Smoke Graph

Use this graph to prove canvas placement, wiring, and solving:

```text
Number Slider A = 3.5
Number Slider B = 7.25
Number Slider Z = 2.0
-> Construct Point
-> g1_solve_graph
```

Why this graph:

- it uses only standard GH components;
- it has visible preview geometry;
- it avoids `Panel` wiring edge cases;
- it does not depend on Rhino document objects.

## Script Component Smoke

After the standard graph solves:

```text
Number Slider A
Number Slider B
-> C# Script component inputs x/y
```

At the current RhinoMCP `g1_*` tool level, placing and wiring `C# Script` and
`Python 3 Script` components works. Source editing is not exposed as a direct
`g1_*` operation. Rhino 8 components may expose `SetSource(...)` through the
Grasshopper .NET API, but this route must be smoke-tested before production
because it can accept code while keeping the wrong default `x/y/out/a` IO.

Keep script bodies as paste-ready files under:

```text
scripts/grasshopper/
```

Use `scripts/grasshopper/examples/point_sum_csharp.cs` as the first C# script
body example.

For C# Script work, read:

```text
docs/tools/grasshopper-csharp-script-nodes.md
```

## Graph Strategy

Choose the smallest graph type that can prove the task:

| Need | Prefer |
| --- | --- |
| Pure numeric/param test | Sliders + standard components |
| Preview geometry | Construct Point / Line / Rectangle / Boundary Surface |
| Source Rhino curves | Rhino document read via RhinoMCP, then reference/bake later |
| Parametric massing | Sliders + footprints + extrusion/script component |
| Complex geometry logic | C# Script component body stored in repo |
| Repeated production graph | Scripted graph builder in `scripts/grasshopper/` |

For C# Script components, distinguish the safe parts from the risky part:

```text
safe after smoke: sliders, groups, standard GH components, simple wiring
risky: programmatic C# source injection / IO refresh
```

The Pavilion 80hz case proved that legacy `SourceCodeChanged(None)` can crash
Rhino 8.30 (GH-015). Keep paste-ready C# bodies in source control and paste
manually unless a source bridge has just been proven on a disposable graph.

## Build Order

```text
1. Ask the user to open Rhino and Grasshopper, then run `MCPStart`
2. Place named sliders first
3. Place standard components
4. Wire one chain
5. Solve
6. Validate the preview or outputs
7. Add the next chain
8. Only then place script components
```

Do not place all components before the first solve. One bad selector or one
input-name mismatch should not invalidate the whole graph.

## Source Authority

If Rhino curves, footprints, or selected objects are the source authority:

- inspect them first with RhinoMCP/RhinoCommon;
- record object ids, names, layers, colors, area/bbox;
- do not replace them with generic geometry;
- keep source curves in Rhino and use GH as transformation/generation logic.

For model-building work, source Rhino curves override inferred parametric
sections.

## Validation Gates

Every useful GH graph should report:

```yaml
rhino_version:
grasshopper_access:
  g1_start: pass/fail
  component_search: pass/fail
  place_component: pass/fail
  connect: pass/fail
  solve: pass/fail
components_used:
inputs:
outputs:
known_limitations:
```

For geometry:

- no floating outputs unless intentionally preview-only;
- units are declared;
- source curves are preserved;
- component previews match expected bbox/scale;
- script component code is stored in repo if it matters.

## When To Use RhinoCommon

Use RhinoCommon inside a C# or Python script component when:

- GH standard components would require too much wiring;
- the task needs precise loops, classification, validation, or object metadata;
- the operation depends on tolerances, sections, lofts, booleans, or contours;
- you need a reusable script body in source control.

For third-party Rhino/GH plugins, use their components only after a component
search and a small smoke solve. For non-trivial geometry, prefer RhinoCommon
script logic over opaque plugin helper chains.

For Grasshopper C# Script nodes, follow the dedicated node rules in
`docs/tools/grasshopper-csharp-script-nodes.md`.
