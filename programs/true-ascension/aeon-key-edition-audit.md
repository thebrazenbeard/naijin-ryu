# Aeon Key Workbook — bounded Word/PDF text comparison

**Source IDs:** `NRY-027` (Word workbook) and `NRY-028` (seven-page PDF workbook). **Date reviewed:** 2026-10-21. Both were read as authorized private source files; this page contains **only comparative findings**, not the full source text.

## Method actually used

Extracted the Word document's visible `w:t` text spans from its text-bearing outline and the PDF's seven pages of extractable text. Split each at the **five named module headings**, excluded PDF's repeated running page headers and blank underline writing spaces, folded case/quotation differences and compared the module-level normalized word vocabulary. This tests **text overlap**, not semantic identity or correct PDF page rendering. It is not an XML layout audit and does not compare vector graphics or font placement.

| Original module | Word text tokens* | PDF text tokens* | Portion of Word tokens whose vocabulary occurs in PDF |
| --- | ---: | ---: | ---: |
| 1. Clear the Static | 83 | 83 | 100% |
| 2. Come Back to Yourself | 86 | 86 | 100% |
| 3. Anchor Your Memory | 59 | 50 | 92% |
| 4. Release the Guilt | 62 | 61 | 98% |
| 5. Step Outside the Noise | 120 | 119 | 100% |

*Counts apply only to the normalized module extraction used for this comparison, not to physical page word counts or unique words. The fifth module's extraction includes the final reminder paragraph. Coverage reports **presence of vocabulary**, not ordered phrase or paragraph identity; equal percentages do not prove exact editions.

## Observed differences and limits

- All five module titles appear in both extracted forms **in the same order**.
- The PDF repeats the workbook subtitle as a running header across its pages. The Word outline contains extra writing-space and label scaffolding, particularly around the **Anchor Your Memory** notes and a **Forgiveness Notes** label.
- In this comparison, no module exposed an obvious new vocabulary term in the PDF absent from its Word counterpart after normalization. That is **not** proof there are no word-order, punctuation, omitted-paragraph, typographic or semantic differences.
- The previous whole-file six-word-sequence Jaccard of **74%** and smaller-text overlap of **88%** were affected by different extraction/layout formats. This new targeted module test reduces the uncertainty about missing *module themes*, **not** uncertainty about complete paragraph-by-paragraph equality.

**Disposition:** The Word and PDF share all five module headings and high vocabulary overlap, with some omitted/extracted note labels. Preserve both as separate receipted source editions. A **true ordered paragraph alignment and visual page check** remain required before asserting identical text or publishing a print-ready edition.

[Five-module companion](aeon-key-study-companion.md) · [Source relationship map](source-relationship-map.md) · [existing global edition review](../../docs/source-editions.md) · [source custody and provenance](../../docs/provenance.md)
