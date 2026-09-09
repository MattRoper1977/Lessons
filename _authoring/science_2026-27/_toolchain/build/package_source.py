from pathlib import Path
import zipfile,json,hashlib

ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'downloads/Science_24_Animated_Exemplars_Authoring_Source.zip'
prefix=Path('Science_24_Animated_Exemplars_Authoring_Source')
files=[]
for folder in ['content','chassis','build','authoring']:
 for f in (ROOT/folder).rglob('*'):
  rel=f.relative_to(ROOT)
  if not f.is_file() or any(x in rel.parts for x in ['__pycache__','node_modules','packages','figures','ppt']):continue
  if folder=='build' and f.name in ['author_build.py','author_grow.py']:continue
  if f.suffix not in ['.json','.py','.mjs','.css','.js','.md']:continue
  files.append((f,prefix/rel))
for f in (ROOT/'qa').glob('*.json'):
 if 'library' not in f.name:files.append((f,prefix/'qa'/f.name))
for name in ['FINAL_QA.json','COMPLETION_REPORT.txt']:
 f=ROOT/'qa'/'ppt'/name
 if f.is_file():files.append((f,prefix/'qa'/'ppt'/name))
for name in ['SCHEMA.md','selection_map.json']:
 files.append((ROOT/name,prefix/name))
for f in (ROOT.parent/'science_source_audit').glob('*'):
 if f.name in ['BUILD_SOW.xlsx','GROW_SOW.xlsx','LAUNCH_SOW.xlsx','BUILD_Science_SOW.json','GROW_Science_SOW.json','LAUNCH_Science_SOW.json']:
  files.append((f,prefix/'scheme_references'/f.name))
readme='''# Science exemplar authoring source

The three classroom ZIPs contain all 24 lessons in PowerPoint, Word, PDF and HTML. Standard classroom editing needs only PowerPoint, Word or compatible software.

This optional source archive preserves final lesson JSON, classic chassis, SVG/HTML interaction code, office generators, scheme references and validation reports. The final content JSON files are authoritative. Authoring scripts preserve how lessons were drafted and can predate final reviewed corrections; do not run them over edited content without reviewing their changes.

Rebuilding requires Python with python-docx, Pillow and PyMuPDF, Node with the presentation dependencies referenced by ppt.mjs, and the managed office renderer. Some runtime and skill paths are environment-specific and need adaptation elsewhere. Dependencies are not bundled.

Run the document, presentation and HTML generators against content JSON. Review regenerated diagrams, answers and page layouts before teaching. build/package.py makes eight-lesson pathway ZIPs and checks each stays below 20,000,000 bytes.

Animations are controllable SVG elements in the HTML lessons. Selected lessons extend their diagrams with model controls for investigation and explanation. Each of the 24 lessons also has three authored prediction/test/explanation decisions. Diagram transition timing is not a real scientific time scale. Interactive state changes passed automated checks; direct browser and physical-phone testing remains unverified.
'''
dest.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,9) as z:
 z.writestr(str(prefix/'READ_ME.md'),readme)
 for src,arc in sorted(files):z.write(src,str(arc))
with zipfile.ZipFile(dest) as z:assert z.testzip() is None
assert dest.stat().st_size<20_000_000
print(json.dumps({'file':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}))
