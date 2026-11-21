#!/usr/bin/env python3
"""Whole-pack local-reference scan, chassis selector matrix and byte rebuild proof."""
import json,re,sys,hashlib,subprocess,csv
from pathlib import Path
from lxml import html as LH
from urllib.parse import urlsplit
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
sys.path.insert(0,str(ROOT/'source'));from build import EXEMPLARS
from class_a_patterns import findings_for
pop=json.loads((ROOT/'qa/population.json').read_text());report={'chassis':[],'pack_links':[],'class_a_companions':[]}
tests={1:('//main[@id="lessonDeck"]',1),2:('//main[contains(@class,"slide-container")]',1),9:('//*[@id="auto-timer"]',1),10:('//*[@id="auto-timer-toggle" or @id="auto-timer-display"]',2),11:('//dialog[@id="word-dialog"]',1),12:('//dialog[@id="pause-dialog"]',1),13:('//dialog[@id="tools-dialog"]',1),14:('//dialog[@id="organiser-dialog"]',1),16:('//dialog[@id="ta-dialog"]',1),17:('//dialog[@id="cold-call-dialog"]',1),18:('//*[@id="arrival-panel-supported"]/article',4),19:('//*[@id="arrival-panel-standard"]/article',4),20:('//*[@id="arrival-panel-stretch"]/article',4),21:('//*[starts-with(@id,"print-arrival-") and not(starts-with(@id,"print-arrival-answers-"))]',3),22:('//*[starts-with(@id,"print-arrival-answers-")]',3),23:('//*[starts-with(@id,"print-exit-")]',3),25:('//*[@id="print-area"]',1),27:('//*[@id="print-organiser"]',1),28:('//*[@id="print-shared"]',1),32:('//*[@id="progressBar" or @id="progressLabel"]',2),33:('//*[@id="classic-progress" or @id="classic-status"]',2),34:('//*[@id="previous-slide" or @id="next-slide" or @id="slide-picker"]',3),35:('//section[starts-with(@id,"slide-")]',9),36:('//script[@id="lesson-config"]',1)}
def props(doc):
 d={}
 for node in doc.xpath('//style'):
  for k,v in re.findall(r'(--[\w-]+)\s*:\s*([^;}]+)',node.text or ''):d[k]=v.strip()
 return d
for r in pop:
 doc=LH.fromstring((ROOT/r['html']).read_text());p=r['pathway'];isbuild=p=='BUILD'
 matrix={str(k):{'actual':len(doc.xpath(x)),'expected':v,'pass':len(doc.xpath(x))==v} for k,(x,v) in tests.items()}
 for k,x,v in [(3,'//nav[@class="review-top"]',0 if isbuild else 1),(4,'//nav[@class="classic-toolbar"]',1 if isbuild else 0),(5,'//a[@class="skip"]',0 if isbuild else 1),(6,'//*[@id="xpWrap"]',1 if isbuild else 0),(7,'//*[@id="xpFill" or @id="xpCount" or @id="xpTotal"]',3 if isbuild else 0),(8,'//*[@id="lc-overlay"]',1 if isbuild else 0),(24,'//*[starts-with(@id,"print-task-")]',3 if isbuild else 6),(26,'//*[@id="print-answers" or @id="all-answers"]',1 if isbuild else 2),(29,'//*[@id="print-staff" or contains(concat(" ",@class," ")," staff-card ")]',1 if isbuild else 2),(30,'//*[contains(concat(" ",@class," ")," teacher-only ")]',2 if isbuild else 3),(31,'//*[contains(concat(" ",@class," ")," science-reveal ")]',2 if p=='GROW' else 0),(37,'/html[@class="pathway-'+p.lower()+'"]',1)]:matrix[str(k)]={'actual':len(doc.xpath(x)),'expected':v,'pass':len(doc.xpath(x))==v}
 matrix['15']={'pass':len(doc.xpath('//*[@class="ko-content"]'))==1,'method':'R-KO HTML organiser, one A4 page in browser output; no fabricated SVG IDs'}
 expected=props(LH.fromstring((REPO/EXEMPLARS[p]).read_text()));actual=props(doc)
 palette={k:{'expected':v,'actual':actual.get(k),'pass':actual.get(k)==v} for k,v in expected.items()}
 report['chassis'].append({'id':r['id'],'rows':matrix,'palette':palette,'palette_source':EXEMPLARS[p],'palette_note':'Compare effective style-block properties. Contract lexical counts also include arrival inline order and n6 comment markers, which are not colour tokens. No --mbm layer introduced.'})
 pack=ROOT/'packs'/f'HUM_Summer_1_{p}_Final'
 for file in pack.rglob('*.html'):
  d=LH.fromstring(file.read_text());bad=[]
  if file!=ROOT/r['html']:
   for node in d.xpath('//*[@href or @src]'):
    for a in ['href','src']:
     v=node.get(a)
     if not v or v.startswith(('#','data:')):continue
     u=urlsplit(v);q=(file.parent/u.path).resolve()
     if u.scheme or u.netloc or not q.is_relative_to(pack) or not q.is_file():bad.append(v)
  report['pack_links'].append({'file':str(file.relative_to(ROOT)),'violations':bad})
  text=' '.join(d.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]'))
  report['class_a_companions'].append({'file':str(file.relative_to(ROOT)),'findings':findings_for(re.sub(r'\s+',' ',text))})
paths=[f for f in ROOT.rglob('*.html') if 'vendor' not in f.parts]
before={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}
subprocess.run([sys.executable,str(ROOT/'source/build.py')],check=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
after={k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in before}
report['deterministic_html_build']={'files':len(before),'pass':before==after,'sha256':after}
report['all_pass']=all(x['pass'] for r in report['chassis'] for x in [*r['rows'].values(),*r['palette'].values()]) and not any(r['violations'] for r in report['pack_links']) and not any(r['findings'] for r in report['class_a_companions']) and before==after
(ROOT/'qa/pack_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'all_pass':report['all_pass'],'chassis_failures':{r['id']:[k for k,v in r['rows'].items() if not v['pass']] for r in report['chassis']},'link_failures':[r for r in report['pack_links'] if r['violations']],'class_a':[r for r in report['class_a_companions'] if r['findings']],'deterministic':before==after}))
