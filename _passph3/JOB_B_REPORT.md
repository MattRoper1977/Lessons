# PH-3 JOB B REPORT — guidance hidden by default, 85 decks

Scope: 79 ASDAN lessons + 6 `Build/Slideshows/BUILD_DT_W1–W6`. No `GUIDE:` override lines were
present, so the §5.2 hide-set shipped as ruled. Per-deck tag counts are in
`_passph3/GUIDANCE_INVENTORY.md` (committed before any apply, B-G0).

## What each deck now carries (all five artifacts, reversible by construction)

1. `<!--mbm-guide:v1-->` marker (idempotence key) — once per file.
2. `<style id="mbm-guide-css">` — `html:not(.mbm-guide-on) [data-mbm-guide], … .asvl-purpose, … .asvl-route {display:none!important}` + a `box-shadow` pressed-state for the button. No transitions.
3. `<button class="mbm-guide-btn" aria-pressed="false" onclick="mbmGuideToggle()">ⓘ Guidance</button>` between **TA Brief** and **Cold Call** in `.controls` (label becomes "ⓘ Guidance ✓" when on).
4. `<script id="mbm-guide-js">` — IIFE that defines and then immediately initialises (no bare
   `try{}catch{}` around init, per CLAUDE.md; only the `localStorage` accesses are individually
   guarded because `file://` can throw). Reads `mbm_guide_v1` (`'1'` = on; default off), toggles
   `mbm-guide-on` on `<html>`, syncs `aria-pressed` + label, binds `g`/`G` (ignored in
   input/textarea/contenteditable and while a `.v4-modal-overlay`/lesson-complete/midpoint overlay
   is visible — hud.js binds only Escape; the deck binds arrows/Escape, no collision), announces
   through `#vu-live-region` when visual-upgrade has created one, silently otherwise.
5. Tags: ` data-mbm-guide="1"` attributes and, on the two counter boxes only,
   `<span data-mbm-guide="1">…</span>` wrapped around the instruction text with the
   `Found:`/`Score:` counter left outside the wrapper.

## Counts (uniform across the 85 — per-deck table in the inventory)

| pattern | per deck | total |
|---|---|---|
| li-box counter-wraps (How it works ✱ `#pres-num`, Step 1/2 ✱ `#match-score`) | 2 | 170 |
| li-box attr-tags (Instructions ×2, Why ×1) | 3 | 255 |
| `Steps:` paragraphs in `.task-box` (3 tiers) | 3 | 255 |
| `.wit-panel` moderator paragraph | 1 (79 ASDAN; the 6 D&T have none) | 79 |
| "Talk first, then we play" Starter line | 1 (79 ASDAN; D&T none) | 79 |
| `.sow-strip` provenance chip | 1 | 85 |
| `.asvl-purpose` / `.asvl-route` | CSS-only (runtime-injected on the 48 visual-upgrade decks) | — |

**Unclassified li-box labels — stay VISIBLE (7 instances, listed per deck/slide in the
inventory):** `🧭 Coming next` (5 decks), `🔎 Contrast check` (1), `🧭 And that's the unit` (1).
No label was guessed into the hide-set.

## Gate results

- **B-G1 reversibility: 85/85** — removing marker + style + script + button, unwrapping the
  spans (inner HTML kept) and stripping the attributes reproduces the pre-Job-B file
  **byte-identically** (reference `fd95fffb…`; for 82 decks that equals BASE bytes; for
  W4/W5/DT-W6 it equals BASE + their authorised Job A edits).
- **B-G2 idempotence:** second apply run patched 0/85 (marker key) — zero diff.
- **B-G3 print purity: PASS** — zero `data-mbm-guide` inside any `#print-area` subtree;
  `print-section` count per file unchanged; every original script block (incl. `printPack` id
  lists) byte-identical.
- **B-G4 protected lines: PASS** — no protected D&T string inside any tagged element or wrapper;
  `#pres-num`/`#match-score` (and every id'd element) outside every tag.
- **B-G5 runtime (jsdom 30, https-origin + repo-mapped resources): PASS 85/85** — boots with no
  console error (expected `/hud.js`-absent and jsdom-CSS-parser noise excluded); default state
  hidden (computed `display:none` on tagged elements, counters visible); button flips class +
  `aria-pressed` + storage; `g`/`G` toggles and is ignored while the TA modal is open;
  ArrowRight/ArrowLeft still navigate; TA Brief + Cold Call still open; `mbm_guide_v1='1'`
  honoured on reload; on all **48** visual-upgrade decks the `asvl-panel` renders with
  `.asvl-purpose` hidden by default and `.asvl-notice` visible.
- **B-G6:** `node --check` on all 263 unique inline script blocks — 0 failures; div balance
  unchanged; sentinel `ll-g:loop-mark` per-file counts unchanged and the repo-wide bearing set
  is 50 files, equal to BASE (LAUNCH carries none); hud.js loader presence per file unchanged
  (79 lessons + 6 D&T all carried it at their own baselines); no new absolute URLs; no
  `<script src>` added.
- **B-G7:** per-slide visible-text multiset (tags stripped) equals pre-Job-B for every slide of
  every deck — hiding moved and rewrote nothing (the button text lives in `.controls`, outside
  the slides).

## Storage key registration

`mbm_guide_v1 — boolean, guidance visibility, no pupil data.` The repo keeps no general
storage-key register: the two files that list `mbm_cc_v1` (`LundyLoop/6_designs/LL-I_B1_measurement_map.md`
— a Tutor_Time-scoped store inventory — and `quality/SAFEGUARDING_CONTENT_GATE.md` — a
don't-touch instruction) are suite-scoped documents, so the key is recorded **here** rather
than appended to a document whose scope it would break.

## Estate map — the chassis beyond the 85 (measured proposal, NO edits made)

`class="li-box"` decks outside this pass's scope, by tree: Art_Teesside 31 (Build 15 / Grow 8 /
Launch 8) · Science_Teesside 35 (Build 5 / Grow 15 / Launch 15) · Build/Slideshows non-DT 8
(ART/HUM/L1 chassis-bearing subset) · root science suites ("2 Physics 10" 16, biology 8,
chemistry 8) · "6 Art" 15 · "5 Intervention 10" 5 · "5_6 Local Choice" 2 · Grow 8 · Launch 8 ·
one ASDAN-tree non-lesson page — **≈145 further decks** share the li-box/.controls chassis and
could take the same five-artifact patch mechanically. Proposed as a follow-up rollout
(OPEN_ITEMS 50); nothing outside the 85 was touched.
