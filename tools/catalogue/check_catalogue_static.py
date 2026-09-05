from pathlib import Path
import argparse, collections, hashlib, json, subprocess
from lxml import html
from urllib.parse import urlsplit,unquote
r=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--baseline-root',type=Path,default=r);args=ap.parse_args()
rows=json.loads((r/'resources.json').read_text());proof=json.loads((r/'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json').read_text())['entries'];science=json.loads((r/'assets/catalogue/science-shelf.json').read_text())['lessons']
checks=[]
def check(name,condition):
 assert condition,name
 checks.append({'name':name,'status':'PASS'})
base=subprocess.check_output(['git','show','HEAD:resources.json'],cwd=args.baseline_root)
check('resources.json byte-identical to current baseline',base==(r/'resources.json').read_bytes())
check('Every committed resource row has additive metadata',len(rows)>0 and all(x['file'] in proof for x in rows))
check('All 123 Science lessons remain available with a proven or explicitly unknown term',len(science)==123 and len({x['path'] for x in science})==123 and all((r/x['path']).is_file() and x['term'] in ['Aut1','Aut2','Spr1','unspecified'] for x in science))
check('Current content hashes match every hashed metadata entry',all(hashlib.sha256((r/p).read_bytes()).hexdigest()==v['sha256'] for p,v in proof.items() if 'sha256' in v))
check('Recommended selection contains only the 15 selected LAUNCH Science routes',sum(x['style']=='recommended' for x in science)==15 and all(x['pathway']=='LAUNCH' for x in science if x['style']=='recommended'))
for filename in ['index.html','Science_Teesside/index.html','Humanities_Teesside/index.html']:
 p=r/filename;doc=html.fromstring(p.read_text());ids=doc.xpath('//*[@id]/@id');check(filename+' has unique element IDs',len(ids)==len(set(ids)))
 missing=[]
 for value in doc.xpath('//script[@src]/@src|//link[@rel="stylesheet"]/@href'):
  url=urlsplit(value)
  if url.scheme or value.startswith('/'):continue
  target=p.parent/unquote(url.path)
  if not target.is_file():missing.append(value)
 check(filename+' has resolvable local scripts and styles',not missing)
science_doc=html.fromstring((r/'Science_Teesside/index.html').read_text())
check('All static Science lesson URLs resolve locally',all((r/'Science_Teesside'/unquote(a)).is_file() for a in science_doc.xpath('//article[@data-lesson-path]/a[@class="go"]/@href')))
check('No browser zoom restriction added',all('user-scalable=no' not in (r/p).read_text() and 'maximum-scale=1' not in (r/p).read_text() for p in ['index.html','Science_Teesside/index.html','Humanities_Teesside/index.html']))
humanities=json.loads((r/'assets/catalogue/humanities-shelf.json').read_text())['lessons']
hselection=json.loads((r/'tools/catalogue/HUMANITIES_SELECTION.json').read_text())
selected=hselection['lessons']
declared={row['file'] for row in rows if row.get('subject','').casefold()==hselection['resourcesSubject'].casefold()}
for manifest_path in hselection['manifestSources']:
 mf=r/manifest_path;md=json.loads(mf.read_text())
 for row in md.get('lessons',md.get('sequence',[])):
  declared.add(str((mf.parent/row['file']).relative_to(r)))
check('Humanities selection includes all current declared manifests and retained catalogue rows',declared=={x['path'] for x in selected})
expected=[x['path'] for x in selected]
check('Humanities preserves every selected current and retained resource exactly once',len(expected)>0 and len(humanities)==len(set(expected))==len(expected) and {x['path'] for x in humanities}==set(expected))
check('Known subject terms have classification evidence, not just presentation style',all(x['term'] in ['any','unspecified','flexible'] or (x['term'] in proof[x['path']]['terms'] and any(e.get('method')!='current presentation structure' for e in proof[x['path']]['evidence'])) for x in science+humanities))
reviewed_unknown={x['file'] for x in json.loads((r/'tools/catalogue/TERM_REVIEW.json').read_text())}
check('Every unknown subject term remains visible in the review record',all(x['path'] in reviewed_unknown for x in science+humanities if x['term']=='unspecified'))
check('Humanities shelf is discoverable from the main and existing Humanities hubs',all('Humanities_Teesside/index.html' in html.fromstring((r/name).read_text()).xpath('//a/@href') for name in ['index.html','humanities_teesside.html']))
hdoc=html.fromstring((r/'Humanities_Teesside/index.html').read_text())
check('All static Humanities resources are linked without JavaScript',set(hdoc.xpath('//article[@data-lesson-path]/@data-lesson-path'))==set(expected))
check('All Humanities lesson and reference URLs resolve locally',all((r/'Humanities_Teesside'/unquote(a)).is_file() for a in hdoc.xpath('//article[@data-lesson-path]/a[@class="go"]/@href')))
for filename in ['Science_Teesside/index.html','Humanities_Teesside/index.html']:
 doc=html.fromstring((r/filename).read_text())
 check(filename+' keeps recreational games out of its learning header',all(urlsplit(a).path.rstrip('/').lower()!='/games' and 'madebymatt-play.uk' not in a for a in doc.xpath('//header//a/@href')))
result={'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=args.baseline_root,text=True).strip(),'resourceSha256':hashlib.sha256(base).hexdigest(),'rootResourceTerms':dict(collections.Counter(proof[x['file']]['term'] for x in rows)),'scienceTerms':dict(collections.Counter(x['term'] for x in science)),'scienceStyles':dict(collections.Counter(x['style'] for x in science)),'humanitiesRows':len(humanities),'humanitiesTerms':dict(collections.Counter(x['term'] for x in humanities)),'humanitiesStyles':dict(collections.Counter(x['style'] for x in humanities)),'checks':checks,'limitations':['No real browser rendering or device interaction was performed.','Print expansion logic and print CSS are checked; page pagination remains unverified.','No publication, commit, push, pull request or deployment was performed.']}
(r/'tools/catalogue/STATIC_CHECK_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
