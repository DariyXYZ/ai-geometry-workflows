# Repo Vs Obsidian Knowledge Boundary

Date: 2026-06-26

## Decision

The GitHub repository is the shared operating memory for architects and AI
agents. It should contain only distilled, geometry-actionable knowledge needed
to build, revise, validate, or explain architecture in Rhino/Grasshopper and
related CAD workflows.

The local Obsidian vault remains the broader research and continuity layer:
raw precedent notes, trend research, private project memory, speculative ideas,
and personal reasoning stay there until they pass the repo promotion gate.

## Reason

The repo will be handed to many architects and to fresh AI sessions. It must be
small enough to load, clear enough to act on, and current enough for 2026
geometry work. Raw research would make the repo noisy and less reliable.

## Consequences

- Every import from Obsidian must become a pattern, recipe, case, error,
  metric/default, source synthesis, or dated decision.
- Modern typology and trend research enters the repo only after it is converted
  into buildable geometry logic, parameter ranges, validation gates, and
  efficient Rhino/Grasshopper command paths.
- `docs/obsidian-knowledge-map.md` tracks useful local notes that are not yet
  promoted.
- `docs/repo-knowledge-boundary.md` owns the detailed checklist for what goes
  into GitHub and what remains local.

