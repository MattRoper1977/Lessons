#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import re
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = Path(__file__).resolve().parent
EXPECTED_POSTER_SHA256 = "7a2caf724d81f6ff85c52eb640baf145513f704aa54dd4fd9e2cc30581493122"
JSON_TYPES = {"application/json", "application/ld+json", "importmap", "application/importmap+json"}
JS_TYPES = {"", "text/javascript", "application/javascript", "module", "text/ecmascript", "application/ecmascript"}


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new)


def patch_orbital_source(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "let seed=1, gameState='MENU';",
        "let seed=1, gameState='MENU', pauseReturnState='AIM';",
        "readable state declaration",
    )
    text = replace_once(
        text,
        "function togglePause(){ if(gameState==='AIM'||gameState==='FLY'){ gameState='PAUSE'; show('pause'); } else if(gameState==='PAUSE'){ document.getElementById('pause').classList.add('hidden'); gameState='AIM'; } }",
        "function togglePause(){ if(gameState==='AIM'||gameState==='FLY'){ pauseReturnState=gameState; gameState='PAUSE'; show('pause'); } else if(gameState==='PAUSE'){ document.getElementById('pause').classList.add('hidden'); gameState=(pauseReturnState==='FLY'&&probe.flying)?'FLY':'AIM'; } }",
        "readable pause function",
    )
    path.write_text(text, encoding="utf-8")


def patch_orbital_release(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        'Qe=1,Ve="MENU",ia=null',
        'Qe=1,Ve="MENU",pauseReturnState="AIM",ia=null',
        "bundled state declaration",
    )
    text = replace_once(
        text,
        'function ca(){Ve==="AIM"||Ve==="FLY"?(Ve="PAUSE",Qi("pause")):Ve==="PAUSE"&&(document.getElementById("pause").classList.add("hidden"),Ve="AIM")}',
        'function ca(){Ve==="AIM"||Ve==="FLY"?(pauseReturnState=Ve,Ve="PAUSE",Qi("pause")):Ve==="PAUSE"&&(document.getElementById("pause").classList.add("hidden"),Ve=pauseReturnState==="FLY"&&We.flying?"FLY":"AIM")}',
        "bundled pause function",
    )
    path.write_text(text, encoding="utf-8")


def patch_index(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        'src="/assets/video/poster-art.jpg"',
        'src="assets/video/poster-art.jpg"',
        "Lessons poster route",
    )
    path.write_text(text, encoding="utf-8")


def install_poster(path: Path) -> dict[str, int | str]:
    encoded = (PAYLOAD / "poster-art.jpg.b64").read_text(encoding="ascii").strip()
    data = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_POSTER_SHA256:
        raise SystemExit(f"poster digest mismatch: {digest}")
    if len(data) != 9114 or not data.startswith(b"\xff\xd8\xff") or not data.endswith(b"\xff\xd9"):
        raise SystemExit("poster is not the verified JPEG")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

    width = height = None
    index = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while index + 3 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        while index < len(data) and data[index] == 0xFF:
            index += 1
        marker = data[index]
        index += 1
        if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
            continue
        length = struct.unpack(">H", data[index:index + 2])[0]
        if marker in sof:
            height, width = struct.unpack(">HH", data[index + 3:index + 7])
            break
        index += length
    if (width, height) != (480, 360):
        raise SystemExit(f"poster dimensions changed: {width}x{height}")
    return {"bytes": len(data), "sha256": digest, "width": width, "height": height}


def script_type(attrs: str) -> str:
    match = re.search(r"\btype\s*=\s*(['\"])(.*?)\1", attrs, re.I | re.S)
    return match.group(2).strip().lower() if match else ""


def check_inline_scripts(path: Path) -> dict[str, int]:
    html = path.read_text(encoding="utf-8")
    js_count = json_count = 0
    for attrs, body in re.findall(r"<script([^>]*)>(.*?)</script>", html, re.I | re.S):
        if re.search(r"\bsrc\s*=", attrs, re.I) or not body.strip():
            continue
        kind = script_type(attrs)
        if kind in JSON_TYPES:
            json.loads(body)
            json_count += 1
            continue
        if kind not in JS_TYPES:
            continue
        suffix = ".mjs" if kind == "module" else ".js"
        with tempfile.NamedTemporaryFile("w", suffix=suffix, encoding="utf-8") as handle:
            handle.write(body)
            handle.flush()
            subprocess.run(["node", "--check", handle.name], check=True)
        js_count += 1
    if js_count == 0:
        raise SystemExit(f"{path}: no JavaScript block was checked")
    return {"javascript_blocks": js_count, "json_blocks": json_count}


def main() -> None:
    source = ROOT / "Games/Orbital_source.html"
    release = ROOT / "Games/Orbital.html"
    index = ROOT / "index.html"
    poster = ROOT / "assets/video/poster-art.jpg"

    patch_orbital_source(source)
    patch_orbital_release(release)
    patch_index(index)
    poster_info = install_poster(poster)

    index_text = index.read_text(encoding="utf-8")
    if index_text.count('src="assets/video/poster-art.jpg"') != 1 or 'src="/assets/video/poster-art.jpg"' in index_text:
        raise SystemExit("poster route was not repaired exactly once")

    report = {
        "sentinel": "mbm-full-repair-upgrade-2026-08-07",
        "poster": poster_info,
        "syntax": {
            "Games/Orbital_source.html": check_inline_scripts(source),
            "Games/Orbital.html": check_inline_scripts(release),
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
