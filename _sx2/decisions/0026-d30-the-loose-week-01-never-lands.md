## D30 — the loose Week 01 never lands

`GROW_Week_01_Interactive.html`, **24,013 B, md5 `b927e6f686`**, is **provenance,
not content**. It predates the current chassis: no `id="route"` selector, no
`id="largeText"`, no `id="chassis"` stage nav, and its options are `0,1,2,3`
instead of step / main / challenge. It cannot satisfy P1's eight-stages-three-routes
gate.

**The canonical Week 01 lesson is the copy inside
`GROW_Computing_Weeks_01_02_Complete.zip`, 33,725 B, md5 `d8f60ff52b`**, and
G7(b)'s duplicate `id="centre"` is a property of *that* copy — the order's
measurement was taken correctly.

**The slides diverge too.** `GROW_Week_01_Teaching_Slides.pptx` is **47,188 B, md5
`dd2951722d`** loose against **59,661 B, md5 `fc6c7f7cb8`** in the zip. Not a
duplicate: a superseded revision, listed by name, never landed, never merged with
the zip copy.

Both go to `_authoring/GROW_Computing_2026-09-09/superseded/` under **G13**. G13 is
a GC1 **P2** step and GC1 is at P0–P1 with zero writes, so the copy is **deferred
with its destination and hashes pinned here**; the record is made now, the bytes
move when the queue opens.

### Correction (FIN3 §8, 2026-09-10): two figures were characters, not bytes

Re-measured before GC1's queue opens, because P2's gates compare byte sizes.

| file | as written | binary bytes | text-mode chars | md5 |
|---|---:|---:|---:|:--:|
| loose `GROW_Week_01_Interactive.html` | 24,008 B | **24,013** | 24,008 | ✅ |
| zip `GROW_Week_01_Interactive.html` | 33,712 B | **33,725** | 33,712 | ✅ |
| loose `GROW_Week_01_Teaching_Slides.pptx` | 47,188 B | 47,188 | — | ✅ |
| zip `GROW_Week_01_Teaching_Slides.pptx` | 59,661 B | 59,661 | — | ✅ |

The two HTML figures were `len(text)`, not `len(bytes)`. Both `.pptx` figures are
right, because a binary file has no text mode to be read in — which is the tell:
the two files that could be misread were, and the two that could not, were not.
CRLF pairs number **0** in both, so this is not line-ending collapse; the gap is
multi-byte UTF-8, 5 such characters in one file and 13 in the other.

Every md5 matches, so nothing is misidentified and no conclusion here moves: the
loose copy is still provenance, the zip copy is still canonical, both still go to
`_authoring/GROW_Computing_2026-09-09/superseded/` under G13, and the destination
stands. Only the sizes change.

This is **D33** — a text-mode read is not a byte measurement — and D30 was written
in the same batch that adopted it. Corrected here rather than left for a P2 gate
to trip over.
