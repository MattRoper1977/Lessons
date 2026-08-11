#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

SENTINEL="grow-launch-estate-v3-autonomous-closeout-2026-08-10"
HISTORIC="1e8a428b523d1b970a8a3a2ab2a99f48a8271d09"
TRANSPORT_SHA="782ff5865e1406c159c78081bcc218bdaa46678e5c42448a6f298f696ca73f5e"
TRANSPORT_SIZE=102160
POST_HEADING="Post-verification edits applied 2026-08-10"
PROTECTED=["Art_Teesside","GROW_ASDAN","LAUNCH_ASDAN","Grow/Slideshows","Launch/Slideshows","Science_Teesside","Humanities_Teesside","Baseline_Weeks","BUILD_Estate_v3"]
EXPECTED={
 "GROW":{"files":51,"html":41,"lessons":34,"manifest":"0e83488ecad487c0da697c083f79fb99b783660fed193f1efe0f1fce1aeddd30","subjects":{"Art":8,"Humanities":8,"ASDAN":18},"zip":{"name":"GROW_ESTATE_v3_REPAIRED_2026-08-10.zip","sha256":"95bf78a4124f20196508748c4b44c3935b0eb09181bac69fcc00c4c0a5e6f58a","size":418166,"members":54,"html_members":41}},
 "LAUNCH":{"files":63,"html":53,"lessons":46,"manifest":"0946be2600bc9794a2d71a74191ed9e01aa8c6d9cfa6a61c7bd32f4c6754170a","subjects":{"Art":8,"Humanities":8,"ASDAN":30},"zip":{"name":"LAUNCH_ESTATE_v3_REPAIRED_2026-08-10.zip","sha256":"aacbeda81d4bb5d665a0d70aafd5732431b64457a313e2f8843a120d0515768c","size":517266,"members":66,"html_members":53}}
}

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for block in iter(lambda:f.read(1048576),b""): h.update(block)
 return h.hexdigest()
def write(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def git(repo,*args,bytes_out=False):
 r=subprocess.run(["git",*args],cwd=repo,check=True,capture_output=True,text=not bytes_out)
 return r.stdout

def inventory(root):
 rows=[]; seen={}
 for p in sorted(x for x in root.rglob("*") if x.is_file()):
  rel=p.relative_to(root).as_posix(); q=PurePosixPath(rel)
  if q.is_absolute() or ".." in q.parts or p.is_symlink() or p.stat().st_mode&0o111: raise SystemExit(f"unsafe source member: {rel}")
  if rel.casefold() in seen: raise SystemExit(f"case collision: {seen[rel.casefold()]} / {rel}")
  seen[rel.casefold()]=rel
  rows.append({"path":rel,"size":p.stat().st_size,"sha256":sha_file(p),"html":p.suffix.lower()==".html"})
 material="\n".join(f"{r['path']}\0{r['size']}\0{r['sha256']}" for r in rows).encode()
 return rows,sha_bytes(material)

def subject(rel):
 parts=[x.casefold() for x in PurePosixPath(rel).parts]; stem=PurePosixPath(rel).stem.casefold()
 if any("humanit" in x for x in parts) or stem.startswith(("hum_","humanities_")): return "Humanities"
 if any(x in {"art","arts","art_teesside"} or x.startswith("art_") for x in parts) or stem.startswith("aa_") or "arts_award" in stem: return "Art"
 if any("asdan" in x or "peq" in x or "vocational" in x or "pfa" in x for x in parts) or stem.startswith(("peq_","asdan_")): return "ASDAN"
 return None

def destination(estate,rel):
 p=PurePosixPath(rel); parts=list(p.parts); name=parts[-1]
 parts[-1]="index.html" if name.casefold().startswith("start_here") else re.sub(r"_OUTSTANDING_V3_TEST(?=\.html$)","",name,flags=re.I)
 return f"{estate}_Estate_v3/"+"/".join(parts)

def manifest_hits(root,rel):
 base=PurePosixPath(rel).name; hits=[]
 for p in sorted(root.rglob("*")):
  if not p.is_file() or p.suffix.lower() not in {".json",".csv",".tsv",".md",".txt"}: continue
  t=p.read_text(encoding="utf-8",errors="replace")
  if base in t or rel in t: hits.append(p.relative_to(root).as_posix())
 return hits

def classify(estate,root,rows):
 out=[]; dests=defaultdict(list)
 for r in rows:
  if not r["html"]: continue
  rel=r["path"]; p=PurePosixPath(rel); n=p.name.casefold()
  lesson=bool(re.search(r"_OUTSTANDING_V3_TEST\.html$",p.name,re.I))
  if lesson: kind="deployable lesson"; rule="validated authored lesson suffix; no filename-prefix allowlist"
  elif n.startswith("start_here") and len(p.parts)==1: kind="estate hub"; rule="root START_HERE HTML"
  elif n.startswith("start_here"): kind="subject hub"; rule="nested START_HERE HTML"
  else: kind="audit/support/non-deployable"; rule="HTML without validated lesson suffix"
  week=None; strand=None
  m=re.search(r"(?:^|[_-])W(\d+)(?:L(\d+))?(?:[_-]|$)",p.stem,re.I)
  if m: week=f"W{int(m.group(1))}"; strand=f"L{int(m.group(2))}" if m.group(2) else None
  pm=re.search(r"(?:^|[_-])PEQ[_-]?W(\d+)(?:[_-]|$)",p.stem,re.I)
  if pm: week=f"W{int(pm.group(1))}"; strand="PEQ"
  dst=destination(estate,rel); dests[dst.casefold()].append(rel)
  out.append({"estate":estate,"source_path":rel,"source_size":r["size"],"source_sha256":r["sha256"],"classification":kind,"classification_rule":rule,"source_manifest_entries":manifest_hits(root,rel),"subject":subject(rel),"pathway":estate,"week":week,"strand":strand,"intended_destination_path":dst,"duplicate_collision_status":"PENDING"})
 collisions={k:v for k,v in dests.items() if len(v)>1}
 for x in out: x["duplicate_collision_status"]="COLLISION" if x["intended_destination_path"].casefold() in collisions else "UNIQUE"
 return out,collisions

def audit_hits(root):
 hits=[]
 for p in sorted(root.rglob("*")):
  if p.is_file() and p.suffix.lower() in {".md",".txt",".html"} and POST_HEADING.casefold() in p.read_text(encoding="utf-8",errors="replace").casefold(): hits.append(p.relative_to(root).as_posix())
 if not hits: raise SystemExit(f"missing `{POST_HEADING}` under {root}")
 return hits

def tree_manifest(repo,commit):
 trees={}; aggregate=[]
 for tree in PROTECTED:
  files=[]
  for line in git(repo,"ls-tree","-r",commit,"--",tree).splitlines():
   if not line: continue
   meta,path=line.split("\t",1); mode,typ,blob=meta.split()
   if typ!="blob": continue
   data=git(repo,"show",f"{commit}:{path}",bytes_out=True)
   row={"path":path,"git_blob_sha":blob,"byte_size":len(data),"sha256":sha_bytes(data),"mode":mode}; files.append(row); aggregate.append(f"{path}\0{blob}\0{len(data)}\0{row['sha256']}")
  trees[tree]={"file_count":len(files),"files":files}
 return {"commit":commit,"trees":trees,"aggregate_sha256":sha_bytes("\n".join(sorted(aggregate)).encode())}

def compare(a,b):
 am={x["path"]:(x["git_blob_sha"],x["byte_size"],x["sha256"]) for t in a["trees"].values() for x in t["files"]}; bm={x["path"]:(x["git_blob_sha"],x["byte_size"],x["sha256"]) for t in b["trees"].values() for x in t["files"]}
 added=sorted(set(bm)-set(am)); removed=sorted(set(am)-set(bm)); modified=sorted(x for x in set(am)&set(bm) if am[x]!=bm[x])
 return {"identical":not(added or removed or modified),"added":added,"removed":removed,"modified":modified,"base_aggregate_sha256":a["aggregate_sha256"],"candidate_aggregate_sha256":b["aggregate_sha256"]}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,required=True); ap.add_argument("--grow",type=Path,required=True); ap.add_argument("--launch",type=Path,required=True); ap.add_argument("--historic-sha",default=HISTORIC); ap.add_argument("--integration-sha",required=True); ap.add_argument("--starting-branch-sha",required=True); ap.add_argument("--transport",type=Path,required=True); args=ap.parse_args()
 repo=args.repo.resolve(); roots={"GROW":args.grow.resolve(),"LAUNCH":args.launch.resolve()}; inputs={}; records=[]; collisions={}
 if sha_file(args.transport)!=TRANSPORT_SHA or args.transport.stat().st_size!=TRANSPORT_SIZE: raise SystemExit("deterministic transport mismatch")
 for name,root in roots.items():
  if not root.is_dir() or any(p.is_dir() and p.name.casefold()=="science" for p in root.iterdir()): raise SystemExit(f"invalid {name} root / Science present")
  rows,digest=inventory(root); recs,col=classify(name,root,rows); records+=recs; collisions[name]=col; exp=EXPECTED[name]; kinds=Counter(x["classification"] for x in recs); subs=Counter(x["subject"] for x in recs if x["classification"]=="deployable lesson"); audits=audit_hits(root)
  checks={"files":len(rows)==exp["files"],"html":sum(x["html"] for x in rows)==exp["html"],"manifest":digest==exp["manifest"],"lessons":kinds["deployable lesson"]==exp["lessons"],"subjects":dict(subs)==exp["subjects"],"no_collisions":not col,"audit_heading":bool(audits),"science_absent":True}
  if not all(checks.values()): raise SystemExit(f"{name} reconciliation failed: {checks}; kinds={dict(kinds)}; subjects={dict(subs)}")
  inputs[name.lower()]={"original_zip":{**exp["zip"],"verified_out_of_band_from_exact_user_upload":True,"repository_transport_is_original_zip_bytes":False},"extracted_source":{"file_count":len(rows),"html_count":sum(x["html"] for x in rows),"manifest_sha256":digest,"science_folder_present":False,"post_verification_heading_hits":audits,"files":rows},"checks":checks}
 lessons=Counter(x["estate"] for x in records if x["classification"]=="deployable lesson"); total=sum(lessons.values()); peq=sorted(x["source_path"] for x in records if x["estate"]=="GROW" and x["classification"]=="deployable lesson" and re.search(r"(?:^|/)PEQ_W[1-6]",x["source_path"],re.I))
 if lessons!=Counter({"LAUNCH":46,"GROW":34}) or total!=80 or len(records)!=94 or len(peq)!=6: raise SystemExit(f"combined count failure: lessons={dict(lessons)} html={len(records)} peq={peq}")
 historic=tree_manifest(repo,args.historic_sha); integration=tree_manifest(repo,args.integration_sha)
 out=repo/"_glv3"
 write(out/"INPUT_INTEGRITY.json",{"sentinel":SENTINEL,"generated_at":now(),"repository":"MattRoper1977/Lessons","source_kind":"DETERMINISTIC_EXTRACTED_FILE_TRANSPORT","deterministic_transport":{"sha256":TRANSPORT_SHA,"size":TRANSPORT_SIZE,"valid":True,"not_byte_identical_recreation_of_original_zips":True},"superseded_transport":{"reported_sha256":"efef35d7c8504f603646663da603a2f3690ed8204b2af7d0730b52560a9db918","corrupt_reconstructed_sha256":"777fcdafefc246c5c6b68a559886dc27b641471b7638ea79e51640c3e62791fd","status":"REJECTED_CORRUPT_XZ"},"inputs":inputs})
 write(out/"COUNT_RECONCILIATION.json",{"sentinel":SENTINEL,"generated_at":now(),"result":"PASS","cause_of_prior_28_count":{"actual_cause":"The prior proof used a narrow filename-prefix allowlist and omitted the six genuine GROW PEQ lesson files PEQ_W1 through PEQ_W6. Classification now uses the validated authored lesson suffix plus source inventory, not a prefix allowlist.","previous_count":28,"corrected_count":34,"omitted_files":peq,"input_missing":False,"tooling_defect":True},"expected":{"GROW":{"lessons":34,"subjects":EXPECTED["GROW"]["subjects"]},"LAUNCH":{"lessons":46,"subjects":EXPECTED["LAUNCH"]["subjects"]},"combined_lessons":80,"combined_source_html":94},"actual":{"lessons_by_estate":dict(lessons),"combined_lessons":total,"combined_source_html":len(records)},"destination_collisions":collisions,"html_members":records})
 write(out/"PROTECTED_TREES.json",{"sentinel":SENTINEL,"generated_at":now(),"historic":historic,"integration":integration,"historic_vs_integration":compare(historic,integration),"authoritative_baseline":args.integration_sha,"candidate_comparison_pending":True})
 old={}
 try: old=json.loads((out/"AUTONOMOUS_SENTINEL.json").read_text())
 except Exception: pass
 phases=old.get("phase_timestamps",{}) if isinstance(old.get("phase_timestamps"),dict) else {}; phases.update({"INPUT_RECONSTRUCTION":now(),"COUNT_RECONCILIATION":now()})
 write(out/"AUTONOMOUS_SENTINEL.json",{"sentinel":SENTINEL,"repository":"MattRoper1977/Lessons","historic_rollback_sha":args.historic_sha,"starting_main_sha":args.integration_sha,"starting_recovery_branch_sha":args.starting_branch_sha,"current_phase":"COUNT_RECONCILIATION","phase_timestamps":phases,"discovered_pr":old.get("discovered_pr",{"number":108,"url":"https://github.com/MattRoper1977/Lessons/pull/108"}),"actions":old.get("actions",{}),"input_hashes_and_counts":{"transport_sha256":TRANSPORT_SHA,"grow_manifest_sha256":EXPECTED["GROW"]["manifest"],"launch_manifest_sha256":EXPECTED["LAUNCH"]["manifest"],"grow_lessons":34,"launch_lessons":46,"total_lessons":80},"gate_states":{**(old.get("gate_states",{}) if isinstance(old.get("gate_states"),dict) else {}),"source_integrity":"PASS","count_reconciliation":"PASS","protected_baseline_captured":"PASS"},"latest_failure":None,"latest_diagnosis_and_repair":{"failure":"Corrupt staged transport and 28-versus-34 mismatch","diagnosis":"Old XZ corrupt; old prefix classifier omitted PEQ_W1–W6","repair":"Exact ZIPs verified; deterministic extracted transport verified; suffix-and-manifest classifier restores six genuine PEQ lessons"},"candidate_head_sha":old.get("candidate_head_sha"),"merged_sha":old.get("merged_sha"),"pages":old.get("pages",{}),"final_production_status":old.get("final_production_status","STAGED_NOT_DEPLOYED"),"updated_at":now()})
 print(json.dumps({"result":"PASS","grow_lessons":34,"launch_lessons":46,"total_lessons":80,"source_html":94,"peq_restored":peq}))
if __name__=="__main__": main()
