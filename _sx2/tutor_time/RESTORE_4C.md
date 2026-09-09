# §4c restoration — 12 ids restored, 5 held

Run under LF1M-FIN D29 on the derived 86 content sentences. `status` and
`model.type` stay excluded as deliberate state changes; the 17 non-content
sentences are recorded here and not restored.

## What landed

| id | derived | restored | fields | 2 copies before | 2 copies after | whole-file delta |
|---|---:|---:|---:|:--:|:--:|---|
| `B01` | 4 | **4** | 2 | 2/2 | 2/2 | +506 bytes = 2 × 253 appended |
| `B03` | 5 | **5** | 2 | 2/2 | 2/2 | +540 bytes = 2 × 270 appended |
| `B04` | 8 | **8** | 3 | 2/2 | 2/2 | +874 bytes = 2 × 437 appended |
| `S02` | 5 | **5** | 2 | 2/2 | 2/2 | +594 bytes = 2 × 297 appended |
| `S03` | 2 | **2** | 1 | 2/2 | 2/2 | +210 bytes = 2 × 105 appended |
| `S07` | 2 | **2** | 2 | 2/2 | 2/2 | +424 bytes = 2 × 212 appended |
| `S09` | 4 | **4** | 2 | 2/2 | 2/2 | +746 bytes = 2 × 373 appended |
| `V02` | 3 | **3** | 2 | 2/2 | 2/2 | +498 bytes = 2 × 249 appended |
| `V03` | 5 | **5** | 2 | 2/2 | 2/2 | +680 bytes = 2 × 340 appended |
| `V05` | 4 | **4** | 2 | 2/2 | 2/2 | +572 bytes = 2 × 286 appended |
| `V06` | 3 | **3** | 2 | 2/2 | 2/2 | +566 bytes = 2 × 283 appended |
| `V07` | 6 | **6** | 2 | 2/2 | 2/2 | +734 bytes = 2 × 367 appended |
| **total** | **51** | **51** | | **12/12** | **12/12** | **clean on all 12** |

**51 of 51 sentences present in the restored payload, and the derived diff is
0 for every one of the 12.** The byte delta equalling exactly twice the appended
text is the B4 proof that nothing else moved: any other edit would show up in it.

## Why the two-copies count *is* the byte-equality assertion

Each re-cut holds its text twice — rendered into the static `<aside class="staff"
hidden>` and again in the `DATA` payload — and they agree today. So a field's exact
text must occur **exactly twice** in the file. 2 before the write and 2 after is
B2 proved, and one write does both copies, so they cannot drift apart. Nothing is
regenerated: there is no builder here, and a divergence is a STOP, never a rebuild.

## Held, with the reason

| id | derived | why held |
|---|---:|---|
| `S06` | 5 | **S2** — Online blackmail. Derived and diffed below; nothing written. |
| `S04` | 5 | **S2** — Deepfakes and sharing. Derived and diffed below; nothing written. |
| `B02` | 7 | **B1 conflict** — 2 of 7 are replacements in single-sentence slots |
| `B05` | 9 | **B1 conflict** — 1 replacement, plus `model.caption` rendering into the SVG |
| `V04` | 9 | **B1 conflict** — 3 replacements incl. the thirteenth named line, plus `model.caption` |

## The conflicts, named

These are **not dropped lines**. The slot holds *different approved wording*, so
appending the original verbatim would put two instructions in one single-sentence
slot. That is a listed conflict under B1, not a restoration.

**`B02` · `followup.action`**  
- original: *Choose one unclear routine and draft a clearer instruction with accessible options.*  
- re-cut: *Optionally suggest clearer wording for one fictional routine first; staff can consider an appropriate real routine later.*

**`B02` · `followup.response_by`**  
- original: *Within one week: staff share the accepted wording or explain a change.*  
- re-cut: *Suggested: within one week, staff explain whether the wording can be used or needs a change.*

**`B05` · `followup.response_by`**  
- original: *Next tutor session for clarity; safeguarding concerns immediately*  
- re-cut: *Suggested: next tutor session for route clarity; safeguarding concerns immediately.*

**`V04` · `model.steps[2].label`**  
- original: *State a boundary*  
- re-cut: *Choose a safe response*

**`V04` · `model.steps[2].text`**  
- original: *Say no, pause or use another safe way to respond.*  
- re-cut: *Pause, decline or get adult help; do not confront someone if unsafe.*

**`V04` · `model.steps[3].text`**  
- original: *A trusted adult can help when pressure continues.*  
- re-cut: *Ask a trusted adult now if worried; no refusal is required first.*

### And a second constraint on `model.*`

`model.caption` and `model.steps[*]` render **into the SVG** as `textLength`-fitted
`<text>` runs, plus a `<desc>` and an `aria-label` — three places, laid out to a
measured width. An append there is not verbatim; it is a relayout. The restorer
refuses any `model.*` path outright, and that refusal is one of its controls.

## B3 — the thirteenth line, on its own

The thirteenth named line is `V04` `model.steps[3].text`:

> original: **A trusted adult can help when pressure continues.**  
> re-cut: **Ask a trusted adult now if worried; no refusal is required first.**

**It cannot be restored verbatim and V04 is held.** The slot is not empty — it
carries different safeguarding wording, and the field renders into the SVG. Merging
the two would reword safeguarding text, which S7 forbids. It is posted here for a
ruling rather than written.

## S06 and S04 — derived, diffed, nothing written

Both derive **clean**: all ten lines are additive, no conflicts. They would restore
without incident. They stay held under S2.

### `S06`

- `hook` — *Fictional: 'Pay by tonight or I share it.' The message wants a rushed decision.*
- `hook` — *What gives the targeted person more support?*
- `staff.delivery` — *Use the shared 20-minute sequence with the fallback unless the film is previewed.*
- `staff.delivery` — *Silent choice, pointing, adult reading and pass are available.*
- `staff.delivery` — *If a pupil raises an actual concern, safeguarding action begins now; it never waits for an exit ticket or tutor follow-up.*

### `S04`

- `hook` — *Fictional: a group chat says an intimate image is fake.*
- `hook` — *Does that make forwarding it harmless?*
- `staff.delivery` — *Use the shared 20-minute sequence.*
- `staff.delivery` — *Allow silent choice, pointing, adult reading or pass.*
- `staff.delivery` — *If personal information emerges, stop the public discussion and follow safeguarding procedure immediately.*

