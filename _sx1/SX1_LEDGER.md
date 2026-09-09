# SX1 ledger — Spring/Summer Science batch

51 lessons, 51 companion packs, authoring source. Nothing silently dropped.

## Intake

14 distinct files by SHA-256. The BUILD Next-8 zip appears twice in the upload
(`a499eae4…`, `f6999e69…`) and both hash `70eba300345b95cc4019497bb43d37d3c925b026bac8b3797023dc3fda392965`
— one file, listed twice. Appendix A counts confirmed exactly: exemplars 7 HTML,
animated-6 13, Next-8 17, authoring source 57 json / 33 py / 14 css / 3 xlsx.

## The four loose decks — all four are no-ops

Every one is byte-identical to a deck already served:

| deck | sha256 | served at |
|---|---|---|
| BUILD_HUM_W10 | `d49da66c…` | `Humanities_Teesside/Teaching_Packs/BUILD/Week_10/…Rails_Meet_The_River.pptx` |
| GROW_W8A | `b7638aae…` | `Science_Teesside/Teaching_Packs/GROW/lessons/W8A/…Day_And_Night_Sky_Shift.pptx` |
| LAUNCH_A2_W7L1 | `c603dcaa…` | `Science_Teesside/Teaching_Packs/LAUNCH/lessons/A2_W7L1/…Assessment_Review_Map.pptx` |
| **BUILD_W3A_Backbones (2)** | `07e840c3…` | `Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones.pptx` |

Appendix A expected Backbones (2) to differ from every pack deck in the batch and
to need diffing against the served copy. It does not differ: the `_2` is a browser
download suffix, not a revision. **F6 is a no-op in full** — no deck replaced, no
Slides.pdf regenerated, no deck rider in the BUILD commit. Finding, not a stop.

## P1 — 51 measured, zero writes

| check | result |
|---|---|
| folder complete (9 files + `Diagrams/`) | 51/51 |
| stage minutes = 40 | **51/51 in the decks and in the source**, agreeing slide for slide |
| SoW cell resolves; `exactOutcome` verbatim in the named cell | **51/51** |
| declared classic donor exists in this repo and sha256 matches | **51/51** |
| duplicate ids · `<script src>` · `hud.js` · storage · "Made by Matt" | 0 |
| `node --check` on inline scripts | 153/153 pass |
| external **loads** | **0** — every URL a citation, 1-6 per file excluding the SVG namespace |
| `prefers-reduced-motion` halts every animation, every slide, in a browser | **51/51** |
| repeating animation cycles under 333 ms | **0 of 867**; shortest repeating cycle 550 ms (1.8 Hz) |
| tap targets ≥ 44 px | **8505/8505** |
| pptx/docx/pdf parse, pages > 0 | 255/255; `Slides.pdf` page counts equal deck slide counts |
| byte-identical rebuild from authoring source | **24/24** (source covers the Next-8 only) |
| `:root` pathway tokens equal the donor's | **51/51** — F2 needed no work |
| data-URI images over 50 KB | **0** — F5 confirmed empty |

### Two measurements I had to throw away

Both would have passed vacuously, and neither is reported as green:

- **Animation safety, first attempt.** One sample at 1200 ms on slide 1 returned
  0 animations in *both* motion modes — but the CSS plainly carries
  `animation:artHeroPulse 2.4s … infinite`. Entrance animations finish by ~600 ms
  and leave `getAnimations()`, and 13 of 14 slides are `display:none`. Rewritten to
  walk every slide and sample at +90 ms, it observes 4 running animations per
  lesson, and *then* the reduced-motion result means something.
- **"8 controls at 43 px."** `min-height:44px` was set and honoured; the entrance
  keyframe is `transform:scale(.985)`, and `getBoundingClientRect` returns the
  transformed box — 44 × 0.985 = 43.3. Measured with motion reduced: 0 of 8505 under 44.

Also discarded: the order's `^<STAGE> · <n> min across this stage` footer pattern
appears **0 times in the whole served estate**. Minutes were read instead from the
decks' own `<PATHWAY> SCIENCE <stage> <n> min` footers and the source `slides[].minutes`,
which agree slide for slide — unfootered slides carry `minutes: 0` and are continuations.

## What the order named that this repo does not have

- `SOW_CELL_LEDGER` — no such file. The three SoW workbooks named by the lessons'
  own source JSON (`_passsb/`, `_passsg/`, `_passsl/inputs/*.xlsx`) are the cell
  authority, and all 51 cells were verified against them.
- The **PH-3 furniture patcher** — absent. Furniture applied on the NAV-1 pattern
  (`_nav1/tools/nbutton.py`) copied literally from a served sibling.
- **`canonical` is not the family convention.** 9 of 214 served Science lessons carry
  one (4%). Adding it would have made these 51 unlike their 203 siblings, so it was
  not added — AUTO-DECISION SX1-D4, agreed with Matt. Applied instead: way-home,
  splash, `data-mbm-guide` on the staff layers, and exactly one `<h1>`.

## Fixes

| class | what |
|---|---|
| F1 | way-home (depth-derived href, arrow + word, 44 px, hidden in print), splash, 3 staff regions tagged per lesson, `<h1>` promoted from the Opening slide's `<h2>` — the batch shipped with **no `<h1>` at all** |
| F2 | none needed: 51/51 already equal their donor's tokens |
| F3 | 1006 pupil-facing calendar labels rewritten to sequence-relative across six meta dialects, originals kept in `data-mbm-cal` (reversible); plus 6 prose rewrites in `launch_genetic_engineering` |
| F4 | no defects: the two candidates were both my own measurement errors (above) |
| F5 | none: 0 data-URIs over 50 KB |
| F6 | no-op: the deck is byte-identical to the served one |

### The gate could not see Summer

`tools/relabel_public.py` FORBID matched `Autumn 1|2` and `Spring 1|2` but **not**
`Summer 1|2` or `Sum1|Sum2`. No Summer content had ever reached the estate, so the
hole was invisible; 20 of these 51 are Summer, and the gate would have read 0 on a
pupil-facing "Summer 1" and called it green. Pattern widened in its own commit,
red-proved both ways.

### Why the token gate still reports hits, and why that is right

After the rewrite the gate reports 568 hits on the batch. Every one was classified:

- **567** are pupil **task numbers** — `W1.` `W2.` `W3.` worksheet items, and ranges
  like "paper W1–W3". `\bW(?:eek)?\s?\d+\b` cannot tell those from a week label.
- **1** is a `data-teacher="…"` note, a staff attribute the tool does not recognise as staff.

**Zero are genuine pupil-facing calendar labels.** For comparison, the *already-served*
W8-W13 lessons fail the same gate with 104 hits that include real ones — "Autumn 2 ·
Week 3 · Explore", "Week 9 · Explore". This batch is cleaner than main on this rule.
Rewriting pupil worksheet numbering to chase a vacuous zero would corrupt the
worksheets, so it was not done. AUTO-DECISION SX1-D5.

## Admission — 51 ADD BESIDE, 0 REPLACE, 0 STOP

Full table in `_sx1/ADMISSION.md`. Existing coverage stops at `C28`/`C29`; the batch
starts at `C29`/`C30` — exactly contiguous.

Two cells carry two lessons each, and both are **compound outcomes split one lesson
per conjunct**, not collisions:

- `GROW Weekly - Spring!B30:C30` "thermal **and** electrical conductors and insulators"
  → *The cold case* (thermal) + *Circuit fault clinic* (electrical). The authors marked
  these "lesson A" / "lesson B"; landed `W18A` / `W18B` on the family's own A/B convention.
- `LAUNCH Weekly - Spring!C30` "selective breeding **& genetic engineering**"
  → *Selective breeding* + *Genetic engineering*. Same shape, unmarked by the authors;
  landed `W18L1` / `W18L2` on LAUNCH's own L1/L2/L3 convention. AUTO-DECISION SX1-D6.

**Three lessons have no calendar week.** `Spr2·W6` / `C39` is a real SoW row, but
`CALENDAR_2026_27.json` gives Spring 2 five weeks (abs 22-26) and marks `Spr2·W6`
NOT-TIMETABLED. Matt's call: land as unscheduled Spring 2 review rather than STOP —
all three are consolidation/evidence checkpoints, usable whenever the term runs short.
Their manifests carry `scopeStatus: IN_SCOPE_NO_CALENDAR_WEEK` with the reason.

**Coverage gaps this batch does not fill** (nothing to land, not a failure):
LAUNCH `C31` (Spr1·W4, evaluate GM) is only referenced as a bridge, and LAUNCH `C32`
(Spr1·W5, Topic 4 assessment) has no lesson. Absolute weeks 19 and 20 stay empty in
the LAUNCH Spring folder.

## Placement

Folder names derived from the actual week span, on the family's existing
`W<start>-W<end>_2026-27` pattern — no invented convention, no renumbered week:

| | Spring | Summer |
|---|---|---|
| BUILD | `W18-W26_2026-27` (10) | `W27-W34_2026-27` (7) |
| GROW | `W18-W26_2026-27` (11) | `W27-W32_2026-27` (6) |
| LAUNCH | `W17-W26_2026-27` (10) | `W27-W34_2026-27` (7) |

`unit` comes from the SoW "Unit / Topic" column for that pathway and half-term,
taking the mainline Science strand — the "IGCSE Sciences OPTION" block is a separate
optional course and is skipped. `halfTerm` comes from each lesson's own source
declaration. Neither is read from a filename.

**Recommended: 0 changes.** Every cell here has exactly one lesson, so
`rx3_recommended.py` has nothing to arbitrate; one-recommended-per-cell holds trivially.

## Gates

| gate | result | red proof |
|---|---|---|
| RX3 family gate (`boot390`, 390×844) | **51/51 PASS** — 0 errors, 0 failed requests, way-home visible at 44 px in the first viewport, `h1=1`, 3 staff regions each hidden by default, no overflow, 0 storage | the harness's own pass predicate |
| way-home census | 51/51 exactly one control, all resolving to the real `/Lessons/index.html` | — |
| animation safety, re-run on the placed files | PRM halts all, 51/51; 0 visible infinite cycles under 333 ms; 0 errors | v1 discarded as vacuous (above) |
| tap targets | 8505/8505 ≥ 44 px | measured with motion reduced so no transform shrinks the box |
| catalogue schema | green over all 950 rows | a novel `halfTerm` "Winter 1" and a malformed id are each rejected |
| `_authoring/` not served | **0 of 344 paths admitted**, while 51/51 lessons and 309/309 pack files are | the publisher's own `public_file()` visibly refuses `_sownb/…` and `tools/…` and admits a landed lesson |
| reachability | every landed lesson appears once under its half-term row with its SoW unit; BUILD 8+12+12+2, GROW 10+12+12, LAUNCH 8+12+12+2 — 17 each, counts derived by the page | browser-driven, every row and "Show N more" expanded |
| pack chip | opens exactly 6 rows = `files[].length`, each 44 px | browser-driven |
| forbidden-token gate | 0 genuine pupil-facing calendar labels; 568 classified false positives | the widened pattern hits Summer; planted-token behaviour unchanged |

## Not done, and why

- **`s23` learner-name gate → MEASUREMENT INVALID.** Its reference list is absent by
  design (`_next6/FINDINGS.md`: the list would itself be the leak). That is the
  specified behaviour, not a failure. Nothing removed.
- **Pupil Office files still carry calendar tokens.** So do **45 of 80** already-served
  Science pack docx, pupil files included. The relabel rule has only ever been applied
  to HTML surfaces; rewriting Office files needs the managed renderer, which the
  authoring READ_ME states is environment-specific and not bundled. Pre-existing
  estate condition, reported, not silently inherited as new.
- **`Slides.pdf` not regenerated** — no proven pptx→pdf path in CI, and no deck changed.
- **`SCI_G_A2_W7A`** is not in this batch. #428/#429/#416 untouched.
- **START_HERE pages, sources and diagrams are not served** (A6, Appendix B).
