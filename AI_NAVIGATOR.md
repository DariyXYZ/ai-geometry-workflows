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

## Reading Hierarchy

Use one entry flow. Do not combine all indexes as a default context dump.

```text
Tier 0: AI_NAVIGATOR.md
  Purpose: repo role, non-negotiable rules, and routing principle.
  Read: always first.

Tier 1: docs/task-read-maps.md
  Purpose: concrete task -> smallest required read set.
  Read: always second for real work.

Tier 2: scenario workflow
  Purpose: stage gates and decision order for this task type.
  Read: only files named by the matching task row.

Tier 3: libraries / command cards / one closest case or error file
  Purpose: values, operators, RhinoMCP sequences, and known failures.
  Read: only when the task row or workflow calls for them.

Tier 4: indexes and maintenance docs
  Purpose: finding files or writing back knowledge.
  Read: only when locating unknown material or updating the repo.
```

Default AI load:

1. `AI_NAVIGATOR.md`
2. `docs/task-read-maps.md`
3. the single matching task row
4. active Rhino/Grasshopper/source inspection when relevant

Do not read `docs/START_HERE.md`, `docs/repository-map.md`,
`docs/library-index.md`, `docs/case-library.md`, or `docs/obsidian-knowledge-map.md`
by default. They are lookup/onboarding files.

`NEWS.md` is a chronological changelog and audit trail, not a fast-load file.
Read it only when you need recent repository history. Any rule needed for
modeling must also live in the relevant workflow, library, case digest, command
card, or error file.

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
`docs/libraries/massing/form-operator-library.md`,
`docs/libraries/standards/moscow-massing-metric-quick-cards.md`,
`docs/libraries/massing/tep-calculation-patterns.md`, then the detailed Moscow
dimensional libraries only as needed,
the closest case, and the active Rhino scene. Preserve source gabarit/TEP scale
and report the new variant as deltas from the first one.

## Scenario Router

Use `docs/task-read-maps.md` as the source of truth for scenario read sets.
This file only defines the scenario names:

| Scenario | Use when |
| --- | --- |
| 1 Reference to model | Build architecture from photos, plans, elevations, dimensions, underlays, text, or references. |
| 2 Complex model cleanup | Simplify existing Rhino/architecture models for analysis geometry. |
| 3A Fixed zoning massing | User already gave zoning, footprints, or entries; do not move them unless asked. |
| 3B Plot-plus-entries zoning | User gave plot/access only; propose zoning before 3D massing. |
| 3C Existing massing revision | Improve or make another variant while preserving accepted scale/anchors. |
| 3D Checklist review | Review existing massing/building against approval/checklist criteria before redesign. |
| Grasshopper branch | Build/test GH graphs, C# Script nodes, plugins, or `g1_*` automation. |

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

## Lookup Files

Read these only when the task needs them:

| Need | File |
| --- | --- |
| Concrete task read set | `docs/task-read-maps.md` |
| Compact wins/errors before modeling | `docs/case-digest.md` |
| Repository/file location | `docs/repository-map.md` |
| Library discovery | `docs/library-index.md` |
| Full case list | `docs/case-library.md` |
| Global mistakes | `docs/error-ledger.md` |
| Human onboarding | `docs/START_HERE.md` |
| Write-back format | `docs/experience-capture-format.md` |
| Repo vs Obsidian boundary | `docs/repo-knowledge-boundary.md` |
| Folder architecture | `docs/repo-folder-architecture.md` |
| Obsidian import map | `docs/obsidian-knowledge-map.md` |
| Maintenance guide | `docs/repo-maintenance-guide.md` |

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
4. For direct Rhino construction, map the user's intent through
   `docs/tools/rhino/rhino-mcp-command-library.md`.
5. Define the validation gates.
6. Build the smallest useful geometry, or collect checklist evidence if this is
   a review task.
7. Validate numerically, visually, and against checklist criteria when relevant.
8. Record reusable results back into this repo.

This repo should make the AI slower at the start and much less random later.
