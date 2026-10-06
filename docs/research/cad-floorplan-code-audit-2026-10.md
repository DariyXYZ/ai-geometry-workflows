# Кодовые базы алгоритмов планировок: аудит исходников

Проверено: 2026-10-06. Фокус: **где лежит настоящий алгоритм**, что он принимает и возвращает, насколько близок к типовым офисным этажам Rhino/Revit. Это исправляет приоритеты [первого обзора](cad-floorplan-generation-2026-10.md): рынок и лицензии остаются в нём, здесь главное — код. Исходники просмотрены в указанных коммитах; результат для наших этажей ещё не измерен.

## Выбор базы

**Для первого рабочего генератора офисного этажа взять за отправную точку [Magnetizing Floor Plan Generator](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/tree/9faf7d92a87e).** Это C# Grasshopper-плагин, который действительно строит комнаты и коридоры по контуру, площадям и графу соседств. Важно вынести ядро из большого `GH_Component`, добавить фиксированные колонны/ядро и отдельный валидатор. Для офисной расстановки и деления private/open office взять проверенные идеи/компоненты [HyparSpace](https://github.com/hypar-io/HyparSpace/tree/f277d1b9151b). Если нужен серверный JSON-движок, архитектурно сильнейший кандидат — [floor-plan-generation-engine](https://github.com/BhaveshY/floor-plan-generation-engine/tree/83cbb65e508f), но его генерацию квартир придётся заменить офисной типологией.

## Ранжирование именно исходников

| Место | Кодовая база | Алгоритм в коде | Подходит для | Главная доработка |
| --- | --- | --- | --- | --- |
| **1** | [Magnetizing](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/MagnetizingRooms_ES.cs) | Дискретная сетка; комнаты растут по площадям/пропорциям; следующая комната выбирается по соседствам с уже размещёнными; к комнатам добавляются одно-, двух- или четырёхсторонние полосы коридора; несколько лучших решений частично разбираются и перестраиваются | Общие помещения/общественные здания; прямой вывод кривых в GH/Rhino | Вынести solver из монолитного компонента, закрепить ядро/шахты/колонны, проверить связность коридоров/дверей и качество на реальном этаже |
| **2** | [HyparSpace](https://github.com/hypar-io/HyparSpace/tree/f277d1b9151b/LayoutFunctions) | Геометрия и типовые правила **уже выделенных офисных зон**: private office subdivision, сетка столов, мебель переговорных, избегание колонн; отдельно граф путей и расстояний | Офисный fit-out **после** разбиения этажа на зоны | Перевести `Elements`/Hypar объекты в наш контракт; составить собственный генератор зон и программу помещений |
| **3** | [EBA floor-plan-generation-engine](https://github.com/BhaveshY/floor-plan-generation-engine/tree/83cbb65e508f/FloorPlanGeneration) | Детерминированные варианты, выбор коридорного spine, полосы квартир, комнаты, двери, topology, жёсткая валидация и ранжирование; JSON I/O | База отдельного C# сервиса + адаптер в GH, особенно если планируется жильё | `UnitMixPlanner`/`DwellingTemplateGenerator` заменить на офисную программу, площади и соседства; офисных паттернов пока нет |
| **4** | [Hypergraph](https://github.com/ramonweber/hypergraph/tree/fe049f1c31fb/ResearchGeometryLibrary/RGeoLib/BuildingSolver) | Поиск похожих планов, перенос разбиения из референса в новую границу, фильтрация по площади/доступу/фасаду, оценка формы и мебель | Вторая ветка для повторяющихся этажей и квартир из библиотеки принятых решений | Адаптировать сущности `Apartment`/`Room` к офисным модулям; собрать библиотеку своих планов |
| **5** | [architect-layout-solver](https://github.com/dashu-baba/architect-layout-solver/tree/3990f3dc5bc3/constraints-resolver/src) | Генерация прямоугольных кандидатов, порядок «сначала самые ограниченные», scoring и рекурсивный backtracking | Малый эталон для геометрически простых комнат | Сейчас граница прямоугольная, нет полноценного ядра и коридорной сети; Rust/WASM требует мост к GH |
| **6** | [floorplan-optimizer](https://github.com/rainon-feroze/floorplan-optimizer/tree/7cf5326332db/floorplan) | DEAP genetic algorithm с genome/decode и штрафами за наложения, границу, соседства, свет, циркуляцию и выход | Референс функции качества и разнообразия вариантов | Жилые комнаты; «путь до выхода» в коде — расстояние между центрами, не реальный маршрут; не использовать как готовую проверку |
| **7** | [archit-app](https://github.com/archit-app/archit-app/tree/e2913370845b/archit_app/analysis) | Топология, поиск комнат, анализ циркуляции, площади/света/доступности, DXF/GeoJSON | Независимая проверка и экспорт результатов | Библиотека анализа; готового генератора офисных вариантов не найдено |

## Точные точки входа для разработчика

### 1. Magnetizing: наиболее прямой генератор

- [Основной цикл и `TryPlaceNewRoomToTheGrid`](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/MagnetizingRooms_ES.cs): входы `HouseInstance`/`RoomInstance`, контур и размер ячейки; перебор порядка комнат и частичная пересборка лучших решений; выход — room/corridor Breps и имена.
- [Структура комнаты и связей](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/RoomProgram/RoomInstance.cs) и [вход GH](https://github.com/hellguz/Magnetizing_FloorPlanGenerator/blob/9faf7d92a87e/Magnetizing_FPG/RoomProgram/HouseInstance.cs).
- Код гибкий по программе помещений, хотя имена классов `House*`. Первым делом добавить маску неприкосновенных ячеек под ядро/колонны и проверку доступности каждой комнаты от выхода. Исходный solver сосредоточен в одном файле (~1500 строк); отдельного автоматического тестового набора в репозитории не найдено.

### 2. HyparSpace: офисная логика, но solver программы частично внешний

- [Разделение private offices](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/LayoutFunctions/PrivateOfficeLayout/src/PrivateOfficeLayout.cs): `Grid2d`, разбиение зоны по заданному размеру кабинета, варианты с полосой коридора.
- [Open Office Layout](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/LayoutFunctions/OpenOfficeLayout/src/OpenOfficeLayout.cs) и [общие `GetValidGrids`/`LayoutDesksInGrid`](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/LayoutFunctions/LayoutFunctionCommon/LayoutStrategies.cs): ориентация по коридору, сетка столов, ширина проходов, стратегия обхода колонн.
- [TravelDistanceAnalyzer](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/TravelDistanceAnalyzer/src/AdaptiveGridBuilder.cs): построение графа маршрутов по коридорам/выходам — пригодно как образец геометрической проверки.
- [Архивный авторазделитель зон](https://github.com/hypar-io/HyparSpace/blob/f277d1b9151b/ZonePlanningFunctions/Archive/SpacePlanningZonesAutoPlace/src/SpacePlanningZones.cs): генерирует коридорную геометрию и привязку зон к ядру, **но** `AutoLayoutProgram` отправляет задачу «какую программу положить в какую зону» на `https://ah-sand.api.hypar.io/optimize`. Эту часть нельзя считать самодостаточным открытым solver; её придётся реализовать локально. Текущие [Function-SpacePlanning](https://github.com/hypar-io/Function-SpacePlanning/blob/f802a505cd7f/src/SpacePlanning.cs) и [function-Circulation](https://github.com/hypar-io/function-Circulation/blob/4f35c301e1f3/src/Circulation.cs) в первую очередь собирают/обрабатывают заданные пространства и overrides, а не создают полный офисный план без исходной разметки.

### 3. EBA: готовая структура сервиса и валидатора

- [Оркестратор и проверки](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/FloorPlanEngine.cs): input → clean → candidate → validate → score; явные диагностические проверки коридоров, комнат, дверей и слоёв.
- [CandidateGenerator](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Generation/CandidateGenerator.cs): коридор и зоны размещения; [DoorNetworkBuilder](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/FloorPlanGeneration/Topology/DoorNetworkBuilder.cs) — граф дверей; [Grasshopper adapter](https://github.com/BhaveshY/floor-plan-generation-engine/blob/83cbb65e508f/adapters/grasshopper/fp_generate.py) — уже готовый мост HTTP → Rhino curves/layers.
- Локально запущен `dotnet test` на Windows: **247 из 248 тестов прошли**. Единственный сбой — UI regression test сравнивает `\n` с `\r\n` в JS-файле (`WebFrontendRegressionTests`, строка 949); к алгоритму генерации этот сбой не относится. Время генерации и архитектурное качество на наших планах не проверены.

### 4. Дополнительные алгоритмы

- [Hypergraph `Apartment.fitApartment` / `createRoomsWithReferenceAndRot`](https://github.com/ramonweber/hypergraph/blob/fe049f1c31fb/ResearchGeometryLibrary/RGeoLib/BuildingSolver/Apartment.cs): особенно полезно, если есть библиотека утверждённых этажей. Это **retrieval/transfer**, а не генерация с нуля.
- [Rust `solve_layout`](https://github.com/dashu-baba/architect-layout-solver/blob/3990f3dc5bc3/constraints-resolver/src/solver.rs) + [candidate generation](https://github.com/dashu-baba/architect-layout-solver/blob/3990f3dc5bc3/constraints-resolver/src/candidate_generation.rs): компактный учебный backtracking solver с тестами. Не приписывать ему полноценную генерацию коридоров.
- [GA `fitness.py`](https://github.com/rainon-feroze/floorplan-optimizer/blob/7cf5326332db/floorplan/fitness.py) + [цикл эволюции](https://github.com/rainon-feroze/floorplan-optimizer/blob/7cf5326332db/floorplan/ga.py): годится как перечень критериев, но часть критериев пока только proxy. Для офисного этажа использовать лишь после явной проверки дверей/маршрутов.

## Практическая сборка для первого кейса БЦ

1. **Контур/исходники:** Rhino floorplate + ядро, колонны, шахты, входы, фасад, неизменяемые объекты. Не заменять их эвристикой.
2. **План помещений:** зафиксировать типы/диапазоны площадей и граф обязательных соседств. Дискретизировать по сетке для Magnetizing; отдельно хранить исходные координаты для точного вывода.
3. **Зонирование:** вынести алгоритм Magnetizing в отдельный C# сервис/библиотеку; добавить запрещённые ячейки, проходы к выходам, разные стратегии коридоров и seed для вариантов.
4. **Офисный fit-out:** после выбора зон применять HyparSpace-подобные сетки столов, деление кабинетов, переговорные и оценку проходов. Проверять доступность каждой комнаты и не доверять только числу помещённых комнат.
5. **Проверка/вывод:** использовать схему независимого валидатора и диагностики EBA; отдавать JSON + Rhino curves/layers, затем маппить выбранный вариант в Revit через Rhino.Inside.Revit.

**Критерий выбора базы:** если цель — как можно быстрее увидеть полный вариант в Grasshopper, начать с Magnetizing. Если цель — поддерживаемое API с тестами и развитием на офисы и жильё, опереться на EBA как каркас, а сам офисный алгоритм взять из отдельного Magnetizing-подобного модуля. HyparSpace подключать для офисных деталей, потому что весь его авто solver нельзя воспроизвести только из опубликованного кода.
