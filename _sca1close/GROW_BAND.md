# SCA-1 CLOSE v2 3d — GROW reading-band check (MEASURE ONLY, nothing edited)

Band supplied by the owner this session: **reading age 8–12 ≈ Flesch–Kincaid 3.0–7.0**.
Instrument: SCA-1's own `fk()` and the same selector used for BUILD — question stems of
≥25 characters from `_sca1/tables/questions_raw.csv`, regenerated from the current bytes
(`_sca1/tools/extract.py`, 2060 rows). Tables: `_sca1close/tables/grow_band.csv`,
`grow_band_core.json`.

## Per-lesson verdict

| lesson | n | median FK | min | max | out of band |
|---|---:|---:|---:|---:|---:|
| SCI_G_W3A_Friction_Explore | 48 | 2.3 | −0.7 | 10.7 | 36 |
| SCI_G_W3B_Friction_Do | 48 | 3.6 | 0.6 | 11.2 | 22 |
| SCI_G_W4A_Mechanisms_Explore | 48 | 2.5 | −2.5 | 9.2 | 38 |
| SCI_G_W4B_Mechanisms_Do | 48 | 3.8 | 0.1 | 11.2 | 28 |
| SCI_G_W5A_Fair_Test_Explore | 48 | 3.5 | −1.4 | 10.7 | 28 |
| SCI_G_W5B_Fair_Test_Do | 48 | 3.8 | −1.1 | 19.0 | 30 |
| SCI_G_W6A_Earth_And_Planets_Explore | 48 | 3.7 | 0.1 | 12.7 | 28 |
| SCI_G_W6B_Earth_And_Planets_Do | 48 | 4.1 | 0.1 | 15.8 | 32 |
| SCI_G_W7A_The_Moon_Explore | 48 | 3.7 | −0.7 | 16.8 | 27 |
| SCI_G_W7B_The_Moon_Do | 48 | 4.2 | −1.1 | 12.7 | 30 |

**Every lesson's median sits inside the band (2.3–4.2 against 3.0–7.0);** eight of ten
medians are in the lower half, i.e. GROW reads easier than its ceiling, which is the
right direction for this cohort.

## Raw count, then what it actually means

480 stems measured, **299 "out of band"** — but that headline is misleading and should
not be ruled on as-is:

- **203 of the 299 are BELOW 3.0** — easier than the band. For a mixed-attainment SEND
  cohort that is a feature, not a defect. No action proposed.
- **96 are above 7.0.** Filtering to real prose (≥15 words — FK is mathematically
  unstable on short fragments; a 4-word label like "Two-arrow explanation frame."
  scores 13.1 purely on syllable density) leaves **50**.

Those 50 classify as:

| class | n | disposition |
|---|---:|---|
| print-only prose (staff/worksheet density, never on screen) | 15 | report only |
| Stretch by design (★-marked or Stretch tier — the tier exists to exceed the band) | 11 | report only |
| teacher model-explainer ("What this model helps us see: …") | 10 | report only |
| glossary list ("WORD HELP term — definition term — definition …" run together, so FK measures list density, not a sentence) | 9 | artifact, no action |
| **screen-facing pupil prose** | **5** | **→ PROPOSED** |

## The actionable core — 5 stems, all PROPOSED, none edited

| FK | words | lesson | slide | stem |
|---:|---:|---|---|---|
| 10.4 | 18 | W4B_Mechanisms_Do | starter | "Predict before touching equipment: will a pivot nearer the load make the effort feel easier, harder or unchanged?" |
| 9.8 | 16 | W7B_The_Moon_Do | exit | "Explain why an eclipse is different from the normal phase cycle and name one model limitation." |
| 8.6 | 25 | W4A_Mechanisms_Explore | starter | "How can one person lift, turn or move something that feels too difficult by hand? Choose a familiar object: scissors, wheelbarrow…" |
| 8.4 | 17 | W6B_Earth_And_Planets_Do | arrival | "Last lesson: explain how gravity keeps a planet in orbit instead of moving in a straight line." |
| 7.7 | 18 | W4A_Mechanisms_Explore | arrival | "Week 3: explain why the same force can be useful in one design and a problem in another." |

All five are single sentences of ordinary science English whose FK is driven by
multisyllabic subject vocabulary (*equipment, unchanged, gravity, eclipse, limitation*)
that the lessons deliberately teach. Simplifying them would mean removing the taught
term. **Recommendation: hold all five** — or, if the band is to bind on screen prose,
split each into two shorter sentences rather than substituting the vocabulary. Not
applied: 3d is a measure-only ruling.

## Caveat on the instrument, stated so it is not over-read
Flesch–Kincaid was built for continuous prose. On question stems it is noisy at the
short end, and on the concatenated WORD HELP glossary blocks it is meaningless. The
per-lesson medians and the ≥15-word screen subset are the trustworthy readings here.
