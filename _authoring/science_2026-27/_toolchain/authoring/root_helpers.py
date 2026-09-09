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
