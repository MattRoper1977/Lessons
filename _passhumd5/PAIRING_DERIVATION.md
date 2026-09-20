# B2 landing — where the pack lessons actually go, and the four that cannot go there

B2 lands pack lessons "against the served routes, upgrades in place". This records
how each destination was derived, because the first derivation was unsound and the
correction matters.

## The week join, and why it is not a key

The first pass joined pack lessons to served lessons on
`(pathway, strand, absolute_week)`. That key is **not unique in the served estate**:

- **Classic alternatives sit at the same week as the lesson they replace** —
  `GROW_HUM_W12_Festival_lights_across_places_Classic` beside
  `GROW_HUM_W12_Compare_With_Care_OUTSTANDING_V3_1`; the same at GROW W13 and
  LAUNCH W11.
- **BUILD runs two parallel units over weeks 9-16**: a Teesside industry unit in
  `BUILD_W9-W14_2026-27/` (Meet the Lower Tees, Rails Meet the River, The Iron Rush,
  A Town Grows Fast, Crossing the Steel River, Industry and Nature) and a
  festivals/citizenship set in `BUILD_W14-W20_2026-27/` plus
  `BUILD_W1-W8_2026-27/BUILD_HUM_W8_A_Festival_Of_Light.html`.

So a week number names two or three different served lessons, and for the pack's
whole BUILD Autumn-2 festivals unit it named the industry one.

## Three independent instruments

| instrument | what it compares | what it is good for |
|---|---|---|
| title | pack title vs the served `<h1>` | strong when it fires; the served `<h1>` is often an *activity* title where the pack titles by *topic*, so silence is not evidence |
| content | tf-idf cosine, pack lesson vs every served lesson **in the same (pathway, strand) family** | ranks within the family; absolute values run 0.07-0.36 because these are different authorings of a topic, not two versions of one lesson, so it can **contradict** a pairing but never confirm one alone |
| filename | pack title vs the served **filename** with the pathway/week/variant stripped | the filename usually carries the topic title where the `<h1>` carries the activity |

Two earlier faults in the content instrument, corrected and recorded: it ranked
against every tracked `.html` including `Pupil_Resources`, `START_HERE`,
`Teacher_Notes` and `SOURCE_PROVENANCE_REGISTER`, which are not lessons; and it
scored with `|a n b| / min(|a|,|b|)`, which rewards short documents. Together those
made resource pages the "best match" 8 times. The candidate set is now the 77 served
files that parse as a pathway/strand/week lesson, and the measure is cosine.

**A pairing stands when any one instrument supports it. It is contested only when
all three fail.**

## Result: 38 of 42 confirmed, 4 contested

Confirmed by: both title and content 8; title only 4 (content pulled to a broad
Classic re-teach lesson); content only 24 (served titled by activity); resolved by
the filename instrument 2.

### The 4 contested — the BUILD Autumn-2 unit collision

All four pack lessons carry the **same** learning objective: *"I can describe a
festival, compare two celebrations, order events and explain one caring or
respectful action."* The served lessons the week join chose are a geography and
industry unit. Read side by side:

| pack lesson | served objective at that week |
|---|---|
| `BUILD_A2_W02` Comparing celebrations | Meet the Lower Tees — *locate the lower Tees, identify an estuary, explain one physical-human connection* |
| `BUILD_A2_W03` Objects and respectful enquiry | Rails Meet the River — *the railway's principal coal purpose, its link to Stockton's river port* |
| `BUILD_A2_W04` The sequence of a celebration | The Iron Rush — *how ironstone, mines, rail, river and ironworks formed a change chain* |
| `BUILD_A2_W06` Fairness and rights | Crossing the Steel River — *match a river-crossing problem to two steel bridge solutions* |

The content instrument puts all four at ranks 46-66 of their own family, cosine
0.02-0.03. The festivals lessons they belong beside are in the other folder:
`BUILD_HUM_W12_A_celebration_in_order_Classic`, `BUILD_HUM_W14_A_fair_chance_to_join_in_Classic`,
`BUILD_HUM_W14_Festivals_Display_and_Reflection`.

**Nothing is written to these four routes.** Landing the pack content there would
replace live Teesside industry lessons with festival lessons - not an upgrade, a
substitution. The destination for the pack's BUILD Autumn-2 unit is a ruling, not a
measurement, and it is carried to the signature table.

## The wider finding the order should know

Across all 42, content similarity between a pack lesson and its served partner runs
**0.07 to 0.36**. Even the confirmed pairs are different authorings of the same
topic, not two versions of one lesson. "Upgrades in place" therefore means the pack
lesson **replaces** a differently-written live lesson on the same topic, with the
live furniture, nav and tokens winning. That is a larger change than the phrase
implies, and it is stated here rather than assumed.
