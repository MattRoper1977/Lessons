#!/usr/bin/env python3
"""SCA-1 s2 questions_master.csv — every QUESTIONS row with a verdict."""
import csv,re,os,collections,json,glob,subprocess
Q="/home/user/Lessons/_sca1/tables/questions_raw.csv"
rows=list(csv.DictReader(open(Q)))
find=list(csv.DictReader(open("/home/user/Lessons/_sca1/tables/findings_raw.csv")))
keys=list(csv.DictReader(open("/home/user/Lessons/_sca1/tables/answer_keys.csv")))
# map: file -> list of (quoted current_text, verdict, fix_type)
byfile=collections.defaultdict(list)
for f in find: byfile[f['file']].append(f)
# encoded answers per file
ans=collections.defaultdict(list)
for k in keys: ans[k['file']].append(k)
FIXED={  # applied in this pass, with commit subject
 'SCI_B_W7A_Food_Sources_Explore.html':'FIXED prediction language (e690c8f)',
 'SCI_B_W7B_Food_Chain_Do.html':'FIXED prediction language (e690c8f)',
 'SCI_B_W4A_Muscles_Explore.html':'FIXED elastic->string safety (8b40204)',
 'SCI_B_W4B_Muscle_Model_Do.html':'FIXED elastic->string safety (8b40204)',
 'SCI_G_W3A_Friction_Explore.html':'FIXED sandpaper removed (8084da9)',
 'SCI_G_W6B_Earth_And_Planets_Do.html':'FIXED Neptune scale 1.2->3.5 km (8084da9)',
 'SCI_L_W4L1_Diffusion_Introduce.html':'FIXED gradient bridge + false caveat (927be7a)',
 'SCI_L_W4L2_Diffusion_Lungs_Explore.html':'FIXED gradient bridge (927be7a)',
 'SCI_L_W6L1_Active_Transport_Introduce.html':'FIXED gradient bridge + lab scope (927be7a)',
 'SCI_L_W6L3_Compare_Transport_Do.html':'FIXED gradient bridge + arrival note (927be7a)',
}
out=[]
for r in rows:
    base=r['file'].split('__')[-1]
    pw=r['file'].split('__')[0]
    # default verdict
    verdict='CORRECT'; note=''
    # encoded answer rows
    enc=''
    for k in ans.get(base,[]):
        if k['correct_text'] and k['correct_text'][:30].lower() in r['stem'].lower():
            enc=f"correct=[{k['correct_index']}] {k['correct_text'][:60]}"
    # findings touching this file
    hit=[f for f in byfile.get(base,[]) if f['current_text'] and
         (f['current_text'][:40] in r['stem'] or r['stem'][:40] in f['current_text'])]
    if hit:
        h=hit[0]; verdict=h['verdict']; note=h['fix_type']+': '+h['issue'][:120]
    if base in FIXED and hit: note=FIXED[base]+' | '+note
    out.append(dict(pathway=pw,file=base,slide=r['slide_type'],tier=r['tier'] or '',
                    surface=r['surface'],qnum=r['qnum'],stem=r['stem'][:300],
                    encoded_answer=enc,verdict=verdict,disposition=note))
cols=['pathway','file','slide','tier','surface','qnum','stem','encoded_answer','verdict','disposition']
with open("/home/user/Lessons/_sca1/tables/questions_master.csv","w",newline="") as fh:
    w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); [w.writerow(x) for x in out]
print(f"questions_master rows: {len(out)}")
print("verdicts:",dict(collections.Counter(x['verdict'] for x in out)))
print("by pathway:",dict(collections.Counter(x['pathway'] for x in out)))
print("rows carrying an encoded answer:",sum(1 for x in out if x['encoded_answer']))
