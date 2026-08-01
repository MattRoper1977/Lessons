# Convergence fix pass — evidence v2

**Branch:** `claude/convergence-prep` (PR #12) · **base:** `main` at `cacaf16`
**Still DO NOT MERGE. `build-anim/` is still not deleted.** `git diff --stat main -- build-anim/` is empty.

v1 found five things that break when the five BUILD lessons run on the GROW
engine. This pass fixes them, plus **one more that v1 got wrong**, and re-runs the
v1 harness unchanged so the two are comparable.

**Test suite: 8/24 passing before the fixes, 24/24 after.** Every test in
`reports/convergence/tests/run.mjs` was seen failing on the unfixed tree first;
both runs are quoted per fix below.

---

## JOB 0 — the judgement v1 asked to be checked

v1 called the `draw`-verb class-placement difference cosmetic **on the strength of
an aggregate visibility census**. An aggregate cannot clear a per-part claim, so
it was re-measured per instance: every affected part walked through every step of
its own stage, sampling the part's own computed opacity, visibility, display and
laid-out box, on both engines.

### Verdict: **CLEARED**

| lesson | stage | part | steps | samples | laid out in both | invisible in exactly one | opacity/visibility identical |
|---|---|---|---:|---:|---|---|---|
| `W3_Backbones` | `ido1-fish` | `ribs` | 7 | 8 | yes | 0 | 2 differ (fade .15 vs .16) |
| `W3_Backbones` | `ido1-fish` | `skull` | 7 | 8 | yes | 0 | 2 differ (fade .15 vs .16) |
| `W3_Backbones` | `ido2-say` | `limbs` | 7 | 8 | yes | 0 | yes |
| `W3_Backbones` | `ido2-say` | `pelvis` | 7 | 8 | yes | 0 | yes |
| `W3_Backbones` | `ido2-say` | `ribs` | 7 | 8 | yes | 0 | yes |
| `W3_Backbones` | `ido2-say` | `skull` | 7 | 8 | yes | 0 | yes |
| `W3_Backbones` | `wedo1b-rail` | `limbs` | 7 | 16 | yes | 0 | yes |
| `W3_Backbones` | `wedo1b-rail` | `pelvis` | 7 | 16 | yes | 0 | yes |
| `W3_Backbones` | `wedo1b-rail` | `ribs` | 7 | 32 | yes | 0 | yes |
| `W3_Backbones` | `wedo1b-rail` | `skull` | 7 | 32 | yes | 0 | yes |
| `W4_Muscle_Pairs` | `ido1-arm` | `forearm` | 10 | 11 | yes | 0 | yes |
| `W4_Muscle_Pairs` | `ido1-arm` | `humerus` | 10 | 11 | yes | 0 | yes |
| `W6_Balanced_Plate` | `ido1-plate` | `rim` | 9 | 10 | yes | 0 | yes |

**13 part instances, 176 samples. 0 laid out in only one engine. 0 invisible in
only one engine.** The 71 occurrences collapse to these 13 parts because the same
part is re-sampled at every subsequent step and, in a rail, in every cell.

The only paint difference anywhere in those 176 samples is **4 samples where a
faded part reads opacity 0.15 under `build-anim` and 0.16 under `grow-anim`** —
`.fade-rest` against `.g-fade`, two different constants for the same motion. It is
recorded here rather than fixed: it is one hundredth of an opacity step, it is not
the `draw` verb, and picking a number is a design call.

Harness: `reports/convergence/drewcheck.mjs`, data in `_data/drew-{before,after,after-v2}.json`.

### The named suspect: **PROVEN — a real bug, and it was not in v1's list**

`food-svg.js`'s `HIDE_CSS` hides every `drop-`/`food-` part at opacity 0 and
un-hides on one of `.ba-fadein, .ba-drew, .g-in, .g-draw`. `grow-anim`'s `draw`
put `g-draw` only on the part's **child shapes**, never on the part — so the
`.g-draw` entry in that list was dead, and a part revealed by `draw` alone stayed
invisible with the script reporting success. The same family as a gate released by
something that does not happen.

The minimal case, built on each engine and measured (test 1 in the suite):

```
before   build-anim   draw drop-apple -> opacity 1   partClasses="ba-drew"  kidClasses="draw-svg"
         grow-anim    draw drop-apple -> opacity 0   partClasses=""         kidClasses="g-draw"
         FAIL — `draw` left a hide-gated part at opacity 0

after    grow-anim    draw drop-apple -> opacity 1   partClasses="g-draw"   kidClasses="g-draw"
         PASS         (control: drop-pasta revealed by `show` = opacity 1 in both)
```

**Fix.** `grow-anim.js`'s `draw` now adds `g-draw` to the part as well as to its
shapes — the same two-role split `build-anim` had with `draw-svg` on the shapes and
`ba-drew` on the part. `grow-motion.css` gains
`[data-part].g-draw { animation: none; opacity: 1; visibility: visible; }` so the
group carries the marker without also running the stroke animation (which would
inherit `stroke-dasharray` into children that are already animating it), placed
**before** `[data-part].g-hidden` so hiding still wins. `reset()` now clears
`g-draw` from the part, not only from its children.

Why it was live-but-invisible in the lessons today: **0 of the 23 `draw` steps in
the unit target a `drop-`/`food-` name.** Every one of those parts is revealed by
`show` (26 steps) or `pop` (4). The bug was one authoring choice away.

### Consumers of the part-level marker — the full list

| consumer | what it does with it | after convergence |
|---|---|---|
| `build-anim/build-anim.css:105` `.ba-stage [data-part].ba-drew{opacity:1;visibility:visible}` | build-anim's own reveal | dies with `build-anim/`; `[data-part].g-draw` now does the same job |
| `build-anim/food-svg.js:75` `ON = ['.ba-fadein','.ba-drew','.g-in','.g-draw']` | the asset's own visibility gate | **was broken, now works** |
| `build-anim/build-anim.js:368` | `reset()` clears it | dies with `build-anim/` |
| `grow-anim/grow-motion.css:309` | reduced-motion neutralises `.g-draw` | unchanged, applies to shapes and now to the part |
| JS querying it for logic | **none anywhere in the repo** | — |
| print paths | **none** — no print rule references either class | — |
| `check.js` | **does not exist**; the repo has no `check*.js` at any path. The three GitHub workflows are `verify-axiomshift.yml`, `verify-charcoal.yml`, `verify-offbrand.yml` and none reference these classes | — |

---

## JOB 1 — the `</script>` hazard

**This was the fifth time on this estate that the instrument measured something
adjacent to the claim.** `--check` compares the inlined bytes to the source bytes,
which is a true statement about injection and says nothing about whether the
result parses. The lesson loaded, exited 0, and did nothing.

### (a) The escape now lives in the shared injection path

Moved out of `reports/convergence/inject_convergence.py` and into
`grow-anim/inject.py` as `escape_for_inline()`, applied inside `read()` so every
block written by that injector is protected. The convergence injector imports it
rather than keeping a second copy.

The escape is a backslash before the slash — `<\/script`, `<\/style`. Round trip,
run as a check:

```
in : var s = "</script>"; /* </style> */
out: var s = "<\/script>"; /* <\/style> */
round trip (JS sees the same string): True
```

`"<\/script>"` is the identical string to a JavaScript parser (`\/` is just `/`)
and is not a close tag to an HTML one. In CSS it is inert inside a comment or a
string. The five lessons prove it end to end: engine loads, 5 stages built, no
stray `<script src>` — test 2, five lessons, all passing.

### (b) Census of every source either injector can inline

`reports/convergence/tests/script_census.py`, run over 17 sources:

```
Sources an injector can inline:                  17
Sources with no self-closing token at all:       14
LIVE HAZARDS (token can close its element AND
              the injector does not escape):      0
HANDLED OR INERT:                                 7
```

| file:line | token | inlined into | status |
|---|---|---|---|
| `grow-anim/compat-build-anim.js:10` | `</script` | `<script>` | escaped |
| `grow-anim/compat-build-anim.js:11` | `</script` | `<script>` | escaped |
| `grow-anim/compat-build-anim.js:12` | `</script` | `<script>` | escaped |
| `grow-anim/compat-build-anim.js:13` | `</script` | `<script>` | escaped |
| `grow-anim/grow-svg.js:189` | `</style` | `<script>` | inert — cannot close a `<script>` |
| `build-anim/bio-svg.js:581` | `</style` | `<script>` | inert — cannot close a `<script>` |

The census is exhaustive over the injectors' own block tables (`grow-anim/inject.py`
imported directly, `inject_convergence.py` imported directly, `build-anim/inject.py`
transcribed because it must not be touched). It exits 1 if a live hazard appears,
so it can run as a check.

---

## JOB 2 — XP parity

| lesson | main | v1 | **v2** | target |
|---|---:|---:|---:|---:|
| `SCI_B_W3_Backbones` | 13 | 7 | **13** | 13 |
| `SCI_B_W4_Muscle_Pairs` | 9 | 6 | **9** | 9 |
| `SCI_B_W5_Right_Nutrition` | 9 | 6 | **9** | 9 |
| `SCI_B_W6_Balanced_Plate` | 10 | 6 | **10** | 10 |
| `SCI_B_W7_Where_Food_Comes_From` | 10 | 5 | **10** | 10 |

Fixed the way the brief prefers — the glue recognises the shared vocabulary
rather than the engine stamping a legacy class. One character class added per
lesson, outside the injected blocks:

```js
registerXP(document.querySelectorAll('.ba-pc,.g-pc').length)
```

`querySelectorAll` returns each element once, so an element carrying both classes
is not double-counted; the compat shim only ever adds classes to markup already in
the file, and the cards it builds carry `.g-pc` alone.

Test 3, five lessons — before: `xpTotal=7 expected=13`, `6/9`, `6/9`, `6/10`,
`5/10`. After: all five exact.

---

## JOB 3 — the caption under the navigation, and the frame sizes

### (a) The caption — a defect at any size

v1 read this as a frame-size symptom. Measuring it properly showed it is worse
than that, and that two obvious fixes make it worse still:

- Padding the slide does nothing: the slide scrolls, so the caption stays where it
  was and the space appears below it. Measured: caption bottom unchanged at 717.
- Shrinking the slide (reserving the nav strip on `.slide-container`) steals the
  same height from the content it was protecting. Measured: the caption went from
  *under the nav* at 717 to **clipped by the slide's own overflow** at 680 against
  a slide bottom of 679 — invisible until you scroll, which is worse.

What works is capping the picture against the height that is actually usable
rather than against the whole viewport. A stage is never just its picture: it
carries a control bar above and, in a rail, a caption below, and the navigation
covers the last strip of the viewport. `--g-chrome-reserve: 150px` is all of that
together (nav strip 57 + control bar 48 + caption 15 + gaps), and a `tall` frame is
58% of what is left, not 58vh. No layout is reserved and nothing is clipped.

Test 4, three viewports, natural scroll position, asserting both *not under the
nav* and *not clipped by the slide*:

| viewport | nav top | slide bottom | caption bottom before | caption bottom after | verdict |
|---|---:|---:|---:|---:|---|
| 1280 × 720 | 663 | 679 | **717** (under nav; `main` = 636) | **649** | clears by 14px, inside the slide by 30px |
| 1024 × 768 | 711 | 724 | 633 | 633 | already clear, unchanged |
| 390 × 844 | 781 | 796 | 581 | 581 | already clear, unchanged |

This also fixed something v1 never looked at: at 1280×720 on `main`, an ordinary
46vh stage overflows the slide by 20px and the bottom of the slide is cut off.
`reports/convergence/SCI_B_W3_Backbones/slide-05.png` against the same slide on
`main` shows the **Common mistake / Actually** misconception box going from clipped
mid-sentence to fully readable.

### (b) Frame sizes — **the one call made on Matt's behalf**

**GROW's factors are adopted** (default .46 · wide .34 · mini .20 · tall .58),
because one shared language is the point of the convergence. All four live in
custom properties at the top of `grow-anim.css`; reverting is those four values and
nothing else moves.

Rendered three ways at 1280×720, in `reports/convergence/_frames/`:

| slide | set | picture height | stage bottom | caption bottom | verdict (nav top 663, slide bottom 679) |
|---|---|---:|---:|---:|---|
| W4 rail (`tall`) | **grow (adopted)** | 326 | 657 | 649 | clear |
| W4 rail | build factors | 247 | 578 | 571 | clear, noticeably smaller |
| W4 rail | build **absolute** (44vh, reserve 0) | 312 | 643 | 636 | clear |
| W6 plate (default) | **grow (adopted)** | 258 | 631 | — | clear |
| W6 plate | build factors | 258 | 631 | — | clear |
| W6 plate | build absolute (46vh, reserve 0) | 326 | 699 | — | **clipped by the slide** |

Two things worth Matt's eye. "Revert to BUILD's numbers" means two different
pictures: BUILD's *factors* on the new basis (smaller than either engine ever
drew), or BUILD's *absolute* sizes, which need `--g-chrome-reserve: 0px` as well
and put the default frame back over the slide edge. And the single number most
worth tuning is `--g-chrome-reserve`; every picture in the unit scales with it.

---

## JOB 4 — `all()` narration

| lesson | main | v1 | **v2** |
|---|---|---|---|
| `SCI_B_W3_Backbones` | 4/4 | 0/4 | **4/4** |
| `SCI_B_W4_Muscle_Pairs` | 4/4 | 0/4 | **4/4** |
| `SCI_B_W5_Right_Nutrition` | 4/4 | 0/4 | **4/4** |
| `SCI_B_W6_Balanced_Plate` | 4/4 | 0/4 | **4/4** |
| `SCI_B_W7_Where_Food_Comes_From` | 4/4 | 0/4 | **4/4** |

(A prediction panel's stage carries no script until a card is tapped and has
nothing to say; it is excluded, which is why the denominator is 4 and not 5. v1's
count of 5 included it.)

`all()` now sets the narration and the beat badge from the last step it ran, the
same as pressing Next to the end.

**Which path is taught.** Both, and the decks say so. Every stage renders a bar
with three controls — `▶ Start`, `⇥ Show all`, `↺ Replay` — and the lessons script
the Next path explicitly ("Nothing moves until I click", "Do not tell me yet…
When you spot what is the same, hand on your head"). `Show all` is the recovery
control: the teacher who is behind, or who is re-showing a stage a second time. So
this was a break in the *secondary* path — real, and the sort of thing that bites
in the second period when time has run short, but not the path the lesson is
written around. That is the honest priority.

---

## JOB 5 — `BioSVG.list()`

| lesson | main | v1 | **v2** | what is registered |
|---|---:|---:|---:|---|
| `SCI_B_W3_Backbones` | 13 | 13 | **13** | 13 animals |
| `SCI_B_W4_Muscle_Pairs` | 16 | 13 | **16** | + `arm`, `armmodel`, `pullpush` |
| `SCI_B_W5_Right_Nutrition` | 16 | 13 | **16** | + `plate`, `jobs`, `animalfood` |
| `SCI_B_W6_Balanced_Plate` | 16 | 13 | **16** | + `plate`, `jobs`, `animalfood` |
| `SCI_B_W7_Where_Food_Comes_From` | 20 | 13 | **20** | + the seven food-chain assets |

The compat shim mapped `list()` to `GrowSVG.list('animals')`; it now maps to
`GrowSVG.list()`, which is what `build-anim`'s `BioSVG.list()` returned
(`Object.keys(A)`). `vertebrates()` and `invertebrates()` stay tag-scoped and are
unchanged at 6 and 7.

**Consumers of `list()`, and what each lost.** Searched the whole repo:

| consumer | uses | what it lost at 13 |
|---|---|---|
| `build-anim/demo.html:117–122` | `list()`, then subtracts `vertebrates()+invertebrates()` to count the subject libraries | the subtraction went to **0**, so the reference page said "13 layered assets … and 0 from the muscle, nutrition and food-chain libraries" on a lesson carrying 20. The only real consumer, and the count is the whole point of that line |
| the five BUILD lessons | never call it | nothing |
| the five GROW lessons | never call it | nothing |
| print paths | never call it | nothing |
| any check or index | none exists | nothing |

So: one consumer, and it was measurably wrong rather than harmlessly wrong.

---

## JOB 6 — the v1 harness, re-run unchanged

`reports/convergence/audit.mjs` and `reports/convergence/stepstate.mjs` are
byte-identical to the versions that produced v1 (`git diff HEAD` on both is empty).
Nothing about the instrument changed in this pass.

### Delta table — `main` → v1 → **v2**

Every figure that moved:

| figure | main | v1 | **v2** |
|---|---:|---:|---:|
| XP total (W3/W4/W5/W6/W7) | 13/9/9/10/10 | 7/6/6/6/5 | **13/9/9/10/10** |
| `BioSVG.list()` (W3/W4/W5/W6/W7) | 13/16/16/16/20 | 13/13/13/13/13 | **13/16/16/16/20** |
| `all()` stages narrating (per lesson) | 4/4 | 0/4 | **4/4** |
| stage-steps identical to `main` | — | 127/160 (79.4%) | **160/160 (100%)** |
| rail caption bottom @1280×720 | 636 | 717 (under the nav) | **649** |
| `draw` on a hide-gated part | visible | invisible | **visible** |
| `[id]` count per lesson | 52 | 53 | 53 |
| `<svg>` count per lesson | 9/6/5/6/5 | +1 | +1 |
| `.ba-pc` / `.g-pc` | 7/0 | 0/7 | 0/7 |

Every figure that did **not** move between v1 and v2:

| figure | value |
|---|---|
| slides per lesson | 12, all five, all three versions |
| `data-title` strings | identical position-for-position to `main` |
| script-step target resolutions | 72/76/77/82/80 — **387 total, 0 matching zero elements** |
| per-name target totals (`audit.byName`) | identical to `main` on all five lessons |
| `<script>` / `<style>` / `[data-part]` / `[data-label]` / `.print-section` / `.match-pill` counts | unchanged |
| print packs | byte-for-byte identical, all three tiers, all five lessons |
| console | one `/hud.js` 404 per lesson, nothing else, across 60 slides |

The two remaining differences from `main` are the same two v1 documented and both
are `grow-polish.js`'s single motion-blur filter: `#g-mblur`, one extra `[id]` and
one extra `<svg>`. `idsDuplicated` is `[]` on every lesson.

### The six re-assertions

1. **Print packs byte-for-byte identical** on all three tiers of all five lessons —
   11 sections visible, 0 empty, character counts equal to `main` to the byte
   (W3 4425/4185/4199, W4 4373/4115/4169, W5 4167/3906/3964, W6 4280/4021/4064,
   W7 4181/3930/3943).
2. **Slide counts 12/12** on all five, and the twelve `data-title` strings match
   `main` position-for-position on all five.
3. **`prefers-reduced-motion`: parts still animating = 0 on every lesson** (`main`
   was 10/19/26/32/25).
4. **Console: the one pre-existing `/hud.js` 404 per lesson and nothing new**,
   across all 60 slides. No page error, no other failed request.
5. **The W5/W6 always-invisible parts are unchanged at 10 and 14** — the
   `food-svg.js` `HIDE_CSS` parts no script in those lessons reveals, identical
   under animation and under reduced motion, and identical on `main`.
6. **Stage-step comparison: 160/160 identical, up from 127/160.** The 33 differences
   were all the `draw`-verb class placement, and fixing the bug behind it closed
   them. There is no remaining class-level difference between the two engines on
   any step of any stage in the unit.

### Renders

All 60 slide PNGs re-captured at 1280×720 in `reports/convergence/<lesson>/`.
Pixel comparison against the same slides rendered from `main`:

| | v1 | **v2** |
|---|---|---|
| mean difference | 2.43% | **5.52%** |
| median | 1.23% | **2.86%** |
| slides >5% different | 10 | **27** |
| slides pixel-identical | 10 | **25** |

The mean went up and so did the identical count, and both come from the same
change: pictures on stages are smaller (the chrome reserve), which moves a lot of
pixels on the slides that carry one, while the slides that carry none are now
identical to `main` rather than nearly identical. The largest movers are the I Do
and We Do slides — the ones with a stage. `SCI_B_W3_Backbones/slide-05.png` is the
one to look at first: the same slide on `main` has its misconception box cut off
mid-sentence.

---

## Consequences to act on before this can merge

- **The five GROW lessons are now stale.** `grow-anim/` changed, so
  `python3 grow-anim/inject.py --check Science_Teesside/Grow/SCI_G_*.html` reports
  `STALE` ×5 and exits 1. Deliberately not re-injected: that would change five
  lessons this pass was not asked to touch, and the frame-size change would alter
  their layout too. Re-injecting them, walking them, and re-measuring is the next
  piece of work, and it has to happen before any of this lands.
- **`build-anim/demo.html`** still loads `build-anim.js` and `bio-svg.js` by
  `<script src>` and is the one page that genuinely breaks on deletion.
- **The fade constant** — `.fade-rest` 0.15 against `.g-fade` 0.16 — is the only
  paint difference left between the engines. One of the two numbers should go.
- **`pop` on a hide-gated part still does nothing in either engine.** `HIDE_CSS`
  reveals on `.ba-fadein/.ba-drew/.g-in/.g-draw`; `pop` sets `ba-pop`/`g-draw-pop`
  and none of those. 4 such steps exist in the unit and their parts are shown by
  other steps too, so nothing is invisible today. Now the *only* member of that
  family left, since `draw` is fixed.

## Reproducing

```bash
git checkout claude/convergence-prep
node   reports/convergence/tests/run.mjs                 # 24/24
python3 reports/convergence/tests/script_census.py       # 0 live hazards
python3 reports/convergence/inject_convergence.py --check Science_Teesside/Build/SCI_B_W*.html
node   reports/convergence/audit.mjs     --label after-v2 --out /tmp/a.json --shots /tmp/shots
node   reports/convergence/stepstate.mjs --out /tmp/s.json
node   reports/convergence/drewcheck.mjs --out /tmp/d.json
node   reports/convergence/framecompare.mjs
```

For the control, run the same harnesses with `main` checked out. Playwright
resolves from `/opt/node22/lib/node_modules`; override with `PLAYWRIGHT_PATH`.
