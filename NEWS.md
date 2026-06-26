# Новости

## 2026-06-26 - Strengthened repo-as-skill architecture

Added a task-level routing layer so an AI can use the repository as a compact
skill instead of reading everything:

- `docs/task-read-maps.md`
- `docs/case-digest.md`
- `docs/experience-capture-format.md`

The new task map routes concrete asks such as "make a second massing variant"
to the right scenario, libraries, cases, dimensional defaults, and error gates.
The case digest gives a one-minute list of wins, failures, techniques, metrics,
standards, and current decisions. The experience format defines how a session is
promoted into a case note, pattern/operator, error, metric/default, prompt/hint,
decision, or tool note.

Cleaned ignored local build artifacts:

- `.pytest_cache/`
- `__pycache__/`
- `outputs/`

Fixed `.gitignore` so `docs/cases/` is not accidentally hidden from future
agents.

Updated:

- `AI_NAVIGATOR.md`
- `README.md`
- `docs/START_HERE.md`
- `docs/case-digest.md`
- `docs/repository-map.md`
- `docs/library-index.md`
- `docs/repo-maintenance-guide.md`
- `docs/context-system.md`
- `docs/project-data-map.md`
- `docs/case-library.md`

Follow-up stale-information audit:

- replaced active `MCPConnect` instructions with `MCPStart`;
- updated RhinoMCP setup wording to use local `.mcp.json` / installed router
  path instead of obsolete copy-command language;
- corrected active repo path references to `C:\VS Code\ai-geometry-workflows`;
- updated the latest known test result to `python -m pytest` -> 8 passed;
- removed active-case dependence on deleted ignored `outputs/rhino/*.3dm`
  artifacts.

## 2026-06-24 - Added Moscow road dimensional library

Added a road/street dimensional reference for Moscow massing and site context:

- `docs/libraries/moscow-road-dimensional-library-2026.md`

The library records lane-width and carriageway defaults for Rhino/Grasshopper
generators: magistral lanes, local streets, quarter driveways, production-zone
truck lanes, bus lanes, high-rise fire access, road-layer naming, and the
`VISUAL_LIFT_M = 0.001` rule for road markings and other coplanar graphics.

Updated:

- `docs/START_HERE.md`
- `docs/library-index.md`

## 2026-06-24 - Captured BC50 two-tower stylobate case lessons

Added the accepted BC50 massing case and promoted its modeling rules:

- `docs/cases/bc50-two-tower-stylobate-2026-06-24.md`
- `scripts/rhino/massing/two_tower_bc_50f_stylobate.py`

Key rules:

- use contour-derived roof/parapet geometry for stylobates and tower roofs;
- use straight core overruns/headhouses, not twisted roof cores;
- keep metric text on a vertical board outside the model;
- use translucent blue glass material for tower massing readability;
- raise thin finish surfaces by at least `0.001 m` to avoid Rhino viewport
  z-fighting/flicker.

Updated:

- `docs/case-library.md`
- `docs/error-ledger.md`
- `docs/errors/moscow-bc-massing-error-library.md`

## 2026-06-23 - Added Moscow 2026 dimensional baseline library

Added an active dimensional reference for Moscow residential and office massing:

- `docs/libraries/moscow-building-dimensional-library-2026.md`
- `docs/libraries/moscow-building-dimensional-library-2026.yaml`

The library separates normative gates from practice heuristics and generator
defaults: floor counts, floor heights, core placeholders, facade-to-core depths,
slab/service packages, flat/operated roof packages, parapets, openings, windows,
facade grids, and Grasshopper/Rhino validation flags.

Also mirrored the compact research note into Obsidian:

```text
C:\Users\dariy.n\Documents\Obsidian Vault\50 Research\Moscow Dimensions\Moscow Building Dimensional Library 2026.md
```

## 2026-06-18 - Уточнена структура отчета Scenario 3D

PDF чек-листа ДГП прочитан через `microsoft/markitdown`; извлеченный Markdown
сохранен как справочный материал:

```text
archive/reference/dgp-architecture-checklist-2026-06-13/markitdown.md
```

В `docs/scenarios/architecture-compliance-check.md` закреплена более строгая
русскоязычная структура отчета для сравнения вариантов объемного решения:

- начинать с исходных материалов и типа объекта, а не с общего вывода;
- сохранять порядок PDF: тип объекта, критерии оценки архитектурного облика,
  критерии градостроительной оценки, итоговая оценка;
- использовать одну таблицу критериев для всех вариантов;
- разделять «соответствие критерию», «не соответствие критерию / нет данных»,
  «риск» и «что исправить»;
- для скриншотов объемного решения без фасадного пакета отмечать как
  предварительные или `нет данных` критерии по фасадам, входным группам,
  пятому фасаду, подсветке, парковкам, ТЭП и нормам.
- все пользовательские отчеты Scenario 3D писать на русском в терминологии PDF;
  английские поля допустимы только как внутренние ключи YAML/automation.

## 2026-06-17 - Refined architecture checklist reporting after Flow_Model_V2 review

Updated Scenario 3D after reviewing `Flow_Model_V2.3dm` against the Moscow
architecture checklist.

Key corrections:

- reports must start with the PDF checklist criteria, not with free-form
  architectural commentary;
- classify object type first: `Видовой / Средовой / Не определено`;
- for a free-standing **Видовой** object, do not mechanically penalize lack of
  dense street frontage unless the site condition actually requires it;
- use binary `yes/no` for factual criteria such as two presented variants,
  architectural lighting, or visible surface parking;
- use exact evidence-based percentages for visual criteria instead of converting
  `pass/partial/fail` to round `100/50/0`;
- avoid vague report phrases such as "пятый фасад решен частично"; state what
  is visible and what is missing.

Updated:

- `docs/scenarios/architecture-compliance-check.md`
- `docs/libraries/moscow-architecture-approval-checklist.md`
- `docs/error-ledger.md`

## 2026-06-17 - Added Scenario 3D architecture approval checklist review

Added a new Scenario 3 subscenario for checking an existing building or massing
proposal against city/architecture approval criteria:

```text
3D - architecture compliance checklist review
```

Source checklist:

```text
C:\Users\dariy.n\Downloads\2026_06_13_ДГП_Чек_лист_оценки_архитектурного_объекта_2.pdf
```

Added:

- `docs/scenarios/architecture-compliance-check.md`
- `docs/libraries/moscow-architecture-approval-checklist.md`

Promoted workflow:

```text
connect Rhino MCP
-> inspect scene, units, context, bbox, roof, entries, frontage, parking
-> review main viewpoints and top/roof view
-> classify object as visual / contextual / unknown
-> score checklist criteria as pass / fail / not_enough_data / not_applicable
-> separate design checklist review from optional TEP/norm checks
-> report approval risks and recommended fixes
```

Updated Scenario 3 routing, massing decision rules, library index, repository
map, and AI navigator.

Later refinement:

- rendered all 15 PDF pages as visual reference screenshots in
  `archive/reference/dgp-architecture-checklist-2026-06-13/`;
- added visual example signals to
  `docs/libraries/moscow-architecture-approval-checklist.md`;
- added percentage scoring: architectural image %, urban planning %, weighted
  total %, and evidence coverage %;
- made five review views the minimum evidence set: north, south, east, west,
  and orthogonal top plan;
- promoted the core interpretation from the presentation: the city evaluates a
  complete urban image, not only facade appearance.

## 2026-06-16 - Cleaned repo architecture for active AI workflow use

Reorganized the repository into a stable active/archived structure:

```text
docs/scenarios/
docs/libraries/
docs/cases/
docs/errors/
docs/tools/
docs/research/
archive/reports/
archive/rhino-experiments-2026-06/
```

Root now keeps only entrypoints, package/tooling files, and active project
metadata. Historical public reports, old team updates, and one-off Rhino
experiment scripts/outputs were moved to `archive/`.

Added:

- `docs/README.md`
- `archive/README.md`
- `scripts/README.md`

Rewrote:

- `README.md`
- `docs/project-data-map.md`

Updated links and maintenance rules across the repo so future knowledge can be
added natively into the right folder instead of piling up in the root.

## 2026-06-16 - Imported useful Obsidian massing memory into repo navigation

Scanned the Obsidian vault for AI geometry, Moscow massing, Rhino/Aurox,
testing, research, and error notes. Added a durable repo bridge:

```text
docs/obsidian-knowledge-map.md
docs/libraries/form-operator-library.md
docs/libraries/massing-decision-library.md
```

Promoted useful Obsidian lessons into the repo:

- massing decision order must go from site/context to footprint, public space,
  massing family, operators, risk, then CAD parameters;
- every Scenario 3 variant needs a site-reasoned form operator, not plain boxes
  or decorative moves;
- Rhino pilot/test iterations v2-v8 are now referenced as case memory;
- visual typology catalog, site-footprint system, image-to-CAD protocol, and
  GhCrowdFlow movement research are listed as future imports.

Updated:

- `AI_NAVIGATOR.md`
- `docs/START_HERE.md`
- `docs/library-index.md`
- `docs/case-library.md`
- `docs/repository-map.md`

## 2026-06-16 - Started universal AI architecture library structure

Added the first navigation and maintenance layer for using this repo as a
portable architecture/geometry memory system for any AI agent:

```text
AI_NAVIGATOR.md
docs/library-index.md
docs/case-library.md
docs/repo-maintenance-guide.md
```

The repo is now explicitly organized around:

- scenario strategies;
- pattern and form libraries;
- successful and failed case memory;
- error and anti-pattern libraries;
- compressed external source-repo knowledge;
- Rhino/Aurox/build123d workflow gates.

Updated:

- `README.md`
- `docs/START_HERE.md`
- `docs/repository-map.md`

## 2026-06-16 - Moscow BC massing zoning failure promoted to error library

Added two durable Scenario 3 massing documents:

```text
docs/errors/moscow-bc-massing-error-library.md
docs/libraries/moscow-bc-site-zoning-patterns.md
```

The 2026-06-16 `AI_BC_V01-V03` Rhino variants passed numeric checks
(boundary, INSO, floor module, approximate GFA) but failed the design review:
low bars cut pedestrian movement, V02 had accidental building intersections,
the variants created narrow leftover gaps, and all variants were too box-like.

Promoted rule:

```text
zoning skeleton first
-> public spine/service edge/buildable bands/height anchors
-> architectural operator
-> geometry
-> hard constraints and TEP validation
```

Updated:

- `docs/error-ledger.md`
- `docs/START_HERE.md`
- `docs/repository-map.md`
- `docs/cases/moscow-bc-massing-modeling-brief-2026-06-16.md`

## 2026-06-16 - Split Scenario 3 into TEP/massing subscenarios

Added:

```text
docs/scenarios/tep-massing-scenario-subtypes.md
```

Scenario 3 now starts by classifying the task:

- `3A`: zoning, footprints, and entries are already given. Preserve them and
  work on building form, height, TEP, and constraints.
- `3B`: only plot boundary and entries/access are given. First create zoning
  and tentative footprints, then get zoning approval before architecture.
- `3C`: plot plus existing massing iteration are given. Use the source massing
  as the TEP/gabarit anchor and focus on image/form revision.

Updated:

- `docs/START_HERE.md`
- `docs/repository-map.md`
- `docs/development-state.md`
- `docs/libraries/moscow-bc-site-zoning-patterns.md`

## 2026-06-04 - Preserved recent Rhino/Aurox case memory for fresh chats

Added a compact durable case-memory file:

```text
docs/cases/recent-rhino-case-lessons.md
```

It records the latest results, techniques, and mistakes from:

- Infinity Tower / SOM;
- Shanghai Tower-style twisted shaft;
- Flock chapel shell;
- symmetric stepped residential tower;
- Aqua Tower / Studio Gang video demonstrator;
- Absolute World Towers video demonstrator.

Key rules promoted:

- user-prepared Rhino curves can be the highest source authority;
- soft triangular twist sections must be built from primitive/cutter logic, not
  organic point blobs;
- shell cases must pass footprint/support gates before glass and posts;
- fixed-envelope stepped towers must not taper when the plan types change;
- video replay scripts must preserve the user camera, slow construction down,
  ground the building, and remove obsolete helper geometry.

Updated:

- `AGENTS.md`
- `docs/START_HERE.md`
- `docs/repository-map.md`
- `docs/error-ledger.md`
- Obsidian: `30 Projects/AI CAD Platform/AI CAD Platform - Current Status.md`

## 2026-06-02 - Added RhinoCommon helper layer for native Rhino operations

Added a first runnable RhinoCommon helper runner:

```text
scripts/rhino_common_helper.py
```

The helper uses Aurox `execute_csharp` as the transport and executes native
RhinoCommon code inside the active Rhino document. This is the preferred route
for operations that should not be approximated by point drawing:

- visible source curve readback;
- soft closed NURBS/control-point curves;
- 2D curve boolean difference;
- Brep contours;
- custom C# operations through `run-csharp`.

Updated:

- `docs/tools/rhino-common-helper.md`
- `docs/context-system.md`
- `docs/repository-map.md`
- `docs/START_HERE.md`
- `docs/project-data-map.md`
- `TOOLKIT.md`
- `tests/test_cli.py`

## 2026-06-01 - Flock chapel shell: medium-success massing, failed support/fit/detail gates

The new shell-roof case reached a medium-success state: the generated roof
started to read as the intended wave/ribbon concrete shell rather than a flat
roof or generic surface. The main topography of alternating crests and valleys
was recognizable.

However, the model failed three important gates:

1. secondary elements such as glass, posts, and mullions were generated before
   the shell was accepted; they protruded below the shell and were misaligned;
2. the roof footprint was too long compared with the scaled plan underlay and
   had to be compressed manually;
3. the shell was treated as floating over the site instead of bearing on the
   concrete folded/plinth elements shown in the plan and sections.

Next attempt: build only the shell first, fit it to the plan footprint, create
the concrete folded supports/plinths at the low shell contact points, and add
glass/posts only after the shell/support relationship is accepted.

Updated:

- `docs/error-ledger.md`
- `docs/scenarios/reference-modeling-gates.md`
- `decisions/2026-06-01-flock-chapel-shell-medium-success.md`

## 2026-06-01 - Shanghai Tower v5: square cutter must be the actual section boolean

The latest Shanghai Tower-style Rhino attempt became substantially closer after
switching from an organic radial blob to this constructive grammar:

```text
raw triangle
-> rounded / softened triangle
-> rotated square cutter at the corner
-> 4 transformed sections over 632 m
-> 180 degree twist
-> loft validation before Contour floors
```

Remaining issue: the square cutters were visible as construction curves, but
the section notch was still generated by separate hand-coded notch points. That
made the cutters explanatory, not authoritative. The next version must derive
the final section directly from `soft triangle minus rotated square`, using the
actual square/triangle intersection or an equivalent explicit 2D trim operation.

Updated:

- `docs/error-ledger.md`
- `docs/scenarios/reference-modeling-gates.md`
- `decisions/2026-06-01-shanghai-tower-square-cutter-source-grammar.md`

## 2026-06-01 - Зафиксирован урок Shanghai Tower: cut-out section, not organic blob

В reference-to-model workflow для Shanghai Tower-подобной формы уточнена
constructive grammar сечения. Ошибка: моделировать план как округлый
полярный blob с радиальной вмятиной.

Правильная логика:

```text
мягкий треугольник
minus повернутый square/diamond cutter в углу
-> глубина выреза меняется по высоте
-> 4 контрольных сечения
-> loft validation
-> Contour этажи только после принятия формы
```

Обновлено:

- `docs/error-ledger.md`

## 2026-06-01 - Зафиксирован урок Infinity Tower: использовать подготовленные Rhino-кривые

В reference-to-model workflow для Infinity Tower/SOM выявлен повторяемый риск:
если пользователь уже построил в Rhino контур этажа, круг ядра и ось высоты,
нельзя заменять их упрощенным квадратным/прямоугольным параметрическим
сечением.

Принятое правило: user-prepared Rhino curves становятся source authority.
Башня должна строиться трансформацией копий точного контура по высоте:

```text
visible source curves
-> classify floor/core/axis
-> verify units and height
-> rotate exact floor contour through Z
-> loft/floor/facade guides from transformed copies
```

Обновлено:

- `docs/error-ledger.md`
- `docs/scenarios/reference-modeling-gates.md`
- `decisions/2026-06-01-infinity-tower-user-rhino-curves-source-authority.md`

## 2026-06-01 - Добавлен первый `validate-candidate` gate

В CLI добавлена команда `validate-candidate` для Scenario 2 cleanup workflow.
Она сравнивает source scan и candidate scan по scene bbox, size и center deltas,
пишет:

- `reports/candidate_validation.json`;
- `reports/candidate_validation.md`.

Это первый численный gate для проверки candidate/source соответствия перед
acceptance. Он не заменяет архитектурную проверку: даже `pass` требует
section/profile deltas, source overlays, fixed captures и review по частям.

Обновлено:

- `ai_geometry_toolkit/cli.py`
- `tests/test_cli.py`
- `README.md`
- `TOOLKIT.md`
- `docs/development-state.md`

## 2026-06-01 - Добавлено правило вертикальных сечений для Karlatornet-подобных форм

Зафиксирован новый урок по выбору метода построения. Не каждую скрученную башню
нужно строить через горизонтальные сечения этажей.

Для Karlatornet-подобной формы правильнее читать объект как четыре вертикальных
ствола с фасадными поверхностями, которые скручиваются в средней зоне:

```text
простые вертикальные примитивы
-> вертикальные направляющие / профильные кривые
-> loft переходной поверхности
-> зеркало / повторение на остальные части
-> достройка центрального креста и просветов
```

Сравнение методов теперь записано явно:

- Grove at Grand Bay: горизонтальные contour-кривые этажей из временного loft.
- Karlatornet: вертикальные сечения/направляющие, loft поверхности, зеркало.

Обновлено:

- `AGENTS.md`
- `docs/START_HERE.md`
- `docs/scenarios/reference-modeling-gates.md`
- `docs/error-ledger.md`
- Obsidian: `50 Research/Karlatornet Vertical Section Loft Workflow 2026-06-01.md`

## 2026-06-01 - Репозиторий упакован как переносимая память проекта

Добавлен стартовый слой для нового AI-чата или нового компьютера без Obsidian и
без истории переписки:

- `AGENTS.md` - короткие обязательные инструкции для агента;
- `docs/START_HERE.md` - маршрут чтения по сценариям;
- `docs/repository-map.md` - карта repo: что читать первым, что пропускать;
- `docs/source-repos/` - сжатая библиотека внешних репозиториев и reusable
  pieces.

Цель: репозиторий должен сам объяснять текущий workflow, правила, ошибки,
приемы моделирования и внешние источники. Новый агент должен начинать с
маленького read set, а не перечитывать весь repo и не угадывать контекст.

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

- `docs/scenarios/reference-modeling-gates.md`
- `docs/error-ledger.md`
- `decisions/2026-06-01-grove-contour-derived-floor-plates.md`
- Obsidian: `50 Research/Grove Contour Floor Plates 2026-06-01.md`

## 2026-05-28 - Добавлен gate `constructive grammar before geometry`

После неудачного первого blockout Karlatornet зафиксировано новое обязательное правило для Scenario 1 `Reference to model`.

Проблема: модель была построена как один угаданный envelope, хотя правильная логика объекта - четыре квадратных ствола, центральный крест/просветы, высотные отметки скручивания, loft по сечениям и зеркалирование/повторение частей.

Добавлено:

- `docs/scenarios/reference-modeling-gates.md`
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

- `docs/research/external-repo-constructor-map.md`
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

Добавлен документ `docs/research/development-directions-repo-fit.md`.

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

Документ направления: `docs/research/spellshape-live-obj-direction.md`.

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
