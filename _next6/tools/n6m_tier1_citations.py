#!/usr/bin/env python3
"""ORDER N6-M §M2 — apply the Tier 1 citation fixes that are documentation only.

Every fix here adds a SoW cross-reference to a pack's CURRICULUM_ALIGNMENT.md.
Nothing touches a lesson file, a learning objective, a success criterion, a
timing, or anything a pupil does. The rows quoted are read out of the workbook
extract at run time, so the citation cannot drift from the instrument.

The section is appended under one marked heading and is idempotent: re-running
replaces the section rather than appending a second one.

What this tool deliberately does NOT do, and why. Eleven of the 32 Tier 1 rows
propose editing a citation string INSIDE a lesson — the `"sow"` field that
renders as `.sowline`, or LAUNCH_ASDAN's "SOW position" line. Those proposals are
given as examples ("e.g. ..."), not as exact replacement strings. Applying an
example verbatim would be authoring lesson-visible text under a Tier 1 label,
and Tier 1 is "a label, a week number, a strand name, a citation" — not new
prose in a pupil-facing surface. They are listed in FINDINGS as proposed and
held, with the workbook rows they would cite, so ruling them is a one-line job.
"""
import json, os, sys

MARK = '<!-- n6m-tier1-citations -->'
END = '<!-- /n6m-tier1-citations -->'

# pack -> (lane, sheet-term, strand prefix, weeks, note)
JOBS = [
    ('Art_Teesside/Build/Spring2_2026-27', 'BUILD', 'Spring', 'Creative Arts',
     'Spr2', 'The pack delivers a sculpture unit built from the repo\'s own '
     '`Art_Teesside/Spring2_Scheme_of_Work.html`. The SoW\'s Creative Arts block '
     'for this half term is drama and performance. The divergence is deliberate '
     'and declared here rather than left to be rediscovered.'),
    ('Art_Teesside/Grow/Spring2_2026-27', 'GROW', 'Spring', 'Creative Arts',
     'Spr2', 'As BUILD: the sculpture unit follows the repo\'s committed Spring 2 '
     'scheme, not the SoW\'s drama block. Declared, not accidental.'),
    ('Art_Teesside/Launch/Spring2_2026-27', 'LAUNCH', 'Spring', 'Creative Arts',
     'Spr2', 'As BUILD and GROW. The Arts Award rung (Silver) matches the Pathway '
     'Ladder row 11 for LAUNCH and is not affected by the divergence.'),
    ('Humanities_Teesside/BUILD_W9-W14_2026-27', 'BUILD', 'Autumn',
     'World About Me', 'Aut2',
     'Estate weeks 9-14 map to Aut2 W2-W7 on the workbook\'s own numbering. The '
     'pack teaches a Tees-valley local-history sequence where the SoW names '
     'festivals, beliefs and light; the departure is declared in each lesson\'s '
     'Sequence intent and is cross-referenced here.'),
    ('Science_Teesside/Build/W8-W13_2026-27', 'BUILD', 'Autumn', 'Science',
     'Aut2', 'C41 (Aut2-W3, rock hardness and permeability) is taught across TWO '
     'estate weeks, W10 (hardness) and W11 (permeability). That displaces the '
     'remaining rows by one: estate W12 delivers C42 (Aut2-W4). The split is the '
     'pack\'s design, not a gap, and this is the record of it.'),
]


def rows_for(lane, term, strand, wk):
    d = json.load(open('_next6/sow/%s.json' % lane))
    out = []
    for w in d['weekly']:
        if w['sheet'] == '%s Weekly - %s' % (lane, term) \
                and w['strand'].startswith(strand) and w['week'].startswith(wk):
            out.append(w)
    return sorted(out, key=lambda w: w['row'])


def main():
    n = 0
    for pack, lane, term, strand, wk, note in JOBS:
        path = os.path.join(pack, 'CURRICULUM_ALIGNMENT.md')
        if not os.path.exists(path):
            print('  SKIP (no alignment doc) %s' % pack)
            continue
        rs = rows_for(lane, term, strand, wk)
        if not rs:
            print('  SKIP (no SoW rows matched) %s' % pack)
            continue
        body = [MARK, '',
                '## SoW cross-reference (ORDER N6-M §M2, Tier 1 — citation only)',
                '',
                'Added so the relationship to the scheme of work is on the record '
                'rather than inferred. **No learning objective, success criterion, '
                'timing or task changed.**', '',
                'Instrument: `%s`' % json.load(open('_next6/sow/%s.json' % lane))['workbook'],
                '', note, '',
                '| SoW cell | week | outcome as written in the workbook |',
                '|---|---|---|']
        for w in rs:
            body.append('| `\'%s\'!C%d` | %s | %s |'
                        % (w['sheet'], w['row'], w['week'],
                           w['outcome'].replace('|', '/')))
        body += ['', END, '']
        s = open(path, encoding='utf-8').read()
        if MARK in s:
            s = s[:s.index(MARK)] + s[s.index(END) + len(END):]
        s = s.rstrip('\n') + '\n\n' + '\n'.join(body)
        open(path, 'w', encoding='utf-8').write(s)
        print('  %-46s + %d SoW rows' % (pack, len(rs)))
        n += 1
    print('alignment docs updated: %d' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
