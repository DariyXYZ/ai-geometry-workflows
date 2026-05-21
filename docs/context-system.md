# Context System

This repository uses a small context system so future development does not
scatter decisions, errors, generated runs, and next steps across chats.

## Canonical Layers

Use these layers in order:

1. **Repository docs** - shared project truth that should be visible on GitHub.
2. **Case folders** - reproducible run state for one modeling task.
3. **Obsidian** - personal branch-independent continuity and reload notes.
4. **Ignored temporary folders** - disposable smoke tests and local experiments.

Do not store durable project state only in chat history.

## Where To Save Things

| Information | Save it here | Notes |
| --- | --- | --- |
| Current public project state | `README.md`, `docs/development-state.md` | Keep concise and current. |
| Roadmap and open decisions | `ai_geometry_workplan.md`, `decisions/` | Decisions get dated files. |
| Data/source map | `docs/project-data-map.md` | Update when folders or source roles change. |
| Known failures and lessons | `docs/error-ledger.md` | Record enough to avoid repeating work. |
| Tool commands and backend contracts | `TOOLKIT.md` | Keep runnable. |
| Chronological updates | `NEWS.md` | One entry per material change. |
| One modeling run | `cases/<case_id>/` | Tracked only when ready to share. |
| Local smoke runs | `.tmp_cases/<case_id>/` | Ignored by Git. |
| Personal reload notes | Obsidian `Codex Workspace Control Center` | Use for cross-repo context. |
| GitHub implementation task | Engineering task issue template | Use when a task should be tracked publicly. |
| GitHub failure or lesson | Failure/lesson issue template | Mirror into `docs/error-ledger.md` when durable. |

## Case Folder Contract

Each real case should be understandable without chat history:

```text
case.json
params.json
intake.md
source/
reports/
captures/
artifacts/
scripts/
README.md
```

Recommended report files:

- `reports/development_route.md`
- `reports/source_classification.json`
- `reports/scan_audit.md`
- `reports/sections.json`
- `reports/sections.csv`
- `reports/candidate_vs_source.md`
- `reports/backend_text_to_cad.md`
- `reports/validation.md`

## Development Memory Rules

- If a failure changes the route, add it to `docs/error-ledger.md`.
- If a file or folder gains a new role, update `docs/project-data-map.md`.
- If a command changes, update `TOOLKIT.md`.
- If a next step changes, update `docs/development-state.md`.
- If a tradeoff becomes accepted policy, add a dated decision in `decisions/`.
- If the change only helps local continuity, update the Obsidian control center.

## Active Boundary

Rhino/Aurox owns `.3dm` scene readback, scan, overlays, section extraction, and
Rhino visual review.

`text-to-cad` / build123d owns clean parametric source and STEP-first candidate
generation.

`ai_geometry_toolkit` owns orchestration: cases, params, routes, backend links,
normalization, validation reports, and handoff state.
