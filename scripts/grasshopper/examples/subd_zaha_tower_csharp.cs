#region Usings
using System;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;
#endregion

public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(object x, object y, ref object a)
  {
    double height;
    double twistDeg;

    if (!TryReadDouble(x, out height))
      height = 180.0;

    if (!TryReadDouble(y, out twistDeg))
      twistDeg = 255.0;

    int rings = 34;
    int sides = 28;
    double baseRadiusX = 22.0;
    double baseRadiusY = 15.0;

    Mesh mesh = BuildTowerMesh(rings, sides, height, twistDeg, baseRadiusX, baseRadiusY);
    SubD subd = SubD.CreateFromMesh(mesh);

    a = subd != null ? (object)subd : mesh;
    Print(string.Format(
      "SubD tower: height={0:0.0}m, twist={1:0.0}deg, rings={2}, sides={3}, output={4}",
      height,
      twistDeg,
      rings,
      sides,
      subd != null ? "SubD" : "Mesh fallback"));
  }

  private static Mesh BuildTowerMesh(int rings, int sides, double height, double twistDeg, double rx, double ry)
  {
    var mesh = new Mesh();

    for (int i = 0; i < rings; i++)
    {
      double t = (double)i / (double)(rings - 1);
      double z = height * t;

      double taper = 1.0 - 0.34 * t;
      double waist = 1.0 - 0.22 * Math.Exp(-Math.Pow((t - 0.48) / 0.19, 2.0));
      double crownFlare = 1.0 + 0.11 * Math.Exp(-Math.Pow((t - 0.88) / 0.10, 2.0));
      double breathing = 1.0 + 0.045 * Math.Sin(2.0 * Math.PI * (t * 3.0 + 0.12));
      double angleOffset = RhinoMath.ToRadians(twistDeg * Smooth01(t));

      for (int j = 0; j < sides; j++)
      {
        double u = (double)j / (double)sides;
        double angle = 2.0 * Math.PI * u + angleOffset;

        double lobe = 1.0 + 0.10 * Math.Sin(3.0 * angle + 2.5 * Math.PI * t);
        double pinch = 1.0 - 0.08 * Math.Cos(2.0 * angle - 1.2 * Math.PI * t);

        double localRx = rx * taper * waist * crownFlare * breathing * lobe;
        double localRy = ry * taper * waist * crownFlare * breathing * pinch;

        mesh.Vertices.Add(localRx * Math.Cos(angle), localRy * Math.Sin(angle), z);
      }
    }

    for (int i = 0; i < rings - 1; i++)
    {
      for (int j = 0; j < sides; j++)
      {
        int a = i * sides + j;
        int b = i * sides + (j + 1) % sides;
        int c = (i + 1) * sides + (j + 1) % sides;
        int d = (i + 1) * sides + j;
        mesh.Faces.AddFace(a, b, c, d);
      }
    }

    int bottomCenter = mesh.Vertices.Count;
    mesh.Vertices.Add(0.0, 0.0, 0.0);
    for (int j = 0; j < sides; j++)
      mesh.Faces.AddFace(bottomCenter, (j + 1) % sides, j);

    int topCenter = mesh.Vertices.Count;
    mesh.Vertices.Add(0.0, 0.0, height);
    int topStart = (rings - 1) * sides;
    for (int j = 0; j < sides; j++)
      mesh.Faces.AddFace(topCenter, topStart + j, topStart + (j + 1) % sides);

    mesh.Normals.ComputeNormals();
    mesh.Compact();
    return mesh;
  }

  private static double Smooth01(double t)
  {
    return t * t * (3.0 - 2.0 * t);
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

    var ghNumber = value as GH_Number;
    if (ghNumber != null)
    {
      number = ghNumber.Value;
      return true;
    }

    return double.TryParse(value.ToString(), out number);
  }
}
