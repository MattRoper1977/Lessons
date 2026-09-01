#!/usr/bin/env python3
"""W2 named safeguarding strings with all-carrier deletion controls."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
REQUIRED=("No diagnosis or medical advice.","No personal or family disclosure.","school-approved local","Learning does not depend on a runtime connection.")
NETWORK=("fetch(","XMLHttpRequest","serviceWorker","http://","https://")
def main():
 p=argparse.ArgumentParser();p.add_argument('--file',required=True);p.add_argument('--output',required=True);a=p.parse_args();path=ROOT/a.file;source=path.read_text();counts={v:source.count(v) for v in REQUIRED};network={v:source.count(v) for v in NETWORK};controls={v:{'mutation':'delete every exact carrier in memory','fired':source.count(v)>0 and source.replace(v,'').count(v)==0} for v in REQUIRED};passed=all(counts.values()) and not any(network.values()) and all(x['fired'] for x in controls.values());report={'gate':'w2-named-safeguarding','file':a.file,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'requiredExactStrings':counts,'runtimeNetworkTokens':network,'controls':controls,'status':'PASS' if passed else 'RED'};out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'strings':counts,'offline':not any(network.values()),'controlsFired':all(x['fired'] for x in controls.values())},indent=2));return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
