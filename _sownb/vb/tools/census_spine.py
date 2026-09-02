#!/usr/bin/env python3
"""Census of the live lesson estate on the RULED spine (ORDER VB-RUN12A).

This is the run-11 census with two keying defects fixed. It is put in the repo
rather than left in a scratchpad because the defects it fixes cost this run its
whole wave-4 build, and the next run should not re-derive them.

THE RULED KEYING is _sownb/CALENDAR_2026_27.json, "Matt's confirmed dates, ORDER
VB-RUN11F": Aut1 Wn -> n, Aut2 -> 8+n, Spr1 -> 15+n, Spr2 -> 21+n, Sum1 -> 26+n,
Sum2 -> 33+n. The same file records the previous mapping under a key named
oldSpine, and VB_STATE spine_run11.mapping records the ruled one as ruled.

FIX 1  the _A([12])_ filename rule added the OLD Autumn 2 offset (7) while the
       term table three lines above it added the ruled one (8). 55 decks read a
       different week depending on which rule fired first.

FIX 2  CALENDAR_SPINE.json's absoluteWeek column is DERIVED from the old offsets
       -- all 897 cells with a value fit them exactly -- and was being used as a
       deck's ruled week without conversion. Of the 55 decks carrying both a
       declared week and a cited cell, 30 disagreed, every one by exactly one
       week. _ruled() converts it.

WHAT IS STILL NOT SETTLED, and why this tool does not close the horizon on its
own: with both fixes the path reading gives 231 covered and the content reading
236. Reconciling the last five means re-deriving the Science trio rule and the
D-H path fallback on the ruled keying. Until that is done, do NOT take an
"uncovered" slot from here as a licence to build. Use the cell-claim check,
which depends on no keying at all: does any existing deck already claim this
workbook cell? See _sownb/vb/evidence/run12/COVERAGE_INSTRUMENT_CONTESTED.json.

Run from the repository root. Writes /tmp/census_v4.json for coverage_spine.py.
"""
import json,re,os,hashlib,collections,subprocess,sys
S=json.load(open('_sownb/CALENDAR_SPINE.json'))
prior={e['path']:e for e in S['existingHtml']}
cellweek={}  # (lane, ref)->absweek ; and subject
cellsub={}
bare=collections.defaultdict(set)   # (lane,subject,cellnum) -> {absweek}
def _ruled(o):
    # CALENDAR_SPINE absoluteWeek is DERIVED from the old offsets (897/897 fit them).
    # Aut2, Spr1, Spr2 and Sum2 each moved +1 under the VB-RUN11F ruling.
    return None if not isinstance(o,int) else (o+1 if (8<=o<=26 or 33<=o<=39) else o)
for c in S['workbookCells']:
    cellweek[c['reference']]=_ruled(c.get('absoluteWeek')); cellsub[c['reference']]=(c.get('lane'),c.get('subject'))
    m=re.match(r"'(BUILD|GROW|LAUNCH) Weekly - (?:Autumn|Spring|Summer)'!C(\d+)",c['reference'])
    if m and c.get('absoluteWeek'): bare[(m.group(1),c.get('subject'),int(m.group(2)))].add(_ruled(c['absoluteWeek']))
TERM={'Autumn1':0,'Autumn2':8,'Spring1':15,'Spring2':21,'Summer1':26,'Summer2':33}
roots=['BUILD_ASDAN','GROW_ASDAN','LAUNCH_ASDAN','Science_Teesside','Humanities_Teesside','Art_Teesside','Build/Slideshows','Grow/Slideshows','Launch/Slideshows']
files=subprocess.run(['bash','-c','find '+' '.join(roots)+" -name '*.html' | sort"],capture_output=True,text=True).stdout.split()
def lane_of(p):
    P=p.upper()
    if P.startswith('BUILD') or '/BUILD' in P or '/Build/' in p or 'BUILD_' in P: return 'BUILD'
    if P.startswith('GROW') or '/Grow/' in p or 'GROW_' in P: return 'GROW'
    if P.startswith('LAUNCH') or '/Launch/' in p or 'LAUNCH_' in P: return 'LAUNCH'
    return None
def subject_of(p):
    if 'ASDAN' in p: return 'ASDAN'
    if p.startswith('Science_'): return 'Science'
    if p.startswith('Humanities_'): return 'Humanities'
    if p.startswith('Art_'): return 'Art'
    return None
def path_week(p):
    parts=p.split('/'); fn=parts[-1]; d='/'.join(parts[:-1])
    m=re.search(r'(Autumn|Spring|Summer)([12])',d); base=None
    if m: base=TERM[m.group(1)+m.group(2)]
    # filename patterns
    fm=re.search(r'_A([12])_[A-Z_]*W(\d+)',fn) or re.search(r'_A([12])_W(\d+)',fn)
    if fm: return {'1':0,'2':8}[fm.group(1)]+int(fm.group(2))
    sm=re.search(r'Spring([12])_W(\d+)',fn)
    if sm: return TERM['Spring'+sm.group(1)]+int(sm.group(2))
    wm=re.search(r'(?:^|_)W(\d+)(?:[A-Z]|L\d|_|\b)',fn)
    if wm:
        n=int(wm.group(1))
        if base is None: return n
        # dir carries a term; filename W may be term-relative (<=7) or absolute (> block start)
        lo=base+1
        if n>=lo: return n          # already absolute
        return base+n
    return None
def content_week(p,txt):
    out={}
    m=re.search(r'"week"\s*:\s*(\d+)',txt)
    if m: out['manifestWeek']=int(m.group(1))
    m=re.search(r'"placement"\s*:\s*"([^"]*)"',txt)
    if m: out['placement']=m.group(1)
    refs=set(re.findall(r"'(?:BUILD|GROW|LAUNCH) Weekly - (?:Autumn|Spring|Summer)'!C\d+",txt))
    wk=set()
    for r in refs:
        w=cellweek.get(r)
        if w: wk.add(w)
    if refs: out['cells']=sorted(refs); out['cellWeeks']=sorted(wk)
    # The W8-W13 / W14-W15 chassis cites its cell as a screen chip, "\U0001F4CD C44 only",
    # with no sheet name. A bare number is ambiguous across terms in general (253 of 558
    # keys are), so it is resolved ONLY when (lane, subject, number) maps to exactly one
    # absolute week in the spine. Anything ambiguous stays unresolved and is reported.
    chips=set(int(x) for x in re.findall(r'\U0001F4CD\s*C(\d+)\b',txt))
    if chips:
        out['chipCells']=sorted('C%d'%c for c in chips)
        res=set()
        for c in chips:
            cand=bare.get((lane_of(p),subject_of(p),c),set())
            if len(cand)==1: res|=cand
            else: out.setdefault('chipAmbiguous',[]).append('C%d'%c)
        if res: out['chipWeeks']=sorted(res)
    m=re.search(r'Week\s+(\d+)\s*·',txt)
    if m: out['labelWeek']=int(m.group(1))
    m=re.search(r'(Aut|Spr|Sum)([12])\s*·\s*W(\d+)',txt)
    if m: out['termLabel']=m.group(0); out['termLabelAbs']=TERM[{'Aut':'Autumn','Spr':'Spring','Sum':'Summer'}[m.group(1)]+m.group(2)]+int(m.group(3))
    return out
rows=[]
for p in files:
    b=open(p,'rb').read(); txt=b.decode('utf-8','replace'); sha=hashlib.sha256(b).hexdigest()
    pr=prior.get(p)
    surface = pr['surface'] if pr else ('lesson' if (txt.count('class="slide')>=9 or 'data-mbm-guide' in txt) and 'START_HERE' not in p and 'index' not in p.lower() else 'support')
    cw=content_week(p,txt)
    cweek = cw.get('cellWeeks',[None])[0] if len(cw.get('cellWeeks',[]))==1 else None
    if cweek is None and len(cw.get('chipWeeks',[]))==1: cweek=cw['chipWeeks'][0]
    if cweek is None: cweek = cw.get('termLabelAbs') or cw.get('manifestWeek')
    if cw.get('placement','').startswith('enrichment'): cweek='ENRICHMENT'
    rows.append({'path':p,'lane':lane_of(p),'subject':subject_of(p),'surface':surface,'surfaceSource':'spine' if pr else 'heuristic',
        'pathWeek':path_week(p),'contentWeek':cweek,'content':cw,'sha256':sha,
        'priorPathReading':pr['pathReading'] if pr else None,'priorContentReading':pr['contentReading'] if pr else None,
        'priorStatus':pr['spineStatus'] if pr else 'NEW-SINCE-SPINE','blobChanged':(pr['blobSha256']!=sha) if pr else None})
json.dump(rows,open('/tmp/census_v4.json','w'),indent=0)
les=[r for r in rows if r['surface']=='lesson']
print('files',len(rows),'lessons',len(les),'support',len(rows)-len(les),'new-since-spine',sum(1 for r in rows if r['priorStatus']=='NEW-SINCE-SPINE'),'blobChanged',sum(1 for r in rows if r['blobChanged']))
print(collections.Counter((r['lane'],r['subject']) for r in les))
print('== path vs prior pathReading disagreements (unchanged blobs)')
for r in les:
    if r['priorPathReading'] is not None and r['pathWeek']!=r['priorPathReading']: print('  ',r['pathWeek'],r['priorPathReading'],r['path'])
print('== path vs content disagreements')
for r in les:
    if r['contentWeek'] not in (None,r['pathWeek']): print('  ',r['pathWeek'],r['contentWeek'],r['priorStatus'],r['path'])
print('== lessons with no path week')
for r in les:
    if r['pathWeek'] is None: print('  ',r['path'],r['contentWeek'])
