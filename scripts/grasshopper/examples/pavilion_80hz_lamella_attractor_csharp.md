# Pavilion 80hz Lamella Attractor Generator

Grasshopper C# Script case for a simplified but controllable Pavilion 80hz-like
system:

- overall form is built from vertical generatrix curves;
- curve control points move toward or away from an attractor in the XZ plane;
- structural lamellas are thickened around each generatrix and shifted through Y
  so thickness is centered on the line;
- shingle anchor points are distributed in a checkerboard pattern:
  row 1 on lamellas 1, 3, 5; row 2 on lamellas 2, 4, 6; row 3 again on odd
  lamellas;
- each shingle is tangent to the source lamella and tilts outward from it by a
  controllable angle.

Practical defaults for a 1:1 millimeter model:

- `Width_mm = 5200`
- `Height_mm = 5100`
- `LamellaCount = 13`
- `Rows = 18`
- `AttractorStrength_mm = 520`
- `ShingleTiltDeg = 15`

Implementation note: this case intentionally keeps geometry as meshes for fast
Grasshopper iteration. Convert or bake selected meshes to Breps only when the
form is accepted.
