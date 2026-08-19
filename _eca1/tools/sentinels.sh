#!/bin/sh
# ECA-1 sentinel derivation: sorted sets, counts must hold at 50/123 and be set-identical.
cd "$(git rev-parse --show-toplevel)"
git grep -l 'll-g:loop-mark' -- '*.html' | sort > _eca1/tables/sentinel_loopmark.now
git grep -l 'What I said, and what it changed' -- '*.html' | sort > _eca1/tables/sentinel_closure.now
LM=$(wc -l < _eca1/tables/sentinel_loopmark.now)
CL=$(wc -l < _eca1/tables/sentinel_closure.now)
echo "loop-mark files: $LM  closure files: $CL"
if [ -f _eca1/tables/sentinel_loopmark.base ]; then
  diff _eca1/tables/sentinel_loopmark.base _eca1/tables/sentinel_loopmark.now > /dev/null || { echo "SENTINEL SET DRIFT: loop-mark"; exit 1; }
  diff _eca1/tables/sentinel_closure.base _eca1/tables/sentinel_closure.now > /dev/null || { echo "SENTINEL SET DRIFT: closure"; exit 1; }
  echo "sentinels: set-identical to base"
fi
[ "$LM" = "50" ] && [ "$CL" = "123" ] && echo "sentinels: counts hold 50/123" || { echo "SENTINEL COUNT WRONG"; exit 1; }
