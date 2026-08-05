# ACCREDITATION ALIGNMENT MATRIX — Pass 4, 2026-08-05

Sentinel `six-close-2026-08-05`. **Report-first.** Base `bc38dfa` (Lessons main after the
Pass 1 item-17 append). Authority hierarchy applied strictly: (1) official awarding-body
documents — **none reached this session**, so no verdict below rests on one; (2) committed
spec-verified records (`_passpq/SPEC_FACTS.md`, the spec-verified PEQ primer, the Evidence
Binder, SoWs at HEAD); (3) absent authority = **UNDETERMINED**, never inferred.

**No verification was performed against any awarding body's website.** This container has no
usable egress. Every verdict below is derived from committed bytes at the named HEAD.

## What the census looked for

Universe: **548** tracked `*.html` at HEAD. Five claim families were searched, each with its
inclusion rule stated. A census returning a non-zero count classifies **every** hit (R25);
instrument artefacts are named as such rather than quietly dropped.

| # | family | rule | raw hits | genuine |
|--:|---|---|--:|--:|
| 1 | `Delivering a Project` (banned label) | case-insensitive, tracked `*.html` | **0** | 0 |
| 2 | Arts Award hours thresholds | numeric + `hours` near Arts Award / Silver / qualification | 3 | **3** |
| 3 | Gold progression claims | `gold` near arts-award context | 13 | 10 (3 are CSS `--gold` artefacts) |
| 4 | ASDAN unit codes | word-boundary code tokens | 554 | see §4 |
| 5 | 10-hour window on Communication | `10-hour`/`ten hours` near comm/ComSk1 | 1 | **0** |

## §1 · `Delivering a Project` — VALID (clean)

**0 occurrences estate-wide.** The nonexistent unit label remains absent. Open item 2's close
holds at this HEAD.

## §2 · Arts Award hours thresholds — WRONG (claim-accuracy), 3 surfaces

P4.2 is explicit: **never add an hours threshold at any level; TQT is guidance only.** Three
LAUNCH Art surfaces stated ≈95 hours as a completion condition.

| file | line | claim as found | verdict | disposition |
|---|--:|---|---|---|
| `Art_Teesside/Launch/Scheme_of_Work.html` | 94 | "Silver completion **requires** … normally around **95 total qualification hours**" | **WRONG** — guidance framed as a requirement | **FIXED this pass** (staff-facing prose, wording-level, no task design touched) |
| `Art_Teesside/Launch/LAUNCH_ART_W8_…Portfolio_Audit.html` | 415 | Key Facts: "Silver closes: two units, one folder, **≈95 guided hours**" | **WRONG** | **PROPOSAL — held.** Pupil-facing print surface |
| `Art_Teesside/Launch/LAUNCH_ART_W8_…Portfolio_Audit.html` | 346 | recall task: "Roughly how many hours does Silver expect?" → "≈95 guided hours across the award" | **WRONG** | **PROPOSAL — held.** This is a task item with an answer; removing or rewording it changes what a pupil does, so §4.3 stops the fix and makes it a proposal |

**The fix applied**, in full: the words "normally around 95 total qualification hours" were
removed from the completion sentence, and an additive paragraph now states the honest
position — *hours are guidance, not a threshold; completion is decided by tasks evidenced
across both units and the adviser's portfolio audit, never by a total.* Assessed task,
timings and deliverables unchanged. The A2e ladder re-ran **15 / 0 / 15** across the edit —
this is the file carrying the ratified LAUNCH refusal, so that gate is load-bearing here.

**The two held proposals are one decision, not two:** whether the ≈95 figure appears at all
on a pupil-facing surface. Matt's call; both hunks are in the same file and revert together.

## §3 · Gold — VAGUE, flagged, no fix

The adviser is trained at Explore, Bronze and Silver, **not Gold**. The suite carries a
`GOLD reach` tier across all eight LAUNCH Art weeks plus the printable pack, and the SoW says
"Silver's reach is Gold Arts Award".

**Verdict: VAGUE, not WRONG.** These are stretch-tier descriptors, not claims that this
centre can register, assess or certificate at Gold, and no Gold *assessment* is offered
anywhere. But "GOLD reach" on a pupil-facing ladder can read as an available route. **Held as
a Band-2 proposal** — it is pedagogy and tier design, which §4.3 puts outside claim-accuracy.

Three hits were **instrument artefacts**: CSS custom properties `--gold` / `--arena-gold` in
`5 Intervention 10/` and `5_6 Local Choice/`. Named, not counted.

**Correct and left alone (VALID):** "A public showing is a **GOLD** requirement — welcome at
Silver, never required" (Silver has no public-showing requirement — the estate states this
right, repeatedly) · "Artsmark is whole-setting development, not an individual pupil award" ·
Unit 1D's artist **and arts organisation** pairing, with the organisation half explicitly
flagged as the most commonly missing piece — the standing "where is the organisation
evidence?" check is already wired into the surface.

## §4 · ASDAN unit codes — census recorded, scoping question OPEN

Word-boundary counts over tracked `*.html`: `PEQ` **428** · `ComSk1` **86** · `TmWkSk1` **28**
· `ThSk1` **10** · `LSk1` **1** · `DecMkSk1` **1**.

The rule is that **ComSk1 is the only unit code printable on a public surface.** This census
counts *occurrences*, not *public surfaces* — separating pupil-facing/public pages from staff
binders, primers and evidence records was **not completed this pass** and is not claimed.
**UNDETERMINED, and it is the largest open item this audit leaves.** The single `LSk1` and
single `DecMkSk1` sit inside open item 8's STILL-UNDETERMINED descriptive-week mapping and
must not be resolved by inference.

## §5 · The 10-hour window — VALID (and the earlier close is confirmed)

One hit only: `ASDAN/ASDAN PEQs/Evidence_Binder_PEQ_v7.html:1102`, criterion **3.5.1**,
*"Develop a plan to demonstrate own critical thinking skills … Activity planned over min 10
hours."* That is **critical thinking, not Communication** — exactly where the spine puts it.

**Estate-wide residual 10-hour ComSk1 claims: 0.** Open item 9's close holds at this HEAD,
re-derived rather than quoted.

## §6 · Facts carried, not re-derived

Per P4.2 these were treated as settled and were neither re-derived nor contradicted: the
school **is registered** for ASDAN PEQ (never framed as pending); pathway ceilings BUILD =
Award-class short courses + UAS, GROW = Extended Award L1, LAUNCH = L1 Certificate; the
Trinity centre is registered; AQA UAS units are bespoke and Cheryl-submitted, so **every UAS
mapping is a draft to confirm, never spec**; Tees Trekkers = AQA unit 113789; **LAUNCH
science is the GCSE route** and carries no unit codes. This audit **read** the 15 hidden
LAUNCH science witness sheets' status from open item 17 and **touched none of them**.

## §7 · What would change these verdicts

Only an official awarding-body document. Trinity's own Silver specification would settle §2
and §3; the member-gated ASDAN unit assessment booklets would settle §4 and open item 8.
Third-party and AI descriptions of either award are non-authoritative and were not used.
