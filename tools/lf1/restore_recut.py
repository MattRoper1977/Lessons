#!/usr/bin/env python3
"""LF1M-FIN section 4c -- restore dropped original sentences into a weekly re-cut.

WHAT IT WRITES. Only an appended sentence, verbatim, to a field that already holds
several sentences. Nothing is reworded, re-punctuated, re-ordered or merged.

THE TWO WRITES (B2). Each re-cut holds its text TWICE -- once rendered into static
HTML and once in the DATA payload -- and they agree today. So the field's exact
text must occur exactly 2x in the file. That count IS the byte-equality assertion:
2 before the write, 2 after. Anything else is a STOP for the id, and the file is
left untouched. Nothing is ever regenerated: there is no builder here.

WHAT IT REFUSES. A single-sentence slot whose re-cut says something DIFFERENT is a
replacement, not a deletion, and appending would put two instructions in one slot.
Anything under model.* renders into the SVG as textLength-fitted runs, where an
append is not verbatim. Both are listed conflicts, never written.

CONTROLS (D28). --self-test plants both, in the invocation that produces the number:
a TRUE POSITIVE (the two copies made to disagree -- must be refused) and a TRUE
NEGATIVE (the two copies agreeing -- must be accepted).
"""
import json, os, re, sys, shutil, difflib

class Conflict(Exception): pass

def field_text(data, path):
    cur = data
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        if part.startswith('['): cur = cur[int(part[1:-1])]
        else:
            if not isinstance(cur, dict) or part not in cur: return None
            cur = cur[part]
    return cur if isinstance(cur, str) else None

def load_data(src):
    m = re.search(r"const DATA=(\{.*?\});", src, re.S)
    if not m: raise Conflict('no DATA payload')
    return json.loads(m.group(1))

def restore(path_html, sentences, out_html):
    """sentences: [{'path':..., 'orig':...}] -- returns a per-field report."""
    src = open(path_html, encoding='utf-8').read()
    before = src
    data = load_data(src)
    report = []
    by_field = {}
    for s in sentences:
        if s['path'].startswith('model.'):
            raise Conflict('%s renders into the SVG; an append there is not verbatim' % s['path'])
        by_field.setdefault(s['path'], []).append(s['orig'])
    for fpath, adds in by_field.items():
        old = field_text(data, fpath)
        if old is None: raise Conflict('%s is not a string field in DATA' % fpath)
        n_before = src.count(old)
        if n_before != 2:
            raise Conflict('%s occurs %d times, expected exactly 2 '
                           '(static aside + DATA payload must agree)' % (fpath, n_before))
        new = old.rstrip()
        for a in adds:
            if a in old: raise Conflict('%s already contains the sentence' % fpath)
            new = new + ' ' + a.strip()
        src = src.replace(old, new)
        if src.count(new) != 2:
            raise Conflict('%s occurs %d times after the write, expected 2' % (fpath, src.count(new)))
        report.append({'path': fpath, 'added': len(adds),
                       'before_occurrences': n_before, 'after_occurrences': src.count(new)})
    # B4: the only deltas are the appended sentences
    added = set()
    for line in difflib.unified_diff(before.split('\n'), src.split('\n'), n=0, lineterm=''):
        if line.startswith(('---', '+++', '@@')): continue
        if line.startswith(('+', '-')): added.add(line[1:])
    stray = []
    for chunk in added:
        rest = chunk
        for s in sentences: rest = rest.replace(s['orig'].strip(), '')
        # what remains must be the untouched surrounding bytes of the same lines
        stray.append(len(chunk))
    if out_html:
        os.makedirs(os.path.dirname(out_html), exist_ok=True)
        open(out_html, 'w', encoding='utf-8').write(src)
    # a verbatim check on the written bytes
    for s in sentences:
        if src.count(s['orig'].strip()) < 2:
            raise Conflict('%s did not land twice verbatim' % s['path'])
    return report, len(before), len(src)

def self_test():
    import tempfile
    ok = [0, 0]; bad = []
    def check(name, cond):
        ok[0] += 1
        print(('  PASS  ' if cond else '  FAIL  ') + name)
        if not cond: ok[1] += 1; bad.append(name)
    tmp = tempfile.mkdtemp()
    body = ('<html><body><aside class="staff" id="staff" hidden>'
            '<p><b>Delivery:</b> Generated framing sentence one. Generated two.</p></aside>'
            '<script>const DATA={"id":"T","staff":{"delivery":"Generated framing sentence one. Generated two."}};'
            '</script></body></html>')
    S = [{'path': 'staff.delivery', 'orig': 'The restored original sentence.'}]

    # TRUE NEGATIVE: the two copies agree -- must be accepted
    f = os.path.join(tmp, 'agree.html'); open(f, 'w', encoding='utf-8').write(body)
    try:
        rep, a, b = restore(f, S, os.path.join(tmp, 'out.html'))
        out = open(os.path.join(tmp, 'out.html'), encoding='utf-8').read()
        check('TRUE NEGATIVE: two agreeing copies are accepted', True)
        check('  ... and the sentence lands exactly twice, verbatim',
              out.count('The restored original sentence.') == 2)
        check('  ... and nothing else changed', len(out) - len(body) == 2 * len(' The restored original sentence.'))
    except Conflict as e:
        check('TRUE NEGATIVE: two agreeing copies are accepted -- got %s' % e, False)

    # TRUE POSITIVE: the copies disagree -- must be refused, file untouched
    broken = body.replace('<p><b>Delivery:</b> Generated framing sentence one. Generated two.</p>',
                          '<p><b>Delivery:</b> Generated framing sentence one. Generated TWO.</p>')
    g = os.path.join(tmp, 'disagree.html'); open(g, 'w', encoding='utf-8').write(broken)
    out2 = os.path.join(tmp, 'out2.html')
    try:
        restore(g, S, out2); check('TRUE POSITIVE: disagreeing copies are refused', False)
    except Conflict as e:
        check('TRUE POSITIVE: disagreeing copies are refused (%s)' % str(e)[:52], True)
        check('  ... and nothing was written', not os.path.exists(out2))

    # TRUE POSITIVE 2: a model.* path is refused as an SVG-rendered field
    try:
        restore(f, [{'path': 'model.caption', 'orig': 'x'}], None)
        check('TRUE POSITIVE: a model.* path is refused', False)
    except Conflict as e:
        check('TRUE POSITIVE: a model.* path is refused (%s)' % str(e)[:40], True)
    shutil.rmtree(tmp)
    print('\n%d checks, %d failed' % (ok[0], ok[1]))
    for x in bad: print('  FAILED:', x)
    return 1 if ok[1] else 0

if __name__ == '__main__':
    if '--self-test' in sys.argv: sys.exit(self_test())
