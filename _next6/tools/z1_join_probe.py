#!/usr/bin/env python3
"""Third and fourth instruments for §Z1/§Z2: which calendar reading is each
bare-estate-week pack actually authored against?

Six of the nine packs state a bare estate week ("W10", SCI_L_W10L1_...) and
nothing else, so the calendar is the only thing that can place them on the SoW
grid — and the two readings the estate has in use place them one cell apart.
60 of 132 rows therefore select a different SoW outcome depending on a ruling
that has not been made.

Neither instrument here reads a week number. Both consume the two candidate cells
the matrix already carries, so they share no reasoning with the join that
produced them; and they are keyed differently from each other:

  CONTENT   content-word overlap between what the deck TEACHES (title,
            objective, success criteria) and each candidate outcome.
  PRINTED   sequence similarity between the outcome the deck PRINTS FOR ITSELF
            (its sow-strip, or its manifest row) and each candidate outcome.
            This is the instrument that settled the ASDAN off-by-one 24/24.

They are reported side by side and a row where they disagree is printed as a
finding, not reconciled.

usage: z1_join_probe.py MATRIX.json [-v]
"""
import json, re, sys, collections, difflib

STOP = set('''a an the and or of to in for on with by from as at is are be been being this that these those
it its their his her they them we our you your i can will shall may might must do does did done
use uses using used one two three make makes making explain explains describe describes
lesson week pupils pupil learners learner students student'''.split())


def words(s):
    return set(w for w in re.findall(r"[a-z]+", (s or '').lower())
               if len(w) > 3 and w not in STOP)


def content_score(deck, outcome):
    o = words(outcome)
    if not o:
        return None
    return len(o & deck) / len(o)


def flat(s):
    return re.sub(r'[^a-z0-9 ]', ' ', re.sub(r'\s+', ' ', (s or '').lower())).strip()


def printed_score(printed, outcome):
    a, b = flat(printed), flat(outcome)
    if not a or not b:
        return None
    return difflib.SequenceMatcher(None, a, b).ratio()


# A margin floor is what separates a reading from a coin toss, and both floors
# below are MEASURED FROM THE NOISE RUN, not chosen against the answer.
#
# Red-proof 2 randomises the outcome text. Under it the two instruments still
# produce margins -- sequence similarity never returns exactly equal, so with no
# floor PRINTED declared GROW_Science 1/9 on text that means nothing. The floors
# are the 95th percentile of the margin distribution under that randomisation:
#
#            noise median   noise p95   REAL median
#   CONTENT      0.000        0.333        0.600
#   PRINTED      0.075        0.223        0.484
#
# so a floor at noise-p95 discards 95% of what noise can manufacture while
# sitting well below the real signal. A first draft used 0.15 for PRINTED, which
# is BELOW the noise p90 of 0.191 -- 9 of 41 randomised rows would have cleared
# it. That floor was wrong and is recorded here rather than quietly replaced.
MARGIN = {'CONTENT': 0.34, 'PRINTED': 0.23}


def winner(a, b, kind):
    """Only compare where BOTH candidates exist. A row with no cell under one
    reading is not evidence for the other reading -- it IS the conflict, and it
    is counted in its own column."""
    if a is None or b is None:
        return 'n/m'
    d = abs(a - b)
    if d < 1e-9:
        return 'tie@0' if a == 0 else 'weak'
    if d < MARGIN[kind]:
        return 'weak'
    return 'SOW' if a > b else 'CALENDAR'


def main(path, verbose):
    rows = json.load(open(path))
    tally = collections.defaultdict(lambda: collections.Counter())
    detail = collections.defaultdict(list)
    disagree = []

    for r in rows:
        if r.get('A_sourceWeek') or r.get('A_termLabel'):
            continue                  # names its own half-term; no calendar needed
        deck = words(' '.join(filter(None, [
            r.get('A_title'), r.get('A_objective'), r.get('A_outcome'),
            r.get('B_objective'), ' '.join(r.get('B_sc') or []), r.get('B_seqOutcome')])))
        printed = r.get('B_exactOutcome') or r.get('B_seqOutcome') or r.get('A_outcome')
        cells = {k: (r.get('sow_' + k) or {}).get('outcome') for k in ('SOW', 'CALENDAR')}

        wc = winner(content_score(deck, cells['SOW']),
                    content_score(deck, cells['CALENDAR']), 'CONTENT')
        wp = winner(printed_score(printed, cells['SOW']),
                    printed_score(printed, cells['CALENDAR']), 'PRINTED')
        p = r['pack']
        tally[p]['C:' + str(wc)] += 1
        tally[p]['P:' + str(wp)] += 1
        if wc in ('SOW', 'CALENDAR') and wp in ('SOW', 'CALENDAR') and wc != wp:
            disagree.append((p, r['id'], wc, wp))
        detail[p].append((r['id'], wc, wp, cells, printed))

    print("WHICH CALENDAR READING IS EACH BARE-WEEK PACK AUTHORED AGAINST?")
    print("CONTENT = what the deck teaches.  PRINTED = the outcome the deck prints for itself.")
    print()
    print("weak  = the two cells score within %.2f of each other; not a reading." % MARGIN['PRINTED'])
    print("tie@0 = NEITHER cell matches, so the calendar ruling cannot rescue the row.")
    print("n/m   = not measurable: no cell under one reading, or the deck prints no outcome.")
    print()
    print("%-20s %-34s %-34s" % ('', '--------- CONTENT ---------', '--------- PRINTED ---------'))
    print("%-20s %7s %8s %5s %6s %5s  %7s %8s %5s %6s %5s" % (
        'pack', 'SoW', 'calendar', 'weak', 'tie@0', 'n/m',
        'SoW', 'calendar', 'weak', 'tie@0', 'n/m'))
    for p in sorted(tally):
        t = tally[p]
        print("%-20s %7d %8d %5d %6d %5d  %7d %8d %5d %6d %5d" % (
            p, t['C:SOW'], t['C:CALENDAR'], t['C:weak'], t['C:tie@0'], t['C:n/m'],
            t['P:SOW'], t['P:CALENDAR'], t['P:weak'], t['P:tie@0'], t['P:n/m']))
    print()
    print("ROWS WHERE THE TWO INSTRUMENTS DISAGREE: %d" % len(disagree))
    for p, i, wc, wp in disagree:
        print("  %-20s %-8s content says %-9s printed says %s" % (p, i, wc, wp))

    if verbose:
        for p in sorted(detail):
            print('=' * 78)
            print(p)
            for id_, wc, wp, cells, printed in detail[p]:
                print("  %-10s content=%-9s printed=%-9s" % (id_, wc, wp))
                print("     deck prints  %s" % str(printed)[:74])
                print("     SoW cell     %s" % str(cells['SOW'])[:74])
                print("     cal cell     %s" % str(cells['CALENDAR'])[:74])


if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('-')]
    if not args:
        sys.exit(__doc__)
    main(args[0], '-v' in sys.argv)
