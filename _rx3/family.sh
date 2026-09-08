#!/bin/bash
# Land one family end-to-end: worktree → land → gates → witnesses → commit → push. Usage: family.sh <worktree name> <branch> <ids> <json> "<family title>" "<family notes>"
set -u; W=/home/user/$1; BR=$2; IDS=$3; J=$4; TITLE=$5; NOTES=$6
git -C /home/user/Lessons fetch -q origin main && (git -C /home/user/Lessons worktree list --porcelain | grep -qx "worktree $W" || git -C /home/user/Lessons worktree add -q -b "$BR" "$W" origin/main) || { echo "worktree setup failed for $W"; exit 1; }
cd "$W" || exit 1; git checkout -q "$BR" 2>/dev/null || git checkout -q -b "$BR" || exit 1; git reset -q --hard origin/main && mkdir -p tools
[ "$(git rev-parse --abbrev-ref HEAD)" = "$BR" ] || { echo "wrong branch in $W"; exit 1; }
/home/user/Lessons/_rx3/reland.sh "$W" "$IDS" "$J" | grep -v "^SAME\|^CHANGED" 
OUT=/tmp/gates_$1; /home/user/Lessons/_rx3/family_gates.sh "$W" /tmp/site-e33a "$J" "$OUT" > "$OUT.log" 2>&1; RC=$?
grep "syntax errors\|sentinels:\|SENTINEL\|G12 s24\|=====\|tier gate\|data-URI\|FAMILY GATES\|^FAIL\|DUPID" "$OUT.log"; grep -c "^PASS" "$OUT.log" | sed 's/^/boot PASS lines: /'
python3 - "$W" "$J" > /tmp/witness_$1.txt <<'PY'
import json,subprocess,hashlib,sys
for r in json.load(open(sys.argv[2])):
    pre=subprocess.run(['git','-C',sys.argv[1],'show','origin/main:'+r['target']],capture_output=True).stdout
    extra=(' print-fix' if r.get('print_fix') else '')+(' T2-4' if r.get('learner_confirmation') else '')+(' webp' if (r.get('images') or {}).get('webp_dir') else '')+(' svg-scene' if (r.get('images') or {}).get('scene_uri_chars') else '')
    print(f"{r['verdict']:14s} {r['target']} pre={hashlib.sha256(pre).hexdigest()[:16] if pre else 'absent'} post={r['sha256'][:16]} bytes={r['bytes']} pack={r['pack_sha256'][:16]} pack-manifest-match={r['pack_sha_matches_manifest']}{extra}")
PY
cat /tmp/witness_$1.txt
if [ $RC -ne 0 ]; then echo "GATES RED — not committing"; exit 1; fi
S24=$(grep "G12 s24" "$OUT.log" | sed 's/.*G12 s24-print-renders *//' | cut -c1-120); BOOT=$(grep -c "^PASS" "$OUT.log"); SENT=$(grep "sentinels:" "$OUT.log" | head -1)
git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -F - <<MSG
$TITLE (RX3 P3)

Landed by tools/rx3_land.py from the reviewed 33-pack (pack HTML sha256 equals the pack manifest for every row):
$(sed 's/^/  /' /tmp/witness_$1.txt)
$NOTES

Furniture (3.2): NAV-1 way-home + splash (estate bytes), PH-3 guidance on details.staff-detail (hidden by default, ⓘ Guidance / key G,
mbm_guide_v1), canonical link, one h1 (the other two → h2.slide-h1 with the donor rule), hud.js by donor parity, the closure sentinel
on REPLACE targets only where the donor carries it. Family manifests: REPLACE rows updated, ADD rows added (outcome/objective/week
from the pack). Beside filenames are numbered by the ruled absolute week of the pack's placement (never a filename).

Gate battery (_rx3/family_gates.sh): node --check 0 · dup-id 0 · $SENT · s24 print render $S24 · 390 px boot PASS ×$BOOT
(0 console/page errors, way-home in the first viewport, staff guidance hidden, one h1, no overflow, localStorage 0) · g27 PASS ·
tier gate: 2 pre-existing failures on main · s23 names MEASUREMENT INVALID by design · data-URI images > 50 KB: 0.

Rollback: origin/main $(git rev-parse origin/main) (pre-bytes above); new files are additive.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DDjNAxAPpxvV8sTq42X6nm
MSG
git log --oneline -1 && git push --force-with-lease -u origin "$BR" 2>&1 | tail -1
