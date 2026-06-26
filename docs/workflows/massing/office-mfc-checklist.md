# Office / MFC Concept Checklist

IND internal checklist for office and mixed-function complex (МФК) concept review.
Applies together with the general concept checklist.

Primary source:

```text
C:\Users\dariy.n\Downloads\Чеклист_концепции_IND_офисы_мобильный.pdf
```

Secondary source (same content, flat list format):

```text
C:\Users\dariy.n\Downloads\Чек-лист по офисам.docx
```

## Use When

Use this checklist when reviewing or generating an office or МФК concept to
verify that all IND-standard requirements are addressed. Apply it at massing
and concept stage, not only at DD.

Trigger conditions:

- user is reviewing or developing an office building, business center, or МФК;
- project height is stated or implied (≤50 m, 50–100 m, 100–150 m, 150–200 m,
  or above 200 m);
- user asks to check functional program, core, facade, or efficiency ratios.

> Any massing change requires insolation recheck. Flag this automatically.

## Checklist

### 01 — Lobby and Ground Floors

- [ ] Double-height lobby (двухсветный вестибюль)
- [ ] Dry-feet principle (крытый подход, навес или аркада)
- [ ] Ground-floor retail with street-independent access
- [ ] Building management (УК) offices on floor 1 or 2

### 02 — Core and Engineering

- [ ] All technical and auxiliary rooms located in the core
- [ ] Engineering shaft ratio to GFA (excluding lifts):
  - up to 50 m → 2–2.5%
  - 100 m → 4.5–5%
  - above 100 m → intermediate technical floor preferred + 5% for shafts
- [ ] Transfer and service lifts included where feasible

### 03 — Lifts

- [ ] Lift zones split into groups to minimise total lift count
- [ ] Overruns and machine rooms accounted for (speed-dependent)
- [ ] Approx. calculation: 200–250 persons per lift
- [ ] For buildings above 100 m: intermediate technical floors and outrigger floors
  included

Building section diagram (reference):

```text
  [Machine room   3 m above top served floor]
  [Overrun        5–8 m, speed-dependent    ]
  [Top served floor                         ]
```

### 04 — Office Floor Plate and Subdivision

- [ ] Office depth 8–12 m; end bays may be deeper if WCs are provided
- [ ] Lot subdivision follows structural grid axes (for combinatorics)
- [ ] Structural columns either flush with facade or set back 1.5–3 m
- [ ] Partitions align to mullions at lot boundaries
- [ ] Corridor width ≥1.8 m clear (or 1.5 m with accessibility alcoves)
- [ ] Raised floor 150 mm
- [ ] Typical office floor-to-floor height 3.9 m

### 05 — Loading and Technical Zones

- [ ] Loading bay, transformer rooms, and waste chambers preferably at basement level

### 06 — Facade

- [ ] Jumbo glass module respected (3 × 6 m)
- [ ] Fire spandrels between floors: 1200 mm standard, 600 mm minimum per STO

### 07 — Roof and Terraces

- [ ] Roof build-up (excluding slab) approx. 500 mm
- [ ] Podium roof build-up 1.0–1.5 m depending on landscaping
- [ ] Client informed: terraces reduce rentable area on the floor below

### 08 — Efficiency Ratios (Rentable / GFA)

Depends on building height, facade complexity, and office layout:

| Height band | Rentable / GFA |
| --- | --- |
| Up to 50 m | 0.75–0.80 |
| Up to 100 m | 0.69–0.73 |
| Above 100 m | individual (0.60–0.65) |

### 09 — Site and Insolation

- [ ] Building placed with utility routes and fire access lanes in mind
- [ ] **Any massing change = mandatory insolation recheck**

### 10 — End-of-Trip / Active Mobility

- [ ] Covered, secured bicycle parking; number of spaces matches building class
- [ ] Showers, changing rooms, and drying rooms adjacent to bike parking
- [ ] Bike repair station or spare-parts vending
- [ ] E-scooter and personal mobility device charging

### 11 — Lobby as Public Space

- [ ] Lobby is not a transit corridor — it is a lounge, coworking, or café space
- [ ] Lobby creates the first impression for tenants and their employees

### 12 — Roof as Event Asset

- [ ] Scenes designed for different formats and weather:
  outdoor cocktail → covered fallback without losing the event
- [ ] Roof can generate revenue beyond the tenant base
- [ ] Decided at concept stage: passive small-group rest OR large-event venue
  (determines structural reinforcement scope)
- [ ] Technical requirements:
  - lift access + minimum two egress stairs
  - interior–terrace level connection (flush floor)
  - vestibules control stack effect

### 13 — EV Infrastructure

- [ ] EV charging stations in parking
- [ ] Cable routes for EV charging pre-installed at design stage,
  even if stations are fitted later

### 14 — Wellness and Ambient Quality

- [ ] Air-quality monitoring infrastructure (CO₂ sensors, humidity)
- [ ] Acoustic comfort in open-plan and shared zones
- [ ] Interior and public-space planting

### 15 — Flexible Amenities

- [ ] Meeting rooms, fitness, food hall — amenity mix drives rental rate
- [ ] Sharing amenities between tenants or adjacent buildings is possible

## Output Format

When performing a checklist review, report in Russian. Use this structure:

```text
Объект: [name / address]
Высота: [height band]
Стадия: концепция / ЭП / П / другое

[Section name]
  ✓ / ✗ / ? [item]
  ...

Итого: X из Y пунктов выполнено
Критические нарушения: ...
Требует уточнения: ...
Обязательно: пересчитать инсоляцию если менялся массинг
```

Mark items:
- `✓` confirmed from model or documentation
- `✗` not met
- `?` not enough data

## Hard Rules

- Any massing change requires insolation recheck — flag this even if not asked.
- Do not assume efficiency ratios without knowing height band and facade complexity.
- Do not skip sections 10–15 for Class A / premium office projects.
- Sections 10–15 are not optional for Class A — they drive rental rate and
  tenant attraction.
