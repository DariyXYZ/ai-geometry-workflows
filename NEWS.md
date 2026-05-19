# Новости

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
