# Moscow Building Dimensional Library 2026

Status: active reference, checked on 2026-06-23.

Use this before generating Moscow residential or office massing, Grasshopper
floor stacks, early TEP models, facade grids, or core placeholders.

This is not a replacement for project-specific code review, fire strategy,
structural design, lift traffic calculation, daylight calculation, or MEP
coordination. It is a fast baseline for 1:1 meter models and AI/Rhino/GH
geometry that should not start from fantasy dimensions.

## Source Hierarchy

Treat values in this file as one of three types:

| Type | Meaning | Use |
| --- | --- | --- |
| `normative` | Directly tied to active Russian SP/GOST source found in the 2026 check | Must be respected or explicitly rechecked |
| `practice heuristic` | Common early-stage architecture/engineering range from design references or practice | Good default for massing, not final compliance |
| `generator default` | A conservative parameter for AI/Rhino/Grasshopper scripts | Safe first pass only |

Key active sources checked:

- SP 54.13330.2022 for residential buildings, with changes 1 and 2 active in
  2026.
- SP 118.13330.2022 for public buildings, including office/public functions,
  with changes through 5.
- SP 160.1325800.2014 for multifunctional buildings, used with SP 54, SP 118,
  SP 113, SP 59, and other base standards.
- SP 1.13130.2020 for evacuation routes and exits, as referenced by SP 118 for
  public/office evacuation design. Use the active amendments before treating
  core/stair count as a compliance claim.
- SP 267.1325800.2016 for high-rise buildings and complexes, revision active
  from 2025-01-28.
- SP 477.1325800.2020 for high-rise fire-safety requirements.
- SP 17.13330.2017 for roofs.
- SP 367.1325800 and SP 52.13330 for natural lighting.
- GOST 23166-2024 for window and balcony blocks.

Historical Moscow high-rise material such as MGSN 4.19-2005 is useful only as
context; it is not active.

## First Classification Gate

Before creating geometry, classify the building:

| Function / height | Rule |
| --- | --- |
| Residential up to 75 m | Start from SP 54.13330.2022. |
| Residential above 75 m | Apply high-rise fire logic from SP 477 and high-rise design logic from SP 267 in addition to residential rules. |
| Office / public up to 50 m | Start from SP 118.13330.2022. |
| Office / public above 50 m | Treat as high-rise for fire strategy under SP 477 and check SP 267 applicability. |
| Multifunctional | Use SP 160 as the routing layer, then apply the standards for each function. |
| Any building above 28 m fire-technical height | Do not use low-rise stair/core assumptions; smoke protection and evacuation strategy become a core driver. |

Fire-technical height is not the same as just "number of floors x floor height";
for review, determine it from fire-appliance access level to the relevant
occupied/opening/roof mark according to fire rules.

## Office Towers

### Height And Floor Count

| Class | Typical early massing range | Notes |
| --- | --- | --- |
| Low / mid office | 6-12 floors, about 25-50 m | Usually no high-rise fire category by height. |
| High-rise office | 13-35 floors, about 50-145 m | SP 477 threshold is crossed above 50 m. |
| Tall office tower | 35-60 floors, about 145-250 m | Requires lift zoning, refuge/fire compartments, technical floors, and structural strategy. |
| Very tall / landmark | 60+ floors | Never model as a simple extruded plate without zones, outriggers/tech floors, and sky/evacuation logic placeholders. |

### Floor Heights

| Element | Range, m | Type | Notes |
| --- | ---: | --- | --- |
| Typical office floor-to-floor | 3.9-4.2 | practice heuristic | Good base for Moscow Class A / B+ massing. |
| Premium / high-spec office floor-to-floor | 4.2-4.5 | practice heuristic | Use when raised floor, larger plenum, or expressive facade module is intended. |
| Public rooms clear height | 3.0 min | normative | SP 118 sets a 3 m baseline for rooms with permanent/mass occupancy unless a specific room type says otherwise. |
| Ground lobby / retail | 4.5-6.0 | practice heuristic | Use 5.4 m as generator default if first floor is active/public. |
| Technical / mechanical floor | 3.0-4.5 | practice heuristic | Place every 20-30 office floors or at zone transfers in tall towers. |
| Crown / plant screen | 3.0-8.0 | practice heuristic | Model separately from counted tenant floors. |

### Plans, Lease Depth, And Cores

| Parameter | Range | Type | Notes |
| --- | ---: | --- | --- |
| Efficient tower floor plate | 900-1800 m2 | practice heuristic | Below 900 m2 can be boutique/slender; above 1800 m2 needs careful core/daylight planning. |
| Large low-rise / podium office plate | 1500-3000 m2 | practice heuristic | Better as slab/podium than tower. |
| Core-to-glass depth | 10-14.5 m | practice heuristic | 12.8 m is a good private-office target; 14.3 m suits open workstation layouts. |
| Office around atrium commercial band | 15-18 m | practice heuristic | Use when atrium layout drives the plan. |
| Naturally ventilated office total width | 12-15 m | practice heuristic | Narrower plate, two spans around corridor. |
| Typical structural grid | 8.4, 9.0, 10.5 m | practice heuristic | 7.5 m and 15 m grids also appear in steel office concept design. |
| Facade planning module | 1.35, 1.5, 1.8 m | practice heuristic | 1.5 m default; align rooms, mullions, ceiling grid, and furniture. |

Core placeholders:

| Tower height | Core placeholder | Notes |
| --- | --- | --- |
| 6-12 floors | 12 x 18 m to 16 x 22 m | 2 stairs, 2-4 lifts, toilets/shafts. |
| 13-35 floors | 16 x 22 m to 22 x 30 m | 2 stairs, 4-8 passenger lifts, service/fire lift placeholder. |
| 35-60 floors | 22 x 30 m to 30 x 42 m | Lift zoning and transfer/technical floors likely. |
| 60+ floors | 30 x 42 m and up | Do not guess final core; run traffic/fire/structure study. |

Core count quick gate for early office massing:

- Start with one core zone only when the typical floor plate is compact enough
  that the core-to-glass depth stays near `12.5-14.0 m` and the floor plate
  does not create long dead-end office wings.
- Do not derive required core count from a graphic 50/50 area split. Core count
  is an evacuation/fire/project-strategy gate: check SP 1.13130 / SP 118 route,
  occupant load, travel distance, floor area, height/fire category, and project
  brief before treating one or two cores as accepted.
- Do not encode a single "second core from N m2" rule for all office/public
  buildings. For common public/administrative fire classes, SP 1.13130.2020 is
  primarily an evacuation-exit, occupant-count, travel-distance, and fire-
  strategy check. Basement/cellar area thresholds are a separate case and
  should not be copied to normal office floors.
- In early massing, translate the code check into "prove independent
  evacuation exits/directions and plausible stair/core zones", not
  automatically into two identical full cores.
- For elongated plates above roughly `3000 m2`, or stepped/slab buildings where
  one core would sit far from a large part of the plan, test two core zones
  before placing roof access volumes.
- After two or more cores are selected, equal-area service-zone splitting can
  be used as a first-pass placement heuristic. It is not a legal or universal
  rule; tenant divisions, fire compartments, entry locations, structure, and
  travel distances may require unequal service zones.
- Do not place one visible roof access box on every terrace. Place roof exits
  only where a plausible vertical core/service zone reaches an operated roof.
- Keep core zones inside broad internal bands. They should organize corridor /
  service logic, not create narrow leftover strips or touch the facade.

## Residential Towers

### Height And Floor Count

| Class | Typical early massing range | Notes |
| --- | --- | --- |
| Mid-rise residential | 9-17 floors | Typical city block massing range. |
| Upper non-high-rise residential | 18-25 floors, up to about 75 m depending floor height | SP 54 scope is up to 75 m. |
| High-rise residential | 25-45 floors, above 75 m | SP 477 high-rise fire threshold for F1.3 is crossed above 75 m. |
| Landmark residential | 45+ floors | Requires explicit lift zoning, fire strategy, wind/structure assumptions, and technical floors. |

### Floor Heights

| Element | Range, m | Type | Notes |
| --- | ---: | --- | --- |
| Typical residential floor-to-floor | 3.0-3.15 | practice heuristic | Good mass-market / comfort base. |
| Business / premium residential floor-to-floor | 3.15-3.45 | practice heuristic | Use 3.3 m for better facade and clear-height margin. |
| High-end / penthouse floor-to-floor | 3.45-4.2 | practice heuristic | Use selectively for top floors, not whole tower unless brief says so. |
| Ground floor lobby/commercial | 3.6-5.4 | practice heuristic | 4.2 m default for residential lobby; 5.4 m if retail. |
| Technical floor | 2.4-3.6 | practice heuristic | Place at roof, basement interface, and tall-tower zones as needed. |

### Plans, Apartment Depth, And Cores

| Parameter | Range | Type | Notes |
| --- | ---: | --- | --- |
| Efficient residential tower floor plate | 500-900 m2 | practice heuristic | Good default for one section/tower. |
| Large residential tower floor plate | 900-1200 m2 | practice heuristic | Use only with many apartments or split core/wing logic. |
| Apartment depth from facade to corridor/core | 6-9 m | practice heuristic | 7.5 m default; deeper plans need careful daylight and room layout. |
| Double-loaded residential slab total depth | 14-18 m | practice heuristic | Includes corridor/core band. |
| Premium corner / through-unit depth | 8-12 m | practice heuristic | Requires better aspect and daylight strategy. |
| Residential facade bay | 3.0-3.6 m | practice heuristic | 3.3 m default; 2.7 m is tight bedroom bay; 4.2 m living bay. |
| Loggia / balcony projection | 1.2-1.8 m | practice heuristic | Model only when brief requires balcony massing. |

Core placeholders:

| Fire-technical height / floors | Core placeholder | Notes |
| --- | --- | --- |
| Below 28 m | 8 x 12 m to 10 x 14 m | Low-rise assumptions only; still check stairs/lifts/accessibility. |
| About 28-75 m | 10 x 14 m to 14 x 20 m | 2 lifts plus protected stair strategy is a common placeholder, but project rules decide. |
| Above 75 m | 14 x 20 m to 20 x 30 m | High-rise fire, lift, smoke-control, and evacuation logic drive the core. |
| 45+ floors | project-specific | Add lift zones, technical floors, refuge/fire compartments where required. |

## Facade-To-Core Depth Gate

Use this gate before making a floor plate:

| Function | Good default | Soft limits |
| --- | ---: | --- |
| Office core-to-glass | 12.5-14.0 m | Below 10 m is inefficient; above 15 m usually hurts daylight/workplace quality unless atrium or special layout is used. |
| Residential facade-to-corridor/core | 7.0-8.5 m | Below 6 m is shallow; above 9 m risks deep rooms unless corner/through-unit logic is used. |
| Public/retail podium | 10-18 m bay/depth modules | Depends heavily on tenant, structure, and egress. |

SP 367 daylight logic is the hard reminder: for side daylight in multi-storey
public and residential buildings, the room-depth-to-window-top-height ratio is a
first-pass constraint. Do not let a massing generator create deep rooms and then
assume daylight works.

## Slabs, Services, And Floor Build-Ups

These are early massing/package values. Structural engineer, fire rating,
acoustics, vibration, spans, facade loads, and MEP concept can shift them.

| Function | Structural slab | Floor build-up | Ceiling / plenum | Total above clear height |
| --- | ---: | ---: | ---: | ---: |
| Residential typical | 180-220 mm | 60-120 mm | 50-150 mm | 300-500 mm |
| Residential wet / acoustic zones | 200-250 mm | 100-180 mm | 100-200 mm | 450-650 mm |
| Office typical | 200-280 mm | 100-150 mm raised floor | 450-700 mm | 750-1100 mm |
| Office low-services / exposed ceiling | 200-280 mm | 60-120 mm | 0-250 mm | 300-650 mm |
| Retail / podium | 250-350 mm | 100-200 mm | 600-1200 mm | 950-1700 mm |
| Parking | 220-320 mm | topping/slope as needed | services local | project-specific |

Raised floors can be very shallow for cable distribution, but air-distribution
underfloor systems need substantially more depth. For generator defaults, use
120 mm raised floor for office and 600 mm ceiling/services unless the brief says
exposed services or UFAD.

## Roofs, Parapets, And Operated Roofs

| Element | Range | Type | Notes |
| --- | ---: | --- | --- |
| Non-operated flat roof total build-up | 200-450 mm | practice heuristic | Slope layer, vapor barrier, insulation, waterproofing, protection. |
| Operated terrace build-up | 300-600 mm | practice heuristic | Add drainage/protection and paving/slabs. |
| Intensive green roof build-up | 450-900+ mm | practice heuristic | Depends on substrate depth, vegetation, irrigation, drainage. |
| Flat roof slope | 1.5-3% | practice heuristic | Use for drainage arrows/slope geometry, not detailed design. |
| Insulation placeholder | 150-250 mm mineral/PIR equivalent | practice heuristic | Product/system can vary; TechnoNICOL PIR example may be around 110 mm for a specified resistance. |
| Pavers on operated roof | 40-60+ mm | practice heuristic / product guidance | Use 60 mm for robust terrace placeholder. |
| Non-accessible parapet / upstand | 0.6-0.9 m | practice heuristic | Recheck SP 17 and fire/roof safety details. |
| Accessible roof guard/parapet | 1.2 m | practice heuristic | Use 1.2 m generator default for occupied roof edges. |
| AI massing inset parapet edge setback | 0.5-0.7 m | generator default | Keeps a readable roof coping/border outside the parapet in Rhino review models. |
| AI massing parapet thickness | 0.32-0.42 m | generator default | Use for solid guard/parapet rings from `DupBorder -> setback -> Offset x2 -> Extrude`. |
| Plant screen / roof equipment enclosure | 1.5-3.0 m | practice heuristic | Model as separate screen, not as tenant floor. |

## Openings, Windows, And Facade Grids

### Residential

| Parameter | Range / rule | Type | Notes |
| --- | --- | --- | --- |
| Window opening area to floor area | not more than 1:5.5 and not less than 1:8 | normative | SP 54 living rooms and kitchens; inclined top-floor openings not less than 1:10. |
| Bedroom window | 0.9-1.5 m wide, 1.4-1.8 m high | practice heuristic | Use with 2.7-3.3 m room bay. |
| Living room window | 1.5-2.4 m wide, 1.5-2.2 m high | practice heuristic | Wider/panoramic for premium. |
| Panoramic glazing | 2.1-2.7 m high | practice heuristic | Needs facade, overheating, guard, and fire checks. |
| Sill height | 0.45-0.9 m | practice heuristic | 0.6 m default for residential massing; 0.9 m for conservative windows. |
| Balcony door | 0.8-1.0 m wide, 2.1-2.4 m high | practice heuristic | Model when balconies/loggias exist. |

### Office / Public

| Parameter | Range | Type | Notes |
| --- | ---: | --- | --- |
| Curtain wall module | 1.35, 1.5, 1.8 m | practice heuristic | 1.5 m default. |
| Vision glass height | 1.4-2.4 m | practice heuristic | Coordinate with floor-to-floor and spandrel. |
| Spandrel / opaque band | 0.8-1.2 m | practice heuristic | Can shrink with high-performance facade but keep slab/service zone plausible. |
| Operable vent panel | project-specific | practice heuristic | Do not assume operability in high-rise facade without fire/MEP strategy. |
| AI facade panel visual outset | 0.06-0.10 m | generator default | Use only after panel/opening is generated from the local facade plane; prevents same-tone panels from disappearing in Rhino views. |
| BC ground-floor retail/cafe glazing | 3.5-4.8 m high visual panel | generator default | Use with 5.4 m active ground floor; larger and closer to floor than upper-office windows. |

GOST 23166-2024 is the current general window/balcony block standard. Do not use
old fixed window-size tables as if they were current design requirements; use
them only as historical/module context.

## Generator Defaults

Use these values when the user gives a vague massing request and no stricter
brief exists.

### Office Tower Default

```yaml
function: office
city: Moscow
units: meters
floors:
  podium: 2
  tower: 32
floor_heights:
  ground: 5.4
  podium: 4.5
  office_typical: 4.05
  technical: 4.2
floor_plate:
  tower_width: 42
  tower_depth: 32
  target_plate_area_m2: 1344
core:
  width: 18
  depth: 24
  core_to_glass_target: 12.5
structure:
  grid_primary: 8.4
  facade_module: 1.5
floor_package:
  slab: 0.25
  raised_floor: 0.12
  ceiling_services: 0.60
roof:
  build_up: 0.45
  parapet: 1.2
```

### Residential Tower Default

```yaml
function: residential
city: Moscow
units: meters
floors:
  podium: 1
  tower: 24
floor_heights:
  ground: 4.2
  residential_typical: 3.15
  top: 3.3
floor_plate:
  tower_width: 34
  tower_depth: 26
  target_plate_area_m2: 884
core:
  width: 12
  depth: 16
  facade_to_corridor_target: 7.5
structure:
  facade_bay: 3.3
floor_package:
  slab: 0.20
  floor_build_up: 0.10
  ceiling_services: 0.10
roof:
  build_up: 0.40
  parapet: 1.2
windows:
  residential_default_width: 1.5
  residential_default_height: 1.65
  sill: 0.6
```

## Grasshopper / Rhino Usage Pattern

1. Inspect Rhino units. If the model is not meters, stop and convert/ask.
2. Classify function and fire-technical height band.
3. Pick a preset from this library, then expose every dimensional assumption as
   a slider/input.
4. Generate footprint, core, floor stack, roof/parapet, and facade grid as
   separate named layers/outputs.
5. Compute at minimum: footprint area, GBA/GFA placeholder, rentable/residential
   plate efficiency, total height, core area ratio, facade-to-core depth, and
   floor count.
6. Add warning panels for any value outside this library's soft limits.
7. Only then bake Rhino geometry.

## Quick Validation Flags

Stop or warn if:

- office tower above 50 m is modeled without high-rise/fire placeholder logic;
- residential tower above 75 m is modeled with a small low-rise core;
- any building above 28 m keeps a simple low-rise stair assumption;
- office core-to-glass is above 15 m without atrium/special plan;
- residential facade-to-corridor depth is above 9 m without daylight strategy;
- office floor-to-floor is below 3.9 m while using raised floor and full plenum;
- residential floor-to-floor is below 3.0 m without clear-height verification;
- roof is occupied but parapet/guard is below 1.2 m in the model;
- facade grid is unrelated to structure, room bays, or floor height.

## Sources

- SP 54.13330.2022 active status and scope:
  https://www.gostinfo.ru/catalog/Details/?id=6900862 and
  https://tiflocentre.ru/documents/sp_54.13330.2022.php
- SP 54.13330.2022 change 2:
  https://normativ.kontur.ru/document?documentId=489823&moduleId=9
- SP 118.13330.2022 and change 5:
  https://tiflocentre.ru/documents/sp-118-13330-2022.php and
  https://normativ.kontur.ru/document?documentId=488894&moduleId=9
- SP 1.13130.2020 evacuation routes and exits:
  https://tiflocentre.ru/documents/sp-1-13130-2020.php
- SP 267.1325800.2016 high-rise design, revision active from 2025-01-28:
  https://tk-expert.ru/lib/1087/ and
  https://nav.tn.ru/documents/regulatory/ast_s_sp_267_1325800_2016/
- SP 477.1325800.2020 high-rise fire safety:
  https://vniipo-help.ru/data/uploads/sp-477.1325800.2020.pdf
- SP 17.13330.2017 roofs:
  https://meganorm.ru/Data2/1/4293744/4293744728.pdf and
  https://nav.tn.ru/documents/regulatory/ast_s_sp_17_13330_2017/
- SP 367 daylight depth/window-top rule:
  https://meganorm.ru/Data2/1/4293735/4293735697.htm
- GOST 23166-2024 window and balcony blocks:
  https://normativ.kontur.ru/document?documentId=493996&moduleId=9
- Office planning depth references:
  https://urbanland.uli.org/office/pillars-of-design and
  https://steelconstruction.info/Multi-storey_office_buildings
- Office structural/service concept references:
  https://www.steelconstruction.info/Concept_design and
  https://constructalia.arcelormittal.com/files/MSB02%20Concept%20Design--3193df3624346e5b7299792599e90933.pdf
