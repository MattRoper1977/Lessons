#!/usr/bin/env python3
"""Build FEB wave pack support from the frozen horizon ledger.

The script never authors pupil content. It only binds already-authored lesson
files into reciprocal chains and writes the family-proved front door, manifest
and checksum surfaces required for a pack landing.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HORIZON = ROOT / "_sownb/HORIZON_FEB.json"
CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"

CFG = {
    "BUILD Science": {
        "tokens": {"--grow": "#4E7A9B", "--navy": "#10233f", "--ink": "#1f2937", "--paper": "#ffffff", "--line": "#d8e0e8"},
        "accent": "var(--grow)", "title": "BUILD Science · Autumn review and Spring foundations",
    },
    "GROW Science": {
        "tokens": {"--grow": "#3F7D6E", "--navy": "#10233f", "--ink": "#1f2937", "--paper": "#ffffff", "--line": "#d8e0e8"},
        "accent": "var(--grow)", "title": "GROW Science · Spring materials and change",
    },
    "LAUNCH Science": {
        "tokens": {"--grow": "#7A5C9E", "--ink": "#1f2937", "--paper": "#ffffff", "--line": "#d8e0e8"},
        "accent": "var(--grow)", "title": "LAUNCH Science · Assessment, variation and selection",
    },
    "BUILD ASDAN": {
        "tokens": {"--ink": "#17223B", "--teal": "#346B7B", "--paper": "#FFFCF5", "--line": "#CAD5DF"},
        "accent": "var(--teal)", "title": "BUILD ASDAN · Spring choices and practical planning",
        "start_aliases": ["START_HERE_BUILD_ASDAN_AUT2.html"],
    },
    "GROW ASDAN": {
        "tokens": {"--slot": "#4a6fa5"},
        "accent": "var(--slot)", "title": "GROW ASDAN · Spring goals and project planning",
        "checksum": "CHECKSUMS.sha256",
    },
    "LAUNCH ASDAN": {
        "tokens": {"--accent": "#8e4f82", "--ink": "#18233f", "--line": "#d7dee5"},
        "accent": "var(--accent)", "title": "LAUNCH ASDAN · Spring decisions and practical action",
    },
    "BUILD Humanities": {
        "tokens": {"--ink": "#18233F", "--steel": "#4F869C", "--rust": "#D06438", "--teal": "#16877A", "--gold": "#E1AB32"},
        "accent": "var(--steel)", "title": "BUILD Humanities · Festivals, time and caring",
    },
    "GROW Humanities": {
        "tokens": {"--bg": "#141C24", "--steel": "#5B91A5", "--ink": "#172334", "--paper": "#ffffff", "--line": "#42515D"},
        "accent": "var(--steel)", "title": "GROW Humanities · Rights and belief resilience",
        "start_aliases": ["START_HERE_GROW_HUMANITIES_W9-W14.html"],
        "manifest_aliases": ["manifest-v3.1.json"],
    },
    "LAUNCH Humanities": {
        "tokens": {"--bg": "#141C24", "--steel": "#5B91A5", "--ink": "#172334", "--paper": "#ffffff", "--line": "#42515D"},
        "accent": "var(--steel)", "title": "LAUNCH Humanities · Conflict causes and ethical decisions",
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contract_value(row_id: str):
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    return next(row["value"] for row in contract["rows"] if row["id"] == row_id)


def rechain(paths: list[Path]) -> None:
    for index, path in enumerate(paths):
        source = path.read_text(encoding="utf-8")
        match = re.search(r'(<script id="lesson-config" type="application/json">)(.*?)(</script>)', source, re.S)
        if not match:
            raise RuntimeError(f"no lesson-config: {path}")
        data = json.loads(match.group(2))
        data["previousFile"] = "START_HERE.html" if index == 0 else paths[index - 1].name
        data["nextFile"] = "START_HERE.html" if index == len(paths) - 1 else paths[index + 1].name
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        path.write_text(source[: match.start(2)] + payload + source[match.end(2) :], encoding="utf-8")


def start_html(family: str, items: list[dict], pack: Path) -> str:
    cfg = CFG[family]
    depth = len(pack.relative_to(ROOT).parts)
    home = "../" * depth + "index.html"
    token_css = ";".join(f"{name}:{value}" for name, value in cfg["tokens"].items())
    cards = []
    for item in items:
        name = Path(item["destination"]).name
        outcomes = " · ".join(item["verbatimOutcomes"])
        cards.append(
            f'<a class="card week lesson-link" href="{html.escape(name)}">'
            f'<b>Absolute week {item["absoluteWeek"]} · {html.escape(item["objective"])}</b>'
            f'<span>{html.escape(outcomes)}</span></a>'
        )
    splash = contract_value("shared.splash.byte-block")
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(cfg["title"])} · lesson pack</title><style>:root{{{token_css}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper,#fff);color:var(--ink,#17223b);font-family:"Segoe UI",Arial,sans-serif}}main{{max-width:1040px;margin:auto;padding:18px}}.hero,.thread{{background:var(--ink,#17223b);color:#fff;border-radius:18px;padding:22px;border-bottom:9px solid {cfg["accent"]}}}h1{{font-size:clamp(2rem,6vw,3.6rem);line-height:1.05;margin:.2rem 0}}p,span{{line-height:1.45}}.grid,.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:12px;margin-top:16px}}.card,.week,.lesson-link{{display:block;border:2px solid var(--line,#ccd5df);border-top:8px solid {cfg["accent"]};border-radius:13px;padding:14px;background:#fff;color:var(--ink,#17223b);text-decoration:none;min-height:118px}}.card span,.week span,.lesson-link span{{display:block;margin-top:8px;color:#526173}}.mbmhome{{min-height:44px}}@media(max-width:420px){{main{{padding:10px}}}}@media print{{.mbmhome,.n6-splash{{display:none!important}}}}</style></head><body><!--n6-nav1:v1--><style id="n6-nav1-css">@media print{{.mbmhome,.n6-splash{{display:none!important}}}}.mbmhome{{display:inline-block;margin:6px 0 0 8px;font:600 .85rem/1.4 "Segoe UI",Arial,sans-serif;color:#1e3a8a;text-decoration:none}}.mbmhome:hover,.mbmhome:focus{{text-decoration:underline}}</style><a class="mbmhome" href="{home}" aria-label="Back to the Lessons catalogue">← Lessons</a><!--/n6-nav1--><main><header class="hero thread"><p>{html.escape(family)} · local offline lesson pack</p><h1>{html.escape(cfg["title"])}</h1><p>Open a lesson below. Every lesson target resolves inside this folder.</p></header><section class="grid cards">{''.join(cards)}</section></main>{splash}</body></html>'''


def build(pack: Path) -> dict:
    ledger = json.loads(HORIZON.read_text(encoding="utf-8"))
    items = [
        target for target in ledger["targets"]
        if target.get("authoringWave") == 1
        and (ROOT / target["destination"]).parent == pack
        and (ROOT / target["destination"]).is_file()
    ]
    if not items:
        raise RuntimeError("NO PACK: no authored wave-one targets")
    items.sort(key=lambda row: row["sequence"])
    family = items[0]["family"]
    if any(item["family"] != family for item in items):
        raise RuntimeError("mixed-family pack")
    cfg = CFG[family]
    paths = [ROOT / item["destination"] for item in items]
    rechain(paths)

    start_source = start_html(family, items, pack)
    (pack / "START_HERE.html").write_text(start_source, encoding="utf-8")
    for alias in cfg.get("start_aliases", []):
        (pack / alias).write_text(start_source, encoding="utf-8")

    manifest = {
        "schema": "feb-pack-v1",
        "family": family,
        "title": cfg["title"],
        "start": "START_HERE.html",
        "lessonCount": len(items),
        "timings": [0, 3, 3, 4, 3, 3, 4, 16, 4],
        "lessons": [
            {
                "id": item["id"], "file": Path(item["destination"]).name,
                "absoluteWeek": item["absoluteWeek"], "cells": item["workbookCells"],
                "outcomes": item["verbatimOutcomes"], "objective": item["objective"],
            }
            for item in items
        ],
    }
    manifest_source = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    (pack / "manifest.json").write_text(manifest_source, encoding="utf-8")
    for alias in cfg.get("manifest_aliases", []):
        (pack / alias).write_text(manifest_source, encoding="utf-8")

    members = sorted(
        list(pack.glob("*.html")) + list(pack.glob("manifest*.json")),
        key=lambda path: path.name,
    )
    checksum_name = cfg.get("checksum", "SHA256SUMS.txt")
    (pack / checksum_name).write_text(
        "".join(f"{sha(path)}  {path.name}\n" for path in members), encoding="ascii"
    )
    return {
        "status": "PASS", "pack": str(pack.relative_to(ROOT)), "family": family,
        "lessons": [path.name for path in paths], "members": [path.name for path in members],
        "checksum": checksum_name,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack", action="append", required=True)
    args = parser.parse_args()
    reports = [build((ROOT / rel).resolve()) for rel in args.pack]
    print(json.dumps(reports, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
