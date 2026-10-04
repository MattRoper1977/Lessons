#!/usr/bin/env python3
"""DY-4 (ruling dy) / EB-5: bind the 7 Wave 1 Science return-week lessons to their Autumn 1 Week 8 cells, as data at
the sources of truth, in the shape tools/rx3_recommended.py --land-a2 writes for Autumn 2 (LAND-A2 R1/R3). Prepared
change for a scratch copy of Lessons; never run on a real checkout without the owner's go.

  BUILD  Aut1 W8: SCI_BUILD_A1_W08_P1, _P2 recommended (slots 1-2); W8A and W8B stay bound beside them, untouched.
  LAUNCH Aut1 W8: SCI_LAUNCH_A1_W08_L1, _L2, _L3 recommended (slots 1-3); the three live W8L1-L3 pages stay bound
                  beside them, untouched (their shelf style is already 'earlier').
  GROW   Aut1 W8: a new cell with GROW_SCI_A1_W08_P1, _P2 recommended; no Alternative (D20).
Unit tags are NOT written here: unit_tags.py --write derives them; LAUNCH L1-L3 carry none (ruling eb EB-4 b).

Writes (idempotent): tools/catalogue/SHELF_SELECTION.json, tools/catalogue/SCIENCE_WEEK_BINDINGS.json,
resources.json (+7 rows after the reviewed appended rows), tools/catalogue/pin_catalogue_contract.py (SHELF_ROWS),
the cross-repo gate in both repos (CATALOGUE_SHELF_ROWS = rows after the original 734; the Apps copy must get the same line).
Each page must state its own cell (book header "Science · <PATHWAY> · Autumn 1 · Week 08"); a delivery lesson record,
where one exists, must name the same lesson id (and the same pathway where it names one); else nothing is written.
usage: prepare_dy4_bind.py REPO [--run-date YYYY-MM-DD] [--dry]"""
import sys, os, re, json, hashlib, html as H, importlib.util, argparse
ap = argparse.ArgumentParser(); ap.add_argument('repo'); ap.add_argument('--run-date', default='2026-10-03'); ap.add_argument('--dry', action='store_true')
a = ap.parse_args(); R = a.repo
P = lambda p: os.path.join(R, p)
def J(p): return json.load(open(P(p), encoding='utf-8'))
def W(p, d, indent=2):
    if not a.dry: open(P(p), 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=indent) + '\n')
sha = lambda p: hashlib.sha256(open(P(p), 'rb').read()).hexdigest()
sys.path.insert(0, P('tools/catalogue')); from title_slide import title_slide_heading

PAGES = [  # (path, pathway, part label for the id, record or None)
 ('Science_Teesside/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1.html', 'BUILD', 'p1', '_land_a2/SC3R/SCI_BUILD_A1_W08_P1/LESSON_SOURCE.json'),
 ('Science_Teesside/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2.html', 'BUILD', 'p2', '_land_a2/SC3R/SCI_BUILD_A1_W08_P2/LESSON_SOURCE.json'),
 ('Science_Teesside/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1.html', 'GROW', 'p1', '_land_a2/SC3R4/GROW_SCI_A1_W08_P1/LESSON_SOURCE.json'),
 ('Science_Teesside/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2.html', 'GROW', 'p2', '_land_a2/SC3R4/GROW_SCI_A1_W08_P2/LESSON_SOURCE.json'),
 ('Science_Teesside/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1.html', 'LAUNCH', 'l1', None),
 ('Science_Teesside/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2.html', 'LAUNCH', 'l2', None),
 ('Science_Teesside/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3.html', 'LAUNCH', 'l3', None),
]
BOOK = re.compile(r'Science\s*·\s*(BUILD|GROW|LAUNCH)\s*·\s*Autumn 1\s*·\s*Week\s*0*(\d+)\b')
txt = lambda s: re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
landed, problems = [], []
for path, pw, part, rec in PAGES:
    if not os.path.isfile(P(path)): problems.append(f'{path}: page not in the tree'); continue
    raw = open(P(path), encoding='utf-8').read()
    vis = txt(re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', raw))
    m = BOOK.search(vis)
    if not m or (m.group(1), int(m.group(2))) != (pw, 8): problems.append(f'{path}: own book header does not state {pw} · Autumn 1 · Week 8 ({m.group(0) if m else None})'); continue
    if rec:
        if not os.path.isfile(P(rec)): problems.append(f'{path}: record {rec} missing'); continue
        r = json.load(open(P(rec), encoding='utf-8'))
        if r.get('lesson_id') != os.path.basename(path)[:-5] or r.get('pathway', pw) != pw:
            problems.append(f'{path}: record disagrees: {r.get("pathway")} {r.get("lesson_id")}'); continue
    title = title_slide_heading(raw) or os.path.basename(path)[:-5]
    goal = re.search(r'I can… ☐ ([^☐]+)', vis)
    landed.append(dict(path=path, pathway=pw, part=part, title=title, quote=m.group(0), record=rec,
                       goal=(goal.group(1).strip() if goal else '')))
if problems:
    print('REFUSED, nothing written:'); [print('  ' + p) for p in problems]; sys.exit(1)

BATCH = 'Science · Autumn 1 · Week 8 · DY-4: the return-week lesson is recommended; the live Week 8 lessons stay beside it'
sel = J('tools/catalogue/SHELF_SELECTION.json'); sel.setdefault('recommendedBatches', {})
rec_now = set(sel['recommended'])
for L in landed:
    rec_now.add(L['path']); sel['recommendedBatches'][L['path']] = BATCH
sel['recommended'] = sorted(rec_now)
have = {x['path'] for x in sel['science']}
for L in landed:
    if L['path'] not in have:
        sel['science'].append({'path': L['path'], 'classificationEvidence': [{'method': 'own title slide declaration', 'source': L['path'], 'quote': L['quote']}]})
W('tools/catalogue/SHELF_SELECTION.json', sel)

wb = J('tools/catalogue/SCIENCE_WEEK_BINDINGS.json'); ent = wb['entries']
for L in landed:
    e = {'pathway': L['pathway'], 'style': 'recommended', 'title': '%s · %s' % (L['pathway'], L['title']),
         'weeks': [{'key': 'Aut1·W8', 'term': 'Aut1', 'weekWithinTerm': 8, 'label': 'Autumn 1 · Week 8', 'ruledAbsoluteWeek': 8}],
         'sourceSha256': sha(L['path']), 'sourceProofUnchanged': True, 'status': 'set',
         'evidence': [{'method': 'own title slide declaration', 'source': L['path'], 'quote': L['quote'],
                       'calendar': '_sownb/CALENDAR_2026_27.json mapping abs8: enrichment week, no workbook row',
                       'ruling': 'DY-4 (ruling dy); EB-5 (ruling eb): return-week lessons bound to Aut1 · W8'}]}
    if L['record']:
        e['evidence'].append({'method': 'delivery lesson record, not served', 'source': L['record']})
    ent[L['path']] = e
runs = wb.setdefault('bindingRuns', [])
listed = sorted(L['path'] for L in landed)
runs[:] = [r for r in runs if r.get('by') != 'tools/catalogue/prepare_dy4_bind.py (DY-4)'] + [{'by': 'tools/catalogue/prepare_dy4_bind.py (DY-4)', 'bound': len(landed), 'listed': listed}]
W('tools/catalogue/SCIENCE_WEEK_BINDINGS.json', wb, indent=1)

rows = J('resources.json'); files = {r['file'] for r in rows}
pc = 'tools/catalogue/pin_catalogue_contract.py'; src = open(P(pc), encoding='utf-8').read()
spec = importlib.util.spec_from_file_location('pcc', P(pc)); pcc = importlib.util.module_from_spec(spec); spec.loader.exec_module(pcc)
at = pcc.ORIGINAL_ROW_COUNT + len(pcc.SHELF_ROWS); new = []
slug = lambda s: re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')
for L in landed:
    if L['path'] in files: continue
    words = [w for w in slug(L['title']).split('-') if len(w) > 2 and w not in ('and', 'the', 'for', 'use')]
    new.append({'subject': 'Science · Teesside', 'title': '%s · %s' % (L['pathway'], L['title']), 'file': L['path'],
                'id': 'dy4-sci-%s-a1-w08-%s-%s' % (L['pathway'].lower(), L['part'], slug(L['title'])), 'type': 'lesson', 'family': 'Science Teesside',
                'keywords': [L['pathway'].lower(), 'science', 'autumn 1', 'week 8'] + words,
                'desc': '%s Science · Autumn 1 · Week 8. I can %s' % (L['pathway'], (L['goal'][0].lower() + L['goal'][1:]) if L['goal'] else L['title']),
                'added': a.run_date, 'new': True, 'year': '2026-27'})
rows[at:at] = new
gate = 'tools/verify_cross_estate_unification.py'; gsrc = open(P(gate), encoding='utf-8').read()
m = re.search(r'^CATALOGUE_SHELF_ROWS = (\d+)$', gsrc, re.M)
if not a.dry and new:
    open(P('resources.json'), 'w', encoding='utf-8').write(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    lines = src.rstrip('\n').split('\n'); last = max(i for i, l in enumerate(lines) if l.startswith('SHELF_ROWS.append('))
    open(P(pc), 'w', encoding='utf-8').write('\n'.join(lines[:last + 1] + ['SHELF_ROWS.append(%r)' % r for r in new] + lines[last + 1:]) + '\n')
    open(P(gate), 'w', encoding='utf-8').write(gsrc[:m.start(1)] + str(len(rows) - pcc.ORIGINAL_ROW_COUNT) + gsrc[m.end(1):])
for L in landed:
    print(f"bound {L['pathway']:6} Aut1·W8 {L['path'].split('/')[-1]:28} quote '{L['quote']}' record {'yes' if L['record'] else 'none'}")
print(f'DY-4: {len(landed)} lessons · SHELF_SELECTION recommended {len(sel["recommended"])} · resources.json +{len(new)} rows at {at} ({len(rows)} total) · '
      f'SCIENCE_WEEK_BINDINGS {len(ent)} entries · CATALOGUE_SHELF_ROWS {m.group(1)} -> {len(rows) - pcc.ORIGINAL_ROW_COUNT} (its _SHA256 is re-cut by pin_catalogue_contract.py)')
