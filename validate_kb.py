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

for path in markdown:
    content = (root / path).read_text(encoding="utf-8")
    if re.search(r"\b\d{2,5}\s+(?:E|W|N|S)\s+\w+(?:\s+\w+)?\s+(?:St|Street|Ave|Avenue|Rd|Road)\b", content, flags=re.I):
        errors.append(f"potential street address in {path}")

result = {"markdown_files": len(markdown), "links_checked": links_checked,
          "cataloged_uploads": len(records), "errors": errors}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
