#!/usr/bin/env python3
"""N6-F §F2 — build the alignment work list and the SoW slice each pack needs.

Twelve packs, 192 lesson files. Each pack is anchored to one lane's workbook and
one term, so an agent judging a lesson does not need all 506/702 weekly rows —
it needs its own lane's term. The slice is written per pack so a verdict can
name the exact sheet and row it was derived from.
"""
import json, os, glob, sys

PACKS = [
    # dir,                                        lane,    term,     packweeks
    ('BUILD_ASDAN/Autumn2_W1-W6_2026-27',         'BUILD',  'Autumn', 'Aut2·W1-W6'),
    ('GROW_ASDAN/Autumn2_W1-W6_2026-27',          'GROW',   'Autumn', 'Aut2·W1-W6'),
    ('LAUNCH_ASDAN/W7-W12_2026-27',               'LAUNCH', 'Autumn', 'pack W7-W12'),
    ('Science_Teesside/Build/W8-W13_2026-27',     'BUILD',  'Autumn', 'estate W8-W13'),
    ('Science_Teesside/Grow/W8-W13_2026-27',      'GROW',   'Autumn', 'estate W8-W13'),
    ('Science_Teesside/Launch/W8-W13_2026-27',    'LAUNCH', 'Autumn', 'estate W8-W13'),
    ('Humanities_Teesside/BUILD_W9-W14_2026-27',  'BUILD',  'Autumn', 'estate W9-W14'),
    ('Humanities_Teesside/GROW_W9-W14_2026-27',   'GROW',   'Autumn', 'estate W9-W14'),
    ('Humanities_Teesside/LAUNCH_W9-W14_2026-27', 'LAUNCH', 'Autumn', 'estate W9-W14'),
    ('Art_Teesside/Build/Spring2_2026-27',        'BUILD',  'Spring', 'Spr2·W1-W6'),
    ('Art_Teesside/Grow/Spring2_2026-27',         'GROW',   'Spring', 'Spr2·W1-W6'),
    ('Art_Teesside/Launch/Spring2_2026-27',       'LAUNCH', 'Spring', 'Spr2·W1-W6'),
]

CHUNK = 6   # lessons per verdict agent — small enough to judge each one properly


def main():
    outdir = '_next6/sow'
    os.makedirs(outdir, exist_ok=True)
    work = []
    total = 0
    for pdir, lane, term, packweeks in PACKS:
        files = sorted(glob.glob(os.path.join(pdir, '**', '*.html'), recursive=True))
        total += len(files)
        d = json.load(open(os.path.join(outdir, '%s.json' % lane)))
        rows = [w for w in d['weekly'] if w['term'] == term]
        grid = [g for g in d['grid'] if g['term'] == term]
        slug = pdir.replace('/', '__')
        md = ['# SoW slice · %s lane · %s term' % (lane, term),
              '', 'Workbook: `%s`' % d['workbook'],
              'sha256: `%s`' % d['sha256'],
              '', 'Pack: `%s`  (pack weeks: %s)' % (pdir, packweeks),
              '', '## Weekly outcomes (%d rows)' % len(rows), '',
              '| cell | strand | week | weekly outcome | programme alignment | accreditation |',
              '|---|---|---|---|---|---|']
        for w in rows:
            md.append('| %s!C%d | %s | %s | %s | %s | %s |' % (
                w['sheet'], w['row'], w['strand'], w['week'],
                w['outcome'].replace('|', '/').replace('\n', ' '),
                w['programme'].replace('|', '/').replace('\n', ' ')[:200],
                w['accreditation'].replace('|', '/').replace('\n', ' ')[:200]))
        md += ['', '## Half-term grid (%d rows)' % len(grid), '',
               '| cell | strand | weeks | theme | unit/topic | learning outcomes | qualification |',
               '|---|---|---|---|---|---|---|']
        for g in grid:
            md.append('| %s!%d | %s | %s | %s | %s | %s | %s |' % (
                g['sheet'], g['row'], g['strand'], g['weeks'], g['theme'],
                g['unit'].replace('|', '/').replace('\n', ' '),
                g['outcomes'].replace('|', '/').replace('\n', ' '),
                g['qualification'].replace('|', '/').replace('\n', ' ')))
        path = os.path.join(outdir, 'slice_%s.md' % slug)
        open(path, 'w').write('\n'.join(md))

        for i in range(0, len(files), CHUNK):
            work.append({'pack': pdir, 'lane': lane, 'term': term,
                         'packweeks': packweeks, 'slice': path,
                         'files': files[i:i + CHUNK],
                         'group': '%s#%d' % (os.path.basename(pdir), i // CHUNK + 1)})
    json.dump(work, open(os.path.join(outdir, 'worklist.json'), 'w'), indent=1)
    print('%d lesson files across %d packs -> %d verdict groups'
          % (total, len(PACKS), len(work)))
    for w in work:
        print('  %-34s %-7s %2d files  %s' % (w['group'], w['lane'], len(w['files']),
                                              os.path.basename(w['slice'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
