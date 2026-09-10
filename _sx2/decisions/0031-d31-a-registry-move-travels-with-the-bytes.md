## D31 — a registry move travels with the bytes that need it

Any PR that changes the bytes of an admitted served path MUST carry the registry
move **in the same commit**. Not the next PR, not a follow-up, not "once this
lands". The same commit.

Enforced by `tools/lf1/check_admission_move.py` reading the registry **at
`builder_ref`**, and the guard joins REQUIRED CHECKS so it cannot be waved
through by a green-on-main illusion.

**A path with no row in Site main's registry is NOT "not served, ignore."** It is
`[ARRIVING, digest]` and it is checked.

### The evidence, which is two of my own merges

| breach | what it changed | what it did not carry |
|---|---|---|
| `#475` (Ruling 1) | `Science_Teesside/Grow/v3_40min/manifest-v3.json`, the ten Grow weeks | no registry move |
| `aee37a1f` (Ruling 2) | the F6 no-week marker in three family manifests | no registry move |

Both asked *"is this only manifest data?"*, got "yes", and merged. That is the
wrong question, and it is precisely the question D11 exists to replace: *does this
change the bytes of a path the registry already admits?* The publication was red
on main for about eighty minutes and named all four paths exactly.

### Why the guard did not catch it

It was pointed at a Site **main** checkout. Three of the four paths have no row
there at all, so each fell into "not served, ignore" — and it printed
`of those, served paths : 0` in the same hour the publisher was blocking on those
very paths. The publisher reads the record from the builder checkout at
`builder_ref`, never Site main (**D1**), and the two are different lineages that
disagree by thousands of rows.

A guard that reads the wrong authority does not fail. It agrees with you.

That is fixed at the read site — `--site` resolves `builder_ref` from the
publication workflow and the run now names the registry it read — and D31 closes
it at the policy site, so the rule does not depend on anyone remembering to pass
the right flag.
