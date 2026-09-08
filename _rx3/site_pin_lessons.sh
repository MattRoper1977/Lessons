#!/bin/bash
# usage: site_pin_lessons.sh <Site worktree> <new Lessons sha>   (P4.1: the Site's own Lessons pin, three workflow lines, nothing else)
set -euo pipefail
W=$1; NEW=$2; [ ${#NEW} -eq 40 ] || { echo "bad sha"; exit 1; }
FILES="$W/.github/workflows/domain-split-verify.yml $W/.github/workflows/education-publication.yml $W/.github/workflows/published-completion-verify.yml"
OLD=$(grep -ho 'ref: [0-9a-f]\{40\}' $W/.github/workflows/domain-split-verify.yml | grep -o '[0-9a-f]\{40\}' | head -1)
echo "Lessons pin $OLD -> $NEW"
n=0; for f in $FILES; do c=$(grep -c "$OLD" "$f"); n=$((n+c)); sed -i "s/$OLD/$NEW/g" "$f"; done
[ "$n" -eq 3 ] || { echo "expected exactly three pin lines, found $n"; exit 1; }
git -C "$W" diff --stat
[ "$(git -C "$W" diff --numstat | awk '{a+=$1;d+=$2} END{print a"/"d}')" = "3/3" ] || { echo "diff is not three lines"; exit 1; }
