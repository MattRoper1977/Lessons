"""Approximate SVG label clearance gate for SC4, with sampled curves and marker instances.
Labels: 0.6 * font size * characters wide, one font size high, 0.2 fs descender.
Paths: 48 samples per quadratic/cubic, arcs <= 3-degree steps. Shape edges and markers included.
This is a static screen; Chromium confirmation remains NOT RUN.
"""
import math,re,json
from lxml import etree as ET
from pathlib import Path

def tag(e):return ET.QName(e).localname if isinstance(e.tag,str) else "#comment"

def num(v,d=0):
 try:return float(re.match(r'[-+]?\d*\.?\d+',str(v)).group())
 except:return d

def paths(d):
 ts=re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?',d);i=0;cmd='';cur=(0.,0.);start=cur;ctrl=None;prev='';lines=[];part=[]
 def add(p):
  nonlocal cur
  if part:lines.append((cur,p))
  part.append(p);cur=p
 while i<len(ts):
  if ts[i].isalpha():cmd=ts[i];i+=1
  C=cmd.upper();rel=cmd.islower()
  if C=='Z':add(start);part=[];prev=C;cmd='';continue
  n={'M':2,'L':2,'H':1,'V':1,'C':6,'S':4,'Q':4,'T':2,'A':7}.get(C)
  if not n:raise ValueError('unsupported path '+cmd)
  a=list(map(float,ts[i:i+n]));i+=n;ox,oy=cur
  def xy(x,y):return (x+ox,y+oy) if rel else (x,y)
  if C=='M':
   cur=xy(*a);start=cur;part=[cur];cmd='l' if rel else 'L';ctrl=None
  elif C=='L':add(xy(*a));ctrl=None
  elif C=='H':add((a[0]+ox if rel else a[0],oy));ctrl=None
  elif C=='V':add((ox,a[0]+oy if rel else a[0]));ctrl=None
  elif C in ['C','S','Q','T']:
   p0=cur
   if C=='C':p1,p2,p3=xy(*a[:2]),xy(*a[2:4]),xy(*a[4:]);ctrl=p2
   if C=='S':p1=(2*ox-ctrl[0],2*oy-ctrl[1]) if prev in ['C','S'] and ctrl else cur;p2,p3=xy(*a[:2]),xy(*a[2:]);ctrl=p2
   if C=='Q':p1,p3=xy(*a[:2]),xy(*a[2:]);ctrl=p1
   if C=='T':p1=(2*ox-ctrl[0],2*oy-ctrl[1]) if prev in ['Q','T'] and ctrl else cur;p3=xy(*a);ctrl=p1
   for k in range(1,49):
    t=k/48;u=1-t
    if C in ['C','S']:p=(u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])
    else:p=(u*u*p0[0]+2*u*t*p1[0]+t*t*p3[0],u*u*p0[1]+2*u*t*p1[1]+t*t*p3[1])
    add(p)
  elif C=='A':
   rx,ry,deg,large,sweep,x,y=a;end=xy(x,y);rx=abs(rx);ry=abs(ry)
   if not rx or not ry or cur==end:add(end)
   else:
    phi=math.radians(deg);co,si=math.cos(phi),math.sin(phi);dx=(ox-end[0])/2;dy=(oy-end[1])/2;xp=co*dx+si*dy;yp=-si*dx+co*dy
    rat=xp*xp/rx**2+yp*yp/ry**2
    if rat>1:rx*=math.sqrt(rat);ry*=math.sqrt(rat)
    fac=math.sqrt(max(0,(rx**2*ry**2-rx**2*yp**2-ry**2*xp**2)/(rx**2*yp**2+ry**2*xp**2))) * (-1 if bool(large)==bool(sweep) else 1)
    cxp=fac*rx*yp/ry;cyp=-fac*ry*xp/rx;cx=co*cxp-si*cyp+(ox+end[0])/2;cy=si*cxp+co*cyp+(oy+end[1])/2
    ang=math.atan2((yp-cyp)/ry,(xp-cxp)/rx);en=math.atan2((-yp-cyp)/ry,(-xp-cxp)/rx);delta=(en-ang)%(2*math.pi)
    if not sweep:delta-=2*math.pi
    count=max(2,int(abs(delta)*20))
    for k in range(1,count+1):
     t=ang+delta*k/count;add((cx+co*rx*math.cos(t)-si*ry*math.sin(t),cy+si*rx*math.cos(t)+co*ry*math.sin(t)))
   ctrl=None
  prev=C
 return lines

def edge(e):
 t=tag(e);a=e.attrib
 if t=='path':return paths(a.get('d',''))
 if t=='line':return [((num(a.get('x1')),num(a.get('y1'))),(num(a.get('x2')),num(a.get('y2'))))]
 if t in ['rect','image']:
  x,y,w,h=[num(a.get(k)) for k in ['x','y','width','height']];pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)];return list(zip(pts,pts[1:]))
 if t in ['circle','ellipse']:
  x,y=num(a.get('cx')),num(a.get('cy'));rx=num(a.get('r',a.get('rx')));ry=num(a.get('r',a.get('ry')));pts=[(x+rx*math.cos(i*math.pi/90),y+ry*math.sin(i*math.pi/90)) for i in range(181)];return list(zip(pts,pts[1:]))
 if t in ['polyline','polygon']:
  ns=list(map(float,re.findall(r'[-+]?\d*\.?\d+',a.get('points',''))));pts=list(zip(ns[::2],ns[1::2]));
  if t=='polygon':pts.append(pts[0])
  return list(zip(pts,pts[1:]))
 return []

def intersects(seg,box,pad=0):
 (x1,y1),(x2,y2)=seg;xl,yt,xr,yb=box;xl-=pad;yt-=pad;xr+=pad;yb+=pad
 dx=x2-x1;dy=y2-y1;t0=0;t1=1
 for p,q in [(-dx,x1-xl),(dx,xr-x1),(-dy,y1-yt),(dy,yb-y1)]:
  if abs(p)<1e-9:
   if q<0:return False
  else:
   r=q/p
   if p<0:t0=max(t0,r)
   else:t1=min(t1,r)
   if t0>t1:return False
 return True

def label(e):
 tx=''.join(e.itertext());fs=num(e.get('font-size'),18);x=num(e.get('x'));y=num(e.get('y'));w=.6*fs*len(tx);anchor=e.get('text-anchor','start')
 if anchor=='middle':x-=w/2
 elif anchor=='end':x-=w
 return {'text':tx,'box':(x,y-fs,x+w,y+fs*.18),'element':e}

def analyse(svg):
 root=ET.fromstring(svg.encode());view=list(map(float,root.get('viewBox','0 0 500 360').split()));labels=[];shapes=[];markers={e.get('id'):e for e in root.iter() if tag(e)=='marker'};marker_instances=[]
 for idx,e in enumerate(root.iter()):
  if any(tag(a) in ['defs','clipPath','marker'] for a in e.iterancestors()):continue
  if tag(e)=='text':labels.append(label(e));continue
  seg=edge(e)
  if seg:
   sw=num(e.get('stroke-width'),1 if e.get('stroke') else 0);shapes.append((f'{tag(e)}[{idx}]',seg,sw))
   mr=e.get('marker-end')
   if mr:
    name=mr.split('#')[-1].rstrip(')');m=markers.get(name)
    if m is not None:
     end=seg[-1][1];beg=seg[-1][0];ang=math.atan2(end[1]-beg[1],end[0]-beg[0]);scale=1 if m.get('markerUnits')=='userSpaceOnUse' else sw
     vw=list(map(float,m.get('viewBox',f"0 0 {m.get('markerWidth','3')} {m.get('markerHeight','3')}").split()));sx=num(m.get('markerWidth'),3)/vw[2]*scale;sy=num(m.get('markerHeight'),3)/vw[3]*scale;refx=num(m.get('refX'));refy=num(m.get('refY'))
     def xf(p):
      x=(p[0]-refx)*sx;y=(p[1]-refy)*sy;return(end[0]+x*math.cos(ang)-y*math.sin(ang),end[1]+x*math.sin(ang)+y*math.cos(ang))
     ms=[(xf(a),xf(b)) for c in m for a,b in edge(c)];shapes.append((f'arrowhead:{name}[{idx}]',ms,0));marker_instances.append({'id':name,'width':num(m.get('markerWidth'),3)*scale,'fraction_of_view_width':round(num(m.get('markerWidth'),3)*scale/view[2],4),'units':m.get('markerUnits','strokeWidth')})
 issues=[]
 for i,l in enumerate(labels):
  b=l['box']
  if b[0]<view[0] or b[1]<view[1] or b[2]>view[0]+view[2] or b[3]>view[1]+view[3]:issues.append({'label':l['text'],'collision':'viewBox edge','box':b})
  for name,segs,sw in shapes:
   if any(intersects(seg,b,sw/2+1) for seg in segs):issues.append({'label':l['text'],'collision':name,'box':b})
  for other in labels[i+1:]:
   c=other['box']
   if b[0]-1<c[2] and b[2]+1>c[0] and b[1]-1<c[3] and b[3]+1>c[1]:issues.append({'label':l['text'],'collision':'label:'+other['text'],'box':b})
 return root,labels,shapes,issues,marker_instances

def check_file(p):
 h=p.read_text();s=re.search(r'<svg\b.*?</svg>',h,re.S).group();_,labs,shapes,issues,marks=analyse(s)
 return {'file':str(p),'labels':len(labs),'edge_sets':len(shapes),'markers':marks,'collisions':issues,'browser':'NOT RUN'}
if __name__=='__main__':
 import sys
 r=Path(sys.argv[1]);out=[]
 for p in sorted(r.glob('SCI_*/*/*.html')):
  if p.name=='KNOWLEDGE_ORGANISER.html':continue
  out.append(check_file(p))
 (r/'svg_clearance_report.json').write_text(json.dumps(out,indent=2)+'\n')
 for x in out:
  if x['collisions']:print(Path(x['file']).parent.parent.name,Path(x['file']).parent.name,[(a['label'],a['collision']) for a in x['collisions']])
 print(len(out),'SVGs;',sum(len(x['collisions']) for x in out),'flags')
