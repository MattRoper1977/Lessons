# Convergence prep — evidence

**Branch:** `claude/convergence-prep` · **base:** `main` at `cacaf16977646b40f0ff72c9e5112a7f31877679`
**Date:** 2026-08-01 · **Scope:** evidence only. Nothing was deleted, nothing was merged, `main` was not touched.

This pass answers one question: *if `build-anim/` were deleted and the five Autumn 1
BUILD science lessons ran on the GROW engine through `compat-build-anim.js`, what
would break?*

The answer is **five things, all measured, none of them fatal, none of them fixed here.**
The re-injection on this branch is the experiment, not the proposal.

---

## What was done

`reports/convergence/inject_convergence.py` re-injects the five BUILD lessons against
`grow-anim/` instead of `build-anim/`. `reports/convergence/audit.mjs` and
`reports/convergence/stepstate.mjs` then walk every slide of every lesson in Chromium and
record what actually happens. Both were run twice — once on `main`'s lessons (the control)
and once on this branch's — and every number below is a comparison of those two runs.

Raw data: `reports/convergence/_data/{before,after}.json` and
`reports/convergence/_data/steps-{before,after}.json`.
Renders: `reports/convergence/<lesson>/slide-NN.png`, 60 images at 1280×720.

### The README's step 1 was too glib

> "Re-inject the five Autumn 1 lessons against `grow-anim` rather than this folder —
> `inject.py`'s `BLOCKS` table is where that switch happens."

Changing `BLOCKS` does nothing, for two reasons:

1. **The marker vocabularies are disjoint.** BUILD lessons carry
   `/* BUILD-ANIM:CSS|BIO|BODY|FOOD|CHAIN|JS */`. `grow-anim/inject.py` writes
   `/* GROW-ANIM:MOTION|COMP|POLISH|SVG|BIO|ANIM|PHY|CHEM|ENGINE|SHINE */`. Point either
   injector at the other suite's files and it finds no markers and exits 0 having written
   nothing. The switch has to be a *re-mapping* of BUILD's six markers onto GROW's sources.
2. **Load order is forced.** `compat-build-anim.js` reads `global.GrowAnim` at load, so it
   must run after `grow-anim.js`; the BUILD subject libraries call `global.BioSVG.helpers`
   at load, and compat is what defines `BioSVG`, so they must run after compat. BUILD's
   marker order is CSS → BIO → SUBJECT → JS, so the entire GROW engine *and* the compat
   shim have to land in the **BIO** block and the **JS** block becomes a stub.

### Neither injector reports a per-step match count

`grep -ci "data-ba-script\|data-grow-script\|data-part\|match"` returns **0** for both
`build-anim/inject.py` and `grow-anim/inject.py`. Neither knows anything about animation
scripts or part names — `--check` only re-splices each source between its markers and
byte-compares the result against the file on disk.

There are also two different things called a "step": *injection* steps target marker names,
*animation script* steps target part names. Only the second can fail silently. Both are
measured below, separately.

---

## Finding 1 — `compat-build-anim.js` cannot be inlined as it stands

Its usage comment contains four literal `<script src=…></script>` lines. Inlined raw, the
first `</script>` closes the block; the following three become real `<script>` elements
requesting files that do not exist next to the lesson.

Measured on the first attempt, before the fix:

```
PAGEERROR SyntaxError: Invalid or unexpected token
file:///grow-anim/grow-svg-bio-animals.js :: net::ERR_FILE_NOT_FOUND
file:///grow-anim/grow-anim.js            :: net::ERR_FILE_NOT_FOUND
file:///grow-anim/compat-build-anim.js    :: net::ERR_FILE_NOT_FOUND

BuildAnim: undefined   GrowAnim: undefined   BioSVG: undefined   GrowSVG: undefined
svgs: 0   svgParts: 0   stages built: 0 of 5
```

Twelve slides of every lesson, no error dialog, no build failure, exit 0 — and not one
thing on the page moves. `inject_convergence.py` escapes `</script` and `</style` in every
inlined source (`ESCAPES`, +5 bytes per lesson). **Neither existing injector does this**,
because until now no inlined source contained the token. Found by rendering, not by reading.

## Finding 2 — the XP score drops on all five lessons

`compat-build-anim.js` translates markup that is **in the file at load time**. Elements the
GROW engine *builds afterwards* — prediction cards, the stage inside a prediction panel —
are born `.g-pc` / `.g-stage` and never carry the old class. Each lesson's own glue counts
`document.querySelectorAll('.ba-pc').length` to register XP, and now counts zero.

| lesson | `xpTotal` | `.ba-pc` | `.g-pc` | `.ba-stage` | `.g-stage` |
|---|---|---|---|---|---|
| `SCI_B_W3_Backbones` | **13 → 7** | 7 → 0 | 0 → 7 | 6 → 5 | 0 → 6 |
| `SCI_B_W4_Muscle_Pairs` | **9 → 6** | 4 → 0 | 0 → 4 | 6 → 5 | 0 → 6 |
| `SCI_B_W5_Right_Nutrition` | **9 → 6** | 4 → 0 | 0 → 4 | 6 → 5 | 0 → 6 |
| `SCI_B_W6_Balanced_Plate` | **10 → 6** | 5 → 0 | 0 → 5 | 6 → 5 | 0 → 6 |
| `SCI_B_W7_Where_Food_Comes_From` | **10 → 5** | 6 → 0 | 0 → 6 | 6 → 5 | 0 → 6 |

51 XP across the unit becomes 30. Nothing errors; the number is just quietly smaller.

## Finding 3 — `data-*-frame` means different sizes in the two engines

| frame | `build-anim.css` | `grow-anim.css` |
|---|---|---|
| `wide` | 34vh | 34vh |
| `mini` | **24vh** | **20vh** |
| `tall` | **44vh** | **58vh** |

Measured on `#wedo1b-rail` in W4 at 1280×720:

| | before | after |
|---|---|---|
| SVG `max-height` | 316.8px | 417.6px |
| SVG rendered height | 312.0px | 393.6px |
| stage height | 403.6px | 485.2px |
| rail caption top edge | y = 620.8 | y = 702.4 |

The caption ("The model you built" / "The arm it copies") is still in the DOM with the same
text, but it is pushed to y=702 on a 720px-high screen and lands underneath the fixed
navigation bar. Compare `reports/convergence/SCI_B_W4_Muscle_Pairs/slide-07.png` against the
same slide today: the captions are gone from view. This is the largest pixel change in the
whole set (15.22%), and it is the same cause on every `frame="tall"` slide.

## Finding 4 — "Show all" loses the narration line

`build-anim`'s `all()` calls `step()` per step, which sets the narration. `grow-anim`'s
`all()` inlines the loop and skips the `.g-say` update. On the teaching path (▶ Next, once
per step) narration is identical — this only affects the ▶ Show all button.

W4, all five stages, after `reset()` then `all()`:

| | narration set | narration blank |
|---|---:|---:|
| before | 5 | 1 (stage has no say element) |
| after | 1 | 5 |

Before: *"Swap them over. The bottom one pulls now."* After: the placeholder
*"Press ▶ Start and narrate as it appears."*

## Finding 5 — `BioSVG.list()` stops seeing the subject libraries

The compat shim maps `list()` to `GrowSVG.list('animals')`, which returns only the 13
classification animals. Assets registered by `body-svg.js`, `food-svg.js` and
`chain-svg.js` still **render** correctly — every one of them is exercised below — but they
are invisible to `list()`.

| lesson | `BioSVG.list().length` |
|---|---|
| `SCI_B_W3_Backbones` | 13 → 13 |
| `SCI_B_W4_Muscle_Pairs` | 16 → 13 |
| `SCI_B_W5_Right_Nutrition` | 16 → 13 |
| `SCI_B_W6_Balanced_Plate` | 16 → 13 |
| `SCI_B_W7_Where_Food_Comes_From` | 20 → 13 |

No lesson calls `list()`. `build-anim/demo.html` does, and would show 13 assets instead of
20.

---

## What did NOT change

### Slide counts — gate 4

| lesson | slides before | slides after | titles identical |
|---|---:|---:|---|
| `SCI_B_W3_Backbones` | 12 | 12 | yes |
| `SCI_B_W4_Muscle_Pairs` | 12 | 12 | yes |
| `SCI_B_W5_Right_Nutrition` | 12 | 12 | yes |
| `SCI_B_W6_Balanced_Plate` | 12 | 12 | yes |
| `SCI_B_W7_Where_Food_Comes_From` | 12 | 12 | yes |

All twelve `data-title` strings match position-for-position in every lesson: Title, Arrival
Task, Today at a Glance, I Do 1, I Do 1b, We Do 1, We Do 1b, I Do 2, We Do 2, Independent
Work, Lundy Loop, Exit Ticket.

### Element census

| lesson | `[id]` | `<script>` | `<style>` | `<svg>` | `[data-part]` | `[data-label]` | `.print-section` | `.match-pill` |
|---|---|---|---|---|---|---|---|---|
| W3 | 52 → 53 | 7 | 4 | 9 → 10 | 42 | 18 | 15 | 6 |
| W4 | 52 → 53 | 8 | 10 | 6 → 7 | 33 | 26 | 15 | 5 |
| W5 | 52 → 53 | 8 | 8 | 5 → 6 | 40 | 10 | 15 | 5 |
| W6 | 52 → 53 | 8 | 9 | 6 → 7 | 60 | 10 | 15 | 5 |
| W7 | 52 → 53 | 8 | 4 | 5 → 6 | 31 | 17 | 15 | 4 |

The one added id and the one added `<svg>` are the same element: `#g-mblur`, the motion-blur
filter `grow-polish.js` appends once per page. `idsDuplicated` is `[]` on every lesson before
and after, so it collides with nothing.

### Script-step target resolution — gate 3, the silent-failure trap

Every step of every stage was parsed out of the built stage (`stage._g.steps`) and each
target name resolved against the rendered DOM using the engine's own `byAttr()` logic.
Prediction-panel cards were clicked so their per-card scripts were audited too — those
scripts do not exist in the DOM until a card is tapped.

| lesson | script steps audited | distinct target names | **targets matching 0 elements** | min | max |
|---|---:|---:|---:|---:|---:|
| `SCI_B_W3_Backbones` | 72 | 17 | **0** | 1 | 4 |
| `SCI_B_W4_Muscle_Pairs` | 76 | 21 | **0** | 1 | 2 |
| `SCI_B_W5_Right_Nutrition` | 77 | 22 | **0** | 1 | 1 |
| `SCI_B_W6_Balanced_Plate` | 82 | 14 | **0** | 1 | 1 |
| `SCI_B_W7_Where_Food_Comes_From` | 80 | 18 | **0** | 1 | 1 |

**387 target resolutions, 0 matched nothing** — identical counts before and after, and the
per-name totals (`audit.byName` in the JSON) are byte-identical between the two runs on all
five lessons. No script step targets a part name the converged engine cannot find.

### Injection steps

| lesson | markers matched | bytes |
|---|---|---:|
| `SCI_B_W3_Backbones` | CSS + BIO + JS (3) | +74,972 |
| `SCI_B_W4_Muscle_Pairs` | CSS + BIO + BODY + JS (4) | +75,020 |
| `SCI_B_W5_Right_Nutrition` | CSS + BIO + FOOD + JS (4) | +75,020 |
| `SCI_B_W6_Balanced_Plate` | CSS + BIO + FOOD + JS (4) | +75,020 |
| `SCI_B_W7_Where_Food_Comes_From` | CSS + BIO + CHAIN + JS (4) | +75,022 |

19 marker blocks, every one matched. `--check` afterwards: `ok` ×5, exit 0.
Control on `main` beforehand: `build-anim/inject.py --check` `ok` ×5 exit 0, and
`grow-anim/inject.py --check` `ok` ×5 exit 0 on the five GROW lessons — nothing was stale
when this started.

### Step-by-step teaching states

`stepstate.mjs` presses ▶ Next once per step on every stage and records which parts carry
which motion, which labels are up, the narration text, the pose, the verdict, the spotlight
and the follower count. Motion class names are normalised across the two engines
(`glow-path`↔`g-glow`, `highlight-region`↔`g-hi`, `fade-rest`↔`g-fade`,
`pulse-answer`↔`g-pulse`, `reveal-label`↔`g-labelled`, …); anything unmapped is reported
verbatim so it shows up as a difference rather than being dropped.

**160 stage-steps compared. 127 identical (79.4%). All 33 differences are one thing:** the
`draw` verb. `build-anim` adds `ba-drew` to the part element; `grow-anim` puts `g-draw` on
the part's child shapes and marks the part only by removing `g-hidden`. Different mechanism,
same visible result — see the visibility census below. Nothing else differs: not one
narration string, pose, label, verdict, spotlight or follower count.

### Print packs

Byte-for-byte identical. All three tiers on all five lessons: 11 sections visible, 0 empty,
and the total visible character count matches exactly.

| lesson | supported | standard | stretch |
|---|---|---|---|
| W3 | 4425 → 4425 | 4185 → 4185 | 4199 → 4199 |
| W4 | 4373 → 4373 | 4115 → 4115 | 4169 → 4169 |
| W5 | 4167 → 4167 | 3906 → 3906 | 3964 → 3964 |
| W6 | 4280 → 4280 | 4021 → 4021 | 4064 → 4064 |
| W7 | 4181 → 4181 | 3930 → 3930 | 3943 → 3943 |

### `prefers-reduced-motion`

Measured in a Chromium context with `reducedMotion: 'reduce'`, all stages driven to their
last step, then every `[data-part]` checked for computed visibility and for a live animation.

| lesson | parts still hidden | parts still animating |
|---|---|---|
| W3 | 9 → **0** | 10 → **0** |
| W4 | 19 → **0** | 19 → **0** |
| W5 | 36 → **10** | 26 → **0** |
| W6 | 46 → **14** | 32 → **0** |
| W7 | 25 → **0** | 25 → **0** |

Reduced motion is **strictly better** after: nothing animates anywhere, and far less stays
hidden.

The residual 10 (W5) and 14 (W6) are not a reduced-motion problem. They are
`food-svg.js`'s `HIDE_CSS` parts (`[data-part^="food-"]`, `[data-part^="drop-"]`) that no
script in those lessons ever reveals. Running the same measurement with animation **on** and
a 3-second settle gives exactly the same names and exactly the same counts — 10 and 14 —
both before and after. A teacher clicking through normally has never seen them either.

### Console errors and 404s

One per lesson, before and after, identical: `file:///hud.js :: net::ERR_FILE_NOT_FOUND`.
That is the site-wide `<script defer src="/hud.js">`, which resolves against the filesystem
root when a lesson is opened from `file://` and is present on GitHub Pages. No other console
error, no page error, no other failed request on any of the 60 slides.

### Renders

60 PNGs at 1280×720, one per slide: `reports/convergence/<lesson>/slide-NN.png`. Every slide
was pixel-compared against the same slide rendered from `main`:

- mean difference **2.43%**, median **1.23%**
- 10 of 60 slides differ by more than 5%
- the 9 largest are all slide 6 or slide 7 — the prediction panel and the comparison rail —
  and all are Finding 3, the `frame="tall"` size change
- 4 slides are pixel-identical

Two artefacts of the harness, not of the lessons: the progress label reads "Title • 1/12" on
every shot because the screenshot driver toggles `.slide.active` directly rather than going
through `showSlide()`; and the fixed navigation bar overlaps the foot of the stage on every
shot in both runs equally.

---

## Noted in passing, not acted on

- **`pop` on a hide-gated part does nothing in either engine.** `food-svg.js`'s `HIDE_CSS`
  reveals on `.ba-fadein, .ba-drew, .g-in, .g-draw`; `pop` sets `ba-pop` / `g-draw-pop` on a
  wrapper and none of those. There are 4 such steps in the unit today. Their parts are shown
  by other steps as well, so nothing is currently invisible because of it — but a future
  script that reaches for `pop` alone on a `drop-`/`food-` part will get silence.
- **`draw` on a hide-gated part would regress under the converged engine.** `HIDE_CSS`
  lists `.g-draw` as an ON class, but grow's `draw` never puts `g-draw` on the part — only on
  its children. There are **0** such steps today (checked: 23 `draw` steps in the unit, none
  targeting a `drop-`/`food-` name), so this is latent, not live.
- `build-anim/demo.html` still loads `build-anim.js` and `bio-svg.js` by `<script src>`. It
  is not a lesson and was not touched, but it is the one page that would actually break on
  deletion.
- Two of three `frame` sizes differ between the engines (Finding 3). Making them agree is a
  two-line CSS change; deciding *which* value is right is a teaching judgement, not a
  refactor.

---

## What this branch is for

It is the experiment written down. It is **not** a proposal to merge: merging it would put
the XP drop and the rail-caption clipping into five live lessons to buy nothing the current
lessons do not already do.

The order that makes deletion safe:

1. Escape `</script`/`</style` in `grow-anim/inject.py` (Finding 1). Without this, inlining
   compat silently produces a dead lesson.
2. Decide the `.ba-pc` question (Finding 2) — either have `compat-build-anim.js` add the old
   classes to elements the engine builds, or change the five lessons' glue to count `.g-pc`.
3. Reconcile `frame` sizes (Finding 3).
4. Optionally: narration in `all()` (Finding 4) and `list()` scope (Finding 5). Neither
   affects a lesson as taught.
5. Re-run this branch's harness. When findings 1–3 are closed, `build-anim/` can go — except
   `demo.html`, which needs rehoming first.

## Reproducing

```bash
git checkout claude/convergence-prep
python3 reports/convergence/inject_convergence.py --check Science_Teesside/Build/SCI_B_W*.html
node reports/convergence/audit.mjs     --label after --out /tmp/after.json --shots /tmp/shots
node reports/convergence/stepstate.mjs --out /tmp/steps-after.json
```

For the control, run the same two harnesses with `main` checked out. Playwright resolves
from `/opt/node22/lib/node_modules` by default; override with `PLAYWRIGHT_PATH`.
