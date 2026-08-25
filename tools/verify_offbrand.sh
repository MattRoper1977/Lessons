#!/usr/bin/env bash
#
# verify_offbrand.sh — deploy gates + safeguarding contract for Games/Off_Brand.html
#
# Encodes the Off-Brand deploy gates as repo automation so no future change can
# silently regress them — in particular the SAFEGUARDING CONTRACT: the public,
# indexed game file must never carry a child's age, home city, or other
# identifying details.
#
# Usage:   tools/verify_offbrand.sh [path-to-html]
#          (defaults to <repo>/Games/Off_Brand.html)
#
# Exits 0 if every gate passes; non-zero with a clear message on the first
# failure. Uses node + standard POSIX tools only — no third-party dependencies.

set -euo pipefail

# --- locate the target ------------------------------------------------------
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-$ROOT/Games/Off_Brand.html}"

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "  ok  $*"; }

[ -f "$TARGET" ] || fail "target not found: $TARGET"
command -v node >/dev/null 2>&1 || fail "node is required but not on PATH"

echo "verify_offbrand: checking $TARGET"

# --- temp workspace ---------------------------------------------------------
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# ===========================================================================
# 1 · SYNTAX — node --check every inline <script> block
#     (external `src` blocks have no inline body; importmap blocks are JSON)
# ===========================================================================
COUNT="$(node - "$TARGET" "$TMP" <<'NODE'
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const outDir = process.argv[3];
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m, i = 0;
while ((m = re.exec(html))) {
  const attrs = m[1] || '';
  if (/\bsrc\s*=/i.test(attrs)) continue;                       // external
  if (/type\s*=\s*["']?importmap["']?/i.test(attrs)) continue;  // JSON, not JS
  fs.writeFileSync(outDir + '/block_' + i + '.js', m[2]);
  i++;
}
process.stdout.write(String(i));
NODE
)"

[ "$COUNT" -ge 1 ] || fail "no inline <script> blocks found — file looks wrong"
for b in "$TMP"/block_*.js; do
  node --check "$b" || fail "syntax error in inline <script> block: $(basename "$b")"
done
ok "syntax: $COUNT inline script block(s) pass node --check"

# ===========================================================================
# 2 · IDENTITY MARKERS
# ===========================================================================
grep -qE "GAME_VERSION='[0-9]" "$TARGET" || fail "identity: GAME_VERSION marker missing (or not a digit version)"
for pat in \
  "niece Clara" \
  "suggested by Clara" \
  "PARADE=CAST.concat([CLARA])" \
  "id:'g_clara'" ; do
  grep -qF -- "$pat" "$TARGET" || fail "identity marker missing: $pat"
done
ok "identity markers present (version, dedication, credit, parade, guide entry)"

# ===========================================================================
# 3 · SAFEGUARDING CONTRACT — no identifying details on the public file
# ===========================================================================
grep -iqE 'years? old' "$TARGET" && fail "safeguarding: file contains an age ('years old')" || true
grep -iqwF 'London'    "$TARGET" && fail "safeguarding: file contains the city 'London'"    || true
grep -iqwE 'address|birthday' "$TARGET" && fail "safeguarding: file contains 'address'/'birthday'" || true

# No written-out child age *inside the g_clara guide entry text*
# (a whole-file search would false-match 'listen', 'height', etc.)
GCLARA="$(grep -oE "\{id:'g_clara'[^}]*\}" "$TARGET" || true)"
# Herestring, not a pipe: a printf that died of a broken pipe would make this
# safeguarding check pass without having read the entry.
if [ -z "$GCLARA" ]; then
  # An entry that was never found cannot be clean. Saying "clean" here would be
  # a safeguarding claim about text nobody read.
  fail "safeguarding: MEASUREMENT INVALID - no g_clara entry found to check"
elif grep -iqwE 'eight|nine|ten|eleven|twelve' <<<"$GCLARA"; then
  fail "safeguarding: g_clara entry contains a written-out age"
fi
ok "safeguarding: no age / city / address / birthday; g_clara entry clean"

# ===========================================================================
# 4 · HOUSE PROMISES — offline-first, Made-by-Matt-only, gentle vocabulary
# ===========================================================================
grep -qF 'fetch('        "$TARGET" && fail "house: fetch( present (must stay offline)"      || true
grep -qF 'XMLHttpRequest' "$TARGET" && fail "house: XMLHttpRequest present"                  || true
grep -qF 'WebSocket'     "$TARGET" && fail "house: WebSocket present"                        || true
grep -iqE '<script[^>]*\bsrc=' "$TARGET" && fail "house: external <script src> present"      || true
grep -qF 'new Audio'     "$TARGET" && fail "house: new Audio present (no network/audio deps)" || true
grep -qF 'AudioContext'  "$TARGET" && fail "house: AudioContext present"                     || true

# Gentle vocabulary: no elimination language. Match the phrase 'vote out'
# literally so the cherished tribute line 'nobody here is ever voted out' passes.
grep -iqF 'vote out' "$TARGET" && fail "house: 'vote out' vocabulary present" || true
grep -iqE '\b(kill|eject)' "$TARGET" && fail "house: 'kill'/'eject' vocabulary present" || true

# The only localStorage key literal must be mbm_offbrand
KEYS="$( { grep -oE "localStorage\.(getItem|setItem|removeItem)\(\s*'[^']*'" "$TARGET" | grep -oE "'[^']*'$" || true
           grep -oE "localStorage\[\s*'[^']*'\s*\]" "$TARGET" | grep -oE "'[^']*'" || true ; } \
        | tr -d "'" | sort -u )"
[ -n "$KEYS" ] || fail "house: no localStorage key literal found"
while IFS= read -r k; do
  [ "$k" = "mbm_offbrand" ] || fail "house: unexpected localStorage key literal: '$k'"
done <<< "$KEYS"
ok "house: offline-first, gentle vocabulary, single save key 'mbm_offbrand'"

# ===========================================================================
# 5 · STRUCTURE — well-formed and sane size
# ===========================================================================
LAST="$(tr -d '[:space:]' < "$TARGET" | tail -c 7)"
[ "$LAST" = "</html>" ] || fail "structure: file does not end with </html> (got '$LAST')"

BYTES="$(wc -c < "$TARGET")"
[ "$BYTES" -ge 80000 ]  || fail "structure: file too small ($BYTES bytes) — truncated commit?"
[ "$BYTES" -le 400000 ] || fail "structure: file too large ($BYTES bytes) — runaway commit?"
ok "structure: ends with </html>, size $BYTES bytes (80k-400k)"

echo "PASS: all Off-Brand verification gates satisfied"
