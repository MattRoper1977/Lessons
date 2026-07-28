# FINDINGS — Pass U (Lessons body)

**Branch** `pass-u-audit` (real name, recorded per brief §3) · off `main` · repo tip at sweep = `32ca685` (derived `git log -1`, not stated by any artefact).
**Base clone** shallow → **`git fetch --unshallow`** run (484 commits) because git-timing instruments give false zeros on `--depth 1` (see U-T2-01).
**Instruments** run from `LundyLoop/tools/` per HANDOVER — not rebuilt.

---

## HEADLINE

**Zero Tier-1 defects. The estate is healthy, exactly as its own HANDOVER predicts.**
Every candidate the sweep raised resolved to one of three dispositions: a **deliberate convention** already
in the record, an **instrument false-positive**, or a **known scheduled OPEN item** with its own pass. This
is the eleventh time (HANDOVER: "healthier than its instruments every single time") and the pattern held —
when an instrument disagreed with the estate, the instrument was wrong. No fix was committed to any lesson,
instrument, or `resources.json`. The deliverable is this record + one Tier-2 proposal.

---

## LINEAGE (brief §0) — recorded, and corrected

The brief frames this as a "Pass Q / Pass U" programme with site branches `claude/pass-q-audit-c5tg3s @ 6845f44`
and site `pass-u-audit`. **The Lessons repo's own record knows no Pass Q or Pass U** — its history is Lundy Loop
(LL-A…LL-I @ HANDOVER), Pass V (D&T v5), Pass S. Per REGISTER R-G01 (cached claims across a boundary) those
site SHAs/branches are treated as **UNVERIFIED** — I did not read the site repo's git to confirm them, and no
Lessons-side finding depends on them. The brief's *rigor rules* were honoured in full; its *stated SHAs* were not
trusted. Any finding that would depend on the site-side taxonomy merge is marked so; none here do (taxonomy was
verified directly in `resources.json`, see U-06).

---

## THE SWEEP — every class, with two independent signals and a disposition

### U-01 · Catalogue integrity, both directions — CLEAN
- **Signals:** `identity_audit.py` (555 files) + `hash_sweep.py` (independent: content-hash vs catalogue).
- **Result:** 0 type-lies (R-C06 "429=429" state holds); 384 catalogue entries; **3** entries "pointing at missing
  files" — *both instruments agree on the same 3* — and all three are `Planning/{BUILD,GROW,LAUNCH}` whose `file`
  is a deliberate **GitHub folder-tree URL** (`type:teacher`, `family:"Weekly Planning"`, `desc:"8 weekly plans…
  Anonymised"`). The resource *is* a browsable folder, not a file; the three folders exist on disk (`ls` confirmed).
  The instruments flag them only because they path-check an `https://` string as if local — a **classification gap
  in the instrument, not an estate defect** (the "resolves above repo root / fine live" class, brief §6/§9, R-D01).
- **Pupil/teacher consequence:** none — the folder links resolve live on github.com.
- **Tier 3 (report only).** *Disposition: not a defect. Optional instrument nicety in carry-forward.*

### U-02 · Uncatalogued leaves — CONVENTION, not drift
- **Signal:** `identity_audit` REVERSE + `hash_sweep` agree: **53** tracked HTML with no catalogue entry.
- This is REGISTER **R-D04** ("entry points catalogued, leaves reachable through the page") — expected, not drift.
- **Tier 3.** *Disposition: convention, closed by reading R-D04.*

### U-03 · Duplicate / near-identical files — DELIBERATE
- **Signal:** `hash_sweep` exact_sets = **4**, near_identical = 31 (declared a floor, not a total — LL-INST-01 limit).
- The 4 byte-identical sets are all the **Planning/ mirror's own content** (`README.txt`, the ASDAN year-plan
  `.xlsx`) duplicated between the subject folder and `Planning/`, plus one `_Archive_VersionA_…` copy. These are the
  content the U-01 folder-links point at; deleting them would break those catalogued resources (R-C04: "uncatalogued
  and unlinked conflates junk with finished work" — do NOT invert into a delete criterion).
- **Tier 3.** *Disposition: deliberate mirror + archive; do not de-duplicate.*

### U-04 · Link integrity — 0 GENUINE broken links (207 raw, all false-positive)
- **Signals:** `link_graph.py` (built to avoid the bare-basename bug) + manual classification of all 207 records +
  on-disk existence checks of every suspect.
- **207 broken-link records = 197 root-absolute (`/Lessons/*`, `/hud.js`, `/theme.js` — live-fine, R-D01) + 6
  JS-concat (`${…}`, not hrefs) + 4 examined:**
  - `about:blank` (`5_6 Local Choice/index.html:801`) — not a link.
  - `COMM_W2_The_Site's_Need.html` (`BUILD_ASDAN/Community_Project/START_HERE.html:11`) — **file exists**; link_graph
    truncated the href at the literal apostrophe inside a *double-quoted* attribute (valid HTML). **Parser blind spot.**
  - `../Launch/` (`YearPlan/index.html:36`) — resolves to `Launch/index.html` which **exists** (Pages directory index).
  - `../` (`YearPlan/index.html:38`) — resolves to root `index.html` which **exists** (the ledgered `../../` class).
- **Consequence:** none — no broken link reaches a pupil/teacher. Consistent with R-G01 row 3 (sitemap 0 dead).
- **Tier 3.** *Disposition: all false-positive. `about:blank`, the apostrophe-truncation and directory-index are three
  small link_graph classification gaps (carry-forward), not estate defects.*

### U-05 · Script validity — CLEAN
- **Signal:** `node --check` on **670** real inline `<script>` blocks estate-wide → **0 syntax errors**.
- **Planted positive (rule 4):** 6 `type="importmap"` blocks were correctly rejected as non-JS by the checker,
  proving it fires — then excluded as JSON, leaving 0. (The Games CDN three.js import maps are a pre-existing
  Games-folder architecture, ruled separate.)
- **Tier 3 / n-a.** *Disposition: clean, verified against a non-zero control.*

### U-06 · Four-surface week/title agreement (rule 11) — CLEAN (only the ledgered swap)
- **Signal A:** scripted intra-file week scan over **150** week-named lesson files (filename vs `<title>` vs `<h1>`).
  *(First pass matched only 7 — a `\b`-before-`_W` regex bug in **my own** check; fixed the boundary, re-ran: the
  self-catch is logged here per the estate's "suspect your own instrument" doctrine.)*
- **Signal B:** `resources.json` titles for the flagged pair.
- **Result:** exactly **2** disagreements, both the **deliberate Careers W6/W7 filename↔label swap** (ledger §9,
  standing rule 7). Four surfaces confirmed to agree on the real week: `resources.json` title = "Careers **W7** ·
  My Career Profile" for the W6-named file (and mirror for W7); the file `<title>` agrees; the filename is the known
  misleading hint. **No new four-surface contradiction anywhere in 150 files** — the signature-defect class is clean.
- **Tier 3.** *Disposition: deliberate, closed by reading.*

### U-07 · resources.json schema/id hygiene — PRISTINE
- **Signal:** 384 entries — **0 duplicate ids, 0 missing ids, 0 missing file/url targets, 0 duplicate file targets**;
  byte-stable round-trip at `json.dumps(indent=1, ensure_ascii=False)` (brief §5.4 holds).
- **Taxonomy (brief §9):** types = lesson 263 · teacher 39 · support 38 · game 30 · pupil 12 · revision 2.
  `teacher` is the canonical value (no capitalised `Teacher`); no `Simulation`/`Game` conflation. **Verified directly**,
  so U-06/U-07 are NOT conditional on the unverified site-side merge.
- **Tier 3 / n-a.** *Disposition: clean.*

### U-08 · Storage keys — consistent with baseline, no new collision
- **Signal:** estate-wide enumeration of `localStorage` literals + bracket access (98 literal distinct + per-file
  `KEY`/`k`/`i` variable indirections, consistent with the ~121 baseline).
- Every do-not-fix key present and correctly shaped: `coldCall_y10`×7 (graded, R-B02 — NOT merged), `ps_coldcall_roster`×105
  (shared strings, R-B01), `coldCall_y10_geog`×4 (cohort silo, R-B03), `mbm_tt_evidence`×20 (no reader, deliberate, R-B04),
  `tt_tracker_v2`×3 (R-B05). No key doing two jobs surfaced.
- **Tier 3.** *Disposition: no new finding; R-B rulings stand. Full KEY-indirection resolution deferred (token discipline).*

### U-09 · Print integrity — 0 ABSENT (R-E05 holds)
- **Signal:** `print_pack_audit.py` (with `classify.py` required stage) → `ABSENT = 0`, `files_with_zero_print_sections = 0`.
  `NOT_DETERMINED` = **16** (was 14 in R-G01/classify note; +2, honestly-unknown files, NOT defects — the honest headline
  is always "N defects and M not-established").
- **Tier 3.** *Disposition: "not one dead print control in this estate" (R-E05) re-confirmed. The +2 NOT_DETERMINED is a
  carry-forward candidate for a human classify, not a defect.*

### U-10 · KO staleness — 114 candidates = the known OPEN scheduled item
- **Signal:** `ko_staleness.py` on **full** history → 114 candidates / 3 architecture-dropped / 44 clean (cardinality
  114+3+44=161 ✓). Matches REGISTER R-G02's recorded ~109 + the predicted LL-G growth (R-E07).
- **Tier 3.** *Disposition: R-G02 is OPEN and scheduled (queue item 9 / R-E07 refinement is its own pass, R-E09). Not
  this pass's to fix. Reads no content, makes no correctness claim.*

### U-11 · Assessed Conditions Cards — known unmentioned offers
- **Signal:** `assessed_conditions_gate.py` → the same NEEDS_HUMAN_RULING offers recorded in HANDOVER open-ruling §2
  (3 real rulings + 1 tool artefact: GROW Supported Opening/Close Frame is word-for-word correct, token matcher blind).
- **Tier 3.** *Disposition: scheduled (HANDOVER §2/§3 reconciliation pass, text-to-Matt-first). Nothing new.*

### U-12 · Reduced motion — scheduled programmes, out of scope
- HANDOVER open queue already scopes all remaining RM work as **scheduled** (LIGHT 10 / MEDIUM 25 / HEAVY 34, each
  gated on Matt; Games ruled out; LAUNCH_HUM blanket rule logged-accepted; Assembly check `8bc2b8b`). Nothing to add.
- **Tier 3.** *Disposition: known, scheduled — brief §9 forbids reopening.*

### U-13 · sitemap_audit — correctly UNRUN
- `sitemap_audit.py` fails loud ("An unfetchable sitemap is NOT a pass. Nothing below was checked.") behind the proxy
  403 — matches HANDOVER. **Not counted as a pass.**

---

## TIER 2 — build the fix, STOP and ask (one decision)

### U-T2-01 · `ko_staleness.py` returns a silent false-zero on a shallow clone
- **Evidence:** on my `--depth 1` clone the tool printed **"CANDIDATES … 0 / clean 161"** — a *pass*. After
  `git fetch --unshallow` the same tool on the same tree printed **114 candidates**. On a shallow clone
  `git log -- <file>` yields one commit, so `last_change` (ko_staleness.py:99-103) returns index 0 for both KO and
  body → `i_ko <= i_body` (line 106) → every file counts "clean". **Unlike `sitemap_audit`, it does not fail loud** —
  it reports the reassuring number.
- **Consequence:** a future session that clones shallow (the add_repo default *tells* you to) and trusts
  `ko_staleness` gets "estate clean" when 114 KO candidates are outstanding — the exact silent-false-pass shape the
  estate's whole doctrine (R-E05, R-G01, sitemap_audit's fail-loud) exists to prevent.
- **The fix (ready, additive, zero-change on full clones — mirrors `sitemap_audit`'s "NOT a pass"):** at the top of
  `main()` in `LundyLoop/tools/ko_staleness.py`, before the `files = …` line:
  ```python
  if sh("git", "rev-parse", "--is-shallow-repository").strip() == "true":
      print("FAIL — shallow clone: per-file history is one commit, so every KO and "
            "body look co-moved and this tool would report 0 candidates. A shallow "
            "clone is NOT a pass. Run `git fetch --unshallow` first. Nothing checked.")
      sys.exit(1)
  ```
- **Two verification signals:** (1) the before/after count flip on one tree (0 → 114); (2) `git rev-parse
  --is-shallow-repository` returns `true`/`false` deterministically and is the canonical shallow test.
- **Why NOT committed here:** REGISTER **R-E09** — an instrument must not be modified in the pass that measures with
  it (I used `ko_staleness` this pass), and HANDOVER's "nothing commits without asking Matt for a key." Also fits the
  already-scheduled ko_staleness own-pass (queue item 9).
- **THE ONE DECISION for Matt:** *apply this shallow-guard to `ko_staleness.py` (and audit the other git-timing tools
  for the same guard) — yes / no?* Recommended **yes**; it only adds a fail-loud path.

*(No Tier-2 items touch a lesson, `resources.json`, or pupil-facing text. No `type` change is proposed, so the site
repo's `chips_check.py` gate is not engaged this pass.)*

---

## REFUSED / DELIBERATE — closed by reading, do not re-flag (feeds the next audit)

| # | what a fresh audit will re-raise | why it is not a defect |
|---|---|---|
| D1 | 3 catalogue entries "point at missing files" | `Planning/{BUILD,GROW,LAUNCH}` are deliberate GitHub folder-links (`type:teacher`); folders exist; live-fine (U-01) |
| D2 | 53 uncatalogued HTML | leaves, R-D04 convention (U-02) |
| D3 | 4 exact-dup sets, 31 near-identical | Planning mirror + `_Archive_` copy; near-list is a floor not a total (U-03, LL-INST-01) |
| D4 | 207 "broken links" | 197 root-absolute live-fine + 6 JS-concat + 4 examined-and-fine (U-04) |
| D5 | Careers W6/W7 filename ≠ title week | deliberate swap, four surfaces agree, ledger §9 / rule 7 (U-06) |
| D6 | `coldCall_y10` vs `ps_coldcall_roster` etc. | two deliberate data models, R-B02/B03/B04/B05 — never merge (U-08) |
| D7 | 16 `NOT_DETERMINED` print files | honest "could not classify", not ABSENT; R-E05 closes print (U-09) |
| D8 | 114 KO candidates | R-G02 OPEN + scheduled own-pass; a candidate list, not a defect count (U-10) |
| D9 | 4 unmentioned assessed offers | HANDOVER §2 rulings + 1 token-matcher artefact; scheduled (U-11) |
| D10 | RM "uncovered" files | all remaining RM is scheduled/gated; Games ruled out (U-12, HANDOVER queue) |
| D11 | Games use CDN three.js | Games ruled separate ("motion is the content"); pre-existing architecture |
| D12 | REGISTER/INSTRUMENTS counts that "don't match HEAD" | historical stamps (R-G04) — re-checkable, not currency claims; movement (382→384, 109→114) is the estate moving, not drift |

---

## CARRY-FORWARD PACK (next letter)

1. **Clone full, or fail loud.** `git fetch --unshallow` before ANY git-timing instrument. `ko_staleness` (and any
   tool shelling `git log`) gives a **false 0** on `--depth 1`. Fix ready at U-T2-01, pending Matt's key.
2. **link_graph classification gaps (cheap, optional):** (a) skip `about:blank`; (b) don't split hrefs on `'`
   inside double-quoted attributes; (c) treat a trailing-slash target as `<dir>/index.html`. All three would drop
   the 4 examined false-positives to 0 and make the 207→~197 (root-absolute) headline honest. None is a defect.
3. **identity_audit / hash_sweep:** classify an `https?://` catalogue `file` as EXTERNAL, not "missing" — removes the
   3-entry U-01 noise permanently (mirrors classify.py's ethos: name the kind of zero).
4. **NOT_DETERMINED grew 14→16** — two files await a human classify (LL-INST-05 twin: novel architecture is
   human-only). Not urgent.
5. **The estate-`data-timer` and Games-decorative-motion questions** remain the human's open calls (HANDOVER).

---

## DEPLOY-VISIBLE CHANGE SET

**Empty.** No lesson, instrument, `resources.json`, sitemap, or pupil-facing text was changed on this branch. The
only commit is this `_passu/` audit record (FINDINGS.md + PLAN.md), which GitHub Pages does not serve as a lesson.

---

## HAND-BACK ORDER (brief §11.4)

- **Provably better, merged:** *nothing* — there was nothing broken to fix.
- **Waiting on Matt:** U-T2-01 (the `ko_staleness` shallow-guard, one yes/no; fix written and ready).
- **Left alone and why:** everything in REFUSED/DELIBERATE (D1–D12) and every scheduled OPEN item (U-10/11/12) — the
  record already rules them, and re-deciding them is the regression the register exists to prevent.

*Tip SHA intentionally not written here (R-G04): derive with `git log -1` on the branch.*
