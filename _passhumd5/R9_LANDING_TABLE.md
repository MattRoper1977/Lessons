# R9 — RESOLVED: land the full proofread set

The 950 MB figure is **struck from the order as a non-fact**. What follows is the
measurement that struck it, and the landing table the ruling asks to be recorded.

## Why there was nothing to land "within"

SCOPE: `origin/main` at `cbfbc70c`, the whole Lessons repo.

**There is no coded size gate.** No workflow, no tool and no record names a byte
budget. Searched: every `.github/workflows/*.yml` for `count-objects`, `du -sh`,
"repo size", "repository size"; every `tools/**/*.py|*.mjs|*.cjs` for `MAX_BYTES`,
`size_limit`, "too large", "byte budget"; every `*.md` for "950 MB", "size budget",
"repo-size". Every hit was coincidental — sha256 digests, `font-weight:950`, a row
count of 950. `.gitattributes` carries **one** line (`Science_Teesside/Teaching_Packs/**/*.pdf binary`)
and no `filter=lfs`.

**There is no separate large-asset route either.** The estate already tracks this
exact class of media directly in git:

| type | tracked files | bytes |
|---|---:|---:|
| `.zip` | 115 | 390.2 MB |
| `.pdf` | 965 | 207.3 MB |
| `.png` | 740 | 177.5 MB |
| `.html` | 1530 | 133.9 MB |
| `.pptx` | **247** | **96.3 MB** |
| `.docx` | 415 | 27.7 MB |
| `.mp4` | **3** | **16.7 MB** |

Largest single tracked file: `LundyLoop/6_posters/source/LundyLoop_Sublime_Posters_EDITABLE_MASTER.pptx`,
37.4 MB. So holding 63.2 MB of pptx and video back for a route that does not exist
would have shipped broken packs for no measured benefit.

## Landed, per pack

SCOPE: the 13 proofread packs as they stand after B1 — D1 and D2 applied, 22
`Pupil_Resources.pdf` re-rendered, `SHA256SUMS.txt` verified **1605 entries / 0 FAIL**
across all 11 Final packs.

| pack | bytes landed | files |
|---|---:|---:|
| `HUM_00_SoW_and_Order` | 298,214 | 7 |
| `HUM_Autumn_1_BUILD_GROW_Fallback` | 16,963,659 | 127 |
| `HUM_Autumn_1_LAUNCH_Final` | 11,613,310 | 97 |
| `HUM_Autumn_2_BUILD_Final` | 12,423,785 | 121 |
| `HUM_Autumn_2_GROW_Final` | 17,595,871 | 111 |
| `HUM_Autumn_2_LAUNCH_Final` | 25,208,538 | 115 |
| `HUM_Spring_1_BUILD_GROW_Final` | 24,414,082 | 184 |
| `HUM_Spring_1_LAUNCH_Final` | 10,956,192 | 84 |
| `HUM_Spring_2_BUILD_GROW_Final` | 26,520,872 | 194 |
| `HUM_Spring_2_LAUNCH_Final` | 16,997,594 | 104 |
| `RE_Autumn_BUILD_Final` | 21,444,681 | 202 |
| `RE_Autumn_GROW_Final` | 22,179,251 | 202 |
| `RE_Autumn_LAUNCH_Final` | 23,678,754 | 202 |
| **TOTAL** | **230,294,803 = 230.3 MB** | **1750** |

By type: html 487 / 102.2 MB · mp4 120 / 46.5 MB · pdf 360 / 26.4 MB ·
docx 228 / 17.6 MB · png 158 / 17.2 MB · pptx 120 / 16.7 MB · svg 106 / 2.6 MB ·
jpg 6 / 0.5 MB · txt 130 / 0.3 MB · xlsx 13 / 0.1 MB · md 12 / 0.1 MB ·
json 1 / 19,126 B · csv 9 / 3,244 B.

**Nothing held.** The 270 images (20.4 MB) land with the rest: D1's media credits sit
directly under `Teaching_Visual_1.png`, so landing the HTML without them would have
published a credit pointing at a missing image.

## Repo size, before and after

| | bytes | |
|---|---:|---|
| before (`cbfbc70c`, all tracked regular files) | 1,127,354,861 | **1,127.4 MB** |
| after (projected, + the full pack set) | 1,357,649,664 | **1,357.6 MB** |
| delta | +230,294,803 | **+230.3 MB, +20.4%** |

For completeness, the other measures at `cbfbc70c`: tracked minus top-level `_*`/`.*`
directories **921.1 MB** (3,599 files / 206.2 MB sit in those); the `.git` pack
**1.46 GiB** (`git count-objects -vH`).

## Carried to the next order, not tonight

The Lessons repo has **no size gate and no large-asset route**. Both are backlog. If a
budget is ever wanted, it has to be written as a gate with a red proof, like every
other control in this estate — the figure in an order text is not one, which is what
this measurement established.

## Landed — ORDER FINISH-2 §3 (2026-09-20)

Branch `claude/hum-d5-packs`, commit `8b5db17b`, stacked on F3b (`a2478abd`) so the
gate copies and pins never conflict; Apps companion `claude/hum-d5-packs-companion`
`ff5285a` (gate copy byte-identical, `a94755ec…`).

**Source**: the post-B1 workspace `/tmp/claude-0/humd5/unzipped/` — 13 packs, 1750
files, 230,294,803 bytes, byte-for-byte the R9 table above. Each pack's single inner
root lands as `Humanities_Teesside/Teaching_Packs/<inner root>/` (the pack's own name,
e.g. `HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W01/…`); 0 collisions with the HC5
series already there (`BUILD/`, `GROW/`, `LAUNCH/`, `index.html`, …).

**Verification at landing**: the 11 Final packs against their own `SHA256SUMS.txt`:
96 + 120 + 110 + 114 + 183 + 83 + 193 + 103 + 201 + 201 + 201 = **1605 OK, 0 FAIL**.
`HUM_00_SoW_and_Order` (7 files) and `HUM_Autumn_1_BUILD_GROW_Fallback` (127) carry no
`SHA256SUMS.txt` — recorded, not invented.

**Route** (§2): `HUMANITIES_PACKS = 'Humanities_Teesside/Teaching_Packs/'` beside
`SCIENCE_PACKS`, same clause shape, no wider. Self-test 1312 → **1321** controls, all
PASS. Red proofs, quoted from the self-test output:

```
A Humanities file outside the pack prefix is not admitted by the pack route
An unlisted Humanities teaching file is rejected
A modification of a pinned Humanities pack file is rejected
A deletion of a pinned Humanities pack file is rejected
A pinned Humanities pack file whose bytes drift from its pin is rejected
A planted, exactly pinned Humanities pack file passes as an addition
Exact individually pinned Humanities teaching files pass as additions   (the tree's 1750)
```

Judge on the committed diff against F3b: `status PASS, protectedChanges 1750`.
The permission classifier did not block the fence edit (it had blocked the spine
admission earlier; that was then ruled).

**Pins**: 1750 explicit paths appended to `REVIEWED_PATHS` (the Science pack
precedent: *"Every path is explicit; no directory wildcard can admit future
payloads"*), `CATALOGUE_PINS` in both gate copies, `gateSha256 a94755ec`. PIN1 by
`derive_triggers.py --write`: **560 → 2310** exact triggers per event;
`mbm-cross-estate-unification.yml` **104,085 → 534,033 bytes, 1420 → 4920 lines**.
Whether Actions accepts a workflow of that size is not known from any document I
can find; the PR's first run proves it (STOP-R if not).

**PR granularity — one PR, and why**: the ≤12-lessons rule governs content PRs that
rewrite served lessons (F3); this set rewrites none — it is 1750 additive files the
fence judges one by one against their pins. Splitting it would cost a gate re-pin,
an Apps companion and a PIN1 rewrite per slice for no added review surface, since
the review unit is the pack (13) and the proof unit is the file (1750), both already
itemised here.

**Repo size** (`git count-objects -vH`, the shared object store, before → after the
landing commit): loose `size` **139.55 → 282.81 MiB**; `size-pack` **1.46 GiB → 1.46 GiB**
(new objects are loose until the next gc). The earlier figure in this file
(1,127.4 → 1,357.6 MB) was the scratch clone's working tree, not this store.

**Not done here, named**: the packs are served but not yet *listed*. The pack hub
`Humanities_Teesside/Teaching_Packs/index.html` sits under the new prefix, unpinned,
so an edit to it falls through to the fence by design (and pinning it would make the
new clause reject the edit as a non-addition). The subject hub
`Humanities_Teesside/index.html` has a SHELVES route (M + pin) but its writer,
`build_humanities_shelf.py`, is fed by `build_catalogue.py`, which the shelf STOP-X
(`_sx3/SHELF_RECLASSIFICATION.md`) keeps unrun. Listing is a §5/§7 input, not a §3
deliverable; recorded so it is not mistaken for done.
