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
