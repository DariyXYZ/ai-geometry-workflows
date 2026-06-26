# Grasshopper MCP Smoke - 2026-06-22

Status: tooling / accepted smoke.

Scenario:

Grasshopper automation through standard RhinoMCP.

## AI Extraction Summary

```yaml
case_family: grasshopper
use_when: "starting or debugging Grasshopper automation through RhinoMCP"
source_authority: "fresh-slot MCP smoke test with component search/place/wire/solve"
geometry_grammar: "tooling case; no architectural grammar"
effective_rhino_gh_route: "fresh Rhino slot -> run_python capability scan -> g1_start -> component search -> manual place/wire -> solve"
key_parameters:
  fresh_slot: "armadillo"
  first_preview_component: "Construct Point"
  avoid_first_preview: "Panel"
promoted_rules:
  - "use a fresh slot for GH smoke when active scene matters"
  - "capability scan before graph building"
  - "manual place/wire before batching with g1_apply_graph"
  - "store script bodies in repo until source setter exists"
failure_gates:
  - "used slot may leave Rhino command-busy after g1_start timeout"
  - "g1_apply_graph generic errors hide useful diagnostics"
  - "GH preview geometry may not appear in Rhino document-object capture"
validation: "component search finds Script/A+B/Construct Point; sliders wire; g1_solve_graph returns Success"
read_more_when: "opening GH through MCP, choosing smoke graph, or diagnosing g1 workflow failures"
related_scripts: []
```

Goal:

Prove a fast, repeatable workflow for inspecting Rhino/GH capabilities, opening
Grasshopper, placing components, wiring sliders, and solving.

What worked:

- Fresh Rhino slot `armadillo` avoided interfering with the active modeling
  scene.
- Rhino version and document state were readable through `run_python`.
- `g1_start` opened Grasshopper successfully on a fresh slot.
- `g1_search_components` found `Python 3 Script`, `C# Script`, `A+B`,
  `Construct Point`, and related components.
- Sliders, `Construct Point`, and `C# Script` components could be placed.
- Sliders wired correctly into `Construct Point` and `C# Script`.
- `g1_solve_graph` returned `Success`.

What failed or was limited:

- On the already-used `aardvark` slot, `g1_start` timed out and left Rhino in a
  command-busy state.
- `g1_apply_graph` returned a generic error; manual placement/wiring gave
  better diagnostics.
- Wiring to `Panel` failed because it behaved as a value source.
- No dedicated tool was exposed for setting script component source code.
- GH preview geometry was not visible to Rhino document-object viewport capture.

Promoted rules:

- Use a fresh slot for GH smoke if the active Rhino scene matters.
- Always run capability scan before building a GH graph.
- Use `Construct Point` as the first smoke preview, not `Panel`.
- Place/wire manually before batching with `g1_apply_graph`.
- Store script component bodies in the repo until a reliable source setter
  exists.

Reusable workflow:

See:

- `docs/tools/grasshopper-workflow.md`
- `docs/tools/grasshopper-mcp-smoke.md`
- `docs/errors/grasshopper-mcp-error-library.md`
- `docs/libraries/grasshopper-pattern-library.md`
