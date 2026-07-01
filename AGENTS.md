# Agent Start Context

This repository is intended to be enough context for a new AI/code agent to
continue the geometry workflow without chat history or Obsidian.

Read these files first, in this order:

1. `AI_NAVIGATOR.md`
2. `docs/START_HERE.md`
3. `docs/repository-map.md`
4. `docs/library-index.md`
5. `docs/case-digest.md`
6. `docs/error-ledger.md`

Then choose the scenario-specific read set from `docs/START_HERE.md`.

## Non-Negotiable Rules

- Do not rely on chat memory. Durable rules go into repo docs and, when
  available, Obsidian.
- For reference modeling, prove source authority and constructive grammar
  before building geometry.
- If views are missing, ask for them instead of inventing a plausible envelope.
- Do not use facade detail to hide wrong massing.
- In Rhino, keep source underlays and helper plates below the first-floor datum
  when they are references, not building mass.
- For rotating orthogonal floor towers, use:

```text
control sections -> temporary loft -> Rhino Contour -> final floor contours
```

- Choose section direction by constructive grammar. Grove-style balcony towers
  use horizontal Contour floor plates. Karlatornet-like four-shaft twists use
  primitive shafts, vertical guide/profile curves, lofted transition surfaces,
  and mirror/repeat logic.
- For balcony towers, the contour curve is the slab/balcony edge, not the glass
  line. Offset glass inward and give slabs real thickness.
- Recent Rhino/RhinoMCP case memory lives in
  `docs/cases/rhino-geometry/recent-rhino-case-lessons.md`. Read it before replaying or extending
  Infinity Tower, Shanghai Tower-style twists, Flock chapel shells, symmetric
  stepped towers, Aqua Tower, or Absolute World Towers.
- For direct Rhino modeling commands such as slab, parapet, roof access,
  facade panel, lamella, entry, or cleanup, read
  `docs/tools/rhino/rhino-mcp-command-library.md` and use standard RhinoMCP
  `run_python` / `run_csharp` by default. Do not use Aurox patterns unless the
  user explicitly requests that backend or a legacy replay requires it.

## Current Product Vectors

1. `Reference to model`: build architecture from text, images, plans,
   elevations, dimensions, and Rhino underlays.
2. `Complex model to simplified analysis geometry`: simplify existing Rhino
   architecture into validated analysis geometry.
3. `Massing, TEPs, and checklist review`: generate, revise, or review early
   massing/building proposals from constraints, redlines, underlays, metrics,
   and architecture approval checklist criteria.

## External Repo Memory

Do not reread external repositories blindly. Start from:

- `docs/research/source-repos/README.md`
- `docs/research/external-repo-constructor-map.md`
- `docs/research/development-directions-repo-fit.md`

Use external GitHub only when the source card says the local summary is
insufficient.

## Where To Save New Knowledge

- New durable workflow rule: `docs/workflows/rhino-reference/reference-modeling-gates.md`
- New massing/checklist subscenario: `docs/workflows/massing/tep-massing-scenario-subtypes.md`
- Architecture approval checklist review: `docs/workflows/massing/architecture-compliance-check.md`
- Failure or repeated mistake: `docs/error-ledger.md`
- Accepted tradeoff/decision: `decisions/YYYY-MM-DD-short-title.md`
- External repo finding: `docs/research/source-repos/`
- Optional chronological changelog entry: `NEWS.md`
- Current implementation state: `docs/development-state.md`
