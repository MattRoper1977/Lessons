#!/usr/bin/env python3
"""HUM-D5 A3 E14 - readability, measured not judged.
Flesch-Kincaid GRADE on pupil-facing text per lesson per route, read from the
RENDERED route panels (TEXT_INDEX_RENDERED.jsonl rows surface=rendered:route,
data-route-panel="<block>-<level>"): what a pupil on that route sees, all
blocks (arrival/task/shared/model/review/exit/starter/check). Each panel row is
a text unit; a sentence ends at . ! ? or at the end of a unit. Syllables are
counted with a vowel-group heuristic (no textstat in this container) - the
same counter for every lesson, so the between-route comparison is exact even
if the absolute grade carries the heuristic's bias.
FK = 0.39*(words/sentences) + 11.8*(syllables/words) - 15.59.
Flags (Class B, report only): BUILD > 5, GROW > 7, LAUNCH > 9; Supported
harder than Standard by more than 0.5 grade."""
import json, re, sys, collections
IDX, OUT = sys.argv[1], sys.argv[2]
CFG = sys.argv[3] if len(sys.argv)>3 else None   # TEXT_INDEX.jsonl for the config-unit measure
LEVELS=('supported','standard','stretch')
WORD=re.compile(r"[A-Za-z][A-Za-z'’-]*")
def syl(w):
    w=w.lower().strip("'’"); w=re.sub(r"[^a-z]","",w)
    if not w: return 0
    if len(w)<=3: return 1
    w=re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$','',w); w=re.sub(r'^y','',w)
    g=re.findall(r'[aeiouy]+',w); return max(1,len(g))
def fk(units):
    words=0; sents=0; syls=0
    for u in units:
        parts=[p for p in re.split(r'(?<=[.!?])\s+',u.strip()) if p.strip()]
        if not parts: continue
        for p in parts:
            ws=WORD.findall(p)
            if not ws: continue
            sents+=1; words+=len(ws); syls+=sum(syl(x) for x in ws)
    if not words or not sents: return None,words,sents
    return round(0.39*(words/sents)+11.8*(syls/words)-15.59,2),words,sents
units=collections.defaultdict(list); pathway={}
scope={'index':IDX,'rows':0,'route_rows':0,'lessons':set()}
for line in open(IDX,encoding='utf-8'):
    o=json.loads(line); scope['rows']+=1
    if o['surface']!='rendered:route': continue
    m=re.search(r'data-route-panel="([a-z]+)-(supported|standard|stretch)"',o['locator'])
    if not m: continue
    scope['route_rows']+=1; scope['lessons'].add(o['lesson_id'])
    units[(o['lesson_id'],m.group(2))].append(o['text'])
    pathway[o['lesson_id']]=o['lesson_id'].split('_')[0]
# Second instrument: CONFIG route units. The rendered panels collapse
# whitespace, so control labels ("My answer 1") fuse into the next sentence
# and inflate words-per-sentence. The config carries the same pupil text as
# discrete units per route: arrival[i].questions[j][0] (question) and [1]
# (hint) - [2] is the hidden teacher answer and is EXCLUDED - tasks[i].steps,
# tasks[i].help, tasks[i].extension, exits[i][j][*]. i = 0 supported,
# 1 standard, 2 stretch (arrival[i].name proves the order per lesson).
cunits=collections.defaultdict(list); cname={}
if CFG:
    for line in open(CFG,encoding='utf-8'):
        o=json.loads(line)
        if o['surface']!='config': continue
        L=o['locator']; lid=o['lesson_id']
        m=re.match(r'(arrival|tasks|exits)\[(\d)\]',L)
        if not m: continue
        i=int(m.group(2))
        if m.group(1)=='arrival' and L.endswith('.name'): cname[(lid,i)]=o['text'].strip().lower(); continue
        if m.group(1)=='arrival' and not (L.endswith('][0]') or L.endswith('][1]')): continue
        if m.group(1)=='tasks' and not re.search(r'\.(steps\[\d+\]|help|extension)$',L): continue
        cunits[(lid,i)].append(o['text'])
LIMIT={'BUILD':5,'GROW':7,'LAUNCH':9}
rows=[]; flags=[]
for lid in sorted(pathway):
    r={'lesson_id':lid,'pathway':pathway[lid]}
    for k,lv in enumerate(LEVELS):
        g,w,s=fk(units.get((lid,lv),[]))
        r[lv+'_rendered']=g; r[lv+'_rendered_words']=w; r[lv+'_rendered_sentences']=s
        if CFG:
            assert cname.get((lid,k),lv)==lv, (lid,k,cname.get((lid,k)))
            cg,cw,cs=fk(cunits.get((lid,k),[]))
        else: cg,cw,cs=None,0,0
        r[lv]=cg; r[lv+'_words']=cw; r[lv+'_sentences']=cs
        if cg is not None and cg>LIMIT[pathway[lid]]:
            flags.append({'lesson_id':lid,'route':lv,'grade':cg,'limit':LIMIT[pathway[lid]],'kind':'above pathway ceiling'})
    if r['supported'] is not None and r['standard'] is not None and r['supported']-r['standard']>0.5:
        flags.append({'lesson_id':lid,'route':'supported','grade':r['supported'],'standard':r['standard'],'kind':'Supported reads harder than Standard'})
    rows.append(r)
scope['lessons']=len(scope['lessons'])
json.dump({'scope':scope,'formula':'FK grade 0.39*(W/S)+11.8*(Syl/W)-15.59; heuristic syllables','rows':rows,'flags':flags},open(OUT,'w'),indent=1)
print('SCOPE: index rows',scope['rows'],'route rows',scope['route_rows'],'lessons',scope['lessons'])
print('FLAGS are computed on the CONFIG-UNIT measure (columns supp/std/str); rendered-panel grades shown beside for the record.')
print(f"{'lesson':20s} {'pw':7s} {'supp':>6s} {'std':>6s} {'str':>6s} | {'r-supp':>6s} {'r-std':>6s} {'r-str':>6s}")
for r in rows: print(f"{r['lesson_id']:20s} {r['pathway']:7s} {str(r['supported']):>6s} {str(r['standard']):>6s} {str(r['stretch']):>6s} | {str(r['supported_rendered']):>6s} {str(r['standard_rendered']):>6s} {str(r['stretch_rendered']):>6s}")
import statistics
for pw in ('BUILD','GROW','LAUNCH'):
    for lv in LEVELS:
        v=[r[lv] for r in rows if r['pathway']==pw and r[lv] is not None]
        vr=[r[lv+'_rendered'] for r in rows if r['pathway']==pw and r[lv+'_rendered'] is not None]
        if v: print(f'  {pw:7s} {lv:9s} n={len(v):3d} config: median={statistics.median(v):5.2f} max={max(v):5.2f} over={sum(1 for x in v if x>LIMIT[pw])}  | rendered: median={statistics.median(vr):5.2f} max={max(vr):5.2f}  ceiling={LIMIT[pw]}')
print('FLAGS:',len(flags))
for f in flags: print('  ',f)
