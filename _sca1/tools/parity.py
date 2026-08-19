#!/usr/bin/env python3
"""SCA-1 Track C: screen<->print parity of the independent task per tier.
Tier for independent/print rows is carried by the glyph, not data-tier."""
import csv,re,collections,difflib
rows=list(csv.DictReader(open("/home/user/Lessons/_sca1/tables/questions_raw.csv")))
GLYPH={'◆':'Supported','▲':'Standard','★':'Stretch'}
def tier_of(r):
    m=re.search(r'[◆▲★]', r['stem'])
    if m: return GLYPH[m.group(0)]
    if r['tier'] in ('Supported','Standard','Stretch'): return r['tier']
    return None
def norm(s):
    s=re.sub(r'(Supported|Standard|Stretch) independent route\s*','',s,flags=re.I)
    s=re.sub(r'🧰\s*Scaffold.*$','',s)
    s=re.sub(r'[^a-z0-9 ]',' ',s.lower())
    return re.sub(r'\s+',' ',s).strip()
byfile=collections.defaultdict(lambda: collections.defaultdict(lambda: {'screen':[],'print':[]}))
for r in rows:
    if not r['file'].startswith(('BUILD','GROW','LAUNCH')): continue
    if r['surface']=='screen' and r['slide_type']!='independent': continue
    t=tier_of(r)
    if not t: continue
    n=norm(r['stem'])
    if len(n)>18: byfile[r['file']][t][r['surface']].append(n)
out=[]
for f,tiers in sorted(byfile.items()):
    for t in ('Supported','Standard','Stretch'):
        s=tiers.get(t)
        if not s: 
            out.append(dict(file=f,tier=t,status='NO-ROWS',detail='',best=0.0,screen='',print_=''));continue
        sc,pr=s['screen'],s['print']
        if not sc or not pr:
            out.append(dict(file=f,tier=t,status='MISSING-SURFACE',detail=f"screen={len(sc)} print={len(pr)}",
                            best=0.0,screen=(sc[0][:150] if sc else ''),print_=(pr[0][:150] if pr else '')));continue
        best=0;bs=bp=''
        for a in sc:
            for b in pr:
                r2=difflib.SequenceMatcher(None,a,b).ratio()
                if r2>best: best,bs,bp=r2,a,b
        out.append(dict(file=f,tier=t,status='OK' if best>=0.6 else 'DIVERGENT',
                        detail=f"screen_n={len(sc)} print_n={len(pr)}",best=round(best,3),
                        screen=bs[:180],print_=bp[:180]))
with open("/home/user/Lessons/_sca1/tables/parity.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=["file","tier","status","detail","best","screen","print_"]);w.writeheader();[w.writerow(x) for x in out]
print("parity rows:",len(out),dict(collections.Counter(x['status'] for x in out)))
for x in out:
    if x['status'] in ('DIVERGENT','MISSING-SURFACE'):
        print(f"\n [{x['status']}] {x['file'][:42]} / {x['tier']} sim={x['best']} {x['detail']}")
        print(f"    screen: {x['screen'][:140]}")
        print(f"    print : {x['print_'][:140]}")
