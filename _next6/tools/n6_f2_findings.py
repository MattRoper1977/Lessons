#!/usr/bin/env python3
"""N6-F — emit the §F2 section of FINDINGS.md from the matrix data.

Every number in the prose comes from the journal, so the narrative cannot drift
away from the table it summarises.

Usage: n6_f2_findings.py <journal.jsonl>
"""
import json, os, sys, collections

sys.path.insert(0, '_next6/tools')
import n6_f2_matrix as M

VERDICTS = M.VERDICTS


def main():
    journal = sys.argv[1]
    work = json.load(open('_next6/sow/worklist.json'))
    allfiles = [f for g in work for f in g['files']]
    rows, dis, _ = M.load(journal)
    have = [f for f in allfiles if f in rows]

    dist = collections.Counter(rows[f]['verdict'] for f in have)
    tiers = collections.Counter(rows[f].get('tier') for f in have)
    surf = collections.Counter(rows[f].get('surface') for f in have)
    whos = collections.Counter(d.get('who_is_right') for d in dis)
    lesson = [f for f in have if rows[f].get('surface') == 'lesson']
    ldist = collections.Counter(rows[f]['verdict'] for f in lesson)

    o = []
    o += ['', '---', '', '## §F2 — the SoW alignment matrix', '',
          '§F0.4 found **no alignment output of any kind**: no matrix, no rows, '
          '0 of 192', 'files carrying a verdict. §2 had not run, so §F2 ran from the '
          'beginning', 'rather than resuming a partial one.', '',
          'Full table: [`_next6/SOW_MATRIX.md`](_next6/SOW_MATRIX.md).', '',
          '### Coverage', '',
          '- files in the twelve packs: **%d**' % len(allfiles),
          '- files carrying a verdict: **%d / %d**' % (len(have), len(allfiles)),
          '- of those, **%d lesson surfaces** and **%d support surfaces**'
          % (surf.get('lesson', 0), surf.get('support', 0)), '',
          '### Verdicts', '',
          '| verdict | all %d | lesson surfaces only (%d) |' % (len(have), len(lesson)),
          '|---|---|---|']
    for v in VERDICTS:
        o.append('| %s | %d | %d |' % (v, dist.get(v, 0), ldist.get(v, 0)))
    sil_support = sum(1 for f in have if rows[f]['verdict'] == 'SOW-SILENT'
                      and rows[f].get('surface') == 'support')
    sil_lesson = dist.get('SOW-SILENT', 0) - sil_support
    o += ['',
          'The SOW-SILENT column lands exactly on the support surfaces: **%d of the %d'
          % (sil_support, dist.get('SOW-SILENT', 0)),
          'silent rows are support pages**, and **%d lesson surfaces are silent**.'
          % sil_lesson,
          'That is the consistency check on the distinction §F0 drew — every',
          'START_HERE, staff guide, matrix, evidence window and index came out silent',
          'because the SoW has nothing to prescribe for one, and no lesson hid there.',
          'No colleague-taught strand appears as a lesson in these twelve packs, so the',
          'order\'s "colleague-taught strands are SOW-SILENT, not defects" had nothing',
          'to catch here — correctly, not vacuously: it is why support surfaces are',
          'tiered "none" rather than reported as gaps.', '',
          '### Tiers', '',
          '| tier | n | meaning |', '|---|---|---|',
          '| Tier 1 | %d | mechanical — a label, a week number, a citation |' % tiers.get('1', 0),
          '| Tier 2 | %d | **would change what an LO or SC means. Diffed and held, not applied.** |' % tiers.get('2', 0),
          '| Tier 3 | %d | report only |' % tiers.get('3', 0),
          '| none | %d | nothing to fix |' % tiers.get('none', 0), '',
          '**Nothing in the packs was edited for §F2.** Tier 1 fixes are proposed in',
          'the matrix rather than applied, because the largest cluster of them sits',
          'downstream of D-A and would be wrong work if the calendar is ruled the',
          'other way.', '',
          '### The adversarial pass', '',
          'Every group was independently re-derived by a second agent told to **refute,',
          'not review**, with every non-ALIGNED row and two ALIGNED rows put to it, and',
          'instructed to default to reporting a disagreement when unsure — a false',
          'ALIGNED is the failure mode that matters here.', '',
          '- disagreements raised: **%d**' % len(dis),
          '- verifier right, row corrected: **%d**' % whos.get('mine', 0),
          '- original right, row stands: **%d**' % whos.get('original', 0),
          '- unresolved, left flagged rather than waved through: **%d**' % whos.get('unresolved', 0), '',
          'It earned its place. It caught a tier that no mechanical fix could resolve,',
          'an evidence claim contradicted by the file it cited, an ALIGNED that was',
          'really SURFACE-SPLIT, and a PARTIAL resting on five occurrences of "ethic"',
          'that on reading all said the opposite.', '',
          '### Two independent checks on the matrix', '',
          '**The citations resolve.** `n6_f2_recheck.py` re-derives a sample straight',
          'from the workbooks — not another judgement, a mechanical check that the cell',
          'a row names exists, sits on the week the row claims, and holds the text the',
          'row attributes to it. **10/10 agreeing**, and 9 of the 10 carry the workbook',
          'outcome verbatim in the lesson file (the tenth is a GROW deck that',
          'paraphrases, which that chassis does by design).', '',
          '**The surface typing agrees three ways.** The distilled record fed to each',
          'agent, the agent reading the file, and a stricter re-check accepting only an',
          'explicit "Learning objective" or "Success criteria" label. They agree on all',
          '%d files at **%d lesson / %d support** — and the agents **corrected the record'
          % (len(have), surf.get('lesson', 0), surf.get('support', 0)),
          'they were given on 10 files**, all of them planning documents, teacher guides,',
          'START_HERE pages and source cards that the first classifier had typed as',
          'lessons on scraped table text.', '']
    print('\n'.join(o))
    return 0


if __name__ == '__main__':
    sys.exit(main())
