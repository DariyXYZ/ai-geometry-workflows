# AI Geometry Construction Workflows

Рабочий пакет к публичному отчету `ai_geometry_research.html`.

## Контекст

Направление оформляется по операционной модели отдела вычислительного проектирования:

- тип задачи: R&D / пилот;
- владелец: Дарий на этапе исследования и прототипирования;
- review: Петр по приоритетам и развилкам, Лена по архитектуре инструмента;
- статус: Clarification -> In Progress после согласования первого benchmark;
- судьба результата: шаблон, библиотечный модуль или инструмент по итогам пилота.

## Цель

Проверить и систематизировать сценарии построения CAD-геометрии с помощью AI, где:

- AI интерпретирует входные данные и формирует параметры;
- Rhino / Grasshopper / RhinoCommon строят геометрию;
- валидатор проверяет результат до принятия;
- успешные сценарии переводятся в повторяемые шаблоны и инструменты.

## Сценарии

### 1. Модель по изображениям, планам, фасадам и описанию

Статус: R&D / шаблон.

Первый результат:

- `reference_model_intake.md`;
- `reference_model_params.schema.json`;
- `reference_model_build.py`;
- `reference_model_validation.md`.

Критерий успеха:

- перед построением есть parameter table;
- top/front/side пропорции проходят validation;
- детализация не добавляется до прохождения blockout gate.

### 2. Упрощенная модель из сложной

Статус: R&D -> кандидат в инструмент.

Первый результат:

- `scan_scene`;
- `classify_building_meshes`;
- `extract_sections`;
- `validate_candidate`;
- fixed capture set.

Критерий успеха:

- источник считывается вместе с hidden/locked объектами;
- крупная форма и кривизна сохраняются;
- watertight/solid статус подтвержден вместе с section/bbox delta report.

### 3. Массинг по описанию, ТЭПам и правкам

Статус: шаблон -> кандидат в инструмент.

Первый результат:

- `massing_intake.md`;
- `massing_params.schema.json`;
- `variant_generator.py`;
- `variant_metrics.csv`;
- `revision_log.md`.

Критерий успеха:

- 5-10 вариантов строятся одним запуском;
- метрики считаются автоматически;
- пользовательские правки переводятся в изменения параметров.

## Shared Pipeline

`intake -> extract -> plan -> build -> validate -> handoff`

Обязательные артефакты:

- intake card;
- parameter table;
- build script;
- validation report;
- review captures;
- handoff note.

## Первый practical milestone

Создать `C:\VS Code\workfiles\rhino_workflow_kit`.

Минимальный состав:

- `templates/reference_model_intake.md`;
- `templates/cleanup_model_intake.md`;
- `templates/massing_intake.md`;
- `schemas/reference_model_params.schema.json`;
- `schemas/cleanup_model_params.schema.json`;
- `schemas/massing_params.schema.json`;
- `scripts/rhino_runner.py`;
- `scripts/scan_scene.py`;
- `scripts/extract_sections.py`;
- `reports/`.

## План на 4 недели

### Week 1

- согласовать task card;
- выбрать benchmark cases;
- создать workflow kit;
- подготовить intake templates и schemas.

### Week 2

- реализовать `scan_scene`;
- реализовать `extract_sections`;
- прогнать на текущей сложной Rhino-модели;
- получить `scene_scan.json`, `sections.csv`, review captures.

### Week 3

- собрать candidate blockout для Scenario 2;
- собрать простой variant generator для Scenario 3;
- добавить validation report.

### Week 4

- подготовить demo/review;
- принять решение по судьбе сценариев:
  - hold;
  - заготовка;
  - шаблон;
  - библиотечный модуль;
  - инструмент.

## Lessons From Clear Model 4 (2026-05-18)

Проведены 3 итерации реконструкции башни. Результат — частичный прогресс.

### Что стало лучше

- Низ/подиум реконструируется лучше, если использовать секции из источника, а не bbox.
- Закрытые source meshes конвертируются в Brep напрямую — лучше сохраняют кривизну.
- Boolean union надо избегать — он молча удаляет большие массы; вместо этого используем appended Brep.

### Что всё ещё не работает

- Башня деформируется при лофтинге: каждая секция выбирает шов и порядок вершин независимо.
- Итог: диагональные cross-connections, "плавленый/скрученный" вид башни.
- `isSolid=True` недостаточно — нужна архитектурная корреспонденция сторон.

### Новый обязательный шаг: Section Correspondence

`extract_sections` → **`fit_architectural_sections`** → `build_zone_lofts`

`fit_architectural_sections` должен:

1. определить длинные стороны фасада, закруглённые/скошенные углы;
2. назначить stable corner/side anchors на каждом Z-уровне;
3. пересемплировать секции с одного anchor, одним направлением;
4. разделить стек на зоны: lower_shaft / mid_shaft / upper_shaft / crown_shoulder / roof_cap;
5. отклонить билд, если correspodence не доказана.

### Обновлённый алгоритм для Scenario 2

1. `scan_scene` — все объекты включая hidden/locked
2. `classify_source_groups` — tower / podium / ovals / base / supports / trash
3. `extract_raw_sections` — несколько Z-срезов на группу
4. `fit_architectural_sections` — упростить контуры, выровнять швы, убрать facade noise
5. `validate_section_correspondence` — сравнить anchors и длины сторон между уровнями
6. `build_zone_lofts` — lower/mid/upper/crown зоны отдельно
7. `append_or_export` — appended Brep или watertight mesh (не boolean union)
8. `review_capture_set` — top/front/back/perspective + section delta table

## Decisions Needed

### Accepted 2026-05-19 - Feature-Preserving Mesh Reconstruction

For Scenario 2, the next primary test path is plane/primitive-based polygonal surface reconstruction from mesh-derived point clouds.

Primary stack:

- CGAL Shape Detection / Efficient RANSAC for plane and primitive extraction;
- CGAL Polygonal Surface Reconstruction for compact watertight polygonal output;
- CGAL 3D Alpha Wrapping as a ShrinkWrap-style baseline;
- quad remeshing only after solid/fidelity validation passes.

See `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`.

1. Script toolkit first или сразу custom Rhino MCP connector?
2. Финальный output для анализа: multiple closed Brep shells допустимы или нужен один watertight mesh?
3. Какой кейс берем для Scenario 1?
4. Где долгосрочно хранить шаблоны и бенчмарки?
5. Кто утверждает переход из R&D в поддерживаемый инструмент?
