# Session close — BUILD/GROW convergence

*One of two closes for 1 August 2026. The other is
[`2026-08-01-gate-census.md`](2026-08-01-gate-census.md); the index is
[`README.md`](README.md).*

**Branch:** `claude/convergence-prep` · **PR #12** · **base:** `main` at `cacaf16977646b40f0ff72c9e5112a7f31877679`
Nothing merged. Nothing pushed to `main`. `build-anim/` byte-identical to `main`.

---

## Correction: the PR-stacking claim, and what was actually true when

Stated first because it is a correction to the record, and because the claim was
carried unchecked into three separate briefs. The sequence matters, because a later
event made the claim true and it would be easy to conclude it was right all along.

**At 15:56 on 1 August, when the claim had already appeared three times**, the API
said all four PRs based on `main` at `cacaf16`:

| PR | branch | base at that moment | head |
|---|---|---|---|
| #10 | `claude/launch-animation-philosophy-79lohp` | `main` @ `cacaf16` | `d944207` |
| #11 | `claude/grow-anim-unused-svg-ids` | `main` @ `cacaf16` | `88bc8f4` |
| #12 | `claude/convergence-prep` | `main` @ `cacaf16` | `c866582` |
| #13 | `claude/gate-census` | `main` @ `cacaf16` | `2dcd6aa` |

**No stacking existed.** The claim originated in an earlier session's report and was
copied into two briefs and a ledger without being checked; by its third appearance
it read as established. It was queried only because a brief asked for a re-point
command that made no sense against what the branches showed.

**Then #13's own session re-pointed it**, deliberately and with the reasoning in its
PR body: the exemplar bug lived in #10's layer, so the census could not land first.
By the time the merge pass ran, #13 genuinely based on
`claude/launch-animation-philosophy-79lohp` at head `1d633ce`. It was re-pointed
back to `main` through the API — not rebased, not force-pushed — once #10 had
landed, and its diff was re-confirmed as its own work only: **26 files, 1,049
insertions, 8 commits**, against **35 files and 5,548 insertions** had it merged
unstacked.

**The rule survives the reversal, and this is why it is worth writing down.** A
claim that is unverified when made is unverified even if something later makes it
true. The cost was real: the diff would have carried #10's whole changeset.

**Incidentally:** `#11` is `claude/grow-anim-unused-svg-ids` — the branch flagged
twice in earlier passes as unidentified. It is now identified.

## Correction: the reduced-motion register did not exist

The second of two, and also upstream of this session. A brief routed a finding to
"the RM programme's own register" as an existing document. **There was no such file
at any path.** `REGISTER.md` mentions `prefers-reduced-motion` only as a
byte-identical *gate* on other passes, never as a programme with a register of its
own. The claim came from a note about a reduced-motion *programme*, from which a
*document* was inferred.

`reports/REDUCED_MOTION_REGISTER.md` was created, the finding filed as RM-1, and the
assumption recorded inside it — better than filing into a document that turned out to
be imaginary, and better than silently not filing.

**Two instances in one session** of something being asserted to exist that nobody had
checked. That is what makes the rule below a rule rather than an observation.

---

---

## Vertical space is oversubscribed estate-wide

Two sessions measured the same thing in different corpora and neither can fix it
alone, so it is recorded once here.

- **BUILD_ASDAN at 1280×720:** everything on the I Do slide except the diagram
  totals **679px against 638px visible**.
- **BUILD/GROW convergence:** the We Do 2 slide's single column needs **932–1069px**
  of viewport height depending on width; only 1920×1080 provides it. At 150% display
  scaling the slide has **~460px for content needing 1069px**.

**Per-deck tuning cannot fix this.** The convergence pass bought back 106–120px by
rearrangement without removing anything, and that was enough at 100% and 125% and
nowhere near enough at 150%. The next step is a decision about how much a slide is
allowed to carry, and it is a teaching decision.

**ASDAN did not reproduce the y≈702 collision** the convergence pass found — its
worst was 637 against a nav top of 663. Different corpus, not a refutation.

## The 606 — 205 teaching contrast failures, ruled on

`contrast_check.js` reports 606 contrast findings, of which **205 are teaching
elements**. All 205 are identity hues — the school's own palette. **Matt has ruled
that the identity hues stand.**

Recorded here as a *decision*, not as a backlog item, because the alternative is
that the next audit re-reports all 205 as defects and someone spends a day
rediscovering the ruling. The instrument is not silenced and is not wrong; its
output is governed.


## The rules this session earned — now in the estate's rules file

Recorded as standing rules **17–20** in `LundyLoop/tools/INSTRUMENTS.md`, with rule
**15** extended to carry its third sighting. That file is the register; this list is
a pointer, not a second copy — a rule kept in two places is a rule that will
disagree with itself (rule 19).

1. **Fix at the gate, never at the call site** — rule 15, now three sightings.
2. **A check that can return zero must first prove its input set was non-empty** — rule 16.
3. **A fact repeated across documents has been copied, not verified** — rule 17.
4. **Instruments that disagree are evidence** — rule 18.
5. **A document that argues with itself is worse than one out of date** — rule 19.
6. **A target metric moving the right way is not evidence the change is correct** — rule 20.

### How they were earned here

1. **A measurement adjacent to the claim is not the claim.** `inject.py --check`
   compares inlined bytes to source bytes, which says nothing about whether the
   result parses. A lesson loaded, exited 0, and did nothing.
2. **An aggregate cannot clear a per-instance claim.** The `draw`-verb difference was
   called cosmetic on an aggregate visibility census; only 176 per-instance samples
   could actually clear it — and the same investigation turned up a real bug the
   aggregate had hidden.
3. **A fact repeated across documents has been copied, not verified. Re-derive it at
   its source before acting on it.** Repetition is not corroboration. Both
   corrections above are this rule: a claim restated across briefs has been copied,
   and copying is how a false zero survives — it closes a question nobody re-opened.
4. **Instruments that disagree are evidence. Investigate the discrepancy — never
   average it, never pick the more convenient one, never call it noise.** Two probes
   differed by 37px on one cell. Chasing that difference, rather than resolving it,
   is the only reason the `--g-fit` defect was found before the work shipped.

Rule 4 is the only one of the four that would have caught `--g-fit` in advance.

---

## Ratified: the `--g-fit` patch, and why it broke an instruction

`paint()` opened with `if (!st || !bar) return;` and a later pass appended `fit()` to
its tail, so the fit was unreachable on every stage carrying `data-grow-nobar` — five
`wedo2-rule` stages, one per BUILD deck, left with only the async `ResizeObserver` as
a backstop. Visible as a reflow in the room; invisible to any synchronous check.

It was patched during a closing pass that said not to patch. The instruction existed
to stop scope creep, not to protect a false claim, and shipping a mechanism that
provably does not run on a whole class of stages while the evidence says it does
would have been the worse outcome. Now demonstrated to house standard — failing then
passing, both directions quoted, in `reports/CONVERGENCE_EVIDENCE_v3.md`.

---

---

## What the convergence work is, and what state it is in

The five Autumn 1 BUILD science lessons now run on the GROW engine through
`compat-build-anim.js`, so that the question "can `build-anim/` be deleted?" can be
answered from measurements. **It still cannot be answered without Matt walking the
slides** — see the walk sheet at the top of `reports/CONVERGENCE_EVIDENCE_v3.md`.

Three evidence passes, each re-running the same harness:

| pass | question | outcome |
|---|---|---|
| [v1](CONVERGENCE_EVIDENCE.md) | what breaks? | five findings, measured, none fixed |
| [v2](CONVERGENCE_EVIDENCE_v2.md) | fix them | five fixed, plus a sixth v1 got wrong |
| [v3](CONVERGENCE_EVIDENCE_v3.md) | close it | reserve derived, test widened, GROW re-injected |

## Merge timing — a point that is Matt's to weigh

**This branch is measurably better than `main` at every scaled viewport, and the
gap is not small.** As authored, stages clearing the navigation:

| viewport | `main` | this branch |
|---|---|---|
| 819×614 (1024×768 @125%) | 5/25 | **25/25** |
| 1093×614 (1366×768 @125%) | 7/25 | **25/25** |
| 683×512 (1024×768 @150%) | 0/25 | 5/25 |

with **zero regressions anywhere**, plus the We Do 2 slide going from 106–120px of
overflow to zero at 1280×720 and 1024×768.

Holding it unmerged keeps the worse state live through September. That is not an
argument for merging it unwalked — the walk answers a question no measurement can,
and slides 4 and 9 from the back of a real room is still the gate. It is an
argument for deciding *what the walk is for*: whether it gates the merge or
verifies it. **Sunday 6 September is the slot, and the call is Matt's.** Nothing
here merges either way.

## Open, and deliberately not closed here

- **`build-anim/` is not deleted.** Gated on the slide walk.
- **One test is red on purpose** — projector + long heading, 117/120 at nominal
  viewports. It documents a design limit: in every overflowing cell the picture is
  already at its 96px floor, so the overflow is the text. The floor does not move
  without Matt's say-so, and the reason is annotated at `grow-anim/grow-anim.js:620`.
- **Display scaling — fixed at 125%, open at 150%.** The We Do 2 slide is
  rearranged below a derived 960px height breakpoint: the same eleven elements in
  two columns, the sort activity keeping the width and the picture taking the
  narrow column. Nothing removed, reworded or hidden. **At 125% every stage now
  clears on every deck (25/25 at 819×614, 1093×614 and 1536×864, against 5/25,
  7/25 and — on `main` — failures at all three).** 1280×720 and 1024×768 go from
  106–120px of slide overflow to zero. What remains: at 819×614 the slide still
  *scrolls* by 70–153px (the scaffold and end-of-period note sit below the fold),
  and at 150% nothing in the layout layer helps — the slide has ~460px for content
  needing 1069px. Closing either needs a thirteenth slide or content moved, which
  changes what a pupil sees and is **Matt's**.
- **`.g-flow-orbit`** is recorded in `reports/REDUCED_MOTION_REGISTER.md`, not fixed
  here — it predates this work and belongs to the reduced-motion programme.
- **`build-anim/demo.html`** still loads the old files by `<script src>` and is the
  one page that genuinely breaks on deletion.
- **The BUILD/GROW philosophy divergence** — one engine, two stated intents — is
  unresolved. PR #10 is where that argument lives.
- **The circulation asset** is still unexercised by any lesson.

## The red assertions — two turned green, four remain

Left red deliberately. A red test that documents a design limit is worth more than a
green one that hides it.

| assertion | result | what it documents |
|---|---|---|
| nominal · as authored | **green** | was already green |
| nominal · caption wraps | **green** | was already green |
| nominal · long heading | **turned green** | the two-column arrangement absorbed it — the mechanism improved, no threshold moved |
| nominal · font 16→20px | **turned green** | same reason |
| scaled · as authored | red, 80/100 | 150% scaling only; 125% now clears entirely |
| scaled · caption wraps | red, 78/100 | as above, plus a wrapped caption |
| scaled · long heading | red, 56/100 | a heading over 57 chars at 150% scaling |
| scaled · font 16→20px | red, 64/100 | a larger font at 150% scaling |

Two turned green and neither threshold moved: `FLOOR` is still 96px and the heading
limit is still 57 characters. All four remaining reds are 150% display scaling,
where the slide has ~460px for content that needs 1069px.

The assertion that tests the *mechanism* rather than the outcome passes: of 173
overflowing cells across 1,080, **173 have the picture already at its 96px floor**.

## Named backlogs — filed, not opened

`reports/INSTRUMENT_INDEX.md`:

- **IDX-1 · early returns that skip trailing work** — the class `--g-fit` belonged
  to, with its search pattern and what a pass would have to prove. This estate has
  been bitten by it once, measurably.
- **IDX-2 · 27 instruments by register** — carried from the brief, **not verified
  here**. The count was not re-derived; recorded so it is not lost, marked so it is
  not inherited as fact.
- **IDX-3 · fill-mode enumeration, known incomplete** — carried from the brief, **not
  verified here**. Neither the enumeration nor the sense in which it is incomplete
  was checked.

IDX-2 and IDX-3 are marked unverified under rule 3, which is the point of the rule.


---

# Handover

## The distinction that must not be lost

At 125% display scaling, on the We Do 2 slide:

- **every stage now clears the navigation** — 25/25 at 819×614 and 25/25 at
  1093×614, against 5/25 and 7/25 on `main` before this landed; **and**
- **the slide still scrolls**, by 70–153px, because the scaffold box and the
  end-of-period note sit below the fold.

Both are true. They answer different questions — *is anything hidden under the
buttons* and *does the whole slide fit* — and the second is the one a teacher meets
in a room. **Do not let the 25/25 stand alone.**

## Walk sheet

**Slides 4 and 9, stood at the back of the room, on the real projector, at the
scaling the room is actually set to.**

Check the scaling first: right-click the desktop → Display settings → *Scale and
layout*. **125% is a common default on school hardware — assume it is on until you
have looked.** At 150% the four red test fixtures are exactly what you would be
looking at, and no layout change solves it.

Slide 4 is the first I Do — the biggest picture in the deck and the one that shrank
most (326px → 256px). Slide 9 is We Do 2 — the tightest layout in the unit.

## Corrections attributable to the briefs, not to the work

Three, all of the same shape — something asserted to exist that nobody had checked:

1. **The PR-stacking claim**, above.
2. **The reduced-motion register**, which did not exist at any path. Created as
   `reports/REDUCED_MOTION_REGISTER.md` with the assumption recorded inside it.
3. **Two filename collisions created by briefing two sessions into the same paths** —
   `reports/INSTRUMENT_INDEX.md` and `reports/SESSION_CLOSE.md`. Both sessions wrote
   the same paths in good faith. The index is now one file with two sections; the
   closes are now one file per session, which makes the collision structurally
   impossible rather than a matter of care.

## Named backlogs — filed, none opened

- **27 instruments by register** — `INSTRUMENT_INDEX.md` §1, four discrete passes
  BL-1 to BL-4, each naming the register to load first.
- **IDX-1 · early returns that skip trailing work** — §2, with its `rg` multiline
  guard-return pattern. The class `--g-fit` belonged to; this estate has been bitten
  by it once, measurably.
- **The fill-mode enumeration, known incomplete** — §1, *with its trigger stated*: it
  becomes load-bearing the first time anyone patches a call site instead of a gate.
- **IDX-4 · the width-aware breakpoint** — §2, with the full derivation table and the
  exact failing region. Deliberately not built.

## Open, and Matt's alone

Nothing below is decided here.

1. **Deleting `build-anim/`** — gated on the 13 September walk. It is present and
   byte-identical on `main`.
2. **The four glow decks.** `label_rest_check.js` is red on CAREERS_W6, COMM_W1,
   DUKE_W5 and LI_W2. **COMM_W1 reads as design and LI_W2 reads as a defect** — in
   LI_W2 the glowing element is the £1 answer to 20+20+10+50=100p, which gives the
   answer away. **CAREERS_W6 and DUKE_W5 need classifying design-vs-defect with
   their aria-labels quoted.** Not done here; the instrument stays red with its
   reason recorded rather than silenced.
3. **The BUILD/GROW philosophy divergence.** Both READMEs open with *"the animation
   is the explanation"*, while the pathway table says BUILD replaces text and GROW
   explains a process. One engine now serves both. PR #10 drew LAUNCH's distinction
   in markup; the BUILD/GROW one is still to be drawn.
4. **Smaller pictures on stages.** W6's plate went 326px → 256px at 1280×720. On
   `main` that stage was bigger *and* cut off by 20px.
5. **The 150%-scaling content question.** ~460px of slide for content needing
   1069px. No layout change solves it; it is a decision about how much a slide
   carries.

## Two things that are not risks, said plainly

- **The `build-anim-autumn1-v1` tag is uncreated**, at `297af43`. The proxy in this
  environment 403s `refs/tags/*` by ref type — it is not a permissions problem and
  not a failed attempt. It is a home-machine job and nothing depends on it.
- **`rm_budget.png` at `6f61323` was inspected.** It is a synthetic lesson frame: no
  roster, no register, no class list, no pupil name. Accepted in history and not to
  be rewritten. Said plainly because "an image in git history" alarms anyone reading
  cold.
