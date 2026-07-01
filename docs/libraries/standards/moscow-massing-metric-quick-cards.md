# Moscow Massing Metric Quick Cards

Status: active fast-use layer.

Use this file when the AI needs to model quickly and should not reread the full
dimensional libraries. It is a task-facing shortcut into:

- `docs/libraries/standards/moscow-building-dimensional-library-2026.md`
- `docs/libraries/standards/moscow-building-dimensional-library-2026.yaml`
- `docs/libraries/standards/moscow-road-dimensional-library-2026.md`
- `docs/libraries/massing/tep-calculation-patterns.md`

This is not a legal compliance engine. It is a fast baseline for early Rhino /
Grasshopper massing and for preventing fantasy dimensions.

Before using these values as compliance claims, re-check the active SP edition
and amendments. Fast public check points:

- SP 118.13330.2022 public/office buildings:
  `https://docs.cntd.ru/document/351102147`
- SP 1.13130.2020 evacuation routes/exits:
  `https://tiflocentre.ru/documents/sp-1-13130-2020.php`
- SP 54.13330.2022 apartment buildings:
  `https://docs.cntd.ru/document/351139048`
- Minstroy documents search for current amendments:
  `https://minstroyrf.gov.ru/docs/`

## Fast Decision Chain

```text
function
-> height band / fire-technical attention
-> floor-height preset
-> footprint area and plate depth
-> core placeholder and core count
-> roof / parapet / operated roof rule
-> road / fire access quick check
-> TEP approximation
-> warning flags
-> RhinoMCP command card
```

If the user gives approved footprints, do not resize them to fit a preset.
Use the preset to choose heights, cores, grids, roofs, and warnings.

## Minimal Metric Pack

Before running RhinoMCP, prepare this compact parameter pack:

```yaml
metric_pack:
  function: office | residential | mfc | public | unknown
  scenario: 3A | 3B | 3C | 3D
  units: meters
  source_authority:
    footprint: user_curve | inferred | proposed
    height_limit_m:
    target_gfa_m2:
  floors:
    ground_height_m:
    typical_height_m:
    count_above_ground:
    technical_floor_assumption:
  footprint:
    area_m2:
    width_m:
    depth_m:
    plate_family: compact | bar | slab | tower | podium
  core:
    count:
    placeholder_width_m:
    placeholder_depth_m:
    target_depth_to_facade_m:
  roof:
    operated: true | false
    guard_or_parapet_m:
    roof_access_from_core: true | false
  roads:
    fire_access_width_m:
    service_edge_named: true | false
  warnings: []
```

## Office Massing Card

Use for business centers, office towers, and office/MFC parts.

Quick defaults:

| Parameter | Fast value |
| --- | ---: |
| Typical floor-to-floor | 4.05 m |
| Ground lobby / retail | 5.4 m |
| Office tower plate | 900-1800 m2 |
| Large low-rise/podium office plate | 1500-3000 m2 |
| Core-to-glass target | 12.5-14.0 m |
| Default tower footprint | 42 x 32 m |
| Default core | 18 x 24 m |
| Facade module | 1.5 m |
| Structural grid | 8.4 / 9.0 / 10.5 m |
| Office slab + raised floor + services package | about 0.95-1.10 m |
| Operated roof guard | 1.2 m |

Height gates:

| Height / floors | Action |
| --- | --- |
| Up to 50 m | SP 118 baseline; normal office core placeholder can be used. |
| Above 50 m | Add high-rise fire placeholder logic; do not use simple low-rise core. |
| 35+ floors | Add technical/transfer floor assumption. |
| 60+ floors | Stop treating as generic massing; needs lift/fire/structure zoning note. |

Core count quick gate:

- One core only for compact plates where core-to-glass stays near `12.5-14 m`.
- Test two core zones for elongated or stepped plates above roughly `3000 m2`.
- Roof access volumes appear only where a core reaches an operated roof.

RhinoMCP build hints:

```text
footprint -> massing block / floor stack
core zone -> hidden guide first
roof -> border offsets -> guard ring
facade -> module grid only after massing/detail gate
```

## Residential Massing Card

Use for residential towers, slabs, and mixed residential complexes.

Quick defaults:

| Parameter | Fast value |
| --- | ---: |
| Typical residential floor-to-floor | 3.0-3.15 m |
| Better/business residential floor-to-floor | 3.15-3.45 m |
| Ground lobby/commercial | 4.2 m default, 5.4 m if active retail |
| Efficient tower plate | 500-900 m2 |
| Large tower plate | 900-1200 m2 |
| Facade-to-corridor/core target | 7.0-8.5 m |
| Default tower footprint | 34 x 26 m |
| Default core | 12 x 16 m |
| Facade bay | 3.0-3.6 m, default 3.3 m |
| Loggia/balcony projection | 1.2-1.8 m |
| Operated roof guard | 1.2 m |

Height gates:

| Height / floors | Action |
| --- | --- |
| Up to 75 m | SP 54 baseline. |
| Above 75 m | Add high-rise fire/lift/smoke-control placeholder logic. |
| Above 28 m fire-technical height | Do not use low-rise stair assumptions. |

Daylight warning:

- If facade-to-corridor/core depth is above `9 m`, add daylight strategy warning.
- If residential floor-to-floor is below `3.0 m`, add clear-height warning.

## Stepped Slab / Terraced BC Card

Use for stepped office slabs, terraced buildings, and river/city-view massings.

Fast values:

| Element | Rule |
| --- | --- |
| Step height | Usually one or more full floor modules; avoid arbitrary thin ledges. |
| Terrace guard | Use continuous closed guard ring, 1.2 m default. |
| Roof access | Only at planned core/LLY zones. |
| Detail gate | Do not add dense windows before massing approval. |
| Evacuation/core count gate | Do not invent one universal "second core from N m2" trigger. For office/public floors, read SP 1.13130.2020 as an evacuation-exit, occupant-load, travel-distance, floor-area, height, and fire-strategy check. A two-exit requirement is not the same as a blind 50/50 two-core split. |
| Core count | One compact core only for compact plates; test two zones for long/stepped slabs. First decide from SP/fire/evacuation/project strategy, occupant load, travel distance, height, plate size/length, and core-to-glass depth; do not derive core count from a 50/50 graphic split. |
| Core placement | After 2+ cores are required/selected, split first-floor area into rational service zones, place LLY cores near functional zone centers, then shift only enough to reach the highest operated roof. Equal-area split is only a first-pass heuristic. |
| Inset parapet | `DupBorder -> inward setback -> Offset x 2 -> Extrude`; use about 0.55 m edge setback, 0.32-0.42 m thickness, 1.18-1.2 m height. |
| First-floor glazing | Use taller retail/cafe glazing near floor level; do not repeat small office windows unchanged at ground floor. |
| Facade panel readability | Generate windows/entries from the local facade plane first; after validation, a tiny 0.06-0.10 m local-normal outset is allowed for Rhino readability. |

Common failure gates:

- roof guard built from ragged separate boxes;
- parapet sitting exactly on the roof edge when a visible coping/setback band is
  needed;
- roof access boxes scattered on every terrace;
- core/LLY boxes touching facade or creating narrow leftover strips;
- using 50/50 area split as if it were an SP rule for the number of cores;
- entrances added as decorative portals instead of direct LLY/core exits.
- first-floor windows too small for retail/cafe frontage;
- window/entry panels either vanish into the facade or become large pasted-on
  boxes instead of tiny local-normal outsets.

## Road And Fire Access Card

Use before placing site/service roads.

Fast values:

| Element | Fast value |
| --- | ---: |
| High-rise BC fire/service loop | 6.0-7.0 m |
| Standard two-way local street | 6.5-7.0 m |
| Tight local access street | 6.0 m |
| One-way non-fire service lane | 3.5-4.0 m |
| Fire access for building height > 46 m | 6.0 m minimum model clear width |

Modeling rule:

```text
road_type + lane_count + lane_width + fire_access flag
```

Do not draw arbitrary gray road slabs without lane/fire/service logic.

## Fast TEP Approximation Card

Use only for early massing comparison, not final legal TEP.

```text
footprint_area = closed_footprint_area
gross_above_ground_area = sum(floor_plate_area_i)
simple_gfa = footprint_area * floor_count
approx_total_height = ground_floor_height + (floors - 1) * typical_floor_height + roof/crown/technical extras
far_like_ratio = gross_above_ground_area / plot_area
core_ratio = core_area / typical_floor_plate_area
```

Efficiency placeholders:

| Function | Early usable/rentable hint |
| --- | ---: |
| Office up to 50 m | about 0.75-0.80 rentable/GFA |
| Office up to 100 m | about 0.69-0.73 rentable/GFA |
| Office above 100 m | often about 0.60-0.65, project-specific |
| Residential | do not infer saleable area without apartment mix and corridor/core logic |

Always report:

```text
calculation_type: early_massing_approximation
not_checked: legal GFA, fire, daylight/INSO, parking, MEP, lift traffic
```

## Warning Flags To Print

Print these flags into the model report or ground label when triggered:

- `office_above_50m_needs_high_rise_fire_placeholder`
- `residential_above_75m_needs_high_rise_fire_placeholder`
- `above_28m_needs_non_low_rise_stair_core_assumption`
- `office_core_to_glass_above_15m_warn`
- `residential_facade_to_corridor_above_9m_warn`
- `occupied_roof_guard_below_1_2m_warn`
- `fire_access_width_below_required_warn`
- `tep_is_approximation_not_legal_area_warn`

## How To Use With RhinoMCP

```text
read quick card
-> build metric_pack
-> use docs/tools/rhino/rhino-mcp-command-library.md
-> run one RhinoCommon script through mcp__rhino.run_python/run_csharp
-> write warnings to report/user message, not as noisy visible geometry
-> hide helper layers before final review
```
