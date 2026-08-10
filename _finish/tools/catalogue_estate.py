"""Phase C — catalogue the BUILD estate v3 route. Existing chips only.

    python3 _finish/tools/catalogue_estate.py
"""
import sys, os, re, json, glob

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ROOT = os.path.join(REPO, 'BUILD_Estate_v3')
RES = os.path.join(REPO, 'resources.json')
TODAY, YEAR = '2026-08-10', '2026-27'
PRINT_REPAIR = '.proute{display:block}body[data-tier] .proute{display:none}'

# Existing chips, derived from the live counterparts. No new subject is minted.
SUBJECT = {'Art_Teesside': 'Art · Teesside Studio Suite',
           'BUILD_ASDAN': 'BUILD Vocational & PfA',
           'DT_Community_Upcycling': 'BUILD Vocational & PfA',
           'Humanities_Teesside': 'Humanities'}
LABEL = {'Art_Teesside': 'Art', 'BUILD_ASDAN': 'ASDAN',
         'DT_Community_Upcycling': 'D&T', 'Humanities_Teesside': 'Humanities'}
FAMILY = 'BUILD Estate v3'

STOP = set('the a an and or of to in on with for is are can i my your what which how why when '
           'who not do does using use it its this that from into at by as be them they their '
           'we you one two three then than so if but about more most build outstanding'.split())


def read(f):
    return open(f, encoding='utf-8').read()


def kw(*bits):
    out = []
    for b in bits:
        for w in re.findall(r"[A-Za-z][A-Za-z'’-]+|\d+", str(b).lower()):
            if w in STOP or len(w) < 3 or w in out:
                continue
            out.append(w)
    return out[:9]


def title_of(t, fallback):
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    s = re.sub(r'\s+', ' ', m.group(1)).strip() if m else fallback
    s = re.sub(r'\s*·?\s*Outstanding v3.*$', '', s, flags=re.I)
    # The <title> already repeats "BUILD <subject> · W<n> ·". Strip it so the
    # catalogue entry does not read "BUILD · Art · W1 · BUILD Art W1 · …".
    s = re.sub(r'^BUILD\s+(ASDAN|Art|D&amp;T|D&T|Humanities)[^·]*·\s*', '', s, flags=re.I)
    s = re.sub(r'^[^·]{0,28}·\s*W\d+[^·]*·\s*', '', s)
    s = re.sub(r'^W\d+\s*·\s*', '', s)
    return s.strip(' ·')


def desc_of(t):
    m = re.search(r'<b>Learning objective:</b>\s*(.*?)</p>', t, re.S)
    if not m:
        m = re.search(r'(?i)learning objective[:<][^<]*<[^>]*>\s*(.*?)</', t, re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else None


def week_of(name):
    m = re.search(r'_(W\d+(?:-W\d+)?)[_.]', name)
    return m.group(1) if m else None


def main():
    res = json.load(open(RES, encoding='utf-8'))
    base = len(res)
    have = {e['id'] for e in res}
    add = []

    for sub, chip in SUBJECT.items():
        d = os.path.join(ROOT, sub)
        for f in sorted(glob.glob(os.path.join(d, '**', '*.html'), recursive=True)):
            t = read(f)
            if PRINT_REPAIR not in t:
                continue                      # not a route-bearing lesson
            name = os.path.basename(f)
            rel = os.path.relpath(f, REPO)
            w = week_of(name)
            short = title_of(t, name)
            rid = 'bev3-' + re.sub(r'[^a-z0-9]+', '-',
                                   os.path.splitext(rel[len('BUILD_Estate_v3/'):])[0].lower()
                                   ).strip('-')
            desc = desc_of(t) or short
            add.append({
                'subject': chip,
                'title': f'BUILD · {LABEL[sub]} · {w + " · " if w else ""}{short} (v3 route)',
                'file': rel,
                'id': rid,
                'type': 'lesson',
                'family': FAMILY,
                'keywords': kw('build', LABEL[sub], 'v3 route', w, short),
                'desc': desc,
                'added': TODAY, 'new': True, 'year': YEAR,
            })

    # hubs — type derived from the existing START_HERE / index hub entries
    add.append({
        'subject': 'BUILD Vocational & PfA',
        'title': 'BUILD Estate v3 route · start here',
        'file': 'BUILD_Estate_v3/index.html',
        'id': 'bev3-estate-hub', 'type': 'teacher', 'family': FAMILY,
        'keywords': kw('build', 'estate', 'v3 route', 'start here', 'autumn 1'),
        'desc': ('Alternative BUILD route for Autumn 1 across Art, ASDAN, D&T and Humanities. '
                 'The existing lessons remain available in the Lessons catalogue.'),
        'added': TODAY, 'new': True, 'year': YEAR})
    for sub, chip in SUBJECT.items():
        add.append({
            'subject': chip,
            'title': f'BUILD · {LABEL[sub]} · v3 route · start here',
            'file': f'BUILD_Estate_v3/{sub}/index.html',
            'id': f'bev3-{sub.lower().replace("_", "-")}-hub',
            'type': 'teacher', 'family': FAMILY,
            'keywords': kw('build', LABEL[sub], 'v3 route', 'start here'),
            'desc': (f'Alternative BUILD {LABEL[sub]} route, Autumn 1. The existing lessons '
                     'remain available in the Lessons catalogue.'),
            'added': TODAY, 'new': True, 'year': YEAR})

    dupes = [e['id'] for e in add if e['id'] in have]
    assert not dupes, f'duplicate ids: {dupes}'
    seen = set()
    for e in add:
        assert e['id'] not in seen, e['id']
        seen.add(e['id'])
        assert os.path.exists(os.path.join(REPO, e['file'])), 'missing: ' + e['file']
        assert e['desc'], 'no desc: ' + e['file']

    res.extend(add)
    json.dump(res, open(RES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(RES, 'a', encoding='utf-8').write('\n')

    from collections import Counter
    print(f'  entries {base} -> {len(res)}  (+{len(add)}: '
          f'{sum(1 for e in add if e["type"] == "lesson")} lessons + '
          f'{sum(1 for e in add if e["type"] == "teacher")} hubs)')
    print('  chips touched (existing only, none minted):')
    for c, n in Counter(e['subject'] for e in add).items():
        tot = sum(1 for e in res if e['subject'] == c)
        print(f'     {c:30s} +{n:3d}  -> {tot}')
    print('\n  sample:')
    for e in (add[0], add[8], add[-5], add[-1]):
        print('   ', json.dumps(e, ensure_ascii=False)[:180])


if __name__ == '__main__':
    main()
