from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_CLIENT = Path(
    os.environ.get(
        "AUROX_CLIENT",
        r"C:\Users\dariy.n\.codex\skills\rhino-aurox-modeling\scripts\rhino_aurox_client.py",
    )
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run native RhinoCommon helper operations through Aurox execute_csharp."
    )
    parser.add_argument("--client", default=str(DEFAULT_CLIENT), help="Path to rhino_aurox_client.py.")
    parser.add_argument("--dry-run", action="store_true", help="Print generated C# instead of executing it.")
    sub = parser.add_subparsers(required=True)

    sub.add_parser("list-ops", help="List built-in helper operations.").set_defaults(func=cmd_list_ops)

    run = sub.add_parser("run-csharp", help="Execute a C# file inside the active Rhino document.")
    run.add_argument("file", help="C# file to execute.")
    run.set_defaults(func=cmd_run_csharp)

    visible = sub.add_parser("read-visible-curves", help="Print visible Rhino curve objects and bbox data.")
    visible.set_defaults(func=cmd_read_visible_curves)

    soft = sub.add_parser("make-soft-closed-curve", help="Create a closed NURBS/control-point curve from JSON points.")
    soft.add_argument("--points", required=True, help="JSON list of [x,y,z] points or path to JSON file.")
    soft.add_argument("--degree", type=int, default=3)
    soft.add_argument("--layer", default="RC_HELPER_curves")
    soft.add_argument("--name", default="rc_helper_soft_closed_curve")
    soft.set_defaults(func=cmd_make_soft_closed_curve)

    diff = sub.add_parser(
        "curve-difference-2d",
        help="Create a 2D curve boolean difference: boundary minus cutter. Inputs are JSON point loops.",
    )
    diff.add_argument("--boundary", required=True, help="JSON list of [x,y,z] points or path to JSON file.")
    diff.add_argument("--cutter", required=True, help="JSON list of [x,y,z] points or path to JSON file.")
    diff.add_argument("--layer", default="RC_HELPER_curves")
    diff.add_argument("--name", default="rc_helper_curve_difference")
    diff.set_defaults(func=cmd_curve_difference_2d)

    contour = sub.add_parser("contour-brep", help="Contour a Brep by interval along Z.")
    contour.add_argument("--object-id", required=True)
    contour.add_argument("--z-min", type=float, required=True)
    contour.add_argument("--z-max", type=float, required=True)
    contour.add_argument("--interval", type=float, required=True)
    contour.add_argument("--layer", default="RC_HELPER_contours")
    contour.add_argument("--name", default="rc_helper_contour")
    contour.set_defaults(func=cmd_contour_brep)

    args = parser.parse_args(argv)
    return args.func(args)


def cmd_list_ops(args: argparse.Namespace) -> int:
    print(
        "\n".join(
            [
                "read-visible-curves",
                "make-soft-closed-curve",
                "curve-difference-2d",
                "contour-brep",
                "run-csharp",
            ]
        )
    )
    return 0


def cmd_run_csharp(args: argparse.Namespace) -> int:
    code = Path(args.file).read_text(encoding="utf-8")
    return execute(args, code)


def cmd_read_visible_curves(args: argparse.Namespace) -> int:
    return execute(args, READ_VISIBLE_CURVES)


def cmd_make_soft_closed_curve(args: argparse.Namespace) -> int:
    points = read_points(args.points)
    if len(points) < 4:
        raise SystemExit("Need at least 4 points for a closed control curve.")
    code = COMMON_PREAMBLE + f"""
var points = new List<Point3d> {{ {point_list_literal(points, close=True)} }};
var curve = Curve.CreateControlPointCurve(points, {int(args.degree)});
if (curve == null)
{{
    output.AppendLine("FAIL curve=null");
    return;
}}
var layer = EnsureLayer(doc, {cs_string(args.layer)}, System.Drawing.Color.Magenta);
var attr = new ObjectAttributes();
attr.LayerIndex = layer;
attr.Name = {cs_string(args.name)};
var id = doc.Objects.AddCurve(curve, attr);
doc.Views.Redraw();
output.AppendLine("OK soft_closed_curve id=" + id.ToString());
output.AppendLine("points=" + points.Count.ToString() + " degree={int(args.degree)}");
"""
    return execute(args, code)


def cmd_curve_difference_2d(args: argparse.Namespace) -> int:
    boundary = read_points(args.boundary)
    cutter = read_points(args.cutter)
    if len(boundary) < 4 or len(cutter) < 4:
        raise SystemExit("Boundary and cutter both need at least 4 points.")
    code = COMMON_PREAMBLE + f"""
var boundary = new PolylineCurve(new List<Point3d> {{ {point_list_literal(boundary, close=True)} }});
var cutter = new PolylineCurve(new List<Point3d> {{ {point_list_literal(cutter, close=True)} }});
var boundaryCrv = boundary.ToNurbsCurve();
var cutterCrv = cutter.ToNurbsCurve();
var result = Curve.CreateBooleanDifference(boundaryCrv, cutterCrv, doc.ModelAbsoluteTolerance);
if (result == null || result.Length == 0)
{{
    output.AppendLine("FAIL curve_boolean_difference produced no curves");
    return;
}}
var layer = EnsureLayer(doc, {cs_string(args.layer)}, System.Drawing.Color.Magenta);
int n = 0;
foreach (var crv in result)
{{
    var attr = new ObjectAttributes();
    attr.LayerIndex = layer;
    attr.Name = {cs_string(args.name)} + "_" + n.ToString("00");
    var id = doc.Objects.AddCurve(crv, attr);
    output.AppendLine("OK curve_difference id=" + id.ToString());
    n++;
}}
doc.Views.Redraw();
output.AppendLine("curves=" + n.ToString());
"""
    return execute(args, code)


def cmd_contour_brep(args: argparse.Namespace) -> int:
    code = COMMON_PREAMBLE + f"""
Guid objectId = new Guid({cs_string(args.object_id)});
var rhObj = doc.Objects.FindId(objectId);
if (rhObj == null)
{{
    output.AppendLine("FAIL object not found");
    return;
}}
var brep = rhObj.Geometry as Brep;
if (brep == null)
{{
    output.AppendLine("FAIL object is not Brep");
    return;
}}
var start = new Point3d(0, 0, {float(args.z_min)});
var end = new Point3d(0, 0, {float(args.z_max)});
var contours = Brep.CreateContourCurves(brep, start, end, {float(args.interval)});
if (contours == null || contours.Length == 0)
{{
    output.AppendLine("FAIL contour produced no curves");
    return;
}}
var layer = EnsureLayer(doc, {cs_string(args.layer)}, System.Drawing.Color.Orange);
int n = 0;
foreach (var crv in contours)
{{
    var attr = new ObjectAttributes();
    attr.LayerIndex = layer;
    attr.Name = {cs_string(args.name)} + "_" + n.ToString("000");
    var id = doc.Objects.AddCurve(crv, attr);
    output.AppendLine("OK contour id=" + id.ToString());
    n++;
}}
doc.Views.Redraw();
output.AppendLine("contours=" + n.ToString());
"""
    return execute(args, code)


def execute(args: argparse.Namespace, code: str) -> int:
    if args.dry_run:
        print(code)
        return 0
    result = call_aurox(Path(args.client), "execute_csharp", {"code": code})
    if isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)
    return 0


def call_aurox(client: Path, command: str, params: dict[str, Any]) -> Any:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as fh:
        json.dump(params, fh)
        params_file = fh.name
    try:
        proc = subprocess.run(
            [sys.executable, str(client), "call", command, "--params-file", params_file],
            text=True,
            capture_output=True,
        )
    finally:
        os.unlink(params_file)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr[-2000:])
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.stdout


def read_points(value: str) -> list[list[float]]:
    path = Path(value)
    text = path.read_text(encoding="utf-8") if path.exists() else value
    data = json.loads(text)
    if not isinstance(data, list):
        raise SystemExit("Points must be a JSON list.")
    points = []
    for point in data:
        if not isinstance(point, (list, tuple)) or len(point) not in (2, 3):
            raise SystemExit("Each point must be [x,y] or [x,y,z].")
        z = 0.0 if len(point) == 2 else float(point[2])
        points.append([float(point[0]), float(point[1]), z])
    return points


def point_list_literal(points: list[list[float]], close: bool) -> str:
    pts = points[:]
    if close and pts and distance(pts[0], pts[-1]) > 1e-9:
        pts.append(pts[0])
    return ", ".join(f"new Point3d({p[0]:.12g}, {p[1]:.12g}, {p[2]:.12g})" for p in pts)


def distance(a: list[float], b: list[float]) -> float:
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def cs_string(value: str) -> str:
    return json.dumps(value)


COMMON_PREAMBLE = """
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Rhino.DocObjects;

int EnsureLayer(RhinoDoc doc, string name, System.Drawing.Color color)
{
    int index = doc.Layers.FindByFullPath(name, -1);
    if (index >= 0) return index;
    var layer = new Layer();
    layer.Name = name;
    layer.Color = color;
    return doc.Layers.Add(layer);
}
"""


READ_VISIBLE_CURVES = COMMON_PREAMBLE + """
int count = 0;
foreach (var rhObj in doc.Objects)
{
    if (rhObj == null) continue;
    if (rhObj.IsDeleted) continue;
    if (rhObj.IsHidden) continue;
    var curve = rhObj.Geometry as Curve;
    if (curve == null) continue;
    var bbox = curve.GetBoundingBox(true);
    output.AppendLine(
        rhObj.Id.ToString()
        + " name=" + rhObj.Name
        + " layer=" + doc.Layers[rhObj.Attributes.LayerIndex].Name
        + " closed=" + curve.IsClosed.ToString()
        + " length=" + curve.GetLength().ToString("0.###")
        + " bbox_min=(" + bbox.Min.X.ToString("0.###") + "," + bbox.Min.Y.ToString("0.###") + "," + bbox.Min.Z.ToString("0.###") + ")"
        + " bbox_max=(" + bbox.Max.X.ToString("0.###") + "," + bbox.Max.Y.ToString("0.###") + "," + bbox.Max.Z.ToString("0.###") + ")"
    );
    count++;
}
output.AppendLine("visible_curves=" + count.ToString());
"""


if __name__ == "__main__":
    raise SystemExit(main())
