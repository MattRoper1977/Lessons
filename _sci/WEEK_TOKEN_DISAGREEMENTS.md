# The four Explore decks whose own week token disagrees with their binding

**Ruled by Matt Roper, 2026-09-22 (on the STOP-B3 limb measurement): the ROW is right.**

The widened Science limb (four accepted forms of a deck stating its own term-week) made a
disagreement visible that the limb as first written could not distinguish from silence: a deck
that states a week, and states a *different* one from the row the signed record binds it to.
Estate-wide there are exactly four, and they are consecutive:

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
