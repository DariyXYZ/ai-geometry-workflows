# Repo Knowledge Boundary

This file defines what belongs in the shared GitHub repository and what should
stay in the local Obsidian vault until it is distilled.

The repository is the portable operating memory for architects and AI agents.
Obsidian is the broader research, capture, and personal continuity layer.

## Core Decision

Put information in the repo only when it changes how future geometry is made,
checked, repaired, or explained.

Keep information in Obsidian when it is raw, personal, speculative, redundant,
private, or useful mainly as research background.

## Goes In The Repo

| Information | Repo shape | Why |
| --- | --- | --- |
| Geometry typologies | `docs/libraries/<typology>.md` | Helps an AI choose a massing or facade grammar. |
| Form operators | `docs/libraries/massing/form-operator-library.md` or focused libraries | Gives reusable moves such as setbacks, chamfers, rotations, voids, taper, crown logic. |
| Construction recipes | `docs/workflows/`, `docs/tools/`, `scripts/` | Tells architects and agents which Rhino/Grasshopper operations build the form efficiently. |
| Dimensional defaults | `docs/libraries/*dimensional*.md` and YAML when useful | Prevents scale errors in floors, cores, facade depth, roads, roofs, and clearances. |
| Validation gates | `docs/errors/`, `docs/error-ledger.md`, scenario files | Catches numeric-pass/design-fail and known modeling mistakes. |
| Proven cases | `docs/cases/`, `docs/case-library.md`, `docs/case-digest.md` | Shows what worked, what failed, and what rule was promoted. |
| Tool/backend rules | `docs/tools/`, `TOOLKIT.md`, `scripts/README.md` | Records effective Rhino, RhinoCommon, Grasshopper, C# Script, and MCP routes. |
| Source synthesis | `docs/research/`, `docs/research/source-repos/` | Compresses external repositories or public research into actionable local memory. |
| Accepted tradeoffs | `decisions/YYYY-MM-DD-*.md` | Settles policy so future agents do not relitigate it. |

Repo entries must be compact, source-aware, and action-oriented. A good entry
lets a fresh AI or architect answer:

```text
when do I use this?
what inputs do I need?
what geometry do I build?
which Rhino/Grasshopper command path is efficient?
what parameters and defaults matter?
how do I know the result is acceptable?
what mistakes should I avoid?
```

## Stays In Obsidian

| Information | Keep local because |
| --- | --- |
| Raw article notes, image dumps, and long precedent lists | They are research substrate, not operating memory. |
| Unverified trend impressions | They need source/date/project evidence before becoming repo rules. |
| Personal reasoning, scratch rankings, and broad brainstorming | They help thinking but add noise for shared users. |
| Private project details, client-sensitive context, or non-shareable sources | The repo is intended for distribution. |
| Duplicate versions of the same idea | The repo should keep one canonical compact rule. |
| Weak or one-off observations | Promote only after repeated use, case evidence, or a clear decision. |
| Full chat transcripts | Convert to patterns, cases, errors, metrics, decisions, or tool notes. |

Obsidian may point to repo files, but the repo should not depend on Obsidian to
execute a normal geometry task.

## Promotion Gate

Before copying anything from Obsidian into the repo, pass this checklist:

1. **Geometry-actionable:** can it change a floor plate, massing, structure,
   facade, roof, site edge, circulation, or validation step?
2. **Reusable:** will more than one project, architect, or AI session use it?
3. **2026-relevant:** is the source or internal decision current enough for the
   target market and task type?
4. **Source-aware:** does it name the source family, date, region, case, or
   confidence level?
5. **Buildable:** does it map to Rhino, RhinoCommon, Grasshopper, C# Script, or
   another explicit command/tool path?
6. **Checkable:** does it include acceptance gates or failure modes?
7. **Shareable:** can it be distributed to all architects without private or
   licensing issues?
8. **Compact:** can it be summarized as a pattern, recipe, error, case, metric,
   source card, or decision?

If any answer is no, leave it in Obsidian and add only a pointer to
`docs/obsidian-knowledge-map.md` if future import is likely.

## Status Labels

| Status | Meaning |
| --- | --- |
| `Active` | Safe default for current work. Case-backed, tested, or accepted as policy. |
| `Draft active` | Usable, but needs more cases or parameter tuning. |
| `Watchlist` | Trend or technique worth tracking, not yet a rule. |
| `Local only` | Known to exist in Obsidian but not portable or not distilled. |
| `Deprecated` | Kept for history; should not guide new geometry. |

## 2026 Trend Intake

Modern typology and trend notes should not enter the repo as vibes. Convert
them into one of these forms:

- **Typology grammar:** footprint family, section logic, height strategy,
  public realm relation, structural order, facade order.
- **Operator:** one clear geometric move with inputs, parameters, command path,
  and failure modes.
- **Dimensional default:** numeric range with region/date/source confidence.
- **Case rule:** a worked or rejected example with promoted lesson.
- **Tool recipe:** the fastest reliable Rhino/Grasshopper route to generate or
  edit the geometry.
- **Watchlist card:** trend is visible but not yet trusted enough for default
  generation.

Use public/current sources only as evidence. The repo should store the
distilled rule, not copied articles or large visual catalogs.

## Recommended Import Order From Obsidian

1. `docs/libraries/massing/massing-typology-catalog.md` for large-form typologies.
2. Focused libraries for structure systems and facade grammars.
3. `docs/libraries/massing/form-operator-library.md` for reusable geometry moves.
4. `docs/libraries/grasshopper/grasshopper-architectural-form-patterns.md` and
   `docs/tools/` for efficient build methods.
5. `docs/errors/` for rejection rules discovered during modeling.
6. `decisions/` when a boundary or tradeoff becomes policy.

## Import Template

```markdown
## Pattern Name

Status: Draft active
Last reviewed: YYYY-MM-DD
Source basis: Obsidian note / case / public source / internal decision
Scope: large form / structure / facade / site / tool

### Use When

### Inputs Needed

### Geometry Logic

### Efficient Rhino / Grasshopper Route

### Parameters

### Acceptance Gates

### Failure Modes

### Related Cases Or Sources
```
