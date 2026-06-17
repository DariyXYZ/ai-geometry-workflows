# Architecture Compliance Check

Scenario 3D is a review workflow for checking an existing building or massing
proposal against an architectural approval checklist.

It is a subscenario of Scenario 3 because it works with massing, TEP context,
urban position, visual image, and Rhino scene evidence. It does not generate a
new building first. It reviews what exists.

Primary source:

```text
C:\Users\dariy.n\Downloads\2026_06_13_ДГП_Чек_лист_оценки_архитектурного_объекта_2.pdf
```

Checklist library:

```text
docs/libraries/moscow-architecture-approval-checklist.md
```

## Use When

Use this scenario when the user asks to:

- check whether a building matches city/approval criteria;
- review a massing or architectural proposal before submission;
- compare one or more options against a checklist;
- identify weak points in silhouette, fifth facade, entries, street frontage,
  permeability, parking strategy, material/color diversity, or evening image;
- make an approval-risk report from a Rhino scene.

Optional add-ons:

- norms/code compliance, only if the user asks and gives enough source data;
- TEP/GFA/FAR compliance, only if TEP targets or source TEPs are available;
- INSO/height/boundary checks, when the scene contains those constraints.

## Required Inputs

Minimum:

- Rhino scene or model through MCP/Aurox/RhinoCommon;
- building geometry or massing;
- context geometry or at least site/street orientation;
- object type: visual/landmark-like or contextual/environmental if known.

Recommended:

- plot boundary;
- entries and public approach directions;
- roof/engineering elements;
- facade/material/color concept or visual references;
- night lighting concept;
- parking/drop-off/service data;
- TEP targets if TEP compliance is requested.

## Workflow

```text
connect Rhino MCP
-> inspect layers, units, object types, and context
-> collect building bbox, heights, footprint, roof state, entries, public edges
-> capture/review evidence views: north, south, east, west, orthogonal top plan
-> classify object as visual / contextual / unknown
-> score each checklist criterion: 0 / 0.5 / 1 plus status
-> separate visual-architectural, urban-planning, TEP/normative issues
-> calculate group and total compliance percentage
-> write approval-risk report with evidence and recommended fixes
```

Do not invent missing evidence. Mark it as `not_enough_data`.

Reports must output checklist criteria using the original Russian
`criterion_ru` from `docs/libraries/moscow-architecture-approval-checklist.md`.
English criterion names are only stable machine IDs and working notes.

## Rhino Evidence To Collect

| Evidence | Why |
| --- | --- |
| Scene units and scale | Avoid false height/TEP judgments |
| Plot boundary and setbacks | Understand legal/geometric limits |
| Building footprint and bbox | Determine height, massing family, urban edge |
| Main street/corner/context views | Judge silhouette, frontage, visibility |
| Entry locations | Judge entrance accents and approach logic |
| Roof/top view | Judge fifth facade, parapets, roof equipment |
| Ground plane and parking areas | Judge surface parking and public realm |
| Variant layers | Check whether 2+ options are presented |
| Existing constraints/TEP layers | Optional TEP/height/norm checks |

Minimum visual evidence set before a confident score:

```text
north facade
south facade
east facade
west facade
orthogonal top plan
```

If any of these views are missing, mark the percentage as `preliminary`.

## Review Categories

Use the checklist library as the base criteria. Group findings into:

1. **Architectural image** - variants, facade/material diversity, silhouette,
   unique massing, cornice horizon, entrance accents, parapets/crowns, fifth
   facade, architectural lighting.
2. **Urban planning** - street frontage, permeability, absence of surface
   parking.
3. **Optional compliance** - TEP, height, INSO, code/normative checks when
   requested and sufficiently sourced.

## Percentage Scoring

Use percentages in addition to `pass/fail` so variants can be compared quickly.

Score each applicable criterion:

| Status | Score |
| --- | --- |
| `pass` | `1.0` |
| `partial` | `0.5` |
| `fail` | `0.0` |
| `not_enough_data` | excluded from compliance percent, but counted as evidence risk |
| `not_applicable` | excluded |

Formula:

```text
compliance_percent = scored_points / applicable_scored_criteria * 100
evidence_coverage_percent = criteria_with_enough_data / applicable_criteria * 100
```

Always report both numbers. A project can score well only on known criteria but
still have weak evidence coverage.

Recommended group weights for the total checklist score:

| Group | Weight |
| --- | --- |
| Architectural image | 70% |
| Urban planning | 30% |

Use equal weights inside each group unless the user asks for custom weighting.
Optional TEP/norm checks are reported separately and must not silently change
the design-checklist percentage.

## Output Format

```yaml
scenario_subtype: 3D
source_authority:
  rhino_scene:
  checklist:
  object_type: visual | contextual | unknown
evidence:
  units:
  building_bbox:
  height:
  footprint_area:
  floors_if_known:
  view_set:
  variant_layers:
checklist_results:
  architectural_image:
    criterion_id:
      criterion_ru:
      status: pass | fail | not_enough_data | not_applicable
      score: 1.0 | 0.5 | 0.0 | null
      evidence:
      risk:
      fix:
  urban_planning:
    criterion_id:
      criterion_ru:
      status:
      score:
      evidence:
      risk:
      fix:
scoring:
  architectural_image_percent:
  urban_planning_percent:
  total_weighted_percent:
  evidence_coverage_percent:
  confidence: high | medium | low | preliminary
optional_checks:
  tep:
  norms:
  height_inso_boundary:
summary:
  likely_approval_risk: low | medium | high
  strongest_points:
  weakest_points:
  recommended_next_actions:
```

## Hard Rules

- Do not claim compliance without visible or measurable evidence.
- Do not mix design-quality checklist review with legal code compliance unless
  requested.
- Do not judge TEP compliance without TEP targets or source TEPs.
- Do not treat a massing-only model as if facade materials, colors, or lighting
  were already proven.
- If the model lacks roof detail, mark fifth facade as `not_enough_data` or
  `fail`, depending on the review intent.
- If only one option exists, mark the "2+ architectural options" criterion as
  `fail` unless the user says variants exist elsewhere.

## Relationship To Other Scenario 3 Subtypes

- After `3A`, use 3D to review fixed-footprint massing/form before submission.
- After `3B`, use 3D only after zoning/footprints are approved enough to judge.
- After `3C`, use 3D to compare whether the revised image solves checklist
  risks.

If the 3D review reveals major planning failure, return to 3B or 3C instead of
trying to fix everything with facade treatment.
