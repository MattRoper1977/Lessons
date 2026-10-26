# Art Visual Learning Layer v1.0 — recovered toolkit

**Status: MOUNTED ON THREE SPECIMEN LESSONS** (Stage B), one per pathway:
`BUILD_ART_W3_Industrial_Surface_Skills_Lab` · `GROW_ART_W3_Independent_Studio_Challenge` ·
`LAUNCH_ART_W3_Implement_and_Critically_Develop`. The remaining 28 decks are untouched.

Sentinel: `art-visual-learning-2026-08-05`

## Stage B — what changed in the engine, and why

Four changes, all in `art-visual-learning.js`. Everything else remains as recovered.

1. **The LAUNCH explanation lock is fixed (§5.1).** `refreshExplanation` now consults
   `staffAnswersShown()`, which reads the chassis organ already in every deck: `.show-ans` on
   `#exit-slide`. A `MutationObserver` re-checks it whenever staff toggle it, so the reveal is
   live rather than only correct at mount time. **No second toggle concept was invented and no
   new adult control was added** — the explanation simply follows the `👁️ Answers` button the
   decks already have. When the staff route opens it, `artOpenedBy` records `'staff answer
   reveal'` rather than claiming the pupil produced evidence.

   Verified in a real browser on all three specimens, and — critically — **verified against the
   pre-fix engine, where the same test leaves the explanation hidden.** The test can fail, so the
   pass means something.

   **The 8-character threshold was not changed.** It remains a design question for pupils with
   writing difficulty.

2. **The clipboard capability ships disabled (ruled 2026-08-05).** As recovered, the panel called
   `navigator.clipboard.writeText` and fell back to `document.execCommand('copy')`. Both write to
   the pupil's clipboard. **Neither remains.** The button now shows the note in a read-only
   textarea with the text pre-selected, and the pupil copies it themselves with their own
   keystroke. Code-only search (comments stripped) reports `navigator.clipboard` 0, `execCommand`
   0, `writeText` 0. Do not reintroduce a programmatic clipboard write without a fresh ruling.

3. **The transfer task is declared not-evidence (ruled 2026-08-05).** The panel now states in
   plain words: *"This is a teaching activity, not Arts Award evidence. Nothing here goes in the
   portfolio — record evidence on the weekly evidence pack as usual."* The portfolio of record
   remains the weekly evidence pack. This panel is not a third portfolio.

4. **The reduced-motion listener is fixed.** `reducedMotion` was computed once at load with no
   `change` listener, so an OS preference changed mid-session was never honoured in JS. The media
   query is now watched and `isStatic()` reads the live value.

### How mounting works

Each lesson carries an authored loader inside an owned `AVL-MOUNT:BEGIN`/`AVL-MOUNT:END` comment
pair, immediately before `</body>`. **Authored per file and gated per file — no bulk injector.**
Everything outside the marker pair is byte-for-byte identical to HEAD, checked per file against a
control that detects a single-character tamper.

The engine finds its lesson by filename and mounts into the `We Do 1` slide.

### Two pre-existing conditions, neither caused by the mount

Both were isolated by loading the deck at HEAD, unmounted, and observing identical behaviour:

- Toggling the staff answers organ on the exit slide also triggers the chassis lesson-complete
  overlay and confetti. Staff revealing answers will see the celebration. **Pre-existing.**
- The CSS ids `#cold-call-btn` and `#ta-focus-btn` are styled but never applied to any element.
  The Cold Call and TA Brief organs are real and present — they are plain `<button>` elements —
  so these are vestigial selectors, not missing organs. **Pre-existing, cosmetic.**

---

## What these files are

| File | Bytes | SHA-256 | Origin |
|---|---|---|---|
| `art-visual-learning.css` | 16,977 | `0685aa7cc170f17b5bc809c4a0b3ead80892177185615f85ed2c39f227b34252` | `<style>` block [0] of the vendor demo |
| `art-visual-payloads.js` | 45,445 | `e3efa5a8d1abeb7ed0357f88caa4f90dab38d39294cf3cb05cce997b533526ae` | `<script>` block [0] — `window.ArtVisualPayloads` |
| `art-visual-learning.js` | 75,820 | `f0db9ae1320bcec0624e735ba0b517cfc0f16ae874ad7e70472bd9523922b6e2` | `<script>` block [1] — engine IIFE, exports `window.ArtVisualLearning` |

All three were **extracted byte-for-byte** from `Art_Visual_Learning_Demo.html` (147,045 b) and
verified by `cmp` read-back against the source blocks after writing. **No line was
prose-reconstructed.** Two further blocks in the demo — 841 b of demo chrome CSS and a 727 b demo
bootstrap — were deliberately discarded as demo-only.

`_meta` in the payloads reads: version `1.0.0` · prepared `2026-08-05` · baseline `067c76a4…` ·
principle *"Notice or predict → manipulate → freeze → name evidence → explain → transfer"* ·
contentRule *"Add-only visual teaching; preserve authored lesson wording, Arts Award evidence and
studio constraints."*

The "15 original SVG teaching resources" are **not files.** They are inline SVG built by the engine
at runtime. They arrived with the engine and need no separate extraction.

## What was NOT recovered, and is not reconstructable

Matt holds a 12-file re-compressed subset of the vendor pack. These parts of the original pack are
**absent** and have deliberately **not** been simulated, reconstructed or stubbed:

- both `.patch` files
- the entire `repo-overlay/Art_Teesside/visual-learning/` tree
- `inject.py`, `check.py`, `build_payloads.py`
- the canonical `lesson-payloads.json` (the payloads here are the *generated* form)
- the 15 SVGs as standalone files
- the file-integrity manifest and the ZIP checksum file

Because `build_payloads.py` and `lesson-payloads.json` are both absent, `art-visual-payloads.js`
is currently a **source file, not a build artefact.** Its header comment still says "Generated from
lesson-payloads.json; edit the JSON, then run build_payloads.py." That instruction cannot be
followed in this repo. Edit the `.js` directly, or re-establish the JSON + builder first.

## There is no provenance gate. Do not claim one.

The vendor summary quotes SHA-256 `f022ddf576edf34d88775fdfa5dcf5bc0b573062912768ff8bcfc4b1a375c1c7`
for its original ZIP. The archive Matt holds is a re-compression:
`f9a198c8cc0b7d2a92f392387d727d4bebfb6fc493b4ff5c875267024451866b`. The mismatch is **expected and
proves nothing in either direction.** There is no manifest to check the members against.

**Absence of a mismatch is not evidence of integrity.** The checksums in the table above establish
only that what is committed here matches what was extracted from the demo Matt holds — they say
nothing about whether that demo is what the vendor built. Nothing in this directory is
provenance-verified.

## The pinned baseline is stale

The pack pins itself to `067c76a4407ce0991eca10aca67e3f526f425ce1`. At the time of this commit that
commit is **still an ancestor of `main`, but `main` is 7 commits ahead of it.** The pinned patches
were never applied and were never reconstructed (they are absent, see above). Nothing here depends
on the pin.

## BLOCKING: the LAUNCH explanation lock (§5.1)

**This toolkit must not be mounted on any LAUNCH lesson in its current state.**

The engine gates the teaching explanation behind a typed evidence note, on LAUNCH only:

```js
var evidenceReady = !ctx.evidenceInput || ctx.evidenceInput.value.trim().length >= 8;
if (ctx.pathway === 'LAUNCH' && !evidenceReady) { ctx.explanation.hidden = true; ... }
```

The textarea also ships `disabled: true` and is enabled only by `complete(ctx)`. So a LAUNCH pupil
must finish the activity **and then type eight characters** before the teaching explanation appears.
All 8 `evidencePrompt` fields sit on all 8 LAUNCH lessons — verified in this repo.

There is **no adult override on screen.** The engine contains zero occurrences of `staff`,
`teacher`, `Answers`, `override` or `revealAll`. The `avl-static` toggle switches animation only.

This is the **same defect already recorded against the science sibling as open-item 37**, where it
forced that pack to close mounted-nowhere.

**Print is not affected.** `@media print` force-shows the explanation with a `"STATIC TEACHER COPY · "`
prefix. The defect is on screen only.

### The fix is specified and wirable

Every one of the 31 target decks already carries the chassis staff-answer organ — a button toggling
`.show-ans` on `#exit-slide`. Verified present in **31 of 31**. The reveal must be wired to that
existing organ: same pattern, same vocabulary, no second toggle concept and no new adult control
invented.

Note for whoever builds it: the organ's literal label is `👁️ Answers`, **not** `👁 Answers (staff)`.
A search for the latter returns zero. The emoji also carries a variation selector (U+FE0F). Search
for `show-ans` instead.

**The 8-character threshold is not ruled** and must not be changed without Matt's decision.

## Open rulings required before any mount

1. **Clipboard capability.** The engine calls `navigator.clipboard.writeText`, guarded by
   `isSecureContext` with a manual-selection fallback, to copy a pupil's own evidence note. It
   writes nothing to disk and sends nothing, but it touches the pupil's clipboard — a device
   capability the science sibling did not have. **It ships disabled unless Matt rules otherwise.**
   Inert at present because nothing loads the engine.
2. **The award-blind transfer task.** Each activity ends in an "independent transfer task" carrying
   **no Arts Award Part tag at all.** There are already two print routes — the weekly evidence pack
   (the declared portfolio of record) and the in-lesson print sections. This would be a third
   surface. It must either route explicitly into the existing weekly sheet, or the panel must say in
   plain words that it is a teaching activity and not evidence. It must not become a third portfolio
   by drift.
3. **`innerHTML` sink.** One occurrence, reachable only via an `el()` helper on a `html:` key. **No
   payload uses that key** (0 occurrences). The sink exists and is unfed. Either remove the branch or
   record it as a deliberate unused affordance.
4. **Reduced-motion listener.** `reducedMotion` is computed **once at module top level** with no
   `change` listener, so an OS preference changed mid-session is not honoured in JS. The blanket CSS
   rule still applies, so this is a degradation, not a failure. Left as recovered; fix before mount.

## Runtime safety, as measured from these exact files

`localStorage` 0 · `sessionStorage` 0 · `indexedDB` 0 · `fetch(` 0 · `XMLHttpRequest` 0 · `eval(` 0 ·
`new Function` 0 · `document.write` 0 · `cookie` 0 · `postMessage` 0 · `WebSocket` 0 · `<form` 0.

External URLs: **3, all `http://www.w3.org/2000/svg` namespace declarations.** No network requests.

Each of those zeros was replayed against a control file that must return non-zero, and did.

`data-art-opened-by` is real: the engine sets `dataset.artOpenedBy` on the explanation node. It is
**temporary interface state — not stored, not transmitted, never Arts Award evidence.** The
textarea's own helper text says so: *"This note stays in this page only. Nothing is saved or sent."*

## Absent-kit check (standing rule 15)

There is no press, no rollers, no screens, no squeegees, no block or screen inks and no dyes at this
setting. Both numbers are recorded so the next reader cannot repeat a crude search:

| Term | Substring | Word-boundary |
|---|---|---|
| `press` | 49 | **0** (all `pressure`) |
| `etch` | 14 | **0** (all `sketch` / `stretch`) |
| `print` | 1 | **1** — `@media print`, a CSS at-rule, not kit |
| `ink` | 11 | **3** — all `--avl-ink`, a CSS colour token, not kit |
| `presses` `roller` `brayer` `squeegee` `screenprint` `lino` `drypoint` `printing` `dye` `inking` | 0 | **0** |

**The toolkit is clean on kit.** The two non-zeros are adjudicated above and neither is printmaking
vocabulary. Note that `--avl-ink` will make a future crude `grep -ow ink` over the estate return a
false positive; it is a CSS custom property name and is never pupil-visible.

`registration` (12) and `edition` (9) were adjudicated separately: both are **native**. `registration`
already appears at HEAD in the Autumn 2 decks in exactly the layer-alignment sense — *"Lining a
stencil up the same way each time"*, *"registration jig"* — and `BUILD_ART_A2_W6_Resolve_and_Edition`
exists. Neither is new technique vocabulary.

## Estate locks, as measured from these exact files

`AO1` `AO2` `AO3` `AO4` `GCSE` `grade band` `guided learning` `GLH` `TQT` `hours` — **all 0.**
`Explore` `Bronze` `Silver` `Part A`–`Part D` `Unit` `adviser` `moderator` `Artsmark` — **all 0.**

Arts Award only. Tiers are Supported / Standard / Stretch. **Never add an hours threshold at any
level.**

## Scope, when this is eventually mounted

Target set is the **31 pupil-facing lesson decks**, derived — not inherited — as *"an Art_Teesside
HTML file that requests `/hud.js`"*. That set is exactly 31 of the 53 Art_Teesside HTML files, and it
is **identical, one for one, to the 31 lesson IDs in the payloads.** The 22 files it excludes are
precisely the hubs, schemes of work, printable evidence packs, House Standard & Safety and the Arts
Partnership Log — every one of which must receive **no panels.**

Mounting is **authored per file and gated per file.** No bulk injector. `/hud.js` itself lives at the
site repo root and 404s when Lessons is served alone locally — that is neither a defect nor fixable
here. Do not "fix" it.
