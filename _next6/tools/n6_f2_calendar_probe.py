#!/usr/bin/env python3
"""N6-F §F2/D-A — which autumn calendar was a pack actually built to?

D-A is usually argued from labels. This argues it from content, which labels
cannot fake.

The two candidate calendars disagree by exactly one week:

  workbook   Aut1 = 7 weeks, so estate week 8 is Aut2 W1
  LA dates   Aut1 = 8 weeks, so estate week 9 is Aut2 W1

So for a lesson at estate week N, the SoW row it should deliver is Aut2 W(N-7)
under the first and Aut2 W(N-8) under the second. Those are different rows with
different topics. Score the lesson's text against the distinctive vocabulary of
each candidate row and the pack tells you which calendar it was written to.

Run against Science_Teesside/Launch/W8-W13_2026-27, the LAUNCH biology strand:

  14 of 18 lessons match the Aut1 = 8 mapping. NONE matches Aut1 = 7.

Four match neither, and three of those are the point rather than a miss: the
estate-week-8 lessons teach enzymes, which is Topic 1 and has no Aut2 row under
either reading. Under Aut1 = 8 they sit in Aut1 W8 — the week the workbook has
no row for. The pack put lessons in the orphan week.

The fourth, SCI_L_W9L3_Identical_Daughter_Cells_Do.html, is a scoring artefact
and not a counter-example: it is a mitosis lesson whose commonest words are
chromosome vocabulary, because identical daughter cells are explained in terms
of chromosome copies. Counting words cannot separate that from a DNA lesson.
Read, it belongs with the other two W9 surfaces at C39.

This does not settle D-A. It says what one pack did, and it is evidence a
ruling should see: six of that pack's MISALIGNED and PARTIAL verdicts in
SOW_MATRIX.md are correct against the workbook and disappear under the LA
calendar. They are the calendar question surfacing as content misalignment,
not six independent authoring errors.
"""
import re, os, sys, glob, html as H

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')

# distinctive vocabulary per LAUNCH-biology Aut2 row, keyed by Aut2 week number
MARKERS = {
    1: ("C39 mitosis & the cell cycle",
        ['mitosis', 'cell cycle', 'interphase', 'cytokinesis', 'prophase', 'anaphase']),
    2: ("C40 growth & stem cells",
        ['stem cell', 'differentiation', 'meristem', 'growth']),
    3: ("C41 stem-cell ethics (links RE/PSHE)",
        ['ethic', 'benefit and risk', 'consent', 'moral', 'uncertainty']),
    4: ("C42 DNA, genes & chromosomes",
        ['chromosome', 'double helix', 'base pair', 'nucleotide', 'genome']),
    5: ("C43 genetic cross (Punnett square)",
        ['punnett', 'genotype', 'phenotype', 'allele', 'heterozygous']),
}


def plain(p):
    return WS.sub(' ', H.unescape(TAG.sub(
        ' ', open(p, encoding='utf-8', errors='ignore').read()))).lower()


def main():
    pack = sys.argv[1] if len(sys.argv) > 1 \
        else 'Science_Teesside/Launch/W8-W13_2026-27'
    m7 = m8 = neither = 0
    print('%-46s %-5s %-28s %s' % ('lesson', 'estW', 'dominant topic', 'calendar'))
    for f in sorted(glob.glob(os.path.join(pack, '**', '*.html'), recursive=True)):
        b = os.path.basename(f)
        mm = re.search(r'_W(\d+)L', b)
        if not mm:
            continue
        ew = int(mm.group(1))
        t = plain(f)
        hits = {k: sum(t.count(x) for x in v[1]) for k, v in MARKERS.items()}
        best = max(hits, key=lambda k: hits[k])
        if not hits[best]:
            continue
        if best == ew - 7:
            tag, m7 = 'Aut1=7 (workbook)', m7 + 1
        elif best == ew - 8:
            tag, m8 = 'Aut1=8 (LA dates)', m8 + 1
        else:
            tag, neither = 'neither', neither + 1
        print('%-46s W%-4d %-28s %s' % (b[:46], ew, MARKERS[best][0][:28], tag))
    print('\nmatches Aut1 = 7 (workbook) : %d' % m7)
    print('matches Aut1 = 8 (LA dates) : %d' % m8)
    print('matches neither             : %d  '
          '(3 are estate week 8 — enzymes, Topic 1, no Aut2 row either way;'
          ' 1 is W9L3, a mitosis lesson scored onto chromosome vocabulary)'
          % neither)
    return 0


if __name__ == '__main__':
    sys.exit(main())
