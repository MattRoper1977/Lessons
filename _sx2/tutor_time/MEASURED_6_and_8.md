# §6 architecture and §8 gates, re-measured

ORDER LF1-M §6 and §8. Measured on the uploads before anything lands; §8c's
re-measurement on the served routes comes after landing and is a separate pass.

**Population.** The order measures 29 per-deck files (17 originals + 12 batch) and
7 collections. `Safeguarding_Assemblies_Part_2.zip` **is** in the upload set, so the
real population is **42 decks** (21 originals + 21 batch) and **8 collections**
(batch 02's lives inside its zip rather than as a loose upload). Every figure below
is on 42/8, which is why some totals are larger than the order's — the denominator
moved, not the property.

---

## §8a — must be zero

| | order | measured, 42 decks | |
|---|---|---:|---|
| `<script src>` | 0 | **0** | ✅ |
| `localStorage` · `sessionStorage` · `indexedDB` | 0 | **0** | ✅ |
| `<input>` | 0 | **0** | ✅ |
| `<textarea>` | 0 | **0** | ✅ |
| duplicate ids | 0 | **0** | ✅ |
| Progress Schools branding | 0 | **0** | ✅ |
| `<iframe>` per deck | 0 | **0** | ✅ |
| **YouTube** | **0** | **2** | ⚠ see below |

**Must be present, decks missing it:** `prefers-reduced-motion` **0**, print route
**0**, Made by Matt **0**. All 42 carry all three.

**Deck sizes: 36,564 – 46,569 bytes — the order's figures exactly**, across 42 files
rather than 29. (Read the files in text mode and you get 36,456–46,367; the
difference is CRLF collapsing, not content. Size claims are measured on bytes.)

**Collections:** master **1,001,160**; batch 01 145,088 · 03 149,963 · 04 **149,293**
· 05 **152,928** · 06 **154,770** · 07 **149,783**. Every figure the order states is
reproduced. Exactly **1 iframe per collection**, the §6c viewer.

### The two YouTube hits

Both are in **`V08_Belonging_Without_Assumptions`** (batch 01, one of the four new
sessions cleared to land under §5), and both are the same claim — once in visible
prose, once in the `DATA` payload:

> *Official KS3/KS4 resource and teacher guidance rechecked 9 September 2026. Full
> film: `https://www.youtube.com/watch?v=jUg8ue5_vvA` (3:22 in guidance). Stream and
> captions not checked.*

**It is a URL in text, not an embed.** There is no iframe, no `<script src>`, nothing
that loads YouTube — so §8a's *intent* holds and the "0 YouTube" figure is right
about embedding. But a youtube.com URL does render on a pupil-facing surface of a
session that is otherwise cleared to land, and the order's own §5 clearance was
written without it. **Flagged, not changed.**

---

## §6a — the pack-link

`><a class="pack-link" href="../../START_HERE.html">Back to pack menu</a` appears
**exactly once in every one of the 42 decks**, 42 occurrences in total. It is a ZIP
artefact and dangles at a live route. Strip at deploy, replace with estate back-link
furniture per NAV-1; `START_HERE.html` is a pack artefact and goes to `_authoring`.

**Proof obligation on landing:** 0 occurrences of `START_HERE` across all served
`Tutor_Time/` routes.

## §6b — the second copy

**42 of 42 payloads equal their per-deck file minus the pack-link, delta 71 bytes,
every time, across all 8 collections.** No exceptions.

| collection | payloads | byte-equal |
|---|---:|---:|
| master `Interactive_Assembly_Collection` | 21 | **21** |
| batch 01 · 02 · 03 · 04 · 05 · 06 · 07 | 3 each | **3 each** |

The duplication is faithful today and will drift tomorrow, so the ruling stands: the
per-route file is canonical, collections are **regenerated** from the post-strip route
files and never hand-edited, and a payload that does not match its route file byte
for byte after furniture injection is a blocker.

*(One trap worth recording: originals and re-cuts share basenames — `B02_Ready_
Respectful_Safe.html` exists in both the originals pack and batch 02. A lookup keyed
on basename alone silently compares a batch payload against the original deck and
reports 17 of 42 mismatching. The comparison has to be scoped to the package the
collection came from.)*

## §6c — the viewer is opaque-origin

All 8 collections carry the identical sandbox:

```
sandbox="allow-scripts allow-popups allow-popups-to-escape-sandbox allow-modals"
```

**`allow-same-origin` absent in all 8** (correct — storage inside would throw, and the
decks use none). **`allow-modals` present in all 8** (correct — the print route depends
on it). Do not add the first; do not remove the second.

**Proof obligation on landing:** open a session in the viewer on the *served*
collection and confirm a dialog. Markup that exists but is inert inside the sandbox
does not satisfy the gate.

## §6d — staff blocks

One `<aside class="staff" id="staff" hidden>` per deck, holding **three** labelled
paragraphs — `Before delivery:`, `Sensitivity:`, `Delivery:` — plus one visible
control `<button id="staff-toggle" aria-expanded="false">Teacher notes</button>`.

**42 of 42 decks match that shape exactly**: 42 asides, 126 paragraphs, 42 toggles, no
exceptions. The order's "class=staff ×3" is the three paragraphs inside the one
aside, not three elements. Hidden by default; bind both to the estate guide toggle
(ECA-1).

**The `Delivery:` paragraph is `staff.delivery`** — the field the re-cut build
overwrites. That is what makes the §4 finding a teaching problem rather than a
bookkeeping one.

## §6e — duplicate uploads

Every duplicate is md5-identical, including the four zips that arrived twice, the
collection that arrived five times, and the second tranche of originals packs. One
file each; never land two.

## §6f — dated claims

23 dated source claims across the batch decks, registered in `SOURCE_REGISTER.md`
with a **recheck-before** date taken from each batch slot. The one the order
predicted is real: **V07's Representation of the People Bill claim is checked
9 September against a 2 November slot**, with a second reading on 14 September —
seven weeks stale on the day it is taught. Not changed: the deck already tells the
teacher to check current eligibility, and an honestly labelled dated claim is not a
defect.
