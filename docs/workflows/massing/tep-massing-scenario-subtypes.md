# TEP Massing Scenario Subtypes

Scenario 3 is not one workflow. It splits into subscenarios depending on how
much site/planning information already exists and whether the user wants
generation or review.

Before generating geometry, classify the task as one of these:

```text
3A - given zoning and footprints
3B - given plot and entries only
3C - given plot plus existing massing iteration
3D - existing building/massing compliance checklist review
```

Do not mix the workflows. Most bad results come from treating 3B as if it were
3A, treating 3C as if the task were only a zoning problem, or treating 3D as if
it were legal/code compliance without enough source data.

## 3A - Given Zoning, Footprints, And Entries

Use when the input already contains:

- building footprints;
- entries or lobby positions;
- open spaces / routes / zoning diagram;
- plot boundary and constraints;
- TEP targets.

Main task:

Create or revise the building form from the given planning structure. Do not
move footprints unless the user asks.

Workflow:

```text
read given zoning
-> lock footprints / entries / routes as source authority
-> compute TEP gap
-> choose height distribution
-> apply architectural operators to building form
-> validate TEP, height envelope, floor modules
-> hide construction/helper layers and leave final review layers visible
-> output clean massing
```

Allowed moves:

- height changes;
- setbacks;
- taper or upper-form change;
- chamfers / rounded corners;
- roof or crown massing;
- voids/cut-outs that do not break the approved zoning;
- podium/tower shaping if the footprint relationship is already defined.

Forbidden moves:

- invent a new public route;
- cut across the approved spine;
- move entrances casually;
- replace footprints with a different site plan;
- create new blocks that invalidate the given zoning.

Acceptance:

- footprints stay aligned with the given plan;
- entries remain connected and legible;
- GFA/FAR/height are close to target;
- architectural form is richer than boxes;
- no new movement conflict is introduced;
- tower-on-stylobate variants have a readable transition zone, not an
  unsupported upper volume hanging off the base;
- final viewport shows the massing result, not source copies, datums, core
  helpers, guide rays, metric boards, debug objects, or old variants.

## 3B - Given Plot Boundary And Site Entries Only

Use when the input contains:

- plot/buildable boundary;
- site entry points or likely access edges;
- hard constraints such as red lines, INSO, setbacks, context;
- TEP target or rough density;
- no approved footprints.

Main task:

Create a preliminary zoning proposal first. The output of this stage is not
final architecture; it is a planning skeleton for agreement.

Workflow:

```text
connect RhinoMCP and run capability scan
-> read plot/context/entries
-> classify site shape and edges
-> reserve public spine and service/fire edge
-> choose open-space type
-> create buildable bands
-> place tentative footprints for 1+ buildings
-> check movement, gaps, daylight, service, TEP capacity
-> ask for zoning approval
-> only after approval start architectural massing
```

Allowed moves:

- propose one or several footprint layouts;
- place 1+ buildings depending on site size and shape;
- define public spine, courtyard/plaza, service edge;
- test tower anchors;
- estimate height bands to prove TEP feasibility.

Forbidden moves:

- jump directly to expressive building form;
- fill the site with bars before reserving movement;
- treat residual gaps as planned public space;
- use towers only to recover area;
- over-detail architecture before zoning is approved.

Acceptance:

- public route is continuous and clear;
- service/fire access is not an afterthought;
- all gaps have roles;
- footprint depths are plausible for the program;
- TEP capacity is roughly plausible;
- user can approve or edit the zoning before form work begins.

## 3C - Given Plot Plus Existing Massing Iteration

Use when the input contains:

- plot/buildable boundary;
- constraints such as INSO;
- one or more existing massing iterations;
- target to make a new form in roughly the same scale/gabarit;
- design feedback about image, silhouette, or architectural expression.

Main task:

Use the existing massing as the TEP/gabarit anchor and generate a better
architectural image. This is more about form, hierarchy, silhouette, and
composition than discovering the entire site plan from scratch.

Workflow:

```text
read existing massing
-> compute its TEP, footprint, height bands, and envelope
-> diagnose what must be preserved vs changed
-> preserve approximate gabarit / density / anchors
-> improve form language and site relationships
-> apply explicit architectural operators
-> validate against existing TEP scale and constraints
-> output alternatives with clear deltas from source
```

Allowed moves:

- reshape a volume while keeping its approximate footprint zone;
- consolidate or split mass if it improves image and movement;
- add setbacks, chamfers, rotations, rounded corners, voids, terraces;
- strengthen skyline and roofscape;
- improve tower/base relationship;
- refine public-space edges without inventing a totally unrelated plan.

Forbidden moves:

- ignore the existing iteration's TEP scale;
- produce a completely new zoning unless requested;
- start from a generic tower because the envelope allows it;
- keep box-only volumes when the task is image/form improvement;
- create accidental intersections or narrow residual slots.

Acceptance:

- GFA and height remain roughly comparable to the source iteration;
- massing reads as a clear evolution, not an unrelated restart;
- movement and open-space logic improve or at least do not degrade;
- architectural operator is visible and justified;
- all changes can be explained as deltas from the existing massing.

## 3D - Architecture Compliance Checklist Review

Use when the input contains:

- an existing building, massing, or architectural proposal in Rhino;
- city/approval checklist review intent;
- need to inspect views, dimensions, roof, entries, street edge, permeability,
  parking, silhouette, and architectural image;
- optional TEP/norm/height checks only if the user asks and provides enough
  source data.

Main task:

Review the building against the architectural approval checklist. Do not start
by generating a new form. Collect evidence from the model and views first.

Workflow:

```text
connect Rhino MCP
-> inspect scene/layers/units/context
-> collect bbox, height, footprint, roof, entries, street edge, parking/public realm
-> capture or review main viewpoints and top/roof view
-> classify object as visual / contextual / unknown
-> score checklist criteria as pass / fail / not_enough_data / not_applicable
-> separate design checklist risks from optional TEP/norm risks
-> recommend targeted fixes or return to 3A/3B/3C if redesign is needed
```

Allowed moves:

- judge architectural image and urban-planning criteria;
- compare two or more variants if present;
- report missing evidence as a submission risk;
- recommend corrections such as silhouette hierarchy, fifth facade, entry
  accent, crown/parapet, frontage, permeability, or parking strategy;
- run optional TEP/norm checks only on request.

Forbidden moves:

- claim compliance without visual or measurable evidence;
- treat a massing-only file as proof of facade materials, color, or lighting;
- judge TEP compliance without TEP targets;
- judge legal/norm compliance unless the user explicitly requested it and
  enough source data is available;
- redesign the building before completing the checklist review.

Acceptance:

- every checklist item has status, evidence, risk, and fix direction;
- missing evidence is clearly marked;
- review distinguishes `design/approval checklist`, `TEP`, and `norm/code`;
- output identifies likely approval risk and the fastest fixes.

## Subscenario Classifier

Use this decision table before acting:

| Input condition | Subscenario | First output |
| --- | --- | --- |
| Footprints and entries are already given | `3A` | Form/height options on fixed zoning |
| Only plot, entries, context, and TEP are given | `3B` | Zoning and tentative footprint proposal |
| Existing massing exists and needs a better version | `3C` | Image/form revision with source TEP comparison |
| Existing building/massing needs checklist review | `3D` | Compliance/approval-risk report with evidence |

If multiple inputs exist, prioritize source authority:

```text
approved zoning/footprints override new zoning ideas
existing massing overrides generic typology
checklist review intent overrides generation
plot boundary and hard constraints override everything
```

## Required Metadata Per Variant

Every Scenario 3 variant should report:

```yaml
scenario_subtype: 3A | 3B | 3C | 3D
rhino_mcp_capability_scan:
  slot: string
  rhino_version: string
  units: string
  command_families_checked: [Box, Layer, Boolean, Loft, Extrude, View, Python]
  third_party_backend: none | name
  rhino_common_route_required: true_if_third_party_backend
source_authority:
  plot_boundary: required
  zoning: given | proposed | inferred_from_existing
  footprints: given | proposed | revised_from_existing
  entries: given | proposed | inferred
intent:
  planning_goal: string
  form_goal: string
  architectural_operator: string
checks:
  boundary: pass/fail
  height_envelope: pass/fail
  gfa_ratio_to_target_or_source: number
  public_spine: pass/fail/not_applicable
  gap_classification: pass/fail
  source_massing_delta: for 3C only
  checklist_results: for 3D only
```
