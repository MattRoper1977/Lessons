# Pass FIN-1 — DECISIONS log

## Identity gate (verified before any action)
- Repo: mattroper1977/lessons (served madebymatt.uk/Lessons/) — CORRECT target
- 2ce19ce: present, ancestor of HEAD — PASS
- 88d6d32: present, ancestor of HEAD — PASS
- tracked *.html = 459 — PASS
- Science_Teesside/ = 25 lessons — PASS
- Verdict: 4/4 PASS

## Rollback SHA
- origin/main head at pass start: 654962529e74ecae01a642172dda0c378abb42c3

## Note on session scope
- This session originally attached to mattroper1977/mattroper1977.github.io (WRONG repo).
  Lessons repo added via add_repo + cloned to /workspace/lessons after identity STOP+report.

## AMBER decisions log
(entries added inline as encountered)

## §1 MEASUREMENT OUTCOME (2026-07-30)
- Harness: _passfin1/measure.py (playwright + pip, chromium /opt/pw-browsers), both http://127.0.0.1 and file://
- 8 BUILD_HUM v4 files (W1–W8), 2 modes each = 16 renders.
- RESULT: ALL 16 CLEAN.
  - script errors: 0 · uncaught pageErrors: 0
  - data-driven regions (Arrival x3, Starter, WeDo1 sort pills+targets, WeDo2 match pills+targets,
    Independent, Lundy zones, Exit x3): all populated
  - print pack sections (KO, arrival, starter, wedo, reference, exit, lundy): all populated
  - empty slides: 0 · empty task-boxes: 0 · generator-leak tokens: 0
  - level-switch reveal (arrival+exit supported/standard/stretch): all show populated content
- Described defect family (registerXP/xpCount/xpFill/timer-pill chassis organ throw): ABSENT — these
  files contain no registerXP/xp* symbols at all; nothing to throw.
- Screenshots: _passfin1/shots_W1/slide00..09 (all 10 slides render fully).

## VERDICT: §1 STOP condition MET — no reproducible pupil-content defect in 8×2 modes.
Per master prompt §1: STOP, report matrix, await Matt's specific lesson/slide. Do NOT fix by guesswork.
Consequently §2 (fix) has nothing to fix; §4 (ship) has nothing to merge. §3 estate sweep deferred —
pass is gated on the repro Matt will supply.

## REPORT-ONLY / AMBER findings (not the pupil-content bug)
- [AMBER] /hud.js referenced by 218 tracked HTML files as <script defer src="/hud.js">, absent from THIS
  repo. NOT a production defect: no CNAME here -> served as project page madebymatt.uk/lessons/, so
  absolute /hud.js resolves to the user-page repo root (mattroper1977.github.io/hud.js, which exists).
  Over file:// it 404s but content still fully populates (HUD overlay is cosmetic/optional). Report-only.
- [INFO] WAGOLL region absent in all 8 BUILD_HUM by design (BUILD pathway uses I-Do modelling; 7 I-Do
  blocks/file). GROW/LAUNCH humanities live at Grow/Slideshows/ and Launch/Slideshows/. Not a defect.

## REDs standing
frozen science untouched · no assessed conditions blocks touched · no parked branch touched ·
no deletion · no history rewrite · nothing merged/pushed.

## §3 ESTATE CHECK RESULTS (triggered by PACK-1 RUN CONDITION — read-only)
- §3.2 resources.json: VALID JSON, 411 entries (active YEAR 2026-27 = 267). 0 missing active-year
  local files. 3 "missing" = external GitHub tree URLs (type=teacher, subject=Planning, year=2025-26)
  — external-by-design, not local files. hub_chip_gate.js (LL chip gate): PASS across 21 subjects
  (every in-collection chip advertises what render() returns; Science·Teesside 25/25). ✓
- §3.3 frozen science hashes 2ce19ce vs HEAD: Science_Teesside 96d872b=96d872b, biology 2fdbd43=2fdbd43,
  chemistry 422e322=422e322, "2 Physics 10" 6ed42d1=6ed42d1 — ALL UNCHANGED ✓
- §3.4 LL-INST-09 loop_mark_print_gate spot sample (2/pathway incl science): PASS —
  CAREERS_W1, CAREERS_W2 (BUILD_ASDAN), BUILD_DT_W1, BUILD_DT_W2 (Build), SCI_B_W3, SCI_B_W4 (Science)
  × 3 tiers × 17 assertions all pass. Loop-mark reaches paper in all sampled. ✓
- §3.5 sentinel universes: tracked *.html = 459 at 88d6d32, 459 at HEAD, 459 working. UNCHANGED.
  Delta: none — §2 applied no fix, so no content/file-count change vs 88d6d32 (as expected). Working
  tree clean except _passfin1/ (untracked measurement artefacts). ✓
- §3.6 print-parity BUILD_HUM_W1 all tiers: 8 print sections visible/populated per tier, 0 empty.
  print-lundy NOT on paper in any tier -> CONSISTENT WITH R-A07 (VERIFIED RECORD): the zero is
  DIFFERENT_MODEL not ABSENT; Lundy Loop is on-screen class activity, not a printed sheet. Adding
  'lundy' to printPack is the RULED ANTI-PATTERN (REGISTER.md:816). NOT a defect; NOT to be "fixed".

## §3.1 render sweep — classification rule
FAIL trigger = script error OR uncaught pageError OR non-benign network failure (hud.js+favicon stubbed).
So far 0 code/script/page errors. All failures are EXTERNAL-CDN/asset deps blocked by sandbox network
(YouTube thumbnails i.ytimg.com, Google Fonts, jsdelivr canvas-confetti/three.js). These load on the
live site (public CDNs) but FAIL OFFLINE — material for PACK-1 offline packs. Full list on sweep end.

## §3.1 RENDER SWEEP FINAL (459 files)
- 84 flagged / 459. Network-independent code defects that break ONLINE: 0. Humanities failures: 0.
- (A) Offline functional breakers (JS libs): jsdelivr x8 (Games + 5_6 Local Choice), tailwind x2, cdnjs x1
      (Neon_Snake "THREE not defined" — downstream of blocked cdnjs three.js).
- (B) Cosmetic offline: Google Fonts x75, YouTube thumbnails x52, youtube-nocookie x1.
- (C) Absolute-root shared assets: index.html + primary/index.html -> /theme.js (resolves at domain root
      in production via user-page repo, same class as /hud.js). Not defects.
- Concentrated in primary/ (53) and Games/ (17). Core BUILD/GROW/LAUNCH lesson chassis + all humanities:
      ZERO external deps -> fully offline-safe. Full list: _passfin1/SWEEP_FAILURE_LIST.md
- §3.1 fix rule ("fix only humanities-bug-class failures"): NOTHING to fix — zero humanities failures.

## FIN-1 CLOSURE STATE
- §1 bug did NOT reproduce (8x2 clean). No fix. Nothing merged/pushed. main unchanged at 6549625.
- §3 estate check complete (items 1-6). §3.6 print-lundy zero = R-A07 DIFFERENT_MODEL (ruled, not a defect).
- §4 ship: N/A (no fix to ship). §5 report delivered to Matt.
- PACK-1 gate: §3.1 report-only failure list emitted for Matt's read (_passfin1/SWEEP_FAILURE_LIST.md).

## FIN-1 FOLLOW-UP (Matt's 2 pre-PACK-1 items)
- Item 1 Art print-pack population: all 8 Art_Teesside/Build BUILD_ART W1-W8 PASS LL-INST-09
  (17/17 x3 tiers, 9 sections/paper). §3.1 console sweep: Art_Teesside/Build 0 failures. Offline-safe.
- Item 2 Art ZIP verdict: committed pipeline build_staff_pack.py -> MadeByMatt offline BUILD Art copies
  BYTE-IDENTICAL to repo modulo intended hud.js strip (-38b). LL-INST-09 on offline copies PASS. No
  transform data loss. CAVEAT: pipeline is a reconstruction of a 404'd original; cannot diff a lost
  builder. If Matt's zip predates it, need the actual zip or a rebuild-from-committed.
