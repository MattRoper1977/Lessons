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

## What landed, and in what order

**Final `main` is `cf2971b11ff58cb396257c0b8f9631bd8c5b0c8d`.** Six merges, gated
between each, no force push and no rebase of pushed work:

| # | what | merge SHA |
|---|---|---|
| 10 | LAUNCH: animation that supports reasoning | `0047e8a` |
| 13 | gate & instrument census | `e68d1bc` |
| 11 | unused SVG ids in grow-anim | `cce5030` |
| 12 | BUILD/GROW convergence — prep, fixes, closing pass | `1158d96` |
| 14 | BUILD_ASDAN visual teaching layer | `214669a` |
| 15 | rebuild the pinned grow-motion dist | `cf2971b` |

**#15 belonged to no PR, and a cold reader will otherwise take it for someone's
mistake.** `launch-engine/check.js` reported `dist/grow-motion.min.css` stale —
pinned `db3fd9602a69eb20`, actual `83bdca2c9898413e`. #10 pins each `dist/` source's
SHA-256 so staleness is a hard failure; #12 changed `grow-anim/grow-motion.css` for
the `draw` fix. **Neither PR was wrong and neither could have seen it**: the
divergence existed only once both were on `main`. Post-merge verification found it,
it took its own change to close, and it is now standing rule 21.

**#13 needed re-pointing before it could merge.** Its base was still
`claude/launch-animation-philosophy-79lohp` when #10 landed, so merging it then would
have put it on a dead branch rather than on `main`. Changed with
`update_pull_request` — **not** the rebase-and-force-push its own body suggested,
because rebasing pushed work was forbidden. Diff re-confirmed after the change: **26
files, 1,049 insertions**, against 35 files and 5,548 had it merged unstacked.

## Post-merge staleness sweep — every pin instrument, once, on merged main

#15 proved that a generated artefact can go stale in the *combination* of two
correct PRs. Six landed together, so every other pinned or generated artefact was in
the same position. All of them were run on merged `main`, and the greens are part of
the deliverable:

**27 instruments reported · 7 CLEAN · 3 reported STALE and all three refuted · 13 not
staleness checks · 4 not run (write-only, no check mode).**

| instrument | verdict |
|---|---|
| `Science_Teesside/launch-engine/check.js` | **CLEAN** — all three dist pins re-derived independently: `sci-engine.min.js` `7acd485f`, `sci-engine.min.css` `6abc48d5`, `grow-motion.min.css` `83bdca2c`, each matching its source |
| `Science_Teesside/launch-engine/inject.js --check` | **CLEAN** — "0 file(s) would change" across all 15 LAUNCH decks; verifies both hops, dist-vs-source and deck-vs-dist |
| `BUILD_ASDAN/_framework/apply_framework.py --check` | **CLEAN** — `asdan-teach.css`/`.js` inlined into 31 decks, all current |
| `grow-anim/inject.py --check` | **CLEAN** — ok ×5 |
| `reports/convergence/inject_convergence.py --check` | **CLEAN** — ok ×5 |
| `build-anim/inject.py --check` | reported STALE → **refuted** |
| `grow-anim/wire_lessons.py --check --patch-only` | reported STALE → **refuted** |
| `LundyLoop/tools/ko_staleness.py` | reported STALE → **refuted** |
| 13 others (`gate-leak.js`, `health.js`, `verify_commit_set.py`, `preflight.py`, `sitemap_audit.py`, `qa_check.py`, `style_check.js`, `_passla/build/gates.py`, `_passsci1/gates.py`, `batch_gate.py`, `hub_chip_gate.js`, `verify_axiomshift.sh`, `verify_charcoal.sh`) | **not staleness checks** — they assert behaviour, counts or accessibility, and were reported as such rather than forced into the frame |
| 4 write-only (`build.js`, `prune_dead_css.py`, and two generators) | **not run** — no check mode; running them would repair the evidence |

**Why each STALE claim fell, because a refuted claim is only useful with its reason:**

- **`build-anim/inject.py`** exits 1 on the five BUILD lessons *by design*: #12
  deliberately re-pointed them at `grow-anim/`, so the injector is measuring against
  sources those files are no longer generated from. Probed per-block, the three
  libraries `build-anim/` still owns are **byte-identical** — `BODY 16125 vs 16125`,
  `FOOD 38016 vs 38016`, `CHAIN 16318 vs 16318` — the whole difference is a 48-byte
  provenance header. Coverage is not lost: those three are read from `build-anim/` by
  `inject_convergence.py`, which is green.
- **`grow-anim/wire_lessons.py --patch-only`** reports 289 STALE, and **structurally
  cannot detect drift** — proved, not argued: a lesson was given genuinely stale
  inlined content in a scratch copy and the tool passed it, exit 0. Its "STALE" means
  "has not yet received the patch". The same 289 files, byte-identical set, fail at
  `cacaf16` before any of the six merges. It is a rollout backlog, merge-invariant.
- **`ko_staleness.py`** produces 131 candidates and its own docstring forbids the
  reading: *"The output is a CANDIDATE LIST for reading, never a defect count."* The
  same output was adjudicated in Pass Q — `_passq/TRIAGE.md`: **"Result: 0 STALE. 0 KO
  edits."** Its top-ranked flag is byte-frozen since that read. It also refuses to run
  at all in this shallow clone rather than returning a false zero, which is standing
  rule 16 doing its job.

**Nothing on merged `main` is stale.** The one artefact that was is closed by #15.

**One piece of tooling hygiene, recorded not fixed:** `build-anim/inject.py` will now
always exit 1 on those five lessons, and `build-anim/README.md` still advertises it as
a CI-style check. Nothing invokes it — no workflow file and no git hook — so nothing
is broken today. Whether to retire it as a gate or teach it that those five lessons
belong to `inject_convergence.py` is a decision, and it sits with the `build-anim/`
deletion question rather than apart from it.


## The walk now verifies live decks, not a branch

That was Matt's call, and it is recorded as his. What it changes: **a problem found
on 13 September is live while it is being fixed.** So the revert-not-forward-fix rule
applies to anything the walk turns up, exactly as it applied during the merge — revert
to a known-good `main`, confirm clean, document, and only then decide the fix. A
hurried patch to a live deck in September is the failure mode this ordering exists to
avoid.

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


---

# Handover

## The distinction that must not be lost

At 125% display scaling, on the We Do 2 slide:

- **every stage now clears the navigation** — 25/25 at 819×614 and 25/25 at
  1093×614, against 5/25 and 7/25 before; **and**
- **the slide still scrolls**, by 70–153px, because the scaffold box and the
  end-of-period note sit below the fold.

Both are true. They answer different questions — *is anything hidden under the
buttons* and *does the whole slide fit* — and the second is the one a teacher meets
in a room. **Never let the 25/25 stand alone.**

## What was verified, and what was not

Five PRs were verified **structurally, not pedagogically.** On merged `main`:
`inject.py --check` clean on all ten decks · 12/12 slides on the five BUILD decks and
10/10 on the five GROW · 110 renders · print packs byte-for-byte identical across all
three tiers · 670 script-step target resolutions with none matching zero elements ·
one `/hud.js` 404 per BUILD deck and two per GROW, nothing new · the display gate and
the fit gate both green · every pin consistent.

**None of that says whether a LAUNCH gate reads right to a Year 10, or whether a
256px plate reads from the back row.** Those are the questions the walk exists for,
and no instrument in this estate can answer either.

## Rule 19 was applied to this document, twice

Left visible because it is the rule working rather than a tidy-up. The PR-stacking
correction was **rewritten as a sequence** rather than appended to, once #13 became
genuinely stacked and the original wording began contradicting the facts. And two
sections duplicated by the handover — an earlier "Open" list and an earlier "Named
backlogs" — were **removed**, not left beside their replacements. A reader cannot
tell which of two contradictory claims is live, and will reasonably pick whichever
suits them.

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
2. **The four glow decks — all four now classified against one standard.**
   `label_rest_check.js` settles 5s past arrival, then samples a repeating 6s cycle
   and fails any label whose effective opacity ever drops below 1. All four decks
   fail on exactly one glyph, all at ~0.35, and **in every case every other text in
   the diagram stays at opacity 1.** So the question is only ever: *is the dimmed
   glyph something a pupil must read or produce?*

   | deck | glyph | the deck's own `aria-label` | everything else at rest | verdict |
   |---|---|---|---|---|
   | `LI_W2_Notes_and_Coins` | `£1` @5550ms | — | `20p 20p 10p 50p` `=` `20 + 20 + 10 + 50 = 100p` `DIFFERENT COINS, SAME POUND` all at 1 | **defect** |
   | `COMM_W1_Choose_Our_Asset` | `🌳 🏞️ 🏫` @450/1050/1650ms | *"three community spots glow"* | all other labels at 1 | **design** |
   | `DUKE_W5_Our_Social_Enterprise` | `💡` @2850ms | *"An idea bulb lights, earns a coin, and the coin powers a heart"* | `OUR IDEA` `£` `WE SELL · WE EARN` `IT HELPS SOMEONE` `PROFIT WITH A PURPOSE` all at 1 | **design** |
   | `CAREERS_W6_My_Career_Profile` | `✓` @3600ms | *"Pieces of a career profile fly in and assemble into one card"* | `👤` `ME` `MY STRENGTHS` `MY EVIDENCE` `🏁 MY NEXT STEP` `MY CAREER PROFILE — BUILT FROM PROOF` all at 1 | **design, weakly** |

   **`LI_W2` is the defect and it is the clearest case in the set:** the single dimmed
   glyph is `£1`, which is the answer to the sum printed beside it at full opacity.
   The animation dims the one thing the pupil is there to work out.

   **`DUKE_W5` is design by the deck's own account of itself.** Its `aria-label`
   promises *"an idea bulb **lights**"* — the pulse is the first beat of the described
   animation, and the word `OUR IDEA` that the bulb decorates never dims.

   **`CAREERS_W6` is design but the weakest of the three**, and the reason is worth a
   sentence rather than a tick. Nothing a pupil must read or produce dims: the `✓`
   prefixes `MY CAREER PROFILE — BUILT FROM PROOF`, which stays at 1 and carries the
   same meaning. But unlike `DUKE_W5` and `COMM_W1`, **the deck's `aria-label`
   describes assembly and says nothing about a recurring pulse** — so the motion and
   the deck's own description of it have drifted apart. That is a documentation gap,
   not a legibility one.

   **The ruling is Matt's.** The instrument stays red on all four with its reason
   recorded, rather than silenced — a red test that documents a decision is worth more
   than a green one that hides it.
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
