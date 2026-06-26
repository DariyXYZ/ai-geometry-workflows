# AI Geometry Workflows

Portable architecture and geometry workflow library for AI agents working with
RhinoMCP, CAD-as-code, massing, reference modeling, and analysis-geometry
cleanup.

The repo is meant to be handed to a fresh AI session as structured memory:
strategies, pattern libraries, successful and failed cases, error ledgers,
source-repo summaries, and runnable helper code.

## Start Here

For any AI agent:

```text
AI_NAVIGATOR.md
```

For a human or new machine:

```text
docs/START_HERE.md
docs/task-read-maps.md
docs/case-digest.md
docs/repo-knowledge-boundary.md
docs/repository-map.md
docs/library-index.md
```

Do not read the whole repo first. Pick the smallest scenario read set from
`docs/task-read-maps.md`.

## Active Scenarios

1. **Reference to model** - build Rhino/CAD geometry from photos, drawings,
   references, dimensions, or text.
2. **Complex model cleanup** - convert messy architecture/Rhino models into
   simplified analysis geometry.
3. **Massing, TEP revisions, and checklist review** - generate, revise, or
   review early massing/building proposals from plot boundaries, TEP/GFA/FAR,
   entries, height constraints, INSO, underlays, user feedback, and architecture
   approval checklist criteria.

## Repo Shape

```text
AI_NAVIGATOR.md          portable first page for AI agents
AGENTS.md               compact agent rules
NEWS.md                 newest project changes
TOOLKIT.md              CLI/tooling contract
ai_geometry_toolkit/    runnable Python orchestration code
tests/                  unit tests and fixtures
docs/                   active knowledge library
decisions/              dated accepted decisions
scripts/                reusable promoted scripts only
archive/                old reports and one-off experiments
```

Inside `docs/`:

```text
workflows/   task approach and scenario strategy by domain
libraries/   reusable patterns, standards, dimensions, and GH libraries
cases/       separated Rhino geometry and Grasshopper case branches
errors/      domain-specific anti-patterns and rejection gates
tools/       Rhino and Grasshopper backend notes
research/    compressed research and external source-repo synthesis
```

## Runnable CLI

```powershell
python -m ai_geometry_toolkit --help
```

Create a case folder:

```powershell
python -m ai_geometry_toolkit new-case `
  --scenario cleanup `
  --name test_data_2_mvp `
  --source test_data_2.3dm `
  --units m `
  --downstream Ladybug
```

Validate and route:

```powershell
python -m ai_geometry_toolkit validate-case .\cases\<case_id>
python -m ai_geometry_toolkit route .\cases\<case_id>
```

## Knowledge Rules

- Save reusable structure, not raw chat.
- Follow `docs/repo-folder-architecture.md` before creating or moving files.
- Put new patterns in the matching `docs/libraries/<domain>/` folder.
- Put workflow rules in `docs/workflows/<domain>/`.
- Put reusable case lessons in the matching `docs/cases/<case-family>/` folder.
- Put repeated failures in `docs/error-ledger.md` or `docs/errors/<domain>/`.
- Put dated tradeoffs in `decisions/`.
- Put disposable run output in `.tmp_cases/` or `archive/`, not active docs.
- Use `docs/experience-capture-format.md` to split case experience into
  patterns, errors, metrics, prompts, decisions, and tool notes.
- Use `docs/repo-knowledge-boundary.md` before promoting Obsidian research into
  the shared repo.

Read `docs/repo-maintenance-guide.md` before adding new durable knowledge.
