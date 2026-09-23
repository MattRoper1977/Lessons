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

## Job 10 pupil-voice pages: skip-link fix (accessibility; ruling 2026-09-23)

Public pages under `find-out-more/pupil-voice/<pathway>/` (landed in the Job 8/10 public PR). The skip link sat at
`left:-9999px`, which the PACK-1R 390/1280 harness reads as an element beyond the viewport (6 FAIL at 390). It now sits
on-screen at `left:12px`, visually hidden with `clip-path:inset(50%)` until focused, where `clip-path:none` shows it.
Harness 12/12 PASS; Tab focuses the link and it shows at left 12 px; still one A4 page each. CSS only; no text changed.

| page | Job 10 delivered sha256 | landed sha256 | reason |
|---|---|---|---|
| `find-out-more/pupil-voice/build/BUILD_Six_Cards_A4.html` | `20c73211a2e854cc4ebae199a8213d0afd6894038252a51f00662ae7701cc896` | `586e14fac41b595e633b242e0aee01c8cbd96d941ae29daeacee54798f74a2cc` | skip-link |
| `find-out-more/pupil-voice/build/BUILD_Wall_Poster_A4.html` | `5dd3e52ffdf72e6f5aea06ae3503a0772f0b96c53b706c1d65d0c4fe582bcd22` | `1095e5bb24c33910bcf0e617f411cdb2bf3c8eb3567c69f8e54202e05a08ae14` | skip-link |
| `find-out-more/pupil-voice/grow/GROW_Six_Cards_A4.html` | `480268b4c6cdf9deda7a814938954f8f1186835548a68837d2cbe69421e29cfa` | `9a27d83f56292f158ebc3349ebccd4477054db8dcbbf4353e0684465065a81cc` | skip-link |
| `find-out-more/pupil-voice/grow/GROW_Wall_Poster_A4.html` | `2022d7ba6c9151fe9573f0849becda3b68c065ec4d84dcc84237febb6e823594` | `432d4749755688af97f846bf1a09eac84b1036a85c4c39d8b472fec9238f4cf2` | skip-link |
| `find-out-more/pupil-voice/launch/LAUNCH_Six_Cards_A4.html` | `7c747f5f346328d6922de72840cce76d07bb02f7893dc9b608f08c25eb245a31` | `4cb6d5c25c8abd5e99fd676172b129a7bb993c623b4fafd86b329cd5982ef7ad` | skip-link |
| `find-out-more/pupil-voice/launch/LAUNCH_Wall_Poster_A4.html` | `55e815755378389364c7b637d151215ee6795d63638921e3a1717c43c939b224` | `e3ec1978801dd38ee92a9104c4e78c637b89a804913364e4a2c27e0a1168271d` | skip-link |
