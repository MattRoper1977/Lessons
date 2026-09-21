#!/usr/bin/env python3
"""SCI-COMPLETE PASS B — the chassis census of the science shelf, as a pinned record.

A route CONFORMS when its own bytes carry the exemplar chassis: stateful Lundy steps
(data-lundy-step with data-state), the three loop controls the sequence script drives
(data-action lundy-voice / lundy-audience / lundy-influence), and the named next moves
(data-next-move). Anything less is measured and named, never inferred from a style
label: the evidence record can say full-lundy while the bytes carry no furniture, and
this record is what the science hub reads to decide what is current (PASS F).

Writes tools/catalogue/SCIENCE_CHASSIS_CENSUS.json; --check refuses when the record
does not match the tree; --self-test red-proves the measure.
"""
import argparse, collections, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHELF = ROOT / 'assets/catalogue/science-shelf.json'
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
OUT = ROOT / 'tools/catalogue/SCIENCE_CHASSIS_CENSUS.json'

STEP = re.compile(r'data-lundy-step="[a-z]+"[^>]*data-state="|data-state="[^"]*"[^>]*data-lundy-step="')
CONTROL = re.compile(r'data-action="lundy-(voice|audience|influence)"')
MOVE = re.compile(r'data-next-move="')


def measure(text: str) -> dict:
    steps = len(STEP.findall(text))
    controls = collections.Counter(CONTROL.findall(text))
    moves = len(MOVE.findall(text))
    has_all = all(controls.get(k) for k in ('voice', 'audience', 'influence'))
    if steps and has_all and moves:
        cls = 'conforming'
    elif steps and not has_all:
        cls = 'ribbon-only'
    elif not steps:
        cls = 'no-furniture'
    else:
        cls = 'partial'
    return {'class': cls, 'statefulSteps': steps, 'controls': dict(controls), 'namedMoves': moves}


def census(root: Path) -> dict:
    shelf = json.loads((root / 'assets/catalogue/science-shelf.json').read_text())
    evidence = json.loads((root / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json').read_text())['entries']
    rows = {}
    for r in shelf['lessons']:
        data = (root / r['path']).read_bytes()
        m = measure(data.decode('utf-8', 'replace'))
        m['sha256'] = hashlib.sha256(data).hexdigest()
        m['recordedStyle'] = (evidence.get(r['path']) or {}).get('style')
        rows[r['path']] = m
    counts = collections.Counter(m['class'] for m in rows.values())
    by_style = collections.defaultdict(collections.Counter)
    for m in rows.values():
        by_style[m['class']][str(m['recordedStyle'])] += 1
    return {'schema': 'science-chassis-census/1', 'order': 'SCI-COMPLETE PASS B',
            'rule': 'conforming = stateful Lundy steps + the three loop controls + named next moves, all in the route\'s own bytes',
            'routes': len(rows), 'counts': dict(counts), 'byRecordedStyle': {k: dict(v) for k, v in by_style.items()},
            'conforming': sorted(p for p, m in rows.items() if m['class'] == 'conforming'),
            'entries': dict(sorted(rows.items()))}


def self_test() -> int:
    bad = 0
    def check(name, cond):
        nonlocal bad
        print('  %s %s' % ('PASS' if cond else 'FAIL', name)); bad += 0 if cond else 1
    ex = ('<div class="ls" data-lundy-step="space" data-state="available">SPACE</div>'
          '<button data-action="lundy-voice">v</button><button data-action="lundy-audience">a</button>'
          '<button data-next-move="secure" data-action="lundy-influence">Secure</button>')
    check('the exemplar shape conforms', measure(ex)['class'] == 'conforming')
    check('a ribbon with steps but no controls is ribbon-only', measure('<div data-lundy-step="voice" data-state="waiting">')['class'] == 'ribbon-only')
    check('no furniture is no-furniture', measure('<p>plain deck</p>')['class'] == 'no-furniture')
    check('controls without named moves do not conform', measure(ex.replace(' data-next-move="secure"', ''))['class'] != 'conforming')
    check('a missing audience control does not conform', measure(ex.replace('<button data-action="lundy-audience">a</button>', ''))['class'] != 'conforming')
    check('a style label alone conforms nothing', measure('<meta name="style" content="full-lundy">')['class'] == 'no-furniture')
    print('self-test %s' % ('PASS' if not bad else 'FAIL'))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true'); ap.add_argument('--check', action='store_true'); ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    c = census(ROOT)
    text = json.dumps(c, indent=1, ensure_ascii=False) + '\n'
    if a.write:
        OUT.write_text(text); print('wrote %s: %d routes, %s' % (OUT.relative_to(ROOT), c['routes'], c['counts'])); return 0
    if a.check:
        if not OUT.is_file():
            print('[FAIL] no census record'); return 1
        old = json.loads(OUT.read_text())
        if old.get('entries') != c['entries']:
            diff = [p for p in set(old.get('entries', {})) | set(c['entries']) if old.get('entries', {}).get(p) != c['entries'].get(p)]
            print('[FAIL] the census record differs from the tree on %d route(s): %s' % (len(diff), diff[:3])); return 1
        print('[PASS] the chassis census matches the tree: %d routes, %s' % (c['routes'], c['counts'])); return 0
    print(json.dumps({k: c[k] for k in ('routes', 'counts', 'byRecordedStyle')}, indent=1)); return 0


if __name__ == '__main__':
    sys.exit(main())
