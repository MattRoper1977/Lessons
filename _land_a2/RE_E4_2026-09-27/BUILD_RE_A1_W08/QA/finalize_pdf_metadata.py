from pathlib import Path
import json,sys,os
from pypdf import PdfReader,PdfWriter
from pypdf.generic import BooleanObject,NameObject,DictionaryObject
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
for item in json.loads((root/'chromium_export_evidence.json').read_text()):
 p=root/item['pdf'];r=PdfReader(p);w=PdfWriter();w.clone_document_from_reader(r)
 w.add_metadata({'/Title':item['title'],'/Author':'Matt Roper','/Subject':'Religious Education','/Creator':'Made by Matt'})
 w._root_object.update({NameObject('/ViewerPreferences'):DictionaryObject({NameObject('/DisplayDocTitle'):BooleanObject(True)})})
 tmp=p.with_suffix('.tmp.pdf')
 with tmp.open('wb') as f:w.write(f)
 os.replace(tmp,p)
print('PDF metadata updated without reflowing rendered pages.')
