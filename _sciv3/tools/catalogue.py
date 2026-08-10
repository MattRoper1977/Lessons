"""Phase C — 46 catalogue entries, matching the existing entries' shape exactly.

    python3 _sciv3/tools/catalogue.py
"""
import sys, os, re, json, glob

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TODAY = '2026-08-10'
YEAR = '2026-27'
RES = os.path.join(REPO, 'resources.json')

PACK = {'grow': ('Grow', 'GROW', 'g'), 'build': ('Build', 'BUILD', 'b'),
        'launch': ('Launch', 'LAUNCH', 'l')}

# route word shown in the title, per lesson key
STAGE = {'A': 'Explore', 'B': 'Do', 'L1': 'Introduce', 'L2': 'Explore', 'L3': 'Do'}

STOP = set('the a an and or of to in on with for is are can i my your what which how '
           'why when who not do does using use it its this that from into at by as be '
           'them they their we you one two three then than so if but about more most '
           'they’re own also each other same different'.split())


def lo_of(t):
    m = re.search(r'<b>Learning objective:</b>\s*(.*?)</p>', t, re.S)
    return re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else None


def topic_of(name):
    m = re.match(r'SCI_[GBL]_(W\d(?:[AB]|L\d))_(.+)\.html$', name)
    return m.group(1), m.group(2).replace('_', ' ')


def kw(*bits):
    out = []
    for b in bits:
        for w in re.findall(r"[A-Za-z][A-Za-z'’-]+|\d+", b.lower()):
            if w in STOP or len(w) < 3 or w in out:
                continue
            out.append(w)
    return out[:9]


def main():
    res = json.load(open(RES, encoding='utf-8'))
    before = len(res)
    have = {e['id'] for e in res}
    add = []

    for pack, (Cap, LAB, letter) in PACK.items():
        d = os.path.join(REPO, 'Science_Teesside', Cap, 'v3_40min')
        for f in sorted(glob.glob(os.path.join(d, 'SCI_*.html'))):
            name = os.path.basename(f)
            t = open(f, encoding='utf-8').read()
            key, topic = topic_of(name)
            stage = STAGE[key[2:] if pack == 'launch' else key[-1]]
            # topic already ends in the stage word; strip it for the title's topic half
            tclean = re.sub(r'\s*(Introduce|Explore|Do)$', '', topic)
            lo = lo_of(t)
            assert lo, f'{name}: no learning objective'
            add.append({
                'subject': 'Science · Teesside',
                'title': f'{LAB} · {key} · {tclean} {stage} (40-min route)',
                'file': os.path.relpath(f, REPO),
                'id': f'sci-tees-{letter}-{key.lower()}-v3',
                'type': 'lesson',
                'family': 'Science Teesside',
                'keywords': kw(LAB, 'science', '40-min route', key, tclean, stage),
                'desc': lo,
                'added': TODAY,
                'new': True,
                'year': YEAR,
            })
        add.append({
            'subject': 'Science · Teesside',
            'title': f'{LAB} · Science 40-min route · start here',
            'file': f'Science_Teesside/{Cap}/v3_40min/index.html',
            'id': f'sci-tees-{letter}-v3-hub',
            'type': 'teacher',   # derived from the existing START_HERE / index hub entries
            'family': 'Science Teesside',
            'keywords': kw(LAB, 'science', 'hub', '40-min route', 'start here', 'Aut 1'),
            'desc': (f'Alternative 40-minute route for {LAB} Science Aut 1 W3–W7. '
                     'The existing route remains available in the Lessons catalogue.'),
            'added': TODAY, 'new': True, 'year': YEAR,
        })

    # ---- Baseline Weeks: the one place a new subject chip is correct (§3.1)
    BASE = [
        ('index.html', 'Baseline Weeks · start here', 'baseline-weeks-hub', 'teacher',
         'Hub for the public First Two Weeks baseline pack: how to run it, what it is not, '
         'and how it differs from the baseline app.'),
        ('baseline-reading-writing-standard.html',
         'Reading & Writing Baseline · Pathway A · Standard Transitions',
         'baseline-reading-writing-a', 'pupil',
         'Reading comprehension, writing/communication and spelling/word knowledge — '
         'a starting point, not a score.'),
        ('baseline-reading-writing-specialist-semh.html',
         'Reading & Writing Baseline · Pathway B · Specialist / SEMH',
         'baseline-reading-writing-b', 'pupil',
         'Reading comprehension, writing/communication and spelling/word knowledge, '
         'shortened and split into 10–15 minute pieces.'),
        ('baseline-maths-standard.html', 'Maths Baseline · Pathway A · Standard Transitions',
         'baseline-maths-a', 'pupil',
         'Number sense & calculation, problem solving/reasoning and pattern/measure/data — '
         'a starting point, not a score.'),
        ('baseline-maths-specialist-semh.html',
         'Maths Baseline · Pathway B · Specialist / SEMH', 'baseline-maths-b', 'pupil',
         'Number sense & calculation, problem solving/reasoning and pattern/measure/data, '
         'shortened and split into 10–15 minute pieces.'),
        ('baseline-science-standard.html', 'Science Baseline · Pathway A · Standard Transitions',
         'baseline-science-a', 'pupil',
         'Observing & describing, scientific reasoning and practical enquiry/data — '
         'a starting point, not a score.'),
        ('baseline-science-specialist-semh.html',
         'Science Baseline · Pathway B · Specialist / SEMH', 'baseline-science-b', 'pupil',
         'Observing & describing, scientific reasoning and practical enquiry/data, '
         'shortened and split into 10–15 minute pieces.'),
        ('baseline-profile-review.html', 'Baseline Profile Review (staff sheet)',
         'baseline-profile-review', 'teacher',
         'Staff-facing sheet for turning baseline evidence into first teaching actions. '
         'Not a pupil surface.'),
    ]
    for fn, title, rid, typ, desc in BASE:
        add.append({
            'subject': 'Baseline',
            'title': title,
            'file': f'Baseline_Weeks/{fn}',
            'id': rid,
            'type': typ,
            'family': 'Baseline Weeks',
            'keywords': kw('baseline', 'first two weeks', 'starting point', title),
            'desc': desc,
            'added': TODAY, 'new': True, 'year': YEAR,
        })

    dupes = [e['id'] for e in add if e['id'] in have]
    assert not dupes, f'duplicate ids: {dupes}'
    seen = set()
    for e in add:
        assert e['id'] not in seen, e['id']
        seen.add(e['id'])
        assert os.path.exists(os.path.join(REPO, e['file'])), 'missing file: ' + e['file']

    res.extend(add)
    json.dump(res, open(RES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(RES, 'a', encoding='utf-8').write('\n')

    print(f'  entries {before} -> {len(res)}  (+{len(add)})')
    print(f'  Science · Teesside: '
          f'{sum(1 for e in res if e["subject"] == "Science · Teesside")}')
    print(f'  Baseline:           {sum(1 for e in res if e["subject"] == "Baseline")}')
    print('\n  sample entries:')
    for e in (add[0], add[10], add[21], add[-8], add[-1]):
        print('   ', json.dumps(e, ensure_ascii=False)[:190])


if __name__ == '__main__':
    main()
