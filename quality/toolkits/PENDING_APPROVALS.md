# PENDING_APPROVALS — the TK-1 sign-off ledger

**STATUS: live ledger · OWNER: Matt · created at the TK-1 close (2026-08-04), so the sign-off list survives
the chat that produced it.**

The four TK-1 merges landed wording that is **strictly safer or more conservative** than what it replaced —
that is why it merged ahead of sign-off (Matt's ruling, TK-1 Close §1: withholding a correct safety instruction
pending approval would leave the wrong one live). The PENDING-LOCAL-APPROVAL tags in the files themselves keep
the approval state honest. **This ledger is the checklist that retires them.**

When a row is signed: tick it, date it, replace the in-file `PENDING-LOCAL-APPROVAL` tag and any
`[local ref]` / `[date]` placeholder with the real reference, and note the commit here.

| ☐ | owner | what needs signing | file(s) | current wording (summary) | status | date signed |
|---|---|---|---|---|---|---|
| ☐ | **First-aid lead** | Burns wording and the escalation route | `Art_Teesside/House_Standard_and_Safety.html` · `Art_Teesside/Launch/Printable_LAUNCH_Evidence_and_Lundy_Pack.html` | *"cool running water for at least 20 minutes, as soon as possible… follow the centre's first-aid escalation… Cool, not cold."* Checked 2026-08-04 against NHS burns first aid; review 1 Sep 2026 | **PENDING** | |
| ☐ | **H&S + safeguarding** | Missing-tool procedure — does the centre have a named missing-sharp procedure to point at? | the two files above + `Art_Teesside/Spring2_Scheme_of_Work.html` | *"stop work, count the tools in, tell a staff member straight away — staff manage movement and exits under the centre's missing-sharp procedure. Pupils are never collectively held."* | **PENDING** | |
| ☐ | **H&S / technician** | Pallet acceptance criteria (six checks, reject on any single failure even when HT-stamped) | `BUILD_ASDAN/Resources_and_Tools.html` | stamp · provenance · contamination · coatings · condition · magnet sweep | **PENDING** | |
| ☐ | **H&S / COSHH / technician** | Dust hierarchy, RPE selection, named stop condition | `BUILD_ASDAN/Resources_and_Tools.html` | prevent → extract → RPE; *"if visible dust is being raised that extraction is not capturing, work stops and an adult is told"* | **PENDING** | |
| ☐ | **DPO / SLT** | Retention defaults (current term) and the approved-device rule for local-only tools | `LundyLoop/2_leadership/Loop_Walk_Logger.html` · `quality/toolkits/DATA_GOVERNANCE.md` | opening notice: what is captured, why, where it stays, retention, deletion, export handling | **PENDING** | |
| ☐ | **DSL** | Firewall wording + the unsaved "safeguarding handoff made" tick — **fold into the DSL sitting already planned for PR #33** | `LundyLoop/2_leadership/Loop_Walk_Logger.html` · `LundyLoop/2_leadership/Impact_Monitoring_Crib.html` | *"Not for disclosures… it goes to the DSL by the school's safeguarding route — never into a box on this page."* Tick stores no detail, never exported | **PENDING** | |
| ☐ | **DSL** | Science evidence disclosure boundary — the Science-specific moments where a disclosure surfaces (caption, health/food topics, photographs, group data, verbal aside) | `quality/LUNDY_SCIENCE_DATA_FIREWALL.md` | *"A disclosure leaves the ordinary evidence workflow entirely… never a caption, queue, board, handoff note, portfolio note or moderation sample."* Reuses the ruled `DATA_GOVERNANCE.md` firewall wording verbatim; asserts nothing PR #33 has not settled and defers to #33's outcome | **PENDING — review at the same DSL sitting as held PR #33** | |
| ☐ | **SENCo + exams officer** | JCQ classroom-practice wording | `LundyLoop/4_send_and_pupils/SEND_Overlay.html` · `LundyLoop/4_send_and_pupils/Loop_Passports.html` | *"a classroom-practice record… does not establish or guarantee a JCQ access arrangement"* + the SENCo/exams-officer gate named | **PENDING** | |
| ☐ | **RSHE lead / DSL** | Statutory version gates | `Tutor_Time/START_HERE.html` · `Tutor_Time/Scheme_of_Work.html` · `build_asdan.html` | KCSIE 2025 until 31 Aug 2026 · KCSIE 2026 from 1 Sep 2026 · RSHE statutory guidance mandatory 1 Sep 2026 | **PENDING** | |
| ☐ | **Cheryl (ASDAN/UAS coordinator)** | Short Course vs PEQ display on the hub | `BUILD_ASDAN/BUILD_ASDAN_Hub.html` | non-regulated Short Course (no grade, no level) vs regulated PEQ (unit, code, credit); registration DONE | **PENDING** | |
| ☐ | **Matt** | The `[local ref]` / `[date]` placeholders across every changed safety surface | all safety files above | placeholders deliberately unfilled — a fabricated reference would be worse than a visible gap | **PENDING** | |

**Standing rule carried from `SAFETY_CONTENT_GATE.md`:** a signed row means a person read the wording in the
file, not this summary of it. Review-by for every row: **1 September 2026**.
