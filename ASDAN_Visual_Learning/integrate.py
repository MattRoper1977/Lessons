#!/usr/bin/env python3
"""Integrate the ASDAN visual-learning layer through the estate's existing sources.

Dry-run by default. This script never invokes Git, commits, pushes or opens a PR.
"""
from __future__ import annotations
import argparse, difflib, json, re, sys
from pathlib import Path
from typing import Iterable

TOOLKIT = Path(__file__).resolve().parent
CSS = (TOOLKIT / "asdan-visual-learning.css").read_text(encoding="utf-8").rstrip() + "\n"
CORE_JS = (TOOLKIT / "asdan-visual-learning.js").read_text(encoding="utf-8").rstrip() + "\n"
PAYLOADS = json.loads((TOOLKIT / "lesson-payloads.json").read_text(encoding="utf-8"))

CSS_START = "/* ASDAN-VISUAL-LEARNING:CSS:BEGIN v1 */"
CSS_END = "/* ASDAN-VISUAL-LEARNING:CSS:END v1 */"
JS_START = "/* ASDAN-VISUAL-LEARNING:JS:BEGIN v1 */"
JS_END = "/* ASDAN-VISUAL-LEARNING:JS:END v1 */"
HTML_START = "<!-- ASDAN-VISUAL-LEARNING:HTML:BEGIN v1 -->"
HTML_END = "<!-- ASDAN-VISUAL-LEARNING:HTML:END v1 -->"

SOURCE_TARGETS = {
    "BUILD": {
        "css": "BUILD_ASDAN/_framework/asdan-teach.css",
        "js": "BUILD_ASDAN/_framework/asdan-teach.js",
    },
    "GROW": {
        "css": "GROW_ASDAN/visual-upgrade.css",
        "js": "GROW_ASDAN/visual-upgrade.js",
    },
    "LAUNCH": {
        "css": "LAUNCH_ASDAN/visual-upgrade.css",
        "js": "LAUNCH_ASDAN/visual-upgrade.js",
    },
}
DT_PATHS = sorted(
    payload["path"] for payload in PAYLOADS.values()
    if payload["path"].startswith("Build/Slideshows/")
)
BUILD_MATERIALISED = sorted(
    payload["path"] for payload in PAYLOADS.values()
    if payload["path"].startswith("BUILD_ASDAN/")
)

def registry_js(payloads: dict) -> str:
    compact = json.dumps(payloads, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return "window.ASDANVisualPayloads = Object.assign(window.ASDANVisualPayloads || {}, " + compact + ");\n"

def css_block() -> str:
    return f"\n{CSS_START}\n{CSS}{CSS_END}\n"

def js_block(pathway: str) -> str:
    subset = {slug: payload for slug, payload in PAYLOADS.items() if payload["pathway"] == pathway}
    return f"\n{JS_START}\n{registry_js(subset)}{CORE_JS}{JS_END}\n"

def html_block(slug: str) -> str:
    payload = {slug: PAYLOADS[slug]}
    return (
        f"\n{HTML_START}\n"
        f"<style>\n{CSS}</style>\n"
        f"<script>\n{registry_js(payload)}{CORE_JS}</script>\n"
        f"{HTML_END}\n"
    )

def strip_between(text: str, start: str, end: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"(?:\r?\n)?", re.S)
    return pattern.sub("", text)

def set_source_block(text: str, start: str, end: str, block: str) -> str:
    clean = strip_between(text, start, end).rstrip() + "\n"
    return clean + block.lstrip("\n")

def set_html_block(text: str, block: str) -> str:
    clean = strip_between(text, HTML_START, HTML_END)
    marker = re.search(r"</body\s*>", clean, re.I)
    if not marker:
        raise ValueError("HTML has no closing </body> element.")
    return clean[:marker.start()] + block.strip() + clean[marker.start():]

def strip_all(text: str) -> str:
    # Direct D&T blocks contain the CSS/JS markers inside the outer HTML marker,
    # so remove the outer unit first. Shared sources then use their own markers.
    text = strip_between(text, HTML_START, HTML_END)
    text = strip_between(text, CSS_START, CSS_END)
    text = strip_between(text, JS_START, JS_END)
    return text

def read_required(repo: Path, rel: str) -> str:
    path = repo / rel
    if not path.is_file():
        raise FileNotFoundError(f"Required integration target does not exist: {rel}")
    return path.read_text(encoding="utf-8")

def desired_changes(repo: Path, strip: bool = False) -> dict[str, tuple[str, str]]:
    changes: dict[str, tuple[str, str]] = {}
    for pathway, targets in SOURCE_TARGETS.items():
        css_rel, js_rel = targets["css"], targets["js"]
        old_css = read_required(repo, css_rel)
        old_js = read_required(repo, js_rel)
        new_css = strip_all(old_css) if strip else set_source_block(old_css, CSS_START, CSS_END, css_block())
        new_js = strip_all(old_js) if strip else set_source_block(old_js, JS_START, JS_END, js_block(pathway))
        if old_css != new_css:
            changes[css_rel] = (old_css, new_css)
        if old_js != new_js:
            changes[js_rel] = (old_js, new_js)
    for rel in DT_PATHS:
        old = read_required(repo, rel)
        if strip:
            new = strip_all(old)
        else:
            slug = Path(rel).stem
            if slug not in PAYLOADS:
                raise KeyError(f"No payload for D&T lesson {slug}.")
            new = set_html_block(old, html_block(slug))
        if old != new:
            changes[rel] = (old, new)
    return changes

def unified_patch(changes: dict[str, tuple[str, str]]) -> str:
    chunks: list[str] = []
    for rel in sorted(changes):
        old, new = changes[rel]
        diff_lines = difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile=f"a/{rel}",
            tofile=f"b/{rel}",
            lineterm="",
        )
        chunks.append("\n".join(diff_lines) + "\n")
    return "".join(chunks)

def exact_source_check(repo: Path) -> list[str]:
    errors: list[str] = []
    for pathway, targets in SOURCE_TARGETS.items():
        css = read_required(repo, targets["css"])
        js = read_required(repo, targets["js"])
        expected_css = css_block().strip()
        expected_js = js_block(pathway).strip()
        if css.count(CSS_START) != 1 or css.count(CSS_END) != 1:
            errors.append(f"{targets['css']}: expected one owned CSS marker pair.")
        elif expected_css not in css:
            errors.append(f"{targets['css']}: owned CSS block is stale.")
        if js.count(JS_START) != 1 or js.count(JS_END) != 1:
            errors.append(f"{targets['js']}: expected one owned JS marker pair.")
        elif expected_js not in js:
            errors.append(f"{targets['js']}: owned JS block is stale.")
    for rel in DT_PATHS:
        text = read_required(repo, rel)
        slug = Path(rel).stem
        expected = html_block(slug).strip()
        if text.count(HTML_START) != 1 or text.count(HTML_END) != 1:
            errors.append(f"{rel}: expected one owned HTML marker pair.")
        elif expected not in text:
            errors.append(f"{rel}: owned lesson block is stale.")
    return errors

def materialised_check(repo: Path) -> list[str]:
    errors: list[str] = []
    for rel in BUILD_MATERIALISED:
        path = repo / rel
        if not path.is_file():
            errors.append(f"{rel}: missing BUILD lesson.")
            continue
        text = path.read_text(encoding="utf-8")
        if text.count(CSS_START) != 1 or text.count(JS_START) != 1:
            errors.append(f"{rel}: BUILD framework has not materialised the visual-learning source.")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="Lessons repository root.")
    parser.add_argument("--apply", action="store_true", help="Write the proposed source changes.")
    parser.add_argument("--check", action="store_true", help="Verify the exact owned blocks already exist.")
    parser.add_argument("--strip", action="store_true", help="Remove only this toolkit's owned blocks.")
    parser.add_argument("--expect-build-materialized", action="store_true",
                        help="Also require BUILD_ASDAN/_framework/apply_framework.py to have propagated the source.")
    parser.add_argument("--patch-out", help="Write an exact unified diff for the current checkout.")
    parser.add_argument("--json-report", help="Write a machine-readable report.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    report = {
        "repo": str(repo),
        "baselineNote": "Derive the current checkout at run time; never trust a stale prompt SHA.",
        "lessonPayloads": len(PAYLOADS),
        "sourceFiles": [item for targets in SOURCE_TARGETS.values() for item in targets.values()],
        "directLessonFiles": DT_PATHS,
        "buildMaterialisedLessons": BUILD_MATERIALISED,
        "mode": "check" if args.check else "strip" if args.strip else "apply" if args.apply else "dry-run",
    }
    try:
        if args.check:
            errors = exact_source_check(repo)
            if args.expect_build_materialized:
                errors.extend(materialised_check(repo))
            report["errors"] = errors
            report["ok"] = not errors
            if args.json_report:
                Path(args.json_report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            if errors:
                print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
                return 1
            print(f"PASS · exact source integration present · 6 shared sources · {len(DT_PATHS)} direct D&T lessons"
                  + (f" · {len(BUILD_MATERIALISED)} BUILD lessons materialised" if args.expect_build_materialized else ""))
            return 0

        changes = desired_changes(repo, strip=args.strip)
        report["changedFiles"] = sorted(changes)
        report["changedFileCount"] = len(changes)
        patch = unified_patch(changes)
        if args.patch_out:
            Path(args.patch_out).write_text(patch, encoding="utf-8")
        if args.apply or args.strip:
            for rel, (_, new) in changes.items():
                (repo / rel).write_text(new, encoding="utf-8")
        if args.json_report:
            report["ok"] = True
            Path(args.json_report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        verb = "removed" if args.strip else "written" if args.apply else "planned"
        print(f"PASS · {len(changes)} source/direct-lesson changes {verb}; no Git command invoked.")
        if not args.apply and not args.strip:
            print("Dry run only. Use --apply to write, or --patch-out to save the exact diff.")
        return 0
    except Exception as exc:
        report["ok"] = False
        report["errors"] = [str(exc)]
        if args.json_report:
            Path(args.json_report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
