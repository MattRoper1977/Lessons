#!/usr/bin/env python3
"""Hash and reproducibly package the three completed P1 preview folders."""
import hashlib,io,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=[]
for p in ['BUILD','GROW','LAUNCH']:
 pack=ROOT/'packs'/f'HUM_Summer_1_{p}_Final'
 lesson=pack/p/'Summer_1/W01'
 for name in [p+'_HUM_S1_W01_Lesson.html','Editable_Slides.pptx','Teacher_Notes.docx','Teacher_Notes.pdf','Knowledge_Organiser.html','Knowledge_Organiser.pdf','Pupil_Resources.html','Pupil_Resources.pdf','Sources_and_checks.html']:assert (lesson/name).is_file(),str(lesson/name)
 files=sorted(f for f in pack.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
 (pack/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(pack))+'\n' for f in files))
 def make():
  b=io.BytesIO()
  with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for f in sorted(pack.rglob('*')):
    if f.is_file():
     info=zipfile.ZipInfo(str(f.relative_to(pack)),(2026,9,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,f.read_bytes())
  return b.getvalue()
 a,b=make(),make();assert a==b and len(a)<20*1024*1024
 dest=ROOT/(pack.name+'_P1.zip');dest.write_bytes(a)
 out.append({'pathway':p,'zip':dest.name,'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest(),'two_packaging_passes_identical':True,'full_binary_regeneration_parity':'NOT CLAIMED at P1','files':len(files)+1})
(ROOT/'qa/package_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
