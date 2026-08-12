# LSG-1 · LAUNCH Science v3+ GRAFT — decisions, at the time

Pass `lsg-1-2026-08-12`. Third sibling of BSG-1 (`_bsg1/DECISIONS.md`, merged
`dcc23dc`) and GSG-1 (`_gsg1/DECISIONS.md`, merged `e76c654`).
Written **as the pass runs**. An AMBER first seen in the final summary has failed.

---

## 0 · Base, rollback, identity

| Item | Value |
|---|---|
| `origin` | `https://github.com/MattRoper1977/Lessons` |
| Current `origin/main` | `470be572baf4f71d5656afe3aa9bd3bf97129daa` (descendant of `e76c654`, the GSG-1 merge) |
| **ROLLBACK SHA** | **`470be572baf4f71d5656afe3aa9bd3bf97129daa`** — recorded before the first commit of this pass |
| Branch | `claude/lsg-1-launch-science-graft` |
| Pack base | `dcc23dc` — one merge stale |

### Identity gate — 5/5, re-derived

1. `origin` resolves to `MattRoper1977/Lessons` ✔
2. `Science_Teesside/Launch/v3_40min/` carries **fifteen** `SCI_L_W{3..7}L{1,2,3}_*.html`
   (Microscopy → Exam_Practice) + index + manifest + guide + reflection window ✔
3. `Science_Teesside/Grow/v3_40min/SCI_G_W3A_Friction_Explore.html` carries the
   written closure line (×2) — proves post-GSG-1 ✔
4. `_gsg1/DECISIONS.md` present (and `_bsg1/DECISIONS.md`) ✔
5. `main` history contains `e76c654` **and** `dcc23dc`, both ancestors ✔

### Staleness re-verified independently

`git rev-parse dcc23dc:Science_Teesside/Launch/v3_40min` ==
`git rev-parse HEAD:Science_Teesside/Launch/v3_40min` == `acc76256…`.
**19/19 blobs byte-identical** across the two SHAs. The pack's one-merge
staleness therefore affects repo-wide claims only; every LAUNCH lesson claim is
evaluable at HEAD. Proceeding.

---

## 1 · Inputs — the two-build hazard, THIRD CONFIRMED INSTANCE

Delivery: `1978fa53-Compress_12_08_2026_104211.rar` — a **RAR5** containing a
single 27.5 MB ZIP. No `unrar`/`unar`/`bsdtar` in the environment and the apt
mirror 404s; extracted with `libarchive` via `libarchive-c`, recorded here
because the extraction route is part of the provenance chain.

**Verified against `DOWNLOAD_SHA256SUMS-4.txt` (≡ `-5.txt`, `cmp` clean):**

| Artefact | SHA-256 | Verdict |
|---|---|---|
| `LAUNCH_SCIENCE_v3PLUS_COMPLETE_PREVIEW.zip` | `ab8307da…` | OK |
| `LAUNCH_SCIENCE_v3PLUS_CHANGED_FILES_ONLY.zip` | `0f1db359…` | OK |
| `LAUNCH_SCIENCE_v3PLUS_REVIEW_PACK.zip` | `ef67d1fd…` | OK |
| `LAUNCH_SCIENCE_v3PLUS_PATCH.diff` | `c9ad555f…` | OK |

**Covered by NO checksum** — enumerated deliberately, because a provenance gate
is silent about absences: all 29 loose `SCI_L_*.html`, all 10 `.md` reports, all
10 `.png` contact sheets. **Every file this pass may quarry is uncovered.**

### Twins are one artefact, not two

**14 byte-identical `-1` twin pairs** (`cmp` clean on all 14).
**`SCI_L_W6L1_Active_Transport_Introduce.html` has no twin.**
29 files → **15 distinct artefacts**. This pass uses the unsuffixed set. A
delivery that ships fourteen duplicates is not a fifteen-plus-fourteen corpus.

### The two builds, discriminated by measurement

| Build | Where | Lesson size | `assets/` refs |
|---|---|---|---|
| **external-asset** | inside `CHANGED_FILES_ONLY.zip` | ~32 KB + `assets/launch-science-v3plus.{css,js}` (27.7 KB + 41.3 KB) | present |
| **inlined single-file** | the 15 **loose** unsuffixed files | ~101 KB | **0 across all 15**, scanner validated on a known positive (2/2) |

**DECISION: content is sourced from the loose inlined build ONLY.**
Third confirmed instance in this programme — now a pattern, not an accident.

### AMBER-INPUT-1 — the pack carries 30 bare `matchMedia`

Unit: occurrences. Universe: the 15 unsuffixed loose pack lessons. **2/file × 15
= 30**, against an estate standard of **zero**. Same consequence as GSG-1:
**every graft is hand-written into the live chassis. No pack markup bytes.**

---

## 2 · Phase 0 · verification at HEAD

Scanners validated on a synthetic known positive (12/12 returned 1) before use.
Every count carries a unit and a universe. **Eighteen prior instrument failures
are on record; one more was caught inside this pass and is recorded below.**

Universe A = the 15 live LAUNCH v3_40min lessons.
Universe B = the 15 unsuffixed loose pack lessons.

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| V1 | Written closure | **CONFIRMED** | "What I said, and what it changed" = **2/file (screen + print), 15/15, 30 occurrences total**; no-signature framing = **2/file, 15/15** · universe A |
| V2 | Witness | **CONFIRMED** | `witness` = **2/file, 15/15** · universe A |
| V3 | Print pack | **CONFIRMED, count restated** | `printTier` **1/file**, `afterprint` **1/file**, 15/15. Print family = **43/file** under the correct dialect, not ~31. See AMBER-V3 — LAUNCH is a **third dialect**. |
| V4 | Tiers | **CONFIRMED (tiers) / REFUTED (word banks)** | Supported 15 + Standard 15 + Stretch 15 = **45/file exactly**, 15/15 — matches. **Word banks are NOT 0 estate-wide: W6L1 carries 2** (screen + print), the other fourteen carry 0. See AMBER-V4. |
| V5 | Stages / arrival shape | **CONFIRMED** | Spine `title→arrival→starter→ido→wedo→ido→wedo→independent→exit` identical across **15/15**. Arrivals are **not** 3+1: three tier panels, one retrieval. Entry surface `entry-route` **15/15** on screen and `pentry` **15/15** in print — **verified before assuming** (see AMBER-INSTR-1 on the wording split). |
| V6 | Oak links | **CONFIRMED, and the v5 original LOCATED** | `thenational.academy` = **0/15** in live v3 — the loss is real. The v5 original suite carries **exactly one** external clip in the whole 15-file suite, in exactly the named file `Science_Teesside/Launch/SCI_L_W5_L2_OsmosisCP.html`. A4 can proceed. |
| V7 | Mark-scheme census | **CONFIRMED — 0 violations, context-read** | **0 regex hits across universe A.** Universe B has **3 hits, all in W7L2, all the same model-limitation caution card** rendered three times (screen, print, JSON config): *"Real mark schemes may accept more than one clear answer form."* A caution, not a scheme. **The context-read rule held: 3 hits, 0 findings.** |
| V8 | Sentinels | **CONFIRMED** | `ll-g:loop-mark` = **50**; written-closure = **123** · unit: bearing files · universe: git-tracked `*.html`. The 123-set contains **all 15 LAUNCH v3_40min files**, **10 GROW v3_40min**, and **0 BUILD v3_40min** — correct, BUILD closes through adult Audience. |
| V9 | Baseline | **CONFIRMED** | `Aut1·W2` = **0**; `Baseline_Weeks` links = **0** · universe A |
| V10 | Reading | **CONFIRMED on one selector, REFUTED on the other** | See AMBER-V10 — this is the most consequential measurement of the pass. |
| V11 | Runtime | **CONFIRMED, plus a finding** | Universe A: **0** storage / network / form / external assets — **and 0 `matchMedia`**. Universe B: 0 storage / network / form / external assets, but **30 `matchMedia`**. |

### The pack's deletions, measured — not just the closure

Universe B totals, and this is the whole case against installing it:

| Surface | live (universe A) | pack (universe B) |
|---|---|---|
| written closure line | **30** (2 × 15) | **0** |
| witness statement | **30** (2 × 15) | **0** |
| print-pack family markers | **645** (43 × 15) | **0** |
| word bank (W6L1) | 2 | 0 |
| `matchMedia` | 0 | 30 |

The pack replaces the entire tiered print pack with a **single `#printSheet`**
section, and deletes the assessor witness statement outright.

### AMBER-CLOSURE — the headline defect, characterised

The pack carries **0/15** on all three probes (`What I said, and what it
changed`, `what it changed`, `What I said`). It is not a relocation; the line is
gone.

What replaced it, from pack W5L2's Exit stage, is a generic slot:

> **4 · LAUNCH response on the existing work** — *"My edit, re-attempt or
> explanation:"* … *"Record the pupil response on the same work. The adult
> receives it. No signature is added."*

So the pack **keeps the no-signature framing and loses the ratified line**.
The slot number is even the same (`4 ·`) as the GROW pack's `4 · GROW written
close`, which *did* carry "What I said, and what it changed". **Same builder,
same slot, opposite outcome.** Register entry at §7.

**Decision: live is correct at 15/15 and is not touched. Nothing to add, nothing
to move, nothing to lose. Sentinels hold at 50/123 for the whole pass.**

### AMBER-V3 — LAUNCH is a THIRD print dialect

Unit: occurrences per file. Universe A. The three-dialect warning is concrete
here, and counting LAUNCH with GROW's dialect returns a false low:

| dialect | tokens | LAUNCH count/file |
|---|---|---|
| GROW's | `print-pack`, `print-route`, `print-box` | **0** |
| BUILD's | `pp`, `proute` | present |
| LAUNCH's own | `printpack`, `pline`, `pidline`, `pentry`, `scaf`, `box` | present |
| shared | `data-tier` (17), `print-section`, `print-witness`, `printTier`, `afterprint` | present |

Full family under the correct union = **43/file, uniform 15/15**. The brief's
"~31" does not reproduce; the difference is dialect scope, not a defect. My
first probe using the GROW dialect returned a plausible-looking **19** — a
number that would have been wrong in the same silent way the register's
eighteen failures were wrong.

### AMBER-V4 — word banks are not 0 estate-wide

W6L1 carries a word bank on **both** the screen (`"Fill in the comparison table.
Use the word bank."`) and the print route (`"Fill comparison table from word
bank."`). The other fourteen carry none. The brief's "word banks 0 — do not
restore what never existed" is right for fourteen files and wrong for one.
**Consequence: the gate baseline is the measured vector, and W6L1's word bank is
protected.** The pack carries none — so installing it would delete that too.

### AMBER-V10 — the reading claim splits by selector, and the split is the finding

Selector A (pupil-facing stage prose) and Selector B (whole-file), both stated
in `_lsg1/reading/fk.py`, both applied identically to live and pack:

| selector | live mean | pack mean | delta | pack higher |
|---|---|---|---|---|
| **B · whole-file** | 7.96 | 5.55 | **−2.42** | **0/15** |
| **A · pupil-facing** | 5.99 | 5.15 | **−0.84** | **1/15 — W5L1, +0.26** |

**The brief's "0/15 higher" is CONFIRMED on whole-file and REFUTED on
pupil-facing prose.** The direction is right on both; the magnitude is not.

Why it matters rather than being pedantry: **roughly two-thirds of the pack's
apparent reading win is in text pupils never read** — staff notes, print
furniture, provenance strings. On the prose actually projected to a pupil the
gain is −0.84, and in one lesson it is negative. A pack marketed on a −3.47
whole-file drop delivers −0.84 where it counts.

The brief's live ≈11.58 does not reproduce (mine: 7.96 whole-file / 5.99
pupil-facing) — expected, and the brief said to treat its figure as direction
only.

### AMBER-INSTR-1 — instrument failure #19, mine, caught inside this pass

A cwd from a previous command persisted into a `grep` path, and the live
closure-line check returned **0/15** — a catastrophic-looking false negative on
the single most protected surface in this pass. Re-derived from the repo root:
**15/15, 30 occurrences.** Recorded rather than quietly fixed, because the
failure mode is exactly the register's: *a negative whose universe was wrong.*
Every subsequent census in this pass runs from an absolute path.

The related wording split is **not** a defect and was verified before being
assumed: `entry-route` is 15/15, of which **14 read "Not here last lesson?" and
1 (W3L1) reads "New to this class, or not sure?"** — correct, because W3L1
follows the baseline weeks and has no last lesson to have missed. Identical
by-design split to GROW's.

---

## 3 · Reading — no band exists, and none has been asked for

The pack ships a **"9.0–14.0 years" release gate**. It is invented.

- **No LAUNCH reading band has ever been supplied to this programme.**
- Unlike GROW's — which is *with the SENCo and pending* — **LAUNCH's has not
  even been requested.**

This pass therefore reports **deltas with selectors stated and no verdict**,
never estimates a reading age, and never attaches a level to a pupil.

**Flag to Matt, recorded here so it reaches the right conversation:** the SENCo
discussion already open for the GROW band should collect the **LAUNCH** band in
the same sitting. When either arrives it becomes that pathway's standing target
and this pass's "after" column becomes its baseline.

---

## 4 · Pathway split — three pathways, two closure shapes

- **BUILD** closes through the adult Audience strip, **no** pupil-written line.
- **GROW and LAUNCH** close through the pupil-written line *"What I said, and
  what it changed"*, adult as audience, **no signature or initial**.

This pass touches **no** BUILD file and **no** GROW file, moves no closure
surface in any direction, and infers no band across pathways.

---

## 5 · Phase B · the refusal set — considered and DECLINED

| Declined | Reason |
|---|---|
| **The pack's fifteen files as installed lessons** | Graft, don't replace. Installing them would delete the written closure (30 → 0), the assessor witness statement (30 → 0), the entire tiered print pack (645 family markers → 0) and W6L1's word bank, and would import 30 bare `matchMedia`. |
| **The closure deletion — the pack's worst defect, named as such** | The ratified LAUNCH closure is the pupil-written line, adult as audience, no signature. The pack replaces it with a generic "My edit, re-attempt or explanation" textarea while keeping the no-signature framing. Live is correct at 15/15 and is untouched. |
| The external-asset (zip) build | Single-file rule; offline staff packs. Loose inlined build only, as a quarry for wording and mechanism. |
| Witness / tier / print-depth deletions | Assessment record (UAS route); the tiers ARE the school's scaffolded, TA-supported provision; the tiered print pack is what staff teach from. All verified intact or richer. |
| The invented 9.0–14.0 reading gate | No LAUNCH band exists **and none has been requested**. Deltas only. See §3. |
| Any replacement window or index | Not installed. The live reflection window and index are kept; the index gains one link. |
| The marked-correct commit device | The pack's `lessonConfig` carries `"correct": 0` **and** `"guided_correct": 0` in all fifteen files — checked and recorded before deciding. Ported judgement-free. |
| `#printSheet` as the print story | Not installed. The pack replaces a 43-marker tiered print pack with one sheet; at most it could ever land as one additional section beside the full pack. |
| Any pack markup bytes | 30 bare `matchMedia` against an estate standard of zero. Everything is hand-written. |
| Phantom-lab advertising | Audited for, and **not found** — see AMBER-A7-CREDIT. The one imprecision was corrected. |
| The pack's seven-rung prompt ladder | Present in the pack's TA blocks. A seventh WT-DS wording is RED; queue-16 owns reconciliation. Left behind. |
| Sourcing the Progress lockup | Human-only. The `--mirror` build hard-stops without it; reported, not worked around. |
| Any cross-pathway closure move | BUILD closes through adult Audience with no written line; GROW and LAUNCH close through the pupil-written line. No BUILD or GROW file was touched. |

---

## 6 · What was grafted, by school stage

| Stage | What landed | Where |
|---|---|---|
| **Arrival** | Rebuilt to **3 retrieval + 1 lead-in** at all three tiers (12 questions/file). R1 last lesson · R2 previous week · R3 older · L lead-in. Every question carries a non-reading route **and** a named tier step. Thin-history substitutions declared on the slide. | A2 · 15/15 screen + print |
| **Starter** | Judgement-free predict-commit. Nothing marked, scored or stored. | A5 · 15/15 |
| **I Do** | "What this model helps us see / does not show" pair. | A5 · 15/15 screen + print |
| **I Do (W5L2)** | The restored Oak osmosis clip, beside the teaching. | A4 · 1/15 |
| **We Do** | **One specimen only** — W5L2 Osmosis prediction lab, beside the live calculator. | A6 · 1/15, then STOP |
| **Independent** | WORD HELP bridges: Biology term dominant, bridge hidden until requested, TA fade route. | A5 · 15/15 screen + print |
| **Exit** | Speech route added **outside** the close block; the closure line itself untouched. | A5 · 15/15 |

**A2 summary.** The retrieval spine follows LAUNCH's three-lesson weekly arc:
L2 retrieves L1; L3 retrieves L2 then L1; each week's L1 retrieves the prior
week's arc. W3L1 is elicitation-only and says so, because W1–W2 are baseline.
W3L2 and W3L3 declare their substitutions too — Week 3 has no taught week behind
it. **`Aut1·W2` remains 0 and `Baseline_Weeks` remains 0**: no baseline topic is
named and the baseline pack is never linked. The entry surface was **verified
before being assumed** and is 15/15 on screen (`entry-route`) and 15/15 in print
(`pentry`), with W3L1's wording correctly differing because it follows baseline.

**A4 result: RESTORED.** The v5 original carries exactly one external clip in
the whole fifteen-file suite, in the named file. URL read from that file at run
time, asserted **byte-equal**, one occurrence in live W5L2, zero in the other
fourteen, new tab with `noopener noreferrer`, Oak named as the source,
needs-internet and captions noted, "this lesson teaches fully without it"
stated, and **hidden from the print pack**. The item did not collapse.

---

## 7 · Reading — deltas, no verdict, and a band nobody has asked for

Selector A (pupil-facing stage prose), stated in `_lsg1/reading/fk.py`, applied
identically to baseline, working tree and pack.

| file | base | after | delta | pack |
|---|---|---|---|---|
| W3L1_Microscopy_Introduce | 6.09 | 3.87 | **−2.22** | 5.54 |
| W3L2_Calculating_Magnification | 5.17 | 4.30 | **−0.87** | 4.22 |
| W3L3_Magnification_Lab_Do | 5.02 | 4.45 | **−0.57** | 4.95 |
| W4L1_Diffusion_Introduce | 5.72 | 4.15 | **−1.57** | 4.79 |
| W4L2_Diffusion_Lungs_Explore | 5.71 | 4.14 | **−1.57** | 4.74 |
| W4L3_Diffusion_Explanation_Do | 5.88 | 4.55 | **−1.33** | 4.88 |
| W5L1_Osmosis_Introduce | 5.08 | 3.88 | **−1.20** | 5.34 |
| W5L2_Osmosis_Core_Practical | 6.80 | 4.60 | **−2.20** | 5.68 |
| W5L3_Osmosis_Data_Do | 6.15 | 4.53 | **−1.62** | 5.36 |
| W6L1_Active_Transport_Introduce | 6.54 | 4.12 | **−2.42** | 5.98 |
| W6L2_Root_Hairs_And_Gut | 5.77 | 4.01 | **−1.76** | 5.36 |
| W6L3_Compare_Transport_Do | 7.11 | 4.49 | **−2.62** | 5.40 |
| W7L1_Topic_1_Round_Up | 6.73 | 4.37 | **−2.36** | 5.05 |
| W7L2_Command_Words_Explore | 5.67 | 4.03 | **−1.64** | 4.77 |
| W7L3_Exam_Practice_Do | 6.40 | 4.56 | **−1.84** | 5.18 |
| **mean** | **5.99** | **4.27** | **−1.72** | **5.15** |

Lower in **15/15**, and now **below the pack's own pupil-facing figure** while
keeping the closure, witness, print pack and tier depth the pack deletes.

**No verdict is attached to any number here.** No reading age is estimated and
no level is attached to any pupil.

**Recorded, and it needs Matt's action: no LAUNCH band exists, and unlike
GROW's it has never even been requested.** GROW's is with the SENCo and pending;
LAUNCH's has not been asked for at all. **The SENCo conversation already open
for GROW should collect the LAUNCH band in the same sitting.** When either
arrives it becomes that pathway's standing target and this table's "after"
column becomes its baseline.

---

## 8 · AMBERs, every one by name

| # | AMBER | Where |
|---|---|---|
| AMBER-INPUT-1 | The pack carries **30 bare `matchMedia`** (2/file × 15) against an estate standard of zero. Consequence: nothing copy-pasted; every graft hand-written. | §1 |
| AMBER-CLOSURE | **The pack deletes the ratified closure line from all fifteen files** and substitutes a generic response slot in the same numbered position, keeping the no-signature framing. Characterised in full at §2. | §2 |
| AMBER-V3 | **LAUNCH is a THIRD print dialect** — BUILD's `pp`/`proute` plus its own `printpack`/`pline`/`pidline`/`pentry`. Full family = 43/file, not ~31. Counting it with GROW's dialect returned a plausible **19** that would have been silently wrong. | §2 |
| AMBER-V4 | **Word banks are not 0 estate-wide**: W6L1 carries one on screen and in print. Protected accordingly; the pack carries none. | §2 |
| AMBER-V10 | **The reading claim splits by selector.** "0/15 higher" holds whole-file (−2.42) and fails on pupil-facing prose (−0.84, W5L1 up +0.26). About two-thirds of the advertised win is in text pupils never read. | §2 |
| AMBER-INSTR-1 | **Instrument failure #19, mine**: a persisted cwd made the live closure check read **0/15** on the most protected surface in the pass. Re-derived from the repo root: 15/15. It recurred once more during the reading step and was caught the same way. | §2 |
| AMBER-INSTR-2 | **Instrument failure #20, mine**: my own JS comment contained the literal token `matchMedia` while asserting the layer had none — my scanner hit my own sentence and the transform failed closed. **The context-read rule applies to my own text.** Reworded so the emitted file genuinely contains zero. | A5 |
| AMBER-INSTR-3 | **Instrument failure #21, mine**: gate 5b counted `class="lq` , which prefix-matches `lq-head`/`lq-ask`/`lq-route`/`lq-badge`/`lq-declare`, inflating 12 questions to 24–25. Corrected to an exact match. | §6 gates |
| AMBER-INSTR-4 | **Instrument failure #22, mine**: the close-block guard captured as far as the *next sibling*, so an insertion that never touched the block still tripped it. Tightened to the block's own closing tag. Caught because the transform fails closed rather than warning. | A2 |
| AMBER-A3-SCOPE | **A3 is deliberately small on LAUNCH.** The suite's heaviest pupil-facing sentence sits inside the protected close block and is RED to alter — the single biggest available reading win is one this pass may not take. Named, not worked around. | A3 |
| AMBER-A3-VOCAB | The A2 rebuild displaced **seven** protected terms across four files. The gate caught every one; the questions now carry them rather than the gate being relaxed. | A3 |
| AMBER-PACK-BLEED | **The pack ships GROW content in all fifteen LAUNCH files.** The printed Exit sentence frame reads *"Friction helped when ___. It caused a problem when ___."* on every LAUNCH GCSE Biology lesson. Context-read confirmed `lever`/`Moon`/`planet` are dead CSS class names (build bloat), but the friction frame is **pupil-visible print content**. | A3 |
| AMBER-A7-CREDIT | **The pack's equipment matrix is accurate.** Audited for the GROW defects and found neither: no degenerate columns, and all fifteen named labs verified present. I had expected phantom labs and was wrong. Recorded as a finding in the pack's favour; only its digital column's imprecision was corrected. | A7 |
| AMBER-LOCKUP | `--mirror` hard-stops for want of the real Progress lockup. Expected, reported, **not worked around**. The non-mirror pack builds clean at 328 files. | A7 |
| AMBER-CRAWL | The staff-pack crawl reports missing `Baseline_Weeks` and `_sciv3` targets from the three v3 indexes. **Pre-existing** — baseline lives on PythonAnywhere by design. Not introduced here. | A7 |

---

## 9 · Register entries

**1 · The same-builder-opposite-defect finding.** One builder produced all three
sibling packs. In **GROW** it *fixed* the missing closure line, supplying the
ratified wording in a slot headed "4 · GROW written close". In **LAUNCH** it
*deleted* the same line from all fifteen files, in a slot headed "4 · LAUNCH
response on the existing work" — same builder, same slot number, opposite
outcome, and a repeat of the regression its own earlier LAUNCH pack made.

*A pack family's quality is per-pack and is never inherited.* Sibling of the
standing rule that **a register ID quoted across passes inherits authority it
never had**: provenance is not quality, and neither is a good sibling.

The corollary, proved twice in this pass: **the reverse is equally true.** The
LAUNCH equipment matrix was audited expecting GROW's degenerate columns and
phantom labs and had neither. A pack that is worse in one place is not worse
everywhere, and a finding in a pack's favour must be recorded as carefully as a
fault.

**2 · The context-read rule for scanner hits.** *A regex hit is not a finding
until its context is read.* Established by the W7L2 precedent — the pack's only
mark-scheme hits are a **caution card** saying real mark schemes accept more
than one answer form. Applied four times in this pass, and it changed the verdict
every time: 3 mark-scheme hits → 0 findings; `lever`/`Moon`/`planet` in the pack
→ dead CSS, not content; two mark-scheme hits on my own matrix → inside my own
prohibition; and **one hit inside my own JS comment**, which is the sharpest form
of the rule — *it applies to your own text, not only to other people's.*

**3 · The third two-build delivery.** Checksummed zips carried the ~32 KB
external-asset build plus `assets/`; the loose files carried the ~101 KB inlined
build. Third confirmed instance — the discriminator (`assets/` count and file
size) should now be run on every delivery before anything is quarried. Note also
that the checksums covered only the four zips/diff: **every file this pass could
legitimately quarry carried no checksum at all.** And the fourteen byte-identical
`-1` twins are **one artefact each, not two** — 29 files, 15 distinct.

**4 · The LAUNCH band has never been requested.** GROW's reading band is with
the SENCo and pending. LAUNCH's has not been asked for. Both are recorded here as
unsupplied, with the action chained to the one conversation already open: collect
both bands in the same sitting.

---

## 10 · Sentinels — the "unchanged" green shape

GSG-1's green shape was *moved exactly as declared*. **LSG-1's is *unchanged*.**

| sentinel | main | branch tip | required |
|---|---|---|---|
| `ll-g:loop-mark` | 50 | **50** | unchanged **and set-identical** |
| written-closure line | 123 | **123** | unchanged **and set-identical** |

Unit: bearing files. Universe: git-tracked `*.html`. Both bearing sets are
**file-for-file identical to main's** at every gate run and at the final tip —
not merely equal in size. The 123-set contains all 15 LAUNCH v3_40min files, all
10 GROW v3_40min files, and 0 BUILD v3_40min files.

There is **no declared movement in this pass**. Any change in either number, at
any commit, would be a defect and a stop.

## 11 · Rollback

`git reset --hard 470be572baf4f71d5656afe3aa9bd3bf97129daa` restores the
pre-pass estate exactly. Nothing outside `Science_Teesside/Launch/v3_40min/` and
`_lsg1/` was modified — asserted as gate 15.

---

## 12 · AMBER-INSTR-5 — instrument failure #23, mine, at the last gate

The scope check `git diff --name-only <base>..HEAD -- 'Science_Teesside/Launch/*.html'`
reported **18 changed v5 original files** — which would have meant this pass had
edited the frozen v5 suite that A4 quarries from, a serious breach.

It had not. **Git pathspecs are not shell globs: `*` crosses directory
boundaries**, so the pattern matched everything under `v3_40min/` as well.
Re-derived with `:(glob)Science_Teesside/Launch/*.html`, which does not cross
`/`: **0 v5 originals changed.**

Same family as the other four in this pass: *a count whose universe was wrong.*
It is the third distinct way a universe has gone wrong here — a persisted cwd
(#19), a prefix-matching class selector (#21), a guard that captured past its
own boundary (#22), and now a pathspec whose wildcard is broader than it looks.
**Recorded because the number was alarming and false, and the reflex to believe
an alarming number is exactly what the register exists to interrupt.**

---

# LSG-1C · VERIFY & CLOSE — continuation session, 2026-08-12T10:49Z

Pass `lsg1c-nav1-2026-08-12`. A fresh session picks up the branch at `a8d7090`
under the superseding master prompt (`lsg1c-nav1-2026-08-12-TOP`). Everything
below is written **at the time**, same rule as above.

## C0 · Sign-off — recorded verbatim, both readings

**Matt, 2026-08-12:** *"please triangulate everything within lsg 1 input 2,
the addendum and to finish what's outstanding here."*

1. **Reading one — the W5L2 specimen is signed off.** The stop at A6 ("one
   specimen, then STOP") is cleared; the specimen pattern is the approved
   pattern for the remaining labs.
2. **Reading two — delegation to complete the pass**, including the conditional
   merge authority at §5 of the master prompt: merge only if every gate is
   green, with the rollback SHA recorded first.

## C1 · Identity at session start — 5/5

1. `origin` = `MattRoper1977/Lessons` ✔
2. `claude/lsg-1-launch-science-graft` at tip `a8d7090`, **unmerged** ✔
3. `origin/main` = `470be572…` **exactly** — no movement since the pass began ✔
4. 15 LAUNCH lessons on main; GROW W3A closure ×2 ✔
5. `_lsg1/DECISIONS.md` on the branch ✔

## C2 · Triangulation of the previous session's report — T1–T10

| # | Claim | Verdict | Evidence, re-derived at `a8d7090` |
|---|---|---|---|
| T1 | Sentinels 50 / 123, set-identical | **CONFIRMED** | `ll-g:loop-mark` bearing files = **50**; closure line = **123**; unit bearing files, universe git-tracked `*.html`; both sets **file-for-file identical to main's** (diff of sorted lists empty). Derived fresh because the report's block arrived empty in transit. |
| T2 | Closure ×2, 15/15, untouched | **CONFIRMED** | 2/file exactly, 15/15. |
| T3 | Witness 15/15, 30 occurrences | **CONFIRMED** | 2 occurrences/file × 15 = 30. |
| T4 | Third print dialect, family ≈43/file | **CONFIRMED in substance; figure scanner-dependent** | The dialect is real: GROW's hyphenated tokens = **0** in LAUNCH; BUILD-shared `pp`/`proute`/`printpack`/`pline` present; LAUNCH-only `prgrid`/`prcell`/`print-section`/`print-witness` present. My validated ten-token structural scanner returns a **uniform 36/file, 15/15** — recorded as this session's per-file baseline; the report's 43 included `scaf`/`box`-family tokens whose exact scope its scanner owned. Gates assert **≥36 uniform**, set-stable. |
| T5 | W6L1 word bank, screen+print, the only one | **CONFIRMED** | Screen "Use the word bank." + print "Fill comparison table from word bank." — W6L1 only, 1/15. |
| T6 | A4 Oak clip | **CONFIRMED** | Exactly one external URL in the whole suite, in W5L2; byte-equal to the v5 original's (`SCI_L_W5_L2_OsmosisCP.html`); `target="_blank" rel="noopener noreferrer"`; Oak named; "teaches fully without it" stated; single occurrence sits before `printpack` and the specimen CSS carries `@media print{.oslab{display:none}}` — absent from every print surface; 0 external URLs in window/guide/index. |
| T7 | W5L2 specimen | **CONFIRMED** | `.oslab` predict-commit → three-solution test with frozen results list → keep/repair glitch, beside the live percentage-change widget; identity solid/dashed/dotted + ▲◎✳ + words; 0 `matchMedia`; own class family, no pack markup. |
| T8 | Reading artefacts + figures | **CONFIRMED** | `_lsg1/reading/` present, selectors stated in `fk.py`. Recomputed from `fk_table.json`: pupil 5.99 → 4.27, **−1.72, 15/15 lower**. Honesty note decodes exactly: pack whole-file −2.41, pack pupil-facing −0.84, W5L1 pack +0.26 above base. No LAUNCH band exists; deltas only. |
| T9 | Footprint | **CONFIRMED** | 52 files changed main→`a8d7090`, all inside `Science_Teesside/Launch/v3_40min/` (18) and `_lsg1/` (34). BUILD / GROW / v5 originals / legacy trees: **0 changed**. |
| T10 | Mark-scheme census 0 | **CONFIRMED** | All pattern hits are prohibitions/cautions (matrix "No mark schemes… appear anywhere in this suite"; W7L2/W7L3 "not grades", "No public marks"). Context-read: 0 findings. |

**No claim REFUTED. The pass proceeds.**

## C3 · INPUT-2 — REPLACED MID-RUN, and the guard rises to six builds

The replacement notice (`lsg1c-nav1-input2r-2026-08-12`) arrived at
2026-08-12T10:45Z, **before §3 started** — so all fifteen labs use the rebuilt
map. Both packs share one filename and are different artefacts:

| Pack | Files | Sums | Lessons under | Verdict |
|---|---|---|---|---|
| EARLIER (66 files, `launch_v3plus/`, unprefixed labs) | 66 | none | `launch_v3plus/` | **Discarded as a quarry** — superseded |
| REBUILT (86 files, `PACKAGE_SHA256SUMS.txt`) | 86 | **85/85 OK** (`sha256sum -c`) | `Science_Teesside/Launch/v3plus_local_preview/` | **Authoritative INPUT-2, design quarry only** |

- **Fingerprint guard (now SIX builds):** authorized content source remains
  solely the build whose W3L1 = `db757a23…`. The earlier preview's W3L1 =
  `3ea778d6…` (refused); the rebuilt pack's W3L1 = `351907aa…` (refused — a
  sixth build). Neither was needed: the branch already carries the grafts.
- **Refused as bytes:** both packs' 15 lesson files, `assets/`, reflection
  windows, `serve_preview.py`/`start_preview.*`/`run_preview.py`, `verify_*.py`,
  `tests/*.py`, reports, and the earlier pack's `.pyc`.
- **Accepted as reference:** rebuilt `science-labs/` (15 lesson-prefixed
  designs), `lab-logic.mjs` + `tests/lab_logic_fixtures.mjs`, screenshots.
- **`Science_Teesside/Launch/v3plus_local_preview/` IS NOT A DESTINATION** —
  repo-path-shaped preview workspace; nothing is committed to that path and no
  parallel route is created from it.
- **Fixtures: `node tests/lab_logic_fixtures.mjs` → suite passes with 20/20
  checks.** AMBER-FIXTURE-COUNT: the notice said 19; the suite carries **20**
  (measurement beats document; everything passes).
- Census on the 15 rebuilt designs + engine: 0 storage / network / forms /
  external URLs. The pack's own `matchMedia` (1, in `lab-engine.mjs`, which
  never ships) and two "mark scheme" strings (both disclaimers) are
  **caveats, not violations** — context-read, as the notice directs.

### The lesson→lab map, READ FROM THE PACK (supersedes the prompt's map)

| Lesson | Design | Note |
|---|---|---|
| W3L1 | `microscope_observation_lab` | |
| W3L2 | `cell_scale_lab` | prompt said magnification_lab — pack wins |
| W3L3 | `magnification_evidence_lab` | |
| W4L1 | `particle_evidence_chamber` | |
| W4L2 | `gas_exchange_evidence_lab` | |
| W4L3 | `diffusion_explanation_studio` | prompt said particle/gas as LO directs — pack wins |
| W5L1 | `membrane_reasoning_lab` | **closes the W5L1 gap** — prompt had none |
| W5L2 | `potato_osmosis_investigation` | already live — the A6 specimen |
| W5L3 | `osmosis_data_studio` | |
| W6L1 | `against_gradient_lab` | prompt said active_transport_gradient_lab |
| W6L2 | `uptake_evidence_lab` | |
| W6L3 | `transport_decision_lab` | prompt said + membrane_reasoning_lab; pack assigns membrane reasoning to W5L1 |
| W7L1 | `knowledge_map_lab` | |
| W7L2 | `question_decoder_lab` | |
| W7L3 | `biology_evidence_paper` | |

Earn-the-place still decides per LO; an honest AMBER-unbuilt stays valid.
