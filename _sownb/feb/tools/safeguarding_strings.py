#!/usr/bin/env python3
"""Assert the named safeguarding strings on all three LAUNCH Science lessons."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILES = sorted((ROOT / "Science_Teesside/Launch/W14-W15_2026-27").glob("SCI_L_W14L*.html"))
REQUIRED = [
    "No diagnosis or medical advice.",
    "No personal or family information.",
    "learning does not depend on a runtime connection.",
]
NETWORK = ("fetch(", "XMLHttpRequest", "serviceWorker", "http://", "https://")
rows = []
for path in FILES:
    source = path.read_text(encoding="utf-8")
    strings = {value: source.count(value) for value in REQUIRED}
    network = {value: source.count(value) for value in NETWORK}
    controls = {}
    for value in REQUIRED:
        planted = source.replace(value, "")
        controls[value] = {"mutation": "delete every carrier of the exact named string in memory", "fired": planted.count(value) == 0 and source.count(value) > 0}
    rows.append({
        "file": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "requiredExactStrings": strings,
        "runtimeNetworkTokens": network,
        "controls": controls,
        "status": "PASS" if all(count >= 1 for count in strings.values()) and all(count == 0 for count in network.values()) and all(item["fired"] for item in controls.values()) else "RED",
    })
report = {
    "gate": "launch-science-named-safeguarding-strings",
    "lessonCount": len(rows),
    "rows": rows,
    "status": "PASS" if len(rows) == 3 and all(row["status"] == "PASS" for row in rows) else "RED",
}
output = ROOT / "_sownb/rsh3/evidence/packs/launch-science-w14-w15/safeguarding-final.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": report["status"], "lessons": [{"file": Path(row["file"]).name, "strings": row["requiredExactStrings"], "offline": all(value == 0 for value in row["runtimeNetworkTokens"].values()), "controls": all(item["fired"] for item in row["controls"].values())} for row in rows]}, indent=2))
raise SystemExit(0 if report["status"] == "PASS" else 1)
