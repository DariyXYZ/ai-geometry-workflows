from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ai_geometry_toolkit", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )


def run_helper(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/rhino/common/rhino_common_helper.py", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )


class ToolkitCliTests(unittest.TestCase):
    def test_new_cleanup_case_validate_route_and_classify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "cleanup",
                "--name",
                "sample cleanup",
                "--root",
                str(root),
                "--source",
                "sample.3dm",
                "--units",
                "m",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            self.assertTrue((case / "case.json").exists())
            self.assertTrue((case / "params.json").exists())

            validated = run_cli("validate-case", str(case))
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)

            routed = run_cli("route", str(case))
            self.assertEqual(routed.returncode, 0, routed.stdout + routed.stderr)
            self.assertTrue((case / "reports" / "development_route.md").exists())

            scan = ROOT / "tests" / "fixtures" / "scan_scene_sample.json"
            classified = run_cli("classify-scan", str(case), "--scan", str(scan))
            self.assertEqual(classified.returncode, 0, classified.stdout + classified.stderr)
            data = json.loads((case / "reports" / "source_classification.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(data["summary"]["primary_envelope"], 1)
            self.assertGreaterEqual(data["summary"]["podium_base"], 1)

    def test_reference_case_requires_parameter_table_before_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "reference",
                "--name",
                "reference missing params",
                "--root",
                str(root),
                "--units",
                "m",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            validated = run_cli("validate-case", str(case))
            self.assertEqual(validated.returncode, 1)
            self.assertIn("empty params.footprint.width_m", validated.stdout + validated.stderr)

    def test_new_case_accepts_feet_for_drawing_based_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "reference",
                "--name",
                "drawing in feet",
                "--root",
                str(root),
                "--units",
                "ft",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            params = json.loads((case / "params.json").read_text(encoding="utf-8"))
            self.assertEqual(params["units"], "ft")

    def test_link_text_to_cad_backend_writes_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "cleanup",
                "--name",
                "backend link",
                "--root",
                str(root),
                "--source",
                "sample.3dm",
                "--units",
                "m",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            repo = root / "text-to-cad"
            for path in (
                repo / "skills" / "cad" / "scripts" / "step",
                repo / "skills" / "cad" / "scripts" / "inspect",
                repo / "skills" / "render" / "scripts" / "viewer",
            ):
                path.mkdir(parents=True)
            for path in (
                repo / "README.md",
                repo / "skills" / "cad" / "SKILL.md",
                repo / "skills" / "cad" / "requirements.txt",
                repo / "skills" / "cad" / "scripts" / "step" / "cli.py",
                repo / "skills" / "cad" / "scripts" / "inspect" / "cli.py",
                repo / "skills" / "render" / "scripts" / "viewer" / "package.json",
            ):
                path.write_text("stub\n", encoding="utf-8")

            linked = run_cli("link-backend", str(case), "--backend", "text-to-cad", "--repo", str(repo))
            self.assertEqual(linked.returncode, 0, linked.stdout + linked.stderr)
            self.assertTrue((case / "reports" / "backend_text_to_cad.md").exists())
            manifest = json.loads((case / "case.json").read_text(encoding="utf-8"))
            params = json.loads((case / "params.json").read_text(encoding="utf-8"))
            self.assertIn("text-to-cad", manifest["backends"])
            self.assertEqual(params["backends"]["text-to-cad"]["repo"], str(repo.resolve()))

    def test_import_semantic_obj_writes_part_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "reference",
                "--name",
                "office tower semantic smoke",
                "--root",
                str(root),
                "--units",
                "m",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            source = ROOT / "tests" / "fixtures" / "office_tower_semantic.live.obj"

            imported = run_cli("import-semantic-obj", str(case), "--source", str(source))
            self.assertEqual(imported.returncode, 0, imported.stdout + imported.stderr)
            data = json.loads((case / "reports" / "semantic_parts.json").read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["partCount"], 5)
            self.assertEqual(data["summary"]["visiblePartCount"], 4)
            self.assertEqual(data["summary"]["partsWithBbox"], 5)
            self.assertEqual(data["summary"]["partsWithAnchors"], 4)
            self.assertEqual(data["summary"]["partsWithControls"], 2)
            self.assertEqual(data["validation"]["status"], "valid")

            parts = {part["id"]: part for part in data["parts"]}
            self.assertEqual(parts["tower_main"]["params"]["floors"], 24)
            self.assertEqual(parts["tower_main"]["bbox"]["max"][2], 102.0)
            self.assertEqual(parts["tower_main"]["buildMethod"], "build123d_step")
            self.assertEqual(parts["facade_grid_hint"]["hidden"], True)
            self.assertEqual(parts["facade_grid_hint"]["buildMethod"], "guide_only")
            self.assertTrue((case / "reports" / "semantic_parts.md").exists())
            self.assertTrue((case / "reports" / "semantic_plan.json").exists())
            self.assertTrue((case / "reports" / "semantic_validation.md").exists())
            plan = json.loads((case / "reports" / "semantic_plan.json").read_text(encoding="utf-8"))
            self.assertEqual(len(plan["parts"]), 5)
            self.assertIn("podium_oval", parts["tower_main"]["constraints"][0])

    def test_validate_candidate_compares_source_and_candidate_scan_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "cleanup",
                "--name",
                "candidate validation",
                "--root",
                str(root),
                "--source",
                "source.3dm",
                "--units",
                "m",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            source = ROOT / "tests" / "fixtures" / "scan_scene_sample.json"
            candidate = root / "candidate_scan.json"
            candidate.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            validated = run_cli("validate-candidate", str(case), "--source-scan", str(source), "--candidate-scan", str(candidate))
            self.assertEqual(validated.returncode, 0, validated.stdout + validated.stderr)
            report = json.loads((case / "reports" / "candidate_validation.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["summary"]["maxSizeDelta"], 0.0)
            self.assertTrue((case / "reports" / "candidate_validation.md").exists())

            bad = json.loads(source.read_text(encoding="utf-8"))
            bad["objects"][0]["bbox"]["max"][2] = 120
            bad_candidate = root / "bad_candidate_scan.json"
            bad_candidate.write_text(json.dumps(bad), encoding="utf-8")
            failed = run_cli(
                "validate-candidate",
                str(case),
                "--source-scan",
                str(source),
                "--candidate-scan",
                str(bad_candidate),
            )
            self.assertEqual(failed.returncode, 1)
            failed_report = json.loads((case / "reports" / "candidate_validation.json").read_text(encoding="utf-8"))
            self.assertEqual(failed_report["status"], "fail")
            self.assertIn("z", failed_report["failures"]["sizeAxes"])

    def test_import_semantic_obj_validates_unknown_keys_and_post_ops(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            created = run_cli(
                "new-case",
                "--scenario",
                "reference",
                "--name",
                "semantic validation",
                "--root",
                str(root),
                "--units",
                "m",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            case = Path(created.stdout.strip())
            source = root / "bad.live.obj"
            source.write_text(
                "\n".join(
                    [
                        "#@scene",
                        "#@units: meters",
                        "o test_part",
                        "#@source: procedural",
                        "#@type: box",
                        "#@params: width=1, depth=1, height=1",
                        "#@bbox: min=[0,0,0] max=[1,1,1]",
                        "#@banana: surprise",
                        "#@post: teleport distance=10",
                        "v 0 0 0",
                        "f 1 1 1",
                    ]
                ),
                encoding="utf-8",
            )

            imported = run_cli("import-semantic-obj", str(case), "--source", str(source))
            self.assertEqual(imported.returncode, 0, imported.stdout + imported.stderr)
            data = json.loads((case / "reports" / "semantic_parts.json").read_text(encoding="utf-8"))
            warnings = "\n".join(data["validation"]["warnings"])
            self.assertEqual(data["validation"]["status"], "valid")
            self.assertIn("unknown part metadata key: banana", warnings)
            self.assertIn("unsupported post op: teleport", warnings)

    def test_rhino_common_helper_lists_ops_and_dry_runs(self) -> None:
        listed = run_helper("list-ops")
        self.assertEqual(listed.returncode, 0, listed.stdout + listed.stderr)
        self.assertIn("read-visible-curves", listed.stdout)
        self.assertIn("curve-difference-2d", listed.stdout)

        dry = run_helper("--dry-run", "read-visible-curves")
        self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
        self.assertIn("visible_curves", dry.stdout)
        self.assertIn("RhinoDoc", dry.stdout)

        soft = run_helper(
            "--dry-run",
            "make-soft-closed-curve",
            "--points",
            "[[0,0,0],[8,0,0],[10,5,0],[5,9,0],[0,5,0]]",
        )
        self.assertEqual(soft.returncode, 0, soft.stdout + soft.stderr)
        self.assertIn("Curve.CreateControlPointCurve", soft.stdout)
        self.assertIn("RC_HELPER_curves", soft.stdout)


if __name__ == "__main__":
    unittest.main()
