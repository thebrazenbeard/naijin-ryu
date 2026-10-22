"""Public-only mechanical verification for Phase 1 starter sessions.

This verifier checks referential integrity, evidence boundaries and session math.
It does NOT certify exercise safety, efficacy, readiness, or instructor authority.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

EXPECTED = {"A": "Shock", "B": "Unbalance", "C": "Reversal", "D": "Grapple"}
TIME_SPAN = re.compile(r"\*\*(\d+)\s*[–-]\s*(\d+)(?:\s*min)?\*\*")


def verify(root: Path) -> dict:
    errors: list[str] = []
    try:
        root = root.resolve()
        plan = json.loads(
            (root / "data/training-restart-week-v1.json").read_text(encoding="utf-8")
        )
        intake = json.loads(
            (root / "data/intake-register-v1.json").read_text(encoding="utf-8")
        )
        sources = {i["source_id"]: i for i in intake["items"]}
        if (plan.get("schema") != "NRY_TRAINING_RESTART_V1"
                or plan.get("program_id") != "martial-training"
                or plan.get("phase") != "Phase 1"):
            errors.append("incorrect-plan-identity")
        if plan.get("status") != "EDITORIAL_TEMPLATE_NOT_SAFETY_CERTIFIED":
            errors.append("unqualified-authority-claim")
        if plan.get("mandatory_contact") is not False:
            errors.append("contact-must-not-be-required")
        if plan.get("qualified_instructor_required_for_advanced_training") is not True:
            errors.append("supervision-gate-absent")
        if plan.get("session_order") != list(EXPECTED):
            errors.append("bad-session-order")
        if "not fifth" not in str(plan.get("environment_scope", "")):
            errors.append("environment-fifth-day-confusion")
        if plan.get("source_ids") != ["NRY-013", "NRY-009"]:
            errors.append("unexpected-source-basis")
        for source_id in plan["source_ids"]:
            if source_id not in sources:
                errors.append("missing-source-id")
            elif sources[source_id].get("publication") == "restricted":
                errors.append("restricted-source-reference")
        entries = plan["sessions"]
        found = set()
        minutes_total = 0
        documents = set()
        for entry in entries:
            sid = entry["id"]
            if sid in found or sid not in EXPECTED:
                errors.append(f"{sid}:unexpected-or-duplicate-session")
                continue
            found.add(sid)
            if entry.get("pillar") != EXPECTED[sid]:
                errors.append(f"{sid}:wrong-pillar")
            path = entry.get("document")
            correct = f"programs/martial-training/phase-1-session-{sid.lower()}.md"
            if path != correct or path in documents:
                errors.append(f"{sid}:document-path-mismatch")
                continue
            documents.add(path)
            target = (root / path).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f"{sid}:missing-document")
                continue
            segments = entry["segments"]
            dur = entry["duration_minutes"]
            if (type(dur) is not int or not (15 <= dur <= 60)
                    or not isinstance(segments, list) or len(segments) != 5):
                errors.append(f"{sid}:invalid-duration-or-segments")
                continue
            if not all(
                isinstance(s, dict)
                and isinstance(s.get("name"), str) and s["name"].strip()
                and type(s.get("minutes")) is int and s["minutes"] > 0
                for s in segments
            ):
                errors.append(f"{sid}:invalid-segment")
                continue
            if sum(s["minutes"] for s in segments) != dur:
                errors.append(f"{sid}:duration-does-not-add-up")
            minutes_total += dur
            spans = [(int(a), int(b)) for a, b in
                     TIME_SPAN.findall(target.read_text(encoding="utf-8"))]
            # Read the first five bold minute ranges from the main timing table;
            # further prose ranges are not interpreted as actual schedule blocks.
            spans = spans[:len(segments)]
            if len(spans) != len(segments):
                errors.append(f"{sid}:missing-time-ranges")
            else:
                clock = 0
                for (start, end), segment in zip(spans, segments):
                    if start != clock or end-start != segment["minutes"]:
                        errors.append(f"{sid}:time-range-mismatch")
                        break
                    clock = end
                if clock != dur:
                    errors.append(f"{sid}:final-timestamp-mismatch")
        if found != set(EXPECTED) or len(entries) != 4:
            errors.append("incomplete-four-day-phase-one")
        target = (root / plan["progression_document"]).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            errors.append("missing-progression-document")
        if not plan.get("privacy") or not plan.get("source_boundaries"):
            errors.append("missing-provenance-or-privacy")
    except (ValueError, KeyError, OSError, TypeError) as exc:
        entries = []
        minutes_total = 0
        errors.append("unreadable-program:" + type(exc).__name__)
    return {"schema": "NRY_TRAINING_RESTART_VALIDATION_V1",
            "status": "PASS" if not errors else "FAIL",
            "sessions": len(entries), "planned_minutes": minutes_total,
            "errors": errors}


if __name__ == "__main__":
    import sys
    print(json.dumps(result := verify(Path(__file__).resolve().parents[1]), indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
