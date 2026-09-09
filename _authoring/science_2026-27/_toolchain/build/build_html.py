"""Build standalone Science lessons in Matt's recovered classic chassis."""
from pathlib import Path
from html import escape
import json,re,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from chassis.shell import render_shell
from visuals import render_svg
from interactive_html import panel_html, CSS as LAB_CSS, JS as LAB_JS

def e(x): return escape(str(x),quote=True)
def lines(x): return e(x).replace('\n','<br>')
def para(x,cls=''): return f'<p'+(f' class="{cls}"' if cls else '')+'>'+lines(x)+'</p>'
def route_for(page):
    label=page.get('route','')+' '+page.get('title','')
    for route in ['supported','standard','stretch']:
        if re.search(r'\b'+route+r'\b',label,re.I):return route
    if re.search(r'\bChallenge\b',label,re.I):return 'stretch'
    match=re.search(r'\bRoute\s+([123])\b',label,re.I)
    if match:return {'1':'supported','2':'standard','3':'stretch'}[match.group(1)]
    return 'all'

def table_html(table, uid='table'):
    head=''.join('<th scope="col">'+lines(v)+'</th>' for v in table['headers'])
    rows=''.join('<tr>'+''.join('<td>'+lines(v)+'</td>' for v in row)+'</tr>' for row in table['rows'])
    caption='<caption>'+lines(table['caption'])+'</caption>' if table.get('caption') else ''
    return f'<div class="science-table-wrap" tabindex="0" role="region" aria-label="{e(table.get("caption","Evidence table"))}"><table class="science-table" id="{e(uid)}">{caption}<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'

def visual_html(visual,uid,description=True):
    return '<figure class="science-figure">'+render_svg(visual,uid)+'<figcaption>'+e(visual.get('title','Scientific diagram'))+'</figcaption>'+(f'<details class="diagram-description"><summary>Diagram description</summary>{para(visual.get("description",""))}</details>' if description else '')+'</figure>'

def blocks_html(page,uid,interactive=False):
    out=[]
    for i,b in enumerate(page.get('blocks',[])):
        bid=f'{uid}-b{i}'; typ=b['type']
        if typ=='text':out.append(para(b['text']))
        elif typ=='visual':out.append(visual_html(b['visual'],bid+('-screen' if interactive else '-print'),interactive))
        elif typ=='table':out.append(table_html(b,bid+('-screen' if interactive else '-print')))
        elif typ=='cards':
            out.append('<div class="science-cards">'+''.join(f'<article class="science-card"><h3>{e(c["title"])}</h3>{para(c["text"])}</article>' for c in b['cards'])+'</div>')
        elif typ=='response':
            if interactive:out.append(f'<label class="response-label" for="work-{bid}">{lines(b["prompt"])}</label><textarea id="work-{bid}" data-print-target="paper-{bid}" aria-label="{e(page["title"]+": "+b["prompt"])}" rows="{max(2,b.get("lines",2))}"></textarea>')
            else:out.append('<div class="science-response">'+para(b['prompt'])+f'<div id="paper-{bid}" class="saved-response" hidden></div>'+''.join('<div class="print-line"></div>' for _ in range(max(2,b.get('lines',2))))+'</div>')
        elif typ=='choices':
            if interactive:
                out.append(f'<fieldset class="work-choices"><legend>{lines(b["prompt"])}</legend>'+''.join(f'<label><input type="checkbox" data-note aria-label="{e(page["title"]+": "+str(v))}" data-choice-note data-print-choice-target="paper-{bid}-choice{j}" value="Not selected"> <span>{lines(v)}</span></label>' for j,v in enumerate(b['choices']))+'</fieldset>')
            else:out.append('<div class="science-response">'+para(b['prompt'])+''.join(f'<p><span id="paper-{bid}-choice{j}">☐</span> {lines(v)}</p>' for j,v in enumerate(b['choices']))+'</div>')
        else:raise ValueError('Unknown block type '+typ)
    return ''.join(out)

CSS=r'''
/* Content widgets only. Original Science family tokens and chassis geometry are retained. */
.science-meta{font-size:.82rem;font-weight:800;letter-spacing:.04em;color:var(--muted);margin:0 0 8px}.science-body>p{margin:7px 0}.science-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(340px,1.3fr);gap:24px;align-items:start}.science-layout .science-figure{margin-top:0}.science-layout>*{min-width:0}.science-figure{margin:12px 0;padding:10px;background:#fff;border:1px solid #cbd5e1;border-radius:12px}.science-figure svg{display:block;width:100%;height:auto;max-height:420px}.science-figure figcaption{font-size:.88rem;color:#334155;font-weight:700;margin-top:8px}.diagram-description{font-size:.88rem;margin-top:6px}.diagram-description summary{min-height:44px;cursor:pointer;padding:5px 0}.diagram-description p{font-size:.9rem;line-height:1.45;margin:6px 0}.science-table-wrap{overflow-x:auto;width:100%;margin:12px 0;border-radius:8px;min-width:0}.science-table{width:100%;border-collapse:collapse;background:#fff;font-size:1rem;line-height:1.45}.science-table th,.science-table td{text-align:left;vertical-align:top;padding:10px;border:1px solid #94a3b8}.science-table th{background:var(--scaffold-bg);font-weight:750}.science-table caption{caption-side:top;text-align:left;font-weight:700;padding:6px 0 9px}.science-prompt{font-weight:750;margin:12px 0}.science-quiz{margin:12px 0}.science-options{display:grid;gap:9px}.science-option{display:block;width:100%;text-align:left;background:#fff;color:var(--text);border:2px solid #94a3b8;box-shadow:none;font-size:1.05rem;line-height:1.45;padding:10px 14px}.science-option:hover,.science-option:focus-visible{background:var(--scaffold-bg);color:var(--text);transform:none}.science-option[aria-pressed=true]{border-color:var(--ido-border);background:var(--ido-bg)}.science-feedback{background:#f8fafc;border-left:5px solid var(--scaffold-border);padding:12px;margin:12px 0;font-size:1.05rem;line-height:1.5}.science-feedback[data-result=correct]{border-color:#15803d}.science-feedback[data-result=incorrect]{border-color:#b45309}.science-reveal{margin:12px 0}.science-reveal>div{margin-top:10px}.science-notes label,.response-label{display:block;font-weight:750;margin-top:14px;margin-bottom:8px}.science-notes textarea{min-height:80px}.science-route-buttons{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.science-route-buttons button{background:#fff;color:var(--text);border:2px solid #94a3b8;box-shadow:none}.science-route-buttons button[aria-pressed=true]{background:var(--ido-bg);border-color:var(--ido-border)}.science-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:12px 0}.science-card{border:2px solid #94a3b8;border-radius:10px;padding:12px;background:#fff;break-inside:avoid}.science-card h3{font-size:1.02rem;margin:0 0 6px}.science-card p{font-size:1rem;line-height:1.45;margin:0}.workbook-page{margin:20px 0;border-top:2px solid #cbd5e1;padding-top:16px}.workbook-page>h3{font-size:1.25rem}.workbook-page textarea{width:100%;min-height:90px;padding:10px;font:inherit;line-height:1.5;border:2px solid #94a3b8;border-radius:8px}.work-choices{border:1px solid #94a3b8;margin:14px 0;padding:12px;border-radius:8px}.work-choices legend{font-weight:750}.work-choices label{display:flex;align-items:center;gap:10px;min-height:44px;padding:6px}.work-choices input{width:22px;height:22px;flex-shrink:0}.workbook-footer{display:flex;gap:8px;flex-wrap:wrap}.science-source-list{font-size:.9rem}.science-source-list a{overflow-wrap:anywhere}.stage-guide{font-size:.88rem;color:var(--muted);margin:6px 0}.science-opening-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:24px}.science-opening-grid ul{padding-left:22px}.science-opening-grid h3{margin-top:0}.science-support-list{padding-left:20px}.science-support-list li{font-size:1rem}.science-ta-answers details{margin:12px 0}.science-ta-answers summary{font-weight:700;cursor:pointer}.science-ta-answers p{font-size:.96rem}.print-section .science-meta{font-size:9pt}.print-section .science-figure{border:0;padding:0}.print-section .science-figure svg{max-height:220px}.print-section .science-figure figcaption{font-size:9pt}.print-section .science-card p{font-size:10pt}.saved-response{white-space:pre-wrap;min-height:48px;padding:8px;border:1px solid #94a3b8}.science-response{break-inside:avoid}.science-response>p{margin-bottom:6px}.workbook-page .science-table{font-size:.9rem}
@media screen and (min-width:701px){.slide.science-slide h2{margin-right:0}.slide.science-slide h1{font-size:2.3rem}.science-slide .science-figure:only-child svg{max-height:390px}}
@media screen and (max-width:1100px){.science-layout,.science-opening-grid{grid-template-columns:1fr}.science-layout .science-figure svg{max-height:none}.science-layout{gap:10px}}
@media screen and (max-width:700px){.science-cards{grid-template-columns:1fr}.science-table{font-size:.92rem}.science-table th,.science-table td{padding:8px}.science-slide h2{font-size:1.4rem}.science-figure{padding:5px}.science-figure svg{min-width:560px;max-width:none!important;width:560px;height:auto;max-height:none}.science-figure{overflow-x:auto}.science-figure figcaption,.science-figure details{position:sticky;left:0;max-width:100%}.science-route-buttons button{font-size:.85rem;padding:8px}.science-option{font-size:1rem}}
@page{size:A4;margin:14mm}
@media print{#print-area{padding:0!important}.print-section{padding:0!important}.print-section h1{font-size:20pt}.print-section h2{font-size:17pt}.print-section h3{font-size:12pt}.print-section p{margin:6px 0}.print-section .science-cards{gap:8px}.print-section .science-card{padding:9px}.print-section .science-table{font-size:10pt}.print-section .science-table th,.print-section .science-table td{padding:6px}.print-section .print-line{height:20px;margin-top:6px}.print-section .science-response{margin:9px 0 12px}.print-section .science-figure{margin:8px 0}.print-section .science-meta{margin:0 0 8px}.print-section .diagram-description{display:none}.print-section .science-figure svg{width:100%;height:auto;max-height:210px}.science-table-wrap{overflow:visible}.science-ta-answers{display:none!important}}
'''

JS=r'''
(function(){
'use strict';
document.querySelectorAll('[data-quiz-choice]').forEach(button=>button.addEventListener('click',()=>{
 const quiz=button.closest('.science-quiz');
 quiz.querySelectorAll('[data-quiz-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 const f=quiz.querySelector('[role=status]');
 const correct=button.dataset.correct==='true';
 f.dataset.result=correct?'correct':'incorrect';f.textContent=(correct?'Yes. ':'Think again. ')+button.dataset.feedback;f.hidden=false;
}));
document.querySelectorAll('[data-reveal-target]').forEach(button=>button.addEventListener('click',()=>{
 const target=document.getElementById(button.dataset.revealTarget);const show=target.hidden;
 target.hidden=!show;button.setAttribute('aria-expanded',String(show));button.textContent=show?'Hide explanation':'Reveal explanation';
}));
function setRoute(route){
 document.querySelectorAll('[data-work-route]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.workRoute===route)));
 document.querySelectorAll('.workbook-page').forEach(page=>page.hidden=page.dataset.route!=='all'&&page.dataset.route!==route);
 document.getElementById('workbook-route-label').textContent=route[0].toUpperCase()+route.slice(1)+' route';
 document.querySelector('#workbook-dialog .v4-modal').scrollTop=0;
}
document.querySelectorAll('[data-work-route]').forEach(button=>button.addEventListener('click',()=>setRoute(button.dataset.workRoute)));
document.querySelectorAll('[data-open-workbook]').forEach(button=>button.addEventListener('click',()=>{setRoute(button.dataset.openWorkbook||'standard');window.openModal('workbook-dialog');}));
document.querySelectorAll('[data-save-workbook]').forEach(button=>button.addEventListener('click',()=>window.downloadNotes()));
document.querySelectorAll('[data-choice-note]').forEach(field=>field.addEventListener('change',()=>field.value=field.checked?'Selected':'Not selected'));
window.addEventListener('beforeprint',()=>document.querySelectorAll('[data-print-target]').forEach(field=>{
 const paper=document.getElementById(field.dataset.printTarget);if(!paper)return;paper.textContent=field.value;paper.hidden=!field.value.trim();paper.parentElement.querySelectorAll('.print-line').forEach(line=>line.hidden=Boolean(field.value.trim()));
}));
window.addEventListener('beforeprint',()=>document.querySelectorAll('[data-print-choice-target]').forEach(field=>{const paper=document.getElementById(field.dataset.printChoiceTarget);if(paper)paper.textContent=field.checked?'☑':'☐';}));
setRoute('standard');
}());
'''

def staff_html(d):
    h='<h3>Objective</h3>'+para(d['objective'])+'<h3>Preparation</h3><ul>'+''.join('<li>'+lines(v)+'</li>' for v in d.get('preparation',[]))+'</ul>'
    if d.get('safety'):h+='<h3>Method precautions</h3><ul>'+''.join('<li>'+lines(v)+'</li>' for v in d['safety'])+'</ul>'
    h+='<h3>Practical alternative</h3>'+para(d.get('practicalAlternative',''))
    h+='<h3>Access and regulation</h3>'+''.join(para(k.title()+': '+str(v)) for k,v in d.get('access',{}).items())
    h+='<div class="science-ta-answers"><h3>Teacher answers</h3>'+''.join('<details><summary>'+e(a['label'])+'</summary>'+para(a['answer'])+'</details>' for a in d.get('answers',[]))+'</div>'
    h+='<h3>Sources checked for this lesson</h3><ul class="science-source-list">'+''.join('<li><a href="'+e(s['url'])+'" target="_blank" rel="noopener">'+e(s['title'])+'</a>'+para(s.get('note',''))+'</li>' for s in d.get('sources',[]))+'</ul>'
    return h

def worksheet_dialog(d):
    pages=''.join(f'<section class="workbook-page" data-route="{route_for(p)}"><h3>{e(p["title"])}</h3>{para(p.get("intro",""))}{blocks_html(p,f"p{i}",True)}</section>' for i,p in enumerate(d['pupilPages']))
    return '<dialog id="workbook-dialog" class="classic-dialog" aria-labelledby="workbook-dialog-title"><div class="v4-modal"><h2 id="workbook-dialog-title">My science task sheets</h2>'+para('Choose one route with your teacher. Shared evidence and the exit sheet appear in every route. Your work stays here while the page is open; save it before closing.')+'<div class="science-route-buttons">'+''.join(f'<button type="button" data-work-route="{r}" aria-pressed="{str(r=="standard").lower()}">{r.title()}</button>' for r in ['supported','standard','stretch'])+'</div><p id="workbook-route-label" role="status"></p>'+pages+'<div class="v4-modal-footer workbook-footer"><button type="button" data-save-workbook>Save my work</button><button type="button" data-action="close">Return to lesson</button></div></div></dialog>'

def slide_html(d,s,i):
    st=s['stage'];typ={'I do':'ido','We do':'wedo','You do':'independent'}.get(st,'')
    tag={'Opening':'arrival','Retrieval':'starter','I do':'ido','We do':'wedo','Hinge':'starter','You do':'independent','Review':'lundy','Exit':'starter'}.get(st,'starter')
    attrs=f'class="slide science-slide" id="slide-{i+1}" data-title="{e(s["title"])}" data-timer="{s.get("minutes",0)}" data-type="{typ}" data-teacher="{e(s.get("notes",""))}" data-prompt="{e(s.get("prompt",s["title"]))}"'
    h=f'<section {attrs}><span class="slide-tag tag-{tag}">{e(st)}</span><p class="science-meta">{e(d["pathway"])} · SCIENCE · {e(d["sow"].get("term",""))} · {e(d["sow"].get("week",""))}</p><h2>{e(s["title"])}</h2>'
    if d.get('interactive') and d['interactive'].get('slideIndex')==i:h+=f'<a class="lab-jump" href="#{e(d["id"])}-lab">Go to interactive investigation</a>'
    if st=='Opening':
        h+='<div class="science-opening-grid"><div class="li-box"><h3>Learning intention</h3>'+para(d['objective'])+''.join(para(v) for v in s.get('body',[]))+'</div><div class="sc-box"><h3>Success looks like</h3><ul>'+''.join('<li>'+lines(v)+'</li>' for v in d.get('success',[]))+'</ul></div></div>'
    else:
        body='<div class="science-body '+('ido-box' if st=='I do' else 'task-box' if st=='You do' else '')+'">'+''.join(para(v) for v in s.get('body',[]))+'</div>'
        if s.get('visual'):
            h+='<div class="science-layout">'+body+visual_html(s['visual'],f's{i}-visual')+'</div>'
        else:h+=body
    if st=='Opening' and s.get('visual'):h+=visual_html(s['visual'],f's{i}-visual')
    if s.get('table'):h+=table_html(s['table'],f's{i}-table')
    if s.get('prompt'):h+=para(s['prompt'],'science-prompt')
    if s.get('options'):
        h+=f'<div class="science-quiz" role="group" aria-label="{e(s.get("prompt",s["title"]))}"><div class="science-options">'+''.join(f'<button type="button" class="science-option" data-quiz-choice="{j}" data-correct="{str(o["correct"]).lower()}" data-feedback="{e(o["feedback"])}" aria-pressed="false">{chr(65+j)}. {lines(o["text"])}</button>' for j,o in enumerate(s['options']))+'</div><div class="science-feedback" role="status" aria-live="polite" hidden></div></div>'
    if s.get('reveal'):
        h+=f'<div class="science-reveal"><button type="button" data-reveal-target="reveal-{i}" aria-controls="reveal-{i}" aria-expanded="false">Reveal explanation</button><div id="reveal-{i}" class="scaffold-box" hidden>{para(s["reveal"])}</div></div>'
    if st in ['We do','You do','Review','Exit'] and not s.get('options'):
        prompt=s.get('prompt','My scientific thinking')
        h+=f'<div class="science-notes"><label for="note-{i}">My response — say it, sketch on paper or type</label><textarea id="note-{i}" aria-label="{e(prompt)}" rows="2"></textarea></div>'
    if st=='You do':
        h+='<div class="science-route-buttons">'+''.join(f'<button type="button" data-open-workbook="{r}">Open {r} tasks</button>' for r in ['supported','standard','stretch'])+'</div>'
    if d.get('interactive') and d['interactive'].get('slideIndex')==i:h+=panel_html(d['interactive'],d['id']+'-lab')
    if s.get('minutes',0)==0:h+='<p class="stage-guide">Continue within this stage’s shared time.</p>'
    return h+'</section>'

def menu_html(d):
    files=[('Lesson.html','Open interactive lesson and science investigation','HTML'),('Lesson.pptx','Editable teaching slides','PPTX'),('Slides.pdf','Teaching slides to view or print','PDF'),('Pupil.docx','Editable pupil booklet and cards','DOCX'),('Pupil.pdf','Printable pupil booklet and cards','PDF'),('Teacher.docx','Editable teacher plan and answers','DOCX'),('Teacher.pdf','Teacher plan and answers','PDF')]
    links=''.join(f'<a href="{name}"><span>{e(label)}</span><strong>{fmt}</strong></a>' for name,label,fmt in files)
    return '<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(d['title'])+' — Start here</title><style>body{font-family:Segoe UI,Arial,sans-serif;background:#f8fafc;color:#1f2937;margin:0;padding:24px;line-height:1.6}main{max-width:780px;margin:auto;background:#fff;padding:28px;border-top:8px solid '+{'BUILD':'#4E7A9B','GROW':'#3F7D6E','LAUNCH':'#7A5C9E'}[d['pathway']]+';border-radius:14px}h1{font-size:2rem;line-height:1.2}a{display:flex;justify-content:space-between;align-items:center;gap:14px;min-height:44px;margin:12px 0;padding:14px;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:9px;text-decoration:none;color:#153b5a}a:hover{background:#e0f2fe}a:focus-visible{outline:3px solid #c9803b;outline-offset:3px}strong{font-size:.85rem}li{margin:6px 0}small{display:block;color:#475569} @media(max-width:600px){body{padding:10px}main{padding:20px}h1{font-size:1.7rem}}</style></head><body><main><p><b>'+e(d['pathway'])+' · SCIENCE · 40 MINUTES</b></p><h1>'+e(d['title'])+'</h1>'+para(d.get('subtitle',''))+'<h2>Learning intention</h2>'+para(d['objective'])+links+'<h2>Choose a pupil route</h2>'+para('Print the shared evidence and exit sheet, plus one of Supported, Standard or Stretch. These are selectable levels of support for the same lesson, not three sets to finish.')+'<h2>Using the HTML lesson</h2><ul><li>Extract the ZIP before opening START_HERE.html. Keep each lesson folder together.</li><li>Previous and Next move through the lesson. Arrow keys work when you are not typing or using a control.</li><li>TA Brief holds the current teaching script and teacher answers. Word help gives the vocabulary.</li><li>The timer starts only when you choose. Pause provides a quiet return point; pupils may pass in Cold Call.</li><li>In We do, choose a prediction and test it against the evidence. Selected lessons also let you replay dated growth records, compare stopping distances, choose a separation method or step through blood-glucose regulation. Pause model stops its motion and controls; Reset investigation clears its decisions.</li><li>Open the task sheets during You do. Save my work downloads typed responses; they are not retained after reload.</li><li>Tools &amp; print selects a pupil print route. The HTML lesson and resources work offline; source links need internet access.</li></ul><h2>Scheme of work</h2>'+para(d['sow'].get('alignment',''))+'<small>'+e(d['sow'].get('workbook',''))+' · '+e(d['sow'].get('sheet',''))+' · '+e(d['sow'].get('cells',''))+'</small></main></body></html>'

def build_one(d):
    dest=ROOT/'output'/d['id'];dest.mkdir(parents=True,exist_ok=True)
    slides=''.join(slide_html(d,s,i) for i,s in enumerate(d['slides']))+worksheet_dialog(d)
    prints=''.join(f'<section class="print-section" id="print-page-{i}" data-print-route="{route_for(p)}"><p class="science-meta">{e(d["pathway"])} SCIENCE · {e(d["title"])}</p><h2>{e(p["title"])}</h2>{para(p.get("intro",""))}{blocks_html(p,f"p{i}",False)}</section>' for i,p in enumerate(d['pupilPages']))
    shell_data={**d,'subject':'Science','staff':staff_html(d),'extra_css':CSS+LAB_CSS,'menu_href':'START_HERE.html'}
    (dest/'Lesson.html').write_text(render_shell(shell_data,slides,prints,JS+LAB_JS),encoding='utf-8')
    (dest/'START_HERE.html').write_text(menu_html(d),encoding='utf-8')
    qa=ROOT/'qa'/'html';qa.mkdir(parents=True,exist_ok=True)
    source=ROOT/'content'/(d['id']+'.json')
    renderer_files=[Path(__file__),ROOT/'build'/'interactive_html.py',ROOT/'build'/'interactive_models.py',ROOT/'build'/'visuals.py',ROOT/'chassis'/'shell.py',ROOT/'chassis'/'controls.js',ROOT/'chassis'/'controls.css',ROOT/'chassis'/'access.css',ROOT/'chassis'/'styles'/(d['pathway'].lower()+'_science.css')]
    manifest={'id':d['id'],'slides':len(d['slides']),'quizzes':sum(bool(s.get('options')) for s in d['slides']),'bytes':(dest/'Lesson.html').stat().st_size,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'htmlSha256':hashlib.sha256((dest/'Lesson.html').read_bytes()).hexdigest(),'rendererSha256':hashlib.sha256(b''.join(p.read_bytes() for p in renderer_files)).hexdigest(),'interactiveDecisions':len(d.get('interactive',{}).get('steps',[])),'model':d.get('interactive',{}).get('mode')}
    (qa/(d['id']+'_build.json')).write_text(json.dumps(manifest,indent=2))
    return manifest

if __name__=='__main__':
    paths=[Path(x) for x in sys.argv[1:]] if len(sys.argv)>1 else sorted((ROOT/'content').glob('*.json'))
    print(json.dumps([build_one(json.loads(p.read_text())) for p in paths],indent=2))
