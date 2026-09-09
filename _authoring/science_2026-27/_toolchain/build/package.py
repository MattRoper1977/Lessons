from pathlib import Path
import json, zipfile, shutil, hashlib, html, re

ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['Lesson.html','Lesson.pptx','Slides.pdf','Pupil.docx','Pupil.pdf','Teacher.docx','Teacher.pdf','START_HERE.html']

def main():
 ds=[json.loads(p.read_text()) for p in sorted((ROOT/'content').glob('*.json'))]
 dest=ROOT/'downloads';dest.mkdir(exist_ok=True)
 records=[]
 for pathway in ['BUILD','GROW','LAUNCH']:
  items=sorted([d for d in ds if d['pathway']==pathway],key=lambda d:(0 if 'Spring' in d['sow']['sheet'] else 1,int(re.findall(r'\d+',d['sow']['cells'])[-1])))
  assert len(items)==8,(pathway,len(items))
  stage=ROOT/'build'/'packages'/f'{pathway}_Science_Next_8_Animated_Lesson_Pack';stage.mkdir(exist_ok=True,parents=True)
  for d in items:
   folder=ROOT/'output'/d['id']
   for f in REQUIRED:assert (folder/f).is_file(),(d['id'],f)
   target=stage/d['id']
   if target.exists():shutil.rmtree(target)
   shutil.copytree(folder,target)
   shutil.copyfile(ROOT/'content'/(d['id']+'.json'),target/'Editable_lesson_source.json')
  lines=['# '+pathway+' Science exemplars','', 'Eight complete 40-minute lessons using the Made by Matt classic Science chassis.','', 'Extract this ZIP fully, then open START_HERE.html. Choose a lesson and read Teacher.pdf before teaching.','', '## Inside each lesson','', '- Lesson.html: offline interactive slideshow with controllable SVG explanations, We do investigations, answer feedback, word help, pause, optional timer, teacher briefing and print routes.','- Lesson.pptx: editable slides, text, scientific diagrams and data tables. Detailed answers and teaching guidance are in speaker notes.','- Slides.pdf: static slide copy.','- Pupil.docx and Pupil.pdf: shared evidence and supported, standard and stretch response routes. Choose one route.','- Teacher.docx and Teacher.pdf: scheme links, preparation, 40-minute sequence, worked answers, misconceptions and responsive teaching.','- Editable_lesson_source.json and Diagrams/: reusable authoring source and scientific SVG diagrams where present.','', 'Animations and investigation controls run in Lesson.html. PowerPoint, Word and PDF contain the corresponding editable or printable static diagrams, evidence and teaching steps. Animation timing is for explanation and does not represent the speed of real processes.','', '## Lesson coverage','']
  for d in items:
   sw=d['sow'];lines.extend([f"### {d['title']}",f"{sw['term']} / {sw['week']}",f"Scheme: {sw['sheet']}!{sw['cells']}",sw['exactOutcome'],''])
  lines.extend(['## Validation','', 'Scientific content and rendered PowerPoint, Word and PDF layouts were reviewed. HTML controls and SVG investigation state changes passed automated checks; direct browser and phone testing remains unverified.','', '## Classroom use','','Pathways follow the school schemes; they are not fixed ability labels. Use the short retrieval and hinge checks to choose or change support. All routes preserve the core science goal. Pupils may speak, point, draw, type or dictate.','', 'The default lesson works from supplied cards and clearly labelled constructed sample data. Optional practical routes need the listed equipment and normal school preparation. Practical care is specific to each activity in the teacher guide. Constructed examples are not pupil observations.','', 'HTML answer feedback is interactive. PowerPoint answers are available in speaker notes and the teacher guide. Static PDFs do not reproduce interactive controls. Open HTML after extracting; archive previews and some mobile file viewers do not run HTML.','', 'These are eight additional lessons following the previous 27 exemplars, covering the next Spring review and Summer scheme outcomes, including intentional consolidation and improved topic revisits. They do not constitute a complete term or accredited assessment. They are supplied for review and classroom use; no website publishing is included.','', 'Use the interactive investigation within the shared We do stage time: predict before testing, pause to compare evidence, and explain what changed. The supplied paper route follows the same reasoning.',''])
  (stage/'READ_ME.md').write_text('\n'.join(lines),encoding='utf8')
  rows=''.join('<article><h2>'+html.escape(d['title'])+'</h2><p>'+html.escape(d['sow']['term']+' · '+d['sow']['week'])+'</p><p>'+html.escape(d['objective'])+'</p><a href="'+d['id']+'/START_HERE.html">Open lesson pack</a></article>' for d in items)
  (stage/'START_HERE.html').write_text('<!doctype html><html lang="en-GB"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+pathway+' Science exemplars</title><style>body{font:18px/1.6 Arial,sans-serif;margin:0;background:#f6f1e7;color:#1f2937}main{max-width:900px;margin:auto;padding:28px}h1{font-size:36px}article{background:white;padding:24px;margin:24px 0;border-left:6px solid '+{'BUILD':'#4E7A9B','GROW':'#3F7D6E','LAUNCH':'#7A5C9E'}[pathway]+';border-radius:12px}a{display:inline-block;padding:12px 18px;background:#161d3d;color:white;border-radius:8px}a:focus{outline:3px solid #C9803B;outline-offset:3px}</style><main><p>MADE BY MATT</p><h1>'+pathway+' Science exemplars</h1><p>Eight complete 40-minute lessons. Open a pack, choose one pupil response route and read the teacher guide before teaching.</p>'+rows+'<p>All lesson files work locally after the ZIP is extracted. See READ_ME.md for format details and scheme coverage.</p></main></html>',encoding='utf8')
  zpath=dest/(stage.name+'.zip')
  with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,9) as z:
   for f in sorted(stage.rglob('*')):
    if f.is_file():z.write(f,f.relative_to(stage.parent))
  with zipfile.ZipFile(zpath) as z:assert z.testzip() is None
  assert zpath.stat().st_size<20_000_000,(zpath,zpath.stat().st_size)
  records.append({'pathway':pathway,'file':str(zpath),'bytes':zpath.stat().st_size,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'lessons':[d['id'] for d in items]})
 (ROOT/'qa'/'zip_validation.json').write_text(json.dumps(records,indent=2))
 print(json.dumps(records,indent=2))

if __name__=='__main__':main()
