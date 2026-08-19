# P2 FieldOps FINISH — F0 verdict: the prompt is STALE; report and stop

**Sentinel context:** `p2-fieldops-finish-2026-08-19`. F0 rules: "The FieldOps
APPS (labs + Studio) are NOT in either repo and NOT live. … If they ARE present,
this prompt is stale — report what exists and stop." They are present, in both
repos, as a ruled and gated placement. This file is the report; nothing beyond it
was executed. Every figure below was measured this session (R0.2).

## F0 confirmations that DID hold

- `origin/main` = `fdd0a34`, descending via `9919a74` — both ancestor-checked.
- FieldOps CI run **32288345978** on `9919a74`: all six jobs success, including
  "The sweep over all three estates" and the planted-stale qa-record control;
  Watch main green (32288393865, 32288726959); Pages success at `fdd0a34`.
- The 20 Matt-s-Apps- QA rows: untouched, as ordered (the A3 repair was
  grammar-side in Lessons and stands green).

## The F0 premise that did NOT hold — what actually exists

| F0 claim | measured |
|---|---|
| labs not under `Science_Teesside/` | **present**: `Science_Teesside/Build/v4_fieldops/01–04_*.html`, each **byte-identical to `tools/fieldops/staging/`** (the patched build) |
| Studio not in Matt-s-Apps- tools area | **present**: `FieldOps_Teacher_Studio.html` at the Apps repo **root**, sha `6678059f…` — byte-identical to the patched staging Studio |
| not live | Lessons Pages **success** at `fdd0a34` (labs are in that tree). Apps Pages: no `pages build and deployment` run in the last three workflow runs — not confirmed either way from here. Live-origin pin: **raw-pin NOT RUN — network blocked** (000 from this environment). |

This placement is not an accident to be corrected: it is the **ruled position of
2026-08-16** — `CONVENTIONS_EXEMPTION_fieldops.md` names exactly these two paths
("Subjects: `Science_Teesside/Build/v4_fieldops/01–04`, and their counterpart
`FieldOps_Teacher_Studio.html` in `Matt-s-Apps-`"), records the estate-fit
transforms (NAV-1, Made-by-Matt) as inherited on the placed files, and the CI job
"Merged is not served — the placed labs and the Studio"
(`tools/verify_fieldops_served.mjs`, which names both paths) is **green** on main.
Executing F1–F3 on top of it would have re-placed the labs at a second folder
(`Science_Teesside/Build/FieldOps/` — currently 0 files), re-applied patches that
are already in the deployed bytes, and stripped a `SAMPLE_MISSIONS.html` that was
never committed. Stale premise, correctly halted.

## Genuine residue found while proving the staleness — owner-held, not executed

Measured gaps the FINISH prompt's F2 would have addressed and which remain real
after the staleness verdict (each one measurement, with its selector):

1. **Studio→labs links are unrewritten for the split.** The placed Apps Studio's
   engine table still reads `file:'01_Newport_Bridge_Lift_Permit_Lab.html'`
   (relative, all four) and contains no absolute URL to the Lessons origin —
   "Launch mission" on the Apps origin resolves to a path that exists only in the
   Lessons tree. The governing prompt §3 called this "the likeliest thing to
   break the pack's best feature"; it is broken in exactly that way.
2. **Labs carry no link to the Studio** (0 hrefs matching studio/apps in lab 01).
   May be deliberate — pupils don't need the teacher tool — but unproven either way.
3. **Nothing links the labs**: `v4_fieldops` appears in no tracked html/json
   outside `tools/`, and `resources.json` has **0** FieldOps entries. Served but
   unreachable by navigation.
4. **No Apps catalogue/homepage card**: 0 `FieldOps` mentions in the Apps
   `index.html`; no `*.json` in the Apps root mentions it.

Whether 2–4 are gaps or rulings ("instruments, not lessons" may deliberately keep
them out of the lesson catalogue) is the owner's call; item 1 looks like a plain
defect. A corrected FINISH prompt should start from the placed files at their
real paths, not from the release pack.

## The sweep-vs-new-folder statement F1 asked for

Moot as ordered (no new folder was created), but for the record: the sweep's
forward universe is tracked files matching `/(^|\/)(evidence|qa)\//` with
extensions `.out|.json|.txt|.md|.log`. A future `Science_Teesside/Build/FieldOps/`
folder of html labs would be **outside that universe** unless it shipped an
`evidence/` or `qa/` subfolder; the placed `v4_fieldops` labs are likewise outside
it today.

## Owner-held list

- Rule on residues 1–4 above (1 = fix the Studio's launch links for the split and
  prove both transport directions per the governing §4; 2–4 = confirm or add).
- Staff-pack rebuild: unblocked (unchanged from the CLOSE v2 report).
- PROPOSED triage table: **exists** — `_sca1close/PROPOSED_RANKED.md` (written by
  SCA-1 CLOSE v2), with the underlying items in `_sca1/PROPOSED.md`,
  `_eca1/PROPOSED_A.md`, `_eca1/PROPOSED_B.md`.
- Phone-check URLs (when a session can reach the live origin, or from the phone):
  `madebymatt.uk/Science_Teesside/Build/v4_fieldops/01_Newport_Bridge_Lift_Permit_Lab.html`
  (boots, Calm works, no pupil text survives refresh) and the Apps origin's
  `FieldOps_Teacher_Studio.html` (forge → launch will 404 until residue 1 is fixed).
