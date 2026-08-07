#!/usr/bin/env bash
# Runs every Glitch Clash suite against the shipped file.
#
#   tools/glitchclash/run.sh                     # the game in this repo
#   tools/glitchclash/run.sh path/to/copy.html   # any other copy
#
# Needs Playwright. If Chromium lives somewhere non-standard, point at it:
#   CHROMIUM_PATH=/opt/pw-browsers/chromium/chrome-linux/chrome tools/glitchclash/run.sh
#
# Exits non-zero if any suite fails, so it works as a gate.
set -uo pipefail
cd "$(dirname "$0")"
TARGET="${1:-}"

# Playwright is commonly installed globally, and node does not look there on
# its own. Add the global root to NODE_PATH rather than making every developer
# npm-install into this repo.
if ! node -e "require.resolve('playwright')" 2>/dev/null; then
  GROOT="$(npm root -g 2>/dev/null || true)"
  if [ -n "$GROOT" ] && [ -d "$GROOT/playwright" ]; then
    export NODE_PATH="${NODE_PATH:-}${NODE_PATH:+:}$GROOT"
  else
    echo "playwright not found. Install it with:  npm i -g playwright" >&2
    exit 2
  fi
fi

fail=0
for t in gc gc-endless gc-mods gc-clock gc-weekly gc-fx gc-music gc-cb gc-hc gc-a11y gc-league; do
  printf '%-22s ' "$t"
  out=$(node "$t.test.js" $TARGET 2>&1)
  last=$(printf '%s\n' "$out" | tail -1)
  if printf '%s\n' "$out" | grep -qE 'FAILED|Error'; then
    fail=1
    echo "FAIL"
    printf '%s\n' "$out" | grep -E '  FAIL|Error' | head -5 | sed 's/^/    /'
  else
    echo "$last"
  fi
done
echo
if [ "$fail" -ne 0 ]; then echo "SUITES FAILED"; exit 1; fi
echo "ALL GLITCH CLASH SUITES PASSED"
