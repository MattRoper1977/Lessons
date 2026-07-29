# Pass SCI-2 — Decision log

Appended as calls are made (SCI-2 §3). One line per non-trivial choice. GREEN = decided and done;
AMBER = done, flagged; RED = stopped and asked. Written at the time, never reconstructed.

[GREEN] Sentinel emitter `_passsci1/sentinel.py` written — recomputes tracked-*.html count at emit
        time from git and prints the file list; no number carried between reports (§1 mandate).
[AMBER] SENTINEL RECONCILED. The correct universe is TRACKED *.html (the gate's `-- '*.html'`).
        Fork 8540eee = 45; HEAD = 70; delta = +25 = exactly the 25 science lessons. The "51"/"76"
        figures were the ALL-FILES universe (html + 6 non-html tooling/docs), which is unstable —
        it is 79 now (my committed tooling adds ~3 more string-mentions), NOT 51+25=76. So the
        html universe (45→70) is the one to quote; the all-files number should never be carried.
[GREEN] The "six files" (the 51-vs-45 gap at fork) identified and checked: LL-I_B1_measurement_map.md,
        INSTRUMENTS.md, bundle_facts.py, patch_loopmark.py, REGISTER.md, _passsg/FINDINGS.md — all
        NON-html tooling/docs, ALL PRESENT in both 8540eee and HEAD, never removed, never the second
        writer's (they predate the fork). Not lessons, so outside the sentinel universe.
[GREEN] Rebuilt both packs on current head (aec32b1) — the pre-clip zips were stale by definition.
        Osmosis clip present in both packs; 219 html rebranded, 0 wordmark residue, x-brand every
        page, assessed conditions intact, crawl clean, both zips unzip -t OK. Delivered to Matt.
[AMBER] Clip verification is impossible this session: Oak (thenational.academy), BBC (bbc.co.uk)
        and NASA (spaceplace.nasa.gov) all return 403 to the session fetch tool (BBC blocked
        outright). So NO new clip is wired (§4: never wire an unverified clip). Candidates found
        via the search index are staged in CLIP_REGISTER.md for Matt's 30-second check. The
        renderer already supports a per-lesson `clip` field, so wiring later is a one-line change.
[GREEN] CLIP_REGISTER.md built across all 25 lessons (WIRED 1 / CANDIDATE 4 / SEARCH ~8 / rest
        EMPTY BY DESIGN). Slots prepared via the renderer's clip= field. Nothing wired unverified.
[GREEN] FINDINGS_SCI2.md written. SCI-2 §6 items 1-5 complete; nothing merged.

# --- SCI-3 close-out ---
[AMBER] RETRACTED the "second writer" claim (§0). It appeared as fact in FINDINGS.md and
        FINDINGS_SCI2.md and in the d6df2e5 commit message. Struck in place in the docs (originals
        kept visible) with the correction: main advanced during the pass with commits this session
        did not author (a4cdd36, 013121e/bc215d1, 2236d0b), but those are Claude-authored from other
        passes (PQ/Season-close/T2-4), several "approved by Matt" — not an established separate
        writer. The sentinel never corroborated one. Commit message d6df2e5 is immutable history
        (not rewriting a pushed commit); retraction lives in the docs and here.
[AMBER] The "63 overlapping" coexistence scare (SCI-2 hand-back) was a MALFORMED DIFF read in the
        wrong direction: `git diff --name-only aec32b1..origin/main` reports files that differ, and
        since my branch is AHEAD of main it surfaced MY OWN 63 changed paths, not a second writer's.
        The correct check is whether origin/main advanced past my rebase base and touched my paths —
        it had not (still 2236d0b). A scare that resolved is still an instrument that lied; logged so
        the next person knows a diff read in the wrong direction lies this way.
[GREEN] REGISTER.md R-G06 added — "a count is meaningless without its universe" + the corollary
        (an emitter that names its sentinel joins the population; exclude own tooling and SAY SO).
        Cross-refs R-G01/R-G03; notes R-E21's independent "invariant at 45". sentinel.py now prints
        its universe + exclusions and drops any _passsci1/ path defensively.
[AMBER] Contact sheet (§2): built for all 25 lessons WITH render-only assertions (no illuminator
        clipped by viewBox / no label-pill overlap / print p1 not blank/overflow). The assertions
        CAUGHT 3 clips — food-chain (BUILD W7), friction (GROW W3), gas-exchange (LAUNCH W4 L2) —
        labels/arrows spilling 2-20px past x=640. Fixed (GREEN, own defect): food-chain labels
        176w/-88, friction smooth arrow 116, gas-exchange two limewater captions merged to one.
        All 25 now PASS; 3 touched lessons re-gated ALL PASS, re-placed, packs rebuilt.
