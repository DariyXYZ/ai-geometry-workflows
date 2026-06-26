# Repo Folder Architecture

This file is the source of truth for where durable knowledge and reusable code
belong. The goal is to prevent Rhino geometry, Grasshopper automation, massing
libraries, standards, tools, research, and temporary artifacts from mixing.

## Core Rule

Choose the folder by the question the file answers.

```text
workflow: how should a task be approached?
library: what reusable domain knowledge or pattern should be applied?
case: what happened in one proven or failed run?
error: what must not happen again?
tool: how should a backend or API be used?
research: what external or raw source was distilled?
script: what reusable executable artifact performs work?
```

## Top-Level Shape

```text
docs/
  START_HERE.md
  task-read-maps.md
  repository-map.md
  library-index.md
  repo-folder-architecture.md
  workflows/
  libraries/
  cases/
  errors/
  tools/
  research/
scripts/
  rhino/
  grasshopper/
decisions/
archive/
```

Root-level `docs/*.md` files are navigation, policy, indexes, current state, or
global ledgers only. New long-form domain knowledge should not be added to
`docs/` root.

## Docs Folders

| Folder | Owns | Examples |
| --- | --- | --- |
| `docs/workflows/rhino-reference/` | Scenario 1 source-authority and constructive-grammar workflows | `reference-modeling-gates.md` |
| `docs/workflows/massing/` | Scenario 3 massing, TEP, checklist, office/MFC workflows | `tep-massing-scenario-subtypes.md`, `architecture-compliance-check.md` |
| `docs/workflows/analysis-cleanup/` | Future Scenario 2 cleanup workflows | part-preserving cleanup gates |
| `docs/libraries/massing/` | Reusable massing/site/form operator knowledge | form operators, site zoning, massing decisions |
| `docs/libraries/grasshopper/` | GH graph, plugin, architecture-snippet, and C# pattern libraries | GH form patterns, plugin stack |
| `docs/libraries/standards/` | Numeric standards, dimensional defaults, checklist baselines | Moscow building/road dimensions, approval checklist |
| `docs/cases/rhino-geometry/` | Direct Rhino/RhinoCommon/.3dm geometry cases | reference modeling, Rhino massing, replay cases |
| `docs/cases/grasshopper/` | GH graph/C# Script/plugin/source-injection cases | GH smoke, voxel tower, C# SetSource |
| `docs/errors/massing/` | Massing/site/design rejection gates | Moscow BC massing errors |
| `docs/errors/grasshopper/` | GH/MCP/C# automation failures | GH source-injection and `g1_*` errors |
| `docs/tools/rhino/` | RhinoMCP, RhinoCommon, backend policy | Rhino MCP backend notes |
| `docs/tools/grasshopper/` | GH automation and C# Script tool notes | GH workflow, performance |
| `docs/research/source-repos/` | External repository cards | RhinoMCP, Live OBJ, text-to-CAD |
| `docs/research/` | Distilled research and direction synthesis | external repo constructor map |

## Case Family Rule

Every durable case note must include `case_family` in its
`AI Extraction Summary`.

Use:

```yaml
case_family: rhino-geometry
case_family: grasshopper
case_family: analysis-cleanup
case_family: source-research
```

If the case is about a Grasshopper graph, C# Script component, GH plugin,
slider wiring, `g1_*`, source injection, or GH canvas behavior, it belongs in
`docs/cases/grasshopper/`.

If the case is about building or validating `.3dm` geometry directly in Rhino,
RhinoCommon, RhinoMCP scene operations, reference modeling, or massing, it
belongs in `docs/cases/rhino-geometry/`.

## Script Folders

| Folder | Owns |
| --- | --- |
| `scripts/rhino/common/` | Reusable RhinoCommon helper code |
| `scripts/rhino/massing/` | Rhino massing generators and validators |
| `scripts/rhino/smoke/` | Rhino/RhinoCommon smoke tests |
| `scripts/rhino/demos/` | Reproducible Rhino demo builders |
| `scripts/grasshopper/examples/` | Paste-ready GH C# or Python examples |
| `scripts/grasshopper/snippets/` | Small reusable GH C# Script blocks |
| `scripts/grasshopper/smoke/` | GH selectors and smoke artifacts |

Do not put new scripts directly in `scripts/`. Choose the smallest domain
folder. Disposable scripts go in `.tmp_cases/` or `archive/`.

## Adding A New File

Before creating or moving a file, answer:

1. Is this a workflow, library, case, error, tool note, research note, decision,
   or script?
2. Is it Rhino geometry, Grasshopper, massing, standards, research, or
   analysis-cleanup?
3. Does an index need a one-line pointer?
4. Does `NEWS.md` need a short entry because future agents should notice it?

When in doubt, add a compact index pointer and keep the long content in the
domain folder, not in `docs/` root.

