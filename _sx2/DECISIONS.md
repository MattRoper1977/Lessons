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
