#!/usr/bin/env python3
"""A5 -- census the three repos for a harness that deletes a path it was HANDED
without first proving that path is inside something it owns.

INCLUSION RULE, stated so the number means something:
  universe   = every file tracked at origin/main in the three repositories,
               read as bytes and decoded utf-8 with errors ignored; binary and
               unreadable files are counted and excluded, never silently dropped.
  candidate  = a line matching one of the DELETE verbs below.
  finding    = a candidate whose deleted path expression reaches an EXTERNAL
               source -- directly on the line, or through a variable assigned
               from one earlier in the same file -- AND for which no CONTAINMENT
               proof appears earlier in the file.
  A literal path with no external input is not a finding. A guarded delete is
  reported as GUARDED, not hidden, so the guard can be inspected too.

This is a regex census. It cannot follow a path across files or through a
function boundary, and it says so rather than implying completeness; an LLM
sweep runs beside it for the shapes a regex cannot express.
"""
import re, subprocess, sys
from pathlib import Path

REPOS = [('Lessons', '/home/user/Lessons'),
         ('Site', '/home/user/mattroper1977.github.io'),
         ('Apps', '/home/user/matt-s-apps-')]

DELETE = [
    (re.compile(r'\brm\s+-[A-Za-z]*[rf][A-Za-z]*\b'), 'rm -rf'),
    (re.compile(r'\bshutil\.rmtree\s*\('), 'shutil.rmtree'),
    (re.compile(r'\bos\.(?:remove|unlink|rmdir|removedirs)\s*\('), 'os.remove'),
    (re.compile(r'\.unlink\s*\(|\.rmdir\s*\('), 'Path.unlink'),
    (re.compile(r'\bfs\.(?:rmSync|rmdirSync|unlinkSync|rm)\s*\(|fs\.promises\.rm\s*\('), 'fs.rm'),
    (re.compile(r'\brimraf\b|\bdel\s*\(\s*\['), 'rimraf/del'),
    (re.compile(r'-delete\b'), 'find -delete'),
    (re.compile(r'\bgit\s+clean\s+-[A-Za-z]*[dfx]'), 'git clean'),
]
# Something that came from outside this script, tested against the DELETE'S OWN
# ARGUMENT and not the whole line. The first cut tested the line, and duly
# reported `rm -f _served/Lessons && ln -s "$PWD" _served/Lessons` -- a literal
# target, with the variable in the OTHER command.
EXTERNAL_DIRECT = re.compile(
    r'\$\{?[1-9@*]|sys\.argv|os\.environ|process\.argv|process\.env'
    r'|\bargs\.[A-Za-z_]|\$\{\{\s*(?:inputs|github|env)\.')
# A bare $VAR only counts if that name was ASSIGNED from an external source
# earlier in the file. Otherwise `for T in T1 T2 ...; do rm -rf "drop_$T"` reads
# as externally supplied when the values are a hardcoded list in the same script.
BARE_VAR = re.compile(r'\$\{?([A-Za-z_][A-Za-z0-9_]*)')
# a variable on the delete line that was assigned from an external source above it
# NOT anchored at ^. `set -u; W=$1; SITE=$2; OUT=$4; ...` puts four external
# assignments on one line after a command, and an anchored pattern sees none of
# them. That mistake made this census report a clean ZERO over a universe that
# contained two real findings it had already been shown by hand.
ASSIGN_EXTERNAL = re.compile(
    r'\b(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[^;\n]*?'
    r'(?:\$\{?[1-9@]|sys\.argv|os\.environ|process\.argv|process\.env'
    r'|args\.[A-Za-z_]|parse_args\(|\$\{\{\s*inputs\.)')
# `cd "$W" && git clean -qfd .` deletes a RELATIVE path -- but in a directory the
# caller chose. The delete's own argument names nothing external, and the danger
# is entirely in the cd. So a relative-target delete counts as external whenever
# an external cd precedes it.
CD_EXTERNAL = re.compile(r'\bcd\s+"?\$\{?([A-Za-z_][A-Za-z0-9_]*|[1-9])')
# Lines longer than this are minified bundles, not harnesses. The unanchored lazy
# assignment pattern backtracks quadratically over one, and a single 400 KB line
# in a vendored tesseract worker took this census from 25 seconds to four minutes.
SCAN_LINE_CAP = 500
RELATIVE_TARGET = re.compile(r'^\s*(?:-[A-Za-z-]+\s+|-e\s+\S+\s+)*\.?(?:/|\s|$)')
CONTAINMENT = [
    (re.compile(r'case\s+"?\$'), 'case guard on the path'),
    (re.compile(r'is_relative_to|commonpath|os\.path\.realpath|\.resolve\(\)'), 'resolve/containment'),
    (re.compile(r'startswith\s*\(|\.startsWith\s*\('), 'prefix check'),
    (re.compile(r'TemporaryDirectory|mkdtemp|mkdtempSync|mktemp\b'), 'script-owned temp dir'),
    (re.compile(r'\[\[\s*"?\$\w+"?\s*==\s*'), 'bash [[ ]] pattern guard'),
    (re.compile(r'realpath\b'), 'realpath normalisation'),
]
TEXT_SUFFIX = {'.sh','.bash','.py','.js','.cjs','.mjs','.yml','.yaml','.json','.toml','.cfg',
               '.mk','.make','.md','.txt','.ts','.rb','.pl',''}

def files(root):
    out = subprocess.check_output(['git','-C',root,'ls-tree','-r','--name-only','origin/main'], text=True)
    return [p for p in out.split('\n') if p]

def read(root, path):
    try:
        return subprocess.check_output(['git','-C',root,'show','origin/main:'+path], stderr=subprocess.DEVNULL).decode('utf-8','ignore')
    except Exception:
        return None

def census(extra=None, plants_only=False):
    universe = considered = binary = 0
    rows = []
    targets = [] if plants_only else [(n, r, files(r)) for n, r in REPOS]
    if extra:
        targets.append(('PLANT', extra[0], [extra[1]]))
    for name, root, paths in targets:
        for path in paths:
            universe += 1
            if Path(path).suffix.lower() not in TEXT_SUFFIX:
                continue
            text = (Path(root, path).read_text('utf-8','ignore') if name == 'PLANT' else read(root, path))
            if text is None:
                binary += 1; continue
            considered += 1
            lines = text.split('\n')
            assigned = {m.group(1) for l in lines if len(l) <= SCAN_LINE_CAP
                        for m in ASSIGN_EXTERNAL.finditer(l)}
            cd_lines = [i for i, l in enumerate(lines, 1) for m in [CD_EXTERNAL.search(l)]
                        if m and (m.group(1) in assigned or m.group(1).isdigit())]
            for i, line in enumerate(lines, 1):
                for pat, verb in DELETE:
                    m = pat.search(line)
                    if not m:
                        continue
                    target = line[m.end():]          # the delete's own argument
                    direct = bool(EXTERNAL_DIRECT.search(target))
                    indirect = any(v in assigned for v in BARE_VAR.findall(target))
                    via_cd = (bool(RELATIVE_TARGET.match(target)) and any(c <= i for c in cd_lines))
                    if not (direct or indirect or via_cd):
                        continue
                    before = '\n'.join(lines[:i])
                    guard = next((why for g, why in CONTAINMENT if g.search(before)), None)
                    rows.append({'repo': name, 'path': path, 'line': i, 'verb': verb,
                                 'src': line.strip()[:120],
                                 'origin': ('on the delete line' if direct else
                                            'via a variable assigned above' if indirect else
                                            'relative target, after cd to an external path'),
                                 'status': 'GUARDED (' + guard + ')' if guard else 'UNGUARDED'})
                    break
    return {'universe': universe, 'considered': considered, 'unreadable': binary, 'rows': rows}

PLANT_UNGUARDED = """#!/bin/bash
# the exact shape ORDER TH1 A5 names
OUT="$2"
rm -rf "$OUT"
mkdir -p "$OUT"
"""
PLANT_CD = """#!/bin/bash
# the delete names nothing external; the cd above it does
W=$1
cd "$W" && git clean -qfd -e tools/ .
"""
PLANT_SEMICOLON = """#!/bin/bash
# four external assignments on one line, after a command
set -u; W=$1; SITE=$2; LAND=$3; OUT=$4; mkdir -p "$OUT"
rm -rf "$OUT/s24"
"""
PLANT_INTERNAL = """#!/bin/bash
# the value is a hardcoded loop list, not something the caller supplies
for T in T1 T2 T3; do
  rm -rf "drop_$T"
done
"""
PLANT_GUARDED = """#!/bin/bash
# the same delete, containment proved first
OUT="$2"
case "$OUT" in /tmp/claude-0/*/scratchpad/*) ;; *) echo refusing; exit 2;; esac
rm -rf "$OUT"
mkdir -p "$OUT"
"""


def self_test():
    """A zero is only a result if the census could have found something.

    Two plants, both ways: the shape must be reported UNGUARDED, and its guarded
    twin -- same delete, same variable, same line -- must not be. A census that
    only ever passes is indistinguishable from one that cannot see."""
    import tempfile, os
    ok = True
    with tempfile.TemporaryDirectory(prefix='delete-census-selftest-') as temp:
        for name, body, want in [('unguarded.sh', PLANT_UNGUARDED, 'UNGUARDED'),
                                 ('guarded.sh', PLANT_GUARDED, 'GUARDED'),
                                 ('internal.sh', PLANT_INTERNAL, 'NOT REPORTED'),
                                 ('cd_then_clean.sh', PLANT_CD, 'UNGUARDED'),
                                 ('semicolon_assign.sh', PLANT_SEMICOLON, 'UNGUARDED')]:
            Path(temp, name).write_text(body)
            hits = [x for x in census(extra=(temp, name), plants_only=True)['rows']
                    if x['repo'] == 'PLANT']
            got = hits[0]['status'] if hits else 'NOT REPORTED AT ALL'
            passed = got.startswith(want)
            ok = ok and passed
            print('  [%s] planted %-13s expected %-9s got %s'
                  % ('ok' if passed else 'FAIL', name, want, got))
    print('self-test', 'PASS' if ok else 'FAIL')
    return ok


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        raise SystemExit(0 if self_test() else 1)
    r = census()
    print('UNIVERSE   : %d files tracked at origin/main across three repositories' % r['universe'])
    print('CONSIDERED : %d (text suffixes only); %d unreadable/binary excluded' % (r['considered'], r['unreadable']))
    ung = [x for x in r['rows'] if x['status'] == 'UNGUARDED']
    print('CANDIDATES : %d deleting an externally-supplied path' % len(r['rows']))
    print('UNGUARDED  : %d\n' % len(ung))
    for x in sorted(r['rows'], key=lambda x: (x['status'] != 'UNGUARDED', x['repo'], x['path'], x['line'])):
        print('%-9s %-6s %s:%d  [%s]  %s' % (x['status'].split(' ')[0], x['repo'], x['path'], x['line'], x['verb'], x['origin']))
        print('           %s' % x['src'])
