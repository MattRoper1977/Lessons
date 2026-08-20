# PEQ-E3 — PROPOSED

These are the judgement calls this pass could not settle on its own, and the residuals it
measured and deliberately left. Each carries its measurement so the next pass starts from
evidence rather than rediscovery.

**Status after the readback ruling of 2026-08-20:** **P1 RULED IN and discharged** ·
**P2 RULED KEPT** · **P5 RATIFIED** · P3 and P4 still open, unapplied · **P6 is new** — the
one sub-item of P1 that is blocked in this session and could not land.

`DECISIONS.md` §3 records the judgement calls that were *made* inside the pass. This file
records the ones that needed an owner word.

---

## P1 · ~~The 12 parallel PEQ decks in the `*_Estate_v3` trees still say "PEQ L1"~~ — RULED IN, DISCHARGED

> **RULED 2026-08-20: "extend the sweep — the twelve `*_Estate_v3` PEQ decks come INTO the
> ground. The estate must not name two levels for the same weeks."** Discharged: 88
> substitutions across 18 live v3 files; 0 now name Level 1 as the level. One sub-item is
> blocked and is recorded as **P6** below.

**This was the headline item. It was the same shape as the 8th EQA file PROP-1 reported and
the owner then ruled in.**

Measured across `GROW_Estate_v3/`, `LAUNCH_Estate_v3/`, `ASDAN_Visual_Learning/` and
`_glv3/`:

| string | files |
|---|---:|
| `Personal Effectiveness (PEQ L1)` | 20 files, **44 occurrences** |
| `PEQ Level 1` | 14 files |
| `PEQ Level 1 (E3 floor · L2 stretch)` | 0 |
| `ASDAN PEQ L1` / `L2 standard` | 0 |

Those files include **twelve PEQ decks covering the same twelve weeks this pass just
re-anchored**:

```
GROW_Estate_v3/GROW_ASDAN/PEQ_W1_Knowing_Myself.html          … W2 … W3 … W4 … W5 … W6
LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_W1_Intro_Choosing_My_Level.html … W2 … W3 … W4 … W5 … W6
```

**They are live in the registry, not archived.** `resources.json` carries **88** references
into the two v3 trees, including each of those twelve decks by path. They are **not** in
`TAXONOMY_MAP.md`, so they are not shipped to the OneDrive estate, and they are a different
and much smaller chassis — roughly **34 KB against the live decks' 107 KB** — so they are a
summary/alternative build rather than a copy.

### How it was discharged

**No generator exists to fix, and that was checked first.** The ruling required the
generator route where one exists — "if any of the twelve is generated from a shared
payload, fix the generator and re-materialise, never the copies." Measured:

- **0** of the twelve carry the owned-payload marker `ASDAN-VISUAL-LEARNING:JS:BEGIN`, and
  `materialise.py`'s scope is `BUILD_ASDAN/**/*.html` only;
- **0** HTML files exist under `_glv3/`;
- `_glv3/tools/deploy.py` sources its packs from `/tmp/glv3-packs/{grow,launch}` — an
  **uncommitted, external** directory, absent from this container — and installs them with
  `shutil.copy2`;
- the only other repo files containing a v3 deck's title string are `_glv3/PRODUCTION_GATES.json`
  (an audit record) and a sibling v3 page that links to it.

So the deployed files **are** the only copy of that content in the repository. There is no
generator or shared payload to fix, and editing the deployed files is the only available
route rather than a shortcut past one.

**E1 applied — 88 substitutions across 18 live v3 files:**

| substitution | n |
|---|---:|
| `Personal Effectiveness (PEQ L1)` → `Personal Effectiveness · PEQ Entry 3 (Level 1 stretch)` | 31 |
| `PEQ Level 1` → `PEQ Entry 3 (Level 1 stretch)` (LAUNCH slot / title / tag / manifest) | 31 |
| GROW qualification/boundary claim rewritten | 13 |
| LAUNCH qualification/boundary claim rewritten (incl. `ComSk1` → `ComSkE3 · ComSk1 (stretch)`) | 13 |

The GROW half reconciles to the ruled **44**: 31 bare identity strings + 13 inside the
guardrail sentence. After: **0** live v3 files name Level 1 as the level, and the paired
decks agree — `GROW ASDAN · PEQ Entry 3 (Level 1 stretch) W1` on the taught deck,
`GROW ASDAN · Personal Effectiveness · PEQ Entry 3 (Level 1 stretch) · W1` on the v3 route.

**E2 and E3 had no target here, and that is measured, not assumed.** The ruling scopes them
"wherever those decks state a minimum or use a command verb at a tier". The twelve are a
generic pedagogy chassis, not ComSk lesson decks:

- **ComSk minima stated at a tier: 0.** The only `N minutes` strings are the `16 minutes`
  independent-work timing chip.
- **Tier stems: `Standard: add` ×12, `Stretch: add` ×6, `Stretch: state` ×6.** None uses a
  verb above Level 1, and none uses an L1 verb at an Entry 3 tier. `Stretch: state` is an E3
  verb at a Stretch tier, which is allowed — a Level 1 stem may sit easier but must never be
  topped up (`SPEC_FACTS` §19).

`_passpq/tools/v3_tier_gate.py` measures all three conditions every run, so if a minimum or
an above-level verb ever appears in these decks it goes red rather than passing unnoticed.

---

## P2 · `A-P68`'s TA line did not name both floors, and now does — RULED KEPT

> **RULED 2026-08-20: "A-P68 correction KEPT — naming only ComSk1's floor would have had
> assessors holding E3 pupils to 4 components and a 3-minute talk. Your correction is
> right; record it as ruled, do not revert."**

Applied, and flagged because it **corrects the ruling's premise**. §3 E2 says the line
"already names both floors — keep, verify it matches §2b exactly." Measured: both markup
variants in both decks named **ComSk1's floors only**. Left as written, the staff brief
would have told an assessor that Entry 3 pupils owe 4 components, 3 difficulties, 4
audience questions and a 3-minute talk — the whole defect this pass exists to remove, on
the one surface an assessor trusts most.

It now names both floors and says which tier evidences which unit. **The owner has ruled it
KEPT.** No revert is owed, and none should be made.

---

## P3 · 29 short-course decks still stamp `Stretch (L2 standard)`

Measured: Community Project 6 · Enterprise 6 · Community Enterprise 5 · Living
Independently 6 · Vocational 6. **0 PEQ decks carry it.**

§5 holds the short-course family out of this pass, and PROP-1 F07 disclosed the same
boundary when it fixed seven of them. But the claim is wrong on its own terms — ASDAN Short
Courses are unregulated and carry no level, so "(L2 standard)" stamps a level the provision
cannot award, and nobody in the cohort is at L2 in any case. **One row per deck closes it,
on the owner's word.**

---

## P4 · The GROW PEQ weeks cite no unit codes, so none were added

GROW W3 cites `TmWkSk1` and W5 cites `ThSk1`; both took the dual citation E1 requires
(`TmWkSkE3 · TmWkSk1 (stretch)`, `ThSkE3 · ThSk1 (stretch)`). **W1, W2, W4 and W6 cite no
unit code at all** — they bank "core-skills audit", "planning & reviewing own learning",
"managing own performance" and "reviewing & presenting progress".

Those were re-levelled but given **no** code, because inferring one would be authoring an
accreditation claim the deck never made. W2 reads as Learning skills and W4 as Wellbeing or
Learning, but the deck does not say so and neither does `COVERAGE_GROW`. **If the owner can
name the unit each of those four weeks banks, the dual citation is a one-line change per
deck** — and it would let `CREDIT_PATHWAYS` model GROW's E3 route precisely instead of
approximately.

---

## P5 · E5's safeguarding line has no deck to sit on yet — RATIFIED

> **RULED 2026-08-20: "E5-to-checklist ratified as the correct outcome."**

Not a judgement call so much as a measurement that reads like an omission if unrecorded.
**0 of the 14 PEQ files run the DecMk situation choice or the WellbLe improvement
discussion**, and `safeguard*` appears **0** times in either PEQ suite. The requirement is
recorded in `COMPLIANCE_CHECKLIST.md` item 15 and becomes due the moment a DecMk or WellbLe
deck is authored. **Ratified as the correct outcome** — it is here so it is not lost.

---

## P6 · `resources.json` cannot be re-pinned from this session — the one blocked sub-item

**Ruled in with P1** ("+ the resources.json descriptions where they state a level").
**Measured, prepared, verified, and then reverted** — because landing it would turn a green
gate red, which is worse than the disagreement it fixes.

**What the edit is, exactly.** 22 registry entries state a PEQ level, and every one of them
describes a **live** deck this pass re-anchored — so registry and deck now disagree:

| substitution | occurrences |
|---|---:|
| `Personal Effectiveness (PEQ L1)` → `Personal Effectiveness · PEQ Entry 3 (Level 1 stretch)` | 15 |
| `ASDAN PEQ L1` → `ASDAN PEQ Entry 3` | 12 |
| `PEQ Level 1` → `PEQ Entry 3 (Level 1 stretch)` | 6 |
| `PEQ L1 core skills` / `PEQ L1 (Communication complete)` (the two hub descs) | 2 |
| **total** | **35** |

The edit was applied in full, verified to leave **0** entries naming Level 1 and to parse as
valid JSON, and then reverted. `resources.json` is byte-identical to its pin,
`da6600349e68b91d7d59616ec8695c21c7b62f1015bbe9c1916f6d66c48ee5c6`.

**The 146 v3 registry entries need nothing.** Measured: **0** of them state a level — their
titles read "GROW · ASDAN · PEQ W1 · Knowing Myself (v3 route)" with an empty `desc`. P1's
registry half is entirely about the live decks' entries.

**Why it cannot land here.** `resources.json` is guarded by a SHA-256 pin inside
`tools/verify_cross_estate_unification.py`, which is byte-identical in **Lessons and Apps**.
Moving it is `tools/pin_manifests.py`, and that tool writes **both gate copies or neither**.
Its output here, verbatim:

    manifests:
       MISSING apps.json (no owning checkout found)

and the preflight rule that stops it, verbatim from the tool:

    """Every gate copy must carry a movable pin for every manifest, BEFORE any
    write. Writing one of two copies is how the shared file diverges."""
    if len(targets) < 2:
        return ("only one copy of the gate is reachable — re-pinning one of two leaves "
                "the repositories disagreeing. Check out both, or pass --apps/--lessons.")

The Apps checkout is absent from this session (`/workspace/matt-s-apps-`,
`/home/user/matt-s-apps-`, `../matt-s-apps-` all absent) and Apps is outside this session's
repository scope. Edited without re-pinning, the gate reds on a digest mismatch —
`da6600…` pinned against `2bb276…` edited.

**This is the established boundary, not a new one.** PROP-1's own gate record reads
"both repos' gates if anything crosses | **N/A** | nothing crosses; **Apps is out of
scope**", and it recorded the same registry-vs-deck disagreement for the Vocational titles
for the same reason.

**To close it, from a checkout that has both repositories:**

    # apply the 35 substitutions above to resources.json, then:
    python3 tools/pin_manifests.py     # writes both gate copies
