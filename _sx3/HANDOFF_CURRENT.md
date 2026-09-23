# HANDOFF — current state (overwritten after every closed item or STOP)

**Read this first.** It is overwritten, not appended: `git log -- _sx3/HANDOFF_CURRENT.md` holds
every earlier version. The sequence ledger beside it (`_sx3/sequence_2026-09-22/S0x_*.md`) holds
the evidence for each closed item.

Written 2026-09-23 by session `01Grmg9b` (https://claude.ai/code/session_01Grmg9bdXpQhYEj2CAZ8dFg),
under the OVERNIGHT AUTONOMY order of 2026-09-23/24. Last event: **the Science hub fold closed**
(overnight item 1). The pure carrier #656 merged as `dda76aa4`. Its publication, run 35802172279,
succeeded. The source-side served proof shows 0 served bytes moved in all three estates. Evidence:
`_sx3/sequence_2026-09-22/S03_HUB_ORDER_FOLD.md`.

## 1. The three mains

Each read with `git ls-remote`, 2026-09-23 ~00:30Z, before this docs PR.

| repo | main | what it is |
|---|---|---|
| Lessons | `dda76aa48a8bf8f48678a6d8e23e325e516ed02a` | #656, the pure carrier that closes the hub fold. This docs PR's own squash merge follows it. |
| Site (`mattroper1977.github.io`) | `dd9831f3530336b4623fb666d6a0834725cea0ce` | #434, the EQUAL window. |
| Apps (`Matt-s-Apps-`) | `1c3238dcc7a5f13604e5d336be43f92e0e13b69a` | #173, the gate-copy companion for #656. |

Gate copies are byte-identical on both mains at `e90427cc9772`. Lessons carrier: `uses:` and
`builder_ref` = Site `dd9831f3`. Site pins: Lessons `b1c70b0e` and Apps `7a69b63d`, both
EQUAL-declared.

## 2. Open PRs and branches (every repo uses `claude/lessons-handoff-execution-34mw9j`)

**No PR opened by this session is open.** The working branch in each repo:

| repo | branch head | state |
|---|---|---|
| Lessons | this docs PR's head | merges on green, served intersection 0 |
| Site | `81f445fd` | the head of #434, merged. Nothing unmerged. |
| Apps | `c0c1cf2d` | the head of #173, merged. Nothing unmerged. |
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
| `wt/limbs` | `2c8ae8ca` (on `f99d651d`) | The Science ROW + LABEL limbs and the second-cut rulings 1–4. Also the W16B title-claim refusal and the re-stamp counter fix. `restamp --self-test` 52 PASS. |
| `wt/s3` | `d90e568a` (on `f99d651d`) | S3: `admit_transaction` accepts `SHA256SUMS.txt` as a transaction member, red-proved. |
| `wt/d3` | `c01e22f8` (on `f99d651d`) | D3: verify_loop row 48, "unbounded modelling" plus "I do 2 before I do", reported RED. |
| `wt/w9l1` | `279d3930` (on `c01e22f8`) | W9L1: the declared eyebrow channel wins over the heading route. Stacked on D3. |
| `wt/site-sw` | `f877b68` (on Site `acb7bfa`) | `serve-witness.yml:31` declared floating by design, scanner constant 1→2. |

A read-only batch-1 dry-run workflow (`wf_20c1bcae-fe1`) stacks the limbs and S3 drafts on
`b1c70b0e` and runs the whole batch-1 pipeline. Its findings feed the batch-1 PR and are not a
ruling. Its reconciling critic was still running when this was written. Measured so far (to be
re-measured on the real branch before they count):
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

Item 1 is **done** (S03).

### Q1 · Limbs PR — next
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

### Q2 · S3 tool
> "S3 EXTEND admit_transaction's Science part to accept SHA256SUMS.txt as a transaction member
> (derived digest of the re-cut manifest, pinned), red-proved: a manifest not in the transaction
> → refused; a manifest whose rows disagree with member bytes → refused. No one-off declarer."

### Q3 · PASS C Autumn 2 batch 1 (11 decks)
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

| set | count | record |
|---|---|---|
| Held A, Held B, parked C, the 5 GROW `_Do` decks (D) | per record | `_sx3/HELD.md` |
| 15 LAUNCH print | 15 | `_sx3/HELD.md`, `_sx3/CHASSIS_CONTRACT.md` |
| 5 week-token disagreements (the B_W4A–W7A correction rides the limbs PR) | 5 | `_sci/WEEK_TOKEN_DISAGREEMENTS.md` |
| 2 case-study decks | 2 | `_sci/HELD.md` |
| the 51 unscoped science decks (verify_loop row 48 reds all 51 once D3 lands) | 51 | `_sx3/handoff_2026-09-22/artefacts/SCI_51.md` |
| SCI_L_W9L1: "held pending the Science row limb". It leaves HELD in the limbs PR. | 1 | `_sci/HELD.md` |
| SCI_B_W12: held on its R-GAPS exception, out of every PASS C batch | 1 | `_sx3/RELEASE_LEDGER.md:1312` |
| SCI_B_W16B: refused (title stage claims Spr1·W16). Its label is derived from the row (Spr1·W2) at PASS C, never typed. | 1 | `_sci/WEEK_TOKEN_DISAGREEMENTS.md` (corrected in the limbs PR) |
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

**Cut the limbs PR from post-fold Lessons main** (Q1). Stack the `wt/limbs` draft
(`f99d651d..2c8ae8ca`) onto Lessons main, then in the same PR:
1. Remove SCI_L_W9L1 from `_sci/HELD.md`.
2. Admit `_sci/HELD.md`, `_sx3/RELEASE_LEDGER.md` and `_sci/WEEK_TOKEN_DISAGREEMENTS.md` to
   `REVIEWED_PATHS` (the three records the re-stamp derives from).
3. Re-pin `_sx3/FENCE.json` and the tools.
4. Regenerate PIN1.
5. Sync the gate copies and land the Apps companion first.

Then measure all 31 (expect 30 proved + SCI_B_W12 held), run the adversarial review, open the PR,
wait for green and merge. `lesson-order.json` is expected unchanged, so no Site window is
expected; confirm it from built bytes.
