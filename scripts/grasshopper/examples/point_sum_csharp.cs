#region Usings
using System;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
#endregion

public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(double X, double Y, double Z, ref object Point, ref object Sum, ref object Info)
  {
    Point3d p = new Point3d(X, Y, Z);
    double sum = X + Y + Z;

    Point = p;
    Sum = sum;
    Info = string.Format(
      "Rhino {0}; units={1}; point=({2:0.###}, {3:0.###}, {4:0.###}); sum={5:0.###}",
      RhinoApp.Version,
      RhinoDoc.ActiveDoc != null ? RhinoDoc.ActiveDoc.ModelUnitSystem.ToString() : "unknown",
      p.X,
      p.Y,
      p.Z,
      sum
    );
  }
}
