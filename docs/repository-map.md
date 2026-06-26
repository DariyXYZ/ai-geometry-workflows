# Repository Map

This file tells a new user or AI agent what to read and what to ignore.

## Read First

| File | Purpose |
| --- | --- |
| `AI_NAVIGATOR.md` | Portable first page for any AI agent using this repo as architecture/geometry memory. |
| `AGENTS.md` | Minimal agent instructions and non-negotiable rules. |
| `docs/START_HERE.md` | Main loading path for fresh chats and new computers. |
| `docs/task-read-maps.md` | Task-to-read-set router for AI agents using the repo as a skill. |
| `docs/case-digest.md` | Compact wins, errors, techniques, standards, and current case-derived decisions. |
| `docs/repo-knowledge-boundary.md` | Boundary between shared repo knowledge and local Obsidian research/capture. |
| `docs/repo-folder-architecture.md` | Folder ownership rules that keep Rhino, Grasshopper, massing, standards, tools, and research separated. |
| `NEWS.md` | Chronological project memory, newest entries first. |
| `README.md` | Project overview and runnable CLI commands. |
| `docs/development-state.md` | Current technical state and next engineering steps. |

## Workflow Rules

| File | Purpose |
| --- | --- |
| `docs/workflows/rhino-reference/reference-modeling-gates.md` | Scenario 1 gates: source authority, constructive grammar, missing views, geometry. |
| `docs/library-index.md` | Index of strategy, pattern, source-repo, tool, and data libraries. |
| `docs/case-library.md` | Index of successful, partial, failed, source-correction, and tooling cases. |
| `docs/obsidian-knowledge-map.md` | Map of useful Obsidian research, tests, errors, decisions, and import backlog. |
| `docs/error-ledger.md` | Known failure modes and fixes. |
| `docs/workflows/massing/tep-massing-scenario-subtypes.md` | Scenario 3 split into 3A fixed zoning, 3B plot-plus-entries zoning proposal, 3C existing-massing image/form revision, and 3D checklist review. |
| `docs/workflows/massing/architecture-compliance-check.md` | Scenario 3D workflow for Rhino evidence collection and architecture approval checklist review. |
| `docs/libraries/massing/massing-decision-library.md` | Scenario 3 massing decision order, footprint families, massing families, risk checks, and generator output schema. |
| `docs/libraries/massing/form-operator-library.md` | Reusable form operators for early massing: chamfer, rotation, rounding, setbacks, voids, taper, podium/tower logic. |
| `docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md` | Bridge from architectural massing/form operators to Grasshopper control geometry, native nodes, plugin nodes, and validation gates. |
| `docs/libraries/grasshopper/grasshopper-architecture-plugin-stack.md` | Routing matrix for choosing GH native nodes, C# Script, RhinoCommon, and architecture plugins. |
| `docs/libraries/grasshopper/grasshopper-architecture-snippet-library.md` | Fast reusable architecture snippets for floorization, TEP/metrics, and smoke tests. |
| `docs/libraries/standards/moscow-building-dimensional-library-2026.md` | Moscow 2026 dimensional baseline for tower floors, cores, facade depths, slabs, roofs, openings, and facade grids. |
| `docs/libraries/standards/moscow-architecture-approval-checklist.md` | Compact checklist criteria from the 2026-06-13 DGP architecture evaluation PDF. |
| `docs/errors/massing/moscow-bc-massing-error-library.md` | Moscow BC massing failure modes: site fail despite numeric pass, cut routes, box-only variants, accidental intersections. |
| `docs/libraries/massing/moscow-bc-site-zoning-patterns.md` | Zoning patterns and pre-geometry gates for BC/residential massing: public spine, service edge, buildable bands, height anchors. |
| `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` | Recent Rhino/RhinoMCP case results, video replay scripts, and fresh modeling rules. |
| `docs/cases/grasshopper/README.md` | Separate Grasshopper case branch for GH graphs, C# Script, plugins, and `g1_*` automation. |
| `docs/context-system.md` | Where to store decisions, cases, reports, and temporary work. |
| `docs/experience-capture-format.md` | Standard format for turning cases into patterns, errors, metrics, prompts, decisions, and tool notes. |
| `docs/repo-knowledge-boundary.md` | Promotion gate for deciding what belongs in GitHub and what remains local in Obsidian. |
| `docs/repo-folder-architecture.md` | Source of truth for where new docs, cases, errors, tools, libraries, research notes, and scripts belong. |
| `docs/repo-maintenance-guide.md` | How to add reusable strategies, patterns, cases, errors, and source findings without clutter. |
| `docs/project-data-map.md` | Where source data and related repos live. |
| `docs/tools/rhino/rhino-mcp-backends.md` | Rhino backend policy: McNeel RhinoMCP default, optional plugin backends by request. |
| `docs/tools/rhino/rhino-common-helper.md` | Native RhinoCommon helper layer for backend-specific RhinoCommon execution. |
| `docs/tools/grasshopper/grasshopper-workflow.md` | Grasshopper MCP workflow for capability scan, smoke graph, build order, and validation. |
| `docs/tools/grasshopper/grasshopper-csharp-script-nodes.md` | Grasshopper C# Script node rules, RhinoCommon gotchas, and source-injection gates. |
| `docs/tools/grasshopper/grasshopper-csharp-performance.md` | Automatic IO, list/tree access, parallel-safe loops, caching, and performance gates for GH C# Script nodes. |
| `docs/errors/grasshopper/grasshopper-mcp-error-library.md` | Known Grasshopper MCP automation failure modes and fixes. |
| `decisions/` | Dated accepted decisions. Read relevant files only. |

## External Repo Library

| File | Purpose |
| --- | --- |
| `docs/research/source-repos/README.md` | Index of external repositories and what they contribute. |
| `docs/research/source-repos/live-obj.md` | Semantic OBJ metadata, planner, patching, Grasshopper/Rhino ideas. |
| `docs/research/source-repos/2d-plan-to-3d.md` | Plan/image to contour extraction pattern. |
| `docs/research/source-repos/spellshape-three-format.md` | Expression, distribution, and `.spell` ideas. |
| `docs/research/source-repos/text-to-cad.md` | STEP-first build123d backend role. |
| `docs/research/source-repos/mcneel-rhino-grasshopper-dev.md` | Official McNeel developer docs, samples, Package Manager/Yak, and Rhino.Inside.Revit source map. |
| `docs/research/external-repo-constructor-map.md` | Long-form external repo map. |
| `docs/research/development-directions-repo-fit.md` | Which repo pieces fit which product vector. |

## Runnable Code

| Path | Purpose |
| --- | --- |
| `ai_geometry_toolkit/` | Case-based CLI and orchestration code. |
| `tests/` | Unit tests and fixtures. |
| `scripts/` | Utility scripts when promoted out of experiments, including RhinoCommon helpers. |
| `TOOLKIT.md` | CLI contract and command notes. |

## Usually Do Not Read First

| Path | Why |
| --- | --- |
| `.tmp_cases/` | Local ignored experiments; useful only when the user names a specific run. |
| `archive/reports/ai-geometry-research.html`, `archive/reports/index.html` | Report/presentation outputs, not primary working memory. |
| Old team updates | Useful for history, but `NEWS.md` and `development-state.md` are faster. |

## Scenario Read Sets

### Reference To Model

Read:

- `docs/START_HERE.md`
- `docs/workflows/rhino-reference/reference-modeling-gates.md`
- `docs/error-ledger.md`
- `docs/cases/rhino-geometry/recent-rhino-case-lessons.md`
- `decisions/2026-05-28-constructive-grammar-before-reference-modeling.md`
- `decisions/2026-06-01-grove-contour-derived-floor-plates.md`

Optional:

- `docs/research/source-repos/live-obj.md`
- `docs/research/source-repos/2d-plan-to-3d.md`

### Complex Model Cleanup

Read:

- `docs/development-state.md`
- `docs/error-ledger.md`
- `docs/context-system.md`
- `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`
- `decisions/2026-05-20-nurbs-restart-from-named-rails.md`

### Massing And Revisions

Read:

- `docs/workflows/massing/tep-massing-scenario-subtypes.md`
- `docs/workflows/massing/architecture-compliance-check.md`
- `docs/libraries/standards/moscow-architecture-approval-checklist.md`
- `docs/libraries/massing/form-operator-library.md`
- `docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md` if Grasshopper will build or iterate the form
- `docs/libraries/grasshopper/grasshopper-architecture-plugin-stack.md` if plugin/native/C# stack choice matters
- `docs/libraries/grasshopper/grasshopper-architecture-snippet-library.md` for quick floorization, metrics, and TEP snippets
- `docs/libraries/standards/moscow-building-dimensional-library-2026.md` before choosing floor heights, core size, facade-to-core depth, slab/package, roof, or window/facade module assumptions
- `docs/errors/massing/moscow-bc-massing-error-library.md`
- `docs/libraries/massing/moscow-bc-site-zoning-patterns.md`
- `docs/development-state.md`
- `docs/research/development-directions-repo-fit.md`
- `docs/research/source-repos/live-obj.md`
- `docs/research/source-repos/spellshape-three-format.md`

### Grasshopper Automation

Read:

- `docs/tools/grasshopper/grasshopper-workflow.md`
- `docs/cases/grasshopper/README.md`
- `docs/tools/grasshopper/grasshopper-csharp-script-nodes.md` when writing C# Script nodes
- `docs/tools/grasshopper/grasshopper-csharp-performance.md` when writing large, automatic-IO, cached, or parallel C# Script nodes
- `docs/tools/grasshopper/grasshopper-mcp-smoke.md`
- `docs/libraries/grasshopper/grasshopper-pattern-library.md`
- `docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md` for building-form and facade-graph tasks
- `docs/libraries/grasshopper/grasshopper-architecture-plugin-stack.md` for choosing plugins and bundled workflows
- `docs/libraries/grasshopper/grasshopper-architecture-snippet-library.md` for reusable quick architecture C# snippets
- `docs/errors/grasshopper/grasshopper-mcp-error-library.md`

## Rule For Future Agents

Prefer the smallest read set that matches the task. Do not load the whole
repository by default. If a task changes the workflow, update the matching rule
file before finishing.
