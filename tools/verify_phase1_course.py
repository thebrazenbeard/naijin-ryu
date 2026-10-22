"""Machine-check an editorial 32-session Phase 1 solo course.

This verifies documentation and source boundaries only. It cannot establish
physical safety, instructor qualification, contact skill, or training outcomes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DAYS = {"A": "Shock", "B": "Unbalance", "C": "Reversal", "D": "Grapple"}
CLOCK = re.compile(r"^\| \*\*(\d+)[–-](\d+) min\*\* \| ([^|]+) \| ([^|]+) \|$", re.M)
HEADER = re.compile(r"^## ([ABCD]) — ([^:\n]+): ([^\n]+) \((\d+) min\)\s*$", re.M)


def verify(root: Path) -> dict:
    errors: list[str] = []
    count = 0
    try:
        root = root.resolve()
        course = json.loads((root / "data/training-phase1-eight-week-v1.json").read_text(encoding="utf-8"))
        base = json.loads((root / "data/training-restart-week-v1.json").read_text(encoding="utf-8"))
        intake = json.loads((root / "data/intake-register-v1.json").read_text(encoding="utf-8"))
        public_sources = {x["source_id"] for x in intake["items"] if x["publication"] != "restricted"}
        if (course.get("schema") != "NRY_PHASE1_EIGHT_WEEK_COURSE_V1"
                or course.get("program_id") != "martial-training"
                or course.get("phase") != "Phase 1"):
            errors.append("wrong-course-identity")
        if course.get("status") != "EDITORIAL_SOLO_COURSE_NOT_INSTRUCTOR_QUALIFIED":
            errors.append("unsupported-course-qualification")
        if course.get("automatic_advancement") is not False:
            errors.append("automatic-advancement-prohibited")
        if course.get("mandatory_contact") is not False:
            errors.append("contact-not-optional")
        if course.get("allowed_to_repeat_weeks") is not True:
            errors.append("week-repeat-required")
        if set(course.get("source_basis", [])) != {"NRY-013", "NRY-009", "NRY-012", "NRY-007"}:
            errors.append("unexpected-source-basis")
        if any(x not in public_sources for x in course.get("source_basis", [])):
            errors.append("restricted-or-missing-source")
        if not course.get("privacy") or not course.get("editorial_statement"):
            errors.append("missing-privacy-or-editorial-scope")
        base_days = base["sessions"]
        base_by_id = {d["id"]: d for d in base_days}
        if set(base_by_id) != set(DAYS):
            errors.append("base-week-incomplete")
        reference = course["week_one"]
        if (reference.get("week") != 1
                or reference.get("document") != "programs/martial-training/phase-1-restart-week.md"
                or reference.get("registry") != "data/training-restart-week-v1.json"
                or reference.get("sessions") != list(DAYS)):
            errors.append("week-one-reference-invalid")
        if not (root / reference["document"]).is_file():
            errors.append("missing-week-one")
        count += len(base_days)
        weeks = course.get("weeks", [])
        if len(weeks) != 7 or [w["week"] for w in weeks] != list(range(2, 9)):
            errors.append("weeks-2-through-8-required")
        for week in weeks:
            w = week["week"]
            expected_path = f"programs/martial-training/phase-1-week-{w:02d}.md"
            path = week.get("document")
            if path != expected_path:
                errors.append(f"W{w}:unexpected-document-path")
                continue
            target = (root / path).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f"W{w}:missing-document")
                continue
            text = target.read_text(encoding="utf-8")
            if not text.startswith(f"# Phase 1, Week {w} — {week['theme']}"):
                errors.append(f"W{w}:title-not-aligned")
            if week.get("gate", "") not in text:
                errors.append(f"W{w}:gate-not-shown")
            headers = list(HEADER.finditer(text))
            if [m.group(1) for m in headers] != list(DAYS):
                errors.append(f"W{w}:session-headings-not-four")
                continue
            entries = week.get("sessions", [])
            if len(entries) != 4 or [d["day"] for d in entries] != list(DAYS):
                errors.append(f"W{w}:session-data-not-four")
                continue
            for i, entry in enumerate(entries):
                day = entry["day"]
                count += 1
                base_day = base_by_id[day]
                marker = headers[i]
                page_part = text[marker.end():headers[i+1].start() if i < 3 else len(text).split("## Week ")[0].__len__()]
                # Use the text between neighboring headings; for D the table
                # remains before the week-level review heading.
                if i == 3:
                    page_part = text[marker.end():].split("## Week ", 1)[0]
                if entry["pillar"] != DAYS[day] or marker.group(2) != DAYS[day]:
                    errors.append(f"W{w}{day}:wrong-pillar")
                if marker.group(3) != entry["focus"]:
                    errors.append(f"W{w}{day}:focus-not-synced")
                if (int(marker.group(4)) != base_day["duration_minutes"]
                        or entry["duration_minutes"] != base_day["duration_minutes"]):
                    errors.append(f"W{w}{day}:duration-mismatch")
                for field in ("practice", "easier_option", "review_question"):
                    if not entry.get(field) or entry[field] not in page_part:
                        errors.append(f"W{w}{day}:{field}-missing")
                rows = list(CLOCK.findall(page_part))
                segments = base_day["segments"]
                if len(rows) != len(segments):
                    errors.append(f"W{w}{day}:missing-time-blocks")
                    continue
                clock = 0
                for start, end, label, desc in rows:
                    if int(start) != clock or int(end) - int(start) != segments[len([s for s in rows if int(s[0]) < int(start)])]["minutes"]:
                        errors.append(f"W{w}{day}:time-block-drift")
                        break
                    clock = int(end)
                if clock != entry["duration_minutes"]:
                    errors.append(f"W{w}{day}:clock-total-mismatch")
        if not (root / "programs/martial-training/phase-1-eight-week-course.md").is_file():
            errors.append("missing-course-index")
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        errors.append("course-unreadable:" + type(exc).__name__)
    return {"schema":"NRY_PHASE1_EIGHT_WEEK_CHECK_V1",
            "status":"PASS" if not errors else "FAIL",
            "planned_sessions":count,"errors":errors}


if __name__ == "__main__":
    import sys
    print(json.dumps(result := verify(Path(__file__).resolve().parents[1]), indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
