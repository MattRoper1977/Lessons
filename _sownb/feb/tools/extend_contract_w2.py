#!/usr/bin/env python3
"""Append proved BUILD-family rows and freeze W2 g16/g19 inputs.

Existing contract rows are treated as immutable objects.  Every appended row is
bound to a literal, non-zero occurrence in a named same-family donor at the
current anchor.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"
DENOMS = ROOT / "_sownb/G16_DENOMINATORS_W2.json"
TOKENS = ROOT / "_sownb/G19_TOKEN_OWNERSHIP_W2.json"
EVIDENCE = ROOT / "_sownb/w2/CONTRACT_EXTENSION.json"
UNPROVEN_ADDENDUM = ROOT / "_sownb/w2/UNPROVEN_W2.md"

SPLASH = '<!--n6-nav1:v1--><div class="n6-splash"><div style="text-align:center;margin-top:8px"><svg width="64" height="64" viewBox="0 0 100 100" aria-label="Made by Matt"><circle cx="50" cy="50" r="47" fill="none" stroke="#1e3a8a" stroke-width="3.4"/><g transform="translate(0 2)"><path d="M28 71 L28 37 L50 59 L72 37 L72 71" fill="none" stroke="#1e3a8a" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M50 22.5 L51.48 28.52 L57.5 30 L51.48 31.48 L50 37.5 L48.52 31.48 L42.5 30 L48.52 28.52 Z" fill="#F2A24A"/></g></svg></div></div><!--/n6-nav1-->'

FAMILIES = {
    "BUILD Science": {
        "slug": "build-science",
        "lesson": "Science_Teesside/Build/W8-W13_2026-27/SCI_B_W13B_Method_Pilot_Test_The_Test_Do.html",
        "start": "Science_Teesside/Build/W8-W13_2026-27/START_HERE.html",
        "pack": "Science_Teesside/Build/W8-W13_2026-27",
        "home": 'href="../../../index.html"',
        "tokens": {
            "--grow": "#4E7A9B", "--navy": "#10233f", "--text": "#1f2937",
            "--muted": "#64748b", "--bg": "#f5f8fa", "--lo": "#e7d8e9",
            "--purple": "#7c3aed", "--pink": "#db2777", "--amber": "#eab308",
            "--blue": "#3b82f6", "--green": "#16a34a", "--softblue": "#e9f4fb",
            "--softamber": "#fff7d6", "--softgreen": "#eaf8ef", "--line": "#d8e0e8",
        },
        "controls": ["TA Brief", "Live Loop", "Guidance", "Word help", "Calm view", "Teacher Freeze", "Previous", "Next"],
        "structures": [".lundy", ".ladder", ".ta-card", ".modal", ".chips", ".hero-visual", ".evidence-gate", ".prog"],
        "tiers": [("route-s", ".route.s"), ("route-m", ".route.m"), ("route-h", ".route.h")],
        "labels": ["◆ Supported", "▲ Standard", "★ Stretch"],
        "print": [".printpack", ".proute"],
        "start_tokens": ["--grow", "--navy"],
        "start_selectors": [".hero", ".card"],
        "start_name": "START_HERE.html",
        "checksums": "SHA256SUMS.txt",
    },
    "BUILD Humanities": {
        "slug": "build-humanities",
        "lesson": "Humanities_Teesside/BUILD_W9-W14_2026-27/BUILD_HUM_W14_Industry_and_Nature_The_Tees_Story_OUTSTANDING_V4.html",
        "start": "Humanities_Teesside/BUILD_W9-W14_2026-27/START_HERE.html",
        "pack": "Humanities_Teesside/BUILD_W9-W14_2026-27",
        "home": 'href="../../index.html"',
        "tokens": {
            "--ink": "#18233F", "--steel": "#4F869C", "--steel-dark": "#356478",
            "--rust": "#D06438", "--rust-dark": "#A94722", "--teal": "#16877A",
            "--teal-dark": "#0E685F", "--gold": "#E1AB32", "--cream": "#FAF7EF",
            "--line": "#CBD5E1", "--muted": "#526173", "--green": "#286E54",
            "--paper": "#fffdf8", "--focus": "#18233F",
        },
        "controls": ["TA", "Read response", "Staff &amp; print", "Calm mode", "Previous", "Next"],
        "structures": [".lundy", ".ladder", ".ta-card", ".drawer", ".chips", ".hero-visual", ".prog"],
        "tiers": [("route-supported", ".route.supported"), ("route-standard", ".route.standard"), ("route-stretch", ".route.stretch")],
        "labels": ["◆ Supported", "▲ Standard", "★ Stretch"],
        "print": [".printpack", ".proute"],
        "start_tokens": ["--ink", "--steel"],
        "start_selectors": [".thread", ".week"],
        "start_name": "START_HERE.html",
        "checksums": "SHA256SUMS.txt",
    },
    "BUILD ASDAN": {
        "slug": "build-asdan",
        "lesson": "BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_COMM_W6_Share_Our_Impact.html",
        "start": "BUILD_ASDAN/Autumn2_W1-W6_2026-27/START_HERE_BUILD_ASDAN_AUT2.html",
        "pack": "BUILD_ASDAN/Autumn2_W1-W6_2026-27",
        "home": 'href="../../index.html"',
        "tokens": {
            "--ink": "#17223B", "--paper": "#FFFCF5", "--soft": "#F3F6F8",
            "--line": "#CAD5DF", "--muted": "#526274", "--gold": "#B57918",
            "--green": "#246B55", "--slot": "#346B7B", "--slot-pale": "#EAF6F8",
            "--danger": "#8A3C2D",
        },
        "controls": ["Teacher tools", "Evidence & print", "Calm mode", "Static diagrams", "Previous", "Next"],
        "structures": [".lundy-strip", ".prompt-ladder", ".route-card", ".chips", ".evidence-gate", "dialog"],
        "tiers": [("route-supported", ".print-route.supported"), ("route-standard", ".print-route.standard"), ("route-stretch", ".print-route.stretch")],
        "labels": ["◆ Supported", "▲ Standard", "★ Stretch"],
        "print": [".print-pack", ".print-page"],
        "start_tokens": ["--ink", "--teal"],
        "start_selectors": [".grid", ".lesson-link"],
        "start_name": "START_HERE_BUILD_ASDAN_AUT2.html",
        "checksums": "SHA256SUMS.txt",
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proof(rel: str, literal: str) -> tuple[int, dict[str, str]]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    output = []
    first = None
    for number, line in enumerate(text.splitlines(), 1):
        count = line.count(literal)
        if count:
            first = first or number
            output.extend(f"{number}:{literal}" for _ in range(count))
    if not output:
        raise RuntimeError(f"zero literal proof: {literal!r} in {rel}")
    quoted = literal.replace("'", "'\\''")
    return int(first), {
        "command": f"grep -n -F -o -- '{quoted}' {rel}",
        "output": "\n".join(output),
    }


def row(row_id: str, family: str, artifact: str, kind: str, value, required: str, donor: str, literal: str | None = None) -> dict:
    hit = literal if literal is not None else (value if isinstance(value, str) else f"{value['name']}:{value['value']}")
    line, proved = proof(donor, hit)
    return {
        "id": row_id, "scope": f"family:{family}", "kind": kind, "value": value,
        "donor_path": donor, "donor_line": line, "proof": proved,
        "required": required, "artifact": artifact,
    }


def build_rows() -> tuple[list[dict], list[dict[str, str]]]:
    out = []
    unproven = []
    for family, cfg in FAMILIES.items():
        slug, lesson, start = cfg["slug"], cfg["lesson"], cfg["start"]
        out.append(row(f"family.{slug}.home", family, "lesson", "visible-string", cfg["home"], ">=1", lesson))
        for name, value in cfg["tokens"].items():
            key = name[2:].replace("_", "-")
            out.append(row(f"family.{slug}.token.{key}", family, "lesson", "token", {"name": name, "value": value}, "==reference", lesson))
        for number, literal in enumerate(cfg["controls"], 1):
            out.append(row(f"family.{slug}.control.{number:02d}", family, "lesson", "visible-string", literal, ">=1", lesson))
        for literal in cfg["structures"]:
            key = literal.lstrip(".").replace(".", "-")
            out.append(row(f"family.{slug}.structure.{key}", family, "lesson", "selector", literal, ">=1", lesson))
        for key, literal in cfg["tiers"]:
            out.append(row(f"family.{slug}.tier.{key}", family, "lesson", "selector", literal, ">=1", lesson))
        for literal in cfg["labels"]:
            key = re.sub(r"[^a-z]+", "-", literal.lower()).strip("-")
            out.append(row(f"family.{slug}.tier.label-{key}", family, "lesson", "visible-string", literal, ">=1", lesson))
        for number, literal in enumerate(cfg["print"], 1):
            out.append(row(f"family.{slug}.print.{number:02d}", family, "lesson", "selector", literal, ">=1", lesson))
        for key, literal in (("marker", "<!--n6-learner-confirm:v1-->"), ("text", "Learner confirmation")):
            if literal in (ROOT / lesson).read_text(encoding="utf-8"):
                out.append(row(f"family.{slug}.confirmation.{key}", family, "lesson", "visible-string", literal, ">=1", lesson))
            else:
                unproven.append({
                    "family": family, "candidateRow": f"family.{slug}.confirmation.{key}",
                    "literal": literal, "donor": lesson,
                    "reason": "zero same-family literal hits; shared confirmation rows remain binding on new lessons",
                })

        checksum_rel = f"{cfg['pack']}/{cfg['checksums']}"
        manifest_rel = f"{cfg['pack']}/manifest.json"
        out.append(row(f"pack.{slug}.manifest", family, "pack", "visible-string", "manifest.json", "required filename", checksum_rel))
        out.append(row(f"pack.{slug}.start-here", family, "start_here", "visible-string", cfg["start_name"], "required filename and dialect", checksum_rel))
        # The checksum donor proves its own dialect by a literal checksum entry for manifest.json.
        out.append(row(f"pack.{slug}.checksums", family, "pack", "visible-string", cfg["checksums"], "required filename", checksum_rel, "manifest.json"))
        for name in cfg["start_tokens"]:
            # Start donors may use a family synonym only when that synonym is literally measured there.
            match = re.search(rf"{re.escape(name)}\s*:\s*([^;}}]+)", (ROOT / start).read_text(encoding="utf-8"))
            if not match:
                raise RuntimeError(f"start token {name} absent: {start}")
            value = match.group(1).strip()
            out.append(row(f"start.{slug}.token-{name[2:]}", family, "start_here", "token", {"name": name, "value": value}, "==reference", start, f"{name}:{value}"))
        for literal in cfg["start_selectors"]:
            out.append(row(f"start.{slug}.{literal.lstrip('.')}", family, "start_here", "selector", literal, ">=1", start))
        out.append(row(f"start.{slug}.way-home", family, "start_here", "visible-string", "← Lessons", "==1", start))
        out.append(row(f"start.{slug}.splash", family, "start_here", "byte-block", SPLASH, "==1", start))
        out.append(row(f"start.{slug}.home-marker", family, "start_here", "visible-string", "<!--n6-nav1:v1-->", ">=2", start))
    return out, unproven


def token_config() -> dict:
    families = {}
    for family, cfg in FAMILIES.items():
        donors = [cfg["lesson"], cfg["start"]]
        values: dict[str, set[str]] = {}
        donor_rows = []
        for rel in donors:
            path = ROOT / rel
            found = re.findall(r"(--[A-Za-z_][\w-]*)\s*:\s*([^;}]+)", path.read_text(encoding="utf-8"))
            donor_rows.append({"path": rel, "sha256": sha(path), "declarations": len(found)})
            for name, value in found:
                normal = re.sub(r"\s+", " ", value.strip()).lower()
                if re.fullmatch(r"#[0-9a-f]{3}", normal):
                    normal = "#" + "".join(ch * 2 for ch in normal[1:])
                values.setdefault(name, set()).add(normal)
        families[family] = {"donors": donor_rows, "values": {k: sorted(v) for k, v in sorted(values.items())}}
    return {
        "schema": "w2-g19-token-ownership-v1",
        "rule": "Every declared custom property is measured in this family's named live lesson or START_HERE donor; declarations are unique; values match a measured family value.",
        "sharedEstateSet": [], "families": families,
    }


def main() -> int:
    original_bytes = CONTRACT.read_bytes()
    contract = json.loads(original_bytes)
    if len(contract["rows"]) != 225:
        raise RuntimeError(f"expected immutable 225-row prefix, found {len(contract['rows'])}")
    prefix = [hashlib.sha256(json.dumps(item, sort_keys=True, ensure_ascii=False).encode()).hexdigest() for item in contract["rows"]]
    additions, unproven = build_rows()
    ids = {item["id"] for item in contract["rows"]}
    if any(item["id"] in ids for item in additions):
        raise RuntimeError("append id collides with existing contract row")
    contract["rows"].extend(additions)
    contract["rowCount"] = len(contract["rows"])
    CONTRACT.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    reread = json.loads(CONTRACT.read_text(encoding="utf-8"))
    after_prefix = [hashlib.sha256(json.dumps(item, sort_keys=True, ensure_ascii=False).encode()).hexdigest() for item in reread["rows"][:225]]
    if prefix != after_prefix:
        raise RuntimeError("immutable contract prefix changed")

    shared_lesson = [r["id"] for r in reread["rows"] if r["scope"] == "shared" and r["artifact"] == "lesson"]
    families = {}
    for family, cfg in FAMILIES.items():
        scoped = [r for r in reread["rows"] if r["scope"] == f"family:{family}"]
        lesson = shared_lesson + [r["id"] for r in scoped if r["artifact"] == "lesson"]
        support = [r["id"] for r in scoped if r["artifact"] in {"pack", "start_here"}]
        families[family] = {
            "lessonCount": len(lesson), "lessonRowIds": lesson,
            "supportCount": len(support), "supportRowIds": support,
            "count": len(lesson) + len(support), "rowIds": lesson + support,
        }
    denominators = {
        "schema": "w2-g16-denominators-v1", "contractSha256": sha(CONTRACT),
        "contractRowCount": len(reread["rows"]), "frozenAtAnchor": "4916fe9511e24e1f5541e7454f3d2e9d4bac5f75",
        "families": families, "rule": "Frozen before the first W2 candidate measurement; no drift within the run.",
    }
    DENOMS.write_text(json.dumps(denominators, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    TOKENS.write_text(json.dumps(token_config(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# W2 unproven contract-row addendum", "",
        "The protected `_sownb/UNPROVEN.md` baseline is unchanged. These W2 candidates had zero literal proof in the named same-family donor and were not asserted.", "",
    ]
    for item in unproven:
        lines.append(f"- `{item['candidateRow']}` — {item['family']}; literal `{item['literal']}`; donor `{item['donor']}`; {item['reason']}.")
    UNPROVEN_ADDENDUM.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = {
        "status": "PASS", "route": "ABSENT / exact recovery plus explicit W2 extension",
        "immutablePrefixRows": 225, "immutablePrefixHashIdentity": prefix == after_prefix,
        "addedRows": len(additions), "rowCount": len(reread["rows"]),
        "contractBeforeSha256": hashlib.sha256(original_bytes).hexdigest(), "contractAfterSha256": sha(CONTRACT),
        "denominatorsSha256": sha(DENOMS), "tokenOwnershipSha256": sha(TOKENS),
        "families": {family: {"addedRows": sum(1 for r in additions if r["scope"] == f"family:{family}"), **families[family]} for family in FAMILIES},
        "proofsNonZero": all(r["proof"]["output"] for r in additions),
        "unprovenRows": unproven,
        "donors": {family: {"lesson": cfg["lesson"], "start": cfg["start"]} for family, cfg in FAMILIES.items()},
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
