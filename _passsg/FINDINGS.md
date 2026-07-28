# Pass SG — GROW SoW 2026-27 Alignment Audit · FINDINGS

**Letter:** SG (free — no `_passsg/` or "Pass SG" ledger existed on main at base; no self-rename needed).
**Branch:** `pass-sg-sow-grow` (off `origin/main`).
**Base SHA (pinned, fetch-and-pin first act):** `32ca685e1df619b333f3ee4385aed227aa675cdf`.
**Instrument:** `_passsg/inputs/GROW SOW 2026-27.xlsx` (md5 `befdd3f1687b4c66e5960aec7cb7d579`), committed to the branch for reproducibility.
**Posture:** Measure-first complete. **Nothing merged. No lesson file modified.** Only `_passsg/` artefacts committed.

Units used throughout: **lesson** (a taught slide-deck `.html`), **file** (any `.html`), **suite** (a folder of weekly lessons), **strand** (a SoW row). Counts state unit + scope in-sentence.

---

## 0 · Lineage block (siblings + provenance)

- **Base measured at:** `32ca685e` (origin/main @ 2026-07-28).
- **Branch tip:** see close-out (§9) — derived post-commit, never hand-typed.
- **Sibling passes (verified on origin):**
  - **Pass SL (LAUNCH SoW):** `origin/pass-sl-sow-launch` @ `40a0637`.
  - **Pass U (T-audit / instruments):** `origin/pass-u-audit` @ `7c4b2b4` (ledger `_passu/FINDINGS.md`).
  - **Pass X (instruments):** `origin/pass-x-instruments` @ `98a8dbd`.
- **Brief-vs-repo mismatch (rule 3):** the brief names **Pass SB (BUILD)** as a live sibling. **No `pass-sb*` branch exists on origin.** Pass SB is either unmerged/local elsewhere or not yet created. Recorded, not blocking.

---

## 1 · Brief-verification: claims that did NOT hold against the repo (rule 3 — repo wins)

| # | Brief claim | Repo reality | Disposition |
|---|---|---|---|
| BV-1 | "T-audit's **159-lesson** verdict table (@7889055a) … its **GROW count was 34 files**." | No string `159` exists in any tracked `.md` on any branch (main, pass-u-audit, pass-x-instruments, pass-sl-sow-launch, art-remediation). `7889055` is a real commit ("W6 D&T: include Lundy loop in printed pack") but carries no 159-row verdict table. Pathway counts DO exist in `HANDOVER.md` (GROW_ASDAN 18, GROW_HUM 7+W7) and corroborate parts of "34". | **34 unverifiable as a single table.** Population derived mechanically instead (see §2). "34" is *consistent with* ASDAN 18 + HUM 8 + one art suite 8, but the specific art suite is not fixed by any recoverable T-audit record. |
| BV-2 | "GROW ASDAN 18 … GROW Humanities ×8 … Art Teesside GROW route ×8" (= 34 GROW lessons). | Mechanically there are **42** GROW `type:lesson` entries: ASDAN 18 + GROW_HUM 8 + **Grow/Slideshows GROW_ART 8** + Art_Teesside/Grow 8. The brief's 34 **omits the `Grow/Slideshows` "GROW · Art & Arts Award" suite (8 lessons)**. | **Delta tabled (§2). +8 lessons.** Do not force the number. |
| BV-3 | "Sentinel-45 … derive the sentinel set and assert it still returns exactly **45**." | Raw `ll-g` substring appears in **50** `.html` files at base. **None are in the GROW population** (they are `BUILD_ASDAN`, `Art_Teesside/Build`, `Build/Slideshows`, chemistry, Intervention, Games). | Either "45" is stale or "the sentinel set" is a narrower derivation than a raw substring. **Moot for Pass SG:** no scoped GROW lesson carries `ll-g`, and no commit here touches an `ll-g` file, so the gate never engages. Recorded. |
| BV-4 | Middle SC tier named **"Standard"**. | Confirmed — `#arrival-standard`/`#exit-standard`, `switchLevel(...,'standard')`, "🖨 Standard pack", buttons "🤝 With support / 👤 On your own / 🚀 Take it further". | Brief correct. Tier vocabulary is **Supported · Standard · Stretch** across ASDAN + HUM + Art_Teesside. |
| BV-5 | GROW Humanities chassis is **v4** (`.task-box`/`.li-box`/`.answer`/`.lundy-box`, no `.v5-step`). | Confirmed for `Grow/Slideshows/GROW_HUM_*`. **Note:** `Grow/Slideshows/GROW_ART_*` is a THIRD chassis (`.tag`/`.lo-item`/`.sc-box`/`.aspire-box`), older than both v4 and ASDAN v5. | Brief correct on HUM. Art-slideshows chassis flagged (§6). |

---

## 2 · Population — mechanically derived, reconciled

**Derivation method:** `resources.json` (384 entries) filtered to `type=="lesson"` AND (`family` startswith `GROW` OR (`family=="Art Teesside"` AND path contains `/Grow/`)), cross-checked against folder/filename patterns. No list adopted from the brief.

**Result: 42 GROW lessons** (unit: lesson). Non-lesson GROW files (5 `teacher` hubs/SoW + 2 `support`) excluded.

| Suite | Path | Lessons | resources.json family | Chassis |
|---|---|---|---|---|
| GROW ASDAN · PEQ | `GROW_ASDAN/PEQ/PEQ_W1–W6` | 6 | GROW ASDAN · Personal Effectiveness | v5 studio |
| GROW ASDAN · Community Project | `GROW_ASDAN/Community_Project/GCOMM_W1–W6` | 6 | GROW ASDAN · Community Project | v5 studio |
| GROW ASDAN · Enterprise | `GROW_ASDAN/Enterprise/ENT_W1–W6` | 6 | GROW ASDAN · Enterprise | v5 studio |
| GROW Humanities | `Grow/Slideshows/GROW_HUM_W1–W8` | 8 | GROW · Humanities Aut 1 | **v4** |
| GROW Art (Arts Award) | `Grow/Slideshows/GROW_ART_W1–W8` | 8 | GROW · Art & Arts Award Aut 1 | older (.tag/.lo-item) |
| Art Teesside · GROW route | `Art_Teesside/Grow/GROW_ART_W1–W8` | 8 | Art Teesside | v5-ish (S/S/S tiers) |
| **Total** | | **42** | | |

**Reconciliation with brief/T-audit (34):**
- **Agreement (34 lessons):** ASDAN 18 + GROW_HUM 8 + Art_Teesside/Grow 8 = 34 — exactly the brief's expected membership; corroborated by `HANDOVER.md` RM ledger (`RM: GROW_ASDAN 18`, `RM: GROW_HUM 7`, `RM: GROW_HUM_W7`).
- **Delta (+8 lessons):** `Grow/Slideshows/GROW_ART_W1–W8` — family "GROW · Art & Arts Award Aut 1", `type:lesson`, `year:2026-27`, keywords `['grow','art','arts award','explore','bronze','semh']`. **This is a genuine, catalogued GROW 2026-27 lesson suite the brief's 34 did not count.** Reasons it could have been excluded by the T-audit: (a) added after the @7889055a measurement; (b) treated as superseded by the Teesside studio suite. **Not forced.** Measured here (report-only — see §6, §7), and surfaced to Matt as the scope question (§8).

**Two distinct art suites, both GROW, both "Aut 1":** `Grow/Slideshows/GROW_ART` is built at **Arts Award Explore → Bronze** (identity portraits, matches SoW Autumn exactly); `Art_Teesside/Grow` is built as **full Bronze (Parts A–D)** (Teesside studio, skill-share). Not duplicates — different content and level. Their coexistence is the core of Gate 2 (§8).

---

## 3 · Strand → suite mapping (emitted before any classification depends on it)

SoW strands are the **14** rows of the `GROW Weekly - <Term>` sheets (the term sheets fold Humanities+RE and omit a distinct Enrichment row; the weekly sheets are canonical for strand identity).

| Estate GROW suite | → SoW strand (weekly sheet) | SoW term-sheet row | Mapping confidence | Notes / wrinkles resolved |
|---|---|---|---|---|
| ASDAN PEQ (6) | **Strand 11** "PfA: Independence, Careers & Vocational (ASDAN PEQ E3–L1 + Employability)" | `GROW - Autumn` r19 (Personal Effectiveness…) | High | Estate PEQ module = the PEQ core of the term-long PfA strand. E3 floor · L1 · L2 stretch matches SoW ("E3–L1 only in 2026/27"; L2 stretch deliberate, §4). |
| ASDAN Community Project / GCOMM (6) | **Strand 14** "Community Project & Vocational (flexible)" | `GROW - Autumn` r22–23 | High | Accredited via **PEQ 'Delivering a Project' + UAS community evidence** — supported by the SoW's own cross-credit model ("a single challenge can bank PEQ credit and cover another curriculum area"). **GCOMM_W3 deliberately feeds off the PEQ audit** (§4) — kept intact. |
| ASDAN Enterprise / ENT (6) | **Strand 12** "Enrichment Award: Young Duke + Community & Social Enterprise" | (weekly only) | Medium | ENT covers the **Community & Social Enterprise half** (idea→users→money→brand→pitch). The **Young Duke** half (first-aid/cookery/eco/sport progressive challenges) is **not** in this suite → SOW-SILENT(b) + scheme-level report-only ("Duke challenges-between-lessons assumption", §5). |
| GROW Humanities (8) | **Strand 4** "Humanities: History & Geography (Kapow)" | `GROW - Autumn` r10 | High | W1–W7 = Aut1·W1–W7 (History migration account); **W8 bridges to Aut2·W1** (atlas/Geography). W7 assessed → quarantine (§5). |
| GROW Art · Arts Award — Slideshows (8) | **Strand 9** "Creative Arts (Trinity Arts Award Explore/Bronze)" | `GROW - Autumn` r16 | High (content) | LOs match Aut1·W1–W7 near-verbatim; W8 = Aut2·W1 (festival music/sound). Level = Explore→Bronze (matches SoW Autumn). **Unscoped by brief (§2 delta) → report-only.** |
| Art Teesside · GROW (8) | **Strand 9** "Creative Arts" | `GROW - Autumn` r16 | Medium | Built as **full Bronze A–D**; tagged "Arts Aut 1". Gate 2(a) — SoW Autumn = Explore(→Bronze). **Patch quarantine** (§5) — fixes as proposed diffs only. |

**SoW strands with NO estate GROW lesson suite (mapping-derived, report-only):** English & Communication (1), Maths & Numeracy (2), Science (3), RE & World Views (5, delivered *as context* inside PEQ), PSHE & Citizenship (6), RSHE (7), Computing & ICT (8), PE (10), Design & Technology (13). See §5 SOW-SILENT(b).

---

## 4 · Per-lesson classification table

Classes: **ALIGNED · PARTIAL · MISALIGNED · SURFACE-SPLIT · SOW-SILENT · DELIBERATE-DIVERGENCE.**
Every row cites the SoW cell (weekly sheet · strand · week) and the lesson surface measured (sow-strip / LO `sc-v4` or `sc-box` / tag / award-strip / tiers / printPack / witness). Full verbatim surfaces captured in `_passsg/inputs/…` extraction (reproducible via `scratchpad/extract.py`).

### 4.1 ASDAN PEQ → Strand 11 (PfA/PEQ), `GROW Weekly - Autumn` r130
| Lesson | SoW cell | Lesson surfaces (sow-strip / LO) | Verdict |
|---|---|---|---|
| PEQ_W1 Knowing Myself | Aut1·W1 "Identify my strengths, interests and goals" | "…PEQ Level 1 (E3 floor · L2 stretch) · Week 1" / LO: audit strengths+interests, name development area, set starting point | **ALIGNED** |
| PEQ_W2 Goals That Work | Aut1·W2 "Begin an ASDAN PEQ L1 'wellbeing' unit" / planning-own-learning | LO: vague→specific dated goal, first step, success measure | **ALIGNED** |
| PEQ_W3 Working With Others | Aut1·W5 "Practise working with others" | award "PEQ L1 'Working with Others'"; LO: teamwork behaviours, real role, disagree-not-attack | **ALIGNED** |
| PEQ_W4 Managing Myself | Aut1·W3 "daily independence/self-management routine" | LO: routines>motivation, build routine, log actual-vs-plan | **ALIGNED** |
| PEQ_W5 Solving Problems | Aut2 problem-solving / decision-making PEQ unit | LO: break into steps, try+adjust, who to ask | **ALIGNED** (deliberate wrong-answer pill "Ignore it and hope" ×5 — protected, §4-est) |
| PEQ_W6 Present My Progress | Aut2·W6 "Review 'about me & my future' profile" / W7 complete | LO: present vs Week-1 audit, dated evidence, set next goal | **ALIGNED** |

### 4.2 ASDAN Community Project (GCOMM) → Strand 14, `GROW Weekly - Autumn` r174
| Lesson | SoW cell | Lesson surfaces | Verdict |
|---|---|---|---|
| GCOMM_W1 Our Patch, Our Say | Aut1·W1 "explore community & identify a need/opportunity" | LO: identify real needs, back with evidence, need≠complaint | **ALIGNED** |
| GCOMM_W2 Choose The Need | Aut1·W2 "agree goal and success criteria" | LO: weigh needs vs criteria, argue with evidence, commit | **ALIGNED** |
| GCOMM_W3 Roles, Steps, Resources | Aut1·W3 "decide roles" + W4 "plan steps/resources" | LO: ordered owned steps, role↔strength, cost list | **ALIGNED · DELIBERATE-DIVERGENCE** (W3 feeds off PEQ audit — cross-strand design, §4; never aligned away) |
| GCOMM_W4 First Contact | Aut1·W5 "first contact with partner" | LO: draft polite first contact, check tone, log reply→next step | **ALIGNED** |
| GCOMM_W5 Risk And Ready | Aut1·W6 "early project task" / off-site readiness | LO: rate risks, controls, logistics vs off-site reqs | **ALIGNED** (off-site partner approval pending = scheme-level, §5) |
| GCOMM_W6 Green Light | Aut1·W7 "record evidence" → plan sign-off | LO: present for sign-off, answer challenge, name first Aut2 delivery task | **ALIGNED** |

### 4.3 ASDAN Enterprise (ENT) → Strand 12 (Enrichment: …Social Enterprise), `GROW Weekly - Autumn` r144
| Lesson | SoW cell | Lesson surfaces | Verdict |
|---|---|---|---|
| ENT_W1 Helps And Earns | Aut1·W3 "plan a community or social-enterprise idea" | LO: what is enterprise, two engines of social enterprise, test a local example | **ALIGNED** (social-enterprise half) |
| ENT_W2 Spot The Gap | Aut2·W1 "develop the social-enterprise idea" (market gap) | LO: spot gaps, match to answer, 3 customer questions | **ALIGNED** |
| ENT_W3 Our Idea Our Users | Aut2·W2 "plan roles and resources" | LO: filter ideas, name customer+beneficiary, commit | **ALIGNED** |
| ENT_W4 Money In Money Out | Aut2·W2 (budget) / links FS Maths | LO: real costs, price+break-even, purpose of profit | **ALIGNED** |
| ENT_W5 Brand And Pitch | Aut2·W3 "run a small enterprise/community activity" (prep) | LO: brand fit, 5-part pitch, strong vs weak move | **ALIGNED** |
| ENT_W6 Pitch Day | Aut2·W3 (deliver) / W6 "share achievements" | LO: deliver section, capture feedback, decide next move | **ALIGNED** |
> **Suite-level note:** ENT is a coherent social-enterprise mini-course; it does **not** cover the strand's **Young Duke** enrichment challenges → SOW-SILENT(b), report-only (§5). Verdict per-lesson ALIGNED to the enterprise half; strand coverage PARTIAL at suite level.

### 4.4 GROW Humanities → Strand 4, `GROW Weekly - Autumn` r46 (v4 chassis)
| Lesson | SoW cell | Lesson LO (sc-v4) | Verdict |
|---|---|---|---|
| GROW_HUM_W1 Time Detectives | Aut1·W1 "place migration events on a timeline (chronology)" | date events + challenge a suspect date; place-clue; century/decade language | **ALIGNED** |
| GROW_HUM_W2 Source Detectives | Aut1·W2 "use a source to find out about migration" | provenance; infer + confidence; source usefulness | **ALIGNED** |
| GROW_HUM_W3 Cause And Consequence | Aut1·W3 "explain a cause and a consequence" | sort motive/condition/trigger; rank+defend; connect causes | **ALIGNED** |
| GROW_HUM_W4 People Who Shaped Britain | Aut1·W4 "investigate diverse British history (BHM)" | agency + context; weigh agency vs circumstance; respectful precision | **ALIGNED** |
| GROW_HUM_W5 Significance | Aut1·W5 "evaluate the significance of a person/event" | criteria; significance depends on perspective/timescale; qualify | **ALIGNED** |
| GROW_HUM_W6 Plan The Account | Aut1·W6 "plan a structured account using evidence" | structure point/evidence/explanation; select evidence; plan conclusion | **ALIGNED** |
| GROW_HUM_W7 Write The Account | Aut1·W7 "write and assess a structured account + source evaluation" | write in assessment conditions; use+explain evidence; answer enquiry | **ALIGNED** · **QUARANTINE** (pupil-assessed; §5 — no change contemplated) |
| GROW_HUM_W8 Where In The World | Aut2·W1 "locate countries/continents/oceans on a map/atlas" | index/grid/key; map route at scale; what the map adds | **ALIGNED** (W8 = Aut2 bridge; Gate 1 §8) |

### 4.5 GROW Art · Arts Award (Slideshows) → Strand 9, `GROW Weekly - Autumn` r102 — **UNSCOPED DELTA (report-only)**
| Lesson | SoW cell (Creative Arts) | Lesson LO (sc-box) | Verdict |
|---|---|---|---|
| GROW_ART_W1 Art Battle Tasters | Aut1·W1 "explore materials and techniques in my chosen art form" | explore materials/techniques (5 stations) | **ALIGNED (content)** |
| GROW_ART_W2 Level Up Portrait | Aut1·W2 "develop a skill and record it in my arts log" | develop skill; surreal "this is me" self-portrait; log | **ALIGNED** |
| GROW_ART_W3 Plan The Portrait | Aut1·W3 "plan an identity portrait or piece" | plan idea/materials/technique/symbol | **ALIGNED** |
| GROW_ART_W4 Create The Piece | Aut1·W4 "create my identity piece (BHM artist inspiration)" | create from plan using borrowed artist idea | **ALIGNED** |
| GROW_ART_W5 Review And Improve | Aut1·W5 "review and improve my work" | one star/one step; make one improvement; before/after | **ALIGNED** |
| GROW_ART_W6 Artist Research | Aut1·W6 "research an artist who inspires me" | research artist; 2 facts + 1 opinion | **ALIGNED** |
| GROW_ART_W7 Share The Portfolio | Aut1·W7 "share my Explore portfolio evidence so far" | present portfolio (3 stems); log next step | **ALIGNED** |
| GROW_ART_W8 Festival Sounds | Aut2·W1 "explore festival music, sound and instruments" | describe sound (volume/tempo/rhythm); sound→feeling | **ALIGNED** (W8 = Aut2 bridge) |
> **Suite-level flags (report-only, unscoped):** (i) no **Supported/Standard/Stretch** tier structure (uses `.sc-box`/`.aspire-box` only) — divergent chassis; (ii) Aspire framed as **"GCSE Stretch / GCSE Art habit / GCSE development page"** — the SoW's GROW arts route is **Arts Award** (GCSE Art is not in the SoW arts accreditation; GCSE is a LAUNCH pathway concept) → Gate 2(c-analogue), tabled §8.

### 4.6 Art Teesside · GROW → Strand 9, `GROW Weekly - Autumn` r102 — **PATCH QUARANTINE (proposed diffs only)**
| Lesson | SoW cell | Lesson LO / award | Verdict |
|---|---|---|---|
| GROW_ART_W1 The Local Canvas | Creative Arts Aut (skills/inspiration) | map local area; select sites; plan map→studio / "Bronze Part A" | **PARTIAL — Gate 2(a)** |
| GROW_ART_W2 Studio Skills & Safe Practice | ″ (develop skills) | tools/materials safely; technique control / "Bronze Part A (Skills)" | **PARTIAL — Gate 2(a)** |
| GROW_ART_W3 Independent Studio Challenge | ″ | set own challenge; independent choices; record decisions / "Bronze Part A (Challenge)" | **PARTIAL — Gate 2(a)** |
| GROW_ART_W4 Arts Event Attend/Capture/Review | Aut1·W-equiv "review an arts event" | audience; capture; review with reasons / "Bronze Part B" | **PARTIAL — Gate 2(a)** |
| GROW_ART_W5 Practitioner Career & Inspiration | Aut1·W6 "research an artist who inspires me" | describe arts career; what inspires; link to own / "Bronze Part C" | **PARTIAL — Gate 2(a)** |
| GROW_ART_W6 Plan & Rehearse the Skill Share | ″ (skills/sharing) | choose teachable skill; break into steps; rehearse / "Bronze Part D (Plan)" | **PARTIAL — Gate 2(a)** |
| GROW_ART_W7 Deliver the Skill Share & Curate | Aut2·W-equiv "share/perform" | teach skill; adapt; curate evidence / "Bronze Part D (Deliver)" | **PARTIAL — Gate 2(a)** (tri-channel skill-share protected, §4) |
| GROW_ART_W8 Reflect, Audit & Close the Loop | Aut2·W7 "complete arts log + Explore/Bronze evidence" | audit portfolio vs Bronze; strongest evidence; close the loop / "Bronze · Reflect + Portfolio Audit" | **PARTIAL — Gate 2(a) + 2(d)**: Aspire "**draft the Silver ambition**" = Silver language on a Bronze artefact (known repeat defect) |

### 4.7 Counts (unit: lessons)
- **ALIGNED: 34** (PEQ 6 + GCOMM 6 + ENT 6 + HUM 8 + Slideshows-Art 8) — of which 8 (Slideshows-Art) are **unscoped-delta/report-only** and 1 (HUM_W7) is quarantined.
- **PARTIAL (Gate 2 pending): 8** (Art_Teesside/Grow, all quarantined).
- **MISALIGNED: 0.**
- **SURFACE-SPLIT: 0** (no screen/print disagreement found; print strings mirror screen exactly — e.g. PEQ_W1 success phrase appears identically 8× across screen+print).
- **DELIBERATE-DIVERGENCE (sub-tag): GCOMM_W3** (PEQ cross-feed).
- Total classified: **42 lessons** (= derived population; cardinality asserted).

---

## 5 · SOW-SILENT (both directions, both report-only) & quarantines

**(a) Lessons with no plausible SoW strand row:** **none** — every one of the 42 maps to a strand (§3).

**(b) SoW strands with no estate GROW lesson suite** (expected — taught by colleagues from other resources; an empty strand is NOT a defect):
English & Communication · Maths & Numeracy · Science · RE & World Views (delivered *as PEQ context*, not a standalone suite) · PSHE & Citizenship · RSHE · Computing & ICT · PE (PE Passport) · Design & Technology (ASDAN Foodwise/Textiles/Construction — **no GROW D&T suite in the estate**; BUILD side has `Build/Slideshows/BUILD_DT_*` and `DT_Community_Upcycling`). Also the **Young Duke** half of Strand 12 (enrichment challenges done between lessons).

**Computing/ICT (Gate 2 note):** SoW describes generic NC/functional digital skills; the recorded 2026-27 GROW ICT plan is AI-first via bespoke AQA UAS L1 — **Matt's live plan, not a defect.** No GROW ICT lesson suite exists to collide with it; no action.

**Quarantines honoured:**
- **GROW_HUM_W7** — pupil-assessed; inside population; read + classified only; **no change contemplated.** No other assessed markers anywhere in the 42 (grep for "assessment conditions"/"summative"/"exam conditions" returns only HUM_W7).
- **Art_Teesside/*** — read + classified; **any fix = proposed diff in FINDINGS only, no commits.** (None proposed as a commit; Gate 2 items tabled §8.)
- **Sentinel-45 / `ll-g`** — no scoped GROW lesson carries it; gate not engaged (BV-3).
- **`ps_coldcall_roster` (8 files) / `_ccQuestions` (26 files) / all storage keys** — inventoried; **none renamed or migrated.**
- **Witness printPack wiring** (18 ASDAN carry `print-witness`) — **not edited.**
- **hud.js / theme.js / shared engine** — not touched.

---

## 6 · Deliberate designs & protections — confirmed present and intact (not "fixed")

- **18/18 GROW ASDAN** carry the printable **Assessor Witness Statement** (`print-witness` in the id array) + on-screen witness panel + Access/sensory notes. Confirmed, untouched.
- **GROW ASDAN built at L1 with L2 *stretch*** by design; sow-strip reads "PEQ Level 1 (E3 floor · L2 stretch)". **No surface claims L2 registration/accreditation** — award-strips bank "ASDAN PEQ L1…" only. **Gate 2(b) CLEAR.**
- **GCOMM_W3** feeds off the PEQ audit — cross-strand design, intact.
- **Match pills include deliberate wrong answers** (PEQ_W5 "Ignore it and hope") — present, not resequenced/corrected.
- **Art_Teesside W7 tri-channel skill-share** (station wording present) and W5 organisation-card escalation — present, quarantined.
- **Lundy after the timer**, safeguarding lines, calm palettes, icon+label+colour (no colour-alone), no leaderboards, no "REJECTED" verdicts, answer keys staff-side, no mark schemes authored — all consistent with the estate SEMH rules; nothing authored against them.
- **Witness section makes GROW ASDAN packs 14 sections** — noted; not "corrected" to 13.

---

## 7 · Tiered outcomes

**Tier 1 (auto-fix, committed):** **NONE.** The brief-scoped, non-quarantined suites (ASDAN 18, GROW_HUM 8) show no stale week/title metadata, no wrong half-term/theme in any sow-strip, no vocab typos against the SoW column, and no print/screen string disagreements. There is nothing that is simultaneously mechanical, zero-meaning, and in-scope. (Nothing on GROW_HUM_W7 or Art_Teesside is ever Tier 1.)

**Tier 2 (build-then-ask):** **NONE built.** No LO/SC-meaning, task, KO, or accreditation change is warranted on the scoped suites — they align. Any Art_Teesside change is a *proposed diff only* (quarantine) and depends on the Gate 2 ruling (§8), so nothing is pre-built.

**Tier 3 (report-only):**
- **T3-1** `Grow/Slideshows/GROW_ART` (8) is a catalogued GROW suite outside the brief's scoped 34 — scope decision for Matt (§8-Q).
- **T3-2** `Grow/Slideshows/GROW_ART` has no Supported/Standard/Stretch tier structure (divergent older chassis) — structural, out of scope to "fix" without a build decision.
- **T3-3** `Grow/Slideshows/GROW_ART` Aspire uses "GCSE" framing vs the SoW's Arts-Award-only GROW arts route.
- **T3-4** `Art_Teesside/Grow` built as full Bronze A–D while tagged "Arts Aut 1"; SoW Autumn Creative Arts = Explore(→Bronze) — Gate 2(a).
- **T3-5** `Art_Teesside/Grow/GROW_ART_W8` Aspire "draft the Silver ambition" — Silver language on a Bronze artefact — Gate 2(d).
- **T3-6** ENT suite does not cover the Young Duke enrichment half of Strand 12 (SOW-SILENT(b) / scheme-level).
- **T3-7** Scheme-level report-only (unchanged): community partner off-site approval pending; GCOMM_W1 week-one survey dependency; Duke challenges-between-lessons assumption.

---

## 8 · Gates

**Gate 1 — week mapping: RESOLVED by derivation (no question needed).**
- ASDAN suites run **W1–W6** = a 6-week Autumn-1 module inside the term-long PfA/Community/Enrichment strands (plan phase; GCOMM_W6/PEQ_W6/ENT_W6 explicitly hand off to Aut 2). No ambiguity.
- HUM & both Art suites run **W1–W8**: **W1–W7 = SoW Aut1·W1–W7**, **W8 = SoW Aut2·W1** (HUM_W8 atlas/Geography; ART_W8 festival music). This is consistent with the school's **8-week Autumn-1 calendar** (brief §6): the 8th teaching week delivers the first Aut-2 content. Derived per-suite from planner "Week n of m" strings + LO content; recorded, not guessed.

**Gate 2 — accreditation/level: TABLED (one consolidated question, §8-Q).** Repo cannot settle these — they are curriculum-design decisions:
- (a) Two GROW art suites, both "Aut 1": Slideshows = **Explore→Bronze** (matches SoW Autumn); Art_Teesside = **full Bronze A–D**. Is this intended dual provision (Explore entry + Bronze progression), and is Art_Teesside's "Aut 1" tag correct (vs a later-term Bronze route)?
- (b) *(cleared — no L2 registration claim anywhere.)*
- (c) Computing/ICT AI-first UAS plan — no collision (no GROW ICT suite); no action.
- (d) `Art_Teesside/Grow/GROW_ART_W8` "Silver ambition" language on a Bronze artefact — remove/keep? (quarantine → proposed only).
- (+scope) Should `Grow/Slideshows/GROW_ART` (the +8 delta) be in GROW SoW-alignment scope, or is it superseded by the Teesside Bronze route?

**§8-Q — the single consolidated question put to Matt:** see chat message accompanying this pass (Art level + population scope). No Tier-2 work proceeds until answered; nothing merges regardless.

---

## 9 · Close-out — final verification sweep (at branch tip)

- **Files modified in this pass:** `_passsg/` only (`inputs/GROW SOW 2026-27.xlsx`, `SOW_MATRIX.md`, `FINDINGS.md`). **Zero lesson files touched.**
- **node --check / jsdom-boot / tag balance:** N/A — no `.html` inline script block was edited (no lesson file changed). Nothing to re-validate.
- **Print-section counts:** unchanged (no pack edited); GROW ASDAN packs remain 14 sections (witness included) — not "corrected".
- **Sentinel-45:** untouched (no `ll-g` file edited); assertion not required.
- **Base SHA:** `32ca685e1df619b333f3ee4385aed227aa675cdf`. **Branch tip (this pass's substantive commit):** `9b9bde4f8a52` (derived via `git rev-parse`; the tip-stamp commit that records this line sits one above it).
- **Nothing merged. Stop.**

---

## 10 · Post-Gate-2 addendum — Matt's ruling + deeper-read corrections

Matt answered the §8 consolidated Gate-2 question (2026-07-28):
- **Art scope:** *Both* GROW art suites in scope — `Grow/Slideshows` = Explore entry, `Art_Teesside/Grow` = Bronze progression (intended dual provision). ✅
- **Art_Teesside:** *Prep proposed diffs* for (i) the "Aut 1" half-term tag and (ii) the W8 "Silver ambition" line.

### 10.1 ACTIONED — Slideshows GROW_ART "GCSE" stretch → "Bronze" (Tier-2, committed to branch)
- **Now in scope** (Matt). One defect class across all 8 lessons: aspire-box label read **"GCSE Stretch"** and 3 body phrases named a **"GCSE Art habit / development page"**. The SoW accredits GROW Creative Arts via **Trinity Arts Award Explore/Bronze**; GCSE Art is not in the SoW arts accreditation (GCSE = LAUNCH concept).
- **Fix:** relabelled → **"Bronze Stretch"** (×16) + 3 body phrases aligned to Bronze. **Task content unchanged.**
- **SoW cell:** `GROW Weekly - Autumn` · Creative Arts (r102); Pathway Ladder GROW Creative Arts = "Explore / Bronze".
- **Surface:** `.aspire-box` (2/file, on-screen only; print pack is JS-built from `LESSON.*`, no mirror — verified).
- **Verification:** occurrence count 19 `GCSE` → **0**; 16 `Bronze Stretch:` labels present; tag-multiset unchanged vs prior; `section`/`div`/`strong` balanced across all 8.
- **Commit:** `cdc9623` · **Rollback:** `0b4597a`. **Not merged.**

### 10.2 WITHDRAWN as non-defects on deeper read (repo wins over the flag; §4 "never fix deliberate designs")
The two Art_Teesside proposals were approved on my §8 framing. Closer reading of the files **reverses that framing** — prepping either diff would damage deliberate, correct design. No diff prepped; recorded report-only.

- **W8 "Silver" language — NOT Gate 2(d).** "Silver" appears **16×** in `GROW_ART_W8`, forming the lesson's spine: it is the **Bronze→Silver bridge** close-out (the "Silver prospectus" maps Bronze evidence to Silver's *future* demands; "Silver is Bronze at project scale: today's prospectus is the bridge"). The **award-strip is correctly "🎨 Bronze"**; there is **no claim the portfolio IS Silver / is Silver-accredited** (defect test negative). Silver is the correct next tier (Pathway Ladder: LAUNCH Creative Arts = **Silver/Gold**). This is legitimate laddering, not "Silver-tier language tagging a Bronze artefact." **Recommendation: leave verbatim.** (The brief's Gate 2(d) target — a *false Silver claim/registration on a Bronze artefact* — does not occur here.)
- **"Arts Aut 1" tag — plausibly correct, not a clear defect.** sow-strip = `Progress SoW · Arts Aut 1 · 2026–27 · GROW · Week N` (nbsp `Aut\xa01`). With dual provision confirmed, the Teesside **Bronze** route may be the school's **Autumn** GROW-art delivery (8-week intensive) alongside the Slideshows Explore suite; the tag is then accurate. Re-tagging to Spring/Summer would assert a term placement the files do not support and the repo does not confirm. **Recommendation: leave as-is unless Matt confirms the Teesside Bronze route is taught in a later term** — in which case a one-line sow-strip re-tag (8 files, `Aut 1` → the taught term) is the entire change, delivered as a proposed diff (quarantine, no auto-commit).

### 10.3 Revised classification for Art_Teesside/Grow (supersedes §4.6 tentative Gate-2(d) on W8)
- W1–W7: **DELIBERATE-DIVERGENCE** — Bronze A–D build; level is the confirmed Bronze-progression provision (not a defect vs SoW Autumn Explore, given dual provision). Quarantine — report-only.
- W8: **DELIBERATE-DIVERGENCE** — Bronze close-out with correct Bronze→Silver bridge. **Gate 2(d) cleared** (award correctly Bronze; no false Silver claim). Quarantine — report-only.

### 10.4 Slideshows tier-structure (S/S/S) — Tier-3 recommendation, NOT actioned
`Grow/Slideshows/GROW_ART` has no Supported/Standard/Stretch differentiated tasks (only `.sc-box`/`.aspire-box`). Adding proper tiers is a **chassis rebuild across 8 lessons** — substantial pedagogical authoring, not a discrete SoW-cell mismatch. Recommended as a **separate scoped build pass** (build-then-ask per lesson), not attempted here (risk of damaging working lessons in a measurement pass). Matt indicated openness ("if you want") — flagged for a future dedicated pass.

### 10.5 Revised tier tally (supersedes §7)
- **Tier 1 (auto-commit):** 0 — unchanged.
- **Tier 2 (built on branch, awaiting merge):** **1 defect class** — Slideshows GCSE→Bronze (8 files, commit `cdc9623`).
- **Tier 3 (report-only):** Art_Teesside level/tag/Silver (all deliberate-correct — leave); Slideshows S/S/S tier rebuild (future pass); ENT/Young Duke coverage; scheme-level items.
- **Still nothing merged.** Branch tip advances to `cdc9623`; Matt merges.
