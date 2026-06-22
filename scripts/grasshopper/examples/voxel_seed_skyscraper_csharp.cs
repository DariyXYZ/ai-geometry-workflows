#region Usings
using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;
#endregion

// Case: seed-driven voxel skyscraper.
// Target: Rhino 8 C# Script component, C# 9-compatible.
// Units: meters.
//
// Inputs:
//   Seed, Floors, GridX, GridY, CellSize, FloorHeight, Density,
//   TwistDeg, Taper, TerraceBias, Noise, MakeBoxes, FacadeEvery
// Outputs:
//   VoxelPoints, EnvelopeMesh, FloorOutlines, FacadeLines, PluginGuides, Metrics, Info
//
// Fast workflow:
//   EnvelopeMesh is the fastest direct preview output.
//   VoxelPoints can drive Pufferfish Voxel Mesh, so visible plugin nodes can
//   build the final voxelized mesh.
//   PluginGuides are sparse section curves for Pufferfish Tween Through Curves,
//   Parameter Loft Mesh, Net On Surface, or native Loft/Contour workflows.
public class Script_Instance : GH_ScriptInstance
{
  private bool _described = false;

  private void RunScript(
    object Seed,
    object Floors,
    object GridX,
    object GridY,
    object CellSize,
    object FloorHeight,
    object Density,
    object TwistDeg,
    object Taper,
    object TerraceBias,
    object Noise,
    object MakeBoxes,
    object FacadeEvery,
    ref object VoxelPoints,
    ref object EnvelopeMesh,
    ref object FloorOutlines,
    ref object FacadeLines,
    ref object PluginGuides,
    ref object Metrics,
    ref object Info)
  {
    VoxelPoints = new List<Point3d>();
    EnvelopeMesh = null;
    FloorOutlines = new List<Curve>();
    FacadeLines = new List<Curve>();
    PluginGuides = new List<Curve>();
    Metrics = null;
    Info = "Voxel tower idle.";

    SetComponentDescriptions();

    int seed = ReadInt(Seed, 240622);
    if (seed == 0)
      seed = 240622;
    int floors = Clamp(ReadInt(Floors, 48), 6, 120);
    int gx = Clamp(ReadInt(GridX, 13), 5, 35);
    int gy = Clamp(ReadInt(GridY, 11), 5, 35);
    double cell = ReadDouble(CellSize, 4.2);
    if (cell <= 0.05)
      cell = 4.2;
    double floorH = ReadDouble(FloorHeight, 3.9);
    if (floorH <= 0.05)
      floorH = 3.9;
    double density = Clamp01(ReadDouble(Density, 0.74));
    double twistDeg = ReadDouble(TwistDeg, 145.0);
    double taper = ReadDouble(Taper, 0.68);
    taper = taper > 0.05 ? Math.Min(taper, 1.35) : 0.68;
    double terraceBias = Clamp01(ReadDouble(TerraceBias, 0.34));
    double noise = Clamp01(ReadDouble(Noise, 0.42));
    bool makeBoxes = ReadBool(MakeBoxes, false);
    int facadeEvery = Clamp(ReadInt(FacadeEvery, 4), 1, 20);

    RhinoDoc doc = RhinoDoc.ActiveDoc;
    double tolerance = doc != null ? doc.ModelAbsoluteTolerance : 0.001;

    bool[,,] occupied = new bool[floors, gx, gy];
    int occupiedCount = 0;

    double halfX = (gx - 1) * 0.5;
    double halfY = (gy - 1) * 0.5;
    double coreRadiusCells = Math.Max(1.25, Math.Min(gx, gy) * 0.16);

    for (int f = 0; f < floors; f++)
    {
      double t = floors == 1 ? 0.0 : (double)f / (double)(floors - 1);
      double shapeScale = Lerp(1.0, taper, Smooth01(t));
      double waist = 1.0 - 0.16 * Bell(t, 0.48, 0.22);
      double crownLift = 1.0 + 0.08 * Bell(t, 0.88, 0.11);
      double rx = Math.Max(1.5, halfX * shapeScale * waist * crownLift);
      double ry = Math.Max(1.5, halfY * (0.94 * shapeScale + 0.06) * waist);
      double terraceCut = terraceBias * Smooth01(t);

      for (int ix = 0; ix < gx; ix++)
      {
        for (int iy = 0; iy < gy; iy++)
        {
          double lx = ix - halfX;
          double ly = iy - halfY;
          double coreMetric = Math.Sqrt(lx * lx + ly * ly);

          double angle = Math.Atan2(ly, lx);
          double lobe = 1.0 + 0.10 * Math.Sin(3.0 * angle + seed * 0.017 + t * Math.PI * 2.0);
          double superEllipse = Math.Pow(Math.Abs(lx) / (rx * lobe), 2.8) +
                                Math.Pow(Math.Abs(ly) / (ry / lobe), 2.8);

          double edgeSoftness = 1.0 - superEllipse;
          double h = Hash01(seed, f, ix, iy);
          double h2 = Hash01(seed + 9187, ix, iy, f);
          double verticalVein = 0.18 * Math.Sin((ix * 0.71 + iy * 0.37) + seed * 0.013 + f * 0.21);
          double threshold = 0.30 + density * 0.55 + verticalVein;

          bool inMainMass = superEllipse < 1.0 + noise * 0.24;
          bool keepByNoise = h < threshold + edgeSoftness * 0.32 - terraceCut * Math.Max(0.0, superEllipse - 0.55);
          bool keepTerrace = !(t > 0.45 && superEllipse > 0.70 && h2 < terraceBias * 0.42);
          bool keepCore = coreMetric <= coreRadiusCells;

          bool keep = keepCore || (inMainMass && keepByNoise && keepTerrace);
          occupied[f, ix, iy] = keep;
          if (keep)
            occupiedCount++;
        }
      }
    }

    var boxes = new List<Brep>(makeBoxes ? occupiedCount : 0);
    var voxelPoints = new List<Point3d>(occupiedCount);
    var mesh = new Mesh();
    var outlines = new List<Curve>(floors);
    var facade = new List<Curve>();
    var pluginGuides = new List<Curve>();

    for (int f = 0; f < floors; f++)
    {
      double t = floors == 1 ? 0.0 : (double)f / (double)(floors - 1);
      double z0 = f * floorH;
      double z1 = z0 + floorH;
      Plane floorPlane = RotatedFloorPlane(z0, RhinoMath.ToRadians(twistDeg * Smooth01(t)));

      var floorCorners = new List<Point2d>();

      for (int ix = 0; ix < gx; ix++)
      {
        for (int iy = 0; iy < gy; iy++)
        {
          if (!occupied[f, ix, iy])
            continue;

          double x0 = (ix - halfX - 0.5) * cell;
          double x1 = (ix - halfX + 0.5) * cell;
          double y0 = (iy - halfY - 0.5) * cell;
          double y1 = (iy - halfY + 0.5) * cell;
          voxelPoints.Add(floorPlane.PointAt((x0 + x1) * 0.5, (y0 + y1) * 0.5, floorH * 0.5));

          floorCorners.Add(new Point2d(x0, y0));
          floorCorners.Add(new Point2d(x1, y0));
          floorCorners.Add(new Point2d(x1, y1));
          floorCorners.Add(new Point2d(x0, y1));

          if (makeBoxes)
          {
            var box = new Box(
              floorPlane,
              new Interval(x0, x1),
              new Interval(y0, y1),
              new Interval(0.0, floorH));
            Brep brep = box.ToBrep();
            if (brep != null)
              boxes.Add(brep);
          }

          AddExposedFaces(mesh, occupied, f, ix, iy, gx, gy, floors, floorPlane, x0, x1, y0, y1, 0.0, floorH);

          if (f % facadeEvery == 0 || f == floors - 1)
            AddFacadeLinesForExposedCell(facade, occupied, f, ix, iy, gx, gy, floorPlane, x0, x1, y0, y1, 0.0, floorH);
        }
      }

      PolylineCurve outline = ConvexHullCurve(floorCorners, floorPlane, tolerance);
      if (outline != null)
      {
        outlines.Add(outline);
        if (f == 0 || f == floors - 1 || f % Math.Max(3, facadeEvery) == 0)
          pluginGuides.Add(outline);
      }
    }

    mesh.Normals.ComputeNormals();
    mesh.Compact();

    VoxelPoints = voxelPoints;
    EnvelopeMesh = mesh;
    FloorOutlines = outlines;
    FacadeLines = facade;
    PluginGuides = pluginGuides;

    double height = floors * floorH;
    double footprintX = gx * cell;
    double footprintY = gy * cell;
    string units = doc != null ? doc.ModelUnitSystem.ToString() : "unknown";

    Metrics = string.Format(
      "seed={0}; floors={1}; height={2:0.0}m; grid={3}x{4}; occupied={5}; boxes_built={6}; mesh_faces={7}; facade_lines={8}; guides={9}",
      seed,
      floors,
      height,
      gx,
      gy,
      occupiedCount,
      makeBoxes ? boxes.Count : 0,
      mesh.Faces.Count,
      facade.Count,
      pluginGuides.Count);

    Info = string.Format(
      "Voxel skyscraper ready. Footprint envelope {0:0.0} x {1:0.0} m, height {2:0.0} m, twist {3:0.0} deg, units {4}. Use EnvelopeMesh for fast preview; wire PluginGuides to Pufferfish Tween/Loft workflows and FacadeLines to native Pipe only after density is approved.",
      footprintX,
      footprintY,
      height,
      twistDeg,
      units);
  }

  private void SetComponentDescriptions()
  {
    if (_described || Component == null)
      return;

    _described = true;
    Component.Name = "Seed Voxel Skyscraper";
    Component.NickName = "VoxelTower";
    Component.Description = "Seed-driven voxel tower generator with fast mesh preview, optional Brep voxels, facade linework, and plugin guide curves.";

    SetInputDescription("Seed", "Deterministic random seed. Change it to generate another stable tower.");
    SetInputDescription("Floors", "Number of voxel floors in the tower.");
    SetInputDescription("GridX", "Voxel grid count across the wider footprint direction.");
    SetInputDescription("GridY", "Voxel grid count across the deeper footprint direction.");
    SetInputDescription("CellSize", "Voxel cell width and depth in model units.");
    SetInputDescription("FloorHeight", "Height of one voxel floor in model units.");
    SetInputDescription("Density", "How much of the voxel field remains filled. Higher values make a heavier tower.");
    SetInputDescription("TwistDeg", "Total tower twist from base to crown in degrees.");
    SetInputDescription("Taper", "Top scale relative to base. Lower values make a slimmer crown.");
    SetInputDescription("TerraceBias", "Amount of upper-floor carving and terraces.");
    SetInputDescription("Noise", "Amount of seed-driven edge breakup.");
    SetInputDescription("MakeBoxes", "If true, outputs individual Brep voxel boxes. Keep false for fast slider work.");
    SetInputDescription("FacadeEvery", "Floor interval for facade guide line extraction.");

    SetOutputDescription("VoxelPoints", "Occupied voxel centers. Connect to Pufferfish Voxel Mesh for visible node-based voxelization.");
    SetOutputDescription("EnvelopeMesh", "Fast exposed-face mesh for preview, Weaverbird-style smoothing, SubD conversion, or mesh plugin workflows.");
    SetOutputDescription("FloorOutlines", "Convex floor outline curves for native Loft, Contour comparison, or section checks.");
    SetOutputDescription("FacadeLines", "Lightweight facade grid lines. Pipe these only after line density is approved.");
    SetOutputDescription("PluginGuides", "Sparse section curves for Pufferfish Tween Through Curves, Parameter Loft Mesh, and facade-net workflows.");
    SetOutputDescription("Metrics", "Compact parameter and output-count summary.");
    SetOutputDescription("Info", "Human-readable usage note.");
  }

  private void SetInputDescription(string name, string description)
  {
    for (int i = 0; i < Component.Params.Input.Count; i++)
    {
      if (Component.Params.Input[i].Name == name)
      {
        Component.Params.Input[i].Description = description;
        return;
      }
    }
  }

  private void SetOutputDescription(string name, string description)
  {
    for (int i = 0; i < Component.Params.Output.Count; i++)
    {
      if (Component.Params.Output[i].Name == name)
      {
        Component.Params.Output[i].Description = description;
        return;
      }
    }
  }

  private static Plane RotatedFloorPlane(double z, double angle)
  {
    double ca = Math.Cos(angle);
    double sa = Math.Sin(angle);
    var origin = new Point3d(0.0, 0.0, z);
    var xAxis = new Vector3d(ca, sa, 0.0);
    var yAxis = new Vector3d(-sa, ca, 0.0);
    return new Plane(origin, xAxis, yAxis);
  }

  private static void AddExposedFaces(
    Mesh mesh,
    bool[,,] occupied,
    int f,
    int ix,
    int iy,
    int gx,
    int gy,
    int floors,
    Plane p,
    double x0,
    double x1,
    double y0,
    double y1,
    double z0,
    double z1)
  {
    if (!IsOccupied(occupied, f, ix, iy - 1, gx, gy, floors))
      AddQuad(mesh, p.PointAt(x0, y0, z0), p.PointAt(x1, y0, z0), p.PointAt(x1, y0, z1), p.PointAt(x0, y0, z1));
    if (!IsOccupied(occupied, f, ix + 1, iy, gx, gy, floors))
      AddQuad(mesh, p.PointAt(x1, y0, z0), p.PointAt(x1, y1, z0), p.PointAt(x1, y1, z1), p.PointAt(x1, y0, z1));
    if (!IsOccupied(occupied, f, ix, iy + 1, gx, gy, floors))
      AddQuad(mesh, p.PointAt(x1, y1, z0), p.PointAt(x0, y1, z0), p.PointAt(x0, y1, z1), p.PointAt(x1, y1, z1));
    if (!IsOccupied(occupied, f, ix - 1, iy, gx, gy, floors))
      AddQuad(mesh, p.PointAt(x0, y1, z0), p.PointAt(x0, y0, z0), p.PointAt(x0, y0, z1), p.PointAt(x0, y1, z1));
    if (!IsOccupied(occupied, f - 1, ix, iy, gx, gy, floors))
      AddQuad(mesh, p.PointAt(x0, y1, z0), p.PointAt(x1, y1, z0), p.PointAt(x1, y0, z0), p.PointAt(x0, y0, z0));
    if (!IsOccupied(occupied, f + 1, ix, iy, gx, gy, floors))
      AddQuad(mesh, p.PointAt(x0, y0, z1), p.PointAt(x1, y0, z1), p.PointAt(x1, y1, z1), p.PointAt(x0, y1, z1));
  }

  private static void AddFacadeLinesForExposedCell(
    List<Curve> lines,
    bool[,,] occupied,
    int f,
    int ix,
    int iy,
    int gx,
    int gy,
    Plane p,
    double x0,
    double x1,
    double y0,
    double y1,
    double z0,
    double z1)
  {
    if (!IsOccupied(occupied, f, ix, iy - 1, gx, gy, occupied.GetLength(0)))
      AddFaceGridLines(lines, p, x0, x1, y0, y0, z0, z1);
    if (!IsOccupied(occupied, f, ix + 1, iy, gx, gy, occupied.GetLength(0)))
      AddFaceGridLines(lines, p, x1, x1, y0, y1, z0, z1);
    if (!IsOccupied(occupied, f, ix, iy + 1, gx, gy, occupied.GetLength(0)))
      AddFaceGridLines(lines, p, x1, x0, y1, y1, z0, z1);
    if (!IsOccupied(occupied, f, ix - 1, iy, gx, gy, occupied.GetLength(0)))
      AddFaceGridLines(lines, p, x0, x0, y1, y0, z0, z1);
  }

  private static void AddFaceGridLines(List<Curve> lines, Plane p, double ax, double bx, double ay, double by, double z0, double z1)
  {
    Point3d a0 = p.PointAt(ax, ay, z0);
    Point3d b0 = p.PointAt(bx, by, z0);
    Point3d a1 = p.PointAt(ax, ay, z1);
    Point3d b1 = p.PointAt(bx, by, z1);
    lines.Add(new LineCurve(a0, b0));
    lines.Add(new LineCurve(a0, a1));
    lines.Add(new LineCurve(b0, b1));
  }

  private static bool IsOccupied(bool[,,] occupied, int f, int ix, int iy, int gx, int gy, int floors)
  {
    if (f < 0 || f >= floors || ix < 0 || ix >= gx || iy < 0 || iy >= gy)
      return false;
    return occupied[f, ix, iy];
  }

  private static void AddQuad(Mesh mesh, Point3d a, Point3d b, Point3d c, Point3d d)
  {
    int start = mesh.Vertices.Count;
    mesh.Vertices.Add(a);
    mesh.Vertices.Add(b);
    mesh.Vertices.Add(c);
    mesh.Vertices.Add(d);
    mesh.Faces.AddFace(start, start + 1, start + 2, start + 3);
  }

  private static PolylineCurve ConvexHullCurve(List<Point2d> points, Plane plane, double tolerance)
  {
    if (points == null || points.Count < 3)
      return null;

    points.Sort(ComparePoint2d);
    var hull = new List<Point2d>();

    for (int i = 0; i < points.Count; i++)
    {
      while (hull.Count >= 2 && Cross(hull[hull.Count - 2], hull[hull.Count - 1], points[i]) <= tolerance)
        hull.RemoveAt(hull.Count - 1);
      hull.Add(points[i]);
    }

    int lowerCount = hull.Count;
    for (int i = points.Count - 2; i >= 0; i--)
    {
      while (hull.Count > lowerCount && Cross(hull[hull.Count - 2], hull[hull.Count - 1], points[i]) <= tolerance)
        hull.RemoveAt(hull.Count - 1);
      hull.Add(points[i]);
    }

    if (hull.Count < 4)
      return null;

    hull.RemoveAt(hull.Count - 1);

    var poly = new Polyline();
    for (int i = 0; i < hull.Count; i++)
      poly.Add(plane.PointAt(hull[i].X, hull[i].Y, 0.0));
    poly.Add(poly[0]);

    return new PolylineCurve(poly);
  }

  private static int ComparePoint2d(Point2d a, Point2d b)
  {
    int x = a.X.CompareTo(b.X);
    if (x != 0)
      return x;
    return a.Y.CompareTo(b.Y);
  }

  private static double Cross(Point2d o, Point2d a, Point2d b)
  {
    return (a.X - o.X) * (b.Y - o.Y) - (a.Y - o.Y) * (b.X - o.X);
  }

  private static double Hash01(int seed, int a, int b, int c)
  {
    unchecked
    {
      int h = seed;
      h = h * 73856093 ^ a * 19349663;
      h = h * 83492791 ^ b * 297121507;
      h = h * 1103515245 ^ c * 12345;
      uint u = (uint)h;
      return (u & 0x00FFFFFF) / 16777215.0;
    }
  }

  private static double Bell(double t, double center, double width)
  {
    double x = (t - center) / Math.Max(0.0001, width);
    return Math.Exp(-(x * x));
  }

  private static double Smooth01(double t)
  {
    t = Clamp01(t);
    return t * t * (3.0 - 2.0 * t);
  }

  private static double Lerp(double a, double b, double t)
  {
    return a + (b - a) * t;
  }

  private static double Clamp01(double value)
  {
    if (value < 0.0)
      return 0.0;
    if (value > 1.0)
      return 1.0;
    return value;
  }

  private static int Clamp(int value, int min, int max)
  {
    if (value < min)
      return min;
    if (value > max)
      return max;
    return value;
  }

  private static int ReadInt(object value, int fallback)
  {
    double number;
    if (!TryReadDouble(value, out number))
      return fallback;
    return (int)Math.Round(number);
  }

  private static double ReadDouble(object value, double fallback)
  {
    double number;
    return TryReadDouble(value, out number) ? number : fallback;
  }

  private static bool ReadBool(object value, bool fallback)
  {
    if (value == null)
      return fallback;

    if (value is bool)
      return (bool)value;

    var ghBool = value as GH_Boolean;
    if (ghBool != null)
      return ghBool.Value;

    double number;
    if (TryReadDouble(value, out number))
      return Math.Abs(number) > 0.5;

    bool parsed;
    if (bool.TryParse(value.ToString(), out parsed))
      return parsed;

    return fallback;
  }

  private static bool TryReadDouble(object value, out double number)
  {
    number = 0.0;

    if (value == null)
      return false;

    if (value is double)
    {
      number = (double)value;
      return true;
    }

    if (value is int)
    {
      number = (int)value;
      return true;
    }

    if (value is float)
    {
      number = (float)value;
      return true;
    }

    var ghNumber = value as GH_Number;
    if (ghNumber != null)
    {
      number = ghNumber.Value;
      return true;
    }

    var ghInteger = value as GH_Integer;
    if (ghInteger != null)
    {
      number = ghInteger.Value;
      return true;
    }

    return double.TryParse(value.ToString(), out number);
  }
}
