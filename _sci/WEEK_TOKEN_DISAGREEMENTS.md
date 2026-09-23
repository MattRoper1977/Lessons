# The decks whose own week claim disagrees with their binding

> **CORRECTED 2026-09-23 — Matt's ruling 3 on the Science limbs review. The four BUILD decks were
> never a deck defect; the READER was.** Each deck's only `Aut1·W3`-style week is a correct line on
> a later stage recalling the PREVIOUS lesson ("Retrieve the actual previous lesson: Aut1·W3 —
> vertebrates have an internal skeleton…"). Its title stage states no term·week at all ("BUILD ·
> Science · Week 4A · Explore"). The limb read the whole deck and took a recall line for the deck's
> own claim.
>
> **Fixed in the reader, not in the decks.** Only the TITLE STAGE — the first top-level slide, its
> meta line included — counts as the deck's claim. `tools/hum/admit_transaction.py`
> (`title_stage_text`) and `tools/catalogue/build_lesson_order.py` (`deck_statement_text`) read the
> same stage. Recall and review text on later stages is ignored. Red proofs: a title stage claiming
> the wrong week still refuses in both tools; the same wrong week read over the whole deck would have
> refused the recall deck; `science_allowed` lands SCI_B_W4A only through the title-stage reader.
>
> **Re-measured on the limbs PR, bytes moved:**
>
> | deck | admission (`judge_science`) | re-stamp oracle (`derive()`) |
> | --- | --- | --- |
> | `SCI_B_W4A_Muscles_Explore.html` | LANDABLE, form (iv) | proved by the Science row limb, `Aut1·W4` |
> | `SCI_B_W5A_Body_Needs_Explore.html` | LANDABLE, form (iv) | proved by the Science row limb, `Aut1·W5` |
> | `SCI_B_W6A_Balanced_Plate_Explore.html` | LANDABLE, form (iv) | proved by the Science row limb, `Aut1·W6` |
> | `SCI_B_W7A_Food_Sources_Explore.html` | LANDABLE, form (iv) | proved by the Science row limb, `Aut1·W7` |
>
> All four can join a batch (their route is `Build/v3_40min/`: the Aut1 v3 sets, autonomy order item
> 3). Across all 180 bound decks, the reader change moves exactly these four from REFUSED to
> LANDABLE and no other deck. Estate-wide, 40 decks state a week on the title stage only, 11 on the
> title stage and later stages, these 4 on later stages only, and 125 nowhere. No deck states one
> in its `<head>`.
>
> **The fifth, SCI_G_W16B — STAYS REFUSED (Matt, 2026-09-23).** Measured on Lessons main
> `f99d651d`, it had been LANDABLE, and the reason was not the label parser: the parser has no
> range check and reads "Spring 1 · Week 16" as the claim `Spr1·W16`. It landed through the COVER
> rule: its own lesson-config cell `'GROW Weekly - Spring'!C29` adds `Spr1·W2`, and {`Spr1·W16`,
> `Spr1·W2`} covers its row `Spr1·W2`. Ruled: a week the TITLE STAGE claims that the row does not
> bind is a refusal, whatever another form covers. `admit_transaction.judge_science` and
> `build_lesson_order` (`title_claim_conflict`) both now refuse it: "the deck's title stage states
> Spr1·W16, which its row (Spr1·W2) does not bind". Across all 180 bound decks this refuses W16B and
> no other deck; on moved bytes it is the only deck proved before and refused now.
>
> **Totals, measured** (`admit_transaction.science_allowed` over the 180 decks bound in
> `SCIENCE_WEEK_BINDINGS.json`): Lessons main `f8cc300a` admits **172** and refuses 8 (the four no-week
> BUILD decks W8A, W8B, W11A, W11B and B_W4A–W7A). After this PR it admits **175** and refuses **5**: the
> same four no-week decks and SCI_G_W16B. The count table further down (171 landable) predates both
> measurements.
>
> **Recorded for the transplant.** The visible label is wrong for pupils and teachers. When PASS C
> re-cuts W16B, its title-stage token and label are DERIVED from the row (`Spr1·W2`, "Spring 1 ·
> Week 2"), never typed.
>
> The sections below are kept as they were written; where they disagree with this correction, the
> correction governs.

**Ruled by Matt Roper, 2026-09-22 (on the STOP-B3 limb measurement): the ROW is right.**

The widened Science limb (four accepted forms of a deck stating its own term-week) made a
disagreement visible that the limb as first written could not distinguish from silence: a deck
that states a week, and states a *different* one from the row the signed record binds it to.
Estate-wide there are **five**: four consecutive BUILD Explore decks, ruled below, and one GROW
deck found later, recorded in its own section.

| deck | route | the deck says | the row says | pack manifest | calendar spine cell |
| --- | --- | --- | --- | --- | --- |
| `SCI_B_W4A_Muscles_Explore.html` | `Science_Teesside/Build/v3_40min/` | `Aut1·W3` | **`Aut1·W4`** | `Aut1·W4 — Explain how muscles work in pairs…` | `'BUILD Weekly - Autumn'!C35` → `Aut1·W4` |
| `SCI_B_W5A_Body_Needs_Explore.html` | `Science_Teesside/Build/v3_40min/` | `Aut1·W4` | **`Aut1·W5`** | `Aut1·W5 — …` | `'BUILD Weekly - Autumn'!C36` → `Aut1·W5` |
| `SCI_B_W6A_Balanced_Plate_Explore.html` | `Science_Teesside/Build/v3_40min/` | `Aut1·W5` | **`Aut1·W6`** | `Aut1·W6 — …` | `'BUILD Weekly - Autumn'!C37` → `Aut1·W6` |
| `SCI_B_W7A_Food_Sources_Explore.html` | `Science_Teesside/Build/v3_40min/` | `Aut1·W6` | **`Aut1·W7`** | `Aut1·W7 — …` | `'BUILD Weekly - Autumn'!C38` → `Aut1·W7` |

## The basis, as measured

Four independent records agree on the later week for every one of the four: the **filename**
(`W4A`…`W7A`), the pack's own **manifest** row (`manifest-v3.json`, quoted verbatim in the
binding's evidence), the **calendar spine** cell that carries that outcome (C35–C38, consecutive),
and the **signed** `SCIENCE_WEEK_BINDINGS` row itself. Only the deck's own text says otherwise,
and it is wrong by exactly one week on four consecutive Explore decks.

That offset pattern is the ruling's reason: each Explore deck was cloned from the previous week's
and its week token carried forward. **A deck disagreeing with three independent records by the
same offset is a deck defect, not a scheme question.** The spine match for W6A is at 0.99 rather
than 1.00: the two texts differ only in the capitalisation of "FoodWise"/"Foodwise".

## Status

* The four are **REFUSED** by the limb — as they should be: form (iv), which proves a deck that
  states nothing by the signed row alone, deliberately does not swallow a deck that states a
  *different* week. That refusal is red-proved in `tools/hum/admit_transaction.py --self-test`.
* **No edit now.** Neither the decks nor the record is touched under this ruling.
* They close at **PASS C**, when the transplant derives the token from the binding rather than
  leaving the typed one in place; the disagreement then disappears because the deck stops
  asserting a week of its own.

---

# The fifth: a GROW deck that writes its pack number into the label

Found on 2026-09-22 while measuring Spring 1 for B1, on the signed record whose digest was
verified equal to its pin (`2f7ea74d51d4`). **Not covered by the ruling above, which names four.
Recorded here under the same reasoning, for Matt to differ from if he reads it otherwise.**

| deck | the deck says | the row says | manifest row | calendar spine cell |
| --- | --- | --- | --- | --- |
| `SCI_G_W16B_Getting_The_Solid_Back_Do.html` | label `Spring 1 · Week 16` | **`Spr1·W2`** (`weekWithinTerm` 2, `ruledAbsoluteWeek` 17) | `Science_Teesside/Grow/W15-W20_2026-27/manifest.json` | `'GROW Weekly - Spring'!C29` → `Spr1·W2` |

## The basis, as measured

* **Spring 1 has six weeks.** The estate's label convention is `<term> · Week <weekWithinTerm>`,
  so "Spring 1 · Week 16" names a week that does not exist in that term. It is the deck's own
  pack number, `W16`, written into the slot the label reserves for the within-term week.
* **Its sibling agrees with the record, not with it.**
  `SCI_G_W16A_Solubility_And_Recovery_Explore.html` is bound to the *same* row, the *same*
  spine cell `'GROW Weekly - Spring'!C29` and the *same* outcome ("Investigate solubility and
  how to recover a substance from solution."). W16A states no week at all and is landable by
  form (iv) — the signed row alone. Only W16B contradicts the row.
* **Three independent records agree** on `Spr1·W2`: the manifest lesson row, the resolved
  workbook cell, and the signed `SCIENCE_WEEK_BINDINGS` entry. Only the deck's typed label
  says otherwise, and what it says is not a valid Spring 1 week.

This is the same class as the four above — a typed claim contradicting the records — but not the
same pattern: it is a single deck writing its pack number where the within-term week belongs,
not a one-week offset carried forward down a run of Explore decks.

## Status

* **REFUSED** by the limb, for the reason the limb prints:
  `the deck states Spr1·W16 about itself, which does not cover the record's term-week (Spr1·W2)`.
* **No edit now**, exactly as for the four: neither the deck nor the record is touched.
* It closes at **PASS C** for the same reason — the transplant derives the label from the
  binding, so the deck stops asserting a week of its own.

## The estate-wide count, corrected

Measured with the ruled limb over all 180 bound routes, on the record verified equal to its pin:

| | routes |
| --- | --- |
| landable | **171** |
| refused — the signed row binds them to no week (HELD by name, per the ruling) | 4 |
| refused — the four consecutive BUILD Explore decks above | 4 |
| refused — this GROW deck | 1 |
| **total** | **180** |

**Correction.** I previously reported this as 172 of 180 with four contradictions. The measured
figure is **171 of 180 with five**; the fifth is the deck named here. The four no-week routes
(`SCI_B_W8A`, `SCI_B_W8B`, `SCI_B_W11A`, `SCI_B_W11B`) are unchanged and stay HELD by name.
