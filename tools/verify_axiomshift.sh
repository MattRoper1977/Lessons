#!/usr/bin/env bash
# Axiom Shift server-side gate. Runs the Node harness (solvability, determinism,
# Daily sweep, §5 contract, render smoke) against the built file, then a
# node --check on the extracted <script>. Fails the build on any red.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/.." && pwd)"
file="${1:-$root/Games/Axiom_Shift.html}"

echo "Verifying: $file"
[ -f "$file" ] || { echo "missing file: $file"; exit 2; }

# structural sanity (NOT a version prefix — stays green across version bumps)
grep -q 'AXIOM SHIFT — SIM CORE (BEGIN)' "$file" || { echo "sim core marker missing"; exit 2; }
grep -q "mbm_axiomshift" "$file" || { echo "save key missing"; exit 2; }

# node --check every inline <script> block.
#
# This used to slice once, from the FIRST <script> to the LAST </script>, and
# call the result "the extracted script". That is not an extraction, it is a
# guess that the file contains exactly one block: the moment a second one
# appears, the slice swallows the closing tag of the first and node --check
# reports SyntaxError: Unexpected token '<' — blaming the game for a fault in
# the reader. The gate was anchored on a position any tag moves.
#
# It now walks the blocks the way verify_charcoal.sh and verify_offbrand.sh
# already do, so it judges what it says it judges. Axiom Shift carries a second
# block from 2026-08-10: the stamped inline exit region, so a child on a
# locked-down school device has a way out of the page.
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
count="$(node -e '
const fs=require("fs");
const h=fs.readFileSync(process.argv[1],"utf8");
const re=/<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m,n=0;
while((m=re.exec(h))!==null){
  if(/\bsrc\s*=/i.test(m[1]))continue;      // nothing to check in an external ref
  fs.writeFileSync(process.argv[2]+"/block"+(n++)+".js",m[2]);
}
process.stdout.write(String(n));
' "$file" "$tmp")"
[ "$count" -ge 1 ] || { echo "no inline <script> blocks found — file looks wrong"; exit 2; }
for b in "$tmp"/block*.js; do
  node --check "$b" || { echo "syntax error in inline <script> block: $(basename "$b")"; exit 1; }
done
echo "node --check: OK ($count inline script block(s))"

# full harness (x3 for stochastic safety — this sim is deterministic, so all
# three runs must agree; a flake here is a real fault, not noise)
for i in 1 2 3; do
  echo "--- harness pass $i ---"
  node "$here/verify_axiomshift.js" "$file"
done
echo "verify_axiomshift: ALL GREEN"
