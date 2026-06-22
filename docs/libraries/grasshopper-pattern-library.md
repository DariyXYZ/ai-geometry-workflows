# Grasshopper Pattern Library

Status: draft active library.

Reusable patterns for fast Grasshopper work through RhinoMCP.

## Pattern - Capability Scan First

When to use:

Every GH automation session.

Inputs needed:

- Rhino slot id
- current document state
- intended component families

Logic:

```text
list_slots
-> run_python version/units/object_count
-> get_commands Grasshopper/Script/Python
-> g1_search_components
-> g1_start
-> smoke graph
```

Acceptance:

- Rhino version known;
- units known;
- required component GUIDs known;
- smoke graph solves.

Failure modes:

- `g1_start` timeout;
- component search without GH document;
- ambiguous duplicate component names.

## Pattern - Manual First, Batch Later

When to use:

Any new GH graph builder.

Logic:

```text
place one slider
-> place one component
-> wire one connection
-> solve
-> repeat
-> only then use g1_apply_graph
```

Acceptance:

Every selector and parameter name is proven before batching.

Failure modes:

- `g1_apply_graph` generic failure;
- wrong parameter name;
- wrong duplicate component.

## Pattern - Preview Geometry Smoke

When to use:

To prove Grasshopper solve and viewport preview quickly.

Graph:

```text
Slider X
Slider Y
Slider Z
-> Construct Point
```

Acceptance:

`g1_solve_graph` returns `Success`.

Note:

Preview geometry is not a Rhino document object until baked.

## Pattern - Script Body In Repo

When to use:

When a GH script component contains meaningful logic.

Logic:

```text
script body in scripts/grasshopper/<case>.cs
-> script component placed/wired through MCP
-> manual or future automated source assignment
-> graph validation
```

Acceptance:

- script body is version-controlled;
- inputs/outputs are clear;
- known RhinoCommon gotchas are avoided;
- no hidden chat-only code.

Failure modes:

- code exists only in the chat;
- source setter unavailable;
- script body uses ambiguous RhinoCommon APIs without local verification.

## Pattern - C# Script Node Preflight

When to use:

Every Grasshopper C# Script component task.

Read:

```text
docs/tools/grasshopper-csharp-script-nodes.md
```

Logic:

```text
detect Rhino/GH version
-> confirm units
-> choose modern C# Script vs legacy C# component
-> write GH_ScriptInstance-compatible code
-> store code in scripts/grasshopper/examples/
-> if automating source injection, prove IO after SetSource
```

Acceptance:

- C# 9.0-compatible script;
- `using Rhino;` included when `RhinoDoc` is used;
- output names are meaningful;
- script compiles when pasted into the target component;
- automated source injection is used only after IO names are inspected.

Failure modes:

- default `x/y/out/a` IO remains after `SetSource`;
- `Brep.CreateFromExtrusion` generated for Rhino 8 C#;
- `Extrusion.CreateExtrusion` typed as `Extrusion` without verification;
- script exists only in the chat and is lost after the session.

## Pattern - Rhino Source Curves To GH Graph

When to use:

Footprints, rails, contours, or selected Rhino geometry control the design.

Inputs needed:

- object ids;
- layer/color/name;
- bbox/area/length;
- units.

Logic:

```text
inspect source curves in Rhino
-> classify source authority
-> preserve curves
-> feed/reference them into GH logic
-> validate generated preview or baked geometry against source ids
```

Acceptance:

- source geometry is not deleted;
- generated geometry aligns with source;
- object ids are reported in handoff.
Failure modes:

- replacing source curves with guessed rectangles;
- losing units;
- baking floating geometry.
