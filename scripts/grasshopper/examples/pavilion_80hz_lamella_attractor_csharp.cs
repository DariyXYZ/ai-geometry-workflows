#region Usings
using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
#endregion

public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(
    double Width_mm,
    double Height_mm,
    int LamellaCount,
    int Rows,
    int CurveSamples,
    double AttractorX_mm,
    double AttractorZ_mm,
    double AttractorStrength_mm,
    double LamellaDepth_mm,
    double LamellaYThickness_mm,
    double ShingleWidth_mm,
    double ShingleHeight_mm,
    double ShingleThickness_mm,
    double ShingleTiltDeg,
    double ShingleStandOff_mm,
    double TopBeamDepth_mm,
    ref object Log,
    ref object LamellaCurves,
    ref object LamellaMeshes,
    ref object AnchorPoints,
    ref object ShingleMeshes,
    ref object TopBeamMesh,
    ref object GuideCurves)
  {
    double width = Fallback(Width_mm, 5200.0);
    double height = Fallback(Height_mm, 5100.0);
    int lamellaCount = MakeOdd(Clamp(LamellaCount, 13, 3, 41));
    int rows = Clamp(Rows, 18, 3, 60);
    int samples = Clamp(CurveSamples, 9, 4, 30);

    var curves = new List<Curve>();
    var lamellaMeshes = new List<Mesh>();
    var anchors = new List<Point3d>();
    var shingles = new List<Mesh>();
    var guides = new List<Curve>();

    for (int i = 0; i < lamellaCount; i++)
    {
      double u = lamellaCount == 1 ? 0.5 : (double)i / (double)(lamellaCount - 1);
      double baseX = -width * 0.5 + width * u;
      var pts = new List<Point3d>();

      for (int s = 0; s < samples; s++)
      {
        double t = samples == 1 ? 0.0 : (double)s / (double)(samples - 1);
        double z = height * t;
        double dx = baseX - AttractorX_mm;
        double dz = z - AttractorZ_mm;
        double dist = Math.Sqrt(dx * dx + dz * dz);
        double sigma = Math.Max(width, height) * 0.33;
        double falloff = Math.Exp(-(dist * dist) / (2.0 * sigma * sigma));
        double verticalPin = Math.Sin(Math.PI * t);
        double dir = dx >= 0.0 ? 1.0 : -1.0;
        double x = baseX + dir * AttractorStrength_mm * falloff * verticalPin;
        pts.Add(new Point3d(x, 0.0, z));
      }

      Curve curve = Curve.CreateInterpolatedCurve(pts, 3);
      if (curve == null) curve = new PolylineCurve(pts);
      curves.Add(curve);
      lamellaMeshes.Add(BuildLamellaMesh(curve, samples * 3, LamellaDepth_mm, LamellaYThickness_mm));
    }

    for (int r = 0; r < rows; r++)
    {
      double t = (r + 0.5) / rows;
      int start = (r % 2 == 0) ? 0 : 1;

      for (int i = start; i < lamellaCount; i += 2)
      {
        Point3d p;
        Vector3d tangent;
        if (!EvalAtNormalizedLength(curves[i], t, out p, out tangent)) continue;
        anchors.Add(p);
        shingles.Add(BuildShingleMesh(
          p,
          tangent,
          LamellaDepth_mm + ShingleStandOff_mm,
          ShingleWidth_mm,
          ShingleHeight_mm,
          ShingleThickness_mm,
          ShingleTiltDeg));
      }
    }

    var basePts = new List<Point3d>();
    var topPts = new List<Point3d>();
    for (int i = 0; i < lamellaCount; i++)
    {
      Point3d p0;
      Point3d p1;
      Vector3d tangent;
      EvalAtNormalizedLength(curves[i], 0.0, out p0, out tangent);
      EvalAtNormalizedLength(curves[i], 1.0, out p1, out tangent);
      basePts.Add(p0);
      topPts.Add(p1);
    }

    guides.Add(new PolylineCurve(basePts));
    guides.Add(new PolylineCurve(topPts));

    Log = string.Format(
      "Pavilion_80hz lamella attractor: {0} lamellas, {1} rows, {2} checkerboard shingles, {3:0.0} deg tilt.",
      lamellaCount,
      rows,
      shingles.Count,
      ShingleTiltDeg);
    LamellaCurves = curves;
    LamellaMeshes = lamellaMeshes;
    AnchorPoints = anchors;
    ShingleMeshes = shingles;
    TopBeamMesh = BuildTopBeamMesh(topPts, LamellaYThickness_mm * 1.8, TopBeamDepth_mm);
    GuideCurves = guides;
  }

  private double Fallback(double value, double fallback)
  {
    if (double.IsNaN(value) || double.IsInfinity(value) || Math.Abs(value) < RhinoMath.ZeroTolerance)
      return fallback;
    return value;
  }

  private int Clamp(int value, int fallback, int min, int max)
  {
    if (value == 0) value = fallback;
    return Math.Max(min, Math.Min(max, value));
  }

  private int MakeOdd(int value)
  {
    return value % 2 == 0 ? value + 1 : value;
  }

  private bool EvalAtNormalizedLength(Curve curve, double t, out Point3d point, out Vector3d tangent)
  {
    point = Point3d.Unset;
    tangent = Vector3d.ZAxis;
    if (curve == null) return false;

    double length = curve.GetLength();
    double parameter;
    if (length <= RhinoMath.ZeroTolerance ||
      !curve.LengthParameter(length * Math.Max(0.0, Math.Min(1.0, t)), out parameter))
    {
      parameter = curve.Domain.ParameterAt(Math.Max(0.0, Math.Min(1.0, t)));
    }

    point = curve.PointAt(parameter);
    tangent = curve.TangentAt(parameter);
    if (!tangent.Unitize()) tangent = Vector3d.ZAxis;
    return true;
  }

  private Vector3d OutwardNormal(Vector3d tangent)
  {
    Vector3d normal = Vector3d.CrossProduct(Vector3d.YAxis, tangent);
    if (!normal.Unitize()) normal = Vector3d.XAxis;
    return normal;
  }

  private Mesh BuildLamellaMesh(Curve curve, int stations, double depth, double yThickness)
  {
    var mesh = new Mesh();
    if (curve == null) return mesh;
    stations = Math.Max(2, stations);

    for (int i = 0; i < stations; i++)
    {
      Point3d p;
      Vector3d tangent;
      EvalAtNormalizedLength(curve, (double)i / (stations - 1), out p, out tangent);
      Vector3d normal = OutwardNormal(tangent);
      Vector3d halfY = Vector3d.YAxis * (yThickness * 0.5);
      int v = mesh.Vertices.Count;

      mesh.Vertices.Add(p - halfY);
      mesh.Vertices.Add(p + halfY);
      mesh.Vertices.Add(p + normal * depth + halfY);
      mesh.Vertices.Add(p + normal * depth - halfY);

      if (i > 0)
      {
        int a = v - 4;
        mesh.Faces.AddFace(a, a + 1, v + 1, v);
        mesh.Faces.AddFace(a + 1, a + 2, v + 2, v + 1);
        mesh.Faces.AddFace(a + 2, a + 3, v + 3, v + 2);
        mesh.Faces.AddFace(a + 3, a, v, v + 3);
      }
    }

    int last = mesh.Vertices.Count - 4;
    mesh.Faces.AddFace(0, 1, 2, 3);
    mesh.Faces.AddFace(last, last + 3, last + 2, last + 1);
    mesh.Normals.ComputeNormals();
    mesh.Compact();
    return mesh;
  }

  private Mesh BuildShingleMesh(
    Point3d anchor,
    Vector3d tangent,
    double outwardOffset,
    double widthY,
    double heightAlong,
    double thickness,
    double tiltDeg)
  {
    var mesh = new Mesh();
    if (!tangent.Unitize()) tangent = Vector3d.ZAxis;

    Vector3d outward = OutwardNormal(tangent);
    Vector3d halfY = Vector3d.YAxis * (widthY * 0.5);
    Vector3d thick = outward * thickness;
    double bottomKick = Math.Tan(RhinoMath.ToRadians(tiltDeg)) * heightAlong;

    Point3d top = anchor + outward * outwardOffset - tangent * (heightAlong * 0.45);
    Point3d bottom = anchor + outward * (outwardOffset + bottomKick) + tangent * (heightAlong * 0.55);

    Point3d a = top - halfY;
    Point3d b = top + halfY;
    Point3d c = bottom + halfY;
    Point3d d = bottom - halfY;
    Point3d a2 = a + thick;
    Point3d b2 = b + thick;
    Point3d c2 = c + thick;
    Point3d d2 = d + thick;

    mesh.Vertices.Add(a); mesh.Vertices.Add(b); mesh.Vertices.Add(c); mesh.Vertices.Add(d);
    mesh.Vertices.Add(a2); mesh.Vertices.Add(b2); mesh.Vertices.Add(c2); mesh.Vertices.Add(d2);
    mesh.Faces.AddFace(0, 1, 2, 3);
    mesh.Faces.AddFace(4, 7, 6, 5);
    mesh.Faces.AddFace(0, 4, 5, 1);
    mesh.Faces.AddFace(1, 5, 6, 2);
    mesh.Faces.AddFace(2, 6, 7, 3);
    mesh.Faces.AddFace(3, 7, 4, 0);
    mesh.Normals.ComputeNormals();
    mesh.Compact();
    return mesh;
  }

  private Mesh BuildTopBeamMesh(List<Point3d> topPts, double yThickness, double depth)
  {
    var mesh = new Mesh();
    if (topPts == null || topPts.Count < 2) return mesh;

    for (int i = 0; i < topPts.Count; i++)
    {
      Vector3d tangent = i == 0
        ? topPts[1] - topPts[0]
        : i == topPts.Count - 1
          ? topPts[i] - topPts[i - 1]
          : topPts[i + 1] - topPts[i - 1];
      if (!tangent.Unitize()) tangent = Vector3d.XAxis;

      Vector3d outward = Vector3d.CrossProduct(Vector3d.YAxis, tangent);
      if (!outward.Unitize()) outward = Vector3d.XAxis;
      Vector3d halfY = Vector3d.YAxis * (yThickness * 0.5);
      Point3d p = topPts[i] + Vector3d.ZAxis * (depth * 0.45);
      int v = mesh.Vertices.Count;

      mesh.Vertices.Add(p - halfY);
      mesh.Vertices.Add(p + halfY);
      mesh.Vertices.Add(p + outward * depth + halfY);
      mesh.Vertices.Add(p + outward * depth - halfY);

      if (i > 0)
      {
        int a = v - 4;
        mesh.Faces.AddFace(a, a + 1, v + 1, v);
        mesh.Faces.AddFace(a + 1, a + 2, v + 2, v + 1);
        mesh.Faces.AddFace(a + 2, a + 3, v + 3, v + 2);
        mesh.Faces.AddFace(a + 3, a, v, v + 3);
      }
    }

    int last = mesh.Vertices.Count - 4;
    mesh.Faces.AddFace(0, 1, 2, 3);
    mesh.Faces.AddFace(last, last + 3, last + 2, last + 1);
    mesh.Normals.ComputeNormals();
    mesh.Compact();
    return mesh;
  }
}
