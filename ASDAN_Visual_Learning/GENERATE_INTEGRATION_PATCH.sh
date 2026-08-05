#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-.}"
OUT="${2:-/tmp/asdan-visual-source-integration.patch}"
REPORT="${3:-/tmp/asdan-visual-source-integration.json}"

python3 "$REPO/ASDAN_Visual_Learning/build_payloads.py" --check
python3 "$REPO/ASDAN_Visual_Learning/check.py"

python3 "$REPO/ASDAN_Visual_Learning/integrate.py" \
  --repo "$REPO" \
  --patch-out "$OUT" \
  --json-report "$REPORT"

git -C "$REPO" apply --stat "$OUT"
git -C "$REPO" apply --check "$OUT"

printf '\nExact source integration patch is ready at:\n  %s\n' "$OUT"
printf 'No file was committed, pushed or merged.\n'
