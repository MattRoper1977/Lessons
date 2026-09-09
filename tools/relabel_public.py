#!/usr/bin/env python3
"""tools/relabel_public.py — the single writer for the public-relabel rule (Matt, 2026-09-08).

madebymatt.uk is public; a calendar period (week number, half-term, w/c date, "Week 9 of 14") belongs to one school's year.
On PUPIL-FACING surfaces this tool replaces calendar-specific labels with SEQUENCE-RELATIVE ones — "Lesson n of N" within
the unit (the family manifest's recommended sequence), "Lesson k" for a sibling lesson, "the previous/next unit" for a
lesson outside it, "next lesson" for "next week" — and leaves STAFF layers alone ([data-mbm-guide], TA drawers/modals,
manifests, _sownb, teacher overviews). Every rewrite is string-level and reversible: the enclosing element keeps the
original text in data-mbm-cal (attributes in data-mbm-cal-<name>); --revert restores it. A rewritten label on the TITLE STAGE
(the first .slide) also keeps a staff-layer twin of the original — <span data-mbm-guide="staff" class="mbm-cal-staff" style="display:none"> —
so the reviewed download-pack evidence (tools/downloads/SOURCE_PLACEMENT.json reads the title stage) and staff still see the
calendar declaration; pupils, and print, do not.

Modes:  --report  census only (RELABEL=report does the same) · --apply  rewrite in place · --revert  undo · --gate  0-hit gate
        --plant   plant one forbidden token into a copy and prove the gate goes red.
Forbidden public tokens (the gate): \bW(eek)?\s?\d+\b · \bAut(umn)?\s?[12]\b · \bSpr(ing)?\s?[12]\b · \bSum(mer)?\s?[12]\b · w/c · 2026-27 · "of 14" · "of 8" — the last two
are week counts ("Week 3 of 8"); the sequence-relative form this tool writes ("Lesson 3 of 8") is the rule's own target and is not a hit.
Exempt (provenance, never rewritten): source-card codes HUM-B-W10-S01 / SCI-… and lesson ids / file names (SCI_B_W9A…, LAUNCH_ART_AUT1_W3).
"""
import argparse, json, os, re, sys, html as H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORBID = re.compile(r"\bW(?:eek)?\s?\d+\b|\bAut(?:umn)?\s?[12]\b|\bSpr(?:ing)?\s?[12]\b|\bSum(?:mer)?\s?[12]\b|\bw/c\b|2026[-–]27|(?<!Lesson \d )(?<!Lesson \d\d )\bof 14\b|(?<!Lesson \d )(?<!Lesson \d\d )\bof 8\b|\b(?:BUILD|GROW|LAUNCH) Weekly\s*[-–]\s*\w+'?!?\s?[A-Z]+\d+(?::[A-Z]+\d+)?", re.I)  # the last alternative: a SoW cell reference on a pupil-facing surface (staff layers only)
EXEMPT = re.compile(r"\b(?:HUM|SCI)-[A-Z]-W\d+-[A-Z]\d+\b|\bW\d+[A-Z]?L?\d?-S\d+\b|\b(?:SCI|HUM|ART)_[A-Z]+_[A-Z0-9_]*W\d+[A-Z0-9_]*\b|\b[A-Z]+_(?:HUM|ART|ASDAN)_[A-Z0-9_]*W\d+[A-Za-z0-9_]*\b|\bLAUNCH_ART_AUT\d_W\d+\b")
STAFF_ATTR = ('data-mbm-guide',); STAFF_CLASSES = {'ta-drawer', 'mbm-modal', 'staff-only', 'teacher-only', 'ta-note', 'ta-focus', 'staffnote'}
STAFF_IDS = {'mbmTA', 'ta', 'staff', 'teacher-notes'}
PROVENANCE_CLASSES = {'source-card', 'learner-source-ref', 'provenance', 'citation', 'source-board', 'sources', 'lab-note'}  # citation surfaces: kept verbatim (§P1), exempt from the gate; STAFF_IDS = {'mbmTA', 'ta', 'staff', 'teacher-notes'}
SKIP_TAGS = {'script', 'style', 'template', 'noscript'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
ATTRS = ('data-title', 'aria-label', 'title', 'data-page-title', 'alt', 'content')
SEP = '⁋'
BANNED = ('the previous unit', 'the next unit')   # LF1: labels this tool must never author. See Unresolvable.


class Unresolvable(Exception):
    """A calendar label that cannot be turned into a sequence-relative one.

    The first version of this tool answered these with 'the previous unit' or
    'the next unit'. Neither is a translation of a week number; both are a guess.
    On 2026-09-08 they replaced 121 specific week references across 22 published
    pages, and every one of them was wrong — W5, W6 and W7 all became the same
    four words, ranges became "the previous unit-the previous unit", and "the W14
    question" became "the the next unit question".

    A tool that cannot resolve a label must say which label, in which file, with
    the sentence it appears in, and then change nothing. A human decides what a
    pupil reads. LF1 C2.
    """

    def __init__(s, week, letter, reason, path=None, context=None):
        s.week, s.letter, s.reason, s.path, s.context = week, letter, reason, path, context
        super().__init__(reason)

    def report(s):
        tok = 'W%d%s' % (s.week, s.letter or '')
        ctx = re.sub(r'\s+', ' ', (s.context or '')).strip()
        return ('REFUSING %s\n'
                '  cannot resolve %s: %s\n'
                '  in: "%s"\n'
                '  Nothing was written. Decide what a pupil should read here, or give this\n'
                '  unit a manifest entry for that week; this tool will not guess. (LF1 C2)'
                % (s.path or '?', tok, s.reason, ctx[:240]))


def added_banned(before, after):
    """B6: the post-condition. 'the previous unit' can be honest prose a teacher wrote,
    so the assertion is that a run never INCREASES the count, not that it is zero."""
    return [(b, before.count(b), after.count(b)) for b in BANNED if after.count(b) > before.count(b)]
TOK = re.compile(r'(<!--.*?-->|<script\b.*?</script\s*>|<style\b.*?</style\s*>|<template\b.*?</template\s*>|<[^>]+>)', re.S | re.I)

def chassis(p):
    if 'v3_40min' in p: return 'sci-v3'
    if 'Science' in p and 'W8-W13' in p: return 'sci-w8'
    if 'Science' in p: return 'sci-light'
    if 'BUILD_W9' in p: return 'hum-v4'
    if 'GROW_W9' in p: return 'hum-v31'
    if 'LAUNCH_W9' in p: return 'hum-launch'
    return 'classic'

def entry_week(x):
    """A lesson's teaching week comes from its manifest entry — the ruled workbook cell (cells[].termWeek) or the entry's own
    week field — never from a path (VB-RUN13 R0 / g27)."""
    if isinstance(x.get('absoluteWeek'), int): return x['absoluteWeek']
    if isinstance(x.get('week'), int): return x['week']
    for c in x.get('cells') or []:
        if isinstance(c.get('absoluteWeek'), int): return c['absoluteWeek']
    return None

def manifest_lessons(mf):
    """(entries, unit title) from a manifest, whatever envelope it uses.

    Two envelopes are in the estate and both are legitimate. Most manifests are an
    OBJECT carrying the sequence under 'lessons' or 'sequence'. Three -- the
    Science v3_40min ones for Build, Grow and Launch -- are the ARRAY itself, and
    their entries carry the same per-entry fields the object form does (file,
    week, id), so it is a third envelope for the same data rather than a different
    schema. Build and Launch entries have week numbers; Grow's do not, which is not
    this function's problem: an entry with no week is already skipped, and a file
    whose unit yields no weeks refuses rather than being guessed at.

    Anything else is not a manifest this tool understands. It returns no entries,
    which leaves the file with no sequence and makes lesson_ref refuse -- the same
    outcome as no manifest at all. It must never raise: `m.get(...)` on a
    top-level array raised AttributeError on 47 served pages, and a crash is worse
    than a refusal because it aborts the run wherever it reached and says nothing
    about the files after it.
    """
    try:
        m = json.load(open(mf, encoding='utf-8'))
    except (OSError, ValueError):
        return [], ''
    if isinstance(m, list):
        return [x for x in m if isinstance(x, dict)], ''
    if isinstance(m, dict):
        L = m.get('lessons') or m.get('sequence') or []
        return ([x for x in L if isinstance(x, dict)] if isinstance(L, list) else []), (m.get('title') or '')
    return [], ''


def sequence(path):
    """The family's recommended lesson sequence (manifest order, RX3 _CLASSIC siblings excluded): (n, N, unit, weekmap, weeks).
    Weeks come from the manifest entries only; a file with no manifest entry gets n=None and its own-week strips are left alone."""
    d = os.path.dirname(path); mf = next((os.path.join(d, m) for m in ('manifest-v3.1.json', 'manifest-v3.json', 'manifest.json') if os.path.exists(os.path.join(d, m))), None)
    files = []; unit = ''
    if mf:
        L, unit = manifest_lessons(mf)
        for x in L:
            f = x.get('file') or x.get('path') or ''
            if not f or '_CLASSIC' in (x.get('id') or '') or '_Classic' in f or 'START_HERE' in f: continue
            w = entry_week(x)
            if w is None: continue
            files.append((w, f))
    names = [f for _, f in files]   # manifest order IS the recommended sequence; never re-sorted, never read from a path
    base = os.path.basename(path); n = names.index(base) + 1 if base in names else None; N = len(names)
    weekmap = {}
    for i, (w, f) in enumerate(files): weekmap.setdefault(w, []).append(i + 1)
    own = files[n - 1][0] if n else None
    if FORBID.search(unit or ''): unit = ''
    return n, N, unit, weekmap, [w for w, _ in files], own

class Rewriter:
    def __init__(s, path, rel):
        s.n, s.N, s.unit, s.weekmap, s.weeks, s.own = sequence(path); s.rel = rel
        s.lo, s.hi = (min(s.weeks), max(s.weeks)) if s.weeks else (None, None)
    def lesson_ref(s, w, letter=None):
        if w == s.own and not letter: return 'this lesson'
        if s.lo is None:
            raise Unresolvable(w, letter, 'this file has no manifest entry, so it has no sequence to be relative to')
        if w < s.lo or w > s.hi:
            raise Unresolvable(w, letter, "it is outside this unit's manifest weeks %d-%d" % (s.lo, s.hi))
        ns = s.weekmap.get(w)
        if not ns:
            raise Unresolvable(w, letter, "it falls inside the unit's weeks %d-%d but no manifest lesson claims it" % (s.lo, s.hi))
        if letter:
            k = {'A': 0, 'B': 1, 'L1': 0, 'L2': 1, 'L3': 2}.get(letter.upper().replace('L', 'L') if len(letter) > 1 else letter.upper(), 0)
            return 'Lesson %d' % ns[min(k, len(ns) - 1)]
        return 'Lesson %d' % ns[0] if len(ns) == 1 else 'Lessons %d–%d' % (ns[0], ns[-1])
    def text(s, t):
        try:
            return s._text(t)
        except Unresolvable as e:
            if e.context is None: e.context = t
            raise

    def _text(s, t):
        o = t
        if s.n:
            t = re.sub(r'\bWeek\s?\d+\s+of\s+\d+\b', 'Lesson %d of %d' % (s.n, s.N), t)
            t = re.sub(r'\bAut(?:umn)?\s?[12]\s*·\s*W(?:eek)?\s?\d+\b', 'Lesson %d of %d' % (s.n, s.N), t)
            t = re.sub(r'\bAut(?:umn)?\s?[12]\s*·\s*(?=W(?:eek)?\s?\d+)', '', t)
        # own week labels in title strips: "· Week 11" / "W11 ·" with the file's own week -> Lesson n of N
        def wk(m):
            w = int(m.group(2)); letter = m.group(3) or ''
            if w == s.own and s.n and not letter: return 'Lesson %d of %d' % (s.n, s.N)
            return s.lesson_ref(w, letter or None)
        t = re.sub(r'\b(Week\s?|W)(\d+)((?:[AB]|L[1-3])?)\b', wk, t)
        t = re.sub(r'\s*·\s*(?:Autumn|Spring|Aut|Spr)\s?[12]\b', '', t)
        t = re.sub(r'\b(?:Autumn|Spring|Aut|Spr)\s?[12]\s*·\s*', '', t)
        t = re.sub(r'\b(?:Autumn|Spring|Aut|Spr)\s?[12]\b', 'this term', t)
        t = re.sub(r'\s*·\s*2026[-–]27\b', '', t); t = re.sub(r'\b2026[-–]27\s*·\s*', '', t); t = re.sub(r'\b2026[-–]27\b', '', t)
        t = re.sub(r'\s*·\s*(?:BUILD|GROW|LAUNCH) Weekly\s*[–-]\s*\w+\s+[A-Z]+\d+(?::[A-Z]+\d+)?', '', t)
        t = re.sub(r'\bSoW:\s*(?:BUILD|GROW|LAUNCH) Weekly\s*[-–]\s*\w+\'?!?\s?[A-Z]+\d+(?::[A-Z]+\d+)?\s*[—–-]\s*', 'SoW outcome: ', t)
        t = re.sub(r'\s*·\s*(?:BUILD|GROW|LAUNCH) Weekly\s*[-–]\s*\w+\'?!?\s?[A-Z]+\d+(?::[A-Z]+\d+)?', '', t)
        t = re.sub(r'(?:BUILD|GROW|LAUNCH) Weekly\s*[-–]\s*\w+\'?!?\s?[A-Z]+\d+(?::[A-Z]+\d+)?', 'the curriculum workbook', t)
        t = re.sub(r'\bw/c\s+\d{1,2}\s+\w+(?:\s+\d{4})?', 'this lesson', t, flags=re.I)
        t = re.sub(r'\b(next|last|this|previous)\s+week\b', lambda m: m.group(1) + ' lesson', t, flags=re.I)
        if s.unit and s.rel and t != o and 'Lesson %d of %d' % (s.n or 0, s.N) in t and s.unit not in t and len(t) < 90: pass
        return t

def walk(html_text, path, mode, rel=True):
    """mode: 'census' -> hits; 'apply' -> (new_html, changes); 'revert' -> (new_html, restored)"""
    rw = Rewriter(path, rel) if mode == 'apply' else None
    toks = TOK.split(html_text); stack = []; hits = []; changes = {}; attr_changes = {}; restored = 0; seen_slide = [False]
    def instaff(): return any(x[2] for x in stack)
    def intitle(): return any(x[5] for x in stack)
    for i, tk in enumerate(toks):
        if not tk: continue
        if tk.startswith('<'):
            if tk.startswith('<!--') or tk.lower().startswith(('<script', '<style', '<template')) or tk.startswith('<!'): continue
            if tk.startswith('</'):
                name = re.match(r'</\s*([a-zA-Z][\w-]*)', tk).group(1).lower()
                for j in range(len(stack) - 1, -1, -1):
                    if stack[j][0] == name: del stack[j:]; break
                continue
            m = re.match(r'<\s*([a-zA-Z][\w-]*)', tk); name = m.group(1).lower() if m else ''
            rawattrs = dict((k.lower(), v) for k, v in re.findall(r'([\w:-]+)\s*=\s*"([^"]*)"', tk)); attrs = dict((k, H.unescape(v)) for k, v in rawattrs.items())
            cls = set((attrs.get('class') or '').split())
            staff = any(k in attrs for k in STAFF_ATTR) or bool(cls & STAFF_CLASSES) or bool(cls & PROVENANCE_CLASSES) or attrs.get('id') in STAFF_IDS or name in SKIP_TAGS
            # attributes on this tag
            if not staff and not instaff():
                for a in ATTRS:
                    if a == 'content' and name != 'meta': continue
                    if a == 'content' and (attrs.get('name') or attrs.get('property')) not in ('description', 'og:description', 'og:title', 'twitter:title', 'twitter:description'): continue
                    v = attrs.get(a)
                    if v and not EXEMPT.search(v) and FORBID.search(v):
                        if mode == 'census': hits.append(('attr:' + a, v, name))
                        elif mode == 'apply':
                            nv = rw.text(v)
                            if nv != v:
                                tk = re.sub(r'(\b%s\s*=\s*")([^"]*)(")' % re.escape(a), lambda mm: mm.group(1) + H.escape(nv, quote=True) + mm.group(3), tk, count=1)
                                tk = re.sub(r'\s*/?>$', lambda mm: ' data-mbm-cal-%s="%s"%s' % (a, rawattrs[a].replace('"', '&quot;'), mm.group(0)), tk, count=1); attr_changes[i] = True
                    if mode == 'revert' and ('data-mbm-cal-' + a) in attrs:
                        ov = rawattrs['data-mbm-cal-' + a]
                        tk = re.sub(r'(\b%s\s*=\s*")([^"]*)(")' % re.escape(a), lambda mm: mm.group(1) + ov + mm.group(3), tk, count=1)
                        tk = re.sub(r'\s+data-mbm-cal-%s="[^"]*"' % re.escape(a), '', tk, count=1); restored += 1
                toks[i] = tk
            if name in VOID or tk.rstrip().endswith('/>'): continue
            title = False
            if 'slide' in cls and not seen_slide[0]: seen_slide[0] = True; title = True
            stack.append([name, i, staff, 0, attrs.get('data-mbm-cal'), title])
            continue
        # text node
        if not stack: continue
        top = stack[-1]; idx = top[3]; top[3] += 1
        if instaff(): continue
        raw = tk; plain = H.unescape(raw)
        if mode == 'census':
            for m in FORBID.finditer(plain):
                seg = plain[max(0, m.start() - 40): m.end() + 40]
                if EXEMPT.search(seg) and EXEMPT.search(seg).start() <= (m.start() - max(0, m.start() - 40)) <= EXEMPT.search(seg).end(): continue
                hits.append(('text', re.sub(r'\s+', ' ', plain).strip(), top[0])); break
        elif mode == 'apply':
            if not FORBID.search(plain) and not re.search(r'\b(next|last|this|previous)\s+week\b', plain, re.I): continue
            parts = []; pos = 0   # rewrite outside exempt spans only
            for e in EXEMPT.finditer(plain):
                parts.append(rw.text(plain[pos:e.start()])); parts.append(e.group(0)); pos = e.end()
            parts.append(rw.text(plain[pos:])); new = ''.join(parts)
            if new != plain:
                if not new.strip(): new = ' '   # never leave an empty text node: --revert counts text nodes by position
                toks[i] = H.escape(new, quote=False) if '&' in raw or '<' in plain else new
                if intitle() and FORBID.search(plain):
                    # the title stage's calendar declaration moves to a STAFF layer (guide-on shows it; screen and print hide it)
                    toks[i] += '<span data-mbm-guide="staff" class="mbm-cal-staff" style="display:none">' + H.escape(plain.strip(), quote=False) + '</span>'
                changes.setdefault(top[1], []).append((idx, raw))
        elif mode == 'revert' and top[4]:
            cal = dict((int(k), v) for k, v in (x.split('=', 1) for x in top[4].split(SEP) if '=' in x))
            if idx in cal: toks[i] = cal[idx]; restored += 1
    if mode == 'census': return hits
    if mode == 'apply':
        for ti, lst in changes.items():
            val = SEP.join('%d=%s' % (k, v) for k, v in lst)
            toks[ti] = re.sub(r'\s*/?>$', lambda mm: ' data-mbm-cal="%s"%s' % (H.escape(val, quote=True), mm.group(0)), toks[ti], count=1)
        return ''.join(toks), sum(len(v) for v in changes.values()) + len(attr_changes)
    if mode == 'revert':
        out = ''.join(toks); out = re.sub(r'\s+data-mbm-cal="[^"]*"', '', out); out = re.sub(r'<span data-mbm-guide="staff" class="mbm-cal-staff" style="display:none">.*?</span>', '', out, flags=re.S); return out, restored


def manifest_lessons_probe(obj):
    """self-test helper: manifest_lessons() against an in-memory manifest."""
    import tempfile as _t
    with _t.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
        json.dump(obj, fh); name = fh.name
    try:
        return manifest_lessons(name)
    finally:
        os.unlink(name)


def self_test():
    """LF1 B. Proves both directions: a resolvable label is still rewritten, an
    unresolvable one aborts the file with its bytes untouched and a non-zero exit."""
    import shutil, subprocess, tempfile
    ok = [0]; bad = []
    def check(name, cond):
        ok[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: bad.append(name)

    def unit(tmp, weeks, files=None, title='Autumn Science'):
        d = os.path.join(tmp, 'unit'); os.makedirs(d, exist_ok=True)
        files = files or ['L%d.html' % (i + 1) for i in range(len(weeks))]
        json.dump({'title': title, 'lessons': [{'file': f, 'week': w, 'id': f}
                                               for f, w in zip(files, weeks)]},
                  open(os.path.join(d, 'manifest.json'), 'w'))
        return d

    def write(d, name, body):
        q = os.path.join(d, name); open(q, 'w', encoding='utf-8').write('<body><p>%s</p></body>' % body); return q

    def apply_one(q):
        return subprocess.run([sys.executable, os.path.abspath(__file__), '--apply', q],
                              capture_output=True, text=True)

    with tempfile.TemporaryDirectory() as tmp:
        d = unit(tmp, [8, 9, 10])
        # ---- green direction: the tool still does its job
        q = write(d, 'L1.html', 'Recap W9 and the W10 planner.')
        r = apply_one(q); body = open(q, encoding='utf-8').read()
        check('in-unit weeks still rewrite (W9 -> Lesson 2, W10 -> Lesson 3)',
              r.returncode == 0 and 'Lesson 2' in body and 'Lesson 3' in body)
        check('a resolvable run authors no banned label', not any(b in body for b in BANNED))
        q = write(d, 'L1.html', 'Week 8 of 3 · W8 today.')
        apply_one(q); body = open(q, encoding='utf-8').read()
        check('own week becomes "this lesson" / "Lesson 1 of 3"',
              'this lesson' in body or 'Lesson 1 of 3' in body)
        q = write(d, 'L3.html', 'Last lesson: retrieve W8.')
        apply_one(q)
        check('last lesson of a unit resolves a sibling week', 'Lesson 1' in open(q, encoding='utf-8').read())

        # ---- red direction: every shape that produced the live defect now refuses
        for name, body_in, why in [
            ('sibling week below the unit (W6 in an 8-10 unit)', 'W6: foods can be grouped.', 'outside'),
            ('sibling week above the unit (W14 in an 8-10 unit)', 'Plan the W14 repeats.', 'outside'),
            ('a range (W6-W7) refuses rather than doubling the phrase', 'Recap W6-W7 evidence.', 'outside'),
            ('an article-led reference ("the W14 question")', 'Write the W14 question.', 'outside'),
        ]:
            q = write(d, 'L2.html', body_in); before = open(q, 'rb').read()
            r = apply_one(q)
            check(name, r.returncode == 2 and 'REFUSING' in r.stdout)
            check('  ... and the file is byte-unchanged', open(q, 'rb').read() == before)
            check('  ... and the refusal quotes the sentence', body_in.split(':')[0][:12] in r.stdout)

        # ---- the shapes the order named: flat folder, single-lesson unit
        flat = os.path.join(tmp, 'flat'); os.makedirs(flat)
        q = write(flat, 'X.html', 'Recap W3 evidence.'); before = open(q, 'rb').read()
        r = apply_one(q)
        check('flat folder (no manifest) refuses instead of guessing',
              r.returncode == 2 and 'no manifest entry' in r.stdout and open(q, 'rb').read() == before)
        shutil.rmtree(os.path.join(tmp, 'unit'))
        d1 = unit(tmp, [14], ['S1.html'])
        q = write(d1, 'S1.html', 'Builds on W12 DNA.'); before = open(q, 'rb').read()
        r = apply_one(q)
        check('single-lesson unit (lo == hi) refuses a week outside it',
              r.returncode == 2 and open(q, 'rb').read() == before)
        q = write(d1, 'S1.html', 'W14 today.'); r = apply_one(q)
        check('single-lesson unit still resolves its own week', r.returncode == 0)

        # ---- a gap inside the unit's range
        shutil.rmtree(os.path.join(tmp, 'unit'))
        d2 = unit(tmp, [8, 10], ['G1.html', 'G2.html'])
        q = write(d2, 'G1.html', 'Recap W9.'); r = apply_one(q)
        check('a week inside the range that no lesson claims refuses',
              r.returncode == 2 and 'no manifest lesson claims it' in r.stdout)

        # ---- B6 post-condition, and honest prose
        check('B6 sees an increase', added_banned('x', 'x the next unit') != [])
        check('B6 ignores prose the author wrote', added_banned('go on to the next unit.', 'go on to the next unit.') == [])
        shutil.rmtree(os.path.join(tmp, 'unit'), ignore_errors=True)
        d3 = unit(tmp, [8], ['P1.html'])
        q = write(d3, 'P1.html', 'Leave a gap and go on to the next unit.')
        r = apply_one(q)
        check('a page whose author wrote "the next unit" is left alone and passes',
              r.returncode == 0 and 'the next unit' in open(q, encoding='utf-8').read())

        # ---- --revert is untouched by this change
        q = write(d3, 'P1.html', 'W8 today, recap W8 again.'); before = open(q, 'rb').read()
        apply_one(q)
        subprocess.run([sys.executable, os.path.abspath(__file__), '--revert', q], capture_output=True)
        check('--revert still restores the original bytes', open(q, 'rb').read() == before)

        # ---- manifest envelopes: three shapes, none of them may crash (LF1-G 3.1)
        shutil.rmtree(os.path.join(tmp, 'unit'), ignore_errors=True)
        arr = os.path.join(tmp, 'arr'); os.makedirs(arr, exist_ok=True)
        json.dump([{'id': 'W3A', 'week': 3, 'file': 'A1.html'},
                   {'id': 'W4A', 'week': 4, 'file': 'A2.html'}],
                  open(os.path.join(arr, 'manifest-v3.json'), 'w'))
        q = write(arr, 'A1.html', 'Recap W4 method.')
        r = apply_one(q)
        check('an ARRAY manifest resolves instead of crashing',
             r.returncode == 0 and 'Lesson 2' in open(q, encoding='utf-8').read())
        check('  ... and does not raise AttributeError', 'AttributeError' not in r.stdout + r.stderr)
        q = write(arr, 'A1.html', 'Recap W9 method.'); before = open(q, 'rb').read()
        r = apply_one(q)
        check('an ARRAY manifest still REFUSES an out-of-unit week',
             r.returncode == 2 and 'REFUSING' in r.stdout and open(q, 'rb').read() == before)

        noweek = os.path.join(tmp, 'noweek'); os.makedirs(noweek, exist_ok=True)
        json.dump([{'id': 'W3A', 'file': 'N1.html', 'mission': 'no week field'}],
                  open(os.path.join(noweek, 'manifest-v3.json'), 'w'))
        q = write(noweek, 'N1.html', 'Recap W3 method.'); before = open(q, 'rb').read()
        r = apply_one(q)
        check('an ARRAY manifest whose entries carry no week refuses, byte-unchanged',
             r.returncode == 2 and open(q, 'rb').read() == before)

        for name, blob in [('a bare string', '"not a manifest"'),
                           ('a number', '42'),
                           ('an object with no lessons key', '{"title": "x"}'),
                           ('a truncated file', '{"lessons": [')]:
            odd = os.path.join(tmp, 'odd'); os.makedirs(odd, exist_ok=True)
            open(os.path.join(odd, 'manifest-v3.json'), 'w').write(blob)
            q = write(odd, 'O1.html', 'Recap W3 method.'); before = open(q, 'rb').read()
            r = apply_one(q)
            check('%s is refused, not crashed' % name,
                 r.returncode == 2 and 'Traceback' not in r.stdout + r.stderr
                 and open(q, 'rb').read() == before)
            shutil.rmtree(odd)

        check('manifest_lessons reads the object envelope',
             manifest_lessons_probe({'lessons': [{'file': 'x'}], 'title': 'T'}) == ([{'file': 'x'}], 'T'))
        check('manifest_lessons reads the array envelope',
             manifest_lessons_probe([{'file': 'x'}]) == ([{'file': 'x'}], ''))
        check('manifest_lessons drops non-dict entries',
             manifest_lessons_probe([{'file': 'x'}, 'junk', 7]) == ([{'file': 'x'}], ''))

        # ---- the live regression itself, when the repo is present
        live = os.path.join(ROOT, 'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html')
        if os.path.exists(live):
            src = open(live, encoding='utf-8').read()
            rev, _ = walk(src, live, 'revert')            # the pre-relabel bytes, from the file's own store
            try:
                walk(rev, live, 'apply'); caught = False
            except Unresolvable as e:
                caught = 'outside' in e.reason
            check('the real page that broke (SCI_B_W8A, W5/W6/W7B) now refuses', caught)

    print('\n%d checks, %d failed' % (ok[0], len(bad)))
    for b in bad: print('  FAILED:', b)
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(); g.add_argument('--report', action='store_true'); g.add_argument('--apply', action='store_true'); g.add_argument('--revert', action='store_true'); g.add_argument('--gate', action='store_true'); g.add_argument('--plant', action='store_true'); g.add_argument('--self-test', action='store_true', dest='self_test')
    ap.add_argument('--json'); ap.add_argument('files', nargs='*'); a = ap.parse_args()
    if a.self_test: sys.exit(self_test())
    if os.environ.get('RELABEL') == 'report': a.report, a.apply = True, False
    total = 0; refused = 0; out = {}
    for p in a.files:
        s = open(p, encoding='utf-8').read()
        if a.apply:
            try:
                new, n = walk(s, p, 'apply')
            except Unresolvable as e:
                e.path = p; print(e.report()); out[p] = {'refused': e.reason, 'week': e.week}; refused += 1; continue
            grew = added_banned(s, new)
            if grew:                        # B6: unreachable by construction, asserted anyway
                print('REFUSING %s\n  the run would author %s (%d -> %d). Nothing was written.'
                      % (p, grew[0][0], grew[0][1], grew[0][2])); out[p] = {'refused': 'banned label'}; refused += 1; continue
            open(p, 'w', encoding='utf-8').write(new); hits = walk(new, p, 'census'); print(f'{p}: rewrote {n} · residual pupil-facing tokens {len(hits)}'); out[p] = {'rewrote': n, 'residual': hits}; total += len(hits)
        elif a.revert:
            new, n = walk(s, p, 'revert'); open(p, 'w', encoding='utf-8').write(new); print(f'{p}: restored {n}'); out[p] = n
        elif a.plant:
            planted = s.replace('<h1', '<h1 data-plant="1">Week 99 of 14 </h1><h1', 1) if '<h1' in s else s.replace('<body', '<body><p>Week 99 of 14</p><span', 1)
            hits = walk(planted, p, 'census'); ok = any('Week 99' in h[1] for h in hits); print(f'{p}: planted token caught={ok}'); total += 0 if ok else 1
        else:
            hits = walk(s, p, 'census'); out[p] = hits; total += len(hits); print(f'{p}: {len(hits)} pupil-facing calendar tokens')
    if a.json: json.dump(out, open(a.json, 'w'), indent=1, ensure_ascii=False)
    if a.apply and refused: print(f'REFUSED {refused} file(s); every one of them is byte-unchanged.'); sys.exit(2)
    if a.gate or a.apply: print('GATE', 'PASS' if total == 0 else f'FAIL ({total} hits)'); sys.exit(0 if total == 0 else 1)
    if a.plant: sys.exit(total)
if __name__ == '__main__': main()
