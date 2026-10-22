"""Validate Markdown links, source manifest, and basic privacy on a repo checkout."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and ".git" not in p.parts}
errors = []
links_checked = 0
markdown = sorted(p for p in files if p.endswith(".md"))

for path in markdown:
    content = (root / path).read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
        target = match.group(1).split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (root / path).parent.joinpath(target).resolve()
        links_checked += 1
        if not resolved.is_relative_to(root) or not resolved.is_file():
            errors.append(f"broken link {path}: {target}")

manifest_path = root / "data/source-manifest.json"
if not manifest_path.is_file():
    errors.append("missing source manifest")
    records = []
else:
    try:
        obj = json.loads(manifest_path.read_text(encoding="utf-8"))
        records = obj["files"]
        if len(records) != 9:
            errors.append(f"source count {len(records)} != 9")
        ids = [r["id"] for r in records]
        if len(ids) != len(set(ids)):
            errors.append("duplicate source IDs")
        for r in records:
            if not re.fullmatch(r"[0-9a-f]{64}", r["sha256"]):
                errors.append(f"invalid SHA256: {r['id']}")
    except (KeyError, ValueError, TypeError) as exc:
        records = []
        errors.append(f"invalid source manifest: {exc}")

intake_path = root / "data/intake-register-v1.json"
if not intake_path.is_file():
    errors.append("missing 30-source intake register")
else:
    try:
        intake = json.loads(intake_path.read_text(encoding="utf-8"))
        items = intake["items"]
        if len(items) != 30:
            errors.append(f"intake count {len(items)} != 30")
        ids = [i["source_id"] for i in items]
        if len(ids) != len(set(ids)):
            errors.append("duplicate intake IDs")
        for item in items:
            if item["ingest"] != "ADMITTED":
                errors.append("source not admitted: " + item["source_id"])
            sha = item.get("raw_sha256")
            if item["publication"] == "restricted" and sha:
                errors.append("restricted raw SHA published: " + item["source_id"])
            if sha and not re.fullmatch(r"[0-9a-f]{64}", sha):
                errors.append("invalid intake SHA: " + item["source_id"])
    except (KeyError, ValueError, TypeError) as exc:
        errors.append(f"bad intake register: {exc}")

roots_path = root / "data/foundation-roots-receipt.json"
if not roots_path.is_file():
    errors.append("missing Roots public receipt")
else:
    try:
        roots = json.loads(roots_path.read_text(encoding="utf-8"))
        if roots["origin_status"] != "UNRESOLVED" or roots["completeness"] != "PARTIAL":
            errors.append("Roots claim exceeds evidence")
        if any(not c["passed"] for c in roots["claim_strength_checks"]):
            errors.append("Roots claim check failure")
    except (KeyError, ValueError, TypeError) as exc:
        errors.append(f"bad Roots public receipt: {exc}")

for path in markdown:
    content = (root / path).read_text(encoding="utf-8")
    if re.search(r"\b\d{2,5}\s+(?:E|W|N|S)\s+\w+(?:\s+\w+)?\s+(?:St|Street|Ave|Avenue|Rd|Road)\b", content, flags=re.I):
        errors.append(f"potential street address in {path}")

# Validate publication-safe primary-source claim structure without private files.
try:
    from tools.verify_claim_anchors import verify as check_source_claims
    claim_check = check_source_claims(root)
    for error in claim_check["errors"]:
        errors.append("source claim: " + error)
except (OSError, KeyError, ValueError, TypeError) as exc:
    claim_check = {"claims": 0, "declared_anchors": 0}
    errors.append("invalid source claim register: " + type(exc).__name__)
# Validate program workstream registry; branch-ref existence is checked via GitHub separately.
try:
    from tools.verify_program_registry import verify as check_programs
    program_check = check_programs(root)
    for error in program_check["errors"]:
        errors.append("program registry: " + error)
except (OSError, ValueError, KeyError, TypeError) as exc:
    program_check = {"workstreams": 0}
    errors.append("invalid program registry: " + type(exc).__name__)

# Source-bounded, public-only Phase 1 restart plan integrity.
try:
    from tools.verify_training_restart import verify as check_training_restart
    training_check = check_training_restart(root)
    for error in training_check["errors"]:
        errors.append("training restart: " + error)
except (OSError, KeyError, ValueError, TypeError) as exc:
    training_check = {"sessions": 0, "planned_minutes": 0}
    errors.append("invalid training restart: " + type(exc).__name__)

result = {"markdown_files": len(markdown), "links_checked": links_checked,
          "cataloged_uploads": len(records), "source_claims": claim_check["claims"],
          "source_anchors_declared": claim_check["declared_anchors"],
          "program_workstreams": program_check["workstreams"],
          "training_sessions": training_check["sessions"],
          "training_restart_minutes": training_check["planned_minutes"], "errors": errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
