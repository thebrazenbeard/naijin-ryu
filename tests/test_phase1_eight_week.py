"""Test positive and adversarial mutations of the eight-week course index."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.verify_phase1_course import verify

REAL_ROOT = Path(__file__).resolve().parents[1]


class EightWeekCourseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        paths = [
            "data/training-phase1-eight-week-v1.json",
            "data/training-restart-week-v1.json",
            "data/intake-register-v1.json",
            "programs/martial-training/phase-1-restart-week.md",
            "programs/martial-training/phase-1-eight-week-course.md",
        ] + [f"programs/martial-training/phase-1-week-{w:02d}.md" for w in range(2, 9)]
        for name in paths:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REAL_ROOT / name, dest)
        self.path = self.root / paths[0]
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")

    def test_all_thirty_two_sessions(self):
        x = verify(self.root)
        self.assertEqual(x["errors"], [], x)
        self.assertEqual(x["planned_sessions"], 32)

    def test_missing_week_is_rejected(self):
        (self.root / "programs/martial-training/phase-1-week-05.md").unlink()
        self.assertIn("W5:missing-document", verify(self.root)["errors"])

    def test_week_order_is_rejected(self):
        self.data["weeks"][2]["week"] = 9
        self.save()
        self.assertIn("weeks-2-through-8-required", verify(self.root)["errors"])

    def test_unsupported_qualification_is_rejected(self):
        self.data["status"] = "APPROVED_CONTACT_TRAINING"
        self.save()
        self.assertIn("unsupported-course-qualification", verify(self.root)["errors"])

    def test_automatic_advancement_is_rejected(self):
        self.data["automatic_advancement"] = True
        self.save()
        self.assertIn("automatic-advancement-prohibited", verify(self.root)["errors"])

    def test_mandatory_contact_is_rejected(self):
        self.data["mandatory_contact"] = True
        self.save()
        self.assertIn("contact-not-optional", verify(self.root)["errors"])

    def test_restricted_source_is_rejected(self):
        self.data["source_basis"][0] = "NRY-015"
        self.save()
        self.assertIn("restricted-or-missing-source", verify(self.root)["errors"])

    def test_markdown_time_drift_is_rejected(self):
        p = self.root / "programs/martial-training/phase-1-week-03.md"
        p.write_text(p.read_text(encoding="utf-8").replace("**5–11 min**", "**5–12 min**", 1), encoding="utf-8")
        self.assertIn("W3A:time-block-drift", verify(self.root)["errors"])

    def test_missing_easier_option_is_rejected(self):
        self.data["weeks"][0]["sessions"][0]["easier_option"] = "INVENTED NONEXISTENT ALTERNATIVE"
        self.save()
        self.assertIn("W2A:easier_option-missing", verify(self.root)["errors"])

    def test_mismatched_pillar_is_rejected(self):
        self.data["weeks"][0]["sessions"][1]["pillar"] = "Shock"
        self.save()
        self.assertIn("W2B:wrong-pillar", verify(self.root)["errors"])


if __name__ == "__main__":
    unittest.main()
