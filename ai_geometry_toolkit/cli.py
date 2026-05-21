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
    new_case.add_argument("--units", default="m", choices=("mm", "m", "cm"))
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

    link_backend = sub.add_parser("link-backend", help="Attach an external geometry backend to a case.")
    link_backend.add_argument("case")
    link_backend.add_argument("--backend", required=True, choices=("text-to-cad",))
    link_backend.add_argument("--repo", required=True, help="Path to the backend repository.")
    link_backend.set_defaults(func=cmd_link_backend)

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
