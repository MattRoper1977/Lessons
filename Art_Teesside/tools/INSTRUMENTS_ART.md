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

---

## AT-INST-02 · C6 — scheme mapping as an invariant

Added with R3, on the principle that a one-time fix this estate can keep must be
an invariant rather than a correction. C6 asks whether each scheme of work states,
**per week**, which award section that week evidences, and whether that statement
agrees with the two sources that are the record: the lesson badge and the pack
evidence locator.

Specified on **category, not phrasing**, per standing rule 9. The question is not
"does the string `Part B` appear" — that is what produced the withdrawn finding.
It is "does this scheme declare a per-week award section, and do the three sources
agree".

### Result at `d805706`

```
AGREE     Grow/Scheme_of_Work.html            7 weeks agree
UNMAPPED  Build/Autumn2_Scheme_of_Work.html   declares no per-week award section
UNMAPPED  Build/Scheme_of_Work.html           "
UNMAPPED  Build/Spring1_Scheme_of_Work.html   "
UNMAPPED  Launch/Scheme_of_Work.html          "
```

**The 22 / 14 / 23 / 0 signal has inverted, and that is a finding.** The other
three schemes carry Part and Unit tokens in prose — BUILD Autumn 2 has 22 — but
none of them declares a *per-week* mapping, so an adviser still cannot read
week → Part off them. GROW is now the only tier that can be checked this way, and
therefore the only tier where a future divergence between scheme, badge and
locator will be caught. Raising the other three is not in the current nine-pass
plan and is not done here; it is recorded so the asymmetry is visible.

W8 is correctly excluded from GROW's seven: it audits the four Parts and adds no
fifth, and neither badge nor locator assigns it one.

## Withdrawn findings

- **"GROW Part B absent from six lessons"** — withdrawn before R3 ran. It was a
  token count in files that correctly lack the token. Marked withdrawn in
  `Defect_Register_Pass4.md` rather than deleted: a silently removed false
  finding is indistinguishable from a fixed one, and this programme has already
  been bitten by exactly that difference.

## Standing rules adopted during Pass 4 (continued)

9. **Assertions are specified on category and destination, not on phrasing.**
   A6 was simultaneously false-positive 73 times and false-negative 24 times, and
   both failures came from the same cause: it tested wording when the rule it
   enforces is about a data category and where that data goes. Where an assertion
   cannot be written on category, say so explicitly and it becomes a human check
   on the pre-commit path rather than a number that looks like assurance.

---

## AT-INST-03 — `assert_print.js`

- **Derives:** every sheet's rendered height in every pack at true A4 content size,
  the real PDF page count, and any sheet exceeding the printable area.
- **Method:** **Literal** — a render, not a stylesheet reading. Chromium, print
  media, viewport 718 × 1047px (210 × 297mm at 96dpi less 10mm `@page` margins).
- **Independent of:** AT-INST-01 and AT-INST-02 entirely; those read text, this
  measures geometry.
- **Status:** current.

### Why it exists instead of `min-height: 277mm`

`min-height: 277mm` was proposed to stop sheets reflowing. It cannot: `@media print`
already sets `.a4{min-height:0;height:auto}`, so no min-height change reaches the
printed page. Nor does reducing a screen min-height reveal overflow at authoring
time — content taller than a minimum simply grows past it. What actually catches
a sheet that has grown is measuring it. That is an instrument, not a stylesheet.

### Self-test — replayed against a commit where it must fail

| Commit | Result | Exit | Ground truth |
|---|---|---|---|
| `62dffcd` (pre-R7) | 56 pages / 55 sheets, 1 overflowing, GROW Week 7 +35px | 1 | known defect |
| `2e2c8e3` (post-R7) | 55 pages / 55 sheets, 0 overflowing | 0 | known fixed |

### Headroom at `2e2c8e3` — the number worth watching

```
Autumn2 pack     tallest  801px   headroom 246px
BUILD pack                875px            172px
Spring1 pack              792px            255px
GROW pack                1038px              9px   <-- thin
LAUNCH pack               867px            180px
Spring2 pack              875px            172px
Summer1 pack              839px            208px
Summer2 pack              861px            186px
```

**GROW Week 7 clears by 9px and nothing else clears by less than 172px.** That
sheet is one added line away from failing again, and it is the sheet a future
author is most likely to add to, because it is the fullest. The assertion will
catch it; this note is so that whoever sees the failure knows it is not a
regression in the fix but the sheet running out of room.

### Known sensitivity limits — declared, not hidden

- **Renderer disagreement.** Measured in one Chromium build on one machine. A
  school print driver or a different font stack can differ by a few px, which is
  why R7 was tightened from a 1px clearance to 9px rather than shipped at 1px.
- **Content that is wrong rather than tall** is invisible to it. A sheet can fit
  perfectly and say nothing useful.
- **A pack that fails to render** reports 0 sheets and 0 overflows, which is
  indistinguishable from a clean pass. Sheet and page *counts* are therefore
  asserted against 55/55 as well, so a silent render failure fails the check.

## Withdrawn — `.a4.dense` (was R8)

Dropped, not deleted, with the reason. It was designed as belt-and-braces for a
global density problem. There is no global density problem: one sheet, 35px, in an
estate whose next-tallest sheet cleared by 128px before R7 and by 172px after. A
conditional second density regime firing on `${x.extra}` would be a trapdoor for
whoever next wonders why two sheets in the estate space differently — the same
objection that killed a single-pack scoping of the R7 fix. With AT-INST-03 in
place it earns nothing.

## Standing rules adopted during Pass 4 (continued)

10. **A print measurement taken at screen width is not a print measurement.** All
    print measurement happens at 718 × 1047px. At 1280px the overflow check
    reported zero overflows on a pack that was printing 9 pages for 8 sheets: the
    sheet was 1082px tall at A4 width and comfortably short at desktop width.

---

## AT-INST-04 — `assert_kit.py` + `kit_text.py`. **A8 is superseded.**

Specified on **category**: enumerate what the room has, report every craft noun and
process verb outside it. A8 was a list of press nouns and had no terminating
condition — four widenings (`plate`, `inking`, `hand-pulled`, `screen print`) each
found more, and its under-count produced a **false zero in C5**, which reported
D-PRESS-02 closed when it was not.

**Ordinary language is derived, not listed.** A word is ordinary if it appears in
≥2 non-art subject folders in this repo — an independent corpus sharing no premise
with the kit list. `6 Art`, `Build`, `Grow`, `Launch` and `DT_Community_Upcycling`
are excluded so craft vocabulary cannot launder itself as ordinary.

**Unmatched vocabulary is the deliverable.** 4,265 distinct words in readable text,
1,660 art-specific after subtraction, **456 at count ≥ 4** — the finite review list
that makes "have we finished sweeping?" answerable for the first time.

### Rule 13, implemented as intent rather than letter

Rule 13 says exclude script blocks. Taken literally that would create a false
negative larger than the one it fixes: most pupil-facing prose in this estate lives
*inside* `<script>` — `_taBriefs`, `_pres` fault cards, the `WEEKS` array behind
every print pack. Excluding script blocks would have hidden the TA brief that sets
up an inking bench, the worst string in GROW W2. So `<style>` is dropped whole,
and inside `<script>` only **string literals** are kept. Selectors, camelCase
identifiers, CSS declarations and short JSON keys are dropped — `grid-template-columns`
was the source of 16 phantom `plate` hits.

### What is judgement, not instrument — declared per rule 9

**Sense cannot be derived.** "Press" appears in two non-art folders as *press Escape*,
so frequency marks it ordinary — yet *press corner* is kit. No corpus method
separates senses. The `VIOLATIONS` table is a record of **human decisions**, with a
script attached. Refusal is detected from context (negation within 95 characters),
which is mechanical; which sense a word carries is not. Anyone quoting a number
from this instrument is quoting a human decision.

### Baseline, and the true ladder

```
kit-dependence 47 · vocabulary-residue 4 · refusal-context 8 · offer-scope 2  = 61
```

A8 said 29. The true figure is **61**, and 8 of those are declared refusals.

| pass | hits | after |
|---|---|---|
| — | | **61** |
| A2d-2 — BUILD A2_W6 3, Run Sheets 1, Autumn2 SoW 2 | 6 | 55 |
| A2a — GROW W2 | 24 | 31 |
| A2b — GROW W6 3, GROW W7 3 | 6 | 25 |
| A2e — LAUNCH W1 2, W5 2, W6 10, W7 3 | 17 | **8** |

Terminal 8 = refusal-context, declared: GROW W2 1, Autumn 2 SoW 4, START_HERE 2,
Summer 1 SoW 1. Not 2, as previously predicted — the rebuilt check finds more
legitimate refusals as well as more defects, which is the correct direction.

### Correction to the A2d commit message

`9f87a5a` claims "C5 ROUTE CONTRADICTION 2 -> 0. D-PRESS-02 is closed." **It is
not.** BUILD_ART_A2_W6 still carries `hand-pulled editions vary`, `hand-pulled
prints` and `pull it again`, and the Autumn 2 run sheets carry `Pull the remaining
prints`. C5 did not fail — it faithfully reported what A8's vocabulary let it see.
The commit message stands as pushed; this register carries the truth, same handling
as R6's 167px.

### New finding — Summer 1 was never in scope

`Summer1_Scheme_of_Work.html` carries "No screens, squeegees or fabric inks
needed" — a legitimate refusal, and the first evidence that the screen-print
question reaches beyond LAUNCH W1 into a term nobody has looked at.

---

## Corrections and additions at the close of Pass 4

### AT-INST-03 gains a warning band

Fails over 1047px; **warns under 50px clearance**. Current output:

```
WARN  Printable_GROW_Evidence_Lundy_and_LAUNCH_Pack.html sheet 7 "Week 7"
      1038px  clears by only 9px
PRINT ASSERTION PASS (1 within 50px of the limit)
```

An author told at 20px has a choice. An author told at −3px has a broken pack and
a deadline.

### Escalation ladder for GROW Week 7 — written now, not under pressure

That sheet's furniture has been tightened twice (R6 styled the ladder, −64px; R7
trimmed header, spine, Lundy strip, ladder and footer margins, −44px). **There is
nothing left in the furniture.** When it next fails, do not hunt millimetres. In
order:

1. **Move a block to the recovery route.** The recovery route is already a
   separate print section; a diagnostic can live there.
2. **Shorten the diagnostic prose.** The two `.diag` blocks are 145px and 185px —
   the largest non-evidence items on the sheet.
3. **Split the week across two sheets.** Costs a page; costs nothing else.

Evidence fields, mount zones and the recovery route stay untouchable, as always.

### Terminal enumeration — the seven declared refusals, named not counted

A count cannot be checked next session; a named set can. This is how `29` survived
four widenings.

| file | string | ×|
|---|---|---|
| `Build/Autumn2_Scheme_of_Work.html` | `there is no press, no rollers and no printing inks in the room` | 2 |
| `Build/Autumn2_Scheme_of_Work.html` | `No press, no rollers, no inks, no blades beyond classroom scissors` | 2 |
| `Build/START_HERE.html` | `No press, no rollers, no inks — rubbings, stencils and sponged acrylic only` | 2 |
| `Summer1_Scheme_of_Work.html` | `No screens, squeegees or fabric inks needed` | 1 |

### The negation detector was wrong on its first outing — terminal 8 → 7

Its first version matched any nearby `not` and swallowed GROW W2's `ghost` card —
*"Plate not re-inked. Every pull needs its own ink"* — which **asserts** the press.
A genuine kit-dependence hit was moved into the safe column, and a false refusal
closes a defect instead of opening one. Negation must now fall on the kit's
**existence** (`there is no`, `no press`, `none are needed`, `off the table`,
`without`), never on a verb.

Corrected counts: **kit-dependence 48, vocabulary-residue 4, refusal-context 7,
offer-scope 2 = 61.** GROW W2 is 25, not 24.

**Corrected ladder:** 61 → A2d-2 (6) → 55 → A2a (25) → 30 → A2b (6) → 24 →
A2e (17) → **7**.

### Offer-scope sweep — result, and its limitation

All 53 files, three tiers, every term with content. **4 hits, 2 files.** Only one
is a genuine offer: `LAUNCH_ART_W1`'s challenge menu offers *"Master screen
printing from zero"* beside five runnable options. GROW W2's two are already inside
A2a's 25.

**It does not reach outside LAUNCH.** Summer 1 is not a second instance — its
"No screens, squeegees or fabric inks needed" is a *refusal*, and its spine gets it
right.

The first run reported **24 hits in 16 files**, every extra one a substring:
`etched` inside *sketched*, `etchbooks` inside *sketchbooks*, `sewhere` inside
*elsewhere*, `ETCHES` inside *SKETCHES*. Recorded because a sweep finding trouble
in sixteen files reads as a crisis and would have moved the pass boundaries a
fourth time on nothing.

**Limitation, declared:** this sweep tests offers against a *list* of absent
processes — A8's old weakness. The category-correct version enumerates every option
in every choice menu and checks each against the kit. Not built.

## Withdrawn — relayed from the lost sandbox, contradicted by the sibling at HEAD

Phantoms four, five and six. Visible rather than tidy.

| withdrawn | replaced by | reason |
|---|---|---|
| fault card `lift` | `island` | `lift` is step five of the chain, where it names the *correct* action; the sibling's own `drag` fix reads "straight down, **lift** straight up". One word on both success and failure in one file. |
| fault card `shift` | `slip` kept | the sibling says `slip`, the old GROW W2 key said `slip`; the rename broke two alignments and bought nothing. |
| cue "squeeze until it stops dripping" | "squeeze the sponge out on scrap before you start" | appears nowhere in the sibling; *dripping* has zero hits estate-wide. A sponge that has stopped dripping is still wet enough to `bleed`, the fault directly above it. |

## Standing rules 11–13

11. **An expected value may only change in the same commit as the change that moved
    it if the message carries the full decomposition.** The register keeps the
    sequence as a ladder, so a future reader can check each step was justified
    rather than merely consistent with the last.
12. **An artefact does not assert its own delivery state.** "Nothing is pushed",
    "no token has arrived", "not yet committed" describe the world at write-time
    and expire the moment the artefact moves. That belongs in the report or the
    commit message, which are timestamped by nature. Same shape as R6's 167px and
    the phantom SHAs: true when made, carried where it reads as still true.
13. **Assertions run over readable text — string literals and markup text — not
    over identifiers, selectors, class names or JSON keys. Location is not the
    test; role is.** A pupil-facing sentence inside a `<script>` tag is readable
    text; `grid-template-columns` is not, wherever it sits. *(The first version of
    this rule said "exclude script blocks" and was wrong — it generalised from one
    symptom to a location, and would have hidden the TA brief that sets up an
    inking bench, the worst string in GROW W2.)*

### One addition to the human half — ambiguous words are ruled once

Each ambiguous word gets its ruling recorded once, with the reason, and is not
re-adjudicated later. Otherwise the same word is decided differently in March than
in July and the drift is invisible, because both decisions look like judgement.
`ALLOW` in `assert_kit.py` is that record; `press` is ruled kit in `press corner`
and ordinary in `press Escape`, and that ruling stands.

---

## Ratification, and rules 14–15

### BUILD Autumn 2 is finished

`vocabulary-residue 0` **and** `C5 0`. The first thing in this programme that is
done. The folder that denies the press now carries no press vocabulary anywhere.

### Rule 14 — a defect closes on two independent signals, never one

A2d claimed D-PRESS-02 closed on C5 alone. C5 was not wrong; it was **blind** —
reporting faithfully against a vocabulary that could not see `hand-pulled`. And
blindness reads exactly like a pass. Independent means not sharing a vocabulary, a
corpus or a premise: two checks built on the same word list are one check counted
twice.

### The refusal classifier proposes; it does not decide

Three versions, three different failures: it swallowed an assertion (`Plate not
re-inked`), then missed a trailing negation (`is relief printing. It is off the
table`), then read a fault-card menu as a refusal. A check that decides **intent**
has no final version.

So intent is now **ratified once by a human** and the classifier's remaining job is
regression: it flags changes to the ratified set, and anything new is a
`refusal-candidate` — a question, not a reclassification.

**The ratified nine**, each with its one-line reason, live in `RATIFIED` inside the
instrument so list and check cannot drift apart:

| file | string | ratified because |
|---|---|---|
| Autumn2 SoW | `there is no press, no rollers and no printing inks` | names the kit in order to rule it out |
| Autumn2 SoW | `No press, no rollers, no inks, no blades beyond classroom scissors` | the kit list, stated as what the room does not hold |
| Autumn2 SoW | `is relief printing. It is off the table` | names the rejected route so a reader knows it was considered |
| Autumn2 SoW | `Teaching relief printing in an alternative-provision session` | the pedagogic reason for the refusal; deleting it loses *why* |
| START_HERE | `No press, no rollers, no inks` | the entry document's refusal |
| Summer1 SoW | `No screens, squeegees or fabric inks needed` | Summer 1's own refusal of the screen route |

**The tenth was rejected, and the hesitation was the finding.** `GROW_ART_W7`'s
"Learner stuck at inking" is a fault-card menu, not a refusal — version three of
the classifier reading a list as a disavowal. It returns to kit-dependence, so
GROW W7 is **3**, not 2. Corrected: kit-dependence 45, refusal-context 9,
refusal-candidate 1, offer-scope 2 = 57.

### Rule 15 — word boundaries, which should have been rule 1

All vocabulary assertions match on word boundaries, never substrings. Three
distinct incidents in one day — `plate` inside *grid-template-columns*, `etched`
inside *sketched*, `sewhere` inside *elsewhere* — each fixed locally rather than as
a default. It is now enforced in the harness at import (`_assert_bounded`) so it
cannot be forgotten per-check.

### Token comparison — hash, never prefix

Fine-grained tokens share a fixed prefix plus an account-scoped segment, so two
genuinely different tokens from one account agree on their first twenty-odd
characters. The new token shares **21** with the old. Any prefix comparison is
guaranteed to pass a duplicate eventually. Compare SHA-256 digests: different
digests, different tokens, and the secret never returns to screen. Same family as
"substitution counts are not verification, read-back is" — a check that measures a
proxy instead of the thing.
