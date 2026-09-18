# The 55 drifted week bindings — three buckets, reported not fixed

ORDER SX3-M2 §5(b). Reporting only. Nothing here is repaired in this release;
these are the inputs to the shelf-restore order (§5d).

## Search scope

The 55 shelf decks whose current bytes differ from their recorded
`sourceSha256` in `tools/catalogue/SCIENCE_WEEK_BINDINGS.json`, measured at
`origin/main`. Each bucketed by what, if anything, still re-proves its binding in
the **current** text: the recorded evidence quote as a whole; the binding in
**token** form (`Aut2·W7`); the binding in **label** form (matched by the
estate's own `term_codes` regex, `\b(Aut|Spr|Sum)(?:umn|ing|mer)?\s*([12])…`);
or nothing.

## Correction to the first report

My readback of 2026-09-18 gave these as 36 / 1 / 18. Re-measured with the label
instrument added, the true split is **35 / 1 / 1 / 16 / 2**. Two changes:

- the one I reported as "not provable" **is** provable — see Bucket 2;
- the 18 "nothing to re-prove against" split into 16 with nothing and 2 whose
  binding records no week at all, which is a different defect.

## Bucket 1 — mechanical re-stamp: 37

**35** still carry their recorded evidence quote verbatim (Build 5 · Grow 13 ·
Launch 17). Their bytes moved; their evidence did not. Re-stamping
`sourceSha256` is a byte operation with no editorial content.

**1** (Bucket 1b) has a broken quote but carries the binding in **token** form:
`Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html` (`Aut1·W4`). The quote broke
because the words `Knowledge organiser` were inserted into the title slide.

**1** (Bucket 2, below) is provable by label form.

## Bucket 2 — quote broken, binding present only in LABEL form: 1

`Science_Teesside/Grow/Autumn2_W7_2026-27/SCI_G_A2_W7B_Autumn_Science_Evidence_Do.html`
(`Aut2·W7`). This is the one I first called unprovable. It is not.

Recorded quote:

```
Lesson overview GROW · Science · Autumn 2 · Week 7 · Do Autumn Science: …
```

Current slide 1:

```
Lesson overview GROW · Science · Lesson 2 of 2 · Do GROW · Science · Autumn 2 · Week 7 · Do Autumn Science: …
```

A breadcrumb — `Lesson 2 of 2 · Do GROW · Science ·` — was inserted into the
middle of the recorded quote. The longest matching prefix is 30 characters. The
binding facts, `Autumn 2 · Week 7`, are still present, verbatim and in order.

**This is the same evidence-model defect as the quote limb, and it is the same
defect twice over.** The whole-quote comparison fails on an inserted breadcrumb
that changes no fact. And the narrowed limb would also fail here, for a second
reason: it looks for the key in **token** form (`Aut2·W7`), and this deck writes
it in **label** form.

## Bucket 3 — nothing in the current text re-proves the binding: 16

Build 3 · Grow 7 · Launch 6. Named:

| route | binding |
|---|---|
| `Build/W8-W13_2026-27/SCI_B_W9A_Rock_Evidence_Explore.html` | `Aut2·W2` |
| `Build/W8-W13_2026-27/SCI_B_W13A_Fair_Test_Planner_Change_One_Thing_Explore.html` | `Aut2·W6` |
| `Build/W8-W13_2026-27/SCI_B_W13B_Method_Pilot_Test_The_Test_Do.html` | `Aut2·W6` |
| `Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html` | `Aut2·W1` |
| `Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html` | `Aut2·W1` |
| `Grow/W8-W13_2026-27/SCI_G_W11A_Global_Warming_Explore.html` | `Aut2·W4` |
| `Grow/W8-W13_2026-27/SCI_G_W11B_Climate_Action_Do.html` | `Aut2·W4` |
| `Grow/W8-W13_2026-27/SCI_G_W12A_Science_Connections_Explore.html` | `Aut2·W5` |
| `Grow/W8-W13_2026-27/SCI_G_W13A_Rover_Rescue_Plan_Explore.html` | `Aut2·W6` |
| `Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html` | `Aut2·W6` |
| `Launch/W8-W13_2026-27/SCI_L_W11L2_Benefit_Risk_Uncertainty_Explore.html` | `Aut2·W3` |
| `Launch/W8-W13_2026-27/SCI_L_W12L1_DNA_Hierarchy_Introduce.html` | `Aut2·W4` |
| `Launch/W8-W13_2026-27/SCI_L_W12L3_Fruit_DNA_Evidence_Do.html` | `Aut2·W4` |
| `Launch/W14-W15_2026-27/SCI_L_W14L1_Genetic_Condition_Research_Introduce.html` | `Aut2·W6` |
| `Launch/W14-W15_2026-27/SCI_L_W14L2_Genetic_Condition_Source_Evidence_Explore.html` | `Aut2·W6` |
| `Launch/W14-W15_2026-27/SCI_L_W14L3_Genetic_Condition_Presentation_Do.html` | `Aut2·W6` |

Every one is an `Aut2` binding. These decks carry a binding in the record and
nothing in themselves to confirm it against. This is the evidence-model defect at
its sharpest: the record asserts a fact the artefact does not restate, so the only
thing holding the binding is the byte hash — and the bytes have already moved.

## Bucket 4 — the binding records no week at all: 2

`Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html` and
`Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html`. Both appear
in the audit's own `unsetWeekRoutes` list. There is nothing to re-prove; there is
a week to establish.

## The defect these share, named

The estate writes the same binding in **three** forms, and every instrument that
asks "is the binding still there" picks one form and only one:

| form | example | decks of 129 carrying it |
|---|---|---|
| token | `Aut2·W7` | 36 |
| label only | `Autumn 2 · Week 7` | 8 |
| neither — the deck does not restate its binding | — | **81** |

`build_catalogue.py`'s `term_codes()` and `build_lesson_order.py`'s
`weeks_from()` both accept either form. The **quote limb**, old and new, accepts
only one: the old one required the whole recorded sentence, the new one requires
the token. So the narrowing landed in #586 is still strictly better than what it
replaced — it goes red on a wrong or absent binding, and it survives prose edits
— but it narrows to a *form*, not to the *fact*.

Recorded as an input to the shelf-restore order, not repaired here. Widening the
limb to accept the label form is a gate change, and there is no CI-edit budget.
