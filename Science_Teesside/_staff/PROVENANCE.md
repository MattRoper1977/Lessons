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
