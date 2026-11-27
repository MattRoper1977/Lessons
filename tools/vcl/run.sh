#!/usr/bin/env bash
# tools/vcl/run.sh — rebuild staging/ from release/ and run every gate.
#   run.sh            build + controls + assert-unchanged
#   run.sh --drops    also run the removal matrix (19 rebuilds, slow)
set -uo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"
rank() { case "$1" in 1) echo 3;; 2) echo 2;; 3) echo 1;; *) echo 0;; esac; }
WORST=0
bump() { [ "$(rank "$1")" -gt "$(rank "$WORST")" ] && WORST="$1"; return 0; }
hdr() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

hdr "build  release/ -> staging/"
node build.mjs || { echo BUILD FAILED; exit 1; }
hdr "controls  every fix red on release, green on staging"
node controls.mjs; bump $?
hdr "assert-unchanged  the V0 freeze held"
node assert_unchanged.mjs; bump $?
if [ "${1:-}" = "--drops" ]; then
  hdr "removal matrix  drop each transform, the gates must notice"
  ./dropmatrix.sh; bump $?
fi
printf '\n\033[1m== worst exit: %s\033[0m\n' "$WORST"
exit "$WORST"
