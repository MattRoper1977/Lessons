#!/usr/bin/env python3
"""ORDER HUM-T, STANDING RULE L38: a carrier that moves a published file is not a carrier.

The L33 carrier bump points the Lessons publication at a new Site carrier. It must therefore
change NOTHING the publication serves: a served file changed on the carrier branch is judged
against the registry the carrier is leaving, and the publication refuses it (batch 1, run
35544583041: CHANGED education-lessons/assets/catalogue/lesson-order.json).

This check reads the Site's education-publication-admission.json, takes the education-lessons
tree's key set as the served path set, and refuses when the branch's changed paths meet it.
It never guesses: no registry, no tree, or an empty tree is a refusal, not a pass.
"""
import argparse, json, subprocess, sys
from pathlib import Path

REGISTRY = 'domain-split/education-publication-admission.json'
TREE = 'education-lessons'


def served_paths(site: Path) -> set:
    f = site / REGISTRY
    if not f.is_file():
        raise SystemExit('REFUSED: no publication registry at %s' % f)
    try:
        registry = json.loads(f.read_text(encoding='utf-8'))
    except ValueError as exc:
        raise SystemExit('REFUSED: publication registry is not readable JSON: %s' % exc)
    trees = registry.get('trees')
    if not isinstance(trees, dict) or TREE not in trees:
        raise SystemExit('REFUSED: publication registry names no %s tree' % TREE)
    paths = set(trees[TREE])
    if not paths:
        raise SystemExit('REFUSED: the %s tree admits no path; nothing could be proved' % TREE)
    return paths


def changed_paths(root: Path, base: str) -> set:
    def run(*args):
        out = subprocess.run(('git', '-C', str(root)) + args, capture_output=True, text=True)
        if out.returncode:
            raise SystemExit('REFUSED: %s failed: %s' % (' '.join(args), out.stderr.strip()))
        return out.stdout.splitlines()
    paths = set()
    for line in run('status', '--porcelain'):
        paths.add(line[3:].split(' -> ')[-1].strip())
    if base:
        paths.update(run('diff', '--name-only', '%s..HEAD' % base))
    return {p for p in paths if p}


def judge(changed: set, served: set) -> list:
    return sorted(changed & served)


def self_test() -> int:
    served = {'assets/catalogue/lesson-order.json', 'data/resource-sizes.json',
              'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W1_People_Special_To_Me.html'}
    red = [
        ('a moved lesson order is refused', {'assets/catalogue/lesson-order.json',
                                             '.github/workflows/education-pages.yml'},
         ['assets/catalogue/lesson-order.json']),
        ('a moved deck is refused', {'Humanities_Teesside/BUILD_W1-W8_2026-27/'
                                     'BUILD_HUM_W1_People_Special_To_Me.html'},
         ['Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W1_People_Special_To_Me.html']),
        ('a moved size table is refused', {'data/resource-sizes.json'}, ['data/resource-sizes.json']),
        ('two served files are both named', {'data/resource-sizes.json',
                                             'assets/catalogue/lesson-order.json'},
         ['assets/catalogue/lesson-order.json', 'data/resource-sizes.json']),
        ('a pure carrier passes', {'.github/workflows/education-pages.yml',
                                   'tools/verify_cross_estate_unification.py',
                                   'tools/catalogue/STATIC_CHECK_RESULTS.json',
                                   '_sx3/SX3_PASSES_LEDGER.md'}, []),
        ('a path merely under a served prefix passes', {'assets/catalogue/lesson-order.json.bak'}, []),
        ('no change at all passes', set(), []),
    ]
    bad = 0
    for name, changed, want in red:
        got = judge(changed, served)
        if got != want:
            bad += 1
            print('  FAIL %s: wanted %s, got %s' % (name, want, got))
        else:
            print('  PASS %s' % name)
    for name, kwargs in (('no registry', {'site': Path('/nonexistent-site')}),):
        try:
            served_paths(**kwargs)
        except SystemExit as exc:
            print('  PASS %s refuses: %s' % (name, str(exc).split(':')[0]))
        else:
            bad += 1
            print('  FAIL %s did not refuse' % name)
    print('self-test %s' % ('PASS' if not bad else 'FAIL'))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', type=Path, help='the Site checkout that carries the publication registry')
    ap.add_argument('--root', type=Path, default=Path('.'), help='the Lessons checkout under test')
    ap.add_argument('--base', default='', help='also judge the committed diff against this ref')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.site:
        raise SystemExit('REFUSED: --site is required (the registry is the Site\'s)')
    served = served_paths(a.site)
    changed = changed_paths(a.root, a.base)
    hit = judge(changed, served)
    print('L38 carrier purity: %d changed, %d served, %d served among the changed'
          % (len(changed), len(served), len(hit)))
    if hit:
        for p in hit:
            print('  REFUSED: the carrier changes a served file: %s' % p)
        return 1
    print('[PASS] the carrier changes nothing the publication serves')
    return 0


if __name__ == '__main__':
    sys.exit(main())
