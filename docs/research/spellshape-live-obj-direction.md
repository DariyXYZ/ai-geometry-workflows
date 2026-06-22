# Spellshape / Live OBJ direction

Дата: 2026-05-28  
Статус: исследовать как upstream semantic layer, не как замену CAD-backend.

## Что изучено

Основной актуальный источник:

- https://spellshape.com/
- https://github.com/StepanKukharskiy/live-obj

Связанные источники:

- https://github.com/StepanKukharskiy/spellshape
- https://github.com/StepanKukharskiy/spellshape-format
- https://github.com/StepanKukharskiy/spellshape-webapp
- https://github.com/StepanKukharskiy/spellshape-three
- https://github.com/StepanKukharskiy/spellshape-agent
- https://github.com/StepanKukharskiy/2DPlanTo3D

Текущий сайт Spellshape описывает продукт как tool for the messy stage before
CAD. Самый актуальный technical direction лежит в `live-obj`: обычный OBJ
расширяется `#@` metadata comments.

## Что такое Live OBJ

Live OBJ = portable OBJ mesh + semantic metadata in comments.

Обычные 3D-приложения читают `v/f` geometry как обычный OBJ. Spellshape-aware
tools читают `#@` metadata как editable source of truth.

Типовые metadata:

- `#@scene`
- `#@units`
- `#@up`
- `#@source: procedural | llm_mesh | assembly | sdf | simulation`
- `#@params`
- `#@controls`
- `#@bbox`
- `#@anchor`
- `#@lock`
- `#@constraint`
- `#@post`
- `#@ops`
- `#@material_preset`

Главный паттерн:

```text
mesh preview stays portable
metadata carries design intent
executor can regenerate or post-process geometry
```

## Как это ложится на наш txt-to-cad

Текущая граница проекта:

- RhinoMCP: scan, scene context, overlays, classification, sections, review captures.
- `text-to-cad` / build123d: STEP-first parametric CAD candidates.
- `ai_geometry_toolkit`: case folders, manifests, routes, reports, backend registration.

Spellshape / Live OBJ можно добавить как промежуточный semantic sketch layer:

```text
prompt / reference / intent
-> semantic OBJ / Live OBJ sketch
-> normalized part table
-> build123d / Rhino script
-> STEP / 3DM candidate
-> source-derived validation
```

Это особенно полезно для Scenario 1 и Scenario 3:

- разложить prompt на named parts;
- сохранить rough geometry preview;
- вытащить bbox, anchors, controls, constraints;
- не терять semantic intent между LLM output и CAD build stage.

## Что не переносим

Не принимаем Spellshape как финальный CAD pipeline.

Причины:

- Live OBJ остается mesh-friendly format, а не STEP-first B-rep format.
- CADQuery hooks в `live-obj` есть, но основной artifact все равно OBJ/cache.
- Схемы экспериментальные, без production stability.
- `.spell` направление выглядит более ранним/параллельным, а не текущим главным
  runtime для сайта.

## Что переносим как идею

1. `semantic_obj` как наш собственный промежуточный формат.
2. `#@params` / `#@controls` для LLM-generated editable knobs.
3. `#@bbox` / `#@anchor` / `#@lock` / `#@constraint` для последующей CAD-реконструкции.
4. Decomposed generation: сначала part plan, потом one part per step.
5. Разделение raw mesh post-processing и precise procedural regeneration.

## Возможный MVP

Новый route/backend name:

```text
semantic_obj
```

Минимальный эксперимент:

1. Сгенерировать или вручную написать маленький `.live.obj`.
2. Парсер читает `#@` metadata и обычные OBJ object names.
3. На выходе пишет:
   - `reports/semantic_parts.json`
   - `reports/semantic_parts.md`
4. Следующий шаг переводит part table в build123d или Rhino Python script.
5. CAD candidate проходит существующий validation route.

Минимальная структура `semantic_parts.json`:

```json
{
  "source": "live_obj",
  "parts": [
    {
      "id": "tower_main",
      "source": "procedural",
      "semantic": "main tower mass",
      "bbox": [[0, 0, 0], [20, 30, 120]],
      "params": {
        "height": 120,
        "width": 20,
        "depth": 30
      },
      "anchors": [],
      "controls": []
    }
  ]
}
```

## Acceptance

Направление считается полезным, если Live OBJ metadata:

- улучшает part/control extraction;
- не ослабляет STEP-first validation;
- помогает Scenario 1/3 быстрее дойти от prompt/reference до проверяемого CAD script;
- не превращает проект в еще один нерегулируемый mesh generator.

## Решение

Зафиксировать Spellshape / Live OBJ как source и research direction.

Не внедрять сейчас UI или API Spellshape. Следующий практический шаг - маленький
локальный importer `semantic_obj` внутри `ai_geometry_toolkit`.
