#!/bin/bash
# Re-land a family with the current tool; report which HTML bytes changed vs the previous landing json. Usage: reland.sh <worktree> <ids> <json>
set -u; W=$1; IDS=$2; J=$3; P=/tmp/claude-0/-home-user-Lessons/66c1d222-c1e7-597f-9ba2-ca04f6d2c4f3/scratchpad/intake/pack33/Classic_Lessons_33_Complete_Pack
cd "$W" && git checkout -q -- . && git clean -qfd -e tools/ . >/dev/null && cp /home/user/Lessons/tools/rx3_land.py /home/user/Lessons/tools/rx3_scenes.py tools/ && cp "$J" "$J.prev" 2>/dev/null
python3 tools/rx3_land.py --pack $P --repo "$W" --admission /home/user/Lessons/_rx2/ADMISSION.md --ids "$IDS" --json "$J" | tail -n +2
python3 - "$J" <<'PY'
import json,sys,os
new=json.load(open(sys.argv[1]));old={r['id']:r for r in json.load(open(sys.argv[1]+'.prev'))} if os.path.exists(sys.argv[1]+'.prev') else {}
for r in new: print(('SAME  ' if old.get(r['id'],{}).get('sha256')==r['sha256'] else 'CHANGED ')+r['id']+' -> '+r['target']+(' print_fix' if r.get('print_fix') else ''))
PY
python3 _sownb/vb/tools/g27_no_filename_weeks.py > /dev/null 2>&1 && echo "g27 PASS" || echo "g27 RED"
if ls Science_Teesside >/dev/null 2>&1 && git status --short | grep -q Science_Teesside; then python3 tools/downloads/verify_definitions.py > /dev/null 2>/tmp/vd.err && echo "verify_definitions PASS" || { echo "verify_definitions RED"; tail -1 /tmp/vd.err; }; fi
git status --short | grep -v "tools/rx3" | head -12
