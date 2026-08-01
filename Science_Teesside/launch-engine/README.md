# LAUNCH Scientific Observation Layer

The animation layer for `Science_Teesside/Launch/`. It exists to make one
distinction real in the markup, not just in the scheme of work:

| pathway | pupil's role | animation's role | teacher's role |
|---|---|---|---|
| **BUILD** | learn the concept | **replaces text** — makes the idea visible so there is less to read | guide and narrate |
| **GROW** | explore the concept | **explains a process** — models how the mechanism runs | prompt predictions and discussion |
| **LAUNCH** | think like a scientist | **supports reasoning** — withholds until the pupil has observed, predicted or tested | facilitate enquiry, challenge conclusions |

Before this layer, all three pathways were structurally identical: same ten
slides, same sixteen `v5-step` reveals, same one static SVG, same sort/match/
WAGOLL set. The only difference between BUILD and LAUNCH was the difficulty of
the words. That is a difficulty ladder, not a progression in how pupils work.

---

## The one rule

**Nothing scientific may appear on load, on hover, or on a timer alone.**

Every reveal is gated on an act the pupil performed. `_gate(node, why)` is the
only function that opens anything, and it takes the reason as an argument,
which it writes to `data-sci-opened-by`. You can inspect any revealed element
in a browser and read what earned it:

```
data-sci-opened-by="observed 3 features over 22s"
data-sci-opened-by="all differences found by the class"
data-sci-opened-by="prediction committed: More layers inside them"
```

If you add a component and cannot name the act, the component does not belong
in LAUNCH — it belongs in GROW.

---

## It inherits GROW's motion language

`grow-anim/grow-motion.css` already defines ten movements that mean the same
thing in BUILD, GROW and LAUNCH — glow = important, shake = incorrect,
bounce = correct, flow = moving, and so on. That file is inlined ahead of
`sci-engine.css`, and the engine applies `.g-flow-jiggle`, `.g-draw-pop`,
`.g-bounce` and `.g-in` rather than defining private equivalents.

`check.js` enforces both directions: `sci-engine.css` may not restyle any of the
ten, and the engine may not apply a `.g-` class that `grow-motion.css` does not
define. A pupil arriving from GROW already reads this vocabulary; LAUNCH's
difference is what it *withholds*, not how it moves.

The diffusion simulator's temperature slider drives `--g-heat`, the shared
jiggle's own knob — so a pupil's variable moves the language they already know.

---

## Files

| file | what it is |
|---|---|
| `sci-engine.js` | the engine: components, scenes, simulators, mounting |
| `sci-engine.css` | the stylesheet |
| `payloads.js` | per-lesson content — **pure JSON, no functions** |
| `build.js` | minifies the three sources into `dist/` |
| `dist/` | **committed build output** — what actually goes into the decks |
| `inject.js` | inlines `dist/` + payload into the fifteen decks |
| `check.js` | contract checker — run it before you inject |

### Working on it

```sh
npm install --no-save terser clean-css   # once, only if you change source
node build.js            # minify source into dist/
node check.js            # contracts — must pass before injecting
node inject.js           # inject / re-inject all fifteen lessons
node inject.js --check   # report only
node inject.js --strip   # remove the layer; restores the decks byte-for-byte
```

The decks carry the **minified** build, which keeps the added weight to about
75 KB per deck instead of 120 KB. Readable source — and the reasoning behind
every gate — stays here.

`dist/` is committed so that `inject.js` needs no dependencies: it is the tool
anyone touching a lesson will reach for, and making it need `npm install` would
eventually mean someone hand-edits an injected block instead. A committed
artefact normally rots, so every `dist/` file pins the SHA-256 of its source and
**both `inject.js` and `check.js` refuse to run against a stale build.** Editing
the injected block inside a lesson is pointless either way — the next
`inject.js` overwrites it.

---

## The twelve phases, and where each one lives

| phase | component | what it does |
|---|---|---|
| 1 Observation engine | `observe` | image → *what do you notice?* → pupil marks the figure → **then** zoom → spotlight → label |
| 2 Progressive discovery | `discover` | the diagram is assembled part by part, each part preceded by a question; labels last |
| 3 Zoom framework | `zoom` | leaf → cells → chloroplast → membrane → molecules as one continuous movement, with the field-of-view rule shrinking as you go |
| 4 Investigation animation | `method` | the practical is animated, in order, including the blur before the sharpen |
| 5 Thinking pauses | `pause`, and woven into 2/3/4/7 | the animation stops, a prediction is committed, only then does it continue |
| 6 Evidence before explanation | `chain` | observe → evidence → pattern → conclusion → explanation, each locked behind the last |
| 7 Data visualisation | `graph` | bars grow, the table fills a row at a time, the axis rescales, and it pauses before the final point |
| 8 Interactive models | `model` | pupils drive the variables; the model answers honestly, including when the answer is worse |
| 9 Reasoning animations | `model` + `tradeOff` | the trade-off is asked about before it is stated |
| 10 Comparative investigation | `compare` | two panels driven by ONE control; the explanation unlocks only when every difference is found |
| 11 Scientific storytelling | the spine bar | every component says where it sits: question › evidence › pattern › explanation › application › evaluation |
| 12 Premium interaction | throughout | lens glint, vignette, focus blur, light beam, specimen drift |

### The twelve universal verbs

🔍 zoom · 🎯 spotlight · ✏️ annotate · 📏 measure · ⚖️ compare · 📊 graph ·
🧪 simulate · 🧩 classify · 🔄 transform · 📝 predict · ✅ test · 💡 explain
(plus 👁 observe)

Each component declares which verbs it uses; they render as chips at the top
and light up as the pupil actually uses them. Pupils meet the same twelve
interactions in every lesson, so the interaction stops costing attention and
the science gets it instead.

---

## Traps this layer has already fallen into

Each of these shipped once and was caught. They are listed because every one of
them is **invisible in a screenshot of the finished state**.

1. **`after` vs `anchor`.** The mount anchor is `anchor`. `after` is the pause
   component's follow-up sentence. Using `after` as a selector fed a whole
   English sentence to `querySelector` and threw on nine of fifteen lessons.

2. **Duplicate SVG ids.** A deck holds several copies of the same scene. A
   duplicated `clipPath` id makes `url(#…)` resolve to the first match in the
   document — and when that sits on a `display:none` slide, Chromium silently
   drops the reference. Cells spilled outside the eyepiece circle. Use `uid()`.

3. **Steps that reveal nothing.** The alveolus builder had `parts: []` on every
   step. It asked its questions, ticked itself off, and built nothing.
   `check.js` now fails on an empty `parts`.

4. **Scenes that caption themselves.** The diffusion box printed *"more
   particles here"* — one of the very things the observation engine asks pupils
   to notice. `observe` and `discover` now force `bare: true`, and `check.js`
   fails any scene that still prints text without marking it `sci-neutral`.

5. **A comparison with nothing to compare.** The light/electron panels were the
   same picture with different captions. If you ask pupils to observe a
   difference, the difference has to be in the pixels — hence `detail:'light'`
   vs `detail:'electron'`.

6. **The XP bar.** The deck registers a fixed XP total *before* this layer
   mounts, and `gainXP()` fires level-up and confetti on reaching it. A slider
   awarding XP per drag set off the end-of-lesson celebration during the first
   I Do. All awards now spend from a declared pool (`declareXP`/`xpCost`).

7. **Part ids repeated across scene instances.** Part ids must stay stable
   because payloads name them — but the gas-exchange deck renders the alveolus
   three times (once to build, twice to compare), so stable ids meant four
   duplicate ids in one document. Parts are now addressed by `data-part`, which
   may legally repeat, is scoped to the component's own stage, and is what
   grow-anim already uses. Only generated gradient/clip references use `id`.

8. **`margin-inline:auto` on a grid item.** It switches the item out of stretch
   sizing into fit-content, which for an SVG is its 300px intrinsic default —
   the figure silently collapsed to half size inside `.sci-method`.

---

## What this layer does not touch

- **The print pack.** `REGISTER.md` R-E05 closes the print subsystem. Nothing
  here reads, writes or references `printPack`, `printSection` or `#print-area`.
  The only print CSS is `@media print` rules that stop an on-screen simulator
  printing as a broken widget, and that make locked content legible on paper.
- **Existing slide markup.** The engine finds a slide by `data-title`, finds an
  anchor inside it, and inserts. It never rewrites markup it did not create.
- **Assessed files.** There are none in `Science_Teesside/` — the assessed
  quarantine is in Humanities.

## Honesty

Several models use invented or typical figures. Every one of them carries a
`caveat` line saying so, and `check.js` fails a `graph` that has no caveat.
A model that is wrong in a way pupils cannot see is worse than a diagram.
