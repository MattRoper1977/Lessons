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
