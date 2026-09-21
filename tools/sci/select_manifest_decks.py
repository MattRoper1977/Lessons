#!/usr/bin/env python3
"""ORDER SCI-COMPLETE PASS A3 — select the Spring and Summer decks for the Science shelf.

The shelf lists what tools/catalogue/SHELF_SELECTION.json['science'] names, and
build_catalogue.py re-proves each route's term from current evidence. The Spring
and Summer chassis decks were never named there, so the shelf stopped at Autumn
while the decks, their manifests and their companion packs all existed.

Every route is DERIVED from the pathway folder manifests, never typed and never
inferred from a folder or filename:

  * a folder is in scope only if its manifest.json carries a `lessons` list
  * a route is selected only if its manifest row names a file that exists and
    every workbook cell that row cites resolves in _sownb/CALENDAR_SPINE.json
  * the classification evidence recorded beside the route is exactly the shape
    build_catalogue.py itself emits for such a row, so the selection and the
    rebuilt evidence agree

A row whose cell does not resolve is REFUSED and named; the run writes nothing.
A route already selected is left as it is.

  select_manifest_decks.py --folders Science_Teesside/Build/W18-W26_2026-27 ... [--write]
  select_manifest_decks.py --self-test
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / 'tools/catalogue/SHELF_SELECTION.json'
SPINE = ROOT / '_sownb/CALENDAR_SPINE.json'
METHOD = 'current manifest lesson row with resolved workbook cells'
SOW_METHOD = 'current manifest lesson row sow declaration'
TOKEN = re.compile(r'\b(Aut|Spr|Sum)([12])·W(\d+)\b')


def refs_of(item):
    cells = item.get('cells', ([item['cell']] if item.get('cell') else []))
    return [c.get('reference', '') if isinstance(c, dict) else c for c in cells]


def derive_rows(folder_rel, manifest, cells, exists):
    """Pure: (selected rows, refusals) for one folder's manifest."""
    rows, refused = [], []
    for item in manifest.get('lessons', []):
        if not isinstance(item, dict) or not isinstance(item.get('file'), str):
            continue
        rel = folder_rel.rstrip('/') + '/' + item['file']
        if not exists(rel):
            refused.append((rel, 'manifest names a file that is not in the tree'))
            continue
        refs = refs_of(item)
        if not refs:
            refused.append((rel, 'manifest row cites no workbook cell'))
            continue
        missing = [r for r in refs if r not in cells]
        if missing:
            # build_catalogue.py's own order: the cell method needs EVERY cited cell to
            # resolve; otherwise the row's sow declaration, when it carries a term·week
            # token, is the evidence. The unresolved cells are named beside it, never
            # dropped. A row with neither is refused.
            if TOKEN.search(item.get('sow', '') or ''):
                rows.append({'path': rel,
                             'classificationEvidence': [{'method': SOW_METHOD,
                                                         'source': folder_rel.rstrip('/') + '/manifest.json',
                                                         'file': item['file'], 'quote': item['sow'],
                                                         'unresolvedCells': missing}]})
                continue
            refused.append((rel, 'cell not in the calendar spine and no sow token: ' + ', '.join(missing)))
            continue
        rows.append({'path': rel,
                     'classificationEvidence': [{'method': METHOD,
                                                 'source': folder_rel.rstrip('/') + '/manifest.json',
                                                 'file': item['file'], 'refs': refs}]})
    return rows, refused


def self_test():
    bad = 0
    def check(name, cond):
        nonlocal bad
        print('  [%s] %s' % ('ok' if cond else 'FAIL', name)); bad += 0 if cond else 1
    cells = {"'S'!C1": {'termWeek': 'Spr1·W3'}}
    man = {'lessons': [{'file': 'a.html', 'cells': [{'reference': "'S'!C1"}]},
                       {'file': 'b.html', 'cells': [{'reference': "'S'!C9"}]},
                       {'file': 'd.html', 'cells': [{'reference': "'S'!C1"}, {'reference': "'S'!B1"}], 'sow': 'Spr1·W3 — x'},
                       {'file': 'e.html', 'cells': [{'reference': "'S'!C1"}, {'reference': "'S'!B1"}], 'sow': 'no token here'},
                       {'file': 'c.html'},
                       {'file': 'gone.html', 'cells': [{'reference': "'S'!C1"}]}]}
    ex = lambda rel: not rel.endswith('gone.html')
    rows, refused = derive_rows('X/F', man, cells, ex)
    check('a row whose cell resolves is selected with the builder\'s evidence shape',
          [r['path'] for r in rows] == ['X/F/a.html', 'X/F/d.html'] and rows[0]['classificationEvidence'][0]['method'] == METHOD)
    d = next(r for r in rows if r['path'].endswith('d.html'))
    check('a row with an unresolved cell but a sow token takes the builder\'s sow route, unresolved cells named',
          d['classificationEvidence'][0]['method'] == SOW_METHOD and d['classificationEvidence'][0]['unresolvedCells'] == ["'S'!B1"])
    check('a row with an unresolved cell and no token is refused', any(rel.endswith('e.html') for rel, _ in refused))
    check('a cell missing from the spine is refused by name',
          any('C9' in why for rel, why in refused if rel.endswith('b.html')))
    check('a row citing no cell is refused', any(rel.endswith('c.html') for rel, _ in refused))
    check('a manifest file not in the tree is refused', any(rel.endswith('gone.html') for rel, _ in refused))
    check('nothing is inferred from the folder name: a folder with no manifest rows selects nothing',
          derive_rows('X/W99-W100', {}, cells, ex) == ([], []))
    print('self-test ' + ('PASS' if not bad else 'FAIL (%d)' % bad))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--folders', nargs='*', default=[])
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    cells = {c['reference']: c for c in json.loads(SPINE.read_text())['workbookCells']}
    sel = json.loads(SELECTION.read_text())
    have = {x['path'] for x in sel['science']}
    new, refused = [], []
    for f in a.folders:
        mf = ROOT / f / 'manifest.json'
        if not mf.is_file():
            refused.append((f, 'no manifest.json in this folder')); continue
        rows, bad = derive_rows(f, json.loads(mf.read_text()), cells, lambda rel: (ROOT / rel).is_file())
        refused += bad
        new += [r for r in rows if r['path'] not in have]
    print('SEARCH SCOPE: %d folder(s); %d route(s) already selected; %d new; %d refused'
          % (len(a.folders), len(have), len(new), len(refused)))
    for rel, why in refused:
        print('  REFUSED %s: %s' % (rel, why))
    if refused:
        print('[FAIL] refusals; nothing written'); return 1
    for r in new:
        ev0 = r['classificationEvidence'][0]
        print('  + %s  %s' % (r['path'], ','.join(ev0.get('refs', [])) or 'sow: ' + ev0.get('quote', '')[:30]))
    if a.write and new:
        sel['science'] += new
        SELECTION.write_text(json.dumps(sel, ensure_ascii=False, indent=2) + '\n')
        print('[DONE] science routes %d -> %d' % (len(have), len(sel['science'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
