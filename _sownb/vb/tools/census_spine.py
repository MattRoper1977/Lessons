#!/usr/bin/env python3
"""RETIRED 2026-09-02 by ORDER VB-RUN13 R0. Superseded by cell_coverage.py.

This tool derived a deck's teaching week from its filename and from
CALENDAR_SPINE's absoluteWeek column. Both are now out of bounds:

  "Coverage is counted PER WORKBOOK CELL, never per week, never per file. A week
   is a property of a cell (via the ruled spine); a deck's week is the ruled week
   of the cells its TRACE claims. No tool may derive a week from a filename, a
   folder name or CALENDAR_SPINE.json's absoluteWeek column."

Why the rule exists, and why this file is the reason for it. The run-11 spine
re-key moved labels and left filenames alone, on purpose and correctly -- a
filename is a label, and renaming live decks breaks links, catalogues, planners
and QR codes. So a filename still counts weeks the old way. This tool read the
filename, reported weeks as open that already had decks standing in them, and
run 12 authored five lessons against that list. All five were duplicates. None
shipped, but the whole build was lost.

The body is not kept here. It is in the history, at the commit that retired it,
and nothing is deleted. Use:

    _sownb/vb/tools/cell_coverage.py     coverage per workbook cell
    _sownb/vb/tools/g27_no_filename_weeks.py   the gate that keeps it that way
"""
import sys

print(__doc__.strip(), file=sys.stderr)
raise SystemExit(2)
