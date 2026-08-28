#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ORDER N6-Z · Z1 — INSTRUMENT A: each lesson's claimed week and strand, from
its FILENAME and its pack MANIFEST.

Deliberately does not open the deck. Instrument B reads the rendered deck, and
the two are compared; a reader that quietly consulted both would make the
comparison meaningless.

Every pack states this differently, so there is an adapter per pack rather than
one clever guess:

  BUILD_ASDAN    manifest.lessons[]  week + continuationWeek + strandId
  GROW_ASDAN     manifest.lessons[]  week + strand + term
  LAUNCH_ASDAN   manifest is a bare LIST  pack_week + source_week + strand_code
  Science ×3     manifest.sequence[] week + kind + outcome + objective
  BUILD/LAUNCH Humanities  manifest.lessons[] week + objective + enquiry
  GROW Humanities          manifest-v3.1.json, same shape

The filename half is derived independently of the manifest, from the W-number in
the basename, so a manifest that disagrees with its own filenames is visible.
"""
import glob
import json
import os
import re
import sys

PACKS = [
    ('BUILD_ASDAN',       'BUILD',  'ASDAN',      'BUILD_ASDAN/Autumn2_W1-W6_2026-27'),
    ('GROW_ASDAN',        'GROW',   'ASDAN',      'GROW_ASDAN/Autumn2_W1-W6_2026-27'),
    ('LAUNCH_ASDAN',      'LAUNCH', 'ASDAN',      'LAUNCH_ASDAN/W7-W12_2026-27'),
    ('BUILD_Science',     'BUILD',  'Science',    'Science_Teesside/Build/W8-W13_2026-27'),
    ('GROW_Science',      'GROW',   'Science',    'Science_Teesside/Grow/W8-W13_2026-27'),
    ('LAUNCH_Science',    'LAUNCH', 'Science',    'Science_Teesside/Launch/W8-W13_2026-27'),
    ('BUILD_Humanities',  'BUILD',  'Humanities', 'Humanities_Teesside/BUILD_W9-W14_2026-27'),
    ('GROW_Humanities',   'GROW',   'Humanities', 'Humanities_Teesside/GROW_W9-W14_2026-27'),
    ('LAUNCH_Humanities', 'LAUNCH', 'Humanities', 'Humanities_Teesside/LAUNCH_W9-W14_2026-27'),
]

# Surfaces that are not lessons. Named exactly, anchored, and NOT as loose
# substrings — the first version of this list carried a bare `SOURCE`, which
# matched "People, Steps and Resources" and silently dropped a real GROW_ASDAN
# lesson deck from the population. The error was visible only because the
# classifier prints what it excluded; a count alone would have looked fine.
NOT_A_LESSON = re.compile(
    r'^(index\.html|START_HERE.*|STAFF_GUIDE\.html|STAFF_ONLY_.*|TEACHER_.*|'
    r'SCHEME_OF_WORK\.html|SOURCE_PROVENANCE_REGISTER\.html|SOURCE_REGISTER\.html|'
    r'.*_TEACHER_PLANNING_SOW\.html|'
    r'LOCAL_SOURCE_CARDS_.*|PRACTICALS_MATRIX\.html|PRINTABLE_RESOURCES\.html|'
    r'.*_EVIDENCE_WINDOW\.html|.*_SAME_DAY_EVIDENCE\.html|.*_PORTFOLIO_STUDIO\.html|'
    r'.*_Hub\.html|Resources_and_Tools\.html|VISUAL_UPGRADE_GUIDE\.html|'
    r'QA_REPORT\.html|README.*)$', re.I)

FN_WEEK = re.compile(r'_W(\d{1,2})[A-Z]?\d?_', re.I)


def manifest_of(root):
    for n in ('manifest.json', 'manifest-v3.1.json', 'manifest-v3.json'):
        p = os.path.join(root, n)
        if os.path.exists(p):
            return n, json.load(open(p, encoding='utf-8'))
    return None, None


def entries(root):
    """Normalise every manifest shape to {file, week, strand, source_week, obj}."""
    name, m = manifest_of(root)
    out = []
    if m is None:
        return name, out
    items = m if isinstance(m, list) else (m.get('lessons') or m.get('sequence') or [])
    for e in items:
        if not isinstance(e, dict):
            continue
        out.append({
            'mfile': e.get('file'),
            'mid': e.get('id'),
            'mweek': e.get('pack_week', e.get('week')),
            'mcontinuation': e.get('continuationWeek'),
            'msource_week': e.get('source_week'),
            'mstrand': e.get('strand') or e.get('strand_code') or e.get('strandId') or e.get('kind'),
            'mterm': e.get('term') or e.get('termLabel'),
            'mobjective': e.get('objective'),
            'moutcome': e.get('outcome') or e.get('sow_topic'),
            'mtitle': e.get('title'),
        })
    return name, out


def run():
    rows = []
    for key, lane, family, root in PACKS:
        mname, ents = entries(root)
        by_file = {}
        for e in ents:
            if e['mfile']:
                by_file[os.path.normpath(os.path.join(root, e['mfile']))] = e
        files = sorted(glob.glob(os.path.join(root, '**', '*.html'), recursive=True))
        for f in files:
            base = os.path.basename(f)
            is_lesson = not NOT_A_LESSON.search(base)
            fm = FN_WEEK.search('_' + base)
            e = by_file.get(os.path.normpath(f), {})
            rows.append({
                'pack': key, 'lane': lane, 'family': family, 'root': root,
                'file': f, 'base': base,
                'isLesson': bool(is_lesson),
                'manifestFile': mname,
                'inManifest': os.path.normpath(f) in by_file,
                'A_week_filename': int(fm.group(1)) if fm else None,
                'A_week_manifest': e.get('mweek'),
                'A_continuation': e.get('mcontinuation'),
                'A_source_week': e.get('msource_week'),
                'A_strand': e.get('mstrand'),
                'A_term': e.get('mterm'),
                'A_objective': e.get('mobjective'),
                'A_outcome': e.get('moutcome'),
                'A_title': e.get('mtitle'),
                'A_id': e.get('mid'),
            })
    return rows


if __name__ == '__main__':
    rows = run()
    lessons = [r for r in rows if r['isLesson']]
    print('%-20s %6s %8s %10s %12s' % ('pack', 'html', 'lessons', 'inManifest', 'fn==manifest'))
    for key, _, _, _ in PACKS:
        rs = [r for r in rows if r['pack'] == key]
        ls = [r for r in rs if r['isLesson']]
        inm = sum(1 for r in ls if r['inManifest'])
        agree = sum(1 for r in ls
                    if r['A_week_filename'] is not None and r['A_week_manifest'] is not None
                    and r['A_week_filename'] == r['A_week_manifest'])
        print('%-20s %6d %8d %10d %12s' % (key, len(rs), len(ls), inm, '%d/%d' % (agree, len(ls))))
    print('%-20s %6d %8d' % ('TOTAL', len(rows), len(lessons)))
    if len(sys.argv) > 1:
        json.dump(rows, open(sys.argv[1], 'w'), indent=1)
        print('-> %s' % sys.argv[1])
