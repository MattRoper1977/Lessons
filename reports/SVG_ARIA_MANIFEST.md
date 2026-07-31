# SVG accessibility manifest

Inventory of every `<svg>` in the Lessons estate that carries **neither** `aria-hidden="true"`
**nor** a label (`aria-label`, `aria-labelledby`, or `role="img"`). Screen readers currently
announce these as unnamed graphics.

**Nothing has been changed.** This file is a proposal for Matt to rule on. No `aria-hidden`
was added anywhere and no descriptions were written — a description of a teaching diagram is
lesson content, and content is Matt's to approve.

## How to read it

| verdict | meaning | suggested fix (not applied) |
|---|---|---|
| `decorative` | the graphic repeats meaning already present in nearby words, or is a small mark | `aria-hidden="true"` |
| `teaching` | the graphic carries information not available in text | `role="img"` + an `aria-label` **written by Matt** |
| `NEEDS LABEL` | the graphic is the only content of a control, so the control is currently unnamed | an accessible name on the control |
| `review` | evidence was not decisive — needs a human look | — |

Every row is classified from that element's own evidence — canvas size, how many `<text>`
labels it contains, how many shapes, and what it sits inside. No file, folder or filename
bucket was used to decide any verdict.

## Totals

- `<svg>` elements across the estate: **801**
- of those, unlabelled: **385** in **132** files
- decorative: **174**
- teaching: **109**
- review: **102**

**No unnamed controls were found.** Every icon-only button and link in the estate already
carries its own `aria-label` or `title`, so no control is announced as a bare graphic —
those inner icons are listed as `decorative` because the control around them is already named.

## Files

### `2 Physics 10/Consolidation_Electricity_Review-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="200" height="160" viewBox="0 0 200 170"` | teaching | high | 5 <text> labels on a 200x170 canvas |
| 2 | `class="water-svg" viewBox="0 0 300 150"` | teaching | high | 4 <text> labels on a 300x150 canvas |
| 3 | `id="series-svg" width="300" height="150" viewBox="0 0 300 150"` | teaching | high | 3 <text> labels on a 300x150 canvas |
| 4 | `width="180" height="150" viewBox="0 0 180 150"` | teaching | high | 4 <text> labels on a 180x150 canvas |

### `2 Physics 10/L1_Circuits_Symbols_Series_Parallel-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 4 shapes |
| 2 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 5 shapes |
| 3 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 5 shapes |
| 4 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 3 shapes |
| 5 | `width="50" height="24"` | decorative | high | 50x24 glyph, no text, 4 shapes |
| 6 | `width="50" height="24"` | decorative | high | 50x24 glyph, no text, 6 shapes |
| 7 | `width="50" height="24"` | decorative | high | 50x24 glyph, no text, 5 shapes |
| 8 | `width="50" height="24"` | decorative | high | 50x24 glyph, no text, 5 shapes |
| 9 | `width="50" height="24"` | decorative | high | 50x24 glyph, no text, 3 shapes |
| 10 | `width="50" height="24"` | review | low | 50x24 (width/height), 3 shapes, 1 text — not clear-cut |
| 11 | `width="50" height="24"` | review | low | 50x24 (width/height), 3 shapes, 1 text — not clear-cut |
| 12 | `width="50" height="24"` | decorative | high | 50x24 glyph, no text, 1 shapes |
| 13 | `width="300" height="120" viewBox="0 0 300 120"` | teaching | high | 4 <text> labels on a 300x120 canvas |
| 14 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 4 shapes |
| 15 | `width="60" height="30"` | review | low | 60x30 (width/height), 3 shapes, 1 text — not clear-cut |
| 16 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 5 shapes |
| 17 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 3 shapes |
| 18 | `width="60" height="30"` | decorative | medium | small 60x30 mark, no text, 5 shapes |
| 19 | `width="60" height="30"` | review | low | 60x30 (width/height), 3 shapes, 1 text — not clear-cut |
| 20 | `width="280" height="100" viewBox="0 0 280 100"` | teaching | medium | 1 <text> label on a 280x100 canvas |
| 21 | `width="280" height="140" viewBox="0 0 280 140"` | teaching | high | 5 <text> labels on a 280x140 canvas |
| 22 | `width="320" height="180" viewBox="0 0 320 180"` | teaching | high | 4 <text> labels on a 320x180 canvas |
| 23 | `width="320" height="180" viewBox="0 0 320 180"` | teaching | high | 5 <text> labels on a 320x180 canvas |
| 24 | `width="300" height="200" viewBox="0 0 300 200"` | teaching | high | 9 <text> labels on a 300x200 canvas |

### `2 Physics 10/L2_Voltage_Current_Resistance-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="340" height="180" viewBox="0 0 340 180"` | teaching | high | 4 <text> labels on a 340x180 canvas |
| 2 | `width="260" height="200" viewBox="0 0 260 200"` | teaching | high | 4 <text> labels on a 260x200 canvas |
| 3 | `width="240" height="210" viewBox="0 0 240 210"` | teaching | high | 4 <text> labels on a 240x210 canvas |
| 4 | `width="320" height="160" viewBox="0 0 320 160"` | teaching | high | 6 <text> labels on a 320x160 canvas |
| 5 | `width="300" height="220" viewBox="0 0 300 220"` | teaching | high | 6 <text> labels on a 300x220 canvas |
| 6 | `width="180" height="150" viewBox="0 0 180 150"` | teaching | high | 4 <text> labels on a 180x150 canvas |

### `2 Physics 10/L2_Voltage_Current_Resistance.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="340" height="180" viewBox="0 0 340 180"` | teaching | high | 4 <text> labels on a 340x180 canvas |
| 2 | `width="260" height="200" viewBox="0 0 260 200"` | teaching | high | 4 <text> labels on a 260x200 canvas |
| 3 | `width="240" height="210" viewBox="0 0 240 210"` | teaching | high | 4 <text> labels on a 240x210 canvas |
| 4 | `width="320" height="160" viewBox="0 0 320 160"` | teaching | high | 6 <text> labels on a 320x160 canvas |
| 5 | `width="300" height="220" viewBox="0 0 300 220"` | teaching | high | 6 <text> labels on a 300x220 canvas |
| 6 | `width="180" height="150" viewBox="0 0 180 150"` | teaching | high | 4 <text> labels on a 180x150 canvas |

### `2 Physics 10/L2b_Ohms_Law_PhET_Practical-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="220" height="180" viewBox="0 0 240 200"` | teaching | high | 4 <text> labels on a 240x200 canvas |
| 2 | `width="220" height="180" viewBox="0 0 240 200"` | teaching | high | 4 <text> labels on a 240x200 canvas |

### `2 Physics 10/L2b_Ohms_Law_PhET_Practical_1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="220" height="180" viewBox="0 0 240 200"` | teaching | high | 4 <text> labels on a 240x200 canvas |

### `2 Physics 10/L2c_Ohms_Law_PhET_Take2 (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="220" height="180" viewBox="0 0 240 200"` | teaching | high | 4 <text> labels on a 240x200 canvas |
| 2 | `width="180" height="150" viewBox="0 0 240 200"` | teaching | high | 4 <text> labels on a 240x200 canvas |

### `2 Physics 10/L3_Ohms_Law_Action.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="vir-triangle-svg" viewBox="0 0 240 220"` | teaching | high | 4 <text> labels on a 240x220 canvas |
| 2 | `width="280" height="130" viewBox="0 0 280 130"` | teaching | high | 4 <text> labels on a 280x130 canvas |

### `2 Physics 10/L4_Electron_Flow_Series_Calculations.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="320" height="190" viewBox="0 0 320 190"` | teaching | high | 8 <text> labels on a 320x190 canvas |
| 2 | `width="300" height="160" viewBox="0 0 300 160"` | teaching | high | 6 <text> labels on a 300x160 canvas |
| 3 | `width="180" height="150" viewBox="0 0 180 150"` | teaching | high | 4 <text> labels on a 180x150 canvas |

### `2 Physics 10/L4_Wave_Properties_Definitions-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="280" height="200" viewBox="0 0 280 200"` | teaching | high | 4 <text> labels on a 280x200 canvas |
| 2 | `width="340" height="200" viewBox="0 0 340 200"` | teaching | high | 5 <text> labels on a 340x200 canvas |
| 3 | `width="300" height="160" viewBox="0 0 300 160"` | teaching | high | 3 <text> labels on a 300x160 canvas |
| 4 | `width="320" height="160" viewBox="0 0 320 160"` | teaching | high | 2 <text> labels on a 320x160 canvas |

### `2 Physics 10/L4a_Electron_Flow_in_Metals.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="320" height="190" viewBox="0 0 320 190"` | teaching | high | 8 <text> labels on a 320x190 canvas |

### `2 Physics 10/L5_Wave_Speed_Equation-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="260" height="240" viewBox="0 0 260 240"` | teaching | high | 4 <text> labels on a 260x240 canvas |
| 2 | `width="240" height="210" viewBox="0 0 240 210"` | teaching | high | 4 <text> labels on a 240x210 canvas |
| 3 | `width="180" height="150" viewBox="0 0 180 150"` | teaching | high | 4 <text> labels on a 180x150 canvas |

### `2 Physics 10/L6_Waves_Context_Reflection_Refraction-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="280" height="140" viewBox="0 0 280 140"` | teaching | high | 6 <text> labels on a 280x140 canvas |
| 2 | `width="280" height="140" viewBox="0 0 280 140"` | teaching | high | 6 <text> labels on a 280x140 canvas |
| 3 | `width="180" height="150" viewBox="0 0 180 150"` | teaching | high | 4 <text> labels on a 180x150 canvas |

### `2 Physics 10/Waves/L4b_Frequency_Period.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="320" height="160" viewBox="0 0 320 160"` | teaching | high | 2 <text> labels on a 320x160 canvas |

### `2 Physics 10/Waves/L4c_Energy_Transfer.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="280" height="200" viewBox="0 0 280 200"` | teaching | high | 4 <text> labels on a 280x200 canvas |
| 2 | `width="300" height="160" viewBox="0 0 300 160"` | teaching | high | 3 <text> labels on a 300x160 canvas |

### `5 Intervention 10/InterventionA_Battle_Arena (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 2 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 3 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 4 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |

### `5 Intervention 10/Intervention_Digestion_Absorption_Gut_Reaction.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 400 280"` | teaching | medium | 1 <text> label on a 400x280 canvas |

### `5 Intervention 10/Lesson_VIR_Intervention.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 230 200"` | teaching | high | 3 <text> labels on a 230x200 canvas |
| 2 | `viewBox="0 0 320 150"` | teaching | high | 3 <text> labels on a 320x150 canvas |
| 3 | `viewBox="0 0 320 150"` | teaching | high | 3 <text> labels on a 320x150 canvas |
| 4 | `viewBox="0 0 320 140"` | teaching | high | 3 <text> labels on a 320x140 canvas |
| 5 | `viewBox="0 0 340 160"` | teaching | high | 4 <text> labels on a 340x160 canvas |

### `5 Intervention 10/Lesson_VIR_Pupil_App.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 380 170"` | teaching | high | 5 <text> labels on a 380x170 canvas |
| 2 | `viewBox="0 0 230 200"` | teaching | high | 3 <text> labels on a 230x200 canvas |
| 3 | `viewBox="0 0 320 120"` | teaching | high | 3 <text> labels on a 320x120 canvas |
| 4 | `viewBox="0 0 340 150"` | teaching | high | 4 <text> labels on a 340x150 canvas |
| 5 | `viewBox="0 0 340 120"` | teaching | high | 3 <text> labels on a 340x120 canvas |
| 6 | `viewBox="0 0 340 130"` | teaching | high | 4 <text> labels on a 340x130 canvas |
| 7 | `viewBox="0 0 340 150"` | teaching | medium | 1 <text> label on a 340x150 canvas |

### `5_6 Local Choice/L18_Risk_Sampling.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="bank-scene" viewBox="0 0 680 200"` | teaching | high | 6 <text> labels on a 680x200 canvas |
| 2 | `viewBox="0 0 280 70"` | review | low | 280x70 (viewBox), 7 shapes, 2 text, beside: "picked by chance / Best for: removing bias. " — not clear-cut |
| 3 | `viewBox="0 0 280 70"` | review | low | 280x70 (viewBox), 7 shapes, 2 text, beside: "same gap each time / Best for: showing chang" — not clear-cut |
| 4 | `viewBox="0 0 280 70"` | review | low | 280x70 (viewBox), 9 shapes, 3 text, beside: "split into zones / Best for: very different " — not clear-cut |

### `5_6 Local Choice/L19_Fieldwork_Day.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="trend-mini" viewBox="0 0 520 130"` | teaching | high | 8 <text> labels on a 520x130 canvas |

### `5_6 Local Choice/Opening_Night.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="w-5 h-5 mr-2" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Print All Slides" — the control is already named |
| 2 | `class="w-5 h-5 mr-2" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Print All Worksheets" — the control is already named |
| 3 | `class="w-6 h-6 text-amber-500" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 4 | `class="w-8 h-8 text-rose-500" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 5 | `class="w-6 h-6 text-amber-600" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 6 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 7 | `class="w-8 h-8 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 8 | `class="svg-icon" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 9 | `class="svg-icon" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 10 | `class="svg-icon" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 11 | `class="svg-icon" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 12 | `class="svg-icon" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 13 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 14 | `class="w-8 h-8 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 15 | `class="w-8 h-8 text-slate-400" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 16 | `class="w-8 h-8 text-rose-400" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 17 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 18 | `class="w-8 h-8 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 19 | `class="w-8 h-8 text-slate-400" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 20 | `class="w-8 h-8 text-amber-400" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 21 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 22 | `class="w-6 h-6 text-green-600" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 23 | `class="w-6 h-6 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 24 | `class="w-5 h-5" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Previous" — the control is already named |
| 25 | `class="w-5 h-5" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Next" — the control is already named |

### `5_6 Local Choice/Rivers/L1a_Tees_Source_to_Sea.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 900 120"` | teaching | high | 5 <text> labels on a 900x120 canvas |

### `5_6 Local Choice/Rivers/L1b_Your_River_Your_Home.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 900 200"` | teaching | high | 3 <text> labels on a 900x200 canvas |

### `5_6 Local Choice/Rivers/L1c_Reading_the_River.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 900 120"` | teaching | high | 5 <text> labels on a 900x120 canvas |

### `5_6 Local Choice/Rivers/L1d_Life_in_the_Grass.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 900 120"` | teaching | medium | 1 <text> label on a 900x120 canvas |

### `5_6 Local Choice/The_Foxglove_Case.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="w-5 h-5 mr-3" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Print Worksheets & Slides" — the control is already named |
| 2 | `class="w-6 h-6 text-amber-500" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 3 | `class="w-8 h-8 text-amber-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 4 | `class="w-6 h-6 text-amber-600" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 5 | `class="w-8 h-8 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 6 | `class="w-10 h-10 mb-2 text-green-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 7 | `class="w-10 h-10 mb-2 text-green-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 8 | `class="w-10 h-10 mb-2 text-green-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 9 | `class="w-10 h-10 mb-2 text-green-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 10 | `class="w-10 h-10 mb-2 text-green-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 11 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 12 | `class="w-8 h-8 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 13 | `class="w-8 h-8 text-slate-400" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 14 | `class="w-6 h-6" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 15 | `class="w-7 h-7 text-amber-800" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 16 | `class="w-6 h-6" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 17 | `class="w-8 h-8 text-amber-700" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 18 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 19 | `class="w-8 h-8 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 20 | `class="w-6 h-6" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 21 | `class="w-8 h-8 text-slate-400" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 22 | `class="w-8 h-8 text-amber-700" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 23 | `class="w-8 h-8 text-sky-500 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 24 | `class="w-6 h-6 text-green-600" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 25 | `class="w-6 h-6 text-green-600 flex-shrink-0 mt-1" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 26 | `class="w-5 h-5" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Previous" — the control is already named |
| 27 | `class="w-5 h-5" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Next" — the control is already named |

### `5_6 Local Choice/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `viewBox="0 0 24 24"` | decorative | high | icon inside a <a> with text "Launch Studio Suite" — the control is already named |
| 3 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 4 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 4 shapes |
| 5 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 7 | `viewBox="0 0 24 24"` | decorative | high | icon inside a <a> with text "Launch the Studio Suite" — the control is already named |
| 8 | `class="search-icon" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 9 | `viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Expand all" — the control is already named |
| 10 | `viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Collapse all" — the control is already named |
| 11 | `class="dice" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> with text "Surprise me" — the control is already named |
| 12 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 3 shapes |
| 13 | `viewBox="0 0 24 24"` | decorative | high | icon inside a <a> with text "Open full" — the control is already named |
| 14 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 1 shapes |
| 15 | `viewBox="0 0 24 24"` | decorative | high | icon inside a <button> already named aria-label="Back to top" — the control is already named |
| 16 | `viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |

### `6 Art/Art_Miro_Mural_STAGE_COUNTDOWNS_FINAL.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `id="miroBuild" viewBox="0 0 800 260"` | review | low | 800x260 (viewBox), 1 shapes, 0 text — not clear-cut |

### `6 Art/Lesson10_SurrealistCollage_HANDSON_v5 (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 220 130"` | teaching | high | 4 <text> labels on a 220x130 canvas |
| 2 | `viewBox="0 0 220 130"` | teaching | high | 4 <text> labels on a 220x130 canvas |
| 3 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Round eye" — not clear-cut |
| 4 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 9 shapes, 0 text, beside: "Lashed eye" — not clear-cut |
| 5 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 5 shapes, 0 text, beside: "Outline eye" — not clear-cut |
| 6 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Wide eye" — not clear-cut |
| 7 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 4 text, beside: "Clock" — not clear-cut |
| 8 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 10 shapes, 0 text, beside: "Gear" — not clear-cut |
| 9 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Hourglass" — not clear-cut |
| 10 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Key" — not clear-cut |
| 11 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Padlock" — not clear-cut |
| 12 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Light bulb" — not clear-cut |
| 13 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 5 shapes, 0 text, beside: "Scissors" — not clear-cut |
| 14 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Spring" — not clear-cut |
| 15 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 9 shapes, 0 text, beside: "Sun" — not clear-cut |
| 16 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 1 shapes, 0 text, beside: "Crescent moon" — not clear-cut |
| 17 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 1 shapes, 0 text, beside: "Star" — not clear-cut |
| 18 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 1 shapes, 0 text, beside: "Cloud" — not clear-cut |
| 19 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 2 shapes, 0 text, beside: "Raindrop" — not clear-cut |
| 20 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Wave" — not clear-cut |
| 21 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 2 shapes, 0 text, beside: "Flame" — not clear-cut |
| 22 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 5 shapes, 0 text, beside: "Leaf" — not clear-cut |
| 23 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 7 shapes, 0 text, beside: "Feather" — not clear-cut |
| 24 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 7 shapes, 0 text, beside: "Butterfly" — not clear-cut |
| 25 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 6 shapes, 0 text, beside: "Bird" — not clear-cut |
| 26 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Fish" — not clear-cut |
| 27 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Snake" — not clear-cut |
| 28 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 5 shapes, 0 text, beside: "Snail" — not clear-cut |
| 29 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Tree" — not clear-cut |
| 30 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 6 shapes, 0 text, beside: "Ladder" — not clear-cut |
| 31 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 2 shapes, 0 text, beside: "Keyhole" — not clear-cut |
| 32 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 6 shapes, 0 text, beside: "Hand" — not clear-cut |
| 33 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 1 shapes, 0 text, beside: "Spiral" — not clear-cut |
| 34 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Balloon" — not clear-cut |
| 35 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Door" — not clear-cut |
| 36 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 2 shapes, 0 text, beside: "Mountain" — not clear-cut |

### `6 Art/Lesson10_SurrealistCollage_OBSERVATION_v5 (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 220 130"` | teaching | high | 4 <text> labels on a 220x130 canvas |
| 2 | `viewBox="0 0 220 130"` | teaching | high | 4 <text> labels on a 220x130 canvas |
| 3 | `viewBox="0 0 220 130"` | teaching | high | 4 <text> labels on a 220x130 canvas |
| 4 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "Eye" — not clear-cut |
| 5 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 4 text, beside: "Clock" — not clear-cut |
| 6 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 6 shapes, 0 text, beside: "Butterfly" — not clear-cut |
| 7 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Lightbulb" — not clear-cut |
| 8 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Wave" — not clear-cut |
| 9 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 5 shapes, 0 text, beside: "Flower" — not clear-cut |
| 10 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 3 shapes, 0 text, beside: "Key" — not clear-cut |
| 11 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 1 shapes, 0 text, beside: "Bird" — not clear-cut |
| 12 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 6 shapes, 0 text, beside: "Gear" — not clear-cut |

### `6 Art/Lesson12_FinishTheEye_DreamIt_v5.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 9 shapes, 0 text — not clear-cut |
| 2 | `class="demo" width="120" viewBox="0 0 120 26"` | decorative | medium | small 120x26 mark, no text, 6 shapes |
| 3 | `class="demo" width="120" viewBox="0 0 120 26"` | decorative | medium | 120x26 mark (viewBox), no text, named alongside: "Sprint 2 · Hatch / A hatched patch: sparse →" |
| 4 | `class="demo" width="120" viewBox="0 0 120 26"` | decorative | medium | small 120x26 mark, no text, 1 shapes |

### `6 Art/Lesson13_TheFinalIdea_v5.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 6 shapes, 0 text — not clear-cut |
| 2 | `viewBox="0 0 320 200"` | teaching | medium | 320x200 with 10 shapes and no text |

### `6 Art/Lesson14_TheTestLab_v5.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 6 shapes, 0 text — not clear-cut |
| 2 | `viewBox="0 0 300 210"` | teaching | high | 4 <text> labels on a 300x210 canvas |

### `6 Art/Lesson15_MiniMasterpiece_v5.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 7 shapes, 0 text — not clear-cut |

### `6 Art/Lesson3_Magritte_Study_v4.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 60 60"` | review | low | 60x60 (viewBox), 7 shapes, 0 text — not clear-cut |
| 2 | `width="100%" viewBox="0 0 480 150"` | teaching | high | 3 <text> labels on a 480x150 canvas |
| 3 | `width="260" viewBox="0 0 280 210"` | review | low | 280x210 (viewBox), 7 shapes, 0 text, beside: ""The False Mirror" (1928)" — not clear-cut |

### `6 Art/Lesson4_Miro_v4.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 60 60"` | review | low | 60x60 (viewBox), 7 shapes, 0 text — not clear-cut |
| 2 | `width="260" viewBox="0 0 300 240"` | review | low | 300x240 (viewBox), 7 shapes, 0 text, beside: "Miró-style composition" — not clear-cut |

### `6 Art/Lesson5_Dali_Research_v4-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 12 shapes, 0 text — not clear-cut |
| 2 | `width="280" viewBox="0 0 320 240"` | teaching | medium | 320x240 with 21 shapes and no text |

### `6 Art/Lesson6_Dali_Study_v4.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 11 shapes, 0 text — not clear-cut |
| 2 | `width="280" viewBox="0 0 320 240"` | teaching | medium | 320x240 with 21 shapes and no text |
| 3 | `width="120" height="120" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 8 shapes, 0 text, beside: "Image with grid" — not clear-cut |
| 4 | `width="120" height="120" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 8 shapes, 0 text, beside: "Sketchbook outline" — not clear-cut |

### `6 Art/Lesson7_Hoch_v5 (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 14 shapes, 0 text — not clear-cut |
| 4 | `width="250" viewBox="0 0 280 240"` | teaching | medium | 280x240 with 21 shapes and no text |

### `6 Art/Lesson8_Hoch_FactFile_v5.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 13 shapes, 0 text — not clear-cut |

### `6 Art/Surrealism_Eye_Study_v5.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="gridsvg eye-hidden" id="demo-grid" viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |
| 2 | `class="gridsvg" id="we-grid" viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |
| 3 | `class="gridsvg eye-hidden" id="ind-grid" viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |
| 4 | `viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |
| 5 | `viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |
| 6 | `viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |
| 7 | `viewBox="0 0 800 535"` | review | low | 800x535 (viewBox), 0 shapes, 0 text — not clear-cut |

### `6 Art/lesson2_magritte-2.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="260" viewBox="0 0 300 240"` | review | low | 300x240 (viewBox), 6 shapes, 0 text, beside: ""The Human Condition" (1933)" — not clear-cut |
| 2 | `width="180" height="100" viewBox="0 0 180 100"` | review | low | 180x100 (viewBox), 2 shapes, 1 text — not clear-cut |
| 3 | `width="180" height="100" viewBox="0 0 180 100"` | review | low | 180x100 (viewBox), 5 shapes, 1 text — not clear-cut |
| 4 | `width="180" height="100" viewBox="0 0 180 100"` | review | low | 180x100 (viewBox), 6 shapes, 1 text — not clear-cut |

### `Assembly/Behaviour Focus/resilience_poster.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 520 120"` | teaching | medium | 1 <text> label on a 520x120 canvas |

### `Assembly/British Value/rule_of_law_poster.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="scaleSvg" viewBox="0 0 480 320"` | teaching | medium | 480x320 with 12 shapes and no text |

### `Assembly/KCSIE/emergency_kcsie_poster (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 520 110"` | review | low | 520x110 (viewBox), 1 shapes, 0 text — not clear-cut |

### `GROW_ASDAN/Community_Project/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `GROW_ASDAN/Enterprise/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `GROW_ASDAN/GROW_ASDAN_Hub.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `GROW_ASDAN/PEQ/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `GROW_ASDAN/Scheme_and_Resources.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `Games/Charcoal.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 120 120"` | decorative | high | icon inside a <div> with text "MADE BY MATT LEARN · BUILD · EXPLO" — the control is already named |
| 2 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "MADE BY MATT" — not clear-cut |
| 3 | `viewBox="0 0 52 52"` | decorative | medium | small 52x52 mark, no text, 3 shapes |

### `Games/Neon_Snake_Overdrive.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="24" height="24" viewBox="0 0 24 24"` | decorative | high | icon inside a <button> already named aria-label="Pause" — the control is already named |

### `Games/Off_Brand.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `viewBox="0 0 120 120"` | decorative | high | icon inside a <div> with text "MADE BY MATT LEARN · BUILD · EXPLO" — the control is already named |
| 2 | `viewBox="0 0 120 120"` | review | low | 120x120 (viewBox), 4 shapes, 0 text, beside: "MADE BY MATT" — not clear-cut |
| 3 | `viewBox="0 0 52 52"` | decorative | medium | small 52x52 mark, no text, 3 shapes |

### `Games/Static.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `id="strings"` | review | low | no viewBox and no width/height; 0 shapes, 0 text |

### `LAUNCH_ASDAN/Careers/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `LAUNCH_ASDAN/Community_Enterprise/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `LAUNCH_ASDAN/Living_Independently/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `LAUNCH_ASDAN/PEQ/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `LAUNCH_ASDAN/Scheme_of_Work.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `LAUNCH_ASDAN/Vocational/START_HERE.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="56" height="56" viewBox="0 0 100 100"` | review | low | 100x100 (viewBox), 3 shapes, 0 text — not clear-cut |

### `biology/Bio_Respiration_Limewater_Exercise.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="18" height="18" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 2 | `class="tube-svg" viewBox="0 0 120 130"` | review | low | 120x130 (viewBox), 11 shapes, 0 text, beside: "▶ Blow into it ↺ Reset CO₂ + limewater → the" — not clear-cut |

### `biology/Chem_Making_Limewater.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="18" height="18" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |

### `biology/Digestion_and_Absorption (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="360" height="50" viewBox="0 0 360 50"` | review | low | 360x50 (viewBox), 7 shapes, 5 text — not clear-cut |
| 2 | `width="280" height="50" viewBox="0 0 280 50"` | review | low | 280x50 (viewBox), 4 shapes, 3 text — not clear-cut |
| 3 | `width="300" height="70" viewBox="0 0 300 70"` | teaching | high | 4 <text> labels on a 300x70 canvas |
| 4 | `width="260" height="130" viewBox="0 0 260 130"` | teaching | high | 4 <text> labels on a 260x130 canvas |
| 5 | `width="280" height="55" viewBox="0 0 280 55"` | review | low | 280x55 (viewBox), 9 shapes, 2 text — not clear-cut |
| 6 | `width="100%" height="340" viewBox="0 0 440 340"` | teaching | high | 16 <text> labels on a 440x340 canvas |
| 7 | `width="100%" viewBox="0 0 320 340"` | teaching | high | 13 <text> labels on a 320x340 canvas |
| 8 | `width="320" height="340" viewBox="0 0 320 340"` | teaching | medium | 1 <text> label on a 320x340 canvas |

### `biology/L5_Anaerobic.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `width="360" height="120" viewBox="0 0 360 120"` | teaching | high | 7 <text> labels on a 360x120 canvas |
| 3 | `width="220" height="110" viewBox="0 0 220 110"` | teaching | high | 4 <text> labels on a 220x110 canvas |

### `biology/Lesson_2_Absorption_v4-6.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="260" height="160" viewBox="0 0 260 160"` | teaching | high | 8 <text> labels on a 260x160 canvas |
| 3 | `width="220" height="240" viewBox="0 0 220 240"` | teaching | high | 6 <text> labels on a 220x240 canvas |
| 4 | `width="240" height="250" viewBox="0 0 240 250"` | teaching | medium | 240x250 with 13 shapes and no text |

### `biology/Respiration_ATP_Recap.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="380" height="100" viewBox="0 0 380 100"` | teaching | high | 11 <text> labels on a 380x100 canvas |
| 2 | `width="220" height="120" viewBox="0 0 220 120"` | teaching | high | 3 <text> labels on a 220x120 canvas |

### `biology/Respiration_and_ATP_Lesson_1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="380" height="100" viewBox="0 0 380 100"` | teaching | high | 11 <text> labels on a 380x100 canvas |
| 2 | `width="220" height="120" viewBox="0 0 220 120"` | teaching | high | 3 <text> labels on a 220x120 canvas |

### `biology/Structure_of_the_Thorax.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `width="260" height="280" viewBox="0 0 260 280"` | teaching | high | 6 <text> labels on a 260x280 canvas |
| 3 | `class="airway-svg" id="airway-svg" width="290" height="300" viewBox="0 0 290 300"` | teaching | high | 9 <text> labels on a 290x300 canvas |
| 4 | `width="280" height="310" viewBox="0 0 280 310"` | teaching | medium | 280x310 with 17 shapes and no text |
| 5 | `class="prot-svg" id="prot-svg" width="270" height="250" viewBox="0 0 270 250"` | teaching | high | 4 <text> labels on a 270x250 canvas |
| 7 | `width="300" height="330" viewBox="0 0 260 280"` | teaching | high | 5 <text> labels on a 260x280 canvas |

### `biology/Testing Breath - FINAL Observation Lesson (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="18" height="18" viewBox="0 0 24 24"` | decorative | high | 24x24 glyph, no text, 2 shapes |
| 2 | `class="tube-svg" viewBox="0 0 120 130"` | review | low | 120x130 (viewBox), 11 shapes, 0 text, beside: "▶ Blow into it ↺ Reset CO₂ + limewater → the" — not clear-cut |

### `chemistry/L3c_VirtualLab_AcidsAlkalis (2).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="ui-dropper-svg" viewBox="0 0 44 58"` | review | low | 44x58 (viewBox), 5 shapes, 1 text, beside: "UniversalIndicator" — not clear-cut |
| 2 | `class="test-tube-svg" viewBox="0 0 100 200"` | review | low | 100x200 (viewBox), 5 shapes, 0 text, beside: "Test tube(empty)" — not clear-cut |
| 3 | `class="burette-svg" viewBox="0 0 80 340"` | teaching | high | 7 <text> labels on a 80x340 canvas |
| 4 | `class="flask-svg" viewBox="0 0 160 140"` | teaching | high | 2 <text> labels on a 160x140 canvas |

### `chemistry/Lesson1_Indicators-1.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="280" height="160" viewBox="0 0 280 160"` | teaching | high | 9 <text> labels on a 280x160 canvas |
| 2 | `width="300" height="180" viewBox="0 0 300 180"` | teaching | high | 8 <text> labels on a 300x180 canvas |

### `chemistry/Lesson2_pH_Scale_v4.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 2 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 3 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 4 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 5 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 6 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 7 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 8 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 9 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 10 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 11 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 12 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 13 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 14 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 15 | `width="60" height="100" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 16 | `width="40" height="68" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 17 | `width="40" height="68" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 18 | `width="44" height="72" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 19 | `width="44" height="72" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 20 | `width="44" height="72" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 21 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 22 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 23 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 24 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |
| 25 | `width="50" height="80" viewBox="0 0 60 100"` | decorative | medium | small 60x100 mark, no text, 2 shapes |

### `chemistry/Lesson3_Ions_Neutralisation_v4.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="280" height="180" viewBox="0 0 280 180"` | teaching | high | 10 <text> labels on a 280x180 canvas |
| 2 | `width="300" height="200" viewBox="0 0 300 200"` | teaching | high | 14 <text> labels on a 300x200 canvas |
| 3 | `width="300" height="140" viewBox="0 0 300 140"` | teaching | high | 10 <text> labels on a 300x140 canvas |
| 4 | `width="120" height="130" viewBox="0 0 120 130"` | review | low | 120x130 (viewBox), 2 shapes, 0 text, beside: "pH:1" — not clear-cut |
| 6 | `width="50" height="70" viewBox="0 0 60 100"` | review | low | 60x100 (viewBox), 1 shapes, 2 text, beside: "Beaker A" — not clear-cut |
| 7 | `width="50" height="70" viewBox="0 0 60 100"` | review | low | 60x100 (viewBox), 1 shapes, 2 text, beside: "Beaker B" — not clear-cut |

### `chemistry/Lesson4a_Gas_Tests_H2_O2_CO2 (1).html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="lab-svg" viewBox="0 0 740 240"` | teaching | high | 11 <text> labels on a 740x240 canvas |

### `chemistry/Lesson4b_Gas_Tests_NH3_Cl2.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `class="lab-svg" viewBox="0 0 740 240"` | teaching | high | 11 <text> labels on a 740x240 canvas |
| 2 | `width="300" height="200" viewBox="0 0 300 200"` | teaching | high | 14 <text> labels on a 300x200 canvas |

### `chemistry/Lesson5_Flame_Tests.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `class="lab-svg" viewBox="0 0 740 240"` | teaching | high | 17 <text> labels on a 740x240 canvas |

### `chemistry/Lesson6_Anion_Water_Tests.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 2 | `class="lab-svg" viewBox="0 0 740 240"` | teaching | high | 14 <text> labels on a 740x240 canvas |

### `primary/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="22" height="22" viewBox="0 0 22 22"` | decorative | high | icon inside a <a> with text "Made by Matt" — the control is already named |
| 2 | `width="18" height="18" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/group-classify-living-things/Lesson1_GroupAnimals.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/group-classify-living-things/Lesson2_VertebratesInvertebrates.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/group-classify-living-things/Lesson3_ClassificationKeysAnimals.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/group-classify-living-things/Lesson4_GroupPlants.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/group-classify-living-things/Lesson5_ClassificationKeysPlants.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/group-classify-living-things/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson10_EvaluateEvaporation.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson1_ExploreStates.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson2_ThinkDifferently.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson3_ChangeStates.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson4_UseEquipment.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson5_PlanMelting.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson6_InvestigateMelting.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson7_WaterCycle.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson8_PlanEvaporation.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/Lesson9_InvestigateEvaporation.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year4/science/autumn/states-of-matter/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson1_Friction.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson2_AirResistance.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson3_PlanParachute.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson4_InvestigateParachute.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson5_EvaluateParachute.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson6_PlanWaterResistance.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson7_InvestigateWaterResistance.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson8_ExploreGravity.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/Lesson9_SmallForcesGreaterEffects.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/forces/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson1_TheSolarSystem.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson2_ThePlanets.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson3_Modelling.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson4_MotionOfEarthAndPlanets.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson5_IdeasOverTime.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson6_PlanetEarth.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson7_NightAndDay.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/Lesson8_TheMoon.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year5/science/autumn/space/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson1_ConditionsForLife.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson2_GroupOrganisms.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson3_ClassifyAnimals.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson4_ClassifyPlants.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson5_Microorganisms.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson6_ClassifyMicroorganisms.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/Lesson7_CarlLinnaeus.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/living-things/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson1_WhatIsRenewableEnergy.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson2_FossilFuelsAndEnvironment.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson3_SolarPower.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson4_WindPower.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson5_WeighingItUp.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson6_RenewableInOurCommunity.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/Lesson7_PlanForOurSchool.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

### `primary/year6/science/autumn/renewable-energy/index.html`

| # | locator | verdict | confidence | evidence |
|---|---|---|---|---|
| 1 | `width="20" height="20" viewBox="0 0 22 22"` | decorative | high | 22x22 glyph, no text, 3 shapes |

