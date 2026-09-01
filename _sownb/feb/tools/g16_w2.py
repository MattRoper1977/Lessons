#!/usr/bin/env python3
"""W2 family-parameterised frozen-denominator contract gate.

The gate applies only rows frozen before candidate measurement.  It includes a
token-deletion firing control against the same candidate and reports every row.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from lxml import html


ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "_sownb/STYLE_CONTRACT.json"
DENOMS = ROOT / "_sownb/G16_DENOMINATORS_W2.json"
DECL = re.compile(r"(--[A-Za-z_][\w-]*)\s*:\s*([^;}]+)")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip()).lower()
    if re.fullmatch(r"#[0-9a-f]{3}", value):
        value = "#" + "".join(ch * 2 for ch in value[1:])
    return value


def compound_xpath(selector: str) -> str:
    selector = selector.strip()
    tag_match = re.match(r"^[A-Za-z][\w-]*|^\*", selector)
    tag = tag_match.group(0) if tag_match else "*"
    predicates = []
    for ident in re.findall(r"#([\w-]+)", selector):
        predicates.append(f"@id={json.dumps(ident)}")
    for cls in re.findall(r"\.([\w-]+)", selector):
        predicates.append(f"contains(concat(' ',normalize-space(@class),' '),' {cls} ')")
    for name, quote, value in re.findall(r"\[([\w:-]+)(?:=([\"'])(.*?)\2)?\]", selector):
        predicates.append(f"@{name}={json.dumps(value)}" if quote else f"@{name}")
    return tag + "".join(f"[{item}]" for item in predicates)


def selector_count(tree, selector: str) -> int:
    parts = [item.strip() for item in selector.split(">")]
    if len(parts) == 1:
        return len(tree.xpath("descendant-or-self::" + compound_xpath(parts[0])))
    if len(parts) == 2:
        return len(tree.xpath("descendant-or-self::" + compound_xpath(parts[0]) + "/" + compound_xpath(parts[1])))
    raise ValueError(f"unsupported proved selector: {selector}")


def requirement_ok(required: str, actual: int, reference: int | None = None) -> bool:
    if required.startswith("==") and required[2:].isdigit():
        return actual == int(required[2:])
    if required.startswith(">=") and required[2:].isdigit():
        return actual >= int(required[2:])
    if required == "==reference":
        return reference is not None and actual == reference
    return actual > 0


def metric(row: dict, source: str, tree) -> tuple[object, bool, str]:
    row_id = row["id"]
    if row_id == "shared.deck.timing-array":
        nodes = tree.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," deck ")]/section[contains(concat(" ",normalize-space(@class)," ")," slide ")]')
        values = [int(float(node.get("data-min", "-1"))) for node in nodes]
        config = tree.xpath('//script[@id="lesson-config"]')
        config_values = None
        if config and config[0].text:
            try:
                config_values = json.loads(config[0].text).get("timings")
            except json.JSONDecodeError:
                config_values = None
        ok = values == row["value"] and sum(values) == 40 and config_values == values
        return {"dataMin": values, "lessonConfigTimings": config_values, "sum": sum(values)}, ok, "exact timing array and lesson-config binding"
    if row_id == "shared.motion.no-keyframes":
        actual = source.count("@keyframes")
        return actual, actual == 0, "zero @keyframes"
    if row_id == "shared.offline.boundary":
        patterns = ["fetch(", "XMLHttpRequest", "serviceWorker", "http://", "https://"]
        found = [item for item in patterns if item in source]
        return found, not found, "zero runtime-network calls or URLs"
    if row_id == "shared.controls.minimum":
        found = [int(v) for v in re.findall(r"min-(?:height|width)\s*:\s*(\d+)px", source)]
        actual = max(found) if found else 0
        return actual, actual >= 44, "declared minimum interactive dimension"
    if row_id == "shared.print.typography-h1":
        actual = source.count(".print-pack h1")
        return actual, actual >= 1, "rendered clipping is separately measured by running-head/PDF gate"
    if row_id == "shared.confirmation.placement":
        count = len(tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," print-pack ")]//*[contains(concat(" ",normalize-space(@class)," ")," print-page ") and contains(concat(" ",normalize-space(@class)," ")," n6-lc-page ")]'))
        return count, count == 1, "one confirmation page inside print pack"
    return None, False, "unimplemented metric"


def evaluate(source: str, row: dict, tree) -> dict:
    kind, value, required = row["kind"], row["value"], row["required"]
    if kind in {"visible-string", "byte-block", "css-rule"}:
        actual = source.count(value)
        ok = requirement_ok(required, actual, row.get("reference_count"))
        detail = "literal source occurrence"
    elif kind == "selector":
        actual = selector_count(tree, value)
        ok = requirement_ok(required, actual, row.get("reference_count"))
        detail = "parsed DOM selector count"
    elif kind == "token":
        values = [norm(v) for n, v in DECL.findall(source) if n == value["name"]]
        actual = values
        ok = len(values) == 1 and values[0] == norm(value["value"])
        detail = "unique declaration and measured value"
    elif kind == "metric":
        actual, ok, detail = metric(row, source, tree)
    else:
        actual, ok, detail = None, False, f"unsupported kind {kind}"
    return {"id": row["id"], "kind": kind, "required": required, "actual": actual, "pass": ok, "measurement": detail}


def rows_for(family: str, artifact: str, contract: dict, denoms: dict) -> list[dict]:
    ids = denoms["families"][family]["lessonRowIds" if artifact == "lesson" else "supportRowIds"]
    by_id = {row["id"]: row for row in contract["rows"]}
    if artifact == "start_here":
        ids = [item for item in ids if item.startswith("start.")]
    elif artifact == "pack":
        ids = [item for item in ids if item.startswith("pack.")]
    return [by_id[item] for item in ids]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", required=True)
    parser.add_argument("--artifact", choices=("lesson", "start_here", "pack"), default="lesson")
    parser.add_argument("--file", required=True, help="HTML file for lesson/start_here, pack directory for pack")
    parser.add_argument("--output")
    args = parser.parse_args()
    contract, denoms = json.loads(CONTRACT.read_text()), json.loads(DENOMS.read_text())
    if sha(CONTRACT) != denoms["contractSha256"]:
        raise SystemExit("MEASUREMENT INVALID: frozen denominator contract hash mismatch")
    rows = rows_for(args.family, args.artifact, contract, denoms)
    if not rows:
        raise SystemExit("MEASUREMENT INVALID: zero frozen rows")
    target = ROOT / args.file
    if args.artifact == "pack":
        results = []
        for row in rows:
            expected = row["value"]
            exists = (target / expected).is_file()
            results.append({"id": row["id"], "kind": row["kind"], "required": row["required"], "actual": exists, "pass": exists, "measurement": "required pack filename"})
        source, candidate_sha = "", None
    else:
        source = target.read_text(encoding="utf-8")
        tree = html.fromstring(source)
        results = [evaluate(source, row, tree) for row in rows]
        candidate_sha = sha(target)
    firing = {"applicable": args.artifact == "lesson", "fired": None}
    if args.artifact == "lesson":
        token_row = next((row for row in rows if row["kind"] == "token"), None)
        if token_row:
            literal = f"{token_row['value']['name']}:{token_row['value']['value']}"
            mutated = source.replace(literal, "", 1)
            mutated_result = evaluate(mutated, token_row, html.fromstring(mutated))
            firing = {"applicable": True, "mutation": f"delete {token_row['value']['name']} declaration", "row": token_row["id"], "fired": not mutated_result["pass"], "mutatedResult": mutated_result}
    failed = [row for row in results if not row["pass"]]
    status = "PASS" if not failed and firing.get("fired") is not False else "RED"
    report = {
        "gate": "g16-w2-frozen", "family": args.family, "artifact": args.artifact,
        "candidate": args.file, "candidateSha256": candidate_sha,
        "contractSha256": sha(CONTRACT), "denominatorSha256": sha(DENOMS),
        "frozenRowCount": len(rows), "nonVacuous": len(rows) > 0,
        "passed": len(results) - len(failed), "failed": len(failed), "failedRows": failed,
        "rows": results, "firingControl": firing, "status": status,
    }
    if args.output:
        out = ROOT / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("gate", "family", "artifact", "frozenRowCount", "passed", "failed", "failedRows", "firingControl", "status")}, indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
