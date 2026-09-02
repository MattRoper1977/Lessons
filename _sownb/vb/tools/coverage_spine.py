#!/usr/bin/env python3
"""Coverage over the census, weeks 1-26, on the RULED spine (ORDER VB-RUN12A).

Reads /tmp/census_v4.json from census_spine.py. Two readings are printed, the
path reading and the content reading, and they do not yet agree -- see the
header of census_spine.py for what is outstanding.

EXCLUSIONS. Absolute week 8 is excluded for every lane and subject: it is the
enrichment week CALENDAR_2026_27.json names, and zero workbook cells land there
once each Autumn cell is converted from the old keying to the ruled one.
LAUNCH ASDAN week 16 is the C100 STOP, excluded and not a gap.

An "uncovered" slot here is a candidate to investigate, not a licence to build.
Check the cell claim first.
"""
import json,collections,math,re
rows=json.load(open('/tmp/census_v4.json'))
S=json.load(open('_sownb/CALENDAR_SPINE.json'))
split={e['path'] for e in S['spineSplits']}
def subj(r):
    if r['subject']:
        if r['subject']=='ASDAN' and '/CAREERS/' in r['path']: return 'OUT'
        return r['subject']
    fn=r['path'].split('/')[-1]
    m=re.match(r'(BUILD|GROW|LAUNCH)_(ART|HUM|DT|L1)_',fn)
    if m: return {'ART':'Art','HUM':'Humanities','DT':'OUT','L1':'ASDAN'}[m.group(2)]
    return 'OUT' if fn.startswith('FW_L1') else None
REQ={'ASDAN':1,'Humanities':1,'Art':1}; SCI={'BUILD':2,'GROW':2,'LAUNCH':3}
lanes=['BUILD','GROW','LAUNCH']; subs=['ASDAN','Science','Humanities','Art']; WEEKS=range(1,27)
EXCLUDED_SLOTS={('LAUNCH','ASDAN',16)}|{(l,s,8) for l in ('BUILD','GROW','LAUNCH') for s in ('ASDAN','Science','Humanities','Art')}          # D-F: C100 STOP, excluded not a gap
cov={'path':collections.defaultdict(list),'content':collections.defaultdict(list)}
dh=collections.defaultdict(list); ex=collections.Counter(); spineCredited=[]
for r in rows:
    if r['surface']!='lesson': continue
    s=subj(r); l=r['lane']
    if s in (None,'OUT'): ex['out-of-scope/unsubjected']+=1; continue
    pw=r['pathWeek']
    if r['priorStatus']!='NEW-SINCE-SPINE' and not r['blobChanged']:
        cr=r['priorContentReading']; cw=cr if isinstance(cr,int) else None
    else:
        cw=r['contentWeek'] if isinstance(r['contentWeek'],int) else None
    if r['contentWeek']=='ENRICHMENT':
        cw=None; ex['ENRICHMENT (D-C: no week by ruling)']+=1
        if isinstance(pw,int): pw=None
    if r['path'] in split:
        # D-C RESOLVED: the spine-split decks are counted, by their citation
        cw = r['contentWeek'] if isinstance(r['contentWeek'],int) else cw
        spineCredited.append((l,s,cw,r['path']))
    if isinstance(pw,int): cov['path'][(l,s,pw)].append(r['path'])
    if isinstance(cw,int): cov['content'][(l,s,cw)].append(r['path'])
    elif isinstance(pw,int):
        # D-H: a deck stands on the path, so the slot HAS a deck even untraced
        cov['content'][(l,s,pw)].append(r['path']); dh[(l,s,pw)].append(r['path'])
res={}
for reading in ('path','content'):
    tot=covd=exc=0; matrix={}
    for l in lanes:
        for s in subs:
            line=[]
            for w in WEEKS:
                need=SCI[l] if s=='Science' else REQ[s]
                if (l,s,w) in EXCLUDED_SLOTS: exc+=need; line.append('×'); continue
                have=len(cov[reading][(l,s,w)])
                if s=='Science' and w<=2: have=need
                c=min(need,have); tot+=need; covd+=c
                line.append('■' if c>=need else f"{c}/{need}")
            matrix[f"{l} {s}"]=line
    rem=tot-covd
    res[reading]=dict(required=tot+exc,excluded=exc,effective=tot,covered=covd,remaining=rem,
                      wavesAt24=math.ceil(rem/24),matrix=matrix)
    r_=res[reading]
    print(f"== {reading.upper()}: required {r_['required']} · excluded {r_['excluded']} (C100) · effective {r_['effective']} · covered {covd} · remaining {rem} · waves at 24 = {r_['wavesAt24']}")
    for k,v in matrix.items(): print(f"   {k:18s}"," ".join(f"{x:>3s}" for x in v))
print('excluded decks:',dict(ex))
print('D-H fallback slots credited (content reading only):',len(dh))
print('spine-split decks now counted:',len(spineCredited),'-> distinct slots',len({(l,s,w) for l,s,w,_ in spineCredited if w}))
# WRITES TO /tmp, NOT INTO THE EVIDENCE TREE. The run-11 copy of this tool
# overwrote _sownb/vb/evidence/run11/HORIZON_TOOL_RUN11.json every time it ran,
# silently rewriting a closed run's record -- caught twice in run 12. A
# measurement tool reports; it does not edit history. Copy the output into a
# dated evidence file deliberately if you want one.
json.dump({'file':'_sownb/VB_STATE.json','subject':'horizon recount on the RULED spine (census_spine.py); path and content readings do not yet agree, see the tool header',
  'readings':{k:{kk:vv for kk,vv in v.items() if kk!='matrix'} for k,v in res.items()},
  'matrix':{k:v['matrix'] for k,v in res.items()},
  'dHFallbackSlots':{f"{l}|{s}|{w}":p for (l,s,w),p in dh.items()},
  'spineSplitDecksCounted':len(spineCredited),
  'spineSplitSlots':sorted({f"{l} {s} wk{w}" for l,s,w,_ in spineCredited if w}),
  'excludedDecks':dict(ex)},open('/tmp/horizon_spine.json','w'),indent=1)
# --- run 11: print the uncovered slots on the new spine, week-major, ASDAN -> Science -> Humanities -> Art
try:
    order={'ASDAN':0,'Science':1,'Humanities':2,'Art':3}
    unc=[]
    for w in WEEKS:
        for s in subs:
            for l in lanes:
                need=SCI[l] if s=='Science' else REQ.get(s,1)
                if (l,s,w) in EXCLUDED_SLOTS: continue
                have=len(cov['path'].get((l,s,w),[]))
                if have<need: unc.append({'lane':l,'subject':s,'week':w,'have':have,'need':need})
    unc.sort(key=lambda u:(u['week'],order[u['subject']],u['lane']))
    json.dump(unc,open('/tmp/w4_uncovered.json','w'),indent=1)
    print('UNCOVERED (path reading) weeks 1-26:',len(unc)); 
    for u in [x for x in unc if x['week']>=9][:30]: print(f"  W{u['week']:2} {u['lane']:6} {u['subject']:10} have {u['have']}/{u['need']}")
except Exception as e: print('uncovered print failed:',e)
