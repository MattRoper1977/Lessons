# Session close — 1 August 2026

For someone with no context. Nothing here is merged. `main` is `cacaf16`.

---

## The four open PRs

| PR | branch | base | what it is |
|---|---|---|---|
| **#10** | `claude/launch-animation-philosophy-79lohp` | `main` | The LAUNCH animation layer — 50 components across the 15 LAUNCH decks, giving that pathway its own philosophy rather than harder words. |
| **#11** | `claude/grow-anim-unused-svg-ids` | `main` | Two unused SVG ids in `grow-anim`: `ropepath` dropped, and the circulation asset's pulmonary circuit animated so all four vessels move. |
| **#12** | `claude/convergence-prep` | `main` | Convergence prep — the five BUILD lessons re-injected on `grow-anim`, plus six fixes. Evidence only. |
| **#13** | `claude/gate-census` | **#10** | The gate & instrument census, its fixes, and the instrument index. |

### Merge order, and why

**#13 is stacked on #10** and cannot land first — the layer it audits is not on
`main`. If #10 merges, re-point it:

```sh
git rebase --onto main claude/launch-animation-philosophy-79lohp claude/gate-census
git push --force-with-lease origin claude/gate-census
```

**#11 and #12 do not conflict textually.** #12 changes `grow-anim.js`,
`grow-motion.css` and `grow-svg.js`; #11 changes `grow-svg-bio.js` and
`grow-svg-phy.js`. Disjoint. Only #11 touches the five GROW decks.

**All of #11's substantive work is in source, not in generated files** — tested,
not assumed: regenerating the five decks from #11's own sources reproduces them
byte-identically. **Nothing needs porting.** Order alone settles it.

**But one re-injection must follow whichever of #11/#12 lands last**, because
#12's source changes leave the five GROW decks stale (#12 says so itself and
deliberately did not re-inject). Run:

```sh
python3 grow-anim/inject.py Science_Teesside/Grow/*.html
python3 grow-anim/inject.py --check Science_Teesside/Grow/*.html   # must exit 0
```

**And #13 needs a rebuild after #12**, because #12 edits `grow-motion.css`, which
#13 inlines under a pinned SHA-256. `check.js` will refuse to inject against the
stale pin — that is the guard working, not a fault:

```sh
cd Science_Teesside/launch-engine && node build.js && node check.js
```

---

## The convergence's real state

**Five BUILD lessons, twelve slides each — 60 slides**, gated on your walk.

The brief for this pass said "ten lessons, 120 slides". That is the figure *after*
the five GROW lessons are also re-injected, which has not happened: #12 left them
stale on purpose. Today the evidence covers 60 slides.

`build-anim/` is **not deleted** and is byte-identical on every branch here.

### The tag

`build-anim-autumn1-v1` is **still uncreated**, pointing at `297af43` when it is
made. It remains a home-machine job. Nothing is at risk in the meantime — the
commit is on `main` and reachable.

---

## The three rules this session earned, in the estate's words

Written into `LundyLoop/tools/INSTRUMENTS.md` as standing rules 14–16.

**14 · Call it a FALSE ZERO.** `preflight.py` named this family before any audit
did: *"a FALSE ZERO from an under-specified check is the most expensive defect
class: it CLOSES a question that was never examined."* The estate has now twice
been right by convention while a fresh audit's priors were wrong — the print
subsystem (R-E05) and this. Read the registers before forming an expectation.

**15 · Fix at the gate, never at the call site.** A hardened gate is immune to an
incomplete list of what could defeat it; a patched call site is only as good as
that list. This was load-bearing here: the fill-mode census missed inline styles,
longhand declarations and deck-level `<style>` blocks, and the gates held anyway.

**16 · A check that can return zero must first prove its input set was
non-empty.** A count of zero and an empty corpus are indistinguishable from
inside the result.

Also standing rule 13 (never read an animated property synchronously, or on a
hidden slide) and `REGISTER` R-E22 (a gate hides with `visibility`, never
`opacity` alone).

---

## The backlog

`reports/INSTRUMENT_INDEX.md` accounts for all 62 test/gate scripts in the tree:
41 instruments, 19 generators, 2 engines. 9 audited-sound, 5 audited-flagged,
**27 not yet audited** — filed as four discrete passes (BL-1 Glitch Clash, BL-2
Art Teesside, BL-3 `_passsci1`/`_passla`, BL-4 BUILD_ASDAN/build-engine), each
naming the register that must be loaded first.

They are deliberately **not** one sweep. Auditing an instrument without its
register is how you get a confident false zero.

One note carried there: `build-anim/tools/preview.mjs` fails only when the page
throws, so it cannot see the failure `build-anim/README.md` itself warns about —
*"a step targeting a part name that does not exist does nothing at all,
quietly."* `grow-anim/` has **no equivalent tool**, so the defect dies with the
folder. The patch is recorded in the index; **if you do the deletion walk, know
that the tool you might reach for is blind.**

---

## Two decisions that are yours alone

### 1 · BUILD and GROW state the same philosophy

`build-anim/README.md` and `grow-anim/README.md` open with **word-for-word
identical** paragraphs:

> *"The point is not decoration. The point is that the animation is the
> explanation. Movement explains, teacher narration reinforces, and a short label
> confirms after the idea has landed — so the amount of reading a pupil has to do
> to follow the lesson drops close to zero."*

Your pathway table says they should differ:

> | **BUILD** | learn the concept | **replaces text** | guide and narrate |
> | **GROW** | explore the concept | **explains a process** | prompt predictions and discussion |

LAUNCH's distinction is now drawn in the markup. The BUILD/GROW one is not drawn
anywhere. Neither README has been rewritten — which tier means what is a teaching
decision, and it changes what the lessons should *do*, not just what the
documents say.

### 2 · Smaller pictures on stages

#12 caps the picture against the usable height so the rail caption clears the nav
(caption bottom 717 → 649; nav top 663). It also un-clips the bottom of every
default-frame slide, which overflowed by 20px at 1280×720 on `main`.

The tension is worth naming: **both READMEs say the animation *is* the
explanation.** If that is true, a smaller picture is a smaller explanation, and
the trade against a readable caption is a pedagogical judgement rather than a
layout one. Reverting is four custom properties in `grow-anim.css` and nothing
else; `reports/convergence/_frames/` renders the same slides three ways so the
choice can be seen rather than argued.

---

## How to check any of this rather than trust it

```sh
cd Science_Teesside/launch-engine
node check.js                 # payload + source contracts
node inject.js --check        # decks match the built engine
node test/gate-shape.js       # every gate pairs visibility
node test/gate-leak.js        # nothing gated is readable before it is earned
node test/print-pack.js       # every tier of every pack produces a handout
node test/health.js           # 25 decks, every slide, errors + overflow
```

The last four need `playwright-core` and a Chromium; set `SCI_CHROMIUM` if it is
not at the default path.
