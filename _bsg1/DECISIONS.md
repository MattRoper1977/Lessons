# BSG-1 v2 — Decisions record

Pass: `bsg-1-v2-2026-08-11` · Branch: `claude/bsg-1-science-graft-2yvo26`
Written at the time, per §1 AMBER rule.

## Base and rollback

- **Base**: current `origin/main` = `574035bf6c3ee640cf8b5b3f9b10de341497831e`
  (Merge PR #92, 2026-08-11 18:45 +0100).
- **Rollback SHA**: `574035bf6c3ee640cf8b5b3f9b10de341497831e` — to abandon this
  pass, delete the branch; `main` is untouched throughout (nothing merges; Matt
  merges).
- **Finding — main has not moved.** §0.2 warns against adopting the pack's build
  base `574035bf…`; at the time of this pass `origin/main` *is* `574035bf…`.
  The two coincide because no commit has landed on main since the pack was
  built, not because the pack's base was adopted. If main moves mid-pass, HEAD
  wins and this entry gets a follow-up.
- Branch note: the master prompt names `claude/bsg-1-science-graft`; the session's
  designated branch is `claude/bsg-1-science-graft-2yvo26`. The designated branch
  is used (system instruction outranks the prompt's spelling; same work, same
  review path).

## Identity gate — 5/5 CONFIRMED

1. `origin` → `MattRoper1977/Lessons` ✓
2. `Science_Teesside/Build/v3_40min/`: ten `SCI_B_W{3..7}{A,B}_*.html` +
   `index.html` + `manifest-v3.json` + reflection window + teacher guide ✓
3. `Science_Teesside/Build/SCI_B_W3_Backbones.html` 261,653 B ✓
4. `LundyLoop/5_staff_training/Reading_the_Response_Card.html` ✓
5. `651a88e` and `2ce19ce` both ancestors of `origin/main` ✓ (repo arrived as a
   shallow clone; `git fetch --unshallow` was required before `2ce19ce`
   resolved — a shallow clone is another way an identity gate can lie).

## Input provenance

Received both deliveries as uploads:

- **v1** = `Compress_11_08_2026_110816.rar` (RAR v5 wrapping a zip). Contents:
  ten `SCI_B_*.html` v1 lesson files, `BUILD_DAILY_REFLECTION_EVIDENCE_WINDOW.html`,
  `TEACHER_IMPLEMENTATION_GUIDE.html`, `index-7.html`, `index-8.html`, nested
  COMPLETE_PREVIEW / CHANGED_FILES_ONLY / REVIEW_PACK zips, PATCH.diff,
  manifest, sums, three contact-sheet PNGs. **All four shipped SHA-256 sums
  verify OK.** Used as documentation source only; no v1 lesson file installs.
- **v2** = `Compress_11_08_2026_113728.zip`. Contents: ten loose `SCI_B_*-N.html`
  (~60 KB each, **inlined single-file build** — verified zero `href="assets/`
  and zero `src="assets/` across all ten; universe: the ten loose files,
  pattern `href="assets/|src="assets/`), nested COMPLETE_PREVIEW /
  CHANGED_FILES_ONLY / REVIEW_PACK zips, PATCH-1.diff ≡ PATCH-2.diff
  (byte-identical, confirmed), DOWNLOAD_SHA256SUMS.txt ≡ -1.txt (identical,
  confirmed). **All four shipped sums verify OK — and they checksum the
  external-asset build**: CHANGED_FILES_ONLY carries ~21 KB lessons +
  `assets/science-v3plus.css|js`. Two-build hazard confirmed exactly as
  documented.
- **Absent from the v2 delivery** (present in v1): the standalone
  `BUILD_DAILY_REFLECTION_EVIDENCE_WINDOW.html`, `TEACHER_IMPLEMENTATION_GUIDE.html`
  and index files as loose items (v2 ships them only inside the nested zips, in
  external-asset form), the `BEFORE_AFTER_SIDE_BY_SIDE.png`,
  `INFLUENCE_CONTACT_SHEET.png`, `PRACTICALS_CONTACT_SHEET.png` loose PNGs, and
  a loose `DOWNLOAD_MANIFEST.json`. Nothing needed for this pass is missing:
  lesson content comes from the loose inlined build; matrices come from the
  review packs.
- Both packs' `BASE_MAIN_SHA.txt` = `574035bf…` (matches, see base finding).
- **Source ruling**: lesson content sources **only** from
  `scratchpad/v2pack/SCI_B_*-N.html` (loose inlined v2). Review-pack matrices
  (v2 preferred, v1 where richer) are documentation sources. The
  external-asset build and v1 lesson files never source shipped content.

## Decisions log (running)

(entries added at the time, below)

## Phase 0 — §2 verification at HEAD (574035bf)

Instrument notes first, because two scanners failed validation on first cast:
- The V9 scanner's known positive `Aut1·W3` returned 0 — the live dialect is
  `Aut1 W3` (space, not middle dot). Both dialects were then searched.
  **Instrument failure #14 for the register: the sentinel dialect itself
  drifted between the governing doc and the estate.**
- V8's stated counts (21/17/17) are **case-insensitive** string counts; the
  case-sensitive cast gives 15/15/15. Same file, same truth, different unit.

| # | Verdict | Evidence (unit · universe) |
|---|---|---|
| V1 | CONFIRMED | 2 `<div class="pp">` + 1 `class="print-section"` = 3 print-sections; `proute` string ×8 (5 CSS + 3 divs) · per file, ten lesson files · 10/10 |
| V2 | CONFIRMED | `printTier` and `afterprint` present · substring, ten files · 10/10 |
| V3 | CONFIRMED | `print-witness` present · substring, ten files · 10/10 |
| V4 | CONFIRMED | exactly 2 distinct Oak URLs, 4 href occurrences: W3A+W3B → `animals-without-bones`, W4A+W4B → `muscles-for-movement` · href values, ten files |
| V5 | CONFIRMED | route banner, `Baseline_Weeks` link, `POLICY_ALIGNMENT.md` link all present; no `README_LOCAL_PREVIEW` link · substring, `index.html` |
| V6 | CONFIRMED | branches secure×4 / mixed×4 / misconception×2 / access×5 / method×4 (ci substrings); "not a second closure" and "Disclosures leave this workflow" both present · reflection window file |
| V7 | CONFIRMED | all six school stages typed via `data-type` (plus `title`, and doubled `ido`/`wedo`) · attribute values, ten files · 10/10; first six hits per file are CSS selectors, not slides — unit noted |
| V8 | CONFIRMED (unit clarified) | W3A ci: Supported 21 / Standard 17 / Stretch 17 / scaffold 12 — matches doc under case-insensitive counting; case-sensitive is 15/15/15/12. All ten files identical. Pre-pass tier baseline recorded per file for gate 7. |
| V9 | CONFIRMED | `Aut1·W2` = 0 and `Aut1 W2` = 0 (also W1 forms = 0) · exact substrings, ten files; scanner validated on `Aut1 W3` = 1 in W3A |
| V10 | CONFIRMED with finding | every calorie/weight/good-bad hit is a prohibition; BUT 2 of 14 `diet` hits are **uses**, both animal-species contexts: W5B "food that fits its natural diet" (rescue-centre animal), W7A "not as universal diet rules". Not personal-diet talk, not prohibitions either. **The estate wins; the doc's "zero uses" is imprecise. These two pre-date this pass and are left untouched.** `font-weight` excluded by construction (`(?<!font-)weight`). |
| V11 | CONFIRMED (ordering); absolutes re-derived | Selector: visible text of `p`+`li`, screen = outside print container, print = inside `.printpack`/`#printSheet`, style/script excluded, headings excluded by construction. Means: live screen **7.10** · live print **6.30** · v3+ v2 screen **9.27** · v5 W3 original **5.57**. Doc's 8.9/6.2/10.6/5.1 reproduce in ordering and print-pack absolute; screen absolutes differ because the doc's selector included more than p/li. This pass's before/after comparisons all use THIS instrument. |
| V12 | CONFIRMED | `ll-g:loop-mark v1` = 50 bearing files (git grep, `*.html`); written-closure marker "What I said, and what it changed" = 113 in `*.html` (137 all types) · git-tracked tree. Zero of either in BUILD v3_40min — correct; BUILD closes through adult Audience. Rule: same sets before and after this pass. |

Baseline for gate 7 (tier integrity), unit = case-insensitive substring per file:
every live lesson: supported 21 · standard 17 · stretch 17 · scaffold 12.

### A1 — Practicals & Equipment Matrix (GREEN, logged)

- Created `Science_Teesside/Build/v3_40min/BUILD_SCIENCE_PRACTICALS_MATRIX.html`
  (Made by Matt) and `..._PROGRESS_SCHOOLS.html` (rebranded per REBRAND.md:
  strip, `x-brand` meta, exact `>by madebymatt.uk<` credit, residue sweep run
  with zero remaining MBM forms) in the same commit. Linked from `index.html`
  beside the Teacher Guide.
- **Source defect corrected**: the pack's EQUIPMENT_MATRIX Preparation column
  repeats "W4 pre-punch/secure joint" in all ten rows — a template fault.
  Preparation re-derived per lesson from each row's own equipment. AMBER by
  name: preparation text for W3A/W3B/W5A/W5B/W6A/W6B/W7A/W7B is authored, not
  pack-sourced.
- **Digital alternative column**: the pack names its own labs; the estate's
  real digital alternatives are the live We Do 2 widgets, so the column names
  those instead. (If the A6 specimen ships, W4A's row stays true either way.)
- **AMBER — Progress Schools lockup**: the real logo binary is deliberately
  out of git (SHA in REBRAND.md). The PS variant ships with the strip and text
  branding only; the lockup must be added from Matt's recorded asset before
  the file leaves the estate. No placeholder logo was drawn (REBRAND rule 1).
- No CLEAPSS approval claimed; local proportionate RA stated; adult does all
  cutting/piercing; W5–W7 printed fictional resources only.

### §3.1 — Arrival rebuild (GREEN, logged) + two AMBERs

- All ten arrivals rebuilt to **3 retrieval + 1 lead-in**, delivered inside the
  existing Supported/Standard/Stretch tier machinery — all four questions
  appear in each panel at that tier's demand, so every question has a tier
  route AND the participation block's point/say/demonstrate modalities.
- R1 keeps each lesson's existing previous-lesson question as its basis; R2/R3
  derive from the taught lessons' own LO/KO text; nothing invented.
- **W3A**: all four are prior-knowledge elicitation (baseline weeks taught no
  science); no baseline topic named, no baseline resource linked.
- **W3B**: R1 retrieves W3A (real); questions 2–3 are elicitation, declared in
  the slide note.
- **W4A/W4B**: no clean R3 exists (one prior taught week) — question 3
  retrieves week 3 a second time, declared in the slide note.
- Print packs gain a compact "three retrievals and a lead-in (Supported
  forms)" line under the existing retrieval line; nothing removed.
- New arrival text FK (selector: question text in arrival panels): W3A 2.3,
  W3B 5.0, W4A 3.1, W4B 3.5, W5A 3.3, W5B 3.7, W6A 3.0, W6B 2.3, W7A 1.9,
  W7B 2.1. Nine of ten inside FK 1.0–4.0. **AMBER — W3B arrival at FK 5.0**:
  the Stretch route carries "vertebrates"/"invertebrates" (protected terms,
  4–5 syllables each); the sentence frames are minimal, so this is the honest
  floor for that content. Left as written rather than stripping the science.
- **AMBER — entry-line wording**: §3.1/gate 6 say the "New to this class, or
  not sure?" line exists on every arrival; at HEAD the exact wording existed
  only in W3A (1/10) — the other nine said "Not here last lesson?". All ten
  standardised to the gate's wording (superset meaning: covers newness,
  absence and uncertainty). The doc's premise was wrong; logged, not hidden.
- **Correction to the V8 note above**: "all ten files identical at 21/17/17"
  was wrong — that was W3A alone; the other nine baselined at ci 18/17/17.
  Gate 7 is measured per file against each file's own pre-pass counts; after
  the rebuild every count is ≥ its own baseline (18→19/20, 21→22).
- Headless Chromium boot: 10/10, zero page errors, tier toggle live.

### §3.2 + §3.3 + A4 — starter commit, model limits, WORD HELP (GREEN, logged)

- **Starter commit device** grafted into all ten starters after the puzzle box,
  additive to the frame sequence. Deliberately **judgement-free** — the pack's
  version marks a correct answer; a school starter assumes no prior knowledge
  and receives predictions without judgement (the slide's own TA note), so the
  graft commits and echoes, never marks. Hypotheses authored per live puzzle
  (the pack's commit options fit the pack's QUESTION stage, not always the
  live puzzle); W4A and W7B reuse pack option shapes directly.
- **Model help/limit pair** added to every I Do 2 and to every print pack.
  Wording from the pack's own `model_help`/`model_limit` fields, with these
  adjustments: (a) **W6A limit rewritten** — the pack text contains "dietary"
  (food-census hit); replaced with judgement-free wording, zero census delta
  verified old-vs-new with one instrument; (b) carrier sentences lightly
  shortened for band on W4B/W5A/W5B/W7A/W7B; science content unchanged.
- **A7 WORD HELP**: vocab row (3 terms + hidden bridges) in every I Do 1;
  global "Word help" toggle in the controls nav (`aria-pressed` stated);
  formal term always dominant; TA fade route stated on the slide. Terms and
  bridges from VOCAB_BRIDGE_MATRIX. Adjustments, AMBER by name: **W6A
  "BALANCED DIET" declined** (food rule) — replaced by BALANCE with bridge "a
  range across groups" (authored); "a simplified representation" bridge (W4B/
  W6B MODEL) replaced by "a simple version of the real thing" — a plain-
  language bridge must itself be plain; "substance in food used by the body"
  → "a part of food the body uses"; "obtains" → "gets"; "organisms" →
  "living things".
- **A8 (partial, vocab)**: pupil-triggered 🔊 per term, `speechSynthesis`
  feature-detected, silent degradation, never automatic. Instruction-level
  read-aloud lands with §3.6.
- **A4**: W7B Stretch independent + exit (screen and print, ×2 each) no longer
  ask pupils to *predict* population outcomes; they now say what the chain
  evidence *suggests*, with "A model suggests — it cannot prove."
- No new animation (gate 18 n/a); no colour-only cue (held-state = border +
  background + text change); all new controls labelled.
- Functional boot 10/10: commit device judgement-free (exact feedback string
  asserted), bridges hidden→shown on toggle, model pair present, 3 labelled
  speak buttons, speakTerm safe without the API. Zero page errors.

### §3.6 + §3.8 — exit-side grafts and the evidence sheet (GREEN, logged)

- **Influence rule**: checked `Reading_the_Response_Card.html` first — it
  explains what Influence means but states "it makes no claim about closure",
  so no equivalent completeness line exists there. The line "A lesson counts
  as complete only when Influence names an observable change. 'The adult
  listened' is not Influence." added to the reflection window's INFLUENCE
  stage as guidance text only. One account of the rule, in the one place that
  owns closure guidance for this route.
- **A5**: "Support level records access. It does not define ability." appended
  to the TA overlay's least-prompt card note, once per lesson file — the
  surface where support levels are actually discussed.
- **Declined (§3.6/queue-16): the pack's 8-step prompt dropdown.** It would be
  a seventh WT-DS/least-prompt wording and a recorded field. The live seven-
  rung ladder stands; queue-16 owns any change to it.
- **A8 (instructions)**: "🔊 Read task" on Arrival, Independent and Exit
  (3 per lesson), reading the visible tier's task text; pupil-triggered only,
  feature-detected, buttons hidden when the API is absent, never automatic.
- **§3.8**: the pack's one-page sheet added as a **third** `.pp` print section
  per lesson — retitled "Evidence capture sheet", PUPIL/EVIDENCE ID blank
  kept, boxes: decision / observed / evidence / meaning / changed / Audience /
  "what changed because of my voice" / TA comment, plus "point, say, draw or
  scribe — writing is never required" (BUILD: no written-closure surface).
  The tiered pack and the witness statement stay untouched beside it.
  (First insertion nested it inside the second print section — caught by the
  browser assert `.printpack > .pp == 3`, relocated; evidence, not proxies.)
- Boot: ten lessons + window + index + guide + both matrices, zero errors.

### §5 — reading-band pass (stages logged; one commit per stage)

Instrument (stated once, used throughout): FK on visible text of `p`+`li`;
screen = outside print containers; print = `.printpack` subtree **including**
the assessor witness; style/script excluded; headings and telegraphic
equipment lists excluded from rewriting because FK on fragments is
meaningless (failure #13). Plain-text before/after prose diffs per file in
`_bsg1/reading/`.

- **Stage 1 (print)**: evidence targets rewritten as direct address; audience
  box simplified; model-pair carriers shortened; arrival label compacted.
  Print FK mean 6.24 → 5.39; C1 word deltas −3.5%…+2.1%.
- **Stage 2 (independent)**: screen evidence targets aligned to the print
  rewrites. The live independent task prose was already in band; the pack-era
  "worst offender" figure (9.97/254w) described the pack's EVIDENCE stage,
  not the live slide.
- **Stage 3 (arrival)**: no separate commit — §3.1 wrote it in band from
  birth (FK 1.9–3.7; W3B 5.0 AMBER already logged).
- **Stage 4 (rest of body)**: participation note ("A different communication
  route changes access…") → "You can change how you answer. The Science goal
  stays the same." ×6 per file.
- **Whole-pass table vs origin/main (574035bf)**: screen mean 7.10 → 6.10;
  print mean 6.30 → 5.39. Word counts vs origin/main grew +41–69% — that is
  Phase A's mandated additions (3+1 arrival, model pairs, evidence sheet,
  bridges), not C1 edits; the ±15% honesty guard was applied to each C1 prose
  edit against its own pre-edit surface, all within bounds. No lesson element
  removed.
- **AMBER, by name — every file, both surfaces, remains above FK 4.0**: the
  floor is set by SoW LO statements (verbatim, e.g. "classify unfamiliar
  animals using evidence about their body structure" ≈ FK 14 on 11 words),
  protected vocabulary (vertebrate/invertebrate/classification/nutrient…),
  the assessor witness (assessor-facing, deliberately untouched), and Stretch
  routes serving the top of the band. Chasing FK ≤ 4.0 on these surfaces
  would strip the science; per §5.5 they are left honest and named: W3A–W7B
  screen 5.5–7.0, print 4.7–7.0 (W3B highest at 6.97 print / 6.95 screen).
- **C2 is the arm serving RA 6–8** and is now mechanical, not aspirational:
  every pupil-facing instruction on every changed surface has tier routes,
  the point/say/demonstrate participation block, pupil-triggered read-aloud
  (arrival/independent/exit), WORD HELP bridges, and adult-scribe wording on
  the evidence sheet.
- Decision — the assessor witness statement was excluded from prose editing:
  it is the ASDAN/AQA-facing record surface; changing its wording risks the
  banking route for zero pupil-facing gain.

### §3.4 / A6 — the We Do specimen (built, gated, STOPPED at one)

- Determination: yes — the pack's state-based muscle lab transplants cleanly
  into W4A's We Do 2 as an upgrade of the existing model-arm widget, within
  chassis conventions (inline SVG, single script, button-only controls) and
  without touching the print pack (3 pp sections + witness verified after).
- Ported: prediction-commit before reveal, three discrete positions with a
  direct keyboard/tap position route, TEST disabled until a prediction is
  committed, FREEZE & LOOK, reset, contract/relax state readout. Muscle
  identity is pattern + dash style + text label — never colour alone. No
  drag anywhere. The forearm transition is suppressed globally under
  `prefers-reduced-motion`; every state is carried by the text readout, so
  meaning never rides on the motion (gate 18 classification).
- **The pack's unguarded `matchMedia` call is not guarded — it is absent**:
  it lived in the pack's stage-navigation smooth scroll, which was not
  ported. `matchMedia` occurrences in shipped W4A: 0 (strongest guard).
- Old `arm()` chassis function left in place (shared function set across the
  ten; W4A no longer calls it — harmless, consistent with siblings).
- Gate run on the specimen: zero page errors; predict→test, both directions,
  freeze, reset, rotation and pattern overlay all asserted in-browser;
  rendered screenshot delivered for sign-off.
- **STOP honoured: one specimen only. The other nine We Do labs are not
  built and will not be until Matt signs off in writing.**

## §4 — The refusal set (considered and declined, with reasons)

| Declined | Reason |
|---|---|
| The pack's stage grammar (ARRIVE/QUESTION/MODEL/INVESTIGATE/EVIDENCE/INFLUENCE) as shipped structure, headings or navigation | The school's six-stage grammar is required; §3.0 is law. The pack grammar served only as a quarry; its names appear in no shipped file. |
| The external-asset build (the checksummed zips) | Single-file rule; the offline OneDrive/network staff packs depend on it. Only the loose inlined v2 build sourced content. |
| Replacement of `BUILD_DAILY_REFLECTION_EVIDENCE_WINDOW.html` | Five diagnostic branches (PR #42 lineage), the "not a second closure…" line and the disclosure safeguard live there. It received one guidance line and nothing else. |
| Replacement of `index.html` | Route banner, Baseline link, policy link. It received one added link (practicals matrix) and nothing else. |
| The 8-step prompt dropdown | Would be a seventh WT-DS/least-prompt wording and a recorded field; queue-16 owns it. |
| Deletion or thinning of print pack / tier routes / witness / Oak links | Protected; the tiers ARE the school's "scaffolded, adapted/TA-supported". All verified intact-or-richer at the gate. |
| v1's `before_reconstruction_html/` images and v2's `*_source_audit.png` | 4.8 KB mock-ups vs 48.5 KB real files (v1); v2's relabelled versions are honest but still stay out of the repo. Neither entered the repo or any staff-facing document. |
| v1 lesson files in their entirety | Superseded by v2; installing any would resurrect `<form>`, `data-testid`, unlabelled controls and external assets. Used as documentation only. |
| The pack's `#printSheet` as a replacement print pack | Ported as one additional section only (§3.8); the tiered pack and witness stand. |
| "BALANCED DIET" as a WORD HELP term (W6A) | Food rule: diet language is prohibited on pupil surfaces; BALANCE with an authored bridge replaced it. |
| The nine remaining We Do lab transplants | A6 is specimen-only; stopped at one, awaiting Matt's written sign-off. |

### Staff-pack rebuild (AMBER)

Content changed, so the OneDrive staff-pack rebuild is automatic policy — but
`tools/build_staff_pack.py` hard-stops without the real Progress Schools
lockup (`--logo`), whose binary is deliberately kept out of git (REBRAND.md;
SHA recorded there). The rebuild therefore **cannot run in this session** and
is flagged AMBER by name rather than skipped silently: Matt (or any holder of
the recorded logo asset) runs the builder against this branch after merge.

## §6 — Gate battery at branch tip

| # | Verdict | Evidence (unit · universe) |
|---|---|---|
| 1 | PASS | Identity 5/5; base = origin/main `574035bf` (stated); rollback recorded above |
| 2 | PASS | 11 inline scripts `node --check` clean; 0 JSON blocks (live chassis carries none — parsed-as-JSON rule had nothing to parse) · 14 changed files |
| 3 | PASS | Headless boot 15/15 (ten lessons + window + guide + index + both matrices), zero page errors · real Chromium via Playwright, so the jsdom `scrollTo`/`matchMedia` shims were **not needed — declared, not silently skipped** |
| 4 | PASS | 0 storage / 0 network / 0 form / 0 external CSS-JS · regex census, 14 changed files |
| 5 | PASS | Six school stages in order (slide `data-type` sequence) 10/10; pack stage names as structure: 0 (`data-label`/element-text scan for ARRIVE/QUESTION/INVESTIGATE) · 14 files |
| 6 | PASS | 3 retrieval + 1 lead-in in each of three tier panels; "New to this class, or not sure?" 10/10 |
| 7 | PASS | supported/standard/stretch/scaffold ci counts ≥ per-file baseline at `574035bf` · 10/10 |
| 8 | PASS | Print pack **richer**: 3 `pp` sections (was 2), 3 `proute` divs, `printTier` + `afterprint` 10/10; evidence sheet is an addition |
| 9 | PASS | `print-witness` 10/10; exactly 2 distinct Oak URLs, byte-identical to baseline |
| 10 | PASS | Banner + `Baseline_Weeks` + `POLICY_ALIGNMENT.md` intact; no `README_LOCAL_PREVIEW` link |
| 11 | PASS | Five branches ≥2 hits each; both safeguard lines; counters/tallies/n-of-5: 0; every `score` occurrence in changed files is a prohibition (classifier corrected once — the window's own "Do not turn this into a pupil label or score" first flagged itself) |
| 12 | PASS | `ll-g:loop-mark v1` = 50, closure line = 113 · git-tracked `*.html`, both unchanged |
| 13 | PASS | Food-language counts byte-identical to per-file baseline (validated on W5A `calorie` ≥ 1); mark scheme / band descriptor / grade boundary: 0 · 14 files |
| 14 | PASS | Reading table recorded (§5 entry): screen 7.10→6.10, print 6.30→5.39, selector stated, protected vocabulary verbatim, C1 deltas within ±15%; per-file AMBERs named |
| 15 | PASS | C2: every pupil-facing instruction on changed surfaces has tier routes + point/say/demonstrate + read-aloud (arrival/independent/exit) + WORD HELP; evidence sheet states scribe route |
| 16 | PASS | Speech: onclick-only, feature-detected, hidden/silent degradation, zero autoplay · 10/10 |
| 17 | PASS | Both new staff artefacts branded; PS variant strip + `x-brand` + exact credit; residue sweep 0 |
| 18 | PASS | No new animation carries meaning; specimen forearm transition suppressed by the global `prefers-reduced-motion` rule; state readouts textual; icon+word throughout |
| 19 | PASS | Working tree clean after commit; branch pushed; **nothing merged, nothing to `main`** |

## Close order — sign-off and delegated completion (2026-08-11)

- **A6 sign-off, Matt's words, recorded verbatim as his: "I like the lab
  specimen."** Dated 2026-08-11. The A6 stop is released; the remaining nine
  labs build on exactly the approved W4A pattern.
- **Merge authority**: Matt's instruction **"complete the job for me"**,
  relayed with the sign-off in the close order `bsg-1-close-2026-08-11`,
  delegates the merge that §9 of the master prompt reserved to him — recorded
  as his, received through his authenticated session while he is away. The
  delegation is **conditional: every gate green at the final tip, sentinels
  unmoved (50/113), otherwise no merge.** Rollback SHA to be re-recorded
  immediately before the merge.
