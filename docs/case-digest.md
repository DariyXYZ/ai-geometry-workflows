# Case Digest

This is the one-minute case memory for an AI agent. Read this before opening
detailed case notes when the task resembles previous Rhino, massing,
Grasshopper, or cleanup work.

For full routing, use `docs/case-library.md`. For full case notes, open only the
linked file that matches the current task.

## Current Standards

| Standard | Use for | Source |
| --- | --- | --- |
| Source authority before geometry | Any reference/modeling task | `docs/scenarios/reference-modeling-gates.md`, `docs/cases/recent-rhino-case-lessons.md` |
| Scenario 3 subtype first | Any massing/TEP/checklist task | `docs/scenarios/tep-massing-scenario-subtypes.md` |
| Site zoning before form | Plot-plus-entries massing | `docs/libraries/moscow-bc-site-zoning-patterns.md` |
| Numeric pass is not design acceptance | Moscow BC / Scenario 3 | `docs/errors/moscow-bc-massing-error-library.md` |
| McNeel RhinoMCP is default | Rhino work | `docs/tools/rhino-mcp-backends.md` |
| `MCPStart`, not `MCPConnect` | RhinoMCP slot startup | `docs/errors/grasshopper-mcp-error-library.md` |
| Store GH C# bodies in repo | Grasshopper script logic | `docs/tools/grasshopper-csharp-script-nodes.md` |
| Promote experience by type | Any useful session | `docs/experience-capture-format.md` |

## Wins To Reuse

| Win | Reusable move | Read |
| --- | --- | --- |
| BC50 two-tower stylobate | Contour-derived roofs/parapets, straight core overruns, translucent massing glass, 1 mm visual lift, metric board | `docs/cases/bc50-two-tower-stylobate-2026-06-24.md` |
| Grove at Grand Bay correction | Use authoritative control sections -> temporary loft -> Rhino Contour -> final slabs; contour is slab edge, not glass line | `decisions/2026-06-01-grove-contour-derived-floor-plates.md` |
| Aqua Tower replay | Floor-by-floor wavy slabs plus grounded base can be a strong video demonstrator | `docs/cases/recent-rhino-case-lessons.md` |
| Absolute World replay | Repeated rotated elliptical rings plus guide lines communicate tower twist cleanly | `docs/cases/recent-rhino-case-lessons.md` |
| Grasshopper voxel tower | Controlled architectural mask plus Pufferfish `Voxel Mesh`, not random `Populate 3D` | `docs/cases/grasshopper-voxel-skyscraper-2026-06-22.md` |
| Grasshopper architecture snippets | RhinoCommon smoke for massing -> floors -> core -> TEP metrics | `docs/cases/grasshopper-architecture-snippets-smoke-2026-06-23.md` |

## Failure Gates

| Failure | Gate to apply | Read |
| --- | --- | --- |
| Generic envelope guessed from one view | Identify constructive grammar and source authority first | `docs/scenarios/reference-modeling-gates.md` |
| User Rhino curves replaced by generic sections | Use visible user curves as source authority | `decisions/2026-06-01-infinity-tower-user-rhino-curves-source-authority.md` |
| Shanghai-style twist became organic blob | Build soft triangle minus square/diamond cutter; cutter must drive the final cut | `decisions/2026-06-01-shanghai-tower-square-cutter-source-grammar.md` |
| Shell got detailed before accepted | Shell/support/plan fit first; glass/posts later | `decisions/2026-06-01-flock-chapel-shell-medium-success.md` |
| Fixed-envelope tower accidentally tapered | Keep every plan type inside the same bbox; validate Z bands | `docs/cases/recent-rhino-case-lessons.md` |
| BC variants passed numbers but failed site | Reserve public spine/service edge/open-space logic before building volumes | `docs/errors/moscow-bc-massing-error-library.md` |
| Accidental intersections called stylobate | Declare true podium, separate blocks, or gate/bridge condition | `docs/errors/moscow-bc-massing-error-library.md` |
| Mesh cleanup accepted only because closed | Validate parts, bbox, sections, views, and source fidelity | `docs/error-ledger.md` |
| GH C# source injection crashed Rhino | Never call `SourceCodeChanged(None)`; paste or use proven bridge | `docs/errors/grasshopper-mcp-error-library.md` |

## Techniques And Patterns

| Technique | When useful | Source |
| --- | --- | --- |
| Contour-derived roof/parapet rings | Non-rectangular tower or stylobate roofs | `docs/cases/bc50-two-tower-stylobate-2026-06-24.md` |
| Visual lift `0.001 m` | Thin finishes over coplanar surfaces | `docs/errors/moscow-bc-massing-error-library.md` |
| Public spine + service edge | Scenario 3B site skeletons | `docs/libraries/moscow-bc-site-zoning-patterns.md` |
| Explicit massing operator | Any Scenario 3 variant | `docs/libraries/form-operator-library.md` |
| Vertical guide/profile loft | Karlatornet-like repeated shaft twist | `decisions/2026-06-01-karlatornet-vertical-section-loft-workflow.md` |
| Source contour transformation | Infinity Tower-like exact section rotation | `decisions/2026-06-01-infinity-tower-user-rhino-curves-source-authority.md` |
| C# Script as repo artifact | GH logic with loops/parity/tangent frames | `docs/cases/grasshopper-pavilion-80hz-lamella-attractor-2026-06-26.md` |

## Metrics And Defaults

| Metric/default | Use for | Source |
| --- | --- | --- |
| Moscow building dimensions | Floors, cores, depths, slabs, roofs, facade modules | `docs/libraries/moscow-building-dimensional-library-2026.md` |
| Moscow road dimensions | Lanes, driveways, fire access, road modeling | `docs/libraries/moscow-road-dimensional-library-2026.md` |
| Moscow architecture checklist | 3D approval review, evidence, scoring | `docs/libraries/moscow-architecture-approval-checklist.md` |
| BC50 validation snapshot | Two 50-floor office towers on stylobate | `docs/cases/bc50-two-tower-stylobate-2026-06-24.md` |
| Pavilion 80hz defaults | Lamella count, rows, shingle dimensions, top beam | `docs/cases/grasshopper-pavilion-80hz-lamella-attractor-2026-06-26.md` |

## If You Only Have Time For Three Files

For massing/revision work:

```text
docs/task-read-maps.md
docs/case-digest.md
docs/scenarios/tep-massing-scenario-subtypes.md
```

For reference-to-model work:

```text
docs/task-read-maps.md
docs/case-digest.md
docs/scenarios/reference-modeling-gates.md
```

For Grasshopper automation:

```text
docs/task-read-maps.md
docs/case-digest.md
docs/tools/grasshopper-workflow.md
```

