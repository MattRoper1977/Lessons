#!/usr/bin/env python3
"""CX2 §4.2 · plain-language edits to pupil-facing text, driven by a JSON table.

The reading band is a GATE for lessons authored under CX2 (LESSON_STANDARD_2026-27.md
B1). BUILD W8B measured 5.18 against the BUILD band 1.0-4.0, and the load is in
the sentence shapes, not the science words: the instrument keeps subject vocabulary
and this pass keeps it too (contract, relax, vertebrate, carbohydrate, protein,
calcium, nutrient, energy, joint, backbone all stay). What changes is the Tier 2
scaffolding around them: 'provides' -> 'gives', 'simplified' -> 'simple',
'distinguish' -> 'is not the same as', long joined sentences split in two.

Each row is an exact string pair. Every `old` must be present at least once (the
same sentence often appears on the slide AND in its print sheet, and both copies
move together, which is the print-parity rule) and after the run no `old` may
remain. A second run finds nothing to do. --check reports without writing.

    python3 tools/rw1/pupil_text_edits.py tools/rw1/edits/W8B_plain_language.json [--check]
"""
import argparse, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def run(table_path, check):
    table = json.loads(Path(table_path).read_text())
    path = REPO / table['file']
    text = before = path.read_text()
    applied = already = 0
    for old, new in table['edits']:
        assert old != new and old, old
        have, done = text.count(old), text.count(new)
        if have == 0 and done >= 1:
            already += 1
            continue
        assert have >= 1, 'anchor absent: %r' % old[:90]
        text = text.replace(old, new)
        applied += 1
    for old, new in table['edits']:
        assert old not in text or old in new, 'old text survived: %r' % old[:90]
    changed = text != before
    if changed and not check:
        path.write_text(text)
    print('%s: %d rows, %d applied, %d already, %s' % (path.name, len(table['edits']), applied, already,
          ('WOULD CHANGE' if check else 'written') if changed else 'up to date'))
    return changed


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('tables', nargs='+')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    pending = sum(run(t, args.check) for t in args.tables)
    if args.check and pending:
        sys.exit('[FAIL] %d table(s) not applied' % pending)
