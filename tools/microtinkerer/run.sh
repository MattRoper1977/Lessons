#!/usr/bin/env bash
# Micro-Tinkerer PWA gate.
#   tools/microtinkerer/run.sh                       # finds a sibling site checkout
#   tools/microtinkerer/run.sh /path/to/site-repo    # or point at one
# Exits non-zero on findings, 3 if it could not get into a position to judge.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SITE="${1:-${MBM_SITE_ROOT:-}}"
cd "$ROOT"
node -e "require.resolve('playwright')" 2>/dev/null || npm i --no-save playwright@1.49.1 >/dev/null
if [ -n "$SITE" ]; then exec node tools/microtinkerer/verify_pwa.mjs --site "$SITE"; fi
exec node tools/microtinkerer/verify_pwa.mjs
