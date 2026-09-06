# Filename labels

Filenames are labels. ORDER VB-RUN13 H12-3 keeps every one of them: renaming a
live deck breaks links, the catalogue, planners and QR codes. The stale week in a
name is recorded here once and read by nobody -- g27 fails any tool under
`_sownb/` or `tools/` that derives a week from a path, and the script that built
this file lives outside both for that reason.

Measured 2026-09-02 across 445 deck files whose name carries a week number.

## What the numbers are

    91  the name agrees with the ruled week of the cells the deck claims
    67  the name DRIFTS from the ruled week of its cells
     6  the name is term-relative, so its number was never an absolute week
   281  the deck claims no cell, so there is nothing to compare the name with

Nearly every drift is one week, and it has a single cause: the run-11 spine
re-key moved Autumn 2, Spring 1, Spring 2 and Summer 2 up by one, and the D-C
correction that carried it through the estate was text only, with zero renames.
That was the right call and it is why this file exists.

  drift distribution, ruled week minus the number in the name:
    +1 week   67 files

## The drifted names

The 67 rows are written once, in `_sownb/FILENAME_DRIFT.md` (file · label week · ruled week), under ORDER VB-RUN14 R0. They are not repeated here.

## Names that are term-relative, not absolute

These carry a term marker before the week number, so the number is a position
inside a term and was never a claim about an absolute week. Not drift.

  PEQ_A2_W7_Complete_Profile_and_Evidence_GROW_v3_40min.html — 7 within its term, cells say [15]
  SCI_G_A2_W7A_Autumn_Science_Review_Explore.html — 7 within its term, cells say [15]
  SCI_G_A2_W7B_Autumn_Science_Evidence_Do.html — 7 within its term, cells say [15]
  SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html — 7 within its term, cells say [15]
  SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html — 7 within its term, cells say [15]
  SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html — 7 within its term, cells say [15]

## Why this file has no bulleted list

Register files in this estate are tokenised bullet by bullet by the g10 name
gate. This is not a register, it is a record, and it carries no bullets so that
it can never be mistaken for one.
