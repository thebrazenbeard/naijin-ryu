"""Regression coverage for program workstream topology and privacy boundaries."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.verify_program_registry import verify

REPO = Path(__file__).resolve().parents[1]


class ProgramRegistryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "repo"
        shutil.copytree(REPO, self.root,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        self.file = self.root / "data/program-workstreams.json"
        self.data = json.loads(self.file.read_text(encoding="utf-8"))

    def save(self):
        self.file.write_text(json.dumps(self.data), encoding="utf-8")

    def test_five_valid_lanes(self):
        result = verify(self.root)
        self.assertEqual(result["workstreams"], 5)
        self.assertEqual(result["status"], "PASS")

    def test_unrelated_horror_cannot_become_active_naijin_ryu_program(self):
        item = dict(self.data["programs"][0])
        item["id"] = "horror-immersion"
        item["branch"] = "program/horror-immersion"
        item["root"] = "programs/horror-immersion/README.md"
        self.data["programs"].append(item)
        self.save()
        self.assertIn("unrelated-horror-reclassified-as-naijin-ryu",
                      verify(self.root)["errors"])

    def test_separate_concept_cannot_be_lost(self):
        self.data.pop("non_program_concepts", None)
        self.save()
        self.assertIn("separate-horror-provenance-not-preserved",
                      verify(self.root)["errors"])

    def test_duplicate_branch_is_rejected(self):
        self.data["programs"][1]["branch"] = self.data["programs"][0]["branch"]
        self.save()
        self.assertEqual(verify(self.root)["status"], "FAIL")

    def test_wrong_landing_path_is_rejected(self):
        self.data["programs"][0]["root"] = "programs/elsewhere/README.md"
        self.save()
        self.assertEqual(verify(self.root)["status"], "FAIL")

    def test_restricted_source_citation_is_rejected(self):
        self.data["programs"][0]["source_ids"].append("NRY-015")
        self.save()
        self.assertTrue(any("restricted-source-citation" in e
                            for e in verify(self.root)["errors"]))

    def test_unverified_operation_status_rejected(self):
        self.data["programs"][3]["status"] = "OPEN-FOR-ENROLLMENT"
        self.save()
        self.assertTrue(any("invalid-status" in e
                            for e in verify(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
