# HANDOFF — current state (overwritten after every closed item or STOP)

**Read this first.** It is overwritten, not appended: `git log -- _sx3/HANDOFF_CURRENT.md` holds
every earlier version. The sequence ledger beside it (`_sx3/sequence_2026-09-22/S0x_*.md`) holds
the evidence for each closed item.

Written 2026-09-23 by session `01Grmg9b` (https://claude.ai/code/session_01Grmg9bdXpQhYEj2CAZ8dFg),
under the OVERNIGHT AUTONOMY order of 2026-09-23/24. Last event: **the S3 tool landed** (overnight item 3). Lessons #660 merged as `d8acf3ac`; Apps #175 as
`b694ffad`. Its publication, run 35814262000, succeeded. One live-origin 503 on the teaching-pack check was re-run once, as pre-granted, and passed (35815033808, attempts 1 and 2); main is green. Evidence: `_sx3/sequence_2026-09-22/S05_S3.md`. Items 1 and 2 are in S03 and
S04.

## 1. The three mains

Each read with `git ls-remote` before this docs PR, 2026-09-23 ~03:50Z.

| repo | main | what it is |
|---|---|---|
| Lessons | `d8acf3ac72b2f425a0c845609fa439466c147d1d` | #660, the S3 tool. This docs PR's own squash merge follows it. |
| Site (`mattroper1977.github.io`) | `dd9831f3530336b4623fb666d6a0834725cea0ce` | #434, the EQUAL window. |
| Apps (`Matt-s-Apps-`) | `b694ffad1e4cec0be7d3157af64962659ae93796` | #175, the gate-copy companion for #660. |

Gate copies are byte-identical on both mains at `cb53e71cd323`. Lessons carrier: `uses:` and
`builder_ref` = Site `dd9831f3`. Site pins: Lessons `b1c70b0e` and Apps `7a69b63d`, both
EQUAL-declared.

## 2. Open PRs and branches (every repo uses `claude/lessons-handoff-execution-34mw9j`)

**Open:** Site #435 (batch 1's window). The working branch in each repo:

| repo | branch head | state |
|---|---|---|
| Lessons | this docs PR's head | merges on green, served intersection 0 |
| Site | `2622f3ae` | **Site #435 OPEN**: batch 1's window (16 transition pairs). It waits on its CI, then merges; the Apps companion and the Lessons batch PR follow. |
| Apps | `74b563b9` | the head of #175, merged. Nothing unmerged. |
| Games, Games- | no branch | untouched |

Open PRs that predate this session, untouched and not in the sequence:
- Lessons: #609 (PACK-1R P1), #596 (SX3 PASS 7 close), #560, #497, #465, #456; #118 is
  parked (ruled), #116 is a reference diff, #45 and #43 are HELD.
- Site: #382, #381, #380, #371, #370, #368, #366, #363, #362, #361, #358 (immutable carriers and
  drafts); #291 is HELD.
- Apps: #4.

**Session-local drafts.** They live in this session's scratchpad
(`/tmp/claude-0/-home-user/73e01f17-23b4-5ea3-aeac-a6644cdd53ef/scratchpad/wt/`) and are **not
durable**. If the container was reclaimed they are gone, and each must be rebuilt from the
ruling it implements (section 3).

| draft | head (base) | what it holds |
|---|---|---|
| `wt/b1` | `f69400b3` (on main `d8acf3ac`) | **PASS C batch 1, in progress** (route C). It holds the split and transplant of the 11, all derivation writers and the `REVIEWED_PATHS` admission. See §3 Q3 for the state and the remaining steps. |
| `wt/d3` | `c01e22f8` (on `f99d651d`) | D3: verify_loop row 48, "unbounded modelling" plus "I do 2 before I do", reported RED. |
| `wt/w9l1` | `279d3930` (on `c01e22f8`) | W9L1: the declared eyebrow channel wins over the heading route. Stacked on D3. |
| `wt/site-sw` | `f877b68` (on Site `acb7bfa`) | `serve-witness.yml:31` declared floating by design, scanner constant 1→2. |

**The S3 review** has landed with #660: three rounds, recorded in S05.

The read-only batch-1 dry run (`wf_20c1bcae-fe1`, finished) stacked the limbs and S3 drafts on
`b1c70b0e` and ran the whole batch-1 pipeline. Its findings feed the batch-1 PR and are not a
ruling. Its results are in the scratchpad (`passc_dry_result.json`, not durable). They are to be
re-measured on the real branch before they count:
- **Stacking.** Limbs then S3 conflict only inside `admit_transaction.self_test()`, where both
  append checks. Keeping both blocks resolves it, and `--self-test` then gives PASS (71 checks).
- **Split.** The ruled split of W9 Classic, W12 Classic and W13L2 takes each from 8 to 9 stages.
  Digests `64a0e2c1`, `3359a88f` and `5b32a37c` equal S02's.
- **Transplant.** 11 of 11 decks, 64 panels (GROW 5 each, LAUNCH 6 each), 0 FAIL rows against
  the split bytes. Row 45 equals the derived value on 11 of 11. Proving limb: token on 5, explicit
  cell on 6.
- **Re-stamp.** 11 re-stamped, 0 refused. `lesson-order.json` moves exactly 11 `sourceSha256`
  leaves and no week line.
- **Census and hub.** All 11 flip to CONFORMING (14 → 25). On the hub, 11 badges flip and no card
  moves.
- **S3.** Three Launch `SHA256SUMS.txt` manifests are re-cut, with stale rows riding along. The
  four Classics have no manifest row. The batch needs 4 `REVIEWED_PATHS` admissions: the 3
  manifests and `tools/catalogue/SCIENCE_CHASSIS_CENSUS.json`.
- **The one blocker, and the route taken.** `admit_transaction --strand Science` refuses a branch
  that also rebuilds `Science_Teesside/index.html`: the hub has no week row, and `derive()` sweeps
  every Science `.html` in the diff.
  - Route C needs no ruling. The batch PR carries the 11 decks, census, spine, evidence, order,
    sizes, manifests and pins, with its own Site window (16 transition pairs, measured).
  - A #655-shape hub follow-on PR then moves `Science_Teesside/index.html`, the bindings and the
    hub's size row, with its own window (3 pairs).
  - Between the two merges the hub under-claims NOT YET on 11 conforming decks.
  - The alternative, the tool skipping the hub path, is a pinned-tool change not ruled, so it was
    not taken.
- **Style, a question for Matt.** L39 records Matt accepting the 31 re-deriving full-lundy →
  earlier "(no Lundy furniture in their bytes; PASS C restores it)".
  - The re-stamp never writes style, so batch 1 leaves the 7 non-Classic decks recorded
    'earlier'.
  - Measured on the dry run: a `build_catalogue.py` run moves only the 11 batch entries. It flips
    the 7 styles to full-lundy and moves `terms-and-styles.json`, `science-shelf.json` and the hub
    style badges (served).
  - When PASS C restores style (in each batch, in the hub follow-on, or once at the end) is not
    ruled. It is not a pre-signature column, so it holds nothing.

## 3. Ruled but not done, in the ruled order

The current order is the overnight order, merged with the earlier rulings without contradicting any
of them:

1. limbs PR
2. S3 tool
3. PASS C batch 1 (11)
4. D3 (row 48), then the W9L1 declared-channel fix (both before batch 2)
5. batch 2 onward
6. item 4 re-cut
7. LW-1 after Autumn 2 batch 1

Item 4 follows the overnight order ("5. Item 4" after "4. … batch 2 → as far as the zero-exception
rule allows"). That supersedes S02's "run item 4 immediately after PASS C batch 1". The deviation is
recorded here, not decided.

**Overnight order (Matt, 2026-09-23/24), verbatim:**
> "RUN in order, standard landing route each time: 1. #434 → merge → pure carrier pair →
> publication by run id. 2. Limbs PR (all four rulings built, W9L1 out of HELD, fence re-pinned,
> three records pinned, Apps companion) → merge. 3. S3 tool (SHA256SUMS as transaction member) →
> merge. 4. PASS C Autumn 2 batch 1 (≤12) → batch 2 → as far as the zero-exception rule allows.
> 5. Item 4: HUM-T P1 re-cut (the 24 decks with a Title panel). Held stays held. GPT-work items
> (new science content; cybersecurity) are listed, never written."

Items 1, 2 and 3 are **done** (S03, S04, S05).

### Q1 · Limbs PR — DONE (#658 `e6f7fcc6`, S04)
> "RULING — batch 2 limbs: ADD BOTH, the Humanities Q1 shape. 1. Science ROW limb in
> build_lesson_order.derive(): a deck is proved when its SCIENCE_WEEK_BINDINGS row exists, the
> record's digest equals its pin, and the row's term·week equals the evidence record's own
> projection. Red proofs: row absent → refuse; pin mismatch → refuse; row week ≠ projection →
> refuse; W9L1 → proved; W14L1 → unchanged (control). 2. Science LABEL limb: the deck's "Autumn 2
> · Week n" label parsed by the estate's existing term_codes/weeks_from readers (the form they
> already accept) and required to equal the row. Red proofs: wrong week in label → refuse; label
> present, row absent → refuse; the 5 GROW *A decks → proved. 3. Both limbs pinned (REVIEWED_PATHS,
> gate copies, Apps companion after); own PR ahead of batch 2; measure all 31 after it: expect 30
> proved (SCI_B_W12 stays on its R-GAPS exception). Anything else refusing → HELD by name with the
> limb that refuses."

> "RULINGS — limbs PR second cut. Push it as built … 1. Identity-only rows (14 of the 19):
> accepted within the ruling, but VISIBLE — the S2 table's limb column reads "row
> (identity-only)" for those decks so Matt signs knowing it … 2. FENCE.json: the three decks the
> new limbs now prove LEAVE the fence … Red proof: remove one from the fence, alter its bytes, the
> row limb still holds its week; the three still-fenced decks unchanged. FENCE.json re-pinned.
> 3. B_W4A–W7A: correct _sci/WEEK_TOKEN_DISAGREEMENTS.md … Fix in the reader: only the title
> stage's term·week token and meta line count as the deck's claim; recall/review text is ignored.
> Red proof: a title stage claiming the wrong week still refuses; the four then re-measured and, if
> proved, join a batch. 4. Counts corrected: 30 proved + SCI_B_W12 held (R-GAPS). The re-stamp list
> excludes held decks BY DERIVATION from _sci/HELD.md and the R-GAPS record, never by hand; W9L1
> leaves HELD in the same PR as the row limb."

> "RULING — W16B … if (b), W16B stays refused. Either way the visible label is wrong for pupils
> and teachers: record it for the transplant — the token is derived from the row (Spr1·W2) when
> PASS C re-cuts it, never typed. Everything else accepted as built. Cut the limbs PR from
> post-fold main once #434, the carrier and the publication close."

Measured: W16B is (b). It was landable through the cover rule; the title-claim refusal now refuses
it.

> Re-stamp counter bug (2026-09-23): "correction numbered; the fix rides the limbs PR with its
> planted-failure proof." Label limb: "keep it — it is the proof for decks without a row; its
> self-test is the evidence it works."

### Q2 · S3 tool — DONE (#660 `d8acf3ac`, S05)
> "S3 EXTEND admit_transaction's Science part to accept SHA256SUMS.txt as a transaction member
> (derived digest of the re-cut manifest, pinned), red-proved: a manifest not in the transaction
> → refused; a manifest whose rows disagree with member bytes → refused. No one-off declarer."

### Q3 · PASS C Autumn 2 batch 1 (11 decks) — IN PROGRESS, next

**Measured so far on `wt/b1`**, on main `d8acf3ac`, with the committed tools and the reconciled
dry-run runbook:
- **Split** of W9 Classic, W12 Classic and W13L2: 8 → 9 stages, digests `64a0e2c1`, `3359a88f`,
  `5b32a37c`.
- **Transplant of the 11:**
  - 64 panels (GROW 5 each, LAUNCH 6 each), and row 45 equals the derived value on 11 of 11;
  - 0 verify FAIL rows against the split bytes;
  - against the pre-split originals, the 3 split decks each fail only row 13: the glued meta line
    the ruled split separates, with 0 words missing.
- **390 px render with axe:** 64 of 64 panels reached and disclosed, rows 38–40 all 64 of 64, 0
  serious axe violations, 0 page errors.
- **Shell-by-DOM:** PASS on 11 of 11, with JS off and on. Stripping the declared nodes returns each
  body exactly, apart from 4 whitespace characters at the injection points.
- **Limb:** token on 5, explicit cell on 6; the row and label limbs are not reached.
- **Re-stamp:** 11 re-stamped, 0 held. `lesson-order.json` moves exactly 11 `sourceSha256` leaves.
- **Spine:** 4 re-censused.
- **Census:** exactly the 11 entries move (14 → 25 conforming).
- **Sizes:** the 4 Classic rows move.
- **Manifests:** 3 Launch manifests re-cut (all rows verify).
- **Admission:** 4 records admitted.

**Remaining, in order:**
1. Cherry-pick onto the working branch after this docs PR merges.
2. Pin and run PIN1.
3. Declare the GLV3 transaction (`admit_transaction --strand Science`), then re-pin.
4. Run the battery.
5. Take the served moving set from built bytes: 16 pairs are expected.
6. Site window (`[main-today, pending]`).
7. Apps companion.
8. Lessons batch PR, with the carrier bumped last.
9. Publication.
10. Site EQUAL window, carrying the hub follow-on's 3 pending pairs.
11. Apps companion.
12. The hub follow-on PR (`build_science_hub.py`, sizes, pins), which carries the carrier.
13. Publication, EQUAL window, pure carrier.

> "W9L1 is EXCLUDED from batch 1 (the one-exception hold helps no one). Batch 1 = 11 decks, zero
> exceptions, pre-signed."

> "S1 PASS C IS AN IN-PLACE TRANSPLANT. The 31 are published; changing them is an edit at the same
> route, TERM+WEEK UNCHANGED, evidence re-stamped, a declared replacement transaction per batch."

The 11 decks:
- SCI_G_W9 Classic and SCI_G_W12 Classic
- SCI_L_W9 Classic and SCI_L_W12 Classic
- SCI_L_W13L2
- SCI_L_W14L1–3
- SCI_L_A2_W7L1–3

Pre-signature (overnight order): "any STOP-SIGN table is SIGNED IN ADVANCE when every row reads
TERM+WEEK UNCHANGED = YES, evidence sha == bytes, row 45 == derived expectation, shell-by-DOM
PASS, exceptions EMPTY. "Row (identity-only)" in the limb column is not an exception. Any table
with an exception HOLDS; batches behind it build and stage but do not merge."

### Q4 · D3, then W9L1 (before batch 2)
> "1. Order: D3 (row 48) lands BEFORE the W9L1 declared-channel fix; the widened row 48 (I do 2
> before I do → RED) accepted. The 51 held decks stay held on row 48; the 17 Build Spring/Summer
> decks keeping their Lundy-loop stage is recorded."

> "D3 as a real check: add the "unbounded modelling" result to verify_loop's report (RED on a
> third), so the 51 affected decks are reported, not silently passed. Own small PR."

> "W9L1 stage 6: the DECLARED channel wins — eyebrow "We do 2" → wedo2; the heading route never
> names a science stage when the eyebrow channel is present."

After W9L1, regenerate `PASSC_ROW45_DERIVED.json`.

### Q5 · Batch 2 onward
> "batch 2 (30 − batch 1)". W9L1 joins batch 2 through the row limb.

The four B_W4A–W7A join a batch if proved. They are `v3_40min` copies: Earlier versions, and not
in the 31.

### Q6 · Item 4: the HUM-T P1 re-cut
> "The 24 Humanities decks with a panel on the title slide: these are the pre-P1 batches (BUILD
> W1–W8, GROW W1–W8, the OUTSTANDING V4 six, W14/W15). They are item 4's re-cut population (P1-1,
> no Title panel)."

### Q7 · Site `serve-witness.yml:31`
> "declare it floating on purpose with the recording line (the "floating by design" category from
> find_pins) — one-time change, scanner constant 1→2. It witnesses live main; that is its job."

Draft `wt/site-sw`.

### Q8 · LW-1 (after Autumn 2 batch 1)
Inputs are held and not landed (section 6). From the LW-1 inputs order:
- **R2 = Job 2:** a TA-brief line, "EHCP areas this lesson can evidence", with observable
  behaviours by lesson id. Measure row 52.
- **R3 = Job 1:** after the M1 census, the worksheet-dependent Summer 1 lessons get two activities
  at the TEACHER_NOTE stage, via the adapter: inline, keyboard, no external loads, provenance.
  Re-measure rows 38–45, then one table for Matt's signature. Unflagged lessons are untouched.
- Job 3 stays with Matt.

### Later in the autonomy order
- B1 Spring 1 (10), then Spring 2, Summer 1 and the Aut1 v3 sets.
- Next-order items only once everything above is closed.

## 4. Held by name

Held means listed, never forced: no transplant, re-cut or rename until a ruling releases it.

Since #658 the re-stamp derives its held set from `_sci/HELD.md` (every backticked Science deck
path) and the R-GAPS rows of `_sx3/RELEASE_LEDGER.md`. Today that set is SCI_B_W12 and the two
case-study decks.

| set | count | record |
|---|---|---|
| Held A, Held B, parked C, the 5 GROW `_Do` decks (D) | per record | `_sx3/HELD.md` |
| 15 LAUNCH print | 15 | `_sx3/HELD.md`, `_sx3/CHASSIS_CONTRACT.md` |
| week-token disagreements: 1 still held, SCI_G_W16B (refused for its title-stage claim). B_W4A–W7A were a reader defect and may join a batch (ruling 3, landed in #658). | 1 of 5 | `_sci/WEEK_TOKEN_DISAGREEMENTS.md` |
| 2 case-study decks | 2 | `_sci/HELD.md` |
| the 51 unscoped science decks (verify_loop row 48 reds all 51 once D3 lands) | 51 | `_sx3/handoff_2026-09-22/artefacts/SCI_51.md` |
| SCI_B_W12: held on its R-GAPS exception, out of every PASS C batch | 1 | `_sx3/RELEASE_LEDGER.md:1312` |
| SCI_G_W16B: its label is derived from the row (Spr1·W2) when PASS C re-cuts it, never typed | (the row above) | `_sci/WEEK_TOKEN_DISAGREEMENTS.md` |
| SCI_G_A2_W7A, SCI_G_A2_W7B: released from the fence by #658 (ruling 2), still listed in `_sx3/HELD.md` as excluded from the transplant. The held derivation does not read that file (question for Matt, §6). | 2 | `_sx3/HELD.md:197-198` |
| decks or files needing GPT work (standing rule 2) | 0 so far | listed here when found |

## 5. Standing rules added this session

1. **HANDOFF_CURRENT (Matt, 2026-09-23).** "After every closed item or STOP, overwrite
   _sx3/HANDOFF_CURRENT.md on Lessons main (docs-only PR, served intersection 0) with: the three
   mains' SHAs; open PRs/branches with head SHAs and what each waits on; the ruled-but-not-done
   queue with ruling text quoted; held-by-name lists with their record files; standing rules added
   this session; owed items for Matt; the single next command."
   - Measured: this file sits outside every workflow trigger, so a docs-only overwrite never
     reaches the boundary gate.
   - Do not put it in a PR that does trigger the gate: a modified file outside the allowed sets
     reds the boundary.
   - Since #658, `_sci/HELD.md`, `_sx3/RELEASE_LEDGER.md` and `_sci/WEEK_TOKEN_DISAGREEMENTS.md`
     are pinned and are boundary-gate triggers. An edit to any of them is a gated PR with a
     re-pin, never part of a docs-only HANDOFF PR.
2. **GPT work (Matt, 2026-09-23; this final wording replaces the earlier two).** "Work that goes
   to GPT, never Code or Claude: 1. NEW lesson content in science: biology, chemistry and life
   sciences, and anything touching virology, toxicology or molecular design. 2. ANYTHING
   cybersecurity-related: computing / online-safety lessons for pupils, and finding or fixing
   security vulnerabilities in the apps, the website or their workflows. When a task needs
   either, do not write it: HOLD by name with reason "GPT work", list exactly what is needed
   (deck + stage + field + SoW objective, or file + suspected weakness + where found), and
   report the list at the next STOP so Claude can brief GPT. When GPT delivers, intake as
   usual: hash on arrival, checks, table for Matt, standard landing route. Mechanical
   transplant, re-stamp and derivation of EXISTING content continue as before."
3. **Correction #39 (accepted).** Before any merge, read main with `git ls-remote`. Never trust the
   PR's cached base.sha.
4. **Carrier last.** A carrier must point at the Site SHA that admits every mover, derived
   artefacts included. The carrier bump is the last edit on the Lessons branch, made only after the
   window merges. Applied in #655 and #656.
5. **Window re-cut on a moved head.** If the content head moves after its window's pending digests
   were measured, re-measure from built bytes and re-cut the window before it merges. #433 was
   re-cut `35aacf64 → 4d2ec44d`.
6. **Gate-copy sync before pinning.** `pin_catalogue_contract.py --lessons L --apps A` refuses
   ("gate copies differ") until the Apps copy carries the same reviewed logic. Copy the Lessons
   gate file over the Apps one, then pin, then `--check`.
7. **D3 before W9L1 (Matt).** The declared-channel fix, landed alone, turns all 51 held decks green
   after transplant (111 → 162 decks with no FAIL row). Stacked on row 48, the passing set equals
   main's.
8. **Concurrency on content PRs (measured).**
   - On a PR touching `Science_Teesside/**`, `cross-estate-on-content.yml` calls
     `mbm-cross-estate-unification.yml`, and the shared concurrency group cancels the direct run.
   - The gate verdict is the called run's `cross-estate / static-contract`.
   - The cancelled direct checks are expected, not a failure.
9. **Qualify Lessons paths in Site workflow comments (measured on #434).**
   - Site gate s10 (`tools/check_workflow_paths.py`, run by "Gates are proven red, not just
     green") resolves every tools/assets/data path a workflow names, comments included.
   - A Lessons path written unqualified names no Site file, so s10 goes red. Write it as
     `Lessons/data/resource-sizes.json`.
   - Run `python3 tools/check_workflow_paths.py` on the Site branch before pushing any workflow
     edit.
10. **Name every hex literal in a carrier (measured on #656).**
    - The Site lag control's C1 needs a naming word (pin, pinned, expected, frozen, canonical,
      previous, …) within 12 lines before or 3 lines after every hex literal in
      `education-pages.yml`.
    - Write "the publisher pin X -> Y", not a bare "X -> Y".

## 6. Owed to Matt, and known reds

- **NOAA 2025 value.** Still owed. Never source, estimate or insert it (427.35 ppm is
  unverified in 7 LAUNCH files).
- **390 px served proof** of the three Summer 1 pages. Still owed. This environment's egress to
  the live host is refused (`403` on CONNECT). That is recorded as a LIMIT, never as a pass.
- **Known red: Site main `published-completion-verify`.** It has failed on every Site main commit
  since at least 2026-09-21. Latest: run 35799501649 on `dd9831f3`.
  - **Cause (re-measured in that run's log):** it checks the live site against a Lessons checkout
    pinned at `b54c9006` (2026-09-16, `published-completion-verify.yml:25`). The live BUILD
    collection has 17 Build Spring/Summer decks (`W18-W26_2026-27/…`, `W27-W34_2026-27/…`) that
    the pin predates. So `check_completion.cjs:120` asserts "BUILD collection lost or duplicated
    teaching versions".
  - **Ruling applied (Matt, 2026-09-23):** "move it only if it is declared EQUAL; if it is a
    deliberately frozen pin (Previous/Receiver class), leave it and record the red as known with
    its cause in HANDOFF_CURRENT.md".
  - The lag control reads that pin as not declared EQUAL: its comment says "held equal to it" in
    lower case, and the control tests for the word `EQUAL`. So it was left.
  - Releasing it takes a ruling that declares that pin EQUAL.
- **Questions from the limbs item (S04), not decided:**
  1. Should `_sx3/HELD.md` feed the re-stamp's held derivation? SCI_G_A2_W7A and W7B left the
     fence (ruling 2) but are listed there as excluded from the transplant. Neither is in the 31.
  2. CI runs neither `restamp_evidence_sha256.py --self-test` nor `admit_transaction.py
     --self-test`. This predates #658. Adding a step is a CI edit the limits reserve for a ruling.
  3. Identity-only rows (14 of the 19 row-proved decks): "recorded against the evidence-model
     finding" is owed at the S2 table (batch 2).
  4. Style restoration (L39 "PASS C restores it"): when, and by which writer (§2, the dry run).
- **Correction #40** (the re-stamp self-test's counter): recorded in S04, fixed and red-proved in
  #658.
- **Lag control C1 is fixed** (was red on Lessons main before the fold). After #656: "6 hex
  literals in the carrier, all named". The only red left is P0 `serve-witness.yml:31` (Q7).
- **LW-1 inputs** (Matt, 2026-09-23). Held untracked in `_incoming/lw1/` (locally excluded) in the
  session container, not landed:
  - `JOB_1_Learning_Walk_Interactions.zip` sha256
    `123b8f40499ece9bcadcf155d221a1175177ac64e369d8c4e7d91ca26cc3240c`: 63/63 checksums pass; 36
    activities; 0 external URLs or script/link/fetch loads; viewport set on 36/36.
  - `JOB_2_EHCP_Outcome_Area_Map.zip` sha256
    `c0c6f5fc7f9702652de303cb998a095761b23dcaba496ccf8e44aa9b97252865`: 6/6 checksums pass; CSV
    of 36 lesson ids (18 Humanities + 18 `SCI_*`).
  - If the container was reclaimed, Matt re-sends both and these hashes verify the copy.
  - Job 3 (the RE scheme draft) stays with Matt.

## 7. The single next command

**Continue PASS C batch 1 on route C** (Q3). Cherry-pick `wt/b1`'s three commits
(`bc106199..f69400b3`) onto the working branch after this docs PR merges.

If the scratchpad is gone, rebuild the batch on the branch in this order:
1. `tools/sx3/split_arrival_stage.py --write` on the 3 merged decks.
2. `loop_adapter.adapt(bytes, PATHWAY, False)` on the 11, verified with `verify_loop.verify`
   against the split or main bytes.
3. `restamp_evidence_sha256.py --write --decks` with the 11 after-digests.
4. `build_lesson_order.py`.
5. `_sownb/vb/tools/recensus_existing_html.py --write` on W13L2 and W14L1–3.
6. `tools/sci/chassis_census.py --write`.
7. `tools/ux2/resource_sizes.py --write`.
8. `refresh_pack_checksums.py` on the 7 non-Classics.
9. `admit_batch.py` for the 3 manifests and the census.

Then, on the branch:
1. `pin_catalogue_contract.py --lessons . --apps <Apps>`, then `derive_triggers.py --write`.
2. Commit. Run `admit_transaction.py --name 'PASS C Autumn 2 batch 1' --strand Science --base
   origin/main` (without `--check`), then commit.
3. Re-pin.
4. Run the battery.
5. Build Site `dd9831f3` + head + Apps `b694ffad` to take the moving set.
6. Cut the Site window, land the Apps companion, then open the Lessons PR with the carrier bumped
   last.

The PR body carries the STOP-SIGN table: 11 rows with TERM+WEEK UNCHANGED, evidence sha == bytes,
row 45 == derived, shell-by-DOM PASS, exceptions EMPTY and the limb column. On zero exceptions it
reads "(pre-signed, zero exceptions)".
