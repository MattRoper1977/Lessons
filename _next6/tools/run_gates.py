#!/usr/bin/env python3
"""Run the N6 gate battery over every pack. Usage: run_gates.py <packs_root> [intake_root]"""
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates as G

root = sys.argv[1]
intake = sys.argv[2] if len(sys.argv) > 2 else None
reflist = os.environ.get('S23_NAMES')

packs = sorted(d for d in glob.glob(os.path.join(root,'*')) if os.path.isdir(d))
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
