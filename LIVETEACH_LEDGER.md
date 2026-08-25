# LIVETEACH_LEDGER — the Live-Teach Projector Kit build, phase by phase

One readback block per merged phase (order LT-GO). Convention: a phase's merge
SHA lands in the block at the **next** phase's append, because a ledger cannot
carry the SHA of the merge that ships it. Decisions D1–D5 are quoted from the
order and marked as applied where a phase leans on them.

---

## Phase 0 — Recon & decisions (governing spec: MASTER_PROMPT_Live_Teach_Projector_Kit.md)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR #150 → merge `26dd45d`.
- **Delivered:** `LIVETEACH_RECON.md` — estate survey (HUD, theme, splash/exit,
  reduced-motion, CI), 15-family roster census, placement at
  `/Lessons/liveteach/`, Q1–Q3 recorded.
- **Gates:** all 5 PR checks green; post-merge fieldops + Pages deploy +
  watch-main all green. Negative controls seen live: the stale-evidence
  sweep's self-test, the pr-census emptied-baseline red-proof, and the
  fixture-name sweep's seeded-detection control (run locally).
- **Deferred at the time:** Q1 unknown (dissolved by LT-GO D1); roster ruling
  (settled by LT-GO D2: session-only, in memory, nowhere else); the recon §8
  name exposures (executed as LT1, below).

## LT1 — Pupil-name remediation (safeguarding; LT-GO D3)

- **Branch/PR/merge:** `claude/new-session-43lyml` → PR (this one) → merge SHA
  recorded at next append.
- **Delivered:** 23 public files' hard-coded class rosters neutralised
  (`Pupil A…` style; WorldCup squads → England player surnames), one scenario
  and one placeholder sentence de-named, `MASTER_PROMPT_Live_Teach_Projector_Kit.md`
  landed in-repo (the governing spec, verbatim from the session upload),
  REGISTER.md brought up to the code (R-LT101: LT1 record + the `mbm_cc_v1`
  ×175 census R-B01 predates), and `LIVETEACH_LT1_CONTACT_SHEET.md` for Matt's
  post-hoc veto.
- **Gates, with negative controls named:**
  - Name-absence: a local census over 23 real name tokens (names never
    committed) detected 71 files before the edits (positive control), and
    after them exactly the judged-and-left set in the contact sheet;
    **negative control** — a seeded file carrying one census name was
    detected, then removed and the tree re-verified clean.
  - `tools/verify_fixture_names.mjs` clean; **negative control** — its
    `--self-test` seeds a person-shaped fixture and must go red, and did.
  - Diff shape: 29 insertions / 29 deletions across 23 files — array lengths,
    grades and quoting preserved.
- **Corrections to the recon recorded:** the ASDAN `Consent_*` family is
  adjudicated **fictional** (provenance in the files, REGISTER R-D03 family,
  `_passpq/CLAIMS.md`) — recon §8 was wrong to list it; the `6 Art` list reads
  as synthetic (A→L initials) and was replaced belt-and-braces.
- **Deferred (contact sheet C1–C3):** the frozen
  `biology/Structure_of_the_Thorax.html:1372` fallback list (the one real-name
  file left; frozen path + no-self-merged-safeguarding rule); two site-repo
  demo strings; git history retention.
- **Decisions applied:** D3 (names first, contact-sheet + post-hoc veto),
  D4 (self-merge on green), D5 (container limits recorded, not blocking).
