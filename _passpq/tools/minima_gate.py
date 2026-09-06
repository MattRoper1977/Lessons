#!/usr/bin/env python3
"""PEQ-E3 E2 control — assert every tier surface states the minimum for ITS level.

Supported/Standard evidence ComSkE3, so they must carry the Entry 3 figures and must
NOT carry an L1-only figure. Stretch evidences ComSk1 and must carry the L1 figures.
The staff brief must name BOTH floors. A deliberately mis-set minimum fails here.
"""
import re, sys, glob
sys.path.insert(0, '/tmp/claude-0/-home-user-Lessons/f0b62ee6-863a-5c76-96eb-f17745970589/scratchpad')
try:
    from movepa import match_close
except ImportError:
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
                e = re.search(r'</%s\s*>' % name, s[m.end():], re.I)
                i = m.end() + (e.end() if e else 0); continue
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

L1_ONLY = [r'\b3 minutes\b', r'\b8 minutes\b', r'\b250 words\b', r'\bat least four questions\b',
           r'two positive outcomes', r'two areas to develop', r'\b4 components\b']
E3_MARK  = [r'\b2 minutes\b', r'\b100 words\b', r'\b2 min\+', r'2 minutes spoken',
            r'a positive outcome', r'an area to develop', r'talk 2 min']

def sections(s, ids):
    out = {}
    for pid in ids:
        m = re.search(r'<div[^>]*id="%s"' % pid, s)
        if m:
            a = m.start(); _, b = match_close(s, a); out[pid] = s[a:b]
    return out

def text(x): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))

fails = []; checked = 0
for f in sorted(glob.glob('LAUNCH_ASDAN/PEQ/PEQ_W*.html')):
    s = open(f, encoding='utf-8').read()
    name = f.split('/')[-1]
    lower = ['print-scaffold-standard','print-worksheet-standard','print-scaffold-supported',
             'print-worksheet-supported','arrival-standard','exit-standard']
    for pid, seg in sections(s, lower).items():
        t = text(seg); checked += 1
        for p in L1_ONLY:
            if re.search(p, t, re.I):
                fails.append('%s %s carries the LEVEL 1 figure %s but evidences ComSkE3' % (name, pid, p))
    for pid, seg in sections(s, ['print-worksheet-stretch']).items():
        checked += 1
        # a Stretch surface that states a review/activity minimum must state the L1 one
        t = text(seg)
        if re.search(r'positive outcome|area', t, re.I) and not re.search(r'two positive outcomes', t, re.I):
            fails.append('%s %s states a review minimum that is not the Level 1 one' % (name, pid))
    if 'what the unit requires at EACH level' in s:
        checked += 1
        for need in ['ComSkE3', 'ComSk1', 'at least 2 minutes', 'at least 100 words',
                     '3 minutes, 8 minutes or 250 words']:
            if need not in s:
                fails.append('%s staff brief does not name both floors — missing %r' % (name, need))

print('minima gate: %d tier surfaces checked' % checked)
for x in fails: print('  FAIL  ' + x)
print('minima gate: %s' % ('PASS' if not fails else '%d FAILURES' % len(fails)))
sys.exit(1 if fails else 0)
