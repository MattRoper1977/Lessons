#!/usr/bin/env python3
"""SCA-1 §5 PROTECTED manifest v2.
Hashes each protected string WITH A BOUNDED CONTEXT WINDOW (+/-140 chars), not the whole
line -- these are single-long-line HTML files, so a whole-line hash flags any edit anywhere
on the line and is useless as a protection instrument.
Compares working tree against a given git ref."""
import re,os,sys,hashlib,json,subprocess,collections
ROOT="/home/user/Lessons"
FAM=[
 ("food-no-disclosure", r'personal diet|body or weight|weight disclosure|do not disclose'),
 ("food-no-bmi",        r'\bBMI\b'),
 ("food-no-calories",   r'calorie'),
 ("lundy-loop-mark",    r'll-g:loop-mark'),
 ("witness",            r'[Ww]itness'),
 ("grow-closure",       r'What I said, and what it changed'),
 ("grow-no-initial",    r'No adult initial is required'),
 ("grow-next-i-will",   r'Next I will'),
 ("launch-closure",     r'Closing the loop'),
 ("oak-url",            r'https?://[^"\s<]*(?:thenational\.academy|oaknational)[^"\s<]*'),
 ("word-bank",          r'[Ww]ord bank'),
 ("answer-key-data",    r'data-(?:correct|c|e|h|m|fix)="[^"]*"'),
 ("markscheme-caution", r'mark scheme|mark-scheme'),
 ("brand",              r'Made by Matt|Progress Schools'),
]
W=25  # tight: detects edits to the protected string and its immediate delimiters,
      # NOT unrelated prose elsewhere on the same (single-line) file. See _sca1/G4_NOTE.md
def files():
    out=[]
    for p in ("Build","Grow","Launch"):
        d=f"{ROOT}/Science_Teesside/{p}/v3_40min"
        out+= [f"Science_Teesside/{p}/v3_40min/{f}" for f in sorted(os.listdir(d)) if f.endswith(".html")]
    return out
def read_ref(rel, ref):
    if ref=="WORKTREE": return open(f"{ROOT}/{rel}",encoding='utf-8',errors='replace').read()
    r=subprocess.run(["git","show",f"{ref}:{rel}"],cwd=ROOT,capture_output=True,text=True)
    return r.stdout
def manifest(ref):
    rows=[]
    for rel in files():
        t=read_ref(rel,ref); base=os.path.basename(rel)
        for fam,rx in FAM:
            for m in re.finditer(rx,t):
                ctx=t[max(0,m.start()-W):m.end()+W]
                rows.append((base,fam,m.group(0)[:80],hashlib.sha256(ctx.encode()).hexdigest()[:24]))
    return rows
def census(ref):
    c={}
    for rel in files():
        t=read_ref(rel,ref); base=os.path.basename(rel)
        c[base]={w:len(re.findall(r'\b'+w+r'\b',t,re.I)) for w in
                 ["diet","calorie","calories","BMI","weight","obese","obesity","nutrition","food","healthy"]}
    return c
if __name__=="__main__":
    ref=sys.argv[1] if len(sys.argv)>1 else "WORKTREE"
    tag=sys.argv[2] if len(sys.argv)>2 else ref.replace("/","_")
    rows=manifest(ref); cen=census(ref)
    with open(f"{ROOT}/_sca1/PROTECTED_MANIFEST.{tag}.txt","w") as f:
        for r in rows: f.write("\t".join(r)+"\n")
    json.dump(cen,open(f"{ROOT}/_sca1/food_census.{tag}.json","w"),indent=1,sort_keys=True)
    print(f"[{tag}] protected strings={len(rows)}  families={len(set(r[1] for r in rows))}")
    print(f"[{tag}] by family: {dict(collections.Counter(r[1] for r in rows))}")
