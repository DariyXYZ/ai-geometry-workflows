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

For production work, avoid closing a user's active slot. Spawn a fresh slot for
Grasshopper smoke tests, or ask the user to close the stuck command manually.

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

Run `g1_start` on a fresh or idle slot, then place a tiny graph.

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

## GH-006 - Script Component Source Setter Missing

Symptom:

`C# Script` or `Python 3 Script` can be placed and wired, but no exposed MCP
tool can set the component's code body.

Cause:

Current g1 tool surface exposes placement/wiring/solve but not script-source
editing.

Correction:

Store paste-ready script bodies in `scripts/grasshopper/` and use them manually
or through a future reliable source-setting bridge.

Required gate:

When a script component matters, commit its script body to the repo.
## GH-007 - Ambiguous Duplicate Components

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
