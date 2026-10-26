# Instrument Register — LundyLoop

**What this is.** One line per instrument, written when the instrument is written,
committed with the pass it served. Not assembled at the end of a session.

**Why it exists.** The previous register, and every script it described, lived in a
session working directory and did not survive it. The document and its subject were
lost together. A thing that is safe only because of what someone currently has open
is not safe.

**What this register structurally cannot detect.** Everything here agreeing, and
everything here being wrong, are indistinguishable from inside this file. This is a
record of what was intended and what was built. It is not evidence that either was
correct. The only external check is re-deriving a finding by a method that shares no
premise with the instrument that produced it — and where that has been done, the
entry says so.

**Last re-derived at Pass SEMH-1 (LL-INST-14 added)** — the list below matches `tools/` in both
directions: **14 scripts / 14 full `LL-INST` entries, plus 1 QUARANTINED**
(`LL-INST-03-v1`, an entry with no script by design). Re-check it rather than trust it:
`git ls-files 'LundyLoop/tools/*.py' | wc -l` against
`grep -cE '^## LL-INST-[0-9]+ ' INSTRUMENTS.md`. The prior stamp read *6 listed / 6 actual
at `8c384a7`* and went stale silently (R-G03) — which is why the count now travels with the
command that re-derives it, not as a bare number (`bundle_facts.py`, LL-INST-12, is the
runnable form). This stamp is not a mechanism and does not keep the claim true; it makes it
**re-checkable**, which is the achievable version.

**Companion documents.** [`/REGISTER.md`](../../REGISTER.md) — estate conventions,
exceptions, deliberate absences, storage keys, deletion records and the decisions
that constrain what a pass may touch. [`/REBRAND.md`](../../REBRAND.md) — the
staff-pack rebrand procedure. **Load `/REGISTER.md` too**: this file governs how
instruments must behave, `/REGISTER.md` governs what they are allowed to conclude.

**Note on location.** These instruments are estate-wide and belong at the repo root
by the same argument that puts `/REGISTER.md` there. Recorded in `/REGISTER.md`
R-E06 as a decision made and deliberately deferred, so it is not re-asked.

**Loading order.** Any pass that measures the estate loads this file before it runs.
An instrument marked QUARANTINED must not be used, and must not be used to validate
its own replacement (standing rule 6).

---

## Fields

| Field | Meaning |
|---|---|
| ID | Stable. Never reused, even after retirement. |
| Derives | What it outputs. |
| Method | **Literal** (presence only) or **Interpretive** (requires reading meaning). Standing rule 4. |
| Independent of | Which other instruments it does *not* share a premise with. |
| Consumed by | What downstream work depends on its numbers. |
| Status | current / superseded / QUARANTINED |

---

## LL-INST-01 — `hash_sweep.py`

- **Derives:** identical and near-identical file sets across the tracked estate, each member's catalogue status in `resources.json`, catalogue entries pointing at absent paths, and tracked HTML absent from the catalogue.
- **Method:** Literal for exact and normalised hashing and for catalogue membership (path match, percent-decoded). **Approximate** for near-identity (MinHash over 8-word shingles, 128 permutations, seed 20260726).
- **Independent of:** filename-based reasoning entirely — it never consults a name to decide identity. Cross-checked *against* stem similarity, which is the independent method.
- **Known sensitivity limit — declared, not hidden:** the near-identical list is a **floor, not a complete set**. At the 0.60 shingle-Jaccard threshold it did **not** surface `biology/L4_Aerobic.html` ↔ `biology/L4_Aerobic_Respiration.html`, which word-set Jaccard scores 0.763 and sequence ratio 0.914. Shingle Jaccard is far harsher than word-set Jaccard on files that share vocabulary but differ in ordering. Do not quote "N near-identical pairs" as a total.
- **Consumed by:** queue item 6 (hash sweep), item 7 (Respiration twin).
- **Status:** current.

## LL-INST-02 — `link_graph.py`

- **Derives:** resolved inbound-link graph — for any target, which files reference it, at which line, with what visible anchor text; plus in-repo broken links and zero-inbound orphans.
- **Method:** Literal. Resolves every link relative to the *containing file's directory*.
- **Independent of:** LL-INST-01. Content hashing and link topology share no premise; a file can be a byte-identical twin and still be the only one linked, or vice versa.
- **Built to avoid a specific bug:** a bare-basename grep counted `LundyLoop/3_subject_guides/science.html` as an inbound reference to root `science.html`. It reported 1–3 inbound links for files that in fact have zero. That grep is **not** an instrument and must not be reintroduced.
- **Known limit — must be quoted with the number:** "zero inbound" means **zero in-repo**. It cannot see printed QR codes, staff-pack PDFs, bookmarks, or emailed links. Zero inbound is *not* a deletion warrant.
- **Consumed by:** queue item 6, item 7 (Respiration twin delete-or-stub decision).
- **Status:** current.

## LL-INST-03 — `print_pack_audit.py`

- **Derives:** per file, the print slots the JavaScript requests vs the slots the markup provides, in both directions.
- **Method:** Literal on both sides, parsed from two independently-located regions of the file (script body vs markup attributes). Unenumerable variables are reported as UNRESOLVED, never silently counted as satisfied.
- **Independent of:** LL-INST-01 and -02.
- **Externally corroborated:** its count of 5 unsatisfiable slots in `6 Art/Lesson10_SurrealistCollage_HANDSON_v5 (1).html` matches, exactly and independently, the "five print references it can't satisfy" recorded before this instrument existed.
- **Status:** current (v2).

## LL-INST-03-v1 — `print_pack_audit.py`, first derivation — **QUARANTINED**

- **Defect:** hardcoded the tier level names as `('foundation','middle','higher')`. The Art_Teesside suite uses `('supported','standard','stretch')`. Every file using the second vocabulary was reported as missing six slots that in fact exist.
- **Numbers it produced, now retired and unquotable (standing rule 7):** *123 files with at least one absent slot; 691 absent slot-instances.* Both are false. The true figures from v2 are 13 files and 22 slot-instances.
- **Why it was caught:** standing rule 5. 691 was too large and too dramatic to be true of an estate this size, and that implausibility was treated as evidence about the instrument before it was treated as evidence about the estate.
- **Remedy, and why it is not the broken instrument (standing rule 6):** the level names are no longer a premise at all. v2 derives them literally, per file, from that file's own `printPack('...')` call sites. The failure set of v1 was "files whose vocabulary I assumed wrongly"; v2 has no vocabulary assumption to fail on.
- **Status:** QUARANTINED. Do not reuse. Retained here as the record.

## LL-INST-04 — `identity_audit.py`

- **Derives:** both directions of the declared↔actual mapping in one run. FORWARD: does the thing this file claims to be exist? REVERSE: is the thing that is here what it claims?
- **Method:** Literal both ways — magic-byte sniff vs extension, `<title>` vs filename, catalogue entry vs file on disk.
- **Why both directions, and why one instrument:** every one-directional check in this estate has produced a confident wrong answer. Forward-only reported *four subject posters lost*; all ten existed under permuted names. Forward-only on print slots found dangling requests and binned the reverse result — which was the only real defect in the file. Three separate occasions, three one-directional tools. Both are literal presence checks; the failure was never interpretation, it was **direction**.
- **Cannot detect:** a file whose name and content agree but are both wrong; semantic mismatch inside a correct type; intent.
- **Status:** current.

## LL-INST-05 — `classify.py` — **REQUIRED STAGE**

- **Derives:** which print architecture a file uses, *before* anything counts its slots.
- **The completion criterion it enforces, binding on every counting instrument in `tools/`:** an instrument that cannot say **which** kind of zero it found is not finished. `ABSENT` (defect) · `NOT_APPLICABLE` (convention) · `DIFFERENT_MODEL` (solved another way, and I can name which) · `NOT_DETERMINED` (I could not classify this) · `DYNAMIC` (built at runtime, unverifiable statically) · `UNREADABLE` (my failure). Five of the six are not defects.
- **`NOT_DETERMINED` is top-level, deliberately.** Folding "I could not classify this" into `DIFFERENT_MODEL` asserts a positive identification the instrument does not have — the zero rule failing one level up. Fourteen files currently sit there. The honest headline is always *N known defects and M files not established*, never one number.
- **The five false defects that produced it**, all on one subsystem: 691 absent slots across 123 files (hardcoded tier vocabulary) → 12 buttons "wired to nothing" (8 were document-native) → 4 "genuine dead" (3 build at runtime) → 13/0/7 (the dynamic gate, twice wrong) → 7 "dead" including two AQA evidence files (they use `.print-doc` / `.pp` / `.slip`). **Final answer: ABSENT = 0. There is not one dead print control in this estate.**
- **The lesson, and it is not "be careful":** every one of those five was a **vocabulary test wearing a presence test's clothes**. "Does it have `.print-section`" sounds literal but silently assumes the name. "Does the container have content" is presence, and presence does not need to know what the content is called. **Test for the thing, never for its name.**
- **Status:** current.

## LL-INST-06 — `assessed_conditions_gate.py`

- **Derives:** per assessed file, what the Conditions Card AUTHORISES at each tier, what the file actually OFFERS at each tier, and every offer that appears in neither list — the ones nobody has ruled on.
- **Method:** Literal — the Card's allowed/forbidden lists vs the file's per-tier offers. The timing mismatch (LAUNCH's 45 min in a 40-min period) was the **symptom** that first exposed it; the gate searches for the fault, not the tell, because a defect found through a symptom has symptomless siblings.
- **The tell it keys on:** the Card *mentioning* an offer, allowed or forbidden.
- **The sibling it cannot see:** the Card being **silent** about an entire category of offer — silence read as permission (the Route Card survived because no clause discussed timing scaffolds at all). Not fixable in the tool; the Card gains a closed-world line (REGISTER OPEN RULING 1).
- **How to run:** `python3 LundyLoop/tools/assessed_conditions_gate.py`
- **Independent of:** the in-file gates and LL-INST-09 — it reasons over Card↔slide agreement, not over a render.
- **Status:** current. Entry authored at H3 from the instrument's docstring; instrument predates this pass.

## LL-INST-07 — `sitemap_audit.py`

- **Derives:** every URL in the deployed sitemap, and whether it actually resolves.
- **Method:** Literal over HTTP — it tests the claim the sitemap is *ultimately* about ("these URLs resolve"), not the cross-repo artefacts on either side of a boundary no instrument can cross.
- **The tell it keys on:** an HTTP response for each catalogued URL.
- **The sibling it cannot see:** a URL that resolves (200) but serves the WRONG content — 200 is not correctness. When it cannot reach the sitemap it fails loud ("NOT a pass. Nothing below was checked.") and exits non-zero — it never hands back a reassuring number.
- **How to run:** `python3 LundyLoop/tools/sitemap_audit.py [sitemap-url]` (defaults to the deployed sitemap). Needs real network egress; a proxied agent sandbox returns 403 — run it from a machine with egress (HANDOVER "Unrun"; the LL-INST-11 / R-E13 fail-loud family).
- **Independent of:** every repo-internal instrument — it reasons over the deployed site, not the tree.
- **Status:** current. Entry authored at H3 from the instrument's docstring; instrument predates this pass.

## LL-INST-08 — `ko_staleness.py`

- **Derives:** files whose Knowledge Organiser may be stale — the lesson's VISIBLE text moved in a commit *after* the KO block's text last moved, AND at least one moving commit was a CONTENT pass rather than an architecture pass.
- **Method:** Literal/temporal — commit ordering of visible-text vs KO-block movement, each moving commit classified. It asks nothing about correctness and reads no content meaning; staleness is temporal.
- **The tell it keys on:** co-movement timing (body moved after the KO, by a content pass).
- **The sibling it cannot see (stated up front in its own docstring):** a lesson and its KO changed IN THE SAME COMMIT but inconsistently. Co-modification is a proxy for consistency, not consistency itself — files it calls clean are UNCHECKED, not verified.
- **How to run:** `python3 LundyLoop/tools/ko_staleness.py`. Needs **full git history**; on a shallow (`--depth 1`) clone it false-zeros — guard it with LL-INST-11.
- **Independent of:** content-reading instruments; it reasons over the commit graph and visible-text hashes.
- **Status:** current (v3). Entry authored at H3 from the instrument's docstring; instrument predates this pass.

## LL-INST-09 — `loop_mark_print_gate.py`

- **Derives:** per tier (`supported` / `standard` / `stretch`), whether a named element actually reaches paper — by loading the file in Chromium, emulating `media=print`, invoking the file's own `printPack(level)`, and reading back the rendered box, the enclosing section's `.visible` state, and the text of every visible print section.
- **Method:** Literal, but **rendered rather than parsed**. It does not read the `printPack` array and infer. It asks the document what printed.
- **Independent of:** every other instrument here. LL-INST-01..08 all reason over source text; this one reasons over a render, so it shares no premise with any of them.
- **Why it exists, and what it caught.** A static read says *"`feedback` is in the array, therefore the section prints"*. That is a **vocabulary test wearing a presence test's clothes** — LL-INST-05's lesson. This instrument re-derived R-A07 (`print-lundy` absent from all three tier packs) by a method sharing no premise with the static read that first found it.
- **Known limit — must be quoted with the result:** it proves an element is in the print box and in the printed text. It does **not** prove the element is legible, correctly paginated, or that a specific physical printer renders it. Greyscale and glyph-loss are asserted separately, in-page, not by this tool.
- **Consumed by:** Pass LL-G gate 1 (45 files × 3 tiers × 17 assertions).
- **Status:** current.

## LL-INST-10 — `verify_commit_set.py`

- **Derives:** whether a declared **set of commits** is present and carries what it should — commit count between two refs, and per commit the exact paths it touches, checked against emitted manifests. Asserted against `git log`, never against a memory of having built it.
- **Method:** Literal, over the commit graph rather than over file contents. It is the only instrument here whose unit is a *scope*.
- **Independent of:** all of LL-INST-01..09, which reason within a file or a render. This one cannot see inside a file and does not try to.
- **Why it exists — R-F08.** A per-sub-pass cardinality assertion counts files inside its own scope and **nothing counted the scopes**. A commit silently failed to be created; the three sub-passes after it each asserted 15/15/15 and passed. The assertion that eventually fired did so for an unrelated reason. **A scope-level check cannot detect a missing scope.**
- **Exercised against the defect, not just written (standing rule 6):** the set was rebuilt with commit 2 deliberately omitted. All three per-sub-pass cardinality assertions passed 15/15/15; this instrument reported `commit count == 5 · found 4` and refused to check further. **On its first real run it also caught a stale constant in its own declaration** — a path total of 48 carried over from when commit 2 held two files rather than three.
- **Known limit:** it proves the commits exist and touch the declared paths. It does **not** prove the content of a change is correct — that is LL-INST-09's job and the in-file gates'. A green result here plus a green result there is two different claims.
- **Consumed by:** any batched deployment. Run before push, not after.
- **Status:** current.

## LL-INST-11 — `preflight.py`

- **Derives:** a shared guard — each instrument declares the external dependency it rests on (full git history, a reachable host, a corpus of the expected size), and this FAILS LOUD (stderr, non-zero exit) when one is absent, instead of returning a plausible number.
- **Method:** Literal precondition checks. A guard's whole job is to stop the run, not be caught and swallowed.
- **The tell it keys on:** the presence or absence of a *declared* external dependency.
- **The sibling it cannot see:** a dependency the caller never declared — it checks only what each instrument tells it to, so an undeclared assumption stays invisible (the false-zero class it exists to prevent, one turn out). Built by Pass X from Pass U's finding: `ko_staleness` returned "0, all clean" on a shallow clone and did not fail loud.
- **How to run:** imported by other instruments (its helpers), not a standalone report.
- **Independent of:** the instruments it guards — it is the shared dependency-declaration layer beneath them.
- **Status:** current. Added by Pass X; entry authored at H3 from its docstring to close the census.

## LL-INST-12 — `bundle_facts.py`

- **Derives:** one dated OBSERVATION RECORD of the estate's standing figures — each figure beside the exact command that derived it, stamped at HEAD. A figure it cannot trust prints `NOT_DERIVED` with the reason (a truthful null, never a guess).
- **Method:** Literal — `git grep` / `git ls-files`, read-only by construction (prints to stdout, writes nothing, stages nothing). Emits both sentinel forms per R-E10, so a marker quoted in `5_staff_training/` would show as diverging forms.
- **The tell it keys on:** literal marker strings and git-tracked file extensions.
- **The sibling it cannot see:** same-purpose content under other wording; uncommitted working-tree state (it reads HEAD); and whether any counted thing is CORRECT — it bundles cardinalities, not judgements. Its INSTRUMENTS-entry heuristic keys on `## name.py` headings, so it prints `NOT_DERIVED` against this file's `## LL-INST-NN — name.py` format — an honest null; this enumeration is authoritative.
- **How to run:** `python3 LundyLoop/tools/bundle_facts.py` (no args).
- **Independent of:** every judgement-based instrument; it emits counts, not verdicts. A number a script prints when it runs cannot go stale — the R-G03 / R-E08 lesson made runnable.
- **Status:** current. Placed and run read-only at `51d14aa` (H2).

## LL-INST-14 — `semantic_integrity_check.py`

- **Derives:** whether a lesson's surfaces agree **with each other** — subject, week, deck title vs knowledge-organiser title, the success criteria quoted by the midpoint peer-check and the completion summary, the next-lesson pointer, the timer contract, and house tier vocabulary. Every expectation is read out of the file under test; the title index used by the pointer check is recomputed from the corpus each run.
- **Method:** Literal, over source text. Strips data-URIs before any measurement (200 tracked `*.html` carry base64 blobs at `6aaffb7`).
- **Why it exists:** every other instrument here proves a lesson *works*. None can see a lesson that works perfectly while teaching the wrong message. All six `BUILD_DT` decks passed every technical gate while their midpoint quoted `CAREERS_W1_My_Strengths`' success criteria, their completion summary ticked a Careers criterion, and their next-lesson pointer sent pupils to `CAREERS_W2`. A technical pass is not evidence the wording is correct.
- **The tell it keys on:** a success criterion quoted in a *quoting* surface (`.mp-prompt`, `.lc-summary`) that does not appear in the deck's own outcome surfaces; and a next-lesson pointer naming a deck title that lives in another module folder.
- **Exercised against the defect, not just written (standing rule 6) — and it failed twice before it passed.** Replayed against `BUILD_DT_W2_Blueprint.html` at `main`, where the defect was already proven: (1) it reported **clean**. The ground truth was derived from the whole file, so the pasted criterion was part of its own evidence — a self-referential false negative. Excluding the quoting regions fixed it. (2) It then reported the *repaired* files as defective. The criterion regex ran over tag-stripped text, where `<` no longer delimits, so adjacent criteria ran together and nothing ever matched. Extracting from raw HTML fixed it. **Neither bug was visible from the instrument's own output — only the replay found them.**
- **Independent of:** LL-INST-01 (hashing), -03 (print-box membership) and -09 (render). Those reason over bytes, boxes and layout; this one reasons over whether two authored copies of one fact agree. A file can be byte-unique, print-complete, render-clean and still teach another lesson's outcomes.
- **Known limits — must be quoted with the result:** it cannot judge whether a deck's own outcomes are pedagogically *right*, only that the surfaces quoting them agree; it cannot see a paraphrase; it does not measure print geometry (that needs 718×1047 in a browser-capable environment, rule 26); and when two surfaces disagree it reports the disagreement without deciding **which copy is stale** — that is a human read. In `BUILD_ART_A2` the correct copy turned out to be the midpoint and the stale pair the objectives slide and completion summary, the opposite polarity to `BUILD_DT`.
- **SI-07 is REPORT-ONLY by construction.** Estate timer values are Matt's call (`HANDOVER.md`, "The human's open calls": *"No session edits timers in passing"*), and the authorisation `Fix the timer contract — go` is awaited. The check names the contradiction and never licenses an edit.
- **How to run:** `python3 LundyLoop/tools/semantic_integrity_check.py` (estate-wide report) · `... <path>...` (named files) · `... --json`.
- **First estate run, Pass SEMH-1 at `6aaffb7`:** 503 files scanned, 192 lesson decks recognised, **84 findings across 50 files** (unit: findings, not files) — SI-04 15 · SI-05 10 · SI-06 1 · SI-07 58 (24 critical). The 24 SI-07 criticals reproduce the recorded 24-file Art timer set **exactly**, by a method sharing no premise with the browser harness that first found it — a second independent signal.
- **Status:** current. Added by Pass SEMH-1.

## LL-INST-13 — `patch_loopmark.py`

- **Derives:** a dry-run manifest of which named target files would receive the BUILD loop-mark block ported from a donor (`would-patch` / `skip-reason`), asserted to sum to the targets given. DRY-RUN by default; writes only with `--write`.
- **Method:** Literal — locates the donor's marker block and its structural anchor (the nearest preceding `id`), inserts by position, confirms by marker text, and FAILS CLOSED on any doubt (a file is never modified on a guess).
- **The tell it keys on:** the marker string `ll-g:loop-mark v1` plus the donor block's structural anchor.
- **The sibling it cannot see:** a closure block already present in a target under DIFFERENT wording or a different marker version — the idempotence check keys only on the exact v1 marker, so a same-purpose block in other words is invisible (the LL-E lesson) and would be double-inserted.
- **How to run:** `python3 LundyLoop/tools/patch_loopmark.py --donor <build.html> <target.html …>` (add `--write` to apply). Refuses targets outside `Build/`, and refuses assessed / `LundyLoop/` / `tools/` paths.
- **Independent of:** the closure it ports — it moves a block, it does not judge closure. Its marker string is inert to the sentinel derivations (`-- '*.html'`, R-E10).
- **Status:** current. Placed at `51d14aa` (H2); dry-run verified read-only — fails closed on all six `Build/` donors (no preceding `id` to anchor on), writing nothing.

## Fixes applied to existing instruments

- **LL-INST-01 `hash_sweep.py` — extension blindness, fixed.** v1 chose near-identity candidates by file extension, *in a repo whose defining defect is that filenames lie*. It never tested `Head_Office_Summary.pdf` (HTML) or `weekly_loop_log.csv` (HTML), so two displaced copies were invisible to the instrument that exists to find displaced copies. Now sniffs content.
- **LL-INST-03 `print_pack_audit.py` — now calls `classify` as a required first stage** and reports what it classified out, so a zero never leaves the tool unlabelled.

---

## Blind twins — what each instrument's tell hides

**The rule this section exists for:** *a defect found through a symptom will have
symptomless siblings.* The symptom is what made the defect **findable**, not what
made it a **defect**. LAUNCH W7's Route Card was found because 45 minutes didn't fit
a 40-minute period. GROW W7 had the identical breach at 39 minutes — correctly
sized, therefore silent, and it would have sat there indefinitely. **A plan that fits
its period looks finished.**

Every instrument here keys on a tell. Each therefore has a twin it cannot see. The
third column is the one that saves work: **some twins are reachable and some are
structurally out of reach**, and nobody should spend a week building a detector for
something no detector can find. That is the zero rule — *absent / not applicable /
undetermined* — applied to instruments instead of files.

| instrument | the tell it keys on | the twin it cannot see | reachable? |
|---|---|---|---|
| **LL-INST-01** `hash_sweep` | byte-identity, or shingle similarity above threshold | a copy that diverged **just past** the threshold; and a file that is semantically the same lesson but shares no text | **Partly.** Threshold twins are reachable by lowering the threshold and reading the extra pairs — that is how `L4_Aerobic` ↔ `L4_Aerobic_Respiration` was found, below the cut but 0.763 by word-set. The no-shared-text twin is **out of reach**: there is nothing to compare. |
| **LL-INST-02** `link_graph` | a link written as a literal attribute that resolves to a tracked path | links built at runtime by string concatenation (`${href}`); and every inbound link from **outside** the repo — printed QR codes, staff-pack PDFs, bookmarks, emails | **Genuinely unreachable — this one does mean stop.** A printed QR code on a classroom wall is unknowable in principle; no instrument and no inspection recovers it. This is why *zero inbound* is never a deletion warrant. |

**Two kinds of unreachable, and only one means give up.** *Unreachable by instrument*
means the method is looking rather than measuring — the poster case proves it works.
*Unreachable in principle* means the information does not exist anywhere accessible.
Do not read the first as the second.
| **LL-INST-03** `print_pack_audit` | a slot the code **requests** that the markup does not provide | a slot that is **present and empty** — the shell exists, the pack prints, the page is blank | **Yes, cheaply.** Measure text length inside each slot, not just its existence. Presence of the element is not presence of content. **Not yet built.** |
| **LL-INST-04** `identity_audit` | extension and content **disagreeing** | a file where extension and content **agree and are both wrong** — a correctly-named `.png` showing the wrong subject | **Unreachable by instrument, reachable by inspection.** No second surface exists to compare, so no comparison can find it — but a person opened ten permuted posters and identified every one by eye. This does not mean stop; it means the method is looking, not measuring. |
| **LL-INST-05** `classify` | matching a print architecture already known to the module | a genuinely novel architecture | **Reachable, but only by a human.** It returns `NOT_DETERMINED` rather than guessing — honest, and not the same as understanding. 14 files sit there now. |
| **LL-INST-06** `assessed_conditions_gate` | the Card **mentioning** something, allowed or forbidden | the Card being **silent** about an entire category of offer. The Route Card survived because no clause discussed timing scaffolds at all — **silence read as permission** | **Not fixable in the tool.** See below. |

### The gate's twin was repaired in the artefact, not the instrument

This is the transferable lesson, and it is the more useful half of this section.

No improvement to `assessed_conditions_gate.py` could decide an offer its Card never
mentions, because the information required is **absent from the document**, not
merely hard to extract. The repair is to change the artefact:

1. **Closed-world Card** — *"anything not named above is not allowed"*. Converts
   silence from permission-by-default into prohibition-by-default, which is how
   assessment conditions work everywhere else: permitted materials are enumerated,
   not excluded.
2. **Declared authorisation** — every tier-offer names the Card clause that permits
   it (`authorised-by: supported-frames`). The gate stops doing string similarity and
   starts asking three exact questions: does this offer name a clause · does that
   clause exist · does it permit this?

Together they make the gate decidable **in both directions**, and they retire the
false-positive class the heuristic produces. Evidence that the heuristic needed
retiring rather than tuning: `GROW Supported` was flagged as unmentioned while being
**word-for-word correct** against its Card — a human reads *"Opening Frame / Close
Frame"* as matching *"the opening and close frames"*; a token comparison does not.

**When a blind spot is caused by missing information rather than weak extraction, fix
the document.** A better instrument cannot read what was never written down.

### A seventh tell, outside the instruments

`refs/remotes/origin/main` in a working copy is a **cached claim about a remote**,
and nothing keeps it true. Pushing to an explicit URL rather than to the named remote
leaves it stale — silently, every time, all session. Its twin is **any other local
artefact asserting something about a different artefact with no mechanism binding
them**, which is the dominant failure shape of this entire programme. Enumerated
separately in `/REGISTER.md`.

**Fetch after every push.** That keeps the claim re-observed, and keeps the token out
of `.git/config`, which pushing to a token-bearing `origin` would not.

---

## Standing rules this estate earned, that govern instruments

1. **Report every category you compute, including the ones nobody asked about.** A discarded output is worse than an uncollected one: the work was done and the answer thrown away. A brief that names an expected finding narrows what can be reported — name the question, not the answer.
2. **Any point where data changes medium is a derivation.** Tool output into prose, screen into manifest, a number leaving the thing that produced it and being retyped. Each needs the same assertion as any other. **Emit, don't transcribe.**
3. **Any message stating a count and printing a list compares the two before it is sent.** One assertion, no judgement.
4. **Any change to a classification comes with a re-asserted total in the same message.** A moved bucket without a new sum is a table that looks verified and isn't.
5. **Check plausibility before the number leaves the tool**, not after it reaches a report. That is a design, not advice.
6. **A test that can pass without exercising the thing under test proves nothing.** A no-op push does not prove write permission; a control case that was never going to fail does not validate an instrument.
7. **In this estate a filename is a hint, never a fact.** Derive from content, path and catalogue. Never bucket, scope, route or assert on a name. Seven independent cases: a `.pdf` that is HTML · ten permuted posters · four `.png` files containing text · `Chem_` on a biology-sequence file · `L4_Aerobic` beside `L4_Aerobic_Respiration` · meaningless `(N)` suffixes · a Careers file named W6 carrying W7.
8. **"The X file" is an unverified singleton.** Any item with a definite article inherits a count nobody derived. Re-ask it as a query before acting.
9. **Every raised concern gets an explicit disposition** — confirmed, withdrawn, or closed with the reason. Findings do not get to evaporate.
10. **Every deletion pass records what was removed, why, and the SHA of the commit immediately before it.** A deletion nobody wrote down is irreversible in practice, because recovery depends on knowing to look and knowing where.
11. **A declaration binds only when what it asserts is verifiable inside the artefact that makes it.** Everything that failed here claimed something about elsewhere — an approval held by a centre, a deploy in a dashboard, keys in other files, scripts in a container that had ended. When a claim points outward, a sentence is not enough; it needs a test, and until it has one it is decoration.
12. **An inherited control is not a chosen control**, and nobody audits what they don't know is governing them.
13. **An animated property read at the wrong moment is not a measurement.** Never read computed style synchronously after adding a class — the animation has not started, so you read the pre-animation value and record a pass. And never measure an animated property on a hidden slide: Chromium does not start animations inside a `display:none` subtree, so everything reads as inert whether it is gated or not. Show the slide, wait past the longest animation, *then* read. Both halves were learned the same afternoon: a gate check measuring `[data-shown]` instead of computed opacity reported green through a build where every label was readable, and its first repair still passed because it measured at load. The census that found this then reproduced the synchronous-read error inside itself, on its own first probe.
14. **Call it a FALSE ZERO.** `preflight.py` named this family before any audit did, and its wording is the canonical one: *"a FALSE ZERO from an under-specified check is the most expensive defect class: it CLOSES a question that was never examined."* Use that phrase. An auditor's fresh coinage for a thing the estate has already named costs everyone a translation, and this estate has now twice been right by convention while a fresh audit's priors were wrong — the print subsystem (R-E05) and this. **Read the registers before forming an expectation; they are cheap and they are evidence.**
15. **Fix at the gate, never at the call site.** A gate hardened against a whole mechanism is immune to an incomplete enumeration of what could defeat it; a patched call site is only as good as the list of attackers you happened to find. **Three sightings, one family: a new rule landing at higher specificity than an existing gate defeats the gate silently.** `.g-in`'s held final keyframe beat a plain `opacity:0`, so every label in the observation engine was readable at load. A private class took the name of a shared verb and shadowed it. And `.slide.wedo2-layout { display: grid }` beat the deck's own `.slide { display: none }`, so a slide that should have been hidden shared the flex row with whichever slide was showing — measured: every other slide's width halved from 742px to 403px and every picture collapsed to its floor. Each was invisible in the artefact and visible only to a check that asserted the gate's own outcome (`test/gate-shape.js`, `reports/convergence/tests/displaygate.mjs`). This was load-bearing: the fill-mode census scanned five stylesheets and later turned out to have missed inline `style=` attributes, longhand `animation-fill-mode` and deck-level `<style>` blocks. The gates held anyway, because they were hardened rather than patched. Do not "simplify" a gate fix back into a call-site fix — the incompleteness it protects against is permanent and unmeasured.
16. **A check that can return zero must first prove its input set was non-empty.** Straight from `preflight.py`: it is not enough to iterate and find nothing; the instrument must assert that there was something to iterate. A count of zero and an empty corpus are indistinguishable from inside the result.
17. **A fact repeated across documents has been copied, not verified. Re-derive it at its source before acting on it.** Repetition is not corroboration; copying is how a false zero survives, because it closes a question nobody re-opened. Three sightings in one day. A PR-stacking claim originated in one session's report, was carried into two briefs and a ledger, and read as established by its third appearance — while git said all four PRs based on `main`; #13's body claimed a stacking git did not have, so its diff carried #10's whole changeset, **11 commits / 35 files / 5,520 additions against 8 / 26 / 1,049 once re-pointed.** A brief routed a finding to "the RM programme's own register", which did not exist at any path. And a backlog count of 27 instruments was carried unverified until the census derived it — the one case where the transition is recorded rather than hidden, in `reports/INSTRUMENT_INDEX.md` §2 IDX-2.
18. **Instruments that disagree are evidence. Investigate the discrepancy — never average it, never pick the more convenient one, never call it noise.** Two probes differed by 37px on one cell. Chasing that difference rather than resolving it found `paint()` opening with `if (!st || !bar) return;` while a later pass had appended `fit(stage);` to its tail — so every stage carrying `data-grow-nobar` was never fitted and depended on an async `ResizeObserver`, which is a visible reflow in the room and invisible to any synchronous check. Nothing else in the session would have caught it.
19. **A document that argues with itself is worse than one simply out of date.** When a correction lands, remove what it contradicts rather than appending beside it. A reader cannot tell which of two contradictory claims is the live one, and will reasonably pick the one that suits them.
20. **A target metric moving the right way is not evidence the change is correct — it can improve for the wrong reason.** Measure the thing you changed, first. While the `.wedo2-layout` display collision was live, the slide-overflow numbers being optimised *improved*; the defect surfaced only as unrelated stages failing a different check. The slide's own width was the last hypothesis tested and should have been the first.
21. **Green PRs do not sum to a green main. Verify on merged main, not on the sum of the branches.** A defect can exist only in the combination, belonging to no PR and visible to no per-PR check. Six PRs landed together on 1 August; `Science_Teesside/launch-engine/dist/grow-motion.min.css` was stale the moment two of them were both on `main` — **pinned `db3fd9602a69eb20`, actual `83bdca2c9898413e`** — because #10 pins each `dist/` source's SHA-256 while #12 changed `grow-anim/grow-motion.css` for an unrelated fix. Neither PR was wrong and neither could have caught it. It took its own change (#15) to close, and post-merge verification to find at all.
    **The mechanism is the actionable part: the pin did its job.** A generated artefact pinned by the *content hash* of its source turns a silent divergence into a hard failure at the next check, whatever order the changes arrive in. Build order, review order and merge order are all assumptions; a content hash is not. Pin generated artefacts by source hash rather than trusting that whoever changed the source will remember the artefact.

22. **A search-based census must carry a positive control known to exist, or its zero is unreadable.** Without one, *clean* and *blind* return the same answer. GitHub's `search_code` was asked whether the `Lessons` or `Games` repos referenced the site's `mbm-features.css` before 57 selectors were deleted from it. It returned `total_count: 0` with `incomplete_results: true` — which reads as "no dependencies, safe to delete". The instrument was then asked for a term certain to exist in the repo the search was standing in. **It returned 0 for that too.** The tool was not indexing those repos at all, so every zero it had produced was a false zero wearing a number. The question was re-answered with shallow clones and a `raw.githubusercontent.com` fetch, each validated the same way first: the raw fetch was trusted only after a known-positive control returned 2 hits. Final population, honestly obtained: **1,007 sibling-repo files scanned, 0 dependencies.** A control costs one query. Skipping it costs the whole census, silently.

23. **Anything downstream of a blocked origin is UNKNOWN, not absent. Enumerate what the environment blocks before reporting any zero that depends on it.** A dead-CSS census across 101 selectors × 26 pages reported 73 with zero matching elements anywhere, and 73 is a number that invites deletion. **Four of them were alive.** `.mbm-row`, `.mbm-track`, `.mbm-fill` and `.mbm-num` build the stats leaderboard, which only renders *after* `api.counterapi.dev` replies — and the container's proxy blocks that origin. They looked dead because the network was down, not because nothing used them. Re-running with the counter **stubbed to a success response** brought all four straight back, and the same reasoning saved every conditional-state selector beside them (`.is-you`, `.mbm-board-empty`, `[data-ready]`, `:empty::before`), which the stub happened not to trigger. Deleting on the first number would have shipped a broken leaderboard under cover of a green census. This is R16 with a specific and very common cause: the empty input set was created by the environment, not by the code.

24. **A promotional claim is a claim surface, and every number on it is derived, never typed.** Marketing copy leaves the repository and cannot be corrected in place; a wrong number in a video description outlives every fix. This estate has already shipped **"twenty-eight" beside "30 of 30"** in the same artefact. Every figure that reached the launch film — 15 lessons, 5 weeks, 48 cards, 7 leagues, 16 nations, 0 of 27 pages setting a cookie — was computed from the files being described, at build time, and the one fact taken from a grep instead of the rendered page was wrong: the LAUNCH biology decks were read as **AQA** because `AQA` appears in all fifteen, when the rendered badge says **Pearson Edexcel GCSE Biology 1BI0 Foundation** and every `AQA` hit was the phrase *"AQA UAS science units"* — the Unit Award Scheme link, not the exam board. Caught by reading a screenshot, one step before it went on screen.

25. **A census returning a non-zero count must have every hit individually classified, not merely counted. A count is not an inventory.** R16 and R22 protect against a *false zero* — a question closed without examining its input set. Nothing protected against the mirror image: a **false non-zero**, where the search returns hits, the hits get counted, the count gets reported, and no one ever opens them. It is more dangerous than it looks, because a non-zero result *feels* like evidence of work done.

    **Provenance, two sightings in one pass.** A census of FormSubmit endpoints across four repos reported **4 distinct endpoints**. There is **one**. The regex had captured trailing markdown punctuation — a backtick and a full stop — from documents *quoting* the URL, so `…gmail.com`, `` …gmail.com` `` and `…gmail.com`. counted as three separate endpoints. A four-endpoint estate and a one-endpoint estate call for completely different work.

    The same pass then did it again while writing this rule. A `mailto:` census reported the file count rising from 20 to 23 while occurrences stayed flat — arithmetically impossible for three genuinely new files. `grep -rl` output had been split on **whitespace**, so the Lessons path `5_6 Local Choice/` became three phantom "files" with zero hits each. Re-run with `grep -rlZ` and NUL delimiters: **21 files**, and the real delta was a single line in a report quoting the string.

    **The practical form:** print the hits, not the tally. If the list is too long to print, classify it into buckets and print the bucket counts *with one example each* — and make the buckets exhaustive, because summing two of three buckets is how the second sighting above got its wrong file count. Prefer `-Z`/NUL delimiters over whitespace splitting whenever paths are involved; this estate has directory names with spaces in them.

26. **This container has no browser and no direct network; browser evidence comes from CI or it does not exist.** Managed Chromium blocks every navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`, including `localhost` and `file://`; direct DNS/network requests fail before reaching the host. `jsdom` is a DOM stub, not a browser, and any result derived from it says so in the same sentence. A gate requiring layout, input, WebGL, media emulation, print geometry or real navigation runs in GitHub Actions or another browser-capable environment. If it does not run there, the result is **UNVERIFIED**, never inferred from source or jsdom.

### Session-close record — Art Teesside browser and print gates, 3 August 2026

- **STATUS:** OPEN DIAGNOSIS. No lesson content was changed, and neither PR was merged.
- **Lessons PR #26**, head `4eb3e5ec2e2467ada785e391dfc04891d0f40cc8`: the static/content/instrument job passed. Chromium completed **140/140 page-and-viewport executions** across 35 entry points and four viewports; the deep run completed 31 lesson executions, with the seven A2 lessons passing and the remaining 24 failing one timer contract. Reduced-motion checks passed 3/3. Overall browser result: **174 checks, 24 failed**. The 718 × 1047 print assertion and its positive control were skipped after the browser exit, so print executions = **0** and print is **UNVERIFIED**.
- **R25 classification of all 24 failures:** every file has the same complete source signature — initial `#timerDisplay` text `20:00`; Independent Work `data-timer="20"`; `timerTotal=900` and `timerLeft=900`; and `resetTimer()` assigns `timerLeft=timerTotal`. The reset body and configuration declaration are byte-identical across the 24. No pair differs on the timer cause.

  - BUILD: `BUILD_ART_W1_The_Local_Canvas.html`; `BUILD_ART_W2_Artists_Makers_and_Teesside_Connections.html`; `BUILD_ART_W3_Industrial_Surface_Skills_Lab.html`; `BUILD_ART_W4_Build_the_Brief.html`; `BUILD_ART_W5_Critique_Test_and_Redirect.html`; `BUILD_ART_W6_Resolve_the_Artwork.html`; `BUILD_ART_W7_Curate_the_Showcase.html`; `BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html`.
  - GROW: `GROW_ART_W1_The_Local_Canvas.html`; `GROW_ART_W2_Studio_Skills_and_Safe_Practice.html`; `GROW_ART_W3_Independent_Studio_Challenge.html`; `GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html`; `GROW_ART_W5_Practitioner_Career_and_Inspiration.html`; `GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html`; `GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html`; `GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html`.
  - LAUNCH: `LAUNCH_ART_W1_Frame_the_Local_Challenge.html`; `LAUNCH_ART_W2_Practice_Careers_and_Pathways.html`; `LAUNCH_ART_W3_Implement_and_Critically_Develop.html`; `LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html`; `LAUNCH_ART_W5_Design_the_Leadership_Project.html`; `LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html`; `LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html`; `LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html`.

- **Defect class:** two authored copies of one timer fact disagree. The initial display and 20-minute slide metadata say 20 minutes; the independent timer source of truth and reset path say 15 minutes. The approved repair shape, if authorised, is derivation: render the initial display from the configured duration and assert `initial display == configured reset`. Editing `20:00` separately in 24 files would preserve the defect class. Authorisation awaited: `Fix the timer contract — go`.
- **Lessons PR #30**, head `f3133625fe2d6aed7088e27579fc47d6e60be920`, is validation-only and must not merge. Run `30829030929` has a tooling race: the HTTP server was backgrounded and probed immediately; `curl` exited 7, so browser and print both ran **0** times. The repair is bounded readiness polling, not a fixed sleep. Run `30829029533` verified the patch checksum and expected publication head, then `git apply --check` failed at `Art_Teesside/tools/assert_visual_browser.js:349`; no commit or push occurred. The patch must be re-derived against the current head, never forced.
- **Print verdict on both PRs:** 718 × 1047 executions = **0 on #26 and 0 on #30**. Skipped means **UNVERIFIED**, not passed.

## HANDOVER — Apex Golf orchestration close, 3 August 2026

- **Authorisation ledger:** `Merge MattRoper1977/Games#6 — go` was given and consumed; `Delete branch codex/apex-golf — go` is withheld; `Fix the timer contract — go` and `Apex Golf design — go` are awaited.
- **Open Art defects:** Lessons#26 remains red on the 24-file two-copies-of-one-timer contract and has no print result. Lessons#30 is validation-only and remains red on the bounded-readiness tooling race and the stale patch; it is not for merge.
- **Browser environment:** this container cannot produce browser evidence and has no direct network. Apex Golf gates G4, G5, G9 and G10 therefore run in the game’s committed GitHub Actions workflow or another browser-capable environment; otherwise they remain unverified.
- **Arcade 42 versus 31:** `/Games/games.json` is the only game data source and contains 31 entries. The Arcade’s 42 `.gcard` components are 31 whole-shelf cards plus 11 deliberate repeat placements from that same manifest: seven themed-grid repeats (`Orbital`, `Marble`, `Trail Runner`, `Trekkers Trail Runner — Tees Coast`, `Grid Chase`, `Neon Garden`, `Neon Siege`) and four classroom-favourites repeats (`Kids vs Staff: Showdown`, `World Cup: Road to the Three Lions Final`, `World Cup v3 — Match Director`, `World Cup v5 — Showdown`). There is no second catalogue source.
- **Apex Golf:** remains unstarted by design. No `apexgolf/` path, build branch, game commit or PR was created. The empty Lessons branch `codex/apex-golf` is deliberately retained.

---

## Seed conventions carried forward

These are decisions, not scan results, and belong in the exception register proper
(queue item 1). Listed here so they are not lost twice.

- The two assessed files' declared absences.
- The 56 BUILD files deliberately lacking the writing line.
- The **I Do** convention: no print counterpart, deliberately, because it is modelled live.
- The **Arrival** convention: settling routine the adult runs.
- The deliberately identical Standard/Stretch rows.
- `coldCall_y10` → `ps_coldcall_roster` migration state, and the deliberately estate-wide shared keys.
- The superseded Surrealist Collage file.
