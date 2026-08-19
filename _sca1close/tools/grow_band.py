#!/usr/bin/env python3
"""SCA-1 CLOSE v2 3d — GROW reading-band check. MEASURE ONLY, no edits.

Band supplied by the owner this session: reading age 8-12 ~ Flesch-Kincaid 3.0-7.0.
Selector and FK function are SCA-1's own (identical to the BUILD run): question stems
of >=25 characters from _sca1/tables/questions_raw.csv, FK =
0.39*(words/sentences) + 11.8*(syllables/words) - 15.59.
Out-of-band stems are reported for PROPOSED; nothing is rewritten.
"""
import csv, re, collections, json

LO, HI = 3.0, 7.0

def syll(w):
    w = re.sub(r'[^a-z]', '', w.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', w); w = re.sub(r'^y', '', w)
    return max(1, len(re.findall(r'[aeiouy]{1,2}', w)))

def fk(text):
    sents = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    words = re.findall(r"[A-Za-z’'-]+", text)
    if not words or not sents: return None
    return round(0.39 * (len(words) / len(sents)) + 11.8 * (sum(syll(w) for w in words) / len(words)) - 15.59, 1)

rows = list(csv.DictReader(open('_sca1/tables/questions_raw.csv')))
grow = [r for r in rows if r['file'].startswith('GROW')]
per = collections.defaultdict(list)
out = []
for r in grow:
    stem = r['stem']
    if len(stem) < 25: continue
    g = fk(stem)
    if g is None: continue
    inband = LO <= g <= HI
    per[r['file']].append(g)
    out.append(dict(file=r['file'], slide=r['slide_type'], tier=r['tier'], surface=r['surface'],
                    fk=g, inband=inband, stem=stem[:160]))

with open('_sca1close/tables/grow_band.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['file', 'slide', 'tier', 'surface', 'fk', 'inband', 'stem'])
    w.writeheader(); [w.writerow(x) for x in out]

print(f'GROW stems measured: {len(out)} (band {LO}-{HI} FK, reading age 8-12)\n')
print(f"{'lesson':46s} {'n':>4s} {'median':>7s} {'min':>6s} {'max':>6s} {'out':>4s}  verdict")
tot_out = 0
for f in sorted(per):
    v = sorted(per[f]); n = len(v)
    med = v[n // 2] if n % 2 else round((v[n // 2 - 1] + v[n // 2]) / 2, 1)
    o = [x for x in v if not (LO <= x <= HI)]
    tot_out += len(o)
    verdict = 'IN BAND' if not o else f'{len(o)} stem(s) out of band'
    print(f'{f[:46]:46s} {n:4d} {med:7.1f} {v[0]:6.1f} {v[-1]:6.1f} {len(o):4d}  {verdict}')
print(f'\nTOTAL out-of-band stems: {tot_out} of {len(out)}')

low = [x for x in out if x['fk'] < LO]
high = [x for x in out if x['fk'] > HI]
print(f'  below {LO} (easier than band): {len(low)}')
print(f'  above {HI} (harder than band): {len(high)}')
if high:
    print('\n  HARDER THAN BAND (these are the ones that matter -> PROPOSED):')
    for x in sorted(high, key=lambda y: -y['fk'])[:25]:
        print(f"    FK {x['fk']:4.1f}  {x['file'][:40]:40s} {x['tier']:10s} {x['surface']:7s} {x['stem'][:80]}")
json.dump({'low': len(low), 'high': len(high), 'total': len(out),
           'high_items': sorted(high, key=lambda y: -y['fk'])}, open('_sca1close/tables/grow_band_summary.json', 'w'), indent=1)
