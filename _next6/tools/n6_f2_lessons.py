#!/usr/bin/env python3
"""N6-F §F2 — distil each of the 192 lesson files to the fields a verdict needs.

11MB of lesson HTML cannot be read whole 37 times over, and most of it is
chassis: styles, slide furniture, print CSS, the interaction layer. What a
verdict actually turns on is the lesson's title, its week label, its learning
objective, its success criteria and whatever it says about its own strand and
provenance. Those are pulled here, once, so a judgement cites the same text a
re-derivation would.

Nothing is inferred: every field is either present in the file or empty. A
verdict that needs more can still read the file.
"""
import json, os, re, sys, html as H

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')


def text(s):
    return WS.sub(' ', H.unescape(TAG.sub(' ', s))).strip()


def after(s, label, span=700):
    """Visible text following a label, label excluded.

    The label is matched with an optional trailing colon and any markup that
    closes the label element, because the three chassis in this estate write it
    three ways: `Learning objective:` inline, `<b>🎯 Learning objective</b><p>`,
    and `objective:` inside a heading.
    """
    m = re.search(re.escape(label.rstrip(':')) + r'\s*:?', s, re.I)
    if not m:
        return ''
    seg = s[m.end():m.end() + span]
    seg = re.sub(r'^(?:</[^>]+>|<(?:p|div|span|b|strong)[^>]*>|\s)+', '', seg)
    return text(seg)


def bullets(s, label, span=1400, cap=8):
    m = re.search(re.escape(label.rstrip(':')) + r'\s*:?', s, re.I)
    if not m:
        return []
    seg = s[m.end():m.end() + span]
    out = []
    for li in re.findall(r'<li[^>]*>(.*?)</li>', seg, re.S | re.I):
        t = text(li)
        if t:
            out.append(t)
        if len(out) >= cap:
            break
    if not out:
        t = text(seg)
        out = [x.strip() for x in re.split(r'(?<=[.;])\s+', t)[:cap] if x.strip()]
    return out


def record(p):
    s = open(p, encoding='utf-8', errors='ignore').read()
    title = ''
    m = re.search(r'<title[^>]*>(.*?)</title>', s, re.S | re.I)
    if m:
        title = text(m.group(1))
    h1 = ''
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S | re.I)
    if m:
        h1 = text(m.group(1))
    lo = after(s, 'Learning objective', 400)
    if not lo:
        lo = after(s, 'Lesson objective', 400)
    if not lo:
        lo = after(s, 'Objective', 400)
    sc = bullets(s, 'Success criteria')
    if not sc:
        sc = bullets(s, 'I can')
    # provenance the pack states about itself
    prov = {}
    for lbl in ('Estate sequence:', 'Exact SOW outcome:', 'Source:',
                'SOW outcome:', 'Curriculum link', 'Strand:'):
        v = after(s, lbl, 260)
        if v:
            prov[lbl.rstrip(':')] = v
    cells = sorted(set(re.findall(r"'[^']*Weekly - (?:Autumn|Spring|Summer)'![A-Z]+\d+", s)))
    strand = sorted(set(re.findall(r'data-strand="([^"]+)"', s)))
    wk = sorted(set(re.findall(r'\b(?:W|Week\s*)(\d{1,2})\b', os.path.basename(p))))
    # A lesson states what a pupil will learn. A support surface — START_HERE,
    # a staff guide, a practicals matrix, an evidence window, an index — does
    # not, and the SoW has nothing to say about one. Recording that distinction
    # keeps the matrix honest: 192 files is not 192 lessons, and a support
    # surface counted as SOW-SILENT alongside a genuinely silent lesson would
    # hide both.
    kind = 'lesson' if (lo or sc) else 'support'
    return {
        'file': p, 'name': os.path.basename(p), 'surface': kind,
        'title': title[:220], 'h1': h1[:220],
        'learning_objective': lo[:400],
        'success_criteria': sc[:8],
        'provenance': prov, 'sow_cells': cells,
        'strand_attr': strand, 'week_in_filename': wk,
        'bytes': os.path.getsize(p),
    }


if __name__ == '__main__':
    work = json.load(open('_next6/sow/worklist.json'))
    out = {}
    nlo = nsc = 0
    for g in work:
        for f in g['files']:
            r = record(f)
            out[f] = r
            nlo += bool(r['learning_objective'])
            nsc += bool(r['success_criteria'])
    json.dump(out, open('_next6/sow/lessons.json', 'w'), indent=1)
    # a per-group compact file so an agent reads only its own six
    os.makedirs('_next6/sow/groups', exist_ok=True)
    for i, g in enumerate(work):
        slug = '%02d_%s' % (i + 1, g['pack'].replace('/', '__'))
        json.dump({'group': g['group'], 'pack': g['pack'], 'lane': g['lane'],
                   'term': g['term'], 'packweeks': g['packweeks'],
                   'slice': g['slice'],
                   'lessons': [out[f] for f in g['files']]},
                  open('_next6/sow/groups/%s.json' % slug, 'w'), indent=1)
        g['groupfile'] = '_next6/sow/groups/%s.json' % slug
        g['label'] = slug
    json.dump(work, open('_next6/sow/worklist.json', 'w'), indent=1)
    nles = sum(1 for v in out.values() if v['surface'] == 'lesson')
    print('%d files distilled · %d lesson surfaces · %d support surfaces'
          % (len(out), nles, len(out) - nles))
    print('learning objective found in %d · success criteria in %d' % (nlo, nsc))
    print('support surfaces:')
    for k, v in sorted(out.items()):
        if v['surface'] == 'support':
            print('   ', k)
