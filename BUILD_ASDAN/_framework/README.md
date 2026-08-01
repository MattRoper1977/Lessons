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

**The illuminator** — the I Do diagram's caption waits for the build to finish
(timed from each lesson's own SVG delays), and a Replay control re-runs it.

**The We Do activities** — face-down prediction cards, answers numbered back to
the card that produced them, a match grid sized to its real number of targets,
and confirmation by tick as well as by colour.

**Accessibility** — the card activities are `<div onclick>` in the lesson markup;
the layer promotes them to buttons in the accessibility tree with Enter/Space,
and makes score, feedback and slide-position announce politely. Every animation
resolves instantly under `prefers-reduced-motion` with nothing left hidden.

---

## Known, left alone deliberately

- **Zone token contrast.** None of the four zone colours clears 4.5:1 against
  white (they run 2.2–4.2:1). The decks already use white-on-zone-colour for
  `.slide-tag` and `.wedo-capture`, so it is established house style and the
  layer follows it rather than overruling a branding decision. The layer does
  not *add* new small text in a zone colour. Worth a look if the palette is ever
  revisited.
- **`.pres-cap` text colour** is a hardcoded indigo inherited from the Art
  template the decks were cloned from, rather than a subject token, so it is the
  one element that does not follow its deck's palette. Left as-is: changing it is
  a palette decision, not a layout one.
- **SVG geometry.** A few illuminator SVGs draw slightly outside their `viewBox`
  and crowd the caption. That is per-lesson artwork, not a layer concern.

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
