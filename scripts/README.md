# Scripts

Only reusable or active project scripts should live here.

## Active

| Path | Role |
| --- | --- |
| `rhino/common/rhino_common_helper.py` | Legacy optional backend-specific RhinoCommon helper; current implementation uses Aurox `execute_csharp`; new Rhino work should use `mcp__rhino.run_python` / `run_csharp` plus `docs/tools/rhino/rhino-mcp-command-library.md` |
| `rhino/smoke/build_semantic_smoke_rhino.py` | Legacy Aurox Semantic OBJ / Rhino smoke demonstrator; port to RhinoMCP before new use |
| `rhino/smoke/quick_architecture_snippets_smoke.cs` | RhinoCommon smoke for architecture snippet validation |
| `rhino/massing/two_tower_bc_50f_stylobate.py` | Source-controlled BC50 tower/stylobate generator |
| `rhino/massing/moscow_bc/` | Moscow BC massing analysis, validation, and generation scripts |
| `rhino/massing/residential_okn/` | Residential complex massing with retained OKN/public brick building |
| `rhino/demos/` | Reproducible Rhino demo builders |
| `grasshopper/examples/` | Paste-ready GH C# / Python examples |
| `grasshopper/snippets/` | Small reusable GH C# Script architecture blocks |
| `grasshopper/smoke/` | Grasshopper smoke artifacts and selectors |

## Archive Rule

One-off experiments, generated PNGs, JSON reports, and obsolete versioned
scripts belong in `archive/`, not in this folder.

Promote a script here only when it is reusable, placed in the smallest domain
folder, and has a clear role in docs or `TOOLKIT.md`. Do not add new files
directly under `scripts/`.
