# SX3 handover — the Remaining Science batch

Written at the close of R6, on Lessons main `2e910b8`. Everything below is
measured on that tree, not carried forward from an earlier order.

---

## 1. SX3's re-tokenisation is gated on #466, and #466 changes what is possible

#466 removed the two lines that let `tools/relabel_public.py` answer an
unresolvable week number with `the previous unit` / `the next unit`. It now
raises, names the token, the reason and the sentence, writes nothing, and exits 2.

That is not a small behavioural change for SX3. Measured across
`Science_Teesside` on this tree — 290 HTML files:

| | files |
|---|---|
| no pupil-facing calendar token at all | 54 |
| the fixed relabeller would **rewrite** | **27** |
| the fixed relabeller **refuses** | **209** |

**SX3 cannot be a relabelling pass.** Seven of every eight Science pages carrying
a calendar token now stop the tool. Why they stop:

| refusals | reason |
|---|---|
| 83 | the file has no manifest entry, so it has no sequence to be relative to |
| 47 | *a crash, not a refusal* — see §2 |
| 23 | outside this unit's manifest weeks 8–13 |
| 21 | outside this unit's manifest weeks 18–26 |
| 14 | outside this unit's manifest weeks 27–34 |
| 10 | outside this unit's manifest weeks 17–26 |
| … | the remainder, other unit ranges |

The 83 with no manifest entry are the honest core of it: a file the manifest does
not claim has no "Lesson n of N" to be rewritten into, and inventing one is the
class of error LF1 spent a day removing from the live estate. The rest are
cross-unit references — a recap naming an earlier week, or a forward reference to
the next half-term — where the right answer is a human's, not a tool's.

**So SX3's first act is a scoping census, not a run.** For every file in its
batch: does the manifest claim it, and does every calendar token it carries fall
inside that unit's weeks? Only the files where both are true can be
re-tokenised automatically. The rest need a decision each.

---

## 2. A blocker SX3 will hit immediately: three array-shaped manifests

`sequence()` assumes a manifest is an object:

```python
m = json.load(open(mf, encoding='utf-8'))
L = m.get('lessons') or m.get('sequence') or []
```

Three Science manifests are a top-level **array**, so `.get` raises:

```
AttributeError: 'list' object has no attribute 'get'
  tools/relabel_public.py:94 in sequence
  reproducing file: Science_Teesside/Build/v3_40min/BUILD_SCIENCE_PRACTICALS_MATRIX.html
```

- `Science_Teesside/Build/v3_40min/manifest-v3.json`
- `Science_Teesside/Grow/v3_40min/manifest-v3.json`
- `Science_Teesside/Launch/v3_40min/manifest-v3.json`

**47 files** sit in those three folders and crash rather than refuse. This
predates #466 — that PR did not touch the manifest reader — and #466's 25
self-tests do not cover it, which is a gap in my testing, not a regression.

The fix is small (accept a list as the lesson array) but it is a behaviour change
to a tool that now refuses by design, so it wants its own red-proof and its own
PR rather than riding on SX3's first content change. **It is not fixed here.**

---

## 3. What SX3 inherits

**D11 — a changed admitted byte needs a registry move as much as a new path
does.** The publisher pins a digest per path. "Does this add a new served path?"
is the wrong pre-merge question; "does this change the bytes of any path the
registry already admits?" is the right one. Stage the move as a transition pair
`[pre, post]`, prove the registry on **unchanged** bytes first, then merge the
content. `tools/lf1/check_admission_move.py` checks the necessary condition
before the merge.

**D12 — build a counterfactual to contradict you, not to pass.** An invariant
that reads the same before and after has proved nothing. Construct the case that
should make it fire, and check that it does.

**D13 — a browser-rendered census is the standard for any pupil-visible claim.**
Neither a source grep nor a tag-stripped fetch is a render. Use a source scan to
enumerate candidates; adjudicate in the DOM.

**D14 — what a render census must cover:** the deck driven through its real
control (not slide 1), each gate pressed and sampled individually (not a batch),
both chassis conventions (data-attributes and inline `onclick`), print as a
separate subtree, and accessible names. On LF1 the same phrase counted 8, 72, 83,
86 and 121 depending on which of those was missed.

**D15 — one re-run of an install-time failure is a discriminating test, not a
retry.** A second identical install failure is an outage: wait it out, never
bypass.

---

## 4. State of the estate SX3 starts from

- **LF1 closed the live defect.** 121 restorations across 22 files and 9 redundant
  staff twins removed (#468). Repo-wide: 0 defect occurrences, 3 authored
  instances of the phrase retained (`6 Art/Lesson15`, `Grow/Slideshows/GROW_HUM_W7`,
  a PEQ script string).
- **The publisher pin cycle for LF1 is #469**, and the Autumn 1 refresh's cycle is
  stacked on it (Site `fac26001`). Both are proved on unchanged bytes.
- **R6's five content PRs (#460–#464) are re-cut with the relabel dropped** and
  hold for the Thursday window. Their 38 files and 25 pins partition cleanly, 5 /
  0 / 5 / 8 / 7.
- `tools/relabel_public.py` is the single writer for the public-relabel rule and
  is now refusing by default. Do not add a mode that guesses.
