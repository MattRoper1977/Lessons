# Class of Ashes: Zero Period — PATCHED AND PARKED

**This game is not being placed, and nothing in this branch places it.**
**C0's scope fence is the position, not a holding pattern.**

The deciding question was never whether the content is too violent. By the
standard of what fifteen-year-olds already play it plainly is not, and the
enemies are an insectoid Brood and a construct boss rather than people — a
genuine mitigator, not pretended away.

The question is: should a teacher publish, under his own name, on the site his
SEMH pupils reach through lesson links, a game set in a school under attack with
a mode called **PROTOCOL LOCKDOWN**? Lockdown is not a neutral word in a school
building. It names a drill those pupils have stood through, and for some of them
it will name more than a drill. The cost of parking is nothing; the cost of
publishing and being asked to explain it is disproportionate to any benefit, and
unpublishing is much harder than not publishing.

**The technical work proceeds regardless.** A parked artefact with a known
boot-kill is still a liability, and these fixes are the reference material for
the next pack that repeats them.

**If it is ever wanted on the shelf, the route is a re-skin, not a debate about
content.** Strip the school framing — PROTOCOL LOCKDOWN, the Academy, the Dean's
Exam, the Arch-Provost, the Academic Transcript — and it becomes an ordinary
tactical combat game that publishes on ordinary merits. That is a content
commission with its own budget, not a patch, and it does not belong in this
close. Swap line: `COA RESKIN`.

So: no route, no manifest entry, no card, hue, genre, feel tag, take, `TOP` or
`hero`, and no link from anywhere. The `C0` gate asserts that, by looking for any
mention of this game in the canonical shelf record, both audience pages and the
curation renderer — and it reports **INCONCLUSIVE**, never a pass, if it cannot
read one of them.

```sh
tools/coa/run.sh          # build staging/, run every gate
tools/coa/run.sh --drops  # also drop each fix and check a gate notices
```

## Provenance — worth stating plainly

The prototype at v0.1.0 has **0 `localStorage` calls, 0 normalizers and 0
`__COA_QA`**. Every defect fixed below was introduced by the PRO release's own
*"Reliability and hardening"* work.

## What changed

| id | what |
|---|---|
| Y1a/b | shape guards inside both normalizers |
| Y2 | the autostart block removed |
| Y3 | `window.__COA_QA` removed in full |
| Y4a–d | subtitle clearance derived from the drawn HUD |
| Y5d | `user-scalable=no` and `maximum-scale=1` stripped from the viewport |
| Y5e1 | `prefers-reduced-motion` seeds the in-game setting |

### C1 — the null-parse boot kill

Storing the literal string `null` under the settings or the profile key killed
boot. `safeParse` returns `JSON.parse('null')` → `null`, which is **not
`undefined`**, so the `raw={}` default parameter never fired and the first
property read threw.

The scope is exactly two keys, measured rather than assumed —
`C1-scope` reports `settings=BREAKS · profile=BREAKS · activeRun=fine`.

The guard goes **inside** both normalizers, not at the call sites, so every
future caller inherits it, and it guards on **shape**, not on `undefined`, which
is the whole lesson of the defect.

**Why the release report claimed a pass:** its own `qa/TEST_SUMMARY.json` records
the injected settings as `{"difficulty":"nightmare","aimAssist":"500",...}` — a
well-formed **object** with bad **values**. The top-level **type** was never
varied. `C1` varies it: 7 shapes × 3 keys = 21 cases, and release fails 2 of 21.

### C2 — unvalidated URL parameters

`?autostart=1&overclock=bogus` threw at boot; `qs.get()` values went straight
into `startRun` with no check against MODES / CLASSES / OVERCLOCKS. The hardening
was asymmetric — localStorage defended, URL input trusted — and the prototype
does not have this at all.

Repair (1), the preferred one: the block existed only to serve the QA harness
that C3 removes, so it went with it. **All five bad parameter sets break the
release build; none breaks the patched one.**

### C3 — the ungated QA hook

`window.__COA_QA` shipped live with `grant`, `setPlayer`, `hurt`, `teleport`,
`spawn`, `strike`, `setStats` and more. Anyone with a console rewrote the run
**and the persistent Academic Transcript** — a pupil-visible record of grades,
best wave and commendation seals. Scrap Core v10 removed its hooks outright;
this matches that.

The cost was paid rather than dodged: **every gate here drives the game through
the DOM and real events.** No hook was kept "just for the test". `C3c` walks
mode → chassis → overclock → Deploy through the real UI and asserts the game
canvas is *painting*, for each of the three modes and each of the four chassis
(4 configurations covering the union, not the 12-case cross product — stated
rather than implied).

### C4 — subtitle / HUD collision

`#subtitles` sat at `bottom:134px`, dropping to `82px` under
`@media(max-height:560px)`. The drawn HUD's bottom-left vitals panel occupies
`vh+16` from the bottom, and `vh` is **106** in compact mode (`CW<980`). At
915×412 the page is compact *and* short, so the subtitle panel landed at 82px
inside a 122px band — on top of the ammo/heat/scrap readout.

The clearance is now **derived from the same expression the draw path uses**, not
guessed: `setSubtitleClearance(vh+16)` writes `--hud-bottom`, and the media-query
override is gone. Measured at 915×412, 844×390, 740×360 and 1280×600, with
`largeHud` off and on and a longest-string subtitle forced: release overlaps in
**6 of 8**, the patched build in **0 of 8**.

The doubled "MUNITIONS SIPHON" text in their own capture was deliberately not
chased — it is a compositing artefact of their DOM-plus-framebuffer method, not
a game defect.

## The Academic Transcript — ruled

**No persistent graded record attached to a pupil's name.** The Transcript grades
DISTINCTION / MERIT / PASS and keeps a persistent record; the estate has already
settled this in its own governance copy — *"not grades, diagnoses"*, *"do not
turn action counts into ability labels"* — and holding that line in the science
instruments while dropping it the moment the same pupils meet a game would be
incoherent. For an SEMH cohort a stored grade beside their name is a shame
trigger, and a stored one they cannot escape by playing better.

**Record what was done and observed, not what it was worth.** Not implemented
here: the game is parked, so the ruling is recorded against it rather than
enacted, and it lands with the re-skin if that is ever commissioned. Swap line:
`GRADED ARTEFACTS = KEEP`.

## Not done, and why

- **C5.1–C5.3, C5.6 (splash, way home, title, `og:`)** — not in this pass. They
  need the house conventions derived from the live shelf, and that census is
  Target A's work; landing a hand-written approximation of a generated control
  is exactly what the estate's inline-exit ledger exists to prevent.
- **C5.7 storage keys — NOT renamed, deliberately.** The order says stop and ask
  rather than default. `COA-TRANSCRIPT-1` is an export format possibly in the
  wild; a rename must keep import of existing files working unchanged and
  migrate all three keys atomically. That was not proven here, so the keys stand.
- **`canonical`** — omitted on purpose while C0 stands, rather than inventing a
  URL that does not exist.
- Mode names and in-game copy are untouched. **Protocol Lockdown is Matt's
  decision, not a repair.**
