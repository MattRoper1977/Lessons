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
