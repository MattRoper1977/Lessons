from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json, sys

head=sys.argv[1]
root=Path('builder-810/domain-split/output/education-lessons')
unit=root/'ICT/Teaching_Packs/GROW_Computing'
files=sorted([*unit.glob('Week_*/*Interactive.html'),*unit.glob('Week_*/Paper_Route/*.pdf'),*unit.glob('Week_*/Paper_Route/*.docx')])
assert len(files)==24
def fetch(p):
 rel=p.relative_to(root).as_posix();url='https://madebymatt.uk/Lessons/'+quote(rel,safe='/')+'?p6='+head
 row={'path':rel,'url':url,'measured_at':datetime.now(timezone.utc).isoformat(),'expected_sha256':sha256(p.read_bytes()).hexdigest()}
 try:
  with urlopen(Request(url,headers={'Cache-Control':'no-cache'}),timeout=40) as response:
   data=response.read();row.update(status=response.status,bytes=len(data),actual_sha256=sha256(data).hexdigest())
  row['match']=row['status']==200 and row['actual_sha256']==row['expected_sha256']
 except Exception as error:row.update(match=False,error=str(error))
 return row
with ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(fetch,files))
result={'source_merge':head,'scope':'Eight served lessons and all sixteen pupil Paper_Route PDF/DOCX files; byte identity does not assert paper-only outcome parity.','matched':sum(r['match'] for r in rows),'total':len(rows),'rows':rows}
Path('recovery/gc1-p6-served-files.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}));print(json.dumps([r for r in rows if not r['match']]))
sys.exit(0 if result['matched']==24 else 1)
