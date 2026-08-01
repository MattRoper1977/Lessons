# GROW Animation Framework · v1.0

A reusable set of **motion primitives**, **layered SVG science assets** and **teaching
behaviours** for the GROW science suite.

The point is not decoration. The point is that **the animation is the explanation**.
Movement explains, teacher narration reinforces, and a short label confirms *after*
the idea has landed — so the amount of reading a pupil has to do to follow the
lesson drops close to zero.

> If a concept can be shown, don't tell it.

The question this framework answers is not "how do we animate friction?" It is
"what reusable components do we need so that every science topic can teach through
movement?" Every new lesson is composed from behaviours that already exist and have
already been tested in a classroom — and pupils learn the language of the interface
as well as the science.

---

## What's in the box

| File | Phase | What it is |
|---|---|---|
| `grow-motion.css` | 1 | The ten movements. The punctuation of the whole suite. |
| `grow-svg.js` | 2 | Asset registry + the drawing kit assets are built from. |
| `grow-svg-bio.js` | 2 | Biology: skeleton, cell, heart, circulation, lungs, digestion, food chain, plant, DNA. |
| `grow-svg-bio-animals.js` | 2 | Biology: 13 animals for classification — fish, human, snake, bird, dog, frog, crab, spider, worm, snail, jellyfish, beetle, octopus. |
| `grow-svg-phy.js` | 2 | Physics: forces, friction, lever, pulley, gears, fair test, Solar System, day/night, Moon phases, circuit, light, waves, particles, heating. |
| `grow-svg-chem.js` | 2 | Chemistry: atom, ion, bonding, reaction, dissolving, burning, neutralisation, electrolysis. |
| `grow-anim.js` | 3–11 | The engine: reveal, We-Do, prediction, overlays, dual, retrieval, misconception, story. |
| `grow-anim.css` | 3–11 | The furniture those behaviours need. |
| `grow-polish.css` / `.js` | 12 | Lighting, depth, parallax, particles, micro-interactions. Optional. |
| `demo.html` | — | **Open this first.** Living reference — every asset, every phase, copy-paste snippets. |
| `compat-build-anim.js` | — | Makes existing BUILD lesson markup run on this engine unchanged. |
| `inject.py` | — | Inlines the library into single-file lessons so they still work offline. |
| `wire_lessons.py` | — | Puts the teaching behaviours on the right slides of the GROW lessons, and applies small idempotent repairs to the lesson's own deck code. |

---

## Phase 1 — the motion language

Ten movements. Each means **exactly one thing**, in every subject, all year. Pupils are
never taught this table; they absorb it, because it never changes. Print it and put it
on the wall in week one — or drop `<div class="g-key"></div>` on a slide and the
framework renders it.

| Motion | Class | Verb | Meaning to the pupil |
|---|---|---|---|
| Draw | `.g-draw` | `draw` | A structure is forming |
| Glow | `.g-glow` | `glow` | This is the important feature |
| Pulse | `.g-pulse` | `pulse` | Pay attention — look here now |
| Fade | `.g-fade` | `fade` | This matters less right now |
| Morph | `.g-morph-*` | `morph` | Something is **changing** |
| Flow | `.g-flow*` | `flow` | Something is **moving** |
| Shake | `.g-shake` | `shake` | That idea is incorrect |
| Bounce | `.g-bounce` | `bounce` | That answer is correct |
| Trace | `.g-trace` | `trace` | Follow this pathway |
| Zoom | `.g-zoom-layer` | `zoom` | We are going in close |

Supporting marks (stage directions, not meanings): `show hide hi unhi only spot
unspot label unlabel tick cross think unthink note wait`.
Teaching verbs: `pause overlay unoverlay heat`.

`grow-motion.css` works with **zero JavaScript** — add the class, get the meaning. The
engine exists only to *sequence* these, never to redefine them. Shake is reserved for
wrong and bounce for right; nothing else in the suite may use them.

---

## Phase 2 — the SVG science library

Nothing is a picture. **Everything is layers.** Every structure a teacher might want to
draw, glow, fade, morph, trace or zoom on its own is its own `<g data-part="name">`.
That single decision is what turns a diagram into a teaching instrument, and it is why
this phase is worth more than any of the animation code.

Each asset ships with the scripts it needs:

| Script | Used by | What it is |
|---|---|---|
| `@teach` | I Do | The full teaching sequence |
| `@reveal` | We Do | The short answer sequence, after a class vote |
| `@process` | Phase 5 | The scientific process actually running |
| `@wrong` / `@right` | Phase 10 | The misconception, then the correction |
| `@retrieve` | Phase 9 | Animated recall |

```js
GrowSVG.render('circuit')          // '<svg …>…</svg>'
GrowSVG.script('circuit', 'teach') // the teaching script
GrowSVG.list('physics')            // ['forces', 'friction', …]
```

---

## Using it in a lesson

### 1. Include it

```html
<link rel="stylesheet" href="/grow-anim/grow-motion.css">
<link rel="stylesheet" href="/grow-anim/grow-anim.css">
<link rel="stylesheet" href="/grow-anim/grow-polish.css">   <!-- optional -->
<script src="/grow-anim/grow-svg.js"></script>
<script src="/grow-anim/grow-svg-bio.js"></script>
<script src="/grow-anim/grow-svg-phy.js"></script>
<script src="/grow-anim/grow-svg-chem.js"></script>
<script src="/grow-anim/grow-anim.js"></script>
<script src="/grow-anim/grow-polish.js"></script>           <!-- optional -->
```

For a lesson that must run from a USB stick, use `inject.py` instead — the files get
inlined between markers and the lesson stays a single self-contained file.

### 2. Drop in a stage (Phase 3)

```html
<div class="g-stage" data-grow-asset="circuit" data-grow-script="@teach"></div>
```

The teacher presses **▶ Next**; one step fires; they narrate the line the framework
prints for them. Pupils cannot read ahead, because nothing has been written yet.

### 3. Let the text follow the picture

Anything on the slide carrying `data-grow-step="n"` appears at step *n* — so the
definition confirms the idea only once the animation has made it.

```html
<div data-grow-step="6" data-grow-for="s1"><b>circuit</b> — a complete loop…</div>
```

### 4. Switch on the invisible (Phase 6)

```html
<div class="g-stage" data-grow-asset="forces"
     data-grow-overlays="force,friction,gravity,reaction,energy"></div>
```

Nothing physical changes when a layer comes on — pupils simply see more. That
experience *is* the lesson, which is why the scene is drawn once and never redrawn.

### 5. Run a We-Do (Phase 4)

```html
<div class="g-wedo" data-grow-asset="circuit"
     data-grow-q="Will the lamp light?"
     data-grow-options="Yes|No|Only if the loop is complete"
     data-grow-discuss="Turn and talk. Give a REASON, not a guess."
     data-grow-explain="Current only flows when the loop is complete."
     data-grow-check="Draw one circuit that works and one that cannot."></div>
```

Question → Prediction → Discussion → Animation → Explanation → Check. Each move
unlocks the next, so nothing can be skim-read ahead of the class.

### 6. The other behaviours

```html
<!-- Phase 8 · real world | scientific model, one script, never out of step -->
<div class="g-stage" data-grow-dual="forces:REAL WORLD|states:MODEL" …></div>

<!-- Phase 9 · the picture builds, stops, and waits for the class to say what's next -->
<div class="g-retrieve" data-grow-asset="foodchain" data-grow-script="@retrieve"
     data-grow-stop="2" data-grow-cue="Say the next organism."></div>

<!-- Phase 10 · animate the misconception honestly, then correct it -->
<div class="g-misc" data-grow-asset="forces"
     data-grow-claim="Pushing a box? That's one force."
     data-grow-wrong="@wrong" data-grow-right="@right"></div>

<!-- Phase 11 · the story spine; each slide declares data-grow-beat="0..4" -->
<div class="g-story" data-grow-story="Question|Investigation|Discovery|Explanation|Application"></div>
```

---

## Writing a script

One line = one press of ▶ Next.

```
[beat] verb targets + verb targets :: what the teacher says out loud

observe: show ground, person, box    :: Somebody pushing a box.
think:   pause "How many forces?"    :: Hold up fingers.
notice:  overlay force + pulse box   :: One. The push.
notice:  overlay friction            :: And a second one, pushing back.
explain: label push                  :: Four forces. They were always there.
```

The optional beat prefix (`observe notice think explain label apply`) shows the
teacher which of the five moves they are on.

**Targets** are part names, comma-separated. `morph ice>water` for a change.
`body#2` addresses the second panel of a rail or a dual stage. `heat solid 2.4`
sets how hard particles vibrate (0–3).

**Prediction pauses.** `pause "…"` stops the animation dead and asks. The deck's own
Next button becomes the reveal — press once to stop and ask, press again to show.
It never simply does nothing.

---

## Navigation

The framework wraps the lesson's own `nextSlide()` and `showSlide()`. One press of
**Next ▶** first advances any unfinished stage on the current slide, then moves on.
The teacher never has to think about which Next they mean. Moving to a slide resets
its stages, so a lesson taught twice in a day starts clean both times.

---

## Accessibility, print and offline

- Every asset carries a real `aria-label` describing what a sighted pupil sees.
- `prefers-reduced-motion` switches every animation off and leaves every part
  **visible** — a pupil who cannot tolerate motion loses the animation, never the
  content.
- Printing forces all layers and labels on and hides the teacher furniture, so a
  worksheet shows the finished diagram.
- `inject.py` keeps lessons single-file, so they run from a USB stick with no network.

---

## Maintaining it

```bash
python3 grow-anim/inject.py         Science_Teesside/Grow/*.html   # refresh the library
python3 grow-anim/wire_lessons.py   Science_Teesside/Grow/*.html   # refresh the wiring
python3 grow-anim/inject.py --check Science_Teesside/Grow/*.html   # CI / pre-commit
```

Both scripts are idempotent and marker-based: they replace what is between their
markers and never touch anything else. A fix made once here reaches every lesson.
Existing lesson content is added to, never removed.

`wire_lessons.py` fills eight slots per lesson — story spine, motion key, I Do
stage, We-Do frame, misconception engine, dual representation, process animation
and retrieval — and applies the repairs listed in its `PATCHES` table. Each patch
is explained where it is declared and is a no-op once applied. `--patch-only`
applies just those repairs, so they can be rolled across the ~240 lessons in the
estate that have no GROW wiring but share the same deck code:

```bash
python3 grow-anim/wire_lessons.py --patch-only <lesson>.html
```

One of those repairs is the **HUD loader**. The Live-Teach HUD is site-level
furniture served from the root of the estate, so `/hud.js` is right when a lesson
is served and unreachable when one is opened off a USB stick. The loader keeps
the served behaviour byte-for-byte identical — one request to `/hud.js`, no
fallback — and adds a relative fallback so copying `hud.js` next to the lessons
makes the HUD work offline too. With neither present it fails silently and the
lesson is unaffected.

---

## Relationship to `build-anim/`

There is now **one engine**. `build-anim/` was a second codebase doing the same
job for the BUILD pathway; its thirteen animal assets have been ported into
`grow-svg-bio-animals.js`, and `compat-build-anim.js` makes every piece of
existing BUILD lesson markup run against this engine unchanged:

```html
<script src="/grow-anim/grow-svg.js"></script>
<script src="/grow-anim/grow-svg-bio-animals.js"></script>
<script src="/grow-anim/grow-anim.js"></script>
<script src="/grow-anim/compat-build-anim.js"></script>
```

The shim provides `window.BuildAnim` and `window.BioSVG`, translates `.ba-stage`,
`.ba-predict`, `.ba-key` and every `data-ba-*` attribute to its GROW equivalent,
and keeps `dim`/`undim` alive as aliases of `fade`/`unfade`. No BUILD lesson had
to be rewritten. Once the BUILD lessons have been re-injected against
`grow-anim/`, `build-anim/build-anim.js`, `build-anim.css` and `bio-svg.js` can
be deleted and the shim retired with them.

A fix to a motion, a verb or a shape is now made **once** and reaches both
suites — which was the point of sharing the grammar in the first place.

---

## Validated

Framework and all five GROW lessons exercised in headless Chromium:
every asset renders with layers; every script verb and target resolves against its
own asset; every motion applies and every reset clears; prediction pauses block and
release correctly; all five decks navigate end to end with the lesson's own controls,
with the existing XP, timer, Cold Call and print behaviour intact.
