#!/usr/bin/env python3
"""Progress Schools ASDAN PEQ OneDrive mirror pack.

One zip whose single top-level folder is `ASDAN PEQ/`, mirroring the ASDAN PEQ
folder of Matt's OneDrive (screenshots of 2026-08-12) so it can be dragged onto
the drive's `ASDAN PEQ` and merged. Every page is rebranded to Progress Schools.

Like tools/build_art_mirror.py before it, this does NOT reimplement the rebrand.
It imports the proven primitives from tools/build_staff_pack.py (the PACK-4
mirror builder, merged in PR #92) and supplies what is specific to this pack:

  1. scope     -- the three ASDAN pathway trees + the D&T strand, nothing else
  2. geometry  -- repo paths -> `ASDAN PEQ/...` drive paths, with the NEW
                  foldered Launch sort (supersedes the 7 Aug flat taxonomy
                  for the Launch folder only)
  3. gates     -- the geometry gate, the R-J01 content-matched logo swap, the
                  semantic week census, and this brief's content locks

Usage:
    python3 tools/build_asdan_peq_mirror.py --logo PATH --repo PATH --out DIR

The logo binary never enters git. It is passed in and SHA-gated by
bsp.load_logo. The finished zip never enters git either.
"""
import os, sys, re, html, json, shutil, zipfile, subprocess, base64
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse, unquote, quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_staff_pack as bsp

TOP = "ASDAN PEQ"
X_BRAND = "Progress Schools Tees Valley — internal copy"
X_BRAND_META = f'<meta name="x-brand" content="{X_BRAND}">'

# ---------------------------------------------------------------- geometry
# Drive names, not repo names. Where they disagree, THE DRIVE WINS.
BUILD_SUBS = ["Careers", "Community_Project", "Duke_and_Enterprise",
              "FoodWise", "Living_Independently"]          # repo == drive
GROW_SUBS = {                                              # repo -> drive
    "Community_Project": "Community Project",
    "Enterprise":        "Community and Enterprise",
    "PEQ":               "Personal Effectiveness",
}
# The NEW foldered Launch sort. Each strand keeps its own plain START_HERE --
# safe inside its own folder, so the flat-era START_HERE_<strand> renames are
# retired (they become DELETE-after-merge entries in the placement guide).
LAUNCH_SUBS = {
    "Careers":              "Careers",
    "Community_Enterprise": "Community",
    "Living_Independently": "Independent Living",
    "PEQ":                  "PEQ",
    "Vocational":           "Vocational",
}
BUILD_ROOT = ["BUILD_ASDAN_Hub.html", "Resources_and_Tools.html", "Scheme_of_Work.html"]
GROW_ROOT  = ["GROW_ASDAN_Hub.html", "Resources_and_Tools.html", "Scheme_and_Resources.html",
              "visual-upgrade.css", "visual-upgrade.js"]
LAUNCH_ROOT = ["LAUNCH_ASDAN_Hub.html", "Resources_and_Tools.html", "Scheme_of_Work.html",
               "visual-upgrade.css", "visual-upgrade.js"]

# Links that must resolve on the DRIVE, outside this zip. Because the zip's
# top folder merges onto the drive's `ASDAN PEQ`, a shipped file's zip path IS
# its drive path, so the drive-relative form is a plain relpath between the
# two. These are the ONLY link targets allowed to leave the zip; the crawl
# whitelists exactly these drive-root paths and nothing else.
EXTERNAL = {
    "LundyLoop/assets/style.css":  "LundyLoop/assets/style.css",
    "Tutor_Time/START_HERE.html":  "Tutor Time BF_BV_KCSIE/START_HERE.html",
    "Tutor_Time/Scheme_of_Work.html": "Tutor Time BF_BV_KCSIE/Scheme_of_Work.html",
}

# GEOMETRY GATE (permanent): a repo-tree name at any level = instant FAIL.
REPO_TREE_NAMES = {"BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN", "Slideshows",
                   "DT_Community_Upcycling", "Community_Enterprise", "Enterprise"}

# R-J01: the Made-by-Matt mark, matched by SVG CONTENT, never by aria-label.
# 12 entry docs (7 LAUNCH + 5 GROW) carry the mark without the label; the
# labelled swap in bsp.mirror_rebrand misses them. The second path is the
# monogram favicon form the Art pack found -- none in this scope today, but
# the gate scans for both, in inline SVG and in base64 data URIs.
MARK_PATH_SIGS = ["M28 71 L28 37 L50 59 L72 37 L72 71",
                  "M26 76 L26 30 L50 55 L74 30 L74 76"]
ANY_SVG = re.compile(r"<svg[^>]*>.*?</svg>", re.S | re.I)
SVG_B64 = re.compile(r"data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)")

WEEK6_TOPIC = "After Year 11"          # Pass H: W6 = After Year 11 / post-16
WEEK7_TOPIC = "My Career Profile"      # Pass H: W7 = My Career Profile


# ---------------------------------------------------------------- scope
def scope(repo: Path):
    """[(repo_rel, dest_rel)] with dest_rel drive-rooted (starts `ASDAN PEQ/`),
    plus the deliberate exclusions. Mechanical: strand contents are globbed
    from disk, root files are named and asserted to exist."""
    pairs, dropped = [], []

    def add_dir(repo_dir, dest_dir):
        found = sorted((repo / repo_dir).glob("*.html"))
        assert found, f"empty strand: {repo_dir}"
        for p in found:
            pairs.append((f"{repo_dir}/{p.name}", f"{dest_dir}/{p.name}"))

    def add_file(rel, dest):
        assert (repo / rel).exists(), f"missing {rel}"
        pairs.append((rel, dest))

    # --- Build
    for sub in BUILD_SUBS:
        add_dir(f"BUILD_ASDAN/{sub}", f"{TOP}/Build/{sub}")
    for name in BUILD_ROOT:
        add_file(f"BUILD_ASDAN/{name}", f"{TOP}/Build/{name}")
    add_file("build_asdan.html", f"{TOP}/Build/build_asdan.html")   # position-rebuilt
    dt_decks = sorted(repo.glob("Build/Slideshows/BUILD_DT_W*.html"))
    assert len(dt_decks) == 6, f"expected 6 D&T decks, found {len(dt_decks)}"
    for p in dt_decks:
        pairs.append((f"Build/Slideshows/{p.name}", f"{TOP}/Build/DT/{p.name}"))
    add_file("build_dt_upcycling.html", f"{TOP}/Build/DT/build_dt_upcycling.html")
    for name in ("Scheme_of_Work.html", "Weekly_Plan.html"):
        add_file(f"DT_Community_Upcycling/{name}", f"{TOP}/Build/DT/{name}")

    # --- Grow (drive folder names carry SPACES)
    for sub, drive in GROW_SUBS.items():
        add_dir(f"GROW_ASDAN/{sub}", f"{TOP}/Grow/{drive}")
    for name in GROW_ROOT:
        add_file(f"GROW_ASDAN/{name}", f"{TOP}/Grow/{name}")

    # --- Launch (the NEW foldered sort)
    for sub, drive in LAUNCH_SUBS.items():
        add_dir(f"LAUNCH_ASDAN/{sub}", f"{TOP}/Launch/{drive}")
    for name in LAUNCH_ROOT:
        add_file(f"LAUNCH_ASDAN/{name}", f"{TOP}/Launch/{name}")

    # --- exclusions, recorded not silent
    shipped = {r for r, _ in pairs}
    for tree in ("BUILD_ASDAN", "GROW_ASDAN", "LAUNCH_ASDAN", "DT_Community_Upcycling"):
        for p in sorted((repo / tree).rglob("*")):
            if not p.is_file():
                continue
            rel = str(p.relative_to(repo))
            if rel in shipped:
                continue
            why = ("build/QA tooling, not a lesson" if "_framework/" in rel
                   else "repo documentation / working note, not on the drive")
            dropped.append((rel, why))

    # destination collision guard
    seen = {}
    for r, d in pairs:
        assert d not in seen, f"DESTINATION COLLISION: {seen[d]} and {r} both -> {d}"
        seen[d] = r
    return pairs, dropped


# ---------------------------------------------------------------- rebrand
def swap_marks_by_content(text, mark_html):
    """Replace any remaining Made-by-Matt SVG, matched on its path data.

    Runs AFTER the shared (aria-label) swap; catches the R-J01 unlabelled 12.
    Verified against the repo: the signature never appears inside a <script>
    block in this scope, so a whole-document sub is safe."""
    n = [0]

    def one(m):
        if any(sig in m.group(0) for sig in MARK_PATH_SIGS):
            n[0] += 1
            return mark_html
        return m.group(0)

    return ANY_SVG.sub(one, text), n[0]


def fix_contact(text):
    """The shared rebrand names the science lead -- wrong subject here -- and
    leaves it inside href="mailto:...". Same correction the Art pack made."""
    text, k1 = re.subn(r"your Progress Schools science lead",
                       "your Progress Schools ASDAN lead", text)
    text, k2 = re.subn(r'<a\s+href="mailto:([^"@]*)"([^>]*)>(.*?)</a>',
                       lambda m: f"<span{m.group(2)}>{m.group(3)}</span>",
                       text, flags=re.S | re.I)
    return text, k1, k2


def asdan_rebrand(text, rel, mark_html):
    new, log = bsp.mirror_rebrand(text, rel, mark_html)
    new, k = swap_marks_by_content(new, mark_html)
    if k:
        log["logo_swapped"] = log.get("logo_swapped", 0) + k
        log["logo_content_matched"] = k
    # normalise the x-brand marker to this pack's long form
    new, n = re.subn(r'<meta\s+name="x-brand"\s+content="[^"]*"\s*/?>',
                     X_BRAND_META, new, flags=re.I)
    if not n:
        new, n = re.subn(r"(<head[^>]*>)", r"\1\n" + X_BRAND_META, new,
                         count=1, flags=re.I)
    log["xbrand"] = 1 if n else 0
    new, k1, k2 = fix_contact(new)
    log["contact_subject"] = k1
    log["dead_mailto_unwrapped"] = k2
    return new, log


# ---------------------------------------------------------------- links
HREF = re.compile(r'\b(href|src)\s*=\s*(["\'])(.*?)\2', re.I | re.S)
SKIP_RAW = ("http://", "https://", "//", "#", "data:", "mailto:", "javascript:", "/")


def rewrite_external(text, src_rel, dest_rel):
    """Point the known drive-root dependencies at their drive-relative paths,
    resolved from THIS file's destination. Runs after bsp.rewrite_links, which
    leaves unknown targets alone."""
    src_dir = os.path.dirname(str(src_rel))
    dst_dir = os.path.dirname(dest_rel)
    n = [0]

    def one(m):
        attr, q, raw = m.group(1), m.group(2), m.group(3)
        if not raw or raw.startswith(SKIP_RAW) or "${" in raw or "{{" in raw:
            return m.group(0)
        parts = urlparse(raw)
        target = unquote(parts.path)
        if not target:
            return m.group(0)
        repo_target = os.path.normpath(os.path.join(src_dir, target)).replace("\\", "/")
        if repo_target not in EXTERNAL:
            return m.group(0)
        new = os.path.relpath(EXTERNAL[repo_target], dst_dir).replace("\\", "/")
        if parts.query:
            new += "?" + parts.query
        if parts.fragment:
            new += "#" + parts.fragment
        n[0] += 1
        return f"{attr}={q}{new}{q}"

    return HREF.sub(one, text), n[0]


def crawl_pack(pack: Path):
    """Every internal link, crawled from each file's own location. A target is
    OK if it exists in the pack, or if it normalises to exactly one of the
    whitelisted drive-root paths. Everything else is broken."""
    whitelist = set(EXTERNAL.values())
    broken, external_used = defaultdict(set), defaultdict(int)
    for p in sorted(pack.rglob("*.html")):
        rel = str(p.relative_to(pack))
        t = p.read_text(encoding="utf-8", errors="ignore")
        for m in HREF.finditer(t):
            raw = html.unescape(m.group(3))
            if not raw or raw.startswith(SKIP_RAW) or "${" in raw or "{{" in raw:
                continue
            target = unquote(urlparse(raw).path)
            if not target:
                continue
            joined = os.path.normpath(
                os.path.join(os.path.dirname(rel), target)).replace("\\", "/")
            if (pack / joined).exists():
                continue
            if joined in whitelist:
                external_used[joined] += 1
                continue
            broken[rel].add(raw)
    return broken, dict(external_used)


# ---------------------------------------------------------------- generated pages
def chooser_page(mark_html):
    """The Progress-branded chooser at Launch/START_HERE.html, updated to point
    into the five strand FOLDERS (the flat-era names are dead)."""
    strands = sorted(LAUNCH_SUBS.values())
    items = "\n".join(
        f'    <li><a href="{quote(s)}/START_HERE.html">{html.escape(s)}</a></li>'
        for s in strands)
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{X_BRAND_META}
<title>Start Here · LAUNCH ASDAN</title>
<style>
body{{margin:0;background:#fbfbfc;color:#1a1a1e;font:16px/1.6 system-ui,-apple-system,sans-serif}}
.wrap{{max-width:640px;margin:0 auto;padding:32px 20px}}
header{{text-align:center;margin-bottom:1.5rem}}
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
<p class="sub">LAUNCH holds five strands, one folder each. Pick the one you are teaching.</p>
<ul>
{items}
</ul>
<div class="note">Each strand now lives in its own folder with its own
<code>START_HERE</code>. The old flat copies of these lessons (and the
<code>START_HERE_&lt;strand&gt;</code> pages) are superseded &mdash; the placement
guide lists each one to delete after the merge.</div>
<footer>{bsp.CREDIT}</footer>
</div>
</body></html>
"""


def write_section_index(pack: Path, logo_uri, logo_size):
    """`ASDAN PEQ/index.html` -- the section index at the folder root, built for
    this position from the assembled tree (never from the repo's estate hub,
    which is out of scope here)."""
    top = pack / TOP
    groups = defaultdict(list)
    for p in sorted(top.rglob("*.html"), key=lambda x: str(x).lower()):
        d = str(p.relative_to(top))
        if d == "index.html":
            continue
        groups[d.split("/")[0]].append(d)
    w, h = logo_size
    rows = []
    for g in sorted(groups, key=str.lower):
        rows.append(f'<section><h2>{html.escape(g)}'
                    f'<span class="n">{len(groups[g])} pages</span></h2><ul>')
        for d in groups[g]:
            label = d.rsplit("/", 1)[-1][:-5].replace("_", " ")
            href = "/".join(quote(s) for s in d.split("/"))
            rows.append(f'<li><a href="{href}">{html.escape(label)}</a>'
                        f'<span class="p">{html.escape(os.path.dirname(d))}</span></li>')
        rows.append("</ul></section>")
    doc = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{X_BRAND_META}
<title>Progress Schools · ASDAN PEQ</title>
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
ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:2px}}
li{{padding:5px 8px;border-radius:7px;min-width:0}}
li:hover{{background:var(--bg)}}
a{{color:var(--fg);text-decoration:none;font-size:.88rem;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
a:hover{{color:var(--acc);text-decoration:underline}}
.p{{display:block;font-size:.68rem;color:var(--mut);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
footer{{text-align:center;color:var(--mut);font-size:.7rem;padding:18px}}
</style></head><body>
<header>
<span class="chip"><img src="{logo_uri}" width="{w}" height="{h}" alt="Progress Schools"></span>
<div class="strip">{bsp.STRIP}</div>
<h1>ASDAN PEQ</h1>
<p class="sub">{sum(len(v) for v in groups.values())} pages · BUILD · GROW · LAUNCH · nothing loads from the internet</p>
</header>
<main>
{chr(10).join(rows)}
</main>
<footer>{bsp.CREDIT}</footer>
</body></html>
"""
    (top / "index.html").write_text(doc, encoding="utf-8")
    return sum(len(v) for v in groups.values())


# ---------------------------------------------------------------- guide
def launch_delete_list(repo: Path):
    """The flat-era Launch files to delete after the merge: every strand
    lesson's bare name (they sat loose in Launch/) plus the five flat-era
    START_HERE_<strand> disambiguations. Walked from disk, never typed."""
    loose = []
    for sub in LAUNCH_SUBS:
        for p in sorted((repo / "LAUNCH_ASDAN" / sub).glob("*.html")):
            if p.name != "START_HERE.html":
                loose.append(p.name)
    flats = [f"START_HERE_{sub}.html" for sub in sorted(LAUNCH_SUBS)]
    return loose, flats


def write_placement_guide(pack: Path, repo: Path, counts, total, external_used):
    loose, flats = launch_delete_list(repo)
    L = []
    add = L.append
    add("=" * 74)
    add("PROGRESS SCHOOLS · ASDAN PEQ — ONEDRIVE MIRROR PACK")
    add("=" * 74)
    add("")
    add("WHAT THIS IS")
    add("")
    add("  One folder, `ASDAN PEQ`, shaped exactly like the `ASDAN PEQ` folder on")
    add("  your OneDrive. Every page is rebranded to Progress Schools. Nothing")
    add("  loads from the internet.")
    add("")
    add("HOW TO PLACE IT")
    add("")
    add("  1. Unzip. You get a single folder called  ASDAN PEQ")
    add("  2. Drag it onto your OneDrive, on top of the existing `ASDAN PEQ`.")
    add("  3. Choose MERGE (\"Merge the folders\"), then REPLACE files when asked.")
    add("  4. Nothing outside `ASDAN PEQ` is touched.")
    add("")
    add("WHAT IS IN IT")
    add("")
    for folder in sorted(counts):
        add(f"  {folder + '/':<42} {counts[folder]:>3} files")
    add(f"  {'TOTAL':<42} {total:>3} files")
    add("")
    add("-" * 74)
    add("")
    add("LAUNCH IS NOW FOLDERED — DELETE THE OLD FLAT COPIES AFTER THE MERGE")
    add("")
    add("  Each LAUNCH strand now lives in its own folder (Careers, Community,")
    add("  Independent Living, PEQ, Vocational), each with its own START_HERE.")
    add("  The old flat copies in the Launch folder root are superseded. After")
    add("  the merge, delete each of these from `ASDAN PEQ/Launch/` if present:")
    add("")
    for n in loose:
        add(f"      {n}")
    add("")
    add("  ... and the five flat-era chooser targets:")
    add("")
    for n in flats:
        add(f"      {n}")
    add("")
    add("  KEEP `Launch/START_HERE.html` — this pack replaces it with a chooser")
    add("  that points into the five strand folders.")
    add("")
    add("-" * 74)
    add("")
    add("DELIBERATELY NOT IN THIS PACK — a merge cannot touch any of these")
    add("")
    add("  * BUILD_ASDAN_Year_SoW_2026-27.xlsx        (Build folder)")
    add("  * GROW_ASDAN_Year_SoW_2026-27.xlsx         (Grow folder)")
    add("  * GROW_Autumn_Year_Plan_ASDAN.xlsx         (Grow folder)")
    add("  * Scheme_of_Work / Weekly_Plan / PLACE_THIS_README at the ASDAN PEQ root")
    add("  * 0_ABOUT_THIS_FOLDER (Build folder)")
    add("  * everything under Planning/ (standing rule: never in any pack)")
    add("")
    add("  These are drive-only or Planning-lineage artefacts. The pack ships no")
    add("  file with any of those names, so the merge leaves each one untouched.")
    add("")
    add("-" * 74)
    add("")
    add("CAREERS WEEKS 6 AND 7 — GO BY THE SLIDE, NEVER THE FILENAME")
    add("")
    add("  Week 6 = \"What Happens After Year 11\" = file CAREERS_W7_After_Year_11.html")
    add("  Week 7 = \"My Career Profile\"          = file CAREERS_W6_My_Career_Profile.html")
    add("  The full note travels as  Build/Careers/0_WEEK_ORDER.txt.  Do NOT rename")
    add("  the files — the hub and the scheme of work link to them by name.")
    add("")
    add("-" * 74)
    add("")
    add("EXTERNAL DEPENDENCIES — two folders at the DRIVE root")
    add("")
    add("  * `LundyLoop/` — the D&T pages and the Build hub load")
    add("    LundyLoop/assets/style.css by a relative path that climbs out of")
    add("    ASDAN PEQ to the drive root. Your drive already has that folder;")
    add("    keep it where it is and the styling resolves.")
    add("  * `Tutor Time BF_BV_KCSIE/` — the Build hub links to its START_HERE")
    add("    and Scheme_of_Work the same way.")
    if external_used:
        add("")
        add("  Link targets outside this zip, counted at build time:")
        for k in sorted(external_used):
            add(f"      {k}   ({external_used[k]} reference(s))")
    add("")
    add("VIEWING THE PAGES")
    add("")
    add("  * OneDrive's web preview may ignore linked CSS, so a scheme of work can")
    add("    render unstyled in the browser preview. Sync the folder, or download")
    add("    the file, and open it locally in Edge or Chrome.")
    add("  * Start at  ASDAN PEQ/index.html")
    add("")
    add("PUPIL DATA")
    add("")
    add("  These pages store nothing on a server. Anything typed into a deck is")
    add("  saved in that browser on that machine only. No pupil data of any kind")
    add("  is in this pack.")
    add("")
    add("=" * 74)
    (pack / TOP / "PLACEMENT_GUIDE.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- validation
def residue_sweep(pack: Path, whitelist: bool):
    hits, detail = 0, []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        s = t.replace(">" + bsp.CREDIT + "<", "><", 1) if whitelist else t
        if bsp.PERSONAL_RESIDUE.search(s):
            hits += 1
            detail.append(str(p.relative_to(pack)))
    return hits, detail


def matt_mark_census(pack: Path):
    """0 Matt-mark SVGs may ship, checked by CONTENT: inline SVG and base64
    data URIs both, against both known path signatures."""
    bad = []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        if any(sig in t for sig in MARK_PATH_SIGS):
            bad.append(f"{p.relative_to(pack)}: mark path in document text")
            continue
        for m in SVG_B64.finditer(t):
            try:
                svg = base64.b64decode(m.group(1)).decode("utf-8", "ignore")
            except Exception:
                continue
            if any(sig in svg for sig in MARK_PATH_SIGS):
                bad.append(f"{p.relative_to(pack)}: mark path inside a data URI")
                break
    return bad


def week_census(pack: Path):
    """Semantic week census over every shipped page (house rule: mtime is not
    evidence). Any adjacency pairing Week 6 with the W7 topic, or Week 7 with
    the W6 topic, in either order, fails. The correct pairings must also be
    POSITIVELY present on the Careers surfaces."""
    fails, good6, good7 = [], 0, 0
    bad_pats = [
        re.compile(r'Week\s*6\b[^<>{}"]{0,120}' + re.escape(WEEK7_TOPIC)),
        re.compile(re.escape(WEEK7_TOPIC) + r'[^<>{}"]{0,60}Week\s*6\b'),
        re.compile(r'Week\s*7\b[^<>{}"]{0,120}(' + re.escape(WEEK6_TOPIC) + r"|post.?16 routes)"),
        re.compile(re.escape(WEEK6_TOPIC) + r'[^<>{}"]{0,60}Week\s*7\b'),
    ]
    good6_pat = re.compile(r'Week\s*6\b[^<>{}"]{0,120}' + re.escape(WEEK6_TOPIC))
    good7_pat = re.compile(r'Week\s*7\b[^<>{}"]{0,120}' + re.escape(WEEK7_TOPIC))
    for p in sorted(pack.rglob("*.html")):
        t = html.unescape(p.read_text(encoding="utf-8", errors="ignore"))
        for pat in bad_pats:
            m = pat.search(t)
            if m:
                fails.append(f"{p.relative_to(pack)}: {m.group(0)[:90]!r}")
        good6 += len(good6_pat.findall(t))
        good7 += len(good7_pat.findall(t))
    if good6 == 0:
        fails.append(f"no surface pairs Week 6 with '{WEEK6_TOPIC}'")
    if good7 == 0:
        fails.append(f"no surface pairs Week 7 with '{WEEK7_TOPIC}'")
    return fails, good6, good7


FOOD_TOKENS = re.compile(r"calorie|calories|kcal|weight loss|lose weight|slimming|diet plan|restrict",
                         re.I)
FOOD_RULED = ("not calories or a pupil",          # the payload guardrail sentence
              "the calories, or something else",  # the ruled FW_W2 swap-logic line
              "never restriction")                # LI_W6 teacher note banning restriction talk


def content_locks(pack: Path, repo: Path):
    fails = []
    unit_shape = re.compile(r"\b[A-Za-z]{2,8}Sk(?:E3|\d)\b")
    codes = defaultdict(lambda: defaultdict(int))
    for p in sorted(pack.rglob("*.html")):
        rel = str(p.relative_to(pack))
        t = p.read_text(encoding="utf-8", errors="ignore")
        for c in unit_shape.findall(t):
            codes[c][rel.split("/")[1] if rel.count("/") else "(root)"] += 1
        # banned strings, per the estate gate lists. NB `ll-g:loop-mark` is NOT
        # banned here: that sentinel legitimately ships inside the built lessons
        # (REGISTER: "= 50, SET-invariant"); gates.py bans it only in freshly
        # AUTHORED files, which this pack contains none of.
        for b in ("ASDAN Studio · ASDAN Studio", "Delivering a Project"):
            if b in t:
                fails.append(f"{rel}: banned string {b!r}")
        # An L2 CLAIM fails; an explicit DENIAL ("no L2 registration", "never an
        # L2 registration") is the compliant form the estate requires and passes.
        # Scoped to Launch/: the zero-L2 census is the LAUNCH suite's (REGISTER
        # claims census); GROW's Scheme carries a Matt-approved CONDITIONAL
        # ("pupils who fly can be registered for Level 2 units — UAS
        # coordinator decision") that is not a claim and must not be stripped.
        if rel.startswith(f"{TOP}/Launch/"):
            low = t.lower()
            for b in ("register at level 2", "level 2 registration", "l2 registration",
                      "registered for level 2", "banked at level 2", "level 2 award",
                      "level 2 certificate", "level 2 extended award"):
                for m in re.finditer(re.escape(b), low):
                    lead = low[max(0, m.start() - 40):m.start()]
                    if re.search(r"\b(no|never(\s+an)?|not|zero|without)\b[^.!?]{0,30}$", lead):
                        continue
                    fails.append(f"{rel}: L2 claim {b!r}: "
                                 f"...{t[max(0, m.start()-50):m.end()+30]!r}...")
        # calorie/restriction language: only the two ruled contexts may carry it
        for m in FOOD_TOKENS.finditer(t):
            ctx = t[max(0, m.start() - 120):m.end() + 120]
            if not any(r in ctx for r in FOOD_RULED):
                fails.append(f"{rel}: food-language outside the ruled lines: "
                             f"...{t[max(0,m.start()-40):m.end()+40]!r}...")
    # unit codes: the three spec-confirmed codes only, each confined to its home
    allowed_home = {"ComSk1": "Launch", "ThSk1": "Grow", "TmWkSk1": "Grow"}
    for c, homes in sorted(codes.items()):
        if c not in allowed_home:
            fails.append(f"unit code {c} is not spec-confirmed "
                         f"(allowed: {sorted(allowed_home)}) — found in {dict(homes)}")
        else:
            stray = {k: v for k, v in homes.items() if k != allowed_home[c]}
            if stray:
                fails.append(f"unit code {c} outside its home {allowed_home[c]}: {stray}")
    # practice-money lines intact: every LI lesson keeps its repo count
    money = re.compile(r"practice (money|notes|coins)|not real", re.I)
    for src in sorted((repo / "BUILD_ASDAN" / "Living_Independently").glob("LI_W*.html")):
        want = len(money.findall(src.read_text(encoding="utf-8", errors="ignore")))
        dest = pack / TOP / "Build" / "Living_Independently" / src.name
        got = len(money.findall(dest.read_text(encoding="utf-8", errors="ignore")))
        if got < want:
            fails.append(f"practice-money line lost in {src.name}: {want} -> {got}")
    return fails, {c: dict(h) for c, h in codes.items()}


def witness_census(pack: Path):
    """#print-witness present (and its Assessor section with it) in every
    lesson deck. Lessons = *_W*.html under the strand folders."""
    fails, n = [], 0
    for p in sorted(pack.rglob("*.html")):
        rel = str(p.relative_to(pack))
        parts = rel.split("/")
        if len(parts) != 4 or parts[1] not in ("Build", "Grow", "Launch"):
            continue
        name = parts[-1]
        if name == "START_HERE.html" or not re.search(r"_W\d", name):
            continue
        if parts[2] == "DT":
            continue                      # D&T decks are not ASDAN-witnessed
        n += 1
        t = p.read_text(encoding="utf-8", errors="ignore")
        if 'id="print-witness"' not in t:
            fails.append(f"{rel}: no #print-witness section")
        elif not re.search(r"Assessor (Witness Statement|declaration)", t):
            fails.append(f"{rel}: witness section lacks its Assessor heading")
    return fails, n


def inline_js_check(pack: Path):
    bad = []
    for p in sorted(pack.rglob("*.html")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for mm in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", t, re.S | re.I):
            body = mm.group(1).strip()
            if not body or (body.startswith("{") and body.endswith("}")):
                continue
            r = subprocess.run(["node", "--check", "-"], input=body, text=True,
                               capture_output=True)
            if r.returncode != 0:
                err = next((l for l in r.stderr.splitlines() if "Error" in l), "unknown")
                bad.append(f"{p.relative_to(pack)}: {err[:110]}")
                break
    return bad


def js_asset_check(pack: Path):
    bad = []
    for p in sorted(pack.rglob("*.js")):
        r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
        if r.returncode != 0:
            bad.append(f"{p.relative_to(pack)}: syntax error")
    return bad


# The drive listings, off the 2026-08-12 screenshots, with each truncated name
# resolved against a REAL filename before anything is compared. `shipped` names
# must exist in the assembled tree; `excluded` names must NOT.
SCREENSHOT_ITEMS = {
    f"{TOP}": {
        "shipped": ["Build", "Grow", "Launch", "index.html"],
        "excluded": ["PLACE_THIS_README", "Scheme_of_Work", "Weekly_Plan"],
    },
    f"{TOP}/Build": {
        "shipped": ["Careers", "Community_Project", "DT", "Duke_and_Enterprise",
                    "FoodWise", "Living_Independently", "build_asdan.html",
                    "BUILD_ASDAN_Hub.html", "Resources_and_Tools.html", "Scheme_of_Work.html"],
        "excluded": ["0_ABOUT_THIS_FOLDER", "BUILD_ASDAN_Year_SoW_2026-27"],
    },
    f"{TOP}/Grow": {
        "shipped": ["Community and Enterprise", "Community Project", "Personal Effectiveness",
                    "GROW_ASDAN_Hub.html", "Resources_and_Tools.html",
                    "Scheme_and_Resources.html", "visual-upgrade.css", "visual-upgrade.js"],
        "excluded": ["GROW_ASDAN_Year_SoW_2026-27", "GROW_Autumn_Year_Plan_ASDAN"],
    },
    f"{TOP}/Launch": {
        "shipped": ["Careers", "Community", "Independent Living", "PEQ", "Vocational",
                    "LAUNCH_ASDAN_Hub.html", "Resources_and_Tools.html", "Scheme_of_Work.html",
                    "START_HERE.html", "visual-upgrade.css", "visual-upgrade.js"],
        # the flat-era strays the screenshots still show; resolved from their
        # truncated display names to real filenames by launch_delete_list()
        "excluded": [],
    },
}
# Truncated names as the OneDrive UI shows them (prefix…suffix), each of which
# must resolve to exactly one real filename in the Launch delete list.
TRUNCATED_LAUNCH_STRAYS = [
    ("VOC_W1_Introdu", "and_Workplaces"),
    ("VOC_W2_Health_", "ygiene_at_Work"),
    ("VOC_W3_Followi", "ns_and_Routines"),
    ("VOC_W4_Teamw", "cational_Setting"),
    ("VOC_W5_Tools_E", "t_and_Safe_Use"),
    ("VOC_W6_Comple", "Vocational_Task"),
]


def screenshot_reconcile(pack: Path, repo: Path):
    """UNMAPPED census: every screenshot name resolves against a real shipped
    or deliberately-excluded name; anything unmatched is reported, not
    guess-dropped."""
    unmapped = []
    for folder, spec in SCREENSHOT_ITEMS.items():
        d = pack / folder
        have = {p.name for p in d.iterdir()} if d.exists() else set()
        for name in spec["shipped"]:
            if name not in have and name + "/" not in have:
                unmapped.append(f"screenshot item not shipped: {folder}/{name}")
        for name in spec["excluded"]:
            hits = [h for h in have if h.startswith(name)]
            if hits:
                unmapped.append(f"excluded item present in pack: {folder}/{hits[0]}")
    loose, _flats = launch_delete_list(repo)
    stems = {n[:-5] for n in loose}                       # sans .html
    for pre, suf in TRUNCATED_LAUNCH_STRAYS:
        matches = [s for s in stems if s.startswith(pre) and s.endswith(suf)]
        if len(matches) != 1:
            unmapped.append(f"truncated screenshot name {pre}…{suf} resolves to "
                            f"{len(matches)} repo filenames (need exactly 1)")
    return unmapped


def geometry_gate(pack: Path):
    fails = []
    roots = sorted(p.name for p in pack.iterdir())
    if roots != [TOP]:
        fails.append(f"GEOMETRY: zip root entries {roots}, must be exactly ['{TOP}']")
    want_children = {"Build", "Grow", "Launch", "index.html", "PLACEMENT_GUIDE.txt"}
    have_children = {p.name for p in (pack / TOP).iterdir()}
    if have_children != want_children:
        fails.append(f"GEOMETRY: {TOP} children {sorted(have_children)} != {sorted(want_children)}")
    want_launch = set(LAUNCH_SUBS.values()) | set(LAUNCH_ROOT) | {"START_HERE.html"}
    have_launch = {p.name for p in (pack / TOP / "Launch").iterdir()}
    if have_launch != want_launch:
        fails.append(f"GEOMETRY: Launch children {sorted(have_launch)} != {sorted(want_launch)}")
    for p in pack.rglob("*"):
        for part in p.relative_to(pack).parts:
            if part in REPO_TREE_NAMES:
                fails.append(f"GEOMETRY: repo-tree name {part!r} at {p.relative_to(pack)}")
                break
    return fails


# ---------------------------------------------------------------- main
def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    repo, out = Path(a.repo).resolve(), Path(a.out).resolve()
    bsp.REPO = repo

    print("=" * 70)
    print("PROGRESS SCHOOLS ASDAN PEQ MIRROR")
    print("=" * 70)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    print(f"repo HEAD: {head}")

    (lock_uri, lock_size), (mark_uri, mark_size) = bsp.load_logo(a.logo)
    print(f"logo OK  lockup {lock_size}  mark {mark_size}  "
          f"({len(lock_uri) * 3 // 4 / 1024:.1f} KB embedded)")
    mark_html = bsp.logo_html(lock_uri, lock_size)

    pairs, dropped = scope(repo)
    fwd = {r: d for r, d in pairs}
    print(f"scope: {len(pairs)} files in, {len(dropped)} deliberately excluded")

    if out.exists():
        shutil.rmtree(out)
    pack = out / "pack"
    (pack / TOP).mkdir(parents=True)

    # position-rebuilt pages get a visible mark even though the repo page never
    # drew one: staff land on them first.
    BRAND_HEADER = {"build_asdan.html", "build_dt_upcycling.html"}

    totals, logo_pages, rewrites, ext_rewrites = defaultdict(int), 0, 0, 0
    for rel, dest in pairs:
        src = repo / rel
        target = pack / dest
        if src.suffix != ".html":
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            continue
        raw = src.read_text(encoding="utf-8", errors="ignore")
        new, log = asdan_rebrand(raw, rel, mark_html)
        if log.get("logo_swapped"):
            logo_pages += 1
        elif rel in BRAND_HEADER:
            new, _ = bsp.brand_header(new, mark_html)
        new, n = bsp.rewrite_links(new, rel, fwd, dest_override=dest)
        rewrites += n
        new, n = rewrite_external(new, rel, dest)
        ext_rewrites += n
        for k, v in log.items():
            if k != "delta":
                totals[k] += v
        bsp.write_guarded(raw, new, target)   # read -> transform -> assert -> write
    print(f"rebrand: {dict(totals)}")
    print(f"link rewrites: {rewrites} internal, {ext_rewrites} drive-root external")

    # the Careers week-order note travels IN POSITION, inside the folder it warns about
    (pack / TOP / "Build" / "Careers" / "0_WEEK_ORDER.txt").write_text(
        bsp.WEEK_ORDER_NOTE, encoding="utf-8")

    # generated pages, authored BEFORE validation so every gate covers them
    (pack / TOP / "Launch" / "START_HERE.html").write_text(
        chooser_page(mark_html), encoding="utf-8")
    listed = write_section_index(pack, lock_uri, lock_size)
    print(f"generated {TOP}/index.html: {listed} pages listed")

    # counts describe the FINISHED tree: everything now on disk plus the guide
    counts = defaultdict(int)
    for f in sorted(pack.rglob("*")):
        if f.is_file():
            counts[os.path.dirname(str(f.relative_to(pack)))] += 1
    counts[TOP] += 1                                       # the guide, written next
    total_files = sum(counts.values())
    broken, external_used = crawl_pack(pack)               # pre-guide crawl for the guide's numbers
    write_placement_guide(pack, repo, dict(counts), total_files, external_used)

    # ---------------------------------------------------------- validation
    fails = []
    html_files = sorted(pack.rglob("*.html"))
    n_html = len(html_files)

    fails += geometry_gate(pack)
    unmapped = screenshot_reconcile(pack, repo)
    fails += unmapped

    broken, external_used = crawl_pack(pack)
    if broken:
        fails.append(f"CRAWL: {sum(len(v) for v in broken.values())} broken internal links")
        for f, ts in list(broken.items())[:10]:
            print("  BROKEN:", f, "->", sorted(ts)[:4])

    on, on_d = residue_sweep(pack, whitelist=True)
    off, _ = residue_sweep(pack, whitelist=False)
    if on:
        fails.append(f"RESIDUE (whitelist on) = {on}, expected 0: {on_d[:5]}")
    if off != n_html:
        fails.append(f"RESIDUE (whitelist off) = {off}, expected {n_html} "
                     "(exactly one anchored credit per page)")

    mark_fails = matt_mark_census(pack)
    fails += mark_fails

    week_fails, good6, good7 = week_census(pack)
    fails += week_fails

    lock_fails, code_census = content_locks(pack, repo)
    fails += lock_fails

    witness_fails, witnessed = witness_census(pack)
    fails += witness_fails
    if witnessed != 79:
        fails.append(f"witness census covered {witnessed} lessons, expected 79")

    nocredit = multicredit = noxb = tiny = notclosed = strip = hud = 0
    for p in html_files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        c = t.count(bsp.CREDIT)
        if c == 0: nocredit += 1
        elif c > 1: multicredit += 1
        if X_BRAND_META not in t: noxb += 1
        if bsp.STRIP in t: strip += 1
        if len(t) < 200: tiny += 1
        if not t.rstrip().lower().endswith("</html>"): notclosed += 1
        if re.search(r"hud\.js", t, re.I) or bsp.HUD_DYNAMIC.search(t): hud += 1
    if nocredit:    fails.append(f"{nocredit} pages missing the credit")
    if multicredit: fails.append(f"{multicredit} pages carry the credit more than once")
    if noxb:        fails.append(f"{noxb} pages missing the x-brand meta")
    if tiny:        fails.append(f"{tiny} pages truncated or empty")
    if notclosed:   fails.append(f"{notclosed} pages do not end </html>")
    if not strip:   fails.append("no page carries the TEES VALLEY strip")
    if hud:         fails.append(f"{hud} pages still reference hud.js")

    js = inline_js_check(pack) + js_asset_check(pack)
    fails += js

    ALLOWED = {".html", ".js", ".css", ".txt"}
    strays = [str(p.relative_to(pack)) for p in pack.rglob("*")
              if p.is_file() and p.suffix.lower() not in ALLOWED]
    if strays: fails.append(f"unexpected file types: {strays[:5]}")

    visible = sum(1 for p in html_files
                  if 'alt="Progress Schools"' in p.read_text(encoding="utf-8", errors="ignore"))
    meta_only = n_html - visible

    # expected-lesson arithmetic: 79 ASDAN (31+18+30) + 6 D&T, walked not typed
    def lessons_in(sub):
        return sum(1 for p in (pack / TOP / sub).rglob("*.html")
                   if re.search(r"_W\d", p.name) and p.parent.name != "DT")
    got_b, got_g, got_l = lessons_in("Build"), lessons_in("Grow"), lessons_in("Launch")
    got_dt = sum(1 for p in (pack / TOP / "Build" / "DT").glob("BUILD_DT_W*.html"))
    if (got_b, got_g, got_l, got_dt) != (31, 18, 30, 6):
        fails.append(f"lesson arithmetic: Build {got_b}/31, Grow {got_g}/18, "
                     f"Launch {got_l}/30, DT {got_dt}/6")

    print("\n" + "-" * 70)
    print(f"pages              : {n_html}")
    print(f"files in tree      : {total_files}")
    print(f"lessons            : {got_b}+{got_g}+{got_l} ASDAN + {got_dt} D&T")
    print(f"residue on/off     : {on} / {off}  (expect 0 / {n_html})")
    print(f"matt-mark by content: {len(mark_fails)}  (expect 0)")
    print(f"week census        : {len(week_fails)} mismatches; correct pairings {good6}+{good7}")
    print(f"witnessed lessons  : {witnessed} / 79")
    print(f"unit codes         : {code_census}")
    print(f"crawl              : {sum(len(v) for v in broken.values())} broken; "
          f"external whitelist used {external_used}")
    print(f"inline+asset JS    : {len(js)} syntax errors")
    print(f"logo               : {visible} visible / {meta_only} meta+credit only")
    print("-" * 70)
    for f in fails[:30]:
        print("  FAIL:", f)
    if not fails:
        print("  ALL CHECKS PASS")
    assert not fails, f"{len(fails)} checks failed - refusing to package"

    # ---------------------------------------------------------- package
    zpath = out / "Progress_Schools_ASDAN_PEQ_Mirror.zip"
    n = 0
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(pack.rglob("*")):
            if f.is_file():
                z.write(f, str(f.relative_to(pack)))
                n += 1
    assert n == total_files, f"zip has {n} entries, manifest says {total_files}"
    with zipfile.ZipFile(zpath) as z:
        assert z.testzip() is None, "unzip -t equivalent FAILED"
        top_entries = {e.split("/")[0] for e in z.namelist()}
        assert top_entries == {TOP}, f"zip roots {top_entries} != {{{TOP!r}}}"
    print(f"\nPACKAGED {zpath.name}: {n} entries, {zpath.stat().st_size/1024/1024:.2f} MB")

    report = {
        "head": head, "pages": n_html, "files": n,
        "lessons": {"Build": got_b, "Grow": got_g, "Launch": got_l, "DT": got_dt},
        "logo_visible": visible, "logo_meta_only": meta_only,
        "residue_on": on, "residue_off": off,
        "week_census": {"mismatches": len(week_fails), "good_w6": good6, "good_w7": good7},
        "unit_codes": code_census, "witnessed": witnessed,
        "rewrites": rewrites, "external_rewrites": ext_rewrites,
        "external_used": external_used, "unmapped": unmapped,
        "by_folder": dict(counts), "excluded": len(dropped),
    }
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["by_folder"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
