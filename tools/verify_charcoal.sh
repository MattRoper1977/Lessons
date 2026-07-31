#!/usr/bin/env bash
#
# verify_charcoal.sh — deploy gates + safeguarding contract for Games/Charcoal.html
#
# Encodes the Charcoal deploy gates as repo automation so no future change can
# silently regress them — in particular the SAFEGUARDING CONTRACT: the public,
# indexed game file must never carry a child's age, home city, school, address,
# birthday or surname.
#
# It also guards the CARRIED TRAP the whole game is built to avoid: the witness
# check must take TWO exclusions (the actor AND the target). Off-Brand shipped a
# one-exclusion version that made the antagonist a no-op for three releases. That
# marker is anchored to the function signature itself, so it cannot pass if the
# fix is reverted.
#
# Usage:   tools/verify_charcoal.sh [path-to-html]
#          (defaults to <repo>/Games/Charcoal.html)
#
# Exits 0 if every gate passes; non-zero with a clear message on the first
# failure. Uses node + standard POSIX tools only — no third-party dependencies.

set -euo pipefail

# --- locate the target ------------------------------------------------------
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-$ROOT/Games/Charcoal.html}"

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "  ok  $*"; }

[ -f "$TARGET" ] || fail "target not found: $TARGET"
command -v node >/dev/null 2>&1 || fail "node is required but not on PATH"

echo "verify_charcoal: checking $TARGET"

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
#     Anchored to things that cannot survive deletion of what they guard:
#       - the two-exclusion witness signature IS the carried-trap fix
#       - PARADE=CAST.concat([CLARA]) is the only way Clara joins the parade
#         yet stays out of the round cast
#       - the version marker matches any leading digit, so it survives a
#         major bump (Off-Brand's was pinned to '3.' and would break at v4)
# ===========================================================================
grep -qE "GAME_VERSION='[0-9]" "$TARGET" || fail "identity: GAME_VERSION marker missing (or not a digit version)"
for pat in \
  "function witnesses(p,exclActor,exclTarget)" \
  "niece Clara" \
  "PARADE=CAST.concat([CLARA])" \
  "was her call" \
  "Clara ♥" ; do
  grep -qF -- "$pat" "$TARGET" || fail "identity marker missing: $pat"
done
ok "identity markers present (version, two-exclusion witness, dedication, parade, credit, nameplate)"

# ===========================================================================
# 3 · SAFEGUARDING CONTRACT — no identifying details on the public file
# ===========================================================================
grep -iqE 'years? old' "$TARGET" && fail "safeguarding: file contains an age ('years old')" || true
grep -iqwF 'London'    "$TARGET" && fail "safeguarding: file contains the city 'London'"    || true
grep -iqwE 'address|birthday|surname' "$TARGET" && fail "safeguarding: file contains 'address'/'birthday'/'surname'" || true
grep -iqwF 'school'    "$TARGET" && fail "safeguarding: file contains 'school'"              || true

# No written-out child age anywhere in the file (whole words only, so 'listen',
# 'often', 'tenth' etc. never false-match).
if grep -iqwE 'eight|nine|ten|eleven|twelve' "$TARGET"; then
  fail "safeguarding: file contains a written-out age word"
fi
# No surname following the first name.
grep -qE 'Clara [A-Z][a-z]' "$TARGET" && fail "safeguarding: a capitalised word follows 'Clara' (possible surname)" || true
ok "safeguarding: no age / city / school / address / birthday / surname; first name only"

# ===========================================================================
# 4 · HOUSE PROMISES — offline, no audio, Made-by-Matt-only, gentle vocabulary
# ===========================================================================
grep -qF 'fetch('        "$TARGET" && fail "house: fetch( present (must stay offline)"        || true
grep -qF 'XMLHttpRequest' "$TARGET" && fail "house: XMLHttpRequest present"                    || true
grep -qF 'WebSocket'     "$TARGET" && fail "house: WebSocket present"                          || true
grep -iqE '<script[^>]*\bsrc=' "$TARGET" && fail "house: external <script src> present"        || true
grep -qF 'new Audio'     "$TARGET" && fail "house: new Audio present (this game ships no audio)" || true
grep -qF 'AudioContext'  "$TARGET" && fail "house: AudioContext present"                       || true
grep -iqE '<audio\b'     "$TARGET" && fail "house: <audio> element present"                    || true

# Gentle vocabulary: no elimination / harm language.
grep -iqE 'voted? out' "$TARGET" && fail "house: 'vote out'/'voted out' vocabulary present" || true
grep -iqE '\b(kill|killed|murder|murderer|dead|death|die|died|dies|corpse|stab|shoot|shot|gun|knife|weapon|eject|ejected|eliminate|eliminated)\b' "$TARGET" \
  && fail "house: harm/elimination vocabulary present" || true
ok "house: offline, no audio, gentle vocabulary"

# The only localStorage key literal must be mbm_charcoal
KEYS="$( { grep -oE "localStorage\.(getItem|setItem|removeItem)\(\s*'[^']*'" "$TARGET" | grep -oE "'[^']*'$" || true
           grep -oE "localStorage\[\s*'[^']*'\s*\]" "$TARGET" | grep -oE "'[^']*'" || true ; } \
        | tr -d "'" | sort -u )"
[ -n "$KEYS" ] || fail "house: no localStorage key literal found"
while IFS= read -r k; do
  [ "$k" = "mbm_charcoal" ] || fail "house: unexpected localStorage key literal: '$k'"
done <<< "$KEYS"
ok "house: single save key 'mbm_charcoal'"

# ===========================================================================
# 5 · STRUCTURE — well-formed and sane size
# ===========================================================================
LAST="$(tr -d '[:space:]' < "$TARGET" | tail -c 7)"
[ "$LAST" = "</html>" ] || fail "structure: file does not end with </html> (got '$LAST')"

BYTES="$(wc -c < "$TARGET")"
[ "$BYTES" -ge 80000 ]  || fail "structure: file too small ($BYTES bytes) — truncated commit?"
[ "$BYTES" -le 400000 ] || fail "structure: file too large ($BYTES bytes) — runaway commit?"
ok "structure: ends with </html>, size $BYTES bytes (80k-400k)"

echo "PASS: all Charcoal verification gates satisfied"
