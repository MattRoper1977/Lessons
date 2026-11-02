# Play landing train · proposed order · Mon 2 Nov 2026, 11:05 UTC

Read-only survey, made after the owner (10:46Z) asked for Play's game names and look to be "addressed … you decide". No Play PR has merged since Site #558. The live Play site is pinned at Site 76cc9044 / Lessons e82625ea (Games play-publication.json).

## 0 · Names rule, live breach (land today, before anything else)

Served at 10:55Z: a child's real first name appears 11× on /offbrand/ and 29× on /Lessons/Games/Charcoal.html.

1. Lessons #769 (Charcoal) and #770 (retired Off_Brand), 12/12 green each. Merge both.
2. Games pin release: Lessons → the new Lessons main. Games #140 targets 135489a9, so re-cut it to the post-#769/#770 SHA.
3. Games #139: Site 76cc9044 → 1e18cb4c (carries Site #558). Draft, 3 pass, mergeable. Re-cut to current Site main if the gates allow.
4. Games #137 (games.json dedication sentences) and Site #560 (manifest mirror + /games/ curation), both drafts. Mark ready and land them in the same window.
5. Proof: served bytes on both routes show 0 hits; the ruling side checks this before closing.

## 1 · Names and finding games (the owner's ask)

- Site #544 (P2: homepage revision, four named shelves, filters dialog).
- Site #541 (P3: per-game launch pages, VideoGame schema, posters, sitemap).

These are about 85–88 files each and touch .github, so they are stacked branches. Land the stack bottom-up, rebasing each onto the previous merge. Do not merge one upper PR that carries all the lower ones.

## 2 · The look (stack continues)

| PR | Content |
|---|---|
| #536 | P1b masthead motif and poster frames |
| #545 | rails and subgrid card alignment |
| #546 | display typography |
| #547 | reduce-motion-safe transitions |
| #554 / #561 / #575 / #576 / #577 | hub polish: phone spotlight, Updated dates, carousel dots, Apex Kick tag |
| #549 / #551 | today's seed card, read-only badge wall |

#554 and #561 overlap (both "phone spotlight / 60-day Updated dates / Apex K…"), so keep one. #575–#577 (P-17) supersede the overlapping parts.

## 3 · Classroom-ready games (independent, small: 4–5 files each)

#563 Apex Kick, #564 Aurora Links, #565 Blackout Pulse, #566 Emberwild, #567 Voxel, #568 House Olympiad, #569 Off-Brand, #570 Echo Vault, #571 Skybreak, #573 Stormbreak.

- Each touches its own game folder plus shared records (domain-split, reports). Land them one at a time and re-cut the shared preservation and evidence rows each time.
- #569 Off-Brand must follow §0.
- Grapple blur fix (ruled separately) slots in here, with the 1 Nov Grapple branding pack (scratch\grapple, candidate C).

## 4 · Housekeeping

- #538: a one-file check re-pin. Land it any time.
- #519: CONFLICTING, 37 files, older maker-splash work. Ask the lane whether it is superseded. If it is, close it with a note.
- #521, #522, #523 are marked "not for merge" proposals. Leave them.

## Owner load

Play publishes through Games pin releases (Games repository PRs), not the Lessons education-pages carrier. Confirm whether any step needs an owner web-editor commit. If one does, batch the steps so the owner (unwell today) gets one edit per batch, with exact lines. I verify every owner commit to the byte.

## After the train: professional look (direction, same family as the education site)

- Real game artwork on every card: the existing 640×360 poster frames from #536 and #541.
- One card and tile system shared with the education tiles.
- Calm motion, with reduced motion respected.
- Plain names. No version or jargon tags in visible text (the P-12 classroom pass already removes AAA, V4/V6, FPS and HUD).
- Proof per step: screenshots at 390×844 and 1280×800, 0 console errors, names scan 0.
