import Rhino

doc = Rhino.RhinoDoc.ActiveDoc

ids = [obj.Id for obj in doc.Objects]
for oid in ids:
    doc.Objects.Delete(oid, True)

for layer in doc.Layers:
    if layer is not None:
        layer.IsVisible = True
        layer.IsLocked = False

doc.Views.Redraw()
print("Deleted objects: %d" % len(ids))
