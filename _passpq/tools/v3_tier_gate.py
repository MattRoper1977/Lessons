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
# Every LIVE PEQ-bearing surface, not just the v3 trees. The first pass of E1 missed
# `Personal Effectiveness (PEQ L1)` in the GROW hub and START_HERE and two claims wrapped
# in <b> tags in LAUNCH — all of them live surfaces naming Level 1 as the level. Widened
# so that miss goes red rather than passing.
LIVE  = [p for p in glob.glob('GROW_Estate_v3/**/*.*', recursive=True) +
                    glob.glob('LAUNCH_Estate_v3/**/*.*', recursive=True) +
                    glob.glob('GROW_ASDAN/**/*.*', recursive=True) +
                    glob.glob('LAUNCH_ASDAN/**/*.*', recursive=True)
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

# ---- Level 2 sweep (pass PEQ-L2K) ------------------------------------------
# PEQ-E3 E1 removed every L2 PEQ claim from the live surfaces. The owner ruling of
# 2026-08-21 re-introduces EXACTLY the ruled strings below, scoped to the LAUNCH
# suite (the in-deck L2 route) and to GROW_ASDAN/PEQ_L2_Kitchen/ (the L2 lane of
# the Kitchen year, gated by l2k_gates.py). Anything else that names Level 2, an
# L2 unit code, or an L2 qualification on a live surface goes red here.
L2_PAT = re.compile(r'Level\s*2|\bL2\b|\b(?:ComSk2|DecMkSk2|LSk2|TmWkSk2|CrThSk2|WellbLe2)\b')
# negative statements — true claims of absence, kept verbatim on out-of-scope mirrors
L2_ALLOWED_ANY = [
    'no Level 2 is registered or claimed',
    'no Level 2 registration',
    # the 29 short-course decks' held-out stems — DECISIONS.md §3 J5: NOT PEQ claims,
    # deliberately out of PEQ-E3's scope and out of PEQ-L2K's; inherited, not new
    'Stretch (L2 standard)',
    'the L2 evaluation standard in one question',     # same held-out family (ENT_W6)
    # v3 mirror's true meta-statement about that held-out stretch wording:
    'L2 wording in the 2026/27 PEQ hub is stretch language only, never an L2 registration.',
]
# the ruled strings — LAUNCH_ASDAN/** only (anchored exact matches)
L2_ALLOWED_LAUNCH = [
    'PEQ Entry 3 (Level 1 · Level 2 routes)',
    'ComSkE3 · ComSk1 · ComSk2 routes',
    '(Communication, ComSk1 · ComSk2 routes, begins)',
    '&#9744;&nbsp;<strong>Level 2</strong>',
    'Entry 3, Level 1 <em>or</em> Level 2, never more than one',
    'the staff-directed Level 2 route evidences Level 2',
    'a staff-directed Level 2 route sits in-deck &mdash; registration at any level stays a coordinator decision',
    'a staff-directed Level 2 route sits in-deck; registration at any level stays a coordinator decision',
    'the staff-directed Level 2 route sits in-deck, and no registration is claimed here',
    'with a staff-directed Level 2 route in-deck &mdash; never a registration claim',
    "getElementById('print-l2route')",
    'Any L2 registration is a coordinator decision &mdash; none is claimed here',
]

def strip_element(s, anchor):
    """remove a whole <div>...</div> element starting at anchor (balanced scan)"""
    i = s.find(anchor)
    while i >= 0:
        depth = 0
        for m in re.finditer(r'<div\b|</div>', s[i:]):
            depth += 1 if m.group(0).startswith('<div') else -1
            if depth == 0:
                s = s[:i] + s[i + m.end():]
                break
        else:
            break
        i = s.find(anchor)
    return s

def l2_view(p):
    if p.startswith('GROW_ASDAN/PEQ_L2_Kitchen/'):
        return ''                      # the L2 programme surface — l2k_gates.py owns it
    s = open(p, encoding='utf-8', errors='replace').read()
    if p.startswith('LAUNCH_ASDAN/PEQ/PEQ_W'):
        s = strip_element(s, '<div class="wit-panel" data-mbm-guide="1" data-l2route="1"')
        s = strip_element(s, '<div class="print-section" id="print-l2route">')
    allowed = L2_ALLOWED_ANY + (L2_ALLOWED_LAUNCH if p.startswith('LAUNCH_ASDAN/') else [])
    for a in sorted(allowed, key=len, reverse=True):
        s = s.replace(a, '')
    return s

l2 = [(p, m.group(0)) for p in LIVE for m in [L2_PAT.search(l2_view(p))] if m]
for p, frag in l2:
    fails.append('%s carries an unruled Level 2 string (%r)' % (p, frag))

print('v3 tier gate: %d decks · %d live files (v3 trees + GROW_ASDAN + LAUNCH_ASDAN)' % (len(DECKS), len(LIVE)))
print('  ComSk minima stated at a tier: %d %s' % (sum(minima_hits.values()), dict(minima_hits) or ''))
print('  tier stems: %s' % dict(stems))
print('  live files naming Level 1 as the level: %d' % len(l1))
print('  live files with an unruled Level 2 string: %d' % len(l2))
for x in fails: print('  FAIL  ' + x)
print('v3 tier gate: %s' % ('PASS' if not fails else '%d FAILURES' % len(fails)))
sys.exit(1 if fails else 0)
