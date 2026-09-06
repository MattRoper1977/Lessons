# Scrap Core: Expedition SIGNATURE v10 — Target A, P0 only

**P0 is the STOP gate for placement, and it is resolved. P1–P5 are not attempted
in this pass** — see "What is not here".

Baseline reproduced exactly: sha256 `33f1260bcae24e462909ed58049c7fdac57487f9a20214502cce1a1d2ce97608`,
217,715 B, 3,121 lines, 15/15 checksums verify.

```sh
node tools/scrapcore/p0_census.mjs                 # P0.1, writes qa/P0_estate_injection_census.json
node tools/scrapcore/verify_csp_allows_estate.mjs  # P0.3, with its planted failure
```

## P0.1 — what the estate actually injects, measured in a browser

Not from a hand-list and not from the source. The site repo is served over http,
every root game route is loaded in Chromium, and **every request the page makes**
is recorded. "The file contains a script tag" and "the page requests that script"
are different claims; this measures the second.

The route set is **derived** from `data/mbm-search-index.json` — `category ==
"game"` and a root-level route — which is the same record the estate's own
`verify_hud_on_games.py` iterates.

| | |
|---|---|
| root game routes measured | **23** |
| declared unable to carry the HUD (`data/hud-coverage.json`) | 10 |
| **routes shipping their own CSP meta** | **NONE** |
| routes requesting `/hud.js` | **12 of 23** |
| routes requesting `/assets/mbm-profile.js` | 2 |
| routes requesting a vendored `three.min.js` | 3, each its own copy under its own route |
| routes requesting `/theme.js` | **0** — the games family is still unported, confirmed at HEAD |
| **routes requesting NOTHING same-origin** | **11** |

The eleven: `/apexpool/ /apexrally/ /biopunkhive/ /echovault/ /emberwild/
/neonmeridian/ /neonsync/ /novasiege/ /ouroboros/ /rallyvector3d/ /relicforge/`.

## P0.2 — the ruling: KEEP THE CSP AS SHIPPED

Not one directive is widened, because **on this route not one directive has a
measured consumer** — and P0.2 says a directive widened without a named consumer
is a fault, not a fix.

The default repair would have been `script-src 'self' 'unsafe-inline'` to admit
`/hud.js`. The census says that is not the only way to satisfy the estate, and
not the way this estate prefers. `data/hud-coverage.json` documents a generated
**inline exit region**, in as many words:

> No src, no dependency, no request: the single-file promise these games make is
> intact.
>
> …the precedent cited for [amending verifiers to admit `/hud.js`] is
> `/neonbreach/`, whose amendment let in a script that then rendered nothing for
> months and nobody looked.

Eleven routes already take that path. `classify()` in `verify_hud_on_games.py`
has a **third state** for exactly this — added when `/emberwild/` was reported
for carrying neither the script nor a declaration, which was correct and useless:
*"What a player needs is not a particular chip, it is a way out."*

So `/scrapcore/` is declared in `data/hud-coverage.json` with its verifier and
the gate it would otherwise break, and the region is stamped by the estate's own
`tools/render_inline_exit.py` — **never hand-copied**.

**This is not the STOP condition.** The STOP condition is an injection that
cannot be reconciled without weakening a directive beyond its measured consumer.
There is no injection here to reconcile.

## P0.3 — the control, with its planted failure

Served over http from a scratch estate assembled **from the ledger** (the first
cut copied five directories and `render_inline_exit.py` refused, because it
stamps every declared route — the generator being right).

| id | assertion | result |
|---|---|---|
| P0.3a | the estate's own generator stamps the region — 11 targets, 0 divergent, 3,216 bytes | PASS |
| P0.3b | zero `securitypolicyviolation` at boot | PASS |
| P0.3c | the region **executed** — `window.__mbmExit`, its side effect, not its tag | PASS |
| P0.3d | no page errors at boot | PASS |
| P0.3e | zero `securitypolicyviolation` through one live descent | PASS |
| P0.3f | the canvas is painting after the descent — 120,000 lit pixels | PASS |
| **P0.3g** | **PLANTED FAILURE: reinstating `<script src="/hud.js">` is BLOCKED** — `script-src-elem`, `errorText: csp` | **PASS (seen red)** |
| P0.3h | removing it restores a clean run — the gate is not stuck red | PASS |
| P0.2 | the shipped CSP is unchanged: no `'self'` on any directive | PASS |

P0.3g is the assertion that makes the rest mean anything. If the CSP could not
block `/hud.js`, it would not be doing anything and the ruling would be worthless.
It blocks it, visibly, and that is simultaneously the proof that `/hud.js` could
not have been used here without widening.

## What is not here

**P1–P5 are not attempted.** Placement is the larger half of Target A — the save
key rename with a proven migration, the splash, the way home, `og:`/`canonical`,
the route, the ΔE00 hue check against every existing card, the genre argued by
verb, the manifest entry, and the 60→61 card invariant across both audience
pages with a control that moves a genre in a scratch copy.

None of that is half-done here, deliberately. The order's own principle applies:
ending with one thing proven beats ending with six half-proven.

**The curation fence holds regardless**: nothing in this branch touches `TAKES`,
`TOP`, `hero` or any manifest, and no take was written, drafted or improved.
