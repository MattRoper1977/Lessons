# Decision — the term-and-style quote limb

## Signature

> Decision signed by Matt Roper, 2026‑09‑18: the term‑and‑style quote limb is narrowed to the term·week token derived from SCIENCE_WEEK_BINDINGS. The sha256 limb is unchanged. Rationale as recorded in _sx3/DECISION_quote_limb.md

## What the limb is

`tools/catalogue/build_lesson_order.py` proves a Science deck's timing when the
deck's current bytes no longer match the `sha256` recorded for it in
`tools/catalogue/TERM_AND_STYLE_EVIDENCE.json`. Proof is granted by any one of
five limbs. The fourth was the *quote* limb: every `own title slide declaration`
quote recorded for the deck had to appear, whitespace-normalised, in the deck's
current text. Those recorded quotes are 750–1200 characters of title-slide prose.

## Why it is narrowed

The quote limb asserted the wrong thing. What the record needs to keep true is
the deck's **calendar binding** — which term and which week within that term the
lesson is taught. The recorded quote carries that binding in one token
(`Aut1·W3`) and then 700–1100 further characters of lesson title, exam-board
strapline, specification reference and objective wording, none of which the
binding depends on. Editing any of that surrounding prose — a retitle, a
reworded objective, a changed strapline — broke the limb without changing a
single fact the limb exists to protect.

The narrowed limb requires, from `SCIENCE_WEEK_BINDINGS.json`, every derived
term·week key for that deck to be present in the deck's current text, and still
requires a recorded `own title slide declaration` to exist. It compares the
binding and stops comparing the prose.

## What is unchanged

The sha256 limb — `approved_science[path] == digest` plus every recorded timing
quote — is untouched. So are the enrichment, explicit-cell and preserved-outcome
limbs. A deck that satisfies none of the five still fails, and for a
`recommended` deck that failure is an `AssertionError`, not a warning.

The deck's changed bytes are still recorded: `lesson-order.json` carries the new
`sourceSha256`, and `lesson-order.json` is itself digest-pinned in
`CATALOGUE_PINS`, so a byte change cannot pass through unremarked.

## Red proof

Measured 2026-09-18 on `Science_Teesside/Launch/SCI_L_W3_L1_Microscopy.html`
(`style: recommended`, binding key `Aut1·W3`), running the builder under the
original limb and the narrowed limb. Baseline, deck untouched: GREEN under both.

| mutation | bytes | original limb | narrowed limb |
|---|---|---|---|
| A — wrong token (`Aut1·W3` → `Aut1·W4`) | `bec6f261` → `3f12bd4b` | RED — `Recommended source needs current proof` | **RED** — same |
| B — token absent (token removed from the title slide) | `bec6f261` → `67d1a651` | RED — `Recommended source needs current proof` | **RED** — same |
| C — prose changed, token intact | `bec6f261` → `7e60f7f9` | RED — `Recommended source needs current proof` | GREEN — deck recorded as `refreshed`; `sourceSha256` in `lesson-order.json` becomes `7e60f7f937b3` |

A and B are the narrowing's teeth: it goes red on a wrong binding and on an
absent binding. C is the intended change of behaviour — prose drift alone no
longer fails a deck whose binding is intact — and the byte change is still
carried into `lesson-order.json`, whose own pin then requires a deliberate
re-stamp.

## Scope of the change

One expression in `tools/catalogue/build_lesson_order.py`. `lesson-order.json`
is byte-identical after the change (`--check` passes against the copy at
`origin/main`), because no deck on `main` currently differs from its recorded
evidence sha256 — the limb is dormant on `main` and fires only when a content
change lands ahead of a catalogue rebuild.
