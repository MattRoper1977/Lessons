#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-Z · Z1 — join the two pack instruments to the SoW grid.

Produces one row per lesson with both derivations side by side, the SoW row each
maps to under each of the two calendar readings, and the raw material a verdict
needs. It assigns INSTRUMENT-SPLIT itself, because that is mechanical. It does
NOT assign ALIGNED/PARTIAL/MISALIGNED — that is a reading of meaning and is done
separately, against this file.

THE STRAND MAP IS COMMITTED, NOT INFERRED. Every pack names its strands
differently from the workbook, so the correspondence is written out here where it
can be argued with, rather than guessed at by string similarity at run time.
"""
import json
import os
import re
import sys

# pack -> (SoW lane, {pack strand token or None: SoW strand name})
# None means "this pack has one strand and the manifest does not name it".
STRAND_MAP = {
    'BUILD_ASDAN': ('BUILD', {
        'PfA: Independent Living, Careers & Vocational (ASDAN)':
            'PfA: Independent Living, Careers & Vocational (ASDAN)',
        'Enrichment Award: Junior/Young Duke + Community & Social Enterprise':
            'Enrichment Award: Junior/Young Duke + Community & Social Enterprise',
        'Design & Technology (ASDAN Foodwise, Textiles & Construction) – taster units':
            'Design & Technology (ASDAN Foodwise, Textiles & Construction) – taster units',
        'Community Project & Vocational (flexible – adapt to your local area)':
            'Community Project & Vocational (flexible – adapt to your local area)',
    }),
    'GROW_ASDAN': ('GROW', {
        'PEQ': 'PfA: Independence, Careers & Vocational (ASDAN PEQ E3–L1 + Employability)',
        'COMM': 'Community Project & Vocational (flexible – adapt to your local area)',
        'ENT': 'Enrichment Award: Young Duke + Community & Social Enterprise',
    }),
    'LAUNCH_ASDAN': ('LAUNCH', {
        'Employability & Careers': 'Employability & Careers (ASDAN Careers / Employability E2 to E3)',
        'Community Project, Enterprise & Vocational':
            'Community Project, Enterprise & Vocational (flexible – adapt to your local area)',
        'Independent Living Skills · Living Independently / Foodwise':
            'Independent Living Skills (ASDAN Living Independently / Foodwise)',
        'Personal Effectiveness · Team Working':
            'Personal Effectiveness (ASDAN PEQ – 6 units, E3 to L1)',
        'Vocational Pathway · Hospitality':
            'Vocational Pathway (ASDAN Hospitality / Gardening / Enterprise)',
    }),
    'BUILD_Science':     ('BUILD',  {None: 'Science (White Rose Science Year 3)'}),
    'GROW_Science':      ('GROW',   {None: 'Science (White Rose Science Year 5/6; Entry Level Science 8939)'}),
    'LAUNCH_Science':    ('LAUNCH', {None: 'Science (Edexcel GCSE Biology 1BI0 Foundation / Combined Science Foundation)'}),
    'BUILD_Humanities':  ('BUILD',  {None: 'World About Me (Humanities)'}),
    'GROW_Humanities':   ('GROW',   {None: 'Humanities: History & Geography (Kapow)'}),
    'LAUNCH_Humanities': ('LAUNCH', {None: 'Humanities, History & Geography (National Curriculum KS3/4)'}),
}

# THE TWO CALENDAR READINGS, both stated so neither is smuggled in as "the" one.
#
#   SOW      the workbooks' own grid: Autumn = Aut1 W1-7 + Aut2 W1-7 = 14 weeks.
#            Measured directly from all three workbooks, not assumed.
#   CALENDAR the repo calendar: _passpq/tools/l2k_plan.py BLOCKS
#            [("Aut1",1,8),("Aut2",9,15),...] = 15 autumn weeks, derived from real
#            dates ("W8 = w/c 19 Oct <- LAST WEEK OF AUT 1", Planning/*/README.txt).
#
# They disagree by exactly one week, and the disagreement is estate-wide rather
# than a LAUNCH peculiarity: all three workbooks carry the identical 7/7 autumn.
def estate_to_htwk(week, reading):
    """Estate week number -> (half-term, week-within-half-term)."""
    if reading == 'CALENDAR':
        return ('Aut1', week) if week <= 8 else ('Aut2', week - 8)
    return ('Aut1', week) if week <= 7 else ('Aut2', week - 7)


def norm(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()


def main(a_path, b_path, grid_path, out_path):
    A = [x for x in json.load(open(a_path)) if x['isLesson']]
    B = {x['file']: x for x in json.load(open(b_path))}
    G = json.load(open(grid_path))
    grid = G['rows']
    idx = {}
    for r in grid:
        idx[(r['lane'], r['strand'], r['ht'], r['week'])] = r

    rows = []
    for a in A:
        f = a['file']
        b = B.get(f, {})
        lane, smap = STRAND_MAP[a['pack']]
        sow_strand = smap.get(a['A_strand']) if a['A_strand'] in smap else smap.get(None)

        # --- instrument A: the estate week this lesson claims ---
        a_week = a['A_continuation'] or a['A_week_manifest']
        # --- instrument B: the estate week the DECK claims ---
        b_week = None
        for k in ('b_estateSeq', 'b_weekOf', 'b_brandWeekAlt'):
            if b.get(k):
                m = re.search(r'\d+', str(b[k]))
                if m:
                    b_week = int(m.group()); break
        if b_week is None and b.get('b_brandWeek'):
            # brandline gives a week WITHIN the half-term, plus the term
            t = (b.get('b_brandTerm') or '').upper()
            w = int(re.search(r'\d+', b['b_brandWeek']).group())
            b_week = w + 8 if '2' in t else w        # CALENDAR reading for display
            b_within = (('Aut2' if '2' in t else 'Aut1'), w)
        else:
            b_within = None
        if b_week is None and b.get('b_htwk'):
            m = re.match(r'(Aut|Spr|Sum)(\d)\s*[·.]\s*W(\d+)', b['b_htwk'], re.I)
            if m:
                b_within = ('%s%s' % (m.group(1).title(), m.group(2)), int(m.group(3)))

        # --- the SoW row ---
        #
        # JOIN ON WHAT THE PACK ACTUALLY CLAIMS. A pack that names its half-term
        # and week ("Autumn 2 · Week 1", source_week "Aut2·W1") is already
        # speaking the workbook's units, so deriving an estate week and mapping
        # it back through a disputed calendar introduces an off-by-one that the
        # pack never had.
        #
        # A first version did exactly that and it was wrong for 42 of 132 rows.
        # BUILD_ASDAN_A2_COMM_W1 claims Aut2·W1; via continuationWeek 9 and the
        # SoW reading it came out as Aut2·W2, so the lesson was judged against
        # "Practise a vocational skill our project needs" — which is what the
        # pack's own W2 deck teaches. GROW_ASDAN was worse: its bare week 1-6 was
        # read as an estate week, landing every deck in Aut1 instead of Aut2.
        # The second, independent verdict pass caught it by quoting the outcome
        # it had been handed; that is what the two-instrument rule is for.
        #
        # Only packs that state a BARE ESTATE WEEK (Science, Humanities) need the
        # calendar to place them, and for those the two readings are both kept.
        claim = None
        if a['A_source_week']:
            m = re.match(r'(Aut|Spr|Sum)(\d)\s*[·.]\s*W(\d+)', norm(a['A_source_week']), re.I)
            if m:
                claim = ('%s%s' % (m.group(1).title(), m.group(2)), int(m.group(3)))
        if claim is None and a['A_term'] and a['A_week_manifest'] is not None:
            t = norm(a['A_term'])
            m = re.match(r'(Autumn|Spring|Summer)\s*([12])', t, re.I)
            if m:
                claim = ('%s%s' % (m.group(1)[:3].title(), m.group(2)), int(a['A_week_manifest']))

        got = {}
        if claim:
            row = idx.get((lane, sow_strand, claim[0], claim[1]))
            got['SOW'] = got['CALENDAR'] = row
        else:
            for reading in ('SOW', 'CALENDAR'):
                ht, wk = estate_to_htwk(a_week, reading) if a_week else (None, None)
                got[reading] = idx.get((lane, sow_strand, ht, wk))

        # --- the deck's OWN claim about its half-term, if it makes one ---
        deck_htwk = None
        if b_within:
            deck_htwk = '%s·W%d' % b_within
        elif b.get('b_htwk'):
            deck_htwk = norm(b['b_htwk'])
        elif b.get('b_termLabel'):
            m = re.match(r'(Autumn|Spring|Summer)\s*([12])\s*[·.]\s*Week\s*(\d+)', norm(b['b_termLabel']), re.I)
            if m:
                deck_htwk = '%s%s·W%s' % (m.group(1)[:3].title(), m.group(2), m.group(3))

        manifest_htwk = norm(a['A_source_week']) if a['A_source_week'] else None
        if not manifest_htwk and a['A_term']:
            t = norm(a['A_term'])
            m = re.match(r'(Autumn|Spring|Summer)\s*([12])\s*[·.]\s*Week\s*(\d+)', t, re.I)
            if m:
                manifest_htwk = '%s%s·W%s' % (m.group(1)[:3].title(), m.group(2), m.group(3))
            else:
                # GROW_ASDAN states the half-term and the week in SEPARATE fields
                # ("term": "Autumn 2", "week": 1). Reading only a combined string
                # left 18 decks with nothing to compare against their brandline,
                # which is a comparator that cannot fire, not an agreement.
                m2 = re.match(r'(Autumn|Spring|Summer)\s*([12])$', t, re.I)
                if m2 and a['A_week_manifest'] is not None:
                    manifest_htwk = '%s%s·W%d' % (m2.group(1)[:3].title(), m2.group(2),
                                                  a['A_week_manifest'])

        # For packs that state only a bare estate week, the comparable quantity
        # is that week, not a half-term neither side names.
        split = None
        if a['A_week_manifest'] is not None and b_week is not None and not (deck_htwk and manifest_htwk):
            if int(a['A_week_manifest']) != int(b_week):
                split = 'estate week: manifest W%s vs deck W%s' % (a['A_week_manifest'], b_week)
        if deck_htwk and manifest_htwk:
            if norm(deck_htwk).replace(' ', '') != norm(manifest_htwk).replace(' ', ''):
                split = 'half-term/week: manifest %r vs deck %r' % (manifest_htwk, deck_htwk)
        if a['A_week_filename'] is not None and a['A_week_manifest'] is not None \
           and a['A_week_filename'] != a['A_week_manifest']:
            split = (split + ' ; ' if split else '') + \
                'filename W%s vs manifest W%s' % (a['A_week_filename'], a['A_week_manifest'])

        rows.append({
            'pack': a['pack'], 'lane': lane, 'family': a['family'],
            'file': f, 'base': a['base'], 'id': a['A_id'],
            'packStrand': a['A_strand'], 'sowStrand': sow_strand,
            'A_estateWeek': a_week, 'A_weekFilename': a['A_week_filename'],
            'A_weekManifest': a['A_week_manifest'], 'A_sourceWeek': a['A_source_week'],
            'A_termLabel': a['A_term'], 'A_title': a['A_title'],
            'A_objective': a['A_objective'], 'A_outcome': a['A_outcome'],
            'B_estateWeekGuess': b_week, 'B_htwk': deck_htwk,
            'B_brandline': b.get('b_brandline'),
            'B_exactOutcome': b.get('b_exactOutcome'), 'B_seqOutcome': b.get('b_seqOutcome'),
            'B_objective': b.get('b_objective'), 'B_sc': b.get('b_sc'),
            'B_enquiry': b.get('b_enquiry'), 'B_sowCell': b.get('b_sowCellFull'),
            'B_title': b.get('b_title'),
            'manifestHtwk': manifest_htwk, 'deckHtwk': deck_htwk,
            'instrumentSplit': split,
            'sow_SOW': got['SOW'], 'sow_CALENDAR': got['CALENDAR'],
        })
    json.dump(rows, open(out_path, 'w'), indent=1)
    return rows


if __name__ == '__main__':
    rows = main(*sys.argv[1:5])
    import collections
    print('%-20s %5s %10s %12s %12s %14s' % ('pack', 'n', 'strandOK', 'sowRow(SOW)', 'sowRow(CAL)', 'INSTRUMENT-SPLIT'))
    for p in sorted({r['pack'] for r in rows}):
        rs = [r for r in rows if r['pack'] == p]
        print('%-20s %5d %10d %12d %12d %14d' % (
            p, len(rs), sum(1 for r in rs if r['sowStrand']),
            sum(1 for r in rs if r['sow_SOW']), sum(1 for r in rs if r['sow_CALENDAR']),
            sum(1 for r in rs if r['instrumentSplit'])))
    print('%-20s %5d %10d %12d %12d %14d' % (
        'TOTAL', len(rows), sum(1 for r in rows if r['sowStrand']),
        sum(1 for r in rows if r['sow_SOW']), sum(1 for r in rows if r['sow_CALENDAR']),
        sum(1 for r in rows if r['instrumentSplit'])))
