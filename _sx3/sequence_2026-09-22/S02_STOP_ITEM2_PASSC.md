# S02 — STOP at item 2: Science PASS C Autumn 2 needs one conflict resolved and one route chosen (2026-09-22)

Sequence ledger, entry 2. Written by session `01Grmg9b`.

This entry is a **STOP**. It does **not** close item 2. No PASS C write was made: no deck,
record, window or carrier was touched. The next session resumes here once Matt has ruled on
**S1** and **S3**.

The STOP fires under the clause *"a ruling genuinely absent for an item IN the sequence"*.

Draft history: the first draft cited twelve blockers. An adversarial "find the ruling" review
refuted eight of them with primary sources, and every refutation below was re-measured in the
main thread before it counted. This text is the corrected version.

## Item 1 tail (the atomic step finished before stopping)

| what | run / sha | result |
|---|---|---|
| Ledger S01, #652 | squash `5c5d3554f2a0fb1be4d34e2a428ad9a698a02663`, parent `5e9604cc` | 8/8 checks SUCCESS, run 35769648008, on PR head `dc2bafa5` (tree-identical) |
| its publication | **35770706869** | build `106891397599` SUCCESS · deploy `106895599491` SUCCESS |
| FieldOps P2 on `5c5d3554` | 35770705777 | SUCCESS |
| post-publication checks | science packs 35772025461 · watch-main 35772025263, 35772069466, 35772255082 | all SUCCESS; main green |
| served bytes, source-side | full local build, Site `acb7bfa9` / Apps `86933c99` | `education-lessons` 5739 → 5739, **0 changed**, digest `39eb2088…` unchanged, 0 `_sx3/` paths |

The live host was not measured. That is a LIMIT: egress was refused with `403` on CONNECT.

## What works, measured on copies

- **Transplant.** #649's code plus the in-memory split gives **31/31 decks through `adapt` and
  `verify`, 208 panels, 0 FAIL rows**. Row 45 equals the derived expectation on 31/31.
- **Split.** The split is **RULED**: `tools/sx3/split_arrival_stage.py:202`, "RULED 2026-09-22
  (STOP-C1, the split refusal amended rather than bypassed)", and `pin_catalogue_contract.py:2485`.
  - `--self-test` passes 29/29.
  - The three merged decks go from 8 to 9 stages, and the timer total stays 40.
  - Output is deterministic: W9 `64a0e2c1…`, W12 `3359a88f…`, W13L2 `5b32a37c…`.

## STOP — what must be ruled

### S1 — What PASS C is: an in-place transplant, or new replacement routes? (a conflict in the primary record)

**For replacements / additions:**
- `_sx3/SX3_PASSES_LEDGER.md:1845-1851`, "ADOPTED 2026-09-23 (3)". This is part of the numbered
  2026-09-23 series; its item (1) is marked RULED. It reads: "**Autumn 2 batch 1 of PASS C is
  additions**", and it gives the ruling-4 tool an ADDITIONS limb.
- `tools/catalogue/build_science_hub.py:12-19` (ORDER SCI-COMPLETE, ruling of 2026-09-22 on
  STOP-F1). A lesson is demoted "only where a conforming replacement EXISTS … another route bound
  to the SAME pathway, term and week … until PASS C **delivers replacements**".

**For in-place:**
- The D1 ruling (handoff :80-82) says the 51 are "re-named when their PASS C batch **transplants**
  them".
- The pre-signature column is "TERM+WEEK UNCHANGED".
- Matt's item-2 terms are all in-place operations: "evidence re-stamp", "four term-week forms",
  "pack SHA256SUMS via transaction".
- The same hub docstring says "the badge flips as PASS C lands".
- Every writer is modification-only (`admit_transaction.judge_member`).
- Measured: **31/31 are served routes held as 2-element transition pairs** at Site `acb7bfa9`.
  Editing them is CHANGED, not ARRIVING.

The two readings produce different PRs, different windows (transition pairs vs ARRIVING entries)
and different hub behaviour (badge flip vs demotion). The ledger names ORDER SCI-COMPLETE, the
order that defines PASS C, but its **text is in no repo and no PR body**; `git grep` finds
references only. **Choosing either reading would be a ruling.**

### S3 — The route by which a Science pack `SHA256SUMS.txt` joins the batch's transaction

- `admit_transaction.py:471`: the Science limb declares `.html` members only. The
  SHA256SUMS/CHANGELOG record limb (`SUMMER1_RECORDS`, `:221`) is scoped to the Humanities Summer 1
  trees.
- The gate reds on 4 of the 5 packs holding the 31. `boundary_errors(…, 'lessons')` gives RED for Grow
  W8-W13, Launch W8-W13, Launch Autumn2_W7 and Launch W14-W15, and green for Build W8-W13, which is
  pinned.
- Precedent exists. The one-off declarer `tools/build_resources/admit_w8a_chassis.py` (D-1, #567)
  placed a Science pack SHA256SUMS inside a GLV3 transaction. So did the GROW_W3, CX2_W4L1 and
  SUGAR_R10 transactions, each admitted via REVIEWED_PATHS.
- **Route needing a ruling:** extend admit_transaction's Science limb (a change to a pinned tool),
  or write a D-1-style one-off declarer per batch.
- **Already answered, not open:**
  - Stale non-batch rows may ride along (the D-1 precedent).
  - The 5 Classics with no row are not enrolled (ruling 2026-09-23 §2 / correction #32: "refresh
    the rows that exist, leave the rest").
- Measured: among the 31, **26 rows are stale, 0 fresh, and 5 have no row**. There are **7** stale
  rows outside the 31: 5 deck rows and 2 `manifest.json` rows.

## Not blockers — covered by a standing route, precedent or pre-ruling

Each of these was refuted as a blocker by the review and re-measured.

| point | how it is covered |
|---|---|
| S2 — evidence re-stamp holds on 12 and refuses 19 (measured on byte-moved copies) | This decides batch composition, not the whole item. The 12 are SCI_B_W12, the SCI_G_W9 and W12 Classics, the SCI_L_W9 and W12 Classics, SCI_L_W13L2, SCI_L_W14L1–3 and SCI_L_A2_W7L1–3. Any batch containing the 19 would show an exception and HOLD under pre-signature. Precedent: HUM-T STOP-T3 Q3, "a deck neither rescues is HELD by name". |
| S4 — the hub records (`SCIENCE_CHASSIS_CENSUS.json`, `science-hub-bindings.json`) red the boundary; the census digests all 180 routes, so even the split stales it | This is the standing REVIEWED_PATHS / CATALOGUE_PINS pin route, a tightening. Precedent: `assets/catalogue/humanities-hub-bindings.json` is pinned (gate :170), and there are L37, D-1 and #649. |
| S5 — pre-signature instruments | `row 45 == derived` is measurable today with `verify_loop.panels` plus S01's JSON. `shell-by-DOM` is defined by `_hum/SERVED_PAGE_SHELL_RULE.md` (Matt, STOP-R2 pt 3), with precedent verdicts in #647 and the Summer 1 CHANGELOGs. Only point 3's declared-change comparison has no committed CLI. |
| S6 — named exceptions: SCI_B_W12 carries R-GAPS (`_sx3/RELEASE_LEDGER.md:1312`), SCI_L_W9L1 carries S01's `complete`/Earwig `{6,8}` | Both are ruled or recorded. The pre-signature rule settles the outcome: these rows hold. Excluding SCI_B_W12 leaves **11** decks that could be pre-signed. |
| S7 — `render_proof.cjs:24-25` hard-codes an axe path | axe-core can be supplied at that path without editing or loosening anything. axe is not a pre-signature column. |
| S8 — `LOOP_CONTRACT.md:172,195` "pending Matt's P1 ok" | The status line is stale. Matt's order says "P1 shape", and L42–L45 are pre-signed "in the RULED P1 shape". |
| S9 — authority to apply the split | RULED; see above. |
| S10 — two PASS C duties (exemplar wiring; token-from-binding) | Neither touches the 31. |
| S11 — the single `baseline_sha` in `check_education_separation.py` | No in-place window has ever moved it (#413, #416–#424, #430). |
| S12 — no Science batch driver | Composition is delegated ("batches ≤12"). The missing driver is a tooling gap, not a ruling gap. |

## Corrections carried in this entry

- **Correction #33's served-path figure: 6040 → 6049.** The registry at Site `acb7bfa9` holds
  203 + 5739 + 107 = 6049 keys, and 6040 appears in no registry revision. The intersection with
  #650 and #652 is 0 under either figure.
- **STOP_C3's "an earlier route decides 0" → 1.** SCI_L_W9L1 stage 6 is named wrongly, so 46 stages
  are declared and 45 resolve. This was recorded in S01.
- **D3 "unbounded modelling" RED is enforced at name level only.**
  - `eyebrow_names` bounds a third bare I do / We do to `unnamed` on **51** decks, exactly the
    held-by-name 51. On 19 of them this surfaces as `stage_name == 'unnamed'`.
  - No row emits "unbounded modelling": 0 verdicts across the 51. Row 2 on the 51 is 25 PASS and 26 FAIL.
  - Impact on the 31: none, because they have 0 unnamed stages.
- **`tools/hum/deck_dom.py:338`** still says "19 Science decks declare NEITHER"; the measured figure
  is 0. It is a stale comment in a pinned file, reported and not edited.
- **This entry's own first draft** said "pack SHA256SUMS via transaction" appears nowhere. It does
  appear, but only as the handoff's quotation of the order (:127), with no definition. The draft
  also mis-attributed ADOPTED (3) to "a session". Both are corrected above.

## Housekeeping

Scratch builds and the git worktrees this session registered in the three clones were removed,
and `git worktree prune` was run. Each clone lists 1 worktree. Disk went from 1.3 GB to 24 GB free.
