# Pass SCI-1 — Findings

**What this is.** The record of what Pass SCI-1 measured, changed, and refused — written as it
was done, committed with the work. Companion to `/REGISTER.md` (constraints) and
`/REBRAND.md` (staff-pack procedure).

**Scope built.** 25 v5 science lessons under `Science_Teesside/` — BUILD W3–W7 (5), GROW W3–W7
(5), LAUNCH 5 topics × Discover/Use/Master (15) — each an animated illuminator, a sort/match
We-Do-2, a 3-tier print pack with the Assessor Witness Statement and the canonical loop-mark
strip. Plus: both staff packs rebuilt, and the planner Science rows W03–07 for all three
pathways. Base pinned at `8540eee`; rebased forward onto `main` as it advanced during the pass.

> **Retraction (SCI-3, 2026-07-29).** ~~rebased forward onto the *second writer's* moving `main`~~ —
> the "second writer" framing is retracted. `main` did advance during the pass with commits my
> session did not author (`a4cdd36`, `013121e`/`bc215d1`, `2236d0b`), but those are **Claude-authored
> commits from other passes** (PQ / Season-close / T2-4), several "approved by Matt" — not an
> established separate writer. What survives, directly observed: commits appeared on `main` that this
> session did not create. The sentinel never corroborated a "second writer", and `main` advancing
> without adding loop-mark HTML is not evidence either way of who authored those commits.

---

## What was measured (not assumed)

- **The deployed chassis, directly.** `engine.py`'s "script blocks 0 and 1 reusable verbatim"
  is **false** and was not trusted. Measured from `BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html`:
  the illuminator keyframe family (`ilmPop ilmDraw ilmGlow ilmSpin ilmHand ilmRide ilmRise
  ilmRipple ilmSweep ilmFill` — **no `ilmSpinB`**, which the brief listed), the reduced-motion
  block (`.ilm *{animation:none;opacity:1;stroke-dashoffset:0;transform:none}` already covers
  all illuminator-internal motion), the widget CSS, `registerXP`/`gainXP`/`printPack`, and the
  print structure (**15 `print-section` divs, 11 visible per tier**).

- **The loop-mark sentinel, in the gate's own universe.** `grep -rIl 'll-g:loop-mark' -- '*.html'`
  on pristine `origin/main` = **45**, not the **51** the Block-2 brief (and my own S2 report)
  stated. The "51" counted *all files* — 6 are `.py`/`.md` tooling/docs that mention the string
  (`INSTRUMENTS.md`, `REGISTER.md`, `patch_loopmark.py`, `bundle_facts.py`, one design `.md`,
  one findings `.md`). After the 25 science files: **45 → 70**, delta emitted as the full file
  list at each batch.

- **The Careers filename↔slot swap.** `CAREERS_W6_My_Career_Profile.html` has `<title>` "slot
  **W7**"; `CAREERS_W7_After_Year_11.html` has "slot **W6**". The filenames are the opposite of
  the teaching slot (a prior slot swap left them behind). The README_FIRST warning is grounded
  in this, not invented.

---

## What changed (chassis corrections, now canon)

1. **`_wagollText` is content-bound and sits in "block 0"** — verbatim reuse ships FoodWise's
   WAGOLL into every science lesson. Injected per lesson.
2. **`printPack`'s section array** omitted `glance` and `lundy` and named a non-existent
   `starter`. Slide 3 is **Today at a Glance**; the array now carries glance, witness and lundy
   so all three print in every tier pack.
3. **The loop-mark strip lives in `print-feedback`, not the KO block** (Block-2 §1.3 confirmed;
   the original SCI-1 §6 was wrong). Emitted byte-identical to the estate standard; **LL-INST-09
   passes 17/17 on all three tiers** for every file.
4. **CONTROLS is not content-free** (widening the §2 check beyond `_wagollText`): the
   lesson-complete overlay and the mid-point peer-check overlay embed FoodWise's title,
   subtitle and success criteria. Now patched per lesson with a donor-anchor residue assertion.
   (HEAD's only FoodWise text is the `<title>`, already replaced.)
5. **We Do 2 SORT widget** built for the ambiguous-target case (n cards → k icon+word bins,
   distractors normalising to one bin, keyboard-reachable, `#match-fb` icon+word feedback,
   `registerXP` re-pointed so a sort registers a real denominator — no NaN width). Reused
   verbatim across the suite; match lessons keep the original widget.
6. **Two-period design** (BUILD/GROW): a declared break after We Do 2, a teacher note in
   `print-intro`, and break lines in the TA briefs. LAUNCH runs one lesson per period.

---

## Refinements made against the briefing document (estate/reality wins)

- **Gate 6 ("zero exit answers on any print surface, whole-file")** is *unsatisfiable* when a
  lesson's core KO fact **is** an exit answer — the magnification equation is `ko_facts[0]` and
  the supported exit answer, and the KO must teach it. Gate 6 now enforces the property §6
  actually protects — **no answer *key* on a print surface**: (a) no `class="answer"` element in
  `#print-area`, (b) no exit answer inside `#print-exit`, (c) no distinctive (≥30-char) answer
  outside the teaching surfaces (KO, WAGOLL, scaffold). Re-verified: no Block-2 regression.

- **Print-section count**: kept the chassis reality (15 divs / 11 visible per tier / the 4
  hidden named as the non-selected scaffold+worksheet tier variants), asserted by render — not
  the brief's "14".

---

## Bugs caught and fixed in-pass

- **Illuminator physics**: the Moon phase labels were 90° out (NEW/FULL at top/bottom). With
  sunlight from the left, NEW must sit between Earth and Sun and FULL opposite — fixed.
- **Catalogue footgun**: placing LAUNCH topics one at a time made `place.py`'s tier-scoped strip
  wipe the previous topics' `resources.json` entries, stranding 12 LAUNCH files (on disk but
  unreachable in the hub). Caught by the hub gate. Fixed the catalogue (all 25 registered) and
  added a `place.py` post-condition — every `Science_Teesside` html must have an entry, asserted
  **before** any write — which now fails loudly on the same mistake.

---

## What I refused to do

- **No mark schemes, grade descriptors or band descriptors** anywhere in LAUNCH (UAS route).
  Command words and real question shapes only; model answers and WAGOLLs are fine. Awarding is not.
- **Did not re-author the supplied specs.** The 5 LAUNCH seeds were kept as each arc's spine;
  the 10 new LAUNCH lessons were authored around them.
- **Did not touch the legacy science folders.** `biology/` was read for pitch only and proven
  byte-identical against a hash baseline captured before reading; `chemistry/` and `2 Physics 10/`
  unchanged. The IGCSE 4BI1/4CH1/4PH1 column was noted and left out of scope.
- **Did not swap the two `★ ASSESSED LESSON` conditions blocks** in the staff pack (R-A01 /
  REBRAND rule 7 need Matt's word); rebranded the wordmark only and asserted the conditions
  block byte-identical.
- **Did not invent** URLs, video IDs, accreditation codes (UAS unit left "TBC for Cheryl"), or
  cold-call tier variants (the one authored question is mirrored across F/M/H).
- **Did not merge anything.** All work sits on `claude/sci-1-pass-science-build-b2dyew`.

---

## Gate summary (all green, by render not by reading arrays)

`node --check` · jsdom boot · tag balance / ends `</html>` · print derivation (15/11/4-named) ·
witness in all 3 tiers · exit-answer leak · reduced motion (**0 new keyframe families across all
25**) · LL-INST-09 (17/17, all tiers) · sentinel 45→70 with file list · legacy byte-identity ·
specimen reproduced byte-for-byte · hub reachability (chip 25 == returned 25) · cardinality.
Staff pack: 0 wordmark residue (attribute + domain), x-brand on every page, strip present,
assessed conditions intact, crawl clean, both zips `unzip -t` OK.

## Still open (needs Matt)

- **Clips (§10.3)**: not started — S4 requires one spec per turn with Matt's approval before any
  clip is wired. Nothing wired.
- **The merge**: nothing merges. Matt merges.
