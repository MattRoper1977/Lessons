#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SITE_ROOT="${SITE_ROOT:-$REPO_ROOT/.audit-site}"
AUDIT_OUTPUT="${AUDIT_OUTPUT:-$REPO_ROOT/audit-output}"
PUBLISHED_REF="${PUBLISHED_REF:-origin/main}"

if [[ ! -d "$SITE_ROOT" ]]; then
  printf 'Website checkout not found: %s\n' "$SITE_ROOT" >&2
  printf 'Clone MattRoper1977/mattroper1977.github.io there, or set SITE_ROOT.\n' >&2
  exit 2
fi

args=(
  --repo-root "$REPO_ROOT"
  --site-root "$SITE_ROOT"
  --output "$AUDIT_OUTPUT"
  --published-ref "$PUBLISHED_REF"
)

if [[ "${AUDIT_BROWSER:-1}" != "0" ]]; then
  args+=(--browser)
fi
if [[ "${AUDIT_LIVE:-1}" != "0" ]]; then
  args+=(--live)
fi
if [[ -n "${AUDIT_BROWSER_MODES:-}" ]]; then
  args+=(--browser-modes "$AUDIT_BROWSER_MODES")
fi

exec python3 "$SCRIPT_DIR/estate_audit.py" "${args[@]}"
