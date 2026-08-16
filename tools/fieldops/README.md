# FieldOps — P2

Five single-file offline apps: a Teacher Studio that mints missions and reads
evidence capsules, and four pupil-facing labs. `release/` is what was handed
over. `staging/` is built from it, and is **not deployed anywhere** — see
"Why this is not merged" below.

```sh
tools/fieldops/run.sh            # build staging/, run every gate
tools/fieldops/run.sh --drops    # also drop each fix in turn and check a gate notices
```

Exit codes are not interchangeable:

| code | meaning |
|---|---|
| 0 | everything green |
| 1 | a gate failed, or a regression was measured |
| 2 | a subject was **unreachable** — INCONCLUSIVE, never counted as a pass |
| 3 | patch-scoped gates green, a pre-existing red recorded and left alone |

**Today it exits 1.** That is deliberate and it is the point of the ledger below.

---

## How the build works

`build.mjs` turns `release/` into `staging/` by applying thirteen named
transforms, each an exact-string swap that must match **exactly once**. A miss
throws. There is no hand-editing anywhere in the pipeline, so:

- `assert_unchanged.mjs` **U1** drops all thirteen and gets `release/` back byte
  for byte. Nothing else the builder does can be hiding in the shipped tree.
- `dropmatrix.sh` drops each one in turn and requires the verdict set to change.
  All thirteen are watched.

| id | what |
|---|---|
| T1–T3 | the three localStorage calls: the boot read, the write, the explicit clear |
| T4 | `prefers-reduced-motion` seeds `body.calm` at boot |
| T5a/b | the Studio's one inline `onclick`, replaced with a delegated listener |
| T6a/b | `csvCell` — a leading `= + - @` is neutralised on CSV write |
| T7 | the Wilton band boundaries (R-Wilton-3) |
| T8a/b/c | the C24 feed, in all three places it has to exist |
| T9 | the residue label on the column |

## The Wilton band fix (T7)

`wBoil` is **untouched** — asserted, not asserted-about. Only the tray cut-offs
move, and each one lands in a gap:

```
bp<25 gases · bp<160 petrol · bp<280 kerosene · bp<360 diesel · bp<960 fuel-oil · else residue
```

`wBoil(n) = -50 + 20n` is always ≡ 10 (mod 20). None of `25 160 280 360 960` is,
so **no integer carbon number can land on a boundary**, not just none of the six
selectable ones. Every comparison is strict `<`; the earlier `<=` build is
reverted. `W-GAP` checks this for n = 1…200 rather than for the six feeds.

Through the real buttons, on the real furnace slider, reading what the lab tells
the pupil:

| feed | release says | staging says | correct |
|---|---|---|---|
| C6 | petrol | petrol | petrol |
| C10 | kerosene | **petrol** | petrol |
| C14 | diesel | **kerosene** | kerosene |
| C18 | fuel-oil | **diesel** | diesel |
| C20 | residue | **diesel** | diesel |
| C24 | *no button* | *cannot be distilled* | fuel-oil |

**Release scores 1 of 5. Staging scores 5 of 6.** Not 6 of 6 — see ruling A.

`C11`, `C15` and `C16` are also checked, and are labelled in the output as
**UNIT-LEVEL — NOT USER-REACHABLE**, because the feed set is a closed list and
nobody can select them. They are a `wTray()` call, not pupil experience, and the
report says so on every line.

---

## Why this is not merged: two rulings needed

### Ruling A — C24 is selectable but cannot be distilled

Adding the button was not enough. `runDistil` requires
`effectiveFurnace ≥ wBoil(feed) + 20`. C24 boils at 430 °C, so it needs 450 °C;
the furnace slider stops at **390 °C**. Selecting C24 and running distillation
gives *"Effective furnace 390°C is too low for this teaching feed to enter the
vapour stream."* — on staging **and** on release, confirmed independently by the
transport probe. The fuel-oil band is still never taught.

`W-R-C24` reports **UNREACHABLE**, not a pass and not a fail. The measurement is
in hand; the choice is not mine:

- **C21** boils at 370 °C, needs 390 °C, and distils at the existing ceiling —
  landing in fuel-oil under the new bands. C21 sits in the fuel-oil range
  (C20–C50) chemically, so this needs no invented number.
- **Raise the furnace ceiling to 450 °C** and keep C24. Real atmospheric
  columns run 350–400 °C, so this buys reachability with a temperature that
  does not exist in the plant it is modelling.
- **Leave it.** C24 stays as a feed that visibly refuses to vaporise, which is
  honest about heavy fractions but leaves the fuel-oil label untaught.

The order named C24, so C24 is what landed, in all three places, with
three-way identity re-asserted. This ruling is about the furnace, not the feed.

### Ruling B — the column prints a fourth set of numbers, and the fix contradicts them

The column diagram carries five tray temperatures as static SVG text. Nothing
had ever checked them against the code. `W-DIAG` now does:

| printed on the column | release puts it in | staging puts it in |
|---|---|---|
| 25 °C · gases | petrol ✗ | petrol ✗ |
| 80 °C · petrol range | petrol ✓ | petrol ✓ |
| 150 °C · kerosene range | kerosene ✓ | **petrol ✗** |
| 230 °C · diesel range | diesel ✓ | **kerosene ✗** |
| 300 °C · fuel oils | fuel-oil ✓ | **diesel ✗** |

Release agrees 4 of 5. Staging agrees 1 of 5. The 25 °C disagreement is
pre-existing (`bp<25` is strict, so 25 itself falls into petrol).

So the band fix, which is right about carbon numbers, makes the lab argue with
its own diagram: pick C10 and the marker lands on the tray labelled *150 °C ·
kerosene range* while the readout says *petrol range*. That is a new
contradiction on screen, and it is why `W-DIAG` is a **REGRESSION** and the
suite exits 1.

Correcting it means changing five printed temperatures — taught content beyond
the one content addition authorised in P2, so it is not done here. Column tray
temperatures consistent with the new bands would be roughly
`<25 · 110 · 220 · 320 · 400`.

**Neither ruling is a reason to un-fix the bands.** Release teaches four of five
selectable feeds into the wrong fraction. This is about which of the two changes
lands with it.

---

## Recorded and left alone

`p26_inputs.mjs` states its predicate before it counts, because "38" is not a
measurement until you say 38 of what: **`<input>` elements in the four
pupil-facing labs, Studio excluded**. Other defensible predicates on the same
tree give 72, 49 and 265.

**22 of those 38 inputs have no accessible name** — the alias field and every
range slider. Identical on release; the patch neither caused it nor worsened it
(`A1` proves no name was lost and the one added control is named). Out of P2's
scope, so: recorded, left, exit 3 from that gate alone.

## Transport

`transport.mjs` runs all four `{release, staging}` Studio × lab combinations in
both directions — mission out, capsule back — because a partial deploy is the
normal case. All eight pass. Every mission fixture is minted by a real Studio
through its real export button; none is hand-written. The release Studio cannot
mint a C24 mission at all, which is recorded as a declared asymmetry rather than
filled in with an authored stand-in.
