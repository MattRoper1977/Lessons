#!/usr/bin/env bash
# Removal control. For each transform, rebuild WITHOUT it and re-run the whole
# control set. A transform is WATCHED only if dropping it changes the verdict
# set against the baseline. Exit code alone is not enough: the baseline already
# exits 2 (one unreachable), so "exit != 0" would have called every transform
# watched, including three that nothing was watching at all.
set -uo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"
mkdir -p work

verdicts() { grep -E '^[A-Z0-9][A-Za-z0-9.-]*[[:space:]]' "$1" | awk '{print $1, $NF}'; }

rm -rf staging && node build.mjs >/dev/null 2>&1 || { echo "baseline build failed"; exit 1; }
node controls.mjs > work/baseline.out 2>&1
echo "baseline: $(tail -1 work/baseline.out)"
verdicts work/baseline.out > work/baseline.verdicts
echo

BAD=0
for T in T1 T2 T3 T4 T5a T5b T6a T6b T7 T8a T8b T8c T9; do
  rm -rf "drop_$T"
  node build.mjs "--drop=$T" "--out=drop_$T" >/dev/null 2>&1 || { printf '  %-5s BUILD FAILED\n' "$T"; BAD=1; continue; }
  P2_PATCHED="drop_$T" node controls.mjs > "work/drop_$T.out" 2>&1
  verdicts "work/drop_$T.out" > "work/drop_$T.verdicts"
  changed=$(diff work/baseline.verdicts "work/drop_$T.verdicts" | grep '^>' | awk '{print $2"->"$3}' | tr '\n' ' ')
  if [ -z "$changed" ]; then
    printf '  %-5s UNWATCHED    verdict set identical to baseline\n' "$T"; BAD=1
  else
    printf '  %-5s watched      %s\n' "$T" "$changed"
  fi
  rm -rf "drop_$T"
done

rm -rf staging && node build.mjs >/dev/null 2>&1
echo
[ "$BAD" = 0 ] && echo "every transform has a gate that changes verdict without it" \
              || echo "AT LEAST ONE TRANSFORM IS UNWATCHED"
exit "$BAD"
