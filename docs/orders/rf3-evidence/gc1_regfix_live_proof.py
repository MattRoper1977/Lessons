from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from hashlib import sha256
import json,sys
root=Path('builder-810/domain-split/output/education-lessons');unit=root/'ICT/Teaching_Packs/GROW_Computing'
files=sorted([*unit.glob('Week_*/*Interactive.html'),*unit.glob('Week_*/Paper_Route/*.pdf'),*unit.rglob('*.sb3')]);assert len(files)==39
head=sys.argv[1]
def measure(p):
 rel=p.relative_to(root).as_posix();url='https://madebymatt.uk/Lessons/'+quote(rel,safe='/')+'?gc1='+head
 want=sha256(p.read_bytes()).hexdigest();row={'path':rel,'url':url,'expected_sha256':want,'measured_at':datetime.now(timezone.utc).isoformat()}
 try:
  with urlopen(Request(url,headers={'Cache-Control':'no-cache'}),timeout=40) as r: data=r.read();row.update(status=r.status,bytes=len(data),actual_sha256=sha256(data).hexdigest())
  row['match']=row['status']==200 and row['actual_sha256']==want
 except Exception as e:row.update(match=False,error=str(e))
 return row
with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(measure,files))
result={'source_merge':head,'lessons':8,'paper_pdfs':8,'scratch_projects':23,'matched':sum(r['match'] for r in rows),'total':len(rows),'rows':rows}
Path('recovery/gc1-regfix-live-proof.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}));print(json.dumps([r for r in rows if not r['match']],indent=2));sys.exit(0 if result['matched']==39 else 1)
