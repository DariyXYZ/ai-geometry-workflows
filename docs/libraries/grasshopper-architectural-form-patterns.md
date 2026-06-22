# Grasshopper Architectural Form Patterns

Status: active bridge library.

Use this when architectural massing rules need to become a Grasshopper graph.
The goal is to avoid generic parametric sculpture: every Grasshopper definition
should carry a readable architectural intent, a small set of controlling
parameters, and validation gates.

This file connects:

```text
docs/libraries/form-operator-library.md
-> docs/libraries/grasshopper-pattern-library.md
-> docs/tools/grasshopper-workflow.md
```

## Core Translation Rule

Grasshopper is the geometry executor. Architectural pattern logic comes first.

```text
site / TEP / view / movement reason
-> architectural pattern
-> control geometry
-> GH graph recipe
-> preview form
-> architectural validation
-> optional facade/detail graph
```

Do not start from available nodes alone. Pick the architectural pattern first,
then choose nodes and plugins that express it.

## Pattern Contract

Every reusable Grasshopper form pattern should declare:

- architectural intent;
- source authority: site lines, footprint, existing massing, sketches, or text;
- primary control geometry: axis, spine, footprint, section stack, rails,
  attractor points, or surface;
- main parameters: height, floors, plate depth, twist, taper, offsets, setbacks,
  density, grid count;
- graph family: loft, sweep, morph, surface grid, mesh deformation, section
  tweening, panelization, contouring;
- plugin dependency, if any;
- validation gates before detail or bake.

## Pattern - Section Stack Tower

Use when:

- a tower is controlled by floor plates or repeated horizontal sections;
- the form needs taper, twist, or soft corners;
- the output should remain easy to compare against TEP and floor count.

Architectural intent examples:

- twisted landmark tower;
- slender tower with lighter crown;
- tower with view-oriented rotation;
- existing massing revision with the same gabarit.

Control geometry:

```text
base footprint
-> floor/elevation parameter list
-> transformed section curves
-> lofted Brep/SubD/mesh
-> floor plates and facade guides
```

Useful native nodes:

- `Series` / `Range`
- `Graph Mapper`
- `Move`
- `Scale`
- `Rotate`
- `Loft`
- `Contour`
- `Divide Curve`
- `Surface Closest Point`
- `Evaluate Surface`
- `IsoTrim`

Useful plugin families:

- Pufferfish `Tween Through Curves`
- Pufferfish `Tween Consecutive Curves`
- Pufferfish `Rebuild Curve`
- Pufferfish `Parameter Surface Grid`
- Pufferfish `Tween Through Curves On Surface`

Validation:

- floor count and height match intent;
- section stack does not collapse near the core;
- silhouette reads from main viewpoints;
- facade guides follow the same section logic as the massing;
- detail is not added until the lofted form is accepted.

## Pattern - Spine And Rib Building

Use when:

- the building follows a curved site edge, promenade, transit axis, or public
  spine;
- the form should read as a flowing bar, terminal, museum, or low-rise shell;
- vertical sections are more authoritative than floor plates.

Control geometry:

```text
spine curve
-> stations along spine
-> local planes
-> rib profiles
-> loft / sweep / tweened sections
-> facade ribs or structural lines
```

Useful native nodes:

- `Divide Curve`
- `Perp Frame`
- `Orient`
- `Scale NU`
- `Loft`
- `Sweep1`
- `Offset Curve`
- `Pipe`

Useful plugin families:

- Pufferfish `Tween Through Curves Along Curve`
- Pufferfish `Slide Curve Along Curve`
- Pufferfish `Tween Consecutive Curves Along Curve`
- Pufferfish `Parameter Pipe Mesh`

Validation:

- spine has an architectural reason;
- entries and public edges remain legible;
- station spacing is controlled, not accidental;
- shell or bar remains grounded;
- ribs do not become facade detail before massing approval.

## Pattern - Podium Plus Dynamic Tower

Use when:

- the site needs a clear public base and a higher landmark;
- office TEP efficiency matters;
- the tower needs a visible image move without destroying the ground plane.

Control geometry:

```text
public spine / service edge
-> podium footprint
-> tower anchor
-> tower section stack
-> podium cuts / courtyard / active edge
-> facade grid by surface or section contours
```

Useful native nodes:

- `Boundary Surfaces`
- `Extrude`
- `Solid Difference`
- `Area`
- `Box`
- `Loft`
- `Surface Split`
- `Contour`

Useful plugin families:

- Pufferfish `Offset Curve`
- Pufferfish `Bounding Rectangle`
- Pufferfish `Parameter Surface Grid`
- Pufferfish `Net On Surface`
- Pufferfish `Parameter Loft Mesh`

Validation:

- podium and tower have a clean joint;
- public movement is not blocked by low bars;
- tower anchor is tied to view, entry, or skyline logic;
- TEP is preserved after podium cuts;
- no accidental intersections are presented as design.

## Pattern - Facade Net From Accepted Form

Use when:

- the massing is accepted and needs a readable facade logic;
- linework should follow the surface instead of floating in space;
- the output should remain light enough for Grasshopper preview.

Control geometry:

```text
accepted Brep/SubD/mesh
-> facade surface selection
-> UV or curve grid
-> horizontal floor bands
-> vertical ribs / diagonals / density variation
-> lightweight line preview
```

Useful native nodes:

- `Deconstruct Brep`
- `Divide Domain2`
- `IsoTrim`
- `Evaluate Surface`
- `Isotrim`
- `Interpolate`
- `Polyline`
- `Pipe` only after line density is proven

Useful plugin families:

- Pufferfish `Parameter Surface Grid`
- Pufferfish `Parameter Surface Isocurve`
- Pufferfish `Net On Surface`
- Pufferfish `Tween Through Curves On Surface`

Validation:

- grid follows surface parameterization cleanly;
- floor bands correspond to plausible floor heights;
- facade density is controlled by a parameter or attractor;
- line preview is approved before pipes, panels, or baked detail;
- facade work does not hide a weak massing.

## Pattern - Attractor-Based Softening

Use when:

- a corner, crown, terrace, or facade density should respond to a view, entry,
  daylight, or public-space attractor;
- the form needs controlled local variation, not random deformation.

Control geometry:

```text
base sections / surface grid
-> attractor point or curve
-> distance field
-> remapped parameter
-> local scale / offset / rotation / density change
```

Useful native nodes:

- `Distance`
- `Bounds`
- `Remap Numbers`
- `Graph Mapper`
- `Scale`
- `Move`
- `Evaluate Surface`

Useful plugin families:

- Pufferfish `Weighted Average Curve`
- Pufferfish `Weighted Average Mesh`
- Pufferfish `Displace Mesh`
- Pufferfish `Smooth Curve`
- Pufferfish `Rebuild Mesh`

Validation:

- the attractor is named and has an architectural reason;
- deformation stays within buildable limits;
- floor plates remain usable;
- no pinch points or facade self-intersections appear;
- before/after delta can be explained in one sentence.

## Classic Node-First Build Order

For node-only Grasshopper work, prefer this order:

```text
sliders / panels / source geometry
-> ranges and control points
-> source curves or profiles
-> section transformations
-> tween / loft / sweep / surface / mesh
-> facade grid from accepted form
-> metrics panels
-> bake only after preview validation
```

If using a C# Script node, keep it as one compact generator or metric node.
If the user asks for classic Grasshopper, do not hide the whole algorithm inside
C#.

## Anti-Patterns

- starting from a plugin menu and inventing a building around the component;
- using twist, smooth, tween, or displace with no site or image reason;
- making a complex facade grid before accepting the primary massing;
- using dense pipes/panels before line previews pass;
- baking Grasshopper preview geometry before validating height, footprint, and
  silhouette;
- calling a generic blob a tower without floor, core, entry, and facade logic.

## Handoff Template

Use this short template when recording a reusable GH form graph:

```yaml
pattern_name:
architectural_intent:
source_authority:
control_geometry:
native_nodes:
plugin_nodes:
parameters:
outputs:
validation_gates:
known_risks:
```
