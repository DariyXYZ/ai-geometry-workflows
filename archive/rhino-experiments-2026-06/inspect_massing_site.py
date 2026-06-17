import Rhino
import scriptcontext as sc

for obj in sc.doc.Objects:
    layer = sc.doc.Layers[obj.Attributes.LayerIndex].Name
    geo = obj.Geometry
    bbox = geo.GetBoundingBox(True)
    print("OBJ|%s|%s|%s|%.3f,%.3f,%.3f|%.3f,%.3f,%.3f" % (
        str(obj.Id), layer, geo.ObjectType,
        bbox.Min.X, bbox.Min.Y, bbox.Min.Z,
        bbox.Max.X, bbox.Max.Y, bbox.Max.Z
    ))
    if layer == u"Участок застройки":
        crv = geo
        pts = []
        if isinstance(crv, Rhino.Geometry.PolylineCurve):
            pts = list(crv.ToPolyline())
        elif hasattr(crv, "Points"):
            for i in range(crv.Points.Count):
                pts.append(crv.Points[i].Location)
        if pts:
            print("SITE_POLY_COUNT|%d" % len(pts))
            for i, p in enumerate(pts):
                print("SITE_PT|%02d|%.3f|%.3f|%.3f" % (i, p.X, p.Y, p.Z))
        else:
            print("SITE_CURVE_NOT_POLYLINE")
