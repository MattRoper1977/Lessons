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

## Run 2 (2026-09-01, Phase 1 cohort A)

WRONG: "Main is expected around 20216304 (eleven past 22f6470f)."
RIGHT: main is dedbf06f — six more FEB wave 1 packs landed while the order was in flight (PRs #181–#186: BUILD/GROW ASDAN Spring 1, LAUNCH ASDAN Spring 1 W16, BUILD/GROW/LAUNCH Humanities W14–W15). None touches the twelve or _sownb. PR #181, recorded as an empty anomaly in run 1, got its commits and merged.

WRONG: "the RSH-3 reference deck named in the denominators file."
RIGHT: G16_DENOMINATORS_RSH3.json names no reference deck. The four per-family reference decks live in _sownb/feb/tools/render_measure.js (grow-asdan PEQ_A2_W6, grow-science SCI_G_W13B, launch-asdan PEQ_W12, launch-science SCI_L_W13L3). Those were used as the §2 controls.

WRONG (order §4): cohort B = PRs #177–#180.
RIGHT: cohort B measured by diff against 22f6470f is ten packs across PRs #177–#186: 36 added HTML surfaces (24 lessons + 12 front doors/variants). Recorded in VB_STATE with a week-major split.

RAISED THEN DOWNGRADED — four g16/static red classes on cohort A, every one an instrument artefact of the FEB rebuild, none content:
1. shared.offline.boundary red ('localStorage') on all 8 lessons. The PINNED row value forbids ["fetch(","XMLHttpRequest","serviceWorker","data:"] only; FEB's metric() hard-codes a wider list including localStorage. The pinned contract's own shared.guide rows require the localStorage-backed guide persistence — the exact conflict feb/DENOMINATOR_REFREEZE.json documents. All 8 lessons contain none of the four pinned-forbidden tokens. Same artefact reds the four static_pack_gate runs; everything else in them (ids, 40-minute timings, chains, checksums, planted controls) is green.
2. family.*.token.grow red (actual []) on 5 lessons. The RSH-3 provenance comment before <style> (e.g. <!--RSH-W7A:v1-->) pseudo-matches DECL's `--name:value` regex and its greedy value consumes the real --grow declaration that follows. Comment-stripped, every deck declares the token exactly once with the contract value.
3. family.{grow,launch}-asdan.control-count red (7 and 6 vs references 8 and 7). The references do not reproduce on the rows' OWN donor decks: both donors render 6 buttons, static-parsed and rendered alike, on this engine. Row is MEASUREMENT INVALID for cohort A. Substantive parity recorded: LAUNCH W13/W14 = donor exactly (6=6); GROW W7 = donor + one deliberate Evidence-routine button (7 vs 6).
4. START_HERE firing controls fired=False on GROW ASDAN and LAUNCH ASDAN. The mutation literal uses the contract's case-normalised value (#4a6fa5) against a file that writes #4A6FA5 — the replace no-ops, so the still-intact declaration re-passes. Removing the actual declaration makes the row fail: the red control fires under the corrected mutation.

RAISED THEN DOWNGRADED — g10 RED on 3 lessons: unresolved pairs "Community Project", "Safe Research", "Triangulate Source". Capitalised headings, not personal names. No personal name exists in any of the twelve.

REAL DEFECT, REPAIRED: LAUNCH Science W14 front door carried the stale "Held local candidate: nothing in this pack is pushed, merged, deployed or catalogued" notice. Removed (PR #189); SHA256SUMS regenerated; front-door gate PASS with red controls firing; nothing regressed.

MEASUREMENT INVALID, NOT GREEN: public 200 + body-hash binding for all twelve — the venue's network policy answers 403 to CONNECT for mattroper1977.github.io. Verified on landed git bytes instead; link targets verified on disk.

ENGINE NOTE: this venue renders on Chromium 141.0.7390.37; the twelve were measured on 149.0.7827.0. Running-head clearances shift with the engine (references measure 17–53pt here; the order's ≈33.37pt is not reproduced); the version-robust predicate (every page's named head inside its own page-local MediaBox) passes on all twelve and both control families. No pagination red survived its control.

READING LEVEL, PRINTED NOT FIXED: 6 of 8 lessons measure >1 IQR EASIER than their pack median (FK approx, pupil+staff body text): GROW ASDAN W7 11.0 vs 12.2; GROW Science W7A 7.9 / W7B 8.4 vs 10.3; LAUNCH ASDAN W13 11.5 / W14 11.7 vs 14.5; LAUNCH Science W14L2 12.4 vs 13.3 (L1, L3 within range). Deviation is toward easier reading in a SEN setting and the medians include staff-facing text; recorded, no action.

