# HANDOVER — Pass LA (LAUNCH ASDAN suite build)

**Pass-scoped handover.** Kept under `_passla/` with the pass's other deliverables, NOT
written into the root `/HANDOVER.md`. Reason: the root file's own header rule is
"supersede wholesale, carry the queue", and it tracks the *current estate* state — but
this branch **parks UNMERGED and merges LAST** (behind SL → SBX). Rewriting the live
root HANDOVER on a branch that lands last would clobber it with a stale, partial view.
**Action for whoever integrates the merge:** fold the one-line summary below into the
root HANDOVER's queue at merge time.

---

## 1 · Where this got to

- **Branch** `pass-la-launch-asdan`, off BASE `6945c223ab55469df09b9c53c79fd2c584cc06b1`
  (origin/main HEAD at open). **Tip `daf28a6…`** (live-verified via
  `raw.githubusercontent.com` at that SHA). **No PR. Parks UNMERGED.**
- **Merge position:** behind the **29 Aug order — SL → SBX → this.** Matt merges.
- **Delivered:**
  - **Phase 1** (`_passla/`): `SUITE_PROPOSAL.md`, `OVERVIEW_DIFF.md`, `FINDINGS.md`,
    `inputs/` (LAUNCH SoW xlsx + provenance). Approved by Matt at the Phase-1 STOP.
  - **Phase 2:** **30 lessons** = 5 strands × 6-week Autumn-1 modules —
    `LAUNCH_ASDAN/{PEQ, Careers, Living_Independently, Vocational, Community_Enterprise}/`.
    Entry points: `LAUNCH_ASDAN_Hub.html` + 5 `START_HERE.html` + `Scheme_of_Work.html`.
    Overviews (Matt's Option A): standalone `Resources_and_Tools.html` for **GROW** and
    **LAUNCH** (LAUNCH last).
  - **Generator** (`_passla/build/`): regenerable — `gen.py` (chassis carry) + `gen_entry.py`
    + `gen_resources.py` + `content_{peq,careers,living,vocational,community,common}.py` +
    `gates.py` + `boot.js`.

## 2 · Totals (state these; do not regress)

- **ASDAN lessons: BUILD 31 + GROW 18 + LAUNCH 30 = 79.** The old "**49**" is stale —
  **never restore 49** (REGISTER R-I01).
- **Rings** (`git grep -l … -- '*.html'`): GROW/LAUNCH written-line
  `What I said, and what it changed` **68 → 98** (+30, the new lessons; LAUNCH is the
  GROW/LAUNCH ring). BUILD loop-mark `ll-g:loop-mark v1` **= 50, UNCHANGED** (SET-invariant;
  new LAUNCH files carry none). CLOSE-1 invariant (R-CL01) preserved.

## 3 · `UNVERIFIED-AGAINST-SPEC` — reconcile at the PQ resume

The three official ASDAN PDFs were **ABSENT** from `_passpq/inputs/` (only its README
present). Every PEQ credit/unit/level fact in the suite derives from brief §2.2 +
`_passpq/PEQ_PRIMER.md` + the Evidence Binder (Ofqual-URN corroborator). When the PDFs
land (`_passpq/inputs/README.md` RESUME SEQUENCE), reconcile these, individually:

1. **Unit credit values** printed: **ComSk1 = 3 credits** (the only unit code printed;
   84 occurrences, PEQ strand only). Confirm against the spec (Binder gives `ComSk1 T/651/6412`).
2. **`≥10-hour` cross-week use window** for ComSk1 — surfaced in PEQ W4/W5 (plan/use).
   Confirm the exact spec wording.
3. **ComSk1 activity minimum** — presentation ≥3 min OR text ≥250 words; group ≥3.
   Surfaced in W4/W5. Confirm against the unit booklet.
4. **L1 command verbs** (Outline / Describe / Give a range of examples) — used across the
   PEQ strand. Confirm the per-criterion LO verbs.
5. **Certificate reachability** claim (hub/Scheme level): all six L1 units homed across
   the full-year SoW → 15 credits ≥ 14, min 11 at level. Confirm the rules of combination.
6. **Safeguarding-disclosure notice** (DecMk/WellbLe territory) — NOT reached this pass
   (Autumn 1 is ComSk1 only); flag for the Spring/Summer PEQ modules when authored.

## 4 · Successor warnings

- **Never restore 49** ASDAN lessons — the total is now 79 (§2).
- **D&T witness §5 is OPEN_ITEMS #7** (Matt's decision) — **not this pass's**. The 6
  `BUILD_DT` witness files still lack §5; untouched here. Do not "fix" it without Matt.
- **Sentinel baseline is 50 HTML files, not the brief's stated 45** (5 `Science_Teesside`
  decks added by later science passes — see `_passla/FINDINGS.md` §2). Gate future passes
  on SET-invariance of the current set, not on 45 or 49.
- **No-touch, respected here, keep respecting:** science folders, D&T (incl. **Foodwise**
  — never referenced by the Vocational strand), Art_Teesside, `GROW_HUM_W7`/`LAUNCH_HUM_W7`,
  main. GROW was touched **additively only** (new sibling `Resources_and_Tools.html`).
- **L2 is stretch language only** — zero L2 registration claims anywhere (Cheryl's call).
  Keep this on the Spring/Summer PEQ modules.
- **Root `/HANDOVER.md` wholesale supersession** is deferred to the merge integrator (§ top).

## 5 · Open for Matt / next pass (not blockers)

- **Spring + Summer PEQ modules** would complete the other five L1 units
  (TmWk, DecMk, Thinking, Learning, **WellbLe1**) and make the L1 Certificate a *built*
  reality, not just the year target. Same generator; author `content_peq` W7+ per the SoW.
- **The other four strands' Spring/Summer modules** (SoW arcs already mapped in
  `SUITE_PROPOSAL.md` / the weekly-grid dumps) — same pattern.
- **Cross-strand PEQ skill contributions** (SUITE_PROPOSAL Q6): currently the four
  short-course strands bank short course + UAS only, with PEQ contributions surfaced at
  hub level, not per-lesson (deliberate, to avoid GROW's drift). If Matt wants per-lesson
  by-code PEQ skill banks on those strands, that's a small generator change.
