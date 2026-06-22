#region Usings
using System;
using Rhino.Geometry;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;
#endregion

public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(object x, object y, ref object a)
  {
    double xValue;
    double yValue;

    if (!TryReadDouble(x, out xValue))
      xValue = 3.5;

    if (!TryReadDouble(y, out yValue))
      yValue = 7.25;

    double zValue = xValue + yValue;
    a = new Point3d(xValue, yValue, zValue);

    Print(string.Format(
      "Point from sliders: X={0:0.###}, Y={1:0.###}, Z=X+Y={2:0.###}",
      xValue,
      yValue,
      zValue));
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
