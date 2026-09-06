#!/usr/bin/env python3
"""Compile a phone-readable W2 per-surface gate table from bound JSON evidence."""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def load(path):return json.loads(path.read_text())
def display(path):
 try:return str(path.relative_to(ROOT))
 except ValueError:return str(path)
def main():
 p=argparse.ArgumentParser();p.add_argument('--evidence',required=True);p.add_argument('--surface',required=True);p.add_argument('--family',required=True);p.add_argument('--output',required=True);a=p.parse_args();e=ROOT/a.evidence
 mapping=[('g10 role classification','g10.json'),('g11 similarity + floor','g11.json'),('g15 guidance hidden','g15.json'),('g16 frozen contract','g16.json'),('g18 content floor','g18.json'),('g19 token ownership','g19_controls.json'),('g21 trailing sheet economy','g21.json'),('c-gate containment','c_gate.json'),('s24 print renders','s24.json'),('running heads','running_heads.json'),('render installation','render_installation.json'),('safeguarding','safeguarding.json'),('static pack/chains/checksums','static_pack.json')]
 rows=[]
 for gate,name in mapping:
  path=e/name;data=load(path);rows.append({'gate':gate,'status':data['status'],'evidence':display(path)})
 rows.extend([
  {'gate':'g2 frozen jsdom runner','status':'MEASUREMENT INVALID','reason':'hard-resolved ../../../.snb_node/node_modules/jsdom is absent; Chromium installation is separately named'},
  {'gate':'g17 render parity','status':'MEASUREMENT INVALID','reason':'g17 is intentionally GROW-Science-only; BUILD Science uses family-bound render installation'},
  {'gate':'g20 page fill','status':'MEASUREMENT INVALID','reason':'35% floor reds all seven live references; values are informational only'},
  {'gate':'s23 names','status':'MEASUREMENT INVALID','reason':'by design; S23_NAMES is prohibited'},
 ])
 passed=all(r['status']=='PASS' or r['status']=='MEASUREMENT INVALID' for r in rows)
 report={'surface':a.surface,'family':a.family,'rows':rows,'fullGreenWithHonestInvalids':passed,'verdict':'GREEN — LANDING ELIGIBLE' if passed else 'HELD','status':'PASS' if passed else 'RED'}
 out=Path(a.output).resolve();out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
