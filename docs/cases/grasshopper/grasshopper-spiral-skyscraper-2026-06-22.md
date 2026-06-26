# Grasshopper Spiral Skyscraper - 2026-06-22

Status: first reusable Grasshopper architecture case, pending manual GH paste
test.

Scenario: tooling / Grasshopper architecture massing.

## AI Extraction Summary

```yaml
case_family: grasshopper
use_when: "baseline parametric tower in Grasshopper using one Rhino 8 C# Script node plus sliders"
source_authority: "source-controlled C# Script body and RhinoCommon runtime validation"
geometry_grammar: "repeated rectangular floor plates -> controlled twist -> controlled taper -> capped slabs -> vertical core -> four facade rails"
effective_rhino_gh_route: "manual paste into modern Rhino 8 C# Script component; validate RhinoCommon logic through run_python/RhinoCommon before trusting GH canvas delivery"
key_parameters:
  units: meters
  floors: 42
  floor_height_m: 3.9
  width_m: 34
  depth_m: 28
  twist_deg: 210
  taper: 0.72
  core_radius_m: 5
promoted_rules:
  - "one source-controlled C# Script node is the fastest baseline for early parametric tower massing"
  - "script body must live in repo, not only in GH or chat"
  - "validate object counts, Z levels, and rails before adding facade detail"
failure_gates:
  - "do not rely on automated GH source assignment unless IO inspection and tiny solve pass"
  - "avoid g1_* and run_csharp on adopted/problematic slots when they wedge the plugin handler"
validation: "42 plates, 4 rails, 1 capped core, first slab at Z=0, total height 163.8 m, bbox and visible object count audited"
read_more_when: "creating a quick twist/taper tower C# node or debugging GH C# Script delivery"
related_scripts:
  - "scripts/grasshopper/examples/spiral_tower_csharp.cs"
```

## Goal

Create a parametric spiral skyscraper as a Grasshopper C# Script node case that
is fast to reproduce, easy to inspect, and useful as a baseline for future
architecture generators.

This case intentionally uses one C# Script node plus sliders instead of a large
component graph. The core logic is RhinoCommon, stored in source control, and
kept independent from optional Grasshopper plugins.

## Source Files

```text
scripts/grasshopper/examples/spiral_tower_csharp.cs
docs/tools/grasshopper/grasshopper-csharp-script-nodes.md
docs/errors/grasshopper/grasshopper-mcp-error-library.md
```

## Target Environment

Observed during setup:

```yaml
rhino_version: 8.30.26103.11001
grasshopper: Rhino 8 Grasshopper
model_units: meters
node_type: C# Script component
script_style: GH_ScriptInstance
csharp_baseline: C# 9-compatible
```

## Design Parameters

Default values:

```yaml
Floors: 42
FloorHeight: 3.9
Width: 34.0
Depth: 28.0
TwistDeg: 210.0
Taper: 0.72
SlabThick: 0.35
CoreRadius: 5.0
```

Expected metrics:

```yaml
total_height_m: 163.8
floor_plate_count: 42
base_plate_m: 34.0 x 28.0
top_plate_scale: 0.72
twist_total_degrees: 210.0
```

## Outputs

```yaml
FloorPlates: list of capped Breps, one per floor slab
FacadeRails: four twisting corner polyline curves
Core: capped cylindrical Brep
Info: summary string with floors, height, twist, and units
```

## Reproduction Workflow

1. Open Rhino 8 and Grasshopper.
2. Confirm the Rhino model units are meters.
3. Place a modern Rhino 8 `C# Script` component.
4. Paste `scripts/grasshopper/examples/spiral_tower_csharp.cs` into the script
   editor.
5. Let the script signature create the inputs and outputs.
6. Add sliders for the eight inputs.
7. Solve and inspect the preview before baking.

Recommended slider ranges:

| Input | Min | Default | Max |
| --- | ---: | ---: | ---: |
| Floors | 8 | 42 | 80 |
| FloorHeight | 3.0 | 3.9 | 5.5 |
| Width | 18.0 | 34.0 | 70.0 |
| Depth | 18.0 | 28.0 | 70.0 |
| TwistDeg | 0.0 | 210.0 | 540.0 |
| Taper | 0.35 | 0.72 | 1.0 |
| SlabThick | 0.15 | 0.35 | 0.8 |
| CoreRadius | 2.0 | 5.0 | 12.0 |

## Acceptance Gates

- The model is in meters.
- No geometry floats below or above its intended Z levels.
- `FloorPlates` count equals `Floors`.
- The first slab is at Z = 0.
- Total tower height equals `Floors * FloorHeight`.
- The top plate is smaller than the base when `Taper < 1.0`.
- `FacadeRails` follow the same corner order floor-to-floor.
- `Core` is vertical and capped.
- The script body is stored in the repo, not only in the GH file or chat.

## Test Status

RhinoCommon logic: runtime-validated 2026-06-22. The `RunScript` body was ported
to `run_python` (the stable layer; `run_csharp`/`g1_*` were avoided per GH-009 /
GH-012) and executed against a fresh Rhino 8 slot in a meters document. All
acceptance gates passed and the geometry was baked to a `SpiralTower` layer.

```yaml
rhino_version: 8.30.26103.11001
slot_port: 10502
units: Meters
tolerance: 0.001
plates_built: 42 / 42
extrude_fails: 0
cap_fails: 0
first_slab_z: 0.0
total_height_m: 163.8
base_scale: 1.0
top_scale: 0.72
rails_count: 4
core_is_solid: true
baked_objects: 47   # 42 plates + 4 rails + 1 core
bbox: [-20.93, -20.61, 0] .. [20.93, 20.61, 163.8]
viewport: perspective / Shaded, visibleObjectCount 47
```

Grasshopper C# Script node delivery still uses the manual paste route — the
logic is proven, but in-canvas source assignment remains blocked (see Known
Limitations). The validation confirms the RhinoCommon code is correct before any
paste.

Connection issues hit and logged during this session: GH-009 (`g1_*` crashes an
adopted slot), GH-010 (`MCPStart`, not `MCPConnect`), GH-011 (competing
`rhino-mcp-router` from claude.exe + codex.exe -> plugin double-write), GH-012
(`run_csharp`/RhinoCode wedges the plugin handler). Lead validation with
`run_python`, keep a single MCP client per Rhino.

## Known Limitations

The current RhinoMCP `g1_*` surface can place and wire components, but direct
script-source editing is not exposed as a stable `g1_*` operation.

The Rhino 8 `RhinoCodePluginGH.Components.CSharpComponent` exposes
`SetSource(...)`, but a smoke test showed that programmatic assignment can keep
default `x/y/out/a` IO and rewrite the `RunScript` signature. Therefore this
case is currently treated as paste-ready source plus documented workflow.

Do not use automated source injection for this case unless this gate passes:

```text
SetSource
-> SetParametersFromScript
-> TryGetSource
-> inspect Params.Input / Params.Output
-> solve tiny script
```

## Why This Is The First Case

It exercises the geometry patterns we need often:

- repeated floor sections;
- controlled twist;
- controlled taper;
- Brep extrusion and capping;
- vertical guide curves;
- compact architecture massing;
- source-controlled C# Script body.

It is small enough to debug quickly but architectural enough to reveal real
Grasshopper/C# workflow problems.

## Next Extensions

- Add a podium and entrance plinth as a second C# Script node.
- Add a facade-system node with ribs, belts, or panel curves.
- Add a metrics node for GFA, typical floor area, top area, and height summary.
- Add a baked Rhino validation helper once bake workflow is stable.
