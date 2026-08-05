#!/usr/bin/env python3
"""Browser checks for ASDAN visual-learning payloads and integrated lessons."""
from __future__ import annotations
import argparse, json, os, sys, tempfile, threading
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

TOOLKIT = Path(__file__).resolve().parent
PAYLOADS = json.loads((TOOLKIT / "lesson-payloads.json").read_text(encoding="utf-8"))
CSS = (TOOLKIT / "asdan-visual-learning.css").read_text(encoding="utf-8")
CORE = (TOOLKIT / "asdan-visual-learning.js").read_text(encoding="utf-8")
REGISTRY = json.dumps(PAYLOADS, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet": {"width": 1024, "height": 768},
    "mobile": {"width": 390, "height": 844},
}

def harness_html() -> str:
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ASDAN visual browser harness</title>
<style>body{{font-family:Arial,sans-serif;margin:0;padding:18px;background:#f4f1ea;color:#17212a}}main{{max-width:1180px;margin:auto}}</style>
<style>{CSS}</style>
<script>
const _slug = new URLSearchParams(location.search).get('slug');
if (_slug) document.documentElement.dataset.asdanLesson = _slug;
window.ASDANVisualPayloads = {REGISTRY};
</script>
</head><body><main><h1>Browser harness</h1></main><script>{CORE}</script></body></html>"""

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

def start_server(root: Path):
    handler = partial(QuietHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"

def mount_harness_payload(page, slug: str) -> None:
    page.evaluate(
        """slug => {
          const main=document.querySelector('main');
          main.replaceChildren();
          const heading=document.createElement('h1');
          heading.textContent='Browser harness';
          main.append(heading);
          window.ASDANVisualLearning.mountPayload(window.ASDANVisualPayloads[slug], main);
        }""",
        slug,
    )

def click_prediction(page) -> None:
    choices = page.locator(".asvl-choice")
    if choices.count():
        choices.first.evaluate("(e)=>e.click()")

def complete_activity(page, payload: dict) -> None:
    activity = payload["activity"]
    kind = activity["type"]
    panel = page.locator(f'[data-asdan-visual-learning="{payload["slug"]}"]')
    if kind == "sort":
        for item in activity["items"]:
            panel.locator(f'.asvl-sort-item[data-item-id="{item["id"]}"]').evaluate("(e)=>e.click()")
            panel.locator(f'.asvl-sort-target[data-category-id="{item["answer"]}"] .asvl-target-button').evaluate("(e)=>e.click()")
    elif kind == "sequence":
        expected = [step["id"] for step in activity["steps"]]
        for target_index, step_id in enumerate(expected):
            while True:
                current = page.evaluate(
                    """({slug,id}) => {
                      const p=document.querySelector(`[data-asdan-visual-learning="${slug}"]`);
                      return p.__asdanVisualState.sequence.indexOf(id);
                    }""",
                    {"slug": payload["slug"], "id": step_id},
                )
                if current <= target_index:
                    break
                panel.locator(".asvl-sequence-row").nth(current).locator("button").first.evaluate("(e)=>e.click()")
        panel.locator(".asvl-check").evaluate("(e)=>e.click()")
    elif kind == "evidence":
        for statement in activity["statements"]:
            if statement["correct"]:
                panel.locator(f'.asvl-evidence-card[data-statement-id="{statement["id"]}"]').evaluate("(e)=>e.click()")
        panel.locator(".asvl-check").evaluate("(e)=>e.click()")
    elif kind == "hotspot":
        buttons = panel.locator(".asvl-hotspot-button")
        for index in range(buttons.count()):
            buttons.nth(index).evaluate("(e)=>e.click()")
    elif kind == "model":
        panel.locator(".asvl-run").evaluate("(e)=>e.click()")
        for _ in range(1, int(activity["requiredRuns"])):
            select = panel.locator(".asvl-model-control select").first
            values = select.locator("option").evaluate_all("(nodes)=>nodes.map(n=>n.value)")
            current = select.input_value()
            replacement = next(value for value in values if value != current)
            select.select_option(replacement)
            panel.locator(".asvl-run").evaluate("(e)=>e.click()")
    else:
        raise AssertionError(f"Unsupported activity type: {kind}")

def finish_pathway(page, payload: dict) -> None:
    panel = page.locator(f'[data-asdan-visual-learning="{payload["slug"]}"]')
    open_button = panel.locator(".asvl-open-explanation")
    if payload["pathway"] == "LAUNCH":
        if open_button.is_enabled():
            raise AssertionError("LAUNCH explanation unlocked before the structured locator.")
        groups = panel.locator(".asvl-locator-group")
        if groups.count() != 3:
            raise AssertionError("LAUNCH structured locator does not contain three groups.")
        for index in range(3):
            groups.nth(index).locator("input").first.evaluate("(e)=>e.click()")
        if not open_button.is_enabled():
            raise AssertionError("LAUNCH explanation did not unlock after all locator choices.")
    open_button.evaluate("(e)=>e.click()")
    if payload["pathway"] == "LAUNCH":
        marker = panel.get_attribute("data-asdan-opened-by")
        if marker != "completed activity and selected structured evidence-locator route":
            raise AssertionError(f"LAUNCH provenance marker incorrect: {marker!r}")
    panel.locator(".asvl-transfer-button").evaluate("(e)=>e.click()")
    if not panel.locator(".asvl-transfer").is_visible():
        raise AssertionError("Independent handover did not become visible.")

def page_checks(page, payload: dict, exercise: bool, check_static: bool = False) -> dict:
    slug = payload["slug"]
    panel = page.locator(f'[data-asdan-visual-learning="{slug}"]')
    panel.wait_for(state="visible", timeout=7000)
    if panel.get_attribute("data-asdan-visual-ready") != "true":
        raise AssertionError("Panel ready marker missing.")
    count = page.locator(f'[data-asdan-visual-learning="{slug}"]').count()
    if count != 1:
        raise AssertionError(f"Expected one panel, found {count}.")
    overflow = page.evaluate(
        """slug => {
          const p=document.querySelector(`[data-asdan-visual-learning="${slug}"]`);
          const r=p.getBoundingClientRect();
          return {panel:r.width, scroll:p.scrollWidth, body:document.documentElement.scrollWidth, viewport:innerWidth};
        }""",
        slug,
    )
    if overflow["scroll"] > overflow["panel"] + 3:
        raise AssertionError(f"Panel horizontal overflow: {overflow}.")
    if overflow["body"] > overflow["viewport"] + 3:
        raise AssertionError(f"Page horizontal overflow: {overflow}.")
    if not panel.locator(".asvl-route").is_visible():
        raise AssertionError("Teacher/access route missing.")
    notice = panel.locator(".asvl-notice").inner_text()
    if "Nothing is saved" not in notice or "portfolio" not in notice:
        raise AssertionError("Rehearsal-only notice incomplete.")
    if check_static:
        panel.locator(".asvl-static-toggle").evaluate("(e)=>e.click()")
        if panel.get_attribute("class").find("asvl-static") < 0:
            raise AssertionError("Static mode did not apply.")
        panel.locator(".asvl-static-toggle").evaluate("(e)=>e.click()")
    if exercise:
        click_prediction(page)
        complete_activity(page, payload)
        state = page.evaluate(
            """slug => document.querySelector(`[data-asdan-visual-learning="${slug}"]`).__asdanVisualState.completed""",
            slug,
        )
        if not state:
            raise AssertionError("Activity did not complete.")
        finish_pathway(page, payload)
        panel.locator(".asvl-reset").evaluate("(e)=>e.click()")
        reset_state = page.evaluate(
            """slug => {
              const s=document.querySelector(`[data-asdan-visual-learning="${slug}"]`).__asdanVisualState;
              return {completed:s.completed,prediction:s.prediction,runs:s.runs.length,transfer:s.transferOpen};
            }""",
            slug,
        )
        if reset_state != {"completed": False, "prediction": None, "runs": 0, "transfer": False}:
            raise AssertionError(f"Reset state is not clean: {reset_state}.")
    return overflow

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="Integrated Lessons checkout. If omitted, use the standalone harness.")
    parser.add_argument("--evidence-dir", default=str(TOOLKIT / "_browser-evidence"))
    parser.add_argument("--chromium", default=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"))
    parser.add_argument("--mount-only", action="store_true", help="Skip full activity completion.")
    args = parser.parse_args()

    evidence = Path(args.evidence_dir).resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    harness = evidence / "harness.html"
    harness.write_text(harness_html(), encoding="utf-8")
    errors: list[str] = []
    measurements: list[dict] = []
    console_errors: list[str] = []

    server = None
    base_url = None
    if args.repo:
        server, base_url = start_server(Path(args.repo).resolve())

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, executable_path=args.chromium)
            for viewport_name, viewport in VIEWPORTS.items():
                page = browser.new_page(viewport=viewport, reduced_motion="reduce" if viewport_name == "tablet" else "no-preference")
                page.on("console", lambda message, n=viewport_name: console_errors.append(f"{n}: {message.text}") if message.type == "error" else None)
                page.on("pageerror", lambda error, n=viewport_name: console_errors.append(f"{n}: PAGEERROR {error}"))
                if not args.repo:
                    page.set_content(harness_html(), wait_until="load")
                for index, payload in enumerate(PAYLOADS.values(), 1):
                    try:
                        if args.repo:
                            rel = quote(payload["path"], safe="/")
                            page.goto(f"{base_url}/{rel}", wait_until="load", timeout=15000)
                        else:
                            mount_harness_payload(page, payload["slug"])
                        exercise = not args.mount_only and viewport_name == "desktop"
                        metrics = page_checks(page, payload, exercise, check_static=(index == 1))
                        measurements.append({"viewport": viewport_name, "slug": payload["slug"], **metrics})
                        if index % 10 == 0 or index == len(PAYLOADS):
                            print(f"{viewport_name}: {index}/{len(PAYLOADS)}", flush=True)
                        if index in {1, len(PAYLOADS)//2, len(PAYLOADS)} and viewport_name == "desktop":
                            page.screenshot(path=str(evidence / f"{index:02d}-{payload['slug']}.png"), full_page=True)
                    except Exception as exc:
                        errors.append(f"{viewport_name} · {payload['slug']}: {exc}")
                page.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
            server.server_close()

    result = {
        "payloads": len(PAYLOADS),
        "viewports": VIEWPORTS,
        "pageChecks": len(measurements),
        "fullActivityChecks": 0 if args.mount_only else len(PAYLOADS),
        "errors": errors,
        "consoleErrors": console_errors,
    }
    (evidence / "browser-results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (evidence / "measurements.json").write_text(json.dumps(measurements, indent=2) + "\n", encoding="utf-8")

    if console_errors:
        errors.extend(f"console: {entry}" for entry in console_errors)
    if errors:
        print(f"FAILED · {len(errors)} browser errors", file=sys.stderr)
        for error in errors[:50]:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"PASS · {len(PAYLOADS)} payloads × {len(VIEWPORTS)} viewports = {len(measurements)} mount/layout checks")
    if not args.mount_only:
        print(f"PASS · {len(PAYLOADS)} full desktop pathway completions, explanation gates, transfers and resets")
    print(f"Evidence: {evidence}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
