#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
ROLLBACK = "1e8a428b523d1b970a8a3a2ab2a99f48a8271d09"
TODAY = "2026-08-10"
GROW_SRC = Path(os.environ.get("GLV3_GROW_SRC", "/tmp/glv3-packs/grow"))
LAUNCH_SRC = Path(os.environ.get("GLV3_LAUNCH_SRC", "/tmp/glv3-packs/launch"))

LIVE_RED = (
    "Art_Teesside/",
    "GROW_ASDAN/",
    "LAUNCH_ASDAN/",
    "Grow/Slideshows/",
    "Launch/Slideshows/",
    "Science_Teesside/",
    "Humanities_Teesside/",
    "Baseline_Weeks/",
    "BUILD_Estate_v3/",
)

CHIPS = {
    ("GROW", "art"): "Art · Teesside Studio Suite",
    ("GROW", "asdan"): "GROW Vocational & PfA",
    ("GROW", "humanities"): "Humanities",
    ("LAUNCH", "art"): "Art · Teesside Studio Suite",
    ("LAUNCH", "asdan"): "LAUNCH Vocational & PfA",
    ("LAUNCH", "humanities"): "Humanities",
}
FAMILIES = {
    "GROW": "GROW Estate v3",
    "LAUNCH": "LAUNCH Estate v3",
}

LAUNCH_HUM_LIVE = [
    "Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html",
    "Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html",
    "Launch/Slideshows/LAUNCH_HUM_W3_Archive_NOP.html",
    "Launch/Slideshows/LAUNCH_HUM_W4_Century_Of_Change.html",
    "Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html",
    "Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html",
    "Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html",
    "Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html",
]

PEQ_CODES = (
    "ComSk1", "ComSkE3", "TmWkSk1", "ThSk1", "WellbLe1",
    "DecMkSk1", "LSk1",
)
CLOSURE_SENTINEL = "What I said, and what it changed"
LOOP_SENTINEL = "ll-g:loop-mark"

class GateError(RuntimeError):
    pass

def require(ok: bool, msg: str) -> None:
    if not ok:
        raise GateError(msg)

def sh(*args: str, check=True, text=True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=ROOT, check=check, text=text,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def git_show(path: str, ref: str = ROLLBACK) -> str:
    p = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(p.returncode == 0, f"cannot read {path} at {ref}: {p.stderr.strip()}")
    return p.stdout

def git_exists(path: str, ref: str = ROLLBACK) -> bool:
    return subprocess.run(["git", "cat-file", "-e", f"{ref}:{path}"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def rel_repo(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def html_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.html") if p.is_file())

def lesson_name(p: Path) -> bool:
    return "_OUTSTANDING_V3_TEST.html" in p.name

def positive_scanner_selftest() -> None:
    sample = """<form action="https://example.invalid"><script>
    localStorage.setItem('x','y'); fetch('https://example.invalid');
    eval('1+1');</script> mark scheme AO2 8 marks minimum of 10 hours
    ll-g:loop-mark What I said, and what it changed
    """
    tests = {
        "storage": r"\b(?:localStorage|sessionStorage|indexedDB|document\.cookie)\b",
        "network": r"\b(?:fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket\s*\()",
        "form": r"<form\b",
        "eval": r"\beval\s*\(",
        "external": r"https?://",
        "launch-red": r"(?i)(?:mark\s*scheme|AO\d|\b\d+\s+marks?\b)",
        "hours": r"(?i)(?:at\s+least\s+\d+\s+hours?|minimum\s+of\s+\d+\s+hours?|\d+\s+GLH|TQT)",
        "loop-sentinel": re.escape(LOOP_SENTINEL),
        "closure-sentinel": re.escape(CLOSURE_SENTINEL),
    }
    for name, pat in tests.items():
        require(re.search(pat, sample), f"known-positive scanner self-test failed: {name}")

def validate_pack(src: Path, pathway: str) -> dict:
    require(src.is_dir(), f"missing extracted repaired pack: {src}")
    require(not (src / "Science").exists(), f"{pathway} input unexpectedly contains Science/")
    all_html = html_files(src)
    lessons = [p for p in all_html if lesson_name(p)]
    expected = 34 if pathway == "GROW" else 46
    require(len(lessons) == expected, f"{pathway}: expected {expected} deployable lessons, got {len(lessons)}")
    audit = src / (f"{pathway}_COMPLETION_AUDIT.md")
    require(audit.exists(), f"{pathway}: completion audit missing")
    audit_text = audit.read_text("utf-8")
    require("Post-verification edits applied 2026-08-10" in audit_text,
            f"{pathway}: repaired audit marker missing")

    print_lessons = []
    afterprint = []
    priv = collections.Counter()
    external = []
    for p in lessons:
        t = p.read_text("utf-8")
        if "@media print" in t and ".proute" in t and "printTier" in t:
            print_lessons.append(p)
            if "afterprint" in t:
                afterprint.append(p)
        for k, pat in (
            ("storage", r"\b(?:localStorage|sessionStorage|indexedDB|document\.cookie)\b"),
            ("network", r"\b(?:fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket\s*\()"),
            ("form", r"<form\b"),
            ("eval", r"\beval\s*\("),
        ):
            priv[k] += len(re.findall(pat, t, re.I))
        external += [(p, m.group(0)) for m in re.finditer(r"https?://", t)]
    want_print = 16 if pathway == "GROW" else 8
    require(len(print_lessons) == want_print,
            f"{pathway}: repaired print-tier count expected {want_print}, got {len(print_lessons)}")
    require(len(afterprint) == want_print,
            f"{pathway}: afterprint fix expected in {want_print}, got {len(afterprint)}")
    require(sum(priv.values()) == 0, f"{pathway}: privacy primitives in deployable lessons: {dict(priv)}")
    require(not external, f"{pathway}: external URL in deployable lessons: {external[:2]}")
    return {
        "html": all_html,
        "lessons": lessons,
        "print_lessons": print_lessons,
        "audit": audit,
    }

def load_manifests(src: Path, pathway: str) -> list[dict]:
    out = []
    for p in sorted(src.rglob("manifest-v3.json")):
        data = json.loads(p.read_text("utf-8"))
        if isinstance(data, dict):
            entries = data.get("lessons") or data.get("items") or data.get("files") or []
        else:
            entries = data
        parent = p.parent.relative_to(src).as_posix()
        subject = "art" if parent == "Art_Teesside" else ("humanities" if parent == "Humanities_Teesside" else "asdan")
        for item in entries:
            rec = dict(item)
            rec["_manifest"] = rel_repo(p) if p.is_relative_to(ROOT) else p.as_posix()
            rec["_pack_parent"] = parent
            rec["_subject"] = subject
            rec["_pathway"] = pathway
            out.append(rec)
    return out

def item_file(item: dict) -> str:
    for key in ("file", "filename", "output", "html", "path"):
        v = item.get(key)
        if isinstance(v, str) and v.endswith(".html"):
            return v
    raise GateError(f"manifest item has no HTML filename: {item}")

def item_title(item: dict) -> str:
    for key in ("title", "name", "lesson"):
        v = item.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return Path(item_file(item)).stem

def item_source(item: dict) -> str | None:
    for key in ("source", "source_file", "live", "live_file", "sourcePath"):
        v = item.get(key)
        if isinstance(v, str) and v.endswith(".html"):
            return v.lstrip("./")
    return None

def make_pack_mapping(src: Path, estate: str, pathway: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for p in sorted(x for x in src.rglob("*") if x.is_file()):
        old = p.relative_to(src).as_posix()
        if p.suffix.lower() == ".md":
            new = f"_glv3/{pathway.lower()}/{old}"
        elif p.suffix.lower() == ".html" and p.parent == src and p.name.startswith("START_HERE_"):
            new = f"{estate}/index.html"
        elif p.suffix.lower() == ".html" and p.name.startswith("START_HERE_"):
            new = f"{estate}/{p.parent.relative_to(src).as_posix()}/index.html"
        else:
            new_name = p.name.replace("_OUTSTANDING_V3_TEST", "")
            parent = p.parent.relative_to(src).as_posix()
            new = f"{estate}/{parent}/{new_name}" if parent != "." else f"{estate}/{new_name}"
        mapping[old] = new
    return mapping

def copy_pack(src: Path, estate: str, pathway: str, mapping: dict[str, str]) -> None:
    for old, new in mapping.items():
        s = src / old
        d = ROOT / new
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)

def split_href(raw: str) -> tuple[str, str]:
    m = re.match(r"^([^?#]*)(.*)$", raw, re.S)
    return (m.group(1), m.group(2)) if m else (raw, "")

def rewrite_links(src: Path, pathway: str, estate: str, mapping: dict[str, str]) -> None:
    for old, new in mapping.items():
        if not new.endswith(".html"):
            continue
        p = ROOT / new
        text = p.read_text("utf-8")
        old_parent = posixpath.dirname(old)
        new_parent = posixpath.dirname(new)

        def repl(m: re.Match) -> str:
            q, quote, raw = m.group(1), m.group(2), m.group(3)
            base, suffix = split_href(raw)
            if not base or base.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                return m.group(0)
            if re.match(r"^[a-z]+://", base, re.I):
                return m.group(0)
            if old == ("START_HERE_GROW_ESTATE_OUTSTANDING_V3.html" if pathway == "GROW"
                       else "START_HERE_LAUNCH_ESTATE_OUTSTANDING_V3.html") and base.startswith("Science/"):
                target = f"Science_Teesside/{'Grow' if pathway == 'GROW' else 'Launch'}/v3_40min/"
                new_href = posixpath.relpath(target, new_parent or ".")
                if not new_href.endswith("/"):
                    new_href += "/"
                return f"{q}{quote}{new_href}{suffix}{quote}"
            old_target = posixpath.normpath(posixpath.join(old_parent, base))
            if old_target in mapping:
                target = mapping[old_target]
                new_href = posixpath.relpath(target, new_parent or ".")
                return f"{q}{quote}{new_href}{suffix}{quote}"
            clean = base.replace("_OUTSTANDING_V3_TEST", "")
            return f"{q}{quote}{clean}{suffix}{quote}"

        text = re.sub(r"(\bhref\s*=\s*)([\"'])(.*?)\2", repl, text, flags=re.I | re.S)
        p.write_text(text, "utf-8")

def hub_banner(path: Path, pathway: str, screen_only: bool = False) -> None:
    text = path.read_text("utf-8")
    line = (f'<div class="note"><b>Route status:</b> Alternative {pathway} route, Autumn 1 2026–27. '
            'The existing lessons remain available in the Lessons catalogue.</div>')
    if "The existing lessons remain available in the Lessons catalogue." not in text:
        text = text.replace("</header>", "</header>" + line, 1)
    if screen_only and "This route is screen-only." not in text:
        screen = ('<div class="note"><b>Print and evidence:</b> This route is screen-only. '
                  'Printable pupil work, portfolio evidence and ASDAN assessment records come from the existing lessons.</div>')
        text = text.replace(line, line + screen, 1)
    text = text.replace("TEST ESTATE", "ALTERNATIVE ESTATE").replace("TEST BUNDLE", "ALTERNATIVE ROUTE")
    if path.name == "index.html" and path.parent.name in ("GROW_Estate_v3", "LAUNCH_Estate_v3"):
        if pathway == "GROW":
            text = text.replace("<b>44 lesson HTML files</b> across Science, Bronze Art, Humanities and the exact 18-deck GROW ASDAN estate.",
                                "<b>34 alternative lesson HTML files</b> across Bronze Art, Humanities and the exact 18-deck GROW ASDAN estate. Science remains on the installed v3_40min route and is linked below.")
            text = re.sub(r"<p><b>Science:</b>.*?</p>",
                          "<p><b>Science:</b> the already-installed GROW v3_40min route remains authoritative and is linked here; no Science files are duplicated in this estate.</p>",
                          text, count=1, flags=re.S)
        else:
            text = text.replace("<b>61 lesson HTML files</b> across GCSE Biology, Silver Art, GCSE-bridge Humanities and the exact 30-deck LAUNCH ASDAN estate.",
                                "<b>46 alternative lesson HTML files</b> across Silver Art, GCSE-bridge Humanities and the exact 30-deck LAUNCH ASDAN estate. Science remains on the installed v3_40min route and is linked below.")
            text = re.sub(r"<p><b>Science:</b>.*?</p>",
                          "<p><b>Science:</b> the already-installed LAUNCH v3_40min route remains authoritative and is linked here; no Science files are duplicated in this estate.</p>",
                          text, count=1, flags=re.S)
    path.write_text(text, "utf-8")

def update_hubs() -> None:
    hubs = [
        (ROOT/"GROW_Estate_v3/index.html", "GROW", False),
        (ROOT/"GROW_Estate_v3/Art_Teesside/index.html", "GROW", False),
        (ROOT/"GROW_Estate_v3/GROW_ASDAN/index.html", "GROW", True),
        (ROOT/"GROW_Estate_v3/Humanities_Teesside/index.html", "GROW", False),
        (ROOT/"LAUNCH_Estate_v3/index.html", "LAUNCH", False),
        (ROOT/"LAUNCH_Estate_v3/Art_Teesside/index.html", "LAUNCH", True),
        (ROOT/"LAUNCH_Estate_v3/LAUNCH_ASDAN/index.html", "LAUNCH", True),
        (ROOT/"LAUNCH_Estate_v3/Humanities_Teesside/index.html", "LAUNCH", False),
    ]
    for p, pathway, screen in hubs:
        require(p.exists(), f"missing route hub after install: {rel_repo(p)}")
        hub_banner(p, pathway, screen)

def resolve_internal_hrefs() -> list[str]:
    bad = []
    roots = [ROOT/"GROW_Estate_v3", ROOT/"LAUNCH_Estate_v3"]
    for base_root in roots:
        for p in html_files(base_root):
            soup = BeautifulSoup(p.read_text("utf-8"), "html.parser")
            for a in soup.find_all(href=True):
                href = str(a["href"])
                path, _ = split_href(href)
                if not path or path.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                    continue
                if re.match(r"^[a-z]+://", path, re.I):
                    bad.append(f"{rel_repo(p)} external href {href}")
                    continue
                if path.startswith("/"):
                    target = ROOT / path.lstrip("/")
                else:
                    target = (p.parent / path).resolve()
                try:
                    target.relative_to(ROOT.resolve())
                except ValueError:
                    bad.append(f"{rel_repo(p)} href escapes repo: {href}")
                    continue
                if path.endswith("/"):
                    target = target / "index.html"
                if not target.exists():
                    bad.append(f"{rel_repo(p)} -> {href} (missing {target.relative_to(ROOT)})")
    return bad

def derive_lessons(src: Path, pathway: str, estate: str) -> list[dict]:
    items = load_manifests(src, pathway)
    expected = 34 if pathway == "GROW" else 46
    require(len(items) == expected, f"{pathway}: manifests enumerate {len(items)}, expected {expected}")
    recs = []
    launch_hum_i = 0
    for item in items:
        old_file = item_file(item)
        pack_rel = posixpath.normpath(posixpath.join(item["_pack_parent"], old_file))
        pack_path = src / pack_rel
        require(pack_path.exists(), f"{pathway}: manifest target missing: {pack_rel}")
        new_rel = f"{estate}/{item['_pack_parent']}/{Path(old_file).name.replace('_OUTSTANDING_V3_TEST','')}"
        subject = item["_subject"]
        source = item_source(item)
        if source:
            source = source.replace("\\", "/").lstrip("./")
        elif pathway == "LAUNCH" and subject == "humanities":
            require(launch_hum_i < 8, "LAUNCH Humanities source mapping overflow")
            source = LAUNCH_HUM_LIVE[launch_hum_i]
            launch_hum_i += 1
        require(source and git_exists(source), f"{pathway}: live counterpart missing/unknown for {pack_rel}: {source}")
        stem = Path(new_rel).stem
        week_m = re.search(r"_W(\d+)", stem)
        week = int(week_m.group(1)) if week_m else None
        title = item_title(item)
        strand = None
        if subject == "asdan":
            strand = stem.split("_W", 1)[0]
            strand = {
                "PEQ": "PEQ", "COMM": "Community", "ENT": "Enterprise",
                "CAREERS": "Careers", "LI": "Living Independently", "VOC": "Vocational"
            }.get(strand, strand)
        pack_text = pack_path.read_text("utf-8")
        has_print = "@media print" in pack_text and ".proute" in pack_text and "printTier" in pack_text
        recs.append({
            "pathway": pathway,
            "subject_key": subject,
            "chip": CHIPS[(pathway, subject)],
            "pack_rel": pack_rel,
            "file": new_rel,
            "live": source,
            "week": week,
            "strand": strand,
            "title": title,
            "print": has_print,
        })
    return recs

def clean_title(raw: str) -> str:
    s = BeautifulSoup(raw, "html.parser").get_text(" ", strip=True)
    s = re.sub(r"\s+", " ", s)
    return s

def catalogue_title(r: dict) -> str:
    p, sub, week = r["pathway"], r["subject_key"], r["week"]
    title = clean_title(r["title"])
    if sub == "art":
        label = "Silver Art" if p == "LAUNCH" else "Art"
        return f"{p} · {label} · W{week} · {title} (v3 route)"
    if sub == "humanities":
        return f"{p} · Humanities · W{week} · {title} (v3 route)"
    return f"{p} · ASDAN · {r['strand']} W{week} · {title} (v3 route)"

def slug(*parts: object) -> str:
    s = "-".join(str(x).lower() for x in parts if x is not None)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def update_resources(recs: list[dict]) -> dict:
    p = ROOT/"resources.json"
    base = json.loads(git_show("resources.json"))
    require(isinstance(base, list), "resources.json is not an array")
    base_count = len(base)
    base_ids = [x.get("id") for x in base]
    require(len(base_ids) == len(set(base_ids)), "base resources.json already has duplicate id")

    resources = json.loads(p.read_text("utf-8"))
    require(len(resources) == base_count, "working resources.json does not match rollback count before union")
    humanities_fixed = []
    for item in resources:
        if str(item.get("file", "")).startswith("Humanities_Teesside/") and item.get("year") == "2025-26":
            item["year"] = "2026-27"
            humanities_fixed.append(item.get("id"))

    new_entries = []
    for r in recs:
        rid = "glv3-" + slug(r["pathway"], r["subject_key"], r["strand"], f"w{r['week']}")
        desc = f"Alternative {r['pathway']} Autumn 1 {r['subject_key']} lesson; existing lessons remain the default route."
        new_entries.append({
            "id": rid,
            "title": catalogue_title(r),
            "subject": r["chip"],
            "type": "Lesson",
            "file": r["file"],
            "description": desc,
            "added": TODAY,
            "new": True,
            "thumbnail": "",
            "year": "2026-27",
            "family": FAMILIES[r["pathway"]],
        })

    hub_specs = [
        ("GROW", "estate", "GROW Vocational & PfA", "GROW_Estate_v3/index.html", "GROW · Autumn 1 alternative v3 estate"),
        ("GROW", "art", "Art · Teesside Studio Suite", "GROW_Estate_v3/Art_Teesside/index.html", "GROW · Art · alternative v3 route hub"),
        ("GROW", "asdan", "GROW Vocational & PfA", "GROW_Estate_v3/GROW_ASDAN/index.html", "GROW · ASDAN · alternative v3 route hub"),
        ("GROW", "humanities", "Humanities", "GROW_Estate_v3/Humanities_Teesside/index.html", "GROW · Humanities · alternative v3 route hub"),
        ("LAUNCH", "estate", "LAUNCH Vocational & PfA", "LAUNCH_Estate_v3/index.html", "LAUNCH · Autumn 1 alternative v3 estate"),
        ("LAUNCH", "art", "Art · Teesside Studio Suite", "LAUNCH_Estate_v3/Art_Teesside/index.html", "LAUNCH · Silver Art · alternative v3 route hub"),
        ("LAUNCH", "asdan", "LAUNCH Vocational & PfA", "LAUNCH_Estate_v3/LAUNCH_ASDAN/index.html", "LAUNCH · ASDAN · alternative v3 route hub"),
        ("LAUNCH", "humanities", "Humanities", "LAUNCH_Estate_v3/Humanities_Teesside/index.html", "LAUNCH · Humanities · alternative v3 route hub"),
    ]
    for pathway, key, chip, file, title in hub_specs:
        new_entries.append({
            "id": "glv3-" + slug(pathway, key, "hub"),
            "title": title,
            "subject": chip,
            "type": "Hub",
            "file": file,
            "description": f"Alternative {pathway} Autumn 1 route hub. Existing lessons remain available and default.",
            "added": TODAY,
            "new": True,
            "thumbnail": "",
            "year": "2026-27",
            "family": FAMILIES[pathway],
        })

    require(len(new_entries) == 88, f"catalogue new-entry count expected 88, got {len(new_entries)}")
    ids = [x["id"] for x in new_entries]
    require(len(ids) == len(set(ids)), "duplicate new catalogue IDs")
    require(not (set(ids) & set(base_ids)), f"new catalogue ID collides with base: {set(ids)&set(base_ids)}")

    resources.extend(new_entries)
    all_ids = [x.get("id") for x in resources]
    require(len(all_ids) == len(set(all_ids)), "resources.json union has duplicate IDs")
    require(len(resources) == base_count + len(new_entries),
            f"resources count {len(resources)} != base {base_count} + {len(new_entries)}")

    by_id = {x.get("id"): x for x in resources}
    for old in base:
        now = by_id.get(old.get("id"))
        require(now is not None, f"pre-existing resource disappeared: {old.get('id')}")
        a, b = dict(old), dict(now)
        if old.get("id") in humanities_fixed:
            a["year"] = "2026-27"
        require(a == b, f"pre-existing resource changed unexpectedly: {old.get('id')}")

    p.write_text(json.dumps(resources, ensure_ascii=False, indent=2) + "\n", "utf-8")

    chip_expected = {}
    for chip in sorted(set(CHIPS.values())):
        chip_expected[chip] = sum(1 for x in resources if x.get("subject") == chip and x.get("year") == "2026-27")
    (ROOT/"_glv3/chip_expected.json").write_text(json.dumps(chip_expected, ensure_ascii=False, indent=2)+"\n", "utf-8")
    return {
        "base_count": base_count,
        "new_count": len(new_entries),
        "final_count": len(resources),
        "humanities_year_fixed": humanities_fixed,
        "chip_expected": chip_expected,
    }

def update_routes() -> None:
    path = ROOT/"_finish/ROUTES.md"
    text = path.read_text("utf-8")
    require("GROW_Estate_v3/" not in text and "LAUNCH_Estate_v3/" not in text,
            "_finish/ROUTES.md already contains this run")
    rows = [
        "| Art · GROW | `Art_Teesside/Grow/` — 8 lessons, W1–W8 | `GROW_Estate_v3/Art_Teesside/` — 8 lessons, alternative Autumn 1 route |",
        "| Art · LAUNCH | `Art_Teesside/Launch/` — 8 lessons, W1–W8 | `LAUNCH_Estate_v3/Art_Teesside/` — 8 lessons, alternative Autumn 1 route; screen-only — live remains the printable Silver portfolio route |",
        "| ASDAN · GROW | `GROW_ASDAN/` — 18 taught lessons across PEQ / Community / Enterprise | `GROW_Estate_v3/GROW_ASDAN/` — 18 lessons, alternative Autumn 1 route; screen-only — live supplies printable PEQ records |",
        "| ASDAN · LAUNCH | `LAUNCH_ASDAN/` — 30 taught lessons across 5 slots | `LAUNCH_Estate_v3/LAUNCH_ASDAN/` — 30 lessons, alternative Autumn 1 route; screen-only — live supplies printable PEQ records |",
        "| Humanities · GROW | `Grow/Slideshows/` — 8 lessons, W1–W8 | `GROW_Estate_v3/Humanities_Teesside/` — 8 lessons, alternative Autumn 1 route |",
        "| Humanities · LAUNCH | `Launch/Slideshows/` — 8 lessons, W1–W8 | `LAUNCH_Estate_v3/Humanities_Teesside/` — 8 lessons, alternative Autumn 1 route |",
    ]
    marker = "| Baseline (W1–W2) |"
    idx = text.find(marker)
    require(idx >= 0, "ROUTES.md table marker not found")
    line_end = text.find("\n", idx)
    require(line_end >= 0, "ROUTES.md baseline row terminator not found")
    text = text[:line_end+1] + "\n".join(rows) + "\n" + text[line_end+1:]
    insert = """
## GROW + LAUNCH v3 additions

The six rows above extend this file rather than creating a rival map. GROW/LAUNCH live suites stay
the default. The alternative ASDAN routes are screen-only; printable pupil work and PEQ assessment
records remain in the live suites. LAUNCH alternative Art is also screen-only; the live Silver Art
suite remains the printable portfolio route.
"""
    text = text.replace("\n## How to tell them apart in the catalogue", insert + "\n## How to tell them apart in the catalogue", 1)
    path.write_text(text, "utf-8")

def red_tree_blob_manifest(ref: str) -> dict[str, list[str]]:
    out = {}
    for prefix in LIVE_RED:
        p = sh("git", "ls-tree", "-r", ref, "--", prefix).stdout.strip().splitlines()
        out[prefix] = p
    return out

def verify_live_invariance() -> dict:
    before_manifest = red_tree_blob_manifest(ROLLBACK)
    after_manifest = {}
    for prefix in LIVE_RED:
        lines = []
        for p in sorted(x for x in (ROOT/prefix).rglob("*") if x.is_file()):
            rp = rel_repo(p)
            blob = sh("git", "hash-object", rp).stdout.strip()
            lines.append(f"{blob}\t{rp}")
        after_manifest[prefix] = lines
        before_pairs = []
        for line in before_manifest[prefix]:
            m = re.match(r"\d+\s+blob\s+([0-9a-f]+)\t(.+)$", line)
            if m:
                before_pairs.append(f"{m.group(1)}\t{m.group(2)}")
        require(before_pairs == lines, f"LIVE INVARIANCE FAILED under {prefix}")
    digests = {k: hashlib.sha256(("\n".join(v)+"\n").encode()).hexdigest()
               for k, v in after_manifest.items()}
    return {"blob_hashes": digests}

def repo_sentinel_set(needle: str, ref: str | None = None) -> list[str]:
    if ref:
        p = subprocess.run(["git", "grep", "-l", "-F", needle, ref, "--", "*.html"], cwd=ROOT,
                           text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode not in (0, 1):
            raise GateError(f"git grep sentinel failed: {p.stderr.strip()}")
        paths = []
        for line in p.stdout.splitlines():
            paths.append(line.split(":", 1)[1] if ":" in line else line)
        return sorted(set(paths))
    paths = []
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        try:
            t = p.read_text("utf-8")
        except UnicodeDecodeError:
            continue
        if needle in t:
            paths.append(rel_repo(p))
    return sorted(set(paths))

def sentinel_report(pack_roots: list[Path]) -> dict:
    expected = {}
    for needle in (LOOP_SENTINEL, CLOSURE_SENTINEL):
        pack_hits = []
        for pr in pack_roots:
            for p in html_files(pr):
                if needle in p.read_text("utf-8"):
                    pack_hits.append(p)
        expected[needle] = len(pack_hits)
    before = {n: repo_sentinel_set(n, ROLLBACK) for n in (LOOP_SENTINEL, CLOSURE_SENTINEL)}
    after = {n: repo_sentinel_set(n, None) for n in (LOOP_SENTINEL, CLOSURE_SENTINEL)}
    for n in before:
        delta = sorted(set(after[n]) - set(before[n]))
        removed = sorted(set(before[n]) - set(after[n]))
        require(not removed, f"sentinel files removed for {n}: {removed[:5]}")
        require(len(delta) == expected[n],
                f"sentinel delta for {n}: expected {expected[n]} pack-bearing new files, got {len(delta)}")
    return {"expected_delta": expected, "before": before, "after": after}

def privacy_scan(paths: list[Path]) -> dict:
    pats = {
        "storage": r"\b(?:localStorage|sessionStorage|indexedDB|document\.cookie)\b",
        "network": r"\b(?:fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket\s*\()",
        "form": r"<form\b",
        "eval": r"\beval\s*\(",
        "external": r"https?://",
    }
    hits = {k: [] for k in pats}
    for p in paths:
        t = p.read_text("utf-8")
        for k, pat in pats.items():
            if re.search(pat, t, re.I):
                hits[k].append(rel_repo(p))
    require(all(not v for v in hits.values()), f"privacy gate hits: { {k:v[:3] for k,v in hits.items() if v} }")
    return {k: len(v) for k, v in hits.items()}

def inline_node_check(paths: list[Path]) -> dict:
    blocks = 0
    failures = []
    tmp = ROOT/"_glv3/.inline-check.js"
    for p in paths:
        soup = BeautifulSoup(p.read_text("utf-8"), "html.parser")
        for i, s in enumerate(soup.find_all("script")):
            if s.get("src"):
                continue
            code = s.string if s.string is not None else s.get_text()
            if not code.strip():
                continue
            blocks += 1
            tmp.write_text(code, "utf-8")
            proc = subprocess.run(["node", "--check", str(tmp)], cwd=ROOT, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if proc.returncode:
                failures.append(f"{rel_repo(p)} script#{i+1}: {proc.stdout.strip()}")
    tmp.unlink(missing_ok=True)
    require(not failures, "node --check failures:\n" + "\n".join(failures[:8]))
    return {"files": len(paths), "blocks": blocks, "failures": 0}

def print_static_gate(recs: list[dict]) -> dict:
    bearing = [r for r in recs if r["print"]]
    screen = [r for r in recs if not r["print"]]
    require(len(bearing) == 24, f"print-bearing expected 24, got {len(bearing)}")
    require(len(screen) == 56, f"screen-only expected 56, got {len(screen)}")
    group_counts = collections.Counter((r["pathway"], r["subject_key"]) for r in screen)
    require(group_counts == collections.Counter({("GROW","asdan"):18, ("LAUNCH","asdan"):30, ("LAUNCH","art"):8}),
            f"screen-only groups unexpected: {dict(group_counts)}")
    for r in bearing:
        t = (ROOT/r["file"]).read_text("utf-8")
        require("body[data-tier] .proute" in t, f"print default repair missing {r['file']}")
        require("afterprint" in t, f"afterprint repair missing {r['file']}")
        require(len(re.findall(r'class=["\'][^"\']*\bproute\b', t)) == 3,
                f"expected 3 .proute blocks in {r['file']}")
    for r in screen:
        t = (ROOT/r["file"]).read_text("utf-8")
        require("@media print" not in t and ".proute" not in t and "printTier" not in t,
                f"screen-only file unexpectedly acquired print surface: {r['file']}")
    return {
        "bearing": len(bearing),
        "screen_only": len(screen),
        "screen_groups": {f"{k[0]} {k[1]}": v for k,v in sorted(group_counts.items())},
    }

def arts_report(recs: list[dict]) -> dict:
    art = [r for r in recs if r["subject_key"] == "art"]
    require(len(art) == 16, "Arts gate universe is not 16 lessons")
    threshold_hits = []
    new_form = []
    artefacts = {}
    for r in art:
        t = (ROOT/r["file"]).read_text("utf-8")
        plain = BeautifulSoup(t, "html.parser").get_text(" ", strip=True)
        for m in re.finditer(r"(?i)(?:at\s+least\s+\d+\s+hours?|minimum\s+of\s+\d+\s+hours?|\b\d+\s+GLH\b|\bTQT\b)", plain):
            context = plain[max(0,m.start()-100):m.end()+140]
            threshold_hits.append({"file": r["file"], "match": m.group(0), "context": context})
        if re.search(r"(?i)\bnew\s+art\s+form\b", plain):
            new_form.append(r["file"])

    bad_thresholds = []
    for h in threshold_hits:
        c = h["context"].lower()
        if re.search(r"at\s+least\s+\d+\s+hours?|minimum\s+of\s+\d+\s+hours?", h["match"], re.I):
            bad_thresholds.append(h)
        elif not any(x in c for x in ("guidance", "no minimum", "not a minimum", "not a threshold", "no hours threshold")):
            bad_thresholds.append(h)
    require(not bad_thresholds, f"Arts Award hours-threshold gate failed: {bad_thresholds[:3]}")
    require(not new_form, f"'new art form' claim present in v3 Art: {new_form}")

    for pathway, week in (("GROW",5), ("LAUNCH",2)):
        r = next(x for x in art if x["pathway"] == pathway and x["week"] == week)
        plain = BeautifulSoup((ROOT/r["file"]).read_text("utf-8"), "html.parser").get_text(" ", strip=True)
        org_mentions = len(re.findall(r"(?i)\borganisation\b", plain))
        artefact_terms = re.findall(r"(?i)\b(?:evidence|record|capture|locator|portfolio|card|sheet|log|artefact|artifact)\b", plain)
        local = False
        for m in re.finditer(r"(?i)\borganisation\b", plain):
            c = plain[max(0,m.start()-450):m.end()+450]
            if re.search(r"(?i)\b(?:evidence|record|capture|portfolio|card|sheet|log|artefact|artifact)\b", c):
                local = True
                break
        require(org_mentions > 0 and artefact_terms and local,
                f"{pathway} Art W{week}: organisation taught but no organisation evidence artefact confirmed")
        artefacts[f"{pathway} W{week}"] = {"organisation_mentions": org_mentions, "evidence_artefact_confirmed": True}

    grow_table = [
        ("W1","A","A"), ("W2","A+D","A"), ("W3","A","A"), ("W4","A+B","B"),
        ("W5","C","C"), ("W6","D","D"), ("W7","D","D"), ("W8","all four","all four"),
    ]
    launch_table = [
        ("W1","1A","1A"), ("W2","1D","1D"), ("W3","1B","1B"), ("W4","1C","1C"),
        ("W5","2A–B","2A–B"), ("W6","2C–D","2C–D"), ("W7","2C–D","2C–D"),
        ("W8","1A–B, 1C–D, 2A–B, 2C–D, 2E","2E"),
    ]
    return {
        "universe": len(art),
        "threshold_context_hits": threshold_hits,
        "bad_thresholds": 0,
        "new_art_form": 0,
        "organisation_evidence": artefacts,
        "grow_table": grow_table,
        "launch_table": launch_table,
    }

def peq_report(recs: list[dict]) -> dict:
    asdan = [r for r in recs if r["subject_key"] == "asdan"]
    require(len(asdan) == 48, f"ASDAN universe expected 48 v3 lessons, got {len(asdan)}")
    tables = {"GROW": [], "LAUNCH": []}
    v3_code_hits = []
    banned = []
    comm10 = []
    l2reg = []
    for r in asdan:
        v3 = BeautifulSoup((ROOT/r["file"]).read_text("utf-8"), "html.parser").get_text(" ", strip=True)
        live = BeautifulSoup(git_show(r["live"]), "html.parser").get_text(" ", strip=True)
        vcodes = sorted({c for c in PEQ_CODES if re.search(rf"\b{re.escape(c)}\b", v3)})
        lcodes = sorted({c for c in PEQ_CODES if re.search(rf"\b{re.escape(c)}\b", live)})
        if vcodes:
            v3_code_hits.append({"file": r["file"], "codes": vcodes})
        tables[r["pathway"]].append({
            "v3": r["file"], "live": r["live"], "live_codes": lcodes, "v3_codes": vcodes
        })
        for phrase in ("Delivering a Project",):
            if phrase.lower() in v3.lower():
                banned.append((r["file"], phrase))
        if re.search(r"(?i)(?:unit|PEQ\s+unit)\s*[:·\-–—]?\s*(?:Working with Others|Problem Solving)", v3):
            banned.append((r["file"], "legacy phrase used as unit name"))
        if re.search(r"(?i)Communication.{0,120}\b10\s*hours?\b|\b10\s*hours?\b.{0,120}Communication", v3):
            comm10.append(r["file"])
        if re.search(r"(?is)(?:register(?:ed|ing|ation)?).{0,100}(?:\bL2\b|Level\s*2)|(?:\bL2\b|Level\s*2).{0,100}(?:register(?:ed|ing|ation)?)", v3):
            l2reg.append(r["file"])
    require(not v3_code_hits, f"v3 deployable ASDAN lesson unexpectedly names PEQ code(s): {v3_code_hits[:3]}")
    require(not banned, f"banned PEQ unit labels: {banned[:3]}")
    require(not comm10, f"10-hour Communication assertion: {comm10}")
    require(not l2reg, f"L2 registration claim in lesson file: {l2reg}")
    hub_code_hits = {}
    for p in [ROOT/"GROW_Estate_v3/GROW_ASDAN/index.html", ROOT/"LAUNCH_Estate_v3/LAUNCH_ASDAN/index.html"]:
        plain = BeautifulSoup(p.read_text("utf-8"), "html.parser").get_text(" ", strip=True)
        codes = sorted({c for c in PEQ_CODES if re.search(rf"\b{re.escape(c)}\b", plain)})
        if codes:
            hub_code_hits[rel_repo(p)] = codes
    return {
        "universe": len(asdan),
        "tables": tables,
        "v3_lesson_code_hits": 0,
        "hub_code_hits": hub_code_hits,
        "banned_labels": 0,
        "communication_10h": 0,
        "l2_registration_claims": 0,
        "consequence": "Without v3 lesson-level unit codes, activity evidence cannot be reconciled to a PEQ unit criterion from this route alone; retain the live Evidence Binder/authorised mapping and do not infer missing codes.",
    }

def launch_redline(recs: list[dict]) -> dict:
    launch_paths = html_files(ROOT/"LAUNCH_Estate_v3")
    pats = [
        r"(?i)\bmark\s*scheme\b", r"(?i)\bband\s+descriptors?\b",
        r"(?i)\blevel\s+descriptors?\b", r"(?i)\bgrade\s+boundar(?:y|ies)\b",
        r"\bAO[1-9]\b", r"(?i)\bmark\s+allocations?\b", r"(?i)\b\d+\s+marks?\b",
    ]
    hits = []
    for p in launch_paths:
        plain = BeautifulSoup(p.read_text("utf-8"), "html.parser").get_text(" ", strip=True)
        for pat in pats:
            m = re.search(pat, plain)
            if m:
                hits.append((rel_repo(p), m.group(0)))
    require(not hits, f"LAUNCH red-line hit(s): {hits[:5]}")
    return {"universe_html": len(launch_paths), "hits": 0}

VOWELS = "aeiouy"
def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count = 0
    prev = False
    for ch in w:
        cur = ch in VOWELS
        if cur and not prev:
            count += 1
        prev = cur
    if w.endswith("e") and count > 1 and not w.endswith(("le","ye")):
        count -= 1
    return max(1, count)

def prose_from_html(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup.select("script,style,svg,nav,header,footer,form,button,template,noscript"):
        tag.decompose()
    selected = soup.select("main p, main li, article p, article li, .slide p, .slide li")
    if not selected:
        selected = soup.select("p, li")
    bits = []
    blocked = re.compile(r"(?i)(?:print|proute|key[-_ ]?facts?|worksheet|evidence[-_ ]?pack)")
    for el in selected:
        blocked_ancestor = False
        for anc in [el, *el.parents]:
            classes = " ".join(anc.get("class", [])) if getattr(anc, "get", None) else ""
            if blocked.search(classes):
                blocked_ancestor = True
                break
        if not blocked_ancestor:
            s = re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()
            if s:
                bits.append(s)
    return " ".join(bits)

def fk(text: str) -> dict:
    words = re.findall(r"\b[A-Za-z]+(?:['’-][A-Za-z]+)?\b", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if re.search(r"[A-Za-z]", s)]
    if not words or not sentences:
        return {"words": len(words), "sentences": len(sentences), "syllables": 0, "fk": None}
    syl = sum(syllables(w) for w in words)
    score = 0.39 * (len(words)/len(sentences)) + 11.8 * (syl/len(words)) - 15.59
    return {"words": len(words), "sentences": len(sentences), "syllables": syl, "fk": round(score, 2)}

def reading_report(recs: list[dict]) -> dict:
    groups = collections.defaultdict(list)
    for r in recs:
        groups[(r["pathway"], r["subject_key"])].append(r)
    out = {}
    for (pathway, subject), rs in sorted(groups.items()):
        v3_text = " ".join(prose_from_html((ROOT/r["file"]).read_text("utf-8")) for r in rs)
        live_text = " ".join(prose_from_html(git_show(r["live"])) for r in rs)
        v3m, livem = fk(v3_text), fk(live_text)
        delta = None if v3m["fk"] is None or livem["fk"] is None else round(v3m["fk"] - livem["fk"], 2)
        out[f"{pathway} {subject}"] = {
            "lessons": len(rs), "v3": v3m, "live": livem, "delta": delta
        }
    return {
        "selector": "BeautifulSoup: script/style/svg/nav/header/footer/form/button/template/noscript removed; select main p, main li, article p, article li, .slide p, .slide li (fallback p/li); exclude ancestors whose class matches print|proute|key-fact|worksheet|evidence-pack.",
        "instrument": "Flesch-Kincaid grade using one deterministic vowel-group syllable heuristic for both live and v3.",
        "groups": out,
    }

def write_reports(recs: list[dict], results: dict) -> None:
    g = ROOT/"_glv3"
    g.mkdir(exist_ok=True)
    (g/"run_manifest.json").write_text(json.dumps({"rollback": ROLLBACK, "lessons": recs}, ensure_ascii=False, indent=2)+"\n", "utf-8")
    (g/"GATES_STATIC.json").write_text(json.dumps(results, ensure_ascii=False, indent=2)+"\n", "utf-8")

    arts = results["arts"]
    peq = results["peq"]
    reading = results["reading"]
    sent = results["sentinels"]
    cat = results["catalogue"]

    def md_table(rows):
        return "\n".join("| " + " | ".join(map(str,row)) + " |" for row in rows)

    peq_sections = []
    for pathway in ("GROW","LAUNCH"):
        rows = [["v3 lesson","live counterpart","live unit code(s)","v3 lesson code(s)"],
                ["---","---","---","---"]]
        for x in peq["tables"][pathway]:
            rows.append([f"`{x['v3']}`", f"`{x['live']}`",
                         ", ".join(x["live_codes"]) or "—",
                         ", ".join(x["v3_codes"]) or "—"])
        peq_sections.append(f"### {pathway}\n\n{md_table(rows)}")

    read_rows = [["Pathway / subject","lessons","live prose words","live FK","v3 prose words","v3 FK","delta"],
                 ["---","---:","---:","---:","---:","---:","---:"]]
    for k,v in reading["groups"].items():
        read_rows.append([k, v["lessons"], v["live"]["words"], v["live"]["fk"],
                          v["v3"]["words"], v["v3"]["fk"], v["delta"]])

    grow_rows = [["Week","live Bronze tag","v3 Bronze tag"],["---","---","---"], *arts["grow_table"]]
    launch_rows = [["Week","live Silver tag","v3 Silver tag"],["---","---","---"], *arts["launch_table"]]

    report = f"""# GROW + LAUNCH v3 deployment verification

ROLLBACK_SHA: `{ROLLBACK}`

## Three findings first

1. **56/80 deployable lessons are screen-only**: GROW ASDAN 18, LAUNCH ASDAN 30, LAUNCH Art 8. The live ASDAN suites therefore remain the printable PEQ assessment-record route, including the witness statement and T2-4 learner-confirmation line; live LAUNCH Art remains the printable Silver portfolio route.
2. **The 48 deployable v3 ASDAN lesson files name no PEQ unit code.** {peq['consequence']}
3. **Arts Award tags are adviser decisions, not code changes.** GROW reduces W2 A+D→A and W4 A+B→B; LAUNCH reduces W8 from the whole portfolio tag set to Unit 2E alone. No tag was changed by this run.

## Pack / install counts

- GROW: 34 lessons (Art 8 · Humanities 8 · ASDAN 18)
- LAUNCH: 46 lessons (Art 8 · Humanities 8 · ASDAN 30)
- Total: 80 lessons + 2 estate hubs + 6 subject hubs = 88 new catalogue entries.
- Print-bearing: 24 lessons.
- Screen-only: 56 lessons.

## Catalogue

- Base resources universe: {cat['base_count']} entries.
- Added universe: {cat['new_count']} entries.
- Final universe: {cat['final_count']} entries.
- Conditional Humanities_Teesside year corrections applied: {len(cat['humanities_year_fixed'])} IDs.
- Expected 2026-27 chip totals: `{json.dumps(cat['chip_expected'], ensure_ascii=False)}`.

## Arts Award adviser tables

### GROW Bronze

{md_table(grow_rows)}

### LAUNCH Silver

{md_table(launch_rows)}

Organisation evidence artefacts confirmed: `{json.dumps(arts['organisation_evidence'], ensure_ascii=False)}`.

Hours-threshold gate: 0 bad thresholds across 16 v3 Art lesson files. Raw GLH/TQT/guidance contexts, if any, are preserved in `GATES_STATIC.json`.
`new art form` claims: 0.

## PEQ live-vs-v3 unit-code tables

{chr(10).join(peq_sections)}

Note: the A2 gate universe is the **48 deployable ASDAN lesson files**. The copied LAUNCH ASDAN **subject hub** already contains `ComSk1` in contextual live-mapping wording from the repaired pack; it was not added by this run. Hub code hits: `{json.dumps(peq['hub_code_hits'], ensure_ascii=False)}`.

Banned unit-label gate: 0. Communication 10-hour assertion: 0. L2 registration claim in deployable lesson files: 0.

## Sentinels

Expected delta was derived from the repaired pack bytes **before** deployment:
- `{LOOP_SENTINEL}`: {sent['expected_delta'][LOOP_SENTINEL]} new bearing files.
- `{CLOSURE_SENTINEL}`: {sent['expected_delta'][CLOSURE_SENTINEL]} new bearing files.

Rollback file-set sizes:
- loop: {len(sent['before'][LOOP_SENTINEL])}
- closure: {len(sent['before'][CLOSURE_SENTINEL])}

Working-tree file-set sizes after install:
- loop: {len(sent['after'][LOOP_SENTINEL])}
- closure: {len(sent['after'][CLOSURE_SENTINEL])}

## Reading level — prose only, report only

Selector: {reading['selector']}

Instrument: {reading['instrument']}

{md_table(read_rows)}

## Static gates

- Inline scripts: {results['node']['blocks']} blocks across {results['node']['files']} new HTML files; 0 `node --check` failures.
- Privacy across all new estate HTML: 0 storage · 0 network · 0 `<form>` · 0 `eval(` · 0 external URLs.
- LAUNCH red line: 0 hits across every installed LAUNCH HTML file (universe recorded in `GATES_STATIC.json`).
- Print static gate: 24/24 route-bearing files repaired; 56 screen-only files confirmed as an expected state.
- Internal relative hrefs: 0 unresolved.
- Live invariance: all nine protected trees byte/blob-identical to ROLLBACK_SHA. Blob-manifest digests are in `GATES_STATIC.json`.
- Root sitemap: no `sitemap.xml` exists at ROLLBACK_SHA, so this run did not invent a rival sitemap.
"""
    (g/"REPORT.md").write_text(report, "utf-8")

    ambers = [
        "A1 — 56/80 deployable lessons are screen-only; no print pack was authored.",
        "A2 — 48 deployable v3 ASDAN lessons contain no PEQ unit code; no mapping was inferred.",
        "A3 — GROW W2/W4 and LAUNCH W8 tag reductions are adviser judgements; no tag was changed.",
        "Repository — no root sitemap.xml exists at ROLLBACK_SHA; no new sitemap was invented.",
        "Spec — §9.1 says 6/6 although §0 defines seven identity checks and explicitly says 7/7.",
        "Input audits — the phrase 'Post-verification edits applied 2026-08-10' is the final section heading near the tail, not literally the final line.",
    ]
    if peq["hub_code_hits"]:
        ambers.append("A2 wording contradiction — the 48 deployable lesson files contain zero unit codes, but the repaired LAUNCH ASDAN subject hub already says ComSk1 in contextual mapping wording.")
    if sent["expected_delta"][CLOSURE_SENTINEL] == 0:
        ambers.append(f"Sentinel measurement — repaired deployable GROW/LAUNCH lessons contain 0 literal `{CLOSURE_SENTINEL}` strings, so expected closure-set delta is 0 despite the brief saying both pathways 'close on the written line'.")
    for k,v in reading["groups"].items():
        if v["delta"] is not None and v["delta"] >= 2.6:
            ambers.append(f"Reading level — {k} v3 prose is +{v['delta']} FK grades vs live using the declared prose selector, consistent with the pathway-wide load pattern seen in science.")
    (g/"AMBERS.md").write_text("# AMBER findings\n\n" + "\n".join(f"- {x}" for x in ambers) + "\n", "utf-8")

    d = g/"DECISIONS.md"
    with d.open("a", encoding="utf-8") as f:
        f.write("\n## Measured execution results\n\n")
        f.write(f"- Static gates executed against ROLLBACK_SHA `{ROLLBACK}` and the generated branch worktree.\n")
        f.write(f"- Catalogue union: base {cat['base_count']} + new {cat['new_count']} = final {cat['final_count']}.\n")
        f.write("- `_finish/ROUTES.md` extended with six GROW/LAUNCH rows; no rival route map created.\n")
        f.write("- No root `sitemap.xml` exists at rollback, so none was invented.\n")
        f.write(f"- Sentinel expected deltas derived before copy: loop {sent['expected_delta'][LOOP_SENTINEL]}, closure {sent['expected_delta'][CLOSURE_SENTINEL]}.\n")
        f.write("- All live RED trees are blob-identical to rollback after install.\n")
        f.write("- Browser boot/print/chip/contact-sheet results are appended by the browser gate before commit.\n")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rerun-live-privacy", action="store_true")
    args = parser.parse_args()

    positive_scanner_selftest()
    if args.rerun_live_privacy:
        results = {
            "live": verify_live_invariance(),
            "privacy": privacy_scan(html_files(ROOT/"GROW_Estate_v3") + html_files(ROOT/"LAUNCH_Estate_v3")),
        }
        print(json.dumps(results, indent=2))
        return 0

    require(git_exists("BUILD_Estate_v3/index.html"), "BUILD_Estate_v3 missing at rollback")
    require(git_exists("_finish/ROUTES.md"), "_finish/ROUTES.md missing at rollback")
    require(not git_exists("GROW_Estate_v3/index.html"), "prior GROW v3 estate already exists at rollback")
    require(not git_exists("LAUNCH_Estate_v3/index.html"), "prior LAUNCH v3 estate already exists at rollback")
    require(not (ROOT/"GROW_Estate_v3").exists(), "GROW_Estate_v3 exists in worktree before generator")
    require(not (ROOT/"LAUNCH_Estate_v3").exists(), "LAUNCH_Estate_v3 exists in worktree before generator")

    gpack = validate_pack(GROW_SRC, "GROW")
    lpack = validate_pack(LAUNCH_SRC, "LAUNCH")

    gmap = make_pack_mapping(GROW_SRC, "GROW_Estate_v3", "GROW")
    lmap = make_pack_mapping(LAUNCH_SRC, "LAUNCH_Estate_v3", "LAUNCH")
    copy_pack(GROW_SRC, "GROW_Estate_v3", "GROW", gmap)
    copy_pack(LAUNCH_SRC, "LAUNCH_Estate_v3", "LAUNCH", lmap)
    rewrite_links(GROW_SRC, "GROW", "GROW_Estate_v3", gmap)
    rewrite_links(LAUNCH_SRC, "LAUNCH", "LAUNCH_Estate_v3", lmap)
    update_hubs()

    require(not list((ROOT/"GROW_Estate_v3").rglob("*_OUTSTANDING_V3_TEST*")), "GROW TEST filename survived")
    require(not list((ROOT/"LAUNCH_Estate_v3").rglob("*_OUTSTANDING_V3_TEST*")), "LAUNCH TEST filename survived")
    require(not list((ROOT/"GROW_Estate_v3").rglob("*.md")), "GROW markdown record leaked into pupil-facing tree")
    require(not list((ROOT/"LAUNCH_Estate_v3").rglob("*.md")), "LAUNCH markdown record leaked into pupil-facing tree")

    bad_links = resolve_internal_hrefs()
    require(not bad_links, "unresolved internal href(s):\n" + "\n".join(bad_links[:20]))

    recs = derive_lessons(GROW_SRC, "GROW", "GROW_Estate_v3") + derive_lessons(LAUNCH_SRC, "LAUNCH", "LAUNCH_Estate_v3")
    require(len(recs) == 80, f"run manifest lessons {len(recs)} != 80")
    require(len({r["file"] for r in recs}) == 80, "duplicate installed lesson path")
    for r in recs:
        require((ROOT/r["file"]).exists(), f"installed lesson missing: {r['file']}")

    update_routes()
    cat = update_resources(recs)

    all_new_html = html_files(ROOT/"GROW_Estate_v3") + html_files(ROOT/"LAUNCH_Estate_v3")
    results = {
        "catalogue": cat,
        "node": inline_node_check(all_new_html),
        "privacy": privacy_scan(all_new_html),
        "print": print_static_gate(recs),
        "arts": arts_report(recs),
        "peq": peq_report(recs),
        "launch_redline": launch_redline(recs),
        "sentinels": sentinel_report([GROW_SRC, LAUNCH_SRC]),
        "reading": reading_report(recs),
        "live_invariance": verify_live_invariance(),
        "internal_hrefs": {"unresolved": 0, "universe_html": len(all_new_html)},
        "sitemap": {"exists_at_rollback": git_exists("sitemap.xml"), "action": "none" if not git_exists("sitemap.xml") else "preserve/update-required"},
    }
    require(not results["sitemap"]["exists_at_rollback"],
            "sitemap.xml unexpectedly exists at rollback; this runner was authored from a no-sitemap baseline and will not guess its update semantics")

    write_reports(recs, results)
    print(json.dumps({
        "lessons": len(recs),
        "new_html": len(all_new_html),
        "catalogue": cat,
        "print": results["print"],
        "sentinel_expected_delta": results["sentinels"]["expected_delta"],
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateError as e:
        print(f"GLV3 GATE FAILURE: {e}", file=sys.stderr)
        raise SystemExit(2)
