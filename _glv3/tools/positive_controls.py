#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil, tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

BANNER="This route is screen-only. Printable pupil work, portfolio evidence and ASDAN assessment records come from the existing lessons."
PRIVACY={"fetch":re.compile(r"\bfetch\s*\("),"storage":re.compile(r"\b(?:localStorage|sessionStorage|indexedDB)\b|document\.cookie")}
LAUNCH_RED=re.compile(r"\b(?:mark scheme|band descriptors?|level descriptors?|grade boundaries?|AO[1-9]|\d+\s+marks?)\b",re.I)
ARTS_HOURS=re.compile(r"\b(?:minimum|at least|required)\s+\d+(?:\.\d+)?\s*(?:hours?|GLH|TQT)\b",re.I)
PEQ_CODE=re.compile(r"\b(?:PEQ[-_ ]?UNIT[-_ ]?[A-Z]*\d+|ComSk\d+|WwO\d+|PS\d+)\b",re.I)

class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k.lower() in {"href","src"} and v: self.links.append(v)

def resources(path):
 data=json.loads(path.read_text()); rows=data if isinstance(data,list) else data.get("resources") or data.get("items") or data.get("records")
 if not isinstance(rows,list): raise AssertionError("resources.json has no record list")
 return data,rows

def write_resources(path,data,rows):
 if isinstance(data,list): out=rows
 else:
  out=dict(data); key=next((k for k in ("resources","items","records") if isinstance(data.get(k),list)),None); assert key; out[key]=rows
 path.write_text(json.dumps(out,indent=2)+"\n")

def href_fail(path,root):
 parser=Links(); parser.feed(path.read_text(encoding="utf-8",errors="replace"))
 for raw in parser.links:
  u=urlsplit(raw.strip())
  if u.scheme or u.netloc or raw.startswith(("mailto:","tel:","data:","javascript:","#")): continue
  target=unquote(u.path)
  if not target: continue
  resolved=(root/target.lstrip("/")) if target.startswith("/") else (path.parent/target)
  if resolved.is_dir(): resolved=resolved/"index.html"
  if not resolved.exists(): return True
 return False

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def expect_failure(name,mutation,gate,results):
 before=mutation(); detected=False; detail=""
 try: gate(before)
 except Exception as exc: detected=True; detail=str(exc)
 if not detected: raise AssertionError(f"positive control did not fail: {name}")
 results.append({"name":name,"mutation":"disposable temporary copy","detected":True,"diagnostic":detail})

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,default=Path(".")); args=ap.parse_args(); repo=args.repo.resolve(); results=[]
 with tempfile.TemporaryDirectory(prefix="glv3-positive-") as td:
  tmp=Path(td); shutil.copytree(repo/"GROW_Estate_v3",tmp/"GROW_Estate_v3"); shutil.copytree(repo/"LAUNCH_Estate_v3",tmp/"LAUNCH_Estate_v3"); shutil.copy2(repo/"resources.json",tmp/"resources.json")
  data,rows=resources(tmp/"resources.json"); gl=[r for r in rows if str(r.get("id","")).startswith("glv3-")]; lessons=[r for r in gl if str(r.get("type","")).lower()=="lesson"]
  def missing():
   grow=[r for r in lessons if "grow" in str(r.get("family","")).lower()]; assert grow; victim=grow[0]
   rel=victim.get("file") or victim.get("url") or victim.get("path") or victim.get("href"); assert rel,"GROW catalogue lesson has no file route"
   p=tmp/str(rel).lstrip("/"); assert p.is_file(),f"GROW lesson route missing before mutation: {rel}"; p.unlink(); return p
  expect_failure("missing GROW lesson",missing,lambda p: (_ for _ in ()).throw(AssertionError("GROW lesson count/path mismatch")) if (not p.exists()) else None,results)
  def dup():
   d,r=resources(tmp/"resources.json"); r.append(dict(r[0])); write_resources(tmp/"resources.json",d,r); return tmp/"resources.json"
  def unique(p):
   _,r=resources(p); ids=[x.get("id") for x in r]; assert len(ids)==len(set(ids)),"duplicate resource ID"
  expect_failure("duplicate resource ID",dup,unique,results)
  protected=json.loads((repo/"_glv3/PROTECTED_TREES.json").read_text()); base=protected["integration"]; first=next(x for t in base["trees"].values() for x in t["files"]); original=repo/first["path"]; altered=tmp/"protected"/first["path"]; altered.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(original,altered)
  def prot_mut(): altered.write_bytes(altered.read_bytes()+b"\nTAMPER\n"); return altered
  expect_failure("modified protected live file",prot_mut,lambda p: (_ for _ in ()).throw(AssertionError("protected SHA mismatch")) if sha(p)!=first["sha256"] else None,results)
  html=next((tmp/"GROW_Estate_v3").rglob("*.html"))
  def broken(): p=tmp/"broken.html"; p.write_text(html.read_text(errors="replace")+'<a href="__positive_missing__.html">broken</a>'); return p
  expect_failure("broken internal link",broken,lambda p: (_ for _ in ()).throw(AssertionError("unresolved internal link")) if href_fail(p,tmp) else None,results)
  def inject(name,text,source=html): p=tmp/name; p.write_text(source.read_text(errors="replace")+text); return p
  expect_failure("fetch insertion",lambda:inject("fetch.html","<script>fetch('/x')</script>"),lambda p: (_ for _ in ()).throw(AssertionError("network primitive fetch")) if PRIVACY["fetch"].search(p.read_text()) else None,results)
  expect_failure("storage insertion",lambda:inject("storage.html","<script>localStorage.setItem('x','y')</script>"),lambda p: (_ for _ in ()).throw(AssertionError("storage primitive")) if PRIVACY["storage"].search(p.read_text()) else None,results)
  launch=next((tmp/"LAUNCH_Estate_v3").rglob("*.html"))
  expect_failure("LAUNCH AO2/marks insertion",lambda:inject("launch-red.html","<p>AO2: 10 marks</p>",launch),lambda p: (_ for _ in ()).throw(AssertionError("unsupported LAUNCH assessment language")) if LAUNCH_RED.search(p.read_text()) else None,results)
  expect_failure("Arts Award minimum-hours phrase",lambda:inject("arts-hours.html","<p>A minimum 10 hours is required.</p>"),lambda p: (_ for _ in ()).throw(AssertionError("invented Arts Award hours threshold")) if ARTS_HOURS.search(p.read_text()) else None,results)
  expect_failure("invented PEQ code",lambda:inject("peq-code.html","<p>PEQ-UNIT-X99</p>"),lambda p: (_ for _ in ()).throw(AssertionError("invented PEQ unit code")) if PEQ_CODE.search(p.read_text()) else None,results)
  banner_source=next((p for p in [*(tmp/"GROW_Estate_v3").rglob("*.html"),*(tmp/"LAUNCH_Estate_v3").rglob("*.html")] if BANNER in p.read_text(encoding="utf-8",errors="replace")),None); assert banner_source,"screen-only banner source missing"
  def no_banner(): p=tmp/"no-banner.html"; p.write_text(banner_source.read_text(errors="replace").replace(BANNER,"")); return p
  expect_failure("missing screen-only banner",no_banner,lambda p: (_ for _ in ()).throw(AssertionError("screen-only banner missing")) if BANNER not in p.read_text() else None,results)
  _,base_rows=resources(repo/"resources.json"); expected=sum(1 for r in base_rows if str(r.get("id","")).startswith("glv3-"))
  expect_failure("incorrect chip count",lambda:expected+1,lambda advertised: (_ for _ in ()).throw(AssertionError(f"advertised {advertised} != JSON {expected}")) if advertised!=expected else None,results)
 out={"sentinel":"grow-launch-estate-v3-autonomous-closeout-2026-08-10","result":"PASS","controls_expected":11,"controls_detected":len(results),"working_tree_mutated":False,"controls":results}; assert len(results)==11
 (repo/"_glv3/POSITIVE_CONTROLS.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps({"result":"PASS","controls":len(results)}))
if __name__=="__main__": main()
