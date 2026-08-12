# GSG-1 · GROW Science v3+ GRAFT — decisions, at the time

Pass `gsg-1-2026-08-12`. Sibling of BSG-1 (`_bsg1/DECISIONS.md`, merged `dcc23dc`).
This file is written **as the pass runs**, not afterwards. An AMBER first seen in
the final summary has failed.

---

## 0 · Base, rollback, identity

| Item | Value |
|---|---|
| `origin` | `https://github.com/MattRoper1977/Lessons` — the real repo, not the `mattroper1977.github.io` decoy |
| Current `origin/main` | `dcc23dc2485516eb5d50409494c7d70f56c62f78` |
| **ROLLBACK SHA** | **`dcc23dc2485516eb5d50409494c7d70f56c62f78`** — recorded before the first commit of this pass |
| Branch | `claude/gsg-1-grow-science-graft-wp8p48` |
| Pack base | `574035bf` (Merge PR #92, PACK-4 OneDrive mirror) — one merge stale |

### Identity gate — 5/5, all re-derived

1. `origin` resolves to `MattRoper1977/Lessons` ✔
2. `Science_Teesside/Grow/v3_40min/` carries **ten** `SCI_G_W{3..7}{A,B}_*.html`
   (Friction, Mechanisms, Fair_Test, Earth_And_Planets, The_Moon) + index +
   `manifest-v3.json` + `TEACHER_IMPLEMENTATION_GUIDE.html` +
   `LUNDY_DAILY_REFLECTION_EVIDENCE_WINDOW.html` ✔
3. `Science_Teesside/Build/v3_40min/` carries the BSG-1 grafted BUILD suite
   incl. `BUILD_SCIENCE_PRACTICALS_MATRIX*.html` — proves post-BSG-1 ✔
4. `_bsg1/DECISIONS.md` present ✔
5. `main` history contains `dcc23dc` and `651a88e` (both ancestors of `origin/main`) ✔

### Staleness re-verified independently (not taken from chat)

`git rev-parse 574035bf:Science_Teesside/Grow/v3_40min` ==
`git rev-parse dcc23dc:Science_Teesside/Grow/v3_40min` == `06b49ca2…`.
All **14/14** blobs in the directory byte-identical across the two SHAs.
The pack's staleness therefore affects **repo-wide claims only**; every GROW
lesson claim it makes is evaluable at HEAD. Proceeding.

---

## 1 · Inputs — the two-build hazard, SECOND CONFIRMED INSTANCE

Delivery: `494dd216-Compress_12_08_2026_093154.zip`, 22 entries.

**Received and verified:**

| Artefact | SHA-256 | Verdict |
|---|---|---|
| `GROW_SCIENCE_v3PLUS_COMPLETE_PREVIEW.zip` | `ab207319…` | OK |
| `GROW_SCIENCE_v3PLUS_CHANGED_FILES_ONLY.zip` | `680065c4…` | OK |
| `GROW_SCIENCE_v3PLUS_REVIEW_PACK.zip` | `041f6380…` | OK |
| `GROW_SCIENCE_v3PLUS_PATCH.diff` | `20d285cf…` | OK |

**Duplicate pairs, both byte-identical (`cmp` clean):**
`DOWNLOAD_SHA256SUMS-2.txt` ≡ `-3.txt`;
`GROW_SCIENCE_v3PLUS_REVIEW_PACK-1.zip` ≡ `…REVIEW_PACK.zip`
(the `-1` duplicate carries the same `041f6380…` sum but is **not itself listed**
in either sums file).

**Received but covered by NO checksum (a provenance gate is silent about
absences — enumerated here deliberately):** all ten loose
`SCI_G_*.html`, and all five `.md` reports
(`FINAL_SUMMARY`, `LUNDY_MATRIX`, `READING_AGE_REPORT`, `STAGE_LABEL_MATRIX`,
`TEST_REPORT`). **The only files this pass is permitted to quarry are the ten
that carry no checksum.** Recorded, not waved through.

### The two builds, discriminated by measurement

| Build | Where | Lesson size | `href="assets/`/`src="assets/` |
|---|---|---|---|
| **external-asset** | inside `CHANGED_FILES_ONLY.zip` / `COMPLETE_PREVIEW.zip` | ~30 KB + `assets/grow-science-v3plus.{css,js}` (20 KB + 35 KB) | present — the zip ships the two asset files |
| **inlined single-file** | the ten **loose** `SCI_G_*.html` | ~87 KB | **0/10, scanner validated on a known positive** |

**DECISION: this pass sources content from the loose inlined build ONLY.**
The zip build would break the single-file rule and the offline staff packs.
This is the **second confirmed instance** of a two-build delivery in this
programme; entered in the register at §8.

### AMBER-INPUT-1 — the pack carries 20 bare `matchMedia`

Unit: occurrences. Universe: the ten loose pack `SCI_G_*.html`.
**2 per file × 10 = 20.** The BSG-1 estate standard is **zero**.
Consequence, decided now: **every graft in this pass is hand-written into the
live chassis idiom. Nothing is copy-pasted from a pack file.** The pack is a
quarry for *wording and mechanism*, never for markup.

---

## 2 · Phase 0 · verification at HEAD

Every scanner below was validated against a known positive before use.
Every count carries a unit and a universe. Thirteen prior instrument failures
were all unstated-universe negatives; two more were caught *inside this pass*
and are recorded as such rather than silently corrected.

| # | Claim | Verdict | Evidence (unit · universe) |
|---|---|---|---|
| V1 | Print pack | **CONFIRMED** | Universe: 10 live lessons. `data-tier` = **22/file**; print-pack family (`print-pack` 3 + `print-route` 8 + `print-box` 8) = **19/file**; token `printTier` = **6/file**; `afterprint` = **1/file**. 10/10 uniform. Also present: `print-page` 4, `print-line` 4, `data-print-tier` 4, `print-witness` 1, `print-section` 1. |
| V2 | Witness statement | **CONFIRMED** | `witness` (case-insens) = **2/file**, 10/10 · 10 live lessons |
| V3 | Oak links | **CONFIRMED** | `thenational.academy` URLs: 1–3/file, **W4A carries 3**, W6A carries 2, remaining eight carry 1. **Suite total = 13** · 10 live lessons |
| V4 | Tier depth | **CONFIRMED (tiers) / REFUTED (word bank)** | Supported 20 + Standard 20 + Stretch 21 = **61/file exactly**, 10/10 — matches. **Word bank is NOT ×2/file: it is 2 FILES out of 10** (W3A ×4, W5A ×2; the other eight carry zero). See AMBER-V4. |
| V5 | School grammar | **CONFIRMED** | Typed stages present 10/10: `data-type=` arrival/starter/ido/wedo/ido2/wedo2/independent/exit; label occurrences uniform across the suite |
| V6 | **Closure gap** | **CONFIRMED** | "What I said, and what it changed" = **0/10** in live GROW v3_40min. Probed three ways (full line, `what it changed`, `What I said`) — 0 on all three. **The gap is real.** See AMBER-V6 for what live *does* carry. |
| V7 | Sentinels | **CONFIRMED** | `ll-g:loop-mark` = **50 bearing files**; written-closure line = **113 bearing files**. Unit: bearing files. **Universe: git-tracked `*.html`** — the universe ratified at BSG-1 (`_bsg1/DECISIONS.md` L95). GROW v3_40min contributes **0** to the 113; BUILD v3_40min also **0** (correct — BUILD closes through adult Audience). See AMBER-INSTR-1. |
| V8 | Reflection window | **CONFIRMED** | `LUNDY_DAILY_REFLECTION_EVIDENCE_WINDOW.html` = **5,776 B** vs BUILD's 9,710 B. Five Lundy stages (SPACE/VOICE/AUDIENCE/INFLUENCE/lean evidence), **zero** BUILD-style diagnostic branches, **zero** score/counter/tally/"of N". A different artefact from BUILD's, as stated. |
| V9 | Baseline | **CONFIRMED** | `Aut1·W2` = **0** across the ten. `Aut1` = 18 (all `Aut1·W3`…`Aut1·W7`, i.e. taught weeks only). `Baseline_Weeks` = **0** — nothing links the baseline pack. W3A already states "Weeks 1 and 2 were baseline. There is no previous lesson to recall." |
| V10 | Reading | **CONFIRMED in direction, REFUTED in absolute level** | Selector stated in `fk.py` docstring, applied identically to both corpora. Live whole-file FK mean **7.38** (6.83–7.96); pack mean **4.85** (4.42–5.67); mean delta **−2.53**; pack higher than live in **0/10**. The *direction* and the *0/10* claim confirm. The brief's absolutes (8.52 / 7.11) do not reproduce under a stated selector. See AMBER-V10. |
| V11 | Runtime | **CONFIRMED as written** | Live 10/10 and pack 10/10: **0** storage, **0** network, **0** `<form`/form-action, **0** external CSS/JS/assets. But `matchMedia` — not in V11's list — is **0 live / 20 pack**. See AMBER-INPUT-1. |

### AMBER-INSTR-1 — instrument failure #15 and #16, caught inside this pass

Both were mine, both caught before they reached a verdict, both recorded
rather than quietly fixed:

- **#15 · wrong universe on the sentinels.** First derivation used "all files
  in the working tree excluding `.git`" and returned **82 / 138** instead of
  50 / 113. The ratified universe is **git-tracked `*.html`**. Under it the
  numbers reproduce exactly. *The count was never wrong; the universe was.*
- **#16 · wrong unit on `printTier` and on the entry line.** `grep -F 'printTier('`
  returns 4 (paren-bearing call sites only); the claim is about the **token**,
  which is 6. Likewise the "entry line" probed as the literal string
  `New to this class` returns **1/10** — but the *surface* is the
  `entry-route` div, which is **10/10**. W3A's wording differs
  ("New to this class, or not sure?" vs "Not here last lesson?") **correctly**,
  because W3A follows the baseline weeks and has no last lesson to have missed.
  A count that looked like a 1/10 catastrophe was a design feature.

The brief warned the BSG-1 premise of 10/10 was wrong at 1/10 and told me to
verify, never assume. Verified: **the entry surface is 10/10 and healthy.**

### AMBER-V4 — the word bank is 2 files, not 2 per file

Live word-bank mentions, unit: occurrences, universe: 10 live lessons —
W3A **4**, W5A **2**, all other eight **0**. The brief's "word bank ×2/file"
does not reproduce. **Estate wins; the disagreement is the finding.**
Consequence for gate 7: the per-file baseline this pass must not fall below is
the measured vector `[4,0,0,0,2,0,0,0,0,0]`, not a flat 2. Word banks are
**not** deleted anywhere, and this pass adds WORD HELP bridges (A4) on top.

### AMBER-V6 — live GROW is not closure-less; it is missing *this* line

V6 confirms 0/10 for "What I said, and what it changed". But the live Exit
slide **already carries a pupil-written closure line**: `close-line` →
*"3) Pupil writes: **“Next I will ______.”**"* with
*"No adult signature, initial or second receipt mark."*

These are **different instruments**: `Next I will ___` is a forward next-step;
`What I said, and what it changed` is the **Influence-naming** line — the one
the reflection window's completeness rule is about. **Decision: A1 ADDS the
ratified line alongside the existing one and removes nothing.** Deleting
`Next I will ___` would be a RED (weakening a closure surface) and would also
strip the existing "no signature/initial" framing. The pass therefore ends
with GROW carrying both, which is the correct ratified state, not a duplication.

### AMBER-V10 — the absolute reading levels do not reproduce

My selector (stated in full in `fk.py`: `<p>`/`<li>`/`.task-box` prose only;
headings, SVG, script/style, buttons, options, textareas, attributes, all-caps
and sub-5-word fragments all excluded) yields live **7.38** / pack **4.85**.
The brief cites live ≈8.52 / pack ≈7.11. Neither figure is wrong *as such* —
they are different instruments — but **no selector was stated for the brief's
numbers**, and this programme's standing rule is that an unselectored reading
figure is not evidence. I report mine, with the selector, and flag the gap.
**The direction — the first downward pack — is confirmed on both instruments.**

---

## 3 · The unsourced-gate finding (register entry)

The pack ships `GROW_SCIENCE_V3PLUS_READING_AGE_REPORT.md` asserting a
**"7.0–11.0 years" release gate**. No GROW reading band has ever been supplied
to this programme; the band sits with the SENCo and is **still pending**.

**A release gate measured against a band nobody supplied is not a pass.**
This pass therefore:

- reports reading as **before/after deltas with the selector stated**;
- attaches **no verdict**, no pass/fail, no "meets/does not meet";
- **never estimates a reading age** and never attaches a level to a pupil;
- records the trigger: **when Matt supplies the GROW band, it becomes the
  standing target for GROW and this pass's deltas become its baseline.**

The pack's own direction of travel is good and is being taken. Its *verdict*
is refused. Direction recorded; verdict refused.

---

## 4 · Pathway split — held, not inferred

Ratified and not to be crossed, restated here because this is the pass where
crossing them would be easiest:

- **GROW closes with the pupil-written line. The adult is audience, not
  signatory. No adult initial.**
- **BUILD closes with the adult Audience/modality strip and carries no
  pupil-written line.**

BUILD is post-BSG-1 and settled. This pass touches **no** BUILD file, adds
**no** modality strip to GROW, and infers **no** band across pathways.

---

## 5 · Decisions log (appended as the pass runs)

*(entries below are added at the time of each decision — see §6 refusals and
the per-phase entries that follow)*
