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
