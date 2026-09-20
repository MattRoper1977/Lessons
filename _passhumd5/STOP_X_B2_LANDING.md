# STOP-X — B2's landing target does not exist

B2: *"per pack, ≤12-file PRs against the served routes, upgrades in place, live wins
on furniture/nav/tokens."* Measured against the estate, that shape has no target.
This is STOP-X as the order defines it: a ruling genuinely absent. Nothing has been
written to any served route.

## Measurement 1 — the packs are not repository content

The 13 HUM-D5 packs arrived as ZIPs (`HUM_Autumn_1_LAUNCH_Final`, `RE_Autumn_BUILD_Final`,
…). **0 files matching those pack names are tracked in the Lessons repo.** The
Humanities packs that ARE published there are a different series entirely —
`Humanities_Teesside/Teaching_Packs/{BUILD,GROW,LAUNCH}/downloads/*_Humanities_Autumn1_W3-W7_*.zip`.
So there is no repository path for a pack file to be PR'd to.

## Measurement 2 — no served file can carry a D1 or D2 change

The proof pass lives in exactly three pack file types, and B1 applied it there:

| file type | copies | carries |
|---|---:|---|
| `*_Lesson.html` | 120 | D2 — the `.step-ribbon` colour token |
| `*_Pupil_Resources.html` | 33 | D1 limb (a) — the media credit under the Visual resource |
| `Sources_and_checks.html` | 117 | D1 limb (b) — the fenced media review rows |

Across **all 185 tracked `Humanities_Teesside/**.html`**:

| what D1/D2 edits | files that carry it |
|---|---:|
| `.step-ribbon` | **0 of 185** |
| `<h2>Visual resource</h2>` | **0 of 185** |
| a Sources-and-checks table | **0 of 185** |

There is no served file that either ruling can touch.

## Measurement 3 — the two populations are different chassis, and the estate's own precedent says so

Over the 38 pairs whose destination three independent instruments confirm:

| | pack lesson | served lesson |
|---|---|---|
| bytes | 670,922 – 1,159,113 (median 832,066) | 31,748 – 139,228 (median 47,949) |
| chassis marker | `window.CLASSIC_LESSON` 38/38 | `script#lesson-config` 29/38; `CLASSIC_LESSON` 1/38 |
| `<dialog>` | 6 on every one | 0 to 5 |
| `.step-ribbon` | 1 to 3 | **0 on every one** |

Median size ratio **16.3×**; stage counts differ on 9 of the 38.

The decisive precedent is the order's own held set. The **14 Fallback lessons are
already served from the pack** (generation `fallback-2026-09-19`). They are served at
69–98 KB with `script#lesson-config`, and **0 of the 14 carry a ribbon, a Visual
resource section or a Sources-and-checks table.** So when a pack lesson is published
to a served route, the served form is a generated, much smaller artefact that drops
every structure D1 and D2 change. That is not a hypothesis about what would happen —
it is what did happen, on the 14 the order named.

## What follows

Neither reading of B2 delivers the pass:

- **live shell wins** → the pack's HUM-D5 features have nowhere to go; D2 lands on 0
  of 185 files and D1 on 0 of 185. The proof pass delivers nothing.
- **pack lesson wins** → a 48 KB classroom lesson is replaced by an 832 KB deck. That
  is a substitution, not an upgrade, and it contradicts "live wins on furniture, nav
  and tokens".

The order assumed the packs and the served routes are two generations of one artefact,
as they are for science. For Humanities they are not. Where the pass should be
published — the packs as a download series, a served-form regeneration, or a widened
served chassis that can carry a ribbon — is a ruling, not a measurement.

## What is NOT blocked by this

- B1 is applied, proved and committed: D1 and D2 are in the workspace packs, 1605
  checksum entries 0 FAIL, 22 PDFs re-rendered, changelogs written.
- D2 is fully proved, and on the printed page it fixed something worse than the
  ruling named — see `D2_PROOF.md`.
- The four contested BUILD Autumn-2 destinations are recorded in
  `PAIRING_DERIVATION.md` and are a separate ruling.
- **SX3-FU1 is unaffected.** F2 is applied, proved and committed on
  `claude/sx3-fu1-arrival-split`; the science estate is repository content and its
  landing route is the established one.
