# Build SOW 2026-2027 — vC-PROPOSED · change table

**Status:** PROPOSAL for Matt's review. vC becomes operative only when Matt adopts it.
**Produced by:** Pass SBX (execution arm of Pass SB), from the operative vB instrument.
**Author:** automated close-out session, 2026-07-28.

## Provenance chain (unbroken; nothing upstream modified)

| Version | Role | File | sha256 | Touched this pass? |
|---|---|---|---|---|
| **vA** | archived, **superseded** | `Build/_Archive_VersionA_LivingIndependently/BUILD_SOW_2026-27_vA_with_LivingIndependently.xlsx` | (unchanged) | **No** |
| **vB** | **operative instrument** | `_passsb/inputs/Build SOW 2026-2027.xlsx` | `730f9a86a105a50fae64cc3560deb33a8f78f8a15959c608fa0c9fc197ce5bac` | **No** (loaded read-only) |
| **vC** | **proposal** (this file's sibling) | `_passsbx/proposed/Build SOW 2026-2027 vC-PROPOSED.xlsx` | generated from vB | new file |

vB's sha256 was re-checked after generation and is **byte-identical** to the committed instrument — vA and vB were not written.

## Scope — three change sets and nothing else

24 cell edits, all in-place (no rows inserted → every merged range, column width and cell
style preserved; the openpyxl 3.1.5 `insert_rows`/`CellRange.shift` hazard does not arise).
The workbook contains **0 formula cells**, so no recalculation is involved.

### W1 — Humanities realigned to the eight BUILD_HUM lessons  (15 cell edits)

| Sheet | Cell | Before | After |
|---|---|---|---|
| BUILD Weekly - Autumn | `C46` | Talk about my family and people special to me. | Place local Teesside events on a timeline (earliest left) and turn a year into its century; use a clue to say WHEN something happened. |
| BUILD Weekly - Autumn | `C47` | Identify people who help us in the community. | Say what a historical source shows and suggest what it might mean; back one idea with a detail I can point to. |
| BUILD Weekly - Autumn | `C48` | Recognise places in my local community. | Give reasons why people came to Teesside and sort them into push and pull factors; link a reason to a real example. |
| BUILD Weekly - Autumn | `C49` | Sort 'then and now' photographs. | Describe what one person or group did and one way they shaped Britain, without lumping a whole community together. |
| BUILD Weekly - Autumn | `C50` | Show respect for what makes us same/different (Black History Month). | Judge whether an event was a big deal or a small deal, give one criterion, and accept that others might rank it differently. |
| BUILD Weekly - Autumn | `C51` | Contribute to a class community map. | Plan a historical account: choose the order, pick evidence for each part, and say what the story will explain. |
| BUILD Weekly - Autumn | `C52` | Share a group/team/community I belong to. | Tell my planned historical account in order, use a piece of evidence, and finish with what it explains. |
| BUILD Weekly - Autumn | `C53` | Explore a festival of light and why it matters. | Find Teesside and a journey route on a map using the key; say one way migration shaped where we live. |
| BUILD Weekly - Autumn | `D46` | NC KS1 History & Geography (adapted) · ACT primary citizenship framework · AQA UAS. | Kapow History & Geography (KS2/3 disciplinary enquiry) · AQA UAS. |
| BUILD - Autumn | `D10` | My family, my community & special people | Local history enquiry: Teesside timeline, sources & migration |
| BUILD - Autumn | `E10` | Talk about own family and community in sentences; recognise that people belong to different groups; identify a special person and explain why. | Sequence local events and use centuries; interrogate sources for what they show and mean; explain why people migrated to Teesside using push and pull factors; describe significant people and judge historical significance; plan and tell an evidenced historical account. |
| BUILD - Autumn | `F10` | Family photo sharing; community walks and visitors; ‘people who help us’; BHM significant people (blends with English/PSHE). | Build a Teesside history timeline; work as history detectives on real sources; sort push/pull reasons for migration; study people who shaped Britain; rank events by significance; plan, tell and map a local history story (blends with English). |
| BUILD - Autumn | `G10` | family, community, special, help, belong | timeline, century, source, evidence, push factor, pull factor, migration, significance, account |
| BUILD - Autumn | `H10` | Coming to England (shared extracts, supported); community photos | Coming to England (migration extracts, supported); local archive photographs, maps and historical sources |
| BUILD - Autumn | `J10` | F: discussion and sorting.  S: ‘my community’ book page. | F: timeline and source tasks.  S: an evidenced Teesside history account (Dec). |

### W2 — Living Independently restored to the Pathway Ladder (BUILD)  (1 cell edits)

| Sheet | Cell | Before | After |
|---|---|---|---|
| Pathway Ladder | `B14` | Foodwise / Gardening taster short courses. Floor: supported single-step tasks. | ASDAN Living Independently, Foodwise & Gardening taster short courses. Floor: supported single-step tasks. |

### W3 — Autumn Creative Arts: Discover → Explore (Gate-2 ruling)  (8 cell edits)

| Sheet | Cell | Before | After |
|---|---|---|---|
| BUILD - Autumn | `D16` | Identity portraits & self-image in art (Arts Award Discover) | Identity portraits & self-image in art (Arts Award Explore) |
| BUILD - Autumn | `F16` | Drawing and painting techniques; identity portraits (blends with PSHE identity); explore a BHM artist; begin Arts Award Discover log. | Drawing and painting techniques; identity portraits (blends with PSHE identity); explore a BHM artist; begin Arts Award Explore log. |
| BUILD - Autumn | `I16` | Trinity Arts Award (Discover), Part A/B begun; AQA UAS, ‘Creating artwork’. | Trinity Arts Award (Explore), Part A/B begun; AQA UAS, ‘Creating artwork’. |
| BUILD - Autumn | `I17` | Trinity Arts Award (Discover) continued; AQA UAS, ‘Performing in a group’. | Trinity Arts Award (Explore) continued; AQA UAS, ‘Performing in a group’. |
| BUILD - Autumn | `J17` | F: participation.  S: performance + Discover log (Dec). | F: participation.  S: performance + Explore log (Dec). |
| BUILD Weekly - Autumn | `A102` | Creative Arts (Trinity Arts Award Discover) | Creative Arts (Trinity Arts Award Explore) |
| BUILD Weekly - Autumn | `D102` | Trinity Arts Award Discover (Part A: take part; Part B: find out about an artist) · art, music, drama. | Trinity Arts Award Explore (Part A: take part; Part B: find out about an artist) · art, music, drama. |
| BUILD Weekly - Autumn | `F102` | Arts Award Discover log (Parts A-B). F: arts-log photos. S: identity artwork + festival performance (Dec). | Arts Award Explore log (Parts A-B). F: arts-log photos. S: identity artwork + festival performance (Dec). |

## Mapping decisions & flags (read before adopting)

### W1 — Humanities (Matt's ruling: *the workbook moves, not the lessons*)
- **Lesson → weekly-cell mapping.** The estate's eight `BUILD_HUM` decks are a single sequential
  Teesside local-history disciplinary arc (W1 timeline → W2 sources → W3 push/pull migration →
  W4 significant people → W5 significance → W6 plan account → W7 tell account → W8 map/migration).
  They are mapped to the **eight consecutive** Humanities weekly cells beginning at Aut1·W1:
  `C46–C52` (Aut1·W1–W7 = lessons W1–W7) and `C53` (Aut2·W1 = lesson W8).
- **Wording is derived ONLY from each lesson's own title + "Success looks like" (SC) surfaces** —
  no content invented. (LO slides carry no separate greppable objective; title+SC were the sources.)
- **Cells with no matching lesson — KEPT and flagged:** `C54–C59` (Aut2·W2–W7, six weekly cells)
  retain their existing SoW text (festivals of light / remembrance / rights). The eight-lesson arc
  does not reach them; they are taught from other provision or are Matt's to populate.
- **`D46` (strand alignment, merged `D46:D59`)** changed `NC KS1` → `Kapow History (KS2/3
  disciplinary enquiry)` to match the lessons Matt ruled the workbook onto. ⚠ This merged cell also
  spans the six kept festival weeks — verify the alignment label still reads acceptably for them.
- **KEPT and flagged (Matt's Tier-3 curriculum call, per Pass SB FINDINGS §3.2):**
  the strand **labels** still read *"World About Me (Humanities)"* (`A46`) and *"World About Me
  (Humanities & RE)"* (`A10`). The content is now KS2/3 disciplinary; Matt may wish to rename the
  strand. Not renamed here — a label change is a curriculum-pitch decision, not a content realignment.
- **Term row 11 (Aut2, `D11`–`K11`) KEPT.** Only its first week maps to a lesson (W8), already
  captured at weekly `C53`; the rest of the Autumn-2 half-term has no `BUILD_HUM` lesson.
- **KEPT:** `E46`/`F46` (strand resources / UAS accreditation) and `I10`/`K10` (RE-PEQ accreditation,
  SEND scaffolds) — not lesson-content surfaces; some still reference festival/community material that
  overlaps the kept weeks. Flagged for Matt if he wants them fully re-pointed.

### W2 — Living Independently → Pathway Ladder BUILD (`B14`)
- Restored **ASDAN Living Independently** to the Ladder BUILD cell so it **agrees with weekly
  strand 11** (`D130` = "ASDAN Living Independently / Foodwise (Entry)"), the weekly-operative reading
  the Pass SB audit adopted. Foodwise and Gardening were **kept** (pure addition, nothing removed).
- Ladder ⇄ strand now agree: both name Living Independently at BUILD.

### W3 — Autumn Creative Arts Discover → Explore (Gate-2 ruling)
- Changed every "Discover" award-level surface in the **Autumn** Creative Arts term row
  (`D16, F16, I16, I17, J17`) and weekly strand (`A102` label, plus `D102`/`F102` — the strand's
  alignment and log cells that also name the award level, changed to keep the weekly strand internally
  consistent rather than leaving `Explore` label over `Discover` body).
- **KEPT (correct, per the brief):** Pathway Ladder `B11` *"Trinity Arts Award Discover / Explore.
  Floor: Discover w/ support."* — already right, unchanged.
- ⚠ **RESIDUAL, OUT OF W3's Autumn scope — for Matt:** the **Spring** and **Summer** Creative Arts
  rows still read "Discover" and were **not** touched (W3 is Autumn-only, "nothing else"):
  `BUILD - Spring` `F16/I16/J16/I17/J17`; `BUILD Weekly - Spring` `A88/D88/F88`;
  `BUILD - Summer` `I16`; `BUILD Weekly - Summer` `A94/D94/F94/C106`. If Matt wants the whole year
  consistent with the Explore ruling, these are the follow-on cells. (`Qualification Map` and
  `Programmes & Frameworks` name the full Discover→Gold ladder correctly and should stay.)

## Round-trip verification (all PASS)

| Check | Result |
|---|---|
| Sheet names unchanged | **PASS** — 11 sheets, identical order |
| Row/column counts per sheet | **PASS** — every sheet's `max_row`/`max_col` identical to vB |
| Merged ranges per sheet | **PASS** — identical set on every sheet |
| Only intended cells changed | **PASS** — exactly 24 differing cells, all in the change set; zero drift |
| Every edited cell reads back exactly | **PASS** — 24/24 |
| vA / vB unmodified | **PASS** — vB sha256 byte-identical after generation; vA archive untouched |

## What remains Matt's

1. **Adopt vC** (rename to operative) or return edits.
2. **W1 flags** above — the strand-label rename and the kept `D46`/`E46`/`F46`/Aut2 cells.
3. **W3 residual** — decide whether Spring & Summer Creative Arts should also move Discover → Explore.
4. **Book the Discover & Explore adviser training** (Pass SB R5): running Arts Award **Explore** at
   BUILD needs the separate Discover & Explore adviser course — the Bronze & Silver course being
   arranged does not cover it. Owner: Matt / Graham.
