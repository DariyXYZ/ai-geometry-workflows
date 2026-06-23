# Library Index

This is the index of reusable architectural and geometry knowledge in the repo.
Use it to find strategies, patterns, modeling grammars, errors, source-repo
ideas, and tools without rereading every document.

## Scenario Strategy Library

| Library | Use when | File |
| --- | --- | --- |
| Scenario router | Choosing which workflow applies | `docs/START_HERE.md` |
| Reference modeling gates | Building from references, plans, photos, underlays | `docs/scenarios/reference-modeling-gates.md` |
| TEP/massing subtypes | Splitting Scenario 3 into 3A/3B/3C/3D | `docs/scenarios/tep-massing-scenario-subtypes.md` |
| Architecture compliance check | Reviewing a building/massing against checklist criteria | `docs/scenarios/architecture-compliance-check.md` |
| Moscow BC zoning patterns | Plot-plus-entries or site-zoning massing work | `docs/libraries/moscow-bc-site-zoning-patterns.md` |
| Development direction matrix | Choosing which external repo ideas fit which vector | `docs/research/development-directions-repo-fit.md` |

## Pattern And Form Libraries

| Library | Contents | Status |
| --- | --- | --- |
| `docs/libraries/moscow-bc-site-zoning-patterns.md` | Public spine, service edge, open-space types, buildable bands, tower anchors, BC/residential site zoning | Active |
| `docs/scenarios/tep-massing-scenario-subtypes.md` | 3A fixed zoning, 3B plot-plus-entries, 3C existing-massing image revision, 3D checklist review | Active |
| `docs/scenarios/architecture-compliance-check.md` | Rhino/MCP evidence collection and approval-risk review workflow | Active |
| `docs/libraries/massing-decision-library.md` | Decision order from site context to CAD parameters; subtype routing, footprint families, risk checks | Active |
| `docs/libraries/form-operator-library.md` | Reusable massing operators: chamfer, rotation, taper, setbacks, voids, podium/tower logic, crown moves | Active |
| `docs/libraries/grasshopper-architectural-form-patterns.md` | Translation from architectural operators to Grasshopper section stacks, spines, attractors, facade nets, native nodes, and plugin nodes | Active |
| `docs/libraries/grasshopper-architecture-plugin-stack.md` | Research-backed routing matrix for GH architecture plugins, McNeel official sources, and task-specific stacks | Active |
| `docs/libraries/moscow-architecture-approval-checklist.md` | Moscow architecture approval checklist criteria: visual image, urban frontage, permeability, parking | Active |
| `docs/scenarios/reference-modeling-gates.md` | Source authority, constructive grammar, section direction, massing-before-detail | Active |
| `docs/tools/grasshopper-workflow.md` | Grasshopper automation workflow through RhinoMCP: scan, smoke graph, build, validate | Active |
| `docs/tools/grasshopper-csharp-script-nodes.md` | C# Script node rules imported from local skill: GH_ScriptInstance shape, RhinoCommon gotchas, source-injection gates | Active |
| `docs/tools/grasshopper-csharp-performance.md` | C# Script automatic IO, list/tree access, parallel-safe patterns, caching, and performance gates | Active |
| `docs/libraries/grasshopper-pattern-library.md` | Reusable Grasshopper graph/script patterns and acceptance gates | Draft active |
| `docs/cases/recent-rhino-case-lessons.md` | Case-derived rules for twist towers, shells, stepped towers, video replay | Active |
| `docs/cases/grasshopper-spiral-skyscraper-2026-06-22.md` | First reusable Grasshopper architecture C# Script node case: spiral skyscraper massing | Active |
| `docs/obsidian-knowledge-map.md` | Map of useful Obsidian research, tests, postmortems, and future imports | Active index |
| Obsidian project notes | Broader Moscow massing typologies, visual catalogs, source research, raw project memory | External canonical project memory |

Missing but desired future libraries:

- `docs/site-planning-pattern-library.md` - reusable patterns across BC, ЖК,
  mixed-use, TPU, infill, campus.
- `docs/tep-calculation-patterns.md` - floor modules, GFA/FAR strategies,
  podium/tower TEP balancing.
- `docs/massing-typology-catalog.md` - compact typology catalog from Moscow
  reference imagery and Obsidian visual research.

## Error And Anti-Pattern Library

| Library | Contents |
| --- | --- |
| `docs/error-ledger.md` | Global failure modes across scenarios |
| `docs/errors/moscow-bc-massing-error-library.md` | Numeric-pass/site-fail, cut routes, box-only massing, accidental intersections |
| `docs/errors/grasshopper-mcp-error-library.md` | Grasshopper MCP automation failures: start timeout, missing document, generic batch errors, panel/source setter limits |
| `docs/cases/recent-rhino-case-lessons.md` | Recent case-specific failures and promoted rules |
| `docs/libraries/moscow-architecture-approval-checklist.md` | Approval checklist weak points and missing-evidence risks |
| `decisions/` | Accepted tradeoffs that prevent old mistakes |

Use this shape for new errors:

```text
error code/title
-> symptom
-> cause
-> detection
-> correction
-> required gate
```

## Case Library

Start with:

- `docs/case-library.md`
- `docs/cases/recent-rhino-case-lessons.md`
- `decisions/`

Case categories:

- successful enough to reuse;
- medium-success with gates failed;
- failed and promoted to error rule;
- source-authority correction;
- workflow/tooling case.

## Source-Repo Memory

Do not start by opening external GitHub repositories. Read the local source
cards first.

| Source card | What it contributes |
| --- | --- |
| `docs/source-repos/README.md` | Index of local cards |
| `docs/source-repos/live-obj.md` | Semantic OBJ metadata, planning, anchors, patching ideas |
| `docs/source-repos/spellshape-three-format.md` | Expression/distribution ideas and `.spell` format concepts |
| `docs/source-repos/2d-plan-to-3d.md` | Plan/image to contour extraction ideas |
| `docs/source-repos/text-to-cad.md` | STEP-first CAD-as-code backend role |
| `docs/source-repos/rhinomcp.md` | Default McNeel RhinoMCP backend role |
| `docs/source-repos/mcneel-rhino-grasshopper-dev.md` | Official Rhino/GH developer docs, sample repos, Package Manager/Yak, Rhino.Inside.Revit |
| `docs/research/external-repo-constructor-map.md` | Long-form external repo map |

Rule:

```text
local source card
-> external repo only if implementation detail is missing
-> update source card after learning something durable
```

## Tool And Backend Library

| Tooling note | Purpose |
| --- | --- |
| `docs/tools/rhino-mcp-backends.md` | Rhino backend policy: McNeel RhinoMCP by default; Aurox/other plugins only by request |
| `docs/tools/rhino-common-helper.md` | Native RhinoCommon helper path for backend-specific operations |
| `docs/tools/grasshopper-workflow.md` | Full Grasshopper MCP workflow: capability scan, smoke, graph strategy, validation |
| `docs/tools/grasshopper-csharp-script-nodes.md` | Grasshopper C# Script node workflow, C# 9 baseline, RhinoCommon gotchas, source-injection validation |
| `docs/tools/grasshopper-csharp-performance.md` | Performance and parallel rules for Grasshopper C# Script nodes |
| `docs/tools/grasshopper-mcp-smoke.md` | Grasshopper MCP capability scan and smoke graph workflow |
| `TOOLKIT.md` | CLI contract and commands |
| `ai_geometry_toolkit/` | Runnable orchestration code |
| `tests/` | Unit tests and fixtures |

## Data And Context Maps

| File | Purpose |
| --- | --- |
| `docs/obsidian-knowledge-map.md` | Obsidian research, tests, errors, and import backlog |
| `docs/context-system.md` | Where to save project context, cases, errors, decisions |
| `docs/project-data-map.md` | Active data and source locations |
| `docs/repository-map.md` | Repo structure and scenario read sets |
| `docs/development-state.md` | Current technical state and roadmap |

## How To Add A New Library Entry

1. Decide the type: strategy, pattern, case, error, decision, source card, tool.
2. Add or update the smallest matching file.
3. Add an index entry here if it should be discoverable.
4. Add a short `NEWS.md` entry if it changes future behavior.
5. If the rule came from a project session, also update the relevant handoff or
   case note.

## Target Information Architecture

Current repo files are still partly historical. The intended long-term shape is:

```text
AI_NAVIGATOR.md
docs/
  START_HERE.md
  repository-map.md
  library-index.md
  case-library.md
  error-ledger.md
  repo-maintenance-guide.md
  scenarios/
  patterns/
  cases/
  errors/
  source-repos/
  tools/
decisions/
scripts/
  <domain>/
tests/
```

Do not move files into this structure casually. First add indexes and stable
links. Move only when the existing docs have become clearly too large or too
mixed.
