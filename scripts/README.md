# Scripts

Only reusable or active project scripts should live here.

## Active

| Path | Role |
| --- | --- |
| `rhino_common_helper.py` | Optional backend-specific RhinoCommon helper; current implementation uses Aurox `execute_csharp` |
| `build_semantic_smoke_rhino.py` | Legacy Aurox Semantic OBJ / Rhino smoke demonstrator; port to RhinoMCP before new use |
| `moscow_bc_massing/` | Active Moscow BC massing analysis, validation, and generation scripts |

## Archive Rule

One-off experiments, generated PNGs, JSON reports, and obsolete versioned
scripts belong in `archive/`, not in this folder.

Promote a script here only when it is reusable and has a clear role in docs or
`TOOLKIT.md`.
