# Ruling 2's new control — "no panel may land on a stage carrying the deck <h1>"

Derived predicate, well-defined on all 34 decks (3 exemplars + the 31):

```python
PATHWAY = re.compile(r'^(build|grow|launch)\s+science(\s+\S+)?$', re.I)

def deck_title(doc):
    ts   = doc.find(lambda x: x.tag == 'title')
    head = [t for t in ts if any(a.tag == 'head' for a in t.ancestors())] or ts
    segs = [norm(s) for s in norm(head[0].inner_text()).split('·')]
    return ' · '.join(s for s in segs if not PATHWAY.match(s)).lower()

def stage_heading(s):
    hs = s.find(lambda x: x.tag in ('h1', 'h2', 'h3'))
    return norm(hs[0].inner_text()).lower() if hs else ''
```

RED when `stage_heading(s) == deck_title(doc)` and `s.find(is_ribbon)` is non-empty.

```
title-heading stage [0] -> 34 deck(s)
anomalies: NONE
decks where that stage already carries a panel: 0   (expected 0 — the 31 have row45 = 0)
```

## Three format variations had to be handled; each was a miss before it was a rule

The naive predicates both fail, and my first two attempts were wrong:

1. **`<title>` contains more than one `·`.** `'build science · give a rock a job · classic'` —
   splitting on the LAST separator yields `'classic'`. Missed 3 decks
   (`SCI_B_W12`, `SCI_G_W9`, `SCI_G_W12`).
2. **The word order is reversed between the exemplars and the 31.** The 31 put the pathway
   first (`'BUILD Science · …'`); the GROW and LAUNCH exemplars put it last
   (`'Day and Night: Sky Shift · GROW Science'`). Splitting on the FIRST separator then
   missed the 2 exemplars. Hence: drop whichever segment *is* the pathway marker, rather
   than relying on position.
3. **The pathway segment may carry a week code.** The BUILD exemplar is
   `'BUILD Science W8A · Sugar Evidence: Read the Label'`, so `^(build|grow|launch) science$`
   does not match it. Hence the optional `(\s+\S+)?`.

Two further hazards the predicate must not assume away:

- **A document carries several `<title>` nodes** — 5 on the GROW exemplar, 6 on LAUNCH —
  because inline SVGs carry their own. The head `<title>` must be selected by ancestry, not
  by taking the first match.
- **The exemplars have no `<h1>` inside any stage at all.** Their title stage heads with a
  lower level, so an `h1`-only predicate finds nothing on 2 of 34. The heading probe must
  accept `h1`/`h2`/`h3`.

## Why this control is the one that would have caught the defect

Under the pre-correction mapping the three merged title+arrival stages resolved to `arrival`,
so they were *eligible* and row 1 would have demanded exactly one panel on each — placing a
pupil-response panel on the stage holding the lesson's own title heading, on 3 of 31 decks.
Row 14 could not see it because `title_stages` was empty there.

This control does not depend on stage naming at all. It reads the deck's title and the
stage's heading directly, so it fires whatever the identity oracle believes — which is
precisely what makes it a check on the oracle rather than a restatement of it.
