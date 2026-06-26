# Task Read Maps

This file is the fast router for an AI agent using the repository as a skill.
Start here after `AI_NAVIGATOR.md` when the user asks for a concrete geometry,
massing, Rhino, Grasshopper, or analysis task.

Do not read everything. Pick the closest task, load the required files, inspect
the active Rhino/Grasshopper/source context if relevant, then act.

## Universal Load

Always read:

1. `AI_NAVIGATOR.md`
2. `docs/task-read-maps.md`
3. `docs/case-digest.md`
4. `docs/repository-map.md`
5. The task-specific row below

Then read case files only when the task resembles that case.

## Task Matrix

| User task | Scenario | Required read set | Useful libraries | Output discipline |
| --- | --- | --- | --- | --- |
| Build from photo, plan, facade, reference, or text | Scenario 1 | `docs/workflows/rhino-reference/reference-modeling-gates.md`, `docs/error-ledger.md`, `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` | `docs/research/source-repos/2d-plan-to-3d.md`, `docs/research/source-repos/live-obj.md` | State source authority and constructive grammar before geometry |
| Make second variant from an existing massing | Scenario 3C | `docs/workflows/massing/tep-massing-scenario-subtypes.md`, `docs/libraries/massing/massing-decision-library.md`, source case note if present | `docs/libraries/massing/form-operator-library.md`, `docs/libraries/standards/moscow-building-dimensional-library-2026.md`, `docs/errors/massing/moscow-bc-massing-error-library.md` | Preserve source gabarit/TEP scale; describe deltas from variant 1 |
| Generate first massing from plot and entries only | Scenario 3B | `docs/workflows/massing/tep-massing-scenario-subtypes.md`, `docs/libraries/massing/moscow-bc-site-zoning-patterns.md` | `docs/libraries/massing/massing-decision-library.md`, `docs/libraries/standards/moscow-road-dimensional-library-2026.md`, `docs/libraries/massing/form-operator-library.md` | Propose zoning/public spine before expressive form |
| Build form on given footprints/zoning | Scenario 3A | `docs/workflows/massing/tep-massing-scenario-subtypes.md`, given source notes, `docs/libraries/massing/form-operator-library.md` | `docs/libraries/standards/moscow-building-dimensional-library-2026.md`, `docs/libraries/massing/massing-decision-library.md` | Do not move approved footprints/entries unless asked |
| Review massing/building against approval checklist | Scenario 3D | `docs/workflows/massing/architecture-compliance-check.md`, `docs/libraries/standards/moscow-architecture-approval-checklist.md` | `docs/libraries/standards/moscow-building-dimensional-library-2026.md`, `docs/error-ledger.md` | Collect Rhino/view evidence before scoring or redesigning |
| Clean complex Rhino model for analysis | Scenario 2 | `docs/development-state.md`, `docs/error-ledger.md`, `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`, `decisions/2026-05-20-nurbs-restart-from-named-rails.md` | `docs/context-system.md`, `docs/tools/rhino/rhino-mcp-backends.md` | Preserve source; classify parts; validate sections, not only watertightness |
| Build or test Grasshopper graph | Grasshopper branch | `docs/tools/grasshopper/grasshopper-workflow.md`, `docs/tools/grasshopper/grasshopper-mcp-smoke.md`, `docs/cases/grasshopper/README.md` | `docs/tools/grasshopper/grasshopper-csharp-script-nodes.md`, `docs/tools/grasshopper/grasshopper-csharp-performance.md`, `docs/libraries/grasshopper/grasshopper-pattern-library.md` | Smoke-test small graph first; store script bodies in repo; do not read Rhino geometry cases unless the form grammar matches |
| Choose Rhino backend or run RhinoMCP | Tooling | `docs/tools/rhino/rhino-mcp-backends.md`, `docs/research/source-repos/rhinomcp.md` | `TOOLKIT.md`, `scripts/README.md` | Use McNeel RhinoMCP by default; scan capabilities before build |
| Reuse an existing successful or failed case | Case work | `docs/case-library.md`, matching `docs/cases/*.md` or `decisions/*.md` | matching error and pattern libraries | Promote only the reusable rule, not raw chat |
| Promote Obsidian research into the repo | Knowledge import | `docs/repo-knowledge-boundary.md`, `docs/obsidian-knowledge-map.md`, `docs/repo-maintenance-guide.md` | `docs/experience-capture-format.md`, matching scenario/library files | Import only geometry-actionable, reusable, source-aware, buildable, checkable, shareable, compact knowledge |

## Scenario 3C Example - Second Massing Variant

When the user says "make another variant" and there is already a first massing,
do not restart from generic typology.

Read:

```text
docs/workflows/massing/tep-massing-scenario-subtypes.md
docs/libraries/massing/massing-decision-library.md
docs/libraries/massing/form-operator-library.md
docs/libraries/standards/moscow-building-dimensional-library-2026.md
docs/errors/massing/moscow-bc-massing-error-library.md
docs/case-library.md
docs/case-digest.md
```

If the first variant has a case note, read it. If it exists only in Rhino,
inspect the active scene through RhinoMCP and record:

```text
units
visible generated layers
source massing bbox
approximate footprint zones
height bands
public route/open-space logic
TEP/GFA/FAR if available
what user accepted or rejected
```

Then choose one or two explicit operators from
`docs/libraries/massing/form-operator-library.md`, for example:

```text
setback
chamfer
rotation
public void
taper
podium/tower split
crown/top-shape change
```

Report the variant as a delta:

```yaml
source_variant: name_or_layer
preserved:
  - gabarit / density scale
  - source anchors
  - required entries or routes
changed:
  - operator
  - silhouette
  - open-space edge
checks:
  - boundary
  - height
  - public spine
  - TEP scale
  - known error gates
```

## Reading Budget Rule

The first answer should be based on the smallest useful context:

```text
entrypoint
-> task read map
-> scenario workflow
-> one or two relevant libraries
-> one closest case/error file
-> active Rhino/source inspection
```

Only expand when the task changes or a gate fails.
