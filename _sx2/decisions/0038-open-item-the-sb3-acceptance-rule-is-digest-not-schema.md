## OPEN ITEM — the `.sb3` acceptance rule is a digest, not a schema

> **Nothing anywhere in the estate verifies that a file called `.sb3` is a
> Scratch project.** Admission is exact reviewed digest plus extension
> classification. A standing PR gate that parses every `.sb3` and refuses one
> that is not a valid Scratch 3 project does not exist and is not built by this
> order. **TRIGGER: wire it before a SECOND Scratch unit lands** — 122058
> (scoring), 119195 (variables), 122060, 121956 — **not before #493.**

This is an **open item, not a fix and not a defect blocking GC1**. It is recorded
here so the next Scratch unit cannot arrive without someone meeting it.

### The four facts, stated plainly

1. **Admission is exact reviewed digest.** `education_publication_admission.py`
   pins one sha256 per served path. `.sb3` was added to `INERT` so the census can
   *classify* the suffix at all; the suffix decides nothing about acceptance.
   The module's own comment already says it: *"A suffix is not a safety boundary…
   Every emitted path and byte needs approval."*
2. **Nothing verifies a `.sb3` is a Scratch project.** Not the publisher, not the
   census, not any check in the publication workflow. A `.sb3` is admitted on the
   same terms as a `.zip`, a `.pptx` or a `.png`.
3. **G1's `scratch-parser` run was by hand**, over #493's 23 files, once. It is
   not wired into any workflow — measured: `grep -rln "sb3" .github/workflows/`
   returns nothing in any of the three repositories.
4. **`tools/gc1/check_sb3_parents.py` is unwired too.** It is the only
   `.sb3`-aware instrument in the estate and no workflow calls it.

### What the digest rule does and does not buy, red-proved

Against the real built tree, with a genuine zip holding a script and no
`project.json` (328 B, `sha256 fffbcb7e…`):

| planted | result |
|---|---|
| renamed zip at a **new** `.sb3` path | **REFUSED** — `UNREVIEWED …/EVIL_Renamed.sb3` |
| its bytes at an **admitted** `.sb3` path | **REFUSED** — `CHANGED …/W01_Start.sb3` |
| its bytes **with a reviewed row written for them** | **ACCEPTED** |
| `disguised code cannot enter as sb3`, all three trees | planted **FAIL**, restored **PASS** |

Rows one and two are real protection: a renamed archive cannot reach the site by
wearing the extension. Row three is the boundary — **a reviewer who writes a
digest row for non-Scratch bytes gets them served**, and today nothing would tell
them. That is the whole gap, and it is a review-surface gap rather than an
attacker-surface one.

### Why the trigger sits where it does

With one Scratch unit and 23 files reviewed by hand, the digest rule and a
one-off parse are proportionate. The moment a **second** unit lands the hand-run
stops scaling and its absence stops being visible: nobody re-runs a check that
lives in a commit message. So the gate is owed to the next unit, not to this one,
and blocking #493 on it would delay a unit whose 23 files *were* parsed to buy a
control for files that do not exist yet.

### What wiring it means, when someone does

A PR-time gate over every tracked `.sb3` in the changed unit: parse with the
official `scratch-parser`, refuse anything that is not a valid Scratch 3 project,
and ship it with a planted red — a renamed non-Scratch zip must make the gate
fail, proven in the same commit, per §0.3.

**It must assert schema validity only, never behaviour.** D39's six seeded-fault
files are *valid* Scratch projects with deliberately wrong logic, and a gate that
reached for correctness would delete the lesson.
