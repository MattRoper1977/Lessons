## D29 — §4c restoration proceeds on the derived 86

Ruled by Matt, 2026-09-09 (LF1M-FIN). The count is the **output** of the
derivation, never a target to match: the 183 does not gate §4c, and a figure not
produced by a script that was run is MEASUREMENT INVALID.

Derived: **103 dropped sentences, 86 of them content.** `status` and `model.type`
are deliberate state changes and stay excluded; the 17 non-content sentences are
recorded in `_sx2/tutor_time/RESTORE_4C.md`, not restored.

**Restored: 12 ids, 51 sentences, derived diff 0 on every one.**
**Held: 5** — S06 and S04 under S2, and B02, B05, V04 as listed B1 conflicts.

### The distinction the run turned up

Six of the 86 are **not dropped lines at all — they are replacements.** The slot
holds different approved wording, so appending the original verbatim would put two
instructions in one single-sentence slot. That is a conflict to post, not a
restoration to perform. The thirteenth named line is one of them:

> `V04` `model.steps[3].text` — original *"A trusted adult can help when pressure
> continues."*, re-cut *"Ask a trusted adult now if worried; no refusal is required
> first."*

Merging those would reword safeguarding text, which S7 forbids. **A diff that says
"absent" cannot tell a deletion from a replacement, and only one of them is
restorable.**

### Two copies, one write

Each re-cut holds its text twice — the static `<aside class="staff" hidden>` and
the `DATA` payload — and they agree today. So a field's exact text must occur
**exactly twice** in the file: 2 before the write and 2 after is B2 proved, and a
single write updates both copies so they cannot drift. Nothing is regenerated;
there is no builder here, and a divergence is a STOP.

The B4 proof is arithmetic: the whole-file byte delta equals exactly **twice** the
appended text on all 12. Any other edit would show up in that number.

### `model.*` is not appendable

`model.caption` and `model.steps[*]` render into the SVG as `textLength`-fitted
`<text>` runs, plus a `<desc>` and an `aria-label`. An append there is a relayout,
not a verbatim insertion. `tools/lf1/restore_recut.py` refuses any `model.*` path
outright, and that refusal is one of its D28 controls.
