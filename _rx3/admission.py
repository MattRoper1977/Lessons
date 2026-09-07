#!/usr/bin/env python3
"""RX3 P3: build the education publication exactly as the Lessons-caller publisher does
(Site builder at the given checkout, Lessons at a family branch worktree, Apps at the Site's pinned
revision) and report every output path whose bytes the Site admission registry does not admit.
--propose merges those paths into a registry copy: new paths as [digest, ARRIVING], changed paths as a
transition pair [main-digest, new-digest]."""
import argparse, json, subprocess, sys, hashlib
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument('--site', required=True); ap.add_argument('--lessons', required=True); ap.add_argument('--apps', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--label', required=True); ap.add_argument('--skip-build', action='store_true')
ap.add_argument('--propose', help='write a merged registry copy here')
a = ap.parse_args()
site = Path(a.site).resolve(); out = Path(a.out).resolve(); ds = site/'domain-split'
sys.path.insert(0, str(ds))
import education_publication_admission as adm
if not a.skip_build:
    out.mkdir(parents=True, exist_ok=True)
    for cmd in (['build_publications.py', '--lessons', a.lessons, '--output', str(out)],
                ['build_education.py', '--lessons', a.lessons, '--apps', a.apps, '--output', str(out)]):
        r = subprocess.run([sys.executable, str(ds/cmd[0])] + cmd[1:], text=True, capture_output=True)
        tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
        print(f'[{a.label}] {cmd[0]} rc={r.returncode}', *tail, sep='\n  ')
        if r.returncode and cmd[0] == 'build_publications.py':
            sys.exit('build_publications failed')
reg = adm.load_registry(ds/'education-publication-admission.json')
report = {'label': a.label, 'lessons': subprocess.run(['git', '-C', a.lessons, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(), 'trees': {}}
for name in adm.TREES:
    actual = adm.census(out/name); expected = reg['trees'][name]
    unrev = sorted(p for p in actual if p not in expected)
    changed = sorted(p for p in actual if p in expected and actual[p] not in adm.admitted(expected[p]))
    missing = sorted(p for p in expected if p not in actual and not adm.may_be_absent(expected[p]))
    report['trees'][name] = {'files': len(actual), 'unreviewed': {p: actual[p] for p in unrev}, 'changed': {p: {'registry': expected[p], 'built': actual[p]} for p in changed}, 'missing': missing}
    print(f'[{a.label}] {name}: files={len(actual)} UNREVIEWED={len(unrev)} CHANGED={len(changed)} MISSING={len(missing)}')
    for p in unrev: print('   UNREVIEWED', p)
    for p in changed: print('   CHANGED   ', p)
    for p in missing: print('   MISSING   ', p)
(out/f'admission-{a.label}.json').write_text(json.dumps(report, indent=1))
if a.propose:
    for name, t in report['trees'].items():
        files = reg['trees'][name]
        for p, d in t['unreviewed'].items(): files[p] = [d, adm.ARRIVING]
        for p, c in t['changed'].items():
            cur = files[p]
            if isinstance(cur, list): raise SystemExit('cannot widen an existing digest set: '+name+'/'+p+' '+str(cur))
            files[p] = [cur, c['built']]
    Path(a.propose).write_text(json.dumps(reg, ensure_ascii=False, indent=2)+'\n')
    print('proposal written', a.propose)
