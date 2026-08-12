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
