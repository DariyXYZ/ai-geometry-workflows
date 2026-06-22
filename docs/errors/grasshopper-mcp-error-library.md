# Grasshopper MCP Error Library

Status: active.

This file records failure modes observed or expected when automating
Grasshopper through RhinoMCP.

## GH-001 - `g1_start` Timeout Does Not Prove Failure

Symptom:

`g1_start` times out after a long wait.

Cause:

Grasshopper may still be loading, or Rhino may have a command queue state that
does not return cleanly to MCP.

Detection:

Run `g1_search_components` after the timeout. If component search works,
Grasshopper may be loaded even though `g1_start` timed out.

Correction:

For production work, avoid closing or spawning slots unless the user explicitly
asks for it. Ask the user to open Grasshopper manually, then reconnect with
`MCPConnect` if needed.

Required gate:

Never proceed from `g1_start` timeout directly to a large graph. Run component
search and a tiny smoke placement first.

## GH-002 - Component Search Can Work Without An Active GH Document

Symptom:

`g1_search_components` returns components, but `g1_place_component` returns:

```text
Could not get or create GH document
```

Cause:

The Grasshopper component library is available, but no active canvas/document
exists.

Correction:

Ask the user to open Grasshopper manually in the connected Rhino slot, then
place a tiny graph.

Required gate:

Do not treat component search as proof that a canvas exists.

## GH-003 - `g1_apply_graph` Generic Failure

Symptom:

`g1_apply_graph` returns only:

```text
An error occurred invoking 'g1_apply_graph'.
```

Cause:

The batch call hides which step failed.

Correction:

Place sliders and components one by one, then wire one connection at a time.

Required gate:

Use `g1_apply_graph` only after the same graph has been proven manually, or for
simple repeatable graphs with known selectors.

## GH-004 - `Panel` Can Behave As A Value Source

Symptom:

Wiring to `Panel` fails with:

```text
destination '' is a value source, not an input
```

Cause:

The MCP selector semantics can treat Panel as a parameter/value source rather
than a standard component input.

Correction:

For first smoke tests, avoid Panel. Use visible preview geometry such as
`Construct Point`.

Required gate:

Do not use Panel as the only proof that solve worked.

## GH-005 - GH Preview Is Not A Rhino Document Object

Symptom:

`g1_solve_graph` succeeds, but Rhino viewport capture reports an empty document.

Cause:

Grasshopper preview geometry is not baked into the Rhino document.

Correction:

Validate solve success through `g1_solve_graph`, component outputs where
available, or bake/reference workflow when document geometry is required.

Required gate:

Do not mistake empty Rhino document object count for failed GH preview.

## GH-006 - Direct `g1_*` Script Source Setter Missing

Symptom:

`C# Script` or `Python 3 Script` can be placed and wired, but no exposed MCP
`g1_*` tool can set the component's code body.

Cause:

Current g1 tool surface exposes placement/wiring/solve but not script-source
editing. Source editing may still be available indirectly through the
Grasshopper .NET API.

Correction:

Store paste-ready script bodies in `scripts/grasshopper/` and use them manually
or through a proven source-setting bridge.

Required gate:

When a script component matters, commit its script body to the repo.

## GH-007 - Programmatic `SetSource` Can Keep Wrong IO

Symptom:

The Rhino 8 C# Script component accepts source through `SetSource(string)`, but
the component still shows default inputs/outputs such as:

```text
x
y
out
a
```

and `TryGetSource` shows that `RunScript(...)` has been rewritten to the
default signature.

Cause:

Programmatic source assignment into
`RhinoCodePluginGH.Components.CSharpComponent` is not equivalent to manually
pasting a classic `GH_ScriptInstance` script into the component editor. The
component may preserve the existing IO contract unless its expected source
format and parameter update path are proven.

Detection:

After `SetSource(...)`, inspect:

```text
TryGetSource
Params.Input
Params.Output
```

Do not rely on `SetSource` returning without error.

Correction:

Use `docs/tools/grasshopper-csharp-script-nodes.md`. Keep the code as a
paste-ready script in `scripts/grasshopper/examples/`, or use a legacy/dedicated
component route only after a tiny source-and-IO smoke test succeeds.

Required gate:

For any automated source injection, prove this sequence first:

```text
SetSource
-> SetParametersFromScript
-> inspect IO names
-> solve tiny script
```

If the IO names are wrong, stop before building the production graph.

## GH-008 - Ambiguous Duplicate Components

Symptom:

A search returns multiple components with the same display name, for example
`Addition`.

Cause:

Grasshopper has category-specific components with identical names.

Correction:

Use GUID selectors from `g1_search_components`, not names, once the exact
component has been identified.

Required gate:

For reusable graph builders, store GUIDs and the component category/subcategory
in comments or config.
