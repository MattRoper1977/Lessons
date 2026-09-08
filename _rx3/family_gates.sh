#!/bin/bash
# RX3 family gate battery. Usage: family_gates.sh <worktree> <site root> <land.json> <out dir>
# Gates: node --check (every inline script) · dup-id 0 · sentinel sets identical to origin/main · s24 print render + measure ·
#        390 px boot (0 console/page errors, way-home in the first viewport, staff guidance hidden, one h1, no horizontal overflow) ·
#        tier gate condition (v3_tier_gate.py, PEQ *_Estate_v3 only) · s23 names (MEASUREMENT INVALID by design: reference list absent).
set -u; W=$1; SITE=$2; LAND=$3; OUT=$4; mkdir -p "$OUT"; cd "$W"; rc=0
FILES=$(python3 -c "import json,sys;print(' '.join(r['target'] for r in json.load(open('$LAND'))))")
ROUTES=$(python3 -c "import json;print(','.join('/Lessons/'+r['target'] for r in json.load(open('$LAND'))))")
echo "== node --check"; python3 - "$W" $FILES <<'PY' | tee "$OUT/node_check.txt"
import re,subprocess,tempfile,os,sys
bad=0
for t in sys.argv[2:]:
    s=open(os.path.join(sys.argv[1],t),encoding='utf-8').read()
    for i,m in enumerate(re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>',s,re.S)):
        with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False) as f: f.write(m.group(1));p=f.name
        r=subprocess.run(['node','--check',p],capture_output=True,text=True);os.unlink(p)
        if r.returncode: bad+=1;print('SYNTAX',t,i,r.stderr[:160])
    ids=re.findall(r'id="([^"]+)"',s);dups=sorted({i for i in ids if ids.count(i)>1})
    print(('DUPID ' if dups else 'ok    ')+t+' dup-ids='+str(dups))
print('scripts with syntax errors:',bad); sys.exit(1 if bad else 0)
PY
[ ${PIPESTATUS[0]} -ne 0 ] && rc=1
echo "== sentinel sets vs origin/main"; git add -A >/dev/null 2>&1
git grep -l 'll-g:loop-mark' -- '*.html' | sort > "$OUT/lm_land.txt"; git grep -l 'What I said, and what it changed' -- '*.html' | sort > "$OUT/cl_land.txt"; git reset -q
git -C "$W" show origin/main --name-only >/dev/null 2>&1
( cd "$W" && git ls-tree -r --name-only origin/main -- '*.html' >/dev/null )
git grep -l 'll-g:loop-mark' origin/main -- '*.html' | sed 's/^origin\/main://' | sort > "$OUT/lm_main.txt"; git grep -l 'What I said, and what it changed' origin/main -- '*.html' | sed 's/^origin\/main://' | sort > "$OUT/cl_main.txt"
if diff -q "$OUT/lm_main.txt" "$OUT/lm_land.txt" >/dev/null && diff -q "$OUT/cl_main.txt" "$OUT/cl_land.txt" >/dev/null; then echo "sentinels: set-identical to origin/main (loop-mark $(wc -l < "$OUT/lm_main.txt") · closure $(wc -l < "$OUT/cl_main.txt"))"; else echo "SENTINEL SET DRIFT"; diff "$OUT/lm_main.txt" "$OUT/lm_land.txt"; diff "$OUT/cl_main.txt" "$OUT/cl_land.txt"; rc=1; fi
echo "== s24 print render"; rm -rf "$OUT/s24"; NODE_PATH=/home/user/Lessons/node_modules node _next6/tools/s24_render.mjs --out "$OUT/s24" $FILES > "$OUT/s24_render.log" 2>&1 || { echo "s24 render FAILED"; tail -3 "$OUT/s24_render.log"; rc=1; }
python3 _next6/tools/s24_print_renders.py --renders "$OUT/s24" > "$OUT/s24_measure.log" 2>&1; s=$?; tail -2 "$OUT/s24_measure.log"; [ $s -ne 0 ] && rc=1
echo "== 390 px boot"; NODE_PATH=/home/user/Lessons/node_modules node /home/user/Lessons/_rx3/boot390.cjs --root="$W" --site="$SITE" "--routes=$ROUTES" --out="$OUT/boot390.json" | tee "$OUT/boot390.txt"; [ ${PIPESTATUS[0]} -ne 0 ] && rc=1
echo "== tier gate (condition measured; PEQ *_Estate_v3 only)"; python3 _passpq/tools/v3_tier_gate.py > "$OUT/tier_gate.txt" 2>&1; echo "tier gate exit $? · $(tail -1 "$OUT/tier_gate.txt")"
echo "== s23 names: MEASUREMENT INVALID by design (reference list absent; gates.py g10)"
echo "== data-URI images > 50 KB across landed files: $(python3 -c "
import re,sys,os;n=0
for t in '$FILES'.split(): n+=len(re.findall(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]{68000,}',open(os.path.join('$W',t),encoding='utf-8').read()))
print(n)")"
echo "FAMILY GATES rc=$rc"; exit $rc
