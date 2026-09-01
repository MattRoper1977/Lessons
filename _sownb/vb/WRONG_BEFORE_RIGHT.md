# WRONG_BEFORE_RIGHT — Order VB

One entry per figure the order quoted that measurement disproved, and per finding raised then downgraded by reading the call site. Plain lines. Appended per run, never rewritten.

## Run 1 (2026-09-01, Phase 0)

WRONG: main head 22f6470f (RSH-3 catalogue merge).
RIGHT: main head 20216304. Eleven commits landed after 22f6470f: PRs #177–#180 (FEB wave 1 — BUILD Science W14–W16 plus measured instruments, LAUNCH Science Autumn2 W7, GROW Science W15–W16, LAUNCH Science W15) are inside this order's trees; PR #176 (Games AAA V6) is outside.

WRONG: thirteen open PRs.
RIGHT: fourteen. The extra one is #181 "FEB wave 1: BUILD ASDAN Spring 1 W15–W16", and it is an anomaly — its head commit 257ad6a4 is already an ancestor of main and its diff against main is empty. An open PR carrying nothing. Recorded as a human item.

WRONG: STYLE_CONTRACT.json has 225 rows, sha256 prefix e0f8f546.
RIGHT: the live contract on main has 457 rows, sha256 467a8df6. FEB wave 1 extended it (PR #177) — an authorised landed append, not drift. The 225-row e0f8f546 contract survives as the pinned contractSha256 inside G16_DENOMINATORS_RSH3.json, whose own hash matches the order's expected prefix 4ec68f96 exactly.

RIGHT AS QUOTED: frozen production denominators GROW Science 86 / GROW ASDAN 76 / LAUNCH ASDAN 80 / LAUNCH Science 87 — all four re-derive from G16_DENOMINATORS_RSH3.json as lessonCount + supportCount. Caveat measured: the FEB refreeze (feb-denominator-refreeze-v2) excludes the shared.guide.byte-block row from the FEB production denominator; RSH-3's rows are untouched.

FEARED, NOT TRUE: instruments living only inside RSH3_EVIDENCE.zip.
RIGHT: the full gate toolkit (34 scripts: g10, g11, g15, g16, g18, g19, g21, c-gate containment and identity, running heads by PyMuPDF, s24, safeguarding, static, render battery) is on main under _sownb/feb/tools/, and the denominators, contract, token-ownership, calendar spine and horizon files are on main under _sownb/. No rebuild PR needed.

RAISED THEN DOWNGRADED: four branches contend on the twelve RSH-3 surfaces (rsh3/grow-asdan-w7, rsh3/grow-science-w7, rsh3/launch-asdan-w13-w14, rsh3/launch-science-w14-w15).
DOWNGRADED BECAUSE: their blobs for those paths are byte-identical to main — they are the stale delivery branches of the very merges that landed the files (squash-merge residue). The twelve surfaces are uncontended; Phase 1 repairs are not mutation-blocked.

MEASURED, NEW: 92 branches sit strictly ahead of main (order implied ~14). Most are historic pass/audit/backup refs. The strict §0.11 reading would mutation-block much of Art_Teesside via parked/ruled PR branches; flagged as a human item rather than silently adopting either reading.
