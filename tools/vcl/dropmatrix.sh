#!/usr/bin/env bash
# Removal control. Rebuild without each transform in turn; the verdict set must
# change. Comparing against the BASELINE verdict set, not against the exit code:
# an exit code alone would call a transform "watched" whenever anything else was
# already red.
set -uo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"

TRANSFORMS="X1a X1b X1c X2a X2b X2c X2d X3a X3c X3d X3e X4 X5a X5b X6c X6d1 X6d2 X6d3"

verdicts() { grep -E '^[A-Z0-9][A-Za-z0-9 .@-]*[[:space:]]{2,}' "$1" | awk '{print $1, $NF}'; }

rm -rf staging && node build.mjs >/dev/null 2>&1 || { echo "baseline build failed"; exit 1; }
node controls.mjs > /tmp/vcl_baseline.out 2>&1
echo "baseline: $(tail -1 /tmp/vcl_baseline.out)"
verdicts /tmp/vcl_baseline.out > /tmp/vcl_baseline.verdicts
echo

BAD=0
for T in $TRANSFORMS; do
  rm -rf "drop_$T"
  if ! node build.mjs "--drop=$T" "--out=drop_$T" >/dev/null 2>&1; then
    printf '  %-6s BUILD FAILED\n' "$T"; BAD=1; continue
  fi
  VCL_STAGING="drop_$T" node controls.mjs > "/tmp/vcl_drop_$T.out" 2>&1
  code=$?
  if [ "$code" -gt 1 ] && ! grep -q '^id ' "/tmp/vcl_drop_$T.out"; then
    # the harness itself died — that is still the fix being load-bearing, but say so
    printf '  %-6s watched      harness aborted without it: %s\n' "$T" "$(grep -m1 -oE '(Error|error): .*' "/tmp/vcl_drop_$T.out" | head -c 90)"
    rm -rf "drop_$T"; continue
  fi
  verdicts "/tmp/vcl_drop_$T.out" > "/tmp/vcl_drop_$T.verdicts"
  changed=$(diff /tmp/vcl_baseline.verdicts "/tmp/vcl_drop_$T.verdicts" | grep '^>' | awk '{print $2"->"$3}' | tr '\n' ' ')
  # A transform whose sole removal leaves a page that THROWS is load-bearing,
  # but the red says the build did not run — it is not a measurement of the
  # behaviour the transform changes. Say which kind it is rather than letting a
  # crash read as a behavioural control.
  if grep -q 'ERR->ERROR' "/tmp/vcl_drop_$T.verdicts"; then kind='LOAD-BEARING'; else kind='watched     '; fi
  if [ -z "$changed" ]; then
    printf '  %-6s UNWATCHED    verdict set identical to baseline\n' "$T"; BAD=1
  else
    printf '  %-6s %s %s\n' "$T" "$kind" "$changed"
  fi
  rm -rf "drop_$T"
done

rm -rf staging && node build.mjs >/dev/null 2>&1
echo
echo "LOAD-BEARING = its sole removal leaves a build that does not run. A real red,"
echo "but it measures the crash, not the behaviour, so it is labelled rather than counted"
echo "as a behavioural control. Every other transform's removal was measured."
echo
[ "$BAD" = 0 ] && echo "every transform has a gate that changes verdict without it" \
              || echo "AT LEAST ONE TRANSFORM IS UNWATCHED"
exit "$BAD"
