# GUIDE TAG MAP — the nine landed 2026-27 packs

`ORDER N6-I · I5` · measured 2026-08-28 · branch `claude/new-session-q7ztqq`

**Nothing in this document has been applied. Nothing was patched. This is a map and a
price, as the order requires.**

---

## The headline, before the tables

> **A correction, at the top, because an earlier version of this document said the
> opposite.** The first pass of this map probed for a chosen list of *string families* —
> SoW cell references, `Exact SOW outcome`, `Estate sequence`, `AQA UAS` — and concluded
> that eight of the nine packs put no staff-facing text on screen at all. **That was wrong.**
> A string-family probe finds the families it was handed. Re-probing by **addressee** —
> who is the sentence talking to? — finds staff-facing content visible in **all nine
> packs**: GROW_ASDAN's *"Staff: select one route before giving this page to the learner"*,
> LAUNCH_ASDAN's *"Authorship check: Staff may model the process…"*, Science's
> *"Sequence outcome: Rocks: test hardness."*, BUILD_Humanities' *"Named-adult
> report-back · Decision maker: Class teacher — replace with the adult's name before
> delivery."* The corrected measurement is what follows. The error is recorded rather than
> quietly overwritten, because the method that produced it is the method a future pass will
> reach for first.

Three things were measured that change what this job is:

1. **The TA/teacher briefing layer is already invisible to the room, and it is the bulk of
   the guidance.** 132 of the 159 files carry `data-ta1`/`data-ta2` briefing strings — 1188
   of them — and **zero** reach the pupil-facing surface. They live in four container
   families, one per lesson deck, none visible at load. PH-3's headline purpose is already
   achieved by the chassis for that layer.

2. **But staff-facing text on the slides themselves exists in all nine packs**, and it is a
   different thing from the briefing layer: delivery routines, authorship boundaries,
   named-adult actions, and SoW provenance.

3. **Almost all of it is reachable with selectors that already exist.** `.staff`,
   `.choose`, `.guard`, `.evidence-note`, `.boundary`, `.screen`, `.reportback`, `.lnote`,
   `.sowline`, `.lesson-link`, `.small` are purpose-built and clean; four more BUILD_ASDAN
   families need label- or position-keying rather than a new attribute. **Exactly one family
   in one pack has to have a marker authored:** BUILD_ASDAN's `Exact SOW outcome` paragraph,
   25 files.

---

## §1 · What the twelve packs are, and what could be measured

The order says twelve packs. **Nine are in the repository and were measured. The three Art
packs are not** — they were an intake tree in the previous session and no commit on any
branch ever added them, so their selectors cannot be counted here and are not guessed at.
That is 159 HTML files measured of the 192 the order counts.

## §2 · Why the PH-3 patcher cannot see any of this

`_eca1/tools/guidepatch.js` classifies by `.li-box`, `.task-box` and `.wit-panel` and tags
with `data-mbm-guide`. Across all nine packs those occur **0, 0, 0 and 0** times. The
patcher therefore classifies all 159 as chassis `doc` and skips every one, exactly as the
previous pass reported.

**The semantic hide-set that was "already ruled" does not map either.** Checked
case-insensitively across all 159 files:

| PH-3 vocabulary | files carrying it |
|---|---:|
| `sow-strip` | 0 |
| "How it works" | 0 |
| "Key Question" | 0 |
| "Spark" | 0 |
| "👀 Look:" | 0 |
| "Key Idea" | 5 |
| "Instructions" | 11 |
| "Step 1" | 42 |

So this is not "the same job with different selectors". Six of the eight ruled markers do
not exist in these packs at all.

## §3 · The guidance-container census — what actually holds the guidance

| pack | html | `#teacherDialog` | `#taOverlay` | `#taDialog` | `#tool-ta` | `data-ta1` | `data-ta2` | `.staff-card` | `.note` | `.drawer-card` | `.route*` | `.tierbtn` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `BUILD_ASDAN` | 28 | 24 / 24 | — | — | — | 24 / 216 | 24 / 216 | — | — | — | 25 / 218 | — |
| `GROW_ASDAN` | 22 | — | 18 / 18 | — | — | 18 / 162 | 18 / 162 | 18 / 72 | 21 / 203 | — | 19 / 90 | — |
| `LAUNCH_ASDAN` | 32 | — | — | 30 / 30 | — | 30 / 270 | 30 / 270 | — | 30 / 150 | 30 / 210 | 30 / 90 | — |
| `BUILD_Science` | 15 | — | — | 12 / 12 | — | 12 / 108 | 12 / 108 | — | 12 / 48 | — | 12 / 96 | 12 / 108 |
| `GROW_Science` | 16 | — | — | 12 / 12 | — | 12 / 108 | 12 / 108 | — | 12 / 48 | — | 12 / 96 | 12 / 108 |
| `LAUNCH_Science` | 21 | — | — | 18 / 18 | — | 18 / 162 | 18 / 162 | — | 18 / 234 | — | 18 / 144 | 18 / 162 |
| `BUILD_Humanities` | 8 | — | — | 6 / 6 | — | 6 / 54 | 6 / 54 | — | 8 / 98 | 6 / 24 | 6 / 18 | 6 / 36 |
| `GROW_Humanities` | 8 | — | — | — | 6 / 6 | 6 / 54 | 6 / 54 | — | 6 / 14 | — | 6 / 16 | 6 / 36 |
| `LAUNCH_Humanities` | 9 | — | 6 / 6 | — | — | 6 / 54 | 6 / 54 | — | 7 / 58 | 6 / 48 | 6 / 18 | 6 / 18 |
| **total** | **159** | **24 / 24** | **24 / 24** | **78 / 78** | **6 / 6** | **132 / 1188** | **132 / 1188** | **18 / 72** | **114 / 853** | **42 / 282** | **134 / 786** | **60 / 468** |

*(files carrying it / total occurrences. `—` is zero.)*

**Four container families, disjoint, and every one of the 132 lesson decks has exactly
one.** 24 + 24 + 78 + 6 = 132.

| container | packs | what it is in the DOM | visible at load |
|---|---|---|---|
| `#teacherDialog` | BUILD_ASDAN (24) | `<dialog role="dialog" aria-modal="true">` | no |
| `#taOverlay` | GROW_ASDAN (18), LAUNCH_Humanities (6) | `<div class="overlay" aria-hidden="true">` | no |
| `#taDialog` | LAUNCH_ASDAN (30), Science ×3 (12+12+18), BUILD_Humanities (6) | `<div class="overlay" role="dialog" aria-modal="true" hidden>`; in Science a `<dialog data-audience="staff">` | no |
| `#tool-ta` | GROW_Humanities (6) | `<section class="toolsection" role="tabpanel">` in a tools drawer | no |

**`data-ta1` / `data-ta2` are ATTRIBUTES, not elements** — 1188 of them across the nine
packs, on `<section class="slide">`. No CSS selector can hide an attribute; only the
container that renders it. Anyone planning a hide-set of selectors needs to know that
before starting, because it means the guidance payload and the thing you can actually
target are different objects.

## §4 · What is visible to the room — the real hide-set

Measured by activating every slide in turn and reading the visible `innerText`, which
excludes a closed `<dialog>`, a `[hidden]` element and any `display:none` subtree. The
all-slides walk is load-bearing: these decks hide non-active slides with
`.slide{display:none}`, so reading at load returns the title slide and nothing else.

Files where the family is present in source / **visible across all slides**:

| pack | SoW ref | `Exact SOW outcome` / `Sequence outcome:` | `Estate sequence` | `AQA UAS` | staff addressed directly | adult prompting instruction | delivery routine label |
|---|---:|---:|---:|---:|---:|---:|---:|
| BUILD_ASDAN | 28/**28** | 25/**25** | 26/**26** | 25/1 | 24/**24** | 25/**25** | 24/**24** |
| GROW_ASDAN | 0/0 | 0/0 | 0/0 | 0/0 | 19/**19** | 19/7 | 19/**19** |
| LAUNCH_ASDAN | 0/0 | 0/0 | 0/0 | 13/**13** | 30/**30** | 31/1 | 30/**30** |
| BUILD_Science | 0/0 | 12/**12** | 0/0 | 0/0 | 12/0 | 12/0 | 0/0 |
| GROW_Science | 0/0 | 12/**12** | 0/0 | 0/0 | 12/0 | 12/0 | 0/0 |
| LAUNCH_Science | 0/0 | 18/**18** | 0/0 | 0/0 | 18/0 | 18/0 | 0/0 |
| BUILD_Humanities | 0/0 | 0/0 | 0/0 | 0/0 | 6/**6** | 6/0 | 0/0 |
| GROW_Humanities | 7/2 | 0/0 | 0/0 | 0/0 | 3/**3** | 7/1 | 1/1 |
| LAUNCH_Humanities | 0/0 | 0/0 | 0/0 | 0/0 | 6/0 | 1/1 | 6/0 |

**Every pack has something visible.** The Science packs' is a single clean provenance line;
the ASDAN packs carry delivery routines and authorship boundaries as well; the Humanities
packs carry named-adult actions and pedagogical notes.

**Route labels are pupil-facing and stay.** `Supported route` / `Standard route` /
`Stretch route` are visible in GROW_ASDAN 19/19 and LAUNCH_ASDAN 30/30, and a pupil chooses
between them. Treating "route metadata" as a hide target — the reading the order's wording
invites — would remove the pupil's own access route from the screen. GROW_ASDAN's `.soft`
looks staff-facing to a keyword probe and is not: *"Standard: add a reason or example.
Optional reach: name what evidence could change your first answer."* is addressed to the
pupil.

## §5 · The candidate hide-set, per pack, read rather than pattern-matched

Every candidate below is a class **all of whose instances** carry staff material, then read
in a browser to confirm what the whole block says and whether it is on screen. Machine
matching proposes; reading disposes — a literal-match-ratio test was tried and discarded,
because these are staff *labels* on prose blocks and the prose does not match the label.

| pack | selector | instances | on screen | what it says | verdict |
|---|---|---:|---|---|---|
| GROW_ASDAN | `.choose` | 18 | **yes** | *"Staff: select one route before giving this page to the learner. Change access, not authorship."* | **clean — tag it** |
| GROW_ASDAN | `.staff` | 18 | **yes** | *"Staff pre-stage before the 16-minute transfer · Select two current, centre-approved job and route cards…"* | **clean — tag it** |
| GROW_ASDAN | `.guard` | 18/74 | **yes** | *"Teaching / qualification boundary · Learners contribute to the project; they do not authorise external contact…"* | **clean — tag it** |
| GROW_ASDAN | `.evidence-note` | 18/36 | **yes** | *"Potential evidence only. Keep adult preparation and support separate…"* | **clean — tag it** |
| GROW_ASDAN | `.boundary` | 18/36 | **yes** | *"Use: preserve the learner's first prediction and explanation…"* | **clean — tag it** |
| LAUNCH_ASDAN | `.screen` | 30/60 | **yes** | *"Authorship check: Staff may model the process and preserve access…"* | **clean — tag it** |
| BUILD_Humanities | `.reportback` | 6 | **yes** | *"Named-adult report-back · Decision maker: Class teacher — replace with the adult's name before delivery."* | **clean — tag it** |
| BUILD / GROW / LAUNCH Humanities | `.lnote` | 12/54, 6/90, 6/54 | **yes** | *"One Lundy loop only. Humanities adds disciplinary interpretation, not a second closure system."* | **clean — tag it** |
| Science ×3 | `.sowline` | 12, 12, 18 | **yes** | *"Sequence outcome: Rocks: test hardness."* | **clean — tag it** |
| BUILD_ASDAN | `.lesson-link` | 24 | **yes** | *"…BUILD_A2_PFA_W1 · Estate sequence W9 · 'BUILD Weekly - Autumn'!C137"* | **clean — tag it** |
| BUILD_ASDAN | `.small` | 24/24 in decks | **yes** | *"Source: 'BUILD Weekly - Autumn'!B181 · …!C181"* | **clean — tag it** |
| BUILD_ASDAN | **`.chips .chip:last-child`** | 24 | **yes** | *"Estate sequence W9"* — verified as the last chip in **24/24** decks, so a positional selector reaches it and the other three chips are untouched | **clean — tag it, no marker needed** |
| BUILD_ASDAN | `.box.objective` **keyed on its `<strong>` label** | 72 of 96 | **yes** | `SPACE routine` · `Model aloud:` · `Connect:` are staff; the fourth, `Learning objective:`, is the pupil's. Exactly 24 of each, verified | **clean if label-keyed — class-wide would delete the objective from every deck** |
| BUILD_ASDAN | `.box.good` **keyed on its label** | 48 of 96 | **yes** | `Authorship check:` and `Adult close` are staff; `Success criteria` is the pupil's and `Potential evidence: assessor review required` is the assessor's. 24 of each | **clean if label-keyed** |
| BUILD_ASDAN | `.box.rehearsal` **keyed on its text** | 24 of 120 | **yes** | only *"Do not reveal the pupil's whole answer…"* is staff; the other 96 are pupil-protective (*"Screen rehearsal only…"* ×72, *"The sequence advances only when a person chooses"* ×24) | **clean if text-keyed** |
| BUILD_ASDAN | `.hero` | 24 | **yes** | holds `Exact SOW outcome:` **and** the lesson `<h1>` and objective; the outcome paragraph is unclassed | **the one family that needs a marker authored — 25 files** |
| BUILD_ASDAN | `.model-step` | 144 | **yes** | **KEEP VISIBLE.** Six per deck on slides 4 and 6, revealed one at a time by the teacher's button. They read as step-by-step instructions and any "Step"/"How it works" rule catches them — but measured, they are **49–58% of their slide's text**, so hiding them halves two slides per deck. This is the shape of the 140-of-175 incident. | **do not tag** |
| all nine | `.prompt-ladder` / `.ladder` / `.adult-action` / `.mobile-teacher-tools` / `.print-note` | — | **no** | already inside a dialog, drawer or print-only block | **no action** |

**So the hide-set is almost entirely mappable.** Fourteen selector families across the nine
packs are reachable with selectors that already exist — ten plain, and four in BUILD_ASDAN
that need **label- or position-keying** rather than a new attribute (`.chips
.chip:last-child`, and `.box.objective` / `.box.good` / `.box.rehearsal` keyed on their
leading `<strong>` label, which is exactly the `STAFF_LABELS` mechanism `guidepatch.js`
already implements).

**The residue that genuinely needs a marker authored is one family in one pack**:
BUILD_ASDAN's `Exact SOW outcome` paragraph, unclassed inside `.hero`, **25 files**.

*(Two probe artefacts worth recording so a later pass does not chase them. `.enhanced` in
the Science packs appears in the candidate list because its element is a `<style>` block and
the probe read CSS text as content. And an earlier, case-sensitive run of the overlap probe
reported `.small` as mixed with ten pupil-facing instances; all ten were staff strings missed
on a lower-case `e`. A probe case-sensitive about prose invents overlap.)*

## §6 · Worked example — `BUILD_ASDAN_A2_COMM_W1_Review_Progress_and_Solve_a_Problem.html`

Slide 1, "Lesson overview", exactly as a class sees it on the wall:

```
BUILD ASDAN | Community & Vocational | Autumn 2 · Week 1 | Estate sequence W9
Project Checkpoint: Solve the Real Blocker
Exact SOW outcome: Review progress and solve a problem as a team.
Source: 'BUILD Weekly - Autumn'!B181 · 'BUILD Weekly - Autumn'!C181
Learning objective: I can help the team review progress and choose one workable
problem-solving action.
Success criteria
  I can identify one completed, in-progress or blocked project action from evidence.
  I can suggest or choose one safe solution without blaming a person.
  I can explain how the agreed action changes the project plan.
```

**Would be tagged (3 items, all on this one slide):**

| text | carrier | can an existing selector reach it? |
|---|---|---|
| `Estate sequence W9` | `<span class="chip">`, the 4th of 4 | **yes** — `.chips .chip:last-child`, verified as this chip in 24/24 decks |
| `Exact SOW outcome: Review progress and solve a problem as a team.` | unclassed `<p><strong>…</strong> …</p>` inside `.hero` | **no** — no class and no stable position. This is the one marker that has to be authored, in all nine packs |
| `Source: 'BUILD Weekly - Autumn'!B181 · 'BUILD Weekly - Autumn'!C181` | `<p class="small">` | **yes** — `.small` is 24/24 clean in the lesson decks |

**Would stay visible:**

`BUILD ASDAN`, `Community & Vocational`, `Autumn 2 · Week 1` (the same `.chip` class as the
tagged item), the `<h1>` lesson title, `Learning objective:`, all three success criteria,
the pupil task, the Lundy zone boxes, the route ladder, and every `data-ta1`/`data-ta2`
string — which is already invisible and needs no tagging.

**What would break if the mapping were wrong for this file.** Hiding `.chip` removes the
lane, unit and week — a pupil arriving mid-term loses the only on-screen statement of where
they are. Hiding `.hero` removes the lesson title and the learning objective, which is the
140-of-175 failure the patcher's own comments record. `.small` and `.lesson-link` are the two
safe moves on this deck and between them they remove one of the three items on this slide;
the other two are what the 51 authored markers are for.

**And this deck is the hard case, not the typical one.** In GROW_ASDAN the same job is
`.choose`, `.staff`, `.guard`, `.evidence-note` and `.boundary` — five clean, purpose-built
classes. In the Science packs it is one: `.sowline`. BUILD_ASDAN is the only pack where the
staff text was written without a class of its own.

## §7 · Cost

| # | work | scope | estimate | what drives it |
|---|---|---|---:|---|
| 1 | **Tag the ten clean selector families** | `.choose` `.staff` `.guard` `.evidence-note` `.boundary` (GROW_ASDAN) · `.screen` (LAUNCH_ASDAN) · `.reportback` `.lnote` (Humanities) · `.sowline` (Science ×3) · `.lesson-link` `.small` (BUILD_ASDAN) | **a selector list, not an edit** — the classes exist and are clean | This is the part that really is patching. It is one CSS rule per family plus the toggle. |
| 2 | **Label- and position-key four BUILD_ASDAN families** | `.chips .chip:last-child` · `.box.objective` · `.box.good` · `.box.rehearsal`, keyed on the leading `<strong>` label | **a selector list** — `guidepatch.js` already implements `STAFF_LABELS` | Class-wide rules here are the dangerous ones: `.box.objective` class-wide deletes the pupil's `Learning objective:` from every deck. |
| 3 | **Author markers for the residue** | BUILD_ASDAN only: the `Exact SOW outcome` paragraph, unclassed inside `.hero` | **25 marker insertions**, an hour or two with the checks | It is the only visible staff string in all nine packs with neither a class nor a stable position. |
| 4 | **Render / visibility check per family per lane** | already built | **~5 minutes per run** | `s24-print-renders` renders all 159 to A4; `i5_guidance_visibility.mjs` walks every slide of all 159 and reports what reaches the screen. This was the expensive line item in the previous estimate and is not any more. |
| 5 | **The `localStorage` question** | a straight fork, unchanged from N7 | **a ruling, not engineering** | PH-3 persists `mbm_guide_v1`; gate 4 requires 0 browser storage and every deck declares `storageKeys: []`. Narrow gate 4 to that one key (matching 175 estate carriers), or ship the toggle without persistence. |
| 6 | **Regression** | 159 files, ~40 touched | **low** | Additive, markered, strip-reversible in the estate's usual pattern; `s24` and the existing battery both gate it. |

### What a toggle would and would not remove

**Would remove, and is worth removing from a projected screen:** GROW_ASDAN's *"Staff:
select one route before giving this page to the learner"* and its staff pre-stage block;
LAUNCH_ASDAN's authorship check; BUILD_Humanities' *"Decision maker: Class teacher —
replace with the adult's name before delivery"*, which is an unfinished instruction to the
teacher sitting on the wall; the Humanities Lundy notes.

**Would remove, and is more arguable:** the SoW audit trail — BUILD_ASDAN's `Estate
sequence W9`, `Exact SOW outcome:` and `Source: …!B181`, and Science's `Sequence outcome:`.
A teacher can see which SoW cell the lesson came from without opening anything, which is
defensible as a feature.

**Would not remove, because it is already invisible:** the whole TA briefing layer — 1188
`data-ta1`/`data-ta2` strings across 132 decks, plus the prompt ladders, adult-action notes
and teacher-tool drawers. This is the bulk of the guidance and needs no toggle at all.

### What is NOT priced

The three Art packs. They are not in this repository, so their selectors were not counted
and their cost is not estimated. On the pattern of the nine, an Art pack would be one more
container family and somewhere between one and three visible families — but that is an
extrapolation, and it is labelled as one.

## §8 · The tools this map was measured with

| tool | what it measures |
|---|---|
| `_next6/tools/i5_guidance_visibility.mjs` | walks every slide; reports which of a deck's own TA strings reach the visible surface, which container family holds them, and which staff-facing string families are on screen — keyed by **addressee**, not only by a chosen list of phrases |
| `_next6/tools/i5_overlap.mjs` | for every class in every deck, how many instances carry staff material in their own text — the overlap risk, measured in a real DOM |

Both are read-only and take a file list. Neither applies anything.
