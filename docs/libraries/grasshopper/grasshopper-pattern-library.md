# Grasshopper Pattern Library

Status: draft active library.

Reusable patterns for fast Grasshopper work through RhinoMCP.

For building-form tasks, read the architectural bridge first:

```text
docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md
docs/libraries/grasshopper/grasshopper-architecture-plugin-stack.md
docs/libraries/grasshopper/grasshopper-architecture-snippet-library.md
```

It maps Scenario 3 form operators into Grasshopper control geometry, node
families, plugin nodes, and validation gates.

Use the plugin stack when the task requires choosing between native GH nodes,
C# Script/RhinoCommon, and plugins such as Ladybug, Kangaroo, Karamba3D,
Elefront, Human, Pufferfish, PanelingTools, LunchBox, Rhino.Inside.Revit,
VisualARQ, ShapeDiver, or Speckle.

Use the snippet library when the task needs quick reusable C# pieces such as
floorization, gabarits, TEP/GFA/FAR metrics, or smoke-test geometry.

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
-> if empty, ask the user to run MCPStart in Rhino (GH-010)
-> run_python version/units/object_count
-> get_commands Grasshopper/Script/Python
-> component lookup via run_python or documented GUIDs (NOT g1_search_components
   on an adopted slot; it crashes Rhino, GH-009)
-> confirm Grasshopper is open, or ask the user to open it manually
-> validate C# logic via run_csharp before manual paste
```

Acceptance:

- Rhino version known;
- units known;
- required component GUIDs known;
- smoke graph solves.

Failure modes:

- no Rhino slot because `MCPStart` was not run;
- `g1_search_components` crashing an adopted slot (GH-009);
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
docs/tools/grasshopper/grasshopper-csharp-script-nodes.md
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

## Pattern - One C# Node Plus Sliders For Tower Massing

When to use:

Parametric tower blockouts, early massing, and geometry cases where a component
graph would need many repeated wires.

Example:

```text
docs/cases/grasshopper/grasshopper-spiral-skyscraper-2026-06-22.md
scripts/grasshopper/examples/spiral_tower_csharp.cs
```

Logic:

```text
sliders define design parameters
-> one C# Script node generates primary massing geometry
-> outputs expose solids, guide curves, and Info
-> optional downstream nodes handle facade/detail/metrics
```

Acceptance:

- all meaningful logic is in a source-controlled script;
- slider ranges are documented;
- units and design metrics are reported;
- output count is controlled;
- bake/detail is deferred until preview passes.

Failure modes:

- replacing a compact script with a large fragile wire graph;
- baking before preview validation;
- mixing massing, facade, and metrics in one unreviewable node;
- losing the script body inside a Grasshopper file.

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

## Pattern - Architectural Operator To GH Graph

When to use:

Building form, massing, facade-line, tower, podium, shell, or SubD/Brep
generation in Grasshopper.

Read:

```text
docs/libraries/massing/form-operator-library.md
docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md
```

Logic:

```text
choose architectural operator
-> declare why it belongs on the site or building
-> choose control geometry: section stack, spine, rails, attractor, or surface
-> build node graph from simple curves to preview massing
-> add facade net only after form is accepted
-> record the pattern if it becomes reusable
```

Acceptance:

- operator has a site, TEP, view, movement, or image reason;
- node graph exposes meaningful parameters;
- primary massing is visible before facade/detail;
- plugin nodes support the pattern instead of defining it;
- validation checks height, footprint, silhouette, and source authority.

Failure modes:

- starting from plugin components without an architectural reason;
- hiding a requested node graph inside one script node;
- adding dense facade pipes before line preview is approved;
- baking geometry before the Grasshopper preview passes.
