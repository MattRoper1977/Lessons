#!/bin/bash
# usage: repin_education.sh <worktree> <new Site sha>   (moves the two publisher lines + caller digest)
set -euo pipefail
W=$1; NEW=$2; F=$W/.github/workflows/education-pages.yml; G=$W/tools/verify_cross_estate_unification.py
OLD=$(grep -o 'education-publication.yml@[0-9a-f]\{40\}' "$F" | cut -d@ -f2)
[ ${#NEW} -eq 40 ] || { echo "bad sha"; exit 1; }
sed -i "s/$OLD/$NEW/g" "$F"
grep -c "$NEW" "$F" | grep -qx 2 || { echo "expected exactly two pin lines"; exit 1; }
OLDD=$(grep -o 'PUBLICATION_CALLER_SHA256 = "[0-9a-f]\{64\}"' "$G" | grep -o '[0-9a-f]\{64\}')
NEWD=$(sha256sum "$F" | cut -d' ' -f1)
sed -i "s/$OLDD/$NEWD/" "$G"
echo "publisher $OLD -> $NEW ; caller digest $OLDD -> $NEWD"
git -C "$W" diff --stat
