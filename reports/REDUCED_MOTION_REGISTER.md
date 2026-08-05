# Reduced-motion register

**Nothing here has been changed.** This file is an inventory for Matt to rule on, in
the same shape as [`SVG_ARIA_MANIFEST.md`](SVG_ARIA_MANIFEST.md): the estate's
reduced-motion work is a separate phased programme, and a finding that belongs to it
should not be smuggled into a pull request whose claim is about something else.

**This register did not exist before 2026-08-01.** The brief that routed the first
entry here referred to "the RM programme's own register" as an existing document. It
was not in the tree — no file at any path carried a reduced-motion inventory, and
`REGISTER.md` mentions `prefers-reduced-motion` only as a byte-identical *gate* on
other passes, never as a programme of its own. Rather than file into a document that
turned out to be assumed, the register was created and the assumption recorded. That
is the same failure shape as the entry below: a claim repeated across briefs reads as
established without anyone having re-derived it.

## What "reduced motion" has to mean here

A pupil who cannot tolerate motion gets the whole lesson: every part visible, every
label on. **They lose the animation, never the content.** That is the standing rule
in `grow-anim/grow-motion.css`, and every entry below is measured against it.

## How to read it

| verdict | meaning |
|---|---|
| **content lost** | something a sighted pupil sees is not shown under `prefers-reduced-motion` |
| **motion remains** | content is fine, but something still moves |
| **imperceptible** | a rule technically still runs, at a duration or amplitude no one can see |

---

## RM-1 · `.g-flow-orbit` is absent from the reduced-motion list

**Verdict: imperceptible. Pre-existing. Not caused by the convergence work.**

`grow-anim/grow-motion.css`'s `@media (prefers-reduced-motion: reduce)` block
neutralises `.g-flow`, `.g-flow-drift` and `.g-flow-jiggle`. It does not list
`.g-flow-orbit`, which is the fourth member of the same family and the one the
orbit motion uses.

**Measured** — `SCI_G_W6_Earth_And_Planets`, Chromium with `reducedMotion: 'reduce'`,
all stages driven to their last step:

| part | animation | computed duration |
|---|---|---|
| `earth` | `gOrbit` | `0.00001s` |
| `mars` | `gOrbit` | `0.00001s` |
| `jupiter` | `gOrbit` | `0.00001s` |

Three parts on one lesson. Nothing perceptibly moves — the duration is ten
microseconds, so the planets arrive at their final orbital position rather than
travelling to it — which is why the verdict is *imperceptible* and not
*motion remains*.

**Provenance.** The count is **identical on `main` and on
`claude/convergence-prep`**: 3 before, 3 after, on the same three parts. It was found
while auditing the GROW five after re-injection, not created by that re-injection.
Raw data: `reports/convergence/_data/grow-{before,after}.json`, field
`reduced.animatedParts`.

**Why it is worth an entry despite being imperceptible.** The gap is in the *list*,
not in the outcome. `.g-flow-orbit` is the only member of its family missing from a
rule its siblings all carry, so the next motion added to that family inherits the
omission rather than the convention. The fix is one class name; the reason it is not
in the convergence PR is that a PR claiming "this changes nothing but the injection"
must not also carry an unrelated CSS change, or the claim stops being checkable.

**Suggested fix (not applied):** add `.g-flow-orbit` to the selector list at
`grow-anim/grow-motion.css:314`.

---

---

## RM-2 · the 12 `avl*` animation families, classified on arrival

**Verdict: finite-teaching. No content lost. Blanket coverage confirmed.**

The Art Visual Learning Layer (`Art_Teesside/visual-learning/art-visual-learning.css`,
landed at `85953b1`) introduces **12 `@keyframes` families**. The house rule says new
families are classified in the commit that lands them. **That was owed in Stage A's
commit and was not paid** — this entry pays it one commit late, on the branch that
mounts the layer. Recording the miss rather than back-dating it.

### The families, as measured — not as described

| family | applied to | iterations | fill | final frame persists |
|---|---|---:|---|---|
| `avlDrawMark` | `.avl-mark-stroke.is-running`, `.avl-rub.is-running` | 1 | `both` | yes |
| `avlRouteTrace` | `.avl-route.is-running` | 1 | `both` | yes |
| `avlDabLift` | `.avl-dab.is-running` | 1 | `both` | yes |
| `avlLayerBuild` | `.avl-layer.is-running`, `.avl-version.is-running` | 1 | `both` | yes |
| `avlEditionReveal` | `.avl-edition.is-running` | 1 | `both` | yes |
| `avlBarGrow` | `.avl-bars.is-running` | 1 | `both` | yes |
| `avlFlowStep` | `.avl-flow.is-running` | 1 | `both` | yes |
| `avlSlideBlock` | `.avl-block.is-running` | 1 | `forwards` | yes |
| `avlReveal` | `.avl-reveal` | 1 | `both` | yes |
| `avlFlowRight` | `.avl-particle.is-running-right` | 1 | `both` | yes |
| `avlFlowLeft` | `.avl-particle.is-running-left` | 1 | `both` | yes |
| `avlContract` | **never applied** | — | — | — |

**All 12 are finite.** Every shorthand carries an explicit `1`, and the string
`infinite` does not occur anywhere in the file. Nothing loops, nothing needs
stopping, and no family is decorative — in each case the moving element *is* the
artistic cause being taught (a mark being drawn, layers registering, an edition
revealing).

**Two corrections to the description this entry was commissioned under.** It was
issued as "single iteration, `both`/`forwards`/`alternate`, final frame persists" for
all twelve. Measured, that is true of ten:

- `avlFlowRight` and `avlFlowLeft` carried **no fill mode** when this entry was
  first written. `alternate` is their *direction*, not a fill, so with one iteration
  they reverted to their unanimated position instead of persisting a final frame.
  **Fixed 2026-08-05** (sentinel `avl-tail-2026-08-05`): `both` added to both
  shorthands, nothing else in those two declarations changed. This was a real
  divergence from the pack's own rule — *finite movement; the final frame stays
  visible for pointing, questioning and annotation* — and the two flow families were
  the only members of the twelve that broke it.

  **Measured, both sides**, `--avl-duration: .12s`, computed `transform` read 700ms
  after the class is applied:

  | | `avlFlowRight` | `avlFlowLeft` |
  |---|---|---|
  | before the fix | `none` | `none` |
  | after the fix | `matrix(1, 0, 0, 1, 150, 0)` | `matrix(1, 0, 0, 1, -150, 0)` |

  The after values are the `to` frames of each family exactly. The before values are
  why this needed fixing, and why the test is trustworthy: it returns a different
  answer on the two CSS files, so it can fail.
- `avlContract` is **defined and never applied.** No rule anywhere references it. It
  is a dead family, not a live one. **Deliberately retained** — removing it would be
  prose-editing a toolkit that was recovered by byte-for-byte extraction, which is a
  larger risk than an unused `@keyframes` block. Recorded here as a known dead family
  so the next reader does not go looking for its effect, and so a future audit does
  not read it as an accident.

### Coverage

One blanket rule, at the foot of the same file:

```css
@media (prefers-reduced-motion: reduce) {
  .avl-panel *, .avl-panel *::before, .avl-panel *::after {
    animation-duration: .001ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: .001ms !important;
  }
}
```

It is scoped to `.avl-panel *`, so it reaches every one of the 12 by descent rather
than by enumeration. **This family cannot inherit the RM-1 omission** — there is no
list to be left out of. A `forced-colors: active` block is also present.

**Measured** — Chromium, `reducedMotion: 'reduce'`, `We Do 1` slide activated so the
panel is visible and the assertion can fail:

| lesson | running animations | labels/explanations retained |
|---|---:|---:|
| `BUILD_ART_W3_Industrial_Surface_Skills_Lab` | 0 | 12 |
| `GROW_ART_W3_Independent_Studio_Challenge` | 0 | 15 |
| `LAUNCH_ART_W3_Implement_and_Critically_Develop` | 0 | 13 |

**Scope of that measurement, stated honestly:** all three specimens carry a `model`
activity, so the run exercises the model-family animations and `avlReveal`. It does
**not** exercise every one of the 12 — `avlFlowRight`/`avlFlowLeft`
(`.avl-particle`) and the sort/sequence/evidence/hotspot paths are reached by other
payloads. The blanket selector makes per-family enumeration unnecessary for the
verdict, but the empirical figure above covers three lessons, not thirty-one.

**Static parity independent of the OS setting.** Each panel carries an
`avl-static` control which `isStatic()` reads alongside `reducedMotion`, so a pupil
who needs stillness gets it without changing a system preference. The static path
retains every label, comparison and explanation.

**One defect found and fixed while classifying.** `reducedMotion` was computed once
at module load with no `change` listener, so an OS preference changed mid-session was
never honoured in JS. The CSS rule still applied, so it degraded rather than failed.
The media query is now watched and `isStatic()` reads the live value.

## Standing measurement

`reports/convergence/audit.mjs` records `reduced.hiddenParts` and
`reduced.animatedParts` per lesson under a real `reducedMotion: 'reduce'` context.
Last observed across all ten Autumn 1 science lessons at `c866582`:

| lesson | parts still hidden | parts still animating |
|---|---:|---:|
| `SCI_B_W3_Backbones` | 0 | 0 |
| `SCI_B_W4_Muscle_Pairs` | 0 | 0 |
| `SCI_B_W5_Right_Nutrition` | 10 | 0 |
| `SCI_B_W6_Balanced_Plate` | 14 | 0 |
| `SCI_B_W7_Where_Food_Comes_From` | 0 | 0 |
| `SCI_G_W3_Friction` | 15 | 0 |
| `SCI_G_W4_Mechanisms` | 15 | 0 |
| `SCI_G_W5_Fair_Test` | 9 | 0 |
| `SCI_G_W6_Earth_And_Planets` | 6 | **3** (RM-1) |
| `SCI_G_W7_The_Moon` | 12 | 0 |

The hidden counts are **not** reduced-motion failures: they are parts no script in
that lesson ever reveals, and they are identically hidden with animation on. Checked
for BUILD W5 and W6 by re-running the same measurement with animation enabled and a
three-second settle — same names, same counts, 10 and 14. The GROW hidden counts have
**not** been checked that way and are recorded here as unverified.
