"""Regression tests for private raw-hash reconciliation and publication redaction."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from tools.verify_private_intake import verify


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.sources = self.base / "originals"
        self.sources.mkdir()
        (self.sources / "draft.txt").write_bytes(b"not public")
        self.private = self.base / "private.json"
        self.public = self.base / "public.json"
        digest = hashlib.sha256(b"not public").hexdigest()
        self.entry = {"local_id": "NRY-001", "relative_path": "draft.txt",
                      "status": "ACCEPTED", "sha256": digest}
        self.item = {"source_id": "NRY-001", "publication": "review-required",
                     "raw_sha256": digest, "display": "draft.txt", "ingest": "ADMITTED"}
        self.write()

    def write(self):
        self.private.write_text(json.dumps({"sources": [self.entry]}), encoding="utf-8")
        self.public.write_text(json.dumps({"items": [self.item]}), encoding="utf-8")

    def check(self):
        return verify(self.sources, self.private, self.public)

    def test_all_bytes_match(self):
        self.assertEqual(self.check()["status"], "PASS")

    def test_modified_source_fails(self):
        (self.sources / "draft.txt").write_bytes(b"changed")
        self.assertIn("NRY-001:private-hash-mismatch", self.check()["errors"])

    def test_path_escape_is_rejected(self):
        self.entry["relative_path"] = "../not-in-root.txt"
        self.write()
        self.assertIn("NRY-001:invalid-relative-path", self.check()["errors"])

    def test_restricted_record_does_not_publish_name_or_hash(self):
        self.item.update({"publication": "restricted", "display": "WITHHELD PRIVATE SOURCE NRY-001",
                          "raw_sha256": None})
        self.write()
        self.assertEqual(self.check()["status"], "PASS")
        self.item["raw_sha256"] = self.entry["sha256"]
        self.write()
        self.assertIn("NRY-001:privacy-redaction-failure", self.check()["errors"])



    def test_private_source_cannot_be_reclassified_as_public(self):
        self.entry["visibility"] = "PRIVATE"
        self.write()
        self.assertIn("NRY-001:private-source-declassified", self.check()["errors"])

    def test_graphic_source_must_be_restricted(self):
        (self.sources / "draft.txt").rename(self.sources / "figure.jpg")
        self.entry["relative_path"] = "figure.jpg"
        self.item["display"] = "figure.jpg"
        self.write()
        self.assertIn("NRY-001:private-source-declassified", self.check()["errors"])

if __name__ == "__main__":
    unittest.main()
