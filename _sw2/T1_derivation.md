# SW2 T1 — where every token value is read from (derivation record, before writing the file)

T1 says the values are read, never retyped. This records each source, and the three
places where the order's own parenthetical differs from what the estate ships. In each
case the estate wins, per §0.4 "derive/degrade/never invent" and §0.7 "from the records,
never typed".

## Pathway chips — READ, source recorded

The order says to read these from "a BUILD, a GROW and a LAUNCH deck's chassis CSS".
**Measured: the deck chassis does not carry them.** The BUILD, GROW and LAUNCH
Humanities decks share one palette (`--bg #fff`, `--text #1f2937`, `--lo-bg #e6d4e8`,
`--task-bg #fef9c3` …) with no per-pathway colour at all, so there is nothing to read
there. The estate's single definition is UX2 A2's:

  file  `assets/catalogue/hub.css`  ·  selector `:root`  ·  lines 8–9

| pathway | ink | background |
|---|---|---|
| BUILD | `--t-build #8A4C0B` | `--b-build #F5DDBF` |
| GROW | `--t-grow #2F6B4D` | `--b-grow #D5EEDD` |
| LAUNCH | `--t-launch #6E5A0C` | `--b-launch #F3E8B8` |

**AUTO-DECISION T1-1.** Read the pathway chips from `assets/catalogue/hub.css:8–9`
rather than from a deck chassis, because the decks carry no pathway colour. Same rule
as the order intends (read, don't retype); different file, and the file is named here.

## Subject accents — the order's colour names do NOT match what UX2 ships

The order writes "subject accents (Science orange · Humanities & RE green · Art Studio
purple · Lifeskills grey-blue) **as already used by UX2**". Those two halves disagree.
UX2's map is in `resources/index.html` (UX2 B4), `:root` plus the unit-card subject
band:

| subject | the order's word | what UX2 actually ships |
|---|---|---|
| Science | orange | **green** `--green #247761` |
| Humanities & RE | green | **blue** `--blue #33608f` |
| Art Studio | purple | **purple** `--purple #7c5cb8` — the one that agrees |
| Lifeskills | grey-blue | **amber** `--amber #f2a24a` |

**AUTO-DECISION T1-2.** Take the shipped map, not the parenthetical. "As already used
by UX2" is the instruction; the colour words are a description of it that has drifted,
and following the words would repaint three of four subjects across the estate and
disagree with the Resources page the same order tells us not to change. Both readings
are recorded here so the choice is visible rather than silent.

## Values the order gives as hex, checked against what is in use

| token | order | in the estate today |
|---|---|---|
| `--mbm-ink` / `--mbm-primary` `#161d3d` | given | **matches** `--navy #161D3D` (`hub.css:6`) and `--mbm-navy` (`brand-tokens.css`) |
| `--mbm-bg` `#f6f1e7` | given | close to, but not equal to, `--cream #F6F1E4` (10 pages), `#F6F3EC` (2), `#F5F3EC` (1) |
| `--mbm-card` `#ffffff` | given | in use is `--card #FFFDF6` on every card but `/for/pupils/` |
| `--mbm-card-radius` `12px` | given | in use: 12 · 14 · 16 · 17 · 20 px; `brand-tokens.css` says 14px |
| `--mbm-accent` `#1f6b4a` | given | no accent token exists today; nearest in use is `--mint-deep #2F6B4D` (`hub.css:6`) |

The four given hexes are taken as written, because T1 states them as values rather than
as derivations. The differences are listed so the visual change is expected: `--mbm-bg`
moves every page by a hair, `--mbm-card` whitens the card fill, and the radius
converges five values onto one.

## Still to read before the file is written

- format badges HTML amber / PPTX red / DOCX blue / PDF grey — source not yet located
- dark set for Play — to be read from the shelf CSS (`domain-split/play/play.css`)
- contrast: every ink/background pair measured ≥4.5:1 body, ≥3:1 large and chips

## Outcome

`assets/mbm-tokens.css` written on Site branch `claude/sw2-t1-tokens` (61e905e),
3,959 bytes against the 8 KB cap. Format badges and subject accents each ship a
paired ink token, because the measurement showed no single ink is readable on all
four: amber needs dark ink and fails under white, the other three the reverse. With
the pairs, every combination the file offers measures ≥4.5:1 against a 3:1
requirement. Raw table in `_sw2/T1_contrast.txt`.

Remaining in Part T: T2 chrome templates, T3 stamping, T4 gates, T5 landing.
