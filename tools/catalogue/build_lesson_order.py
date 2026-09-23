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
SCIENCE_BINDINGS=ROOT/'tools/catalogue/SCIENCE_WEEK_BINDINGS.json'
GATE=ROOT/'tools/verify_cross_estate_unification.py'
WEEK_KEY=re.compile(r'^(Aut[12]|Spr[12]|Sum[12])·W(\d+)$')
# The estate's one reader of a written term-week, token or label form alike ("Aut2·W1",
# "Autumn 2 · Week 1"): weeks_from_cells applies it to a recorded quote, and the Science label
# limb applies the same expression to the deck's own text.
WEEK_QUOTE=re.compile(r'\b(Aut|Spr|Sum)(?:umn|ing|mer)?\s*([12])\s*[·:—-]?\s*W(?:eek)?\s*(\d+)\b',re.I)
def week_keys(s):return [a.title()+b+'·W'+w for a,b,w in WEEK_QUOTE.findall(s)]
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
# A written week immediately followed by a range or decimal ("Week 1–2", "Week 1-3", "Week 1.5"):
# week_keys reads only its first number, so a label written this way names more than it says.
WEEK_RANGE=re.compile(WEEK_QUOTE.pattern+r'\s*[–\-.]\s*\d',re.I)
NO_PROJECTION='the deck projects no week to compare with the SCIENCE_WEEK_BINDINGS row'
SLIDE='contains(concat(" ",normalize-space(@class)," ")," slide ")'
def deck_statement_text(doc):
 """What the deck CLAIMS about its own week: the text of its TITLE STAGE -- the first top-level
 slide, its meta line included -- outside <script>, <style> and <template>. Ruled 2026-09-23 (Matt,
 on the limbs review): a recall or review line on a later stage ("Retrieve the actual previous
 lesson: Aut1·W3") quotes ANOTHER lesson's week and is not the deck's claim; reading it as one
 is what refused SCI_B_W4A-W7A. A week inside a script is configuration, never a claim.
 tools/hum/admit_transaction.py reads the same stage for the same reason (title_stage_text)."""
 stages=doc.xpath('//*[%s][not(ancestor::*[%s])]'%(SLIDE,SLIDE))
 if not stages:return ''
 return norm(' '.join(stages[0].xpath('.//text()[not(ancestor::script) and not(ancestor::style) and not(ancestor::template)]')))
def science_row_keys(row):
 """The row's term·week keys, or None when any week in the row is unreadable: a key WEEK_KEY
 cannot parse, or a key that disagrees with the same week's own term / weekWithinTerm fields.
 An unreadable week is a refusal, never a week quietly dropped from the comparison."""
 keys=set()
 for w in (row or {}).get('weeks',[]):
  m=WEEK_KEY.match(w.get('key','')) if isinstance(w,dict) else None
  if not m or m[1]!=w.get('term') or int(m[2])!=w.get('weekWithinTerm'):return None
  keys.add(w['key'])
 return sorted(keys)
def science_row_proof(path,rows,record_digest,pinned_digest,projected_keys,stated_keys=()):
 """Matt Roper, 2026-09-22, ruling on the batch-2 limbs (the Humanities Q1 shape, for Science):
 the signed, digest-pinned SCIENCE_WEEK_BINDINGS record proves a deck whose bytes moved and which
 no deck limb proves when (1) its row exists, (2) the record's bytes equal their CATALOGUE_PINS
 digest, and (3) the row's term·week equals what the deck's own evidence record projects. Any of
 the three failing is a refusal, by name. Pure, so the re-stamp tool's self-test plants against it.

 One more refusal, taken from the estate's standing rule rather than added to it: a deck that
 STATES weeks about itself (stated_keys: its written weeks and its own lesson-config cell) which do
 not cover its row is refused -- tools/hum/admit_transaction.py, "a deck that projects a DIFFERENT
 week from its row still refuses; that is the one case (iv) must never swallow". Without it this
 limb proved a deck whose own pages name another week (review of the first cut)."""
 row=rows.get(path)
 if row is None:return False,'no SCIENCE_WEEK_BINDINGS row for '+path
 if not pinned_digest or record_digest!=pinned_digest:return False,'SCIENCE_WEEK_BINDINGS digest differs from its pin'
 want=science_row_keys(row)
 if want is None:return False,'the SCIENCE_WEEK_BINDINGS row carries an unreadable week'
 if not want:return False,'the SCIENCE_WEEK_BINDINGS row carries no term·week'
 keys=sorted(set(projected_keys))
 if not keys:return False,NO_PROJECTION
 if keys!=want:return False,'SCIENCE_WEEK_BINDINGS row %s differs from the projection %s'%(want,keys)
 stated=set(stated_keys)
 if stated and not set(want)<=stated:return False,'the deck states %s about itself, which does not cover its row %s'%(sorted(stated),want)
 return True,','.join(want)
def science_label_proof(path,rows,record_digest,pinned_digest,text):
 """The same ruling, second limb: a deck that writes its own term-week in the form the estate's
 readers already accept ("Autumn 2 · Week 3", read by week_keys, the expression weeks_from applies)
 is proved when every week it writes equals its pinned SCIENCE_WEEK_BINDINGS row. A label with no
 row, a row whose record is off its pin, a label naming any other week, and a label written as a
 range or decimal (week_keys reads only its first number) are refusals, by name. `text` is what
 the deck says on its pages (deck_statement_text), never its scripts."""
 if WEEK_RANGE.search(text):return False,'the deck writes a week range or decimal, which week_keys reads as one week'
 labels=sorted(set(week_keys(text)))
 if not labels:return False,'the deck writes no term-week label'
 row=rows.get(path)
 if row is None:return False,'the deck writes %s but has no SCIENCE_WEEK_BINDINGS row'%labels
 if not pinned_digest or record_digest!=pinned_digest:return False,'SCIENCE_WEEK_BINDINGS digest differs from its pin'
 want=science_row_keys(row)
 if want is None:return False,'the SCIENCE_WEEK_BINDINGS row carries an unreadable week'
 if labels!=want:return False,'the deck writes %s, its SCIENCE_WEEK_BINDINGS row is %s'%(labels,want)
 return True,','.join(labels)
def title_claim_conflict(row,claims):
 """The weeks a deck's TITLE STAGE claims that its row does not bind, as a refusal; None when there
 are none. Ruled 2026-09-23 (Matt, on SCI_G_W16B): such a claim refuses the deck whatever limb would
 otherwise prove it -- W16B's own cell covered its row while its title stage told pupils and
 teachers "Spring 1 · Week 16". admit_transaction.judge_science refuses the same case."""
 want=science_row_keys(row) or []
 stray=sorted(set(claims)-set(want))
 return ("the deck's title stage states %s, which its row %s does not bind"%(stray,want)) if stray else None
def science_limbs(path,rows,record_digest,pinned_digest,projected_keys,stated_keys,said):
 """derive()'s Science part, pure: ('row'|'label', key) when a limb proves the deck, else
 (None, {limb: reason}). The row limb first; the label limb only where the evidence projects no
 week at all -- a projection that disagrees with the row is ruled a refusal, and no label rescues
 it. Split out of derive() so the self-test plants against the wiring, not only the judges."""
 ok,why=science_row_proof(path,rows,record_digest,pinned_digest,projected_keys,stated_keys)
 if ok:return 'row',why
 if why!=NO_PROJECTION:return None,{'row':why,'label':'not tried: the evidence projects a week, so the row decides'}
 ok,lwhy=science_label_proof(path,rows,record_digest,pinned_digest,said)
 if ok:return 'label',lwhy
 return None,{'row':why,'label':lwhy}
def explicit_cell_holds(declared,cells,evidence):
 """The explicit-cell deck limb: the deck's own lesson-config names a spine cell, quotes that
 cell's outcome verbatim, and the evidence record cites the same cell."""
 ref="'"+declared.get('sheet','')+"'!"+declared.get('cell','')
 return ref in cells and norm(declared.get('outcome',''))==norm(cells[ref]['verbatimOutcome']) and any(ref in p.get('refs',[]) for p in evidence)
def weeks_from_cells(proofs,cells):
 values=[]
 for p in proofs:
  for ref in p.get('refs',[]):
   if ref in cells:values.append(cells[ref]['termWeek'])
  quote=p.get('quote','')
  if isinstance(quote,str):
   values.extend(week_keys(quote))
  values.extend(weeks_from_cells(p.get('donorEvidence',[]),cells))
 return values
def catalogue_pin(record):
 """The CATALOGUE_PINS digest the gate copy records for this record, or None."""
 if not GATE.is_file():return None
 import ast
 for node in ast.parse(GATE.read_text()).body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CATALOGUE_PINS' for t in node.targets):
   return ast.literal_eval(node.value).get('files',{}).get(record.relative_to(ROOT).as_posix())
 return None
def evidence_projection(evidence,cells,terms):
 """What a deck's own evidence record projects: the term·week keys its recorded refs and quotes
 name, kept to the terms the catalogue already records for it. Q1 and the Science row limb both
 compare a row with this, so it is one expression, not two."""
 return [k for k in weeks_from_cells(evidence,cells) if WEEK_KEY.match(k) and WEEK_KEY.match(k)[1] in terms]
def strand_rows():
 if not STRAND.is_file():return {},None,None
 raw=STRAND.read_bytes();doc=json.loads(raw)
 rows={r['path']:r for r in doc.get('lessons',[])}
 return rows,hashlib.sha256(raw).hexdigest(),catalogue_pin(STRAND)
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
 entries={}; refreshed=[]; unresolved=[]; strand_proved=[]; row_proved=[]; label_proved=[]; science_refused={}
 srows,srecord,spin=strand_rows()
 # The Science record, digested from the bytes read above and judged against its own pin.
 brecord=hashlib.sha256(SCIENCE_BINDINGS.read_bytes()).hexdigest();bpin=catalogue_pin(SCIENCE_BINDINGS)
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
    explicit_cell=explicit_cell_holds(declared,cells,e['evidence'])
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
     projected=evidence_projection(e.get('evidence',[]),cells,m.get('terms',[]))
     ok,_why=strand_proof(path,srows,srecord,spin,projected)
     if ok:proved=True;strand_proved.append(path)
    if not proved and path in science['entries']:
     # Ruling on the batch-2 limbs: the Science row, then the Science label, each against the
     # pinned SCIENCE_WEEK_BINDINGS row. The row limb reads the same projection as Q1 above. The
     # label limb is tried ONLY where the evidence projects no week at all: a projection that
     # disagrees with the row is a refusal ("row week != projection -> refuse", ruled), and a
     # label must not rescue it (review of the first cut).
     projected=evidence_projection(e.get('evidence',[]),cells,m.get('terms',[]))
     said=deck_statement_text(html.fromstring(source.read_text()))
     stated=set(week_keys(said))|({cells[declared_ref]['termWeek']} if declared_ref in cells and cells[declared_ref].get('termWeek') else set())
     limb,result=science_limbs(path,science['entries'],brecord,bpin,projected,stated,said)
     if limb=='row':proved=True;row_proved.append(path)
     elif limb=='label':proved=True;label_proved.append(path)
     else:science_refused[path]=result
    if path in science['entries']:
     # Ruled on W16B: a title-stage week the row does not bind refuses, whichever limb proved it.
     conflict=title_claim_conflict(science['entries'][path],week_keys(deck_statement_text(html.fromstring(source.read_text()))))
     if conflict:
      proved=False
      for lst in (row_proved,label_proved):
       if path in lst:lst.remove(path)
      science_refused[path]={'claim':conflict}
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
 out={'schema':1,'basis':'Projection of accepted catalogue, explicit week evidence and registered version donors. Unrecorded weeks and sequences stay unspecified.','supplements':supplements,'entries':entries,'refreshedSourceProofs':refreshed,'strandProofs':strand_proved,'unresolvedTiming':unresolved}
 # Named only when a Science limb fired. A limb fires only on bytes that moved from their recorded
 # digest, which a reviewed re-stamp then closes, so on a re-stamped tree both lists are empty and
 # the served lesson-order.json keeps its bytes (pin_catalogue_contract compares it with derive()).
 if row_proved:out['scienceRowProofs']=row_proved
 if label_proved:out['scienceLabelProofs']=label_proved
 # Why each moved Science deck no limb proves was refused, per limb -- so a refusal is HELD by
 # name with the limb that refuses (ruling), not reported as "the narrowed token limb".
 if science_refused:out['scienceRefusals']=science_refused
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 data=derive();text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
 if args.check:assert OUT.read_text()==text,'Run build_lesson_order.py to refresh derived view'
 else:OUT.write_text(text)
 print(json.dumps({'entries':len(data['entries']),'weekBound':sum(bool(r['weeks']) for r in data['entries'].values()),'versionLinks':sum(k!=r['canonical'] for k,r in data['entries'].items()),'refreshedSourceProofs':len(data['refreshedSourceProofs'])}))
if __name__=='__main__':main()
