# Pass Q (KO Triage) — TRIAGE LEDGER

**Provisional letter Z, self-renamed to Q per R-H09 (record below). Branch `pass-q-ko-triage`,
cut off `origin/main` at `c034ffd`. Tier-1 artefact: this ledger + `_passq/tools/` check scripts.
Deploy-visible change set on `main`: EMPTY. No KO file was edited by this pass.**

> **Disambiguator (cross-repo, per Matt's disposition):** Pass Q (Lessons, KO triage, `38c8f6b`) is
> distinct from Pass Q (site repo, quality sweep, `6845f44`); letter checks must consult BOTH repos'
> records. The Lessons ledger cannot see site-repo letters — R-H09's blind spot appearing in the
> other direction. Not renamed: commits exist, and a mid-flight rename is worse than a dispositioned
> collision. See §0.

---

## 0 · Letter hygiene (R-H09) — the check, recorded

Provisional designation was **Pass Z (KO Triage)**. R-H09 requires a letter be checked against the
ledger/register **AND** git history before adoption (a measurement-only pass leaves no commits, so
git alone cannot clear a letter).

- **Z — COLLISION.** Git history carries two `Pass Z` commit subjects: *"Pass Z remediation: LI W5
  becomes a budgeting task…"* and *"Pass Z: differentiate Careers W7 from W6"*. Disqualified on git
  history alone.
- **Next-free scan.** Register R-code families exist for A B C D E F G H SB; git subjects + register
  mentions additionally consume J K L LL M N O P Q(site-repo only) R? S T U V W X Y Z, and E/N/U via
  ledger-without-commits. Genuinely free in **this** repo (register + handover + git + worktree, all
  four checked): **I, Q, R**.
  - **I — rejected**: namespace-ambiguous with the active `Pass LL-I` (a whole HANDOVER section).
  - **R — rejected**: visually collides with the `R-xx` register-entry prefix used throughout.
  - **Q — selected**: zero hits in Lessons register/handover/git-history/worktree. A `Pass Q` exists
    in the sibling **site** repo (`mattroper1977.github.io`) — a different programme in a different
    repo, outside R-H09's stated scope (this repo's REGISTER/HANDOVER + git history).
    - **Cross-repo update (Matt's disposition):** the site-repo `Pass Q` is in fact *spent* (quality
      sweep, closed at `6845f44` there) — a genuine collision the Lessons ledger structurally could
      not see, which is R-H09's blind spot in the other direction. **Dispositioned, NOT renamed:**
      commits already exist and a mid-flight rename is worse than a named collision. See the header
      disambiguator; R-H09 gains a cross-repo clause in this pass's REGISTER commit.

**This pass is Pass Q (KO Triage).** Not a STOP point: the collision was resolvable from the record.

---

## 1 · Derived count at HEAD (R-E11 — unit and scope in one string)

Ran the **frozen** `ko_staleness.py` (LL-INST-08; queue-9 R-E07 refinement still OPEN, so this is the
un-patched instrument — R-E09: not modified in the pass that measures it) on the **full clone**
(preflight X2 guard accepted it; a shallow clone would false-zero).

> **114 KO-staleness candidates** in the **161-file KO corpus** (`id="print-ko"`) at HEAD `c034ffd`,
> produced by `ko_staleness.py` on a full clone — assumptions banner: *full clone · 161-file KO corpus
> · network not required · co-modification is a consistency proxy, not consistency*.

Cardinality re-asserted by the instrument: **114 candidates + 3 architecture-only-dropped + 44 clean
= 161 == KO files → True.** The 44 "clean" are the instrument's **blind twin** — UNCHECKED, not
verified (KO + body moved in the same commit, possibly inconsistently); out of this pass's scope,
which triages the 114 flagged candidates only.

**Inherited nothing.** The CARRYFORWARD figure "114" and its "117→109→114" history are not carried
(R-E11); the number above is re-derived at this pass's own HEAD. It coincides with CARRYFORWARD's 114
but was independently measured.

---

## 2 · Grouping — and a documented divergence from CARRYFORWARD's expected shape

CARRYFORWARD_KO anticipated three groups, the first being an **R-E07 Loop-Mark artefact group** (~39)
to "clear first, mostly mechanically." **At this HEAD that pure-artefact group is EMPTY**, and this is
a finding, not an oversight:

- Evidence (`_passq/tools/movers.json`, produced by `triage_movers.py` reusing the frozen instrument's
  own `visible()`/`ko_text()`/`ARCHITECTURE`): every one of the 114 has `ko_same=True` (KO block
  byte-identical since its last change — instrument-consistent) but `excl_same=False` (real visible
  body outside the self-declaring not-KO regions moved). **No candidate is moved *only* by the Loop
  Mark.**
- Why: the Loop-Mark commits (`Pass LL-G sub-pass 1/2/3`, 15+15+14 mover-instances) are merely the
  **most recent** mover of the BUILD files. Those files' KOs last changed at the **Pass G rebuild**
  (`9f657b6`, ASDAN) or the **v4/v5 rebuild** (`d103ec1`, Art/HUM) and have since been moved by whole
  sequences of genuine content passes (Pass W ×48, W2 ×49, F ×34, O ×29, C, D, M, …). The Loop Mark
  sits on top; it does not make them artefacts.

The honest grouping used here (sums to 114):

| group | n | what it is |
|---|---|---|
| **A · Assessed pair** | 2 | `GROW_HUM_W7`, `LAUNCH_HUM_W7`. READ-ONLY, REPORT-ONLY (§2.4 / no-touch). |
| **B · ASDAN, Pass-G-anchored** | 49 | The **R-G05 population** — KO last rebuilt at `9f657b6` "…(49 lessons)". |
| **C · Body-mover (Art / HUM / D&T / Science)** | 63 | KO predates later content/scaffolding passes. |

---

## 3 · Verdicts

**Method.** For every candidate the KO block (`print-ko`) was read against the lesson's We-Do content
(`print-wedo`, and on-screen We-Do-2 where the print mirror was ambiguous). A KO is STALE only if a
fact it asserts is contradicted by the current body. Mover classes were characterised once and applied:
Loop Mark (print feedback), Pass O witness-statement/staff notes, reduced-motion CSS, D&T week-label
print fixes, keydown guards, and rebrand are **not** things a KO summarises; instruction-line and
tier-scaffold passes (W/W2/F) add pupil-facing scaffolding without changing the organised knowledge.

**Result: 0 STALE. 0 KO edits. 0 Tier-2 batches.** Consistent with the estate's standing pattern
(HANDOVER: healthier than its instruments every time; suspect the instrument first).

| verdict | n | note |
|---|---|---|
| **STILL-TRUE** | 110 | KO agrees with its lesson body at HEAD. |
| **NO-ORGANISER** | 4 | `print-ko` slot holds only a Name/Class/Date header (worksheet template), not an organiser — no truth-claim exists to be stale. Tier-3 observation, §5. |
| **STALE** | 0 | — |
| **UNDETERMINED** | 0 | Every candidate was read. |

### 3A · The assessed pair (READ-ONLY findings — no edit, no proposed fix applied)

- `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` ★ — **STILL-TRUE on read.** The standing
  HANDOVER §7 / R-G02 worry was: Pass LL-A2a removed the **Connective Bank** and **Evaluation
  Deployments**; if the KO still named either it would describe support that no longer exists. **It
  names neither.** The KO's "Evaluation clause — deployed provenance honesty" is a *provenance*
  evaluation, a different construct; no "Connective Bank" appears. The §7 concern does **not**
  materialise at HEAD. Nothing edited (no-touch; would need Matt's key + assessed-file diff discipline).
- `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` ★ — **STILL-TRUE on read.** KO names the
  W1–W6 tool ladder (support spectrum, courtroom, NOP, change dials, person+pattern, thesis control),
  all present in the lesson; "assessed independence — arrangements yes, assistance no" is current. No
  reference to removed scaffolding. Nothing edited.

### 3B · R-G05 — the "37 of 49 KOs disagreeing with their own slide" figure — **REFUTED AT HEAD**

R-G05 is a **content-disagreement** claim sourced to Pass G's ASDAN KO rebuild (`9f657b6`), explicitly
NOT `ko_staleness` output, and UNVERIFIED at HEAD. Verified here by a direct read of **all 49** ASDAN
KO blocks against their We-Do-2 slides (`_passq` scratch dumps drove the read; evidence reproducible via
`triage_movers.py` + the extractors).

> **0 of 49 ASDAN KOs disagree with their We-Do-2 slide at HEAD `c034ffd`.** The KO Key-Word
> definitions match the We-Do-2 matching targets; Key Facts are consistent with the taught content.
> Wording variances are cosmetic (e.g. COMM_W1 "keeps working" vs "keeps giving"), never contradictions.

**The 37/49 figure does not reproduce at HEAD.** Scope of this verdict: KO-vs-We-Do-2 content read;
"disagreement" judged as a definitional/factual contradiction. What this does **not** settle: whether
37/49 ever held immediately after the `9f657b6` rebuild (before Pass W/W2/F/O). That is a separate
git-archaeology question (check out `9f657b6` and re-read) — offered as follow-up, out of this
HEAD-scoped pass.

### 3C · Full verdict table

*(generated by `_passq/tools/build_ledger_table.py` from `movers.json` — emit, don't transcribe;
counts §3 are derived from this table, cardinality 114.)*
| # | file | suite | group | verdict | KO unchanged since | fix |
|---|---|---|---|---|---|---|
| 1 | `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 2 | `BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 3 | `BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 4 | `BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 5 | `BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 6 | `BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `df353f6e7a` | n/a |
| 7 | `BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `df353f6e7a` | n/a |
| 8 | `BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 9 | `BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 10 | `BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 11 | `BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 12 | `BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 13 | `BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 14 | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 15 | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 16 | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 17 | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 18 | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 19 | `BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 20 | `BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 21 | `BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 22 | `BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 23 | `BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 24 | `BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 25 | `BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 26 | `BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 27 | `BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 28 | `BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 29 | `BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 30 | `BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 31 | `BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 32 | `GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 33 | `GROW_ASDAN/Community_Project/GCOMM_W2_Choose_The_Need.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 34 | `GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 35 | `GROW_ASDAN/Community_Project/GCOMM_W4_First_Contact.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 36 | `GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 37 | `GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 38 | `GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 39 | `GROW_ASDAN/Enterprise/ENT_W2_Spot_The_Gap.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 40 | `GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 41 | `GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 42 | `GROW_ASDAN/Enterprise/ENT_W5_Brand_And_Pitch.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 43 | `GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 44 | `GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 45 | `GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 46 | `GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 47 | `GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 48 | `GROW_ASDAN/PEQ/PEQ_W5_Solving_Problems.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 49 | `GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html` | ASDAN | B-asdan(R-G05) | STILL-TRUE | `9f657b6773` | n/a |
| 50 | `Art_Teesside/Build/BUILD_ART_A2_W1_Surface_Hunt.html` | Art | C-body-mover | STILL-TRUE | `dae6d20516` | n/a |
| 51 | `Art_Teesside/Build/BUILD_ART_A2_W2_Arts_Inspiration.html` | Art | C-body-mover | STILL-TRUE | `dae6d20516` | n/a |
| 52 | `Art_Teesside/Build/BUILD_ART_A2_W3_Stencil_Lab.html` | Art | C-body-mover | STILL-TRUE | `2106b3fbf3` | n/a |
| 53 | `Art_Teesside/Build/BUILD_ART_A2_W4_Audience_Week.html` | Art | C-body-mover | STILL-TRUE | `2106b3fbf3` | n/a |
| 54 | `Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 55 | `Art_Teesside/Build/BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 56 | `Art_Teesside/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 57 | `Art_Teesside/Build/BUILD_ART_W4_Build_the_Brief.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 58 | `Art_Teesside/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 59 | `Art_Teesside/Build/BUILD_ART_W6_Resolve_the_Artwork.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 60 | `Art_Teesside/Build/BUILD_ART_W7_Curate_the_Showcase.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 61 | `Art_Teesside/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 62 | `Art_Teesside/Grow/GROW_ART_W1_The_Local_Canvas.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 63 | `Art_Teesside/Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 64 | `Art_Teesside/Grow/GROW_ART_W3_Independent_Studio_Challenge.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 65 | `Art_Teesside/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 66 | `Art_Teesside/Grow/GROW_ART_W5_Practitioner_Career_and_Inspiration.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 67 | `Art_Teesside/Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 68 | `Art_Teesside/Grow/GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 69 | `Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 70 | `Art_Teesside/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 71 | `Art_Teesside/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 72 | `Art_Teesside/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 73 | `Art_Teesside/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 74 | `Art_Teesside/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 75 | `Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 76 | `Art_Teesside/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 77 | `Art_Teesside/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html` | Art | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 78 | `Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html` | D&T | C-body-mover | STILL-TRUE | `32d0f238a3` | n/a |
| 79 | `Build/Slideshows/BUILD_DT_W2_Blueprint.html` | D&T | C-body-mover | STILL-TRUE | `55699a312d` | n/a |
| 80 | `Build/Slideshows/BUILD_DT_W3_Core_Cut.html` | D&T | C-body-mover | STILL-TRUE | `1e1ae793ef` | n/a |
| 81 | `Build/Slideshows/BUILD_DT_W4_Assembly.html` | D&T | C-body-mover | STILL-TRUE | `b1f1bf51d4` | n/a |
| 82 | `Build/Slideshows/BUILD_DT_W5_Finish.html` | D&T | C-body-mover | STILL-TRUE | `a7dbbf97e2` | n/a |
| 83 | `Build/Slideshows/BUILD_DT_W6_Handover.html` | D&T | C-body-mover | STILL-TRUE | `069786e772` | n/a |
| 84 | `Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html` | Humanities | C-body-mover | STILL-TRUE | `94d8f4a195` | n/a |
| 85 | `Build/Slideshows/BUILD_HUM_W2_History_Detectives.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 86 | `Build/Slideshows/BUILD_HUM_W3_Why_People_Came.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 87 | `Build/Slideshows/BUILD_HUM_W4_People_Who_Shaped_Britain.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 88 | `Build/Slideshows/BUILD_HUM_W5_Big_Deal.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 89 | `Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 90 | `Build/Slideshows/BUILD_HUM_W7_Tell_The_Story.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 91 | `Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 92 | `Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 93 | `Grow/Slideshows/GROW_HUM_W2_Source_Detectives.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 94 | `Grow/Slideshows/GROW_HUM_W3_Cause_And_Consequence.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 95 | `Grow/Slideshows/GROW_HUM_W4_People_Who_Shaped_Britain.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 96 | `Grow/Slideshows/GROW_HUM_W5_Significance.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 97 | `Grow/Slideshows/GROW_HUM_W6_Plan_The_Account.html` | Humanities | C-body-mover | STILL-TRUE | `ff259c9d14` | n/a |
| 98 | `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` | Humanities | A-assessed | STILL-TRUE | `d103ec1e25` | n/a |
| 99 | `Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 100 | `Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 101 | `Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 102 | `Launch/Slideshows/LAUNCH_HUM_W3_Archive_NOP.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 103 | `Launch/Slideshows/LAUNCH_HUM_W4_Century_Of_Change.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 104 | `Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 105 | `Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 106 | `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html` | Humanities | A-assessed | STILL-TRUE | `d103ec1e25` | n/a |
| 107 | `Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html` | Humanities | C-body-mover | STILL-TRUE | `d103ec1e25` | n/a |
| 108 | `2 Physics 10/Waves/L4a_Wave_Anatomy.html` | Science | C-body-mover | NO-ORGANISER | `df650518cd` | n/a |
| 109 | `biology/L4_Aerobic.html` | Science | C-body-mover | NO-ORGANISER | `390a10e4a9` | n/a |
| 110 | `biology/Lesson_2_Absorption_v4-6.html` | Science | C-body-mover | STILL-TRUE | `874f6cfb30` | n/a |
| 111 | `biology/Structure_of_the_Thorax.html` | Science | C-body-mover | STILL-TRUE | `506d5472f3` | n/a |
| 112 | `chemistry/Lesson3_Ions_Neutralisation_v4.html` | Science | C-body-mover | STILL-TRUE | `7f5b330834` | n/a |
| 113 | `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html` | Science | C-body-mover | NO-ORGANISER | `d1ea59903b` | n/a |
| 114 | `chemistry/Lesson5_Flame_Tests.html` | Science | C-body-mover | NO-ORGANISER | `1cdc96492b` | n/a |

---

## 4 · Findings outside KO scope (Tier-3 — report only, nothing edited)

1. **`BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html` — print We-Do-2 answer-bank mismatch.**
   The **printed** worksheet region (`print-wedo`, a clean 612-char bounded region — no extraction
   bleed) carries CAREERS_W6's answer set — *"Real example · Name · strengths with examples · a job
   area · The Strengths Wall · Your call"* — under W7's **route** questions ("Can you stop learning at
   16?", "Which route pays a wage?", …). The **on-screen** We-Do-2 is correct (route-matched answers:
   "earn while you learn… ready for a workplace", "EHC plan… job coach", …), and the **KO is correct**.
   So this is a print-mirror co-present contradiction on the tangled W6/W7-swap history (R-H09 Careers
   note) — **not a stale KO**. Belongs to a future print/content pass, not this one. A systematic
   on-screen-vs-print We-Do mirror check across the estate is a separate instrument question.

2. **Four `print-ko` slots contain no organiser** (worksheet template — Name/Class/Date header only):
   `2 Physics 10/Waves/L4a_Wave_Anatomy.html`, `biology/L4_Aerobic.html`,
   `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html`, `chemistry/Lesson5_Flame_Tests.html`. These flag as
   candidates because the instrument keys on `id="print-ko"`, but they assert no KO knowledge, so they
   cannot be stale. Whether these science lessons *should* carry an organiser is a content-authoring
   observation for a future pass, not a defect this pass fixes.

3. **Instrument note (R-E09 — a report, not an edit).** `triage_movers.py`'s R-E07 exclusion lens
   (`excl_same`) reproduced the "not-KO region moved" test independently of the frozen instrument. It
   confirms R-E07's mechanism but also shows that at this HEAD the exclusion no longer *drops* any
   candidate (all 114 have real body movement outside the Loop-Mark regions), because later content
   passes now dominate the mover window. When queue-9 (the R-E07 refinement) is eventually applied in
   its own instrument pass, it will **not** shrink this candidate list — a prediction registered here
   for that pass to check against.

---

## 5 · Tier-2 (build-then-hold) — status

**No STALE KO fixes were found, so there are NO held suite batches.** Nothing pupil-facing was built,
staged, or pushed. If Matt's read of §3B/§4 surfaces a fix he wants (e.g. the CAREERS_W7 print
answer-bank, which is *print*, not KO, and outside this pass's tier gating), it is commissioned
separately.

## 6 · Gates

- **Deploy-visible change set on `main`: EMPTY.** This branch adds only `_passq/` (ledger + check
  scripts). No `*.html` lesson file is touched by this pass.
- **Instrument frozen (R-E09):** `ko_staleness.py` and all `LundyLoop/tools/` instruments unmodified;
  `triage_movers.py` *imports* the instrument, never edits it.
- **Assessed pair (R-A / §2.4):** read only; no edit, no proposed fix applied; findings in §3A.
- **Manifest = committed set**, explicit paths, verified at origin by a separate read after push.

## 7 · Close state (for HANDOVER)

- Denominator: **114 candidates / 161-file KO corpus @ `c034ffd`** (re-derived, R-E11-scoped).
- Verdicts: **110 STILL-TRUE · 4 NO-ORGANISER · 0 STALE · 0 UNDETERMINED**; cardinality 114 closed.
- **R-G05 REFUTED at HEAD** (0/49 ASDAN KOs disagree with their slide).
- **§7 / R-G02 assessed worry resolved** (neither assessed KO names the removed Connective Bank /
  Evaluation Deployments).
- Held batches awaiting Matt: **none** (no STALE fixes).
- Follow-ups offered, not done: historical R-G05 check at `9f657b6`; CAREERS_W7 print-mirror fix
  (Tier-3); missing-organiser question on 4 science worksheets (Tier-3).
