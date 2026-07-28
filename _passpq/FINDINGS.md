# FINDINGS.md — Pass PQ · PEQ audit of BUILD & GROW ASDAN

**Letter PQ.** No prior `_passpq/` or "Pass PQ" ledger entry existed → no self-rename.
**Base SHA** `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main), branch
`pass-pq-peq-audit`. **Nothing merged. Nothing modified — measure-and-report only.**

**Repo gate (brief ground rule 1):** the session opened in the **site repo**
(`mattroper1977.github.io`) — the same default that trapped three prior sessions. Caught
before any audit ran; the Lessons repo was attached and cloned, and all work is here.

**Authority & caveat:** Phase 0 is **blocked** — `asdan.org.uk` is refused by network
policy, so the official spec is not in `inputs/`. The audit ran on the brief's **§2
baseline (PROVISIONAL)** + the Evidence Binder's Ofqual-URN-bearing unit table (strong
internal corroborator). **Every spec-dependent claim below is `UNVERIFIED-AGAINST-SPEC`**
and reconciles the moment the three PDFs land (see `inputs/README.md`).

---

## Headline (what Matt needs before training)

1. **BUILD does not deliver PEQ.** All 31 BUILD lessons bank **ASDAN short courses**
   (FoodWise, Living Independently) and **AQA Unit Award Scheme** — **zero** occurrences of
   "PEQ", "Entry 3", "Personal Effectiveness", or any PEQ unit code. The E3-level skill
   teaching is present and correctly pitched, but **entirely unbanked as PEQ.**
2. **GROW does deliver real PEQ L1** — correct product, level, Stretch-to-L2 design, backed
   by a correct Evidence Binder. Its gaps are precise: a **missing Wellbeing unit**, a
   **NONEXISTENT "Delivering a Project" unit label**, and **friendly unit names** where
   formal codes belong.
3. **The Evidence Binder is your correct PEQ backbone** (real units/criteria/credits with
   live Ofqual URNs). The lessons drift from it; it is the reconciliation target.
4. **Two assessment-record deltas vs §2** on the (protected) printed witness statements:
   **no learner signature**, and **per-activity not per-criterion**.

---

## §A · Census classification counts (unit-labelled)

Population: **64 files** (BUILD_ASDAN 39 · GROW_ASDAN 23 · Evidence Binder 1 · launcher 1),
**49 lessons**. Full detail in `CLAIMS.md`. Counts are **distinct claim-string types**:

| class | count | headline |
|---|---|---|
| VALID | GROW product/level framing (~6) + entire Binder unit set | GROW is genuinely PEQ; Binder is spec-shaped |
| VAGUE | ~8 | BUILD "ASDAN/UAS community evidence"; GROW friendly unit labels |
| WRONG-PRODUCT | ~12 | all BUILD short-course + AQA-UAS banks (not PEQ) |
| NONEXISTENT | 1 (×7 phase variants) | GROW `PEQ L1 'Delivering a Project'` — no such PEQ unit |
| WRONG-LEVEL | 0 | L2 appears only as declared *Stretch* design, never as a banked level |
| PLACEHOLDER | whole provision | PEQ unit codes deliberately absent from all 49 lessons |

## §B · Coverage summary

- **BUILD vs E3** (`COVERAGE_BUILD.md`): every E3 unit **UNCLAIMED** — the vocational
  contexts generate all six E3 skills' evidence but bank none as PEQ. plan→use→review arc
  explicit in **1 of 5 modules** (Community Project). Pitch is correctly E3. → registration/
  architecture decision, **Tier 3**.
- **GROW vs L1** (`COVERAGE_GROW.md`): five of six L1 units taught (LSk1 best-served);
  **WellbLe1 = GAP** (0 "wellbeing" in the strand). Each unit's use/review LOs depend on
  the GCOMM/ENT project strands → mostly **PARTIAL** until cross-strand banking is confirmed.
  Command verbs: L1 verbs absent, "Explain" ×12 leans L2 → verify.
- **Credit pathways** (`CREDIT_PATHWAYS.md`): GROW as built → **L1 Extended Award (9 cr)**;
  **L1 Certificate (14 cr) needs Wellbeing added** (→15). BUILD *if* claimed → E3 Certificate.
  Barred-combination trap flagged for cross-tier pupils.

## §C · Assessment-record deltas (protected surfaces — reported, not edited)

1. **No learner signature/declaration** on the Assessor Witness Statement (assessor
   sign-off only). §2 requires assessor **AND** learner. 0 occurrences of "learner sign".
2. **Per-activity, not per-criterion** printed record; §2 requires explicit evidence per
   criterion. The **Evidence Binder** supplies per-criterion capture — confirm Binder-first
   workflow (QUESTIONS §Q8). → **Tier 2/3, awaits Matt + Cheryl.**

## §D · §2-vs-internal discrepancy to resolve at training

§2 says each unit's "use" LO runs **over a minimum period of 10 hours**; the Binder's "use"
criterion shows **activity minimums** (minutes/words/group size), not hours. **0
occurrences of "10 hours" anywhere in the provision.** Which governs changes how many
lessons a unit needs. **UNDETERMINED — needs spec / unit booklets.**

---

## Tiered response

### Tier 1 (mechanical, auto-commit) — **NONE**
The only mechanical self-inconsistency found (§Tier-2 below) sits in sentinel-45 + witness
surfaces, so per brief §6 it is **Tier-2 minimum**. **No Tier-1 commits were made; nothing
was modified.** (No rollback SHAs because nothing landed.)

### Tier 2 (build-then-ask — exact diffs, await Matt) — **PROPOSED, NOT APPLIED**

**T2-1 · Doubled "ASDAN Studio · ASDAN Studio" label.**
- **Where:** KO print header + witness/print header of **all 49 ASDAN lessons** (BUILD 31 +
  GROW 18); **98 string occurrences** (2/file).
- **Diff:** `ASDAN Studio · ASDAN Studio` → `ASDAN Studio` (and the `&#183;` entity variant).
- **Evidence it is a defect, not design:** the single canonical form exists on the screen
  tag line (`BUILD Pathway · ASDAN Studio · [Module]`); the doubling is a template
  concatenation artifact. Truth settled in-file.
- **Guards required before applying:** sentinel-45 gate (all 31 BUILD are sentinel);
  witness-statement protection; **print/screen parity** (count occurrences per surface
  before edit); GROW ASDAN packs stay **14 sections**. **Awaits Matt's key.**

**T2-2 · "Delivering a Project" → real unit codes** (GROW GCOMM/ENT). NONEXISTENT PEQ unit
label → relabel to the units the project actually evidences (e.g. TmWkSk1 + ComSk1 +
DecMkSk1), by code, per the Binder and the estate "reference by code" rule (§5). **Diff
deferred until the spec confirms the exact unit set the project banks — awaits Matt +
spec.**

**T2-3 · Friendly unit labels → Binder codes** on staff-facing `Banks:` strings and witness
headers (GROW). Reconcile "Working with Others" → TmWkSk1, "Problem Solving" → ThSk1, etc.
**Diff deferred pending spec verification of unit titles — awaits Matt.**

### Tier 3 (report-only — curriculum/registration for Matt & Cheryl)
- BUILD: decide short-courses-vs-PEQ-E3 (QUESTIONS §Q1); bank E3 units if PEQ chosen.
- GROW: teach/bank **Wellbeing** (§Q9); confirm cross-strand use/review banking.
- Add learner signature to records (§Q8); confirm safeguarding disclosure notice (§Q10).
- All centre-process items: registration, first-year EQA booking, IQA, membership approval,
  member-gated documents (QUESTIONS Q2–Q10).

---

## UNDETERMINED register (names the document that unlocks each)

| item | unlocks with |
|---|---|
| Which of "10 hours" vs activity-minimums governs the "use" LO (§D) | **PEQ spec / unit assessment booklets** |
| Exact per-criterion LO command verbs (L1 verb-pitch scoring) | **PEQ spec + unit booklets** |
| Safeguarding disclosure wording on DecMk / WellbLe (§Q10) | **unit booklets (DecMkSk, WellbLe)** |
| Team min-3 / presentation-minutes met per task | **unit booklets** + task-level read |
| T-audit 159-lesson pathway reconciliation | **the T-audit 159 table** (not in this repo) |
| Whether school's membership carries PEQ approval (§Q5) | **ASDAN centre account** (Cheryl) |
| Which units/sizes to register; L2 registration; EQA booking | **Cheryl** (QUESTIONS Q2, Q3, Q6) |
| Spec version delta (expect v1.2 Oct 2025) | **the downloaded PEQ spec PDF** |

---

## Verification sweep (on work touched)

**No lesson/estate file was modified** — nothing to node-check, boot in jsdom, or
tag-balance beyond the untouched originals. The eight `_passpq/*` deliverables are Markdown.
Print-section counts unchanged (no edits); GROW ASDAN packs remain 14 sections by design.

## Lineage

Pass PQ (PEQ audit) is the accreditation-verification pass over the **SoW passes SL / SB /
SG** (the BUILD/GROW ASDAN scheme-of-work builds). It shares the estate with the live
Lundy Loop programme (LL-*) and Pass V/S; it read `REGISTER.md` + `HANDOVER.md` and honours
their conventions (sentinel-45, R-A02 deliberate absences, R-F07 `_ccQuestions`/`_taBriefs`
scoping, protected witness statements, deliberate-wrong-answer match pills e.g. PEQ_W5
"Ignore it and hope"). **Coexistence:** fetch-before-push observed; STOP if new commits
touch `_passpq/` paths. Matt merges.
