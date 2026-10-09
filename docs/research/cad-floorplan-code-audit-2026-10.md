# Код для генерации жилых и офисных планировок

Обновлено 9 октября 2026 года. Мы просмотрели исходники, чтобы понять, где действительно есть алгоритм, а где только интерфейс или пример. Под квартирографией здесь понимаем нужное число квартир каждого типа и их площади. Инструменты сгруппированы по типу алгоритма. В таблицах ссылки ведут на главные страницы репозиториев, ниже — на проверенные файлы по закреплённым коммитам (все 57 ссылок открываются на 9 октября). Лицензии, звёзды и дата последнего изменения взяты из GitHub API. На наших проектах генераторы пока не запускались. Общий обзор и вопросы лицензий — в [первом обзоре](cad-floorplan-generation-2026-10.md).

## С чего начать

- **Жилой этаж с коридором и квартирографией:** [EBA floor-plan-generation-engine](https://github.com/BhaveshY/floor-plan-generation-engine/tree/83cbb65e508f) — самый удобный старт на C# с Grasshopper: коридор, квартиры, комнаты, проверки. Лицензии нет, поэтому код — только как образец, пока автор не разрешит. Тот же сценарий под MIT — [Forma floorplate-generator](https://github.com/DanielGameiroAutodesk/floorplate-generator): Г-, П-, Н-образные корпуса и дворы, три стратегии квартирографии, проверка тупиков коридора по IBC.
- **Комнаты внутри квартиры:** [FloorPlan6](https://github.com/poolpet/floorplan6/tree/0f8a1421171f/core) (CP-SAT, понятный код, но AGPL-3.0) и [Habx Optimizer v2](https://github.com/habx/optimizer-v2/tree/77f0d1e66428/libs) (MIT, старые зависимости). Для непрямоугольных квартир — [дифференцируемый Вороной](https://github.com/nobuyuki83/floor_plan) (MIT, Rust).
- **Квартира по образцу:** [Hypergraph](https://github.com/ramonweber/hypergraph) (MIT) переносит утверждённую планировку в новый контур. Если соберём свою библиотеку планов, это самый предсказуемый путь.
- **Квартирография в Revit/Dynamo:** упаковщик [Refinery Toolkits](https://github.com/DynamoDS/RefineryToolkits/blob/8e1326d4ffea/src/SpacePlanning/Generate/Packing.cs) (Apache-2.0) — строительный блок, а не готовая секция.
- **Офисный этаж:** [Magnetizing](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/tree/9faf7d92a87e) и [HyparSpace](https://github.com/hypar-io/HyparSpace/tree/f277d1b9151b), см. [раздел про офис](#офис).

## Лицензии: что можно брать в продукт

| Можно встраивать | Только с раскрытием своего кода | Только как образец (лицензии нет) | Некоммерческое |
| --- | --- | --- | --- |
| MIT, Apache-2.0, BSD-3: Forma floorplate-generator, Habx, Hypergraph, Refinery Toolkits, ibuilder, HyparSpace, Mycelium, architect-layout-solver, archit-app, nobuyuki83/floor_plan, Infinigen, ProcTHOR, MaskPLAN, Biomorpher, PlanBee | AGPL/GPL: **FloorPlan6 (AGPL-3.0)**, Topologic (AGPL-3.0), GSDiff (GPL-3.0), depthmapX (GPL-3.0) | EBA, Magnetizing, Co-Layout, HypergraphFormer (веса на HF — Apache-2.0), UnitPacking, LayoutLab, IFC-GPT, floorplan-optimizer, msd-floorplan-challenge, WallPlan, DiffPlanner, Tell2Design | House-GAN / House-GAN++, HouseDiffusion; данные RPLAN, CubiCasa5K (CC BY-NC), Structured3D, 3D-FRONT |

Отсутствие лицензии означает «все права защищены»: идеи брать можно, копировать код — нет. Лицензию данных проверять отдельно от лицензии кода: модели, обученные на RPLAN или CubiCasa, наследуют некоммерческие ограничения.

## Инструменты по типу алгоритма

Звёзды (★) и дата последнего изменения — на 9 октября 2026.

### 1. Процедурные правила: коридор → полосы → квартиры → комнаты

Детерминированная или сидированная раскладка по шаблонам. Самый простой для отладки и ближе всего к тому, как проектирует архитектор секцию.

| Репозиторий | Язык, лицензия | Масштаб | Что уже работает | Что нужно доделать для нас |
| --- | --- | --- | --- | --- |
| [EBA](https://github.com/BhaveshY/floor-plan-generation-engine) | C#, нет | Этаж + квартира | Строит коридор, режет полосы на квартиры, подбирает типы под заданные количества, делит квартиры на комнаты по параметрическим шаблонам, ранжирует варианты. GH-адаптер — HTTP-клиент к локальному серверу движка. | Проверить на наших контурах; ядра, типы квартир, местные нормы. Получить разрешение автора на использование кода. |
| [Forma floorplate-generator](https://github.com/DanielGameiroAutodesk/floorplate-generator) | TypeScript (расширение Autodesk Forma), MIT, ★1, 2026-03 | Этаж | Делит корпус на крылья через граф, раскладывает квартиры по трём стратегиям (баланс / точная квартирография / эффективность), Г/П/V/Н-формы, двор, проверка эвакуации и тупиков по IBC; 170+ тестов. | Автор называет проект учебным. Алгоритм деления на крылья удобно перенести в GH/Python; нормы заменить на СП. |
| [ibuilder/massing](https://github.com/ibuilder/massing) | Python, MIT, ★122 | Этаж | `test_fit.py` раскладывает квартиры с двух сторон прямого коридора циклической последовательностью; `optimize()` перебирает 5 наборов квартир × парковку × глубину и сравнивает по доходности. | Только прямоугольный этаж; доли типов приблизительные; ядра нет. Хорош для быстрой оценки вместимости. |
| [FloorPlan6: этаж](https://github.com/poolpet/floorplan6) | Python, **AGPL-3.0** | Этаж | Ставит лестницы и коридор, режет оставшееся на квартиры, считает путь до лестницы по графу коридоров (польские нормы WT, лимит 40 м). Вывод — в ArchiCAD через Tapir. | Квартиры режутся по габаритному прямоугольнику зоны: на Г-/П-образном этаже выходят за контур. AGPL требует открыть наш код при распространении. |
| [Hypar UnitPacking](https://github.com/hypar-io/UnitPacking) | C#, нет | Линия корпуса | ~200 строк: перебирает сочетания ширин квартир вдоль одной линии. | Глубина, ядро, коридор, входы. |
| [ProcTHOR](https://github.com/allenai/procthor) | Python, Apache-2.0, ★474, 2023 | Дом | Граф комнат → рекурсивное деление прямоугольника на сетке → двери. | Сделан для обучения роботов, а не под нормы. Полезен как чистый образец деления. |
| [Infinigen Indoors](https://github.com/princeton-vl/infinigen) | Python/Blender, BSD-3, ★7,3k, активен | Квартира, дом | Решатель планировок на ограничениях и графе + расстановка мебели. | Сильно привязан к Blender; решатель придётся вычленять. |
| [LeandroDornela/floor-plan-generator](https://github.com/LeandroDornela/floor-plan-generator) | C# Unity, MIT, ★5 | Дом | Рост комнат на сетке по графу смежности. | Маленький проект; C# легко перенести в GH-ноду. |

### 2. Рекурсивное деление и упаковка прямоугольников

| Репозиторий | Язык, лицензия | Масштаб | Что делает | Ограничения |
| --- | --- | --- | --- | --- |
| [Refinery Toolkits](https://github.com/DynamoDS/RefineryToolkits) | C# Dynamo, Apache-2.0, ★53 | Зоны этажа | Жадная упаковка прямоугольников (MaxRects-подобная, по умолчанию `BestAreaFits`) в одну или несколько зон; узел Dynamo возвращает размещённые и оставшиеся элементы. | Упаковщик универсальный: про квартиры, входы и фасады ничего не знает. Состав квартир подбирать отдельно. |
| [Mycelium](https://github.com/MyceliumGH-Dev/Mycelium) | C# GH, Apache-2.0 | Участок | Рекурсивное ортогональное деление участка; проезды — зазоры между участками; разные типы объёмов. | Планировок этажей нет — подключить генератор этажа. |
| [LayoutLab](https://github.com/0209vaibhav/layoutlab) | Python + GH, нет | Комнаты | Упаковывает прямоугольные комнаты по площадям; есть файл Grasshopper. | Нет соседств, коридора, окон. |
| [squarify](https://github.com/laserson/squarify) | Python, ★335 | Блок | Squarified treemap — основа метода Marson & Musse для деления квартиры. | Только ядро; готовой реализации Marson & Musse не нашли. |

### 3. Сетка + ограничения (CP-SAT, CP, MILP, перебор с откатом)

Подходят, когда нужно жёстко соблюсти площади, соседства, окна и вход и получить объяснимый отказ.

| Репозиторий | Язык, лицензия | Решатель | Что делает | Что нужно доделать |
| --- | --- | --- | --- | --- |
| [FloorPlan6: комнаты](https://github.com/poolpet/floorplan6) | Python, **AGPL-3.0** | OR-Tools CP-SAT | Размеры и положение комнат: NoOverlap2D, вложенность, покрытие, соседства, фасад. Польские нормы в отдельном пакете `rules/`. | Контур и вход из Rhino; наши нормы; сложные контуры; вопрос AGPL. |
| [Habx Optimizer v2](https://github.com/habx/optimizer-v2) | Python, MIT, ★4, 2023 | OR-Tools CP (старый `pywrapcp`) + свой NSGA-II | Режет контур на ячейки, назначает их комнатам с учётом площадей, окон, входа и связей, затем многокритериально улучшает. | Одна квартира. ortools 7.5, numpy 1.18, shapely 1.7 и приватный индекс Gemfury с пакетами `lib-logger`, `lib-features` — заменять перед запуском. |
| [Co-Layout](https://github.com/xccElephant/co-layout) | Python, нет, ★17 | MILP (Gurobi) | Сетка комнат и проходов вместе с мебелью; LLM-агенты переводят текст в ограничения. | Нужна лицензия Gurobi; одна квартира; вывод в Rhino/Revit. |
| [architect-layout-solver](https://github.com/dashu-baba/architect-layout-solver) | Rust, MIT | Перебор с откатом | Компактный поиск прямоугольных комнат на сетке. | Ядро, коридоры, мост в GH. |
| [rectangularDualExplorer](https://github.com/joklawitter/rectangularDualExplorer) | JS, BSD-3 | Rectangular dual | Граф смежности → прямоугольная раскладка. Единственный открытый код этого метода, который нашли (GPLAN Шекхавата — только статьи). | Исследовательский инструмент. |

### 4. Непрерывная оптимизация

| Репозиторий | Язык, лицензия | Что делает | Ограничения |
| --- | --- | --- | --- |
| [nobuyuki83/floor_plan](https://github.com/nobuyuki83/floor_plan) | Rust, MIT, ★356 | Дифференцируемая диаграмма Вороного (Pacific Graphics 2024): площади комнат и связность в произвольном контуре. Хорошо подходит для квартир неправильной формы. | Rust, стены получаются ломаными — нужна ортогонализация. |
| [HypergraphFormer `run_parametric.py`](https://github.com/hsalehipour/HypergraphFormer/blob/7b1306932012/scripts/run_parametric.py) | Python, нет | Градиентный спуск по долям BSP-дерева подгоняет площади комнат. | Часть ML-конвейера, см. раздел 7. |

### 5. Метаэвристики (генетические алгоритмы, эволюционные стратегии)

| Репозиторий | Язык, лицензия | Что делает | Ограничения |
| --- | --- | --- | --- |
| [Magnetizing](https://github.com/hellguz/Magnetizing_FloorPlanGenerator) | C# GH, нет, ★71 | Сетка ячеек, коридор как ячейки `-1`, комнаты пристраиваются к коридору; квази-эволюция со случайными перезапусками. Писался под общественные здания. | Монолитный компонент; ядро, колонны, проверка доступа к каждой комнате. |
| [floorplan-optimizer](https://github.com/rainon-feroze/floorplan-optimizer) | Python, нет | GA на DEAP сам генерирует жилые планировки из случайной популяции и оценивает наложения, соседства, свет. | Путь к выходу приблизительный. |
| [Biomorpher](https://github.com/johnharding/Biomorpher) | C# GH, MIT, ★78 | Интерактивный GA с кластеризацией вариантов. Единственный открытый эволюционный движок для GH (Galapagos, Wallacei, Octopus, Opossum закрыты). | Это движок: генератор планировки надо подключить свой. |
| [DynaShape](https://github.com/LongNguyenP/DynaShape) | C# Dynamo, MIT | Физический решатель ограничений для пузырьковых диаграмм. | Надстройка DynaSpace для планировок публично не выложена. |

### 6. Перенос по образцу и графы

| Репозиторий | Язык, лицензия | Что делает | Что нужно |
| --- | --- | --- | --- |
| [Hypergraph](https://github.com/ramonweber/hypergraph) | C# Rhino, MIT, ★90 | `fitApartment`, `createApartmentsFromReference` переносят деление эталонного плана в новый контур с учётом фасада и циркуляции; есть мебель. Статья в Nature Communications 2024. | Библиотека наших утверждённых планировок. |
| [MSD floorplan challenge: поиск](https://github.com/Luraxx/msd-floorplan-challenge) | Python, нет | Поиск похожих планов (`baseline_retrieval*.py`). | Внешний датасет. |

### 7. Генеративные нейросети (GNN, диффузия, трансформеры, LLM)

Почти все обучены на домах и китайских квартирах RPLAN. Для продукта — только как исследование или с переобучением на своих данных.

| Репозиторий | Лицензия | Метод | Комментарий |
| --- | --- | --- | --- |
| [HypergraphFormer](https://github.com/hsalehipour/HypergraphFormer) | нет (веса на HF — Apache-2.0) | LoRA на Qwen3-4B-Instruct: граф связей → граф разбиения | 5 чекпойнтов [на HF](https://huggingface.co/NikitaKlimenko/HypergraphFormer); нужна GPU и C#-библиотека hypergraph на Mono. |
| [MSD floorplan challenge](https://github.com/Luraxx/msd-floorplan-challenge) | нет | Диффузия центров комнат на трансформере + взвешенный Вороной | Весов нет. |
| [MaskPLAN](https://github.com/HangZhangZ/MaskPLAN) | MIT, ★15, 2026-09 | Маскированная генерация (CVPR 2024) | Дорисовывает план по частичному вводу — сценарий «доведи квартиру». |
| [DiffPlanner](https://github.com/shidong-wang/DiffPlanner) | нет | Векторная диффузия (TVCG 2025) | Без растрового шага. |
| [Residential_Floorplan_Diffusion](https://github.com/zengpengyu-student/Residential_Floorplan_Diffusion) | MIT, ★18 | Диффузия | Жилые планы. |
| [floorplan-diffusion-guidance](https://github.com/zhanghuihui1988/floorplan-diffusion-guidance) | MIT, 2026-09 | Семантическое управление диффузией без дообучения | Свежий, без звёзд. |
| [House-GAN](https://github.com/ennauata/housegan) / [House-GAN++](https://github.com/ennauata/houseganpp) | **некоммерческая** | GAN по пузырьковому графу | Базовая линия для сравнения. |
| [WallPlan](https://github.com/cgjiahui/WallPlan) | нет | Генерация графа стен по контуру (SIGGRAPH 2022) | В репозитории в основном подготовка данных. |
| [Tell2Design](https://github.com/LengSicong/Tell2Design) | нет | Текст → план, seq2seq (ACL 2023) | Датасет + базовая модель. |
| [Holodeck](https://github.com/allenai/Holodeck) | Apache-2.0, ★575 | LLM строит план и сцену | Для симуляции, не для норм. |
| [Floorplan-generation](https://github.com/WizardZZH/Floorplan-generation) | GPL-3.0 | Нейросетевая раскладка по пузырьковой диаграмме | |
| [fml-wright](https://github.com/SebGr/fml-wright) | нет | Поэтапный GAN | 2022. |
| Graph2Plan, GSDiff, HouseDiffusion, TLC-PLAN | см. [первый обзор](cad-floorplan-generation-2026-10.md) | | |

Код не нашли (только статьи или пустые репозитории): GPLAN/G2PLAN, MIQP-раскладка Wu et al. 2018, iPLAN, ChatHouseDiffusion, HouseMind, HouseTune, Evolving Floor Plans. Kremlas (DeCodingSpaces) и Syntactic — бесплатные GH-плагины без исходников.

### 8. Оценка вариантов (функции качества)

| Репозиторий | Лицензия | Что считает |
| --- | --- | --- |
| [archit-app](https://github.com/archit-app/archit-app) | MIT | Комнаты, площади, связи, проходы; DXF/GeoJSON. Генератора нет. |
| [PlanBee](https://github.com/M-JULIANI/planbeeGH) | MIT, 2021 | Видимость, изовисты в Grasshopper. |
| [depthmapX](https://github.com/SpaceGroupUCL/depthmapX) | GPL-3.0 | Space syntax: VGA, осевой анализ. |
| [Topologic](https://github.com/wassimj/Topologic) | **AGPL-3.0** | Неманифолдная топология, дуальные графы ячеек — проверка соседств. |

### 9. Данные для тестов и обучения

| Набор | Лицензия данных | Что внутри |
| --- | --- | --- |
| [Swiss Dwellings v3](https://zenodo.org/records/7788422) | CC BY 4.0 | ~45 тыс. квартир в ~3,1 тыс. зданиях, целые этажи. Самый чистый по лицензии источник многоквартирных этажей. |
| [MSD](https://github.com/caspervanengelenburg/msd) | CC BY-SA 4.0 (Kaggle, ~17 ГБ) | 5372 этажа, 18,9 тыс. квартир; код готовит [графы](https://github.com/caspervanengelenburg/msd/blob/a5d069ee589a/graphs.py). Share-alike: производные данные открывать на тех же условиях. |
| [ResPlan](https://github.com/m-agour/ResPlan) | CC BY 4.0 | 17 тыс. жилых планов, вектор + граф. Южная Азия. |
| [MLStructFP](https://github.com/MLSTRUCT/MLStructFP) | MIT (код), архив с 2026-04 | Многоквартирные планы. |
| [CubiCasa5K](https://github.com/CubiCasa/CubiCasa5k) | **CC BY-NC 4.0** | 5 тыс. размеченных финских планов. |
| RPLAN ([инструменты](https://github.com/zzilch/RPLAN-Toolbox)) | **академическая** | 80 тыс. китайских квартир, основа большинства ML-моделей. |
| [Structured3D](https://github.com/bertjiazheng/Structured3D), 3D-FRONT | **некоммерческая** | Синтетические 3D-дома с мебелью. |

### 10. Коммерческие сервисы и плагины (закрытый код)

Проверены по сайтам и новостям на 9 октября 2026. Алгоритм указан, только если его раскрывает производитель. Основной подход для многоквартирных домов — правила плюс перебор вариантов; ML-модель всего этажа есть только у Forma, и та экспериментальная.

| Инструмент | Платформа | Что генерирует | Алгоритм | Выход | Статус |
| --- | --- | --- | --- | --- | --- |
| [TestFit](https://www.testfit.io) | Десктоп/веб | Многоквартирный дом с типами квартир и квартирографией, парковка | Конфигуратор на правилах + поиск по ТЭП (Generative Design, 2024) | Revit, AutoCAD, SketchUp, Excel; есть MCP | Живой, подписка |
| [Finch3D](https://docs.finch3d.com/llms.txt) | Веб + Revit/Rhino/GH/ArchiCAD | Этаж с коридором, лестницами и квартирографией, затем планировки квартир | 3 алгоритма этажа, графовые правила, адаптивная библиотека планов, ИИ-ассистент | Обратно в Revit, ArchiCAD, Rhino | Живой; планировки квартир — только Enterprise |
| [Autodesk Forma — Building Layout Explorer](https://adsknews.autodesk.com/en/news/building-layout-explorer-in-autodesk-forma/) | Веб | Планы офисов и многоквартирных этажей по объёму | Нейросетевая модель Autodesk | Revit | Экспериментальный (с 2026-06), только США |
| [ArkDesign.ai](https://arkdesign.ai/faq/) | Веб | Многоквартирные схемы с квартирами по нормам США | ИИ + правила норм | `.rvt`, PDF | Живой |
| [Zenerate](https://en.prnasia.com/releases/global/zenerate-announces-partnership-with-avalonbay-communities-to-support-early-stage-multifamily-feasibility-analysis-539272.shtml) | Веб | Участок, объём, этажи, квартирография, парковка, финмодель | Перебор 50 тыс.+ вариантов | Revit, AutoCAD, Excel | Живой |
| [Architechtures](https://archgyan.com/architechtures-ai-building-design-platform/) | Веб | Жилые здания: квартирография и этажи по ограничениям | Свой генеративный движок | IFC, DXF, XLSX | Живой по каталогам 2025–26; сайт из РФ не открылся |
| [Archistar](https://archistar.ai/for-architects/page/14) | Веб | Квартиры, таунхаусы, деление участков; инсоляция и проветривание | Библиотека + правила | GLTF, DXF, Rhino | Живой |
| [PlanFinder](https://www.food4rhino.com/en/app/planfinder) | Rhino/GH | Fit: подбор плана квартиры из базы по стенам и входу; Generate по числу комнат; мебель | Поиск по базе + ИИ | Rhino | Живой, €10/мес |
| [Maket.ai](https://www.testingcatalog.com/maket-2-0-brings-ai-floor-plans-and-3d-home-renders/) | Веб | Частные дома и таунхаусы из текстового брифа | Генеративная модель + LLM | DXF, PDF | Maket 2.0 вышел 2026-10-02 |
| [Snaptrude](https://www.dezeen.com/2025/10/15/snaptrudes-ai-platform-architects/amp/) | Веб-BIM | Программа → раскладка (Pack, Arrange по соседствам), сильнее на домах | ИИ + решатель соседств | Revit | Живой |
| [Higharc](https://www.inman.com/2025/02/14/higharcs-ai-seeks-to-pick-up-the-pace-of-home-construction/) | Веб | Типовые дома для девелоперов, эскиз → BIM | Распознавание + параметрическая модель | Рабочая документация | Живой |
| [Planner 5D](https://planner5d.com/use/ai-floor-plan-generator) | Веб/мобайл | Комнаты и дома по размерам | ИИ-генерация | Платные форматы, API | Живой |

**Российский рынок.** Коммерческого генератора «квартирография → план этажа» не нашли.
- [ПИК Digital R2.ОПР](https://habr.com/ru/companies/pik_digital/articles/960766/) — внутренняя платформа: раскладывает квартиры на типовом этаже под квартирографию, считает инсоляцию по окнам, использует библиотеку ядер и типовых квартир; перебор с оптимизацией. Пилот, наружу не продаётся.
- [Самолёт 10D](https://www.comnews.ru/digital-economy/content/240066/2025-07-08/2025-w28/1012/it-reshenie-samoleta-pomogaet-operativno-ocenit-investicionnyy-potencial-uchastka-pod-zastroyku) — внутренняя: по типам квартир и положению лестниц и лифтов выдаёт топ-10 раскладок с проверкой инсоляции по СанПиН.
- [rTIM](https://rutube.ru/video/cf59601e7ccab7d474af545a95fa52a3/) — коммерческая платформа генерации территории и ТЭП; планировок квартир не подтверждено.
- Плагины Revit [ModPlus](https://modplus.org/en/news/mprapartmentbuildinglayout), ITEMIKA, Marks Digital «Квартирография» только заполняют параметры и спецификации, планы не генерируют.

Не подходят: Hypar (ушёл в офисы и медицину), qbiq и laiout (офисы), Swapp (документация), ArchiLabs (дата-центры), Modelur и Digital Blue Foam (только объёмы), Delve (закрыт).

## Какие файлы брать разработчику

### Жилой этаж и квартира

- **EBA:** [CandidateGenerator.cs](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Generation/CandidateGenerator.cs) строит этаж (`TryResolveCorridor` → полоса коридора → нарезка полос на квартиры); [UnitMixPlanner.cs](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Generation/UnitMixPlanner.cs) задаёт состав квартир; [RoomTemplateGenerator.cs](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Generation/RoomTemplateGenerator.cs) и [DwellingTemplateGenerator.cs](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Generation/DwellingTemplateGenerator.cs) строят комнаты. [DoorNetworkBuilder.cs](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Topology/DoorNetworkBuilder.cs) не расставляет двери, а заносит уже существующие двери в граф связей и сверяет их. [FloorPlanEngine.cs](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/FloorPlanEngine.cs) запускает генерацию и проверки. [fp_generate.py](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/adapters/grasshopper/fp_generate.py) — HTTP-клиент: сначала поднять локальный сервер движка (`scripts/run-web.ps1`, `localhost:5127`); текстовый бриф по флагу `use_ai` разбирает Claude или Codex.
- **FloorPlan6, этаж:** [floor_layout.py](https://github.com/poolpet/floorplan6/blob/0f8a1421171f/core/floor_layout.py) строит квартиры, лестницы и коридор; [floor_validation.py](https://github.com/poolpet/floorplan6/blob/0f8a1421171f/core/floor_validation.py) ищет кратчайший путь до лестницы по осям коридоров (networkx). Функция `_slice_zone` режет габаритный прямоугольник зоны на равные квартиры, поэтому на сложном контуре квартиры попадают за границу здания — README это признаёт.
- **FloorPlan6, квартира:** [cpsat_solver.py](https://github.com/poolpet/floorplan6/blob/0f8a1421171f/core/cpsat_solver.py) размещает комнаты; [variant_generator.py](https://github.com/poolpet/floorplan6/blob/0f8a1421171f/core/variant_generator.py) делает несколько вариантов; [templates/](https://github.com/poolpet/floorplan6/tree/0f8a1421171f/templates) хранит состав помещений.
- **Небольшие заготовки:** [UnitPacking.cs](https://github.com/hypar-io/UnitPacking/blob/4e76bffba623/src/UnitPacking.cs) подбирает сочетания ширин; [LayoutLab packing_engine.py](https://github.com/0209vaibhav/layoutlab/blob/c31c19bf2eb3/gh/services/packing_engine.py) раскладывает комнаты, а [cedar_floor_planner.gh](https://github.com/0209vaibhav/layoutlab/blob/c31c19bf2eb3/grasshopper/cedar_floor_planner.gh) показывает связку с GH.
- **Dynamo/Revit, упаковка квартир:** [RectanglePacker.cs](https://github.com/DynamoDS/RefineryToolkits/blob/8e1326d4ffea/src/SpacePlanning/Generate/Packers/RectanglePacker.cs) содержит алгоритм; [Packing.cs](https://github.com/DynamoDS/RefineryToolkits/blob/8e1326d4ffea/src/SpacePlanning/Generate/Packing.cs) даёт узел Dynamo; [пример `.dyn`](https://github.com/DynamoDS/RefineryToolkits/blob/8e1326d4ffea/samples/SpacePlanning/dt_GenerativeToolkit_PackingRectangles_BAF.dyn) показывает использование.
- **Быстрая проверка квартирографии:** [ibuilder `test_fit.py`](https://github.com/ibuilder/massing/blob/523e5b3a120b/services/api/src/aec_api/test_fit.py): `layout()` берёт тип квартиры как `seq[i % len(seq)]`, число каждого типа = round(доля · 12); `optimize()` перебирает наборы и ранжирует по доходности к затратам.
- **Habx:** [grid.py](https://github.com/habx/optimizer-v2/blob/77f0d1e66428/libs/modelers/grid.py) режет контур на ячейки; [constraints_manager.py](https://github.com/habx/optimizer-v2/blob/77f0d1e66428/libs/space_planner/constraints_manager.py) назначает комнаты; [refiner.py](https://github.com/habx/optimizer-v2/blob/77f0d1e66428/libs/refiner/refiner.py) — свой NSGA-II «по мотивам DEAP» (сам DEAP не подключён); [optimizer.py](https://github.com/habx/optimizer-v2/blob/77f0d1e66428/libs/optimizer.py) собирает процесс.
- **Co-Layout:** [floorplan_model.py](https://github.com/xccElephant/co-layout/blob/e847bfaf8523/optimization/floorplan_model.py) — модель комнат и проходов; [coopt_model.py](https://github.com/xccElephant/co-layout/blob/e847bfaf8523/optimization/coopt_model.py) добавляет мебель.
- **HypergraphFormer:** [generators.py](https://github.com/hsalehipour/HypergraphFormer/blob/7b1306932012/scripts/generators.py) получает от модели граф разбиения; [run_parametric.py](https://github.com/hsalehipour/HypergraphFormer/blob/7b1306932012/scripts/run_parametric.py) подгоняет доли площадей.
- **MSD:** [деление квартиры](https://github.com/Luraxx/msd-floorplan-challenge/blob/c0074ace4f04/src/model/partition.py), [модель центров комнат](https://github.com/Luraxx/msd-floorplan-challenge/blob/c0074ace4f04/src/model/centroid_diffusion_model.py), [сборка полигонов](https://github.com/Luraxx/msd-floorplan-challenge/blob/c0074ace4f04/src/model/centroid_reconstruct.py).
- **Hypergraph:** [Apartment.cs](https://github.com/ramonweber/hypergraph/blob/fe049f1c31fb/ResearchGeometryLibrary/RGeoLib/BuildingSolver/Apartment.cs) переносит готовый план в новый контур.
- **Участок:** [ParcelSubdivision.cs](https://github.com/MyceliumGH-Dev/Mycelium/blob/dbb074dc206d/src/Mycelium/Core/ParcelSubdivision.cs) делит участок; [BuildingGenerators.cs](https://github.com/MyceliumGH-Dev/Mycelium/blob/dbb074dc206d/src/Mycelium/Core/BuildingGenerators.cs) строит контуры корпусов.
- **Мелкие решатели:** [architect-layout-solver](https://github.com/dashu-baba/architect-layout-solver/blob/3990f3dc5bc3/constraints-resolver/src/candidate_generation.rs), [floorplan-optimizer `ga.py`](https://github.com/rainon-feroze/floorplan-optimizer/blob/7cf5326332db/floorplan/ga.py).

### Офис

- **Magnetizing:** [основной алгоритм](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/MagnetizingRooms_ES.cs) получает контур, сетку, площади и связи комнат; входные структуры — [HouseInstance.cs](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/RoomProgram/HouseInstance.cs) и [RoomInstance.cs](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/RoomProgram/RoomInstance.cs). Несмотря на названия `House*`, состав помещений можно заменить офисным.
- **HyparSpace** (MIT): [PrivateOfficeLayout.cs](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/LayoutFunctions/PrivateOfficeLayout/src/PrivateOfficeLayout.cs) делит зону на кабинеты; [OpenOfficeLayout.cs](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/LayoutFunctions/OpenOfficeLayout/src/OpenOfficeLayout.cs) и [LayoutStrategies.cs](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/LayoutFunctions/LayoutFunctionCommon/LayoutStrategies.cs) ставят рабочие места; [AdaptiveGridBuilder.cs](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/TravelDistanceAnalyzer/src/AdaptiveGridBuilder.cs) строит сеть проходов. [Старый модуль зонирования](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/ZonePlanningFunctions/Archive/SpacePlanningZonesAutoPlace/src/SpacePlanningZones.cs) отправляет выбор назначения зон на `ah-sand.api.hypar.io/optimize`; этой части в открытом коде нет. [SpacePlanning](https://github.com/hypar-io/Function-SpacePlanning/blob/f802a505cd7f/src/SpacePlanning.cs) и [Circulation](https://github.com/hypar-io/function-Circulation/blob/4f35c301e1f3/src/Circulation.cs) работают с заданными зонами и проходами.

## Как довести результат до Rhino и Revit

- **Rhino:** EBA возвращает кривые через Grasshopper-адаптер при запущенном локальном сервере. Hypergraph работает в Rhino напрямую. Habx, Co-Layout, HypergraphFormer, ibuilder и Forma floorplate-generator возвращают свои структуры данных — нужен перевод полигонов и типов помещений в слои и кривые.
- **ArchiCAD:** FloorPlan6 уже выводит результат через Tapir (`bridge/`).
- **Revit через Grasshopper:** [Rhino.Inside.Revit](https://github.com/mcneel/rhino.inside-revit) (MIT) создаёт элементы Revit из геометрии GH. Сопоставить полигоны квартир, комнат и стен с категориями, уровнями и типами семейств придётся нашему модулю.
- **Dynamo внутри Revit:** Refinery Toolkits даёт узел упаковки; стены, помещения и параметры квартир создаёт отдельный граф.
- **IFC:** [IFC-GPT `apartment_unit.py`](https://github.com/ngyathin16/ifc-gpt2.0/blob/f781ae94b3f3/building_blocks/assemblies/apartment_unit.py) показывает запись стен, двери, окон и помещения в IFC; план квартиры в нём жёстко задан. [pyRevit-мост ibuilder](https://github.com/ibuilder/massing/blob/523e5b3a120b/integrations/pyrevit/README.md) работает только в сторону **из Revit**.

Среди проверенных репозиториев нет готовой связки «задать квартирографию → получить проверенный жилой этаж → создать нативные стены и помещения Revit». Первую половину ближе всего закрывают EBA и Forma floorplate-generator, вторую — наш адаптер через Rhino.Inside.Revit.

## Проверка и следующий шаг

Тесты EBA на Windows: **247 из 248 прошли**; единственный сбой — сравнение окончаний строк в JS-файле интерфейса, к генератору не относится. Остальные проекты изучены по коду, на наших этажах не запускались. Коммерческие сервисы проверены только по открытым источникам, без пробных запусков.

Для первого опыта достаточно 2–3 реальных контуров с ядром, входами, колоннами и нужными площадями:

1. **Этаж:** прогнать EBA и перенести алгоритм крыльев из Forma floorplate-generator; сравнить с упаковкой Refinery Toolkits и ibuilder по числу квартир каждого типа, площадям, потерям, входам и времени.
2. **Квартира:** сравнить три подхода — CP-SAT (FloorPlan6 как образец модели, свой код из-за AGPL), перенос по образцу (Hypergraph) и Вороной (nobuyuki83) для неправильных контуров.
3. **Выпуск:** выбранный вариант передать в Revit через Rhino.Inside.Revit и проверить элементы и параметры.
