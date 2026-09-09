from pathlib import Path
import hashlib,json,re,zipfile
from lxml import etree
import fitz
R=Path('/workspace/scratch/53a97a57d058/science_next24')
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
norm=lambda s: re.sub(r'\s+','',s).replace('–','-').replace('—','-').replace('\u00ad','').replace('ﬁ','fi').replace('ﬂ','fl')
reports=[]
visual=json.load(open(R/'qa/ppt/VISUAL_REVIEW.json'))
for source in sorted(R.glob('content/*.json')):
 d=json.load(open(source));out=R/'output'/d['id'];m=json.load(open(R/'qa/ppt'/d['id']/'build-manifest.json'));ppt=out/'Lesson.pptx';pdf=fitz.open(out/'Slides.pdf');missing=[]
 for i,s in enumerate(d['slides']):
  t=norm(pdf[i].get_text())
  expected=[s['title'],*s.get('body',[]),s.get('prompt','')]
  if s.get('visual'):expected += [e['text'] for e in s['visual'].get('elements',[]) if e['type']=='text']
  if s.get('table'):expected += [str(v) for row in [s['table']['headers'],*s['table']['rows']] for v in row] + [s['table'].get('caption','')]
  if s.get('options'):expected += [re.sub(r'^[A-Z][.)]\s+', '',o['text']) for o in s['options']]
  for line in expected:
   if norm(line) not in t:missing.append({'slide':i+1,'text':line})
 with zipfile.ZipFile(ppt) as z:
  slides=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
  notes=[n for n in z.namelist() if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml')]
  tables=shapes=images=0
  for name in slides:
   xml=etree.fromstring(z.read(name));tables+=len(xml.xpath('//a:tbl',namespaces=ns));shapes+=len(xml.xpath('//p:sp',namespaces=ns));images+=len(xml.xpath('//p:pic',namespaces=ns))
  report={'id':d['id'],'sourceCurrent':hashlib.sha256(source.read_bytes()).hexdigest()==m['sourceSha256'],'pptxHashVerified':hashlib.sha256(ppt.read_bytes()).hexdigest()==m['pptxSha256'],'slideCount':len(slides),'pdfPages':len(pdf),'notesCount':len(notes),'nativeTables':tables,'nativeShapes':shapes,'images':images,'missingPdfText':missing,'fitIssues':m['fitIssues'],'pptxBytes':ppt.stat().st_size,'pdfBytes':(out/'Slides.pdf').stat().st_size}
  v=visual['lessons'].get(d['id'],{})
  report['visualReviewCurrent']=v.get('status')=='pass' and v.get('sourceSha256AtBuild')==m['sourceSha256'] and v.get('reviewedSlides')==list(range(1,len(d['slides'])+1))
  report['nativeContentVerified']=shapes>0 and images==0 and tables==sum(bool(s.get('table')) for s in d['slides'])
  report['pass']=report['visualReviewCurrent'] and report['nativeContentVerified'] and report['sourceCurrent'] and report['pptxHashVerified'] and len(slides)==len(pdf)==len(notes)==len(d['slides']) and not missing and not m['fitIssues'];reports.append(report)
result={'allPass':len(reports)==24 and all(x['pass'] for x in reports),'lessonCount':len(reports),'slideCount':sum(x['slideCount'] for x in reports),'nativeTables':sum(x['nativeTables'] for x in reports),'nativeDiagrams':sum(sum(bool(s.get('visual')) for s in json.load(open(p))['slides']) for p in R.glob('content/*.json')),'reports':reports}
(R/'qa/ppt/FINAL_QA.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
