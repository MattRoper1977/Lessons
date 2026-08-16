#!/usr/bin/env bash
# tools/fieldops/run.sh — rebuild staging/ from release/ and run every gate.
#
#   tools/fieldops/run.sh            build + all gates
#   tools/fieldops/run.sh --drops    also run the removal matrix (slow, ~13 rebuilds)
#
# Exit codes, and they are not interchangeable:
#   0  everything green
#   1  a gate failed, or a regression was measured
#   2  a subject was unreachable — INCONCLUSIVE, never treated as a pass
#   3  patch-scoped gates green, a pre-existing red recorded and left
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
# Severity is NOT the numeric order of the codes: 1 outranks 2 outranks 3.
# Taking a numeric max reported "pre-existing red" as the headline while a
# measured regression sat underneath it.
rank() { case "$1" in 1) echo 3;; 2) echo 2;; 3) echo 1;; *) echo 0;; esac; }
WORST=0
bump() { [ "$(rank "$1")" -gt "$(rank "$WORST")" ] && WORST="$1"; return 0; }

hdr() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

hdr "build  release/ -> staging/"
node build.mjs || { echo "BUILD FAILED"; exit 1; }

hdr "controls  every fix red on release, green on staging"
node controls.mjs; bump $?

hdr "assert-unchanged  nothing moved outside the declared transforms"
node assert_unchanged.mjs; bump $?

hdr "P2.6  the 38 inputs"
node p26_inputs.mjs; bump $?

hdr "transport  Studio <-> lab, all four splits, both directions"
node transport.mjs; bump $?

if [ "${1:-}" = "--drops" ]; then
  hdr "removal matrix  drop each transform, the gates must notice"
  ./dropmatrix.sh; bump $?
fi

printf '\n\033[1m== worst exit: %s\033[0m\n' "$WORST"
exit "$WORST"
