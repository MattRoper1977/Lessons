"""Build additive catalogue metadata from current lesson content and SoW evidence.

No filename week inference, resource-row edits, route moves or timing assertions.
"""
from pathlib import Path
from lxml import html
import collections, hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/catalogue'; OUT.mkdir(parents=True,exist_ok=True)
PROOF=ROOT/'tools/catalogue'; PROOF.mkdir(parents=True,exist_ok=True)
SPINE=json.loads((ROOT/'_sownb/CALENDAR_SPINE.json').read_text())
CELLS={x['reference']:x for x in SPINE['workbookCells']}
EXISTING={x['path']:x for x in SPINE['existingHtml']}
SELECTION=json.loads((ROOT/'tools/catalogue/SHELF_SELECTION.json').read_text())
RECOMMENDED=set(SELECTION['recommended'])
ROWS=json.loads((ROOT/'resources.json').read_text())
SCI=SELECTION['science']
HUM=json.loads((PROOF/'HUMANITIES_SELECTION.json').read_text())['lessons']
PRIOR={x['path']:x for x in SCI}
TERM={'Aut1':'Autumn 1','Aut2':'Autumn 2','Spr1':'Spring 1','Spr2':'Spring 2','Sum1':'Summer 1','Sum2':'Summer 2','multi':'Across terms','flexible':'Flexible sequence','any':'Any term · reference','unspecified':'Term not specified'}
STYLE={'recommended':'Recommended · current chassis','current':'Current classroom series','full-lundy':'Full Lundy Loop','award':'Flexible award sequence','earlier':'Earlier retained versions','reference':'Tools and reference'}
MANIFESTS={}
for mf in sorted(ROOT.rglob('manifest*.json')):
 if any(part.startswith('.') for part in mf.relative_to(ROOT).parts):continue
 try:data=json.loads(mf.read_text())
 except (ValueError,UnicodeError):continue
 rows=data if isinstance(data,list) else data.get('lessons',data.get('sequence',[])) if isinstance(data,dict) else []
 for item in rows:
  if not isinstance(item,dict) or not isinstance(item.get('file'),str):continue
  candidate=mf.parent/item['file']
  if candidate.is_file():MANIFESTS.setdefault(str(candidate.relative_to(ROOT)),[]).append((str(mf.relative_to(ROOT)),item))
CACHE={}

def norm(s):return re.sub(r'\s+',' ',s).strip()
def term_codes(s):
 return sorted(set(a.title()+b for a,b in re.findall(r'\b(Aut|Spr|Sum)(?:umn|ing|mer)?\s*([12])\b',s,re.I)))
def path_tier(path,title=''):
 for t in ('Build','Grow','Launch'):
  if any(part.casefold()==t.casefold() or part.upper().startswith(t.upper()+'_') for part in Path(path).parts) or title.upper().startswith(t.upper()):return t.upper()
 return 'OTHER'
def current_donor(item):
 source=item.get('source')
 if not isinstance(source,str) or '_Estate_v3/' in source:return None
 if (ROOT/source).is_file():return source
 # Two old manifest donor names differ from current canonical spelling. Resolve
 # only a unique exact current H1/title in that registered source directory.
 parent=(ROOT/source).parent
 if not parent.is_dir() or not item.get('title'):return None
 wanted=norm(item['title']).casefold();matches=[]
 for candidate in parent.glob('*.html'):
  document=html.fromstring(candidate.read_text(errors='replace'))
  if any(norm(' '.join(node.itertext())).casefold()==wanted for node in document.xpath('//h1')):matches.append(str(candidate.relative_to(ROOT)))
 return matches[0] if len(matches)==1 else None
def classify(path,row=None):
 row=row or {};f=ROOT/path
 if path in CACHE:return {**CACHE[path],'title':row.get('title') or CACHE[path].get('title')}
 result={'term':'any','terms':[],'style':'reference','pathway':path_tier(path,row.get('title','')),'evidence':[]}
 if not f.is_file() or f.suffix.lower()!='.html':return result
 raw=f.read_text(errors='replace');doc=html.fromstring(raw)
 slides=doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
 title_slide=norm(' '.join(slides[0].itertext())) if slides else ''
 title=doc.xpath('//title/text()');own_title=title[0] if title else row.get('title',path)
 is_lesson=str(row.get('type','')).lower() in ('lesson','revision') or len(slides)>5
 if not is_lesson:return result
 result['term']='unspecified'
 configs=doc.xpath('//script[@id="lesson-config" or @id="lesson-data" or @id="lessonData"]/text()')
 config={}
 for value in configs:
  try:config=json.loads(value);break
  except ValueError:pass
 refs=config.get('cells',[])
 if refs and isinstance(refs[0],dict):refs=[x.get('reference','') for x in refs]
 if refs and all(isinstance(x,str) and x in CELLS for x in refs):
  terms=sorted(set(CELLS[x]['termWeek'].split('·')[0] for x in refs))
  result['evidence'].append({'method':'current lesson config cells','source':path,'refs':refs})
 else:
  sow_nodes=slides[0].xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," sow-strip ")]') if slides else []
  own_sow=norm(' '.join(' '.join(x.itertext()) for x in sow_nodes))
  terms=term_codes(own_sow) or term_codes(config.get('sow',''))
  if terms:result['evidence'].append({'method':'own title slide declaration','source':path,'quote':own_sow if term_codes(own_sow) else config.get('sow') if term_codes(config.get('sow','')) else title_slide[:1200] or own_title})
  # Current explicit manifest rows identify an exact resource, not a filename week.
  if not terms:
   for manifest,item in MANIFESTS.get(path,[]):
    mrefs=[x.get('reference','') if isinstance(x,dict) else x for x in item.get('cells',([item['cell']] if item.get('cell') else []))]
    if mrefs and all(x in CELLS for x in mrefs):
     terms=sorted(set(CELLS[x]['termWeek'].split('·')[0] for x in mrefs))
     result['evidence'].append({'method':'current manifest lesson row with resolved workbook cells','source':manifest,'file':item['file'],'refs':mrefs});break
    if term_codes(item.get('sow','')):
     terms=term_codes(item['sow']);result['evidence'].append({'method':'current manifest lesson row sow declaration','source':manifest,'file':item['file'],'quote':item['sow']});break
  # Prefer a registered donor's exact current binding to incidental references
  # to future terms elsewhere in a transformed deck's overview.
  if not terms:
   for manifest,item in MANIFESTS.get(path,[]):
    source=current_donor(item)
    if source and source!=path:
     donor=classify(source,{'type':'lesson'})
     if donor.get('terms') or donor['term']=='flexible':
      terms=donor.get('terms',[]);result['term']=donor['term']
      result['evidence'].append({'method':'registered transformed-version donor with current term proof','source':manifest,'donor':source,'registeredDonor':item['source'],'identityProof':'exact registered path' if source==item['source'] else 'unique exact current H1 in registered donor directory','donorEvidence':donor['evidence']});break
  if not terms and result['term']!='flexible':
   terms=term_codes(title_slide or own_title)
   if terms:result['evidence'].append({'method':'own title slide declaration','source':path,'quote':title_slide[:1200] or own_title})
  # Re-prove a census binding against the current content or unchanged bytes.
  if not terms and path in EXISTING:
   refs=EXISTING[path].get('contentCellReferences',[])
   if refs and all(x in CELLS for x in refs):
    unchanged=hashlib.sha256(f.read_bytes()).hexdigest()==EXISTING[path].get('blobSha256')
    body=norm(doc.text_content())
    outcomes=all(len(norm(CELLS[x]['verbatimOutcome']))>28 and norm(CELLS[x]['verbatimOutcome']) in body for x in refs)
    reviewed_solar_equivalence=(config.get('sow')=='Research and present findings about the Solar System using ICT.' and refs==["'GROW Weekly - Autumn'!C41"] and CELLS[refs[0]]['verbatimOutcome']=='Research and present findings about the Solar System (ICT).')
    cell_labels=all(re.search(r'\b'+re.escape(CELLS[x]['cell'])+r'\s+only\b',title_slide,re.I) for x in refs)
    audited=EXISTING[path].get('secondInstrumentEvidence',{})
    # Re-prove the exact reviewed manifest-to-workbook binding when a lesson
    # was edited without changing its curriculum outcome/objective. No week
    # filename or fuzzy wording match is used; all three records must agree.
    audited_current_binding=(audited.get('invalidReason') is None
     and audited.get('matchedWorkbookCells')==refs
     and bool(audited.get('manifestOutcome')) and bool(audited.get('manifestObjective'))
     and norm(config.get('sow',''))==norm(audited['manifestOutcome'])
     and norm(config.get('objective',''))==norm(audited['manifestObjective'])
     and any(mf==audited.get('manifest') and item.get('id')==audited.get('manifestId')
      and norm(item.get('outcome',''))==norm(audited['manifestOutcome'])
      and norm(item.get('objective',''))==norm(audited['manifestObjective'])
      for mf,item in MANIFESTS.get(path,[])))
    if unchanged or outcomes or cell_labels or reviewed_solar_equivalence or audited_current_binding:
     terms=sorted(set(CELLS[x]['termWeek'].split('·')[0] for x in refs))
     result['evidence'].append({'method':'current content re-proves audited workbook binding' if not unchanged else 'unchanged source census with resolved workbook cells','source':'_sownb/CALENDAR_SPINE.json','refs':refs,'proof':'unchanged bytes' if unchanged else 'verbatim current outcome' if outcomes else 'current title explicit cell-only label' if cell_labels else 'current manifest and lesson-config exactly reproduce audited outcome/objective/cell binding' if audited_current_binding else 'reviewed equivalent wording: (ICT) / using ICT','quote':title_slide[:1200] if cell_labels else [CELLS[x]['verbatimOutcome'] for x in refs],'currentOutcome':config.get('sow')})
  # A previously reviewed declaration is accepted only if its quote still exists.
  if not terms and path in PRIOR:
   text=norm(doc.text_content())
   for evidence in PRIOR[path].get('classificationEvidence',[]):
    quote=norm(evidence.get('quote',''))
    if quote and quote in text and term_codes(quote):
     terms=term_codes(quote);result['evidence'].append(evidence);break
  # The current deck explicitly calls Week 8 enrichment; ruled term dates put
  # absolute week 8 in Autumn 1. No route-name or obsolete week-block inference.
  if not terms and re.search(r'\bWeek 8 Enrichment\b',title_slide,re.I):
   terms=['Aut1'];result['evidence'].append({'method':'current explicit enrichment label and ruled school calendar','source':path,'quote':'Week 8 Enrichment','calendar':'_sownb/TERM_DATES.md'})
 if terms:
  result['terms']=terms;result['term']=terms[0] if len(terms)==1 else 'multi'
 if config.get('artsAward') and not terms:
  result['term']='flexible';result['evidence'].append({'method':'award sequence; no calendar binding','source':path,'planId':config.get('planId')})
 loops=doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," lundy-grid ") or contains(concat(" ",normalize-space(@class)," ")," lundy-loop ")]')
 if path in RECOMMENDED:
  result['style']='recommended';result['batch']='LAUNCH W3–W7 · integrated teaching pack'
 elif len(loops)>=4:
  result['style']='full-lundy';result['batch']='Full Lundy Loop · repeated prompts'
 elif config.get('artsAward'):
  result['style']='award';result['batch']='Arts Award · '+str(config.get('artsAward',{}).get('level','sequence') if isinstance(config.get('artsAward'),dict) else config['artsAward'])
 elif 'sci-lesson-payload' in raw or config.get('chassis')=='classic-v2' or 'data-main-session-plan' in raw:
  result['style']='current';result['batch']='Current chassis · interactive teaching'
 else:
  result['style']='earlier';result['batch']='Earlier retained versions'
 result['evidence'].append({'method':'current presentation structure','source':path,'repeatedLundyPanels':len(loops),'chassis':config.get('chassis')})
 result['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
 result['title']=row.get('title') or own_title
 CACHE[path]=result
 return result

entries={r['file']:classify(r['file'],r) for r in ROWS}
science=[]
for old in SCI:
 path=old['path'];m=classify(path,{'type':'lesson'})
 science.append({'path':path,**m})
 # Include uncatalogued Science versions in metadata; the Science shelf links them.
 entries.setdefault(path,m)
humanities=[]
for selected in HUM:
 path=selected['path'];m=classify(path,{'type':selected['type'],'title':selected.get('title')})
 m.setdefault('title',selected['title']);m.setdefault('batch','Tools and reference')
 humanities.append({'path':path,'resourceType':selected['type'],**m})
 entries.setdefault(path,m)
proof={'schema':'catalogue-evidence-v1','basis':'Explicit current lesson/SoW evidence. Flexible sequences are not assigned calendar weeks. Recommended is an editorial selection, not a claim of universal curriculum coverage.','entries':entries}
(PROOF/'TERM_AND_STYLE_EVIDENCE.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
public={'schema':1,'terms':TERM,'styles':STYLE,'entries':{p:{k:v for k,v in m.items() if k not in ('evidence','sha256','title','pathway')} for p,m in entries.items()}}
(OUT/'terms-and-styles.json').write_text(json.dumps(public,ensure_ascii=False,separators=(',',':'))+'\n')
(OUT/'science-shelf.json').write_text(json.dumps({'schema':1,'terms':TERM,'styles':STYLE,'lessons':[{k:v for k,v in x.items() if k not in ('evidence','sha256')} for x in science]},ensure_ascii=False,separators=(',',':'))+'\n')
(OUT/'humanities-shelf.json').write_text(json.dumps({'schema':1,'terms':TERM,'styles':STYLE,'lessons':[{k:v for k,v in x.items() if k not in ('evidence','sha256')} for x in humanities]},ensure_ascii=False,separators=(',',':'))+'\n')
print('Humanities shelf:',len(humanities),'resources')
print('Catalogue terms:',dict(collections.Counter(entries[r['file']]['term'] for r in ROWS)))
print('Catalogue styles:',dict(collections.Counter(entries[r['file']]['style'] for r in ROWS)))
print('Science shelf:',len(science),'routes')
(PROOF/'TERM_REVIEW.json').write_text(json.dumps([{'file':path,'title':m.get('title',path),'inResourceCatalogue':any(r['file']==path for r in ROWS)} for path,m in entries.items() if m['term']=='unspecified'],ensure_ascii=False,indent=2)+'\n')
