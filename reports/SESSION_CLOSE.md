# Session close — BUILD/GROW convergence

**Branch:** `claude/convergence-prep` · **PR #12** · **base:** `main` at `cacaf16977646b40f0ff72c9e5112a7f31877679`
Nothing merged. Nothing pushed to `main`. `build-anim/` byte-identical to `main`.

---

## Correction: PR #13 was never stacked on PR #10

Stated first because it is a correction to the record rather than a finding, and
because it was carried, unchecked, into three separate briefs.

**What was claimed:** that PR #13 was stacked on PR #10 and needed re-pointing.

**What is true**, from `GET /repos/MattRoper1977/Lessons/pulls?state=all`:

| PR | branch | base | head |
|---|---|---|---|
| #10 | `claude/launch-animation-philosophy-79lohp` | `main` @ `cacaf16` | `d944207` |
| #11 | `claude/grow-anim-unused-svg-ids` | `main` @ `cacaf16` | `88bc8f4` |
| #12 | `claude/convergence-prep` | `main` @ `cacaf16` | `c866582` |
| #13 | `claude/gate-census` | `main` @ `cacaf16` | `2dcd6aa` |

All four base on `main` at the same SHA. **There is no stacking and nothing to
re-point.** `claude/convergence-prep` is PR #12's own branch, not a stray.

**Where it came from.** The claim originated in an earlier session's report, and
was carried into two subsequent briefs and a project ledger without being checked
against the API. By its third appearance it read as established fact. It was not
verified by this session either until the API was queried in the closing pass —
and it was queried only because the brief asked for a re-point command that did
not make sense against what the branches actually showed.

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

## The four rules this session earned

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

## Open, and deliberately not closed here

- **`build-anim/` is not deleted.** Gated on the slide walk.
- **One test is red on purpose** — projector + long heading, 117/120 at nominal
  viewports. It documents a design limit: in every overflowing cell the picture is
  already at its 96px floor, so the overflow is the text. The floor does not move
  without Matt's say-so, and the reason is annotated at `grow-anim/grow-anim.js:620`.
- **Display scaling — Matt's open decision, quantified.** At 125% the only stage type
  that fails is `wedo2-rule`, on all five BUILD decks: **one template, which makes it
  tractable**. It is **pre-existing** — `main` clears 5 of 25 at 819×614 where this
  branch clears 20, with zero regressions anywhere. The cause is content volume, not
  layout: the slide renders 11 elements totalling 708px into 543px of slide, and the
  picture is already at its 96px floor. It needs 665–762px of viewport height to fit
  as authored; 614px is 51–148px short. Four options with costs are laid out in v3
  and **none is chosen**. At 150% every stage type fails and only a deck redesign
  would help.
- **`.g-flow-orbit`** is recorded in `reports/REDUCED_MOTION_REGISTER.md`, not fixed
  here — it predates this work and belongs to the reduced-motion programme.
- **`build-anim/demo.html`** still loads the old files by `<script src>` and is the
  one page that genuinely breaks on deletion.
- **The BUILD/GROW philosophy divergence** — one engine, two stated intents — is
  unresolved. PR #10 is where that argument lives.
- **The circulation asset** is still unexercised by any lesson.

## The four red assertions, and what each documents

Left red deliberately. A red test that documents a design limit is worth more than a
green one that hides it.

| assertion | result | what it documents |
|---|---|---|
| nominal · long heading | 97/100, worst −25px | a heading over 57 characters on a We Do 2 slide does not fit a 720px projector. Now linted so it cannot be authored by accident |
| scaled · as authored | 70/100, worst −241px | the 125%/150% finding above — pre-existing, improved, unfixed |
| scaled · caption wraps | 70/100, worst −256px | the same slide with a two-line caption |
| scaled · font 16→20px | 59/100, worst −366px | the derived reserve absorbs a larger font on most stages and cannot once the picture is at its floor |

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
