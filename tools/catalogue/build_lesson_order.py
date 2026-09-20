"""Project reviewed timing and version evidence into a read-only hub view.
No resource rows, recommendations, calendar mappings or source lessons are edited.
"""
import argparse, hashlib, json, re
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'assets/catalogue/lesson-order.json'
def read(name):return json.loads((ROOT/name).read_text())
def norm(s):return re.sub(r'\s+',' ',s).strip()
STRAND=ROOT/'tools/catalogue/HUMANITIES_STRAND.json'
GATE=ROOT/'tools/verify_cross_estate_unification.py'
WEEK_KEY=re.compile(r'^(Aut[12]|Spr[12]|Sum[12])·W(\d+)$')
def strand_proof(path,rows,record_digest,pinned_digest,projected_keys):
 """ORDER HUM-T, STOP-T3 ruling Q1 (Matt Roper, 2026-09-20): the signed, digest-pinned
 strand record tools/catalogue/HUMANITIES_STRAND.json is an accepted binding source. A
 deck whose bytes moved and which no deck limb proves is proved by its strand row when
 (1) the row exists, (2) the record's bytes equal its CATALOGUE_PINS digest, and (3) the
 row's term·week equals what the deck's own evidence projects. Any of the three failing
 is a refusal, by name. Pure, so the re-stamp tool's self-test plants against it."""
 row=rows.get(path)
 if row is None:return False,'no strand row for '+path
 if not pinned_digest or record_digest!=pinned_digest:return False,'strand record digest differs from its pin'
 if row.get('term') is None or row.get('week') is None:return False,'strand row carries no term·week'
 key='%s·W%d'%(row['term'],int(row['week']))
 keys=sorted(set(projected_keys))
 if not keys:return False,'the deck projects no week to compare with the strand row'
 if keys!=[key]:return False,'strand row %s differs from the projection %s'%(key,keys)
 return True,key
def weeks_from_cells(proofs,cells):
 values=[]
 for p in proofs:
  for ref in p.get('refs',[]):
   if ref in cells:values.append(cells[ref]['termWeek'])
  quote=p.get('quote','')
  if isinstance(quote,str):
   values.extend(a.title()+b+'·W'+w for a,b,w in re.findall(r'\b(Aut|Spr|Sum)(?:umn|ing|mer)?\s*([12])\s*[·:—-]?\s*W(?:eek)?\s*(\d+)\b',quote,re.I))
  values.extend(weeks_from_cells(p.get('donorEvidence',[]),cells))
 return values
def strand_rows():
 if not STRAND.is_file():return {},None,None
 raw=STRAND.read_bytes();doc=json.loads(raw)
 rows={r['path']:r for r in doc.get('lessons',[])}
 pinned=None
 if GATE.is_file():
  import ast
  for node in ast.parse(GATE.read_text()).body:
   if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CATALOGUE_PINS' for t in node.targets):
    pinned=ast.literal_eval(node.value).get('files',{}).get(STRAND.relative_to(ROOT).as_posix())
 return rows,hashlib.sha256(raw).hexdigest(),pinned
def derive():
 rows=read('resources.json'); known={r['file']:r for r in rows}; supplements=[]
 for filename,subject in [('science-shelf.json','Science'),('humanities-shelf.json','Humanities')]:
  for r in read('assets/catalogue/'+filename)['lessons']:
   if r['path'] not in known:
    item={'file':r['path'],'title':r['title'],'subject':subject,'type':r.get('resourceType','lesson'),'family':subject+' Teesside','_shelfPathway':r['pathway']}
    supplements.append(item);known[r['path']]=item
 rows=rows+supplements
 metadata=read('assets/catalogue/terms-and-styles.json')['entries']
 evidence=read('tools/catalogue/TERM_AND_STYLE_EVIDENCE.json')['entries']
 science=read('tools/catalogue/SCIENCE_WEEK_BINDINGS.json')
 cells={r['reference']:r for r in read('_sownb/CALENDAR_SPINE.json')['workbookCells']}
 terms=read('assets/catalogue/terms-and-styles.json')['terms']
 entries={}; refreshed=[]; unresolved=[]; strand_proved=[]
 srows,srecord,spin=strand_rows()
 approved_science={r['path']:r['expectedPatchedSha256'] for r in read('tools/easter/SCIENCE_ORIGINAL_TARGETS.json')['targets']}
 def weeks_from(proofs):return weeks_from_cells(proofs,cells)
 for ordinal,row in enumerate(rows):
  path=row['file'];m=metadata.get(path,{});e=evidence.get(path,{})
  info={'ordinal':ordinal,'canonical':path,'weeks':[]}
  source=ROOT/path
  if e.get('sha256'):
   digest=hashlib.sha256(source.read_bytes()).hexdigest()
   if digest!=e['sha256']:
    # These later accepted Science revisions keep their own explicit SoW quote.
    text=norm(' '.join(html.fromstring(source.read_text()).itertext()))
    proofs=[p for p in e['evidence'] if p.get('method')=='own title slide declaration' and isinstance(p.get('quote'),str)]
    audit=science['entries'].get(path,{})
    configs=html.fromstring(source.read_text()).xpath('//script[@id="lesson-config"]/text()')
    config=json.loads(configs[0]) if configs else {}
    declared=config.get('source',{})
    declared_ref="'"+declared.get('sheet','')+"'!"+declared.get('cell','')
    explicit_cell=declared_ref in cells and norm(declared.get('outcome',''))==norm(cells[declared_ref]['verbatimOutcome']) and any(declared_ref in p.get('refs',[]) for p in e['evidence'])
    preserved_outcome=any(p.get('currentOutcome') and config.get('sow')==p['currentOutcome'] and p.get('refs') and all(ref in cells for ref in p['refs']) for p in e['evidence'])
    timing=[p['quote'] for p in audit.get('evidence',[]) if p.get('method')=='own title slide declaration' and isinstance(p.get('quote'),str)]
    enrichment=any(p.get('method')=='current explicit enrichment label and ruled school calendar' and p.get('quote') in text and config.get('week')==8 and 'enrichment' in config.get('placement','') for p in audit.get('evidence',[]))
    # Decision signed by Matt Roper, 2026-09-18 (_sx3/DECISION_quote_limb.md):
    # the term-and-style quote limb is narrowed to the term·week token derived
    # from SCIENCE_WEEK_BINDINGS. A recorded declaration is still required, and
    # every derived token must still be present in the current text; only the
    # surrounding prose is no longer compared. The sha256 limb is unchanged.
    tokens={w['key'] for w in audit.get('weeks',[])}
    token_proved=bool(proofs) and bool(tokens) and all(key in text for key in tokens)
    proved=enrichment or explicit_cell or preserved_outcome or token_proved or (approved_science.get(path)==digest and timing and all(norm(q) in text for q in timing))
    if not proved:
     # STOP-T3 ruling Q1: the strand row, compared against the deck's own projection.
     projected=[k for k in weeks_from(e.get('evidence',[])) if WEEK_KEY.match(k) and WEEK_KEY.match(k)[1] in m.get('terms',[])]
     ok,_why=strand_proof(path,srows,srecord,spin,projected)
     if ok:proved=True;strand_proved.append(path)
    if proved:refreshed.append(path)
    else:
     assert m.get('style')!='recommended','Recommended source needs current proof: '+path
     unresolved.append(path)
   info['sourceSha256']=digest
  binding=science['entries'].get(path)
  if path in unresolved:pass
  elif binding:
   assert info.get('sourceSha256') or hashlib.sha256(source.read_bytes()).hexdigest()==binding['sourceSha256'],path
   info['weeks']=[{'term':w['term'],'week':w['weekWithinTerm'],'label':w['label']} for w in binding['weeks']]
  else:
   for key in sorted(set(weeks_from(e.get('evidence',[])))):
    match=re.fullmatch(r'(Aut[12]|Spr[12]|Sum[12])·W(\d+)',key)
    if match and match[1] in m.get('terms',[]):info['weeks'].append({'term':match[1],'week':int(match[2]),'label':terms[match[1]]+' · Week '+str(int(match[2]))})
  # Only an explicit, accepted donor relationship establishes a version pair.
  for p in e.get('evidence',[]):
   if p.get('method')=='registered transformed-version donor with current term proof' and p.get('donor') in known:
    info['canonical']=p['donor']
  entries[path]=info
 for pair in science['launchVersionPairs']:
  version=pair['versionPath'];canonical=pair['canonicalSlotPath']
  if version not in entries or canonical not in entries:continue
  manifest=read(pair['evidence']);manifest=manifest if isinstance(manifest,list) else manifest.get('lessons',manifest.get('sequence',[]))
  row=next(r for r in manifest if r['id']==pair['manifestId'])
  assert row['source']==canonical and str(Path(pair['evidence']).parent/row['file'])==version
  entries[version]['canonical']=canonical
  # Array order is the authored teaching sequence; the route spelling is unused.
  order=manifest.index(row)
  entries[canonical]['sequence']=order;entries[version]['sequence']=order
 for path,info in entries.items():
  seen={path};target=info['canonical']
  while entries[target]['canonical']!=target:
   assert target not in seen,'Version cycle';seen.add(target);target=entries[target]['canonical']
  info['canonical']=target
  assert all(w['term'] in metadata.get(path,{}).get('terms',[]) for w in info['weeks']),path
 return {'schema':1,'basis':'Projection of accepted catalogue, explicit week evidence and registered version donors. Unrecorded weeks and sequences stay unspecified.','supplements':supplements,'entries':entries,'refreshedSourceProofs':refreshed,'strandProofs':strand_proved,'unresolvedTiming':unresolved}
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 data=derive();text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
 if args.check:assert OUT.read_text()==text,'Run build_lesson_order.py to refresh derived view'
 else:OUT.write_text(text)
 print(json.dumps({'entries':len(data['entries']),'weekBound':sum(bool(r['weeks']) for r in data['entries'].values()),'versionLinks':sum(k!=r['canonical'] for k,r in data['entries'].items()),'refreshedSourceProofs':len(data['refreshedSourceProofs'])}))
if __name__=='__main__':main()
