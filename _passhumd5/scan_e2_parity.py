#!/usr/bin/env python3
"""HUM-D5 A3 E2 - cross-surface parity per lesson.
Reference = the lesson HTML config (TEXT_INDEX rows surface=config). Fields:
title, outcome, key words + definitions (words[n][0/1]), evidence cards
(cards[n].title/.text), the two check questions and answers (q, a, mq, ma).
Compared surfaces: Editable_Pack.docx, Editable_Slides.pptx (+ :notes),
Pupil_Resources.html, Teacher_Notes.docx, Knowledge_Organiser.html,
Model_Transcript.txt. PDFs are renderings of the html/docx and are not
scored twice.
Measure per field x surface, on normalised text (case, whitespace, curly
quotes/dashes folded): PRESENT (exact substring), PARTIAL (>=60% of the
field's word 3-grams occur on the surface but not the whole string: a
near-miss = a DISAGREEMENT to report, with the closest surface unit quoted),
ABSENT (<60%, or the field is too short (<7 words) for a 3-gram near-miss to
mean anything: the surface does not carry the field - reported, not a
disagreement by itself: answers are meant to be absent from pupil surfaces).
Punctuation is folded before comparing: "Book or place?" on the config and
"D Book or place" on the DOCX heading are the same words.
Prints its search scope."""
import json, re, sys, collections, difflib
IDX, OUT = sys.argv[1], sys.argv[2]
SURF=['Editable_Pack.docx','Editable_Slides.pptx','Editable_Slides.pptx:notes','Pupil_Resources.html','Teacher_Notes.docx','Knowledge_Organiser.html','Model_Transcript.txt']
def norm(s):
    s=s.lower().replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('–','-').replace('—','-').replace('…','...')
    s=re.sub(r"[^a-z0-9' ]+",' ',s)          # punctuation folded: a dropped '?' or '-' on a DOCX heading is not a disagreement
    s=re.sub(r'\s+',' ',s).strip(); return s
def grams(s,n=3):
    w=re.findall(r"[a-z0-9']+",s); return set(tuple(w[i:i+n]) for i in range(max(0,len(w)-n+1))) or ({tuple(w)} if w else set())
cfg=collections.defaultdict(dict); text=collections.defaultdict(lambda: collections.defaultdict(list))
scope={'index':IDX,'rows':0,'lessons':set(),'surfaces_seen':collections.Counter()}
for line in open(IDX,encoding='utf-8'):
    o=json.loads(line); scope['rows']+=1; lid=o['lesson_id']
    if o['surface']=='config':
        L=o['locator']
        if L in ('title','outcome','q','a','mq','ma') or re.match(r'words\[\d+\]\[[01]\]$',L) or re.match(r'cards\[\d+\]\.(title|text)$',L):
            cfg[lid][L]=o['text']; scope['lessons'].add(lid)
    elif o['surface'] in SURF:
        text[lid][o['surface']].append(o['text']); scope['surfaces_seen'][o['surface']]+=1
results=[]; counts=collections.Counter(); disagreements=[]
for lid in sorted(cfg):
    joined={s:' | '.join(norm(t) for t in text[lid].get(s,[])) for s in SURF}
    gsets={s:grams(joined[s]) for s in SURF}
    absent_surfaces=[s for s in SURF if not text[lid].get(s)]
    for field,val in sorted(cfg[lid].items()):
        nv=norm(val)
        if len(nv)<4: continue
        row={'lesson_id':lid,'field':field,'value':val[:160]}
        for s in SURF:
            if not text[lid].get(s): row[s]='SURFACE ABSENT'; counts[(s,'surface_absent')]+=1; continue
            if nv in joined[s]: row[s]='PRESENT'; counts[(s,'present')]+=1; continue
            g=grams(nv)
            cov=len(g&gsets[s])/len(g) if g else 0
            if cov>=0.6 and len(g)>=5:            # short strings share 3-grams by chance; need >=5 grams (>=7 words) to call a near-miss
                units=[norm(t) for t in text[lid][s]]
                best=difflib.get_close_matches(nv,units,n=1,cutoff=0.3)
                row[s]=f'PARTIAL {cov:.2f}'; counts[(s,'partial')]+=1
                disagreements.append({'lesson_id':lid,'field':field,'surface':s,'coverage':round(cov,2),'config':val[:220],'surface_text':(best[0] if best else '')[:220]})
            else: row[s]='ABSENT'; counts[(s,'absent')]+=1
        results.append(row)
scope['lessons']=len(scope['lessons']); scope['surfaces_seen']=dict(scope['surfaces_seen'])
json.dump({'scope':scope,'surfaces':SURF,'rows':results,'disagreements':disagreements,'counts':{f'{k[0]}::{k[1]}':v for k,v in counts.items()}},open(OUT,'w'),indent=1,ensure_ascii=False)
print('SCOPE: rows',scope['rows'],'lessons with config fields',scope['lessons'],'field rows',len(results))
print(f"{'surface':28s} {'present':>8s} {'partial':>8s} {'absent':>8s} {'no-surf':>8s}")
for s in SURF: print(f"{s:28s} {counts[(s,'present')]:8d} {counts[(s,'partial')]:8d} {counts[(s,'absent')]:8d} {counts[(s,'surface_absent')]:8d}")
print('DISAGREEMENTS (partial matches):',len(disagreements))
byf=collections.Counter((d['field'].split('[')[0],d['surface']) for d in disagreements)
for k,v in sorted(byf.items(),key=lambda x:-x[1])[:30]: print('  ',v,k)
for d in disagreements[:25]: print(f"  {d['lesson_id']} {d['field']} @{d['surface']} cov={d['coverage']}\n      cfg: {d['config'][:150]}\n      srf: {d['surface_text'][:150]}")
