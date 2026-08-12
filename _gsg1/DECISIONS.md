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

---

## 6 · Phase B · the refusal set — considered and DECLINED

| Declined | Reason |
|---|---|
| **The pack's ten files as installed lessons** | Graft, don't replace. The four deletions ride in the vehicle: witness statement, Oak links, print-pack depth, tier scaffolding. Every gain the pack carries is now on the live chassis without them. |
| **The external-asset (zip) build** | Single-file rule; offline staff packs. Only the loose inlined build was quarried, and only for wording and mechanism. |
| **Deletion of witness / Oak links / print depth / tier depth** | Assessment record (ELC 8939 + UAS banking); links verified at install incl. the two kept-and-flagged; the tiered print pack is what TAs actually teach from; the tiers ARE the school's "scaffolded, adapted/TA-supported". All verified intact or richer at the tip. |
| **The invented 7.0–11.0 reading gate** | No GROW band exists; it is with the SENCo. Deltas only. See §3. |
| **The pack's replacement reflection window** | A8 keeps the live 5.8 KB artefact and ports one line. The pack's 26 KB replacement is not installed. |
| **The marked-correct commit device** (`"correct": 0` in the pack's JSON) | Ported judgement-free per A5: the starter receives a prediction and does not mark it. The reveal happens through the teaching. |
| **Its single `#printSheet` as the print story** | Not installed. It could only ever land as ONE additional section beside the full pack, never instead of it; the full pack is intact. |
| **The pack's seven-rung prompt ladder** (`WAIT / SELF-PROMPT / VISUAL CUE / GENERAL VERBAL / SPECIFIC VERBAL / MODEL / DIRECT SUPPORT`) | **RED.** A seventh wording of the WT-DS least-prompt ladder. Six exist; queue-16 owns reconciliation. Found on the pack's W4A We Do while quarrying for A6 and deliberately left behind. |
| **Copy-pasting any pack markup** | The pack carries 20 bare `matchMedia` against an estate standard of zero (AMBER-INPUT-1). Every graft is hand-written. |
| **Sourcing the Progress Schools lockup** | Human-only. The `--mirror` build hard-stops without it; reported, not worked around. |

---

## 7 · What was grafted, by school stage

| Stage | What landed | Where |
|---|---|---|
| **Arrival** | Rebuilt to **3 retrieval + 1 lead-in**, at all three tiers (12 questions/file). R1 last lesson · R2 previous week · R3 older · L lead-in. Every question carries a non-reading route AND a named tier step. Thin-history substitutions **declared on the slide**. | A2 · 10/10 screen + print |
| **Starter** | Judgement-free predict-commit. No correct answer, no tick, nothing counted. | A5 · 10/10 |
| **I Do** | "What this model helps us see / does not show" pair. | A4 · 10/10 screen + print |
| **We Do** | **One specimen only** — W4A Mechanism Hunt, added beside the live lever explorer. | A6 · 1/10, then STOP |
| **Independent** | WORD HELP bridges: formal term dominant, bridge hidden until requested, TA fade route stated. | A4 · 10/10 screen + print |
| **Exit** | The ratified GROW written closure line, **added beside** the existing `Next I will ___`. | A1 · 10/10 screen + print |
| *(all pupil surfaces)* | Pupil-activated speech synthesis: feature-detected, silently removed where unsupported, never automatic. | A4 · Arrival / Independent / Exit |

**A2 arrival summary.** The retrieval chain runs W3A(none behind it) → W3B(W3A only) → W4A(W3B, W3A, +declared second W3) → W4B → W5A → W5B → W6A → W6B → W7A → W7B, each R1/R2/R3 reaching only into lessons this suite has actually taught. The W3 pair and W4A's R3 declare their substitutions in a visible box on the slide. **W1–W2 are never named as a topic and the Baseline_Weeks pack is never linked** — `Aut1·W2` remains 0 across the ten and `Baseline_Weeks` remains 0. The entry line for a pupil who was not there was **verified at 10/10 before any edit**, not assumed (see AMBER-INSTR-1 #16).

---

## 8 · Reading — deltas, no verdict

Selector A, pupil-facing stage prose, stated in full in `_gsg1/reading/fk.py` and applied identically to baseline, working tree and pack. **Unit: Flesch–Kincaid Grade. Universe: the ten lessons' pupil-facing stage prose.**

| file | base | now | delta | pack |
|---|---|---|---|---|
| W3A_Friction_Explore | 4.73 | 2.92 | **-1.81** | 3.74 |
| W3B_Friction_Do | 6.2 | 3.31 | **-2.89** | 4.05 |
| W4A_Mechanisms_Explore | 5.77 | 3.43 | **-2.34** | 4.35 |
| W4B_Mechanisms_Do | 5.98 | 3.68 | **-2.30** | 4.26 |
| W5A_Fair_Test_Explore | 5.7 | 3.46 | **-2.24** | 3.84 |
| W5B_Fair_Test_Do | 5.05 | 3.58 | **-1.47** | 4.93 |
| W6A_Earth_And_Planets_Explore | 4.72 | 3.09 | **-1.63** | 3.96 |
| W6B_Earth_And_Planets_Do | 5.96 | 3.63 | **-2.33** | 5.3 |
| W7A_The_Moon_Explore | 5.59 | 3.48 | **-2.11** | 4.12 |
| W7B_The_Moon_Do | 4.9 | 3.33 | **-1.57** | 4.11 |
| **mean** | **5.46** | **3.39** | **-2.07** | **4.27** |

Lower in **10/10** files and on **every** measured surface (arrival, starter, I Do, independent, exit — per-surface table in `_gsg1/reading/fk_table.json`).

**No verdict is attached to any of these numbers.** No GROW reading band has been supplied to this programme. **Nothing here is a pass or a fail, no reading age is estimated, and no level is attached to any pupil.**

**Standing trigger, recorded:** when Matt supplies the GROW band, it becomes the standing target for GROW and this table's "now" column becomes its baseline.

---

## 9 · AMBERs, every one by name

| # | AMBER | Where recorded |
|---|---|---|
| AMBER-INPUT-1 | The pack carries **20 bare `matchMedia`** (2/file × 10) against an estate standard of zero. Consequence: nothing is copy-pasted; every graft is hand-written. | §1, at input inspection |
| AMBER-V4 | **Word bank is 2 files, not 2 per file** — measured `[4,0,0,0,2,0,0,0,0,0]`. The brief's "×2/file" does not reproduce. Estate wins. Gate 7 pinned to the measured vector; no word bank reduced. | §2, at verification |
| AMBER-V6 | Live GROW is **not closure-less**: it already carries a pupil-written `Next I will ___` line with "no signature/initial". The missing instrument is specifically the Influence-naming line. A1 therefore **adds beside** rather than replacing — removing either would be RED. | §2, at verification |
| AMBER-V10 | **Absolute reading levels do not reproduce.** The brief cites live ≈8.52 / pack ≈7.11; no selector was stated for those figures. Under a stated selector the direction confirms and the levels differ. Reported as measured, with the selector. | §2, at verification |
| AMBER-INSTR-1 | **Instrument failures #15 and #16, both mine, caught inside the pass**: wrong universe on the sentinels (82/138 vs 50/113), and wrong unit on `printTier` and on the entry line (a 1/10 that was really 10/10). | §2 |
| AMBER-INSTR-2 | **Instrument failures #17 and #18, both mine**: gate 5 asserted `ido2`/`wedo2` data-types the estate has never used, failing 10/10 correct files; and compared a section-scoped scan against a bare-attribute scan, reporting a false baseline difference 10/10. Both fixed in the gate, not in the files. | §10 below |
| AMBER-INSTR-3 | **Instrument failure #19, mine**: the FK extractor concatenated adjacent blocks into artificial 40-word sentences (spurious FK 22.3), and did not exclude the provenance footer its own docstring claimed to exclude — a `<p class="source-note">` build string with a repo path and a SHA scored as the hardest "pupil" sentence in the suite. Both corrected; the block-boundary rule is now explicit. | §10 below |
| AMBER-A3-SELF | **The heaviest pupil-facing sentence in the suite after Phase A was one I had just written** (38 words, FK 14.14, on all ten files). Held to the same standard as the live prose and rewritten. A pass that only audits other people's prose is not auditing. | A3 |
| AMBER-A3-VOCAB | The A2 arrival rebuild **displaced four protected terms** (`variable` W5B, `evidence` W6A, `gravity` W6B, `Solar System` W7A). The gate caught them. Fixed by putting the terms back into the questions — **not** by relaxing the gate. | A3 |
| AMBER-A6-CONTRAST | The specimen's buttons rendered **white-on-white** — the chassis carries a bare `button{color:#fff}` rule and the specimen set a white background without restating colour. Caught by rendering, not by a static gate. Fixed and re-rendered. | A6 |
| AMBER-A7-MATRIX | The pack's equipment matrix carries **three degenerate columns** (Preparation, Reusable/consumable, Setup time — identical in all ten rows) and a Digital-alternative column naming **ten labs that are not installed**. Same class of defect BSG-1 found in the BUILD matrix, and worse. All four columns re-derived per lesson. | A7 |
| AMBER-CRAWL | The staff-pack crawl reports **5 missing internal targets** (`Baseline_Weeks/index.html` ×3 and two `_sciv3` policy docs). **Pre-existing at the rollback SHA** — verified, not introduced here. Baseline lives on PythonAnywhere by design. | A7 |
| AMBER-LOCKUP | `build_staff_pack.py --mirror` **hard-stops** for want of the real Progress Schools lockup. Expected, reported, **not worked around** — the binary is human-only and was not sourced. The non-mirror pack builds clean: 340 files, all REBRAND checks pass. | A7 |

---

## 10 · Register entries

**1 · The declared-sentinel-movement form.** A pass that must move a sentinel **declares the exact delta and the file list in advance**; afterwards, "unchanged" and "moved exactly as declared" are both green and everything else is red. GSG-1 is the first pass to use it. Declared: `ll-g:loop-mark` stays 50; written-closure sentinel 113 → 123, delta = exactly the ten GROW v3_40min lessons. **Derived at emit time: 50 and 123, +10, all ten inside `Science_Teesside/Grow/v3_40min/`.** Universe on both: git-tracked `*.html`.

**2 · The unsourced-gate finding.** *A release gate measured against a band nobody supplied is not a pass.* The pack's "7.0–11.0 years" gate was invented. The correct response is to **take the direction and refuse the verdict**: report deltas with a stated selector, attach no pass/fail, estimate no reading age, and record the trigger for when the real band arrives. Direction taken (10/10 lower). Verdict refused.

**3 · The second confirmed two-build delivery.** Checksummed zips carried the ~30 KB external-asset build plus an `assets/` folder; the loose files carried the ~87 KB inlined build. Only the inlined build is usable. **Second confirmed instance** — this is now a pattern, and the discriminator (`href="assets/` count, and file size) should be run on every future delivery before anything is quarried. Note also that **the ten quarried files carried no checksum at all**; the sums covered only the four zips/diff.

**4 · Matt's stated school grammar, and the still-open SENCo band.** Recorded as his words and his pending decision: the six stages (Arrival with 3 retrieval + 1 lead-in · Starter assuming no prior knowledge · I Do · We Do · Independent scaffolded and TA-supported · Exit ticket) are the standing shape and are now carried 10/10. **The GROW reading band is with the SENCo and is still open.** Until it arrives GROW reading is reported as deltas. When it arrives it becomes the standing target.

**5 · Hold your own prose to the gate.** Two of this pass's AMBERs (A3-SELF, A3-VOCAB) are defects the pass introduced and then caught in its own gates. A gate that only ever fires on inherited content is not calibrated.

---

## 11 · Pathway split at the tip — verified, not assumed

- GROW closes with the pupil-written line, adult as audience: **10/10**, with "No adult initial is required" **10/10**.
- **Zero** BUILD modality strips on any GROW file.
- **Zero** BUILD files touched by this pass.
- The pre-existing GROW `Next I will ___` line survives **10/10** — GROW now carries both instruments, which is the correct ratified state.

## 12 · Rollback

`git reset --hard dcc23dc2485516eb5d50409494c7d70f56c62f78` restores the pre-pass estate exactly. Nothing outside `Science_Teesside/Grow/v3_40min/` and `_gsg1/` was modified.

---

## 13 · SIGN-OFF · A6 specimen approved

**Matt, 2026-08-12, verbatim: "This is great."**

His written sign-off on the W4A Mechanism Hunt specimen, and with it the
delegated authority to complete the job: build the remaining labs, run the full
battery, and merge if and only if every gate is green.

Recorded as his words. The A6 stop is lifted.

---

## 14 · Sentinel readback, committed to the repo

Delivered in chat at tip `79e17c4` and accepted as the missing report section.
Committed here so it exists in the repository, not only in a transcript.

**Unit: bearing files. Universe: git-tracked `*.html`.**

| sentinel | 574035bf | dcc23dc | 79e17c4 | movement |
|---|---|---|---|---|
| `ll-g:loop-mark` | 50 | 50 | **50** | none — **file-for-file identical** across all three |
| written-closure line | 113 | 113 | **123** | **+10, purely additive** |

The +10 is exactly the ten `Science_Teesside/Grow/v3_40min/SCI_G_*.html` lessons.
The 113 bearing files at `dcc23dc` are all still bearing at `79e17c4`: the set
grew, nothing left it. **0 BUILD files appear in the 123-set** — correct, because
BUILD closes through adult Audience and carries no pupil-written line.

This is the declared-sentinel-movement form closing green: the movement was
declared in advance, and what moved is exactly what was declared.

**From this point the declared movement has happened. Both sentinels now hold
still at 50 / 123, and any further change to either is a defect, not a delta.**

---

## 15 · We Do labs · eight built, one deliberately not

Close order §2. Each lesson was asked the W4A question — *does the live We Do
interaction already cover this lesson's own LO, and if so does an added lab give
something it lacks?* — and the answer was derived from the live widget's markup
against the lesson's stated LO, not assumed.

| # | lesson | lab | the gap it fills |
|---|---|---|---|
| 1 | W3A | Grip Decision Lab | Surface explorer shows one surface at a time and holds nothing; no prediction; never touches the helpful/unhelpful judgement that is half the LO |
| 2 | W3B | Surface Evidence Lab | Results interpreter is reachable **only by typing three numbers** — no button route exists — and asks for no prediction before the data |
| 3 | W4A | Mechanism Hunt *(the signed-off specimen)* | Lever pivot explorer covers levers only; the lesson covers levers, pulleys **and** gears |
| 4 | W4B | Pivot Evidence Lab | Slider shows one pivot position at a time and holds nothing; the LO is about using **evidence** from several positions |
| 5 | W5A | Measure and Unit Lab | Repair the method covers only the CHANGE arm; the LO names change, measure **and** keep the same, and the unit is never asked for |
| 6 | W5B | Trust the Repeat Lab | Repeat-and-mean lab is reachable **only by typing nine numbers**, and computes means without ever asking pupils to judge which repeats to trust |
| 7 | W6A | Gravity and Motion Lab | Planet order challenge covers order thoroughly; the LO also says "explain gravity's role" and gravity is absent from the widget |
| 8 | W6B | Honest Model Lab | Orbit viewer shows positions; the LO is a model "accurate for its purpose", and the scale trade-off is not in the widget |
| 9 | W7B | Phase or Eclipse Lab | Phase explorer is byte-identical to W7A's and covers phases only; the LO adds "distinguish phases from eclipses" and the word never appears |

### AMBER-W7A-UNBUILT — the one lab deliberately not built

**W7A ships no added lab, and this is the finding, not an omission.**

W7A's LO is *"I can explain why the Moon appears to change shape as it orbits
Earth."* Its live Phase explorer offers four phase buttons, connects Moon
position, sunlight direction and the view from Earth, and states in its own text
that the effect is viewing geometry and **not** Earth's shadow. It is already
button-only, already carries no score, and already answers the LO directly and
completely. A second lab there would be a duplicate wearing a new border.

The evidence that made this decision non-obvious is worth recording: **W7A's and
W7B's widgets are byte-identical apart from the id suffix** (920 bytes each,
verified). Identical widgets, different verdicts — because the two lessons have
different LOs. W7B's demands the phase/eclipse distinction that neither copy of
the widget mentions; W7A's does not. *The same widget can be sufficient in one
lesson and insufficient in the next, and only the LO decides which.*

**Nine minus one honest labs beat nine duplicates.** If W7A's LO is ever widened
— to eclipses, to the orbital tilt, to anything the phase explorer does not
carry — this decision should be revisited, and the W7B lab is the pattern to
follow.

### Lab invariants, asserted in the installer before any file is written

`_gsg1/tools/lab.py` refuses to write a file unless the print pack is
byte-identical, the witness block is byte-identical, the three tier counts are
unchanged, and `matchMedia` is absent. Every transplant then re-verified by
`_gsg1/tools/verify_lab.py` and driven end-to-end in real Chromium, with
**contrast probed by computed style at render time** — the A6-CONTRAST lesson,
where a white-on-white button passed every static gate and was caught only by
looking at the page.
