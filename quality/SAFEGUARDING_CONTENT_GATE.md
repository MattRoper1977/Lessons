# Safeguarding content gate

> **Source: SEMH audit 2026-08-04, adapted.** Corrections the auditor could not know are
> marked **[estate]**. **Nothing in this file is a substitute for the DSL's judgement.**

## Scope

Every pupil-facing resource that carries a legal claim, a safeguarding statistic, a help
route, or a route by which a pupil can disclose something. At `6aaffb7` that is
**10 files** in `Tutor_Time/` (`WB_W1`–`WB_W8`, `KCSIE_Deepfakes_Screenshot_Culture`,
`KCSIE_Vapes_Rumours_and_Facts`) plus any RSE/consent material.

## Gate 1 — Volatile claims carry a date and an owner

No pupil-facing legal or statistical claim ships without: official source · publication
date · verified date · **review-by date** · named owner · replacement action on expiry.
Recorded in `QUALIFICATION_CLAIMS_REGISTRY.json`.

**Dated facts as at 2026-08-04** — all four marked
`supplied-by-audit 2026-08-04, review-by 2026-09-01, verify-live: Matt`, because the
agent environment cannot reach official sources:

- **KCSIE 2025 is statutory until 31 August 2026. KCSIE 2026 is in force from
  1 September 2026.** A lesson must not say "KCSIE 2026" without the effective date.
- **Not all deepfake/intimate-image offences trace to the Online Safety Act 2023.**
  Adult purported-intimate-image creation/request offences commenced **6 February 2026**
  under the Sexual Offences Act framework; further generator offences commenced
  **June 2026**. Child sexual imagery was already covered by separate law.
- Legal detail must be **brief, dated and DSL-approved**.

## Gate 2 — Help routes are correct and scoped

| route | for | not for |
|---|---|---|
| **CEOP** | online sexual abuse and grooming | ordinary bullying, hacked accounts, fake accounts |
| **Report Remove** | eligible under-18s in the UK reporting sexual images/videos **of themselves** | third-party images |
| **Childline 0800 1111** | anything, 24 hours a day, 7 days a week | — |
| **999** | immediate danger | — |

**Professionals follow local safeguarding procedure. They do not use the public CEOP
reporting form.**

## Gate 3 — Statistics are sourced or softened

A pupil-facing statistic needs a **named dataset and context**, or it is reframed at
pattern level. A sample of indexed videos is not the prevalence of every form of
deepfake. **The practical safety action matters more than a dramatic number.**

## Gate 4 — Disclosure separation and staff review

**[estate] Verified at `6aaffb7` — the estate already satisfies most of this. Read
before "fixing" anything.**

Already true across all 10 files:

- **No pupil words persist on the device.** Anonymous text lives in an in-memory
  `_voices` array and never reaches `localStorage`. The persisted evidence payload is
  `{completed, date, xp}` only. Free-text-persistence detector: **0 hits / 17
  `Tutor_Time/*.html`**, replayed against a must-hit synthetic.
- **DSL handoff wording exists**, including a sign-off table with *"Items passed to DSL"*
  and *"DSL signature / date"*, and a warning that timestamps can identify a pupil in a
  small group.
- **Roster names are time-boxed to 14 days** (`ROSTER_TTL_DAYS = 14`) with automatic
  expiry.

**The one real gap:** the anonymous text reaches staff **only** through
`printEvidence()` → `window.print()`. There is no on-screen review surface, and lesson
completion is not gated on unreviewed messages.

### What the gate therefore requires

1. Safeguarding disclosure is **separated** from ordinary learning evidence.
2. An **on-screen staff review surface exists before print**. Print remains available as
   the durable artefact — it is no longer the only route.
3. A **mandatory review state**: the lesson cannot be marked complete while unreviewed
   anonymous messages exist. Reviewed / referred / no-concern is recorded **without
   retaining the disclosure text**.
4. Session memory during the lesson is acceptable. **Nothing pupil-written survives it.**
5. Explicit DSL handoff wording and the dated claims above.

### What the gate forbids

**[estate] Do not touch the roster keys.** `_CC_KEY` (`mbm_cc_v1`) and its documented
fallback `ps_coldcall_roster` sit behind an explicit in-file warning: *"NEVER read, parse
or rewrite the roster value itself — two different data models live behind these keys and
both break if you touch the shape."*

`coldCall_y10` holds `{name, grade}` objects driving tier-matched questioning in 3 files
and **must never be naively migrated in either direction**: strings→objects breaks 14
`.join(', ')` readers; objects→strings destroys the grades and permanently disables a
start button. `ps_coldcall_roster` name persistence across ~66 files was **accepted by
Matt as-is** (school-owned machines). **There is no estate-wide roster purge.**

## Gate 5 — Participation safety

Cold calling is inappropriate where an answer could reveal trauma, abuse, sexuality,
family history or current risk. Personal/family routes are **fictional by default**;
personal history only by informed opt-in. A "pass" is genuine and is not followed by
public pressure.

**[estate]** A fictional character with a provenance comment is **not pupil data**. Do
not classify one as such.

## Authorisation

**Safeguarding corrections land after DSL approval.** No safeguarding change in this
estate is self-merged, regardless of how green its gates are.
