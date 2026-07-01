# RhinoMCP Command Library

Status: active command-selection library.

Use this file when the user gives a modeling intent such as "build a slab",
"make a roof guard", "project lamellas to the facade", or "clean the view".
The goal is to translate architectural language into a reliable RhinoMCP /
RhinoCommon execution sequence.

This is not a Grasshopper graph library. Grasshopper cases live under
`docs/tools/grasshopper/` and `docs/cases/grasshopper/`.

## Default Execution Stack

Use this order for normal Rhino work:

```text
intent
-> source authority and stage gate
-> RhinoMCP capability scan
-> RhinoCommon script through mcp__rhino.run_python or mcp__rhino.run_csharp
-> Rhino command only when command behavior is needed
-> visible-layer cleanup and numeric validation
```

Do not use Aurox return shapes, Aurox helper names, or hidden plugin behavior
in new command cards. Aurox is legacy/optional and belongs only in archive,
explicit replay, or deliberate backend workaround notes.

## Preflight For Every Build

Before changing geometry:

```text
mcp__rhino.list_slots
-> mcp__rhino.run_python:
   Rhino version, document name, unit system, object count, active layer
-> set or confirm units for the task
-> mcp__rhino.get_commands for any Rhino command family you plan to call
-> tiny run_python/run_csharp smoke if using a new RhinoCommon pattern
```

For architecture massing, units are meters unless the source says otherwise.
Record the slot, units, and source layers in the case note or final handoff.

## Stage Gates

Choose the detail level before building:

| Stage | Allowed geometry | Forbidden before approval |
| --- | --- | --- |
| Zoning | site bands, entries, service/public edges, tentative footprints | 3D massing, facade detail |
| Massing | primary volumes, floor/roof slabs, setbacks, cores, roof exits, major voids | dense windows, mullions, ribs, signage, high-count facade modules |
| Detail | approved facade rhythm, panels, openings, guards, lamellas | new large opaque volumes that change silhouette |
| Cleanup | layer visibility, names, small fixes, validation labels | rebuilding accepted massing unless requested |

When the user asks for massing, show massing. Do not spend tokens or Rhino
operations on unsanctioned facade detail.

## Command Card Template

Use this structure when adding a new reusable command:

```text
Intent:
Inputs:
RhinoMCP route:
RhinoCommon operations:
Layer policy:
Validation:
Failure gates:
```

## Core Command Cards

### Build Floor Slab / Perekrytie

Intent: create a real slab from a closed floor contour or footprint.

Inputs:

- one closed planar curve, or a list of joined boundary curves;
- elevation `z`;
- thickness, usually `0.18-0.35 m` for concept massing unless a structural
  value is provided;
- layer/name prefix.

RhinoMCP route:

```text
run_python
-> join/validate source curve
-> set curve to target Z if needed
-> create closed extrusion from the curve
-> cap solid
-> assign final slab layer and name
-> add optional top/bottom edge curves only if needed for review
```

RhinoCommon operations:

```text
Curve.JoinCurves
Curve.TryGetPlane
Extrusion.Create(closed_curve, thickness, true)
Brep/Extrusion cap check
doc.Objects.AddBrep or AddExtrusion
```

Validation:

- source curve is closed and planar;
- extrusion direction matches the architectural intent;
- bottom of the slab does not accidentally go below the source datum unless
  that was requested;
- bbox height equals requested thickness within tolerance.

Failure gates:

- do not make slabs from loose open polylines;
- do not draw only outline curves when a slab solid is requested;
- do not offset the glass/facade line instead of the slab edge.

### Build Floor Stack From Footprint

Intent: massing floors from one approved footprint.

Inputs: footprint curve, floor count, floor-to-floor height, slab thickness,
optional setback levels.

Route:

```text
run_python
-> validate footprint
-> for each floor: copy footprint to Z datum
-> extrude slab or floor mass by stage
-> optional contour/top curves for review
-> group/name by level range
```

For massing, use low object count: floor bands or level groups are better than
hundreds of individual panels. Use real per-floor slabs only when the user asks
for floor-by-floor readability or TEP checking.

Validation:

- total height equals `floors * floor_to_floor` plus roof/parapet assumptions;
- footprint does not move from user-approved source;
- layer names separate source, final mass, and helper curves.

### Build Massing Block From Footprint

Intent: create early building mass without facade detail.

Route:

```text
closed footprint
-> Extrusion.Create / Brep.CreateFromLoft for vertical or tapered mass
-> cap
-> assign final mass layer
-> add only major floor bands if useful
```

Use a section stack/loft instead of one vertical extrusion when the form has
taper, twist, curved sides, or setback levels.

Failure gates:

- no random core boxes;
- no facade windows before massing approval;
- no unsupported overhangs or blocks hanging off the podium unless intentional.

### Build Roof Guard / Terrace Parapet

Intent: make clean guards around operated roofs or stepped terraces.

Preferred manual Rhino command grammar:

```text
DupBorder
-> Offset x 2
-> Extrude
```

RhinoCommon equivalent:

```text
duplicate roof border curve
-> Curve.Offset inward/outward by guard thickness
-> build closed ring from outer and inner loops
-> extrude guard height, usually 1.05-1.2 m for concept roof safety
-> cap and assign roof/guard layer
```

Validation:

- guard is a continuous closed ring;
- corners are clean, not separate ragged boxes;
- guard does not crawl onto the facade plane;
- roof access volumes are tied to core/LLY zones.

Failure gates:

- no segmented random parapet blocks;
- no fences floating above or intersecting facade openings;
- no one roof-access box per terrace unless the core actually reaches it.

### Build Roof Access / LLY Exit Volume

Intent: show where a core reaches an operated roof during massing.

Route:

```text
choose core/service zone first
-> place compact roof exit volume inside the roof plate
-> align with circulation logic
-> keep it set back from facade edges
-> assign roof-access/core layer
```

Validation:

- core count matches plate length and egress logic;
- roof access does not create awkward narrow floor strips;
- roof exit is visible enough for massing but not over-detailed.

### Build Ground LLY Emergency Exit

Intent: show emergency exits directly from lift/lobby/stair core zones.

Route:

```text
find core/LLY zone on plan
-> choose nearest suitable facade bay
-> adjust first-floor window grid if needed
-> create door/panel in local facade plane
-> add only minimal threshold pad projecting outward
```

Validation:

- exit is direct from LLY/core zone, not a decorative public portal;
- four exits are a good default for a long two-core office slab unless the
  source egress plan says otherwise;
- door/panel geometry is coplanar with the facade;
- threshold pad may project, but the door frame/opening must not float away
  from the facade.

### Build Facade Plane Opening Or Panel

Intent: add a door, window, opaque panel, or infill on an approved facade.

Route:

```text
identify local facade plane
-> project rectangle/module points onto that plane
-> create planar surface or shallow inset/extrusion normal to that plane
-> keep module inside the facade grid bay
```

Validation:

- panel/opening lies in the local facade plane;
- offsets are along the local normal, not world X/Y guesswork;
- first-floor entries align with the same grid logic as windows.

Failure gates:

- no floating boxes in front of facade;
- no windows/doors that ignore the ground-floor grid;
- no detail before massing approval.

### Project Lamellas To Facade

Intent: create vertical fins/lamellas that follow the facade surface.

Route:

```text
approved facade surface or facade polyline
-> create module stations along edge/UV direction
-> evaluate closest point / local plane on facade
-> build each lamella from facade plane with small controlled offset
-> skip ground floor if the concept requires clear glass base
```

Validation:

- lamellas sit on or near the facade, not at a large offset;
- lower/public floor rules are respected;
- top/bottom extents are consistent and do not pierce roof slabs.

### Build Transfer Link Between Volumes

Intent: connect two podiums/towers without a random connector object.

Route:

```text
identify floors to connect
-> create monolithic bridge/transfer volume or deck between approved masses
-> carve/leave a clear passage if public route must pass through
-> align top/bottom to floor datums
```

Validation:

- link reads as part of the building system;
- passage is legible;
- link does not become a detached dark block or unsupported tube.

### Clean Final Review View

Intent: leave the user with a clear Rhino viewport after generation.

Route:

```text
hide source/helper/construction/temp layers by default
-> keep final mass/detail layers visible
-> keep intentional site boundary/context visible
-> add horizontal ground labels only when requested
-> run visible object/layer audit
```

Validation:

- no old variants visible unless comparison was requested;
- no helper curves, section frames, construction points, or debug labels in the
  final review view;
- labels lie horizontally on the ground and do not block the model.

## When To Use Rhino Commands Instead Of RhinoCommon

Use Rhino command strings through RhinoMCP only when the command itself is the
desired modeling grammar or when it is faster and safer than rebuilding the
logic:

| Intent | Rhino command family |
| --- | --- |
| inspect existing edge/border | `DupBorder`, `DupEdge` |
| generate contours from a temporary volume | `Contour` |
| user-facing offset review | `Offset`, `OffsetSrf` |
| simple boolean proof | `BooleanDifference`, `BooleanUnion` |
| visual cleanup | `SelLayer`, `Hide`, `Show`, `SetObjectName`, `SetLayer` |

For multi-step geometry, prefer one `run_python` or `run_csharp` script over
many small command calls. It is more token-efficient and easier to validate.

## Standard Layer Naming

Use ASCII layer names:

```text
00_source_context
01_final_massing
02_final_slabs_roofs
03_final_cores_access
04_final_facade_detail
05_final_entries
90_helper_construction
99_archive_old
```

Hide `90_*` and `99_*` before final review. Do not delete user source layers
unless the user explicitly asks.

## Write Back Rule

If a command sequence succeeds or fails in a reusable way, update one of:

- this file for command grammar;
- `docs/errors/massing/moscow-bc-massing-error-library.md` for massing errors;
- `docs/cases/rhino-geometry/` for a concrete Rhino case;
- `docs/case-digest.md` for compact promoted rules.
