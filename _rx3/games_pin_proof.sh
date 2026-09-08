#!/bin/bash
# RX3 P4.3: build the Play tree at the CURRENT pin tuple and at the PROPOSED tuple exactly as Games' pin-release.yml does,
# then report payloads, missing/external refs, shelf identity and the payload byte-sets that move.
# usage: games_pin_proof.sh <games checkout> <site before> <lessons before> <site after> <lessons after> <workdir>
set -euo pipefail
G=$1; SB=$2; LB=$3; SA=$4; LA=$5; W=$6; mkdir -p "$W"
co(){ # <repo url> <sha> <dir>
  [ -d "$3/.git" ] || git clone -q "$1" "$3"; git -C "$3" fetch -q origin "$2" 2>/dev/null || git -C "$3" fetch -q origin; git -C "$3" checkout -q --detach "$2"; }
co https://github.com/MattRoper1977/mattroper1977.github.io "$SB" "$W/before/Site"; co https://github.com/MattRoper1977/Lessons "$LB" "$W/before/Lessons"
co https://github.com/MattRoper1977/mattroper1977.github.io "$SA" "$W/after/Site";  co https://github.com/MattRoper1977/Lessons "$LA" "$W/after/Lessons"
python3 "$W/before/Site/domain-split/build_publications.py" --lessons "$W/before/Lessons" --output "$W/before/out" > "$W/before.json"
python3 "$W/after/Site/domain-split/build_publications.py"  --lessons "$W/after/Lessons"  --output "$W/after/out"  > "$W/after.json"
python3 - "$G" "$W" <<'PY'
import json,sys,hashlib,pathlib
G,W=pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2])
a=json.loads((W/'after/out/build-report.json').read_text()); b=json.loads((W/'before/out/build-report.json').read_text())
print('after build:', json.loads((W/'after.json').read_text())['counts'])
print('before build:', json.loads((W/'before.json').read_text())['counts'])
print('shelf identical to games.json:', (W/'after/out/games/games.json').read_bytes()==(G/'games.json').read_bytes())
B={p['path']:p['published_sha256'] for p in b['payloads']}; A={p['path']:p['published_sha256'] for p in a['payloads']}
moved=sorted(k for k in A if B.get(k)!=A[k]); print('payloads', len(A), 'moved', len(moved))
for k in moved: print('  moved', k, (B.get(k) or 'absent')[:12], '->', A[k][:12])
lum=[p for p in a['payloads'] if p['path'].endswith('/Lessons/Games/Lumins.html') or p['path'].endswith('Lumins.html')]
for p in lum: print('Lumins payload', p['path'], 'published_sha256', p['published_sha256'])
same=sorted(k for k in A if B.get(k)==A[k]); print('unchanged payloads', len(same))
PY
