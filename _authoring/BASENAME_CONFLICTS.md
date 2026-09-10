# Same-basename divergences (D31)

D26 applied to inbound files rather than to lookups. Any upload sharing a basename
with a landed file is compared by **content hash** before use. A hash mismatch is a
listed conflict reported by name — never a silent overwrite, never a merge of the
two.

A basename collision does not announce itself. It produces a plausible file.

| basename | path A | size A | md5 A | path B | size B | md5 B | canonical | why |
|---|---|---:|---|---|---:|---|---|---|
| `GROW_Week_01_Interactive.html` | loose upload | 24,013 B | `b927e6f686` | `GROW_Computing_Weeks_01_02_Complete.zip` → `Week_01/` | 33,725 B | `d8f60ff52b` | **B (zip)** | A predates the current chassis: no `id="route"` selector, no `id="largeText"`, no `id="chassis"` stage nav, and its options are `0,1,2,3` rather than step/main/challenge. It cannot satisfy P1's eight-stages-three-routes gate. |
| `GROW_Week_01_Teaching_Slides.pptx` | loose upload | 47,188 B | `dd2951722d` | `GROW_Computing_Weeks_01_02_Complete.zip` → `Week_01/` | 59,661 B | `fc6c7f7cb8` | **B (zip)** | Divergent by hash, 12,473 bytes smaller. Same treatment: superseded revision, never landed, never merged with the zip copy. |

### D37 — a whole-pack supersession, not a basename collision

`GROW_Computing_Weeks_07_08_Complete.zip` exists in two versions, and this one is
listed here because the same reasoning applies at pack scale.

| version | files | bytes | md5 | standing |
|---|---:|---:|---|---|
| revised | 35 | 1,549,100 B | `3f30a30d50e33a7ebbd2bf75ad958a31` | **canonical** |
| superseded | 32 | 1,053,102 B | `4719a668cd9e1ce5413a954bde7b4f8c` | held in `GROW_Computing_2026-09-09/superseded/` |

**Measured: 0 of the 32 shared paths are byte-identical.** So there is no per-file
"best of" to assemble and no merge to attempt — every shared file diverges, which
is what makes this a replacement rather than a collision. No file is taken from
the superseded pack.

Three files are new in the revision: `GROW_Computing_Weeks_07_08_Review_Notes.txt`
(an authoring record, held in `_authoring`, never on a route) and
`Planning/GROW_Computing_Final_Evidence_Check.docx`/`.pdf`.

Note the sizes above are **bytes on binary reads**. The two Week 01 rows in the
table above previously read 24,008 and 33,712, which are character counts: see
D30 and D33, and `tools/measure_size.py`, which now refuses to label a text-mode
read `B`.

## Checked and NOT divergent

`GROW_Week_03..06_Interactive.html` — the loose uploads and the zip copies are
equal by **md5 on binary reads** (D33), all four:

| week | bytes | md5 |
|---|---:|---|
| W03 | 26,429 | `6973fbee1ffc` |
| W04 | 30,611 | `ba23e3f395f6` |
| W05 | 31,306 | `c27cadaccf0a` |
| W06 | 31,840 | `14c1411c2a29` |

An earlier report called these "byte-identical" from a text-mode read. The claim
was right and the instrument was not — see D33.
