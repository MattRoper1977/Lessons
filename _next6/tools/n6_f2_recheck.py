#!/usr/bin/env python3
"""N6-F §F2 — re-derive a sample of matrix rows straight from the workbooks.

This is deliberately not another judgement. It is a mechanical check on the two
things a wrong row would get wrong first:

  the citation resolves   the cell a row names, e.g. 'BUILD Weekly - Autumn'!C166,
                          exists in the workbook and sits on the week the row claims

  the quote is real       the outcome text the row attributes to that cell is the
                          text the cell actually holds

It also reports, without judging, whether the lesson file contains the workbook
outcome verbatim. Some chassis quote the SoW line ("Exact SOW outcome:"), others
paraphrase, so a miss there is information rather than a defect.

A row can pass all of this and still carry the wrong verdict — that is what the
adversarial pass in the workflow is for. What this rules out is a row citing a
cell that says something else, which is the failure a plausible-looking matrix
hides best.

Usage: n6_f2_recheck.py <journal.jsonl> [n]
"""
import json, os, re, sys, html as H

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
CELL = re.compile(r"'([^']+)'!([A-Z]+)(\d+)")


def plain(s):
    return WS.sub(' ', H.unescape(TAG.sub(' ', s))).strip()


def main():
    journal = sys.argv[1]
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    books = {l: json.load(open('_next6/sow/%s.json' % l))
             for l in ('BUILD', 'GROW', 'LAUNCH')}
    index = {}
    for lane, d in books.items():
        for w in d['weekly']:
            index[(w['sheet'], w['row'])] = w

    rows = {}
    for line in open(journal):
        try:
            d = json.loads(line)
        except Exception:
            continue
        r = d.get('result')
        if isinstance(r, dict) and isinstance(r.get('rows'), list):
            for x in r['rows']:
                if isinstance(x, dict) and x.get('file'):
                    rows[x['file']] = x

    # sample across packs, and only rows that actually make a citation
    cited = [r for r in rows.values()
             if r.get('sow_cell') and CELL.match(r['sow_cell'])]
    cited.sort(key=lambda r: r['file'])
    sample, packs = [], set()
    for r in cited:
        p = r['file'].split('/')[0]
        if p not in packs:
            sample.append(r)
            packs.add(p)
    for r in cited:
        if len(sample) >= want:
            break
        if r not in sample:
            sample.append(r)
    sample = sample[:want]

    ok = 0
    bad = []
    print('%-52s %-9s %-9s %-8s %-8s %s'
          % ('file', 'cell wk', 'row wk', 'quote', 'week', 'verbatim in file'))
    for r in sample:
        m = CELL.match(r['sow_cell'])
        w = index.get((m.group(1), int(m.group(3))))
        if not w:
            bad.append((r['file'], 'cell %s does not resolve' % r['sow_cell']))
            continue
        claim = plain(r.get('sow_outcome') or '').lower().rstrip('.')
        real = plain(w['outcome']).lower().rstrip('.')
        qok = claim == real or claim in real or real in claim
        wok = w['week'] == r.get('sow_week')
        infile = real[:55] in plain(open(r['file'], encoding='utf-8',
                                         errors='ignore').read()).lower()
        print('%-52s %-9s %-9s %-8s %-8s %s'
              % (os.path.basename(r['file'])[:52], w['week'],
                 r.get('sow_week'), qok, wok, infile))
        if qok and wok:
            ok += 1
        else:
            bad.append((r['file'], 'claim=%r cell=%r' % (claim[:60], real[:60])))
    print('\nre-derived and agreeing: %d/%d' % (ok, len(sample)))
    for f, why in bad:
        print('  MISMATCH %s :: %s' % (os.path.basename(f), why))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
