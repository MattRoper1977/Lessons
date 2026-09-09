# UX2 state at 2026-09-09 04:45Z (write-on-limit record, Q4)

## Landed
- Part A: Lessons #435 (495d5a06), #437 (6b742b56), #441 (205f6ba6) + caller pins #436 #438 #442.  UX2_A_OK
- Part D: Lessons #439 (c509498a), #443 (894a099d); Site registry #331 (1c7601b8), #333 (2179ca71).  UX2_D_OK
- Part B: Site #335 -> 92abc460; Lessons #450 (6ae34c37), #451 (54041bdb), #445 (d582a6fc), #452 (2c33266b).
  Served proof: github-pages deployment 6341617889 at Site 92abc460, state success 2026-09-09T03:04:19Z, https://madebymatt.uk/.  UX2_B_OK
- Part E: Lessons #447 -> 11d85b55 (nine remasters; glitch-clash STOPPED at E1).
  Served proof: education-pages run 34289556569 at 11d85b55, build and deploy both success.  UX2_E_OK (E5 list below)

## Heads
Lessons main 2c33266b · Site main 92abc460 · Games main ce5b85db (unchanged)
Order start: Lessons 7416dd69 · Site 6430f23f

## Open
- Site #332 (Part C, Play shelf) at 5cfc225: Play shelf + main merge + Lessons pin held equal to 2c33266b.
- Games #80 (C1 manifest): red only on the pinned Site mirror; clears once #332 lands and pin-release runs.
- Games #78/#79: stale pin-release PRs, superseded by the next cron/dispatch.
- Then: Games pin-bump (P4 hand-made path, M3 is OFF), delete the temporary Games branch claude/ux2-c2-shelf, UX2_C_OK.

## Known-red, established as NOT this order's
1. Town Life "Serial comparative and splash performance": baseline byte-pinned (PRE_SPLASH_SHA 7041e767),
   candidate townlife/ tree 9e2e4d547e78 and harness 68ed77813f51 IDENTICAL across main and both PRs.
   Failed then PASSED on re-run on BOTH #332 and #335; passed on main at f62470da by dispatch.
2. "Eight-game V4 deployment gate": deterministic, failed twice on main incl. a re-run. Its own navigation to
   https://madebymatt-play.uk/... is answered on www., and the origin comparison counts that redirect as a
   third-party request. Red on main at 24be4b1a (6 Sep) and 47c47569 (7 Sep), before this order.
   Patch proposed on Site #335, not applied: this order does not edit gate assertions.
3. Lessons "Merged is not served": prepare_served_published waits 240 s; education-pages runs take 350-620 s.
   Red on every main push since 0e0cd743 (2026-09-07T12:09), before this order. Not fixed: same reason.

## Defects found and fixed in-lane this session
- Site: /resources/ lost the professional shell (10 findings) -> restored from main verbatim.
- Site: /resources/ lost 4 of 5 reading themes and its named mbmTheme block -> restored, 6 distinct backgrounds measured.
- Site: shared_navigation imported education_expansion at module scope, which needs lxml; the design audit
  could not reach header(). Now read at the point of use.
- Lessons: CATALOGUE_PINS drift x3 (verify_education_navigation.cjs #450; check_hub_browser.cjs and subject.html #452).
- Lessons: the packs-hub check counted the B1 header's labelled search icon as an empty link.
- Site: usage_discovery.inject() gained a parameter on each side of the C/B merge; both kept.

## E5 phone list (corrected: the first draft had two three.js games and no DOM game)
- three.js: Trekkers (ES module importmap -> shared Games/vendor/three-0.160.0/, plus its AQA evidence link)
- canvas:   One Guy (canvas#cv role=application, 32 fillRect; the game whose exit region was rewritten and restored)
- DOM:      NOT AVAILABLE among the nine landed. The collection's only DOM game is Glitch Clash (its canvas is an
            aria-hidden particle layer) and it STOPPED at E1. Report, do not substitute.
