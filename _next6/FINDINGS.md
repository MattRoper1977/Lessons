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
| **N7** chassis furniture | **PARTIAL** — way-home + splash; toggle HELD, now **mapped and priced** in `_next6/GUIDE_TAG_MAP.md` (N6-I · I5) |
| **N8** checksums | **FIXED** — 193 entries across 9 packs |
| **N9** index.html twin | **FIXED** — KEEP-WITH-REASON |
| **N10** UAS hedge | **FIXED** — 90 staff-facing sites |
| **N11** link liveness | **CANNOT MEASURE HERE** — egress policy; nothing removed |
| **N12** Art placement | **CLOSED — REFUTED** (N6-I · I3, 2026-08-28) — packs stay at Spring 2, D9 withdrawn |
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

### N12 · The three Art packs — **CLOSED — REFUTED** (Order N6-I · I3, 2026-08-28)

> **CLOSED — REFUTED. Matt's ruling of 2026-08-28: land all three Art packs at Spring 2 with
> no relabel, no renames, no manifest or checksum churn. D9 is withdrawn. No later pass
> should reopen this.** All seven signals below were re-verified independently in the N6-I
> session; the evidence and the one thing that could not be executed there (the pack trees
> are not in this repository) are recorded under **ORDER N6-I · I3** at the end of this file.

The original finding, left intact:

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

## §3 — content accuracy

### The named risk — checked hardest, and the packs already guard it

The order names the failure mode this design invites: fixed representative data, with the
"practice" sets liable to be conflated with the investigation sets. **They are not, and the
packs say so themselves.**

`SCI_G_W12A_Science_Connections_Explore.html` carries the practice set and states, verbatim:
*"These practice data are not next week's investigation."* Its worked evidence is
*"smooth 46, 44, 45 cm; fabric 18, 20, 19 cm. Every fabric result is lower."* — recomputed:
every one of 18/19/20 is below every one of 44/45/46. **True.**

`SCI_G_W13B_Rover_Rescue_Investigation_Do.html` carries the investigation set, labelled
*"New investigation evidence"*. Every stated figure recomputed:

| stated in the file | recomputed | verdict |
|---|---|---|
| "Range: 3 cm (48–51 cm interval) … 51 − 48 = 3 cm" | 51 − 48 = 3 | ✓ |
| fabric range 29 − 27 = 2 cm | 29 − 27 = 2 | ✓ |
| "Every smooth result is greater" | min(48,49,51)=48 > max(27,28,29)=29 | ✓ |
| "Typical distance is about 49 cm on smooth and 28 cm" | medians 49 and 28; means 49.33 and 28.0 | ✓ |

Every explicit subtraction across all three science packs was recomputed independently: **4
checked, 4 correct, 0 wrong.**

### Spot-checks confirmed, not re-litigated

Mars 687 Earth days; Earth 365.25 days; Mars red = iron oxide; Saturn's rings ice and rock in
ringlets; mitosis phase evidence (metaphase aligned near the equator, anaphase in groups at
opposite poles); hardness as resistance to scratching with the explicit no-Mohs-number
caveat; the per-100 g label basis; natural vs enhanced greenhouse effect with "greenhouse
gases are not a solid lid"; the rover ranges above; Kapoor void/scale, Whiteread casting
absent space, Barlow everyday materials and precarious scale. All present and correct.

### Protected strings — preserved verbatim

LAUNCH_Science's Foundation-tier discipline is intact and was never a candidate for edit:
*"Do not introduce codominance, sex linkage or Higher-tier drift"*, *"No chi-squared test or
Higher-tier genetics"*, *"Do not add Higher-tier protein synthesis"*. `Art_Teesside` W8's
"Silver" language was not touched and is not re-flagged.

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
| **the three Art packs** | **ruled to Spring 2 (N6-I · I3); not yet landed — the pack trees are not in this repository** |

---

## Open for Matt

1. **N5 — which reading?** RENUMBER (the 15th autumn week is the W8 audit) or RELABEL (it is
   absorbed at the end of term). They are mutually exclusive. The decision also needs a
   **lane rule**, because LAUNCH_Science and LAUNCH_Humanities already disagree with each
   other at real week 9. Until it is ruled, LAUNCH_ASDAN's labels stand as shipped.
2. ~~**N12 — the Art packs.**~~ **RULED AND CLOSED 2026-08-28 (Order N6-I · I3):** land them
   at Spring 2 unchanged, no relabel, no renames, no manifest or checksum churn. D9
   withdrawn. The recommendation below was accepted in full. *"Follow on from what we already
   have" remains a separate per-lane question about which unbuilt slot to build next.*
3. **N6 — GROW_ASDAN's `★ Optional reach`.** Renaming it to `Stretch` for estate consistency
   removes "Optional" and changes what a pupil is asked to do. Tier 2, diffed, not merged.
4. **N7 — the guidance toggle.** The hide-set map the spec above asks for now exists:
   `_next6/GUIDE_TAG_MAP.md` (Order N6-I · I5), with counts, the overlap risk measured in
   the DOM, a worked example and a price. It changes what is being asked for: the **TA
   briefing layer** (1188 strings, 132 decks) is already invisible and needs no toggle,
   while the staff text that *is* on the slides mostly already has a clean selector — ten
   families across the nine packs — with only two families in one pack needing a marker
   authored (51 sites, 26 files). Still needs the `localStorage` ruling.
5. **N2 — the dangling `5 ·`** in the ported learner-confirmation heading. One token.

---
---

# ORDER N6-I — INTERIM FINDINGS

`mbm-next-six-weeks-interim-2026-08-28-N6I` · worked 2026-08-28 · branch
`claude/new-session-q7ztqq`, started from `origin/claude/new-session-llckrn` (`cb8dfaea`)

**On the branch.** The order says continue on `claude/new-session-llckrn`. This session is
issued `claude/new-session-q7ztqq` and may not push anywhere else, so the designated branch
was created **from** `llckrn` and carries all eight of its commits. Nothing is lost and
nothing is forked: `llckrn` is an ancestor of every commit here.

**Coexistence.** `origin` was re-fetched before starting and before each push. The §2
alignment task had not moved `llckrn` at intake, and no file this order touches is a week
label, term tag, LO, success criterion or placement string. Nothing was rebased past and
nothing of that task's was reverted.

---

## I1 — Rendered and counted. Both named defects were already fixed; a third was not.

Not asserted, not grepped, not `checkVisibility()`. Chromium, print media emulation, A4,
`page.pdf()`, then the PDF itself measured: page count, per-page ink coverage on a
rasterised bitmap, and the page's own text layer.

### The population, and why it is derived rather than collected

75 evidence surfaces, derived the way the N2 patcher derives them — every HTML surface in
the three ASDAN packs minus the assessor-side and front-door pages
(`BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW.html`, `START_HERE*.html`, `STAFF_GUIDE.html`,
`index.html`, `PRINTABLE_RESOURCES.html`). BUILD_ASDAN 26 · GROW_ASDAN 19 · LAUNCH_ASDAN
30. That derivation and the set of files carrying the block agree exactly, symmetric
difference **0** — which is the point: the set is not *defined* as "files that carry the
block", because a file that lost it would then silently leave the population.

The 30 LAUNCH_ASDAN decks the order names separately are 30 of those 75, so the render set
is 75 surfaces, not 105.

### The render set is larger than the surface count, and it has to be

BUILD_ASDAN's 24 decks gate their printable pack on `body[data-print-route=…]`: with the
attribute unset, all three `.print-route` blocks are `display:none`. The real pathway is the
deck's own `printSelectedRoute()`, which reads `#printRoute` and calls `window.print()`. So
`window.print` is stubbed, the deck's **own** function is called once per selectable option
(`supported` / `standard` / `stretch` / `all`, with `all` the default), and each resulting
state is rendered. Anything less renders a state no teacher ever prints.

**147 PDFs from 75 surfaces. 812 pages.**

### Assertion 1 — the learner-confirmation block in the rendered print output

**75/75. Zero failures, nothing to name.**

Measured as the four strings of the ported T2-4 block — `Learner confirmation`, `I confirm
this is my own work.`, `Learner name`, `Signature` — appearing in the **text layer of the
produced PDF**. Not the DOM. Not a computed style. The words on the paper.

**N2's defect was already remediated in the seven commits.** The order asks which of the two
were fixed and which were only found: this one was fixed. The previous pass moved the block
inside `<section class="print-pack">` as a final `.print-page`, and this render is the first
evidence that says so from the artefact rather than from the bytes. Its own evidence used
`checkVisibility()`, which is a good proxy and is not the printed page.

### Assertion 2 — blank and near-blank pages

**4 near-blank before · 0 after. Plus 2 more in the reported grey band, also 0 after — so
6 bad sheets, not 4.**

A page is near-blank when it carries essentially no marks **and** essentially no text: ink
coverage below **0.4%** of rasterised pixels *and* fewer than **40** non-whitespace
characters. Both halves are required — a full-page background wash is not text but is not
blank, and white-on-white text has characters but no ink.

**The threshold is not in a clean gap, and saying otherwise would be dishonest.** Sorting all
812 pages by ink shows a continuum at the bottom, not two clusters:

| ink | chars | what it is |
|---:|---:|---|
| 0.061% | 10 | orphaned clause — **fails** |
| 0.129% | 20 | *"and systems, not blame."* — **fails** |
| 0.148% | 23 | orphaned clause — **fails** |
| 0.244% | 38 | orphaned clause — **fails** |
| 0.379% | 61 | orphaned sentence — same defect, **reported not failed** |
| 0.498% | 86 | orphaned sentence — same defect, **reported not failed** |
| *(largest gap in the bottom 40 pages: 0.259%)* | | |
| 0.757% | 76 | **the learner signature page — legitimate**, sparse on purpose |

Ink cannot separate "sparse on purpose" from "sparse by accident", and neither can character
count: the legitimate signature page carries **fewer** characters (76) than an orphan sheet
it must not be confused with (86). So the failing floor sits where a failure is unambiguous,
with nearly a 2× margin to the sparsest legitimate page, and the grey band above it is
**reported** rather than silently passed. Raising the floor to 0.6% would catch those two
extra orphans and would sit 1.26× from the signature page — close enough that a font
substitution on another machine could red a clean tree, and a standing gate that cries wolf
gets switched off.

The sparse report excludes the learner-confirmation page by identifying it from its own
printed text. Without that it listed 101 pages, 99 of them legitimate signature sheets,
which buried the two that mattered.

**This correction came from checking my own threshold rather than from the gate.** The first
version of this section said "4"; the honest number for the defect is 6, of which 4 breach
the floor. The fix cleared all six.

**N3's defect was already remediated too.** All 30 LAUNCH_ASDAN decks print 9 slides plus
the signature page at 10 pages each, no page below 1.5% ink. The nine-blank-pages state does
not exist in the shipped bytes.

**The third defect, which nothing before this render could have found.**

BUILD_ASDAN's print pack defaults to *"All three routes"*. In that state the first
`.print-page` carries the header, the SoW source strings, the objective, three success
criteria, all three route blocks, the independent task and the safety note — more than one
A4 sheet holds. It spilled in all 24 decks. In four of them it spilled by a single clause,
leaving a physical sheet holding ten to thirty-eight characters:

| deck | page 2 ink | page 2 characters | what was on the sheet |
|---|---:|---:|---|
| `…A2_DUKE_W5_Gather_and_Present_Project_Evidence` | 0.061% | 10 | a clause |
| `…A2_COMM_W1_Review_Progress_and_Solve_a_Problem` | 0.129% | 20 | *"and systems, not blame."* |
| `…A2_CON_W5_Record_Process_and_Evaluation` | 0.148% | 23 | a clause |
| `…A2_COMM_W5_Gather_and_Organise_Project_Evidence` | 0.244% | 38 | a clause |
| `…A2_COMM_W4_Take_Responsibility_for_My_Project_Role` | 0.379% | 61 | a sentence — grey band |
| `…A2_PFA_W3_Follow_a_Two_Step_Recipe` | 0.498% | 86 | a sentence — grey band |

A near-blank sheet in the middle of a printed portfolio artefact, on the option a teacher
gets by default. Every element was present, and the element that spilled was *visible*, so
element-presence checks and `checkVisibility()` were both green on all six.

**The fix, chosen by rendering three candidates over all 24 decks rather than by reasoning.**
The smallest one that works, and the only one that changes nothing about what a page shows —
only where the break falls:

```css
@media print{
  .print-page { orphans:4; widows:4 }
  .print-route{ break-inside:avoid; page-break-inside:avoid }
}
```

`widows:4` forbids a break that would leave fewer than four lines of a paragraph at the top
of the next sheet, so a paragraph that cannot satisfy it moves whole. `break-inside:avoid`
on a route block says a route is a unit — a pupil should never meet half of their own route
at a page turn, which is worth having on its own merits.

Measured over all 24 decks in the `route-all` state: **minimum page-2 ink 0.061% → 0.976%**,
sixteen times the gate's floor, and every page 2 now carries a whole paragraph of 159–373
characters instead of an orphaned clause. Total page count is **812 before and 812 after** —
the fix moved a break, it did not add paper.

**A candidate that also worked and was rejected.** Shrinking `.print-pack` to `.92em` and
its padding to 6mm fitted four decks onto three sheets. Reducing type size on an
accessibility-led pupil artefact to win a pagination argument is the wrong trade, and it
changes what a page looks like rather than where it breaks.

**Additivity and screen parity, both proven rather than argued.** The block is confined to
`@media print`, so screen rendering cannot change by construction — and does not: every
element's computed display, visibility, position, colour, background, font-size, box metrics
**and** `orphans`/`widows`/`break-inside`, plus the full `innerText`, hashed before and
after, **24/24 identical**. Strip the marked block → byte-identical to the pre-fix state,
**24/24**. `SHA256SUMS.txt` regenerated for exactly the 24 changed entries; the estate's nine
packs verify **193 entries, 0 mismatches**.

### Assertion 3 — page count per deck, as a table

| pack | print variant | surfaces | units the file declares | pages/deck | lowest page ink, before | lowest page ink, after | near-blank before | near-blank after |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| BUILD_ASDAN | `bare` | 2 | 1 unbanded | 4-5 | 0.757% | 0.757% | 0 | 0 |
| BUILD_ASDAN | `route-all` | 24 | 3 print-page | 4 | 0.061% | 0.764% | 4 | 0 |
| BUILD_ASDAN | `route-standard` | 24 | 3 print-page | 3 | 0.764% | 0.764% | 0 | 0 |
| BUILD_ASDAN | `route-stretch` | 24 | 3 print-page | 3 | 0.764% | 0.764% | 0 | 0 |
| BUILD_ASDAN | `route-supported` | 24 | 3 print-page | 3 | 0.764% | 0.764% | 0 | 0 |
| GROW_ASDAN | `bare` | 18 | 9 slide | 10 | 13.675% | 13.675% | 0 | 0 |
| GROW_ASDAN | `bare` | 1 | 1 unbanded | 11 | 0.802% | 0.802% | 0 | 0 |
| LAUNCH_ASDAN | `bare` | 30 | 9 slide | 10 | 1.513% | 1.513% | 0 | 0 |
| **total** | | **75 surfaces / 147 renders** | | **812 pages** | | | **4** | **0** |

The band each surface is held to is **the one the document declares about itself** — every
`.print-page` inside `.print-pack` that is visible in print media, or, on the deck chassis
that has no print pack, every visible `.slide`. A print stylesheet that puts each unit on
its own sheet cannot honestly produce fewer pages than it has units.

The lowest-ink page in every deck is the final signature page (76 characters, 0.76%–1.5%),
which is what a signature table should look like: mostly white, by design, and two to four
times the gate's floor.

**The 51/75 the order quotes was the pre-remediation figure and is not reproducible now** —
it belongs to the state before the seven commits. What this render reproduces is 75/75.

---

## I2 — `s24-print-renders` is a standing gate, and it has been seen red three times

Registered as **G12** in `_next6/tools/gates.py`, run automatically by
`_next6/tools/run_gates.py` for **every pack that has a print surface**, decided by the pack
itself (`has_print_surface`: any `@media print`, `print-pack` or `#print-area`).

**Wired so print and evidence work cannot ship unmeasured.** A pack that is in scope and
cannot be rendered — no Chromium, no `pypdfium2`, no render set — is reported **FAILED**, not
INVALID-and-ignorable. `N6_SKIP_RENDERS=1` exists for a pack with no print surface and
cannot buy a green for one that has: the scope test runs first. This is deliberately
stricter than the `s23-no-learner-names` contract, where MEASUREMENT INVALID is correct
because the reference list is *withheld on purpose*; here nothing is withheld, so an
unmeasurable print surface is a failure of the run.

**Full battery, all nine landed packs: OVERALL GREEN**, 1113 pages rendered, 0 near-blank,
0 non-G12 regressions. The nine `MEASUREMENT INVALID` lines are G10's, pre-existing and
correct.

**One thing the battery's sparse report surfaced across the wider estate, reported not
failed and not touched by this order.** `Humanities_Teesside/GROW_W9-W14_2026-27/
GROW_HUM_W13_Belonging_Briefing_OUTSTANDING_V3_1.html` prints a page 3 carrying 28
characters at 0.795% ink. That is one of the **two decks the previous pass already recorded
as printing different text run to run** — two `setInterval` timers and a `setTimeout` mutate
DOM text, so what reaches paper depends on how long the deck has been open. The render gate
found it independently, from a different direction, which is a useful corroboration of both
findings. It is out of this order's scope and is left alone.

### Proven red

| # | perturbation | observed red |
|---|---|---|
| **P1** | the learner-confirmation block moved back **outside** `.print-pack` — the shipped N2 defect | `learner-confirmation 25/26`, FAIL, all four route variants of the named file |
| **P2b** | the LAUNCH chassis addendum stripped — the naive donor-only port, the shipped N3 defect | `2 printed pages, expected 9-60 — 9 visible slide unit(s) declared by the document`, **30/30 named**, FAIL |
| **P3** | the block **deleted outright** from one LAUNCH deck | coverage caught it: `ABSENT from print … (declared in the expectation list)`, FAIL |

Plus a `--self-test` that proves the *measurement* in both directions on synthetic pages: a
blank A4 reads 0.0000% ink and is flagged; an inked signature page reads 0.7848% and is not.

### Two things the red-proof itself found, recorded rather than tidied away

**1 · "Restore `height:91%`" does not reproduce the N3 defect, and the first attempt at P2
was correctly GREEN.** The addendum's own `.deck{height:auto!important}` makes a percentage
height resolve to `auto`, so `height:91%` alone is inert. The three neutralisations —
`html,body{overflow:visible;height:auto}`, `.deck{height:auto;display:block}`,
`.slide{height:auto;overflow:visible}` — are load-bearing **as a set**, and only stripping
the whole addendum restores the nine-blank-pages state. Anyone re-running this red-proof from
the order's wording will get a green and should not conclude the gate is broken.

**2 · That green exposed a real gap in the gate and closed it.** The page-count band was
originally a table of per-pack path regexes. The perturbed copy sat at a different path,
matched none of them, fell through to a permissive default of 1–24, and a deck that had
**collapsed from ten printed pages to two** passed as green. A gate whose scope depends on a
directory name goes quiet the moment a tree is copied — which is exactly what a red-proof
does. The band now comes from the document's own declared units and cannot fall through.
This is the second time in two orders that a check was wrong before it was right; the
transferable rule is that **a red-proof is not a formality, it is the test of the gate.**

### Delivery and coverage are two questions and the gate keeps them apart

Conflating them is how the original defect hid.

- **Delivery** — a surface whose source carries `<!--n6-learner-confirm:v1-->` **must print
  it**. Derived from the files, needs no list, and catches the shipped defect exactly.
- **Coverage** — the block must be on every surface that is supposed to have one. This
  *cannot* be derived from the files, because a surface that lost it would stop being asked
  about. It is committed as `_next6/evidence/S24_EVIDENCE_SURFACES.txt`, 75 paths, with the
  derivation rule written into the file. A dropped, renamed or moved evidence surface reds
  the gate against that list instead of going quiet.

The Science and Humanities packs were never specified to carry a learner signature. The gate
does not invent that requirement for them — it reports `DELIVERY ONLY` and still checks them
for blank pages and page count.

### An accessibility render pass, and the hole it found in the gate

Calm Mode and `prefers-reduced-motion` are authoritative on this estate, so a print gate
that only measures the default appearance is half a gate. `s24_render.mjs --a11y` renders
the same 75 surfaces under reduced motion, dark scheme, and the decks' own `.calm` and `.hc`
classes.

**Its first run returned a green on bytes the default pass had just failed.** That is how
the hole was found rather than shipped.

Isolated one mode at a time, the cause is `body.calm{background:#F4F1E9}`. It sits outside
`@media print` and **outranks** the print block's `body{background:#fff}` on specificity, so
the cream survives into print. With background graphics on, every sheet carries a full-page
wash — 84.3% of pixels are then "not white", and a sheet holding an orphaned twenty-character
clause measures as densely inked. The ink floor could never fire.

**Fixed by measuring twice.** `ink` stays coverage-against-white — the order's own wording,
and the right number for an ordinary sheet. `edge` is added: the share of pixels where the
image changes against its neighbour, so a flat region contributes nothing *whatever its
colour*. Over the corpus it separates the same way and keeps separating when ink cannot:

| | edge |
|---|---:|
| the four orphan sheets | 0.085% · 0.182% · 0.527% · 0.700% |
| the legitimate signature page | **1.258%** — 1.8× the worst orphan |
| ordinary content pages | 6.4% · 12.7% |

A page is near-blank when it is text-poor **and** *either* measurement is under its floor.
Requiring both would let a themed background veto the check.

A modal-background version of `ink` was tried first and rejected on measurement, not taste:
a BUILD_ASDAN sheet under Calm Mode has **two** large flat regions — the cream body and the
white print-page — so "differs from the commonest value" counts the entire print-page as
marks and reports 16–26%.

| | near-blank | sparse | verdict |
|---|---:|---:|---|
| a11y pass, pre-fix bytes, before this correction | 0 | 0 | **hollow green** |
| a11y pass, pre-fix bytes, after it | 3 | 3 | FAIL |
| a11y pass, post-fix bytes | 0 | 0 | PASS |
| default pass, pre-fix / post-fix | 4 → 0 | 2 → 0 | FAIL → PASS |

Both modes now agree the defect was **six** sheets, and both agree it is gone.

### The Calm Mode print tint itself — reported, not fixed

**With background graphics OFF, which is Chrome's default and what a teacher gets unless
they tick the box, the Calm Mode output is identical to baseline** — ink
10.7 / 1.1 / 4.7 / 0.8%, edge 12.70 / 1.50 / 6.43 / 1.26%, the same numbers to three
decimal places. Nobody meets this by accident.

It is confined to the 24 BUILD_ASDAN decks: 27 files estate-wide carry
`body.calm{background:…}`, 24 of them also try `body{background:#fff}` inside `@media print`,
and all 24 are these. It is a specificity-convention question of exactly the kind
`CLAUDE.md` already rules on for themes under `.hc` — *"A theme stands down entirely under
`.hc` rather than beating it on inline-style specificity"* — so it wants one estate-wide
decision, not a patch to 24 files for a mode no default user reaches. **Left for a ruling.**

What *was* fixed is the instrument: a hole in a gate I wrote is mine to close, and a green
that only holds in one display mode is not a green.

### Determinism, checked — because a gate that varies run to run is worse than none

The whole 75-surface set was rendered twice from identical bytes and the two runs compared
two ways:

- **byte-identical PDFs: 0 of 147.** A PDF carries a creation timestamp and a document ID,
  so hashing the file always differs. Anyone building a print gate on `sha256` of the PDF
  gets a check that fails on every run and will end up disabling it.
- **measurement differences: 0.** Every page count, every ink coverage to 1e-6, every
  character count reproduced exactly across all 812 pages.

That is the estate's own rule about proxies, met from the other side: the obvious artefact
comparison is the broken one, and the derived measurement is the sound one.

### The tools

| file | what it is |
|---|---|
| `_next6/tools/s24_render.mjs` | the render half — Chromium, print emulation, A4, per-route variants, `--a11y`, records what each file declares it will print |
| `_next6/tools/s24_print_renders.py` | the measure half — ink coverage, tint-invariant edge coverage, text layer, page counts, `--self-test`, `--packs`, `--expect` |
| `_next6/tools/i1_print_pagination.py` | the pagination fix; idempotent, markered, strip-reversible |
| `_next6/tools/i1_screen_parity.mjs` | the screen-parity witness for a print-only change |
| `_next6/evidence/S24_EVIDENCE_SURFACES.txt` | the committed coverage contract, 75 surfaces |

Dependencies: `pypdfium2` and `numpy` for rasterising and pixel arithmetic, `playwright` +
the repo's Chromium for the render. Absent, the gate says MEASUREMENT INVALID and never
PASS — and, for a pack with a print surface, that is escalated to a failure.

---

## I3 — N12 CLOSED — REFUTED. The Art packs stay at Spring 2.

**Matt's ruling of 2026-08-28 is recorded: the three Art packs land at Spring 2 with no
relabel, no renames, no manifest or checksum churn. D9 is withdrawn. This item is closed and
no later pass should reopen it.**

Every signal that carried the refutation is re-verified in this session, independently of
the previous pass's report:

| # | signal | verified now |
|---|---|---|
| 1 | `Art_Teesside/Spring2_Scheme_of_Work.html` exists | yes — `<title>` *"Art — Spring 2 Scheme of Work: Teesworks & Reclaimed Spaces"*, subtitle *"Spring 2 (6 weeks) · 3D sculpture · 2026–27"* |
| 2 | six week rows, same as the packs | yes — Armature & Frame · Scale & Negative Space · Surface & Patination · Contextual Study (Kapoor, Whiteread, Barlow) · Site Integration · Proposal, Pitch & Review |
| 3 | six enquiry questions, verbatim | yes — all six extracted, e.g. W1 *"What makes a structure stand up — and still let you change your mind?"*, W6 *"Why this, why there, and what does it ask people to notice?"* |
| 4 | the evidence pack declares the same unit | yes — `Spring2_Printable_Weekly_Evidence_Pack.html` carries `const UNIT="BUILD/GROW/LAUNCH Art · Spring 2 · Teesworks & Reclaimed Spaces"` and a `WEEKS` array whose lane/part cells (`"Explore A · Bronze A · Silver 1A"`, …) are the packs' three-lane mapping |
| 5 | all three lane hubs already link it | yes — `Art_Teesside/{Build,Grow,Launch}/START_HERE.html` |
| 6 | the Spring 2 **deck** slot is empty in all three lanes | yes — no Spring 2 lesson deck exists anywhere in `Art_Teesside/` |
| 7 | Autumn 2 is occupied, so a relabel had nowhere to go | yes — `Art_Teesside/Build/` holds `BUILD_ART_A2_W1…A2_W7` plus its own Autumn 2 scheme, evidence pack and run sheets |

The Spring 2 tag was derived from the repo's own committed scheme. The ruling matches the
evidence.

### What could not be executed here, stated plainly

**The three Art pack trees are not in this repository or this session.** They were an intake
tree in the previous session and that tree is gone; `find` over the whole filesystem returns
nothing for `*Art_Spring2*`, `BUILD_Art*`, `GROW_Art*` or `LAUNCH_Art*`, and no commit on any
branch ever added them. So the **ruling is recorded and the placement is settled, but the
landing itself cannot be performed in this venue** — there are no pack bytes to place.

This is the one item of this order that is complete as a decision and incomplete as an
action. It needs a session that has the three pack trees. Nothing else is blocking: the
destination is empty, the ruling is unambiguous, and the instruction is "no relabel, no
renames, no manifest or checksum churn", so it is a copy and a checksum generation, not
authoring.

---

## I4 — CANNOT MEASURE HERE. One line, as instructed.

**This venue still cannot reach the network: 26 unique citation URLs, all 26 return `000`,
while the allowlisted control hosts answer `200` in the same run — an egress policy
signature, not 26 simultaneously dead links. Item stopped, nothing simulated, nothing
proposed for removal.**

The reading is committed anyway, as a timestamped artifact, because the *attempt* is the
evidence that the clock has not started:
`_next6/evidence/I4_link_liveness_reading1.json` — taken `2026-08-28T14:16:54Z`, 26 URLs
across 19 hosts, every carrier file recorded, `"valid": false`, controls `pypi.org` 200 and
`registry.npmjs.org` 200. `_next6/tools/i4_link_liveness.py` refuses to record a liveness
result when every citation host fails and a control answers; it is that discrimination, not
the count, that makes a second reading meaningful when one is possible.

**On the count.** The order says 34 unique URLs and the previous pass measured 30. This pass
measures **26** across the nine landed packs — the difference is the three Art packs, which
are not in this repository, so their citations are not in this inventory. The figure is not a
correction of 30; it is a smaller population.

Order TS D3's second reading, at least an hour later, has not been attempted: a second
invalid measurement is not a second measurement.

---

## I5 — Guidance toggle: mapped, priced, nothing applied

Full map in [`_next6/GUIDE_TAG_MAP.md`](GUIDE_TAG_MAP.md). **Nothing was applied and nothing
was patched**, as the order requires.

**A correction first, because an earlier version of this section said the opposite.** My
first probe looked for a chosen list of *string families* — SoW cell references,
`Exact SOW outcome`, `Estate sequence`, `AQA UAS` — and concluded that eight of the nine
packs put no staff-facing text on screen at all. **That was wrong.** A string-family probe
finds the families it was handed. Re-probing by **addressee** — who is the sentence talking
to? — finds staff-facing content visible in **all nine packs**. The error surfaced from an
adversarial pass over nine independently-produced per-pack maps, which is what that pass was
for, and it is recorded rather than overwritten because the method that produced it is the
method a future pass will reach for first.

### What is true

**1 · The TA briefing layer is already invisible, and it is the bulk of the guidance.** 132
of the 159 files carry `data-ta1`/`data-ta2` briefing strings — **1188** of them — and
**zero** reach the pupil-facing surface. Four container families, disjoint, exactly one per
lesson deck, none visible at load:

| container | packs | in the DOM |
|---|---|---|
| `#teacherDialog` | BUILD_ASDAN 24 | `<dialog role="dialog" aria-modal="true">` |
| `#taOverlay` | GROW_ASDAN 18, LAUNCH_Humanities 6 | `<div class="overlay" aria-hidden="true">` |
| `#taDialog` | LAUNCH_ASDAN 30, Science 12+12+18, BUILD_Humanities 6 | hidden/modal; in Science a `<dialog data-audience="staff">` |
| `#tool-ta` | GROW_Humanities 6 | a `role="tabpanel"` in a tools drawer |

24 + 24 + 78 + 6 = 132. For that layer, PH-3's purpose is already achieved by the chassis,
and the prompt ladders, adult-action notes and teacher-tool drawers are hidden too.

**2 · But staff-facing text on the slides themselves exists in every pack**, and it is a
different thing from the briefing layer. Files where the family is visible across all slides:

| pack | visible staff-facing families |
|---|---|
| BUILD_ASDAN | SoW ref 28 · `Exact SOW outcome` 25 · `Estate sequence` 26 · staff addressed 24 · adult prompting 25 · delivery routine 24 |
| GROW_ASDAN | staff addressed **19** · delivery routine **19** · adult prompting 7 |
| LAUNCH_ASDAN | `AQA UAS` 13 · staff addressed **30** · delivery routine **30** |
| BUILD / GROW / LAUNCH Science | `Sequence outcome:` **12 / 12 / 18** |
| BUILD_Humanities | staff addressed **6** |
| GROW_Humanities | SoW ref 2 · staff addressed 3 · delivery routine 1 |
| LAUNCH_Humanities | adult prompting 1 |

**3 · Most of it already has a dedicated selector.** Ten families are clean, purpose-built
and exist today — each read in a browser to confirm what the whole block says, because
machine matching proposes and reading disposes:

| selector | packs | what it says |
|---|---|---|
| `.choose` | GROW_ASDAN 18 | *"Staff: select one route before giving this page to the learner. Change access, not authorship."* |
| `.staff` | GROW_ASDAN 18 | *"Staff pre-stage before the 16-minute transfer…"* |
| `.guard` · `.evidence-note` · `.boundary` | GROW_ASDAN 18 each | qualification boundary, evidence boundary, use-note |
| `.screen` | LAUNCH_ASDAN 30 | *"Authorship check: Staff may model the process and preserve access…"* |
| `.reportback` | BUILD_Humanities 6 | *"Named-adult report-back · Decision maker: Class teacher — replace with the adult's name before delivery."* |
| `.lnote` | Humanities ×3 | the Lundy staff notes |
| `.sowline` | Science ×3, 12/12/18 | *"Sequence outcome: Rocks: test hardness."* |
| `.lesson-link` · `.small` | BUILD_ASDAN 24 each | the SoW cell reference and estate sequence |

**Four more BUILD_ASDAN families are reachable by label- or position-keying**, which is the
`STAFF_LABELS` mechanism `guidepatch.js` already implements — not by authoring anything:

| selector | staff share | verified |
|---|---|---|
| `.chips .chip:last-child` | 24 of 96 chips | it is the `Estate sequence` chip in **24/24** decks |
| `.box.objective` keyed on its `<strong>` label | 72 of 96 | exactly 24 each of `SPACE routine`, `Model aloud:`, `Connect:` — the fourth is the pupil's `Learning objective:` |
| `.box.good` keyed on its label | 48 of 96 | `Authorship check:` and `Adult close` staff; `Success criteria` pupil; `Potential evidence: assessor review required` assessor |
| `.box.rehearsal` keyed on its text | 24 of 120 | only *"Do not reveal the pupil's whole answer…"*; the other 96 are pupil-protective |

**So exactly one family in one pack needs a marker authored**: BUILD_ASDAN's `Exact SOW
outcome` paragraph, unclassed inside `.hero`, **25 files**. The job is almost entirely
mappable.

**And one selector that must NOT be tagged, measured rather than assumed.** `.model-step`,
144 instances, reads exactly like step-by-step delivery instruction and any "Step" or "How
it works" rule catches it — but it is **49–58% of its slide's text** on slides 4 and 6, so
hiding it halves two slides per deck. That is the shape of the 140-of-175 incident the
patcher's own comments record.

**Route labels are pupil-facing and stay** — visible 19/19 in GROW_ASDAN and 30/30 in
LAUNCH_ASDAN. Reading "route metadata" as a hide target, which the order's wording invites,
would take the pupil's own access route off the screen. GROW_ASDAN's `.soft` looks
staff-facing to a keyword probe and is not: *"Standard: add a reason or example. Optional
reach: name what evidence could change your first answer."*

**`data-ta1`/`data-ta2` are attributes, not elements.** No CSS selector can hide an
attribute — only the container that renders it. The guidance payload and the thing a
selector can target are different objects on this chassis.

### Cost

| work | scope | estimate |
|---|---|---|
| tag the ten clean selector families | the classes exist and are clean | a selector list plus the toggle |
| label- and position-key four BUILD_ASDAN families | selectors that already exist | a selector list |
| author markers for the residue | **25 sites, 25 files, BUILD_ASDAN only** | an hour or two with the checks |
| render / visibility check per family per lane | already built and running | ~5 minutes per run |
| the `localStorage` question | a ruling, not engineering | narrow gate 4 to `mbm_guide_v1`, or ship without persistence |
| regression | ~40 of 159 files, additive and strip-reversible | low |

**What a toggle would remove that is worth removing:** GROW_ASDAN's staff route-selection
instruction, LAUNCH_ASDAN's authorship check, and BUILD_Humanities' *"Decision maker: Class
teacher — replace with the adult's name before delivery"* — an unfinished instruction to the
teacher, sitting on the wall. **What is more arguable:** the SoW audit trail, which a teacher
can read without opening anything. **What needs no toggle at all:** the 1188-string briefing
layer, which is already invisible.

**Two probe artefacts recorded so a later pass does not chase them.** `.enhanced` in the
Science packs appears in the candidate list because its element is a `<style>` block whose
CSS text the probe read as content. And an earlier case-sensitive run of the overlap probe
reported `.small` as mixed with ten pupil-facing instances; all ten were staff strings missed
on a lower-case `e`. A probe case-sensitive about prose invents overlap.

**Not priced: the three Art packs**, which are not in this repository. Labelled unpriced
rather than extrapolated.

---

## I6 — **CLOSED — PREMISE REFUTED** (Order N6-Z · Z6, 2026-08-28)

> **CLOSED — PREMISE REFUTED.** "D13 contradicts the estate anchor" was a misreading of a
> **target** cell as a **floor**. Four measurements, each reproducible:
>
> 1. The LAUNCH column states a floor for **0 of its 13 subjects** — not English, not maths,
>    not science. BUILD states one in 10 of 13, GROW in 13 of 13. The missing "Floor:" in
>    `D13` is a column-wide layout convention, not a ruling about PEQ.
> 2. The ladder says what it is. `A2`, verbatim: *"Each cell shows the pathway's **TARGET**
>    and, **where relevant**, the FLOOR for the lowest learners so no one is stranded."*
> 3. `D13` is **byte-identical** (sha256 `f9c416e890fdc52f…`) in all three committed
>    workbooks, so it is shared front-matter, not a statement about the LAUNCH cohort.
> 4. Of the **29** cells in the LAUNCH workbook that name PEQ with a level, **28 name Entry
>    3**. The one exception, `Qualification Map!E15`, is the **GROW** column.
>
> The workbook does not claim LAUNCH excludes Entry 3. **No later pass should reopen this.**
>
> **One live item survives, as a question and not a defect:** `_passsl/` — the pass that
> ingested the LAUNCH SoW — carries **no level statement at all** across its five `.md`
> files, so nobody has ruled on this on the record. That is a one-line confirmation for
> Matt and Cheryl, not work.

The original write-up, left intact:

## I6 — The accreditation contradiction, as first recorded

**For Matt and Cheryl.** Nothing is edited for this. No pack, no deck, no string. It is a
scheme-level question and the ruling is theirs.

**But the premise does not survive measurement, and saying so is part of the job.** The
order states that `D13` gives LAUNCH *"PEQ Level 1 Award" with no Entry 3 floor* and that
both sources cannot be right about LAUNCH. Measured against the workbooks, the disagreement
is much narrower than that, and may not be a disagreement at all. The evidence is below;
the ruling is still theirs to make.

### Source A — the SoW Curriculum Pathway Ladder

`_passsl/inputs/LAUNCH KS4 - 2026-27.xlsx`, sheet **`Pathway Ladder`**, row 13
(`A13` = *"Personal Effectiveness (ASDAN PEQ)"*), column header `D3` = *"LAUNCH (GCSE)"*.
Verbatim, with its two row-mates, because the comparison is the whole point:

> **`B13`** (BUILD) — *"PEQ Entry 3 units introduced. **Floor:** introductory/taster units."*
> **`C13`** (GROW) — *"PEQ Level 1 Award. **Floor: Entry 3 units.** (E3–L1 only in 2026/27.)"*
> **`D13`** (LAUNCH) — *"PEQ Level 1 Award / Extended Award / Certificate. (E3–L1 only in 2026/27.)"*

### Source B — the merged estate anchor

`_passpq/DECISIONS.md` §0, quoting the owner:

> *"The owner stated, 2026-08-20: pupils are mainly ENTRY LEVEL (Entry 3). Only 2–4 pupils
> are at Level 1. Nobody is at Level 2."*

and §2, family E1, recording what was done with it:

> *"`PEQ Level 1 (E3 floor · L2 stretch)` → `PEQ Entry 3 (Level 1 stretch)` … 195
> substitutions over 20 files + an 8-file tail sweep"*

| tier | evidences | was |
|---|---|---|
| Supported | **Entry 3** | Level 1 |
| Standard | **Entry 3** | Level 1 |
| Stretch | **Level 1** | Level 2 |

### Five measurements that narrow the question

**1 · The missing "Floor:" is a column-wide layout convention, not a LAUNCH ruling.**
Counted across the ladder's 13 subject rows:

| column | cells containing "Floor" |
|---|---:|
| B — BUILD | **10 of 13** |
| C — GROW | **13 of 13** |
| D — LAUNCH | **0 of 13** |

The LAUNCH column never states a floor for **any** subject — not English, not maths, not
science, not RE. Reading `D13`'s silence as an accreditation ruling requires reading the
same silence as a ruling in twelve other subjects too.

**2 · The sheet says outright what it is.** `A2`, verbatim:

> *"Each cell shows the pathway's **TARGET** and, **where relevant**, the FLOOR for the
> lowest learners so no one is stranded."*

So the ladder is a table of targets with an *optional* floor clause. That is the workbook's
own description of itself, and it answers the question of whether the ladder is a target
statement or a delivery statement without anyone having to infer it.

**3 · `D13` is not a LAUNCH-authored statement.** The cell is **byte-identical**
(sha256 `f9c416e890fdc52f…`) in all three committed workbooks —
`_passsl/inputs/LAUNCH KS4 - 2026-27.xlsx`, `_passsb/inputs/Build SOW 2026-2027.xlsx` and
`_passsg/inputs/GROW SOW 2026-27.xlsx`. The Pathway Ladder is shared front-matter carried in
every workbook, so `D13` is not a statement made about the LAUNCH cohort in particular.

**4 · The same workbook names Entry 3 for LAUNCH 28 times.** Of the **29** cells in the
LAUNCH workbook that name PEQ with a level, **28 mention Entry 3 or E3**. The single
exception is `Qualification Map!E15` — which is the **GROW** column. The LAUNCH cell in that
same row, `F15`, reads *"PEQ Level 1 Award / Extended Award / Certificate (E3–L1 only in
2026/27)"*, and the row's own summary `C15` is *"E3 to L1"*. `B15` states it plainly:

> *"ASDAN Personal Effectiveness Qualification (PEQ), **Entry 3 and Level 1** (Award /
> Extended Award / Certificate) – delivered at **E3–L1 only in 2026/27**; Levels 2–3 to be
> introduced in future years."*

**5 · `D13` is not silent about Entry 3 in the first place.** It carries
**"(E3–L1 only in 2026/27.)"**. What it lacks against `C13` is the literal word "Floor:" —
which, per measurement 1, no LAUNCH cell has for any subject.

**Taken together: the workbook does not claim that LAUNCH excludes Entry 3.** It claims
Level 1 is the LAUNCH *target* and states an E3–L1 range for the year. The estate anchor
claims Entry 3 is what the room *evidences today*, with Level 1 as stretch. Those are
answers to different questions, and the estate has already said so in terms —
`_passpq/DECISIONS.md` §1: the earlier "L1 primary" framing *"is superseded **for delivery
purposes**"*, its arithmetic *"still correct"*, the L1 routes *"re-labelled as the stretch
route … not deleted"*.

### The anchor string, counted here

The order gives ×118. Measured at `db066603` with a clean tree:

```
grep -roF "PEQ Entry 3 (Level 1 stretch)" . --exclude-dir=.git --exclude-dir=node_modules  # 139
grep -rlF "PEQ Entry 3 (Level 1 stretch)" . --exclude-dir=.git --exclude-dir=node_modules  # 38
```

**139 across 38 files**, of which **3 occurrences are this document's own quotations** — a
write-up that cites a string inflates the count of it, so the estate figure to work from is
**126 across 33 live-content files** (working directories and root ledgers excluded).
`origin/main` is 136 across 37.

| area | files | occurrences |
|---|---:|---:|
| `GROW_ASDAN/` (hub, PEQ W1–W6, START_HERE, resources) | 10 | 25 |
| `GROW_Estate_v3/GROW_ASDAN/` | 9 | 44 |
| `LAUNCH_ASDAN/` (hub, PEQ START_HERE, resources, scheme) | 4 | 5 |
| `LAUNCH_Estate_v3/LAUNCH_ASDAN/` | 9 | 31 |
| `resources.json` — 13 LAUNCH records, 8 GROW, by record id | 1 | 21 |
| **total** | **33** | **126** |

**None of the 126 is in the three new packs.** `LAUNCH_ASDAN/W7-W12_2026-27/` and
`GROW_ASDAN/Autumn2_W1-W6_2026-27/` carry the string **0 times**. This is a question about
the pre-existing estate, which is why nothing here is edited.

### The arithmetic consequence of each reading

**Reading 1 — `D13` governs; LAUNCH is a Level 1 lane.** In scope is only what `D13`'s own
column covers: **49 occurrences across 14 files** — 36 in the 13 LAUNCH-path files, plus the
13 `resources.json` records whose ids begin `launch-asdan-`. The GROW side is untouched —
**69 across 19 pack and estate files, plus the 8 GROW `resources.json` records, so 77 across
20** — because `C13` gives GROW an explicit Entry 3 floor and the anchor agrees with it
there. The cost is not the substitution. It is that the estate would then name Level 1 as
the level for a room in which, on the owner's own statement, **2–4 pupils are at Level 1 and
the rest are at Entry 3** — and everything `_passpq` moved down would be pointing above the
room again: 34 tier-minimum substitutions over 4 decks, 53 command-verb stems over 11 decks,
8 arithmetic panels.

**Reading 2 — the estate anchor governs; LAUNCH delivers at Entry 3 with Level 1 stretch.**
No file changes; the 126 stand. What is contradicted is the workbook's headline *target* for
the lane. Against it: the staged LAUNCH pack asserts a bare **"Level 1"** 8 times and carries
the unit code `TmWkSk1` (Team Working Skills Level 1) 8 times, and in `LAUNCH_ASDAN/` the
Level 1 codes dominate — `ComSk1` 87 against `ComSkE3` 64, `TmWkSk1` 12 against `TmWkSkE3`
**0**, while `GROW_ASDAN/` carries `TmWkSkE3` 77 times.

### What genuinely cannot be settled from the repository

1. **No one has ever chosen between them on the record.** `_passsl/` — the pass that ingested
   the LAUNCH SoW — contains **no level statement at all**: its five `.md` files carry zero
   occurrences of "Entry 3", "Level 1" or "E3–L1". The ladder entered the repository as raw
   input evidence and was never adjudicated. `_passpq/DECISIONS.md` §1 supersedes an internal
   audit "for delivery only"; the **workbook** is nowhere named as superseded.
2. **The per-pupil split is not in the repository.** The cohort fact gives a range
   ("2–4 pupils"), not a roll, and no file records which pupils were entered at which level
   for which skill. So nobody working from these files can say how many pupils either reading
   would move, or whether the entries already made match either one. That is a question for
   the coordinator and the ASDAN account.
3. **What `D13`'s parenthetical was for.** *"(E3–L1 only in 2026/27.)"* could be a floor
   statement (Entry 3 is available in this lane this year) or a suite-availability note (the
   centre offers only E3 and L1 school-wide this year, Levels 2–3 later — which is how
   `Qualification Map` B15 and `Programmes & Frameworks` B23 both phrase it). It appears
   identically in `C13`, *alongside* an explicit "Floor: Entry 3 units", which suggests it is
   not itself a floor clause — but that is an inference, not a record.
4. **A third string already disagrees with both.** The six live `LAUNCH_ASDAN/PEQ` decks
   carry neither: they carry `PEQ Entry 3 (Level 1 · Level 2 routes)`, **18 occurrences
   across those 6 files** (23 repo-wide including tooling). It arrived on a later owner
   ruling — `_passpq/CREDIT_PATHWAYS.md:181`, 2026-08-21, adding an in-deck Level 2 route —
   one day after the anchor was adopted. Whichever way this is ruled, that third form needs
   ruling with it, or the estate will name two things for the same weeks, which is exactly
   the failure `_passpq` P1 was opened to fix.

### What is actually being asked

1. Is the Pathway Ladder a **target** table? Its own `A2` says yes. If that is accepted, the
   contradiction dissolves and the answer should be written into the workbook so no later
   pass re-derives it.
2. If it is not, for LAUNCH in 2026/27 is the **default** Entry 3 with Level 1 as stretch, or
   Level 1 with Entry 3 admitted?
3. Either way: what happens to `PEQ Entry 3 (Level 1 · Level 2 routes)`, 18 occurrences
   across the 6 live LAUNCH PEQ decks, which agrees with neither?

---

## Outcomes — I1 to I6

| item | outcome |
|---|---|
| **I1** prove the two print defects | **DONE — both were already fixed; a third was found and fixed.** 75/75 learner confirmation in the printed text; near-blank pages 6 → 0; 812 pages tabulated |
| **I2** make the render gate permanent | **DONE.** `s24-print-renders` is G12, runs for every pack with a print surface, red-proved three ways, full battery GREEN |
| **I3** close N12 | **CLOSED — REFUTED.** Ruling recorded, all seven signals re-verified. **The landing itself could not be performed here — the pack bytes are not in this repository** |
| **I4** start the external-link clock | **CANNOT MEASURE HERE.** Stopped after one line, as instructed. Timestamped artifact committed; nothing proposed for removal |
| **I5** guidance tag map | **DONE — map only, nothing applied.** `_next6/GUIDE_TAG_MAP.md`. Ten clean selector families already exist; the residue needing an authored marker is 51 sites in one pack. **Corrected once:** my first probe was keyed to string families and wrongly reported eight of nine packs as having no visible staff text |
| **I6** record the accreditation contradiction | **CLOSED — PREMISE REFUTED** (N6-Z · Z6). Originally: **recorded, not resolved.** Both sources quoted, both readings costed. **The premise does not survive measurement:** the ladder's own `A2` calls it a TARGET table, no LAUNCH cell states a floor for any of its 13 subjects, `D13` is byte-identical in all three workbooks, and 28 of the LAUNCH workbook's 29 PEQ-with-level cells name Entry 3 |

## What this order's instruments got wrong before they got it right

Three of my own checks were wrong first. Each is recorded so the next pass does not
re-derive it, and each was caught by a red-proof or by checking the instrument against its
own output rather than by luck.

1. **A gate scoped by directory name goes quiet when a tree is copied.** The page-count band
   was a table of per-pack path regexes; a perturbed copy at a different path fell through
   to a permissive default and passed a deck that had collapsed from ten printed pages to
   two. The band now comes from the document's own declared print units.
2. **A threshold placed without looking at its own distribution hides what it was built to
   catch.** The bottom of the ink distribution is a continuum. Two more orphan sheets sat
   above the floor, so the honest count is six, not four.
3. **A pixel check can be silenced by a background colour.** Calm Mode's cream survives into
   print on specificity; every pixel is then non-white and the ink floor can never fire. The
   accessibility pass returned a green on bytes the default pass had just failed. Closed with
   a tint-invariant edge measure.
4. **A probe that is case-sensitive about prose invents overlap.** The I5 overlap run
   reported `.small` as a mixed class carrying ten pupil-facing instances; all ten were staff
   strings missed on a lower-case `e`. `.small` is in fact clean, which is the opposite
   conclusion.
5. **A probe keyed to string families finds the families it was handed, and nothing else.**
   My first I5 measurement asked for SoW-provenance phrases and concluded that eight of the
   nine packs put no staff-facing text on screen. Re-keying it to **addressee** — who is the
   sentence talking to? — found staff-facing content visible in all nine, including
   GROW_ASDAN's *"Staff: select one route before giving this page to the learner"* and
   BUILD_Humanities' *"Decision maker: Class teacher — replace with the adult's name before
   delivery"*. It surfaced from an adversarial pass over nine independently-produced per-pack
   maps, seven of which were themselves PARTIAL on verification — the cross-check earned its
   keep in both directions.

And one about the artefact rather than the instrument:

6. **Comparing the artefact is the broken assertion; comparing the measurement is the sound
   one.** Rendered twice from identical bytes: **0 of 147** PDFs byte-identical, because a
   PDF carries a creation timestamp — and **0** measurement differences across all 812 pages.

## Still open

Carried forward from N6 and untouched here: the **N5** reading and its lane rule; GROW_ASDAN's
`★ Optional reach` → `Stretch` (Tier 2); the **N7** toggle, now mapped and priced by I5 but
still unruled; and the dangling `5 ·` in the ported learner-confirmation heading.

New from this order:

1. **I3's landing.** The ruling is settled; the three Art pack trees are not in this
   repository, so a session that has them must perform the copy.
2. **I4's clock.** Not started. It needs a venue that can reach the citation hosts.
3. **I6 — the LAUNCH accreditation question**, for Matt and Cheryl, with both readings
   costed above. The question is narrower than the order frames it: the Pathway Ladder says
   of itself that it shows the **target** with an optional floor, the LAUNCH column states a
   floor for **0 of its 13 subjects**, and the LAUNCH workbook names Entry 3 in **28 of the
   29** cells where it gives PEQ a level. If the ladder is accepted as a target table the
   contradiction dissolves — but that acceptance is a ruling, and it should be written into
   the workbook so no later pass re-derives it. A **third** string,
   `PEQ Entry 3 (Level 1 · Level 2 routes)` (18 occurrences across the 6 live LAUNCH PEQ
   decks), agrees with neither and needs ruling alongside.
4. **The Calm Mode print tint** — `body.calm{background:#F4F1E9}` outranks the print block's
   `body{background:#fff}` on specificity in the 24 BUILD_ASDAN decks. Invisible with
   background graphics off, which is the default. A specificity-convention ruling, not a
   patch to 24 files.
5. **`GROW_HUM_W13_Belonging_Briefing`** prints a page 3 of 28 characters at 0.795% ink —
   reported by the new gate, not failed, and out of this order's scope. It is one of the two
   decks the previous pass recorded as printing different text run to run.
---

# ORDER N6-Z — FINISH AND LAND

`mbm-next-six-weeks-final-2026-08-28-N6Z` · worked 2026-08-28 · branch
`claude/new-session-q7ztqq`, from N6-I's tip `3cdb4ee4`

Supersedes N6-F and N6-I. **§Z4 halted on its own hard gate: the three Art zips are not
attached to this session** — the uploads directory holds only the N6-I order file, and a
filesystem search finds no zip. Nothing was reconstructed. N12 stays CLOSED — REFUTED.

## §Z0 — State at intake

| | |
|---|---|
| `origin/main` | `288f84543ccef2884de62e6002b4b814360249c1` |
| branch tip | `3cdb4ee4` — as the order predicted; 24 commits ahead of `origin/main`; tree clean |
| `_next6/FINDINGS.md` | two order sections (N6, N6-I), 56 headings |
| `_next6/GUIDE_TAG_MAP.md` | present |
| lessons carrying a SoW alignment verdict | **0** |
| frozen `Science_Teesside/*/v3_40min` | untouched vs `origin/main` (0-line diff) |
| Art pack trees in the repo | **none** |

**A deviation from the order's prediction map, stated before anything rests on it.** The
order says "one row per lesson across all 192". **192 is the count of HTML *files* across
twelve packs.** Nine packs are in the repository — 159 files — of which **132 are lessons**
and 27 are support surfaces (hubs, front doors, evidence windows, printable resource sheets,
the assessor-side teacher planning SoW, the Science practicals matrix). The three Art packs'
33 files are absent. **The matrix has 132 rows**, and every excluded file is named in the
tool that excludes it.

## §Z1 — The SoW alignment matrix

Full matrix in [`_next6/SOW_MATRIX.md`](SOW_MATRIX.md).

### The instruments

| lane | workbook | sha256 |
|---|---|---|
| BUILD | `_passsb/inputs/Build SOW 2026-2027.xlsx` | `d757f2a5e5bc8b26…` |
| GROW | `_passsg/inputs/GROW SOW 2026-27.xlsx` | `5b56e6a9a18f3d79…` |
| LAUNCH | `_passsl/inputs/LAUNCH KS4 - 2026-27.xlsx` | `ede3f82a5660f7ba…` |

BUILD is the **vB** instrument per `_passsb/inputs/README.md`. **`vC-PROPOSED` was not used;
there is none in the repository.**

> **A stale pointer, found on the way in.** All three workbooks were edited at `a946f1ce`
> ("label Aut1 W1-W2 as baseline weeks in the three SoW workbooks"), which rewrote 8 science
> rows in the Autumn 1 W1–W2 cells. The files above are the operative, post-edit ones — they
> are what is on `main`. But `_passsb/inputs/README.md`, `_passsb/FINDINGS.md`,
> `_passsb/SOW_MATRIX.md`, `_passsl/FINDINGS.md` and `BUILD_ASDAN/…/manifest.json` all still
> cite the **pre-edit** shas (`730f9a86…`, `05f385ae…`). The edited rows are outside these
> packs' range so no verdict below is affected, but a later pass reading those pointers will
> audit against a workbook that is no longer there. **Reported, not fixed** — correcting five
> records across three earlier passes is beyond this order.

### The grid, measured rather than confirmed

| lane | strands | Autumn | Spring | Summer |
|---|---:|---|---|---|
| BUILD | 14 | Aut1 W1–7 · Aut2 W1–7 | Spr1 W1–6 · Spr2 W1–6 | Sum1 W1–6 · Sum2 W1–7 |
| GROW | 14 | Aut1 W1–7 · Aut2 W1–7 | Spr1 W1–6 · Spr2 W1–6 | Sum1 W1–6 · Sum2 W1–7 |
| LAUNCH | **18** | Aut1 W1–7 · Aut2 W1–7 | Spr1 W1–6 · Spr2 W1–6 | Sum1 W1–6 · Sum2 W1–7 |

The order's facts hold on strand counts — 14, 14, 18 — and on LAUNCH's non-uniform grid
(7/7, 6/6, 6/7). **The deviation: BUILD and GROW have the *identical* non-uniform grid.**
The order describes "14 strands × W1–W7 per half term" for BUILD/GROW as if uniform and
LAUNCH as the exception; measured, all three lanes share one shape. That matters for §Z2,
because it makes the one-week conflict estate-wide rather than a LAUNCH peculiarity.

### Two instruments, no shared code path

| | reads | never reads |
|---|---|---|
| **A** `z1_instrument_a.py` | the filename and the pack manifest | the deck |
| **B** `z1_instrument_b.mjs` | the rendered deck, every slide activated in turn | the manifest or the filename |

**INSTRUMENT-SPLIT: 0 of 132.** Earned, not assumed:

- the comparator reaches **every** row. A first version fired on only 54 of 132, because two
  packs state the half-term and the week in separate manifest fields and one states a bare
  estate week — a comparator that cannot fire is not agreement.
- it is **red-proved on all three deck shapes**: perturb a deck's week and it names exactly
  that deck, whether the deck states its week as a term label, a brandline or "Week n of 14".

**Both instruments were wrong before they were right**, and both were caught by printing what
they excluded rather than by trusting a count:

- A's lesson classifier carried a bare `SOURCE` in its exclusion list, which matched
  "People, Steps and **Resources**" and silently dropped a real GROW_ASDAN deck from the
  population.
- B asked for a fixed list of week phrases and read **60 of 132 decks as stating no week at
  all**. Three packs state it only in a brandline — `GROW ASDAN · PERSONAL EFFECTIVENESS ·
  AUTUMN 2 · W1`, `BUILD · SCIENCE · WEEK 8A · EXPLORE` — and GROW_ASDAN writes its
  objective as a heading with the text on the next line. Fixed: 132/132 on both.

### The join, and the off-by-one the second instrument caught

**The join is on what the pack claims, not on a derived week.** A pack naming `Aut2·W1` is
already speaking the workbook's units; converting through the disputed calendar introduces an
off-by-one the pack never had.

A first version did exactly that, and **42 of 132 verdicts rested on it**.
`BUILD_ASDAN_A2_COMM_W1`, which claims `Aut2·W1`, came out as `Aut2·W2` and was judged
against *"Practise a vocational skill our project needs"* — which is what the pack's own **W2**
deck teaches. GROW_ASDAN was worse: its bare week 1–6 was read as an estate week, landing
every deck in Aut1 instead of Aut2. **The second, independent verdict pass caught it by
quoting the outcome it had been handed.** That is what the two-instrument rule is for, and it
is the clearest return this order got from it.

Confirmed by a **third instrument**:

| check | result |
|---|---|
| BUILD_ASDAN prints its own `Exact SOW outcome` — does it equal the selected cell? | **24/24 exact**. The old join would have scored 0/24. |
| LAUNCH_ASDAN's manifest `sow_topic` — does it equal the selected cell? | **27/30 exact**; the 3 are paraphrases of the same outcome (*"Gather feedback from those we support"* vs *"Design and, where authorised, gather project feedback"*), not different weeks. Tier 3. |

### The verdicts, from two passes that were not allowed to see each other

Every lesson was classified **twice**: once from the extracted row alone, by a reader
forbidden to open a deck; once by reading the deck itself, by a reader forbidden the
manifest. Where the two returned different classes the row is **UNRESOLVED** and both
readings are kept, because the standing rule makes a disagreement a finding.

| pack | lessons | ALIGNED | PARTIAL | MISALIGNED | SURFACE-SPLIT | SOW-SILENT | DELIBERATE-DIVERGENCE | UNRESOLVED |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `BUILD_ASDAN` | 24 | 23 | 0 | 0 | 0 | 0 | 0 | 1 |
| `GROW_ASDAN` | 18 | 17 | 0 | 0 | 0 | 0 | 0 | 1 |
| `LAUNCH_ASDAN` | 30 | 28 | 0 | 0 | 0 | 0 | 0 | 2 |
| `BUILD_Science` | 12 | 2 | 4 | 0 | 0 | 0 | 0 | 6 |
| `GROW_Science` | 12 | 8 | 2 | 0 | 0 | 0 | 0 | 2 |
| `LAUNCH_Science` | 18 | 0 | 2 | 10 | 0 | 0 | 0 | 6 |
| `BUILD_Humanities` | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 |
| `GROW_Humanities` | 6 | 5 | 0 | 0 | 0 | 0 | 0 | 1 |
| `LAUNCH_Humanities` | 6 | 5 | 0 | 0 | 0 | 0 | 0 | 1 |
| **total** | **132** | **88** | **8** | **16** | **0** | **0** | **0** | **20** |

**The two passes agreed on 112 of 132 rows and disagreed on 20.**

| pack | lesson | data pass | deck pass | |
|---|---|---|---|---|
| `BUILD_ASDAN` | `BUILD_A2_CON_W2` | ALIGNED | SURFACE-SPLIT |  |
| `BUILD_Science` | `W11A` | SURFACE-SPLIT | MISALIGNED | ⚠ calendar |
| `BUILD_Science` | `W11B` | SURFACE-SPLIT | MISALIGNED | ⚠ calendar |
| `BUILD_Science` | `W12A` | SURFACE-SPLIT | MISALIGNED | ⚠ calendar |
| `BUILD_Science` | `W12B` | SURFACE-SPLIT | MISALIGNED | ⚠ calendar |
| `BUILD_Science` | `W8A` | SURFACE-SPLIT | DELIBERATE-DIVERGENCE | ⚠ calendar |
| `BUILD_Science` | `W8B` | SURFACE-SPLIT | DELIBERATE-DIVERGENCE | ⚠ calendar |
| `GROW_ASDAN` | `ENT_A2_W5` | ALIGNED | PARTIAL |  |
| `GROW_Humanities` | `W14` | ALIGNED | DELIBERATE-DIVERGENCE | ⚠ calendar |
| `GROW_Science` | `W10B` | PARTIAL | ALIGNED | ⚠ calendar |
| `GROW_Science` | `W12B` | PARTIAL | ALIGNED | ⚠ calendar |
| `LAUNCH_ASDAN` | `COMM_W10` | ALIGNED | DELIBERATE-DIVERGENCE |  |
| `LAUNCH_ASDAN` | `PEQ_W12` | PARTIAL | DELIBERATE-DIVERGENCE |  |
| `LAUNCH_Humanities` | `LAUNCH_HUM_W12_Fieldwork_Data_Graphs.htm` | PARTIAL | ALIGNED | ⚠ calendar |
| `LAUNCH_Science` | `W10L2` | MISALIGNED | PARTIAL | ⚠ calendar |
| `LAUNCH_Science` | `W11L1` | MISALIGNED | SURFACE-SPLIT | ⚠ calendar |
| `LAUNCH_Science` | `W12L1` | MISALIGNED | SURFACE-SPLIT | ⚠ calendar |
| `LAUNCH_Science` | `W12L2` | MISALIGNED | SURFACE-SPLIT |  |
| `LAUNCH_Science` | `W13L1` | MISALIGNED | SURFACE-SPLIT | ⚠ calendar |
| `LAUNCH_Science` | `W8L1` | MISALIGNED | DELIBERATE-DIVERGENCE | ⚠ calendar |

**None of these was broken by picking one.** The deck reader is better informed on some of
them — it saw a "Staff Ready · SOW position" card in `LAUNCH_ASDAN/COMM_W10` that rewrites
the SoW cell, and a qualification-boundary note in `PEQ_W12` that makes the missing
sign-off deliberate rather than absent — and that is exactly the temptation the rule
exists to refuse. Better informed on the row is not the same as right about the class.

### Tier 2: 28 rows, and not one applied

§Z7 makes any Tier-2 item a hold, and Tier 2 is *any* change to an LO, a success criterion,
or what a pupil actually does. **28 rows carry one from at least one pass. All are diffed
and held; none is applied.**

**And the Tier-2 count is itself contingent.** 22 of the 28 sit on rows whose SoW cell
changes with the §Z2 ruling, so ruling the calendar the other way would dissolve most of
them. **6 stand regardless of it**, and they are two different things:

- **5 BUILD_Humanities rows.** Both passes call them MISALIGNED and the deck reader
  tiers them Tier 2, because the pack teaches the lower Tees, the 1825 railway and the
  ironstone chain against a `World About Me` half-term of festivals, Remembrance and
  Human Rights Day. Neither calendar reading matches; closing the gap would mean
  rewriting six lessons or re-owning the strand. **Held.**
- **`GROW_ASDAN/ENT_A2_W5`.** The deck reader found the Young Duke enrichment challenge
  repurposed as an instrument for the enterprise project — *"one practical project
  improvement rather than a broad environmental or social-impact claim"* — and a
  Supported route on which no challenge is attempted at all. The data pass, which could
  not see the route ladder, called it ALIGNED. **Held**, and it is one of the 20
  disagreements above, so it is doubly not mine to settle.

Full per-row detail, both readings and both tiers, in `_next6/SOW_MATRIX.md`.

## §Z2 — The calendar conflict: RULE 3, recorded, nothing changed

| | Autumn shape | source |
|---|---|---|
| **SoW grid** | Aut1 W1–W7 + Aut2 W1–W7 = **14 weeks** | all three workbooks, read directly; the half-term rows agree (*"Aut 1 · Sep to Oct (7 wks)"*) |
| **repo calendar** | Aut1 W1–W8 + Aut2 W9–W15 = **15 weeks** | `_passpq/tools/l2k_plan.py` `BLOCKS`; `Planning/*/README.txt` — *"Aut 1 = 8 weeks (W1 1 Sep → W8 19 Oct)"*, *"W8 = w/c 19 Oct ← LAST WEEK OF AUT 1"*, *"The LA calendar confirms the 8-week Aut 1"*; `_assert_calendar()` passes |

They disagree by exactly one week. **§Z2's rule 1 (the SoW governs where its grid is
explicit) and rule 2 (the repo calendar governs where the SoW is silent) both fire and point
opposite ways — which is rule 3: record both, change nothing, put it to Matt.**

**And each ASDAN pack is internally consistent under a *different* reading, in its own
manifest:**

| pack | states | consistent only under |
|---|---|---|
| BUILD_ASDAN | `"Autumn 2 · Week n"` **and** `continuationWeek` 9–14 | **CALENDAR** — Aut2·W1 = estate W9 |
| LAUNCH_ASDAN | `pack_week` 7–12 **and** `source_week` Aut1·W7, Aut2·W1–W5 | **SoW** — pack W8 = Aut2·W1, so Aut1 ends at W7 |

Neither pack is wrong on its own terms. **The estate has two conventions in use at once**,
which is the finding N5 could not reach without this matrix.

### The cost of each reading

| reading | cost |
|---|---|
| **SoW governs** | every lesson lands on a real SoW cell, 132/132. BUILD_ASDAN and GROW_ASDAN re-seat to estate W8–W13; LAUNCH_ASDAN to W7–W12. BUILD_ASDAN's own `continuationWeek` then contradicts its own term label. |
| **calendar governs** | **7 Science lessons land on `Aut1·W8`, a cell the SoW does not have** — the workbook supplies 14 autumn rows for a 15-week autumn. 125/132 map. LAUNCH_ASDAN re-seats to W7–W13. |

**Packs that would move under each reading** are in `_next6/SOW_MATRIX.md`. **No week number,
term tag, sequence chip, manifest, checksum or nav string was changed** — and that is proved,
not asserted. Re-run at the merge tip: of the **126 lesson files this order touched, 126 strip
back byte-for-byte** to the tree §Z3 patched from, so the only change any lesson carries is the
toggle and no placement string, LO or success criterion differs by a single byte. This is a
named stop condition and the ruling is Matt's.

### The verdicts are **not** unaffected by it — 60 of 132 rows turn on the ruling

An earlier draft of this section said the alignment verdicts were unaffected, because the
packs that name their own half-term week are joined on that claim and select the same cell
either way. That is true of the three ASDAN packs. **It is false of the other six.**
BUILD/GROW/LAUNCH Science and Humanities state a *bare estate week* (`W10`, `SCI_L_W10L1_…`)
and nothing else, so the calendar is the only thing that can place them — and the two readings
place them one cell apart.

| pack | rows | select a **different** SoW cell under the two readings | land on a cell the SoW does not have |
|---|---:|---:|---:|
| BUILD_ASDAN | 24 | 0 | 0 |
| GROW_ASDAN | 18 | 0 | 0 |
| LAUNCH_ASDAN | 30 | 0 | 0 |
| BUILD_Science | 12 | 12 | 2 |
| GROW_Science | 12 | 12 | 2 |
| LAUNCH_Science | 18 | 18 | 3 |
| BUILD_Humanities | 6 | 6 | 0 |
| GROW_Humanities | 6 | 6 | 0 |
| LAUNCH_Humanities | 6 | 6 | 0 |
| **total** | **132** | **60** | **7** |

**60 of 132 lessons select a different SoW outcome depending on a ruling that has not been
made, and on 54 of them the verdict genuinely turns on it.** The other 6 — the whole of
BUILD_Humanities — score zero against *both* candidate cells, so their verdict stands either
way; "the cells differ" and "the answer changes" are not the same claim and are counted
separately here. The verdict pass was handed one of the two readings — the SoW grid, §Z2's own
rule 1 — and had no way to know the other existed.

### Two more instruments, keyed to content and to the deck's own printed outcome

`_next6/tools/z1_join_probe.py`. Neither reads a week number, and both consume the two
candidate cells the matrix already carries rather than re-deriving them, so neither shares
reasoning with the join that produced them:

| instrument | keyed to |
|---|---|
| **CONTENT** | content-word overlap between what the deck *teaches* — title, objective, success criteria — and each candidate outcome |
| **PRINTED** | sequence similarity between the outcome the deck *prints for itself* (its sow-strip, or its manifest row) and each candidate outcome. This is the instrument that settled the ASDAN off-by-one 24/24. |

```
                     --------- CONTENT ---------        --------- PRINTED ---------
pack                     SoW calendar  weak  tie@0   n/m      SoW calendar  weak  tie@0   n/m
BUILD_Humanities           0        0     1      5     0        0        0     0      0     6
BUILD_Science              4        4     2      0     2        4        4     2      0     2
GROW_Humanities            4        0     2      0     0        6        0     0      0     0
GROW_Science              10        0     0      0     2       10        0     0      0     2
LAUNCH_Humanities          4        0     2      0     0        0        0     0      0     6
LAUNCH_Science             0        6     8      1     3        0        1    14      0     3
```

*weak* = the two cells score within the margin floor of each other, so the row states no
reading. *tie@0* = neither cell matches at all, so the calendar ruling cannot rescue the row.
*n/m* = not measurable: the calendar reading supplies no cell, or the deck prints no outcome.

**Both instruments point the same way in every pack, and there are zero row-level
disagreements between them.**

### The margin floors are measured from the noise, not chosen against the answer

Sequence similarity never returns exactly equal for two different strings, so with no floor
the PRINTED instrument declares a winner on pure noise — under the randomisation red-proof it
returned GROW_Science 1 to 9 on text that means nothing. So each instrument carries a margin
floor taken from the **95th percentile of its own margin distribution under that
randomisation**:

| instrument | noise median | noise p95 → floor | real median |
|---|---:|---:|---:|
| CONTENT | 0.000 | **0.34** | 0.600 |
| PRINTED | 0.075 | **0.23** | 0.484 |

**A first draft used 0.15 for PRINTED. That was wrong** — it sits below the noise *p90* of
0.191, so 9 of 41 randomised rows would have cleared it. It is recorded here rather than
quietly replaced, because a floor chosen for its effect on the real run is not a floor.

**Red-proofed twice:**

| perturbation | expected | got |
|---|---|---|
| the two candidate cells swapped in the input | every column mirrors | **exact mirror** |
| the outcome text randomised across all rows | no reading survives | **none does** — every pack falls to *weak* or *tie@0* on both instruments bar two stray BUILD_Science rows |

### What the four instruments together say

**The estate does not have one convention; it has both, and the split runs inside the teaching
packs as well as inside the ASDAN manifests.**

- **GROW_Science is authored against the SoW grid**, decisively and on both instruments: its
  decks print the SoW cell **verbatim** — `W9` prints *"Compare and group rocks…"*, `W11`
  prints *"Describe causes and effects of global warming…"*, ten rows at similarity 1.00 to
  the SoW cell and never once to the calendar cell. GROW_Humanities and LAUNCH_Humanities
  likewise, 4–6 rows to nil.
- **LAUNCH_Science is authored against the repo calendar.** It never once scores a SoW win on
  either instrument. `W10L2` *Growth and Differentiation* scores 1.00 on content against the
  calendar cell *"Explain growth & stem cells"* and 0.33 against the SoW cell *"Stem-cell
  ethics discussion"*; `W12L1` prints *"Describe DNA, genes and chromosomes."* — the calendar
  cell verbatim, 0.94 against it and 0.39 against the SoW one.
- **BUILD_Science is split against itself**, 4 rows to 4 on both instruments, and this is the
  one place the conflict is a genuine pack defect rather than an unmade ruling. `W9` prints
  the SoW cell at 1.00; `W12` prints the *calendar* cell at 1.00. A single pack cannot be on
  both readings at once, so whichever way §Z2 is ruled, half of BUILD_Science moves. Its own
  sow-strip and its own week tag disagree — which is the estate's definition of
  **SURFACE-SPLIT**, and the data verdict pass reached that label independently.

### What this does to the verdicts, and what I did not do about it

The data pass returned **22 MISALIGNED**, of which **16 are LAUNCH_Science** — and the agent
reached that verdict honestly, writing *"the whole pack sits one week later than the SoW cells
it is joined to"* and tiering them **Tier 1, a stale week anchor, not an LO edit**. On the
repo-calendar reading those rows are largely ALIGNED. The verdict is not a property of the
lesson; it is a property of the unmade ruling.

**So those rows are reported under both readings and no verdict is asserted for them.** This is
the order's own stop condition — *"a §Z2 lane conflict where SoW and repo calendar disagree"* —
and the honest output is the pair, not a pick.

**BUILD_Humanities survives both readings and is a real finding.** Its six decks teach the lower
Tees, the 1825 Stockton & Darlington Railway, the ironstone chain and dated town growth; the
`World About Me (Humanities)` strand's Aut2 cells ask for festivals of light, comparing
celebrations, handling festival artefacts, Remembrance and Human Rights Day. **Five of six rows
are tie@0 — neither reading matches at all** — so shifting the calendar by a week does not
rescue it: the whole half-term of that strand is festival content and the whole pack is
local-history content. That is a strand-ownership question for Matt, not a week number, and it
is Tier 3: nothing in it is fixable by editing a lesson.

I checked the obvious instrument defect first and it is not one: `World About Me (Humanities)`
and `RE & World Views` are separate blocks in the workbook with separate outcomes, so the
grid extractor has not carried a merged cell across the two, and `STRAND_MAP` points at the
right one.

## §Z3 — The guidance toggle, applied

**380 tags across 126 lesson decks.** PH-3's mechanism, not a new one:
`data-mbm-guide="staff|route"`, hidden unless `html.mbm-guide-on`, an **ⓘ Guidance** button
in the controls, key **G**, `localStorage mbm_guide_v1`, default hidden, hidden not removed.
The CSS, script and button are PH-3's own, taken from `_eca1/tools/guidepatch.js` rather than
retyped. The **patcher** is new because PH-3's classifies by `.li-box`/`.task-box`/
`.wit-panel`, which occur **0 times in all 159 files**.

**Selection happens in a real DOM, application in the source**, because three tests that
decide the hide-set cannot be done on markup:

1. **is it visible at all?** Half the GROW_ASDAN candidates sit inside the TA briefing
   overlay, which this order says to leave alone. Tagging them is churn at best and a second
   hiding mechanism on top of the estate's TA layer at worst.
2. **is it inside a Lundy zone box?** Those stay visible. A source-side proximity window
   cannot answer it — a first attempt using a 2500-character window blocked **100% of
   candidates in three packs**, because these decks carry `.lundy` containers throughout.
   `closest()` answers it exactly.
3. **who is the text talking to?** Needs rendered text, not markup.

The hide-set is committed as `_next6/evidence/Z3_HIDE_SET.json` so it can be argued with.

### What is hidden, and what is not

| pack | selectors | decks | tags |
|---|---|---:|---:|
| BUILD_ASDAN | `.chips .chip:last-child` · `p.small` · `.hero p` (label-keyed) · `.box.objective`/`.box.good` (label-keyed) · `.box.rehearsal` (text-keyed) | 24 | 216 |
| GROW_ASDAN | `.guard` · `.evidence-note` | 18 | 50 |
| LAUNCH_ASDAN | `.box.screen` | 30 | 30 |
| BUILD_Science | `p.sowline` | 12 | 12 |
| GROW_Science | `p.sowline` | 12 | 12 |
| LAUNCH_Science | `p.sowline` | 18 | 18 |
| BUILD_Humanities | `.reportback` | 6 | 6 |
| GROW_Humanities | `.lnote` | 6 | 36 |
| LAUNCH_Humanities | — | 0 | 0 |
| **total** | | **126** | **380** |

*(An earlier draft of this table gave BUILD_ASDAN 192 and folded the three Science packs into
one row of 42. The rows did not sum to the total. Re-counted from the tree: 216, and Science
split out. The total was right; the breakdown was not.)*

**No element was tagged `lundy`.** Counted in the tree: 266 `staff`, 114 `route`, **0
`lundy`** across the nine packs — so the order's instruction to keep the Lundy zone boxes
visible is satisfied by construction and not merely by intent. (The estate's 175 pre-existing
PH-3 files do carry 280 `lundy` tags; none of those files is in these nine packs.)

**`.hero p` reached the paragraph GUIDE_TAG_MAP predicted would need an authored marker.**
The map said BUILD_ASDAN's unclassed `Exact SOW outcome` paragraph was the one family in the
nine packs needing a new attribute. It is unclassed *and* inside an unclassed div, so
`.hero > p` reaches nothing — but `.hero p` plus the leading-`<strong>` label reaches exactly
those two paragraphs and no pupil-facing one. **No marker was authored anywhere.** The map's
estimate of 25 sites is superseded by 0.

**LAUNCH_Humanities received 0 tags**, and that is a correct outcome, not a failure: its
`.lnote` all sit inside `.lundy` zone boxes, which stay visible.

**Kept visible, verified:** the pupil's `Learning objective:`, the success criteria, the
`.lundy` SPACE/VOICE/AUDIENCE/INFLUENCE zone strip, the route ladder, the task. GROW_ASDAN's
`.soft` reads as staff to a keyword probe and is not — *"Standard: add a reason or example.
Optional reach: name what evidence could change your first answer."* is addressed to the
pupil, and it is untagged.

### The order's parenthetical is false, and asserting it is what found that

§Z3 says *"print CSS hides the slide container, so slide-side tagging must never reach it —
assert it, do not reason about it."* **Asserted: false for two packs.** GROW_ASDAN and
LAUNCH_ASDAN both carry an `@media print` rule that reveals `.slide` — LAUNCH_ASDAN's is
N6-I's own N3 addendum, added so the deck would print at all. In those **48 decks a
slide-side tag does reach paper**, and with the toggle defaulting to hidden it would delete
staff content from a printed artefact that used to carry it.

One addition to PH-3's CSS, and it is load-bearing:

```css
@media print{html:not(.mbm-guide-on) [data-mbm-guide]{display:revert!important}}
```

**Red-proved.** With it removed, GROW_ASDAN's printed characters drop **5019 → 4557**, deleting
462 characters of staff content from paper. Science, whose slides do not print, is unchanged
— the negative control. Without the exemption the order's own print gate cannot pass.

### Gates

| gate | result |
|---|---|
| strip → byte-identical to pre-patch | **126/126** |
| idempotent on re-run | 126 skipped, 0 re-tagged |
| **print output identical** (pages, ink to 1e-6, characters) | **198/198 renders** |
| toggle-ON: lesson text identical to pre-patch | **126/126** |
| toggle-ON: element count identical | **126/126** |
| default OFF hides every tagged element | **126/126**, 0 tagged visible |
| `s24-print-renders` | **PASS**, all nine packs |
| estate battery G1, G2, G3, G5, G6, G12 | **PASS**, all nine packs |
| checksums | 126 entries regenerated, **0 mismatches** across all nine packs |

**Measured and reported rather than tuned away:** adding the ⓘ button wraps the control bar
to two rows in **36 of 126 decks** (Humanities 1250×44 → 1250×96, LAUNCH_ASDAN 1256×58 →
1256×96). Computed styles are identical in the other 90. The gate is **text and element
count**, because hashing computed styles while deliberately adding a visible control measures
the control, not the patch — and extending an exclusion list until the hash matched would be
tuning a gate rather than running one.

**5.2% of the on-screen text (11,346 characters of 219,436) is hidden by default.**

### Three bugs this section's own gates caught

1. **The markers bracketed the whole document.** A first version opened before `</head>` and
   closed before `</body>`, so `strip()` removed everything between them — the entire body.
   The reversibility gate caught it on the first run: **0 of 126** stripped back, every one
   40 KB short. Markers must wrap what they own and nothing else.
2. **Two rules selected the same element.** `p.small` and `.hero p` both reach the SoW
   cell-reference paragraph; applying both edits to one span produced
   `<p class="small">="route" class="small">`, a corrupted tag, in 24 files. Deduped by span,
   first rule wins.
3. **The applier refused to guess, and it was right to.** The signature for an unclassed
   `<p>` found no candidates while it required a `class=""` match, so it reported a mismatch
   and patched nothing rather than tagging the nearest paragraph.

## §Z4 — HALTED on its own hard gate

**The three Art zips are not attached to this session.** The uploads directory holds only the
N6-I order file; a filesystem search for `*Art_Spring2*`, `*Teesworks*Reclaimed*` and
`*6x40min*` returns nothing. **Nothing was reconstructed**, as the order requires. No
destination collision check was needed because nothing was landed. **N12 stays CLOSED —
REFUTED** and I3's ruling stands unchanged: the packs land at Spring 2, unaltered, in a
session that has them.

## §Z5 — External links: reconciled, and the count difference is proved

**26 unique citation URLs across the nine landed packs**, reproduced by a second, independent
derivation (a different script, same figure).

**The reconciliation, proved from the committed record rather than assumed.** The order asks
which instrument is wrong between chat's 34 and I4's 26. Neither, quite — there are three
figures and each is right about a different population:

| figure | population | status |
|---|---|---|
| **34** | chat's count across twelve packs | an over-count; Pass N6 corrected it by measurement |
| **30** | Pass N6's measurement across twelve packs | correct for twelve packs |
| **26** | this pass, nine landed packs | correct for nine |

**30 − 26 = 4, and the four are nameable**: comparing N6's committed host list to mine, the
absent ones are **Tate ×2, Tees Valley Museums ×1, and Teesside University / MIMA ×1** — all
art-gallery and art-education citations, which is exactly what three Art packs on a Teesworks
sculpture unit would carry. The hypothesis that 26 is "the nine landed packs only" is
therefore **proved, not assumed**.

**MEASUREMENT INVALID — venue.** `example.com` → `000`, `historicengland.org.uk` → `000`,
**control `pypi.org` → `200`** in the same run. That is the venue's network allowlist, not
link rot. **No reading was recorded and nothing is proposed for removal.** A second reading
an hour later would be a second invalid measurement, so none was attempted.

## §Z6 — I6 CLOSED — PREMISE REFUTED

Recorded at the head of the I6 section above with its four measurements, so no later pass
reopens it. In summary: the LAUNCH column states a floor for **0 of its 13 subjects**; the
ladder's own `A2` says each cell shows the pathway's **target**, with a floor only "where
relevant"; `D13` is **byte-identical across all three workbooks**, so it is shared
front-matter; and **28 of the 29** LAUNCH-workbook cells that name a PEQ level name Entry 3,
the one exception being the GROW column. "D13 contradicts the estate anchor" read a target
cell as a floor.

**One live item, as a question and not a defect:** `_passsl/` — the pass that ingested the
LAUNCH SoW — carries **no level statement at all** across its five `.md` files, so nobody has
ruled on this on the record. A one-line confirmation for Matt and Cheryl.

## §Z7 — Merge: **HELD**, on three grounds, two of them the order's own stop conditions

§Z7 says merge only if **all** of its conditions hold, and prints each. They do not all hold.

### 1 · A conflict between two requirements of this order — **the decisive one**

**§Z3 mandates `localStorage mbm_guide_v1`. §Z7's gate list requires "no browser storage".**
Both cannot be true, and applying §Z3 is what makes §Z7 fail.

Measured: **252 `localStorage` occurrences, all 252 inside the `n6z-guide` marked block, all
for the single key `mbm_guide_v1`, 0 outside.** The packs carried none before. G4 offline
integrity therefore fails in **8 of 9 packs** (the ninth, LAUNCH_Humanities, received no tags)
and the battery is **OVERALL: RED**.

**I have not narrowed gate 4 and I have not dropped persistence.** Either would be breaking a
tie by picking one, which this order's own standing rule forbids. The estate already named
the fork, in N7: **narrow gate 4 to that one key**, or **ship the toggle without persistence**.
It is Matt's call, and the merge waits on it.

**The fact that bears on the choice, and a round trip worth recording.** I doubted the "175
existing carriers" figure mid-pass, re-measured with a differently-keyed probe — files
containing the string `localStorage` — got 532 estate-wide and 406 outside these packs, and
concluded the 175 was unreproducible. **It was not; my second probe was keyed to the wrong
thing.** 175 is the count of files that already carry *this exact mechanism*, and it verifies
exactly on `origin/main`:

| measured on `origin/main` | count |
|---|---|
| HTML files carrying `data-mbm-guide` | **175** |
| …of those, files using `localStorage` | **175** |
| …of those, files using the key `mbm_guide_v1` | **175** |

**The estate already ships this toggle, with this key, in 175 files that gate 4 has never been
run against.** So "no browser storage" is not an invariant §Z3 broke; it is a gate that only
the nine new packs were passing. (The wider `localStorage` figures are real too — 532
estate-wide, 406 outside these packs, 267 with an `mbm_` key — but they are not what "narrow
gate 4 to that one key" is measured against, and quoting them in its place was my error.)

**And this is the standing rule catching me, not an instrument.** A second probe disagreed
with a recorded number, and my first instinct was to treat the newer reading as the correct
one and rewrite the record. That is precisely the tie-break the order forbids. The
disagreement was the finding: two probes, two different questions, and the older number was
answering the right one.

### 2 · A §Z2 lane conflict — a named stop condition

The SoW grid and the repo calendar disagree by one week, estate-wide, and §Z2's rules 1 and 2
both fire in opposite directions. Recorded above; nothing relabelled.

**And the conflict is not cosmetic: 60 of 132 lessons select a different SoW outcome
depending on which reading is ruled correct — on 54 of them the verdict changes with it** —
and 7 land on `Aut1·W8`, a cell the workbooks do not have. Two further instruments — content, and the deck's own printed outcome,
neither reading a week number — say the estate uses **both** conventions: GROW_Science is
authored against the SoW grid and prints its cells verbatim; LAUNCH_Science is authored
against the repo calendar and never once scores a SoW win; BUILD_Science is split 4 to 4
against itself. Ruling either way moves real packs, and the ruling is Matt's.

### 3 · §Z1's Tier-2 count — **28 rows, none applied**

Any Tier-2 item is a hold under §Z7 and there are 28 of them, so this ground stands on its
own. 22 dissolve or survive on the §Z2 ruling; **6 stand regardless** — five BUILD_Humanities
rows where the pack and the strand teach different subjects, and `GROW_ASDAN/ENT_A2_W5`, where
one pass saw a Supported route on which no enrichment challenge is attempted and the other
could not. Diffed in `_next6/SOW_MATRIX.md`; not one applied.

**And §Z1 itself did not come out clean.** The two verdict passes returned different classes
on **20 of 132 rows**, and every one is kept as UNRESOLVED with both readings shown. That is
not a defect in the matrix; it is the matrix reporting honestly. But it means no row in that
20 has a settled verdict, and §Z7 asks for a matrix "complete for all 192 lessons" — on 132
of them it is complete and on 20 of those it is complete in the sense of *knowing that the
answer is contested*, which is not the same thing.

### The rest of §Z7's list, each printed

Re-run in full at the merge-candidate tip, *after* §Z3 had patched 126 lesson files —
`_next6/evidence/Z7_GATE_BATTERY.txt`. **55 PASS · 8 FAIL · 9 MEASUREMENT INVALID · OVERALL
RED.** All 8 failures are gate 4 and all of them are the toggle: the per-pack violation count
equals the per-pack `localStorage` count exactly, 48/36/60/24/24/36/12/12/0. All 9 INVALIDs
are `s23-no-learner-names` correctly refusing to pass without its reference list, which is not
in the repository and should not be.

**`s24-print-renders` is green on all nine packs at this tip: 159 surfaces, 231 renders, 1113
pages, near-blank pages 0, and learner-confirmation 26 + 19 + 30 = 75/75** — N6-I's I1 number,
re-proved on paper after 126 files were rewritten underneath it.

| condition | result |
|---|---|
| `node --check` + `json.loads` on every block | **PASS**, 9/9 packs |
| tag balance and duplicate ids 0 | **PASS**, 9/9 |
| `timings` sum to 40 | **PASS**, 9/9 |
| offline integrity | **FAIL** — see 1 above; every violation is §Z3's own toggle |
| reduced motion, no `@keyframes` reintroduced | **PASS**, 9/9 |
| links and manifest ↔ disk, both ways | **PASS**, 9/9 |
| additivity, strip → byte-identical | **PASS** — 126/126 for §Z3 |
| sentinel `ll-g:loop-mark` SET-invariance (the constant 45 retired) | **PASS** — 72 at the branch point, 72 now |
| `s23-no-learner-names` exits MEASUREMENT INVALID without its list | **PASS** — 9 packs, and the reference list is still absent from the repository, which is correct |
| `s24-print-renders` | **PASS**, every landed pack |
| every new gate proven red once | **PASS** — the print exemption (462 characters lost from paper without it), the instrument-split comparator (all three deck shapes), the names predicate (seeded fixture reds the real tree) |

### A gate that was red for two commits, and nothing said so

Running the `s23` predicate half for §Z7 produced a **names-scan hit** — a named stop
condition — so it was investigated before anything else:

```
_next6/evidence/S24_EVIDENCE_SURFACES.txt:
  CAREERS_W11_<the mock-interview lesson's filename>_LAUNCH
```

**The token is elided even here**, and that is not squeamishness: quoting it in this file
would make *this file* an eighth carrier and force an eighth allowlist entry, which is the
whole point being made below. The token itself is in
`tools/verify_fixture_names.mjs`, where it is declared once with its reason.

**It names no person.** It is a *file path* in the s24 coverage contract, and the string is
the same real LAUNCH ASDAN W11 lesson title Order N6 already ruled on and allowlisted in four
other carriers; it trips the predicate only because `MOCK` is a fixture marker and the
neighbouring words are ordinary titlecase.

**And then it happened a second time, in this order's own evidence.** Committing the battery
log `_next6/evidence/Z7_GATE_BATTERY.txt` tripped the same predicate on the same string, for
the same reason: the log names every surface each pack renders, so it carries the lesson's
file path. A sixth per-file allowlist entry, red-proved the same way — seeding
the checker's own red vector — a `CANARY_PUPIL_` prefix on a first name and a listed
surname — into that very file still reds the gate, so the entry did not widen
anything.

**And a third time, an artefact later, in the same order.** `_next6/evidence/Z1_VERDICTS.json`
keys every row on its file path, so it carries the string too. **Seventh carrier, second
within N6-Z.**

**The recurrence is the finding.** This string trips on *every* artefact that quotes a
LAUNCH_ASDAN file list, and an allowlist that grows once per artefact is saying something
about the predicate, not about the artefacts. Widening the predicate is a ruling on how the
estate detects learner names, so **it is not made here** — it is on the list for Matt. Each
entry stayed narrow and each was red-proved: seeding the checker's own red vector into the very
file just allowlisted still reds the gate, both times.

**The honest part: N6-I committed that file without running this gate**, so the estate's names
gate has been red since `3c683d9f` and I did not notice. Fixed by extending the existing
**per-file** allowlist to the fifth carrier with the same recorded reason — not by exempting
the file, which the allowlist's own comment calls *"an excuse with a filename"*. The gate is
now clean and its self-test passes both directions. The miss is recorded in the allowlist
entry itself, because the useful fact is not the string; it is that a gate went red for two
commits and stayed quiet.


## §Open — what remains for Matt, one line each

1. **The §Z2 calendar ruling.** SoW grid (14-week autumn, all three workbooks) or repo calendar (15 weeks, from real dates) — 60 rows change cell, 54 change verdict, 22 of 28 Tier-2 items dissolve or survive on it, and 7 Science lessons land on a cell the workbooks do not have.
2. **`BUILD_Science` is split against itself, 4 rows to 4** — whichever way §Z2 is ruled, half that pack moves; that half is a pack defect, not a ruling artefact.
3. **`BUILD_Humanities` strand ownership.** Six decks of local Teesside history against a `World About Me` half-term of festivals and Remembrance; both calendar readings score zero, so no ruling rescues it.
4. **§Z3 vs §Z7 on browser storage.** Narrow gate 4 to `mbm_guide_v1` — 175 estate files already carry exactly that mechanism — or ship the toggle without persistence. The merge waits on this one.
5. **28 Tier-2 items, diffed and held, none applied**, in `_next6/SOW_MATRIX.md`.
6. **19 rows where the two verdict passes disagree**, both readings kept; no tie was broken.
7. **§Z4: the three Art zips are not attached to this session** — nothing was reconstructed and nothing is claimed about them.
8. **§Z5: link liveness is MEASUREMENT INVALID in this venue**, not a removal signal; 26 URLs across the nine landed packs, and the 4 that make up N6's 30 are named. Nothing removed.
9. **§Z6 is closed as PREMISE REFUTED**, with one live item: `_passsl/` carries no level statement, so nobody has ruled on the record.
10. **The names predicate.** Its allowlist now grows once per artefact that quotes a LAUNCH_ASDAN file list; widening the predicate is a ruling on how the estate detects learner names.
11. **Five records across three earlier passes cite pre-edit workbook shas.** No verdict here depends on them; a later pass reading them will audit against a workbook that is gone.
12. **Branch deletions remain yours.** Nothing was deleted.
