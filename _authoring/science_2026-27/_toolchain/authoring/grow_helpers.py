import json, pathlib, copy
ROOT=pathlib.Path('/workspace/scratch/53a97a57d058/science_next24')
OUT=ROOT/'content'
DARK='#1F2937'; GREEN='#3F7D6E'; BLUE='#4D82A0'; ORANGE='#C9803B'; RED='#B64745'
def txt(x,y,w,h,text,size=28,color=DARK,bold=False):return dict(type='text',x=x,y=y,w=w,h=h,text=text,size=size,color=color,bold=bold,align='center')
def rect(x,y,w,h,fill='#EFF7F3',stroke=GREEN):return dict(type='rect',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,strokeWidth=3)
def ell(x,y,w,h,fill='#EFF7F3',stroke=GREEN):return dict(type='ellipse',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,strokeWidth=3)
def line(x,y,x2,y2,color=DARK,arrow=True):return dict(type='line',x=x,y=y,x2=x2,y2=y2,stroke=color,strokeWidth=5,arrow=arrow)
def vis(title,description,els):return dict(title=title,description=description,width=1000,height=560,elements=els)
def boxes(title,labels,caption='',colors=None):
    n=len(labels); w=(880-30*(n-1))/n; es=[txt(40,25,920,50,title,32,bold=True)]
    for i,label in enumerate(labels):
        x=60+i*(w+30); es += [rect(x,190,w,130,stroke=(colors or [GREEN]*n)[i]),txt(x+8,210,w-16,90,label,27)]
        if i<n-1:es.append(line(x+w,255,x+w+30,255))
    if caption:es.append(txt(50,375,900,130,caption,27))
    return vis(title,'A simplified scientific sequence: '+ '; '.join(labels)+'. '+caption,es)
def loop(title,labels,caption,colors=None):
    xy=[(80,110),(610,110),(610,340),(80,340)];es=[txt(40,22,920,50,title,32,bold=True)]
    for i,(x,y) in enumerate(xy):es += [rect(x,y,310,110,stroke=(colors or [GREEN]*4)[i]),txt(x+10,y+16,290,80,labels[i],28)]
    es += [line(390,165,610,165),line(765,220,765,340),line(610,395,390,395),line(235,340,235,220),txt(55,478,890,60,caption,25)]
    return vis(title,'Clockwise sequence: '+ '; '.join(labels)+'. '+caption,es)
def slide(stage,minutes,title,body,notes,**kw):return dict(stage=stage,minutes=minutes,title=title,body=body,notes=notes,**kw)
def response(prompt,lines=3):return dict(type='response',prompt=prompt,lines=lines)
def choices(prompt,cs):return dict(type='choices',prompt=prompt,choices=cs)
def table(headers,rows,caption=None):
    d=dict(headers=headers,rows=rows)
    if caption:d['caption']=caption
    return d
def tb(headers,rows):return dict(type='table',headers=headers,rows=rows)
def textblock(text):return dict(type='text',text=text)
def cards(items):return dict(type='cards',cards=[dict(title=t,text=s) for t,s in items])
def page(title,intro,blocks):return dict(title=title,intro=intro,blocks=blocks)
def opts(items):return [dict(text=t,feedback=f,correct=c) for t,c,f in items]
def ans(label,answer):return dict(label=label,answer=answer)
def source(title,url,note):return dict(title=title,url=url,note=note)
SOW=json.loads(pathlib.Path('/workspace/scratch/53a97a57d058/science_source_audit/GROW_Science_SOW.json').read_text())
def base(id,title,subtitle,obj,row,prior,success,vocab,equip,prep,safety,alternative,mis,access,sources):
    r=next(r for r in SOW['scienceRows'] if r['sheet']=='GROW Weekly - Spring' and r['row']==row)
    return dict(id=id,pathway='GROW',title=title,subtitle=subtitle,objective=obj,sow=dict(workbook=SOW['workbook'],sheet=r['sheet'],cells=f'B{row}:C{row}',term='Spring 1' if row<34 else 'Spring 2',week=r['week'],exactOutcome=r['outcome'],alignment='Directly develops this stated outcome with secondary-age tasks at an upper-KS2 conceptual level. Support and stretch are flexible; this exemplar is not a claim of qualification approval.'),priorLearning=prior,success=success,vocabulary=[dict(term=t,meaning=m) for t,m in vocab],equipment=equip,preparation=prep,safety=safety,practicalAlternative=alternative,misconceptions=[dict(claim=c,correction=k,check=q) for c,k,q in mis],access=dict(supported=access[0],standard=access[1],stretch=access[2],regulation='Offer quiet pointing, private writing, drawing or adult scribing. Pass-and-return for public questions. Use fictional cases; no personal medical disclosure or comparison of bodies. Assign response routes from current evidence, not fixed pupil labels.'),sources=sources,slides=[],pupilPages=[],answers=[],teacherNotes=[])
def finish(d,notes):
    assert len(d['slides'])==15,(d['id'],len(d['slides']))
    assert sum(x['minutes'] for x in d['slides'])==40
    assert len(d['pupilPages'])==5
    assert sum('visual' in x for x in d['slides'])>=3
    d['teacherNotes']=['40 minutes: opening 2; retrieval 3; I do 8; We do 8; hinge 3; You do 10; review 4; exit 2. Zero-minute slides share their stage time.','Supply shared page 1, one selected route page 2, 3 or 4, and page 5. Do not require all three routes. An independent spoken explanation can be recorded verbatim by an adult.']+notes
    tmp=OUT/(d['id']+'.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2));tmp.replace(OUT/(d['id']+'.json'))
    print(d['id'],flush=True)
def interactive(d,title,items,mode=None):
    steps=[]
    for i,(q,cs,ex) in enumerate(items):steps.append(dict(question=q,choices=opts(cs),visual=copy.deepcopy(d['slides'][2+i]['visual']),explanation=ex))
    d['interactive']=dict(title=title,intro='Predict first, test the model, then explain using the evidence. Move at your own pace; paper W1–W3 tasks assess the same reasoning.',slideIndex=5,steps=steps)
    if mode:d['interactive']['mode']=mode

OLD_BASE=base
SELECTION=json.loads((ROOT/'selection_map.json').read_text())
def base(id,title,subtitle,obj,sequence,prior,success,vocab,equip,prep,safety,alternative,mis,access,sources):
    d=OLD_BASE(id,title,subtitle,obj,32,prior,success,vocab,equip,prep,safety,alternative,mis,access,sources)
    r=next(r for r in SELECTION['lessons'] if r['pathway']=='GROW' and r['sequence']==sequence)
    d['sow']=dict(workbook=r['workbook'],sheet=r['sheet'],cells=r['cell'],term='Spring 2' if r['week'].startswith('Spr') else 'Summer 1',week=r['week'],exactOutcome=r['outcome'],alignment=r['freshness']+' Original secondary-age exemplar at an upper-KS2 conceptual level; no qualification approval or completion claim.')
    d['access']['regulation']='Offer private writing, pointing, drawing or adult scribing. Allow pass-and-return for public questions and desk-based participation. Choose support from current learning evidence, not fixed ability labels.'
    return d

def common_tail(d,brief,checks,review,exitq,exitnote):
    d['slides'] += [slide('You do',10,'Your independent investigation',brief,'10 minutes across the three You do slides. Supply shared page 1 and one selected route page. All routes target the stated science objective; a labelled drawing or independent dictated explanation is valid.'),slide('You do',0,'Use the evidence',checks,'Shared You do time. Ask pupils which evidence supports their explanation. Read prompts or scribe without supplying the scientific conclusion.'),slide('You do',0,'Check before sharing',['Does my explanation answer the question?','Have I named the evidence or process?','Have I kept the conclusion within its limits?'],'Shared You do time. Use the route-specific worked answers to identify one precise next step.'),slide('Review',4,'Compare and improve',review,'4 minutes across Review. Offer partner or private teacher feedback. Ask for one specific revision linked to evidence; no public ranking.'),slide('Review',0,'A question worth investigating',['Suggest one next question about this lesson’s evidence.','Choose a question whose answer would improve our model.'],'Lundy cycle: invite written, spoken or pointed suggestions. Select one feasible question and explain how the pupil contribution changes the next example or investigation.'),slide('Exit',2,'Show the science you can explain',exitq,exitnote)]

FROG=source('Froglife: Common frog','https://www.froglife.org/info-advice/amphibians-and-reptiles/common-frog-2/','Checked September 2026. Common-frog eggs, tadpoles and adult life history. Activities and diagrams are original.')
MONARCH=source('Monarch Joint Venture: Life cycle','https://monarchjointventure.org/monarch-biology/life-cycle','Checked September 2026. Named monarch sequence: egg, larva, pupa, adult; not a rule for all insects.')
PLATYPUS=source('Australian Museum: Platypus','https://australian.museum/learn/animals/mammals/platypus/','Checked September 2026. Egg-laying mammal; young receive milk. This is a counterexample to all mammals giving live birth.')
ROBIN=source('RSPB: Robin','https://www.rspb.org.uk/birds-and-wildlife/robin','Checked September 2026. Eggs, nest and young robin development; no nest disturbance is needed.')
POLLEN=source('OpenStax Biology 2e: Pollination and fertilization','https://openstax.org/books/biology-2e/pages/32-2-pollination-and-fertilization','Checked September 2026. Pollination differs from gamete fusion; fertilised ovule develops into seed and ovary into fruit. College detail is selectively simplified for GROW.')
ASEX=source('OpenStax Biology 2e: Asexual reproduction','https://openstax.org/books/biology-2e/pages/32-3-asexual-reproduction','Checked September 2026. Runners, cuttings and clonal reproduction. Some plants can produce asexual seeds; core examples identify the actual process.')
RSC=source('Royal Society of Chemistry: Separation techniques','https://edu.rsc.org/cpd/separation-techniques/3009787.article','Checked September 2026. Filtration, evaporation and separation misconceptions. Classroom activities are original and include a complete paper route.')
RSC2=source('Royal Society of Chemistry: Separating sand and salt','https://edu.rsc.org/experiments/separating-sand-and-salt-by-filtering-and-evaporation/386.article','Checked September 2026 through primary search extract. Solubility, filtration and evaporation; this pack does not reproduce the heated practical.')
