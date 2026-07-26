# Instrument Register — Art Teesside

Companion to `LundyLoop/tools/INSTRUMENTS.md`, kept separate because `main` is
shared with a live Lundy Loop workstream and a single register edited by two
workstreams is a merge conflict waiting to be resolved by whoever pushes second.
The standing rules in that file apply here unchanged, in particular: any pass
that measures the estate loads this register before it runs, and an instrument
marked QUARANTINED must not be used, nor used to validate its own replacement.

**What this register structurally cannot detect.** Everything here agreeing, and
everything here being wrong, are indistinguishable from inside this file.

---

## AT-INST-01 — `assert_estate.py`

- **Derives:** live (non-residual) counts for the six house assertions across every
  tracked `*.html` file under `Art_Teesside/`, plus the declared-residual count
  each assertion is expected to tolerate, plus uncontested counts for tier
  vocabulary and attribution.
- **Method:** **Literal** throughout. Every assertion is a regular expression over
  file text. No assertion reads meaning.
- **Independent of:** the link graph and catalogue-membership methods used for
  D-ORPHAN-01; shares no premise with either.
- **Consumed by:** every pass R1–R9. The full set is run after each and reported
  as counts.
- **Status:** current.

### Baseline at `3b805af`, 53 files

| Assertion | Live | Declared residual | Verdict |
|---|---|---|---|
| `A2_no_aos` | 0 | 8 | PASS |
| `A3_no_grade_bands` | 0 | 8 | PASS |
| `A4_no_hours_gate` | 0 | 30 | PASS |
| `A5_tier_vocab` | 0 | 0 | PASS |
| `A6_no_pupil_names` | 0 | 0 | PASS |
| `A8_closed_kit` | **40** | 3 | PASS (open finding, expected) |

`A8` is the only non-zero and is not a defect in the instrument: it is
D-PRESS-01 (31 — GROW W2 19, LAUNCH W6 6, GROW W3 4, GROW W6 2) plus D-PRESS-02
(9 — BUILD A2_W6 5, Autumn2 SoW 3, Autumn2 pack 1). It closes at A2a, not before.

### Known sensitivity limits — declared, not hidden

- **Paraphrase is invisible.** "The pull is a ceremony, not a snatch" teaches a
  press and matches nothing. Every count here is a **floor, not a total**. Do not
  quote `A8 = 40` as the number of press references in the estate.
- **`\brollers?\b` was `\broller\b` for one revision** and silently missed all four
  plural instances, one of which is live in GROW W2. Any assertion added later
  must be checked against its own plural and possessive forms before it is trusted.
- **Refusal context is counted live in three Autumn 2 SoW hits.** Those name the
  press in order to refuse it and could defensibly be residuals. They are counted
  live deliberately: under-counting a banned string is the failure mode that
  matters, over-counting merely creates work.
- **`*.html` only.** The staff-side `.md` files in `Art_Teesside/` quote banned
  strings in the course of describing them. Sweeping them would re-manufacture the
  false positives this estate has a documented history of.

### Calibration — four false-positive families found and removed before first use

Recorded so they are not reintroduced. This estate has withdrawn nineteen false
absence findings in one audit and retired 691 more from a quarantined instrument;
the cost of an over-crude check here is not hypothetical.

| Pattern | Matched | Why it was wrong | Action |
|---|---|---|---|
| `\bDistinction\b` | "the method-vs-biography **distinction**" | grade word that is also an ordinary noun | removed |
| `greater depth` | "4. **Greater depth** (Think)" | question-difficulty label in every arrival grid | removed |
| `pupil name` | 73 hits | every one inside a sentence *forbidding* pupil names ("carries no pupil names — codes only") or using the verb ("Every pupil **names** their own PROTECT") | replaced with a search for actual name-collection fields, of which the estate has **none** |
| `working at` | ordinary prose | not a band descriptor here | removed |

Had these shipped, the instrument would have reported 106 violations across 53
files, every one of them false, and four of the six assertions would have read
MOVED at a baseline where nothing has moved.

### The declared residuals register

Eighteen exact strings, 49 instances, held in `RESIDUALS` inside the instrument
rather than in a separate document, so that the list and the check that consumes
it cannot drift apart. Five families of refusal sentence for AO/grade bands,
eight for the hours gate, two for the press, plus one staff-side planning figure
(`Bronze guidance is 40 GLH + 20 ILH`) which sits in the Autumn 2 SoW immediately
above its own refusal to gate on it and is never pupil-facing.

A standalone `Declared_Residuals.md` is still owed as a staff-facing document.
This is its machine-readable half, arriving early because the assertions needed it.
