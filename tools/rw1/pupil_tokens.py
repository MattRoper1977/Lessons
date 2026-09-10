#!/usr/bin/env python3
"""LW1 §A2 · one census of week tokens and dates on PUPIL surfaces, for every
return-week lesson file in every pathway.

WHY ONE STEP AND NOT THREE. All three packs ship the same defect because one
generator made them: a dated week label repeated across pupil surfaces. Fixing it
three times would mean three inclusion rules to keep in step, and the next fix
would land in two of them. So the property is tested once, here.

TEST THE PROPERTY, NOT THE PHRASE (RW1-E §C3). An earlier check grepped
"w/c 19 October 2026" and missed three pupil sheets carrying the bare date. This
matches ANY week token and ANY date, independently of each other and of any
prefix:

  week token : W8, W 8, Week 8, w/c, 2026-27, Autumn 2
  date       : "19 October 2026", "19/10/2026", "2026-10-19", "19 Oct 26"

PUPIL vs STAFF IS DECIDED BY DOM ANCESTRY, never by proximity in the source. The
openstax link in LAUNCH sits 6,917 characters after the nearest "teacher-only"
string and is nonetheless inside the staff dialog; a proximity rule would have
called it pupil-facing.

Every count carries its denominator (GW1-B §R1): text nodes examined, attributes
examined, and the split between pupil and staff must reconcile to the total.
"""
import re, sys, argparse
from html import escape
from pathlib import Path
import lxml.html

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pathways

MONTHS = ('January|February|March|April|May|June|July|August|September|October'
          '|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec')
WEEK = re.compile(r'\bW\s?\d{1,2}\b|\bWeeks?\s?\d{1,2}\b|\bw/c\b|\b20\d\d-\d\d\b'
                  r'|\bAutumn\s?[12]\b|\bSpring\s?[12]\b|\bSummer\s?[12]\b', re.I)
DATE = re.compile(r'\b\d{1,2}\s+(?:%s)\.?\s+\d{2,4}\b' % MONTHS      # 19 October 2026
                  + r'|\b(?:%s)\.?\s+\d{1,2},?\s+\d{2,4}\b' % MONTHS  # October 19, 2026
                  + r'|\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b'           # 19/10/2026
                  + r'|\b20\d\d-\d{2}-\d{2}\b', re.I)                 # 2026-10-19

# An element is STAFF if it or an ancestor carries one of these. The guide layer
# is display:none until html.mbm-guide-on, and the print sections marked staff
# are the four the teacher keeps.
STAFF_XPATH = ('ancestor-or-self::*['
               '@data-mbm-guide'
               ' or contains(concat(" ",normalize-space(@class)," ")," teacher-only ")'
               ' or contains(concat(" ",normalize-space(@class)," ")," staff-only ")'
               ' or contains(concat(" ",normalize-space(@class)," ")," mk-print ")'
               ' or contains(concat(" ",normalize-space(@class)," ")," ta-drawer ")'
               ' or @data-print-route="staff"'
               ']')

# Attributes that reach a person: read aloud, shown on hover, or used as a label.
SPOKEN = ('aria-label', 'title', 'alt', 'data-title', 'placeholder', 'summary')
# data-mbm-cal is the relabeller's UNDO BUFFER: it holds the ORIGINAL pre-rewrite
# text so a rewrite is reversible. It is never rendered. Counting it as a pupil
# surface would report every reversible relabel as a violation.
IGNORED_ATTRS = ('data-mbm-cal',)


def scan(path):
    return scan_text(Path(path).read_text(encoding='utf-8'))


def scan_text(text):
    doc = lxml.html.document_fromstring(text)
    for bad in doc.xpath('//script | //style'):
        bad.getparent().remove(bad)

    rows = []
    nodes = attrs = 0
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        staff = bool(el.xpath(STAFF_XPATH))
        for kind, value in ([('text', el.text)] + [('tail', el.tail)]
                            + [('@' + a, el.get(a)) for a in SPOKEN
                               if a not in IGNORED_ATTRS]):
            if not value or not value.strip():
                continue
            if kind in ('text', 'tail'):
                nodes += 1
            else:
                attrs += 1
            for label, rx in (('week', WEEK), ('date', DATE)):
                for m in rx.finditer(value):
                    rows.append({'kind': label, 'where': kind, 'staff': staff,
                                 'tag': el.tag, 'match': m.group(0),
                                 # raw is the node value EXACTLY as parsed. The
                                 # scrub edits raw bytes, so a whitespace-
                                 # normalised preview cannot be what it matches
                                 # on -- the organiser header is spaced with
                                 # double spaces and normalising loses that.
                                 'raw': value,
                                 'context': re.sub(r'\s+', ' ', value)[:110]})
    return rows, {'text_nodes': nodes, 'attributes': attrs,
                  'elements': sum(1 for e in doc.iter() if isinstance(e.tag, str))}


def report(paths, verbose=False):
    print('%-46s %7s %7s %7s %7s %7s %7s' % (
        'file', 'pupilWK', 'pupilDT', 'staffWK', 'staffDT', 'nodes', 'attrs'))
    bad = 0
    for p in paths:
        rows, den = scan(p)
        pw = sum(1 for r in rows if r['kind'] == 'week' and not r['staff'])
        pd = sum(1 for r in rows if r['kind'] == 'date' and not r['staff'])
        sw = sum(1 for r in rows if r['kind'] == 'week' and r['staff'])
        sd = sum(1 for r in rows if r['kind'] == 'date' and r['staff'])
        assert pw + pd + sw + sd == len(rows), 'pupil/staff split does not reconcile'
        if not den['text_nodes'] or not den['elements']:
            print('   [DENOMINATOR ZERO] %s -- nothing examined' % p)
            bad += 1
            continue
        print('%-46s %7d %7d %7d %7d %7d %7d'
              % (Path(p).name[:46], pw, pd, sw, sd, den['text_nodes'], den['attributes']))
        if pw or pd:
            bad += 1
        if verbose:
            for r in rows:
                if not r['staff']:
                    print('      %-5s %-7s <%s> %-18r  %s'
                          % (r['kind'], r['where'], r['tag'], r['match'], r['context']))
    print('\nfiles with a week token or a date on a PUPIL surface: %d of %d'
          % (bad, len(paths)))
    return bad


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--pathway', action='append', default=[])
    ap.add_argument('--pack', help='pack root, used with --pathway')
    ap.add_argument('-v', '--verbose', action='store_true')
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()

    if a.self_test:
        # GW1-B R3: the control is proved to fire before any zero is believed.
        import tempfile, os
        ok = True
        for name, html in [
            ('bare date, no w/c', '<p>Sheet · 19 October 2026 · Supported</p>'),
            ('week token only',   '<p>Week 8 starter</p>'),
            ('w/c form',          '<p>w/c 19 October 2026</p>'),
            ('numeric date',      '<p>due 19/10/2026</p>'),
            ('iso date',          '<p>2026-10-19</p>'),
            ('staff-gated date',  '<div data-mbm-guide="staff"><p>19 October 2026</p></div>'),
            ('undo buffer only',  '<p data-mbm-cal="0=Week 8">sequence</p>'),
        ]:
            f = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
            f.write('<html><body>%s</body></html>' % html); f.close()
            rows, _ = scan(f.name)
            pupil = [r for r in rows if not r['staff']]
            want = name not in ('staff-gated date', 'undo buffer only')
            got = bool(pupil)
            print('  %-20s pupil hits %d   %s' % (name, len(pupil),
                                                  'PASS' if got == want else '*** FAIL ***'))
            ok &= (got == want)
            os.unlink(f.name)
        print('\nself-test %s' % ('PASS -- the census can find each shape it claims to'
                                  if ok else 'FAIL'))
        sys.exit(0 if ok else 1)

    paths = list(a.paths)
    for name in a.pathway:
        pw = pathways.ALL[name]
        for k in pathways.need(pw, 'lessons'):
            paths.append(str(Path(a.pack) / pathways.need(pw, 'pack', k)) if a.pack
                         else pathways.need(pw, 'live', k))
    sys.exit(1 if report(paths, a.verbose) else 0)


# ---------------------------------------------------------------------------
# LW1 §A2 · the FIX, driven by the same property as the census.
#
# Three families of dated pupil text turned up in GROW and LAUNCH that BUILD did
# not have: the <title>, the exit-slip headers, and an organiser header spaced
# "Week 8 | w/c 19 October 2026 | Made by Matt". My organiser pattern missed that
# last one because it allowed no 'w/c' between the pipe and the date -- the same
# blind spot that had already cost me the B3 check and the print-identity date
# regex, now for the third time.
#
# So the fix does not get a fourth bespoke pattern. It uses the census's OWN
# matchers: every text node and spoken attribute the census calls pupil-facing
# has its week tokens and dates removed, together with the separator that
# orphaned them. Any family I have not thought of is covered by construction,
# and the census re-run is the proof.
SEP = r'(?:\s*[·|,–—-]\s*|\s+)'


def _scrub(value):
    """Remove week tokens and dates from one string, taking the separator that
    binds them with it, and leave the rest exactly as it was."""
    out = value
    for rx in (DATE, WEEK):
        # token plus a LEADING separator, else token plus a TRAILING one
        out = re.sub(SEP + rx.pattern, '', out, flags=re.I)
        out = re.sub(rx.pattern + SEP, '', out, flags=re.I)
        out = rx.sub('', out)
    out = re.sub(r'(' + SEP + r')\1+', r'\1', out)          # collapse doubles
    out = re.sub(r'^\s*[·|,–—-]\s*', '', out)  # orphaned lead
    out = re.sub(r'\s*[·|,–—-]\s*$', '', out)  # orphaned tail
    return out


def scrub_text(text):
    """Scrub every pupil-facing surface. Returns (text, edits, before, after)
    with before/after taken from the census itself, so the fix reports the same
    numbers the gate does."""
    rows, _ = scan_text(text)
    before = sum(1 for r in rows if not r['staff'])
    edits, seen = 0, set()
    for r in rows:
        if r['staff'] or r['raw'] in seen:
            continue
        raw = r['raw']
        cleaned = _scrub(raw)
        if cleaned == raw:
            continue
        seen.add(raw)
        # lxml gives back the ENTITY-DECODED value; the file holds the encoded
        # bytes. Try the decoded form first, then the escaped form, and count
        # every replacement so a node that could not be located is visible as a
        # shortfall rather than as silence.
        for form_in, form_out in ((raw, cleaned),
                                  (escape(raw, quote=True), escape(cleaned, quote=True)),
                                  (escape(raw, quote=False), escape(cleaned, quote=False))):
            n = text.count(form_in)
            if n:
                text = text.replace(form_in, form_out)
                edits += n
                break
    rows2, _ = scan_text(text)
    after = sum(1 for r in rows2 if not r['staff'])
    return text, edits, before, after
