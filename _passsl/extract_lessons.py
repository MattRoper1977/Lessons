#!/usr/bin/env python3
"""Pass SL — per-lesson extraction across ALL surfaces (slide + print pack).
Strips data-URIs and script/style before text measurement (ground rule 6).
Emits _passsl/lesson_extract.json + a readable audit stub."""
import re, html, json, glob, os

# ---- LAUNCH population (mechanical globs; near-twins kept, flagged later) ----
GROUPS = {
    "Launch/Art (identity)":      ["Launch/Art_L*_*.html"],
    "Launch/ART slideshows":      ["Launch/Slideshows/LAUNCH_ART_W*.html"],
    "Launch/HUM slideshows":      ["Launch/Slideshows/LAUNCH_HUM_W*.html"],
    "Art_Teesside/Launch (QUAR)": ["Art_Teesside/Launch/LAUNCH_ART_W*.html"],
    "Humanities_Teesside (LAUNCH)":["Humanities_Teesside/LAUNCH_*.html"],
    "Science/biology":            ["biology/*.html"],
    "Science/chemistry":          ["chemistry/*.html"],
    "Science/physics":            ["2 Physics 10/*.html","2 Physics 10/Waves/*.html"],
}

CODE_RE = re.compile(r'\b(1BI0|1SC0|4BI1|4CH1|4PH1|8700|8702|8145|8062|8061|8100|8939|1MA1|NEN0|5972|PEQ|UAS|Trinity Arts|Arts Award|Silver|Gold|Foundation|Higher tier|Higher-tier)\b')
THEMES = {
    "Identity & Belonging":"Autumn", "Resilience & Change":"Spring",
    "Our World, My Future":"Summer", "Our World My Future":"Summer",
}

def visible(raw):
    raw = re.sub(r'<script\b.*?</script>','',raw,flags=re.S|re.I)
    raw = re.sub(r'<style\b.*?</style>','',raw,flags=re.S|re.I)
    raw = re.sub(r'data:image/[^"\')\s]+','',raw)
    t = re.sub(r'<[^>]+>',' ',raw)
    return re.sub(r'\s+',' ',html.unescape(t)).strip()

def grab(pat, txt, n=200):
    m = re.search(pat, txt, re.I)
    return txt[m.start():m.start()+n].strip() if m else ""

records=[]
for group, patterns in GROUPS.items():
    files=[]
    for p in patterns: files+=glob.glob(p)
    for f in sorted(set(files)):
        raw=open(f,encoding="utf-8",errors="replace").read()
        vt=visible(raw)
        rec={
          "group":group, "file":f,
          "bytes":len(raw), "datauris":len(re.findall(r'data:image',raw)),
          "has_printpack": bool(re.search(r'id="print-',raw)),
          "lundy_boxes": len(re.findall(r'lundy-box',raw)),
          "reduced_motion": bool(re.search(r'prefers-reduced-motion',raw)),
          "ll_g_sentinel": bool(re.search(r'\bll-g\b',raw)),
          # self-declared SoW mapping
          "self_sow": grab(r'Progress SoW[^A-Za-z0-9]{0,3}[^<]{0,80}', vt, 120),
          "week_of":  (re.search(r'Week\s+(\d+)\s+of\s+(\d+)', vt, re.I) or [None]),
          "ht_label": grab(r'\b(Aut|Spr|Sum)\s*[12]\b', vt, 12),
          # LO / SC idiom
          "enquiry":  grab(r'Enquiry[:\s]', vt, 160),
          "success":  grab(r'Success looks like', vt, 300),
          "codes": sorted(set(CODE_RE.findall(raw))),
          "theme": next((th for th in THEMES if th in vt), ""),
          "exit_present": bool(re.search(r'Exit Ticket', raw, re.I)),
        }
        wo=re.search(r'Week\s+(\d+)\s+of\s+(\d+)', vt, re.I)
        rec["week_of"]= f"{wo.group(1)}/{wo.group(2)}" if wo else ""
        records.append(rec)

json.dump(records, open("_passsl/lesson_extract.json","w"), indent=2, ensure_ascii=False)

# readable summary
print(f"{'FILE':64} {'wk':>5} {'ht':>5} {'thm':3} codes")
for r in records:
    print(f"{r['file'][-63:]:64} {r['week_of']:>5} {r['ht_label'][:5]:>5} "
          f"{('Y' if r['theme'] else '-'):>3} {','.join(r['codes'])[:40]}")
print(f"\nTOTAL lesson files extracted: {len(records)}")
by={}
for r in records: by[r['group']]=by.get(r['group'],0)+1
for g,n in by.items(): print(f"  {n:3d}  {g}")
