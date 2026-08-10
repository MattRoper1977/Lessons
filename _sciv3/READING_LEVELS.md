# Gate 10 — reading levels across all six sets, one instrument

`_sciv3/tools/measure.py` (+ `lib_text.py`). Run it yourself:

```sh
python3 _sciv3/tools/measure.py /path/to/extracted/zips     # pre-repair "new" columns
python3 _sciv3/tools/measure.py /tmp/final_measure          # post-repair "new" columns
```

## The universes, named — a count is meaningless until its universe is stated

- **Slides** — the text inside every on-screen slide, print pack excluded. The new packs use
  `<section class="slide" data-type=…>`; the live suites use `<div class="slide" data-title=…>`.
  Both are handled; checking only one produces a confident zero on the other set.
- **Route, universe A** — the whole printed tier route: task **and** scaffold.
  New packs: `.print-route <tier>` / `.proute <tier>`. Live: `#print-scaffold-<tier>` +
  `#print-worksheet-<tier>`. This is the universe that reproduces the document's house standard
  (it measures GROW-live Supported at **8.47** against the document's **8.24**).
- **Route, universe B** — the task line only, the ~17–32 word fragment.
- Flesch–Kincaid, with emoji, tier glyphs (◆ ▲ ★) and rule characters excluded from the word count.

## Instrument failures found and fixed before any figure below was believed

1. `\bslide\b` also matches `slide-container`, so the first run swallowed every live slide into
   its own container and inflated live word counts by ~60%.
2. `slide` and `slide active` were matched by two separate passes, double-counting the title slide.
3. A non-greedy `(.*?)</div>` stops at the **first nested** `</div>`, so route extraction captured
   the task and silently dropped the scaffold. Replaced with depth counting.

## The table (post-repair "new" rows)

| set | n | slides FK | slides words/lesson | Supported | Standard | Stretch |
|---|---|---|---|---|---|---|
| GROW live | 5 | 5.61 | 803 | 8.47 | 9.45 | 10.65 |
| GROW new | 10 | 8.21 | 1300 | **4.74** | 8.44 | 10.39 |
| BUILD live | 5 | 4.30 | 728 | 6.70 | 8.86 | 9.13 |
| BUILD new | 10 | 8.42 | 1055 | 5.43 | 5.81 | 9.53 |
| LAUNCH live | 15 | 7.73 | 840 | 8.56 | 9.04 | 9.38 |
| LAUNCH new | 15 | 11.83 | 1169 | 11.09 | 11.07 | 14.30 |

Route figures rest on 10–117 word fragments and are noisy. **Direction, not decimals.**

## Where this instrument disagrees with the master prompt — stated plainly

The prompt's own §1 says the measurement wins and the disagreement is a finding. Three findings:

**1. Slide FK — agrees on direction and roughly on size.** The prompt has GROW live 6.17 → new
9.35 (+3.18); this instrument has 5.61 → 8.21 (+2.60). BUILD +4.37 vs +4.12. LAUNCH +3.76 vs
+4.10. The absolute values sit ~0.5–1.1 grades lower throughout, consistent with a different
syllable heuristic. **Every claim about the slides that Phase E rests on survives.**

**2. LAUNCH slide word count — the prompt has this backwards.** It states, twice, that LAUNCH's
new slides carry **30% FEWER** words than live (1,304 vs 1,877) and builds §8 item 2b's
"leave it and judge it in a room" recommendation on that density argument. Measured here, LAUNCH
new carries **1,169 words per lesson against live's 840 — 39% MORE, not 30% fewer.**

Live LAUNCH lessons are big files (≈185 KB) but most of that is SVG and a 17-section print pack,
not on-screen slide text. Every live suite lands in the same 730–840 band on this instrument, and
the three new packs in the 1,055–1,300 band.

**This weakens §8 item 2b.** The recommendation to leave LAUNCH's slides alone rests on "harder but
shorter". If the pack is harder *and* longer, LAUNCH's slides look like the same finding as GROW's
and BUILD's, not a special case. **Not acted on — Phase E is not authorised — but it changes the
evidence 2b would be decided from.**

**3. Route FK — the prompt's "new" figures are not reproducible here.** GROW new Supported is
given as 9.26; universe A measures 5.96 pre-repair and 4.74 post-repair, and universe B measures
7.23. LAUNCH new Supported is given as 10.17; measured 11.09. See `A6_READING.md` for what that
did to A6's scope, and what was done about it.

## Per-slide-type breakdown, so Phase E is scoped from evidence

FK / mean words per lesson.

| slide | GROW live | GROW new | BUILD live | BUILD new | LAUNCH live | LAUNCH new |
|---|---|---|---|---|---|---|
| title | 6.09 / 100 | 9.19 / 165 | 5.65 / 194 | 9.24 / 92 | 9.78 / 226 | 12.49 / 111 |
| arrival | 3.68 / 52 | 8.65 / 135 | 4.06 / 47 | 7.72 / 104 | 7.14 / 53 | 11.95 / 105 |
| starter | — | 7.03 / 147 | — | 6.72 / 131 | — | 12.38 / 126 |
| I Do | 5.38 / 272 | 8.70 / 171 | 3.45 / 173 | 8.28 / 157 | 7.16 / 296 | 12.02 / 168 |
| We Do | 7.06 / 101 | 7.52 / 184 | 2.92 / 134 | 9.34 / 157 | 8.33 / 122 | 12.80 / 211 |
| independent | 7.13 / 87 | 9.60 / 346 | 6.01 / 83 | **9.97 / 254** | 8.41 / 74 | **13.40 / 228** |
| exit | 6.66 / 67 | 6.84 / 135 | 7.03 / 62 | 7.32 / 142 | 9.44 / 75 | 11.14 / 158 |

(GROW/BUILD/LAUNCH new figures are post-repair. The live chassis has no separate `starter` slide;
its `glance` and `lundy` slides have no new-pack equivalent and are folded into the totals.)

**Where Phase E's work actually is.** In both BUILD and LAUNCH the Independent slide is the hardest
*and* the longest — BUILD 9.97 on 254 words against a live 6.01 on 83; LAUNCH 13.40 on 228 against
8.41 on 74. The exit slide is the closest to live in both. A Phase E scoped to the Independent and
We Do slides would move most of the gap for a fraction of the rewriting.
