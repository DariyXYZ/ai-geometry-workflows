# Library Index

This is the index of reusable architectural and geometry knowledge in the repo.
Use it to find strategies, patterns, modeling grammars, errors, source-repo
ideas, and tools without rereading every document.

## Scenario Strategy Library

| Library | Use when | File |
| --- | --- | --- |
| Scenario router | Choosing which workflow applies | `AI_NAVIGATOR.md`, `docs/task-read-maps.md` |
| Task read maps | Matching a concrete user task to the smallest read set | `docs/task-read-maps.md` |
| Case digest | Compact wins, failures, techniques, standards, and current decisions from cases | `docs/case-digest.md` |
| Repo knowledge boundary | Deciding what is shared repo memory vs local Obsidian research/capture | `docs/repo-knowledge-boundary.md` |
| Repo folder architecture | Deciding where durable docs, cases, errors, tools, libraries, research, and scripts belong | `docs/repo-folder-architecture.md` |
| Reference modeling gates | Building from references, plans, photos, underlays | `docs/workflows/rhino-reference/reference-modeling-gates.md` |
| TEP/massing subtypes | Splitting Scenario 3 into 3A/3B/3C/3D | `docs/workflows/massing/tep-massing-scenario-subtypes.md` |
| Architecture compliance check | Reviewing a building/massing against checklist criteria | `docs/workflows/massing/architecture-compliance-check.md` |
| Office / MФК concept checklist | IND internal checklist for office and МФК projects (15 sections, concept stage) | `docs/workflows/massing/office-mfc-checklist.md` |
| Moscow BC zoning patterns | Plot-plus-entries or site-zoning massing work | `docs/libraries/massing/moscow-bc-site-zoning-patterns.md` |
| Development direction matrix | Choosing which external repo ideas fit which vector | `docs/research/development-directions-repo-fit.md` |
| Experience capture format | Splitting cases into patterns, errors, metrics, prompts, decisions, and tool notes | `docs/experience-capture-format.md` |

## Pattern And Form Libraries

| Library | Contents | Status |
| --- | --- | --- |
| `docs/libraries/massing/moscow-bc-site-zoning-patterns.md` | Public spine, service edge, open-space types, buildable bands, tower anchors, BC/residential site zoning | Active |
| `docs/workflows/massing/tep-massing-scenario-subtypes.md` | 3A fixed zoning, 3B plot-plus-entries, 3C existing-massing image revision, 3D checklist review | Active |
| `docs/workflows/massing/architecture-compliance-check.md` | Rhino/MCP evidence collection and approval-risk review workflow | Active |
| `docs/libraries/massing/massing-decision-library.md` | Decision order from site context to CAD parameters; subtype routing, footprint families, risk checks | Active |
| `docs/libraries/massing/form-operator-library.md` | Reusable massing operators: chamfer, rotation, taper, setbacks, voids, podium/tower logic, crown moves | Active |
| `docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md` | Translation from architectural operators to Grasshopper section stacks, spines, attractors, facade nets, native nodes, and plugin nodes | Active |
| `docs/libraries/grasshopper/grasshopper-architecture-plugin-stack.md` | Research-backed routing matrix for GH architecture plugins, McNeel official sources, and task-specific stacks | Active |
| `docs/libraries/grasshopper/grasshopper-architecture-snippet-library.md` | Fast reusable GH/C# architecture snippets: floorization, TEP/metrics, smoke builder | Active |
| `docs/libraries/standards/moscow-building-dimensional-library-2026.md` | Moscow 2026 tower/building dimensional baselines: floors, cores, depths, slabs, roofs, openings, facade grids | Active |
| `docs/libraries/standards/moscow-building-dimensional-library-2026.yaml` | Machine-readable defaults and warning flags for Rhino/Grasshopper generators | Active |
| `docs/libraries/standards/moscow-massing-metric-quick-cards.md` | Fast task-facing metric cards for Moscow massing: office/residential defaults, road/fire access, TEP approximations, warning flags | Active |
| `docs/libraries/standards/moscow-road-dimensional-library-2026.md` | Moscow 2026 road/street/driveway CAD defaults: lane widths, carriageways, fire access, internal drives, visual modeling rules | Active |
| `docs/libraries/standards/moscow-architecture-approval-checklist.md` | Moscow architecture approval checklist criteria: visual image, urban frontage, permeability, parking | Active |
| `docs/libraries/massing/tep-calculation-patterns.md` | Active early-massing TEP/GFA/FAR/height/efficiency formulas, warnings, and Rhino/GH output contract | Active |
| `docs/workflows/rhino-reference/reference-modeling-gates.md` | Source authority, constructive grammar, section direction, massing-before-detail | Active |
| `docs/cases/rhino-geometry/bc50-two-tower-stylobate-2026-06-24.md` | Accepted two-tower BC massing precedent: contour roofs/parapets, transparent glass, 1 mm visual lifts, metric board, sunken courtyard bridge rules | Active |
| `docs/cases/grasshopper/README.md` | Separate Grasshopper case branch: GH graphs, C# Script, plugins, source injection, and MCP `g1_*` failures | Active |
| `docs/tools/grasshopper/grasshopper-workflow.md` | Grasshopper automation workflow through RhinoMCP: scan, smoke graph, build, validate | Active |
| `docs/tools/grasshopper/grasshopper-csharp-script-nodes.md` | C# Script node rules imported from local skill: GH_ScriptInstance shape, RhinoCommon gotchas, source-injection gates | Active |
| `docs/tools/grasshopper/grasshopper-csharp-performance.md` | C# Script automatic IO, list/tree access, parallel-safe patterns, caching, and performance gates | Active |
| `docs/libraries/grasshopper/grasshopper-pattern-library.md` | Reusable Grasshopper graph/script patterns and acceptance gates | Draft active |
| `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` | Case-derived rules for twist towers, shells, stepped towers, video replay | Active |
| `docs/cases/grasshopper/grasshopper-spiral-skyscraper-2026-06-22.md` | First reusable Grasshopper architecture C# Script node case: spiral skyscraper massing | Active |
| `docs/obsidian-knowledge-map.md` | Map of useful Obsidian research, tests, postmortems, and future imports | Active index |
| Obsidian project notes | Broader Moscow massing typologies, visual catalogs, source research, raw project memory | External canonical project memory |

Missing but desired future libraries:

- `docs/libraries/massing/site-planning-pattern-library.md` - reusable patterns across BC, ЖК,
  mixed-use, TPU, infill, campus.
- `docs/libraries/massing/massing-typology-catalog.md` - compact typology catalog from Moscow
  reference imagery and Obsidian visual research.

## Error And Anti-Pattern Library

| Library | Contents |
| --- | --- |
| `docs/error-ledger.md` | Global failure modes across scenarios |
| `docs/errors/massing/moscow-bc-massing-error-library.md` | Numeric-pass/site-fail, cut routes, box-only massing, accidental intersections |
| `docs/errors/grasshopper/grasshopper-mcp-error-library.md` | Grasshopper MCP automation failures: start timeout, missing document, generic batch errors, panel/source setter limits |
| `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` | Recent case-specific failures and promoted rules |
| `docs/libraries/standards/moscow-architecture-approval-checklist.md` | Approval checklist weak points and missing-evidence risks |
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

- `docs/case-digest.md`
- `docs/case-library.md`
- `docs/cases/rhino-geometry/recent-rhino-case-lessons.md`
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
| `docs/research/source-repos/README.md` | Index of local cards |
| `docs/research/source-repos/live-obj.md` | Semantic OBJ metadata, planning, anchors, patching ideas |
| `docs/research/source-repos/spellshape-three-format.md` | Expression/distribution ideas and `.spell` format concepts |
| `docs/research/source-repos/2d-plan-to-3d.md` | Plan/image to contour extraction ideas |
| `docs/research/source-repos/text-to-cad.md` | STEP-first CAD-as-code backend role |
| `docs/research/source-repos/rhinomcp.md` | Default McNeel RhinoMCP backend role |
| `docs/research/source-repos/mcneel-rhino-grasshopper-dev.md` | Official Rhino/GH developer docs, sample repos, Package Manager/Yak, Rhino.Inside.Revit |
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
| `docs/tools/rhino/rhino-mcp-backends.md` | Rhino backend policy: McNeel RhinoMCP by default; Aurox/other plugins only by request |
| `docs/tools/rhino/rhino-mcp-command-library.md` | RhinoMCP command cards: architectural intent -> Rhino/RhinoCommon operation sequence -> validation gates |
| `docs/tools/rhino/rhino-common-helper.md` | Legacy optional RhinoCommon helper path for backend-specific operations |
| `docs/tools/grasshopper/grasshopper-workflow.md` | Full Grasshopper MCP workflow: capability scan, smoke, graph strategy, validation |
| `docs/tools/grasshopper/grasshopper-csharp-script-nodes.md` | Grasshopper C# Script node workflow, C# 9 baseline, RhinoCommon gotchas, source-injection validation |
| `docs/tools/grasshopper/grasshopper-csharp-performance.md` | Performance and parallel rules for Grasshopper C# Script nodes |
| `docs/tools/grasshopper/grasshopper-mcp-smoke.md` | Grasshopper MCP capability scan and smoke graph workflow |
| `TOOLKIT.md` | CLI contract and commands |
| `ai_geometry_toolkit/` | Runnable orchestration code |
| `tests/` | Unit tests and fixtures |

## Data And Context Maps

| File | Purpose |
| --- | --- |
| `docs/obsidian-knowledge-map.md` | Obsidian research, tests, errors, and import backlog |
| `docs/context-system.md` | Where to save project context, cases, errors, decisions |
| `docs/experience-capture-format.md` | How to promote session experience into reusable repo knowledge |
| `docs/repo-knowledge-boundary.md` | What gets promoted from Obsidian into the shared GitHub repo |
| `docs/repo-folder-architecture.md` | Folder ownership rules for the shared GitHub repo |
| `docs/project-data-map.md` | Active data and source locations |
| `docs/repository-map.md` | Repo structure and scenario read sets |
| `docs/development-state.md` | Current technical state and roadmap |

## How To Add A New Library Entry

1. Decide the type: strategy, pattern, case, error, decision, source card, tool.
2. Add or update the smallest matching file.
3. Add an index entry here if it should be discoverable.
4. Add a short `NEWS.md` entry only if an audit trail is useful; do not rely on
   `NEWS.md` as the only place for a future-behavior rule.
5. If the rule came from a project session, also update the relevant handoff or
   case note.

## Target Information Architecture

Current repo files are organized by role:

```text
AI_NAVIGATOR.md          first AI entry and reading hierarchy
AGENTS.md               compact non-negotiable agent rules
docs/
  task-read-maps.md     concrete task -> smallest read set
  START_HERE.md         human onboarding, not default AI context
  repository-map.md     file/folder locator
  library-index.md      library catalog
  case-digest.md        compact case/error/metric memory
  case-library.md       full case index
  workflows/            stage gates and task processes
  libraries/            reusable metrics, operators, standards
  cases/                concrete session results
  errors/               failure libraries
  research/             source cards and external repo memory
  tools/                RhinoMCP/GH command and backend docs
decisions/              accepted dated tradeoffs
scripts/                reusable promoted scripts
tests/                  unit tests and fixtures
```

Do not move files into this structure casually. First add indexes and stable
links. Move only when the existing docs have become clearly too large or too
mixed.
