#!/usr/bin/env python3
"""Pass SL — infer science-lesson -> SoW week mapping from topic keywords (D3).
No week-label assumptions; matches lesson topic to the SoW outcome that names it.
Flags low-confidence. Report-only artifact."""
import json, glob, re, html

W = json.load(open("_passsl/sow_extract/sow_weekly.json"))
SCI = [r for r in W if r["strand"].startswith("Science")]  # GCSE Bio + IGCSE option

def vt(f):
    raw=open(f,encoding="utf-8",errors="replace").read()
    raw=re.sub(r'<script\b.*?</script>','',raw,flags=re.S|re.I)
    raw=re.sub(r'<style\b.*?</style>','',raw,flags=re.S|re.I)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',raw))).lower()

# topic keyword -> (SoW route label, term/ht/week hint)
def best_match(text):
    # score each SoW week by keyword overlap with lesson text
    KW = {
      "respiration":"resp","aerobic":"resp","anaerobic":"resp","atp":"resp",
      "digestion":"digest","absorption":"digest","enzyme":"digest",
      "thorax":"vent","breath":"vent","ventilation":"vent","lung":"vent",
      "limewater":"resp",
      "indicator":"acid","ph scale":"acid","neutralis":"acid","acid":"acid","alkali":"acid","ions":"acid",
      "flame test":"anal","gas test":"anal","anion":"anal","cation":"anal","precipitate":"anal",
      "circuit":"elec","voltage":"elec","current":"elec","resistance":"elec","ohm":"elec","electron flow":"elec",
      "wave":"wave","frequency":"wave","wavelength":"wave","reflection":"wave","refraction":"wave","amplitude":"wave",
    }
    hits={}
    for kw,tag in KW.items():
        if kw in text: hits[tag]=hits.get(tag,0)+text.count(kw)
    if not hits: return ("(none)","", "LOW")
    tag=max(hits,key=hits.get)
    SOWMAP={
      "resp":("GCSE Bio ~Sum1 (exchange/transport region); respiration NOT an explicit SoW week","Sum1 W3-5 / SOW-SILENT?","MED"),
      "digest":("GCSE Bio — digestion/enzymes not an explicit SoW weekly outcome","(no direct week)","LOW"),
      "vent":("GCSE Bio Sum1 W4 'exchange surfaces & ventilation'","Sum Sum1 W4","HIGH"),
      "acid":("IGCSE-option Chem Spr1 W3 'acids, bases and preparing salts'","Spr Spr1 W3","HIGH"),
      "anal":("Chem qualitative analysis (flame/gas/anion) — Combined/IGCSE analysis, ~Spring chem","Spr chem (analysis)","MED"),
      "elec":("IGCSE-option Phys Spr1 W6–Spr2 W2 'circuits/current/voltage/resistance/power'","Spr Spr1W6-Spr2W2","HIGH"),
      "wave":("IGCSE-option Phys Spr2 W3 'waves – properties, reflection & refraction'","Spr Spr2 W3","HIGH"),
    }
    return SOWMAP[tag]

files=sorted(glob.glob("biology/*.html")+glob.glob("chemistry/*.html")+glob.glob("2 Physics 10/*.html")+glob.glob("2 Physics 10/Waves/*.html"))
print("| File | Inferred SoW target | Week | Conf |")
print("|--|--|--|--|")
from collections import Counter
conf=Counter()
for f in files:
    tgt,wk,c=best_match(vt(f)); conf[c]+=1
    print(f"| `{f}` | {tgt} | {wk} | {c} |")
print("\nConfidence tally:", dict(conf), "of", len(files), "files")
