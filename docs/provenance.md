# Provenance and transformation rules

This repository distinguishes **original source documents** from **editorial knowledge pages**. GitHub docs are neither the originals nor proof that every proposition appearing in an original source is correct.

## Identified collections

- **OneDrive parent:** `Documents/Naijin-Ryu`, containing 16 files and one subfolder.
- **OneDrive True Ascension:** nine files plus `Archetype Integration` (two private Word documents) and `The Aeon Key images` (three image files).
- **Total items cataloged:** 30 files, across the parent and nested directories.
- **Local uploaded study copies:** nine distinct files; a tenth attachment repeated the Church foundational package.

## Hash validation

Five DOCX files uploaded into this conversation were verified byte-for-byte against OneDrive's SHA-256 file metadata:

| Source | SHA-256 prefix | Result |
|---|---|---|
| Core Naijin-Ryū martial manual | `de246912fd43` | Match |
| SURGE training manual | `b5352a6b2afb` | Match |
| Phase 1 mental conditioning | `5145492e7f01` | Match |
| Clear Intent last-resort manual | `c9851490cd74` | Match |
| Church foundational document package | `e9a301e56a0f` | Match |

PDF uploads were read directly, but corresponding OneDrive PDF objects did not expose SHA-256 in the same metadata results. **Do not claim PDF byte identity without a later comparison**. The same applies to the OneDrive Word files not uploaded into the local session.

## Stable source identifiers

The machine-readable `data/source-manifest.json` records the nine directly inspected uploaded files by source ID and full SHA-256. These hashes are evidence of bytes in the local study session, **not** a signature proving authorship, accuracy, originality, or external approval. Private OneDrive drive/item identifiers and sharing URLs are deliberately excluded.

## Editorial transformation types

- **TRANSCRIPTION:** exact source text; none of the current public GitHub summaries claims to be a full transcription.
- **SUMMARY:** faithful description with a named source and preferably a section/page reference.
- **NORMALIZATION:** an explicitly authorized working convention; the eight-week Phase 1 is one example.
- **FACT CHECK:** source assertion compared against appropriately sourced external evidence.
- **EXCLUSION:** original details withheld for personal privacy, legal uncertainty, or unnecessary operational harm.

The source files are not modified by editorial decisions. Corrections to derivative pages do not rewrite their provenance.

## Separate evidence obligations

A document can establish that a proposed church name exists **in a document**. It cannot establish actual incorporation; a training schedule cannot establish a qualified instructor; a scenario narrative cannot establish a technique's real-world performance; and a private personal reflection cannot be treated as publication consent.

See [sources](sources.md), [normalization policy](curriculum.md), [research](research-evidence.md) and [review register](REVIEW.md).

## Ingest all-source acquisition (2026-10-21)

**Executed source:** [Ingest](https://github.com/thebrazenbeard/ingest) `main` commit `e55af474323f2115c5181b443760b8427090562f` on Lappy, working from the signed-in user's synced `OneDrive/Documents/Naijin-Ryu` tree. The Ingest content-addressed store and its full private manifest remain **outside the public repository**.

- **30 original files:** 15 Word files, 11 PDFs and four images; exact raw bytes acquired by filename-bound FileSource.
- **30 accepted records:** 30 valid graphs and 0 corrupt graphs in `audit-records`.
- **Whole-store audit:** 30 blobs, 30 records, no unreferenced blobs; **51 unreferenced stage receipts** remain after initial cloud-placeholder failures. No cleanup was performed. Because the whole-store status is **ISSUES**, it must **not** be represented as a clean audit pass.
- **Independent OneDrive metadata cross-check:** all **18** files for which OneDrive exposed a SHA-256 hash matched their private Ingest raw SHA-256 exactly (**18/18**). The remaining 12 objects did not expose SHA-256 metadata in the retrieved listing; this is **unknown**, not a mismatch.
- **DOCX structure:** 15 of 15 extracted with paragraph/heading counts into a local private outline.
- **PDFs:** all 11 text-extracted for section/page review; see [edition comparison](source-editions.md).
- **Images:** four raw files acquired and format/dimensions read, but full visual meaning not exhaustively reviewed.

The [public 30-source intake index](../data/intake-register-v1.json) includes source IDs and non-private hashes; names and hashes for restricted sources are withheld. It is a derivative overview, not the private Ingest receipt graph itself.

## Source-to-claim evidence anchoring (2026-10-21)

The [public claim register](../data/source-claim-register-v1.json) contains source-bound editorial paraphrases, stable source IDs, section locators, phrase anchors and explicit limitations. The [private verifier](../tools/verify_claim_anchors.py) rehashes each referenced DOCX against the private intake manifest, then checks each source phrase in document XML. This demonstrates an actual **document-level text occurrence**, **not** an independently verified section boundary, historical priority, doctrinal truth, scientific effect, or legal filing. Section locators are editorial citations and must be reviewed separately when accuracy is disputed. Its separate public-mode verification checks that claim references point only to unrestricted catalog entries and existing public pages.

## Source-to-claim evidence anchoring (2026-10-21)

The [public claim register](../data/source-claim-register-v1.json) contains source-bound editorial paraphrases, stable source IDs, section locators, phrase anchors and explicit limitations. The [private verifier](../tools/verify_claim_anchors.py) rehashes each referenced DOCX against the private intake manifest, then checks each source phrase in document XML. This demonstrates an actual **document-level text occurrence**, **not** an independently verified section boundary, historical priority, doctrinal truth, scientific effect, or legal filing. Section locators are editorial citations and must be reviewed separately when accuracy is disputed. Its public-mode verification checks that claim references point only to nonrestricted catalog entries and existing public pages.

## Roots typed provenance (2026-10-21)

The [Roots](https://github.com/thebrazenbeard/roots) model and claim-strength checker at `24ed94d69ec07c5bba638de9ed2b8ecfad3cc7ce` were executed against a **partial** two-event receipt documenting the Church foundational package and the author's later clarification. Both partial claim-strength checks passed. **Origin remains unresolved**; a 2025 file modification date is not evidence of a concept's first appearance. The sanitized [public Roots receipt](../data/foundation-roots-receipt.json) records the distinction between whole-system interpretation and historical Indiana filing intent.
