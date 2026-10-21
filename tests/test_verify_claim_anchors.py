"""Hostile/negative checks for public source references and private anchors."""
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.verify_claim_anchors import verify, word_text


class ClaimChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.originals = self.root / "source"
        (self.repo / "data").mkdir(parents=True)
        (self.repo / "docs").mkdir()
        self.originals.mkdir()
        (self.repo / "docs/guide.md").write_text("Study", encoding="utf-8")
        self.word = self.originals / "sample.docx"
        self._write_docx("First part of source claim")
        self.source = {"local_id": "NRY-001", "status": "ACCEPTED",
                       "relative_path": "sample.docx", "sha256": self._hash()}
        self.intake = {"source_id": "NRY-001", "publication": "review-required"}
        self.claim = {"id": "NRY-C001", "claim_type": "SPIRITUAL_PRACTICE",
                      "evidence_status": "SOURCE_RECORDED",
                      "statement": "Source phrase exists",
                      "source": {"source_id": "NRY-001", "locator": "section one",
                                 "anchors": ["First part of source claim"]},
                      "public_document": "docs/guide.md",
                      "limitation": "This is source only."}
        self.manifest = self.root / "private.json"
        self._sync()

    def _write_docx(self, text):
        prefix = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>'
        suffix = '</w:t></w:r></w:p></w:body></w:document>'
        with zipfile.ZipFile(self.word, "w") as z:
            z.writestr("word/document.xml", prefix + text + suffix)

    def _hash(self):
        return hashlib.sha256(self.word.read_bytes()).hexdigest()

    def _sync(self):
        (self.repo / "data/intake-register-v1.json").write_text(
            json.dumps({"items": [self.intake]}), encoding="utf-8")
        (self.repo / "data/source-claim-register-v1.json").write_text(
            json.dumps({"claim_types": ["SPIRITUAL_PRACTICE"],
                        "claims": [self.claim]}), encoding="utf-8")
        self.manifest.write_text(json.dumps({"sources": [self.source]}), encoding="utf-8")

    def _check(self):
        return verify(self.repo, source_root=self.originals,
                      private_manifest=self.manifest)

    def test_public_and_private_complete(self):
        self.assertEqual(self._check()["status"], "PASS")
        self.assertEqual(self._check()["private_anchors_verified"], 1)

    def test_anchor_does_not_exist(self):
        self.claim["source"]["anchors"] = ["Invented evidence anchor"]
        self._sync()
        self.assertIn("NRY-C001:anchor-not-found", self._check()["errors"])

    def test_raw_docx_drift_detected(self):
        self._write_docx("A rewritten phrase after ingestion")
        self.assertIn("NRY-C001:source-drift", self._check()["errors"])

    def test_restricted_source_cannot_support_public_claim(self):
        self.intake["publication"] = "restricted"
        self._sync()
        self.assertIn("NRY-C001:restricted-source-citation", self._check()["errors"])

    def test_source_escape_rejected(self):
        self.source["relative_path"] = "../sample.docx"
        self._sync()
        self.assertIn("NRY-C001:unsafe-relative-path", self._check()["errors"])

    def test_public_document_escape_rejected(self):
        self.claim["public_document"] = "../private.md"
        self._sync()
        self.assertIn("NRY-C001:invalid-document", self._check()["errors"])

    def test_claim_type_cannot_be_upgraded(self):
        self.claim["evidence_status"] = "VERIFIED_TRUE"
        self._sync()
        self.assertIn("NRY-C001:invalid-evidence-status", self._check()["errors"])

    def test_split_word_runs_are_joined(self):
        text = ('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                '<w:body><w:p><w:r><w:t>First part</w:t></w:r>'
                '<w:r><w:t> of source claim</w:t></w:r></w:p></w:body></w:document>')
        with zipfile.ZipFile(self.word, "w") as z:
            z.writestr("word/document.xml", text)
        self.source["sha256"] = self._hash()
        self._sync()
        self.assertIn("first part of source claim", word_text(self.word))
        self.assertEqual(self._check()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
