# Development Directions And External Repo Fit

Дата: 2026-05-28

Цель: разложить полезные фрагменты внешних репозиториев StepanKukharskiy по трем нашим направлениям разработки. Одна и та же библиотека не одинаково полезна везде: для reference-to-model нужен intake из изображений и semantic planning, для Rhino cleanup важнее validation/readback, для massing нужны параметры, варианты и быстрые правки.

## Summary Matrix

| External piece | Scenario 1: reference to model | Scenario 2: complex Rhino -> analysis geometry | Scenario 3: massing from TEPs/revisions |
| --- | --- | --- | --- |
| `live-obj` metadata | High | Medium | High |
| `live-obj` decomposed planner | High | Medium | High |
| `live-obj` raw post-op validation | Medium | Low/Medium | Medium |
| `live-obj` Rhino/GH renderer | Medium | Low/Medium | Medium |
| `live-obj` CadQuery/executor vocabulary | Medium | Low | Medium |
| `live-obj` surgical patching | Medium | Low/Medium | High |
| `2DPlanTo3D` contour tracer | High | Low | Medium |
| `spellshape-three` expression/distribution | Medium | Low | High |
| `spellshape-format` `.spell` ideas | Medium | Low | Medium |
| `spellshape-webapp` / `spellshape-agent` | Low | Low | Low |

## Scenario 1 - Reference To Model

Scenario 1 starts from images, plans, elevations, drawings, generated references and text. It needs help turning messy visual inputs into a controlled CAD route.

First gate: identify the constructive grammar before building geometry. For a
tower, this may be "four repeated square shafts around a cross" rather than
"one outer envelope". If the grammar cannot be proven from the supplied views,
request more views before modeling. See `docs/scenarios/reference-modeling-gates.md`.

Most useful pieces:

1. `2DPlanTo3D / contour-tracer.js`
   - Role: plan/image -> contour -> profile.
   - Best use: extract building footprint, podium outline, site boundary, simple elevation silhouette.
   - Pipeline fit:

```text
source image / plan
-> contour extraction
-> footprint/profile candidate
-> semantic part with source authority
-> Rhino/build123d blockout
-> plan/elevation validation
```

2. `live-obj` metadata and planner
   - Role: preserve named parts, bbox, anchors, params and controls between interpretation and CAD.
   - Best use: avoid one-shot model generation; force a part table first.
   - Already integrated in our repo as `import-semantic-obj`, `semantic_parts.json`, `semantic_plan.json`, `semantic_validation.md`.

3. `live-obj` prompt/generation budget rules
   - Role: keep first pass modular and compact.
   - Best use: model massing/proportions first, keep facade grids as guides, avoid dense window-by-window geometry before blockout approval.

4. `spellshape-three` expression/distribution ideas
   - Role: repeat floor modules, facade bays, columns, panels.
   - Best use: after blockout is accepted, not during first source extraction.

Do not prioritize:

- `spellshape-webapp` UI.
- `spellshape-agent` API dependency.
- raw mesh smoothing/subdivision as acceptance logic.

Recommended next implementation for Scenario 1:

```text
import-plan-contour
-> reports/contours.json
-> reports/contours.md
-> optional semantic footprint part
```

## Scenario 2 - Complex Rhino Model To Simplified Analysis Geometry

Scenario 2 starts from an existing Rhino source model. The primary problem is not text generation; it is source understanding, simplification, and validation.

Most useful pieces:

1. `live-obj` metadata as an internal interchange layer
   - Role: name classified parts and preserve bbox/anchors/locks after Rhino scan.
   - Best use: store part intent after `scan_scene` and `classify-scan`, not replace Rhino readback.

2. Decomposed planner
   - Role: order reconstruction by architectural part.
   - Best use:

```text
tower envelope
-> podium/base
-> low blocks
-> supports
-> major bands
-> analysis-relevant facade proxy
```

3. Surgical patching
   - Role: apply small parameter/metadata fixes without rewriting case state.
   - Best use: correct one bbox, one lock, one part label, one validation hint.

4. Raw post-op validation
   - Role: prevent invented operations from entering scripts.
   - Best use: useful as a guardrail if semantic metadata includes `#@post`, but not central.

Low usefulness:

- `2DPlanTo3D` contour extraction. Scenario 2 already has 3D source geometry; contours may help only for diagnostic section silhouettes.
- `spellshape-three` expression/distribution. It is not the core of analysis geometry cleanup.
- Live OBJ mesh executor. It is mesh/preview oriented and should not replace source-derived Rhino/Brep validation.

Recommended next implementation for Scenario 2:

```text
scan_scene/classify-scan
-> semantic part map with locks/anchors
-> section extraction per part
-> candidate/source delta validation
```

## Scenario 3 - Massing From TEPs And Revisions

Scenario 3 is the best match for the generative parts of the Spellshape ecosystem. It needs fast variants, parameters, controls, metrics and iterative revisions.

Most useful pieces:

1. `live-obj` decomposed planner
   - Role: generate a clear build queue for massing variants.
   - Best use: divide site, podium, tower volumes, cores, setbacks, terraces, facade guide grids.

2. `#@params`, `#@controls`, `#@bbox`, `#@anchor`, `#@lock`
   - Role: make variants editable and reviewable.
   - Best use: floor count, floor height, podium footprint, tower width/depth, setbacks, rotation, entrance positions.

3. `spellshape-three` expression/distribution
   - Role: formulas and repeated modules.
   - Best use:

```text
total_height = floors * floor_height
gfa_proxy = footprint_area * floors
facade_bays = bay_count_x * bay_count_y
```

4. Surgical patching
   - Role: revisions as exact parameter deltas.
   - Best use:

```text
"increase tower to 28 floors"
"move entrance to south edge"
"reduce podium depth by 6m"
```

5. Raw post-op vocabulary
   - Role: safe small transforms and arrays.
   - Best use: array floors/bays, mirror entrances, snap masses to ground, center origin.

Medium usefulness:

- `2DPlanTo3D` contour tracer, when the starting point is a sketch/site image rather than numeric TEP.
- Rhino/GH renderer, for quick review controls and captures.

Recommended next implementation for Scenario 3:

```text
generate-massing-variants
-> params.json variants
-> semantic_plan.json
-> Rhino preview scripts
-> metrics table
-> revision_log.md
```

## Priority By Direction

### If working on Scenario 1 next

Implement:

1. `import-plan-contour` from the `2DPlanTo3D` idea.
2. Source authority table for plan/elevation/image inputs.
3. Semantic footprint/profile parts.
4. Blockout validation against plan/elevation proportions.

### If working on Scenario 2 next

Implement:

1. Rhino `scan_scene` integration.
2. Part-aware semantic map from scan/classification.
3. Section extraction normalization.
4. Candidate/source validation.

Use external repo pieces only as support. Do not let Live OBJ mesh generation become the Scenario 2 core.

### If working on Scenario 3 next

Implement:

1. `generate-variants`.
2. Safe expression evaluator for a tiny formula subset.
3. Param/control-driven massing parts.
4. Surgical revision patching.
5. Metrics and comparison captures.

## Decision

The external repositories should not be adopted as one dependency. Use them as a parts library:

- `2DPlanTo3D` mainly feeds Scenario 1.
- `live-obj` metadata/planner feeds Scenario 1 and Scenario 3, and lightly supports Scenario 2.
- `spellshape-three` distribution/expression ideas mainly feed Scenario 3.
- Standard RhinoMCP remains the authority for Scenario 2.
- `text-to-cad` / build123d remains the authority for STEP-first precise CAD.
