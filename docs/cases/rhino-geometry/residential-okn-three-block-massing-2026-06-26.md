# Residential OKN Three-Block Massing 2026-06-26

Date: 2026-06-26

Status: draft active

Scenario: 3A

Case family: rhino-geometry

## AI Extraction Summary

```yaml
case_family: rhino-geometry
use_when: "given residential footprints plus protected/public OKN block need first-pass modern ЖК massing"
source_authority: "user sketch: red plot boundary, three blue residential footprints, orange OKN brick gable public building"
geometry_grammar: "three residential blocks frame a central courtyard and diagonal public spine; OKN remains low brick gable house with public plaza"
effective_rhino_gh_route: "dependency-free Python OBJ generator; import OBJ into Rhino or port dimensions into RhinoCommon for live .3dm build"
key_parameters:
  units: meters
  residential_floors: "10-16 typical, 17 not used in v1"
  residential_f2f_m: 3.15
  ground_floor_m: 4.2
  max_height_m: 51.6
  approximate_residential_gfa_m2: 164104
  okn_size_m: "34 x 16"
  okn_ridge_h_m: 10.8
promoted_rules:
  - "for fixed ЖК footprints, classify as Scenario 3A and keep footprints/OKN as source authority"
  - "use height stepping and top setbacks to make modern residential massing without inventing new zoning"
  - "preserve an OKN public plaza and do not bury the heritage block inside residential mass"
failure_gates:
  - "no surveyed scale or legal OKN protection zone yet"
  - "INSO, daylight, fire access, parking, and code checks are not validated"
  - "residential depth is massing-level only, not apartment plan validation"
validation: "script-generated OBJ/MTL/report; height below 75 m residential high-rise threshold; report includes GFA, floor counts, warnings"
read_more_when: "building first-pass ЖК massing from a footprint sketch with a retained public/heritage low block"
related_scripts:
  - "scripts/rhino/massing/residential_okn/build_residential_okn_massing.py"
```

## Source Authority

- Text: user requested three residential blocks plus orange OKN block.
- Plan/top: user sketch shows red plot boundary, three blue hatched residential
  footprints, and orange OKN in the south-west part of the plot.
- Elevation/facade: none provided.
- Rhino scene/layers: none provided.
- User feedback: OKN is a brick gable-roof building with public function.

## Goal

Create a first-pass massing for a modern residential complex while preserving
the given footprint logic and making the OKN block legible as a low public
heritage/public building, not as residual service mass.

## Input State

- Files: user-provided image in chat.
- Rhino slot/document: not connected in this session.
- Existing layers/variants: none.
- Units: meters, inferred scale because no survey/CAD dimensions were provided.

## Massing Logic

The case is Scenario `3A`: footprints and OKN position are source authority.
The generator does not move the three residential building families. It assigns
heights and simple form operators:

- north large perimeter/courtyard block: 14-16 floors;
- east L-shaped block: 13-15 floors;
- south L-shaped lower block: 10-11 floors;
- OKN: 34 x 16 m brick public building with 6.8 m wall and 10.8 m ridge;
- public logic: central courtyard, diagonal public spine, and OKN plaza.

Applied operators:

- top-floor setbacks on residential bars;
- height stepping from lower south block to higher north/east blocks;
- public-spine and courtyard preservation;
- low OKN contrast against residential mass.

## Metrics Snapshot

```yaml
units: meters
residential_footprint_area_m2: 11942
residential_approx_gfa_m2: 164104
max_residential_height_m: 51.6
residential_f2f_m: 3.15
ground_floor_m: 4.2
top_floor_m: 3.3
visual_lift_m: 0.001
```

The current height band remains below the 75 m residential high-rise threshold
from the dimensional library, so the first pass avoids high-rise residential
core/fire assumptions.

## What Worked

- The new repo folder structure made placement clear:
  `docs/cases/rhino-geometry/` for the case and
  `scripts/rhino/massing/residential_okn/` for the generator.
- The massing uses fixed footprints as source authority instead of inventing
  a new site plan.
- OKN is modeled as a small public brick house with a gable roof and a separate
  plaza, so it remains distinct from the residential mass.
- Height stepping and top setbacks create a modern ЖК image without turning the
  first pass into facade/detail design.
- The generator writes a JSON report with assumptions and warnings.

## What Failed / Not Validated Yet

- No surveyed plot or footprint dimensions were provided; scale is inferred
  from the image and must be replaced with CAD dimensions.
- No INSO/daylight, fire access, parking, evacuation, or legal OKN protection
  zone checks were run.
- Residential bars are massing-depth placeholders. They are not yet divided
  into sections, cores, stair/lift groups, or apartment plans.
- OBJ is a portable preview, not a native `.3dm` with Rhino layers/materials.

## Promoted Patterns

| Pattern | Destination | Action |
| --- | --- | --- |
| OKN public anchor inside residential complex | `docs/libraries/massing/site-planning-pattern-library.md` | add after one more validated case |
| Fixed-footprint ЖК height stepping | `docs/libraries/massing/form-operator-library.md` | already covered by setback/terrace and height strategy |

## Promoted Errors

| Error | Destination | Gate |
| --- | --- | --- |
| Treating OKN as leftover object | future massing error library | OKN must have plaza/address/protection space before residential massing is accepted |
| Accepting inferred scale as final | `docs/error-ledger.md` if repeated | replace sketch scale with CAD/survey dimensions before approval or TEP claims |

## Reusable Workflow

```text
classify as Scenario 3A
-> lock residential footprints and OKN block as source authority
-> set metric assumptions from 2026 residential dimensional defaults
-> choose height bands below high-rise threshold for first pass
-> preserve central courtyard / public spine / OKN plaza
-> generate clean massing preview and JSON metrics
-> report unvalidated gates explicitly
-> only then refine in Rhino with exact CAD dimensions
```

## Validation

- Numeric: generated report gives footprint area, approximate GFA, floor counts,
  max height, OKN dimensions, and warnings.
- Visual: OBJ preview separates residential, OKN brick, OKN roof, courtyard,
  public spine, and plaza materials.
- Source-derived: source sketch proportions are preserved at first-pass scale;
  exact CAD dimensions are not available.
- RhinoMCP/tooling: no live Rhino slot was used; output is OBJ/MTL plus JSON
  report.

## Links

- `scripts/rhino/massing/residential_okn/build_residential_okn_massing.py`
- `exports/residential-okn-massing/residential_okn_massing_v1.obj`
- `exports/residential-okn-massing/residential_okn_massing_v1_report.json`
- `docs/workflows/massing/tep-massing-scenario-subtypes.md`
- `docs/libraries/standards/moscow-building-dimensional-library-2026.md`
- `docs/libraries/massing/form-operator-library.md`

