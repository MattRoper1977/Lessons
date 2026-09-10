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
