import scriptcontext as sc

show = set([
    "Default",
    u"Участок застройки",
    u"Высота здания",
    "TEP_Massing_V7_Unity_River_Cascade",
])

for layer in sc.doc.Layers:
    if layer is None:
        continue
    if layer.Name.startswith("TEP_Massing_") or layer.Name in show:
        layer.IsVisible = layer.Name in show

sc.doc.Views.Redraw()
print("Visible generated layer: TEP_Massing_V7_Unity_River_Cascade")
