# Whole-system source traceability — where documentation is still thin

**Evidence snapshot:** 2026-10-22, the `main`-derived registry on the whole-system review branch (based on pending PR #4). The private [30-file intake index](../data/intake-register-v1.json), [source claim register](../data/source-claim-register-v1.json), and [corpus coverage record](CORPUS_COVERAGE.md) describe **different forms of coverage**.

This is a **quality diagnosis, not a finding that files were unread, irrelevant, or publicly distributable**. All 30 originals were reportedly hash-verified in the private Ingest store and structurally/textually sampled in earlier passes. Fewer are represented by exact, typed, public source claims.

## Current recorded claims, by source (main-derived data)

| Source ID(s) | Original theme or edition | Anchored claims in main-derived register | Interpretive limitation |
| --- | --- | ---: | --- |
| **NRY-007** | Main martial manual (Word) | **6** | Partial extraction of values/curriculum is not full chapter validation |
| **NRY-013** | SURGE student/Guardian manual (Word) | **3** | More Phase 2–4 claims exist in pending martial PR #5; not merged at snapshot |
| **NRY-009** | Phase 1 mental conditioning | **1** | Psychology and neural mechanisms need independent evidence, not just text occurrence |
| **NRY-001** | Camps Overview (Word) | **1** | Historical estimates and law claims require separate official review |
| **NRY-023** | Whole-system Church package | **2** | Eight sections cover doctrine, governance, clergy, draft legal texts, archetypes and practices; two claims cannot represent all those decisions |
| **NRY-017 / NRY-018** | Plain-language / full True Ascension guides | **2 / 2** | The six Aeons are indexed, but detailed edition/term claims remain sparse |
| **NRY-021** | Book of Signs | **4** | Source assertions about transformative methods are not verified outcomes |
| **NRY-029 / NRY-027** | Aeon Key / Word workbook | **1 / 1** | Workbook PDF is a separate artifact; text/layout equivalence unfinished |
| **NRY-022 / NRY-030** | Confrontation scripts / Shadow Walkers guide | **1 / 1** | Rhetorical guidance and spiritual narrative are not proof of another person's motives |

**Total:** 25 claims, 50 declared text anchors across **12** distinct source IDs. Original source hashes do not automatically add a source claim.

## Nine additional review-required sources without individual anchored claims

| Source ID | Public description | What to verify next, without publishing original private bytes |
| --- | --- | --- |
| **NRY-002** | Camps Overview PDF | Edition alignment with Word and program/regulatory assertions; distinguish unrelated horror text |
| **NRY-006** | Glossary PDF | Meaning and referent of terms; ambiguous title references; no invented canonical definitions |
| **NRY-008** | Martial manual PDF | Page-level differences and graphics compared with Word; avoid duplicate claims solely from parallel format |
| **NRY-010** | Solo-intensive syllabus PDF | Separate individualized training and pacing, not a universal class protocol |
| **NRY-011** | General dojo extension PDF | Actual permitted text review, without releasing identifying property details; previous direct read failed |
| **NRY-012** | Six-week Phase 1 Fundamentals PDF | Exact deviations from eight-week working calendar, including former individualized constraints |
| **NRY-014** | SURGE training manual PDF | Confirm text/diagram comparison against Word `NRY-013`; avoid treating a high overlap score as exact identity |
| **NRY-016** | Stances PDF | Source-defined terminology versus anatomical or medical inference; protect against risky copy-pasted technique |
| **NRY-028** | Aeon Key Workbook PDF | Ordered paragraph and **visual** comparison with Word `NRY-027` (pending PR #6 has a preliminary extracted-text check) |

All nine are labeled **review-required** in the public intake. That designation is **not** public-release permission, nor a claim that every PDF is safe to repost. Several contain images or personal/site-context details.

## Cross-domain next steps

1. **Church:** before producing an organization plan, independently anchor the eight source sections `NRY-023` against each high-level statement, especially §§3–6 where historical *filing and role proposals* must not be promoted into authority; restrict sensitive personal examples from §7.
2. **True Ascension:** check term/symbol inventories across `NRY-017/018/021/027/029/030`, mark actual wording differences rather than claim an author's conceptual derivation chronology.
3. **Martial:** retain the current 25-claim baseline until PR #5 is integrated; its additional claims are training-focused, not full-system coverage.
4. **Youth camp:** verify actual state program definitions and applicability from officials; an anchored camp assertion about law is still only a source statement.
5. **Facilities:** resolve safe private access to `NRY-011` before making claims of cost, floor area, design or site suitability. Redacted summaries should be kept free of physical identifying information.
6. **Restricted nine originals:** keep their existence/provenance entries; **do not create public content-anchored claims** that expose intimate reflective texts, dangerous last-resort technical procedures or private property assets merely to improve an artificial count.

## Interpreting any future progress metric

These thresholds are **not interchangeable**:

- **Raw intake:** original file bytes receipted and hash-checked.
- **Structural/text reading:** contents were parsed or viewed, possibly partially.
- **Document interpretation:** analyst describes source theme with a locator.
- **Public source claim:** an exact source assertion has a typed entry and anchor(s), subject to private rehash.
- **Independent verification:** external or real-world evidence tests an empirical, safety, historical, legal or operational proposition.

More claim entries are desirable only if they **increase substantive traceability**; they are not a proxy for doctrinal completeness, clinical efficacy, or current organizational reality.

[Reader's whole-system guide](START_HERE.md) · [System relationships](SYSTEM_COHERENCE.md) · [Source edition comparisons](source-editions.md) · [Improvement register](WHOLE_SYSTEM_BACKLOG.md).
