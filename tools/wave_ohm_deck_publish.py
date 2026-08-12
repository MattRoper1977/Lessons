#!/usr/bin/env python3
"""Publish the complete WAVE & OHM lesson deck into this repository — Part B's Lessons half.

WHAT THE DECK IS
----------------
One self-contained physics lesson (259,695 B pristine) that carries byte-exact
base64 copies of the WAVE and OHM apps as JSON string literals inside a
`const tools=[…]` array, and mounts each in a sandboxed Blob iframe. Four task
cards, including the Wheatstone investigation.

THE TRAP, THIRD TIME
--------------------
The moment the standalones changed (splash + guard + hud, in Matt-s-Apps-),
the deck's embedded copies went stale. So this build re-encodes both
`"htmlB64"` literals from the FINAL PUBLISHED standalone bytes in the Apps
checkout, and --prove decodes them back out and asserts byte-equality against
those same published files — plus a negative control proving the gate can fail.

Because the embedded copies are the PUBLISHED apps, they carry the frame guard:
the deck splashes once at deck level, and the framed copies keep quiet. The
deck itself is always top-level, so it takes the donor and NO guard.

The donor is read from the site repository's assets/brand/mbm-splash.js — the
same file the estate's own instruments assert against — and its byte-identity
inside the deck is gated here exactly as the estate gates it elsewhere.

The pristine source is the Apps repo's release archive
(_release-docs/wave-ohm-v2-3/), hash-checked before every build.

    python3 tools/wave_ohm_deck_publish.py --build
    python3 tools/wave_ohm_deck_publish.py --prove
    python3 tools/wave_ohm_deck_publish.py --self-test
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import re
from pathlib import Path

LESSONS = Path(__file__).resolve().parent.parent


def _first(*c: Path) -> Path | None:
    for p in c:
        if p.exists():
            return p
    return None


APPS = _first(LESSONS.parent / "matt-s-apps-", Path("/workspace/matt-s-apps-"))
SITE = _first(LESSONS.parent / "mattroper1977.github.io", Path("/workspace/mattroper1977.github.io"))

PRISTINE = APPS / "_release-docs/wave-ohm-v2-3/made-by-matt-wave-ohm-complete-offline-lesson-v2-3.html" if APPS else None
PRISTINE_SHA = "69c3af808e6df9ea3aad5d34c1da08d5dbef78909e19f029d5c73784e9bfe192"

DEST = LESSONS / "Physics_WaveOhm" / "made-by-matt-wave-ohm-complete-offline-lesson-v2-3.html"

# tool id in the deck's array -> the published standalone it must equal
# The deck's own ids, read from its tools array: "wave" and "ohm" — not
# "ohms", which is the HUB's app id for the same tool. Guessed wrong once.
EMBEDS = {
    "wave": "wave-interference-iridescence-engine-v2-3.html",
    "ohm": "ohms-law-fault-finder-v2-3.html",
}

MARKER = ("<!-- mbm-splash-inline: canonical Made by Matt splash, inlined from "
          "the games estate standard. -->")
HUD = '<script defer src="/hud.js"></script>'
SUFFIX = " — Made by Matt"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def donor_text() -> str:
    p = SITE / "assets/brand/mbm-splash.js"
    return p.read_text(encoding="utf-8").strip()


def literal_span(text: str, tool_id: str) -> tuple[int, int]:
    """[start, end) of the base64 inside "htmlB64":"…" for one tool entry.

    Derived, not assumed: anchored on the entry's own "id":"…" then the next
    "htmlB64":" key, ending at the next unescaped quote. The payload is pure
    base64 (verified before every write), so no escape can occur inside it —
    asserted, because an assumption about content is how a splice corrupts.
    """
    entry = text.index(f'"id":"{tool_id}"')
    key = text.index('"htmlB64":"', entry) + len('"htmlB64":"')
    end = text.index('"', key)
    return key, end


def reembed(text: str, payloads: dict[str, bytes]) -> str:
    for tool_id in sorted(payloads, key=lambda k: literal_span(text, k)[0], reverse=True):
        s, e = literal_span(text, tool_id)
        b64 = base64.b64encode(payloads[tool_id]).decode("ascii")
        if not re.fullmatch(r"[A-Za-z0-9+/=]+", b64):
            raise SystemExit("[FAIL] encoder produced non-base64 output — refusing to splice")
        text = text[:s] + b64 + text[e:]
    return text


def splash_and_hud(text: str, donor: str) -> str:
    cut = text.rfind("</body>")
    tail = text[cut + len("</body>"):]
    if not re.fullmatch(r"\s*(?:</html>)?\s*", tail, re.I):
        raise SystemExit(f"[FAIL] content after the last </body> ({tail[:40]!r})")
    parts = [
        f"{MARKER}\n<script>\n{donor}\n</script>",
        # The donor's Skip button inherits the host page's font and lands under
        # 44px on these pages; raised from OUTSIDE the donor block, exactly as
        # the Apps builds do, so the donor stays byte-identical.
        "<style>\n.mbm-splash .mbm-skip{min-height:44px}\n</style>",
        # Always top-level: the deck takes the invocation and NO frame guard.
        "<script>\n(function(){if(window.MadeByMattSplash)window.MadeByMattSplash.start("
        "{title:\"WAVE & OHM INVESTIGATION\"})})();\n</script>",
        HUD,
    ]
    return text[:cut] + "\n" + "\n".join(parts) + "\n" + text[cut:]


def retitle(text: str) -> tuple[str, str]:
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    old = m.group(1)
    mm = re.match(r"Made by Matt\s+—\s+(.*)$", old.strip(), re.S)
    new = (mm.group(1).strip() + SUFFIX) if mm else (old.rstrip() + SUFFIX)
    return text[:m.start(1)] + new + text[m.end(1):], new


def build() -> int:
    data = PRISTINE.read_bytes()
    if sha(data) != PRISTINE_SHA:
        raise SystemExit(f"[FAIL] pristine deck hashes {sha(data)[:16]}, expected {PRISTINE_SHA[:16]}")
    text = data.decode("utf-8")
    text, title = retitle(text)
    text = splash_and_hud(text, donor_text())
    payloads = {k: (APPS / v).read_bytes() for k, v in EMBEDS.items()}
    text = reembed(text, payloads)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(text, encoding="utf-8")
    print(f"  built {DEST.relative_to(LESSONS)}  {len(data)} -> {DEST.stat().st_size} B")
    print(f"        <title> {title!r}")
    for k, v in EMBEDS.items():
        print(f"        embeds {k}: the PUBLISHED {v} ({(APPS / v).stat().st_size} B)")
    return 0


def prove(path: Path = DEST) -> list[str]:
    problems: list[str] = []
    if not path.is_file():
        return [f"{path} not built"]
    text = path.read_text(encoding="utf-8")
    donor = donor_text()

    i = text.find("mbm-splash-inline")
    inlined = text[text.index("<script>", i) + 8:text.index("</script>", i)].strip() if i >= 0 else ""
    print(f"  donor block: {'byte-identical' if inlined == donor else 'DRIFTED'}")
    if inlined != donor:
        problems.append("deck: inlined splash is not the donor")

    code = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    n_start = len(re.findall(r"MadeByMattSplash\.start\(\{title:", code))
    n_guard = code.count("window.MadeByMattSplash.start=function()")
    print(f"  invocations {n_start} (want 1) · frame guards {n_guard} (want 0 — always top-level)")
    if n_start != 1:
        problems.append(f"deck: {n_start} splash invocations")
    if n_guard != 0:
        problems.append(f"deck: {n_guard} frame guards — the deck is never framed")
    if text.count(HUD) != 1:
        problems.append(f"deck: {text.count(HUD)} hud loaders")
    if not re.search(r"<title>.*— Made by Matt</title>", text, re.S):
        problems.append("deck: title lacks the estate suffix")
    if "<title>Made by Matt —" in text:
        problems.append("deck: title still leads with the estate name")

    for tool_id, name in EMBEDS.items():
        s, e = literal_span(text, tool_id)
        dec = base64.b64decode(text[s:e], validate=True)
        want = (APPS / name).read_bytes()
        same = sha(dec) == sha(want)
        print(f"  embed {tool_id:5} decoded {len(dec):>7} B {sha(dec)[:12]} vs published "
              f"{len(want):>7} B {sha(want)[:12]}  {'MATCH' if same else 'DIFFER'}")
        if not same:
            problems.append(f"deck embed {tool_id}: decoded bytes != published {name}")
    return problems


def self_test() -> int:
    """A flipped byte inside one embedded literal must be caught, in memory."""
    problems = []
    text = DEST.read_text(encoding="utf-8")
    s, e = literal_span(text, "wave")
    body = text[s:e]
    flip = "B" if body[100] != "B" else "C"
    sab = text[:s] + body[:100] + flip + body[101:] + text[e:]
    if sab == text:
        problems.append("THE SABOTAGE DID NOT LAND")
    else:
        import tempfile, os
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(sab)
            p = Path(f.name)
        found = [x for x in prove(p) if "decoded bytes" in x or "decode" in x.lower()]
        os.unlink(p)
        print(f"   sabotage: one embedded byte flipped -> {len(found)} finding(s)")
        if not found:
            problems.append("a corrupted embed went unnoticed")
    for x in problems:
        print("   FAIL " + x)
    print("[FAIL] deck self-test" if problems else
          "[PASS] deck self-test: a flipped embedded byte is caught, nothing written to the tree")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--prove", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.build:
        return build()
    if a.self_test:
        return self_test()
    if a.prove:
        problems = prove()
        print()
        if problems:
            print(f"[FAIL] deck gates: {len(problems)} problem(s)")
            for p in problems:
                print("   - " + p)
            return 1
        print("[PASS] deck gates: donor byte-identical, one invocation and no guard, hud once, "
              "title rearranged, and both embedded copies decode byte-equal to the PUBLISHED "
              "standalones in Matt-s-Apps-")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
