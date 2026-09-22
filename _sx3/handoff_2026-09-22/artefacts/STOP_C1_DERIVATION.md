# STOP-C1 ruled option (a) — the derivation, and one thing the ruling could not have known

## The ruling's parenthetical names `data-kind`. That attribute does not exist here — and the obvious substitute is FORBIDDEN.

The ruling says: *"prefer explicit markers where a deck carries them (data-kind, then the
eyebrow label, then the heading phrase)"*.

Measured on all 34 decks (3 exemplars + the 31), 317 stages:

```
data-kind on the 317 stages: {'<absent>': 317}
```

`data-kind` is carried by **no** Science stage. The attribute Science decks *do* carry is
**`data-type`** (ido 60, wedo 70, independent 39, opening 28, arrival 36, starter 31,
exit 36, workshop 5, empty 12).

I was about to read `data-type`. **That is forbidden by STANDING INSTRUMENT RULE 5**, which
I found in `tools/hum/STAGE_IDENTITY_RULE.md` and in a comment block in `deck_dom.py` itself:

> **A stage is identified by its slide id — by what the deck declares for that slide — and
> never by the `data-type` attribute.** … `data-type` may still be styled on, counted and
> reported; it may never be the value an identity function returns.
> — Ruled by Matt, 2026-09-22 (Addendum 2 ruling 5, re-affirmed at A3.5 ruling 7)

The recorded rationale is that `data-type` is a **category, not an identity**: one value
covered "We do", "Check" and "Review" on 120 landed decks, which made `verify_loop` row 14
("the Title stage carries no panel") run over an empty `title_stages` set and pass without
testing anything, on more than half the estate.

So the ruling's `data-kind` was named deliberately and correctly. The estate simply has
neither `data-kind` nor a permitted attribute on Science. That leaves the ruling's second
and third routes: **the eyebrow label, then the heading phrase.**

## The eyebrow: the CLASS conflates, the TEXT does not

Every Science stage carries `<span class="slide-tag tag-NAME">TEXT</span>` — present on
**317 of 317** stages.

The **class** conflates exactly the way ruling 5 warns:

| eyebrow class | stages | eyebrow texts it covers |
|---|---:|---|
| `tag-wedo` | 70 | We do (37), **We do 2** (23), **Check** (5), **Review evidence** (5) |
| `tag-ido` | 60 | I do (37), **I do 2** (23) |
| `tag-arrival` | 42 | Arrival (36), Arrival task (3), **Opening** (3) |
| `tag-independent` | 39 | Independent (23), You do (11), **Refine** (5) |
| `tag-exit` | 39 | Exit (39) |
| `tag-starter` | 34 | Starter (34) |
| `tag-opening` | 28 | Opening (28) |
| `tag-workshop` | 5 | Workshop (5) |

`tag-wedo` covering "We do", "Check" **and** "Review evidence" is the identical failure
ruling 5 documents for `data-type`. **The class is unsafe.**

The **text** discriminates cleanly — fifteen distinct declared labels, each one a stage kind:

```
Opening · Arrival · Arrival task · Starter · I do · I do 2 · We do · We do 2 ·
Check · Review evidence · You do · Independent · Refine · Workshop · Exit
```

That is "what the deck declares for that slide", it is visible rendered markup rather than a
styling attribute, and it is not `data-type`. It is the ruling's second route, and it is the
one that survives.

## The derived expectations

Mapping the fifteen labels into the ruled allowed set, with `MODELLING_STAGES = {ido, ido2}`
and `title` the only other exclusion:

| stages | title | ido + ido2 | **row45 expected** | decks |
|---:|---:|---:|---:|---:|
| 7 | 1 | 1 | **5** | 3 |
| 8 | 0 | 2 | **6** | 3 |
| 9 | 1 | 2 | **6** | 20 |
| 13 | 1 | 1 | **11** | 5 |

**Unresolved eyebrow labels: NONE.** Total expected panels across the 31: **208**.

The nine-stage limb derives to **6** — the order's stated figure, now derived rather than
typed. That the two agree is the check on the method, not a coincidence to be assumed.

## Three shapes looked wrong and were checked rather than trusted

- **8-stage LAUNCH Classic has no title stage at all** (`title=0`). Verified by dumping the
  deck: it opens directly on `Arrival`. Not a detection failure — real structure.
  **This has a consequence worth a ruling of its own:** `verify_loop` row 14 (P1-1, "the
  Title stage carries no panel") will run over an empty `title_stages` on those 3 decks and
  pass without testing anything — precisely the failure mode ruling 5 exists to prevent.
- **13-stage GROW Explore is a 7-stage Classic plus a 6-stage extension** — it carries two
  `Arrival` and two `Exit` stages. Real structure, verified by dump.
- **7- and 13-stage decks carry only one modelling stage** ("I do", no "I do 2"). Real.

Note that the mapping choice among the *non-modelling* labels (Workshop / Refine / Check /
Review evidence → independent or review or check) **cannot change the expectation**: none of
them is `title` and none is in `MODELLING_STAGES`. Only `Opening→title` and
`I do`/`I do 2`→`ido`/`ido2` move the number. Those three are the ones that had to be right.

## Status

Nothing implemented yet. Five adversarial lenses are reviewing this plan before any code is
written — ruling-5 compliance (including whether the eyebrow is mechanically generated from
`data-type`, which would make reading it an evasion), Humanities regression, conflation
across the wider Science estate, the edge-case arithmetic, and downstream blast radius.

---

# RULING 1's CONDITION, TESTED DIRECTLY — the eyebrow text is NOT a projection of `data-type`

Ruling 1: *"if the text is a 1:1 mechanical projection of data-type it is an evasion and the
fix moves to the heading phrase; if it distinguishes labels data-type conflates (as measured:
15 vs a category), it is the deck's declaration."*

Measured, 34 decks, 317 stages, `data-type` → the eyebrow texts it covers:

| `data-type` | n | distinct eyebrow texts it covers | |
|---|---:|---|---|
| `wedo` | 70 | We do (37), **We do 2** (23), **Check** (5), **Review evidence** (5) | ← one type, **four** labels |
| `ido` | 60 | I do (37), **I do 2** (23) | ← one type, **two** labels |
| `independent` | 39 | Independent (23), **You do** (11), **Refine** (5) | ← one type, **three** labels |
| *(empty)* | 12 | **Opening** (3), **Arrival task** (3), **Starter** (3), **Exit** (3) | ← one type, **four** labels |
| `arrival` | 36 | Arrival (36) | 1:1 |
| `exit` | 36 | Exit (36) | 1:1 |
| `starter` | 31 | Starter (31) | 1:1 |
| `opening` | 28 | Opening (28) | 1:1 |
| `workshop` | 5 | Workshop (5) | 1:1 |

```
distinct data-type values : 9
distinct eyebrow texts    : 15
```

**VERDICT: NOT a 1:1 projection.** Four of the nine `data-type` values each cover two to four
distinct declared labels. The eyebrow text distinguishes precisely what `data-type` conflates
— and note *which* conflation it resolves: `data-type="wedo"` covering **"We do", "Check" and
"Review evidence"** is the identical failure ruling 5 was created to prevent, reproduced on
Science. Reading the eyebrow text does not re-enter through the back door; it is the route
that repairs the conflation.

Under ruling 1 the condition is therefore met: **the eyebrow text is the deck's declaration**,
and it, never the class and never `data-type`, is the Science stage-identity source.

This is my own measurement. The independent lens verdict — specifically whether some generator
in this repo emits the eyebrow mechanically *from* `data-type`, which would change the answer —
is pending and will be recorded beside this rule as ruling 1 requires.
