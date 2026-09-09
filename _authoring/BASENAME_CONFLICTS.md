# Same-basename divergences (D31)

D26 applied to inbound files rather than to lookups. Any upload sharing a basename
with a landed file is compared by **content hash** before use. A hash mismatch is a
listed conflict reported by name — never a silent overwrite, never a merge of the
two.

A basename collision does not announce itself. It produces a plausible file.

| basename | path A | size A | md5 A | path B | size B | md5 B | canonical | why |
|---|---|---:|---|---|---:|---|---|---|
| `GROW_Week_01_Interactive.html` | loose upload | 24,008 | `b927e6f686` | `GROW_Computing_Weeks_01_02_Complete.zip` → `Week_01/` | 33,712 | `d8f60ff52b` | **B (zip)** | A predates the current chassis: no `id="route"` selector, no `id="largeText"`, no `id="chassis"` stage nav, and its options are `0,1,2,3` rather than step/main/challenge. It cannot satisfy P1's eight-stages-three-routes gate. |
| `GROW_Week_01_Teaching_Slides.pptx` | loose upload | 47,188 | `dd2951722d` | `GROW_Computing_Weeks_01_02_Complete.zip` → `Week_01/` | 59,661 | `fc6c7f7cb8` | **B (zip)** | Divergent by hash, 12,473 bytes smaller. Same treatment: superseded revision, never landed, never merged with the zip copy. |

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
