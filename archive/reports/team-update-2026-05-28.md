# Team Update: AI Geometry / txt-to-cad direction cleanup

Date: 2026-05-28  
Repo: `DariyXYZ/ai-geometry-workflows`

## Short Version

The repository direction is now split into clear layers:

```text
Rhino/Aurox readback
-> semantic sketch / Live OBJ research
-> build123d/text-to-cad CAD backend
-> validation-first case orchestration
```

Spellshape / Live OBJ is now documented as a source for the semantic sketch
layer, not as a replacement for our CAD backend.

## What Was Added

New direction document:

- `docs/research/spellshape-live-obj-direction.md`

Updated organizing docs:

- `README.md`
- `NEWS.md`
- `docs/development-state.md`
- `docs/project-data-map.md`
- `archive/reports/ai-geometry-workplan.md`

## Spellshape / Live OBJ Decision

Source:

- https://spellshape.com/
- https://github.com/StepanKukharskiy/live-obj

What we take:

- OBJ as portable preview geometry;
- `#@` metadata for parts, params, controls, bbox, anchors, locks and constraints;
- decomposed generation: plan parts first, then generate one part at a time;
- importer path from semantic metadata into deterministic CAD scripts.

What we do not take:

- no dependency on Spellshape UI/API;
- no acceptance of mesh OBJ as final CAD;
- no replacement of STEP-first `text-to-cad` / build123d path.

## Current Architecture

Rhino/Aurox owns source readback and scene evidence.

`semantic_obj` / Live OBJ-like importer should own:

```text
rough preview mesh + semantic metadata -> normalized part table
```

`text-to-cad` / build123d owns:

```text
normalized parameters -> STEP-first CAD candidate
```

`ai_geometry_toolkit` owns:

```text
case folder -> route -> reports -> validation
```

## Next Work

1. Keep Scenario 2 active: migrate scan/section tools and build
   `v4_refined_clean_massing`.
2. Add a tiny `semantic_obj` experiment:
   - input: `.live.obj`;
   - output: `reports/semantic_parts.json` and `.md`;
   - no final geometry acceptance without CAD validation.
3. Keep `NEWS.md` in Russian as the main chronological project log.

