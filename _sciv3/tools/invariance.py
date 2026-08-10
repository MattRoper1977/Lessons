"""Gates 4, 5, 7 — what must NOT have moved.

    python3 _sciv3/tools/invariance.py <ROLLBACK_SHA>
"""
import sys, subprocess, os, glob, re

SHA = sys.argv[1]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FAIL = []


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True, cwd=REPO).stdout


def check(ok, label, detail=''):
    print(('  PASS  ' if ok else '  FAIL  ') + label + (('   ' + detail) if detail else ''))
    if not ok:
        FAIL.append(label)


print('=== GATE 4 · the live twenty-five are byte-identical (universe: 25 files) ===')
diff = sh('git', 'diff', '--stat', f'{SHA}..HEAD', '--',
          'Science_Teesside/Grow/SCI_G_*', 'Science_Teesside/Build/SCI_B_*',
          'Science_Teesside/Launch/SCI_L_*').strip()
check(diff == '', 'git diff --stat over the live twenty-five is empty', repr(diff[:200]))

live = sorted(glob.glob(f'{REPO}/Science_Teesside/*/SCI_*.html'))
live = [f for f in live if 'v3_40min' not in f]
check(len(live) == 25, 'exactly 25 live lesson files at HEAD', str(len(live)))
print('   blob hashes at ROLLBACK_SHA vs working tree:')
drift = []
for f in live:
    rel = os.path.relpath(f, REPO)
    old = sh('git', 'rev-parse', f'{SHA}:{rel}').strip()
    new = sh('git', 'hash-object', rel).strip()
    print(f'     {"same" if old == new else "DRIFT"}  {old[:12]}  {rel}')
    if old != new:
        drift.append(rel)
check(not drift, 'all twenty-five blob hashes match their ROLLBACK_SHA values', str(drift))

print('\n=== GATE 5 · sentinels ===')


def fileset(needle):
    out = set()
    for f in glob.glob(f'{REPO}/**/*.html', recursive=True):
        if '/.git/' in f or '/node_modules/' in f:
            continue
        try:
            if needle in open(f, encoding='utf-8', errors='ignore').read():
                out.add(os.path.relpath(f, REPO))
        except OSError:
            pass
    return out


def fileset_at(sha, needle):
    files = sh('git', 'grep', '-Il', needle, sha, '--', '*.html').strip().splitlines()
    return {l.split(':', 1)[1] for l in files if ':' in l}


loop_now, loop_then = fileset('ll-g:loop-mark'), fileset_at(SHA, 'll-g:loop-mark')
check(loop_now == loop_then, "`ll-g:loop-mark` file set identical before and after",
      f'{len(loop_then)} -> {len(loop_now)}')
print('   ll-g:loop-mark files:', sorted(loop_now) or '(none)')
new_paths = {p for p in loop_now if 'v3_40min' in p or p.startswith('Baseline_Weeks/')}
check(not new_paths, 'none of the 35 new lessons carries ll-g:loop-mark', str(new_paths))

cl_now = fileset('What I said, and what it changed')
cl_then = fileset_at(SHA, 'What I said, and what it changed')
added, removed = cl_now - cl_then, cl_then - cl_now
expect = {os.path.relpath(f, REPO) for f in
          glob.glob(f'{REPO}/Science_Teesside/Launch/v3_40min/SCI_L_*.html')}
check(added == expect and not removed,
      'closure-line set grows by exactly the 15 new LAUNCH lessons and nothing else',
      f'+{len(added)} / -{len(removed)}')
print(f'   before: {len(cl_then)} files   after: {len(cl_now)} files')
print('   added:')
for p in sorted(added):
    print('     +', p)
bad = [p for p in added if '/Build/' in p or '/Grow/' in p]
check(not bad, 'no BUILD or GROW file appears in the closure-line set', str(bad))

print('\n=== GATE 7 · frozen trees ===')
for d in ('biology', 'chemistry', '2 Physics 10'):
    old = sh('git', 'rev-parse', f'{SHA}:{d}').strip()
    new = sh('git', 'ls-tree', 'HEAD', f'{d}').split()
    cur = subprocess.run(['git', 'ls-files', '-s', d], capture_output=True, text=True,
                         cwd=REPO).stdout
    import hashlib
    wt = hashlib.sha1(cur.encode()).hexdigest()[:8]
    check(old == (new[2] if len(new) > 2 else ''), f'{d}/ tree hash unchanged vs ROLLBACK_SHA',
          f'{old[:12]} (index digest {wt})')

print('\n=== assessed + Art files untouched ===')
for pat in ('Grow/Slideshows/GROW_HUM_W7*', 'Launch/Slideshows/LAUNCH_HUM_W7*', 'Art_Teesside/*'):
    d = sh('git', 'diff', '--stat', f'{SHA}..HEAD', '--', pat).strip()
    check(d == '', f'{pat} unchanged', repr(d[:120]))

print('\n' + ('INVARIANCE: ALL PASS' if not FAIL else f'{len(FAIL)} FAILURE(S)'))
sys.exit(1 if FAIL else 0)
