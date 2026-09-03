# REVIEW — VB-EASTER-A2R (read this first)

Read on a phone. Plain lines, no tables.

## The one thing worth knowing

Four gates have been measuring nothing on 264 of the estate's 607 lesson decks,
and reporting it as a pass.

g18, g23, g24 and g25 all looked for teaching stages in one place:
`main.deck > section.slide`. That is the n6 shell. The classic chassis puts its
stages somewhere else, so on a classic deck those gates found no slides, counted
no words, and printed the good news.

  BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html   0w   x0.0   WITHIN   PASS

That deck has ten stages and 2,159 pupil words. It was reshelled onto the
classic chassis and landed on main in PR #271, and from that moment its period
load, its content floor and its we-do variety went unmeasured.

Under the corrected instrument it reads 2,159 words, family median 1,412,
x1.53, HEAVY, ceiling RED.

Nothing was reverted. The deck is fine. The instrument was not.

## What this PR changes

One new module, lesson_stages.py, is now the only place the estate decides what
pupil teaching content is. Every gate that counts pupil content imports it
instead of deciding for itself.

It reads both shells. It resolves what a pupil actually sees on screen from the
deck's own CSS, so the print pack drops out because `#print-area{display:none}`
says so, not because a class name was typed into a tool.

The hard part was the carousel. Both shells run `.slide{display:none}` with
`.slide.active{display:flex}`, so nine stages in ten are hidden at any instant.
A gate that asked "is this visible?" would count one stage and call the lesson
thin. So visibility is resolved INSIDE a stage, and whether a stage counts at all
is decided by what sits above it. That one distinction is most of the module.

A second correction fell out of it. The old counter joined block elements with
no separator, so every `</p><p>` boundary glued two words into one. Every family
median in the estate was overstated. All nine are re-derived and printed
before -> after on every line. All nine fell, so every ratio rose. The correction
is strictly stricter and no threshold moved.

## Family medians, before -> after

  BUILD ASDAN         1082.5 -> 980.5
  BUILD Humanities    1563.5 -> 1412.0
  BUILD Science       1812.0 -> 1501.5
  GROW ASDAN           991.0 -> 940.5
  GROW Humanities     1104.0 -> 906.0
  GROW Science        1682.5 -> 1378.5
  LAUNCH ASDAN        1493.0 -> 1365.0
  LAUNCH Humanities    923.5 -> 822.0
  LAUNCH Science      1823.5 -> 1551.5

## The two fail-open cases in g24, closed

A print-only diagram counted as screen teaching. The old stage test accepted a
`print-section` ancestor, and the classic chassis has fourteen of those per deck,
so a deck could satisfy "two explanatory visuals per lesson" without a pupil ever
seeing one on the board.

An svg holding three rotated `<text>` labels in a large viewBox satisfied every
numeric test and counted as a diagram. It is typography. A visual now needs a
graphical primitive with real geometry, and no transform makes text into a
drawing.

## The controls

98 controls across 11 tools. Every one planted, shown to fire, withdrawn.

  lesson_stages                    18
  g27 no-filename-weeks            19
  classic-v2 contract selftest     10
  reshell classic-v2 contract      10
  g24 visual density                9
  g25 we-do variety                 8
  cgate containment                 6
  reshell recipe                    6
  g18 family floor                  5
  g23 period load                   5
  g19 token ownership               2

No number above is asserted anywhere. CI asks each tool for its list through
`--list-controls` and requires that every listed control fired. The old workflow
pinned "18 controls" and "133 tools"; adding one tool this session moved the
scanned count from 130 to 131, which is the whole argument.

The battery has its own control: `mechanism_battery.py --prove-red` copies a
tool, inverts one control's expectation, and requires the battery to go red.

## The audit of what landed

9 PRs audited, 3 regressions. Full working in `_sownb/vb/LANDED_AUDIT_A2.md`.

  R1  the shell blindness above
  R2  the reshell dropped nine stage timings that summed to exactly 40, and
      nothing noticed, because R1 hid it: the only reader of data-min was the
      same n6-shaped XPath that already returned nothing on a classic deck
  R3  every screen diagram on a classic deck is print-dead, because the chassis
      hides the whole slide container under @media print

R1 is repaired here. R2 is repaired in the recipe and the contract, but the
landed deck still needs its nine values put back — that is a lesson PR. R3 needs
print-safe figures authored, also a lesson PR. Both are in the resume block.

No workbook, NO-TOUCH deck or allowlist entry was touched. No gate's binding
number moved. g27 is armed and its 19 controls fire.

## The five over-ratio decks, re-measured

  BUILD W15    x1.26 -> x1.44   over 1.25, under 1.5    TRIM
  BUILD W16    x0.0  -> x1.53   over both               TRIM
  GROW W15     x3.14 -> x3.90   over both               SPLIT CANDIDATE
  GROW W16     x1.09 -> x1.38   over 1.25, under 1.5    TRIM
  LAUNCH W15   x3.75 -> x4.29   over both               SPLIT CANDIDATE
  LAUNCH W16   x1.09 -> x1.28   over 1.25, under 1.5    TRIM

The order asked whether the measurement was the defect. It was not: every deck
got worse, because the denominator was overstated.

GROW W15 and LAUNCH W15 are not trims. Both declare 40 minutes, so neither is a
double period, and in both the overload sits in ONE stage: "I Do 2 · connect"
carries about 1,450 words against a 3-minute declaration, where the same stage in
the sibling deck carries 108. Even deleting that stage outright leaves them near
x2.3. Reaching x1.25 would mean moving about 70% of the lesson into the drawer,
which is not a trim by any reading of R5.5. They are yours.

Matt's ruling this session: trim the four, hand back the two. The four are
recorded with their word deltas and are the next session's first lesson PRs.

## Two things that will bite the next session

The reshell recipe cannot currently run on ANY n6 deck on main. It refuses a
source whose lesson-config week disagrees with the ruled week of the cell it
cites — correctly, as a red control. 19 decks disagree, every one by exactly +1,
and every one is a week 14/15/16 deck whose config carries a filename-era label
the run-11 spine re-key left behind. Meanwhile all 30 decks the recipe WOULD
accept are already classic, so reshelling them is a no-op.

Do not fix that by relaxing the check. The check is right and it is catching 19
stale labels. §5.2 is blocked until they are corrected.

The second: `visuals.explanatory.min` asks for 2 explanatory visuals per lesson
and BUILD_HUM_W15 has 0. That is long-standing across all three Humanities
families, not new. Recorded so the corrected g24's reds are not read as fresh
breakage.

## Where the mechanism was proved

  _sownb/vb/evidence/a2r/MECHANISM_PROOF_MATRIX.txt

  Four RSH-3 references     PASS, all four: 9 stages, 40 minutes, non-zero
  Seven-candidate set       reported above
  Negative controls         all RED

The historical W16 negative artefacts the order names lived only in the Codex
preservation folder, which is not recoverable in this venue. Substitutes are
named in the matrix so the swap is auditable, not silent.

## Capability

Chromium 141.0.7390.37, 59 fonts, family fingerprint c555ca08 — identical to
run 14, zero drift. The fingerprint is method-dependent; the method that
reproduces the recorded value is `fc-list -f '%{family}\n' | sort -u | md5sum`,
as WRONG_BEFORE_RIGHT already records.

## Human items

Two SPLIT CANDIDATES: GROW_HUM_W15 and LAUNCH_HUM_W15. Both unlanded, untouched,
and waiting on your decision.
