#!/usr/bin/env python3
"""SCA-1 Track C: question construction. Parity, leakage, command words, FK band."""
import csv,re,os,collections,json
rows=list(csv.DictReader(open("/home/user/Lessons/_sca1/tables/questions_raw.csv")))

def syll(w):
    w=re.sub(r'[^a-z]','',w.lower())
    if not w: return 0
    if len(w)<=3: return 1
    w=re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$','',w); w=re.sub(r'^y','',w)
    return max(1,len(re.findall(r'[aeiouy]{1,2}',w)))

def fk(text):
    sents=[s for s in re.split(r'[.!?]+',text) if s.strip()]
    words=re.findall(r"[A-Za-z’'-]+",text)
    if not words or not sents: return None
    return round(0.39*(len(words)/len(sents))+11.8*(sum(syll(w) for w in words)/len(words))-15.59,1)

band=[]
for r in rows:
    if len(r['stem'])<25: continue
    g=fk(r['stem'])
    if g is None: continue
    band.append(dict(file=r['file'],slide=r['slide_type'],tier=r['tier'],surface=r['surface'],
                     fk=g,words=len(re.findall(r"[A-Za-z’'-]+",r['stem'])),stem=r['stem'][:150]))
with open("/home/user/Lessons/_sca1/tables/reading_band.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["file","slide","tier","surface","fk","words","stem"]); w.writeheader(); [w.writerow(x) for x in band]

CMD={'BUILD':['name','say','point','sort','match','describe','circle','tick','draw','show','choose','label','find','use','write','put','look','count','tell','pick','add','read','copy','join','colour'],
     'GROW':['name','say','point','sort','match','describe','predict','explain','compare','measure','test','record','label','use','write','find','choose','show','draw','tick','circle','look','pick','add','read','check','plan','set'],
     'LAUNCH':['state','describe','explain','calculate','compare','evaluate','define','identify','suggest','name','give','determine','label','use','write','complete','draw','show','work','convert','find','read','tick','circle','match','sort','plan','check','pick','add','apply']}
ALL=sorted(set(sum(CMD.values(),[])))
cmdcount=collections.defaultdict(lambda: collections.Counter()); offpitch=[]
for r in rows:
    p='BUILD' if r['file'].startswith('BUILD') else 'GROW' if r['file'].startswith('GROW') else 'LAUNCH' if r['file'].startswith('LAUNCH') else None
    if not p: continue
    m=re.match(r"\s*[◆▲★☐·•]*\s*([A-Za-z]+)", r['stem'])
    if not m: continue
    v=m.group(1).lower()
    if v in ALL:
        cmdcount[p][v]+=1
        if v not in CMD[p]:
            offpitch.append(dict(pathway=p,file=r['file'],tier=r['tier'],surface=r['surface'],verb=v,stem=r['stem'][:140]))

leak=[]
for r in rows:
    for rx,why in [(r'\((?:answer|ans)\s*[:=]',"explicit answer marker"),
                   (r'\b(?:the answer is|answer:)\b',"answer stated in stem")]:
        if re.search(rx,r['stem'],re.I):
            leak.append(dict(file=r['file'],tier=r['tier'],surface=r['surface'],why=why,stem=r['stem'][:170]))
dneg=[]
for r in rows:
    n=len(re.findall(r"\b(not|never|no|none|cannot|can't|won't|don't|isn't|doesn't|without|neither|nor)\b",r['stem'].lower()))
    if n>=2: dneg.append(dict(file=r['file'],tier=r['tier'],surface=r['surface'],negs=n,stem=r['stem'][:170]))

for name,data,cols in [("cmd_offpitch",offpitch,["pathway","file","tier","surface","verb","stem"]),
                       ("leakage",leak,["file","tier","surface","why","stem"]),
                       ("double_negative",dneg,["file","tier","surface","negs","stem"])]:
    with open(f"/home/user/Lessons/_sca1/tables/{name}.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); [w.writerow(x) for x in data]

print(f"FK rows: {len(band)}  (report-only; no band supplied except BUILD ~6-9)")
for p in ['BUILD','GROW','LAUNCH']:
    s=sorted(b['fk'] for b in band if b['file'].startswith(p))
    if s: print(f"  {p:7s} n={len(s):4d} median={s[len(s)//2]:5.1f} mean={sum(s)/len(s):5.1f} p90={s[int(len(s)*.9)]:5.1f}")
print("\ncommand words (first verb):")
for p in ['BUILD','GROW','LAUNCH']: print(f"  {p:7s} {dict(cmdcount[p].most_common(8))}")
print(f"\noff-pitch verbs: {len(offpitch)}")
for o in offpitch[:15]: print(f"   {o['pathway']:6s} {o['file'][:32]:32s} '{o['verb']}' :: {o['stem'][:78]}")
print(f"\nleakage: {len(leak)}   double-negative: {len(dneg)}")
for d in dneg[:10]: print(f"   {d['file'][:34]:34s} n={d['negs']} :: {d['stem'][:95]}")
