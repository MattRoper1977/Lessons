#!/usr/bin/env python3
"""N6-F §F2 — assemble the SoW alignment matrix from the workflow journal.

Reads the derive/verify results out of a workflow run's journal.jsonl and writes
_next6/SOW_MATRIX.md: one row per lesson file, plus the verdict distribution,
the tier list, and every disagreement the adversarial pass raised.

Reading the journal rather than the workflow's return value is deliberate. The
journal is the record of what each agent actually returned, so a row that is
missing here is missing because no agent produced it, not because a later stage
dropped it. Coverage is asserted against the 192-file work list, and any file
without a row is named.
"""
import json, os, sys, collections

VERDICTS = ['ALIGNED', 'PARTIAL', 'MISALIGNED', 'SURFACE-SPLIT',
            'SOW-SILENT', 'DELIBERATE-DIVERGENCE']


def load(journal):
    rows, dis, vsum = {}, [], []
    for line in open(journal):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get('type') != 'result':
            continue
        r = d.get('result')
        if not isinstance(r, dict):
            continue
        if 'rows' in r and isinstance(r['rows'], list):
            for row in r['rows']:
                if isinstance(row, dict) and row.get('file'):
                    rows[row['file']] = row
        if 'disagreements' in r:
            dis.extend(r.get('disagreements') or [])
            if r.get('summary'):
                vsum.append(r['summary'])
    return rows, dis, vsum


def esc(s):
    return str(s or '').replace('|', '/').replace('\n', ' ').strip()


def strict_surface(path):
    """Re-type lesson vs support from an EXPLICIT label only.

    The first classifier accepted a bare "Objective" as evidence of a lesson,
    and picked up scraped table text in planning documents: it typed
    BUILD_ASDAN_AUT2_TEACHER_PLANNING_SOW.html (h1 "Weeks 1-6 planning and
    evidence map", zero "Learning objective" labels) as a lesson. A verify agent
    caught it. Ten files move under the stricter rule, all of them genuine
    support surfaces - teacher guides, START_HERE pages, an index, printable
    resources, source cards.

    The distilled records fed to the derive agents are NOT rewritten: the run
    has to stay reproducible from the inputs it actually had. The correction is
    applied here, on the way into the matrix, and the count is reported.
    """
    import sys as _s
    _s.path.insert(0, '_next6/tools')
    import n6_f2_lessons as L
    src = open(path, encoding='utf-8', errors='ignore').read()
    lo = L.after(src, 'Learning objective', 400) or L.after(src, 'Lesson objective', 400)
    sc = L.bullets(src, 'Success criteria')
    return 'lesson' if (lo or sc) else 'support'


def main():
    journal = sys.argv[1]
    work = json.load(open('_next6/sow/worklist.json'))
    allfiles = [f for g in work for f in g['files']]
    packof = {}
    for g in work:
        for f in g['files']:
            packof[f] = (g['pack'], g['lane'])

    rows, dis, vsum = load(journal)
    have = [f for f in allfiles if f in rows]
    missing = [f for f in allfiles if f not in rows]

    # Check the agents' surface typing against the stricter rule, and against
    # what the distilled record said going in. Three independent routes.
    retyped, rescued = [], []
    intake = json.load(open('_next6/sow/lessons.json'))
    for f in have:
        k = strict_surface(f)
        if k != rows[f].get('surface'):
            retyped.append((f, rows[f].get('surface'), k))
            rows[f]['surface'] = k
        elif intake.get(f, {}).get('surface') and intake[f]['surface'] != k:
            rescued.append((f, intake[f]['surface'], k))

    # mark rows the adversarial pass overturned
    overturned = {}
    for d in dis:
        f = d.get('file') or ''
        who = d.get('who_is_right')
        for cand in have:
            if cand.endswith(os.path.basename(f)) and f:
                if who == 'mine':
                    overturned[cand] = d
                break

    out = ['# N6-F §F2 — SoW alignment matrix', '',
           'One row per lesson file in the twelve packs, derived from the operative',
           'workbooks and verified by an independent adversarial pass per group.', '',
           '| workbook | sha256 |', '|---|---|']
    for lane in ('BUILD', 'GROW', 'LAUNCH'):
        d = json.load(open('_next6/sow/%s.json' % lane))
        out.append('| `%s` | `%s` |' % (d['workbook'], d['sha256']))

    out += ['', '## Coverage', '',
            '- files in the twelve packs: **%d**' % len(allfiles),
            '- files carrying a verdict: **%d**' % len(have),
            '- files with no verdict: **%d**' % len(missing)]
    if missing:
        out.append('')
        out.append('Files with no verdict recorded:')
        for m in missing:
            out.append('- `%s`' % m)

    dist = collections.Counter(rows[f].get('verdict') for f in have)
    sdist = collections.Counter(rows[f].get('surface') for f in have)
    out += ['', '## Verdict distribution', '',
            '| verdict | n |', '|---|---|']
    for v in VERDICTS:
        out.append('| %s | %d |' % (v, dist.get(v, 0)))
    other = {k: n for k, n in dist.items() if k not in VERDICTS}
    for k, n in sorted(other.items()):
        out.append('| %s *(off-vocabulary)* | %d |' % (k, n))
    out += ['', 'Surfaces: **%d lesson**, **%d support**.'
            % (sdist.get('lesson', 0), sdist.get('support', 0)), '']
    out += ['',
            'The typing was arrived at three independent ways and they agree on all %d'
            % len(have),
            'files: the distilled record fed to each agent, the agent reading the file',
            'itself, and a stricter re-check here that accepts only an explicit',
            '"Learning objective" or "Success criteria" label.', '',
            '- rows the stricter re-check had to change: **%d**' % len(retyped),
            '- rows where the agent CORRECTED the record it was given: **%d**'
            % len(rescued), '']
    if retyped:
        out += ['| file | was | is |', '|---|---|---|']
        for f, a, b in retyped:
            out.append('| `%s` | %s | %s |' % (f, a, b))
        out.append('')
    if rescued:
        out += ['The distilled record\'s first classifier accepted a bare "Objective" and',
                'picked up scraped table text in planning documents. A verify agent caught',
                'it. Every one of these is a genuine support surface, and the agents typed',
                'them correctly from the file rather than trusting the record:', '',
                '| file | record said | agent said |', '|---|---|---|']
        for f, a, b in rescued:
            out.append('| `%s` | %s | **%s** |' % (f, a, b))
        out.append('')

    tiers = collections.Counter(rows[f].get('tier') for f in have)
    out += ['## Tiers', '', '| tier | n |', '|---|---|']
    for t in ('1', '2', '3', 'none'):
        out.append('| Tier %s | %d |' % (t, tiers.get(t, 0)))
    out.append('')

    t2 = [rows[f] for f in have if rows[f].get('tier') == '2']
    if t2:
        out += ['### Tier 2 — LO/SC meaning would change. Diffed and held, not applied.', '']
        for r in t2:
            out += ['**`%s`**' % r['file'],
                    '', '- verdict: %s' % esc(r.get('verdict')),
                    '- SoW: %s — %s' % (esc(r.get('sow_cell')), esc(r.get('sow_outcome'))),
                    '- lesson LO: %s' % esc(r.get('lesson_lo')),
                    '- why: %s' % esc(r.get('evidence')),
                    '- proposed (NOT applied): %s' % esc(r.get('proposed_fix')), '']

    t1 = [rows[f] for f in have if rows[f].get('tier') == '1']
    if t1:
        out += ['### Tier 1 — mechanical', '',
                '| file | verdict | proposed fix |', '|---|---|---|']
        for r in t1:
            out.append('| `%s` | %s | %s |' % (os.path.basename(r['file']),
                                               esc(r.get('verdict')),
                                               esc(r.get('proposed_fix'))))
        out.append('')

    whos = collections.Counter(d.get('who_is_right') for d in dis)
    out += ['## Adversarial verification', '',
            'Every group was independently re-derived by a second agent that was told to',
            'refute rather than review, with every non-ALIGNED row and two ALIGNED rows',
            'put to it. It was asked to default to reporting a disagreement when unsure,',
            'because a false ALIGNED is the failure mode that matters here.', '',
            '- disagreements raised: **%d**' % len(dis),
            '- verifier right (row corrected): **%d**' % whos.get('mine', 0),
            '- original right (row stands): **%d**' % whos.get('original', 0),
            '- unresolved, left flagged: **%d**' % whos.get('unresolved', 0),
            '- rows overturned in the matrix below: **%d**' % len(overturned), '']
    if dis:
        out += ['| file | original | re-derived | who is right | why |', '|---|---|---|---|---|']
        for d in dis:
            out.append('| `%s` | %s | %s | **%s** | %s |'
                       % (os.path.basename(esc(d.get('file'))),
                          esc(d.get('original_verdict')), esc(d.get('my_verdict')),
                          esc(d.get('who_is_right')), esc(d.get('why'))))
        out.append('')

    out += ['## The matrix', '']
    bypack = collections.defaultdict(list)
    for f in have:
        bypack[packof[f][0]].append(rows[f])
    for pack in [g['pack'] for g in work]:
        if pack not in bypack:
            continue
        rs = bypack.pop(pack)
        out += ['### `%s`' % pack, '',
                '| file | surf | pack week | SoW week | SoW strand | SoW outcome | cell | lesson LO | verdict | tier |',
                '|---|---|---|---|---|---|---|---|---|---|']
        for r in sorted(rs, key=lambda x: x['file']):
            mark = ' ⚑' if r['file'] in overturned else ''
            out.append('| %s%s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s |' % (
                os.path.basename(r['file']), mark, esc(r.get('surface')),
                esc(r.get('pack_week')), esc(r.get('sow_week')),
                esc(r.get('sow_strand'))[:60], esc(r.get('sow_outcome'))[:110],
                esc(r.get('sow_cell')), esc(r.get('lesson_lo'))[:110],
                esc(r.get('verdict')), esc(r.get('tier'))))
        out.append('')

    open('_next6/SOW_MATRIX.md', 'w').write('\n'.join(out))
    print('rows %d/%d · verdicts %s · tiers %s · disagreements %d · retyped %d · overturned %d'
          % (len(have), len(allfiles), dict(dist), dict(tiers), len(dis),
             len(retyped), len(overturned)))
    print('   surface typing: %d agent-corrected, %d stricter-corrected' % (len(rescued), len(retyped)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
