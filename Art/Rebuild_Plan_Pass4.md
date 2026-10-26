# Art Teesside — rebuild plan, re-derived from the register

**Base:** `3b805af` · **Branch:** `art-remediation` · **Terminal point:** A2a, then stop.
**Status:** published for approval. Nothing executed. Token not yet received; nothing pushed.

Nine passes, not eleven. The grade purge and the hours-gate wording collapse out — both are already
satisfied at origin. Every count below is a **prediction**; exceeding it stops the pass.

---

## The passes

| Pass | Item | Files | Predicted count | Confidence |
|---|---|---|---|---|
| **R1** | Autumn 2 headers | `Build/BUILD_ART_A2_W1…W7` | **7 files, 26 substantive string edits** | Exact — surveyed |
| **R2** | Orphan lessons: link + catalogue | `resources.json`, `Build/START_HERE.html`, `Build/Autumn2_Scheme_of_Work.html` | **3 files, 0 lesson files** | Exact |
| **R3** | GROW Part B | `GROW_ART_W1, W2, W3, W5, W6, W7` | **6 files** | Exact — Part B absent in all six, present in W4 and W8 |
| **R4** | Silver 1B observer block + locator row | LAUNCH 1B carriers | **3 files** | To be fixed at pass open, reported before first edit |
| **R5** | 1B portfolio row | LAUNCH pack + carrier | **2 files** | To be fixed at pass open |
| **R6** | `.ladder` rule | the eight packs | **8 files** | Exact |
| **R7** | `min-height: 277mm` | the eight packs | **8 files, 55 sheets** | Exact |
| **R8** | `.a4.dense` | the eight packs | **8 files** (6 carry `x.extra`) | Exact |
| **R9** | A2a | `GROW_ART_W2` | **1 file** | Exact |

Full assertion set across all 53 files after each pass, reported as counts. One pass, one commit, one push.

### Why this order

R1 and R2 first because they are navigational: R2 makes `Stencil_Lab` reachable, and `Stencil_Lab` is the
sole source R9 derives from. Deriving A2a from a file no one can find is how the last A2 ended.

**R6 must precede R7.** `.ladder` collapses three full-width block divs into a 3-column 7pt grid, which
cuts their rendered height substantially, which changes page counts, which is the thing R7 measures.
Measuring `min-height` before `.ladder` lands would measure a layout that is about to change.

R8 after R7, per your sequence — the real fix measured first, belt-to-braces second.

---

## Three corrections to the header brief (R1)

You asked to be contradicted rather than taken at your word. All three fields are wrong somewhere, so
your reading holds in aggregate — but not one of them is wrong where you said, and the true shape is worse.

**The award level is already Bronze.** The `award-strip` reads `🎨 Bronze Part A · Take Part` in all seven,
with correct per-lesson Parts. `Explore` survives in two *other* places:

- the coloured badge — `BUILD · Explore · Week 3 of 7 · Autumn 2`
- the footer — `Art Studio Suite · Trinity Arts Award Explore`

So the same slide header carries `BUILD · Explore` and `Bronze Part A` inches apart. The file does not
merely say the wrong thing; it says both things at once, which is why it survived review.

**The badge already carries the right term and the right week** — `Week 3 of 7 · Autumn 2`, correct in all
seven. What is wrong is the `sow-strip` and the print mirror.

**Field-by-location, all seven files:**

| Location | Award | Term | Week |
|---|---|---|---|
| `sow-strip` slide header | — | `Aut 1` ✗ | `Week 1` ✗ |
| coloured badge | `Explore` ✗ | `Autumn 2` ✓ | `Week N of 7` ✓ |
| `award-strip` | `Bronze` ✓ | — | — |
| footer | `Explore` ✗ | — | — |
| `Teacher Print Tools — Week 1` print mirror | — | — | `Week 1` ✗ |

Four locations, not the slide / print mirror / KO / rev-block set you named — I found no KO or rev-block
instance of any of the three fields.

**Two traps, both of which would produce a confident wrong answer:**

1. The term separator is a **non-breaking space**: the literal string is `Aut\xa01`, not `Aut 1`.
   A plain `Aut 1` search returns zero across all seven files. Anything matching on a normal space
   silently reports the defect as absent.
2. `Week 1` appears **2–4 times per file, and only 2 of them are header fields.** The rest are
   legitimate cross-references to Week 1's rubbings — "sponge one stencil over a Week 1 rubbing",
   "Overlay: stencil over a Week 1 rubbing". A blanket replace destroys the teaching in W3 and W5.
   `W1_Surface_Hunt` has three `Week 1` strings of which two are header fields that need no change.

A half-fix here makes the file look audited. An over-fix makes it look audited *and* breaks the overlay
task. Both are worse than the defect.

---

## Two independent confirmations

Per the standing rule, a finding re-derived by a method sharing no premise with the first says so.

**D-ORPHAN-01, confirmed twice.** Method 1: link graph — zero inbound references anywhere in the repo.
Method 2: catalogue membership — `resources.json` holds 51 Art Teesside entries against 53 tracked HTML
files, and the two absent are `BUILD_ART_A2_W3_Stencil_Lab.html` and `BUILD_ART_A2_W4_Audience_Week.html`.
Same two files, no shared premise. R2 therefore has two jobs, not one: link *and* catalogue.

**55 sheets, confirmed independently of the earlier figure.** Counted from each pack's own `WEEKS` array
rather than from a render: 7 + 8 + 6 + 8 + 8 + 6 + 6 + 6 = **55** across the eight `sheet()` packs. This
agrees with the lost measurement, which is worth stating precisely because it is the only lost figure
that has now been re-derived rather than re-trusted. R7 still re-measures the render; this only confirms
the denominator.

---

## Standing constraints carried into every pass

- Branch `art-remediation` only. Never `main`.
- Verified means read at `origin/art-remediation`, by a read separate from the write.
- Pack work validated by rendering to A4, not by reading CSS. `print_pack_audit v1` is QUARANTINED
  and will not be used; its tier vocabulary premise fails on supported/standard/stretch.
- R7 mount floor: no mount zone below **167px** on any of the 55 sheets. `.mounts` carries `flex:1`,
  so it returns space when `min-height` takes it. Any sheet below the floor stops the pass.
- R9 scope guard: press residue found outside `GROW W2/W3/W6/W7` is **listed and not touched**. It
  becomes A2d. Scope expansion is what stopped the original A2.
- The 24-week GROW and LAUNCH gap stays untouched.
