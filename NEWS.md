# Новости

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
