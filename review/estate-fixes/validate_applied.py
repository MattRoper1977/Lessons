#!/usr/bin/env python3
"""Validate the Lessons estate fix pack after applying it to a disposable worktree."""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import http.server
import json
import pathlib
import posixpath
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter
from typing import Any, Sequence

import html5lib  # type: ignore
import tinycss2  # type: ignore

BASE = "4aced082cc8f51868a99a8c6ab9d8147e380f6ec"
WAVE = "2 Physics 10/Waves/L4a_Wave_Anatomy.html"
GRID = "Games/Grid_Chase.html"
DIGESTION = "biology/Digestion_and_Absorption (1).html"
INDEX = "index.html"
MOTION = [
    "Science_Teesside/Build/SCI_B_W3_Backbones.html",
    "Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html",
    "Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html",
    "Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html",
    "Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html",
    "Science_Teesside/Grow/SCI_G_W3_Friction.html",
    "Science_Teesside/Grow/SCI_G_W4_Mechanisms.html",
    "Science_Teesside/Grow/SCI_G_W5_Fair_Test.html",
    "Science_Teesside/Grow/SCI_G_W6_Earth_And_Planets.html",
    "Science_Teesside/Grow/SCI_G_W7_The_Moon.html",
]
HTML_TARGETS = [WAVE, GRID, DIGESTION, INDEX, *MOTION]
EXPECTED_CHANGED = sorted([*HTML_TARGETS, "assets/video/poster-art.svg"])
SEVERE_HTML5_CODES = {
    "duplicate-attribute",
    "expected-closing-tag-but-got-eof",
    "eof-in-element-that-can-contain-only-text",
    "unexpected-null-character",
    "invalid-codepoint",
    "invalid-character-in-attribute-name",
    "unexpected-character-in-unquoted-attribute-value",
    "unexpected-end-tag",
    "end-tag-too-early",
}


@dataclasses.dataclass(slots=True)
class Finding:
    severity: str
    path: str
    message: str
    details: Any = None

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class Validator:
    def __init__(self, repo: pathlib.Path, site_root: pathlib.Path, output: pathlib.Path) -> None:
        self.repo = repo.resolve()
        self.site_root = site_root.resolve()
        self.output = output.resolve()
        self.findings: list[Finding] = []
        self.browser_results: list[dict[str, Any]] = []

    def error(self, path: str, message: str, details: Any = None) -> None:
        self.findings.append(Finding("error", path, message, details))

    def warning(self, path: str, message: str, details: Any = None) -> None:
        self.findings.append(Finding("warning", path, message, details))

    def run(self, browser: bool) -> int:
        self.output.mkdir(parents=True, exist_ok=True)
        self._check_changed_paths()
        self._parse_targets()
        self._check_specific_invariants()
        self._check_svg()
        if browser:
            self._browser_smoke()
        self._write_outputs()
        return 1 if any(item.severity == "error" for item in self.findings) else 0

    def _check_changed_paths(self) -> None:
        proc = subprocess.run(
            ["git", "diff", "--name-only", BASE, "--"],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode:
            self.error("<worktree>", "Could not enumerate applied changes", proc.stderr.strip())
            return
        actual = sorted(line for line in proc.stdout.splitlines() if line.strip())
        if actual != EXPECTED_CHANGED:
            self.error("<worktree>", "Changed-path allowlist mismatch", {"expected": EXPECTED_CHANGED, "actual": actual})
        check = subprocess.run(
            ["git", "diff", "--check", BASE, "--"],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if check.returncode:
            self.error("<worktree>", "Applied diff fails git diff --check", check.stdout.strip())

    def _parse_targets(self) -> None:
        for rel in HTML_TARGETS:
            path = self.repo / rel
            if not path.is_file():
                self.error(rel, "Expected HTML target is missing")
                continue
            text = path.read_text(encoding="utf-8")
            parser = html5lib.HTMLParser(tree=html5lib.getTreeBuilder("etree"), namespaceHTMLElements=False)
            try:
                document = parser.parse(text)
            except Exception as exc:
                self.error(rel, "HTML parser failed", f"{type(exc).__name__}: {exc}")
                continue
            severe = [
                {"position": position, "code": code, "data": data}
                for position, code, data in parser.errors
                if code in SEVERE_HTML5_CODES
            ]
            if severe:
                self.error(rel, "Severe HTML5 parse findings remain", severe)
            ids: list[str] = []
            for element in document.iter():
                value = element.attrib.get("id")
                if value:
                    ids.append(value)
                if str(element.tag).split("}")[-1].lower() == "style":
                    css = "".join(element.itertext())
                    errors = [
                        getattr(token, "message", "CSS parse error")
                        for token in tinycss2.parse_stylesheet(css, skip_comments=False, skip_whitespace=False)
                        if getattr(token, "type", None) == "error"
                    ]
                    if errors:
                        self.error(rel, "CSS parse errors remain in an actual <style> block", errors)
            duplicates = sorted(name for name, count in Counter(ids).items() if count > 1)
            if duplicates:
                self.error(rel, "Duplicate IDs remain", duplicates)

    def _check_specific_invariants(self) -> None:
        wave = (self.repo / WAVE).read_text(encoding="utf-8")
        if wave.count('onclick="fireLessonComplete()"') < 1:
            self.error(WAVE, "Lesson-complete control disappeared while fixing structure")

        grid = (self.repo / GRID).read_text(encoding="utf-8")
        if 'id="title"' in grid:
            self.error(GRID, "Duplicate title ID selector remains")
        if grid.count('class="panel-title"') != 3:
            self.error(GRID, "Expected three panel-title elements", grid.count('class="panel-title"'))
        for control_id in ("seed-input", "initials-input", "share-str"):
            match = re.search(rf"<input\b[^>]*\bid=\"{re.escape(control_id)}\"[^>]*>", grid, re.I)
            if not match or not re.search(r"\b(?:aria-label|name)=", match.group(0), re.I):
                self.error(GRID, f"Input {control_id} still lacks an explicit accessible name")
        if "wght@500;700;900&display=swap" in grid:
            self.error(GRID, "Raw ampersand remains in Google Fonts URL")

        digestion = (self.repo / DIGESTION).read_text(encoding="utf-8")
        if 'id="indep-timer-display"' in digestion:
            self.error(DIGESTION, "Old duplicate timer ID remains")
        if digestion.count('class="indep-timer-display"') != 2:
            self.error(DIGESTION, "Expected two timer displays", digestion.count('class="indep-timer-display"'))
        if "querySelectorAll('.indep-timer-display')" not in digestion:
            self.error(DIGESTION, "Timer renderer does not update both displays")
        if not digestion.rstrip().lower().endswith("</html>"):
            self.error(DIGESTION, "Content still exists after the closing html element")
        memory = digestion.find('<div class="memory-trick">Amylase Makes Maltose')
        body_close = digestion.lower().rfind("</body>")
        if memory < 0 or body_close < 0 or memory > body_close:
            self.error(DIGESTION, "Memory trick was not moved inside the document body")

        index = (self.repo / INDEX).read_text(encoding="utf-8")
        if 'src="assets/video/poster-art.svg"' not in index:
            self.error(INDEX, "Lesson Hub does not reference the repository-local SVG poster")
        if "/assets/video/poster-art.jpg" in index:
            self.error(INDEX, "Missing root-site JPG poster reference remains")

        for rel in MOTION:
            text = (self.repo / rel).read_text(encoding="utf-8")
            if "url(#g-mblur)" in text:
                self.error(rel, "Undefined SVG motion-blur filter reference remains")
            if ".g-blur-fast { filter: blur(.8px); }" not in text:
                self.error(rel, "CSS blur fallback was removed")

    def _check_svg(self) -> None:
        svg = self.repo / "assets/video/poster-art.svg"
        if not svg.is_file():
            self.error("assets/video/poster-art.svg", "Proposed poster asset is missing")
            return
        try:
            root = ET.parse(svg).getroot()
        except Exception as exc:
            self.error("assets/video/poster-art.svg", "Poster SVG is not well formed", str(exc))
            return
        if not root.tag.lower().endswith("svg"):
            self.error("assets/video/poster-art.svg", "Poster asset has no SVG root")
        ids = [element.attrib["id"] for element in root.iter() if element.attrib.get("id")]
        duplicates = [name for name, count in Counter(ids).items() if count > 1]
        if duplicates:
            self.error("assets/video/poster-art.svg", "Poster SVG has duplicate IDs", duplicates)

    def _browser_smoke(self) -> None:
        try:
            from selenium import webdriver  # type: ignore
        except Exception as exc:
            self.error("<browser>", "Selenium is unavailable", str(exc))
            return
        server = CombinedServer(self.repo, self.site_root)
        server.start()
        driver = None
        try:
            options = webdriver.ChromeOptions()
            for arg in (
                "--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
                "--disable-background-networking", "--disable-component-update", "--disable-default-apps",
                "--disable-features=Translate,BackForwardCache", "--window-size=1440,1000",
                "--remote-allow-origins=*", "--no-first-run",
            ):
                options.add_argument(arg)
            options.set_capability("goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"})
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(20)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": ERROR_HOOK})
            for mode in ("desktop", "mobile-reduced"):
                self._set_mode(driver, mode)
                for rel in HTML_TARGETS:
                    result: dict[str, Any] = {"path": rel, "mode": mode, "errors": [], "warnings": []}
                    try:
                        with contextlib.suppress(Exception):
                            driver.get_log("browser")
                            driver.get_log("performance")
                        url = f"{server.origin}/Lessons/{urllib.parse.quote(rel, safe='/')}"
                        driver.get(url)
                        time.sleep(0.45)
                        hook = driver.execute_script("return window.__fixPackErrors || []") or []
                        for entry in hook:
                            text = str(entry)
                            if text.startswith("resource:") and server.origin not in text:
                                result["warnings"].append(text[:1000])
                            else:
                                result["errors"].append(text[:1000])
                        for entry in driver.get_log("browser"):
                            message = str(entry.get("message", ""))
                            if str(entry.get("level", "")).upper() == "SEVERE" and "Failed to load resource" not in message:
                                result["errors"].append(message[:1000])
                        for entry in driver.get_log("performance"):
                            try:
                                payload = json.loads(entry["message"])["message"]
                                if payload.get("method") != "Network.responseReceived":
                                    continue
                                response = payload["params"]["response"]
                                status = int(response.get("status", 0))
                                resource_url = str(response.get("url", ""))
                                if status >= 400 and resource_url.startswith(server.origin) and not resource_url.endswith("/favicon.ico"):
                                    result["errors"].append(f"HTTP {status}: {resource_url}")
                            except Exception:
                                continue
                        text_len = driver.execute_script("return document.body ? (document.body.innerText || '').trim().length : 0")
                        renderable = driver.execute_script("return !!document.querySelector('canvas,svg,img,video,iframe')")
                        if not text_len and not renderable:
                            result["errors"].append("No visible text or renderable surface")
                    except Exception as exc:
                        result["errors"].append(f"{type(exc).__name__}: {exc}")
                    result["status"] = "fail" if result["errors"] else "pass"
                    self.browser_results.append(result)
                    if result["errors"]:
                        self.error(rel, f"Browser smoke failed in {mode}", result["errors"])
                    with contextlib.suppress(Exception):
                        driver.execute_script("try{localStorage.clear();sessionStorage.clear();}catch(e){}")
        except Exception as exc:
            self.error("<browser>", "Chrome session failed", f"{type(exc).__name__}: {exc}")
        finally:
            if driver is not None:
                with contextlib.suppress(Exception):
                    driver.quit()
            server.stop()

    @staticmethod
    def _set_mode(driver: Any, mode: str) -> None:
        mobile = "mobile" in mode
        driver.execute_cdp_cmd("Emulation.setEmulatedMedia", {
            "media": "screen",
            "features": [{"name": "prefers-reduced-motion", "value": "reduce" if "reduced" in mode else "no-preference"}],
        })
        if mobile:
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390, "height": 844, "deviceScaleFactor": 3, "mobile": True,
                "screenWidth": 390, "screenHeight": 844,
            })
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
            driver.set_window_size(390, 844)
        else:
            with contextlib.suppress(Exception):
                driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {"enabled": False})
            driver.set_window_size(1440, 1000)

    def _write_outputs(self) -> None:
        summary = {
            "base": BASE,
            "expected_changed_paths": EXPECTED_CHANGED,
            "html_targets": HTML_TARGETS,
            "browser_result_count": len(self.browser_results),
            "browser_status_counts": dict(Counter(result.get("status") for result in self.browser_results)),
            "finding_counts": dict(Counter(item.severity for item in self.findings)),
            "findings": [item.as_dict() for item in self.findings],
        }
        (self.output / "validation-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (self.output / "browser-results.json").write_text(json.dumps(self.browser_results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        lines = [
            "# Proposed fix-pack validation",
            "",
            f"- Base: `{BASE}`",
            f"- Expected changed paths: **{len(EXPECTED_CHANGED)}**",
            f"- HTML pages parsed: **{len(HTML_TARGETS)}**",
            f"- Browser executions: **{len(self.browser_results)}**",
            f"- Errors: **{sum(item.severity == 'error' for item in self.findings)}**",
            f"- Warnings: **{sum(item.severity == 'warning' for item in self.findings)}**",
            "",
        ]
        if self.findings:
            lines.extend(["| Severity | Path | Finding |", "|---|---|---|"])
            for item in self.findings:
                lines.append(f"| {item.severity.upper()} | `{item.path}` | {item.message.replace('|', '\\|')} |")
        else:
            lines.append("All exact-application, structural, defect-specific and browser checks passed.")
        (self.output / "VALIDATION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


class Handler(http.server.SimpleHTTPRequestHandler):
    lessons_root: pathlib.Path
    site_root: pathlib.Path

    def translate_path(self, path: str) -> str:
        decoded = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        if decoded.startswith("/Lessons/"):
            root = self.lessons_root
            relative = decoded[len("/Lessons/"):]
        else:
            root = self.site_root
            relative = decoded.lstrip("/")
        parts = [part for part in posixpath.normpath(relative).split("/") if part not in {"", ".", ".."}]
        return str(root.joinpath(*parts))

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


class CombinedServer:
    def __init__(self, lessons_root: pathlib.Path, site_root: pathlib.Path) -> None:
        handler = type("FixPackHandler", (Handler,), {"lessons_root": lessons_root, "site_root": site_root})
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.origin = f"http://127.0.0.1:{self.httpd.server_port}"

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)


ERROR_HOOK = r"""
(() => {
  window.__fixPackErrors = [];
  const push = (kind, value) => {
    const text = typeof value === 'string' ? value : (value && (value.stack || value.message)) || String(value);
    window.__fixPackErrors.push(`${kind}: ${text}`.slice(0, 2000));
  };
  window.addEventListener('error', event => {
    const target = event.target;
    if (target && target !== window && target !== document) {
      const url = target.currentSrc || target.src || target.href || '(unknown URL)';
      push('resource', url);
      return;
    }
    push('error', event.error || event.message || 'unknown window error');
  }, true);
  window.addEventListener('unhandledrejection', event => push('unhandledrejection', event.reason), true);
})();
"""


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--site-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--browser", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    validator = Validator(pathlib.Path(args.repo), pathlib.Path(args.site_root), pathlib.Path(args.output))
    return validator.run(args.browser)


if __name__ == "__main__":
    raise SystemExit(main())
