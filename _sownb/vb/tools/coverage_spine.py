#!/usr/bin/env python3
"""RETIRED 2026-09-02 by ORDER VB-RUN13 R0. Superseded by cell_coverage.py.

This read census_spine.py's output, which derived weeks from filenames, so every
number it produced inherited that defect. It also wrote its result straight into
a closed run's evidence file, which is recorded in WRONG_BEFORE_RIGHT.

The body is in the history at the commit that retired it. Use
_sownb/vb/tools/cell_coverage.py.
"""
import sys

print(__doc__.strip(), file=sys.stderr)
raise SystemExit(2)
