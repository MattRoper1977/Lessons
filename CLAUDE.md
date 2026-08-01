# Working in this repo

Notes for whoever picks this up — human or Claude. This is the durable stuff:
architecture, traps, and how to prove a change works. For "what shipped when",
read the git log.

---

## Shape of the thing

`Games/*.html` are **single self-contained files**. No build step, no bundler,
no `<script src>` to anything external. A game is one file you can open from
`file://` and play. Keep it that way — do not introduce a CDN, a webfont or an
image file to one.

They are served by GitHub Pages from `main`. A merge to `main` triggers
`pages build and deployment`; check that run succeeded before telling anyone
it is live.

---

## The temporal dead zone trap

**This has bitten three separate times in this repo. Read this before you add
an init call.**

These files are one enormous script. A `const` module defined at line 2000 is
in its *temporal dead zone* everywhere above line 2000 — touching it there
throws `ReferenceError`. That on its own would be obvious. What makes it
vicious here is that these files wrap init calls in `try{ ... }catch(e){}`,
which **swallows the error silently**.

Three real instances:

1. `try{ FX.init(); }catch(_){}` sat ~1150 lines above `const FX`. It threw on
   every load, forever. `init()` is the only thing that sizes `#fxcanvas` and
   takes its 2D context, so `cx` stayed null and every `spawn()` returned at
   its first line. **The particle layer never drew, from the day it was
   written until August 2026.** Nobody noticed because nothing errored.
2. A settings block referenced `GCX` above its definition. Same mechanism —
   but that one threw *inside the shared UI closure*, aborting the whole
   closure. The page loaded and nothing worked at all.
3. `closeSheets()` probes a flag defined below it. `typeof` does **not**
   protect against the TDZ, so that flag has to be `var` (hoisted, undefined)
   and not `let`.

Rules that follow:

- **Init a module immediately after it, never before.**
- **Do not wrap an init call in a bare catch.** If it fails it should be a
  visible error, not a dead feature. The one in `Glitch_Clash.html` after
  `FX` is deliberately bare.
- If you must reference something possibly-undefined from above, use `var`,
  not `let`/`const`, and know that `typeof` will not save you.

---

## Glitch Clash

`Games/Glitch_Clash.html`. Four layers, and the boundary between them is the
whole design:

| Layer | What it may touch |
|---|---|
| `Engine` | the rules: damage, energy, AI, pack pulls. **Do not change this** unless balance is the actual task. |
| game code | assembles battles, drives turns, renders. Inside `if (typeof document !== "undefined") (function(){ ... })()` — so nothing in it is global. |
| `GCX` | audio, sparks, combo, reality glitches, achievements, CRT, menu music |
| `GCX2` | themes, boons, endless scaling, colourblind palette |

**The additive rule.** `GCX`/`GCX2` and every run mode change *the numbers
going in*, never the rules. Endless scales the enemy template **before**
`mkGlitch`. Boons and modifiers adjust fighter objects **after** `mkFighter`.
Engine resolves the turn identically either way. Keep new features on that
side of the line and balance stays provable.

**Reality glitches are cosmetic and must stay so.** They never alter damage,
energy or AI, and each one also announces itself in the battle log — a player
who cannot perceive the effect still learns it happened.

**Run modes must not farm the campaign.** A cleared Endless round counts as a
win and runs the achievement check, but pulls no card pack and marks no stage
cleared. Endless and the Weekly resolve in *their own* result sheets — falling
through to the campaign one double-counted the win and handed out a pack.
There is a suite pinning that.

### Test seams

The UI closure means a harness can reach nothing by default. Read-only entry
points are exported at the bottom: `__GCstart`, `__GCturn`, `__GC`,
`__GCsave`, `__GCrun`, `__GCplan`, `__GCmod`, `__GCglitches`, `__GCclock`,
`__GCclockSet`, `__GCov`, `__GCclose`, plus `window.GCX` / `window.GCX2`.
Add to these rather than making game internals global.

Two things that will waste your time otherwise:
- `startBattle(0, {})` plays an intro cutscene and returns early. Pass
  `{__scened:true}`.
- `doTurn` takes an object, `{act:'strike'}`, not a string.

---

## Accessibility invariants

These are not decoration. Breaking one is a regression, and there are suites
that will catch you.

- **Calm Mode and `prefers-reduced-motion` are the authority.** They suppress
  distortion, thin particles, skip freezes and silence the menu pad. Anything
  animated needs a static state that still reads.
- **Colour is never the only cue.** Every Keeper shows a shape glyph, a name
  and a role next to its colour. Every theme row and modifier states its
  status in text (`☑`/`☐`, `🔒 8 wins`), not just a tint.
- **High Contrast outranks cosmetics.** A theme stands down entirely under
  `.hc` rather than beating it on inline-style specificity.
- **The colourblind palette was measured, not chosen.** Candidates went
  through a Viénot–Brettel dichromat simulation scored on worst pairwise
  CIELAB distance across normal/deutan/protan/tritan vision. Shipped palette:
  worst ΔE **15.9** (teal and blue collapse under tritanopia). Current:
  **40.8**, every swatch ≥4.5:1 on the panel. If you change those four hues,
  redo the measurement — do not eyeball it.

### One CSS gotcha worth knowing

The page fill lives on `<html>`, not `<body>`, and this is load-bearing. A
negative-`z-index` pseudo-element paints above `html`'s background but *below*
`body`'s — an opaque body hid the ambient backdrop entirely. Because
`body.hc` sets its variables on `<body>`, `applySettings()` flags **both**
elements; without that, High Contrast leaves the page fill unchanged behind a
black UI.

---

## Proving a change works

```sh
tools/glitchclash/run.sh                     # the game in this repo
tools/glitchclash/run.sh path/to/copy.html   # any other copy
```

Ten headless-Chromium suites, run against the shipped file rather than an
extracted copy. Non-zero exit if any fail, so it works as a gate.

| suite | covers |
|---|---|
| `gc` | module load, audio, sparks, glitches, combo, a full battle end-to-end |
| `gc-endless` | a run through the real buttons: rounds 1→3, boon picker, boon carried forward |
| `gc-mods` | the sheet, toggling, payout scaling, each modifier moving the right numbers |
| `gc-clock` | Time Attack: pauses on sheets, tops up, never interrupts a turn, tears down |
| `gc-weekly` | ISO week edges, plan determinism, once-a-week payout, campaign untouched |
| `gc-fx` | the particle layer: canvas sizing, pixels actually painted, calm gates, resize |
| `gc-music` | off by default, real oscillators, menus only, muteable, calm-safe, persists |
| `gc-cb` | colourblind palette applies, persists, redraws the SVGs, clears cleanly |
| `gc-hc` | High Contrast still blacks the page out and a theme cannot override it |
| `gc-a11y` | booted under `prefers-reduced-motion`: focus, labels, Escape, Calm Mode |

**Assert on evidence, not on proxies.** Two examples from these suites that
caught real problems:

- A canvas at `300×150` with no style width is the browser *default*. Checking
  `width > 0` passes on a canvas that was never initialised. Check it matches
  the viewport.
- `musicPlaying()` returning true only proves an interval is running. `gc-music`
  checks live oscillator count and pad gain, so a silent-but-ticking pad is
  distinguishable from a working one.

When you change a feature, update its suite in the same commit. A stale
assertion that fails is noise; one that passes wrongly is worse.
