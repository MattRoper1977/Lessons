# FINDING — the relabeller refuses or crashes on 209 of 290 served Science pages

Raised at the close of R6, measured on Lessons main `1c5c527f`. **This needs a
ruling. It is not a handover note and it should not be filed as one.**

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

## 5. Rulings wanted

1. ~~**The crash**~~ — ruled: fix now. Done in **#473**.
2. ~~**The unclaimed files**~~ — ruled: manifest coverage, report only. Done in
   §4a. **Two follow-ups fall out of it and are not started:** the 25 decks in
   folders with no manifest, and the 10 `Grow/v3_40min` entries missing a `week`.
3. **The rule** — drafted in §4b with one amendment argued for. **Not applied.**
   Your word on the amendment and on the rule as a whole.
4. **New, from §4a:** four served pages have no inbound link anywhere in the
   estate. Separate from labelling; wants its own ruling.

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

## 7. State of the estate SX3 starts from

- **LF1 is closed.** 121 restorations across 22 files and 9 redundant staff twins
  removed (#468), published and confirmed live 2026-09-09 19:50 BST. Repo-wide on
  the deployed SHA `1c5c527f`: 0 defect, 3 authored instances retained.
- **#460–#464** are re-cut with the relabel dropped and hold for the Thursday
  window. 38 files partition cleanly; pins split 5 / 0 / 5 / 8 / 7.
- **Site `fac26001`** carries the Autumn 1 admission rows, proved on unchanged
  bytes (0 problems) and on the candidate (0).
- `tools/relabel_public.py` is the single writer for the public-relabel rule and
  refuses by default. Do not add a mode that guesses.
