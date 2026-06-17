# Massing Decision Library

This is a compact repo version of the Obsidian research note:

```text
50 Research\Moscow Massing\Massing V2 Decision Library 2026.md
```

Use it before generating or revising early massing from TEP, plot, entries,
height constraints, references, or user feedback.

## Decision Order

```text
site_context
-> function_program
-> TEP pressure
-> access / entries / service
-> footprint type
-> public-space structure
-> massing family
-> form operators
-> facade / image language
-> approval, market, buildability, operation risks
-> CAD parameters
```

The important rule: facade language is late. Do not use facade or detail to
compensate for wrong zoning, movement, or volume hierarchy.

## Scenario Routing

| Subtype | Input state | Correct action |
| --- | --- | --- |
| `3A` fixed zoning | Footprints, entries, and zoning are already given | Treat footprints as source authority; work on heights, form, TEP, INSO, image |
| `3B` plot plus entries | Boundary and access are given, but no approved footprints | Propose zoning and tentative footprints first; do not jump into architecture |
| `3C` existing iteration | Current massing exists and needs improvement | Preserve approximate gabarit/TEP; revise form language and hierarchy |
| `3D` checklist review | Existing building/massing/proposal needs city/approval checklist review | Inspect Rhino evidence and score criteria before redesigning |

## Footprint Types

| Type | Use when | Risk |
| --- | --- | --- |
| Bar | Efficient office/residential plate along an edge or spine | Can block movement if placed across desire lines |
| L-shape | Need edge definition plus semi-open court | Corner can create dead pocket |
| U-shape / courtyard | Need protected open space | Courtyard can become narrow and dark |
| Compact plate | Need tower or dominant anchor | May be too isolated without podium/public logic |
| Perimeter block | Need urban edge and clear inside/outside | Can become a closed wall |
| Cluster | Need several buildings on large plot | Risks random scatter and leftover gaps |
| Podium footprint | Need public/commercial/base program | Risks swallowing landscape and routes |

## Massing Families

| Family | Works for | Watch |
| --- | --- | --- |
| Low-midrise contextual | Sensitive edges, calm office/campus blocks | Needs at least one deliberate operator |
| Office midrise generic | Regular BC plots and efficient plates | Must not become pure boxes |
| Podium + tower | TEP pressure, public base, clear hierarchy | Tower-podium relation must be explicit |
| Urban block + dominant | Large sites, city-facing corner, landmark need | Dominant must not kill public ground |
| Stepped / terraced | Height transition, INSO, roofscape | Preserve TEP and orient terraces logically |
| Slender tower / skyline | High visibility or tight footprint | Needs strong core/plate plausibility |
| Emotech/plastic landmark | Special sites needing image signal | High buildability and approval risk |

## Risk Checks

| Risk | Detection question |
| --- | --- |
| TEP failure | Does GFA/floor count remain close to target? |
| Boundary failure | Does any volume leave the absolute plot boundary? |
| INSO/height failure | Is every floor height below the allowed envelope? |
| Movement failure | Does a continuous public route remain legible and comfortable? |
| Gap failure | Are there narrow leftover slots between buildings? |
| Hierarchy failure | Can a viewer explain podium, tower, court, edge, and service logic? |
| Image failure | Does the scheme have one clear architectural move, not random styling? |
| Buildability failure | Could the geometry plausibly be built with normal office/residential logic? |
| Approval checklist failure | Does the proposal fail silhouette, unique volume, fifth facade, entry accents, frontage, permeability, or parking criteria? |

## Output Schema For Future Generators

Use this shape for AI/Rhino candidate descriptions:

```yaml
scenario_subtype:
site_context:
entries:
service_edge:
public_spine:
open_space_type:
footprint_type:
massing_family:
primary_operator:
secondary_operator:
floor_logic:
tep_strategy:
height_strategy:
movement_check:
approval_risks:
buildability_risks:
cad_parameters:
approval_checklist:
  object_type: visual | contextual | unknown
  criteria_status:
  missing_evidence:
```

## Hard Stop

If zoning, public route, service edge, buildable bands, and massing family are
not declared, do not generate Rhino geometry yet.

For `3D`, if Rhino evidence and checklist criteria are not collected, do not
claim compliance yet. Use:

```text
docs/scenarios/architecture-compliance-check.md
docs/libraries/moscow-architecture-approval-checklist.md
```
