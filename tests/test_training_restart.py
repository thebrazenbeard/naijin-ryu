"""Negative tests for phase-one restart integrity and safety boundaries."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.verify_training_restart import verify

ROOT = Path(__file__).resolve().parents[1]


class TrainingRestartValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repository"
        self.root.mkdir()
        (self.root / "data").mkdir()
        (self.root / "programs/martial-training").mkdir(parents=True)
        for name in ("data/intake-register-v1.json",
                     "data/training-restart-week-v1.json",
                     "programs/martial-training/phase-1-progression-gates.md"):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        for sid in "abcd":
            name = f"programs/martial-training/phase-1-session-{sid}.md"
            shutil.copyfile(ROOT / name, self.root / name)
        self.path = self.root / "data/training-restart-week-v1.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def save(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")

    def test_four_days_are_valid(self):
        result = verify(self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["sessions"], 4)
        self.assertEqual(result["planned_minutes"], 105)

    def test_duration_mismatch_is_detected(self):
        self.data["sessions"][1]["segments"][2]["minutes"] += 1
        self.save()
        self.assertIn("B:duration-does-not-add-up", verify(self.root)["errors"])

    def test_markdown_clock_drift_is_detected(self):
        file = self.root / "programs/martial-training/phase-1-session-c.md"
        file.write_text(file.read_text(encoding="utf-8").replace(
            "**5–13 min**", "**5–14 min**"
        ), encoding="utf-8")
        self.assertIn("C:time-range-mismatch", verify(self.root)["errors"])

    def test_extra_day_is_rejected(self):
        self.data["sessions"].append(dict(self.data["sessions"][0], id="E"))
        self.save()
        self.assertEqual(verify(self.root)["status"], "FAIL")

    def test_writing_contact_as_mandatory_is_rejected(self):
        self.data["mandatory_contact"] = True
        self.save()
        self.assertIn("contact-must-not-be-required", verify(self.root)["errors"])

    def test_martial_source_cannot_be_swapped_for_restricted(self):
        self.data["source_ids"] = ["NRY-013", "NRY-015"]
        self.save()
        self.assertIn("restricted-source-reference", verify(self.root)["errors"])

    def test_prepared_plan_cannot_call_itself_qualified(self):
        self.data["status"] = "CLINICALLY_VALIDATED"
        self.save()
        self.assertIn("unqualified-authority-claim", verify(self.root)["errors"])

    def test_wrong_pillar_is_rejected(self):
        self.data["sessions"][1]["pillar"] = "Shock"
        self.save()
        self.assertIn("B:wrong-pillar", verify(self.root)["errors"])

    def test_lost_document_is_rejected(self):
        (self.root / "programs/martial-training/phase-1-session-d.md").unlink()
        self.assertIn("D:missing-document", verify(self.root)["errors"])


if __name__ == "__main__":
    unittest.main()
