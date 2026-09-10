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
