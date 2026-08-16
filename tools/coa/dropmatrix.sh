#!/usr/bin/env bash
set -uo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"
TRANSFORMS="Y1a Y1b Y2 Y3 Y4a Y4b Y4c Y4d Y5d Y5e1"
verdicts() { grep -E '^[A-Z0-9][A-Za-z0-9.-]*[[:space:]]{2,}' "$1" | awk '{print $1, $NF}'; }
rm -rf staging && node build.mjs >/dev/null 2>&1 || { echo "baseline build failed"; exit 1; }
node controls.mjs > /tmp/coa_baseline.out 2>&1
echo "baseline: $(tail -1 /tmp/coa_baseline.out)"; verdicts /tmp/coa_baseline.out > /tmp/coa_base.v; echo
BAD=0
for T in $TRANSFORMS; do
  rm -rf "drop_$T"
  if ! node build.mjs "--drop=$T" "--out=drop_$T" >/dev/null 2>&1; then printf '  %-6s BUILD FAILED\n' "$T"; BAD=1; continue; fi
  COA_STAGING="drop_$T" node controls.mjs > "/tmp/coa_drop_$T.out" 2>&1
  verdicts "/tmp/coa_drop_$T.out" > "/tmp/coa_drop_$T.v"
  changed=$(diff /tmp/coa_base.v "/tmp/coa_drop_$T.v" | grep '^>' | awk '{print $2"->"$3}' | tr '\n' ' ')
  if [ -z "$changed" ]; then printf '  %-6s UNWATCHED\n' "$T"; BAD=1; else printf '  %-6s watched      %s\n' "$T" "$changed"; fi
  rm -rf "drop_$T"
done
rm -rf staging && node build.mjs >/dev/null 2>&1
echo; [ "$BAD" = 0 ] && echo "every transform has a gate that changes verdict without it" || echo "AT LEAST ONE TRANSFORM IS UNWATCHED"
exit "$BAD"
