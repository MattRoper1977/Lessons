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
| `A6_no_pupil_names` | **24** | 0 | PASS (open finding D-NAMES-01) |
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

---

## AT-INST-02 — `assert_cooccurrence.py`

- **Derives:** contradictions between two things that are each individually true.
  C1 award level disagreeing between chassis layers within a file; C2 term/week
  disagreeing between strip, badge and print mirror; C3 kit vocabulary beside a
  kit disavowal in the same file; C4 a Part described as both banked and open;
  C5 a route whose scheme of work disavows kit its own lessons teach.
- **Method:** **Literal** for C1, C2, C3, C5. **Approximate** for C4 — it matches
  status words inside a ±130-character window near a Part token, so read every C4
  hit before quoting it.
- **Independent of:** AT-INST-01 entirely. AT-INST-01 asks whether a banned string
  is present; every string this instrument reasons about is legitimately present.
  A finding here is invisible to that one by construction.
- **Status:** current.

### Why it exists

R1 found seven files carrying `BUILD · Explore` and `Bronze Part A` inches apart
on the same header strip. Seven human reviews passed them, because whichever half
you looked at was correct. This estate's characteristic fault is not a false
statement; it is two true-looking halves that cannot both hold. An absence check
cannot see that class — every string it hunts for is genuinely there.

### Self-test — the check was validated against known ground truth before use

Run at HEAD the instrument returns zero, which is exactly what a broken check
returns. It was therefore run against the estate as it stood at `6486176`, one
commit before R1, where the answer was independently known:

| Assertion | Found at 6486176 | Ground truth | |
|---|---|---|---|
| `C1_award_level` | 7 | 7 files, Explore badge + footer against Bronze award-strip | ✓ |
| `C2_term` | 7 | 7 files, strip Aut 1 against badge Autumn 2 | ✓ |
| `C2_week` | 6 | 6 files — W1 excluded, its week was coincidentally correct | ✓ |

The W1 exclusion is the useful part of that result: the instrument distinguishes
a field that is wrong from a field that is right by accident. Zero at HEAD is
therefore a real zero, not a silent failure.

### Baseline at `023ec96` (post-R1), 53 files

C1 0, C2_term 0, C2_week 0, C3 0, C4 0 — **C5 2**.

`C5` reports `Build/BUILD_ART_A2_W6_Resolve_and_Edition.html` (`pull an edition`
×5) and `Build/Autumn2_Printable_Weekly_Evidence_Pack.html` (×1) against the
Autumn 2 scheme of work's own disavowal. This is D-PRESS-02, it predates this
session, and it arrived with `2106b3f` — the commit that performed the
press-to-stencil conversion and did not finish inside its own folder.

**Estate headline, wider than any single assertion:** kit is disavowed in 2 files
and taught in 6 that carry no disavowal — the two above plus GROW W2 (19 hits),
LAUNCH W6 (6), GROW W3 (4), GROW W6 (2). C5 is folder-scoped and cannot report
the GROW and LAUNCH four, because their folders contain no disavowal to
contradict. That is D-PRESS-01 and it closes at A2a.

### C3 returned zero, and the zero was the finding

C3 was specified as within-file: kit vocabulary beside a kit disavowal in the
same file. It returns zero at every commit, because the estate's contradiction
does not live inside single files — the file that denies the press and the file
that teaches it are different files. C5 exists because the within-file question
was the wrong question. C3 is retained: it costs nothing and it guards against a
future file that argues with itself.

---

## Session constraints

- **GitHub API is unreachable from this session.** `/repos/{owner}/{repo}/pages`,
  `/pages/builds` and `/actions/runs` all return *"Access to this GitHub API path
  is not permitted through this proxy."* Deploy state cannot be observed from
  here and must be confirmed by a human in Settings → Pages. Recorded so a future
  run does not spend time rediscovering it. Git over HTTPS works normally.

## Standing rules adopted during Pass 4

5. **NBSP is written as an explicit `\xa0` escape, never as a literal character.**
   The character survives one heredoc and not the next. In R1 a dry run reported
   4 of 4 patterns matching and the apply reported 21 of 28, because the literal
   nbsp in one script had become an ordinary space in the other.
6. **Substitution counts are not verification. Read-back is.** Every substitution
   pass ends by reading back every field it claims to have changed and reporting
   matched against expected. A dry run and an apply that disagree are measuring
   two different strings, and no count will ever say so.
7. **An instrument returning zero is not trusted until it has been run against a
   commit where the answer is independently known.** Zero and broken are
   indistinguishable from inside the instrument.


---

## D-NAMES-01 — the estate collects the names it says it never stores. **HIGH.**

Found during R4 while placing the observer block, not by either instrument.

24 lesson files print a feedback sheet whose first field is:

```
<tr><td style="width:50%"><strong>Pupil name:</strong></td><td><strong>Date:</strong></td></tr>
```

All 8 GROW lessons, all 8 LAUNCH lessons, and 8 BUILD lessons. Meanwhile four
other files in the same estate state the opposite, in terms:

- "It never goes in a pupil portfolio and it carries **no pupil names** — codes only"
- "**No pupil names are stored in any file**; a code works everywhere a name would"
- "No pupil names are stored in any file; **a name or a code both work**"

The third of those is itself in tension with the first two, so the estate holds
three positions, not two. This is the C-class fault exactly: each half is true
where it sits, and a reviewer reading either one is satisfied.

### AT-INST-01 reported A6 clean, and that was a FALSE NEGATIVE

Worse than a false positive, and the reason it happened is recorded here so the
method changes and not just the pattern. The A6 pattern was
`Full name|First name|Surname|Name of (?:pupil|student)|Name:\s*_`. The estate
writes `<strong>Pupil name:</strong>`, which none of those match — `Name:\s*_`
requires an underscore, and this field is followed by a table cell boundary.

The calibration that produced that pattern examined `grep ... | sort -u | head -6`
and found all six unique contexts were prohibitions, so the phrase was ruled
benign and the pattern was narrowed. There were five unique contexts in total and
the **first** of them was the field. Sampling the head of a sorted unique list is
not reading the list. Standing rule 8 below.

### Not fixed here

Whether a printed feedback sheet kept with a sketchbook counts as "a file" is a
policy question, and the estate's own text argues both ways. `A6` is set to the
measured 24 so that the count is visible and any *movement* is caught, and the
finding is declared rather than silently repaired.

## Standing rules adopted during Pass 4 (continued)

8. **A sampled `head` of a unique-context list is not a reading of it.** When a
   pattern is being narrowed or ruled benign, every distinct context is read, or
   the narrowing does not happen. A6 was declared clean on six sampled contexts
   out of five, and missed a field in 24 files.
