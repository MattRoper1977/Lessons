# Delivery readiness checklist

> **Source: SEMH audit 2026-08-04, adapted.** The audit's central readiness finding:
> *"Presentation-ready is sometimes mistaken for delivery-ready."* Verified TRUE at
> `6aaffb7` — but as a **visibility** problem, not a truthfulness one. Hubs and schemes
> already state their unmet requirements in plain language; what is missing is a
> consistent, visible badge.

## The seven states

A resource is at exactly one of these. Later states assume all earlier ones.

| # | state | what it means | who can assert it |
|--:|---|---|---|
| 1 | **drafted** | Pedagogically written. Nothing verified beyond the author's judgement. | Author |
| 2 | **source-verified** | Every factual, local, legal and health claim has a named source and a verified date in `QUALIFICATION_CLAIMS_REGISTRY.json`. | Subject lead |
| 3 | **locally-adapted** | Place, cohort, equipment and site risk controls are the setting's own, not the template's. | Subject lead |
| 4 | **delivery-ready** | A teacher can run it tomorrow with what the school has. | Subject lead |
| 5 | **registration-verified** | Where the resource banks toward a qualification, the centre registration exists and the exact unit/code is confirmed. | Exams / qualification lead |
| 6 | **assessment-ready** | Assessment conditions, adviser/IQA arrangements and evidence requirements are in place. | Qualification lead + IQA |
| 7 | **print-offline-verified** | Print packs render per tier at **718×1047px**, and the core teaching flow works offline. | Developer, **from a browser-capable environment** |

## Rules

**A strong average does not override a red blocker.** A resource may be excellent at
state 1 and unsafe to timetable because state 5 is absent. Readiness is a floor, not a mean.

**States 5 and 6 are centre actions.** No repository change can close them. Do not
represent a code change as having closed one.

**State 7 cannot be claimed from an agent container.** This estate's containers have no
browser: managed Chromium blocks `file://` and `localhost`, and print geometry cannot be
measured. A skipped gate is **UNVERIFIED**, never passed. Claim state 7 only from CI or
another browser-capable environment.

**Honesty already present must not be removed.** Examples at `6aaffb7`:
`LAUNCH_ASDAN/Scheme_of_Work.html` — *"(no registration is claimed here)"*;
`BUILD_ASDAN/BUILD_ASDAN_Hub.html` — *"nothing is certified until the awarding
organisation says so"*. These are the model, not the problem.

## Known integration risk — read before implementing a badge

Any change to `resources.json` **can silently mint a new hub chip**. This is a registered
trap. A readiness badge that is wired through `resources.json` is therefore a **separate,
authorised pass** with its own hub-chip cardinality assertion — not a side effect of
adding this checklist.

## Current estate readiness signals (measured at `6aaffb7`)

| signal | measurement | unit / universe |
|---|---|---|
| Files carrying an unconfirmed UAS unit code (`TBC`) | **25** | files / tracked `*.html` |
| Art lesson files with a self-contradictory timer contract | **24** | files / `Art_Teesside/**/*.html` |
| Art lesson files with a consistent timer contract | **7** | files / `Art_Teesside/**/*.html` (the A2 cohort) |
| Print execution evidence at 718×1047 for Art | **0** | executions / PRs #26 and #30 — **UNVERIFIED**, not passed |
| Tutor Time files whose only staff review route is print | **10** | files / `Tutor_Time/*.html` (17 total) |

Each figure was derived at the pinned SHA. Re-derive rather than quote.
