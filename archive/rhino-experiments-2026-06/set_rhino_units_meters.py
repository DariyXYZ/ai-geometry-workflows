import Rhino
import scriptcontext as sc

sc.doc.ModelUnitSystem = Rhino.UnitSystem.Meters
sc.doc.PageUnitSystem = Rhino.UnitSystem.Meters
sc.doc.ModelAbsoluteTolerance = 0.001
sc.doc.ModelAngleToleranceRadians = 0.017453292519943295
sc.doc.Views.Redraw()

print("Units set to meters")
