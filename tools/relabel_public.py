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

def sequence(path):
    """The family's recommended lesson sequence (manifest order, RX3 _CLASSIC siblings excluded): (n, N, unit, weekmap, weeks).
    Weeks come from the manifest entries only; a file with no manifest entry gets n=None and its own-week strips are left alone."""
    d = os.path.dirname(path); mf = next((os.path.join(d, m) for m in ('manifest-v3.1.json', 'manifest-v3.json', 'manifest.json') if os.path.exists(os.path.join(d, m))), None)
    files = []; unit = ''
    if mf:
        m = json.load(open(mf, encoding='utf-8')); L = m.get('lessons') or m.get('sequence') or []; unit = m.get('title') or ''
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
        if s.lo is not None and w < s.lo: return 'the previous unit'
        if s.hi is not None and w > s.hi: return 'the next unit'
        ns = s.weekmap.get(w)
        if not ns: return 'the next unit' if (s.own and w > s.own) else 'the previous unit'
        if letter:
            k = {'A': 0, 'B': 1, 'L1': 0, 'L2': 1, 'L3': 2}.get(letter.upper().replace('L', 'L') if len(letter) > 1 else letter.upper(), 0)
            return 'Lesson %d' % ns[min(k, len(ns) - 1)]
        return 'Lesson %d' % ns[0] if len(ns) == 1 else 'Lessons %d–%d' % (ns[0], ns[-1])
    def text(s, t):
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

def main():
    ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(); g.add_argument('--report', action='store_true'); g.add_argument('--apply', action='store_true'); g.add_argument('--revert', action='store_true'); g.add_argument('--gate', action='store_true'); g.add_argument('--plant', action='store_true')
    ap.add_argument('--json'); ap.add_argument('files', nargs='+'); a = ap.parse_args()
    if os.environ.get('RELABEL') == 'report': a.report, a.apply = True, False
    total = 0; out = {}
    for p in a.files:
        s = open(p, encoding='utf-8').read()
        if a.apply:
            new, n = walk(s, p, 'apply'); open(p, 'w', encoding='utf-8').write(new); hits = walk(new, p, 'census'); print(f'{p}: rewrote {n} · residual pupil-facing tokens {len(hits)}'); out[p] = {'rewrote': n, 'residual': hits}; total += len(hits)
        elif a.revert:
            new, n = walk(s, p, 'revert'); open(p, 'w', encoding='utf-8').write(new); print(f'{p}: restored {n}'); out[p] = n
        elif a.plant:
            planted = s.replace('<h1', '<h1 data-plant="1">Week 99 of 14 </h1><h1', 1) if '<h1' in s else s.replace('<body', '<body><p>Week 99 of 14</p><span', 1)
            hits = walk(planted, p, 'census'); ok = any('Week 99' in h[1] for h in hits); print(f'{p}: planted token caught={ok}'); total += 0 if ok else 1
        else:
            hits = walk(s, p, 'census'); out[p] = hits; total += len(hits); print(f'{p}: {len(hits)} pupil-facing calendar tokens')
    if a.json: json.dump(out, open(a.json, 'w'), indent=1, ensure_ascii=False)
    if a.gate or a.apply: print('GATE', 'PASS' if total == 0 else f'FAIL ({total} hits)'); sys.exit(0 if total == 0 else 1)
    if a.plant: sys.exit(total)
if __name__ == '__main__': main()
