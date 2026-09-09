"""Recover literal classic styles. Run with the original Lessons checkout as argv[1]."""
from pathlib import Path
import sys,json,re,hashlib
HERE=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else HERE.parents[1]/'lesson-source'
CONTRACT=SOURCE/'_sownb/STYLE_CONTRACT_v2.json'
refs=json.loads(CONTRACT.read_text())['references']; selected={}
for r in refs:
 selected.setdefault(r['family'],r)
items=[]
for family,r in selected.items():
 raw=(SOURCE/r['path']).read_bytes();s=raw.decode(); styles=re.findall(r'<style([^>]*)>(.*?)</style>',s,re.S)
 original=styles[0][1]; additions=[b for a,b in styles[1:] if any(x in a for x in ['science-navigation-space','science-print-flow'])]
 key=family.lower().replace(' ','_'); target=HERE/'styles'/f'{key}.css'
 target.write_text(original+''.join(additions))
 tokens=dict(re.findall(r'(--[a-zA-Z][\w-]*)\s*:\s*([^;}]+)',original))
 items.append({'family':family,'donor':r['path'],'donor_sha256':hashlib.sha256(raw).hexdigest(),'stylesheet':str(target.relative_to(HERE)),'stylesheet_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'first_style_bytes':len(original.encode()),'first_style_sha256':hashlib.sha256(original.encode()).hexdigest(),'literal_first_style_preserved':True,'donor_patch_count':len(additions),'tokens':{k:v.strip() for k,v in tokens.items()}})
manifest={'schema':'classic-chassis-recovery-v1','contract':str(CONTRACT.relative_to(SOURCE)),'contract_sha256':hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),'source_commit':'c4cfa942cb60735233a63aa656d94a38a6e41c8c','scope':'Literal geometry, source typeface, stage classes, colours and print conventions from 12 classic donor families. Reusable controls are content-independent revisions using the source function names; this does not certify every historical contract gate for new lesson content.','requirements':{'container':'.slide-container','slide':'.slide','active':'.slide.active','stage_border_types':['ido','wedo','independent'],'boxes':['li-box','sc-v4','ido-box','wedo-capture','task-box','scaffold-box','aspire-box'],'font':"'Segoe UI',Tahoma,Geneva,Verdana,sans-serif",'print_routes':['supported','standard','stretch'],'print_scaffold_ids':['print-scaffold-supported','print-scaffold-standard','print-scaffold-stretch'],'print_worksheet_ids':['print-worksheet-supported','print-worksheet-standard','print-worksheet-stretch'],'lundy':['own slide','teacher cue','print-lundy'],'controls':['prevSlide','showTABrief','showColdCall','nextSlide','printPack','switchLevel']},'logo':'Original donor Science has no raster logo; no replacement mark authored. render_shell may embed supplied original logo_data_uri unchanged.','donors':items}
(HERE/'chassis_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Recovered',len(items),'classic family styles.')
