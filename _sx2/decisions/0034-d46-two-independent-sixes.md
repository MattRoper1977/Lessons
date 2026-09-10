## D46 — the instrument correction is recorded, not just the result

Three facts belong in the register together, because it is their agreement that
makes D38's parent-link finding evidence rather than a claim.

| source | superseded 32-file pack | revised 35-file pack |
|---|---:|---:|
| the revision's own authoring record — *"Repaired six unintended Scratch block-parent links"* | **6** | — |
| `tools/gc1/check_sb3_parents.py`, per-target | **6** (exactly 1 per project, all six `control_wait_until` CONDITION with `parent: null`) | **0** |
| the same checker's first draft, flat project-wide map | 7 | 1 |

**Two independently derived sixes agreeing** is the finding. The author counted
six repairs; a checker written without knowledge of that count measured six, one
per project, all of the same shape. Neither figure was derived from the other.

### The third row is the one worth keeping

The first draft built **one block map for the whole project**. Scratch block ids
are unique per target, not per project, and these packs are hand-authored with
`k1..kN` restarting in every sprite — measured on `W07_Bug_Hunt`, **eleven ids
appear in both `Player` and `Hazard`**. So Player's `k11` was judged against
Hazard's `k11`'s parent, and the checker reported a bad link in the revised pack.

That would have been a **STOP on a sound pack**, produced by the module written
to prevent exactly that. It is the fourth instrument this week to return a verdict
on a property it could not observe — after basename keying, the detached clone,
and the schema validator — and the first of the four that was mine.

Per D28 the gate ships with both controls regardless: a real run over the estate
(6 / 0 / 0 across superseded, revised and Weeks 1–6), and a planted null parent
proving it fires. A third control was added for the defect itself — two sprites
sharing block ids, each internally consistent — because that is the shape that
caught the instrument out.
