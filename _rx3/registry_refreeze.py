#!/usr/bin/env python3
"""RX3 P4.1: the Site's frozen usage-registry baseline, measured with the check's own partition rule.
usage: registry_refreeze.py <Site domain-split dir> <build A> <build B>   (builds from _rx3/admission.py --out)
Prints each build's retained-row sha256 (what check_education_separation.py freezes) and the reviewed diff A -> B."""
import sys, json, hashlib, pathlib
site, A, B = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
sys.path.insert(0, str(site)); import check_education_separation as C
def retained(out):
    approved = {'/Lessons/Science_Teesside/Teaching_Packs/': json.loads((C.HERE/'science-download-usage-additions.json').read_text())}
    approved.update(json.loads(C.TEACHING_PACK_ADDITIONS.read_text()))
    rows = json.loads((out/'usage-registry.json').read_text()); lessons = out/'education-lessons'
    installed = {p: (lessons/p[len('/Lessons/'):]/'index.html').is_file() for p in approved}
    errs, ret = C.registry_partition(rows, approved, installed)
    return errs, ret, hashlib.sha256((json.dumps(ret, ensure_ascii=False, indent=2)+'\n').encode()).hexdigest()
ra, rb = retained(A), retained(B)
for name, (errs, ret, sha) in (('A '+A.name, ra), ('B '+B.name, rb)):
    print(f'{name}: retained {len(ret)} rows · sha256 {sha} · partition errors {errs or "none"} · check says {C.registry_errors(A if name.startswith("A") else B) or "PASS"}')
a = {r['route']: r for r in ra[1]}; b = {r['route']: r for r in rb[1]}
print(f'added {len(set(b)-set(a))} · removed {len(set(a)-set(b))} · changed {sum(1 for k in set(a)&set(b) if a[k]!=b[k])}')
for k in sorted(set(b)-set(a)): print('  +', k, b[k].get('source_ids'))
for k in sorted(set(a)-set(b)): print('  -', k)
for k in sorted(set(a)&set(b)):
    if a[k]!=b[k]:
        for f in a[k]:
            if a[k][f]!=b[k].get(f): print('  ~', k, f, repr(a[k][f])[:80], '->', repr(b[k].get(f))[:80])
