"""Additional checks on the actual Chrome-generated GROW PDFs.

The original Science print inspector still renders and checks every PDF.
This adds pupil-answer exclusion, answer-key inclusion, and mutation controls.
"""
from pathlib import Path
import argparse,json
import fitz

def normalize(value):return ' '.join(value.split())

def inspect(text,required,answer,include_answers):
    text=normalize(text);required=normalize(required);answer=normalize(answer)
    problems=[]
    if required not in text:problems.append('Required task heading is missing')
    if include_answers and answer not in text:problems.append('Explicit answer key is missing its worked explanation')
    if not include_answers and answer in text:problems.append('Pupil task leaks a worked explanation')
    return problems

def complete_exports(entries, ids):
    expected={f'{code}-{kind}.pdf':answers for code in ids for kind,answers in [('pupil-task',False),('answer-key',True)]}
    return len(entries)==len(expected) and {e['file'] for e in entries}==set(expected) and all(e['includeAnswers'] is expected[e['file']] for e in entries)

def main(root):
    browser=json.loads((root/'grow-resource-browser.json').read_text())
    rows=[]
    for entry in browser['pdfs']:
        with fitz.open(root/entry['file']) as pdf:text=' '.join(p.get_text() for p in pdf)
        rows.append({'file':entry['file'],'includeAnswers':entry['includeAnswers'],'problems':inspect(text,entry['requiredText'],entry['answerFragment'],entry['includeAnswers'])})
    expected={c['id'] for c in browser['inputs']['pages']}
    complete=complete_exports(browser['pdfs'],expected)
    controls={
      'planted-pupil-answer-leak':bool(inspect('Task heading. Worked answer.','Task heading.','Worked answer.',False)),
      'planted-missing-answer-key':bool(inspect('Task heading.','Task heading.','Worked answer.',True)),
      'planted-missing-task-heading':bool(inspect('Worked answer.','Task heading.','Worked answer.',True)),
      'valid-pupil':not inspect('Task heading. Pupil reasoning.','Task heading.','Worked answer.',False),
      'valid-answer-key':not inspect('Task heading. Worked answer.','Task heading.','Worked answer.',True),
      'planted-duplicate-export':not complete_exports([{'file':'GS_W3A-pupil-task.pdf','includeAnswers':False}]*2,{'GS_W3A'}),
      'planted-mislabelled-answer-key':not complete_exports([{'file':'GS_W3A-pupil-task.pdf','includeAnswers':False},{'file':'GS_W3A-answer-key.pdf','includeAnswers':False}],{'GS_W3A'}),
    }
    result={'schema':'grow-resource-print-content-v1','result':'PASS' if complete and all(controls.values()) and all(not r['problems'] for r in rows) else 'FAIL','completeExportSet':complete,'pdfs':rows,'controls':controls,'scope':'Text extracted from actual Chrome PDFs. The original Science inspector supplies all page images and blank/clipped-page checks; visual page review remains required.'}
    (root/'grow-resource-print-content.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':result['result'],'pdfs':len(rows),'completeExportSet':complete,'failed':[r for r in rows if r['problems']]}))
    return 0 if result['result']=='PASS' else 1

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--artifacts',type=Path,required=True);a=p.parse_args();raise SystemExit(main(a.artifacts))
