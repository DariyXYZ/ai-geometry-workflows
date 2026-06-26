# Docs Structure

`docs/` is the active knowledge library. It should stay compact, indexed, and
useful for a fresh AI session.

## Core Indexes

| File | Role |
| --- | --- |
| `START_HERE.md` | Scenario read sets and operating rules |
| `task-read-maps.md` | Concrete task-to-read-set router for AI agents |
| `repository-map.md` | Current repo structure |
| `repo-folder-architecture.md` | Folder ownership rules for durable docs and scripts |
| `library-index.md` | Pattern, strategy, source, and tool index |
| `case-digest.md` | One-minute case wins, failures, techniques, and standards |
| `case-library.md` | Reusable case memory |
| `error-ledger.md` | Cross-scenario failures |
| `experience-capture-format.md` | Format for promoting cases into patterns, errors, metrics, prompts, and decisions |
| `obsidian-knowledge-map.md` | Useful vault research and import backlog |
| `repo-maintenance-guide.md` | How to add new knowledge cleanly |

## Folders

| Folder | Contents |
| --- | --- |
| `workflows/` | Workflow gates and scenario-specific strategy by domain |
| `libraries/` | Domain folders for massing, Grasshopper, and standards |
| `cases/` | Case-family folders such as Rhino geometry and Grasshopper |
| `errors/` | Domain-specific anti-pattern libraries |
| `tools/` | Rhino and Grasshopper tool/backend notes |
| `research/` | Compressed research, direction synthesis, and source-repo cards |

## Rule

Keep long-form knowledge in the smallest correct domain folder, then link it
from the core indexes. Do not duplicate full rules across many files. Follow
`repo-folder-architecture.md` before adding or moving durable files.
