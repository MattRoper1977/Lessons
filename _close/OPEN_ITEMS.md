# OPEN ITEMS — season close (2026-07-29), at main `8540eee`

Derived **only** from committed records at the landed tip. Nothing invented. Each item cites its source.

| # | open item | status / blocker | recorded in |
|--:|---|---|---|
| 1 | **T2-4 learner-signature** row on ASDAN print packs | **CLOSED (2026-07-29)** — approved by Matt's explicit merge-and-close order (the master-order execution + this approval satisfy the "one-line spec"); additive §5 Learner-confirmation block `013121e` merged no-ff to `main` `bc215d1` (rollback `a4cdd36`), 49 ASDAN witness surfaces | `REGISTER.md` R-E20 (the diff) + R-E21 (the close); supersedes R-RL01's "EXCLUDED" framing |
| 2 | **T2-2 / T2-3 unit codes** ("Delivering a Project" → real GROW GCOMM/ENT unit codes) | **CLOSED (Pass PQ-reconcile)** — spec v1.2 Oct 2025 obtained; two-source agreement (spec + Binder) **total**. "Delivering a Project" removed from GROW (86 occurrences, 10 files) → "cross-unit project work"; CoPE-era friendly labels → codes ('Working with Others'→Team working TmWkSk1, 'Problem Solving'→Thinking ThSk1). All gates green. On branch, held for Matt's merge. Descriptive-phrase weeks (LSk1/DecMkSk1/ComSk1 mapping) left STILL-UNDETERMINED — see new item 8. | `_passpq/RECONCILIATION.md` J1/J2; `REGISTER.md` R-K03 |
| 3 | **Slideshows S/S/S tiering rebuild** (Supported/Standard/Stretch) | deferred to its own lettered pass | `REGISTER.md` R-RL01 ("… Slideshows tiering rebuild") |
| 4 | **BUILD SoW workbook adoption** | vB (FoodWise-only) is the live instrument audited; vA archived/superseded; workbook-side items are Matt's file, outside repo scope, no patches | `_passsb/FINDINGS.md` §R4 "WORKBOOK-SIDE items" and §3. **Note:** the season-close brief's phrase *"workbook vC-PROPOSED"* does **not** appear in any committed record — the records name **vA (archived)** and **vB (live)** only; corrected here per "invent nothing." |
| 5 | **Discover & Explore adviser training** | required before Arts Award **Explore** can run at BUILD; a scheme/booking decision (human lead time), Matt's call, not a defect | `_passsb/FINDINGS.md` (l.228, l.324) |
| 6 | **Assessed residue — `GROW_HUM_W7` `Evaluation clause` KO row** | **AWAITING-WORD** (S4): pupil-rendered `<td>`, so not auto-committable; proposed hunk held verbatim, `GROW_HUM_W7` untouched | `_passe/ASSESSED_RESIDUE_HELD.md` (season-close S4) |
| 7 | **BUILD_DT witness statements lack the §5 learner line** (`Build/Slideshows/BUILD_DT_W1..W6` — 6 DT decks) | **AWAITING-WORD** — the 6 DT decks carry an Assessor Witness Statement but were **out of T2-4 scope** (ASDAN-only) and correctly left untouched; whether DT evidence needs the same additive §5 Learner-confirmation block is Matt's decision; **no fix made** | Pass PQ T2-4 merge finding (this file); `REGISTER.md` R-E21 |

## Newly surfaced by Pass PQ-reconcile (2026-07-30, branch `claude/asdan-pq-spec-reconcile-sj4gqf`)

| # | open item | status / blocker | recorded in |
|--:|---|---|---|
| 8 | **GROW PEQ descriptive-week → formal unit-code mapping** (W1 core-skills audit, W2 planning/reviewing learning, W4 managing own performance, W6 reviewing/presenting progress) | **STILL-UNDETERMINED** — spec + Binder agree the codes exist but neither maps these descriptive labels to a code; the audit's own mapping is internally ambiguous (W2/W4 both lean LSk1, which would double-bank and leave DecMkSk1 unhomed). **Not guessed** (brief: "never pick one"). Needs the member-gated unit assessment booklets + Cheryl's per-pupil registration intent. Only the two literal CoPE-era unit *names* (W3 TmWkSk1, W5 ThSk1) were corrected. | `_passpq/RECONCILIATION.md` E3/J2 |
| 9 | **LAUNCH ComSk1 "~10-hour window" over-claim** (W4/W5) | **CLOSED (Matt-authorised, claim-accuracy)** — the spec places **no** 10-hour requirement on Communication (`SPEC_FACTS §15/§16`). Reframed 5 surfaces (W4 ×3, W5 ×2): removed the false "10-hour window / unit asks for ten hours / used over ~10 hours" claims; kept the "planned/used across weeks, within another challenge" pedagogy. **Assessed task, timings and deliverable unchanged.** Separate commit, own gate run, independently revertable. Estate-wide residual 10-hour ComSk1 claims: **0**. | `_passpq/RECONCILIATION.md` D2; `REGISTER.md` R-K04 |
| 10 | **Member-gated booklets** (unit assessment booklets, delivery guide, IQA guidance, tracker, challenge bank) | **STILL-UNDETERMINED** — the per-criterion record design, exact safeguarding-disclosure wording, and per-pupil achieved-minimum confirmation all wait on these. ASDAN member login required. | `_passpq/inputs/README.md`; `RECONCILIATION.md` STILL-UNDETERMINED 1–3 |
| 11 | **Off-repo compliance actions** (centre/PEQ-suite approval, registration, assessor + IQA training, IQA sample, **mandatory first-year EQA booking**, names ≈4 wks pre-sampling, records retention) | **CENTRE-ACTION** — no repo change can close these; nothing certificates without them | `_passpq/COMPLIANCE_CHECKLIST.md` |

## Surviving remote branches with ZERO unique commits vs `main` — safe for Matt's UI deletion
Enumerated by `git rev-list --count origin/main..origin/<branch>` at `8540eee` (0 = fully merged / no unique work):

- `art-remediation`
- `claude/grow-sow-audit-phase-3-8tb3oz`
- `pass-e-ko-triage`  *(Pass E held snapshot; its content landed via `pass-e-land`; API delete returned 403)*
- `pass-pq-peq-audit`
- `pass-q-careers-w7-print-fix`
- `pass-q-ko-triage`
- `pass-sb-sow-build`
- `pass-sg-sow-grow`
- `pass-x-instruments`
- `pass-y-assumptions`
- `pilot/launch-hum-w1-illuminator`

## Remote branches WITH unique commits — do NOT delete (real unmerged work)
- `pass-sl-sow-launch` — **12** unique commits
- `pass-sbx-art-a2` — **5** unique commits *(the SBX C1 Bronze→Explore work — NOT-LANDED, see S2)*
- `pass-art-a2b` — **2** unique commits
- `pass-u-audit` — **1** unique commit

## Added by Pass SEMH-1 (2026-08-04), at main `73d6330` → `8040e6e`

Each with owner and trigger, per Matt's close ruling §3.5.

| # | open item | owner | trigger / status |
|--:|---|---|---|
| 12 | **CAREERS / v5 timing-spine census.** Derive the timing spine for **every v5 suite estate-wide, per deck**, against the 40-minute period, identifying drop-first / "if time" slides. The CAREERS donor chassis sums to **53 whole-deck / 52 spine** on a 40-minute period; the Art decks were reconciled to 41/40 under ruling 2, but no other suite was measured. **Whether an over-planned spine is a defect or a design is Matt's call when he sees the table.** | any session | **REPORT-ONLY, no edits.** Any session may run it. |
| 13 | **`chemistry/Lesson2_pH_Scale_v4.html` throws at load.** `TypeError: Cannot read properties of undefined (reading 'trim')` under jsdom on boot. **Pre-existing — verified identical at `6aaffb7`, so it predates the pH correction merged at `8040e6e`.** Unscoped. Also a **clip-verification target file**. | developer | small fix pass |
| 14 | **`BUILD_DT_W1` "spot" vs "match" divergence.** `.sc-v4` carries *"I can **spot** HT pallet wood…"* while `.lc-summary` carries *"I can **match** HT pallet wood…"*. Ruling 4 fixed the wording form; align `.sc-v4` to the ruled wording, **"match"**. One word. | D&T lead | **rides the next D&T-touching pass, not its own** |
| 15 | **3 LAUNCH_ASDAN PEQ decks — SI-04/05 outcome-ownership findings.** `PEQ_W1_Intro_and_Choosing_My_Level`, `PEQ_W2_What_Makes_Communication_Effective`, `PEQ_W3_Active_Listening_and_Giving_Feedback`: midpoint and/or completion surfaces quote criteria the deck does not own. Found by `semantic_integrity_check.py` (LL-INST-14). | ASDAN lead | small pass |
| 16 | **10 files in `6 Art/` — SI-07 timer-contract (high).** A different chassis from Art Teesside. **PARKED with the rest of the unruled legacy `6 Art/` material; NOT queued for action.** | — | parked, no trigger |
| 17 | **SEMH-2 (Matt's commission, separate brief).** (a) Hide the TBC unit code across the **25** Science Teesside witness sheets using the reversible mechanism specified in the SEMH-1 brief — sheet content untouched, returns the moment Cheryl confirms; (b) constructed-source label wording for the Humanities decks delivered **as PROPOSED DIFFS for Matt's read**. **Pupil-facing authoring stays Matt's.** | Matt commissions | awaiting the SEMH-2 brief |


## Added by Pass TK-1 close (2026-08-04), at main `82c40ba`

| # | open item | owner | trigger / status |
|--:|---|---|---|
| 18 | **D&T dust/HT proposed diffs** (`Build/Slideshows/BUILD_DT_W1–W6`: window/mask dust lines, HT-as-the-wood-decision framing). Wording ready in `quality/toolkits/SAFETY_CONTENT_GATE.md` §"Where a P0 string sits inside a protected file". | D&T lead + H&S | **HELD — chained to PR #34's resolution.** Apply only after #34 merges or closes; never touching printPack id lists or the Lundy print-page text (R-A07 BOUNDARY / OPEN_ITEMS #7). |
| 19 | **`Printable_LAUNCH_Evidence_and_Lundy_Pack.html` large-print option** — the 8th pack; the other seven gained it on `tk1-access`. | developer | **chained to PR #41** — built as `tk1-access-2` under the close order's §5 once the print-check trigger lands. |
| 20 | **Primary lesson + Tutor_Time Google-Fonts debt.** ~40 primary lesson/unit-index files + 2 Tutor_Time decks import Google Fonts; templates locked (TK-1 §3). Hub fixed on #41. | developer | **REPORT-ONLY** until the primary template unlocks. |
| 21 | **Humanities pack print units.** The 3 `Humanities_Teesside` `WEEKS[]` packs express sizes in non-`pt` units — a separate measurement model; unmeasured by TK-1's print census. | developer | next accessibility pass |
| 22 | **Metadata-strip rollout beyond the ≤10-page pilot** (`quality/toolkits/METADATA_SCHEMA.md`). A strip's `reviewed` date means a person read the file — never stamped in bulk. | Matt commissions | its own pass |
| 23 | **Progress staff-pack zips are stale after the TK-1 merges** (safety wording, JCQ wording, hub text all moved). **Hard precondition of the next full rebuild: the `MARK_SVG`/`gen_entry` aria-less "M"-mark reconciliation** (12 entry docs; R-J01/R-K01/R-K02, detail in HANDOVER's PACK-LA/PACK-LN ledgers). | Matt commissions | before the next pack rebuild |
