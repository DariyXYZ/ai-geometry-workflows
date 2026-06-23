# Moscow Road Dimensional Library 2026

Use this library when drawing streets, driveways, service roads, fire access,
parking edges, and schematic road context for Moscow architecture massing.

Status: active CAD defaults, not a substitute for transport design.

Last checked: 2026-06-24.

## Source Hierarchy

1. Moscow regional planning norms: Government of Moscow resolution No. 945-PP,
   current public PDF edition dated 2025-09-01.
2. Federal urban road geometry: `SP 42.13330.2016`, tables 11.2 and 11.6.
3. Urban street design rules: `SP 396.1325800.2018`.
4. Fire access: `SP 4.13130.2013`, section 8.
5. Moscow street improvement standards are useful for visual/street-space
   character, but geometry for vehicle lanes should still be checked against
   the planning and SP documents above.

## Important Interpretation

Moscow norms do not give one universal "Moscow street width." The 2025 edition
of Moscow 945-PP says street and road width is determined by calculation based
on vehicle and pedestrian intensity and on the elements placed in the cross
section. Red-line width is fixed by planning documentation.

For early Rhino/Grasshopper massing, use the CAD defaults below as realistic
schematic dimensions, then mark them as `needs_transport_check` if the road is
part of a real approval package.

## Lane Widths For Schematic Moscow Models

| Element | CAD default | Range / minimum | Use in massing |
| --- | ---: | ---: | --- |
| Main city road / express class lane | 3.75 m | 3.50-3.75 m | Major arterials, high-speed city roads, large context roads |
| General magistral street lane | 3.50 m | 3.25-3.75 m | Most urban arterial context roads |
| Right lane on magistral streets/roads | 3.75 m | use 3.75 m | Use when drawing outer/right lane on major streets |
| District magistral street lane | 3.50 m | 3.25-3.75 m | 2-4 lane district collectors |
| Local street lane, residential / public-business / retail zones | 3.25 m | 3.0-3.5 m | Default for site-adjacent city streets |
| Production / warehouse area lane | 3.75 m | 3.5 m typical; 3.75-4.0 m for two-lane industrial streets | Trucks, logistics, industrial service context |
| Main internal driveway / quarter driveway | 3.0 m per lane | carriageway not less than 6.0 m for quarter driveways | Two-way internal access around blocks |
| Secondary one-way driveway | 3.5 m | 3.5 m one lane in SP 42 table 11.6 | Only for low-intensity one-way/local access, not as fire access for high-rise |
| Park road | 3.0 m per lane | 2 lanes | Park/service/ecological transport roads |
| Bus / trolleybus lane on major streets | 3.75 m | check project; 3.75 m is safe Moscow/magistral default | Dedicated or public transport priority lanes |
| Fire access, building height <= 13 m | 3.5 m | minimum | Fire truck access, low buildings |
| Fire access, building height > 13 m and <= 46 m | 4.2 m | minimum | Mid-rise fire access |
| Fire access, building height > 46 m | 6.0 m | minimum | High-rise office/residential massing; use for BC towers |
| Emergency stopping bay on constrained major city road | 3.0 m x 80.0 m | per SP 396 update | Only for detailed road context, not typical site driveway |

## Quick Carriageway Defaults

Use these for Rhino blockout when the road type is not yet fully specified.

| Road type | Width to draw | Composition |
| --- | ---: | --- |
| High-rise BC fire/service loop | 6.0-7.0 m | one shared two-way/fire-capable lane zone; avoid below 6 m |
| Standard two-way local street | 6.5-7.0 m | 2 x 3.25-3.5 m |
| Tight local access street | 6.0 m | 2 x 3.0 m, only when low speed and no heavy transport assumption |
| District street, 2 lanes | 7.0 m | 2 x 3.5 m |
| District street, 4 lanes | 14.0 m | 4 x 3.5 m |
| Major street, 4 lanes | 14.0-15.0 m | 4 x 3.5-3.75 m |
| Major street, 6 lanes | 21.0-22.5 m | 6 x 3.5-3.75 m |
| Industrial two-way truck street | 7.5-8.0 m | 2 x 3.75-4.0 m |
| One-way service lane, non-fire | 3.5-4.0 m | one lane, check turning and loading |

Do not draw arbitrary 10-12 m single gray roads without lane logic. A road
surface should usually be explainable as:

```text
lane_count * lane_width
+ edge strips / curb / gutter
+ parking / bus stop / loading if present
+ median / safety island if present
+ sidewalks / landscape strips if drawing full red-line section
```

## Red-Line Widths And Full Street Sections

For early massing, only draw full red-line width when the street corridor is
part of the site planning story. Otherwise draw carriageway plus sidewalks and
landscape bands only as visual context.

SP 42 gives broad reference widths for largest-city streets:

- magistral roads: 50-100 m in red lines;
- magistral streets: 40-100 m;
- local streets and roads: 15-30 m.

These are not default road pavement widths. They include the whole corridor:
carriageway, sidewalks, green strips, technical zones, possible medians,
parking/loading, transit elements, and utility space.

## Modeling Rules For Rhino / Grasshopper

1. Always name the road type in parameters:

   ```yaml
   road_type: local_street | district_street | magistral | service_drive | fire_access | park_road
   lane_count: integer
   lane_width_m: number
   carriageway_width_m: number
   fire_access: true | false
   needs_transport_check: true | false
   ```

2. For Moscow high-rise BC massing, any road used as fire access should be
   at least `6.0 m` clear because the building height is normally above 46 m.

3. Internal quarter driveways should not be below `6.0 m` when modeled as
   two-way access. Use `3.5 m` only for explicit one-way secondary driveways.

4. On magistral streets, use `3.75 m` for the outer/right lane and bus lane.
   Use `3.5 m` for quick schematic inner lanes unless a narrower `3.25 m`
   constrained condition is explicitly part of the story.

5. Draw curbs, sidewalks, parking bays, medians, and green strips as separate
   layers, not as one large road rectangle.

6. Apply the project visual-lift rule to road markings, lane stripes, crossings,
   curb-top paving, and other coplanar graphics:

   ```text
   VISUAL_LIFT_M = 0.001
   ```

7. Add turn radii only when the road function requires it. For a purely
   schematic context road, avoid over-modeling swept paths; for loading/fire
   access, flag `turning_radius_check_required`.

## Recommended Layers

```text
*_roads_carriageway
*_roads_lane_marking
*_roads_curbs
*_roads_sidewalks
*_roads_parking_loading
*_roads_fire_access
*_roads_landscape
*_roads_metrics
```

## Sources

- Government of Moscow, Resolution No. 945-PP, public PDF edition dated
  2025-09-01: https://www.mos.ru/upload/documents/files/5917/945-ppS1092025.pdf
- SP 42.13330.2016, tables 11.2 and 11.6:
  https://tiflocentre.ru/documents/sp42-13330-2016.php
- SP 396.1325800.2018:
  https://meganorm.ru/Data2/1/4293732/4293732357.htm
- SP 396.1325800.2018 amendment No. 2:
  https://meganorm.ru/mega_doc/norm/prikaz/14/izmenenie_N_2_k_sp_396_1325800_2018_ulitsy_i_dorogi.html
- SP 4.13130.2013 fire access summary:
  https://www.consultant.ru/document/cons_doc_LAW_148575/a91b622c83837aebecc09e6aa7a1f87c67b68bb8/
- Dr.Urban road-width explainer, useful as secondary quick reference:
  https://dr-urban.ru/standards/roads
