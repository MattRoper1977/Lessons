# CORRECTION #41 — the EQUAL set is five lines in three Site workflow files (2026-09-25)

Supersedes the pin counts in Standing Record 1 (`_sx3/handoff_2026-09-22/artefacts/L51_draft.md`,
"the four EQUAL pin lines") and Correction #34 (`_sx3/SX3_PASSES_LEDGER.md`, "the declared-EQUAL
Lessons pin and its declared-EQUAL Apps companion, in both files — four lines"). Neither is rewritten;
this entry is the dated correction to both.

**Why it changed.** Site #446 (`cc28d5c5`, RULING RS1-G3b R1) moved the Lessons pin in
`published-completion-verify.yml` from `b54c9006` to `7aed39b3` and declared it EQUAL in its own
comment block. Recorded here on Claude's note on RS1-G4 §1 (2026-09-25).

**The EQUAL set, measured on Site main `d9cdceef`:**

| # | file | line | pin | form |
|---|---|---|---|---|
| 1 | `.github/workflows/domain-split-verify.yml` | 154 | Lessons `7aed39b3` | bare |
| 2 | `.github/workflows/domain-split-verify.yml` | 215 | Apps `045088e8` | bare |
| 3 | `.github/workflows/education-publication.yml` | 137 | Lessons `7aed39b3` | `${{ … \|\| '<sha>' }}` wrapper, fallback only |
| 4 | `.github/workflows/education-publication.yml` | 200 | Apps `045088e8` | `${{ … \|\| '<sha>' }}` wrapper, fallback only |
| 5 | `.github/workflows/published-completion-verify.yml` | 32 | Lessons `7aed39b3` | bare |

**RESTATED RULE.** Every EQUAL window discharges **all five**: the declared-EQUAL Lessons pin in
`domain-split-verify.yml`, `education-publication.yml` and `published-completion-verify.yml`, and its
Apps companion (L31) in `domain-split-verify.yml` and `education-publication.yml`.
`published-completion-verify.yml` has no Apps checkout, so it has no Apps line. The selector is still
the EQUAL declaration in each pin's own contiguous comment block, never a count and never the file.
The frozen pins (`.sources/Previous-Lessons`, `.sources/Receiver-Lessons`) never move. Correction
#34's two hard constraints stand: exactly one checkout per repository in `education-publication.yml`,
and its lines 3–4 keep the wrapper with only the quoted fallback substituted. Line 5 is bare, like
lines 1–2.

**What the lag control covers.** `tools/lessons_pin_lag_control.py` controls Lessons checkouts only.
Run on Site `d9cdceef` against Lessons `645aa4bb`: 13 Lessons pins, of which **3 declared EQUAL**
(lines 1, 3 and 5 above) — P4 "EQUAL holds" on all three and P5 "EQUAL-declared pins agree:
7aed39b3e2e6". The two Apps lines (2 and 4) are outside its population, so P5 counts three of the
five, not five. The tool was not changed (the note's instruction). Line 5 is inside P5 now, so a
future window that misses it reds P4/P5 — but only when the control is run: it is wired into no
workflow, and the job it pins runs only after a Site "Education publication".

**Where this could not go.** `_sx3/SX3_PASSES_LEDGER.md` is digest-pinned in both gate copies
(`tools/verify_cross_estate_unification.py` `CATALOGUE_PINS`, and `REVIEWED_PATHS` in
`tools/catalogue/pin_catalogue_contract.py`). A gate is never re-pinned to land a docs note, so this
correction lives here and in the amendment under Standing Record 1. The ledger takes it in the next
PR that legitimately touches it.
