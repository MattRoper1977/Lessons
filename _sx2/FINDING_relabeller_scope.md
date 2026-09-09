# FINDING — the relabeller resolves 27 of 290 served Science pages, and that is correct

Raised at the close of R6, measured on Lessons main `1c5c527f`. Its central
ruling arrived as **R-CAL-1** (D20) and the amendment as **D19**; §4c–§4g are the
work LF1-I ordered on the back of them, and §5 lists what is still open. **Five
of those are still questions for Matt and three of them gate SX3 — see §6a.**

---

## 1. The measurement

Every `Science_Teesside` HTML file, run through `tools/relabel_public.py` as it
stands after #466. "Served" means the path is in the Site all-file admission
registry — a page a pupil can open today.

| | on main today | after #473 | served |
|---|---:|---:|---:|
| no pupil-facing calendar token at all | 54 | 54 | 54 |
| the tool would **rewrite** | 27 | **58** | 58 |
| the tool **refuses** | 162 | **178** | 127 |
| the tool **crashes** | **47** | **0** | — |
| **total** | 290 | 290 | |

Two separate problems lived in the first column and they needed different
answers. The crash is fixed in #473; these numbers are restated rather than left
at the figures I first reported, because #473 moves 31 of the 47 into the
rewritable column and the scope claim has to be made on the corrected count.

---

## 2. The crash — 47 served pages, every one of them

```
AttributeError: 'list' object has no attribute 'get'
  tools/relabel_public.py:94 in sequence
    m = json.load(open(mf, encoding='utf-8'))
    L = m.get('lessons') or m.get('sequence') or []
```

`sequence()` assumes a manifest is a JSON object. Three are top-level arrays:

- `Science_Teesside/Build/v3_40min/manifest-v3.json` — 14 files
- `Science_Teesside/Grow/v3_40min/manifest-v3.json` — 14 files
- `Science_Teesside/Launch/v3_40min/manifest-v3.json` — 19 files

Reproducing file: `Science_Teesside/Build/v3_40min/BUILD_SCIENCE_PRACTICALS_MATRIX.html`.

**All 47 are served.** The tool does not refuse them — it dies, which is a
different and worse failure: a refusal names the problem and leaves the file
alone, a crash aborts the run at whatever file it reached.

This predates #466 (that PR did not touch the manifest reader) and **#466's 25
self-tests do not cover it** — a gap in my testing, and one a fixture with an
array-shaped manifest would have caught.

**Fixed in #473**, per your ruling: handled rather than refused, because the
array entries carry the same per-entry fields the object form does (`file`,
`week`, `id`) — a third envelope for the same data, not a different schema. An
unrecognised shape now returns no entries and refuses, rather than raising.
Red-proved across all 290 files: crashes **47 → 0**, the 47 reclassifying as 31
rewritable and 16 refusing, with the other 243 untouched in every bucket.
`--self-test` 25 → 36 checks, covering flat, sibling-week and array.

---

## 3. The refusals — 111 served pages, and mostly correct

162 files refuse, 111 of them served. The reasons, by count:

| files | reason |
|---:|---|
| 83 | the file has no manifest entry, so it has no sequence to be relative to |
| 23 | outside this unit's manifest weeks 8–13 |
| 21 | outside this unit's manifest weeks 18–26 |
| 14 | outside this unit's manifest weeks 27–34 |
| 10 | outside this unit's manifest weeks 17–26 |
| … | the remainder, other unit ranges |

**Most of these refusals are the tool working.** A file the manifest never
claimed has no "Lesson n of N" to become; a cross-unit reference — a recap naming
an earlier week, a forward pointer to the next half-term — has no sequence-relative
form that is true. Inventing one is exactly what put 121 wrong labels on 22 live
pages, and what LF1 spent a day removing.

But the scale is the finding. **Seven of every eight Science pages carrying a
calendar token cannot be re-tokenised by tool.** Any plan that assumes a
relabelling pass over the remaining batch is wrong by roughly that factor.

---

## 4. What this changes

**SX3 cannot be a relabelling pass.** Its first act has to be a scoping census
per file — does the manifest claim it, and does every token it carries fall
inside that unit's weeks — because only the 27 can be done automatically. The
other 209 need a decision each, or a manifest that claims them.

The 83 with no manifest entry are the interesting subset: they may be a
*manifest* problem rather than a labelling one. If those files should be claimed
by a manifest and are not, fixing that turns some of them into the 27.

---

## 4a. §3.2 REPORT — the files no manifest claims

Report only, no fix, as ruled. Measured with #473's tool, so the array-shaped
folders are included rather than crashed past. **97 files**, all 97 served.

**35 are lesson decks — these are the real orphans.**

| directory | unclaimed decks | manifest in the folder |
|---|---:|---|
| `Science_Teesside/Launch` | 15 | **none** |
| `Science_Teesside/Grow/v3_40min` | 10 | yes, but their entries carry no `week` |
| `Science_Teesside/Build` | 5 | **none** |
| `Science_Teesside/Grow` | 5 | **none** |

Two different causes. **25 sit in folders with no manifest at all** — `Launch` 15,
`Build` 5, `Grow` 5 — so nothing claims them and nothing could. **10 are listed by
`Grow/v3_40min/manifest-v3.json` but their entries carry no `week` field**, which
its Build and Launch siblings do carry. That one is a data gap in a single
manifest, not an absent manifest, and it is the cheaper of the two to close.

**62 are not lesson decks and are correctly outside any sequence:**

| directory | files |
|---|---:|
| `Science_Teesside/Grow/resources` | 10 |
| `Science_Teesside/Teaching_Packs/BUILD/HTML` | 10 |
| `Science_Teesside/Teaching_Packs/BUILD/Resources` | 10 |
| `Science_Teesside/Teaching_Packs/GROW/HTML` | 10 |
| `Science_Teesside/Teaching_Packs/GROW/Resources` | 10 |
| `Science_Teesside/Grow/v3_40min` | 4 |
| `Science_Teesside/Teaching_Packs/BUILD` | 2 |
| `Science_Teesside/Teaching_Packs/GROW` | 2 |
| `Science_Teesside/Teaching_Packs` | 2 |
| `Science_Teesside/Launch/resources` | 1 |
| `Science_Teesside` | 1 |

Companion worksheets (`Grow/resources/GS_W*`), the pack copies under
`Teaching_Packs/*/HTML` and `*/Resources`, three index pages, two practicals
matrices, a teacher guide and two pupil-resources pages. None of these is a
lesson in a taught order, so no manifest should list them and their refusal is
the tool being right.

**Navigation reach.** 93 of the 97 are linked from somewhere — 81 from an index
page, 74 from another lesson. **Four have no inbound link anywhere in the estate:**

- `Science_Teesside/Grow/v3_40min/index.html` — an index nothing points at
- `Science_Teesside/Grow/v3_40min/GROW_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html`
- `Science_Teesside/Teaching_Packs/BUILD/Pupil_Resources.html`
- `Science_Teesside/Teaching_Packs/GROW/Pupil_Resources.html`

All four are served and admitted. A page a pupil can reach only by typing its URL
is a separate question from labelling, and it is not answered here.

## 4b. §3.3 DRAFT RULE — for Matt's word, not applied

Your starting position, with the data I have:

> A refusal on a genuine out-of-folder reference is correct and the file keeps its
> existing literal label. Re-tokenisation is only attempted where the referenced
> week is inside the folder's own sequence.

**The data supports it, and here is the sharpest reason.** The 121 wrong labels
LF1 removed were produced by exactly the case this rule excludes: a reference to a
week outside the folder's manifest range. Every one of them. The rule is not a
convenience — it is the boundary the defect crossed.

**One amendment I would argue for.** As written the rule is silent on the 10
`Grow/v3_40min` decks, whose manifest *does* list them but without a `week`. Those
are not out-of-folder references; they are in-folder references the manifest
cannot currently resolve. Adding the missing `week` fields would move them from
"refuse" to "rewrite" without any judgement about pupil-facing text. So:

> …**and** where a file is listed by its folder's manifest but the entry carries
> no week, that is a manifest defect to fix, not a labelling decision to make.

**What the rule leaves.** With #473 merged, 58 of 290 Science pages are
re-tokenisable by tool. Closing the `Grow/v3_40min` week gap would add up to 10
more. The remaining ~178 keep their literal labels, and that is the answer, not a
backlog: **seven in eight Science pages being un-re-tokenisable is a finding about
the tool's scope, not work to grind through by hand.** Any plan that treats it as
a queue is planning to repeat LF1 at scale.

## 4c. R-CAL-1 MEASURED — §1.3, dry, nothing written

`tools/relabel_public.py --measure` over all 290 `Science_Teesside` pages. The
run writes nothing, so the numbers can be read before a byte moves; `git status`
after it is clean.

| | files | worked example |
|---|---:|---|
| no pupil-facing calendar token | 54 | — |
| **RESOLVED** | **27** (80 labels) | `Build/v3_40min/SCI_B_W3A_Backbones_Explore.html` — *"…BUILD Science · Week 3 (40-min route · Explore)"* → *"…BUILD Science · Lesson 1 of 10 (40-min route · Explore)"* |
| **F1** week outside the folder sequence | 68 | `Build/W18-W26/SCI_B_W18_Soil_What_Is_In_The_Mix.html`, token W1, weeks 18–26 — *"W1. Sort A, B and C. Give one evidence clue."* (a numbered question, not a week) |
| **F2** no manifest claims the file | 109 | 83 folder has no manifest: `Build/SCI_B_W3_Backbones.html`, token W3. 26 the manifest lists other files: `Build/W8-W13_2026-27/PRACTICALS_MATRIX.html`, token W13 |
| **F3** entry carries no week (D19) | 13 | `Grow/v3_40min/SCI_G_W3A_Friction_Explore.html` — listed, no `week` field |
| **F4** manifest shape unrecognised | **0** | none in the estate; the fixture is `--self-test`'s bare-string manifest, which refuses without raising |
| **F5** ambiguous, or matches no lesson | 15 | `Build/v3_40min/SCI_B_W4A_Muscles_Explore.html`, token W3 — *"3 · Week 3 again:"*, and two manifest lessons claim week 3 |
| **CRASHED** | **0** | — |
| UNSEEN — see below | 4 | |
| **total** | **290** | |

**§1.4 reconciliation with the 58 / 162 / 47 split.** The 47 crashes went to 0 in
#473 and are not in this table as a bucket. Of the 58 that #473 left rewritable,
**27 still resolve and 31 now refuse** — 15 F5, 12 F2, and 4 that were never
rewrites at all (below). The 178 that already refused did not move in or out;
R-CAL-1 only re-attributes them, 68 F1 / 97 F2 / 13 F3. Every file is accounted
for: 97+68+54+27+15+13+12+4 = 290.

R-CAL-1 therefore **halves the resolvable set, 54 files → 27.** That is the rule
working, not a loss: each of the 27 refusals it adds is a case where the old
implementation answered a question it could not actually answer.

### The three places the code was answering a question it could not answer

- **F2 is a file-level fact now.** Before, a file its folder's manifest did not
  list still resolved sibling weeks, because the folder had *a* sequence. But
  "Lesson 3" on a page that is not in the sequence is a claim about a sequence
  the page is not in. 26 files.
- **F5 exists.** Two manifest lessons claiming one week used to produce
  `Lessons 3–4`. 15 files.
- **The letter clamp is gone.** `min(k, len(ns) - 1)` turned `W7B` in a
  one-lesson week into lesson A. That is inference from file order (N2) wearing a
  resolution's clothes — the same class of guess as `the previous unit`.

### UNSEEN — four files in neither column, and why the report shows them

Four `START_HERE.html` pages carry **`Absolute week 14`** in visible text. The
census pattern is case-insensitive; the rewriter's week pattern is not. So the
gate counts a pupil-facing token the rewriter cannot see: not resolved, not
refused, and previously reported as "no change" — which reads like success.
`--measure` gives it its own bucket instead. The same asymmetry hides a bare
`W9B`: `\bW\d+\b` needs a word boundary after the digit, so a lesson-letter
reference standing alone is invisible to the gate too. **Neither is fixed here**
— widening what the rewriter matches changes what it will write, and that wants
a ruling.

### Two things only reading the output could find

1. **`'BUILD Weekly - Spring'!C29` was becoming `'the curriculum workbook`** —
   opening quote orphaned — and `!B41, C41` left `, C41` stranded. Ten rewrites
   went down that path. A count reports ten successes. **Fixed**, with the
   estate's 16 real cell strings as the fixtures.
2. **The sibling-week pathway fires zero times on this estate.** Of 80 rewrites:
   47 own-week, 20 `last week`→`last lesson`, 10 SoW cells, 2 term labels, 1
   academic year, **0 `Lesson k`**. The code that authored the 121 wrong labels
   is dead on this content — not by removal, by never resolving.

## 4d. §1.2 — R-CAL-1 against my own draft

**They agree on the core and on every case my draft covered.** My §4b draft said
re-tokenise only where the referenced week is inside the folder's own sequence;
R-CAL-1's R1 is the same rule with the manifest-entry condition made explicit,
and F1 is its refusal. My D19 amendment is R-CAL-1's F3.

**One real difference, and it is R-CAL-1 refusing where I would have resolved:
F5, 15 files.** My draft was silent on a week claimed by two manifest lessons, so
the existing `Lessons %d–%d` behaviour would have stood. I now think that was
wrong and R-CAL-1 is right, and the evidence is the sentences themselves:
`Build/v3_40min/SCI_B_W4A_Muscles_Explore.html` carries the retrieval badge
**"3 · Week 3 again:"**, which the old code turns into **"3 · Lessons 1–2
again:"**. That is not a translation of the reference — it asserts the pupil did
the thing across both lessons of that week when it was one of them, and it reads
worse than the literal it replaced. R-CAL-1's PRINCIPLE settles it: a correct
literal label is not a defect.

The one thing worth your word: if you ever want the whole-week case resolvable,
it needs its own rule (*"a reference to a week taught as several lessons resolves
to the range"*), not a loosening of F5. **My recommendation is to leave F5 as
ruled.** 15 files keep an accurate literal.

## 4e. §2 — the weekless entries. There are 13, not 10, and 10 of them resolve

My §4a said 10. That was `Grow/v3_40min` only. Measured with `entry_week()`
rather than the `week` key — `absoluteWeek` and `cells[].absoluteWeek` are also
read — the count is **13**, and the extra three are a different case entirely.

**The 10 `Grow/v3_40min` decks — all sourced, four ways in agreement.**

| entry | file | week | |
|---|---|---:|---|
| W3A | `SCI_G_W3A_Friction_Explore.html` | **3** | |
| W3B | `SCI_G_W3B_Friction_Do.html` | **3** | |
| W4A / W4B | `..._Mechanisms_Explore/Do.html` | **4** | |
| W5A / W5B | `..._Fair_Test_Explore/Do.html` | **5** | |
| W6A / W6B | `..._Earth_And_Planets_Explore/Do.html` | **6** | |
| W7A / W7B | `..._The_Moon_Explore/Do.html` | **7** | |

The sources, in order of authority:

1. **`_sownb/TERM_DATES.md`, the ruled mapping** — *"Aut1 Wn → n"*. This is the
   estate's own statement that a week is derived from a term-relative label and
   never from a filename (g27).
2. **The SoW spine.** `Planning/GROW/…Weekly_Plan_Week0N_*.xlsx` for weeks 3–7
   each name the deck by title — *"v5 whiteboard deck 'Friction: Friend and
   Enemy'"*, *"'Levers, Pulleys and Gears'"*, *"'Planning a Fair Test'"*,
   *"'Earth and the Planets'"*, *"'The Moon's Journey'"* — against
   **`Aut1·W3` … `Aut1·W7`**. The same rows carry *"Runs across BOTH weekly
   40-min periods"*, which is the authority for A and B sharing one week.
3. **Each file's own content.** Nine carry a print row `<strong>Lesson</strong>`
   reading e.g. *"Planning a Fair Test — GROW Science · Week 5 (40-min route ·
   Explore)"*. The tenth, `W3A`, has no such row but carries
   `const LESSON = {… "period": "Autumn 1 · Week 3 · Explore" …}` and the SoW
   cell `GROW Weekly - Autumn!B34, C34`.
4. **Corroboration, not a source.** In `Build/v3_40min` and `Launch/v3_40min` the
   digits in `id` equal `week` in **25 of 25** entries. Grow's ids give the same
   ten weeks. That agreement is a check on the three sources above; on its own it
   would be inference from a code, and would not be enough.

Nothing here is derived from a filename or from folder order. **Zero
unsourceable.**

**The other three are correctly null and must not be "repaired".**

`Build/W18-W26/…SX1-018`, `Grow/W18-W26/…SX1-014`,
`Launch/W17-W26/…SX1-031` — all three the last lesson of their unit, all three
`sow: "Spr2·W6 — …"`, all three citing row **C39** of their lane's *Weekly -
Spring* sheet. I read `'BUILD Weekly - Spring'!C39` in the workbook: HT·Wk
**Spr2·W6**, outcome matching the manifest verbatim.

`_sownb/TERM_DATES.md` then rules on it directly:

> Spring 2 has five timetabled weeks, so its sixth column is NOT-TIMETABLED.

And the mapping makes the collision plain: `Spr2 Wn → 21 + n` puts Spr2·W6 at
absolute 27, and `Sum1 Wn → 26 + n` already puts Sum1·W1 there. **There is no
absolute week to supply.** The `null` is the correct value, recorded by someone
who met the same conflict.

**This is an amendment to D19 that wants your word.** D19 calls F3 "a manifest
defect to repair". For these three it is not a defect and there is nothing to
repair; F3 is refusing correctly and permanently. Either D19 gains an exception
for a ruled NOT-TIMETABLED column, or those three pages need a different answer
to "what does a pupil read here" — but no `week` field will ever be right.

*(Confirmation the mapping is the live authority: every one of the 17 term-labels
that appear alongside an `absoluteWeek` in a Science manifest matches it exactly,
including `Sum2 Wn → 33 + n`, which is why absolute 33 is absent from the
estate, and `Aut2·W7 → 15`, which is why `Launch/Autumn2_W7_2026-27` resolves to
week 15.)*

## 4f. §3 — the 25 decks in folders with no manifest

**All 25 are class (b): the folder has no manifest at all.** None is class (a)
— no existing manifest omits them — and none is class (c). They are three
complete taught sequences:

| folder | decks | shape |
|---|---:|---|
| `Science_Teesside/Build` | 5 | `SCI_B_W3…W7`, one per week |
| `Science_Teesside/Grow` | 5 | `SCI_G_W3…W7`, one per week |
| `Science_Teesside/Launch` | 15 | `SCI_L_W3_L1…W7_L3`, three per week |

**All 25 carry a calendar token today and all 25 refuse under F2.** That is 25 of
25, not a subset — the whole set is the "unclaimed AND un-re-tokenisable"
combination you flagged.

**They are not orphans; they are the other route.** Weeks 3–7 exist twice: once
as one lesson per week in the parent folder, once split for 40-minute periods in
`v3_40min`. The GROW Weekly Plan for week 6 points at the parent file by path —
*"Science_Teesside/Grow/SCI_G_W6_Earth_And_Planets.html (3-tier print pack off
the title slide)"* — so the spine treats the parent deck as primary and
`v3_40min` as the derived route.

**What a manifest would have to say — not written.** For each of the three
folders, entries in taught order with `file` and `week`, weeks 3–7 from the same
ruled mapping used above (`Aut1 Wn → n`): Build and Grow one entry per week 3–7;
Launch three entries per week, `W3L1/W3L2/W3L3` … `W7L1/W7L2/W7L3`. **Writing
them would also create F5 on Launch** — three lessons claiming each week — so
adding these manifests moves Launch's 15 from F2 to F5 and resolves nothing
unless a whole-week rule exists. Build and Grow, one lesson per week, would
resolve.

That is the argument for taking §3 and F5 together rather than one at a time.

## 4g. §4 — the four served pages with no inbound link

Measured against the Site's own surfaces, with a control that passes: the sibling
deck `Grow/v3_40min/SCI_G_W3A_Friction_Explore.html` is in the source manifest
and in the built search index, so the instrument reads Science.

| page | inbound link | source manifest | search index | sitemap |
|---|---|---|---|---|
| `Grow/v3_40min/index.html` | none | **yes** — `sci-tees-g-v3-hub`, type `teacher`, *"GROW · Science 40-min route · start here"* | **yes** | no |
| `Grow/v3_40min/GROW_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html` | none | no | no | no |
| `Teaching_Packs/BUILD/Pupil_Resources.html` | none | no | no | no |
| `Teaching_Packs/GROW/Pupil_Resources.html` | none | no | no | no |

**One correction to §4a.** I called `Grow/v3_40min/index.html` "an index nothing
points at". No page links it, but it is a declared teacher hub and it **is**
reachable by search. It is not orphaned.

**The other three are.** No inbound link, absent from the source manifest,
absent from the search index. `sitemap.xml` proves nothing either way — it
carries only 4 Science URLs out of ~290 served, and `audience-sitemap.xml`
carries no Science at all, so their silence is not evidence.

Two of the three are pupil-facing by name (`Pupil_Resources.html`, one per
pack). **Handed to the catalogue/discoverability work and stopped here.** It is
not a labelling problem.

## 5. Rulings wanted

1. ~~**The crash**~~ — ruled: fix now. Done in **#473**.
2. ~~**The unclaimed files**~~ — ruled: manifest coverage, report only. Done in
   §4a, extended in §4e/§4f.
3. ~~**The rule**~~ — ruled as **R-CAL-1**, landed verbatim as **D20** and in the
   tool's docstring. The amendment is **D19**. Measured in §4c, compared against
   my draft in §4d.
4. ~~**The four unlinked pages**~~ — answered in §4g. One is reachable by search
   and is not orphaned; three are, and are handed to catalogue/discoverability.

**Still open, and SX3 is gated on two of them:**

- **A. The 10 `Grow/v3_40min` weeks (§4e).** Sourced and agreed four ways. They
  are a manifest data repair, not a labelling decision. Say go and they can be
  written; nothing else in §4e needs a decision.
- **B. D19 vs the three `Spr2·W6` entries (§4e).** Their `absoluteWeek: null` is
  correct — `_sownb/TERM_DATES.md` rules that column NOT-TIMETABLED, and the
  ruled mapping puts it on a week Sum1·W1 already holds. D19 as written calls F3
  "a defect to repair"; for these three there is nothing to repair. **Needs your
  word**, because it decides whether F3 is a queue or a permanent state.
- **C. The 25 no-manifest decks (§4f).** Class (b), all three folders, all 25
  carrying a token. Writing the manifests resolves Build and Grow but moves
  Launch's 15 from F2 to F5 unless a whole-week rule exists — **so §3 and F5
  should be decided together, not one at a time.**
- **D. F5 and the whole-week case (§4d).** My recommendation is to leave F5 as
  ruled and let 15 files keep an accurate literal. Recorded here so the option is
  visible rather than lost.
- **E. UNSEEN (§4c).** The census is case-insensitive and the rewriter is not, so
  `Absolute week 14` and a bare `W9B` are pupil-facing tokens nothing can act on.
  Widening the rewriter changes what it writes. Not touched.

---

## 6. What SX3 inherits regardless

**D11** — a changed admitted byte needs a registry move as much as a new path
does. Stage as a transition pair `[pre, post]`, prove the registry on unchanged
bytes first, then merge content. `tools/lf1/check_admission_move.py` checks it
before the merge.

**D12** — build a counterfactual to contradict you, not to pass. An invariant
reading the same before and after has proved nothing.

**D13** — a browser-rendered census is the standard for a pupil-visible claim.
Neither a source grep nor a tag-stripped fetch is a render.

**D14** — cover the deck driven through its real control, each gate pressed and
sampled individually, both chassis conventions, print as a separate subtree, and
accessible names. On LF1 the same phrase counted 8, 72, 83, 86 and 121 depending
on which was missed.

**D15** — one re-run of an install-time failure is a discriminating test; a
second identical one is an outage, waited out and never bypassed.

---

## 6a. SX3 GATES — restated, so nothing downstream assumes it is clear

The crash gate is **lifted** (#473: 47 → 0, red-proved across all 290, and 18 of
the tool's 54 self-test checks now cover manifest envelopes and reason codes).

**SX3 remains gated on all three of these:**

| gate | state |
|---|---|
| **R-CAL-1 landed** | **MET.** Verbatim in `_sx2/DECISIONS.md` D20 and in `tools/relabel_public.py`'s docstring. Enforced by F1–F5, `--measure`, and 54 self-test checks. |
| **The 10 weeks resolved** | **NOT MET.** Sourced four ways in §4e and ready to write; needs Matt's go. Until then those 10 refuse under F3. |
| **Matt's word on §3** | **NOT MET.** The 25 decks are classified in §4f; the ruling is open, and it interacts with F5 (item C above). |

**And R-CAL-1 has not been run on content.** §1.5 of LF1-I: the first real
application is SX3's, under its own order. Every number in §4c is a dry run.

**What SX3 should not assume.** That the remaining ~205 refusals are a backlog.
R-CAL-1's CONSEQUENCE ACCEPTED is explicit: most Science pages carrying a
calendar token will not be re-tokenised, and that is the correct outcome.
Resolving all three gates in Matt's favour moves at most 10 + 10 files, not 205.

---

## 7. State of the estate SX3 starts from

- **LF1 is closed.** 121 restorations across 22 files and 9 redundant staff twins
  removed (#468), published and confirmed live 2026-09-09 19:50 BST. Repo-wide on
  the deployed SHA `1c5c527f`: 0 defect, 3 authored instances retained.
- **#460–#464** are re-cut with the relabel dropped and hold for the Thursday
  window. 38 files partition cleanly; pins split 5 / 0 / 5 / 8 / 7.
- **Site `fac26001`** carries the Autumn 1 admission rows, proved on unchanged
  bytes (0 problems) and on the candidate (0).
- `tools/relabel_public.py` is the single writer for the public-relabel rule and
  refuses by default. Do not add a mode that guesses. Use `--measure` before
  `--apply`, always: it is the same code path, writes nothing, and prints the
  resulting text rather than a count.
- **Thursday 2026-09-10, after 15:30 BST** is the content-merge window. The
  14:00 UTC pre-flight check-in is armed and nothing in LF1-I touched it.
