using System;
using System.Collections.Generic;
using Rhino;
using Rhino.DocObjects;
using Rhino.Geometry;

public static class QuickArchitectureSnippetsSmoke
{
  public static void Run(RhinoDoc doc)
  {
    if (doc == null)
      throw new ArgumentNullException("doc");

    if (doc.ModelUnitSystem != UnitSystem.Meters)
      doc.AdjustModelUnitSystem(UnitSystem.Meters, false);

    string prefix = "GH_SNIPPET_SMOKE";
    DeleteObjectsByPrefix(doc, prefix);

    int massLayer = EnsureLayer(doc, prefix + "_massing");
    int floorLayer = EnsureLayer(doc, prefix + "_floors");
    int coreLayer = EnsureLayer(doc, prefix + "_core");
    int textLayer = EnsureLayer(doc, prefix + "_metrics");

    double width = 36.0;
    double depth = 28.0;
    double height = 78.0;
    double floorHeight = 3.9;
    double slabThickness = 0.30;
    double siteArea = 4200.0;
    double efficiency = 0.82;

    Brep mass = BoxBrep(width, depth, height);
    var massAttr = Attr(prefix + "_massing_box", massLayer);
    doc.Objects.AddBrep(mass, massAttr);

    var floorAreas = new List<double>();
    int floors = Math.Max(1, (int)Math.Floor(height / floorHeight));
    double gfa = 0.0;
    for (int i = 0; i < floors; i++)
    {
      double z = i * floorHeight;
      Curve outline = RectCurve(width, depth, z);
      Surface slabSurface = Surface.CreateExtrusion(outline, Vector3d.ZAxis * slabThickness);
      Brep openSlab = slabSurface != null ? slabSurface.ToBrep() : null;
      Brep slab = openSlab != null ? openSlab.CapPlanarHoles(doc.ModelAbsoluteTolerance) : null;
      if (slab != null)
        doc.Objects.AddBrep(slab, Attr(prefix + "_floor_" + (i + 1).ToString("00"), floorLayer));
      floorAreas.Add(width * depth);
      gfa += width * depth;
    }

    Curve coreCircle = new Circle(Plane.WorldXY, 4.2).ToNurbsCurve();
    Surface coreSurface = Surface.CreateExtrusion(coreCircle, Vector3d.ZAxis * height);
    Brep openCore = coreSurface != null ? coreSurface.ToBrep() : null;
    Brep core = openCore != null ? openCore.CapPlanarHoles(doc.ModelAbsoluteTolerance) : null;
    if (core != null)
      doc.Objects.AddBrep(core, Attr(prefix + "_core", coreLayer));

    double net = gfa * efficiency;
    double far = gfa / siteArea;
    string text = string.Format(
      "Quick architecture snippets smoke\\nFloors: {0}\\nHeight: {1:0.#} m\\nGFA: {2:0.#} m2\\nNet: {3:0.#} m2\\nFAR: {4:0.###}",
      floors,
      height,
      gfa,
      net,
      far);

    var entity = new TextEntity();
    entity.Plane = new Plane(new Point3d(-width * 0.5, depth * 0.5 + 8.0, 4.0), Vector3d.ZAxis);
    entity.PlainText = text;
    entity.TextHeight = 2.2;
    doc.Objects.AddText(entity, Attr(prefix + "_metrics_text", textLayer));

    doc.Views.Redraw();
    RhinoApp.WriteLine(string.Format("GH_SNIPPET_SMOKE OK floors={0} height={1} gfa={2} far={3:0.###}", floors, height, gfa, far));
  }

  private static Brep BoxBrep(double width, double depth, double height)
  {
    var box = new Box(
      Plane.WorldXY,
      new Interval(-width * 0.5, width * 0.5),
      new Interval(-depth * 0.5, depth * 0.5),
      new Interval(0.0, height));
    return box.ToBrep();
  }

  private static Curve RectCurve(double width, double depth, double z)
  {
    double hw = width * 0.5;
    double hd = depth * 0.5;
    var pts = new List<Point3d>
    {
      new Point3d(-hw, -hd, z),
      new Point3d( hw, -hd, z),
      new Point3d( hw,  hd, z),
      new Point3d(-hw,  hd, z),
      new Point3d(-hw, -hd, z)
    };
    return new PolylineCurve(pts);
  }

  private static ObjectAttributes Attr(string name, int layerIndex)
  {
    var attr = new ObjectAttributes();
    attr.Name = name;
    attr.LayerIndex = layerIndex;
    return attr;
  }

  private static int EnsureLayer(RhinoDoc doc, string name)
  {
    int existing = doc.Layers.FindName(name) != null ? doc.Layers.FindName(name).Index : -1;
    if (existing >= 0)
      return existing;
    var layer = new Layer();
    layer.Name = name;
    return doc.Layers.Add(layer);
  }

  private static void DeleteObjectsByPrefix(RhinoDoc doc, string prefix)
  {
    var ids = new List<Guid>();
    foreach (RhinoObject obj in doc.Objects)
    {
      if (obj == null || obj.Attributes == null || string.IsNullOrEmpty(obj.Attributes.Name))
        continue;
      if (obj.Attributes.Name.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
        ids.Add(obj.Id);
    }

    for (int i = 0; i < ids.Count; i++)
      doc.Objects.Delete(ids[i], true);
  }
}

QuickArchitectureSnippetsSmoke.Run(__rhino_doc__);
