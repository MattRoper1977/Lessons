#!/usr/bin/env python3
"""Where a "/"-absolute link actually points, on the deployed domain.

WHY THIS EXISTS
---------------
The GLV3 generated-tree gate resolves every href and src, and treats any
"/"-absolute path as repo-root-relative. That is right for most of this
repository and wrong for exactly one thing: madebymatt.uk serves the SITE repo
at the domain root and mounts THIS repository at /Lessons/. So

    <script defer src="/hud.js"></script>

is a correct, working link in production — hud.js is served from the site repo's
root — and a broken one to a gate that only knows about this tree. That
disagreement stopped 78 decks from getting the slide announcer at a108c4e3.

The gate was right about what it could see. Its model of the world was one mount
short. This module is that model, written down where it can be reviewed rather
than inferred from a special case buried in a workflow.

THE MAP
-------
    /Lessons/**   ->  this repository's tree      (unchanged behaviour)
    /**           ->  the site repo at a PINNED SHA, checked over raw.github

Resolution order for a "/"-absolute href:
  (a) under this repo's mount  -> resolve against the tree, exactly as before
  (b) otherwise                -> look it up in the site mount at the pinned SHA
  (c) neither                  -> broken, exactly as before

FAIL-SAFE, NOT FAIL-OPEN
------------------------
A 404 from the site mount is a BROKEN link: definitive, the file is not there.
Anything else that is not a 200 — a timeout, a DNS failure, a 5xx, a proxy
refusal — is UNVERIFIED, carries its own distinct message, and is RED. It is
never green. A gate that goes quiet when the network hiccups is worse than no
gate, because it looks like a pass.

The pinned SHA is printed on every run so drift is visible in the log rather
than discovered later.

    python3 _glv3/tools/mount_map.py --self-test
    python3 _glv3/tools/mount_map.py --site-sha <sha> --check /hud.js
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE_REPO = "MattRoper1977/mattroper1977.github.io"
SITE_RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"
SITE_REMOTE = f"https://github.com/{SITE_REPO}"

# This repository's mount on the deployed domain. Anything under it resolves
# against the local tree with the prefix stripped.
LOCAL_MOUNT = "/Lessons/"

OK, BROKEN, UNVERIFIED = "ok", "broken", "unverified"


def pin_site_sha(timeout: float = 30.0) -> str:
    """The site repo's main at the moment the gate starts.

    Pinned once per run and passed down, so every link in a run is checked
    against the same tree. Resolving per-request would let the answer change
    underneath a single verification.
    """
    out = subprocess.run(
        ["git", "ls-remote", SITE_REMOTE, "main"],
        capture_output=True, text=True, timeout=timeout,
    )
    if out.returncode != 0 or not out.stdout.strip():
        raise RuntimeError(f"could not pin site SHA: {out.stderr.strip() or 'no output'}")
    return out.stdout.split()[0]


class SiteMount:
    """The site repo at one pinned SHA, asked over raw.githubusercontent.com."""

    def __init__(self, sha: str, timeout: float = 20.0):
        self.sha = sha
        self.timeout = timeout
        self._cache: dict[str, tuple[str, str]] = {}

    def lookup(self, path: str) -> tuple[str, str]:
        """(status, detail) for one domain-root path such as '/hud.js'."""
        rel = path.lstrip("/")
        if not rel:
            rel = "index.html"
        if rel in self._cache:
            return self._cache[rel]
        url = SITE_RAW.format(repo=SITE_REPO, sha=self.sha, path=rel)
        req = urllib.request.Request(url, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = ((OK, url) if resp.status == 200
                          else (UNVERIFIED, f"HTTP {resp.status} from {url}"))
        except urllib.error.HTTPError as exc:
            # 404 is an answer: the file is not in the site repo at this SHA.
            # Every other HTTP error is the check failing, not the link.
            result = ((BROKEN, f"not in {SITE_REPO}@{self.sha[:8]}")
                      if exc.code == 404 else (UNVERIFIED, f"HTTP {exc.code} from {url}"))
        except Exception as exc:  # timeout, DNS, proxy refusal, TLS
            result = (UNVERIFIED, f"{type(exc).__name__}: {exc} ({url})")
        self._cache[rel] = result
        return result


def resolve(raw: str, from_file: Path, root: Path, site: SiteMount | None) -> tuple[str, str]:
    """Resolve one href/src the way the deployed domain would.

    Returns (status, detail). Non-local schemes and in-page anchors are skipped
    by the caller before they reach here.
    """
    parts = urlsplit(raw.strip())
    path = unquote(parts.path)
    if not path:
        return OK, "no path component"

    if not path.startswith("/"):
        target = from_file.parent / path
        if target.is_dir():
            target = target / "index.html"
        return (OK, str(target)) if target.exists() else (BROKEN, f"missing {target}")

    # (a) this repository's own mount
    if path.startswith(LOCAL_MOUNT):
        target = root / path[len(LOCAL_MOUNT):]
        if target.is_dir():
            target = target / "index.html"
        return (OK, str(target)) if target.exists() else (BROKEN, f"missing {target}")

    # Historic behaviour: a "/"-absolute path also resolves against this tree,
    # because much of the estate is written that way and those links are real.
    target = root / path.lstrip("/")
    if target.is_dir():
        target = target / "index.html"
    if target.exists():
        return OK, str(target)

    # (b) the domain root, which is the site repo
    if site is None:
        return UNVERIFIED, f"no site mount available to resolve {path}"
    return site.lookup(path)


def self_test() -> int:
    """Prove the map answers all three ways, and that it fails safe."""
    problems = []
    root = Path(__file__).resolve().parent.parent.parent
    here = root / "GROW_Estate_v3"

    sha = pin_site_sha()
    print(f"   pinned site SHA {sha}")
    site = SiteMount(sha)

    # 1. a real domain-root asset resolves through the site mount
    status, detail = resolve("/hud.js", here / "x.html", root, site)
    if status != OK:
        problems.append(f"/hud.js should resolve through the site mount, got {status}: {detail}")

    # 2. a domain-root path that exists nowhere is still broken
    status, _ = resolve("/definitely-not-a-real-file-9f3a.js", here / "x.html", root, site)
    if status != BROKEN:
        problems.append(f"a nonexistent domain-root path should be broken, got {status}")

    # 3. a missing relative link is still broken
    status, _ = resolve("./nope-9f3a.js", here / "x.html", root, site)
    if status != BROKEN:
        problems.append(f"a missing relative link should be broken, got {status}")

    # 4. FAIL-SAFE: an unreachable mount must be UNVERIFIED, never OK
    dead = SiteMount(sha, timeout=0.001)
    dead._cache.clear()
    status, detail = resolve("/hud.js", here / "x.html", root, dead)
    if status != UNVERIFIED:
        problems.append(f"an unreachable site mount must be unverified, got {status}: {detail}")

    # 5. and a repo-local /Lessons/ path still resolves against this tree
    status, _ = resolve("/Lessons/index.html", here / "x.html", root, site)
    if status != OK:
        problems.append("a /Lessons/ path should resolve against this repository")

    for p in problems:
        print("   FAIL " + p)
    if problems:
        print(f"[FAIL] mount map self-test: {len(problems)} problem(s)")
        return 1
    print("[PASS] mount map self-test: site mount resolves, missing paths still break, "
          "an unreachable mount is unverified rather than green")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--site-sha")
    ap.add_argument("--check", metavar="PATH")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.check:
        sha = a.site_sha or pin_site_sha()
        print(f"pinned site SHA {sha}")
        print(json.dumps(dict(zip(("status", "detail"), SiteMount(sha).lookup(a.check)))))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
