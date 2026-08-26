#!/usr/bin/env python3
"""Emit the classified per-lesson verdict table (markdown) from verified signals."""
import json
rows=json.load(open("_passsl/verdict_rows.json"))

def classify(r):
    f=r["file"]; suite=r["suite"]; codes="; ".join(r["codes"])
    # Humanities Launch slides — self-declared SoW, NC (no code correct), SC+printpack
    if suite=="Launch/HUM slides":
        if r["file"].endswith("W8_OS_Map_Skills.html"):
            return ("PARTIAL","Self-labels Aut1 but OS-Map=Geography content sits in SoW Aut2; week-label vs term-mapping (4c gate)")
        return ("ALIGNED*","Self-declared SoW Aut1 Wk match; SC present; NC KS3/4 (no code correct). *pending SC-operationalisation spot-check")
    if suite=="Humanities_Teesside":
        return ("SOW-SILENT?","Pack/SoW support doc, not a weekly lesson; parallel to Launch/HUM slides — canonical? (decision)")
    # Creative Arts — Teesside (quarantined, SoW-labelled) vs Launch (older, no SoW label)
    if suite=="Art_Teesside/Launch (QUAR)":
        return ("DECISION/QUAR","SoW-labelled Aut1 8-wk arc (develop→experience→review) vs SoW 7-wk half-terms; QUARANTINED → propose-only; parallel to Launch/ART (canonical?)")
    if suite=="Launch/ART slides":
        return ("PARTIAL","Arts Award Silver present but NO self-SoW label, no 'Success looks like' idiom, theme not named — older v5-style; parallel to Art_Teesside/Launch (canonical?)")
    if suite=="Launch/Art (identity)":
        return ("SOW-SILENT?","v5 identity lessons (Art_L1/L2); no SoW week; likely legacy — report only")
    # Science
    if r["strand"].startswith("Science"):
        note=[]
        if "4SS0" in codes: note.append("cites off-map Edexcel IGCSE 4SS0 (N1 exception → DECISION, not auto-fix)")
        note.append("no self-SoW label; topic (respiration/acids/circuits/waves) = Combined/IGCSE content mapping to SoW Spring/Summer, not Autumn — term/topic mapping unresolved (4c)")
        cls = "MISALIGNED?" if "4SS0" in codes else "MAPPING-PENDING"
        return (cls,"; ".join(note))
    return ("REVIEW","")

print("| # | Strand | File | self-SoW | wk | SC | code(visible) | Class | Note |")
print("|--|--|--|--|--|--|--|--|--|")
from collections import Counter
cc=Counter()
for i,r in enumerate(rows,1):
    cls,note=classify(r); cc[cls]+=1
    print(f"| {i} | {r['strand']} | `{r['file']}` | {r['self_sow'] or '—'} | {r['week_of'] or '—'} | {r['success']} | {'; '.join(r['codes']) or '—'} | **{cls}** | {note} |")
print("\n### Class tally")
for k,v in cc.most_common(): print(f"- {k}: {v}")
print(f"- TOTAL rows: {len(rows)}")
