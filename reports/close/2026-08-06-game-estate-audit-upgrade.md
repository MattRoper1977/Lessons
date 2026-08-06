# Game estate audit + upgrade sitting — 6 August 2026

For a reader with no context. Every figure below was derived in this session at
the SHAs named; nothing is quoted from the brief as fact.

## §0 · Gate, capability, base

**The audit pack did not arrive.** The sitting's brief pinned
`madebymatt-game-audit-pack-2026-08-06.zip` (sha `a75fce78…`) as its one needed
attachment; the only zip present was the previous day's estate-review bundle
(sha `14780c64…`). Per the brief's own park discipline the session continued on
repo-derived truth: the pack's tools, fixtures, evidence CSVs and checklist
template were all unavailable, and everything below was derived fresh at tip.
Pack-dependent items are named as parked at the end.

**Heads at open**, via `ls-remote`, never `branch -r` on a shallow clone:

| repo | expected minimum | derived | verdict |
|---|---|---|---|
| Lessons | `e214926` | `e214926` | exact |
| Games | `0fc29d5` | `919f4a2` | moved — the PR18/19 marker sitting closed (addendum state, verified: sole `NEW · ` holder Echo Vault, 41 entries, zero desc holders) |
| site | `878d54f` | `878d54f` | exact |

**Capability.** Chromium: launch-proven. **WebKit: NOT RUN** — no binary, and
the install attempt fails at download through the container proxy (derived, not
assumed). Live `madebymatt.uk`: unreachable from the container (403 on
CONNECT). npm registry: reachable (proxy-exempt), which is what made Band 2a
possible.

**Census.** Games repo: 0 open PRs. Lessons: 8 open (HELD/agent/retrospective —
none touched). Site: 1 open (#25, HOLD — untouched, and its diff touches no
game file). No in-flight branch touched `games.json` / shelf / homepage
surfaces, so nothing here parked on sequencing. **The Games repo was read-only
this session and stayed that way.**

## §2 · Dedicated verifiers, all discovered and run at tip

**Lessons (3 + inner harness): all green.** Off-Brand, Charcoal shell gates;
Axiom Shift shell + node harness — 69 assertions, max flash 2.600 Hz.

**Games (4): all green at `919f4a2`** (run this session: sports rail 6/6 incl.
S6 positive control, Echo Vault 20/20, Relicforge 20/20, canonical manifest
validator PASS at 41).

**Site (31): 28 green once given their real inputs; 3 red with named causes.**
The reds were each investigated, none weakened:

- `verify_apexkick.js` 24/25 — **gate over-broad**: its "no remote resources"
  matcher counts `rel=canonical` / `og:*` / `twitter:image` metadata, which
  browsers never fetch. The game is runtime-clean (12/12 matrix cells, incl.
  blocked network). No CI workflow wires this gate. Instrument correction
  candidate.
- `verify_arcade_sports_browser.js` 23/28 — **gate stale**: written against the
  four-game Sports rail; the rail legitimately grew to five (Apex Rally,
  Games PR #15). The current-generation surfaces gates own this contract and
  pass against the 41-entry manifest.
- `verify_apextennis_browser.js` — **environment**: a 32 ms frame-budget gate
  cannot be attested in a shared container (1 frame at 33.3 ms even idle);
  its own workflow last ran **green on runner hardware 2026-08-04**.
- Also environmental, resolved by supplying inputs: the three `*_surfaces`
  gates (needed `GAMES_MANIFEST` / a served shelf; **6/6, 6/6, 5/5 green**
  against the local root + current manifest), `verify_home_doors_baseline`
  (needs its site.json argument; green + self-test), the two `*_home_browser`
  gates (48/49 runnable-green; the 49th needs a CI-produced baseline artifact
  and honestly reports NOT RUN rather than passing). `verify_surfaces.js`
  needs the live origin: **NOT RUN** from this container; the live site was
  proven byte-identical to Games main with a full browser render on
  2026-08-06 by the previous sitting's runner workflow.

**Version-pin trip hazards for any future version bump** (§2.2 duty): Off-Brand's
gate anchors `GAME_VERSION='[digit]` — **not** `'3.`-pinned as the brief warned,
so a major bump does not break it. Axiom Shift's gate states in its own header
it is not version-pinned. No gate found that a version bump would snap.

## §3 · The matrix

**516 cells: 43 targets** (41 shelf + `Voxel_Frontier.html` + `Orbital_source.html`)
× desktop / 390×844 portrait / 844×390 landscape × reduced-motion on/off ×
online / fully-blocked network. Chromium only (WebKit NOT RUN, above).

- **Zero load failures. One game with page errors**: Neon Snake Overdrive,
  `THREE is not defined` — in *both* network states, because the container
  proxy blocks cdnjs even "online". Container-online ≠ real-online for every
  CDN game; labelled throughout, never conflated.
- **The seven CDN-runtime games were menu-only shells on any blocked network**
  — loaded, showed their start screen, could never begin a run.
- Overflows, responsible element named: Slipstream desktop 474–1050px
  (`div.archlab`); Trail Runner + Trekkers 2px portrait (`#instructions-box`);
  Wrecking Crew 2px portrait (title `h1`, first attributed to a `position:fixed`
  nudge — a mis-attribution the fix pass caught, since fixed boxes never grow
  the document).
- Unnamed controls at tip: `seed-input` ×7 games (+1 secondary), `ghost-paste`
  ×2, NSO `initials`, One Guy `codeIn`. The brief's "four one-unnamed-control
  games" list was stale in both directions and was re-derived.
- **The Last Lighthouse: no freeze.** Its dedicated boot route (primer dialog →
  start screen → FREE and GUIDED watches) reached 150+ frames, canvas
  advancing, zero uncaught errors, on both routes. `toggleDOMClass` does not
  appear in the published file. Verdict: the described freeze belongs to a
  draft that never shipped. The brief's "highest-priority Band-2 repair" was
  NOT NEEDED.
- Touch-target census (rendered, portrait) recorded for the run: smallest
  targets include 12px footer links (Apex Kick/Tennis, Medevac, Voxel
  Frontier), Lighthouse's deliberate quiet `resetFiresBtn`, and the ~34px
  `mbmhud-back` chip across most Lessons games. Census only — no repairs
  attempted this sitting.

## §4 · What landed (Lessons PRs #74–#77, all merged on green)

**#74 Band 1** (`5f991ae`) — remote fonts out of 15 games (all had system
fallback stacks; `Slipstream_GP.html` exempt under its red line, exemption
encoded by name in the gate); 5 raw markup `&` → `&amp;` in 3 games
(script-body `&` untouched — the scanner parses markup context); 11
placeholder-only inputs named across 9 games; the three 2px portrait overflows
fixed at the responsible element. *Deviation recorded: the brief wanted one PR
per family; the four mechanical families landed as one PR with per-family
evidence.*

**#75 Band 2a** (`a8d3b35`) — vendored runtimes: three 0.160.0 / 0.160.1 /
0.128.0, cannon-es 0.20.0, aframe 1.7.1 under `Games/vendor/`, licences
beside every copy, npm-tarball sha256s in the PR. Import maps to `./vendor/…`;
voxelcraft local-first with CDN fallbacks retained as defence-in-depth;
Slipstream GP's surgical two-line swap with every R2 tell-tale asserted PRESENT
after the edit. **Offline gate: 7/7 reach running gameplay fully offline;
7/7 FAIL on the pristine tree.** Booting Wrecking Crew for the first time
revealed (and fixed) a 12px intro jiggle from its scale(1.12) entrance
animation — `overflow:clip` on the animation's own container.

**#76 Band 2b** (`17e7569`) — Slipstream `.archlab` `absolute→fixed`: the
projection math already assumed viewport coordinates, and fixed boxes never
extend the document. Pristine max overflow over a 9s scripted drive: 3314px;
patched: 0px at all three viewports.

**#77 Band 2c** (`aa3e97d`) — the stale-input sweep. One confirmed instance
(Slipstream's held touch steering, zero `touchcancel`/`visibilitychange` in the
live listener census) repaired with the shared reset pattern; census after:
1/1. Twelve other static candidates dispositioned: tap-only, already-patterned,
or held-by-design.

**Standing gates added:** `tools/verify_games_hygiene.mjs` (H1 fonts, H2
entities, H3 CDN-runtimes-need-local-first; 90/90 at close; `--self-test`
proves all three trip), `tools/verify_games_rendered.mjs` (overflow +
accessible names, browser), `tools/verify_games_offline_runtime.mjs` (the
blocked-network running-gameplay contract). Every gate ran red on the
pre-repair tree before it ran green on the patched one.

## §5 · Splash

- Donor `site/assets/brand/mbm-splash.js` verified unmoved at
  `e375642c631358c6753a93c5e410742af2ad49c26634d0428352ec75ed87bc4c` — the
  brief's fixture hash, so the absent fixture cost nothing.
- **Census (rendered, all 43): zero canonical-v2 users anywhere.** 27 games
  show Made-by-Matt branding at boot (bespoke intros/screens — Off-Brand,
  Charcoal, One Guy, Lumins, Lighthouse's keeper primer, the Apex family,
  Echo Vault, Relicforge among them). 14 show none: Trail Runner, Globe Snake,
  Neon Snake Overdrive, Neon Siege, Neon Garden, Orbital, Grid Chase, Prism,
  Marble, Slipstream, Kids vs Staff, Trekkers, **Apex Golf** (alone among its
  shelf siblings), and the secondary Orbital_source. Most carry the small
  `mbmhud-back` chip — hub chrome, not a splash.
- **Splash patching: PARKED.** Thirteen-plus patches, each requiring the full
  gate list in both reduced-motion states with wired `onComplete` boot joins,
  cannot be completed to standard in this sitting's remaining budget. The
  census above is the next sitting's input. Zero patches shipped thin.

## §6 · Expansions — PARKED by name

G1 Glitch Clash Fracture League, G2 Axiom Shift Proofline, G3 Lumins
Constellation Workshop: none started. Blocking condition, derived: §4–§5 had
first call on the session budget and §5's own patching already parked. Per the
brief: fewer things finished completely. All three preserved-design
constraints lists remain in the brief for the next sitting; Axiom Shift's
2.600 Hz flash headroom and its tape harness ran green today (§2), so G2's
floor is measured and current.

## Instrument corrections (this session's own tools)

Recorded because a gate that cannot fail proves nothing, and three of ours
briefly couldn't:

1. The matrix's "responsible element" heuristic named a `position:fixed`
   element for Wrecking Crew's 2px overflow; fixed boxes never grow the
   document. The fix pass re-derived the true offender (title `h1`).
2. The offline gate's canvas probe asked `getContext('webgl')`, which CREATES
   a context on a bare canvas — two pristine menu shells read as "live". The
   negative control caught it; existing-context detection replaced it.
3. The first Slipstream overflow probe sampled a single moment and passed the
   pristine copy — a projection-dependent defect needs a max-over-time
   sampler, which then measured 3314px.

Also: first Band-1 overflow fix patched the *landscape* media query and still
measured 2px in portrait; moved to the portrait query and re-measured 0px.

## Honest not-run / parked list

- The audit pack: absent — §2.1 tool re-derivation, §2.3 finding
  classification, the splash fixture/template comparisons: all parked on that.
- WebKit: NOT RUN (derived: download blocked).
- `verify_surfaces.js` and any live-origin check: NOT RUN from the container.
- The two `*_home_browser` baseline-diff checks: NOT RUN without CI artifacts.
- Frame-budget gates: not attestable in a shared container; runner history
  green.
- Splash patches and all three expansions: parked, above.
- Online-vs-blocked "behavioural equivalence" for the five flagged titles: the
  container cannot observe real-online for CDN games (proxy). What was proven
  instead is stronger for the four import-map games among them — they now run
  fully offline — and the fifth (NSO) likewise. True CDN-vs-vendored
  byte-behaviour comparison remains impossible from here and is stated.

## Deliberate states verified and left (Band 3)

Ledger checked before acting, as required: `poster-art.jpg` intentionally
pending (unruled item, 2026-08-05 ledger); `Voxel_Frontier.html` +
`Orbital_source.html` remain non-shelf secondaries (offline repairs only, both
made; no modernisation, no promotion); Trekkers' old-fork product question
stays with the closed PR18/19 sitting's records; site PR #25 untouched; the
frozen legacy trees untouched; Games repo untouched.
