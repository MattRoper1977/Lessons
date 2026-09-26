#!/usr/bin/env python3
"""The arrival line appears only in Week 1, on every served surface, and a surface's week is read from
what it says, never from where it sits (rulings LAND-A2 R5 §1 and R8 §3; ORDER VB-RUN13 R0).

v9 printed "You can begin without previous learning. Word help — X: …" at the start of every lesson,
and from Week 2 on that word help stated the answer to arrival question 2 (R3). v10 keeps the line in
Week 1 only, where HUM-D5 holds it by design. This check holds every later week to that on every served
surface a pupil or TA can see under Humanities_Teesside: the lesson and pupil pages (HTML), their PDFs,
and the editable Word and PowerPoint files. Served = git ls-files, dropping any path with a part that
starts with '_' or '.', which the publisher does not copy. Text is extracted from the file's own bytes
(HTML without tags, scripts or styles; PDF by pypdf; DOCX/PPTX from their XML parts) and whitespace is
folded, so a line broken across PDF lines still matches "without previous learning".

WHERE A WEEK COMES FROM. VB-RUN13 R0 forbids deriving a week from a filename or a folder name, and g27
enforces it. Nothing here reads a week out of a path. A file's week is read from its words:

  own text   the term-week label the file prints: a term, its half (1 or 2), then the week. The forms
             in the estate today are
               "Autumn 2 · Week 1"   lesson page brandline
               "Autumn 1 / Week 1"   PPTX title slide
               "Autumn 2  W1"        DOCX page header, PPTX slide footer
               "Summer 1 Week 2"     pupil sheet header
             Between the half and the week: nothing, or one of  · / | , : - – —  (case is ignored).
             Where a file has a header of its own, ONLY the header is read: the HTML elements of class
             "brandline", and the DOCX header and footer parts. So a lesson page that links "Next:
             Autumn 2 · Week 2" in its body is still the week its header prints. A file without such a
             header is read whole.
             The file must state exactly ONE distinct week. Two or more is a failure, never a guess.
  inherited  a file that states no week at all (a pupil-sheet PDF) takes the week of the served HTML
             pages in the tree that link it (href/src/object data, resolved relative to the linking
             page), counting only pages that state exactly one week of their own. Those pages must agree
             on one week; if they do not, that is a failure too.

A path printed as text ("BUILD_A2_W01", "Autumn_2/W01") is never read as a week: every label form needs
whitespace between the term and its half, which no path in the estate carries.

THE RULE. Every served file carrying the line must have a readable week, and that week must be 1. A file
whose week cannot be read (it states none and no week-stating page links it) FAILS unless it is on the
exception list.

THE EXCEPTION LIST (arrival_week_exceptions.json next to this file; LAND-A2 R8 §3). The pupil-sheet pages
(*_Pupil_Resources.html) that carry the line state no week and are linked by no page, so their week
cannot be read until they print it ("Autumn N · Week N", GPT B9 then POLISH-A2). Each is named with the
reason, the ruling, the date it was added and when it leaves. The list only shrinks:
  - an entry for a file that is not served, no longer carries the line, now has a readable week, or now
    states conflicting weeks FAILS: remove it from the exception list;
  - an entry for a file outside the set R8 §3 ruled (RULED_R8_S3 below) FAILS: the list may not grow;
  - a malformed list FAILS, and then no entry is honoured.
A missing list file means no exceptions.

  check_arrival_surfaces.py [--root DIR] [--tree Humanities_Teesside] [--exceptions FILE] [--verbose]
  check_arrival_surfaces.py --self-test      fixtures in a temporary directory; no repository needed
Exit 1 on any failure. Needs pypdf.
"""
import argparse, html, json, posixpath, re, shutil, subprocess, sys, tempfile, zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINE = re.compile(r'without\s+previous\s+learning', re.I)
# a term, its half, an optional separator, then the week. Applied to text read from a file's bytes only.
LABEL = re.compile(r'\b(?:Autumn|Spring|Summer)\s+[12]\s*(?:[·/|,:\-–—]\s*)?(?:Week\s*(\d{1,2})|W(\d{1,2}))\b', re.I)
KINDS = ('.html', '.htm', '.pdf', '.docx', '.pptx')
EXCEPTIONS = Path(__file__).resolve().with_name('arrival_week_exceptions.json')

RULING = 'LAND-A2 R8 §3'
ADDED = '2026-09-26'
REASON = 'states no week; not linked by a week-stating page'
ENTRY_KEYS = {'path', 'reason', 'ruling', 'added', 'leaves_when'}
TOP_KEYS = {'about', 'exceptions'}
# The files R8 §3 ruled onto the list. The list may be any subset of these and nothing else: an entry
# leaves when its sheet prints its week, and no entry is added without a new ruling (and a change here).
_T = 'Humanities_Teesside/Teaching_Packs/'
RULED_R8_S3 = frozenset(_T + s for s in (
    'HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W01/LAUNCH_A1_W01_Pupil_Resources.html',
    'HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_A2_W01_Pupil_Resources.html',
    'HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W01/GROW_A2_W01_Pupil_Resources.html',
    'HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_A2_W01_Pupil_Resources.html',
    'HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W01/BUILD_S1_W01_Pupil_Resources.html',
    'HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W01/GROW_S1_W01_Pupil_Resources.html',
    'HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W01/LAUNCH_S1_W01_Pupil_Resources.html',
    'HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W01/BUILD_S2_W01_Pupil_Resources.html',
    'HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W01/GROW_S2_W01_Pupil_Resources.html',
    'HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W01/LAUNCH_S2_W01_Pupil_Resources.html',
    'RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W01/BUILD_RE_A1_W01_Pupil_Resources.html',
    'RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_RE_A2_W01_Pupil_Resources.html',
    'RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W01/GROW_RE_A1_W01_Pupil_Resources.html',
    'RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Pupil_Resources.html',
    'RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W01/LAUNCH_RE_A1_W01_Pupil_Resources.html',
    'RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_RE_A2_W01_Pupil_Resources.html',
))


def served(root, tree, use_git=True):
    listed = []
    if use_git:
        try:
            listed = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--', tree],
                                    capture_output=True, check=True).stdout.decode().split('\0')
        except Exception:
            listed = []
    if not any(listed):
        listed = [q.relative_to(root).as_posix() for q in (root / tree).rglob('*') if q.is_file()]
    return sorted(x for x in listed if x and x.lower().endswith(KINDS)
                  and not any(seg.startswith(('_', '.')) for seg in x.split('/')))


class _Page(HTMLParser):
    """One pass over a page: its words (no scripts or styles), its brandline header, and its links."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.words, self.header, self.links = [], [], []
        self._skip = None      # inside <script> or <style>
        self._head = None      # [tag, depth] while inside a brandline element

    def handle_starttag(self, tag, attrs):
        if self._skip:
            return
        if tag in ('script', 'style'):
            self._skip = tag
            return
        a = {k: v for k, v in attrs if v}
        for k in ('href', 'src'):
            if k in a:
                self.links.append(a[k])
        if tag == 'object' and 'data' in a:
            self.links.append(a['data'])
        if self._head:
            if tag == self._head[0]:
                self._head[1] += 1
        elif 'brandline' in a.get('class', '').split():
            self._head = [tag, 1]

    def handle_endtag(self, tag):
        if self._skip:
            if tag == self._skip:
                self._skip = None
            return
        if self._head and tag == self._head[0]:
            self._head[1] -= 1
            if not self._head[1]:
                self._head = None
                self.header.append(' ')

    def handle_data(self, data):
        if self._skip:
            return
        self.words.append(data)
        if self._head:
            self.header.append(data)


def _xml_words(xml):
    return html.unescape(re.sub(r'<[^>]+>', ' ', xml))


def read_doc(file):
    """{'words': whole text, 'header': the file's own header text or '', 'links': [...] (HTML only)}"""
    kind = file.suffix.lower()
    if kind in ('.html', '.htm'):
        pg = _Page()
        pg.feed(file.read_bytes().decode('utf-8', 'replace'))
        pg.close()
        return {'words': ' '.join(pg.words), 'header': ' '.join(pg.header), 'links': pg.links}
    if kind in ('.docx', '.pptx'):
        with zipfile.ZipFile(file) as z:
            parts = [n for n in z.namelist() if n.endswith('.xml') and n.startswith(('word/', 'ppt/slides/', 'ppt/notesSlides/'))]
            heads = [n for n in parts if n.startswith(('word/header', 'word/footer'))]
            body = ' '.join(_xml_words(z.read(n).decode('utf-8', 'replace')) for n in parts)
            head = ' '.join(_xml_words(z.read(n).decode('utf-8', 'replace')) for n in heads)
        return {'words': body, 'header': head, 'links': []}
    if kind == '.pdf':
        from pypdf import PdfReader
        return {'words': ' '.join(pg.extract_text() or '' for pg in PdfReader(str(file)).pages), 'header': '', 'links': []}
    return {'words': '', 'header': '', 'links': []}


def weeks_in(text):
    return sorted({int(m.group(1) or m.group(2)) for m in LABEL.finditer(' '.join(text.split()))})


def own_weeks(doc):
    """(weeks, where): the header when the file has one that prints a label, otherwise the whole text."""
    heard = weeks_in(doc['header'])
    if heard:
        return heard, 'header'
    return weeks_in(doc['words']), 'text'


def link_target(page, ref):
    """The served path a link on `page` points at, or None (external, site-absolute, outside the tree)."""
    u = urlsplit(ref.strip())
    if u.scheme or u.netloc or not u.path or u.path.startswith('/'):
        return None
    hop = posixpath.normpath(posixpath.join(posixpath.dirname(page), unquote(u.path)))
    return None if hop == '..' or hop.startswith('../') else hop


def week_of(rel, docs, linkers):
    """-> (status, week, detail); status is 'own', 'inherited', 'none' or 'conflict'."""
    weeks, where = own_weeks(docs[rel])
    if len(weeks) == 1:
        return 'own', weeks[0], f'its {where} prints Week {weeks[0]}'
    if weeks:
        return 'conflict', None, f'its {where} prints more than one week ({", ".join(map(str, weeks))})'
    stating = {}
    for page in sorted(linkers.get(rel, ())):
        w, _ = own_weeks(docs[page])
        if len(w) == 1:
            stating[page] = w[0]
    distinct = sorted(set(stating.values()))
    if len(distinct) == 1:
        return 'inherited', distinct[0], 'inherited from ' + ', '.join(sorted(stating))
    if distinct:
        return 'conflict', None, 'the pages linking it print different weeks: ' + '; '.join(
            f'{pg} (Week {w})' for pg, w in sorted(stating.items()))
    return 'none', None, REASON


def load_exceptions(listfile, ruled):
    """-> (honoured {path: entry}, problems [str]). A malformed list honours nothing."""
    if not listfile.exists():
        return {}, []
    try:
        doc = json.loads(listfile.read_text(encoding='utf-8'))
    except Exception as e:
        return {}, [f'malformed exception list {listfile.name}: not JSON ({e})']
    bad = []
    if not isinstance(doc, dict) or not isinstance(doc.get('exceptions'), list) or set(doc) - TOP_KEYS:
        return {}, [f'malformed exception list {listfile.name}: want an object with "exceptions": [...] '
                    f'and no keys beyond {sorted(TOP_KEYS)}']
    honoured = {}
    for i, e in enumerate(doc['exceptions']):
        where = f'entry {i}'
        if not isinstance(e, dict) or set(e) != ENTRY_KEYS or not all(isinstance(v, str) and v.strip() for v in e.values()):
            bad.append(f'malformed exception list {listfile.name}: {where} must have exactly the non-empty string fields {sorted(ENTRY_KEYS)}')
            continue
        where = e['path']
        if e['ruling'] != RULING or e['reason'] != REASON or e['added'] != ADDED:
            bad.append(f'malformed exception list {listfile.name}: {where}: ruling, reason and added must be '
                       f'"{RULING}", "{REASON}", "{ADDED}"')
        elif where in honoured:
            bad.append(f'malformed exception list {listfile.name}: {where} is listed twice')
        elif where not in ruled:
            bad.append(f'exception list grows: {where} is not one of the files {RULING} ruled; '
                       f'the list may only shrink')
        else:
            honoured[where] = e
    return ({} if bad else honoured), bad


def evaluate(root, tree, listfile, ruled, use_git=True, verbose=False):
    """-> (fail lines, counts, rows)."""
    fails = []
    honoured, problems = load_exceptions(listfile, ruled)
    fails += problems
    files = served(root, tree, use_git)
    docs = {}
    for rel in files:
        try:
            docs[rel] = read_doc(root / rel)
        except Exception as e:  # a surface nobody can read is a failure to look at, never a silent pass
            fails.append(f'unreadable surface: {rel} ({type(e).__name__}: {e})')
            docs[rel] = {'words': '', 'header': '', 'links': []}
    linkers = {}
    for rel, doc in docs.items():
        for ref in doc['links']:
            hop = link_target(rel, ref)
            if hop and hop != rel:
                linkers.setdefault(hop, set()).add(rel)
    carrying = [rel for rel in files if LINE.search(' '.join(docs[rel]['words'].split()))]
    counts = {'served': len(files), 'carrying': len(carrying), 'own': 0, 'inherited': 0, 'excepted': 0,
              'week1': 0, 'listed': len(honoured)}
    rows = []
    for rel in carrying:
        status, week, detail = week_of(rel, docs, linkers)
        rows.append((status, week, rel, detail))
        if status in ('own', 'inherited'):
            counts[status] += 1
            counts['week1'] += week == 1
            if week != 1:
                fails.append(f'arrival line in Week {week}: {rel} ({detail})')
            if rel in honoured:
                fails.append(f'stale exception: {rel} now has a readable week (Week {week}: {detail}); '
                             f'remove it from the exception list')
        elif status == 'conflict':
            fails.append(f'week unreadable: {rel}: {detail}')
            if rel in honoured:
                fails.append(f'stale exception: {rel} no longer "{REASON}" ({detail}); remove it from the exception list')
        elif rel in honoured:
            counts['excepted'] += 1
        else:
            fails.append(f'week unreadable: {rel} {REASON}; a file carrying the arrival line must print its week '
                         f'(and it must be Week 1)')
    carried, served_set = set(carrying), set(files)
    for rel in sorted(honoured):
        if rel not in served_set:
            fails.append(f'stale exception: {rel} is not a served file; remove it from the exception list')
        elif rel not in carried:
            fails.append(f'stale exception: {rel} no longer carries the arrival line; remove it from the exception list')
    if verbose:
        for status, week, rel, detail in rows:
            tag = f'Week {week}' if week else ('excepted' if rel in honoured and status == 'none' else status)
            print(f'  {status:9s} {tag:9s} {rel}  [{detail}]')
    return fails, counts, rows


def report(fails, counts):
    for f in fails:
        print('FAIL ' + f)
    print(f"arrival surfaces: {counts['carrying']} served file(s) carry the arrival line: {counts['own']} print their "
          f"week, {counts['inherited']} inherit it from a linking page, {counts['excepted']} excepted "
          f"({RULING}; {counts['listed']} listed); {counts['week1']} read as Week 1; {len(fails)} failure(s)")
    print('PASS' if not fails else f'FAIL: {len(fails)} failure(s)')
    return 1 if fails else 0


# ---------------------------------------------------------------------------------------------- self-test

def _pdf(text):
    """A one-page PDF whose only text is `text`, in the standard Helvetica font."""
    esc = text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    stream = f'BT /F1 11 Tf 40 760 Td ({esc}) Tj ET'.encode('latin-1')
    objs = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
            b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
            b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
            b'<< /Length %d >>\nstream\n' % len(stream) + stream + b'\nendstream']
    out, offsets = bytearray(b'%PDF-1.4\n'), []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += b'%d 0 obj\n' % i + o + b'\nendobj\n'
    xref = len(out)
    out += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1) + b''.join(b'%010d 00000 n \n' % o for o in offsets)
    out += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, xref)
    return bytes(out)


def _docx(header, body):
    import io
    w = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr('word/document.xml', f'<w:document {w}><w:body><w:p><w:r><w:t>{body}</w:t></w:r></w:p></w:body></w:document>')
        z.writestr('word/header1.xml', f'<w:hdr {w}><w:p><w:r><w:t>{header}</w:t></w:r></w:p></w:hdr>')
    return buf.getvalue()


ARRIVE = '<p>You can begin without previous learning. Word help — source: where evidence comes from.</p>'
PDF_ARRIVE = 'Arrival task. You can begin without previous learning. Word help - source.'


def _lesson(label, body=ARRIVE, links=()):
    a = ''.join(f'<a href="{h}">download</a>' for h in links)
    return (f'<!doctype html><html><head><title>Lesson</title><script>var s = "Autumn 2 · Week 9";</script></head><body>'
            f'<section class="slide"><p class="brandline">{label}</p><h2>Arrival task</h2>{body}{a}</section></body></html>')


def _sheet(extra=ARRIVE):
    return f'<!doctype html><html><head><title>Pupil resources</title></head><body><h1>Pupil resources</h1>{extra}</body></html>'


def self_test():
    T = 'Humanities_Teesside'
    d1 = f'{T}/P/X/Autumn_2/W01'
    d2 = f'{T}/P/X/Autumn_2/W02'
    base = {
        # own week from the header, although the body links "Autumn 2 · Week 2" and a script says Week 9
        f'{d1}/X_A2_W01_Lesson.html': _lesson('X · Humanities · Autumn 2 · Week 1',
                                              ARRIVE + '<p><a href="../W02/X_A2_W02_Lesson.html">Next: Autumn 2 · Week 2</a></p>',
                                              ['X_A2_W01_Pupil_Resources.pdf']),
        f'{d1}/X_A2_W01_Pupil_Resources.pdf': _pdf(PDF_ARRIVE),                          # inherits Week 1
        f'{d1}/X_A2_W01_Editable_Pack.docx': _docx('Made by Matt  X  Humanities  Autumn 2  W1',
                                                   'Arrival: You can begin without previous learning.'),
        f'{d1}/X_A2_W01_Pupil_Resources.html': _sheet(),                                 # listed: states no week
        f'{d2}/X_A2_W02_Lesson.html': _lesson('X · Humanities · Autumn 2 · Week 2', '<p>Recall last week.</p>',
                                              ['X_A2_W02_Pupil_Resources.pdf']),
        f'{d2}/X_A2_W02_Pupil_Resources.pdf': _pdf('Recall task. Use last week.'),
        f'{T}/_drafts/X_A2_W02_Lesson.html': _lesson('X · Humanities · Autumn 2 · Week 2'),  # not served
    }
    listed = f'{d1}/X_A2_W01_Pupil_Resources.html'
    ruled = frozenset({listed, f'{d1}/Y_A2_W01_Pupil_Resources.html'})
    entry = {'path': listed, 'reason': REASON, 'ruling': RULING, 'added': ADDED,
             'leaves_when': 'the sheet prints Autumn N · Week N (GPT B9 / POLISH-A2)'}
    good_list = json.dumps({'about': 'fixture', 'exceptions': [entry]})

    cases = [
        # name, {path: bytes-or-str-or-None}, list text or None to keep, want_fail, substrings every failure set must contain
        ('Week 1 files pass: own header week, inherited PDF week, DOCX header week, one listed sheet',
         {}, None, False, []),
        ('the line planted in a Week 2 lesson page FAILS',
         {f'{d2}/X_A2_W02_Lesson.html': _lesson('X · Humanities · Autumn 2 · Week 2', ARRIVE, ['X_A2_W02_Pupil_Resources.pdf'])},
         None, True, ['arrival line in Week 2: ' + f'{d2}/X_A2_W02_Lesson.html']),
        ('the line planted in an unlisted week-less pupil sheet FAILS (its W01 folder and _W01_ name do not make it Week 1)',
         {f'{d1}/Y_A2_W01_Pupil_Resources.html': _sheet()}, None, True,
         ['week unreadable: ' + f'{d1}/Y_A2_W01_Pupil_Resources.html']),
        ('a listed sheet that gains "Autumn 2 · Week 1" FAILS as stale',
         {listed: _sheet('<p class="kicker">Pupil resources | X Humanities Autumn 2 · Week 1</p>' + ARRIVE)}, None, True,
         ['stale exception: ' + listed + ' now has a readable week (Week 1']),
        ('a listed path that no longer exists FAILS as stale',
         {listed: None}, None, True, ['stale exception: ' + listed + ' is not a served file']),
        ('a PDF inheriting Week 2 from its linking page FAILS',
         {f'{d2}/X_A2_W02_Pupil_Resources.pdf': _pdf(PDF_ARRIVE)}, None, True,
         ['arrival line in Week 2: ' + f'{d2}/X_A2_W02_Pupil_Resources.pdf (inherited from {d2}/X_A2_W02_Lesson.html)']),
        ('a listed sheet that no longer carries the line FAILS as stale',
         {listed: _sheet('<p>Match the words.</p>')}, None, True,
         ['stale exception: ' + listed + ' no longer carries the arrival line']),
        ('a DOCX whose header prints W2 and carries the line FAILS',
         {f'{d2}/X_A2_W02_Editable_Pack.docx': _docx('Made by Matt  X  Humanities  Autumn 2  W2', 'You can begin without previous learning.')},
         None, True, ['arrival line in Week 2: ' + f'{d2}/X_A2_W02_Editable_Pack.docx']),
        ('a page whose header prints two weeks FAILS, never guessed',
         {f'{d1}/X_A2_W01_Lesson.html': _lesson('X · Autumn 2 · Week 1</p><p class="brandline">X · Autumn 2 · Week 3',
                                                ARRIVE, ['X_A2_W01_Pupil_Resources.pdf'])},
         None, True, ['week unreadable: ' + f'{d1}/X_A2_W01_Lesson.html: its header prints more than one week (1, 3)']),
        ('a surface that cannot be read FAILS, never passes silently',
         {f'{d2}/X_A2_W02_Editable_Slides.pptx': b'not a zip archive'}, None, True,
         ['unreadable surface: ' + f'{d2}/X_A2_W02_Editable_Slides.pptx']),
        ('a malformed exception list FAILS',
         {}, '{"exceptions": [', True, ['malformed exception list']),
        ('an entry with a field missing FAILS as malformed',
         {}, json.dumps({'exceptions': [{k: v for k, v in entry.items() if k != 'leaves_when'}]}), True,
         ['malformed exception list']),
        ('an entry outside the ruled set FAILS: the list may not grow',
         {f'{d1}/Z_A2_W01_Pupil_Resources.html': _sheet()},
         json.dumps({'exceptions': [entry, dict(entry, path=f'{d1}/Z_A2_W01_Pupil_Resources.html')]}), True,
         ['exception list grows: ' + f'{d1}/Z_A2_W01_Pupil_Resources.html']),
    ]
    ok_all = True
    with tempfile.TemporaryDirectory() as tmp:
        for name, changes, list_text, want_fail, want in cases:
            root = Path(tmp) / 'case'
            if root.exists():
                shutil.rmtree(root)
            files = dict(base)
            files.update(changes)
            for rel, body in files.items():
                if body is None:
                    continue
                q = root / rel
                q.parent.mkdir(parents=True, exist_ok=True)
                q.write_bytes(body.encode('utf-8') if isinstance(body, str) else body)
            lf = root / 'exceptions.json'
            lf.write_text(good_list if list_text is None else list_text, encoding='utf-8')
            fails, counts, _ = evaluate(root, T, lf, ruled, use_git=False)
            good = bool(fails) == want_fail and all(any(w in f for f in fails) for w in want)
            if name.startswith('Week 1 files pass'):
                good = good and (counts['carrying'], counts['own'], counts['inherited'], counts['excepted'], counts['week1']) == (4, 2, 1, 1, 3)
            ok_all &= good
            print(f"  {'ok    ' if good else 'FAILED'} {name}")
            for f in fails:
                print(f'           -> {f}')
            if name.startswith('Week 1 files pass'):
                print(f"           -> counts {counts}")
    print('self-test ' + ('PASS' if ok_all else 'FAIL'))
    return 0 if ok_all else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', type=Path, default=Path('.'))
    ap.add_argument('--tree', default='Humanities_Teesside')
    ap.add_argument('--exceptions', type=Path, default=EXCEPTIONS)
    ap.add_argument('--verbose', action='store_true', help='print every file carrying the line and where its week came from')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    fails, counts, _ = evaluate(a.root.resolve(), a.tree, a.exceptions, RULED_R8_S3, verbose=a.verbose)
    sys.exit(report(fails, counts))


if __name__ == '__main__':
    main()
