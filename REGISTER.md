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
- **STATUS** OPEN · **VERIFIED** `3e2b99d`
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

### R-G05 · The "37 of 49 KOs" figure — SOURCED to Pass G, UNVERIFIED at HEAD
- **STATUS** RECORD · sourced, not re-derived
- Originates in **Pass G's ASDAN Knowledge-Organiser rebuild** (`9f657b6`, *"rebuild the Knowledge Organisers
  from safe sources (49 lessons)"*): rewriting the We-Do-2 targets is reported to have left **37 of 49 KOs
  disagreeing with their own slide**. It is a **content-disagreement** claim, **NOT `ko_staleness` output** —
  that instrument is temporal, reads no content and makes no correctness judgement (R-G02).
- **Reclassified** from Pass X's initial *"appears nowhere in the record"* (VERDICT_PROVENANCE.md) to **SOURCED
  (Pass G, ASDAN suite) — UNVERIFIED AT HEAD.** Its status now is unknown; **checking it is a content read that
  belongs to the KO carry-forward pass, not a `ko_staleness` run.** Do not re-derive it in passing (R-H07: a
  number quoted across passes inherits an authority it never earned).

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
