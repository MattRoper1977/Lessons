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
