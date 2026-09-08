# Census of calendar-specific tokens in PUPIL-FACING text of lesson HTML. Staff layers skipped: [data-mbm-guide], .ta-drawer, #mbmTA, .mbm-modal, script/style/template/noscript(?), <head> meta except title.
import re,sys,os,json,html
from html.parser import HTMLParser
FORBID=re.compile(r"\bW(?:eek)?\s?\d+\b|\bAut(?:umn)?\s?[12]\b|\bSpr(?:ing)?\s?[12]\b|\bw/c\b|2026-27|\bof 14\b|\bof 8\b",re.I)
STAFF_ATTR=('data-mbm-guide',)
STAFF_CLASSES={'ta-drawer','mbm-modal','staff-only','teacher-only','ta-note','ta-focus','staffnote'}
STAFF_IDS={'mbmTA','ta','staff','teacher-notes'}
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.stack=[]; s.hits=[]; s.skipdepth=0; s.rawskip=0
    def handle_starttag(s,t,a):
        a=dict(a); cls=set((a.get('class') or '').split()); staff=any(k in a for k in STAFF_ATTR) or (cls&STAFF_CLASSES) or (a.get('id') in STAFF_IDS) or t in('script','style','template','noscript')
        sig=t+('#'+a['id'] if a.get('id') else '')+(''.join('.'+c for c in sorted(cls)[:3]))
        s.stack.append((t,sig,staff,dict(a)))
        if t in('meta',) and a.get('content') and FORBID.search(a['content']): s.hits.append(('meta:'+(a.get('name') or a.get('property') or '?'),a['content'],'head'))
        for k in('data-title','aria-label','title','data-page-title','alt'):
            if a.get(k) and FORBID.search(a[k]) and not s.instaff(): s.hits.append(('attr:'+k+' on '+sig,a[k],'/'.join(x[1] for x in s.stack[-4:])))
        if t in('br','img','meta','link','input','hr','source','wbr','col','area','base','embed','param','track'): s.stack.pop()
    def instaff(s): return any(x[2] for x in s.stack)
    def handle_endtag(s,t):
        for i in range(len(s.stack)-1,-1,-1):
            if s.stack[i][0]==t: del s.stack[i:]; break
    def handle_data(s,d):
        if s.instaff(): return
        d=re.sub(r'\s+',' ',d).strip()
        if d and FORBID.search(d): s.hits.append(('text',d,'/'.join(x[1] for x in s.stack[-5:])))
out={}
for p in sys.argv[1:]:
    q=P(); q.feed(open(p,encoding='utf-8').read()); out[p]=q.hits
json.dump(out,open(os.environ.get('CENSUS_OUT','relabel_census.json'),'w'),indent=1,ensure_ascii=False)
tot=sum(len(v) for v in out.values()); print('files',len(out),'pupil-facing hits',tot)
from collections import Counter
c=Counter()
for p,v in out.items():
    for kind,txt,path in v: c[(kind.split(' on ')[0] if kind.startswith('attr') else kind, path.split('/')[-1] if path!='head' else 'head')]+=1
for k,n in c.most_common(40): print(f'{n:5d}  {k[0]:14s} {k[1]}')
