#!/usr/bin/env python3
"""FEB destination-relative content floor with two-arm rendered blank test."""
from __future__ import annotations
import argparse, copy, hashlib, json, math, re, subprocess, unicodedata
from pathlib import Path
import fitz
from lxml import html
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[3]
BASELINES={
 "BUILD Science":["Science_Teesside/Build/W8-W13_2026-27/SCI_*.html"],
 "BUILD Humanities":["Humanities_Teesside/BUILD_W9-W14_2026-27/BUILD_HUM_*.html"],
 "BUILD ASDAN":["BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_*.html"],
 "GROW Science":["Science_Teesside/Grow/W8-W13_2026-27/SCI_*.html"],
 "GROW ASDAN":["GROW_ASDAN/Autumn2_W1-W6_2026-27/*.html"],
 "LAUNCH ASDAN":["LAUNCH_ASDAN/W7-W12_2026-27/lessons/**/*.html"],
 "LAUNCH Science":["Science_Teesside/Launch/W8-W13_2026-27/SCI_*.html"],
 "GROW Humanities":["Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_*.html"],
 "LAUNCH Humanities":["Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_*.html"],
}
WORD=re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")
LIG=str.maketrans({'ﬁ':'fi','ﬂ':'fl','ﬀ':'ff','ﬃ':'ffi','ﬄ':'ffl'})

def strip(node):
    for child in list(node.iterdescendants()):
        tag=child.tag.lower() if isinstance(child.tag,str) else ''
        classes=set((child.get('class') or '').split())
        if tag in {'script','style','noscript','template','svg'} or child.get('data-mbm-guide') is not None or child.get('data-audience','').lower()=='staff' or 'hero-visual' in classes:
            parent=child.getparent()
            if parent is not None: parent.remove(child)

def count_lesson(path):
    tree=html.fromstring(path.read_text(encoding='utf-8'));rows=[]
    nodes=tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
    for i,source in enumerate(nodes,1):
        node=copy.deepcopy(source);strip(node);text=' '.join(node.text_content().split())
        rows.append({'slide':i,'title':source.get('data-title') or '', 'wordCount':len(WORD.findall(unicodedata.normalize('NFKC',text))), 'deliberatePause':source.get('data-deliberate-pause')})
    return {'file':path.name,'totalWords':sum(r['wordCount'] for r in rows),'slides':rows}

def derive_floor(family):
 rows=[]
 for pattern in BASELINES[family]:
  for path in sorted(ROOT.glob(pattern)):
   try:
    measured=count_lesson(path)
   except Exception:
    continue
   if measured['totalWords']:
    rows.append({'path':str(path.relative_to(ROOT)),'words':measured['totalWords']})
 if len(rows)<2: raise SystemExit(f'MEASUREMENT INVALID: {family} p25 has {len(rows)} qualifying donor lessons')
 ordered=sorted(row['words'] for row in rows)
 p25=ordered[max(0,math.ceil(.25*len(ordered))-1)]
 return {'family':family,'patterns':BASELINES[family],'sample':rows,'sampleCount':len(rows),'p25':p25,'method':'nearest-rank p25 of own-family donor pack'}

def norm(text): return ' '.join(text.translate(LIG).split())
def pdf_measure(path):
    py=[norm(p.extract_text() or '') for p in PdfReader(path).pages]
    raw=subprocess.run(['pdftotext','-raw',str(path),'-'],check=True,text=True,capture_output=True).stdout
    po=[norm(x) for x in raw.split('\f')]
    if po and not po[-1]: po.pop()
    doc=fitz.open(path);ink=[]
    for page in doc:
        pix=page.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csGRAY,alpha=False)
        data=pix.samples;ink.append(sum(1 for value in data if value<245)/len(data))
    doc.close();pages=[]
    for i in range(max(len(py),len(po),len(ink))):
        a=len(py[i]) if i<len(py) else 0;b=len(po[i]) if i<len(po) else 0;c=ink[i] if i<len(ink) else 0
        character_blank=a<40 and b<40;character_near=a<80 and b<80;blank=character_blank or c<.004;near=(not blank) and (character_near or c<.008)
        pages.append({'page':i+1,'pypdfChars':a,'pdftotextRawChars':b,'inkCoverage':c,'blank':blank,'nearBlank':near})
    return {'thresholds':{'blank':{'charactersBothBelow':40,'inkBelow':.004,'join':'OR'},'nearBlank':{'charactersBothBelow':80,'inkBelow':.008,'join':'OR'}},'pages':pages,'blankPages':[r['page'] for r in pages if r['blank']],'nearBlankPages':[r['page'] for r in pages if r['nearBlank']]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--family',required=True,choices=sorted(BASELINES));p.add_argument('--file',required=True);p.add_argument('--pdf',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    path=ROOT/a.file;pdf=ROOT/a.pdf if not Path(a.pdf).is_absolute() else Path(a.pdf);candidate=count_lesson(path);baseline=derive_floor(a.family);floor=baseline['p25'];thin=[r for r in candidate['slides'] if r['wordCount']<40 and not r['deliberatePause']];candidate['p25Required']=floor;candidate['wordFloorPass']=candidate['totalWords']>=floor;candidate['thinSlidePass']=not thin;printed=pdf_measure(pdf)
    planted=copy.deepcopy(candidate['slides']);planted[0]['wordCount']=20;planted[0]['deliberatePause']=None;red=any(r['slide']==1 and r['wordCount']==20 for r in planted if r['wordCount']<40 and not r['deliberatePause'])
    green=candidate['totalWords']>=floor and not thin and not printed['blankPages'] and not printed['nearBlankPages'];report={'gate':'g18-feb','family':a.family,'baseline':baseline,'candidate':candidate,'candidateSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'p25Floor':floor,'wordFloorPass':candidate['totalWords']>=floor,'thinSlides':thin,'print':printed,'redControl':{'mutation':'first slide reduced to 20 words in memory','fired':red},'status':'PASS' if green and red else 'RED'}
    out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'words':candidate['totalWords'],'p25':floor,'thinSlides':[r['slide'] for r in thin],'blankPages':printed['blankPages'],'nearBlankPages':printed['nearBlankPages'],'redControlFired':red},indent=2));return 0 if report['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
