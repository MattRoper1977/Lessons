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
  assets/catalogue/science-hub-bindings.json       the derivation: population, families, slots (in
                                                   rendered order), earlier counts, packs
"current" = THE SERVED LESSON FOR EACH WEEK (ORDER SCI-COMPLETE, ruling of 2026-09-22 on
STOP-F1), ordered and filtered by GENERATION, never by style (Matt's ruling on the S02 STOP,
2026-09-22):
  1. the decks in the week's dated folder (one named _YYYY-YY), or in the pathway's own folder
     where no dated folder serves the week -- non-Classic decks first, in lesson order;
  2. then the Classic in that same folder;
  3. older copies (v3_40min, Slideshows) move to Earlier versions wherever a newer generation
     serves the same week. A week never loses its served lesson.
Style ("Full Lundy Loop" / "earlier") and CONFORMS / NOT YET are BADGES on the card, never
ordering or membership keys. PASS C is an in-place transplant: a lesson is rebuilt at its own
route (replacements in place), so its CONFORMS / NOT YET badge flips as PASS C lands and the
card does not move. A Classic is the deck's own declaration -- its head <title>, or its
lesson-config key, prefix, title or stage lesson -- never its file name.
The writer refuses to write while any C1-C10 control is red. --self-test runs the red proofs, reads
the ordering back from the RENDERED page, and fails while any control is red.
"""
from pathlib import Path
import collections, hashlib, html as H, json, re, sys
from lxml import html as lhtml
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hub_sections as S
from title_slide import title_slide_heading   # RULING 2026-09-23 B.2, one definition

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
    """The deck's listed title: its TITLE SLIDE's heading, falling back only off a deck.

    The parser rule below is kept for pages that carry no slides at all (hub and shelf pages).
    31 Science decks write their printable packs from a script, so their source carries
    <h1>Knowledge organiser<\\/h1> INSIDE a JavaScript string. A regex hunting for </h1> steps
    straight over the escaped close and runs on to the next REAL one: measured on
    SCI_G_W10A_Solar_System_Research_Explore.html that turned 86 KB of slide text into a
    49,963-character card title (and a 1.12 MB hub that scrolled sideways at 390 px). A parser
    keeps script content in a text node, so a heading written inside one is never markup.
    """
    raw = path.read_bytes()
    heading = title_slide_heading(raw.decode('utf-8', 'replace'))
    if heading:
        return heading
    doc = lhtml.fromstring(raw)
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


# ------------------------------------------- generation, and route families (ruling on S02)
PART = {r['path']: part_of(ROOT / r['path']) for r in DATA['lessons']}
OLDER_COPY_FOLDERS = ('v3_40min', 'Slideshows')
OLDER_COPY_LABEL = {'v3_40min': '40-minute copy', 'Slideshows': 'Slideshows series'}
DATED_FOLDER = re.compile(r'_\d{4}-\d{2}$')
GENERATION_RANK = {'dated': 0, 'pathway': 1, 'older copy': 2}


def generation(path: str) -> str:
    """'dated' (a folder named _YYYY-YY), 'older copy' (v3_40min / Slideshows) or 'pathway' (the
    pathway's own folder). Read off the folder each generation was filed in."""
    folder = Path(path).parent.name
    if folder in OLDER_COPY_FOLDERS:
        return 'older copy'
    return 'dated' if DATED_FOLDER.search(folder) else 'pathway'


def declared_classic(path: str) -> bool:
    """A Classic by the deck's OWN declaration, never its file name: a 'Classic' segment in its head
    <title>, or its lesson-config naming itself Classic (key, prefix or title, or a stage's lesson).
    Measured 2026-09-22: 5 of the 6 *_Classic files declare it; the sixth (SCI_B_W13) declares
    nothing and serves its week alone, which C9 proves harmless."""
    raw = (ROOT / path).read_text(encoding='utf-8', errors='replace')
    heads = lhtml.fromstring(raw.encode('utf-8')).xpath('/html/head/title')
    if heads and any(seg.strip().lower() == 'classic' for seg in heads[0].text_content().split('\u00b7')):
        return True
    m = re.search(r'<script[^>]*id="lesson-config"[^>]*>(.*?)</script>', raw, re.S)
    try:
        cfg = json.loads(m.group(1)) if m else None
    except ValueError:
        cfg = None
    if not isinstance(cfg, dict):
        return False
    word = re.compile(r'(?<![A-Za-z])Classic(?![A-Za-z])')
    if any(isinstance(cfg.get(k), str) and word.search(cfg[k]) for k in ('key', 'prefix', 'title')):
        return True
    return any(isinstance(st, dict) and st.get('lesson') == 'Classic' for st in (cfg.get('stages') or []))


CLASSIC = {r['path']: declared_classic(r['path']) for r in DATA['lessons']}
SLOTS: dict[tuple, list[str]] = collections.defaultdict(list)
for _r in DATA['lessons']:
    _e = WEEKS.get(_r['path']) or {}
    for _w in (_e.get('weeks') or []):
        SLOTS[(_e['pathway'], _w['term'], _w['weekWithinTerm'])].append(_r['path'])


def older_copies(slots: dict[tuple, list[str]] = SLOTS) -> dict[str, str]:
    """{older copy: a newer-generation route serving its week}. An older copy leaves current only
    where a newer generation serves EVERY week it is bound to, so no week loses its lesson."""
    bound: dict[str, list[tuple]] = collections.defaultdict(list)
    for k, members in slots.items():
        for p in members:
            bound[p].append(k)
    out: dict[str, str] = {}
    for path, keys in bound.items():
        if generation(path) != 'older copy':
            continue
        newer = [next((p for p in slots[k] if generation(p) != 'older copy'), None) for k in keys]
        if keys and all(newer):
            out[path] = newer[0]
    return out


OLDER = older_copies()


def within_week(current: list[dict]) -> list[dict]:
    """The ruled within-week order: generation, then a deck's Classic after it, then lesson order
    (natural path: A before B, L1 before L2). Never style, never a badge."""
    return sorted(current, key=lambda L: (GENERATION_RANK[generation(L['path'])], CLASSIC.get(L['path'], False),
                                           S.natural(L['path'])))


S.CURRENT_ORDER_HOOK = within_week


def family(path: str) -> str:
    if Path(path).name.startswith('START_HERE'):
        return 'reference'
    if path in OLDER:
        return OLDER_COPY_LABEL[Path(path).parent.name]     # the card's visible family label
    return 'current'


FAMILIES = {r['path']: family(r['path']) for r in DATA['lessons']}


# --------------------------------------------- strand rows (every served lesson, badged)
CONFORMS_PILL = '<span class="pill ok" data-conforms="1">CONFORMS</span>'
NOT_YET_PILL = '<span class="pill" data-conforms="0">NOT YET</span>'


def strand_rows() -> list[dict]:
    """Every lesson that is current under the ruling -- the served lesson for its week -- each
    carrying the badge the census earns it. Only an older copy a newer generation replaces in
    every week it serves is left out; it moves to Earlier versions."""
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


def c5_errors(d: dict, conforming: set, older: dict[str, str], rows: list[dict]) -> list[str]:
    """CURRENT = THE SERVED LESSON FOR THE WEEK, by generation (ruling on S02, 2026-09-22).
    Red if a served lesson left current without being an older copy a newer generation replaces,
    if an older copy is still current beside a newer generation, or if any current card carries
    the wrong badge. Conformance decides the badge only, never membership."""
    served = {r['path'] for r in DATA['lessons'] if not Path(r['path']).name.startswith('START_HERE')}
    errs = [f'C5 served lesson dropped from current, and not an older copy a newer generation replaces: {p}'
            for p in sorted(served - d['current'] - set(older))]
    errs += [f'C5 older copy still rendered current beside a newer generation: {p} (newer: {older[p]})'
             for p in sorted(set(older) & d['current'])]
    for row in rows:
        want = CONFORMS_PILL if row['path'] in conforming else NOT_YET_PILL
        if row['badges'] != want:
            errs.append(f'C5 wrong badge on a current card: {row["path"]}')
    return errs


errors += c5_errors(D, CONFORMING, OLDER, lessons)
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
    return f'<p class="downloads-link"><a href="{E(href, quote=True)}">PowerPoint, Word and PDF downloads →</a></p>' if href else ''


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
        got = re.findall(r'<p class="downloads-link"><a href="([^"]+)">PowerPoint, Word and PDF downloads', body)
        if got:
            carried.add(path)
        if want and got != [E(want, quote=True)]:
            errs.append(f'C7 recorded downloads link missing or wrong on a card: {path} (record {want}, card {got})')
        if not want and got:
            errs.append(f'C7 downloads link on a route the record does not bind: {path}')
    errs += [f'C7 bound route rendered with no downloads link: {p}'
             for p in sorted(set(rendered_paths) & set(DOWNLOADS) - carried)]
    return errs


def c8_errors(rows: list[dict]) -> list[str]:
    """C8. A card title is the deck's OWN TITLE SLIDE's heading -- never another slide's.

    RULING 2026-09-23 B.2. The defect this stands against is silent: a first-<h1>-in-the-document
    rule returns a task slide's heading whenever the title slide writes its heading as an <h2>,
    and the hub then lists a lesson as "Your task * 1 of 2". Measured on main before the fix:
    six served pages carried that string, five decks plus the hub itself.

    The control re-reads each deck and refuses when the listed title is not what the title slide
    says. It names the first-<h1> case separately, because that is the defect with a history and a
    reader should not have to infer it from a diff of two strings.
    """
    errs = []
    for r in sorted(rows, key=lambda r: r['path']):
        path = ROOT / r['path']
        if not path.is_file():
            continue
        raw = path.read_bytes()
        want = title_slide_heading(raw.decode('utf-8', 'replace'))
        if want is None or r['h1'] == want:
            continue
        doc = lhtml.fromstring(raw)
        first = next((' '.join(e.text_content().split()).strip()
                      for e in doc.iter('h1') if ' '.join(e.text_content().split()).strip()), None)
        if r['h1'] == first:
            errs.append(f'C8 card title is the document\'s first <h1>, not the title slide\'s heading: '
                        f'{r["path"]} (listed {r["h1"]!r}, title slide {want!r})')
        else:
            errs.append(f'C8 card title is not the title slide\'s heading: '
                        f'{r["path"]} (listed {r["h1"]!r}, title slide {want!r})')
    return errs


# C10 reads the folder names LITERALLY rather than through OLDER_COPY_FOLDERS / generation(), so a
# change to those cannot switch off the check that is meant to catch it (review of the first cut:
# with OLDER_COPY_FOLDERS emptied, every v3_40min copy rendered current and C5 and C9, both built on
# generation(), stayed green).
C10_OLDER_COPY = re.compile(r'/(?:v3_40min|Slideshows)/[^/]+$')


def rendered_week_rows(current_page: str) -> dict[tuple, list[str]]:
    """{(pathway, term, week): [lesson paths, in rendered order]}, read off the page itself."""
    doc = lhtml.fromstring(f'<div>{current_page}</div>')
    out: dict[tuple, list[str]] = {}
    for row in doc.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " week-row ")]'):
        pw = row.xpath('ancestor::details[@data-pathway][1]/@data-pathway')
        term = row.xpath('ancestor::section[@data-term][1]/@data-term')
        key = (pw[0] if pw else '', term[0] if term else '', row.get('data-week'))
        out.setdefault(key, []).extend(a.get('data-lesson-path') for a in row.xpath('.//article[@data-lesson-path]'))
    return out


def c9_errors(current_page: str, slots: dict[tuple, list[str]], current: set, classic: dict[str, bool]) -> list[str]:
    """C9. The generation order, read back from the RENDERED page, not from the hook that wrote it.
    Red if a week is served by two dated folders (choosing the newest would need a date no record
    carries), if a week has no current lesson, if a file named Classic that does not declare it
    shares its week (its place would rest on a file name), or if a week row renders a later
    generation or a Classic ahead of an earlier generation or a non-Classic, or breaks lesson order
    inside one generation (A before B, L1 before L2).
    C10. Red if a week row renders an older copy (a v3_40min or Slideshows file) beside a lesson
    from any other folder: the ruling moves it to Earlier versions wherever a newer generation
    serves its week."""
    errs = []
    for k, members in sorted(slots.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        dated = sorted({str(Path(p).parent) for p in members if generation(p) == 'dated'})
        if len(dated) > 1:
            errs.append(f'C9 week served by two dated folders, so "newest" would need a date no record carries: {k}: {dated}')
        if not any(p in current for p in members):
            errs.append(f'C9 week left with no current lesson: {k}')
        if len(members) > 1:
            errs += [f'C9 a file named Classic that does not declare it shares its week: {p}'
                     for p in members if Path(p).stem.endswith('_Classic') and not classic.get(p)]
    doc = lhtml.fromstring(f'<div>{current_page}</div>')
    for row in doc.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " week-row ")]'):
        paths = [a.get('data-lesson-path') for a in row.xpath('.//article[@data-lesson-path]')]
        ranks = [(GENERATION_RANK[generation(p)], classic.get(p, False)) for p in paths]
        if ranks != sorted(ranks):
            errs.append(f'C9 week row out of generation order (headline {paths[0]}): ' + ', '.join(paths))
        elif [(r, S.natural(p)) for r, p in zip(ranks, paths)] != sorted((r, S.natural(p)) for r, p in zip(ranks, paths)):
            errs.append(f'C9 week row out of lesson order inside one generation: ' + ', '.join(paths))
        older = [p for p in paths if C10_OLDER_COPY.search(p)]
        if older and len(older) < len(paths):
            errs.append(f'C10 older copy rendered current beside a newer generation: ' + ', '.join(paths))
    return errs


page_cards = current_html + packs_html + earlier_html
errors += c6_errors(lessons) + c7_errors(page_cards, rendered) + c8_errors(lessons)
errors += c9_errors(current_html, SLOTS, D['current'], CLASSIC)
ROWS = rendered_week_rows(current_html)


def self_test() -> int:
    """Red proofs for the ruling on the S02 STOP, planted against the functions the hub is built by."""
    week = lambda pw, t, n: [L for L in lessons if L['pathway'] == pw and L['term'] == t and L['week'] == n]
    old_order = lambda rows: sorted(rows, key=lambda L: L.get('part') or '')   # hub_sections' default before the hook
    g1, g2 = week('GROW', 'Aut2', 1), week('GROW', 'Aut2', 2)
    dated = 'Science_Teesside/Grow/W8-W13_2026-27/'
    planted_slots = {('GROW', 'Aut2', 1): [dated + 'X_Explore.html', 'Science_Teesside/Grow/v3_40min/X_v3.html']}
    two_dated = {('GROW', 'Aut2', 1): [dated + 'X.html', 'Science_Teesside/Grow/W14-W20_2026-27/Y.html']}
    classic_first = ('<div class="week-row" data-week="1"><article data-lesson-path="' + g1[0]['path'] + '"></article>'
                     + ''.join(f'<article data-lesson-path="{L["path"]}"></article>' for L in g1 if not CLASSIC[L['path']])
                     + '</div>')
    classic_path = next(L['path'] for L in g1 if CLASSIC[L['path']])
    classic_first = classic_first.replace(g1[0]['path'], classic_path, 1)
    checks = [
        ('RED PROOF: before the ruling, GROW Aut2 W1 headlined its Classic', CLASSIC[old_order(g1)[0]['path']]),
        # Read off the RENDERED page, not from within_week(): the review of the first cut unhooked
        # the order and these checks, then calling the hook directly, stayed green.
        ('GROW Aut2 W1 on the page headlines the dated folder\'s non-Classic, SCI_G_W8A_Day_And_Night_Explore',
         ROWS.get(('GROW', 'Aut2', '1'), [''])[0].endswith('/SCI_G_W8A_Day_And_Night_Explore.html')),
        ('GROW Aut2 W1 on the page: the Classic comes after every non-Classic',
         [CLASSIC[p] for p in ROWS.get(('GROW', 'Aut2', '1'), [])] == sorted(CLASSIC[L['path']] for L in g1)
         and any(CLASSIC[L['path']] for L in g1)),
        # Matt's named check. It already held before the ruling -- the W9 Classic is bound to Aut2
        # W1, not W2 -- so it is kept as a control, and the W1 checks above are the red proof.
        ("Matt's check, on the page: GROW Aut2 W2's headline is SCI_G_W9A_Spherical_Bodies_Explore, not a Classic",
         ROWS.get(('GROW', 'Aut2', '2'), [''])[0].endswith('/SCI_G_W9A_Spherical_Bodies_Explore.html')),
        ('RED PROOF: C9 reds a week row that renders the Classic first',
         any('out of generation order' in e for e in c9_errors(classic_first, {}, set(), CLASSIC))),
        ('RED PROOF: C9 reds a week row out of lesson order inside one generation',
         any('out of lesson order' in e for e in c9_errors(
             '<div class="week-row"><article data-lesson-path="' + dated + 'X_W9B_Do.html"></article>'
             '<article data-lesson-path="' + dated + 'X_W9A_Explore.html"></article></div>', {}, set(), {}))),
        ('RED PROOF: C10 reds an older copy rendered beside a newer generation, read from its folder alone',
         any(e.startswith('C10 ') for e in c9_errors(
             '<div class="week-row"><article data-lesson-path="' + dated + 'X_Explore.html"></article>'
             '<article data-lesson-path="Science_Teesside/Grow/v3_40min/X_v3.html"></article></div>', {}, set(), {}))),
        ('the page as built passes every control, C1-C10: 0 errors', not errors),
        ('RED PROOF: an older copy beside a dated deck leaves current',
         older_copies(planted_slots) == {'Science_Teesside/Grow/v3_40min/X_v3.html': dated + 'X_Explore.html'}),
        ('an older copy that alone serves its week stays current (no week loses its lesson)',
         older_copies({('GROW', 'Aut2', 1): ['Science_Teesside/Grow/v3_40min/X_v3.html']}) == {}),
        ('RED PROOF: C5 reds an older copy still rendered current',
         any('older copy still rendered current' in e for e in c5_errors({'current': {'Science_Teesside/Grow/v3_40min/X_v3.html'}}, set(), {'Science_Teesside/Grow/v3_40min/X_v3.html': 'x'}, []))),
        ('RED PROOF: C9 reds a week served by two dated folders',
         any('two dated folders' in e for e in c9_errors('', two_dated, {'Science_Teesside/Grow/W14-W20_2026-27/Y.html'}, {}))),
        ('RED PROOF: C9 reds a week with no current lesson',
         any('no current lesson' in e for e in c9_errors('', planted_slots, set(), {}))),
        ('every v3_40min copy on the shelf leaves current (measured 35)',
         len(OLDER) == 35 and all(generation(p) == 'older copy' for p in OLDER)),
        ('no Classic is decided by its file name where it shares a week',
         not any('file named Classic' in e for e in c9_errors('', SLOTS, D['current'], CLASSIC))),
        ('style and badge are not order keys: reversing every style leaves the order unchanged',
         [L['path'] for L in within_week(g1)] == [L['path'] for L in within_week([{**L, 'style': 'x' + L.get('style', ''), 'badges': ''} for L in reversed(g1)])]),
    ]
    for name, ok in checks:
        print(f'  {"PASS" if ok else "FAIL"}  {name}')
    bad = sum(1 for _, ok in checks if not ok)
    print(f'build_science_hub self-test: {len(checks) - bad} of {len(checks)} PASS')
    return 1 if bad else 0


if '--self-test' in sys.argv:
    raise SystemExit(self_test())
if errors:
    print('\n'.join(errors)); raise SystemExit(f'REFUSED: {len(errors)} control error(s); nothing written')

served_by_earlier = collections.Counter()
for r in D['earlier']:
    for w in (WEEKS.get(r['path']) or {}).get('weeks', []):
        served_by_earlier[(r['pathway'], w['term'])] += 1
note_items = ''.join(f'<li>{E(p)} · {E(TERM_LABEL.get(t, t))}: {n} lessons</li>' for (p, t), n in sorted(served_by_earlier.items(), key=lambda kv: (S.PATHWAYS.index(kv[0][0]), (S.TERM_ORDER.index(kv[0][1]) if kv[0][1] in S.TERM_ORDER else len(S.TERM_ORDER)))))
conforming_now = len([r for r in DATA['lessons'] if r['path'] in CONFORMING])
not_yet_now = len(D['current']) - conforming_now
note_html = (f'<details class="hub-gaps" id="pre-chassis"><summary>How these lessons are ordered and badged · {conforming_now} CONFORMS, {not_yet_now} NOT YET</summary>'
             f'<p class="hub-note">Each week lists its newest lessons first: the lessons in that week\u2019s newest folder, then that folder\u2019s Classic. Older 40-minute copies sit in Earlier versions. CONFORMS means the lesson\u2019s own bytes carry the exemplar chassis (the PASS B census); NOT YET means they do not yet. The badge changes as lessons are rebuilt in place, and it never changes a lesson\u2019s position.</p>'
             f'<p class="hub-note">Older copies now in Earlier versions, by pathway and term:</p><ul>{note_items}</ul></details>')

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
<style>''' + base_css + '''</style><link rel="stylesheet" href="../assets/mbm-platform.css"><link rel="stylesheet" href="../assets/mbm-hub.css"><link rel="stylesheet" href="../assets/catalogue/catalogue.css"><link rel="stylesheet" href="../assets/catalogue/science-shelf.css">
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
    'slots': [{'pathway': k[0], 'term': k[1], 'week': k[2], 'current': [{'path': L['path'], 'part': L.get('part')} for L in within_week(s['current'])]}
              for k, s in sorted(D['slots'].items(), key=lambda kv: (S.PATHWAYS.index(kv[0][0]), (S.TERM_ORDER.index(kv[0][1]) if kv[0][1] in S.TERM_ORDER else len(S.TERM_ORDER)), kv[0][2] is None, kv[0][2] or 0))],
    'earlierByPathwayTerm': [{'pathway': p, 'term': t, 'lessons': n} for (p, t), n in sorted(served_by_earlier.items())],
    'packs': [{'id': c['id'], 'pathway': c['pathway'], 'lessons': c['lesson_count'], 'startHere': c['start_here'], 'links': len(c['links'])} for c in cards],
}
(ROOT / 'assets/catalogue/science-hub-bindings.json').write_text(json.dumps(bindings, indent=1, ensure_ascii=False) + '\n')
print(f'Built the Science hub: {len(rendered)} of {len(DATA["lessons"])} shelf cards rendered '
      f'({len(D["current"])} current = {conforming_now} CONFORMS + {not_yet_now} NOT YET, {len(D["reference"])} reference, '
      f'{len(D["earlier"])} earlier, of which {len(OLDER)} are older copies a newer generation replaces); '
      f'{len(D["slots"])} current slots; {len(cards)} pack cards; controls C1-C10 0 errors.')
