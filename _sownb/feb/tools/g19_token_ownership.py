#!/usr/bin/env python3
"""RSH-3 g19: bind declared CSS custom properties to measured family donors."""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DECL = re.compile(r"(--[A-Za-z_][\w-]*)\s*:\s*([^;}]+)")
COMMENT = re.compile(r"/\*.*?\*/", re.S)


class Styles(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_style = False
        self.parts: list[tuple[str, int]] = []
        self.line = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "style":
            self.in_style = True
        for name, value in attrs:
            if name.lower() == "style" and value:
                self.parts.append((value, self.getpos()[0]))

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.parts.append((data, self.getpos()[0]))


def norm(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip()).lower()
    match = re.fullmatch(r"#([0-9a-f]{3})", value)
    if match:
        value = "#" + "".join(char * 2 for char in match.group(1))
    return value


def declarations(path: Path) -> list[dict[str, object]]:
    parser = Styles()
    parser.feed(path.read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for css, base_line in parser.parts:
        css = COMMENT.sub("", css)
        for match in DECL.finditer(css):
            rows.append({
                "name": match.group(1),
                "value": match.group(2).strip(),
                "normalisedValue": norm(match.group(2)),
                "approximateLine": base_line + css[:match.start()].count("\n"),
            })
    return rows


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_config(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def measure(path: Path, family: str, config: dict[str, object]) -> dict[str, object]:
    rows = declarations(path)
    family_values: dict[str, list[str]] = config["families"][family]["values"]  # type: ignore[index]
    all_names = {
        name
        for item in config["families"].values()  # type: ignore[union-attr]
        for name in item["values"]
    }
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["name"]] = counts.get(row["name"], 0) + 1  # type: ignore[index]
    duplicate = sorted(name for name, count in counts.items() if count > 1)
    foreign = sorted({row["name"] for row in rows if row["name"] not in family_values and row["name"] in all_names})
    unknown = sorted({row["name"] for row in rows if row["name"] not in all_names})
    wrong_values = []
    for row in rows:
        expected = family_values.get(row["name"])
        if expected is not None and row["normalisedValue"] not in expected:
            wrong_values.append({"name": row["name"], "actual": row["normalisedValue"], "expected": expected})
    status = "PASS" if rows and not duplicate and not foreign and not unknown and not wrong_values else "RED"
    return {
        "file": str(path.relative_to(ROOT)),
        "sha256": sha(path),
        "family": family,
        "declarations": rows,
        "duplicateDeclarations": duplicate,
        "foreignFamilyTokens": foreign,
        "unknownTokens": unknown,
        "wrongValues": wrong_values,
        "status": status,
    }


def build_config(output: Path) -> None:
    donors = {
        "GROW Science": [
            "Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html",
            "Science_Teesside/Grow/W8-W13_2026-27/START_HERE.html",
        ],
        "GROW ASDAN": [
            "GROW_ASDAN/Autumn2_W1-W6_2026-27/PEQ_A2_W6_My_Future_Profile_Now_Next_Maybe_GROW_v3_40min.html",
            "GROW_ASDAN/Autumn2_W1-W6_2026-27/START_HERE.html",
        ],
        "LAUNCH ASDAN": [
            "LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W12_Review_My_Teamwork_Progress_Evidence_Next_Action_LAUNCH.html",
            "LAUNCH_ASDAN/W7-W12_2026-27/START_HERE.html",
        ],
        "LAUNCH Science": [
            "Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L3_Inheritance_Probability_Do.html",
            "Science_Teesside/Launch/W8-W13_2026-27/START_HERE.html",
        ],
    }
    families: dict[str, object] = {}
    for family, rels in donors.items():
        values: dict[str, set[str]] = {}
        donor_rows = []
        for rel in rels:
            path = ROOT / rel
            rows = declarations(path)
            donor_rows.append({"path": rel, "sha256": sha(path), "declarations": len(rows)})
            for row in rows:
                values.setdefault(row["name"], set()).add(row["normalisedValue"])  # type: ignore[index]
        families[family] = {"donors": donor_rows, "values": {key: sorted(value) for key, value in sorted(values.items())}}
    config = {
        "schema": "rsh3-g19-token-ownership-v1",
        "rule": "Every declared custom property is measured in this family's named live lesson or START_HERE donor; declarations are unique; values match a measured family value.",
        "sharedEstateSet": [],
        "families": families,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-config", action="store_true")
    parser.add_argument("--config", default="_sownb/G19_TOKEN_OWNERSHIP.json")
    parser.add_argument("--family")
    parser.add_argument("--file")
    parser.add_argument("--output")
    args = parser.parse_args()
    config_path = ROOT / args.config
    if args.build_config:
        build_config(config_path)
        print(json.dumps({"status": "PASS", "config": args.config, "sha256": sha(config_path)}, indent=2))
        return 0
    if not args.family or not args.file:
        parser.error("--family and --file are required unless --build-config is used")
    report = measure(ROOT / args.file, args.family, load_config(config_path))
    if args.output:
        out = ROOT / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("file", "family", "duplicateDeclarations", "foreignFamilyTokens", "unknownTokens", "wrongValues", "status")}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
