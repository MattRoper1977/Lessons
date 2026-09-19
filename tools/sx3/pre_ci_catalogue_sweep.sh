#!/usr/bin/env bash
# Pre-CI sweep: the four DERIVED RECORDS that every resources.json row must
# appear in. Adding a catalogue row without updating all four is the defect
# SX3 3b hit four separate times -- four separate reds, each found only in CI:
#
#   TERM_AND_STYLE_EVIDENCE   check_catalogue_static.py
#   CATALOGUE_PINS            pin_catalogue_contract.py   (GLV3 admits a
#                             protected ADDITION only via this pin)
#   data/resource-sizes.json  tools/ux2/resource_sizes.py
#   PIN1 trigger list         tools/pin1/derive_triggers.py
#
# They are one class: a derived record keyed on the catalogue. Run this before
# any push that adds or removes a catalogue row. Each writer has a --write;
# regenerate with it, never hand-edit.
set -uo pipefail
PY="${PY:-/tmp/pubvenv/bin/python3}"
cd "$(dirname "$0")/../.."
fail=0
run() {
  local name="$1"; shift
  printf '  %-48s ' "$name"
  if out=$("$@" 2>&1); then echo "PASS"; else
    echo "FAIL"; echo "$out" | tail -3 | sed 's/^/        /'; fail=1
  fi
}
echo "Pre-CI catalogue sweep - the four derived records"
run "TERM_AND_STYLE_EVIDENCE (check_catalogue_static)" "$PY" tools/catalogue/check_catalogue_static.py
run "CATALOGUE_PINS (pin_catalogue_contract --check)"  "$PY" tools/catalogue/pin_catalogue_contract.py --lessons . --apps "${APPS:-/home/user/matt-s-apps-}" --check
run "data/resource-sizes.json (resource_sizes --check)" "$PY" tools/ux2/resource_sizes.py --check
run "PIN1 trigger list (derive_triggers --check)"       "$PY" tools/pin1/derive_triggers.py --check
# L23 tail: data/resource-sizes.json is a PUBLISHED derived record. When any published
# record moved, the Site admission registry must admit the new digest BEFORE the build
# that supplies pairs is taken (regenerate, THEN build, THEN write pairs). The census
# below is the builder's own admission check run against a Site checkout; it is the
# instrument that turned red on Lessons main 124f513b for exactly this path.
if [ -n "${SITE:-}" ] && [ -f "$SITE/domain-split/check_education_publication_admission.py" ]; then
  run "publication census (Site admission, --build-control)" "$PY" "$SITE/domain-split/check_education_publication_admission.py" --output "${OUTPUT:-$SITE/domain-split/output}" --lessons . --apps "${APPS:-/home/user/matt-s-apps-}" --build-control
else
  printf '  %-48s %s\n' "publication census (Site admission)" "NOT RUN - set SITE=<site checkout> (and OUTPUT= to a built tree) to run the tail"
fi
echo
if [ "$fail" -eq 0 ]; then echo "SWEEP PASS - all four derived records are in step"
else echo "SWEEP FAIL - a derived record is stale. Run that writer's --write, never hand-edit."; fi
exit "$fail"
