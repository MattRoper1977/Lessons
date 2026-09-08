#!/usr/bin/env python3
"""RX3: fold one or more publication censuses (from _rx3/admission.py) into a Site registry copy.
New paths become [digest, ARRIVING]. Changed paths become a transition pair [what main builds now, what the branch will
build]; a pre-existing pair loses its stale or never-merged half. --main-output is a fully admitted build of Lessons main
(the digest main carries is read from its files). Prints every row it moves."""
import argparse, json, hashlib
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('--registry', required=True); ap.add_argument('--main-output', required=True)
ap.add_argument('--census', action='append', required=True); ap.add_argument('--note', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--keep-output', help="a build whose digests must stay admitted (the Site's own pinned source); when it lacks a path the row keeps ARRIVING; default: --main-output")
a = ap.parse_args()
reg = json.load(open(a.registry)); moved = []
for c in a.census:
  rep = json.load(open(c))
  for tree_name in ('education-site', 'education-lessons', 'education-apps'):
    t = rep['trees'][tree_name]; tree = reg['trees'][tree_name]; main_out = Path(a.main_output) / tree_name
    for p, d in t['unreviewed'].items():
        assert p not in tree, 'unreviewed path already registered: ' + p
        tree[p] = [d, 'ARRIVING']; moved.append(('ARRIVING', tree_name + '/' + p, '', d))
    keep_out = Path(a.keep_output) / tree_name if a.keep_output else main_out
    for p, ch in t['changed'].items():
        cur = tree[p]; cur = cur if isinstance(cur, list) else [cur]
        if a.keep_output and (keep_out / p).exists():
            keep_d = hashlib.sha256((keep_out / p).read_bytes()).hexdigest(); assert keep_d in cur, ('kept build digest not admitted', p)
            tree[p] = [keep_d, ch['built']]; moved.append(('PAIR', tree_name + '/' + p, '+'.join(x[:8] for x in cur), ch['built'])); continue
        if not (keep_out / p).exists():
            # absent from main's build: an ARRIVING row whose reviewed digest moves with the branch
            assert 'ARRIVING' in cur, ('absent from main but not ARRIVING', p)
            tree[p] = [ch['built'], 'ARRIVING']; moved.append(('ARRIVING', tree_name + '/' + p, '+'.join(x[:8] for x in cur), ch['built'])); continue
        main_d = hashlib.sha256((main_out / p).read_bytes()).hexdigest(); assert main_d in cur, ('main digest not admitted', p)
        tree[p] = [main_d, ch['built']]; moved.append(('PAIR', tree_name + '/' + p, '+'.join(x[:8] for x in cur), ch['built']))
reg['reviewSources'].append(a.note)
Path(a.out).write_text(json.dumps(reg, ensure_ascii=False, indent=1) + '\n')
for kind, p, cur, new in moved: print(f'{kind:8s} {p}  {cur} -> {new[:16]}')
