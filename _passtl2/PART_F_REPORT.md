# TL-2 Part F — NEON RIFT: AFTERDARK // Resonance Protocol: vendored, conformed, DEPLOYED (unlisted)

Sentinel: `townlife-tl2-2026-08-18-PARTF-TOP`

## Identity gate (F1)

Source zip `NEON_RIFT_AFTERDARK_RESONANCE_PROTOCOL_PRO_v2_0_0_2026-08-15.zip` **925,265 B, sha256
`706b337b2165207ba249c6123ea7fef092efbecccd43b58519030dafadff587a`** — exact. Inner HTML both copies
**170,695 B, `0fbbad3c3e74ab8d2bb9379bd9875fa97deb80c2ac767093dec71d4aac290f8e`** — the pinned
identity. Zip's own SHA256SUMS 26/26 OK.

## What shipped (Games PR #38 → merged)

Branch `tl2-afterdark-vendor-touch` (head `6f9bfe83`), **merged to Games main
`52fa624a1b6dfdb64dfeae559b1f4900f1f74520`**. 15 files: `afterdark/index.html` (185,974 B, sha256
`9c491a6f86ff9451e33127c272b9022ffccab3180b59e60960bd6257ef5a34d8`, from pristine 0fbbad3c/170,695 B)
plus `afterdark/vendor/three-0.185.1/` (three.module.js + three.core.js + 10 addon files by import-graph
closure + MIT LICENSE + VENDOR_SHA256SUMS.txt with per-file fetch hashes). Zero check runs fired on
the PR — no path-filtered workflow in the Games repo covers `/afterdark/**` (recorded, not assumed).

All eight pinned findings (F1–F8) were reproduced RED on the pristine file in a real-Chromium
harness before any edit, then fixed and proven green; the PR description enumerates each red→green.
Highlights: vendored offline boot proven with network denied AND a pristine-FAIL control; single
pointer-lock handler + key flush (blur/hidden/lock-loss/pointercancel); `mbm_afterdark_settings_v1`
+ one-time legacy migration with sibling isolation; OS reduced-motion floor + live listener gating
the WebGL bloom; context-lost pause/restore; canonical/og/noscript + estate ma-splash (pointer-UP +
400 ms arm) + `/hud.js` + "Made by Matt"; CDN watchdog copy → generic fallback.

**Touch layer shipped behind the Settings override, default OFF** — the contingency the addendum
authorises: the ≥30 fps @ 4×-throttle 390×844 LITE gate measured **6.3 fps in the SwiftShader
software-render harness**, an honest red (the harness has no GPU; the real-device verdict is Matt's
phone check). Coarse-pointer devices get an honest "best played with keyboard + mouse" notice and
LITE defaults; rendered 44 px census at 390×844: **0 under-floor** (keyed to `body.coarse-input` so
the Settings path itself is tappable). Worst-4 s flash window: **0 luminance transitions >10%**
(9-sample method, software renderer — method recorded).

## Register census (report-only; owner ruled PUPILS = yes)

Player-visible: ELIMS ×2 · ALIVE ×2 · "You were eliminated by …" ×1 · damage · weapon names
PULSE AR / SCATTER / LONGSHOT / NOVA / SHIELD · "hip fire". Internal only: `killFeed` ×23 ·
`score.kills` ×4 · damageByWeapon · weaponName. Zero blood/death/gore strings. **Ships as-is** — the
owner's swap line (`Afterdark register: ELIMS→OUTS, eliminated→knocked out — go`) was not received.

## P5 listing surfaces — HELD: `PARTF_WAITING_ON_B`

Site PR #169 is unmerged and B is not parked, so per the addendum the route **deployed unlisted**:
no `games.json` entry, no `/games/` shelf edit, no `/for/pupils/` edit, no catalogue/search entry,
TOP rail untouched, NEW· holder untouched. The genre (Action & Survival), feels (fast + long-haul),
derived-count shelf/pupil edits and the cross-page count control all follow in a separate PR once
#169 merges or B is parked.

## P6 close — deployment proof (this session's reachability limits declared)

- `pages build and deployment` run **32177423202** at head `52fa624a…`: **success** — the route
  `https://madebymatt.uk/Games/afterdark/` is deployed from the merged bytes.
- Repo truth at the merge SHA proven via raw.githubusercontent (reachable): `afterdark/index.html`,
  `three.module.js`, `three.core.js`, `LICENSE` all hash-match the merged tree exactly.
- **Live-route browser boot: LIMITED** — madebymatt.uk AND mattroper1977.github.io are both
  proxy-blocked from this session (CONNECT 403), so the first in-the-wild WebGL boot cannot run
  here. Compensating evidence: the vendored build booted on real Chromium over HTTP from the same
  bytes (frames advancing, zero fatal errors, pristine control fails identically), and Pages
  deployed those exact bytes. Matt's phone opens the real route (checklist below).

## PHONE_CHECKLIST (for Matt)

1. Open `https://madebymatt.uk/Games/afterdark/` (unlisted — type the URL). Expect the Made-by-Matt
   splash, then the START card; no "local server" message may appear at any point.
2. Tap once anywhere → audio unlocks. On a phone you should see the notice that the game is best
   with keyboard + mouse, and LITE quality defaults.
3. Settings → **Touch controls → On** → start a match: left thumb = move stick, right side =
   look-drag; FIRE/JUMP/SLIDE/USE/RELOAD/BUILD buttons and weapon slots visible; COMBAT/BUILD HUD
   toggles. Report the fps chip reading after ~60 s of play — that number decides whether touch
   comes out from behind the override.
4. Rotate/lock the phone, background the tab and return: no stuck movement (key flush), the match
   pauses on context loss and resumes.
5. Chromebook note (mandatory before any pupil use in class, same as Town Life): repeat 1–4 on a
   school Chromebook; the 6× throttled proxy measured 5.17–7.11 fps on Town Life-class devices, so
   an honest fps reading matters here too.

## Tokens and holds

- `PARTF_WAITING_ON_B` — listing surfaces held (shelf, pupil page, catalogue, genre counts).
- `AFTERDARK_VENDORED_TOUCH_PUBLISHED_SHA_PROVEN` is **NOT emitted**: the route is deployed and
  byte-proven at the merge SHA, but the addendum's token covers the fully-published state (listing
  surfaces + live boot), which waits on B and on Matt's phone check.

Sentinel: `townlife-tl2-2026-08-18-PARTF-BOTTOM`
