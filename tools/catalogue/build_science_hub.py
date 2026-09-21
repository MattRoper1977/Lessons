"""Build the static Science hub in HUB-1 shape (ORDER SCI-COMPLETE PASS F, 2026-09-21).

Inputs, every one a pinned record or a pack manifest:
  assets/catalogue/science-shelf.json              the 180 shelf rows (card population)
  tools/catalogue/SCIENCE_WEEK_BINDINGS.json       pathway, term, week per route (bound from the spine)
  tools/catalogue/SCIENCE_CHASSIS_CENSUS.json      PASS B: which routes carry the exemplar chassis
  Science_Teesside/Teaching_Packs/**               each pathway's SHA256SUMS.txt is the ONLY source of
                                                   download links; DOWNLOADS_MANIFEST_HTML.json names weeks
  every current deck's own lesson-config           its part (kind: Explore / Do) -- never a filename
Outputs:
  Science_Teesside/index.html
  assets/catalogue/science-hub-bindings.json       the derivation: slots, conformers, packs
"current" = the census's conforming routes and nothing else (exemplar-chassis lessons only as
current, CONFORMS badge from the census); every other route is listed under Earlier versions
labelled by its RECORDED style, so nothing is called current that the bytes do not prove.
The writer refuses to write while any C1-C5 control is red.
"""
from pathlib import Path
import collections, hashlib, html as H, json, re, sys
from lxml import html as lhtml
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hub_sections as S

ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / 'assets/catalogue/science-shelf.json').read_text())
WEEKS = json.loads((ROOT / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json').read_text())['entries']
CENSUS = json.loads((ROOT / 'tools/catalogue/SCIENCE_CHASSIS_CENSUS.json').read_text())
PACKS = ROOT / 'Science_Teesside/Teaching_Packs'
E = H.escape
TERM_LABEL = DATA['terms']
DOWNLOAD_EXT = {'.pdf': 'PDF', '.docx': 'DOCX', '.pptx': 'PPTX', '.zip': 'ZIP', '.html': 'HTML', '.txt': 'TXT'}
CONFORMING = set(CENSUS['conforming'])
assert CENSUS.get('schema') == 'science-chassis-census/1' and CENSUS.get('routes') == len(DATA['lessons']), 'the census is not this shelf\'s'
for p in CONFORMING:
    assert CENSUS['entries'][p]['sha256'] == hashlib.sha256((ROOT / p).read_bytes()).hexdigest(), f'the census was measured on other bytes: {p}'


def h1_of(path: Path) -> str:
    text = path.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    h1 = H.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    if h1:
        return h1
    t = re.search(r'<title>(.*?)</title>', text, re.S)
    return re.split(r'\s+[|—]\s+', H.unescape(t.group(1)).strip())[0].strip() if t else path.stem


def part_of(path: Path) -> str | None:
    """The deck's own part (Explore / Do) from its lesson-config, never from its name."""
    m = re.search(r'<script[^>]*id="lesson-config"[^>]*>(.*?)</script>', path.read_text(encoding='utf-8', errors='replace'), re.S)
    if not m:
        return None
    try:
        cfg = json.loads(m.group(1))
    except ValueError:
        return None
    kind = cfg.get('kind') if isinstance(cfg, dict) else None
    return kind.strip() if isinstance(kind, str) and kind.strip() else None


# ------------------------------------------------------------ route families
def family(path: str) -> str:
    if path in CONFORMING:
        return 'current'
    if Path(path).name.startswith('START_HERE'):
        return 'reference'
    style = (WEEKS.get(path) or {}).get('style') or next((r['style'] for r in DATA['lessons'] if r['path'] == path), 'earlier')
    return f'recorded {style}'


FAMILIES = {r['path']: family(r['path']) for r in DATA['lessons']}


# ------------------------------------------------------------ strand rows (the conformers)
def strand_rows() -> list[dict]:
    rows = []
    for p in sorted(CONFORMING):
        e = WEEKS[p]
        weeks = e['weeks'] or [None]
        for w in weeks:
            rows.append({'path': p, 'pathway': e['pathway'], 'term': (w['term'] if w else next(r['term'] for r in DATA['lessons'] if r['path'] == p)),
                         'week': (w['weekWithinTerm'] if w else None), 'strand': 'Science', 'h1': h1_of(ROOT / p),
                         'alternative': False, 'part': part_of(ROOT / p),
                         'badges': '<span class="pill ok" data-conforms="1">CONFORMS</span>'})
    return rows


# ------------------------------------------------------------- pack tree
def manifest_members(pack: Path) -> list[str]:
    if (pack / 'SHA256SUMS.txt').is_file():
        return [l.split(maxsplit=1)[1].strip() for l in (pack / 'SHA256SUMS.txt').read_text().splitlines() if l.strip()]
    raise SystemExit(f'pack without a manifest: {pack}')


def pack_cards() -> list[dict]:
    dm = json.loads((PACKS / 'DOWNLOADS_MANIFEST_HTML.json').read_text())['pathways']
    rel = lambda p: str(p.relative_to(ROOT / 'Science_Teesside'))
    cards = []
    for pathway in S.PATHWAYS:
        base = PACKS / pathway
        if not base.is_dir():
            continue
        spec = dm.get(pathway, {})
        members = manifest_members(base)
        by_id = {}
        for mem in members:
            if mem.startswith('HTML/') and mem.endswith('.html'):
                by_id[Path(mem).stem] = mem
        week_rows = collections.OrderedDict()
        for L in spec.get('lessons', []):
            mem = by_id.get(L['id'])
            if mem:
                week_rows.setdefault(f'W{L["week"]}', []).append((f'HTML · {L["title"]}', rel(base / mem)))
        documents = []
        for mem in sorted(members, key=S.natural):
            if mem.startswith('HTML/') or mem.startswith('Resources/'):
                continue
            ext = Path(mem).suffix.lower()
            if ext in DOWNLOAD_EXT and not mem.endswith('.json'):
                documents.append((f'{DOWNLOAD_EXT[ext]} · ' + Path(mem).stem.replace('_', ' '), rel(base / mem)))
        start = PACKS / 'index.html'
        lesson_count = sum(len(v) for v in week_rows.values())
        cards.append({'id': f'{pathway}_Science_pack', 'pathway': pathway, 'pathway_label': pathway, 'term': 'Aut1', 'term_label': TERM_LABEL['Aut1'],
                      'strand': 'Science', 'title': f'{pathway} · Science teaching pack', 'start_here': rel(start), 'proofread': False,
                      'lesson_count': lesson_count, 'weeks': list(week_rows.items()), 'documents': documents,
                      'links': [('start here', rel(start))] + [f for _, fs in week_rows.items() for f in fs] + documents})
    return cards


# ------------------------------------------------------------ derivation
lessons = strand_rows()
cards = pack_cards()
D = S.derive(DATA['lessons'], lessons, [], {}, FAMILIES, TERM_LABEL)
errors = S.c1_errors(D) + S.c2_errors(D, FAMILIES) + S.c3_errors(ROOT / 'Science_Teesside', cards)


def c5_errors(d: dict, conforming: set) -> list[str]:
    """PASS F: current <=> conforming. A current card the census did not prove, or a
    conforming route not rendered current, is red."""
    errs = [f'C5 current card not in the chassis census: {p}' for p in sorted(d['current'] - conforming)]
    errs += [f'C5 conforming route not rendered current: {p}' for p in sorted(conforming - d['current'])]
    return errs


errors += c5_errors(D, CONFORMING)
href_of = lambda path: '../' + path
pack_href = lambda path: path.removeprefix('Science_Teesside/')
blurb, start_hrefs = {}, {}
for pw in S.PATHWAYS:
    sh = ROOT / 'Science_Teesside' / pw.capitalize() / 'START_HERE.html'
    assert sh.is_file(), f'no START_HERE page for {pw}'
    blurb[pw] = h1_of(sh)
    start_hrefs[pw] = f'{pw.capitalize()}/START_HERE.html'
strip = S.render_start_strip('Science', blurb, start_hrefs)
current_html, r1 = S.render_current(D, 'Science', href_of, pack_href, {'Science': 'Science'}, DATA['styles'])
packs_html, r2 = S.render_packs(cards, D['reference'], href_of, 'Science')
def recorded_week(path: str):
    """The route's own bound week from SCIENCE_WEEK_BINDINGS (a record, never a path); None when
    the record binds none or more than one."""
    ws = (WEEKS.get(path) or {}).get('weeks') or []
    return ws[0]['weekWithinTerm'] if len(ws) == 1 else None
earlier_html, r3 = S.render_earlier(D['earlier'], FAMILIES, href_of, TERM_LABEL, week_of=recorded_week)
rendered = r1 + r2 + r3
errors += S.c4_errors(rendered, DATA['lessons'])
if errors:
    print('\n'.join(errors)); raise SystemExit(f'REFUSED: {len(errors)} control error(s); nothing written')

served_by_earlier = collections.Counter()
for r in D['earlier']:
    for w in (WEEKS.get(r['path']) or {}).get('weeks', []):
        served_by_earlier[(r['pathway'], w['term'])] += 1
note_items = ''.join(f'<li>{E(p)} · {E(TERM_LABEL.get(t, t))}: {n} lessons</li>' for (p, t), n in sorted(served_by_earlier.items(), key=lambda kv: (S.PATHWAYS.index(kv[0][0]), (S.TERM_ORDER.index(kv[0][1]) if kv[0][1] in S.TERM_ORDER else len(S.TERM_ORDER)))))
note_html = (f'<details class="hub-gaps" id="pre-chassis"><summary>Lessons in the earlier shape · {len(D["earlier"])} routes listed under Earlier versions</summary>'
             f'<p class="hub-note">Current shows only the lessons whose own bytes carry the exemplar chassis (the PASS B census). Every other lesson is still served and listed below, by pathway and recorded term.</p><ul>{note_items}</ul></details>')

# ------------------------------------------------------------ page
term_options = ''.join(f'<option value="{E(term)}">{E(label)}</option>' for term, label in DATA['terms'].items() if any(r['term'] == term or term in r['terms'] for r in DATA['lessons']))
style_options = ''.join(f'<option value="{E(style)}">{E(label)}</option>' for style, label in DATA['styles'].items() if any(r['style'] == style for r in DATA['lessons']))
root_source = (ROOT / 'index.html').read_text()
header = re.search(r'<header class="header mbm-site-header".*?</header>', root_source, re.S).group(0)
header_doc = lhtml.fromstring(header)
for link in list(header_doc.xpath('//a[@href]')):
    u = urlsplit(link.get('href'))
    if u.netloc in {'madebymatt-play.uk', 'www.madebymatt-play.uk'} or u.path.rstrip('/').lower() == '/games':
        link.drop_tree()
header = lhtml.tostring(header_doc, encoding='unicode')
base_css = re.sub(r'^/\*.*?\*/\n', '', (ROOT / 'assets/catalogue/shelf-base.css').read_text(), count=1, flags=re.S)
assert ':root{--navy:#161D3D' in base_css and base_css.count('{') == base_css.count('}') >= 200, 'shelf-base.css is not the house block'
output = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Science by pathway, term and week — Made by Matt</title><meta name="description" content="Find the current Science lesson for any week by BUILD, GROW and LAUNCH pathway, then packs and downloads, then earlier versions.">
<meta name="theme-color" content="#161D3D"><link rel="icon" href="https://madebymatt.uk/favicon.svg">
<style>''' + base_css + '''</style><link rel="stylesheet" href="../assets/mbm-platform.css"><link rel="stylesheet" href="../assets/mbm-hub.css"><link rel="stylesheet" href="../assets/catalogue/catalogue.css">
<script>try{var theme=localStorage.getItem('mbm_reading_theme');if(theme&&theme!=='cream')document.documentElement.setAttribute('data-theme',theme)}catch(e){}</script>
</head><body class="mbm-hub mbm-hub-lessons hub-v2" data-mbm-estate="lessons" data-catalogue-subject="Science" data-catalogue-noun="teaching version"><a class="skip" href="#main">Skip to Science lessons</a>''' + header + '''
<main id="main"><section class="hero hero-compact"><div class="hero-in"><nav class="lesson-breadcrumb" aria-label="Breadcrumb"><a href="/">Learning home</a><a href="../">All lessons</a></nav><p class="eyebrow">Science · Teesside</p><h1>Science by pathway, term and week</h1><p class="lede">The current lesson for each week first, then packs and downloads, then earlier versions.</p></div></section>
''' + strip + '''
<div class="toolbar" role="search" aria-label="Filter Science lessons"><label>Search<input id="science-search" type="search" placeholder="Try: osmosis, muscles, fossils…" autocomplete="off"></label><label>Pathway<select id="science-pathway"><option value="">All pathways</option><option value="BUILD">BUILD</option><option value="GROW">GROW</option><option value="LAUNCH">LAUNCH</option></select></label><label>Strand<select id="science-strand"><option value="">All strands</option><option value="Science">Science</option></select></label><label>Term<select id="science-term"><option value="">All terms</option>''' + term_options + '''</select></label><label>Teaching style<select id="science-style"><option value="">All teaching styles</option>''' + style_options + '''</select></label></div>
<div class="science-status"><p id="science-count" role="status" aria-live="polite" aria-atomic="true">''' + str(len(DATA['lessons'])) + ''' Science teaching versions</p><button type="button" id="science-clear">Clear filters</button></div>
<p id="science-empty" class="status" hidden>No matching lessons. Try a different term or clear the filters.</p>
<noscript><p class="status">All lessons are listed below: current lessons first, then packs and downloads, then earlier versions. The filters need JavaScript; every link works without it.</p></noscript>
<div id="science-lessons">''' + current_html + note_html + packs_html + earlier_html + '''</div></main><footer class="footer"><div class="bar"><p>Made by Matt · Learn • Build • Explore</p><a href="../">Return to the Lesson Hub</a></div></footer>
<script src="../assets/catalogue/science-shelf.js"></script><script defer src="../assets/mbm-theme.js"></script><script defer src="../assets/mbm-platform.js"></script><script defer src="/hud.js"></script>
</body></html>
'''
(ROOT / 'Science_Teesside/index.html').write_text(output)
bindings = {
    'schema': 'science-hub-bindings/1', 'order': 'SCI-COMPLETE PASS F',
    'censusSha256': hashlib.sha256((ROOT / 'tools/catalogue/SCIENCE_CHASSIS_CENSUS.json').read_bytes()).hexdigest(),
    'weekBindingsSha256': hashlib.sha256((ROOT / 'tools/catalogue/SCIENCE_WEEK_BINDINGS.json').read_bytes()).hexdigest(),
    'population': {'shelfRows': len(DATA['lessons']), 'rendered': len(rendered), 'currentCards': len(D['current']),
                   'reference': len(D['reference']), 'earlier': len(D['earlier']), 'packCards': len(cards)},
    'families': dict(collections.Counter(FAMILIES.values())),
    'slots': [{'pathway': k[0], 'term': k[1], 'week': k[2], 'current': [{'path': L['path'], 'part': L.get('part')} for L in s['current']]}
              for k, s in sorted(D['slots'].items(), key=lambda kv: (S.PATHWAYS.index(kv[0][0]), (S.TERM_ORDER.index(kv[0][1]) if kv[0][1] in S.TERM_ORDER else len(S.TERM_ORDER)), kv[0][2] is None, kv[0][2] or 0))],
    'earlierByPathwayTerm': [{'pathway': p, 'term': t, 'lessons': n} for (p, t), n in sorted(served_by_earlier.items())],
    'packs': [{'id': c['id'], 'pathway': c['pathway'], 'lessons': c['lesson_count'], 'startHere': c['start_here'], 'links': len(c['links'])} for c in cards],
}
(ROOT / 'assets/catalogue/science-hub-bindings.json').write_text(json.dumps(bindings, indent=1, ensure_ascii=False) + '\n')
print(f'Built the Science hub: {len(rendered)} of {len(DATA["lessons"])} shelf cards rendered ({len(D["current"])} current CONFORMS, {len(D["reference"])} reference, {len(D["earlier"])} earlier); '
      f'{len(D["slots"])} current slots; {len(cards)} pack cards; controls C1-C5 0 errors.')
