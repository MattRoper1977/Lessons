# Science v3 install — decision record

Branch `claude/sci-v3-install-37iodu`. Started 2026-08-10.
Appended as work proceeded; nothing here was written retrospectively.

---

## D0 · Identity and rollback

- Repo confirmed `MattRoper1977/Lessons` (`origin` → https://github.com/MattRoper1977/Lessons).
- Identity gate **5/5**:
  1. `SCI_G_W3_Friction.html` 332,462 B · `SCI_B_W3_Backbones.html` 261,653 B · `SCI_L_W3_L1_Microscopy.html` 184,942 B — all present.
  2. `Science_Teesside/` holds `Build/`, `Grow/`, `Launch/`, 25 lesson HTML files.
  3. Root `resources.json` parses; 448 entries; 25 with `subject = "Science · Teesside"`.
  4. `biology/`, `chemistry/`, `2 Physics 10/` all present.
  5. `origin/main` resolves; `93d5700` confirmed ancestor.
- **ROLLBACK_SHA = `7a846cba9ee8c2cc128006d6be9b0244c3b7d893`**
- §0.5 prior-run detection: **nothing found**. No `v3_40min/` under Grow/Build/Launch, no `_sciv3/`,
  no `Baseline_Weeks/`, no branch `claude/sci-v3-install` or `claude/grow-sci-v3-install`
  (local or remote).

### D0a · AMBER — branch name differs from §0

§0 specifies branch `claude/sci-v3-install`. The session was provisioned on
`claude/sci-v3-install-37iodu` with an explicit instruction never to push elsewhere.
Work proceeds on the harness-assigned branch. Same base (`origin/main` @ ROLLBACK_SHA),
same content; only the suffix differs.

---

## D1 · Input gate (§0.6)

First run of this session had **three** zips: BUILD, LAUNCH, Baseline Weeks. GROW was absent.
Per §0.6 the run stopped and reported rather than proceeding on a subset. GROW was then supplied
and the gate re-run from scratch on all four.

**53/53 checksummed files verified byte-exact** — every sha256 first-16 matches §0.6.
GROW 16/16 · BUILD 16/16 · LAUNCH 21/21.
Baseline Weeks: **9 files** (8 HTML + `README.md`), no published checksums, enumerated by name and size.

**No filename aliases were received.** All four listed aliases were absent; every file arrived under
its canonical name.

### D1a · AMBER — §0.6's own arithmetic

§0.6 asks for `52/52 verified`. Its three checksum tables contain **53** rows
(16 + 16 + 21), not 52. 52 is the count of *HTML* files across all four packs
(GROW 13 + BUILD 13 + LAUNCH 18 + Baseline 8). Both numbers are reported explicitly
throughout so neither is mistaken for the other. Per §1, the measurement wins and the
disagreement is recorded as a finding.

---

## D2 · §0.7 — BUILD food links: DEFAULT TAKEN

No veto line was given. The default was applied.

**Removed (6):** the healthy-eating links in W5A, W5B, W6A, W6B, W7A, W7B.

| Lesson | URL removed |
|---|---|
| W5A `What a Body Needs` | `…/units/healthy-eating/lessons/types-of-food` |
| W5B `Nutrition Mission` | `…/units/healthy-eating/lessons/types-of-food` |
| W6A `Building a Balanced Plate` | `…/units/healthy-eating/lessons/nutrient-rich-meal-planning-non-statutory` |
| W6B `Balanced Plate Design Challenge` | `…/units/healthy-eating/lessons/nutrient-rich-meal-planning-non-statutory` |
| W7A `Animals Cannot Make Their Own Food` | `…/units/healthy-eating/lessons/making-or-finding-food` |
| W7B `Build a Food Source Chain` | `…/units/healthy-eating/lessons/making-or-finding-food` |

The "Optional current Oak resource" card is **kept** in all six, its text replaced by
*"No external food media in this lesson — see the BUILD protection rule."*
The protection rule is kept verbatim.

**Kept (4):** W3A/W3B `animals-without-bones`, W4A/W4B `muscles-for-movement` — skeleton/muscle unit,
not food, both confirmed at their exact URL by prior verification.

**Manifest corrected** either way: BUILD's `manifest-v3.json` declared `media: []` for all ten
lessons while ten Oak links existed in the pages. After this run the manifest states the four links
that remain and records the six as removed, so a manifest audit and a page audit agree.

---

## D3 · Placement (§3) — parallel routes

All three packs install as clearly-labelled parallel 40-minute routes under
`Science_Teesside/{Grow,Build,Launch}/v3_40min/`. The **twenty-five live lessons are untouched**
and remain the default. No veto line was given for any pathway.

---

## D4 · A2 — print-pack scope

Each new lesson prints 2 pages. The three live suites each carry the full 17 print-section ids.
Only the three additions specified in A2 were made: a date + name line at the head of print page 1,
an Assessor Witness Statement on print page 2, and (LAUNCH only, A8.1) the written closure line.

**The remaining twelve v5 print sections are deliberately absent, not overlooked.** Porting the v5
pack onto a different chassis would be a half-port, and A2 rules that out explicitly.

GROW's page-2 closure ("Adult is audience, not signatory. No initials or signature.") and BUILD's
adult-Audience wording differ by design and were **not** harmonised.

### D4a · Witness-statement wording provenance

A2 says copy the wording, do not invent it. The chassis — heading, awarding-body line,
"Records what was observed, and at which level of independence.", the Pupil/Lesson/Date table,
"Observed in this lesson", "Assessor comment", "Ring the tier the pupil actually worked at",
and the assessor name/role/signature line — is copied byte-for-byte from the matching live lesson.

The three lesson-specific "Observed in this lesson" statements are copied from the **live lesson for
the same SoW week in the same pathway**, not written fresh:

- LAUNCH is 1:1 — new `W3L1` takes live `SCI_L_W3_L1_Microscopy.html`, and so on for all fifteen.
- GROW and BUILD split one live week across an A and a B period, so both A and B take the same
  three observed statements from that week's live lesson. They describe the week's science, which
  is what the two periods jointly cover.

The `Lesson` row names the new route explicitly, e.g.
`Friction: Friend and Enemy — GROW Science · Week 3 (40-min route · Explore)`.

---

## D5 · A3 — links

**GROW, two unconfirmed slugs kept and flagged**, marked `data-link-unverified="true"`:

- `…/units/forces-including-simple-machines/lessons/how-gears-can-help-us` — W4A
- `…/units/earth-sun-and-moon/lessons/the-planets-in-our-solar-system-non-statutory` — W6A

Both lessons appear in Oak's unit listings; only the slugs are unproven, and Oak commonly 403s
agent fetch tools. Neither was deleted and no replacement was guessed. **30-second check for Matt.**

**LAUNCH carries zero external URLs** across all 20 files. Verified on arrival and re-asserted after
every edit.

---

## D6 · A8.2 — the verified osmosis clip, recorded as a named consequence

Live `Science_Teesside/Launch/SCI_L_W5_L2_OsmosisCP.html` carries the Oak osmosis core-practical
link that **Matt personally cleared**. It is the only externally-verified clip in the science estate.

The new LAUNCH pack has zero external links. Under the parallel-route ruling nothing is lost,
because the live file stays.

> **Named consequence.** A future `Retire the live lessons in LAUNCH — v3 route is the only route
> there` discards that clip. It is not carried into the new pack, because it was cleared against
> that lesson, not this one. Anyone acting on the LAUNCH retirement veto should be told this first.

---

## D7 · A9 — the baseline weeks

Autumn 1 W1 and W2 are **baseline weeks; no science was taught in them**. All three packs assumed
otherwise. Derived count of the literal string `Aut1·W2`: **10 occurrences across 7 files**, plus one
differently-worded curriculum block in `launch/SOW_AND_POLICY_ALIGNMENT.md` — an eighth file.
That matches §0.7's "ten occurrences across eight files" exactly.

**The hard constraint was honoured: no claim about what the baseline covered appears anywhere.**
The baseline runs on PythonAnywhere and is not in this repo. Nothing was created, linked or implied
inside Lessons that would stand in for it.

Presupposition classification and the full before/after prompt table are in `A9_PROMPTS.md`
in this directory.

---

## D8 · A10 — Baseline Weeks pack

Four repairs and no others, per A10.1–A10.4. See `BASELINE_WEEKS.md` in this directory for the
detail, the naming-divergence question and the AMBER list.

---

## D9 · A6 — reading load, GROW Supported route only

Not applied to BUILD (its routes already work; its slides are the problem — Phase E).
Not applied to LAUNCH (its routes already read 1.4–2.6 grades **easier** than live at every tier;
editing them would undo an improvement). Per-file before/after in `A6_READING.md`.

---

## D10 · Deferred, recorded, not built

Phase E items 1, 2, 2b, and deferred items 3–8 from §8 were **not** started. No trigger was given.

---

## D11 · Findings where the measurement contradicted the brief (§1 AMBER)

Recorded in the order they were found. In every case the measurement was re-checked against a
known positive before it was believed.

1. **§0.6's checksum arithmetic.** The three tables hold **53** rows, not 52. 52 is the count of
   *HTML* files across all four packs. Both numbers reported separately throughout. (D1a)
2. **BUILD's manifest does not declare `media: []`** — it has **no `media` key at all**. §0.7
   describes the symptom correctly and the cause incorrectly. Same audit consequence.
3. **GROW has two more "from last lesson" prompts than the A9 table lists**, plus a said-aloud
   staff opener and a Lundy thread that both assume a previous lesson. Found by reading, not by
   grepping the two strings the table names. All corrected. (`A9_PROMPTS.md`)
4. **A4's GROW input list is right; the raw count is misleading.** 17 `<input>` elements exist,
   but only the 9 W5B table cells and the 2 lever sliders lack an accessible name — the rest are
   wrapped in `<label>`. LAUNCH's 11 inputs are all wrapped and needed nothing.
5. **A6's premise does not reproduce.** On the universe that reproduces the 8.24 house standard
   (GROW live Supported measures 8.47), the new GROW Supported route already sits **below** the
   target before any edit. A6 was therefore applied to the fragments that are genuinely hard in
   their own right rather than to files that already pass. (`A6_READING.md`)
6. **LAUNCH's slide word count is the other way round.** §5 gate 10 and §8 item 2b both rest on
   LAUNCH's new slides carrying 30% *fewer* words than live. Measured: **39% more**
   (1,169 vs 840 per lesson). This weakens 2b's "harder but shorter" defence. Not acted on —
   Phase E is not authorised — but it changes the evidence 2b would be decided from.
   (`READING_LEVELS.md`)
7. **A second false-deficit case in the Baseline pack**, not named in A10.2, firing on every
   sitting rather than only on an all-uncertain one. Fixed and flagged. (`BASELINE_WEEKS.md`)

## D12 · Two instrument failures of my own, and what they cost

Recorded because the brief is right that a negative from a text search is evidence about the text,
never about the runtime — and because both would have produced confident wrong numbers.

1. `\bslide\b` matches `slide-container`. The first reading-level run swallowed every live slide
   into its own container and inflated live word counts by ~60%, which would have inverted the
   live-vs-new comparison. Fixed by matching whole class tokens.
2. The first food-language census scanned raw HTML and returned **296 hits**, of which ~280 were
   the CSS property `font-weight`. A count over markup is not evidence about language. Fixed by
   scanning visible text only; the honest count is 26, and the binary prohibition/use
   classification needed a third class (an animal's *natural diet* is biology, not personal-diet
   language).

Neither reached a commit. Both are the reason every scanner in `_sciv3/tools/` is validated
against a known positive first.

## D13 · Sitemap

**Not maintained in this repository.** There is no `sitemap.xml` and no `robots.txt` here, and the
repo's own instrument documentation (`LundyLoop/tools/sitemap_audit.py`, LL-INST-07) states that
the sitemap lives in the SITE repo and asserts things about this one. Per §4, nothing was done.

## D14 · AMBER — a prior run's gate now fails by design

`_passsci1/hub_chip_gate.js` hard-asserts `Science · Teesside` at 25/25 and exits non-zero
otherwise. The chip legitimately moved to 63, so that instrument now fails. It is a prior run's
sealed record and was **not** edited. The current equivalent is `_sciv3/tools/chip_gate.mjs`,
which drives the real `index.html` in a browser rather than replicating its filter chains.

## D15 · Phase E and §8 — not started

No trigger was given for any of: BUILD slide reading load, GROW slide reading load, LAUNCH slide
reading load, Progress Schools-branded variants, the evidence-window promotion, the prompt-ladder
reconciliation, the 5-vs-10 ruling, or the pathway entry bands. Nothing was built for any of them.

---

## D16 · A7, second half — the retrieval boxes

A7's gate has two halves. The first (line present on 35 arrival slides and 35 print page 1s)
passed on the first run. The second — *"the retrieval box must answer that lesson's Supported
arrival prompt by reading alone… where a box falls short, add the missing fact to the box"* —
was audited per lesson and **fifteen boxes were extended**. Seventeen were left alone.

Full table, including why each of the seventeen is correct as it stands: `A7_RETRIEVAL_BOXES.md`.

**Three would have been actively wrong to "fix".** BUILD W3B, BUILD W7A and LAUNCH W4L1 are
elicitations into the lesson's own new concept; putting the answer in the retrieval box would
pre-teach, which every one of these lessons forbids on the same slide. A cruder instrument would
have "repaired" all three.

**A first audit was discarded.** Its per-lesson briefs carried hand-transcribed prompts and 25 of
32 were wrong — BUILD W3B is about a robin, not "fish or crab"; BUILD W4A was reversed. Findings
built on wrong inputs are worthless even where they happen to look right, so the run was stopped
and rebuilt to carry no lesson text at all: every agent extracts the box and the prompt from the
file itself, and reports both back so the extraction can be checked.

Each addition was then adversarially verified against two failure modes — not actually taught in
the predecessor, and would pre-teach today's concept. All fifteen confirmed as genuine retrieval;
five tightened by the verifier, and the tightened wording is what shipped.

The gate for W4–W7 arrival retrievals changed shape accordingly: it no longer asserts
byte-identity, because A7 deliberately extends some boxes. It now asserts the original text
survives **byte-for-byte as a prefix** and that the only addition is one of the fifteen verified
facts. Anything else is still drift and still fails.
