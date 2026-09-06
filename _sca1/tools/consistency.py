#!/usr/bin/env python3
"""SCA-1 Track B part 2: term consistency + punctuation over PROSE stream."""
import re,glob,os,collections,csv
D="/home/user/Lessons/_sca1/streams"
def prose():
    for fp in sorted(glob.glob(D+"/*.prose.txt")):
        yield os.path.basename(fp).replace(".prose.txt",""), open(fp,encoding='utf-8',errors='replace').read()

TERMS={
 "backbone":      [r'\bbackbone\b', r'\bback bone\b', r'\bback-bone\b'],
 "newton-unit":   [r'\bnewtons?\b', r'\bNewtons?\b'],
 "partially-perm":[r'\bpartially permeable\b', r'\bsemi-?permeable\b', r'\bselectively permeable\b'],
 "vertebrate":    [r'\bvertebrates?\b', r'\binvertebrates?\b'],
 "antagonistic":  [r'\bantagonistic\b', r'\bantagonist pairs?\b'],
 "magnification": [r'\bmagnification\b', r'\bmagnifcation\b'],
 "micrometre":    [r'µm', r'μm', r'\bum\b', r'micrometre', r'micrometer'],
 "conc-units":    [r'mol\s*dm', r'mol/dm', r'moldm'],
 "air-resistance":[r'\bair resistance\b', r'\bair-resistance\b'],
 "water-resist":  [r'\bwater resistance\b', r'\bwater-resistance\b'],
 "food-chain":    [r'\bfood chains?\b', r'\bfood-chains?\b'],
 "exam-board-S":  [r'\bsulfur\b', r'\bsulphur\b'],
}
PUNCT=[
 ("double-space",  r'(?<=\S)  +(?=\S)'),
 ("space-before-punct", r'\s+[,.;:!?](?=\s|$)'),
 ("no-qmark-on-wh", r'^(?:What|Why|How|Which|Where|When|Who|Is|Are|Does|Do|Can|Could|Would|Should)\b[^?\n]{12,150}[.](?:\s|$)'),
 ("straight-apostrophe", r"\w'\w"),
 ("double-punct",  r'[.]{2}(?![.])|[?]{2}|[!]{2}'),
]
rows=[]; termhits=collections.defaultdict(lambda: collections.Counter())
for base,txt in prose():
    for fam,pats in TERMS.items():
        for p in pats:
            n=len(re.findall(p,txt))
            if n: termhits[fam][p]+=n
    for name,rx in PUNCT:
        for m in re.finditer(rx, txt, re.M):
            s=max(0,m.start()-70)
            rows.append(dict(file=base,check=name,found=repr(m.group(0))[:40],
                             context=re.sub(r'\s+',' ',txt[s:m.end()+70]).strip()))
# unmatched quotes per line
for base,txt in prose():
    for i,ln in enumerate(txt.split('\n'),1):
        for q,name in (('“”','curly-double'),):
            if ln.count(q[0])!=ln.count(q[1]):
                rows.append(dict(file=base,check='unmatched-'+name,found=f"{ln.count(q[0])} open / {ln.count(q[1])} close",
                                 context=re.sub(r'\s+',' ',ln)[:150]))
with open("/home/user/Lessons/_sca1/tables/consistency_raw.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["file","check","found","context"]); w.writeheader(); [w.writerow(r) for r in rows]
print("=== TERM CONSISTENCY (variant counts across PROSE, 50 files) ===")
for fam,c in sorted(termhits.items()):
    variants={k:v for k,v in c.items() if v}
    flag="  <-- MIXED" if len(variants)>1 else ""
    print(f"  {fam:16s} {variants}{flag}")
print("\n=== PUNCTUATION / GRAMMAR ===")
for k,v in collections.Counter(r['check'] for r in rows).most_common():
    print(f"  {k:24s} {v}")
