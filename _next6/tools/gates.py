#!/usr/bin/env python3
"""ORDER N6 gate harness — measures the twelve next-six-weeks packs.

Every gate here answers one line of the order's §4. Each returns
(name, ok, detail, evidence_rows). Run with a pack root; `--json` for machine
output. Gate 10 exits MEASUREMENT INVALID rather than passing when its
reference list is absent (order §4.10).
"""
import re, sys, json, os, glob, subprocess, tempfile, collections, hashlib


# Attribute-aware. `data-lab-feedback="<b>Bridge:</b>"` is an ATTRIBUTE VALUE, not two
# tags — a naive <([a-z]+)[^>]*> tokenizer stops at the first > inside the quotes and
# invents stray-close errors. This consumes quoted runs whole.
TAG = re.compile(r"""<(/?)([a-zA-Z][\w:-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)(/?)>""")
# HTML5 optional end tags: model them or a stack parser invents unclosed-<p> errors.
IMPLIED = {'p':{'p','div','ul','ol','table','h1','h2','h3','h4','h5','h6','section',
                'blockquote','pre','form','address','fieldset','details','main','nav',
                'header','footer','article','aside','figure','dl'},
           'li':{'li'}, 'td':{'td','th','tr'}, 'th':{'td','th','tr'},
           'tr':{'tr'}, 'option':{'option','optgroup'}, 'dt':{'dt','dd'}, 'dd':{'dt','dd'},
           'thead':{'tbody','tfoot'}, 'tbody':{'tbody','tfoot'}}
AUTOCLOSE = {'p','li','td','th','tr','option','dt','dd','thead','tbody','tfoot'}

VOID = {'area','base','br','col','embed','hr','img','input','link','meta',
        'param','source','track','wbr','!doctype','!--'}

def read(p):
    return open(p, encoding='utf-8', errors='replace').read()

def html_files(root):
    return sorted(p for p in glob.glob(os.path.join(root,'**','*.html'), recursive=True))

def all_files(root):
    return sorted(p for p in glob.glob(os.path.join(root,'**','*'), recursive=True)
                  if os.path.isfile(p))

# ---------------------------------------------------------------- extraction
def scripts(s):
    """Inline JS blocks only (no src=, no non-JS type=)."""
    out=[]
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', s, re.S|re.I):
        attrs, body = m.group(1), m.group(2)
        if re.search(r'\bsrc\s*=', attrs, re.I): continue
        t = re.search(r'\btype\s*=\s*["\']?([^"\'\s>]+)', attrs, re.I)
        if t and t.group(1).lower() not in ('text/javascript','application/javascript',
                                            'module','text/ecmascript'): continue
        out.append((m.start(), body))
    return out

def json_blocks(s):
    out=[]
    for m in re.finditer(r'<script\b([^>]*type\s*=\s*["\']?application/json[^>]*)>(.*?)</script>',
                         s, re.S|re.I):
        out.append((m.start(), m.group(2)))
    return out

def strip_non_markup(s):
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', s, flags=re.S|re.I)
    return s

# ---------------------------------------------------------------- gate 1
def g1_syntax(files):
    rows=[]; bad=0; njs=0; njson=0
    with tempfile.TemporaryDirectory() as td:
        for p in files:
            s=read(p)
            for i,(off,body) in enumerate(scripts(s)):
                njs+=1
                f=os.path.join(td,'x%d.js'%i)
                open(f,'w',encoding='utf-8').write(body)
                r=subprocess.run(['node','--check',f],capture_output=True,text=True)
                if r.returncode!=0:
                    bad+=1; rows.append((p,'js@%d'%off,r.stderr.strip().split('\n')[0]))
            for off,body in json_blocks(s):
                njson+=1
                try: json.loads(body)
                except Exception as e:
                    bad+=1; rows.append((p,'json@%d'%off,str(e)))
    return ('G1 syntax (node --check + json.loads)', bad==0,
            '%d inline JS blocks, %d application/json blocks, %d errors'%(njs,njson,bad), rows)

# ---------------------------------------------------------------- gate 2
# The estate's own definition (_passsci1/gates.py:gate3_tags) — paired open/close counts
# per element that REQUIRES both tags. Deliberately not a nesting parser: three
# hand-rolled nesting attempts each invented failures the files do not have —
# on SVG foreign content (<g>/<defs>/<pattern>), on HTML5 optional end tags, and on
# markup inside attribute values (data-lab-feedback="<b>Bridge:</b>"). Paired counting
# is immune to all three, and matches what every sibling pass measured.
PAIRED = ('div','script','style','table','svg','ul','ol','section','main','header',
          'footer','article','aside','nav','button','span','g','defs','text','form',
          'label','details','summary','figure','select','textarea','a','b','strong','em')

def g2_balance_dupid(files):
    rows=[]; tb=0; du=0
    for p in files:
        raw=read(p)
        body=re.sub(r'<!--.*?-->',' ',raw,flags=re.S)
        errs=[]
        if not raw.rstrip().endswith('</html>'): errs.append('does not end </html>')
        for t in PAIRED:
            src = body if t in ('script','style') else strip_non_markup(raw)
            o=len(re.findall(r'<%s[\s>]'%t, src)); c=len(re.findall(r'</%s>'%t, src))
            if o!=c: errs.append('<%s> open=%d close=%d'%(t,o,c))
        if errs: tb+=1; rows.append((os.path.basename(p),'tag-balance','; '.join(errs[:4])))
        # (?<![-\w]) — data-parity-id="x" is not an id attribute.
        ids=re.findall(r'(?<![-\w])id\s*=\s*["\']([^"\']+)["\']', strip_non_markup(raw))
        d=[k for k,v in collections.Counter(ids).items() if v>1]
        if d: du+=1; rows.append((os.path.basename(p),'dup-id',','.join(sorted(d)[:6])))
    return ('G2 tag balance + duplicate id', tb==0 and du==0,
            '%d files with tag-balance errors, %d with duplicate ids'%(tb,du), rows)

# ---------------------------------------------------------------- gate 3
def g3_timings(files):
    rows=[]; arrays=0; bad=0
    for p in files:
        s=read(p)
        for m in re.finditer(r'["\']?timings["\']?\s*:\s*\[([^\]]*)\]', s):
            nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', m.group(1))]
            if not nums: continue
            arrays+=1
            tot=sum(nums)
            if abs(tot-40)>1e-9:
                bad+=1; rows.append((p,'timings','sum=%g (%d entries)'%(tot,len(nums))))
    return ('G3 timings sum to 40', bad==0,
            '%d timings arrays, %d not summing to 40'%(arrays,bad), rows)

# ---------------------------------------------------------------- gate 4
OFFLINE = [('data-URI', re.compile(r'\bdata:[a-z]+/[a-z0-9.+-]+;base64,', re.I)),
           ('localStorage', re.compile(r'\blocalStorage\b')),
           ('sessionStorage', re.compile(r'\bsessionStorage\b')),
           ('fetch(', re.compile(r'\bfetch\s*\(')),
           ('XMLHttpRequest', re.compile(r'\bXMLHttpRequest\b')),
           ('serviceWorker', re.compile(r'\bserviceWorker\b')),
           ('external src/href', re.compile(r'\b(?:src|href)\s*=\s*["\']https?://', re.I))]
def g4_offline(files):
    rows=[]; hits=0
    for p in files:
        s=read(p)
        for name,rx in OFFLINE:
            if name=='external src/href':
                for m in rx.finditer(s):
                    ctx=s[max(0,m.start()-160):m.start()]
                    # citations in visible prose are allowed (N11); runtime loads are not
                    if re.search(r'<(?:script|link|img|iframe|video|audio|source)\b[^>]*$',ctx,re.I):
                        hits+=1; rows.append((p,'runtime-external',s[m.start():m.start()+70]))
                continue
            n=len(rx.findall(s))
            if n: hits+=n; rows.append((p,name,str(n)))
    return ('G4 offline integrity', hits==0,
            '%d violations (0 storage, 0 fetch/XHR/SW, 0 runtime-external required)'%hits, rows)

# ---------------------------------------------------------------- gate 5
def g5_reduced_motion(files, intake_root=None, root=None):
    """Two corrections to the order's wording, both evidenced:
    (a) GROW_ASDAN ships 18 pre-existing `@keyframes orbit` rules, properly guarded by
        BOTH prefers-reduced-motion and .calm. The order says "0 @keyframes
        re-introduced" — so the gate is a DELTA against intake, not an absolute zero.
    (b) A file with no animation and no transition has nothing to reduce; requiring a
        reduced-motion block there (PRINTABLE_RESOURCES.html) measures file size, not
        accessibility."""
    rows=[]; missing=0; kf=0; motion=0; unguarded=0
    for p in files:
        s=read(p)
        k=len(re.findall(r'@keyframes', s, re.I)); kf+=k
        has_motion = k or re.search(r'\banimation\s*:\s*(?!none)', s, re.I) \
                       or re.search(r'\btransition\s*:\s*(?!none)', s, re.I)
        if not has_motion: continue
        motion+=1
        rm = re.search(r'prefers-reduced-motion', s, re.I)
        neutral = re.search(r'animation\s*:\s*none\s*!important', s, re.I)
        if not (rm and neutral):
            missing+=1; rows.append((os.path.basename(p),'motion-not-neutralised',
                                     'rm=%s none!important=%s'%(bool(rm),bool(neutral))))
        if k and not neutral:
            unguarded+=1; rows.append((os.path.basename(p),'unguarded @keyframes',str(k)))
    delta_ok=True
    if intake_root and root:
        def count(r):
            return sum(len(re.findall(r'@keyframes', read(x), re.I)) for x in html_files(r))
        before, after = count(intake_root), count(root)
        delta_ok = after<=before
        rows.append(('(delta)','@keyframes intake->now','%d -> %d'%(before,after)))
    return ('G5 reduced motion authoritative; no NEW @keyframes',
            missing==0 and unguarded==0 and delta_ok,
            '%d files carry motion, %d not neutralised, %d @keyframes total (all guarded)'
            %(motion,missing,kf), rows)

# ---------------------------------------------------------------- gate 6
def g6_links_manifest(root):
    """Ghosts (manifest lists a file that is not on disk) are always a defect — that is
    N1. Orphans are split: a LESSON on disk missing from the sequence is a defect; a
    support page (START_HERE / TEACHER_* / *MATRIX / index) that the manifest
    deliberately does not sequence is not. Manifests here are lesson-sequence
    documents with an optional supportFiles map, never file inventories."""
    rows=[]; broken=0; hard=0
    files=html_files(root)
    for p in files:
        s=read(p); d=os.path.dirname(p)
        for m in re.finditer(r'(?:href|nextFile|previousFile)\s*[:=]\s*["\']([^"\'#?]+)["\']', s):
            t=m.group(1)
            if re.match(r'^(?:https?:|mailto:|tel:|data:|#|javascript:)', t): continue
            if not os.path.exists(os.path.normpath(os.path.join(d,t))):
                broken+=1; hard+=1; rows.append((os.path.basename(p),'broken-link',t))
    SUPPORT=re.compile(r'^(?:START_HERE|TEACHER_|README|index|.*MATRIX|.*GUIDE|.*_CARDS|'
                       r'.*EVIDENCE_WINDOW|.*PLANNING|.*SOURCE_MAP|PRINTABLE|STAFF_ONLY)', re.I)
    for mf in sorted(glob.glob(os.path.join(root,'manifest*.json'))):
        try: j=json.loads(read(mf))
        except Exception as e:
            hard+=1; rows.append((os.path.basename(mf),'unparseable',str(e))); continue
        listed=set()
        def walk(o):
            if isinstance(o,str):
                if o.endswith('.html'): listed.add(o.split('/')[-1])
            elif isinstance(o,dict):
                for v in o.values(): walk(v)
            elif isinstance(o,list):
                for v in o: walk(v)
        walk(j)
        disk={os.path.basename(x) for x in files}
        for g in sorted(listed-disk):
            hard+=1; rows.append((os.path.basename(mf),'GHOST manifest->no disk',g))
        for o in sorted(disk-listed):
            if SUPPORT.match(o):
                rows.append((os.path.basename(mf),'support-orphan (informational)',o))
            else:
                hard+=1; rows.append((os.path.basename(mf),'LESSON-ORPHAN disk->no manifest',o))
    return ('G6 internal links + manifest<->disk', hard==0,
            '%d broken links; %d hard manifest disagreements (%d rows total)'
            %(broken,hard-broken,len(rows)), rows)

# ---------------------------------------------------------------- gate 9
def g9_sentinel_set(root_a, root_b):
    def mark(root):
        out=set()
        for p in html_files(root):
            if re.search(r'll-g:loop-mark', read(p)):
                out.add(os.path.relpath(p,root).replace(os.sep,'/'))
        return out
    a,b=mark(root_a),mark(root_b)
    return ('G9 sentinel ll-g:loop-mark SET-invariance', a==b,
            'intake %d files, now %d files, symmetric diff %d'%(len(a),len(b),len(a^b)),
            [('-',x,'') for x in sorted(a-b)]+[('+',x,'') for x in sorted(b-a)])

# ---------------------------------------------------------------- gate 10
def g10_names(files, reflist):
    if not reflist or not os.path.exists(reflist):
        print('MEASUREMENT INVALID: s23-no-learner-names reference list absent (%s)'%reflist,
              file=sys.stderr)
        return ('G10 s23-no-learner-names', None,
                'MEASUREMENT INVALID — reference list absent', [])
    names=[l.strip() for l in read(reflist).splitlines()
           if l.strip() and not l.startswith('#')]
    rows=[]; hits=0
    for p in files:
        s=read(p)
        for n in names:
            for m in re.finditer(r'\b%s\b'%re.escape(n), s):
                hits+=1; rows.append((p,'name-hit','offset %d'%m.start()))
    return ('G10 s23-no-learner-names', hits==0,
            '%d reference entries, %d hits'%(len(names),hits), rows)

# ---------------------------------------------------------------- print surface
def print_surface(s):
    """Byte-exact extraction of the print surface: #print-area subtree + print CSS."""
    parts=[]
    for m in re.finditer(r'<div\b[^>]*id="print-area"[^>]*>', s):
        parts.append(s[m.start():_balanced(s,m.start())])
    for m in re.finditer(r'@media\s+print\b', s):
        parts.append(s[m.start():m.start()+_css_block(s,m.start())])
    return '\n'.join(parts)

def _balanced(s,start):
    tag=re.compile(r'</?div\b'); depth=1; i=start+1
    while True:
        m=tag.search(s,i)
        if not m: return len(s)
        depth += -1 if s[m.start()+1]=='/' else 1
        i=m.end()
        if depth==0: return s.index('>',m.start())+1

def _css_block(s,start):
    i=s.index('{',start); depth=1; j=i+1
    while j<len(s) and depth:
        if s[j]=='{': depth+=1
        elif s[j]=='}': depth-=1
        j+=1
    return j-start

# ------------------------------------------------- s24 · print renders (N6-F §F1)
# Why this gate exists. Two defects reached the branch that every check we had
# called green:
#   · the learner-confirmation block was appended before </body>, OUTSIDE the
#     `.print-pack` container that BUILD_ASDAN gates with
#     `body>*:not(.print-pack){display:none!important}`. A grep for the block
#     found it in 75/75 files. It printed on 51.
#   · the LAUNCH_ASDAN print donor revealed nine slides and left each at
#     `height:91%`, so nine sheets per deck came out blank. Any check that asked
#     "is there an @media print block, and does it reveal the slides" said yes.
# Both are invisible to element presence. Both are obvious on the paper. So the
# gate renders through real Chromium print pagination to A4 and measures the
# raster: ink coverage per page, and the confirmation text as extracted from the
# PDF rather than from the DOM. Thresholds live in n6_print_measure, which owns
# the definition of an empty page.
S24_SENTINELS   = ['I confirm this is my own work', 'Learner confirmation']


def g11_print_renders(files, workdir=None, require_sentinel=True):
    """Render every carrier surface to A4 and measure the paper.

    Returns the standard (name, ok, detail, rows) tuple. `ok` is None —
    MEASUREMENT INVALID, never a pass — when the renderer or the raster reader
    is unavailable, because a gate that silently skips is worse than no gate.
    """
    carriers = [p for p in files if '<!--n6-learner-confirm:v1-->' in read(p)]
    if not carriers:
        return ('G11 s24-print-renders', None,
                'MEASUREMENT INVALID — no print carriers found', [])
    try:
        import pypdfium2  # noqa: F401
        import numpy      # noqa: F401
    except Exception as e:
        return ('G11 s24-print-renders', None,
                'MEASUREMENT INVALID — raster reader unavailable (%s)' % e, [])

    here = os.path.dirname(os.path.abspath(__file__))
    renderer = os.path.join(here, 'n6_print_render.js')
    if not os.path.exists(renderer):
        return ('G11 s24-print-renders', None,
                'MEASUREMENT INVALID — renderer absent (%s)' % renderer, [])

    tmp = workdir or tempfile.mkdtemp(prefix='s24-')
    r = subprocess.run(['node', renderer, tmp] + carriers,
                       capture_output=True, text=True,
                       cwd=os.path.dirname(here) or '.')
    man_path = os.path.join(tmp, 'render_manifest.json')
    if r.returncode != 0 or not os.path.exists(man_path):
        return ('G11 s24-print-renders', None,
                'MEASUREMENT INVALID — render failed: %s'
                % (r.stderr or r.stdout or '')[-200:], [])

    sys.path.insert(0, here)
    import n6_print_measure as M
    rows = []
    nsent = 0
    nblank = 0
    for m in json.load(open(man_path)):
        base = os.path.relpath(m['src'])
        if m.get('error'):
            rows.append((base, 'RENDER ERROR', m['error']))
            continue
        pages, text = M.measure(m['pdf'])
        low = text.lower()
        if any(s.lower() in low for s in S24_SENTINELS):
            nsent += 1
        elif require_sentinel:
            rows.append((base, 'CONFIRMATION BLOCK NOT ON PAPER',
                         '%d pages rendered, sentinel absent from PDF text' % len(pages)))
        for p in pages:
            if p['blank']:
                nblank += 1
                rows.append((base, 'BLANK PAGE',
                             'p%d ink=%.4f%% chars=%d'
                             % (p['page'], p['ink'] * 100, p['chars'])))
        if m.get('external'):
            rows.append((base, 'EXTERNAL REQUEST DURING RENDER',
                         ', '.join(m['external'][:3])))
    ok = not rows
    return ('G11 s24-print-renders', ok,
            '%d surfaces rendered · confirmation on paper %d/%d · %d blank pages'
            % (len(carriers), nsent, len(carriers), nblank), rows)
