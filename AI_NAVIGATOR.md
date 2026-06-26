# AI Navigator

This repository is a portable architecture and geometry workflow library for AI
agents. It should give a new model enough structure to think architecturally,
use RhinoMCP or another CAD bridge responsibly, avoid known failures, and add
new reusable knowledge after each project.

Use this file as the first page when giving the repo to any AI.

## What This Repo Is

The repo combines five kinds of memory:

1. **Scenario strategies** - workflows for different task types.
2. **Pattern libraries** - architectural approaches, form operators, zoning
   patterns, and modeling grammars.
3. **Case library** - successful, partial, and failed Rhino/CAD experiments.
4. **Error library** - bad patterns, repeated mistakes, and rejection gates.
5. **Source-repo memory** - compressed notes from external repositories so an AI
   does not reread everything from scratch.

The goal is not to store every chat transcript. The goal is to preserve reusable
decision structure.

## Fast Load For Any AI

Read in this order:

1. `AI_NAVIGATOR.md` - this file.
2. `docs/task-read-maps.md` - task-specific read sets.
3. `docs/START_HERE.md` - scenario read sets.
4. `docs/repository-map.md` - where things live.
5. `docs/library-index.md` - pattern, strategy, source, and tool libraries.
6. `docs/case-digest.md` - one-minute wins, errors, techniques, and standards.
7. `docs/case-library.md` - known successful and failed cases.
8. `docs/error-ledger.md` - mistakes that must not repeat.
9. `docs/experience-capture-format.md` - how to write back reusable lessons.
10. `docs/repo-knowledge-boundary.md` - what belongs in GitHub vs local Obsidian.
11. `docs/repo-folder-architecture.md` - where each kind of durable file belongs.
12. `docs/obsidian-knowledge-map.md` - useful vault research not fully migrated.
13. `NEWS.md` - newest changes and promoted rules.

Then load only the scenario-specific documents. Do not read the whole repo by
default.

## Repo-As-Skill Workflow

For any concrete task:

```text
classify task
-> open docs/task-read-maps.md
-> load the smallest scenario/library/case set
-> inspect active Rhino/source context
-> act
-> write back only reusable experience
```

Example: if the user asks for a second massing variant and variant 1 already
exists, route to Scenario `3C`. Read
`docs/workflows/massing/tep-massing-scenario-subtypes.md`,
`docs/libraries/massing/massing-decision-library.md`,
`docs/libraries/massing/form-operator-library.md`, the Moscow dimensional libraries,
the closest case, and the active Rhino scene. Preserve source gabarit/TEP scale
and report the new variant as deltas from the first one.

## Scenario Router

### Scenario 1 - Reference To Model

Use when building architecture from photos, plans, elevations, dimensions,
underlays, text descriptions, or reference images.

Read:

- `docs/workflows/rhino-reference/reference-modeling-gates.md`
- `docs/cases/rhino-geometry/recent-rhino-case-lessons.md`
- relevant `decisions/`

First question:

```text
What is the source authority, and what constructive grammar makes the object?
```

### Scenario 2 - Complex Model To Simplified Analysis Geometry

Use when simplifying an existing Rhino/architecture model for wind comfort,
analysis geometry, or clean massing.

Read:

- `docs/development-state.md`
- `docs/error-ledger.md`
- `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`
- `decisions/2026-05-20-nurbs-restart-from-named-rails.md`

First question:

```text
What architectural parts must be preserved, and which details can be discarded?
```

### Scenario 3 - Massing And Revisions From TEPs

Use when generating, revising, or reviewing early massing/building proposals
from plot boundary, TEP/GFA/FAR, height constraints, red lines, INSO,
underlays, user feedback, or approval checklist criteria.

Read:

- `docs/workflows/massing/tep-massing-scenario-subtypes.md`
- `docs/libraries/massing/massing-decision-library.md`
- `docs/libraries/massing/form-operator-library.md`
- `docs/workflows/massing/architecture-compliance-check.md`
- `docs/libraries/standards/moscow-architecture-approval-checklist.md`
- `docs/libraries/massing/moscow-bc-site-zoning-patterns.md`
- `docs/errors/massing/moscow-bc-massing-error-library.md`

First question:

```text
Is this 3A fixed zoning, 3B plot-plus-entries, 3C existing-massing revision,
or 3D checklist/compliance review?
```

## Non-Negotiable Operating Rules

- Do not invent geometry before classifying the scenario.
- Do not treat numeric validation as design acceptance.
- Do not use facade/detail to hide wrong massing.
- Do not replace user-provided source geometry, footprints, entries, or curves
  with generic parametric guesses.
- Preserve source and context layers in Rhino.
- If using RhinoMCP, validate by scene units, bbox/sections, source
  authority, and visible review state.
- If a case reveals a reusable failure, add it to an error library before
  moving on.

## Where To Look

| Need | Start here |
| --- | --- |
| Quick scenario choice | `docs/START_HERE.md` |
| Concrete task read map | `docs/task-read-maps.md` |
| Repository structure | `docs/repository-map.md` |
| Pattern and strategy library | `docs/library-index.md` |
| Compact case memory | `docs/case-digest.md` |
| Experience capture format | `docs/experience-capture-format.md` |
| Repo vs Obsidian boundary | `docs/repo-knowledge-boundary.md` |
| Folder architecture | `docs/repo-folder-architecture.md` |
| Obsidian research map | `docs/obsidian-knowledge-map.md` |
| Massing decision order | `docs/libraries/massing/massing-decision-library.md` |
| Massing form operators | `docs/libraries/massing/form-operator-library.md` |
| Approval checklist review | `docs/workflows/massing/architecture-compliance-check.md` |
| Moscow architecture checklist | `docs/libraries/standards/moscow-architecture-approval-checklist.md` |
| Successful/failed examples | `docs/case-library.md` |
| Known mistakes | `docs/error-ledger.md` |
| Recent Rhino lessons | `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` |
| Accepted decisions | `decisions/` |
| External repo memory | `docs/research/source-repos/` |
| Current technical state | `docs/development-state.md` |
| How to add knowledge | `docs/repo-maintenance-guide.md` |

## Knowledge Shape

When adding reusable knowledge, prefer one of these forms:

```text
strategy: when to use, inputs, workflow, acceptance
pattern: intent, geometry logic, constraints, examples, failure modes
case: context, result, what worked, what failed, promoted rules
error: symptom, cause, detection, correction, gate
decision: accepted tradeoff, date, reason, consequences
source card: external repo idea, usable pieces, non-goals
```

Use `docs/experience-capture-format.md` when a session should be split into a
case note, pattern/operator, error, metric/default, prompt/hint, decision, or
tool note.

Use `docs/repo-knowledge-boundary.md` before importing local Obsidian research:
only geometry-actionable, reusable, source-aware, buildable, checkable, and
shareable knowledge belongs in the shared repo.

## RhinoMCP Session Rule

Default to the official McNeel `mcneel/RhinoMCP` server for Rhino work. Use
Aurox or another Rhino plugin only when the user asks for that backend or the
standard RhinoMCP route cannot expose a required operation.

Before modeling or checklist review:

1. Read the scenario-specific gate.
2. Inspect source layers and units.
3. Decide what is source authority.
4. Define the validation gates.
5. Build the smallest useful geometry, or collect checklist evidence if this is
   a review task.
6. Validate numerically, visually, and against checklist criteria when relevant.
7. Record reusable results back into this repo.

This repo should make the AI slower at the start and much less random later.
