# Seed Voxel Skyscraper - Grasshopper Graph Recipe

Use with:

```text
scripts/grasshopper/examples/voxel_seed_skyscraper_csharp.cs
```

Goal: keep the random voxel tower fast while still letting the definition use
native Grasshopper nodes and plugins around the script output.

The live Grasshopper test on 2026-06-22 uses two branches:

- hybrid branch: C# generates deterministic occupied voxel centers, Pufferfish
  `Voxel Mesh` builds the actual voxel mesh;
- pure node branch: `Center Box -> Populate 3D -> Pufferfish Voxel Mesh` gives
  a fully node-only seed-driven voxel cloud proof.

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

## Pufferfish Voxel Mesh Path

```text
C# VoxelPoints
-> XY Plane
-> Pufferfish Voxel Mesh
   Points = VoxelPoints
   Plane = XY Plane
   Size X = CellSize
   Size Y = CellSize
   Size Z = FloorHeight
-> Custom Preview
```

Use this as the main Grasshopper/plugin-visible voxel path. The C# node handles
only the deterministic seed mask and point centers; the voxel mesh is generated
by Pufferfish.

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

## Pure Node Seed Proof

This branch uses no C# geometry generation:

```text
NodeWidth, NodeDepth, NodeHeight
-> Center Box
NodeCount, NodeSeed
-> Populate 3D
NodeCell
-> Pufferfish Voxel Mesh
-> Custom Preview
```

It is less architectural than the seed-mask tower because the points are random
inside a box, but it is useful as a fully node-only seed-driven voxel proof.
For a grounded tower, move the box or resulting voxel mesh upward by
`NodeHeight / 2`.

## Facade Net Path

```text
C# FacadeLines
-> Cull Index / Dispatch for density control
-> native Pipe or Pufferfish Parameter Pipe Mesh
-> Custom Preview
```

Only pipe lines after the line preview is accepted. Dense pipes will slow
Grasshopper more than the voxel generator itself.

## Validation Gates

Before baking:

- change `Seed` several times and confirm the tower remains architectural, not
  random noise;
- check `Metrics` for face and line counts;
- verify total height from `Floors * FloorHeight`;
- approve massing through `EnvelopeMesh` before adding pipes or panels;
- keep plugin outputs downstream of the C# node, not hidden inside the script.
