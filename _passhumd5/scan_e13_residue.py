#!/usr/bin/env python3
"""HUM-D5 A3 E13 - personal data and residue.
Scans EVERY text unit in TEXT_INDEX.jsonl (all 20 surfaces, 120 lessons, both
SoWs) for: emails, phone numbers, build-machine paths, tool artefacts
(*.ndjson, *.jsonl), 'review copy', TODO/TBC/FIXME/XXX, lorem, NaN/undefined/
null-as-text, [object Object], template braces, and staff/pupil-name
candidates (capitalised Firstname Surname pairs that are not on the allow
list). Names are REPORTED for reading, never auto-scored: a scan cannot tell a
historical figure from a pupil.  Prints its search scope."""
import json, re, sys, collections
IDX = sys.argv[1]; OUT = sys.argv[2]
P = {
 'email':      re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
 'phone':      re.compile(r'(?<![\d/.-])(?:\+44\s?\d{2,4}|\(?0\d{3,4}\)?)[\s-]?\d{3,4}[\s-]?\d{3,4}(?![\d/.-])'),
 'path':       re.compile(r'(?:/home/|/Users/|/tmp/|/mnt/|/var/|[A-Z]:\\\\|C:\\)[\w./\\-]*'),
 'artefact':   re.compile(r'\b[\w-]+\.(?:ndjson|jsonl|pyc|log)\b'),
 'review_copy':re.compile(r'\breview copy\b', re.I),
 'todo':       re.compile(r'\b(?:TODO|TBC|TBD|FIXME|XXX|PLACEHOLDER)\b'),
 'lorem':      re.compile(r'\blorem ipsum\b|\bdolor sit amet\b', re.I),
 'nan_undef':  re.compile(r'(?<![\w.])(?:NaN|undefined|null|\[object Object\])(?![\w.])'),
 'template':   re.compile(r'\{\{[^}]*\}\}|\$\{[^}]*\}|<%[^%]*%>'),
}
ALLOW_NAMES = {'Made by Matt','Matt Roper'}  # R14: the one permitted real person + brand line
NAME = re.compile(r"\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b")
STOP = {'The','This','That','These','Those','Your','Their','What','When','Where','Which','Who','How','Why','Key','Word','Step','Stage','Week','Term','Autumn','Spring','Summer','Lesson','Pupil','Teacher','Standard','Supported','Stretch','Made','World','Views','Knowledge','Organiser','Scheme','Work','Check','Evidence','Source','Sources','Print','Review','Record','Model','Transcript','Data','Editable','Pack','Slides','Resources','Notes','Save','Reveal','Next','Back','Play','Pause','Hide','Show','Open','Close','Exit','Task','Arrival','Method','Answer','Answers','Reflection','Support','Challenge','Help','Bank','Cards','Card','Route','Routes','Level','Timer','Tools','Word','Words','Note','Read','Look','Think','Write','Talk','Ask','Say','Tell','Point','Choose','Compare','Explain','Describe','Name','Give','Use','Find','Match','Sort','Decide','Sequence','Order','List','Yes','New','Old','First','Second','Third','Last','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','North','South','East','West','United','Kingdom','Great','Britain','England','Scotland','Wales','Northern','Ireland','British','Middle','East','Ancient','Modern','Early','Late','Roman','Greek','Islam','Christian','Jewish','Muslim','Hindu','Sikh','Buddhist','Humanist','Humanism','Remembrance','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','January','February','March','April','May','June','July','August','September','October','November','December','Holy','Guru','Granth','Sahib','Bar','Bat','Mitzvah','Ordnance','Survey','Natural','Earth','Open','Street','Map','Census','Office','National','Statistics','Health','Service','Royal','Society','Museum','Library','University','College','School','Teesside','Middlesbrough','Stockton','Hartlepool','Redcar','Darlington','Durham','Newcastle','York','London','Paris','Berlin','Rome','Athens','Cairo','Delhi','Mumbai','Tokyo','Beijing','Sydney','Kingston','Windrush','Empire','Commonwealth','Second','First','War','Wars','Poppy','Cenotaph','Menorah','Torah','Bible','Gospel','Quran','Hajj','Diwali','Hanukkah','Ramadan','Eid','Easter','Christmas','Lent','Advent','Passover','Shabbat','Sabbath','Grace','Faith','Hope','Love','Peace','Justice','Truth'}
scope={'index':IDX,'rows':0,'lessons':set(),'surfaces':set()}
hits=collections.defaultdict(list); names=collections.Counter(); name_where={}
for line in open(IDX,encoding='utf-8'):
    o=json.loads(line); scope['rows']+=1; scope['lessons'].add(o['lesson_id']); scope['surfaces'].add(o['surface'])
    t=o['text']
    for k,rx in P.items():
        for m in rx.finditer(t):
            hits[k].append({'lesson_id':o['lesson_id'],'pack':o['pack'],'surface':o['surface'],'locator':o['locator'],'match':m.group(0),'context':t[max(0,m.start()-50):m.end()+50]})
    for m in NAME.finditer(t):
        a,b=m.group(1),m.group(2)
        if a in STOP or b in STOP: continue
        full=f'{a} {b}'
        if full in ALLOW_NAMES: continue
        names[full]+=1
        name_where.setdefault(full,{'lesson_id':o['lesson_id'],'surface':o['surface'],'context':t[max(0,m.start()-60):m.end()+60]})
scope['lessons']=len(scope['lessons']); scope['surfaces']=sorted(scope['surfaces'])
out={'scope':scope,'hits':{k:v for k,v in hits.items()},'hit_counts':{k:len(v) for k,v in hits.items()},
     'name_candidates':[{'name':n,'count':c,**name_where[n]} for n,c in names.most_common()]}
json.dump(out,open(OUT,'w'),indent=1,ensure_ascii=False)
print('SCOPE: rows',scope['rows'],'lessons',scope['lessons'],'surfaces',len(scope['surfaces']))
for k in P: print(f'  {k:12s} {len(hits[k])}')
print('  name candidates (distinct):',len(names))
for n,c in names.most_common(40): print(f'    {c:4d} {n}  <- {name_where[n]["lesson_id"]}/{name_where[n]["surface"]}')
