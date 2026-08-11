#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
BRANCH="claude/gl-estate-v3"
HISTORIC="1e8a428b523d1b970a8a3a2ab2a99f48a8271d09"
STARTING_SHA="$(git rev-parse HEAD)"
RUNNER_BLOB_SHA="$(git hash-object _glv3/tools/run_registered_candidate.sh)"
export PYTHONDONTWRITEBYTECODE=1

log() { printf '\n== %s ==\n' "$*"; }
fail() { printf 'GLV3 candidate failure: %s\n' "$*" >&2; exit 1; }

assert_exact_non_evidence_clean() {
  local phase="$1"
  local report="/tmp/glv3-diagnostics/exact-${phase}.log"
  local unexpected
  {
    printf 'phase=%s\nhead=%s\n' "$phase" "$(git rev-parse HEAD)"
    printf '%s\n' '--- git status --short ---'
    git status --short
    for tracked in resources.json routes.json; do
      printf '%s\n' "--- ${tracked} ---"
      if [[ -f "$tracked" ]]; then
        printf 'head_blob=%s\n' "$(git rev-parse "HEAD:${tracked}")"
        printf 'worktree_blob=%s\n' "$(git hash-object "$tracked")"
        python - "$tracked" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
b = p.read_bytes()
print(f"bytes={len(b)} lf={b.count(chr(10).encode())} crlf={b.count(chr(13).encode()+chr(10).encode())} trailing_newline={b.endswith(chr(10).encode())}")
PY
        if git diff --ignore-space-at-eol --quiet HEAD -- "$tracked"; then
          printf 'ignore_space_at_eol=identical\n'
        else
          printf 'ignore_space_at_eol=different\n'
        fi
        git diff --numstat HEAD -- "$tracked" || true
        git diff --no-ext-diff --unified=3 HEAD -- "$tracked" | sed -n '1,260p' || true
      else
        printf 'missing=true\n'
      fi
    done
  } >"$report" 2>&1
  cat "$report"
  unexpected="$(git diff --name-only HEAD | grep -v '^_glv3/' || true)"
  if [[ -n "$unexpected" ]]; then
    fail "exact-tree phase ${phase} changed non-evidence paths: ${unexpected}"
  fi
}

log "Bind current branch and integration base"
git fetch --no-tags origin "refs/heads/main:refs/remotes/origin/main" "refs/heads/${BRANCH}:refs/remotes/origin/${BRANCH}"
BASE_SHA="$(git rev-parse refs/remotes/origin/main)"
test "$(git rev-parse HEAD)" = "$STARTING_SHA"
EXPECTED_EVENT_HEAD="${GLV3_EXPECTED_HEAD:-${GITHUB_SHA:-}}"
if [[ -n "$EXPECTED_EVENT_HEAD" ]]; then test "$STARTING_SHA" = "$EXPECTED_EVENT_HEAD"; fi
git merge-base --is-ancestor "$BASE_SHA" "$STARTING_SHA"
test -s _glv3/tools/bs4.py
test -s _glv3/tools/shutil.py
test -s _glv3/tools/safe_extract_transport.py
test -s _glv3/tools/build_candidate_dossier.py
test -s _glv3/tools/finalize_candidate_bundle.py
grep -q 'Deterministic Humanities print-surface reconstruction' _glv3/tools/bs4.py
grep -q 'Source-authored PEQ code provenance' _glv3/tools/bs4.py
grep -q 'TEST-FILENAME REFERENCES' _glv3/tools/shutil.py
grep -q 'SCRUB_EXCLUDED_TOP_LEVEL' _glv3/tools/build_candidate_dossier.py
grep -q '#cards article.card' _glv3/tools/browser_verify.mjs
grep -q '.ytab\[data-year="2026-27"\]' _glv3/tools/browser_verify.mjs
grep -q '#quicknav .chip' _glv3/tools/chip_gate.mjs
printf 'integration_base=%s\nstarting_head=%s\n' "$BASE_SHA" "$STARTING_SHA"

log "Reconstruct and safely extract verified source transport"
for part in _glv3/input/valid.part{00..09}.b64; do test -s "$part"; done
cat _glv3/input/valid.part{00..09}.b64 | tr -d '[:space:]' | base64 --decode > /tmp/glv3-packs.tar.xz
python _glv3/tools/safe_extract_transport.py \
  /tmp/glv3-packs.tar.xz /tmp/glv3-packs \
  --sha256 782ff5865e1406c159c78081bcc218bdaa46678e5c42448a6f298f696ca73f5e \
  --size 102160
test "$(find /tmp/glv3-packs/grow -type f | wc -l)" = 51
test "$(find /tmp/glv3-packs/launch -type f | wc -l)" = 63

log "Reconcile exact inputs, counts and protected baselines"
python _glv3/tools/closeout_reconcile.py \
  --repo "$ROOT" \
  --grow /tmp/glv3-packs/grow \
  --launch /tmp/glv3-packs/launch \
  --historic-sha "$HISTORIC" \
  --integration-sha "$BASE_SHA" \
  --starting-branch-sha "$STARTING_SHA" \
  --transport /tmp/glv3-packs.tar.xz
python -m pip install --disable-pip-version-check --no-cache-dir beautifulsoup4==4.13.4 pillow lxml

log "Generate parallel estates and static evidence"
rm -f _glv3/tools/hashlib.py
rm -rf GROW_Estate_v3 LAUNCH_Estate_v3 _glv3/contact_sheet
GLV3_GROW_SRC=/tmp/glv3-packs/grow \
GLV3_LAUNCH_SRC=/tmp/glv3-packs/launch \
python _glv3/tools/deploy.py
python _glv3/tools/finalize_filename_references.py --repo "$ROOT"
test "$(find GROW_Estate_v3 LAUNCH_Estate_v3 -type f -name '*.html' | wc -l)" = 94
test -s _glv3/GATES_STATIC.json
test -s _glv3/REPORT.md
test -s _glv3/AMBERS.md
test -s _glv3/run_manifest.json
test -z "$(git diff --name-only -- Art_Teesside GROW_ASDAN LAUNCH_ASDAN Grow/Slideshows Launch/Slideshows Science_Teesside Humanities_Teesside Baseline_Weeks BUILD_Estate_v3)"
git diff --check

log "Run all disposable tamper controls"
python _glv3/tools/positive_controls.py --repo "$ROOT"
test -s _glv3/POSITIVE_CONTROLS.json

log "Install print/contact-sheet and real Chromium dependencies"
mkdir -p /tmp/glv3-diagnostics
command -v pdftoppm | tee /tmp/glv3-diagnostics/pdftoppm-path.log
command -v montage | tee /tmp/glv3-diagnostics/montage-path.log
node --version | tee /tmp/glv3-diagnostics/node-version.log
npm --version | tee /tmp/glv3-diagnostics/npm-version.log
npm install --no-save --no-package-lock playwright@1.55.0 sharp pngjs pdfjs-dist 2>&1 | tee /tmp/glv3-diagnostics/npm-install.log
npx playwright install chromium 2>&1 | tee /tmp/glv3-diagnostics/playwright-install.log

log "Run real Chromium gates"
python -m http.server 4173 --bind 127.0.0.1 --directory "$ROOT" >/tmp/glv3-diagnostics/http-primary.log 2>&1 &
SERVER_PID=$!
cleanup_server() { kill "$SERVER_PID" 2>/dev/null || true; wait "$SERVER_PID" 2>/dev/null || true; }
trap 'cleanup_server; cat /tmp/glv3-diagnostics/http-primary.log 2>/dev/null || true' EXIT
for attempt in $(seq 1 60); do
  curl -fsS http://127.0.0.1:4173/ >/dev/null && break
  sleep 0.25
  [[ "$attempt" != 60 ]] || fail "local HTTP server did not start"
done
BASE_URL=http://127.0.0.1:4173 GLV3_BASE_URL=http://127.0.0.1:4173 \
  timeout 55m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4173 2>&1 | tee /tmp/glv3-diagnostics/browser-primary.log
BASE_URL=http://127.0.0.1:4173 GLV3_BASE_URL=http://127.0.0.1:4173 \
  timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4173 2>&1 | tee /tmp/glv3-diagnostics/chips-primary.log
cleanup_server
trap - EXIT
test -s _glv3/GATES_BROWSER.json
test -s _glv3/GATES_CHIPS.json
test "$(find _glv3/contact_sheet -type f -name '*.png' | wc -l)" = 83

log "Build truthful pre-merge evidence dossier"
python _glv3/tools/build_candidate_dossier.py \
  --repo "$ROOT" \
  --integration-sha "$BASE_SHA" \
  --starting-branch-sha "$STARTING_SHA"
test "$(git hash-object _glv3/tools/run_registered_candidate.sh)" = "$RUNNER_BLOB_SHA" || fail "evidence scrubber rewrote the active candidate runner"
python _glv3/tools/finalize_candidate_bundle.py --repo "$ROOT"
python -c 'import json; p=json.load(open("_glv3/GROW_LAUNCH_v3_DEPLOY_PROOF.json", encoding="utf-8")); assert p["candidate_verified"] is True and p["deployment_complete"] is False and p["publication_proven"] is False'
test -s _glv3/GROW_LAUNCH_v3_DEPLOY_FINAL_REPORT.md
test -s _glv3/GROW_LAUNCH_v3_DEPLOY_PROOF.json
test -s _glv3/GROW_LAUNCH_v3_REPORT_AND_PROOF.zip
test -s _glv3/EVIDENCE_ZIP_INTEGRITY.json

log "Remove one-shot transport and obsolete orchestration"
rm -rf _glv3/input _glv3/tooling
rm -f _glv3/RUN_GENERATION.md
rm -f _glv3/tools/bs4.py _glv3/tools/shutil.py _glv3/tools/hashlib.py _glv3/tools/closeout_prep.py _glv3/tools/prepare_registered_candidate.py _glv3/tools/run_registered_candidate.sh
rm -f .github/workflows/glv3-candidate.yml .github/workflows/glv3-closeout.yml .github/workflows/glv3-deploy.yml
rm -f .github/workflows/glv3-generate.yml .github/workflows/glv3-generation-gate.yml .github/workflows/glv3-preflight.yml .github/workflows/glv3-execute.yml
test "$(find GROW_Estate_v3 LAUNCH_Estate_v3 -type f -name '*.html' | wc -l)" = 94
test "$(find _glv3/contact_sheet -type f -name '*.png' | wc -l)" = 83
test -z "$(git diff --name-only -- Art_Teesside GROW_ASDAN LAUNCH_ASDAN Grow/Slideshows Launch/Slideshows Science_Teesside Humanities_Teesside Baseline_Weeks BUILD_Estate_v3)"
! grep -RIlE '/home/runner/work|gh[pousr]_[A-Za-z0-9_]{20,}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY' _glv3 GROW_Estate_v3 LAUNCH_Estate_v3 | grep -q .
! find . -path './.git' -prune -o -path './node_modules' -prune -o -type f -size +50M -print | grep -q .
git diff --check

log "Guard integration and recovery heads before candidate commit"
git fetch --no-tags origin "refs/heads/main:refs/remotes/origin/main" "refs/heads/${BRANCH}:refs/remotes/origin/${BRANCH}"
test "$(git rev-parse refs/remotes/origin/main)" = "$BASE_SHA" || fail "main moved during candidate execution"
test "$(git rev-parse refs/remotes/origin/${BRANCH})" = "$STARTING_SHA" || fail "recovery branch moved during candidate execution"

log "Commit and push immutable candidate"
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git diff --cached --quiet && fail "candidate generation produced no tracked changes"
git commit -m 'feat: install verified GROW and LAUNCH alternative v3 estates'
CANDIDATE_SHA="$(git rev-parse HEAD)"
git push origin HEAD:"$BRANCH"
printf 'candidate_sha=%s\n' "$CANDIDATE_SHA" >> "${GITHUB_OUTPUT:-/tmp/glv3-output}"
printf 'candidate_head=%s\n' "$CANDIDATE_SHA"

log "Re-prove exact committed candidate tree"
rm -rf /tmp/glv3-exact
git worktree add --detach /tmp/glv3-exact "$CANDIDATE_SHA"
cd /tmp/glv3-exact
assert_exact_non_evidence_clean "after-checkout"
test "$(find GROW_Estate_v3 LAUNCH_Estate_v3 -type f -name '*.html' | wc -l)" = 94
test "$(find _glv3/contact_sheet -type f -name '*.png' | wc -l)" = 83
python - <<'PY'
import hashlib,json,zipfile
from pathlib import Path
archive=Path('_glv3/GROW_LAUNCH_v3_REPORT_AND_PROOF.zip')
manifest=json.loads(Path('_glv3/EVIDENCE_ZIP_INTEGRITY.json').read_text())
assert hashlib.sha256(archive.read_bytes()).hexdigest()==manifest['sha256']
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
PY
python _glv3/tools/deploy.py --rerun-live-privacy
assert_exact_non_evidence_clean "after-privacy"
BEFORE_POSITIVE="$(git status --porcelain)"
python _glv3/tools/positive_controls.py --repo "$PWD"
AFTER_POSITIVE="$(git status --porcelain)"
test "$BEFORE_POSITIVE" = "$AFTER_POSITIVE"
assert_exact_non_evidence_clean "after-positive-controls"
ln -s "$ROOT/node_modules" node_modules
python -m http.server 4174 --bind 127.0.0.1 --directory "$PWD" >/tmp/glv3-diagnostics/http-exact.log 2>&1 &
EXACT_SERVER=$!
cleanup_exact() { kill "$EXACT_SERVER" 2>/dev/null || true; wait "$EXACT_SERVER" 2>/dev/null || true; }
trap 'cleanup_exact; cat /tmp/glv3-diagnostics/http-exact.log 2>/dev/null || true' EXIT
for attempt in $(seq 1 60); do
  curl -fsS http://127.0.0.1:4174/ >/dev/null && break
  sleep 0.25
  [[ "$attempt" != 60 ]] || fail "exact-tree HTTP server did not start"
done
BASE_URL=http://127.0.0.1:4174 GLV3_BASE_URL=http://127.0.0.1:4174 \
  timeout 55m node _glv3/tools/browser_verify.mjs http://127.0.0.1:4174 2>&1 | tee /tmp/glv3-diagnostics/browser-exact.log
assert_exact_non_evidence_clean "after-browser"
BASE_URL=http://127.0.0.1:4174 GLV3_BASE_URL=http://127.0.0.1:4174 \
  timeout 20m node _glv3/tools/chip_gate.mjs http://127.0.0.1:4174 2>&1 | tee /tmp/glv3-diagnostics/chips-exact.log
cleanup_exact
trap - EXIT
rm node_modules
assert_exact_non_evidence_clean "after-chip-gate"
test -z "$(git diff --name-only HEAD -- Art_Teesside GROW_ASDAN LAUNCH_ASDAN Grow/Slideshows Launch/Slideshows Science_Teesside Humanities_Teesside Baseline_Weeks BUILD_Estate_v3)"
git diff --check

log "Publish SHA-bound success statuses"
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  TARGET_URL="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"
  for CONTEXT in glv3/source-generation glv3/exact-tree glv3/protected-invariance; do
    PAYLOAD="$(jq -nc --arg state success --arg context "$CONTEXT" --arg description 'Verified GLV3 candidate gate passed' --arg target_url "$TARGET_URL" '{state:$state,context:$context,description:$description,target_url:$target_url}')"
    curl --fail-with-body --silent --show-error -X POST \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H 'Accept: application/vnd.github+json' \
      -H 'X-GitHub-Api-Version: 2022-11-28' \
      "${GITHUB_API_URL}/repos/${GITHUB_REPOSITORY}/statuses/${CANDIDATE_SHA}" \
      -d "$PAYLOAD" >/dev/null
  done
fi

cd "$ROOT"
rm -rf node_modules
printf 'GLV3 candidate complete: %s\n' "$CANDIDATE_SHA"
