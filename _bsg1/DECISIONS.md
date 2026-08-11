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
