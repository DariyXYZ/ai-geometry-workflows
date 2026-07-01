# TEP Calculation Patterns

Status: active early-massing calculation library.

Use this for quick TEP/GFA/FAR/height/efficiency checks during Scenario 3
massing. It is not a substitute for project-specific legal area calculation,
fire strategy, daylight/INSO, parking, MEP, or lift traffic calculation.

The goal is to keep AI-generated massing numerically plausible and comparable
between variants.

## Read With

- `docs/libraries/standards/moscow-massing-metric-quick-cards.md`
- `docs/libraries/standards/moscow-building-dimensional-library-2026.md`
- `docs/libraries/standards/moscow-building-dimensional-library-2026.yaml`
- `docs/libraries/standards/moscow-road-dimensional-library-2026.md`
- `docs/workflows/massing/tep-massing-scenario-subtypes.md`

## Calculation Types

Always label which calculation type is being used.

| Type | Meaning | Use |
| --- | --- | --- |
| `early_massing_approximation` | Gross floor area from modeled floor plates or footprint x floors | Fast variant comparison |
| `model_area_report` | Area derived from actual Rhino curves/surfaces by layer | Better than guesswork, still not legal TEP |
| `legal_tep_review` | Project-specific code/accounting method | Only when the user provides source rules/data |

Do not present early massing approximation as approved legal GFA.

## Required Inputs

Minimum:

```yaml
plot_area_m2:
function: office | residential | mfc | public | mixed | unknown
footprints:
  - id:
    area_m2:
    floors:
    floor_height_m:
height_limit_m:
calculation_type: early_massing_approximation
```

Better:

```yaml
above_ground_floor_plates:
  - level:
    area_m2:
    function:
    counted: true | false | unknown
below_ground_area_m2:
podium_area_m2:
tower_area_m2:
core_area_m2:
parking_area_m2:
operated_roof_area_m2:
```

## Core Formulas

### Area

```text
footprint_area_m2 = closed_curve_area
simple_gross_area_m2 = footprint_area_m2 * floor_count
gross_above_ground_area_m2 = sum(area of counted above-ground floor plates)
gross_total_area_m2 = gross_above_ground_area_m2 + below_ground_area_m2
far_like_ratio = gross_above_ground_area_m2 / plot_area_m2
```

Use `far_like_ratio`, not "FAR", unless the project's legal FAR/GFA definition
is known.

### Height

```text
height_m =
  ground_floor_height_m
  + (typical_floor_count - 1) * typical_floor_height_m
  + technical_floor_height_m
  + crown_or_plant_screen_height_m
```

If the first floor is not special:

```text
height_m = floor_count * typical_floor_height_m + roof_extra_m
```

Estimate floors from height:

```text
floor_count =
  1 + floor((height_limit_m - ground_floor_height_m - roof_extra_m) / typical_floor_height_m)
```

Always report assumptions for `ground_floor_height_m`, `typical_floor_height_m`,
and `roof_extra_m`.

### Plate Efficiency

```text
core_ratio = core_area_m2 / typical_floor_plate_area_m2
net_like_area_m2 = gross_above_ground_area_m2 * efficiency_placeholder
```

Do not infer saleable residential area without apartment mix, corridor scheme,
balconies/loggias, technical zones, and accounting rules.

Office placeholder efficiency:

| Height band | Rentable / GFA placeholder |
| --- | ---: |
| Up to 50 m | 0.75-0.80 |
| Up to 100 m | 0.69-0.73 |
| Above 100 m | 0.60-0.65, project-specific |

## Variant Comparison Table

Every generated variant should be comparable with this table:

| Field | How to compute |
| --- | --- |
| `plot_area_m2` | source boundary area |
| `built_footprint_area_m2` | sum footprint curves that touch ground/podium |
| `footprint_coverage_ratio` | built footprint / plot area |
| `gross_above_ground_area_m2` | sum counted floor plates |
| `far_like_ratio` | gross above-ground area / plot area |
| `floor_count_max` | maximum above-ground floor count |
| `height_max_m` | maximum model bbox height, excluding labels/helpers |
| `typical_floor_height_m` | from metric pack |
| `core_count` | planned core zones |
| `core_ratio_typical` | core area / typical plate area |
| `fire_access_width_m` | minimum modeled clear fire/service access width |
| `warnings` | warning flags triggered |

## Scenario Patterns

### 3A - Approved Footprints / Build Form

Use source footprint areas as hard anchors:

```text
for each footprint:
  floor_count = selected from height / TEP / design intent
  gross_area = footprint_area * floor_count
```

Allowed changes:

- height distribution;
- setbacks;
- roof/crown;
- core placement;
- public/entry accents.

Forbidden unless user asks:

- moving or resizing approved footprints to satisfy TEP.

### 3B - Plot Plus Entries / Zoning First

Before modeling, propose:

```yaml
buildable_bands:
public_spine:
service_edge:
open_space_type:
target_coverage_range:
target_height_band:
```

TEP is a pressure check, not the first drawing:

```text
required_average_floors = target_gross_area / proposed_total_footprint_area
```

If required average floors are unrealistic for the site, revise footprint family
or height strategy before detailed architecture.

### 3C - Existing Massing Revision

Preserve scale:

```text
source_gross_area_approx = source_footprint_area * source_floor_count
new_gross_area_approx should stay within agreed tolerance
```

Default tolerance:

- `+/- 5%` if the user wants same TEP scale;
- `+/- 10%` if the user asks for a looser image/form revision.

### 3D - Checklist Review

Separate review streams:

```text
design_approval_checklist
TEP / area arithmetic
norm/code assumptions
```

Do not reduce the architecture score just because a TEP value is missing. Mark
TEP as `not_enough_data` unless the model/source contains enough evidence.

## Parking Placeholder

Parking is too project-specific for a universal legal formula. Use this only to
reserve massing space and flag risk:

```yaml
parking:
  required_spaces: unknown
  source_rule: not_provided
  modeled_parking_area_m2:
  assumed_area_per_space_m2: 28-35
  levels_needed_approx: modeled_or_required_area / basement_plate_area
  warning: parking_not_verified
```

Use `28-35 m2/place` only as an early geometry allowance for parking module,
ramps, drive aisles, structure, and circulation. Do not report it as a Moscow
requirement unless the project's parking norm/source is provided.

## Warning Flags

Trigger these flags automatically when inputs are known:

| Flag | Condition |
| --- | --- |
| `tep_is_approximation_not_legal_area_warn` | Any non-legal calculation is used |
| `height_exceeds_limit_warn` | modeled height > source height limit |
| `target_gfa_unmet_warn` | gross area differs from target beyond tolerance |
| `required_average_floors_high_warn` | target GFA requires implausibly high floors for site/context |
| `office_above_50m_needs_high_rise_fire_placeholder` | office/public height > 50 m |
| `residential_above_75m_needs_high_rise_fire_placeholder` | residential height > 75 m |
| `above_28m_needs_non_low_rise_stair_core_assumption` | fire-technical height likely > 28 m |
| `fire_access_width_below_required_warn` | modeled access width below quick-card fire access rule |
| `parking_not_verified_warn` | parking source rule or count missing |
| `inso_not_checked_warn` | massing changed and INSO/daylight not checked |

## Rhino / Grasshopper Output Contract

For any script or GH node that reports TEP:

```yaml
units: meters
calculation_type: early_massing_approximation
inputs:
  plot_area_m2:
  footprint_areas_m2:
  floor_counts:
  floor_heights_m:
outputs:
  gross_above_ground_area_m2:
  far_like_ratio:
  height_max_m:
  warnings:
not_checked:
  - legal_gfa
  - fire_strategy
  - daylight_inso
  - parking_norm
  - lift_traffic
  - mep
```

Keep this report as text/JSON on a report layer or external file. Do not clutter
the Rhino viewport with large metric boards unless the user asks for a visible
comparison board.
