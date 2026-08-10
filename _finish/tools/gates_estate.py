"""§7 gates for the BUILD estate. Every number prints with its universe.

    python3 _finish/tools/gates_estate.py <install-root> <rollback-sha>

Scanners are validated against a known positive first. Ten confident-but-wrong
numbers have been produced across this programme; every one was a measurement
whose unit or universe went unstated. Sizes are named in bytes or characters.
"""
import sys, os, re, glob, json, subprocess

ROOT = sys.argv[1]
SHA = sys.argv[2] if len(sys.argv) > 2 else None
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FAIL, AMBER = [], []
SUBJ = ['Art_Teesside', 'BUILD_ASDAN', 'DT_Community_Upcycling', 'Humanities_Teesside']
PRINT_REPAIR = '.proute{display:block}body[data-tier] .proute{display:none}'


def check(ok, label, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + label + (('   ' + detail) if detail else ''))
    if not ok:
        FAIL.append(label)
    return ok


def read(f):
    return open(f, encoding='utf-8').read()


def html(sub=None):
    g = os.path.join(ROOT, sub or '', '**', '*.html')
    return sorted(glob.glob(g, recursive=True)) + \
        (sorted(glob.glob(os.path.join(ROOT, '*.html'))) if sub is None else [])


def routes(sub=None):
    """A route-bearing lesson is a file carrying the print-tier repair (Rev C A-ii)."""
    return sorted(f for f in html(sub) if PRINT_REPAIR in read(f))


def text_of(f):
    t = read(f)
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))


print('\n=== INSTRUMENT CHECK — known positives first ===')
live_dt1 = os.path.join(REPO, 'Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html')
check('Run a <strong>magnet</strong> slowly' in read(live_dt1),
      'nail-sweep scanner finds the live W1 wording (known positive)')
check(len(routes()) > 0, 'print-repair scanner matches the estate dialect (known positive)')
check(sum(1 for f in glob.glob(os.path.join(REPO, 'BUILD_ASDAN/**/*.html'), recursive=True)
          if 'Assessor Witness Statement' in read(f)) > 0,
      'witness scanner finds live ASDAN witness surfaces (known positive)')

print('\n=== COUNTS, universes named ===')
allh = html()
print(f'   files installed: {len(glob.glob(os.path.join(ROOT, "**", "*"), recursive=True))} '
      f'· HTML: {len(allh)} · route-bearing lessons: {len(routes())}')
for s in SUBJ:
    print(f'     {s:24s} {len(routes(s)):3d} route-bearing of {len(html(s)):3d} HTML')
check(len(routes()) == 53, 'route-bearing lessons = 53', f'{len(routes())}')
check(not glob.glob(os.path.join(ROOT, '**', '*TEST*'), recursive=True),
      'no _OUTSTANDING_V3_TEST left in any filename')
check(not os.path.isdir(os.path.join(ROOT, 'Science')),
      'the skipped Science/ folder is absent from the install')

print('\n=== GATE 1 · node --check, every inline script block ===')
bad, nb = [], 0
os.makedirs('/tmp/gej', exist_ok=True)
for f in allh:
    for i, m in enumerate(re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', read(f), re.S)):
        if not m.group(1).strip():
            continue
        nb += 1
        p = f'/tmp/gej/{os.path.basename(f)}.{i}.js'
        open(p, 'w', encoding='utf-8').write(m.group(1))
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode:
            bad.append((os.path.basename(f), r.stderr.strip().splitlines()[:2]))
check(not bad, f'node --check clean over {nb} inline script blocks in {len(allh)} HTML files',
      str(bad[:2]))

print('\n=== GATE 2 + 3 · boot and print default, headless Chromium ===')
boot = os.path.join(REPO, '_sciv3', 'tools', 'boot.mjs')
r = subprocess.run(['node', boot] + routes(), capture_output=True, text=True, cwd=REPO)
tail = r.stdout.strip().splitlines()
print('   ' + '\n   '.join(tail[-4:]) if tail else r.stderr[-500:])
check(r.returncode == 0,
      f'boot: 0 console/page errors and A1 print assertions over {len(routes())} route files')

print('\n=== GATE 6 · Arts Award — report the tags, assert only two things ===')
LIVE_ART = sorted(glob.glob(os.path.join(REPO, 'Art_Teesside/Build/BUILD_ART_W*.html')))
V3_ART = sorted(glob.glob(os.path.join(ROOT, 'Art_Teesside/BUILD_ART_W*.html')))


def part_tag(f):
    """The file's OWN tag, read in context. A 'Part A' inside a retrieval sentence is
    not a tag — that conflation is what generated the brief's error."""
    t = read(f)
    for m in re.finditer(r'(?:<span[^>]*class="[^"]*(?:tag|pill|part)[^"]*"[^>]*>|<b>|<strong>)'
                         r'\s*(Explore Parts? [A-D][^<]{0,60})', t):
        return re.sub(r'\s+', ' ', m.group(1)).strip()
    m = re.search(r'(Explore Parts? [A-D][^<]{0,60})', t)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else None


print(f'   {"week":6s} {"live Art_Teesside/Build":42s} v3')
diverge = []
for lf, vf in zip(LIVE_ART, V3_ART):
    w = re.search(r'_(W\d)_', os.path.basename(lf)).group(1)
    a, b = part_tag(lf), part_tag(vf)
    def norm(x):
        # HTML entities and curly quotes are encoding, not content. Comparing them
        # raw reported three false divergences on the first run.
        x = (x or '').replace('&amp;', '&').replace('&#39;', "'")
        x = x.replace('\u2019', "'").replace('\u2018', "'")
        return re.sub(r'[\s+]', '', x).lower()
    same = norm(a) == norm(b)
    print(f'   {w:6s} {str(a)[:42]:42s} {b}   {"" if same else "<< DIVERGES"}')
    if not same:
        diverge.append((w, a, b))
if diverge:
    AMBER.append(f'Part-tag divergence live vs v3: {diverge}')
print('   (reported, not asserted — no Part tag is changed in any file)')

hrs = []
for f in V3_ART:
    for pat in [r'at least \d+ hours', r'minimum of \d+ hours', r'\d+ GLH', r'TQT']:
        for m in re.finditer(pat, read(f), re.I):
            ctx = text_of(f)
            k = ctx.find(m.group(0))
            hrs.append((os.path.basename(f)[:34], m.group(0),
                        ctx[max(0, k - 130):k + 130].strip()))
print(f'   hours/TQT hits: {len(hrs)} — every one read in context:')
for b, term, ctx in hrs:
    print(f'     {b:34s} [{term}]  …{ctx[:190]}')
gate = [h for h in hrs if not re.search(r'(?i)\b(no|not|never|guidance|does not|rather than|'
                                        r'is not|without)\b', h[2])]
check(not gate, 'zero Arts Award hours THRESHOLDS across the 8 v3 art files '
      '(guidance mentions that explicitly deny a threshold are not thresholds)',
      f'{len(hrs)} hits, {len(gate)} unexplained')

w2 = [f for f in V3_ART if '_W2_' in f]
if w2:
    t2 = text_of(w2[0])
    org = len(re.findall(r'(?i)organisation|gallery|museum|studio|venue', t2))
    artefact = re.findall(r'(?i)(evidence card|evidence sheet|print worksheet|record sheet|'
                          r'organisation card|evidence target|capture|record)[^.]{0,110}', t2)
    print(f'   W2 organisation mentions: {org}')
    print('   W2 evidence-artefact candidates:')
    for a in artefact[:6]:
        print(f'     · {re.sub(chr(92)+"s+"," ",str(a))[:160]}')
    check(bool(artefact), 'Part B produces an organisation EVIDENCE ARTEFACT, not merely teaching',
          f'{len(artefact)} artefact phrases')

print('\n=== GATE 7 · PEQ must not appear on any BUILD file ===')
peq = {}
for term in ['PEQ', 'Entry 3', 'ComSkE3', 'WellbLe', 'DecMkSk', 'TmWkSk', 'ThSk', 'LSk']:
    hits = [os.path.basename(f) for f in routes('BUILD_ASDAN') if re.search(r'\b%s\b' % term, read(f))]
    if hits:
        peq[term] = hits
check(not peq, f'zero PEQ / Entry 3 / unit-code claims across the {len(routes("BUILD_ASDAN"))} '
      'ASDAN route files', str(peq))

print('\n=== GATE 8 · FoodWise food language — classified, not counted ===')
TERMS = (r'\b(calorie|calories|calorific|body weight|weight loss|weight gain|dieting|diet|'
         r'good/bad food|bad food|restrict|restricting|restriction)\b')
rows = []
for f in routes('BUILD_ASDAN'):
    if '/FoodWise/' not in f and not os.path.basename(f).startswith('FW_'):
        continue
    txt = text_of(f)
    for m in re.finditer(TERMS, txt, re.I):
        ctx = txt[max(0, m.start() - 150):m.end() + 160]
        # Read BOTH sides. A denial can follow the term as easily as precede it —
        # "diet ... is optional unless genuinely required" is a data-minimisation
        # rule, not personal-diet language, and a look-behind alone misreads it.
        neg = bool(re.search(r'\b(no|never|zero|without|avoid|not|override|prohibit|forbid|'
                             r'free of|rather than|instead of|optional|does not|is not)\b',
                             ctx, re.I))
        cls = 'PROHIBITION' if neg else 'REVIEW'
        rows.append((os.path.basename(f)[:30], m.group(0), cls, ctx))
print(f'   {len(rows)} hits across the FoodWise route files, each classified:')
for b, term, cls, ctx in rows:
    print(f'     [{cls}] {b:30s} {term:12s} …{ctx[-150:]}')
check(all(r[2] == 'PROHIBITION' for r in rows),
      'every FoodWise food-language hit is a prohibition; zero are personal-diet uses',
      f'{len(rows)} hits')

print('\n=== GATE 9 · D&T safety ===')
dt = routes('DT_Community_Upcycling')
LEG = ('Do not use an open window/door or a generic dust mask as the control plan. '
       'Local COSHH/RA decides the actual controls.')
HT = 'HT stamp is only one check and is not sufficient by itself'
check(sum(LEG in read(f) for f in dt) == len(dt),
      f'legacy-framing refusal present and byte-unchanged in all {len(dt)} D&T files',
      f'{sum(LEG in read(f) for f in dt)}/{len(dt)}')
check(sum(HT in read(f) for f in dt) >= 1, 'HT-stamp-not-sufficient ruling present',
      f'{sum(HT in read(f) for f in dt)}/{len(dt)}')
NAIL = 'Run a <strong>magnet</strong> slowly over both faces and both edges'
check(sum(NAIL in read(f) for f in dt) == 1, 'nail-sweep wording restored (W1)',
      f'{sum(NAIL in read(f) for f in dt)}')
check(sum('Magnet-sweep the board' in read(f) for f in dt) == 1,
      'nail-sweep step restored (W3 decision chain)')
check(sum('the magnet finds metal' in read(f) for f in dt) == 1,
      'nail-sweep STOP condition restored (W3)')

print('\n=== GATE 10 · privacy (universe: all installed HTML) ===')
PRIV = [('localStorage', r'\blocalStorage\b'), ('sessionStorage', r'\bsessionStorage\b'),
        ('indexedDB', r'\bindexedDB\b'), ('document.cookie', r'document\.cookie'),
        ('fetch(', r'\bfetch\s*\('), ('XMLHttpRequest', r'XMLHttpRequest'),
        ('sendBeacon', r'sendBeacon'), ('<form', r'<form\b'), ('eval(', r'\beval\s*\(')]
hits = {n: sum(len(re.findall(p, read(f))) for f in allh) for n, p in PRIV}
check(all(v == 0 for v in hits.values()), 'zero storage / network / form / eval', str(hits))

print('\n=== GATE · internal hrefs resolve on disk ===')
missing = []
for f in allh:
    for h in re.findall(r'href="([^"#?]+)', read(f)):
        if h.startswith(('http', 'mailto')):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), h))):
            missing.append((os.path.relpath(f, ROOT), h))
check(not missing, 'every internal href in the estate resolves', str(missing[:5]))

print('\n=== GATE 4 · live invariance ===')
if SHA:
    for tree in ['Art_Teesside', 'BUILD_ASDAN', 'Build/Slideshows', 'Humanities_Teesside',
                 'Baseline_Weeks', 'biology', 'chemistry', '2 Physics 10']:
        d = subprocess.run(['git', 'diff', '--stat', f'{SHA}..HEAD', '--', tree],
                           capture_output=True, text=True, cwd=REPO).stdout.strip()
        check(d == '', f'{tree}/ unchanged since ROLLBACK_SHA', repr(d[:100]))
    live25 = [f for f in glob.glob(os.path.join(REPO, 'Science_Teesside/*/SCI_*.html'))
              if 'v3_40min' not in f]
    drift = []
    for f in live25:
        rel = os.path.relpath(f, REPO)
        a = subprocess.run(['git', 'rev-parse', f'{SHA}:{rel}'], capture_output=True,
                           text=True, cwd=REPO).stdout.strip()
        b = subprocess.run(['git', 'hash-object', rel], capture_output=True, text=True,
                           cwd=REPO).stdout.strip()
        if a != b:
            drift.append(rel)
    check(not drift, f'all {len(live25)} live science lessons byte-identical (blob hash)',
          str(drift))

print('\n=== GATE 5 · sentinels, no movement expected ===')


def fset(needle):
    out = set()
    for f in glob.glob(os.path.join(REPO, '**', '*.html'), recursive=True):
        if '/.git/' in f or '/node_modules/' in f:
            continue
        try:
            if needle in open(f, encoding='utf-8', errors='ignore').read():
                out.add(os.path.relpath(f, REPO))
        except OSError:
            pass
    return out


for needle, expect in [('ll-g:loop-mark', 50), ('What I said, and what it changed', 113)]:
    s = fset(needle)
    new_in = {p for p in s if p.startswith('BUILD_Estate_v3/')}
    check(len(s) == expect and not new_in,
          f'`{needle}` set unmoved at {expect} files; 0 in the new estate',
          f'{len(s)} files, {len(new_in)} in BUILD_Estate_v3/')

print('\n' + ('ESTATE GATES: ALL PASS' if not FAIL else f'{len(FAIL)} FAILURE(S): ' + '; '.join(FAIL)))
for a in AMBER:
    print('  AMBER:', a)
sys.exit(1 if FAIL else 0)
