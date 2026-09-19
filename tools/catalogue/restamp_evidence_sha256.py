#!/usr/bin/env python3
"""Re-stamp the recorded source digest of reviewed catalogue evidence entries.

    restamp_evidence_sha256.py --check
    restamp_evidence_sha256.py --write --decks <reviewed.json>
    restamp_evidence_sha256.py --self-test

tools/catalogue/TERM_AND_STYLE_EVIDENCE.json records, per hashed entry, the sha256 of the
bytes that entry's term/style evidence was derived from. When a reviewed release re-dresses a
deck, those bytes move and tools/catalogue/check_catalogue_static.py goes red on a content-hash
mismatch -- correctly, because nothing has yet said the evidence still holds for the new bytes.

restamp_generated_region_digests.py already covers the one case it can PROVE without judgement:
a change confined to the generated maker-splash region. It refuses anything else by name, which
is why it refuses a chassis re-dress. This tool covers the reviewed case instead, and it refuses
to act on judgement it has not been given:

  * the deck list is passed EXPLICITLY and has no default population. A deck outside the list is
    never touched, whatever its digest says.
  * each listed deck carries its REVIEWED NEW DIGEST. If the working tree does not match, the
    bytes moved after the review and the tool refuses the whole run.
  * the narrowed token limb must hold on the new bytes. build_lesson_order.py proves a drifted
    deck through that limb (_sx3/DECISION_quote_limb.md); a deck it cannot prove is refused,
    because re-stamping would freeze in a week binding nothing can demonstrate. This is the
    latent loss _sx3/FENCE.json exists to fence, so a fenced path is refused outright.
  * the entry's recorded term/weeks must still agree with SCIENCE_WEEK_BINDINGS, and style is
    never written.

ONLY the sha256 field of a listed, moved, proved entry is rewritten. No other field, no other
entry, no shelf, no lesson-order projection. After --write, run build_lesson_order.py to project
the digests and re-pin.

--check takes no list: it asserts the invariant the estate actually needs, that no hashed entry's
recorded digest differs from the working tree. That is the same condition check_catalogue_static
asserts, reported per path instead of as one bare assertion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
BINDINGS = ROOT / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'
FENCE = ROOT / '_sx3/FENCE.json'


def moved_entries(entries, digest_of):
    """(path, recorded, actual) for every hashed entry whose bytes no longer match."""
    out = []
    for path, meta in entries.items():
        recorded = meta.get('sha256') if isinstance(meta, dict) else None
        if not recorded:
            continue
        actual = digest_of(path)
        if actual is not None and actual != recorded:
            out.append((path, recorded, actual))
    return sorted(out)


def fenced_paths():
    if not FENCE.is_file():
        return set()
    return {row['path'] for row in json.loads(FENCE.read_text()).get('fenced', [])}


def restamp_plan(entries, reviewed, digest_of, proved, bindings, fenced):
    """Pure rule, so the self-test plants against the code the tree is judged by.

    Returns (errors, restamps, noops). `reviewed` maps path -> reviewed new digest."""
    errors, restamps, noops = [], [], []
    for path in sorted(reviewed):
        meta = entries.get(path)
        if not isinstance(meta, dict) or 'sha256' not in meta:
            errors.append('listed deck has no hashed evidence entry: ' + path)
            continue
        if path in fenced:
            errors.append('listed deck is fenced by _sx3/FENCE.json: ' + path)
            continue
        actual = digest_of(path)
        if actual is None:
            errors.append('listed deck is not present in the tree: ' + path)
            continue
        if actual != reviewed[path]:
            errors.append('working tree disagrees with the reviewed new digest, so the bytes '
                          'moved after the review: ' + path)
            continue
        if actual == meta['sha256']:
            noops.append(path)
            continue
        if path not in proved:
            errors.append('the narrowed token limb does not hold on the new bytes: ' + path)
            continue
        binding = bindings.get(path)
        if binding is not None:
            terms = set(meta.get('terms') or ([meta['term']] if meta.get('term') else []))
            if terms and not all(w['term'] in terms for w in binding.get('weeks', [])):
                errors.append('recorded term/weeks no longer agree with SCIENCE_WEEK_BINDINGS: ' + path)
                continue
        restamps.append((path, meta['sha256'], actual))
    return errors, restamps, noops


def load_proved():
    """The decks build_lesson_order.py currently proves through the narrowed limb."""
    sys.path.insert(0, str(ROOT / 'tools/catalogue'))
    import build_lesson_order
    return set(build_lesson_order.derive()['refreshedSourceProofs'])


def digest_of_tree(path):
    f = ROOT / path
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None


def run_check():
    entries = json.loads(EVIDENCE.read_text())['entries']
    moved = moved_entries(entries, digest_of_tree)
    hashed = sum(1 for m in entries.values() if isinstance(m, dict) and m.get('sha256'))
    print(f'SEARCH SCOPE: {EVIDENCE.relative_to(ROOT)} — {hashed} hashed entries, working-tree bytes')
    for path, recorded, actual in moved:
        print(f'  [MOVED] {path}\n      recorded {recorded}\n      tree     {actual}')
    if moved:
        print(f'[FAIL] {len(moved)} recorded digest(s) differ from the tree; a reviewed re-stamp is '
              f'needed, or the change was not intended')
        return 1
    print(f'[PASS] every hashed entry matches the tree')
    return 0


def run_write(decks_path):
    entries_doc = json.loads(EVIDENCE.read_text())
    entries = entries_doc['entries']
    reviewed = json.loads(Path(decks_path).read_text())
    bindings = json.loads(BINDINGS.read_text())['entries'] if BINDINGS.is_file() else {}
    proved = load_proved()
    errors, restamps, noops = restamp_plan(entries, reviewed, digest_of_tree, proved, bindings, fenced_paths())
    print(f'SEARCH SCOPE: {len(reviewed)} reviewed deck(s) from {decks_path}, '
          f'against {EVIDENCE.relative_to(ROOT)}')
    print(f'  limb-proved decks available: {len(proved)}')
    for e in errors:
        print('  [REFUSED] ' + e)
    for path in noops:
        print(f'  [NO-OP] listed deck already matches its recorded digest: {path}')
    for path, old, new in restamps:
        print(f'  [RESTAMP] {path}\n      {old}\n   -> {new}')
    if errors:
        print(f'[FAIL] {len(errors)} refusal(s); nothing written')
        return 1
    # Only the sha256 of a listed, moved, proved entry is rewritten.
    before = json.dumps(entries_doc, ensure_ascii=False, indent=2) + '\n'
    for path, _old, new in restamps:
        entries[path]['sha256'] = new
    after = json.dumps(entries_doc, ensure_ascii=False, indent=2) + '\n'
    changed = sum(1 for a, b in zip(before.splitlines(), after.splitlines()) if a != b)
    assert changed == len(restamps), f'rewrote {changed} lines for {len(restamps)} re-stamps'
    EVIDENCE.write_text(after)
    print(f'[DONE] {len(restamps)} digest(s) re-stamped, {len(noops)} no-op, '
          f'{changed} line(s) changed in the file')
    return 0


def self_test():
    ok = 0

    def check(name, condition):
        nonlocal ok
        print(f'  [{"ok" if condition else "FAIL"}] {name}')
        ok += 0 if condition else 1

    entries = {
        'A.html': {'sha256': 'a' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'full-lundy'},
        'B.html': {'sha256': 'b' * 64, 'term': 'Aut2', 'terms': ['Aut2'], 'style': 'classic'},
        'F.html': {'sha256': 'f' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'classic'},
        'T.html': {'sha256': 't' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'classic'},
        'U.html': {'sha256': 'u' * 64, 'term': 'Aut1', 'terms': ['Aut1'], 'style': 'classic'},
    }
    tree = {'A.html': '1' * 64, 'B.html': 'b' * 64, 'F.html': '3' * 64,
            'T.html': '4' * 64, 'U.html': '5' * 64}
    d = tree.get
    bindings = {'T.html': {'weeks': [{'term': 'Spr1', 'key': 'Spr1·W2'}]}}
    proved = {'A.html', 'F.html', 'T.html'}
    fenced = {'F.html'}

    e, r, n = restamp_plan(entries, {'A.html': '1' * 64}, d, proved, bindings, fenced)
    check('a listed, moved, proved deck is re-stamped', not e and [x[0] for x in r] == ['A.html'])

    e, r, n = restamp_plan(entries, {'A.html': '1' * 64}, d, proved, bindings, fenced)
    check('(i) an unlisted deck is never touched', 'B.html' not in [x[0] for x in r]
          and 'U.html' not in [x[0] for x in r] and len(r) == 1)

    e, r, n = restamp_plan(entries, {'T.html': '4' * 64}, d, proved, bindings, fenced)
    check('(ii) recorded term disagreeing with the binding is refused',
          len(e) == 1 and 'no longer agree with SCIENCE_WEEK_BINDINGS' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'B.html': 'b' * 64}, d, proved, bindings, fenced)
    check('(iii) a listed deck whose bytes did not move is a reported no-op',
          not e and not r and n == ['B.html'])

    e, r, n = restamp_plan(entries, {'U.html': '5' * 64}, d, proved, bindings, fenced)
    check('a deck the token limb cannot prove is refused',
          len(e) == 1 and 'narrowed token limb' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'F.html': '3' * 64}, d, proved, bindings, fenced)
    check('a fenced deck is refused outright', len(e) == 1 and 'fenced' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'A.html': '9' * 64}, d, proved, bindings, fenced)
    check('bytes that moved after the review are refused',
          len(e) == 1 and 'moved after the review' in e[0] and not r)

    e, r, n = restamp_plan(entries, {'Z.html': '1' * 64}, d, proved, bindings, fenced)
    check('a listed deck with no evidence entry is refused',
          len(e) == 1 and 'no hashed evidence entry' in e[0] and not r)

    e, r, n = restamp_plan(entries, {}, d, proved, bindings, fenced)
    check('an empty list writes nothing', not e and not r and not n)

    print('self-test ' + ('PASS' if not ok else f'FAIL ({ok})'))
    return 1 if ok else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--self-test', action='store_true')
    ap.add_argument('--decks', help='JSON mapping deck path -> reviewed new sha256. Required with --write.')
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.check:
        return run_check()
    if not args.decks:
        ap.error('--write requires --decks: the reviewed deck list is never defaulted')
    return run_write(args.decks)


if __name__ == '__main__':
    sys.exit(main())
