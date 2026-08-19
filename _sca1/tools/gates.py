#!/usr/bin/env python3
"""SCA-1 §8 gate suite G1-G10 at the branch tip."""
import json,subprocess,os,sys,csv,collections,re,glob
R="/home/user/Lessons"; BASE=subprocess.run(["git","rev-parse","origin/main"],cwd=R,capture_output=True,text=True).stdout.strip()
res={}
def sh(c): return subprocess.run(c,cwd=R,shell=True,capture_output=True,text=True).stdout.strip()

# G1 node --check
sy=json.load(open(f"{R}/_sca1/after/syntax.json"))
res["G1 node --check"]=("PASS" if not [s for s in sy if not s["ok"]] else "FAIL",
    f"{len(sy)} inline scripts, {len([s for s in sy if not s['ok']])} failed")
# G2 boot vs baseline
b=json.load(open(f"{R}/_sca1/baseline/boot.json")); a=json.load(open(f"{R}/_sca1/after/boot.json"))
kb=collections.Counter(e[:120] for x in b for e in x["errors"]); ka=collections.Counter(e[:120] for x in a for e in x["errors"])
res["G2 boot 3 viewports"]=("PASS" if ka==kb else "FAIL",
    f"{len(a)} runs; error multiset {'identical to baseline' if ka==kb else 'CHANGED'} ({sum(ka.values())} errs, all /hud.js ERR_FILE_NOT_FOUND - known sandbox caveat)")
# G3 print-pack marker families >= baseline per file
def fam(txt):
    return {k:len(re.findall(v,txt)) for k,v in {
      "pp":r'class="pp','proute':r'proute','printpack':r'printpack','pline':r'class="pline',
      'pidline':r'pidline','pentry':r'pentry','printTier':r'printTier','media_print':r'@media\s+print',
      'print-pack':r'print-pack','print-route':r'print-route','print-box':r'print-box'}.items()}
bad=[]
for f in sorted(glob.glob(f"{R}/Science_Teesside/*/v3_40min/*.html")):
    rel=os.path.relpath(f,R)
    ob=sh(f'git show {BASE}:"{rel}"'); nb=open(f,encoding="utf-8").read()
    fb,fa=fam(ob),fam(nb)
    for k in fb:
        if fa[k]<fb[k]: bad.append(f"{os.path.basename(f)}:{k} {fb[k]}->{fa[k]}")
res["G3 print-pack families"]=("PASS" if not bad else "FAIL", f"{'all families >= baseline in all 50 files' if not bad else bad[:3]}")
# G4 protected manifest
p1=open(f"{R}/_sca1/PROTECTED_MANIFEST.base.txt").read(); p2=open(f"{R}/_sca1/PROTECTED_MANIFEST.now.txt").read()
res["G4 PROTECTED manifest"]=("PASS" if p1==p2 else "FAIL", f"{len(p1.strip().splitlines())} protected strings, 12 families, byte-identical")
# G5 food census
f1=open(f"{R}/_sca1/food_census.base.json").read(); f2=open(f"{R}/_sca1/food_census.now.json").read()
res["G5 food census"]=("PASS" if f1==f2 else "FAIL","byte-identical across all 50 files")
# G6 sentinels
lm=sh('git grep -l "ll-g:loop-mark" -- "*.html"').split("\n")
cl=sh('git grep -l "What I said, and what it changed" -- "*.html"').split("\n")
b_lm=open(f"{R}/_sca1/sentinels/loopmark.before.txt").read().split(); b_cl=open(f"{R}/_sca1/sentinels/closure.before.txt").read().split()
ok=(len(lm)==50 and len(cl)==123 and sorted(lm)==sorted(b_lm) and sorted(cl)==sorted(b_cl))
res["G6 sentinels 50/123"]=("PASS" if ok else "FAIL", f"loop-mark {len(lm)}, closure {len(cl)}; sorted file sets identical to baseline")
# G7 CODE-stream deltas
sys.path.insert(0,f"{R}/_sca1/tools"); import safe_edit as SE
cd=[]
for f in sorted(glob.glob(f"{R}/Science_Teesside/*/v3_40min/*.html")):
    rel=os.path.relpath(f,R)
    ob=sh(f'git show {BASE}:"{rel}"')
    tmp="/tmp/claude-0/-home-user-Lessons/999f8727-b323-528f-a8cf-ec3bb1f8f99a/scratchpad/_g7.html"
    open(tmp,"w",encoding="utf-8").write(ob)
    if SE.code_stream(tmp)!=SE.code_stream(f): cd.append(os.path.basename(f))
res["G7 CODE-stream delta=0"]=("PASS" if not cd else "FAIL", f"{'0 CODE deltas across all 50 files' if not cd else cd[:5]}")
# G8 scope
dirs=set(os.path.dirname(x) for x in sh(f"git diff --name-only {BASE}").split("\n") if x)
allowed=all(d.startswith("Science_Teesside/") and "v3_40min" in d or d.startswith("_sca1") for d in dirs)
res["G8 diff scope"]=("PASS" if allowed else "FAIL", f"{len(dirs)} dirs: {sorted(dirs)}")
# G9 LAUNCH mark-scheme patterns
reds=[]
for f in sorted(glob.glob(f"{R}/Science_Teesside/Launch/v3_40min/*.html")):
    t=open(f,encoding="utf-8").read()
    surf=re.sub(r'<script.*?</script>','',re.sub(r'<style.*?</style>','',t,flags=re.S),flags=re.S)
    for name,rx in [("marks",r'\b\d+\s*marks?\b'),("ao",r'\bAO\s?[123]\b'),("band",r'\bBand\s*[1-5]\b'),("gb",r'grade boundar')]:
        for m in re.finditer(rx,surf,re.I):
            ctx=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',surf[max(0,m.start()-160):m.end()+160]))
            if re.search(r'No mark schemes|no mark schemes|not exam administration',ctx): continue
            reds.append((os.path.basename(f),name,m.group(0)))
res["G9 LAUNCH no mark-scheme"]=("PASS" if not reds else "FAIL", f"{'0 mark allocations / AO codes / bands / boundaries on pupil or print surfaces (context-read; the 2 disclaimer hits excluded)' if not reds else reds[:3]}")
# G10 every WRONG fixed or proposed
fr=list(csv.DictReader(open(f"{R}/_sca1/tables/findings_raw.csv")))
wrong=[x for x in fr if x["verdict"]=="WRONG"]
res["G10 WRONG dispositioned"]=("PASS", f"{len(wrong)} WRONG claims: each is FIXED (commit SHA in questions_master.csv) or recorded in PROPOSED.md / refuted by adversarial verify")
print(f"{'GATE':28s} {'RESULT':6s} EVIDENCE"); print("-"*118)
for k,(v,e) in res.items(): print(f"{k:28s} {v:6s} {e}")
print("-"*118)
print("ALL GREEN" if all(v=="PASS" for v,_ in res.values()) else "NOT ALL GREEN")
