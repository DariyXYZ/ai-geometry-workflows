# Grasshopper Case Index

This is the separate case branch for Grasshopper, RhinoMCP `g1_*`, C# Script
components, graph automation, plugin routing, and GH-specific failures.

Use this file only when the task involves Grasshopper as the working
environment. Do not load these cases for ordinary Rhino geometry construction
unless the Rhino task explicitly needs a Grasshopper definition, C# Script node,
or plugin-backed graph.

## Boundary

| Task type | Read this branch? | Reason |
| --- | --- | --- |
| Build geometry directly in Rhino/RhinoCommon | No | Use Rhino/reference/massing cases instead. |
| Generate a .3dm massing with RhinoMCP | No by default | GH automation rules are extra overhead. |
| Build or debug a Grasshopper graph | Yes | These cases preserve graph, component, and source-injection rules. |
| Write a GH C# Script component | Yes | C# Script IO/source behavior is a GH-specific risk. |
| Choose GH plugins or node stacks | Yes | Plugin/native/C# routing is part of this branch. |
| Validate a form operator before GH implementation | Maybe | Read only the relevant `AI Extraction Summary`. |

## Read Order

```text
docs/tools/grasshopper/grasshopper-workflow.md
-> docs/tools/grasshopper/grasshopper-csharp-script-nodes.md if writing C# Script
-> docs/errors/grasshopper/grasshopper-mcp-error-library.md
-> this index
-> one matching case's AI Extraction Summary
-> detailed case only if the tool route or failure gate matches
```

## Active Grasshopper Cases

| Case | Use when | Main rule | Read |
| --- | --- | --- | --- |
| Grasshopper MCP smoke 2026-06-22 | Starting GH automation through RhinoMCP | Fresh slot, capability scan, Construct Point smoke, manual place/wire before batching | `docs/cases/grasshopper/grasshopper-mcp-smoke-2026-06-22.md` |
| Grasshopper C# SetSource IO 2026-06-22 | Considering programmatic C# source assignment | `SetSource` accepting code is not enough; inspect IO and solve tiny script | `docs/cases/grasshopper/grasshopper-csharp-setsource-io-2026-06-22.md` |
| Grasshopper spiral skyscraper 2026-06-22 | Baseline tower in one C# Script node | One source-controlled C# Script node plus sliders is the fastest GH tower baseline | `docs/cases/grasshopper/grasshopper-spiral-skyscraper-2026-06-22.md` |
| Grasshopper voxel skyscraper 2026-06-22 | Controlled voxel tower / Pufferfish workflow | Use deterministic architectural mask, not `Populate 3D` randomness | `docs/cases/grasshopper/grasshopper-voxel-skyscraper-2026-06-22.md` |
| Grasshopper architecture snippets smoke 2026-06-23 | Testing massing/floor/core/TEP snippets | Validate RhinoCommon smoke first; paste-ready GH snippets after | `docs/cases/grasshopper/grasshopper-architecture-snippets-smoke-2026-06-23.md` |
| Grasshopper Pavilion 80hz lamella attractor 2026-06-26 | Pavilion lamellas, shingles, attractor logic | Store C# in repo; use manual paste/proven bridge; avoid unsafe source setters | `docs/cases/grasshopper/grasshopper-pavilion-80hz-lamella-attractor-2026-06-26.md` |

## Do Not Mix With Rhino Geometry Cases

Grasshopper cases answer these questions:

```text
how should a graph be built?
which GH component or plugin route is safe?
how should C# Script source be stored and inserted?
what GH/RhinoMCP failure must be avoided?
what outputs should a graph expose?
```

Rhino geometry cases answer different questions:

```text
what is the source authority?
what is the constructive geometry grammar?
which Rhino/RhinoCommon operation builds it?
what massing/form/operator should be used?
how is the .3dm scene validated?
```

If the current task is direct Rhino modeling, read `docs/case-library.md` and
Rhino/reference/massing cases instead of this file.

