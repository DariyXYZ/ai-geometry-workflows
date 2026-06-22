# Seed Voxel Skyscraper - Grasshopper Graph Recipe

Use with:

```text
scripts/grasshopper/examples/voxel_seed_skyscraper_csharp.cs
```

Goal: keep the random voxel tower fast while still letting the definition use
native Grasshopper nodes and plugins around the script output.

## C# Script Node

Paste `voxel_seed_skyscraper_csharp.cs` into a Rhino 8 C# Script component.

Suggested slider defaults:

| Input | Default | Range |
| --- | ---: | --- |
| `Seed` | `240622` | `1..999999` |
| `Floors` | `48` | `12..90` |
| `GridX` | `13` | `7..23` |
| `GridY` | `11` | `7..23` |
| `CellSize` | `4.2` | `2.5..7.5` |
| `FloorHeight` | `3.9` | `3.2..5.2` |
| `Density` | `0.74` | `0.35..0.95` |
| `TwistDeg` | `145` | `-240..240` |
| `Taper` | `0.68` | `0.35..1.10` |
| `TerraceBias` | `0.34` | `0..0.85` |
| `Noise` | `0.42` | `0..1` |
| `MakeBoxes` | `false` | toggle |
| `FacadeEvery` | `4` | `1..12` |

## Fast Preview Path

```text
C# EnvelopeMesh
-> Custom Preview
-> optional Weaverbird / mesh smoothing
-> optional Rhino SubD conversion after form approval
```

Keep `MakeBoxes=false` while searching seeds. The mesh is the intended fast
interactive output.

## Native GH Form Path

```text
C# FloorOutlines
-> Cull Pattern / List Item for selected levels
-> Loft
-> Deconstruct Brep
-> Divide Domain2
-> IsoTrim
-> Custom Preview
```

Use this when the voxel mass should become a cleaner Brep envelope.

## Pufferfish Path

```text
C# PluginGuides
-> Pufferfish Rebuild Curve
-> Pufferfish Tween Through Curves
-> Pufferfish Parameter Loft Mesh
-> Pufferfish Parameter Surface Grid
```

Use this to turn the voxel sections into a smoother tower family while keeping
the same seed-driven footprint logic.

## Facade Net Path

```text
C# FacadeLines
-> Cull Index / Dispatch for density control
-> native Pipe or Pufferfish Parameter Pipe Mesh
-> Custom Preview
```

Only pipe lines after the line preview is accepted. Dense pipes will slow
Grasshopper more than the voxel generator itself.

## Baking / Attribute Path

```text
C# VoxelBoxes with MakeBoxes=true
-> Elefront / Human attributes
-> bake by floor, seed, or occupied-cell group
```

Use this only for export or presentation snapshots. It is intentionally not the
default preview path.

## Validation Gates

Before baking:

- change `Seed` several times and confirm the tower remains architectural, not
  random noise;
- check `Metrics` for face and line counts;
- verify total height from `Floors * FloorHeight`;
- approve massing through `EnvelopeMesh` before adding pipes or panels;
- keep plugin outputs downstream of the C# node, not hidden inside the script.
