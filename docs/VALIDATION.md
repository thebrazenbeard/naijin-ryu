# Knowledge-base validation checklist

This file defines testable quality requirements for future additions. It does not claim that a markdown checker verifies martial efficacy, spiritual claims or legal compliance.

## Repository integrity

1. Each local Markdown link resolves to a file in this exact branch.
2. `data/source-manifest.json` has nine valid uploaded-source records and SHA-256 hashes; `data/intake-register-v1.json` has **30** unique admitted records, with restricted content hashes withheld.
3. All nine locally uploaded source artifacts have unique IDs.
4. No published source-identifying URLs, private addresses, medical records, personal reflection extracts or full injurious last-resort procedures are silently introduced.
5. Core doctrine is not silently rewritten by editorial harmonization.
6. Calendar alternatives remain traceable to original documents.
7. Roots' public receipt remains explicitly **PARTIAL / UNRESOLVED**, with validated claim-strength checks.
8. External source code commits and observed run results are identified, without treating either as a permanent deployment.
9. Research citations distinguish source assertions from independently checked evidence.

## Recheck the private corpus locally

For an authorized operator with the separately held private manifest, run `python tools/verify_private_intake.py --source-root <local OneDrive Naijin-Ryu folder> --private-manifest <private intake-manifest-private.json>`. The local tool re-hashes all 30 originals, compares nonrestricted public hashes, and verifies that restricted public entries contain neither source names nor SHA-256 values. Neither file path belongs in a public issue or log.

`python -m unittest discover -s tests -v` exercises local intake and evidence-anchor checks against source mutation, traversal, invented evidence, and restricted-source disclosure. `python validate_kb.py` checks repository links, intake IDs, typed public source claims and Roots claim strength. `python tools/verify_claim_anchors.py --source-root <local OneDrive Naijin-Ryu folder> --private-manifest <private intake-manifest-private.json>` validates the source register's exact Word anchors against independently rehashed source bytes. The private manifest and source paths stay local.

## Evidence classes

`SOURCE` is a document assertion; `EDITORIAL` is a normalization/synthesis; `EXTERNAL` is an independently retrieved authority or study; `INFERENCE` is an interpretation; `UNKNOWN` remains unknown; `VERIFIED` requires appropriate observation.

## Known incomplete qualifications

- Visual/layout review and exact text differences for the Aeon Key Workbook PDF/Word pair; four larger pairs have very high extracted-text overlap, not byte identity.
- Original-source bibliographies and attribution quality.
- Practitioner outcomes, instructor competence and contact-training safeguards.
- Government filings, permits and actual operational state of proposed activities.
- Consent and copyright review for any distribution of source binaries.
- The glossary's **Eclipse of Dawn** reference versus the surviving **Clear Intent** title.

## Release gate

Successful link validation and source-hash matching support repository consistency, **not** independent safety or clinical approval. Do not present this repository as a qualified instructional school or launch authorization based on documentation alone.

## Verified intake and review data

On 2026-10-21, **all 30 files** were admitted into private Ingest CAS with 30/30 valid deep-verified records; **whole-store audit is not clean** because it reports 51 unreferenced stage receipts from failed initial cloud reads. Those audit artifacts remain untouched. Root-of-meaning interpretation was tested through a **partial** Roots receipt whose two limited claim-strength checks passed. Neither result establishes document authorship, metaphysical truths, legal filing or safe martial practice.
