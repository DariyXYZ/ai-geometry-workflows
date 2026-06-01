# AI Geometry Workflows

Рабочий репозиторий для AI-assisted CAD, Rhino, Grasshopper и
architecture-to-CAD workflows.

Проект переводит разрозненные эксперименты "Codex сделал модель в Rhino" в
повторяемый validation-first toolchain для реальных задач моделирования.

## Текущее направление

AI используется для:

- интерпретации входных данных;
- извлечения параметров;
- разложения модели на части;
- генерации CAD/Rhino/build123d scripts;
- routing и iteration control.

Геометрию создают deterministic tools: Rhino, Aurox, build123d, CadQuery,
OpenCascade и проверяемые Python/Rhino scripts.

Ни один результат не считается принятым без source-derived validation.

Базовый pipeline:

```text
intake -> extract -> plan -> build -> validate -> handoff
```

## Четыре рабочих слоя

1. **Rhino/Aurox readback layer**
   Скан сцены, source overlays, классификация объектов, sections, fixed review captures.

2. **Semantic sketch layer**
   Новое исследовательское направление: Spellshape / Live OBJ как источник идеи
   `semantic OBJ`. Цель - хранить rough mesh preview вместе с `#@` metadata:
   parts, bbox, anchors, params, controls, locks, constraints.

3. **CAD-as-code backend layer**
   `text-to-cad` / build123d как STEP-first backend для чистых parametric CAD
   candidates.

4. **Case orchestration layer**
   `ai_geometry_toolkit` создает case folders, manifests, routes, reports,
   backend links и validation stubs.

## Три продуктовых сценария

### 1. Reference to model

Построение модели из изображений, планов, фасадов/elevations, чертежей,
описаний и известных размеров.

Это долгосрочное направление для будущей интеграции в AI-платформу. Сначала
строим надежный локальный движок через Rhino/build123d, затем переносим workflow
в платформенный формат.

### 2. Complex model to simplified analysis geometry

Первый активный engineering MVP.

Цель: превратить сложную Rhino/architect source geometry в simplified closed
parts или watertight analysis geometry для wind comfort и других анализов.

Принятое направление:

```text
source geometry -> classify architectural parts -> reconstruct closed simplified parts -> validate by sections/views
```

Не принимаем как финальный метод: global decimation, ShrinkWrap, Poisson, one
global loft или one hull/envelope.

### 3. Massing and revisions from TEPs

Rhino-first автоматизация раннего массинга: active scene, context, red lines,
underlays, rough/black massing, TEP, GFA/FAR/height constraints и правки
пользователя.

Цель: генерировать варианты, считать proxy metrics и применять revisions как
parameter deltas.

## Runnable MVP

```powershell
python -m ai_geometry_toolkit --help
```

Создать case folder:

```powershell
python -m ai_geometry_toolkit new-case `
  --scenario cleanup `
  --name test_data_2_mvp `
  --source test_data_2.3dm `
  --units m `
  --downstream Ladybug
```

Проверить и построить route:

```powershell
python -m ai_geometry_toolkit validate-case .\cases\<case_id>
python -m ai_geometry_toolkit route .\cases\<case_id>
```

Классифицировать Rhino `scan_scene` report:

```powershell
python -m ai_geometry_toolkit classify-scan .\cases\<case_id> `
  --scan "C:\VS Code\workfiles\rhino\workflow-kit\rhino_workflow_kit\reports\tower_bbox_classification.json"
```

Сравнить source и candidate scan перед acceptance:

```powershell
python -m ai_geometry_toolkit validate-candidate .\cases\<case_id> `
  --source-scan .\cases\<case_id>\reports\scene_scan.json `
  --candidate-scan .\cases\<case_id>\reports\candidate_scan.json
```

Подключить локальный `text-to-cad` checkout:

```powershell
python -m ai_geometry_toolkit link-backend .\cases\<case_id> `
  --backend text-to-cad `
  --repo "C:\VS Code\text-to-cad"
```

Импортировать Live OBJ-style semantic metadata:

```powershell
python -m ai_geometry_toolkit import-semantic-obj .\cases\<case_id> `
  --source tests\fixtures\office_tower_semantic.live.obj
```

## Выходные артефакты case folder

- `case.json`
- `params.json`
- `intake.md`
- `reports/development_route.md`
- `reports/source_classification.json`
- `reports/candidate_validation.json`
- `reports/candidate_validation.md`
- `reports/backend_text_to_cad.md`
- `reports/semantic_parts.json`
- `reports/semantic_parts.md`
- `reports/semantic_plan.json`
- `reports/semantic_validation.md`
- `reports/validation.md`

## Карта репозитория

- `AGENTS.md` - короткий стартовый контекст для AI/code agent без истории чата.
- `docs/START_HERE.md` - главный маршрут чтения для нового чата или нового компьютера.
- `ai_geometry_toolkit/` - runnable orchestration CLI.
- `tests/` - unit tests and fixtures.
- `docs/repository-map.md` - карта структуры repo: что читать первым, что не читать без нужды.
- `docs/context-system.md` - куда сохранять project context, cases, errors и decisions.
- `docs/project-data-map.md` - карта active data/source across repo, Rhino workfiles, Obsidian, `text-to-cad`, Spellshape/Live OBJ.
- `docs/development-state.md` - текущий статус разработки и next engineering steps.
- `docs/error-ledger.md` - известные failure modes.
- `docs/reference-modeling-gates.md` - обязательные gates для Scenario 1: source authority, constructive grammar, missing-view check.
- `docs/spellshape-live-obj-direction.md` - направление Spellshape / Live OBJ как semantic sketch layer.
- `docs/source-repos/` - сжатые карточки внешних репозиториев: что брать, где применять, что не тащить.
- `docs/external-repo-constructor-map.md` - карта внешних репозиториев StepanKukharskiy и элементов конструктора, которые можно встроить в pipeline.
- `docs/development-directions-repo-fit.md` - матрица: какие внешние repo pieces полезны для Scenario 1, 2 и 3.
- `ai_geometry_workplan.md` - roadmap по сценариям.
- `TEAM_UPDATE_2026-05-21.md` - team-facing status snapshot.
- `NEWS.md` - хронология изменений на русском.
- `decisions/` - принятые technical decisions.
- `ai_geometry_research.html` - public/team report page.

## Текущий статус

На 2026-05-28 активный engineering MVP - Scenario 2 на `test_data_2.3dm`.

Следующие практические шаги:

1. Перенести Rhino `scan_scene.py` в `ai_geometry_toolkit`.
2. Нормализовать section extraction reports.
3. Построить `v4_refined_clean_massing` как reproducible case.
4. Расширить `semantic_obj` / `live_obj_import`: planner -> build123d/Rhino
   script candidate.

## Правила данных

Перед добавлением новых данных читать `docs/context-system.md`.

Коротко:

- shared truth хранится в repo docs;
- один modeling run хранится в case folder;
- local smoke tests идут в `.tmp_cases/`;
- личная cross-repo memory идет в Obsidian;
- известные failures идут в `docs/error-ledger.md`;
- durable decisions идут в `decisions/`.
