"""Shared composite-hub sections and controls (ORDER HUB-1, 2026-09-20).

A subject writer (build_humanities_shelf.py today; build_science_shelf.py once its
week bindings are restored) hands this module the SAME inputs and gets the SAME page
structure back:

  S1  "Start here" strip: one card per pathway + "Packs & downloads", first in <main>.
  S2  CURRENT LESSONS: Pathway -> Strand -> Term -> Week, ONE current card per week,
      titled "W<n> · <deck h1>"; an alternative sits in the same row as a badge-level
      card; a slot with no shelf card but a pack lesson is filled by that pack lesson.
  S3  PACKS & DOWNLOADS: one card per pack, links read from the pack's own manifest;
      printable packs, schemes of work and folder start pages under "Reference".
  S4  EARLIER VERSIONS: one collapsed section at the end, Pathway -> Term (the shelf
      record's own term; VB-RUN13 R0 forbids deriving a week from a path, and
      lesson-order.json records a week for 1 of the 52 earlier cards), every card
      labelled with its route family and keeping its own title. Nothing is
      deleted: card count in == out.
  S5  Terms come from the subject's own term bases (the strand record carries them).
  S6  The filter toolbar keeps working; without JavaScript everything is listed,
      current first, earlier last.

Controls (C1-C4) are pure functions over the derivation so they can be red-proved by
--self-test and refused by the writer before any byte is written:

  C1  exactly one current card per (pathway, term, week, strand) slot that has a
      lesson anywhere in the served estate (shelf or pack tree); >1 -> red;
      an UNASSIGNED strand -> red. A slot the SoW plans but nothing serves is a GAP:
      counted in the "Not yet published" note, never red (ruling 2026-09-20).
  C2  no v3 / earlier / classic-alternative card outside its ruled place
      (earlier families only in S4; a Classic alternative only beside its week).
  C3  every pack card link (start page, lesson, download) resolves to a file.
  C4  every shelf row renders exactly one [data-lesson-path] card: in == out.
"""
from __future__ import annotations
import collections, html, re
from pathlib import Path

E = html.escape
PATHWAYS = ('BUILD', 'GROW', 'LAUNCH')
TERM_ORDER = ('Aut1', 'Aut2', 'Spr1', 'Spr2', 'Sum1', 'Sum2')
STRAND_ORDER = ('Humanities', 'RE', 'Science')
EARLIER_STYLES = ('earlier',)


def natural(value: str):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', value)]


# ---------------------------------------------------------------- derivation
def derive(shelf_rows: list[dict], lessons: list[dict], pack_lessons: list[dict],
           sow_slots: dict[str, set], families: dict[str, str], terms: dict[str, str]) -> dict:
    """Build the S2/S3/S4 populations from the records. Pure; no filesystem.

    shelf_rows    the subject's shelf record rows (path, title, style, term, pathway ...)
    lessons       the strand record rows: path, pathway, term, week, strand, h1, alternative
    pack_lessons  rows from the pack tree: path, pathway, term, week, strand, h1, pack
    sow_slots     strand -> {(pathway, term, week)} the SoW plans
    families      shelf path -> family key: 'current' | 'reference' | earlier family label
    terms         term key -> label
    """
    by_path = {r['path']: r for r in shelf_rows}
    lesson_paths = {L['path'] for L in lessons}
    unassigned = [L['path'] for L in lessons if L['strand'] not in STRAND_ORDER]
    slots: dict[tuple, dict] = {}
    for L in lessons:
        key = (L['pathway'], L['term'], L['week'], L['strand'])
        slot = slots.setdefault(key, {'current': [], 'alternatives': [], 'pack': []})
        (slot['alternatives'] if L.get('alternative') else slot['current']).append(L)
    for P in pack_lessons:
        key = (P['pathway'], P['term'], P['week'], P['strand'])
        slots.setdefault(key, {'current': [], 'alternatives': [], 'pack': []})['pack'].append(P)
    def _double(cur):
        parts = [L.get('part') for L in cur]
        return len(cur) > 1 and (any(p is None for p in parts) or len(set(parts)) != len(parts))
    def _slot_key(k):
        """Order slot keys when a record binds no week. A week-unbound row carries week=None,
        which cannot be compared with an int, so sort those first and keep every bound week in
        its own numeric order. Ordering only, never membership."""
        pathway, term, week, strand = k
        return (pathway, term, 0 if week is None else 1, week if week is not None else 0, strand)
    double = sorted((k for k, s in slots.items() if _double(s['current'])), key=_slot_key)
    filled_by_pack = sorted((k for k, s in slots.items() if not s['current'] and s['pack']), key=_slot_key)
    gaps = collections.Counter()
    for strand, planned in sow_slots.items():
        for (pathway, term, week) in planned:
            s = slots.get((pathway, term, week, strand))
            if not s or (not s['current'] and not s['pack']):
                gaps[(pathway, strand, term)] += 1
    current_cards = {L['path'] for k, s in slots.items() for L in s['current']}
    alternative_cards = {L['path'] for k, s in slots.items() for L in s['alternatives']}
    earlier = [r for r in shelf_rows if families.get(r['path']) not in ('current', 'reference')]
    reference = [r for r in shelf_rows if families.get(r['path']) == 'reference']
    misplaced = [r['path'] for r in shelf_rows
                 if families.get(r['path']) == 'current' and r['path'] not in lesson_paths]
    return {'slots': slots, 'double': double, 'unassigned': unassigned, 'gaps': gaps,
            'filled_by_pack': filled_by_pack, 'current': current_cards,
            'alternatives': alternative_cards, 'earlier': earlier, 'reference': reference,
            'misplaced': misplaced, 'by_path': by_path, 'terms': terms}


# ------------------------------------------------------------------ controls
def c1_errors(d: dict) -> list[str]:
    errs = [f'C1 double-current slot {k}: ' + ', '.join(L['path'] for L in d['slots'][k]['current'])
            for k in d['double']]
    errs += [f'C1 UNASSIGNED strand: {p}' for p in d['unassigned']]
    return errs


def c2_errors(d: dict, families: dict[str, str]) -> list[str]:
    """An earlier-family card may only render in S4; a current-family card that is
    not in the strand record (and not reference) has no ruled place."""
    errs = [f'C2 current-family card with no strand row, no ruled place: {p}' for p in d['misplaced']]
    for r in d['earlier']:
        if r['path'] in d['current'] or r['path'] in d['alternatives']:
            errs.append(f'C2 earlier-family card rendered as current: {r["path"]}')
    return errs


def c3_errors(root: Path, pack_cards: list[dict]) -> list[str]:
    errs = []
    for card in pack_cards:
        for label, rel in card['links']:
            if not (root / rel).is_file():
                errs.append(f'C3 pack link does not resolve: {card["id"]} {label} -> {rel}')
    return errs


def c4_errors(rendered_paths: list[str], shelf_rows: list[dict]) -> list[str]:
    want = collections.Counter(r['path'] for r in shelf_rows)
    got = collections.Counter(rendered_paths)
    errs = [f'C4 shelf row not rendered: {p}' for p in want if p not in got]
    errs += [f'C4 card rendered {n} times: {p}' for p, n in got.items() if n != 1]
    errs += [f'C4 card with no shelf row: {p}' for p in got if p not in want]
    if sum(want.values()) != len(rendered_paths):
        errs.append(f'C4 card count in {sum(want.values())} != out {len(rendered_paths)}')
    return errs


# ----------------------------------------------------------------- rendering
# A subject whose shelf script filters by the week its own bindings RECORD (science-shelf.js:
# data-week may hold several week values; the card names them in <p class="science-week">)
# installs a hook: row -> (week attribute, week label) or None. Unset, cards are unchanged.
CARD_WEEK_HOOK = None


def _card(row: dict, href: str, title: str, kind: str, week: int | None, strand: str | None,
          extra: str = '', cls: str = '') -> str:
    week_attr = str(week) if week is not None else 'unspecified'
    hooked = CARD_WEEK_HOOK(row) if CARD_WEEK_HOOK else None
    if hooked:
        week_attr = hooked[0]
        extra = f'<p class="science-week">{E(hooked[1])}</p>' + extra
    data = (f' data-term="{E(row["term"], quote=True)}" data-style="{E(row["style"], quote=True)}"'
            f' data-pathway="{E(row["pathway"], quote=True)}"'
            f' data-week="{E(week_attr)}"')
    if strand:
        data += f' data-strand="{E(strand)}"'
    return (f'<article class="card t-{E(row["pathway"])}{(" " + cls) if cls else ""}" '
            f'data-lesson-path="{E(row["path"], quote=True)}"{data}>'
            f'<p class="kind">{E(kind)}</p><h4><a href="{E(href, quote=True)}">{E(title)}</a></h4>'
            f'{extra}<a class="go" href="{E(href, quote=True)}">Open lesson <span aria-hidden="true">→</span></a></article>')


def render_start_strip(subject: str, pathway_blurbs: dict[str, str], pathway_hrefs: dict[str, str] | None = None) -> str:
    """S1. A pathway card links its in-page section unless the subject hands it the
    pathway's own START_HERE page (PASS F: three pathway START_HERE + Packs)."""
    hrefs = pathway_hrefs or {}
    cards = ''.join(
        f'<a class="start-card p-{p}" href="{E(hrefs.get(p, "#lessons-" + p.lower()), quote=True)}"><strong>{E(p)}</strong>'
        f'<span>{E(pathway_blurbs.get(p, "Current lessons by term and week"))}</span></a>' for p in PATHWAYS)
    cards += ('<a class="start-card p-PACKS" href="#packs"><strong>Packs &amp; downloads</strong>'
              '<span>Editable Word, PowerPoint and PDF packs, one card per pack</span></a>')
    return (f'<nav class="start-here" id="start" aria-label="Start here"><h2>Start here</h2>'
            f'<div class="start-grid">{cards}</div></nav>')


def render_current(d: dict, subject: str, href_of, pack_href_of, strand_labels: dict[str, str], style_labels: dict[str, str] | None = None) -> tuple[str, list[str]]:
    """S2. Returns (html, rendered shelf paths)."""
    rendered: list[str] = []
    style_labels = style_labels or {}
    out = ['<section class="hub-block" id="lessons" aria-labelledby="lessons-h"><h2 id="lessons-h">Current lessons</h2>'
           '<p class="hub-note">One lesson per week. Pathway, then strand, then term. Alternatives sit beside their week.</p>']
    for pathway in PATHWAYS:
        keys = [k for k in d['slots'] if k[0] == pathway]
        strands = [s for s in STRAND_ORDER if any(k[3] == s for k in keys)]
        n = sum(len(d['slots'][k]['current']) or (1 if d['slots'][k]['pack'] else 0) for k in keys)
        out.append(f'<details class="science-pathway l-{pathway}" id="lessons-{pathway.lower()}" data-pathway="{pathway}" open>'
                   f'<summary><h2>{pathway}</h2><span data-pathway-count>{n} weeks</span><span class="chev" aria-hidden="true">▾</span></summary>')
        for strand in strands:
            out.append(f'<section class="hub-strand" data-strand="{E(strand)}"><h3 class="strand-h">{E(strand_labels.get(strand, strand))}</h3>')
            # the six terms first, then any extra term key the subject's own record carries
            # (a route bound to no timetabled week sits under 'unspecified', never dropped)
            for term in list(TERM_ORDER) + [t for t in d['terms'] if t not in TERM_ORDER]:
                tkeys = sorted((k for k in keys if k[3] == strand and k[1] == term), key=lambda k: (k[2] is None, k[2] or 0))
                if not tkeys:
                    continue
                out.append(f'<section class="catalogue-term" data-term="{term}"><h3>{E(d["terms"][term])} <span data-term-count>· {len(tkeys)} weeks</span></h3><div class="grid week-grid">')
                for k in tkeys:
                    s = d['slots'][k]
                    week = k[2]
                    out.append(f'<div class="week-row" data-week="{week}">')
                    if s['current']:
                        wk = f'W{week}' if week is not None else 'Week not bound'
                        for L in sorted(s['current'], key=lambda L: L.get('part') or ''):
                            row = d['by_path'][L['path']]
                            rendered.append(L['path'])
                            extra = ''
                            if s['pack'] and L is s['current'][0]:
                                P = s['pack'][0]
                                extra += f'<p class="pack-link"><a href="{E(pack_href_of(P["path"]), quote=True)}">Pack lesson: {E(P["h1"])} →</a></p>'
                            badges = f'<p class="badges"><span class="pill">{E(strand)}</span><span class="pill">{E(style_labels.get(row["style"], row["style"]))}</span>' + L.get('badges', '') + '</p>'
                            part = f' · {L["part"]}' if L.get('part') else ''
                            out.append(_card(row, href_of(row['path']), f'{wk}{part} · {L["h1"]}', f'{pathway} · {strand}', week, strand, badges + extra))
                    else:
                        P = s['pack'][0]
                        out.append(f'<article class="card t-{pathway} pack-lesson" data-pack-lesson="{E(P["path"], quote=True)}" data-term="{term}" data-style="pack" data-pathway="{pathway}" data-week="{week}" data-strand="{E(strand)}">'
                                   f'<p class="kind">{pathway} · {E(strand)} · pack lesson</p><h4><a href="{E(pack_href_of(P["path"]), quote=True)}">W{week} · {E(P["h1"])}</a></h4>'
                                   f'<p class="badges"><span class="pill">{E(strand)}</span><span class="pill">{E(P["pack"])}</span></p>'
                                   f'<a class="go" href="{E(pack_href_of(P["path"]), quote=True)}">Open lesson <span aria-hidden="true">→</span></a></article>')
                    for A in s['alternatives']:
                        row = d['by_path'][A['path']]
                        rendered.append(A['path'])
                        out.append(_card(row, href_of(row['path']), f'W{week} · {A["h1"]}', 'Alternative · same week', week, strand,
                                         f'<p class="badges"><span class="pill alt">Alternative</span><span class="pill">{E(strand)}</span></p>', 'alt'))
                    out.append('</div>')
                out.append('</div></section>')
            out.append('</section>')
        out.append('</details>')
    out.append('</section>')
    return ''.join(out), rendered


def render_gaps(gaps: collections.Counter, terms: dict[str, str]) -> str:
    if not gaps:
        return ''
    items = ''.join(f'<li>{E(p)} · {E(s)} · {E(terms[t])}: {n} week{"s" if n != 1 else ""}</li>'
                    for (p, s, t), n in sorted(gaps.items(), key=lambda kv: (PATHWAYS.index(kv[0][0]), kv[0][1], TERM_ORDER.index(kv[0][2]))))
    total = sum(gaps.values())
    return (f'<details class="hub-gaps" id="not-yet-published"><summary>Not yet published · {total} planned weeks without a lesson yet</summary>'
            f'<ul>{items}</ul></details>')


def render_packs(pack_cards: list[dict], reference_rows: list[dict], href_of, subject: str) -> tuple[str, list[str]]:
    rendered: list[str] = []
    out = ['<section class="hub-block" id="packs" aria-labelledby="packs-h"><h2 id="packs-h">Packs &amp; downloads</h2>'
           '<p class="hub-note">One card per pack. Every link below is read from the pack\'s own manifest.</p><div class="grid pack-grid">']
    for c in pack_cards:
        links = ''.join(f'<li><a href="{E(rel, quote=True)}" download>{E(label)}</a></li>' for label, rel in c['links'] if label.startswith('ZIP'))
        weeks = ''
        for wk, files in c['weeks']:
            weeks += f'<li><span class="wk">{E(wk)}</span> ' + ' · '.join(f'<a href="{E(rel, quote=True)}" download>{E(label)}</a>' for label, rel in files) + '</li>'
        docs = ' · '.join(f'<a href="{E(rel, quote=True)}">{E(label)}</a>' for label, rel in c['documents'])
        badge = '<span class="pill ok">proofread 2026-09-19</span>' if c['proofread'] else ''
        out.append(f'<article class="card pack t-{E(c["pathway"])}" data-pack="{E(c["id"], quote=True)}" data-pathway="{E(c["pathway"])}" data-term="{E(c["term"])}" data-strand="{E(c["strand"])}">'
                   f'<p class="kind">{E(c["pathway_label"])} · {E(c["term_label"])} · {E(c["strand"])}</p>'
                   f'<h4><a href="{E(c["start_here"], quote=True)}">{E(c["title"])}</a></h4>'
                   f'<p class="badges"><span class="pill">{E(c["strand"])}</span>{badge}<span class="pill">{c["lesson_count"]} lessons</span></p>'
                   + (f'<ul class="dl zips">{links}</ul>' if links else '')
                   + (f'<ul class="dl weeks">{weeks}</ul>' if weeks else '')
                   + (f'<p class="pack-docs">{docs}</p>' if docs else '')
                   + f'<a class="go" href="{E(c["start_here"], quote=True)}">Start here <span aria-hidden="true">→</span></a></article>')
    out.append('</div><h3 class="ref-h" id="reference">Reference · printable packs, schemes of work and folder start pages</h3><div class="grid ref-grid">')
    for r in sorted(reference_rows, key=lambda r: (r['pathway'], natural(r['path']))):
        rendered.append(r['path'])
        title = re.sub(r'\s*[·—]\s*40 minutes\s*$', '', r['title'])
        out.append(_card(r, href_of(r['path']), title, ('Shared' if r['pathway'] == 'OTHER' else r['pathway']) + ' · reference', None, None, '', 'ref')
                   .replace('Open lesson', 'Open resource'))
    out.append('</div></section>')
    return ''.join(out), rendered


def render_earlier(earlier_rows: list[dict], families: dict[str, str], href_of, terms: dict[str, str],
                   week_of=None) -> tuple[str, list[str]]:
    """S4. Grouped Pathway -> recorded term. No week is derived from any path; a subject
    whose own bindings RECORD a week for an earlier route may hand it in through week_of
    (path -> week or None), and the card then carries it."""
    rendered: list[str] = []
    n = len(earlier_rows)
    out = [f'<details class="science-pathway earlier" id="earlier" data-pathway="EARLIER"><summary><h2>Earlier versions</h2>'
           f'<span data-pathway-count>{n} resources</span><span class="chev" aria-hidden="true">▾</span></summary>'
           '<p class="hub-note">Retained teaching versions, grouped by pathway and recorded term. Each card names its family and keeps its own title.</p>']
    for pathway in PATHWAYS + ('OTHER',):
        rows = [r for r in earlier_rows if r['pathway'] == pathway]
        if not rows:
            continue
        out.append(f'<section class="catalogue-term earlier-pathway" data-term="earlier"><h3>{E("Shared" if pathway == "OTHER" else pathway)} <span data-term-count>· {len(rows)} resources</span></h3>')
        groups = collections.defaultdict(list)
        for r in rows:
            groups[r['term']].append(r)
        order = {t: i for i, t in enumerate(terms)}
        for term in sorted(groups, key=lambda t: order.get(t, len(order))):
            out.append(f'<section class="catalogue-batch" data-style="earlier"><h4>{E(terms.get(term, term))} <span data-batch-count>· {len(groups[term])} resources</span></h4><div class="grid">')
            wk = (lambda r: week_of(r['path']) if week_of else None)
            for r in sorted(groups[term], key=lambda r: ((wk(r) is None), wk(r) or 0, natural(r['title']))):
                rendered.append(r['path'])
                title = re.sub(r'\s*[·—]\s*40 minutes\s*$', '', r['title'])
                fam = families.get(r['path'], 'earlier')
                w = wk(r)
                out.append(_card(r, href_of(r['path']), (f'W{w} · ' if w is not None else '') + title,
                                 f'{pathway if pathway != "OTHER" else "Shared"} · {fam}', w, None,
                                 f'<p class="badges"><span class="pill">{E(fam)}</span></p>', 'earlier'))
            out.append('</div></section>')
        out.append('</section>')
    out.append('</details>')
    return ''.join(out), rendered


# ---------------------------------------------------------------- self-test
def self_test() -> int:
    """Red proofs for C1-C4. A control that cannot fail is not a control."""
    ok = 0
    def check(name, cond):
        nonlocal ok
        print(f'  [{"ok" if cond else "FAIL"}] {name}')
        ok += 0 if cond else 1
    terms = {'Aut1': 'Autumn 1', 'Aut2': 'Autumn 2'}
    shelf = [{'path': 'a.html', 'title': 'A', 'style': 'full-lundy', 'term': 'Aut1', 'pathway': 'BUILD'},
             {'path': 'b.html', 'title': 'B', 'style': 'earlier', 'term': 'Aut1', 'pathway': 'BUILD'},
             {'path': 'c.html', 'title': 'C', 'style': 'alternative', 'term': 'Aut1', 'pathway': 'BUILD'}]
    fam = {'a.html': 'current', 'b.html': 'Estate v3', 'c.html': 'current'}
    L = [{'path': 'a.html', 'pathway': 'BUILD', 'term': 'Aut1', 'week': 1, 'strand': 'RE', 'h1': 'A', 'alternative': False},
         {'path': 'c.html', 'pathway': 'BUILD', 'term': 'Aut1', 'week': 1, 'strand': 'RE', 'h1': 'C', 'alternative': True}]
    sow = {'RE': {('BUILD', 'Aut1', 1), ('BUILD', 'Aut1', 2)}}
    d = derive(shelf, L, [], sow, fam, terms)
    check('green: one current per slot, alternative beside it', not c1_errors(d) and d['alternatives'] == {'c.html'})
    check('gap counted, not red', d['gaps'][('BUILD', 'RE', 'Aut1')] == 1 and not c1_errors(d))
    pack = [{'path': 'p.html', 'pathway': 'BUILD', 'term': 'Aut1', 'week': 2, 'strand': 'RE', 'h1': 'P', 'pack': 'RE pack'}]
    d2 = derive(shelf, L, pack, sow, fam, terms)
    check('a pack lesson fills the empty slot; gap 0', not d2['gaps'] and d2['filled_by_pack'] == [('BUILD', 'Aut1', 2, 'RE')])
    L2 = L + [{'path': 'b.html', 'pathway': 'BUILD', 'term': 'Aut1', 'week': 1, 'strand': 'RE', 'h1': 'B', 'alternative': False}]
    d3 = derive(shelf, L2, [], sow, fam, terms)
    check('C1 red: two current cards in one slot', any(e.startswith('C1 double-current') for e in c1_errors(d3)))
    Lp = [dict(L[0], part='A'), dict(L[0], path='b.html', h1='B', part='B')]
    check('C1 green: parts A and B of one week share the slot', not c1_errors(derive(shelf, Lp, [], sow, fam, terms)))
    Lq = [dict(L[0], part='A'), dict(L[0], path='b.html', h1='B', part='A')]
    check('C1 red: two rows with the same part', any(e.startswith('C1 double-current') for e in c1_errors(derive(shelf, Lq, [], sow, fam, terms))))
    Lr = [dict(L[0], part='A'), dict(L[0], path='b.html', h1='B')]
    check('C1 red: a part beside a row with no part', any(e.startswith('C1 double-current') for e in c1_errors(derive(shelf, Lr, [], sow, fam, terms))))
    dn = derive(shelf, [dict(L[0], week=None)], [], {}, fam, terms)
    hn, gn = render_current(dn, 'S', lambda p: p, lambda p: p, {'RE': 'RE'})
    check('a week-unbound current row renders last, labelled, and is counted', gn == ['a.html'] and 'Week not bound' in hn)
    check('C2 red: an earlier-family card rendered as current', any('earlier-family' in e for e in c2_errors(d3, fam)))
    L3 = [dict(L[0], strand='UNASSIGNED')] + [L[1]]
    check('C1 red: UNASSIGNED strand', any('UNASSIGNED' in e for e in c1_errors(derive(shelf, L3, [], sow, fam, terms))))
    fam2 = dict(fam, **{'b.html': 'current'})
    check('C2 red: a current-family card with no strand row', any('no ruled place' in e for e in c2_errors(derive(shelf, L, [], sow, fam2, terms), fam2)))
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        root = Path(t); (root / 'x.pdf').write_bytes(b'x')
        cards = [{'id': 'p', 'links': [('PDF', 'x.pdf')]}, {'id': 'q', 'links': [('PDF', 'missing.pdf')]}]
        errs = c3_errors(root, cards)
        check('C3: a resolving link passes, a missing one reds', len(errs) == 1 and 'missing.pdf' in errs[0])
    check('C4 green: every row exactly once', not c4_errors(['a.html', 'b.html', 'c.html'], shelf))
    check('C4 red: a card dropped', any('not rendered' in e for e in c4_errors(['a.html', 'b.html'], shelf)))
    check('C4 red: a card duplicated', any('2 times' in e for e in c4_errors(['a.html', 'a.html', 'b.html', 'c.html'], shelf)))
    check('C4 red: a card invented', any('no shelf row' in e for e in c4_errors(['a.html', 'b.html', 'c.html', 'z.html'], shelf)))
    html_out, got = render_earlier([shelf[1]], fam, lambda p: p, terms)
    check('S4 groups earlier cards by the RECORDED term and derives no week from a path', got == ['b.html'] and 'Autumn 1' in html_out and 'data-week="unspecified"' in html_out)
    html_w, got_w = render_earlier([shelf[1]], fam, lambda p: p, terms, week_of=lambda p: 3)
    check('S4 carries a RECORD-supplied week on an earlier card', got_w == ['b.html'] and 'data-week="3"' in html_w and '>W3 · B<' in html_w)
    print(f'hub_sections self-test: {18 - ok} of 18 controls ok, {ok} FAIL')
    return 1 if ok else 0


if __name__ == '__main__':
    import sys
    sys.exit(self_test())
