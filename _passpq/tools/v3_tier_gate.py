#!/usr/bin/env python3
"""PEQ-E3 P1 control — the twelve *_Estate_v3 PEQ decks.

E1 is the family that applies here. E2 and E3 are CONDITIONAL ("wherever those decks
state a minimum or use a command verb at a tier"), so this gate measures the condition
rather than assuming it, and fails if the condition ever becomes true unnoticed.

  - no ComSk minimum may be stated at a tier without carrying the level split
  - no tier stem may use a verb above its level (Supported/Standard = E3 verbs;
    Stretch = L1 verbs, and may sit easier but never higher)
  - no live v3 file may name Level 1 as THE level
"""
import re, sys, glob, collections

DECKS = sorted(glob.glob('GROW_Estate_v3/GROW_ASDAN/PEQ_*.html')) + \
        sorted(glob.glob('LAUNCH_Estate_v3/LAUNCH_ASDAN/PEQ_*.html'))
LIVE  = [p for p in glob.glob('GROW_Estate_v3/**/*.*', recursive=True) +
                    glob.glob('LAUNCH_Estate_v3/**/*.*', recursive=True)
         if p.endswith(('.html', '.json'))]

# ComSk minima, either level — if one appears at a tier the split must be stated
MINIMA = re.compile(r'\b(?:250|100)\s*words\b|\b(?:2|3|5|8)\s*minutes?\b(?!\s*\.)|'
                    r'(?:two|three|four|2|3|4)\s+(?:components|difficulties|audience questions)|'
                    r'(?:two|2)\s+positive outcomes', re.I)
E3_VERBS = {'state', 'list', 'identify', 'name', 'say', 'point', 'sort', 'match', 'choose', 'complete', 'add'}
L1_VERBS = {'outline', 'describe', 'give'}
ABOVE_L1 = {'evaluate', 'justify', 'explain', 'analyse', 'compare'}
STEM = re.compile(r'\b(Supported|Standard|Stretch)\s*:\s*([a-z]+)', re.I)

def text(p):
    s = open(p, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<style.*?</style>', ' ', s, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))

fails = []
minima_hits = collections.Counter(); stems = collections.Counter()
for p in DECKS:
    t = text(p)
    for m in MINIMA.finditer(t):
        ctx = t[max(0, m.start() - 60):m.end() + 40]
        if re.search(r'\bmin\b|minutes\.\s|⏱', ctx):    # timing chip, not a ComSk minimum
            continue
        minima_hits[m.group(0).lower()] += 1
        if 'Entry 3' not in ctx and 'Level 1' not in ctx:
            fails.append('%s states the minimum %r at a tier without naming its level'
                         % (p.split('/')[-1], m.group(0)))
    for m in STEM.finditer(t):
        tier, verb = m.group(1).lower(), m.group(2).lower()
        stems['%s: %s' % (tier, verb)] += 1
        if verb in ABOVE_L1:
            fails.append('%s stem "%s: %s" uses a verb above Level 1' % (p.split('/')[-1], tier, verb))
        elif tier in ('supported', 'standard') and verb in L1_VERBS:
            fails.append('%s stem "%s: %s" uses a Level 1 verb at an Entry 3 tier'
                         % (p.split('/')[-1], tier, verb))

l1 = [p for p in LIVE if re.search(r'PEQ L1|PEQ Level 1(?! stretch)',
                                   open(p, encoding='utf-8', errors='replace').read())]
for p in l1: fails.append('%s still names Level 1 as the level' % p)

print('v3 tier gate: %d decks · %d live files' % (len(DECKS), len(LIVE)))
print('  ComSk minima stated at a tier: %d %s' % (sum(minima_hits.values()), dict(minima_hits) or ''))
print('  tier stems: %s' % dict(stems))
print('  live files naming Level 1 as the level: %d' % len(l1))
for x in fails: print('  FAIL  ' + x)
print('v3 tier gate: %s' % ('PASS' if not fails else '%d FAILURES' % len(fails)))
sys.exit(1 if fails else 0)
