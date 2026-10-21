# Corpus coverage — 30 original files

**Scope:** the author's `OneDrive/Documents/Naijin-Ryu` collection, observed 2026-10-21. Source IDs bind to the [redacted public intake register](../data/intake-register-v1.json). Originals and full Ingest receipts remain in private storage, not GitHub.

**Three different claims:** `RAW-ADMITTED` means exact source bytes were retained in Ingest and the records passed the deep record audit; `STRUCTURE/TEXT-EXAMINED` means documentary headings/text or PDF pages were read, not that scientific assertions are true; `PUBLIC-DERIVATIVE` means a restricted-purpose educational index exists, **not** that the original file can be distributed.

**Coverage:** 30 raw-admitted files (15 DOCX, 11 PDF, four images). All 15 DOCX files had XML paragraph/heading structures extracted privately. All 11 PDFs had readable text extracted and page counts recorded. All four image files had binary format/dimensions inspected, **not a complete semantic or rights review**. Two of the Word files contain personal archetype material and remain unpublished.

| Source ID | Public identifier | Structural observation | Public treatment / primary index |
| --- | --- | --- | --- |
| NRY-001 | `Camps Overview.docx` | DOCX; paragraphs/headings extracted | [Camp proposal; program planning and regulatory issues indexed](organization/program-concepts.md) |
| NRY-002 | `Camps Overview.pdf` | PDF; 6 pages | [Camp proposal; program planning and regulatory issues indexed](organization/program-concepts.md) |
| NRY-003 | Withheld source | DOCX; paragraphs/headings extracted | [Restricted last-resort force source; no operational techniques published](REVIEW.md) |
| NRY-004 | Withheld source | PDF; 14 pages | [Restricted last-resort force source; no operational techniques published](REVIEW.md) |
| NRY-005 | Withheld source | Graphic; format/dimensions only | [Private site/property design; location and layouts withheld](organization/program-concepts.md) |
| NRY-006 | `Glossary.pdf` | PDF; 24 pages | [Terminology index; ambiguities remain noted](glossary.md) |
| NRY-007 | `Naijin-Ryū Manual .docx` | DOCX; paragraphs/headings extracted | [Thirteen-part martial manual chapter map](martial/manual-guide.md) |
| NRY-008 | `Naijin-Ryū Manual .pdf` | PDF; 29 pages | [Thirteen-part martial manual chapter map](martial/manual-guide.md) |
| NRY-009 | `Naijin-Ryū Phase1 Mental Conditioning.docx` | DOCX; paragraphs/headings extracted | [Phase 1 mental practice, Day 1–5 headings](practice/mental-conditioning.md) |
| NRY-010 | `Naijin-Ryū Solo-Intensive Training Program (Phases 1–4) – Daily Syllabus and Itinerary-1.pdf` | PDF; 26 pages | [Founder-intensive four-phase schedule; not a generalized prescription](curriculum.md) |
| NRY-011 | `Naijin‑Ryū Dojo Extension Build Plan.pdf` | PDF; 4 pages | [Private site/property design; location and layouts withheld](organization/program-concepts.md) |
| NRY-012 | `Phase 1 Fundamentals.pdf` | PDF; 15 pages | [Six-week introductory version preserved as alternate pacing](curriculum.md) |
| NRY-013 | `Phases of SURGE Training Manual.docx` | DOCX; paragraphs/headings extracted | [Student and Guardian phase schedule; four-day through six-day weekly variants](curriculum.md) |
| NRY-014 | `Phases of SURGE Training Manual.pdf` | PDF; 15 pages | [Student and Guardian phase schedule; four-day through six-day weekly variants](curriculum.md) |
| NRY-015 | Withheld source | PDF; 3 pages | [Private site/property design; location and layouts withheld](organization/program-concepts.md) |
| NRY-016 | `Stances for Naijin-Ryū.pdf` | PDF; 15 pages | [Stance visual source reviewed; public discussion excludes unverified claims](surge.md) |
| NRY-017 | `A Guide To True Ascension — Plain‑language Edition (v1).docx` | DOCX; paragraphs/headings extracted | [Plain-language and full spiritual guide, Six Aeons and Seven Divisions](true-ascension.md) |
| NRY-018 | `A Guide to True Ascension.docx` | DOCX; paragraphs/headings extracted | [Plain-language and full spiritual guide, Six Aeons and Seven Divisions](true-ascension.md) |
| NRY-019 | Withheld source | DOCX; paragraphs/headings extracted | [Restricted personal archetype source; no private reflection disclosed](spiritual/practices.md) |
| NRY-020 | Withheld source | DOCX; paragraphs/headings extracted | [Restricted personal archetype source; no private reflection disclosed](spiritual/practices.md) |
| NRY-021 | `Book of Signs.docx` | DOCX; paragraphs/headings extracted | [Seven Signs and twelve-method religious reflection index](spiritual/texts-and-study.md) |
| NRY-022 | `Confrontation Scripts Appendix.docx` | DOCX; paragraphs/headings extracted | [25 interpersonal scripts indexed; not clinical diagnosis](spiritual/texts-and-study.md) |
| NRY-023 | `Naijin-Ryu, Church of Ascension – Foundational Document Package.docx` | DOCX; paragraphs/headings extracted | [Whole-system foundation and historical Indiana filing draft](church.md) |
| NRY-024 | Withheld source | Graphic; format/dimensions only | [Restricted graphic original; dimensions/format only](spiritual/practices.md) |
| NRY-025 | Withheld source | Graphic; format/dimensions only | [Restricted graphic original; dimensions/format only](spiritual/practices.md) |
| NRY-026 | Withheld source | Graphic; format/dimensions only | [Restricted graphic original; dimensions/format only](spiritual/practices.md) |
| NRY-027 | `The Aeon Key Workbook.docx` | DOCX; paragraphs/headings extracted | [Aeon Key workbook: PDF text reformatting and differences under review](spiritual/texts-and-study.md) |
| NRY-028 | `The Aeon Key Workbook.pdf` | PDF; 7 pages | [Aeon Key workbook: PDF text reformatting and differences under review](spiritual/texts-and-study.md) |
| NRY-029 | `The Aeon Key.docx` | DOCX; paragraphs/headings extracted | [Five-module short Aeon Key source](spiritual/texts-and-study.md) |
| NRY-030 | `The Complete Guide for Shadow Walkers-A Roadmap to Divinity Copy.docx` | DOCX; paragraphs/headings extracted | [Six-part Shadow Walkers roadmap](spiritual/texts-and-study.md) |

## Source-to-claim coverage

The [typed claim register](../data/source-claim-register-v1.json) currently indexes **25 nonrestricted claims** across the martial manuals, training material, Church founding package and True Ascension primary texts, with **50 source-text anchors**. Each claim identifies a nonrestricted source ID, source heading or section, public derivative and limitation. The [private Word anchor verifier](../tools/verify_claim_anchors.py) checks the anchors after source byte rehash, without publishing raw documents. Text occurrence is not an independent truth test.

## Edition relationships

- Main martial manual, SURGE training manual, Camps Overview and Clear Intent: Word/PDF text closely matches after normalization; byte identities remain distinct.
- Aeon Key Workbook: PDF text shows page-header repetition, quote normalization and formatting differences. Treat as a separate edition until paragraph-level verification.
- Other PDF-only sources remain distinct; an approximate training calendar does not silently replace any source variant.

## Review controls

1. Maintain the stable source IDs even when filenames, ordering or OneDrive synchronization change.
2. Keep redacted private IDs free of original filenames, private path components, personal names and source hashes in the public index.
3. Never copy restricted originals or their operationally dangerous or autobiographical contents into public docs as a by-product of a text extraction.
4. Compare revision timestamps only as file metadata; they do not prove conceptual origin, author intent or derivative ancestry.
5. Identify editorial interpretations separately, especially the normalized training calendar and Church document's whole-system/historical-filing dual role.
6. Use [local private source verification](../tools/verify_private_intake.py) with the private manifest to recheck hashes after future source changes.

See [source edition comparisons](source-editions.md), [Roots method](lineage-method.md), [publication boundaries](REVIEW.md), and [full system overview](FOUNDATION.md).
