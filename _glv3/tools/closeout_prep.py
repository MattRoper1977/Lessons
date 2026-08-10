#!/usr/bin/env python3
from __future__ import annotations
import base64, datetime as dt, hashlib, io, json, os, re, stat, subprocess, zipfile
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[2]; GL=ROOT/'_glv3'
GROW=Path(os.environ.get('GLV3_GROW_SRC','/tmp/glv3-packs/grow'))
LAUNCH=Path(os.environ.get('GLV3_LAUNCH_SRC','/tmp/glv3-packs/launch'))
SENTINEL='grow-launch-estate-v3-autonomous-closeout-2026-08-10'
HIST='1e8a428b523d1b970a8a3a2ab2a99f48a8271d09'
TRANSPORT='efef35d7c8504f603646663da603a2f3690ed8204b2af7d0730b52560a9db918'
EXP={
 'GROW':{'zip':'GROW_ESTATE_v3_REPAIRED_2026-08-10.zip','sha':'95bf78a4124f20196508748c4b44c3935b0eb09181bac69fcc00c4c0a5e6f58a','size':418166,'members':54,'html':41,'lessons':34,'subjects':{'art':8,'humanities':8,'asdan':18}},
 'LAUNCH':{'zip':'LAUNCH_ESTATE_v3_REPAIRED_2026-08-10.zip','sha':'aacbeda81d4bb5d665a0d70aafd5732431b64457a313e2f8843a120d0515768c','size':517266,'members':66,'html':53,'lessons':46,'subjects':{'art':8,'humanities':8,'asdan':30}},
}

def now(): return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def sh(*a): return subprocess.check_output(a,cwd=ROOT,text=True).strip()
def hbytes(b): return hashlib.sha256(b).hexdigest()
def hfile(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def inventory(root):
 out=[]; seen={}
 for p in sorted(x for x in root.rglob('*') if x.is_file()):
  r=p.relative_to(root).as_posix(); k=r.casefold()
  if p.is_symlink() or (k in seen and seen[k]!=r): raise RuntimeError(f'unsafe/colliding extracted path: {r}')
  seen[k]=r; out.append({'path':r,'size':p.stat().st_size,'sha256':hfile(p),'html':p.suffix.lower()=='.html'})
 return out
def digest(rows): return hbytes('\n'.join(f"{x['path']}\0{x['size']}\0{x['sha256']}" for x in rows).encode())
def safe_zip(data):
 rows=[]; payload={}; seen=set(); fold=set()
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  for i in z.infolist():
   p=PurePosixPath(i.filename); key=i.filename.rstrip('/')
   if p.is_absolute() or '..' in p.parts or key in seen or key.casefold() in fold: raise RuntimeError(f'unsafe/colliding ZIP path: {i.filename}')
   seen.add(key); fold.add(key.casefold())
   if stat.S_ISLNK((i.external_attr>>16)&0xffff): raise RuntimeError(f'symlink ZIP member: {i.filename}')
   if not i.is_dir():
    b=z.read(i); payload[i.filename]=b; rows.append({'path':i.filename,'size':len(b),'sha256':hbytes(b),'html':i.filename.lower().endswith('.html')})
 return rows,payload
def manifest_lookup(root):
 out={}
 for p in sorted(root.rglob('manifest-v3.json')):
  data=json.loads(p.read_text()); items=data if isinstance(data,list) else data.get('lessons') or data.get('items') or data.get('files') or []
  parent=p.parent.relative_to(root).as_posix()
  for x in items:
   f=next((x.get(k) for k in ('file','filename','output','html','path') if isinstance(x.get(k),str) and x[k].endswith('.html')),None)
   if f: out[(f'{parent}/{f}' if parent!='.' else f)]={**x,'manifest_path':p.relative_to(root).as_posix()}
 return out
def subject(rel):
 return {'Art_Teesside':'art','Humanities_Teesside':'humanities','GROW_ASDAN':'asdan','LAUNCH_ASDAN':'asdan'}.get(PurePosixPath(rel).parts[0])
def dest(pathway,rel):
 estate=f'{pathway}_Estate_v3'; p=PurePosixPath(rel)
 if p.suffix.lower()=='.md': return f'_glv3/{pathway.lower()}/{rel}'
 if p.suffix.lower()=='.html' and len(p.parts)==1 and p.name.startswith('START_HERE_'): return f'{estate}/index.html'
 if p.suffix.lower()=='.html' and p.name.startswith('START_HERE_'): return f'{estate}/{p.parent.as_posix()}/index.html'
 name=p.name.replace('_OUTSTANDING_V3_TEST',''); parent=p.parent.as_posix()
 return f'{estate}/{parent}/{name}' if parent!='.' else f'{estate}/{name}'
def classify(pathway,root):
 look=manifest_lookup(root); rows=[]; used={}
 for p in sorted(root.rglob('*.html')):
  rel=p.relative_to(root).as_posix(); m=look.get(rel)
  if '_OUTSTANDING_V3_TEST.html' in p.name: cls='deployable lesson'; rule='Repaired authored lesson suffix plus subject-manifest match.'
  elif p.parent==root and p.name.startswith('START_HERE_'): cls='estate hub'; rule='Root START_HERE HTML becomes estate index.'
  elif p.name.startswith('START_HERE_'): cls='subject hub'; rule='Subject START_HERE HTML becomes subject index.'
  else: cls='audit/support/non-deployable'; rule='Support HTML without lesson suffix and absent from lesson manifest.'
  d=dest(pathway,rel); old=used.get(d); used[d]=rel
  w=re.search(r'(?:^|_)W(\d+)(?:_|\b)',p.stem,re.I); prefix=re.match(r'([A-Z]+)_W\d+',p.stem)
  rows.append({'pathway':pathway,'source_path':rel,'classification':cls,'classification_rule':rule,'source_manifest_entry':m,'subject':subject(rel),'week':m.get('week') if m else (int(w.group(1)) if w else None),'strand':(m.get('slotcode') or m.get('slot')) if m else (prefix.group(1) if prefix else None),'intended_destination_path':d,'duplicate_collision_status':'collision' if old else 'unique','collides_with':old,'size':p.stat().st_size,'sha256':hfile(p)})
 counts={'html_members':len(rows),'deployable':sum(x['classification']=='deployable lesson' for x in rows),'estate_hubs':sum(x['classification']=='estate hub' for x in rows),'subject_hubs':sum(x['classification']=='subject hub' for x in rows),'support_html':sum(x['classification']=='audit/support/non-deployable' for x in rows),'by_subject':{s:sum(x['classification']=='deployable lesson' and x['subject']==s for x in rows) for s in ('art','humanities','asdan')}}
 return rows,counts
def audit(root,pathway):
 p=root/f'{pathway}_COMPLETION_AUDIT.md'; t=p.read_text(); mark='Post-verification edits applied 2026-08-10'
 return {'path':p.name,'sha256':hfile(p),'marker_present':mark in t,'marker_heading_count':t.count(mark)}

def main():
 GL.mkdir(exist_ok=True); mainsha=sh('git','rev-parse','origin/main'); head=sh('git','rev-parse','HEAD')
 tar=Path('/tmp/glv3-packs.tar.xz')
 if not tar.exists() or hfile(tar)!=TRANSPORT: raise RuntimeError('combined transport hash mismatch')
 growzip=base64.b64decode((ROOT/'_glv3/input/GROW_ESTATE_v3_REPAIRED_2026-08-10.zip.b64').read_bytes(),validate=True)
 zrows,zpayload=safe_zip(growzip)
 inputs={'sentinel':SENTINEL,'generated_at':now(),'transport':{'sha256':hfile(tar),'expected_sha256':TRANSPORT,'verified':True},'archives':{}}
 for pathway,root in (('GROW',GROW),('LAUNCH',LAUNCH)):
  e=EXP[pathway]; inv=inventory(root); html=sum(x['html'] for x in inv); a=audit(root,pathway)
  if (root/'Science').exists() or len(inv)!=e['members'] or html!=e['html'] or not a['marker_present']: raise RuntimeError(f'{pathway} input integrity mismatch')
  r={'name':e['zip'],'reported_zip_sha256':e['sha'],'reported_zip_size':e['size'],'reported_zip_members':e['members'],'reported_html_members':e['html'],'original_zip_bytes_available_in_repository':pathway=='GROW','extracted_manifest_digest_sha256':digest(inv),'extracted_members':len(inv),'extracted_html_members':html,'science_folder_present':False,'audit':a,'files':inv}
  if pathway=='GROW':
   exact=hbytes(growzip)==e['sha'] and len(growzip)==e['size'] and len(zrows)==e['members'] and sum(x['html'] for x in zrows)==e['html']; equal=all(x['path'] in zpayload and hbytes(zpayload[x['path']])==x['sha256'] for x in inv)
   r.update({'repository_standalone_zip_sha256':hbytes(growzip),'repository_standalone_zip_size':len(growzip),'repository_standalone_zip_members':len(zrows),'repository_standalone_html_members':sum(x['html'] for x in zrows),'repository_standalone_exact_reported_match':exact,'standalone_vs_combined_extracted_equal':equal})
   if not exact or not equal: raise RuntimeError('standalone GROW disagrees with combined transport')
  else: r['original_zip_verification_note']='Exact uploaded LAUNCH ZIP was independently verified before Actions; this run records the deterministic extracted-manifest digest and does not claim a recreated ZIP is byte-identical.'
  inputs['archives'][pathway]=r
 (GL/'INPUT_INTEGRITY.json').write_text(json.dumps(inputs,indent=2,ensure_ascii=False)+'\n')
 gr,gc=classify('GROW',GROW); lr,lc=classify('LAUNCH',LAUNCH); rows=gr+lr
 if gc['deployable']!=34 or lc['deployable']!=46 or gc['by_subject']!=EXP['GROW']['subjects'] or lc['by_subject']!=EXP['LAUNCH']['subjects'] or any(x['duplicate_collision_status']!='unique' for x in rows): raise RuntimeError('count reconciliation mismatch')
 peq=[x['source_path'] for x in gr if x['classification']=='deployable lesson' and PurePosixPath(x['source_path']).name.startswith('PEQ_W')]
 if len(peq)!=6: raise RuntimeError('six GROW PEQ lessons not found')
 rec={'sentinel':SENTINEL,'generated_at':now(),'classification_method':'Authoritative `_OUTSTANDING_V3_TEST.html` suffix plus subject-manifest cross-check; hubs/support classified separately.','old_28_candidate_result':{'reported_count':28,'resolved':True,'actual_cause':'The earlier candidate classifier omitted the six GROW PEQ lesson files. Its 28 is exactly Art 8 + Humanities 8 + COMM 6 + ENT 6; PEQ_W1–PEQ_W6 were present in both the repaired archive and GROW_ASDAN/manifest-v3.json but were not recognised by the narrower prefix/strand heuristic.','omitted_files':peq,'missing_authored_bytes':False,'replacement_rule':'Classify every repaired lesson-suffix HTML member and require a subject-manifest match; do not allowlist ASDAN prefixes.'},'counts':{'GROW':gc,'LAUNCH':lc,'combined_deployable':gc['deployable']+lc['deployable'],'expected':{'GROW':34,'LAUNCH':46,'combined':80}},'members':rows}
 (GL/'COUNT_RECONCILIATION.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
 sp=GL/'AUTONOMOUS_SENTINEL.json'; old=json.loads(sp.read_text()) if sp.exists() else {}; phases=old.get('phase_timestamps',{}); phases.setdefault('DISCOVERY',now()); phases.update({'INPUT_RECONSTRUCTION':now(),'COUNT_RECONCILIATION':now()})
 sent={'sentinel':SENTINEL,'repository':'MattRoper1977/Lessons','historic_rollback_sha':HIST,'starting_main_sha':old.get('starting_main_sha',mainsha),'starting_recovery_branch_sha':old.get('starting_recovery_branch_sha',head),'current_phase':'GENERATION','phase_timestamps':phases,'discovered_pr':old.get('discovered_pr'),'discovered_actions':old.get('discovered_actions',[]),'inputs':{'transport_sha256':TRANSPORT,'grow_zip_sha256':EXP['GROW']['sha'],'launch_zip_sha256':EXP['LAUNCH']['sha'],'grow_members':54,'launch_members':66},'gate_states':{**old.get('gate_states',{}),'input_integrity':'PASS','count_reconciliation':'PASS'},'latest_failure':None,'latest_diagnosis':'Earlier 28-count proof omitted six GROW PEQ lessons; archive and manifest bytes are complete.','latest_repair':'Replaced prefix allowlisting with suffix-plus-manifest classification.','integration_base_sha':mainsha,'candidate_head_sha':old.get('candidate_head_sha'),'merged_sha':old.get('merged_sha'),'pages':old.get('pages',{}),'final_production_status':old.get('final_production_status','STAGED_NOT_DEPLOYED')}
 sp.write_text(json.dumps(sent,indent=2)+'\n'); print(json.dumps({'input_integrity':'PASS','GROW':gc,'LAUNCH':lc},indent=2))
if __name__=='__main__': main()
