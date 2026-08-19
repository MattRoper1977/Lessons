#!/usr/bin/env python3
"""SCA-1 Track D: LO/SC <-> SoW row alignment + keyword coverage."""
import re,csv,glob,os,collections
SOW={
 "BUILD":{"sheet":"BUILD Weekly - Autumn","rows":{
   "W3":("C34","Compare animals with and without a backbone (vertebrates and invertebrates)."),
   "W4":("C35","Explain how muscles work in pairs with bones to make the body move."),
   "W5":("C36","Identify that humans and animals need the right types and amount of nutrition."),
   "W6":("C37","Sort foods into groups and describe a balanced diet (links PSHE / Foodwise)."),
   "W7":("C38","Explain that animals cannot make their own food; they get it from what they eat.")}},
 "GROW":{"sheet":"GROW Weekly - Autumn","rows":{
   "W3":("C34","Explore friction and how it can be helpful or unhelpful."),
   "W4":("C35","Investigate mechanisms: levers, pulleys and gears."),
   "W5":("C36","Plan and carry out a fair test about forces; record results."),
   "W6":("C37","Describe the movement of the Earth and other planets around the Sun."),
   "W7":("C38","Describe the movement of the Moon around the Earth.")}},
 "LAUNCH":{"sheet":"LAUNCH Weekly - Autumn","rows":{
   "W3":("C34","Calculate magnification (links Maths; record in spreadsheet)."),
   "W4":("C35","Explain diffusion."),
   "W5":("C36","Explain osmosis (core practical; data-logging)."),
   "W6":("C37","Explain active transport."),
   "W7":("C38","Topic 1 review & exam-style questions.")}}}
KEY={ # keywords the SoW row implies, checked against lesson prose
 ("BUILD","W3"):["backbone","vertebrate","invertebrate","skeleton"],
 ("BUILD","W4"):["muscle","pair","contract","relax","bone"],
 ("BUILD","W5"):["nutrition","energy","growth","repair"],
 ("BUILD","W6"):["group","balanced","protein","dairy"],
 ("BUILD","W7"):["food chain","plant","animal","eat"],
 ("GROW","W3"):["friction","surface","helpful","unhelpful"],
 ("GROW","W4"):["lever","pulley","gear","pivot"],
 ("GROW","W5"):["fair test","repeat","variable","record"],
 ("GROW","W6"):["orbit","planet","gravity","Sun"],
 ("GROW","W7"):["Moon","phase","orbit","Earth"],
 ("LAUNCH","W3"):["magnification","resolution","microscope","micrometre"],
 ("LAUNCH","W4"):["diffusion","gradient","concentration","particle"],
 ("LAUNCH","W5"):["osmosis","partially permeable","water","potato"],
 ("LAUNCH","W6"):["active transport","energy","respiration","gradient"],
 ("LAUNCH","W7"):["command word","describe","explain","evaluate"]}
PROSE="/home/user/Lessons/_sca1/streams"
def prose_for(pw,wk):
    out=""
    for fp in glob.glob(f"{PROSE}/{pw}__SCI_*.html.prose.txt"):
        if re.search(rf"_{wk}[AB]_|_{wk}L\d_", os.path.basename(fp)): out+=open(fp,encoding='utf-8').read()
    return out
align=[]; kw=[]
for pw,d in SOW.items():
    for wk,(cell,text) in sorted(d["rows"].items()):
        p=prose_for(pw,wk)
        if not p: align.append(dict(pathway=pw,week=wk,sheet=d["sheet"],cell=cell,sow_text=text,
                                    verdict="NO-PROSE",evidence="")); continue
        ks=KEY[(pw,wk)]
        found=[k for k in ks if re.search(re.escape(k),p,re.I)]
        missing=[k for k in ks if k not in found]
        verdict="ALIGNED" if not missing else ("PARTIAL" if len(found)>=len(ks)/2 else "MISALIGNED")
        align.append(dict(pathway=pw,week=wk,sheet=d["sheet"],cell=cell,sow_text=text,
                          verdict=verdict,evidence=f"{len(found)}/{len(ks)} keywords present; missing={missing}"))
        for k in ks:
            n=len(re.findall(re.escape(k),p,re.I))
            kw.append(dict(pathway=pw,week=wk,keyword=k,occurrences=n,
                           status="TAUGHT" if n else "ASKED-NEVER-TAUGHT/ABSENT"))
for name,data,cols in [("sow_alignment",align,["pathway","week","sheet","cell","sow_text","verdict","evidence"]),
                       ("keywords_sow",kw,["pathway","week","keyword","occurrences","status"])]:
    with open(f"/home/user/Lessons/_sca1/tables/{name}.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); [w.writerow(x) for x in data]
print("=== SoW ALIGNMENT ===")
for a in align: print(f"  {a['pathway']:7s} {a['week']} {a['sheet']}!{a['cell']}  {a['verdict']:11s} {a['evidence']}")
print()
print("verdicts:",dict(collections.Counter(a['verdict'] for a in align)))
miss=[k for k in kw if not k['occurrences']]
print(f"keywords absent from lesson prose: {len(miss)}")
for m in miss: print(f"   {m['pathway']} {m['week']} '{m['keyword']}'")
