#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_staff_pack.py — rebuild of the pack builder that was never committed (404 on main).
Built FROM REBRAND.md at repo root, not from memory.

Produces three zips:
  1. Progress_Schools_Term_1_1.zip        — OneDrive shared drive (Progress branded)
  2. Progress_Schools_Network_Library.zip — school share + generated offline index
  3. MadeByMatt_Term_1_1_Offline.zip      — unbranded offline copy, hud.js stripped

SAFEGUARDS (each one paid for by a previous failure):
  * NEVER open(p,'w').write(transform(open(p).read())) — the write handle truncates first.
    Read fully -> transform -> ASSERT -> then write. This destroyed Launch/index.html once.
  * Post-condition asserts: output ends </html> AND is > half the input length.
  * Rebrand attributes, not just visible text — 2/3 of wordmark occurrences are in
    aria-label/alt/meta and survive every visual check (REBRAND.md rule 3).
  * x-brand tag added ONLY when the rebrand actually completed in that file.
  * The two '★ ASSESSED LESSON' files: conditions block asserted BYTE-IDENTICAL to repo
    (REGISTER R-A01 — a conditions swap needs Matt's word, every time).
  * Link-crawl the ASSEMBLED pack and report anything the scope rules missed.
    Three real misses were invisible until a crawl ran (hubs, LundyLoop css, the fact
    that BUILD/GROW humanities lessons do NOT live in Humanities_Teesside/).
  * Folder structure preserved EXACTLY — every hub links by relative path.
"""
import re, os, shutil, zipfile, html, sys
from pathlib import Path
from urllib.parse import urlparse, unquote

REPO = Path(os.environ.get("PACK_REPO", "/home/claude/repo"))
OUT  = Path(os.environ.get("PACK_OUT", "/home/claude/pack"))
STRIP = "PROGRESS SCHOOLS · TEES VALLEY"

# ---------------------------------------------------------------- scope
INCLUDE_DIRS = [
    "Art_Teesside", "BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN", "Humanities_Teesside",
    "Grow/Slideshows", "Launch", "Tutor_Time", "DT_Community_Upcycling",
    "Science_Teesside",   # PACK-1 v2: current science suite IN; frozen biology/chemistry/"2 Physics 10" stay OUT
    # PACK-5 (R1, extended): the three v3 alternative-route estates. Each is a
    # self-contained tree with its own hub and subject subfolders, installed as a
    # PARALLEL route -- not a replacement for the existing lessons. They ship as three
    # root-level drive folders and are NOT interleaved into the subject/ASDAN folders:
    # the 30 Jul legacy-art interleaving is the precedent against mixing routes in one
    # folder. R1 as written named only GROW and LAUNCH (installed 11 Aug, 62a92d7);
    # BUILD_Estate_v3 landed a day earlier (10 Aug, cc9f36e) as a structural twin and
    # was ruled in as a third peer rather than quarantined.
    "GROW_Estate_v3", "LAUNCH_Estate_v3", "BUILD_Estate_v3",
    # PACK-5 (R2 quarantine): an 8-page self-contained baseline-assessment pack added
    # 10 Aug (24369a3) and linked from all three Science v3_40min hubs. It is in scope
    # -- real teaching material, and leaving it out breaks three shipping links -- but
    # TAXONOMY_MAP has no folder for it, so it is NOT placed in a subject folder on a
    # guess. It ships under _New_This_Rebuild/ and the link rewrite follows it there.
    # Its own README.md is a "Made by Matt" dev note naming PythonAnywhere: excluded on
    # the dual-branding rule and on the existing "README.md is repo documentation" rule.
    "Baseline_Weeks",
]
INCLUDE_GLOBS = [
    "Build/Slideshows/BUILD_DT_W*.html",
    "Build/Slideshows/BUILD_HUM_W*.html",
]
INCLUDE_FILES = [
    "art_teesside.html", "build_asdan.html", "build_dt_upcycling.html",
    "humanities_teesside.html", "LundyLoop/assets/style.css",
    # Art visual-learning runtime. in_scope() globs *.html, so a directory being in
    # INCLUDE_DIRS does NOT carry its non-HTML assets — same reason style.css above is
    # named individually. All 31 Art_Teesside decks load these three by relative path
    # from inside an AVL-MOUNT marker pair. Without them the loader points at nothing
    # and the We Do panel silently never mounts. README.md in that directory is repo
    # documentation and stays out: only what a deck actually loads ships.
    # PACK-3: the two LundyLoop staff-training pages. The crawl over the
    # assembled pack found 4 Humanities lessons linking to Reading_the_Response_Card
    # by relative path, and that card links on to R_Gate_Calibration_Game. Both
    # exist in the repo; neither was in scope, so the shipped pack had four dead
    # links. Same shape as the Art and ASDAN runtime assets above: a directory in
    # INCLUDE_DIRS does not carry files outside it, so they are named here.
    "LundyLoop/5_staff_training/Reading_the_Response_Card.html",
    "LundyLoop/5_staff_training/R_Gate_Calibration_Game.html",
    "Art_Teesside/visual-learning/art-visual-learning.css",
    "Art_Teesside/visual-learning/art-visual-payloads.js",
    "Art_Teesside/visual-learning/art-visual-learning.js",
    # PACK-2: the GROW/LAUNCH ASDAN visual-upgrade runtime, added for exactly the
    # reason the Art three above were. The crawl over the assembled pack found 124
    # references to these four files from 62 decks that ship, resolving to nothing --
    # by far the largest broken-link family in the pack. GROW_ASDAN and LAUNCH_ASDAN
    # are in INCLUDE_DIRS, but in_scope() globs *.html, so their non-HTML assets were
    # never carried. Same silent failure: the loader points at nothing, offline and on
    # OneDrive, with no error a teacher would see.
    "GROW_ASDAN/visual-upgrade.css",
    "GROW_ASDAN/visual-upgrade.js",
    "LAUNCH_ASDAN/visual-upgrade.css",
    "LAUNCH_ASDAN/visual-upgrade.js",
    # PACK-2: two non-HTML siblings linked from Humanities pages that DO ship. Same
    # class as the runtime assets above -- a directory being IN does not carry them.
    "Humanities_Teesside/Lundy_Humanities/SOURCE_PROVENANCE_TEMPLATE.csv",
    "Humanities_Teesside/Lundy_Humanities/specimens/SPECIMEN_ACCEPTANCE.md",
    # PACK-3: the four grow-anim runtime scripts. Five Science_Teesside/Build decks
    # load them. They were written ROOT-ABSOLUTE, so PACK-2 could not fix them by
    # scope alone and said so. The CI probe has since resolved them against the live
    # origin: in-repo YES, live 404 -- the path was broken in BOTH contexts, because
    # the site serves this repo under /Lessons/. The references are now relative, so
    # the assets must ship or the same loader-points-at-nothing failure returns.
    "grow-anim/grow-svg.js",
    "grow-anim/grow-svg-bio-animals.js",
    "grow-anim/grow-anim.js",
    "grow-anim/compat-build-anim.js",
    # PACK-5: five staff reference docs the v3 estate hubs link to by relative path,
    # out of the working directories (_finish/, _glv3/) the estates were built in.
    # Exactly the class of miss PACK-2 and PACK-3 paid for twice: a directory being in
    # INCLUDE_DIRS does not carry a sibling outside it, so a link from a shipping hub
    # to a non-shipping file dies silently on the drive. Each is referenced from
    # exactly one estate and is filed into that estate's _Route_Docs/ folder.
    "_finish/build_estate/Art_Teesside__ARTIST_IMAGE_PROVENANCE_GUIDE.md",
    "_finish/build_estate/Art_Teesside__SOW_POLICY_AND_AWARD_ALIGNMENT.md",
    "_finish/build_estate/BUILD_ASDAN__CLAIMS_AND_SAFETY_READBACK.md",
    "_glv3/grow/GROW_ASDAN/GROW_ASDAN_CLAIMS_READBACK.md",
    "_glv3/launch/LAUNCH_ASDAN/LAUNCH_ASDAN_CLAIMS_READBACK.md",
    # PACK-5: same class again, for the Science v3_40min hubs that came into scope with
    # the rest of Science_Teesside. Each is linked from exactly one v3_40min hub.
    "_sciv3/build/POLICY_ALIGNMENT.md",
    "_sciv3/launch/SOW_AND_POLICY_ALIGNMENT.md",
]

# PACK-5: Science v3_40min reference docs -> the v3_40min folder that links them.
SCI_V3_DOCS = {
    "_sciv3/build/POLICY_ALIGNMENT.md":         "Science_Teesside/Build/v3_40min/",
    "_sciv3/launch/SOW_AND_POLICY_ALIGNMENT.md": "Science_Teesside/Launch/v3_40min/",
}
# PACK-5 (R2): root folder for in-scope content TAXONOMY_MAP has no home for.
QUARANTINE = "_New_This_Rebuild/"

# GEOMETRY GATE (2026-08-11): the assembled root must be the DRIVE's root, byte for
# byte. This exists because a repo-shaped pack has now been rejected twice (30 Jul,
# 11 Aug); a builder that can zip Art_Teesside/ or BUILD_ASDAN/ at root must fail
# loudly instead. Folders may be ABSENT (the pack ships nothing into Computing/ etc.);
# nothing outside this list may be PRESENT.
DRIVE_ROOT_FOLDERS = {
    "Art", "ASDAN PEQ", "Computing", "Curriculum Intent and Rationale", "English",
    "Feedback and Marking", "grow-anim",
    "Humanities Lessons (Whiteboards and resources)", "Lesson Slideshows_Resources",
    "LundyLoop", "Science_Teesside", "SMSC and BV Calendar Evidence",
    "Tutor Time BF_BV_KCSIE", "Weekly Plans",
    "GROW Estate v3 (Alternative Route)", "LAUNCH Estate v3 (Alternative Route)",
    # Ruled in by Matt 11 Aug (extension of R1): the third, structurally identical
    # estate, installed 10 Aug. Peer of the two the corrective list names.
    "BUILD Estate v3 (Alternative Route)",
    "_New_This_Rebuild", "_Pack_Notes",
}
# The repo-tree names whose appearance at root IS the failure being gated against.
REPO_ROOT_NAMES = {
    "Art_Teesside", "BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN",
    "Humanities_Teesside", "Tutor_Time", "Build", "Grow", "Launch",
    "DT_Community_Upcycling", "GROW_Estate_v3", "LAUNCH_Estate_v3", "BUILD_Estate_v3",
}
DRIVE_ROOT_FILES = {
    "art_teesside.html", "build_asdan.html", "build_dt_upcycling.html",
    "humanities_teesside.html", "README_FIRST.txt", "CHANGES_SINCE.html",
    "PLACEMENT_GUIDE.txt",
}
# These drive folders hold this pack's content, so their absence means assembly
# silently dropped a subject — required present.
DRIVE_ROOT_REQUIRED = {
    "ASDAN PEQ", "Art", "Science_Teesside",
    "Humanities Lessons (Whiteboards and resources)", "Tutor Time BF_BV_KCSIE",
    "grow-anim", "LundyLoop",
    "GROW Estate v3 (Alternative Route)", "LAUNCH Estate v3 (Alternative Route)",
    "BUILD Estate v3 (Alternative Route)",
}


def geometry_gate(pack):
    """Assert the assembled root is the drive root. Returns (fails, table_lines)."""
    fails, table = [], []
    entries = sorted(pack.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    table.append(f"{'root entry':<52} {'kind':<7} verdict")
    table.append("-" * 78)
    for e in entries:
        if e.is_dir():
            if e.name in DRIVE_ROOT_FOLDERS:
                v = "OK - drive folder"
            elif e.name in REPO_ROOT_NAMES:
                v = "FAIL - REPO-TREE NAME AT ROOT"
                fails.append(f"geometry: repo-tree folder at root: {e.name}")
            else:
                v = "FAIL - not a drive root folder"
                fails.append(f"geometry: unknown root folder: {e.name}")
            table.append(f"{e.name + '/':<52} {'folder':<7} {v}")
        else:
            v = "OK - allowed root file" if e.name in DRIVE_ROOT_FILES \
                else "FAIL - not an allowed root file"
            if e.name not in DRIVE_ROOT_FILES:
                fails.append(f"geometry: unexpected root file: {e.name}")
            table.append(f"{e.name:<52} {'file':<7} {v}")
    present = {e.name for e in entries if e.is_dir()}
    for req in sorted(DRIVE_ROOT_REQUIRED):
        if req not in present:
            fails.append(f"geometry: required drive folder ABSENT: {req}")
            table.append(f"{req + '/':<52} {'folder':<7} FAIL - REQUIRED, ABSENT")
    return fails, table

# PACK-5: repo prefix -> drive folder for the three alternative-route estates.
ESTATE_V3 = {
    "GROW_Estate_v3/":   "GROW Estate v3 (Alternative Route)/",
    "LAUNCH_Estate_v3/": "LAUNCH Estate v3 (Alternative Route)/",
    "BUILD_Estate_v3/":  "BUILD Estate v3 (Alternative Route)/",
}
# Which estate each carried-in reference doc belongs to (the estate that links it).
ROUTE_DOCS = {
    "_finish/build_estate/Art_Teesside__ARTIST_IMAGE_PROVENANCE_GUIDE.md": "BUILD_Estate_v3/",
    "_finish/build_estate/Art_Teesside__SOW_POLICY_AND_AWARD_ALIGNMENT.md": "BUILD_Estate_v3/",
    "_finish/build_estate/BUILD_ASDAN__CLAIMS_AND_SAFETY_READBACK.md": "BUILD_Estate_v3/",
    "_glv3/grow/GROW_ASDAN/GROW_ASDAN_CLAIMS_READBACK.md": "GROW_Estate_v3/",
    "_glv3/launch/LAUNCH_ASDAN/LAUNCH_ASDAN_CLAIMS_READBACK.md": "LAUNCH_Estate_v3/",
}
# The dynamic hud.js injector. Self-contained script element, byte-identical across
# the five decks that carry it, and its entire body exists to load hud.js.
HUD_DYNAMIC = re.compile(
    r'\s*<script[^>]*id=["\']grow-hud-loader["\'][^>]*>.*?</script>', re.S | re.I)

# Deliberate exclusions (dual-branding rule + superseded sets)
EXCLUDE_RE = re.compile(
    r"(^Games/)"                                   # games are Made by Matt only
    r"|(^Build/Slideshows/BUILD_ART_W\d_)"         # legacy tasters ONLY - NOT Art_Teesside/Build/
    r"|(BUILD_L1_)|(FW_L1_)"                       # superseded by BUILD_ASDAN/
    r"|(^ASDAN/)"                                  # consent forms, not lessons
    r"|(^404\.html)|(^index\.html)|(^hub-health)"  # site furniture
)

def in_scope():
    seen = []
    for d in INCLUDE_DIRS:
        for p in sorted((REPO / d).rglob("*.html")):
            seen.append(p.relative_to(REPO))
    for g in INCLUDE_GLOBS:
        for p in sorted(REPO.glob(g)):
            seen.append(p.relative_to(REPO))
    for f in INCLUDE_FILES:
        p = REPO / f
        if p.exists():
            seen.append(p.relative_to(REPO))
    out, drop = [], []
    for r in seen:
        (drop if EXCLUDE_RE.search(str(r)) else out).append(r)
    return sorted(set(out)), sorted(set(drop))

# ---------------------------------------------------------------- rebrand
MARK_SVG = re.compile(r'<svg[^>]*aria-label="Made by Matt"[^>]*>.*?</svg>', re.S | re.I)
PS_MARK = (
    '<span aria-label="Progress Schools Tees Valley" role="img" '
    'style="display:inline-flex;align-items:center;justify-content:center;'
    'width:64px;height:64px;border:2px solid currentColor;border-radius:8px;'
    'font:700 26px/1 system-ui,sans-serif;letter-spacing:1px">PS</span>'
    '<span style="margin-left:.6rem;font:600 11px/1 system-ui,sans-serif;'
    'letter-spacing:.08em;white-space:nowrap">' + "PROGRESS SCHOOLS \u00b7 TEES VALLEY" + '</span>'
)

def rebrand(text, path):
    """Return (new_text, changelog dict). Pure function — does no I/O."""
    log = {}
    n0 = len(text)

    # 1 · typographic mark replaces the drawn Made by Matt logo (REBRAND rule 1)
    text, k = MARK_SVG.subn(PS_MARK, text)
    log["logo_swapped"] = k

    # 2 · attribute-borne wordmarks FIRST — rule 3's trap, 2/3 of all occurrences
    k = 0
    for attr in ("aria-label", "alt", "title", "content"):
        pat = re.compile(rf'({attr}=")([^"]*?)Made by Matt([^"]*?)(")', re.I)
        text, n = pat.subn(lambda m: m.group(1) + m.group(2) + "Progress Schools" + m.group(3) + m.group(4), text)
        k += n
    log["attr_wordmarks"] = k

    # 3 · domain wording, href values included (rule 4)
    text, k1 = re.subn(r'https?://(www\.)?madebymatt\.uk[^\s"\'<>)]*', "#", text)
    # C7 follow-on: the domain sweep only ever knew madebymatt.uk, but the estate
    # also links to the personal GitHub Pages origin that serves this repo
    # ("Lesson Hub" buttons in Art/Launch/index.html). REBRAND.md rule 4 is about
    # sending staff to a personal public site, not about one spelling of it.
    text, k4 = re.subn(PERSONAL_ORIGINS, "#", text)
    text, k2 = re.subn(r'contactmadebymatt@gmail\.com', "your Progress Schools science lead", text)
    text, k3 = re.subn(r'madebymatt\.uk', "Progress Schools Tees Valley", text, flags=re.I)
    log["domain"] = k1 + k2 + k3

    # 4 · remaining visible wordmark, including the UPPERCASE form Tutor Time uses
    text, k1 = re.subn(r'MADE BY MATT', "PROGRESS SCHOOLS", text)
    text, k2 = re.subn(r'Made by Matt', "Progress Schools", text)
    log["wordmark_text"] = k1 + k2
    # dedupe the name+domain side-by-side double-replace (recorded trap)
    text = re.sub(r'Progress Schools\s*[·\-–—|]\s*Progress Schools Tees Valley',
                  "Progress Schools Tees Valley", text)
    text = re.sub(r'(Progress Schools Tees Valley)(\s*\1)+', r'\1', text)

    # 5 · strip the hud.js loader — only ever loads from the public origin
    text, k = re.subn(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", text, flags=re.I)
    # 5b · and the DYNAMIC loader, which the tag regex above cannot see. Five
    # Science_Teesside/Grow decks carry <script id="grow-hud-loader"> whose whole body
    # is document.createElement("script") + s.src="/hud.js" with a relative-path
    # onerror retry. It survived every previous pack build: the staff copies shipped
    # fetching hud.js at runtime, twice, from a machine that has neither. Found by
    # grepping the ASSEMBLED pack for hud.js rather than trusting the strip count.
    text, k2 = re.subn(HUD_DYNAMIC, "", text)
    log["hud_stripped"] = k + k2

    # 6 · x-brand marker, added last and only if the rebrand actually completed here
    if 'name="x-brand"' not in text:
        text, k = re.subn(r'(<head[^>]*>)', r'\1\n<meta name="x-brand" content="progress-schools">',
                          text, count=1, flags=re.I)
        log["xbrand"] = k
    log["delta"] = len(text) - n0
    return text, log

def write_guarded(src_text, new_text, dest):
    """Post-condition asserts BEFORE any write handle is opened."""
    if "</html>" in src_text.lower():
        assert new_text.rstrip().lower().endswith("</html>"), f"{dest}: lost closing </html>"
    assert len(new_text) > len(src_text) * 0.5, f"{dest}: suspicious shrink {len(src_text)}->{len(new_text)}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(new_text, encoding="utf-8")

# ---------------------------------------------------------------- crawl
HREF = re.compile(r'(?:href|src)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.I)

def crawl(root):
    """Return internal link targets that are missing from the assembled tree."""
    missing = {}
    for p in root.rglob("*.html"):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for dq, sq in HREF.findall(t):
            raw = html.unescape(dq or sq)
            if "${" in raw or "{{" in raw:   # JS template literal, not a link
                continue
            if raw.startswith(("http://", "https://", "#", "data:", "mailto:", "javascript:")):
                continue
            target = unquote(urlparse(raw).path)
            if not target:
                continue
            resolved = (p.parent / target).resolve()
            if not resolved.exists():
                missing.setdefault(str(p.relative_to(root)), set()).add(target)
    return missing

# ---------------------------------------------------------------- AVL gates
# Two gates for the Art visual-learning layer. Both exist because the rebrand
# transform strips the hud.js loader (rebrand step 5), and the AVL marker pair sits
# directly after that loader in all 31 decks. A regex that reached one character too
# far would silently remove the panel from every staff copy.
AVL_BLOCK = re.compile(r"<!-- AVL-MOUNT:BEGIN.*?AVL-MOUNT:END -->", re.S)

def avl_blocks(text):
    return AVL_BLOCK.findall(text)

def check_avl_preserved(src_text, new_text, rel):
    """AVL-1: the rebrand transform must leave the marker pair byte-identical.

    Compares the extracted blocks, not the whole file — the rest of the file is
    supposed to change. Returns a failure string, or None."""
    before, after = avl_blocks(src_text), avl_blocks(new_text)
    if before != after:
        return (f"AVL-1 VIOLATION: {rel}: rebrand altered the AVL marker pair "
                f"({len(before)} block(s) in, {len(after)} out)")
    return None

def check_avl_refs(pack: Path):
    """AVL-2: every reference inside a marker pair resolves to a file in the pack.

    The general crawl only reports; this one fails the build. A loader that points at
    nothing produces no error a teacher would ever see — the panel just never mounts."""
    fails = []
    for p in sorted(pack.rglob("*.html")):
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for blk in avl_blocks(t):
            for dq, sq in HREF.findall(blk):
                raw = html.unescape(dq or sq)
                # A root-relative "/x" resolves against the public origin, not the pack,
                # so it is just as broken offline as a missing file — and it must be
                # named as the absolute path it is, not reported as "missing".
                if raw.startswith(("http://", "https://", "//", "/", "#", "data:")):
                    fails.append(f"AVL-2: {p.relative_to(pack)} -> {raw} is not a relative path")
                    continue
                target = unquote(urlparse(raw).path)
                if not target:
                    continue
                if not (p.parent / target).resolve().exists():
                    fails.append(f"AVL-2: {p.relative_to(pack)} -> {raw} missing from pack")
    return fails

# ---------------------------------------------------------------- verify
def verify(pack: Path, branded: bool):
    fails, notes = [], {}
    files = list(pack.rglob("*.html"))
    notes["html_files"] = len(files)
    a = b = c = d = 0
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'(aria-label|alt|content|title)="[^"]*made by matt', t, re.I): a += 1
        if re.search(r'madebymatt', t, re.I): b += 1
        if 'name="x-brand"' not in t: c += 1
        if STRIP in t: d += 1
        if not t.rstrip().lower().endswith("</html>"): fails.append(f"{p.name}: no closing </html>")
        if len(t) < 200: fails.append(f"{p.name}: suspiciously small ({len(t)}b)")
    notes["attr_residue"] = a; notes["domain_residue"] = b
    notes["missing_xbrand"] = c; notes["carry_strip"] = d
    if branded:
        if a: fails.append(f"REBRAND check 1 FAILED: {a} files with wordmark in an attribute")
        if b: fails.append(f"REBRAND check 2 FAILED: {b} files still name the domain")
        if c: fails.append(f"REBRAND check 3 FAILED: {c} files missing the x-brand marker")
        if d == 0: fails.append("REBRAND check 4 FAILED: no file carries the TEES VALLEY strip")
    return fails, notes

# ---------------------------------------------------------------- main
def main():
    keep, dropped = in_scope()
    print(f"scope: {len(keep)} files in, {len(dropped)} deliberately excluded")

    if OUT.exists(): shutil.rmtree(OUT)
    ps  = OUT / "Progress_Schools_Term_1_1"
    mbm = OUT / "MadeByMatt_Term_1_1_Offline"

    # capture the assessed-file conditions blocks BEFORE anything is touched
    assessed = {}
    for rel in keep:
        src = REPO / rel
        if src.suffix == ".html":
            t = src.read_text(encoding="utf-8", errors="ignore")
            if "★ ASSESSED LESSON" in t:
                m = re.search(r'★ ASSESSED LESSON.{0,2000}', t, re.S)
                assessed[str(rel)] = m.group(0) if m else None
    print(f"assessed files locked: {len(assessed)}")

    totals = {}
    avl_fails = []
    avl_seen = 0
    for rel in keep:
        src = REPO / rel
        raw = src.read_text(encoding="utf-8", errors="ignore")
        if src.suffix == ".html":
            new, log = rebrand(raw, rel)
            for k, v in log.items():
                if k != "delta": totals[k] = totals.get(k, 0) + v
            # AVL-1, checked BEFORE the write, on every file that carries a marker pair
            if avl_blocks(raw):
                avl_seen += 1
                f = check_avl_preserved(raw, new, rel)
                if f: avl_fails.append(f)
            write_guarded(raw, new, ps / rel)
            # unbranded offline copy: hud.js stripped only
            plain = re.sub(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", raw, flags=re.I)
            plain = HUD_DYNAMIC.sub("", plain)
            write_guarded(raw, plain, mbm / rel)
        else:
            for dest in (ps / rel, mbm / rel):
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
    print("rebrand totals:", totals)

    # R-A01: conditions blocks must be byte-identical to the repo
    for relstr, block in assessed.items():
        if block is None: continue
        got = (ps / relstr).read_text(encoding="utf-8", errors="ignore")
        core = re.sub(r'Made by Matt|MADE BY MATT|madebymatt\.uk', "", block)
        core = re.sub(r'\s+', " ", core).strip()[:400]
        haystack = re.sub(r'\s+', " ", got)
        assert core in haystack, f"R-A01 VIOLATION: conditions block altered in {relstr}"
    print(f"R-A01: {len(assessed)} assessed conditions blocks intact")

    # crawl the assembled pack
    miss = crawl(ps)
    if miss:
        print(f"\nCRAWL: {len(miss)} files reference {sum(len(v) for v in miss.values())} missing targets")
        for f, ts in list(miss.items())[:12]:
            print(f"  {f} -> {', '.join(sorted(ts))[:110]}")
    else:
        print("\nCRAWL: clean, no missing internal targets")

    # AVL-1 result, and AVL-2 against the assembled pack
    print(f"\nAVL-1: {avl_seen} decks carry a marker pair; "
          f"{'all preserved byte-for-byte' if not avl_fails else str(len(avl_fails)) + ' ALTERED'}")
    for f in avl_fails[:10]: print("  FAIL:", f)
    ref_fails = check_avl_refs(ps)
    print(f"AVL-2: loader references inside marker pairs "
          f"{'all resolve inside the pack' if not ref_fails else 'BROKEN'}")
    for f in ref_fails[:10]: print("  FAIL:", f)
    avl_fails = avl_fails + ref_fails

    fails, notes = verify(ps, branded=True)
    fails = fails + avl_fails
    print("\nVERIFY (Progress pack):", notes)
    for f in fails[:20]: print("  FAIL:", f)
    if not fails: print("  all REBRAND.md checks pass")
    return ps, mbm, keep, dropped, miss, fails

# ==================================================================== MIRROR
# PACK-4: the OneDrive Mirror Pack.
#
# Everything below is additive. The default build path above is untouched: it
# still preserves the repo tree, because its links assume the repo tree.
#
# This mode does the opposite, and is only safe because it does BOTH halves:
# it assembles into the school's folder geometry AND rewrites every internal
# link against the same map. Zip geometry == drive geometry, so a link between
# two co-shipped folders resolves after a drag-and-merge. Do one half without
# the other and every cross-folder link in the pack dies.
#
# The map below was derived from 35 screenshots of the live drive (2026-08-07),
# not from the repo and not from memory. Where the repo and the drive disagree
# on a name, THE DRIVE WINS — that is the whole point of a mirror.
import base64, argparse, io
from urllib.parse import quote

# The Humanities folder name is truncated in every screenshot that shows it:
#   root listing : "Humanities Less...s and resources)"
#   title bar    : "Humanities Lessons (Whiteboards..."
# The overlap fixes everything except a possible middle word. This is the
# pack's ONE unresolved name and it is flagged, not guessed silently.
HUM = "Humanities Lessons (Whiteboards and resources)"
HUM_AMBIGUOUS = True

# LAUNCH_ASDAN is FLAT on the drive: CAREERS_*, COMM_*, LI_*, PEQ_* and VOC_*
# all sit directly in "ASDAN PEQ/Launch". The repo keeps them in five
# subfolders, and each of those has its own START_HERE.html -- so a naive
# flatten silently destroys four of the five. They are disambiguated instead,
# and every rename is recorded in TAXONOMY_MAP.md.
LAUNCH_SUBS = {
    "Careers": "Careers", "Community_Enterprise": "Community_Enterprise",
    "Living_Independently": "Living_Independently", "PEQ": "PEQ",
    "Vocational": "Vocational",
}
HONESTY_LINE = ""
LOGO_URI = [None, None]   # filled by build_mirror, read by the index writer
LOGO_HTML = [None]        # the rendered lockup, reused by generated pages
LOGO_SHA = "b112fd98e3368f73df4da5588a04238ee4a816b56007ba60e2e63d0286cbdb04"
RENAMES = []          # (repo path, dest path, why) — reported, never silent

def dest_for(rel):
    """Map one in-scope repo path to its OneDrive destination path.

    Ordered, longest-match-first. Returns a POSIX-style string."""
    r = str(rel).replace("\\", "/")
    name = r.rsplit("/", 1)[-1]

    # --- root unit hubs: canonical single placement at the drive root
    if "/" not in r:
        return r

    # --- PACK-5: the three v3 alternative-route estates ---------------------
    # Self-contained trees. Structure is preserved verbatim under a renamed root, so
    # every link inside an estate keeps the same relative shape and survives the move.
    # Checked before the subject rules below: an estate path looks like
    # "GROW_Estate_v3/Art_Teesside/..." and must NOT be caught by the Art rule and
    # interleaved into the shared Art folder.
    for pre, dst in ESTATE_V3.items():
        if r.startswith(pre):
            return dst + r[len(pre):]
    if r in ROUTE_DOCS:
        return ESTATE_V3[ROUTE_DOCS[r]] + "_Route_Docs/" + name
    if r in SCI_V3_DOCS:
        return SCI_V3_DOCS[r] + "_Route_Docs/" + name

    # --- PACK-5 (R2): quarantine, repo-relative structure preserved ---------
    if r.startswith("Baseline_Weeks/"):
        return QUARANTINE + r

    # --- Art -------------------------------------------------------------
    if r.startswith("Art_Teesside/"):
        return "Art/" + r[len("Art_Teesside/"):]
    if r.startswith("Grow/Slideshows/GROW_ART_"):
        return "Art/Grow/" + name
    if r.startswith("Launch/Slideshows/LAUNCH_ART_"):
        return "Art/Launch/" + name
    if r in ("Launch/index.html",) or r.startswith("Launch/Art_L"):
        return "Art/Launch/" + name

    # --- Humanities ------------------------------------------------------
    if r.startswith("Build/Slideshows/BUILD_HUM_"):
        return f"{HUM}/Build/" + name
    if r.startswith("Grow/Slideshows/GROW_HUM_"):
        return f"{HUM}/Grow/" + name
    if r.startswith("Launch/Slideshows/LAUNCH_HUM_"):
        return f"{HUM}/Launch/" + name
    if r.startswith("Humanities_Teesside/Lundy_Humanities/specimens/"):
        return f"{HUM}/LundyLoop/Specimens/" + name
    if r.startswith("Humanities_Teesside/Lundy_Humanities/"):
        return f"{HUM}/LundyLoop/" + name
    if r.startswith("Humanities_Teesside/"):
        for pre, sub in (("BUILD_", "Build"), ("GROW_", "Grow"), ("LAUNCH_", "Launch")):
            if name.startswith(pre):
                return f"{HUM}/{sub}/" + name
        return f"{HUM}/" + name          # Pathway_Tracker.html

    # --- ASDAN PEQ -------------------------------------------------------
    if r.startswith("Build/Slideshows/BUILD_DT_"):
        return "ASDAN PEQ/Build/DT/" + name
    if r.startswith("DT_Community_Upcycling/"):
        return "ASDAN PEQ/Build/DT/" + name
    if r.startswith("BUILD_ASDAN/"):
        return "ASDAN PEQ/Build/" + r[len("BUILD_ASDAN/"):]
    if r.startswith("GROW_ASDAN/"):
        tail = r[len("GROW_ASDAN/"):]
        for src, dst in (("Community_Project/", "Community Project/"),
                         ("Enterprise/", "Community and Enterprise/"),
                         ("PEQ/", "Personal Effectiveness/")):
            if tail.startswith(src):
                return "ASDAN PEQ/Grow/" + dst + tail[len(src):]
        return "ASDAN PEQ/Grow/" + tail
    if r.startswith("LAUNCH_ASDAN/"):
        tail = r[len("LAUNCH_ASDAN/"):]
        if "/" in tail:                                  # inside a subfolder -> FLATTEN
            sub, leaf = tail.split("/", 1)
            if leaf == "START_HERE.html":                # 5-way collision
                new = f"START_HERE_{sub}.html"
                RENAMES.append((r, f"ASDAN PEQ/Launch/{new}",
                                "flattened; 5 subfolder START_HEREs would collide on one name"))
                return "ASDAN PEQ/Launch/" + new
            return "ASDAN PEQ/Launch/" + leaf
        return "ASDAN PEQ/Launch/" + tail

    # --- unchanged names --------------------------------------------------
    if r.startswith("Tutor_Time/"):
        return "Tutor Time BF_BV_KCSIE/" + r[len("Tutor_Time/"):]
    if r.startswith(("Science_Teesside/", "grow-anim/", "LundyLoop/")):
        return r
    raise AssertionError(f"dest_for: no rule for {r}")


def build_index(keep):
    """repo-rel -> dest-rel, and the reverse, with collision detection."""
    fwd, back = {}, {}
    for rel in keep:
        d = dest_for(rel)
        if d in back and back[d] != str(rel):
            raise AssertionError(f"DESTINATION COLLISION: {back[d]} and {rel} both -> {d}")
        fwd[str(rel)] = d
        back[d] = str(rel)
    return fwd, back


def rewrite_links(text, src_rel, fwd, dest_override=None):
    """Rewrite every internal href/src from repo geometry to drive geometry.

    Resolves each link against the SOURCE file's directory to find which repo
    file it means, then re-expresses it relative to the DESTINATION directory.
    A link whose target is not in the pack is left alone and reported by the
    crawl -- it is never silently rewritten to something that happens to exist."""
    src_dir = os.path.dirname(str(src_rel))
    dst_dir = os.path.dirname(dest_override or fwd[str(src_rel)])
    changed = [0]

    def one(m):
        attr, q, raw = m.group(1), m.group(2), m.group(3)
        if (not raw or raw.startswith(("http://", "https://", "//", "#", "data:",
                                       "mailto:", "javascript:", "/"))
                or "${" in raw or "{{" in raw):
            return m.group(0)
        parts = urlparse(raw)
        target = unquote(parts.path)
        if not target:
            return m.group(0)
        repo_target = os.path.normpath(os.path.join(src_dir, target)).replace("\\", "/")
        if repo_target not in fwd:
            return m.group(0)                       # unknown -> leave, crawl reports it
        new = os.path.relpath(fwd[repo_target], dst_dir or ".").replace("\\", "/")
        if parts.query:    new += "?" + parts.query
        if parts.fragment: new += "#" + parts.fragment
        if new != raw:
            changed[0] += 1
        return f'{attr}={q}{new}{q}'

    text = re.sub(r'\b(href|src)\s*=\s*(["\'])(.*?)\2', one, text, flags=re.I | re.S)
    return text, changed[0]


# ---------------------------------------------------------------- the logo
# REBRAND.md rule 1 said the mark is typographic and never drawn. Matt has
# since supplied the real Progress Schools lockup, which SUPERSEDES that rule:
# the trademark now replaces the Made-by-Matt mark directly. What does not
# change is that it is never recoloured, restyled, stretched or redrawn --
# it is embedded as-is, and only ever scaled by width with height:auto so the
# aspect ratio cannot drift.
# D1 -- every spelling of "Matt's own public presence" the repo census turned up.
# Rule 4 is about sending staff to a personal site, not about one spelling of it.
# Named alternates, so adding the next one is a one-line change and the verify
# sweep and the rewrite can never drift apart.
PERSONAL_ORIGIN_FORMS = (
    r'(?:www\.)?madebymatt\.uk',            # the custom domain (canonical)
    r'mattroper1977\.github\.io',           # the GitHub Pages origin it fronts
    r'mattroper1977\.pythonanywhere\.com',  # the live-lessons app
    r'ko-fi\.com/madebymattuk',              # the donation link on the public index
)
PERSONAL_ORIGINS = re.compile(
    r'https?://(?:' + "|".join(PERSONAL_ORIGIN_FORMS) + r')[^\s"\'<>)]*', re.I)
PERSONAL_RESIDUE = re.compile(
    "|".join(PERSONAL_ORIGIN_FORMS) + r'|madebymatt', re.I)

CREDIT = "by madebymatt.uk"      # Matt's explicit instruction; the ONE whitelisted
                                 # Made-by-Matt string. Anything else is residue.

def load_logo(path):
    """Trim the supplied PNG, split the lockup from the P mark, return data URIs.

    The binary stays out of git, so its SHA is recorded here and in REBRAND.md:
    without it the pack is not reproducible from the repo alone."""
    import hashlib
    from PIL import Image, ImageChops
    got = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert got == LOGO_SHA, (
        f"logo SHA mismatch\n  expected {LOGO_SHA}\n  got      {got}\n"
        "Refusing to build: this is not the supplied Progress Schools lockup.")
    im = Image.open(path).convert("RGBA")
    flat = Image.new("RGB", im.size, (255, 255, 255))
    flat.paste(im, mask=im.split()[3])
    bbox = ImageChops.difference(flat, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    lock = flat.crop(bbox)
    # the P mark is everything left of the first wide blank column run
    w, h = lock.size
    px = lock.load()
    ink = [any(px[x, y][:3] != (255, 255, 255) for y in range(h)) for x in range(w)]
    split = w
    run = None
    for x, v in enumerate(ink):
        if not v:
            run = x if run is None else run
        else:
            if run is not None and x - run >= 4:
                split = run
                break
            run = None
    mark = lock.crop((0, 0, split, h))
    mb = ImageChops.difference(mark, Image.new("RGB", mark.size, (255, 255, 255))).getbbox()
    mark = mark.crop(mb)

    def uri(img):
        best = None
        for colors in (16, 32, 64, 128):
            p = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
            buf = io.BytesIO(); p.save(buf, format="PNG", optimize=True)
            d = buf.getvalue()
            if best is None or len(d) <= 10240:
                best = d
        assert len(best) <= 10240, f"logo asset {len(best)}b exceeds the 10 KB budget"
        return "data:image/png;base64," + base64.b64encode(best).decode(), img.size
    return uri(lock), uri(mark)


def logo_html(lock_uri, lock_size):
    """The lockup on a white chip. The chip keeps it legible on a dark header;
    on a light one it is invisible. Either way the artwork is untouched."""
    w, h = lock_size
    return (
        '<span class="ps-logo" style="display:inline-block;background:#fff;'
        'border-radius:8px;padding:6px 10px;line-height:0">'
        f'<img src="{lock_uri}" width="{w}" height="{h}" alt="Progress Schools" '
        'style="width:92px;height:auto;display:block">'
        '</span>'
        '<span style="display:block;margin-top:.45rem;font:600 11px/1 system-ui,sans-serif;'
        'letter-spacing:.08em;white-space:nowrap">' + STRIP + '</span>'
    )


CREDIT_HTML = (
    '<div class="ps-credit" style="text-align:center;font:400 10px/1.4 system-ui,sans-serif;'
    'opacity:.55;margin:10px 0 4px;letter-spacing:.02em">' + CREDIT + '</div>'
)



def insert_credit(text):
    """Put the credit at the document's real end.

    NOT a plain re.sub on '</body>': these decks build printable views with
    w.document.write('<html>...</body></html>'), so the FIRST </body> in the
    file is inside a JavaScript string literal. Injecting HTML there produced
    an unterminated string and broke the deck's whole script block. The real
    tag is the last one with nothing but whitespace and </html> after it."""
    for tag in ("</body>", "</html>"):
        for m in reversed(list(re.finditer(re.escape(tag), text, re.I))):
            if re.fullmatch(r'\s*(</html>)?\s*', text[m.end():], re.I):
                return text[:m.start()] + CREDIT_HTML + "\n" + text[m.start():]
    return text + "\n" + CREDIT_HTML + "\n"


def brand_header(text, mark_html):
    """Put the lockup at the top of a page that never carried a drawn mark.

    Used for the hubs and for pages this build authors. Inserted as the first
    thing in <body> so it sits above whatever heading the page already has."""
    if 'alt="Progress Schools"' in text:
        return text, 0
    block = ('<div style="text-align:center;margin:14px 0 4px">' + mark_html + "</div>")
    new, n = re.subn(r'(<body[^>]*>)', r'\1\n' + block.replace("\\", "\\\\"), text,
                     count=1, flags=re.I)
    return new, n


def mirror_rebrand(text, rel, mark_html):
    """The standard rebrand, with the real logo and the credit."""
    log = {}
    n0 = len(text)
    text, k = MARK_SVG.subn(lambda m: mark_html, text)
    log["logo_swapped"] = k
    k = 0
    for attr in ("aria-label", "alt", "title", "content"):
        pat = re.compile(rf'({attr}=")([^"]*?)Made by Matt([^"]*?)(")', re.I)
        text, n = pat.subn(lambda m: m.group(1) + m.group(2) + "Progress Schools" + m.group(3) + m.group(4), text)
        k += n
    log["attr_wordmarks"] = k
    text, k1 = re.subn(r'https?://(www\.)?madebymatt\.uk[^\s"\'<>)]*', "#", text)
    # C7 follow-on: the domain sweep only ever knew madebymatt.uk, but the estate
    # also links to the personal GitHub Pages origin that serves this repo
    # ("Lesson Hub" buttons in Art/Launch/index.html). REBRAND.md rule 4 is about
    # sending staff to a personal public site, not about one spelling of it.
    text, k4 = re.subn(PERSONAL_ORIGINS, "#", text)
    text, k2 = re.subn(r'contactmadebymatt@gmail\.com', "your Progress Schools science lead", text)
    text, k3 = re.subn(r'madebymatt\.uk', "Progress Schools Tees Valley", text, flags=re.I)
    log["domain"] = k1 + k2 + k3 + k4
    text, k1 = re.subn(r'MADE BY MATT', "PROGRESS SCHOOLS", text)
    text, k2 = re.subn(r'Made by Matt', "Progress Schools", text)
    log["wordmark_text"] = k1 + k2
    text = re.sub(r'Progress Schools\s*[·\-–—|]\s*Progress Schools Tees Valley',
                  "Progress Schools Tees Valley", text)
    text = re.sub(r'(Progress Schools Tees Valley)(\s*\1)+', r'\1', text)
    text, k = re.subn(r'\s*<script[^>]*hud\.js[^>]*>\s*</script>', "", text, flags=re.I)
    text, k2 = re.subn(HUD_DYNAMIC, "", text)
    log["hud_stripped"] = k + k2
    if 'name="x-brand"' not in text:
        text, k = re.subn(r'(<head[^>]*>)', r'\1\n<meta name="x-brand" content="progress-schools">',
                          text, count=1, flags=re.I)
        log["xbrand"] = k
    # the credit goes in LAST, after the domain sweep above has run, or it
    # would be rewritten into "Progress Schools Tees Valley" like any other
    # mention of the domain.
    if CREDIT not in text:
        text = insert_credit(text)
        log["credit"] = 1
    log["delta"] = len(text) - n0
    return text, log


# ------------------------------------------------------- KEEP-21-Jul guard
# Everything dated 21 Jul in the Humanities folders is a hand-made support
# pack. It is not regenerable and the pack must never overwrite it. These are
# the stems visible in the screenshots (several are truncated in the OneDrive
# UI, so the match is by prefix on what IS legible).
KEEP_21JUL = {
    f"{HUM}/Build": ["AQA_UAS_Unit_O", "Cause_Consequ", "Historical_Accou", "Lundy_Influence_",
                     "Map_Route_and_", "Printable_Eviden", "Rapid_Gallery_His", "README",
                     "Recording_Consent_Log", "Source_Observati", "START_HERE",
                     "Studio_Archivist_Role_Card", "Teacher_Guide_and_Moderation"],
    f"{HUM}/Grow":  ["AQA_UAS_Outco", "Atlas_Index_Grid", "Lundy_Influence_", "Multi_Causal_Re",
                     "Printable_Eviden", "README", "Recording_Consent_Log", "Significance_Dep",
                     "Source_Provenan", "START_HERE", "Studio_Archivist", "Teacher_Guide_and_Moderation",
                     "Week7_Assesse"],
    f"{HUM}/Launch": ["Printable_Eviden", "Recording_Consent_Log", "START_HERE",
                      "Teacher_Guide_and_Moderation"],
}

WEEK_ORDER_NOTE = """0_WEEK_ORDER — read before teaching Careers W6 / W7
=====================================================

GO BY THE SLIDE, NEVER BY THE FILENAME.

The filenames for weeks 6 and 7 are swapped relative to the teaching order:

    Week 6  ->  "What Happens After Year 11"  ->  file CAREERS_W7_After_Year_11.html
    Week 7  ->  "My Career Profile"           ->  file CAREERS_W6_My_Career_Profile.html

So in week 6 you open the file whose name says W7, and in week 7 you open the
file whose name says W6. The title on the slide is the one that matches the
scheme of work.

Do not rename the files to "fix" this. They are linked by name from the hub
and from the scheme of work, and renaming them breaks both.

This note travels with the Careers folder deliberately: the warning used to
live only in a build report, which is not where anyone teaching the lesson
would ever look.

(Correction, 2026-08-07: an earlier build of this pack carried the opposite
advice — "the filename is right". That was wrong. If you kept a copy of the
earlier pack, replace this file.)
"""


OFL_SLUG = {"Bebas Neue": "bebasneue", "Barlow Condensed": "barlowcondensed",
            "DM Sans": "dmsans", "JetBrains Mono": "jetbrainsmono",
            "DM Serif Display": "dmserifdisplay", "Inter": "inter"}


def write_font_licences(pack, families):
    """Every vendored family's OFL text, fetched from google/fonts and shipped.

    All six live under `ofl/` in that repo, which is what makes them SIL OFL 1.1
    rather than Apache-2.0 (a handful of Google families are the latter -- the
    directory is the authority, not an assumption)."""
    import urllib.request
    out = ["FONT LICENCES", "=" * 74, "",
           "This pack embeds web fonts directly in the pages that use them, so it makes",
           "no network request. Embedding is redistribution, so the licences travel with",
           "them.", "",
           "All families below are licensed under the SIL Open Font License, Version 1.1,",
           "which permits redistribution and embedding. Verified per family against the",
           "`ofl/` directory of github.com/google/fonts.", ""]
    for fam in sorted(families):
        slug = OFL_SLUG.get(fam)
        out += ["-" * 74, f"{fam} — SIL Open Font License 1.1", "-" * 74, ""]
        if not slug:
            out += [f"  (licence text not bundled: no known slug for {fam};",
                    "   see https://fonts.google.com/specimen/" + fam.replace(" ", "+"), ""]
            continue
        try:
            txt = urllib.request.urlopen(
                f"https://raw.githubusercontent.com/google/fonts/main/ofl/{slug}/OFL.txt",
                timeout=45).read().decode("utf-8", "replace")
            out += [txt.rstrip(), ""]
        except Exception as e:
            out += [f"  (could not fetch: {e})",
                    f"  https://raw.githubusercontent.com/google/fonts/main/ofl/{slug}/OFL.txt", ""]
    # GEOMETRY GATE: the drive root admits a fixed set of files, and this is not one
    # of them. Both font-embedding pages live in Tutor Time BF_BV_KCSIE/, so the
    # licence ships THERE — redistribution and licence stay in the same folder, and
    # the root stays byte-identical to the drive's.
    dest = pack / "Tutor Time BF_BV_KCSIE" / "FONT_LICENCES.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")


# PACK-5 --------------------------------------------------------------------
# A "lesson" is a teaching page: not a hub, not one of the named support pages.
# This rule is not invented here -- it is the one that reproduces the brief's own
# figures for the pair it described (GROW 34, LAUNCH 46, 80 total, 56 screen-only).
# "Screen-only" means the page carries no print stylesheet.
ROUTE_SUPPORT = re.compile(
    r"EVIDENCE_WINDOW|IMPLEMENTATION_GUIDE|CONSOLIDATION|TRANSITION_SUPPORT", re.I)

def route_note_stats():
    """Measure lessons / screen-only per v3 estate, from the repo files."""
    stats = {}
    for pre in ESTATE_V3:
        root = REPO / pre.rstrip("/")
        pages = sorted(root.rglob("*.html"))
        lessons = [f for f in pages
                   if f.name != "index.html" and not ROUTE_SUPPORT.search(f.name)]
        screen = [f for f in lessons
                  if "@media print" not in f.read_text(encoding="utf-8", errors="ignore")]
        stats[pre] = {"pages": len(pages), "lessons": len(lessons),
                      "screen": len(screen), "print": len(lessons) - len(screen),
                      "hubs": len([f for f in pages if f.name == "index.html"])}
    return stats

def quarantine_readme(quarantined, back):
    lines = [
        "NEW IN THIS REBUILD — NOT YET FILED ON THE DRIVE",
        "=" * 68, "",
        "WHY THIS FOLDER EXISTS",
        "    These files are current, in-scope teaching material, but the drive",
        "    taxonomy this pack mirrors has no folder for them. Rather than guess a",
        "    home and bury them somewhere wrong, the build put them here and told you.",
        "",
        "WHAT TO DO",
        "    Drag them wherever you want them — or leave them here. Nothing else in",
        "    the pack depends on their final location EXCEPT the links noted below.",
        "",
        "IF YOU MOVE Baseline_Weeks",
        "    The three Science v3_40min hub pages (Build, Grow, Launch) link into it.",
        "    Those links were rewritten to point at THIS location. Move the folder and",
        "    those three links stop resolving — the pages still work, the one link out",
        "    of each does not.",
        "",
        f"FILES ({len(quarantined)})",
        "-" * 68,
    ]
    for d in quarantined:
        origin = back.get(d, "?")
        lines.append(f"  {d}")
        lines.append(f"      from repo: {origin}")
    lines += [
        "-" * 68, "",
        "NOT INCLUDED",
        "    Baseline_Weeks/README.md — a developer note headed 'Made by Matt' that",
        "    names the PythonAnywhere original. Held out of a Progress-branded pack",
        "    on the dual-branding rule. It is still in the repo if you want it.",
        "",
    ]
    return "\n".join(lines)


def route_note(pre, dst, s):
    unit = pre.split("_")[0]
    if s["screen"] > s["print"]:
        printing = (f"{s['screen']} of the {s['lessons']} lessons are SCREEN-ONLY by design.\n"
                    f"    Print packs for those follow later; {s['print']} already print.")
    elif s["screen"] == 0:
        printing = f"All {s['lessons']} lessons print. No screen-only lessons in this route."
    else:
        printing = (f"{s['print']} of the {s['lessons']} lessons print; "
                    f"{s['screen']} is screen-only.\n    Print packs for the remainder follow later.")
    return f"""ABOUT THIS FOLDER — {dst.rstrip('/')}
{'=' * 68}

WHAT THIS IS
    An ALTERNATIVE Autumn 1 route for {unit}. It is a complete parallel set of
    lessons, not an update to the ones you already have.

THE EXISTING LESSONS REMAIN THE DEFAULT
    Nothing in your current {unit} folders has been changed, moved or replaced by
    this folder. If you do nothing, you teach exactly what you taught before.

WHICH ROUTE TO TEACH IS A STAFF DECISION
    Matt's or the teaching team's call — not a decision this pack makes for you.

PRINTING
    {printing}

WHAT IS IN HERE
    {s['lessons']} lessons, {s['hubs']} hub pages, {s['pages']} pages in total.
    Start at index.html in this folder.
    Self-contained: every link inside this folder points inside this folder,
    so it works from OneDrive and offline with nothing else installed.

Counts above were measured from the files in this folder at build time.
"""


def build_mirror(logo_path, out_root):
    keep, dropped = in_scope()
    print(f"scope: {len(keep)} files in, {len(dropped)} deliberately excluded")
    fwd, back = build_index(keep)
    print(f"taxonomy: {len(set(os.path.dirname(v) for v in fwd.values()))} destination folders")

    (lock_uri, lock_size), (mark_uri, mark_size) = load_logo(logo_path)
    print(f"logo: lockup {lock_size} ({len(lock_uri)} chars b64), mark {mark_size}")
    mark_html = logo_html(lock_uri, lock_size)
    LOGO_URI[:] = [lock_uri, lock_size]
    LOGO_HTML[0] = mark_html

    pack = out_root / "Progress_Schools_OneDrive_Mirror"
    if out_root.exists(): shutil.rmtree(out_root)
    pack.mkdir(parents=True)

    # assessed conditions blocks captured BEFORE anything is touched (R-A01)
    assessed = {}
    for rel in keep:
        src = REPO / rel
        if src.suffix == ".html":
            t = src.read_text(encoding="utf-8", errors="ignore")
            if "★ ASSESSED LESSON" in t:
                mm = re.search(r'★ ASSESSED LESSON.{0,2000}', t, re.S)
                assessed[str(rel)] = mm.group(0) if mm else None
    print(f"assessed files locked: {len(assessed)}")

    totals, avl_fails, avl_seen, rewrites = {}, [], 0, 0
    logo_pages = 0
    font_pages, font_families, font_bytes = 0, set(), 0
    for rel in keep:
        src = REPO / rel
        raw = src.read_text(encoding="utf-8", errors="ignore") if src.suffix != ".csv" else None
        dest = pack / fwd[str(rel)]
        if src.suffix == ".html":
            new, log = mirror_rebrand(raw, rel, mark_html)
            if str(rel) in IN_FOLDER_HUBS:                # D2: brand the root copy too,
                new, _b = brand_header(new, mark_html)    # or the two copies disagree
            new, fam, fb = vendor_fonts(new, FONT_CACHE)
            if fam:
                font_pages += 1; font_families |= set(fam); font_bytes += fb
            new, n = rewrite_links(new, rel, fwd)
            rewrites += n
            if log.get("logo_swapped"): logo_pages += 1
            for k, v in log.items():
                if k != "delta": totals[k] = totals.get(k, 0) + v
            if avl_blocks(raw):
                avl_seen += 1
                f = check_avl_preserved(raw, new, rel)
                if f: avl_fails.append(f)
            write_guarded(raw, new, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    print("rebrand totals:", totals)
    print(f"link rewrites: {rewrites}")
    print(f"D4 fonts vendored: {font_pages} page(s), {font_bytes/1024:.0f} KB inlined, "
          f"0 remaining third-party font fetches")

    # R-A01 — conditions blocks byte-identical
    for relstr, block in assessed.items():
        if block is None: continue
        got = (pack / fwd[relstr]).read_text(encoding="utf-8", errors="ignore")
        core = re.sub(r'Made by Matt|MADE BY MATT|madebymatt\.uk', "", block)
        core = re.sub(r'\s+', " ", core).strip()[:400]
        assert core in re.sub(r'\s+', " ", got), f"R-A01 VIOLATION: conditions block altered in {relstr}"
    print(f"R-A01: {len(assessed)} assessed conditions blocks intact")

    # E4 -- the licence ships with the fonts. Redistributing an OFL font without
    # its licence is a licence breach, and a pack that embeds fonts IS redistribution.
    if font_families:
        write_font_licences(pack, font_families)

    # the Careers week-order note travels INTO the folder it warns about
    (pack / "ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt").write_text(WEEK_ORDER_NOTE, encoding="utf-8")

    # PACK-5: a route note in each v3 estate, so a folder found on the drive explains
    # itself without the README. Counts are MEASURED per estate, never carried from the
    # brief -- BUILD is 53/54 print-ready and repeating GROW's "screen-only" line there
    # would have shipped a false statement into the folder it describes.
    # PACK-5 (R2): the quarantine folder explains itself and names every file.
    quarantined = sorted(v for v in fwd.values() if v.startswith(QUARANTINE))
    if quarantined:
        (pack / QUARANTINE / "0_README.txt").write_text(
            quarantine_readme(quarantined, back), encoding="utf-8")
    print(f"R2 quarantine: {len(quarantined)} file(s) under {QUARANTINE}")

    estate_stats = route_note_stats()
    for pre, dst in sorted(ESTATE_V3.items()):
        (pack / dst / "0_ABOUT_THIS_ROUTE.txt").write_text(
            route_note(pre, dst, estate_stats[pre]), encoding="utf-8")
    print("PACK-5 route notes: " + ", ".join(
        f"{p.rstrip('/')} {s['lessons']}L/{s['screen']}so" for p, s in sorted(estate_stats.items())))

    # ---- C2: a Progress-branded page at every bare name the flattening orphaned
    orphans = bare_name_census(fwd)
    for bare_path, strands in sorted(orphans.items()):
        folder = os.path.dirname(bare_path)
        (pack / bare_path).write_text(
            chooser_page(folder, os.path.basename(bare_path), strands, mark_html), encoding="utf-8")
    print(f"C2 bare-name census: {len(orphans)} orphaned bare name(s) -> chooser page authored")
    for b, s in sorted(orphans.items()):
        print(f"   {b}  -> {len(s)} strands")

    # ---- C3: position-correct in-folder hub copies, each crawled in place
    hub_results = []
    for src_rel, dest_rel in sorted(IN_FOLDER_HUBS.items()):
        raw = (REPO / src_rel).read_text(encoding="utf-8", errors="ignore")
        new_t, _log = mirror_rebrand(raw, src_rel, mark_html)
        new_t, _b = brand_header(new_t, mark_html)      # D2: hubs are Progress pages
        new_t, _n = rewrite_links(new_t, src_rel, fwd, dest_override=dest_rel)
        write_guarded(raw, new_t, pack / dest_rel)
        miss = crawl_one(pack, dest_rel)
        if miss:
            (pack / dest_rel).unlink()          # dropped rather than shipped broken
            hub_results.append((src_rel, dest_rel, False, miss))
        else:
            hub_results.append((src_rel, dest_rel, True, set()))
    print("C3 in-folder hubs:")
    for s, d, ok, miss in hub_results:
        print(f"   {'OK     ' if ok else 'DROPPED'} {d}" + ("" if ok else f"  ({sorted(miss)})"))

    # KEEP-21-Jul: nothing we ship may land on a hand-made support pack
    clashes = []
    for d, stems in KEEP_21JUL.items():
        folder = pack / d
        if not folder.exists(): continue
        for f in folder.iterdir():
            for s in stems:
                if f.name.startswith(s):
                    clashes.append(f"{d}/{f.name} would overwrite a 21-Jul support pack")
    print(f"KEEP-21-Jul: {'clean, no shipped file collides' if not clashes else str(len(clashes)) + ' COLLISIONS'}")
    for c in clashes: print("  FAIL:", c)
    return (pack, keep, fwd, back, avl_fails, avl_seen, clashes, logo_pages,
            rewrites, orphans, hub_results)


def mirror_verify(pack):
    """The full set, run over the ASSEMBLED tree.

    Differs from verify() in one way that matters: exactly ONE Made-by-Matt
    string is permitted per page -- the credit Matt asked for -- and it is
    whitelisted by exact match. Any other spelling still counts as residue."""
    fails, notes = [], {}
    files = sorted(pack.rglob("*.html"))
    notes["html_files"] = len(files)
    attr = dom = noxb = strip = nocredit = multicredit = tiny = 0
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'(aria-label|alt|content|title)="[^"]*made by matt', t, re.I): attr += 1
        # C7 - the exemption is ANCHORED ON THE CREDIT ELEMENT, not on the
        # substring. Matching the token "madebymatt.uk" alone would happily pass
        # href="https://madebymatt.uk" -- a live link to the public site, which
        # is exactly the residue REBRAND.md rule 4 exists to catch. So: delete
        # the one canonical credit element, then require ZERO residue in what
        # is left. Nothing can hide behind the whitelist.
        # Anchor: the credit must appear exactly ONCE and as element TEXT --
        # i.e. between '>' and '<'. That is what makes this a real exemption
        # rather than a hole: an href, a src, or any attribute value cannot
        # satisfy it, so href="https://madebymatt.uk" still fails.
        stripped = t.replace(">" + CREDIT + "<", "><", 1)
        if PERSONAL_RESIDUE.search(stripped): dom += 1
        if t.count(CREDIT) == 0: nocredit += 1
        elif t.count(CREDIT) > 1: multicredit += 1
        if 'name="x-brand"' not in t: noxb += 1
        if STRIP in t: strip += 1
        if not t.rstrip().lower().endswith("</html>"):
            fails.append(f"{p.name}: no closing </html>")
        if len(t) < 200: tiny += 1
    notes.update(attr_residue=attr, domain_residue=dom, missing_xbrand=noxb,
                 carry_strip=strip, missing_credit=nocredit,
                 duplicate_credit=multicredit, truncated_or_empty=tiny)
    if attr:        fails.append(f"REBRAND check 1 FAILED: {attr} files with wordmark in an attribute")
    if dom:         fails.append(f"REBRAND check 2 FAILED: {dom} files carry non-whitelisted madebymatt text")
    if noxb:        fails.append(f"REBRAND check 3 FAILED: {noxb} files missing the x-brand marker")
    if not strip:   fails.append("REBRAND check 4 FAILED: no file carries the TEES VALLEY strip")
    if nocredit:    fails.append(f"CREDIT FAILED: {nocredit} files missing '{CREDIT}'")
    if multicredit: fails.append(f"CREDIT FAILED: {multicredit} files carry it more than once")
    if tiny:        fails.append(f"{tiny} files are truncated or empty")
    return fails, notes


def inline_js_check(pack):
    """Catch inline <script> bodies the transform could have broken."""
    import subprocess, tempfile, json
    bad = []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for mm in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', t, re.S | re.I):
            body = mm.group(1).strip()
            if not body or body.startswith("{") and body.endswith("}"):  # JSON-LD etc
                continue
            r = subprocess.run(["node", "--check", "-"], input=body, text=True,
                               capture_output=True)
            if r.returncode != 0:
                err = next((l for l in r.stderr.splitlines() if "Error" in l), "unknown")
                bad.append(f"{p.relative_to(pack)}: {err[:100]}")
                break
    return bad


def write_docs(pack, keep, fwd, back, clashes, logo_pages, rewrites, crawl_miss,
               hub_results, orphans, manifest_total):
    global HONESTY_LINE
    HONESTY_LINE = (
        f"The Progress Schools logo is on {logo_pages} of "
        f"{len(list(pack.rglob('*.html')))} pages. Those are every page that previously\n"
        "  carried a visible mark, plus the pages this build authors or re-emits (the strand\n"
        "  chooser, the changes page, and the four hubs at both their root and in-folder\n"
        "  paths). The rest never carried a visible mark and were not given one: they get the\n"
        "  x-brand meta tag and the credit line only.")
    """PLACEMENT_GUIDE + TAXONOMY_MAP + README_FIRST.

    C5: TAXONOMY_MAP and PLACEMENT_GUIDE are build artefacts for Matt, not staff
    content, and the drive root is staff-facing. They go in _Pack_Notes/ and are
    explicitly OUTSIDE the drag-and-merge set."""
    notes = pack / "_Pack_Notes"
    notes.mkdir(parents=True, exist_ok=True)
    tops = {}
    for d in fwd.values():
        tops.setdefault(d.split("/")[0] if "/" in d else "(root files)", []).append(d)

    # ---- PLACEMENT_GUIDE.txt
    g = ["PLACEMENT_GUIDE - one line per top-level item. Nothing else to decide.",
         "=" * 74, "",
         "Drag each item below onto its twin in OneDrive and choose MERGE.",
         "Do not rename anything. Do not delete anything first.", ""]
    # PACK-5: a folder this rebuild introduces has NO twin on the drive. Telling staff
    # to "merge into the existing X" when X does not exist is a false instruction, and
    # it is the one line in this guide they act on without checking.
    new_tops = sorted({v.rstrip("/") for v in ESTATE_V3.values()} | {QUARANTINE.rstrip("/")})
    for tname in sorted(tops):
        d = pack / tname
        n = sum(1 for f in d.rglob("*") if f.is_file()) if d.is_dir() else len(tops[tname])
        if tname == "(root files)":
            g.append(f"  {'the loose .html files at the zip root':<46} -> drop at the ROOT of the lessons area (merge)")
        elif tname in new_tops:
            g.append(f"  {tname + '/':<46} -> NEW - nothing to merge onto. Just drop it at the root.  ({n} files)")
        else:
            g.append(f"  {tname + '/':<46} -> merge into the existing '{tname}' folder  ({n} files)")
    g += ["",
          "  The four NEW folders above do not exist on the drive yet. There is no twin to",
          "  merge onto and nothing of yours they can overwrite — dropping them at the root",
          "  is the whole job. Each carries a note explaining itself:",
          "  0_ABOUT_THIS_ROUTE.txt in the three estates, 0_README.txt in _New_This_Rebuild."]
    g += ["",
          "  DO NOT DRAG:  _Pack_Notes/   - build notes for Matt, not staff content.",
          "                                 TAXONOMY_MAP.md, MANIFEST.txt, the collision",
          "                                 check and this guide live there. Keep the zip,",
          "                                 or read them and bin them. They are deliberately",
          "                                 NOT part of the drag-and-merge set.", "",
          "-" * 74, "",
          "FOLDER NAME - CONFIRMED BY MATT 2026-08-07",
          "",
          f'  "{HUM}"',
          "",
          "  Confirmed exactly as spelled above: single spaces, the word \"and\", not \"&\".",
          "  Drag it straight onto its twin. Nothing to check.", "",
          "-" * 74, "",
          "CAREERS WEEKS 6 AND 7 - GO BY THE SLIDE, NEVER THE FILENAME",
          "",
          "  Week 6 = \"What Happens After Year 11\" = file CAREERS_W7_After_Year_11.html",
          "  Week 7 = \"My Career Profile\"          = file CAREERS_W6_My_Career_Profile.html",
          "",
          "  The full note travels inside the folder as",
          "  ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt.",
          "  Do NOT rename the files - the hub and the scheme of work link to them by name.",
          "  (An earlier pack said \"the filename is right\". That was wrong.)", "",
          "-" * 74, "",
          "KEEP / DELETE",
          "",
          "  KEEP    Everything dated 21 JULY, without exception. The Humanities",
          "          organisers, receipt packs, role cards, consent logs and moderation",
          "          guides are hand-made and CANNOT be regenerated. This pack ships",
          "          nothing with those names. If a merge ever offers to replace one,",
          "          say no.",
          "  KEEP    Every _Legacy_2025-26/ folder. The pack never writes into or",
          "          beside one.",
          "  KEEP    ASDAN PEQ/Launch/START_HERE.html - now REPLACED by a Progress-branded",
          "          chooser page pointing at the five strands. Keep the new one.",
          "  DELETE  Nothing else is required. If you want to tidy, the only safe",
          "          deletions are duplicates this pack has already replaced in place.",
          "",
          "-" * 74, "",
          "SYNC OR DOWNLOAD - DO NOT TEACH FROM THE WEB PREVIEW",
          "",
          "  OneDrive's browser preview may not apply linked CSS, so a scheme of work",
          "  can render completely unstyled. Sync the folder, or download the file, and",
          "  open it locally.", "",
          "-" * 74, "",
          "PER-MACHINE STORAGE",
          "",
          "  Cold-call lists, evidence ticks and anything else you type into a deck are",
          "  stored in that browser on that computer. They do not follow the file, they",
          "  are not on the drive, and they are not in any backup. Print the paper",
          "  tracker in Tutor Time for anything that has to survive.", "",
          "-" * 74, "",
          "THE FOUR IN-FOLDER HUB COPIES",
          "",
          "  Your drive keeps a second copy of each root hub inside the folder it serves.",
          "  A root hub's links are written for the root, so copying the root version",
          "  into a subfolder would give you a branded hub with dead links. Each copy",
          "  below was rebuilt for its own depth and crawled from its own location:", ""]
    for src, dest, ok, miss in hub_results:
        if ok:
            g.append(f"    OK      {dest}")
            g.append(f"            rebranded, links rewritten for this depth, crawls clean.")
        else:
            g.append(f"    DROPPED {dest}")
            g.append(f"            could not be made to resolve in place ({', '.join(sorted(miss))[:60]}).")
            g.append(f"            RECOMMENDATION: delete this duplicate and use the root hub.")
    g += ["", "-" * 74, "", "LOGO COVERAGE", "", "  " + HONESTY_LINE, "", "=" * 74, ""]
    (notes / "PLACEMENT_GUIDE.txt").write_text("\n".join(g) + "\n", encoding="utf-8")

    # ---- TAXONOMY_MAP.md
    m = ["# TAXONOMY_MAP - repo path -> OneDrive destination", "",
         f"Derived from 35 screenshots of the live drive, 2026-08-07. {len(keep)} files mapped, "
         f"{manifest_total} entries shipped.",
         "Where the repo and the drive disagree on a name, **the drive wins**.", "",
         f"Folder name `{HUM}` — **CONFIRMED BY MATT 2026-08-07**.", "",
         "## Every in-scope file", "", "| repo path | OneDrive destination |", "|---|---|"]
    for r in sorted(fwd, key=str.lower):
        m.append(f"| `{r}` | `{fwd[r]}` |")
    m += ["", "## Folders RENAMED on the way in", "", "| repo | drive | why |", "|---|---|---|",
          "| `BUILD_ASDAN/` | `ASDAN PEQ/Build/` | the drive groups the three ASDAN strands under one folder |",
          "| `GROW_ASDAN/` | `ASDAN PEQ/Grow/` | as above |",
          "| `LAUNCH_ASDAN/` | `ASDAN PEQ/Launch/` | as above |",
          "| `GROW_ASDAN/Enterprise/` | `ASDAN PEQ/Grow/Community and Enterprise/` | drive uses spaces and the long name |",
          "| `GROW_ASDAN/Community_Project/` | `ASDAN PEQ/Grow/Community Project/` | drive uses a space |",
          "| `GROW_ASDAN/PEQ/` | `ASDAN PEQ/Grow/Personal Effectiveness/` | drive uses the full unit name |",
          "| `DT_Community_Upcycling/` | `ASDAN PEQ/Build/DT/` | drive files it under BUILD |",
          f"| `Humanities_Teesside/` | `{HUM}/` | drive name, confirmed by Matt |",
          f"| `Humanities_Teesside/Lundy_Humanities/` | `{HUM}/LundyLoop/` | drive name |",
          f"| `.../Lundy_Humanities/specimens/` | `{HUM}/LundyLoop/Specimens/` | capital S on the drive |",
          "| `Tutor_Time/` | `Tutor Time BF_BV_KCSIE/` | drive name |",
          "| `Art_Teesside/` | `Art/` | drive name |", "",
          "## LAUNCH_ASDAN is FLAT on the drive", "",
          "The repo keeps five subfolders; the drive holds every deck directly in",
          "`ASDAN PEQ/Launch/`. A census of basenames repeated across the five strands returns",
          "**exactly one**: `START_HERE.html`. Flattening would collide five files onto one name,",
          "destroying four, so they are disambiguated:", ""]
    for a, b, _w in sorted(set(RENAMES)):
        m.append(f"- `{a}` -> `{b}`")
    m += ["", "Each renamed page has its own outbound lesson links rewritten to the flat names.", "",
          "## NEW - things this pack adds that the screenshots do NOT show", ""]
    for o, strands in sorted(orphans.items()):
        m.append(f"- `{o}` — Progress-branded chooser page. The drive's bare-named file at this")
        m.append(f"  path is Made-by-Matt branded and would otherwise survive the merge as an")
        m.append(f"  orphan carrying the name staff know. Links to: {', '.join(strands)}.")
    m += ["- `ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt` — the W6/W7 slide-vs-filename warning.",
          "- `_Pack_Notes/` — build notes, deliberately outside the drag-and-merge set.",
          "- `CHANGES_SINCE.html` — regenerated for this pack.", "",
          "## In-folder hub copies (C3)", "",
          "| destination | result |", "|---|---|"]
    for src, dest, ok, miss in hub_results:
        m.append(f"| `{dest}` | {'rebuilt at this depth, crawls clean in place' if ok else 'DROPPED - ' + ', '.join(sorted(miss))[:50]} |")
    # PACK-5 (R1/R2): folders this rebuild introduces. They have no twin on the drive,
    # so they are recorded here as additions to the taxonomy rather than mappings into it.
    _st = route_note_stats()
    m += ["", "## NEW FOLDERS — added by this rebuild, not present on the drive", "",
          "Four root-level folders the drive does not have. Nothing merges onto them;",
          "they are dropped at the root as-is.", "",
          "| folder | what it is | pages |", "|---|---|---|"]
    for pre, dst in sorted(ESTATE_V3.items()):
        s = _st[pre]
        m.append(f"| `{dst.rstrip('/')}` | alternative Autumn 1 route for "
                 f"{pre.split('_')[0]}; {s['lessons']} lessons "
                 f"({s['print']} print, {s['screen']} screen-only), self-contained | {s['pages']} |")
    _q = sorted(v for v in fwd.values() if v.startswith(QUARANTINE))
    m.append(f"| `{QUARANTINE.rstrip('/')}` | R2 quarantine: in-scope content with no "
             f"home in this map, filed rather than guessed at | {len(_q)} |")
    m += ["",
          "The three estates are NOT interleaved into the existing subject or ASDAN",
          "folders. Mixing two routes in one folder is the failure the 30 Jul legacy-art",
          "interleaving demonstrated; each route stays a self-contained tree so staff can",
          "teach one or the other without picking lessons apart.", "",
          "`BUILD Estate v3` was ruled in as a third peer to the two the brief named. It",
          "landed 10 Aug (cc9f36e), a day before the pair (62a92d7), and is the same shape:",
          "own hub, own subject subfolders, no links out. Unlike the other two it is almost",
          "entirely print-ready (53 of 54 lessons), so its route note says so instead of",
          "repeating the screen-only line.", ""]

    m += ["", "## Taxonomy folders with NO current repo content", "",
          "Recorded, not invented. The pack ships nothing into these:", "",
          "- `Computing/`, `Curriculum Intent and Rationale/`, `English/`,",
          "  `Feedback and Marking/`, `Lesson Slideshows_Resources/`,",
          "  `SMSC and BV Calendar Evidence/`, `Weekly Plans/`",
          "- `ASDAN PEQ/` root files (`index`, `PLACE_THIS_README`, `Scheme_of_Work`, `Weekly_Plan`)",
          "- every `_Legacy_2025-26/` folder — Matt's archive.",
          "- drive-only Art extras (`Autumn2_*`, `Spring1_*`, evidence packs).", "",
          "## Single placement", "",
          "- `LundyLoop/assets/style.css` — shipped ONCE at the root LundyLoop, which is now",
          f"  present at the drive root. The copy at `{HUM}/LundyLoop/style.css` is left as-is;",
          "  it is a stylesheet, byte-identical, and carries no branding either way.",
          "- the four root hubs — shipped at the root AND at their in-folder paths, each built",
          "  for its own depth (see above). No hand-copying is required or advised.", ""]
    (notes / "TAXONOMY_MAP.md").write_text("\n".join(m) + "\n", encoding="utf-8")

    # ---- RULINGS.txt (R3): decisions already taken, recorded so a later pass does
    # not "find" them again and undo them.
    # Case-INSENSITIVE: the files spell it "PythonAnywhere". A case-sensitive probe
    # returns 0 here and would have printed a ruling about pages it could not see.
    py_hits, py_links = [], 0
    for p in sorted(pack.rglob("*")):
        if not p.is_file() or p.suffix not in (".html", ".md"):
            continue
        if p.relative_to(pack).parts[0] in ("_Pack_Notes",):
            continue                      # this file and its siblings are the record
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "pythonanywhere" in t.lower():
            py_hits.append(str(p.relative_to(pack)))
            py_links += len(re.findall(r'(?:href|src)="[^"]*pythonanywhere', t, re.I))
    ru = ["RULINGS — settled decisions for this pack", "=" * 74, "",
          "Each of these looks like a defect to a fresh eye. Each was examined and ruled",
          "on deliberately. If a later audit flags one, read this before acting.", "",
          "-" * 74,
          "R3 — 'PythonAnywhere' NAMED IN PROSE. KEPT DELIBERATELY.", "",
          f"  Measured in this build: {len(py_hits)} surface(s) name it; {py_links} are links.",
          ]
    ru += [f"    {s}" for s in py_hits]
    ru += ["",
           "  It is the bare product name in a sentence telling teachers where the Topic 1",
           "  assessment lives. There is no URL, no link and no fetch — the personal",
           "  subdomain itself is absent from the pack, and the residue sweep confirms that",
           "  separately. (This note deliberately does NOT spell that domain out: writing it",
           "  here to say it is absent would put it in the pack and fail the sweep.)",
           "  Removing a factual sentence would make the pages less useful, not cleaner.",
           "",
           "  The brief named four Science decks. Two more surfaces have since joined the",
           "  pack and say the same kind of thing: the Launch v3_40min policy-alignment doc,",
           "  and the quarantined Baseline_Weeks hub, which contrasts itself with the",
           "  PythonAnywhere baseline app. Same ruling, same reason.",
           "",
           "-" * 74,
           "R4 — VENDORED GOOGLE FONTS. KEPT.", "",
           "  Two pages fetched webfonts. An offline pack makes no network request, so the",
           "  fonts are embedded, latin/latin-ext only. Embedding is redistribution, so",
           "  FONT_LICENCES.txt ships beside the two embedding pages (Tutor Time folder)",
           "  with the full text. All six families",
           "  verified SIL OFL 1.1 against the ofl/ directory of google/fonts, per family —",
           "  a handful of Google families are Apache-2.0 and the directory is the authority.",
           "  Not reopened as vendor-vs-drop.",
           "",
           "-" * 74,
           "R1 (extended) — THREE v3 ESTATES SHIP AS ROOT FOLDERS, NOT INTERLEAVED.", "",
           "  The brief named two. BUILD Estate v3 landed a day earlier and is the same",
           "  shape, so it was ruled in as a third peer rather than quarantined. None of",
           "  the three is merged into the existing subject or ASDAN folders: mixing routes",
           "  in one folder is the failure the 30 Jul legacy-art interleaving demonstrated.",
           "",
           "-" * 74,
           "R2 — UNMAPPED IN-SCOPE CONTENT IS FILED, NOT GUESSED AT OR DROPPED.", "",
           "  Baseline_Weeks (8 pages) is real teaching material linked from three shipping",
           "  Science hubs, but the drive taxonomy has no folder for it. It ships under",
           "  _New_This_Rebuild/ with its links rewritten to follow it. Its own README.md",
           "  is held out: a developer note headed 'Made by Matt' naming the PythonAnywhere",
           "  original, which the dual-branding rule keeps out of a Progress pack.",
           "",
           "-" * 74,
           "R5 — HOW_TO_USE_THESE_LESSONS LEFT AT ITS CURRENT STATE.", "",
           "  The v3 route explanation lives in README_FIRST and in the three",
           "  0_ABOUT_THIS_ROUTE.txt notes instead.",
           "",
           "-" * 74,
           "R-A01 — THE TWO ★ ASSESSED LESSONS.", "",
           "  Their conditions blocks are asserted byte-identical to the repo on every",
           "  build. A conditions change needs Matt's word, every time.", ""]
    (notes / "RULINGS.txt").write_text("\n".join(ru) + "\n", encoding="utf-8")

    # ---- README_FIRST.txt (staff-facing, merges to the drive root)
    r = ["README_FIRST - Progress Schools lessons", "=" * 74, "",
         "WHAT THIS IS",
         "  A Progress Schools-branded copy of the in-scope lessons, in a folder tree that",
         "  mirrors this drive exactly. Drag each top-level folder onto its twin and choose",
         "  merge. See _Pack_Notes/PLACEMENT_GUIDE.txt for the one-line-per-folder version.", "",
         "-" * 74, "CAREERS WEEKS 6 AND 7 - GO BY THE SLIDE, NEVER THE FILENAME",
         "  Week 6 = 'What Happens After Year 11' = file CAREERS_W7_After_Year_11.html",
         "  Week 7 = 'My Career Profile'          = file CAREERS_W6_My_Career_Profile.html",
         "  Full note: ASDAN PEQ/Build/Careers/0_WEEK_ORDER.txt. Do not rename the files.",
         "  An earlier pack carried the opposite advice. That was wrong.", "",
         "-" * 74, "KEEP - 21 JULY SUPPORT PACKS",
         "  Everything dated 21 Jul in the Humanities folders is hand-made and NOT",
         "  regenerable. This pack ships nothing with those names and the build asserts it",
         f"  ({'0 collisions' if not clashes else str(len(clashes)) + ' COLLISIONS - DO NOT UNZIP'}).",
         "  If a merge ever offers to replace one of them, say no.", "",
         "-" * 74, "NEW - THE v3 ALTERNATIVE ROUTES (three folders)",
         "  Three folders in this pack are new. Your drive does not have them, nothing",
         "  merges onto them, and nothing you already have is changed by them:", "",
         "    BUILD Estate v3 (Alternative Route)/",
         "    GROW Estate v3 (Alternative Route)/",
         "    LAUNCH Estate v3 (Alternative Route)/", "",
         "  WHAT THEY ARE",
         "    A complete ALTERNATIVE Autumn 1 route for each unit — a parallel set of",
         "    lessons, not an update to the ones you have.", "",
         "  THE EXISTING LESSONS REMAIN THE DEFAULT",
         "    If you do nothing, you teach exactly what you taught before. Which route to",
         "    teach is a staff decision, not one this pack makes.", "",
         "  PRINTING - THE THREE DIFFER, SO CHECK BEFORE YOU PLAN",
         f"    BUILD  : {_st['BUILD_Estate_v3/']['print']} of "
         f"{_st['BUILD_Estate_v3/']['lessons']} lessons print. Effectively print-ready.",
         f"    GROW   : {_st['GROW_Estate_v3/']['print']} of "
         f"{_st['GROW_Estate_v3/']['lessons']} lessons print; "
         f"{_st['GROW_Estate_v3/']['screen']} are screen-only.",
         f"    LAUNCH : {_st['LAUNCH_Estate_v3/']['print']} of "
         f"{_st['LAUNCH_Estate_v3/']['lessons']} lessons print; "
         f"{_st['LAUNCH_Estate_v3/']['screen']} are screen-only.",
         "    Print packs for the screen-only lessons follow later.", "",
         "  Each folder has 0_ABOUT_THIS_ROUTE.txt inside it saying the same thing.", "",
         "-" * 74, "NEW - _New_This_Rebuild/",
         "  Current teaching material with no folder on the drive to file it under. Rather",
         "  than guess a home, the build put it here and said so. Drag it wherever you want",
         "  it, or leave it. Read _New_This_Rebuild/0_README.txt first — it names every",
         "  file, where it came from, and the three links that point into it.", "",
         "-" * 74, "SYNC OR DOWNLOAD - DO NOT TEACH FROM THE WEB PREVIEW",
         "  OneDrive's browser preview may not apply linked CSS, so a scheme of work can",
         "  render completely unstyled. Sync the folder or download the file.", "",
         "-" * 74, "PER-MACHINE DATA",
         "  Cold-call lists and evidence ticks are stored in that browser on that computer.",
         "  They do not follow the file and are not on the drive. Print the paper tracker in",
         "  Tutor Time for anything that has to survive.",
         "  No pupil data of any kind is in this pack, and none ever will be.", "",
         "-" * 74, "BRANDING CHANGELOG",
         "  * The REAL Progress Schools logo replaces the typographic placeholder, embedded",
         "    per page as a data URI so it survives a file being moved and works offline.",
         "    Never recoloured, restyled, stretched or redrawn; on a white chip so a dark",
         "    header cannot force a change to the trademark's colours.",
         f"  * Every page carries '{CREDIT}', at Matt's instruction. It is the only permitted",
         "    Made-by-Matt string; the sweep whitelists it by exact match and fails on any",
         "    other spelling.",
         "  * Wordmarks replaced in attributes as well as visible text.",
         "  * hud.js loaders stripped, including the dynamic injector form.",
         "  * x-brand meta tag on every page.", "",
         "-" * 74, "WHAT CHANGED THIS BUILD",
         "  * The tree is the SCHOOL's, not the repo's; every internal link was rewritten to",
         f"    match ({rewrites} rewrites).",
         "  * ASDAN LAUNCH is flat, so each strand's start page is named after its strand and",
         "    the plain START_HERE is now a chooser page linking to all five.",
         "  * The four in-folder hub copies are rebuilt at their own depth rather than being",
         "    hand-copied from the root (which would have produced dead links).",
         "  * " + HONESTY_LINE, "",
         "-" * 74, "WHAT THIS PACK DOES NOT CLAIM",
         "  The estate is not clean. This covers the in-scope areas only and leaves the legacy",
         "  trees, the _Legacy_2025-26 archives, Planning, Students material and the personal",
         "  apps entirely alone.",
         f"  Unresolved link targets after the rewrite: {sum(len(v) for v in crawl_miss.values())}.",
         "",
         "  HOW_TO_USE_THESE_LESSONS on the drive root is NOT refreshed by this pack and is",
         "  knowingly left as it stands (6 Aug). Nothing in this update contradicts it; it",
         "  simply predates the branding and structure changes listed above.", ""]
    (pack / "README_FIRST.txt").write_text("\n".join(r) + "\n", encoding="utf-8")


def write_offline_index(pack, fwd, logo_uri, logo_size):
    """Generate the offline index for the Network Library copy.

    Links are relative to the pack root, i.e. the SAME geometry as the mirror,
    so the index works from a network share or from file:// without change."""
    from collections import defaultdict
    groups = defaultdict(list)
    # walk the actual tree, not the map: the map has no rows for the pages this
    # build generates (the strand chooser, the in-folder hubs, CHANGES_SINCE),
    # and a library index that omits shipped pages is worse than none.
    for p in sorted(pack.rglob("*.html"), key=lambda x: str(x).lower()):
        d = str(p.relative_to(pack))
        if d == "index.html" or d.startswith("_Pack_Notes/"):
            continue
        top = d.split("/")[0] if "/" in d else "(top level)"
        groups[top].append(d)
    w, h = logo_size
    rows = []
    for top in sorted(groups, key=str.lower):
        rows.append(f'<section><h2>{html.escape(top)} '
                    f'<span class="n">{len(groups[top])} pages</span></h2><ul>')
        for d in groups[top]:
            label = d.rsplit("/", 1)[-1][:-5].replace("_", " ")
            href = "/".join(quote(seg) for seg in d.split("/"))
            rows.append(f'<li><a href="{href}">{html.escape(label)}</a>'
                        f'<span class="p">{html.escape(d.rsplit("/",1)[0])}</span></li>')
        rows.append("</ul></section>")
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-brand" content="progress-schools">
<title>Progress Schools \u00b7 Offline Lesson Library</title>
<style>
:root{{color-scheme:light dark;--bg:#fbfbfc;--fg:#1a1a1e;--mut:#63636e;--line:#e3e3e8;--card:#fff;--acc:#E5007D}}
@media(prefers-color-scheme:dark){{:root{{--bg:#131317;--fg:#ececf1;--mut:#9a9aa6;--line:#2a2a32;--card:#1c1c22}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif}}
header{{padding:28px 20px 20px;border-bottom:1px solid var(--line);text-align:center;background:var(--card)}}
.chip{{display:inline-block;background:#fff;border-radius:8px;padding:6px 10px;line-height:0}}
.chip img{{width:112px;height:auto;display:block}}
.strip{{margin-top:.5rem;font:600 11px/1 system-ui,sans-serif;letter-spacing:.08em}}
h1{{font-size:1.15rem;margin:.7rem 0 .2rem}}
.sub{{color:var(--mut);font-size:.85rem;margin:0}}
main{{max-width:1000px;margin:0 auto;padding:20px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 16px;padding:14px 18px}}
h2{{font-size:.95rem;margin:.2rem 0 .6rem;display:flex;justify-content:space-between;align-items:baseline;gap:1rem}}
.n{{font-weight:400;font-size:.75rem;color:var(--mut)}}
ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:2px}}
li{{padding:5px 8px;border-radius:7px;min-width:0}}
li:hover{{background:var(--bg)}}
a{{color:var(--fg);text-decoration:none;font-size:.88rem;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
a:hover{{color:var(--acc);text-decoration:underline}}
.p{{display:block;font-size:.68rem;color:var(--mut);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
footer{{text-align:center;color:var(--mut);font-size:.7rem;padding:18px}}
</style></head><body>
<header>
<span class="chip"><img src="{logo_uri}" width="{w}" height="{h}" alt="Progress Schools"></span>
<div class="strip">{STRIP}</div>
<h1>Offline Lesson Library</h1>
<p class="sub">{sum(len(v) for v in groups.values())} pages \u00b7 works from a network share or from file:// \u00b7 nothing loads from the internet</p>
</header>
<main>
{chr(10).join(rows)}
</main>
<footer>{CREDIT}</footer>
</body></html>
"""
    (pack / "index.html").write_text(doc, encoding="utf-8")
    return sum(len(v) for v in groups.values())


def zip_tree(src_dir, zip_path, arc_root):
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists(): zip_path.unlink()
    n = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(src_dir.rglob("*")):
            if f.is_file():
                z.write(f, str(Path(arc_root) / f.relative_to(src_dir)))
                n += 1
    return n, zip_path.stat().st_size


def mirror_main(logo, out):
    out = Path(out)
    (pack, keep, fwd, back, avl_fails, avl_seen, clashes, logo_pages,
     rewrites, orphans, hub_results) = build_mirror(logo, out)

    miss = crawl(pack)
    print(f"\nCRAWL: {'clean, 0 broken internal links' if not miss else str(sum(len(v) for v in miss.values())) + ' UNRESOLVED'}")
    for f, ts in list(miss.items())[:15]:
        print(f"  {f} -> {', '.join(sorted(ts))[:110]}")

    print(f"\nAVL-1: {avl_seen} decks carry a marker pair; "
          f"{'all preserved byte-for-byte' if not avl_fails else str(len(avl_fails)) + ' ALTERED'}")
    ref_fails = check_avl_refs(pack)
    print(f"AVL-2: {'all loader references resolve inside the pack' if not ref_fails else 'BROKEN'}")
    for f in ref_fails[:10]: print("  FAIL:", f)

    # every generated page is authored BEFORE verification, so the sweeps and
    # the x-brand/credit gates cover them too. Verifying first would have left
    # CHANGES_SINCE.html and the chooser page ungated.
    c1 = c1_collision_report(pack, fwd)
    _st = route_note_stats()
    _groups, _dtot = delta_by_taxonomy(fwd)
    if _dtot:
        _rows = "\n".join(
            f"<li><code>{html.escape(t)}</code> — {len(v)} file(s)</li>"
            for t, v in sorted(_groups.items(), key=lambda kv: -len(kv[1])))
        _delta_html = (
            '<h2>Everything else that changed, by folder</h2>\n'
            f'<div class="card">{_dtot} shipped file(s) changed since the last pack '
            f'({CHANGES_BASE}). Grouped by the folder they land in:<ul>{_rows}</ul>'
            'Merging replaces the drive copy of each of these with the version in this pack.'
            '</div>')
    else:
        _delta_html = ""
    write_changes_since(pack, {
        "pages": len(list(pack.rglob("*.html"))),
        # CHANGES_SINCE carries a lockup itself, so it must be written before the
        # on-disk count is taken but must quote the FINAL number. Sentinel now,
        # substituted once disk_logos is known.
        "logo_pages": "__LOGO_PAGES__",
        "delta_html": _delta_html,
        "build_lessons": _st["BUILD_Estate_v3/"]["lessons"],
        "build_print":   _st["BUILD_Estate_v3/"]["print"],
        "grow_lessons":  _st["GROW_Estate_v3/"]["lessons"],
        "grow_print":    _st["GROW_Estate_v3/"]["print"],
        "launch_lessons": _st["LAUNCH_Estate_v3/"]["lessons"],
        "launch_print":   _st["LAUNCH_Estate_v3/"]["print"],
    }, LOGO_HTML[0])
    # Count logos on disk BEFORE writing the docs. logo_pages is only the number of
    # Made-by-Matt marks replaced; the pages this build authors carry one too, and a
    # guide that quotes the subtotal understates its own pack.
    disk_logos = sum(1 for f in pack.rglob("*.html")
                     if 'alt="Progress Schools"' in f.read_text(encoding="utf-8", errors="ignore"))
    # CHANGES_SINCE quotes two totals that are only final once it exists on disk:
    # the logo count (it carries one) and the page count (it IS one of the pages).
    # Both go in as sentinels and are substituted here, from a fresh count.
    _cs = pack / "CHANGES_SINCE.html"
    _t = _cs.read_text(encoding="utf-8")
    for _s in ("__LOGO_PAGES__", "__PAGE_COUNT__"):
        assert _s in _t, f"CHANGES_SINCE sentinel {_s} missing - it would ship a wrong total"
    _new = (_t.replace("__LOGO_PAGES__", str(disk_logos))
              .replace("__PAGE_COUNT__", str(len(list(pack.rglob("*.html"))))))
    assert _new.rstrip().endswith("</html>") and len(_new) > len(_t) // 2
    _cs.write_text(_new, encoding="utf-8")

    write_docs(pack, keep, fwd, back, clashes, disk_logos, rewrites, miss,
               hub_results, orphans, 0)
    total, by_ext, by_top = write_manifest(pack)
    print(f"\nC4 MANIFEST: {total} entries  |  by extension: {dict(by_ext)}")

    fails, notes = mirror_verify(pack)
    js = inline_js_check(pack)
    print(f"INLINE JS: {'0 syntax errors' if not js else str(len(js)) + ' BROKEN'}")
    for f in js[:10]: print("  FAIL:", f)
    print(f"LOGO: {disk_logos} of {notes['html_files']} pages carry the lockup "
          f"({logo_pages} replaced a Made-by-Matt mark, {disk_logos - logo_pages} on generated pages)")
    print("\nVERIFY:", notes)
    all_fails = fails + avl_fails + ref_fails + js + clashes + c1
    # C9 - permanently gated counts. The strip silently fell to zero once; a
    # count that can reach zero without failing the build is not a gate.
    for label, got in (("strip", notes["carry_strip"]), ("credit", notes["html_files"] - notes["missing_credit"]),
                       ("logo", logo_pages)):
        if got <= 0:
            all_fails.append(f"GATE C9: {label} count is {got} - must be > 0")
    if notes["missing_credit"] or notes["duplicate_credit"]:
        all_fails.append("GATE C9: credit count != one per page")
    if logo_pages != 140:
        all_fails.append(f"GATE C9: logo replaced {logo_pages} marks, expected 140")
    if disk_logos < logo_pages:
        all_fails.append(f"GATE C9: only {disk_logos} pages carry the logo on disk")
    # ---- GEOMETRY GATE: blocks zipping. A repo-shaped root has been rejected
    # twice; this is the assertion that a third one cannot ship.
    geo_fails, geo_table = geometry_gate(pack)
    print("\nGEOMETRY GATE - assembled root vs the drive root")
    for line in geo_table: print("  " + line)
    print(f"  GEOMETRY: {'PASS - root is the drive root' if not geo_fails else str(len(geo_fails)) + ' FAILURES'}")
    all_fails += geo_fails

    for f in all_fails[:20]: print("  FAIL:", f)
    if not all_fails: print("  all checks pass")

    # ---- package. Nothing ships if anything above failed.
    assert not all_fails, f"{len(all_fails)} checks failed - refusing to package"
    zips = []
    n, sz = zip_tree(pack, out / "Progress_Schools_OneDrive_Mirror.zip",
                     "Progress_Schools_OneDrive_Mirror")
    zips.append(("Progress_Schools_OneDrive_Mirror.zip", n, sz))

    # optional: same tree + a generated offline index, for the network share
    lib = out / "Progress_Schools_Network_Library"
    shutil.copytree(pack, lib)
    shutil.rmtree(lib / "_Pack_Notes")   # placement + build notes are a OneDrive concern only
    pages = write_offline_index(lib, fwd, LOGO_URI[0], LOGO_URI[1])
    n, sz = zip_tree(lib, out / "Progress_Schools_Network_Library.zip",
                     "Progress_Schools_Network_Library")
    zips.append(("Progress_Schools_Network_Library.zip", n, sz))
    print(f"\nofflineibrary index: {pages} pages listed".replace("ibrary","  library"))
    for nm, c, s in zips:
        print(f"PACKAGED {nm}: {c} entries, {s/1024/1024:.1f} MB")
    return pack, all_fails, notes, miss, logo_pages, rewrites, fwd, zips


# ==================================================== CLOSE GATES (C1..C12)
# Everything below was added at pack close. Each block exists because a gate
# demanded evidence rather than an assurance.

# ---- C1: what is actually ON the drive, read off the screenshots.
# Only the Humanities pathway folders matter here: they are the only place
# where an unregenerable OneDrive-only artefact can be replaced by a merge.
# `21jul` = the untouchable support set. `ours` = files this pack authored,
# which a merge SHOULD replace.
DRIVE_HUM = {
    "Build": {
        "21jul": ["AQA_UAS_Unit_Outcome_Evidence_Mapping", "Cause_Consequence_Significance_Organisers",
                  "Historical_Account_Source_Receipt_Pack", "Lundy_Influence_and_Report_Back_Log",
                  "Map_Route_and_Location_Context_Pack", "Printable_Evidence_and_Transfer_Pack",
                  "Rapid_Gallery_Historian_Audience_Cards", "README", "Recording_Consent_Log",
                  "Source_Observation_Provenance_Check_Cards", "START_HERE",
                  "Studio_Archivist_Role_Card", "Teacher_Guide_and_Moderation"],
        "ours":  ["0_WHICH_SCHEME_READ_ME", "BUILD_HUM_W1_Human_Timeline", "BUILD_HUM_W2_History_Detectives",
                  "BUILD_HUM_W3_Why_People_Came", "BUILD_HUM_W4_People_Who_Shaped_Britain",
                  "BUILD_HUM_W5_Big_Deal", "BUILD_HUM_W6_Plan_The_Story", "BUILD_HUM_W7_Tell_The_Story",
                  "BUILD_HUM_W8_Where_In_The_World", "BUILD_Printable_Pack", "BUILD_Scheme_of_Work"],
    },
    "Grow": {
        "21jul": ["AQA_UAS_Outcome_Assessment_Mapping", "Atlas_Index_Grid_Direction_Route_Pack",
                  "Lundy_Influence_and_Report_Back_Log", "Multi_Causal_Reasoning_Consequence_Organisers",
                  "Printable_Evidence_and_Transfer_Pack", "README", "Recording_Consent_Log",
                  "Significance_Depth_Defence_Cards", "Source_Provenance_Utility_Cards",
                  "Studio_Archivist_Criteria_and_Role_Card", "Teacher_Guide_and_Moderation",
                  "Week7_Assessed_Extract_and_Record"],
        # NOTE: Grow's START_HERE is 4 KB dated Thu -- authored 30 Jul, OURS, not the 21-Jul set.
        "ours":  ["GROW_HUM_W1_Time_Detectives", "GROW_HUM_W2_Source_Detectives",
                  "GROW_HUM_W3_Cause_And_Consequence", "GROW_HUM_W4_People_Who_Shaped_Britain",
                  "GROW_HUM_W5_Significance", "GROW_HUM_W6_Plan_The_Account",
                  "GROW_HUM_W7_Write_The_Account", "GROW_HUM_W8_Where_In_The_World",
                  "GROW_Printable_Pack", "GROW_Scheme_of_Work", "START_HERE"],
    },
    "Launch": {
        "21jul": ["Printable_Evidence_and_Transfer_Pack", "Recording_Consent_Log", "START_HERE",
                  "Teacher_Guide_and_Moderation"],
        "ours":  ["0_WHICH_SCHEME_READ_ME", "LAUNCH_HUM_W1_Source_Investigation",
                  "LAUNCH_HUM_W2_Cause_Consequence_Courtroom", "LAUNCH_HUM_W3_Archive_NOP",
                  "LAUNCH_HUM_W4_Century_Of_Change", "LAUNCH_HUM_W5_People_Modern_Britain",
                  "LAUNCH_HUM_W6_Structured_Account", "LAUNCH_HUM_W7_Source_Assessment",
                  "LAUNCH_HUM_W8_OS_Map_Skills", "LAUNCH_Printable_Pack", "LAUNCH_Scheme_of_Work"],
    },
    # 17:55-17:58 on 6 Aug -- current generation, ours, safe to replace.
    "LundyLoop": {"21jul": [], "ours": ["START_HERE", "style"]},
    "LundyLoop/Specimens": {"21jul": [], "ours": ["START_HERE"]},
}


def c1_collision_report(pack, fwd):
    """C1 -- print the collision list EXPLICITLY, empty or not.

    A merge replaces same-named files, and the 21-Jul Humanities support set
    cannot be regenerated. This walks every pack file destined for a Humanities
    subfolder and states, per file, whether a file of that name is on the drive
    and which set it belongs to."""
    lines = ["", "=" * 78,
             "GATE C1 - 21-JUL COLLISION CHECK (Humanities pathway folders)", "=" * 78,
             f"{'destination':<62} {'on drive?':<12} verdict", "-" * 78]
    collisions = []
    for d in sorted(v for v in fwd.values() if v.startswith(HUM + "/")):
        sub = os.path.dirname(d)[len(HUM) + 1:]
        stem = os.path.basename(d).rsplit(".", 1)[0]
        info = DRIVE_HUM.get(sub, {"21jul": [], "ours": []})
        short = d[len(HUM) + 1:]
        if stem in info["21jul"]:
            lines.append(f"{short:<62} {'YES 21-JUL':<12} *** COLLISION - MUST RENAME ***")
            collisions.append(d)
        elif stem in info["ours"]:
            lines.append(f"{short:<62} {'yes (ours)':<12} replace - current generation")
        else:
            lines.append(f"{short:<62} {'no':<12} new file, nothing overwritten")
    lines += ["-" * 78,
              f"COLLISIONS WITH THE 21-JUL SET: {len(collisions)}"]
    if collisions:
        for c in collisions: lines.append(f"   {c}")
    else:
        lines += ["   (none)",
                  "",
                  "   The 21-Jul artefacts named in the close brief -- README and START_HERE",
                  "   in the BUILD subfolder -- ARE on the drive and ARE untouchable, but this",
                  "   pack ships no file of either name into that folder, so neither is at",
                  "   risk. The pack's only Humanities START_HERE files go to LundyLoop/ and",
                  "   LundyLoop/Specimens/, whose drive copies are dated 6 Aug 17:55-17:58 and",
                  "   are this estate's own current generation."]
    lines.append("=" * 78)
    report = "\n".join(lines)
    print(report)
    (pack / "_Pack_Notes" / "C1_COLLISION_CHECK.txt").parent.mkdir(parents=True, exist_ok=True)
    (pack / "_Pack_Notes" / "C1_COLLISION_CHECK.txt").write_text(report + "\n", encoding="utf-8")
    return collisions


# ---- C2: the bare names the flattening orphans.
def bare_name_census(fwd):
    """Every destination folder where the pack renamed a file away from a bare
    name that already exists on the drive. That drive file survives the merge
    unbranded, still carrying the name staff know."""
    orphans = {}
    for repo, dest, _why in set(RENAMES):
        folder, new = os.path.split(dest)
        bare = os.path.basename(repo)
        if f"{folder}/{bare}" not in fwd.values():
            orphans.setdefault(f"{folder}/{bare}", []).append(new)
    return {k: sorted(v) for k, v in orphans.items()}


def chooser_page(folder, bare, strands, mark_html):
    """A Progress-branded page at the orphaned bare name.

    Same-folder links only -- no '../' -- because the folder is flat on the
    drive and this page must work wherever it is opened from."""
    items = "\n".join(
        f'    <li><a href="{quote(s)}">{html.escape(s[len("START_HERE_"):-5].replace("_", " "))}</a></li>'
        for s in strands)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-brand" content="progress-schools">
<title>Start Here \\u00b7 {html.escape(os.path.basename(folder))}</title>
<style>
body{{margin:0;background:#fbfbfc;color:#1a1a1e;font:16px/1.6 system-ui,-apple-system,sans-serif}}
.wrap{{max-width:640px;margin:0 auto;padding:32px 20px}}
header{{text-align:center;margin-bottom:1.5rem}}
.strip{{margin-top:.5rem;font:600 11px/1 system-ui,sans-serif;letter-spacing:.08em}}
h1{{font-size:1.3rem;margin:1.2rem 0 .3rem;text-align:center}}
p.sub{{text-align:center;color:#63636e;font-size:.9rem;margin:0 0 1.5rem}}
ul{{list-style:none;padding:0;margin:0}}
li{{margin:0 0 8px}}
li a{{display:block;padding:14px 18px;background:#fff;border:1px solid #e3e3e8;border-radius:10px;
      text-decoration:none;color:#1a1a1e;font-weight:600}}
li a:hover{{border-color:#E5007D;color:#E5007D}}
.note{{margin-top:1.6rem;padding:12px 16px;background:#fff;border:1px solid #e3e3e8;
       border-radius:10px;font-size:.85rem;color:#63636e}}
footer{{text-align:center;font:400 10px/1.4 system-ui,sans-serif;opacity:.55;margin-top:1.5rem}}
</style></head><body>
<div class="wrap">
<header>{mark_html}</header>
<h1>Start here</h1>
<p class="sub">This folder holds five strands. Pick the one you are teaching.</p>
<ul>
{items}
</ul>
<div class="note">The five strands used to sit in five subfolders, each with its own
<code>START_HERE</code>. On this drive they share one folder, so each strand's start page is
named after its strand and this page points at all five.</div>
<footer>{CREDIT}</footer>
</div>
</body></html>
"""


# ---- C3: the four in-folder hub duplicates.
# The drive keeps a second copy of each root hub inside the folder it serves.
# Telling Matt to "copy the rebranded root version over each by hand" was wrong
# advice: after a mirror rewrite the root copy's hrefs are written for depth 0,
# so dropping it into Art/ yields a Progress-branded hub with dead links --
# strictly worse than an unbranded hub that works. Each copy is emitted at its
# own depth instead, and gated by a crawl FROM ITS OWN LOCATION.
IN_FOLDER_HUBS = {
    "art_teesside.html":       "Art/art_teesside.html",
    "build_asdan.html":        "ASDAN PEQ/Build/build_asdan.html",
    "build_dt_upcycling.html": "ASDAN PEQ/Build/DT/build_dt_upcycling.html",
    "humanities_teesside.html": HUM + "/humanities_teesside.html",
}


def crawl_one(pack, rel):
    """Crawl a single page from its own location. Returns missing targets."""
    p = pack / rel
    t = p.read_text(encoding="utf-8", errors="ignore")
    missing = set()
    for dq, sq in HREF.findall(t):
        raw = html.unescape(dq or sq)
        if "${" in raw or "{{" in raw: continue
        if raw.startswith(("http://", "https://", "//", "#", "data:", "mailto:", "javascript:")):
            continue
        target = unquote(urlparse(raw).path)
        if not target: continue
        if not (p.parent / target).resolve().exists():
            missing.add(target)
    return missing


# ---- C4: cardinality, walked not typed.
def write_manifest(pack):
    """Walk the tree and reconcile every number. A hand-typed table summed to
    218 while declaring 220 on 30 Jul; the dropped row was real."""
    from collections import Counter
    # create the file before walking so the manifest counts itself -- otherwise
    # the total it declares is one short of the tree it describes.
    (pack / "_Pack_Notes").mkdir(parents=True, exist_ok=True)
    (pack / "_Pack_Notes" / "MANIFEST.txt").write_text("", encoding="utf-8")
    files = sorted(p for p in pack.rglob("*") if p.is_file())
    by_ext = Counter(p.suffix.lower() or "(none)" for p in files)
    by_top = Counter((str(p.relative_to(pack)).split("/")[0]
                      if "/" in str(p.relative_to(pack)) else "(root)") for p in files)
    lines = ["MANIFEST — every file in the pack, walked at build time", "=" * 78, "",
             f"TOTAL ENTRIES: {len(files)}", "",
             "By top-level destination", "-" * 78]
    for k in sorted(by_top, key=str.lower):
        lines.append(f"  {k:<58} {by_top[k]:>5}")
    lines += ["", "By extension", "-" * 78]
    for k in sorted(by_ext):
        lines.append(f"  {k:<58} {by_ext[k]:>5}")
    lines += ["", "Every non-HTML entry, by folder", "-" * 78]
    for p in files:
        if p.suffix.lower() != ".html":
            lines.append(f"  {str(p.relative_to(pack))}")
    lines += ["", "Full listing", "-" * 78]
    for p in files:
        lines.append(f"  {str(p.relative_to(pack))}")
    (pack / "_Pack_Notes" / "MANIFEST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(files), by_ext, by_top


CHANGES_BASE = "d421b38"     # the pack this one replaces

def delta_by_taxonomy(fwd):
    """Group the repo delta since CHANGES_BASE by the DRIVE folder it lands in.

    Staff read this against the folders they actually have, not against repo paths."""
    import subprocess
    try:
        out = subprocess.check_output(
            ["git", "-C", str(REPO), "diff", "--name-only", f"{CHANGES_BASE}..HEAD"],
            text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return {}, 0
    groups, total = {}, 0
    for rel in out.split("\n"):
        rel = rel.strip()
        if not rel or rel not in fwd:
            continue                     # changed but not shipped -> not staff's concern
        top = fwd[rel].split("/")[0] if "/" in fwd[rel] else "(root files)"
        groups.setdefault(top, []).append(fwd[rel])
        total += 1
    return groups, total


def write_changes_since(pack, counts, mark_html):
    """C5 -- CHANGES_SINCE is staff-facing and already exists on the drive at
    the root. Merging a stale one is worse than merging none, so it is
    regenerated for THIS pack."""
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-brand" content="progress-schools">
<title>What changed &middot; Progress Schools lessons</title>
<style>
body{{margin:0;background:#fbfbfc;color:#1a1a1e;font:16px/1.65 system-ui,-apple-system,sans-serif}}
.wrap{{max-width:720px;margin:0 auto;padding:32px 20px}}
header{{text-align:center;margin-bottom:1.2rem}}
.strip{{margin-top:.5rem;font:600 11px/1 system-ui,sans-serif;letter-spacing:.08em}}
h1{{font-size:1.35rem;margin:1.2rem 0 .2rem;text-align:center}}
p.sub{{text-align:center;color:#63636e;font-size:.88rem;margin:0 0 1.6rem}}
h2{{font-size:1rem;margin:1.6rem 0 .4rem;padding-bottom:.3rem;border-bottom:1px solid #e3e3e8}}
.card{{background:#fff;border:1px solid #e3e3e8;border-radius:10px;padding:14px 18px;margin:0 0 10px}}
.warn{{border-left:4px solid #E5007D}}
code{{background:#f2f2f5;padding:1px 5px;border-radius:4px;font-size:.86em}}
ul{{margin:.4rem 0;padding-left:1.2rem}}
footer{{text-align:center;font:400 10px/1.4 system-ui,sans-serif;opacity:.55;margin-top:2rem}}
</style></head><body>
<div class="wrap">
<header>{mark_html}</header>
<h1>What changed in this update</h1>
<p class="sub">11 August 2026 &middot; __PAGE_COUNT__ pages &middot; replaces the 7 August set</p>

<h2>The headline: three alternative routes</h2>
<div class="card"><strong>Three new folders carry a complete alternative Autumn 1 route.</strong>
<ul>
<li><code>BUILD Estate v3 (Alternative Route)</code></li>
<li><code>GROW Estate v3 (Alternative Route)</code></li>
<li><code>LAUNCH Estate v3 (Alternative Route)</code></li>
</ul>
These are <em>parallel</em> sets of lessons, not updates to the ones you have. Nothing in your
current folders was changed, moved or replaced by them. <strong>If you do nothing, you teach
exactly what you taught before.</strong> Which route to teach is a staff decision.
<br><br>
They differ on printing, so check before you plan: {counts['build_print']} of
{counts['build_lessons']} BUILD lessons print, {counts['grow_print']} of {counts['grow_lessons']}
GROW, {counts['launch_print']} of {counts['launch_lessons']} LAUNCH. Print packs for the
screen-only lessons follow later. Each folder has <code>0_ABOUT_THIS_ROUTE.txt</code> inside it.</div>

<div class="card"><strong>A fourth new folder, <code>_New_This_Rebuild</code>,</strong> holds
current teaching material that has no folder on this drive yet — an 8-page baseline assessment
pack. Rather than guess where it belongs, the build filed it there and said so. Drag it wherever
you want it, or leave it. <code>0_README.txt</code> inside names every file.</div>

{counts['delta_html']}

<h2>Read this first</h2>
<div class="card warn"><strong>Careers weeks 6 and 7 — go by the slide, never the filename.</strong>
<ul>
<li>Week 6 teaches <em>What Happens After Year 11</em> — open <code>CAREERS_W7_After_Year_11</code></li>
<li>Week 7 teaches <em>My Career Profile</em> — open <code>CAREERS_W6_My_Career_Profile</code></li>
</ul>
An earlier pack said the opposite ("the filename is right"). That was wrong. The full note is in
the Careers folder as <code>0_WEEK_ORDER.txt</code>. Do not rename the files — the hub and the
scheme of work link to them by name.</div>

<div class="card warn"><strong>Nothing dated 21 July may be deleted.</strong> The Humanities
organisers, receipt packs, role cards, consent logs and moderation guides were made by hand and
cannot be regenerated. This update ships nothing with those names and does not touch them.</div>

<h2>Branding</h2>
<div class="card">The real Progress Schools logo replaces the placeholder mark, embedded in the
page itself so it still shows when a file is moved or opened offline. It is on
{counts['logo_pages']} of the {counts['pages']} pages here — every page that carried a visible
mark, plus the pages this build writes. The rest never carried one and were not given one; they
carry the Progress Schools tag and credit line only.</div>

<h2>Structure</h2>
<div class="card">The ASDAN LAUNCH folder is flat, so each strand's start page is now named after
its strand (<code>START_HERE_Careers</code>, <code>START_HERE_PEQ</code>, and so on). The plain
<code>START_HERE</code> in that folder is now a chooser page linking to all five.</div>

<h2>Practical</h2>
<div class="card"><strong>Sync or download — do not teach from the OneDrive web preview.</strong>
The preview may not apply linked stylesheets, so a scheme of work can render unstyled.</div>
<div class="card"><strong>Ticks and cold-call lists live on the machine, not in the file.</strong>
Anything you tick in a deck is stored in that browser on that computer. It does not follow the file
and it is not on the drive. Print the paper tracker in Tutor Time for anything that matters.</div>

<footer>{CREDIT}</footer>
</div>
</body></html>
"""
    (pack / "CHANGES_SINCE.html").write_text(doc, encoding="utf-8")



# ---- D4: vendor the web fonts.
# Three in-scope pages fetch Google Fonts. A third-party fetch has no place in an
# offline pack: on a school machine without internet the request simply fails, and
# on one with internet it phones out on every open. Matt ruled: vendor the files
# rather than drop the link, so the typography is preserved exactly.
#
# Cached on disk so a rebuild does not depend on the network. The build FAILS if a
# font cannot be resolved -- it never silently leaves the <link> in place.
FONT_CACHE = Path(os.environ.get("PACK_FONT_CACHE",
                  str(Path.home() / ".cache" / "ps-pack-fonts")))
FONT_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
FONT_SUBSETS = ("latin", "latin-ext")     # a UK pack renders no Cyrillic, Greek or Vietnamese
FONT_LINK = re.compile(
    r'\s*<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>', re.I)
FONT_CSS_HREF = re.compile(
    r'<link[^>]*href="(https://fonts\.googleapis\.com/css2\?[^"]+)"[^>]*>', re.I)


def _fetch(url, cache):
    import urllib.request, hashlib
    key = cache / (hashlib.sha256(url.encode()).hexdigest()[:32] + ".bin")
    if key.exists():
        return key.read_bytes()
    data = urllib.request.urlopen(urllib.request.Request(url, headers=FONT_UA), timeout=60).read()
    cache.mkdir(parents=True, exist_ok=True)
    key.write_bytes(data)
    return data


def vendor_fonts(text, cache):
    """Replace Google Fonts <link>s with an inlined @font-face block.

    Returns (text, families_inlined, bytes_added). Raises if a font cannot be
    fetched -- shipping the link would defeat the whole point."""
    hrefs = FONT_CSS_HREF.findall(text)
    if not hrefs:
        # preconnect-only pages still carry an outbound hint; strip it
        new, n = FONT_LINK.subn("", text)
        return new, 0, 0
    blocks, families = [], set()
    for href in hrefs:
        css = _fetch(html.unescape(href), cache).decode("utf-8", "replace")
        for _pre, subset, blk in re.findall(
                r'(/\*\s*([a-z0-9-]+)\s*\*/\s*)?(@font-face\s*\{[^}]*\})', css):
            if subset not in FONT_SUBSETS:
                continue
            m = re.search(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', blk)
            if not m:
                continue
            fam = re.search(r"font-family:\s*'([^']+)'", blk)
            if fam: families.add(fam.group(1))
            woff = _fetch(m.group(1), cache)
            blocks.append(blk.replace(
                m.group(1), "data:font/woff2;base64," + base64.b64encode(woff).decode()))
    assert blocks, f"font vendoring produced nothing for {hrefs[:1]}"
    style = ("\n<style data-vendored-fonts=\"progress-schools\">\n/* "
             + ", ".join(sorted(families)) + " -- vendored from Google Fonts under the\n"
             "   SIL Open Font License 1.1. Full licence text: FONT_LICENCES.txt in this folder.\n"
             "   Inlined so this pack makes no network request. */\n"
             + "\n".join(blocks) + "\n</style>")
    n0 = len(text)
    text = FONT_LINK.sub("", text)               # remove every link AND the preconnects
    text = re.sub(r'</head>', style + "\n</head>", text, count=1, flags=re.I)
    return text, sorted(families), len(text) - n0



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo", help="Progress Schools logo PNG; enables mirror-pack mode")
    ap.add_argument("--mirror", action="store_true", help="assemble in the OneDrive taxonomy")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.mirror:
        if not a.logo:
            sys.exit("HARD STOP: --mirror requires --logo. There is no fallback to the "
                     "typographic mark - REBRAND.md rule 1 is superseded and a pack built "
                     "without the real lockup is not a Progress Schools pack.")
        mirror_main(a.logo, a.out)
    else:
        main()
