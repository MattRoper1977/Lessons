# SX2 — Decisions record

Order SX2 (2026-09-09), written at the time, per the `_eca1`/`_glv3` convention.
Phase S: finish SX1 and get the Spring/Summer Science batch served.

## Merged, with rollback SHAs

| repo | PR | merged | rollback |
|---|---|---|---|
| Lessons | #454 content (51 lessons, 309 pack files, authoring source) | `d4b9b0ca` | `2c33266b` |
| Apps | #74 gate-copy sync, stale apps caller pin corrected | `ca7c3a36` | `630e838a` |
| Lessons | #455 catalogue, 848 → 950 rows | `331b0074` | `d4b9b0ca` |
| Apps | #75 caller-digest parity | `3bd55dbf` | `ca7c3a36` |

Lessons #453 was closed unmerged and superseded by #454 + #455. The GLV3 fence
never needed repair: `glv3-verify.yml` is `verify_change_boundary.py`'s only
caller and does not trigger on `Science_Teesside/**`. #453 carried content *and*
`resources.json`, which summoned the fence and then handed it protected content
to judge. Split, #454 ran 9 checks instead of 13 and the fence never fired.

---

## D1 — The publisher reads the admission registry from the BUILDER CHECKOUT, not Site main

**This is the entry to read before touching publication.** It is not obvious from
either repository and it cost a full diagnosis cycle to establish.

`MattRoper1977/Lessons .github/workflows/education-pages.yml` calls the Site's
reusable `education-publication.yml` with a `builder_ref`. The publisher checks
the Site out at that ref into `.sources/Site` and reads
`domain-split/education-publication-admission.json` **from there**. Site `main`
is never consulted by a Lessons publication.

Consequences, each measured:

- A registry fix landed on Site `main` does nothing for the Lessons publish. The
  pin must move, or nothing changes.
- The registry is **builder-specific**. Between the pinned builder `92abc460`
  and Site main, twelve files differ, `usage_discovery.py` among them, so the
  two builders emit different `education-site` bytes. A census taken against one
  is wrong for the other.
- It is also **source-specific**. `education-publication.yml` checks Lessons out
  at `${{ github.repository == 'MattRoper1977/Lessons' && github.sha || '6ae34c37…' }}`.
  Only the Lessons trigger builds live Lessons; a Site trigger builds the pinned
  commit. A flat exact-digest census of Lessons main is therefore correct on the
  Lessons trigger and **wrong on main**, where the same paths read as MISSING.
  That is what `ARRIVING` markers and transition pairs in the registry are for.
- `verify()` raises on the first failing tree, so CI shows only that tree's
  problems. Reproduce the publisher locally to see the whole census at once.

### The surgical pin, and why it is not on main

Site `94ae15f8` is the reviewed builder `92abc460` plus two review records only:

```
git diff --name-only 92abc460 94ae15f8
domain-split/check_education_separation.py
domain-split/education-publication-admission.json
```

Pinning instead to a Site main commit would carry the twelve-file builder delta,
including 342 lines of `play/play.js`, and so would **move Play** — forbidden by
SX2 §0.1. Merging `94ae15f8` into main would replace main's registry with one
built by an older builder against a different Lessons pin, breaking the
site-triggered publish. So it is deliberately not on main, and Site #339 is
closed rather than merged.

### Durability — a deleted branch would kill publish silently

Nothing in the Lessons repository would look wrong; publication would simply
fail at checkout. Anchors, in order of strength:

1. `refs/pull/339/head` → `94ae15f8`. GitHub maintains this permanently once a
   PR has been opened and users cannot delete it. **Verified present.**
2. Branch `claude/sx1-science-admission-pin` → `94ae15f8`.

An annotated tag `education-publisher-pin-sx1` was created locally and is the
intended third anchor, but **this session cannot push it**: GitHub answers
`HTTP 403` to `git-receive-pack` for a tag ref while branch pushes to the same
repository succeed, so the credential permits `refs/heads/*` and not
`refs/tags/*`. The agent proxy recorded no failure for github.com, so this is
GitHub's refusal, not egress policy. Reported rather than routed around. To
create it by hand:

```sh
git tag -a education-publisher-pin-sx1 94ae15f8d98ab9fe9d814aeb9bf417942452b83e \
  -m "Education publisher pin, SX1/SX2. DO NOT MOVE OR DELETE."
git push origin refs/tags/education-publisher-pin-sx1
```

Before retiring any of these anchors, repoint `education-pages.yml` (both the
`uses:` ref and `builder_ref`) at a successor commit and re-pin
`PUBLICATION_CALLER_SHA256` in **both** copies of
`tools/verify_cross_estate_unification.py`.

---

## D2 — The apps caller pin was a mid-PR state, never on main

`PUBLICATION_CALLER_SHA256_BY_KIND["apps"]` held `c420519111f6`: the Apps caller
at `924ab986`, an intermediate state **inside Apps #72**, superseded 36 minutes
later in that same PR when CX3 cycle C advanced the caller from Site `23a4f360`
to `6430f23f`. Apps main has carried `732591ddeae0` since #72 merged; the pinned
value was never on main.

UX2 A5 justified it as "the Site's catalogue contract control runs this gate
against as kind apps". **No such control exists**: the Site invokes this verifier
in zero workflows, and `detect_kind()` derives the kind from the root it is
standing in, so the only readers are the Apps repository's own gate runs against
their own tree. Corrected in #74/#455.

It stayed invisible because the Apps gate copy predated UX2 A5 and had no
by-kind map to read. **Syncing the two copies is what made it fire** — a general
lesson: a constant that no consumer evaluates is not verified, however exact it
looks. Session `011cypYwzsjkJRHnYRjJzpZF` reached the same conclusion
independently within the hour, from the same evidence (Lessons #456).

---

## D3 — Re-freezing the retained usage-registry baseline

`check_education_separation.py` freezes the digest of the rows
`registry_partition()` retains. The 51 new lesson records move it: **926 → 977
rows, 51 added, 0 removed, 0 field of any existing record changed.**

The method matters more than the number. A build at this repository's previously
pinned source `2c33266b` reproduces the *previous* baseline `d2439c61` **exactly
at 926 rows**. Without that equality the before/after comparison would prove
nothing, so re-freeze this way rather than by taking the new digest on trust.

---

## D4 — Part R builds the target pin-mover (Order SX3 amendment A1)

`tools/easter/SCIENCE_ORIGINAL_TARGETS.json` pins 25 lessons by
`expectedPatchedSha256`, asserted as `Source identity: <file>` by the long
`Original Science navigation` job. **All 25 are files the Autumn 1 refresh
patches**, so any R landing reds that job unless the hashes move with it. No tool
rewrites them today; the file is hand-maintained, and it is *not* in
`CATALOGUE_PINS`, so no catalogue re-pin is involved.

Ruled (SX3 A1): the mover is built **once, in Part R, inside the fence**. It
recomputes `expectedPatchedSha256` from the patched bytes, rewrites the JSON in
the same commit, **fails if any target path is missing**, and is red-proved by
planting one stale hash. SX3 reuses it for its 64 REPLACE/PATCH files.

---

## D5 — Deferred: the zero-check gate should exclude conflicted PRs

**No code now. Own PR, later, never inside an order.**

`tools/pr_check_census.mjs` reds when any non-draft open PR across the three
repositories has zero check runs and is not declared in
`tools/zero_check_baseline.json`. The intent is sound: a green tick on a PR
nothing ran is a false green.

But a PR whose `mergeable_state` is `dirty` **cannot be merged at all**, so it
carries no false-green risk — GitHub can build no merge ref, so no workflow can
fire however the filters are written. The gate's own output says exactly this:
`conflicted — no merge ref, so no workflow could fire`. The result is that one
conflicted PR anywhere in the estate reds **every** PR in the estate, including
unrelated ones in other repositories.

Observed 2026-09-09: three conflicted PRs (Lessons #456, Apps #73, Site #339)
red-flagged Lessons #457, which had 13 green checks and no relationship to any
of them.

Proposed rule: exclude `mergeable_state == 'dirty'` from the undeclared count and
report it as a separate conflicted census, keeping it visible without letting it
gate. `draft` is already excluded on the same reasoning — draftness is read, not
inferred — and conflictedness is the stronger signal of the two.

Do **not** work around this by adding transient conflicts to
`zero_check_baseline.json`. That file's own `_how_it_fails` calls an unpruned
entry stale evidence, and a conflict that clears on rebase would leave a row
nobody prunes.

---

## LF1 — A relabeller that cannot resolve a label must refuse, not guess

**Status: the tool change is here. The 121 restorations are proposed, not landed.**

### What went wrong

`tools/relabel_public.py` replaces pupil-facing calendar labels ("Week 9",
"W14") with sequence-relative ones ("Lesson 3 of 12"). It resolves a week
number against the unit manifest in the file's own folder. When the week was
not in that manifest it returned one of two strings:

```python
if s.lo is not None and w < s.lo: return 'the previous unit'
if s.hi is not None and w > s.hi: return 'the next unit'
```

Neither is a translation of a week number. Both are a guess, and on the CX3
pass of 2026-09-08 the guess was taken **121 times across 22 published pages**.

### Why the guess is always wrong here

The two branches fired on cross-unit references — a recap naming an earlier
week, or a forward reference to the next half-term. Four failure shapes came
out of them:

| shape | occurrences | example |
|---|---|---|
| distinct weeks collapse to one phrase | 105 | `W5:` `W6:` `W7B:` all became `the previous unit:` — three different recap lines, one indistinguishable label |
| ranges double the phrase | 16 | `W2–W3:` → `the previous unit–the previous unit:` |
| an article in front of it duplicates | 11 | `the W14 question` → `the the next unit question` |
| the reference is not to a unit at all | all of them | W5–W7 are earlier lessons in the same strand; calling them "the previous unit" is wrong even where it reads |

(Shapes overlap: the range and article counts are subsets of the first.)

The causal set is exactly two branches — `w < lo` (54 occurrences) and
`w > hi` (51) — plus the never-taken third fallback. Simulating the tool on the
recovered originals reproduces the live bytes for **103 of 103** affected
nodes, so nothing about the mechanism is unexplained. An earlier hypothesis
that flat folders (`sequence()` returning `n=None`) caused it is **wrong**: no
live occurrence came from a flat folder. Every affected file resolved its own
sequence correctly.

### The rule

A tool that cannot resolve a label says which label, in which file, in which
sentence, and changes nothing. `Unresolvable` is raised; the file is not
written; the run exits 2. There is no mode in which this tool authors a label
it did not read.

`added_banned()` is the post-condition (LF1 B6): a run may never *increase* the
count of `the previous unit` / `the next unit`. It asserts an increase, not
zero, because both are honest prose a teacher may have written — `6
Art/Lesson15` and `Grow/Slideshows/GROW_HUM_W7` each contain one, authored, and
neither is a defect.

Red-proved in both directions on the real estate, not on fixtures: of the 64
HTML files the CX3 pass touched, the fixed tool refuses **exactly** the 22 that
carry the defect and applies cleanly to all 42 that do not. No false positive,
no false negative.

### Recovery is from stored bytes, never re-derivation

The relabeller stores the original text in `data-mbm-cal` on the enclosing
element. That store was checked against an independent source: for all 22
files, `walk(live, 'revert')` is **byte-identical** to the blob at the parent of
the first CX3 commit. Two sources, agreeing on every byte, so the restored
strings are the ones that were there — not inferred from neighbouring weeks,
not hand-authored. The C3 list (unrecoverable, needing a human) is **empty**.

### What this costs

The 22 files cannot be relabelled by tooling any more, and should not be. Their
recaps name specific earlier lessons; turning those into sequence-relative text
needs someone who knows what the pupil is being asked to remember.

### LF1-B — how the count was wrong, and what a pupil-visible claim now costs

**31 → 121.** The first LF1 census reported 31 occurrences across 19 files. The
real figure is 121 across 22. Two independent errors, both in the same direction:

1. `git grep -c` counts matching **lines**, not occurrences. A line carrying
   `the previous unit–the previous unit` counted as one.
2. The search set was incomplete. `the next unit` was never searched for in the
   Science Build tree, so `SCI_B_W13A` (18) and `SCI_B_W13B` (33) — the two worst
   pages in the estate — were absent from the list entirely.

**The standard, from here.** Any claim about pupil-visible text is measured in a
browser, on the DOM, on every route the page has. `tools/lf1/render_census.cjs`
is that measurement. What it changed about the LF1 numbers:

| measured as | count |
|---|---|
| source grep, lines | 31 |
| DOM text nodes, slide 1 only | 8 |
| DOM, driving the slide control | 72 |
| …also pressing the tier and model-step controls | 75 |
| print emulation, union over every printable tier | 35 |
| accessible names (`aria-label`) | 3 |
| **total in the document** | **121** |

Three lessons in that table. A count on slide 1 is not the deck — most slides are
`display:none` until navigated, and `showSlide` is inside a closure, so the walk
has to drive the real `#next` control. Content behind one press of a tier or
reveal button is pupil-facing, not a caveat. And the printed worksheet is a
separate DOM subtree: `SCI_B_W8B` had four occurrences in print and none on
screen at load, so the defect reached handouts before it reached a screen.

**The duplicate that was not one.** A direct fetch of `SCI_B_W13A` appeared to
show placeholder and correct copy in one node. It is the `span.mbm-cal-staff`
twin the six *v4 relabel bytes* commits (`a229cdf`, `aa6aaea`, `d1ae3a2`,
`ba61840`, `edc6b36`, `06b77c8`) add so staff keep the calendar declaration a
pupil no longer sees. It is inline `display:none`, so a browser renders one copy
— but any tag strip that ignores CSS renders both, which is what the fetch did.
26 twins exist; the 8 files with only the first CX3 pass have none.

**But the hiding is not load-bearing.** `html.mbm-guide-on
[data-mbm-guide]{display:revert!important}` beats an inline non-important
`display:none`, so with guide/TA mode on the line renders twice — 9 such pairs on
5 pages. That is a guide-mode bug, not a relabel bug, and it is recorded
separately; the LF1 fix deletes only the 9 twins that restoration makes into
word-for-word restatements, and leaves the 17 doing their job.

**The proxy substitution is resolved.** Matt fetched the origin directly. The
admission-registry membership argument is retired as a served proof for LF1;
served proof is a fetch of the four URLs, read as rendered DOM.

**A URL already fetched in this session is not a fresh read after a deploy.**
Closing LF1, two of the four proof pages first came back still showing the
placeholder. That looked like a partial publication — some paths served, some
not — which would have been a serious finding about the publisher. It was fetch
cache. The pages were correct; the reader was not.

So a re-fetch of a URL the same session has already opened proves nothing about
what is being served now. It has to be a genuinely fresh read: a different
client, a cache-defeating request, or a device that has not seen the page.

What actually closed LF1 was the second instrument agreeing with the first. The
census of the published tree said 0 on every route and the phone said the same,
and the phone had never loaded those URLs. Two readings from independent paths,
not one reading taken twice.

LF1 confirmed live 2026-09-09 19:50 BST: SCI_L_W8L1 and LAUNCH_HUM_W9 clean on
screen and in print; SCI_B_W13A reads "for the W14 rock investigation"; SCI_B_W8B's
Arrival reads W8A / W7 / W4 / W2-W3.

---

## D11 — A changed admitted byte needs a registry move as much as a new path does

`education-publication-admission.json` pins **a digest per path**. The publisher
refuses to emit a tree when a built file's digest is not among those admitted, so
a *changed* digest blocks publication exactly as an *unlisted* path does.

The same gate blocked publication twice on 2026-09-09:

| | what changed | what was checked before merging |
|---|---|---|
| #454 | added served paths | — |
| #468 | changed the bytes of 30 already-admitted paths | "does this add a new served path?" — answered no |

The second question was the wrong one. The right test is **"does this change the
bytes of any path the registry already admits?"** Both times the answer arrived
after the merge, from a red publication, with the change sitting on main and not
being served. The second time that meant a live pupil-facing correction was
merged, announced, and not actually live; a pupil went on reading "the previous
unit" for the length of the recovery.

The move is staged as a **transition pair** `[pre, post]` so a build at either
Lessons state passes and no merge ordering can wedge the publisher, then
`builder_ref` advances to the Site commit carrying it (D1).

`tools/lf1/check_admission_move.py` makes this checkable before the merge. It
asserts the necessary condition — a changed admitted path must carry a pair — and
deliberately does not assert the digests, because the registry pins the digest of
the *published artefact* and the publisher injects navigation into many pages: 19
of 40 sampled paths match their source blob and the rest do not, by design.
Proving a pair holds the right digests needs the reviewed builder and a full
build, which is the publisher's own gate.

## D12 — Build a counterfactual to contradict you, not to pass

LF1-B §2.2 required that no page carry two adjacent nodes with identical text.
Measured on live: **0**. Measured on the fix: **0**. A two-column table would have
recorded that as a pass, and it would have proved nothing — the invariant reads 0
on live only because the pupil line said "the next unit" while its staff twin said
"W14", so they were never identical to begin with.

The third column is what made it an invariant rather than a formality: the
restorations applied with the twin deletions **withheld** — **9** adjacent
identical nodes. That is the measure firing, and it is the only evidence that the
9 deletions are necessary rather than tidy.

It also caught an instrument fault. The first counterfactual returned **6**, not
9. A standalone probe found a pair on `BUILD_HUM_W9` that the census called
absent — 232 characters, byte-equal, adjacent. The census was wrong: these decks
persist the chosen tier, so the guide pass's `page.reload()` came back showing
only the last tier the deck walk had pressed. It was measuring one tier's DOM and
calling it the page. Fixed with a fresh context; 6 → 9.

That fault was found only because the counterfactual supplied a number to
disagree with. A measurement that agrees with your expectation teaches you
nothing; give yourself something that can contradict you and check whether it
does.

## D13 — A browser-rendered census is the standard for a pupil-visible claim

Two false findings in one day, from opposite directions, both from not rendering:

- **Mine.** `git grep -c` counts matching *lines*, not occurrences, and the search
  set omitted `the next unit` in the Science Build tree. Reported 31 across 19
  files. The real figure was **121 across 22** — and the two worst pages in the
  estate, `SCI_B_W13A` (18) and `SCI_B_W13B` (33), were not in the list at all.
- **Matt's.** A direct fetch of `SCI_B_W13A` appeared to show the placeholder and
  the correct copy in one node. It is the `span.mbm-cal-staff` twin, inline
  `display:none`; a browser renders one copy, but any tag strip that ignores CSS
  concatenates both.

Neither a source grep nor a tag-stripped fetch is a render. `tools/lf1/render_census.cjs`
walks the DOM the browser builds. A source scan is still sound for *enumerating
candidates* — nothing can render that is not in the bytes — but it never
adjudicates what a pupil reads.

## D14 — What a render census has to cover

The LF1 numbers, same phrase, same 22 pages, by how it was measured:

| measured as | count |
|---|---|
| source grep, lines | 31 |
| DOM text nodes, slide 1 only | 8 |
| driving the real slide control | 72 |
| …sampling after **each** gate press, not a batch | 83 |
| …pressing both chassis conventions | 86 |
| print emulation, union over every printable tier | 35 |
| accessible names (`aria-label`) | 3 |
| **total in the document** | **121** |
| **rendering on no route at all** | **0** |

Every row of that table is a way of undercounting:

- **A count on slide 1 is not the deck.** Most slides are `display:none` until
  navigated and `showSlide` sits inside a closure, so the walk must drive the real
  `#next` control.
- **Pressing every gate then sampling once shows only the last tier chosen.**
  Supported, Standard and Stretch are three panels; sample after each press.
- **Two chassis, two conventions.** Science gates on data-attributes, Humanities
  on inline `onclick="tier(...)"` with a `.tierbtn` or `aria-expanded` button.
- **Print is a different subtree.** 35 occurrences live in the `.printpack`
  worksheet, and `SCI_B_W8B` had four in print and none on screen at load — the
  defect reached handouts before it reached a screen.
- **Accessible names are pupil-facing text.** Three occurrences were `aria-label`s
  no text-node walker can see and a screen reader reads aloud.
- **"Behind a control" is not "unseen".** Content one press away is pupil-facing.
  Reported as 11 unreachable, then 3, then **0**.

## D15 — One re-run is a discriminating test; a second identical failure is an outage

An install-time failure — one that happens before any test body runs — is
re-run **once**, not as a retry but as the test that tells you which it was: the
runner, or the change. If it passes, the first result was the runner. If it fails
identically, that is an outage, and an outage is **waited out**, never bypassed,
never merged past, never disabled.

Observed 2026-09-09 on #469 (two YAML lines and a digest pin). All four
Chromium-dependent checks failed at browser install, twice, verbatim:

```
E: Failed to fetch https://dl.google.com/linux/chrome-stable/deb/dists/stable/main/binary-amd64/Packages.gz  Hash Sum mismatch
   Last modification reported: Wed, 09 Sep 2026 09:41:12 +0000
   Release file created at:    Wed, 09 Sep 2026 17:16:59 +0000
E: Some index files failed to download. They have been ignored, or old ones used instead.
Failed to install browsers
Error: Installation process exited with code: 100
```

Google's own apt index disagreeing with its own `Release` file — a stale CDN
edge, external to this estate and to GitHub. `browser-matrix` fails one step
later with `browserType.launch: Executable doesn't exist at
…/chromium_headless_shell-1181/…`, which is the same failure seen downstream: the
install never happened, so the binary is not there.

A failure **inside** a test body is never attributed to infrastructure without
evidence. The eleven non-browser checks on that PR all passed, and the diff
touches nothing any of the four exercises — but that is the argument for waiting,
not for merging.

---

## D16 — A crash is not a refusal

A refusal names the problem, leaves the file byte-unchanged, and lets the run
continue. A crash aborts wherever it reached and says nothing about the files
after it. The two must never be reported together, and a crashed run's partial
output is not a measurement.

`tools/relabel_public.py` assumed a manifest was a JSON object. Three Science
`v3_40min` manifests are a top-level array, so `m.get('lessons')` raised
`AttributeError` on the **47 files in those folders — every one of them served**.
It had done so since before #466; #466's 25 self-tests did not cover it, which is
a gap in that PR's testing rather than a regression it introduced.

The consequence is bigger than 47 files. While the tool crashes on a tree, no
census that runs it over that tree can be trusted: the run has an unknown tail.
Any "0 findings" from such a run is a statement about where the crash happened,
not about the estate.

Fixed in #473 by normalising the envelope, not by catching the exception:
`manifest_lessons()` reads the object form, the array form, and returns no
entries for anything else — which makes `lesson_ref` refuse, the same outcome as
no manifest at all. Handled rather than refused for the array because the
evidence said so: its entries carry the same `file`, `week` and `id` fields the
object form does.

**What the crash had been hiding, and what it had not.** The 47 carry **zero**
`data-mbm-cal` attributes and zero `mbm-cal-staff` twins — the relabeller's own
signature on every node it rewrites. It had therefore never written to any of
them: the crash is in `sequence()`, before any rewrite. A rendered census of all
47 as published found **0 placeholders on every route**. The crash prevented
processing; it did not damage what is served.

## D17 — A positive control is part of a clean result, not an optional extra

The census of those 47 returned 0. On its own that is worth nothing: a page that
failed to load returns 0 too. The control was to run the same census, over the
same pages, for a phrase that must be present.

The first control used "Science" and came back **45 of 47** — two pages returned
nothing. That looked like two pages the instrument could not read. It was not:
`LAUNCH_SCIENCE_PRACTICALS_MATRIX.html` and its `_PROGRESS_SCHOOLS` twin are
titled *"LAUNCH GCSE Biology"* and contain the word "Science" nowhere. Their
rendered text is ~12,800 characters; the control phrase was simply absent.

Re-run with a phrase present in all 47: **47 of 47**, 6352 occurrences, 3963 on
the deck and 1632 in print — the same routes the clean census reported 0 on. Only
then is the 0 earned.

Two rules from that. A control phrase has to be verified present before it can
prove absence of anything else. And a control that fails is a question, not a
verdict — it was my control that was wrong, not the instrument, and assuming
either way round without checking would have been an error.

## D18 — What the estate's manifests actually look like

Three envelopes are in use and only two were known:

| envelope | example | entries carry |
|---|---|---|
| object under `sequence` | `Build/W8-W13_2026-27/manifest.json` | `file`, `week`, `id` |
| object under `lessons` | various | `file`, `week`, `id` |
| **top-level array** | `Build/v3_40min/manifest-v3.json` | `file`, `week`, `id` |

`Grow/v3_40min/manifest-v3.json` is the array form but its entries carry **no
`week`**, where its Build and Launch siblings do. That is a data gap in one
manifest, and it is why 10 lesson decks that *are* listed still cannot be
resolved.

Across `Science_Teesside`, 97 files are unclaimed by any manifest, all served.
35 are lesson decks — 25 in folders with no manifest at all, 10 the weekless
`Grow/v3_40min` entries. The other 62 are companion worksheets, pack copies,
indexes, matrices and guides, which no manifest should list. Four served pages
have no inbound link from anywhere in the estate.

## LF1-G §6 — DEFERRED, recorded as the next order

**The guide-mode CSS defect.** `html.mbm-guide-on [data-mbm-guide]{display:revert
!important}` beats an inline non-important `display:none`, so the staff layer's
hiding is not load-bearing. LF1 met it as 9 doubled lines on 5 pages and deleted
only the twins its own fix made redundant; **the 17 twins that remain still double
under guide mode**, less nonsensically but in front of a class.

The order when it comes: census every `display:none` staff/TA span in the Lessons
estate against guide mode, calm view, large text and Teacher Freeze — in the
browser, each mode toggled — and report what becomes visible. If it reveals
pupil-visible nonsense anywhere else it jumps the queue, as LF1 did.

Remember R4 while doing it: the "70 pupil-visible calendar literals" that turned
out to be text inside `display:none` staff spans were not a wrong count. They were
a **conditional** one, and this is the condition.

## D19 — A manifest entry with no week is a data defect, not a labelling decision

Granted by Matt, 2026-09-09, on the amendment argued in
`_sx2/FINDING_relabeller_scope.md` §4b.

The rule Matt started from refuses any reference to a week outside the folder's
own sequence. It was silent on a third case: a file the folder's manifest *does*
list, whose entry carries no `week`. `Grow/v3_40min/manifest-v3.json` is the only
one in the estate — its Build and Launch siblings carry `week`, it does not.

Those are not out-of-folder references. They are in-folder references the
manifest cannot currently answer. **Adding the missing `week` fields would move
them from refuse to resolve without any judgement about what a pupil reads** —
which is the whole test. So it is referred for data repair, and the tool refuses
it under its own reason code (**F3**) rather than lumping it in with F2.

The repair itself is not a licence to derive. §2 of LF1-I applies: a week is
recovered from an authority or it goes on a list for Matt. The same rule that
governed the 121.

### D19 as amended — Ruling 2, LF1-M, 2026-09-09: missing is not inapplicable

> - **ABSENT** week field, where a week exists and should be recorded → manifest
>   defect → **F3** → repair.
> - **INAPPLICABLE** week, where no week will ever be correct (the three
>   `Spr2·W6`) → not a defect; repairing it would mean inventing a week.

A manifest entry may therefore carry an **explicit no-week marker with a stated
reason**, and the tool refuses it under a new code:

> **F6.** Entry carries an explicit no-week marker. The literal label stands. Not
> a defect, not a backlog, no repair.

The reason is the whole marker. `noWeek: true`, `noWeek: ""` and a blank string
are **not** markers and fall back to F3 — "this has no week" without "because …"
is indistinguishable from having forgotten, and the point of the amendment is to
separate exactly those two. Accepted forms: `noWeek` or `weekNotApplicable`,
either a non-empty string or an object carrying `reason`.

The three markers written under this ruling all quote the same authority:
`_sownb/TERM_DATES.md` — *"Spring 2 has five timetabled weeks, so its sixth
column is NOT-TIMETABLED"* — plus the collision the mapping makes explicit
(`Spr2 Wn → 21+n` puts a sixth at 27; `Sum1 Wn → 26+n` already holds it).

**What a pupil reads on those three pages, measured rather than assumed.** All
three already render `BUILD/GROW/LAUNCH · SCIENCE · Lesson 10 of 10` (11 of 11
for GROW). `Spr2·W6` survives only inside `data-mbm-cal`, the reversibility
store, which is never rendered. Browser census over all three, every route:
**`Spr2·W6` renders 0 times** on deck, print, guide and accessible names, against
a positive control ("Lesson 1") rendering 14/15/15 on the deck. So there is no
literal calendar label there to be wrong on its face, and F6 defers nothing.

## D20 — RULE R-CAL-1, when a calendar token may be re-tokenised

Ruled by Matt, 2026-09-09. Landed verbatim below and in the docstring of
`tools/relabel_public.py`, which is its enforcement mechanism.

> **RULE R-CAL-1 · WHEN A CALENDAR TOKEN MAY BE RE-TOKENISED**
> Ruled by Matt, 2026-09-09. Governs relabel_public.py and any successor. The refuse-don't-guess behaviour of #466/#473 is its enforcement mechanism.
>
> **PRINCIPLE**
> A week label is re-tokenised only when the referenced week resolves from an authority the tool can read. Where it cannot, the existing literal label stands. A correct literal label is not a defect; a wrong token is. The tool improves accurate labels — it never replaces an accurate literal with an inaccurate token.
>
> **RESOLVE — re-tokenise**
> R1. The referenced week lies inside the folder's own sequence AND the manifest entry for that week carries both a file and a week value.
> R2. Range references (W2–W3) resolve only when BOTH endpoints satisfy R1. A half-resolved range is a refusal, never a partial rewrite.
> R3. Array-shaped manifests resolve identically to sibling-week manifests where entries carry file, week and id (per #473's evidence). Shape is not a reason to refuse; missing data is.
>
> **REFUSE — leave the literal untouched, exit non-zero, file byte-unchanged**
> F1. Referenced week outside the folder's sequence (below min or above max). Majority case, correct behaviour, not a backlog. A cross-unit reference is authored prose about another unit.
> F2. No manifest claims the file.
> F3. Manifest claims the file but the entry carries no week. (D19: manifest defect, referred for data repair, not resolved by the tool.)
> F4. Manifest shape unrecognised. Refuse cleanly; never crash — a crash tells you nothing about the files after it.
> F5. Reference ambiguous: two entries claim the week, or it matches none.
> **F6. Entry carries an explicit no-week marker. The literal label stands. Not a defect, not a backlog, no repair.** *(added by Ruling 2, LF1-M, 2026-09-09 — see D19 as amended)*
> Every refusal names file, token, reason code, and quotes the sentence.
>
> **NEVER**
> N1. No fallback string, no placeholder, no opt-in variant, no pupil-visible stand-in of any kind.
> N2. No inference from neighbouring weeks, file order, filename or surrounding prose. Recovery from an authority, or refusal.
> N3. No partial write. Wholly rewritten or not at all.
> N4. No proxy proof. A run reports resulting text, not the disappearance of the input.
>
> **REPORTING**
> Every run outputs: resolved count, refused count by reason code, crashed count (must be 0), and a sample of resulting text for at least five resolutions across pathways. A run that resolves 0 and refuses all is a valid, reportable outcome — not a failure to work around.
>
> **CONSEQUENCE ACCEPTED**
> Most Science pages carrying a calendar token will not be re-tokenised by tool. That is the correct outcome. Re-tokenisation improves labels the tool can verify; it is not a coverage target to maximise.

### What adopting it changed in the tool

`--measure` is new: the REPORTING block as a dry run, writing nothing, so the
numbers and the resulting text can both be read before a byte moves. Three
behaviours changed to match the rule, and each of them **narrows** what the tool
will write:

- **F2 is now a file-level fact.** A file its folder's manifest does not list is
  refused whatever week it names. "Lesson 3" on a page that is not in the
  sequence is a claim about a sequence the page is not in. 26 files that the
  tool used to answer for now refuse.
- **F5 exists.** Two manifest lessons claiming one week used to produce
  `Lessons 3–4`; a bare `W9` does not say which, so it refuses.
- **The letter clamp is gone.** `min(k, len(ns) - 1)` turned `W7B` in a
  one-lesson week into lesson A. That was N2 inference from file order wearing a
  resolution's clothes — the same class of guess as `the previous unit`.

Measured over all 290 `Science_Teesside` pages: **resolved 54 → 27 files.**
R-CAL-1 refuses 27 files the implementation before it would have rewritten. The
178 that already refused did not move; they were re-attributed to F1 68 / F2 109
(83 folder has no manifest, 26 manifest does not list the file) / F3 13, plus 15
F5 and 12 F2 arriving from the old rewrite column. Crashed 0.

### Two things only reading the output could find (N4)

1. **`'BUILD Weekly - Spring'!C29` became `'the curriculum workbook`.** The cell
   pattern never consumed the opening quote, and `!B41, C41` left `, C41`
   stranded. Ten rewrites across the estate went through that path. A count of
   rewrites reports ten successes; reading the text reports an orphan quote on a
   pupil-facing page. Fixed, with the estate's real cell strings as fixtures.
2. **The sibling-week pathway fires zero times on the whole estate.** Of 80
   rewrites: 47 own-week, 20 `last week` → `last lesson`, 10 SoW cells, 2 term
   labels, 1 academic year, **0 `Lesson k`**. The code path that authored the
   121 wrong labels is now dead on this content — not by being removed, by
   never resolving.

### UNSEEN — a bucket the rule does not have, and why the report shows it

Four `START_HERE.html` pages carry `Absolute week 14` in visible text. The census
pattern is case-insensitive; the rewriter's week pattern is not. So the gate
counts a pupil-facing token the rewriter cannot see: neither resolved nor
refused. `--measure` reports these as **UNSEEN** rather than folding them into
"no change", because a bucket that says "nothing happened" is where a defect
hides. The same asymmetry hides a bare `W9B`: `\bW\d+\b` needs a word boundary
after the digit, so a lesson-letter reference standing alone is invisible to the
gate as well. **Neither is fixed here** — widening the rewriter's pattern changes
what it will write, and that wants a ruling, not a commit.

## D21 — 75 of the 205 refusals are a numbered question, not a week

Found while proving the three `Spr2·W6` pages under F6, because all three refuse
on `W1.`, not on anything calendrical.

Classifying every one of the 205 refusals by the token that actually blocked the
file — normalised so `W3` and `Week 3` count the same — leaves no residue:

| the blocking token is | files | |
|---|---:|---:|
| a real week reference | 130 | 63.4% |
| **a numbered question** (`W1.` `W2:` `W3)`) | **75** | **36.6%** |

| code | total | numbered question | week reference |
|---|---:|---:|---:|
| **F1** | 68 | **59** | 9 |
| F2 | 109 | 13 | 96 |
| F3 | 10 | 0 | 10 |
| F5 | 15 | 0 | 15 |
| F6 | 3 | 3 | 0 |

**87% of F1 is question numbering.** F1 is the code R-CAL-1 calls "the majority
case, correct behaviour, not a backlog", and it is even more correct than that
description: most of it is not a cross-unit reference at all. It is
`W1. Sort A, B and C. Give one evidence clue.` — the first question on a
worksheet — being read as week 1 and, quite rightly, refused rather than rewritten
into `Lesson 1. Sort A, B and C.`

Two consequences worth carrying into SX3.

**The scope finding is softer than it reads.** "Seven in eight Science pages carry
an un-re-tokenisable calendar token" is true of the gate's output, but over a
third of those pages carry **no calendar token in the blocking position**. They
carry a question number. The genuine cross-unit-reference population is smaller
than the refusal count suggests.

**The gate counts question numbers as pupil-facing calendar tokens.** `FORBID`'s
`\bW(?:eek)?\s?\d+\b` cannot tell `W1.` on a worksheet from `W1` meaning week 1,
so every hit count the gate has ever produced includes them. **Not changed here** —
narrowing `FORBID` changes what the gate blocks on, and that wants a ruling, not
a commit. Filed beside the UNSEEN asymmetry in D20, which is the same shape of
problem in the opposite direction: one pattern sees what it should not, the other
does not see what it should.

## D22 — R-CAL-1 does not apply to `Tutor_Time/` or `Assembly/`

LF1-M §8e. Stated here so no future relabelling pass reaches for them.

The tutor-time sessions carry **batch slots**, not spine weeks. "Batch 03 · 28 Sep"
is a position in a publishing run of three linked morning sessions a week; it is
not `Aut1·W4`, it does not map through `_sownb/TERM_DATES.md`, and it has no
manifest week to be relative to. A tool that turned a batch number into
"Lesson n of N" would be inventing a sequence that does not exist — the same
class of error as the 121, with a different vocabulary.

**So:**

- `tools/relabel_public.py` is never run over `Tutor_Time/` or `Assembly/`, in
  report, apply, revert or gate mode.
- Batch and week labels in those trees are **not** bound to spine or calendar
  tokens, and the forbidden-token gate's vocabulary does not govern them.
- The placeholder dates (14 Sep → 14 Dec, break week of 26 Oct) are **not**
  resolved against the real calendar and are never presented as scheduled (§8f).
- `[PLANNED]` sessions are proposals: no route, no card, no catalogue entry.

The naming follows the same logic and is ruled in §2a: successors route under
`Lessons/Tutor_Time/<strand>/<id>/` with strand folders `Behaviour`,
`Safeguarding`, `British_Values`. Cards, hub copy, catalogue entries and search
text say **"Tutor Time"**, never "assembly". `Assembly/` survives only as the
three genuine assembly routes among the retiring originals, plus their three
posters, behind successor-pointer pages. **No new `Assembly/` routes.**

The estate already agreed with the ruling before it was made: across the 42 decks
measured, visible text carries `tutor*` 126 times against `assembl*` 61, and not
one `<title>` says assembly.
