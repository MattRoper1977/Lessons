#!/usr/bin/env python3
"""G-vocab -- cross-surface vocabulary parity, ADDENDUM 3 v3 (2026-09-21).

A lesson carries its vocabulary on three surfaces a pupil can meet: the on-screen organiser
dialog, the print organiser, and the Knowledge Organiser file. The three must agree on
  (1) the SET OF TERMS  -- a term on one surface and absent on another is a defect, and
  (2) the DEFINITION of every term they share.

Why (1) is a separate clause: the withdrawn LAUNCH generation carried a wrong first row on
screen ("sustainability" with a definition belonging to no term) that the print and KO did
not carry at all. A by-word comparison had nothing to compare it with and passed it. Set
equality is what sees a row that exists on one surface only.

Usage: scan_gvocab.py <pack-root>... [--json OUT]        exit 1 if any lesson is flagged
       scan_gvocab.py --self-test <root>                  the red proofs, on the bytes named
"""
import sys, json
from pathlib import Path
import lxml.html as lh

SCREEN = '//dialog[@id="organiser-dialog"]//table'
PRINT = '//*[@id="print-organiser"]//table'
KO = '//table'
HEAD = ('word', 'term', 'vocabulary')


def vocab(doc, xp):
    """A Word/Meaning table, or -- when a surface carries none -- the "Words to use" prose form
    some Knowledge Organisers use: one line per word, "word: meaning". Read from the file's own
    structure either way; never guessed."""
    out = {}
    if xp == KO and not doc.xpath('//table'):
        for h in doc.xpath('//h2[contains(normalize-space(.), "Words to use")]'):
            n = h.getnext()
            while n is not None and n.tag not in ('h1', 'h2'):
                txt = ' '.join(n.text_content().split())
                if ':' in txt:
                    w, m = txt.split(':', 1)
                    if w.strip() and m.strip():
                        out[w.strip().lower()] = m.strip()
                n = n.getnext()
        return out
    for t in doc.xpath(xp):
        rows = [[' '.join(c.text_content().split()) for c in r.xpath('./th|./td')] for r in t.xpath('.//tr')]
        if not rows or len(rows[0]) < 2 or rows[0][0].strip().lower() not in HEAD:
            continue
        for r in rows[1:]:
            if len(r) >= 2 and r[0]:
                out[r[0].strip().lower()] = r[1].strip()
    return out


def judge(lesson_path: Path):
    doc = lh.fromstring(lesson_path.read_bytes())
    surfaces = {'screen': vocab(doc, SCREEN), 'print': vocab(doc, PRINT)}
    kof = sorted(lesson_path.parent.glob('*Knowledge_Organiser.html'))
    surfaces['ko'] = vocab(lh.fromstring(kof[0].read_bytes()), KO) if kof else None
    present = {k: v for k, v in surfaces.items() if v is not None}
    defects = []
    sets = {k: set(v) for k, v in present.items()}
    union = set().union(*sets.values()) if sets else set()
    for term in sorted(union):
        where = {k for k, s in sets.items() if term in s}
        if where != set(sets):                                   # (1) a term missing on a surface
            defects.append({'term': term, 'kind': 'term-set',
                            'present_on': sorted(where), 'absent_on': sorted(set(sets) - where)})
            continue
        defs = {k: present[k][term] for k in present}
        if len(set(defs.values())) > 1:                          # (2) shared term, unequal definition
            defects.append({'term': term, 'kind': 'definition', **defs})
    return {'lesson': lesson_path.stem.replace('_Lesson', ''),
            'surfaces': {k: (len(v) if v is not None else None) for k, v in surfaces.items()},
            'defects': defects}


def run(roots):
    rows = []
    for root in roots:
        for lf in sorted(Path(root).rglob('*_SU1_W0?_Lesson.html')):
            rows.append(judge(lf))
    flagged = [r for r in rows if r['defects']]
    return {'lessons': len(rows), 'clean': len(rows) - len(flagged), 'flagged': len(flagged), 'rows': rows}


def self_test(root: Path):
    """Red proofs on the bytes the ruling names. Each must FLAG; the seeded control must flag
    exactly what was seeded; and a clean pair must pass. Refuses to report PASS on a fixture
    that is absent -- 'did not run' is never a pass."""
    checks = []
    v1 = root / 'withdrawn/su1l/HUM_Summer_1_LAUNCH_Final'
    v2 = root / 'a3v2/LAUNCH/HUM_Summer_1_LAUNCH_Final'
    for name, p, want in (('v1 (withdrawn) LAUNCH: all six lessons flag', v1, 6),
                          ('v2 LAUNCH: all six lessons flag', v2, 6)):
        if not p.exists():
            checks.append((name + ' -- FIXTURE ABSENT, not run', False)); continue
        r = run([p])
        kinds = {x['lesson']: sorted({d['kind'] for d in x['defects']}) for x in r['rows'] if x['defects']}
        checks.append((name + ' (%d/%d, kinds %s)' % (r['flagged'], r['lessons'], kinds), r['flagged'] == want))
        w01 = next((x for x in r['rows'] if x['lesson'] == 'LAUNCH_SU1_W01'), None)
        checks.append(('  W01 flags provenance by DEFINITION',
                       bool(w01) and any(d['term'] == 'provenance' and d['kind'] == 'definition' for d in w01['defects'])))
        w03 = next((x for x in r['rows'] if x['lesson'] == 'LAUNCH_SU1_W03'), None)
        checks.append(('  W03 flags a screen-only term by TERM-SET (the row a by-word check cannot see)',
                       bool(w03) and any(d['kind'] == 'term-set' and d['present_on'] == ['screen'] for d in w03['defects'])))
    # seeded control on clean bytes: one definition changed on one surface must flag that term only
    v3 = root / 'a3v3/LAUNCH/HUM_Summer_1_LAUNCH_Final'
    if v3.exists():
        import tempfile, shutil
        lf = next(v3.rglob('LAUNCH_SU1_W04_Lesson.html'))
        tmp = Path(tempfile.mkdtemp()) / 'W04'; shutil.copytree(lf.parent, tmp)
        base = judge(tmp / lf.name)
        checks.append(('v3 W04 is clean before seeding', not base['defects']))
        # seed through the PARSER: the first definition cell of the screen organiser table
        doc = lh.fromstring((tmp / lf.name).read_bytes())
        cell = None
        for t in doc.xpath(SCREEN):
            rows = t.xpath('.//tr')
            if len(rows) > 1:
                tds = rows[1].xpath('./td')
                if len(tds) >= 2: cell = tds[1]; break
        if cell is not None:
            for ch in list(cell): cell.remove(ch)
            cell.text = 'SEEDED WRONG DEFINITION'
            (tmp / lf.name).write_bytes(lh.tostring(doc, encoding='utf-8', doctype='<!doctype html>'))
            r = judge(tmp / lf.name)
            checks.append(('seeded control: exactly one definition defect, on screen only',
                           len(r['defects']) == 1 and r['defects'][0]['kind'] == 'definition'
                           and r['defects'][0]['screen'] == 'SEEDED WRONG DEFINITION'))
        else:
            checks.append(('seeded control: could not locate the screen organiser cell -- not run', False))
    else:
        checks.append(('v3 LAUNCH fixture ABSENT -- seeded control not run', False))
    ok = True
    for name, good in checks:
        print(('  PASS ' if good else '  FAIL ') + name); ok = ok and good
    return ok


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--self-test':
        sys.exit(0 if self_test(Path(args[1])) else 1)
    out = None
    if '--json' in args:
        i = args.index('--json'); out = args[i + 1]; args = args[:i] + args[i + 2:]
    res = run(args)
    print(json.dumps({k: v for k, v in res.items() if k != 'rows'}))
    for r in res['rows']:
        if r['defects']:
            print('  FLAG', r['lesson'], json.dumps(r['defects'], ensure_ascii=False)[:300])
    if out:
        Path(out).write_text(json.dumps(res, indent=1, ensure_ascii=False))
    sys.exit(1 if res['flagged'] else 0)
