# BUILD Animation Framework · v1.0

A reusable set of **layered SVG assets**, **CSS motion primitives** and **JavaScript
helpers** for BUILD-pathway science lessons.

The point is not decoration. The point is that **the animation is the explanation**.
Movement explains, teacher narration reinforces, and a short label confirms *after*
the idea has landed — so the amount of reading a pupil has to do to follow the
lesson drops close to zero.

> If a concept can be shown, don't tell it.

---

## What's in the box

| File | What it is |
|---|---|
| `build-anim.css` | The motion primitives. Every animation the framework can do. |
| `bio-svg.js` | The layered biology asset library (13 animals, each part animatable on its own). |
| `build-anim.js` | The engine: scripts, teacher-controlled stepping, prediction panels, comparison rails. |
| `demo.html` | Living reference — every asset, every primitive, copy-paste snippets. **Open this first.** |
| `inject.py` | Inlines the three files into a single-file lesson so it still works offline from a USB stick. |

---

## Motion vocabulary

Every movement means one thing, every time. Pupils pick this up without being
taught it — as long as it stays consistent across the whole curriculum.

| Movement | Verb | Meaning to the pupil |
|---|---|---|
| Draw | `draw` | A structure is forming |
| Pop, one by one | `pop` | Count these — they are separate parts |
| Glow | `glow` | This is the important feature |
| Colour change | `hi` | THIS is the one we are testing for |
| Pulse | `pulse` | Look here now |
| Fade | `dim` / `only` | This matters less right now |
| Spotlight | `spot` | Everything except this is switched off |
| Zoom | `zoom` | We are going in close |
| Trace | `trace` | Follow this pathway |
| Bounce | `bounce` | Correct |
| Shake | `shake` | Not that one — a common mistake |
| Three dots | `think` | We are waiting for **your** answer |
| ✓ / ✖ | `tick` / `cross` | The answer lands |

Also available: `show` `hide` `unglow` `unhi` `undim` `unpulse` `unspot` `unzoom`
`label` `unlabel` `unthink` `note` `wait`.

---

## Using it in a lesson

### 1. Include it

```html
<link rel="stylesheet" href="/build-anim/build-anim.css">
<script src="/build-anim/bio-svg.js"></script>
<script src="/build-anim/build-anim.js"></script>
```

For a lesson that must run offline, use `inject.py` instead (see below) — the
three files get inlined between markers and the lesson stays a single file.

### 2. Drop in a stage

```html
<div class="ba-stage" id="fish1" data-ba-asset="fish" data-ba-script="@teach"></div>
```

`@teach` runs the teaching sequence that ships with the asset. `@reveal` runs the
short answer sequence used after a class vote. Or write your own:

```html
<div class="ba-stage" data-ba-asset="crab" data-ba-script="
  show body,shell,legs   :: A crab.
  glow shell + hi shell  :: The hard bit is on the OUTSIDE.
  label shell            :: Hard case outside.
  show nobone + cross    :: Down the middle — nothing.
  label kind             :: No backbone → invertebrate.
"></div>
```

One line = one click of ▶ Next. `verb targets`, joined with `+` when several
things happen at once, then `::` and the sentence the teacher says out loud.
The framework prints that sentence in the control bar as a prompt.

### 3. Let the text follow the picture

Anything on the same slide carrying `data-ba-step="n"` appears at step *n* — so
the definition confirms the idea only once the animation has made it.

```html
<div data-ba-step="5" data-ba-for="fish1"><b>backbone</b> — a line of small bones down the middle of the back.</div>
```

`data-ba-for` is only needed when a slide has more than one stage.

### 4. Prediction panel — pupils commit before the reveal

```html
<div class="ba-predict" data-ba-animals="bird:Robin, worm:Earthworm, frog:Frog, octopus:Octopus"></div>
```

Tap an animal → three dots → take the class vote → press Next → the answer builds
itself. Pupils cannot read ahead, because there is nothing to read.

### 5. Comparison rail — pupils discover the shared feature

```html
<div class="ba-stage" data-ba-rail="human:Human, fish:Fish, snake:Snake, bird:Bird" data-ba-script="
  show body#1 :: A human.
  show body#2 :: A fish.
  show body#3 :: A snake.
  show body#4 :: A bird.
  draw skull,ribs,pelvis,limbs + pop spine :: Now look inside all four.
  glow spine + hi spine  :: What is the SAME in every one?
"></div>
```

`part#2` addresses the second animal along; a bare `part` addresses all of them.

---

## Teacher control

The engine wraps the lesson's own `nextSlide()`. Pressing **→ / space / Next ▶**
advances the *animation* first; only once a stage has run out of steps does the
same key move to the next slide. The class stays with the explanation instead of
jumping ahead.

Every stage also has **⏭ Show all** (skip to the end) and **↺ Replay** (start
again — useful for re-teaching or for a pupil who missed it). Stages reset
automatically when you return to a slide.

---

## Asset library

| Vertebrates | Invertebrates |
|---|---|
| `fish` `human` `snake` `bird` `dog` `frog` | `crab` `spider` `worm` `snail` `jellyfish` `beetle` `octopus` |

Every asset is built from the same named layers, so scripts port between them:

`body` · `skull` · `spine` · `ribs` · `pelvis` · `limbs` · `shell` · `legs` ·
`soft` · `nobone`

`nobone` is the deliberately-empty dashed midline on invertebrates: the pupil
looks where a backbone would be and sees that there is nothing there.

Colours come from the school palette (`#4E7A9B` bone, `#C9803B` hard case,
grey soft tissue). The framework never sets brand colour — only motion.

---

## JavaScript helpers

```js
drawSkeleton(stage)            // skull + ribs + pelvis + limbs, then vertebrae pop
highlightBone(stage,'spine')   // glow + colour change
traceBackbone(stage)           // dashes travel along the spine
fadeOthers(stage,'spine')      // everything else drops back
zoomFeature(stage,'spine')     // go in close
revealLabels(stage)            // show every label at once
pulseCorrect(el) / shakeWrong(el)   // feedback on any HTML element

BuildAnim.next(stage) / .reset(stage) / .all(stage)
BuildAnim.load(stage,'octopus','reveal')  // swap the animal at runtime
BuildAnim.run(stage,'glow','spine')       // fire any verb directly
BuildAnim.advanceActive()                 // used to hook ▶ Next into slide nav
```

---

## Inlining into a single-file lesson

Classroom laptops open lessons straight from a file or a USB stick, so the
lessons stay single-file. `inject.py` keeps that true without copy-paste drift:

```bash
python3 build-anim/inject.py Science_Teesside/Build/SCI_B_W3_Backbones.html
python3 build-anim/inject.py Science_Teesside/Build/*.html      # several at once
python3 build-anim/inject.py --check Science_Teesside/Build/*.html   # CI-style check
```

It replaces whatever sits between the `BUILD-ANIM:*:BEGIN/END` markers with the
current library. Edit the library once, re-run, and every lesson is up to date.
A lesson with no markers is skipped with a warning, never damaged.

---

## Accessibility and printing

* Every SVG carries an `aria-label` describing what a sighted pupil sees.
* Narration lines are exposed in an `aria-live` region as they fire.
* `prefers-reduced-motion` switches every animation off; the content still reveals.
* When printing, all layers and labels are forced visible and the control bars,
  thinking dots and verdict badges are hidden — so a printed slide is a complete
  diagram, not a blank stage.

---

## Adding a new asset

Assets live in `bio-svg.js`. Copy an existing one and change the shapes:

```js
A.newt = {
  title: 'Newt', kind: 'vertebrate',
  alt: 'A newt. Inside it, …',
  svg: function () {
    var sp = curve(function (t) { return [120 + t * 180, 150]; }, 12);
    return g('body', SOFT, shape('…')) +
           g('skull', BONE, shape('…')) +
           g('ribs',  BONE, ribs(sp, 34)) +
           g('spine', BONE, spine(sp, 13, 20)) +
           label('spine', 116, 60, 'BACKBONE', BONE, 200, 140) +
           label('kind',  246, 244, 'VERTEBRATE', BONE, 268, 172);
  },
  teach:  'show body :: A newt.\n…',
  reveal: 'draw skull,ribs :: Look inside.\n…'
};
```

Helpers available inside `svg()`: `g` `shape` `stroke` `path` `ell` `dot`
`vert` `spine` `ribs` `curve` `poly` `label` `nobone`.

Keep the viewBox at `0 0 400 300`, keep labels inside `x = 8…392`, and leave the
top-right corner clear — that is where the ✓ / ✖ badge lands.
