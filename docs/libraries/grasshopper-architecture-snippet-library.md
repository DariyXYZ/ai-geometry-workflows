# Grasshopper Architecture Snippet Library

Status: active quick-piece library.

Use this file when the user asks to quickly build or analyze an architectural
proposal in Grasshopper. The snippets are small reusable blocks, not full
projects.

## Principle

Fast architecture work should be assembled from small named pieces:

```text
source massing / footprints
-> floorization
-> quick metrics / TEP
-> facade or guide curves
-> optional plugin/analysis/bake
```

Prefer one compact C# Script node for logic-heavy steps and native GH/plugin
nodes for visible downstream manipulation.

## Snippet Index

| Snippet | File | Use |
| --- | --- | --- |
| BBox Floorizer | `scripts/grasshopper/snippets/massing_bbox_floorizer_csharp.cs` | Turn a massing Brep into schematic floor plates from its bounding box. |
| Building Metrics / TEP | `scripts/grasshopper/snippets/building_metrics_tep_csharp.cs` | Compute quick height, floors, footprint, GFA, FAR, efficiency, and volume. |
| Smoke Builder | `scripts/rhino/smoke/quick_architecture_snippets_smoke.cs` | RhinoCommon smoke test that bakes a simple massing, floors, and metric text. |

## Quick Routing

| User asks | Use first | Then |
| --- | --- | --- |
| "преврати массинг в этажи" | BBox Floorizer | Replace with contour/section floorizer when exact floor plates matter. |
| "посчитай ТЭПы / габариты" | Building Metrics / TEP | Add site area and efficiency assumptions explicitly. |
| "быстро показать БЦ" | C# massing generator + metrics | Add facade guide lines only after height/area pass. |
| "этажи по существующему объему" | BBox Floorizer as schematic | Ask for source floor plate authority before finalizing. |
| "сравнить варианты" | Metrics / TEP on each variant | Table outputs before visual detail. |
| "подготовить к bake" | Elefront/Human after preview | Store layer/name/material conventions in graph recipe. |

## Snippet - BBox Floorizer

Purpose:

Turn an approximate massing into stacked schematic floor slabs. It is fast and
robust because it uses the massing bounding box, not Brep contour topology.

Use when:

- the goal is early TEP / floor-count reasoning;
- the massing is simple enough for bbox floors;
- the user wants a fast scaffold before exact contour floors.

Do not use as final floor plates when:

- the massing has major setbacks, courtyards, holes, rotated plates, or curved
  edges that must be respected;
- source floor curves exist and should control the design.

Inputs:

```yaml
Massing: Brep
FloorHeight: 3.9
SlabThickness: 0.30
Inset: 0.0
Efficiency: 0.82
SiteArea: 0.0
```

Outputs:

```yaml
FloorPlates: schematic slab Breps
FloorOutlines: outline curves
FloorAreas: per-floor gross areas
Metrics: key/value report lines
Info: compact summary
```

Validation:

- first floor starts at bbox minimum Z;
- top floor does not exceed bbox maximum Z;
- slab count matches `floor(height / floorHeight)` within expected rounding;
- report states that floors are bbox schematic.

## Snippet - Building Metrics / TEP

Purpose:

Calculate fast architectural metrics from massing Breps and optional floor
areas.

Use when:

- comparing massing variants;
- checking whether a proposed BC tower/podium is in the right area range;
- generating a compact handoff report.

Inputs:

```yaml
Masses: List<Brep>
FloorAreas: List<double>
SiteArea: double
FloorHeight: double
Efficiency: double
ParkingRatio: double
```

Outputs:

```yaml
GrossFloorArea
NetFloorArea
FAR
BuildingHeight
EstimatedFloors
FootprintArea
GrossVolume
Report
```

Assumptions:

- if `FloorAreas` are provided, they control GFA;
- otherwise the snippet estimates GFA from bbox footprint and height;
- `Efficiency` is a planning assumption, not measured rentable area;
- `FAR` is only produced when `SiteArea > 0`.

## Snippet - Smoke Builder

Purpose:

Smoke-test the logic in Rhino without relying on Grasshopper source injection.

It creates:

- a simple transparent massing box;
- schematic floor slabs;
- a core;
- metric text;
- named layers.

This proves RhinoCommon geometry and TEP math before a GH graph is built.

Passed smoke case:

```text
docs/cases/grasshopper-architecture-snippets-smoke-2026-06-23.md
```

Rhino 8 C# runner gotchas from the smoke:

- use `entity.PlainText = text`, not obsolete `TextEntity.Text`;
- call `RhinoApp.WriteLine(string.Format(...))`, not
  `RhinoApp.WriteLine("...", args...)`.

## Fast Assembly Pattern

For a normal architectural prompt:

```text
1. Build or inspect source massing.
2. Run floorization snippet.
3. Run metrics snippet.
4. Stop and report height / floors / GFA / FAR assumptions.
5. Add facade guides only after numbers pass.
6. Bake only after preview validation.
```

## Anti-Patterns

- Treating bbox floors as exact leasable floor plates.
- Calculating FAR without stated site area.
- Hiding assumptions such as efficiency or floor height.
- Adding facade detail before area/height/floor count pass.
- Optimizing before variables and constraints are declared.
