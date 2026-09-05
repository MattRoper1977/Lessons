# EASTER HUMAN ITEMS — campaign VB_EASTER_A3

A human item blocks only the plans that need its answer. It never blocks a
family and never blocks the campaign. Each carries the question, the evidence,
and the cells held.

---

## A3-H1 — three cells the coverage instrument cannot score

**Cells held: 3.** Their workbook outcomes carry no distinctive words once
stopwords and corpus-ubiquitous terms are removed, so the SERVES test cannot be
evaluated in either direction. Each already has a standing deck that claims it.

| cell | ruled week | standing deck | verbatim outcome |
|---|---|---|---|
| `'GROW Weekly - Autumn'!C150` | 7 | `GROW_ASDAN/Autumn1_W7_2026-27/GROW_ASDAN_W7_A_Visitor_And_The_Evidence_We_Keep.html` | "Record challenge evidence." |
| `'BUILD Weekly - Spring'!C112` | 16 | `BUILD_ASDAN/Spring1_W1-W6_2026-27/BUILD_ASDAN_W15_Choice_Budget_and_Project_Reset.html` | "Make a choice and say why." |
| `'BUILD Weekly - Spring'!C113` | 17 | `BUILD_ASDAN/Spring1_W1-W6_2026-27/BUILD_ASDAN_W16_Partner_Challenge_and_Seasonal_Goals.html` | "Work with a partner to complete a task." |

**The question, Matt:** does each standing deck teach its outcome? If yes, the
cell is covered and needs no deck. If no, it needs one and joins the target list.

**Why this is not a measurement to improve.** "Make a choice and say why" is four
content words, every one of which appears in most lessons in the estate. Lowering
the distinctiveness floor to score it would make the instrument fire on almost
anything, which is the fail-open the run-13 threshold exists to prevent. The
honest answer is that this outcome is not machine-scorable, and a person should
read the deck.

**Evidence:** `_sownb/vb/evidence/run14/CELL_COVERAGE.json` → `unscorableClaims`;
re-derivable at any time by `_sownb/vb/tools/cell_coverage.py`.

---

## A3-H2 — GROW_HUM_W15 and LAUNCH_HUM_W15 are split candidates

Carried from A2R §4.4, unresolved.

| deck | words | family median | ratio |
|---|---|---|---|
| `GROW_HUM_W15_Rights_Timeline_and_Belief_Resilience.html` | 3529 | 906 | **3.90** |
| `LAUNCH_HUM_W15_Conflict_Causes_and_Ethical_Decisions.html` | 3526 | 822 | **4.29** |

Both declare 40 minutes, so neither is a double period. In both, the overload is
one stage: "I Do 2 · connect" carries ~1,450 words against a 3-minute
declaration, where the same stage in the sibling deck carries 108. Deleting that
stage outright still leaves them near ×2.3; reaching ×1.25 would move about 70%
of the lesson into the drawer, which is not a trim by any reading of the run-11
R5.5 precedent.

**The question:** split each across two periods, or accept a heavy single period
with the overload moved to the drawer? This order's §0c trims them once first;
whatever remains above ×1.6 comes back here.

**Cells held:** none — both decks stand and their cells read covered.

---

## A3-H3 — 19 stale `lesson-config` week labels block the reshell recipe

Carried from A2R, unresolved, and it blocks reshell plans specifically.

The recipe refuses a source whose `lesson-config` week disagrees with the ruled
week of the workbook cell it cites — correctly, as a red control. 19 decks
disagree, **every one by exactly +1**, and every one is a week 14/15/16 deck
whose config carries a filename-era label the run-11 spine re-key left behind.
Meanwhile all 30 decks the recipe *would* accept are already classic-shell, so
reshelling them is a no-op.

**The repair is the 19 labels, not the check.** Correcting them to the ruled week
of their cited cells is a register PR with a planted control. Until it lands, no
n6 deck can be reshelled.

**Cells held:** none directly; the five §1e RESHELL plans may need this first.

---

## A3-H4 — carried, unchanged

- **H14-1 `RULE_CHOICE=<a|b>`** — two pupil-facing rules, no one game file can
  satisfy both. Evidence `_sownb/vb/evidence/run14/R5_TWO_RULES.json`.
- **C100** — LAUNCH ASDAN week 15, E3-L1 versus live Level 2. Matt + Cheryl.
- **ASDAN g16 reference ruling** — g16 passes on 0 of 10 BUILD ASDAN and 0 of 14
  GROW ASDAN decks. Which live deck is each family's reference is a ruling, not
  a measurement.
- **The 54-deck classic-v2 contract backlog** — 54/54 lack stage timings, 24/54
  lack their own lesson-config, 24/54 miss Lundy in one of its three places. CI
  prints the distribution every run, report-only, until the backlog is zero.

---

## A3-H5 — the Lundy banner is counted once per stage, and it is what puts three decks over

**Cells held: none.** Three standing decks are affected; none of their cells is
blocked. This is a ruling about a measurement, not about a lesson.

The three W16 Humanities decks read over the 1.25 operative target. Their excess
is almost entirely one thing: the pupil-facing Lundy banner, printed identically
on every stage.

> "Space means you get room to join in." · "Voice means you get to say it." ·
> "Audience means someone really listens." · "Influence means something changes
> because of what you said."

| deck | ratio | words over target | Lundy banner words | ratio counting banner once |
|---|---|---|---|---|
| `BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html` | 1.53 | 394 | **383** | 1.26 |
| `GROW_HUM_W16_Sources_Campaigns_And_Hope.html` | 1.38 | 116 | **112** | 1.25 |
| `LAUNCH_HUM_W16_Steps_In_Law_And_What_Comes_After.html` | 1.28 | 26 | **144** | 1.11 |

**The question, Matt:** should g23 count a banner repeated verbatim on every
stage once, or once per stage?

**Why I have not just done it.** Both readings are defensible. A pupil reads the
banner once and thereafter recognises it, which argues for counting it once. It
also occupies the slide on every stage and a pupil with a reading difficulty may
re-read it, which argues for counting it as it appears. What is not defensible is
me choosing: discounting a cross-stage refrain makes **every deck in the estate**
pass g23 more easily, and §5 of this order forbids loosening a threshold. A
measurement may be corrected when a planted control proves the old one wrong —
but here the old measurement is not wrong, it is answering a different question
from the one we want asked.

**What happens if it stands as is.** The three decks need ~394, ~116 and ~26
words of real teaching moved into the staff drawer, to compensate for a banner
the estate's own contract requires them to carry (`lundy-in-three-places`). That
is a lesson made worse to satisfy a counting artefact, so I have not done it.

**What happens if the banner is counted once.** All three land at or under the
threshold with no edit at all, and the correction is recorded in
WRONG_BEFORE_RIGHT with a planted control — a deck whose only excess is a refrain
passes, and a deck with genuinely repeated *teaching* still reds.

**Evidence:** re-derivable at any time; the per-deck figures above come from
`_sownb/vb/tools/g23_period_load.py` plus a cross-stage repeat count over
`lesson_stages.stages()`.


---

## A3-H6 — 7,593 words of duplicated instruction, 19 decks, one generator

**Found:** 2026-09-03, while trimming the third of three W15 Humanities decks.
**Status:** measured, projected, not applied. Needs your scheduling decision.

Three Humanities decks were de-duplicated one at a time (#280, #281, #282) and
all three carried the same defect in the same stage. That is not three authoring
accidents — a uniform ×4 repeat inside one named stage is a generator emitting
its task paragraph more than once. So the whole estate was asked the same
question with the same read-only instrument.

    377 decks scanned · 24 affected · 19 with removable duplication
    7,593 removable words · 170 sentences at exactly ×4, 17 at ×2

**What a pupil currently reads.** In `SCI_B_W16B` the eight-sentence task block
("Place two approved fossil images side by side. Describe each before
comparing…") appears **four times running** inside one flat paragraph. There is
no tier label, no heading, nothing that would make the repetition read as three
differentiated versions. The same eight instructions, four times.

**It is not missing differentiation.** I checked, because if the loop had been
meant to emit three tiers then dedupe would leave the deck short of content.
The clean sibling `SCI_B_W14A` has the identical stage structure — three
distinct `<h3>` tier headings, each with its own `<p>` — and differs only in the
task paragraph, 108 words against 597. Nothing is missing. Dedupe restores the
authored shape.

**Ten of the nineteen are live g23 ceiling reds on main right now**, and nobody
has reported them, because §0c was scoped to Humanities. De-duplication alone
clears five of the ten:

| group | decks | ratio now | after dedupe | outcome |
|---|---|---|---|---|
| Science — Build/Grow/Launch, W7 and W14–W20 | 14 | ×1.28–1.78 | ×1.09–1.49 | every one PASSES; 5 reds cleared, 7 reach the 1.25 target |
| ASDAN Spring1 W15/W16 — BUILD ×2, GROW ×2, LAUNCH ×1 | 5 | ×2.40–3.08 | ×1.97–2.57 | **still red** |

Those ratios are measured, not calculated: `dedupe_sweep.py --project` copies
each deck, dedupes the copy and re-runs g23. The repository is never written to,
and a planted mutation that made it write the source reds its own control.

**The five ASDAN decks are the useful negative.** Their overload survives
de-duplication, so it is real teaching content at two-and-a-half times an ASDAN
lesson. They belong with A3-H2's split question, not with this one — and they
are worse than either Humanities split candidate was before its trim.

**The remediation is denominator-neutral.** Not one affected file sits in any of
the nine family baseline sets, so no family median and no p25 floor moves. The
backlog cannot loosen g18 by lowering a floor, and no ratio anywhere else in the
estate changes. That is checked, not assumed.

**Why I stopped rather than fixed it.** Nineteen decks is nineteen lesson units
against a ceiling of 24 with three already spent, and batch 1 alone needs 24
plans. Doing this now would spend the campaign's ceiling on de-duplication and
starve the build the order actually asks for. Scaling the order down is your
call, not mine.

**The question, Matt:** do you want this as its own order before batch 1, or
after the build campaign? My reading is *before*, for one reason — every deck
batch 1 produces comes from the same estate, and if the generator still runs
anywhere, the batch inherits the defect and the ceiling pays for it twice. I
could find no generator script in this repository, so the defect may already be
historical; but "I could not find it" is not "it is not there", and the sweep is
cheap to re-run against anything batch 1 produces.

**Re-run any of this:**

    python3 tools/easter/dedupe_sweep.py --project --output <out>.json
    python3 tools/easter/dedupe_sweep.py --self-test        # 10 controls

**Evidence:** `_sownb/vb/evidence/a3/dedupe_sweep_live.json` — every row carries
the file, the removable words, the stage, and the repeat-factor histogram.

---

## A3-H6 — CLOSED, 2026-09-03, PR #283

Your ruling was "before batch 1, own order". Done: nineteen decks, 7,593 words
of duplicated instruction removed, containment PASS on every one with zero
missing sentences, no family median moved, and the estate re-sweeps to **zero**
removable duplication. Ceiling reds across those decks went 10 → 5.

**Two things you need from this, not one.**

*First, the ceiling.* Nineteen units spent here plus three earlier leaves **2 of
24**. Batch 1 needs 24 plans. The build campaign cannot start against the
current ceiling — it needs raising or re-scoping, and that is a decision only
you can make. I have not assumed either way.

*Second, the five ASDAN decks now belong to A3-H2 below.* Their overload
survived de-duplication, which is exactly what makes them yours.

---

## A3-H2 — split candidates, now seven not two

`GROW_HUM_W15` (×3.02) and `LAUNCH_HUM_W15` (×3.30) are joined by five ASDAN
Spring1 decks whose overload is real teaching content:

| deck | post-dedupe | ratio | family median |
|---|---|---|---|
| `GROW_ASDAN_W16_Authorised_Task_Project_Plan_and_New_Goals` | 2421w | ×2.57 | 940 |
| `GROW_ASDAN_W15_Strengths_Challenge_and_Project_Reset` | 2387w | ×2.54 | 940 |
| `BUILD_ASDAN_W16_Partner_Challenge_and_Seasonal_Goals` | 2441w | ×2.49 | 980 |
| `BUILD_ASDAN_W15_Choice_Budget_and_Project_Reset` | 2394w | ×2.44 | 980 |
| `LAUNCH_ASDAN_W16_Decision_Tools_Banking_Plant_Care_and_Project_Plan` | 2686w | ×1.97 | 1365 |

**Where the overload actually sits, which changes the question.** All five have
the identical profile — nine stages, forty declared minutes — and the words are
distributed against the clock almost exactly backwards:

| stage | words | declared | rate |
|---|---|---|---|
| Lesson overview (title slide) | 327–384 | **0 min** | not timetabled |
| I Do · model | 436–526 | 4 min | 109–132 w/min |
| **I Do 2 · connect** | 491–568 | **3 min** | **164–189 w/min** |
| Independent · evidence | 276–313 | **16 min** | 17–20 w/min |

Two stages carrying about 40% of the words hold 7 of the 40 minutes, while the
stage with 16 minutes carries about 12%. At a 90 w/min supported-reading rate,
"I Do 2 · connect" alone needs roughly 5.5 minutes against its declared 3.

**So this may not be a split at all.** A split assumes there is too much lesson
for one period. What the numbers actually show is a period whose minutes are
allocated against the reverse of its content. Three routes, and the choice is
pedagogic, so it is yours:

1. **Re-declare the minutes** so they match where the teaching is. Cheapest, no
   content lost, and it changes the deck's own data rather than any threshold.
   It would not move the g23 ratio, which is words against the family median —
   but it would make the deck honest about its own shape.
2. **Move content out of the two I Do stages into the drawer.** This is the R5.5
   trim, and here it is defensible in a way it was not for the Humanities decks,
   because the overload is concentrated rather than spread.
3. **Split into two lessons.** Only if the content genuinely needs two periods.

My reading is (2) then (1): trim the concentrated overload, then re-declare what
remains. I have done neither — you said hand them back, and the ratios above are
the measurement, not a proposal I have acted on.

**One observation, recorded rather than acted on, because it is A3-H5's question
in a second form.** The "Lesson overview" stage is the title slide —
`data-type="title"`, `data-min="0"` — and carries 327–384 words of objective,
success evidence and the Lundy banner in every deck in the estate. g23 counts it
as pupil teaching content. Whether a title slide with zero declared minutes
should count is the same question as whether a banner repeated on every stage
should count once or once per stage, and answering either one loosens g23 for
every deck. §5 forbids me deciding it. It is noted here because it is roughly
14% of every deck's word count and it explains part of why the whole estate
reads heavy — not as an argument for any particular answer.

---

## A3-H7 — a deck that does not carry the refrain its family carries

Found by the R3 flip list, 2026-09-04. Not edited.

`LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References.html` measures **0.9% chrome**
where its five LAUNCH Humanities siblings measure ~24%. Under R3 it is the one
deck that flips PASS→RED almost entirely because its family's median fell and
its own did not.

That is not a g23 finding. It says the deck is probably missing the
contract-mandated Lundy refrain — the `lundy-in-three-places` clause the reshell
contract enforces. **The question: is that deck non-compliant, or is its family
over-carrying?** Either answer is a small content PR; neither is mine to pick,
and the g23 red is a symptom, not the thing to fix.

Re-run: `python3 tools/easter/chrome_flip_list.py`

---

## A3N R3 clause (b) — shipped OFF as a DEFAULTED decision

R3 says "any other block repeated within a deck with an identical digest counts
ONCE". Implemented and measured, it reverses R3's own control: the three W16
decks get worse, not better, because the W9–W14 baselines are a richer chassis
generation than the W15/W16 candidates and the rule strips 38% from the
denominator against 31% from the numerator.

It also has nothing left to do — the duplicated teaching it targets was removed
from the estate in #280–#283 and the sweep reports 0 removable words.

So it ships **off**, as a flag (`lesson_stages.REPEAT_COUNTS_ONCE`) rather than
deleted code. **Flipping it to True turns it on and no other edit is needed.**
Full measurements in `WRONG_BEFORE_RIGHT.md`.

---

## A3N-2 §1 — Art had no measurement family, and no Art lesson could be written

Found 2026-09-04 while picking the Art chassis donor. **Acted on** — this is
recorded for a ruling, not left open, because Art authoring stops without it.

The style contract has treated Art as a first-class family all along:
`_sownb/G16_DENOMINATORS_v2.json` names **twelve** families and gives each Art
pathway **108** contract rows, more than any other family in the estate. Only
the word-count baseline, FEB's `g18_measurement.BASELINES`, named **nine**. With
no Art entry the two gates that divide by a family contradicted each other:

| gate | with no Art family | number |
|---|---|---|
| g18 floor | falls back to the GLOBAL p25 | **1638** content words |
| g23 ceiling | `ratioToFamilyMedian` is `None`, and the clause reads *PASS if ratio is not None and ratio <= cap* | **RED, always**, and binding on new work |

So an Art lesson was red on g23 however it was written; and had that been fixed
it would then have had to clear a 1638-word floor that **no live Art lesson in
this estate comes near** — the whole live corpus runs 875–1107 words. The gate
was not strict. It was undefined, and undefined was being read as failure. The
line that would have said so crashed on `f"{None:.0f}"` before it printed.

**What was done.** The rule already written was applied to a family that
qualifies for it: nearest-rank p25 of the family's own live neighbours, with the
global fallback only below `MIN_NEIGHBOURS=5`. Each Art pathway has **14**
measurable live lessons, so it qualifies twice over.

    VB extra  BUILD Art    n=14  p25= 888  median=1015.5  g23 ceiling <=1523w
    VB extra  GROW Art     n=14  p25= 902  median= 918.5  g23 ceiling <=1378w
    VB extra  LAUNCH Art   n=14  p25= 885  median= 894.5  g23 ceiling <=1342w

**Nothing was loosened.** The ceiling is still 1.5× the family median and the
floor is still the family p25, exactly as for the nine. Leaving Art out was
applying a *different* rule to one subject. A control derives all nine FEB
families before and after and they are identical — n, p25 and median, every one.

**The judgement that is yours, not mine.** This defines what "green" means for a
whole subject, so it is written down rather than absorbed: the Art window is
**~885–1350 pupil words**, narrower than Science's (1229–1942) and close to
GROW ASDAN's. If you want Art's ceiling derived from a different corpus — the
eight `*_Estate_v3` W1–W8 decks alone, say, rather than those plus the six
Spring2 `OUTSTANDING_V3` decks — that is a one-line change to `EXTRA_BASELINES`
in `g18_v2_family_floor.py` and a re-run. The corpus is bimodal across two
chassis generations and the median sits between the clusters; that is recorded
rather than smoothed.

Re-run: `python3 _sownb/vb/tools/g18_v2_family_floor.py --families`

**A duplication question falls out of it, not actioned.** The
`Art_Teesside/<pathway>/W1-W8` copies of these same eight lessons measure **zero**
content words under the shell-aware instrument while the `*_Estate_v3` copies
measure ~900–1100. Same lesson titles, two routes, one of them invisible to
every gate in the estate. Logged as **A3-H10**; excluded from the baseline
automatically by the `contentWords` filter, so it moves no number here.

---

## A3-H11 — six Science plans that say there is nothing to teach

Found while building batch 3. **Held back, not authored.**

Six cover-taught Science plans (BUILD, GROW and LAUNCH, weeks 1 and 2) carry the
outcome:

> Baseline assessment (PythonAnywhere) — no new science content; unit starts W3

Two things follow, and they point the same way. Authoring a teaching deck against
an outcome that says there is nothing to teach would be shipping something
doubtful. And BUILD Science's family floor is **1229 pupil words**, which a
baseline-assessment session cannot honestly carry — it would have to be padded
to pass, which is the failure mode the floor exists to prevent.

**The cover teacher still needs something for those six sessions.** A session
sheet — how to run the baseline, what pupils do, what evidence is kept, what to
do when the platform is down — is real and useful and is *not* a lesson deck.
Whether that is what you want, and whether it should sit outside the gate stack
because it teaches nothing new, is a ruling rather than a gate's decision.

The six plans are in `tools/easter/BATCH3_TARGETS.json` under `held`, each with
this reason on the row, so the cells stay visibly open.

---

## A3-H12 — three RESHELL plans in the cover window

`LAUNCH Science W5`, `GROW Art W6` and `GROW Art W7` name a **standing deck to
reshell** rather than a lesson to author. That is a different pipeline
(`reshell_classic_v2`), not the authoring one, and batch 3 held them rather than
authoring over the top of work that already exists. Also listed under `held`.

---

## A3-H13 — the Humanities packs hold more unlisted decks than this batch added

`manifest_sequence.py` added batch 3's six Humanities decks to the three pack
manifests and printed everything else it found unlisted:

    BUILD   BUILD_HUM_W2_A_Special_Book_A_Special_Place.html
            BUILD_Humanities_W1_Pick_a_card_and_say_why_you_picked_it.html
            BUILD_Humanities_W3_Listen_to_Ruth_Then_Point_at_the_Line.html
    GROW    GROW_HUM_W1_Beliefs_And_Worldviews_Around_Us.html
            GROW_HUM_W2_How_Beliefs_Shape_Who_We_Are.html
            GROW_Humanities_W3_Match_the_Lamp_to_Its_Meaning.html
    LAUNCH  LAUNCH_HUM_W1_Belief_Identity_And_Belonging.html
            LAUNCH_HUM_W2_Two_Worldviews_Side_By_Side.html
            LAUNCH_Humanities_W3_Name_the_Guide_Say_the_Meaning.html

Three of those are batch 2's, and six pre-date this campaign entirely. This run
added only what it authored: folding somebody else's decks into a manifest
inside a lesson PR would hide the drift rather than record it.

The tool will add them in one pass when you want it to:

    python3 tools/easter/manifest_sequence.py --pack <dir> --apply

with no `--only`. It is the same round trip, the same derived counts and the
same refusal path.

---

## A3-H14 — the older Art packs are a chassis generation behind

Measured while acting on A3N-3 §2. **Not actioned.**

Forty-two Art decks pre-date this campaign — the eight `*_Estate_v3` W1–W8 decks
per pathway and the six Spring2 `OUTSTANDING_V3` decks per pathway. They are
good decks: n6 shell, nine stages, per-stage `data-min`, the Lundy strip in
eleven places, 875–1107 pupil words.

They carry **no guide toggle, no print pack and no splash**:

    #n6m-guide-css   #n6m-guide-js   data-mbm-guide      the staff drawer
    .print-pack      .print-page     .n6-lc-page         the printable pack
    .n6-splash       .mbmhome        .skip               the entry furniture

So a cover teacher taking one of those lessons has **nothing to print and no
adult guidance drawer** — the two things the cover window most needs — and the
decks cannot serve as chassis donors, because `strip_to_chassis` preserves that
furniture and cannot invent it.

**The question, which is yours:** bring those forty-two up to the current
chassis? It is a reshell, not authoring — the teaching content stays and the
furniture is added — and it would give the Art estate a printable pack and a
staff drawer for Spring 2 and the v3 packs, and make every one of them a
possible donor.

It is a large, mechanical, well-defined job and it is not in any batch's scope.
Recorded rather than started.

Re-run the measurement: `python3 tools/easter/pick_art_donor.py --show-excluded 0`
## AAE-H1 · H2 · H3 · H5 · H6 — the Arts Award items, each holding only what it names

**AAE-H1 — Gold Adviser Toolkit.** The register records Gold's Attempted rule and
file cap as UNKNOWN, toolkit-only. A gate reds any deck that states either, and
the staff block says "confirm with the Gold Adviser Toolkit". Never inferred
from Silver. **Holds nothing.**

**AAE-H2 — the slots are unconfirmed.** `tools/artsaward/SLOTS.json` seeds five
candidates — MIMA, The Auxiliary, Sawdust, Navigator North, Platform A — and
every one is UNCONFIRMED with no booked entry. The colleague running the
programme names the organisation, practitioner, event and showing routes.
**Holds nothing:** every deck is authored route-agnostic across pupils-visit,
they-come-in and live-remote, and a slot changing is a one-file edit.

**AAE-H3 — centre validation and the trained adviser per level.** Recorded as
unknown. Decks state it as staff information and never assert it as done.
**Holds nothing.**

**AAE-H5 — confirm Explore stays BUILD-only**, and whether any pupil sits Explore
AND Bronze in one year, which decides whether the two BUILD Art strands may share
weeks. **Holds nothing** — default taken: separate strands.

**AAE-H6 — name any pupil entered at Gold.** **Holds Gold authoring only.** Gold
is a spec-verified shelf: repairs, no new authoring, and excluded from the Easter
headline and from batch targeting.

---

## AAE — the decks §6, §7 and §8 name for repair are not in this repository

Measured before starting the repairs, so the work is not invented.

    "Arts Leadership" as a deck title        0 files
    "Leadership Portfolio Audit"             0 files

The 44 exemplar decks were **uploaded**, not committed, and the order is explicit
that they are exemplars only — never a donor, never a spec source, never copied.
So §6's "retitle deck 5", §7's "split deck 8" and §8's "relabel deck 7" have no
target in this tree.

What this repository **does** hold is **76 deck-shaped files that name the Arts
Award**, and they are surveyed in `docs/ARTS_AWARD_BSG_CHECK.md` — inferred level
by level, with every contradiction carrying a deck and a line. The repairs §6–§8
describe will be done against **that** measured list rather than against deck
numbers from a set this tree cannot see.

If the 44 exemplar decks are meant to be repaired in place, they need to be in
the repository first. **Holds §6–§8's deck-numbered repairs; holds nothing else.**

---

**AAE-H7 — what the Bronze decks claim in the workbook.** *Holds nothing; the
fourteen Bronze decks ship without a cell claim until this is answered.*

R3(ii) says the Bronze cells sit **under BUILD Art**. Measured before assuming
what that means:

    EASTER_TARGETS.json holds 24 BUILD Art plans
    batches 3 and 4 covered C102-C108
    17 remain uncovered:
      C110-C115  keep a beat · festival art · rehearse · perform · review · log
      C88-C93    colour and sound for feeling · emotion · an artist · technique
                 · review and improve · log a review
      C94-C98    freeze-frame · character · sequence a drama · rehearse · perform

**Not one of the seventeen states a Bronze Part A–D outcome.** Binding a Bronze
deck to "Keep a steady beat" or "Sequence a short drama" would be a deck
claiming to teach an outcome it does not teach, which is the coverage lie the
review's first lens exists to catch. Inventing a cell reference is worse.

So the Bronze decks claim **no workbook cell**, and the binding is left open
rather than fabricated.

**The consequence, stated rather than left to be found.** A deck with no plan
cells carries no `planId`, so **g29 skips it** rather than judging it. The skip
is not silent — one of g29's own controls is
`a-deck-with-no-planId-is-skipped-not-silently-passed`, and the three chassis
already appear in every run as named skips. But *reported* is not *judged*: g29
is the gate that stops two decks claiming the same cell, and for these fourteen
it will report rather than check. Their coverage claim is instead the
`artsAward` block that g30–g35 read and bind, which is a gate reading a
declaration rather than no gate at all.

Three ways this could be answered, in the order they cost:

1. **The Bronze strand gets its own column in the workbook**, and the fourteen
   decks bind to it exactly as every other authored deck does. Cleanest; needs a
   workbook change.
2. **The Bronze strand is placed by catalogue row only** (which R3(ii) already
   schedules for GROW) and the g29 skip is accepted and recorded permanently.
   Cheapest; leaves the fail-open standing.
3. **Bronze re-themes the seventeen uncovered BUILD Art cells** so the outcomes
   and the parts agree. Most work, and it changes what the scheme promises.

Nothing is guessed in the meantime: the decks are authored, gated on everything
that does apply, and the cell column stays empty.

## AAE-R1B closeout clarification — 4 September 2026

The earlier entries above are retained as history. R1B voided the exemplar deck repairs: do not import those binaries or wait for them. Gold is a SPEC-based shelf record, not repairs to absent decks. PR303 introduced bound award-plan identities, so all 42 new award decks are judged by g29; they are no longer the predicted no-planId skips described in the earlier AAE-H7 entry. Their workbook cell sets remain empty following the documented independent reviews. The three named nonlesson chassis are still legitimate skips.

All 42 new award lessons, both secondary placement links and the three catalogue pairs are delivered. The unconfirmed slots, centre/adviser information and possible Gold entrant do not hold the wider Easter Science/Humanities/ASDAN/Art continuation. The whole Easter programme is still active.

## AAV-H3 — the mechanism battery derives its counts over a hand-typed roster

Found while repairing g28 (AAV-NIGHT, 2026-09-05). `mechanism_battery.py` states that nothing in it is pinned. Its control COUNTS are genuinely derived; its TOOL LIST is two hand-typed Python literals. A gate is therefore invisible to the battery until a human types its filename, and `g28_cell_existence.py` — which has had a working `--self-test` all along — was never typed, so its controls ran nowhere, in CI or out of it, until this order added it.

g28 is fixed. The class is not. Any gate added since, or added next, is silent by default rather than caught by default, and the battery's own docstring reads as though that cannot happen.

The fix is auto-discovery: enumerate `_sownb/vb/tools/g*.py` plus the declared `tools/easter` and `tools/artsaward` members, require each to answer `--list-controls`, and red on any tool that cannot. That inverts the default from opt-in to opt-out. It is a real mechanism change and §8c closes that door without a control failing, so it is NOT done here and is put to Matt instead.

Counter-consideration, so the decision is a real one: auto-discovery would red the battery on every helper script that happens to sit in those directories and has no controls to declare, so it needs an explicit "declares no controls" opt-out — which is itself a list, just an inverted one. The gain is that the inverted list fails loudly (a new gate reds until classified) instead of silently (a new gate is skipped until noticed).

## AAV-H2 — the Art chassis authority is contested, and the numbers are here

The order §3 names `Art_Teesside/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html` (sha256 `2eb0f84c…`) as the chassis every Art lesson must match. #316, merged 33 minutes before the order was issued, moved 101 campaign decks — 59 Easter units and all 42 award units — onto the CLASSROOM chassis at your request. These are two different design systems, sharing exactly one token (`--muted`).

Measured, 1280×820, all 42 against the reference: **0 of 42 match on all ten surfaces**, in only two delta signatures. h1 40px→40.96px · h1 colour #000→#101820 · slide padding 40px→38.4px · Lundy purple #f3e8ff→slate #f8fafc · button terracotta-on-transparent→white-on-teal. Stage-0 screenshots show the same styling family, differing in title-slide furniture and nav treatment.

Not actioned, because two of those deltas reverse your own later preference: the ledger of 2026-09-04 records that you now prefer lighter Lundy integration, and slate is lighter than purple. Restyling 101 live decks toward a reference that predates that choice is not a build decision.

**The part that needs deciding either way:** the frozen g16/g19 contract for BUILD/GROW/LAUNCH Art still describes the pre-#316 chassis, so it reds every restyled deck AND would red every future Art deck. It only looks quiet because g16 and g19 are not run per-deck in CI. Two coherent resolutions, and no third:
1. **Classroom chassis is canonical** → re-freeze the Art contract rows against a restyled deck, put g16/g19 into CI, and the estate is consistent. This ratifies what shipped.
2. **The named reference is canonical** → regenerate the 101 through the classroom presentation with the reference's palette and metrics, one token patch (the divergence is systematic, so this is feasible), and keep the contract as it stands.

Option 1 is cheaper and matches your latest stated preference. Option 2 matches the order as written. I did not pick between your two instructions.

Separately: the reference itself fails one of its own contract rows, `sequence.key-facts.build-art` (107/108). §3c says fix the reference before copying it, so that is worth doing under either option.

## AAV-H4 — is the Lundy refrain pupil prose, or chrome?

§9 of the night order says contract refrains — Lundy banner, title slide, running head — are chrome, counted zero in g23. g26 counts them as pupil prose when it measures reading level. The same sentence is therefore chrome to one gate and pupil text to another.

It decides two live verdicts. With the block-boundary bug fixed (landed), the two remaining reds are:

| deck | pupil FK now | with chrome excluded | BUILD band |
|---|---|---|---|
| BUILD_Art_Explore_W2_Test_A_Join_And_Compare_My_Learning | 4.04 RED | 3.97 PASS | 1.0–4.0 |
| BUILD_Art_Explore_W4_Connect_The_Artist_Organisation_And_What_I_Found | 4.15 RED | 3.82 PASS | 1.0–4.0 |

Both overshoot **solely** on chrome — the highest-FK sentence in each is the Lundy refrain "VOICE: the evidence statement remains in the learner's chosen communication mode." That refrain is identical in all 42 decks, so it drags every Art deck's score by the same amount and will do so for every deck the campaign writes next.

I did not decide it, because extending a g23 ruling to g26 moves two decks from RED to PASS and can fairly be read as loosening a threshold, which §9 forbids. Neither deck was reworded either: rewriting real teaching to offset a refrain the pupil is not asked to decode would have bought a green tick and cost a lesson.

**If chrome is chrome:** g26 excludes `.lundy`, the title slide and the running head, the two decks pass on their own prose, and the gate finally measures the same text §9 says to measure.
**If it is not:** the refrain's own wording is the thing to simplify — once, in the donor, which fixes all 42 and every future Art deck at a stroke. That is the better outcome if you want the number to stay honest, and it is a content change, so it needs you.

## AAV-H5 — a week tier in the hub needs a week in the catalogue

§6b asks for pathway → subject → term → week. The first two are built and shipped. The last two are not, because the data does not exist and §9 forbids inventing it.

Of 540 catalogue rows typed `lesson`, **51** carry a lesson-config and **9** have a workbook cell that resolves to a spine week. That is 1% coverage. A term/week tier built on it would be a navigation promise the catalogue cannot keep.

The tempting shortcut is the one g27 exists to stop: most decks say "W7" in their filename or their card title, and reading it from there would populate the tier instantly and wrongly — a filename is a label, and this estate has already been bitten by a label disagreeing with TRACE (three LAUNCH Science decks this same night, fixed in #318).

The honest route, when you want it: add a TRACE-derived `week` and `term` to each catalogue row at the point the catalogue is built, sourced from the deck's own `cells` through CALENDAR_SPINE.json — the same derivation #318 used. Rows whose deck has no resolvable cell get no week and simply do not appear under a week heading, which is truthful rather than tidy. That is catalogue work and lands alone.
