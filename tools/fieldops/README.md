# FieldOps — P2

Five single-file offline apps: a Teacher Studio that mints missions and reads
evidence capsules, and four pupil-facing labs. `release/` is what was handed
over. `staging/` is built from it, and is **not deployed anywhere** — see
"The two rulings" below — it merges, and merging does not deploy it.

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

**It exits 3**: every patch-scoped gate is green, and one pre-existing red is
recorded and left (see "Recorded and left alone").

---

## How the build works

`build.mjs` turns `release/` into `staging/` by applying seventeen named
transforms, each an exact-string swap that must match **exactly once**. A miss
throws. There is no hand-editing anywhere in the pipeline, so:

- `assert_unchanged.mjs` **U1** drops all seventeen and gets `release/` back byte
  for byte. Nothing else the builder does can be hiding in the shipped tree.
- `dropmatrix.sh` drops each one in turn and requires the verdict set to change.
  All seventeen are watched.

| id | what |
|---|---|
| T1–T3 | the three localStorage calls: the boot read, the write, the explicit clear |
| T4 | `prefers-reduced-motion` seeds `body.calm` at boot |
| T5a/b | the Studio's one inline `onclick`, replaced with a delegated listener |
| T6a/b | `csvCell` — a leading `= + - @` is neutralised on CSV write |
| T7 | the Wilton band boundaries (R-Wilton-3) |
| T8a/b/c | the C21 and C24 feeds, in all three places they have to exist |
| T9 | the residue label on the column |
| T10 | the refusal message teaches instead of dead-ending (Ruling A) |
| T11 | the five printed tray temperatures (Ruling B) |
| T12 | the caption separating tray temperature from boiling range (Ruling B) |

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
| C21 | *no button* | **fuel-oil** | fuel-oil |
| C24 | *no button* | *cannot be distilled* | fuel-oil |

**Release scores 1 of 5 selectable. Staging scores 6 of 7** — C24 declared
unreachable by design, and `W-DESIGN` asserts that the undistillable set is
*exactly* the declared set, so a future feed that quietly stops working cannot
hide inside the declaration.

`C11`, `C15` and `C16` are also checked, and are labelled in the output as
**UNIT-LEVEL — NOT USER-REACHABLE**, because the feed set is a closed list and
nobody can select them. They are a `wTray()` call, not pupil experience, and the
report says so on every line.

---

## The two rulings, as issued and as landed

### Ruling A — C21 lands as the taught fuel-oil feed; C24 stays

Adding C24 was not enough on its own. `runDistil` needs
`effectiveFurnace ≥ wBoil(feed) + 20`. C24 boils at 430 °C so it wants 450 °C;
the furnace slider stops at **390 °C**, and it stops there because that is what
the plant this lesson models actually runs at.

**C21 is the answer, and it is the only one.** It boils at 370 °C, needs 390 °C,
and distils at the existing ceiling — measured across C18–C24, where C22 already
needs 410 °C and every heavier feed needs more. C21 sits in the fuel-oil range
(C20–C50) on real chemistry, so nothing was invented to make it reachable.

**C24 stays selectable and stays unable to vaporise**, and `W-R-C24` still
reports UNREACHABLE rather than being quietly converted to a pass by C21's
arrival. The suite distinguishes *declared* from *undeclared* unreachable, so
that line stays visible without pinning the gate at exit 2 forever.

The refusal message now teaches (T10). It had to become two sentences, not one,
because one cannot be true of both situations:

- furnace merely turned down →
  *"C14H30 boils at 230 °C, so it needs about 250 °C to enter the vapour stream.
  The furnace is at 160 °C — raise it."*
- this column can never boil it →
  *"C24H50 boils at 430 °C. This column's furnace only reaches 390 °C, so C24H50
  never enters the vapour stream — it leaves at the bottom as residue."*

Telling a pupil sitting at 160 °C on a C14 feed that the column can never do it
would be false, which is why `T10b` exists as its own control.

### Ruling B — the five printed tray temperatures are corrected

The column printed five tray temperatures that were consistent with the *old*
bands. Under the corrected bands they contradicted the code on four of five
labels, so a pupil picking C10 saw the marker land on the tray reading
*150 °C · kerosene range* while the readout said *petrol range*.

Adopted: **below 25 · 110 · 220 · 320 · 400**. Each falls inside the band its own
label names under `25/160/280/360/960`, and `W-DIAG` — the same comparator that
caught the regression — now reads **5 of 5** against release's 4 of 5. Ruling B's
second limb is `W-DIAG-MARK`, which runs the comparison across every selectable
feed rather than only the five trays: for each feed that distils, the tray the
marker lands on and the readout must name the same fraction. 6 of 6 on the fixed
build.

`below 25°C` rather than `<25°C`, so the marker needs no HTML entity inside SVG
text. The control handles it as two claims, not one: everything under 25 is
gases **and** 25 itself is not, so the word "below" cannot be used to dodge the
assertion.

**The named cost, restated so nobody meets it as a surprise:** the corrected tray
temperatures no longer match the numbers printed in most textbook column
diagrams. That is the trade Ruling B makes — a pupil comparing app and textbook
sees a difference, where a pupil using the app alone previously saw a
contradiction. The caption (T12) is what makes that trade survivable, which is
why it is not optional:

> **Tray temperature** is where a fraction condenses in this column.
> **Boiling range** is a property of the molecules themselves. Related, but not
> the same number — which is why a tray label and a feed's boiling point do not
> have to match.

## Recorded and left alone

`p26_inputs.mjs` states its predicate before it counts, because "38" is not a
measurement until you say 38 of what: **`<input>` elements in the four
pupil-facing labs, Studio excluded**. Other defensible predicates on the same
tree give 72, 49 and 265.

**22 of those 38 inputs have no accessible name** — the alias field and every
range slider. Identical on release; the patch neither caused it nor worsened it
(`A1` proves no name was lost and that exactly the two authorised buttons were added, each named). Out of P2's
scope, so: recorded, left, exit 3 from that gate alone.

## Transport

`transport.mjs` runs all four `{release, staging}` Studio × lab combinations in
both directions — mission out, capsule back — because a partial deploy is the
normal case. All eight pass. Every mission fixture is minted by a real Studio
through its real export button; none is hand-written. The release Studio cannot
mint a C24 mission at all, which is recorded as a declared asymmetry rather than
filled in with an authored stand-in.

---

## The split — where the labs and the Studio went

| half | repo | path |
|---|---|---|
| labs 01–04 | Lessons | **`Science_Teesside/Build/v4_fieldops/`** |
| 00 Teacher Studio | `Matt-s-Apps-` | **`FieldOps_Teacher_Studio.html`** (repo root, matching the 36 flat `*_Studio.html`) |

**The merged Lessons path, quoted so the VSL order can cite it rather than
re-derive it: `Science_Teesside/Build/v4_fieldops/`.** It is a sibling of
`v3_40min`, at the same depth, which is why the NAV-1 href resolves identically.

`tools/fieldops/split_transport.mjs` proves transport across it **both
directions**: three missions minted in `Matt-s-Apps-` load into the lab in
Lessons (C14, C21, C24), and a capsule exported from the lab verifies in the
Studio. NAV-1 is checked to resolve to a file that exists *and* to be the
byte-identical href its eleven neighbours use.

**Every fixture is authored by that harness and says so in its own filename** —
`AUTHORED-BY-HARNESS_not-a-pack-sample_*`. The pack's twelve `.buildmission.json`
samples were never shipped, so none was available; presenting an authored fixture
as the pack's own would be the worst thing this pass could do.

## Three places the order's stated premises did not survive measurement

**1. "Add exactly one feed, C24" does not make fuel oil reachable.** C24 boils at
430 °C and `runDistil` needs `effectiveFurnace ≥ 450 °C`; the furnace slider stops
at 390 °C. Adding C24 alone leaves the fuel-oil band exactly as unreachable as
before, just with a button in front of it. **C21** — 370 °C, needs 390 °C — is the
only carbon number that distils at the existing ceiling and lands in fuel oil.
Both are present: C21 teaches the band, C24 stays and is told why it cannot
vaporise. Seven feeds, not five.

**2. "release 12" mis-assignments is 13 under a strict predicate, 12 under an
overlapping one — and the difference is the disclosure copy's own subject.**
Counting C5–C21 where each carbon number has exactly one correct fraction gives
**13**. Allowing C10 to be either petrol or kerosene — which is what real
refining does — gives **12**. Both are defensible; neither is quotable without
its predicate. The old `<=` build scores **2** and R-Wilton-3 **0** under both.

**3. "splash, NAV-1, `mbm_reading_theme` — all currently 0" is true of the labs
and also true of the family they join.** Measured in the co-location target:
NAV-1 on **11 of 15** files (the 4 without are the matrix, the guide and the
reflection window — not lessons); splash overlays **0 of 15**;
`mbm_reading_theme` **0 of 15**, and only **2 files in the whole Lessons repo**
carry it, both catalogue indexes.

So NAV-1 landed byte-identically. A splash overlay and a reading theme did not:
adding them would make these the only lesson files in the estate with either,
which is divergence dressed as conformance. **The regress trap is still
re-expressed** — `T14` asserts both limbs, release baseline **0** per page and
deployed expectation **exactly 1**, in the header form the eleven neighbours use.

## R-Wilton-3's advantage over the `<=` build is invisible to every user

Said plainly because it should be. The two chains the `<=` build gets wrong are
**C11 and C16 — neither is selectable**. Across the seven feeds a pupil can
actually choose, `<=` and R-Wilton-3 agree completely. R-Wilton-3 is still the
better rule — no chain can land on a boundary, so `<` versus `<=` stops being a
question anyone has to get right — but it buys correctness a user cannot see, and
saying otherwise would be overstating it.
