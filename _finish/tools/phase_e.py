"""Phase E — Independent slide only, in the 35 science v3 lessons.

    python3 _finish/tools/phase_e.py extract          # editable blocks -> JSON
    python3 _finish/tools/phase_e.py measure          # per-file Independent FK/words
    python3 _finish/tools/phase_e.py apply <edits.json>

Scope, from §6: the Independent slide's TASK line, TIER ROUTE text and SCAFFOLD.
Chassis boilerplate repeated identically across every lesson in a pack (evidence
gate, participation chips, science gate, Lundy note) is NOT lesson prose and is
not touched — rewriting it would diverge fifteen files from each other for nothing.
"""
import sys, os, re, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                                '_sciv3', 'tools'))
from lib_text import fk_grade  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PACKS = {'grow': 'Science_Teesside/Grow/v3_40min',
         'build': 'Science_Teesside/Build/v3_40min',
         'launch': 'Science_Teesside/Launch/v3_40min'}
# each pathway's OWN live Independent figure, measured with this instrument
TARGET = {'grow': 7.35, 'build': 6.20, 'launch': 8.48}


def indep(t):
    m = re.search(r'<section class="slide"[^>]*data-type="independent"[^>]*>', t)
    if not m:
        return None, None, None
    i = m.end()
    j = t.find('</section>', i)
    return i, j, t[i:j]


def blocks(seg):
    """The editable prose: the task paragraph, and each tier route's text + scaffold.
    Returned as verbatim substrings so an edit can be applied by exact replacement."""
    out = []
    m = re.search(r'<div class="(?:box task|task-box)"[^>]*>(.*?)</div>', seg, re.S)
    if m:
        for p in re.finditer(r'<p[^>]*>(.*?)</p>', m.group(1), re.S):
            if len(re.sub(r'<[^>]+>', '', p.group(1)).strip()) > 25:
                out.append(p.group(1))
        if not out:
            inner = re.sub(r'^<[bh]\d?>.*?</[bh]\d?>', '', m.group(1), flags=re.S)
            if len(re.sub(r'<[^>]+>', '', inner).strip()) > 25:
                out.append(inner)
    for cls in ('route-card supported', 'route-card standard', 'route-card stretch',
                'route s', 'route m', 'route h'):
        for m in re.finditer(r'<div class="%s"[^>]*>(.*?)(?=<div class="route|</div></div>)'
                             % re.escape(cls), seg, re.S):
            for b in re.finditer(r'<b>(.*?)</b>', m.group(1), re.S):
                if len(re.sub(r'<[^>]+>', '', b.group(1)).strip()) > 25:
                    out.append(b.group(1))
    # GROW's scaffold pop-out, and BUILD/LAUNCH's — different class, same job.
    for pat in (r'<div class="scaffold-pop"[^>]*>(.*?)<div style=',
                r'<div class="scaffold" id="[^"]*">(.*?)<div class="note">'):
        for m in re.finditer(pat, seg, re.S):
            if len(re.sub(r'<[^>]+>', '', m.group(1)).strip()) > 25:
                out.append(m.group(1))
    return [b for b in dict.fromkeys(out)]


def files():
    for p, d in PACKS.items():
        for f in sorted(glob.glob(os.path.join(REPO, d, 'SCI_*.html'))):
            yield p, f


def measure():
    print(f'{"lesson":44s} {"FK":>6s} {"words":>6s}  target  gap')
    agg = {}
    for p, f in files():
        t = open(f, encoding='utf-8').read()
        _, _, seg = indep(t)
        g, w, _, _ = fk_grade(seg or '')
        agg.setdefault(p, []).append((g, w))
        flag = '' if g <= TARGET[p] else f'+{g - TARGET[p]:.2f}'
        print(f'  {os.path.basename(f)[:42]:42s} {g:6.2f} {w:6d}  {TARGET[p]:5.2f}  {flag}')
    print()
    for p, rows in agg.items():
        print(f'  {p.upper():7s} mean FK {sum(r[0] for r in rows)/len(rows):5.2f}  '
              f'mean words {round(sum(r[1] for r in rows)/len(rows)):4d}  target {TARGET[p]}')


def extract():
    out = []
    for p, f in files():
        t = open(f, encoding='utf-8').read()
        _, _, seg = indep(t)
        bl = blocks(seg)
        g, w, _, _ = fk_grade(seg)
        out.append({'pack': p, 'file': os.path.relpath(f, REPO), 'fk': g, 'words': w,
                    'target': TARGET[p], 'blocks': bl})
    json.dump(out, open('/tmp/phase_e_blocks.json', 'w'), ensure_ascii=False, indent=1)
    print(f'{len(out)} lessons; blocks per lesson: '
          f'{[len(o["blocks"]) for o in out]}')
    print('written to /tmp/phase_e_blocks.json')


def apply(path):
    edits = json.load(open(path, encoding='utf-8'))
    report = []
    for e in edits:
        f = os.path.join(REPO, e['file'])
        t = open(f, encoding='utf-8').read()
        _, _, seg0 = indep(t)
        g0, w0, _, _ = fk_grade(seg0)
        t2, applied, failed = t, 0, []
        for pair in e['replacements']:
            old, new = pair['old'], pair['new']
            n = t2.count(old)
            if n == 0:
                failed.append(old[:60])
                continue
            t2 = t2.replace(old, new)
            applied += n
        _, _, seg1 = indep(t2)
        g1, w1, _, _ = fk_grade(seg1)
        dw = (w1 - w0) / w0 * 100 if w0 else 0
        ok = abs(dw) <= 15 and g1 < g0 and not failed
        if ok:
            open(f, 'w', encoding='utf-8').write(t2)
        report.append({'file': e['file'], 'pack': e['pack'], 'fk_before': g0, 'fk_after': g1,
                       'w_before': w0, 'w_after': w1, 'dw_pct': round(dw, 1),
                       'applied': applied, 'failed': failed, 'kept': ok,
                       'target': TARGET[e['pack']]})
    json.dump(report, open('/tmp/phase_e_report.json', 'w'), ensure_ascii=False, indent=1)
    print(f'{"lesson":44s} {"FK":>13s} {"words":>13s} {"Δw%":>6s}  kept')
    for r in report:
        print(f'  {os.path.basename(r["file"])[:42]:42s} {r["fk_before"]:6.2f}->{r["fk_after"]:6.2f} '
              f'{r["w_before"]:6d}->{r["w_after"]:6d} {r["dw_pct"]:+6.1f}  '
              f'{"yes" if r["kept"] else "NO — left unchanged"}'
              + (f'  unmatched:{len(r["failed"])}' if r['failed'] else ''))
    kept = [r for r in report if r['kept']]
    print(f'\n{len(kept)}/{len(report)} files changed; '
          f'{len(report) - len(kept)} left unchanged and named above')


if __name__ == '__main__':
    {'extract': extract, 'measure': measure}.get(sys.argv[1], lambda: apply(sys.argv[2]))()
