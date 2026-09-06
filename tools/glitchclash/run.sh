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
  rc=0
  out=$(node "$t.test.js" $TARGET 2>&1) || rc=$?
  last=$(printf '%s\n' "$out" | tail -1)
  # A suite that was KILLED - OOM, a timeout, a runner losing the process -
  # prints nothing, matches neither FAILED nor Error, and would take the else
  # branch below and be read as passing. The exit status is the only thing that
  # knows, so it is read.
  if [ "$rc" -ne 0 ] && ! grep -qE 'FAILED|Error' <<<"$out"; then
    fail=1
    echo "DIED (exit $rc, no verdict printed)"
    continue
  fi
  # `printf … | grep -q` under pipefail goes non-zero when printf dies of a
  # broken pipe - and non-zero here takes the ELSE branch, so a suite that
  # FAILED prints its last line and reads as passing. This runner is the gate
  # CLAUDE.md tells everyone to run before saying a change works; a false green
  # in it is the expensive kind. Herestrings: a file, never a live pipe.
  if grep -qE 'FAILED|Error' <<<"$out"; then
    fail=1
    echo "FAIL"
    hits="$(grep -E '  FAIL|Error' <<<"$out" || true)"
    sed 's/^/    /' <<<"$(head -5 <<<"$hits")"
  else
    echo "$last"
  fi
done
echo
if [ "$fail" -ne 0 ]; then echo "SUITES FAILED"; exit 1; fi
echo "ALL GLITCH CLASH SUITES PASSED"
