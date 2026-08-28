# ORDER N6 — FINDINGS

`mbm-next-six-weeks-2026-08-28-N6` · worked 2026-08-28 · branch `claude/new-session-llckrn`

Twelve packs, 246 files, 192 HTML. Nine packs are repaired, gated and landed. Three
(the Art packs) are held on a STOP, and one item (N5) is held on a STOP inside a
landed pack. Two questions are open for Matt and are named in §Open.

---

## §0.1 Pre-gate — all four assertions PASS

| assertion | result |
|---|---|
| `_passpq/SPEC_FACTS.md` on `origin/main` | PASS |
| `_passpq/SPEC_FACTS_L2.md` | PASS |
| `_passsb/inputs/`, `_passsg/inputs/`, `_passsl/inputs/` contain the SoW workbooks | PASS — `Build SOW 2026-2027.xlsx`, `GROW SOW 2026-27.xlsx`, `LAUNCH KS4 - 2026-27.xlsx` |
| `_passpq/TIMETABLE_2026-27.md` | PASS |

`origin/main` tip at intake: **`288f84543ccef2884de62e6002b4b814360249c1`** — *"Close C4 as a
false positive in the four records that carry it (#161)"*.

`pass-sl-sow-launch` **IS** an ancestor of `origin/main` (tip `2a1cfda`, 0 commits ahead).
Order SAT-F's merge is in. Nothing merged here.

**A trap worth naming.** The LOCAL `main` ref in this checkout is `8d748424` and is **108
commits behind** `origin/main`. Measuring the estate standard against it gives 130
occurrences across 40 files; against `origin/main` it is **136 across 37**. Every estate
figure in this document is measured against `origin/main`.

---

## §0.2 Intake — re-derived, and it matches

| Pack | files | html | checksums |
|---|---|---|---|
| BUILD_ASDAN_AUT2_W1-W6 | 31 | 28 | none |
| BUILD_Art_Spring2_… | 16 | 11 | SHA256SUMS ✓ |
| BUILD_Humanities_W9-W14 | 12 | 8 | none |
| BUILD_Science_W8-W13_Next_12 | 20 | 15 | SHA256SUMS ✓ |
| GROW_ASDAN_Autumn2_W1-W6_Next_18 | 27 | 22 | CHECKSUMS ✓ |
| GROW_Art_Spring2_… | 16 | 11 | SHA256SUMS ✓ |
| GROW_Humanities_W9-W14 | 12 | 8 | none |
| GROW_Science_W8-W13_Next_12 | 20 | 16 | SHA256SUMS ✓ |
| LAUNCH_ASDAN_W7-W12_2026-27 | 36 | 32 | none |
| LAUNCH_Art_Spring2_… | 16 | 11 | SHA256SUMS ✓ |
| LAUNCH_Humanities_W9-W14_Next_6 | 14 | 9 | SHA256SUMS ✓ |
| LAUNCH_Science_W8-W13_Next_18 | 26 | 21 | SHA256SUMS ✓ |
| **TOTAL** | **246** | **192** | 8 supplied |

**Zero disagreement with the chat figures.** Every count reproduced exactly.

### Deviations from the chat measurements

| # | chat said | measured | consequence |
|---|---|---|---|
| 1 | checksums verified "105 files, 0 mismatches" | **147 entries**, 0 mismatches | none — the clean result stands, the population was larger than reported |
| 2 | "**0 `@keyframes` anywhere**, so residue is zero by construction" | **18 `@keyframes`**, one per GROW_ASDAN lesson | none — see below |
| 3 | "34 unique external URLs" | **30** | none — see N11 |
| 4 | "79/79 ASDAN witness surfaces" carry the T2-4 block | **79** confirmed | none — an initial count of 80 was my own extracted copy |

**On deviation 2.** GROW_ASDAN's 18 lesson decks each carry `@keyframes orbit`, a decorative
hero rotation. It is *properly guarded twice over*: both `@media (prefers-reduced-motion:
reduce)` and `.calm` set `animation:none!important` **and** `display:none` on the
`.hero-visual` pseudo-elements. The accessibility invariant holds; only the "zero by
construction" claim is wrong. §4 gate 5 is therefore measured as a **delta** — no NEW
`@keyframes` — rather than an absolute zero it never had. Intake 18 → now 18.

---

## §1 — the thirteen items

| item | outcome |
|---|---|
| **N1** manifest ghosts | **FIXED** — trimmed to disk |
| **N2** learner confirmation | **FIXED** — 75 surfaces |
| **N3** LAUNCH_ASDAN print route | **FIXED** — 30 lessons |
| **N4** PEQ level anchor | **NO CHANGE REQUIRED** — premise does not hold; gate green |
| **N5** week mapping | **STOP — AMBIGUOUS**, both readings below |
| **N6** tier vocabulary | **PARTIALLY FIXED** — the labels that are labels |
| **N7** chassis furniture | **PARTIAL** — way-home + splash; toggle HELD on Matt's ruling |
| **N8** checksums | **FIXED** — 193 entries across 9 packs |
| **N9** index.html twin | **FIXED** — KEEP-WITH-REASON |
| **N10** UAS hedge | **FIXED** — 90 staff-facing sites |
| **N11** link liveness | **CANNOT MEASURE HERE** — egress policy; nothing removed |
| **N12** Art placement | **STOP — the premise is refuted** |
| **N13** spec code | **CONFIRMED as built** |

### N1 · BUILD_ASDAN manifest ghosts — FIXED

Measured exactly as reported: 32 manifest HTML entries, 28 on disk, **4 ghosts, 0 orphans**.
The ghosts live in `optionalWeek7Closes`, not `lessons`.

D1 applied — trimmed to disk, no lessons authored. **Nothing was lost, and that is
checkable rather than asserted:** each ghost carried a SoW cell pair, and
`BUILD_ASDAN_AUT2_W7_PORTFOLIO_STUDIO.html` already delivers all four closes quoting the
*same* cells verbatim.

| ghost filename | SoW cells | canonical outcome |
|---|---|---|
| `…A2_PFA_W7_Independence_Portfolio_Evidence.html` | `B143`/`C143` | Add evidence to my independence portfolio. |
| `…A2_DUKE_W7_Sign_Off_Challenges_and_Evidence.html` | `B157`/`C157` | Sign off Duke challenges; evidence (UAS). |
| `…A2_CON_W7_Review_Skills_and_Add_Evidence.html` | `B172`/`C172` | Review my D&T skills and add ASDAN/UAS evidence. |
| `…A2_COMM_W7_Reflect_on_Teamwork_and_Add_Evidence.html` | `B187`/`C187` | Reflect on teamwork and add ASDAN/UAS evidence. |

The reason is recorded inside the manifest (`optionalWeek7ClosesNote`) so a later pass does
not restore them. Gate: manifest HTML set == disk HTML set, both directions, 0 diff.

### N2 · Learner confirmation — FIXED, 75 surfaces

Ported, not invented. Recovered byte-for-byte from live carriers on `origin/main`. **Two
variants exist and they differ only in four newlines:** BUILD_ASDAN + GROW_ASDAN carry a
566-byte pretty-printed form (×49), LAUNCH_ASDAN a 562-byte minified form (×30). 49 + 30 =
the 79 the order names. Each pack receives its own lane's form.

Surfaces: BUILD 24 lessons + evidence window + W7 studio = 26; GROW 18 lessons + evidence
window = 19; LAUNCH 30 lessons. **Total 75**, exactly the order's arithmetic.

**The order's insertion anchor does not exist in these packs.** D2 says "insert after the
assessor declaration table". `witness` structure is 0 files, and the evidence windows
explicitly disclaim being assessment records — *"This page helps staff connect authentic work
to learner meaning. It stores, uploads and scores nothing"*, and *"criteria, assessment and
any claim remain with the authorised coordinator/assessor"*. There is no table to insert
after. The block therefore sits at the **end of the print surface**, which is the coherent
placement given N3's own reasoning: the printed deck is the portfolio artefact, so the
learner signs the artefact.

**A bug that only a render caught.** BUILD_ASDAN's 24 decks have a real print surface —
`<section class="print-pack">` — gated by `body>*:not(.print-pack){display:none!important}`.
Appending before `</body>` put the block *outside* that container. All 24 decks carried it
and **none of them printed it**. A grep for the block reported 75/75 success; a headless
print render reported 51/75. The block now goes in as a final `.print-page` inside
`.print-pack`, which is what "confine to the print surface" means on that chassis.

Evidence, in Chromium: **75/75 render the block in print, 0/75 on screen** (using
`checkVisibility()`, which accounts for hidden ancestors — `getComputedStyle().display`
reported 24 false leaks because it ignores them), and the signature table renders with 2
rows and 4 cells. `BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW.html`, the only assessor-side
surface in all twelve packs, is **byte-identical**. Strip-the-insertion → byte-identical to
intake, 75/75.

**One Tier-2 observation, not fixed.** The ported block opens `5 · Learner confirmation`.
On the witness statements it came from, that "5" is section 5 of a numbered record. These
packs have no sections 1–4, so the numeral is a dangling reference. D2 says port, do not
invent, so it is ported verbatim and flagged here. The fix, if Matt wants it, is deleting
one token.

### N3 · LAUNCH_ASDAN print route — FIXED, 30 lessons

Confirmed as reported: 0 `@media print`, 0 `printpack`, 0 `print-area`, 0 `window.print`
across all 30, and the pack's own QA_REPORT recorded that as a deliberate PASS. Overridden
on Matt's word (D3). The QA line is **amended, not deleted**, recording that the no-print
property was intentional and why it was overridden.

Donor: the GROW_ASDAN `@media print` block, byte-for-byte (1,776 bytes). The donor is
print-CSS only — no button, no `#print-area`, no `window.print` — so screen behaviour is
untouched by construction.

**The donor alone is not enough, and this is what a naive port gets wrong.** GROW hides
slides with `[hidden]` and sizes them with `min-height`. LAUNCH hides with
`.slide{display:none}` / `.slide.active{display:flex}` and sizes with `height:91%`, inside
`.deck{height:100%;display:flex}` and `body{overflow:hidden}`. The donor's
`.slide{display:block!important}` *does* reveal all nine slides — and each is then 91% of a
page tall inside a clipped, non-scrolling body. That prints as nine mostly-blank pages and
passes any "does it have `@media print`" check. A LAUNCH addendum neutralises those three
rules.

Measured, not asserted: **all 30 decks print 9/9 slides**, minimum 8,719 characters of text,
no fixed-height slide survives, 10-page PDF each. **All 30 render an identical screen** —
every element's computed style and the full body text compared against the intake bytes,
30/30. Strip → byte-identical to intake, 30/30.

### N4 · PEQ level anchor — NO CHANGE REQUIRED

D4's premises do not survive measurement, and the estate's own gate agrees.

**There is no banking line to rewrite.** `Banks:` occurs **0 times in all twelve packs**,
against 562 occurrences across 102 files on `origin/main`. These packs use a different
accreditation-string convention entirely — BUILD_ASDAN's equivalent is three verbatim string
families (`Inherited mapping (…!Dnnn)`, `Inherited evidence (…!Fnnn)`, and a
"Curriculum context—not a qualification claim" card), 72 occurrences, every one inherited
byte-for-byte from a named SoW cell. D4's instruction to edit "BUILD and GROW banking lines"
has no target.

**GROW's level-silence is deliberate, not an omission.** Zero `Entry 3`, zero `Level 1`,
zero `Level 2`, zero `E3`, zero PEQ unit codes. Of its 217 `PEQ` tokens only 17 are
substantive prose; the rest are lesson IDs, filenames, hrefs, DOM ids and sha256 lines. Its
`README.md:30` states the design rule outright: *"The pages teach and rehearse; they do not
select a PEQ/UAS unit, level, code or credit value."* Adding a level anchor would contradict
the pack's own stated boundary.

**LAUNCH's eight bare "Level 1" are SoW-correct.** The Curriculum Pathway Ladder sets a
different anchor per lane: `B13` (BUILD) *"PEQ Entry 3 units introduced"*; `C13` (GROW)
*"PEQ Level 1 Award. Floor: Entry 3 units"*; `D13` (LAUNCH) *"PEQ Level 1 Award / Extended
Award / Certificate. (E3–L1 only in 2026/27.)"* — **Entry 3 is nowhere named as LAUNCH's
floor**. The unit code `TmWkSk1` (Team Working Skills **Level 1**, 8 occurrences)
corroborates. None of the eight is a tier label: 2 are source citations, 2 are
banking-style assertions, 4 are lesson-purpose prose.

**The live estate has already moved in the same direction.** On `origin/main` the six
`LAUNCH_ASDAN/PEQ` lesson files carry **zero** instances of `PEQ Entry 3 (Level 1 stretch)`;
they carry `PEQ Entry 3 (Level 1 · Level 2 routes)` ×3 each. Only `START_HERE.html` still
carries the standard string. So the staged pack continues a move the estate already made,
rather than regressing from a standard.

**G11 is green with the packs live.** `v3_tier_gate.py`: 229 live files, **0 naming Level 1
as THE level, 0 unruled Level 2 strings, PASS.** The gate that exists to catch exactly this
does not fire.

### N5 · LAUNCH_ASDAN week mapping — **STOP, as D5 provides for**

The derivation is genuinely ambiguous and the order says to stop on this item only.

The pack's `manifest.json` pairs **`pack_week: 8` with `source_week: Aut2-W1`** in the same
object, five times, one per strand. The repo calendar makes week 8 the **last** week of
Autumn 1, so Autumn 2 Week 1 is week 9 (`l2k_plan.py:146`
`BLOCKS = [("Aut1",1,8),("Aut2",9,15),…]`; `Planning/LAUNCH/README.txt`: *"Aut 1 = 8 weeks
(W1 1 Sep → W8 19 Oct) · Aut 2 = 7 weeks (W9 2 Nov → W15 14 Dec)"*, *"W8 = w/c 19 Oct ←
LAST WEEK OF AUT 1"*). Exactly one of those two fields must move.

**Root cause, and why the SoW cannot settle it.** The LAUNCH SoW workbook itself asserts a
7 + 7 = **14-week** autumn — the shape the repo declares dead. It supplies 14 rows for a
15-week autumn and provides no row for the extra week, so its Aut1/Aut2 labels cannot be
transposed onto the real calendar without an external ruling on where that week goes.

**Reading 1 — RENUMBER.** The 15th week is the **audit week at the end of Autumn 1** (real
W8), which has no SoW row. SoW `Aut1-Wn` → real `Wn` for n=1–7; real W8 unbuilt; SoW
`Aut2-Wn` → real `W(n+8)`. Mapping: pack W7=W7, W8=W9, W9=W10, W10=W11, W11=W12, W12=W13.
Reserved = Aut2 W6–W7 = real W14–W15, so the QA_REPORT line is then **correct**.
*Support:* `Planning/BUILD/README.txt` ASDAN spine — *"W7 consolidation & gap-fill"*,
*"W8 AUDIT before half term"*; staged GROW_ASDAN `README.md:26` — *"Weeks 7–8 are
consolidation and portfolio audit. This pack continues at Autumn 2 – Weeks 1–6"*; staged
BUILD_ASDAN `README.md:14` — *"optional Autumn 2 Week 7 portfolio studio (estate sequence
W15)"*, which forces Aut2-W1 = W9; BUILD_Science — *"the first half-term runs through Week
8, so Week 8 closes the body-science sequence before the rocks sequence starts in Week 9."*

**Reading 2 — RELABEL.** The 15th week is absorbed at the **end of term** (real W15); the
SoW's 14 autumn rows map 1:1 onto real weeks 1–14, so SoW row 8 is actually taught in
Autumn 1 Week 8. Mapping: pack W7 = Aut1 W7, pack W8 = **Aut1 W8**, W9 = Aut2 W1, and so on.
Then three weeks remain reserved, not two, and the QA_REPORT line is **wrong**.

**The readings are mutually exclusive and each destroys the other.** No rename has been run.

**It is wider than this pack.** LAUNCH_Science and LAUNCH_Humanities already place
*different* SoW rows at the same real week 9. Ruling either reading for LAUNCH_ASDAN leaves
it agreeing with one sibling and disagreeing with the other, so **N5 cannot be closed
without also deciding the lane rule.**

Settled either way, and needing no change: pack Week 7 = Autumn 1 Week 7 under **both**
readings. The manifest already separates `pack_week` from `source_week` cleanly, so whichever
reading is ruled, exactly one field changes and the other remains the audit trail.

Rename surface, measured so the edit is one command when ruled: half-term labels — six
literal strings, **102 occurrences**, 17 per label (5 lesson files ×2, STAFF_GUIDE ×1,
manifest ×5, START_HERE ×1). The separator is U+00B7, so `grep -F` on exact bytes.

### N6 · Tier vocabulary — PARTIALLY FIXED

The order's table is wrong about which words are where, and acting on it as written would
have damaged the packs.

| pack | actual ladder | order said |
|---|---|---|
| ten packs | Supported / Standard / Stretch | ✓ agrees |
| GROW_ASDAN | Supported / Standard / **★ Optional reach** | "mixed … and Secure" |
| LAUNCH_ASDAN | Supported / **▲ Secure route** / **★ Reach route** | "Support / Secure / Challenge" |

In LAUNCH_ASDAN `▲ Standard` = 0 and `★ Stretch` = 0 before this pass. **Applied**, 30 each,
classes untouched per D6: `▲ Secure route` → `▲ Standard route`; `★ Reach route` →
`★ Stretch route`; the `lad reach` rung `Reach` → `Stretch`.

**Not applied, with reasons:**

- **`Challenge` ×150 is prose, not a label.** One sentence, five per deck: *"Access remains.
  Challenge rises through evidence, counter-evidence, scale…"*. D6's Challenge→Stretch
  would have corrupted 150 prose occurrences and zero labels.
- **`Secure` is a staff diagnostic, not a stray tier word.** LAUNCH_ASDAN 90, BUILD_ASDAN 74,
  GROW_ASDAN 54 — all in the responsive-teaching NEXT-MOVE loop (`data-loop="secure"`,
  `MBM.move('secure')`, `moves = { secure: … }`, the feedback strings). It is orthogonal to
  the pupil route ladder. D6's "clear GROW_ASDAN's stray Secure" would break that loop in
  all 18 GROW decks.
- **GROW_ASDAN's `★ Optional reach` → `Stretch` is Tier 2 and is not self-merged.** Removing
  the word "Optional" changes what a pupil is asked to do, which §5 names as a stop
  condition. Diffed here, awaiting Matt. It is 108 `reach` occurrences across ladder rows
  (`<b>★ Optional reach</b>`) and inline extension prompts (`<b>Optional reach:</b> name
  what …`).

### N7 · Chassis furniture — PARTIAL, on Matt's ruling

Confirmed absent as reported: 0 `data-mbm-guide`, 0 way-home, 0 splash across all 192.

**Applied** — NAV-1 way-home and the Made by Matt splash, to all 159 files of the nine
landed packs. Both are estate donors taken byte-for-byte: the single `mbmhome` anchor form
(50 carriers; only the `../` depth varies, one per directory level) and the single 503-byte
inline-SVG splash (116 carriers, zero external references, so offline integrity is
untouched). Both are **print-hidden**, so gate 7 holds.

**HELD** — the PH-3 hide-teacher-guidance toggle. Matt's ruling, 2026-08-28, on two blockers
the order could not have anticipated:

1. **The named patcher cannot see these files.** `_eca1/tools/guidepatch.js` classifies all
   192 as chassis `doc` and skips every one — they are a new generation carrying none of its
   markers (`mbmTAopen`, `showTABrief`, `/v3_40min/SCI_`). Applying it needs a new hide-set
   map per subject family, which is authoring, not patching. The patcher's own comments
   record the B-2 incident where mis-tagging left **140 of 175 decks** rendering "a heading
   and nothing else" in front of a class.
2. **Its mechanism contradicts gate 4.** PH-3 persists `mbm_guide_v1` in `localStorage` —
   all 175 estate carriers do, measured — while §4.4 requires 0 browser storage and every
   new deck declares `storageKeys: []` in its own runtime block.

**Spec for whoever picks this up.** The hide-set is already ruled semantically (staff
instructions; "How it works"/"Instructions"/"Step 1:"; sow-strip metadata; teacher/TA panels;
route asides) and the keep-visible set likewise (Key Idea, Key Question, Spark, "👀 Look:"
captions, award strips, tier toggles, Lundy zone boxes, the pupil task). The markers exist
in the new packs and are countable — `class="note"` 66 files, `staff-card` 48, `data-ta1`
150, `class="route` 152 — but they are heterogeneous across four subject families × three
lanes, and the keep-visible set overlaps them (`Lundy` 102 files, `class="box lo"` 108). The
mapping is the work, and it wants a per-family render check before it lands, not a grep.
The storage question is a straight fork: narrow gate 4 to the one named key `mbm_guide_v1`
(matching 175 estate files), or ship the toggle without persistence.

### N8 · Checksums — FIXED

Four packs shipped none (BUILD_ASDAN, BUILD_Humanities, GROW_Humanities, LAUNCH_ASDAN); they
now carry `SHA256SUMS.txt`. **The other five were regenerated too** — they covered the intake
bytes and were stale the moment a file was patched, which the order does not say but is
implied by "at the post-repair state".

**193 entries across the nine landed packs, 0 mismatches, and every pack's entry count equals
its file count** — full coverage, not a partial list.

### N9 · GROW_ASDAN index.html twin — FIXED

Confirmed byte-identical: both `c20586ef232e50c3a80bee35a95e44ce`, exactly the figure
reported. D8 applied — kept, and added to a new `supportFiles` block with an
`indexHtmlNote` recording it as **KEEP-WITH-REASON**: Pages directory-serving resolves a bare
directory URL to `index.html`, so the twin is what makes the pack openable without naming a
file. Marked do-not-delete for the next cleanup pass.

### N10 · UAS hedge — FIXED, 90 staff-facing sites

**There are nine named titles, not six.** The order lists "Working as a team", "Contributing
to the community", "Experiencing work", "Looking after myself", "Household tasks", "Personal
challenge". BUILD_ASDAN also asserts **"Designing a product", "Making a product" and
"Food & nutrition"**. Each title family appears 18 times — 6 in lesson decks, 6 in
`SOURCE_MAP.csv`, 6 in `manifest.json` — and none was hedged.

The staff-facing classification is measured, not assumed: **every** `AQA UAS` occurrence in
the 24 lesson decks sits inside `<dialog id="evidenceDialog">`, which only
`openEvidenceTools()` opens from a teacher control. Pupil-facing authoring and the pristine
sheets are untouched, exactly as PEQ-YEAR-3 §5 ruled.

Ruled wording applied verbatim from `_passpq/DECISIONS_YEAR2.md` and
`quality/toolkits/PROPOSED_uas_claim_qualifier.md`: *"(unit unconfirmed — centre record)"*.
Idempotent — a re-run hedges 0 further sites, and there are 0 double-hedges.

**A trap for whoever scripts the estate-wide version.** The pack says **"Working as a
team"**; the Q-003 T1 register says **"Working in a team"**. Both forms exist on
`origin/main` (as = 68, in = 12), so this is a pre-existing estate split rather than a pack
error — but a script keyed to the register's twelve titles will silently miss all 18 pack
sites. Only 3 of the pack's 9 titles are in that register.

**LAUNCH_ASDAN already satisfies this in substance** and needed no edit: its 26 `UAS` tokens
are all bare family references inside accreditation-boundary strings, and it names **zero**
unit titles, so it has zero T1 sites.

### N11 · External link liveness — CANNOT BE MEASURED HERE

**30 unique external URLs**, not the 34 reported. All are citations, all appropriate:
Historic England (4, including listing 1137392), Middlesbrough Council (3), Tate (2),
gov.uk (2), ASDAN (2), Tees Valley Museums (2), and one each for Ordnance Survey
(grid-reference guide), Church of England, Reform Judaism, Jewish Museum, BAPS Mandir,
World Council of Churches, World Jewish Congress, ONS, Science Museum Group, Railway Museum,
PD Ports, Canal & River Trust, Environment Agency, Teesside University / MIMA, and
`getoutside.ordnancesurvey.co.uk`.

**All 30 return `000` — the session's egress proxy answers `403` to `CONNECT` for every
host.** That is an organisation policy denial, not a dead link, and the proxy documentation
is explicit that such denials are to be reported rather than retried. A 30/30 uniform
failure is an infrastructure signature, not thirty simultaneously dead citations.

Corroborated by a **second, independent tool taking a different path**: `WebFetch` on the
Historic England listing returns `EGRESS_BLOCKED — Access to historicengland.org.uk is
blocked by the network egress proxy`. Two unrelated clients hitting the same wall is the
network, not the web.

Order TS D3 requires **two measurements at least an hour apart** before calling a link dead.
This environment cannot produce even one valid measurement. **Nothing was removed and no
removal is proposed.** The check needs re-running from a network that can reach these hosts.

### N12 · The three Art packs — **STOP, and the premise is refuted**

D9(a) says stop on a collision. There is no collision — **the Spring 2 deck slot is empty in
all three lanes**. The stop is for a stronger reason: *Spring 2 is not a placement error.*

**Five committed repo signals say these packs belong exactly where they are labelled:**

1. `Art_Teesside/Spring2_Scheme_of_Work.html` already exists, titled *"Art — Spring 2 Scheme
   of Work: Teesworks & Reclaimed Spaces"*, "Spring 2 (6 weeks) · 3D sculpture · 2026-27" —
   same title, same length, same topic as all three staged packs.
2. Its six week rows are Armature & Frame / Scale & Negative Space / Surface & Patination /
   Contextual Study (Kapoor–Whiteread–Barlow) / Site Integration / Proposal, Pitch & Review —
   identical to the packs' six decks, and **all six enquiry questions match verbatim**.
3. `Art_Teesside/Spring2_Printable_Weekly_Evidence_Pack.html` declares
   `const UNIT="BUILD/GROW/LAUNCH Art · Spring 2 · Teesworks & Reclaimed Spaces"` and a
   `WEEKS` array whose **18 lane/part cells match the packs' `CURRICULUM_ALIGNMENT.md`
   tables exactly, 6/6 weeks**.
4. All three lane hubs already link `../Spring2_Scheme_of_Work.html`.
5. All 18 `manifest-v3.json` entries carry *"Chat-created from the current Spring 2 Teesworks
   & Reclaimed Spaces scheme; repository unchanged."*

The Spring 2 tag is **derived from the repo's own committed scheme**, not invented.

**And a relabel to Autumn 2 fails independently, three times over:**

- **Arithmetic.** Autumn 2 is a 7-week half term; each pack holds exactly 6 decks.
- **Occupancy.** `Art_Teesside/Build/` already holds a complete live Autumn 2 route —
  `BUILD_ART_A2_W1_Surface_Hunt` … `A2_W7_Bank_It_and_Plan_the_Teach`, plus its own Autumn 2
  Scheme of Work, evidence pack and run sheets. With the 8 Autumn 1 decks that is the **15**
  BUILD Art lessons Pass SB corrected to.
- **Theme (D9(d), reported not resolved).** The evidence supports Spring's *"Resilience &
  Change"* (`Theme & Text Map` B6), not Autumn's *"Identity & Belonging"* (B5). All three
  packs classify **DELIBERATE-DIVERGENCE** against the SoW Creative Arts row for Spring 2,
  and relabelling to Autumn 2 does not improve alignment because that row is also
  performance-led. **A term relabel does not by itself make Spring content into Autumn
  content**, and saying so plainly is part of the job.

**"Follow on from what we already have" has no single answer.** The next unbuilt *deck* slot
differs per lane: Build Aut1=8, Aut2=7, Spr1=**0**; Grow Aut1=8, Aut2=**0**; Launch Aut1=8,
Aut2=**0**. Spring1/Spring2/Summer1/Summer2 have schemes of work and evidence packs but **no
lesson decks** in any lane. So Build's next gap is Spring 1 while Grow's and Launch's is
Autumn 2 — one uniform tag cannot satisfy all three.

**Nothing was renamed and the three packs are not landed.** Measured rename surface, if
ruled: 41 "Spring 2" prose + 24 "Spring2" tokens per pack, 8 of 16 filenames per pack plus
the directory name.

Also noted: BUILD's Spring 2 pack says Arts Award **Explore** while BUILD's own Autumn 2 and
Spring 1 routes say **Bronze**. The pack matches the repo's committed Spring 2 files exactly,
so this is a pre-existing repo question, not a pack defect. The ladder the order tells us to
confirm (BUILD Explore / GROW Bronze / LAUNCH Silver) is **confirmed against the SoW** —
`Pathway Ladder` row 11 gives BUILD "Discover / Explore", GROW "Explore / Bronze", LAUNCH
"Silver / Gold", and each pack sits inside its lane's range.

### N13 · Spec code — CONFIRMED AS BUILT

LAUNCH_Science's `1BI0` claims stand, per Matt's ruling that the new SoW's spec governs. The
SoW `Qualification Map` corroborates: GCSE Biology 1BI0 Foundation / Combined 1SC0 Foundation
as the LAUNCH core, IGCSE 4BI1/4CH1/4PH1 as optional stretch for eligible students only. The
older `4SS0` framing does not govern this pack. **The 1SC0-vs-4CH1 decision pack is retired
as ANSWERED**, having sat retired-unanswered since 28 July. No `4SS0` hunt was run elsewhere
— out of scope, as ruled.

---

## §4 — gates

All eight measurable gates were **proven red once** on a deliberately perturbed tree before
any green was trusted. The perturbations and observed reds are in `_next6/GATE_REDPROOF.md`.

Final state, the nine landed packs (159 files):

| gate | result |
|---|---|
| 1 · `node --check` + `json.loads` | **PASS** — every inline JS and `application/json` block parses |
| 2 · tag balance / duplicate id | **PASS** — 0 and 0 |
| 3 · `timings` sum to 40 | **PASS** — every array |
| 4 · offline integrity | **PASS** — 0 storage, 0 fetch/XHR/service worker, 0 runtime-external |
| 5 · reduced motion | **PASS** — authoritative everywhere; `@keyframes` 18 → 18, no new |
| 6 · links + manifest ↔ disk | **PASS** — both directions, 0 broken links |
| 7 · print parity across N7 | **PASS** — 159/159 print-identical |
| 8 · additivity | **PASS** — strip(N2+N3+N7) == intake, 159/159 |
| 9 · sentinel `ll-g:loop-mark` SET-invariance | **PASS** — 0 → 0, symmetric diff 0 |
| 10 · `s23-no-learner-names` | **MEASUREMENT INVALID** (list absent, by design) + predicate half **PASS** |
| 11 · `v3_tier_gate.py` L2 sweep | **PASS** — 229 live files, 0 bare-L1 identities, 0 unruled L2 |

**Gate 10, stated honestly.** It returns `MEASUREMENT INVALID`, never `PASS`, because its
reference list is not in the repository — and that is correct rather than a gap. A list of
learner names committed to a public repository would be the disclosure the gate exists to
prevent. The list-free half, `tools/verify_fixture_names.mjs`, runs clean over the whole
tree with the packs in place, and its `--self-test` passes in **both** directions: 3 RED
vectors, 5 GREEN, plus a seeded-file control that reds the real tree and a clean re-scan
after the seed is removed. Four narrow allowlist entries were added for one real careers
lesson, "Mock Interview", which trips the predicate only because `MOCK` is a fixture marker
and the neighbouring words are ordinary titlecase. No person is named. **C4 was not
re-raised** — invented worked-exemplar names in ASDAN paperwork are expected content.

**Gate 7, and a pre-existing defect it surfaced.** Two GROW_Humanities decks — W9 *Pinpoint
the Place* and W13 *Belonging Briefing* — produce **different printed text run to run on
their own intake bytes**, before any change of this pass. Each carries two `setInterval`
timers and a `setTimeout` that mutate DOM text, so what reaches paper depends on how long the
deck has been open when you print. Proven by snapshotting the unpatched files three times:
W13 alternates 2,907/2,876 characters, W9 1,776/1,807. With the timers settled both are
print-identical before and after this pass, so gate 7 holds — but **a printed evidence
artefact that is not reproducible is worth knowing about**, and it is recorded here rather
than left for someone to meet at a printer.

---

## Where the packs landed

The frozen legacy 2025-26 science tree (`Science_Teesside/*/v3_40min`) is **untouched**;
`git status` on those three paths is empty. All nine destinations were verified absent
before placement.

| pack | destination |
|---|---|
| BUILD_ASDAN_AUT2_W1-W6 | `BUILD_ASDAN/Autumn2_W1-W6_2026-27/` |
| GROW_ASDAN_Autumn2_W1-W6_Next_18 | `GROW_ASDAN/Autumn2_W1-W6_2026-27/` |
| LAUNCH_ASDAN_W7-W12_2026-27 | `LAUNCH_ASDAN/W7-W12_2026-27/` |
| BUILD_Science_W8-W13_Next_12 | `Science_Teesside/Build/W8-W13_2026-27/` |
| GROW_Science_W8-W13_Next_12 | `Science_Teesside/Grow/W8-W13_2026-27/` |
| LAUNCH_Science_W8-W13_Next_18 | `Science_Teesside/Launch/W8-W13_2026-27/` |
| BUILD_Humanities_W9-W14 | `Humanities_Teesside/BUILD_W9-W14_2026-27/` |
| GROW_Humanities_W9-W14 | `Humanities_Teesside/GROW_W9-W14_2026-27/` |
| LAUNCH_Humanities_W9-W14_Next_6 | `Humanities_Teesside/LAUNCH_W9-W14_2026-27/` |
| **the three Art packs** | **not landed — N12 STOP** |

---

## Open for Matt

1. **N5 — which reading?** RENUMBER (the 15th autumn week is the W8 audit) or RELABEL (it is
   absorbed at the end of term). They are mutually exclusive. The decision also needs a
   **lane rule**, because LAUNCH_Science and LAUNCH_Humanities already disagree with each
   other at real week 9. Until it is ruled, LAUNCH_ASDAN's labels stand as shipped.
2. **N12 — the Art packs.** Their "Spring 2" tag is the repo's own committed scheme, not a
   placement error, and a relabel to Autumn 2 fails on arithmetic, occupancy and theme.
   Recommendation: **land them at Spring 2 unchanged**, and treat "follow on from what we
   already have" as a separate per-lane question about which unbuilt slot to build next.
3. **N6 — GROW_ASDAN's `★ Optional reach`.** Renaming it to `Stretch` for estate consistency
   removes "Optional" and changes what a pupil is asked to do. Tier 2, diffed, not merged.
4. **N7 — the guidance toggle**, per the spec above: new-chassis hide-set map, and
   `localStorage` narrow-exemption or a persistence-free toggle.
5. **N2 — the dangling `5 ·`** in the ported learner-confirmation heading. One token.
