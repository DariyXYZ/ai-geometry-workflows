# Start Here

Human onboarding page for reopening the repo on a new machine or explaining it
to another architect. For AI task execution, use `AI_NAVIGATOR.md` first.

## Minimal Reading Order

For an AI agent:

```text
AI_NAVIGATOR.md
-> docs/task-read-maps.md
-> one matching task row
-> only the named workflow/library/case files
```

For a human:

```text
README.md
-> AI_NAVIGATOR.md
-> docs/task-read-maps.md
-> docs/case-digest.md
-> docs/repository-map.md only if you need to find files
```

Do not read `NEWS.md` for modeling context. It is a changelog/audit trail.

## File Roles

| File | Role |
| --- | --- |
| `AI_NAVIGATOR.md` | First AI page: hierarchy, rules, scenario names. |
| `docs/task-read-maps.md` | Source of truth for what to read for a concrete task. |
| `docs/case-digest.md` | Compact lessons, wins, failure gates, and metrics. |
| `docs/repository-map.md` | File/folder location map, not a default read set. |
| `docs/library-index.md` | Library catalog, used when a task row is not enough. |
| `docs/case-library.md` | Full case index, used only when a close precedent matters. |
| `docs/repo-knowledge-boundary.md` | What belongs in GitHub vs local Obsidian. |
| `docs/repo-folder-architecture.md` | Where to save new durable files. |

## Main Workflows

| Workflow | Start with |
| --- | --- |
| Reference/photo/plan to model | `docs/task-read-maps.md`, Scenario 1 row. |
| Existing model cleanup | `docs/task-read-maps.md`, Scenario 2 row. |
| Massing / TEP / revision | `docs/task-read-maps.md`, Scenario 3A/3B/3C row. |
| Checklist review | `docs/task-read-maps.md`, Scenario 3D row. |
| RhinoMCP command execution | `docs/tools/rhino/rhino-mcp-command-library.md`. |
| Grasshopper automation | `docs/task-read-maps.md`, Grasshopper row. |

## Write-Back Rule

After a useful session, update the smallest durable place:

```text
workflow rule -> docs/workflows/
modeling command -> docs/tools/
metric/default -> docs/libraries/
mistake -> docs/errors/ or docs/error-ledger.md
case result -> docs/cases/
tradeoff -> decisions/
```

Use `docs/experience-capture-format.md` when one session contains several
types of knowledge.
