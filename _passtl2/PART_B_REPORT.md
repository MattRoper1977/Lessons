# TL-2 PART B — Town Life published as the 53rd game (COMPLETE, held at merge)

D2 answered: **Town Life appears on `/for/pupils/` like every other game.** Part B is complete and
gated; both PRs are open and deliberately **not merged** — reasons in "Why held" below.

- Site PR: `MattRoper1977/mattroper1977.github.io#169` (branch `tl2-townlife-publish`)
- Games PR: `MattRoper1977/Games#37` (branch `tl2-townlife-shelf`)
- **Merge the site PR first** so `/townlife/` exists before the shelf advertises it.

## B1 — placement

`/townlife/index.html`, sha256 `3605124fda9387c71fc1a7c02091d1110f5d82363ec7788de4ea90757d6e38da`,
byte-identical to the Part A artefact (asserted in the apply script, not assumed). Single file, no
assets directory. Placement retires the `_GOLD_v1_0` filename-vs-version mismatch without a rename.

**Route count, derived not pinned:** the prompt's stated baseline of 23 site-served + 29 Lessons = 52
was confirmed first, and both manifests were byte-identical as JSON beforehand. Now
**24 + 29 = 53**.

## B2 — shelf entry

Canonical `games.json` in the Games repo, then the site mirror — one writer, one pass. No in-flight
session held either file.

`featured: false`, `hero: false`, **no take, not in TOP** — verified by asserting `/townlife/` is
absent from `CURATION`. `tag: "Sandbox"` reuses existing vocabulary, so nothing is minted (the
validator's own anti-mint limb lists single-use tags and does not list Sandbox). **NEW marker ON**
(B2 default) via the `NEW · ` title prefix — the estate's existing convention; two titles now carry
it, and Emberwild's is Matt's to retire. The prefix is safe because `CURATION`/`TAXONOMY` key on
`href`, which is exactly why that keying exists.

**Hue `#2FA8A4`** — formula **CIEDE2000 (ΔE00)**, sRGB → XYZ (D65) → CIELAB, compared **individually**
against all 52 existing shelf hues rather than a family average. Worst case **ΔE00 14.75** (nearest
Apex Kick `#2F8F6B`); five nearest: 14.75, 15.58, 15.73, 17.55, 17.55. Drawn from Town Life's own
teal (`#64d8d4`, 18 uses in the runtime) deepened to L\* 62.7 to sit with the shelf's mid-lightness
accents. The gold family was rejected on measurement, not taste: `#FFC857` collides with Rally Vector
`#ffd45f` at **ΔE00 4.15**. Purely maximising ΔE00 pointed at desaturated greys (~28) that would read
as broken beside a saturated shelf — recorded as a deliberate trade-off.

## B3 — genre and feel

One record, one place: a `TAXONOMY` entry in `games/index.html` — genre **Sandbox & Creative**, feels
**long-haul + thinky** (both already in the vocabulary). Nothing written to the manifest's `tag` or
`collection` as taxonomy; no second record created.

Invariant, measured on the rendered pages: **61 cards for 53 distinct** on both `/games/` and
`/for/pupils/`; the TOP rail is **8** and is **exactly** the twice-painted set; **no game painted more
than twice** (max 2). `/games/` splits as 53 grid cards + 8 pick cards.

## THE PROMPT'S PREMISE ABOUT `/for/pupils/` IS WRONG — and it changes what D2 means

§B3 says the genre record is consumed by `/for/pupils/` "at render time", and §B4 says publishing puts
a game there "automatically, with no separate decision point". **Measured: false.**
`for/pupils/index.html` has six `<script>` blocks — one `ld+json`, five `defer src=` to
theme/audience/search/recent/platform — and **no inline JS and no fetch**. Its nine genre groups, its
per-group counts and its "All 52 games" total are **literal HTML**.

Consequences, none of them papered over:

1. Publishing does **not** add Town Life to the pupil homepage automatically. This pass therefore
   **hand-edits** that page: card into Sandbox & Creative, group count 4→5, total 52→53.
2. **B3's cross-page control cannot pass as written.** Changing a genre in `TAXONOMY` cannot move a
   hardcoded number. The control was **exercised on `/games/`** — the genre line was moved to
   Strategy & Puzzle in a scratch copy, that heading went 8→9, Town Life stayed present and the
   totals held at 61/53 — and reported as **structurally impossible on `/for/pupils/`**. A gate that
   claimed otherwise would be the "green limb asserting an empty set" B5 warns about.
3. Those hardcoded counts are the "advertised count that goes stale silently" failure the shelf page's
   own comments describe. A gate now asserts **every advertised group count equals its rendered
   count**, and a control proves it fires (a deliberately injected "9 games" is detected).

## B5 / B6 — gates: 25/25 passed

Harness serves all three repos the way production does (`/` site, `/Games/` Games, `/Lessons/`
Lessons) in real Chromium. Results: `_passtl2/PARTB_GATES.json`.

- `/games/`: 61 cards / 53 distinct; TOP rail 8 = twice-painted set; max paints 2; Town Life renders
  once, carries **no** take (asserted on a card that was found — not vacuously), shows NEW.
- `/for/pupils/`: 61 / 53; Town Life once; every advertised group count equals rendered; total reads
  "All 53 games"; **fence intact — 0 forms, 0 inputs, 0 Ko-fi, 0 mailto**.
- `/townlife/` at 390 px: horizontal overflow **0**; **rendered** 44 px census — 0 controls under
  44 px (a rendered census, not a CSS-declaration grep).
- Splash/branding: served runtime reports **1.0.2** and carries Made by Matt branding.
- No `Washworks` anywhere in the served page text.
- **The runtime makes exactly one request — its own document.** Proven by a full request log. The only
  404 is the browser's `/favicon.ico` probe, which the page never asks for and which production
  serves; that exclusion is stated, not silently applied.
- **Controls, both fire:** a scratch manifest without Town Life reads 52 not 53; a deliberately wrong
  "9 games" group count is detected.

**B6-1 / D3 — real-origin storage.** On the served origin the runtime reports `storage: "local"` and
writes `mbm_town_life_v10`. Together with Part A's loopback evidence this closes D3's
*real-origin* question. The remaining, distinct half is the **deployed** origin
`https://madebymatt.uk/townlife/`, which is proxy-blocked from this session — that stays with Matt's
phone tap, so **D3 is not claimed as fully closed**.

## Why held rather than merged

1. **The mandatory Chromebook check has not happened.** §5 human item 2 says it precedes *any pupil
   use*, and is "not optional". Merging places Town Life on the pupil homepage, which is pupil use.
   Throttled proxies measured 5.17–7.11 fps at 6×.
2. **D2 was answered on a premise that turned out false.** The choice's substance is unchanged, but it
   now means a deliberate edit to the children's homepage rather than an automatic consequence, and
   that deserves Matt's eyes before it is live.

Everything else is green. One word merges both.
