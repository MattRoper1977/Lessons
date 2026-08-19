#!/usr/bin/env python3
"""SCA-1 §1.2 inventory + §1.3 baseline instruments. Universe-explicit."""
import os, re, csv, hashlib, json, sys

ROOT = "/home/user/Lessons/Science_Teesside"
OUT  = "/home/user/Lessons/_sca1"
PATHWAYS = [("BUILD","Build"),("GROW","Grow"),("LAUNCH","Launch")]

# Print-pack marker families, derived empirically from bytes (not assumed).
PRINT_MARKERS = {
 "pp_class":      r'class="pp',
 "proute":        r'proute',
 "printpack":     r'printpack',
 "pline_class":   r'class="pline',
 "pidline":       r'pidline',
 "pentry":        r'pentry',
 "printTier":     r'printTier',
 "printA":        r'printA',
 "printB":        r'printB',
 "afterprint":    r'afterprint',
 "media_print":   r'@media\s+print',
}
SENTINELS = {
 "loop_mark":     r'll-g:loop-mark',
 "closure_line":  r'What I said, and what it changed',
}

def sha(b): return hashlib.sha256(b).hexdigest()

def scan(path):
    raw = open(path,'rb').read()
    t = raw.decode('utf-8', 'replace')
    r = {
      "path": os.path.relpath(path, "/home/user/Lessons"),
      "file": os.path.basename(path),
      "bytes": len(raw),
      "sha256": sha(raw),
      "scripts": len(re.findall(r'<script\b', t)),
      "witness": len(re.findall(r'witness', t, re.I)),
      "word_help": len(re.findall(r'WORD HELP', t)),
      "word_bank": len(re.findall(r'word bank', t, re.I)),
      "oak_links": len(re.findall(r'thenational\.academy|oaknational', t, re.I)),
      "slides": len(re.findall(r'class="slide"', t)),
    }
    for k,p in PRINT_MARKERS.items(): r["pm_"+k] = len(re.findall(p, t))
    for k,p in SENTINELS.items():     r["sn_"+k] = len(re.findall(p, t))
    return r

rows=[]
for label, folder in PATHWAYS:
    d = os.path.join(ROOT, folder, "v3_40min")
    for fn in sorted(os.listdir(d)):
        fp = os.path.join(d, fn)
        if not os.path.isfile(fp): continue
        if fn.endswith(".html"):
            r = scan(fp)
        else:
            raw=open(fp,'rb').read()
            r={"path":os.path.relpath(fp,"/home/user/Lessons"),"file":fn,"bytes":len(raw),
               "sha256":sha(raw),"scripts":0,"witness":0,"word_help":0,"word_bank":0,
               "oak_links":0,"slides":0}
            for k in PRINT_MARKERS: r["pm_"+k]=0
            for k in SENTINELS: r["sn_"+k]=0
        r["pathway"]=label
        r["kind"]=("lesson" if re.match(r'SCI_[BGL]_W',fn) else
                   "index" if fn=="index.html" else
                   "manifest" if fn.endswith(".json") else "doc")
        rows.append(r)

cols=["pathway","kind","file","path","bytes","sha256","scripts","slides","witness",
      "word_help","word_bank","oak_links"]+["pm_"+k for k in PRINT_MARKERS]+["sn_"+k for k in SENTINELS]
os.makedirs(OUT+"/tables", exist_ok=True)
with open(OUT+"/tables/inventory.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({c:r.get(c,"") for c in cols})

print(f"inventory rows: {len(rows)}")
for label,_ in PATHWAYS:
    sub=[r for r in rows if r["pathway"]==label]
    les=[r for r in sub if r["kind"]=="lesson"]
    print(f"\n{label}: {len(sub)} files ({len(les)} lessons)")
    print(f"  dialect families present (lessons): " +
          ", ".join(k for k in PRINT_MARKERS if any(r['pm_'+k] for r in les)))
    print(f"  witness/file: {sorted(set(r['witness'] for r in les))}  "
          f"WORD HELP/file: {sorted(set(r['word_help'] for r in les))}  "
          f"closure/file: {sorted(set(r['sn_closure_line'] for r in les))}  "
          f"loopmark/file: {sorted(set(r['sn_loop_mark'] for r in les))}")
