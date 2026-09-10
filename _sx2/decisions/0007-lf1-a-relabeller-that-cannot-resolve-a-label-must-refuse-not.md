## LF1 — A relabeller that cannot resolve a label must refuse, not guess

**Status: the tool change is here. The 121 restorations are proposed, not landed.**

### What went wrong

`tools/relabel_public.py` replaces pupil-facing calendar labels ("Week 9",
"W14") with sequence-relative ones ("Lesson 3 of 12"). It resolves a week
number against the unit manifest in the file's own folder. When the week was
not in that manifest it returned one of two strings:

```python
if s.lo is not None and w < s.lo: return 'the previous unit'
if s.hi is not None and w > s.hi: return 'the next unit'
```

Neither is a translation of a week number. Both are a guess, and on the CX3
pass of 2026-09-08 the guess was taken **121 times across 22 published pages**.

### Why the guess is always wrong here

The two branches fired on cross-unit references — a recap naming an earlier
week, or a forward reference to the next half-term. Four failure shapes came
out of them:

| shape | occurrences | example |
|---|---|---|
| distinct weeks collapse to one phrase | 105 | `W5:` `W6:` `W7B:` all became `the previous unit:` — three different recap lines, one indistinguishable label |
| ranges double the phrase | 16 | `W2–W3:` → `the previous unit–the previous unit:` |
| an article in front of it duplicates | 11 | `the W14 question` → `the the next unit question` |
| the reference is not to a unit at all | all of them | W5–W7 are earlier lessons in the same strand; calling them "the previous unit" is wrong even where it reads |

(Shapes overlap: the range and article counts are subsets of the first.)

The causal set is exactly two branches — `w < lo` (54 occurrences) and
`w > hi` (51) — plus the never-taken third fallback. Simulating the tool on the
recovered originals reproduces the live bytes for **103 of 103** affected
nodes, so nothing about the mechanism is unexplained. An earlier hypothesis
that flat folders (`sequence()` returning `n=None`) caused it is **wrong**: no
live occurrence came from a flat folder. Every affected file resolved its own
sequence correctly.

### The rule

A tool that cannot resolve a label says which label, in which file, in which
sentence, and changes nothing. `Unresolvable` is raised; the file is not
written; the run exits 2. There is no mode in which this tool authors a label
it did not read.

`added_banned()` is the post-condition (LF1 B6): a run may never *increase* the
count of `the previous unit` / `the next unit`. It asserts an increase, not
zero, because both are honest prose a teacher may have written — `6
Art/Lesson15` and `Grow/Slideshows/GROW_HUM_W7` each contain one, authored, and
neither is a defect.

Red-proved in both directions on the real estate, not on fixtures: of the 64
HTML files the CX3 pass touched, the fixed tool refuses **exactly** the 22 that
carry the defect and applies cleanly to all 42 that do not. No false positive,
no false negative.

### Recovery is from stored bytes, never re-derivation

The relabeller stores the original text in `data-mbm-cal` on the enclosing
element. That store was checked against an independent source: for all 22
files, `walk(live, 'revert')` is **byte-identical** to the blob at the parent of
the first CX3 commit. Two sources, agreeing on every byte, so the restored
strings are the ones that were there — not inferred from neighbouring weeks,
not hand-authored. The C3 list (unrecoverable, needing a human) is **empty**.

### What this costs

The 22 files cannot be relabelled by tooling any more, and should not be. Their
recaps name specific earlier lessons; turning those into sequence-relative text
needs someone who knows what the pupil is being asked to remember.

### LF1-B — how the count was wrong, and what a pupil-visible claim now costs

**31 → 121.** The first LF1 census reported 31 occurrences across 19 files. The
real figure is 121 across 22. Two independent errors, both in the same direction:

1. `git grep -c` counts matching **lines**, not occurrences. A line carrying
   `the previous unit–the previous unit` counted as one.
2. The search set was incomplete. `the next unit` was never searched for in the
   Science Build tree, so `SCI_B_W13A` (18) and `SCI_B_W13B` (33) — the two worst
   pages in the estate — were absent from the list entirely.

**The standard, from here.** Any claim about pupil-visible text is measured in a
browser, on the DOM, on every route the page has. `tools/lf1/render_census.cjs`
is that measurement. What it changed about the LF1 numbers:

| measured as | count |
|---|---|
| source grep, lines | 31 |
| DOM text nodes, slide 1 only | 8 |
| DOM, driving the slide control | 72 |
| …also pressing the tier and model-step controls | 75 |
| print emulation, union over every printable tier | 35 |
| accessible names (`aria-label`) | 3 |
| **total in the document** | **121** |

Three lessons in that table. A count on slide 1 is not the deck — most slides are
`display:none` until navigated, and `showSlide` is inside a closure, so the walk
has to drive the real `#next` control. Content behind one press of a tier or
reveal button is pupil-facing, not a caveat. And the printed worksheet is a
separate DOM subtree: `SCI_B_W8B` had four occurrences in print and none on
screen at load, so the defect reached handouts before it reached a screen.

**The duplicate that was not one.** A direct fetch of `SCI_B_W13A` appeared to
show placeholder and correct copy in one node. It is the `span.mbm-cal-staff`
twin the six *v4 relabel bytes* commits (`a229cdf`, `aa6aaea`, `d1ae3a2`,
`ba61840`, `edc6b36`, `06b77c8`) add so staff keep the calendar declaration a
pupil no longer sees. It is inline `display:none`, so a browser renders one copy
— but any tag strip that ignores CSS renders both, which is what the fetch did.
26 twins exist; the 8 files with only the first CX3 pass have none.

**But the hiding is not load-bearing.** `html.mbm-guide-on
[data-mbm-guide]{display:revert!important}` beats an inline non-important
`display:none`, so with guide/TA mode on the line renders twice — 9 such pairs on
5 pages. That is a guide-mode bug, not a relabel bug, and it is recorded
separately; the LF1 fix deletes only the 9 twins that restoration makes into
word-for-word restatements, and leaves the 17 doing their job.

**The proxy substitution is resolved.** Matt fetched the origin directly. The
admission-registry membership argument is retired as a served proof for LF1;
served proof is a fetch of the four URLs, read as rendered DOM.

**A URL already fetched in this session is not a fresh read after a deploy.**
Closing LF1, two of the four proof pages first came back still showing the
placeholder. That looked like a partial publication — some paths served, some
not — which would have been a serious finding about the publisher. It was fetch
cache. The pages were correct; the reader was not.

So a re-fetch of a URL the same session has already opened proves nothing about
what is being served now. It has to be a genuinely fresh read: a different
client, a cache-defeating request, or a device that has not seen the page.

What actually closed LF1 was the second instrument agreeing with the first. The
census of the published tree said 0 on every route and the phone said the same,
and the phone had never loaded those URLs. Two readings from independent paths,
not one reading taken twice.

LF1 confirmed live 2026-09-09 19:50 BST: SCI_L_W8L1 and LAUNCH_HUM_W9 clean on
screen and in print; SCI_B_W13A reads "for the W14 rock investigation"; SCI_B_W8B's
Arrival reads W8A / W7 / W4 / W2-W3.

---
