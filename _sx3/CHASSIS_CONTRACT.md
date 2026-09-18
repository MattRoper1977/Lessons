# SX3 chassis contract — the three W8–W13 exemplars

**Ruling R-CH (ORDER SX3-2).** The chassis target for all 79 incoming decks is the live
W8–W13 exemplar **for the deck's own pathway** — not the deck's current shell and not a
generic label. This file is the parity instrument: every row is a feature and the DOM or CSS
selector that proves it.

**How these were measured.** From the bytes at Lessons `main` `d872ef99`, which is what the
education publication serves — each exemplar's path is present in
`domain-split/education-publication-admission.json` `trees["education-lessons"]`, the
publication's own manifest. The agent container cannot reach `madebymatt.uk` (the proxy
denies CONNECT), so this is the served source, not an origin fetch. Classification is
`tools/chassis_census.py` — a DOM query, never a substring match.

**The three exemplars are NOT on the same shell.** That is the point of R-CH: BUILD
normalises to `classroom`, GROW and LAUNCH to `review`. A single estate-wide target would be
wrong for two of the three pathways.

| pathway | exemplar | chassis | bytes | sha256 | served |
|---|---|---|---:|---|---|
| BUILD | `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html` | **classroom** | 639630 | `74d17d4e0f6873f0…` | yes |
| GROW | `Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html` | **review** | 291226 | `2560984b05d13f2e…` | yes |
| LAUNCH | `Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html` | **review** | 293788 | `1e46f94da927f5bb…` | yes |


## BUILD — `SCI_B_W8A_Sugar_Labels_Explore.html`

Chassis class: **`classroom`**. Every row below must be present in a normalised BUILD deck;
`present` is the count measured on the exemplar.

| # | feature | selector that proves it | exemplar |
|---:|---|---|---:|
| 1 | Deck root | `main#lessonDeck` | 1 |
| 2 | Slide container | `main.slide-container` | 1 |
| 3 | Review top nav | `nav.review-top` | 0 |
| 4 | Classic toolbar | `nav.classic-toolbar` | 1 |
| 5 | Skip link | `a.skip` | 0 |
| 6 | XP wrap | `#xpWrap` | 1 |
| 7 | XP fill / count / total | `#xpFill`, `#xpCount`, `#xpTotal` | 3 |
| 8 | Lesson-complete overlay | `#lc-overlay` | 1 |
| 9 | Auto timer | `#auto-timer` | 1 |
| 10 | Timer toggle + display | `#auto-timer-toggle`, `#auto-timer-display` | 2 |
| 11 | Word help | `#word-dialog` | 1 |
| 12 | Pause | `#pause-dialog` | 1 |
| 13 | Tools & print | `#tools-dialog` | 1 |
| 14 | Knowledge organiser open | `#organiser-dialog` | 1 |
| 15 | KO print group + clip | `#ko-*-group`, `#ko-*-clip` | 4 |
| 16 | TA layer | `#ta-dialog` | 1 |
| 17 | Cold-call dialog | `#cold-call-dialog` | 1 |
| 18 | Arrival: Supported | `#arrival-panel-supported` | 1 |
| 19 | Arrival: Standard | `#arrival-panel-standard` | 1 |
| 20 | Arrival: Stretch | `#arrival-panel-stretch` | 1 |
| 21 | Arrival print x3 | `#print-arrival-{supported,standard,stretch}` | 3 |
| 22 | Arrival ANSWERS print x3 | `#print-arrival-answers-*` | 3 |
| 23 | Exit print x3 | `#print-exit-*` | 3 |
| 24 | Per-stage task print | `#print-task-*` | 3 |
| 25 | Print area | `#print-area` | 1 |
| 26 | Answers reveal / print | `#print-answers` or `#all-answers` | 1 |
| 27 | Organiser print | `#print-organiser` | 1 |
| 28 | Shared print | `#print-shared` | 1 |
| 29 | Staff card / staff print | `.staff-card` or `#print-staff` | 1 |
| 30 | Teacher-only region | `.teacher-only` | 2 |
| 31 | Science reveal control | `.science-reveal` | 0 |
| 32 | Progress bar + label | `#progressBar`, `#progressLabel` | 2 |
| 33 | Classic progress + status | `#classic-progress`, `p#classic-status` | 2 |
| 34 | Previous / Next / Picker | `#previous-slide`, `#next-slide`, `#slide-picker` | 3 |
| 35 | Slides | `[id^="slide-"]` | 9 |
| 36 | lesson-config | `script#lesson-config` | 1 |
| 37 | Pathway theme class | `.pathway-{build,grow,launch}` | 1 |

**Navigation and path form**

- `← Lessons` → `../../../index.html?subject=Science&pathway=BUILD` (no class)
- Path form is **relative**, never a hardcoded `https://madebymatt.uk/…` absolute.

**Runtime and style facts**

- External scripts: `/hud.js`
- `prefers-reduced-motion` blocks: **7**
- `@media print` blocks: **16**; `size: A4` page rules: **3**
- localStorage keys: `(none — HUD is external)`
- CSS custom properties (26): `--arrival-order`, `--aspire-bg`, `--aspire-border`, `--aspire-text`, `--bg`, `--btn-bg`, `--btn-hover`, `--error`, `--ido-bg`, `--ido-border`, `--lo-bg`, `--lo-border`, `--lo-text`, `--muted`, `--sc-bg`, `--sc-border`, `--scaffold-bg`, `--scaffold-border`, `--slide-bg`, `--success`, `--task-bg`, `--task-border`, `--text`, `--wedo-bg`, `--wedo-border`, `--zone-count`


## GROW — `SCI_G_W8A_Day_And_Night_Explore.html`

Chassis class: **`review`**. Every row below must be present in a normalised GROW deck;
`present` is the count measured on the exemplar.

| # | feature | selector that proves it | exemplar |
|---:|---|---|---:|
| 1 | Deck root | `main#lessonDeck` | 1 |
| 2 | Slide container | `main.slide-container` | 1 |
| 3 | Review top nav | `nav.review-top` | 1 |
| 4 | Classic toolbar | `nav.classic-toolbar` | 0 |
| 5 | Skip link | `a.skip` | 1 |
| 6 | XP wrap | `#xpWrap` | 0 |
| 7 | XP fill / count / total | `#xpFill`, `#xpCount`, `#xpTotal` | 0 |
| 8 | Lesson-complete overlay | `#lc-overlay` | 0 |
| 9 | Auto timer | `#auto-timer` | 1 |
| 10 | Timer toggle + display | `#auto-timer-toggle`, `#auto-timer-display` | 2 |
| 11 | Word help | `#word-dialog` | 1 |
| 12 | Pause | `#pause-dialog` | 1 |
| 13 | Tools & print | `#tools-dialog` | 1 |
| 14 | Knowledge organiser open | `#organiser-dialog` | 1 |
| 15 | KO print group + clip | `#ko-*-group`, `#ko-*-clip` | 4 |
| 16 | TA layer | `#ta-dialog` | 1 |
| 17 | Cold-call dialog | `#cold-call-dialog` | 1 |
| 18 | Arrival: Supported | `#arrival-panel-supported` | 1 |
| 19 | Arrival: Standard | `#arrival-panel-standard` | 1 |
| 20 | Arrival: Stretch | `#arrival-panel-stretch` | 1 |
| 21 | Arrival print x3 | `#print-arrival-{supported,standard,stretch}` | 3 |
| 22 | Arrival ANSWERS print x3 | `#print-arrival-answers-*` | 3 |
| 23 | Exit print x3 | `#print-exit-*` | 3 |
| 24 | Per-stage task print | `#print-task-*` | 6 |
| 25 | Print area | `#print-area` | 1 |
| 26 | Answers reveal / print | `#print-answers` or `#all-answers` | 2 |
| 27 | Organiser print | `#print-organiser` | 1 |
| 28 | Shared print | `#print-shared` | 1 |
| 29 | Staff card / staff print | `.staff-card` or `#print-staff` | 2 |
| 30 | Teacher-only region | `.teacher-only` | 3 |
| 31 | Science reveal control | `.science-reveal` | 2 |
| 32 | Progress bar + label | `#progressBar`, `#progressLabel` | 2 |
| 33 | Classic progress + status | `#classic-progress`, `p#classic-status` | 2 |
| 34 | Previous / Next / Picker | `#previous-slide`, `#next-slide`, `#slide-picker` | 3 |
| 35 | Slides | `[id^="slide-"]` | 9 |
| 36 | lesson-config | `script#lesson-config` | 1 |
| 37 | Pathway theme class | `.pathway-{build,grow,launch}` | 1 |

**Navigation and path form**

- `← Lessons` → `../../../index.html` (class `mbmhome`)
- `← Lessons` → `START_HERE.html` (class `way-home`)
- Path form is **relative**, never a hardcoded `https://madebymatt.uk/…` absolute.

**Runtime and style facts**

- External scripts: **none — everything inlined**
- `prefers-reduced-motion` blocks: **5**
- `@media print` blocks: **15**; `size: A4` page rules: **6**
- localStorage keys: `mbm_guide_v1`
- CSS custom properties (28): `--arrival-order`, `--aspire-bg`, `--aspire-border`, `--aspire-text`, `--bg`, `--btn-bg`, `--btn-hover`, `--error`, `--growdark`, `--ido-bg`, `--ido-border`, `--lo-bg`, `--lo-border`, `--lo-text`, `--muted`, `--n6-nav1`, `--n6m-guide`, `--sc-bg`, `--sc-border`, `--scaffold-bg`, `--scaffold-border`, `--slide-bg`, `--success`, `--task-bg`, `--task-border`, `--text`, `--wedo-bg`, `--wedo-border`


## LAUNCH — `SCI_L_W8L1_Enzyme_Action_Introduce.html`

Chassis class: **`review`**. Every row below must be present in a normalised LAUNCH deck;
`present` is the count measured on the exemplar.

| # | feature | selector that proves it | exemplar |
|---:|---|---|---:|
| 1 | Deck root | `main#lessonDeck` | 1 |
| 2 | Slide container | `main.slide-container` | 1 |
| 3 | Review top nav | `nav.review-top` | 1 |
| 4 | Classic toolbar | `nav.classic-toolbar` | 0 |
| 5 | Skip link | `a.skip` | 1 |
| 6 | XP wrap | `#xpWrap` | 0 |
| 7 | XP fill / count / total | `#xpFill`, `#xpCount`, `#xpTotal` | 0 |
| 8 | Lesson-complete overlay | `#lc-overlay` | 0 |
| 9 | Auto timer | `#auto-timer` | 1 |
| 10 | Timer toggle + display | `#auto-timer-toggle`, `#auto-timer-display` | 2 |
| 11 | Word help | `#word-dialog` | 1 |
| 12 | Pause | `#pause-dialog` | 1 |
| 13 | Tools & print | `#tools-dialog` | 1 |
| 14 | Knowledge organiser open | `#organiser-dialog` | 1 |
| 15 | KO print group + clip | `#ko-*-group`, `#ko-*-clip` | 4 |
| 16 | TA layer | `#ta-dialog` | 1 |
| 17 | Cold-call dialog | `#cold-call-dialog` | 1 |
| 18 | Arrival: Supported | `#arrival-panel-supported` | 1 |
| 19 | Arrival: Standard | `#arrival-panel-standard` | 1 |
| 20 | Arrival: Stretch | `#arrival-panel-stretch` | 1 |
| 21 | Arrival print x3 | `#print-arrival-{supported,standard,stretch}` | 3 |
| 22 | Arrival ANSWERS print x3 | `#print-arrival-answers-*` | 3 |
| 23 | Exit print x3 | `#print-exit-*` | 3 |
| 24 | Per-stage task print | `#print-task-*` | 6 |
| 25 | Print area | `#print-area` | 1 |
| 26 | Answers reveal / print | `#print-answers` or `#all-answers` | 2 |
| 27 | Organiser print | `#print-organiser` | 1 |
| 28 | Shared print | `#print-shared` | 1 |
| 29 | Staff card / staff print | `.staff-card` or `#print-staff` | 2 |
| 30 | Teacher-only region | `.teacher-only` | 3 |
| 31 | Science reveal control | `.science-reveal` | 0 |
| 32 | Progress bar + label | `#progressBar`, `#progressLabel` | 2 |
| 33 | Classic progress + status | `#classic-progress`, `p#classic-status` | 2 |
| 34 | Previous / Next / Picker | `#previous-slide`, `#next-slide`, `#slide-picker` | 3 |
| 35 | Slides | `[id^="slide-"]` | 9 |
| 36 | lesson-config | `script#lesson-config` | 1 |
| 37 | Pathway theme class | `.pathway-{build,grow,launch}` | 1 |

**Navigation and path form**

- `← Lessons` → `../../../index.html` (class `mbmhome`)
- `← Lessons` → `START_HERE.html` (class `way-home`)
- Path form is **relative**, never a hardcoded `https://madebymatt.uk/…` absolute.

**Runtime and style facts**

- External scripts: **none — everything inlined**
- `prefers-reduced-motion` blocks: **5**
- `@media print` blocks: **15**; `size: A4` page rules: **6**
- localStorage keys: `mbm_guide_v1`
- CSS custom properties (29): `--arrival-order`, `--aspire-bg`, `--aspire-border`, `--aspire-text`, `--bg`, `--btn-bg`, `--btn-hover`, `--error`, `--growdark`, `--ido-bg`, `--ido-border`, `--lo-bg`, `--lo-border`, `--lo-text`, `--muted`, `--n6-nav1`, `--n6m-guide`, `--sc-bg`, `--sc-border`, `--scaffold-bg`, `--scaffold-border`, `--slide-bg`, `--success`, `--task-bg`, `--task-border`, `--text`, `--wedo-bg`, `--wedo-border`, `--zone-count`


## Notes that affect the generator fix

1. **BUILD depends on a Site-owned file.** Its exemplar loads `/hud.js` — the Live-Teach
   HUD, published from the Site repository to the education-site root. A normalised BUILD deck
   must carry that script tag. Referencing it changes no Site file, so it stays inside the
   SX3-2 fence, but it is a cross-repo runtime dependency and is named here rather than
   discovered later.

2. **GROW and LAUNCH carry two `← Lessons` anchors**, not one: `a.mbmhome` →
   `../../../index.html` and `a.way-home` → `START_HERE.html`. BUILD carries one, unclassed,
   with a query string. Both forms are relative.

3. **`.science-reveal` is GROW-only** on these exemplars (2 on GROW, 0 on BUILD and
   LAUNCH), and per-stage task prints differ (BUILD 3, GROW and LAUNCH 6). Contract rows are
   per pathway for exactly this reason; do not level them.

4. **No `--mbm*` tokens.** The palette is the 26–29 local custom properties listed per
   pathway above (`--bg`, `--ink` family, `--lo-*`, `--sc-*`, `--aspire-*`, `--ido-*`,
   `--scaffold-*`), plus `--n6-nav1` and `--n6m-guide` on GROW and LAUNCH.

5. **The guide toggle is the only storage on GROW and LAUNCH**: `mbm_guide_v1`, read and
   written inside try/catch, toggling `.mbm-guide-on` on `<html>`. BUILD keeps its state in
   the external HUD instead.



---

# Amendments ruled at STOP-SX3-2a (ORDER SX3-2)

Confirmed as written: three separate tables, BUILD = `classroom`, GROW = `review`,
LAUNCH = `review`, 36 rows each, **no levelling between pathways**.

## A1 — BUILD's `/hud.js` is a contract row and a known cross-repo runtime dependency

Contract row, BUILD only. The exact tag form, verbatim from the exemplar:

```html
<script defer src="/hud.js">
```

(that is the literal serialised form in the exemplar — `defer` first, `src` second)

- Part 2 **carries this tag verbatim**. It does not vendor, inline, copy or modify `hud.js`.
- `hud.js` is owned by the Site repository and published to the education-site root, so `/hud.js`
  resolves from the education origin. It is the Live-Teach HUD (floating dock: timer, name
  picker, noise meter, calm reset) — it supplies none of the XP or lesson-complete furniture,
  which is inline in the deck.
- **KNOWN CROSS-REPO RUNTIME DEPENDENCY.** Nothing in the SX3-2 fence changes it. The Part 3
  serve proof must show `/hud.js` resolving **200** from the education origin.
- GROW and LAUNCH load no external script. A `/hud.js` tag on a GROW or LAUNCH deck is a FAIL.

## A2 — `← Lessons`: the exemplar's exact anchor form(s) per pathway

| pathway | anchors required | href at the exemplar's depth |
|---|---|---|
| BUILD | one, unclassed | `../../../index.html?subject=Science&pathway=BUILD` |
| GROW | two | `a.mbmhome` → `../../../index.html` · `a.way-home` → `START_HERE.html` |
| LAUNCH | two | `a.mbmhome` → `../../../index.html` · `a.way-home` → `START_HERE.html` |

- All forms are **relative**. The pack's hardcoded
  `https://madebymatt.uk/Lessons/index.html?subject=Science&pathway=…` is a **contract FAIL in
  every variant**.
- **Depth is derived, never copied.** The exemplars sit at
  `Science_Teesside/<Pathway>/W8-W13_2026-27/`, three levels below the Lessons root, hence
  `../../../`. A deck at `Science_Teesside/Grow/SCI_G_W3_Friction.html` is two levels down and
  takes `../../index.html`. Part 2 computes `../` × depth from the deck's **actual** target path
  and **proves it by resolving the result inside the checkout** — a path that does not resolve
  to a real file is a FAIL, not a warning.
- `a.way-home` → `START_HERE.html` is resolved in the deck's own folder. Where the deck's folder
  has no `START_HERE.html`, that is a FAIL for the deck and it is PARKED, not shipped with a
  broken link.

## A3 — Palette, root class and storage

- **Palette row** = the exemplar's custom-property set, present with the exemplar's values, per
  pathway. The sets are listed per pathway above (26 BUILD, 28 GROW, 29 LAUNCH). **No token
  layer is introduced** — no `--mbm*` indirection, no shared token file.
- **Root class.** A3 asks for `.theme-<pathway>` on the root. **Measured: no exemplar carries a
  `theme-` class anywhere.** All three carry exactly `<html class="pathway-<pathway>">` and
  nothing else. Adding `theme-<pathway>` would put a class on 79 decks that no exemplar has,
  which contradicts R-CH ("the exemplar is the contract") and A3's own "no token layer is
  introduced". **Part 2 therefore emits `<html class="pathway-<pathway>">`, the measured
  exemplar form, and this discrepancy is raised at STOP-SX3-2b rather than resolved here.**
- **Storage.** `mbm_guide_v1` is the **only** permitted key, on GROW and LAUNCH only, read and
  written inside try/catch, toggling `.mbm-guide-on` on `<html>`. **BUILD writes no storage of
  its own** — its state lives in the external HUD. Any other `localStorage` or `sessionStorage`
  key in a rebuilt deck is a FAIL.

## Parity rule for Part 2

A deck passes only when **all three** hold:

1. `tools/chassis_census.py` class **==** its pathway exemplar's class; and
2. **all 36 contract rows present** for its pathway, plus A1–A3 above; and
3. the pack's own `qa/browser_checks.json` is green for its topic.

**Any deck at more than 0 missing rows is PARKED, not shipped.**

---

# Part 2 measurements taken before the generator work

## The estate's own chassis toolchain cannot be used as the shell

`_authoring/science_2026-27/_toolchain/chassis/shell.py` exposes `render_shell(d, slides_html,
print_html, inline_js)` — Matt's recovered classic slideshow chassis, with per-family donor CSS
in `styles/<pathway>_<subject>.css`, `controls.js` and `access.css`. It was the obvious
candidate for "wrap pack content in the exemplar shell".

**Measured: its output is `classic`.** It emits `div.classic-toolbar` and a `main.slide-container`
with no id, and carries no `#xpWrap`, no `#lc-overlay`, no `main#lessonDeck`, no `nav.review-top`,
no `a.skip`, no `#organiser-dialog` and no `a.mbmhome`/`a.way-home`. `classic` is **none** of the
three exemplar classes, so `render_shell` would fail R-CH on all three pathways.

Part 2 therefore **transplants** instead: `chassis/estate_shell.py` parses the pathway exemplar,
keeps every structural element and id exactly as the exemplar has them, and replaces only the
content-bearing regions. Every contract row then survives by construction.

## The pack content and the exemplar containers are the same shape

| region | exemplar | pack `content.json` |
|---|---|---|
| arrival, per route | `#arrival-panel-<route>` = `div.arrival-four` with **4** × `article.arrival-cell` (`h3`, `p.arrival-hint`, `p.arrival-answer`) | `arrivals.<A\|B>.<route>` = **4** × (title, question, help, answer) |
| exit, per route | `#print-exit-<route>` with **2** × `article.question-card` | `exits.<A\|B>.<route>` = **2** × (…) |
| word help | `#word-dialog` `<dl>` | `words` |
| TA brief | `#ta-dialog` | `teaching` (per stage) + `safety` + `guardrails` |
| organiser | `#organiser-dialog`, `#print-organiser` | organiser page in `print_pages.ALL` |
| print sections | 20 `section.print-section` in `#print-area` | `print_pages.ALL` / `selected_pupil()` |

The mapping is 1:1, so the transplant is mechanical rather than interpretive.

## A2 resolve check: 25 of 79 decks have no `START_HERE.html` to point at

`estate_shell.resolve_or_fail` proves every rewritten href against the checkout. It refuses, and
the refusal is not hypothetical:

| pathway | target folder | `START_HERE.html` | decks |
|---|---|---|---:|
| BUILD | `Science_Teesside/Build/W8-W13_2026-27` | present | 9 |
| BUILD | `Science_Teesside/Build/W14-W20_2026-27` | present | 2 |
| BUILD | `Science_Teesside/Build` | **MISSING** | 5 |
| GROW | `Science_Teesside/Grow/W8-W13_2026-27` | present | 14 |
| GROW | `Science_Teesside/Grow/Autumn2_W7_2026-27` | present | 2 |
| GROW | `Science_Teesside/Grow` | **MISSING** | 5 |
| LAUNCH | `Science_Teesside/Launch/W8-W13_2026-27` | present | 17 |
| LAUNCH | `Science_Teesside/Launch/W14-W15_2026-27` | present | 3 |
| LAUNCH | `Science_Teesside/Launch/Autumn2_W7_2026-27` | present | 3 |
| LAUNCH | `Science_Teesside/Launch` | **MISSING** | 15 |

50 resolve. **25 do not** — and they are exactly the 25 whole-lesson-route parent-folder decks
of §4f (Build 5, Grow 5, Launch 15). Their folders are the parent route, not a dated pack folder,
so no `START_HERE.html` exists there. Under A2 as ruled they park. 4 ADD-lane decks have no
folder chosen yet.

---

# Part 2 halt: the batch has three built-output dialects, and 43 decks have no generator

The ruling assumed "four `build_html.py` variants edited; rebuild all 79". Measured across the
79 decks, that covers 36 of them. The rest have no generator to edit.

| built-output dialect | decks | pathways | `#print-area` | regenerable source |
|---|---:|---|---|---|
| **A** · sugar format, slide ids `a0`…`b5` | 39 | BUILD 18, GROW 21 | yes | 36 of 39 |
| **B** · slide ids `s0`…`sN` | 23 | LAUNCH 23 | yes | **none** |
| **C** · slides carry no id at all | 17 | BUILD 2, LAUNCH 15 | **NO** | **none** |

All three classify `other`. All three carry arrival and exit content, but under three different
id conventions — `arrival-<route>-<n>` (C), `answer-arrival-<route>-<n>` (B), route panels with
`data-route-panel` (A) — and dialect **C has no `#print-area` element at all**, so contract row
25 cannot be transplanted from the pack for those 17 decks; it would have to be constructed.

Consequences for the plan as ruled:

1. **There is no "edit four generators and rebuild" route for 43 of 79 decks.** The four
   `build_html.py` variants live only in dialect A's `source/` folders.
2. The uniform route that does work for all three dialects is a **DOM transplant from the built
   pack HTML** into the exemplar containers — the content is present in every dialect — but that
   needs one adapter per dialect (three), not one generator edit per variant (four).
3. Dialect C additionally needs `#print-area` built rather than moved.

Nothing was rebuilt and no generator was edited. Reported at STOP-SX3-2b for a ruling.

---

# Row 37 — provenance (R-PROV, ORDER SX3-2)

**Every content-bearing region must differ from the exemplar's, measured per deck. A deck that
fails row 37 is HELD, never shipped.**

This row exists because structural parity alone passed decks that had silently kept the
exemplar's own lesson. Before readers B and C landed, 40 of 75 decks would have shipped W8A's
arrival and exit questions on a different lesson: rows 1–36 all present, content wrong.

Regions compared, per deck, as normalised rendered text against the pathway exemplar:

| | region |
|---|---|
| 1–3 | `#arrival-panel-supported`, `#arrival-panel-standard`, `#arrival-panel-stretch` |
| 4–6 | `#print-arrival-supported`, `#print-arrival-standard`, `#print-arrival-stretch` |
| 7 | `#print-arrival-answers-supported` |
| 8–10 | `#print-exit-supported`, `#print-exit-standard`, `#print-exit-stretch` |
| 11 | `#print-task-supported-1` |
| 12–15 | `#print-organiser`, `#print-answers`, `#print-shared`, `#print-area` |
| 16–19 | `#word-dialog`, `#ta-dialog`, `#organiser-dialog`, `#tools-dialog` |

A region that is non-empty and identical to the exemplar's is a failure. Empty is not a pass by
itself — the row it belongs to still has to be present under rows 1–36.

**The control is not vacuous, proved both ways on the same instrument:** it failed 40 of 75 decks
before the dialect readers existed, and passes 72 of 72 after. Same check, same decks, opposite
verdicts, with only the readers changed.

## Named gaps, ruled at STOP-SX3-2b

| row | gap | ruling | decks |
|---|---|---|---:|
| 15 | KO groups — the pack ships an HTML organiser (`article.sheet`), not the exemplar's clipped A4 vector (`clipPath#ko-*`) | **R-KO**: accept the HTML organiser. No SVG render, no `#ko-*` ids added. KO must still open in the exemplar dialog and print on one A4 page. | 72 |
| 31 | `.science-reveal` — the pack uses `details.answer-details` ("Worked explanation · reveal after thinking") | **R-SR**: no dressing. Same role, different markup is a gap, not a pass. | 19 |
| 30 | `.teacher-only` absent in the pack | **R-GAPS**: named gap, shipped. | 18 |
| — | `#print-first-back` has no pack source | **R-GAPS**: named gap, shipped. | 57 |

## Dialects, detected by content shape (R-READERS)

Never by the presence of `script#lesson-data` — every dialect carries one, which is exactly how
40 decks got silently defaulted to A.

| dialect | signature | reader | decks |
|---|---|---|---:|
| **A** | ids `answer-arrival-<A\|B>-<route>-<n>` | DOM route panels + `#lesson-data.pages` | 35 |
| **B** | ids `answer-arrival-<route>-<n>` | same slide/page schema as A, cards by `details[@id]` | 23 |
| **C** | ids `arrival-<route>-<n>` | `#lesson-data.arrival/.exit/.vocab/.prints`; routes are the item's supported/plain/stretch faces | 14 |
| **D** | ids `arrival-<routeIndex>-<n>`, dialogs `dialog-ko`/`dialog-words`/`dialog-staff`, **no `.slide` elements** | **not built** — discovered at 2b, not commissioned | 3 |

A deck the detector cannot classify is **HELD**, never defaulted.

---

# Row 38 — zero uncaught page errors (R-38, ORDER SX3-2c)

**Zero uncaught page errors on load AND after exercising every pack interactive element once,
measured in the browser per deck. Failure → HELD.**

Elements are enumerated from the DOM, never hand-listed: `[data-action]`, `[data-reveal-group]`,
`[data-print*]`, `[data-choice]`, `[data-check-choice]`, `[data-model-step]`, `[data-place]`,
`[data-card]`, `[data-goto]`, `[data-trial-*]`, `[data-check-*]`, `[data-route]`,
`[data-reveal-target]` and every `details > summary`. 85–178 elements per deck.

**Red proof.** Same deck, same gate, one shim entry removed:

| deck | change | row 38 |
|---|---|---|
| `SCI_G_W3_Friction.html` | untouched | **PASS** (178 exercised, 0 errors) |
| `SCI_G_W3_Friction.html` | the re-emitted `#lesson-data` node removed, nothing else | **FAIL** — `Cannot read properties of null (reading 'textContent')` at line 759 |

## The six rules that closed row 38

Each is a rule over all 75 decks, not a fix to one:

1. **Drop the exemplar's lesson-specific scripts.** An exemplar inline script that reaches for
   an id the exemplar has and this deck does not is removed. The BUILD exemplar's
   `#rich-sugar-interactions` was binding to W8A's `#label-step`.
2. **`#lesson-data` first.** Re-emitted from the pack at the top of `<body>`, before any script
   that reads it.
3. **Preserve shell-owned nodes.** Any subtree whose id a surviving shell script references
   survives a region or dialog fill. `#ta-current-title` and `#ta-current-text` live inside
   `#ta-dialog`; clearing it made `showTABrief()` write to null.
4. **Clone the exemplar's roots.** `[data-arrival-root]` and `[data-exit-root]` are copied from
   the exemplar and only their cells swapped, so every control they carry survives. Writing the
   markup by hand kept missing one — `[data-exit-print]` was the last.
5. **One id-reference rule.** `byId('x')`, `getElementById('x')`, `querySelector('#x')`,
   `$('#x')`, `$$('#x')` — one `script_ids()` used by the shim, the drop rule and the protect
   set. Missing the `byId` spelling is what let rule 1 fail silently.
6. **Shim only what the pack really had.** The shim supplies a private inert node for an id or
   class **the pack's own DOM carried** and the transplant dropped — nothing else. The pack
   guards its optional features (`if($('#particles')){…}`), so inventing the element turns a
   no-op into a throw. A shimmed node also takes **the tag the pack used**, so a `<canvas>`
   stays a canvas.

Two further rules, from defects this work introduced rather than found:

- **An unfillable print section is emptied, not left.** Leaving the exemplar's own lesson in a
  print section is a row 37 failure by construction; it is cleared and named as a gap.
- **The pack's dialog hook is nested, not lost.** The pack reads its own content through its own
  dialog id (`$('#dialog-ko .organiser')`), so the transplanted body is wrapped in that id —
  the same content, one extra hook, no duplication.

## Alias register (R-ALIAS)

`#sx3-pack-shim`, approved in place of aliasing: the pack script is bound to **none** of the
exemplar's controls, so double-driving is impossible by construction rather than by inspection.

**777 entries across 75 decks** — 408 neutralised, 311 inert, 58 shared (pack reads only).
Most-shimmed: `next` and `lesson-data` (75 decks each), `prev`, `timer-display`, `timer-reset`,
`timer-toggle` (61), `confirm-reset`, `live-status`, `progress-fill`, `stage-count` (58).

Attribute mapping, where the pack spells an estate container differently:
`data-check ← data-choice-task`, applied per deck and recorded.

---

## ORDER SX3-GO2b — rows 39–41, and what the earlier instrument could not see

### VOID: every historical pass on a print row, and on row 37's print-region provenance

Not superseded — **void**. They were produced by an lxml parse of the file on disk. The pack's
own script owns `#print-area` at runtime (`setPrint()` assigns `byId('print-area').innerHTML`),
so on 58 of 75 decks every `#print-*` section the static parse counted is deleted the moment
JS runs. R-KO's "the organiser opens and prints A4" is void on the same ground and was
re-proved in the browser (below). Do not cite any of them.

### Row 39 — dialog control parity (RENDERED)

For every dialog the exemplar owns, the chassis controls that still drive something in the
transplanted deck must survive the content fill. The fill previously kept only `h2` and
shell-owned **ids**; a `<button data-action="close">` has neither, so all four content-filled
dialogs lost every control. Measured 71/71 before, 75/75 after.

A control is kept when it still drives something. `close` and `goto` do. The shell's print
furniture does not — the pack owns `#print-area` — so it is a **named gap**, listed per deck in
`_sx3/RELEASE_LEDGER.md`, never shipped dead:

| named gap | decks |
|---|---:|
| `tools-dialog` · `action:print`, `onclick:Print A4 organiser` | 75 |
| `ta-dialog` · `onclick:Print teacher answers` | 75 |
| `organiser-dialog` · `onclick:Print organiser` | 75 |
| `ta-dialog` · `staff-card:marking`, `staff-print:marking`, `staff-card:first-back`, `staff-print:first-back` | 57 |
| `ta-dialog` · `onclick:Print teaching notes` | 18 |

### Row 40 — pack dialog remap

The pack opens its own dialogs with `$('#dialog-'+key).showModal()`. The transplant folds each
pack dialog's body into the exemplar dialog that owns that region and nests the pack's id there
so the pack's content hooks still resolve — which made the pack's id a `<div>`, and `.showModal()`
threw. The nested wrapper now forwards `showModal`/`show`/`close`/`open` to the exemplar
`<dialog>` holding its content. No second dialog is created; no exemplar control is bound twice.
Readers A, B and C now record `dialog_source_ids` as reader D already did — that omission is why
two decks kept a control reaching for a `#staff-dialog` that no longer existed.

### Row 41 — every dialog the deck carries can be opened

All three exemplars keep the knowledge-organiser opener inside slide 1, so the slide rebuild
took it with them. BUILD and GROW packs supply their own `[data-action="organiser"]`; the LAUNCH
packs do not — leaving 38 decks with a populated `#organiser-dialog` no teacher could open. The
exemplar's own opener is restored when the pack supplies none. Measured in the browser:
75/75 decks, zero unopenable dialogs.

### Standing rules

4. **Source selection is never filesystem order.** Every candidate is collected, duplicates are
   detected by content, and a filename carrying two generations must have an explicit ruling or
   the run stops. The choice is recorded per deck in the ledger.
5. **Behavioural rows are measured in a rendered browser.** A static parse returns NOT-CHECKED
   for rows 38, 39, 41 and every print row, and is structurally unable to emit PASS for them.

---

# Rows 42–45 — ORDER SX3-END4 and after

Recorded here because they were implemented in the transplant
(`_authoring/science_2026-27/_toolchain/chassis/estate_shell.py`) but never
written into this contract. Row 45 is recorded as reverted, not as a rule.

## Row 42 — the shell's own controls must not be double-driven

The pack ships a document-level `[data-action]` handler. On a transplanted deck
that handler ran **in addition to** the chassis's own, so a click on the TA
control opened the dialog and then immediately re-ran `openDialog('ta-dialog')`,
which closed it; the exemplar's close handler then stripped `mbm-guide-on`. The
TA dialog rendered 0×0 on **40 of 71** decks.

**Rule.** Every element the chassis contributes carries `data-sx3-shell="1"`, and
a guard stops click propagation from those elements so only the chassis handler
drives them. Measured in a rendered browser by driving the real controls, not by
dispatching synthetic events.

## Row 43 — estate furniture survives the transplant

`a.mbmhome`, the `n6-nav1` navigation shell and the `<script defer src="/hud.js">`
tag are estate furniture, not lesson content. The transplant restores them from
the deck being replaced.

The hud tag is asserted in its literal form, `<script defer src="/hud.js">` —
ruled by Matt, who corrected an earlier reading of mine that allowed a variant.

## Row 44 — the exemplar's sibling navigation is unwrapped

The pathway exemplar carries its own next/previous sibling links (`Next · W8L2 ·`
and so on). Transplanted verbatim, every deck inherited the exemplar's
neighbours. Links the chassis contributes are tagged `data-sx3-shell-link` and
unwrapped rather than copied.

## Row 45 — WRITTEN AND REVERTED. Not a rule.

A print-isolation remap was written on the premise that the chassis should own
`#print-area` on dialect D decks. **The premise was disproved**: the pack
source's own `#printArea` is empty in the file and filled at runtime by the
pack's `setPrint()`. The remap was reverted. It is recorded here so the next
person does not rediscover the same wrong premise — there is no row 45.

## Row 46 — PROPOSED, not implemented. `lesson-config` binding keys.

Measured 2026-09-18, not yet authorised. The transplant **replaces**
`lesson-config` wholesale instead of merging it, so the deck loses its tie to the
scheme of work and to its neighbours:

| key | landing decks that lose it (of 36) |
|---|---|
| `timings`, `previousFile`, `nextFile`, `id` | 30 |
| `week`, `objective` | 27 |
| `handoff`, `model1Steps`, `model2Steps`, `glitch`, `independent`, `mission` | 24 |

`sow` is lost on all 30 that carry one, which is why 30 of the 36 landing decks
fall out of `lesson-order.json`'s week binding. `previousFile`/`nextFile` is
lesson navigation, and is very likely the root of the "Original Science
navigation" defect.

**Proposed rule.** `lesson-config` is merged, not replaced: the chassis deck's
binding keys (`sow`, `objective`, `week`, `id`, `previousFile`, `nextFile`,
`timings`, `source`) are carried through, and the pack supplies the rest.

Simulated end to end against the real builder: `unresolvedTiming` 36 → 6,
`weekBound` 238 → 268. The remaining 6 are the decks with no `lesson-config` on
main to carry from. See `_sx3/STOP_S4_lesson_config.md`.
