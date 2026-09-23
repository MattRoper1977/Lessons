# S03 — The Science hub orders each week by generation, not style (closed 2026-09-23)

Sequence ledger, entry 3. Written by session `01Grmg9b`. Closes the hub-order item of Matt's
rulings on the S02 STOP. The ruling, verbatim:

> "HUB — WITHIN-WEEK ORDER BY GENERATION, NOT STYLE: current card = the non-Classic deck in the
> NEWEST dated folder for that week (the SX3 31 and the six exemplars today); then Classic in the
> same folder; then v3_40min / Slideshows copies (→ Earlier versions). Style ('Full Lundy Loop' /
> 'earlier') and CONFORMS / NOT YET are BADGES on the card, never ordering keys. Red proof: GROW
> Aut2 W2 headline card must be SCI_G_W9A_Spherical_Bodies_Explore, not the Classic. Ship this as
> its own hub PR ahead of PASS C batch 1 so the links are right even before CONFORMS flips."

## The fold, step by step

| step | PR | head tested | merge SHA | checks (run ids) |
|---|---|---|---|---|
| 1. Site window, 3 served paths as `[main-today, pending]` | Site #433 | `0dfb074d` | `bb2836437e1f` | 7 success + reachability skipped: 35786630823, 35786630845, 35786630859, 35786630874, 35786630893 |
| 2a. Apps gate-copy companion | Apps #172 | `d6c6ae48` | `7a69b63d632a` | 5 success, 4 skipped: 35790008103, 35790008163, 35790008354 |
| 2b. Lessons content + carrier (bumped last) | Lessons #655 | `fa6bb3b2` | `b1c70b0e007d` | 17 success in 35792880039, 35792880040, 35792880049, 35792880796 (gate: `cross-estate / static-contract`); direct 35792880046 cancelled by its own concurrency group |
| 3. Site EQUAL window | Site #434 | `81f445fd` | `dd9831f35303` | 7 success + reachability skipped: 35796141306, 35796141310, 35796141312, 35796141314, 35796141327 |
| 4a. Apps companion for the pure carrier | Apps #173 | `c0c1cf2d` | `1c3238dcc7a5` | 5 success, 4 skipped: 35798877849, 35798877901, 35798877908 |
| 4b. Lessons pure carrier | Lessons #656 | `f495e51d` | `dda76aa48a8b` | 15 success, 2 skipped: 35801363093, 35801363095, 35801363157 |

## The publications and served proof

- **#655's publication.** Run **35793981502**: build `106968840738` success, deploy `106971741319`
  success. Lessons main `b1c70b0e` ran 10/10 success, and Apps main `7a69b63d` 4/4.
- **Served bytes, source-side.** The live host was not measured: egress was refused (`403` on
  CONNECT), so that is a LIMIT, not a pass. What was measured is a full rebuild of exactly what the
  publisher builds, Site `bb283643` + Lessons `b1c70b0e` + Apps `86933c99`:
  - `build_education.py` exits 0 against #433's record.
  - `education-lessons`: 5739 → 5739 files, exactly 3 changed. Each equals its admitted pending
    digest: `Science_Teesside/index.html` `4d2ec44d`,
    `assets/catalogue/science-hub-bindings.json` `a2b3a6de`, `data/resource-sizes.json`
    `ed9878b7`. The tree digest is `39eb2088… → 1e421dd0…`.
  - `education-site` and `education-apps`: 0 changed.
- **On the built served page:**
  - GROW Aut2 W1 = W8A Explore, W8B Do, Classic.
  - W2 = W9A first.
  - GROW Aut2 W4 and BUILD Aut2 W4 both put their Classic last.
  - 35 Earlier cards, all labelled "40-minute copy".
- **Site main `dd9831f3` after #434.** Domain split publication 35798739523, Education
  publication 35798739529, Splash region records 35798739543, MBM audience discovery closeout
  35798739493, Professional site live verification 35799501631, Deployment provenance 35799501650,
  Echo Vault 35799501639, Relicforge 35799501646 and Maker splash 35799501655: all success.
  Published Education completion 35799501649 failed; that is the known red below, and its cause
  was re-measured in its log.
- **The pure carrier's publication.** Run **35802172279** on Lessons main `dda76aa4`: build
  `106994764693` success, deploy `106997285874` success. Lessons main `dda76aa4` also ran:
  - push: UX2 gates 35802171873, FieldOps P2 35802171882 and cross-estate unification
    35802171859, all success;
  - workflow_run: Science teaching pack downloads 35803062308 success; Watch main 35802566181,
    35803062285, 35803101620 and 35803195884 success. Watch main 35803089850 was cancelled with no
    job run: a pending run displaced in the `watch-main` concurrency group (`cancel-in-progress:
    false`), not a failure.
- **Served bytes after the pure carrier, source-side.** The live host was not measured (the egress
  LIMIT again). What was measured is a rebuild of what the publisher builds after #656: Site
  `dd9831f3`, Lessons `f495e51d` and Apps `7a69b63d`, the Apps pin at `dd9831f3`.
  - Lessons `f495e51d` has tree `009a0e90`, identical to main `dda76aa4`'s.
  - `build_education.py` exits 0.
  - Against #655's build: `education-lessons` 5739 → 5739, **0 changed**, tree digest
    `1e421dd0…` unchanged. `education-site` 203 → 203 and `education-apps` 107 → 107, 0 changed.
  - The carrier moves no served bytes, as claimed.

## What was built, and what the adversarial reviews changed

- **The ruling as built:**
  - Current cards = the newest dated folder's non-Classic decks, in lesson order, then that
    folder's Classic.
  - The 35 `v3_40min` copies move to Earlier versions.
  - Style and CONFORMS / NOT YET are badges only.
  - Result: 145 current (14 CONFORMS + 131 NOT YET), 35 Earlier.
- **Matt's named red proof was already true.** GROW Aut2 W2 headlined W9A before the change,
  because the W9 Classic is bound to Aut2 W1. It stays as a control. The live proof is W1:
  Classic first before, W8A first after. Ruled 2026-09-23: W1 is the live proof.
- **The review of the first cut** (`b3ad2773`) found the proofs weaker than claimed. The second cut
  (`31ff6ce7`) fixed each finding:
  - The ordering checks now read the rendered page.
  - New C10 reds an older copy rendered beside a newer generation, by its folder name alone.
  - `--self-test` fails whenever a control is red.
  - C9 also checks lesson order.
  - hub_sections' reorder guard is now a `ValueError`, not an `assert`.
  - Earlier cards read "40-minute copy", not the raw slug.
  - Each fix is mutation-proved. Because the served bytes moved, #433 was re-cut
    (`35aacf64 → 4d2ec44d`).
- **#434 failed once, then passed.** s10 (`check_workflow_paths.py`) refused three unqualified
  Lessons paths in the new pin comments (run 35795337676). They were `Lessons/`-qualified; the
  failure was reproduced before the fix and was green after.
- **Lag control.** The EQUAL-declared pins agree at `b1c70b0e` (P4/P5). C1 was red on Lessons main
  before the fold; after the pure carrier it reads "6 hex literals in the carrier, all named". The
  only red left is P0 `serve-witness.yml:31`, which has its own ruled PR. C1 is measured
  source-side on the carrier bytes that landed in #656.

## Known, not this item's

- **Site main `published-completion-verify`** has been red since at least 2026-09-21. Latest run:
  35799501649 on `dd9831f3`, where its log names the same 17 Build decks.
  - Cause: its Lessons pin `b54c9006` predates 17 Build Spring/Summer decks.
  - Ruled 2026-09-23: move it only if it is declared EQUAL.
  - The lag control reads it as not EQUAL: its comment says "held equal" in lower case, and the
    control tests for the word `EQUAL`. So it was left, and the red is recorded as known.
- **Concurrency on content PRs.** A PR touching `Science_Teesside/**` has its direct cross-estate
  run cancelled by the content contract calling the same workflow. The gate verdict is the called
  run's.

## Corrections carried in this entry

1. **Hub red proof.** The named check (GROW Aut2 W2) already held before the change. Ruled: W1 is
   the live proof and W2 the control.
2. **"31/31 proved" → "30 proved + SCI_B_W12 held (R-GAPS)"** (limbs measurement, ruled
   2026-09-23).
3. **`_sci/WEEK_TOKEN_DISAGREEMENTS.md`.**
   - B_W4A–W7A were a READER defect: a recall line was read as the deck's claim. They were not a
     deck defect.
   - W16B was landable through the cover rule, not refused as the record said.
   - Both are corrected in the limbs PR, per the ruling.
4. **The first adversarial trace's scratch deletion.** This session removed a running workflow's
   scratch trees during a disk clean-up. The workflow rebuilt them and completed; the fault was
   process, not result.
