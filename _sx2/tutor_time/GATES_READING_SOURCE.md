# D27 — pupil-visible gates that still read source

Listed, not fixed. LF1M-FIN §A forbids repairing them in this order.

A gate is in scope if **its subject is what a pupil can see**. Gates whose subject
is a file, a digest, a path or a build artefact are out of scope however they read
their input, and are named at the bottom so the exclusion is visible rather than
assumed.

---

## 1. `tools/relabel_public.py` — `--gate`, `--report`

**The estate's most consequential one.** `FORBID` is a regex over HTML source; the
gate's verdict — `GATE PASS` / `GATE FAIL (n hits)` — is a claim about pupil-facing
calendar tokens.

It already has **two recorded symptoms**, both of which a rendered gate would not
have:

- **D20 UNSEEN.** The census pattern is case-insensitive and the rewriter's is not,
  so `Absolute week 14` on four `START_HERE` pages is counted by the gate and
  invisible to the rewriter — neither resolved nor refused. A bare `W9B` is
  invisible to both, because `\bW\d+\b` needs a word boundary after the digit.
- **D21.** 75 of 205 refusals are a **numbered question** (`W1.` `W2:`), not a week
  — 59 of the 68 F1 refusals. The gate cannot tell a worksheet's first question
  from week 1 because it never sees either rendered.

Neither is fixed here. Narrowing `FORBID` changes what the gate blocks on.

## 2. `tools/verify_cross_estate_unification.py` — `visible_body_sha256`

The pin's own name states a pupil/user-visible subject, and its value is a digest
of **source body bytes**. A source digest and a rendered body are different things:
the digest moves when a comment moves, and holds when a stylesheet hides a
paragraph.

---

## Checked and out of scope

| tool | why |
|---|---|
| `tools/lf1/render_census.cjs` | already rendered — the standard D13 set |
| `tools/lf1/gate_thirdparty.cjs` | already rendered, two-sided control (D24 iii, D28) |
| `tools/verify_hud_on_lessons_games.mjs` · `tools/verify_lessons_chips.mjs` | already rendered |
| `tools/lf1/check_admission_move.py` | subject is a registry row, not a pupil |
| `tools/verify_fixture_names.mjs` | subject is a fixture filename |
| `tools/rx3_land.py` · `tools/rx3_scenes.py` · `tools/build_staff_pack.py` | writers and builders, not gates |
