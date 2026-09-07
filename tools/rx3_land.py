#!/usr/bin/env python3
"""RX3 P3 — land a classic-chassis lesson from the 33-pack into the Lessons tree (one writer, reproducible).

Usage: rx3_land.py --pack <pack root> --repo <worktree> --admission <_rx2/ADMISSION.md> --ids a,b,c [--dry] [--json out]

Per lesson (verdict from the rx2 admission table; STOP rows are R3 ADD-BESIDE):
  REPLACE            → the pack HTML lands at the pack's originalPath (same cell, same file the pack re-cut).
  ADD / ADD-BESIDE   → a new file beside the donor: <donor prefix up to the week token>_<Title_Slug>_Classic.html.
Transformations (all measured and printed; every replacement must match exactly the expected count):
  R1  belonging: the photoreal composite becomes the flat SVG scene from tools/rx3_scenes.py (data URI ≤ 40 KB); alt = scene + decision.
  3.3 art: Flow/Crossing become one external webp pair under Art_Teesside/assets/ (q82, ≤ 300 KB each), referenced relatively by both lessons.
  3.2 NAV-1 way-home + splash (estate bytes from _next6/tools/n7_chassis_furniture.py / nav1_splash.html, print-hidden);
      PH-3 guidance: every .ta-section gains data-mbm-guide="staff" and the estate toggle (bytes read from _eca1/tools/guidepatch.js);
      canonical link; a single <h1> (the other two become <h2 class="slide-h1"> with the donor h1 rule copied); /hud.js by donor parity;
      T2-4 learner confirmation on ASDAN surfaces (block bytes from _next6/tools/n2_learner_confirmation.py, inside #print-area);
      the closure sentinel heading where the donor carries it (so _eca1 sentinel sets stay identical).
  Family manifest: REPLACE updates sha256/bytes where the row carries them; ADD appends a row cloned from the donor's row.
"""
import argparse,json,re,os,sys,hashlib,shutil,importlib.util,html
ap=argparse.ArgumentParser();ap.add_argument('--pack',required=True);ap.add_argument('--repo',required=True);ap.add_argument('--admission',required=True)
ap.add_argument('--ids',required=True);ap.add_argument('--beside',default='');ap.add_argument('--dry',action='store_true');ap.add_argument('--json');ap.add_argument('--img',default='/tmp/claude-0/-home-user-Lessons/66c1d222-c1e7-597f-9ba2-ca04f6d2c4f3/scratchpad/img')
a=ap.parse_args();PACK=a.pack;REPO=a.repo
sys.path.insert(0,os.path.join(REPO,'tools'));import rx3_scenes
manifest={e['id']:e for e in json.load(open(os.path.join(PACK,'manifest.json')))}
adm=open(a.admission,encoding='utf-8').read()
verdict={m[0]:('ADD-BESIDE(R3)' if m[1]=='STOP' else m[1]) for m in re.findall(r'\| (\w+) \| \w+ \| [^|]+ \| [^|]+ \| \d+ \| [^|]+ \| [^|]* \| [^|]* \| \*\*(\w+)\*\* \|',adm)}
# A REPLACE target whose bytes another current lesson set pins by digest (the David Humanities cover pack records its 30
# existing routes' sha256 and its CI asserts them) is never overwritten (standing rule): it lands beside instead, and the
# existing lesson keeps its standing. Ids come from --beside or RX3_BESIDE (comma-separated).
for _lid in [x for x in (a.beside or os.environ.get('RX3_BESIDE','')).split(',') if x]:
    assert verdict.get(_lid)=='REPLACE', 'beside override only applies to a REPLACE verdict: '+_lid
    verdict[_lid]='ADD-BESIDE(pinned)'
def sha(b):return hashlib.sha256(b).hexdigest()
def once(s,old,new,label,count=1):
    c=s.count(old)
    if c!=count: raise SystemExit(f'{label}: expected {count} match(es), found {c}: {old[:70]!r}')
    return s.replace(old,new)
# --- estate bytes, never retyped -----------------------------------------------------------------
n7=open(os.path.join(REPO,'_next6/tools/n7_chassis_furniture.py'),encoding='utf-8').read()
N7_OPEN,N7_CLOSE='<!--n6-nav1:v1-->','<!--/n6-nav1-->'
N7_CSS=eval(re.search(r"CSS = \((.*?)\)\n",n7,re.S).group(1).replace('\n','').strip().rstrip(')'))  # the tuple of adjacent string literals
N7_WAYHOME='<a class="mbmhome" href="%sindex.html" aria-label="Back to the Lessons catalogue">← Lessons</a>'
SPLASH=open(os.path.join(REPO,'_next6/tools/nav1_splash.html'),encoding='utf-8').read().strip()
gp=open(os.path.join(REPO,'_eca1/tools/guidepatch.js'),encoding='utf-8').read()
GP_STYLE=re.search(r"const STYLE = '(.*?)';\n",gp,re.S).group(1).replace("\\'","'")
GP_BUTTON=re.search(r"const BUTTON = '(.*?)';\n",gp,re.S).group(1)
GP_SCRIPT=re.search(r"const SCRIPT = `(.*?)`\.replace",gp,re.S).group(1).replace("<\\/script>","</script>")
assert GP_STYLE.startswith('<style id="mbm-guide-css">') and GP_SCRIPT.startswith('<!--mbm-guide:v1-->')
n2spec=importlib.util.spec_from_file_location('n2',os.path.join(REPO,'_next6/tools/n2_learner_confirmation.py'));n2=importlib.util.module_from_spec(n2spec)
try: n2spec.loader.exec_module(n2)
except SystemExit: pass
n6mspec=importlib.util.spec_from_file_location('n6m',os.path.join(REPO,'_next6/tools/n6m_guide_toggle.py'));n6mmod=importlib.util.module_from_spec(n6mspec);n6mspec.loader.exec_module(n6mmod);N6M_PAYLOAD=n6mmod.PAYLOAD
CLOSURE='What I said, and what it changed'
def h1_rule(s):
    m=re.search(r'(?<![\w.#-])h1\s*\{([^}]*)\}',s)
    return m.group(1) if m else None
def slug(t):return re.sub(r'[^A-Za-z0-9]+','_',t).strip('_')
CAL=json.load(open(os.path.join(REPO,'_sownb/CALENDAR_2026_27.json')))
def abs_week(period):
    # the pack's own placement label ("Autumn 2 · Week 4") mapped through the ruled calendar (Aut1·Wn → n, Aut2·Wn → 8+n); never a filename
    term,wk=period.split('·');n=int(wk.strip().split()[-1]);rule=CAL['mapping']['Aut1·Wn' if term.strip()=='Autumn 1' else 'Aut2·Wn']
    return n if rule=='n' else int(rule.split('+')[0])+n
def family_prefix(fname):
    # the donor's family prefix is the part of its basename before the family's week token; nothing about a week is read from it
    return fname.split('_W')[0]
def land(lid):
    e=manifest[lid];v=verdict[lid];donor=e['originalPath'];fam_dir=os.path.dirname(donor)
    src=open(os.path.join(PACK,'lessons',e['file']),encoding='utf-8').read();rec={'id':lid,'verdict':v,'donor':donor,'pack_sha256':sha(src.encode()),'pack_sha_matches_manifest':sha(src.encode())==e['sha256']}
    if v=='REPLACE': target=donor
    else: target=os.path.join(fam_dir,family_prefix(os.path.basename(donor))+'_W'+str(abs_week(e['period']))+'_'+slug(e['title'])+'_Classic.html')
    rec['target']=target;out=src;depth='../'*target.count('/')
    dsrc=open(os.path.join(REPO,donor),encoding='utf-8').read()
    # --- images --------------------------------------------------------------------------------
    if lid=='build_humanities_belonging':
        svg=rx3_scenes.build();import urllib.parse
        uri='data:image/svg+xml;charset=utf-8,'+urllib.parse.quote(svg,safe="-_.~ :/?#[]@!$&'()*+,;=")
        assert len(uri)<=40960
        out,n0=re.subn(r'"group-activities\.png":\s*"data:image/png;base64,[^"]+"',lambda m:'"group-activities.png": '+json.dumps(uri),out,count=1);assert n0==1,'scene not substituted' 
        n=len(re.findall(r'alt="Four imagined school groups[^"]*"',out))
        out=re.sub(r'alt="Four imagined school groups[^"]*"','alt="'+html.escape(rx3_scenes.alt(),quote=True)+'"',out)
        out=out.replace('Original teaching illustration; imagined groups.','Flat illustrated scenes; imagined groups, not real pupils.')
        rec['images']={'scene_uri_chars':len(uri),'alt_replaced':n}
    if e['subject']=='Art' and ('flow.png' in out or 'crossing.png' in out):
        assets=os.path.join(REPO,'Art_Teesside/assets');os.makedirs(assets,exist_ok=True);rel=os.path.relpath(assets,os.path.join(REPO,fam_dir)).replace(os.sep,'/')
        for name in ('flow','crossing'):
            wp=os.path.join(a.img,name+'.q82.webp');dst=os.path.join(assets,name+'.webp')
            if not a.dry and not os.path.exists(dst): shutil.copy(wp,dst)
            out,n1=re.subn(r'"'+name+r'\.png":\s*"data:image/png;base64,[^"]+"','"'+name+'.png": "'+rel+'/'+name+'.webp"',out,count=1);assert n1==1,name+' not substituted' 
        rec['images']={'webp_dir':rel,'sizes':{n:os.path.getsize(os.path.join(a.img,n+'.q82.webp')) for n in ('flow','crossing')}}
    assert len(re.findall(r'data:image/png;base64,[A-Za-z0-9+/=]{70000,}',out))==0,'a data-URI image > 50 KB survived'
    # --- single h1 ------------------------------------------------------------------------------
    rule=h1_rule(out);h1s=re.findall(r'<h1\b',out);rec['h1_before']=len(h1s)
    first=out.find('<h1');rest=out[first+3:]
    rest=re.sub(r'<h1(\s[^>]*)?>(.*?)</h1>',lambda m:'<h2 class="slide-h1"'+(m.group(1) or '')+'>'+m.group(2)+'</h2>',rest,flags=re.S)
    out=out[:first+3]+rest
    if rule and 'h2.slide-h1{' not in out: out=once(out,'</style>','h2.slide-h1{'+rule.strip()+'}</style>','h1-rule',count=out.count('</style>')) if out.count('</style>')==1 else out.replace('</style>','h2.slide-h1{'+rule.strip()+'}</style>',1)
    rec['h1_after']=len(re.findall(r'<h1\b',out))
    # --- estate stage-navigation contract: the offline-pack browser check (and the estate's navigation gates) find the stage controls by
    #     button[data-nav="next"] / button[data-nav="previous"]; the pack keys its own handlers on data-action, so the attribute is additive.
    out=once(out,'<button type="button" id="next-slide" data-action="next">','<button type="button" id="next-slide" data-action="next" data-nav="next">','data-nav next')
    out=once(out,'<button type="button" id="previous-slide" data-action="previous">','<button type="button" id="previous-slide" data-action="previous" data-nav="previous">','data-nav previous')
    # --- canonical -------------------------------------------------------------------------------
    canon='<link rel="canonical" href="https://madebymatt.uk/Lessons/'+target+'">'
    out=re.sub(r'(<meta name="viewport"[^>]*>)',lambda m:m.group(1)+canon,out,count=1);rec['canonical']=out.count('rel="canonical"')
    # --- guidance (PH-3) --------------------------------------------------------------------------
    # staff guidance on the pupil-facing slides is the pack's <details class="staff-detail"> blocks; the TA Brief dialog is already
    # staff-gated (data-audience="staff", opened by its own button) and is left alone so the brief never blanks.
    ta=out.count('<details class="staff-detail">');out=out.replace('<details class="staff-detail">','<details class="staff-detail" data-mbm-guide="staff">')
    # the toggle mechanism follows the donor: its own n6m block bytes (the docked variant carries the `n6m-guide-docked` rule the
    # offline-pack census counts), else the PH-3 bytes if the donor carries those, else the estate's current n6m payload.
    n6m=re.search(r'<!--n6m-guide:v1-->.*?<!--/n6m-guide-->',dsrc,re.S)
    if n6m:
        out=once(out,'</head>',n6m.group(0)+'</head>','guide-n6m');rec['guidance_mechanism']='n6m (donor block %dB)'%len(n6m.group(0))
        # donor parity: the n6m script docks its button into `.controls .left` (44 px, in the toolbar) when that wrapper exists, and the
        # offline-pack browser check requires the docked form on every guidance route. The pack's controls bar has no wrapper, so the
        # buttons are wrapped exactly as the donor's are.
        if re.search(r'<(?:div|nav) class="controls"[^>]*>\s*<div class="left">',dsrc):
            cm=re.search(r'(<div class="controls"[^>]*>)(.*?)(</div>)',out,re.S);out=out[:cm.start()]+cm.group(1)+'<div class="left">'+cm.group(2)+'</div>'+cm.group(3)+out[cm.end():];rec['controls_left_wrap']=True
    elif '<!--mbm-guide:v1-->' in dsrc:
        out=once(out,'</head>',GP_STYLE+'</head>','guide-style')
        cm=re.search(r'(<div class="controls"[^>]*>[\s\S]*?</div>)',out);controls=cm.group(1);anchor=re.search(r'<button[^>]*data-action="ta"[^>]*>[^<]*</button>',controls)
        out=out.replace(controls,controls.replace(anchor.group(0),anchor.group(0)+GP_BUTTON),1);out=once(out,'</body>',GP_SCRIPT+'</body>','guide-script');rec['guidance_mechanism']='PH-3 (donor carries it)'
    else:
        out=once(out,'</head>',N6M_PAYLOAD+'</head>','guide-n6m-estate');rec['guidance_mechanism']='n6m (estate payload; donor has none)'
    rec['guidance_tagged']=ta
    # --- way-home + splash (n6-nav1) -----------------------------------------------------------------
    bm=re.search(r'<body\b[^>]*>',out);head=N7_OPEN+N7_CSS+(N7_WAYHOME%depth)+N7_CLOSE;tail=N7_OPEN+'<div class="n6-splash">'+SPLASH+'</div>'+N7_CLOSE
    out=out[:bm.end()]+head+out[bm.end():];out=out.replace('</body>',tail+'</body>',1);rec['wayhome_depth']=depth
    # --- hud.js by donor parity --------------------------------------------------------------------
    if '/hud.js' in dsrc and '/hud.js' not in out: out=out.replace('</body>','<script defer src="/hud.js"></script></body>',1)
    rec['hud']=out.count('/hud.js');rec['donor_hud']=dsrc.count('/hud.js')
    # --- closure sentinel where the donor carries it ---------------------------------------------------
    rec['donor_closure']=CLOSURE in dsrc
    if v=='REPLACE' and CLOSURE in dsrc and CLOSURE not in out:  # REPLACE only: the _eca1 sentinel SET must stay identical
        pa=out.find('id="print-area"');k=out.find('</div>',out.rfind('<div',0,out.find('</body>')))  # placeholder, replaced below
        # put the closure box at the end of the print area: before the print area's closing tag = the last '</div>' before '<script'
        end=out.find('<script',pa);cut=out.rfind('</div>',pa,end)
        box='<div class="pbox"><h3>'+CLOSURE+'</h3><p>________________________________________________</p></div>'
        out=out[:cut]+box+out[cut:]
    rec['closure_after']=CLOSURE in out
    # --- T2-4 learner confirmation on ASDAN surfaces ---------------------------------------------------
    if 'ASDAN' in e['subject']:  # 'ASDAN' and 'ASDAN · Enterprise' in the pack manifest
        lane='LAUNCH' if e['pathway']=='LAUNCH' else 'BUILD';blk=n2.payload(lane)
        pa=out.find('id="print-area"');end=out.find('<script',pa);cut=out.rfind('</div>',pa,end);out=out[:cut]+blk+out[cut:];rec['learner_confirmation']=len(blk)
    # --- measured print defects, fixed per lesson (each replacement asserted once; recorded in rec['print_fix']) ------------------
    PRINT_FIXES={'b2_launch_science_dna':('.print-resource:last-child,.print-sheet:last-child{break-after:auto;page-break-after:auto}',
        '#print-area .print-resource{break-after:auto;page-break-after:auto}')}  # s24: a forced break after the diagram page left page 5 blank (0 chars); measured 7→6 pages, near-blank 1→0
    if lid in PRINT_FIXES:
        anchor,add=PRINT_FIXES[lid];out=once(out,anchor,anchor+add,'print-fix');rec['print_fix']=add
    # --- write ----------------------------------------------------------------------------------------
    rec['bytes']=len(out.encode());rec['sha256']=sha(out.encode());rec['dup_ids']=sorted({i for i in re.findall(r'id="([^"]+)"',out) if out.count('id="'+i+'"')>1})
    rec['keyframes_before_after']=[src.count('@keyframes'),out.count('@keyframes')]
    if not a.dry:
        p=os.path.join(REPO,target);os.makedirs(os.path.dirname(p),exist_ok=True);open(p,'w',encoding='utf-8').write(out)
        update_manifest(e,v,target,out,rec)
    return rec
def update_manifest(e,v,target,out,rec):
    fam=os.path.join(REPO,os.path.dirname(e['originalPath']));mf=[f for f in os.listdir(fam) if re.match(r'manifest.*\.json$',f)]
    if not mf: rec['manifest']='none';return
    p=os.path.join(fam,mf[0]);m=json.load(open(p,encoding='utf-8'));dn=os.path.basename(e['originalPath'])
    # the row list is whichever top-level list holds a dict whose 'file' is the donor (families name it lessons / sequence / …)
    ls=next((v for v in (m.values() if isinstance(m,dict) else []) if isinstance(v,list) and any(isinstance(r,dict) and r.get('file')==dn for r in v)),None)
    if ls is None: rec['manifest']=mf[0]+': donor row not found in any list';return
    row=next((r for r in ls if r.get('file')==dn),None)
    if row is None: rec['manifest']=mf[0]+': donor row not found';return
    if v=='REPLACE':
        if 'sha256' in row: row['sha256']=rec['sha256']
        if 'bytes' in row: row['bytes']=rec['bytes']
        row['title']=e['title'] if 'title' in row else row.get('title');rec['manifest']=mf[0]+': row updated'
    else:
        new=json.loads(json.dumps(row));new['file']=os.path.basename(target);new['title']=e['title'];new['id']=str(row.get('id',''))+'_CLASSIC'
        if 'sha256' in new: new['sha256']=rec['sha256']
        if 'bytes' in new: new['bytes']=rec['bytes']
        if 'cells' in new and isinstance(new['cells'],list) and new['cells'] and isinstance(new['cells'][0],dict):
            new['cells']=[dict(new['cells'][0],cell=c,reference="'"+e['sow']['sheet']+"'!"+c) for c in e['sow']['cells']]
        if 'outcomes' in new: new['outcomes']=e['sow']['outcomes']
        if 'outcome' in new: new['outcome']=' '.join(e['sow']['outcomes'])
        if 'objective' in new:
            lj=re.search(r'const LESSON=(\{.*?\});const LESSON_IMAGES=',open(os.path.join(PACK,'lessons',e['file']),encoding='utf-8').read(),re.S)
            if lj: new['objective']=json.loads(lj.group(1)).get('objective',new['objective'])
        if 'week' in new: new['week']=int(re.search(r'\d+',e['period'].split('Week')[-1]).group(0))+(8 if 'Autumn 2' in e['period'] else 0) if 'Week' in e['period'] else new['week']
        new['classicPack']={'id':e['id'],'batch':e['batch'],'period':e['period'],'sow':e['sow']['cells']}
        ls.insert(ls.index(row)+1,new)
        if 'lessonCount' in m: m['lessonCount']=len(ls)
        if 'plannedLessonCount' in m: m['plannedLessonCount']=len(ls)  # the two counts move together (tools/easter/manifest_sequence.py control)
        rec['manifest']=mf[0]+': row added'
    json.dump(m,open(p,'w',encoding='utf-8'),indent=2,ensure_ascii=False);open(p,'a').write('\n')
def update_source_placement(recs):
    p=os.path.join(REPO,'tools/downloads/SOURCE_PLACEMENT.json');d=json.load(open(p,encoding='utf-8'));added=[]
    for r in recs:
        if r['target'].startswith('Science_Teesside/') and r['verdict']!='REPLACE' and r['target'] not in d['retainedAlternatives'] and r['target'] not in {x['path'] for x in d['sources']}:
            d['retainedAlternatives'].append(r['target']);added.append(r['target'])
    if added and not a.dry: json.dump(d,open(p,'w',encoding='utf-8'),indent=2,ensure_ascii=False);open(p,'a').write('\n')
    return added
recs=[land(i) for i in a.ids.split(',')]
placement_added=update_source_placement(recs)
if placement_added: print('SOURCE_PLACEMENT.json retainedAlternatives +',len(placement_added))
print(f"{'id':40s} {'verdict':14s} {'target':78s} h1 canon ta home hud clos bytes")
for r in recs: print(f"{r['id']:40s} {r['verdict']:14s} {r['target'][:78]:78s} {r['h1_after']:2d} {r['canonical']:5d} {r['guidance_tagged']:2d} {len(r['wayhome_depth'])//3:4d} {r['hud']:3d} {int(r['closure_after']):4d} {r['bytes']:7d} {r['guidance_mechanism']}")
if a.json: json.dump(recs,open(a.json,'w'),indent=1)
