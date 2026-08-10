"""D3 — add a sentence stem to GROW Supported routes only where one is absent.

Never writes a fresh stem. The stem is lifted VERBATIM from the same lesson's
Standard scaffold, quoted clause and all.

    python3 _finish/tools/d3_stems.py [--apply]
"""
import sys, os, re, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                                '_sciv3', 'tools'))
from lib_text import div_by_class, fk_grade  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
APPLY = '--apply' in sys.argv
STEM_CLAUSE = re.compile(r'((?:Conclusion stem|Orbit stem|Sentence stem|Sentence|Conclusion|Stem)'
                         r'\s*:\s*[‘"][^’"]+[’"])')
HAS_STEM = re.compile(r'(?i)(sentence stem|conclusion stem|orbit stem|\bstem\s*:)')


def scaffold(t, tier):
    b = div_by_class(t, 'print-route ' + tier)
    if not b:
        return None, None
    parts = re.split(r'<h3>Scaffold</h3>\s*<div class="print-box">', b[0])
    if len(parts) < 2:
        return None, None
    inner = parts[1]
    end = inner.rfind('</div>')
    return inner[:end], inner[:end]


rows = []
for f in sorted(glob.glob(os.path.join(REPO, 'Science_Teesside/Grow/v3_40min/SCI_G_*.html'))):
    t = open(f, encoding='utf-8').read()
    sup, _ = scaffold(t, 'supported')
    std, _ = scaffold(t, 'standard')
    name = os.path.basename(f).replace('.html', '')
    if sup is None:
        rows.append((name, f, 'NO SUPPORTED SCAFFOLD', None, None, None))
        continue
    if HAS_STEM.search(re.sub(r'<[^>]+>', '', sup)):
        rows.append((name, f, 'already has a stem', sup, None, None))
        continue
    m = STEM_CLAUSE.search(re.sub(r'<[^>]+>', '', std or ''))
    if not m:
        rows.append((name, f, 'NO SIBLING STEM TO COPY — left unchanged', sup,
                     re.sub(r'<[^>]+>', '', std or '')[:90], None))
        continue
    rows.append((name, f, 'stem copied from this lesson’s Standard scaffold', sup, None,
                 m.group(1).strip()))

print(f'{"lesson":34s} {"outcome":48s} words before -> after')
changed = 0
for name, f, outcome, sup, note, stem in rows:
    before = fk_grade(sup or '')[1]
    after = before
    if stem:
        t = open(f, encoding='utf-8').read()
        old_block = sup
        new_block = sup.rstrip() + (' ' if sup.rstrip().endswith(('.', '’', '"')) else '. ') + stem
        n = t.count(old_block)
        # The Supported scaffold string appears TWICE by design — once in the print
        # route and once in the Independent slide's scaffold pop-out. Both are edited
        # so screen and paper stay in step, exactly as A6 did.
        if n not in (1, 2):
            print(f'  {name[:32]:32s} ANCHOR COUNT {n} — skipped, needs a look')
            continue
        after = fk_grade(new_block)[1]
        if APPLY:
            open(f, 'w', encoding='utf-8').write(t.replace(old_block, new_block))
            changed += 1
        outcome += f' (x{n}: print + Independent slide)'
    print(f'  {name[:32]:32s} {outcome[:52]:52s} {before:4d} -> {after:4d}')
    if stem:
        print(f'       + {stem}')
    if note:
        print(f'       Standard scaffold offers no quotable stem: “{note}”')

print(f'\n{changed} Supported scaffolds given a stem' + ('' if APPLY else ' (dry run)'))
print('Source is the SAME LESSON’s Standard scaffold, not a sibling Supported route:')
print('only one Supported stem exists in the whole pack (W3A) and it is bound to friction,')
print('so copying it into a planets or Moon lesson would be nonsense. Nothing was authored.')
