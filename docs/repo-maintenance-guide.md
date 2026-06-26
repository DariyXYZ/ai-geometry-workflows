# Repo Maintenance Guide

This repo is meant to grow as a reusable architecture/geometry library. Add new
knowledge only when it helps future agents make better decisions.

## Core Rule

Do not save raw chat. Save reusable structure.

Good additions:

- a strategy that changes how future work starts;
- a pattern that can be reused across projects;
- a case that proves or disproves a workflow;
- an error that should never repeat;
- a decision that settles a tradeoff;
- a source-repo insight that saves rereading external code.

Bad additions:

- vague summaries with no action;
- screenshots without interpretation;
- one-off scripts with no case/report;
- duplicated rules in several files;
- long transcripts.

## Where New Knowledge Goes

| Knowledge type | Location |
| --- | --- |
| Universal AI entrypoint | `AI_NAVIGATOR.md` |
| Scenario read path | `docs/START_HERE.md` |
| Task read path | `docs/task-read-maps.md` |
| Repo structure | `docs/repository-map.md` |
| Pattern or strategy index | `docs/library-index.md` |
| Experience capture format | `docs/experience-capture-format.md` |
| Case entry | `docs/case-library.md` |
| Scenario workflow | `docs/scenarios/<scenario>.md` |
| Pattern library | `docs/libraries/<topic>.md` |
| Detailed case note | `docs/cases/<case>.md` |
| Repeated mistake | `docs/error-ledger.md` or `docs/errors/<topic>.md` |
| Tool/backend note | `docs/tools/<tool>.md` |
| Research synthesis | `docs/research/<topic>.md` |
| Accepted tradeoff | `decisions/YYYY-MM-DD-short-title.md` |
| External repo finding | `docs/source-repos/<source>.md` |
| Current technical state | `docs/development-state.md` |
| Chronological update | `NEWS.md` |
| Temporary run output | `.tmp_cases/` or a clearly named scripts subfolder |

## Naming

Use lowercase kebab-case for new repo docs:

```text
docs/<folder>/<topic>.md
decisions/YYYY-MM-DD-<decision>.md
scripts/<domain>/<purpose>.py
```

Prefer clear names over short names:

```text
moscow-bc-massing-error-library.md
tep-massing-scenario-subtypes.md
repo-maintenance-guide.md
```

## Update Checklist

When adding a new reusable rule:

1. Add the rule to the smallest correct file.
2. If it changes navigation, update `AI_NAVIGATOR.md` or `docs/START_HERE.md`.
3. If it should be discoverable, update `docs/library-index.md`.
4. If it came from a case, update `docs/case-library.md`.
5. If it is a failure, update `docs/error-ledger.md`.
6. If it is an accepted tradeoff, add a dated file in `decisions/`.
7. Add a short `NEWS.md` entry if future sessions should notice it.

## Case Promotion Checklist

After a Rhino/CAD session, answer:

| Question | If yes |
| --- | --- |
| Did it teach a reusable workflow? | Add or update `docs/case-library.md` |
| Did it reveal a repeated mistake? | Add to `docs/error-ledger.md` or domain error file |
| Did it settle a tradeoff? | Add a dated decision |
| Did it create a new architectural pattern? | Add/update a pattern library and `docs/library-index.md` |
| Did it depend on external repo knowledge? | Update the relevant `docs/source-repos/` card |

Use `docs/experience-capture-format.md` for the full case note and promotion
table. Every promoted case should make clear which parts became a pattern,
error, metric/default, prompt/hint, decision, or tool note.

## Script And Output Hygiene

Scripts should not pile up anonymously in `scripts/`.

Use:

```text
scripts/<domain>/<case-or-purpose>.py
scripts/<domain>/<case-or-purpose>.json
scripts/<domain>/<case-or-purpose>.png
```

Examples:

```text
scripts/moscow_bc_massing/analyze_scene.py
scripts/moscow_bc_massing/variants_2026_06_16.json
```

If a script is disposable, put it in `.tmp_cases/` instead. If it becomes
reusable, promote it with a short note in `docs/` or `TOOLKIT.md`.

## Active Folder Contract

Use the existing top-level folders inside `docs/`:

```text
docs/scenarios/
docs/libraries/
docs/cases/
docs/errors/
docs/tools/
docs/research/
docs/source-repos/
```

Root-level `docs/*.md` files are indexes, current-state documents, or global
ledgers. New long-form knowledge should usually go into one of the folders
above and be linked from the relevant index.

`docs/task-read-maps.md` and `docs/experience-capture-format.md` are global
operating documents. Keep them compact and update them when the way an AI should
enter or write back to the repo changes.

One-off Rhino scripts, PNGs, JSON reports, and old presentations belong in
`archive/` unless they are actively reusable. Reusable scripts belong in
`scripts/<domain>/`.

## Duplication Policy

Some duplication is useful for navigation, but only one file should own the full
rule.

Use:

- `AI_NAVIGATOR.md` for the shortest global pointer.
- `docs/START_HERE.md` for scenario read sets.
- domain files for full rules.
- indexes for links and one-line descriptions.

Do not paste the same long rule into many files.

## Minimum Quality Bar For New Pattern Libraries

A pattern library entry should include:

```text
name
when to use
inputs needed
geometry/planning logic
parameters
acceptance gates
failure modes
related cases
```

If those fields are missing, keep it as a draft note until it is strong enough
to guide another AI.
