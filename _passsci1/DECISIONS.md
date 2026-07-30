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
        NON-html tooling/docs, ALL PRESENT in both 8540eee and HEAD, never removed, ~~never the second
        writer's~~ never added by anyone during the pass (they predate the fork). Not lessons, so
        outside the sentinel universe.
        [CORRECTION 2026-07-29, SCI-3] The struck phrase "never the second writer's" is retracted:
        it framed the six files against a "second writer" as if that entity were established. The
        sentinel NEVER corroborated a second writer. What survives is only the directly observed
        fact — these six files existed in the authoring container this session did not create, at
        both fork and HEAD. Nothing about who, or whether anyone, "wrote" alongside is supported.
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

# --- SCI-3F merge & ship (Matt-authorised: merge THIS branch to main, push origin/main) ---
[GREEN] §1 measure-first: all four SCI-3 closeout items (a-d) already landed on branch tip e9b72b3
        (= d6df2e5 + 2 closeout commits fb4b942, e9b72b3). Retraction struck in place, R-G06 +
        self-deriving sentinel, contact sheet PNG 1033x5502, MERGE_DOSSIER present. Only (d) was
        stale: dossier derived at origin/main=e3f7212; main since advanced to 2324ddc, so the
        unmerged set is re-derived from git below (§2 mandate: derive, never carry).
[GREEN] ROLLBACK SHA recorded BEFORE any merge step (§3.1): origin/main = 2324ddc
        ("Off-Brand v3.1.2 — add niece Clara..."). To undo the ship: `git push --force-with-lease
        origin 2324ddc:main`. Branch tip merged = the rebased science tip (recorded at push time).
[GREEN] Rebased the 15-commit science branch onto origin/main (2324ddc) per §3.2 — main had
        advanced. Rebase was CLEAN, zero conflicts across all 15 commits: git auto-unioned
        resources.json (my 25 entries append at array end; main's 3 `featured:true` flags are
        mid-file — disjoint hunks). Post-rebase resources.json = 411 entries VALID, 25 unique
        sci-tees ids, all 4 featured flags preserved (§3.3 keep-both-sides satisfied automatically).
[GREEN] Post-rebase gates re-run (§3.2): 25 lesson HTML byte-identical pre/post rebase (rebase
        touched only resources.json) so branch gates still hold. Sentinel 45->70 delta +25.
        Hub chip gate (index.html buildQuicknav/render filter chain, YEAR=2026-27): 21 subjects,
        every in-collection chip advertises what render() returns; Science-Teesside 25/25 — the
        known 25-file chip-count bug is NOT triggered. LL-INST-09 loop-mark gate PASS on 3-lesson
        sample (BUILD/GROW/LAUNCH), all 3 tiers. Print-parity spot render BUILD W3 all tiers PASS.
        Legacy science (biology/ chemistry/ "2 Physics 10/", 40 files) byte-identical to pre-merge
        main. AMBER: jsdom/PIL absent in this container; playwright installed at run time to drive
        the render gates against the pre-installed Chromium.

# --- SCI-3F closing items (post-ship, docs-only, no history rewrite) ---
[GREEN] SENTINEL UNIVERSE STRING MADE EXACT (closing item A). Everywhere this pass wrote "tracked
        *.html" for the 45/70 count it meant "tracked *.html CONTAINING 'll-g:loop-mark'" (the
        lessons) — NOT the raw `git ls-files '*.html' | wc -l`, which is ~433 at fork 8540eee and
        ~459 at merged main 2ce19ce. The two must never be compared: a future pass reading "tracked
        *.html = 70" literally would run the raw count, get ~459, and infer a catastrophe (the exact
        45/51/76/79/235 confusion that cost this programme two turns). sentinel.py now prints BOTH,
        each labelled with its own universe, both derived at emit time from the SHA: at the merge
        boundary 2324ddc->2ce19ce, loop-mark = 45->70 (+25, THE sentinel) and ALL tracked *.html =
        434->459 (+25, context only). Corrected in FINDINGS_SCI2.md and MERGE_DOSSIER.md too. The
        earlier AMBER "SENTINEL RECONCILED / TRACKED *.html" lines above are left in place (no
        rewrite); this line is their exact-universe correction.
[GREEN] MERGE_DOSSIER re-stamped at merged main 2ce19ce (closing item B) with the derivation
        command, the post-merge parked-branch overlap matrix, an explicit resources.json union
        policy for the now-GUARANTEED sbx-art-a2 conflict on 29 Aug, and 2324ddc recorded as the
        pre-SCI-3F rollback SHA inside the dossier itself.

# --- SCI-3F session close ---
[GREEN] PAGES PUBLISHED. The docs-only successor commit 88d6d32 (the sentinel/dossier corrections)
        built and served: "pages build and deployment" status=completed, conclusion=success
        (2026-07-30T07:49:29Z). At session close the site serves 88d6d32. The science payload was
        already live one commit earlier at 2ce19ce (also completed/success); a docs-only build
        failure would have left the site on 2ce19ce, so science stays live either way.
[GREEN] RULE (registered here, estate-facing): a merge dossier's stamp describes HEAD-AT-WRITING,
        because a dossier cannot stamp the very commit that carries it. The commit that lands the
        stamp is a DECLARED docs-only successor — this is the TERMINAL, correct form. Successors of
        a docs-only tail must NOT demand a re-stamp of that tail; doing so is an infinite regress
        (every re-stamp needs another). Cross-refs R-G03 (stamp that couldn't be true when written)
        and the sentinel's R-G06 (a count is meaningless without its universe).
[GREEN] SESSION CLOSE. The Science · Teesside programme is SHIPPED at 2ce19ce (25 lessons live,
        legacy science byte-identical, hub chip gate 25/25, all §3.5 gates green, packs rebuilt).
        Branch claude/sci-1-pass-science-build-b2dyew is CONTENT-MERGED (its 25 lessons byte-
        identical in main) with its ref SUPERSEDED by the rebase; NOTHING science-side is owed to
        the 29 Aug sitting. Matt deletes the superseded branch in the UI. This closing commit is
        itself docs-only; its own Pages build is NOT polled and no successor should reopen the loop.
