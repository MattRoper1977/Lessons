# REGISTER — estate conventions, exceptions and decisions

**Scope: the whole repository.** Not the Lundy Loop pack, not one subject folder.
This file lives at the repo root because a control that isn't found isn't a control,
and a pass working on Games or Art has no reason to open `LundyLoop/`.

**Last observed true at** `35efefd`. Every count below carries the commit at which it
was checked. The stamp is not a mechanism and does not keep a claim true — it makes it
**re-checkable**, which is the achievable version. A claim that names when it was last
observed can be re-observed; one that does not, cannot.

**Load this before any pass that measures, patches or deletes.**
Companion documents: [`REBRAND.md`](REBRAND.md) — the staff-pack rebrand procedure ·
[`LundyLoop/tools/INSTRUMENTS.md`](LundyLoop/tools/INSTRUMENTS.md) — the instrument
register and the standing rules that govern instruments.

---

## What this register structurally cannot detect

Stated first, because a register that only lists what it knows reads as complete.

- **Everything here agreeing and everything here being wrong are indistinguishable
  from inside this file.** No internal comparison can catch it. The only external
  check is re-deriving an entry by a method sharing no premise with the one that
  produced it — and where that has been done, the entry says so.
- **It is built from decisions, not scanned from the tree.** A scanned register can
  only ever hold odd-one-out cases. That is deliberate, and it means the register
  cannot know about a convention nobody wrote down here.
- **`VERIFIED` means verified at the stated commit, not permanently.** State is not
  property. `identity_audit.py` reported zero self-misdescribing files today; a
  single browser upload reintroduced eleven once before.

---

## How to read an entry

```
ID          stable, never reused
STATUS      CONVENTION | DEFECT | HANDLED-ELSEWHERE | OPEN | RETIRED | RECORD
VERIFIED    <commit> — re-derived from the files at that commit
DECLARED    stated by Matt and NOT re-derived here; treat as unverified
SELECTOR    the literal query that identifies the affected files, if one is safe
```

`SELECTOR` matters more than it looks. Several entries below exist because the
obvious selector returns the wrong set.

---

## A · Deliberate absences — things missing on purpose

### R-A01 · The two assessed files
- **STATUS** CONVENTION · **VERIFIED** `d02ec43`
- **Files** `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html` ·
  `Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html`
- **Rule** Support access may be changed. **Content, outcomes and success criteria
  may not** — ask first, every time.
- **TWO SELECTORS, ONE PER DIRECTION. Both are correct; neither replaces the other.**

  | selector | returns | use it for |
  |---|---|---|
  | `★ ASSESSED LESSON` | **2** | **INCLUSION** — scoping a pass *onto* the assessed files |
  | `★ ASSESSED` | **6** | **EXCLUSION only** — keeping a pass *away* from anything assessment-related |

  The broader string is *correctly* broader for its job: a pass avoiding assessed
  material should also avoid the two Printable Packs, which generate the Week 7
  pupil ticket, and the two Schemes of Work, which describe it in prose. Those four
  carry the marker as a **reference**, not a designation.

  **Never use `★ ASSESSED` for inclusion.** A pass scoping on it to *find and edit*
  the assessed files reaches into the Printable Packs and changes what a pupil sits.

### R-A01b · A selector's safety depends on the direction it is used in
- **STATUS** CONVENTION — read before writing any selector
- **Over-broad is safe for exclusion and dangerous for inclusion. Under-broad is the
  reverse.** Nothing about the string changes; the hazard appears the moment the
  direction flips.
- `★ ASSESSED` survived because it had only ever been used to keep passes *out* —
  quarantining four files instead of two costs nothing.
- Second independent instance: **bucket A** (R-C04) — safe as a list, dangerous as a
  criterion. Two instances from unrelated parts of the estate, so this is a property
  of selectors, not a coincidence.
- **Record both directions with every selector**, rather than replacing one with a
  single "right" answer. A lone narrow selector gets re-broadened by the next person
  who finds a case it misses.

### R-A02 · BUILD files without the LL-3 writing line
- **STATUS** CONVENTION · **VERIFIED** `7226b08`
- **SELECTOR** the literal string `What I said, and what it changed`
  *(strip data-URIs before matching — standing rule 10).*
- **POPULATION, derived literally rather than guessed:** the LL-3 population is the
  **union of the five commits that created it** — `8dc6abc` (30) · `12ecf55` (29) ·
  `8f43cea` (18) · `4d574ff` (26) · `d5294e9` (5) = **108 files, all still at HEAD.**
  This is a presence derivation from the commits, not a word-match over the tree.
  *(A four-zone word match returns 166 and is over-broad — it catches the LundyLoop
  pack itself, subject index pages and the schemes of work. Do not use it.)*

  | | files | where |
  |---|---|---|
  | **carry** the writing line | **48** | `GROW_ASDAN` 18 · `Art_Teesside` 16 · `Grow` 7 · `Launch` 7 |
  | **deliberately lack** it | **60** | `BUILD_ASDAN` 31 · `Art_Teesside/Build` 15 · `Build` 14 |
  | population | **108** | 48 + 60 = 108, cardinality asserted |

- **Independent check:** zero files anywhere in the estate carry the marker from
  outside the population. The string is exactly co-extensive with the pass that
  wrote it — so the selector cannot be over-matching.
- **The figures previously carried were 47 and 56. They are 48 and 60.** Both moved
  when LL-3e added the five lessons LL-3a–d silently missed. Retired.
- **The truthful null is already built into the line**, and any LL-5 gate must not
  re-invent it: *"Saying it aloud starts the loop; writing it is what closes it.
  **Pass is always allowed.** What I said, and what it changed:"*

### R-A03 · The **I Do** convention
- **STATUS** CONVENTION · **DECLARED**
- I Do has no print counterpart **deliberately** — it is modelled live. Absence of an
  I Do print slot is never a defect. `print-ido` was absent from 162 of 166 files and
  was reported as a gap once already.

### R-A04 · The **Arrival** convention
- **STATUS** CONVENTION · **DECLARED**
- A settling routine the adult runs. No pupil-facing artefact is required.

### R-A05 · Deliberately identical Standard / Stretch rows
- **STATUS** CONVENTION · **DECLARED**
- Where a Standard and a Stretch row read the same, that is a decision, not a
  copy-paste error. **Do not "fix" by differentiating.** Note this sits in tension
  with the tier-variance content rule (*any line describing what a pupil must produce
  is tier-variant until proven otherwise*) — the tension is deliberate and the
  exception wins where it is declared.

### R-A06 · Declared print-light lessons
- **STATUS** CONVENTION · **VERIFIED** `d02ec43`
- `6 Art/Lesson10_SurrealistCollage_HANDSON_v5 (1).html` is a hands-on making lesson
  with **no pupil worksheets by design**. Two targeted print controls only — an image
  bank (consumable, per pupil or pair) and a mission card (reference, per table).
  Separate runs, different quantities: **do not merge them into one pack.**
- **Do not author worksheet sections into it.** The worst available outcome on this
  file is a parity pass turning a making lesson into a paperwork lesson.
- **SELECTOR** `printPack` defined but never called from the UI → 2 files today
  (this one, plus `biology/Testing Breath - FINAL Observation Lesson (1).html`, where
  it is vestigial beside a bespoke print UI). Re-run the query rather than trusting
  the count.

### R-A07 · `print-lundy` is in the markup and not in the print pack
- **STATUS** RECORD · **VERIFIED** `3e2b99d` — re-derived by two methods sharing no premise
- **The zero is `DIFFERENT_MODEL`, not `ABSENT`.** Nothing is missing from delivery.
- `printPack(level)` enumerates `['ko','intro','arrival','starter','wedo','exit',
  'witness','feedback']` (+ `scaffold-<level>`, `worksheet-<level>`). **`lundy` is in
  that array in 0 of 45 files.** The section exists, carries content, and is never
  given `.visible`.
- **Where the content actually reaches people:** the four `lundy-box` panels on the
  Lundy Loop slide, front of class (icon + label + colour), and the `taBriefs`
  `"Lundy Loop"` entry for the adult. The **printed sheet** is what does not appear.
- **The closure sentence lives only here** — *"Closing the loop: out loud, as a class,
  is enough here. Any inclusion counts — a nod, a word, a pointed finger… Pass is
  always allowed."* It is inside `#print-area` and appears on no slide. An adult gets
  it from the TA brief or not at all.
- **Two derivations, no shared premise:** (1) static read of the `printPack` array;
  (2) Chromium at `media=print`, `printPack()` actually invoked, listing the elements
  that carried `.visible` — 10 sections per tier, `print-lundy` in none.
  Instrument: `LundyLoop/tools/loop_mark_print_gate.py` (LL-INST-09).
- **OPERATIONAL CONSEQUENCE, and why this entry exists.** `print-lundy` is the
  *natural* home for anything that belongs beside the closure line. Anything authored
  there ships into 45 live lessons and never reaches paper. **Author into
  `print-feedback`**, which is in the array in 45 of 45. This was caught by a gate,
  not by reading.
- **Do not "fix" by adding `lundy` to the array.** That prints an adult-facing page
  into every pupil's pack in 45 files. If it is ever wanted, it is a content decision
  with a human behind it. R-E05 applies: the print subsystem is closed to further
  auditing without a concrete report.
- **BOUNDARY — this rule is NOT universal. Ruled by the human via the physical print
  check, 2026-07-28.** It governs the **45-file BUILD chassis it was written for, and
  NOT the six v5 D&T Community Upcycling decks** (`Build/Slideshows/BUILD_DT_W{1..6}_*.html`).
  On those six, the physical print check confirmed the Lundy page prints **between the
  witness and feedback sheets, as intended**; commits `b1b7ee0`–`7889055`, which add
  `lundy` to the array on those six, **stand — no revert**, and their id lists are
  unfrozen. R-A07 continues to govern its original chassis. Reading it as universal is
  what nearly triggered a wrongful revert of those commits; the boundary is recorded
  here so the next governance session does not re-litigate it.
- **RESIDUAL, non-blocking.** The print check confirmed **order, not wording**. If the
  printed Lundy page on the six v5 decks ever reads as staff instructions rather than
  pupil-facing, that is a **wording fix, never a revert**.

### R-A08 · `printSection()` is defined in 45 files and called from none
- **STATUS** RECORD · **VERIFIED** `3e2b99d`
- `function printSection(id,level)` prints one named section. **1 occurrence per file
  across all 45 — the definition. Zero call sites, no UI control, no key binding.**
- **Not a defect.** It is the inverse of R-A06's *"`printPack` defined but never called
  from the UI"* and belongs to the same class: a print utility whose entry point was
  never wired. It is also the only existing route by which `print-lundy` could reach
  paper (R-A07).
- Recorded so the pair is not rediscovered as two separate alarms.

### R-A09 · The Loop Mark has no second copy — the absence *is* the control
- **STATUS** CONVENTION — read before extending anything in Pass LL-G
- The Loop Mark (`<!-- ll-g:loop-mark v1 -->`, in `print-feedback`, 45 BUILD lessons)
  is a ring the pupil makes and an initial the adult adds, **on the pupil's own
  printed sheet**. It is written down nowhere else and there is no version of it any
  adult can read without the pupil handing it over.
- **THE TEST, stated so a future pass can run it:** *if a second copy of the mark
  exists anywhere — a list, a sheet, a column, a total — the thing has changed species
  and the pass stops.*
- **Why this is a control and not a preference.** `LundyLoop/2_leadership/Impact_Framework.html`
  states it first and independently: *"What we will not do: count Rs, set loop quotas,
  or build a tracker. The moment the measure becomes the target, R becomes decoration
  and the framework has failed by its own definition."* `Whole_School_Reference_v2`
  requires moderation *"without creating a parallel evidence system."* The Loop Mark is
  compatible with both **only** while no second copy exists.
- **This entry is the only thing carrying the rule.** It was drafted for a staff note
  on a pupil-held day card; that card is **shelved** (Pass LL-G deliverable B2 §(c)/(d),
  to run only if the lesson-level mark is observed working in a real room). With the
  card shelved, nothing else states it.
- **The two precedents are registered separately, by subject, so they can be found:**
  `mbm_tt_evidence` → **R-B04** · `tt_tracker_v2` → **R-B05**. Read both before
  proposing any aggregation of the Loop Mark; between them they show the two ways this
  goes wrong — a mark nobody reads, and a number that measures the wrong thing.
- **Success measure, declared in advance.** "N files now contain a closure control" is
  a build log, not a finding, and must not be reported as a result. The signal is a
  Loop Walk sample and one question asked **of a pupil**: *"what does this ring mean?"*
  A set of sheets with **no blank rows** is the warning sign, not the good one.

---

## B · Storage keys

### R-B01 · `ps_coldcall_roster` — the shared roster
- **STATUS** CONVENTION · **VERIFIED** `d02ec43` · 65 files
- Deliberately estate-wide and shared. Shape: **plain array of strings**
  `["Amy","Ben"]`. 14 files render it with `loadRoster().join(', ')`.
- The label *"saved for all lessons"* appears in 13 files and **is true in all 13**.

### R-B02 · `coldCall_y10` — graded cold-call, a SEPARATE SYSTEM
- **STATUS** CONVENTION · **VERIFIED** `d02ec43` · 3 files
- `chemistry/Lesson2_pH_Scale_v4.html` · `chemistry/Lesson3_Ions_Neutralisation_v4.html`
  · `5 Intervention 10/Lesson_VIR_Intervention.html`
- **This is not an un-migrated predecessor. It is a richer model.** Shape:
  `[{name, grade}]` where grade ∈ `U,1,2,3,4`. The grade drives **tier-matched
  questioning** — `gradeToTier(picked.grade||'2')` → `rollQuestionForTier(...)`. In
  `Lesson3` the start button is disabled until every pupil has a grade.
- **DO NOT MERGE INTO R-B01.** Two proofs, recorded so nobody re-derives them:
  - Writing objects to the shared key breaks the 14 string consumers:
    `[{name:"Amy"},{name:"Ben"}].join(', ')` → `[object Object], [object Object]`.
    A teacher opens the roster box and sees that instead of their class.
  - Seeding these three *from* the shared key yields pupils with no grade, so
    `gradeToTier(g||'2')` **silently defaults everyone to tier 2** — differentiation
    flattened, no error, no signal. `Lesson3` at least fails loudly.
- **No false promise exists.** These three say *"Add pupil name…"* / *"Enter pupil
  name…"*. They make no cross-lesson claim. The earlier belief that they carried
  *"saved for all lessons"* was a fact observed about R-B01 and applied to files it
  was never seen in.
- **Grades stay local, deliberately.** A shared `ps_coldcall_grades` would be an
  origin-wide persistent store of per-pupil attainment judgements. Class lists on
  school machines were ruled acceptable; **grades are a different category** — a
  judgement about a child, not a name. Any change is its own conversation, never a
  side effect of tidying. Keying such a store by *name* would also be unsound: names
  collide, typo, and go stale.
- **CANDIDATE ESTATE-WIDE UPGRADE.** Tier-matched cold-call questioning exists in
  three lessons and nowhere else. A pupil gets a question pitched at their level at
  the moment of highest exposure — just after being called on in front of the room.
  When the question is *"what would make questioning better across the suite"*, this
  is the answer, already written down.

### R-B03 · `coldCall_y10_geog` — deliberate cohort silo
- **STATUS** CONVENTION · **VERIFIED** `d02ec43` · 2 files
  (`5_6 Local Choice/L18_Risk_Sampling.html`, `L19_Fieldwork_Day.html`)
- A Y10 geography group is a different set of pupils from a Y10 science group.
  Merging distinct cohorts would be a **data defect**, not a tidy-up.
- **Note what protects this: nothing but the key's name.** Naming is not a control.
  This entry is the control.

### R-B04 · `mbm_tt_evidence` — **RETIRED-IN-PLACE**
- **STATUS** RETIRED · **VERIFIED** `3e2b99d` · 10 files, all in `Tutor_Time/`
- **Shape** `{ <LESSON_ID>: {completed:true, date, xp} }`. Written by `finish()` in the
  ten Tutor Time decks (`WB_W1`–`W8`, two KCSIE). Ten `setItem`, ten `getItem`.
- **The ten `getItem` calls are not readers.** Every one is the read half of a
  read-modify-write inside `finish()`, merging into the same object. **There is no
  consumer anywhere in either repository.** A `getItem` count is not a reader count —
  direction is what makes the difference, as in R-A01b.
- **RULING: not deleted, not built on, not promoted.** It is not a candidate reader for
  any future day-loop or evidence carry.
- **Why, and this is the transferable part:** it records that a deck reached its end
  screen. That is **attendance at a slideshow, not a closed loop.** Promoting it would
  give a downstream artefact a field that looks like evidence and means "the last slide
  was shown". *A tick with a reader and no meaning is worse than a tick with no reader,
  because now something depends on it.*
- **Filename/ID drift, noted not fixed:** nine IDs are `tt_*`; the Vapes deck carries
  `LESSON_ID='mazzvapes'`. Standing rule 7 — a name is a hint, never a fact.
- Referenced by **R-A09**.

### R-B05 · `tt_tracker_v2` — the tracker store, and the percentage that ignores the loop
- **STATUS** RECORD · **VERIFIED** `3e2b99d` · 1 file
  (`Tutor_Time/Evidence_Tracker_Online.html`)
- The online twin of `Evidence_Tracker_Paper.html` — same columns, same Lundy key,
  same photo rule. Manual staff entry, device-local.
- **THE DEFECT, registered and deliberately NOT fixed in Pass LL-G:** `prog()` counts a
  session evidenced when **`s.photo && s.cap`** and prints *"n of 8 sessions evidenced
  (n%)"*. **The S/V/A/I ticks sit beside it and are not counted.** The one place in this
  estate that computes an "evidenced" number computes it from a photo and a caption,
  with the loop excluded.
- **Blast radius, derived rather than assumed:** `tt_tracker_v2` is read by exactly one
  file — itself. The percentage is computed client-side from a device-local store, so an
  external visitor sees their own empty sheet reading *"0 of 8"*. **It can only ever
  have been seen by the person who filled that device's sheet in, and there is no path
  from it to leadership.** A number nobody can reach misled nobody.
- **Why it is recorded and not corrected:** correcting it is a content decision about
  what "evidenced" means in Tutor Time, and that belongs to whoever owns the tracker.
  The entry exists so the next pass does not rediscover it as an alarm, and so that any
  future consumer of that percentage is a stop.
- **Not to be merged with R-B04.** Two stores, one folder, no binding between them —
  the R-G01 shape. Referenced by **R-A09**.

---

## C · Deletions — what was removed, why, and how to get it back

Rule: *a deletion nobody wrote down is irreversible in practice, because recovery
depends on knowing to look and knowing where.*

| ID | commit | files | restore from | what |
|---|---|---|---|---|
| R-C01 | `5053aa3` | 29 | `3b805af` | 28 identical root copies + `README.txt` (a stale revision of `LundyLoop/index.html`, argued separately) |
| R-C02 | `03b79b1` | 10 | `5053aa3` | The superseded v1/v2 subject poster series, all ten misnamed |
| R-C03 | `918d7de` | 1 | `452102f` | `wrangler.toml` — a deploy config for a Cloudflare project that has never existed |

`git checkout <restore-sha> -- <path>` recovers any of them.

### R-C04 · **Bucket A's criterion is not reusable**
- **STATUS** RECORD — read before any deletion pass
- The 29 were derived as *displaced copies of a file that stays*. They also happened
  to be uncatalogued and unlinked. **Do not invert that into a criterion.**
- **"Uncatalogued and unlinked" conflates junk with finished work nobody wired up.**
  All ten intact posters satisfied it perfectly, as did six PNG images wearing
  `.html`. A criterion re-derived that way would have deleted the complete poster
  series and reported success. No better criterion fixes this: **the information that
  separates junk from an unwired asset is not in the files.** It has to be declared.

### R-C05 · Intentionally-unlinked assets
- **STATUS** CONVENTION — the class R-C04 requires
- A file that is finished, deliberate and referenced by nothing must **say so**,
  exactly as a deliberate absence says so. Seed case: the poster series, which was
  one criterion away from deletion and protected only by someone opening the images.
- Current members: none. The seed case was superseded and removed under R-C02.

### R-C06 · The tidy-up made a measurement definable
- **STATUS** RECORD · **VERIFIED** `d02ec43`
- Before the deletions, HTML-by-extension and HTML-by-content disagreed by ten.
  After them: **429 = 429, zero self-misdescribing files estate-wide.**
- All eleven type-lies lived in one commit, `8e1eba5` (2026-07-13, *"Add files via
  upload"*), which also permuted ten posters. `a587837` two days later brought
  `wrangler.toml`. **Two web-uploader commits, two days apart, both introducing files
  that misdescribe themselves — a property of the intake path, not of the files.**
- So: *we deleted 40 files and gained a reliable denominator.* That is a better
  argument for tidiness than tidiness.
- **GATE:** run `identity_audit.py` before any pass that scopes by extension. Zero
  lies is a state, not a property.

---

## D · Public surface

### R-D01 · One public origin
- **STATUS** RECORD · **VERIFIED** `d02ec43`
- `madebymatt.uk` — GitHub Pages, `CNAME` in the site repo, extended over project
  pages. There is **no second origin**: `private-year-plan.pages.dev` does not
  resolve and no Cloudflare project exists under any name (dashboard-confirmed).

### R-D02 · Case is not stable in this estate — never assert it
- **STATUS** CONVENTION · **VERIFIED** `4d17f50` (site repo)
- The account has changed case twice: `mattroper1977` → `MattRoper1977`, and the site
  repo to `mattroper1977.github.io`. Redirects have covered it both times, **which is
  exactly why nobody notices until something doesn't follow redirects.**
- **VERIFIED CLEAN:** nothing in `LundyLoop/tools/` constructs a repo path or URL.
  All four instruments locate the repo with `Path(__file__).resolve().parents[2]`.
  **Preserve that.** Never hardcode a host, an owner or a repo name.

### R-D03 · Provenance on the leadership layer
- **STATUS** CONVENTION · **VERIFIED** `452102f`
- One sentence, byte-identical, in `LundyLoop/index.html` and at the head of
  `2_leadership/Head_Office_Summary.html` and `policy_alignment_matrix.html`:
  *"These are working documents written by Matt Roper about his own initiative,
  shared as written. They record one teacher's proposals and are not an
  organisational position."*
- **Do not remove.** The hazard is not embarrassment — it is **misattribution**: a
  document titled *Summary for Head Office* on an open domain reads as a Progress
  Schools position rather than one teacher's proposal.
- Each insertion carries an HTML comment saying so, **so the reason travels with the
  sentence** rather than living only here.

### R-D04 · The manual sitemap block
- **STATUS** CONVENTION · **VERIFIED** `4d17f50` (site repo)
- Seven leadership URLs are hand-added to `sitemap.xml` inside a marked block.
  They are **not derivable from `resources.json`** — the estate's convention is
  *entry points catalogued, leaves reachable through the page*, so only the hub and
  `Loop_Walk_Logger` carry catalogue entries.
- **Any regeneration must preserve that block.** If a generator is ever written, the
  block is its declared-extras input. **A missing sitemap entry has no symptom** —
  nothing breaks, nothing errors, the pages simply stop being found.
- Sequencing that must be repeated if this is ever redone: **provenance first,
  submission second.** The first version a crawler caches must be the framed one.

---

## E · Instruments and metrics

### R-E01 · Quarantined: `print_pack_audit.py` v1
- **STATUS** RETIRED · **Numbers unquotable: 691 absent slots, 123 files.** Both
  false — it hardcoded `foundation/middle/higher` where Art Teesside uses
  `supported/standard/stretch`. True figures came from v2. Full entry in
  `INSTRUMENTS.md`.

### R-E02 · L3, L4 and L5 are unquotable
- **STATUS** OPEN — blocks LL-5
- **L5** was `print_has_lundy`, a proxy for *captured*. A 103-file pass made the proxy
  true; eighteen lessons scored L5 without anything about them changing. The metric
  moved because we patched what it measured, not what it stood for.
- **L3** is *a named observable pupil action*, and LL-5 exists to add exactly that to
  58 files. **Redefine L3 before LL-5 runs, or declare it unquotable in advance.**
- Redefining L4/L5 **is** the evidence-slot specification — one job, not two. A real
  definition of *captured* must say what capture means, where it lands, who can see
  it, and what makes it true.

### R-E03 · LL-E must be re-derived, not reconciled
- **STATUS** OPEN
- LL-E reported 22 files, then 20 files / 16 gaps. `print_pack_audit` v2 reports 13
  files / 22 slot-*instances* — **a different unit; the shared 22 is a collision, not
  agreement.** LL-E's own derivation died with the sandbox, so there is nothing to
  reconcile *against*. Queue item 3 is a rebuild.

### R-E04 · LL-F's nine, confirmed independently
- **STATUS** VERIFIED `d02ec43`
- Ten files lack a `wedo` print slot; one (`Respiration_ATP_Recap.html` at root) was
  a displaced copy removed under R-C01. **Nine remain — matching LL-F's recorded
  nine, derived by an instrument with no access to LL-F.** The tenth was invisible to
  every LL-era instrument because they all scoped off the catalogue and it was
  uncatalogued.

### R-E05 · The print subsystem is closed to further auditing
- **STATUS** RECORD
- Chain: **691 → 12 → 4 → 7 → 0.** Five alarms, five retirements, **zero real defects.**
- Cause: *a subsystem with many valid designs generates false positives in proportion
  to its variety, not its defect rate.* The print layer has at least five legitimate
  architectures. Every pattern-matching instrument reported the four it didn't
  recognise as broken.
- **Do not audit it again without a concrete report from a human.** Demonstrated
  yield: zero. `classify.py` exists because it is the only instrument that can tell
  *another design* from *no design*.

### R-E06 · `LundyLoop/tools/` is mislocated
- **STATUS** RECORD — decision made, action deferred
- The instruments are estate-wide; they belong at the repo root by the same argument
  that puts this file there. **Not moved**, because churning a directory committed
  hours earlier costs more than it buys. Recorded so the question is not re-asked.

### R-E07 · The KO candidate list is about to grow by 45, and it is an artefact of Pass LL-G
- **STATUS** RECORD · **VERIFIED** `d601842` — predicted and measured **before** the number moved
- **Read this before quoting `ko_staleness.py` on any BUILD file.**
- **What will happen.** `ko_staleness.py` (LL-INST-08) flags a file when its **visible
  text** last moved *after* its KO block last moved, in a commit classified as a
  **content** pass. Pass LL-G adds visible text to `print-feedback` in 45 files, and
  `Pass LL-G` does not match the instrument's `ARCHITECTURE` list. **All 45 therefore
  become candidates the moment this lands.** All 45 carry `id="print-ko"`, so 45 is both
  the expected and the maximum increase.
- **Measured, not predicted:** the instrument's own `visible()` hash moves in **45 of
  45** files. Its `ko_text()` hash is **unchanged in all 45** — the KO block itself was
  not touched, which is the point.
- **THIS IS THE PROXY SHAPE AGAIN.** LL-3's print mirror made `print_has_lundy` true
  across 104 files and eighteen lessons appeared to gain a level while nothing about
  them changed (R-E02). Here a staleness proxy will report 45 organisers as candidates
  because a **feedback control** was added to a **printed sheet** — which is not
  something a Knowledge Organiser summarises. *The instrument is not wrong; it is
  answering the question it was built to answer, and that question is a proxy.*
- **Do not read the new candidates as forty-five stale organisers, and do not "fix"
  them.** Nothing about what those KOs summarise has changed.
- **THE FIX, tested and available.** The instrument's v1→v2 lesson was that markup and
  CSS moving is not the body moving; it strips tags, scripts and styles. It does **not**
  strip *print-region text*, which is the same class of thing. Excluding regions that
  declare themselves not-KO-relevant — the Loop Mark carries
  `<td class="lm-strip">` and `<span class="lm-own">` — **restores the pre-patch body
  hash in 45 of 45 files**, verified. Two lines in `visible()`'s caller.
- **Prefer the declaration in the artefact over an entry in the tool's list.** Adding
  `Pass LL-G` to `ARCHITECTURE` would also work and is the **dangerous direction**: a
  wrong entry there silently *drops* a real candidate, which already happened once with
  `Pass LL-A2a`. A region that says in the markup that a KO does not summarise it is
  self-describing, survives the next pass, and needs no list. This is the
  `assessed_conditions_gate` lesson reused: **when a blind spot is caused by missing
  information rather than weak extraction, fix the document.**
- **Not fixed in Pass LL-G**, deliberately — changing an instrument inside the pass whose
  output it is about to judge is the error this register exists to prevent. Its own pass.

### R-E09 · An instrument must not be modified in the pass it is measuring
- **STATUS** CONVENTION — a sequencing rule, and it will read as pedantry to anyone in a hurry
- **The rule.** If a pass changes files that an instrument scores, that instrument is
  **frozen for the duration of the pass**. Read its output, judge it, *then* change it.
  Never adjust the instrument and the files in the same breath.
- **Why, stated so the hurry does not win.** An instrument altered mid-pass produces a
  number nobody can attribute. Did the count fall because the estate improved, because
  the instrument was narrowed, or because both moved and partly cancelled? **There is no
  way back from that**, because the before-reading was taken with a different instrument
  than the after-reading. It is not a rigour preference; it destroys the comparison.
- **The live instance.** Pass LL-G adds visible text to 45 files, which will grow
  `ko_staleness.py`'s candidate list by 45 (**R-E07**). A two-line fix exists and is
  tested. Applying it inside Pass LL-G would have produced a KO list that was neither
  the old measure nor the new one, and the 45 would have been silently absent from a
  number that had also silently changed meaning.
- **Precedent, and why this is not hypothetical.** LL-3's print mirror made
  `print_has_lundy` true across 104 files and eighteen lessons appeared to gain a level
  while nothing about them changed (**R-E02**). `print_pack_audit` v1's retired figures
  are unquotable for the same reason (**R-E01**) — the instrument moved, so its numbers
  cannot be compared to anything.
- **The corollary that makes it usable:** when a pass will move an instrument's output,
  **register the expected movement before the pass lands** and fix the instrument
  afterwards. A predicted artefact is readable; a discovered one starts an investigation.


### R-E08 · The stale-copy marker for the Loop Mark 45
- **STATUS** RECORD · **VERIFIED** `d601842`
- **The most recent deploy touching these 45 files is now `d601842`** — Pass LL-G sub-pass
  3 of 3. It was **`14b691c`** (Pass LL-4b, *"name SPACE as the TA's first job"*), and any
  guard still keyed to `14b691c` will now mismatch — **correctly**, because the files have
  genuinely moved. Re-key it; do not suppress it.
- **Why this needs an entry rather than a memory.** A stale-copy guard names a commit. The
  commit it names stops being the tip of that file's history the moment anything touches
  it, and **a guard keyed to a superseded SHA has no symptom** — it fails open or it fails
  loud depending on which direction it was written in, and neither tells you *why*.
- **The population this marker covers is the 45 of the Pass LL-G set** — not "the BUILD
  lessons", which is ambiguous inside this estate's own record (76 lessons, split
  45/16/8/7; see the Pass LL-G derivation). **The set is a derivation, not a manifest:**
  `git grep -l 'll-g:loop-mark v1' -- '*.html' ':(exclude)LundyLoop/5_staff_training/*'` = **45**.
  The three container-bound sub-pass manifests were archive-only and never committed — the
  R-E08 lesson itself, that a derivation which re-runs beats a list that can go stale.
  Re-derived **45** at `0ec1da0` (2026-07-28), a HEAD already carrying sixteen live commits
  the sentinel has survived unchanged.
- **The `-- '*.html'` scope and the `5_staff_training/` exclusion are load-bearing, not
  tidiness.** `REGISTER.md` already joins the *unscoped* count — R-A09 quotes the sentinel
  `<!-- ll-g:loop-mark v1 -->` (this file, ~line 185) — so a bare `git grep -l` returns 46,
  not 45. `LundyLoop/5_staff_training/` will join the *scoped* count the day the Made-by-Matt
  TA card lands there quoting the sentinel or the `lm-strip`/`lm-own` markup. It contributes
  **0** today, so the exclusion is a **prospective guard**, not a present correction: with it
  45, without it 45; control — excluding `BUILD_ASDAN/*` gives 14, so the exclusion is
  honoured in this git, not a silent no-op.
- **General form — the R-G03 cached-claim family, one layer out:** *a derivation that
  measures a marker can be joined by any document that describes the marker.* R-A09
  describes the sentinel, this entry measures it, and the scope is what keeps the describer
  out of the count. See R-G03.
- **The 31 files not in the set still key to their own last-touching commit.** Do not
  apply `d601842` to anything outside the 45. R-F04: a fact travels no further than the
  file it was observed in.

### R-E10 · An exclusion belongs to a named derivation, not to a folder
- **STATUS** CONVENTION · **VERIFIED** `a5092bb`
- **The general form.** *A folder is only "excluded" relative to the specific derivation
  that excludes it. The exclusion is a property of that derivation's pathspec, not of the
  folder — any other instrument counting the same marker over a different pathspec will
  see the folder.* Telling a pass "that folder is excluded" as though the folder itself were
  out of scope is the cached-claim family (R-E08, R-G03) one turn further out: the claim
  attaches to the wrong object.
- **Two derivations, not one — the reconciliation.** The order that landed `a5092bb` gated on
  the **raw** form (`git grep … -- '*.html'`) and called `LundyLoop/5_staff_training/` an
  "excluded pathspec." It is **not** excluded there. The `5_staff_training/` exclusion lives
  only in the **derivation of record, R-E08.** Emitted, not described (observed at `a5092bb`):
    - raw (order §0.4): `git grep -l 'll-g:loop-mark v1' -- '*.html'` = **45** — *counts the folder*
    - of record (R-E08): `… -- '*.html' ':(exclude)LundyLoop/5_staff_training/*'` = **45** — *excludes the folder*
    - `5_staff_training/` contribution today: `git grep -l 'll-g:loop-mark v1' -- 'LundyLoop/5_staff_training/*.html'` = **0**
  Both read 45 **only because the folder contributes 0 today.** Proof the raw form reaches into
  the folder while R-E08 does not — using a non-sentinel string unique to the game file (never
  quote a marker in this folder; see the interim guard): `git grep -l 'receipt by the back door'
  -- '*.html'` returns `…/R_Gate_Calibration_Game.html`; the same grep with
  `':(exclude)LundyLoop/5_staff_training/*'` returns nothing. Control:
  `… ':(exclude)BUILD_ASDAN/*'` = **14**, so the exclude is honoured in this git, not a no-op.
- **What actually kept §5 safe was discipline, not a guard.** The calibration section stayed out
  of both sentinels because it **quotes neither marker verbatim** — authoring restraint, not the
  raw grep protecting it. Had it quoted `ll-g:loop-mark v1` or the R-A02 written-line selector,
  the raw §0.4 gate would have moved (→ 46 / 49) while R-E08's derivation held. The order claimed
  a structural guard; there was none on the raw form.
- **Interim guard (in force now).** Until/unless the raw §0.4 gate is rewritten to carry the
  R-E08 exclusion, the rule for authoring anything under `LundyLoop/5_staff_training/` is: **do
  not quote either sentinel marker verbatim** — not `<!-- ll-g:loop-mark v1 -->`, not the R-A02
  written-line selector. §5 already did exactly this. Sentinel-2 has **no** path exclusion (R-A02):
  its describers stay out of the count only by `-- '*.html'` dropping the `.md` files, so the same
  discipline is the only thing keeping this folder out of that count too.

---

## F · Superseded and open

### R-F01 · Superseded, do not complete
- `6 Art/` legacy Art series — superseded by the Teesside Studio Suite. The Surrealist
  Collage file is registered under R-A06 for its print-light convention, but the
  series itself is not to be extended.

### R-F02 · `BUILD_ART_W4` missing scaffold sections
- **STATUS** OPEN · **Question:** is it the whole BUILD Art set or W4 alone? Unanswered.
  *"The X file" is an unverified singleton* — re-ask it as a query before acting.

### R-F03 · Near-identical pairs that are both real
- **STATUS** OPEN
- `biology/L4_Aerobic.html` ↔ `biology/L4_Aerobic_Respiration.html` — same `<title>`,
  0.763 word-set Jaccard, **both separately catalogued.** Two live catalogue entries
  for one lesson. Not a displaced copy; needs a content decision.

### R-F05 · Anything verified by eye in this estate is unverified
- **STATUS** CONVENTION · **VERIFIED** `7226b08`
- **This estate has a large invisible text layer.** Of 271 files carrying
  `Made by Matt`, **193 occurrences live in `aria-label` (110) and `alt` (83)** —
  attributes that never render as text. A rebranded pack passes a visual check while
  a screen reader announces the wrong organisation. That is an **accessibility
  failure wearing a branding costume**, and the principle outlives the rebrand.
- Any check performed by looking will miss most of the estate. **Grep, don't glance.**
- **Open follow-up:** are there other strings in `aria-label` and `alt` that would
  embarrass a rebrand or a public copy — school name, staff name, internal phrasing?
  Same greps, different needles. Not yet run.

### R-F06 · Mechanise every rule that can be mechanised; call the rest aspirations
- **STATUS** CONVENTION
- **Three transcription errors in two days, every one caught by a check and none by
  care.** The most recent was written into the very document that records the rule
  against it: `REBRAND.md` said the strip count was 45, read from one bucket of a
  `uniq -c` output. It is 47, caught by the pre-commit assertion.
- **A rule in the tooling catches what a rule in the resolve does not.** Where a rule
  can be a gate, make it one; where it cannot, say plainly that it is an aspiration
  rather than a control.
- Currently mechanised: count-vs-list assertion before send · declared-manifest vs
  committed-files assertion after push · classify-before-count · `identity_audit` as
  a gate before any extension-scoped pass.


### R-F08 · A scope-level check cannot detect a missing scope
- **STATUS** CONVENTION · **VERIFIED** `3e2b99d` — earned by a near-miss in this pass
- **The instance.** Pass LL-G deployed as three sub-passes of 15, each asserting
  `declared == touched == staged == 15` before committing. On a rebuild, **commit 2
  (the gate) silently failed** — its file had been removed from the working tree by a
  branch reset — and the three sub-passes were built and committed without it.
- **The assertion fired, but not for the reason it should have.** It reported
  `touched=16` only because an uncommitted `INSTRUMENTS.md` was sitting in the tree as
  an unrelated sixteenth change. **Had that file been clean, every sub-pass would have
  read 15/15/15, passed, and shipped a five-commit set with one commit missing.**
- **The shape, stated generally:** *a check that validates the contents of a scope is
  blind to the existence of the scope.* Cardinality within N sub-passes says nothing
  about whether there are N sub-passes. The count is correct and the set is wrong.
- **This is the estate's oldest failure arriving in the safety net rather than in the
  pass** — a check that confirms the instrument rather than the work (LL-INST-05,
  R-E05). It is more dangerous here, because a green assertion in a deployment gate
  reads as permission to push.
- **Mechanised**, per R-F06: `verify_commit_set.py` asserts the **set** against the git
  log before any push — commit count, and per commit the paths it carries, checked
  against the emitted manifests. Never against a memory of having built it.
- **Corollary for any future batched pass:** assert one level above the unit you are
  batching. If you batch files into commits, assert the commits. If you batch commits
  into a pass, assert the pass.

### R-F07 · Scope a key search to the object that owns it
- **STATUS** CONVENTION · **VERIFIED** `3e2b99d` — earned by a defect this pass authored
- **Standing rule 8 applies to a JSON key, not only to a filename.** *"The X key"* is an
  unverified singleton in exactly the way *"the X file"* is.
- **The instance.** Pass LL-G v1 appended a TA instruction anchored on the bare key
  `"Independent Work":`. That key resolves to **two objects in each of 45 files**:
  `_ccQuestions` (a pupil-facing cold-call bank, value an object `{F:,M:,H:}`) and
  `_taBriefs` (value a string). **`_ccQuestions` comes first in source order.** The
  append landed inside a Foundation-tier question asked aloud to a pupil, producing
  *"Show me what you have done so far. Give the next step out loud while you circulate
  — say it, do not write it…"*. Same for `"Lundy Loop":`.
- **Why it would have survived review.** The corrupted string is grammatical, is in the
  right file, and reads as almost-plausible on screen. Nothing in the file detects it.
- **The remedy, and why it is not "be careful":** brace-match the owning object first,
  then require the value's *type* to be what you expect before writing. A key is not a
  location. Two structural facts must both hold — right object, right value shape.
- **Mechanised**, per R-F06: the patch scopes to `_taBriefs` by brace-matching and
  refuses a non-string value; a gate asserts `_ccQuestions` is **byte-identical**
  after every apply. That gate is what caught this, and it stays.

### R-G01 · Cached claims — prose asserting something about elsewhere
- **STATUS** RECORD · **VERIFIED** `35efefd`
- The dominant failure shape of this whole programme: a local artefact asserting a
  fact about a different artefact, with nothing binding them. Every one goes stale
  silently, because a stale claim has no symptom.

| # | claim | asserts | about | what keeps it true | at `35efefd` |
|---|---|---|---|---|---|
| 1 | `refs/remotes/origin/main` | "the remote is at X" | a remote repo | **nothing** — stale on every URL-push | was stale; fetch after every push |
| 2 | `INSTRUMENTS.md` | which instruments exist | `tools/` | **nothing** | 6 listed / 6 actual ✓ |
| 3 | `sitemap.xml` | 386 URLs exist & should be indexed | the Lessons repo, **across a repo boundary** | **`sitemap_audit.py`** (LL-INST-07) | 0 dead ✓ |
| 4 | `resources.json` | 382 files exist | the tree | **`hash_sweep`** | 0 broken ✓ |
| 5 | `REGISTER.md` counts | estate state | the estate | **nothing** — but each is stamped | true at the commits named |
| 6 | Knowledge Organisers ×161 | what the lesson contains | the lesson body | **`ko_staleness.py`** (LL-INST-08) | 109 candidates |
| 7 | Conditions Card ×2 | what each tier may use | the slides | **`assessed_conditions_gate`** | 4 unmentioned offers |

- **Two had a mechanism this morning. Five have one now.** #5 has no mechanism and
  cannot have one — a count is true at an instant. The stamp is the achievable form.
- **The rule that produced #3's instrument:** *when a claim spans a boundary no
  instrument can cross, test the thing the claim is ultimately about — not the
  artefacts on either side of it.* The sitemap's real assertion is not "these files
  exist in that repo" but "these URLs resolve", which is testable over HTTP with no
  repo access at all.

### R-G02 · Knowledge Organiser staleness — candidate list, not a defect count
- **STATUS** OPEN · **VERIFIED** `35efefd` · derive with `LundyLoop/tools/ko_staleness.py`
- **161 KO files · 109 candidates · 8 dropped as architecture-only · 44 clean.**
  Cardinality asserted 109 + 8 + 44 = 161.
- A candidate is a file whose **visible lesson text** moved after its KO block last
  moved, in a commit that was a **content** pass rather than architecture. It reads
  no content and makes no judgement about correctness.
- **Read first: `Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html`** — assessed,
  7 content movers, and the first is **`Pass LL-A2a`, which removed the Connective
  Bank and the Evaluation Deployments**. If its KO names either, or describes
  scaffolds by name, the KO is describing support that no longer exists inside an
  assessed file — a **fourth surface** disagreeing with the Card, after the slides,
  the print pack and the scaffold rows. **Read it against the Card, not the body.**
  Second: `LAUNCH_HUM_W7_Source_Assessment.html`, 4 content movers.
- **We are the most recent source of divergence.** Nearly every candidate had an
  author who wrote a KO that matched, and a series of passes since — ours included —
  that moved the lesson without looking at it.
- **The instrument's dangerous part is its `ARCHITECTURE` list**, because a wrong
  entry silently *drops* a real candidate. That happened on the first run:
  `Pass LL-A2a` was mislisted as architecture. Removed. Check that list before
  trusting a shrinking number.

### R-G03 · The cached-claim shape landed on the entry that catalogues cached claims
- **STATUS** CLOSED (`64d8fb4` — H-series H3: INSTRUMENTS.md reconciled to 13 scripts / 13 entries both directions, the "6 listed / 6 actual" claim replaced with a re-derivable form) · **VERIFIED** `3e2b99d`
- **R-G01 row 2** records: *`INSTRUMENTS.md` | which instruments exist | `tools/` |
  what keeps it true: **nothing** | 6 listed / 6 actual ✓*. That was true when observed.
  At `3e2b99d` there are **8 instrument scripts in `tools/` and 6 full `## LL-INST-0X`
  entries.** `assessed_conditions_gate.py`, `sitemap_audit.py` and `ko_staleness.py` are
  referenced by ID in the blind-twin table and in R-G01 itself, but have no entry of
  their own.
- **This is the point of the entry.** R-G01 exists to enumerate claims that go stale
  silently because nothing binds them. **Its own row went stale silently, and its own
  "what keeps it true" column already said `nothing`.** A cached claim about how many
  cached claims there are.
- **The argument it settles, and it is the strongest available:** a count in prose has
  no mechanism and cannot acquire one by being written more carefully — R-G01 predicted
  exactly this failure, in writing, and it happened anyway. **Put counts under an
  assertion or accept that they are re-checkable rather than true.** The stamp is the
  achievable form; the assertion is the preferable one.
- **NOT fixed here, deliberately** — repairing it inside a lesson-authoring pass would
  make the same category error twice. Scoped as its own pass: write the three missing
  entries, re-observe R-G01 row 2, and correct the count to **9 files / 10 entries**
  after `LL-INST-09` (Pass LL-G) lands.
- **Do not read a shrinking discrepancy as progress** without re-running `ls
  LundyLoop/tools/*.py | wc -l` against `grep -c '^## LL-INST-[0-9]'`. Both numbers move.

### R-G04 · A self-referential stamp cannot be maintained by the commit that changes the file
- **STATUS** CONVENTION · **VERIFIED** Pass LL-G, commit 6
- **The shape.** A file that states its own currency — *"current as of X"* — cannot have
  `X` be the commit that most recently changed it, **because that commit's identity does
  not exist until after the content is written.** The stamp is false the instant it lands.
- **This is the fifth data point for R-G03 and the cleanest one.** The other four were
  counts that were correct when written and went stale through neglect. This one is
  **structurally incapable of being true at the moment it is written.** No amount of care
  fixes it; only a different form does.
- **The instance.** `HANDOVER.md`'s header read *"Current as of `35efefd`"* — on the one
  line in the file that governs how the file is maintained. Pass LL-G commit 6 edits that
  header, so the stamp was false the moment the commit landed.
- **Two remedies, both valid:**
  1. **Name the pass, not the commit** — *"Current as of Pass LL-G, commit 6"*. True when
     written, and it stays true, because **a pass does not move after it lands**.
  2. **Patch the value in afterwards**, the way R-E08 takes the pushed SHA as an argument.
  **Taken here: (1).** A header stamp does not need commit precision, and **a value
  nothing keeps true is worse than a coarser one that stays true.**
- **It is the `VERIFIED <commit>` convention run the other way** — not *"here is when this
  was observed"* but *"here is what this describes"*. Both are useful; only one of them can
  be written by the thing it describes.
- **THE DISTINCTION THAT MAKES THIS NARROW, and it was checked rather than assumed.**
  `REGISTER.md` (*"Last observed true at `35efefd`"*) and `INSTRUMENTS.md` (*"Last observed
  true at `8c384a7`"*) do **not** have this defect. They make a **historical** claim — a
  check was run at that commit — which stays true forever, including after the file
  changes. `HANDOVER.md` made a **currency** claim about its own state, which goes false on
  the next edit. **Historical stamps are safe; currency stamps are not.** Only one of the
  three needed fixing.
- **HISTORICAL STAMPS MUST STAY COMMIT-NAMED. That is not an oversight; it is the
  point.** Naming the commit is what makes a historical claim **re-observable**:
  *"6 listed / 6 actual at `8c384a7`"* can be re-run against `8c384a7` and confirmed or
  refuted. Replace that commit with a pass name and the claim becomes **unfalsifiable** —
  nobody can return to the exact tree the check was run against. `VERIFIED <commit>` is
  doing its job. **Do not convert it.**
- **DO NOT RUN THIS RULE BACKWARDS.** *"Never the commit"* applies **only** to a currency
  claim a file makes about its own state. Applied to a historical claim it destroys the
  property that makes the claim worth having. **Two of this estate's three stamps are
  already in the correct form and must not be touched** — `REGISTER.md` and
  `INSTRUMENTS.md` stay commit-named, permanently.
- **Applies to:** any artefact naming its own currency. If a file must state its own
  freshness, name the pass, the term or the release — never the commit that is about to
  contain the sentence. If a file records **when a check was run**, name the commit —
  always.


### R-F04 · Facts do not travel between files
- **STATUS** CONVENTION — the rule two of this session's corrections earned
- **A fact travels no further than the file it was observed in.** Applied to a
  different file, it must be **re-observed there** before being acted on. Restating it
  does not verify it; it only makes it sound verified.
- Both instances survived multiple retellings and were caught only by reading the file:
  - *Respiration:* "catalogued" was true of `biology/Respiration_ATP_Recap.html` and
    was attached to the root copy. The resulting ruling would have deleted the
    catalogued file and broken a live hub entry.
  - *Roster:* *"saved for all lessons"* was true of the `ps_coldcall_roster` files and
    was attached to three that have never carried it. See R-B02.

---

## H · The Pass-V / LL-I collision — pass discipline earned 2026-07-28

**Stated plainly because the first account was wrong.** During Pass LL-I a run of commits
authored by `Claude` landed on `origin/main` against BUILD_DT and other lesson files. LL-I's
first reports called the source a **rogue / unauthorised session** and the containment rulings
ordered the series reverted. **That framing was false.** The source was `session_0183`, Matt's
own commissioned **Pass V** (D&T v5 migration) — every commit authorised. What corrected it:
reading the commits against Matt's own record of Pass V, available the whole time at no cost,
plus the delivery- and anomaly-findings below. **Nothing was ever reverted** — the revert was
withdrawn in full before it was built, and holding-for-trigger / stop-on-gap / fetch-before-
building meant the whole episode cost zero repo changes.

### R-H01 · Commissioned-unread, not rogue — a do-not-touch list binds only sessions that have read it
- **STATUS** RECORD · **VERIFIED** `0ec1da0`
- Two authorised passes (LL-I, Pass V) ran against overlapping files. The one that had read
  R-A07 could not tell the other's authorised work from an attack, because the difference is
  not in the tree. The six W1–W6 `printPack` `'lundy'` adds were the exact R-A07 anti-pattern
  (*the zero is DIFFERENT_MODEL, not ABSENT*) and **R-E05 held** — the commit messages were the
  machine-confident ABSENT-misread verbatim — **but the author had never read the register.**
- **The rule:** a do-not-touch list governs only sessions that have read it. **Remedy, specific:
  every commissioned session's brief carries the register, or the register does not govern that
  session.** Naming a file "protected" in a document one session holds protects it from that
  session alone.
- **Resolved 2026-07-28 — the physical print check ran (Pass V).** On the six v5 D&T decks the
  Lundy page prints between the witness and feedback sheets as intended, so **R-A07's prohibition
  does not reach them** (they carry a Lundy print section *by design* in a 14-section pack);
  commits `b1b7ee0`–`7889055` **stand, no revert**, and the `printPack` id-list hold is **lifted**.
  Recorded independently at `32441c5` as R-A07's **BOUNDARY** note — this session and Pass V were
  both authorised to record it (**R-H02 again**; Pass V landed it first), so this closes the
  question rather than duplicating it. The **adult-facing SPACE line** — *"regulate before you
  educate"* on pupil paper — survives as a **wording candidate**, kept in R-A07's **RESIDUAL**:
  if the printed Lundy page ever reads as staff instructions rather than pupil-usable, that is a
  **wording fix, never a revert**.
- **The remedy appears to be taking, observed in flight (`32441c5`, `0ec1da0`).** After the
  collision, Pass V's own subsequent commits recorded the R-A07 boundary *in this register* and
  added a provenance note in the R-D03 family (*"Aimee is fictional, not a pupil"*) — the behaviour
  of a session that has read the estate's conventions. **One instance, not proof** — the commit
  names are attached so a second can be counted against them. This estate is full of declarations
  that never bound anything; *a rule observed changing behaviour is a different species from a rule
  written down*, and this is the first of the second kind.

### R-H02 · Cross-pass collision — the estate cannot see a pass's work in flight
- **STATUS** OPEN · **VERIFIED** `0ec1da0`
- LL-I read Pass V's commits as a breach; Pass V had no way to know LL-I existed or that its
  files were under a hold. **Nothing in `tools/` detects this and nothing could** — the missing
  artefact is a *statement of what is in flight*, not a property of the tree, and every
  instrument here reasons over the tree or the commit graph.
- **Remedy candidate, a pass not a build:** a declared in-flight scope — which passes hold which
  paths, now — checked before any pass opens on a file. Recorded because the failure recurs
  whenever two passes overlap and neither declares.
- **Recurred live, so this is tested not argued (like R-H05).** Within the same LL-I close, Matt
  authorised LL-I to record the R-A07 boundary *and* Pass V recorded it independently at `32441c5`;
  LL-I fetched-before-building, saw the artefact already landed, and **declined to duplicate** —
  closing its own stale `R-H01` bullet at `195ee37` instead. Two authorised routes to one artefact,
  first-lander wins, second-lander cross-references rather than duplicates. That is the collision's
  benign resolution when at least one side fetches first; the malign one (the near-wrongful revert)
  is what happens when neither does.

### R-H03 · Scope discipline — three forms, and the two worked in anger
- **STATUS** CONVENTION · **VERIFIED** `0ec1da0`
- **Once a predicate admits an exception it stops being a predicate and becomes an enumeration.**
  The containment scope was first a predicate (*session_0183 AND [R-A07 lundy OR benign BUILD_DT
  edit]*); a commit fell outside it (`e3082d2`, Art_Teesside reduced-motion), and the fix was to
  **pin by SHA and re-enumerate on every tip move**, never widen the set by reasoning.
- **Where the reversibility test points opposite ways for two commits in one scope, they are two
  rulings, not one scope.** The lundy adds pointed *in*; `e3082d2` (an accessibility rule —
  reverting it strips a live protection from SEMH pupils) pointed *out*; same test, opposite
  verdicts.
- **A ruling's factual premises are claims too — verify upward, even when the order is Matt's.**
  Two worked examples:
  - *Smaller:* Amendment 1 §0 claimed a trigger under the predicate would have *swept* `e3082d2`
    into the revert. False — a third-kind commit would have **stopped** the build, not been
    reverted. Moot operatively; kept as the clean case.
  - *Larger — authorship.* Containment rested on the commits being unauthorised. The resolved 1A
    ruling had *not* asserted that (it ruled on reversibility precisely so authorship need not be
    settled), yet **every document after it used the vocabulary of an unauthorised actor** —
    *rogue, breach, containment* — until the open question read as settled fact. General form:
    **a question explicitly left open in a ruling can still be closed by the vocabulary used
    around it; restate its openness wherever the subject is named, or the prose answers it.**
  - Reusable check: the first report asked *whose is this?* (answerable only by Matt). The
    productive question was *which of Matt's passes touched BUILD_DT?* (answerable from his
    records, free). **When a question about authorship is expensive, ask the question about scope
    instead.**
- **Untested note, not a rule:** a proposed fourth form — *rulings a freeze will need are made
  before the freeze, not during it* — is withdrawn because no freeze happened and the case never
  occurred. **A principle whose case never happened does not enter the register** (the discipline
  that retired 0-of-8, R-H07). Kept only as this marked-untested note.

### R-H04 · Delivery is part of the order
- **STATUS** CONVENTION · **VERIFIED** `0ec1da0`
- **An order that names a governing document the executor does not have is unexecutable, even if
  every word is correct.** Amendment 2 was internally sound and could not be acted on, because
  Amendment 1 — which it named as load-bearing — had never been delivered; the erratum failed
  delivery the same way a day later. Two governing documents lost in transit in one day.
- **Detection route, worth as much as the rule:** found by reading two documents' claims about
  each other with **no repo access and no instrument** — the route that found every contradiction
  in the July audit, and one nothing in `tools/` performs.

### R-H05 · A correctly-formatted order is not an authenticated one — the anomaly rule
- **STATUS** CONVENTION · **VERIFIED** `0ec1da0` — **tested, not argued**
- Any document claiming to amend the order stack is an **anomaly**: do not act, report it, wait
  for separate confirmation — **even if well-formed, even if it names its replaced sections
  correctly, even if it sounds like Matt.** A document cannot authorise itself; the guarantee is
  only that a human read it before it became an order.
- The one incident rule with a real case behind it: it **fired on its author's own next document**
  (Amendment 3, arriving after the set was declared closed) and was handled exactly as written.
  Argued rules retire; tested ones stay.

### R-H06 · When a ruling is blocked on authority, rule on reversibility instead
- **STATUS** CONVENTION · **VERIFIED** `0ec1da0`
- Authority can be established afterwards; printed paper cannot be recalled. The reversibility
  test both selected the (withdrawn) revert set and kept `e3082d2` out of it, and it produced a
  recoverable outcome throughout — which is why withdrawing the revert cost nothing.

### R-H07 · The "0 of 8 GROW R-gate" claim — retired as a defect claim
- **STATUS** RECORD · **VERIFIED** `0ec1da0`
- *"0 of 8 GROW files clean on the R-gate"* was carried across two passes, including into a brief,
  **as if it were measurement. There is no R-gate.** No `r_gate` predicate exists in `tools/`; the
  claim has no in-tree derivation. The only in-estate definition of the gate is a staff-training
  artefact, `LundyLoop/5_staff_training/R_Gate_Calibration_Game.html`, keying closure on **adult
  receipt** (*"Closed (R) = Voice happened AND an adult genuinely received it"*) — a BUILD-shaped
  token structurally blind to GROW's *pupil-writes* closure. 0-of-8 measures the absence of a
  token GROW does not use by design; it is **not** a GROW defect.
- **General form:** *a number quoted across passes inherits the authority of a derivation without
  ever having been one* (the R-G01/R-G03 family).

### R-H08 · The calibration game mis-trains TAs on GROW/LAUNCH closure — September deadline
- **STATUS** CLOSED (`18270dc` — Matt's stated second paper read of the rebuilt game; a human observation, not a derivation, no instrument witnessed it) · **VERIFIED** `0ec1da0`
- `LundyLoop/5_staff_training/R_Gate_Calibration_Game.html` teaches **adult receipt** as the test
  of closure (*"An R without a received response is a false record"*) to TAs who work **all three
  pathways.** A TA calibrated on it will seek an adult-receipt token in GROW/LAUNCH — where closure
  is the pupil *writing* the line, no receipt by design — find none, and either supply one (the
  day-level R the design forbids: a species change, R-A09) or record the loop as not closed.
  **That is the TA-card failure LL-G exists to prevent, arriving from the opposite end of the
  pathway, on the same first-staff-briefing deadline.**
- **Carried into B2:** whatever closes a GROW loop must be teachable by an update to this game, or
  the game gains a pathway-scoped section stating plainly that GROW and LAUNCH close differently
  and no adult initial is expected. The estate already owns the truthful null it needs — *"Not yet
  = Voice present, Audience pending"*, staff-facing in this same game.

### R-SB01 · The site repo is the environment default — the attach warning is load-bearing
- **STATUS** RECORD · **DECLARED** (Matt, Pass SB close-out)
- Four consecutive sessions (Pass SB and three before it) opened in the **site** repo
  `mattroper1977.github.io` when the task concerned the **Lessons** repo. This is not a
  per-session slip: **the site repo is the environment's default working tree**, so any
  Lessons-repo pass that does not attach the Lessons repo first will silently measure the
  wrong tree.
- **Control:** the "ATTACH THE LESSONS REPO BEFORE PASTING" warning stays in every future
  Lessons-repo brief, and a pass's **first act** is to verify the working tree
  (`git remote -v` + presence of `resources.json`/`BUILD_ASDAN`/`Art_Teesside`) before any
  measurement. Pass SB caught it on the first act and stopped — that is the intended behaviour.

### R-SB02 · A session's harness configuration is a claim — verify it against the order's named target first
- **STATUS** CONVENTION · **VERIFIED** `a5092bb`
- **The general form.** *A session's harness configuration — working tree, checked-out branch,
  repo scope — is a claim, not a given. Verify it against the target the order names, before any
  work; and let the order's explicit target be the thing that catches a mismatch.* This is the
  executor-side control for R-SB01: R-SB01 records the recurring mis-open; R-SB02 is what makes it
  caught every time rather than sometimes.
- **Today's case (September-cluster pass).** The order named `MattRoper1977/Lessons` explicitly and
  made `git remote -v` step 0. The harness had opened in the **site** repo `mattroper1977.github.io`,
  on a `claude/september-…` branch, with GitHub scope limited to that repo — the exact R-SB01
  default. **The order's explicit repo line is what caught it:** the first act was the remote check,
  it failed against the named target, so the pass attached the Lessons repo, cloned it, re-verified
  the remote, and did all work there. The site repo was left untouched; the case-redirect
  (`MattRoper1977/Lessons`) was left alone.
- **Why it belongs in the tree, not only in a brief.** A brief that names the target while the
  harness opens elsewhere is R-H04 (delivery is part of the order) meeting R-SB01: the order is
  correct and **unexecutable against the wrong tree** — and it has **no symptom** where the wrong
  tree happens to hold similarly-named files. The control is one `git remote -v` before any
  measurement, and it has now caught the mis-open on two named passes (SB, and this one).

---

## X · Pass X (instruments) — labelling and identity discipline

*Appended by Pass X (Instrument Integrity), 2026-07-29. Append-only; no existing entry renumbered or re-spaced.
"Pass X (instruments)" is distinct from the pedagogy "Pass X" closed 2026-07-25 (measurement-only, no commits) — see R-H09.*

### R-E11 · Every recorded constant states its UNIT and its SCOPE in the same string
- **STATUS** CONVENTION · **VERIFIED** `5ee2147` (Pass X merge exchange)
- **The defect class, now its third instance.** A constant recorded without its unit or its scope, then
  re-checked by a different instrument, diverges silently — the number is right about a thing that is not the
  thing being asserted:
  - the **45-vs-50 sentinel** — a derivation divergence (two methods, one number, no unit saying which);
  - the **W8 Silver "16"** — *lines* counted, *occurrences* asserted;
  - the **"3 commits / 148 insertions" merge gate** (this exchange) — a *subset* counted (X1–X3 tools only),
    the *whole branch* asserted; it could never have matched the 4-commit branch it was meant to gate.
- **The rule.** Every recorded constant states its **unit** and its **scope** in the same string —
  *"16 lines (= 24 occurrences)"*, *"4 commits on branch (X1–X3 tools = 148 insertions; X4 records = 271)"*.
  **A gate whose constant lacks a unit is ADVISORY, not blocking, until restated. A gate that cannot say what
  it counted cannot fail you.**
- **Superseded here:** the 3/148 gate is restated as **4 commits / 419 insertions / 0 deletions (X1–X3 tools =
  148; X4 records = 271)**. Sibling of R-F06 (mechanise the rule) and R-G01 (a number that leaves its source
  needs an assertion, not a retype).

### R-G05 · The "37 of 49 KOs" figure — REFUTED AT HEAD (Pass Q)
- **STATUS** RECORD · **REFUTED AT HEAD** `c034ffd` by Pass Q (Lessons, KO triage); recorded at merge tip
  `ff0de06`. The sourced-but-unverified history below stays as the dated record; the status moves.
- Originates in **Pass G's ASDAN Knowledge-Organiser rebuild** (`9f657b6`, *"rebuild the Knowledge Organisers
  from safe sources (49 lessons)"*): rewriting the We-Do-2 targets is reported to have left **37 of 49 KOs
  disagreeing with their own slide**. It is a **content-disagreement** claim, **NOT `ko_staleness` output** —
  that instrument is temporal, reads no content and makes no correctness judgement (R-G02).
- **Reclassified** from Pass X's initial *"appears nowhere in the record"* (VERDICT_PROVENANCE.md) to **SOURCED
  (Pass G, ASDAN suite) — UNVERIFIED AT HEAD.** Its status was then unknown; checking it is a content read that
  belongs to the KO carry-forward pass, not a `ko_staleness` run. Do not re-derive it in passing (R-H07: a
  number quoted across passes inherits an authority it never earned).
- **Pass Q derivation (the refutation).** A direct read of **all 49** ASDAN KO blocks (`print-ko`) against their
  We-Do-2 slides (`print-wedo` + on-screen) at HEAD `c034ffd` found **0 of 49 disagreeing**: KO Key-Word
  definitions match the We-Do-2 matching targets; Key Facts are consistent with the taught content; wording
  variances are cosmetic, never contradictions. **The 37/49 figure does not reproduce at HEAD.** Method + full
  ledger: `_passq/TRIAGE.md` §3B. Scope: KO-vs-We-Do-2 definitional/factual read. The historical question
  (was 37/49 ever true immediately after `9f657b6`, pre Pass W/W2/F/O) is **declined as archaeology** — no
  operative value once the refutation is recorded at a named HEAD (Matt's ruling).
- **CORROBORATED independently by Pass E (KO Triage) at `12cb6d9` — same 0/49 by a different method; Pass Q
  (above) landed first, Pass E is the second, agreeing record (R-H02, D1 ruling).** Re-tested, not re-quoted (R-H07). **Method:** per ASDAN
  KO file, extract the KO key-word table terms and the We-Do-2 `match-pill` terms and count KO terms still drawn
  from the pills — the exact coupling the original 37/49 measured (KO print table generated from the game pills,
  gone stale when the pills' targets were rewritten). **Figures at HEAD (49 ASDAN KO files = 31 BUILD + 18 GROW):**
  **0/49** KO tables are still a full snapshot of the game pills; 13/49 share ≥1 term as legitimate common
  vocabulary (e.g. CAREERS_W3 `RELIABLE`/`EFFORT`); 36/49 share none. **Disposition: retired by Pass G's rebuild
  (`9f657b6`), not left unverified** — Pass G decoupled the two artefacts (KO = independently-authored real
  vocabulary; the We-Do-2 game keeps classification items, some deliberate wrong answers), so the coupling that
  made "KO disagrees with the game" meaningful no longer exists. The live question — is each KO stale against its
  *lesson* — is the `ko_staleness`/Tier-1 question; all 49 ASDAN KO files appear in Pass E's 117-candidate set and
  were content-read (all 49 STILL-TRUE). This resolution closes only the game-disagreement claim, not
  lesson-staleness. (Pass E self-renamed from provisional letter Z, spent by the pedagogy *Pass Z* of 2026-07-25;
  see "## Pass E (KO Triage)" at the end of this file, R-E16, and `_passe/KO_TRIAGE_LEDGER.md`.)

### R-H09 · A pass letter is checked against the ledger AND git history — git alone is blind to measurement-only passes
- **STATUS** CONVENTION · **VERIFIED** `5ee2147`
- **The instance.** *"Pass X"* was adopted for Instrument Integrity after a git grep showed the letter free.
  But a pedagogy *"Pass X"* (tier-structure, **closed 2026-07-25**) was **measurement-only and left no commits**,
  so it is **invisible to a git-history check**. Same shape one turn earlier: a prior content *"Pass W"* existed
  in commit **subjects** (`2976816`, `71751d2`) and was missed by a `*.md`-only grep — and the earlier **Pass O**
  double-use. Three instances ⇒ a class, not a coincidence.
- **The rule.** A pass letter is checked against **`REGISTER.md`/`HANDOVER.md` AND git history** before adoption.
  **A measurement-only pass leaves no commits**, so git is necessary but not sufficient; the ledger is the other
  half. **Disambiguator recorded:** *"Pass X (instruments)"* — this pass — vs *"Pass X (pedagogy, closed
  2026-07-25)"*.
- **The cross-repo clause (Pass Q, the blind spot in the other direction).** The letter check must consult
  **BOTH the Lessons AND the site (`mattroper1977.github.io`) repos' records** — this ledger structurally
  cannot see site-repo letters, and a check confined to one repo is blind to the other's spent letters exactly
  as a git-only check is blind to measurement-only passes. **Instance:** Pass Q was cut in Lessons after Z
  collided; "Pass Q" was already spent on the **site repo** (quality sweep, closed `6845f44` there), unseen
  from here. **Dispositioned, NOT renamed:** commits existed and a mid-flight rename is worse than a named
  collision. **Disambiguator recorded:** *"Pass Q (Lessons, KO triage, `38c8f6b`)"* vs *"Pass Q (site repo,
  quality sweep, `6845f44`)"*.
- **The Careers note, verified against the repo (Ruling 5), because the repo wins.** The Careers **W6/W7 swap**
  is **Pass H** (`9d19450`, *"post-16 moves to W6, career profile to W7"*) — a **relabel**: the filenames keep
  their old week numbers, the slot labels swap. It was reverted by the prior *Pass W* and restored at `0706782`.
  **Pass SB's `143a194`** fixed *"of 6"→"of 7"* on **W1–W5 only**; **Pass U** (timber HT/MB verification, closed)
  and **Pass X** touched **none** of these files — confirmed by diff. The three do **not interact**; recorded so
  no later session re-opens it. (Earlier Pass X drafts mis-attributed the swap to Pass U — corrected here: it is
  Pass H, per the commit.)

### R-E12 · An instrument's assumptions ship with its result — and the banner routes by stream
- **STATUS** CONVENTION · **VERIFIED** `15fdb0e` (Pass Y)
- **The rule.** Every result-printing instrument prints the assumptions it rests on **beside the result**
  (`assumptions: full clone · 161-file corpus · network not required`), so no number is ever read alone —
  the discipline that would have surfaced the shallow-clone false zero (R-E11 / Pass X) years earlier.
- **The routing, and it is load-bearing.** The banner goes to **STDERR when the tool's stdout is a machine
  surface** (JSON: `identity_audit`, `hash_sweep`, `link_graph`, `print_pack_audit`, `assessed_conditions_gate`)
  — a text line on a JSON stdout corrupts every downstream `json.load`/`jq`, which is the **same fail-silent
  parser-break the banners exist to prevent, arriving from the other side.** It goes to **STDOUT for a
  human-read tool** (`sitemap_audit`, `verify_commit_set`, `ko_staleness`).
- **The durable rule is RESPECT THE OUTPUT CONTRACT, not enumerate the consumers.** A Pass Y census found no
  in-repo consumer, CI, shell or Makefile parsing any tool's stdout (`*.sh/*.yml/*.yaml/*.py/Makefile`) — but
  a census **cannot** cover consumers outside the repo: another session's scripts, a Cowork run capturing
  output, any machine not in view. So "found no consumer" is **never** a warrant to put prose on a machine
  stdout. **A tool that emits JSON on stdout has a machine contract whether or not a consumer is visible
  today, and stdout stays clean by default.** (Following an instruction to the letter — "no consumer, so add
  the banner to stdout" — would have shipped a rollout that broke quietly and later: the exact fail-silent
  shape Pass X exists to close.)
- **The failure signal is the EXIT CODE, never the emptiness of stderr.** An `assumptions:` line on stderr is
  **not** an error — stderr is where an ordinary run's banner lives. Nothing may ever be built that reads a
  non-empty stderr as failure; that re-introduces the fail-silent shape one layer out. A guard fails loud by
  **exiting non-zero** (preflight exit 3, sitemap exit 2), which is the only signal a caller reads.
- **A library declares, it does not print.** `classify.py` has no result surface, so it exports its
  assumptions as **data** (`ASSUMPTIONS`); its caller `print_pack_audit` **reads** and prints them,
  attributed. A hand-copied restatement in the caller would be two copies of one truth (R-G01 / standing
  rule 2, emit-don't-transcribe). Proof it is read: change a value in `classify.ASSUMPTIONS` and the audit's
  banner changes with no edit to the audit.
- **`loop_mark_print_gate` has no banner yet, and that is a FINDING, not a to-do — see R-E13.**


### R-E13 · `loop_mark_print_gate` is FAIL-SILENT BY ABSENCE in the agent sandbox — a finding, not a to-do
- **STATUS** OPEN · **VERIFIED** `45f0c63` (Pass Y) — the *absence* is verified; the gate's own verdict is not
- **Precondition, stated explicitly:** LL-INST-09 (`loop_mark_print_gate.py`) needs **playwright + Chromium**
  to run — it renders each file at `media=print` and reads back what printed. **That environment is absent in
  the agent sandbox** (`from playwright.sync_api import sync_playwright` → ModuleNotFoundError).
- **Why it is a finding, and the class Pass X did not census.** An instrument that cannot run **in the
  environment where passes are executed** is **fail-silent by absence**: it never runs, so it never reports,
  so its silence is **indistinguishable from a clean result.** That is Pass X's own thesis — a false zero from
  a check that never examined the thing — pointing at a class Pass X's census (git / network / corpus /
  encoding / parse-shape) did not include: *the instrument that is simply never invoked here.*
- **What remains unproven without it.** No `loop_mark_print_gate` verdict exists at current HEAD; the
  print-reaches-paper claims it checks (R-A07 family) are **unverified by this instrument in every agent-run
  pass**, including Pass Y. The Pass Y assumptions banner was **not** added to it — a banner proved on no run
  is an unasked question (R-E12 / standing rule 6).
- **Disposition.** Not a special errand. It **attaches to whichever future pass legitimately runs in a
  Chromium-capable environment** — that pass adds the banner (proving gate (c) on a real render) and takes the
  gate's verdict. Until then, treat any absence of a `loop_mark_print_gate` result as *not run*, never as
  *clean*.

### R-H10 · A training artefact's corrective content must live on the surface the trainee actually uses
- **STATUS** CONVENTION · **DECLARED** (Matt, Pass LL-I — the calibration rebuild)
- **The general form.** *A correction reachable only off the training path trains nobody who stays on it.* Where a
  training artefact has a surface the trainee actually operates — a game's questions, a checklist's items, a form's
  fields — corrective content placed anywhere else (a preface card, a footnote, a summary) reaches only the trainee
  who leaves the path to read it, which is not the one who needs correcting.
- **The case.** `LundyLoop/5_staff_training/R_Gate_Calibration_Game.html` at `a5092bb` carried a faithful, complete
  GROW/LAUNCH correction — a pathway card, a re-scoped summary, a named false record — **entirely outside the
  fourteen questions**, every one of which still taught the BUILD adult-receipt close (R-H08). A TA playing to
  completion answering questions only met the correction as a card they could skip plus one summary sentence. The
  design's own test was *teachable-by-update*, and **an update the trainee can complete without meeting is not
  teaching.** Caught by a paper read asking *where in the flow the pathway questions were* — not by any instrument.
- **The fix that earned this entry:** two GROW/LAUNCH scenarios authored **into the question array itself** (pathway
  named in the question text, correct answer inside the game's answer model), so a question-only TA now meets both
  closes on the surface they use. R-H08 stays OPEN pending the paper read of the rebuilt game.

### R-E14 · Extending an artefact by one case can require editing the shared model it scores against
- **STATUS** CONVENTION · **DECLARED** (Matt, Pass LL-I — the calibration rebuild)
- **The general form.** *An additive change is not always an additive edit.* Adding one item to a set scored against
  a shared model (a legend, a rubric, a schema, a gate's predicate) can be un-expressible until the model itself is
  broadened — and broadening a shared model re-scores **every** item already measured against it. **The keyer
  lesson: fixing a definition upstream moves everything downstream, and the manifest is only the first consumer you
  notice.**
- **The case.** Two GROW/LAUNCH scenarios could not be added to the calibration game truthfully: the only "closed"
  label was legend-defined as *"Voice happened AND an adult genuinely received it"* — BUILD-only, and the card had
  already scoped it there. The correct answer for a GROW close had **no truthful label** — exhausting all four was
  the method that proved the gap, not assumed it (the §2-constraint-1 stop). Adding the two scenarios **forced**
  broadening label 0's legend to be pathway-relative (Option 1): *Closed = the loop reached its pathway's close;
  BUILD an adult received it (R), GROW/LAUNCH the pupil wrote the line.* A shared-model edit, not an array append.
- **The gate this creates, and it is the point.** A shared-model edit re-scores every existing item, so **every one
  is re-verified against the new model before the edit ships** — here all fourteen pre-existing scenarios, one line
  each, correct-answer-before vs correct-answer-after: **all fourteen unchanged** (the BUILD branch preserves
  adult-receipt exactly). *Any* item whose correct answer had moved would have been a STOP — a shared-model edit that
  silently re-scores existing training is worse than the gap it closed. The rejected alternative (Option 2 — leave
  the legend false for two of sixteen items, rely on a card outside the flow to rescue it) was refused as both a
  cached-claim and a second instance of R-H10.

### R-E15 · A pass perturbs the corpus its own instruments measure — verdict-invariance is a SAME-TREE proof
- **STATUS** CONVENTION · **VERIFIED** `eea4062` (Pass Y close; earned by the gate-(c) DIFFERS diagnosis)
- **The rule.** A pass adds files to the tree — `_passX/` records, `FINDINGS`, `REGISTER`/`HANDOVER` edits —
  and those files are **corpus members** of any instrument scoped to the tree (`identity_audit`, `hash_sweep`,
  `link_graph` scan *all* tracked files; `print_pack_audit`/`assessed_conditions_gate` scope to `*.html`/the
  two assessed files and so do **not** move). Therefore a corpus-scoped verdict is **NOT invariant across a
  before/after TREE comparison** — the pass changed the corpus, not only the tool.
- **How invariance is actually proved.** A **CONTROLLED SAME-TREE comparison**: the same tree, the instrument
  **with and without** the change (swap the pre-change tool in place — resolve `REPO` from `__file__`, so run it
  from the real tools dir, never a copy elsewhere), and compare stdout. That, plus "stdout is valid JSON with
  zero banner lines", is what proves a change added nothing to the verdict. The gate-(c) DIFFERS in Pass Y had
  an easy wrong reading — *banner leakage* — sitting right beside the true one: the pass's own new `_passy/`
  file entered the corpus. The same-tree re-proof is the instrument that tells them apart.
- **The presumption, so the next session does not hunt a phantom.** A corpus count that **moves across a merge
  is PRESUMED corpus growth until the same-tree comparison says otherwise** — reconcile before reporting a
  defect. **Corollary for merge sessions:** after each of several merges (the in-flight branches in
  `HANDOVER.md`), expect corpus-scoped figures to move; **that movement is arithmetic, not regression.**
- **One family with R-E11 and R-E12.** An instrument's number means nothing without its **unit** (R-E11), its
  **stream** (R-E12), and its **tree** (this entry). All three are the same lesson: a count read without its
  frame is a false signal waiting to be believed.

### R-H11 · A control is only demonstrated by the case where obeying it is inconvenient
- **STATUS** CONVENTION · **DECLARED** (Matt, H-series H3)
- **The general form.** *A control is only demonstrated by the case where obeying it is inconvenient — the
  near-match that fires nothing is the proof, not the friction.* Sibling to the existing rule that **an
  instruction that only holds when nothing pushes back is not a control**: a gate that fires on "near enough"
  is not a gate.
- **The case.** The R-H08 closure and the Route triggers were held under an exact-match rule — a bare line
  reading *exactly* the trigger, nothing before or after. Across one exchange, several trigger-shaped lines
  arrived that were **not** the bare line: a one-word truncation (`R-H08 read passed — close`, missing "it"),
  triggers wrapped in a prefix or a suffix, a trigger heading a whole amendment document, a bodyless amendment
  filename, and confirmations of undelivered documents. **Every one fired nothing** and took a one-paragraph
  disposition; the line that *was* the bare trigger fired, and only then. Interpreting any near-match would have
  closed a gate on an unverified premise and written it into the tree — the cost the exact-match rule buys back
  for the price of a paragraph.
- **The corollary.** When a control is tested repeatedly and each near-match is refused, the refusals **are**
  the evidence it holds; a control never pushed against is untested, not trusted. (Owed by the H-series order's
  confirmed H3 register-payload amendment; carried here, next free letter at author time.)

---

## Pass E (KO Triage) — collision record and outcome

*Appended by Pass E, 2026-07-29. Append-only; no existing entry renumbered. This pass ran the KO-triage body of
the Q/U/X/Y instrument chain. Named `## Pass E …` (not `## E ·`) because the section-letter `E` is already taken
by "§E · Instruments and metrics"; pass-letter E and section-letter E coexist as pass-letter H already coexists
with §H and the R-H## rules.*

*Renumber note: these entries were authored as R-E13/E14/E15 at base `12cb6d9`, where those numbers were free; the H-series/RL work added estate entries R-E13–R-E15 to §E meanwhile, so at the merged tip Pass E's three renumber to **R-E16/R-E17/R-E18** (R-E11 constant discipline applied to rule numbers; the estate's R-E13–15 are untouched).*

### R-E16 · Provisional letter Z was spent — renamed Z → E (R-H09 applied)
- **STATUS** RECORD · collision resolved
- **The collision.** The pass was briefed with provisional letter **Z**. R-H09 (ledger AND git) found **Z spent**:
  a pedagogy *Pass Z* left two commits merged to main — `453b5e6` *"Pass Z: differentiate Careers W7 from W6"*
  and `d5c8cf1` *"Pass Z remediation: LI W5 becomes a budgeting task…"* (both 2026-07-25). Ledger carried no
  `Pass Z`, so git was the half that caught it — the mirror image of R-H09's original instance.
- **The rename.** Free pass-letters (absent from both git subjects and the ledger) were **E and I only**; `N` is
  taken by HANDOVER's "Pass N print-reference pattern". **E** chosen as the lowest free letter. Branch
  `pass-e-ko-triage`; deliverables `_passe/`; rollback SHA `12cb6d9`.

### R-E17 · The carry-forward's artefact shape no longer described the estate — recorded, not inherited
- **STATUS** RECORD · **VERIFIED** `12cb6d9`
- Re-derived candidate count at HEAD: **117** (not the carried 114; the constant had worn 117→109→114 and is
  re-derived per R-E11, +3 within tolerance). Cardinality `117 + 0 arch + 44 clean = 161` KO files, emitted.
- **The break.** The carry-forward characterised 39 "R-E07 Loop-Mark artefacts" as the cheap first clear. At
  HEAD the Loop-Mark strip (R-E07's own verified remedy, re-run as a diff-class test) cleared **0 of 34** such
  files, and **0 of 117** candidates were chassis-only: the Loop Mark (2026-07-28) is the most-recent mover, but
  Pass F/O/W/W2 (07-24/25) and the art-remediation merge (07-29) moved the same bodies earlier. The halt-gate
  fired and was reported before Tier 2. All 115 non-assessed candidates were then content-read: **112 STILL-TRUE,
  3 STALE** (Careers W6/W7 KO week-labels lagging the restored slot-swap; BUILD_HUM_W6 KO on the pre-PEEL 4-part
  model). The three STALE fixes are held UNMERGED on `pass-e-ko-triage` for Matt's per-row key. Detail:
  `_passe/KO_TRIAGE_LEDGER.md`.
- **Coexistence (R-H02): the same briefed pass also ran as Pass Q, which LANDED FIRST on `main` (`59ad56a`)**
  — 0 STALE / 114, R-G05 refuted 0/49, a CAREERS_W7 *print* fix. Pass Q holds; **Pass E corroborates R-G05
  independently (0/49 == 0/49)** and adds 3 STALE on axes Pass Q's KO-vs-We-Do-2 read did not cover (KO h1
  week label; HUM writing-model completeness), all pre-dating Pass Q's head. This entry is the second, honest
  record — not a competing claim. `REGISTER.md` and `CAREERS_W7` will conflict at merge (both passes touched
  them); resolution is Matt's, at the merged tip. Full reconciliation: `_passe/COEXISTENCE_PassQ.md`.

### R-E18 · Pass E LANDED — Matt's rulings D1–D3 (2026-07-29)
- **STATUS** RECORD · landed by merge onto `main` from `pass-e-land` (base = `main` tip at land time)
- **D1 · IDENTITY — Pass E stays DISTINCT, sibling-of-Q(KO); not folded, not retired.**
  - **(a) Cross-ref E↔Q(KO):** Pass E and Pass Q are the **same brief, twin runs** — both were given provisional
    letter Z, both found it spent (pedagogy *Pass Z*, 2026-07-25), both self-renamed (Q, then E). **Pass Q landed
    first**; **Pass E corroborates R-G05 independently (0/49 == 0/49)** by a different method and adds three STALE
    on axes Pass Q's KO-vs-We-Do-2 read did not cover. Neither supersedes the other; both records stand.
  - **(b) Letter disambiguation — "Q" is now overloaded:** it names **both** the **site-repo sweep** (repo
    `mattroper1977.github.io`, `@6845f44`) **and** this Lessons **KO triage** (`ff0de06`). Future notes citing
    "Pass Q" **must say which** — *"Pass Q (site sweep)"* vs *"Pass Q (KO triage, Lessons)"*. (Sibling of R-H09's
    cross-repo clause: the letter namespace is not repo-local.)
- **D2 · FIXES — all three approved, LANDED.** E1 `CAREERS_W6` KO h1 `W6→W7`, E2 `CAREERS_W7` KO h1 `W7→W6`
  (as-found, KO-text token only, four-surface agreement proven post-edit); E3 `BUILD_HUM_W6` +1 KO row `Link`
  (Phase-3 gates: body still teaches Link; wording from this file's own link bank, not GROW_HUM_W6's KO; exactly
  one row; Pass-G rule holds). **No STOP, no PROPOSED-only outcome — all three passed their gates and landed.**
- **D3 · ASSESSED RESIDUE — `GROW_HUM_W7` UNTOUCHED** (assessed quarantine). The `Evaluation clause — Deployed
  provenance honesty` KO row is logged verbatim in `_passe/ASSESSED_RESIDUE_HELD.md` as HELD-FOR-SCOPED-PASS;
  it lands only on Matt's explicit word.
- **Counts pre/post (deploy-visible):** 3 KO print sheets changed; `<tr>` totals `21→21`, `21→21`, `23→24`;
  print-pack section counts and `prefers-reduced-motion` rules invariant; sentinel `ll-g:loop-mark` set invariant
  at **45**; all inline `<script>` blocks byte-identical to base + `node --check` clean; Chromium headless boot +
  strict DOM parse clean on all three. Instruments untouched (R-E09).

---

### R-D05 · The ASDAN/PEQ work lives in the Lessons repo — sessions default to the site repo
- **STATUS** RECORD · **VERIFIED** Pass PQ (base `32ca685e`)
- **The BUILD/GROW ASDAN provision, the Evidence Binder and the PEQ audit all live in
  `MattRoper1977/Lessons`.** Sessions commissioned to work on them keep opening in the
  **site repo** (`mattroper1977.github.io`) instead, because that is the working tree the
  harness attaches by default.
- **Pass PQ is the FIFTH recorded instance.** The brief warned of it explicitly ("three
  prior sessions defaulted to the site repo"); Pass PQ's own session opened in the site
  repo and caught it at the attach-check before any audit ran.
- **The control is two-part and neither half is optional:** (1) the warning stays in every
  ASDAN/PEQ brief; (2) the session's **first act** is an attach-check — `git remote -v`
  against the expected `Lessons` origin, and STOP if the working tree is the site repo,
  attaching Lessons before anything else. A brief warning without the attach-check let three
  sessions through; the attach-check is what stopped the fourth and fifth.
- **Why an entry and not just a memory:** a recurring cross-session default has no in-tree
  symptom — the wrong repo is a perfectly valid repo — so nothing detects it but the
  discipline of checking the remote first. This is the R-G01 cached-claim shape one layer
  out: the claim "I am in the right repo" is asserted by every session and kept true by
  nothing but the check.


### R-RL01 · Pass RL — re-land PQ + SG + Phase-3, close the SoW alignment chain
- **STATUS** CLOSE · **VERIFIED** Pass RL (base `59ad56a`, merge `faf5318`)
- **Forensic verdict (why RL existed).** Ancestry proof found only SB (`4f5c6a4`) on
  `main`; **PQ (`b137a90`) and SG (`dc41a56`) had NOT landed** — verified by *content*, not
  tip SHA: `_passpq/`/`_passsg/` trees absent, `R-D05` absent, no `pass-pq`/`pass-sg`
  commits in `a5092bb..59ad56a`. Both branch refs survived at origin and were the re-land
  source.
- **What merged (estate main-wins; `_passXX` branch-wins; REGISTER append-only union).**
  - `_passpq/` — 8 deliverables, byte-identical to `b137a90`; **`R-D05` appended** (main's
    62 entries otherwise untouched; SG added none — main already supersets its ledger).
  - **T2-1** doubled-label fix applied **by MEASUREMENT**: `ASDAN Studio · ASDAN Studio` →
    `ASDAN Studio`, **49 files (BUILD 31 + GROW 18), 98 → 0**. *(Master prompt predicted 0
    at BASE; measured 98 — the `>0` branch was taken. `<script>`/reduced-motion blocks
    byte-identical; tag counts unchanged; GROW packs section count invariant.)*
  - `_passsg/` — FINDINGS (incl. §11.8), SOW_MATRIX, `inputs/GROW SOW 2026-27.xlsx`,
    byte-identical to `dc41a56`.
  - **SG content** re-derived on main's current 8 `Grow/Slideshows/GROW_ART` files
    (cdc9623 file states NOT reintroduced): predicate `GCSE Stretch` + `GCSE Art habit`
    **17 → 0** (`GCSE Stretch:`→`Bronze Stretch:` ×16; `Bronze / GCSE Art habit`→
    `Bronze Art habit` ×1). *(Master prompt predicted 0 in `Grow/Slideshows`; measured 17 —
    the earlier forensic 0 read `Art_Teesside/Grow`, the wrong tree.)*
  - **Phase 3** — 8 LAUNCH Art slideshows `launch-art-aut1-w1..w8` subject `Art`→
    `Arts Award`, **re-derived** on main's current `resources.json` (main had advanced to
    **386** entries): total 386 unchanged, **Art 42→34, Arts Award 0→8**.
- **SUPERSEDED / deviation rulings (logged honestly).**
  - The retired `Bronze Stretch = 16` constant is now **true post-edit** (16) as a natural
    consequence of `GCSE Stretch`→`Bronze Stretch` — not treated as an independent gate.
  - **2 non-predicate GCSE mentions** (`GCSE development page`, `GCSE habit`) left in the 8
    files per the narrow predicate + "task text unchanged"; recorded, not changed.
  - **Sentinel `ll-g:loop-mark` set:** estate set unchanged (**50**); full-repo **+1**
    (`_passsg/FINDINGS.md`, a required deliverable that cites the sentinel string in prose).
    No lesson/estate witness surface changed.
  - Residual whole-repo doubled-label count **1** = `_passpq/FINDINGS.md` quoting the defect
    name (documentation, not estate).
  - **Protected verbatim** `Art_Teesside/Grow/GROW_ART_W8…` blob **`4cf5d81e`** byte-identical
    (24 occurrences of "Silver" across 16 lines — corrected F-11 units).
  - **EXCLUDED, untouched (await committed spec / Matt):** T2-2, T2-3, T2-4 learner-signature,
    Slideshows tiering rebuild.
- **Gates.** JSON parses; counts 386/34/8; **155** inline script blocks parse-clean; jsdom
  boot of all **57** touched lessons 0 errors; jsdom real-hub `Arts Award (8)` + `Art (34)`,
  `Showing 393 of 393`, 0 console errors; tag balance clean; W8 blob protected.
- **SBX probe (report-only, NOT merged).** `pass-sbx-art-a2` C1 (Bronze→Explore in BUILD A2
  decks) is **absent at final main** (`Explore Part` = 0, `Bronze Part` = 21). Left for Matt.
- **Ancestry after land:** PQ `b137a90`, SG `dc41a56`, Phase-3 `710c888`, SB `4f5c6a4` all
  ancestors of `main`.

### R-SC01 · Season close — reconciliation at landed main `8540eee`, proven by content
- **STATUS** CLOSE · **VERIFIED** by content at `8540eee` (never by SHA alone)
- **Season ledger — each strand probed at the tip:**

| strand | landed? | content proof at `8540eee` |
|---|---|---|
| **SB** | ✓ | `4f5c6a4` ancestor; R-SB01 present; all 7 Careers files read `Week N of 7`, none `of 6` |
| **PQ** | ✓ | `_passpq/` = 8 docs + `inputs/README`; R-D05 present; doubled `ASDAN Studio · ASDAN Studio` = **0 in the estate** (2 residual hits are documentation prose: `REGISTER.md` R-RL01 + `_passpq/FINDINGS.md`) |
| **SG** | ✓ | `_passsg/` (3 files) incl. FINDINGS §11.8; `GCSE Stretch`/`GCSE Art habit` = 0 in the 8 GROW_ART Slideshows (2 non-predicate `GCSE` mentions remain, per R-RL01); `Art_Teesside/Grow/GROW_ART_W8…` blob `4cf5d81e` byte-identical |
| **P3** | ✓ | `resources.json`: total **386**, **Arts Award = 8**, Art = 34 (hub chip render was RL-jsdom-verified; content is ground truth here) |
| **Q (KO)** | ✓ | `_passq/` (6 files) present; REGISTER carries `R-G05 · … REFUTED AT HEAD (Pass Q)` |
| **E** | ✓ | 3 KO sheets four-surface green (W6 file = Week 7, W7 file = Week 6 — the deliberate swap); BUILD_HUM_W6 `Link` row present; R-E16/R-E17/R-E18 + renumber note; `_passe/` = **4 files** incl. `ASSESSED_RESIDUE_HELD.md` |

- **Corrections to the expected close (invent nothing):** `_passe/` holds **4** files, not the brief's "5" — the four are the ledger, coexistence, R-G05 append, and assessed residue; nothing is missing. Estate sentinel `ll-g:loop-mark` set = **45 files** (whole-repo 51) — the brief/R-RL01 "50" does not reproduce; recorded, estate witness surface unchanged.
- **Cross-merge integrity.** Instruments byte-identical vs BASE `59ad56a`, `cc45b37`, and `12cb6d9` (0 diff — R-E09). REGISTER append-only: **67** entries at main = `cc45b37`'s 64 + Pass E's 3 (R-E16/17/18); no entry from either merge parent lost; no duplicate IDs.
- **S2 · SBX (report-only, NOT merged): NOT-LANDED.** `pass-sbx-art-a2` C1 Bronze→Explore absent in the 7 BUILD A2 decks — `Explore Part` = 0, `Bronze Part` = 21 (re-probed by content; matches R-RL01). Branch retains 5 unique commits; left for Matt.
- **S4 · Assessed residue (`GROW_HUM_W7` `Evaluation clause` KO row): HELD, AWAITING-WORD.** It is a pupil-rendered `<td>`, so it fails S4's non-pupil-rendered commit gate; the proposed single hunk is held verbatim in `_passe/ASSESSED_RESIDUE_HELD.md` and `GROW_HUM_W7` is byte-untouched. The file's three `Reference Zone` strings are the assessed guard (*"Do not print a Reference Zone into this session"*), correct design, not residue.
- **Open items & branch-deletion candidates:** `_close/OPEN_ITEMS.md` (record-derived; 6 open items + 11 zero-unique-commit branches enumerated for Matt's UI deletion; 4 branches with real unique work flagged do-not-delete).

### R-E19 · Assessed residue resolved — `GROW_HUM_W7` `Evaluation clause` KO row REWORDED (Matt's word)
- **STATUS** CLOSE · assessed single-hunk, landed under Matt's authorisation (Claude concurred)
- **Decision by measurement (not by assumption).** The concept is taught **10 times** in `GROW_HUM_W7` itself
  — slides (*"The Brackets: Provenance notes → evaluation lines"*), the match-game, the Steps summary
  (*"every unit carries one evaluation clause"*), and print sections (*"One evaluation clause per unit
  (brackets deployed)"*), excluding the KO row and the Reference-Zone guard. ≥1 occurrence ⇒ **REWORD, not
  remove**: the key word is live taught content, so deleting it would have *broken* the Pass-G snapshot rule,
  not restored it. "Deployed" was the lesson's own vocabulary, not a stale echo — the residue flag was a false
  alarm on that word, correctly resolved by rewording the terse definition rather than excising the concept.
- **The hunk (landed).** `Evaluation clause` definition cell only:
  `Deployed provenance honesty` → `A per-unit bracket that turns provenance notes into an evaluation line`
  (drawn verbatim-in-substance from the lesson's own teaching; no new concept). Whole-file byte-diff = this one
  hunk; three "Reference Zone" guard strings byte-identical; scripts byte-identical + `node --check`; Chromium
  boot clean; tag balance; print-section count 14→14; KO row count unchanged (reword). `GROW_HUM_W7` otherwise
  byte-untouched. Record: `_passe/ASSESSED_RESIDUE_HELD.md` (status RESOLVED).
- **Sentinel corrigendum:** not appended separately — **R-SC01 already records** estate `ll-g:loop-mark` = 45
  (vs R-RL01's "50"); R-RL01 itself left untouched (append-only).

### R-E20 · T2-4 learner-signature APPLIED on branch — HELD for Matt, not merged
- **STATUS** RECORD · branch `pass-pq-t24-learner-signature` (base = `main` tip `a4cdd36`); **NOT MERGED —
  held for Matt's read** (same pattern as the CAREERS_W7 print fix). `_close/OPEN_ITEMS.md` #1 stays OPEN
  until Matt's word; this entry records the prepared diff, not a landing.
- **Provenance — committed records only.** The authorised-but-unexecuted T2-4 diff (Pass PQ close-out item
  5a) recovered from `b137a90` + `_passpq/FINDINGS.md` §Tier-2 T2-4 + `_close/OPEN_ITEMS.md` #1. `b137a90`
  itself touched **no estate file** (docs + R-D05 append only); the diff is the additive block specified
  **verbatim** in FINDINGS. §2 of the PEQ spec requires records signed by assessor **AND** learner; the
  witness statement carried assessor sign-off only.
- **What applied.** Additive **`5 · Learner confirmation`** block (heading + "I confirm this is my own work."
  + name/signature/date table) inserted **after the §4 Assessor declaration table**, before the statement's
  closing note, in **all 49 ASDAN witness surfaces (BUILD 31 + GROW 18)**. The protected assessor block
  (§4) is **byte-untouched**; the change is purely additive.
- **Semantic re-apply at HEAD (b137a90 is stale).** Pass RL re-landed the same 49 files (T2-1 `ASDAN Studio`
  de-double); the diff was **re-applied by measurement** at `a4cdd36`, not replayed from `b137a90`. RL's
  landed fixes are preserved byte-for-byte (script/reduced-motion blocks byte-identical to base; sentinel
  set unchanged). Anchor was the byte-uniform closing-note line, verified present exactly once and directly
  after the assessor `</table>` in **49/49** files.
- **Population.** File count at HEAD = **49** (BUILD_ASDAN 31 + GROW_ASDAN 18), matches FINDINGS — **no
  delta**. Six `Build/Slideshows/BUILD_DT_W1..W6` files also carry witness statements but are the **BUILD DT**
  strand, **out of T2-4 scope** (T2-4 is the ASDAN witness surfaces) — deliberately untouched.
- **Gates (stated per the T2-1 pattern, asserted at branch tip).** 49 files, **245 insertions / 0 deletions**
  (`+5`/file); per-file byte-diff confined to the inserted witness lines. Sentinel `ll-g:loop-mark` set
  **invariant at 45** — R-SC01's corrected constant, not R-RL01's "50" — empty set diff before/after.
  **147** inline `<script>` blocks `node --check` clean and byte-identical to base; reduced-motion blocks
  byte-identical (0 files differ). jsdom DOM parse **0 errors on 49/49**, learner block confirmed inside
  `#print-witness`. Tag balance clean. Print/screen parity: witness + learner block confined to `#print-area`,
  **no on-screen copy** (49/49) — additive change introduces no divergence.

### R-E21 · T2-4 learner-signature MERGED to main — Matt's approval (2026-07-29)
- **STATUS** CLOSE · merged **no-ff** at `bc215d1` (parents `a4cdd36` + `013121e`, branch tip anchored);
  **rollback SHA `a4cdd36`**. R-E20 (the diff record) rode in with the merge; not duplicated here.
- **Authorisation.** Matt's explicit merge-and-close order (2026-07-29), after reading the old→new table and
  gate results. **Supersedes R-RL01's "EXCLUDED" framing** (superseded, not contradicted) and satisfies
  `_close/OPEN_ITEMS.md` #1 — now **CLOSED**. T2-4's gate was Matt's explicit word (unlike T2-2/T2-3, which
  still need the committed spec).
- **Re-proof at the merged tip.** Byte-diff vs rollback `a4cdd36` confined to the **49 ASDAN files** (`+5/−0`
  each) + `REGISTER.md` + `_close/OPEN_ITEMS.md`; **no pupil-facing diff beyond the learner block**. Sentinel
  `ll-g:loop-mark` set **invariant at 45** (empty set diff). RL's `ASDAN Studio` de-double **intact** (0
  doubled on the 49). **147** inline `<script>` blocks `node --check` clean; jsdom **49/49** with the learner
  block inside `#print-witness`.
- **New open item (my finding — no fix).** The 6 `Build/Slideshows/BUILD_DT_W1..W6` witness statements carry
  **no §5 learner line** — out of T2-4 scope (ASDAN-only), correctly untouched. Whether DT evidence needs the
  same additive §5 block is **Matt's decision, AWAITING-WORD** (`_close/OPEN_ITEMS.md` #7).

### R-E22 · A visibility gate hides with `visibility`, never with `opacity` alone
- **STATUS** CONVENTION — read before adding an animation layer
- **SELECTOR** `node Science_Teesside/launch-engine/test/gate-shape.js`
- An `animation` carrying `fill-mode: both` or `forwards` applies its final
  keyframe in the **CSS animation origin**, which outranks every normal author
  declaration *regardless of selector specificity*. A keyframe ending at
  `opacity: 1` therefore defeats `opacity: 0` from any rule, however specific.
  No keyframe in this estate sets `visibility`, so a gate pairing the two cannot
  be defeated by adopting a shared class.
- **Measured, not reasoned.** All 23 fill-mode classes were applied to all 9 gate
  styles in a browser and the held value read. Every `grow-anim` and `build-anim`
  gate held. The three opacity-only gates in `launch-engine` were defeated by 12
  of the 23, and one was live — a spotlight painting over the specimen before any
  pupil act.
- **The estate was already right by convention and a newcomer missed it.**
  `[data-part].g-hidden`, `[data-label]`, `[data-grow-step]`, `[data-overlay]`,
  `.ba-hidden` and `.ba-label` have always paired the two. That is exactly the
  kind of correctness that decays silently, so it is now enforced rather than
  merely true.
- **Not a blanket `opacity:0` scan.** Only 5 opacity-only rules exist tree-wide
  and two are legitimate transients; flagging all of them would repeat R-E05's
  false-positive pattern. `gate-shape.js` asserts a known inventory and flags
  anything new, which is decidable.
- **Two gates in other layers carry the old shape and are recorded, not fixed:**
  `.at-reveal` (`BUILD_ASDAN/_framework/asdan-teach.css`) and `.lo-item`
  (`build-engine/core/styles.css`). Neither is leaking today; both are one
  adopted class away. Listed in `reports/INSTRUMENT_INDEX.md`.

### R-G06 · A count is meaningless without its universe (Pass SCI, 2026-07-29)
- **The rule.** A number is not a measurement until its **universe** is named. Two axes have to be
  stated every time: *tracked (git) vs working tree vs raw filesystem*, and *`*.html` vs all files*.
  The same sentinel read **45 · 51 · 70 · 76 · 79 · 235** across one pass — none of them a counting
  error, all of them universe errors:
  - **45 / 70** — tracked `*.html` at `8540eee` / at HEAD after the 25 science lessons. The gate's
    universe (`grep … -- '*.html'`), and the only stable one. Delta +25, exactly the lessons.
  - **51 / 79** — all-files at fork / now. *Unstable*, and this is the finding: it grew by more than
    the 25 lessons because the pass's **own committed tooling mentions the string it counts**
    (`render_v5.py`, `sentinel.py`, `FINDINGS*.md`, and this `REGISTER.md` — 13 mentions here alone).
  - **76** — a *predicted* `51+25`, never derived. The cached-claim shape (R-G01) in one number.
  - **235** — a raw filesystem grep that swept the gitignored `out/` and `pack/` build artefacts.
- **The corollary (the reusable half).** An instrument that **names** the sentinel it counts **joins
  the population it counts.** Every sentinel emitter must therefore exclude its own tooling and the
  gitignored trees **explicitly, and say so in its output** — not merely in its code, or the exclusion
  is itself an unverifiable claim. `_passsci1/sentinel.py` now derives from `git grep … -- '*.html'`
  (tracked only, artefacts excluded by construction) at emit time and prints both the universe and the
  file list. No number is carried between reports.
- **The family.** This is the R-G01 / R-G03 cached-claim shape one axis further out: R-G01 is prose
  asserting something about elsewhere; R-G03 is the cached-claim landing on the entry that catalogues
  cached claims; R-G06 is the *unit of measure* being unstated so that the same instrument reads six
  different true numbers. Independently corroborated: R-E21 (T2-4, same day) recorded the sentinel
  "invariant at 45" — the `*.html` universe — while SCI-1 was quoting 51. Both were right about
  different universes; only one said which.

### R-CL01 · Closure invariant corrected (CLOSE-1, 2026-07-30)
- **loop-mark `ll-g:loop-mark v1` = 50 (BUILD only)** · **written-line `What I said, and what it changed` = 68 (GROW/LAUNCH)**; mutually exclusive by pathway, 0 carry both. Derive: `git grep -l '<marker>' -- '*.html' | wc -l`.
- The 20 `Science_Teesside/{Grow,Launch}/` decks were re-closed BUILD-ring → written-line; the 5 `Science_Teesside/Build/` keep the ring (they are BUILD). Supersedes the pre-CLOSE-1 leak (loop-mark 70).
- **Art divergence:** 18 `{Grow,Launch}/Slideshows/*_ART_*` + `Launch/Art_L*_v5` close via the **Arts Award evidence-capture flow** (authorship/witness/next-step) — DELIBERATE-DIVERGENCE (REGISTER P3), **not** a gap. Full record: `_passclose1/INVARIANT_CORRECTED.md`.
- **Assessed pair** `GROW_HUM_W7`/`LAUNCH_HUM_W7`: neither marker, by supervised-assessment design; open question deferred to September day-close; proposed (unapplied) diff at `_passclose1/assessed_pair_proposed.diff`; R-A01 untouched.
- **Standing debt:** B3 LAUNCH warrant step-up owed — moves the written-line wording, not its count.

### R-I01 · Pass LA — LAUNCH ASDAN suite built (Autumn 1) + GROW/LAUNCH overviews (2026-07-30)
- **Branch** `pass-la-launch-asdan` off BASE `6945c22` (origin/main HEAD at open). Parks **UNMERGED**; merge position **behind the 29 Aug order: SL → SBX → this**. No PR.
- **New ASDAN lesson totals:** BUILD_ASDAN **31** + GROW_ASDAN **18** + **LAUNCH_ASDAN 30** = **79**. The pre-pass "49 ASDAN lessons" figure is now stale — **state 79; never restore 49**.
- **Deliberate count change (rings, `-- '*.html'` tracked universe):** GROW/LAUNCH **written-line** `What I said, and what it changed` **68 → 98** (+30, exactly the new LAUNCH lessons; LAUNCH is GROW/LAUNCH ring). BUILD **loop-mark** `ll-g:loop-mark v1` **= 50, UNCHANGED** (SET-invariant; new LAUNCH files carry none). Mutually exclusive by pathway, 0 carry both — CLOSE-1 invariant (R-CL01) preserved.
- **Suite shape (Matt-approved at Phase-1 STOP):** 5 strands × 6-week Autumn-1 modules = 30 lessons — `PEQ` (intro + Communication/ComSk1 complete), `Careers`, `Living_Independently`, `Vocational`, `Community_Enterprise`. Entry points: `LAUNCH_ASDAN_Hub.html` + 5 `START_HERE.html` + `Scheme_of_Work.html`. Overview (Matt's Option A): standalone `Resources_and_Tools.html` for **GROW and LAUNCH** (BUILD-only artefact replicated; GROW's regenerated from its own Scheme, LAUNCH last).
- **Claims census (all VALID, pre-authored):** only **ComSk1** printed as a PEQ unit (84×, PEQ strand only); the L1 Award/Extended Award/**Certificate** framing lives at hub/Scheme level as the *year target* (WellbLe1 is homed in the full-year SoW — Summer — so Certificate is reachable, unlike GROW's Extended-Award cap). Four short-course strands bank ASDAN short course + AQA UAS, no PEQ unit. **Zero** L2 registration, `Delivering a Project`, doubled `ASDAN Studio` label, YouTube, or calorie/restriction language.
- **Chassis:** GROW v5 donor carried faithfully via a content-driven generator (`_passla/build/`: `gen.py` + `gen_entry.py` + `gen_resources.py` + `content_*.py` + `gates.py` + `boot.js`). Regenerable (Pathway-Tracker principle). Every lesson born with witness §4 (assessor) + §5 (learner, print-area only), 15 `.print-section`, SVG illuminator, Cold Call, Lundy, XP/confetti.
- **Gates green** every commit (one per strand + entry + overviews): `node --check` per script block, jsdom boot, tag balance, `.print-section`=15, witness §4/§5, sentinel SET-invariance, zero-count asserts, claims census, FKGL ~7.5–8.5. Tip `daf28a6` live-verified via `raw.githubusercontent.com`.
- **UNVERIFIED-AGAINST-SPEC:** the three official ASDAN PDFs were **absent** from `_passpq/inputs/`; every PEQ credit/unit/level fact derives from brief §2.2 + `_passpq/PEQ_PRIMER.md` + the Evidence Binder (Ofqual-URN corroborator). Reconcile at the PQ resume — see HANDOVER.
- **No-touch respected:** science, D&T (incl. Foodwise), Art_Teesside, `GROW_HUM_W7`/`LAUNCH_HUM_W7`, main — none modified. GROW touched only additively (a new sibling `Resources_and_Tools.html`; no existing GROW file edited).

### R-J01 · Pass LA-GO — merged Pass LA to main · published to madebymatt.uk · OneDrive drop-in (2026-07-30)
- **Merge.** `pass-la-launch-asdan` (tip `5ce60e0`, 9 commits off BASE `6945c22`) merged `--no-ff` into main → **`3a74e3a`**. Byte-diff: exactly the 57 LA files, nothing else. Zero conflicts (main was a clean ancestor). All LA gates re-proven at merged tip (30/30 lessons: node --check, jsdom, `.print-section`=15, witness §4/§5). Rollback = `6945c22`.
- **New ASDAN totals: BUILD 31 + GROW 18 + LAUNCH 30 = 79.** State 79; **never restore 49.**
- **Deliberate ring change** (`git grep -l … -- '*.html'`, load-bearing scope per R-E08): GROW/LAUNCH written-line `What I said, and what it changed` **68 → 98** (+30, the new lessons). BUILD loop-mark `ll-g:loop-mark v1` **= 50, UNCHANGED** (SET-invariant; new files carry none). Mutually exclusive by pathway, 0 carry both (R-CL01 preserved). **Reconciliation of the two prior figures:** LA measured 50 at its base, PACK-1 measured 70 at `210c669` — *different moments, not a counting error*: 70 is pre-CLOSE-1 (`*.html` tracked); CLOSE-1 (BASE `6945c22`) re-closed 20 science decks BUILD-ring→written-line, dropping 70→50. Reported by derivation, not "fixed".
- **Publish (both repos).** Lessons `resources.json` **411 → 447** (surgical append of 36 LAUNCH entries: 30 lesson + 6 teacher; mirrors GROW convention — Scheme/Resources left uncatalogued; existing 411 byte-preserved). Lessons hub `index.html` + site `resources/index.html`: `LAUNCH Vocational & PfA` added to PRIORITY/SUBJ_PRIORITY (GROW sibling) + PRINTPACK (justified: 15 print-sections + 3 tiers measured); `SUBJ_LEGACY` untouched. Site `sitemap.xml` **395 → 431** (+36, path-quoted, all crawled 200 at pinned SHA). Reachability gate (jsdom, both pages): chip (36) == returnable 36, Showing reconciles, search reachable.
- **HUD loader.** Already present on all 30 lessons (generator-carried from donor chassis; entry points correctly 0) — matches estate practice (GROW 18/18, START_HERE 0/3). No injection needed.
- **Repo tips at close:** Lessons main **`d283fc0`** (my scope commit rebased onto the concurrent Off-Brand session's `a20de77`, itself a linear descendant of my `f2bb286`); site main **`e074771`**. Live-verify: `madebymatt.uk`/`*.github.io` are **403-blocked by the agent proxy**, so the live hub URL could not be loaded; deployed content verified via `raw.githubusercontent.com` at both pinned SHAs + the jsdom reachability gate.
- **UNVERIFIED-AGAINST-SPEC carried forward** (ASDAN PDFs absent): every PEQ claim provisional; reconcile at the Pass PQ resume (23 Aug). Carried into the OneDrive pack README ("do not promise pupils accreditation yet") and `_passla/HANDOVER.md`.
- **29 Aug append-only-union.** LA overlaps the still-unmerged `pass-sl-sow-launch` / `pass-sbx-art-a2` only on `resources.json` and `REGISTER.md` — both append-only-union: at the sitting keep both sides, never reorder.
- **OneDrive drop-in** (scoped, not the full rebuild — that is 29 Aug): `LAUNCH_ASDAN` added to `build_staff_pack.py` scope + `REBRAND.md` IN-list (tooling commit). 39 pages rebranded via `build_staff_pack.rebrand()` for `ASDAN PEQ/Launch/` + GROW `Resources_and_Tools.html` for `ASDAN PEQ/Grow/`; returned as a zip, **never committed** (branding-leak rule). **Finding:** the 7 entry-doc Matt logos lack `aria-label="Made by Matt"`, so `MARK_SVG` missed them — swapped via a supplementary `PS_MARK` pass in the drop-in; the builder/`gen_entry` should be reconciled before the 29 Aug full rebuild (HANDOVER).
- **`featured`: PROPOSED ONLY, not set** — setting it would displace the current `SUITE` ("Art · Teesside Studio Suite") from the featured slot; left to Matt.


### R-K01 · PACK-LA — three staff-pack zips built from main & handed back as downloads (2026-07-30)
- **Built-from pin.** main `91778c3` (origin == local, tree clean). Every artefact stamped to it. Follows Pass LA-GO (R-J01); this pass commits **no** lesson content and merges nothing — it reads main, builds, validates, returns zips as downloads.
- **Three zips (downloads only, never committed — branding-leak rule):** `Progress_Schools_Term_1_1.zip` (259 real files, 0 dir entries, 4,602,404 B) · `Progress_Schools_Network_Library.zip` (260 real files incl. generated offline `index.html`, 0 dir entries, 4,613,306 B) · `MadeByMatt_Term_1_1_Offline.zip` (259 real files, 0 dir entries, 4,606,856 B; unbranded, hud stripped).
- **Manifest** mechanically derived from `build_staff_pack.in_scope()` + REBRAND scope: **259 files**, arithmetic closes (Σ areas = 259 = len(in_scope)); link-closure crawl = 0 missing (nothing to add).
- **Rebrand via committed `rebrand()`:** 152 visible logos → typographic PS mark; 165 wordmark-text; 34 domain/contact; 175 hud loaders stripped; x-brand 258/258 (Network 259/259). 0 attribute residue, 0 domain residue in both Progress zips (derived at extract). Honest coverage: only the 152 pages that carried a visible logo gained a visible PS mark.
- **R-J01 refinement (amendment A).** Committed `MARK_SVG` keys on `aria-label="Made by Matt"` and misses the aria-less "M"-mark. R-J01 recorded **7** LAUNCH entry docs; measuring by SVG geometry (`M28 71 L28 37 …`) over the whole pack scope finds **12** in-scope aria-less logos — **7 LAUNCH + 5 GROW** (GROW hub, `Scheme_and_Resources`, 3 START_HEREs); root `index.html` also carries it but is out of pack scope. All 12 swapped via a supplementary in-session PS_MARK pass; gate = **0 "M"-mark SVGs in either Progress zip, checked by content not attribute** → PASS. Committed `rebrand()`/`gen_entry` still **unreconciled** — hard precondition of the 29 Aug full rebuild (see HANDOVER).
- **Sentinel at the pin.** `ll-g:loop-mark v1` (`*.html`) = **50**; raw and R-E08 forms coincide (`5_staff_training/` contributes 0); bare unscoped = 60 (10 non-html docs quote it). Matches R-J01's 50; 70→50 vs `210c669` is entirely Science_Teesside 25→5 (the CLOSE-1 science re-close). Reported by derivation, not fixed.
- **Validation (all three zips, from the extracted archives):** `unzip -t` clean ×3 · 0 files without `</html>` · 0 empty · 515 inline-JS blocks `node --check` (temp files) = 0 syntax errors · 0 broken internal links · assessed conditions blocks (`GROW_HUM_W7`, `LAUNCH_HUM_W7`) byte-identical (R-A01) · 0 iframes / 0 video embeds in scope · offline index resolves 258/258 hrefs from inside the zip (urllib-quoted) · MBM copy: 0 x-brand, keeps Made by Matt (198 files), hud stripped. Gate: ALL PASS.
- **Deliverables** returned as downloads with `README_FIRST.txt`, `CHANGES_SINCE.md`, `MANIFEST_derived.txt`, `VALIDATION_table.txt`. Layout caveat carried into README (repo structure ≠ reorganised drive; use the scoped LAUNCH drop-in to update the live drive surgically).
- **Stamp:** term-start pack — rebuilds after merge day (29 Aug); `pass-sl-sow-launch`, `pass-sbx-art-a2`, `pass-art-a2b`, `pass-u-audit` all measured **unmerged** (not ancestors of `91778c3`).


### R-K02 · PACK-LN — LAUNCH network pack + LAUNCH Autumn year-plan workbook (2026-07-30)
- **Built-from pin.** main `f8c4bd6` (origin == local, tree clean). Follows PACK-LA (R-K01); reads main, builds, validates, returns downloads. Two permitted commits: this records line + the workbook into `Planning/LAUNCH/` (gated).
- **Job A — LAUNCH network pack** (`Progress_Schools_LAUNCH_Network_2026-07-30.zip`, download only, never committed): 42 real files / 0 dir entries / 798,674 B. Scope = all `LAUNCH_ASDAN/*.html` (38) + `GROW_ASDAN/Resources_and_Tools.html` (39 rebranded) + generated offline `index.html` + `PLACE_THIS_README.txt` + the workbook. Index-navigated (layout-independent). Rebrand via committed `rebrand()` + the R-J01 supplementary M-mark pass (7 LAUNCH entry docs). Validation: x-brand 40/40, 0 attr/domain residue, 0 Matt "M"-mark SVGs (by content), 0 hud, 90 inline-JS blocks node-checked / 0 errors, 0 broken links, offline index resolves 40/40, unzip -t clean.
- **Job B — `LAUNCH_Autumn_Year_Plan_ASDAN.xlsx`** committed to `Planning/LAUNCH/` (gated on a proven 0-names / 0-initials scan; workbook name-free by construction, every cell derived from the deployed LAUNCH SoW / lessons / term calendar / qualification codes; only personal name is the required teacher line "M Roper"). Mirrors the BUILD template's four sheets (Autumn Overview · PEQ Evidence Map · Key Dates & Compliance · Slot Plan Aut1).
- **Matt's decisions at the gate (recorded):** LAUNCH content is Autumn-1-only at the pin (SoW titled "Aut 1"; strands W1–W6; HUM/Arts W1–W8; Science W3–W7; Aut 2 + Spring/Summer not yet built) → **Aut-1-focused overview**; **W7–W8 mirror BUILD's consolidation/audit pattern, labelled as not-in-SoW**; **PSHE/RSE column omitted** (no LAUNCH strand); **Arts follows the deployed main SoW** (Unit 1 W1–4, Unit 2 W5–8, all Aut 1), noted as differing from §3.1's unmerged Pass-SL provenance.
- **ComSk1 provisionality:** the deployed lessons carry only the unit code `ComSk1` (no sub-criterion codes); the Evidence-Map spine is derived from the lesson sequence and flagged provisional pending the ASDAN spec. Minimums present in the lessons: 3-min talk OR 250-word text; a minimum team size is **not** in the built lessons (not invented). Ceiling stated honestly as L1 Certificate (full-year), this term banks ComSk1 only. Cohort registration unconfirmed (Cheryl) → "do not promise pupils accreditation."
- **R-J01 still unreconciled in the committed builder.** `MARK_SVG`/`gen_entry` keys on `aria-label`; the 7 LAUNCH (+5 GROW) aria-less entry-doc logos were caught only by the in-session supplementary pass. Hard precondition of the 29 Aug full rebuild (HANDOVER).


### R-K03 · Pass PQ-reconcile — spec v1.2 Oct 2025 in hand; blind-audit flags reconciled + held fixes executed (2026-07-30)
- **STATUS** RECORD · branch `claude/asdan-pq-spec-reconcile-sj4gqf` (base = `origin/main` tip **`3fc910d`**; rollback = `3fc910d`); **NOT MERGED — held for Matt** per the estate's standing "Matt merges" doctrine, though every merge condition is met (all gates green, no spec/Binder discrepancy). No-ff merge command ready.
- **Repo-gate (6th recorded instance, R-D05 family).** Session opened in the **site repo** again; caught by the pre-gate (`_passpq/` + `b137a90` absent), Lessons attached and all work done here.
- **Spec obtained & version-gated:** ASDAN PEQ specification **v1.2 October 2025** (title page p1 + review history p2). The three © ASDAN source files are **NOT committed** (copyright hard-rule); `_passpq/inputs/README.md` superseded to retract the old "commit the PDFs" step; `.gitignore` hardened.
- **Two-source agreement = TOTAL.** The Evidence Binder (`U(...)` model, 24 units) matches the spec §6 on every code / Ofqual URN / credit / GLH — zero disagreements, so no code became a STOP finding. `_passpq/RECONCILIATION.md` (VERIFIED 24 · CORRECTED 3 · STILL-UNDETERMINED 5).
- **New committed deliverables** (`_passpq/`): `SPEC_FACTS.md` (source of truth, every line cites spec §/p), `DATES_2026-27.md`, `RECONCILIATION.md`, `COMPLIANCE_CHECKLIST.md`; `PEQ_PRIMER.md` / `CREDIT_PATHWAYS.md` / `QUESTIONS_FOR_CHERYL.md` / `FINDINGS.md` upgraded to spec-verified; `inputs/README.md` superseded.
- **The one substantive spec correction:** the **"plan used over ≥10 hours" window is NOT on Communication** (ComSkE3/ComSk1) — it is on the other five skills only. The blind audit's "appears per-unit" generalisation is corrected.
- **Held fixes executed on the branch — 14 lesson files, byte-diff confined, all gates green:**
  - **T2-2** "Delivering a Project" (nonexistent CoPE-era unit) → **"cross-unit project work"** across **10 GROW files** (86 occurrences: 76 literal-quote + 10 `&#x27;`-entity). Removes the fake unit; honest cross-unit framing. It was already on LAUNCH's `gates.py` BANNED list — GROW was the last carrier.
  - **T2-3** two literal CoPE-era friendly unit *names* → codes: `'Working with Others'` → **Team working (TmWkSk1)**; `'Problem Solving'` → **Thinking skills (ThSk1)**; `links PEQ Working with Others` → `links PEQ Team working (TmWkSk1)`. Anchored so lesson **titles** ("Working With Others", "Solving Problems") are untouched. The **descriptive-phrase weeks** (W1/W2/W4/W6) left **STILL-UNDETERMINED** — neither source maps them, audit mapping is W2/W4-ambiguous; **not guessed** (OPEN_ITEMS 8).
  - **ComSk1 min-evidence (LAUNCH):** measured sweep of all 7 ComSk1 lessons — ≥3-min/≥250-word present W4+W5; **group-≥3 present W5, ABSENT W4** → **added** additively to W4's ComSk1-minimum line (matches W5). (The R-K02 note "team size not in the built lessons" is superseded: it is in W5; W4 was the gap, now closed.)
- **Held, NOT applied (pupil-facing, out of declared additive scope):** the **LAUNCH ComSk1 "~10-hour window" over-claim** (W4/W5) — spec imposes no 10-hour requirement on Communication; reframe awaits Matt (OPEN_ITEMS 9).
- **Superseded stale note:** the audit's **T2-4 "no learner signature"** is **CLOSED** — the "5 · Learner confirmation" block is present in **all 79** ASDAN witness surfaces (merged 2026-07-29, R-E20/R-E21); RECONCILIATION/COMPLIANCE/PRIMER corrected to say so.
- **Gates (asserted):** byte-diff **confinement proof** (strip-tokens residue identical pre/post) on all 14 files · `node --check` every touched inline script · **jsdom boot** per file · tag balance · **verified-codes-only** (only TmWkSk1/ThSk1 introduced, both spec-confirmed) · **reduced-motion** byte-identical · **sentinel** `ll-g:loop-mark v1` **= 50, SET-invariant** (derived, not assumed; no loop-mark file touched) · estate `_passla/build/gates.py` **full check PASS** on the touched LAUNCH W4 (print-section 15, 10 slides, witness §4/§5, banned strings clean, `_ccQuestions`). No pupil names introduced (confinement proves only the four declared strings added).
- **Diff confinement (estate-level):** `git status` shows changes only under `_passpq/`, `GROW_ASDAN/`, `LAUNCH_ASDAN/`, `_close/OPEN_ITEMS.md`, `REGISTER.md`, `.gitignore` — nothing else. No-touch honoured: BUILD, science, D&T/Foodwise, Art_Teesside, `GROW_HUM_W7`/`LAUNCH_HUM_W7`, main.
- **Optional deliverable (downloads only, NEVER committed):** two pre-filled **DRAFT** assessment plans (LAUNCH ComSk1 Autumn-1; GROW L1 set) built from the blank ASDAN template shape + real lesson activities, for Cheryl's meeting.


### R-K04 · Pass PQ-reconcile Phase 2 — LAUNCH ComSk1 "ten-hour window" over-claim corrected (2026-07-30)
- **STATUS** RECORD · base = merged tip `c7f4ab7` (R-K03); separate commit, **independently revertable**.
- **Why.** The spec places **no ten-hour plan-use window on Communication** (it sits on the other five skills — `SPEC_FACTS §15/§16`, RECONCILIATION D1). LAUNCH W4/W5 asserted one as a ComSk1 requirement — an inaccurate accreditation claim on a public site. Held at R-K03; **Matt authorised the reframe**, constrained to claim-accuracy.
- **Applied (claim-accuracy only, 2 files):** W4 — 3 surfaces (the "10-hour window" step header+para; the "the unit asks for … about ten hours" Q&A answer; the "used over about ten hours" recap `<li>`); W5 — the "used over ~10 hours" comprehension question (on-screen + print, 2 occurrences). Replaced with "planned/used across weeks, often **within another challenge**" — spec-accurate per §17 LO1.4/1.5 guidance.
- **Task design UNCHANGED (the constraint).** The assessed activity is untouched: pupils still plan and deliver a **≥3-min talk OR ≥250-word text, group ≥3**. No timing, no deliverable, nothing a pupil does was altered — only the false requirement claim was removed. Nothing stopped-on.
- **Gates:** byte-diff confinement (strip-tokens residue identical) · `node --check` · jsdom boot · tag balance · estate `gates.py` **PASS** (W4+W5) · reduced-motion byte-identical · sentinel `ll-g:loop-mark`=**50** SET-invariant · **estate-wide residual 10-hour ComSk1 claims = 0** (swept all ComSk1 lessons; only W4/W5 ever carried it; GROW W6 = 0).

## R-SEMH01 — a brief's merge grant is subordinate to the repo's own register

**Ruled by Matt, 2026-08-04. Derived at `6aaffb7a07b23833719dd633ed184631c80bc432`.**

A pass brief arrived granting the session authority to squash-merge its own phases.
`HANDOVER.md` says *"Nothing commits without asking Matt for a key. Every time, every
pass, including one-file changes,"* and the in-flight-branch note requires an **explicit
merge commit — no rebase, no squash** — because the ledgers are SHA-anchored and a rebase
orphans every recorded reference. The session followed the register and merged nothing.

**Standing rule: a brief's merge grant is subordinate to the repo's own register.**
Where an incoming instruction conflicts with `REGISTER.md`, `HANDOVER.md` or
`_close/OPEN_ITEMS.md`, the repository's own record wins and the conflict is reported
rather than resolved in the brief's favour. Merges are Matt's, no-ff, never squash.

## R-SEMH02 — legacy-science freeze: a narrow accuracy exception

**Ruled by Matt, 2026-08-04.**

The 2025-26 freeze on `biology/`, `chemistry/`, `2 Physics 10/` and `5 Intervention 10/`
stops **redesign**. It does not require leaving a false, alarm-framed claim in front of
SEMH pupils. One line in `chemistry/Lesson2_pH_Scale_v4.html` asserted that stomach acid
is *"strong enough to dissolve metal"* and that a 0.5 shift in blood pH means *"you die"*.
Both are inaccurate as stated and both use fear as the memory hook.

**Exception granted for exactly one line, in its own commit, with accurate and
proportionate replacement wording.** Everything else in legacy science remains frozen and
travels as proposed diffs only. The exception is the correction of a false claim, not a
licence to edit frozen material.


## R-SEMH03 — the sentinel populations were stale in prose; derive them

**Ruled by Matt, 2026-08-04. Derived at `6aaffb7a07b23833719dd633ed184631c80bc432`.**

Both sentinel populations had grown past the numbers describing them. `HANDOVER.md`
carried **45** strip-carrying BUILD files and **48** written-line GROW/LAUNCH files.
Re-derived at this SHA:

| sentinel | derivation | recorded | derived |
|---|---|---|---|
| LL-G loop-mark (BUILD) | `git grep -l 'll-g:loop-mark v1' -- '*.html'` | 45 | **50** |
| written closure line (GROW/LAUNCH) | `git grep -l 'What I said, and what it changed' -- '*.html'` | 48 | **98** |

The architecture is intact and correctly distributed — every loop-mark file is BUILD and
every closure-line file is GROW/LAUNCH, 0 leakage either way. Only the prose was stale.
`bundle_facts.py` (LL-INST-12) already emits both figures correctly in both R-E08 forms,
so the instrument was right and the sentences were not.

**The live claims in `HANDOVER.md` now carry the command that derives them plus a
derived-at stamp, not a number.** Historical entries recording *"both sentinels unmoved
(45 / 48)"* at earlier commits are left untouched: they were true when written, and
rewriting a dated observation destroys the evidence that the drift happened.

Fifth sighting of the class recorded at R-G03: *a number a script prints when it runs
cannot be stale; a number in prose can.*

## R-SEMH04 — a shallow clone cannot enumerate branches; that zero is structural

**Pass SEMH-1, 2026-08-04.**

`git clone --depth 1` implies `--single-branch`. The resulting refspec is
`+refs/heads/main:refs/remotes/origin/main`, so `git fetch --all` **can only ever return
`main`** — a branch enumeration over a shallow clone is a **false zero by construction**,
not a repository state. This pass first read **0 parked branches** and would have built
its overlap matrix on that.

**Enumerate from `git ls-remote --heads origin`, or repair the refspec first**
(`git config --unset-all remote.origin.fetch` then
`git config --add remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'` and re-fetch).
After repair: **54 branches**, confirmed by two independent signals.

Sibling of the `ko_staleness` shallow-clone false zero that produced LL-INST-11. Same
class, different instrument: **a dependency the caller never declared stays invisible.**

## R-SEMH05 — the canonical path map; a brief's path map is a claim like any other

**Pass SEMH-1, 2026-08-04.**

| canonical location | what it holds |
|---|---|
| `/REGISTER.md` | estate conventions, deliberate absences, deletion records, this register |
| `/HANDOVER.md` | where we got to, open rulings, the queue with decisions attached |
| `/LundyLoop/tools/INSTRUMENTS.md` | the instruments, what each cannot detect, standing rules |
| `/_close/OPEN_ITEMS.md` | open items with status, blocker and source |

The SEMH-1 brief placed **all four** somewhere else — `LundyLoop/REGISTER.md`,
`LundyLoop/HANDOVER.md`, `LundyLoop/INSTRUMENTS.md`, and `OPEN_ITEMS` unlocated. Its
identity gate therefore failed on its own first clause in the correct repository.

**A brief's path map is a claim like any other and gets verified like one.** Four wrong
in a single brief, caught only because the gate had a substance clause — four independent
identifiers resolved (`b137a90`, `_passpq/`, `Art_Teesside/HANDOVER.md`, the three
`Slideshows/` directories), so identity was proven despite the map. A gate whose clauses
are all paths would have stopped the pass dead in the right repo.

## R-SEMH06 — UAS-as-qualification: RETIRED as FALSE, do not re-raise

**Pass SEMH-1, 2026-08-04. Adjudicated by Matt on the close report §1.1.**

The 2026-08-04 SEMH audit claimed estate surfaces describe AQA UAS as a qualification or
show a UAS level (backlog P0-04; scorecard "Humanities LAUNCH", "LAUNCH ASDAN"). **FALSE
at `6aaffb7`.** 40 surfaces match `UAS` near `qualification|level|grade`; every one was
read. None does so. They are of three benign kinds:

1. Scheme-of-Work banners naming a unit *theme* (`AQA UAS 'History around us'`);
2. ASDAN **PEQ** level statements that mention the *UAS coordinator* as the registering
   person — the level belongs to PEQ, a genuinely levelled qualification, not to UAS;
3. Pearson grade ranges (8939 E1–E3, 1BI0 F 1–5) printed *beside* a separate
   "AQA UAS science units" line.

`Humanities_Teesside/LAUNCH_Printable_Pack.html` already carries the corrective wording.
**No edit is warranted and none was made.** Full evidence at
`quality/QUALIFICATION_CLAIMS_REGISTRY.json` Q-002.

**RETIRED. No later pass re-raises this.** What remains open is the separate and real
item: 25 files carrying `AQA UAS unit code: TBC (Cheryl)` — `_close/OPEN_ITEMS.md` #8,
and commissioned as SEMH-2.


## R-TK01 — Pass TK-1 closed: four merges landed, one held on the print check

**Matt's close order, 2026-08-04. Base `74e6fee`.**

| PR | branch | merge SHA (= rollback, `git revert -m 1`) | parents |
|---|---|---|---|
| #37 | tk1-governance | `f03dade` | `74e6fee` + `d4e6607` |
| #38 | tk1-safety | `ce67121` | `f03dade` + `4055c26` |
| #39 | tk1-claims | `4aab666` | `ce67121` + `7fdab61` |
| #40 | tk1-data | `82c40ba` | `4aab666` + `d5fa5de` |

Zero conflicts anywhere — the pairwise-disjointness gate held. Diff-union 24 files, exact. Sentinel
populations derived at the final tip via the R-E08 pathspecs: unchanged (50 / 98 — an observation at
`82c40ba`, not a constant; derive with `bundle_facts.py`). Assessed pair byte-identical. Loop Walk
Logger zero-egress re-derived post-merge. Branding net-unchanged (584 = 584).

**#38's safety merge carries Matt's asymmetry ruling on record:** the replaced burns/missing-tool/offcut
wording was factually wrong, the corrected text is strictly safer, and the in-file PENDING-LOCAL-APPROVAL
tags keep the approval state honest — withholding a correct safety instruction pending sign-off would have
left the wrong one live. The sign-off ledger is `quality/toolkits/PENDING_APPROVALS.md`.

**PR #41 (tk1-access, `f2222d9`) stays HELD** on exactly one precondition: Matt's physical print check of
one evidence-pack week in normal and large-print modes (trigger phrase recorded in the close order and the
PR). The residual micro-branch `tk1-residuals` (two claim-accuracy edits) follows this close — see its own
merge record.

**Mis-open tally:** TK-1's open was the **seventh** recorded site-repo default (R-SB01/R-D05 family). The
close ran inside the same session — no eighth instance, the attach-check having already run.

## R-TK02 — a committed derived-facts file outranks a brief's baked facts

**Earned by Pass TK-1; precedent `_passpq/SPEC_FACTS.md`.**

TK-1's brief carried an ASDAN PEQ facts section (§2) written before the specification was in hand. The
repository already held `_passpq/SPEC_FACTS.md` — derived line-by-line from the PEQ spec v1.2 (Oct 2025)
with total two-source agreement (R-K03). The pass cited the committed file over the brief and was right to.

**The rule:** where a brief bakes in facts and the repository holds a committed derivation of the same
facts from a primary source, **the committed derivation wins**, and the brief's version is treated as a
summary that may have aged. A brief is written once; a derived-facts file names its source, its version and
its verification method, and can be re-checked. Sibling of R-SEMH05 (a brief's path map is a claim) and the
R-G01 family: a fact restated in a brief is a cached claim with nothing keeping it true.

## R-TK03 — TK-1's brief carried two stale branch-facts; the existing form covers it

**Recorded per R-H03's clause — "a ruling's factual premises are claims too — verify upward, even when the
order is Matt's" — rather than minting a rival rule.**

TK-1's brief (§1.8) stated `pass-art-a2b @5b1ea74` (actual tip at open: `952d260`) and listed the
LAUNCH-ASDAN build branch `@5ce60e0` as in-flight (it had merged on 2026-07-30, R-J01). Phase 0's
derive-don't-quote discipline caught both before any action depended on them; neither changed an action.
Both are the R-G01 shape arriving inside an order: a branch tip written into a brief is stale the moment
the branch moves, and a merged branch listed as open is a cached claim about repository state. **Enumerate
the matrix at open, every pass** — the brief's version is the hypothesis, the repo's is the fact.

## R-LLS01 — `R-H16` does not exist; the cross-pass rule is `R-H02`

**Pass LL-S1, 2026-08-04. Adjudicated by Matt on the Phase 0 report. Derived at `7cffd92`.**

The LL-S1 brief cited **`R-H16`** twice as the rule governing cross-pass collision. **There is no
R-H16 in this register.** The rule is **`R-H02` — "Cross-pass collision: the estate cannot see a
pass's work in flight"** — whose own remedy-candidate is *a declared in-flight scope*, which is what
`_lundysci/INFLIGHT.md` implemented. The substance the brief relied on was correct; only the
identifier was wrong, and it was wrong in a way nothing could catch except reading it against this file.

**The register line, which is not "the brief was wrong":**

> **A register ID quoted across passes inherits the authority of an entry without ever having been
> one.** The ID travelled through briefing documents across several passes, each inheriting it from
> the last, and no pass read it against the register until one did.

This is the **R-G01 / R-G03 / R-H07 cached-claim family applied to an identifier rather than a
figure** — the exact shape of the retired 0-of-8 claim, which was also carried across passes as
though it were measurement. **A citation is a claim. Resolve it before relying on it.** An ID is
cheaper to check than a number and is checked less often, precisely because it looks like a reference
rather than an assertion.

## R-LLS02 — Pass TK-1's true shape: four merged PRs, not five branches

**Pass LL-S1, 2026-08-04. Corrects a brief, not the record — `R-TK01` was already right.**

The LL-S1 brief stated that TK-1 "merged five branches plus a records commit and a residuals branch".
**R-TK01 records the true shape and is authoritative:** **four** PRs merged — #37 `f03dade`, #38
`ce67121`, #39 `4aab666`, #40 `82c40ba` — plus a records commit, plus the `tk1-residuals`
micro-branch, with **#41 (`tk1-access`) HELD** on Matt's physical print check.

Operationally this changed nothing: the conclusion drawn from it — that the pack's reference commit
`74e6fee` is stale and cannot be a base — is unaffected and stands. Recorded because a count that is
wrong by one in a brief becomes a count that is wrong by one in the next brief that quotes it.

## R-LLS03 — the site-repo mis-open tally reaches eight

**Pass LL-S1, 2026-08-04.**

LL-S1's session opened in the **site** repo `mattroper1977.github.io` — the **eighth** recorded
instance of the R-SB01 / R-D05 default. R-TK01 recorded the seventh. The control worked exactly as
R-SB02 specifies: the order named `MattRoper1977/Lessons` explicitly, the pass's first act was the
remote check, it failed against the named target, and the Lessons repo was attached and cloned before
any measurement was taken.

**Eight instances is no longer a run of slips; it is the environment's steady-state behaviour.** The
control that catches it is not vigilance — it is the order carrying an explicit repo line and the
gate having a **substance clause** (R-SEMH05), so identity is proven from four independent
identifiers rather than from a path map that may itself be wrong.

A second harness claim was caught in the same act: the session designated a branch
(`claude/ll-s1-lundy-science-vcrh80`) **in the decoy repo**, while the order designated
`claude/ll-s1-lundy-science` in Lessons. Reported rather than resolved in the harness's favour, and
ruled by Matt. **R-SB02 covers this and needs no new rule** — a session's checked-out branch is part
of the harness configuration, and the harness configuration is a claim.

## R-LLS04 — the pack's "84 retained files" is a file count, not a distinct-artefact count

**Pass LL-S1, 2026-08-04. Container-bound fact supplied by Matt; corroborated here by derivation.**

`15_MIN_EVIDENCE_STUDIO.html` and `Lundy_Loop_Science_15_Minute_Evidence_Studio_2026-08-04.html` in
the Lundy-Science pack are **byte-identical**, md5 `399411b16efef770b5c9025a08640909`.

**The derivation, attached so this is an observation and not a bare assertion:** only one of the two
files reached this session, so the duplication itself could not be re-derived here and was correctly
reported **NOT-DETERMINED** in Phase 0. Matt supplied the pairing from the container that held both.
What *was* derived here: `md5sum` of the received `15_MIN_EVIDENCE_STUDIO.html` = the stated
`399411b16efef770b5c9025a08640909`, so the received file is the one the md5 describes.

**Consequence, which is the reason for the entry:** a retained-file count that includes both copies
counts one artefact twice. **Ship one.** Nothing from this pack was shipped, so nothing acted on it;
it is recorded so a later pass reconciling "84 retained" against a distinct-artefact list does not
report a mismatch and start an investigation.

**Free provenance gate, worth reusing:** the pack shipped `32_FILE_MANIFEST.csv` carrying a SHA-256
per file. **Every manifest-listed file received in this session matched its recorded hash exactly —
zero mismatches**, re-derived on each arrival rather than counted once (17 of 17 at the last check;
the manifest cannot list itself — the 82 + 2 = 84 reconciliation). *A supplier who ships hashes hands
the receiver a provenance check for nothing; take it every time.*

**Inputs arrived in three waves, and this entry's own count went stale twice.** It first recorded
**15**. Two further pack files — `TA_PROMPT_OBSERVATION_CARD.html` and `TEACHER_DESK_CARD.html` —
arrived *after* the records commit was written; both matched their manifest hash and byte length
exactly. **A count of what you have received is stale the moment the next file arrives**, which is
why the sentence above is now a derivation and a zero rather than a total. Runtime coverage of the
pack's **18** proposed HTML resources moved **9 → 11**. `START_HERE.html` was never received and
remains NOT-DETERMINED; it is not inferred from the ten that were.

**The corroboration that matters more than the count.** `TA_PROMPT_OBSERVATION_CARD.html` sets out a
least-intrusive support route — *wait · reference · general prompt · specific prompt · re-model ·
direct step* — and separately insists that *"scribing is access, not a thinking prompt"* and that what
fades is a content prompt and **never a reasonable adjustment**. That is `quality/DESIGN_prompt_record.md`'s
prompt ladder (`WT · SP/VC · GV · SV · MO · DS`) plus its `SC` caveat — **the single most important
thing to brief**, per that design's own words — reproduced by a third party with no access to it. The
same card records *"what should be tried without next time"*, which is the one field that design
identifies as the only one that fades anything.

**Why this is worth an entry rather than a remark.** This register states at its head that everything
here agreeing and everything here being wrong are indistinguishable from inside the file, and that the
only external check is **re-deriving an entry by a method sharing no premise with the one that
produced it**. This is that check arriving unbidden for an estate design that is approved in principle
and **unbuilt**. It does not authorise building it — the triggers in `HANDOVER.md` queue 16 are
unchanged and untouched by this — but it is evidence the ladder is not idiosyncratic.

**Now a two-route derivation.** The convergence was read independently twice: once in Matt's chat
workspace, which held the card, and once in this repo session, which received it late and reached the
same WT–DS reading from the artefact with no sight of the first analysis. **Two routes, no shared
premise.** That is the standard this register sets for an entry it cannot otherwise check.

## R-LLS05 — over-broad is safe for exclusion **only when it comes back clean**

**Pass LL-S1, 2026-08-04. Earned by the branch-disjointness gate; sibling of R-SEMH04.**

R-A01b establishes that an over-broad selector is safe for **exclusion** and dangerous for inclusion.
This entry states the limit that clause does not carry:

> **Over-broad is safe for exclusion only when it comes back clean. When it comes back dirty it must
> be refined, never reported.** A dirty over-broad result is not a finding — it is an unfinished
> measurement, and reporting it as a collision is a false positive with a gate's authority behind it.

**The case.** LL-S1's gate 8 compared its change set against six held branches using a two-tree diff
(`git diff --name-only HEAD FETCH_HEAD`) over depth-1 fetches. It returned an intersection on
`quality/toolkits/PENDING_APPROVALS.md` **and all three root ledgers, for five of the six branches** —
which, read literally, is a stop-and-report on every one of them.

**All five were false.** The two-tree form cannot distinguish *"the branch changed this file"* from
*"`main` changed it after the branch was cut"*, and `main` had moved substantially since. Re-derived
from `git merge-base` after deepening the history, every branch's **own** change set was **disjoint**:
`semh1-safeguarding` touches exactly one file (`Tutor_Time/WB_W7_Pressure_Points.html`, confirmed
independently against the PR's own file list), `semh1-dt-semantic` eight, `semh1-art-runtime` 31,
`tk1-access` eight, `pass-art-a2b` three — and `pass-art-a2b`'s apparent `HANDOVER.md` hit is
`Art_Teesside/HANDOVER.md`, a **subject-level** file, not the root ledger.

**Why it is the R-SEMH04 family.** There, a shallow clone made a branch enumeration return a
structural false **zero**; here, a shallow two-tree diff made a disjointness test return structural
false **positives**. Same cause — *a comparison whose anchor is missing answers confidently anyway* —
in both directions. **Neither failure announces itself.** The general form: **an unanchored comparison
is not a weaker measurement, it is a different one**, and it will produce a number that looks like the
one you wanted.

## R-LLS06 — append-only means never renumber, and a reverted error is disclosed

**Pass LL-S1, 2026-08-04.**

The estate's append-only-union rule is usually stated for merges: *keep every entry from both sides,
never choose one side*. Two clauses it does not say out loud, both earned in this pass:

- **Never renumber.** An edit to `_close/OPEN_ITEMS.md` in this pass turned item **23** into **23a**
  while intending to append. Nothing was deleted and the row's text was untouched — and it would still
  have been a silent corruption, because every reference to *"OPEN_ITEMS #23"* in `REGISTER.md`,
  `HANDOVER.md` and two PR bodies would have resolved to nothing. **A ledger's numbers are its
  addresses.** Renumbering is deletion of every inbound reference at once, and it does not look like
  deletion in a diff.
- **A reverted error is disclosed, not absorbed.** The renumbering was caught on the diff, reverted,
  verified byte-identical to HEAD, and appended correctly — so it left **no trace in any commit**.
  That is exactly why it had to be written down. **A clean diff is not evidence that nothing
  happened**; it is evidence that nothing survived. A pass that silently fixes its own near-misses
  reports the same clean history as a pass that never had any, and the estate cannot tell them apart —
  which is the same indistinguishability this register names at its head.

## R-LLS07 — enumerate the inputs against the manifest, and name what is absent

**Pass LL-S1, 2026-08-04. Earned by two workspaces receiving two different subsets of one pack.**

> **A provenance gate verifies what you received. It is silent about what you did not.**

**The case.** One pack was delivered to two workspaces and **neither subset contained the other**.
This session received 16 files (9 HTML, later 11); Matt's chat workspace received 22 (12 HTML). This
session alone held `specimens/OBSERVATION_RECORD.html`; the chat workspace alone held
`TEACHER_DESK_CARD.html`, `TA_PROMPT_OBSERVATION_CARD.html` and `START_HERE.html`. The first two
arrived here late and were verified; **`START_HERE.html` never arrived and is NOT-DETERMINED, not
inferred from the ten that did.**

Every arriving file matched its `32_FILE_MANIFEST.csv` SHA-256 — **zero mismatches throughout** — and
that perfect result said **nothing whatever** about the three that were missing. A gate that can only
return "clean" for what it can see will report clean on a half-delivery.

**The rule, cheap and belonging at the top of every pass:** *enumerate the inputs against the
manifest before starting, and name what is absent.* **An input set is a claim about what was
delivered, never about what exists.** The manifest makes the absence derivable for free; not deriving
it is the choice.

**Worked example — the collision that would have read as agreement.** After the late arrivals, this
session's runtime coverage was **11** of 18 proposed HTML resources. Matt's independent figure was
also **11**. *The sets differ*: his excluded `OBSERVATION_RECORD.html` and included `START_HERE.html`;
this session's is the reverse. **Ten shared members, two different elevens.** Recorded prospectively
because R-E03 had to record it retrospectively — *the shared 22 is a collision, not agreement.*

> **A shared number between two derivations is a collision until the sets are compared, never
> agreement.** Two counts that match are two counts; only the members are the finding.
