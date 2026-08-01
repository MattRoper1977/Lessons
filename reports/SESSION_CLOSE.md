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

### The rule this adds

Two rules already govern this work — a measurement adjacent to the claim is not the
claim, and an aggregate cannot clear a per-instance claim. This is the third, and it
applies to briefs and reports as much as to code:

> **A fact repeated across documents has been copied, not verified. Re-derive it at
> its source before acting on it.**

Repetition is not corroboration. A claim restated across briefs has been copied, and
copying is exactly how a false zero survives: it closes a question nobody re-opened.
The same shape appeared twice more in this session — once when a brief routed a
finding to "the RM programme's own register", which did not exist (see
`reports/REDUCED_MOTION_REGISTER.md`), and once when two of my own probes disagreed
by 37px and only cross-checking them exposed a real bug in what I had shipped.

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
- **Display scaling is a genuine finding, reported not patched.** At 125% and 150%
  Windows scaling, content goes under the navigation on all five BUILD lessons as
  authored. It is far worse on `main` than on this branch and there are zero
  regressions, but it is not fixed. Numbers in v3.
- **`.g-flow-orbit`** is recorded in `reports/REDUCED_MOTION_REGISTER.md`, not fixed
  here — it predates this work and belongs to the reduced-motion programme.
- **`build-anim/demo.html`** still loads the old files by `<script src>` and is the
  one page that genuinely breaks on deletion.
- **The BUILD/GROW philosophy divergence** — one engine, two stated intents — is
  unresolved. PR #10 is where that argument lives.
- **The circulation asset** is still unexercised by any lesson.
