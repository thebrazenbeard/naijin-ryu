"""Validate public Naijin-Ryū program-to-branch registry without requiring GitHub access.

Git branch presence and head SHA must be verified separately after release.
"""
import json
import re
from pathlib import Path


def verify(root: Path) -> dict:
    errors = []
    try:
        o = json.loads((root / "data/program-workstreams.json").read_text(encoding="utf-8"))
        intake = json.loads((root / "data/intake-register-v1.json").read_text(encoding="utf-8"))
        if o.get("schema") != "NRY_PROGRAM_WORKSTREAMS_V1" or o.get("canonical_integration_branch") != "main":
            errors.append("invalid-schema-or-integration-branch")
        entries = o["programs"]
        indexed = {x["source_id"]: x for x in intake["items"]}
        ids = set()
        branches = set()
        roots = set()
        for item in entries:
            key = item["id"]
            b = item["branch"]
            p = item["root"]
            if not re.fullmatch(r"[a-z][a-z0-9-]{2,63}", key):
                errors.append("invalid-program-id:" + str(key))
            if key in ids or b in branches or p in roots:
                errors.append("duplicate-program-branch-or-path:" + str(key))
            ids.add(key)
            branches.add(b)
            roots.add(p)
            if b != "program/" + key:
                errors.append("branch-not-scoped-to-program:" + key)
            if p != "programs/" + key + "/README.md":
                errors.append("root-not-scoped-to-program:" + key)
            target = (root / p).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                errors.append("missing-program-landing:" + key)
            if not item.get("name") or not item.get("scope") or not item.get("privacy"):
                errors.append("incomplete-program-boundary:" + key)
            if item.get("status") not in (
                "SOURCE-BASED DEVELOPMENT", "CONCEPT-ONLY",
                "HISTORICAL-DRAFT-AND-FOUNDATION"
            ):
                errors.append("invalid-status:" + key)
            sources = item.get("source_ids", [])
            if not sources or len(set(sources)) != len(sources):
                errors.append("invalid-sources:" + key)
            for sid in sources:
                if sid not in indexed:
                    errors.append("missing-source:" + key)
                elif indexed[sid]["publication"] == "restricted":
                    errors.append("restricted-source-citation:" + key)
            for relative in item.get("shared_docs", []):
                ref = (root / relative).resolve()
                if not ref.is_relative_to(root.resolve()) or not ref.is_file():
                    errors.append("missing-shared-document:" + key)
        if len(entries) != 6:
            errors.append("unexpected-workstream-count")
        if "church-community" not in ids or "youth-camp" not in ids or "horror-immersion" not in ids:
            errors.append("missing-integrative-or-separated-camp-lanes")
    except (KeyError, ValueError, TypeError, OSError) as exc:
        errors.append("registry-read-failure:" + type(exc).__name__)
        entries = []
    return {"schema": "NRY_WORKSTREAM_REGISTRY_CHECK_V1",
            "status": "PASS" if not errors else "FAIL",
            "workstreams": len(entries), "errors": errors}


if __name__ == "__main__":
    import sys
    root = Path(__file__).resolve().parents[1]
    result = verify(root)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
