#!/usr/bin/env python3
"""§C3 - leave the assembled tree with ZERO dead internal links.

    python3 tools/pack_links.py PACK_DIR [--fix] [--plant-dead]

THE RULING THIS IMPLEMENTS
--------------------------
The item-17 byte-pristine hold protects the REPO, not the zip. The pack rewrites
links as its core function, so shipping dead links to staff is a pack defect, not
an inherited one. The repo copies of these files are not touched; only the packed
copies are.

THREE CAUSES, THREE DIFFERENT RIGHT ANSWERS
-------------------------------------------
Measured, not assumed. Before this ran, the Mirror carried 48 dead links and the
Network Library carried 5 - and the 43-link gap is the whole diagnosis:

  43  ../../../index.html                      "Back to the Lessons catalogue"
      Resolved in the Network Library, dead in the Mirror. The LINK was never
      wrong; the Mirror was missing the catalogue it names. Fixed by generating
      the offline index into the Mirror too, which repoints nothing and touches
      no page. Repointing 43 links would have been fixing the symptom, and would
      have left the 4 suite indexes self-linking.

   3  ../../../Baseline_Weeks/index.html       "Baseline Weeks (public HTML pack)"
   2  ../../../_sciv3/*/POLICY_ALIGNMENT.md    "Policy alignment"
      Both targets are deliberately OUT of pack scope - Baseline_Weeks is a
      separate public pack, _sciv3/ is the repo's own working directory, excluded
      by name in §9.3. The target is correctly absent, so the link is what has to
      go: the anchor is unwrapped and its text kept, so the page still reads and
      nothing promises a file that was never coming.

Unwrapping rather than deleting matters. The sentence "Baseline Weeks (public HTML
baseline pack)" is information a teacher can act on; the underline that goes
nowhere is not.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

# Targets deliberately excluded from the pack. An anchor pointing at one of these
# is unwrapped. Anything NOT on this list that fails to resolve is a real defect
# and stops the build - this is a named list, never a catch-all.
OUT_OF_SCOPE = {
    "../../../Baseline_Weeks/index.html":
        "a separate public pack, not in this pack's scope",
    "../../../_sciv3/build/POLICY_ALIGNMENT.md":
        "the repo's own working directory - §9.3 excludes _passpq/ and _sciv3/ by name",
    "../../../_sciv3/launch/SOW_AND_POLICY_ALIGNMENT.md":
        "the repo's own working directory - §9.3 excludes _passpq/ and _sciv3/ by name",
}

# The closing quote must MATCH the opening one - a backreference, not a character
# class. `[^"\']+` looked right and quietly truncated every filename containing an
# apostrophe: href="COMM_W2_The_Site\'s_Need.html" was read as a link to
# "COMM_W2_The_Site", which does not exist, so a real file reported as a dead link.
HREF = re.compile(r'(?:href|src)\s*=\s*(["\'])(.*?)\1', re.I | re.S)
SCRIPTY = re.compile(r'<script\b.*?</script>|<style\b.*?</style>', re.S | re.I)


def local_targets(text):
    # Script and style bodies are not markup. Scanning them turned JS template
    # literals - ${src}, ${d.href}, ${S.settings.coverDataURL} - into "dead links".
    text = SCRIPTY.sub(" ", text)
    for _q, raw in HREF.findall(text):
        if raw.startswith(("http:", "https:", "data:", "mailto:", "#", "javascript:", "//")):
            continue
        yield raw


def dead_links(pack):
    """{relative file -> [dead target, ...]} over the assembled tree."""
    out = {}
    for p in sorted(pack.rglob("*.html")):
        text = p.read_text(encoding="utf-8", errors="replace")
        bad = []
        for raw in local_targets(text):
            t = unquote(urlsplit(raw).path)
            if not t:
                continue
            if not (p.parent / t).exists():
                bad.append(raw)
        if bad:
            out[str(p.relative_to(pack))] = bad
    return out


def unwrap(text, target):
    """<a ... href="target" ...>label</a>  ->  label. Count of anchors unwrapped."""
    pat = re.compile(
        r'<a\b[^>]*?href\s*=\s*(["\'])' + re.escape(target) + r'\1[^>]*>(.*?)</a>',
        re.S | re.I)
    return pat.subn(lambda m: m.group(2), text)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: pack_links.py PACK_DIR [--fix] [--plant-dead]")
    pack = Path(args[0])
    fix = "--fix" in sys.argv

    if "--plant-dead" in sys.argv:
        t = pack / "README_FIRST.txt"
        q = pack / "ASDAN PEQ" / "Launch" / "START_HERE.html"
        s = q.read_text(encoding="utf-8")
        q.write_text(s.replace("</body>", '<a href="Nowhere_At_All.html">x</a></body>', 1),
                     encoding="utf-8")
        print("*** PLANTED a dead link in ASDAN PEQ/Launch/START_HERE.html ***")

    unwrapped = 0
    if fix:
        for p in sorted(pack.rglob("*.html")):
            text = p.read_text(encoding="utf-8", errors="replace")
            original = text
            for target in OUT_OF_SCOPE:
                text, n = unwrap(text, target)
                unwrapped += n
            if text != original:
                # §9.6 write discipline: prove the output before opening for writing
                assert text.rstrip().lower().endswith("</html>"), f"{p}: bad tail"
                assert len(text) >= len(original) * 0.5, f"{p}: transform halved the file"
                p.write_text(text, encoding="utf-8")

    remaining = dead_links(pack)
    flat = [(f, t) for f, ts in remaining.items() for t in ts]
    print(f"dead internal links after {'fix' if fix else 'inspection'}: {len(flat)}")
    if unwrapped:
        print(f"anchors unwrapped (target deliberately out of scope): {unwrapped}")
        for t, why in OUT_OF_SCOPE.items():
            print(f"   {t}\n     -> {why}")
    for f, t in flat[:15]:
        print(f"   DEAD  {f} -> {t}")

    print()
    if flat:
        print(f"[FAIL] {len(flat)} dead internal link(s) in the assembled tree")
        return 1
    print("[PASS] 0 dead internal links in the assembled tree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
