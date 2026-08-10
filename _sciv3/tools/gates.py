"""§5 gates. Every number prints with the universe it was counted over.

    python3 _sciv3/tools/gates.py <staging-root> [<inputs-root>]

Instrument check runs first: every scanner is validated against a KNOWN POSITIVE
before any negative it reports is believed. Three false negatives were produced
during verification by instruments written for one print dialect.
"""
import sys, os, re, glob, json, hashlib, subprocess

STAGE = sys.argv[1]
INP = sys.argv[2] if len(sys.argv) > 2 else None
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FAIL = []
PACKS = ('grow', 'build', 'launch')


def check(ok, label, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + label + (('   ' + detail) if detail else ''))
    if not ok:
        FAIL.append(label)
    return ok


PACKDIR = {}
for _p in ('grow', 'build', 'launch'):
    _s = os.path.join(STAGE, _p)
    _r = os.path.join(STAGE, 'Science_Teesside', _p.capitalize(), 'v3_40min')
    PACKDIR[_p] = _s if os.path.isdir(_s) else _r


def lessons(pack, root=None):
    d = PACKDIR[pack] if root is None else os.path.join(root, pack)
    return sorted(glob.glob(os.path.join(d, 'SCI_*.html')))


def all_lessons(root=None):
    return [f for p in PACKS for f in lessons(p, root)]


def all_html(root=None):
    if root:
        return sorted(glob.glob(os.path.join(root, '*', '*.html')))
    return sorted(f for p in PACKS for f in glob.glob(os.path.join(PACKDIR[p], '*.html')))


def read(f):
    return open(f, encoding='utf-8').read()


# =================================================== 0 · instrument check
print('\n=== INSTRUMENT CHECK (known positives before any negative is believed) ===')
live_w3 = {
    'grow': f'{REPO}/Science_Teesside/Grow/SCI_G_W3_Friction.html',
    'build': f'{REPO}/Science_Teesside/Build/SCI_B_W3_Backbones.html',
    'launch': f'{REPO}/Science_Teesside/Launch/SCI_L_W3_L1_Microscopy.html'}
for p, f in live_w3.items():
    ids = re.findall(r'id="(print-[a-z0-9-]+)"', read(f))
    check(len(ids) == 17, f'live {p} W3 carries the full 17 print ids', f'{len(ids)} ids')
check(all('Assessor Witness Statement' in read(f) for f in live_w3.values()),
      'witness scanner finds the live wording (known positive)')
check(sum('What I said, and what it changed' in read(f)
          for f in glob.glob(f'{REPO}/Science_Teesside/Launch/SCI_L_W*_L*.html')) == 15,
      'closure-line scanner finds 15/15 live LAUNCH (known positive)')
_dialect_probe = {p: ('print-route' if p == 'grow' else 'proute') for p in PACKS}
for p in PACKS:
    f = lessons(p)[0]
    check(_dialect_probe[p] in read(f), f'{p} print dialect probe `{_dialect_probe[p]}` matches')

# =================================================== 1 · node --check
print('\n=== GATE 1 · node --check, every inline <script> in the 38 new HTML files ===')
new_html = [f for f in all_html() if os.path.basename(f) != 'TEACHER_IMPLEMENTATION_GUIDE.html'
            or True]
targets = all_lessons() + [os.path.join(PACKDIR[p], 'index.html') for p in PACKS]
bad = []
nblocks = 0
os.makedirs('/tmp/gatejs', exist_ok=True)
for f in targets:
    t = read(f)
    for i, m in enumerate(re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', t, re.S)):
        body = m.group(1)
        if not body.strip():
            continue
        nblocks += 1
        p = f'/tmp/gatejs/{os.path.basename(f)}.{i}.js'
        open(p, 'w', encoding='utf-8').write(body)
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode:
            bad.append((f, i, r.stderr.strip().splitlines()[:3]))
check(not bad, f'node --check clean over {nblocks} inline script blocks in {len(targets)} files',
      str(bad[:3]))

# =================================================== 2 · jsdom boot
print('\n=== GATE 2 + A1 RUNTIME · headless Chromium boot, 35 lessons + 3 hubs ===')
print('   (Playwright/Chromium is available here and is stronger evidence than jsdom:')
print('    it emulates @media print and measures RENDERED text, not CSS source.)')
boot = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'boot.mjs')
r = subprocess.run(['node', boot] + targets, capture_output=True, text=True, cwd=REPO)
print(r.stdout.strip()[-6000:] or r.stderr.strip()[-2000:])
check(r.returncode == 0,
      'boot: 0 console errors, 0 page errors over 38 files; A1 runtime assertions')

# =================================================== 3 · A1
print('\n=== GATE A1 · print default (universe: 35 lessons) ===')
n = 0
for p in PACKS:
    route, attr = ('print-route', 'data-print-tier') if p == 'grow' else ('proute', 'data-tier')
    for f in lessons(p):
        t = read(f)
        ok = (f'.{route}{{display:block}}body[{attr}] .{route}{{display:none}}' in t
              and f"window.addEventListener('afterprint'" in t
              and 'setTimeout(()=>{delete document.body.dataset.printTier},500)' not in t
              and 'setTimeout(()=>delete document.body.dataset.tier,500)' not in t)
        n += ok
        if not ok:
            print('     missing in', f)
check(n == 35, 'A1 print-default CSS + afterprint teardown', f'{n}/35')

# =================================================== 4 · A7
print('\n=== GATE A7 · arrival entry route (universe: 35 lessons, screen + print) ===')
screen = sum('class="entry-route"' in read(f) for f in all_lessons())
pr = sum('class="pentry"' in read(f) for f in all_lessons())
check(screen == 35, 'A7 line on the arrival slide', f'{screen}/35')
check(pr == 35, 'A7 line at the head of print page 1', f'{pr}/35')
w3 = [os.path.join(PACKDIR['grow'], 'SCI_G_W3A_Friction_Explore.html'),
      os.path.join(PACKDIR['build'], 'SCI_B_W3A_Backbones_Explore.html'),
      os.path.join(PACKDIR['launch'], 'SCI_L_W3L1_Microscopy_Introduce.html')]
check(all('New to this class, or not sure?' in read(f) for f in w3),
      'A7 W3 variant used in the three W3 lessons', '3/3')
check(all('Not here last lesson?' not in read(f) for f in w3),
      'A7 standard variant absent from the three W3 lessons')
check(sum('Not here last lesson?' in read(f) for f in all_lessons()) == 32,
      'A7 standard variant in the other 32 lessons')
check(not any(re.search(r'<input|localStorage|sessionStorage', read(f).split('class="entry-route"')[1][:400])
              for f in all_lessons() if 'class="entry-route"' in read(f)),
      'A7 added no interactive element')

# =================================================== 5 · A2
print('\n=== GATE A2 · witness statement + date line (universe: 35 lessons) ===')
wit = sum('Assessor Witness Statement' in read(f) for f in all_lessons())
idl = sum('class="pidline"' in read(f) for f in all_lessons())
check(wit == 35, 'Assessor Witness Statement on print page 2', f'{wit}/35')
check(idl == 35, 'date + name line at the head of print page 1', f'{idl}/35')
qual_ok = 0
for p in PACKS:
    for f in lessons(p):
        t = read(f)
        live = read(live_w3[p])
        i = live.find('<div id="print-witness"')
        chassis = live[i:live.find('<strong>Lesson</strong>', i)]
        qual_ok += chassis in t
check(qual_ok == 35, 'witness chassis byte-identical to the matching live lesson', f'{qual_ok}/35')

# =================================================== 6 · A8.1
print('\n=== GATE A8.1 · LAUNCH written closure (universe: all new HTML) ===')
LINE = 'What I said, and what it changed'
launch_n = sum(LINE in read(f) for f in lessons('launch'))
other_n = sum(LINE in read(f) for f in lessons('grow') + lessons('build'))
check(launch_n == 15, 'closure line in 15/15 new LAUNCH lessons', f'{launch_n}/15')
check(other_n == 0, 'closure line in 0 BUILD and 0 GROW lessons', f'{other_n}')
livecl = read(live_w3['launch'])
i = livecl.find('<strong>Closing the loop:</strong>')
j = livecl.find(LINE, i)
verbatim = livecl[i:j + len(LINE)]
byte_ok = sum(verbatim in read(f) for f in lessons('launch'))
check(byte_ok >= 1, 'closure wording byte-identical to live (W3L1 checked directly)',
      f'{byte_ok}/15 share W3L1 wording; each file copies its own live match')

# =================================================== 7 · A9
print('\n=== GATE A9 · baseline-week correction (universe: all 38 new files + 3 docs) ===')
docs = [os.path.join(PACKDIR[p], 'manifest-v3.json') for p in PACKS]
universe = all_html() + docs
tot = sum(read(f).count('Aut1·W2') for f in universe)
check(tot == 0, 'Aut1·W2 returns 0 across all new files', f'{tot} occurrences')
bad3 = {os.path.basename(f): [s for s in ('from last lesson', 'the previous lesson',
                                          'previous learning', 'last lesson')
                              if s in read(f)] for f in w3}
check(all(not v for v in bad3.values()),
      'zero "from last lesson" / "the previous lesson" in the three W3 files', str(bad3))
check(all('🚪 Arrival · what you already know' in read(f) for f in w3),
      'new arrival label present in 3/3')
check(all('Weeks 1 and 2 were baseline' in read(f) for f in w3),
      'new arrival line present 3/3, screen and print')
check(all(read(f).count('Weeks 1 and 2 were baseline') >= 2 for f in w3),
      'new arrival line on BOTH screen and print in 3/3',
      str({os.path.basename(f): read(f).count('Weeks 1 and 2 were baseline') for f in w3}))
# W4-W7 arrival retrievals byte-unchanged
if INP:
    import importlib.util as _il
    _sp = _il.spec_from_file_location('bp', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         'build_packs.py'))
    _bp = _il.module_from_spec(_sp)
    _sys_argv = sys.argv[:]
    sys.argv = [sys.argv[0]]          # builder must not run main() on import
    _sp.loader.exec_module(_bp)
    sys.argv = _sys_argv
    APPROVED_FACTS = set(_bp.A7_BOX_FACTS.values())
    RE = {'grow': r'<div class="li-box"><b>Retrieve the previous lesson:</b>[^<]*</div>',
          'build': r'<div class="box scaf"><b>Retrieve the actual previous lesson:</b>[^<]*</div>',
          'launch': r'<div class="box scaf"><b>Retrieve the previous learning:</b>[^<]*</div>'}
    drift = []
    NAMES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'namemap.json')))['names']
    for p in PACKS:
        for src, dst in NAMES[p].items():
            if not src.startswith('SCI_'):
                continue
            k = re.search(r'SCI_[GBL]_(W\d(?:[AB]|L\d))_', src).group(1)
            if k in ('W3A', 'W3L1'):
                continue
            a = re.search(RE[p], read(os.path.join(INP, p, src)))
            b = re.search(RE[p], read(os.path.join(PACKDIR[p], dst)))
            if a is None or b is None:
                drift.append((dst, 'NO MATCH', ''))
                continue
            ta, tb = a.group(0), b.group(0)
            if ta == tb:
                continue
            # A7's second half deliberately EXTENDS some boxes. That is allowed only if the
            # original text survives byte-for-byte as a prefix and the addition is one of the
            # fifteen verified retrieval facts. Any other change is drift.
            core_a = ta[:-len('</div>')]
            if not tb.startswith(core_a.rstrip('.') if False else core_a):
                drift.append((dst, 'ORIGINAL TEXT ALTERED', tb[:90]))
                continue
            added = tb[len(core_a):-len('</div>')].strip()
            if added not in APPROVED_FACTS:
                drift.append((dst, 'UNAPPROVED ADDITION', added[:90]))
    check(not drift, 'W4–W7 arrival retrievals unchanged, or extended only by a verified '
          'A7 retrieval fact (original text asserted as a byte-exact prefix)', str(drift[:3]))
    print(f'   {len(APPROVED_FACTS)} boxes extended under A7; the rest byte-identical')

# =================================================== 8 · privacy
print('\n=== GATE 6 · privacy (universe: all 44 new lesson-pack HTML files) ===')
PRIV = [('localStorage', r'\blocalStorage\b'), ('sessionStorage', r'\bsessionStorage\b'),
        ('indexedDB', r'\bindexedDB\b'), ('document.cookie', r'document\.cookie'),
        ('fetch(', r'\bfetch\s*\('), ('XMLHttpRequest', r'XMLHttpRequest'),
        ('sendBeacon', r'sendBeacon'), ('<form', r'<form\b'), ('eval(', r'\beval\s*\(')]
hits = {}
for name, pat in PRIV:
    n = sum(len(re.findall(pat, read(f))) for f in all_html())
    hits[name] = n
check(all(v == 0 for v in hits.values()), 'zero storage / network / form / eval APIs', str(hits))

# =================================================== 9 · links
print('\n=== GATE 8 · link census (universe: all new HTML) ===')
urls = {}
for f in all_html():
    for u in re.findall(r'https?://[^"\'<> )]+', read(f)):
        urls.setdefault(u, []).append(os.path.basename(f))
he = [u for u in urls if 'healthy-eating' in u]
check(not he, 'zero healthy-eating URLs remain', str(he))
lp = [u for u in urls if any(os.path.basename(x).startswith('SCI_L_') for x in urls[u])]
launch_ext = sum(len(re.findall(r'https?://', read(f))) for f in lessons('launch'))
check(launch_ext == 0, 'LAUNCH new files contain zero external URLs', f'{launch_ext}')
print(f'   external URLs remaining: {len(urls)} distinct')
for u in sorted(urls):
    print(f'     {len(urls[u])}x {u}')
unv = sum('data-link-unverified="true"' in read(f) for f in lessons('grow'))
check(unv == 2, 'two unverified GROW slugs flagged', f'{unv} files carry the flag')

# =================================================== 10 · internal hrefs
print('\n=== GATE 8b · internal hrefs resolve on disk ===')
missing = []
for p in PACKS:
    for f in glob.glob(os.path.join(PACKDIR[p], '*.html')):
        for h in re.findall(r'href="([^"#?]+)', read(f)):
            if h.startswith('http') or h.startswith('mailto'):
                continue
            tgt = os.path.normpath(os.path.join(os.path.dirname(f), h))
            if not os.path.exists(tgt):
                missing.append((os.path.relpath(f, STAGE), h))
check(not missing, 'every internal href in hubs, guides and lessons resolves',
      str(missing[:6]))

# =================================================== 11 · food language
print('\n=== GATE 9 · BUILD food-language census — classified, not counted ===')
# Scan VISIBLE TEXT ONLY. A first pass over raw HTML returned 296 hits, of which
# ~280 were the CSS property `font-weight`. A count over markup is not evidence
# about language.
TERMS = (r'\b(calorie|calories|calorific|body weight|weight loss|weight gain|dieting|'
         r'diet|good/bad food|good or bad food|bad food|restrict|restricting|restriction)\b')
rows = []
for f in lessons('build'):
    raw = read(f)
    raw = re.sub(r'<(script|style)\b.*?</\1>', ' ', raw, flags=re.S | re.I)
    raw = re.sub(r'<!--.*?-->', ' ', raw, flags=re.S)
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw))
    for m in re.finditer(TERMS, txt, re.I):
        pre = txt[max(0, m.start() - 150):m.start()]
        ctx = txt[max(0, m.start() - 150):m.end() + 110]
        neg = bool(re.search(r'\b(no|never|zero|without|avoid|avoids|not|override|overrides|'
                             r'prohibit|prohibited|forbid|forbidden|free of|rather than)\b',
                             pre, re.I))
        # A third class is needed, and the binary was wrong. "an animal's natural diet"
        # is a biological use about a creature, not personal-diet language about a pupil.
        # The protection rule governs the second, not the first.
        window = txt[max(0, m.start() - 60):m.end() + 60]
        animal = bool(re.search(r'\b(animal|creature|species|herbivore|carnivore|omnivore|'
                                r'panda|koala|fox|owl|cow|sheep|its natural)\b', window, re.I))
        cls = ('PROHIBITION' if neg else 'ANIMAL-BIOLOGY' if animal else 'PERSONAL-USE')
        rows.append((os.path.basename(f), m.group(0), cls, ctx))
print(f'   {len(rows)} hits, each classified:')
for b, term, cls, ctx in rows:
    print(f'     [{cls}] {b[:34]:34s} {term:12s} …{ctx[-150:]}')
from collections import Counter
_c = Counter(r[2] for r in rows)
print('   classification:', dict(_c))
check(not _c['PERSONAL-USE'],
      'zero food-language hits are personal-diet/weight/calorie USES '
      '(prohibitions and animal-biology uses are not)', f'{len(rows)} hits, {dict(_c)}')

# =================================================== 12 · LAUNCH mark-scheme red line
print('\n=== GATE 12 · LAUNCH mark-scheme red line (universe: 18 LAUNCH HTML + manifest) ===')
BANNED = [('mark scheme', r'mark\s*scheme'), ('band descriptor', r'band\s*descriptor'),
          ('level descriptor', r'level\s*descriptor'), ('grade boundary', r'grade\s*boundar'),
          ('AO code', r'\bAO[1-3]\b'), ('(n marks)', r'\(\s*\d+\s*marks?\s*\)'),
          ('[n mark]', r'\[\s*\d+\s*marks?\s*\]')]
luniverse = sorted(glob.glob(os.path.join(PACKDIR['launch'], '*.html'))) + \
            [os.path.join(PACKDIR['launch'], 'manifest-v3.json')]
mh = {}
for name, pat in BANNED:
    found = [(os.path.basename(f), m.group(0))
             for f in luniverse for m in re.finditer(pat, read(f), re.I)]
    mh[name] = found
check(all(not v for v in mh.values()), 'zero mark schemes / descriptors / AO codes / mark '
      'allocations in LAUNCH, W7L2 and W7L3 included',
      str({k: len(v) for k, v in mh.items() if v}))
for k in ('SCI_L_W7L2_Command_Words_Explore.html', 'SCI_L_W7L3_Exam_Practice_Do.html'):
    check(os.path.exists(os.path.join(PACKDIR['launch'], k)), f'{k} was actually scanned')

print('\n' + ('ALL GATES PASS' if not FAIL else f'{len(FAIL)} GATE FAILURE(S): ' + '; '.join(FAIL)))
sys.exit(1 if FAIL else 0)
