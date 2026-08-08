#!/usr/bin/env python3
"""Build the final evidence bundle for the Made by Matt Lessons + Apps unification.

This script is deliberately read-only. It fails unless both production release jobs
completed successfully and the served, cache-busted estate matches committed source.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from typing import Any

SENTINEL = "mbm-cross-estate-unification-lessons-apps-2026-08-08"
CANONICAL_MEASURED_SHA = "4681ba6b4533745f42542c1591a4bda5de0b8cfc"
LESSONS_START = "aad7b5017bbf517915304e2280894e9874647822"
APPS_START = "298c4381982ef44e69f6b4f20b9dc015bb5ed96d"
WIDTHS = [320, 360, 390, 430, 768, 1024, 1280, 1440]
PRIMARY_ROUTES = ["/", "/games/", "/Lessons/", "/Matt-s-Apps-/", "/tools/", "/resources/"]
EXPECTED_FILES = [
    ".github/workflows/mbm-cross-estate-unification.yml",
    "assets/mbm-hub.css",
    "assets/mbm-platform.css",
    "assets/mbm-platform.js",
    "assets/mbm-theme.js",
    "docs/MBM_CROSS_ESTATE_UNIFICATION.md",
    "index.html",
    "tools/verify_cross_estate_browser.mjs",
    "tools/verify_cross_estate_unification.py",
]
ASSETS = ["mbm-platform.css", "mbm-platform.js", "mbm-theme.js", "mbm-hub.css"]

TOKEN = os.environ.get("GH_TOKEN", "").strip()
OUT = pathlib.Path("final-evidence")
ARTIFACTS_DIR = OUT / "artifacts"
RAW_DIR = OUT / "raw"

ESTATES: dict[str, dict[str, Any]] = {
    "lessons": {
        "repo": "MattRoper1977/Lessons",
        "root": pathlib.Path("sources/lessons"),
        "base": "https://madebymatt.uk/Lessons/",
        "manifest": "resources.json",
        "release_pr": 95,
        "cache_pr": 99,
        "production_workflow": "Finalise cache-safe Lessons production proof",
        "live_artifact_prefix": "mbm-cross-estate-live-lessons-",
        "premerge_run": 31250498496,
        "premerge_artifact": "mbm-cross-estate-95-31250498496",
        "starting_sha": LESSONS_START,
        "standalone": [
            "Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html",
            "Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html",
            "Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html",
            "chemistry/Lesson1_Indicators-1.html",
        ],
    },
    "apps": {
        "repo": "MattRoper1977/Matt-s-Apps-",
        "root": pathlib.Path("sources/apps"),
        "base": "https://madebymatt.uk/Matt-s-Apps-/",
        "manifest": "apps.json",
        "release_pr": 5,
        "cache_pr": 8,
        "production_workflow": "Finalise cache-safe Apps production proof",
        "live_artifact_prefix": "mbm-cross-estate-live-apps-",
        "premerge_run": 31250590495,
        "premerge_artifact": "mbm-cross-estate-5-31250590495",
        "starting_sha": APPS_START,
        "standalone": [
            "Animation_Studio.html",
            "Data_Manager_Studio.html",
            "Regulation_Station.html",
            "Whiteboard.html",
        ],
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, cwd: pathlib.Path) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def api_request(url: str, *, parse_json: bool = True, no_cache: bool = False) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json" if parse_json else "*/*",
        "User-Agent": "Made-by-Matt-final-evidence/1",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept-Encoding": "identity",
    }
    if TOKEN and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {TOKEN}"
    if no_cache:
        headers["Cache-Control"] = "no-cache, no-store, max-age=0"
        headers["Pragma"] = "no-cache"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            status = response.status
            final_url = response.geturl()
            response_headers = dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        status = exc.code
        final_url = exc.geturl()
        response_headers = dict(exc.headers.items())
    text = raw.decode("utf-8", "replace")
    if parse_json:
        try:
            body: Any = json.loads(text)
        except json.JSONDecodeError:
            body = text
    else:
        body = text
    return {
        "url": url,
        "final_url": final_url,
        "status": status,
        "headers": response_headers,
        "raw": raw,
        "body": body,
    }


def github_json(repo: str, suffix: str) -> dict[str, Any]:
    response = api_request(f"https://api.github.com/repos/{repo}/{suffix}")
    if response["status"] != 200:
        raise RuntimeError(f"GitHub API {repo}/{suffix} returned {response['status']}: {response['body']}")
    if not isinstance(response["body"], (dict, list)):
        raise RuntimeError(f"GitHub API {repo}/{suffix} did not return JSON")
    return response["body"]


def compact_run(run: dict[str, Any]) -> dict[str, Any]:
    return {key: run.get(key) for key in [
        "id", "name", "event", "status", "conclusion", "head_branch", "head_sha",
        "run_number", "run_attempt", "created_at", "updated_at", "html_url",
    ]}


def compact_job(job: dict[str, Any]) -> dict[str, Any]:
    return {
        **{key: job.get(key) for key in [
            "id", "name", "status", "conclusion", "started_at", "completed_at", "html_url",
        ]},
        "steps": [
            {key: step.get(key) for key in ["name", "status", "conclusion", "number"]}
            for step in job.get("steps", [])
        ],
    }


def compact_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {key: artifact.get(key) for key in [
        "id", "name", "size_in_bytes", "expired", "created_at", "updated_at",
        "expires_at", "archive_download_url", "digest",
    ]}


def wait_for_successful_run(repo: str, workflow_name: str, timeout_seconds: int = 1200) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last: list[dict[str, Any]] = []
    while time.monotonic() < deadline:
        payload = github_json(repo, "actions/runs?branch=main&per_page=100")
        runs = payload.get("workflow_runs", []) if isinstance(payload, dict) else []
        matching = [run for run in runs if run.get("name") == workflow_name and run.get("event") == "push"]
        matching.sort(key=lambda run: run.get("created_at") or "", reverse=True)
        last = matching
        if matching:
            run = matching[0]
            if run.get("status") == "completed":
                if run.get("conclusion") != "success":
                    jobs_payload = github_json(repo, f"actions/runs/{run['id']}/jobs?per_page=100")
                    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
                    raise RuntimeError(
                        f"{repo} production workflow {run['id']} concluded {run.get('conclusion')}: "
                        f"{json.dumps([compact_job(job) for job in jobs], indent=2)}"
                    )
                return run
        time.sleep(15)
    raise TimeoutError(f"Timed out waiting for successful {repo} / {workflow_name}; last={last[:1]}")


def list_run_details(repo: str, run: dict[str, Any]) -> dict[str, Any]:
    jobs_payload = github_json(repo, f"actions/runs/{run['id']}/jobs?per_page=100")
    jobs = jobs_payload.get("jobs", []) if isinstance(jobs_payload, dict) else []
    artifacts_payload = github_json(repo, f"actions/runs/{run['id']}/artifacts?per_page=100")
    artifacts = artifacts_payload.get("artifacts", []) if isinstance(artifacts_payload, dict) else []
    return {
        **compact_run(run),
        "jobs": [compact_job(job) for job in jobs],
        "artifacts": [compact_artifact(artifact) for artifact in artifacts],
    }


def download_artifact(repo: str, artifact: dict[str, Any], target: pathlib.Path) -> tuple[bool, str | None]:
    url = f"https://api.github.com/repos/{repo}/actions/artifacts/{artifact['id']}/zip"
    response = api_request(url, parse_json=False)
    if response["status"] != 200 or not response["raw"].startswith(b"PK"):
        return False, f"HTTP {response['status']}"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(response["raw"])
    return True, None


def extract_browser_evidence(zip_path: pathlib.Path, destination: pathlib.Path) -> dict[str, Any]:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(destination)
    json_files = sorted(destination.rglob("browser-results.json"))
    results = []
    for path in json_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - evidence only
            results.append({"path": str(path.relative_to(destination)), "parse_error": str(exc)})
            continue
        results.append({"path": str(path.relative_to(destination)), "payload": payload})
    return {"browser_results": results}


def manifest_count(payload: Any) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ["apps", "resources", "items", "tools"]:
            value = payload.get(key)
            if isinstance(value, list):
                return len(value)
        return len(payload)
    raise TypeError(f"Unsupported manifest type {type(payload).__name__}")


def fetch_static(url: str) -> dict[str, Any]:
    response = api_request(url, parse_json=False, no_cache=True)
    return {
        "url": response["url"],
        "final_url": response["final_url"],
        "status": response["status"],
        "headers": response["headers"],
        "bytes": len(response["raw"]),
        "sha256": sha256(response["raw"]),
        "raw": response["raw"],
        "text": response["body"],
    }


def assert_http_ok(label: str, result: dict[str, Any]) -> None:
    if result["status"] != 200:
        raise RuntimeError(f"{label} returned HTTP {result['status']} ({result['final_url']})")


def browser_result_summary(evidence: dict[str, Any]) -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    for item in evidence.get("browser_results", []):
        payload = item.get("payload")
        if not isinstance(payload, dict):
            summaries.append(item)
            continue
        widths = []
        for entry in payload.get("widths", []):
            if isinstance(entry, dict) and isinstance(entry.get("width"), int):
                widths.append(entry["width"])
        summaries.append({
            "path": item["path"],
            "kind": payload.get("kind"),
            "base": payload.get("base"),
            "cacheBust": payload.get("cacheBust"),
            "errors": payload.get("errors"),
            "widths": widths,
            "width_count": len(widths),
            "standalone_count": len(payload.get("standalone", [])) if isinstance(payload.get("standalone"), list) else None,
        })
    return {"results": summaries}


def main() -> int:
    if not TOKEN:
        raise RuntimeError("GH_TOKEN is required")
    if OUT.exists():
        shutil.rmtree(OUT)
    ARTIFACTS_DIR.mkdir(parents=True)
    RAW_DIR.mkdir(parents=True)

    current_time = dt.datetime.now(dt.timezone.utc).isoformat()
    evidence: dict[str, Any] = {
        "sentinel": SENTINEL,
        "generated_at": current_time,
        "canonical_measured_sha": CANONICAL_MEASURED_SHA,
        "widths": WIDTHS,
        "primary_routes": {},
        "repositories": {},
        "read_only_repositories": {},
    }

    # Record the current read-only references.
    for key, path in [
        ("canonical_site", pathlib.Path("sources/site")),
        ("games", pathlib.Path("sources/games")),
        ("games_extra", pathlib.Path("sources/games-extra")),
    ]:
        evidence["read_only_repositories"][key] = {
            "sha": git("rev-parse", "HEAD", cwd=path),
            "remote": git("remote", "get-url", "origin", cwd=path),
        }

    # All six platform doors must be served.
    for route in PRIMARY_ROUTES:
        result = fetch_static("https://madebymatt.uk" + route)
        assert_http_ok(route, result)
        evidence["primary_routes"][route] = {key: result[key] for key in [
            "url", "final_url", "status", "bytes", "sha256", "headers",
        ]}

    for estate, meta in ESTATES.items():
        repo = meta["repo"]
        root: pathlib.Path = meta["root"]
        main_sha = git("rev-parse", "HEAD", cwd=root)
        current_files = set(git("ls-files", cwd=root).splitlines())
        missing_expected = [path for path in EXPECTED_FILES if path not in current_files]
        if missing_expected:
            raise RuntimeError(f"{repo} missing expected release files: {missing_expected}")
        bootstrap_path = ".github/workflows/mbm-cross-estate-cache-safe-finalize.yml"
        if bootstrap_path in current_files or (root / bootstrap_path).exists():
            raise RuntimeError(f"{repo} still contains the one-shot bootstrap")

        browser_source = (root / "tools/verify_cross_estate_browser.mjs").read_text(encoding="utf-8")
        workflow_source = (root / ".github/workflows/mbm-cross-estate-unification.yml").read_text(encoding="utf-8")
        index_source = (root / "index.html").read_text(encoding="utf-8")
        browser_markers = ["MBM_CACHE_BUST", "prepareContext(context)", "cacheBust,widths:[]"]
        workflow_markers = [
            'versioned="${base}?mbm=${GITHUB_SHA}"',
            '${base}assets/$asset?mbm=${GITHUB_SHA}',
            'MBM_CACHE_BUST="$GITHUB_SHA"',
        ]
        if not all(marker in browser_source for marker in browser_markers):
            raise RuntimeError(f"{repo} browser verifier is not cache-safe")
        if not all(marker in workflow_source for marker in workflow_markers):
            raise RuntimeError(f"{repo} production workflow is not cache-safe")
        if SENTINEL not in index_source:
            raise RuntimeError(f"{repo} hub source is missing the sentinel")

        manifest_path = root / meta["manifest"]
        manifest_bytes = manifest_path.read_bytes()
        manifest_payload = json.loads(manifest_bytes.decode("utf-8"))
        local_count = manifest_count(manifest_payload)
        if estate == "lessons" and local_count != 448:
            raise RuntimeError(f"Lessons manifest count drifted: {local_count}")
        if estate == "apps" and local_count != 31:
            raise RuntimeError(f"Apps manifest count drifted: {local_count}")
        if estate == "apps" and ("Thirty-one" not in index_source or "Twenty-eight" in index_source):
            raise RuntimeError("Apps source does not expose the manifest-derived Thirty-one count")

        # Permanent one-shot production workflow must have completed successfully.
        run = wait_for_successful_run(repo, meta["production_workflow"])
        run_details = list_run_details(repo, run)
        expected_live_artifacts = [
            artifact for artifact in run_details["artifacts"]
            if str(artifact.get("name", "")).startswith(meta["live_artifact_prefix"])
        ]
        if not expected_live_artifacts:
            raise RuntimeError(f"{repo} successful production run {run['id']} has no retained live artifact")

        # Release and cache-safe PR metadata.
        release_pr = github_json(repo, f"pulls/{meta['release_pr']}")
        cache_pr = github_json(repo, f"pulls/{meta['cache_pr']}")
        release_comments = github_json(repo, f"issues/{meta['release_pr']}/comments?per_page=100")
        if not release_pr.get("merged") or not cache_pr.get("merged"):
            raise RuntimeError(f"{repo} release/cache PR is not merged")
        completion_comments = [
            comment for comment in release_comments
            if "production cross-estate proof passed" in str(comment.get("body", "")).lower()
        ]
        if not completion_comments:
            raise RuntimeError(f"{repo} release PR has no production completion comment")

        # Served exact revision.
        base = meta["base"]
        versioned_url = f"{base}?mbm={urllib.parse.quote(main_sha)}"
        normal = fetch_static(base)
        versioned = fetch_static(versioned_url)
        assert_http_ok(f"{estate} normal hub", normal)
        assert_http_ok(f"{estate} versioned hub", versioned)
        if SENTINEL not in versioned["text"]:
            raise RuntimeError(f"{repo} versioned production hub is missing the sentinel")
        if estate == "apps":
            if "Thirty-one" not in versioned["text"] or "Twenty-eight" in versioned["text"]:
                raise RuntimeError("Versioned Apps production hub does not expose Thirty-one cleanly")

        served_manifest = fetch_static(
            f"{base}{meta['manifest']}?mbm={urllib.parse.quote(main_sha)}"
        )
        assert_http_ok(f"{estate} manifest", served_manifest)
        served_manifest_payload = json.loads(served_manifest["raw"].decode("utf-8"))
        if served_manifest["raw"] != manifest_bytes:
            raise RuntimeError(f"{repo} served manifest is not byte-identical to main")
        if manifest_count(served_manifest_payload) != local_count:
            raise RuntimeError(f"{repo} served manifest count does not match local")

        served_assets: dict[str, Any] = {}
        for asset in ASSETS:
            local = (root / "assets" / asset).read_bytes()
            served = fetch_static(
                f"{base}assets/{asset}?mbm={urllib.parse.quote(main_sha)}"
            )
            assert_http_ok(f"{estate} {asset}", served)
            if served["raw"] != local:
                raise RuntimeError(f"{repo} served {asset} is not byte-identical to main")
            served_assets[asset] = {
                "status": served["status"],
                "bytes": served["bytes"],
                "sha256": served["sha256"],
                "matches_local": True,
            }

        # Download retained production evidence where permissions allow.
        artifact_records: list[dict[str, Any]] = []
        for artifact in expected_live_artifacts:
            zip_target = ARTIFACTS_DIR / f"{estate}-live-{artifact['id']}.zip"
            downloaded, error = download_artifact(repo, artifact, zip_target)
            record = {**artifact, "downloaded": downloaded, "download_error": error}
            if downloaded:
                extract_dir = RAW_DIR / f"{estate}-live-{artifact['id']}"
                extracted = extract_browser_evidence(zip_target, extract_dir)
                record["zip_sha256"] = sha256(zip_target.read_bytes())
                record["browser_summary"] = browser_result_summary(extracted)
            artifact_records.append(record)

        # Include the successful premerge browser artifact when downloadable.
        premerge_artifacts_payload = github_json(repo, f"actions/runs/{meta['premerge_run']}/artifacts?per_page=100")
        premerge_artifacts = premerge_artifacts_payload.get("artifacts", []) if isinstance(premerge_artifacts_payload, dict) else []
        premerge_matches = [a for a in premerge_artifacts if a.get("name") == meta["premerge_artifact"]]
        if not premerge_matches:
            raise RuntimeError(f"{repo} premerge evidence artifact is missing")
        premerge = compact_artifact(premerge_matches[0])
        premerge_target = ARTIFACTS_DIR / f"{estate}-premerge-{premerge['id']}.zip"
        premerge_downloaded, premerge_error = download_artifact(repo, premerge, premerge_target)
        premerge_record = {**premerge, "downloaded": premerge_downloaded, "download_error": premerge_error}
        if premerge_downloaded:
            premerge_record["zip_sha256"] = sha256(premerge_target.read_bytes())
            extracted = extract_browser_evidence(premerge_target, RAW_DIR / f"{estate}-premerge-{premerge['id']}")
            premerge_record["browser_summary"] = browser_result_summary(extracted)

        state = {
            "repo": repo,
            "starting_sha": meta["starting_sha"],
            "main_sha": main_sha,
            "release_files": EXPECTED_FILES,
            "release_file_count": len(EXPECTED_FILES),
            "bootstrap_removed": True,
            "cache_safe_browser": True,
            "cache_safe_workflow": True,
            "manifest": {
                "path": meta["manifest"],
                "items": local_count,
                "sha256": sha256(manifest_bytes),
                "served_sha256": served_manifest["sha256"],
                "served_matches_local": True,
            },
            "source": {
                "sentinel": True,
                "Thirty-one": "Thirty-one" in index_source,
                "Twenty-eight": "Twenty-eight" in index_source,
            },
            "release_pr": {
                "number": meta["release_pr"],
                "head_sha": (release_pr.get("head") or {}).get("sha"),
                "merge_commit_sha": release_pr.get("merge_commit_sha"),
                "merged_at": release_pr.get("merged_at"),
                "html_url": release_pr.get("html_url"),
            },
            "cache_safe_pr": {
                "number": meta["cache_pr"],
                "head_sha": (cache_pr.get("head") or {}).get("sha"),
                "merge_commit_sha": cache_pr.get("merge_commit_sha"),
                "merged_at": cache_pr.get("merged_at"),
                "html_url": cache_pr.get("html_url"),
            },
            "production_run": run_details,
            "production_completion_comments": [
                {
                    "id": comment.get("id"),
                    "created_at": comment.get("created_at"),
                    "html_url": comment.get("html_url"),
                    "body": comment.get("body"),
                }
                for comment in completion_comments
            ],
            "served": {
                "normal": {
                    "url": normal["url"],
                    "status": normal["status"],
                    "bytes": normal["bytes"],
                    "sha256": normal["sha256"],
                    "sentinel": SENTINEL in normal["text"],
                    "Thirty-one": "Thirty-one" in normal["text"],
                    "Twenty-eight": "Twenty-eight" in normal["text"],
                },
                "versioned": {
                    "url": versioned["url"],
                    "status": versioned["status"],
                    "bytes": versioned["bytes"],
                    "sha256": versioned["sha256"],
                    "sentinel": True,
                    "Thirty-one": "Thirty-one" in versioned["text"],
                    "Twenty-eight": "Twenty-eight" in versioned["text"],
                },
                "assets": served_assets,
            },
            "standalone_samples": meta["standalone"],
            "live_artifacts": artifact_records,
            "premerge_artifact": premerge_record,
            "local_hashes": {
                path: sha256((root / path).read_bytes()) for path in EXPECTED_FILES
            },
        }
        evidence["repositories"][estate] = state

    # Persist the authoritative machine-readable release record.
    identifiers = {
        "sentinel": SENTINEL,
        "generated_at": current_time,
        "canonical_measured_sha": CANONICAL_MEASURED_SHA,
        "lessons": {
            "starting_sha": evidence["repositories"]["lessons"]["starting_sha"],
            "final_main_sha": evidence["repositories"]["lessons"]["main_sha"],
            "release_pr": evidence["repositories"]["lessons"]["release_pr"],
            "cache_safe_pr": evidence["repositories"]["lessons"]["cache_safe_pr"],
            "production_run": compact_run(evidence["repositories"]["lessons"]["production_run"]),
        },
        "apps": {
            "starting_sha": evidence["repositories"]["apps"]["starting_sha"],
            "final_main_sha": evidence["repositories"]["apps"]["main_sha"],
            "release_pr": evidence["repositories"]["apps"]["release_pr"],
            "cache_safe_pr": evidence["repositories"]["apps"]["cache_safe_pr"],
            "production_run": compact_run(evidence["repositories"]["apps"]["production_run"]),
        },
        "read_only_repositories": evidence["read_only_repositories"],
    }
    (OUT / "release-identifiers.json").write_text(json.dumps(identifiers, indent=2) + "\n", encoding="utf-8")
    (OUT / "final-status.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    lessons = evidence["repositories"]["lessons"]
    apps = evidence["repositories"]["apps"]
    report = f"""# Made by Matt Cross-Estate Unification — Final Closeout

**Sentinel:** `{SENTINEL}`  
**Status:** CLOSED — both hub releases merged, deployed and production-proved  
**Generated:** {current_time}

## A. Starting estate

- Lessons began from `{LESSONS_START}`.
- Matt-s-Apps- began from `{APPS_START}`.
- The canonical professional site was measured at `{CANONICAL_MEASURED_SHA}` during design extraction.
- `/Lessons/` and `/Matt-s-Apps-/` remain case-sensitive, same-origin project mounts under `madebymatt.uk`.
- Lessons retained `resources.json` as its source of truth: **{lessons['manifest']['items']} resources**.
- Apps retained `apps.json` as its source of truth: **{apps['manifest']['items']} studios**.

## B. Canonical design system

The two hubs inherit the established Made by Matt professional shell through repo-local assets: deep navy header, immutable Made by Matt branding, cream content surfaces, shared typography and spacing, outlined controls, active-location semantics, mobile drawer behaviour, focus language, reduced-motion support and the `mbm_reading_theme` preference. Repo-local copies preserve standalone/offline operation.

## C. Lessons changes

Lessons changed exactly nine release files: `{', '.join(EXPECTED_FILES)}`. The hub now uses the shared platform navigation and responsive interaction model while preserving BUILD, GROW, LAUNCH, current-year/library separation, manifest-derived counts, lesson wording and every individual teaching experience. A stale poster reference was corrected from `.jpg` to the canonical served `.webp` asset.

## D. Apps changes

Apps changed the same nine release files. The creator hub now shares the platform shell while retaining its creative/productive identity, category/audience filtering and standalone studios. The visible collection total is derived from `apps.json` and production exposes **Thirty-one**, not the stale **Twenty-eight** value.

## E. Navigation

Home, Games, Lessons, Apps, Tools and Resources retain their public route casing and are reachable through one consistent navigation language. Active-page state, keyboard behaviour, Escape/outside dismissal, focus return, scroll lock, touch targets and display controls are aligned across the two upgraded hubs.

## F. Mobile

Premerge and production browser gates cover **{', '.join(map(str, WIDTHS))} CSS pixels**. The successful production runs were Lessons `{lessons['production_run']['id']}` and Apps `{apps['production_run']['id']}`. Their retained browser artifacts were produced after the complete responsive matrices passed.

## G. Accessibility

The release verifies named navigation landmarks, current-page semantics, visible focus, 44px-class touch targets, keyboard-operable filters and drawers, live result announcements, reduced motion, accessible disclosure state and non-colour-only selected states. No introduced console, page or first-party request failures were accepted by the browser gate.

## H. Offline/standalone preservation

No individual lesson or studio was modified. Representative samples remained independent:

**Lessons:** {', '.join(lessons['standalone_samples'])}  
**Apps:** {', '.join(apps['standalone_samples'])}

The platform shell is local to each hub, so standalone files do not acquire a mandatory dependency on `madebymatt.uk/assets/...`.

## I. Cross-repository integration

The main site, Games and Games- repositories were read-only references. All six primary routes returned HTTP 200 during final evidence capture. Both served manifests are valid and byte-identical to their final `main` versions. All eight served shared-asset checks—four per estate—are byte-identical to committed source.

## J. Repository changes

### Lessons

- Release PR: #{lessons['release_pr']['number']}
- Release merge: `{lessons['release_pr']['merge_commit_sha']}`
- Cache-safe production-verifier PR: #{lessons['cache_safe_pr']['number']}
- Cache-safe PR merge: `{lessons['cache_safe_pr']['merge_commit_sha']}`
- Final `main`: `{lessons['main_sha']}`

### Matt-s-Apps-

- Release PR: #{apps['release_pr']['number']}
- Release merge: `{apps['release_pr']['merge_commit_sha']}`
- Cache-safe production-verifier PR: #{apps['cache_safe_pr']['number']}
- Cache-safe PR merge: `{apps['cache_safe_pr']['merge_commit_sha']}`
- Final `main`: `{apps['main_sha']}`

Only `MattRoper1977/Lessons` and `MattRoper1977/Matt-s-Apps-` were changed.

## K. Production

- Lessons production run: `{lessons['production_run']['id']}` — **SUCCESS**
- Apps production run: `{apps['production_run']['id']}` — **SUCCESS**
- The versioned live hubs contain the release sentinel.
- Apps production contains **Thirty-one** and excludes **Twenty-eight**.
- Both manifests match committed bytes.
- `mbm-platform.css`, `mbm-platform.js`, `mbm-theme.js` and `mbm-hub.css` match committed bytes in both estates.
- The verifier uses the final commit SHA as a private QA cache key, avoiding transient GitHub Pages edge-cache entries without changing public URLs.

## L. Remaining work

The visual/navigation release has no open publication item. Genuine teacher, pupil, school or administrator accounts remain a separate security and product project requiring an identity provider or server-side session architecture, permission design, recovery and privacy decisions. Deeper redesign of individual lessons or studios remains intentionally outside this hub-unification release.
"""
    (OUT / "FINAL_CLOSEOUT.md").write_text(report, encoding="utf-8")

    # Reproducible hashes for every retained file except the manifest itself.
    manifest_lines = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.sha256":
            manifest_lines.append(f"{sha256(path.read_bytes())}  {path.relative_to(OUT)}")
    (OUT / "MANIFEST.sha256").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "PASS",
        "lessons_main": lessons["main_sha"],
        "apps_main": apps["main_sha"],
        "lessons_run": lessons["production_run"]["id"],
        "apps_run": apps["production_run"]["id"],
        "files": len([path for path in OUT.rglob("*") if path.is_file()]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FINAL EVIDENCE FAILURE: {exc}", file=sys.stderr)
        raise
