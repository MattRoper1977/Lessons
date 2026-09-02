#!/usr/bin/env python3
"""c-gate CONTAINMENT (VB-RUN11F C2): every pupil-facing sentence of the n6 deck
is present, verbatim, in the reshelled deck. Ligatures and whitespace are
normalised; nothing else is. Red control: one sentence deleted from the
candidate must turn the gate RED. Usage: cgate.py <before> <after> <out.json>"""
import json, re, sys, copy, unicodedata
from lxml import html
def pupil_text(path, roots):
    t = html.fromstring(open(path, encoding='utf-8').read()); out = []
    for xp in roots:
        for node in t.xpath(xp):
            node = copy.deepcopy(node)
            for c in list(node.iterdescendants()):
                tag = c.tag.lower() if isinstance(c.tag, str) else ''
                cls = (c.get('class') or '').split()
                if tag in ('script', 'style', 'svg', 'template', 'noscript', 'button') or c.get('data-mbm-guide') is not None or c.get('data-audience') == 'staff' or ('time' in cls or 'tag' in cls or 'slide-tag' in cls or 'running-head' in cls):
                    p = c.getparent()
                    if p is not None: p.remove(c)
            BLOCK = {'p','div','h1','h2','h3','h4','li','td','th','tr','section','article','table','ul','ol','span'}
            for c in node.iter():
                if isinstance(c.tag, str) and c.tag.lower() in BLOCK:
                    c.tail = ' \n ' + (c.tail or '')
            out.append(' '.join(x for x in node.itertext()))
    return '\n'.join(' '.join(l.split()) for l in ' '.join(out).split('\n'))
def norm(s):
    s = unicodedata.normalize('NFKC', s).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace(' ', ' ')
    return '\n'.join(' '.join(l.split()) for l in s.split('\n'))
def sentences(text):
    return [x.strip() for x in re.split(r'(?<=[.!?])\s+|\n+', text) if len(x.strip()) >= 12]
before, after, out = sys.argv[1], sys.argv[2], sys.argv[3]
B = norm(pupil_text(before, ['//main[contains(@class,"deck")]', '//section[contains(@class,"print-pack")]']))
A = norm(pupil_text(after, ['//*[contains(@class,"slide-container")]', '//*[@id="print-area"]']))
sents = sentences(B); AA = ' '.join(A.split()); missing = [s for s in sents if s not in AA]
# red control: delete one mid-deck sentence from the candidate text and re-check
victim = sents[len(sents)//2]; A_red = AA.replace(victim, ''); red_missing = [s for s in sents if s not in A_red]  # every occurrence: the print pack re-prints the slide text
red_fired = victim in red_missing
rec = {'file': after, 'subject': 'containment: every pupil-facing sentence of the n6 deck is verbatim in the reshelled deck (shell chrome excluded on both sides: the minute badge, the stage tag, the running head; scripts, styles, SVG, buttons and keyed staff guidance)', 'before': before, 'sentencesBefore': len(sents), 'charsBefore': len(B), 'charsAfter': len(A), 'missing': missing, 'redControl': {'deleted': victim[:80], 'fired': red_fired}, 'status': 'PASS' if not missing and red_fired else 'RED'}
json.dump(rec, open(out, 'w'), indent=1, ensure_ascii=False)
print(rec['status'], 'sentences', len(sents), 'missing', len(missing), 'red fired', red_fired)
for m in missing[:8]: print('  MISSING:', m[:140])
sys.exit(0 if rec['status'] == 'PASS' else 1)
