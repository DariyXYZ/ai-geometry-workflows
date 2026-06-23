# Grasshopper Snippets

Small paste-ready C# Script nodes for architecture workflows.

Use these as building blocks:

| File | Purpose |
| --- | --- |
| `massing_bbox_floorizer_csharp.cs` | Schematic floor slabs from a massing Brep bounding box. |
| `building_metrics_tep_csharp.cs` | Quick TEP/metrics report from masses and optional floor areas. |

Rules:

- Keep snippets small and single-purpose.
- Put assumptions in outputs.
- Prefer C# 9-compatible Rhino 8 code.
- Do not use these as final analytical truth when source geometry is more
  specific than the snippet.
