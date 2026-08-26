#!/usr/bin/env bash
# Live-Teach harness runner — the hardened glitchclash pattern: read each
# child's exit status BEFORE grepping its output, herestrings never live pipes
# (the broken-pipe false-green fixed at 36da5d1), DIED on a killed child,
# non-zero exit on any failure.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
export NODE_PATH="${NODE_PATH:-$(npm root -g 2>/dev/null)}"
# Container chromium if present; otherwise playwright resolves its own (CI).
if [ -z "${CHROMIUM_PATH:-}" ] && [ -x /opt/pw-browsers/chromium ]; then
  export CHROMIUM_PATH=/opt/pw-browsers/chromium
fi

failed=0

run_step () {
  local label="$1"; shift
  local out status
  out="$("$@" 2>&1)"
  status=$?
  if [ $status -ne 0 ]; then
    if [ $status -ge 128 ]; then echo "DIED (exit $status)  $label"; else echo "FAILED (exit $status)  $label"; fi
    echo "$out" | tail -20
    failed=1
  else
    if grep -q "FAILED\|SELF-TEST] FAIL" <<<"$out"; then
      echo "FAILED (output)  $label"
      echo "$out" | tail -20
      failed=1
    else
      echo "ok  $label"
    fi
  fi
}

cd "$ROOT"
run_step "stamped core matches source"        node tools/liveteach/stamp_core.mjs --check
run_step "core stamper can go red"            node tools/liveteach/stamp_core.mjs --self-test
run_step "splash regions match canonical"     node tools/liveteach/stamp_splash.mjs --check
run_step "splash stamper can go red"          node tools/liveteach/stamp_splash.mjs --self-test
run_step "stamped QR encoder matches source"  node tools/liveteach/stamp_qr.mjs --check
run_step "QR stamper can go red"              node tools/liveteach/stamp_qr.mjs --self-test
run_step "QR decode gate (jsQR round-trips v1–6)" node tools/liveteach/qr_gate.mjs
run_step "QR gate can go red (incl. the fragment's v4 bug)" node tools/liveteach/qr_gate.mjs --self-test
run_step "static gates (onmessage, one loop, TDZ)" node tools/liveteach/static_gates.mjs
run_step "static gates can go red"            node tools/liveteach/static_gates.mjs --self-test
run_step "units check (claims recompute, coords normalised)" node tools/liveteach/units_check.mjs
run_step "units check can go red"             node tools/liveteach/units_check.mjs --self-test
run_step "lt-shell browser suite"             node tools/liveteach/lt-shell.test.js
run_step "lt-stage browser suite"             node tools/liveteach/lt-stage.test.js
run_step "lt-clicker browser suite"           node tools/liveteach/lt-clicker.test.js
run_step "lt-tele browser suite"              node tools/liveteach/lt-tele.test.js
run_step "lt-share browser suite"             node tools/liveteach/lt-share.test.js

if [ $failed -ne 0 ]; then echo "LIVETEACH SUITES FAILED"; exit 1; fi
echo "LIVETEACH SUITES PASSED"
