# ECA-1 §1.2 — Chassis census (measured at BASE 7277859)

Universe (from `tables/inventory.csv`, resources.json tags ∩ folder truth): 259 files —
**79 v5-asdan · 6 v5-dt · 31 v5-art · 24 hum-v4 · 35 sci-v3 (PART B DEFERRED — SCA-1 not
on main: no branch, PR or record named SCA-1 exists; the science passes on main are
GSA-1/BSA-1/GSA-FIX-1) · 69 doc · 15 sci-v3-doc.**

Reconciliation notes (resources.json vs folder truth):
- Humanities: 24 live lessons at `{Build,Grow,Launch}/Slideshows/*_HUM_*` all tagged
  `year=2026-27`. The master prompt's known AMBER (Humanities_Teesside tagged 2025-26)
  is **already resolved on main** — all 59 Humanities entries read 2026-27. No metadata
  fix needed.
- `*_Estate_v3/` trees carry 27 duplicate humanities + 27 art + ASDAN entries in
  resources.json — TEST COPIES by rule (§0), excluded from every count and every edit.
- `{Build,Grow,Launch}/Slideshows/*_ART_*` (24 decks) are a **separate art suite** not
  named by ECA-1's universe (Art = Art_Teesside). Untouched; flagged in PROPOSED_A.
- Old `6 Art/` suite (subjects "Art", "Arts Award" in resources.json): out of universe.

## v5 chassis (ASDAN 79 · D&T 6 · Art_Teesside 31)

Organs: `.slide-container` > `.slide[data-title]` (Title, Arrival, Starter, I Do 1/2,
We Do 1/2, Independent, Lundy?, Exit — ASDAN ~10 slides; Art A2 similar), `.li-box`
(guidance: How it works / Instructions / Step 1–2 / Why), `.task-box` (tiered tasks with
**Steps:** lines), `.wit-panel` (moderator paragraph, I Do 2 — ASDAN only), `.sow-strip`
(provenance chip, Title), `.award-strip` (Art: Arts Award part strip — KEEP), `.controls`
= Previous · TA Brief · [ⓘ Guidance on the 85] · Cold Call · Next, arrays `_pres`,
`_ccQuestions`, `_taBriefs`. Print: `#print-area`, 14–15 × `.print-section`
(scaffolds / worksheets / exit / lundy / feedback / witness). GROW/LAUNCH ASDAN also load
`../visual-upgrade.js` (site-repo hud is NOT loaded from decks; `/hud.js` 404 is a hub
caveat only). BUILD decks carry the `ll-g:loop-mark` ring+R strip in print; GROW/LAUNCH
carry the written closure line ("What I said, and what it changed") in print.

PH-3's guidance toggle (85 = 79 ASDAN + 6 D&T): `<style id="mbm-guide-css">`
(`html:not(.mbm-guide-on) [data-mbm-guide], .asvl-purpose, .asvl-route {display:none
!important}`), `ⓘ Guidance` button in `.controls`, key G, `localStorage mbm_guide_v1`,
`<script id="mbm-guide-js">` before `</body>`. Tagged at BASE: li-box guidance (2
counter-WRAPs + 3 attr-TAGs), 3 × task-box Steps:, wit-panel, talk-first line, sow-strip.
Art_Teesside decks do NOT yet carry the toggle (PART B adds it).

## hum-v4 chassis (Migration & Identity v4 — 24 decks)

10 slides: Title, Arrival (`#arrival-slide`), Starter, I Do 1, We Do 1, I Do 2, We Do 2,
Independent, **Lundy Loop** (dedicated slide: `.lundy-grid` > 4 × `.lundy-box` SPACE/
VOICE/AUDIENCE/INFLUENCE), Exit (`#exit-slide`). Controls: Previous · **TA Focus**
(`mbmTAopen()`, `.mbm-modal`) · Cold Call (`mbmCC.open()`) · Next. No `_taBriefs`/
`showTABrief`; no `.sow-strip`/`.award-strip`/`.wit-panel`. Tiers via
`.supported-content/.standard-content/.stretch-content`. Print: 14 × `.print-section`
incl. `#print-lundy` (Lundy table + closure). Closure per pathway **in print**: GROW/
LAUNCH written line present W1–W6, W8; **absent W7 both** (W7 = Write the Account —
eye-check, PROPOSED not fixed: sentinel 123 holds). BUILD HUM closes orally ("out loud,
as a class, is enough here" + scribe offer) — **no ring+R strip**; sentinel 50 holds, so
any change is PROPOSED, not fixed, this pass.

## sci-v3 chassis (science v3_40min — 35 decks, PART B DEFERRED)

Markers: `print-box`/`print-line`/`print-pack`/`print-page` + 1 × `print-section`;
teacher "drawer"; 2 `<script>` blocks. Three print dialects per SCA-1's design — not
re-derived here (deferred).

## doc class (69 + 15)

Hubs, SoW pages, START_HERE, printable packs, trackers, House_Standard_and_Safety,
Arts_Partnership_Log, run sheets. No slide chassis; PART B does not touch docs (the
print pack and TA-brief routes must stay visible — §7 KEEP).

## Sentinel composition (derived, sorted sets in `tables/`)

loop-mark 50 = BUILD_ASDAN 31 + Art_Teesside/Build 8 + Build/Slideshows DT 6 +
Science_Teesside/Build 5. Closure 123 = GROW_ASDAN 18 + LAUNCH_ASDAN 30 + Art G/L 16 +
Grow/Launch Slideshows HUM 14 (7+7) + Science Grow/Launch 45.
