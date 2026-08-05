from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "estate_audit.py"
SPEC = importlib.util.spec_from_file_location("estate_audit", SCRIPT)
assert SPEC and SPEC.loader
estate_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = estate_audit
SPEC.loader.exec_module(estate_audit)


class EstateAuditInstrumentTests(unittest.TestCase):
    def make_audit(self, root: pathlib.Path) -> object:
        site = root / "site"
        site.mkdir(exist_ok=True)
        return estate_audit.Audit(root, site, root / "out", False, "origin/main")

    def test_module_script_attribute_order_is_irrelevant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            audit = self.make_audit(root)
            audit._text_cache = {
                "index.html": (
                    '<script src="first.js" type="module"></script>'
                    '<script type="module" defer src="second.js"></script>'
                    '<script src="classic.js"></script>'
                )
            }
            self.assertEqual(audit._module_script_targets(), {"first.js", "second.js"})

    def test_json_lines_reports_the_exact_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            audit = self.make_audit(root)
            audit._validate_jsonl("records.jsonl", '{"ok": true}\nnot-json\n')
            self.assertEqual(len(audit.issues), 1)
            self.assertEqual(audit.issues[0].line, 2)
            self.assertEqual(audit.issues[0].category, "json")

    def test_opendocument_and_epub_use_mimetype_not_ooxml_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            audit = self.make_audit(root)
            samples = {
                "sample.odt": "application/vnd.oasis.opendocument.text",
                "sample.ods": "application/vnd.oasis.opendocument.spreadsheet",
                "sample.odp": "application/vnd.oasis.opendocument.presentation",
                "sample.epub": "application/epub+zip",
            }
            for name, mimetype in samples.items():
                path = root / name
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("mimetype", mimetype)
                    archive.writestr("content.xml", "<document/>")
                audit._validate_zip(path, name, office=True)
            self.assertEqual([issue.as_dict() for issue in audit.issues], [])

    def test_missing_ooxml_content_types_is_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            audit = self.make_audit(root)
            path = root / "broken.docx"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("word/document.xml", "<document/>")
            audit._validate_zip(path, path.name, office=True)
            self.assertEqual(audit.blocking_count, 1)
            self.assertIn("[Content_Types].xml", audit.issues[0].message)

    def test_style_markup_inside_javascript_is_not_parsed_as_page_css(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            audit = self.make_audit(root)
            audit._validate_inline_blocks(
                "page.html",
                "<script>const markup = '<style>a{color:red;]</style>';</script>",
            )
            self.assertFalse(any(issue.category == "css" for issue in audit.issues))

            audit._validate_inline_blocks("real-style.html", "<style>a{color:red;]</style>")
            self.assertTrue(any(issue.category == "css" for issue in audit.issues))

    def test_optional_classroom_sync_failure_is_visible_but_nonblocking(self) -> None:
        def performance_log(method: str, params: dict[str, object]) -> dict[str, str]:
            return {"message": json.dumps({"message": {"method": method, "params": params}})}

        origin = "http://127.0.0.1:4321"
        result = {
            "errors": [],
            "warnings": [],
            "local_http_errors": [],
            "optional_http_failures": [],
        }
        performance = [
            performance_log(
                "Network.requestWillBeSent",
                {"requestId": "sync", "request": {"method": "POST", "url": origin + "/Lessons/app/sync.php"}},
            ),
            performance_log(
                "Network.responseReceived",
                {"requestId": "sync", "response": {"status": 501, "url": origin + "/Lessons/app/sync.php"}},
            ),
            performance_log(
                "Network.requestWillBeSent",
                {"requestId": "asset", "request": {"method": "GET", "url": origin + "/missing.png"}},
            ),
            performance_log(
                "Network.responseReceived",
                {"requestId": "asset", "response": {"status": 404, "url": origin + "/missing.png"}},
            ),
        ]
        estate_audit.Audit._classify_browser_logs(result, [], performance, origin)
        self.assertEqual(len(result["optional_http_failures"]), 1)
        self.assertEqual(result["optional_http_failures"][0]["method"], "POST")
        self.assertEqual(len(result["local_http_errors"]), 1)
        self.assertEqual(result["local_http_errors"][0]["status"], 404)
        self.assertTrue(any(warning["kind"] == "optional-http" for warning in result["warnings"]))

    def test_mobile_mode_enables_touch_emulation(self) -> None:
        class FakeDriver:
            def __init__(self) -> None:
                self.commands: list[tuple[str, dict[str, object]]] = []
                self.windows: list[tuple[int, int]] = []

            def execute_cdp_cmd(self, name: str, payload: dict[str, object]) -> None:
                self.commands.append((name, payload))

            def set_window_size(self, width: int, height: int) -> None:
                self.windows.append((width, height))

        driver = FakeDriver()
        estate_audit.Audit._configure_browser_mode(driver, "mobile-reduced")
        command_map = {name: payload for name, payload in driver.commands}
        self.assertTrue(command_map["Emulation.setDeviceMetricsOverride"]["mobile"])
        self.assertEqual(command_map["Emulation.setTouchEmulationEnabled"]["maxTouchPoints"], 5)
        self.assertEqual(driver.windows[-1], (390, 844))

    def test_desktop_mode_disables_touch_without_zero_touch_points(self) -> None:
        class FakeDriver:
            def __init__(self) -> None:
                self.commands: list[tuple[str, dict[str, object]]] = []

            def execute_cdp_cmd(self, name: str, payload: dict[str, object]) -> None:
                self.commands.append((name, payload))

            def set_window_size(self, width: int, height: int) -> None:
                return None

        driver = FakeDriver()
        estate_audit.Audit._configure_browser_mode(driver, "desktop")
        touch_payloads = [payload for name, payload in driver.commands if name == "Emulation.setTouchEmulationEnabled"]
        self.assertEqual(touch_payloads[-1], {"enabled": False})

    def test_live_fetch_retries_transient_status(self) -> None:
        transient = {"ok": False, "status": 503, "error": "temporary"}
        recovered = {"ok": True, "status": 200, "body": b"ok"}
        with mock.patch.object(estate_audit.Audit, "_fetch_url_once", side_effect=[transient, recovered]) as probe, \
             mock.patch.object(estate_audit.time, "sleep"):
            result = estate_audit.Audit._fetch_url("https://example.invalid/test", full=True)
        self.assertEqual(probe.call_count, 2)
        self.assertTrue(result["ok"])
        self.assertEqual(result["attempts"], 2)

    def test_safe_interaction_is_delegated_to_webdriver(self) -> None:
        self.assertNotIn("target.click()", estate_audit.SAFE_INTERACTION_JS)
        self.assertIn("element:target", estate_audit.SAFE_INTERACTION_JS)

    def test_download_manifest_payload_remains_json_serialisable(self) -> None:
        payload = {
            "published_ref": "origin/main",
            "paths": ["index.html", "resources.json"],
            "ok": True,
        }
        self.assertEqual(json.loads(json.dumps(payload)), payload)


if __name__ == "__main__":
    unittest.main()
