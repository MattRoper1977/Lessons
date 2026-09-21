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
"current" = THE SERVED LESSON FOR EACH WEEK (ORDER SCI-COMPLETE, ruling of 2026-09-22 on
STOP-F1). A lesson is demoted to Earlier versions only where a conforming replacement EXISTS --
that is, another route bound to the SAME pathway, term and week whose own bytes carry the exemplar
chassis AND which is the SAME part of that week (the deck's own lesson-config kind). Conformance
alone never demotes: until PASS C delivers replacements, every lesson pupils use today stays
current, carrying a CONFORMS or NOT YET badge derived from the census. The badge flips as PASS C
lands. A route whose part cannot be read from its lesson-config is NEVER treated as replaced -- a
replacement has to be shown to exist, not assumed.
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
DOWNLOADS = json.loads((ROOT / 'assets/catalogue/science-download-bindings.json').read_text())
E = H.escape
TERM_LABEL = DATA['terms']
DOWNLOAD_EXT = {'.pdf': 'PDF', '.docx': 'DOCX', '.pptx': 'PPTX', '.zip': 'ZIP', '.html': 'HTML', '.txt': 'TXT'}
CONFORMING = set(CENSUS['conforming'])
assert CENSUS.get('schema') == 'science-chassis-census/1' and CENSUS.get('routes') == len(DATA['lessons']), 'the census is not this shelf\'s'
for p in CONFORMING:
    assert CENSUS['entries'][p]['sha256'] == hashlib.sha256((ROOT / p).read_bytes()).hexdigest(), f'the census was measured on other bytes: {p}'


TITLE_MAX = 120  # a card title is a lesson name, not a page of slide text (C6)


def h1_of(path: Path) -> str:
    """The deck's OWN first heading, read with a parser -- never a regex over the raw bytes.

    31 Science decks write their printable packs from a script, so their source carries
    <h1>Knowledge organiser<\\/h1> INSIDE a JavaScript string. A regex hunting for </h1> steps
    straight over the escaped close and runs on to the next REAL one: measured on
    SCI_G_W10A_Solar_System_Research_Explore.html that turned 86 KB of slide text into a
    49,963-character card title (and a 1.12 MB hub that scrolled sideways at 390 px). A parser
    keeps script content in a text node, so a heading written inside one is never markup.
    """
    doc = lhtml.fromstring(path.read_bytes())
    for e in doc.iter('h1'):
        text = ' '.join(e.text_content().split()).strip()
        if text:
            return text
    t = doc.find('.//title')
    title = ' '.join((t.text_content() if t is not None else '').split()).strip()
    return re.split(r'\s+[|—]\s+', title)[0].strip() if title else path.stem


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


# ------------------------------------------------------------ replacement, and route families
PART = {r['path']: part_of(ROOT / r['path']) for r in DATA['lessons']}


def replaced_routes() -> dict[str, str]:
    """The ONLY lessons the ruling lets us demote: a route bound to a (pathway, term, week) slot
    where a CONFORMING route sits in the same slot AND is the same part of the week. Returns
    {replaced path: the conforming route that replaces it}. A part of None is not a part: it
    matches nothing, because a replacement must be shown, never assumed."""
    slots: dict[tuple, list[str]] = collections.defaultdict(list)
    for r in DATA['lessons']:
        e = WEEKS.get(r['path']) or {}
        for w in (e.get('weeks') or []):
            slots[(e['pathway'], w['term'], w['weekWithinTerm'])].append(r['path'])
    out: dict[str, str] = {}
    for members in slots.values():
        conformers = [p for p in members if p in CONFORMING]
        for cand in members:
            if cand in CONFORMING or PART[cand] is None:
                continue
            match = next((c for c in conformers if PART[c] is not None and PART[c] == PART[cand]), None)
            if match:
                out[cand] = match
    return out


REPLACED = replaced_routes()


def family(path: str) -> str:
    if Path(path).name.startswith('START_HERE'):
        return 'reference'
    if path in REPLACED:
        style = (WEEKS.get(path) or {}).get('style') or next((r['style'] for r in DATA['lessons'] if r['path'] == path), 'earlier')
        return f'recorded {style}'
    return 'current'


FAMILIES = {r['path']: family(r['path']) for r in DATA['lessons']}


# --------------------------------------------- strand rows (every served lesson, badged)
CONFORMS_PILL = '<span class="pill ok" data-conforms="1">CONFORMS</span>'
NOT_YET_PILL = '<span class="pill" data-conforms="0">NOT YET</span>'


def strand_rows() -> list[dict]:
    """Every lesson that is current under the ruling -- the served lesson for its week -- each
    carrying the badge the census earns it. Only a proven same-part replacement is left out."""
    rows = []
    for path in sorted(r['path'] for r in DATA['lessons'] if FAMILIES[r['path']] == 'current'):
        e = WEEKS.get(path) or {}
        weeks = e.get('weeks') or [None]
        for w in weeks:
            rows.append({'path': path, 'pathway': e.get('pathway') or next(r['pathway'] for r in DATA['lessons'] if r['path'] == path),
                         'term': (w['term'] if w else next(r['term'] for r in DATA['lessons'] if r['path'] == path)),
                         'week': (w['weekWithinTerm'] if w else None), 'strand': 'Science', 'h1': h1_of(ROOT / path),
                         'alternative': False, 'part': PART[path],
                         'badges': CONFORMS_PILL if path in CONFORMING else NOT_YET_PILL})
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


def c5_errors(d: dict, conforming: set, replaced: dict[str, str]) -> list[str]:
    """PASS F under the ruling of 2026-09-22: CURRENT = THE SERVED LESSON FOR THE WEEK.
    Red if a served lesson was dropped from current without a proven replacement (the thing the
    ruling exists to prevent), if a replaced lesson is still shown as current, if a conforming
    route is not current, or if any current card carries the wrong badge."""
    served = {r['path'] for r in DATA['lessons'] if not Path(r['path']).name.startswith('START_HERE')}
    errs = [f'C5 served lesson dropped from current with no conforming replacement: {p}'
            for p in sorted(served - d['current'] - set(replaced))]
    errs += [f'C5 replaced lesson still rendered current: {p} (replaced by {replaced[p]})'
             for p in sorted(set(replaced) & d['current'])]
    errs += [f'C5 conforming route not rendered current: {p}' for p in sorted(conforming - d['current'])]
    for row in lessons:
        want = CONFORMS_PILL if row['path'] in conforming else NOT_YET_PILL
        if row['badges'] != want:
            errs.append(f'C5 wrong badge on a current card: {row["path"]}')
    return errs


errors += c5_errors(D, CONFORMING, REPLACED)
href_of = lambda path: '../' + path
pack_href = lambda path: path.removeprefix('Science_Teesside/')
blurb, start_hrefs = {}, {}
for pw in S.PATHWAYS:
    sh = ROOT / 'Science_Teesside' / pw.capitalize() / 'START_HERE.html'
    assert sh.is_file(), f'no START_HERE page for {pw}'
    blurb[pw] = h1_of(sh)
    start_hrefs[pw] = f'{pw.capitalize()}/START_HERE.html'
def bound_weeks(row):
    """The RECORDED week this card stands for, as science-shelf.js filters it.

    A current row IS one binding: strand_rows() emits one row per bound week, so the route the
    record binds to two weeks produces two cards, one in each week row (the ruling of 2026-09-22
    on STOP-F2: "a route bound to two weeks may render twice"). Each card therefore carries ITS
    OWN week, not the route's whole list. Carrying the list would put "3 4" on both cards, and a
    reader filtering to Week 3 would be shown the same lesson twice with identical text -- the
    duplication the DISTINCT control exists to forbid, arriving through the filter instead of the
    slot. Measured before the fix: ?pathway=LAUNCH&term=Spr1&week=3 showed 3 cards for 2 routes.

    Rows the record binds to no week keep the old shelf's exact contract: 'unspecified' and
    'Week not specified' (check_catalogue_dom.cjs proves the week filter and the honest label).
    A row that names no week of its own -- an earlier-family or pack card -- keeps the whole
    recorded list, which is what those surfaces have always shown.
    """
    ws = (WEEKS.get(row['path']) or {}).get('weeks') or []
    own = row.get('week')
    if own is not None:
        mine = [w for w in ws if w['weekWithinTerm'] == own and w['term'] == row.get('term')]
        if mine:
            return (' '.join(str(w['weekWithinTerm']) for w in mine),
                    '; '.join(w['label'] for w in mine))
    return (' '.join(str(w['weekWithinTerm']) for w in ws) or 'unspecified',
            '; '.join(w['label'] for w in ws) or 'Week not specified')
S.CARD_WEEK_HOOK = bound_weeks


def download_link(path: str) -> str:
    """The route's recorded Teaching Packs section, straight from the reviewed record -- the link
    the shelf carried before PASS F ("PowerPoint, Word and PDF downloads →"), restored on the HUB-1
    card. A route the record does not bind carries nothing; the text is never composed here."""
    href = DOWNLOADS.get(path)
    return f'<p><a class="go" href="{E(href, quote=True)}">PowerPoint, Word and PDF downloads →</a></p>' if href else ''


S.CARD_DOWNLOAD_HOOK = download_link
WEEK_MAX = max((w['weekWithinTerm'] for e in WEEKS.values() for w in e.get('weeks', [])), default=8)
shortcuts = ('<div class="catalogue-links"><a href="?pathway=LAUNCH" data-shortcut="all-launch">All LAUNCH Science</a>'
             '<a href="?pathway=LAUNCH&amp;term=Aut1&amp;style=recommended" data-shortcut="recommended">LAUNCH Science pack · Autumn 1 Weeks 3–7</a>'
             '<a href="?style=full-lundy" data-shortcut="full-lundy">Browse full Lundy Loop versions</a></div>')
strip = S.render_start_strip('Science', blurb, start_hrefs) + shortcuts
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


def c6_errors(rows: list[dict]) -> list[str]:
    """C6. A card title is a title: one line, at most TITLE_MAX characters. Longer means the
    reader is being shown the deck's slide text instead of its lesson name."""
    return [f'C6 card title is not a title ({len(r["h1"])} characters): {r["path"]}'
            for r in sorted(rows, key=lambda r: r['path']) if len(r['h1']) > TITLE_MAX or '\n' in r['h1']]


def c7_errors(page: str, rendered_paths: list[str]) -> list[str]:
    """C7. Every rendered route the download record binds carries THAT record's link, once per
    card; no card carries one the record does not bind."""
    errs, carried = [], set()
    for path, body in re.findall(r'<article class="card[^"]*" data-lesson-path="([^"]+)"(.*?)</article>', page, re.S):
        want = DOWNLOADS.get(path)
        got = re.findall(r'<a class="go" href="([^"]+)">PowerPoint, Word and PDF downloads', body)
        if got:
            carried.add(path)
        if want and got != [E(want, quote=True)]:
            errs.append(f'C7 recorded downloads link missing or wrong on a card: {path} (record {want}, card {got})')
        if not want and got:
            errs.append(f'C7 downloads link on a route the record does not bind: {path}')
    errs += [f'C7 bound route rendered with no downloads link: {p}'
             for p in sorted(set(rendered_paths) & set(DOWNLOADS) - carried)]
    return errs


page_cards = current_html + packs_html + earlier_html
errors += c6_errors(lessons) + c7_errors(page_cards, rendered)
if errors:
    print('\n'.join(errors)); raise SystemExit(f'REFUSED: {len(errors)} control error(s); nothing written')

served_by_earlier = collections.Counter()
for r in D['earlier']:
    for w in (WEEKS.get(r['path']) or {}).get('weeks', []):
        served_by_earlier[(r['pathway'], w['term'])] += 1
note_items = ''.join(f'<li>{E(p)} · {E(TERM_LABEL.get(t, t))}: {n} lessons</li>' for (p, t), n in sorted(served_by_earlier.items(), key=lambda kv: (S.PATHWAYS.index(kv[0][0]), (S.TERM_ORDER.index(kv[0][1]) if kv[0][1] in S.TERM_ORDER else len(S.TERM_ORDER)))))
conforming_now = len([r for r in DATA['lessons'] if r['path'] in CONFORMING])
not_yet_now = len(D['current']) - conforming_now
note_html = (f'<details class="hub-gaps" id="pre-chassis"><summary>How these lessons are badged · {conforming_now} CONFORMS, {not_yet_now} NOT YET</summary>'
             f'<p class="hub-note">Current shows the lesson each week is actually taught from. A lesson is only moved to Earlier versions once a replacement for that same part of the week exists; until then it stays here, badged NOT YET, because it is the lesson being used. CONFORMS means the lesson\u2019s own bytes carry the exemplar chassis (the PASS B census); the badge changes as lessons are rebuilt.</p><ul>{note_items}</ul></details>')

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
<div class="toolbar" role="search" aria-label="Filter Science lessons"><label>Search<input id="science-search" type="search" placeholder="Try: osmosis, muscles, fossils…" autocomplete="off"></label><label>Pathway<select id="science-pathway"><option value="">All pathways</option><option value="BUILD">BUILD</option><option value="GROW">GROW</option><option value="LAUNCH">LAUNCH</option></select></label><label>Strand<select id="science-strand"><option value="">All strands</option><option value="Science">Science</option></select></label><label>Term<select id="science-term"><option value="">All terms</option>''' + term_options + '''</select></label><label>Week within term<select id="science-week"><option value="">All weeks</option>''' + ''.join(f'<option value="{n}">Week {n}</option>' for n in range(1, WEEK_MAX + 1)) + '''<option value="unspecified">Week not specified</option></select></label><label>Teaching style<select id="science-style"><option value="">All teaching styles</option>''' + style_options + '''</select></label></div>
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
print(f'Built the Science hub: {len(rendered)} of {len(DATA["lessons"])} shelf cards rendered '
      f'({len(D["current"])} current = {conforming_now} CONFORMS + {not_yet_now} NOT YET, {len(D["reference"])} reference, '
      f'{len(D["earlier"])} earlier, of which {len(REPLACED)} have a proven same-part conforming replacement); '
      f'{len(D["slots"])} current slots; {len(cards)} pack cards; controls C1-C7 0 errors.')
