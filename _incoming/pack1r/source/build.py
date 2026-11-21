#!/usr/bin/env python3
"""Deterministic P1 HTML build; every output stays inside this intake."""
import csv, hashlib, html, json, re, sys
from pathlib import Path
from lxml import html as LH
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parents[1]
sys.path.insert(0,str(REPO/'tools/hum'))
from deck_dom import parse, stages
from loop_adapter import stage_task
from content import DATA, ROUTES, STAGES, TIMERS, CAVEAT, ACCESS, SPACE, CAPTURE, CODES
E=html.escape
EXEMPLARS={
 'BUILD':'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html',
 'GROW':'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html',
 'LAUNCH':'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html'}
DATE='2026-09-21'
def put(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data,encoding='utf-8')
def palette(p):
 doc=LH.fromstring((REPO/EXEMPLARS[p]).read_text());props={}
 for s in doc.xpath('//style'):
  for k,v in re.findall(r'(--[\w-]+)\s*:\s*([^;}]+)',s.text or ''):props[k]=v.strip()
 return ':root{'+''.join(k+':'+v+';' for k,v in props.items())+'}'
def btn(text,action,extra=''):
 return f'<button type="button" data-sx3-shell="1" data-action="{action}" {extra}>{text}</button>'
def printbtn(id,text,selector,answers=False):
 return f'<button type="button" id="{id}" data-print="{selector}" data-answers="{str(answers).lower()}">{text}</button>'
def routebar():
 return '<div class="route-controls" data-route-group>'+''.join(f'<button type="button" data-route="{r}" aria-pressed="{str(i==0).lower()}">{r.title()}</button>' for i,r in enumerate(ROUTES))+'</div>'
def local_map():
 return '''<figure class="figure"><svg viewBox="0 0 680 320" role="img" aria-label="Fictional plan: park above school; library right of school. Dashed route leads right from school to library."><rect x="1" y="1" width="678" height="318" fill="#f7faf7" stroke="#5c7180"/><path d="M105 95 L145 30 L185 95 Z" fill="#d3e9d8" stroke="#2d5b3a" stroke-width="3"/><text x="145" y="84" text-anchor="middle" font-size="25" fill="#143e22">P</text><text x="210" y="75" font-size="25">Park</text><rect x="110" y="180" width="70" height="65" fill="#dbe8f2" stroke="#2d5270" stroke-width="3"/><text x="145" y="222" text-anchor="middle" font-size="28">S</text><text x="145" y="279" text-anchor="middle" font-size="23">School</text><circle cx="490" cy="213" r="36" fill="#f5e1c9" stroke="#76542d" stroke-width="3"/><text x="490" y="222" text-anchor="middle" font-size="28">L</text><text x="490" y="279" text-anchor="middle" font-size="23">Library</text><path d="M185 213 H444" stroke="#355169" stroke-width="5" stroke-dasharray="10 8"/><path d="M428 199 L447 213 L428 227" fill="none" stroke="#355169" stroke-width="5"/><text x="580" y="50" font-size="21">Top</text><path d="M603 95 V60 M592 74 L603 59 L614 74" stroke="#355169" stroke-width="3" fill="none"/></svg><figcaption>Original teaching plan, not a real street map. Key: square S = school; triangle P = park; circle L = library. No scale. Left and right mean across this fixed page.</figcaption></figure>'''
LAND=json.loads((HERE/'ne_110m_land.geojson').read_text())
def geo_map(kind):
 bounds=(-180,-60,180,85) if kind=='world' else (-11,49,5,61)
 x0,y0,x1,y1=bounds;w,h=720,340
 def xy(lon,lat):return ((lon-x0)/(x1-x0)*w,(y1-lat)/(y1-y0)*h)
 paths=[]
 for f in LAND['features']:
  g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
  for poly in polys:
   ring=poly[0]
   if max(a[0] for a in ring)<x0 or min(a[0] for a in ring)>x1 or max(a[1] for a in ring)<y0 or min(a[1] for a in ring)>y1:continue
   coords=[xy(*a[:2]) for a in ring]
   paths.append('<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in coords)+' Z"/>')
 label='UK' if kind=='world' else 'Middlesbrough'
 lon,lat=(-2.2,54.5) if kind=='world' else (-1.235,54.576)
 x,y=xy(lon,lat)
 text=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#8b173c"/><path d="M{x+7:.1f} {y:.1f} l25 -18" stroke="#8b173c" stroke-width="2"/><text x="{x+33:.1f}" y="{y-18:.1f}" font-size="22" fill="#701330">{label}</text>'
 if kind=='world':text+='<text x="410" y="104" font-size="22" fill="#173149">Europe</text><text x="239" y="220" font-size="20" fill="#173149">Atlantic Ocean</text>'
 else:text+='<text x="405" y="249" font-size="22" fill="#173149">England</text><text x="280" y="118" font-size="22" fill="#173149">Scotland</text><text x="302" y="270" font-size="21" fill="#173149">Wales</text><text x="116" y="178" font-size="18" fill="#173149">Northern Ireland</text>'
 return f'<figure class="figure"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)} marked on a {kind} coastline map; north is up."><rect width="{w}" height="{h}" fill="#e8f2f9"/><g fill="#dfe6d8" stroke="#596e57" stroke-width="1">'+''.join(paths)+f'</g>{text}<text x="660" y="30" font-size="22">N ↑</text></svg><figcaption>Natural Earth public-domain land outlines. Simplified equirectangular view; north up. Marker = {label}. Country boundaries and small islands are omitted. This is a location aid, not a navigation map.</figcaption></figure>'
def map_explorer(key):
 return f'<div data-map-scope><div class="map-controls"><button type="button" data-map-view="uk" aria-pressed="true">UK view</button><button type="button" data-map-view="world" aria-pressed="false">World view</button></div><div data-map-panel="uk">{geo_map("uk")}</div><div data-map-panel="world" hidden>{geo_map("world")}</div></div>'
def emissions():
 return '<figure class="figure chart"><h3>Net UK territorial greenhouse gas emissions</h3><p>Rounded headline values · MtCO₂e · zero-based bars</p>'+''.join(f'<div class="chart-row"><strong>{yr}</strong><div><div class="bar" style="width:{v/790*100:.3f}%" aria-hidden="true"></div></div><span>{v}</span></div>' for yr,v in [(1990,790),(2023,384),(2024,373)])+'<figcaption>DESNZ statistical release, 5 February 2026, pp. 1 and 6. 1990 is reconstructed from rounded headline figures (373 + 417). Years are selected, not evenly spaced. Bars compare totals; they are not a continuous time axis.</figcaption></figure>'
def visual(p):return local_map() if p=='BUILD' else map_explorer('view') if p=='GROW' else emissions()
def source_block(d):
 return '<div class="sources"><h3>Sources and image credits</h3>'+''.join(f'<p><strong>{E(s[0])}</strong><br><span class="source-url">{E(s[1])}</span><br>{E(s[2])}</p>' for s in d['sources'])+'<p>Source checks: 20 September 2026. Source addresses are printed for provenance; no external resources are fetched by the lesson, except the required BUILD HUD.</p></div>'
def organiser(p,d):
 return f'<div class="ko-content"><p class="eyebrow">{p} · Humanities · Sum1·W1</p><h2>{E(d["title"])}</h2><p><strong>Objective:</strong> {E(d["objective"])}</p><div class="ko-words">'+''.join(f'<p><strong>{E(w)}</strong>{E(v)}</p>' for w,v,t in d['words'])+'</div>'+ (local_map() if p=='BUILD' else geo_map('world') if p=='GROW' else emissions())+f'<p><strong>Remember:</strong> {E(d["misconception"])}</p><p><strong>Show learning:</strong> {E(d["success"][1])}</p><p><strong>World of work:</strong> {E(d["career"])}</p></div>'
def staff(p,d):
 return '<div class="ta-card teacher-only" data-hum-t="1" data-mbm-guide="staff"><h3>TA brief · staff only</h3><p>'+E(d['prep'])+'</p><h3>Space · exact Feedback Policy quotations</h3><p>Body §5, PDF page 8; last quotation: body §14, PDF page 14. No public comparison is the policy condition.</p>'+''.join('<blockquote>'+E(q)+'</blockquote>' for q in SPACE)+'<h3>Feedback codes · body §11</h3><dl>'+''.join(f'<dt><strong>{E(c)}</strong></dt><dd>{E(v)}</dd>' for c,v in CODES)+'</dl><h3>Exit: EFL capture · body §14</h3><p>'+E(CAPTURE)+'</p><p>Capture this pupil’s location explanation or evidence-based claim, response to feedback and the next step. R follows the pupil’s response and the adult’s genuine reception; do not award it for a click alone.</p><h3>Check and respond</h3><p>'+E(d['misconception'])+'</p><p>'+E(d['evidence'])+'</p><p>'+E(CAVEAT)+'</p></div>'
def arrival(d):
 s='<div data-route-scope>'+f'<p>{ACCESS}</p>'+routebar()
 for i,r in enumerate(ROUTES):
  s+=f'<div data-route-panel="{r}"'+(' hidden' if i else '')+'>'+f'<div class="arrival-four" id="arrival-panel-{r}">'
  for j,(heading,q,h,a) in enumerate(d['arrival'][r]):
   s+=f'<article class="arrival-cell" style="--arrival-order:{j}"><h3>{j+1}. {E(heading)}</h3><p>{E(q)}</p><p class="arrival-hint">Help: {E(h)}</p><p class="arrival-answer" data-arrival-answer hidden><strong>Answer:</strong> {E(a)}</p></article>'
  s+='</div><div class="toolbar">'+f'<button type="button" data-reveal="#arrival-panel-{r} .arrival-answer" aria-expanded="false">Reveal answers</button>'+printbtn('print-arrival-'+r,'Print questions','#arrival-panel-'+r)+printbtn('print-arrival-answers-'+r,'Print staff answers','#arrival-panel-'+r,True)+'</div></div>'
 return s+'</div>'
def check(d,i):
 c=d['checks'][i]
 return f'<fieldset data-check data-answer="{c["answer"]}" data-feedback="{E(c["feedback"])}"><legend>{E(c["question"])}</legend><div class="choices">'+''.join(f'<button type="button" data-option="{j}" aria-pressed="false">{E(t)}</button>' for j,t in enumerate(c['options']))+'</div><p data-check-result class="answer-result" role="status">Choose, then explain your evidence.</p></fieldset>'
def independent(d):
 return f'<div data-route-scope><p>{ACCESS}</p>'+routebar()+''.join(f'<div data-route-panel="{r}"'+(' hidden' if i else '')+f'><h3>{r.title()} task</h3><p>{E(d["independent"][i])}</p><p class="help">Before recording: rehearse your idea aloud, sign, point or direct an adult. Check the key words and success criteria.</p></div>' for i,r in enumerate(ROUTES))+'<label for="response">My response (optional; clears on reload)</label><textarea class="write-space" id="response"></textarea></div>'
def exit_content(d):
 return '<div data-route-scope>'+routebar()+''.join(f'<div id="exit-{r}" data-route-panel="{r}"'+(' hidden' if i else '')+f'><h3>{r.title()} exit</h3><p>{E(q)}</p><p class="staff-answer" hidden>{E(a)}</p><p>Respond independently in your chosen mode; an adult may scribe your exact words.</p>'+printbtn('print-exit-'+r,'Print exit ticket','#exit-'+r)+'</div>' for i,(r,(q,a)) in enumerate(zip(ROUTES,d['exit'])))+'</div>'
def panel(p,i,task,d):
 modes={'BUILD':'Point, sign, say, draw, demonstrate or direct an adult using the map.','GROW':'Point to a map, give a verbal reply, make a short edit or direct an adult.','LAUNCH':'Give a structured verbal response, annotate the source, make an in-lesson edit or direct an adult.'}[p]
 next_=d['next'][i]
 return f'<div class="lundy hum-t-loop" data-hum-t="1" data-loop-stage="{i}" data-loop-stage-name="{STAGES[i]}" data-loop-key="{p}-{i}" aria-label="Feedback participation"><h3>Space · Voice · Audience · Influence</h3><p>Space: take time with a trusted adult. You may pause or choose another response mode.</p><div class="lundy-grid">'+''.join(f'<div class="ls" data-lundy-step="{x}" data-state="{("available" if x=="space" else "waiting")}">{x.upper()}</div>' for x in ['space','voice','audience','influence'])+f'</div><p data-loop-part="response"><strong>Voice:</strong> {E(task)} <span class="loop-modes">{E(modes)}</span></p><p data-loop-part="audience"><strong>Audience:</strong> Adult, receive the response and read it back exactly; check you understood before changing anything.</p><p data-loop-part="influence"><strong>Influence:</strong> {E(next_)} Agree the change with the pupil.</p><label class="loop-next-label" for="next-{p}-{i}">What will change next?</label><select id="next-{p}-{i}" data-loop-next><option>Use the model again. {E(next_)}</option><option>Reduce the prompt. {E(next_)}</option><option>Explain a reason. {E(next_)}</option></select><div class="loop-controls"><button type="button" data-action="lundy-voice">Voice: I have responded</button><button type="button" data-action="lundy-audience">Audience: adult received it</button><button type="button" data-action="lundy-influence">Influence: agree next step</button></div><p class="loop-status" data-loop-result role="status" aria-live="polite">Respond in your chosen way; the adult then listens or looks.</p></div>'
def dialog(id,title,body):
 return f'<dialog id="{id}" aria-labelledby="{id}-heading"><div class="dialog-head"><h2 id="{id}-heading">{title}</h2>'+btn('Close','close')+f'</div><div class="dialog-body">{body}</div></dialog>'
def lesson(p,d):
 title=E(d['title']);blocks=[];before=[]
 for i,label in enumerate(STAGES):
  typ=['title','arrival','starter','ido','wedo','ido2','wedo2','independent','exit'][i]
  head=(f'<p class="eyebrow">{p} · Humanities · Sum1·W1</p><h1>{title}</h1><p class="objective"><strong>Objective:</strong> {E(d["objective"])}</p>' if i==0 else f'<p class="eyebrow">{p} · Sum1·W1 · {TIMERS[i]} minutes</p><h2>{label}</h2>')
  body=f'<p class="instruction">{E(d["tasks"][i])}</p>'
  if i==0:body+='<div class="success"><h2>Today I can</h2><ul>'+''.join('<li>'+E(x)+'</li>' for x in d['success'])+'</ul></div>'+btn('Knowledge organiser','organiser')+f'<p class="career">{E(d["career"])}</p><p class="small">{E(d["evidence"])}</p><details><summary>Accreditation evidence</summary><p>{E(CAVEAT)}</p></details>'
  if i==1:body+=arrival(d)
  if i==2:body+=visual(p)+f'<p class="help">Pre-teach: {E(d["words"][0][0])} means {E(d["words"][0][1])}. {E(d["words"][2][0])} means {E(d["words"][2][1])}. Use Word help before you respond.</p>'
  if i in (3,5):
   m=0 if i==3 else 1
   body+=visual(p)+f'<button type="button" class="{("science-reveal" if p=="GROW" else "model-reveal")}" data-model="model-{i}" aria-expanded="false">Show worked explanation</button><div class="model" id="model-{i}" data-model-answer hidden><h3>Teacher think-aloud</h3><p>{E(d["models"][m])}</p></div><p>Listen and track the evidence. The next stage is your turn to try.</p>'
  if i in (4,6):body+=visual(p)+check(d,0 if i==4 else 1)+f'<details><summary>Help with this task</summary><p>{E(d["misconception"])}</p></details>'
  if i==7:body+=independent(d)
  if i==8:body+=exit_content(d)+(btn('Finish lesson','finish') if p=='BUILD' else '<p>You have reached the end of this lesson. Agree one next step with the adult.</p>')
  print_id=f'print-task-{i}' if (i in ([2,4,7] if p=='BUILD' else [2,3,4,5,6,7])) else f'print-stage-{i}'
  body+=printbtn(print_id,'Print this stage',f'#stage-content-{i}')
  start=f'<section class="slide" id="slide-{i+1}" data-title="{label}" data-type="{typ}" data-timer="{TIMERS[i]}"'+(' hidden' if i else '')+'>'
  raw=start+f'<div id="stage-content-{i}">{head}{body}</div></section>'
  before.append(raw)
  task=stage_task(stages(parse(raw))[0])
  blocks.append(raw[:-10]+(panel(p,i,task,d) if i not in (3,5) else '')+'</section>')
 ko=organiser(p,d);ta=staff(p,d)
 words='<p>Read, explain, use. Rehearse these words before the source or map task.</p><dl>'+''.join(f'<dt><strong>{E(w)} · {t}</strong></dt><dd>{E(v)}</dd>' for w,v,t in d['words'])+'</dl>'+btn('Go to Starter','goto','data-goto="2"')
 toolsbody='<div class="toolbar">'+btn('Knowledge organiser','organiser')+btn('TA layer · staff','ta')+btn('Volunteer picker','picker')+printbtn('print-organiser','Print A4 organiser','.ko-content')+printbtn('print-shared','Print shared evidence','#stage-content-4')+printbtn('print-answers','Print teacher answers','#teacher-answers',True)+'</div><p>Use a specific print button to print questions, answers, the organiser or this stage.</p>'
 answers='<div id="teacher-answers" class="teacher-only"><h3>Teacher answers</h3>'+''.join(f'<p><strong>{r.title()} arrival</strong></p><ol>'+''.join('<li>'+E(x[3])+'</li>' for x in d['arrival'][r])+'</ol>' for r in ROUTES)+''.join(f'<p><strong>{r.title()} exit:</strong> {E(a)}</p>' for r,(q,a) in zip(ROUTES,d['exit']))+'</div>'
 if p!='BUILD':answers='<div id="all-answers">'+answers+'</div>'
 tabody=ta+answers+printbtn('print-staff','Print teaching notes','.ta-card',True)
 if p!='BUILD':tabody+='<div class="staff-card teacher-only"><p>Staff guide preference stays on this device; pupil responses do not.</p><button type="button" id="guide-toggle" aria-pressed="false">Toggle staff guide preference</button><p id="guide-status" role="status">Preference off.</p></div>'
 dialogs=dialog('word-dialog','Word help',words)+dialog('pause-dialog','Pause and reset','<p>Pause the task. Find a comfortable position, ask for a trusted adult, or use your agreed regulation support. You may return when ready.</p>'+btn('Return to Arrival','goto','data-goto="1"'))+dialog('tools-dialog','Tools and print',toolsbody)+dialog('organiser-dialog','Knowledge organiser',ko)+dialog('ta-dialog','TA layer · staff only',tabody)+dialog('cold-call-dialog','Volunteer picker','<p>Invite volunteers; anyone may pass. Initials only. Nothing is saved.</p><label for="volunteers">Volunteer initials, one per line</label><textarea id="volunteers" class="write-space"></textarea><div class="toolbar"><button type="button" id="pick-volunteer">Invite a volunteer</button><button type="button" id="clear-volunteers">Clear initials</button></div><p id="picker-result" role="status">Ask for volunteers first.</p>')
 backlink='<a href="../../index.html?subject=Humanities&amp;pathway=BUILD" aria-label="Back to the Lessons catalogue">← Lessons</a>' if p=='BUILD' else '<a class="way-home" href="./START_HERE.html">← Lessons</a>'
 outer='' if p=='BUILD' else '<a class="skip" href="#lessonDeck">Skip to lesson</a><a class="mbmhome" href="../../index.html">← Lessons</a>'
 nav=f'<nav class="{("classic-toolbar" if p=="BUILD" else "review-top")}" aria-label="Lesson tools">{backlink}'+btn('Word help','words')+btn('Pause','pause')+btn('Tools & print','tools')+btn('TA layer','ta')+'<div class="timer" id="auto-timer"><button type="button" id="auto-timer-toggle" aria-pressed="false">Start timer</button> <output id="auto-timer-display" aria-label="Stage time remaining">00:00</output><span class="screen-reader" id="timer-status" role="status"></span></div></nav>'
 xp='<div id="xpWrap" aria-label="Stages visited">Stage <span id="xpCount">1</span> / <span id="xpTotal">9</span><div id="xpFill"></div></div><div id="lc-overlay" hidden role="dialog" aria-modal="false" aria-label="Lesson complete"><h2>Lesson complete</h2><p>Show the adult your exit response and agree your next step.</p>'+btn('Return to Exit','close-complete','id="close-complete"')+'</div>' if p=='BUILD' else ''
 progress='<div class="progress"><label for="progressBar" id="progressLabel">1 / 9 · Title</label><progress id="progressBar" value="1" max="9"></progress><p id="classic-status"></p><p id="classic-progress"></p></div>'
 navigation='<footer class="navigation" aria-label="Lesson stages"><button type="button" id="previous-slide">Previous</button><label for="slide-picker" class="screen-reader">Choose a stage</label><select id="slide-picker">'+''.join(f'<option value="{i}">{i+1}. {s}</option>' for i,s in enumerate(STAGES))+'</select><button type="button" id="next-slide">Next</button></footer>'
 js=(HERE/'lesson.js').read_text()
 if p=='BUILD':js=re.sub(r" if\(config.pathway!=='BUILD'\).*?\n go",'\n go',js,flags=re.S)
 css=(HERE/'lesson.css').read_text()
 if p=='GROW':css=css.replace('--zone-count:2;','')
 page=f'<!doctype html><html lang="en" class="pathway-{p.lower()}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{palette(p)}{css}</style></head><body>{outer}{nav}{xp}{progress}<main id="lessonDeck" class="slide-container" tabindex="-1">'+''.join(blocks)+f'</main>{navigation}{dialogs}<div id="print-area"></div><script type="application/json" id="lesson-config">'+json.dumps({'title':d['title'],'pathway':p,'term':'Sum1','week':1,'sow_slot':27,'stages':STAGES,'timers':TIMERS},ensure_ascii=False)+f'</script><script>{js}</script><script data-hum-t-loop="1">'+(HERE/'loop.js').read_text()+'</script>'+('<script defer src="/hud.js"></script>' if p=='BUILD' else '')+'</body></html>'
 return page,'<html><body><main>'+''.join(before)+'</main></body></html>'
def standalone(p,title,body):
 css=(HERE/'lesson.css').read_text()
 return f'<!doctype html><html lang="en" class="pathway-{p.lower()}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><style>{palette(p)}{css}body{{background:white}}main{{padding:20px}}@media print{{main{{display:block!important;padding:0}}}}</style></head><body><main class="print-sheet"><h1>{E(title)}</h1>{body}</main></body></html>'
def landing(p,d,file,pack=False):
 body=f'<header class="hero"><p class="eyebrow">Progress Schools · Humanities · {p}</p><h1>{p} Humanities · Summer 2026–27</h1><p>Year A: Self and Belonging · Summer theme: Change</p><p>Updated {DATE} · P1 preview · Sum1 W1 available</p></header><h2>Summer sequence · Weeks 27–39</h2><p>One 40-minute session per lesson. Nine stages: Title · Arrival · Starter · I Do · We Do · I Do 2 · We Do 2 · Independent · Exit.</p><div class="grid"><article class="card"><p class="eyebrow">Sum1·W1 · SoW slot 27</p><h2 data-card-title="{p}_HUM_S1_W01">{E(d["title"])}</h2><p>{E(d["objective"])}</p><p><strong>Unit:</strong> {E(d["unit"])}</p><a class="button" data-lesson-id="{p}_HUM_S1_W01" href="{file}">Open lesson</a></article><article class="card"><h2>What comes next</h2><p>Sum1 weeks 2–6 and Sum2 weeks 1–7 follow after P1 approval. They are not included in this preview.</p><p><strong>Weekly routine:</strong> choose one arrival route, read the model, rehearse with support, respond independently and agree the next step.</p></article></div><h2>Access and evidence</h2><p>{ACCESS}</p><p>{E(CAVEAT)}</p>'
 if pack:body+='<h2>Companion resources</h2><div class="toolbar">'+''.join(f'<a class="button" href="{p}/Summer_1/W01/{f}">{label}</a>' for f,label in [('Knowledge_Organiser.html','Knowledge organiser'),('Pupil_Resources.html','Pupil resources'),('Teacher_Notes.docx','Editable teacher notes'),('Editable_Slides.pptx','Editable slides'),('Sources_and_checks.html','Sources and checks')])+'</div>'
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{p} Humanities · Summer 2026–27</title><style>{palette(p)}{(HERE/"lesson.css").read_text()}</style></head><body><main class="landing">{body}</main></body></html>'
def build():
 population=[];before={}
 for p,d in DATA.items():
  id=p+'_HUM_S1_W01';filename=id+'_Lesson.html';pack=ROOT/'packs'/f'HUM_Summer_1_{p}_Final';folder=pack/p/'Summer_1/W01';target=f'Humanities_Teesside/{p}_W27-W39_2026-27/{filename}'
  raw,prior=lesson(p,d);put(folder/filename,raw);before[id]=prior
  put(folder/'Knowledge_Organiser.html',standalone(p,d['title']+' · Knowledge organiser',organiser(p,d)))
  sheets=''
  for r in ROUTES:
   sheets+='<section class="paper-section"><h2>'+r.title()+' arrival · choose one route</h2><p>'+ACCESS+'</p>'+''.join(f'<h3>{i+1}. {E(q[0])}</h3><p>{E(q[1])}</p><p class="small">Help: {E(q[2])}</p><div class="response-lines" style="min-height:12mm"></div>' for i,q in enumerate(d['arrival'][r]))+'</section>'
  sheets+='<section class="paper-section"><h2>Evidence to use</h2>'+visual(p)+'</section>'
  for i,r in enumerate(ROUTES):sheets+=f'<section class="paper-section"><h2>{r.title()} independent task</h2><p>{E(d["independent"][i])}</p><div class="response-lines"></div><h2>Exit</h2><p>{E(d["exit"][i][0])}</p><div class="response-lines"></div></section>'
  put(folder/'Pupil_Resources.html',standalone(p,d['title']+' · Pupil resources',sheets))
  put(folder/'Sources_and_checks.html',standalone(p,d['title']+' · Sources and checks',source_block(d)+f'<h2>Curriculum trace</h2><p>{E(d["objective"])}</p><p>{E(CAVEAT)}</p><p>Full-year SoW SHA256 ac8f8d0a4188d147097a491b0db59efef16feb0c0f6c4fa8e13144bb8a53f69f. Policy references: Curriculum §§8–10, 12.2, 14.3–14.4; Feedback body §§5, 11, 14.</p>'))
  put(pack/'START_HERE.html',landing(p,d,f'{p}/Summer_1/W01/{filename}',True))
  put(ROOT/'landing'/f'{p}_W27-W39_2026-27/START_HERE.html',landing(p,d,'./'+filename))
  row={'id':id,'pathway':p,'subject':'Humanities','term':'Sum1','week':1,'sow_slot':27,'objective':d['objective'],'html':str((folder/filename).relative_to(ROOT)),'classification':'new_core_sow_lesson','chassis':'classroom' if p=='BUILD' else 'review','target':target,'title':d['title']}
  population.append(row)
  with (pack/'COVERAGE.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=row,lineterminator="\n");w.writeheader();w.writerow({**row,'html':str((folder/filename).relative_to(pack))})
  put(pack/f'CHANGELOG_Final_{DATE}.md',f'# P1 preview · {DATE}\n\nOne new core SoW lesson: {id}. Nine stages, one 40-minute session. Summer theme Change, Year A Self and Belonging. Remaining Summer weeks await P1 approval. No accreditation unit code supplied or invented.\n')
 put(ROOT/'qa/population.json',json.dumps(population,ensure_ascii=False,indent=2)+'\n')
 put(ROOT/'qa/pre_loop_content.json',json.dumps(before,ensure_ascii=False,indent=2)+'\n')
 put(HERE/'content.json',json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
 allrows=[]
 for plan in json.loads((HERE/'coverage_plan.json').read_text()):
  present=next((r for r in population if r['id']==plan['id']),None)
  allrows.append({**{k:'' for k in population[0]},**plan,**(present or {}),'status':'P1 authored' if present else 'WAITING P1 ok'})
 with (ROOT/'COVERAGE.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=allrows[0],lineterminator="\n");w.writeheader();w.writerows(allrows)
 print(json.dumps({'lessons':len(population),'landing_pages':3,'minutes':sum(TIMERS),'output':str(ROOT)}))
if __name__=='__main__':build()
