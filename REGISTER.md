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
