# PROPOSED_L2K.md — judgement calls needing an owner word (pass PEQ-L2K, 2026-08-22)

Convention as before: DECISIONS_L2K records calls made inside the pass; this file records
what needs Matt (or a later ruling), each with its measurement.

## P1 — `data-speak-text` on the L2 panels is inert on this chassis
The prompt mandated print mirror + `data-speak-text` per panel. Both are present, but the
ASDAN v5 chassis has **no speech-synthesis layer** (`data-speak-text` is a
Science-Teesside v3 convention; 0 occurrences elsewhere in LAUNCH/GROW ASDAN). The
attribute is carried, accurate and harmless. **Open:** add a speech layer to the ASDAN
chassis, or accept the attribute as forward-provision.

## P2 — the weekly-hours parameter is the timetable decision
The year map is worked at 3.5 h/wk (owner-input default); the 2/3/4 h/wk sensitivity
table is on the SoW page. Measured consequence, stated there in bold: **the E3
Certificate consumes the whole year at ≈3.5 h/wk with zero slack** (133 physical + 7
declared co-delivered = 140 unit-GLH, last unit closing in W38); at 4 h/wk there are 12
spare hours. **Open:** Matt sets the timetable; if it lands under 3.5 h/wk, the honest
year target drops per the table (e.g. 3 h/wk → Extended Awards, L1/E3; the map's numbers
regenerate from `l2k_plan.py` by editing `WEEKLY_MIN`).

## P3 — calendar anchoring
The map runs W1–W38 in 7+7+6+6+6+6 half-term blocks; no 2026–27 term-date file exists in
`_passpq` (DATES_2026-27.md carries lifecycle dates only). **Open:** anchor W1 to the
school calendar when set; week numbers, not dates, are the committed structure.

## P4 — FoodWise overlap (RPL note only, per v2 out-of-scope line)
`BUILD_ASDAN/FoodWise/` teaches food content that the kitchen year will also touch.
Spec §7 p15: RPL is eligible within 3 years, centre-assessed. **Measured:** FoodWise is a
BUILD short-course surface, not a PEQ unit; nothing overlaps at criterion level today.
**No action taken** (out of scope); recorded so an RPL claim, if ever wanted, starts here.

## P5 — deck→unit GLH mapping is a named table, not a hidden judgement
GROW deck banking lines on W1/W2/W4/W6 cite no unit codes (inherited open item, PEQ-E3
PROPOSED P4). The ledger maps them LSk/LSk/LSk/LSk (audit · SMART goals · routines ·
review) with W3→TmWk and W5→ThSk/CrTh, per their banking lines — the single edit point is
`DECKS` in `_passpq/tools/l2k_plan.py`. **Open:** if Matt re-maps any deck, edit that
table and re-run; every dependent surface regenerates.

## P6 — merge order for the manifest pin (both repos)
Three branches: `claude/peq-l2k` (the pass) · `claude/peq-l2k-manifests` (Lessons:
resources.json + pin only, inside ALLOWED_DIFF) · Apps `claude/peq-l2k-pin` (the twin
pin). Order: pass first, then the two pin branches promptly together — between the
manifests merge and the Apps merge the two repos' gate copies briefly differ, which the
scheduled cross-estate run would flag if left overnight.

## P7 — the L1 Certificate claim shape
Named default on the SoW page (all six L1 units, 15 cr; exact-14 fallback = five L1
units + ThSkE3); the ASDAN-facing question is lodged in `QUESTIONS_FOR_CHERYL.md` and is
due by names-confirmation.

## P8 — Kitchen pupil decks are the NEXT pass
Out of scope here by v2's own line; when authored FROM this SoW, each DecMk/WellbLe deck
inherits COMPLIANCE item 15 (the safeguarding boxes, `data-mbm-guide="staff"`), and the
witness sheets those decks carry must use the three-way Level tick from day one.

## P9 — browser-matrix "HUD on Lessons games" nondeterminism (added post-merge)
On PR #145 the cross-estate `browser-matrix` job failed twice with **different**
failure sets (11, then 30 of 939 assertions; overlapping Games files; signature = one
home-control click `TimeoutError`, then "navigation interrupted by another navigation"
cascading through later routes in the shared context). The identical content run
locally (canonical site + branch on one origin, canonical search index): **939/939
passed**. The diff was two files outside `Games/`. Established as runner
nondeterminism and merged on that evidence (PR #145 comment carries it).
**Open:** harden `tools/verify_hud_on_lessons_games.mjs` — a fresh context per route,
or one retry on the cascade signature — in its own pass; it sits outside ALLOWED_DIFF
so it could not ship with the manifests split.
