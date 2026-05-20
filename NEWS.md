# Новости

## 2026-05-20 — Сессия упрощения башни: v8–v20, рестарт на NURBS

### Что делали

12 итераций Python-скриптов для упрощения хайполи меша архитектурной башни (файл 22.3dm):
- v8: адаптивные радиальные секции — тело башни улучшилось, корона скручивалась
- v9: point envelope — диагностика кроны, слишком органично
- v10: split shaft/crown — закрытый меш, но слишком "органичный" (следует шуму фасадных рёбер)
- v11: prism blockout — прямые стены, но теряет архитектурную форму
- v12: concave parts — неправильно читает два основных объёма башни
- v13: two masses (main_body_red + rear_top_green) — корректная концепция, но реализация не точная
- v14/v15: parts mesh — выдумывает crown_slab_solid_01..03, которых нет
- v16: sloped halves — верное направление по слопу, но фальшивая пустота в плане
- v17: sloped halves filled — исправлена пустота, слишком абстрактно
- v18: NURBS/Brep restart — сплит футпринта на два объёма со слопом наверху
- v19: point cloud reconstruction (open3d) — исследование через Open3D decimation
- v20: direct decimation — прямая децимация меша

### Ключевые выводы

1. **Меш-примитивный подход провалился.** Point envelopes → органичность. Convex/concave hulls → теряется форма. Crown slabs → выдуманная геометрия.
2. **Проблема не в алгоритме hull — в отсутствии архитектурной корреспонденции.** Нельзя лофтировать меняющиеся контуры без stable corner mapping.
3. **Башня состоит из двух крупных перекрывающихся объёмов** (переднее тело + задний/верхний объём), не из вертикальной призмы с короной сверху.
4. **NURBS — следующий правильный путь**, но не как raw loft по сечениям, а через именованные архитектурные рейлы:
   - `front_left_edge`, `front_right_edge`, `rear_left_edge`, `rear_right_edge`
   - `central_valley_or_seam`, `left_top_cut`, `right_top_cut`, `rounded_side_rail`
   - Сначала диагностические кривые → потом поверхности.

### Следующий шаг

Создать NURBS diagnostic script:
1. Читает текущий source OBJ
2. Находит и подгоняет 8 именованных рейлов из feature lines/long edges
3. Импортирует кривые в Rhino
4. Захватывает front/top/side виды для проверки
5. Только после проверки — строить Brep поверхности

### Артефакты

- Скрипты v8–v20: `C:\VS Code\tools\cad-mesh-tools\`
- Решение о рестарте: `decisions/2026-05-20-nurbs-restart-from-named-rails.md`

---

## 2026-05-19 (Scenario 2 — feature-preserving mesh reconstruction decision)

### Решение

- Для сценария high-poly fragmented Rhino model -> simplified solid model выбран следующий тестовый подход: plane/primitive-based polygonal surface reconstruction from mesh-derived point clouds.
- Основной стек для проверки: CGAL Shape Detection / Efficient RANSAC + CGAL Polygonal Surface Reconstruction.
- CGAL 3D Alpha Wrapping используется как baseline против Rhino ShrinkWrap.
- Rhino QuadRemesh / Instant Meshes / QuadriFlow остаются secondary post-process после того, как закрытая форма и архитектурная fidelity уже доказаны.

### Почему

- ShrinkWrap закрывает модель, но сглаживает/портит sharp architectural corners.
- VSA дает plane clusters и feature edges, но не делает watertight solid.
- Pure quad remeshing не восстанавливает архитектурную топологию из дробной модели.

### Артефакт

- `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md`

## 2026-05-18 (сессия 3 — Clear Model 4 postmortem)

### Результат

- Проведены 3 итерации реконструкции башни (`Clear Model 2/3/4`).
- `Clear Model 4`: `isSolid=True`, `Manifold=True`, 6011 граней, bbox подтверждён.
- Низ/подиум стал значительно лучше — использовались source sections и direct Brep conversion.
- Башня деформирована: raw section lofting без seam alignment даёт "плавленый" результат.

### Главный урок

**Section extraction ≠ section correspondence.**
Каждая Z-секция не должна выбирать свой шов и порядок вершин независимо.
Нужен шаг `fit_architectural_sections` перед любым лофтингом башни.

### Зафиксированные правила

- Boolean union запрещён — молча удаляет массы; использовать appended Brep.
- `isSolid=True` недостаточен как критерий качества.
- Перед лофтингом: classify sides → assign anchors → resample → zone split → validate.

### Обновлённый алгоритм (8 шагов)

`scan_scene` → `classify_source_groups` → `extract_raw_sections` → `fit_architectural_sections` → `validate_section_correspondence` → `build_zone_lofts` → `append_or_export` → `review_capture_set`

### Следующий шаг

Реализовать `fit_architectural_sections` — это ключевой недостающий шаг перед Milestone 2.

## 2026-05-18 (сессия 2)

### Сделано

- Создан `rhino_workflow_kit` в `C:\VS Code\workfiles\rhino_workflow_kit`.
- Три intake-шаблона: `reference_model_intake.md`, `cleanup_model_intake.md`, `massing_intake.md`.
- Три JSON-схемы: `reference_model_params`, `cleanup_model_params`, `massing_params`.
- Скрипт `scan_scene.py` — читает сцену включая hidden/locked объекты, сохраняет `scene_scan.json`.
- Скрипт `extract_sections.py` — извлекает горизонтальные сечения по N Z-уровням, сохраняет `sections.csv` + `sections.json`.
- Скрипт `rhino_runner.py` — общий runner с проверкой соединения, capture и run_id.

### Следующий шаг (Milestone 1 — Reliable Readback)

1. Открыть целевую сложную Rhino-модель.
2. Запустить `scan_scene.py` → получить `scene_scan.json`.
3. Запустить `extract_sections.py --layer SOURCE_LAYER --levels 20` → получить `sections.csv`.
4. Проверить данные: width/depth/center evolution по Z.
5. Если данные корректны — переходить к Milestone 2 (blockout builders + validation gates).

### Открытые решения

1. Script toolkit first или сразу custom Rhino MCP connector?
2. Финальный output: mesh допустим или только Brep/solid?
3. Какой кейс берем для Scenario 1?
4. Где долгосрочно хранить шаблоны и бенчмарки?
5. Кто утверждает переход из R&D в поддерживаемый инструмент?

## 2026-05-18 (сессия 1)

- Создан репозиторий проекта и загружены первые материалы: отчет, рабочий план и стартовая страница.
- Текущий статус: R&D / пилот по трем сценариям AI-построения геометрии.
- Активный фокус: собрать `rhino_workflow_kit` и протестировать сценарий 2 на текущей сложной Rhino-модели.
- Ближайший checkpoint: согласовать формат MVP, тип финальной геометрии и первый benchmark-кейс.
