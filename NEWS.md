# Новости

## 2026-06-01 - Зафиксирован правильный workflow для Grove at Grand Bay

После нескольких неверных вариантов закреплено правило для башен с поворотом
ортогональных этажей:

```text
ключевые сечения
-> временный loft
-> Rhino Contour по отметкам этажей
-> скрыть loft
-> строить финальные этажи напрямую из contour-кривых
```

Важное уточнение по фасаду: contour-кривая задает внешний край плиты/балкона,
а не линию стекла. Поэтому финальная сборка должна разделять:

- толстую плиту перекрытия / балконную плиту;
- стеклянную плоскость с отступом внутрь;
- наружный профиль/ограждение по краю плиты;
- roof datum `310 ft = 94.488 m`;
- mechanical/communication datum `320 ft = 97.536 m`.

Запрещено заново собирать этажи из guessed corners, bbox-прямоугольников или
ресэмплинга кривых. Если пользователь уже построил loft и сделал `Contour`,
эти contour-кривые становятся источником истины для этажей.

Обновлено:

- `docs/reference-modeling-gates.md`
- `docs/error-ledger.md`
- `decisions/2026-06-01-grove-contour-derived-floor-plates.md`
- Obsidian: `50 Research/Grove Contour Floor Plates 2026-06-01.md`

## 2026-05-28 - Добавлен gate `constructive grammar before geometry`

После неудачного первого blockout Karlatornet зафиксировано новое обязательное правило для Scenario 1 `Reference to model`.

Проблема: модель была построена как один угаданный envelope, хотя правильная логика объекта - четыре квадратных ствола, центральный крест/просветы, высотные отметки скручивания, loft по сечениям и зеркалирование/повторение частей.

Добавлено:

- `docs/reference-modeling-gates.md`
- `decisions/2026-05-28-constructive-grammar-before-reference-modeling.md`
- обновления в `docs/error-ledger.md`, `docs/context-system.md`, `docs/development-state.md`
- Obsidian note: `50 Research/Constructive Grammar Before Geometry 2026-05-28.md`

Новый обязательный порядок:

```text
source authority
-> constructive grammar
-> section/repetition strategy
-> missing-view check
-> geometry
-> compare
```

Если ракурсов не хватает, нужно запросить их до моделинга. Строить "правдоподобный" envelope без доказанной конструктивной грамматики запрещено.

## 2026-05-28 - Зафиксирована карта внешних репозиториев для geometry pipeline

Добавлен быстрый индекс по репозиториям StepanKukharskiy, чтобы не перечитывать их заново при поиске полезных элементов конструктора:

- `docs/external-repo-constructor-map.md`
- Obsidian: `50 Research/External Repo Constructor Map for Text-to-CAD 2026-05-28.md`

В карту вынесены источники и конкретные reusable pieces:

- Live OBJ semantic metadata: `#@params`, `#@controls`, `#@bbox`, `#@anchor`, `#@constraint`, `#@lock`, `#@hidden`, `#@source`;
- decomposed generation planner: сначала part plan, затем построение частей по одной;
- raw post operations и validation vocabulary;
- Rhino/Grasshopper Live OBJ renderer как reference для локального просмотра;
- Live OBJ executor/CadQuery hooks как словарь идей, но не как финальный STEP backend;
- surgical patching через exact `find` / `replace`;
- prompt rules для модульной генерации зданий;
- `2DPlanTo3D` contour extraction для будущего plan/elevation intake;
- `.spell` expression/distribution идеи для повторяющихся этажей, панелей и модулей.

Принятое действие: ближайшая интеграция не переносит весь Spellshape runtime. Мы забираем только маленькие проверяемые элементы: schema, validation, planner, contours, patching и route hints.

## 2026-05-28 - Встроена первая часть полезных Live OBJ fragments

`import-semantic-obj` теперь применяет несколько практических элементов из `live-obj`, без переноса внешнего runtime:

- validation gate для известных `#@` metadata keys;
- allowlist для post-ops: `transform`, `symmetrize`, `mirror`, `array`, `deform`, `subdivide`, `smooth`, `simplify`, `snap_to_ground`, `center_origin`, `material`, `tag`;
- автоматический `buildMethod` для частей: `build123d_step`, `rhino_preview`, `guide_only`, `manual_review`;
- генерация `reports/semantic_plan.json` в decomposed planner shape;
- генерация `reports/semantic_validation.md` для быстрого ревью ошибок и предупреждений.

Это закрывает первые два практических фрагмента из карты: metadata validation и planner schema. Следующий полезный шаг - генератор `semantic_plan.json -> build123d/Rhino candidate script`.

## 2026-05-28 - Разложена полезность внешних repo pieces по трем направлениям

Добавлен документ `docs/development-directions-repo-fit.md`.

Вывод:

- Scenario 1 `Reference to model`: сильнее всего нужны `2DPlanTo3D` contour extraction, Live OBJ semantic planning, source-authority gates и только потом distribution/expression идеи.
- Scenario 2 `Complex Rhino model -> simplified analysis geometry`: внешние repo pieces полезны только как поддержка. Главный путь остается Rhino/Aurox readback, part-aware reconstruction и source-derived validation.
- Scenario 3 `Massing from TEPs and revisions`: самый сильный fit для Live OBJ planner, params/controls, surgical patching и expression/distribution идей из `spellshape-three`.

Практическое правило: не тащить весь Spellshape runtime. Для каждого направления брать только подходящие элементы конструктора.

## 2026-05-28 - Добавлено направление Spellshape / Live OBJ как семантический слой до CAD

Зафиксировано новое исследовательское направление для `txt-to-cad`: использовать идеи
Spellshape / Live OBJ не как замену CAD-backend, а как промежуточный слой между
промптом/референсом и точной CAD-реконструкцией.

Источник:

- сайт: https://spellshape.com/
- основной актуальный репозиторий: https://github.com/StepanKukharskiy/live-obj
- связанный meta-repo: https://github.com/StepanKukharskiy/spellshape
- форматный эксперимент: https://github.com/StepanKukharskiy/spellshape-format

Главная идея: обычный OBJ можно расширять комментариями `#@`, где хранится
семантика сцены, параметры, controls, anchors, bbox, locks, constraints и
пост-операции. Обычные 3D-инструменты видят mesh, а наш пайплайн может читать
metadata как намерение модели.

Принятое место в нашей архитектуре:

```text
prompt / reference / intent
-> semantic OBJ / Live OBJ sketch
-> part table + anchors + controls
-> build123d / Rhino reconstruction
-> STEP / 3DM validation
```

Решение: не переносить Spellshape целиком и не заменять `text-to-cad`.
Использовать его как источник паттерна для собственного `semantic_obj` /
`live_obj_import` этапа.

Документ направления: `docs/spellshape-live-obj-direction.md`.

## 2026-05-28 - Пройден первый smoke test `semantic_obj`

Добавлен короткий проверочный тест для нового подхода:

```text
office_tower_semantic.live.obj
-> import-semantic-obj
-> reports/semantic_parts.json / .md
-> Rhino preview through Aurox
```

Тестовый объект: "Офисная башня 24 этажа на овальном подиуме, с двумя входными
объемами и сеткой фасада."

Добавлено:

- `tests/fixtures/office_tower_semantic.live.obj`
- команда `import-semantic-obj`
- parser Live OBJ-style `#@` metadata
- `scripts/build_semantic_smoke_rhino.py`
- unit test на извлечение part table

Результат smoke run:

```text
partCount=5
visiblePartCount=4
partsWithParams=5
partsWithBbox=5
partsWithAnchors=4
partsWithControls=2
guideParts=1
```

Через Aurox на Rhino port `9876` построен preview: 4 massing solids и 33 facade
guide curves на слоях `SEMANTIC_OBJ_SMOKE*`. Capture сохранен локально в
`.tmp_cases/semantic_obj_smoke_rhino_capture.png`.

Вывод: подход прошел самый короткий архитектурный тест. Metadata реально дает
таблицу частей и route hints до CAD, но preview остается smoke artifact, не
валидированным STEP/Brep результатом.

## 2026-05-21 - Уточнены три продуктовых вектора

Проект больше не сводится к одному сценарию mesh cleanup. Зафиксированы три
направления:

1. `Reference to model` - долгосрочное направление для будущей интеграции в
   AI-платформу. Сначала строим надежный локальный движок, вероятно через
   Rhino, затем переносим workflow в платформенный формат.
2. `Complex model to simplified analysis geometry` - первый активный инженерный
   MVP. Это внутренний Rhino workflow для подготовки архитектурных моделей к
   wind comfort и другим анализам.
3. `Massing and revisions from TEPs` - Rhino-first автоматизация раннего
   массинга: сцена, контекст, red lines, underlays, rough volumes, TEP,
   ограничения и правки пользователя.

`text-to-cad` теперь описан как STEP-first reference/backend, который надо
адаптировать под архитектурные источники: фасады, планы, elevations,
source-authority gates и staged validation.

## 2026-05-21 - Добавлены контекстные rails репозитория

Добавлены документы, которые объясняют, где хранить состояние проекта, данные,
ошибки и решения:

- `docs/context-system.md`
- `docs/project-data-map.md`
- `docs/development-state.md`
- `docs/error-ledger.md`
- `.github/ISSUE_TEMPLATE/engineering-task.yml`
- `.github/ISSUE_TEMPLATE/failure-lesson.yml`

Цель: будущая работа должна восстанавливаться из репозитория, а не из смеси
чатов, временных файлов и личных заметок.

## 2026-05-21 - Подключен backend `text-to-cad`

Добавлена команда `link-backend`, которая регистрирует локальный checkout
`earthtojake/text-to-cad` в конкретном case folder.

Команда проверяет ожидаемые CAD skill files, пишет:

- `reports/backend_text_to_cad.md`
- `reports/backend_text_to_cad.json`

и фиксирует backend в:

- `case.json`
- `params.json`

Граница ответственности:

- Rhino/Aurox отвечает за `.3dm` scan, overlays, classification и section extraction.
- `text-to-cad` отвечает за чистые STEP-first parametric candidates после
  принятого route.

## 2026-05-21 - Первый runnable orchestration MVP

Добавлен пакет `ai_geometry_toolkit` - case-based CLI для этого репозитория.

Команды:

- `new-case`
- `validate-case`
- `route`
- `classify-scan`
- `audit-scan`
- `link-backend`

Первый smoke test создал Scenario 2 cleanup case и классифицировал существующий
Rhino scan-like report:

```text
primary_envelope=1
podium_base=11
supports=41
large_bands=3
crown_roof=207
facade_detail=1627
noise=671
```

Это не финальная архитектурная правда. Это первый устойчивый routing layer:
перед build stage система уже умеет создать case, сохранить параметры,
классифицировать источник и записать development route.

## 2026-05-21 - Зафиксировано направление Scenario 2

Benchmark переключен с одиночной башни `22.3dm` на комплексный
`test_data_2.3dm`.

Источник содержит башню, овальный подиум, малый rounded podium, connector slab,
supports, facade ribs, bands и crown detail.

Принятое направление:

```text
source mesh -> classify architectural parts -> reconstruct closed simplified parts -> validate by views/sections
```

Запрещено принимать как финальный метод: global decimation, ShrinkWrap, Poisson,
one global loft, one hull/envelope или попытку сделать весь объект одной
watertight shell без part-aware validation.

`test_data2_v3_clean_massing` остается closed baseline, но он слишком
абстрактный. Следующая цель: `v4_refined_clean_massing`.

## 2026-05-20 - NURBS restart from named rails

После 12 итераций mesh simplification стало ясно, что mesh-primitive подход не
дает архитектурно корректную форму башни.

Активное направление для сложной tower reconstruction:

- извлечь named architectural rails;
- проверить rails во front/top/side views;
- строить Brep/NURBS surfaces от rails;
- не делать raw global loft через зоны с разной топологией.

## 2026-05-19 - Решение по feature-preserving mesh reconstruction

Для Scenario 2 принят исследовательский путь:

- CGAL Shape Detection / Efficient RANSAC;
- CGAL Polygonal Surface Reconstruction;
- CGAL Alpha Wrapping как baseline;
- quad remeshing только после solid/fidelity validation.

VSA остается diagnostic-only: полезен для plane families и feature edges, но не
является полноценным solidification pipeline.

## 2026-05-18 - Создан первый workflow kit

Создан initial workflow kit:

- три intake templates;
- три JSON schemas;
- `scan_scene.py`;
- `extract_sections.py`;
- `rhino_runner.py`.

Ключевой урок: section extraction не равен section correspondence. Перед lofting
нужны stable side/corner anchors, consistent seams и zone splits.
