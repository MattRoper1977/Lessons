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
| `contrast_check.js` | Measures text contrast on every slide, writes `CONTRAST_MANIFEST.md`. |
| `label_rest_check.js` | Proves every illuminator label is readable at rest. Gates. |
| `prune_dead_css.py` | One-off cleanup: removes CSS no deck can ever match. |

## Making a change

```bash
# 1 · edit the source
$EDITOR _framework/asdan-teach.css

# 2 · roll it into all 31 decks
python3 _framework/apply_framework.py

# 3 · prove nothing broke
python3 _framework/qa_check.py
node    _framework/smoke_test.js       */[A-Z]*.html
node    _framework/label_rest_check.js */[A-Z]*.html
node    _framework/contrast_check.js --manifest */[A-Z]*.html   # then diff the manifest
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

## Contrast — ruled from a manifest

[`CONTRAST_MANIFEST.md`](../CONTRAST_MANIFEST.md) is the record. `contrast_check.js
--manifest` regenerates it. **Run it after any change to this layer and compare:
the layer must not add a row.**

```
$ node _framework/contrast_check.js --manifest <strand>/[A-Z]*.html
measured 5589 text elements across 31 decks
607 below target, in 66 distinct patterns
failures by role: teaching 205, UI 308, decorative 94
failures by verdict: identity hue 205, UI chrome 308, decorative 94
```

**THE RULING: manifest-led, and identity tokens are not contrast levers.** A
pathway, tier or subject hue *is* the estate's colour language; a contrast fix
that recolours the language is a bigger regression than the thing it fixes. So
the only rows eligible for a fix are pupil-facing text that carries meaning, is
below target, and can be corrected by moving the **ink** — never the hue. On the
current measurement that set is empty: every remaining teaching failure is an
identity hue, named and measured in the manifest. **Decorative failures are
listed and accepted**, so nobody re-raises them in six weeks.

One row qualified and was fixed: "SUCCESS LOOKS LIKE", set in `--sc-border`
inline in all 31 decks, gold at 12.5px on the panel's own cream — 2.00–2.09:1
against a 4.5 target, the worst teaching text in the suite, labelling the three
things a class is asked to collect. The ink moved to the deck's body colour,
13.22–13.32:1. The token is untouched and still carries the panel's identity on
its 6px left border and on the checkboxes. Earlier, and on the same principle:
the Replay control and the step number take body ink with the zone colour on the
ring rather than on the text.

### Three ways this measurement was wrong before, all fixed

Worth reading before trusting any number it prints.

- **Role matched on `tag + ' ' + cls`**, so an element with no class produced a
  trailing space that defeated the anchored tag pattern, and every bare `<h3>`
  and `<p>` — most of what a pupil reads — fell into the UI bucket. Teaching
  failures read as 25. They are 205.
- **Grouping keyed on a rounded ratio**, so unrelated elements sharing a tag and
  a number collapsed into one row that then reported the first member's text and
  size for all of them. It produced "Success looks like ×32 in 25 decks" when 31
  such headings exist in the whole suite. Grouping is by selector, ink,
  background, size, weight and target — the things that define the pattern.
- **The composited chain is not the painted background.** One representative of
  each pattern now has its ink hidden, its box screenshotted and the modal pixel
  taken, which catches gradients and overlays. It moves rows in *both*
  directions; four the chain called failures are cleared by it and are listed at
  the foot of the manifest so nobody re-raises them from a weaker tool.

---

## Known, and ruled — not open questions

- **Identity-hue contrast.** None of the four zone colours clears 4.5:1 against
  white (2.2–4.2:1), and the same holds for the subject strip, the Lundy four and
  the three tier colours. **Ruled: these are not contrast levers.** The decks
  already use white-on-zone-colour for `.slide-tag` and `.wedo-capture`, so it is
  established house style, and the layer follows it rather than overruling a
  branding decision. The layer does not *add* new small text in a zone colour.
  The manifest is the evidence if the palette is ever revisited.
- **`.pres-cap` text colour** is a hardcoded indigo inherited from the Art
  template the decks were cloned from, rather than a subject token, so it is the
  one element that does not follow its deck's palette. Left as-is: changing it is
  a palette decision, not a layout one.
- **SVG geometry.** A few illuminator SVGs draw slightly outside their `viewBox`
  and crowd the caption. That is per-lesson artwork, not a layer concern.
- **Diagram height — ruled: viewport-conditional cap, projector size protected.**
  A fixed width cap is a fixed answer to a variable problem: it takes the same
  100–130px off a projector, where vertical space is abundant, as off a laptop
  where it is not. The cap is the vertical room left over instead —
  `max(190px, calc(100vh - 500px))` — so it engages only where space is scarce.
  The 500px is the largest constant that leaves 1920×1080 untouched, measured.
  Verified: 1920×1080 and 390×844 render **byte-identical** screenshots before and
  after; 1280×720 gives back 140px, 1024×768 gives back 15px. It does not make the
  slide fit and is not meant to — at 1280×720 everything except the diagram
  already totals 679px against 638px visible. Scrolling the revealed step into
  view is what solves that.
- **The four loop decks — ruled: continuous motion is deliberate, staging
  refused.** `CAREERS_W2`, `CAREERS_W3`, `COMM_W3` and `COMM_W4` animate entirely
  with infinite `glow`/`ride`/`spin`. In a careers path and a communication loop
  the cycle *is* the concept; a staged build would teach a sequence that ends,
  which is the wrong idea. **The standard instead is legibility at rest**, gated
  by `label_rest_check.js`: effective opacity down the whole ancestor chain,
  sampled across a full cycle, then again under `prefers-reduced-motion` where the
  scene must be complete, labelled and static. All four pass. COMM_W4's tick is
  exempt and reported as such — it rides inside a `.ride` group and its own
  aria-label calls it a reply in flight, so fading as it lands is the animation,
  not a legibility failure.

---

## The one unverified axis

**No real browser on a real school device.** Every measurement in this file and
in the manifest comes from headless Chromium 1194 in a container. Nothing here
has been opened on a school laptop, a classroom projector or a managed tablet,
and the decks are taught from all three.

This is named as **unverified**, not as untested-and-forgotten, and it does not
block anything. It is the one axis a machine in this container cannot close.

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
