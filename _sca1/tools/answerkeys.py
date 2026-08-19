#!/usr/bin/env python3
"""SCA-1: extract every encoded answer key with its stem and options, from the real bytes.
Anchors on the option-button GROUP that carries data-correct / data-c, never a byte window."""
import re,glob,os,csv
TAG=re.compile(r'<[^>]+>')
def clean(s): return re.sub(r'\s+',' ',TAG.sub(' ',s)).strip()
rows=[]
for f in sorted(glob.glob('Science_Teesside/*/v3_40min/SCI_*.html')):
    t=open(f).read(); base=os.path.basename(f)
    pw=[x for x in ('Build','Grow','Launch') if f'/{x}/' in f][0].upper()
    # find containers holding data-correct= or data-c=
    for m in re.finditer(r'data-(?:correct|c)="(\d+)"', t):
        idx=int(m.group(1))
        # widen left to the enclosing block that holds the option buttons
        start=t.rfind('<div', max(0,m.start()-3000), m.start())
        end=t.find('</div>', m.end())
        blk=t[start if start>0 else max(0,m.start()-3000): m.end()+2500]
        # options = buttons carrying data-i= (index) in order
        opts=re.findall(r'data-i="(\d+)"[^>]*>((?:(?!</button>).)*)</button>', blk, re.S)
        if not opts:
            opts=[(str(i),o) for i,o in enumerate(re.findall(r'<button[^>]*class="option[^"]*"[^>]*>((?:(?!</button>).)*)</button>', blk, re.S))]
        opts=[(int(i),clean(o)) for i,o in opts]
        opts=sorted({i:o for i,o in opts}.items())
        # stem = last question-mark text before the options
        pre=t[max(0,m.start()-1600):m.start()]
        qs=re.findall(r'>([^<>]{12,190}\?)<', pre)
        stem=clean(qs[-1]) if qs else ''
        if not opts: continue
        corr=dict(opts).get(idx,'(index out of range)')
        rows.append(dict(pathway=pw,file=base,correct_index=idx,correct_text=corr,
                         stem=stem,options=' | '.join(f'[{i}]{o}' for i,o in opts)))
with open('_sca1/tables/answer_keys.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=['pathway','file','correct_index','correct_text','stem','options']);w.writeheader();[w.writerow(r) for r in rows]
print(f'answer keys extracted: {len(rows)}')
for r in rows:
    print(f"\n{r['pathway']:6s} {r['file'][:40]:40s} correct=[{r['correct_index']}] -> {r['correct_text'][:60]}")
    print(f"   Q: {r['stem'][:100]}")
    print(f"   O: {r['options'][:200]}")
