#!/usr/bin/env python3
"""CX3 single writer: re-cut the catalogue digests for exemplar lessons replaced IN PLACE (same path, new bytes).

For each path given: SCIENCE_WEEK_BINDINGS.json sourceSha256 (Science only; the calendar binding is unchanged) with a reviewed note,
then the repo's own catalogue builder (tools/catalogue/build_catalogue.py) regenerates TERM_AND_STYLE_EVIDENCE.json and the shelves.
Writes nothing else. Usage: python3 tools/cx3_recut.py --date 2026-09-09 path [path ...]
"""
import argparse, hashlib, json, subprocess, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument('--date', required=True); ap.add_argument('paths', nargs='+'); a = ap.parse_args()
def sha(p): return hashlib.sha256(open(os.path.join(R, p), 'rb').read()).hexdigest()
wbp = os.path.join(R, 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'); wb = json.load(open(wbp, encoding='utf-8')); ent = wb['entries']
recut = []
for p in a.paths:
    if p in ent:
        if ent[p].get('sourceSha256') != sha(p):
            ent[p]['sourceSha256'] = sha(p); ent[p]['reviewed'] = {'date': a.date, 'reason': 'CX3 exemplar re-cut in place (same path, attached bytes); the calendar binding is unchanged'}; recut.append(p)
open(wbp, 'w', encoding='utf-8').write(json.dumps(wb, ensure_ascii=False, indent=2) + '\n')
print('SCIENCE_WEEK_BINDINGS sourceSha256 re-cut:', len(recut))
r = subprocess.run([sys.executable, os.path.join(R, 'tools/catalogue/build_catalogue.py')], cwd=R, capture_output=True, text=True)
print('build_catalogue.py rc', r.returncode, (r.stdout + r.stderr).strip()[-400:])
sys.exit(r.returncode)
