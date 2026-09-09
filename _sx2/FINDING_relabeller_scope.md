# FINDING — the relabeller refuses or crashes on 209 of 290 served Science pages

Raised at the close of R6, measured on Lessons main `1c5c527f`. **This needs a
ruling. It is not a handover note and it should not be filed as one.**

---

## 1. The measurement

Every `Science_Teesside` HTML file, run through `tools/relabel_public.py` as it
stands after #466. "Served" means the path is in the Site all-file admission
registry — a page a pupil can open today.

| | files | of those, served |
|---|---:|---:|
| no pupil-facing calendar token at all | 54 | 54 |
| the tool would **rewrite** | **27** | 27 |
| the tool **refuses** | **162** | **111** |
| the tool **crashes** | **47** | **47** |
| **total** | **290** | 239 |

Two separate problems live in that table, and they need different answers.

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

The fix is small. It is not made here, because it changes a tool that now
refuses by design and it wants its own red-proof: a fixture per manifest shape,
the crash proved before and the refusal-or-rewrite proved after.

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

## 5. Rulings wanted

1. **The crash** — fix now in its own PR with a red-proof per manifest shape, or
   leave it for SX3 to hit?
2. **The 83 unclaimed files** — are they meant to be in a manifest? If so this is
   a manifest-coverage finding, not a labelling one, and it wants its own census.
3. **The remaining refusals** — a decision each is a lot of decisions. Is there a
   rule you want applied (leave the week number; name the unit in prose; something
   else), or does each one come to you?

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
