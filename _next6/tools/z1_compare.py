#!/usr/bin/env python3
"""ORDER N6-Z §Z1 — compare the two independent verdict passes.

A disagreement between them is a FINDING, not a tie to be broken by whichever ran
last, so a row where the two classes differ is written out as UNRESOLVED with both
readings kept rather than reconciled.

The two passes are differently keyed: one judges from the extracted matrix row and
never opens a deck, the other opens every deck and never reads the manifest. They
do share one input -- the join that says which SoW cell each lesson is measured
against -- so they are NOT independent about the calendar question. That is what
z1_join_probe.py is for, and the calendarContingent / calendarInert flags written
here come from it.

Rows are keyed on the FILE, never on the short id: LAUNCH_Humanities carries
id=None in the matrix and its bundle uses the basename, and an id-keyed join
silently collapsed its six rows into one and lost five of 132.
"""
import json, collections, sys

SC = "/tmp/claude-0/-home-user-Lessons/1f8cd552-913d-529c-af4c-e31f55e5bfc8/scratchpad"
D = SC + "/../subagents"
JOURNAL = ("/root/.claude/projects/-home-user-Lessons/"
           "1f8cd552-913d-529c-af4c-e31f55e5bfc8/subagents/workflows/"
           "wf_626b0d79-bbb/journal.jsonl")

order, res = [], {}
for line in open(JOURNAL):
    line = line.strip()
    if not line: continue
    o = json.loads(line)
    if o.get('type') == 'started':
        order.append(o['key'])
    elif o.get('type') == 'result' and isinstance(o.get('result'), dict):
        res[o['key']] = o['result']

data, deck = {}, {}
for i, k in enumerate(order):
    r = res.get(k)
    if not r: continue
    (data if i < 9 else deck)[r['pack']] = r['verdicts']

# calendar-contingent rows: the two readings select a different SoW cell
# key everything on the FILE. LAUNCH_Humanities carries id=None in the matrix and
# its bundle uses the basename, so an id-keyed join silently collapsed its six
# rows into one and lost five of 132.
import glob, os
idmap = {}                      # (pack, bundle id) -> file
for bp in glob.glob(SC + '/bundles2/*.json'):
    pack = os.path.basename(bp)[:-5]
    for x in json.load(open(bp)):
        idmap[(pack, x['id'])] = x['file']

rows = json.load(open(SC + '/matrix.json'))
contingent = set()
bypack = collections.defaultdict(dict)
for r in rows:
    bypack[r['pack']][r['file']] = r
    if r.get('A_sourceWeek') or r.get('A_termLabel'):
        continue
    if (r.get('sow_SOW') or {}).get('outcome') != (r.get('sow_CALENDAR') or {}).get('outcome'):
        contingent.add((r['pack'], r['file']))

# A row whose two candidate cells DIFFER is not automatically a row whose VERDICT
# turns on the ruling. Where the content probe scores 0 against both cells, neither
# reading delivers the outcome and the verdict stands either way -- BUILD_Humanities
# is the whole of that case. Ask the probe rather than assume.
sys.path.insert(0, '/home/user/Lessons/_next6/tools')
import z1_join_probe as JP
inert = set()
for r in rows:
    if (r['pack'], r['file']) not in contingent:
        continue
    dwords = JP.words(' '.join(filter(None, [
        r.get('A_title'), r.get('A_objective'), r.get('A_outcome'),
        r.get('B_objective'), ' '.join(r.get('B_sc') or []), r.get('B_seqOutcome')])))
    a = JP.content_score(dwords, (r.get('sow_SOW') or {}).get('outcome'))
    b = JP.content_score(dwords, (r.get('sow_CALENDAR') or {}).get('outcome'))
    if a == 0 and b == 0:
        inert.add((r['pack'], r['file']))

def by_file(pack, verdicts):
    d = {}
    for v in verdicts or []:
        f = idmap.get((pack, v['id']))
        if f:
            d[f] = v
    return d

data = {p: by_file(p, v) for p, v in data.items()}
deck = {p: by_file(p, v) for p, v in deck.items()}

out, agree, disagree, missing = [], 0, 0, 0
tally = collections.Counter()
for pack in sorted(bypack):
    for f, r in bypack[pack].items():
        a = (data.get(pack) or {}).get(f)
        b = (deck.get(pack) or {}).get(f)
        rec = {'pack': pack, 'id': r.get('id') or r['base'], 'file': f,
               'data': a and a['verdict'], 'deck': b and b['verdict'],
               'dataTier': a and a['tier'], 'deckTier': b and b['tier'],
               'dataReason': a and a['reason'], 'deckReason': b and b['reason'],
               'calendarContingent': (pack, f) in contingent and (pack, f) not in inert,
               'calendarInert': (pack, f) in inert}
        if a is None or b is None:
            rec['final'] = 'PENDING'; missing += 1
        elif a['verdict'] == b['verdict']:
            rec['final'] = a['verdict']; agree += 1
        else:
            rec['final'] = 'UNRESOLVED'; disagree += 1
        rec['tier'] = max([t for t in (rec['dataTier'], rec['deckTier'])
                           if t and t != 'none'] or ['none'])
        tally[rec['final']] += 1
        out.append(rec)

json.dump(out, open(SC + '/verdicts_final.json', 'w'), indent=1)
print("rows %d   both passes agree %d   disagree %d   pending %d"
      % (len(out), agree, disagree, missing))
print("rows whose two candidate cells differ: %d" % len(contingent))
print("  ...of which the verdict genuinely turns on the ruling: %d" % (len(contingent) - len(inert)))
print("  ...neither cell matches, so the verdict stands either way: %d" % len(inert))
print()
for k, v in tally.most_common():
    print("  %-24s %d" % (k, v))
if '-d' in sys.argv:
    print("\nDISAGREEMENTS")
    for r in out:
        if r['final'] == 'UNRESOLVED':
            print("  %-20s %-40s data=%-22s deck=%-22s%s" % (
                r['pack'], r['id'][:40], r['data'], r['deck'],
                '  [calendar-contingent]' if r['calendarContingent'] else ''))
