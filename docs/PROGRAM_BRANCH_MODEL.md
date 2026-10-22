# Naijin-Ryū program branches and ownership

Naijin-Ryū has one integrated **`main`** repository and multiple named **program workstreams**. Each `program/*` branch is a persistent Git work lane for a program's proposed changes, **not** an independent copy of doctrine or a separate private repository. Every branch begins as an identical snapshot of `main`; the program directory specifies its editorial focus.

## Current workstreams

| Work lane | Work branch | Scope | 
| --- | --- | --- |
| [Martial arts and SURGE](../programs/martial-training/README.md) | `program/martial-training` | Martial instruction, SURGE pillars, Sashes of Dawn, training calendars, assessments and non-operational safety review |
| [True Ascension studies and practices](../programs/true-ascension/README.md) | `program/true-ascension` | Six Aeons, Archons, Aeon Key, Book of Signs, reflection and spiritual study |
| [Church and community foundation](../programs/church-community/README.md) | `program/church-community` | Author's integrative whole-system Church foundation, voluntary participation, historical Indiana formation language, governance concepts |
| [Naijin-Ryū youth summer camp](../programs/youth-camp/README.md) | `program/youth-camp` | Proposed youth overnight camp, educational schedule, supervision and applicable health and safety review |
| [Immersive horror program](../programs/horror-immersion/README.md) | `program/horror-immersion` | Proposed fall/winter immersive narrative experience, participant consent, adult/age boundaries, opt-outs and safeguarding |
| [Dojo and facilities development](../programs/dojo-facilities/README.md) | `program/dojo-facilities` | Dojo facility and extension concept, functional requirements, non-identifying accessibility and approval research |

The Church foundational package is the **umbrella description of the collective whole**, not an authority over the other branches merely because there is a `church-community` work lane. Martial and spiritual participation remain distinguishable and voluntary. Youth and immersive-horror camp concepts use the same historical proposal document but are **two different programs**, requiring separate safety, eligibility and consent reviews.

## Working rules

1. **One integrated source of truth.** `main` carries accepted public documentation and editorial agreements. Protected authored values remain under [editorial authority](EDITORIAL_AUTHORITY.md).
2. **One intended work lane per program.** Use the branch from [the JSON registry](../data/program-workstreams.json) for changes primarily owned by that program. Work can include new material in `programs/<id>/` and compatible updates elsewhere.
3. **No branch implies operation.** An active Git branch proves only that a named Git ref exists. It is not a school, registered church, permit, operating camp, building project, staffed team, deployed system or published source corpus.
4. **Review before integration.** Open a PR from the program branch (or a short-lived branch cut from it) into `main`; run `python validate_kb.py`, `python -m unittest discover -s tests -q`, source checks where accessible, public-content privacy review, and relevant subject review.
5. **Keep lanes fresh.** After a merge, refresh each *clean* program branch from the newest `main` with a fast-forward. If its head has unmerged work, inspect the divergence and reconcile through review; **never force-reset, force-push or silently discard contributions**.
6. **One subject, one writer.** Before parallel editing of a shared file or source, inspect open PRs and declared ownership. Coordinate overlapping changes explicitly rather than letting independent branches overwrite one another.
7. **Never put restricted originals on a public branch.** All `program/*` branches are public. Property plans, sensitive archetype reflections, health or student records, and actionable highly injurious techniques stay in private source custody. A separate private system is required for private operational work.
8. **Separate independent facts.** Religious authorship, organizational filings, observed permits, instruction outcomes and external research have distinct evidence status. Cross-branch references do not raise their epistemic strength.

> **HOSTILE REVIEWER:** Long-lived program branches each contain the full repository and will diverge, duplicate work, and make `main` harder to maintain. Would directories and short-lived feature branches be simpler?

**Partially accepted.** Folders and short-lived feature PRs are simpler technically. These long-lived named branches are maintained as **coordination lanes**, with only one integrated `main`. Work can use short-lived feature branches when a long-lived lane already holds unmerged work. If stale branches begin creating duplicated doctrine or repeated merge conflicts, retire or consolidate the lanes **without deleting unmerged work**.

## Program initiation is not deployment

The current statuses in the workstream registry say `SOURCE-BASED DEVELOPMENT`, `HISTORICAL-DRAFT-AND-FOUNDATION`, or `CONCEPT-ONLY`. They do not imply regulatory approval, instructor certification, safe implementation, teaching consent or current operation. Evidence and launch gates stay explicit in [review](REVIEW.md) and [external research](research-evidence.md).
