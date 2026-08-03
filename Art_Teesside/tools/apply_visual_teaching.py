#!/usr/bin/env python3
"""Apply/check the shared Art Teesside visual-teaching references.

The injector changes only two generated marker blocks per applicable HTML page.
Removing those exact blocks must reproduce the recorded baseline byte for byte.
The source transformation is deliberately line- and structure-aware: generated
blocks are inserted at the start of the real closing-tag line, before any
existing indentation, so authored whitespace and newline conventions survive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ART = REPO / "Art_Teesside"
ROOT_HUB = REPO / "art_teesside.html"
BASELINE = ART / "tools" / "visual_content_baseline.json"
EXPECTED_APPLICABLE = 35
CSS_START = "<!-- ART-TEACH:CSS:START — generated shared reference; edit Art_Teesside/art-teach.css -->"
CSS_END = "<!-- ART-TEACH:CSS:END -->"
JS_START = "<!-- ART-TEACH:JS:START — generated shared reference; edit Art_Teesside/art-teach.js -->"
JS_END = "<!-- ART-TEACH:JS:END -->"
LESSON_RE = re.compile(r"^(?:BUILD|GROW|LAUNCH)_ART_(?:A2_)?W\d+_.+\.html$")
TAG_RE = re.compile(r"^<\s*(/?)\s*([A-Za-z][A-Za-z0-9:_-]*)")
RAW_TEXT_TAGS = {"script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes"}
FOREIGN_ROOTS = {"svg", "math"}


@dataclass(frozen=True)
class ClosingLine:
    tag: str
    line_start: int
    tag_start: int
    tag_end: int
    indent: str


def read_source(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write_source(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def newline_convention(text: str, label: object) -> str:
    without_crlf = text.replace("\r\n", "")
    if "\r" in without_crlf:
        raise ValueError(f"{label}: unsupported bare CR newline")
    if "\r\n" in text and "\n" in without_crlf:
        raise ValueError(f"{label}: mixed LF and CRLF newlines")
    return "\r\n" if "\r\n" in text else "\n"


def _tag_end(text: str, start: int) -> int:
    quote: str | None = None
    index = start + 1
    while index < len(text):
        char = text[index]
        if quote:
            if char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        elif char == ">":
            return index + 1
        index += 1
    raise ValueError(f"unterminated HTML tag beginning at byte {start}")


def _raw_close(text: str, start: int, tag: str) -> tuple[int, int]:
    pattern = re.compile(rf"</\s*{re.escape(tag)}\s*>", re.IGNORECASE)
    match = pattern.search(text, start)
    if not match:
        raise ValueError(f"unterminated raw-text element <{tag}>")
    return match.start(), match.end()


def structural_closing_tags(text: str, wanted: str) -> list[ClosingLine]:
    """Return real wanted closing tags, excluding comments/raw/template/foreign text.

    This is a bounded HTML source scanner rather than a global closing-tag regex.
    It tokenises quoted tags and comments, treats script/style-like elements as
    raw text, and ignores candidate tags while inside template or SVG/MathML
    content. The expected estate insertion point must occupy its own line; this
    lets the injector preserve the complete original closing-tag line verbatim.
    """

    wanted = wanted.lower()
    candidates: list[ClosingLine] = []
    template_depth = 0
    foreign_depth = 0
    raw_tag: str | None = None
    index = 0

    while index < len(text):
        if raw_tag:
            start, end = _raw_close(text, index, raw_tag)
            raw_tag = None
            index = end
            continue

        next_lt = text.find("<", index)
        if next_lt < 0:
            break
        index = next_lt

        if text.startswith("<!--", index):
            end = text.find("-->", index + 4)
            if end < 0:
                raise ValueError("unterminated HTML comment")
            index = end + 3
            continue
        if text.startswith("<![CDATA[", index):
            end = text.find("]]>", index + 9)
            if end < 0:
                raise ValueError("unterminated CDATA section")
            index = end + 3
            continue
        if text.startswith("<?", index):
            end = text.find("?>", index + 2)
            if end < 0:
                raise ValueError("unterminated processing instruction")
            index = end + 2
            continue

        try:
            end = _tag_end(text, index)
        except ValueError:
            raise
        token = text[index:end]
        match = TAG_RE.match(token)
        if not match:
            index = end
            continue

        is_end = bool(match.group(1))
        name = match.group(2).lower()
        self_closing = token.rstrip().endswith("/>")

        if is_end and name == wanted and template_depth == 0 and foreign_depth == 0:
            line_start = text.rfind("\n", 0, index) + 1
            line_prefix = text[line_start:index]
            indent = line_prefix if all(char in " \t" for char in line_prefix) else ""
            candidates.append(ClosingLine(wanted, line_start, index, end, indent))

        if name == "template":
            if is_end:
                template_depth = max(0, template_depth - 1)
            elif not self_closing:
                template_depth += 1
        elif name in FOREIGN_ROOTS:
            if is_end:
                foreign_depth = max(0, foreign_depth - 1)
            elif not self_closing:
                foreign_depth += 1

        if not is_end and not self_closing and name in RAW_TEXT_TAGS:
            raw_tag = name
        index = end

    return candidates


def closing_line(text: str, tag: str, label: object) -> ClosingLine:
    matches = structural_closing_tags(text, tag)
    if len(matches) != 1:
        positions = ", ".join(str(match.tag_start) for match in matches) or "none"
        raise ValueError(
            f"{label}: expected exactly one structural </{tag}>; found {len(matches)} ({positions})"
        )
    return matches[0]


def applicable_files() -> list[Path]:
    files: list[Path] = [ROOT_HUB]
    for strand in ("Build", "Grow", "Launch"):
        folder = ART / strand
        files.append(folder / "START_HERE.html")
        files.extend(p for p in folder.glob("*.html") if LESSON_RE.match(p.name))
    files = sorted(set(files), key=lambda p: p.relative_to(REPO).as_posix())
    if len(files) != EXPECTED_APPLICABLE:
        names = "\n".join(f"  {p.relative_to(REPO).as_posix()}" for p in files)
        raise RuntimeError(
            f"applicable population changed: expected {EXPECTED_APPLICABLE}, found {len(files)}\n{names}"
        )
    missing = [p for p in files if not p.is_file()]
    if missing:
        raise RuntimeError("missing applicable files: " + ", ".join(str(p) for p in missing))
    return files


def hrefs(path: Path) -> tuple[str, str]:
    if path == ROOT_HUB:
        return "Art_Teesside/art-teach.css", "Art_Teesside/art-teach.js"
    return "../art-teach.css", "../art-teach.js"


def blocks(path: Path, text: str) -> tuple[str, str, ClosingLine, ClosingLine]:
    newline = newline_convention(text, path)
    head = closing_line(text, "head", path)
    body = closing_line(text, "body", path)
    css, js = hrefs(path)
    css_block = (
        f"{CSS_START}{newline}"
        f"{head.indent}<link rel=\"stylesheet\" href=\"{css}\">{newline}"
        f"{head.indent}{CSS_END}{newline}"
        f"{head.indent}"
    )
    js_block = (
        f"{JS_START}{newline}"
        f"{body.indent}<script src=\"{js}\"></script>{newline}"
        f"{body.indent}{JS_END}{newline}"
        f"{body.indent}"
    )
    return css_block, js_block, head, body


def marker_counts(text: str) -> dict[str, int]:
    return {marker: text.count(marker) for marker in (CSS_START, CSS_END, JS_START, JS_END)}


def strip_generated(text: str, path: Path) -> str:
    counts = marker_counts(text)
    if not any(counts.values()):
        return text
    if not all(value == 1 for value in counts.values()):
        raise ValueError(f"{path}: partial or duplicate marker set {counts}")

    css_block, js_block, head, body = blocks(path, text)
    css_start = text.index(CSS_START)
    js_start = text.index(JS_START)
    if text[css_start : css_start + len(css_block)] != css_block:
        raise ValueError(f"{path}: CSS markers exist but generated block differs")
    if text[js_start : js_start + len(js_block)] != js_block:
        raise ValueError(f"{path}: JS markers exist but generated block differs")
    if css_start + len(css_block) != head.tag_start:
        raise ValueError(f"{path}: CSS generated block is not immediately before </head>")
    if js_start + len(js_block) != body.tag_start:
        raise ValueError(f"{path}: JS generated block is not immediately before </body>")

    spans = sorted(((css_start, head.tag_start), (js_start, body.tag_start)), reverse=True)
    out = text
    for start, end in spans:
        out = out[:start] + out[end:]
    leftovers = [marker for marker in (CSS_START, CSS_END, JS_START, JS_END) if marker in out]
    if leftovers:
        raise ValueError(f"{path}: malformed generated marker block: {leftovers}")
    return out


def apply_text(text: str, path: Path) -> tuple[str, bool]:
    counts = marker_counts(text)
    if all(value == 1 for value in counts.values()):
        # Exact location and content are validated by the strict stripper.
        strip_generated(text, path)
        return text, False
    if any(counts.values()):
        raise ValueError(f"{path}: partial or duplicate marker set {counts}")

    css_block, js_block, head, body = blocks(path, text)
    insertions = sorted(
        ((head.tag_start, css_block), (body.tag_start, js_block)),
        reverse=True,
    )
    updated = text
    for offset, block in insertions:
        updated = updated[:offset] + block + updated[offset:]

    if strip_generated(updated, path) != text:
        raise AssertionError(f"{path}: generated-block round trip failed")
    return updated, True


def apply_one(path: Path) -> bool:
    text = read_source(path)
    updated, changed = apply_text(text, path)
    if changed:
        write_source(path, updated)
    return changed


def verify_one(path: Path) -> list[str]:
    text = read_source(path)
    problems: list[str] = []
    counts = marker_counts(text)
    for marker, count in counts.items():
        if count != 1:
            problems.append(f"{marker!r} count={count}")
    css_href, js_src = hrefs(path)
    css_tag = f'<link rel="stylesheet" href="{css_href}">'
    js_tag = f'<script src="{js_src}"></script>'
    if text.count(css_tag) != 1:
        problems.append(f"CSS tag count={text.count(css_tag)}")
    if text.count(js_tag) != 1:
        problems.append(f"JS tag count={text.count(js_tag)}")
    try:
        strip_generated(text, path)
    except (AssertionError, ValueError) as exc:
        problems.append(str(exc))
    return problems


def baseline_data() -> dict:
    if not BASELINE.is_file():
        raise FileNotFoundError(f"missing baseline manifest: {BASELINE.relative_to(REPO)}")
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def verify_round_trip(files: list[Path]) -> list[str]:
    data = baseline_data()
    expected = data.get("files", {})
    failures: list[str] = []
    actual_paths = {p.relative_to(REPO).as_posix() for p in files}
    if set(expected) != actual_paths:
        failures.append(
            "baseline path set differs: missing=" + str(sorted(actual_paths - set(expected)))
            + " extra=" + str(sorted(set(expected) - actual_paths))
        )
    for path in files:
        rel = path.relative_to(REPO).as_posix()
        stripped = strip_generated(read_source(path), path).encode("utf-8")
        digest = hashlib.sha256(stripped).hexdigest()
        record = expected.get(rel, {})
        if digest != record.get("sha256") or len(stripped) != record.get("bytes"):
            failures.append(
                f"{rel}: stripped bytes/hash differ: {len(stripped)} {digest}; "
                f"expected {record.get('bytes')} {record.get('sha256')}"
            )
    return failures


def write_baseline(files: list[Path], source_commit: str) -> None:
    if BASELINE.exists():
        raise FileExistsError(f"refusing to overwrite {BASELINE.relative_to(REPO)}")
    records = {}
    for path in files:
        raw = path.read_bytes()
        records[path.relative_to(REPO).as_posix()] = {
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    BASELINE.write_text(
        json.dumps(
            {
                "source_commit": source_commit,
                "scope": "approved authored bytes before ART-TEACH generated reference blocks",
                "file_count": len(records),
                "files": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _expect_failure(label: str, function, expected: str) -> None:
    try:
        function()
    except ValueError as exc:
        if expected not in str(exc):
            raise AssertionError(f"{label}: wrong failure: {exc}") from exc
    else:
        raise AssertionError(f"{label}: expected ValueError containing {expected!r}")


def _has_trailing_whitespace(text: str) -> bool:
    return any(re.search(r"[ \t]+$", line) for line in text.splitlines())


def self_test() -> None:
    fixture_path = REPO / "Art_Teesside" / "Build" / "INJECTOR_FIXTURE.html"

    def fixture(indent: str, newline: str, decoys: bool = False) -> str:
        extra = ""
        if decoys:
            extra = newline.join(
                (
                    "  <!-- fake </body> in a comment -->",
                    "  <script>const fake = '</body>'; const fakeHead = '</head>';</script>",
                    "  <style>.x::after{content:'</body>'}</style>",
                    "  <template><div data-text='</body>'>template</div></template>",
                    "  <svg><text>&lt;/body&gt;</text></svg>",
                )
            ) + newline
        return newline.join(
            (
                "<!doctype html>",
                "<html lang=\"en\">",
                "<head>",
                "  <meta charset=\"utf-8\">",
                f"{indent}</head>",
                "<body>",
                extra.rstrip("\r\n"),
                f"{indent}</body>",
                "</html>",
                "",
            )
        )

    cases = [
        ("unindented LF", "", "\n"),
        ("two-space LF", "  ", "\n"),
        ("four-space LF", "    ", "\n"),
        ("tab LF", "\t", "\n"),
        ("unindented CRLF", "", "\r\n"),
        ("two-space CRLF", "  ", "\r\n"),
        ("four-space CRLF", "    ", "\r\n"),
        ("tab CRLF", "\t", "\r\n"),
    ]
    for label, indent, newline in cases:
        original = fixture(indent, newline)
        generated, changed = apply_text(original, fixture_path)
        if not changed:
            raise AssertionError(f"{label}: first run did not change the fixture")
        if strip_generated(generated, fixture_path) != original:
            raise AssertionError(f"{label}: bytes outside generated blocks changed")
        second, second_changed = apply_text(generated, fixture_path)
        if second_changed or second != generated:
            raise AssertionError(f"{label}: second run was not byte-identical")
        if _has_trailing_whitespace(generated):
            raise AssertionError(f"{label}: generated output contains trailing whitespace")
        if newline == "\r\n" and "\n" in generated.replace("\r\n", ""):
            raise AssertionError(f"{label}: CRLF input gained bare LF newlines")

    decoy_original = fixture("  ", "\n", decoys=True)
    decoy_generated, _ = apply_text(decoy_original, fixture_path)
    if strip_generated(decoy_generated, fixture_path) != decoy_original:
        raise AssertionError("decoy fixture changed bytes outside intended insertion")

    existing, _ = apply_text(fixture("    ", "\n"), fixture_path)
    unchanged, changed = apply_text(existing, fixture_path)
    if changed or unchanged != existing:
        raise AssertionError("existing generated block was duplicated or rewritten")

    missing = fixture("  ", "\n").replace("  </body>\n", "")
    _expect_failure(
        "missing body",
        lambda: apply_text(missing, fixture_path),
        "found 0",
    )
    duplicate = fixture("  ", "\n").replace("  </body>", "  </body>\n  </body>")
    _expect_failure(
        "duplicate body",
        lambda: apply_text(duplicate, fixture_path),
        "found 2",
    )

    # Controlled proof of the historical defect: inserting after indentation
    # leaves an indentation-only line, which git diff --check rejects.
    legacy = fixture("  ", "\n")
    legacy_css = f"\n{CSS_START}\n<link rel=\"stylesheet\" href=\"../art-teach.css\">\n{CSS_END}\n"
    legacy_js = f"\n{JS_START}\n<script src=\"../art-teach.js\"></script>\n{JS_END}\n"
    legacy = legacy.replace("</head>", legacy_css + "</head>", 1)
    legacy = legacy.replace("</body>", legacy_js + "</body>", 1)
    if not _has_trailing_whitespace(legacy):
        raise AssertionError("legacy indentation defect control did not reproduce")

    print(
        "INJECTOR REGRESSION PASS — 8 indentation/newline cases; comments, raw text, "
        "templates and SVG decoys ignored; missing/duplicate tags rejected; legacy defect detected"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--apply", action="store_true")
    action.add_argument("--write-baseline", metavar="COMMIT")
    action.add_argument("--list", action="store_true")
    action.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    files = applicable_files()
    for path in files:
        print(path.relative_to(REPO).as_posix())
    print(f"APPLICABLE TOTAL {len(files)}")

    if args.list:
        return 0
    if args.write_baseline:
        write_baseline(files, args.write_baseline)
        print(f"WROTE {BASELINE.relative_to(REPO)}")
        return 0
    if args.apply:
        changed = sum(apply_one(path) for path in files)
        print(f"APPLIED {changed}; already current {len(files) - changed}")

    failures: list[str] = []
    for path in files:
        failures.extend(f"{path.relative_to(REPO)}: {problem}" for problem in verify_one(path))
    if BASELINE.exists():
        failures.extend(verify_round_trip(files))
    else:
        failures.append(f"missing {BASELINE.relative_to(REPO)}")

    if failures:
        print("VISUAL TEACHING REFERENCE ASSERTION FAILED", file=sys.stderr)
        for failure in failures:
            print("  " + failure, file=sys.stderr)
        return 1
    print(f"VISUAL TEACHING REFERENCE ASSERTION PASS — {len(files)} files, exact content round trip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
