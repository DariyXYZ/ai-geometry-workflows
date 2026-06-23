#region Usings
using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
#endregion

// Quick Architecture Snippet: BBox Floorizer
// Target: Rhino 8 C# Script component, C# 9-compatible.
// Inputs: Massing, FloorHeight, SlabThickness, Inset, Efficiency, SiteArea
// Outputs: FloorPlates, FloorOutlines, FloorAreas, Metrics, Info
// Note: This is schematic. It uses the massing bounding box, not exact contours.
public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(
    Brep Massing,
    double FloorHeight,
    double SlabThickness,
    double Inset,
    double Efficiency,
    double SiteArea,
    ref object FloorPlates,
    ref object FloorOutlines,
    ref object FloorAreas,
    ref object Metrics,
    ref object Info)
  {
    var plates = new List<Brep>();
    var outlines = new List<Curve>();
    var areas = new List<double>();
    var report = new List<string>();

    FloorPlates = plates;
    FloorOutlines = outlines;
    FloorAreas = areas;
    Metrics = report;
    Info = "Connect a massing Brep.";

    if (Massing == null)
      return;

    RhinoDoc doc = RhinoDoc.ActiveDoc;
    double tol = doc != null ? doc.ModelAbsoluteTolerance : 0.001;
    double floorHeight = FloorHeight > 0.01 ? FloorHeight : 3.9;
    double slabThickness = SlabThickness > 0.01 ? SlabThickness : 0.30;
    double inset = Math.Max(0.0, Inset);
    double efficiency = Efficiency > 0.0 ? Math.Min(Efficiency, 1.0) : 0.82;

    BoundingBox bbox = Massing.GetBoundingBox(true);
    if (!bbox.IsValid)
    {
      Info = "Invalid massing bounding box.";
      return;
    }

    double width = Math.Max(0.0, bbox.Max.X - bbox.Min.X - inset * 2.0);
    double depth = Math.Max(0.0, bbox.Max.Y - bbox.Min.Y - inset * 2.0);
    double height = Math.Max(0.0, bbox.Max.Z - bbox.Min.Z);
    int floors = Math.Max(1, (int)Math.Floor(height / floorHeight));
    double grossArea = width * depth;

    for (int i = 0; i < floors; i++)
    {
      double z = bbox.Min.Z + i * floorHeight;
      var pts = new List<Point3d>
      {
        new Point3d(bbox.Min.X + inset, bbox.Min.Y + inset, z),
        new Point3d(bbox.Max.X - inset, bbox.Min.Y + inset, z),
        new Point3d(bbox.Max.X - inset, bbox.Max.Y - inset, z),
        new Point3d(bbox.Min.X + inset, bbox.Max.Y - inset, z),
        new Point3d(bbox.Min.X + inset, bbox.Min.Y + inset, z)
      };

      var outline = new PolylineCurve(pts);
      outlines.Add(outline);
      areas.Add(grossArea);

      Surface slabSurface = Surface.CreateExtrusion(outline, Vector3d.ZAxis * slabThickness);
      Brep openSlab = slabSurface != null ? slabSurface.ToBrep() : null;
      Brep cappedSlab = openSlab != null ? openSlab.CapPlanarHoles(tol) : null;
      if (cappedSlab != null)
        plates.Add(cappedSlab);
    }

    double gfa = grossArea * floors;
    double netArea = gfa * efficiency;
    double far = SiteArea > 0.0 ? gfa / SiteArea : 0.0;

    report.Add("method: bbox schematic floorizer");
    report.Add(string.Format("floors: {0}", floors));
    report.Add(string.Format("height_m: {0:0.##}", height));
    report.Add(string.Format("floor_height_m: {0:0.##}", floorHeight));
    report.Add(string.Format("plate_m: {0:0.##} x {1:0.##}", width, depth));
    report.Add(string.Format("gross_floor_area_m2: {0:0.##}", gfa));
    report.Add(string.Format("net_area_m2_at_efficiency: {0:0.##}", netArea));
    if (SiteArea > 0.0)
      report.Add(string.Format("far: {0:0.###}", far));
    else
      report.Add("far: no site area");

    Info = string.Format(
      "BBox floorizer: {0} floors, {1:0.#} m high, GFA {2:0.#} m2",
      floors,
      height,
      gfa);

    FloorPlates = plates;
    FloorOutlines = outlines;
    FloorAreas = areas;
    Metrics = report;
  }
}
