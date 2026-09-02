#!/usr/bin/env python3
"""g10 candidate personal-name pattern detection and role classification.

The implementation contains no personal name. Legitimate public-figure and
declared-exemplar values are loaded from separate reviewed registers.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, re
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[3]
PAIR=re.compile(r"\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b")
ROLE={"learner","name","teacher","adult","staff","audience","influence","science","humanities","asdan","supported","standard","stretch","review","evidence","autumn","spring","lesson","entry","level","build","route","space","voice","skeleton","nutrition","rocks","week","timeline","now","record","role","evaluation"}
PLACES_BUILTIN={"earth","teesside","stockton","tees","estuary"}
def places_registry(path):
 """Every word of every bullet in _sownb/PLACES.md is a place token (VB-RUN11F NAMES pair rule)."""
 if not path.exists():return set()
 return {tok.casefold() for line in path.read_text().splitlines() if line.startswith('- ') and not line[2:].startswith('"') for tok in line[2:].split()}
PLACES=PLACES_BUILTIN|places_registry(ROOT/'_sownb/PLACES.md')
def registry(path):
 if not path.exists():return set()
 return {line[2:].strip().casefold() for line in path.read_text().splitlines() if line.startswith('- ') and len(line[2:].split())>=2}
def pupil_text(path):
 tree=html.fromstring(path.read_text());decks=tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]')
 if len(decks)!=1: raise ValueError(f'MEASUREMENT INVALID: expected exactly one main.deck, measured {len(decks)}')
 node=copy.deepcopy(decks[0])
 for child in list(node.iterdescendants()):
  tag=child.tag.lower() if isinstance(child.tag,str) else ''
  if tag in {'script','style','svg','template','noscript'} or child.get('data-mbm-guide') is not None or child.get('data-audience','').lower()=='staff':
   parent=child.getparent()
   if parent is not None:parent.remove(child)
 return ' '.join(node.text_content().split())
def classify(value,public,examples):
 low=value.casefold();tokens=set(low.split())
 if low in public:return 'PUBLIC-FIGURE'
 if low in examples:return 'DECLARED-EXEMPLAR'
 if tokens & PLACES:return 'PLACE'
 if tokens & ROLE:return 'ROLE-LABEL'
 return 'UNRESOLVED'
def candidates(text,public,examples):
 seen=[]
 for match in PAIR.finditer(text):
  value=match.group(0)
  if value not in seen:seen.append(value)
 return [{'candidate':value,'classification':classify(value,public,examples)} for value in seen]
def main():
 p=argparse.ArgumentParser();p.add_argument('--file',required=True);p.add_argument('--output',required=True);a=p.parse_args();path=ROOT/a.file;public_path=ROOT/'_sownb/feb/PUBLIC_FIGURES.md';public=registry(public_path);examples=registry(ROOT/'_sownb/DECLARED_EXEMPLARS.md')
 if not public: raise SystemExit('MEASUREMENT INVALID: reviewed public-figure register absent or empty')
 text=pupil_text(path);rows=candidates(text,public,examples);unresolved=[r for r in rows if r['classification']=='UNRESOLVED']
 synthetic=''.join(('Test','given'))+' '+''.join(('Test','family'));red=candidates(text+' '+synthetic,public,examples);red_fired=any(r['candidate']==synthetic and r['classification']=='UNRESOLVED' for r in red);role=' '.join(('Learner','Name'));role_green=classify(role,public,examples)=='ROLE-LABEL';place=' '.join(('Newport','Bridge'));place_green=classify(place,public,examples)=='PLACE';structural=["Week Timeline","Now Record","Role Evaluation"];structural_green=all(classify(value,public,examples)=='ROLE-LABEL' for value in structural);nonvacuous=bool(text) and red_fired and role_green and structural_green and place_green
 report={'gate':'g10-role-classification','file':a.file,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'searchSpace':'pupil-facing main.deck after scripts, styles, SVG and keyed staff guidance are removed','corpusChars':len(text),'candidates':rows,'unresolved':unresolved,'controls':{'unresolvedRedFired':red_fired,'roleGreen':role_green,'placeGreen':place_green,'placeRegisterTokens':len(PLACES),'structuralRoleLabels':structural,'structuralRoleGreen':structural_green,'nonVacuous':nonvacuous},'s23':'MEASUREMENT INVALID by design; S23_NAMES is prohibited','status':'PASS' if nonvacuous and not unresolved else 'RED'};out=ROOT/a.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'candidates':rows,'unresolved':unresolved,'controls':report['controls']},indent=2));return 0 if report['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
