# OBSERVATION RECORD — display-artefact audit of the 24 live Humanities decks

**This is an observation, not a description of the estate.** It records what one sweep, with one
stated inclusion rule, found on one day at one commit. It is not a survey, not a defect list, and
not an instruction. **Re-derive any figure here before relying on it** — every number below is
reproducible from the rule and the tree, and none of it should be quoted from this file into a
decision without being re-run.

**Derived at `df18729`, 2026-08-05. Read-only: the 24 decks changed by zero bytes.**
**Nothing here is a repair, a proposed diff, or a recommendation to any deck.**

---

## 1 · The inclusion rule, stated before the results

The standing remedy after three instances of an instrument's assumption becoming invisible in its
output: **a scan reports what it looked for, not only what it found.**

```
A candidate is a rendered BODY text run satisfying BOTH:

(A) FIRST PERSON, any voice — pupil's or adult's:
      whole-word  I | me | my | mine | we | us | our | ours   (case-insensitive)

(B) FILL-IN AFFORDANCE, one or more of:
      b1  ellipsis: the character U+2026, or three dots
      b2  blank marker: two or more consecutive underscores
      b3  an adjacent ruled writing line (following element with border-bottom,
          or a fixed height >= 30px)
      b4  an adjacent empty table cell  <td></td>
      b5  NO terminal punctuation at the end of the run (>= 3 words)

SCOPE: the 24 files matching {Build,Grow,Launch}/Slideshows/*_HUM_*.html
<style> and <script> stripped, so class names and JS identifiers cannot manufacture hits.
```

### Two assumptions inspected rather than asserted

**The b5 trade.** Clause b5 is what caught the member missed twice before, and it is also the
noisiest. In deck HTML it fires overwhelmingly on **success criteria** (*"I can place local events
on a timeline"*) and **slide headings** (*"I Do: Show vs Infer"*, *"We Do: Match the Source →
…"*). Those are learning objectives and section labels — **not templates, nobody fills them in**.
Of 404 total matches, **361 are b5-only and essentially all are this class**. The trade is real and
it runs the opposite way to the error it was introduced to fix: widening bought one true member
last time and buys mostly noise here. **A match qualifies on the reading, never on the regex.**

**The stripping assumption.** Stripping `<script>` would hide any template held as JS data — the
exact failure mode of searching text for something the runtime builds. A second pass therefore
searched inside the stripped script blocks for the same first-person-plus-affordance shape.
**Result: zero.** The assumption is checked, not asserted. The templates live in body HTML, mostly
inside `print-section` blocks.

---

## 2 · Results

**404 matches · 43 carrying a real (b1–b4) affordance · 361 b5-only · 0 script-residue.**

| verdict | count | files |
|---|--:|---|
| **MEMBER** — carries at least one first-person fill-in template | **19** | BUILD W1–W8 (all 8) · GROW W1, W2, W4, W6, W7, W8 · LAUNCH W1, W2, W5, W6, W8 |
| **NOT A MEMBER** — no run carries a b1–b4 affordance | **5** | GROW W3 · GROW W5 · LAUNCH W3 · LAUNCH W4 · **LAUNCH W7 (assessed)** |

Per-file counts of real-affordance templates: BUILD W1 4 · W2 4 · W3 1 · W4 2 · W5 4 · W6 2 · W7 5
· W8 3 — GROW W1 1 · W2 2 · W3 0 · W4 2 · W5 0 · W6 2 · **W7 1 (assessed)** · W8 2 — LAUNCH W1 1 ·
W2 1 · W3 0 · W4 0 · W5 1 · W6 2 · W7 0 · W8 3.

Nearly every one sits in a **`print-section`** — the printed scaffold sheet, not the projected
slide. Representative, quoted verbatim:

- BUILD W1 — *"The oldest event is…" | "\_\_\_ comes before \_\_\_ because…" | "My clue is…"*
- BUILD W5 — *1) My test card: \_\_\_\_\_\_\_\_\_\_\_\_\_\_*
- GROW W6 — *"I will argue that…" | "My first point is… my evidence is…" | "Some might say… but…"*
- LAUNCH W8 — *GRID station — my six-figure ref: \_\_\_\_\_\_*

---

## 3 · The one template the decks themselves say is displayed

Only one file states that pupil output leaves the pupil's own page. `BUILD_HUM_W2`, twice (slide
and print mirror):

> *"Your best 'suggests… because…' lines get read to the other class as our detective standard."*

This is the only **explicitly display-bound** template found. It also sits directly beside the
already-recorded observation that the assessed decks use best/top-answers framing, and it is a
**BUILD** deck, so the same shape reaches the youngest pathway. **Recorded, not judged** — whether
a best-lines standard read to another class is right for this cohort is a teaching judgement.

Everything else is a scaffold a pupil fills on their own sheet, with no statement that it is shown
to anyone. **That distinction is the substance of §5 below.**

---

## 4 · The because-rule, tested per clause

The rule under test — *a limit or refusal line never stands without its because* — was checked
**clause by clause, not per run**, because a run can satisfy the rule overall while a clause inside
it does not. That is precisely the error corrected in the influence guide, so it is not repeated
here.

**8 limit-bearing clauses. 3 carry their own because. 5 do not.**

| clause | file | own because |
|---|---|:--:|
| *"It withholds \_\_\_ **because** it was made to \_\_\_"* | GROW W2 | ✅ |
| *"**Because** it was made to \_\_\_, I expect it to show \_\_\_ and hide \_\_\_."* | GROW W2 | ✅ |
| *"The map cannot settle \_\_\_ **because** \_\_\_"* | LAUNCH W8 | ✅ |
| *"It cannot tell us…"* | BUILD W2 | ❌ |
| *"cannot tell us…"* (method chain) | BUILD W2 | ❌ |
| *"We can't be sure, but the source suggests…"* | BUILD W7 | ❌ |
| *"The map adds \_\_\_ that the sources couldn't show"* | BUILD W8 | ❌ |
| *"But it hides \_\_\_ — for that we need \_\_\_"* | BUILD W8 | ❌ |

**Two patterns are visible, and they are not the same defect.**

*"We can't be sure, but the source suggests…"* and *"But it hides \_\_\_ — for that we need \_\_\_"*
are **limit-plus-redirect**: they say what to do instead and never why. That is the exact shape
repaired in the influence guide.

*"It cannot tell us…"* is **a bare limit** — but it is a limit **about a source**, not a refusal
addressed to a person, and §5 argues that difference matters.

**The progression is inconsistent, and that is worth someone's attention.** GROW scaffolds the same
move *with* a because; BUILD scaffolds it *without*. That is either a tiering decision — a BUILD
pupil is not yet asked to justify a limit — or an oversight. **This pass does not decide which.**

---

## 5 · The finding that says the property may need a third revision

**The because-rule was written for a refusal directed at a person.** Its home case is an adult
telling a pupil what could not be done with their idea, where a reason-free "no" is a social act
that lands on a child.

**Most of what this sweep found is a different object**: a pupil stating the limits of *evidence*.
*"It cannot tell us who took this photograph"* is not a refusal — it is **correct historical
reasoning**, and it is the disciplinary skill the lesson exists to teach. Requiring a because on
every such clause could push a pupil towards inventing a reason for a limit that is simply
intrinsic to the source.

**So the property, applied mechanically here, over-reaches.** Two distinctions it does not yet
draw:

1. **refusal to a person** vs **limit of evidence** — the because-rule is right for the first and
   arguable for the second;
2. **filled and displayed** vs **filled and kept** — the property says *intended for display*, and
   exactly **one** of the 19 members states that its output is shown to anyone. On a strict reading
   the other 18 are private scaffolds and not display artefacts at all; on a loose reading every
   fill-in template is a member, which makes the term mean very little.

**This is the honest position, and the verdict is not forced:** the 19 are members **by shape**,
one is a member **by its own statement**, and the property cannot presently separate them. A third
revision would draw both distinctions. **That is a design question for whoever owns the property —
it is not patched here, and no deck was touched.**

---

## 6 · Matrix reconciliation, three ways

Against `Humanities_Teesside/Lundy_Humanities/data/lesson_implementation_matrix.csv`,
`current_ticket` column:

| | count |
|---|--:|
| documented-and-found | **4** (BUILD W1–W4) |
| **DOCUMENTED-NOT-FOUND** | **0** |
| found-not-documented | **15** |
| neither | **5** |

**Zero documented-not-found is the important cell.** A documented template the sweep could not find
would have been a finding about the sweep before the deck, and would have required a second
derivation route. None arose, so no second route was needed.

**The 15 found-not-documented are a finding about the matrix, not the decks.** Only BUILD W1–W4
phrase their `current_ticket` in the first person; the remaining 20 rows describe the same tickets
impersonally (*"Chronology claim; because; what would increase certainty; challenge"*). The
templates are in the decks either way. **The matrix under-documents the voice, and anyone using
that column to find first-person material would have found four files and missed fifteen.**

---

## 7 · Where each finding went

| finding | routed to | as |
|---|---|---|
| the 19 members among the 22 non-assessed decks | open-item **39**, the Estate Visuals inheritance | a **specification**, not a patch |
| `GROW_HUM_W7` — 1 member template, assessed | this record only | quoted and located, for Matt's pedagogy ruling |
| `LAUNCH_HUM_W7` — NOT A MEMBER, assessed | this record only | recorded as clean |
| BUILD W2's display-bound best-lines standard | this record only | quoted, beside the existing best/top-answers question |
| the property's two undrawn distinctions | the register method entry | a stated limit of the instrument |

**Nothing was repaired. No proposed diff was minted.** One parked proposed diff already exists
against the assessed pair; a second would be a rival.
