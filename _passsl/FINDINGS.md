# Pass SL — SoW/LAUNCH Alignment Audit — FINDINGS

**Status: PHASE 1 HELD — blocked on missing source-of-truth input (see §BLOCKER).**

## Lineage
- **Brief:** "PASS SL — MASTER BRIEF: LAUNCH LESSONS vs THE 2026-27 LAUNCH SoW"
- **Repo:** `mattroper1977/lessons` (verified — NOT the site repo)
- **Build base:** `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main tip @ session start)
- **Working branch:** `pass-sl-sow-launch` (off build base; never commits to main)
- **Ledger name:** "Pass SL" — no pre-existing `_passsl` at base, so no self-rename needed.
- All measurements below stamped **measured @ 32ca685**.

## Session setup (Section 0) — done
1. Repo identity CONFIRMED as Lessons. The session's environment default was the **site repo**
   (`mattroper1977.github.io`); it was attached first and rejected per Section 0 step 1, then
   `mattroper1977/lessons` was located via list_repos and attached. (This is the exact trap the
   brief flags: "three prior sessions defaulted to the site repo.")
2. `git fetch` done; base SHA pinned (above). Local HEAD == base.
3. Branch `pass-sl-sow-launch` created off base.
4. SoW workbook **NOT supplied** — see BLOCKER.
5. Coexistence: no other writers observed on `_passsl/` paths at base.

## Quarantine state AS FOUND (Section 4f) — verified @ 32ca685
- **Assessed files present:** `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html`,
  `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` — measure/propose-only, no patch without
  per-file authorisation.
- **Art_Teesside quarantine:** 53 tracked files under `Art_Teesside/` (read/measure only; fixes as
  proposed diffs until Matt lifts quarantine in writing).
- **D&T:** `DT_Community_Upcycling/` = 2 files (Scheme_of_Work, Weekly_Plan); root
  `build_dt_upcycling.html`. Standing no-touch on D&T v5 printPack id lists / Lundy print page —
  to be verified against actual scope, likely outside LAUNCH.
- **Storage keys / `ps_coldcall_roster`:** untouched (no changes this pass).

## BLOCKER — source of truth absent
The brief's Section 0 step 4 states Matt will place **`LAUNCH KS4 - 2026-27.xlsx`** in the working
copy. **It is not present anywhere in the repo** (verified: no file of that name; the only LAUNCH
spreadsheets are `Planning/LAUNCH/Progress_Tees_Valley_Weekly_Plan_Week01..08.xlsx`, which are
weekly *progress* plans, NOT the SoW workbook with the `Pathway Ladder` / `Qualification Map` /
`Theme & Text Map` / `LAUNCH - <Term>` / `LAUNCH Weekly - <Term>` sheets the brief describes).

Consequence: the entire comparison spine is blocked —
- 4b coverage matrix needs the SoW's **18 strands**;
- 4c week-mapping needs the **SoW weekly grid (W1–W7)**;
- 4e/4f classification needs derived SoW `(strand, half_term, week)` records;
- N1–N6 non-negotiables need the Qualification Map codes, tier statements, term themes, vocab lists,
  and F/S assessment rhythm — all of which live only in the workbook.

**Held for Matt to supply `LAUNCH KS4 - 2026-27.xlsx`.** On receipt it will be committed to
`_passsl/inputs/`, extracted to `_passsl/sow_extract/` as `(strand, half_term, week)` JSON, and
Phase 1 comparison will proceed.

## PRELIMINARY LAUNCH population (Section 4a) — SoW-INDEPENDENT sketch only
NOT a final count — final population requires the SoW's strand list + catalogue cross-check +
near-twin exclusion rules. Confidence tiers, measured @ 32ca685:

**Tier A — confident LAUNCH-named teaching files:**
- `Launch/` suite: 2 Art identity lessons (`Art_L1`, `Art_L2` v5) + 8 `LAUNCH_ART_W1..W8` slideshows
  + 8 `LAUNCH_HUM_W1..W8` slideshows = **18 lesson files** (+ index.html, README.txt = non-lesson).
- `Art_Teesside/Launch/`: 8 `LAUNCH_ART_W1..W8` + Printable pack + START_HERE + Scheme_of_Work
  = **8 lessons + 3 support** (QUARANTINED — measure only).
- `Humanities_Teesside/`: `LAUNCH_Printable_Pack.html`, `LAUNCH_Scheme_of_Work.html` = **2 LAUNCH-named**.

**Tier B — candidate LAUNCH provision, pending SoW confirmation of which strands/lessons are in scope:**
- Science suites (GCSE-level per brief 4a): `biology/` (14 files), `chemistry/` (9), `2 Physics 10/` (17).
  These carry OBVIOUS near-twins to resolve before counting, e.g.
  `2 Physics 10/L2_Voltage_Current_Resistance.html` vs `...-1.html`;
  `L2b_Ohms_Law_PhET_Practical-1.html` vs `..._1.html`;
  `chemistry/Lesson4a_Gas_Tests_H2_O2_CO2 (1).html` (space+parens — batch-hazard filename).

**Excluded from LAUNCH population:** `Games/` (games), `primary/`, GROW/BUILD-prefixed suites
(other pathways), `LundyLoop/` machinery. To be restated with rule + per-suite split once SoW defines strands.

## Divergences from brief premises (brief-verification rule)
1. **SoW workbook absent** (blocker above).
2. **No `LAUNCH_`-prefixed files at repo root** — the LAUNCH population is folder-scoped
   (`Launch/`, `Art_Teesside/Launch/`, `Humanities_Teesside/LAUNCH_*`), not root-prefixed as 4a implies.
3. **`resources.json` present in THIS (Lessons) repo** (7082 lines) as well as the site repo. Brief says
   catalogue lives in site repo (read-only). Treating site copy as authoritative; local copy noted, not written.

_measured @ 32ca685e1df619b333f3ee4385aed227aa675cdf_
