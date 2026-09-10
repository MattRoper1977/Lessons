#!/usr/bin/env python3
"""Rebuild _sx2/DECISIONS.md as an INDEX over _sx2/decisions/NNNN-<slug>.md.

Why this exists. DECISIONS.md was one append-only file, so two PRs adding two
rulings on the same night both appended to the same tail and both conflicted --
twice in one night. Resolving that a third time is not a fix. One file per ruling
means two PRs touch two different files and cannot collide.

The rules that follow from that:
  * a landed decision file is NEVER edited. A ruling that changes gets a new file
    that says so; D24 keeps its WITHDRAWN status inside its own file.
  * the index is GENERATED. Editing it by hand re-creates the problem.
  * --check reds when the index and the directory disagree, so a hand edit or a
    forgotten regeneration cannot pass CI.

--self-test carries both controls required by D28.
"""
import os, re, sys, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, '_sx2', 'decisions')
INDEX = os.path.join(ROOT, '_sx2', 'DECISIONS.md')
PREAMBLE = """# SX2 — Decisions record

Order SX2 (2026-09-09), written at the time, per the `_eca1`/`_glv3` convention.
Phase S: finish SX1 and get the Spring/Summer Science batch served.

**This file is generated.** One ruling per file in `_sx2/decisions/`; a landed
decision file is never edited. Add a ruling by adding a file, then run
`tools/decisions/build_index.py`. `--check` reds if this index and that directory
disagree.
"""

def slug(title):
    s = re.sub(r'[`*_]', '', title).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:60].rstrip('-')

def entries(d=None):
    d = d or DIR          # resolved at call time: --self-test repoints DIR
    out = []
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = re.match(r'^(\d{4})-([a-z0-9-]+)\.md$', f)
        if not m: continue
        body = open(os.path.join(d, f), encoding='utf-8').read()
        h = re.search(r'^##\s+(.+)$', body, re.M)
        first = ''
        for line in body.split('\n'):
            t = line.strip()
            if t and not t.startswith('#') and not t.startswith('>'):
                first = re.sub(r'[*`\[\]]', '', t); break
        out.append({'seq': m.group(1), 'slug': m.group(2), 'file': f,
                    'title': h.group(1).strip() if h else m.group(2),
                    'summary': (first[:120] + '…') if len(first) > 120 else first})
    return out

def render(rows):
    L = [PREAMBLE, '', '| # | ruling | summary |', '|---|---|---|']
    for r in rows:
        L.append('| `%s` | [%s](decisions/%s) | %s |' % (r['seq'], r['title'].replace('|', '\\|'),
                                                         r['file'], r['summary'].replace('|', '\\|')))
    L.append('')
    L.append('%d rulings. The text of each is in its own file and is never edited after landing.' % len(rows))
    return '\n'.join(L) + '\n'

def main(argv):
    rows = entries()
    new = render(rows)
    if '--check' in argv:
        cur = open(INDEX, encoding='utf-8').read() if os.path.exists(INDEX) else ''
        if cur == new:
            print('DECISIONS index matches %s (%d rulings)' % (os.path.relpath(DIR, ROOT), len(rows)))
            return 0
        print('DECISIONS INDEX STALE — the index and _sx2/decisions/ disagree.')
        for line in list(difflib.unified_diff(cur.split('\n'), new.split('\n'),
                                              'DECISIONS.md (on disk)', 'generated', lineterm=''))[:24]:
            print('  ' + line)
        print('\nRun tools/decisions/build_index.py to regenerate. Never edit the index by hand.')
        return 1
    open(INDEX, 'w', encoding='utf-8').write(new)
    print('wrote %s from %d files' % (os.path.relpath(INDEX, ROOT), len(rows)))
    return 0

def self_test():
    import tempfile, shutil
    global DIR, INDEX
    ok = [0, 0]
    def check(n, c):
        ok[0] += 1; print(('  PASS  ' if c else '  FAIL  ') + n)
        if not c: ok[1] += 1
    tmp = tempfile.mkdtemp(); d = os.path.join(tmp, 'decisions'); os.makedirs(d)
    open(os.path.join(d, '0001-first.md'), 'w', encoding='utf-8').write('## D1 — First\n\nThe first ruling.\n')
    open(os.path.join(d, '0002-second.md'), 'w', encoding='utf-8').write('## D2 — Second\n\nThe second ruling.\n')
    DIR = d; INDEX = os.path.join(tmp, 'DECISIONS.md')
    main([])
    # TRUE NEGATIVE: a freshly generated index matches its directory
    check('TRUE NEGATIVE: a generated index passes --check', main(['--check']) == 0)
    check('  ... and it lists both rulings', open(INDEX, encoding='utf-8').read().count('| `000') == 2)
    # TRUE POSITIVE: a ruling the index does not mention must red
    open(os.path.join(d, '0003-third.md'), 'w', encoding='utf-8').write('## D3 — Third\n\nPlanted, absent from the index.\n')
    check('TRUE POSITIVE: a planted missing entry reds --check', main(['--check']) == 1)
    main([])
    check('  ... and regenerating clears it', main(['--check']) == 0)
    # TRUE POSITIVE 2: a hand edit to the index must red
    cur = open(INDEX, encoding='utf-8').read()
    open(INDEX, 'w', encoding='utf-8').write(cur.replace('D3 — Third', 'D3 — Edited by hand'))
    check('TRUE POSITIVE: a hand edit to the index reds --check', main(['--check']) == 1)
    shutil.rmtree(tmp)
    print('\n%d checks, %d failed' % (ok[0], ok[1]))
    return 1 if ok[1] else 0

if __name__ == '__main__':
    sys.exit(self_test() if '--self-test' in sys.argv else main(sys.argv[1:]))
