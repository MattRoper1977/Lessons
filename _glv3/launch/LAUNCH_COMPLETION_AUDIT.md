# LAUNCH Estate Outstanding v3 — completion audit

Repository: MattRoper1977/Lessons
Current repo main resolved during LAUNCH audit: 651a88ecf2f760c61fa2a221dc9b3351731e6f4e
GitHub writes: NONE

## Authoritative Autumn-1 v3 lesson scope
| Suite | Lesson files |
|---|---:|
| Science | 15 |
| Art · Silver Teesside Studio Suite | 8 |
| Humanities · GCSE Bridge | 8 |
| LAUNCH ASDAN | 30 |
| TOTAL | 61 |

## LAUNCH demand
- infer and evaluate;
- synthesise multiple sources/considerations;
- plan and execute sustained outcomes;
- transfer to unfamiliar contexts;
- explain limitations/trade-offs;
- lead/delegate/pilot/adapt;
- review impact and specify next action.

Access supports remain; reduced scaffolding targets thinking, not accessibility.

## Feedback / Lundy
Space: stable seating/adult, clear deadlines, no public grading.
Voice: in-lesson edit, structured verbal response; extended writing can use deferred edit.
Audience: adult genuinely engages with response against model/criteria before R.
Influence: next instruction, assessment/intervention plan, target or project action changes.

## Protected / claims boundaries
- Humanities W7: protected assessed source evidence; no live content support/post-hoc answer enhancement.
- Silver Art: trained adviser audits both units; hours are guidance, not a threshold.
- ASDAN PEQ: current repo hub says E3–L1 in 2026/27; L2 wording is stretch language only, never L2 registration.
- Careers current information is checked at time of use.
- Vocational HTML is not a risk assessment, induction or competence authorisation.
- Community/Enterprise never invents a partner, permission or impact.

## Post-verification edits applied 2026-08-10 (Claude, pre-deployment)

Verified independently, not from this pack's claims: **0** localStorage / sessionStorage / IndexedDB /
cookies / fetch / XHR / sendBeacon / `<form>` / `eval(`, and **0 external URLs**, across every file.
**Zero mark schemes, band or level descriptors, grade boundaries, AO codes or mark allocations across all
71 files** — the LAUNCH red line holds, including W7L2 Command Words and W7L3 Exam Practice.
**Zero Arts Award hours thresholds** in the v3 art files, matching live. Silver Unit tags mirror live
exactly at W1–W7 (1A · 1D · 1B · 1C · 2A–B · 2C–D · 2C–D).

Two changes were made. Nothing else.

1. **`Science/` REMOVED (21 files).** Its 15 lessons are the earlier test bundle, superseded by the installed
   `Science_Teesside/Launch/v3_40min/` route. Verified per file: **the closure line "What I said, and what it
   changed" appears 0 times in all 15**, where the installed route carries it in all 15 — it was added
   deliberately and moved the estate sentinel from 98 to 113. `SCI_L_W3L1` also still carries the `Aut1·W2`
   baseline error twice. Installing this folder would strip the closure line from the LAUNCH pathway and
   reintroduce the baseline error. Removed at source so no glob can sweep it in.
   **Lesson count for deployment is therefore 46, not 61** — Art 8 · Humanities 8 · ASDAN 30.

2. **Print-tier defect fixed in 8 files** (Humanities). `<body>` carried no `data-tier` while
   `.proute{display:none}` was lifted only inside `printTier()`, so any plain browser print silently dropped
   every tiered task and scaffold. Print default now shows all three routes; a print button still selects one;
   the 500 ms `setTimeout` was replaced with an `afterprint` listener.

Known and NOT changed here — see the deployment master prompt:
- **the 8 Art and 30 ASDAN lessons have no print pack at all** — zero `@media print`, no print button.
  38 of the 46 deployable lessons are screen-only, on the pathway whose Silver Art portfolio and PEQ
  evidence both depend on paper;
- **v3 `LAUNCH_ART_W8` tags Unit 2E alone**, where live tags all five ranges (1A–B, 1C–D, 2A–B, 2C–D, 2E).
  W8 is the portfolio audit; live's tagging is what an Evidence Locator Form needs. Reported, not changed;
- **"new art form" appears 0 times** in both live and v3 — a long-flagged Silver Unit 1 gap, correctly not
  invented here.
