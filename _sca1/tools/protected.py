#!/usr/bin/env python3
"""SCA-1 §5 PROTECTED manifest + food census. Hash before, re-verify after every commit."""
import re,os,sys,hashlib,glob,json

FILES=[]
for p in ["Build","Grow","Launch"]:
    FILES+=sorted(glob.glob(f"/home/user/Lessons/Science_Teesside/{p}/v3_40min/*.html"))

# Protected string families. Each = (family, regex). Whole matched LINE is hashed.
FAM=[
 ("food-no-disclosure", r'no personal diet|personal diet|body or weight|weight disclosure|do not disclose'),
 ("food-no-bmi",        r'\bBMI\b|calculate BMI'),
 ("food-no-calories",   r'calorie target|calorie targets|not calorie|calories'),
 ("lundy-loop-mark",    r'll-g:loop-mark'),
 ("witness",            r'witness'),
 ("grow-closure",       r'What I said, and what it changed'),
 ("grow-no-initial",    r'No adult initial is required'),
 ("grow-next-i-will",   r'Next I will'),
 ("launch-closure",     r'Closing the loop'),
 ("oak-url",            r'https?://[^"\s<]*(?:thenational\.academy|oaknational)[^"\s<]*'),
 ("word-bank",          r'word bank'),
 ("answer-key-data",    r'data-correct="[^"]*"|data-fix="[^"]*"|data-c="[^"]*"|data-e="[^"]*"|data-h="[^"]*"|data-m="[^"]*"'),
 ("seed",               r'\bseed\b|seeded'),
 ("markscheme-caution", r'mark scheme|mark-scheme|markscheme'),
 ("brand",              r'Made by Matt|Progress Schools'),
]
# LAUNCH RED patterns: forbidden on pupil/print surfaces
RED=[("marks-alloc", r'\[\s*\d+\s*marks?\s*\]|\(\s*\d+\s*marks?\s*\)|\b\d+\s*marks\b'),
     ("ao-code",     r'\bAO[123](?:\.\d)?\b'),
     ("band-desc",   r'\bBand\s+[1-5]\b|\bLevel\s+[1-3]\s+\(\d'),
     ("grade-bound", r'grade boundar')]

def lines(fp):
    return open(fp,encoding='utf-8',errors='replace').read().split('\n')

def build():
    out=[]; census={}
    for fp in FILES:
        base=os.path.basename(fp)
        ls=lines(fp)
        for i,ln in enumerate(ls,1):
            for fam,rx in FAM:
                for m in re.finditer(rx, ln, re.I):
                    h=hashlib.sha256(ln.encode()).hexdigest()
                    out.append(f"{base}\t{fam}\tL{i}\t{m.group(0)[:70]!r}\t{h}")
        txt="\n".join(ls)
        census[base]={
          "food_terms": {w: len(re.findall(r'\b'+w+r'\b', txt, re.I)) for w in
              ["diet","calorie","calories","BMI","weight","obese","obesity","slim","fat","healthy eating","nutrition","food"]},
        }
    return out, census

def red_scan():
    """LAUNCH RED — pupil/print surfaces only, context-read."""
    hits=[]
    for fp in FILES:
        if "/Launch/" not in fp: continue
        base=os.path.basename(fp)
        for i,ln in enumerate(lines(fp),1):
            for name,rx in RED:
                for m in re.finditer(rx, ln, re.I):
                    s=max(0,m.start()-140); ctx=re.sub(r'\s+',' ',ln[s:m.end()+140])
                    hits.append({"file":base,"line":i,"pattern":name,"match":m.group(0),"context":ctx})
    return hits

if __name__=="__main__":
    out,census=build()
    tag=sys.argv[1] if len(sys.argv)>1 else "before"
    d="/home/user/Lessons/_sca1"
    open(f"{d}/PROTECTED_MANIFEST.txt" if tag=="before" else f"{d}/PROTECTED_MANIFEST.{tag}.txt","w").write("\n".join(out)+"\n")
    json.dump(census, open(f"{d}/food_census.json" if tag=="before" else f"{d}/food_census.{tag}.json","w"), indent=1, sort_keys=True)
    reds=red_scan()
    json.dump(reds, open(f"{d}/launch_red.{tag}.json","w"), indent=1)
    joined="\n".join(out)
    print(f"[{tag}] protected lines={len(out)}  manifest sha={hashlib.sha256(joined.encode()).hexdigest()[:16]}")
    print(f"[{tag}] food census sha={hashlib.sha256(json.dumps(census,sort_keys=True).encode()).hexdigest()[:16]}")
    print(f"[{tag}] LAUNCH RED candidate hits={len(reds)} (context-read required, not yet verdicts)")
    import collections
    print("  by pattern:", dict(collections.Counter(h['pattern'] for h in reds)))
