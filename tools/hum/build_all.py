#!/usr/bin/env python3
"""ORDER HUM-T stage B — apply the template fixes, then the loop transplant,
to every deck in the signed strand record, and run the acceptance battery.

Order matters: the template defects are fixed FIRST so the transplant reads a
deck whose title and cells are already correct.
"""
from __future__ import annotations
import json, sys, collections
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_template_defects import fix as fix_template      # noqa: E402
from loop_adapter import adapt                            # noqa: E402
from verify_loop import verify, science_texts, FAIL       # noqa: E402


def main(root: Path, write: bool):
    rec = json.loads((root / 'tools/catalogue/HUMANITIES_STRAND.json').read_text())
    sci = science_texts(root)
    report = []
    for r in rec['lessons']:
        p = root / r['path']
        original = p.read_text(errors='replace')
        fixed, tinfo = fix_template(original)
        after, info = adapt(fixed, r['pathway'], r['strand'] == 'RE')
        rows = verify(after, fixed, r['strand'], sci)
        fails = [x for x in rows if x['status'] == FAIL]
        report.append({
            'path': r['path'], 'pathway': r['pathway'], 'strand': r['strand'],
            'term': r['term'], 'week': r['week'], 'alternative': r['alternative'],
            'family': info['family'], 'panels': info['panels'],
            'ribbons_removed': info['ribbons_removed'],
            'lundy_stage_removed': info['lundy_stage_removed'],
            'title_fixed': tinfo['title'], 'cells_blanked': tinfo['council_cells'],
            'cells_added': tinfo['cells_added'],
            'bytes_before': len(original.encode()), 'bytes_after': len(after.encode()),
            'fails': [{'row': x['row'], 'name': x['name'], 'detail': x['detail'][:200]} for x in fails],
            'verdict': 'SHIP' if not fails else 'HELD',
        })
        if write:
            p.write_text(after)
    return report


if __name__ == '__main__':
    root = Path(sys.argv[1])
    write = '--write' in sys.argv
    rep = main(root, write)
    out = root / '_hum/BUILD_REPORT.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rep, indent=1))
    ship = [x for x in rep if x['verdict'] == 'SHIP']
    held = [x for x in rep if x['verdict'] == 'HELD']
    print('SCOPE: %d decks from the signed strand record — %s' % (len(rep), 'WRITTEN' if write else 'dry run'))
    print('  SHIP %d   HELD %d' % (len(ship), len(held)))
    print('  families: %s' % dict(collections.Counter(x['family'] for x in rep)))
    print('  panels written        : %d' % sum(x['panels'] for x in rep))
    print('  ribbons removed       : %d' % sum(x['ribbons_removed'] for x in rep))
    print('  quarantined stages cut: %d' % sum(x['lundy_stage_removed'] for x in rep))
    print('  titles corrected      : %d' % sum(1 for x in rep if x['title_fixed']))
    print('  stray cells blanked   : %d' % sum(x['cells_blanked'] for x in rep))
    print('  missing cells added   : %d in %d decks' % (sum(x['cells_added'] for x in rep), sum(1 for x in rep if x['cells_added'])))
    for x in held[:10]:
        print('  HELD %s' % x['path'])
        for f in x['fails'][:3]:
            print('       row %s %s — %s' % (f['row'], f['name'], f['detail'][:120]))
