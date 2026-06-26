# Grasshopper Architecture Plugin Stack

Status: active research library.

Use this file when an AI agent needs to decide which Grasshopper native nodes,
C# Script nodes, RhinoCommon routes, and third-party plugins should solve an
architecture task.

The goal is fast routing:

```text
user request
-> architectural intent
-> source authority
-> smallest reliable GH stack
-> validation gate
-> only then optional plugins / bake / BIM / optimization
```

## Core Rule

Do not start from a plugin menu. Start from the architectural problem.

Default order:

```text
native GH nodes
-> C# Script / RhinoCommon for compact custom geometry
-> small, named plugin chain
-> bake / BIM / cloud / optimization only after preview validation
```

Use plugins when they provide a proven high-level operation. Use C# Script when
the same operation would become a fragile web of wires.

## Official McNeel Stack

| Need | Prefer | Why |
| --- | --- | --- |
| Authoritative API semantics | RhinoCommon API reference | Primary source for geometry classes and document objects. |
| Grasshopper scripting | Essential C# Scripting for Grasshopper | Official C# Script component and RhinoCommon learning path. |
| Sample code | `mcneel/rhino-developer-samples` | Official sample repository for Rhino and Grasshopper developer code. |
| Plugin installation | Rhino Package Manager / Yak | Official discovery and management path for Rhino and GH plugins. |
| Custom package distribution | Yak package guides | Defines `.yak` structure and package sources. |
| BIM handoff to Revit | Rhino.Inside.Revit | Official Rhino/Grasshopper inside Revit workflow. |
| AI agent transport | `mcneel/RhinoMCP` | Default MCP transport in this repo. |

Research links:

- https://developer.rhino3d.com/
- https://developer.rhino3d.com/api
- https://developer.rhino3d.com/guides/grasshopper
- https://developer.rhino3d.com/guides/grasshopper/csharp-essentials/
- https://developer.rhino3d.com/guides/grasshopper/csharp-essentials/3-rhinocommon-geometry/
- https://github.com/mcneel/rhino-developer-samples
- https://www.rhino3d.com/features/package-manager/
- https://developer.rhino3d.com/guides/yak/
- https://developer.rhino3d.com/guides/yak/the-anatomy-of-a-package/
- https://github.com/mcneel/RhinoMCP
- https://github.com/mcneel/rhino.inside-revit
- https://www.rhino3d.com/features/rhino-inside-revit/

## Architecture Plugin Families

| Family | Plugins / tools | Use when | Avoid when |
| --- | --- | --- | --- |
| Climate / solar / daylight | Ladybug, Honeybee, Dragonfly, Butterfly | Request mentions sun, wind, radiation, daylight, energy, comfort, climate response. | Early pure massing with no analysis goal. |
| Physics / form finding | Kangaroo | Shells, hanging/catenary forms, tensile nets, relaxation, constraint solving. | Office massing that needs clean floor plates and TEP first. |
| Structure | Karamba3D | Early structural feedback for beams, shells, trusses, load paths. | No structural question or license not available. |
| Optimization | Wallacei, Octopus, Galapagos, Opossum | Multiple objectives: GFA vs radiation vs view vs structure. | One-off form generation; optimization can hide poor design intent. |
| Attributes / baking / Rhino document IO | Elefront, Human | Layered bake, object names, attributes, blocks, materials, document references. | Preview-only GH exploration. |
| Paneling / facade grids | PanelingTools, LunchBox, Pufferfish | Repeated facade cells, grids, rationalized panels, tweened section/curve logic. | Before massing is accepted. |
| Mesh / SubD / smoothing | Weaverbird, Mesh+, Pufferfish | Softened mesh/SubD, voxel/mesh preview, subdivision workflows. | When exact NURBS/Brep solids are required for analysis. |
| GIS / urban context | Heron, Elk, Caribou, Meerkat | OSM, shapefiles, terrain/elevation, site context, roads/buildings. | User already provides authoritative CAD/site curves. |
| Nesting / fabrication layout | OpenNest, Clipper | 2D packing, cutting sheets, robust planar polygon booleans/offsets. | 3D massing stage. |
| BIM / documentation | Rhino.Inside.Revit, VisualARQ | Revit handoff, BIM objects, IFC/documentation, architectural elements. | Concept massing with no BIM deliverable. |
| Cloud sharing / configurators | ShapeDiver | User wants web app/client configurator from GH definition. | Local-only design iteration. |
| Collaboration / data exchange | Speckle | Connected data-rich model exchange between tools. | Single local Rhino task. |

## Fast Routing Matrix

| User asks for | Start with | Add plugins when | Validation |
| --- | --- | --- | --- |
| Clean tower / BC massing | C# Script node + sliders + RhinoCommon | Pufferfish for tween helpers, Elefront for bake | height, floors, footprint, no floating, source curves preserved |
| Twisted / tapered landmark | Section-stack C# or native GH section stack | Pufferfish for curve/section tweens | same point order, stable corners, no pinched plates |
| Facade grid after accepted massing | Native surface grid / C# line generator | PanelingTools, LunchBox, Pufferfish | grid follows accepted surface, line preview before pipes/panels |
| Climate-responsive massing | Simple massing + metrics outputs | Ladybug/Honeybee after massing preview | sun/radiation/daylight metric tied to design decision |
| Shell / relaxed roof | Simple boundary/rib geometry | Kangaroo for relaxation, Karamba for structural read | supports and loads declared, shell remains grounded |
| Structural concept | Section or frame model | Karamba3D | material/section assumptions visible, not hidden in form script |
| Urban/site context | Rhino/CAD source scan first | Heron/Elk/Caribou only if source context missing | coordinates, units, crop boundary, source authority declared |
| BIM handoff | RhinoCommon/Elefront attributes | Rhino.Inside.Revit or VisualARQ when BIM target exists | categories/types/levels/names mapped explicitly |
| Fabrication/nesting | Clean 2D outlines | OpenNest/Clipper | planar, low-resolution nesting curves, tolerance stated |
| Client configurator | Stable GH definition | ShapeDiver only after local definition is robust | supported plugins, exposed inputs, object counts controlled |

## Recommended Architecture Bundles

### Bundle A - Fast AI Massing

Use for most early design prompts:

```text
RhinoMCP scan
-> C# Script node for geometry
-> native sliders / panels
-> optional Elefront bake after validation
```

Why:

- low MCP operation count;
- source-controlled script body;
- easy to inspect and version;
- avoids plugin dependency unless needed.

### Bundle B - Facade / Panelization

Use after accepted massing:

```text
accepted Brep/SubD/mesh
-> native surface/curve grid
-> Pufferfish for tween/parameter-grid helpers
-> PanelingTools or LunchBox for panel families
-> Elefront bake with layer/name attributes
```

Gate:

Line preview must pass before adding dense pipes, panels, or baked objects.

### Bundle C - Environmental Option Study

Use when the prompt asks for climate, sun, daylight, or comfort:

```text
simple massing variants
-> Ladybug weather / sun / radiation
-> Honeybee only when building energy/daylight simulation is required
-> Wallacei only when objectives and ranges are explicit
```

Gate:

Do not start optimization until the variables, objectives, and constraints are
named in a small table.

### Bundle D - BIM / Revit Handoff

Use when the prompt mentions Revit, BIM, IFC, documentation, categories, levels,
or families:

```text
validated Rhino/GH geometry
-> attributes/layers/names with Elefront or Human
-> Rhino.Inside.Revit for Revit elements
-> VisualARQ when Rhino-native BIM objects/documentation are preferred
```

Gate:

Map geometry to BIM categories before generating detail.

### Bundle E - Fabrication / Cutting

Use when the prompt asks for panels, sheets, cutting, layout, nesting:

```text
accepted panels/outlines
-> planarize / simplify
-> Clipper for robust planar booleans/offsets
-> OpenNest for sheet packing
-> Elefront bake/export layers
```

Gate:

Only low-resolution nesting curves should drive OpenNest; move detailed objects
with the resulting transforms.

## LLM Search Heuristics

When a prompt arrives, look for these cues:

- `sun`, `radiation`, `wind`, `daylight`, `comfort`, `energy` -> Ladybug Tools.
- `relax`, `membrane`, `tension`, `catenary`, `minimal`, `physics` -> Kangaroo.
- `structure`, `beam`, `shell analysis`, `FEA`, `load` -> Karamba3D.
- `optimize`, `multi-objective`, `Pareto`, `fitness` -> Wallacei / Octopus.
- `bake`, `layer`, `attribute`, `block`, `material`, `name` -> Elefront / Human.
- `panel`, `facade grid`, `cell`, `diagrid`, `rationalize` -> PanelingTools / LunchBox / Pufferfish.
- `smooth`, `SubD`, `mesh`, `voxel`, `soft` -> Weaverbird / Mesh+ / Pufferfish.
- `OSM`, `GIS`, `terrain`, `roads`, `map`, `shapefile` -> Heron / Elk / Caribou.
- `nest`, `sheet`, `cut`, `CNC`, `laser` -> OpenNest / Clipper.
- `Revit`, `BIM`, `IFC`, `family`, `level`, `category` -> Rhino.Inside.Revit / VisualARQ.
- `web configurator`, `client app`, `share GH online` -> ShapeDiver.
- `data sync`, `collaboration`, `exchange` -> Speckle.

## Plugin-Use Guardrails

- Confirm availability before relying on a plugin: Package Manager, component
  search, or user confirmation.
- Keep plugin chains downstream of the architectural generator when possible.
- Store the intended plugin dependency in the case note or graph recipe.
- If a plugin is unavailable, preserve a fallback:
  - C# Script / RhinoCommon for geometry;
  - native GH nodes for simple grids and transforms;
  - manual bake/export when Elefront/Human are missing.
- Do not mix analysis plugins into the first massing pass unless analysis is the
  stated goal.
- Do not optimize a vague prompt. First define variables, bounds, objectives,
  and constraints.

## Research Sources

- McNeel Developer Docs: https://developer.rhino3d.com/
- Rhino API References: https://developer.rhino3d.com/api
- Grasshopper Guides: https://developer.rhino3d.com/guides/grasshopper
- Essential C# Scripting for Grasshopper: https://developer.rhino3d.com/guides/grasshopper/csharp-essentials/
- RhinoCommon Geometry in GH C#: https://developer.rhino3d.com/guides/grasshopper/csharp-essentials/3-rhinocommon-geometry/
- McNeel developer samples: https://github.com/mcneel/rhino-developer-samples
- Rhino Package Manager: https://www.rhino3d.com/features/package-manager/
- Yak guides: https://developer.rhino3d.com/guides/yak/
- Food4Rhino: https://www.food4rhino.com/
- Ladybug Tools: https://www.food4rhino.com/en/app/ladybug-tools
- Kangaroo: https://www.food4rhino.com/en/app/kangaroo-physics
- Karamba3D: https://www.food4rhino.com/en/app/karamba3d
- Elefront: https://www.food4rhino.com/en/app/elefront
- Human: https://www.food4rhino.com/en/app/human
- Pufferfish: https://www.food4rhino.com/en/app/pufferfish
- LunchBox: https://www.food4rhino.com/en/app/lunchbox
- PanelingTools: https://www.food4rhino.com/en/app/panelingtools-rhino-and-grasshopper
- OpenNest: https://www.food4rhino.com/en/app/opennest
- Heron: https://www.food4rhino.com/en/app/heron
- Elk: https://www.food4rhino.com/en/app/elk
- VisualARQ: https://www.food4rhino.com/en/app/visualarq
- Rhino.Inside.Revit: https://www.rhino3d.com/features/rhino-inside-revit/
- Rhino.Inside.Revit GitHub: https://github.com/mcneel/rhino.inside-revit
- ShapeDiver: https://www.shapediver.com/
- Speckle Grasshopper: https://speckle.systems/integrations/grasshopper/
