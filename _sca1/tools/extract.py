#!/usr/bin/env python3
"""SCA-1 §1.4 extractor: PROSE / CODE / QUESTIONS / PROTECTED streams.
Dialects derived from bytes, not assumed:
  compact (BUILD, LAUNCH): printpack / proute / pp / pline / pidline / pentry
  hyphen  (GROW)         : print-pack / print-route / print-box / print-line / print-page
Tier panels: attribute order differs BUILD/LAUNCH vs GROW -> parsed order-independently.
"""
import re, os, json, sys, html as htmlmod, csv, glob

STYLE_RE  = re.compile(r'<style\b[^>]*>.*?</style>', re.S|re.I)
SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.S|re.I)
TAG_RE    = re.compile(r'<[^>]+>')
COMMENT_RE= re.compile(r'<!--.*?-->', re.S)
ATTR_RE   = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')

PROSE_ATTRS = ["alt","aria-label","title","data-speak-text","data-ta1","data-ta2",
               "data-title","data-label","data-hint","data-explain","data-fix",
               "placeholder","data-ta-move","data-name","data-frame"]
PROSE_ATTR_RE = re.compile(r'\b('+"|".join(map(re.escape,PROSE_ATTRS))+r')\s*=\s*"([^"]*)"', re.I)
JS_STR_RE = re.compile(r'(?<![\w$])(["\'])((?:\\.|(?!\1)[^\\\n])*)\1')

def ent(s): return htmlmod.unescape(s)
def clean(s): return re.sub(r'\s+',' ', ent(TAG_RE.sub(' ', s))).strip()

def streams(path):
    raw = open(path, encoding='utf-8', errors='replace').read()
    code = "\n".join(STYLE_RE.findall(raw)+SCRIPT_RE.findall(raw)+TAG_RE.findall(raw))
    body = COMMENT_RE.sub(' ', raw)
    attr_prose = [ent(m.group(2)) for m in PROSE_ATTR_RE.finditer(body)]
    js_prose=[]
    for sm in SCRIPT_RE.finditer(body):
        for m in JS_STR_RE.finditer(sm.group(0)):
            v=m.group(2)
            if len(v)>12 and ' ' in v and re.search(r'[A-Za-z]{3}',v) \
               and not re.match(r'^[\w./#-]+$',v) and 'http' not in v:
                js_prose.append(ent(v))
    text = TAG_RE.sub('\n', SCRIPT_RE.sub(' ', STYLE_RE.sub(' ', body)))
    vis=[l.strip() for l in ent(text).split('\n') if l.strip()]
    return raw, "\n".join(vis+attr_prose+js_prose), code, vis, attr_prose, js_prose

def find_blocks(raw, opentag_re):
    """Return (attrs, inner) for balanced <div|section ...> blocks matching opentag_re."""
    out=[]
    for m in re.finditer(opentag_re, raw):
        tagname = re.match(r'<\s*(\w+)', m.group(0)).group(1)
        i=m.end(); depth=1
        pat=re.compile(r'</?'+tagname+r'\b', re.I)
        while depth>0:
            nm=pat.search(raw,i)
            if not nm: break
            depth += -1 if raw[nm.start():nm.start()+2+len(tagname)].startswith('</') else 1
            i=nm.end()
        out.append((dict(ATTR_RE.findall(m.group(0))), raw[m.end():nm.start() if nm else len(raw)]))
    return out

QP_RE  = re.compile(r'<p[^>]*>\s*(?:<b>)?\s*(\d+)\s*·\s*([^:<]*?):?\s*(?:</b>)?\s*(.*?)</p>', re.S)
PLAIN_P= re.compile(r'<p[^>]*>(.*?)</p>', re.S)
LI_RE  = re.compile(r'<li[^>]*>(.*?)</li>', re.S)
NOISE  = re.compile(r'Non-reading route:|TA fade route:|^Fade:|Use the .* word first', re.I)

def rows_from_block(blk, base, stype, stitle, tier, surface, panel):
    rows=[]; got=False
    for qm in QP_RE.finditer(blk):
        rows.append(dict(file=base,slide_type=stype,slide_title=stitle,panel=panel,tier=tier,
            surface=surface,qnum=qm.group(1),label=clean(qm.group(2)),stem=clean(qm.group(3)))); got=True
    if not got:
        for pm in list(PLAIN_P.finditer(blk))+list(LI_RE.finditer(blk)):
            c=clean(pm.group(1))
            if len(c)>3 and not NOISE.search(c):
                rows.append(dict(file=base,slide_type=stype,slide_title=stitle,panel=panel,tier=tier,
                    surface=surface,qnum="",label="",stem=c)); got=True
    if not got:
        # bare-text containers (GROW print-box, BUILD/LAUNCH pp) carry the task with no <p>
        c=clean(blk)
        if len(c)>3 and not NOISE.search(c):
            rows.append(dict(file=base,slide_type=stype,slide_title=stitle,panel=panel,tier=tier,
                surface=surface,qnum="",label="",stem=c))
    return rows

def questions(path):
    raw=open(path,encoding='utf-8',errors='replace').read(); base=os.path.basename(path); rows=[]
    # ---- SCREEN: tier panels inside slides (attribute-order independent)
    for sattrs, seg in find_blocks(raw, r'<section class="slide"[^>]*>'):
        stype=sattrs.get('data-type',''); stitle=clean(sattrs.get('data-title',''))
        tiers=find_blocks(seg, r'<div class="tier(?:\s[^"]*)?"[^>]*data-tier[^>]*>')
        if tiers:
            for ta, blk in tiers:
                rows+=rows_from_block(blk, base, stype, stitle, ta.get('data-tier',''),
                                      "screen", ta.get('data-tier-panel',''))
        if True:
            for ta, blk in find_blocks(seg, r'<div class="(?:box task|route [smh]|route-card (?:supported|standard|stretch)|task-box)"[^>]*>'):
                rows+=rows_from_block(blk, base, stype, stitle, "", "screen", "")
    # ---- PRINT: both dialects
    for opener, dialect in ((r'<div class="(?:proute|print-route)[^"]*"[^>]*>','route'),
                            (r'<div class="(?:pp|print-box|print-section)(?:\s[^"]*)?"[^>]*>','box')):
        for pa, blk in find_blocks(raw, opener):
            cls=pa.get('class','')
            tier=next((t for t in ("supported","standard","stretch") if t in cls.lower()),"")
            rows+=rows_from_block(blk, base, "print", "print pack", tier.capitalize(), "print", dialect)
    return rows

WORDHELP_RE=re.compile(r'<span class="lw-term">(.*?)</span>.*?<span class="lw-bridge"[^>]*>(.*?)</span>',re.S)
WORDHELP2_RE=re.compile(r'class="(?:wh-term|w-term)"[^>]*>(.*?)<.*?class="(?:wh-bridge|w-bridge)"[^>]*>(.*?)<',re.S)
def wordhelp(path):
    raw=open(path,encoding='utf-8',errors='replace').read()
    out=[(clean(a),clean(b)) for a,b in WORDHELP_RE.findall(raw)]
    out+=[(clean(a),clean(b)) for a,b in WORDHELP2_RE.findall(raw)]
    return out

def targets():
    t=[]
    for p in ["Build","Grow","Launch"]:
        t+=sorted(glob.glob(f"/home/user/Lessons/Science_Teesside/{p}/v3_40min/*.html"))
    return t

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "all"
    if mode=="validate":
        for f in sys.argv[2:]:
            raw,prose,code,vis,ap,js=streams(f); qs=questions(f); wh=wordhelp(f)
            print(f"\n=== {os.path.basename(f)} ===")
            print(f"prose={len(prose)} code={len(code)} rows={len(qs)} "
                  f"screen={sum(1 for q in qs if q['surface']=='screen')} "
                  f"print={sum(1 for q in qs if q['surface']=='print')} wordhelp={len(wh)}")
            for t in ("arrival","exit"):
                sel=[q for q in qs if q['slide_type']==t]
                print(f"  -- {t}: {len(sel)} rows")
                for q in sel[:6]: print(f"     [{q['tier'] or '-':9s}] {q['qnum']:>2s} {q['label'][:18]:18s} :: {q['stem'][:74]}")
            pr=[q for q in qs if q['surface']=='print']
            print(f"  -- print: {len(pr)} rows")
            for q in pr[:4]: print(f"     [{q['tier'] or '-':9s}] {q['stem'][:84]}")
            print(f"  -- WORD HELP: {wh[:3]}")
        sys.exit(0)
    allq=[]; whall=[]
    os.makedirs("/home/user/Lessons/_sca1/streams",exist_ok=True)
    os.makedirs("/home/user/Lessons/_sca1/tables",exist_ok=True)
    for f in targets():
        raw,prose,code,vis,ap,js=streams(f)
        pw=[x for x in ("Build","Grow","Launch") if f"/{x}/" in f][0].upper()
        base=pw+"__"+os.path.basename(f)
        open(f"/home/user/Lessons/_sca1/streams/{base}.prose.txt","w").write(prose)
        open(f"/home/user/Lessons/_sca1/streams/{base}.code.txt","w").write(code)
        for q in questions(f):
            q["file"]=pw+"__"+q["file"]; allq.append(q)
        for a,b in wordhelp(f): whall.append(dict(file=base,term=a,bridge=b))
    cols=["file","slide_type","slide_title","panel","tier","surface","qnum","label","stem"]
    with open("/home/user/Lessons/_sca1/tables/questions_raw.csv","w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=cols); w.writeheader(); [w.writerow(q) for q in allq]
    with open("/home/user/Lessons/_sca1/tables/wordhelp.csv","w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=["file","term","bridge"]); w.writeheader(); [w.writerow(q) for q in whall]
    print(f"question rows={len(allq)}  wordhelp rows={len(whall)}")
