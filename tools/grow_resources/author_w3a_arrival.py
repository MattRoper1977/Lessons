"""Bounded EDU-Q1 arrival authoring from the pinned keyboard draft.
Native PDFs are rendered from the two DOCX outputs, not authored separately.
Do not run over later unrelated lesson edits: this script binds its input head.
"""
from pathlib import Path
import argparse,json,subprocess,io,html
from docx import Document
from docx.shared import Pt
BASE='74929d1b1eadf66f4caaa4f98e1ec65cd009c112'
REL='Science_Teesside/Grow/SCI_G_W3_Friction.html'
PACK='Science_Teesside/Teaching_Packs/GROW/lessons/W3A/'
HERE=Path(__file__).resolve().parent

def main(root):
 data=json.loads((HERE/'W3A_ARRIVAL.json').read_text());esc=html.escape
 def baseline(rel):return subprocess.check_output(['git','-C',str(root),'show',BASE+':'+rel])
 src=baseline(REL).decode()
 def cards(route,answers=False):
  key='answers' if answers else 'questions'
  return ''.join(f'<div class="task-box"><h3>{i+1}. {esc(q)}</h3></div>' for i,q in enumerate(route[key]))
 controls=''.join(f'<button type="button" class="ghost small" data-arrival-route="{k}" aria-pressed="{str(k=="supported").lower()}" onclick="setArrivalLevel(\'{k}\')">{r["label"]}</button>' for k,r in data['routes'].items())
 screen='<div class="slide" data-title="Arrival Task" data-timer="4" id="arrival-slide"><span class="slide-tag tag-arrival">Arrival · four quick questions</span><h2>Arrival task — pick your tier</h2>'
 screen+=f'<p class="grow-arrival-response">{esc(data["response"])}</p><p class="grow-arrival-access">{esc(data["access"])}</p><div class="level-toggle" role="group" aria-label="Arrival route">{controls}</div>'
 for k,r in data['routes'].items():
  display='' if k=='supported' else ' style="display:none"'
  screen+=f'<div id="arrival-{k}" class="arrival-grid"{display}>{cards(r)}<div class="grow-arrival-actions"><button type="button" class="ghost small" onclick="printArrival(\'{k}\',false)">Print {r["label"]} arrival</button><details class="grow-arrival-answers"><summary>Show {r["label"]} arrival answers</summary><p>{esc(data["staff"])}</p><ol>'+''.join('<li>'+esc(a)+'</li>' for a in r['answers'])+f'</ol><button type="button" class="ghost small" onclick="printArrival(\'{k}\',true)">Print {r["label"]} staff answers</button></details></div></div>'
 screen+='</div>'
 start=src.index('<div class="slide" data-title="Arrival Task"');end=src.index('<div class="slide" data-title="Today at a Glance"',start)
 src=src[:start]+screen+src[end:]
 def print_section(answers=False):
  sid='print-arrival-answers' if answers else 'print-arrival'
  result=f'<div id="{sid}" class="print-section grow-arrival-print"><h2>Friction arrival'+(' — staff answers' if answers else '')+'</h2>'
  result+='<p>'+esc(data['staff'] if answers else data['response'])+'</p><p>'+esc(data['access'])+'</p>'
  for k,r in data['routes'].items():
   result+=f'<div class="{k}-content"><h3>{r["label"]}</h3><div class="grow-arrival-paper-grid">'
   for i,q in enumerate(r['questions']):
    result+='<div class="grow-arrival-paper-card"><p><strong>'+str(i+1)+'. '+esc(q)+'</strong></p>'
    result+=('<p>'+esc(r['answers'][i])+'</p>' if answers else '<div class="grow-arrival-space" aria-hidden="true"></div>')+'</div>'
   result+='</div></div>'
  return result+'</div>'
 start=src.index('<div id="print-arrival"');end=src.index('<div id="print-wedo"',start)
 src=src[:start]+print_section()+print_section(True)+src[end:]
 css='''<style id="grow-w3a-arrival-css">
#arrival-slide .task-box{padding:14px;min-width:0}
#arrival-slide .task-box h3{font-size:1rem;line-height:1.4;margin:0;color:var(--text,#172b34)}
#arrival-slide .grow-arrival-response,#arrival-slide .grow-arrival-access{font-size:.95rem;line-height:1.4}
#arrival-slide .grow-arrival-actions{grid-column:1/-1}
#arrival-slide .grow-arrival-answers{margin-top:12px}
#arrival-slide summary{cursor:pointer;padding:12px 4px;font-weight:700}
#arrival-slide summary:focus-visible{outline:3px solid var(--ido-border);outline-offset:2px}
#arrival-slide [aria-pressed="true"]{outline:2px solid currentColor;outline-offset:2px;font-weight:800}
@media print{.grow-arrival-paper-grid{display:grid;grid-template-columns:1fr 1fr;gap:10mm}.grow-arrival-paper-card{break-inside:avoid;border:1px solid #888;padding:4mm;min-width:0}.grow-arrival-space{height:35mm}.grow-arrival-print{font-size:11pt;line-height:1.4}.grow-arrival-print h2{font-size:18pt}.grow-arrival-print h3{font-size:14pt}}
</style>'''
 src=src.replace('</head>',css+'</head>')
 js='''function setArrivalLevel(level){
  switchLevel('arrival',level);
  document.querySelectorAll('[data-arrival-route]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.arrivalRoute===level)));
  document.querySelectorAll('.grow-arrival-answers').forEach(d=>d.open=false);
}
function printArrival(level,answers){
  if(!['supported','standard','stretch'].includes(level))return;
  document.body.classList.remove('print-supported','print-standard','print-stretch');
  document.body.classList.add('print-'+level);
  document.querySelectorAll('.print-section').forEach(s=>s.classList.remove('visible'));
  document.getElementById(answers?'print-arrival-answers':'print-arrival').classList.add('visible');
  window.print();
}
'''
 src=src.replace('function switchLevel(prefix,level)',js+'function switchLevel(prefix,level)')
 (root/REL).write_text(src)
 for audience in ['Pupil','Teacher']:
  rel=PACK+f'GROW_W3A_Friction_{audience}.docx';doc=Document(io.BytesIO(baseline(rel)))
  if audience=='Pupil':
   doc.paragraphs[7].text='Choose your four-question arrival page: Supported 7, Standard 8 or Stretch 9. Use screen or paper; you do not need to do both.'
  else:
   doc.paragraphs[9].text='Each pupil: common pages 1–2, one response page (3 Supported, 4 Standard or 5 Stretch), and one arrival page (7 Supported, 8 Standard or 9 Stretch). Page 6 has reusable cards. Use screen or paper for arrival; do not require both.'
   doc.paragraphs[28].text='Use the four-question arrival answers on pages 6–8. Accept equivalent responses and uncertainty. Hand rubbing is optional; a remembered example or prediction is not an observation made today.'
  for k,r in data['routes'].items():
   p=doc.add_paragraph('ARRIVAL / '+r['label'].upper()+(' / STAFF ANSWERS' if audience=='Teacher' else ''),'Kicker');p.paragraph_format.page_break_before=True
   doc.add_paragraph('Friction arrival','Title')
   doc.add_paragraph(r['label']+' · Four minutes within Lesson A')
   doc.add_paragraph(data['staff'] if audience=='Teacher' else data['response'])
   doc.add_paragraph(data['access'])
   table=doc.add_table(rows=2,cols=2);table.autofit=False
   from docx.oxml import OxmlElement
   from docx.oxml.ns import qn
   from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
   for i,q in enumerate(r['questions']):
    cell=table.cell(i//2,i%2);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
    cell.width=doc.sections[0].page_width//2-doc.sections[0].left_margin
    p=cell.paragraphs[0];p.add_run(str(i+1)+'. '+q).bold=True
    p.paragraph_format.space_after=Pt(10)
    if audience=='Teacher':cell.add_paragraph(r['answers'][i])
    else:
     p=cell.add_paragraph(' ');p.paragraph_format.space_after=Pt(65)
    pr=cell._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
    for edge in ['top','left','bottom','right']:
     el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'5');el.set(qn('w:color'),'D9D9D9');borders.append(el)
    pr.append(borders);margins=OxmlElement('w:tcMar')
    for edge in ['top','left','bottom','right']:
     el=OxmlElement('w:'+edge);el.set(qn('w:w'),'120');el.set(qn('w:type'),'dxa');margins.append(el)
    pr.append(margins)
   doc.add_paragraph('Choose one response route. An adult can read or scribe your words.' if audience=='Pupil' else 'Use the response to choose an explanation or scaffold. No automatic assessment outcome or extra pupil record.')
  doc.save(root/rel)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=HERE.parents[1]);a=ap.parse_args();main(a.root.resolve())
