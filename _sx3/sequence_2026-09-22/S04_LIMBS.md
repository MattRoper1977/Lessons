# S04 — The Science row and label limbs, and the second-cut rulings (closed 2026-09-23)

Sequence ledger, entry 4. Written by session `01Grmg9b`. It closes overnight item 2: "Limbs PR (all
four rulings built, W9L1 out of HELD, fence re-pinned, three records pinned, Apps companion) →
merge."

## The rulings built

The texts are quoted verbatim in `_sx3/HANDOFF_CURRENT.md` §3 Q1:
- "RULING — batch 2 limbs: ADD BOTH" (2026-09-23, 22:14)
- "RULINGS" items 2–3 (22:33): the counter correction and the label limb
- "RULINGS — limbs PR second cut" (23:17)
- "RULING — W16B" (23:25)

| PR | head tested | merge SHA | checks (run ids) |
|---|---|---|---|
| Apps companion | Matt-s-Apps- #174 `d07d640d` | `d9b9966f70c5` | 5 success, 4 skipped: 35809626132, 35809626136, 35809626172 |
| Lessons limbs | Lessons #658 `44f0c680` | `e6f7fcc6da3e` | 15 success, 2 skipped: 35809933252, 35809933353, 35809933406 |

- The merged tree `ac34ca6c` equals the tested head's.
- Gate copies are byte-identical in both estates at `5b8c91491b46`.
- Publication: run **35810675683** on Lessons main `e6f7fcc6`, with build `107021314332` and deploy `107023106834`, both success. Main `e6f7fcc6` ran 10 of 10 runs green: UX2 gates 35810675257, FieldOps P2 35810675253, cross-estate unification 35810675251 (including its live-proof job), Science teaching pack downloads 35811287676, and Watch main 35811023641, 35811287892, 35811328475, 35811437831 and 35811609628.

## Measured

- **All 31, byte-moved** (the three merged decks split first, then all 31 transplanted), through
  the estate's own `derive()` and `restamp_plan`:
  - 31 refreshed, 0 unresolved.
  - First proving limb: token 6, explicit cell 6, row 19, label 0.
  - **30 re-stamped; SCI_B_W12 held** by derivation (R-GAPS).
  - This is the ruled "30 proved + SCI_B_W12 held (R-GAPS)".
  - SCI_L_W9L1 is proved by the row limb at Aut2·W1 and has left HELD.
- **Admission over the 180 bound decks** (`admit_transaction.science_allowed`):
  - main `f8cc300a`: 172 landable, 8 refused;
  - after: 175 landable, 5 refused;
  - exactly B_W4A–W7A move to landable, and exactly SCI_G_W16B to refused.
- **The fence:** 3 released (SCI_G_A2_W7A, SCI_G_A2_W7B, SCI_B_W13 Classic), each held by the row
  limb at its week; 3 still fenced (SCI_B_W8A, W8B, W11A).
- **Held by derivation:** SCI_B_W12 (R-GAPS) and the two case-study decks.
- **Served bytes** (Site `dd9831f3` + the limbs head + Apps `7a69b63d`, built): 0 changed in all
  three estates, and `lesson-order.json` is unchanged. So no Site window and no carrier move.

## Adversarial review, and what it changed

- **The first review** (three lenses and a critic, of `0c10ebb0`) confirmed:
  - a **blocker:** the counter fix had no number and no committed planted-failure proof;
  - **two majors:**
    - the `derive()` wiring had no red proof;
    - held decks aborted `--write` instead of being excluded;
  - **several minors.**
- **The fix round** (`f347cdbc`, re-pinned `cfba4c53`) answered each finding; see the PR body.
- **A confirmatory verifier** found them all CLOSED or DEFERRED-RECORDED. It raised two minors of
  its own, answered in `03087e19` (re-pinned `44f0c680`).

## Correction #40 — the re-stamp self-test printed PASS whatever had failed

`tools/catalogue/restamp_evidence_sha256.py`'s self-test counted failures in `ok`. The Q1 block's
`ok, why = strand_proof(...)` rebound it to a bool, erasing every failure counted before it.

- **Found by:** the adversarial trace of the W9L1 re-stamp refusal.
- **Ruled:** 2026-09-23, "correction numbered; the fix rides the limbs PR with its planted-failure
  proof".
- **Fixed:**
  - the counter is `bad`;
  - `RESTAMP_SELFTEST_PLANT` plants a false check before every rebinding;
  - the last check runs the self-test in a child with it set and requires `self-test FAIL (1)` and
    exit 1.
- **Proved:** with the counter put back to `ok`, only that control goes red.

## Owed to Matt from this item (questions, not decided)

1. **`_sx3/HELD.md` and the held derivation.** SCI_G_A2_W7A and W7B left the fence (ruling 2), but
   `_sx3/HELD.md` lists them as excluded from the transplant, and the held derivation (ruling 4)
   reads only `_sci/HELD.md` and the R-GAPS rows. Neither is in the 31, so nothing lands. Should
   `_sx3/HELD.md` feed the derivation?
2. **CI does not run `restamp_evidence_sha256.py --self-test` or `admit_transaction.py
   --self-test`.** This predates this item. The red proofs are guarded by byte pins and run by
   hand. Adding a CI step is a CI edit the standing limits reserve for a ruling.
3. **Identity-only rows** (14 of the 19 row-proved decks). "Recorded against the evidence-model
   finding" is owed at the S2 pre-signature table (batch 2).
