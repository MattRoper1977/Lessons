#!/usr/bin/env python3
"""Run the N6 gate battery over every pack. Usage: run_gates.py <packs_root> [intake_root]

Gate 12 (`s24-print-renders`) runs automatically for every pack that has a print
surface, and it renders. That is deliberate and is the point of ORDER N6-I I2:
print and evidence work must not be able to ship on a byte check alone, because
the two defects that shipped green were both invisible to one. Set
`N6_SKIP_RENDERS=1` only when you know the pack has no print surface — and note
that a pack which HAS one and cannot be rendered goes RED rather than being
skipped, so the skip switch cannot be used to buy a green.

`N6_RENDERS=<dir>` reuses an existing render set instead of rendering again.
"""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates as G

# Accept either a parent directory of pack dirs (the intake shape) or the pack
# roots themselves (the landed shape — the nine packs live at nine destinations
# across the estate and there is no single parent to point at).
argv = [a for a in sys.argv[1:] if not a.startswith('--')]
roots = [a for a in argv if os.path.isdir(a)]
intake = None
if len(roots) == 2 and os.path.isdir(os.path.join(roots[1], os.path.basename(roots[0]))):
    roots, intake = roots[:1], roots[1]
elif len(roots) == 2 and glob.glob(os.path.join(roots[1], '*', '*.html')):
    roots, intake = roots[:1], roots[1]
reflist = os.environ.get('S23_NAMES')

def _is_pack(d):
    return bool(glob.glob(os.path.join(d, '**', '*.html'), recursive=True)) and \
        not all(os.path.isdir(os.path.join(d, x)) for x in os.listdir(d))

packs = []
for r in roots:
    kids = sorted(d for d in glob.glob(os.path.join(r, '*')) if os.path.isdir(d))
    if glob.glob(os.path.join(r, '*.html')) or not kids:
        packs.append(r)
    elif len(roots) > 1:
        packs.append(r)
    else:
        packs += kids
root = roots[0]
overall = True
report = []
for pk in packs:
    files = G.html_files(pk)
    res = [G.g1_syntax(files), G.g2_balance_dupid(files), G.g3_timings(files),
           G.g4_offline(files), G.g5_reduced_motion(files, os.path.join(intake, os.path.basename(pk)) if intake else None, pk), G.g6_links_manifest(pk)]
    if intake:
        ip = os.path.join(intake, os.path.basename(pk))
        if os.path.isdir(ip): res.append(G.g9_sentinel_set(ip, pk))
    res.append(G.g10_names(files, reflist))
    if os.environ.get('N6_SKIP_RENDERS') != '1':
        res.append(G.g12_print_renders(pk, files, os.environ.get('N6_RENDERS')))
    name = os.path.basename(pk)
    print('\n=== %s ===' % name)
    for gname, ok, detail, rows in res:
        tag = 'PASS' if ok else ('INVALID' if ok is None else 'FAIL')
        if ok is False: overall = False
        print('  %-8s %-48s %s' % (tag, gname, detail))
        for r in rows[:8]:
            print('             · %s' % ' | '.join(str(x) for x in r))
        if len(rows) > 8:
            print('             · ... %d more' % (len(rows)-8))
        report.append({'pack':name,'gate':gname,'ok':ok,'detail':detail,'rows':len(rows)})
print('\n===== OVERALL: %s =====' % ('GREEN' if overall else 'RED'))
if os.environ.get('N6_JSON'):
    open(os.environ['N6_JSON'],'w').write(json.dumps(report,indent=1))
sys.exit(0 if overall else 1)
