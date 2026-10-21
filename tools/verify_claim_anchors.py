"""Verify public source claims and optionally their exact private DOCX anchors.

The public-only pass checks claim identity, publication boundaries and documentation
paths. The private pass rechecks source bytes and Word text without exporting either.
An anchor proves document-level wording, not its section boundary, truth or origin.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value).casefold()).strip()


def word_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        member = archive.getinfo("word/document.xml")
        if member.file_size > 12_000_000:
            raise ValueError("document XML size exceeds review cap")
        raw = archive.read(member)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(raw)
    paragraphs = root.iter(ns + "p")
    text = "\n".join("".join(t.text or "" for t in p.iter(ns + "t"))
                     for p in paragraphs)
    return normalize(text)


def verify(repo: Path, *, source_root: Path | None = None,
           private_manifest: Path | None = None) -> dict:
    register = json.loads((repo / "data/source-claim-register-v1.json").read_text(encoding="utf-8"))
    intake = json.loads((repo / "data/intake-register-v1.json").read_text(encoding="utf-8"))
    claims = register["claims"]
    items = {x["source_id"]: x for x in intake["items"]}
    errors: list[str] = []
    seen: set[str] = set()
    anchor_count = 0
    for claim in claims:
        cid = claim["id"]
        if cid in seen or not re.fullmatch(r"NRY-C\d{3}", cid):
            errors.append(f"{cid}:invalid-or-duplicate-id")
        seen.add(cid)
        if claim.get("evidence_status") != "SOURCE_RECORDED":
            errors.append(f"{cid}:invalid-evidence-status")
        if claim.get("claim_type") not in register["claim_types"]:
            errors.append(f"{cid}:unknown-claim-type")
        s = claim["source"]
        sid = s["source_id"]
        item = items.get(sid)
        if item is None:
            errors.append(f"{cid}:missing-source-id")
            continue
        if item["publication"] == "restricted":
            errors.append(f"{cid}:restricted-source-citation")
        if not str(s.get("locator", "")).strip():
            errors.append(f"{cid}:missing-locator")
        anchors = s.get("anchors")
        if not isinstance(anchors, list) or not anchors or not all(
            isinstance(x, str) and 3 <= len(x.strip()) <= 160 for x in anchors
        ):
            errors.append(f"{cid}:invalid-anchors")
            continue
        target = (repo / claim["public_document"]).resolve()
        if not target.is_relative_to(repo.resolve()) or not target.is_file():
            errors.append(f"{cid}:invalid-document")
        if not claim.get("limitation") or not claim.get("statement"):
            errors.append(f"{cid}:missing-claim-boundary")
        anchor_count += len(anchors)
    checked = 0
    if (source_root is None) != (private_manifest is None):
        errors.append("private-source-and-manifest-must-be-paired")
    if source_root is not None and private_manifest is not None:
        root = source_root.resolve(strict=True)
        raw = json.loads(private_manifest.read_text(encoding="utf-8"))
        private = {x["local_id"]: x for x in raw["sources"]}
        cached: dict[str, str] = {}
        for claim in claims:
            cid = claim["id"]
            sid = claim["source"]["source_id"]
            if sid not in items or sid not in private:
                errors.append(f"{cid}:missing-private-source")
                continue
            source = private[sid]
            rel = str(source["relative_path"]).replace("\\", "/")
            if rel.startswith("/") or ".." in Path(rel).parts or ":" in rel:
                errors.append(f"{cid}:unsafe-relative-path")
                continue
            try:
                path = root.joinpath(*rel.split("/")).resolve(strict=True)
                if not path.is_relative_to(root) or not path.is_file():
                    raise ValueError("not within source root")
                if path.suffix.lower() != ".docx":
                    errors.append(f"{cid}:non-word-source-requires-separate-extractor")
                    continue
                if sid not in cached:
                    b = path.read_bytes()
                    if len(b) > 50_000_000 or hashlib.sha256(b).hexdigest() != source["sha256"]:
                        errors.append(f"{cid}:source-drift")
                        continue
                    cached[sid] = word_text(path)
                for anchor in claim["source"]["anchors"]:
                    if normalize(anchor) not in cached[sid]:
                        errors.append(f"{cid}:anchor-not-found")
                    else:
                        checked += 1
            except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError):
                errors.append(f"{cid}:source-read-failed")
    return {"schema": "NRY_CLAIM_ANCHOR_CHECK_V1",
            "status": "PASS" if not errors else "FAIL",
            "claims": len(claims), "declared_anchors": anchor_count,
            "private_anchors_verified": checked, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--private-manifest", type=Path)
    a = parser.parse_args()
    try:
        result = verify(a.repo, source_root=a.source_root, private_manifest=a.private_manifest)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {"schema":"NRY_CLAIM_ANCHOR_CHECK_V1","status":"FAIL",
                  "errors":["unreadable-input:"+type(exc).__name__]}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
