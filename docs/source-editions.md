# Word and PDF source-edition comparison

**Date:** 2026-10-21. This review used the OneDrive original files acquired by [Ingest](lineage-method.md) plus connector-extracted Word text and locally extracted PDF text. The purpose is to distinguish **near-identical text**, **possible variant editions** and **format-only differences**.

## Corpus formats examined

- **15 DOCX**: document XML was read to extract paragraphs and structural headings.
- **11 PDF**: readable text was extracted and page counts identified; image layout and diagrams are not fully characterized by text alone.
- **4 images**: file bytes were ingested and image format/dimensions inspected; visual semantics have not been formally reviewed.

These 30 files are separately receipted in the private Ingest store; the public [redacted intake index](../data/intake-register-v1.json) records source identifiers.

## Parallel formats: normalized text comparison

Five apparent Word↔PDF edition pairs were compared using normalized lowercase word tokens and sets of six-word sequences. The **Jaccard score** is the fraction of all distinct sequences shared; “overlap” is the shared fraction relative to the smaller of the two sequence sets. Differences in case, typography, page breaks, quotation marks and list segmentation can lower a score.

| Pair | Word tokens | PDF tokens | Shared six-word sequence overlap | Jaccard | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Camps Overview | 2,967 | 2,977 | 99% | 98% | Strong textual equivalence |
| Clear Intent | 10,404 | 10,425 | 100% | 100% | Strong textual equivalence |
| Naijin-Ryū Martial Arts Manual | 18,942 | 18,953 | 100% | 100% | Strong textual equivalence |
| Phases of SURGE Training Manual | 9,271 | 9,284 | 99% | 99% | Strong textual equivalence |
| The Aeon Key Workbook | 447 | 504 | 88% | 74% | Formatting/extraction variation or possibly distinct text |

The workbook PDF repeats its running header on each page and reformats quotations and prompts. A later [five-module targeted text extraction comparison](../programs/true-ascension/aeon-key-edition-audit.md) found all five headings and 92–100% module-level normalized Word-token vocabulary coverage by the PDF, with differences concentrated in note scaffolding; this does **not** establish ordered paragraph or layout equality. A substantive revision is **not established**. Preserve both files until a paragraph-level diff or author edition decision.

**These scores do not mean binary equality.** The original PDF and DOCX always have distinct file bytes and need separate source records even when their extracted text is nearly the same.

## Other PDFs without a same-title Word pair in this folder

- **Glossary** (24 pages) — definitions across martial and spiritual vocabulary.
- **Stances for Naijin-Ryū** (15 pages) — includes stance diagrams and explanations.
- **Phase 1 Fundamentals** (15 pages) — six-week version retained as alternate pacing.
- **Solo-Intensive Program** (26 pages) — founder-specific training variant.
- **Dojo Extension Build Plan** (4 pages) — private practical facilities design.
- **Address-specific extension proposal** (3 pages) — private location and site details withheld.

The **Aeon Key Workbook** PDF is seven pages and paired with a Word document as noted above. The apparent duplicated content should not be counted as distinct doctrine without evidence of a change.

## Limits and next checks

Text extraction does not prove identical drawings, footnotes, tables, formatting, embedded media or substantive meaning. Page-count metadata and PDF excerpts can be incomplete when layout is image-backed. Keep original files unchanged and review visually before any print-ready publication. Do not distribute property-specific plans, identifying imagery or dangerous operational details publicly as a side effect of source comparison.

See [source catalog](sources.md), [provenance](provenance.md) and [normalization choices](curriculum.md).
