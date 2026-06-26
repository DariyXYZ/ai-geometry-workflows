# Grasshopper Architecture Snippets Smoke - 2026-06-23

Status: passed RhinoCommon smoke test.

Scenario: tooling / architecture snippet validation.

## AI Extraction Summary

```yaml
case_family: grasshopper
use_when: "testing quick architecture snippets for massing, floors, core, and TEP metrics without depending on GH source injection"
source_authority: "RhinoCommon smoke script and object/layer audit"
geometry_grammar: "bbox massing -> schematic floors -> central core -> GFA/net/FAR metrics -> visible annotation"
effective_rhino_gh_route: "run RhinoCommon smoke in Rhino first; then use paste-ready GH C# snippets manually"
key_parameters:
  units: meters
  massing_m: "36 x 28 x 78"
  floors: 20
  floor_height_m: 3.9
  slab_thickness_m: 0.30
  site_area_m2: 4200
  far: 4.8
promoted_rules:
  - "use PlainText on TextEntity in Rhino 8 C# runner"
  - "use string.Format for RhinoApp.WriteLine formatting"
  - "compute FAR only when site area is provided"
failure_gates:
  - "do not assume GH source injection is needed for snippet validation"
  - "do not leave generated objects unnamed or unlayered"
validation: "23 generated objects, named smoke layers, grounded geometry, floor slabs within massing height, console OK line"
read_more_when: "checking architecture snippet basics or Rhino 8 C# runner gotchas"
related_scripts:
  - "scripts/rhino/smoke/quick_architecture_snippets_smoke.cs"
  - "scripts/grasshopper/snippets/massing_bbox_floorizer_csharp.cs"
  - "scripts/grasshopper/snippets/building_metrics_tep_csharp.cs"
```

## Goal

Test the first quick architecture snippet bundle without relying on Grasshopper
source injection.

The smoke reproduces the core operations expected from future GH C# snippets:

- make a simple massing;
- convert massing dimensions into schematic floors;
- add a central core;
- compute GFA, net area, FAR, floors, and height;
- write a visible metrics label;
- organize generated objects into named layers.

## Environment

```yaml
rhino_version: 8.30.26103.11001
slot: aardvark
model_units: Meters
grasshopper_canvas_visible: true
test_route: mcp__rhino.run_csharp
script: scripts/rhino/smoke/quick_architecture_snippets_smoke.cs
```

## Result

Console output:

```text
GH_SNIPPET_SMOKE OK floors=20 height=78 gfa=20160 far=4.8
```

Object audit:

```yaml
total_objects: 23
smoke_objects: 23
layers:
  - GH_SNIPPET_SMOKE_core
  - GH_SNIPPET_SMOKE_floors
  - GH_SNIPPET_SMOKE_massing
  - GH_SNIPPET_SMOKE_metrics
```

Generated:

- 1 massing Brep, `36 x 28 x 78 m`;
- 20 slab Breps, `3.9 m` floor-to-floor, `0.30 m` thick;
- 1 central core Brep, `4.2 m` radius, `78 m` high;
- 1 text annotation with floors, height, GFA, net area, and FAR.

Metrics:

```yaml
floors: 20
height_m: 78
gross_floor_area_m2: 20160
net_area_m2_at_0_82_efficiency: 16531.2
site_area_m2: 4200
far: 4.8
```

## Issues Found

The first compile attempt failed because Rhino 8 C# runner did not accept:

```csharp
RhinoApp.WriteLine("...", arg1, arg2)
TextEntity.Text = text
```

Fix:

```csharp
RhinoApp.WriteLine(string.Format("...", arg1, arg2));
entity.PlainText = text;
```

Promote this to C# snippet rules.

## Validation

- Units are meters.
- All generated objects are named with `GH_SNIPPET_SMOKE`.
- Generated geometry is grounded at `Z = 0`.
- Floor objects stay within the `78 m` massing height.
- FAR is only computed because a site area was provided.

## Next Step

Use the two GH paste-ready snippets:

```text
scripts/grasshopper/snippets/massing_bbox_floorizer_csharp.cs
scripts/grasshopper/snippets/building_metrics_tep_csharp.cs
```

inside manually created Rhino 8 C# Script components. Do not depend on
programmatic source injection until the C# Script IO route is proven.
