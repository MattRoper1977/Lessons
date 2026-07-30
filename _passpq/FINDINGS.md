# FINDINGS.md — Pass PQ · PEQ audit of BUILD & GROW ASDAN

> **⟲ RECONCILED (spec v1.2 Oct 2025 now in hand).** Every `UNVERIFIED-AGAINST-SPEC` flag
> below is resolved in **`RECONCILIATION.md`** (VERIFIED 24 · CORRECTED 3 · STILL-UNDETERMINED
> 5). Spec facts: **`SPEC_FACTS.md`**; dates: **`DATES_2026-27.md`**. Two-source agreement
> (spec + Evidence Binder) is **total**, so T2-2/T2-3 unit-code fixes are unlocked. The one
> substantive correction: the **"10-hour" plan-use window is NOT on Communication** (it is on
> the other five skills). This original text is retained as the audit record.

**Letter PQ.** No prior `_passpq/` or "Pass PQ" ledger entry existed → no self-rename.
**Base SHA** `32ca685e1df619b333f3ee4385aed227aa675cdf` (origin/main), branch
`pass-pq-peq-audit`. **Nothing merged — Matt merges.** The audit was measure-and-report
first; after Matt's close-out ruling, **one authorised estate fix (T2-1, doubled label)
was applied** at `0a392a7`. No other estate file changed. Register entry R-D05 appended.

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

## §C · Assessment-record deltas (protected surfaces) — split per close-out ruling item 5

1. **(5a) No learner signature/declaration** on the Assessor Witness Statement (assessor
   sign-off only; §2 requires assessor **AND** learner; 0 occurrences of "learner sign").
   → **T2-4: minimal additive diff proposed above, NOT committed — waits for Matt's word.**
2. **(5b) Per-activity, not per-criterion** printed record. **HELD as
   UNDETERMINED-needs-booklet**, deliberately: the member-gated **unit assessment booklets**
   are likely the per-criterion record, with witness statements *supplementary*. **Do not
   redesign a protected surface to duplicate a document we have not read.** The Evidence
   Binder already supplies per-criterion capture (confirm Binder-first workflow, QUESTIONS §Q8).

## §D · The "10-hour" question — PROVISIONALLY-RESOLVED (close-out ruling item 1; spec-gate open)

**Not a conflict.** The spec's line is *"the plan must be used over a minimum period of 10
hours"* — a **cumulative cross-week window on plan use**, appearing per-unit in the
Additional assessment requirements. The Binder's activity-minimums (minutes/words/group
size) govern **individual assessed activities** — a different instrument. **Both bind;
neither replaces the other.** The finding survives the resolution: **the provision surfaces
neither** — 0 occurrences of "10 hours" anywhere, and no check that any pupil's cumulative
plan use reaches the window. **Re-verify the 10-hour wording against the committed spec.**

---

## Tiered response

### Tier 1 (mechanical, auto-commit) — **NONE**
The only mechanical self-inconsistency found was T2-1, which sits in sentinel-45 + witness
surfaces, so per brief §6 it was **Tier-2, not a Tier-1 auto-commit**. **No Tier-1 commits.**

### Tier 2 (build-then-ask)

**T2-1 · Doubled "ASDAN Studio · ASDAN Studio" label — APPLIED (authorised, close-out item 3).**
- **Applied at** commit `0a392a78ee62aa3bcd3c05160f639951388d9a8f` · **rollback** `ab9c290`
  (`git revert 0a392a7` or `git checkout ab9c290 -- BUILD_ASDAN GROW_ASDAN`).
- **Where:** KO print header + witness/print header of **all 49 ASDAN lessons** (BUILD 31 +
  GROW 18). **Pre 98 doubled occurrences (exactly 2/file, middot variant, 0 entity, 0
  triples) → post 0.** 49 files, 98 insertions / 98 deletions.
- **Gates (stated before edit, asserted after):** sentinel loop-mark set **45 → 45**;
  `<script>` blocks + reduced-motion blocks **byte-identical** pre/post; tag counts
  unchanged; **147 script blocks `node --check` clean**; screen canonical form intact
  (print/screen parity restored, not broken); GROW ASDAN packs remain 14 sections (header
  text only, no section change).

**T2-2 · "Delivering a Project" → real unit codes** (GROW GCOMM/ENT). NONEXISTENT PEQ unit
label. **AUTHORISED CONDITIONALLY (close-out item 4): execute only after the committed spec
AND the Evidence Binder agree on every target code (two-source agreement).** The spec is not
yet committed → **NOT EXECUTED.** When it lands: relabel to the units the project evidences
(candidate: TmWkSk1 + ComSk1 + DecMkSk1), by code; any code where spec and Binder disagree
converts to a **tabled finding**, not a fix. Same gates as T2-1; diffs recorded here.

**T2-3 · Friendly unit labels → Binder codes** (GROW staff-facing `Banks:` strings + witness
headers): "Working with Others" → TmWkSk1, "Problem Solving" → ThSk1, "managing own
performance" → LSk1, etc. **Same conditional authorisation as T2-2** — two-source agreement
required, **NOT EXECUTED** (no committed spec). Awaits Matt.

**T2-4 · Learner signature on the witness statement — PROPOSED, NOT COMMITTED (close-out item
5a).** §2 requires records signed by assessor **AND** learner; the witness statement has
assessor sign-off only. Minimal **additive** diff (does not alter the protected assessor
block), to insert after the assessor declaration table in all 49 lessons:
```html
<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">5 &#183; Learner confirmation</p>
<p style="margin:0 0 8px;font-size:.88rem">I confirm this is my own work.</p>
<table style="width:100%;border-collapse:collapse;font-size:.9rem">
<tr><td style="padding:10px 8px;border:1px solid #999;width:50%">Learner name (print)<br><br></td><td style="padding:10px 8px;border:1px solid #999">Signature<br><br></td></tr>
<tr><td style="padding:10px 8px;border:1px solid #999">Date<br><br></td><td style="padding:10px 8px;border:1px solid #999">&nbsp;</td></tr></table>
```
**Witness surfaces are protected design — this diff waits for Matt's explicit word.** Same
gates as T2-1 when authorised (sentinel-45, script/RM byte-identity, tag balance, 14
sections).

### Tier 3 (report-only — curriculum/registration for Matt & Cheryl)
- BUILD: decide short-courses-vs-PEQ-E3 (QUESTIONS §Q1); bank E3 units if PEQ chosen.
- GROW: teach/bank **Wellbeing** (§Q9); confirm cross-strand use/review banking.
- Add learner signature to records (§Q8); confirm safeguarding disclosure notice (§Q10).
- All centre-process items: registration, first-year EQA booking, IQA, membership approval,
  member-gated documents (QUESTIONS Q2–Q10).

---

## UNDETERMINED register — split three ways (per close-out ruling)

### needs-spec (unlocks when the PEQ spec PDF lands in `inputs/`)
| item |
|---|
| Confirm the "10-hour cumulative plan-use window" wording (§D — now PROVISIONALLY-RESOLVED, spec-gate open) |
| Exact per-criterion LO command verbs (L1 verb-pitch scoring; "Explain" ×12 vs L1 "Describe/Outline") |
| Two-source agreement for T2-2 / T2-3 unit-code corrections (spec **and** Binder must match) |
| Spec version delta (expect v1.2 Oct 2025); verify title page / version / page count on download |
| CREDIT_PATHWAYS Route B thresholds ("max 3 adjacent", "min 11 at level") |

### needs-booklet (unlocks with the member-gated unit assessment booklets)
| item |
|---|
| Per-activity vs per-criterion record design (§C 5b — held; do not redesign the protected surface first) |
| Safeguarding disclosure wording on DecMkSk / WellbLe (§Q10) |
| Team min-3 / presentation-minutes actually met per task (booklet + task-level read) |

### needs-decision (Matt / Cheryl — report-only)
| item |
|---|
| BUILD: short-courses-vs-PEQ-E3, and banking the unclaimed E3 evidence (§Q1) |
| Which units/sizes to register; L2 registration; first-year EQA booking (§Q2, Q3, Q6) |
| Wellbeing: teach at L1 (Route A) or bank at E3 adjacent (Route B) or omit (§Q9) |
| Whether the school's ASDAN membership carries PEQ approval (§Q5) |
| Learner-signature diff T2-4 — apply or not (Matt's explicit word) |

**T-audit reconciliation** is **not** in this register: resolved — source is
EXTERNAL-TRANSCRIPT, reconciled against REGISTER R-A02 @`7226b08`, **no delta** (CLAIMS §0).

---

## Verification sweep (at tip — each result stated)

Estate fix T2-1 (49 lessons) verified at tip:
- **Doubled label:** 98 → **0** occurrences estate-wide. ✓
- **Files changed:** 49 (BUILD 31 + GROW 18); 98 insertions / 98 deletions. ✓
- **Sentinel loop-mark set:** 45 → **45** (unchanged). ✓
- **`node --check`:** **147/147** touched script blocks parse; **0 failures**. ✓
- **Tag balance:** **0** anomalies across div/p/table/tr/td/strong/script in all 49. ✓
- **Script + reduced-motion blocks:** byte-identical pre/post (asserted in the apply
  script; RM byte-preservation honoured). ✓
- **Print/screen parity:** screen canonical form (`… Pathway · ASDAN Studio · [Module]`)
  intact and now matched by the print headers. ✓
- **Print-section counts:** header text only — **GROW ASDAN packs remain 14 sections**. ✓
- **REGISTER.md:** R-D05 appended (site-repo default, 5th instance); header stamp untouched.
- The eight `_passpq/*` deliverables are Markdown (no code to check).

## Lineage

Pass PQ (PEQ audit) is the accreditation-verification pass over the **SoW passes SL / SB /
SG** (the BUILD/GROW ASDAN scheme-of-work builds). Population reconciled against Pass SB's
route — **REGISTER R-A02 @`7226b08`** — no delta. It shares the estate with the live Lundy
Loop programme (LL-*) and Pass V/S; it read `REGISTER.md` + `HANDOVER.md` and honours their
conventions (sentinel-45, R-A02 deliberate absences, R-F07 `_ccQuestions`/`_taBriefs`
scoping, protected witness statements, deliberate-wrong-answer match pills e.g. PEQ_W5
"Ignore it and hope"). **Coexistence:** fetch-before-push observed; STOP if new commits
touch `_passpq/` paths. **Matt merges.**
