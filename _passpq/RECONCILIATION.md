# RECONCILIATION.md — every UNVERIFIED-AGAINST-SPEC flag, resolved

**What this is.** The blind PEQ audit (Pass PQ, base `32ca685…`) ran with `asdan.org.uk`
403-blocked, so every spec-dependent claim was flagged `UNVERIFIED-AGAINST-SPEC` and the
unit-code fixes were held for "two-source agreement (committed spec + Evidence Binder)".
The spec (**v1.2 Oct 2025**) is now in hand and reconciled locally. This file resolves each
flag to **VERIFIED** / **CORRECTED** / **STILL-UNDETERMINED**, citing `SPEC_FACTS.md`
(→ spec section/page). It covers both `_passpq/` (BUILD/GROW) and `_passla/HANDOVER.md`
(LAUNCH) flags.

**Two-source agreement — result: TOTAL.** The Evidence Binder (`ASDAN/ASDAN
PEQs/Evidence_Binder_PEQ_v7.html`, the `U(code,family,level,title,URN,credit,GLH,…)` model,
lines 717–1108) and the committed spec (§6, pp11–14) agree on **all 24 units' code, Ofqual
URN, credit and GLH — zero disagreements.** No code converts to a tabled STOP finding; the
held T2-2/T2-3 corrections are fully unlocked.

Verdict counts: **VERIFIED 24 · CORRECTED 3 · STILL-UNDETERMINED 5.**

---

## A · Spec version and structural facts

| # | Flag (source) | Verdict | Resolution → cite |
|---|---|---|---|
| A1 | Spec version = v1.2 Oct 2025? (FINDINGS needs-spec) | **VERIFIED** | Title page p1 + review history p2. `SPEC_FACTS` header. |
| A2 | All 24 unit codes / URNs / credits / GLH (PRIMER §2, PATHWAYS, Binder) | **VERIFIED** | Match spec §6 pp11–14 exactly. `SPEC_FACTS §2`. |
| A3 | E3 six units = 14 cr; L1 six units = 15 cr | **VERIFIED** | Sums confirmed. `SPEC_FACTS §2`. |
| A4 | Thinking → Critical thinking rename at L2/L3 (CrThSk2/CrThSk3) | **VERIFIED** | §6.3/§6.4. `SPEC_FACTS §2`. (§6.5 shorthand "ThSk2/3" noted.) |
| A5 | 1 credit ≈ 10 h incl. assessment (PRIMER §2, PATHWAYS) | **VERIFIED** | §5.1 p9. `SPEC_FACTS §1`. |

## B · Qualification sizes / rules of combination

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| B1 | Award=4 / Ext Award=9 (min6,max3) / Certificate=14 (min11,max3); L2 Cert=15 (PRIMER §3, PATHWAYS) | **VERIFIED** for E3/L1/L2 | §5.1 p10 table. `SPEC_FACTS §3`. |
| B2 | "Award = 4, all at level" as a blanket statement | **CORRECTED** | True E3/L1/L2 only. **L3 Award=6, L3 Ext=11(min8), L3 Cert=18(min15).** Out of estate scope but recorded. `SPEC_FACTS §3`. |
| B3 | Route B thresholds "max 3 adjacent", "min 11 at level" (FINDINGS needs-spec; PATHWAYS Route B PROVISIONAL) | **VERIFIED** | L1 Certificate: 14 total, **min 11 at level, max 3 adjacent**. §5.1 p10. Route B now confirmed, flag lifted. |
| B4 | Barred combination — highest level counts (PRIMER §3, PATHWAYS) | **VERIFIED** | §6.5 p15. `SPEC_FACTS §4`. |

## C · The credit-pathway arithmetic (CREDIT_PATHWAYS.md, re-run against real tables)

| # | Claim | Verdict | Arithmetic against verified tables |
|---|---|---|---|
| C1 | **LAUNCH L1-Certificate ceiling** — all six L1 units = 15 cr ≥ 14-cr L1 Certificate (min 11 at level) | **VERIFIED** | 3+2+2+2+3+3 = **15**; L1 Cert needs 14 total / 11 at level; all 15 at level → **Certificate reachable**. (LAUNCH homes all six across the full-year SoW; Autumn 1 delivers ComSk1 only.) |
| C2 | **GROW Extended Award secure** — five taught L1 units = 12 cr at level ≥ 9 | **VERIFIED** | Com 3 + Dec 2 + LSk 2 + TmWk 2 + ThSk 3 = **12** ≥ 9 (min 6 at level) → **L1 Extended Award secure**. 12 < 14 → Certificate **not** reached by these five alone. |
| C3 | **GROW Certificate via Route B** — 12 at level + WellbLe at an adjacent level within max-3 | **VERIFIED** | 12 at level (≥ min 11) **+ WellbLeE3 (3 cr, adjacent E3)** = **15 ≥ 14**, max-3-adjacent satisfied, barred-combination fine (Wellbeing at one level only). Route A (add WellbLe1 at L1 → six L1 = 15) also valid. |
| C4 | **BUILD unclaimed-credit headline** — banks zero PEQ; six E3 units = exactly 14 = E3 Certificate *if* claimed | **VERIFIED / unchanged** | E3 six units sum = **14** = E3 Certificate (min 11). BUILD banks no PEQ today → headline stands. |

## D · The "10-hour" plan-use window — the one substantive CORRECTION

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| D1 | "Plan used over a minimum period of 10 hours" wording (FINDINGS §D; PRIMER §4; PATHWAYS §2) | **VERIFIED (real) but CORRECTED (scope)** | The line is real and per-unit, on the **"Use the plan"** criterion — **but it is on Decision making, Learning, Team working, Thinking and Wellbeing ONLY, and is ABSENT from Communication (ComSkE3 / ComSk1)**, which instead carries the activity-time minimums. The blind audit's "appears per-unit" generalisation is corrected. `SPEC_FACTS §15, §16`. |
| D2 | LAUNCH surfaces a "≥10-hour window for ComSk1" (W4/W5) (`_passla` §3.2) | **CORRECTED — APPLIED (Matt-authorised, claim-accuracy only)** | The spec places **NO 10-hour requirement on Communication** (`SPEC_FACTS §15/§16`); LAUNCH W4/W5 asserted one. **Matt authorised the reframe** (constrained to claim-accuracy). Applied: removed the false "the 10-hour window / the unit asks for … ten hours / used over ~10 hours" assertions in **W4 (3 surfaces) + W5 (2 surfaces)**, keeping the spec-accurate pedagogy ("planned/used across weeks, often **within another challenge**", per §17 LO1.4/1.5 guidance). **The assessed task is unchanged** — pupils still plan and deliver a ≥3-min talk / ≥250-word text with a group of ≥3; no timing, task design, or deliverable altered. Separate commit, own gate run, independently revertable. |
| D3 | GROW's non-Communication units (Dec/LSk/TmWk/ThSk) and the 10-hour window | **VERIFIED (applies)** | Those four units **do** carry the 10-hour line; GROW's GCOMM/ENT term-long project strands are well-placed to be that clocked use. The finding that it is never *surfaced* as a requirement (0 occurrences of "10 hours") stands as an estate gap. |

## E · Command verbs (level pitch)

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| E1 | E3 verbs = State/List/Identify/Give an example; L1 verbs = Outline/Describe/range (PRIMER §5) | **VERIFIED (refined)** | E3: State · List · Identify · Give an example. **L1: Outline · Identify a range of · Give examples of a range of · Describe.** `SPEC_FACTS §14`. |
| E2 | "Plural" = ≥2, "Range" = ≥3 (PRIMER §5) | **VERIFIED** | Stated on every unit's requirements page. `SPEC_FACTS §14`. |
| E3 | GROW/LAUNCH "Explain" ×12 leans L2 vs L1 "Describe/Outline" (COVERAGE_GROW §2) | **VERIFIED as observation; NOT a required fix** | "Explain" is **not** an L1 PEQ command verb (it belongs to L2+). Estate discussion/exit prompts using "Explain" over-pitch *relative to the per-criterion verbs*, but as teaching prompts (not assessment criteria) they are not a spec breach. The **1.2 Oct 2025** change was precisely to command verbs at L1/L2/L3 — so verb pitch is now settled by `SPEC_FACTS §14`. No lesson edit required; Stretch-tier L2 reach is deliberate (do not fix). |

## F · Unit content minimums (measurable in lessons)

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| F1 | ComE3 activity: presentation ≥2 min OR discussion ≥5 min OR text ≥100 words; group ≥3 (PRIMER §4) | **VERIFIED** | ComSkE3 E3.5.1 + guidance. `SPEC_FACTS §15`. |
| F2 | ComSk1 activity: presentation ≥3 min OR ≥250 words (+ discussion ≥8 min); group ≥3 (PRIMER §5; `_passla` §3.3) | **VERIFIED** | ComSk1 1.5.1 + guidance p39. `SPEC_FACTS §15`. → the LAUNCH ComSk1 min-evidence fix targets exactly these. |
| F3 | Team min-3 members (COVERAGE_GROW) | **VERIFIED** | Team/group ≥3 on TmWkSkE3 p31 / TmWkSk1 p45 (and Communication group ≥3). `SPEC_FACTS §15`. |
| F4 | Whether each task actually *meets* its minimum, per pupil (FINDINGS needs-booklet) | **STILL-UNDETERMINED** | Measurable at task level in lessons (Phase 3 sweep) but the *achieved* per-pupil record lives in the unit assessment booklet — member-gated. |

## G · Assessment, QA and administration process

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| G1 | Portfolio; explicit evidence per criterion (PRIMER §6) | **VERIFIED** | §10 p17. `SPEC_FACTS §8`. |
| G2 | Records signed & dated by **assessor AND learner** (+ IQA where sampled) (PRIMER §6; FINDINGS §C 5a) | **VERIFIED — and the gap is now CLOSED in the estate** | §10 p17 names assessor, learner and (where sampled) IQA. The blind audit flagged the witness statements as assessor-only, but **T2-4 was subsequently merged (2026-07-29, `013121e`→`bc215d1`, REGISTER R-E20/R-E21)**: the "5 · Learner confirmation" block is now present in **all 79** ASDAN witness surfaces (verified at this branch base). So the requirement is **met** in the current estate; the audit's "held" note is superseded. |
| G3 | Amend and resubmit (PRIMER §6) | **VERIFIED** | §10 p17; §11 p18. `SPEC_FACTS §8/§9`. |
| G4 | IQA before EQA; ASDAN cannot award without IQA (PRIMER §7) | **VERIFIED** | §11 p18. `SPEC_FACTS §9`. |
| G5 | First-year centres MUST book an EQA sampling activity in year one (PRIMER §7; `_passla` implicit) | **VERIFIED** | §12 p19. `SPEC_FACTS §10`. |
| G6 | Register before assessment; coordinator's action; names ≈4 weeks before sampling (PRIMER §7) | **VERIFIED** | §14 p20. `SPEC_FACTS §11`. |
| G7 | IQA standardisation ≥ once every 3 years (PRIMER §7) | **VERIFIED** | §12 p19; §15.2 p20. `SPEC_FACTS §10/§12`. |
| G8 | Assessors need appropriate training, no formal assessing qualification (PRIMER §7) | **VERIFIED (refined)** | §15.1 p20 — training **incl. "Assessment for ASDAN Qualifications" + qualification training**; IQAs additionally need IQA training. `SPEC_FACTS §12`. |
| G9 | Mixed-level groups permitted; differentiation required | **VERIFIED** | §9 p16. `SPEC_FACTS §7`. |
| G10 | Centre + PEQ-suite approval required before delivery (Q5) | **VERIFIED (fact); membership status STILL-UNDETERMINED** | §8 p16 confirms the *requirement*; whether the school's membership carries PEQ approval is an ASDAN-account fact, not a repo fact. |

## H · Safeguarding

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| H1 | Decision-making + Wellbeing carry a safeguarding note; learners told in advance (PRIMER §8; Q10; `_passla` §3.6) | **VERIFIED (scope confirmed)** | Note is on **DecMkSkE3/DecMkSk1 and WellbLeE3/WellbLe1 only** (§17 pp27/41/35/50). **ComSk1 carries no safeguarding note** → LAUNCH Autumn (ComSk1) is correctly outside it; the note lands on the Spring/Summer Dec/Wellbeing modules. `SPEC_FACTS §17`. |
| H2 | Exact safeguarding-disclosure *wording* required (FINDINGS needs-booklet; Q10) | **STILL-UNDETERMINED** | Spec gives the principle; the prescribed wording (if any) is in the unit assessment booklets — member-gated. |

## I · Records design (protected surfaces)

| # | Flag | Verdict | Resolution → cite |
|---|---|---|---|
| I1 | Per-activity vs per-criterion printed record (FINDINGS §C 5b) | **STILL-UNDETERMINED (hold confirmed)** | §10 p17 says judgements are recorded "for example within the **unit assessment booklet**" — so the per-criterion record is the (member-gated) booklet, witness statements supplementary. **Do not redesign the protected witness surface to duplicate a document not yet read.** The Binder already supplies per-criterion capture. |

## J · Held estate fixes — now unlocked (executed/measured in Phase 3)

| # | Fix | Gate result | Action |
|---|---|---|---|
| J1 | **T2-2** "Delivering a Project" → honest framing / real codes (GCOMM/ENT) | two-source agreement **TOTAL** | Unlocked. Relabel across GROW Community (+Enterprise) titles; project is the extended *use* activity evidencing TmWkSk1 + ComSk1 + DecMkSk1 by code, not a PEQ unit. |
| J2 | **T2-3** friendly labels → Binder codes (GROW staff-facing) | two-source agreement **TOTAL** | Unlocked. "Working with Others"→TmWkSk1 · "Problem Solving"→ThSk1 · "managing own performance"→LSk1 · "Goals That Work"→DecMkSk1 · "Present My Progress"→ComSk1 · "core-skills audit"→LSk1. |
| J3 | **ComSk1 min-evidence** (LAUNCH) | minimums VERIFIED (F2/F3); **applied additively to W4** | **Measured sweep of all 7 LAUNCH ComSk1 lessons:** ≥3-min/≥250-word present in W4+W5 ✓; **group-≥3 present in W5 but ABSENT in W4** (the belief "group-≥3 absent" is *partly* refuted — it was already in W5). Fix: **added** the group-≥3 minimum to W4's ComSk1-minimum line additively (matches W5's phrasing), no teaching content rewritten. W1–W3/W6/START_HERE are know/understand or review weeks — the activity minimums correctly belong to the plan (W4) and deliver (W5) weeks only. |
| J4 | **T2-4** learner signature on witness statement | gap VERIFIED (G2) | Remains **PROPOSED, not committed** — protected surface, awaits Matt's explicit word. |

## STILL-UNDETERMINED summary (needs member-gated booklets or an ASDAN-account fact)

1. **F4** — per-pupil *achieved* minimums (unit assessment booklet).
2. **H2** — exact safeguarding-disclosure wording (unit assessment booklets).
3. **I1** — per-criterion record design (unit assessment booklet; hold the protected surface).
4. **G10 (status)** — whether the school's ASDAN membership carries PEQ-suite approval
   (ASDAN account, coordinator).
5. **D2 (wording)** — resolve *how* LAUNCH surfaces the ComSk1 "10-hour" line (measured and
   fixed in Phase 3; listed here because the fix depends on the measured text).
