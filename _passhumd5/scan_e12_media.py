#!/usr/bin/env python3
"""HUM-D5 A3 E12 - media rights.
(1) Every standalone jpg/png/svg under ROOT: which HTML references it, and
    whether that surface (or the lesson config) marks it authored or credits it.
(2) Every <img> / inline <svg> in every *_Lesson.html and Pupil/KO html: the
    enclosing <figure>'s <figcaption>; a PHOTOGRAPH (jpeg payload or .jpg)
    must carry licence + author + a source URL ON THAT SURFACE; any other
    image must carry a credit or an authored mark.
(3) Wherever a map renders (config map_mode != none, or an <svg> with an
    OSM/Natural Earth marker), the credit line must be on the same surface:
    "© OpenStreetMap contributors" for OSM-derived maps, "Natural Earth" for
    world maps.
Prints its search scope."""
import os, re, sys, json, collections, base64
ROOT, OUT = sys.argv[1], sys.argv[2]
IMG_EXT=('.jpg','.jpeg','.png','.svg','.webp','.gif')
LIC=re.compile(r'CC[ -]BY[A-Z0-9 .\-]*|CC0|Public domain|OGL|Open Government Licence|©|Crown copyright',re.I)
URLRX=re.compile(r'https?://\S+')
AUTHORED=re.compile(r'\b(authored|original (?:diagram|drawing|illustration|graphic|map)|made for this (?:pack|lesson)|Made by Matt)\b',re.I)
html_files=[]; img_files=[]
for dp,_,fs in os.walk(ROOT):
    for fn in fs:
        p=os.path.join(dp,fn)
        if fn.lower().endswith('.html'): html_files.append(p)
        elif fn.lower().endswith(IMG_EXT): img_files.append(p)
html_text={p:open(p,encoding='utf-8',errors='replace').read() for p in html_files}
# (1) standalone files
standalone=[]
for ip in sorted(img_files):
    bn=os.path.basename(ip); rel=os.path.relpath(ip,ROOT)
    refs=[]
    for hp,t in html_text.items():
        if bn in t:
            # find the reference and any credit/authored mark within 600 chars after it
            i=t.find(bn); win=t[i:i+900]
            refs.append({'html':os.path.relpath(hp,ROOT),'credited':bool(LIC.search(win)),'authored':bool(AUTHORED.search(win))})
    standalone.append({'file':rel,'referenced_by':len(refs),'any_credit_or_authored':any(r['credited'] or r['authored'] for r in refs),'refs':refs[:4]})
# (2) inline images in lesson-facing HTML
inline=[]
FIG=re.compile(r'<figure\b[^>]*>(.*?)</figure>',re.S|re.I)
IMGTAG=re.compile(r'<img\b[^>]*>',re.I)
for hp,t in html_text.items():
    rel=os.path.relpath(hp,ROOT); base=os.path.basename(hp)
    if not (base.endswith('_Lesson.html') or base in ('Pupil_Resources.html','Knowledge_Organiser.html')): continue
    figs=FIG.findall(t)
    in_fig=set()
    for f in figs:
        for m in IMGTAG.finditer(f):
            in_fig.add(m.group(0))
            src=re.search(r'src="([^"]*)"',m.group(0)); src=src.group(1) if src else ''
            photo=src.startswith('data:image/jpeg') or src.lower().endswith(('.jpg','.jpeg'))
            cap=re.search(r'<figcaption\b[^>]*>(.*?)</figcaption>',f,re.S|re.I); cap=re.sub(r'<[^>]+>','',cap.group(1)).strip() if cap else ''
            alt=re.search(r'alt="([^"]*)"',m.group(0)); alt=alt.group(1) if alt else ''
            inline.append({'html':rel,'kind':'photo' if photo else ('data-png' if src.startswith('data:image/png') else ('data-svg' if src.startswith('data:image/svg') else 'file:'+src[:60])),
              'caption':cap[:200],'alt':alt[:120],'licence':bool(LIC.search(cap)),'url_in_caption':bool(URLRX.search(cap)),
              'author_like':bool(re.search(r'·\s*[A-Z][a-z]+(?: [A-Z][a-z]+)?\s*·',cap)) or bool(re.search(r'\b(?:by|photo|author)\b',cap,re.I)),
              'authored':bool(AUTHORED.search(cap+' '+alt))})
    for m in IMGTAG.finditer(t):
        if m.group(0) in in_fig: continue
        src=re.search(r'src="([^"]*)"',m.group(0)); src=src.group(1) if src else ''
        alt=re.search(r'alt="([^"]*)"',m.group(0)); alt=alt.group(1) if alt else ''
        ctx=t[max(0,m.start()-300):m.end()+300]
        inline.append({'html':rel,'kind':('photo' if src.startswith('data:image/jpeg') else 'no-figure:'+src[:40]),'caption':'','alt':alt[:120],'licence':bool(LIC.search(ctx)),'url_in_caption':False,'author_like':False,'authored':bool(AUTHORED.search(ctx))})
# (3) maps
maps=[]
for hp,t in html_text.items():
    base=os.path.basename(hp)
    if not base.endswith('_Lesson.html'): continue
    lid=base.replace('_Lesson.html','')
    mm=re.search(r'"map_mode"\s*:\s*"([^"]*)"',t) or re.search(r"map_mode\s*:\s*'([^']*)'",t)
    mode=mm.group(1) if mm else None
    osm_marker=bool(re.search(r'openstreetmap|tile\.osm|osm-derived|\bOSM\b',t,re.I))
    ne_marker=bool(re.search(r'naturalearth|Natural Earth',t,re.I))
    maps.append({'lesson_id':lid,'map_mode':mode,'osm_marker':osm_marker,'osm_credit_visible':'© OpenStreetMap contributors' in t or '&copy; OpenStreetMap contributors' in t,
                 'ne_marker':ne_marker,'ne_credit':bool(re.search(r'Natural Earth',t))})
res={'scope':{'root':ROOT,'html_files':len(html_files),'image_files':len(img_files),'lesson_html':sum(1 for p in html_files if p.endswith('_Lesson.html'))},
     'standalone':standalone,'inline':inline,'maps':maps}
json.dump(res,open(OUT,'w'),indent=1,ensure_ascii=False)
print('SCOPE:',res['scope'])
print('standalone files:',len(standalone),'unreferenced:',sum(1 for s in standalone if not s['referenced_by']),'referenced but no credit/authored mark near the reference:',sum(1 for s in standalone if s['referenced_by'] and not s['any_credit_or_authored']))
c=collections.Counter(i['kind'].split(':')[0] for i in inline); print('inline images by kind:',dict(c))
ph=[i for i in inline if i['kind']=='photo']
print('photos:',len(ph),'with licence:',sum(i['licence'] for i in ph),'with author-like:',sum(i['author_like'] for i in ph),'with URL in caption:',sum(i['url_in_caption'] for i in ph))
oth=[i for i in inline if i['kind']!='photo']
print('non-photo inline:',len(oth),'credited or authored:',sum(i['licence'] or i['authored'] for i in oth),'caption present:',sum(bool(i['caption']) for i in oth))
mc=collections.Counter((m['map_mode'],m['osm_marker'],m['osm_credit_visible'],m['ne_marker']) for m in maps)
print('maps (map_mode, osm_marker, osm_credit, ne_marker) -> lessons:'); [print('  ',k,v) for k,v in sorted(mc.items(),key=str)]
print('--- photo captions (distinct) ---'); [print('  ',k) for k in sorted(set(i['html'].split('/')[-2]+' :: '+i['caption'] for i in ph))]
print('--- non-photo without any credit/authored (first 15) ---'); [print('  ',i['html'][-60:],i['kind'],'| cap:',i['caption'][:80],'| alt:',i['alt'][:60]) for i in [x for x in oth if not (x['licence'] or x['authored'])][:15]]
