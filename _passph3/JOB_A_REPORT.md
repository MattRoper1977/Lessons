# PH-3 JOB A REPORT — ASDAN accuracy finish at BASE `ae1d3c7…`

Mode: **FACTS MODE** (no `_asdan_private/`). Gate set G1–G9 run after every step — all PASS at
every commit (see `GATES.md`). Additive-by-default held: strip the authorized insertions and
reverse the authorized replacements and every touched file is **byte-identical to BASE**
(verified programmatically per commit).

## A1 — ComSk1 minima staff blocks (APPLIED)
- `LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html` and `…PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html`
  (the only two pages on main stating a ComSk1 minimum — census C2).
- One block per surface, twice per file: screen `id="peq-comsk1-minima"` inside the Title
  slide's staff-labelled **Teacher Print Tools** box; print `id="peq-comsk1-minima-print"` at
  the tail of `#print-witness` (which every `printPack()` level includes), after — and not
  touching — the protected §4/§5 declaration blocks. All §4.1 numbers kept: 3 ways / 4
  components / 3 difficulties / 4 planned questions / one activity (3 min OR 8 min discussion
  OR 250 words) / group ≥3 / 2 positives / 2 developments / no 10-hour rule on Communication.
- No pupil-slide text changed by A1. Idempotent (2nd run no-op).

## A2 — Pupil-facing claim corrections (APPLIED — 8 edits)
Full register with old→new and justification: `_passph3/PUPIL_TEXT_REGISTER.md`.
W4: two→four prepared questions (slide + print mirror); "ComSk1 asks for…" print Key Fact
completed with the discussion route. W5: "Meet the two-way minimum" heading + paragraph
reframed as the lesson's own target; "ComSk1 minimum:" print line completed; the Key-Facts
line under it reframed; the KO "MINIMUM" cell completed. Everything else (success-measure
examples, task text, match pills, WAGOLLs, answer keys, script pools) deliberately left —
listed in the register.

## A3 — Staff accreditation panels (APPLIED — 17 pages, `id="peq-facts-panel"`)
- **L1 panel (8):** LAUNCH hub (+ Hospitality-VT sentence), LAUNCH PEQ START_HERE, LAUNCH
  Resources_and_Tools, LAUNCH Scheme_of_Work *(trimmed: "IQA before EQA" already on the page)*,
  GROW hub *(trimmed: attribution routing already on the page — panel ends "Nothing is promised
  to a learner")*, GROW Scheme_and_Resources, **GROW PEQ START_HERE** and **GROW
  Resources_and_Tools** *(the last two beyond §4.3's "expect" list — both measurably carry
  qualification-route framing; census evidence in CENSUS.md)*.
- **BUILD short-course variant (8):** BUILD hub *(trimmed: the "What this banks, stated
  honestly" note already covers what BUILD banks — panel keeps only the no-PEQ-unit line, RPL,
  e-portfolio date, attribution)*, the 5 BUILD START_HEREs, `build_dt_upcycling.html`,
  `Build/Slideshows/BUILD_DT_W6_Handover.html` (screen-only, inside the Teacher Print Tools
  box; zero panels inside any print section).
- **LAUNCH Vocational START_HERE (1):** staff panel carrying the Hospitality-VT withdrawal
  clock (register/buy by 31 Dec 2026; certify by 31 Aug 2027; Gardening unaffected) +
  attribution line.
- Each id exactly once per file, zero elsewhere (G4). Panels are additive; no existing text
  replaced. Measured observation, not acted on: the LAUNCH Careers / Community_Enterprise /
  Living_Independently START_HEREs carry one "banks the ASDAN short course + AQA UAS" line
  each — bank labelling, not qualification-route framing; left without panels.

## A4 — C7 sentence (HELD — no `P8: GO` in this session)
`GROW_ASDAN/Scheme_and_Resources.html` line 21 stands unchanged (verbatim, G1-pinned). The
proposed replacement is recorded in `_close/OPEN_ITEMS.md` item 47. The food-safety paragraph
and the before-teaching checklist on that page are byte-untouched.

## A5 — Seven staff sign-off one-liners (APPLIED — 7/7)
Recovered read-only via `git show ab7730c:<path>` (branch never checked out), each verified:
exactly one line differs; staff-side "Witness" evidence step; no doubled token/placeholder/
deletion; replaces a "staff sign off <thing>" claim with "staff prepare <thing> for assessor
sign-off". My re-applied strings were byte-checked against the quarantine tip before applying
(7/7 match). Files: CAREERS_W6, COMM_W6, DUKE_W6, FW_W5, FW_W6, LI_W6, BUILD_DT_W6_Handover.
All other ≈93 sign-off occurrences: REPORT-ONLY, classified with proposals in
`_passph3/SIGNOFF_CENSUS.md`.

## A6 — Paperwork refresh (docs)
- `_passpq/SPEC_FACTS.md`: dated §19 "2026-08 booklet addendum" **appended** (no existing line
  rewritten): L1-easier verbs; worked assessment plan (mixed-level, co-assessment, pre-delivery
  IQA field); PEQ002 = challenge, overlapping windows; e-portfolio 31 Aug 2026; VT/RoadWise
  withdrawal dates; Hospitality = VT / Gardening = Short Course; L3 16+; only-one-adjacent-unit
  arithmetic; §6.5 typo (CrThSk2/CrThSk3); partial certification; registration DONE 30 Jul.
  Each fact cites its source type; nothing quoted longer than a clause.
- `_passpq/COMPLIANCE_CHECKLIST.md`: item 1 status → **DONE — Matt, 30 Jul 2026** (single-cell
  edit) + appended addendum with the two dated actions (e-portfolio export before 31 Aug 2026;
  Hospitality VT register by 31 Dec 2026 / certify by 31 Aug 2027); first-year-EQA item stays.
- `_passpq/QUESTIONS_FOR_CHERYL.md`: appended Q13–Q17 (BUILD WellbLeE3-column contradiction;
  VT clock; e-portfolio export; GROW L2 stretch-vs-registration; ComSk1 four-questions rollout)
  + a note that Q5 is answered.
- `_passpq/CREDIT_PATHWAYS.md` + `PEQ_PRIMER.md`: every number verified against §2.3 — **no
  wrong numbers found**; appended the partial-certification and only-one-adjacent-unit lines
  (both were absent).
- `Planning/LAUNCH/LAUNCH_Autumn_Year_Plan_ASDAN.xlsx` — **read-only scan (openpyxl, values
  only; file NOT edited).** Findings:
  - **FALSE claim, repeated:** the "PEQ Evidence Map" sheet asserts a 10-hour rule **on
    ComSk1** — `A10` "Use over ≥10 hours", `B10` "Plan used over a minimum of 10 hours",
    `A13` "THE 10-HOUR RULE IS THE DESIGN CONSTRAINT", `A14` "ComSk1 requires the plan to be
    USED over a minimum of 10 hours…", plus `B7`/`B21` (Key Dates) "10-hour clock/tally" and
    `E9` "PLAN LIVE — 10-hr clock starts". Spec v1.2: the 10-hour plan-use gate sits on every
    skill EXCEPT Communication. **Proposed cell fixes:** delete rows built on the 10-hour
    premise for ComSk1 (Evidence Map A10/B10/E10, A13–A14; Key Dates B7's "10-hour clock
    starts" clause, B21) or reword to the real ComSk1 gates ("plan used across weeks; activity
    minimum 3 min talk OR 8 min discussion OR 250 words; four planned audience questions").
  - `E9` also understates the ComSk1 minimum (omits the ≥8-min discussion route and the four
    planned questions) — same completion as A2 proposed.
  - The workbook's own banner ("provisional — not yet verified against the official ASDAN
    specification") supports treating it as stale rather than authoritative.
- BOOKLET MODE mapping for GROW W3/W5: **UNDETERMINED** (`_passph3/BOOKLET_MAPPING.md`).

## Gated / not done
- A4 held (above). No filename renamed. No workflow files. No script block touched (G8 proves
  byte-identical script blocks on all Job A files). Quarantined branch used read-only, twice,
  via `git show` only.
