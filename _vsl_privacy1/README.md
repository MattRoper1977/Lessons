# VSL v0.4-privacy1 — preserved, NOT placed

This directory is **preservation, not deployment**. Nothing here is placed at a
route, linked from a hub, listed in a catalogue or added to `resources.json`,
and this branch is not merged. The leading underscore follows this repo's
convention for directories that are not served (`_close/`, `_semh2/`, `_glv3/`).

It exists because a patched file living only in a disposable container is the
site tag's failure repeated: **a countdown, not preservation.**

## What this is

`Virtual_Science_Laboratory_PRO_v0_4-privacy1.html` — the v0.4 lab with **one
finding fixed**: the pupil's name and reflection notes no longer travel in the
URL.

**It is NOT v0.4.1.** In this estate *v0.4.1* means the patch order ran — P1
through P9, all six V-findings and three N-findings. **Only P2 has run.**
Calling this v0.4.1 would guarantee a future reader concludes V1, V3, V4, V5,
V6 and N1–N3 are fixed when they are not.

## The finding, at its real severity

`syncHash()` has **119 call sites**, and both fields update `state` on every
keystroke. So the moment a pupil typed a name, the next bench interaction wrote
it into `location.hash` — where it stayed for the whole session: browser
history, bookmarks, screen shares, **a projector at the front of an SEMH
classroom**, and any copied URL. **Share was the loudest exit, not the only
one.**

## What changed — three changes, plus version strings

| change | what |
|---|---|
| 1 | `shareableState()`, used **only** by `syncHash()`, deletes `pupil` and `notes` and tags the URL payload `0.4p1`. `serialisableState()` is deliberately untouched — `exportEvidence()` calls it, and the evidence JSON legitimately carries the name because it is a local download named after the pupil. **Private in the URL, present in the local download.** |
| 2 | `loadHash()` deletes `pupil`/`notes` from an incoming payload, so a link minted **before** this patch stops repopulating a pupil identity, and accepts `0.4p1` |
| 3 | the Share toast names the guarantee instead of claiming "resumable" |

The caption *"Name for print/export only"* was **not reworded** — this patch
makes it true. A caption that lies must not survive, and the fix is to make the
code honest rather than the words weaker.

## Gates — 6 reds fired, 7 greens returned

`node v2_gates.mjs <original> <patched> <tmpdir>` — reads `location.hash`,
**never the clipboard**, so a headless clipboard permission cannot fake a pass.

Each red is a **named mutant**: `M0` the original file · `M1` strip inside
`serialisableState()` · `M2` print handler clears notes · `M3` patched without
change 2 · `M4` a corrupted token.

> The order proposed *"strip from `serialisableState()` instead"* as the red for
> both the export and print gates. **It does not fire for print** —
> `preparePrint()` reads `state.notes` directly and never goes through
> `serialisableState()`, so that mutant leaves the print gate green. A control
> that cannot fire is not a control, so print got `M2` of its own.

Gate **A** is the one that never touches Share: type both canaries, perform an
ordinary bench interaction, read the hash. That is the gate matching the actual
finding.

## Accepted costs, named not hidden

- **A reload now loses the typed name and notes.** This file has **zero storage
  APIs** and the URL was the only persistence. Storage was deliberately **not**
  added: on a shared classroom machine `localStorage` would leave a pupil's name
  for whoever sits down next — arguably worse than the address bar — and it
  breaks a declared property other checks rely on. **Print or Export before
  reloading**; both still carry the fields.
- **P2 is half-implemented.** `phaseAnswers` and drawing strokes are still in the
  URL payload. Same principle, lower severity — they are not identifying — and
  stripping strokes makes the reload cost far worse: a lost drawing is lost
  work, a lost name is one retype. Their own change.
- **Residue that cannot be fixed:** links already minted, bookmarks already
  saved and screenshots already taken are **unrecoverable**. This stops new
  ones; it does not reach the old ones.

## Measurements

| | v0.4 (pinned input) | v0.4-privacy1 |
|---|---|---|
| bytes | 287,161 | 290,034 |
| lines | 1,978 | 2,031 |
| sha256 | `137bbfac3ea98255fad55b44c3073810d2a0876cc833e555b61f6989114daf7f` | `2004d374b8215227ade8596261ac76f420b92c726d86ff3230a9b66f25f3a701` |
| benches | 13 | 13 |
| page errors, 13/13 benches | 0 | 0 |

The input set is **not replaced** — it stays pinned as the subject this was
derived from.

## Still not deployable

**V1** still rewards the procedure it teaches against. **V5** still marks *"the
glowing splint does not relight"* as correct. **N1** still deletes a pupil's
oldest drawing stroke without a word. Placement, when it happens, is still
**unlinked until Matt's paper read** — no instrument can witness a paper read.
