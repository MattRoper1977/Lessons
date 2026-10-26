# Provenance · Science_Teesside/_staff (ORDER LW-4 §1)

Staff-facing, never served (the `_staff` segment is refused by the education publisher).
Source: Job 9 `JOB_9_Walk_Visible_Routines.zip`, sha256
`963a0e15692dbc7eeea5862db3ea761a78a673d22cfdaf725b2a0e0830f27010` (passed by Claude
2026-09-23; held as delivered in `Lessons/_incoming/lw1/`, never modified).

## Landed copies that differ from the delivered bytes

| landed file | delivered sha256 (Job 9 SHA256SUMS) | landed sha256 | change | reason |
|---|---|---|---|---|
| `Science_Hinges.csv` | `f2f9ae354e84eb825b20425d2880eb5b05d5ddc0fd6554e2d81cc9629fabba12` | `4813e764f4444879b977f895c16e01d2d599d75fc61b282076a62c14c3b2946d` | CRLF → LF line endings only (109 lines); content otherwise byte-identical | CRLF, `git diff --check` (cross-estate / static-contract refused it as trailing whitespace). Accepted by Matt 2026-09-23. |
| `<SCI_ID>/TA_BRIEF.md`, `<SCI_ID>/TEACHER_NOTE.md` (18 ids each, in the pathway folders) | per Job 9 SHA256SUMS | — | one line: `NONE — flag` → the ruled teacher-time default | TEACHER-TIME ruling (Matt, 2026-09-23) |
| `<P>_A4_Science_AfL_Quick_Record.html` (3, in the pathway folders) | per Job 9 SHA256SUMS | — | one token: `E EFL evidence` → `E {EVIDENCE_APP} evidence` | forbidden names; the ruled staff placeholder |

Every other landed file is byte-identical to the delivered file.

## {EVIDENCE_APP} = Cypher (ruling 2026-09-23) — every LW-4 staff file, all folders

Recorded here for the whole LW-4 §1 landing (Humanities, Science and find-out-more `_staff/`
folders alike). Held zips and their extractions in `_incoming/lw1/` stay as delivered; only the
landed copies change. 111 landed files; every other landed file is unchanged by this ruling.

| job | files | change |
|---|---|---|
| Job 9 | 36 `TA_BRIEF.md` | `{EVIDENCE_APP}` → `Cypher` ("E: evidence captured on Cypher") |
| Job 9 | 3 `<P>_A4_Science_AfL_Quick_Record.html` | code key `E {EVIDENCE_APP} evidence` → `E evidence captured on Cypher`; one line added under "Quick record · week ____": "Record on the paper grid or straight into Cypher on the tablet — one or the other, not both." |
| Job 5 v2 | 3 `<P>_A4_AfL_Quick_Record.html` | the same two changes as the Science sheets |
| Job 10 | 3 `TA_Teacher_Briefing.md`, 3 `TA_Teacher_Briefing_A4.html` | `{EVIDENCE_APP}` → `Cypher`; the same grid line added after the feedback code map, before "Close the loop" |
| Job 8 | 63 `STAFF_CARD.md` | `{EVIDENCE_APP}` → `Cypher`; "Staff device or projector" → "Staff device (school tablet) or projector" |

Job 9 `CODE_MAP.md` files carry no placeholder and are unchanged. Print: the six AfL sheets
still render as one A4 page each; the briefing renders two pages, as before. No landed file is
served (the `_staff` segment), so "Cypher" appears on no public route.

## Job 11 regulation layer (passed 2026-09-23; ORDER LW-4 addendum 2)

Source: `JOB_11_Regulation_Layer.zip`, sha256 `34f63f914edcb7dea69c878b3dfb0d52353c4879898358ea2b40ddb8d3e58a9a`
(SHA256SUMS 43/43), held as delivered in `_incoming/lw1/`. Landed byte-identical: 36 `REGULATION_PLAN.md` beside each
TA brief (the `[confirm current …]` brackets stay as delivered: staff fill them per pupil, never in the repo);
`REGULATION_SCRIPTS.md` and `JOB10_BRIEFING_ADDON/EMOTION_COACHING_CARD.{html,md}` beside each copy of the Job 10
briefing (3 Humanities `Summer_1/_staff/` folders); `TA_Teacher_Briefing_Print_Pack.pdf` there = the briefing (2 A4
pages) + the card (1 A4 page, A5 two-up), rendered in Chromium from the landed HTML.

`TA_BRIEF_REGULATION_PATCH_LIST.md` applied to all 36 landed briefs: its two lines inserted immediately before
`## Teacher time and handoff`. One change to the delivered lines: the pack path
`JOB_11_Regulation_Layer/<HUM|SCI>/<id>/REGULATION_PLAN.md` reads `REGULATION_PLAN.md` (beside this brief), because
the plan lands in the brief's own folder and the pack layout is not landed. The patch list's target hashes are the
DELIVERED Job 9 briefs (36/36 match the intake); the landed briefs had already moved under the TEACHER-TIME and
Cypher rulings, so the hashes below are the landed brief before and after this patch.

| brief | delivered (patch-list target) | landed before | landed after |
|---|---|---|---|
| `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/_staff/TA_BRIEF.md` | `959788be12ed` | `66d440551e2c` | `d28e9ed7ad20` |
| `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/_staff/TA_BRIEF.md` | `52c7d675146c` | `c5b27bc16783` | `e55b49716400` |
| `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/_staff/TA_BRIEF.md` | `86a7237bf9be` | `d9417560d162` | `9244173372c0` |
| `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/_staff/TA_BRIEF.md` | `b0d6e9b5499e` | `24c413eeaf8c` | `bd6a9bcc0f03` |
| `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/_staff/TA_BRIEF.md` | `925190979d8a` | `608a0cb04948` | `492c7592bca9` |
| `Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/_staff/TA_BRIEF.md` | `ff383f5eb619` | `4fe112dd5ed6` | `3550dbc1a874` |
| `Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W01/_staff/TA_BRIEF.md` | `58ad7bfafbe8` | `84cc5e028389` | `e4677335086a` |
| `Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W02/_staff/TA_BRIEF.md` | `8203b9deb7dc` | `f22d93ed9678` | `613953445ba2` |
| `Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/_staff/TA_BRIEF.md` | `f575f5b60b29` | `203276c9498b` | `f3490c954df6` |
| `Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/_staff/TA_BRIEF.md` | `83adfbb97395` | `59cd6ce9fdf1` | `f1d5c286f93b` |
| `Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/_staff/TA_BRIEF.md` | `e7f088ff1ce0` | `ba8f596ea647` | `b6081f08a99f` |
| `Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/_staff/TA_BRIEF.md` | `57a4f89f8a97` | `108a93f0d488` | `e0b8e34e8883` |
| `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/_staff/TA_BRIEF.md` | `43879bb31435` | `32e099ea7337` | `f5a569244b7d` |
| `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/_staff/TA_BRIEF.md` | `4ec584dbee56` | `3e7388fa5491` | `e380fed313ec` |
| `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/_staff/TA_BRIEF.md` | `1235e4dfbf40` | `3325c14a401a` | `f9b7ebe4181d` |
| `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/_staff/TA_BRIEF.md` | `6941cc8a2b1f` | `5b02f8edc689` | `cb817fafa40b` |
| `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/_staff/TA_BRIEF.md` | `81fa72b5da88` | `03e0193195df` | `8f7087fd1728` |
| `Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/_staff/TA_BRIEF.md` | `99c2126f75ca` | `aba69d5a94ba` | `4715d058a4c6` |
| `Science_Teesside/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W01/TA_BRIEF.md` | `eb042d6f8e6c` | `1b07d40b1071` | `4d736ec23552` |
| `Science_Teesside/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W02/TA_BRIEF.md` | `afaf9e0dc47f` | `09c1ca653266` | `9f2180e95614` |
| `Science_Teesside/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W03/TA_BRIEF.md` | `ded3896d7f4e` | `c5c1441ce468` | `f0ebe46c6820` |
| `Science_Teesside/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W04/TA_BRIEF.md` | `f10f2cb5233a` | `a9198f4358a6` | `8add803611c3` |
| `Science_Teesside/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W05/TA_BRIEF.md` | `1e6aa1b91540` | `f2626cf7da3c` | `97f262d1e068` |
| `Science_Teesside/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W06/TA_BRIEF.md` | `52325e6ec20d` | `31cb9545b9f9` | `9b031cf913ec` |
| `Science_Teesside/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W01/TA_BRIEF.md` | `3f86d9fa59a5` | `ea9869be22d5` | `63546c8c2bc4` |
| `Science_Teesside/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W02/TA_BRIEF.md` | `c5827f0be07f` | `d9d62c1625bd` | `abc8100fe5fe` |
| `Science_Teesside/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W03/TA_BRIEF.md` | `000c5b98a87b` | `13538fadc074` | `76f9d9a3607f` |
| `Science_Teesside/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W04/TA_BRIEF.md` | `08a201486aa8` | `c7e084723a3a` | `e9e1e319978e` |
| `Science_Teesside/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W05/TA_BRIEF.md` | `5b18289e0cce` | `e677093c6a86` | `9be3667d9606` |
| `Science_Teesside/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W06/TA_BRIEF.md` | `246e462e3959` | `48fb36db93f7` | `5dd50bfc7435` |
| `Science_Teesside/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W01/TA_BRIEF.md` | `f23c29c2e1cc` | `53044ab3cd98` | `d2628e2dbc72` |
| `Science_Teesside/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W02/TA_BRIEF.md` | `fcfe6949fff6` | `058e453d86f6` | `5ba509eca808` |
| `Science_Teesside/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W03/TA_BRIEF.md` | `2327c91ab5b1` | `7e0e191868f5` | `846727993e3a` |
| `Science_Teesside/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W04/TA_BRIEF.md` | `72178703440c` | `437363c91d77` | `5ead0d772a35` |
| `Science_Teesside/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W05/TA_BRIEF.md` | `972399c9975c` | `2a7cf27643d8` | `d0fa0a5a9593` |
| `Science_Teesside/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W06/TA_BRIEF.md` | `af3d43d88fab` | `4c885f9b303f` | `8b6313307fda` |

**Whitespace in the 36 landed `REGULATION_PLAN.md` (`git diff --check`, the CRLF precedent of 2026-09-23):** the
delivered plans end line 3 with a two-space Markdown hard break (36) and line 27 with one stray space (35), which
`git diff --check` refuses as trailing whitespace. Landed copies: the hard break is written as a trailing backslash
(CommonMark's equivalent form) and the stray space is removed. Rendered with CommonMark, delivered and landed plans
produce identical HTML, 36/36. No other byte differs from the delivered plans.
