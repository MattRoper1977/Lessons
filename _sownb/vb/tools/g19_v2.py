#!/usr/bin/env python3
"""g19 v2 — token ownership under the RUN12-A ruling.

The ruling: a token is DEFINED once, in :root. Pathway values live under the
pathway scope selector only; a second definition in :root is a red.

So this gate measures two things and reports both:

  uniqueness  every custom property declared inside a :root block is declared
              there exactly once. A second declaration of the same token in
              :root (in the same block or a later one) is a RED. Declarations
              under a scope selector -- body.pathway-build, .theme-x, a
              component class -- are recorded and are NOT counted against
              uniqueness, because they are not definitions in :root.

  ownership   inherited from FEB's g19 v1: every declared token name belongs to
              this family's measured set, and every value matches one measured
              on the family's own donors.

FEB's g19 is untouched: its parser is imported so the instrument is the same
tokeniser, and its config format is reused (_sownb/vb/G19_TOKEN_OWNERSHIP_v2.json).

Non-vacuity is not optional. Every run plants a duplicate declaration of one of
the candidate's own tokens inside its first :root block, re-measures, and
requires that mutation to be RED. A gate that cannot be made to fire has not
measured anything, and this one says so in its own report.

Usage:
  g19_v2.py --family "GROW ASDAN" --file <deck.html> [--output <report.json>]
  g19_v2.py --family "GROW ASDAN" --file <deck.html> --scoped-ok  (default)
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FEB = ROOT / "_sownb/feb/tools/g19_token_ownership.py"
CONFIG = ROOT / "_sownb/vb/G19_TOKEN_OWNERSHIP_v2.json"

_spec = importlib.util.spec_from_file_location("feb_g19", FEB)
feb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(feb)

DECL = feb.DECL
COMMENT = feb.COMMENT
norm = feb.norm

# A rule's selector list, then its body. Nested at-rules are handled by taking
# the innermost brace pair, which is what a declaration block always is.
RULE = re.compile(r"([^{}]*)\{([^{}]*)\}", re.S)


def css_of(path: Path) -> str:
    """Every <style> block and inline style attribute, comments stripped."""
    parser = feb.Styles()
    parser.feed(path.read_text(encoding="utf-8"))
    return "\n".join(COMMENT.sub("", part) for part, _line in parser.parts)


def declarations(css: str) -> tuple[list[dict], list[dict]]:
    """Split declarations into those inside :root blocks and those elsewhere."""
    in_root, scoped = [], []
    for match in RULE.finditer(css):
        selector = " ".join(match.group(1).split())
        selector = selector.split("}")[-1].split("{")[-1].strip()
        body = match.group(2)
        if "--" not in body:
            continue
        is_root = any(part.strip() == ":root" for part in selector.split(","))
        for decl in DECL.finditer(body):
            name, value = decl.group(1), decl.group(2)
            row = {
                "name": name,
                "value": value.strip(),
                "normalisedValue": norm(value),
                "selector": selector[:120],
            }
            (in_root if is_root else scoped).append(row)
    return in_root, scoped


def measure(path: Path, family: str, config: dict) -> dict:
    css = css_of(path)
    in_root, scoped = declarations(css)
    # ORDER VB-RUN15 H14-3(c): a deck carries ONE :root block. A second block is a red
    # even when no token repeats, because the cascade then depends on source order
    # and the run-12 migration put every pathway value under html.pathway-<lane>.
    root_blocks = len([m for m in RULE.finditer(css) if any(part.strip() == ':root' for part in ' '.join(m.group(1).split()).split('}')[-1].split('{')[-1].split(','))])
    counts: dict[str, int] = {}
    for row in in_root:
        counts[row["name"]] = counts.get(row["name"], 0) + 1
    duplicates = sorted(name for name, count in counts.items() if count > 1)
    duplicate_detail = [
        {"name": name, "declarations": [r["value"] for r in in_root if r["name"] == name]}
        for name in duplicates
    ]

    family_values: dict[str, list[str]] = config["families"][family]["values"]
    base: dict[str, str] = config.get("base", {})
    all_names = {name for item in config["families"].values() for name in item["values"]} | set(base)
    rows = in_root + scoped
    unknown = sorted({r["name"] for r in rows if r["name"] not in all_names})
    foreign = sorted({r["name"] for r in rows if r["name"] not in family_values and r["name"] in all_names})
    # A declaration inside :root must carry the estate base value where the corpus
    # measures one; a scoped declaration must carry a value measured on this family.
    wrong = []
    for row in in_root:
        if row["name"] in base and row["normalisedValue"] != base[row["name"]]:
            wrong.append({"name": row["name"], "actual": row["normalisedValue"], "expected": [base[row["name"]]], "selector": ":root", "rule": "estate base"})
    for row in scoped:
        allowed = family_values.get(row["name"])
        if allowed is not None and row["normalisedValue"] not in allowed:
            wrong.append({"name": row["name"], "actual": row["normalisedValue"], "expected": allowed, "selector": row["selector"], "rule": "family scoped value"})
    status = "PASS" if rows and not duplicates and not foreign and not unknown and not wrong and root_blocks <= 1 else "RED"
    return {
        "file": str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "family": family,
        "rootDeclarations": len(in_root),
        "rootBlocks": root_blocks,
        "rootBlocksRule": "one :root block per deck (ORDER VB-RUN15 H14-3c); a second block is RED",
        "scopedDeclarations": len(scoped),
        "scopeSelectors": sorted({r["selector"] for r in scoped})[:12],
        "duplicateDefinitionsInRoot": duplicates,
        "duplicateDetail": duplicate_detail,
        "foreignFamilyTokens": foreign,
        "unknownTokens": unknown,
        "wrongValues": wrong,
        "status": status,
    }


def plant_duplicate(css_source: str, token: str, value: str) -> str:
    """Add one more declaration of an existing token inside the first :root."""
    match = re.search(r":root\s*\{", css_source)
    if not match:
        return css_source
    return css_source[: match.end()] + f"{token}:{value};" + css_source[match.end() :]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--config", default=str(CONFIG))
    parser.add_argument("--output")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    path = ROOT / args.file if not Path(args.file).is_absolute() else Path(args.file)
    report = measure(path, args.family, config)

    # Firing control: plant a duplicate of the candidate's own first token in
    # :root and re-measure a temporary copy. The gate must go RED.
    source = path.read_text(encoding="utf-8")
    in_root, _ = declarations(css_of(path))
    control = {"applicable": bool(in_root), "fired": None}
    if in_root:
        token, value = in_root[0]["name"], in_root[0]["value"]
        mutated = plant_duplicate(source, token, value)
        scratch = path.parent / f".g19v2_control_{path.name}"
        scratch.write_text(mutated, encoding="utf-8")
        try:
            mutated_report = measure(scratch, args.family, config)
        finally:
            scratch.unlink(missing_ok=True)
        control.update(
            {
                "mutation": f"a second declaration of {token} inside the first :root block",
                "mutatedStatus": mutated_report["status"],
                "mutatedDuplicates": mutated_report["duplicateDefinitionsInRoot"],
                "fired": mutated_report["status"] == "RED" and token in mutated_report["duplicateDefinitionsInRoot"],
            }
        )
    # Second firing control (ORDER VB-RUN15 H14-3c): plant a SECOND :root block carrying
    # a token no other block declares, so the duplicate rule cannot be what fires, and
    # re-measure a temporary copy. The gate must go RED on rootBlocks alone; the scratch
    # copy is deleted afterwards, so the control is fired then withdrawn.
    block_control = {"applicable": True, "fired": None}
    idx = source.find("</style>")
    if idx < 0:
        block_control["applicable"] = False
    else:
        mutated = source[:idx] + ":root{--g19-planted-second-block:1}" + source[idx:]
        scratch = path.parent / f".g19v2_blockcontrol_{path.name}"
        scratch.write_text(mutated, encoding="utf-8")
        try:
            mutated_report = measure(scratch, args.family, config)
        finally:
            scratch.unlink(missing_ok=True)
        block_control.update({
            "mutation": "a second :root block declaring one token no other block declares",
            "mutatedRootBlocks": mutated_report["rootBlocks"],
            "mutatedStatus": mutated_report["status"],
            "mutatedDuplicates": mutated_report["duplicateDefinitionsInRoot"],
            "fired": mutated_report["rootBlocks"] == report["rootBlocks"] + 1 and mutated_report["status"] == "RED",
            "withdrawn": not scratch.exists(),
        })
    report["firingControl"] = control
    report["rootBlockControl"] = block_control
    report["nonVacuous"] = bool(control.get("fired")) and bool(block_control.get("fired"))
    report["rule"] = (
        "RUN12-A: a token is DEFINED once, in :root; pathway values live under a scope selector only; "
        "a second definition in :root is a red. Scoped declarations are recorded, not counted for uniqueness. "
        "RUN15 H14-3c: one :root block per deck; a second block is a red."
    )
    report["subject"] = f"g19 v2 token ownership and :root uniqueness for {args.family}"
    if not report["nonVacuous"]:
        report["status"] = "MEASUREMENT INVALID"
    if args.output:
        out = ROOT / args.output if not Path(args.output).is_absolute() else Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                k: report[k]
                for k in (
                    "family",
                    "rootDeclarations",
                    "scopedDeclarations",
                    "duplicateDefinitionsInRoot",
                    "foreignFamilyTokens",
                    "unknownTokens",
                    "firingControl",
                    "status",
                )
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
