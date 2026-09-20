"""Build the static Humanities hub from reviewed records (ORDER HUB-1, 2026-09-20).

Inputs, every one of them a pinned record or a pinned pack member:
  assets/catalogue/humanities-shelf.json           the 142 shelf rows (card population)
  tools/catalogue/HUMANITIES_STRAND.json           the signed strand record: term, week,
                                                   strand, h1, alternative per lesson card
  Humanities_Teesside/Teaching_Packs/**            the pack tree: SHA256SUMS.txt /
                                                   MANIFEST.json / DOWNLOADS_MANIFEST.json
                                                   are the ONLY source of download links
  HUM_00_SoW_and_Order/{Humanities_Scheme_of_Work_2026-27.docx, RE_Scheme_of_Work_Autumn_2026.html}
                                                   the planned slots (for the gap note)
Outputs:
  Humanities_Teesside/index.html
  assets/catalogue/humanities-hub-bindings.json    the derivation: slots, gaps, packs
The writer refuses to write while any C1-C4 control is red.
"""
from pathlib import Path
import collections, hashlib, html as H, json, re, sys, zipfile
from lxml import html as lhtml
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hub_sections as S

ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / 'assets/catalogue/humanities-shelf.json').read_text())
STRAND = json.loads((ROOT / 'tools/catalogue/HUMANITIES_STRAND.json').read_text())
PACKS = ROOT / 'Humanities_Teesside/Teaching_Packs'
E = H.escape
TERM_LABEL = DATA['terms']
TERM_KEY = {'Autumn_1': 'Aut1', 'Autumn_2': 'Aut2', 'Spring_1': 'Spr1', 'Spring_2': 'Spr2', 'Summer_1': 'Sum1', 'Summer_2': 'Sum2',
            'Autumn 1': 'Aut1', 'Autumn 2': 'Aut2', 'Spring 1': 'Spr1', 'Spring 2': 'Spr2', 'Summer 1': 'Sum1', 'Summer 2': 'Sum2'}
STRAND_LABEL = {'Humanities': 'Humanities', 'RE': 'RE & world views'}
DOWNLOAD_EXT = {'.pdf': 'PDF', '.docx': 'DOCX', '.pptx': 'PPTX', '.zip': 'ZIP'}
ROLE_WORDS = {'Editable', 'Pack', 'Slides', 'Knowledge', 'Organiser', 'Pupil', 'Resources', 'Teacher', 'Notes', 'Captioned', 'Model', 'Transcript', 'Data', 'Complete', 'Collection'}
assert STRAND.get('reviewed', {}).get('signature', '').startswith('Reviewed by Matt Roper'), \
    'the strand record is unsigned; the writer does not read an unsigned record'


def h1_of(path: Path) -> str:
    """The deck's own heading. A pack lesson whose first <h1> is the export template
    ('+esc(d.title)+') names itself in its first <title> instead."""
    text = path.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    h1 = H.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''
    if h1 and 'esc(' not in h1 and "'+" not in h1:
        return h1
    t = re.search(r'<title>(.*?)</title>', text, re.S)
    title = H.unescape(t.group(1)).strip() if t else ''
    assert title and 'esc(' not in title, f'no readable heading: {path}'
    return re.split(r'\s+\|\s+', title)[0].strip()



def lesson_binding(path: Path) -> dict:
    """A pack lesson's pathway, term and week from ITS OWN config text -- never from a
    filename or folder (VB-RUN13 R0). Every pack lesson carries exactly one "week"."""
    text = path.read_text(encoding='utf-8', errors='replace')
    weeks = set(re.findall(r'"week"\s*:\s*(\d+)', text))
    terms = set(re.findall(r'"term"\s*:\s*"([^"]+)"', text))
    pathways = set(re.findall(r'"pathway"\s*:\s*"(BUILD|GROW|LAUNCH)"', text))
    assert len(weeks) == 1 and len(terms) == 1 and len(pathways) == 1, f'no single week/term/pathway in the lesson text: {path}'
    return {'pathway': pathways.pop(), 'term': TERM_KEY[terms.pop()], 'week': int(weeks.pop())}


# ------------------------------------------------------------ route families
def family(path: str) -> str:
    """M2 ruling: the family IS the marking. Dated folder = current; Estate_v3 and the
    Slideshows series are earlier; everything else is reference."""
    if re.match(r'Humanities_Teesside/(BUILD|GROW|LAUNCH)_W', path):
        return 'reference' if 'START_HERE' in Path(path).name else 'current'
    if '_Estate_v3/' in path:
        return 'Estate v3'
    if re.match(r'(Build|Grow|Launch)/Slideshows/', path):
        return 'Slideshows series'
    return 'reference'


FAMILIES = {r['path']: family(r['path']) for r in DATA['lessons']}


# ------------------------------------------------------------- SoW slots
def sow_slots() -> dict[str, set]:
    slots = {'Humanities': set(), 'RE': set()}
    x = zipfile.ZipFile(PACKS / 'HUM_00_SoW_and_Order/Humanities_Scheme_of_Work_2026-27.docx').read('word/document.xml').decode()
    x = re.sub(r'<[^>]+>', '', re.sub(r'</w:p>', '\n', x))
    cur = None
    for line in (H.unescape(l).strip() for l in x.split('\n') if l.strip()):
        m = re.fullmatch(r'(Build|Grow|Launch) (Autumn [12]|Spring [12]|Summer [12])', line)
        if m:
            cur = (m.group(1).upper(), TERM_KEY[m.group(2)]); continue
        m = re.fullmatch(r'([1-9])[A-Z].{5,}', line)
        if m and cur:
            slots['Humanities'].add((cur[0], cur[1], int(m.group(1))))
    t = (PACKS / 'HUM_00_SoW_and_Order/RE_Scheme_of_Work_Autumn_2026.html').read_text(encoding='utf-8', errors='replace')
    t = H.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<(script|style)[\s\S]*?</\1>', '', t)))
    cur = None
    for line in (l.strip() for l in t.split('\n') if l.strip()):
        m = re.fullmatch(r'(BUILD|GROW|LAUNCH) · (Autumn [12])', line)
        if m:
            cur = (m.group(1), TERM_KEY[m.group(2)]); continue
        m = re.fullmatch(r'Week (\d+) · .+', line)
        if m and cur:
            slots['RE'].add((cur[0], cur[1], int(m.group(1))))
    assert len(slots['Humanities']) == 117 and len(slots['RE']) == 42, (len(slots['Humanities']), len(slots['RE']))
    return slots


# ------------------------------------------------------------- pack tree
def manifest_members(pack: Path) -> list[str]:
    """Members named by the pack's own manifest, relative to the pack folder."""
    if (pack / 'SHA256SUMS.txt').is_file():
        return [l.split(maxsplit=1)[1].strip() for l in (pack / 'SHA256SUMS.txt').read_text().splitlines() if l.strip()]
    if (pack / 'MANIFEST.json').is_file():
        return [k.split('/', 1)[1] for k in json.loads((pack / 'MANIFEST.json').read_text())]
    raise SystemExit(f'pack without a manifest: {pack}')


def download_label(mem: str) -> str:
    # The file's role (Editable Pack, Knowledge Organiser ...): the stem after the last '_W'-prefixed token is not read; the role is the trailing words.
    stem = ' '.join(w for w in Path(mem).stem.split('_') if w in ROLE_WORDS)
    return f'{DOWNLOAD_EXT[Path(mem).suffix.lower()]} · {stem}'


def pack_cards_and_lessons() -> tuple[list[dict], list[dict]]:
    cards, lessons = [], []
    rel = lambda p: str(p.relative_to(ROOT / 'Humanities_Teesside'))
    for pack in sorted(p for p in PACKS.iterdir() if p.is_dir() and (p.name.endswith('_Reviewed') or p.name.endswith('_Fallback'))):
        m = re.fullmatch(r'(HUM|RE)_(Autumn|Spring)(?:_(\d))?_([A-Z_]+?)_(Reviewed|Fallback)', pack.name)
        strand = 'RE' if m.group(1) == 'RE' else 'Humanities'
        half = f'{m.group(2)}_{m.group(3)}' if m.group(3) else None
        term = TERM_KEY[half] if half else 'Aut1'
        pathways = m.group(4).split('_')
        members = manifest_members(pack)
        lesson_count = 0
        weeks = collections.defaultdict(list)
        documents, zips = [], []
        # A lesson's directory is the download row's key; its label is the lesson's own week.
        lesson_dirs = {}
        for mem in members:
            if mem.endswith('_Lesson.html'):
                b = lesson_binding(pack / mem)
                lesson_dirs[str(Path(mem).parent)] = b
                lesson_count += 1
                lessons.append({'path': str((pack / mem).relative_to(ROOT)), **b, 'strand': strand, 'h1': h1_of(pack / mem), 'pack': pack.name})
        for mem in sorted(members, key=S.natural):
            p = pack / mem
            ext = Path(mem).suffix.lower()
            if ext in DOWNLOAD_EXT:
                d = str(Path(mem).parent)
                if d in lesson_dirs:
                    weeks[d].append((download_label(mem), rel(p)))
                elif ext == '.zip':
                    zips.append(('ZIP · ' + Path(mem).stem.replace('_', ' '), rel(p)))
                else:
                    documents.append((download_label(mem), rel(p)))
        start = pack / 'START_HERE.html'
        if not start.is_file():
            start = pack / 'READ_ME_FALLBACK.txt'
        for name in ('Review_record.html', 'Sources_and_checks.html', 'CHANGELOG_Final_2026-09-19.md'):
            if (pack / name).is_file():
                documents.append((name.replace('_', ' ').removesuffix('.html').removesuffix('.md'), rel(pack / name)))
        changelog = pack / 'CHANGELOG_Final_2026-09-19.md'
        proofread = changelog.is_file() and 'Proof pass 2026-09-19' in changelog.read_text(errors='replace')
        multi = len(pathways) > 1 or half is None
        week_rows = [((f'{b["pathway"]} · {TERM_LABEL[b["term"]]} · W{b["week"]}' if multi else f'W{b["week"]}'), weeks[d])
                     for d, b in sorted(lesson_dirs.items(), key=lambda kv: (kv[1]['pathway'], kv[1]['term'], kv[1]['week'])) if weeks.get(d)]
        title = f'{" & ".join(pathways)} · {TERM_LABEL[term] if half else "Autumn 1 & 2"} · {STRAND_LABEL[strand]} pack' + (' (fallback)' if pack.name.endswith('_Fallback') else '')
        card_lessons = [('lesson', L['path'].removeprefix('Humanities_Teesside/')) for L in lessons if L['pack'] == pack.name]
        cards.append({'id': pack.name, 'pathway': pathways[0] if len(pathways) == 1 else 'OTHER', 'pathway_label': ' & '.join(pathways),
                      'term': term, 'term_label': TERM_LABEL[term] if half else 'Autumn 1 & 2', 'strand': strand, 'title': title,
                      'start_here': rel(start), 'proofread': proofread, 'lesson_count': lesson_count,
                      'weeks': week_rows, 'documents': documents,
                      'links': [('start here', rel(start))] + zips + [f for _, fs in week_rows for f in fs] + documents + card_lessons})
    # The three Autumn 1 W3-W7 packs list their zips and week files in DOWNLOADS_MANIFEST.json.
    dm = json.loads((PACKS / 'DOWNLOADS_MANIFEST.json').read_text())['pathways']
    for pathway, spec in dm.items():
        base = PACKS / pathway
        zips = [(f'ZIP · {"Complete pack" if k == "complete" else DOWNLOAD_EXT["." + k] + " collection"}', rel(base / 'downloads' / v)) for k, v in spec['zips'].items()]
        week_rows = []
        for w in spec['weeks']:
            files = [(('Pupil ' if 'Pupil' in f else 'Teacher ' if 'Teacher' in f else 'Lesson ') + DOWNLOAD_EXT[Path(f).suffix.lower()], rel(base / f))
                     for f in w['files'] if Path(f).suffix.lower() in DOWNLOAD_EXT]
            week_rows.append((f'W{w["week"]}', files))
        start = rel(base / spec['start_here']['pdf'])
        documents = [('Start here (DOCX)', rel(base / spec['start_here']['docx'])), ('Teacher notes', rel(base / 'Teacher_Notes.html')), ('Pupil resources', rel(base / 'Pupil_Resources.html'))]
        cards.append({'id': f'{pathway}_Autumn1_W3-W7', 'pathway': pathway, 'pathway_label': pathway, 'term': 'Aut1', 'term_label': TERM_LABEL['Aut1'],
                      'strand': 'Humanities', 'title': f'{pathway} · Autumn 1 · Weeks 3–7 · {spec["topic"]}', 'start_here': start,
                      'proofread': False, 'lesson_count': len(spec['weeks']), 'weeks': week_rows, 'documents': documents,
                      'links': [('start here', start)] + zips + [f for _, fs in week_rows for f in fs] + documents})
    order = {'Aut1': 0, 'Aut2': 1, 'Spr1': 2, 'Spr2': 3}
    cards.sort(key=lambda c: (order[c['term']], c['strand'] != 'Humanities', ['BUILD', 'GROW', 'LAUNCH', 'OTHER'].index(c['pathway']), c['id']))
    return cards, lessons


# ------------------------------------------------------------ derivation
lessons = STRAND['lessons']
pack_cards, pack_lessons = pack_cards_and_lessons()
SOW = sow_slots()
D = S.derive(DATA['lessons'], lessons, pack_lessons, SOW, FAMILIES, TERM_LABEL)
errors = S.c1_errors(D) + S.c2_errors(D, FAMILIES) + S.c3_errors(ROOT / 'Humanities_Teesside', pack_cards)
href_of = lambda path: '../' + path
pack_href = lambda path: path.removeprefix('Humanities_Teesside/')
strip = S.render_start_strip('Humanities', {
    'BUILD': 'People, places, festivals and the Tees', 'GROW': 'Migration, belonging and belief', 'LAUNCH': 'Migration, identity and the twentieth century'})
current_html, r1 = S.render_current(D, 'Humanities', href_of, pack_href, STRAND_LABEL, DATA['styles'])
gaps_html = S.render_gaps(D['gaps'], TERM_LABEL)
packs_html, r2 = S.render_packs(pack_cards, D['reference'], href_of, 'Humanities')
earlier_html, r3 = S.render_earlier(D['earlier'], FAMILIES, href_of, TERM_LABEL)
rendered = r1 + r2 + r3
errors += S.c4_errors(rendered, DATA['lessons'])
if errors:
    print('\n'.join(errors)); raise SystemExit(f'REFUSED: {len(errors)} control error(s); nothing written')

# ------------------------------------------------------------ page
term_options = ''.join(f'<option value="{E(term)}">{E(label)}</option>' for term, label in DATA['terms'].items() if any(r['term'] == term or term in r['terms'] for r in DATA['lessons']))
style_options = ''.join(f'<option value="{E(style)}">{E(label)}</option>' for style, label in DATA['styles'].items() if any(r['style'] == style for r in DATA['lessons']))
strand_options = ''.join(f'<option value="{E(s)}">{E(STRAND_LABEL[s])}</option>' for s in ('Humanities', 'RE'))
root_source = (ROOT / 'index.html').read_text()
header = re.search(r'<header class="header mbm-site-header".*?</header>', root_source, re.S).group(0)
header_doc = lhtml.fromstring(header)
for link in list(header_doc.xpath('//a[@href]')):
    u = urlsplit(link.get('href'))
    if u.netloc in {'madebymatt-play.uk', 'www.madebymatt-play.uk'} or u.path.rstrip('/').lower() == '/games':
        link.drop_tree()
header = lhtml.tostring(header_doc, encoding='unicode')
# Reuse the current header from the root page and the Lesson Hub house styles the
# shelves carry inline. The root page no longer holds that block (its first <style> is
# the 651-byte header media rule; the old scrape produced an unstyled hub), so the
# house block is read from its own pinned file, byte for byte. Relative platform
# assets are addressed from this shelf's own directory, not from a new shell.
base_css = re.sub(r'^/\*.*?\*/\n', '', (ROOT / 'assets/catalogue/shelf-base.css').read_text(), count=1, flags=re.S)
assert ':root{--navy:#161D3D' in base_css and base_css.count('{') == base_css.count('}') >= 200, 'shelf-base.css is not the house block'
output = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Humanities by pathway, strand and week — Made by Matt</title><meta name="description" content="Find the current Humanities and RE lesson for any week by BUILD, GROW and LAUNCH pathway, download every teaching pack, and reach earlier versions in one place.">
<meta name="theme-color" content="#161D3D"><link rel="icon" href="https://madebymatt.uk/favicon.svg">
<style>''' + base_css + '''</style><link rel="stylesheet" href="../assets/mbm-platform.css"><link rel="stylesheet" href="../assets/mbm-hub.css"><link rel="stylesheet" href="../assets/catalogue/catalogue.css"><link rel="stylesheet" href="../assets/catalogue/science-shelf.css">
<script>try{var theme=localStorage.getItem('mbm_reading_theme');if(theme&&theme!=='cream')document.documentElement.setAttribute('data-theme',theme)}catch(e){}</script>
</head><body class="mbm-hub mbm-hub-lessons hub-v2" data-mbm-estate="lessons" data-catalogue-subject="Humanities" data-catalogue-noun="resource"><a class="skip" href="#main">Skip to Humanities resources</a>''' + header + '''
<main id="main"><section class="hero hero-compact"><div class="hero-in"><nav class="lesson-breadcrumb" aria-label="Breadcrumb"><a href="/">Learning home</a><a href="../">All lessons</a></nav><p class="eyebrow">Humanities &amp; RE</p><h1>Humanities <span>by week</span></h1><p class="lead">The current lesson for every week, the packs and downloads, and the earlier versions — by pathway and strand.</p></div></section>
''' + strip + '''
<div class="toolbar" role="search" aria-label="Filter Humanities resources"><label>Search<input id="science-search" type="search" placeholder="Try: migration, maps, beliefs…" autocomplete="off"></label><label>Pathway<select id="science-pathway"><option value="">All pathways</option><option value="BUILD">BUILD</option><option value="GROW">GROW</option><option value="LAUNCH">LAUNCH</option><option value="OTHER">Shared resources</option></select></label><label>Strand<select id="science-strand"><option value="">Both strands</option>''' + strand_options + '''</select></label><label>Term<select id="science-term"><option value="">All terms</option>''' + term_options + '''</select></label><label>Teaching style<select id="science-style"><option value="">All teaching styles</option>''' + style_options + '''</select></label></div>
<p class="catalogue-links quick" aria-label="Quick filters"><a href="?term=Aut1" data-shortcut="autumn">Browse Autumn 1</a><a href="?style=full-lundy" data-shortcut="full-lundy">Full Lundy Loop versions</a><a href="Teaching_Packs/">Autumn 1 packs index</a><a href="../">All subjects →</a></p>
<div class="science-status"><p id="science-count" role="status" aria-live="polite" aria-atomic="true">''' + str(len(DATA['lessons'])) + ''' Humanities resources</p><button type="button" id="science-clear">Clear filters</button></div><p id="science-empty" class="status" hidden>No matching resources. Try a different term or clear the filters.</p>
<noscript><p class="status">All resources are listed below: current lessons first, then packs and downloads, then earlier versions. The filters need JavaScript; every link works without it.</p></noscript>
<div id="science-lessons">''' + current_html + gaps_html + packs_html + earlier_html + '''</div></main><footer class="footer"><div class="bar"><p>Made by Matt · Learn • Build • Explore</p><a href="../">Return to the Lesson Hub</a></div></footer>
<script src="../assets/catalogue/science-shelf.js"></script><script defer src="../assets/mbm-theme.js"></script><script defer src="../assets/mbm-platform.js"></script><script defer src="/hud.js"></script>
</body></html>
'''
(ROOT / 'Humanities_Teesside/index.html').write_text(output)
bindings = {
    'schema': 'humanities-hub-bindings/1', 'order': 'HUB-1',
    'strandRecordSha256': hashlib.sha256((ROOT / 'tools/catalogue/HUMANITIES_STRAND.json').read_bytes()).hexdigest(),
    'population': {'shelfRows': len(DATA['lessons']), 'rendered': len(rendered), 'currentCards': len(D['current']),
                   'alternatives': len(D['alternatives']), 'reference': len(D['reference']), 'earlier': len(D['earlier']),
                   'packLessonsFillingSlots': len(D['filled_by_pack']), 'packCards': len(pack_cards)},
    'families': dict(collections.Counter(FAMILIES.values())),
    'slots': [{'pathway': k[0], 'term': k[1], 'week': k[2], 'strand': k[3],
               'current': [L['path'] for L in s['current']] or [P['path'] for P in s['pack'][:1]],
               'currentFrom': 'shelf' if s['current'] else 'pack',
               'alternatives': [A['path'] for A in s['alternatives']],
               'packLesson': [P['path'] for P in s['pack']]}
              for k, s in sorted(D['slots'].items(), key=lambda kv: (S.PATHWAYS.index(kv[0][0]), kv[0][3], S.TERM_ORDER.index(kv[0][1]), kv[0][2]))],
    'gaps': [{'pathway': p, 'strand': s, 'term': t, 'weeks': n} for (p, s, t), n in sorted(D['gaps'].items())],
    'sowSlots': {k: len(v) for k, v in SOW.items()},
    'packs': [{'id': c['id'], 'pathway': c['pathway_label'], 'term': c['term'], 'strand': c['strand'], 'proofread': c['proofread'],
               'lessons': c['lesson_count'], 'startHere': c['start_here'], 'links': len(c['links'])} for c in pack_cards],
}
(ROOT / 'assets/catalogue/humanities-hub-bindings.json').write_text(json.dumps(bindings, indent=1, ensure_ascii=False) + '\n')
print(f'Built the Humanities hub: {len(rendered)} of {len(DATA["lessons"])} shelf cards rendered '
      f'({len(D["current"])} current + {len(D["alternatives"])} alternatives, {len(D["reference"])} reference, {len(D["earlier"])} earlier); '
      f'{len(D["filled_by_pack"])} slots filled by pack lessons; {len(pack_cards)} pack cards; gaps {sum(D["gaps"].values())}; '
      f'controls C1-C4 0 errors.')
