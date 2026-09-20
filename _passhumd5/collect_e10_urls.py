#!/usr/bin/env python3
"""HUM-D5 A3 E10 - enumerate every distinct URL. Reads (a) href/src/url()
attributes in every .html under ROOT (lessons, cards, START_HERE,
Sources_and_checks, Review_record, both SoWs), (b) http(s) strings inside
every text unit of TEXT_INDEX.jsonl (so DOCX/PPTX/PDF/config carry too),
(c) docx/pptx relationship targets (hyperlinks live in rels, not text).
Writes one row per distinct URL with every lesson/surface it occurs on."""
import json, re, sys, os, zipfile, collections
ROOT, IDX, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
URL = re.compile(r'https?://[^\s"\'<>)\]}]+')
ATTR = re.compile(r'(?:href|src|data-src|poster|content)\s*=\s*["\']([^"\']+)["\']', re.I)
where = collections.defaultdict(set); kinds = collections.defaultdict(set)
files_seen = {'html':0,'docx':0,'pptx':0,'index_rows':0}
def clean(u): return u.rstrip('.,;:')
for dp,_,fs in os.walk(ROOT):
    for fn in fs:
        p=os.path.join(dp,fn); rel=os.path.relpath(p,ROOT)
        if fn.endswith('.html'):
            files_seen['html']+=1
            s=open(p,encoding='utf-8',errors='replace').read()
            for m in ATTR.finditer(s):
                v=m.group(1)
                if v.startswith(('http://','https://')): where[clean(v)].add(rel); kinds[clean(v)].add('html-attr')
            for m in URL.finditer(s): where[clean(m.group(0))].add(rel); kinds[clean(m.group(0))].add('html-text')
        elif fn.endswith(('.docx','.pptx')):
            files_seen['docx' if fn.endswith('.docx') else 'pptx']+=1
            try:
                z=zipfile.ZipFile(p)
                for n in z.namelist():
                    if n.endswith('.rels'):
                        for m in re.finditer(r'Target="(https?://[^"]+)"', z.read(n).decode('utf-8','replace')):
                            where[clean(m.group(1))].add(rel); kinds[clean(m.group(1))].add('office-rel')
            except zipfile.BadZipFile: pass
for line in open(IDX,encoding='utf-8'):
    o=json.loads(line); files_seen['index_rows']+=1
    for m in URL.finditer(o['text']):
        u=clean(m.group(0)); where[u].add(f"{o['lesson_id']}/{o['surface']}"); kinds[u].add('index-text')
rows=[{'url':u,'occurrences':len(w),'kinds':sorted(kinds[u]),'where':sorted(w)[:8]} for u,w in sorted(where.items())]
json.dump({'scope':{'root':ROOT,'index':IDX,**files_seen},'distinct_urls':len(rows),'rows':rows},open(OUT,'w'),indent=1)
print('SCOPE:',files_seen); print('distinct URLs:',len(rows))
hosts=collections.Counter(re.sub(r'^https?://([^/]+).*$',r'\1',r['url']) for r in rows)
for h,c in hosts.most_common(40): print(f'  {c:4d} {h}')
