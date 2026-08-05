#!/usr/bin/env python3
"""Static integrity checks for the ASDAN visual-learning toolkit."""
from __future__ import annotations
import hashlib, json, re, sys, xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAYLOADS = json.loads((ROOT / "lesson-payloads.json").read_text(encoding="utf-8"))
CORE = (ROOT / "asdan-visual-learning.js").read_text(encoding="utf-8")
CSS = (ROOT / "asdan-visual-learning.css").read_text(encoding="utf-8")
SVG_DIR = ROOT / "assets" / "svg"
DOCS = ROOT / "docs"

EXPECTED_PATHWAYS = {"BUILD": 37, "GROW": 18, "LAUNCH": 30}
EXPECTED_SUBSECTIONS = {
    ("BUILD", "Careers"): 7,
    ("BUILD", "Living Independently"): 6,
    ("BUILD", "FoodWise"): 6,
    ("BUILD", "Community Project"): 6,
    ("BUILD", "Duke & Enterprise"): 6,
    ("BUILD", "D&T Community Upcycling"): 6,
    ("GROW", "PEQ"): 6,
    ("GROW", "Community Project"): 6,
    ("GROW", "Enterprise"): 6,
    ("LAUNCH", "PEQ"): 6,
    ("LAUNCH", "Careers"): 6,
    ("LAUNCH", "Living Independently"): 6,
    ("LAUNCH", "Vocational"): 6,
    ("LAUNCH", "Community & Enterprise"): 6,
}
REQUIRED_DOCS = {
    "DEEP_AUDIT_AND_DESIGN_REPORT.md",
    "LESSON_UPGRADE_MAP.md",
    "ACTIVITY_PATTERN_LIBRARY.md",
    "MEDIA_REGISTER.md",
    "IMAGE_AND_SVG_REGISTER.md",
    "DATA_EVIDENCE_AND_ASSESSMENT_FIREWALL.md",
    "ESTATE_SCOPE_AND_INTEGRATION_ARCHITECTURE.md",
    "INDEPENDENCE_DESIGN_STANDARD.md",
    "TEST_PLAN.md",
}
PROHIBITED_JS = {
    "localStorage": r"\blocalStorage\b",
    "sessionStorage": r"\bsessionStorage\b",
    "indexedDB": r"\bindexedDB\b",
    "cookies": r"document\.cookie",
    "fetch": r"\bfetch\s*\(",
    "XMLHttpRequest": r"\bXMLHttpRequest\b",
    "WebSocket": r"\bWebSocket\b",
    "sendBeacon": r"\bsendBeacon\b",
    "media devices": r"\bgetUserMedia\b|\bmediaDevices\b",
    "geolocation": r"\bgeolocation\b",
    "clipboard write": r"\bclipboard\.write",
    "file input": r"type\s*=\s*['\"]file",
    "textarea creation": r"createElement\(\s*['\"]textarea",
}

def canonical_without_hash(payload: dict) -> str:
    clean = dict(payload)
    clean.pop("payloadSha256", None)
    return json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def fail(errors: list[str], message: str) -> None:
    errors.append(message)

def main() -> int:
    errors: list[str] = []
    if len(PAYLOADS) != 85:
        fail(errors, f"Expected 85 payloads, found {len(PAYLOADS)}.")

    pathway_counts = Counter(payload.get("pathway") for payload in PAYLOADS.values())
    if dict(pathway_counts) != EXPECTED_PATHWAYS:
        fail(errors, f"Pathway counts moved: {dict(pathway_counts)}.")

    subsection_counts = Counter((payload.get("pathway"), payload.get("subsection")) for payload in PAYLOADS.values())
    if dict(subsection_counts) != EXPECTED_SUBSECTIONS:
        missing = set(EXPECTED_SUBSECTIONS.items()) ^ set(subsection_counts.items())
        fail(errors, f"Subsection counts moved: {sorted(missing)}.")

    paths: set[str] = set()
    activity_counts = Counter()
    for slug, payload in PAYLOADS.items():
        if payload.get("slug") != slug:
            fail(errors, f"{slug}: slug mismatch.")
        path = payload.get("path")
        if path in paths:
            fail(errors, f"{slug}: duplicate path {path}.")
        paths.add(path)
        activity = payload.get("activity", {})
        activity_counts[activity.get("type")] += 1
        expected_hash = hashlib.sha256(canonical_without_hash(payload).encode("utf-8")).hexdigest()
        if payload.get("payloadSha256") != expected_hash:
            fail(errors, f"{slug}: payload hash moved.")
        if payload.get("rehearsalOnly") is not True:
            fail(errors, f"{slug}: rehearsalOnly must be true.")
        if payload.get("pathway") in {"GROW", "LAUNCH"} and not activity.get("predictionOptions"):
            fail(errors, f"{slug}: prediction gate missing.")
        if activity.get("type") == "model":
            minimum = 1 if payload.get("pathway") == "BUILD" else 2
            if int(activity.get("requiredRuns", 0)) < minimum:
                fail(errors, f"{slug}: model run floor is {minimum}.")
        if payload.get("pathway") == "LAUNCH":
            locator = payload.get("locator", {})
            for key in ("evidenceForms", "locations", "routes"):
                if not locator.get(key):
                    fail(errors, f"{slug}: locator group {key} missing.")
            labels = " ".join(item["label"].lower() for group in locator.values() for item in group)
            if "not yet" not in labels:
                fail(errors, f"{slug}: honest not-yet route missing.")
        svg_path = SVG_DIR / f"{slug}.svg"
        if not svg_path.is_file():
            fail(errors, f"{slug}: SVG missing.")
            continue
        try:
            root = ET.parse(svg_path).getroot()
        except ET.ParseError as exc:
            fail(errors, f"{slug}: SVG parse failure: {exc}.")
            continue
        if root.attrib.get("viewBox") != "0 0 1200 675":
            fail(errors, f"{slug}: SVG viewBox moved.")
        ns = {"svg": "http://www.w3.org/2000/svg"}
        if root.find("svg:title", ns) is None or root.find("svg:desc", ns) is None:
            fail(errors, f"{slug}: SVG requires title and desc.")

    if len(list(SVG_DIR.glob("*.svg"))) != 85:
        fail(errors, f"Expected exactly 85 SVGs, found {len(list(SVG_DIR.glob('*.svg')))}.")

    for label, pattern in PROHIBITED_JS.items():
        if re.search(pattern, CORE, re.I):
            fail(errors, f"Core JavaScript contains prohibited {label} API/control.")

    required_strings = [
        "Rehearsal only",
        "dataset.asdanOpenedBy",
        "completed activity and selected structured evidence-locator route",
        "Teacher, assessor and access route",
        "not an evidence judgement",
    ]
    for text in required_strings:
        if text not in CORE and text not in json.dumps(PAYLOADS, ensure_ascii=False):
            fail(errors, f"Required firewall text/behaviour missing: {text}.")

    if "@media print" not in CSS or ".asvl-panel{display:none!important}" not in CSS.replace(" ", ""):
        fail(errors, "Print suppression rule missing.")
    if "prefers-reduced-motion" not in CSS:
        fail(errors, "Reduced-motion rule missing.")

    missing_docs = sorted(name for name in REQUIRED_DOCS if not (DOCS / name).is_file())
    if missing_docs:
        fail(errors, f"Required documents missing: {missing_docs}.")

    for doc_name in ("LESSON_UPGRADE_MAP.md", "MEDIA_REGISTER.md", "IMAGE_AND_SVG_REGISTER.md"):
        text = (DOCS / doc_name).read_text(encoding="utf-8")
        missing = [slug for slug in PAYLOADS if slug not in text]
        if missing:
            fail(errors, f"{doc_name}: {len(missing)} lesson slugs missing.")

    print("ASDAN visual-learning static check")
    print(f"  payloads: {len(PAYLOADS)}")
    print("  pathways: " + " · ".join(f"{key} {pathway_counts[key]}" for key in ("BUILD", "GROW", "LAUNCH")))
    print("  subsections: 14")
    print("  activities: " + " · ".join(f"{key} {activity_counts[key]}" for key in sorted(activity_counts)))
    print(f"  accessible SVGs: {len(list(SVG_DIR.glob('*.svg')))}")
    print(f"  protected API patterns: {len(PROHIBITED_JS)}")
    if errors:
        print("\nFAILED")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("\nPASS · toolkit structure, payloads, firewall and SVG accessibility at expected counts")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
