"""Recheck private source bytes against a redacted public Ingest index.
This script neither copies nor publishes originals. Restricted paths stay private.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def verify(root, manifest, index):
    originals = json.loads(manifest.read_text(encoding="utf-8"))["sources"]
    listed = json.loads(index.read_text(encoding="utf-8"))["items"]
    by_id = {x["source_id"]: x for x in listed}
    errors = []
    seen = set()
    checked = 0
    root = root.resolve(strict=True)
    for source in originals:
        sid = source["local_id"]
        if sid in seen:
            errors.append(sid + ":duplicate-id")
        seen.add(sid)
        item = by_id.get(sid)
        if item is None:
            errors.append(sid + ":missing-index")
            continue
        relative = str(source["relative_path"]).replace("\\", "/")
        rel = PurePosixPath(relative)
        if rel.is_absolute() or ".." in rel.parts or ":" in relative:
            errors.append(sid + ":invalid-relative-path")
            continue
        if source.get("status") not in {"ACCEPTED", "DUPLICATE"}:
            errors.append(sid + ":not-admitted")
            continue
        try:
            resolved = root.joinpath(*rel.parts).resolve(strict=True)
            if not resolved.is_relative_to(root) or not resolved.is_file():
                raise OSError("path outside root")
            h = hashlib.sha256()
            with resolved.open("rb") as f:
                while chunk := f.read(1024 * 1024):
                    h.update(chunk)
            actual = h.hexdigest()
            checked += 1
        except (OSError, RuntimeError, ValueError):
            errors.append(sid + ":source-inaccessible")
            continue
        if source["sha256"] != actual:
            errors.append(sid + ":private-hash-mismatch")
        if item.get("ingest") != "ADMITTED":
            errors.append(sid + ":not-indexed-as-admitted")
        if source.get("visibility") == "PRIVATE" or rel.suffix.lower() in (".png", ".jpg", ".jpeg"):
            if item["publication"] != "restricted":
                errors.append(sid + ":private-source-declassified")
        if item["publication"] == "restricted":
            if item.get("raw_sha256") is not None or not item["display"].startswith("WITHHELD PRIVATE SOURCE "):
                errors.append(sid + ":privacy-redaction-failure")
        else:
            if item.get("raw_sha256") != actual:
                errors.append(sid + ":public-hash-mismatch")
            if item["display"] != rel.name:
                errors.append(sid + ":published-name-mismatch")
    if seen != set(by_id) or len(seen) != len(originals) or len(by_id) != len(listed):
        errors.append("source-set-mismatch")
    return {"schema": "NRY_LOCAL_HASH_RECHECK_V1",
            "status": "FAIL" if errors else "PASS",
            "source_count": len(originals),
            "bytes_rechecked": checked,
            "restricted_count": sum(x["publication"] == "restricted" for x in listed),
            "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--private-manifest", type=Path, required=True)
    parser.add_argument("--public-index", type=Path, default=Path(__file__).resolve().parents[1] / "data/intake-register-v1.json")
    a = parser.parse_args()
    try:
        result = verify(a.source_root, a.private_manifest, a.public_index)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {"schema": "NRY_LOCAL_HASH_RECHECK_V1", "status": "FAIL",
                  "errors": ["manifest-or-root:" + type(exc).__name__]}
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result["status"] == "FAIL" else 0)
