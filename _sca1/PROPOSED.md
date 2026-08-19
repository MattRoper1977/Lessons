# SCA-1 — PROPOSED (not applied). Matt rules on these.

Base: `72778591e8c1fe1d9c5b979c90ccbbd868de4b3a` · branch `claude/sca-1-science-correctness`

Nothing in this file has been applied. Each item says which track it came from, what the
bytes currently say, what is proposed, and why it was not applied under the pass rules.

---

## P0 — WITHDRAWN: witness-statement lesson names are correct
**Track A · BUILD + GROW · raised, then refuted on the bytes · NO ACTION**

This pass initially raised the ten B/"Do" witness statements as naming the wrong lesson,
because each B lesson's witness `Lesson` field holds the A lesson's title (e.g.
`SCI_B_W3B_Backbone_Detectives_Do.html` has its own `<h1>Backbone Detectives</h1>` but a
witness field reading "Backbones and No Backbones — BUILD Science · Week 3 ..."). An
adversarial verification refuted it, and re-checking the bytes confirms the refutation:

1. **The route suffix disambiguates, and sits inside the same string.** All 20 BUILD/GROW
   lessons: every A reads `(40-min route · Explore)`, every B reads `(40-min route · Do)`.
   The field is `<week topic> — <PATHWAY> Science · Week N (40-min route · Explore|Do)` —
   a week-and-route anchor, not a lesson-title field.
2. **It is a convention applied without exception**, 20/20. The same uniformity test is
   what cleared LAUNCH's 15 (`Use: Osmosis Core Practical` for `Osmosis Core Practical`);
   applying it consistently clears BUILD/GROW too.
3. **The portfolio is never ambiguous.** W3B's own print pack names the specific lesson
   twice more: "BUILD Science W3B · Backbone Detectives" and "Evidence capture sheet ·
   W3B · Backbone Detectives".

A topic/unit-level anchor is appropriate on a Pearson ELC 8939 / AQA UAS accreditation
record. **No defect. No change proposed.** Recorded here rather than deleted so the check
is visible: the witness statements were examined and cleared, not skipped.

## P1 — SYSTEMIC · every hinge question has its correct answer in position 0
**Track C (question construction) · all three pathways · 35/35 questions · HIGH**

Every "commit before reveal" hinge question in the suite encodes the correct answer as the
**first option**, and no lesson contains any shuffle or randomisation logic.

Evidence (derived, universe stated):
- `data-correct` / `data-c` across `Science_Teesside/*/v3_40min/SCI_*.html` = 35 questions.
  Index distribution: `{0: 35}`. Table: `_sca1/tables/answer_keys.csv`.
- Shuffle logic: `grep -l 'shuffle\|Math.random\|randomi'` over the same 35 files = **0 files**.
- CSS reordering: true `order:` property (preceded by `;`/`{`/space) = **0 occurrences**
  (all 1 900+ naive `order:` hits are `border:` substrings).

Why it matters: a pupil who always presses the first button scores 100% on every hinge
question in all 35 lessons without any science knowledge. Hinge questions exist to surface
misconceptions before the reveal; a fixed answer position removes their diagnostic value
and inflates the "commit" evidence the Lundy loop then receives.

Proposed: vary the correct index across the suite, or shuffle option order at render while
keeping `data-correct` pointing at the right option.

**Not applied.** §5 protects `data-*` answer keys, editable "only when Track A proves an
answer WRONG". All 35 answers are scientifically CORRECT (verified individually — see
`_sca1/tables/answer_keys.csv`), so the exception does not apply. This is Matt's call.

---

## P2 — GROW W4B Stretch route asks for a measurement with no unit on any pupil surface
**Track A · GROW · MEDIUM**

`SCI_G_W4B_Mechanisms_Do.html`, Stretch route, screen **and** print, identical wording:

> ★ Measure the effort. Then measure the movement distance. Explain the trade-off. Use both
> pieces of evidence.

with the scaffold "Use numbers if you are ready."

"Effort" is a force. Newtons are named **once** in the file, in the teacher-facing
PRACTICAL READY block ("record the force in newtons (N)"); no pupil-facing surface names a
unit for the effort. Distance likewise carries no unit here.

Proposed: `★ Measure the effort — in newtons (N) if you have a spring balance. Then measure
the movement distance in centimetres (cm). Explain the trade-off. Use both pieces of evidence.`
(keeps the agreed-scale fallback the teacher block allows, so a class with no spring balance
is not blocked).

**Not applied.** Pass GSA-FIX-1 landed "W3B/W4B newtons" and the spring-balance line; both
are present and verified at base. Extending the unit onto the pupil Stretch route goes
beyond verifying landed work, and the master prompt says do not re-litigate it.

---

## P3 — BUILD uses `explain` at Supported/Standard, above its stated command-word set
**Track C · BUILD · LOW**

BUILD's stated command words are name / say / point / sort / match / describe. `explain`
opens 6 Standard-tier stems and `complete` one Supported stem, e.g.:

- `SCI_B_W4B` Standard exit: "Explain the muscle swap using contract and relax."
- `SCI_B_W7B` Standard exit: "Explain one link in your chain."
- `SCI_B_W4A` Supported exit: "Complete: muscles work in a ___."

Full table: `_sca1/tables/cmd_offpitch.csv` (86 rows; 11 are BUILD Stretch, which is
defensible differentiation and **not** proposed for change).

Proposed: either re-word the 7 non-Stretch stems to the BUILD set, or widen the documented
BUILD command set to include `explain` at Standard.

**Not applied.** §4 sends scaffolding and pitch judgements to PROPOSED. Reading-band (FK)
data is report-only per the prompt and is **not** offered as evidence here.

---

## P4 — Straight vs curly apostrophes: 8 files depart from the house form
**Track B · GROW + LAUNCH · LOW**

The estate uses the curly apostrophe `’` (242 instances across 47 files). Eight files use the
straight `'` (30 instances):

| file | n |
|---|---|
| `SCI_G_W7A_The_Moon_Explore.html` | 8 |
| `SCI_G_W7B_The_Moon_Do.html` | 8 |
| `SCI_G_W5B_Fair_Test_Do.html` | 4 |
| `SCI_L_W3L3_Magnification_Lab_Do.html` | 3 |
| `SCI_G_W6A_Earth_And_Planets_Explore.html` | 2 |
| `LAUNCH_SCIENCE_PRACTICALS_MATRIX.html` | 2 |
| `LAUNCH_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html` | 2 |
| `SCI_G_W6B_Earth_And_Planets_Do.html` | 1 |

**Not applied**, deliberately. Several instances sit in `data-label` attributes whose text
must stay byte-equal to the visible button text (e.g. `data-label="Earth's shadow on the
Moon"` in `SCI_G_W7B`); changing one side and not the other would break the pairing. Others
sit inside HTML comments. §5 protects answer-key `data-*`. A blanket replacement is unsafe;
a hand-picked one is cosmetic. Matt's call whether it is worth the risk.

---

## P5 — GROW print pack condenses the screen task (24 route/tier pairs)
**Track C · GROW · INFORMATIONAL — no answer changes**

24 of 105 tier/route pairs have print wording that is a condensed paraphrase of the screen
wording, e.g. `SCI_G_W5B` Standard:

- screen: "three repeats with units, a clear conclusion, base it on your results"
- print:  "three repeats with units, evidence-based conclusion"

All 24 express the same task and the same answer; none changes what a pupil must do.
Full table: `_sca1/tables/parity.csv` (81 OK, 24 condensed, 0 answer divergences).

**Not applied.** No defect: §4 requires parity of wording *and answer*; the answer is
identical throughout and the terser print form is a reasonable print-space decision. Listed
so the decision is visible rather than silently absorbed.

---

## P6 — Two WORD HELP bridges are defensible but slightly under-specified
**Track A · GROW + LAUNCH · LOW**

- `SCI_G_W3A` — `friction → "the rub that slows things down"`. Friction also *enables*
  (grip, braking), which is the lesson's own helpful/unhelpful framing. Proposed:
  "the rub between surfaces that resists sliding".
- `SCI_L_W5L1 / W5L2 / W7L1` — `osmosis → "water moving across a membrane towards the
  stronger solution"` omits *partially permeable*.

**Not applied.** Both are plain-language bridges whose job is access, and in both cases the
formal term stays dominant and correct on the same surface: `partially permeable` has its
own bridge in the same WORD HELP card and appears 9 / 5 / 4 times in those files, and the
board definition "net movement of water across a partially permeable membrane" is present.
Verdict MODEL-CAVEAT-OK; offered only if Matt wants maximum exactness in the gloss itself.

---

## P7 — BUILD W6A hint says "five identical sections"; the lesson's plate has four groups
**Track A · BUILD · LOW · sits on a §5-protected surface**

`SCI_B_W6A_Balanced_Plate_Explore.html`, hinge-question hint attribute, verbatim:

> `data-h="Balance is a pattern, not five identical sections or a ban list."`

The lesson's own plate model has **four** groups — `data-target` / `data-correct` both
resolve to exactly `dairy`, `fruitveg`, `protein`, `starchy` in W6A and W6B. A pupil who
has just sorted four groups is told balance is "not five identical sections".

"Five" is almost certainly a reference to the Eatwell Guide's five groups, so the sentence
is defensible as written — but it collides with the count the pupil is looking at.

Proposed: `data-h="Balance is a pattern, not equal-sized sections or a ban list."`
(drops the count entirely; the point is that balance ≠ equal portions, which is what the
sentence is actually for, and it stops contradicting the four-group model).

**Not applied.** `data-h` is an encoded answer-key attribute, protected by §5 and editable
"only when Track A proves an answer WRONG". The answer here is correct — the hint is merely
imprecise — so the exception does not apply and editing it would fail G4.

---

## Checked and cleared (no defect found) — recorded so the check is visible

- **Answer keys, all 35 hinge questions** — every encoded answer is scientifically correct.
  BUILD 10 + LAUNCH 15 via `data-correct`/`data-c`, GROW 10 via `data-correct` index.
  Table: `_sca1/tables/answer_keys.csv`. (Their *position* is P1.)
- **Sort/match cards** — every card resolves to exactly one existing target zone; no card
  points at a zone that does not exist (BUILD 24 cards / 3 zone sets).
- **LAUNCH lab maths** — magnification `40 ÷ 0.10 = ×400`, `20 ÷ 400 = 0.05 mm = 50 µm`,
  `30 ÷ 0.15 = ×200`, `50 mm ÷ 50 µm = ×1000` after unit match, "magnification has no unit",
  percentage change `((final − initial)/initial)×100` "divide by INITIAL" — all correct.
- **Seeded osmosis data actually yields the lesson's conclusion** — the seeded rule
  `expected = 15 − 31c` was executed; mean % change crosses zero at **0.506 mol dm⁻³**
  (anomaly excluded), so the lesson's "Near 0.5" is what the data gives. The flagged
  repeat at 0.6 (+4.19 % against −2.57/−2.26) is a genuine outlier for the anomaly task.
- **Board definitions** — osmosis keeps "partially permeable" (present 9/5/1/4/2/6/4 times
  across W5L1–W7L3); active transport carries both "against the gradient" and "using energy".
- **"SCIENCE GLITCH" cards are distractors by design** — "Osmosis is just diffusion…",
  "Active transport is free…", "50 mm ÷ 50 µm = ×1" are each labelled SCIENCE GLITCH with
  Keep-the-claim / Repair-it buttons and a correct repair text. Not defects.
- **Phases ≠ eclipses** — GROW W7 handles this correctly, including the orbital tilt as the
  reason eclipses are not monthly, and hedges the period as "roughly a month".
- **SoW alignment** — 15/15 weeks ALIGNED, 0 keywords absent. `_sca1/tables/sow_alignment.csv`.
- **Cross-pathway bleed** — none. The single hit (BUILD W4A "a cardboard lever") describes
  the model arm, which is a lever; it is not GROW mechanism content leaking into BUILD.
- **LAUNCH RED** — 0 mark allocations, AO codes, band descriptors or grade boundaries on any
  pupil or print surface. The only two matches are the disclaimer saying none appear.
- **Witness statements** — see P0 (raised, then withdrawn on the bytes).
