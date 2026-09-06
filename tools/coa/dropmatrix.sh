#!/usr/bin/env bash
set -uo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"
TRANSFORMS="Y1a Y1b Y2 Y3 Y4a Y4b Y4c Y4d Y5d Y5e1"
LOCK="/tmp/$(basename "$PWD")-dropmatrix.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "another dropmatrix run holds $LOCK — refusing to interleave into the same evidence file"; exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

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
  # A transform whose sole removal leaves a build that does not run is
  # load-bearing, but the red measures the crash rather than the behaviour.
  # Label it rather than let a crash read as a behavioural control.
  # Test $changed, not the verdicts file. The verdicts file stores "ERR ERROR";
  # the arrow only exists in the diff string. Grepping the wrong one meant this
  # label could never fire — a gate that silently never runs, in the very code
  # written to record R0.11.
  case "$changed" in *'ERR->ERROR'*|*'C3c->REGRESSION'*) kind='LOAD-BEARING' ;; *) kind='watched     ' ;; esac
  if [ -z "$changed" ]; then printf '  %-6s UNWATCHED\n' "$T"; BAD=1; else printf '  %-6s %s %s\n' "$T" "$kind" "$changed"; fi
  rm -rf "drop_$T"
done
rm -rf staging && node build.mjs >/dev/null 2>&1
echo "LOAD-BEARING = its sole removal leaves a build that does not run. A real red,"
echo "but it measures the crash, not the behaviour."
echo; [ "$BAD" = 0 ] && echo "every transform has a gate that changes verdict without it" || echo "AT LEAST ONE TRANSFORM IS UNWATCHED"
exit "$BAD"
