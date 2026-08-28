#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-Z · Z2 — the one-week conflict, and the cost of each reading.

TWO INSTRUMENTS, BOTH MEASURED, NEITHER ASSUMED:

  SoW grid       All three workbooks: Autumn = Aut1 W1-W7 + Aut2 W1-W7 = 14 weeks.
                 Read directly from the three .xlsx by z1_sow_grid.py. The
                 half-term-level rows agree ("Aut 1 · Sep to Oct (7 wks)").
  Repo calendar  _passpq/tools/l2k_plan.py BLOCKS = [("Aut1",1,8),("Aut2",9,15),...]
                 = 15 autumn weeks, and Planning/*/README.txt says why:
                 "Aut 1 = 8 weeks (W1 1 Sep -> W8 19 Oct)", "W8 = w/c 19 Oct
                 <- LAST WEEK OF AUT 1", "The LA calendar confirms the 8-week Aut 1".
                 _assert_calendar() passes on it.

They disagree by exactly one week, and the disagreement is ESTATE-WIDE, not a
LAUNCH peculiarity: all three workbooks carry the identical 7/7 autumn. §Z2's
decision rule 1 (SoW governs where its grid is explicit) and rule 2 (repo
calendar governs where the SoW is silent) therefore both fire and point opposite
ways, which is rule 3: record both, change nothing, put it to Matt.

THE PACKS DO NOT ALL SPEAK THE SAME UNITS, and conflating them is how a first
pass at this got the cost wrong:

  half-term-claiming   BUILD_ASDAN  "Autumn 2 · Week n"  (+ continuationWeek 9-14)
                       GROW_ASDAN   term "Autumn 2" + week n
                       LAUNCH_ASDAN source_week "Aut2·Wn" + pack_week 7-12
  estate-week-claiming Science x3   bare week 8-13
                       Humanities x3 bare week 9-14

A pack that claims a half-term week says nothing about which estate week that is
— that mapping IS the disputed quantity. A pack that claims an estate week says
nothing about which half-term it falls in. So the two classes move under
opposite readings, and the table below states each in its own units.
"""
import collections
import json
import sys

# estate week -> (half-term, week within it), under each reading
def to_ht(week, reading):
    if reading == 'CALENDAR':
        return ('Aut1', week) if week <= 8 else ('Aut2', week - 8)
    return ('Aut1', week) if week <= 7 else ('Aut2', week - 7)


# (half-term, week within it) -> estate week, under each reading
def to_estate(ht, wk, reading):
    base = 8 if reading == 'CALENDAR' else 7
    return wk if ht == 'Aut1' else base + wk


CLAIMS = {
    # pack: (kind, lane, [(ht, wk)] or [estate weeks])
    'BUILD_ASDAN':       ('half-term', 'BUILD',  [('Aut2', n) for n in range(1, 7)]),
    'GROW_ASDAN':        ('half-term', 'GROW',   [('Aut2', n) for n in range(1, 7)]),
    'LAUNCH_ASDAN':      ('half-term', 'LAUNCH', [('Aut1', 7)] + [('Aut2', n) for n in range(1, 6)]),
    'BUILD_Science':     ('estate',    'BUILD',  list(range(8, 14))),
    'GROW_Science':      ('estate',    'GROW',   list(range(8, 14))),
    'LAUNCH_Science':    ('estate',    'LAUNCH', list(range(8, 14))),
    'BUILD_Humanities':  ('estate',    'BUILD',  list(range(9, 15))),
    'GROW_Humanities':   ('estate',    'GROW',   list(range(9, 15))),
    'LAUNCH_Humanities': ('estate',    'LAUNCH', list(range(9, 15))),
}
LESSONS = {'BUILD_ASDAN': 24, 'GROW_ASDAN': 18, 'LAUNCH_ASDAN': 30,
           'BUILD_Science': 12, 'GROW_Science': 12, 'LAUNCH_Science': 18,
           'BUILD_Humanities': 6, 'GROW_Humanities': 6, 'LAUNCH_Humanities': 6}


def main(gridpath):
    G = json.load(open(gridpath))
    have = collections.defaultdict(set)
    for r in G['rows']:
        have[r['lane']].add((r['ht'], r['week']))

    print('%-19s %-6s %-20s %-22s %-22s' % ('pack', 'claims', 'its own units', 'SOW reading implies', 'CALENDAR reading implies'))
    print('-' * 96)
    moves = {'SOW': [], 'CALENDAR': []}
    orphan = {'SOW': [], 'CALENDAR': []}
    for p, (kind, lane, cl) in CLAIMS.items():
        if kind == 'half-term':
            own = '%s·W%d..%s·W%d' % (cl[0][0], cl[0][1], cl[-1][0], cl[-1][1])
            s = [to_estate(h, w, 'SOW') for h, w in cl]
            c = [to_estate(h, w, 'CALENDAR') for h, w in cl]
            simp = 'estate W%d..W%d' % (min(s), max(s))
            cimp = 'estate W%d..W%d' % (min(c), max(c))
            # a half-term claim always resolves to a real SoW cell; what moves is
            # the estate week it occupies
            if s != c:
                moves['SOW'].append(p) if False else None
        else:
            own = 'estate W%d..W%d' % (min(cl), max(cl))
            s = [to_ht(w, 'SOW') for w in cl]
            c = [to_ht(w, 'CALENDAR') for w in cl]
            simp = '%s·W%d..%s·W%d' % (s[0][0], s[0][1], s[-1][0], s[-1][1])
            cimp = '%s·W%d..%s·W%d' % (c[0][0], c[0][1], c[-1][0], c[-1][1])
            for tag, seq in (('SOW', s), ('CALENDAR', c)):
                miss = [x for x in seq if x not in have[lane]]
                if miss:
                    orphan[tag].append((p, miss))
        print('%-19s %-6s %-20s %-22s %-22s' % (p, kind, own, simp, cimp))

    print()
    print('WHAT EACH READING COSTS')
    print()
    for tag in ('SOW', 'CALENDAR'):
        print('  Reading %s:' % tag)
        if orphan[tag]:
            n = 0
            for p, miss in orphan[tag]:
                n += LESSONS[p] // len(CLAIMS[p][2]) * len(miss)
                print('     %-19s %s has no SoW cell -> %d lesson(s) unmapped'
                      % (p, ', '.join('%s·W%d' % m for m in miss),
                         LESSONS[p] // len(CLAIMS[p][2]) * len(miss)))
            print('     total lessons with no SoW row: %d' % n)
        else:
            print('     every estate-week pack lands on a real SoW cell')
        # which half-term-claiming packs sit at a different estate week
        shifted = []
        for p, (kind, lane, cl) in CLAIMS.items():
            if kind != 'half-term':
                continue
            s = [to_estate(h, w, 'SOW') for h, w in cl]
            c = [to_estate(h, w, 'CALENDAR') for h, w in cl]
            if tag == 'SOW' and s != c:
                shifted.append('%s -> estate W%d..W%d' % (p, min(s), max(s)))
            if tag == 'CALENDAR' and s != c:
                shifted.append('%s -> estate W%d..W%d' % (p, min(c), max(c)))
        for x in shifted:
            print('     half-term pack re-seats: %s' % x)
    print()
    print('  BUILD_ASDAN states BOTH: "Autumn 2 · Week n" AND continuationWeek 9-14.')
    print('  Those two are consistent ONLY under the CALENDAR reading (Aut2·W1 = estate W9).')
    print('  Under the SOW reading Aut2·W1 = estate W8, so BUILD_ASDAN\'s own manifest')
    print('  would contradict itself. That is the single sharpest piece of evidence in')
    print('  the packs, and it favours the repo calendar.')
    print()
    print('  LAUNCH_ASDAN states BOTH: pack_week 7-12 AND source_week Aut1·W7, Aut2·W1-W5.')
    print('  pack_week 8 = Aut2·W1 is consistent ONLY under the SOW reading (Aut1 ends W7).')
    print('  So the two ASDAN packs disagree with each other, in their own manifests,')
    print('  and each is internally consistent under a different reading. Neither pack')
    print('  is wrong on its own terms; the estate has two conventions in use at once.')


if __name__ == '__main__':
    main(sys.argv[1])
