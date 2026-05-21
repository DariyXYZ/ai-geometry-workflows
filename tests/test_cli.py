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


if __name__ == "__main__":
    unittest.main()
