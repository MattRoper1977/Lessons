#!/usr/bin/env python3
"""PEQ-E3 E3 — command-verb census by tier surface."""
import re, sys, glob, collections
TAG = re.compile(r'<(/?)(div|script|style)\b[^>]*>|<!--.*?-->', re.I | re.S)
def _scan(s):
    i = 0
    while True:
        m = TAG.search(s, i)
        if not m: return
        if m.group(0).startswith('<!--'): i = m.end(); continue
        name = (m.group(2) or '').lower()
        if name in ('script','style'):
            if m.group(1) == '/': i = m.end(); continue
            e2 = re.search(r'</%s\s*>' % name, s[m.end():], re.I)
            i = m.end() + (e2.end() if e2 else 0); continue
        yield ('close' if m.group(1) == '/' else 'open', m.start(), m.end())
        i = m.end()
def match_close(s, o):
    d = 0
    for k, a, b in _scan(s):
        if b <= o: continue
        if a == o: d = 1; continue
        if d == 0: continue
        d += 1 if k == 'open' else -1
        if d == 0: return a, b
    raise SystemExit('unmatched')

E3_VERBS = ['state','list','identify','name','say','point to','choose','sort','match','complete','give']
L1_VERBS = ['outline','describe','give examples','give a range of examples']
ALL = re.compile(r'\b(state|list|identify|outline|describe|give examples of|give examples|'
                 r'give a range of examples|explain|evaluate|justify|analyse|compare)\b', re.I)

TIER = {'supported':'E3','standard':'E3','stretch':'L1'}

def sections(s):
    out=[]
    for pid in re.findall(r'<div[^>]*id="(print-scaffold-\w+|print-worksheet-\w+|arrival-\w+|exit-\w+)"', s):
        m=re.search(r'<div[^>]*id="%s"'%pid, s); a=m.start(); _,b=match_close(s,a)
        tier=pid.rsplit('-',1)[-1]
        if tier in TIER: out.append((pid,tier,s[a:b]))
    return out

def text(x): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',x))

rows=collections.Counter(); detail=collections.defaultdict(list)
for f in sorted(glob.glob('GROW_ASDAN/PEQ/PEQ_W*.html'))+sorted(glob.glob('LAUNCH_ASDAN/PEQ/PEQ_W*.html')):
    s=open(f,encoding='utf-8').read()
    for pid,tier,seg in sections(s):
        want=TIER[tier]
        for m in ALL.finditer(text(seg)):
            v=m.group(0).lower()
            lvl = 'E3' if v in ('state','list','identify') else 'L1' if v.startswith(('outline','describe','give example','give a range')) else 'L2+'
            ok = (lvl==want) or (want=='L1' and lvl=='E3')   # L1 may use an easier verb; never top up
            rows[(want,v,'OK' if ok else 'OFF-PITCH')]+=1
            if not ok: detail[f.split('/')[-1]].append((pid,tier,v))
print('%-6s %-26s %-10s %s' % ('tier','verb','verdict','n'))
for (want,v,verd),n in sorted(rows.items(), key=lambda x:(-x[1])):
    print('%-6s %-26s %-10s %d' % (want,v,verd,n))
print('\nOFF-PITCH stems, per file:')
for f,items in sorted(detail.items()):
    for pid,tier,v in items: print('   %-50s %-26s %-10s %r' % (f[:50],pid,tier,v))
print('\ntotal off-pitch: %d' % sum(n for (w,v,verd),n in rows.items() if verd=='OFF-PITCH'))

sys.exit(1 if sum(n for (w,v,verd),n in rows.items() if verd=='OFF-PITCH') else 0)
