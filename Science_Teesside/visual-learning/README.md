> # ⛔ BLOCKED — DO NOT MOUNT
>
> **This toolkit is loaded by zero lessons, and that is deliberate.**
>
> **Do not add it to any lesson yet.** Mounting is blocked until the LAUNCH explanation has an
> adult route on screen — a teacher must be able to open the explanation for a pupil who has not
> filled the evidence box, using the toggle the lesson chassis already has for staff answers.
> Until that exists, a pupil who cannot type gets no explanation and no adult can give them one.
>
> BUILD and GROW have no such lock, but nothing mounts until all three pathways are safe.
>
> **Read item 37 in the open-items record before touching this.** If you have arrived here from a
> later job that says "mount the science visual layer", that job is blocked and this notice is the
> reason.

# Science visual-learning toolkit — recovered, mounted nowhere

**STATUS: recovered · not mounted · not in use.** These three files exist in the repository and
are loaded by **no lesson**. A toolkit that exists and is mounted nowhere changes no lesson, which
is why it is a safe resting point.

**Derived at `067c76a`, 2026-08-05. PRINT-UNVERIFIED.**

---

## Where these files came from — read this before trusting them

They are **extractions from a demonstration page**, not the supplier's build output.

The supplied pack contained ten files and **no manifest**. The toolkit's own 18 files, both
`.patch` files, `inject.py`, `check.py`, `build_payloads.py`, the canonical `lesson-payloads.json`,
the file-integrity manifest, the ZIP checksum and every original SVG were **all absent**. Because
there is no manifest, **no provenance gate is possible on this input at all** — the absence of a
mismatch proves nothing here, unlike the humanities pack, which shipped SHA-256 per file.

What survived is `Science_Visual_Learning_Demo.html`, which is self-contained and carries the
substance in three blocks. Those blocks were extracted **byte-exact** and written here unchanged,
so anyone can re-extract from the demo and compare:

| file | source block | bytes | sha256 (first 16) |
|---|---|---|---|
| `science-visual-learning.css` | demo `<style>` block 0 | 15045 | `5997baa042f38dad` |
| `science-visual-payloads.js` | demo `<script>` block 0 | 36209 | `ab7ca0839695e006` |
| `science-visual-learning.js` | demo `<script>` block 1 | 61733 | `2d71174738751f35` |

Nothing was reconstructed from prose. The absent build, check and injection tooling and the
canonical JSON source are **recorded as not-received and were not rebuilt** — you cannot verify
what you do not hold. This README is authored here and is **not** the supplier's.

**A note on the payloads.** `science-visual-payloads.js` opens with *"Generated from
lesson-payloads.json; edit the JSON, then run build_payloads.py."* Neither the JSON nor the script
is held. So the payload file is a **build artefact whose source is missing**: it can be read and
edited directly, but it cannot be regenerated, and there is no upstream to diff it against.

## What was verified here, not inherited

The supplier's own validation table was measured in an isolated browser document with assets
inlined — it says so itself — so it is its own workspace record and is **not inheritable as a gate
in this repository**. Everything below was re-derived here:

- `node --check` passes on both JavaScript files. CSS braces balance (136/136).
- Zero `localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`, `fetch`,
  `XMLHttpRequest`, `sendBeacon`, `WebSocket`, `eval`, `document.write`.
- Reduced motion honoured via `matchMedia('(prefers-reduced-motion: reduce)')`, plus a
  `@media (prefers-reduced-motion)` CSS block and a user-facing static-diagram control.
- **Eight `http://` strings appear in the engine and all eight are the SVG XML namespace**
  (`http://www.w3.org/2000/svg`) — a namespace identifier, never a network request. A naive
  external-URL scan will flag these; they are not external resources. Real external URLs: zero.
- The payloads declare schema `science-visual-learning-payloads.v1`, dated 2026-08-04, and carry
  all **25** lesson IDs — 5 BUILD, 5 GROW, 15 LAUNCH — every one of which resolves to a real file
  in the tree.
- The engine is a dependency-free IIFE exporting `ScienceVisualLearning` on the window object.
- The diagrams are **generated as inline SVG by the engine itself**, so the absent original SVG
  files do not block the visual layer, and no third-party image is involved.

## Why it is mounted nowhere — the blocking finding

**No LAUNCH lesson may mount this toolkit as it currently stands.**

The engine gates the explanation behind the pupil's own writing, for LAUNCH only:

> if the pathway is LAUNCH and the evidence box holds fewer than 8 characters, the explanation
> stays hidden — *"Record a specific observation, value or pattern to unlock the explanation."*

There are two mechanical requirements before a LAUNCH lesson mounts, and the toolkit meets one.

- **Print surface — MET.** The print stylesheet force-shows the hidden explanation and prefixes it
  *"STATIC TEACHER COPY · "*. Teaching content is never gated on paper.
- **Adult route on screen — NOT MET.** There is no staff toggle. The engine's only control is
  `svl-static`, which merely disables animation. Meanwhile the surrounding lesson chassis
  *already has* the right pattern — the exit slide's `👁 Answers (staff)` button toggling a
  `show-ans` class. The toolkit does not use it.

So a LAUNCH pupil who cannot or will not type eight characters — an access barrier, a hand that
will not write today, a refusal — sees no explanation on screen, and no adult can open it for
them. **That is a failing answer on a pupil-facing gate, and a locked explanation withholds
teaching from precisely the pupil least able to unlock it.**

This is a finding, not a failure. The fix is small and belongs to whoever mounts: give the
explanation the chassis staff-toggle so an adult can open it without the pupil having "failed".

BUILD and GROW carry no such lock — the gate is pathway-conditional — but the specimen stage
requires all three pathways green before any batch, so nothing mounts until this is resolved.

## Recorded as evaluated, not adopted

- **No clip is wired.** The supplied media register holds roughly 37 external URLs. None is
  verified, none is embedded, and none is invented. Any register that lands does so as a
  candidate list with prepared slots and a stated platform per entry, for a human's own check.
- **The ESA Paxi material is not adopted** — the pack itself flags it as aimed at ages 6–12
  against a 14–15 cohort. Declined on dignity, not accuracy.
- **No third-party image lands.** Collection-level openness is not an item-level licence.
- **The BUILD nutrition approach is affirmed** — static model, no pupil-facing video, and no
  calorie, weight-loss or restriction language anywhere near the food weeks. The pack reached
  this independently, which authorises nothing but is worth having on the record.
