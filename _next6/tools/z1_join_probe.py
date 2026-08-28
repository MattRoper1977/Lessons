"""Third instrument for the bare-week packs: which calendar reading does the
deck's own content actually match? Keyed to content-word overlap between what
the deck teaches and each candidate SoW outcome. No agent, no LLM, no reuse of
the join code -- it consumes both candidate rows the matrix already carries and
scores them independently."""
import json, re, sys, collections

STOP = set('''a an the and or of to in for on with by from as at is are be been being this that these those
it its their his her they them we our you your i can will shall may might must do does did done
use uses using used one two three make makes making explain explains describe describes
lesson week pupils pupil learners learner students student'''.split())

def words(s):
    return set(w for w in re.findall(r"[a-z]+", (s or '').lower()) if len(w) > 3 and w not in STOP)

def score(deck, outcome):
    o = words(outcome)
    if not o: return None
    return len(o & deck) / len(o)

args = [x for x in sys.argv[1:] if not x.startswith('-')]
if not args:
    sys.exit("usage: z1_join_probe.py MATRIX.json [-v]")
rows = json.load(open(args[0]))
tally = collections.defaultdict(lambda: collections.Counter())
detail = collections.defaultdict(list)

for r in rows:
    if r.get('A_sourceWeek') or r.get('A_termLabel'):
        continue                      # pack states its own half-term; no calendar needed
    deck = words(' '.join(filter(None, [
        r.get('A_title'), r.get('A_objective'), r.get('A_outcome'),
        r.get('B_objective'), ' '.join(r.get('B_sc') or []), r.get('B_seqOutcome')])))
    s = {}
    for reading in ('SOW', 'CALENDAR'):
        cell = r.get('sow_' + reading)
        s[reading] = score(deck, cell.get('outcome')) if cell else None
    p = r['pack']
    if s['SOW'] is None and s['CALENDAR'] is None:
        tally[p]['no-cell either way'] += 1; continue
    a, b = (s['SOW'] or -1), (s['CALENDAR'] or -1)
    if abs(a - b) < 1e-9:
        w = 'tie'
    else:
        w = 'SOW' if a > b else 'CALENDAR'
    tally[p][w] += 1
    detail[p].append((r['id'], w, s['SOW'], s['CALENDAR'],
                      (r.get('sow_SOW') or {}).get('outcome'),
                      (r.get('sow_CALENDAR') or {}).get('outcome')))

print("WHICH CALENDAR READING DOES THE DECK'S OWN CONTENT MATCH?")
print("(bare-estate-week packs only; overlap of SoW outcome content words with the deck)\n")
print(f"{'pack':<20}{'SOW':>6}{'CALENDAR':>10}{'tie':>6}{'no cell':>9}")
for p in sorted(tally):
    t = tally[p]
    print(f"{p:<20}{t['SOW']:>6}{t['CALENDAR']:>10}{t['tie']:>6}{t['no-cell either way']:>9}")
print()
if '-v' in sys.argv:
    for p in sorted(detail):
        print('=' * 78); print(p)
        for id_, w, a, b, oa, ob in detail[p]:
            print("  %-10s %-9s sow=%-5s cal=%-5s" % (id_, w, "None" if a is None else round(a,2), "None" if b is None else round(b,2)))
            print(f"     SOW      {str(oa)[:80]}")
            print(f"     CALENDAR {str(ob)[:80]}")
