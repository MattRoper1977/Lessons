## D49 — the census that printed zero for every branch, and the control that could not fire

The SX2R §4.3 rendered census over the 35 touched pages came back looking clean.
It was not a result. Two defects, both in the shape the family keeps taking: an
inclusion rule that was wrong about what it was looking at.

### Defect 1 — a counter that could not fail

The driver reported occurrences with

```python
sum(len(p.get('occurrences',[])) for p in (d if isinstance(d,list) else d.get('pages',[])))
```

`render_census.cjs` writes an **object keyed by page path**, with no top-level
`pages` key. So `d.get('pages',[])` returned `[]`, the sum was `0`, and no
exception was raised — which meant the `|| echo '?'` fallback never fired
either. **Every branch printed `occurrences 0`, including the four where the
positive control had genuinely found something.** The exit codes were real; the
numbers printed beside them were not.

Counted properly from the JSON the same run had already written to disk:

| branch | control occurrences / rendered | real occurrences / rendered |
|---|---|---|
| build | 10 / 5 | 0 / 0 |
| grow-a | **0 / 0** | 0 / 0 |
| grow-b | 13 / 5 | 0 / 0 |
| launch-1 | 8 / 8 | 0 / 0 |
| launch-2 | 7 / 7 | 0 / 0 |

### Defect 2 — the wrong control for that branch

Which exposed the second one. `grow-a`'s control found nothing because
**"Learning objective" has 0 source hits on all eight of its pages**. Those eight
are `Science_Teesside/Grow/resources/GS_W*.html` — resource sheets, a different
chassis from the decks the phrase was chosen for. A control that is absent from
the tree it runs on cannot fire, and a control that cannot fire proves nothing
about the instrument.

Re-run with `"Return to the lesson"`, present in source on 8/8 of them:

```
grow-a  CONTROL  pages 8  occurrences 8  rendered 8
grow-a  REAL     pages 8  occurrences 0  rendered 0
```

### What is now true

All five branches have a **fired** control and a clean real result. 35 pages,
5 + 8 + 7 + 8 + 7, no overlap. The §4.3 gate is discharged.

### The rule

A positive control is chosen **per tree**, and its presence in that tree is
checked before the run, not inferred from the run. And a counter that returns 0
for a shape it does not recognise must raise instead — see `REGISTER.md` T1,
*a census declares its universe*, and the counter now used
(`census_count.py`) exits 3 on an unrecognised shape rather than printing a
number it did not compute.

Same family as D17 (*the positive control runs first*), and the sibling of the
`a4_fit` printf defect landed in `ee0a85be`: in both, the verdict was computed
correctly and the figures printed beside it were fiction.
