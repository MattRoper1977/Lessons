# ASDAN Teach — the BUILD_ASDAN visual teaching layer

A shared visual and interaction layer for the 31 BUILD_ASDAN lesson decks. It
exists to make the decks **teach visually** rather than display text: to guide
where a class looks, to build ideas in sequence rather than all at once, and to
cut how much has to be read before a lesson can start.

It changes **presentation only**. No lesson wording, task instruction, answer,
learning outcome or assessment text is touched — and that is enforced by a test,
not by good intentions (see *Content integrity*, below).

---

## Files

| File | What it is |
|---|---|
| `asdan-teach.css` | The visual layer. **Source of truth — edit this.** |
| `asdan-teach.js` | The interaction layer. **Source of truth — edit this.** |
| `apply_framework.py` | Injects both into every deck. Idempotent. |
| `qa_check.py` | Proves content is unchanged and the layer is current. |
| `smoke_test.js` | Drives the interactions teachers rely on (needs Playwright). |
| `style_check.js` | Proves a change is visually inert — computed styles + geometry. |
| `contrast_check.js` | Measures text contrast on every slide. Reports; does not gate. |
| `prune_dead_css.py` | One-off cleanup: removes CSS no deck can ever match. |

## Making a change

```bash
# 1 · edit the source
$EDITOR _framework/asdan-teach.css

# 2 · roll it into all 31 decks
python3 _framework/apply_framework.py

# 3 · prove nothing broke
python3 _framework/qa_check.py
node    _framework/smoke_test.js */[A-Z]*.html
```

`smoke_test.js` runs 26 checks per deck and skips anything that is not a deck,
so the glob above can stay as it is — it also matches each strand's
`START_HERE.html`.

Never edit the injected block inside a lesson file — the next
`apply_framework.py` run will overwrite it.

Other commands:

```bash
python3 _framework/apply_framework.py --check   # report drift, change nothing
python3 _framework/apply_framework.py --strip   # remove the layer entirely
```

---

## Why injected, not linked

Every deck in this suite is a single self-contained `.html` file. Teachers open
them off laptops, USB sticks and shared drives as well as from the site, so an
external `<link>`/`<script>` would break any deck that is not being served.

Injection keeps each deck standalone while still giving the suite one place to
edit. The injected blocks are fenced by HTML comment markers:

```html
<!-- ASDAN-TEACH:CSS:START … --> … <!-- ASDAN-TEACH:CSS:END -->
<!-- ASDAN-TEACH:JS:START  … --> … <!-- ASDAN-TEACH:JS:END  -->
```

CSS goes last in `<head>` so it can build on each deck's own styles. JS goes
last in `<body>` so the deck's own functions already exist to wrap.

---

## Two rules the layer keeps

**No new colours.** Every colour resolves from the per-subject `:root` tokens
each deck already declares — `--lo-border`, `--ido-border`, `--wedo-border`,
`--task-border`, `--success`, `--error`, `--muted`. All five subjects declare the
same variable names with their own approved values, so the layer restyles itself
per subject with nothing hardcoded. A new subject palette restyles it for free.

Where a colour has to come from somewhere more specific — the three
differentiation levels, for instance — it is read off the element the lesson
already coloured, rather than written down here.

**No JavaScript is load-bearing.** Every deck must still teach correctly with
`asdan-teach.js` deleted. The JS wraps existing lesson functions rather than
replacing them, so timers, print packs, cold call, the match game and slide
navigation keep working either way. Anything the layer animates is CSS keyed off
`.slide.active`, so content cannot be stranded invisible if a script fails.

---

## Content integrity

`qa_check.py` strips the injected blocks from each deck and compares the result,
byte for byte, against a recorded baseline. If that passes, the layer cannot have
altered a single character of lesson content.

```
$ python3 _framework/qa_check.py
Checked 31 decks against recorded baseline

PASS · lesson content byte-identical in all decks
PASS · current framework present in all decks
```

Run it before every commit. It exits non-zero on failure so it can gate one. It
does catch things — changing one word of a lesson's spark line fails it.

The baseline lives in `.content-baseline.json` so the gate needs no network and
no git ref. Re-record it **only** when deck content changes deliberately, and say
why in the commit message:

```bash
python3 _framework/qa_check.py --rebaseline
python3 _framework/qa_check.py --against origin/main   # or compare to a git ref
```

---

## What the layer provides

**Attention utilities** — `.at-reveal` / `.at-in`, `.at-stagger`, `.at-dim-siblings`
+ `.at-focused`, `.at-pulse`, `.at-draw`, `.at-confirm`. Compose these rather
than writing one-off animations; anything added here should be usable by more
than one lesson.

**Slide build** — slides arrive in reading order over about half a second, so a
class's attention lands where the teacher is speaking instead of on the whole
slide at once.

**Today at a Glance** — the `.product-grid` card rail on the Starter slide. Every
deck emitted this markup; no deck ever styled it.

**The I Do step build** — the 186 `.v5-step`s are the one place the decks already
teach in sequence, so most of the attention work lives here. Each step carries
its number; the step the teacher has just revealed takes the zone colour and a
solid marker while earlier ones keep an outlined marker and a pale edge; the
explanation follows its heading by a quarter of a second; a row of pips fills as
steps come out. Earlier steps are never dimmed — a class refers back to them.

The revealed step is also scrolled into view. Measured on a 1440×900 screen,
**all 31 I Do slides are 256–345 px taller than the space they have** once all
three steps are out, so without this the step the teacher has just revealed
lands below the fold. Confirmed visible at 1440, 1024 and 390 px wide.

**The illuminator** — the I Do diagram's caption waits for the build to finish
(timed from each lesson's own SVG delays), and a Replay control re-runs it.

**Labels that wait for their shape** — 94 of the 225 `<text>` elements in the 31
diagrams carry no animation, so they painted at t=0: "¼ CARBS" on an empty white
plate for two seconds before the wedge it names arrived. Each is paired with the
animated shape it sits inside (smallest containing, so the most specific) or the
nearest, and held until that shape settles. 75 labels now wait; every delay is
measured off the deck's own SVG. A diagram whose animation only loops has no
build to wait for and is left alone.

**Draw-on that actually draws** — every deck declares `.ilm .draw` with a
hardcoded `stroke-dasharray:260` against a keyframe animating the offset 260→0.
The 13 paths using it measure **20 to 119 units** — all shorter than the dash, so
a short one slid inside its first dash and a long one stayed invisible for half
its animation then appeared from the wrong end. **None of them had ever drawn.**
Each path is now measured and animated against its real length.

**The We Do activities** — face-down prediction cards, answers numbered back to
the card that produced them, a match grid sized to its real number of targets,
and confirmation by tick as well as by colour.

**Success looks like** — the three "I can …" lines on every title slide read as a
checklist rather than as prose. The boxes are empty on purpose: this is what
success will look like by the end, not what has been achieved.

**The Lundy four** — Space, Voice, Audience, Influence arrive in the model's own
order, and each row lines up whatever length its text runs to, so the grid reads
as a four-part structure rather than four unrelated notes.

**Accessibility** — the card activities are `<div onclick>` in the lesson markup;
the layer promotes them to buttons in the accessibility tree with Enter/Space,
and makes score, feedback, step position and slide position announce politely.
Every animation resolves instantly under `prefers-reduced-motion` with nothing
left hidden — held labels are present, undrawn lines are drawn.

---

## Contrast

`contrast_check.js` measures every text element on every slide, with answers
revealed and every I Do step out, compositing each translucent layer down to the
page to get the real background. It **reports rather than gates**, because almost
everything it finds is an approved brand colour used as text — a palette
decision, and not one this layer gets to make.

```
$ node _framework/contrast_check.js <strand>/[A-Z]*.html
measured 5589 text elements across 31 decks
652 below WCAG AA, in 58 distinct patterns
```

Run it after any change and compare the patterns. **The layer must not add a
new one.** What it currently finds, all of it pre-existing lesson or brand
styling:

| Pattern | Ratio | What it is |
|---|---|---|
| `🖨 Supported pack` / `Standard pack` | 2.28 / 2.80 | white on `--btn-bg`, the subject's own button colour, 93 each |
| `🤝 With support` / `👤 On your own` | 2.00 / 2.46 | the three level colours, set inline by each lesson |
| Lundy headings | 2.09–4.47 | each box's colour, set inline by each lesson |
| `.slide-tag.tag-lesson`, `.country-badge` | 2.22–4.47 | white on a zone colour — established house style |
| `.v5-step-label`, `✓ All revealed` | 2.58–4.07 | the deck's own `.v5-step-controls` styling |
| `Success looks like` | 2.00–2.08 | `--sc-border` on `--sc-bg`, inline in every deck |

Two the layer *did* own, and fixed inside the palette: the Replay control and
the step number now take the deck's body ink with the zone colour on the ring
instead of on the text — zone-on-white measured 2.9–4.0:1 across the five
subject palettes, and both are chrome that has to read from the back of a room.
Replay is also sized to a 36 px target.

---

## Known, left alone deliberately

- **Zone token contrast.** None of the four zone colours clears 4.5:1 against
  white (they run 2.2–4.2:1). The decks already use white-on-zone-colour for
  `.slide-tag` and `.wedo-capture`, so it is established house style and the
  layer follows it rather than overruling a branding decision. The layer does
  not *add* new small text in a zone colour. Worth a look if the palette is ever
  revisited — the table above is the evidence to look at.
- **`.pres-cap` text colour** is a hardcoded indigo inherited from the Art
  template the decks were cloned from, rather than a subject token, so it is the
  one element that does not follow its deck's palette. Left as-is: changing it is
  a palette decision, not a layout one.
- **SVG geometry.** A few illuminator SVGs draw slightly outside their `viewBox`
  and crowd the caption. That is per-lesson artwork, not a layer concern.
- **Diagram height.** The illuminators are 560×190 viewBoxes stretched to the
  slide width, so on a 1440×900 screen each is 1199×407 — half the slide's usable
  height. Capping the width would free 100–130 px but shrinks the artwork on a
  projector, and it is the referent for everything below it. Scrolling the
  revealed step into view solves the problem the height was causing without
  touching the artwork; the size itself is a judgement call for whoever owns it.
- **Illuminators that only loop.** Four decks (`CAREERS_W2`, `CAREERS_W3`,
  `COMM_W3`, `COMM_W4`) animate entirely with infinite `glow`/`ride`/`spin`, so
  there is no build for a label to wait for and nothing arrives in sequence.
  Staging them would be a real gain, but the author chose a continuous animation
  there and the layer does not second-guess that. Worth a decision, not a guess.

---

## Proving a change is invisible

`style_check.js` records, for every element on every slide of every deck, the
computed values of the properties that decide how it looks plus its position and
size — 310 slide signatures. Snapshot, make the change, compare.

```bash
node _framework/style_check.js --save    */[A-Z]*.html
# … make the change …
node _framework/style_check.js --compare */[A-Z]*.html
```

This replaced an earlier screenshot-diffing version, which was not a usable
oracle: two renders of an *unchanged* page disagreed on 138 of 310 slides,
because each slide carries a live countdown and because emoji rasterisation is
timing-dependent. Computed styles have neither problem.

It is how the dead-CSS prune was shown to be inert: 2666 selectors removed, all
310 signatures unchanged.

It runs under `prefers-reduced-motion`, which makes it the right oracle for a
change that is *meant* to be seen. Anything purely motion should come back
clean; anything that also changes layout should come back with a count you
predicted before you ran it. The step build and reveal work, for instance,
changed exactly **124 of 310** signatures — the Title, both I Do and the Lundy
slide of every deck, and nothing else — matching the four components it touched.
A number you cannot account for in advance is a bug, not a baseline to re-record.

### One trap when you assert on opacity

Reading `getComputedStyle(el).opacity` to prove something is not stranded
invisible **does not work in the task that revealed it, and does not work after
two `requestAnimationFrame`s either.** A freshly created CSS animation sits at
`currentTime: 0` with `playState: "running"` until a real frame ticks, so the
element reports its from-state — opacity 0 — even under
`prefers-reduced-motion`, where the duration is 0.01 ms and it will be fully
opaque the instant it starts.

This cost a round of false positives: 93 of 186 viewport sweeps "failed" on a
step that was fine, and the animation involved was `fadeInUp`, which the decks
have always had. Wait ~80 ms of real time, or check `el.getAnimations()[0]
.currentTime` before believing an opacity.
