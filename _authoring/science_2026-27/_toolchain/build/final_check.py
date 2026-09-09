from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET
import fitz
from PIL import ImageColor
import re
ROOT=Path(__file__).resolve().parents[1]
rows=[];issues=[]
sources=sorted((ROOT/'content').glob('*.json'))
assert len(sources)==24,len(sources)
assert all(sum(json.loads(f.read_text())['pathway']==p for f in sources)==8 for p in ['BUILD','GROW','LAUNCH'])
for f in sorted((ROOT/'content').glob('*.json')):
 d=json.loads(f.read_text());id=d['id'];out=ROOT/'output'/id;sha=hashlib.sha256(f.read_bytes()).hexdigest()
 assert sum(s['minutes'] for s in d['slides'])==40
 assert len(d.get('interactive',{}).get('steps',[]))==3,(id,'interactive steps')
 def validate_strings(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ['fill','stroke','color'] and isinstance(v,str) and v not in ['none','transparent']: ImageColor.getrgb(v)
    if k=='url': assert re.match(r'^https?://\S+$',v),(id,v)
    validate_strings(v)
  elif isinstance(x,list):
   for v in x:validate_strings(v)
 validate_strings(d)
 dm=json.loads((ROOT/'qa'/'docs'/id/'manifest.json').read_text())
 if dm['source_sha256']!=sha:issues.append([id,'docsource stale'])
 pm=json.loads((ROOT/'qa'/'ppt'/id/'build-manifest.json').read_text())
 psha=pm.get('source_sha256') or pm.get('sourceSha256')
 if psha!=sha:issues.append([id,'pptsource stale',list(pm)])
 counts={}
 for n in ['Pupil','Teacher','Slides']:
  p=out/(n+'.pdf');pdf=fitz.open(p);counts[n]=len(pdf)
  if n=='Pupil' and len(pdf)!=len(d['pupilPages']):issues.append([id,'unexpected pupil pages',len(pdf),len(d['pupilPages'])])
  if n=='Slides' and len(pdf)!=len(d['slides']):issues.append([id,'slide count'])
  for i,page in enumerate(pdf):
   txt=page.get_text()
   if n!='Slides' and len(txt.strip())<130:issues.append([id,n,'nearly empty page',i+1])
   for b in page.get_text('blocks'):
    if n=='Slides' or 'MADE BY MATT' in b[4]:continue
    if b[3]>page.rect.height-38 or b[0]<38 or b[2]>page.rect.width-37:issues.append([id,n,'page bounds',i+1])
 for n in ['Pupil.docx','Teacher.docx','Lesson.pptx']:
  with zipfile.ZipFile(out/n) as z:
   assert z.testzip() is None
   for name in z.namelist():
    if name.endswith('.xml'):ET.fromstring(z.read(name))
 rows.append({'id':id,'source_sha256':sha,'pages':counts,'slides':len(d['slides']),'files':len(list(out.rglob('*')))})
report={'status':'PASS' if not issues else 'REVIEW','lessons':rows,'issues':issues,'browser_execution':'Unverified: local browser URL blocked by security policy; actual JS tested with DOM emulation.'}
(ROOT/'qa'/'final_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if issues:raise SystemExit(1)
