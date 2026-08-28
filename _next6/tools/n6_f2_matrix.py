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

    out += ['## Adversarial verification', '',
            '- disagreements raised: **%d**' % len(dis), '']
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
            out.append('| %s | %s | %s | %s | %s | %s | %s | %s | **%s** | %s |' % (
                os.path.basename(r['file']), esc(r.get('surface')),
                esc(r.get('pack_week')), esc(r.get('sow_week')),
                esc(r.get('sow_strand'))[:60], esc(r.get('sow_outcome'))[:110],
                esc(r.get('sow_cell')), esc(r.get('lesson_lo'))[:110],
                esc(r.get('verdict')), esc(r.get('tier'))))
        out.append('')

    open('_next6/SOW_MATRIX.md', 'w').write('\n'.join(out))
    print('rows %d/%d · verdicts %s · tiers %s · disagreements %d'
          % (len(have), len(allfiles), dict(dist), dict(tiers), len(dis)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
