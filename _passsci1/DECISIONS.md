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
