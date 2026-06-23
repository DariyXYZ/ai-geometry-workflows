#region Usings
using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper.Kernel;
#endregion

// Quick Architecture Snippet: Building Metrics / TEP
// Target: Rhino 8 C# Script component, C# 9-compatible.
// Inputs: Masses, FloorAreas, SiteArea, FloorHeight, Efficiency, ParkingRatio
// Outputs: GrossFloorArea, NetFloorArea, FAR, BuildingHeight, EstimatedFloors,
//          FootprintArea, GrossVolume, Report
public class Script_Instance : GH_ScriptInstance
{
  private void RunScript(
    List<Brep> Masses,
    List<double> FloorAreas,
    double SiteArea,
    double FloorHeight,
    double Efficiency,
    double ParkingRatio,
    ref object GrossFloorArea,
    ref object NetFloorArea,
    ref object FAR,
    ref object BuildingHeight,
    ref object EstimatedFloors,
    ref object FootprintArea,
    ref object GrossVolume,
    ref object Report)
  {
    var report = new List<string>();
    GrossFloorArea = 0.0;
    NetFloorArea = 0.0;
    FAR = 0.0;
    BuildingHeight = 0.0;
    EstimatedFloors = 0;
    FootprintArea = 0.0;
    GrossVolume = 0.0;
    Report = report;

    double floorHeight = FloorHeight > 0.01 ? FloorHeight : 3.9;
    double efficiency = Efficiency > 0.0 ? Math.Min(Efficiency, 1.0) : 0.82;
    double parkingRatio = ParkingRatio > 0.0 ? ParkingRatio : 0.0;

    bool hasFloorAreas = FloorAreas != null && FloorAreas.Count > 0;
    double gfa = 0.0;
    if (hasFloorAreas)
    {
      for (int i = 0; i < FloorAreas.Count; i++)
        if (FloorAreas[i] > 0.0)
          gfa += FloorAreas[i];
    }

    BoundingBox union = BoundingBox.Empty;
    double volume = 0.0;
    if (Masses != null)
    {
      for (int i = 0; i < Masses.Count; i++)
      {
        Brep mass = Masses[i];
        if (mass == null)
          continue;

        BoundingBox bb = mass.GetBoundingBox(true);
        if (bb.IsValid)
          union.Union(bb);

        VolumeMassProperties vmp = VolumeMassProperties.Compute(mass);
        if (vmp != null)
          volume += vmp.Volume;
      }
    }

    double height = union.IsValid ? union.Max.Z - union.Min.Z : 0.0;
    double footprint = union.IsValid ? (union.Max.X - union.Min.X) * (union.Max.Y - union.Min.Y) : 0.0;
    int floors = Math.Max(0, (int)Math.Floor(height / floorHeight));

    if (!hasFloorAreas && footprint > 0.0 && floors > 0)
      gfa = footprint * floors;

    double net = gfa * efficiency;
    double far = SiteArea > 0.0 ? gfa / SiteArea : 0.0;
    double parkingDemand = parkingRatio > 0.0 ? gfa * parkingRatio : 0.0;

    report.Add(hasFloorAreas ? "gfa_source: floor areas" : "gfa_source: bbox estimate");
    report.Add(string.Format("building_height_m: {0:0.##}", height));
    report.Add(string.Format("estimated_floors: {0}", floors));
    report.Add(string.Format("footprint_area_m2: {0:0.##}", footprint));
    report.Add(string.Format("gross_floor_area_m2: {0:0.##}", gfa));
    report.Add(string.Format("net_area_m2: {0:0.##}", net));
    report.Add(SiteArea > 0.0 ? string.Format("far: {0:0.###}", far) : "far: no site area");
    report.Add(string.Format("gross_volume_m3: {0:0.##}", volume));
    if (parkingRatio > 0.0)
      report.Add(string.Format("parking_metric: {0:0.##}", parkingDemand));

    GrossFloorArea = gfa;
    NetFloorArea = net;
    FAR = far;
    BuildingHeight = height;
    EstimatedFloors = floors;
    FootprintArea = footprint;
    GrossVolume = volume;
    Report = report;
  }
}
