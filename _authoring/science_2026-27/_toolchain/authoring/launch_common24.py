import json, pathlib, copy
ROOT=pathlib.Path('/workspace/scratch/53a97a57d058/science_next24')
INK='#1F2937'; PURPLE='#7A5C9E'; BLUE='#4D82A0'; GREEN='#3F7D6E'; ORANGE='#C9803B'
def text(x,y,w,h,s,size=28,bold=False,align='left',color=INK):
 return dict(type='text',x=x,y=y,w=w,h=h,text=s,size=size,bold=bold,align=align,color=color)
def rect(x,y,w,h,fill='#F0EBF5',stroke=PURPLE):
 return dict(type='rect',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,strokeWidth=3)
def ellipse(x,y,w,h,fill='#E4F0E9',stroke=GREEN):
 return dict(type='ellipse',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,strokeWidth=3)
def line(x,y,x2,y2,arrow=False,color=PURPLE,width=4):
 return dict(type='line',x=x,y=y,x2=x2,y2=y2,arrow=arrow,stroke=color,strokeWidth=width)
def visual(title,desc,els):
 return dict(title=title,description=desc,width=1000,height=560,elements=[text(30,20,940,48,title,30,True)]+els)
def boxes(title,desc,labels,footer='',arrows=True):
 pos=[(45,110),(540,110),(45,330),(540,330)]
 els=[]
 for (x,y),s in zip(pos,labels): els.extend([rect(x,y,415,145),text(x+20,y+18,375,115,s,26,True)])
 if arrows:
  els.extend([line(470,183,525,183,True),line(750,268,750,317,True),line(530,402,475,402,True)])
 if footer:els.append(text(40,495,920,45,footer,25))
 return visual(title,desc,els)
def bars(title,desc,labels,values,ymax,unit):
 els=[text(40,75,900,40,unit,26),line(120,450,925,450,color=INK),line(120,135,120,450,color=INK)]
 for i in range(5):
  n=ymax*i/4;y=450-300*i/4
  els.extend([line(120,y,925,y,color='#D9D4E0',width=1),text(35,y-18,70,35,str(int(n)) if n==int(n) else str(n),24,align='right')])
 count=len(labels);pitch=740/count
 for i,(label,value) in enumerate(zip(labels,values)):
  x=155+pitch*i;h=300*value/ymax
  els.extend([rect(x,450-h,pitch-35,h,fill='#DACEEC'),text(x,450-h-40,pitch-35,35,str(value),25,True,'center'),text(x-5,465,pitch-25,75,label,25,align='center')])
 return visual(title,desc,els)
def graph(title,desc,xvals,series,ymax,unit,xlabel):
 els=[text(35,75,930,40,unit,25),line(130,430,920,430,color=INK),line(130,140,130,430,color=INK)]
 for k in range(5):
  val=ymax*k/4;y=430-270*k/4
  els.extend([line(130,y,920,y,color='#D9D4E0',width=1),text(38,y-18,78,36,str(int(val)),24,align='right')])
 xs=[150+740*(v-min(xvals))/(max(xvals)-min(xvals)) for v in xvals]
 for x,v in zip(xs,xvals):els.append(text(x-35,442,70,35,str(v),24,align='center'))
 for si,(label,vals,color) in enumerate(series):
  pts=[(x,430-270*v/ymax) for x,v in zip(xs,vals)]
  for (x1,y1),(x2,y2) in zip(pts,pts[1:]):els.append(line(x1,y1,x2,y2,color=color))
  for x,y in pts:els.append(ellipse(x-6,y-6,12,12,fill=color,stroke=color))
  els.append(text(150+si*385,510,370,36,label,24,True,color=color))
 els.append(text(250,476,590,32,xlabel,24,align='center'))
 return visual(title,desc,els)
def slide(stage,minutes,title,body,notes,**kw):return dict(stage=stage,minutes=minutes,title=title,body=body,notes=notes,**kw)
def table(headers,rows,caption=''):return dict(headers=headers,rows=rows,caption=caption)
def response(prompt,lines=3):return dict(type='response',prompt=prompt,lines=lines)
def tb(headers,rows):return dict(type='table',headers=headers,rows=rows)
def txt(s):return dict(type='text',text=s)
def page(title,intro,blocks):return dict(title=title,intro=intro,blocks=blocks)
def choices(prompt,items):return dict(type='choices',prompt=prompt,choices=items)
def qa(label,answer):return dict(label=label,answer=answer)
def source(title,url,note):return dict(title=title,url=url,note=note+' Checked 9 September 2026.')
SPEC=source('Pearson Edexcel GCSE Biology 1BI0 specification','https://qualifications.pearson.com/content/dam/pdf/GCSE/Science/2016/Specification/gcse-biology-spec.pdf','Used to check relevant Foundation curriculum content; this is teacher-authored practice, not an official assessment or complete unit.')
def base(id,title,subtitle,objective,seq,alignment,prior,success,vocab):
 r=next(x for x in json.load(open(ROOT/'selection_map.json'))['lessons'] if x['pathway']=='LAUNCH' and x['sequence']==seq)
 return dict(id=id,pathway='LAUNCH',title=title,subtitle=subtitle,objective=objective,sow=dict(workbook=r['workbook'],sheet=r['sheet'],cells=r['cell'],term='Spring 2' if seq==1 else 'Summer 1',week=r['week'],exactOutcome=r['outcome'],alignment=alignment),priorLearning=prior,success=success,vocabulary=[dict(term=t,meaning=m) for t,m in vocab],equipment=['Shared evidence sheet, one selected response route, pen and ruler.','Projector or offline HTML/PowerPoint; calculator where useful.'],preparation=['Print the shared page, one selected response route and the exit page. Routes are alternatives, not extra tasks.','Read the worked answers and note any constructed data before teaching.'],safety=['Paper and screen lesson; no human sampling, exercise test, breath holding, medicine handling or personal health disclosure.'],practicalAlternative='All evidence is supplied. Use paper diagrams and cards, pointing, annotation or dictation if a device is unavailable.',misconceptions=[],access=dict(supported='Same core concepts with chunked prompts and read-aloud access. Record support used; a pathway is not a diagnosis or fixed attainment label.',standard='Explain the supplied evidence independently using accurate scientific terms and units.',stretch='Optional deeper transfer or evaluation. Higher-tier-only material is labelled explicitly and is not required for the core outcome.',regulation='Offer solo or partner work, a quiet response, a pass and brief reset with clear re-entry. No forced disclosure or public performance.'),sources=[copy.deepcopy(SPEC)],slides=[],pupilPages=[],answers=[],teacherNotes=['40-minute lesson. Zero-minute slides share the preceding stage allocation.','Choose one response route. Accept accurate speech, pointing with explanation, annotations or writing; record the support used.','A teacher or TA can be a quiet audience: ask one evidence question, then let the pupil revise or justify a decision.'])
def misconception(claim,correction,check):return dict(claim=claim,correction=correction,check=check)
def save(j):
 assert len(j['slides'])==15,(j['id'],len(j['slides']))
 assert sum(s['minutes'] for s in j['slides'])==40,(j['id'],sum(s['minutes'] for s in j['slides']))
 assert len(j['pupilPages'])==5
 p=ROOT/'content'/f"{j['id']}.json";tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');tmp.replace(p);print(p)
def option(t,correct,feedback):return dict(text=t,correct=correct,feedback=feedback)
def step(q,good,bad,v,why,wrong):return dict(question=q,choices=[option(good,True,why),option(bad,False,wrong)],visual=v,explanation=why)
def interactive(title,intro,steps,index=5):return dict(title=title,intro=intro,slideIndex=index,steps=steps)
