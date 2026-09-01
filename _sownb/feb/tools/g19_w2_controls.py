#!/usr/bin/env python3
"""Fire FEB g19 foreign-token and duplicate-declaration controls."""
from __future__ import annotations
import argparse, importlib.util, json, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
MODULE=ROOT/'_sownb/feb/tools/g19_token_ownership.py'
spec=importlib.util.spec_from_file_location('g19_impl',MODULE);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def main():
 p=argparse.ArgumentParser();p.add_argument('--family',required=True);p.add_argument('--file',required=True);p.add_argument('--config',default='_sownb/G19_TOKEN_OWNERSHIP_FEB.json');p.add_argument('--output',required=True);a=p.parse_args();source=(ROOT/a.file).read_text();config=mod.load_config(ROOT/a.config);green=mod.measure(ROOT/a.file,a.family,config)
 own=next(iter(config['families'][a.family]['values']));own_value=config['families'][a.family]['values'][own][0]
 other=next(name for fam,data in config['families'].items() if fam!=a.family for name in data['values'] if name not in config['families'][a.family]['values']);other_value=next(data['values'][other][0] for fam,data in config['families'].items() if other in data['values'])
 rows=[]
 with tempfile.TemporaryDirectory(dir=ROOT/'_sownb/feb') as td:
  td=Path(td)
  for label,injection in [('foreign',f'{other}:{other_value};'),('duplicate',f'{own}:{own_value};')]:
   path=td/f'{label}.html';path.write_text(source.replace(':root{',':root{'+injection,1));result=mod.measure(path,a.family,config);rows.append({'control':label,'injection':injection,'status':result['status'],'fired':result['status']=='RED','foreign':result['foreignFamilyTokens'],'duplicates':result['duplicateDeclarations']})
 passed=green['status']=='PASS' and all(r['fired'] for r in rows);report={'gate':'g19-w2-controls','candidate':a.file,'green':green,'controls':rows,'status':'PASS' if passed else 'RED'};out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'green':green['status'],'controls':rows},indent=2));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
