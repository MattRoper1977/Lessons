#!/usr/bin/env python3
"""
semantic_integrity_check.py — LL-INST-14

Asserts that a lesson's surfaces agree WITH EACH OTHER.

The estate already has instruments that prove a lesson *works*: selectors resolve,
scripts parse, print packs populate. None of them can see a lesson that works
perfectly while teaching the wrong message. This one reads meaning.

Its founding case (2026-08-04): all six BUILD_DT decks passed every technical gate
while their mid-point peer-check quoted CAREERS_W1_My_Strengths' success criteria,
their completion summary ticked a Careers criterion, and their next-lesson pointer
sent pupils to CAREERS_W2. Every selector resolved. Every script parsed.

WHAT THIS INSTRUMENT CANNOT DETECT
  - Whether the lesson's own outcomes are pedagogically *right* — only that the
    surfaces quoting them agree with each other. A deck consistently teaching the
    wrong thing passes.
  - Prose that paraphrases another lesson without quoting it verbatim.
  - Anything requiring layout or a real browser. Print geometry is not measured here;
    that needs 718x1047 in a browser-capable environment (see rule 26).
  - Whether a *correct-looking* next-lesson pointer names a lesson that exists.

DESIGN RULE IT OBEYS
  Never keep two copies where one can be derived. Every expectation is read out of the
  file under test. There is no table of expected titles in this script, and there must
  never be one — such a table is a second copy and will go stale silently.

USAGE
  python3 LundyLoop/tools/semantic_integrity_check.py                  # estate-wide report
  python3 LundyLoop/tools/semantic_integrity_check.py <path> [<path>]  # named files
  python3 LundyLoop/tools/semantic_integrity_check.py --json           # machine-readable

EXIT CODES
  0 = no findings at or above 'high'   1 = findings   2 = instrument error
"""

import re, sys, json, pathlib, collections

# ---------------------------------------------------------------- instrument rules

DATA_URI = re.compile(r'data:[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=\s]{40,}')

def strip_data_uris(text):
    """Rule: strip data-URIs before ANY text measurement. 200 tracked *.html files
    carry base64 blobs at 6aaffb7; every count inflates otherwise."""
    return DATA_URI.sub('data:STRIPPED', text)

def tag_text(html):
    return re.sub(r'<[^>]+>', ' ', html)

SEVERITY_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}

# ---------------------------------------------------------------- derivation helpers
# Each returns a value read OUT OF THE FILE. None means "this file does not have that
# surface", which is never itself a finding — absence is a convention in this estate
# (the I Do slide has no print counterpart, deliberately).

def derive_banner(t):
    m = re.search(r'class="slide-tag tag-lesson"[^>]*>([^<]+)', t)
    return m.group(1).strip() if m else None

def derive_week(banner):
    if not banner: return None
    m = re.search(r'\bWeek\s+(\d+)\s+of\s+(\d+)', banner)
    return (int(m.group(1)), int(m.group(2))) if m else None

def derive_subject(banner):
    if not banner: return None
    m = re.match(r'\s*([A-Z&;a-mp-z]+(?:\s+[A-Z&;]+)?)\s*·', banner.replace('&amp;', '&'))
    return m.group(1).strip() if m else banner.split('·')[0].strip()

def derive_title(t):
    m = re.search(r'<h1[^>]*>([^<]{3,140})</h1>', t)
    return m.group(1).strip() if m else None

QUOTING_REGIONS = ('mp-prompt', 'lc-summary')

def derive_own_outcomes(t):
    """The deck's own 'I can ...' statements — the ground truth other surfaces quote.

    CRITICAL: the quoting regions are EXCLUDED from the ground truth. Deriving the
    outcome set from the whole file makes the check self-referential — a criterion
    pasted into the midpoint modal becomes part of its own evidence and the check
    silently never fires. That false negative was caught by replaying this instrument
    against a file whose defect was already proven (2026-08-04, BUILD_DT_W2).
    """
    body = t
    for cls in QUOTING_REGIONS:
        body = re.sub(r'<div class="%s">.*?</div>' % re.escape(cls), ' ', body, flags=re.S)
    # Extract from RAW html, not tag-stripped text: '<' is what delimits a criterion.
    # Stripping tags first removes that boundary and adjacent criteria run together,
    # so no quoted string ever matches the ground truth and the check silently passes.
    return set(m.strip() for m in re.findall(r'I can [^<.]{5,110}', body))

def derive_region(t, cls):
    m = re.search(r'<div class="%s">(.*?)</div>' % re.escape(cls), t, re.S)
    return m.group(0) if m else None

def derive_timer_contract(t):
    disp = re.search(r'id="timerDisplay"[^>]*>\s*([0-9]{1,2}):([0-9]{2})', t)
    tot  = re.search(r'timerTotal\s*=\s*(\d+)', t)
    left = re.search(r'timerLeft\s*=\s*(\d+)', t)
    ind  = re.search(r'data-title="Independent Work"[^>]*data-timer="(\d+)"', t) or \
           re.search(r'data-timer="(\d+)"[^>]*data-title="Independent Work"', t)
    if not (disp and tot): return None
    return {
        'display_s': int(disp.group(1)) * 60 + int(disp.group(2)),
        'total_s':   int(tot.group(1)),
        'left_s':    int(left.group(1)) if left else None,
        'indep_min': int(ind.group(1)) if ind else None,
    }

def derive_print_ids(t):
    return set(re.findall(r'id="(print-[a-z-]+)"', t))

_TITLE_INDEX = None

def _title_index():
    """Map deck title -> set of folders carrying it, derived from the corpus at runtime.

    This is a derivation, not a parallel list: it is recomputed from the files every
    run, so it cannot go stale the way a hand-written table of expected titles would.
    """
    global _TITLE_INDEX
    if _TITLE_INDEX is not None:
        return _TITLE_INDEX
    idx = collections.defaultdict(set)
    for p in corpus():
        try:
            txt = strip_data_uris(p.read_text(encoding='utf-8', errors='replace'))
        except Exception:
            continue
        if not derive_banner(txt):
            continue
        ttl = derive_title(txt)
        if ttl and len(ttl) >= 6:
            idx[ttl].add(p.parent.as_posix())
    _TITLE_INDEX = dict(idx)
    return _TITLE_INDEX

# ---------------------------------------------------------------- checks

def check_file(path):
    raw = pathlib.Path(path).read_text(encoding='utf-8', errors='replace')
    t = strip_data_uris(raw)
    F, add = [], None
    def add(cid, sev, msg, ev=''):
        F.append({'check': cid, 'severity': sev, 'file': str(path),
                  'message': msg, 'evidence': ev[:300]})

    banner   = derive_banner(t)
    week     = derive_week(banner)
    title    = derive_title(t)
    outcomes = derive_own_outcomes(t)
    mid      = derive_region(t, 'mp-prompt')
    lc       = derive_region(t, 'lc-summary')

    if banner is None:
        return F   # not a lesson deck; nothing to assert

    # SI-04 outcome ownership — the founding case.
    for region_name, region, cid in (('midpoint peer-check', mid, 'SI-04'),
                                     ('completion summary', lc, 'SI-05')):
        if not region: continue
        for quoted in re.findall(r'I can [^<.]{5,110}', region):
            q = quoted.strip()
            if q and q not in outcomes:
                add(cid, 'critical',
                    f"{region_name} quotes a success criterion this deck does not own",
                    q)

    # SI-02 week consistency. A multi-week artefact legitimately names several weeks in
    # a sentence about its own lifespan; that is not staleness.
    if week:
        n, of = week
        for m in re.finditer(r'Week\s+(\d+)\s+of\s+(\d+)', tag_text(t)):
            if (int(m.group(1)), int(m.group(2))) != week:
                add('SI-02', 'high', f"a 'Week X of Y' surface disagrees with the banner "
                    f"(banner says {n} of {of})", m.group(0))

    # SI-03 title consistency between the deck title and its knowledge organiser.
    ko = re.search(r'<h1[^>]*>\s*Knowledge Organiser\s*[—-]\s*([^<]+)</h1>', t)
    if ko and title and ko.group(1).strip() != title:
        add('SI-03', 'high', "knowledge-organiser title disagrees with the deck title",
            f"{title!r} vs {ko.group(1).strip()!r}")

    # SI-06 next-lesson pointer must not name a lesson from another subject family.
    # Derived from the corpus at runtime (title -> folders), never from a parallel list.
    nxt = re.search(r'Next lesson:\s*([^<\n]{3,120})', tag_text(t))
    if nxt:
        pointer = nxt.group(1).strip()
        titles = _title_index()
        here = pathlib.Path(path).parent.as_posix()
        for known_title, folders in titles.items():
            if known_title and known_title.lower() in pointer.lower():
                if here not in folders:
                    add('SI-06', 'critical',
                        "next-lesson pointer names a lesson that lives in a different "
                        "module folder — pupils are sent to another subject's lesson",
                        f"pointer={pointer!r} -> {known_title!r} in {sorted(folders)}")
                break

    # SI-07 timer contract. REPORT ONLY — see below.
    tc = derive_timer_contract(t)
    if tc:
        if tc['display_s'] != tc['total_s']:
            add('SI-07', 'critical',
                "two authored copies of one timer fact disagree: the initial display and "
                "the configured total. REPORT ONLY — estate timer values are Matt's call "
                "(HANDOVER.md 'The human's open calls'); authorisation "
                "'Fix the timer contract — go' is awaited.",
                f"display={tc['display_s']}s configured={tc['total_s']}s")
        if tc['indep_min'] is not None and tc['indep_min'] * 60 != tc['total_s']:
            add('SI-07', 'high',
                "Independent Work data-timer disagrees with the configured total. "
                "REPORT ONLY, as above.",
                f"data-timer={tc['indep_min']}min configured={tc['total_s']}s")
        if tc['left_s'] is not None and tc['left_s'] != tc['total_s']:
            add('SI-07', 'high', "timerLeft and timerTotal disagree at declaration",
                f"left={tc['left_s']} total={tc['total_s']}")

    # SI-09 tier vocabulary.
    body = tag_text(t)
    for bad in ('Foundation/Middle/Higher',):
        if bad in body:
            add('SI-09', 'medium', "non-house tier vocabulary on a pathway deck", bad)

    return F

# ---------------------------------------------------------------- corpus

def corpus():
    """Null-safe iteration. Filenames in this estate contain apostrophes AND spaces."""
    root = pathlib.Path('.')
    skip = {'.git', 'node_modules', '_semh_audit'}
    for p in sorted(root.rglob('*.html')):
        if any(s in p.parts for s in skip): continue
        yield p

def main(argv):
    args = [a for a in argv[1:] if not a.startswith('--')]
    as_json = '--json' in argv
    files = [pathlib.Path(a) for a in args] if args else list(corpus())

    findings, scanned, decks = [], 0, 0
    for p in files:
        try:
            f = check_file(p)
        except Exception as e:
            print(f"INSTRUMENT ERROR on {p}: {e}", file=sys.stderr); return 2
        scanned += 1
        if derive_banner(strip_data_uris(p.read_text(encoding='utf-8', errors='replace'))):
            decks += 1
        findings.extend(f)

    findings.sort(key=lambda x: SEVERITY_ORDER.get(x['severity'], 9))

    if as_json:
        print(json.dumps({'scanned_files': scanned, 'lesson_decks': decks,
                          'findings': findings}, indent=2));
    else:
        by = collections.Counter(f['severity'] for f in findings)
        bycheck = collections.Counter(f['check'] for f in findings)
        print(f"semantic_integrity_check — scanned {scanned} files "
              f"(unit: files; universe: tracked *.html excluding .git/_semh_audit)")
        print(f"lesson decks recognised (carry a lesson banner): {decks}")
        print(f"findings: {len(findings)}  " +
              " ".join(f"{k}={v}" for k, v in sorted(by.items())))
        print("by check: " + (" ".join(f"{k}={v}" for k, v in sorted(bycheck.items()))
                              or "none"))
        # Rule 25: a census returning non-zero must print its hits, not merely count them.
        for f in findings:
            print(f"  [{f['severity']:8}] {f['check']} {f['file']}")
            print(f"             {f['message']}")
            if f['evidence']: print(f"             evidence: {f['evidence']}")
        if not findings:
            print("\nZERO findings. Rule 16: a zero is only believed after replay against "
                  "an input where the detector MUST fire. Replay with:\n"
                  "  git stash && git checkout <a commit with a known defect> -- <file>")
    return 1 if any(SEVERITY_ORDER.get(f['severity'], 9) <= 1 for f in findings) else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
