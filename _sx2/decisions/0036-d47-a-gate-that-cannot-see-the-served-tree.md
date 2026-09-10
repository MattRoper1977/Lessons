## D47 — a gate that cannot see the served tree is not a gate

AMEND-3R-GC1 **G9** asks whether every week's sibling `.sb3` link resolves **at
its served path**. It was reported satisfied — *15 sibling links, 15 resolve, 0
missing* — measured against the repository working tree.

On the working tree that question cannot be asked. The file sits beside the
lesson whether or not the publisher would ever emit it. Measured on a real
three-repository build:

| | |
|---|---:|
| unit files in source | 163 |
| unit files in the built `education-lessons` tree | **140** |
| difference | **23** — every `.sb3` in the unit |

`.sb3` was not in `build_education.py`'s `PUBLIC` extension allowlist, so the
publisher dropped all 23 by extension. Nothing errored. Every gate stayed green
and 23 links would have 404ed the moment a pupil clicked one.

### The rule

**A gate whose subject is the served site is run against a built publication
tree, or it is not run.** `--served` is not a nicety; without it the gate is
measuring this repository, and the two disagree in both directions.

Two directions, both real, both measured here:

- **False green.** The sibling `.sb3` exists in the repository and not on the
  site. Fixed by admitting `.sb3` (Site `2e49afdd`) and by asserting G9 only
  under `--served`, where it resolves each authored `href` against the built
  tree. Off the served tree G9 now says nothing at all, which is honest.
- **False red.** A built lesson asks for `/Lessons/assets/catalogue/lesson-navigation.js`,
  a **site** path. Opened over `file://` that resolves to the filesystem root and
  404s, so the first served run reported eight console errors that do not exist
  on the site. The gate now serves `education-lessons` at `/Lessons/` over HTTP.

### And one probe that was measuring nothing at all

G6 counted a `.mbm-usage` element as the publisher's usage layer. Measured
across the built tree:

| marker | built lesson pages carrying it |
|---|---:|
| `.mbm-usage` markup | **2 of 1502** — both hubs |
| `script src="/assets/usage-client.js"` | **817 of 1502** |

`usage_discovery.inject()` emits `.mbm-usage` only under `choice=True`, which is
hubs. A lesson page receives the bare adapter script. So the probe named a
selector no lesson page in the estate has, and would have returned false forever.

Correcting the selector is not enough, and this is the part worth keeping: **which
lessons carry the adapter is a catalogue decision, not a page property.** Only
rows whose `event_types` include `lesson_open` are injected. So it cannot be a
per-lesson pass/fail on any unit. It is now compared against a peer unit —
`--peer` — and only a *disagreement with the neighbour* is a red:

```
usage adapter vs peer : this unit 0 of 8, GROW 0 of 11
```

The live GROW ICT unit beside it is also at zero. Matching the neighbour is the
correct state; a unit that differed from it would be the finding.

### Standing

This is the sixth instrument in a week to report on a property it could not
observe, and the third of the six that was mine. Per D46 the correction is
recorded, not just the result, and the instrument ships with both controls: the
self-test now judges **both postures**, so the served half can never again go
unexercised. 15 checks → 23.
