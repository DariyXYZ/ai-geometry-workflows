# Case Library

This file indexes reusable cases. A case is useful when it teaches a workflow,
a validation gate, an architectural grammar, or a failure mode that should
change future behavior.

Use this before starting a similar task. Do not repeat the old experiment just
to rediscover the same lesson.

## Case Status Types

| Status | Meaning |
| --- | --- |
| `accepted` | Good enough to reuse as a workflow precedent |
| `medium-success` | Direction was right, but one or more gates failed |
| `failed` | Result was rejected; promote the mistake to error library |
| `source-correction` | User/source data changed the correct modeling strategy |
| `tooling` | Case taught something about Rhino/Aurox/build123d/CLI workflow |

## Reference-To-Model Cases

| Case | Status | Main lesson | Read |
| --- | --- | --- | --- |
| Grove at Grand Bay | `accepted` workflow correction | Rotating orthogonal floor plates should use control sections -> temporary loft -> Rhino Contour -> final floor contours. Contour is slab edge, not glass line. | `decisions/2026-06-01-grove-contour-derived-floor-plates.md`, `docs/error-ledger.md` |
| Karlatornet | `source-correction` | Do not guess one envelope. Identify repeated shafts, gaps, twist datums, vertical guide/profile curves, and mirror/repeat logic. | `decisions/2026-06-01-karlatornet-vertical-section-loft-workflow.md`, `docs/error-ledger.md` |
| Infinity Tower/SOM | `source-correction` | User-prepared Rhino curves override generic parametric sections. Use exact source contours and twist axis. | `decisions/2026-06-01-infinity-tower-user-rhino-curves-source-authority.md` |
| Shanghai Tower-style twist | `medium-success` | A soft triangular twist with corner cut-out must be built from primitive/cutter logic, not an organic blob or unrelated point list. | `decisions/2026-06-01-shanghai-tower-square-cutter-source-grammar.md`, `docs/error-ledger.md` |
| Flock chapel shell | `medium-success` | Shell direction was right, but supports, plan fit, and secondary elements must wait for shell acceptance. | `decisions/2026-06-01-flock-chapel-shell-medium-success.md` |
| Symmetric stepped residential tower | `failed-to-rule` | Fixed-envelope plan-type changes must not create unintended taper; validate vertical band placement. | `docs/cases/recent-rhino-case-lessons.md`, `docs/error-ledger.md` |

## Complex Model Cleanup Cases

| Case | Status | Main lesson | Read |
| --- | --- | --- | --- |
| Scenario 2 mesh cleanup / `test_data_2.3dm` | `active-baseline` | Closed geometry is not enough. Preserve architectural parts, extract meaningful sections, validate by source-derived dimensions and views. | `docs/development-state.md`, `docs/error-ledger.md` |
| Feature-preserving mesh reconstruction | `decision` | Avoid global decimation/ShrinkWrap as final. Reconstruct by part and preserve source features. | `decisions/2026-05-19-feature-preserving-mesh-reconstruction.md` |
| NURBS restart from named rails | `decision` | When messy mesh cleanup fails, restart from named/meaningful rails and architectural zones. | `decisions/2026-05-20-nurbs-restart-from-named-rails.md` |

## Massing And TEP Cases

| Case | Status | Main lesson | Read |
| --- | --- | --- | --- |
| Moscow BC `AI_BC_V01-V03` | `failed` | Numeric pass is not design acceptance. Low bars cut movement, accidental intersections are not stylobates, box-only variants are rejected. | `docs/errors/moscow-bc-massing-error-library.md`, `docs/libraries/moscow-bc-site-zoning-patterns.md` |
| Moscow BC Scenario 3 split | `strategy` | Classify as `3A` fixed zoning, `3B` plot-plus-entries zoning proposal, or `3C` existing-massing image revision before acting. | `docs/scenarios/tep-massing-scenario-subtypes.md` |
| Rhino pilot massing v2-v4 | `failed-to-rule` | Circulation came too late, gaps became narrow residual slots, red-line discipline failed, and heavy blocks ignored light/open-space logic. | `docs/obsidian-knowledge-map.md`, `docs/errors/moscow-bc-massing-error-library.md` |
| Rhino test massing v5-v8 | `medium-success` | The strongest direction was compact central podium plus a separated dynamic tower and landscape field; avoid random wide podiums and leftover pavilions. | `docs/obsidian-knowledge-map.md`, `docs/libraries/massing-decision-library.md` |

## Video / Replay / Demonstrator Cases

| Case | Status | Main lesson | Read |
| --- | --- | --- | --- |
| Aqua Tower / Studio Gang video demonstrator | `tooling` | Preserve camera, slow construction down, keep model grounded, and remove obsolete helper geometry. | `docs/cases/recent-rhino-case-lessons.md` |
| Absolute World Towers video demonstrator | `tooling` | Same replay discipline: staged visible construction and clean final state. | `docs/cases/recent-rhino-case-lessons.md` |

## Case Entry Template

Use this when adding a new case:

```markdown
## Case Name

Status:

Scenario:

Source / file:

Goal:

What worked:

What failed:

Promoted rules:

Reusable workflow:

Links:
```

## Promotion Rule

After each meaningful modeling session, decide whether the result should create
or update:

- a case entry here;
- an error in `docs/error-ledger.md` or a domain error library;
- a decision in `decisions/`;
- a strategy or pattern library entry;
- a source-repo card.

If nothing reusable was learned, do not add noise.
