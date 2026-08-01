# Convergence — closing pass, evidence v3

**Branch:** `claude/convergence-prep` (PR #12) · **base:** `main` at `cacaf16977646b40f0ff72c9e5112a7f31877679`
**DO NOT MERGE. `build-anim/` is not deleted** — `git diff --stat main -- build-anim/` is empty.

---

# WALK SHEET — for a room, not a browser

**Walk the slides at the scaling the room is actually set to.** That is the whole
instruction. Everything below is measured in Chromium at nominal scaling, and a
classroom is usually not at nominal scaling.

- **Check it in ten seconds:** right-click the desktop → Display settings → *Scale
  and layout*. Windows-key + I → System → Display gets you to the same place.
- **125% is a common default on school hardware.** Assume it is on until you have
  looked, not off.
- **At 125%, a We Do 2 stage sits under the navigation bar on all five BUILD decks
  — today, on `main`, before any of this work.** It is worse on `main` than on this
  branch. The walk is where that gets seen for the first time, because no test in
  the estate has ever run at a scaled viewport until this pass.

**The one question no harness can answer: does a 256px plate read from the back row?**

## What to do

**Stand at the back of the room, on the actual projector, and look at slides 4 and 9.**
Slide 4 is the first I Do — the biggest picture in the deck and the one that shrank
most. Slide 9 is We Do 2 — the tightest layout in the unit. If the pictures read from
the back on those two, they read everywhere.

## The six stages with the least room

These clear the fixed navigation by **10px** — the tightest anywhere as authored.
Any projector overscan or font difference shows up here first.

| deck | slide | stage | viewport |
|---|---|---|---|
| `SCI_B_W5_Right_Nutrition` | 9 · We Do 2 | `wedo2-rule` | 1280×720 |
| `SCI_B_W6_Balanced_Plate` | 9 · We Do 2 | `wedo2-rule` | 1280×720 |
| `SCI_B_W7_Where_Food_Comes_From` | 9 · We Do 2 | `wedo2-rule` | 1280×720 |
| `SCI_B_W4_Muscle_Pairs` | 9 · We Do 2 | `wedo2-rule` | 1024×768 |
| `SCI_B_W6_Balanced_Plate` | 9 · We Do 2 | `wedo2-rule` | 1024×768 |
| `SCI_B_W7_Where_Food_Comes_From` | 9 · We Do 2 | `wedo2-rule` | 1024×768 |

Also worth a look: **W6 slide 4** (`ido1-plate`), the picture that shrank most —
326px → 256px — and **W4 slide 7** (`wedo1b-rail`), the comparison rail the whole
frame argument started on.

**On the heading margin, so "5 characters" is not read as an alarm.** The threshold
at which a heading pushes a stage off the slide is 57 characters. The longest real
heading in the ten decks is 52 — but it is on a *different slide of a different
deck*. The headings on the slides that actually fail are **33, 19 and 12**
characters, so their own margins are 113, 55 and 45. **The 5 is what would remain if
the estate's longest heading were moved onto its tightest slide.** Nothing is
currently close; the lint exists so nothing drifts there unnoticed.

## What the measurements did NOT cover

Stated plainly so the walk is not treated as a formality:

- **Chromium**, not the projector's browser.
- **Nominal viewports**, plus four Windows-scaling viewports (see below) — no other
  scaling, and no browser zoom.
- **No projector overscan.** A projector that crops 2–3% of the edges is not
  simulated by any cell here, and 10px of clearance does not survive it.
- **Container fonts.** `system-ui` resolves to whatever this container has. A room
  resolving it to a wider or taller face is not this measurement — though see the
  `bigfont` fixture, which tests whether the mechanism absorbs that.

## If it fails in the room

Every picture in the unit is capped by `min(intent, measured fit)`. The intent side
is four numbers at the top of `grow-anim/grow-anim.css`:

```css
--g-frame-default: .46;   --g-frame-wide: .34;
--g-frame-mini:    .20;   --g-frame-tall: .58;
```

**Lower the one that matches the frame on the offending stage.** Every picture using
that frame across all ten lessons gets smaller — the change is deliberately global,
because a per-slide exception is how a motion language stops being a language. Then
re-run `node reports/convergence/tests/run.mjs` and re-inject.

**Do not lower `FLOOR` in `grow-anim/grow-anim.js:620`** to fix a layout complaint —
that is the point below which a picture stops being an explanation, and the reason
is written next to it.

---

## JOB 0 — the reserve is derived, not tuned

`--g-chrome-reserve: 150px` is gone. There is no reserve constant.

A picture is now capped twice, and the two caps mean different things:

- **The frame factor is intent** — how big a picture of this kind should ever be,
  as a fraction of the viewport. A design decision, and a constant: default .46 ·
  wide .34 · mini .20 · tall .58.
- **`--g-fit` is fact** — measured, per stage, at run time: the distance from the
  top of *this* picture to whichever comes first, the fixed navigation or the
  foot of the slide, minus whatever this stage draws underneath the picture.

`max-height: min(calc(var(--g-frame-tall) * 100vh), var(--g-fit, 100vh))` —
never bigger than intended, never bigger than fits.

`grow-anim/grow-anim.js` measures it (`usableBottom()`, `belowPicture()`, `fit()`)
and re-measures on every repaint, on resize, on orientation change, and through a
`ResizeObserver` on the stage and its slide — which is also how a slide becoming
visible triggers a fit without anything having to announce it. A caption that
wraps to two lines now pushes the **picture** down rather than pushing itself
under the buttons.

Two numbers remain, and both are breathing space rather than prediction:

```js
var GAP = 8;       // between the last thing a stage draws and the chrome
var FLOOR = 96;    // below this a picture is decoration, not an explanation
```

**Two bugs found while building this**, both by the widened test rather than by
reading:

1. `fit()` ran at the *start* of `paint()`, so it measured the layout `paint` was
   about to replace — `paint` updates the dot count, the button labels and the
   narration, any of which can wrap the control bar and push the picture down.
   Measured: `--g-fit` settled at 346px when the correct answer was 324px, and
   the stage overflowed its slide by 1px. Moved to the end of `paint`.
2. One pass was not always enough — resizing the picture moves what is under it.
   `fit()` now re-enters up to three times and stops when the answer moves by
   less than 1.5px. Two passes suffice in every case measured; three is the guard.

---

## JOB 1 — the test now points at everything

Test 4 previously covered one stage at three viewports. It now covers **every
stage in all five BUILD lessons at five viewports, under three fixtures**: as
authored, with every rail caption forced to wrap, and with every slide heading
forced long enough to wrap.

**1,080 cells across nine viewports, four fixtures and every stage of the five BUILD
lessons. 900 carry a measurable stage.**

Nominal and scaled viewports are asserted separately, because a room at 100% and the
same room at 125% are not the same measurement and folding them together hides which
one is failing.

| fixture | nominal (1280×720, 1366×768, 1920×1080, 1024×768) | worst | scaled (see Job 1b) | worst | phone 390×844 | worst |
|---|---|---:|---|---:|---|---:|
| as authored | **100/100** | **+10px** | 70/100 | −241px | 24/25 | −14px |
| caption wraps to two lines | **100/100** | **+8px** | 70/100 | −256px | 20/25 | −58px |
| heading wraps long | 97/100 | −25px | 53/100 | −352px | 19/25 | −127px |
| root font 16px → 20px | 95/100 | −63px | 59/100 | −366px | 20/25 | −181px |

**Worst clearance anywhere in the set: −366px**, on `W7_Where_Food_Comes_From /
wedo2-rule` at 683×512 (1024×768 at 150%) under the larger-font fixture, offending
element `.g-canvas`.

**Four assertions fail and are reported failing** — the three scaled fixtures and
nominal + long heading. None is turned green.

The assertion that tests the mechanism rather than the outcome passes:

> **when a slide overflows, the picture is never the offender** — PASS.
> 173 cells of 1,080 overflow; **173 of 173 have the picture already shrunk to its
> 96px floor.**

So in every failing cell the engine has already done everything it can and what
overflows is the text above the picture. Dropping the floor to ~62px would make the
nominal long-heading cells pass, and a 62px picture is decoration. The honest answer
is that a three-line heading on a We Do 2 slide does not fit a 720px projector, and
that is an authoring constraint, not a layout bug — now enforced by a lint, below.

The phone column is asserted separately and deliberately weaker: a phone scrolls as a
matter of course and `.slide` is `overflow-y: auto`, so content below the fold is
reachable. **One as-authored phone failure remains and is not dismissed:**
`W7_Where_Food_Comes_From / wedo2-rule` at 390×844, −14px, picture at the floor.

### The heading-length guardrail

The red long-heading test documents a design limit, so the limit is now written down
and linted rather than left to chance. Bisecting the actual threshold
(`reports/convergence/headingthreshold.mjs`) on the three cells that go red:

| deck | stage | viewport | heading length at which clearance drops below 8px |
|---|---|---|---:|
| `W5_Right_Nutrition` | `wedo2-rule` | 1280×720 | 146 chars |
| `W6_Balanced_Plate` | `wedo2-rule` | 1280×720 | 74 chars |
| `W7_Where_Food_Comes_From` | `wedo2-rule` | 1024×768 | **57 chars** |

**Threshold: 57 characters.** The longest real heading in the ten Autumn 1 decks is
**52** — *"Evidence loop — describe it without saying "healthy""*, `SCI_B_W6_Balanced_Plate`,
slide 8. **Margin: 5 characters.**

That margin is the conservative reading, and worth stating precisely: the 52-character
heading is on a different slide of a different deck from the 57-character threshold.
On the slides that actually fail — the We Do 2 slides themselves — the real headings
are *"Match the animal to what it needs"* (33), *"Sort the statements"* (19) and
*"Put it right"* (12), so the per-slide margins are 113, 55 and 45 characters. **No
real heading is close to its own threshold.** The 5-character figure is what would
remain if the longest heading in the estate were moved onto the tightest slide.

`reports/convergence/tests/run.mjs` now lints every slide heading in all ten decks
against 57 characters, so the failing case cannot be authored by accident:

```
PASS  no slide heading reaches the overflow threshold
      threshold 57 chars; longest real heading 52 (…) — margin 5 chars
```

**The 96px floor does not move without Matt's say-so**, and the reason is annotated
beside the constant at `grow-anim/grow-anim.js:620`.

Raw matrix: `reports/convergence/_data/clearance-matrix.json`.
Full run: `reports/convergence/_data/testrun-final.txt`. **23 of 27 tests pass**; the four failures are the clearance assertions above, left red on purpose.

---

## JOB 1b — display scaling: a genuine finding, reported not patched

**OS display scaling changes the CSS viewport, and none of the original 25 cells used
a scaled one.** Windows at 125% turns a 1024×768 room into an 819×614 page; at 150%
into 683×512. Those are ordinary classroom configurations and they were unmeasured.

Measured, as authored, no adversarial fixture, all 30 stages of the five BUILD
lessons — `main` against this branch, same probe on both trees:

| viewport | scaling | `main` clear | **this branch** | `main` worst | **branch worst** | regressions |
|---|---|---|---|---:|---:|---:|
| 1024×768 | 100% | 20/25 | **25/25** | −159px | **+10px** | **0** |
| 819×614 | 1024×768 @125% | 5/25 | **20/25** | −226px | **−123px** | **0** |
| 1093×614 | 1366×768 @125% | 7/25 | **20/25** | −319px | **−71px** | **0** |
| 683×512 | 1024×768 @150% | **0/25** | **5/25** | −319px | **−241px** | **0** |

**Yes, a scaled cell puts content under the navigation.** At 125% every `wedo2-rule`
stage in all five lessons fails; at 150% twenty of thirty stages do. Per the brief
this outranks everything else in this pass, so it is **reported and not patched**.

Three things qualify it, all measured rather than argued:

1. **Zero regressions at any scaled viewport.** Not one cell that clears on `main`
   fails on this branch.
2. **`main` is far worse.** At 819×614 it clears 5 of 25 stages; this branch clears
   20. At 683×512 `main` clears none at all.
3. **The picture is never the offender** — in all 173 overflowing cells across the
   whole extended matrix the picture is already at its 96px floor. At 512px of
   viewport height a slide is ~460px tall and the heading and control bar alone
   consume most of it. No picture size fixes that; the decks would need shorter
   slides.

### A bug in the fitting mechanism, found by cross-checking two probes

Two probes disagreed by 37px on one cell — `W7 / wedo2-rule @1024×768` read +10px in
the matrix and −27px in the scaled probe. The difference was that one called
`GrowAnim.fit()` explicitly first. Investigating that showed `--g-fit` was **never
set at all** on that stage:

```
preFit=false  clearance=-27px  --g-fit=(empty)
preFit=true   clearance= 10px  --g-fit=116px
```

`wedo2-rule` carries `data-ba-nobar`, and `paint()` began
`var st = stage._g, bar = $('.g-bar', stage); if (!st || !bar) return;` — so the
`fit()` call at the end of `paint` was never reached on any bar-less stage. Those
stages had only the `ResizeObserver` as a backstop, which does fire but
asynchronously: a visible reflow in the room, and invisible to any synchronous
check. `paint()` is now split so the fit runs regardless of whether a bar exists,
and both probes agree.

This was a defect in Job 0's own deliverable rather than a content limit, so it was
fixed rather than reported — the alternative was shipping a mechanism that does not
run on a whole class of stages while the evidence claims it does. Every number in
this document is from after that fix.

### Does the derived reserve absorb a larger default font?

**Partly, and the honest answer is no, not fully.** A `bigfont` fixture raises the
root font from 16px to 20px. Because the reserve is derived from measured chrome —
the nav's real rect, the caption's real height, the picture's real top — a larger
font pushes the picture down and the fit shrinks it to compensate, and on most
stages that is exactly what happens. It does **not** hold on `wedo2-rule`, where the
picture is already at the floor and there is nothing left to give: at 1280×720 the
five `wedo2-rule` stages go from +10px to between −9px and −63px.

So the mechanism converts a font change into a smaller picture rather than a
clipped caption **until the floor is reached**, and after that it cannot.

### What remains genuinely unmeasurable

- **Projector overscan.** A projector cropping 2–3% of the edges is not simulated by
  any cell here. The six stages clearing by 10px would not survive it.
- **`system-ui` resolving to a different face.** The `bigfont` fixture tests size,
  not shape; a face with different metrics is not the same test.

---

## JOB 1c — the We Do 2 slide: fixed by arrangement

### It was pre-existing, and it was never only about scaling

Stated before any number. The single-column We Do 2 slide needs **932–1069px of
viewport height** depending on width — measured by bisection, every width, every
deck (`reports/convergence/_data/breakpoint-derivation.json`). Only 1920×1080
provides it. So on `main`, today, the slide overflows its own scrollport at every
other viewport:

| viewport | overflow on `main` |
|---|---|
| 1920×1080 | 0 |
| 1280×720 | **106–120px** |
| 1024×768 | **72–120px** |
| 819×614 (1024×768 @125%) | **168–255px** |

The earlier clearance matrix never caught the two nominal rows because it asserted
that *the stage* clears the navigation, not that *the slide* fits. Rule 1 again: a
measurement adjacent to the claim is not the claim.

### The threshold is derived

`reports/convergence/breakpoint.mjs` bisects, for every width in the matrix and
every deck, the viewport height at which the single column stops fitting:

| width | worst deck needs |
|---:|---:|
| 1920 | 932px |
| 1536 | 932px |
| 1366 | 935px |
| 1280 | 953px |
| 1093 | 953px |
| 1024 | 1005px |
| 819 | 1029px |
| 683 | 1069px |

Against the real viewports that puts the single column's **failures at heights
512–864 and its only success at 1080**, so a single `max-height` breakpoint must
satisfy **864 < T ≤ 1079**. **T = 960**, the middle of the admissible band — the
most robust point against a viewport not in the set.

### The arrangement, and the two things measurement corrected

Below the threshold the same eleven elements sit in two columns: the sort activity
keeps the width, the picture takes the narrow column. **Nothing is removed,
reworded, or hidden behind interaction.**

Two wrong turns, both caught by measuring rather than reasoning:

1. **An even split made it worse everywhere** — 819×614 overflow went from 168–255px
   to 200–374px. The sort activity is width-hungry; narrowing its bins costs more
   height than a second column saves. A picture is the one element that scales, so
   it takes the narrow column. Three ratios were then measured; 55% is the only one
   that clears every nominal viewport.
2. **`.slide.wedo2-layout { display: grid }` outranks the deck's own
   `.slide { display: none }`**, so the We Do 2 slide was never hidden and shared the
   flex row with whichever slide was showing. Measured: every other slide's width
   halved from 742px to 403px and every picture collapsed to its 96px floor. Scoping
   to `.slide.wedo2-layout.active` fixed it. This was invisible in the overflow
   numbers — they looked *better* — and only showed up as unrelated stages failing
   the clearance matrix.

### What it achieved

Whole-slide fit — does the slide need scrolling at all:

| viewport | `main` | **this branch** |
|---|---|---|
| 1920×1080 | 0 | **0** |
| 1280×720 | 106–120px | **0 on all five** |
| 1024×768 | 72–120px | **0 on all five** |
| 819×614 | 168–255px | **70–153px** |

Stage clearance — does anything the stage draws sit under the navigation, across
the full nine-viewport matrix, every stage, five lessons:

| fixture | nominal | worst | scaled | worst | phone |
|---|---|---:|---|---:|---|
| as authored | **100/100** | **+20px** | **80/100** | −103px | **25/25** |
| caption wraps | **100/100** | **+20px** | 78/100 | −176px | 24/25 |
| heading wraps | **100/100** | **+20px** | 56/100 | −213px | 24/25 |
| font 16→20px | **100/100** | **+20px** | 64/100 | −195px | 24/25 |

As authored, by scaled viewport:

| viewport | scaling | stages clear |
|---|---|---|
| 819×614 | 1024×768 @125% | **25/25 — no failures** |
| 1093×614 | 1366×768 @125% | **25/25 — no failures** |
| 1536×864 | 1920×1080 @125% | **25/25 — no failures** |
| 683×512 | 1024×768 @150% | 5/25 — all fifteen stage types |

**At 125% display scaling every stage now clears, on every deck.** Only 150%
still fails, and there the fault is not the stage: all 125 overflowing cells in the
matrix have the picture already at its 96px floor.

### The five constraints

| constraint | held |
|---|---|
| 1 · no content removed, reworded or hidden behind interaction | **yes** — the eleven elements are the same eleven, all visible |
| 2 · slide count 12/12, titles position-for-position | **yes** — re-measured, all five decks |
| 3 · the 96px picture floor does not move | **yes** — `FLOOR = 96` unchanged, and at 819×614 the binding constraint is the sort bins, not the picture |
| 4 · the heading-length threshold does not move | **yes** — 57 chars, lint still passing |
| 5 · nominal viewports not disturbed unless improved | **improved** — 1280×720 and 1024×768 go from 106–120px of overflow to 0 |

### What is left, and what would have to give

At **819×614 the slide still scrolls by 70–153px** even though every stage clears.
The last grid row — the scaffold box and the end-of-period note — sits below the
fold. Closing that needs one of: a thirteenth slide, the sort bins reflowed to two
rows of two, or the end-of-period note moved to the following slide. **All three
change what a pupil sees or where, so all three are Matt's.**

At **683×512 (150% scaling) nothing in the layout layer helps.** The slide has
~460px for content that needs 1069px.

## JOB 2 — the GROW five, re-injected and measured

`python3 grow-anim/inject.py Science_Teesside/Grow/SCI_G_*.html` — five updates,
+9,232 bytes each. `--check` is now clean on **all ten lessons, exit 0**:

```
grow-anim/inject.py --check          ok ×5   (SCI_G_W3…W7)
inject_convergence.py --check        ok ×5   (SCI_B_W3…W7)
```

Every invariant measured before and after the re-injection:

| lesson | slides | titles | script steps | zero-match | `[data-part]` | print packs | reduced motion | console |
|---|---|---|---|---:|---|---|---|---|
| `SCI_G_W3_Friction` | 10 → 10 | same | 47 → 47 | 0 | 50 → 50 | identical 4701/4414/4429 | 15 hidden, 0 animating | 2 (pre-existing) |
| `SCI_G_W4_Mechanisms` | 10 → 10 | same | 44 → 44 | 0 | 49 → 49 | identical 4633/4335/4371 | 15 hidden, 0 animating | 2 |
| `SCI_G_W5_Fair_Test` | 10 → 10 | same | 56 → 56 | 0 | 54 → 54 | identical 4693/4405/4437 | 9 hidden, 0 animating | 2 |
| `SCI_G_W6_Earth_And_Planets` | 10 → 10 | same | 65 → 65 | 0 | 59 → 59 | identical 4502/4207/4262 | 6 hidden, **3 "animating"** | 2 |
| `SCI_G_W7_The_Moon` | 10 → 10 | same | 71 → 71 | 0 | 95 → 95 | identical 4606/4300/4314 | 12 hidden, 0 animating | 2 |

The two console entries per GROW lesson are the same `/hud.js` 404 counted twice
(once absolute, once relative to the folder). Identical before and after.

**Reported, not fixed** — the brief says a sixth finding does not get fixed inside
a closing pass:

> `.g-flow-orbit` is missing from `grow-motion.css`'s `prefers-reduced-motion`
> list, while `.g-flow`, `.g-flow-drift` and `.g-flow-jiggle` are all in it. On
> `SCI_G_W6_Earth_And_Planets` three parts — `earth`, `mars`, `jupiter` — still
> report a running `gOrbit` animation under reduced motion. Their computed
> duration is **0.00001s**, so nothing perceptibly moves, and the count is
> identical before and after this pass. It is a pre-existing one-word gap in the
> GROW library, not a convergence regression, and it is also the reason the
> "0 animating everywhere" assertion is not literally true.

---

## JOB 3 — the pixel-diff story, constrained

The v2 claim was: slides that moved are the ones carrying a stage; slides that are
pixel-identical are the ones carrying none. Tested as a partition:

**As stated, it is FALSE.**

```
slides 60   moved 35   identical 25   withStage 30   stageless 30
moved      == set-with-stages?      false
identical  == set-without-stages?   false
```

Five slides belong to neither side, and they are the same slide in every lesson:

| slide | difference | what it carries |
|---|---:|---|
| `SCI_B_W3_Backbones/slide-03.png` | 2.852% | `.ba-key` |
| `SCI_B_W4_Muscle_Pairs/slide-03.png` | 2.868% | `.ba-key` |
| `SCI_B_W5_Right_Nutrition/slide-03.png` | 2.852% | `.ba-key` |
| `SCI_B_W6_Balanced_Plate/slide-03.png` | 2.852% | `.ba-key` |
| `SCI_B_W7_Where_Food_Comes_From/slide-03.png` | 2.852% | `.ba-key` |

Slide 3 is "Today at a Glance" and it carries the **motion-key panel**, which the
engine builds even though it is not a stage. The narrative was near-right and
wrong in a specific, checkable way: the predicate is not "carries a stage", it is
"carries anything the engine builds".

**Under the corrected predicate the partition is exact:**

```
withEngineComponent 35   without 25
moved      == engine-built?      true
identical  == not-engine-built?  true
movedButNoEngineComponent:   none
engineComponentButIdentical: none
```

35 moved = 35 engine-built. 25 identical = 25 not built by the engine. Zero
exceptions in either direction. Data: `reports/convergence/_data/pixel-sets.json`.

---

## JOB 4 — for Matt: the explanation is smaller, by this much

Both READMEs open with "the animation is the explanation". Measured, not adjusted:

| stage | viewport | `main` | this branch | change |
|---|---|---:|---:|---:|
| W4 `ido1-arm` (plain stage) | 1280×720 | 326px | 308px | **−18px (−5.5%)** |
| W4 `ido1-arm` | 1366×768 | 348px | 348px | **unchanged** |
| W4 `wedo1b-rail` (comparison rail) | 1280×720 | 312px | 295px | **−17px (−5.4%)** |
| W4 `wedo1b-rail` | 1366×768 | 333px | 337px | **+4px** |
| W6 `ido1-plate` (default frame) | 1280×720 | 326px | 256px | **−70px (−21%)** |
| W6 `ido1-plate` | 1366×768 | 348px | 308px | **−40px (−11.5%)** |

Renders: `reports/convergence/_pictures/{W4-arm,W4-rail,W6-plate}--{1280x720,1366x768}--{main,after}.png`.

Two things are his call and nothing here compensates for them. The picture only
shrinks where it had to — at 1366×768 two of the three are unchanged or slightly
larger, because the derived fit only binds when there is genuinely no room. And
W6 `ido1-plate` at 1280×720, the biggest loss at −21%, is the case where `main`
overflows the slide by 20px: on `main` that plate is bigger *and* cut off.

### Carried forward, unresolved and unchanged by this pass

- **The BUILD/GROW philosophy divergence.** One engine now, two stated intents —
  BUILD's "the animation is the explanation" against GROW's "animation that
  supports reasoning, not animation that explains" (PR #10). Nothing in this
  branch resolves which one the shared engine is for.
- **The circulation asset is still unexercised by any lesson.** No script step in
  either suite targets it.

---

## Gates

| gate | result |
|---|---|
| 1 · nothing merged, nothing on `main`, `build-anim/` untouched | **pass** — `git diff main -- build-anim/` is 0 lines; `main` = `origin/main` = `cacaf16` |
| 2 · `audit.mjs` / `stepstate.mjs` unchanged except additive coverage | **pass** — `stepstate.mjs` byte-identical; `audit.mjs` +6 −2, the diff is below |
| · scaled matrix run in full, worst re-reported | **pass** — four scaled viewports added, −366px |
| · the 117/120 test still failing, threshold documented | **pass** — four clearance assertions red; threshold 57 chars, linted |
| · `.g-flow-orbit` recorded, not fixed here | **pass** — `reports/REDUCED_MOTION_REGISTER.md` RM-1; `grow-motion.css` unchanged |
| · PR correction stated, attributed upstream | **pass** — `reports/SESSION_CLOSE.md`, first section |
| 3 · Job 1 matrix complete, worst clearance quoted | **pass** — 1,080 cells across 9 viewports × 4 fixtures, worst −366px |
| 4 · `inject.py --check` clean on all ten | **pass** — exit 0 both injectors |
| 5 · renders captured, six assertions re-measured | **pass with a correction** — 110, not 120: GROW decks are 10 slides |
| 6 · derived reserve, not a bare 150 | **pass** — derived; no reserve constant remains |

The whole of gate 2's diff to `audit.mjs`:

```diff
-const LESSONS = [
+/* The BUILD five, which is what v1 and v2 measured and what the before/after
+   comparison depends on. --lessons points the same harness at another set (the
+   GROW five) without changing anything it measures; omitting it reproduces v1
+   and v2 exactly. */
+const LESSONS = (arg('lessons', null) || [
   …
-];
+].join(',')).split(',').filter(Boolean);
```

### The six re-assertions, re-measured

1. **Print packs byte-for-byte identical** — all three tiers, all ten lessons.
   BUILD: 4425/4185/4199 · 4373/4115/4169 · 4167/3906/3964 · 4280/4021/4064 ·
   4181/3930/3943. GROW: 4701/4414/4429 · 4633/4335/4371 · 4693/4405/4437 ·
   4502/4207/4262 · 4606/4300/4314. Zero empty sections.
2. **Slide counts and titles** — BUILD 12/12 ×5, GROW 10/10 ×5, every `data-title`
   matching `main` position-for-position on all ten.
3. **`prefers-reduced-motion`: 0 parts animating** on all five BUILD lessons
   (`main` was 10/19/26/32/25) and on four of five GROW lessons. The exception is
   GROW W6's three orbit parts at a 0.00001s duration, unchanged from `main` and
   documented above.
4. **Console** — BUILD one `/hud.js` 404 per lesson, GROW two, nothing else, no
   page error, across all 110 slides. Identical before and after.
5. **The W5/W6 always-invisible parts unchanged at 10 and 14.**
6. **Script-step target resolution** — BUILD 72/76/77/82/80 and GROW 47/44/56/65/71,
   **672 resolutions, 0 matching zero elements**, and per-name totals identical to
   `main` on all five BUILD lessons.

---

## Reproducing

```bash
git checkout claude/convergence-prep
node    reports/convergence/tests/run.mjs              # 24/25; the matrix takes ~3 min
python3 reports/convergence/tests/script_census.py     # 0 live hazards
python3 grow-anim/inject.py            --check Science_Teesside/Grow/SCI_G_*.html
python3 reports/convergence/inject_convergence.py --check Science_Teesside/Build/SCI_B_W*.html
node    reports/convergence/pixelsets.mjs <main-renders> reports/convergence
node    reports/convergence/pictureheight.mjs after reports/convergence/_pictures
```
