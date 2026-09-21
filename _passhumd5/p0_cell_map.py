#!/usr/bin/env python3
"""HUM-D5 Part B, P0 — derive the cell map and the retire list FROM THE FILES.

Ruling 4 of 2026-09-22: "run it now; Part B's '12 of 39 LAND' is a plan until then."
Nothing here is copied from the order or the plan. Every figure is read off a file and
printed with its scope, so a disagreement with the plan is a finding, not a rounding.

Writes, beside this file:
    CELL_MAP.md     one row per SoW cell: what teaches it now, what is incoming
    RETIRE_LIST.md  the existing surfaces whose cell has an incoming lesson
    P0_SOURCES.md   the per-deck source table the chassis contract requires
                    (deck | generations | chosen source | sha256 | bytes)
"""
from __future__ import annotations
import hashlib, json, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOW = ROOT / 'Humanities_Teesside/Teaching_Packs/HUM_00_SoW_and_Order'
OUT = Path(__file__).resolve().parent
import lxml.html as lh

TERM_NAME = {'A1': 'Autumn 1', 'A2': 'Autumn 2', 'S1': 'Spring 1', 'S2': 'Spring 2',
             'SU1': 'Summer 1', 'SU2': 'Summer 2'}
NAME_TERM = {v: k for k, v in TERM_NAME.items()}


# ---------------------------------------------------------------- the cells
def humanities_cells():
    """117 cells: every article.week inside a details.unit[data-pathway]."""
    doc = lh.fromstring((SOW / 'Humanities_Scheme_of_Work_2026-27.html').read_bytes())
    out = []
    for unit in doc.xpath('//details[@class="unit"][@data-pathway]'):
        pathway = unit.get('data-pathway')
        summ = ' '.join(unit.find('summary').text_content().split())
        parts = [p.strip() for p in summ.split('·')]
        term = parts[1] if len(parts) > 1 else '?'
        unit_title = parts[2] if len(parts) > 2 else ''
        for art in unit.xpath('.//article[contains(@class,"week")]'):
            h3 = art.find('.//h3')
            head = ' '.join((h3.text_content() if h3 is not None else '').split())
            m = re.match(r'^Week\s+(\d+)\s*·\s*(.*)$', head)
            if not m:
                continue
            out.append({'subject': 'Humanities', 'pathway': pathway, 'term': term,
                        'term_code': NAME_TERM.get(term, term), 'week': int(m.group(1)),
                        'outcome': m.group(2), 'unit': unit_title})
    return out


def re_cells():
    """42 cells: every details under a 'PATHWAY · TERM' h2 section."""
    doc = lh.fromstring((SOW / 'RE_Scheme_of_Work_Autumn_2026.html').read_bytes())
    out = []
    for sec in doc.xpath('//section'):
        h2 = sec.find('.//h2')
        head = ' '.join((h2.text_content() if h2 is not None else '').split())
        m = re.match(r'^(BUILD|GROW|LAUNCH)\s*·\s*(.*)$', head)
        if not m:
            continue
        pathway, term = m.group(1), m.group(2).strip()
        for i, det in enumerate(sec.xpath('.//details'), start=1):
            summ = ' '.join(det.find('summary').text_content().split())
            wm = re.search(r'Week\s+(\d+)', summ)
            out.append({'subject': 'RE & World Views', 'pathway': pathway, 'term': term,
                        'term_code': NAME_TERM.get(term, term),
                        'week': int(wm.group(1)) if wm else i,
                        'outcome': summ, 'unit': ''})
    return out


# ------------------------------------------------------- the incoming lessons
ID_RX = re.compile(r'^(BUILD|GROW|LAUNCH)_(RE_)?([A-Z]+\d*)_W(\d+)$')


def incoming(roots):
    """Every *_Lesson.html under the given roots, keyed by the cell its id names."""
    found = {}
    for root in roots:
        for f in sorted(Path(root).rglob('*_Lesson.html')):
            lid = f.name[:-len('_Lesson.html')]
            m = ID_RX.match(lid)
            if not m:
                found.setdefault('UNPARSED', []).append(str(f))
                continue
            pathway, is_re, term_code, week = m.group(1), bool(m.group(2)), m.group(3), int(m.group(4))
            key = ('RE & World Views' if is_re else 'Humanities', pathway, term_code, week)
            found.setdefault(key, []).append(f)
    return found


# -------------------------------------------------- the existing estate surfaces
EXISTING_RX = re.compile(r'^(BUILD|GROW|LAUNCH)_(HUM|RE|Humanities)_?', re.I)


def existing_surfaces():
    """Every tracked Humanities html the estate serves today, with whatever cell its own
    name and its own config declare. A surface whose cell cannot be derived is listed as
    UNDERIVED rather than guessed."""
    files = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
    keep = [f for f in files if f.endswith('.html') and re.match(
        r'^(Humanities_Teesside|Build|Grow|Launch|LAUNCH_Estate_v3)/', f)]
    rows = []
    for rel in keep:
        p = ROOT / rel
        if not p.exists():
            continue
        name = p.name
        if name.startswith('START_HERE') or name == 'index.html':
            continue
        s = p.read_text(encoding='utf-8', errors='replace')
        cell = None
        m = re.search(r'"absolute_week"\s*:\s*(\d+)', s)
        hm = re.search(r'<body[^>]*data-lesson-id="([^"]+)"', s)
        lid = hm.group(1) if hm else ''
        im = ID_RX.match(lid)
        if im:
            cell = ('RE & World Views' if im.group(2) else 'Humanities',
                    im.group(1), im.group(3), int(im.group(4)))
        rows.append({'path': rel, 'lesson_id': lid, 'absolute_week': int(m.group(1)) if m else None,
                     'cell': cell})
    return rows


def sha_bytes(p: Path):
    b = p.read_bytes()
    return hashlib.sha256(b).hexdigest(), len(b)


def main():
    roots_120 = ['/tmp/claude-0/humd5/unzipped']
    roots_su1 = sys.argv[1:]                      # the Summer 1 pack roots, if supplied
    cells = humanities_cells() + re_cells()
    inc = incoming(roots_120 + roots_su1)
    unparsed = inc.pop('UNPARSED', [])
    surfaces = existing_surfaces()

    by_cell = defaultdict(list)
    for r in surfaces:
        if r['cell']:
            by_cell[r['cell']].append(r)

    hum = [c for c in cells if c['subject'] == 'Humanities']
    rel = [c for c in cells if c['subject'] != 'Humanities']
    print('SoW CELLS DERIVED FROM THE FILES')
    print('  Humanities        : %d  (scope: article.week inside details.unit[data-pathway],' % len(hum))
    print('                       Humanities_Scheme_of_Work_2026-27.html)')
    print('  RE & World Views  : %d  (scope: details inside each PATHWAY · TERM section,' % len(rel))
    print('                       RE_Scheme_of_Work_Autumn_2026.html)')
    print('  combined          : %d' % len(cells))
    print()
    inc_keys = set(inc)
    print('INCOMING LESSONS FOUND: %d  (unparsed ids: %d)' % (
        sum(len(v) for v in inc.values()), len(unparsed)))
    covered = [c for c in cells if (c['subject'], c['pathway'], c['term_code'], c['week']) in inc_keys]
    nocover = [c for c in cells if (c['subject'], c['pathway'], c['term_code'], c['week']) not in inc_keys]
    print('  cells WITH an incoming lesson : %d' % len(covered))
    print('  cells with NO incoming lesson : %d' % len(nocover))
    orphan = [k for k in inc_keys if not any(
        (c['subject'], c['pathway'], c['term_code'], c['week']) == k for c in cells)]
    print('  incoming lessons with NO SoW cell : %d  %s' % (len(orphan), sorted(orphan)[:6]))
    print()
    print('EXISTING ESTATE SURFACES: %d html tracked under the Humanities trees' % len(surfaces))
    print('  with a derivable cell     : %d' % sum(1 for r in surfaces if r['cell']))
    print('  UNDERIVED (no data-lesson-id that names a cell) : %d'
          % sum(1 for r in surfaces if not r['cell']))
    print()

    # ---- CELL_MAP.md
    lines = ['# P0 — CELL_MAP', '',
             'Derived from the files by `_passhumd5/p0_cell_map.py`, not copied from the order.',
             'Scope of every figure is printed by the instrument itself.', '',
             '| subject | pathway | term | week | incoming lesson | serves it today | state |',
             '|---|---|---|---|---|---|---|']
    counts = defaultdict(int)
    for c in sorted(cells, key=lambda c: (c['subject'], c['pathway'], c['term_code'], c['week'])):
        k = (c['subject'], c['pathway'], c['term_code'], c['week'])
        incoming_ids = [f.name[:-len('_Lesson.html')] for f in inc.get(k, [])]
        rows_here = by_cell.get(k, [])
        packs = [r for r in rows_here if '/Teaching_Packs/' in r['path']]
        served = [r for r in rows_here if '/Teaching_Packs/' not in r['path']]
        now = ['%s%s' % (r['path'].split('/')[-1], ' (pack copy)' if '/Teaching_Packs/' in r['path'] else '')
               for r in rows_here]
        if incoming_ids and served:
            state = 'REPLACE a served route'
        elif incoming_ids and packs:
            state = 'PACK COPY ONLY'
        elif incoming_ids:
            state = 'NEW'
        elif rows_here:
            state = 'LEFT ALONE'
        else:
            state = 'NO INCOMING, NO SURFACE'
        counts[state] += 1
        lines.append('| %s | %s | %s | %d | %s | %s | %s |' % (
            c['subject'], c['pathway'], c['term'], c['week'],
            ', '.join(incoming_ids) or '—', ', '.join(now) or '—', state))
    lines += ['', '## Totals', '']
    for k, v in sorted(counts.items()):
        lines.append('- **%s** — %d cells' % (k, v))
    (OUT / 'CELL_MAP.md').write_text('\n'.join(lines) + '\n')
    print('CELL_MAP.md states:', dict(counts))

    # ---- RETIRE_LIST.md
    rl = ['# P0 — RETIRE_LIST', '',
          'Existing surfaces whose SoW cell has an incoming lesson. Listed, never acted on here.',
          '', '| existing surface | lesson id | cell | incoming |', '|---|---|---|---|']
    n = 0
    for c in sorted(cells, key=lambda c: (c['subject'], c['pathway'], c['term_code'], c['week'])):
        k = (c['subject'], c['pathway'], c['term_code'], c['week'])
        if not inc.get(k):
            continue
        for r in by_cell.get(k, []):
            n += 1
            rl.append('| `%s` | %s | %s %s %s w%d | %s |' % (
                r['path'], r['lesson_id'] or '—', c['subject'], c['pathway'], c['term'], c['week'],
                ', '.join(f.name[:-len('_Lesson.html')] for f in inc[k])))
    rl += ['', '**%d existing surfaces sit on a cell that has an incoming lesson.**' % n]
    und = [r for r in surfaces if not r['cell']]
    lessonish = [r for r in und
                 if re.search(r'(BUILD|GROW|LAUNCH)_(HUM|RE|Humanities)', r['path'].split('/')[-1])]
    nothing = [r for r in lessonish if r['absolute_week'] is None and not r['lesson_id']]
    rl += ['', '## UNDERIVED — %d surfaces whose cell this instrument will not guess' % len(und), '',
           'Of those, **%d have a lesson-shaped file name**. Measured on the files themselves:' % len(lessonish),
           '**%d of the %d carry neither a `data-lesson-id` nor an `absolute_week`** — there is nothing'
           % (len(nothing), len(lessonish)),
           'in the file that names the cell it serves, so the cell cannot be derived at all. It can only',
           'be RULED. This is the P0 finding that blocks the rest of RETIRE_LIST, stated rather than guessed.',
           '', '### The %d lesson-shaped surfaces with no cell in the file' % len(nothing), '']
    for r in nothing:
        rl.append('- `%s`' % r['path'])
    other = [r for r in und if r not in lessonish]
    rl += ['', '### The other %d UNDERIVED surfaces (pack material, indexes, records)' % len(other), '']
    for k in sorted({'/'.join(r['path'].split('/')[:2]) for r in other}):
        rl.append('- `%s/` — %d' % (k, sum(1 for r in other if r['path'].startswith(k + '/'))))
    (OUT / 'RETIRE_LIST.md').write_text('\n'.join(rl) + '\n')
    print('RETIRE_LIST.md: %d surfaces on a covered cell, %d UNDERIVED' % (n, len(und)))

    # ---- P0_SOURCES.md
    src = ['# P0 — per-deck source table', '',
           'CHASSIS_CONTRACT L556: source selection is never filesystem order. Every digest below',
           'is computed at write time from the chosen file.', '',
           '| deck | generations found | chosen source | sha256 | bytes |', '|---|---|---|---|---|']
    for k in sorted(inc, key=lambda k: (k[0], k[1], k[2], k[3])):
        fs = inc[k]
        digs = {}
        for f in fs:
            d, b = sha_bytes(f)
            digs[str(f)] = (d, b)
        chosen = sorted(fs)[0]
        d, b = digs[str(chosen)]
        distinct = len({v[0] for v in digs.values()})
        src.append('| %s | %d file(s), %d distinct by content | `%s` | `%s` | %d |' % (
            fs[0].name[:-len('_Lesson.html')], len(fs), distinct,
            str(chosen).replace(str(ROOT) + '/', ''), d[:16], b))
    (OUT / 'P0_SOURCES.md').write_text('\n'.join(src) + '\n')
    print('P0_SOURCES.md: %d decks' % len(inc))


if __name__ == '__main__':
    main()
