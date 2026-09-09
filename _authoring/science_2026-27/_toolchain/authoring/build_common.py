import json, math, sys
from pathlib import Path
ROOT=Path('/workspace/scratch/53a97a57d058/science_next24')
DARK='#1F2937'; BLUE='#4E7A9B'; GREEN='#3F7D6E'; GOLD='#C9803B'; PALE='#EDF3F7'; WATER='#347EBC'
def tx(x,y,w,h,text,size=28,bold=False,color=DARK,align='left'):return dict(type='text',x=x,y=y,w=w,h=h,text=text,size=size,bold=bold,color=color,align=align)
def rect(x,y,w,h,fill=PALE,stroke=BLUE,sw=3):return dict(type='rect',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,strokeWidth=sw)
def ell(x,y,w,h,fill='white',stroke=DARK,sw=3):return dict(type='ellipse',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,strokeWidth=sw)
def line(x,y,x2,y2,color=BLUE,arrow=True,sw=4):return dict(type='line',x=x,y=y,x2=x2,y2=y2,stroke=color,strokeWidth=sw,arrow=arrow)
def vis(title,desc,e):return dict(title=title,description=desc,width=1000,height=560,elements=e)
def slide(stage,minutes,title,body,notes,**kw):return dict(stage=stage,minutes=minutes,title=title,body=body,notes=notes,**kw)
def resp(prompt,lines=2):return dict(type='response',prompt=prompt,lines=lines)
def choices(prompt,items):return dict(type='choices',prompt=prompt,choices=items)
def textblock(text):return dict(type='text',text=text)
def cards(items):return dict(type='cards',cards=[dict(title=a,text=b) for a,b in items])
def tb(headers,rows):return dict(type='table',headers=headers,rows=rows)
def table(headers,rows,caption):return dict(headers=headers,rows=rows,caption=caption)
def page(title,intro,blocks):return dict(title=title,intro=intro,blocks=blocks)
def step(q,options,v,explanation):return dict(question=q,choices=[dict(text=t,correct=c,feedback=f) for t,c,f in options],visual=v,explanation=explanation)
def opts(options):return [dict(text=t,correct=c,feedback=f) for t,c,f in options]
def source(title,url,note):return dict(title=title,url=url,note='Checked 8 September 2026. '+note)
NC=source('Department for Education: science programmes of study','https://www.gov.uk/government/publications/national-curriculum-in-england-science-programmes-of-study/national-curriculum-in-england-science-programmes-of-study','Year 3 plants, rocks, light and forces underpin the SOW. Accessible teaching models are adapted to the named lesson objective.')
BGS=source('British Geological Survey: fossils','https://www.bgs.ac.uk/discovering-geology/fossils-and-geological-time/fossils/','Preserved ancient remains or traces; formation and limits of fossil evidence.')
SAPS=source('Science and Plants for Schools: plant biology animations','https://www.saps.org.uk/teaching-resources/resources/1299/biology-animations-transport-of-water-and-sugar-respiration-and-photosynthesis-and-cell-growth-in-plants/','Scientific background for our original simplified diagrams: photosynthesis, growth and transport. No external animation is required or embedded.')
WATER_SOURCE=source('Science and Plants for Schools: water transport','https://www.saps.org.uk/growth-hub/plants-as-inspirational-contexts-2-water-transport-in-plants/','Xylem transports water and dissolved minerals; evaporation from leaves contributes to pulling water upwards. Phloem sugar transport is distinct.')
CELERY=source('Science and Plants for Schools: how does water travel through a plant?','https://www.saps.org.uk/teaching-resources/resources/6555/how-does-water-travel-through-a-plant/','Dye evidence can reveal internal water pathways. Our cut-shoot demonstration is explicitly not a complete rooted plant.')
RHS=source('Royal Horticultural Society: sowing seeds indoors','https://www.rhs.org.uk/propagation/how-to-sow-seeds-indoors','Germination uses stored reserves and requires appropriate water, oxygen and temperature; seedling care differs from starting germination.')
RHS_SEED=source('Royal Horticultural Society: germination guide','https://www.rhs.org.uk/membership/rhs-members-seed-scheme/germination-guide','Species differ in their germination requirements, including whether light is required.')
FRICTION=source('OpenStax: friction','https://openstax.org/books/college-physics-2e/pages/5-1-friction','Sliding friction opposes relative sliding at the contact. In a horizontal constant-speed pull, opposing horizontal forces balance. Surface-pair results are not universal rankings.')
ROWS=json.load(open('/workspace/scratch/53a97a57d058/science_source_audit/BUILD_Science_SOW.json'))['scienceRows']
def base(id,title,subtitle,row,obj,vocab,success,prior,mis,extra_sources=None):
 sheet='BUILD Weekly - Spring' if row==39 else 'BUILD Weekly - Summer'; r=next(x for x in ROWS if x['sheet']==sheet and x['row']==row)
 return dict(id=id,pathway='BUILD',title=title,subtitle=subtitle,objective=obj,sow=dict(workbook='_passsb/inputs/Build SOW 2026-2027.xlsx',sheet=sheet,cells=f'C{row}',term='Spring 2' if row==39 else ('Summer 1' if row<=35 else 'Summer 2'),week=r['week'],exactOutcome=r['outcome'],alignment='Chronological continuation of the supplied SOW. This lesson develops or reviews the named outcome; it does not claim an accreditation award.'),priorLearning=prior,success=success,vocabulary=[dict(term=t,meaning=m) for t,m in vocab],equipment=['Printed shared evidence and one chosen pupil route; pencil; optional ruler; projector or offline HTML.'],preparation=['Print the shared evidence, one response route and exit page. Routes are alternatives, not a workload ladder.','Read the worked answers. Prepare an oral, pointing or adult-scribed route where useful.'],safety=['Paper and screen route requires no biological handling.'],practicalAlternative='All core reasoning uses the supplied evidence and can be completed in 40 minutes without a live practical.',misconceptions=[dict(claim=a,correction=b,check=c) for a,b,c in mis],access=dict(supported='Short choices, word bank and pointing or adult-scribed reasons; same core scientific goal.',standard='Make a short evidence-based explanation or record using the supplied information.',stretch='Apply the core idea to a changed case, evaluate evidence or identify a limit.',regulation='Preview the sequence. Offer seated observation, quiet paired rehearsal, private feedback and a pass from public sharing. Routes respond to current access needs, not a diagnosis.'),sources=[NC]+(extra_sources or []),slides=[],pupilPages=[],answers=[],teacherNotes=[])
def end(d,routes,script,review,reviewanswer,exits,answers,extra_notes=None):
 # Eight slides already written: 2+3+7+0+0+4+4+3 = 23 minutes.
 d['slides'] += [slide('You do',2,'Choose your science route',routes,'Set ONE route. '+script),slide('You do',10,'Make your own evidence record',['Use the shared evidence.','Explain one choice.','Check a label or number.'],script),slide('You do',0,'Check what the evidence can show',['Point to the clue you used.','Remove an unsupported claim.'],'Shares independent time. Ask for a reason, not just a correct word. '+script),slide('Review',3,'Lundy loop: improve the shared account',['Choose how to share.','Hear one evidence-based challenge.','Improve or defend one idea.'],'Listen to a selected pupil revision and visibly adopt a scientifically accurate contribution. Offer private, written or partner feedback.',prompt=review,reveal=reviewanswer),slide('Review',0,'Keep the useful change',['What changed in our account?','Which evidence helped?'],'Shares review time. Name how a pupil contribution changed a label, method or conclusion. Do not rank pupils.',reveal=reviewanswer),slide('Exit',2,'Three final checks',[f'E{i+1}. {q}' for i,q in enumerate(exits)],'Collect brief individual evidence. Use the answer key and re-teach the specified misconception if needed.')]
 d['pupilPages'].append(page('Exit and reflection','Point, draw, write or tell an adult.',[resp(f'E{i+1}. {q}',2) for i,q in enumerate(exits)]+[resp('R1. Which idea did you improve or defend? What evidence helped?',3),resp('R2. What useful question would you investigate next?',2)]))
 d['answers']=[dict(label=a,answer=b) for a,b in answers]+[dict(label='R1–R2',answer='Responses vary. Credit a scientific revision, evidence-based defence or relevant next question. A private or oral response has equal value.')]
 d['teacherNotes']=['40 minutes: opening 2, retrieval 3, I do 7, We do 8, hinge 3, independent 12, review 3, exit 2. Zero-minute slides share the named stage time.','BUILD uses the supplied Year 3 science anchor with age-respectful contexts for older pupils. Supported, standard and stretch are selectable routes within the pathway.','Interactive We do: predict first, test against the controlled SVG model or supplied evidence, then explain or revise. Shared W tasks offer the equivalent paper discussion. Animation is a teaching representation, not filmed experimental evidence.','Keep constructed evidence separate from actual class observations. Do not invent measurements or require internet research.']+(extra_notes or [])
 assert len(d['slides'])==14,(d['id'],len(d['slides']))
 assert sum(s['minutes'] for s in d['slides'])==40
 assert len(d['pupilPages'])==5
 assert len(d['interactive']['steps'])==3
 # Root-reviewed first-four JSON refinements are authoritative and must be preserved.
 if d['id'] in {'build_evidence_museum','build_plant_parts_atlas','build_plant_system_jobs','build_growth_needs_clinic'} and (ROOT/'content'/f"{d['id']}.json").exists():return
 if len(sys.argv)>1 and d['id'] not in sys.argv[1:]:return
 p=ROOT/'content'/f"{d['id']}.json";tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2));tmp.replace(p);print(d['id'],flush=True)
def plant_e(x=440,ground=390,top=115,flower=True,colour=GREEN):
 e=[rect(x-130,ground,280,125,'#F3E8D7',GOLD),line(x,ground,x,top,colour,False,12),ell(x-130,top+85,130,65,'#DDEDE2',colour),ell(x+4,top+140,135,65,'#DDEDE2',colour)]
 for xx,yy in [(x-80,ground+65),(x+90,ground+65),(x-40,ground+100),(x+35,ground+105)]:e.append(line(x,ground,xx,yy,GOLD,False,6))
 if flower:
  for dx,dy in [(-40,-20),(25,-20),(-40,35),(25,35)]:e.append(ell(x+dx-18,top+dy-18,62,62,'#F5DDBE',GOLD))
  e.append(ell(x-23,top-5,50,50,'#FFECA8',GOLD))
 return e
