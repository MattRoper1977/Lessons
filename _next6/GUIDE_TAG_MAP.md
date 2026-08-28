# GUIDE TAG MAP — the nine landed 2026-27 packs

`ORDER N6-I · I5` · measured 2026-08-28 · branch `claude/new-session-q7ztqq`

**Nothing in this document has been applied. Nothing was patched. This is a map and a
price, as the order requires.**

---

## The headline, before the tables

Three things were measured that change what this job is:

1. **Staff guidance is already invisible to the room.** 132 of the 159 files carry
   staff-facing guidance strings. **Zero** of them put any of it on the pupil-facing
   surface — measured by activating every slide in turn and reading `innerText`, which
   excludes a closed `<dialog>`, a `[hidden]` element and any `display:none` subtree.
   PH-3's purpose is already achieved by the chassis. What a toggle would add is a
   *persisted preference*, not a capability.

2. **What IS on the wall is one pack and a 13-file tail of a second**, not twelve packs.

3. **No existing selector isolates it.** The hide-set cannot be mapped from what exists;
   it has to be authored. That is the cost.

---

## §1 · What the twelve packs are, and what could be measured

The order says twelve packs. **Nine are in the repository and were measured. The three Art
packs are not** — they were an intake tree in the previous session and no commit on any
branch ever added them, so their selectors cannot be counted here and are not guessed at.
That is 159 HTML files measured of the 192 the order counts.

## §2 · Why the PH-3 patcher cannot see any of this

`_eca1/tools/guidepatch.js` classifies by `.li-box`, `.task-box` and `.wit-panel` and tags
with `data-mbm-guide`. Across all nine packs those occur **0, 0, 0 and 0** times. The
patcher therefore classifies all 159 as chassis `doc` and skips every one, exactly as the
previous pass reported.

**The semantic hide-set that was "already ruled" does not map either.** Checked
case-insensitively across all 159 files:

| PH-3 vocabulary | files carrying it |
|---|---:|
| `sow-strip` | 0 |
| "How it works" | 0 |
| "Key Question" | 0 |
| "Spark" | 0 |
| "👀 Look:" | 0 |
| "Key Idea" | 5 |
| "Instructions" | 11 |
| "Step 1" | 42 |

So this is not "the same job with different selectors". Six of the eight ruled markers do
not exist in these packs at all.

## §3 · The guidance-container census — what actually holds the guidance

| pack | html | `#teacherDialog` | `#taOverlay` | `#taDialog` | `#tool-ta` | `data-ta1` | `data-ta2` | `.staff-card` | `.note` | `.drawer-card` | `.route*` | `.tierbtn` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `BUILD_ASDAN` | 28 | 24 / 24 | — | — | — | 24 / 216 | 24 / 216 | — | — | — | 25 / 218 | — |
| `GROW_ASDAN` | 22 | — | 18 / 18 | — | — | 18 / 162 | 18 / 162 | 18 / 72 | 21 / 203 | — | 19 / 90 | — |
| `LAUNCH_ASDAN` | 32 | — | — | 30 / 30 | — | 30 / 270 | 30 / 270 | — | 30 / 150 | 30 / 210 | 30 / 90 | — |
| `BUILD_Science` | 15 | — | — | 12 / 12 | — | 12 / 108 | 12 / 108 | — | 12 / 48 | — | 12 / 96 | 12 / 108 |
| `GROW_Science` | 16 | — | — | 12 / 12 | — | 12 / 108 | 12 / 108 | — | 12 / 48 | — | 12 / 96 | 12 / 108 |
| `LAUNCH_Science` | 21 | — | — | 18 / 18 | — | 18 / 162 | 18 / 162 | — | 18 / 234 | — | 18 / 144 | 18 / 162 |
| `BUILD_Humanities` | 8 | — | — | 6 / 6 | — | 6 / 54 | 6 / 54 | — | 8 / 98 | 6 / 24 | 6 / 18 | 6 / 36 |
| `GROW_Humanities` | 8 | — | — | — | 6 / 6 | 6 / 54 | 6 / 54 | — | 6 / 14 | — | 6 / 16 | 6 / 36 |
| `LAUNCH_Humanities` | 9 | — | 6 / 6 | — | — | 6 / 54 | 6 / 54 | — | 7 / 58 | 6 / 48 | 6 / 18 | 6 / 18 |
| **total** | **159** | **24 / 24** | **24 / 24** | **78 / 78** | **6 / 6** | **132 / 1188** | **132 / 1188** | **18 / 72** | **114 / 853** | **42 / 282** | **134 / 786** | **60 / 468** |

*(files carrying it / total occurrences. `—` is zero.)*

**Four container families, disjoint, and every one of the 132 lesson decks has exactly
one.** 24 + 24 + 78 + 6 = 132.

| container | packs | what it is in the DOM | visible at load |
|---|---|---|---|
| `#teacherDialog` | BUILD_ASDAN (24) | `<dialog role="dialog" aria-modal="true">` | no |
| `#taOverlay` | GROW_ASDAN (18), LAUNCH_Humanities (6) | `<div class="overlay" aria-hidden="true">` | no |
| `#taDialog` | LAUNCH_ASDAN (30), Science ×3 (12+12+18), BUILD_Humanities (6) | `<div class="overlay" role="dialog" aria-modal="true" hidden>`; in Science a `<dialog data-audience="staff">` | no |
| `#tool-ta` | GROW_Humanities (6) | `<section class="toolsection" role="tabpanel">` in a tools drawer | no |

**`data-ta1` / `data-ta2` are ATTRIBUTES, not elements** — 1188 of them across the nine
packs, on `<section class="slide">`. No CSS selector can hide an attribute; only the
container that renders it. Anyone planning a hide-set of selectors needs to know that
before starting, because it means the guidance payload and the thing you can actually
target are different objects.

## §4 · What is visible to the room — the real hide-set

Measured by activating every slide in turn and reading the visible `innerText`. The
all-slides walk is load-bearing: these decks hide non-active slides with
`.slide{display:none}`, so reading `innerText` at load returns the title slide and nothing
else. A first pass reported route labels as invisible in BUILD_ASDAN and LAUNCH_ASDAN
purely because they sit on slide 4.

| pack | string family | in source | **visible** |
|---|---|---:|---:|
| BUILD_ASDAN | SoW cell reference — `'BUILD Weekly - Autumn'!B181` | 28 | **28** |
| BUILD_ASDAN | `Exact SOW outcome:` | 25 | **25** |
| BUILD_ASDAN | `Estate sequence` | 26 | **26** |
| BUILD_ASDAN | `Inherited mapping` / `Inherited evidence` | 25 | 1 |
| BUILD_ASDAN | `AQA UAS` unit title | 25 | 1 |
| LAUNCH_ASDAN | `AQA UAS` unit title | 13 | **13** |
| GROW_ASDAN · Science ×3 · Humanities ×3 | all of the above | 0 | **0** |

**That is the entire visible staff-facing surface across 159 files.** One pack, four string
families, plus a 13-file tail in a second pack.

**Route labels are pupil-facing and stay.** `Supported route` / `Standard route` /
`Stretch route` are visible in GROW_ASDAN 19/19 and LAUNCH_ASDAN 30/30, and a pupil chooses
between them. `.route*` is a **keep-visible** selector, not a hide candidate, in every pack
that has it (134 files, 786 occurrences). Treating "route metadata" as a hide target — the
reading the order's wording invites — would remove the pupil's own access route from the
screen.

## §5 · The overlap risk, measured in the DOM

For every class in every deck: how many of its instances carry a staff string in their
**own** text — text not inside a nested classed child?

| pack | classes ALWAYS staff-bearing | classes MIXED (hiding them takes pupil content) |
|---|---|---|
| BUILD_ASDAN | `.hero` 24, `.lesson-link` 24, `.table-wrap` 1 | `.chip` 24/96, `.small` 56/58, `.card` 28/404, `.print-page` 24/72, `.good` 1/98, `.safe` 1/29, `.stage` 1/10 |
| LAUNCH_ASDAN | none | `.box` 13/420, `.guard` 13/60, `.drawer-card` 13/210 |
| the other seven | none | none |

**"Always staff-bearing" is necessary and not sufficient.** `.hero` is 24/24 and still
holds the lesson's own `<h1>`. Hiding it would take the lesson title with it.

**The decisive question — does any class isolate staff text, carrying nothing else?**

| pack | answer |
|---|---|
| BUILD_ASDAN | **`.small` — yes, and it is the only one.** 24 of 24 instances in the 24 lesson decks are the `Source:` cell-reference line and nothing else; 56 of 58 across all 28 files, the two exceptions being external ASDAN spec URLs in the assessor-side planning file, which is outside the evidence-surface set anyway. **`.chip` — no.** 24 of 96 are clean (`"Estate sequence W9"`); the other 72 are the lane, unit and week a pupil reads. |
| the other eight | **No class isolates staff text.** |

*(A correction worth recording, because it changes the answer. The first run of this probe
was case-sensitive and reported `.small` as mixed with ten pupil-facing instances. Those ten
were `"Secondary estate sequence metadata: Week 15"` and its neighbours — staff strings the
pattern missed on a lower-case `e`. A probe that is case-sensitive about prose invents
overlap. `i5_overlap.mjs` carries the fix and a comment saying why.)*

And the most obviously staff-facing string on the opening slide, `Exact SOW outcome:`, sits
in an **unclassed** `<p><strong>` inside `.hero`. There is no selector for it at all.

**So the hide-set is one-third mappable and two-thirds authoring.** One of the three visible
BUILD_ASDAN items (`Source:` → `.small`) can be hidden with an existing selector today. The
other two — `Estate sequence W9` and `Exact SOW outcome:` — need markers added to specific
elements. That is what the previous pass meant by *"the mapping is the work"*, now shown at
element level rather than asserted, and it is the main driver of the cost below.

## §6 · Worked example — `BUILD_ASDAN_A2_COMM_W1_Review_Progress_and_Solve_a_Problem.html`

Slide 1, "Lesson overview", exactly as a class sees it on the wall:

```
BUILD ASDAN | Community & Vocational | Autumn 2 · Week 1 | Estate sequence W9
Project Checkpoint: Solve the Real Blocker
Exact SOW outcome: Review progress and solve a problem as a team.
Source: 'BUILD Weekly - Autumn'!B181 · 'BUILD Weekly - Autumn'!C181
Learning objective: I can help the team review progress and choose one workable
problem-solving action.
Success criteria
  I can identify one completed, in-progress or blocked project action from evidence.
  I can suggest or choose one safe solution without blaming a person.
  I can explain how the agreed action changes the project plan.
```

**Would be tagged (3 items, all on this one slide):**

| text | carrier | can an existing selector reach it? |
|---|---|---|
| `Estate sequence W9` | `<span class="chip">`, the 4th of 4 | **no** — `.chip` also carries the three above it |
| `Exact SOW outcome: Review progress and solve a problem as a team.` | unclassed `<p><strong>…</strong> …</p>` inside `.hero` | **no** — no class at all |
| `Source: 'BUILD Weekly - Autumn'!B181 · 'BUILD Weekly - Autumn'!C181` | `<p class="small">` | **yes** — `.small` is 24/24 clean in the lesson decks |

**Would stay visible:**

`BUILD ASDAN`, `Community & Vocational`, `Autumn 2 · Week 1` (the same `.chip` class as the
tagged item), the `<h1>` lesson title, `Learning objective:`, all three success criteria,
the pupil task, the Lundy zone boxes, the route ladder, and every `data-ta1`/`data-ta2`
string — which is already invisible and needs no tagging.

**What would break if the mapping were wrong for this file.** Hiding `.chip` removes the
lane, unit and week — a pupil arriving mid-term loses the only on-screen statement of where
they are. Hiding `.hero` removes the lesson title and the learning objective, which is the
140-of-175 failure the patcher's own comments record. Hiding `.small` is the one safe move on
this slide, and it removes one of the three items.

## §7 · Cost, and the question it raises

### The four line items

| # | work | scope | estimate | what drives it |
|---|---|---|---:|---|
| 1 | **Author the hide-set markers** | Counted exactly: `Estate sequence` 26 files · `Exact SOW outcome` 25 · `AQA UAS` 14 (13 LAUNCH_ASDAN + 1 BUILD_ASDAN) · `Inherited mapping` 1. `Source:` needs none — `.small` already isolates it in all 28. | **66 marker sites across 40 files**; one patcher, half a day with the checks below | It is authoring, not patching. Each marker goes on a specific element and must be proven not to have taken a sibling with it. |
| 2 | **Render-check per family per lane** | The gate already exists — `s24-print-renders` renders 159 files in ~2 minutes. A screen-side equivalent is `i5_guidance_visibility.mjs`, which already walks every slide of all 159. | **~0 new tooling**; ~5 minutes per run | This line item is already paid. It was the expensive part of the previous estimate and is not any more. |
| 3 | **The `localStorage` question** | A straight fork, unchanged from N7 | **a ruling, not engineering** | PH-3 persists `mbm_guide_v1`; gate 4 requires 0 browser storage and every deck declares `storageKeys: []`. Either narrow gate 4 to that one key (matching 175 estate carriers) or ship the toggle without persistence. |
| 4 | **Regression** | 159 files, but only 37 touched | **low** | Additive, markered, strip-reversible in the estate's usual pattern; `s24` and the existing battery both gate it. |

### The question the numbers raise

**Line 1 buys very little.** Everything a toggle would hide, except those 61 sites, is
already invisible: 132 decks, 1188 guidance strings, four container families, **0 leaking to
the room**. What the toggle would actually remove from the wall is:

- `Estate sequence W9` — 26 BUILD_ASDAN files
- `Exact SOW outcome: …` — 25 BUILD_ASDAN files
- `Source: 'BUILD Weekly - Autumn'!B181 · …` — 28 BUILD_ASDAN files
- `AQA UAS …` — 13 LAUNCH_ASDAN files + 1 BUILD_ASDAN

41 files in total carry a visible staff string; 40 of them need a marker authored, and 28
of those are already covered for one of their three items by `.small`.

That is an audit trail on a title slide, not teacher instructions. It is worth asking
whether the right answer is a toggle at all, or one of:

- **do nothing** — the provenance is defensible on screen and is arguably a feature: a
  teacher can see which SoW cell the lesson came from without opening anything;
- **move it** — relocate the three BUILD_ASDAN strings into the already-hidden
  `#teacherDialog`, which is one edit per deck and needs no toggle, no storage, and no
  change to gate 4;
- **the full toggle** — line items 1–4 above.

**The middle option costs less than the toggle and delivers the same visible result.** It is
recorded here as an option, not a recommendation: choosing between them is a ruling, and
this order says map and price, not decide.

### What is NOT priced

The three Art packs. They are not in this repository, so their selectors were not counted
and their cost is not estimated. On the pattern of the nine, an Art pack would be one more
container family to identify and somewhere between zero and three visible string families —
but that is an extrapolation, and it is labelled as one.

## §8 · The tools this map was measured with

| tool | what it measures |
|---|---|
| `_next6/tools/i5_guidance_visibility.mjs` | walks every slide, reports which of a deck's own staff strings reach the visible surface, and which container family holds them |
| `_next6/tools/i5_overlap.mjs` | for every class in every deck, how many instances carry a staff string in their own text — the overlap risk |

Both are read-only and take a file list. Neither applies anything.
