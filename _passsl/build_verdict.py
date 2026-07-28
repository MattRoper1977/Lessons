#!/usr/bin/env python3
"""Pass SL — build the per-lesson verdict table from verified (visible-text) signals.
Codes detected on VISIBLE TEXT only (raw-HTML scan had script/CSS false positives)."""
import re, html, json, glob

GROUPS = [
 ("Creative Arts","Launch/Art (identity)",      ["Launch/Art_L*_*.html"]),
 ("Creative Arts","Launch/ART slides",          ["Launch/Slideshows/LAUNCH_ART_W*.html"]),
 ("Humanities",   "Launch/HUM slides",          ["Launch/Slideshows/LAUNCH_HUM_W*.html"]),
 ("Creative Arts","Art_Teesside/Launch (QUAR)", ["Art_Teesside/Launch/LAUNCH_ART_W*.html"]),
 ("Humanities",   "Humanities_Teesside",        ["Humanities_Teesside/LAUNCH_*.html"]),
 ("Science-Bio",  "biology",                    ["biology/*.html"]),
 ("Science-Chem", "chemistry",                  ["chemistry/*.html"]),
 ("Science-Phys", "physics",                    ["2 Physics 10/*.html","2 Physics 10/Waves/*.html"]),
]
# codes that are REAL accreditation strings (validated in visible text w/ context)
CODE_RE = re.compile(r'(Edexcel[^.,;<\n]{0,45}|1BI0|1SC0|4BI1|4CH1|4PH1|4SS0|8145|8700|8702|8062|8061|8939|Arts Award (?:Silver|Gold|Bronze)|Trinity Arts|National Curriculum|NC KS[0-9/]+|AQA UAS|\bUAS\b|PEQ)', re.I)

def vis(f):
    raw=open(f,encoding="utf-8",errors="replace").read()
    r=re.sub(r'<script\b.*?</script>','',raw,flags=re.S|re.I)
    r=re.sub(r'<style\b.*?</style>','',r,flags=re.S|re.I)
    r=re.sub(r'data:image/[^"\')\s]+','',r)
    return raw, re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',r))).strip()

rows=[]
for strand,suite,pats in GROUPS:
    files=[]
    for p in pats: files+=glob.glob(p)
    for f in sorted(set(files)):
        raw,vt=vis(f)
        codes=sorted({re.sub(r'\s+',' ',c).strip() for c in CODE_RE.findall(vt)})
        wo=re.search(r'Week\s+(\d+)\s+of\s+(\d+)',vt,re.I)
        sow=re.search(r'Progress SoW[^A-Za-z]{0,3}([A-Za-z][^.·]{0,40})',vt)
        rows.append({
          "strand":strand,"suite":suite,"file":f,
          "self_sow": (sow.group(1).strip()[:38] if sow else ""),
          "week_of": (f"{wo.group(1)}/{wo.group(2)}" if wo else ""),
          "success": "Y" if re.search(r'Success looks like',vt,re.I) else "-",
          "theme": "Y" if re.search(r'Identity & Belonging|Resilience & Change|Our World',vt,re.I) else "-",
          "printpack":"Y" if re.search(r'id="print-',raw) else "-",
          "codes": codes,
        })
json.dump(rows,open("_passsl/verdict_rows.json","w"),indent=2,ensure_ascii=False)
print(f"{'FILE':60}{'selfSoW':16}{'wk':>5}{'SC':>3}{'th':>3}{'pp':>3}  codes")
for r in rows:
    print(f"{r['file'][-59:]:60}{r['self_sow'][:15]:16}{r['week_of']:>5}{r['success']:>3}{r['theme']:>3}{r['printpack']:>3}  {'; '.join(r['codes'])[:52]}")
print(f"\nrows={len(rows)}")
