# Moscow Architecture Approval Checklist

Compact repo version of the PDF checklist:

```text
C:\Users\dariy.n\Downloads\2026_06_13_ДГП_Чек_лист_оценки_архитектурного_объекта_2.pdf
```

Use this as a base review library for Scenario 3D:

```text
docs/scenarios/architecture-compliance-check.md
```

Rendered reference screenshots:

```text
archive/reference/dgp-architecture-checklist-2026-06-13/contact-sheet.png
archive/reference/dgp-architecture-checklist-2026-06-13/pages/
```

The checklist is a design/urban-quality review tool. It is not a full legal
code or TEP compliance engine by itself.

## Canonical Language Rule

Use stable English `criterion_id` values for automation, but keep the original
Russian `criterion_ru` as the canonical report label.

Reports must output criteria in Russian first. English notes are working
interpretations only.

```yaml
criterion_id: fifth_facade
criterion_ru: Наличие «пятого фасада»
status: partial
score: 0.5
evidence:
fix:
```

## Object Type

The checklist separates objects by visual role:

| Type | Typical condition |
| --- | --- |
| Visual / view object | Visible from major streets, intersections, MCD/MCC/rail lines, embankments, water objects, significant urban objects, main streets, or squares |
| Contextual / environmental object | Located inside quarters or behind the main street frontage |

If object type is unclear, mark it as `unknown` and evaluate criteria with
explicit evidence limits.

### Type-Sensitive Reading

Do not score every criterion with the same weight for every site.

For **Видовые объекты**, the presentation emphasizes visibility from major
streets, intersections, MCD/MCC/rail lines, embankments, water objects,
significant urban objects, main streets, and squares. The main evidence is:

- silhouette;
- uniqueness of volume;
- crown/parapet logic;
- fifth facade;
- all-side readability;
- entry and evening image where the public approaches the building.

For **Средовые объекты**, the presentation emphasizes objects located inside
quarters or behind the frontage of main streets. The main evidence is:

- fit into the surrounding fabric;
- active and continuous street frontage when relevant;
- ground-floor relationship;
- permeability;
- absence of surface parking;
- clear separation of public and private areas.

`Застройка формирует фронт улицы` is most direct for dense urban frontage along
main streets or squares. A free-standing visual object on a broad open site may
not form a continuous street wall by design; in that case, report the criterion
as secondary and explain whether a street frontage is actually expected by the
site condition.

## Architectural Image Criteria

| criterion_id | criterion_ru | What To Look For | Evidence |
| --- | --- | --- | --- |
| `two_or_more_options` | Представлено 2 и более варианта архитектурного решения | At least two variants of the architectural solution are presented | Variant layers, option files, screenshots, design package |
| `facade_color_material_diversity` | Разнообразие колористических решений и материалов фасадов | Variation in color, materials, facade elements, plasticity, relief, rhythm, texture, and facade accents | Facade views, material schedule, rendered views |
| `silhouette` | Силуэтность застройки | Dynamic city silhouette through different forms and heights of volumes/buildings | Distant views, skyline view, height diagram, massing sections |
| `unique_volume` | Уникальность объемного решения | Plastic massing differs from generic analogues and supports an artistic concept | 3D views, massing operators, concept statement |
| `cornice_horizon_highrise` | Карнизный горизонт (в высотных зданиях) | Human-scaled street frontage with upper-level setbacks or clear cornice/height datum | Street view, section, podium/tower relation |
| `entrance_group_accents` | Акценты на входных группах | Main entrances are visibly accented by facade treatment, decorative elements, color, or lighting | Ground-floor views, entry plan, night/render views |
| `crowns_parapets` | Наличие навершений и парапетов | Silhouette endings through sculptural tops, parapets, terraces, or crown volumes | Top floors, roofline, parapet/crown geometry |
| `fifth_facade` | Наличие «пятого фасада» | Roofs are designed as visible facades: graphic roof design, decorative structures, hidden/organized engineering | Roof/top view, roof equipment plan, aerial view |
| `architectural_lighting` | Архитектурная подсветка | Lighting emphasizes facade plasticity/rhythm, creates evening identity, and highlights entries/public zones | Lighting concept, night render, entry/public-zone views |

## Urban Planning Criteria

| criterion_id | criterion_ru | What To Look For | Evidence |
| --- | --- | --- | --- |
| `street_frontage` | Застройка формирует фронт улицы | Building forms a continuous and active street frontage with services/public functions where relevant | Site plan, ground-floor frontage, street views |
| `permeability` | Проницаемость застройки | Building layout supports insolation, natural ventilation, visual comfort, and separation of public/private spaces, often through tower/stylobate logic | Site plan, gaps/routes, courtyard/public-private diagram |
| `no_surface_parking` | Отсутствие плоскостных парковок | Permanent/temporary car storage is in underground or multi-level parking; short-term stops are within the street network | Parking plan, ground plan, traffic/drop-off diagram |

## Result Scale

Use statuses and numeric scores, but avoid artificial 0/50/100 scoring. A
visual criterion can be 62%, 67%, 82%, etc. when the evidence supports that
level.

| Status | Score | Meaning |
| --- | --- | --- |
| `yes` | 85-100% | Criterion is strongly supported by visible/measurable evidence |
| `mostly_yes` | 65-84% | Criterion is generally met, with specific missing proof or weak spots |
| `mixed` | 35-64% | Criterion is present but incomplete or uneven |
| `mostly_no` | 1-34% | Only weak traces of the criterion are visible |
| `no` | 0% | Criterion is not met or not presented |
| `not_enough_data` | `null` | Model/package lacks enough evidence to judge |
| `not_applicable` | `null` | Criterion does not apply to this object/type/stage |

Do not use a simple green check if the evidence is missing. Missing package
information is a review risk.

Use binary `yes/no` where ranking is not meaningful:

- `Представлено 2 и более варианта архитектурного решения`;
- `Архитектурная подсветка`, if no night image or lighting concept is present;
- `Отсутствие плоскостных парковок`, when surface parking is clearly visible.

Report:

```text
architectural_image_percent
urban_planning_percent
total_weighted_percent
evidence_coverage_percent
```

Default total weighting:

```text
architectural_image = 70%
urban_planning = 30%
```

Optional TEP/norm/legal checks are separate; they do not change the design
checklist percentage unless the user explicitly asks for a combined score.

## Common Approval Risks

| Risk | Typical Cause | Fix Direction |
| --- | --- | --- |
| Box-only image | No explicit massing operator or facade rhythm | Add site-reasoned operator, silhouette move, crown, setbacks, facade depth |
| Weak silhouette | All volumes have similar height/form | Create height hierarchy, upper setbacks, crown/top logic |
| No fifth facade | Roof equipment exposed or roof ignored | Organize equipment, add parapets/screens, design roof pattern |
| No entry hierarchy | Entrances disappear in facade | Add canopy/recess/light/color/volume accent |
| Flat street edge | Building does not form active frontage | Rework podium/ground floor and public edge |
| Poor permeability | Long bars or closed blocks cut movement/light | Open route, split mass, improve courtyard/stylobate logic |
| Surface parking visible | Ground plane used for storage parking | Move parking underground/multilevel; keep only short stops/drop-off |
| Facade/material unknown | Massing stage has no image package | Mark as missing data and request facade/material concept |
| Wrong object-type weighting | A visual/free-standing object is judged as dense street frontage, or a contextual object is judged only by skyline | Classify `Видовой / Средовой` first, then apply criteria by site condition |
| Vague fifth facade note | Report says "partly solved" without evidence | State what is visible on the roof and exactly what is missing: roof graphics, decorative structures, hidden engineering |

## Visual Example Signals From PDF

The PDF examples clarify how to read the criteria visually:

| Criterion | Positive signal in examples | Negative signal in examples |
| --- | --- | --- |
| Видовой / Средовой объект | Visual objects are seen from highways, intersections, rail/MCC/MCD, embankments, landmarks, main streets, and squares | Contextual objects sit deeper inside blocks and are judged more by environment fit |
| Представлено 2 и более варианта архитектурного решения | Multiple genuinely different facade/massing variants are shown | Only one solution or only cosmetic difference |
| Разнообразие колористических решений и материалов фасадов | Distinct but coordinated material zones, facade rhythm, texture, depth, and body-to-body variation | Large repeated monochrome or flat glazed/facade fields |
| Силуэтность застройки | Height hierarchy, stepped tops, varied tower forms, skyline rhythm | Equal-height slabs/towers, flat box skyline, repeated generic blocks |
| Уникальность объемного решения | Plastic massing, sculptural/recognizable form, non-standard volume logic | Generic rectangular tower or slab with no clear concept |
| Карнизный горизонт (в высотных зданиях) | Human-scaled street base plus upper setbacks/terracing in high-rise buildings | Tall volume rises straight from ground with weak street-scale datum |
| Акценты на входных группах | Entrance is legible through recess, canopy, portal, color/material shift, or lighting | Entrance disappears in a uniform facade |
| Наличие навершений и парапетов | Roofline has parapet, sculptural top, terraces, or intentional silhouette ending | Building stops with a flat technical top |
| Наличие «пятого фасада» | Roof is designed from above: pattern, screens, decorative structures, organized equipment | Exposed equipment, blank technical roof, unresolved flat surface |
| Архитектурная подсветка | Night image emphasizes facade rhythm, public zones, and entries | No lighting package or purely utilitarian glow |
| Застройка формирует фронт улицы | Continuous active edge with clear urban room and ground-floor relationship | Towers/blocks floating in leftover open space |
| Проницаемость застройки | Tower/stylobate or separated masses create light, airflow, views, and public/private hierarchy | Closed perimeter/slab blocks with poor gaps and weak visual comfort |
| Отсутствие плоскостных парковок | Parking is hidden underground/multilevel; short stops stay in street network | Large visible surface lots dominate ground plane |

For Scenario 3D, compare Rhino screenshots against these visual signals before
assigning `pass` or `fail`. If the model is massing-only and lacks facade,
lighting, roof, or parking information, use `not_enough_data` instead of
inventing compliance.

## Interpretation Conclusions From Presentation

The PDF is not only a checklist. It communicates the city's expected design
logic for contemporary projects.

Main conclusions:

1. **The city evaluates the whole urban image, not just the object.** A project
   is judged by skyline, street frontage, permeability, ground plane, roof,
   entrances, lighting, parking strategy, and view impact.
2. **Projects are split by visibility role.** View/visual objects need stronger
   silhouette, uniqueness, fifth facade, and recognizable image. Contextual
   objects can be calmer, but must fit the urban fabric and not degrade the
   ground level.
3. **The preferred project is not a flat box with a facade pattern.** Positive
   examples usually have massing hierarchy, differentiated volumes, material
   depth, active roof/crown logic, and a legible public base.
4. **Massing quality comes before facade decoration.** Facade color/material
   diversity helps only if the volume, silhouette, ground level, and urban
   relationship are already convincing.
5. **The roof is part of the submission image.** Low and mid-rise roofs,
   podium roofs, technical zones, and tower crowns are expected to be designed
   as visible surfaces.
6. **The ground plane is treated as architecture.** Surface parking, dead
   leftover space, weak entrances, and unclear pedestrian routes damage the
   project even when the building form is strong.
7. **Permeability is a city-quality criterion, not only a circulation issue.**
   The presentation values light, ventilation, visual comfort, public/private
   separation, and clear passage through or around the massing.
8. **A successful approval package must prove intent.** It should include
   variants, views, top/roof view, facade/material logic, entrance logic,
   evening lighting, and site/parking strategy. Missing drawings or views are
   not neutral; they lower evidence confidence.

For AI review, this means Scenario 3D should not ask only "does the object have
this feature?" It should ask:

```text
Does the project communicate a city-facing architectural idea,
and is that idea proven from all sides, from above, and at ground level?
```

## Session Lesson - Flow_Model_V2 2026-06-17

The review of `Flow_Model_V2.3dm` exposed three reporting mistakes to avoid:

1. Do not mechanically penalize a free-standing **Видовой** object for not
   forming a dense street frontage. In that case, `Застройка формирует фронт
   улицы` is secondary unless the site clearly requires a frontage.
2. Do not convert `pass/partial/fail` into round 100/50/0 values. Review the
   five views and assign a specific percentage from evidence.
3. Do not write vague phrases such as "пятый фасад решен частично". Say plainly:
   what roof elements are present, what engineering/graphic/decorative roof
   evidence is missing, and why the percentage is not higher.

## Review Template

```markdown
## Criterion

criterion_id:

criterion_ru:

Status:

Score:

Evidence:

Risk:

Recommended correction:

Needs user/source data:
```
