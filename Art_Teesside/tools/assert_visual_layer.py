#!/usr/bin/env python3
"""Static assertion for the Art Teesside shared visual-teaching layer.

Prints the exact population behind every count. Use --self-test to prove the
assertions detect deliberate duplicate, missing-reference, debug and CSS defects.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[2]
ART = REPO / "Art_Teesside"
ROOT_ENTRY = REPO / "art_teesside.html"
EXPECTED = {
    "lesson": 31,
    "hub": 3,
    "printable": 8,
    "scheme": 9,
    "support": 2,
}
EXPECTED_HTML = 53
EXPECTED_APPLICABLE = 35
IGNORE_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:")
ROOT_SHARED = {"/hud.js": "mattroper1977.github.io/hud.js"}


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.refs.append((tag, values["href"] or ""))
        if tag in {"script", "img", "iframe", "source", "video", "audio"} and values.get("src"):
            self.refs.append((tag, values["src"] or ""))


def classify(path: Path) -> str:
    name = path.name
    if re.match(r"^(?:BUILD|GROW|LAUNCH)_ART_(?:A2_)?W\d+_.+\.html$", name):
        return "lesson"
    if name == "START_HERE.html":
        return "hub"
    if "Printable" in name or "Pack" in name:
        return "printable"
    if "Scheme_of_Work" in name or "Run_Sheets" in name:
        return "scheme"
    return "support"


def populations() -> dict[str, list[Path]]:
    out = {key: [] for key in EXPECTED}
    for path in sorted(ART.rglob("*.html")):
        out[classify(path)].append(path)
    return out


def applicable(pop: dict[str, list[Path]]) -> list[Path]:
    return sorted([ROOT_ENTRY, *pop["lesson"], *pop["hub"]])


def expected_shared_paths(path: Path) -> tuple[str, str]:
    if path == ROOT_ENTRY:
        return "Art_Teesside/art-teach.css", "Art_Teesside/art-teach.js"
    return "../art-teach.css", "../art-teach.js"


def reference_errors(path: Path, text: str) -> list[str]:
    css, js = expected_shared_paths(path)
    checks = {
        "CSS start marker": text.count("<!-- ART-TEACH:CSS:START"),
        "CSS end marker": text.count("<!-- ART-TEACH:CSS:END -->"),
        "JS start marker": text.count("<!-- ART-TEACH:JS:START"),
        "JS end marker": text.count("<!-- ART-TEACH:JS:END -->"),
        "CSS tag": text.count(f'<link rel="stylesheet" href="{css}">'),
        "JS tag": text.count(f'<script src="{js}"></script>'),
    }
    return [f"{label} count={count}" for label, count in checks.items() if count != 1]


def strip_css_for_balance(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"", "", css)
    return css


def css_balance(css: str) -> tuple[bool, str]:
    cleaned = strip_css_for_balance(css)
    depth = 0
    for index, ch in enumerate(cleaned):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False, f"closing brace before opening at character {index}"
    return (depth == 0, f"final brace depth {depth}")


def local_reference_errors(path: Path, text: str) -> list[str]:
    parser = RefParser()
    parser.feed(text)
    problems: list[str] = []
    for tag, raw in parser.refs:
        ref = raw.strip()
        if not ref or ref.startswith("#") or ref.startswith(IGNORE_SCHEMES):
            continue
        bits = urlsplit(ref)
        route = unquote(bits.path)
        if not route:
            continue
        if route.startswith("/"):
            if route in ROOT_SHARED:
                continue
            # A root URL belongs to the custom-domain repository, not this project checkout.
            continue
        target = (path.parent / route).resolve()
        try:
            target.relative_to(REPO.resolve())
        except ValueError:
            problems.append(f"{tag} {ref!r} escapes repository")
            continue
        if not target.exists():
            problems.append(f"{tag} {ref!r} -> missing {target.relative_to(REPO)}")
    return problems


def self_test() -> int:
    sample = ROOT_ENTRY
    css, js = expected_shared_paths(sample)
    valid = (
        "<!-- ART-TEACH:CSS:START — generated shared reference; edit Art_Teesside/art-teach.css -->\n"
        f'<link rel="stylesheet" href="{css}">\n'
        "<!-- ART-TEACH:CSS:END -->\n"
        "<!-- ART-TEACH:JS:START — generated shared reference; edit Art_Teesside/art-teach.js -->\n"
        f'<script src="{js}"></script>\n'
        "<!-- ART-TEACH:JS:END -->"
    )
    controls = {
        "duplicate shared tag": bool(reference_errors(sample, valid + f'\n<link rel="stylesheet" href="{css}">')),
        "missing local asset": bool(local_reference_errors(ART / "control.html", '<img src="definitely-missing.png">')),
        "unbalanced CSS": not css_balance(".a{display:block}}")[0],
        "debug output": bool(re.search(r"\bconsole\.log\s*\(", "console.log('control')")),
    }
    for name, detected in controls.items():
        print(f"CONTROL {name}: {'DETECTED' if detected else 'MISSED'}")
    ok = all(controls.values())
    print("VISUAL STATIC SELF-TEST PASS" if ok else "VISUAL STATIC SELF-TEST FAILED")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    problems: list[str] = []
    pop = populations()
    total = sum(len(paths) for paths in pop.values())
    for category, paths in pop.items():
        print(f"\n[{category}] {len(paths)}")
        for path in paths:
            print("  " + path.relative_to(REPO).as_posix())
        if len(paths) != EXPECTED[category]:
            problems.append(f"{category}: expected {EXPECTED[category]}, found {len(paths)}")
    print(f"\nART_Teesside HTML TOTAL {total}")
    if total != EXPECTED_HTML:
        problems.append(f"HTML population expected {EXPECTED_HTML}, found {total}")

    scope = applicable(pop)
    print(f"\n[applicable lesson/hub entry points] {len(scope)}")
    for path in scope:
        print("  " + path.relative_to(REPO).as_posix())
    if len(scope) != EXPECTED_APPLICABLE:
        problems.append(f"applicable population expected {EXPECTED_APPLICABLE}, found {len(scope)}")

    scope_set = set(scope)
    for path in [ROOT_ENTRY, *sorted(ART.rglob("*.html"))]:
        text = path.read_text(encoding="utf-8")
        if path in scope_set:
            problems.extend(f"{path.relative_to(REPO)}: {e}" for e in reference_errors(path, text))
        else:
            if "ART-TEACH:" in text or "art-teach.css" in text or "art-teach.js" in text:
                problems.append(f"{path.relative_to(REPO)}: shared presentation layer injected into non-applicable support resource")
        problems.extend(f"{path.relative_to(REPO)}: {e}" for e in local_reference_errors(path, text))

    css_path = ART / "art-teach.css"
    js_path = ART / "art-teach.js"
    if not css_path.is_file() or not js_path.is_file():
        problems.append("shared CSS/JS source missing")
    else:
        balanced, note = css_balance(css_path.read_text(encoding="utf-8"))
        print(f"\nCSS balance: {note}")
        if not balanced:
            problems.append("art-teach.css: " + note)
        node = subprocess.run(["node", "--check", str(js_path)], text=True, capture_output=True)
        print(f"JS syntax exit: {node.returncode}")
        if node.returncode:
            problems.append("art-teach.js syntax: " + (node.stderr.strip() or node.stdout.strip()))
        js = js_path.read_text(encoding="utf-8")
        css = css_path.read_text(encoding="utf-8")
        required_js = [
            "data-art-teach-boot", "window.ArtTeach", "MutationObserver",
            "prefers-reduced-motion", "at-pair-trail", "ilm-replay",
            "aria-live", "requestAnimationFrame",
        ]
        required_css = [
            "@media print", "prefers-reduced-motion", ":focus-visible",
            ".at-activity-bar", ".at-pair-trail", ".ilm-replay",
            "animation-play-state:paused",
        ]
        for token in required_js:
            if token not in js:
                problems.append(f"art-teach.js missing required safeguard {token!r}")
        for token in required_css:
            if token not in css:
                problems.append(f"art-teach.css missing required safeguard {token!r}")

        forbidden = {
            "conflict marker": re.compile(r"^(?:<<<<<<<|=======|>>>>>>>)", re.M),
            "TODO/FIXME": re.compile(r"\b(?:TODO|FIXME)\b"),
            "debugger": re.compile(r"\bdebugger\b"),
            "console.log": re.compile(r"\bconsole\.log\s*\("),
        }
        for label, pattern in forbidden.items():
            for source in (css_path, js_path, ART / "tools" / "apply_visual_teaching.py"):
                if pattern.search(source.read_text(encoding="utf-8")):
                    problems.append(f"{source.relative_to(REPO)} contains {label}")

    round_trip = subprocess.run(
        [sys.executable, str(ART / "tools" / "apply_visual_teaching.py")],
        cwd=REPO,
        text=True,
        capture_output=True,
    )
    print(f"Content/reference round-trip exit: {round_trip.returncode}")
    if round_trip.returncode:
        problems.append("content/reference round trip failed:\n" + round_trip.stdout + round_trip.stderr)

    print("\nRoot-shared dependencies:")
    for route, owner in ROOT_SHARED.items():
        consumers = [
            p.relative_to(REPO).as_posix()
            for p in scope
            if route in p.read_text(encoding="utf-8")
        ]
        print(f"  {route} -> {owner}: {len(consumers)} consumers")
        for consumer in consumers:
            print("    " + consumer)

    if problems:
        print("\nVISUAL LAYER ASSERTION FAILED", file=sys.stderr)
        for problem in problems:
            print("  " + problem, file=sys.stderr)
        return 1
    print("\nVISUAL LAYER ASSERTION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
