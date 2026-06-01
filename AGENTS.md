# Agent Start Context

This repository is intended to be enough context for a new AI/code agent to
continue the geometry workflow without chat history or Obsidian.

Read these files first, in this order:

1. `docs/START_HERE.md`
2. `NEWS.md`
3. `docs/reference-modeling-gates.md`
4. `docs/error-ledger.md`
5. `docs/repository-map.md`

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

## Current Product Vectors

1. `Reference to model`: build architecture from text, images, plans,
   elevations, dimensions, and Rhino underlays.
2. `Complex model to simplified analysis geometry`: simplify existing Rhino
   architecture into validated analysis geometry.
3. `Massing and revisions from TEPs`: generate and revise early massing from
   constraints, redlines, underlays, and metrics.

## External Repo Memory

Do not reread external repositories blindly. Start from:

- `docs/source-repos/README.md`
- `docs/external-repo-constructor-map.md`
- `docs/development-directions-repo-fit.md`

Use external GitHub only when the source card says the local summary is
insufficient.

## Where To Save New Knowledge

- New durable workflow rule: `docs/reference-modeling-gates.md`
- Failure or repeated mistake: `docs/error-ledger.md`
- Accepted tradeoff/decision: `decisions/YYYY-MM-DD-short-title.md`
- External repo finding: `docs/source-repos/`
- Chronological user-facing update: `NEWS.md`
- Current implementation state: `docs/development-state.md`
