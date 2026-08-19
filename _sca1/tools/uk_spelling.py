#!/usr/bin/env python3
"""SCA-1 Track B: British English over the PROSE stream only. CODE is exempt."""
import re,os,glob,csv,sys,json,collections

PROSE_DIR="/home/user/Lessons/_sca1/streams"

# US -> UK. Each entry: (regex over prose, UK form, family)
RULES=[
 (r'\b(\w*)ize\b','-ise','ize-verb'), (r'\b(\w*)izes\b','-ises','ize-verb'),
 (r'\b(\w*)ized\b','-ised','ize-verb'), (r'\b(\w*)izing\b','-ising','ize-verb'),
 (r'\b(\w*)ization\b','-isation','ize-noun'), (r'\b(\w*)izations\b','-isations','ize-noun'),
 (r'\bcolor(s|ed|ing|ful|less)?\b','colour','colour'),
 (r'\bfavorite(s)?\b','favourite','colour'),
 (r'\bbehavior(s|al)?\b','behaviour','colour'),
 (r'\bflavor(s|ed|ing)?\b','flavour','colour'),
 (r'\bhonor(s|ed|able)?\b','honour','colour'),
 (r'\blabor(s|ed|ing)?\b','labour','colour'),
 (r'\bneighbor(s|ing|hood)?\b','neighbour','colour'),
 (r'\bvapor(s|ise|ize)?\b','vapour','colour'),
 (r'\bharbor(s)?\b','harbour','colour'),
 (r'\bcenter(s|ed|ing)?\b','centre','re-ending'),
 (r'\bmeter(s)?\b','metre','re-ending'),
 (r'\bliter(s)?\b','litre','re-ending'),
 (r'\bfiber(s)?\b','fibre','re-ending'),
 (r'\btheater(s)?\b','theatre','re-ending'),
 (r'\bgray(s|er|ish)?\b','grey','misc'),
 (r'\bmold(s|ed|ing|y)?\b','mould','misc'),
 (r'\bsmolder','smoulder','misc'),
 (r'\bprogram(s)?\b','programme (unless computer program)','programme'),
 (r'\baluminum\b','aluminium','misc'),
 (r'\bmath\b','maths','misc'),
 (r'\bdefense(s)?\b','defence','ce-se'),
 (r'\boffense(s)?\b','offence','ce-se'),
 (r'\bpretense\b','pretence','ce-se'),
 (r'\blicense\b','licence (noun) / license (verb)','ce-se'),
 (r'\bpractice(s|d)?\b','practise (verb) / practice (noun)','ce-se-check'),
 (r'\benroll(s|ed|ing|ment)?\b','enrol / enrolment','misc'),
 (r'\bfulfill(s|ed|ing|ment)?\b','fulfil / fulfilment','misc'),
 (r'\bskillful\b','skilful','misc'),
 (r'\btraveled\b','travelled','double-l'), (r'\btraveling\b','travelling','double-l'),
 (r'\blabeled\b','labelled','double-l'), (r'\blabeling\b','labelling','double-l'),
 (r'\bmodeled\b','modelled','double-l'), (r'\bmodeling\b','modelling','double-l'),
 (r'\bfueled\b','fuelled','double-l'), (r'\bfueling\b','fuelling','double-l'),
 (r'\bcanceled\b','cancelled','double-l'), (r'\bcanceling\b','cancelling','double-l'),
 (r'\bmarveled\b','marvelled','double-l'),
 (r'\bjewelry\b','jewellery','misc'),
 (r'\bplow(s|ed|ing)?\b','plough','misc'),
 (r'\bcatalog(s)?\b(?!ue)','catalogue','misc'),
 (r'\bdialog\b','dialogue','misc'),
 (r'\banalyze(s|d)?\b','analyse','ize-verb'), (r'\banalyzing\b','analysing','ize-verb'),
 (r'\bparalyze','paralyse','ize-verb'),
 (r'\bapologize','apologise','ize-verb'),
 (r'\besophagus\b','oesophagus','ae-oe'),
 (r'\bfetus\b','foetus','ae-oe'),
 (r'\banemia\b','anaemia','ae-oe'),
 (r'\bhemoglobin\b','haemoglobin','ae-oe'),
 (r'\bdiarrhea\b','diarrhoea','ae-oe'),
 (r'\bcecum\b','caecum','ae-oe'),
 (r'\bedema\b','oedema','ae-oe'),
 (r'\bleukemia\b','leukaemia','ae-oe'),
 (r'\bpediatric','paediatric','ae-oe'),
 (r'\bgage\b','gauge','misc'),




 (r'\bsulphur\b','sulfur (exam-board spelling wins)','board-spelling'),
]
# whitelist: legitimate -ize/-ise etc that are NOT US, and terms we must not flag
ALLOW=re.compile(r'\b(size|sizes|sized|sizing|resize|prize|prizes|seize|seizes|capsize|'
                 r'maize|assize|downsize|upsize|oversize|midsize|'
                 r'exercise|exercises|exercised|exercising|advertise|advertises|advertising|'
                 r'supervise|supervises|supervised|supervising|revise|revises|revised|revising|'
                 r'devise|devises|devised|advise|advises|advised|advising|surprise|surprises|surprised|'
                 r'comprise|comprises|comprised|compromise|despise|disguise|improvise|televise|'
                 r'franchise|merchandise|enterprise|expertise|arise|arises|arising|rise|rises|'
                 r'wise|likewise|otherwise|clockwise|anticlockwise|precise|concise|paradise|promise|'
                 r'premise|premises|treatise|noise|poise|praise|raise|raises|raised|bruise|cruise|'
                 r'guise|louise|demise|excise|incise|revised)\b', re.I)

GRAMMAR=[
 (r'  +','double space','punct'),
 (r'\bits\'','stray apostrophe (its\')','punct'),
 (r'\bdont\b|\bcant\b|\bwont\b|\bdoesnt\b|\bisnt\b|\bwerent\b|\bwasnt\b|\bhasnt\b|\bhavent\b|\bdidnt\b',
  'missing apostrophe','punct'),
]

def scan():
    rows=[]; universe=0; files=0
    for fp in sorted(glob.glob(PROSE_DIR+"/*.prose.txt")):
        base=os.path.basename(fp).replace(".prose.txt","")
        txt=open(fp,encoding='utf-8',errors='replace').read()
        universe+=len(txt); files+=1
        for ln_no, ln in enumerate(txt.split('\n'),1):
            for rx,uk,fam in RULES:
                for m in re.finditer(rx, ln, re.I):
                    w=m.group(0)
                    if ALLOW.fullmatch(w) or ALLOW.match(w): continue
                    s=max(0,m.start()-70)
                    rows.append(dict(file=base,line=ln_no,family=fam,found=w,uk_form=uk,
                                     context=ln[s:m.end()+70].strip()))
            for rx,label,fam in GRAMMAR:
                for m in re.finditer(rx, ln):
                    s=max(0,m.start()-70)
                    rows.append(dict(file=base,line=ln_no,family=fam,found=repr(m.group(0)),uk_form=label,
                                     context=ln[s:m.end()+70].strip()))
    return rows, universe, files

if __name__=="__main__":
    rows,universe,files=scan()
    os.makedirs("/home/user/Lessons/_sca1/tables",exist_ok=True)
    with open("/home/user/Lessons/_sca1/tables/uk_spelling_raw.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["file","line","family","found","uk_form","context"])
        w.writeheader(); [w.writerow(r) for r in rows]
    print(f"PROSE universe: {files} files, {universe} chars")
    print(f"raw hits: {len(rows)}")
    print("\nby family:")
    for k,v in collections.Counter(r['family'] for r in rows).most_common():
        print(f"  {k:16s} {v}")
    print("\nby token (top 40):")
    for k,v in collections.Counter(r['found'].lower() for r in rows).most_common(40):
        print(f"  {k:24s} {v}")
