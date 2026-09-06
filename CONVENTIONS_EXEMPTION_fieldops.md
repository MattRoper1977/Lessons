# FieldOps v4 — declared exemption list

**Written 2026-08-16, the day the four labs merged into this estate. Not a
proposal to change them. Matt rules on the exemption; this file only records
what they do and do not inherit, so the next conformance sweep reads them as a
declared position rather than as four regressions to quietly rewrite.**

Subjects: `Science_Teesside/Build/v4_fieldops/01–04`, and their counterpart
`FieldOps_Teacher_Studio.html` in `Matt-s-Apps-`.

## What they are

Instruments, not lessons. A lesson is read; these are operated — a distillation
column with a furnace ceiling, a bridge-lift permit, an estuary survey, a wind
operations desk. The teacher mints a mission in the Studio, the pupil runs the
lab, the lab exports an evidence capsule and the Studio verifies it. Nothing in
that loop is a slide.

## Re-measured on the placed files, 2026-08-16

The close order carried a pre-patch measurement of this list. Two of its figures
had gone stale by the time the labs landed, because two of the P2 transforms are
exactly the estate conventions it said were missing. Measured again on the merged
blobs rather than inherited:

| convention | order's figure | measured on the placed files | position |
|---|---|---|---|
| `<h1>` per page | 1, corrected | **1** each | **inherited** |
| back link (NAV-1) | 0 `<a>`, so none | **1** `<a>` each — `<a class="mbmhome" href="../../../index.html" aria-label="Back to the Lessons catalogue">← Lessons</a>` | **inherited** (transform T13, with its 44 px target, focus ring and `print:none` rule asserted) |
| "Made by Matt" | 0 | **1** each — `Made by Matt · Science Teesside · BUILD v4 FieldOps` | **inherited** (transform T14) |
| "Progress Schools" | 0 | **0** | **exempt** — these carry no partner attribution, and none was ever authored |
| `mbm_reading_theme` | 0 | **0** | **exempt** — see below |
| tier vocabulary | Guided/Core/Stretch | **Guided / Core / Stretch** | **exempt** — see below |

## The two real exemptions, with reasons

**`mbm_reading_theme`.** The reading-theme control retints a page for a reader
who needs it. These labs are not pages of prose: the colour on a distillation
column is *data* — a tray band, a temperature, a phase. Retinting them changes
what the instrument says, which is a different act from making text easier to
read. Until there is a theme that leaves the instrument's own colour alone,
inheriting the control would make the lab lie politely. **This is the exemption
most worth arguing with, and the argument is a design one, not a conformance
one.**

**Guided / Core / Stretch, against the estate's Supported / Standard / Stretch.**
These are not the same three things wearing different names. Supported/Standard
are differentiation tiers — the same task, more or less scaffolding. Guided/Core
are *modes of the instrument*: Guided walks a mission with the column's
decisions narrated, Core hands the same column over with the narration off. A
pupil moves between them within one session and back again, which a
differentiation tier is not meant to do. Renaming them to match would make the
estate's vocabulary consistent and the lab's behaviour undescribable.

## What is not claimed here

This list says what these files do; it does not say the exemptions are correct.
Two of the six rows resolved themselves the moment the patch landed, which is
the argument for measuring rather than inheriting, and it is a reason to expect
the remaining two to be arguable as well. Anything Matt rules on goes back into
this file rather than into a commit message.

## Addendum, 2026-08-19 (FINISH v2) — two rulings and one repair

**The labs carry no back-link to the Studio. RATIFIED, not an omission.** A pupil
running a lab has no use for the teacher's mission-minting tool, and a link into
it from a pupil surface would be the only such link in the estate. NAV-1 ("←
Lessons", transform T13) remains the labs' one way out and is asserted by S3/S3b
in `tools/fieldops/evidence/split_transport.out`. Do not add a Studio link; if a
future conformance sweep counts one missing, this line is the answer.

**The Studio's launch links are absolute, and the prefix is derived.** Transform
**T16** rewrites the four engine entries from bare filenames to
`https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/<lab>`. Before
it, "Launch mission" on the Apps origin resolved to a path that exists only in
Lessons and 404'd — the split's predicted failure, shipped. The prefix is not a
constant anyone typed: it is `LESSONS_ORIGIN` (`tools/verify_served.mjs`) joined
to `PLACED` (`tools/verify_fieldops_served.mjs`), and control **T16-derive** in
`controls.mjs` re-derives that join on every run, so if the origin moves in one
file and not the other the harness goes red instead of shipping a second 404.

**Why it survived a green harness, worth recording.** `split_transport.mjs`
proved the *file-import* transport (`setInputFiles` on `#missionFile`) and built
the lab URL itself, so the one string the launch route depends on was never read.
**S4a/S4b/S4c** now serve the two trees on two local origins, click through the
real `#launchMission` href, and require the pre-T16 bare filename to still 404 on
the Apps origin. **S2c** adds the tamper limb the capsule round-trip lacked: a
mutated capsule must be refused by the same import path that accepts a good one.

## Addendum, 2026-08-19 (FIX-1) — the directory hub, and the third path this pass places

**A fifth file is placed in `v4_fieldops/`, and it is not a lab.**
`Science_Teesside/Build/v4_fieldops/index.html` is an authored hub: title, one line
saying these are instruments and not lessons, and four links to the labs by relative
filename. It carries the NAV-1 back-link and, per the ruling above, **no link to the
Teacher Studio**.

**Why it exists.** GitHub Pages serves no directory listing. A directory holding an
`index.html` is served as that file; a directory without one is a 404. Until this
addendum `v4_fieldops/` held only the four labs, so
`https://madebymatt.uk/Lessons/Science_Teesside/Build/v4_fieldops/` was a **404 by
construction** while every lab beneath it served — which is how the estate came to
hold four instruments the owner could not open from the folder they live in. The
exemption doc's subject list therefore now reads: the four labs, this hub, and the
Studio in `Matt-s-Apps-`.

**It is required, not tolerated.** `verify_fieldops_served.mjs` names it in
`PLACED_NON_LAB`, and check **D1** reads *required* = the builder's `LABS` plus that
list. Delete the hub and D1 reds naming it; add any other file to the directory and D1
reds naming that. Both limbs are proven by mutation — controls **C4** and **C5** —
rather than observed passing, and the placed directory is hashed by name and bytes
before and after with the equality asserted, since those controls write inside it.

**What did not change, and why.** The builder does not emit this file and is not asked
to: `build.mjs` transforms release labs, and the hub is authored, with no release
counterpart to transform. All four `resources.json` entries already target lab **files**,
not the directory, so the catalogue needed no retarget; all four of the Studio's T16
engine URLs already target lab **files**, so nothing in `Matt-s-Apps-` moved.
