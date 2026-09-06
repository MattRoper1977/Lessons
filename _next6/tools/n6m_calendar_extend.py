#!/usr/bin/env python3
"""ORDER N6-M §M1 — extend the D-A calendar test beyond LAUNCH Science.

THE METHOD. The two candidate calendars differ by exactly one week:

    workbook   Aut1 = 7 weeks  ->  estate week 8 is Aut2 W1
    LA dates   Aut1 = 8 weeks  ->  estate week 9 is Aut2 W1

So a lesson sitting at estate week N should deliver Aut2 W(N-7) under the first
and Aut2 W(N-8) under the second. Those are different rows asking for different
things. Score the lesson's own visible text against BOTH candidate rows and the
pack says which calendar it was written to. Content decides what labels cannot.

WHY IT IS SCORED THIS WAY. The score is the fraction of a candidate row's
content words that appear in the lesson, with a stop-list removed. Short SoW
outcomes share a lot of generic vocabulary ("record", "review", "project"), so a
bag-of-words score over the whole pack is too noisy to read — that was tried
first in N6-F and gave an inconclusive answer for every pack including the one
that is not remotely ambiguous. What works is scoring per lesson and reporting
the MARGIN between the two candidates, then counting only lessons where one
candidate beats the other by a stated margin. Lessons inside the margin are
reported as UNDECIDED rather than pushed to whichever side is ahead.

WHAT A RESULT MEANS. A pack that matches Aut1=8 was built to the LA term dates
and its labels are right. A pack that matches Aut1=7 was built to the workbook
grid. A split or undecided pack is a finding for the ruling, not a tie to break.

Usage: n6m_calendar_extend.py <pack-dir> <LANE> <strand-prefix> [week-regex]
"""
import collections, html as H, json, os, re, sys

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
STOP = set("""the a an and or of to in for my our with on at is are be as it that this from by
using use their they i can will your you what which when who how do does done not no yes one two
three make made makes take takes taken give gives given work works working""".split())
MARGIN = 0.10          # a candidate must beat the other by this much to count


def words(t):
    return {w for w in re.findall(r'[a-z]{4,}', t.lower()) if w not in STOP}


def visible(path):
    s = open(path, encoding='utf-8', errors='ignore').read()
    return WS.sub(' ', H.unescape(TAG.sub(' ', s))).lower()


def main():
    pack, lane, strand = sys.argv[1], sys.argv[2], sys.argv[3]
    wk_re = sys.argv[4] if len(sys.argv) > 4 else r'_W(\d+)'
    book = json.load(open('_next6/sow/%s.json' % lane))
    rows = {}
    for w in book['weekly']:
        if w['sheet'] == '%s Weekly - Autumn' % lane and w['strand'].startswith(strand):
            m = re.match(r'Aut2·W(\d+)', w['week'])
            if m:
                rows[int(m.group(1))] = w
    if not rows:
        print('no Aut2 rows for strand %r in %s' % (strand, lane))
        return 2

    tally = collections.Counter()
    print('%-52s %-5s %-22s %-22s %s'
          % ('lesson', 'estW', 'Aut1=7 candidate', 'Aut1=8 candidate', 'verdict'))
    for f in sorted(os.path.join(d, x) for d, _, fs in os.walk(pack) for x in fs
                    if x.endswith('.html')):
        b = os.path.basename(f)
        m = re.search(wk_re, b)
        if not m:
            continue
        ew = int(m.group(1))
        t = words(visible(f))
        s7 = rows.get(ew - 7)
        s8 = rows.get(ew - 8)
        def score(r):
            if not r:
                return None
            ow = words(r['outcome'])
            return (len(ow & t) / len(ow)) if ow else None
        v7, v8 = score(s7), score(s8)
        if v7 is None and v8 is None:
            continue
        a = -1 if v7 is None else v7
        c = -1 if v8 is None else v8
        if a - c > MARGIN:
            verdict, key = 'Aut1=7 (workbook)', 'w7'
        elif c - a > MARGIN:
            verdict, key = 'Aut1=8 (LA dates)', 'w8'
        else:
            verdict, key = 'undecided', 'und'
        tally[key] += 1
        f7 = ('C%d %.2f' % (s7['row'], v7)) if v7 is not None else '— (no row)'
        f8 = ('C%d %.2f' % (s8['row'], v8)) if v8 is not None else '— (no row)'
        print('%-52s W%-4d %-22s %-22s %s' % (b[:52], ew, f7, f8, verdict))

    print('\n  matches Aut1 = 7 (workbook) : %d' % tally['w7'])
    print('  matches Aut1 = 8 (LA dates) : %d' % tally['w8'])
    print('  undecided (inside %.0f%% margin): %d' % (MARGIN * 100, tally['und']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
