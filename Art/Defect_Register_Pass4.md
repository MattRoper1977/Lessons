# Art Teesside — defect register, re-derived from origin

**Base:** `3b805af` (origin/main, 2026-07-26 09:39:04 +0000) · **Estate:** 53 HTML files under `Art_Teesside/`
**Status:** read-only. Nothing committed, edited or staged. **NOT PUSHED — no push credential in this session.**

Built by re-deriving each named item from the files, not from the record. Three verdicts are used:

- **SATISFIED** — the defect is not present at origin. The pass has nothing to do.
- **REAL / DERIVABLE** — the defect is present and its fix can be reconstructed from the files.
- **REAL / NOT DERIVABLE** — the defect is present but the fix was *authored* in the lost sandbox and cannot be recovered from origin. Content required from Matt, or fresh authorship authorised.

---

## 1. The ten "lost, mechanical, fully specified" items

| # | Item | Verdict | Evidence at origin |
|---|---|---|---|
| 1 | Grade purge | **SATISFIED** | Every `AO1–AO4`, `grade band`, `GCSE` hit is inside a *disavowal*: "Never map a sheet to AO1–AO4 and never use GCSE grade bands" and "No GCSE assessment objectives, and no GCSE grade bands." 4 files. All 33 `grade` hits are `upgrade` / `graded wash` — false positives of the old kind. Tier vocabulary is clean: supported 490 / standard 509 / stretch 515, zero foundation-middle-higher as tier names. |
| 2 | Hours-gate substitution wording | **SATISFIED (as the two declared residuals)** | "**There is no minimum-hours gate** — Trinity states time figures are guidance" ×2, plus "**No hours threshold, ever.**" These are the two no-gate residuals already on the declared list. One item needs a ruling, not a rewrite — see §3.1. |
| 3 | The two orphan lessons | **REAL / DERIVABLE** | `Build/BUILD_ART_A2_W3_Stencil_Lab.html` and `Build/BUILD_ART_A2_W4_Audience_Week.html` — **zero inbound references anywhere in the repo.** Both created by `2106b3f` and never linked into any START_HERE, scheme of work, pack or catalogue. See §3.2 — this is not a housekeeping item. |
| 4 | The seven Autumn 2 headers | **REAL / DERIVABLE (probable)** | Seven files confirmed: `BUILD_ART_A2_W1…W7`. `<title>` bands are consistent (`BUILD Art A2 W1 · Surface Hunt`). In-page `<h1>` carries the short name only, matching the non-A2 BUILD lessons — so the two are already consistent with each other. **The specific header defect is not visible to me.** Needs one line from Matt saying what was wrong. |
| 5 | ~~GROW Part B~~ | **WITHDRAWN — FALSE FINDING** | Not deleted, per the rule that a silently removed false finding is indistinguishable from a fixed one. The evidence above is a token count in files that *correctly* lack the token: every GROW lesson carries exactly one Bronze Part, and **W4 is Part B**. Part B coverage is complete — pack 3 mentions, W8 audit 6, START_HERE 1, audit stations run A→B→C→D. The real defect nearby was that `Grow/Scheme_of_Work.html` declared no Part shape at all (22 / 14 / 23 / **0** across the four schemes). R3 was re-specified to that and landed at `d805706`. |
| 6 | `.ladder` rule | **REAL / NOT DERIVABLE** | `ladder` appears in Art Teesside **only as prose** ("a BUILD→GROW ladder", "a pressure ladder"). There is no `.ladder` CSS class in use and no rule defining one. Its declarations cannot be re-derived — they never existed in these files. |
| 7 | Silver 1B observer block + locator row | **REAL / NOT DERIVABLE** | Unit 1B material is live across 4 LAUNCH files (1B log, 1B cycle, 1B Log Anatomy, full 1B Log print block). No observer block and no locator row. The *slot* is derivable; the *wording* is not. |
| 8 | The 1B portfolio row | **REAL / NOT DERIVABLE** | Same as 7. |
| 9 | `min-height: 277mm` | **REAL / DERIVABLE** | Absent estate-wide. Fully specified — one declaration, measurement already taken (55 pages / 55 sheets, zero reflow). The only fully recoverable one of the CSS items. |
| 10 | `.a4.dense` | **REAL / NOT DERIVABLE** | Absent estate-wide. The *name* and its role ("belt to braces") are known; the declarations are not. |

**Four of ten need content that origin cannot supply.** The phrase "mechanical and fully specified" holds for items 9 and, with one clarification each, 3, 4 and 5. Items 6, 7, 8 and 10 are authored artefacts whose text died with the sandbox.

---

## 2. Pass-to-item mapping is not recoverable

The stated order — `G1 → G2 → G3 → G4 → A3 → A1 → A4 → A4b → min-height → dense → A2a` — has eleven slots for ten items, and `A3` precedes `A1`, which means the letters are workstream labels, not sequence. **I will not guess the mapping.** Either supply it, or authorise me to re-plan the passes from this register, in which case the two SATISFIED items collapse out and the order is driven by dependency rather than by the lost numbering.

---

## 3. Findings that outrank most of the rebuild

### 3.1 D-PRESS-01 — the estate teaches a press the estate says it does not have. **HIGH.**

Live at origin today, independent of A2a.

| File | Live strings | |
|---|---|---|
| `Grow/GROW_ART_W2` | 21 | teaches the press |
| `Launch/LAUNCH_ART_W6` | 6 | teaches the press |
| `Grow/GROW_ART_W3` | 4 | teaches the press |
| `Grow/GROW_ART_W6` | 3 | teaches the press |
| `Build/Autumn2_Scheme_of_Work` | 5 | **denies** the press |
| `Build/START_HERE` | 1 | **denies** the press |

`START_HERE` is the first file anyone opens. A teacher stocking to the scheme of work will not have the kit the lesson requires.

**`LAUNCH_ART_W6_Pilot_Lead_and_Adapt` is contaminated and is outside A2b's scope.** "The inking queue jams: I don't take over the roller"; "Week 7 gets a second inking slab." A2b covers GROW W3, W6, W7. Completing A2a and A2b as planned still leaves a LAUNCH lesson teaching a press — in the lesson where a pupil *leads other pupils*, so the error acquires a second cohort.

### 3.2 D-ORPHAN-01 — the source of truth for the stencil route is unreachable. **HIGH.**

`BUILD_ART_A2_W3_Stencil_Lab.html` has zero inbound references. It is also the file the whole A2a derivation is drawn from, and the only place in the estate that teaches sponge loading, bridges and islands. A teacher cannot navigate to the lesson that defines the route the scheme of work insists on. `BUILD_ART_A2_W4_Audience_Week.html` is orphaned with it.

This reframes item 3 from housekeeping to a prerequisite: linking Stencil Lab is what makes the A2a rebuild *findable* rather than merely correct.

### 3.3 D-PRESS-02 — the corrected BUILD Autumn 2 route is itself incomplete. **MEDIUM.**

The folder that denies the press still carries, across `BUILD_ART_A2_W1…W7`: `edition` ×20, `pull an edition` ×5, `pulled` ×5, `plate` ×5. Including a lesson *title*: "Resolve and **Pull an Edition of Five**", and the answer line "hand-**pulled** editions vary".

An edition of five is achievable by stencil — re-register, reload, re-dab. So this is re-physicsing, not deletion. But it means `2106b3f` did not finish inside its own folder, and A2a's sibling-derivation is drawing on a file that is 90% converted, not 100%. Worth a ruling before A2a is rebuilt on top of it.

---

## 4. Method and its limits — declared, per the LL instrument register

- **Press sweep.** Literal string match over a declared term list (`press corner, inking bench, inking queue, inking slab, printing ink, ink load, relief print, roller, brayer, lino, pre-cut plate, the plate, plate wear, re-inked`). It under-reports paraphrase ("the pull is a ceremony", "place once, press once") and it missed `pull` / `edition` / `plate` on the first pass — §3.3 exists because the second pass widened the list. **34 is a floor, not a total.**
- **Orphan check.** Literal filename-substring match across repo `*.html` and `*.json`, excluding self-reference. Zero inbound is strong evidence of orphanhood; non-zero inbound is weak evidence of reachability, because a bare mention scores as a link and links built by JS concatenation are invisible to it.
- **Grade sweep.** Literal. Its whole result is that every hit is a disavowal, which is a claim about meaning, not presence — so that verdict is **Interpretive** and was read by eye across all hits, not inferred from counts.
- **`LundyLoop/tools/print_pack_audit.py` v1 is QUARANTINED** and was not used. Its 691 estate-wide absent print slots are retired figures: it hardcoded `foundation/middle/higher`, and Art Teesside is `supported/standard/stretch`. Any later render validation of `min-height: 277mm` must use v2 or an independent method.
