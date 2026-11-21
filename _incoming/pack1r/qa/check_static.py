#!/usr/bin/env python3
"""R2 intake harness: explicit population, unchanged imports, local output only."""
import csv,importlib.util,json,re,sys,hashlib,posixpath
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html as LH
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
def mod(name,path):
 spec=importlib.util.spec_from_file_location(name,REPO/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
census=mod('census','tools/chassis_census.py')
titles=mod('titles','tools/sx3/check_landing_titles.py')
sys.path.insert(0,str(REPO/'tools/hum'));import verify_loop
sys.path.insert(0,str(ROOT/'source'));from build import EXEMPLARS;from content import CAVEAT,SPACE,CAPTURE
from class_a_patterns import findings_for
pop=json.loads((ROOT/'qa/population.json').read_text());before=json.loads((ROOT/'qa/pre_loop_content.json').read_text())
coverage={r['id']:r for r in csv.DictReader((ROOT/'COVERAGE.csv').open())}
results=[];distinct={}
def containment(raw,row):
 doc=LH.fromstring(raw);bad=[];ex=[]
 for n in doc.xpath('//*[@href or @src or @action or @poster]'):
  for attr in ('href','src','action','poster'):
   v=n.get(attr)
   if not v or v.startswith('#') or v.startswith('data:'):continue
   allowed=(n.tag=='script' and row['pathway']=='BUILD' and attr=='src' and v=='/hud.js' and set(n.attrib)=={'defer','src'} and raw.count('<script defer src="/hud.js">')==1)
   allowed=allowed or (n.tag=='a' and attr=='href' and n.text_content().strip()=='← Lessons' and v==('../../index.html?subject=Humanities&pathway=BUILD' if row['pathway']=='BUILD' else '../../index.html') and ('mbmhome' in n.get('class','').split() if row['pathway']!='BUILD' else not n.get('class')))
   allowed=allowed or (n.tag=='a' and attr=='href' and 'way-home' in n.get('class','').split() and v=='./START_HERE.html' and row['pathway']!='BUILD')
   if allowed:ex.append(v);continue
   u=urlsplit(v);resolved=(ROOT/row['html']).parent.joinpath(u.path).resolve();pack=ROOT/'packs'/f'HUM_Summer_1_{row["pathway"]}_Final'
   if u.scheme or u.netloc or v.startswith('/') or not resolved.is_relative_to(pack) or not resolved.is_file():bad.append(v)
 for v in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',raw):
  if not v.startswith(('data:','#')):bad.append(v)
 return {'status':'PASS' if not bad else 'FAIL','exemptions':ex,'violations':bad}
for r in pop:
 raw=(ROOT/r['html']).read_text();doc=LH.fromstring(raw);clean=titles.parse(raw.encode());heading=titles.heading(clean);distinct[r['html']]=(heading,titles.visible(clean))
 land=LH.fromstring((ROOT/'landing'/Path(r['target']).parent.name/'START_HERE.html').read_text());card=land.xpath('//*[@data-card-title]')[0].text_content().strip()
 title=doc.xpath('//title')[0].text_content();loop=verify_loop.verify(raw,before[r['id']],'Humanities',verify_loop.science_texts(REPO))
 cls,marks=census.classify(raw)
 text=' '.join(doc.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]'))
 findings=findings_for(re.sub(r'\s+',' ',text))
 # Raw text-node whitespace (D5), not CSS or JavaScript indentation.
 doubles=[t[:100] for t in doc.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]') if re.search(r'\S {2,}\S',t)]
 ids=doc.xpath('//*[@id]/@id');duplicates=sorted({x for x in ids if ids.count(x)>1})
 timers=[int(x) for x in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]/@data-timer')]
 def count(x):return len(doc.xpath(x))
 structural={'main':count('//main[@id="lessonDeck"]')==1,'nine_stages':len(timers)==9,'timer_distribution':timers==[0,4,4,5,5,4,4,10,4],'no_duplicate_ids':not duplicates,'seven_panels':count('//*[@data-loop-key]')==7,'arrival_12_cells':count('//article[@class="arrival-cell"]')==12,'dialogs_six':count('//dialog')==6,'title_consistency':title==heading==coverage[r['id']]['title']==card,'exact_objective':r['objective'] in text,'exact_caveat':CAVEAT in text,'policy_quotes':all(q in text for q in SPACE) and CAPTURE in text,'EFL_only':'Earwig' not in text,'storage':('localStorage' not in raw and 'sessionStorage' not in raw) if r['pathway']=='BUILD' else set(re.findall(r'(?:getItem|setItem)\([\"\']([^\"\']+)',raw))<={'mbm_guide_v1'},'chassis':cls==r['chassis']}
 results.append({'id':r['id'],'target':r['target'],'chassis':cls,'structural':structural,'duplicate_ids':duplicates,'containment':containment(raw,r),'class_a':{'findings':findings,'raw_double_spaces':doubles},'hum_t_battery':loop,'LISTED':'NOT YET APPLICABLE — registration is Code’s admission'})
distinct_bad=titles.distinct_errors(distinct)
# Planted failures prove exact containment and internal consistency are not vacuous.
row=pop[0];raw=(ROOT/row['html']).read_text()
red={'external_script_rejected':containment(raw.replace('</head>','<script src="https://example.com/escape.js"></script></head>'),row)['status']=='FAIL','extra_hud_attribute_rejected':containment(raw.replace('<script defer src="/hud.js">','<script defer async src="/hud.js">'),row)['status']=='FAIL','near_miss_hud_rejected':containment(raw.replace('src="/hud.js"','src="/hud.js?extra=1"'),row)['status']=='FAIL','escape_anchor_rejected':containment(raw.replace('</head>','<a href="../../../escape.html">escape</a></head>'),row)['status']=='FAIL','wrong_title_rejected':LH.fromstring(raw.replace('<title>','<title>Wrong ')).xpath('//title')[0].text_content()!=coverage[row['id']]['title']}
report={'population':len(pop),'source_hashes':{p:hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in ['tools/chassis_census.py','tools/sx3/check_landing_titles.py','tools/hum/verify_loop.py','tools/hum/render_proof.cjs','_passhumd5/scan_class_a.py']},'distinct_errors':distinct_bad,'red_proofs':red,'lessons':results}
(ROOT/'qa/static_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'lessons':len(results),'structural_failures':{r['id']:[k for k,v in r['structural'].items() if not v] for r in results},'loop_failures':{r['id']:[x for x in r['hum_t_battery'] if x['status']=='FAIL'] for r in results},'class_a':{r['id']:r['class_a'] for r in results},'containment':[r['containment'] for r in results],'red_proofs':red,'distinct_errors':distinct_bad},ensure_ascii=False,indent=2))
