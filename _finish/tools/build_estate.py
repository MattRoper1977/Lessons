"""Phase A + B — repair the BUILD estate pack and lay it into the repository.

    python3 _finish/tools/build_estate.py <extracted-zip-root> <install-root>

Every edit asserts its anchor before touching anything. A silent no-op is the
failure mode that produced most of the defects this programme has chased.

Safety wording is NEVER authored. A2's nail-sweep text is read out of the live
files at run time and transplanted verbatim; if it cannot be located the run
stops rather than reconstructing it.
"""
import sys, os, re, json, shutil, hashlib

SRC, OUT = sys.argv[1], sys.argv[2]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LIVE_DT_W1 = os.path.join(REPO, 'Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html')
LIVE_DT_W3 = os.path.join(REPO, 'Build/Slideshows/BUILD_DT_W3_Core_Cut.html')
LOG, AMBER = [], []


class NoAnchor(Exception):
    pass


def note(kind, f, msg):
    LOG.append((kind, f, msg))


def sub1(t, old, new, f, what, count=1):
    n = t.count(old)
    if n != count:
        raise NoAnchor(f'{f}: {what}: expected {count} of {old[:80]!r}, found {n}')
    return t.replace(old, new)


# ============================================================ A2 · read the live wording

def live_nail_sweep():
    """Locate the four expected sites on the live files and return their wording.
    Never reconstructs: a missing site is returned as None and reported."""
    w1 = open(LIVE_DT_W1, encoding='utf-8').read()
    w3 = open(LIVE_DT_W3, encoding='utf-8').read()
    out = {}

    m = re.search(r'<h3>(Then sweep it for what you cannot see\.)</h3><p>(.*?)</p>', w1, re.S)
    out['w1_slide'] = (m.group(1), m.group(2)) if m else None

    m = re.search(r'<td[^>]*><strong>(NAIL SWEEP)</strong></td><td[^>]*>(.*?)</td>', w1, re.S)
    out['w1_ko'] = (m.group(1), m.group(2)) if m else None

    m = re.search(r'(&#9744; Swept the board with the magnet)', w1)
    out['w1_tick'] = m.group(1) if m else None

    m = re.search(r'<strong>(Magnet-sweep the board\.)</strong>', w3)
    out['w3_step'] = m.group(1) if m else None

    m = re.search(r'<strong>Stop and ask if:</strong> (the magnet finds metal)', w3)
    out['w3_stop'] = m.group(1) if m else None
    return out


NS = live_nail_sweep()
missing = [k for k, v in NS.items() if not v]
if missing:
    raise SystemExit(f'A2 STOP: could not locate live wording for {missing}. '
                     'Safety wording is not reconstructed. Nothing was written.')


# ============================================================ per-file transforms

def transform_dt_w1(t, f):
    """Sites 1 and 2. Words verbatim from live; only the container is adapted —
    a drawer-card beside the safety controls, because the v3 chassis has no slide
    deck section for this and no knowledge organiser."""
    head, body = NS['w1_slide']
    term, defn = NS['w1_ko']
    anchor = ('<div class="drawer-card"><b>Reclaimed timber</b><p>The repo safety gate says an '
              'HT stamp is only one check and is not sufficient by itself. Material acceptance '
              'is staff/technician/local-approval territory, not a pupil decision.</p></div>')
    card = (f'<div class="drawer-card"><b>{head}</b><p>{body}</p>'
            f'<p><b>{term}</b> — {defn}</p></div>')
    t = sub1(t, anchor, anchor + card, f, 'A2 site 1+2 (W1 safety drawer)')
    note('A2', f, 'nail-sweep wording + NAIL SWEEP definition, verbatim, in the safety drawer')

    # site 2 also on paper: the print pack's Supported scaffold already carries definitions
    defs = ('Hazard = something that could cause harm. Control = what reduces the risk. '
            'STOP = outside today’s approved setup.')
    if defs in t:
        t = t.replace(defs, defs + f' {term} = {defn}.')
        note('A2', f, 'NAIL SWEEP definition added to the print scaffold definitions line')
    else:
        AMBER.append(f'{f}: print definitions line not found; NAIL SWEEP is screen-only here')
    return t


def transform_dt_w3(t, f):
    """Site 4. The v3 chassis has no numbered cutting sequence; its equivalent is the
    I Do decision chain and the STOP-point list. Words verbatim, arrows are container."""
    step = NS['w3_step'].rstrip('.')
    chain = ('Model the decision points: material/component approved → mark checked → '
             'setup secured → adult authorises processing → stop if setup changes.')
    new = ('Model the decision points: material/component approved → mark checked → '
           f'{step} → setup secured → adult authorises processing → stop if setup changes.')
    t = sub1(t, chain, new, f, 'A2 site 4 (W3 decision chain)')
    note('A2', f, f'"{step}" inserted verbatim into the W3 decision chain')

    stop = ('STOP points stay visible: setup changed · component loose · unsure · '
            'adult instruction changes.')
    n = t.count(stop)
    if n == 0:
        raise NoAnchor(f'{f}: A2 STOP-point list not found')
    t = t.replace(stop, 'STOP points stay visible: ' + NS['w3_stop'] +
                  ' · setup changed · component loose · unsure · adult instruction changes.')
    note('A2', f, f'"{NS["w3_stop"]}" added verbatim to the STOP-point list (x{n}, screen + print)')
    return t


ASDAN_HUB_LINE = ('This route does not produce ASDAN assessment records. Portfolio evidence for '
                  'accreditation comes from the existing BUILD_ASDAN lessons.')

BANNER = ('Alternative BUILD route, Autumn 1. The existing lessons remain available in the '
          'Lessons catalogue.')


def banner_html(extra=''):
    return ('<div class="v3banner" style="background:#10233f;color:#fff;border-radius:12px;'
            'padding:11px 14px;margin:10px 0;font-weight:700">' + BANNER + extra + '</div>')


def transform_hub(t, f, subject):
    m = re.search(r'<body[^>]*>', t)
    if not m:
        raise NoAnchor(f'{f}: no <body>')
    extra = ''
    if subject == 'BUILD_ASDAN':
        extra = ('<br><span style="font-weight:600">' + ASDAN_HUB_LINE + '</span>')
    t = t[:m.end()] + banner_html(extra) + t[m.end():]
    note('B', f, 'route banner' + (' + ASDAN assessment-record line (A1)' if extra else ''))
    return t


def transform_estate_hub(t, f):
    m = re.search(r'<body[^>]*>', t)
    t = t[:m.end()] + banner_html() + t[m.end():]
    # §0.8 / A-i — the Science link must point at where those lessons actually live
    old = 'href="Science/START_HERE_BUILD_SCIENCE_OUTSTANDING_V3.html"'
    new = 'href="../Science_Teesside/Build/v3_40min/index.html"'
    t = sub1(t, old, new, f, 'B re-point Science link')
    note('B', f, 'Science link re-pointed to Science_Teesside/Build/v3_40min/ (folder skipped)')
    return t


# ============================================================ names

def newname(name):
    return re.sub(r'_OUTSTANDING_V3_TEST(?=\.html$)', '',
                  re.sub(r'_OUTSTANDING_V3(?=\.html$)', '', name))


HUBNAME = {'Art_Teesside': 'START_HERE_BUILD_ART_TEESSIDE_OUTSTANDING_V3.html',
           'BUILD_ASDAN': 'START_HERE_BUILD_ASDAN_OUTSTANDING_V3.html',
           'DT_Community_Upcycling': 'START_HERE_BUILD_DT_COMMUNITY_UPCYCLING_OUTSTANDING_V3.html',
           'Humanities_Teesside': 'START_HERE_BUILD_HUMANITIES_TEESSIDE_OUTSTANDING_V3.html'}


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    docs = os.path.join(REPO, '_finish', 'build_estate')
    os.makedirs(docs, exist_ok=True)

    rename = {}
    for root, _, files in os.walk(SRC):
        for n in files:
            if n.endswith('.html'):
                rename[n] = newname(n)
    rename['START_HERE_BUILD_ESTATE_OUTSTANDING_V3.html'] = 'index.html'
    for s, h in HUBNAME.items():
        rename[h] = 'index.html'

    for root, dirs, files in os.walk(SRC):
        rel = os.path.relpath(root, SRC)
        subject = rel.split(os.sep)[0] if rel != '.' else None
        dst = OUT if rel == '.' else os.path.join(OUT, rel)
        os.makedirs(dst, exist_ok=True)
        for n in sorted(files):
            p = os.path.join(root, n)
            if n.endswith('.md'):
                shutil.copy2(p, os.path.join(docs, (subject + '__' if subject else '') + n))
                continue
            if not n.endswith(('.html', '.json')):
                shutil.copy2(p, os.path.join(dst, n))
                continue
            t = open(p, encoding='utf-8').read()

            if n.endswith('.json'):
                for a, b in rename.items():
                    t = t.replace(a, b)
                open(os.path.join(dst, n), 'w', encoding='utf-8').write(t)
                continue

            # A2
            if subject == 'DT_Community_Upcycling' and '_W1_' in n:
                t = transform_dt_w1(t, n)
            if subject == 'DT_Community_Upcycling' and '_W3_' in n:
                t = transform_dt_w3(t, n)

            # hubs
            if n == 'START_HERE_BUILD_ESTATE_OUTSTANDING_V3.html':
                t = transform_estate_hub(t, n)
            elif subject and n == HUBNAME.get(subject):
                t = transform_hub(t, n, subject)

            # hrefs for the new names — bare AND directory-prefixed. The estate hub
            # links subject hubs as href="Art_Teesside/START_HERE_...", so an
            # exact-match replace on the bare filename silently misses all four.
            for a, b in rename.items():
                t = t.replace(f'href="{a}"', f'href="{b}"')
                t = re.sub(r'href="([^"]*/)' + re.escape(a) + r'"',
                           lambda m: f'href="{m.group(1)}{b}"', t)
            # .md records moved out of the pupil-facing tree
            t = re.sub(r'href="([A-Z_0-9]+\.md)"',
                       lambda m: 'href="%s../../_finish/build_estate/%s%s"' % (
                           '', (subject + '__') if subject else '', m.group(1)), t)

            t = re.sub(r'<!--\s*TEST BUILD\.', '<!-- Made by Matt · BUILD estate v3 route.', t)
            t = t.replace('No repository write.',
                          'Installed as a parallel route; the live lesson is unchanged.')
            open(os.path.join(dst, rename.get(n, n)), 'w', encoding='utf-8').write(t)

    for k, f, m in LOG:
        print(f'  {k:4s} {f[:56]:56s} {m}')
    print(f'\n{len(LOG)} edits')
    for a in AMBER:
        print('  AMBER:', a)
    print('\nA2 sites located on live main:')
    for k, v in NS.items():
        print(f'   {k:9s} {"FOUND" if v else "MISSING"}')


if __name__ == '__main__':
    main()
