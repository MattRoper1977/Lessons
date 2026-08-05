#!/usr/bin/env python3
"""Validate lesson-payloads.json and regenerate lesson-payloads.js."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_PATH = ROOT / "lesson-payloads.json"
JS_PATH = ROOT / "lesson-payloads.js"
PATHWAYS = {"BUILD", "GROW", "LAUNCH"}
ACTIVITIES = {"sort", "sequence", "evidence", "hotspot", "model"}

def canonical_without_hash(payload: dict) -> str:
    clean = dict(payload)
    clean.pop("payloadSha256", None)
    return json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Top-level payload file must be an object keyed by lesson slug."]
    if len(data) != 85:
        errors.append(f"Expected 85 lessons; found {len(data)}.")
    seen_paths: set[str] = set()
    for slug, payload in data.items():
        prefix = f"{slug}: "
        if payload.get("slug") != slug:
            errors.append(prefix + "payload slug does not match key.")
        if payload.get("pathway") not in PATHWAYS:
            errors.append(prefix + "invalid pathway.")
        path = payload.get("path")
        if not isinstance(path, str) or not path.endswith(".html"):
            errors.append(prefix + "invalid lesson path.")
        elif path in seen_paths:
            errors.append(prefix + "duplicate lesson path.")
        else:
            seen_paths.add(path)
        for field in ("lessonTitle", "targetTitle", "title", "purpose", "independent", "panelNotice", "imageBrief", "mediaKey"):
            if not isinstance(payload.get(field), str) or not payload[field].strip():
                errors.append(prefix + f"missing or empty {field}.")
        if len(payload.get("pathwayCycle", [])) != 4:
            errors.append(prefix + "pathwayCycle must contain four stages.")
        if len(payload.get("independenceSteps", [])) != 4:
            errors.append(prefix + "independenceSteps must contain four stages.")
        if len(payload.get("helpLadder", [])) < 4:
            errors.append(prefix + "helpLadder must contain at least four routes.")
        activity = payload.get("activity", {})
        activity_type = activity.get("type")
        if activity_type not in ACTIVITIES:
            errors.append(prefix + f"unsupported activity type {activity_type!r}.")
        if not activity.get("prompt") or not activity.get("completion"):
            errors.append(prefix + "activity requires prompt and completion.")
        if payload.get("pathway") in {"GROW", "LAUNCH"} and not activity.get("predictionOptions"):
            errors.append(prefix + "GROW/LAUNCH requires predictionOptions.")
        if activity_type == "sort":
            if not activity.get("categories") or not activity.get("items"):
                errors.append(prefix + "sort requires categories and items.")
        elif activity_type == "sequence":
            if len(activity.get("steps", [])) < 3:
                errors.append(prefix + "sequence requires at least three steps.")
        elif activity_type == "evidence":
            statements = activity.get("statements", [])
            if not statements or not any(item.get("correct") for item in statements) or not any(not item.get("correct") for item in statements):
                errors.append(prefix + "evidence requires correct and distractor statements.")
        elif activity_type == "hotspot":
            if len(activity.get("hotspots", [])) < 3:
                errors.append(prefix + "hotspot requires at least three points.")
        elif activity_type == "model":
            if not activity.get("controls") or not activity.get("outcomes"):
                errors.append(prefix + "model requires controls and outcomes.")
            required = int(activity.get("requiredRuns", 0))
            expected = 1 if payload.get("pathway") == "BUILD" else 2
            if required < expected:
                errors.append(prefix + f"model requires at least {expected} frozen run(s).")
        if payload.get("pathway") == "LAUNCH":
            locator = payload.get("locator", {})
            if not all(locator.get(key) for key in ("evidenceForms", "locations", "routes")):
                errors.append(prefix + "LAUNCH requires all three structured evidence locator groups.")
        expected_hash = hashlib.sha256(canonical_without_hash(payload).encode("utf-8")).hexdigest()
        if payload.get("payloadSha256") != expected_hash:
            errors.append(prefix + "payloadSha256 does not match canonical payload.")
    return errors

def render_js(data: dict) -> str:
    compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return "/* Generated from lesson-payloads.json. Edit JSON and run build_payloads.py. */\nwindow.ASDANVisualPayloads = " + compact + ";\n"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate and verify generated JS without writing.")
    args = parser.parse_args()
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    errors = validate(data)
    expected = render_js(data)
    if JS_PATH.exists() and JS_PATH.read_text(encoding="utf-8") != expected:
        errors.append("lesson-payloads.js is not the exact generated form of lesson-payloads.json.")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    if not args.check:
        JS_PATH.write_text(expected, encoding="utf-8")
    counts = {pathway: sum(1 for payload in data.values() if payload["pathway"] == pathway) for pathway in sorted(PATHWAYS)}
    print(f"PASS · {len(data)} lesson payloads validated · " + " · ".join(f"{key} {value}" for key, value in counts.items()))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
