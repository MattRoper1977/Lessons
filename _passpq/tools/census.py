#!/usr/bin/env python3
"""PEQ-E3 §1 census: every file whose CONTENT names PEQ, a PEQ unit code, or
'Personal Effectiveness'. Predicates are printed with the counts."""
import re, os, sys, collections

CODES = ['ComSkE3','DecMkSkE3','LSkE3','TmWkSkE3','ThSkE3','WellbLeE3',
         'ComSk1','DecMkSk1','LSk1','TmWkSk1','ThSk1','WellbLe1',
         'ComSk2','DecMkSk2','LSk2','TmWkSk2','CrThSk2','WellbLe2',
         'ComSk3','DecMkSk3','LSk3','TmWkSk3','CrThSk3','WellbLe3']
P_PEQ  = re.compile(r'\bPEQ\b')
P_PE   = re.compile(r'Personal Effectiveness', re.I)
P_CODE = re.compile(r'\b(' + '|'.join(sorted(CODES, key=len, reverse=True)) + r')\b')

SKIP_DIRS = {'node_modules', '.git'}
EXTS = {'.html','.md','.json','.js','.mjs','.py','.txt','.csv','.svg'}

rows = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fn in files:
        p = os.path.join(root, fn).lstrip('./')
        if os.path.splitext(fn)[1].lower() not in EXTS: continue
        try: s = open(p, encoding='utf-8', errors='replace').read()
        except Exception: continue
        peq = len(P_PEQ.findall(s)); pe = len(P_PE.findall(s))
        codes = collections.Counter(P_CODE.findall(s))
        if not (peq or pe or codes): continue
        rows.append((p, peq, pe, codes))

def zone(p):
    for z in ('GROW_ASDAN/PEQ/','LAUNCH_ASDAN/PEQ/','GROW_ASDAN/','LAUNCH_ASDAN/',
              'BUILD_ASDAN/','_passpq/','Humanities_Teesside/','Art_Teesside/'):
        if p.startswith(z): return z
    return p.split('/')[0] + '/' if '/' in p else '(root)'

print('PEQ-E3 CENSUS — %d files match at least one predicate\n' % len(rows))
byz = collections.defaultdict(list)
for r in rows: byz[zone(r[0])].append(r)
for z in sorted(byz, key=lambda z: (-len(byz[z]), z)):
    print('== %s  (%d files)' % (z, len(byz[z])))
    for p, peq, pe, codes in sorted(byz[z]):
        cs = ' '.join('%s:%d' % (k, v) for k, v in sorted(codes.items()))
        print('   %-72s PEQ:%-4d PersEff:%-3d %s' % (p[:72], peq, pe, cs))
    print()
tot_codes = collections.Counter()
for _,_,_,c in rows: tot_codes.update(c)
print('unit-code totals estate-wide:', dict(sorted(tot_codes.items())))
