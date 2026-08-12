# Neon Meridian + Rally Vector 3D — trailer render record

Companion to the two-driving-games launch (site repo `reports/2026-08-12-two-driving-games-launch.md`).
Promotional video only; the Pages repos were read-only this pass and no video
binary is committed anywhere. Files were handed to Matt directly.

## Source of truth

Rendered from the committed game files at site main tip `5f979e7` — both
hashes match the ones the launch close named, so no drift:

```
771c72c3a5e35db4ecc493a7e76492a7dc8c888b0ffd20de1fe97f2bf5bc16cc  neonmeridian/index.html
4af053f5432151d169cee8949c5df84cda165a884a73ed558a1569137b0c434a  rallyvector3d/index.html
```

## Deliverables (files handed over, none committed)

| file | duration | resolution | encode census (worst rate) |
|---|---|---|---|
| rallyvector3d-trailer-1080p.mp4 | 29.5 s | 1920×1080 | 0.847 Hz |
| neonmeridian-trailer-1080p.mp4 | 29.7 s | 1920×1080 | 0.101 Hz |
| rallyvector3d-reel-1080x1920.mp4 | 15.5 s | 1080×1920 | 0.903 Hz |
| neonmeridian-reel-1080x1920.mp4 | 15.2 s | 1080×1920 | 0 Hz |

Census run on the FINAL ENCODES with the estate's own analyser
(`tools/flicker_analyse.mjs` at site tip, self-test first), same floors as the
games' census: hazard 25.5 units, ceiling 3 Hz, margin target ≤2.4 Hz. All four
sit far under the target. Poster frame per video, each held to the card-art
pixel bar (≥24 distinct quantised colours; measured 542–834, lit share 0.96–1.0).

**Audio: silent, no audio track.** WebAudio runs on real time; under the
virtual clock a captured track could not be deterministic, and silent beats
broken (T4 ruling).

Every gameplay sequence asserted its scene state through the games' own seams
before frames counted (Rally: `mode==='running' ∧ speed≥15 ∧ progress≥0.05`;
NM: `{tod, rain, drops, cops, speed}` per shot). The shot logs with the
asserted states sit beside the delivered files.

## Two findings for the register

**1. The toast real-time trap (same family as the parked car).** NM's toasts
hide themselves with a wall-clock `setTimeout(2600)`. Under a virtual-clock
render a captured frame costs ~2 wall-seconds, so every toast — MISSION
STARTED, MISSION COMPLETE, ENTERING WESTHAVEN, LANDMARK DISCOVERED — decayed
within one or two frames and the first pass shot four beats whose payoff was
invisible. In real gameplay a toast lives 2.6 s ≈ the length of the shot, so
the retake pinned exactly the 2600 ms timers for the shot's duration: that
*restores* the honest timing rather than inventing one. The general lesson:
in a virtual-clock harness, anything keyed to real time silently vanishes
from footage, and no scene-state assertion catches it unless you assert the
DOM you meant to film (the retakes assert `s.toasts` content).

**2. Input seeking lies about frame identity.** `ffmpeg -ss <t> -i` on the
static 7.0.2 build landed up to a second off, which made the first boundary
montages show wrong frames — an inspection instrument producing false
evidence about a correct encode. Frame-exact `select='eq(n,F)'` extraction
(one decode pass) fixed it. Assert on evidence holds for the *instrument*
too: the first montage nearly triggered a needless re-edit.

Also of note: `drawtext` is absent from that ffmpeg build; captions went
through libass (`subtitles=` filter) instead. All on-screen caption text is
verbatim or truncated from the games' own strings (stage names + `desc`
fields, meta descriptions, canonical URLs) — no review quotes, no invented
taglines (R6/T3).

## Shot provenance, briefly

Rally: Cliffline Dash in rain; its ford at progress .47 (HUD surface reads
WATER FORD); Timberline Loop at dusk with the pace-note callout asserted
visible; Copper Canyon in storm; a full campaign stage driven by the game's
own-track autopilot to a real "Victory!" result card; the Service Park
overlay ("45 min", next stage Sahara Run); and a ghost recorded by that
campaign finish through `GhostLeaderboardSystem`, raced on camera with
GHOST: ACTIVE in the HUD. NM: night city with live traffic; heavy rain at
night; a DELIVERY mission started and completed on camera (500 CR payout,
Northpoint Mast — its discovery toast landed in the same shot); the
Central→WESTHAVEN district line crossed on camera; Westhaven Terrace
discovered (shot trimmed to end before the car reached the building — the
untrimmed take ended in a crash frame the inspection caught); and a full
ROAD HEAT pursuit at night, whose strobe is the launch record's measured
2.07 Hz gameplay figure.

Matt's check outranks all of the above: watch both trailers end to end on
your phone — do they look like the games, and would a pupil press play?
