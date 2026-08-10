# BUILD estate deploy + science close-out + Phase E — decision record

Branch `claude/estate-finish`, cut from `origin/main` @ **651a88ecf2f760c61fa2a221dc9b3351731e6f4e**.
Written before any file was changed; appended as work proceeded.

---

## D0 · Identity gate — 6/6, every marker derived

| # | marker | measured |
|---|---|---|
| 1 | `Science_Teesside/{Build,Grow,Launch}/v3_40min/` | all three present |
| 2 | `Baseline_Weeks/` at root | 8 HTML files |
| 3 | Art 8 · ASDAN 31 · DT 6 · BUILD humanities in `Build/Slideshows/` | `Art_Teesside/Build` = 8 `BUILD_ART_W*.html`; `BUILD_ASDAN` = **31 lessons** (39 HTML − 5 `START_HERE` − hub − `Resources_and_Tools` − `Scheme_of_Work`); `Build/Slideshows/` = 6 `BUILD_DT_W1..W6` **and** 8 `BUILD_HUM_W1..W8` |
| 4 | `Humanities_Teesside/` holds no lessons | confirmed: 3 SoW + 3 Printable Packs + `Pathway_Tracker.html` + the `Lundy_Humanities/` toolkit. **Zero lesson decks.** The BUILD humanities lessons are in `Build/Slideshows/`. |
| 5 | `resources.json` | parses; `Science · Teesside` = **63**, `Baseline` = **8** |
| 6 | `651a88e` ancestor | confirmed |

**ROLLBACK_SHA = `651a88ecf2f760c61fa2a221dc9b3351731e6f4e`** — `origin/main` has not moved since the
science run.

**§0.5 prior-run detection: nothing found.** No `BUILD_Estate_v3/`, no `_finish/`, no
`claude/estate-finish` branch (local or remote).

### D0a · AMBER — marker 4 is right about lessons, incomplete about contents

`Humanities_Teesside/` also holds the `Lundy_Humanities/` toolkit (27 files: standards, cards,
moderation tools, specimens). The load-bearing claim — *no humanities lessons live here* — holds
exactly. Recorded so a later pass reading "only SoW + Pathway Tracker" does not conclude the
toolkit is stray.

---

## D1 · Input gate — this is the REPAIRED build

95 files, 76 HTML. Both §0.6 assertions pass:

- `.proute{display:block}body[data-tier] .proute{display:none}` present in **exactly 63** files —
  Art 8 · ASDAN 31 · DT 6 · Humanities 8 · Science 10.
- `BUILD_COMPLETION_AUDIT.md` ends at a section headed
  **"Post-verification edits applied 2026-08-10 (Claude, pre-deployment)"** (line 47, the final
  heading in the file).

The count of route-bearing lesson files is **derived from the print-tier repair**, not from a
filename convention: 63 total, minus the 10 skipped science files, = **53 to install**.

---

## D2 · §0.8 — the skip is right, but its stated reason is not

§0.8 says the ten `Science/SCI_B_*` files are **byte-identical** to those already installed at
`Science_Teesside/Build/v3_40min/`, and skips them on that basis.

**Measured: 0 of 10 are byte-identical.** The zip's copies are the *original* TEST pack plus the
print-tier repair and nothing else — a two-line diff from the pristine input zip this programme
received earlier today:

```
- @media print{… .proute{display:none} …}
+ @media print{… .proute{display:block}body[data-tier] .proute{display:none} …}
- </script></body></html>
+ window.addEventListener('afterprint',()=>{delete document.body.dataset.tier});</script></body></html>
```

They are missing every repair the science run applied. Per file:

| repair | zip `Science/` | installed `v3_40min/` |
|---|---|---|
| Assessor Witness Statement (A2) | absent | present |
| arrival entry route, screen + print (A7) | absent | present |
| name + date line on print page 1 (A2) | absent | present |
| `aria-live` on feedback regions (A4) | absent | present |
| **W1–W2 baseline-week correction (A9)** | **absent — `Aut1·W2` in 3 files** | 0 files |
| **six healthy-eating links removed (§0.7)** | **absent — all six still present in 6 files** | 0 files |

**So the skip is not a tidy-up; it is necessary.** Installing the zip's science folder would
reintroduce, onto a live public site, the six food links removed hours ago under the BUILD
protection rule *and* the claim that Autumn 1 Week 2 taught science when it was a baseline week.

Skipped as instructed. **53 lessons installed, not 63.**

---

## D3 · AMBER — two Arts Award claims in the brief are contradicted by the repo

Both derived by reading the part tag out of all sixteen files (8 live, 8 v3).

**1. §0.6: "the live suite refused that double-count once already" — the reverse is true.**

| week | live `Art_Teesside/Build` | v3 |
|---|---|---|
| W1 | Explore Part A | Explore Part A |
| W2 | **Explore Part B** | **Explore Part B** |
| W3 | **Explore Parts A+C** | **Explore Part C** |
| W4–W6 | Explore Part C | Explore Part C |
| W7–W8 | Explore Part D | Explore Part D |

Live W3 is the **only** file in either suite carrying `Parts A+C`. The v3 repair *diverged from*
the live suite; it did not align to it. The Trinity reasoning stands on its own — Part C must be a
distinct activity, so it cannot double-count with Part A — and §1 keeps `Parts A + C` RED, so the
v3 tag stays `Part C`. **But the live file now disagrees with the v3 route, and that is an open
finding on a file this run is forbidden to edit.**

**2. §7 gate 6: "v3 W2 tags Part B only where live tags A+B" — not reproducible.** Both live and
v3 W2 tag `Explore Part B · Explore Artists' Work`. There is no `A+B` tag anywhere in either
suite. The Part B *evidence-artefact* question is still worth asking and is answered under gate 6;
the premise that the two suites differ at W2 is simply not the case.

---

## D4 · AMBER — a leftover inside the "repaired" zip

`Art_Teesside/manifest-v3.json` still records W3 as:

```json
"part": "Explore Parts A + C · Take Part + Create"
```

while the lesson itself now reads `Explore Part C · Create`. The W3 repair reached the page and
not its manifest, so a manifest audit and a page audit give different answers — the same class of
defect as BUILD science's `media: []`-versus-ten-links, corrected in the previous run. Fixed here
under Phase A and recorded, because §0.6 says the W3 tag is already repaired and, in the manifest,
it is not.

---

## D5 · Instruments must be validated against a known positive

Carried forward at §5 D6's instruction, because this failure mode has now cost more time across
this programme than any real defect. Every one of these produced a confident, wrong number:

1. **`font-weight` counted as `weight`.** A food-language census over raw HTML returned 296 hits;
   ~280 were the CSS property. A count over markup is not evidence about language. → scan visible
   text only.
2. **Hand-transcribed prompts, 25 of 32 wrong.** An A7 audit's per-lesson briefs carried prompts
   typed from memory rather than read from the files — BUILD W3B is about a robin, not "fish or
   crab"; BUILD W4A was reversed. The run was stopped and its findings discarded. → the audited
   text must be extracted by the thing doing the audit, never quoted to it.
3. **`\bslide\b` matches `slide-container`.** A reading-level pass swallowed every live slide into
   its own container and inflated live word counts ~60%, which inverted a live-vs-new comparison.
   → match whole class tokens.
4. **Non-greedy `(.*?)</div>` stops at the first *nested* close.** Tier-route extraction captured
   the task and silently dropped the scaffold. → depth-count.
5. **Characters counted as bytes**, and **prohibitions counted as uses** — both from the
   verification side of this programme.
6. **Print dialect written for one pack.** `.print-route` vs `.proute`, `data-print-tier` vs
   `data-tier`: an instrument written for GROW returns a confident zero on BUILD and LAUNCH.

The rule that follows, and the reason every scanner in `_sciv3/tools/` and `_finish/tools/` opens
with a known-positive check: **a negative from a text search is evidence about the text, never
about the runtime.**

---

## D6 · Standing rulings honoured, not re-litigated

- **No Arts Award hours threshold at any level.** TQT is guidance; Trinity sets no minimum-hours
  gate, and an hours gate invents a way to fail an AP pupil for attendance volatility.
- **No PEQ claim on any BUILD file.** BUILD banks ASDAN short courses + AQA UAS. 0/31 is correct.
- **No authored safety wording.** Where safety text is needed it is copied verbatim from a live
  file, or the task stops.
- **A1: the witness statement is not ported.** Recorded under Phase A with the consequence named.
- **A10.3 (science): both escape wordings stay** — "Not sure yet" (standard) and "Not ready yet"
  (SEMH). Ruled **deliberate**, not accidental, so no later pass harmonises it by reflex.
