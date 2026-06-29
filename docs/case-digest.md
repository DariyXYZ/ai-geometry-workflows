# Case Digest

This is the one-minute case memory for an AI agent. Read this before opening
detailed case notes when the task resembles previous Rhino, massing,
Grasshopper, or cleanup work.

For full routing, use `docs/case-library.md`. For full case notes, open only the
linked file that matches the current task.

When opening a case file, read the `AI Extraction Summary` block first and stop
there unless the current task matches the case grammar, tool route, or failure
gate.

Keep two case branches separate:

- direct Rhino geometry cases: reference modeling, massing, cleanup, .3dm scene
  construction, RhinoCommon generators;
- Grasshopper cases: GH graphs, C# Script components, sliders, plugins,
  RhinoMCP `g1_*`, and source-injection/tooling failures.

For Grasshopper work, open `docs/cases/grasshopper/README.md`. For direct
Rhino geometry work, skip that branch unless GH implementation is explicitly
requested.

## Current Standards

| Standard | Use for | Source |
| --- | --- | --- |
| Source authority before geometry | Any reference/modeling task | `docs/workflows/rhino-reference/reference-modeling-gates.md`, `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` |
| Scenario 3 subtype first | Any massing/TEP/checklist task | `docs/workflows/massing/tep-massing-scenario-subtypes.md` |
| Site zoning before form | Plot-plus-entries massing | `docs/libraries/massing/moscow-bc-site-zoning-patterns.md` |
| Numeric pass is not design acceptance | Moscow BC / Scenario 3 | `docs/errors/massing/moscow-bc-massing-error-library.md` |
| Review labels on ground | Visible massing labels | `docs/errors/massing/moscow-bc-massing-error-library.md`, `docs/cases/rhino-geometry/moscow-river-bc-two-footprints-2026-06-29.md` |
| McNeel RhinoMCP is default | Rhino work | `docs/tools/rhino/rhino-mcp-backends.md` |
| `MCPStart`, not `MCPConnect` | RhinoMCP slot startup | `docs/errors/grasshopper/grasshopper-mcp-error-library.md` |
| Store GH C# bodies in repo | Grasshopper script logic | `docs/tools/grasshopper/grasshopper-csharp-script-nodes.md` |
| Separate GH cases from Rhino geometry | Case routing | `docs/cases/grasshopper/README.md` |
| Promote experience by type | Any useful session | `docs/experience-capture-format.md` |

## Wins To Reuse

| Win | Reusable move | Read |
| --- | --- | --- |
| BC50 two-tower stylobate | Contour-derived roofs/parapets, straight core overruns, translucent massing glass, 1 mm visual lift, metric board | `docs/cases/rhino-geometry/bc50-two-tower-stylobate-2026-06-24.md` |
| Moscow river BC V02 | On approved river-edge footprints, use hidden core guides, clean final visibility, recessed transfer shoulders, a supported tower-on-stylobate transition, and a connector deck between tower and lower block | `docs/cases/rhino-geometry/moscow-river-bc-two-footprints-2026-06-29.md` |
| Moscow river BC user-remodeled V03 | For paired rounded BC towers, use shadow reveals above stylobate, a monolithic two-story cut-through connector, and river-facing sloped sides that converge into one upward silhouette | `docs/cases/rhino-geometry/moscow-river-bc-two-footprints-2026-06-29.md` |
| Residential OKN complex | Fixed ЖК footprints plus low public OKN block; use height stepping/top setbacks and keep OKN plaza legible | `docs/cases/rhino-geometry/residential-okn-three-block-massing-2026-06-26.md` |
| Grove at Grand Bay correction | Use authoritative control sections -> temporary loft -> Rhino Contour -> final slabs; contour is slab edge, not glass line | `decisions/2026-06-01-grove-contour-derived-floor-plates.md` |
| Aqua Tower replay | Floor-by-floor wavy slabs plus grounded base can be a strong video demonstrator | `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` |
| Absolute World replay | Repeated rotated elliptical rings plus guide lines communicate tower twist cleanly | `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` |
| Grasshopper voxel tower | Controlled architectural mask plus Pufferfish `Voxel Mesh`, not random `Populate 3D` | `docs/cases/grasshopper/grasshopper-voxel-skyscraper-2026-06-22.md` |
| Grasshopper architecture snippets | RhinoCommon smoke for massing -> floors -> core -> TEP metrics | `docs/cases/grasshopper/grasshopper-architecture-snippets-smoke-2026-06-23.md` |

## Failure Gates

| Failure | Gate to apply | Read |
| --- | --- | --- |
| Generic envelope guessed from one view | Identify constructive grammar and source authority first | `docs/workflows/rhino-reference/reference-modeling-gates.md` |
| User Rhino curves replaced by generic sections | Use visible user curves as source authority | `decisions/2026-06-01-infinity-tower-user-rhino-curves-source-authority.md` |
| Shanghai-style twist became organic blob | Build soft triangle minus square/diamond cutter; cutter must drive the final cut | `decisions/2026-06-01-shanghai-tower-square-cutter-source-grammar.md` |
| Shell got detailed before accepted | Shell/support/plan fit first; glass/posts later | `decisions/2026-06-01-flock-chapel-shell-medium-success.md` |
| Fixed-envelope tower accidentally tapered | Keep every plan type inside the same bbox; validate Z bands | `docs/cases/rhino-geometry/recent-rhino-case-lessons.md` |
| BC variants passed numbers but failed site | Reserve public spine/service edge/open-space logic before building volumes | `docs/errors/massing/moscow-bc-massing-error-library.md` |
| BC massing shows 3D core/helper junk | Keep cores as hidden 2D guides unless requested, then hide all helper/source/debug layers before final review | `docs/errors/massing/moscow-bc-massing-error-library.md`, `docs/cases/rhino-geometry/moscow-river-bc-two-footprints-2026-06-29.md` |
| Review text is hard to read | Hide long metric boards; if a label is needed, place a compact horizontal ground label in XY outside the footprint | `docs/errors/massing/moscow-bc-massing-error-library.md`, `docs/cases/rhino-geometry/moscow-river-bc-two-footprints-2026-06-29.md` |
| Connector reads like a black coffin | Make the link part of a monolithic stylobate/transfer volume with a cut-through; add shadow reveals under rounded towers | `docs/errors/massing/moscow-bc-massing-error-library.md`, `docs/cases/rhino-geometry/moscow-river-bc-two-footprints-2026-06-29.md` |
| Accidental intersections called stylobate | Declare true podium, separate blocks, or gate/bridge condition | `docs/errors/massing/moscow-bc-massing-error-library.md` |
| Mesh cleanup accepted only because closed | Validate parts, bbox, sections, views, and source fidelity | `docs/error-ledger.md` |
| GH C# source injection crashed Rhino | Never call `SourceCodeChanged(None)`; paste or use proven bridge | `docs/errors/grasshopper/grasshopper-mcp-error-library.md` |

## Techniques And Patterns

| Technique | When useful | Source |
| --- | --- | --- |
| Contour-derived roof/parapet rings | Non-rectangular tower or stylobate roofs | `docs/cases/rhino-geometry/bc50-two-tower-stylobate-2026-06-24.md` |
| Visual lift `0.001 m` | Thin finishes over coplanar surfaces | `docs/errors/massing/moscow-bc-massing-error-library.md` |
| Public spine + service edge | Scenario 3B site skeletons | `docs/libraries/massing/moscow-bc-site-zoning-patterns.md` |
| Explicit massing operator | Any Scenario 3 variant | `docs/libraries/massing/form-operator-library.md` |
| Vertical guide/profile loft | Karlatornet-like repeated shaft twist | `decisions/2026-06-01-karlatornet-vertical-section-loft-workflow.md` |
| Source contour transformation | Infinity Tower-like exact section rotation | `decisions/2026-06-01-infinity-tower-user-rhino-curves-source-authority.md` |
| C# Script as repo artifact | GH logic with loops/parity/tangent frames | `docs/cases/grasshopper/grasshopper-pavilion-80hz-lamella-attractor-2026-06-26.md` |

## Metrics And Defaults

| Metric/default | Use for | Source |
| --- | --- | --- |
| Moscow building dimensions | Floors, cores, depths, slabs, roofs, facade modules | `docs/libraries/standards/moscow-building-dimensional-library-2026.md` |
| Moscow road dimensions | Lanes, driveways, fire access, road modeling | `docs/libraries/standards/moscow-road-dimensional-library-2026.md` |
| Moscow architecture checklist | 3D approval review, evidence, scoring | `docs/libraries/standards/moscow-architecture-approval-checklist.md` |
| BC50 validation snapshot | Two 50-floor office towers on stylobate | `docs/cases/rhino-geometry/bc50-two-tower-stylobate-2026-06-24.md` |
| Pavilion 80hz defaults | Lamella count, rows, shingle dimensions, top beam | `docs/cases/grasshopper/grasshopper-pavilion-80hz-lamella-attractor-2026-06-26.md` |

## If You Only Have Time For Three Files

For massing/revision work:

```text
docs/task-read-maps.md
docs/case-digest.md
docs/workflows/massing/tep-massing-scenario-subtypes.md
```

For reference-to-model work:

```text
docs/task-read-maps.md
docs/case-digest.md
docs/workflows/rhino-reference/reference-modeling-gates.md
```

For Grasshopper automation:

```text
docs/task-read-maps.md
docs/case-digest.md
docs/tools/grasshopper/grasshopper-workflow.md
```
