#region Usings
using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
#endregion

public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(
    int Floors,
    double FloorHeight,
    double Width,
    double Depth,
    double TwistDeg,
    double Taper,
    double SlabThick,
    double CoreRadius,
    ref object FloorPlates,
    ref object FacadeRails,
    ref object Core,
    ref object Info)
  {
    var plates = new List<Brep>();
    var rails = new List<Curve>();
    Brep core = null;

    int floors = Math.Max(2, Floors <= 0 ? 42 : Floors);
    double floorHeight = FloorHeight > 0.01 ? FloorHeight : 3.9;
    double width = Width > 0.01 ? Width : 34.0;
    double depth = Depth > 0.01 ? Depth : 28.0;
    double twistDeg = Math.Abs(TwistDeg) > 0.001 ? TwistDeg : 210.0;
    double taper = Taper > 0.05 ? Math.Min(Taper, 1.5) : 0.72;
    double slabThick = SlabThick > 0.01 ? SlabThick : 0.35;
    double coreRadius = CoreRadius > 0.01 ? CoreRadius : 5.0;

    RhinoDoc doc = RhinoDoc.ActiveDoc;
    double tolerance = doc != null ? doc.ModelAbsoluteTolerance : 0.001;
    double totalHeight = floors * floorHeight;

    var cornerTracks = new List<List<Point3d>>();
    for (int c = 0; c < 4; c++)
      cornerTracks.Add(new List<Point3d>());

    for (int i = 0; i < floors; i++)
    {
      double t = floors == 1 ? 0.0 : (double)i / (double)(floors - 1);
      double z = i * floorHeight;
      double scale = Lerp(1.0, taper, t);
      double angle = RhinoMath.ToRadians(twistDeg * t);

      Point3d[] corners = RotatedRectangle(width * scale, depth * scale, angle, z);
      for (int c = 0; c < 4; c++)
        cornerTracks[c].Add(corners[c]);

      var loopPts = new List<Point3d>(corners);
      loopPts.Add(corners[0]);
      var loop = new PolylineCurve(loopPts);

      Surface slabSurface = Surface.CreateExtrusion(loop, Vector3d.ZAxis * slabThick);
      Brep openSlab = slabSurface != null ? slabSurface.ToBrep() : null;
      Brep cappedSlab = openSlab != null ? openSlab.CapPlanarHoles(tolerance) : null;
      if (cappedSlab != null)
        plates.Add(cappedSlab);
    }

    for (int c = 0; c < cornerTracks.Count; c++)
      rails.Add(new PolylineCurve(cornerTracks[c]));

    var coreCircle = new Circle(Plane.WorldXY, coreRadius).ToNurbsCurve();
    Surface coreSurface = Surface.CreateExtrusion(coreCircle, Vector3d.ZAxis * totalHeight);
    Brep openCore = coreSurface != null ? coreSurface.ToBrep() : null;
    core = openCore != null ? openCore.CapPlanarHoles(tolerance) : null;

    FloorPlates = plates;
    FacadeRails = rails;
    Core = core;
    Info = string.Format(
      "Spiral tower: {0} floors, {1:0.0} m height, {2:0.0} deg twist, units {3}",
      floors,
      totalHeight,
      twistDeg,
      doc != null ? doc.ModelUnitSystem.ToString() : "unknown");
  }

  private static double Lerp(double a, double b, double t)
  {
    return a + (b - a) * t;
  }

  private static Point3d[] RotatedRectangle(double width, double depth, double angle, double z)
  {
    double hw = width * 0.5;
    double hd = depth * 0.5;
    double ca = Math.Cos(angle);
    double sa = Math.Sin(angle);

    var local = new Point3d[]
    {
      new Point3d(-hw, -hd, z),
      new Point3d( hw, -hd, z),
      new Point3d( hw,  hd, z),
      new Point3d(-hw,  hd, z)
    };

    var world = new Point3d[4];
    for (int i = 0; i < local.Length; i++)
    {
      double x = local[i].X;
      double y = local[i].Y;
      world[i] = new Point3d(x * ca - y * sa, x * sa + y * ca, z);
    }

    return world;
  }
}
