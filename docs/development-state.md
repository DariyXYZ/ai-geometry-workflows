# Development State

Обновлено: 2026-06-01

## Активный репозиторий

```text
C:\VS Code\workfiles\ai-geometry-workflows
https://github.com/DariyXYZ/ai-geometry-workflows
```

Проект перешел от loose Rhino experiments к case-based orchestration toolchain.
На 2026-06-01 добавлен переносимый context layer: `AGENTS.md`,
`docs/START_HERE.md`, `docs/repository-map.md` и `docs/source-repos/`.
Цель - чтобы новый AI-чат мог восстановить workflow из repo без Obsidian и
истории переписки.

## Текущее состояние

Активный engineering MVP - Scenario 2:

```text
complex Rhino source
-> classified architectural parts
-> reconstructed closed simplified parts
-> section/view validation
```

Benchmark:

```text
test_data_2.3dm
```

Accepted baseline:

```text
test_data2_v3_clean_massing
```

Baseline закрытый и полезный, но слишком абстрактный. Следующая цель -
`v4_refined_clean_massing`, построенный как reproducible case, а не loose Rhino
script.

## Архитектурные слои

### 1. Rhino/Aurox readback

Отвечает за:

- `.3dm` scan;
- hidden/locked object inclusion;
- source overlays;
- architectural part classification;
- section extraction;
- fixed review captures.

### 2. Semantic sketch / Live OBJ research

Новое направление, добавлено 2026-05-28.

Источник: https://github.com/StepanKukharskiy/live-obj

Идея: использовать Spellshape / Live OBJ как источник паттерна для
`semantic_obj`, где rough OBJ preview хранит рядом `#@` metadata: parts, bbox,
anchors, params, controls, locks, constraints.

Статус: исследовательское направление, не production dependency.

Подробнее: `docs/spellshape-live-obj-direction.md`.

Быстрая карта внешних репозиториев и элементов конструктора: `docs/external-repo-constructor-map.md`.

Матрица применимости по трем направлениям: `docs/development-directions-repo-fit.md`.

Обязательные gates для Scenario 1 reference modeling: `docs/reference-modeling-gates.md`.

### 3. CAD-as-code backend

`text-to-cad` / build123d отвечает за:

- clean parametric source;
- STEP-first candidate generation;
- secondary exports when needed;
- CAD-friendly reproducibility.

Это не Rhino replacement и не mesh cleanup engine.

### 4. Case orchestration

`ai_geometry_toolkit` отвечает за:

- case folders;
- manifests and params;
- backend registration;
- routes;
- validation reports.

## Реализовано

CLI commands:

- `new-case`
- `validate-case`
- `route`
- `classify-scan`
- `audit-scan`
- `link-backend`
- `import-semantic-obj`

Case artifacts:

- `case.json`
- `params.json`
- `intake.md`
- `reports/development_route.md`
- `reports/source_classification.json`
- `reports/scan_audit.md`
- `reports/backend_text_to_cad.md`
- `reports/semantic_parts.json`
- `reports/semantic_parts.md`
- `reports/semantic_plan.json`
- `reports/semantic_validation.md`
- `reports/validation.md`

## Product vectors

### Vector 1 - Reference to model

Цель: future AI-platform integration.

Сначала строим надежный local engine через Rhino/build123d, затем переносим
workflow в платформенный формат.

Spellshape / Live OBJ может быть полезен здесь как upstream semantic sketch:
prompt/reference -> named parts/controls/anchors -> CAD script.

Перед геометрией обязательно фиксировать constructive grammar: из каких повторяемых частей собран объект, какие сечения/зеркала/arrays нужны, и каких ракурсов не хватает.

### Vector 2 - Complex model to simplified analysis geometry

Цель: internal Rhino production workflow.

Это первый активный MVP. Основной риск - снова скатиться в global mesh repair.
Не делать этого. Source fidelity важнее красивого watertight claim.

### Vector 3 - Massing and revisions from TEPs

Цель: Rhino-first early project automation.

Входы: active scene, red lines, underlays, rough massing, TEPs, GFA/FAR/height
constraints, user revisions.

Spellshape / Live OBJ тоже может быть полезен как semantic draft layer для
вариантов до build123d/Rhino reconstruction.

## Следующие engineering steps

1. Перенести Rhino `scan_scene.py` в этот repo.
   GitHub: https://github.com/DariyXYZ/ai-geometry-workflows/issues/1
2. Добавить `validate_candidate_vs_source`.
   GitHub: https://github.com/DariyXYZ/ai-geometry-workflows/issues/2
3. Перенести или обернуть `extract_sections.py` и нормализовать output в
   `reports/sections.json` / `reports/sections.csv`.
   GitHub: https://github.com/DariyXYZ/ai-geometry-workflows/issues/3
4. Построить `v4_refined_clean_massing` как real case.
5. Расширить прототип `semantic_obj`:
   `reports/semantic_plan.json` -> build123d/Rhino candidate script.
6. Следующие куски из `docs/external-repo-constructor-map.md`:
   contour extraction и surgical patching.
7. Использовать `docs/development-directions-repo-fit.md` перед выбором следующего направления, чтобы не тащить Scenario 1/3 инструменты в Scenario 2 cleanup.
8. Для каждого Scenario 1 case перед build stage писать constructive grammar и missing-view check.
9. Продвигать stable case outputs только после validation reports.
10. Поддерживать `AGENTS.md`, `docs/START_HERE.md` и `docs/source-repos/` как
    минимальный контекст для нового чата.

## Проверка

```powershell
python -m unittest discover -s tests
```

Последний известный результат: 5 tests passed.

## Не активно прямо сейчас

- Полная platform integration для Scenario 1.
- Полный Scenario 3 variant engine.
- Прямой global mesh repair.
- Packaging как Rhino plugin.
- Зависимость от Spellshape API/UI.
- Public examples.

Эти направления остаются в roadmap, но текущий foundation - readback,
classification, staged build и validation.
