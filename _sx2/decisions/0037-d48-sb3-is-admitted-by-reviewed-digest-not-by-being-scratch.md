## D48 — `.sb3` is admitted by reviewed digest, not by being a Scratch project

Site `2e49afdd` adds `.sb3` to two allowlists: `PUBLIC` in `build_education.py`
(so the publisher emits it at all) and `INERT` in the admission census (so the
census can classify it). Without both, all 23 Scratch projects in the GROW
Computing unit were dropped by extension — 163 source files produced 140 — and
their sibling links would have 404ed on the served site. See D47.

### The rule that is actually in force

**Extension classification + exact reviewed digest.** Nothing at publication
time asks whether an `.sb3` is a Scratch project.

Red-proved against the real built tree, with a genuine zip containing a script
and no `project.json` (328 bytes, `sha256 fffbcb7e…`):

| planted | result |
|---|---|
| the renamed zip at a NEW `.sb3` path | **REFUSED** — `UNREVIEWED education-lessons/…/EVIL_Renamed.sb3` |
| the renamed zip's bytes at an ADMITTED `.sb3` path | **REFUSED** — `CHANGED education-lessons/…/W01_Start.sb3` |
| the renamed zip's bytes **with a reviewed row written for them** | **ACCEPTED** |
| `disguised code cannot enter as sb3`, ×3 trees | planted **FAIL**, restored **PASS** |

The first two are the protection, and it is real: a renamed archive cannot reach
the site by wearing the extension, exactly as a renamed `.zip`, `.pdf` or `.png`
cannot. The census comment already says so in its own words — *"A suffix is not a
safety boundary… Every emitted path and byte needs approval."*

### The limit, stated rather than glossed

The third row is the honest boundary. **If a reviewer writes a digest row for
non-Scratch bytes, they are served.** `.sb3` is no weaker than the eighteen other
`INERT` types in this respect, and no stronger.

So: **an acceptance rule of "schema-valid Scratch 3 project, not extension match"
is NOT the rule in force today, and this commit did not make it one.** Measured:

```
grep -rln "sb3" .github/workflows/     ->  (no matches)
```

AMEND-3R-GC1 **G1** ("all 23 `.sb3` pass the official Scratch 3 schema, npm
`scratch-parser`, 23/23 or red") was run by hand for #493. It is **not wired into
any workflow**, so it is a one-off measurement, not a standing control. The only
`.sb3`-aware instrument in the repository, `tools/gc1/check_sb3_parents.py`, is
likewise unwired.

**This is reported as a red, not as a pass.** Making schema validity the
acceptance rule means a standing gate that parses every `.sb3` in the unit on
every PR, and refuses one that is not a Scratch 3 project. That gate does not
exist. Nothing here should be read as claiming it does.

### DO-NOT-AUTOFIX interaction

D39 forbids repairing the six seeded-fault `.sb3`. A schema gate is compatible
with that — a seeded fault is a *valid* Scratch project with wrong logic — but
any future gate must assert schema validity only, never behaviour.
