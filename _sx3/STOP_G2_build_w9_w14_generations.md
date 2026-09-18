# STOP-G2 — the two generations of the BUILD W9–W14 ten are different products

Standing Ruling 4: a landing deck with a second generation and no ruling is HELD.
No generation ruling without a full surface comparison. Here is the comparison.

## Search scope

For each of the ten identities:
**Generation A** = `scratchpad/sx3/unpacked/BUILD_Rocks_Collection_Part_1_W9_W10_and_Classic/…`
and `…_Part_2_W12_W13_W14/…` — the generation currently transplanted onto
`claude/sx3-build-1`.
**Generation B** = `scratchpad/sx3r/BUILD_Remaining_Science_Part_01_1/BUILD/…`.
Every surface below was read from those two files only.

## The ten

`SCI_B_W9A_Rock_Evidence_Explore` · `SCI_B_W9B_Rock_Sorting_Key_Do` ·
`SCI_B_W10A_Rock_Hardness_Explore` · `SCI_B_W10B_Hardness_Evidence_Do` ·
`SCI_B_W12A_Rock_Jobs_Which_Property_Matters_Explore` ·
`SCI_B_W12B_Choose_Rock_For_The_Job_Do` ·
`SCI_B_W13A_Fair_Test_Planner_Change_One_Thing_Explore` ·
`SCI_B_W13B_Method_Pilot_Test_The_Test_Do` ·
`SCI_B_W14A_Autumn_Science_Review_Explore` ·
`SCI_B_W14B_Autumn_Science_Evidence_Do`

## Surface comparison

Eight of the ten (W9A–W13B) are one shape; W14A/W14B are a second shape.

**W9A–W13B (8 decks), A → B:**

| surface | A | B |
|---|---|---|
| bytes | 710 KB – 924 KB | 105 KB – 156 KB |
| slides | 7 | 9 |
| dialogs | 6 | 3 |
| dialog ids | `organiser` `pause` `reset` `staff` `tools` `words` | `guidanceDialog` `loopDialog` `taDialog` |
| buttons | 103–107 | 76–85 |
| inputs / selects / textareas | 32 | 2 |
| `[data-action]` | 9 | 16 |
| h2 / h3 | 37–38 / 70–76 | 13 / 25–29 |
| words | 11,685 – 13,142 | 6,350 – 7,157 |
| repeated Lundy panels | **0** | **10** |
| `#print-area` | **present** | **absent** |
| `lesson-config.sow` | **absent** | **present** (explicit outcome) |
| `lesson-config.week` | absent | present (9, 10, 12, 13) |

**W14A / W14B, A → B:** 7 → 13 slides; 6 dialogs either side but a different set
(A: `organiser` `reset` `staff` `words`; B: `cold-call` `ta` `word` `workbook`);
buttons 105–106 → 38; words ~12,800 → ~5,660; and **B has no `h1` at all**
(A has `Autumn Science Review Map` / `Autumn Science Evidence`).

## What this means

Neither generation is a superset of the other. Choosing B over A:

- **loses the print section on 8 of 10** (`#print-area` absent)
- **loses the staff toolkit** — organiser, pause, reset, staff, tools, words
  dialogs replaced by guidance / loop / TA
- **halves the written content** (~12,500 → ~6,500 words)
- **loses 30 of 32 pupil inputs**
- **gains the Lundy Loop** (0 → 10 repeated panels), which also reclassifies the
  deck `earlier` → `full-lundy` on the shelf
- **gains an explicit SoW outcome and week**, which is the only one of the two
  that carries its own calendar binding
- on W14A/W14B, **loses the `h1`**

That is an editorial choice about what these lessons are, not a build-quality
choice. I am not making it.

## Requested ruling

Name the authoritative generation for these ten, the way ruling 3 named
`LAUNCH_Science_W3-W7_Complete` for the LAUNCH twelve. Until then all ten stay
HELD and appear in no PR.

---

# Ruling applied — ORDER SX3-M2 §3 — and its overturning condition FIRED

§3 ruled Generation A authoritative, on the principle that when neither
generation is a superset you choose the one whose deficit is **additive**, and
named one measurement that could overturn it: *if the served W9–W14 decks carry
Lundy panels today, A regresses served pedagogy and all ten stay HELD.*

## The measurement

Search scope: the ten routes at `origin/main`, each passed through
`with_lesson_navigation()` from the Site repo's `domain-split/build_education.py`
at `f70f49733373ccfc1660e85771a80eb6f612d6b9` — the exact transform the Education
Pages publication applies to every Lessons `.html` — then counted for repeated
Lundy panels by `build_catalogue.py`'s own rule (class contains `lundy-grid` or
`lundy-loop`).

| route | main | **served** |
|---|---|---|
| `SCI_B_W9A_Rock_Evidence_Explore.html` | 10 | **10** |
| `SCI_B_W9B_Rock_Sorting_Key_Do.html` | 10 | **10** |
| `SCI_B_W10A_Rock_Hardness_Explore.html` | 10 | **10** |
| `SCI_B_W10B_Hardness_Evidence_Do.html` | 10 | **10** |
| `SCI_B_W12A_Rock_Jobs_Which_Property_Matters_Explore.html` | 10 | **10** |
| `SCI_B_W12B_Choose_Rock_For_The_Job_Do.html` | 10 | **10** |
| `SCI_B_W13A_Fair_Test_Planner_Change_One_Thing_Explore.html` | 10 | **10** |
| `SCI_B_W13B_Method_Pilot_Test_The_Test_Do.html` | 10 | **10** |
| `SCI_B_W14A_Autumn_Science_Review_Explore.html` | 9 | **9** |
| `SCI_B_W14B_Autumn_Science_Evidence_Do.html` | 9 | **9** |
| **total** | **98** | **98** |

The transform changes the bytes of all ten (it injects the education navigation
adapter) and changes the panel count of none.

## Verdict: NOT ZERO. HELD A IS NOT DISCHARGED.

All ten stay HELD. Landing set stays **36**; held stays **39**.

## Why this inverts the premise, not just the outcome

`A = 0 / B = 10`, as §3 asked be recorded. Set against the served state:

- **Served today: 9–10 panels per deck.**
- **Generation A: 0.** Landing A would *remove* 98 repeated Lundy panels from
  what is served. That is not an additive deficit — it is a regression against
  live content.
- **Generation B: 10.** B matches the served state on this axis.

So the additive-deficit principle, applied against the served baseline rather
than against B, points the other way on this particular axis. A's other
advantages (print on 8/10, the staff toolkit, twice the words, 30 more inputs)
still stand, and B's losses are still a re-authoring job. Neither generation is
safe to land as it stands: A regresses the Lundy scaffold, B regresses print,
toolkit and content volume.

§3 also directed that the Lundy panels must **not** be added to A now, because
doing so reclassifies the shelf row (`earlier` → `full-lundy`). That instruction
and this measurement together mean there is no in-release path for these ten.

## The question §3 asked be put to Matt

Curriculum policy references Lundy conditions. The served BUILD W9–W14 decks
carry 9–10 repeated Lundy panels each today. Any pack generation that drops them
drops a documented curriculum commitment from live teaching material.

**Requested:** does the Lundy scaffold on these ten routes have to survive the
upgrade? If yes, this is the same supply question as STOP-S3 — the pack is re-cut
preserving it, an authoring order — and these ten join the re-author queue rather
than the release.
