#!/usr/bin/env python3
"""
sitemap_audit.py  —  LundyLoop instrument  [LL-INST-07]

WHAT IT DERIVES
  Every URL in the deployed sitemap, and whether it actually resolves.

WHY IT DOES NOT COMPARE REPOSITORIES
  The sitemap lives in the SITE repo and asserts things about the LESSONS repo.
  No instrument can see both, so the claim was unbound: if a catalogued file were
  deleted, the sitemap would keep submitting it to search engines and nothing
  anywhere would notice. A missing or dead sitemap entry HAS NO SYMPTOM — nothing
  breaks, nothing errors, the page simply stops being found.

  The general rule, which is worth more than this tool:

      When a claim spans a boundary no instrument can cross, test the thing the
      claim is ultimately about — not the artefacts on either side of it.

  The sitemap's real assertion is not "these files exist in that repo". It is
  "these URLs resolve". That is testable directly over HTTP with no repo access
  at all, it is indifferent to how the deploy is wired, and it catches a class the
  repo comparison never could: a file that exists but is served wrongly.

USAGE
    python3 sitemap_audit.py [sitemap-url]
  Defaults to https://madebymatt.uk/sitemap.xml

WHAT IT STRUCTURALLY CANNOT DETECT
  - A URL that resolves but serves the WRONG content. 200 is not correctness.
  - A page that should be in the sitemap and is not. This checks the entries that
    exist; it cannot know what is missing. Absence is not visible from here.
  - Anything about crawler behaviour. Resolving is not indexing.

STATUS: current
"""

import re
import sys
import urllib.error
import urllib.request
from collections import Counter

DEFAULT = "https://madebymatt.uk/sitemap.xml"
UA = {"User-Agent": "LundyLoop-sitemap-audit/1.0"}
TIMEOUT = 20


def fetch(url):
    req = urllib.request.Request(url, headers=UA, method="GET")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.status, r.read().decode("utf-8", "replace")


def head(url):
    """HEAD first; some static hosts answer HEAD differently, so fall back to GET."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "GET":
                return e.code
        except Exception as e:                       # noqa: BLE001
            if method == "GET":
                return f"ERROR {type(e).__name__}"
    return "ERROR unreachable"


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    try:
        status, body = fetch(src)
    except Exception as e:                           # noqa: BLE001
        print(f"FAIL — could not fetch the sitemap itself: {src} ({e})")
        print("An unfetchable sitemap is NOT a pass. Nothing below was checked.")
        sys.exit(2)

    urls = re.findall(r"<loc>([^<]+)</loc>", body)
    print(f"sitemap: {src}  ({status})")
    print(f"URLs declared: {len(urls)}")
    if not urls:
        print("FAIL — sitemap fetched but contains no <loc> entries. Not a pass.")
        sys.exit(2)

    results = []
    for u in urls:
        results.append((head(u.strip()), u.strip()))

    counts = Counter(str(c) for c, _ in results)
    bad = [(c, u) for c, u in results if str(c) != "200"]
    print(f"status counts: {dict(counts)}")
    print(f"NOT 200: {len(bad)}")
    for c, u in bad:
        print(f"   {c}  {u}")
    print()
    if bad:
        print(f"FAIL — {len(bad)} of {len(urls)} declared URLs do not resolve.")
        sys.exit(1)
    print(f"All {len(urls)} declared URLs resolve. NOTE: 200 is not correctness, and "
          f"this cannot see pages that SHOULD be listed and are not.")


if __name__ == "__main__":
    main()
