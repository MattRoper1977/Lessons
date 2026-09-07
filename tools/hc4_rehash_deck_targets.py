#!/usr/bin/env python3
"""Re-hash every deck named in HC4_DECK_TARGETS.json (HC4 §2.1 stop rule).

Exit 0: every sourceSHA256 matches the working tree.
Exit 1: at least one hash moved — STOP, do not edit that deck from this list.
--self-test plants one wrong hash in memory and proves the red fires.
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check(targets):
    moved = []
    for deck in targets['decks']:
        actual = hashlib.sha256((ROOT / deck['sourcePath']).read_bytes()).hexdigest()
        if actual != deck['sourceSHA256']:
            moved.append((deck['sourcePath'], deck['sourceSHA256'][:12], actual[:12]))
    return moved

def main():
    targets = json.loads((ROOT / 'HC4_DECK_TARGETS.json').read_text())
    if '--self-test' in sys.argv:
        real = check(targets)
        planted = json.loads(json.dumps(targets))
        planted['decks'][0]['sourceSHA256'] = '0' * 64
        bad = check(planted)
        restored = check(targets)
        ok = real == [] and len(bad) == 1 and restored == []
        print('self-test real=%s planted=%s restored=%s' % (len(real), len(bad), len(restored)), 'PASS' if ok else 'FAIL')
        sys.exit(0 if ok else 1)
    moved = check(targets)
    for path, want, got in moved:
        print('MOVED', path, want, '->', got)
    print('decks', len(targets['decks']), 'moved', len(moved))
    sys.exit(1 if moved else 0)

if __name__ == '__main__':
    main()
