"""A6 gate — GROW Supported route, per file, before and after.

Scope, exactly as A6 defines it: the `.print-route.supported` block on print page 1
(task + scaffold), the Supported tier text on the Independent slide, and the
Supported arrival and exit prompts.

    python3 _sciv3/tools/a6_report.py <inputs/grow> <installed grow dir>
"""
import sys, os, re, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_text import fk_grade, visible_words, div_by_class, strip_html

OLD, NEW = sys.argv[1], sys.argv[2]
TARGET = 8.24
NAMES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'namemap.json')))['names']['grow']

VOCAB = ['friction', 'surface', 'pivot', 'lever', 'variable', 'orbit', 'gravity',
         'phase', 'reflect', 'force', 'resistance', 'planet', 'moon', 'mnemonic',
         'gear', 'pulley', 'measure', 'record', 'predict', 'conclude', 'observer',
         'rocky', 'giant', 'sunlight', 'distance']


def panel(t, typ):
    m = re.search(r'<section class="slide"[^>]*data-type="%s"[^>]*>' % typ, t)
    seg = t[m.end():t.find('</section>', m.end())]
    mm = re.search(r'<div class="tier[^"]*" data-tier="Supported" data-tier-panel="%s">\s*'
                   r'<div class="task-box"><b>[^<]*</b><p>(.*?)</p>' % typ, seg, re.S)
    return mm.group(1) if mm else ''


def parts(t):
    pr = re.search(r'<div class="print-route supported"><h2>Supported independent route</h2>'
                   r'<div class="print-box">(.*?)</div>\s*<h3>Scaffold</h3>'
                   r'<div class="print-box">(.*?)</div></div>', t, re.S)
    return {'task': pr.group(1), 'scaffold': pr.group(2),
            'arrival': panel(t, 'arrival'), 'exit': panel(t, 'exit')}


def four_elements(p, t):
    """task line · word bank or visual support · sentence stem · evidence route"""
    scaf = p['scaffold'].lower()
    return {
        'task line': bool(p['task'].strip()),
        'word bank / visual support': bool(re.search(
            r'word bank|picture|photo|diagram|visual|icon|card|strip|mnemonic|sequence|'
            r'wheel|table|frame|labelled', scaf)),
        'sentence stem': bool(re.search(r'sentence stem|stem:|‘[^’]*__|choice vocab|'
                                        r'choice words|word bank', scaf)),
        'evidence route': bool(re.search(r'evidence can be|evidence target|evidence', t, re.I)),
    }


rows = []
print(f'{"lesson":32s} {"FK before":>9s} {"FK after":>8s} {"w before":>8s} {"w after":>7s} '
      f'{"Δw%":>6s}  vs 8.24')
for src, dst in NAMES.items():
    if not src.startswith('SCI_'):
        continue
    a = open(os.path.join(OLD, src), encoding='utf-8').read()
    b = open(os.path.join(NEW, dst), encoding='utf-8').read()
    pa, pb = parts(a), parts(b)
    sa, sb = ' '.join(pa.values()), ' '.join(pb.values())
    ga, wa, _, _ = fk_grade(sa)
    gb, wb, _, _ = fk_grade(sb)
    d = (wb - wa) / wa * 100
    rows.append((dst, ga, gb, wa, wb, d, pa, pb))
    flag = 'ok' if gb <= TARGET else 'OVER'
    print(f'{dst.replace(".html",""):32s} {ga:9.2f} {gb:8.2f} {wa:8d} {wb:7d} {d:+5.1f}%  {flag}')

pooled_a = ' '.join(' '.join(r[6].values()) for r in rows)
pooled_b = ' '.join(' '.join(r[7].values()) for r in rows)
print(f'\npooled Supported route: FK {fk_grade(pooled_a)[0]:.2f} -> {fk_grade(pooled_b)[0]:.2f}, '
      f'words {fk_grade(pooled_a)[1]} -> {fk_grade(pooled_b)[1]}')

print('\n--- anti-gaming constraints ---')
bad = []
for dst, ga, gb, wa, wb, d, pa, pb in rows:
    if abs(d) > 15:
        bad.append(f'{dst}: word count moved {d:+.1f}% (limit ±15%)')
    fa = four_elements(pa, '')
    fb = four_elements(pb, '')
    lost = [k for k in fa if fa[k] and not fb[k]]
    if lost:
        bad.append(f'{dst}: lost element(s) {lost}')
    va = {v for v in VOCAB if v in ' '.join(pa.values()).lower()}
    vb = {v for v in VOCAB if v in ' '.join(pb.values()).lower()}
    if va - vb:
        bad.append(f'{dst}: science vocabulary dropped: {sorted(va - vb)}')
print('  word count within ±15% per lesson:', 'PASS' if not any('word count' in x for x in bad) else 'FAIL')
print('  no Supported element lost:        ', 'PASS' if not any('lost element' in x for x in bad) else 'FAIL')
print('  science vocabulary preserved:     ', 'PASS' if not any('vocabulary' in x for x in bad) else 'FAIL')
for x in bad:
    print('   !', x)

print('\n--- four-element audit of every Supported route (state BEFORE any edit) ---')
for dst, ga, gb, wa, wb, d, pa, pb in rows:
    fa = four_elements(pa, open(os.path.join(OLD, [k for k, v in NAMES.items() if v == dst][0]),
                                encoding='utf-8').read())
    missing = [k for k, v in fa.items() if not v]
    print(f'  {dst.replace(".html",""):32s} {"all four present" if not missing else "MISSING: " + str(missing)}')

print('\n--- plain-text diff of every changed Supported block ---')
for dst, ga, gb, wa, wb, d, pa, pb in rows:
    for k in ('task', 'scaffold', 'arrival', 'exit'):
        if pa[k] != pb[k]:
            print(f'\n  {dst}  [{k}]')
            print(f'    -  {strip_html(pa[k])}')
            print(f'    +  {strip_html(pb[k])}')
            print(f'       FK {fk_grade(pa[k])[0]:.2f} -> {fk_grade(pb[k])[0]:.2f}   '
                  f'words {fk_grade(pa[k])[1]} -> {fk_grade(pb[k])[1]}')
sys.exit(1 if bad else 0)
