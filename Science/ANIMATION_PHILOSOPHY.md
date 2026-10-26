# Animation philosophy across the three pathways

Written 1 August 2026, alongside the LAUNCH Scientific Observation Layer.

The three pathways were differentiated by **content difficulty only**. Measured
at HEAD before this pass, a BUILD deck and a LAUNCH deck were structurally
identical: ten slides with the same titles, sixteen `v5-step` reveals, one
static SVG, one sort activity, one match activity, one WAGOLL ghost-typer. The
words were harder in LAUNCH. Nothing else was.

That is a difficulty ladder. It is not a progression in how pupils work, and it
is not what the pathway names promise.

## The distinction

| | BUILD | GROW | LAUNCH |
|---|---|---|---|
| **Pupil's role** | learn the concept | explore the concept | think like a scientist |
| **Animation's role** | **replaces text** | **explains a process** | **supports reasoning** |
| **Teacher's role** | guide and narrate | prompt predictions and discussion | facilitate enquiry, challenge conclusions |
| **What the animation gives** | the idea, made visible | the mechanism, made followable | a question, and the means to answer it |
| **What it withholds** | nothing — showing is the job | the outcome, briefly | the label, the pattern and the explanation, until earned |

BUILD reduces reliance on reading by making ideas visible.
GROW helps pupils understand how scientific processes work.
LAUNCH shifts the emphasis from being shown science to **doing** science.

## What that means in the markup

LAUNCH is the only pathway where an animation is allowed to refuse.

- A label does not appear until the pupil has recorded what they noticed.
- A zoom does not go deeper until a prediction has been committed.
- An explanation is physically unreachable until the pattern has been stated.
- A comparison does not explain itself until every difference has been found.
- A graph pauses before the point where predicting it is a real risk.

Each of those is a gate, and each gate records the act that opened it in
`data-sci-opened-by`. A LAUNCH component you cannot describe in the form
*"this appears because the pupil did X"* is a GROW component in the wrong
folder.

## The shared motion language

`grow-anim/grow-motion.css` defines ten movements, and each means exactly one
thing in every pathway and every subject:

> draw = a structure is forming · glow = this is the important feature ·
> pulse = look here now · fade = this matters less · morph = something is
> changing · flow = something is moving · shake = that idea is incorrect ·
> bounce = that answer is correct · trace = follow this pathway ·
> zoom = we are going in close

Inheriting a vocabulary is not free, and it is worth knowing why before you do
the same in BUILD: `.g-in` was adopted onto observation labels as pure
convergence, and because it is `animation: … both`, its held final keyframe beat
the `opacity:0` that was gating them. Every label became readable at load. The
shared classes carry *behaviour*, not just appearance — add them at the moment
of reveal, not at construction.

**LAUNCH inherits it rather than replacing it.** The layer inlines that file and
applies `.g-flow-jiggle`, `.g-draw-pop`, `.g-bounce` and `.g-in` for the motions
that already have a meaning; it only defines motion of its own where nothing
shared applies. `launch-engine/check.js` fails the build if `sci-engine.css`
restyles one of the ten, or if the engine applies a `.g-` class that
`grow-motion.css` does not define.

This matters because the three pathways sit on one progression. A pupil moving
GROW → LAUNCH should find the interface already familiar and the *demands*
higher — not have to relearn what a wobble means. The difference between the
pathways is in what the animation withholds, not in how it moves.

One small win from the alignment: GROW's jiggle already takes a `--g-heat`
knob, so the diffusion simulator's temperature slider drives the shared motion
directly. Turn the temperature up and the particles jiggle harder, in the same
motion the pupil has been reading since week one.

## Status

All three pathways now carry an animation layer. Measured by rendering all 25
Science_Teesside decks headlessly and walking every slide:

| pathway | decks | framework | animated nodes | speaks the shared `g-` language |
|---|---|---|---|---|
| BUILD | 5 | `build-anim/` (`ba-` prefix) | 109–160 per deck | **0 / 5** |
| GROW | 5 | `grow-anim/` (`g-` prefix) | 49–95 parts per deck | 5 / 5 |
| LAUNCH | 15 | `launch-engine/` (`sci-` prefix) | 50 components | 9 / 15 |

Zero JS errors and zero horizontal overflow across all 25, at 1280 and 768.

### There are three frameworks, and convergence is already planned

`build-anim/README.md` states the destination plainly — *"one engine is better
than two"* — and names the four capabilities `grow-anim`'s compat shim is still
missing (`pose`, `data-ba-cards`, `BioSVG.register()`, the `pop` wrapper). The
BUILD decks are safe meanwhile because `inject.py` inlines everything.

**LAUNCH deliberately did not add a fourth motion vocabulary.** It inherits
`grow-motion.css` rather than defining its own equivalents, which is one fewer
thing to unpick when BUILD converges. `launch-engine/check.js` keeps it that way.

The LAUNCH figure of 9/15 is expected, not a gap: the six decks that do not use
a `g-` motion are the ones whose components are chains, pauses and graphs —
reasoning furniture with nothing to animate. Every LAUNCH deck that draws a
scene speaks the shared language.

### Where each pathway sits against the table above

- **LAUNCH** — built by this pass. `Science_Teesside/launch-engine/`, 50
  components across the fifteen decks.
- **GROW** — `grow-anim/`, the ten-motion language plus layered assets for
  biology, chemistry and physics. Its stated aim, *"the animation is the
  explanation"*, is the GROW row exactly.
- **BUILD** — `build-anim/`, five decks rebuilt on it. Its README opens with the
  same sentence GROW's does: *"the animation is the explanation."*

That last point is worth sitting with. BUILD and GROW currently state the **same
philosophy**, and the table above says they should not: BUILD's animation
replaces text, GROW's explains a process. They are close cousins and the overlap
may be entirely fine in practice — but if the three pathways are meant to differ
in how pupils work and not only in what they read, the BUILD/GROW distinction is
the one still to be drawn. LAUNCH's is now drawn in the markup.

Do not reuse the LAUNCH engine wholesale for BUILD. Its whole design is
withholding, and withholding is the wrong instrument for a pupil whose barrier
is reading. Reuse the scenes, the verbs and the shared motion language; rebuild
the gating.
