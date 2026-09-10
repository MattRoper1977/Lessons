# GROW Computing — source register

AQA UAS 71638 Programming with Scratch (unit 6), Level One, GROW pathway, 8 × 40 min.

## Packs

| pack | files | bytes | md5 | standing |
|---|---:|---:|---|---|
| Weeks 1–2 | 34 | 1,839,368 B | `9387ff90…` upload | current |
| Weeks 3–6 | 59 | 2,864,859 B | `5e4d5ba8…` upload | current |
| Weeks 7–8 **revised** | 35 | 1,549,100 B | `3f30a30d50e33a7ebbd2bf75ad958a31` | **canonical (D37)** |
| Weeks 7–8 superseded | 32 | 1,053,102 B | `4719a668cd9e1ce5413a954bde7b4f8c` | superseded, held in `superseded/` |

**Not one of the 32 shared paths is byte-identical between the two Weeks 7–8
packs** (measured: 0 of 32). So the revision is a whole-unit replacement, never a
merge, and no file is taken from the superseded pack.

Also held in `superseded/`, under D30: the loose `GROW_Week_01_Interactive.html`
(**24,013 B**, md5 `b927e6f686`) and `GROW_Week_01_Teaching_Slides.pptx`
(**47,188 B**, md5 `dd2951722d`). Both are provenance, not content; the canonical
Week 01 files are the copies inside the Weeks 1–2 zip (**33,725 B** md5
`d8f60ff52b`, and **59,661 B** md5 `fc6c7f7cb8`).

`GROW_Computing_Weeks_07_08_Review_Notes.txt` (1,936 B, md5 `2358248008`) is an
authoring record, not teaching material. It is held here and reaches no route.

## Recheck dates — both, as measured (D42)

| materials | AQA recheck date |
|---|---|
| Weeks 1–6 | **9 September 2026** |
| Weeks 7–8 (revised) | **10 September 2026** |

The two coexist. The Weeks 1–6 materials are **not** normalised to the later date:
the register records dates as measured, not as tidied, and a date changed for
neatness is a date nobody can rely on.

## The parent-link finding, and the instrument that got it wrong first (D46)

| source | superseded | revised |
|---|---:|---:|
| the revision's own authoring record | **6** | — |
| `tools/gc1/check_sb3_parents.py`, per target | **6** | **0** |
| the same checker's first draft, one flat map per project | 7 | 1 |

Two independently derived sixes agreeing is what makes this evidence. The third
row is kept because it is the correction: block ids are unique per target, not per
project, and these packs restart at `k1` in every sprite — eleven ids appear in
both `Player` and `Hazard` in `W07_Bug_Hunt`. A flat map judged Player's `k11`
against Hazard's `k11`'s parent and would have stopped a sound pack.

Weeks 1–6: **0** inconsistent links, in both readings.
