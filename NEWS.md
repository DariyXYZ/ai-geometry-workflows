# Новости

## 2026-05-19 (сессия 4 — v5/v6 postmortem + VSA + form reading research)

### Результат

- v5 (true sections + RDP): лучше bbox-версий, но форма скручена — per-section RDP ломает correspondence.
- v6 (template contour): высота исправлена, bbox верный, twist частично уменьшен. Известное ограничение: корона — placeholder.
- Параллельно: реализован VSA-скрипт (`vsa_simplify.py`) для сегментации меша на плоские патчи.
- Проведён ресёрч стратегий чтения формы: адаптивные секции, feature lines, RANSAC, alpha shape.

### Корневой диагноз v5→v6 failure

RDP-упрощение каждой секции независимо сохраняет разные локальные детали на разных уровнях → loft соединяет несовпадающие точки → twist. Решение: outer envelope (alpha shape) + corner label matching.

### v7 направление

1. Alpha shape (outer envelope) вместо RDP — убирает шум рёбер фасада
2. Corner labels через nearest-neighbour к углам reference секции — гарантирует correspondence
3. Zone split по area change > 15% — лофт в пределах зоны, корона отдельно

### Form reading research

- Корневая причина искажений: равномерные секции → пропускают зоны изменения формы
- Стратегия 1: адаптивные секции по пикам Mean Curvature (GH Mesh Curvature component)
- Стратегия 2: feature lines (ridge/valley) — правильный примитив для ребристого фасада (MeshLab / libigl)
- Стратегия 3: RANSAC plane segmentation (Open3D) для плоских частей

### Новая ветка

`scenario-2/mesh-simplification-research` — полный лог итераций, решений и инструментов.

---

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
