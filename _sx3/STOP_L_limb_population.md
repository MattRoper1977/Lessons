# STOP-L — the narrowed limb removed a proof that existed, on 11 decks

ORDER SX3-M3 §4. This check runs before the §3 content change is written.
It is a STOP, and for a sharper reason than the one anticipated.

## Answer to the question asked: no, the limb does not govern the 81

Search scope: all 129 `SHELF_SELECTION.science` decks at `origin/main`. Every
limb of `build_lesson_order.py`'s `proved` expression evaluated against each
deck's current bytes, on the assumption that the limb runs — i.e. that the deck's
bytes have drifted from its recorded evidence sha256.

Of the **81** decks carrying neither the token nor the label form:

| what would carry it if its bytes moved | decks |
|---|---|
| `preserved_outcome` | 34 |
| `explicit_cell` | 19 |
| `enrichment` | 3 |
| **no limb at all — unprovable** | **25** |

So the narrowed limb does not govern the 81; another limb carries 56 of them.
None of the 25 unprovable decks is `style: recommended`, so none would raise an
`AssertionError` — they would land in `unresolvedTiming` and lose their week
binding **silently**. That is a real defect, and it is the same structural one
§5 names: the record asserts a fact the artefact does not restate. It is not
caused by the narrowing — those 25 have no recorded declaration, so the old
whole-quote limb failed them identically.

## The reconciliation: 36 + 8 + 81 + **4** = 129

The four unaccounted decks are the ones with **no week recorded at all**:

- `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html`
- `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html`
- `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W11A_Rock_Permeability_Explore.html`
- `Science_Teesside/Build/W8-W13_2026-27/SCI_B_W11B_Water_Through_Rock_Lab_Do.html`

All four carry `status: unset`, and they are exactly the audit's own
`unsetWeekRoutes` list — verified identical, not merely the same count.

## The actual finding: #586 regressed 11 decks

Old limb against new limb, both evaluated on current bytes as if the limb runs:

| | decks |
|---|---|
| OLD proves and NEW proves | 35 |
| **OLD proves, NEW does not** | **11** |
| NEW proves, OLD did not | 1 |
| neither proves | 82 |

Net **−10**. The 11 split into two causes.

### Cause 1 — no week recorded, so the limb can never fire (3 decks)

`SCI_B_W11A_Rock_Permeability_Explore.html`, `SCI_B_W8A_Sugar_Labels_Explore.html`,
`SCI_B_W8B_Autumn_Science_Checkpoint_Do.html`.

Their recorded declaration is intact, so the old limb proved them. The narrowed
limb requires `bool(tokens)`; with no week in the record `tokens` is empty and the
limb returns `False` unconditionally. **Narrowing turned "provable" into
"structurally unprovable"** for these three.

### Cause 2 — the binding is written in LABEL form (8 decks)

| deck | binding |
|---|---|
| `Grow/Autumn2_W7_2026-27/SCI_G_A2_W7A_Autumn_Science_Review_Explore.html` | `Aut2·W7` |
| `Grow/Autumn2_W7_2026-27/SCI_G_A2_W7B_Autumn_Science_Evidence_Do.html` | `Aut2·W7` |
| `Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html` | `Aut2·W4` |
| `Build/W8-W13_2026-27/SCI_B_W13_Where_did_this_material_come_from_Classic.html` | `Aut2·W5` |
| `Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html` | `Aut2·W1` |
| `Grow/W8-W13_2026-27/SCI_G_W12_Follow_the_warming_chain_Classic.html` | `Aut2·W4` |
| `Launch/W8-W13_2026-27/SCI_L_W9_Copy_separate_divide_Classic.html` | `Aut2·W1` |
| `Launch/W8-W13_2026-27/SCI_L_W12_Zoom_into_genetic_information_Classic.html` | `Aut2·W4` |

Their declaration still matches, so the old limb proved them. They write the
binding as `Autumn 2 · Week 4`, which the estate's own `term_codes` and
`weeks_from` regexes accept, and which the narrowed limb does not.

**One of these eight is in the landing 36**:
`SCI_B_W12_Give_a_rock_a_job_Classic.html`. The §3 content change writes the
token on exactly that deck, so the release repairs its own. The other ten are
pre-existing routes and stay regressed.

## Is it live?

No — it is **latent**. `build_lesson_order.py --check` passes on `main` today
with `unresolvedTiming: 0`, because the limb only runs when a deck's bytes drift
from its recorded evidence sha256, and none of the 11 currently do. The
regression bites the next time any of those eleven decks is edited.

That is not a reason to leave it. It is a trap set for whoever edits one next.

## Proposed fallback limb — NOT written

The limb should prove the **fact**, not the **form**. Three arms, in order:

```python
labels = {a.title()+n+'·W'+w for a,n,w in LABEL.findall(text)}
token_proved = bool(proofs) and (
    (bool(tokens) and all(k in text for k in tokens))          # 1. token form
    or (bool(tokens) and tokens <= labels)                     # 2. label form
    or (not tokens and all(norm(p['quote']) in text for p in proofs))  # 3. no week recorded
)
```

where `LABEL` is the regex `build_catalogue.py` and `build_lesson_order.py`
already use: `\b(Aut|Spr|Sum)(?:umn|ing|mer)?\s*([12])\s*[·:—-]?\s*W(?:eek)?\s*(\d+)\b`.

Arm 2 accepts the binding the estate already knows how to read. Arm 3 says: where
the record asserts **no** week, there is no binding to compare, so fall back to
what the old limb did rather than failing unconditionally.

### Red proof this fallback must carry before it lands

1. **Wrong token** — deck says `Aut1·W4`, record says `Aut1·W3` → RED under all
   three arms (arm 2 must not rescue a wrong binding: `tokens ⊄ labels`).
2. **Wrong label** — deck says `Autumn 1 · Week 4`, record says `Aut1·W3` → RED.
   This is the arm-2-specific case and is the one that proves arm 2 has teeth.
3. **Binding absent in both forms** → RED.
4. **No week recorded, declaration broken** → RED via arm 3.
5. **No week recorded, declaration intact** → GREEN via arm 3, restoring the 3.
6. **Label form, correct binding** → GREEN via arm 2, restoring the 8.

Cases 1–4 are the teeth; 5 and 6 are the repair. A fallback that cannot go red on
1, 2 and 4 is a loosening and must not land.

## What I am asking

The §3 content change is authorised and I have not written it. This check was
ordered to run first, and it returned a STOP. Two things need your word:

1. **Does the fallback limb land in this release or the next?** It is a change to
   `build_lesson_order.py` — a tool, not a workflow — and it moves one pin in both
   gate copies, the same procedure used three times today. It is not a CI edit.
2. **Does §3 proceed now regardless?** The 36 are unaffected by the regression
   except `SCI_B_W12_Give_a_rock_a_job_Classic.html`, which the content change
   repairs. Nothing in the landing set depends on the fallback.
