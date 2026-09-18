# Reconciliations — ORDER SX3-M2 §8

Read-only. No fixes.

## 1. 75 vs 79 — ACCEPTED as 56 + 15 + 8, and now fully decomposed

79 pack deck identities were measured. `79 = 56 + 15 + 8`.

- **56** — the Science files carried by the six sx3 content branches, measured as
  the union of `git diff --name-only origin/main...origin/<branch> -- Science_Teesside/`
  across `sx3-build-1` (11), `sx3-build-2` (5), `sx3-grow-1` (12), `sx3-grow-2` (5),
  `sx3-launch-1` (12), `sx3-launch-2` (11).
- **15** — the parked LAUNCH W3–W7 decks.
- **8** — outside both.

The order's own arithmetic settles what the 8 are. §3 expected held `39 → 29` and
landing `36 → 46`, so the population it counts is `36 + 39 = 75`. And
`75 = 56 + 15 + 4`. So **4 of the 8 are inside the 75 and held**, and **4 are
outside it entirely**. That matches `_sx3/RELEASE_LEDGER.md`'s own held list of
19 = 15 parked + 4 (see §2 below).

## 2. The two 19s

The first 19 is `_sx3/RELEASE_LEDGER.md`: *"56 decks land, 19 are held"*, with a
19-row table. Read out, that 19 is:

- the **15** parked LAUNCH W3–W7 decks, each held because the authoritative
  Complete generation carries 0 print pages and the served deck has printable
  content; and
- **4** more: `SCI_B_W5A_Right_Nutrition`, `SCI_B_W5B_Right_Nutrition`
  (*"0 COVERAGE rows; two distinct lessons, not a split"*) and
  `SCI_G_A2_W7A_Autumn_Science_Review_Explore`,
  `SCI_G_A2_W7B_Autumn_Science_Evidence_Do` (*"one lesson with each other, one
  character apart (data-start-stage a0 vs b0), both 917,895 B"*).

So `19 = 15 + 4`, and the order's `39 = 19 + 10 (sx3r duplicates) + 10 (stage
count)`. The ledger's 19 and the order's 39 are the same population counted
before and after the two new hold classes. **They reconcile exactly.**

If a second, independent 19 was meant, I cannot identify it from the records in
this repository and will not invent one. Naming it would close this item.

## 3. 45-of-56 vs 44+12, and whether the token defect explains the split

It does not, and neither figure survives re-measurement.

Search scope: the 56 Science files at their branch heads. For each, (a) does the
recorded `own title slide declaration` quote in `TERM_AND_STYLE_EVIDENCE.json`
survive in the proposed text — the OLD quote limb; (b) does every term·week key
derived from `SCIENCE_WEEK_BINDINGS` appear in token form — the NEW limb.

| measure | of 56 |
|---|---|
| carry a recorded own-title-slide quote at all | **16** |
| carry a week binding in the record | 56 |
| OLD limb would prove | **0** |
| NEW limb would prove | **0** |
| derived token present in the proposed text | **0** |
| binding present in label form only | 12 |

**All 56 fail both limbs**, not 45 and not 44+12. The earlier 45 and 44 were
measured on the evidence-sha256 path rather than on the limbs themselves, and I
am not able to reproduce either as a limb result.

The token defect explains **6** of the failures — see `_sx3/STOP_S4_lesson_config.md`.
The other 50 fail because the deck carries no recorded declaration for the limb
to anchor on (40) or because the binding is absent from the proposed text (14,
of which 2 carry it in label form only). The dominant cause is neither the token
nor the quote: it is `lesson-config` being replaced wholesale by the transplant.

## 4. The three "placed but excluded" decks — reason recovered, not blank

I earlier recorded four decks as placed in `SOURCE_PLACEMENT.json` but excluded
from the landing set with the reason not recovered. Three are now recovered:

| deck | reason | source |
|---|---|---|
| `SCI_G_A2_W7A_Autumn_Science_Review_Explore.html` | one lesson with `A2_W7B`, one character apart (`data-start-stage` `a0` vs `b0`), both 917,895 B | `_sx3/RELEASE_LEDGER.md` held table |
| `SCI_G_A2_W7B_Autumn_Science_Evidence_Do.html` | as above, the pair | `_sx3/RELEASE_LEDGER.md` held table |
| `SCI_G_W8A_Day_And_Night_Explore.html` | it is the GROW pathway chassis exemplar; transplanting it onto its own chassis is circular | `_sx3/CHASSIS_CONTRACT.md` exemplar row |

**`SCI_G_W8B_Day_And_Night_Do.html` — reason NOT recovered.** It is placed and
bound (`Aut2·W1`), it is the sibling of the GROW exemplar, and no record in this
repository states why it was excluded. Recorded as *reason not recovered*, not
blank, and not guessed.

The other four of the 8 — `SCI_B_A2_W1A_Reduce_Reuse_Recycle_Explore.html`,
`SCI_B_A2_W1B_Our_Waste_Saving_Plan_Do.html`, `SCI_B_W5A_Right_Nutrition.html`,
`SCI_B_W5B_Right_Nutrition.html` — have no route on main. The ledger gives the
W5 pair a reason (*0 COVERAGE rows; two distinct lessons, not a split*); the
`A2_W1` pair has none recorded, and needs a placement ruling before it can land
anywhere.

## 5. Multi-week precedent — ORDER SX3-M2 §5(f)

Precedent **exists**, and it is this very deck.

| record | rows | rows with more than one week |
|---|---|---|
| `tools/catalogue/SCIENCE_WEEK_BINDINGS.json` | 129 | **0** |
| `assets/catalogue/lesson-order.json` | 1077 | **2** |

The two in the derived view are:

- `Grow/Slideshows/GROW_ART_W2_Level_Up_Portrait.html` → `Aut1·W2`, `Spr1·W2`, `Sum1·W2` (three weeks, three terms)
- `Science_Teesside/Launch/W17-W26_2026-27/SCI_L_W18L2_Genetic_Engineering_Change_Test_Decide.html` → `Spr1·W3`, `Spr1·W4`

The second is the deck in question. It is **already** represented as a two-week
span on main, in one term. So §5(f) resolves to *follow the precedent*: bind it
to both `Spr1·W3` and `Spr1·W4`.

One caveat, named rather than smoothed over: the precedent is in the **derived**
record, not the **audited** one. `SCIENCE_WEEK_BINDINGS.json` has no multi-week
row at all, so this would be its first. The shelf renderer already supports it —
`build_science_shelf.py`'s `card()` joins `weekWithinTerm` with a space and
`label` with `"; "` — and the binding assertion tolerates it because both weeks
are `Spr1`. So nothing needs inventing; but the audited record gains a shape it
has not carried before, and that is worth knowing before it is written.
