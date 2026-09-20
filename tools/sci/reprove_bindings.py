#!/usr/bin/env python3
"""ORDER SCI-COMPLETE PASS A2 — re-prove the Science week bindings, never re-author.

A binding is RE-PROVED when the deck's CURRENT text still states the binding, by
any of three forms the estate itself writes:

    quote  the recorded evidence sentence, verbatim
    token  Aut2·W7
    label  Autumn 2 · Week 7

The estate's own readers (`build_catalogue.py` term_codes, `build_lesson_order.py`
weeks_from) accept token OR label; only the quote limb ever required one form.
Accepting all three is what STOP_C2b_55_buckets called for and is not a loosening:
a deck that states no binding still cannot be re-proved.

A binding that no form re-proves is IDENTITY-PINNED: its sourceSha256 is re-stamped
to the served bytes and the basis is recorded as identity only, with the term taken
from the deck's own lesson-config. That is a weaker claim and it is written down as
one, per row, so nothing silently passes as re-proved.

Nothing here edits a lesson. Only the binding record is written.
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

TERM_LABEL = {'Aut1': 'Autumn 1', 'Aut2': 'Autumn 2', 'Spr1': 'Spring 1',
              'Spr2': 'Spring 2', 'Sum1': 'Summer 1', 'Sum2': 'Summer 2'}


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def flat(p: Path) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', p.read_text(errors='replace')))


def config_term(p: Path):
    """The deck's OWN lesson-config term, used only to name an identity pin's basis."""
    h = p.read_text(errors='replace')
    m = re.search(r'"term"\s*:\s*"([^"]+)"', h)
    return m.group(1) if m else None


def limb(entry, text):
    """Which limb re-proves this binding in the current text, if any."""
    for ev in (entry.get('evidence') or []):
        q = re.sub(r'\s+', ' ', (ev.get('quote') or '')).strip()
        if q and q in text:
            return 'quote'
    weeks = entry.get('weeks') or []
    if not weeks:
        return None
    if all(w['key'] in text for w in weeks):
        return 'token'
    if all('%s · Week %d' % (TERM_LABEL.get(w['term'], w['term']), w['weekWithinTerm']) in text
           for w in weeks):
        return 'label'
    return None


def audit(root: Path):
    rec = json.loads((root / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json').read_text())
    out = []
    for path, entry in rec['entries'].items():
        p = root / path
        cur = sha(p)
        if cur is None:
            out.append({'path': path, 'state': 'MISSING FILE'})
            continue
        if cur == entry.get('sourceSha256'):
            out.append({'path': path, 'state': 'FRESH'})
            continue
        which = limb(entry, flat(p))
        out.append({'path': path, 'state': 'REPROVED' if which else 'IDENTITY',
                    'limb': which, 'pathway': entry.get('pathway'),
                    'weeks': [w['key'] for w in (entry.get('weeks') or [])],
                    'configTerm': config_term(p), 'newSha256': cur,
                    'oldSha256': entry.get('sourceSha256')})
    return rec, out


def apply(root: Path, rec, rows, stamp: str):
    n_re = n_id = 0
    for r in rows:
        if r['state'] not in ('REPROVED', 'IDENTITY'):
            continue
        e = rec['entries'][r['path']]
        e['sourceSha256'] = r['newSha256']
        e['sourceProofUnchanged'] = False
        if r['state'] == 'REPROVED':
            e['reproof'] = {'basis': 're-proved from the deck\'s own current text',
                            'limb': r['limb'], 'at': stamp}
            n_re += 1
        else:
            e['reproof'] = {
                'basis': 'identity only; the deck restates no binding. Term taken from '
                         'the deck\'s own lesson-config.',
                'limb': None, 'configTerm': r['configTerm'], 'at': stamp}
            n_id += 1
    rec.setdefault('reproofSummary', {})[stamp] = {'reProved': n_re, 'identityPinned': n_id}
    (root / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json').write_text(
        json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
    return n_re, n_id


def self_test() -> bool:
    checks = []
    e = {'weeks': [{'key': 'Aut2·W7', 'term': 'Aut2', 'weekWithinTerm': 7}],
         'evidence': [{'quote': 'Lesson overview GROW Autumn 2 Week 7'}]}
    checks.append(('quote limb fires', limb(e, 'x Lesson overview GROW Autumn 2 Week 7 y') == 'quote'))
    checks.append(('token limb fires when the quote broke',
                   limb(e, 'breadcrumb inserted ... Aut2·W7 ...') == 'token'))
    checks.append(('label limb fires when neither quote nor token is present',
                   limb(e, 'GROW · Science · Autumn 2 · Week 7 · Do') == 'label'))
    checks.append(('a deck stating NO binding is not re-proved',
                   limb(e, 'nothing about weeks here') is None))
    checks.append(('a deck stating the WRONG week is not re-proved',
                   limb({'weeks': [{'key': 'Aut2·W7', 'term': 'Aut2', 'weekWithinTerm': 7}],
                         'evidence': []}, 'Autumn 2 · Week 4') is None))
    checks.append(('an entry with no week at all is not re-proved',
                   limb({'weeks': [], 'evidence': []}, 'Autumn 2 · Week 7') is None))
    ok = True
    for name, good in checks:
        print(('  PASS ' if good else '  FAIL ') + name)
        ok = ok and good
    return ok


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        sys.exit(0 if self_test() else 1)
    root = Path(sys.argv[1])
    rec, rows = audit(root)
    import collections
    c = collections.Counter(r['state'] for r in rows)
    l = collections.Counter(r.get('limb') for r in rows if r['state'] == 'REPROVED')
    print('SCOPE: %s — %d bindings' % (root, len(rows)))
    print('  FRESH %d · REPROVED %d %s · IDENTITY %d' % (c['FRESH'], c['REPROVED'], dict(l), c['IDENTITY']))
    if '--write' in sys.argv:
        stamp = sys.argv[sys.argv.index('--write') + 1]
        a, b = apply(root, rec, rows, stamp)
        print('  written: %d re-proved, %d identity-pinned' % (a, b))
    else:
        print('  DRY RUN — re-run with --write <YYYY-MM-DD>')
