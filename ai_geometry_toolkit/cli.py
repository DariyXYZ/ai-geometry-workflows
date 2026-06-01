from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCENARIOS = {
    "reference": "Scenario 1 - model from images, drawings, description",
    "cleanup": "Scenario 2 - simplified analysis model from complex Rhino geometry",
    "massing": "Scenario 3 - massing variants and revisions from TEPs",
}

REQUIRED_PARAMS = {
    "reference": [
        ("run_id",),
        ("units",),
        ("footprint", "width_m"),
        ("footprint", "depth_m"),
        ("height_bands",),
    ],
    "cleanup": [
        ("run_id",),
        ("source", "layer_or_file"),
        ("target", "output_type"),
    ],
    "massing": [
        ("run_id",),
        ("site",),
        ("tep",),
        ("variants",),
    ],
}

CASE_DIRS = ("source", "reports", "captures", "artifacts", "scripts")
KEY_VALUE_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_-]*)=([\"'][^\"']*[\"']|\[[^\]]*\]|[^\s,]+)")
SEMANTIC_SCENE_KEYS = {"scene", "units", "up", "live_obj_version", "workflow", "kernel_default"}
SEMANTIC_PART_KEYS = {
    "source",
    "type",
    "semantic",
    "params",
    "controls",
    "bbox",
    "anchor",
    "anchors",
    "lock",
    "constraint",
    "part",
    "variant",
    "hidden",
    "post",
    "ops",
    "sdf",
}
ALLOWED_SEMANTIC_POST_OPS = {
    "transform",
    "symmetrize",
    "mirror",
    "array",
    "deform",
    "subdivide",
    "smooth",
    "simplify",
    "snap_to_ground",
    "center_origin",
    "material",
    "tag",
}
SEMANTIC_BUILD_METHODS = {"semantic_obj", "rhino_preview", "build123d_step", "guide_only", "manual_review"}


@dataclass(frozen=True)
class CasePaths:
    root: Path
    manifest: Path
    params: Path
    intake: Path
    route: Path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-geo", description="AI geometry workflow case runner.")
    sub = parser.add_subparsers(required=True)

    new_case = sub.add_parser("new-case", help="Create a reproducible case folder.")
    new_case.add_argument("--scenario", required=True, choices=sorted(SCENARIOS))
    new_case.add_argument("--name", required=True)
    new_case.add_argument("--root", default="cases")
    new_case.add_argument("--source", default="")
    new_case.add_argument("--units", default="m", choices=("mm", "m", "cm", "ft"))
    new_case.add_argument("--downstream", default="")
    new_case.set_defaults(func=cmd_new_case)

    validate = sub.add_parser("validate-case", help="Validate case manifest and parameter table.")
    validate.add_argument("case")
    validate.set_defaults(func=cmd_validate_case)

    route = sub.add_parser("route", help="Write a scenario-specific development route.")
    route.add_argument("case")
    route.set_defaults(func=cmd_route)

    classify = sub.add_parser("classify-scan", help="Classify objects from a scan_scene-style JSON report.")
    classify.add_argument("case")
    classify.add_argument("--scan", default="")
    classify.add_argument("--output", default="")
    classify.set_defaults(func=cmd_classify_scan)

    audit = sub.add_parser("audit-scan", help="Write a compact scan audit report.")
    audit.add_argument("case")
    audit.add_argument("--scan", default="")
    audit.set_defaults(func=cmd_audit_scan)

    validate_candidate = sub.add_parser(
        "validate-candidate",
        help="Compare source and candidate scan bbox metrics and write validation reports.",
    )
    validate_candidate.add_argument("case")
    validate_candidate.add_argument("--source-scan", default="", help="Source scan JSON. Defaults to case reports.")
    validate_candidate.add_argument("--candidate-scan", required=True, help="Candidate scan JSON to validate.")
    validate_candidate.add_argument(
        "--size-tolerance",
        type=float,
        default=0.05,
        help="Allowed relative scene-size delta per axis. Default: 0.05.",
    )
    validate_candidate.add_argument(
        "--center-tolerance",
        type=float,
        default=0.05,
        help="Allowed relative scene-center delta per axis. Default: 0.05.",
    )
    validate_candidate.add_argument("--output", default="", help="JSON output path.")
    validate_candidate.add_argument("--markdown", default="", help="Markdown output path.")
    validate_candidate.set_defaults(func=cmd_validate_candidate)

    link_backend = sub.add_parser("link-backend", help="Attach an external geometry backend to a case.")
    link_backend.add_argument("case")
    link_backend.add_argument("--backend", required=True, choices=("text-to-cad",))
    link_backend.add_argument("--repo", required=True, help="Path to the backend repository.")
    link_backend.set_defaults(func=cmd_link_backend)

    semantic = sub.add_parser("import-semantic-obj", help="Import Live OBJ-style #@ metadata into semantic part reports.")
    semantic.add_argument("case")
    semantic.add_argument("--source", required=True, help="Path to a .live.obj or OBJ file with #@ metadata.")
    semantic.add_argument("--output", default="", help="JSON output path. Defaults to reports/semantic_parts.json.")
    semantic.add_argument("--markdown", default="", help="Markdown output path. Defaults to reports/semantic_parts.md.")
    semantic.add_argument("--plan", default="", help="Planner JSON output path. Defaults to reports/semantic_plan.json.")
    semantic.add_argument("--validation", default="", help="Validation Markdown output path. Defaults to reports/semantic_validation.md.")
    semantic.set_defaults(func=cmd_import_semantic_obj)

    return parser


class WorkflowError(RuntimeError):
    pass


def cmd_new_case(args: argparse.Namespace) -> int:
    scenario = args.scenario
    case_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{slugify(args.name)}"
    root = Path(args.root).resolve() / case_id
    root.mkdir(parents=True, exist_ok=False)
    for name in CASE_DIRS:
        (root / name).mkdir()

    paths = case_paths(root)
    params = default_params(scenario, case_id, args)
    manifest = {
        "schemaVersion": 1,
        "caseId": case_id,
        "scenario": scenario,
        "scenarioName": SCENARIOS[scenario],
        "status": "intake",
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "source": args.source,
        "units": args.units,
        "paths": {
            "intake": "intake.md",
            "params": "params.json",
            "route": "reports/development_route.md",
            "classification": "reports/source_classification.json",
            "scanAudit": "reports/scan_audit.md",
        },
        "gates": scenario_gates(scenario),
    }

    write_json(paths.manifest, manifest)
    write_json(paths.params, params)
    paths.intake.write_text(intake_template(scenario, case_id, args), encoding="utf-8")
    (root / "reports" / "validation.md").write_text(validation_template(scenario), encoding="utf-8")
    (root / "README.md").write_text(case_readme(manifest), encoding="utf-8")

    print(root)
    return 0


def cmd_validate_case(args: argparse.Namespace) -> int:
    paths = case_paths(resolve_case(args.case))
    manifest = read_json(paths.manifest)
    params = read_json(paths.params)
    scenario = require_scenario(manifest)
    errors = validate_required(params, REQUIRED_PARAMS[scenario])
    errors.extend(validate_manifest_paths(paths.root, manifest))
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"OK {paths.root}")
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    paths = case_paths(resolve_case(args.case))
    manifest = read_json(paths.manifest)
    scenario = require_scenario(manifest)
    text = route_template(manifest, scenario)
    paths.route.parent.mkdir(exist_ok=True)
    paths.route.write_text(text, encoding="utf-8")
    print(paths.route)
    return 0


def cmd_classify_scan(args: argparse.Namespace) -> int:
    case_root = resolve_case(args.case)
    paths = case_paths(case_root)
    scan_path = resolve_scan_path(case_root, args.scan)
    report = read_json(scan_path)
    objects = normalize_scan_objects(report)
    if not objects:
        raise WorkflowError(f"scan report has no objects: {scan_path}")
    classification = classify_objects(objects)
    classification["sourceScan"] = rel_or_abs(scan_path, case_root)
    output = Path(args.output).resolve() if args.output else case_root / "reports" / "source_classification.json"
    write_json(output, classification)
    print(output)
    print(classification_summary(classification))
    return 0


def cmd_audit_scan(args: argparse.Namespace) -> int:
    case_root = resolve_case(args.case)
    scan_path = resolve_scan_path(case_root, args.scan)
    report = read_json(scan_path)
    objects = normalize_scan_objects(report)
    classification = classify_objects(objects) if objects else {"classes": {}, "summary": {}}
    output = case_root / "reports" / "scan_audit.md"
    output.write_text(scan_audit_markdown(scan_path, objects, classification), encoding="utf-8")
    print(output)
    return 0


def cmd_validate_candidate(args: argparse.Namespace) -> int:
    case_root = resolve_case(args.case)
    source_scan = resolve_scan_path(case_root, args.source_scan)
    candidate_scan = resolve_input_path(args.candidate_scan)
    source_report = read_json(source_scan)
    candidate_report = read_json(candidate_scan)
    source_objects = normalize_scan_objects(source_report)
    candidate_objects = normalize_scan_objects(candidate_report)
    if not source_objects:
        raise WorkflowError(f"source scan has no objects with bbox: {source_scan}")
    if not candidate_objects:
        raise WorkflowError(f"candidate scan has no objects with bbox: {candidate_scan}")

    report = candidate_validation_report(
        source_scan=source_scan,
        candidate_scan=candidate_scan,
        source_objects=source_objects,
        candidate_objects=candidate_objects,
        size_tolerance=float(args.size_tolerance),
        center_tolerance=float(args.center_tolerance),
    )
    output = Path(args.output).resolve() if args.output else case_root / "reports" / "candidate_validation.json"
    markdown = Path(args.markdown).resolve() if args.markdown else case_root / "reports" / "candidate_validation.md"
    write_json(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(candidate_validation_markdown(report), encoding="utf-8")

    paths = case_paths(case_root)
    manifest = read_json(paths.manifest)
    manifest.setdefault("paths", {})["candidateValidation"] = rel_or_abs(output, case_root)
    manifest.setdefault("paths", {})["candidateValidationReport"] = rel_or_abs(markdown, case_root)
    write_json(paths.manifest, manifest)

    print(output)
    print(f"status={report['status']} maxSizeDelta={report['summary']['maxSizeDelta']} maxCenterDelta={report['summary']['maxCenterDelta']}")
    return 0 if report["status"] == "pass" else 1


def cmd_link_backend(args: argparse.Namespace) -> int:
    case_root = resolve_case(args.case)
    backend = str(args.backend)
    repo = Path(args.repo).resolve()
    if backend != "text-to-cad":
        raise WorkflowError(f"unsupported backend: {backend}")
    profile = text_to_cad_profile(repo)

    paths = case_paths(case_root)
    manifest = read_json(paths.manifest)
    params = read_json(paths.params)
    manifest.setdefault("paths", {})["textToCadBackend"] = "reports/backend_text_to_cad.md"
    manifest.setdefault("backends", {})["text-to-cad"] = {
        "repo": str(repo),
        "profile": "reports/backend_text_to_cad.json",
    }
    params.setdefault("backends", {})["text-to-cad"] = {
        "repo": str(repo),
        "skillDir": profile["skillDir"],
        "stepLauncher": profile["stepLauncher"],
        "inspectLauncher": profile["inspectLauncher"],
        "renderViewerDir": profile["renderViewerDir"],
        "role": "parametric STEP backend for clean source-controlled parts and baseline candidates",
    }

    write_json(paths.manifest, manifest)
    write_json(paths.params, params)
    write_json(case_root / "reports" / "backend_text_to_cad.json", profile)
    (case_root / "reports" / "backend_text_to_cad.md").write_text(
        backend_markdown(manifest, profile),
        encoding="utf-8",
    )
    print(case_root / "reports" / "backend_text_to_cad.md")
    return 0


def cmd_import_semantic_obj(args: argparse.Namespace) -> int:
    case_root = resolve_case(args.case)
    source = Path(args.source)
    if not source.is_absolute():
        source = (Path.cwd() / source).resolve()
    if not source.exists():
        raise WorkflowError(f"semantic OBJ source does not exist: {source}")

    report = parse_semantic_obj(source)
    report["sourceFile"] = rel_or_abs(source, case_root)
    output = Path(args.output).resolve() if args.output else case_root / "reports" / "semantic_parts.json"
    markdown = Path(args.markdown).resolve() if args.markdown else case_root / "reports" / "semantic_parts.md"
    plan_path = Path(args.plan).resolve() if args.plan else case_root / "reports" / "semantic_plan.json"
    validation_path = (
        Path(args.validation).resolve() if args.validation else case_root / "reports" / "semantic_validation.md"
    )
    write_json(output, report)
    write_json(plan_path, report["planner"])
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(semantic_parts_markdown(report), encoding="utf-8")
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text(semantic_validation_markdown(report), encoding="utf-8")

    paths = case_paths(case_root)
    manifest = read_json(paths.manifest)
    manifest.setdefault("paths", {})["semanticParts"] = rel_or_abs(output, case_root)
    manifest.setdefault("paths", {})["semanticPartsReport"] = rel_or_abs(markdown, case_root)
    manifest.setdefault("paths", {})["semanticPlan"] = rel_or_abs(plan_path, case_root)
    manifest.setdefault("paths", {})["semanticValidation"] = rel_or_abs(validation_path, case_root)
    write_json(paths.manifest, manifest)

    print(output)
    print(semantic_summary(report))
    return 0


def resolve_case(raw: str) -> Path:
    path = Path(raw).resolve()
    if not path.exists():
        raise WorkflowError(f"case path does not exist: {path}")
    if path.is_file():
        path = path.parent
    if not (path / "case.json").exists():
        raise WorkflowError(f"case.json not found in {path}")
    return path


def case_paths(root: Path) -> CasePaths:
    return CasePaths(
        root=root,
        manifest=root / "case.json",
        params=root / "params.json",
        intake=root / "intake.md",
        route=root / "reports" / "development_route.md",
    )


def require_scenario(manifest: dict[str, Any]) -> str:
    scenario = str(manifest.get("scenario", ""))
    if scenario not in SCENARIOS:
        raise WorkflowError(f"unsupported scenario in manifest: {scenario!r}")
    return scenario


def validate_required(data: dict[str, Any], paths: list[tuple[str, ...]]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        cur: Any = data
        for part in path:
            if not isinstance(cur, dict) or part not in cur:
                errors.append(f"missing params.{'.'.join(path)}")
                break
            cur = cur[part]
        else:
            if cur in (None, "", []):
                errors.append(f"empty params.{'.'.join(path)}")
    return errors


def validate_manifest_paths(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ("intake", "params"):
        raw = manifest.get("paths", {}).get(field)
        if raw and not (root / raw).exists():
            errors.append(f"manifest path does not exist: {raw}")
    return errors


def resolve_scan_path(case_root: Path, raw: str) -> Path:
    if raw:
        path = Path(raw)
        if not path.is_absolute():
            path = (Path.cwd() / path).resolve()
        return path
    candidates = [
        case_root / "reports" / "scene_scan.json",
        case_root / "reports" / "tower_bbox_classification.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise WorkflowError("scan path not provided and no default report exists")


def resolve_input_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    if not path.exists():
        raise WorkflowError(f"input path does not exist: {path}")
    return path


def normalize_scan_objects(report: dict[str, Any]) -> list[dict[str, Any]]:
    raw = report.get("objects")
    if raw is None:
        raw = report.get("selected")
    if not isinstance(raw, list):
        return []
    objects: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        bbox = item.get("bbox")
        if not valid_bbox(bbox):
            continue
        size = item.get("size") or bbox_size(bbox)
        objects.append(
            {
                "id": str(item.get("id", "")),
                "name": str(item.get("name", "")),
                "layer": str(item.get("layer", "")),
                "type": str(item.get("type", "")),
                "is_hidden": bool(item.get("is_hidden", False)),
                "is_solid": item.get("is_solid", item.get("isSolid")),
                "bbox": bbox,
                "size": size,
                "center": item.get("center") or bbox_center(bbox),
                "face_count": item.get("face_count", item.get("faceCount")),
                "vertex_count": item.get("vertex_count", item.get("vertexCount")),
            }
        )
    return objects


def classify_objects(objects: list[dict[str, Any]]) -> dict[str, Any]:
    scene_bbox = union_bbox([obj["bbox"] for obj in objects])
    scene_size = bbox_size(scene_bbox)
    scene_diag = max(length(scene_size), 1.0)
    z_min = scene_bbox["min"][2]
    z_max = scene_bbox["max"][2]
    z_span = max(z_max - z_min, 1.0)
    max_footprint = max((footprint_area(obj) for obj in objects), default=1.0)

    classes: dict[str, list[dict[str, Any]]] = {
        "primary_envelope": [],
        "crown_roof": [],
        "podium_base": [],
        "supports": [],
        "large_bands": [],
        "facade_detail": [],
        "noise": [],
    }

    for obj in objects:
        sx, sy, sz = [float(v) for v in obj["size"]]
        area = max(sx * sy, 0.0)
        top_ratio = (obj["bbox"]["max"][2] - z_min) / z_span
        height_ratio = sz / z_span
        diag_ratio = length((sx, sy, sz)) / scene_diag
        thin_z = sz < z_span * 0.035
        slender = sz > max(sx, sy, 0.001) * 2.8 and area < max_footprint * 0.10

        target = "facade_detail"
        if diag_ratio < 0.012:
            target = "noise"
        elif slender:
            target = "supports"
        elif height_ratio > 0.42 and area > max_footprint * 0.04:
            target = "primary_envelope"
        elif top_ratio > 0.82 and height_ratio < 0.22:
            target = "crown_roof"
        elif height_ratio < 0.18 and area > max_footprint * 0.18:
            target = "podium_base"
        elif thin_z and area > max_footprint * 0.08:
            target = "large_bands"

        classes[target].append(object_ref(obj, score=classification_score(obj, scene_bbox)))

    return {
        "schemaVersion": 1,
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "scene": {
            "bbox": scene_bbox,
            "size": scene_size,
            "objectCount": len(objects),
            "hiddenCount": sum(1 for obj in objects if obj.get("is_hidden")),
        },
        "classes": {name: sorted(items, key=lambda item: item["score"], reverse=True) for name, items in classes.items()},
        "summary": {name: len(items) for name, items in classes.items()},
        "method": "bbox_zrange_heuristic_v1",
        "limitations": [
            "Heuristic classification is a routing aid, not final architectural truth.",
            "Validate with source overlays, section deltas, and human review before building.",
        ],
    }


def object_ref(obj: dict[str, Any], *, score: float) -> dict[str, Any]:
    return {
        "id": obj.get("id", ""),
        "name": obj.get("name", ""),
        "layer": obj.get("layer", ""),
        "type": obj.get("type", ""),
        "bbox": obj.get("bbox"),
        "size": obj.get("size"),
        "center": obj.get("center"),
        "score": round(score, 6),
    }


def classification_score(obj: dict[str, Any], scene_bbox: dict[str, list[float]]) -> float:
    sx, sy, sz = [float(v) for v in obj["size"]]
    scene_size = bbox_size(scene_bbox)
    scene_diag = max(length(scene_size), 1.0)
    return length((sx, sy, sz)) / scene_diag


def scan_audit_markdown(scan_path: Path, objects: list[dict[str, Any]], classification: dict[str, Any]) -> str:
    summary = classification.get("summary", {})
    hidden = sum(1 for obj in objects if obj.get("is_hidden"))
    lines = [
        "# Scan Audit",
        "",
        f"- Source scan: `{scan_path}`",
        f"- Objects with bbox: {len(objects)}",
        f"- Hidden objects in scan: {hidden}",
        "",
        "## Classification",
        "",
    ]
    for key in ("primary_envelope", "crown_roof", "podium_base", "supports", "large_bands", "facade_detail", "noise"):
        lines.append(f"- {key}: {summary.get(key, 0)}")
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "- Do not build from this classification alone.",
            "- Confirm major groups against fixed top/front/side captures.",
            "- For Scenario 2, extract sections per architectural part before candidate generation.",
            "",
        ]
    )
    return "\n".join(lines)


def candidate_validation_report(
    *,
    source_scan: Path,
    candidate_scan: Path,
    source_objects: list[dict[str, Any]],
    candidate_objects: list[dict[str, Any]],
    size_tolerance: float,
    center_tolerance: float,
) -> dict[str, Any]:
    source_bbox = union_bbox([obj["bbox"] for obj in source_objects])
    candidate_bbox = union_bbox([obj["bbox"] for obj in candidate_objects])
    source_size = bbox_size(source_bbox)
    candidate_size = bbox_size(candidate_bbox)
    source_center = bbox_center(source_bbox)
    candidate_center = bbox_center(candidate_bbox)
    size_delta = relative_axis_delta(source_size, [candidate_size[i] - source_size[i] for i in range(3)])
    center_delta = relative_axis_delta(source_size, [candidate_center[i] - source_center[i] for i in range(3)])
    size_failures = [axis for axis, value in size_delta.items() if value > size_tolerance]
    center_failures = [axis for axis, value in center_delta.items() if value > center_tolerance]
    status = "pass" if not size_failures and not center_failures else "fail"
    source_classification = classify_objects(source_objects)
    candidate_classification = classify_objects(candidate_objects)
    return {
        "schemaVersion": 1,
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "sourceScan": str(source_scan),
        "candidateScan": str(candidate_scan),
        "tolerances": {
            "size": size_tolerance,
            "center": center_tolerance,
        },
        "source": {
            "objectCount": len(source_objects),
            "bbox": source_bbox,
            "size": source_size,
            "center": source_center,
            "classSummary": source_classification.get("summary", {}),
        },
        "candidate": {
            "objectCount": len(candidate_objects),
            "bbox": candidate_bbox,
            "size": candidate_size,
            "center": candidate_center,
            "classSummary": candidate_classification.get("summary", {}),
        },
        "deltas": {
            "size": size_delta,
            "center": center_delta,
            "objectCount": len(candidate_objects) - len(source_objects),
            "classSummary": class_summary_delta(
                source_classification.get("summary", {}),
                candidate_classification.get("summary", {}),
            ),
        },
        "failures": {
            "sizeAxes": size_failures,
            "centerAxes": center_failures,
        },
        "summary": {
            "maxSizeDelta": round(max(size_delta.values(), default=0.0), 6),
            "maxCenterDelta": round(max(center_delta.values(), default=0.0), 6),
        },
        "limitations": [
            "BBox validation is a first numeric gate, not architectural acceptance.",
            "Pass still requires source-derived sections, fixed captures, and part review.",
            "Use this before claiming that closed candidate geometry matches the source.",
        ],
    }


def relative_axis_delta(reference: list[float], candidate_or_delta: list[float]) -> dict[str, float]:
    axes = ("x", "y", "z")
    deltas: dict[str, float] = {}
    for i, axis in enumerate(axes):
        denominator = max(abs(float(reference[i])), 1e-9)
        deltas[axis] = round(abs(float(candidate_or_delta[i])) / denominator, 6)
    return deltas


def class_summary_delta(source: dict[str, Any], candidate: dict[str, Any]) -> dict[str, int]:
    keys = sorted(set(source) | set(candidate))
    return {key: int(candidate.get(key, 0)) - int(source.get(key, 0)) for key in keys}


def candidate_validation_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Candidate Validation",
        "",
        f"- Status: `{report.get('status')}`",
        f"- Source scan: `{report.get('sourceScan')}`",
        f"- Candidate scan: `{report.get('candidateScan')}`",
        f"- Size tolerance: {report.get('tolerances', {}).get('size')}",
        f"- Center tolerance: {report.get('tolerances', {}).get('center')}",
        "",
        "## Scene Metrics",
        "",
        f"- Source size: `{report.get('source', {}).get('size')}`",
        f"- Candidate size: `{report.get('candidate', {}).get('size')}`",
        f"- Size deltas: `{report.get('deltas', {}).get('size')}`",
        f"- Center deltas: `{report.get('deltas', {}).get('center')}`",
        f"- Object count delta: {report.get('deltas', {}).get('objectCount')}",
        "",
        "## Failures",
        "",
        f"- Size axes: `{report.get('failures', {}).get('sizeAxes', [])}`",
        f"- Center axes: `{report.get('failures', {}).get('centerAxes', [])}`",
        "",
        "## Gate",
        "",
        "- This check only compares source/candidate scan metrics.",
        "- Passing this report does not accept the geometry.",
        "- Continue with sections, source overlays, and fixed captures before handoff.",
        "",
    ]
    return "\n".join(lines)


def text_to_cad_profile(repo: Path) -> dict[str, Any]:
    if not repo.exists():
        raise WorkflowError(f"text-to-cad repo does not exist: {repo}")
    skill_dir = repo / "skills" / "cad"
    required = [
        repo / "README.md",
        skill_dir / "SKILL.md",
        skill_dir / "requirements.txt",
        skill_dir / "scripts" / "step" / "cli.py",
        skill_dir / "scripts" / "inspect" / "cli.py",
        repo / "skills" / "render" / "scripts" / "viewer" / "package.json",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        joined = ", ".join(str(path) for path in missing)
        raise WorkflowError(f"text-to-cad repo is missing required files: {joined}")
    return {
        "schemaVersion": 1,
        "backend": "text-to-cad",
        "repo": str(repo),
        "skillDir": str(skill_dir),
        "stepLauncher": str(skill_dir / "scripts" / "step"),
        "inspectLauncher": str(skill_dir / "scripts" / "inspect"),
        "renderViewerDir": str(repo / "skills" / "render" / "scripts" / "viewer"),
        "primaryArtifact": "STEP",
        "sourceContract": "Python build123d source with gen_step() returning a closed part, compound, or assembly.",
        "fitFor": [
            "clean parametric parts",
            "source-controlled STEP generation",
            "closed simplified baseline candidates",
            "secondary STL/3MF/DXF/GLB exports from a STEP-first model",
        ],
        "notFitFor": [
            "direct repair of messy Rhino meshes",
            "acceptance based only on visual renders",
            "global mesh decimation as final Scenario 2 output",
        ],
    }


def backend_markdown(manifest: dict[str, Any], profile: dict[str, Any]) -> str:
    return f"""# text-to-cad Backend

Case: `{manifest["caseId"]}`

Backend repo: `{profile["repo"]}`

## Role

Use `text-to-cad` as a STEP-first CAD-as-code backend when the case needs a clean
parametric source model. For Scenario 2 cleanup, this is useful for refined
closed baseline candidates after scan classification and section extraction. It
is not the source mesh repair backend.

## Launchers

```powershell
python "{profile["stepLauncher"]}" path\\to\\candidate.py
python "{profile["inspectLauncher"]}" refs path\\to\\candidate.step --facts --planes --positioning
```

## Contract

- Keep editable source in the case `source/` or `scripts/` folder.
- Define `gen_step()` and generate explicit STEP targets.
- Validate generated STEP with facts, planes, positioning, and targeted measures.
- Treat viewer links and snapshots as review aids, not validation by themselves.
- Store generated artifacts under `artifacts/` until promoted.

## Scenario 2 Boundary

Use Rhino/Aurox for source `.3dm` scanning, part classification, section
extraction, and source overlays. Use `text-to-cad` when the accepted route is to
rebuild an architectural part or simplified shell from parameters.
"""


def parse_semantic_obj(path: Path) -> dict[str, Any]:
    parts: list[dict[str, Any]] = []
    scene: dict[str, Any] = {"metadata": {}}
    current: dict[str, Any] | None = None
    active_block = ""
    vertex_count = 0
    face_count = 0

    def ensure_current(line_no: int) -> dict[str, Any]:
        nonlocal current
        if current is None:
            current = new_semantic_part(f"unnamed_{line_no}")
            parts.append(current)
        return current

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("o ") or line.startswith("g "):
            name = line.split(maxsplit=1)[1].strip()
            current = new_semantic_part(name)
            parts.append(current)
            active_block = ""
            continue
        if line.startswith("v "):
            vertex_count += 1
            if current is not None:
                current["meshStats"]["vertices"] += 1
            continue
        if line.startswith("f "):
            face_count += 1
            if current is not None:
                current["meshStats"]["faces"] += 1
            continue
        if not line.startswith("#@"):
            continue

        body = line[2:].strip()
        if body.startswith("-"):
            if active_block == "controls":
                ensure_current(line_no)["controls"].append(parse_control_line(body[1:].strip()))
            elif active_block == "anchors":
                anchor = parse_anchor_body(body[1:].strip())
                if anchor:
                    ensure_current(line_no)["anchors"].append(anchor)
            continue

        key, value = split_metadata(body)
        if current is None and key in SEMANTIC_SCENE_KEYS:
            scene["metadata"][key] = value if value != "" else True
            active_block = key
            continue

        target = ensure_current(line_no)
        target["metadataKeys"].append({"key": key, "line": line_no})
        active_block = key
        if key == "source":
            target["source"] = value
        elif key == "semantic":
            target["semantic"] = value
        elif key == "params":
            target["params"].update(parse_key_values(value))
        elif key == "bbox":
            target["bbox"] = parse_bbox(value)
        elif key == "anchor":
            anchor = parse_anchor_body(value)
            if anchor:
                target["anchors"].append(anchor)
        elif key == "anchors":
            pass
        elif key == "controls":
            pass
        elif key == "lock":
            target["locks"].extend(parse_list_value(value))
        elif key == "constraint":
            target["constraints"].append(value)
        elif key == "part":
            target["part"].update(parse_key_values(value))
        elif key == "variant":
            target["variants"].append(parse_key_values(value) or {"value": value})
        elif key == "hidden":
            target["hidden"] = parse_bool(value)
        elif key == "type":
            target["geometryType"] = value
        elif key in {"post", "ops"}:
            target["postOps"].append(parse_post_op(value))
        elif key == "sdf":
            target["executionHints"].append(key)
        else:
            target["metadata"][key] = value if value != "" else True
    for part in parts:
        part["cadHint"] = infer_cad_hint(part)
        part["buildMethod"] = infer_build_method(part)
        part["validationHints"] = semantic_validation_hints(part)

    report = {
        "schemaVersion": 1,
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "sourceKind": "live_obj_metadata",
        "scene": scene,
        "meshStats": {"vertices": vertex_count, "faces": face_count},
        "parts": parts,
        "summary": semantic_summary_dict(parts),
        "method": "live_obj_metadata_parser_v1",
        "limitations": [
            "This importer reads intent metadata; it does not validate OBJ geometry.",
            "Semantic parts are CAD build hints, not accepted CAD output.",
            "STEP/3DM validation remains required before handoff.",
        ],
    }
    report["validation"] = validate_semantic_report(report)
    report["planner"] = semantic_planner(report)
    return report


def new_semantic_part(name: str) -> dict[str, Any]:
    return {
        "id": slugify(name).replace("-", "_"),
        "name": name,
        "source": "",
        "geometryType": "",
        "semantic": "",
        "bbox": None,
        "params": {},
        "anchors": [],
        "controls": [],
        "locks": [],
        "constraints": [],
        "postOps": [],
        "part": {},
        "variants": [],
        "hidden": False,
        "executionHints": [],
        "buildMethod": "",
        "validationHints": [],
        "meshStats": {"vertices": 0, "faces": 0},
        "metadataKeys": [],
        "metadata": {},
        "cadHint": "",
    }


def split_metadata(body: str) -> tuple[str, str]:
    if ":" in body:
        key, value = body.split(":", 1)
        return key.strip().lower(), value.strip()
    parts = body.split(maxsplit=1)
    if len(parts) == 1:
        return parts[0].strip().lower(), ""
    return parts[0].strip().lower(), parts[1].strip()


def parse_key_values(body: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for key, raw in KEY_VALUE_RE.findall(body):
        parsed[key] = parse_semantic_value(raw.rstrip(","))
    return parsed


def parse_bbox(body: str) -> dict[str, list[float]] | None:
    values = parse_key_values(body)
    min_pt = values.get("min")
    max_pt = values.get("max")
    if is_vec3(min_pt) and is_vec3(max_pt):
        return {"min": [float(v) for v in min_pt], "max": [float(v) for v in max_pt]}
    return None


def parse_anchor_body(body: str) -> dict[str, Any] | None:
    values = parse_key_values(body)
    anchor_id = values.get("id") or values.get("name")
    at = values.get("at") or values.get("position")
    if anchor_id and is_vec3(at):
        return {"id": str(anchor_id), "at": [float(v) for v in at]}
    if "=" in body:
        key, raw = body.split("=", 1)
        parsed = parse_semantic_value(raw)
        if is_vec3(parsed):
            return {"id": key.strip(), "at": [float(v) for v in parsed]}
    return None


def parse_control_line(body: str) -> dict[str, Any]:
    parts = body.split(maxsplit=1)
    kind = parts[0] if parts else "control"
    attrs = parse_key_values(parts[1] if len(parts) > 1 else "")
    attrs["kind"] = kind
    return attrs


def parse_post_op(body: str) -> dict[str, Any]:
    parts = body.split(maxsplit=1)
    op = parts[0].strip() if parts else ""
    params = parse_key_values(parts[1] if len(parts) > 1 else "")
    return {"op": op, "params": params}


def parse_semantic_value(raw: str) -> Any:
    value = raw.strip().strip(",")
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        if any(ch in value for ch in ".eE"):
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_list_value(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1", "on"}


def is_vec3(value: Any) -> bool:
    return isinstance(value, list) and len(value) == 3 and all(isinstance(v, (int, float)) for v in value)


def semantic_summary_dict(parts: list[dict[str, Any]]) -> dict[str, Any]:
    visible = [part for part in parts if not part.get("hidden")]
    return {
        "partCount": len(parts),
        "visiblePartCount": len(visible),
        "partsWithParams": sum(1 for part in parts if part.get("params")),
        "partsWithBbox": sum(1 for part in parts if part.get("bbox")),
        "partsWithAnchors": sum(1 for part in parts if part.get("anchors")),
        "partsWithControls": sum(1 for part in parts if part.get("controls")),
        "proceduralParts": sum(1 for part in parts if part.get("source") == "procedural"),
        "guideParts": sum(1 for part in parts if part.get("hidden") or part.get("metadata", {}).get("guide") is True),
        "partsWithPostOps": sum(1 for part in parts if part.get("postOps")),
        "plannerReadyParts": sum(1 for part in parts if part.get("buildMethod") in SEMANTIC_BUILD_METHODS),
    }


def semantic_summary(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    return ", ".join(f"{key}={summary.get(key, 0)}" for key in sorted(summary))


def semantic_parts_markdown(report: dict[str, Any]) -> str:
    validation = report.get("validation", {})
    lines = [
        "# Semantic Parts",
        "",
        f"- Source: `{report.get('sourceFile', '')}`",
        f"- Parts: {report.get('summary', {}).get('partCount', 0)}",
        f"- Method: `{report.get('method', '')}`",
        f"- Validation status: `{validation.get('status', 'unknown')}`",
        f"- Planner: `reports/semantic_plan.json`",
        "",
        "## CAD Route Hints",
        "",
    ]
    for part in report.get("parts", []):
        bbox = part.get("bbox") or {}
        size = bbox_size(bbox) if valid_bbox(bbox) else None
        kind = part.get("geometryType") or infer_cad_hint(part)
        lines.extend(
            [
                f"### {part.get('id')}",
                "",
                f"- Name: `{part.get('name')}`",
                f"- Source: `{part.get('source')}`",
                f"- Semantic: {part.get('semantic') or '-'}",
                f"- CAD hint: `{kind}`",
                f"- Build method: `{part.get('buildMethod')}`",
                f"- Params: `{json.dumps(part.get('params', {}), ensure_ascii=False)}`",
                f"- BBox size: `{size}`",
                f"- Anchors: {len(part.get('anchors', []))}",
                f"- Controls: {len(part.get('controls', []))}",
                f"- Post ops: `{json.dumps(part.get('postOps', []), ensure_ascii=False)}`",
                f"- Constraints: {len(part.get('constraints', []))}",
                "",
            ]
        )
    lines.extend(
        [
            "## Gate",
            "",
            "- This report is only an intent extraction smoke test.",
            "- Convert accepted parts into Rhino/build123d scripts before validating geometry.",
            "- Do not accept OBJ mesh preview as final CAD.",
            "",
        ]
    )
    return "\n".join(lines)


def semantic_validation_markdown(report: dict[str, Any]) -> str:
    validation = report.get("validation", {})
    lines = [
        "# Semantic OBJ Validation",
        "",
        f"- Status: `{validation.get('status', 'unknown')}`",
        f"- Errors: {len(validation.get('errors', []))}",
        f"- Warnings: {len(validation.get('warnings', []))}",
        "",
        "## Errors",
        "",
    ]
    errors = validation.get("errors", [])
    lines.extend([f"- {error}" for error in errors] or ["- none"])
    lines.extend(["", "## Warnings", ""])
    warnings = validation.get("warnings", [])
    lines.extend([f"- {warning}" for warning in warnings] or ["- none"])
    lines.extend(
        [
            "",
            "## Allowed Post Ops",
            "",
            "`" + "`, `".join(sorted(ALLOWED_SEMANTIC_POST_OPS)) + "`",
            "",
            "## Gate",
            "",
            "- `valid` means metadata is usable as pipeline input.",
            "- It still does not mean geometry is accepted.",
            "- Build and source-derived validation remain separate gates.",
            "",
        ]
    )
    return "\n".join(lines)


def infer_cad_hint(part: dict[str, Any]) -> str:
    semantic = str(part.get("semantic", "")).lower()
    name = str(part.get("name", "")).lower()
    if "oval" in semantic or "oval" in name or "podium" in semantic:
        return "extrude_oval_or_rounded_profile"
    if "grid" in semantic or "facade" in semantic:
        return "guide_curves_or_panels"
    if part.get("bbox"):
        return "extrude_box_from_bbox"
    return "manual_review"


def infer_build_method(part: dict[str, Any]) -> str:
    geometry_type = str(part.get("geometryType", "")).lower()
    source = str(part.get("source", "")).lower()
    if part.get("hidden") or geometry_type == "guide":
        return "guide_only"
    if source == "procedural" and geometry_type in {"box", "extrude"} and part.get("bbox"):
        return "build123d_step"
    if part.get("bbox"):
        return "rhino_preview"
    return "manual_review"


def semantic_validation_hints(part: dict[str, Any]) -> list[str]:
    hints: list[str] = []
    if not part.get("bbox"):
        hints.append("missing_bbox_blocks_direct_reconstruction")
    if not part.get("params"):
        hints.append("missing_params_limits_editability")
    if not part.get("anchors") and not part.get("hidden"):
        hints.append("missing_anchors_limits_relationship_validation")
    if part.get("buildMethod") == "guide_only":
        hints.append("guide_only_not_final_solid")
    return hints


def validate_semantic_report(report: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    scene_keys = set(report.get("scene", {}).get("metadata", {}).keys())
    for key in sorted(scene_keys - SEMANTIC_SCENE_KEYS):
        warnings.append(f"unknown scene metadata key: {key}")

    for part in report.get("parts", []):
        part_id = part.get("id", "unknown")
        seen_keys = {entry.get("key") for entry in part.get("metadataKeys", [])}
        for key in sorted(seen_keys - SEMANTIC_PART_KEYS):
            warnings.append(f"{part_id}: unknown part metadata key: {key}")
        if not part.get("bbox"):
            warnings.append(f"{part_id}: missing bbox")
        if not part.get("params") and not part.get("hidden"):
            warnings.append(f"{part_id}: missing params")
        if part.get("buildMethod") not in SEMANTIC_BUILD_METHODS:
            errors.append(f"{part_id}: unsupported build method {part.get('buildMethod')!r}")
        for post_op in part.get("postOps", []):
            op = str(post_op.get("op", ""))
            if op not in ALLOWED_SEMANTIC_POST_OPS:
                warnings.append(f"{part_id}: unsupported post op: {op}")

    status = "valid" if not errors else "invalid"
    return {
        "schemaVersion": 1,
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "allowedPartKeys": sorted(SEMANTIC_PART_KEYS),
        "allowedSceneKeys": sorted(SEMANTIC_SCENE_KEYS),
        "allowedPostOps": sorted(ALLOWED_SEMANTIC_POST_OPS),
        "allowedBuildMethods": sorted(SEMANTIC_BUILD_METHODS),
    }


def semantic_planner(report: dict[str, Any]) -> dict[str, Any]:
    scene_meta = report.get("scene", {}).get("metadata", {})
    planned_parts: list[dict[str, Any]] = []
    for part in report.get("parts", []):
        method = part.get("buildMethod") or "manual_review"
        planned_parts.append(
            {
                "id": part.get("id"),
                "role": part.get("semantic") or part.get("name"),
                "method": method,
                "dependencies": infer_dependencies(part),
                "prompt": planner_prompt_for_part(part),
                "controls": part.get("controls", []),
                "controlPostOps": part.get("postOps", []),
                "validationHints": part.get("validationHints", []),
            }
        )
    return {
        "schemaVersion": 1,
        "scene": scene_meta.get("scene", "semantic OBJ import"),
        "units": scene_meta.get("units", ""),
        "up": scene_meta.get("up", ""),
        "materials": [],
        "parts": planned_parts,
        "notes": [
            "Generated from Live OBJ-style metadata.",
            "Use guide_only parts for construction/reference only.",
            "Use build123d_step parts as candidate script inputs, not accepted CAD.",
        ],
    }


def infer_dependencies(part: dict[str, Any]) -> list[str]:
    deps: list[str] = []
    for constraint in part.get("constraints", []):
        tokens = str(constraint).replace(",", " ").split()
        if len(tokens) >= 2 and tokens[0].startswith("must_"):
            deps.append(tokens[-1])
    return sorted(set(dep for dep in deps if dep != part.get("id")))


def planner_prompt_for_part(part: dict[str, Any]) -> str:
    bbox = part.get("bbox")
    bbox_note = f" bbox={bbox}" if bbox else ""
    params = json.dumps(part.get("params", {}), ensure_ascii=False)
    return f"Build only `{part.get('id')}` as {part.get('semantic') or part.get('name')}; params={params}.{bbox_note}"


def classification_summary(classification: dict[str, Any]) -> str:
    summary = classification.get("summary", {})
    return ", ".join(f"{key}={summary.get(key, 0)}" for key in sorted(summary))


def default_params(scenario: str, case_id: str, args: argparse.Namespace) -> dict[str, Any]:
    if scenario == "reference":
        return {
            "run_id": case_id,
            "units": args.units,
            "anchor": {"type": "world_origin", "value": None},
            "footprint": {"width_m": None, "depth_m": None, "shape": "rect", "rotation_deg": 0},
            "height_bands": [],
            "crown": {"type": "flat", "height_m": 0},
            "curved_edges": False,
            "chamfered_edges": False,
            "major_voids": [],
            "uncertainties": ["Fill parameter table before build."],
        }
    if scenario == "cleanup":
        return {
            "run_id": case_id,
            "source": {
                "layer_or_file": args.source,
                "units": args.units,
                "object_count": None,
                "bbox": None,
            },
            "target": {
                "output_type": "closed_shell_set",
                "downstream_tool": args.downstream,
            },
            "classification": {},
            "sections": [],
            "validation": {
                "passed": False,
            },
        }
    return {
        "run_id": case_id,
        "site": {"boundary_layer": args.source, "area_m2": None, "units": args.units},
        "tep": {
            "gfa_m2": None,
            "far": None,
            "footprint_area_m2": None,
            "height_limit_m": None,
            "floor_count": None,
            "parking_spots": None,
        },
        "rules": {"tower_count": 1, "podium_height_m": None, "setbacks": []},
        "variants": [{"id": "V01", "layer": "V01_Massing", "params": {}}],
        "revision_log": [],
    }


def scenario_gates(scenario: str) -> list[str]:
    if scenario == "reference":
        return [
            "source classification before modeling",
            "parameter table before blockout",
            "top/front/side proportion approval before detail",
        ]
    if scenario == "cleanup":
        return [
            "scan includes hidden and locked objects",
            "architectural part classification reviewed",
            "sections extracted per major part",
            "candidate/source section deltas pass",
            "closed shells or watertight output documented",
        ]
    return [
        "parameter table before variants",
        "all variants generated in one run",
        "metrics table produced",
        "revisions recorded as parameter deltas",
    ]


def intake_template(scenario: str, case_id: str, args: argparse.Namespace) -> str:
    title = SCENARIOS[scenario]
    return f"""# {title}

case_id: {case_id}
scenario: {scenario}
units: {args.units}
source: {args.source}
downstream: {args.downstream}

## Intent

Describe the real project task, expected model use, required fidelity, and what must not be lost.

## Inputs

- Source files/images/layers:
- Known dimensions:
- Assumptions:
- Uncertainties:

## Acceptance Gates

{chr(10).join(f"- [ ] {gate}" for gate in scenario_gates(scenario))}

## Notes

- Keep source geometry preserved.
- Treat generated geometry as disposable until validation passes.
- Report only checks that were actually run.
"""


def validation_template(scenario: str) -> str:
    return f"""# Validation Report

Scenario: `{scenario}`

## Checks Run

- [ ] case params validated
- [ ] source scan reviewed
- [ ] classification reviewed
- [ ] sections / metrics reviewed
- [ ] fixed captures reviewed
- [ ] final output checked

## Result

Status: pending

## Risks

- Not validated yet.
"""


def case_readme(manifest: dict[str, Any]) -> str:
    return f"""# {manifest["caseId"]}

Scenario: `{manifest["scenario"]}`  
Status: `{manifest["status"]}`

Run:

```powershell
python -m ai_geometry_toolkit validate-case .
python -m ai_geometry_toolkit route .
```
"""


def route_template(manifest: dict[str, Any], scenario: str) -> str:
    common = [
        "# Development Route",
        "",
        f"Case: `{manifest['caseId']}`",
        f"Scenario: `{scenario}`",
        "",
        "## Shared Contract",
        "",
        "1. Intake and parameter table first.",
        "2. Build source-controlled scripts, not manual geometry drift.",
        "3. Preserve source geometry and old runs until review is complete.",
        "4. Validate with numeric gates and fixed captures.",
        "5. Promote only reproducible runs into reusable templates.",
        "",
    ]
    if scenario == "cleanup":
        specific = [
            "## Scenario 2 Route",
            "",
            "1. Run scene scan with hidden and locked objects included.",
            "2. Classify objects into primary envelope, crown/roof, podium/base, supports, bands, detail, noise.",
            "3. Review classification before building.",
            "4. Extract sections per major architectural part, not one global section stack.",
            "5. Validate section correspondence and center drift.",
            "6. Build closed simplified parts from accepted sections or named rails.",
            "7. Add only analysis-relevant detail.",
            "8. Produce bbox/section delta report and fixed captures.",
            "",
            "Near-term benchmark: `test_data_2.3dm`, refining `test_data2_v3_clean_massing` into `v4_refined_clean_massing`.",
        ]
    elif scenario == "reference":
        specific = [
            "## Scenario 1 Route",
            "",
            "1. Classify every source image or drawing by authority.",
            "2. Extract dimensions into a parameter table.",
            "3. Build blockout only.",
            "4. Validate plan/elevation/side proportions.",
            "5. Add detail only after blockout acceptance.",
        ]
    else:
        specific = [
            "## Scenario 3 Route",
            "",
            "1. Convert TEPs and description into params.",
            "2. Generate all variants in one script run.",
            "3. Write metrics per variant.",
            "4. Apply user revisions as parameter deltas.",
            "5. Keep revision log tied to params and layer names.",
        ]
    return "\n".join(common + specific) + "\n"


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkflowError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"invalid JSON {path}: {exc}") from exc


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-").lower()
    return slug or "case"


def valid_bbox(bbox: Any) -> bool:
    return (
        isinstance(bbox, dict)
        and isinstance(bbox.get("min"), list)
        and isinstance(bbox.get("max"), list)
        and len(bbox["min"]) == 3
        and len(bbox["max"]) == 3
    )


def bbox_size(bbox: dict[str, list[float]]) -> list[float]:
    return [float(bbox["max"][i]) - float(bbox["min"][i]) for i in range(3)]


def bbox_center(bbox: dict[str, list[float]]) -> list[float]:
    return [(float(bbox["max"][i]) + float(bbox["min"][i])) / 2.0 for i in range(3)]


def union_bbox(boxes: list[dict[str, list[float]]]) -> dict[str, list[float]]:
    if not boxes:
        return {"min": [0.0, 0.0, 0.0], "max": [0.0, 0.0, 0.0]}
    return {
        "min": [min(float(box["min"][i]) for box in boxes) for i in range(3)],
        "max": [max(float(box["max"][i]) for box in boxes) for i in range(3)],
    }


def footprint_area(obj: dict[str, Any]) -> float:
    sx, sy, _ = [float(v) for v in obj["size"]]
    return max(sx * sy, 0.0)


def length(values: Any) -> float:
    return math.sqrt(sum(float(value) * float(value) for value in values))


def rel_or_abs(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())
