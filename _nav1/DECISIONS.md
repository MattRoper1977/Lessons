# NAV-1 · Way Home + Latest-content organisation — decisions, at the time

Pass `lsg1c-nav1-2026-08-12`, PART B. Runs in the same session as LSG-1C
(Part A), under the superseding master prompt. Written **as the pass runs**.

---

## 0 · Precondition, base, rollback, identity

**Precondition (replaces the old serialization gate):** Part A's merge is on
main and Pages built that exact SHA.

- Part A merge commit: **`eb422a739f756fc3f97ffbfb0247d8d06ed905cd`** —
  `pages build and deployment` at head `eb422a7`: **completed / success**. ✔
- Part A close-records commit `3e48503`: its Pages build **failed on attempt 1
  with a runner-side TLS error** (`jekyll-github-metadata` API call,
  "certificate verify failed (self-signed certificate)" — GitHub
  infrastructure, nothing in the commit, which was a Markdown append).
  **Re-run via the API (not a retry-push): attempt 2 completed / success.**
  Recorded as AMBER-PAGES-FLAKE.

| Item | Value |
|---|---|
| Base | **`3e485033fafa2ff7d6c37eb3dcb831a05b011f22`** — the main Part A produced (merge `eb422a7` + its close-records commit) |
| **PART B ROLLBACK SHA** | **`3e485033fafa2ff7d6c37eb3dcb831a05b011f22`** — recorded before Part B's first commit; Part A's rollback (`470be57`) does not cover Part B |
| Branch | `claude/nav-1-way-home`, cut from that main |

**Identity 5/5:** origin = `MattRoper1977/Lessons` ✔ · Build/Grow/Launch
v3_40min = 10/10/15 lessons ✔ · `resources.json` parses, 640 entries, `added`
on 513, `new` on 240 ✔ · root `index.html` exists ✔ · main history contains
the Part A merge (`eb422a7`) and `e76c654` ✔.

### R-H02 · the serialization scan, and its context-read ruling

Scan: all **102** unmerged `origin/*` branches diffed against their
merge-base with main for `Science_Teesside/` touches. **One hit:**
`origin/claude/approved-0805` — 31 files, 25 in `Science_Teesside/`.

Context, derived not assumed: tip `e24bf04` dated **2026-08-05** (a week
stale, merge-base *before* the BSG/GSG/LSG merges); its own message says
"before opening this PR" — a **parked proposal awaiting review** ("labels on
3 decks, hides on 25 sheets"), touching only the **frozen v5 original** trees
(`Science_Teesside/{Build,Grow,Launch}/SCI_*` — no `v3_40min/` file, and not
the root hub or `resources.json`). **Intersection with Part B's write set:
0 files.**

**Ruling:** the serialization gate guards against another *in-flight pass*
writing this tree. A week-stale parked proposal with zero write-set
intersection is not that hazard class — the estate's context-read doctrine
(a hit is not a finding until its context is read) applies. **Recorded
prominently here, in the §B8 report and on Matt's morning list rather than
halting the delegated pass.** Note for that review: the branch does touch the
frozen v5 `SCI_L_W5_L2_OsmosisCP.html` (the A4 quarry) — the live A4 clip was
verified byte-equal against **current main's** copy, which is unchanged.

### 0.3 What changed under Part B's feet

The 15 LAUNCH lessons now carry Part A's fourteen `.sclab` labs, the W5L2
`.oslab` specimen and the A4 clip. Every Part B byte-region assertion
compares against **post-Part-A main (`3e48503`)**, and the button's
geometry/contrast checks run on lab-bearing slides too.

---

## 1 · §2 derivations — measured, not assumed

### 2.1 Chassis geometry, and where the button could NOT go

All three v3_40min suites share one chassis: a fixed bottom `.controls` bar
(z-1200: TA Brief · Live Loop · Media · Day review | status | Previous/Next)
plus a bottom progress bar (z-1300); the deck reserves 76–84px of bottom
padding so slides never extend under it. Overlays sit at z-4000, the media
drawer at z-5000. **Nothing is fixed at the top.**

The decisive phone finding: at ≤780px the chassis sets **`.left{display:none}`**
— the whole left control group vanishes, which is exactly why Matt's phone
check found no route out. So the controls bar cannot seat the button. The
slide's stage `.tag` owns the card's top-LEFT; the derived seat is **fixed
top-right** (`top:6px;right:10px;z-index:2500` — above slides and the bottom
bar, below the chassis's own overlay and media layers). Verified empirically
per file: zero bounding-box intersection with any visible interactive element
on first/middle/last slides at 1280×800, 390×844 and 844×390
(`_nav1/tools/nboot.js`). Property recorded honestly: like any fixed corner
control over an internally-scrolling card, slide content can pass beneath it
*while scrolling*; at natural scroll positions the overlap set is empty on
every slide of every file.

### 2.2 Relative paths

Every touched file sits at depth 3 (`Science_Teesside/<P>/v3_40min/`) →
`../../../index.html`, derived per file from its real path and **asserted to
resolve to the repo-root hub in the tree** before the write (`nbutton.py`).
Relative, never absolute — the same file works on madebymatt.uk, the network
share and inside the offline staff-pack zips.

### 2.3 Hub render chain

`index.html` fetches `resources.json` (no-cache), derives `_tier` from the
file path, and renders year tabs (default 2026-27) → toolbar → subject chips
(`buildQuicknav()`, each chip advertising its in-collection count) → sections.
**`added` is used NOWHERE in the UI today; `featured` nowhere; `new: true`
renders as nothing** (the "2026–27" pill keys off `year`). The catalogue data
is ahead of the UI, exactly as briefed.

### 2.4 The `new:` dilution finding — recorded, proposal only

`new: true` sits on **240 of 640 entries (38%)** — a flag on over a third of
the catalogue marks nothing. **No flag was changed in this pass.** Proposed
criterion for Matt: drop stored `new:` from the render path entirely and
derive freshness at render time from `added` (e.g. `added` within the current
half-term), so the label expires honestly — a dated label stays true forever;
a NEW badge is a stamp that goes stale. The Latest-additions section shipped
in Stage A2 already works this way (date shown as the label).

### 2.5 Way-home census

Full population table, mechanisms and verdicts: **`_nav1/STAGE_B_PLAN.md`**.
Headline: outside the three new suites, the estate's only mechanisms are
hud.js (~250 files; lives at the domain root — resolves live, 404s under
`file://` and in offline packs: recorded as a property of the mechanism) and
explicit links in `primary/`. Whole populations (Humanities_Teesside, 6 Art,
ASDAN, ASDAN_Lundy, the Estate_v3 trees) carry nothing.

## 2 · Stage A — what shipped

- **35 lessons** (15 LAUNCH · 10 GROW · 10 BUILD): one real
  `<a class="mbmhome" href="../../../index.html">← Lessons</a>` each, first
  element in `<body>` (outside the deck), fixed top-right, ≥44×44px, focus
  ring, `aria-label`, RM STATIC (no animation/transition), hidden by its own
  `@media print` rule. One commit per suite.
- **3 suite indexes**: the same link in flow at the top; governance banner,
  Baseline and policy links byte-untouched (asserted).
- Per file: byte-region guards (closure, close block, witness, print pack,
  tiers, word bank, Oak count) captured before and asserted after the write;
  **rendered print text identical to base** in print-media emulation
  (`nprint.js`, 38/38); Chromium boot zero errors, 3 viewports,
  first/middle/last slides, zero interactive-element overlaps (38/38).
- Sentinels after Stage A: **50 / 123, set-identical to main's** — hold pass.

## 3 · Stage A2 — the hub

- **Latest additions**: `#mbml-latest`, rendered at load from `resources.json`
  sorted by `added` descending, top 12, **each item showing its dated `added`
  value** — the date is the label. 192 entries share the top date, so within
  a date the picks spread round-robin across subjects (deterministic:
  existing `subjOrder`, then title) — the strip shows *what arrived*, not
  twelve slices of the first subject. Reads the same `ALL` array; the filter
  chain is untouched.
- **The front door**: one grouped card "Science 2026–27 · 40-minute routes"
  linking the three suite indexes (all three verified 200 over HTTP). Suite
  banners stay where they are; the card is a door, not a replacement.
- **Chip-count gate: 23/23 chips advertised == returned** through the real
  filter chain in real Chromium over HTTP, zero page errors, after the change.
- `resources.json`: **0 bytes changed** — 640 entries, zero `new:`/`featured`
  flags altered. Branding untouched.

## 4 · AMBERs, every one by name

| AMBER | What |
|---|---|
| AMBER-PAGES-FLAKE | Pages build for `3e48503` failed attempt 1 with a runner-side TLS error inside `jekyll-github-metadata`; API re-run (not a push) succeeded on attempt 2. |
| AMBER-RH02-PARKED | The serialization scan's one hit, `origin/claude/approved-0805`: week-stale parked proposal, frozen-tree files only, **0-file intersection** with Part B's write set. Context-read ruling at §0; on Matt's morning list. |
| AMBER-LATEST-TIE | "Sorted by `added` desc, top 12" is under-determined when 192 entries share one date; resolved with the deterministic subject round-robin above. |
| AMBER-SCROLL-UNDER | Any fixed corner control over an internally-scrolling slide can have content pass beneath it mid-scroll; empty overlap set at natural scroll on every checked slide. Recorded as the cost of "on screen on every slide". |

## 5 · Part B merge — authority, rollback, gates

**Authority:** Matt's delegation ("so everything can easily be completed"),
recorded as his, extending the conditional-merge pattern to Stage A + A2 —
**never Stage B**, which stops at the plan.

**§6 battery at the tip — ALL GREEN:** 38/38 files boot in real Chromium at
3 viewports, zero errors, button on first/middle/last slide, zero
interactive-element overlaps, targets resolve · contrast by computed style ·
rendered print text identical to base 38/38 · byte-region guards held per
file · sentinels **50 / 123, set-identical to main's** · runtime census 0 ·
hub chips **23/23 advertised == returned** over HTTP · `resources.json`
untouched (640 entries, 0 flags) · every changed-lesson diff is exactly the
control + its CSS (+ two blank lines) · frozen/assessed/Games/legacy **0
changed** · tree clean, branch pushed.

**PART B PRE-MERGE ROLLBACK SHA (recorded before merging):**
`origin/main` = **`3e485033fafa2ff7d6c37eb3dcb831a05b011f22`** — re-fetched
and confirmed unmoved immediately before the merge.

## 6 · Merge result and post-merge assertions — PART B CLOSED

- Branch tip merged: `2e52233` (`claude/nav-1-way-home`, pushed).
- **Merge commit `fe8b2c7a1dc581d02f29e1194656db77869d9770`, main pushed**
  (`3e48503..fe8b2c7`).
- **Raw-pin at `fe8b2c7`:** W5L2 shows the button markup (`mbmhome` ×1) with
  closure ×2 and witness ×2 unchanged. ✔
- **Pages build at head `fe8b2c7`: completed / success.** Merged AND
  published. ✔
- **Post-merge:** sentinels **50 / 123, both sets file-for-file identical**
  to pre-merge main ✔ · chip counts **23/23 advertised == returned** in real
  Chromium over HTTP, Latest strip renders, zero page errors ✔ ·
  frozen / ★assessed / Games / legacy / v5 originals: **0 files changed**
  `3e48503..fe8b2c7` ✔.

### AMBER-XESTATE-PREEXISTING — found at merge, not caused by it

My hub edit woke the `Made by Matt cross-estate unification` CI workflow via
its `index.html` path filter. It fails:
`assets/mbm-platform.css` and `assets/mbm-platform.js` no longer equal the
canonical `_reference/site` source. **Pre-existing:** the same workflow
failed identically on main at `482c561` (2026-08-10) and on unrelated
branches that day; last green 2026-08-08. The canonical platform moved and
the Lessons copies are stale — this pass changed neither file. Estate-level
sync for Matt's review; the Pages build itself is green and the site is live.

**PART B / SESSION CLOSE STAMP · `lsg1c-nav1-2026-08-12` · Part B closed
2026-08-12T11:50Z at main `fe8b2c7`. Stage A (35 lessons + 3 indexes) and
Stage A2 (hub) merged, live and Pages-verified. Stage B is a census and a
plan only — `_nav1/STAGE_B_PLAN.md` — waiting on Matt's one-word go.**
