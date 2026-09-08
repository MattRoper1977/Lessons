#!/usr/bin/env python3
"""RX3: fold one or more publication censuses (from _rx3/admission.py) into a Site registry copy.
New paths become [digest, ARRIVING]. Changed paths become a transition pair [what main builds now, what the branch will
build]; a pre-existing pair loses its stale or never-merged half. --main-output is a fully admitted build of Lessons main
(the digest main carries is read from its files). Prints every row it moves."""
import argparse, json, hashlib
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('--registry', required=True); ap.add_argument('--main-output', required=True)
ap.add_argument('--census', action='append', required=True); ap.add_argument('--note', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args()
reg = json.load(open(a.registry)); tree = reg['trees']['education-lessons']; main_out = Path(a.main_output) / 'education-lessons'
moved = []
for c in a.census:
    rep = json.load(open(c)); t = rep['trees']['education-lessons']
    for name in ('education-site', 'education-apps'): assert not rep['trees'][name]['changed'] and not rep['trees'][name]['unreviewed'], name
    for p, d in t['unreviewed'].items():
        assert p not in tree, 'unreviewed path already registered: ' + p
        tree[p] = [d, 'ARRIVING']; moved.append(('ARRIVING', p, '', d))
    for p, ch in t['changed'].items():
        cur = tree[p]; cur = cur if isinstance(cur, list) else [cur]
        if not (main_out / p).exists():
            # absent from main's build: an ARRIVING row whose reviewed digest moves with the branch
            assert 'ARRIVING' in cur, ('absent from main but not ARRIVING', p)
            tree[p] = [ch['built'], 'ARRIVING']; moved.append(('ARRIVING', p, '+'.join(x[:8] for x in cur), ch['built'])); continue
        main_d = hashlib.sha256((main_out / p).read_bytes()).hexdigest(); assert main_d in cur, ('main digest not admitted', p)
        tree[p] = [main_d, ch['built']]; moved.append(('PAIR', p, '+'.join(x[:8] for x in cur), ch['built']))
reg['reviewSources'].append(a.note)
Path(a.out).write_text(json.dumps(reg, ensure_ascii=False, indent=1) + '\n')
for kind, p, cur, new in moved: print(f'{kind:8s} {p}  {cur} -> {new[:16]}')
