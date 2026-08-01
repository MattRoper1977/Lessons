# Convergence — closing pass, evidence v3

**Branch:** `claude/convergence-prep` (PR #12) · **base:** `main` at `cacaf16977646b40f0ff72c9e5112a7f31877679`
**DO NOT MERGE. `build-anim/` is not deleted** — `git diff --stat main -- build-anim/` is empty.

---

# WALK SHEET — what to look hardest at, and why

110 renders in `reports/convergence/<lesson>/slide-NN.png` (60 BUILD across 12 slides,
50 GROW across 10 — the GROW decks are ten slides, not twelve, so the target of
120 was never reachable).

**1 · The three `wedo2-rule` stages that clear by 10px.** These are the tightest
anywhere as authored, and 10px is not much of a margin on a real projector.

| lesson | stage | viewport | clearance |
|---|---|---|---:|
| `W5_Right_Nutrition` | `wedo2-rule` | 1280×720 | **10px** |
| `W6_Balanced_Plate` | `wedo2-rule` | 1280×720 | **10px** |
| `W7_Where_Food_Comes_From` | `wedo2-rule` | 1280×720 | **10px** |
| `W4_Muscle_Pairs` | `wedo2-rule` | 1024×768 | **10px** |
| `W6_Balanced_Plate` | `wedo2-rule` | 1024×768 | **10px** |
| `W7_Where_Food_Comes_From` | `wedo2-rule` | 1024×768 | **10px** |

Slide 9 of W5, W6, W7 and slide 9 of W4. If the room's projector crops even
slightly, these are where it shows first.

**2 · W6 `ido1-plate`, slide 4 — the picture that shrank most.** 326px → 256px at
1280×720, a 21% reduction. It is also the clearest case *for* the change: on
`main` that stage overflows the slide by 20px, so the bottom of the plate was
being cut off. Compare `reports/convergence/_pictures/W6-plate--1280x720--main.png`
with `…--after.png`.

**3 · W4, the slide the whole reserve was tuned on.** `wedo1b-rail`, slide 7 —
this is the comparison rail whose caption started the entire frame-size argument.
It now clears by 20px at 1280×720 and its picture is 295px against `main`'s 312px.
`reports/convergence/SCI_B_W4_Muscle_Pairs/slide-07.png`.

**4 · Slide 3 of every BUILD lesson.** The only slides that moved without carrying
a stage — see Job 3. They carry the motion-key panel, which the engine builds.
Worth thirty seconds to confirm the key still reads correctly.

**5 · The GROW five, all fifty slides**, because they have just been re-injected
against a changed engine for the first time and nobody has looked at them since.

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

**450 cells. 375 carry a measurable stage.**

| fixture | projector viewports (1280×720, 1366×768, 1920×1080, 1024×768) | worst | phone 390×844 | worst |
|---|---|---:|---|---:|
| as-authored | **120/120 clear by ≥8px** | **+10px** | 24/25 | −14px |
| caption wraps to two lines | **120/120 clear by ≥8px** | **+8px** | 20/25 | −58px |
| heading wraps long | 117/120 | **−25px** | 19/25 | −127px |

**Worst clearance anywhere in the set: −127px**, on
`W7_Where_Food_Comes_From / wedo2-rule` at 390×844 under the long-heading
fixture, offending element `.g-canvas`.

**One test fails and is reported as failing:** *whole stage on screen without
scrolling · projector · heading* — 117/120, three cells, all of them
`wedo2-rule`: W5 −19px and W6 −5px at 1280×720, W7 −25px at 1024×768.

The reason it fails is the useful part. A second assertion tests the mechanism
rather than the outcome:

> **when a slide overflows, the picture is never the offender** — PASS.
> 15 cells of 450 overflow; **15 of 15 have the picture already shrunk to its
> 96px floor.**

So in every failing cell the engine has already done everything it can and what
overflows is the text above the picture. Dropping the floor to ~62px would make
those three cells pass, and a 62px picture is decoration. The honest answer is
that a three-line heading on a We Do 2 slide does not fit a 720px projector, and
that is an authoring constraint, not a layout bug.

The phone column is asserted separately and deliberately weaker: a phone scrolls
as a matter of course, and `.slide` is `overflow-y: auto`, so content below the
fold is reachable. **One as-authored phone failure remains and is not dismissed:**
`W7_Where_Food_Comes_From / wedo2-rule` at 390×844, −14px, picture at the floor.

Raw matrix: `reports/convergence/_data/clearance-matrix.json`.
Full run: `reports/convergence/_data/testrun-v3.txt`. **24 of 25 tests pass.**

---

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
| 3 · Job 1 matrix complete, worst clearance quoted | **pass** — 450 cells, worst −127px |
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
