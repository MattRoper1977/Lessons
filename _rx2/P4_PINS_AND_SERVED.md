# RX2 P4 — pins moved and served proof (2026-09-07)

All counts and SHAs below come from tool output, not typed.

## Why the education publisher was red
Lessons `Education Pages publication` runs 55–59 (main 48378736 → 166d79ff) failed in the Site builder before any
education gate: builder 47c47569 → `Review stale control/content evidence: Charcoal`; builder 32ad1441 →
`Unreviewed or ambiguous source revision: Lessons/Games/Orbital.html`. Site main's Play registry only knew the
baseline blobs of Orbital and Glitch Clash; the twelve reviewed Afterlight revisions lived in held Site #316.

## Chain (every step merged on full green; skipped jobs are the by-design PR skips)
| step | PR | merge | evidence |
|---|---|---|---|
| Site: registry + Lumins recapture + builder assets/, **no pin line** | Site #318 | 2eafa9a4c2a86c440708a1d692bf1d66a3d1cba0 | 6/6 checks green; local: source-revision controls PASS at Lessons 419d44f0 / 1a8e3b29 / 95146202; build at Lessons main selects 13 revisions |
| Lessons: publisher 32ad1441 → 2eafa9a4 + caller digest 40a14570… | Lessons #386 | a91780fceea8a1eade23e8a682391902bf7d3ae8 | 10/10 checks green; cross-estate gate PASS, positive control 3 |
| Education Pages publication | run 60 · 34158001709 | — | build+verify, all-file admission, package, deploy-pages: success |
| Games: site a30088ea → 2eafa9a4, lessons 13845784 → a91780fc (hand-made, #74) | Games #75 | fbf1aa1163ada27ada2c9bb00bfcb5888bf64d0b | PR build (tuple + live HTTPS probe) green; local at tuple 69/0/0, shelf byte-identical, shelf contracts PASS |
| Standalone games website (push to main) | run 32 · 34158939638 | — | build, deploy, **verify-published** success against https://www.madebymatt-play.uk |

Payload byte-sets that moved with the Games pin (18): the twelve Afterlight routes, /Lessons/Games/Glitch_Clash.html
(registered HUD revision), /fracture/, /neonsync/, /neonbreach/, /apexrally/, /neonmeridian/ (Site main since a30088ea).

## Still held
Site #316 (Site verify pin lines Lessons 419d44f0 → 166d79ff, Apps ed4c59ae → 65015ed5) waits on the Apps mirror of
`tools/verify_cross_estate_unification.py` (two CATALOGUE_PINS digests + PUBLICATION_CALLER_SHA256 40a14570…).
Served proof here is CI logs at the SHA; both domains answer 403 to this session, so no byte-matched fetch was made from it.

Rollback: Games `play-publication.json` site_commit a30088ea8d3380b0c0e6040a361a9c0449450a89 / lessons_commit
138457849c2690de5413ed80d616725a5160f9d1 (a push to main republishes); Lessons publisher 32ad1441 (main 166d79ff);
Site main 32ad144105fcc3c9b53d59cdedf534a456e77f7e.
