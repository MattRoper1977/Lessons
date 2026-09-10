# LW1 — LAUNCH return week: §0, §B, §C, §D

Order LW1, 2026-09-10. Third pathway in the session. Everything below is measured
today against the pack and `origin/main`; nothing is carried from RW1 or GW1.

---

## §0 — input and shape

### §0.1 The pack verifies

**60 files.** `SHA256SUMS.txt` lists **59** and all 59 verify **OK**. The one file
not covered is `SHA256SUMS.txt` itself, which cannot list its own digest — so the
honest reading is **59 of 60 checked, and the 60th is the manifest**, not "60
verified".

### §0.2 The live directory, derived rather than assumed

Every `SCI_L_*` route on `origin/main` was listed and grouped by directory. The
W8 routes live in `Science_Teesside/Launch/W8-W13_2026-27/` (20 files). All three
named routes **exist live**:

| route | live bytes | verdict |
|---|---|---|
| `SCI_L_W8L1_Enzyme_Action_Introduce.html` | 120,115 | **REPLACE** |
| `SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html` | 120,709 | **REPLACE** |
| `SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html` | 119,246 | **REPLACE** |

**No ADD, so no admission path.** §G's first stop condition does not fire.

### §0.3 Timers, per lesson, not normalised to each other

| lesson | stages | values | independent work | sum |
|---|---|---|---|---|
| L1 | 9 | 0 · 4 · 4 · 5 · 5 · 4 · 4 · **10** · 4 | 10 | **40.0** |
| L2 | 9 | 0 · 3 · 4 · 4 · 4 · 4 · 5 · **12** · 4 | 12 | **40.0** |
| L3 | 9 | 0 · 3 · 3 · 4 · 4 · 3 · 4 · **15** · 4 | 15 | **40.0** |

The 10 / 12 / 15 split the order describes is stage 8 in each file, and the other
eight stages absorb the difference. All three sum to exactly 40 **separately**.

---

## §B — core practical evidence integrity

### §B1 / §B3 — the labelling is already there, and it is honest

The pack labels the supplied dataset in pupil-facing text, repeatedly and without
hedging:

> **"Supplied illustrative observations — not your practical results."**
> *Single runs; equal starting amounts and the same iodine endpoint.*

and on the graph:

> *"Five illustrative single runs, not mean rates. Points show what was sampled;
> do not claim an exact optimum between them."*

and in the staff route-choice block, in **all three** files:

> *"The supplied-observation route needs no reagents and teaches the same
> interpretation; **it does not certify physical practical completion**. Do not
> infer concentrations, heating arrangements or disposal from lesson cards."*

with L2 carrying the stronger form:

> *"…the complete supplied-data route supports the same interpretation goals but
> **cannot establish practical completion**."*

**Verdict: no instance found where the illustrative dataset is allowed to stand
in for practical completion.** The pack anticipated this and said so first. The
one thing §B2 still requires is that the same sentence reaches **both marking
cards**, which are generated rather than shipped — that is a build task, not a
correction.

### §B4 — W8L1 is planning only, confirmed structurally

W8L1 mentions iodine 53 times, which a word count would flag. The structure says
otherwise. The method text sits inside

```html
<ol class="sequence-list"> … <button aria-label="Move A · Sample at a fixed
interval into separate iodine drops. up">↑</button> …
```

and the framing instruction is **"Order the six method cards and explain why
iodine tests separate sampled drops."** The task is **ordering**, not doing.

Corroborating: **0** occurrences in W8L1 of *goggles*, *apron*, *pipette*,
*water bath*, *pour*, *wear*, *hazard*, or *amylase solution*. There is no pupil
equipment list and no pupil risk assessment.

**One nuance worth stating rather than glossing.** The cards are written in the
imperative — *"Mix enzyme with starch and start timing as directed"* — which
reads as an instruction to act if it is lifted out of the ordering widget, for
instance printed alone. The pack already guards this in staff text: *"Do not
infer concentrations, heating arrangements or disposal from lesson cards."*
**§B4 passes**, with that guard named as the reason rather than assumed.

---

## §C — spec and sources

### §C1 — openstax, gated by DOM ancestry rather than by proximity

One citation per file, identical:
`https://openstax.org/books/biology-2e/pages/6-5-enzymes`

| | L1 | L2 | L3 |
|---|---|---|---|
| element | `<a href>` | `<a href>` | `<a href>` |
| resource load | **no** | **no** | **no** |
| ancestry | `a < p < div.v4-modal < dialog.classic-dialog[data-mbm-guide=staff]` | same | same |
| staff-gated | **yes**, by `dialog.classic-dialog teacher-only` | yes | yes |

Proximity would have been misleading here: the nearest preceding `teacher-only`
string is **6,917 characters** back in the source. Only the ancestry chain shows
the link is inside the staff dialog. Same treatment as nhs.uk and NASA:
**staff-gated href, no resource load, kept.**

### §C3 — no spec code in pupil text, recorded as a decision

The pack carries **0** occurrences of `1BI0`, `1SC0` or `IGCSE`. The **live**
files carry `1BI0` twice each. Nothing is added; the omission is recorded here so
it is a decision and not an oversight — and the live occurrences are noted
because a replacement drops them, which is a §D question and not a §C one.

---

## §D — the LF1 strings

### §D2 — per route: carried, superseded, or lost

Measured by taking the LF1 commit `4510b29a` ("LF1 D: restore 121 week
references, drop the 9 twins that restores make redundant"), diffing the visible
text nodes **before and after it** for each route, and checking each added node
against the replacement.

| route | touched by LF1 | text nodes added | denominator | verdict |
|---|---|---|---|---|
| **L1** | yes | **2** | 521 nodes before, 521 after | **DELIBERATELY SUPERSEDED** |
| **L2** | no | **0** | 517 / 517 — LF1 changed no visible text | **N/A, nothing to carry** |
| **L3** | yes | **5** | 534 / 534 | **DELIBERATELY SUPERSEDED** |

**L1.** LF1 added, twice:

> *"W7 review: enzymes are biological catalysts, but enzyme action was not
> securely taught in the installed W6–W7 sequence; today's retrieval box supplies
> the prerequisite facts."*

The replacement has no retrieval box at all (`retrieval` 0). It teaches the same
prerequisites as the lesson's **own opening content** — *"Starting fact: an
enzyme is a biological catalyst"*, with `biological catalyst` ×9, `active site`
×46, `substrate` ×83, `denatur` ×20 — and states the return-week position
outright: *"New arrivals have no prior evidence; that is not a deficit. Everyone
meets the same lesson from the same page."*

**That is the LF1 correction's purpose satisfied in a stronger form.** LF1 made
the lesson stop assuming W6–W7 taught enzyme action; the replacement stops
assuming anything was taught at all. Superseded, not lost.

**L3.** LF1 added five nodes — four command-word lines and one "Last lesson"
concatenation. Each checked separately against the replacement:

| LF1 claim | in the replacement | evidence |
|---|---|---|
| CALCULATE requires working | **carried** | "show the working" ×9, "show the equation, substitution and unit" ×3, "Show relative-rate working using 1 ÷ time with the unit s⁻¹" as a success criterion |
| EVALUATE requires evidence | **carried** | "EVALUATE means judge the evidence" ×3 |
| EVALUATE requires strengths/limitations | **carried** | "Which asks for a strength and a limitation?" ×3, `limitation` ×24 |
| EVALUATE requires a supported judgement | **carried** | "supported judgement" ×2, `judgement` ×10 |
| distinguish DESCRIBE from EVALUATE | **carried** | "DESCRIBE means state the pattern. EVALUATE means judge the evidence." ×3 |

**The `W7` token itself is gone — 0 occurrences — and that is required, not lost.**
The relabeller's public-token gate forbids `\bW(eek)?\s?\d+\b` on a pupil surface,
so carrying "W7" forward would ship a violation. The pedagogy is carried; the
week label is superseded by a later ruling.

**§G's "an LF1-corrected string would be lost" stop condition does not fire.**
Every one of the seven added nodes is either carried in substance or superseded
by a rule that post-dates it, and none is silently dropped.
