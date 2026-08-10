"""Gate 10 — one reading-level instrument across all six sets.

Sets: live GROW / BUILD / LAUNCH (the twenty-five shipped lessons) and the three
new v3 packs. Usage:

    python3 _sciv3/tools/measure.py <new-root>   # new-root holds grow/ build/ launch/
"""
import sys, os, re, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_text import fk_grade, strip_html, visible_words, slide_texts, section_blocks, div_by_class

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TIERS = ['supported', 'standard', 'stretch']


def _dehead(s):
    """Drop tier headings — 'Supported independent route' is a label, not task prose."""
    return re.sub(r'<h2>.*?</h2>|<h3>Scaffold</h3>', ' ', s, flags=re.S)


def route_text_new(t, tier, part='all'):
    """New packs: `.print-route <tier>` (GROW) / `.proute <tier>` (BUILD, LAUNCH).

    part='all'  -> task + scaffold (the whole printed route)
    part='task' -> the task line only
    """
    blocks = div_by_class(t, 'print-route ' + tier) or div_by_class(t, 'proute ' + tier)
    if part == 'task':
        outs = []
        for b in blocks:
            b = re.sub(r'<h2>.*?</h2>', ' ', b, flags=re.S)
            b = re.split(r'<h3>Scaffold</h3>|<div class="box scaf">|<div class="print-box">'
                         r'(?=[^<]*$)', b)[0]
            inner = div_by_class(b, 'print-box')
            outs.append(inner[0] if inner else b)
        return ' '.join(outs)
    return _dehead(' '.join(blocks))


def route_text_live(t, tier, part='all'):
    """Live suites: `#print-scaffold-<tier>` + `#print-worksheet-<tier>`."""
    kinds = ('worksheet',) if part == 'task' else ('scaffold', 'worksheet')
    out = []
    for kind in kinds:
        m = re.search(r'<div id="print-%s-%s" class="print-section">(.*?)(?=<div id="print-)'
                      % (kind, tier), t, re.S)
        if m:
            out.append(m.group(1))
    s = _dehead(' '.join(out))
    if part == 'task':
        # the worksheet's leading "Task:" paragraph, without the ruled answer lines
        mm = re.search(r'<p>(.*?)</p>', s, re.S)
        s = mm.group(1) if mm else s
    return s


def slides_only(t):
    """Slide text with the print pack excluded (it is not on-screen text)."""
    return ' '.join(inner for _, inner in slide_texts(t))


def per_slide_type(t):
    d = {}
    for typ, inner in slide_texts(t):
        d.setdefault(typ, []).append(inner)
    return d


def measure_set(files, live):
    rows, slide_pool, route_pool = [], [], {k: [] for k in TIERS}
    bytype = {}
    for f in files:
        t = open(f, encoding='utf-8').read()
        s = slides_only(t)
        g, w, _, _ = fk_grade(s)
        rows.append((os.path.basename(f), g, w))
        slide_pool.append(s)
        for tier in TIERS:
            fn = route_text_live if live else route_text_new
            route_pool[tier].append((fn(t, tier, 'all'), fn(t, tier, 'task')))
        for typ, chunks in per_slide_type(t).items():
            bytype.setdefault(typ, []).append(' '.join(chunks))
    res = {
        'n': len(files),
        'slides_fk_pooled': fk_grade(' '.join(slide_pool))[0],
        'slides_fk_mean': round(sum(r[1] for r in rows) / len(rows), 2),
        'slides_words_mean': round(sum(r[2] for r in rows) / len(rows)),
        'rows': rows,
        'routes': {}, 'by_type': {},
    }
    for tier in TIERS:
        g, w, _, _ = fk_grade(' '.join(a for a, _ in route_pool[tier]))
        gt, wt, _, _ = fk_grade(' '.join(b for _, b in route_pool[tier]))
        res['routes'][tier] = {
            'fk': g, 'words_mean': round(w / len(files), 1) if w else 0, 'words_total': w,
            'fk_task': gt, 'task_words_mean': round(wt / len(files), 1) if wt else 0,
        }
    for typ, chunks in bytype.items():
        g, w, _, _ = fk_grade(' '.join(chunks))
        res['by_type'][typ] = {'fk': g, 'words_mean': round(w / len(chunks))}
    return res


SETS = {
    'GROW live':   (sorted(glob.glob(f'{REPO}/Science_Teesside/Grow/SCI_G_*.html')), True),
    'BUILD live':  (sorted(glob.glob(f'{REPO}/Science_Teesside/Build/SCI_B_*.html')), True),
    'LAUNCH live': (sorted(glob.glob(f'{REPO}/Science_Teesside/Launch/SCI_L_*.html')), True),
}

if __name__ == '__main__':
    new_root = sys.argv[1] if len(sys.argv) > 1 else None
    sets = dict(SETS)
    if new_root:
        for pack, lab in (('grow', 'GROW'), ('build', 'BUILD'), ('launch', 'LAUNCH')):
            fs = sorted(glob.glob(f'{new_root}/{pack}/SCI_*.html'))
            if fs:
                sets[f'{lab} new'] = (fs, False)
    out = {}
    for name, (files, live) in sets.items():
        files = [f for f in files if 'v3_40min' not in f] if live else files
        out[name] = measure_set(files, live)

    print(f"{'set':13s} {'n':>3s} {'slides FK':>10s} {'words/lsn':>10s} "
          f"{'Supported':>10s} {'Standard':>9s} {'Stretch':>8s}")
    for name in ['GROW live', 'GROW new', 'BUILD live', 'BUILD new', 'LAUNCH live', 'LAUNCH new']:
        if name not in out:
            continue
        r = out[name]
        print(f"{name:13s} {r['n']:3d} {r['slides_fk_pooled']:10.2f} {r['slides_words_mean']:10d} "
              f"{r['routes']['supported']['fk']:10.2f} {r['routes']['standard']['fk']:9.2f} "
              f"{r['routes']['stretch']['fk']:8.2f}")
    print("\nUNIVERSE B — task line only (the ~17-32 word fragment):")
    print(f"{'set':13s} {'Supported':>10s} {'Standard':>9s} {'Stretch':>8s}   mean words/tier")
    for name in ['GROW live','GROW new','BUILD live','BUILD new','LAUNCH live','LAUNCH new']:
        if name not in out: continue
        r = out[name]['routes']
        print(f"{name:13s} {r['supported']['fk_task']:10.2f} {r['standard']['fk_task']:9.2f} "
              f"{r['stretch']['fk_task']:8.2f}   "
              + str({k: r[k]['task_words_mean'] for k in TIERS}))
    print("\nroute fragment sizes, universe A task+scaffold (mean words per lesson):")
    for name in out:
        r = out[name]
        print("  %-13s %s" % (name, {k: r['routes'][k]['words_mean'] for k in TIERS}))
    print("\nper-slide-type FK / mean words (BUILD new, LAUNCH new scope Phase E):")
    for name in out:
        print("  " + name)
        for typ in ['title', 'arrival', 'starter', 'ido', 'wedo', 'independent', 'exit', '?']:
            if typ in out[name]['by_type']:
                d = out[name]['by_type'][typ]
                print(f"      {typ:12s} FK {d['fk']:6.2f}   {d['words_mean']:5d} w")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'measure_out.json'), 'w'), indent=1)
