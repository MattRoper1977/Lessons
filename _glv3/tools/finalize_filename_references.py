#!/usr/bin/env python3
"""Finalize authorised GLV3 test-filename references before browser gates.

The repaired source lessons intentionally include `_OUTSTANDING_V3_TEST` in
source filenames. The primary generator already removes it from pupil-facing
lesson filenames and direct links. Four generated same-day evidence-window
support pages are assembled after that copy stage and therefore need the same
narrow literal filename transform. This script proves the exact expected
64-reference universe, transforms only those four generated support pages, and
then scans all 94 generated HTML files for zero residue.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOKEN = "_OUTSTANDING_V3_TEST"
EXPECTED_SUPPORT = {
    "GROW_Estate_v3/Art_Teesside/GROW_ART_SAME_DAY_EVIDENCE_WINDOW.html": 8,
    "GROW_Estate_v3/GROW_ASDAN/GROW_ASDAN_SAME_DAY_EVIDENCE_WINDOW.html": 18,
    "LAUNCH_Estate_v3/Art_Teesside/LAUNCH_ART_SAME_DAY_EVIDENCE_WINDOW.html": 8,
    "LAUNCH_Estate_v3/LAUNCH_ASDAN/LAUNCH_ASDAN_EVIDENCE_WINDOW.html": 30,
}
EXPECTED_REPOSITORY_ROOT_PROVENANCE = 30
QUOTED_HTML = re.compile(r"[\"']([^\"']+\.html(?:#[^\"']*)?)[\"']", re.I)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", "utf-8")


def resolved_file(path: Path) -> Path:
    return path / "index.html" if path.is_dir() else path


def check_support_references(
    root: Path, support_path: Path
) -> tuple[list[str], Counter[str]]:
    """Resolve both authored support-link forms without weakening the gate.

    The transformed `file` values are page-relative links to generated v3
    lessons. The LAUNCH ASDAN page also retains 30 source-provenance values such
    as `LAUNCH_ASDAN/PEQ/...html`; those are intentionally repository-rooted
    references to the protected installed source tree, not links relative to
    the generated support page. Require every quoted HTML reference to resolve,
    reject ambiguity, and record which resolution contract was used.
    """

    failures: list[str] = []
    resolutions: Counter[str] = Counter()
    text = support_path.read_text("utf-8")
    support_rel = support_path.relative_to(root).as_posix()

    for raw in QUOTED_HTML.findall(text):
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target_text = unquote(parsed.path)
        candidates: list[tuple[str, Path]] = []

        if target_text.startswith("/"):
            candidates.append(("repository-root-absolute", root / target_text.lstrip("/")))
        else:
            candidates.append(("support-page-relative", support_path.parent / target_text))
            # Authored source-provenance values are repository-rooted even
            # though they deliberately omit a leading slash for portability.
            if "/" in target_text:
                candidates.append(("repository-root-provenance", root / target_text))

        hits: list[tuple[str, Path]] = []
        seen: set[Path] = set()
        for mode, candidate in candidates:
            target = resolved_file(candidate)
            if target in seen:
                continue
            seen.add(target)
            if target.is_file():
                hits.append((mode, target))

        if not hits:
            failures.append(f"{support_rel} -> {raw}")
            continue
        if len(hits) > 1:
            rendered = ", ".join(
                f"{mode}:{path.relative_to(root).as_posix()}" for mode, path in hits
            )
            failures.append(f"{support_rel} -> {raw} (ambiguous: {rendered})")
            continue
        resolutions[hits[0][0]] += 1

    return failures, resolutions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repo.resolve()
    reconciliation_path = root / "_glv3/COUNT_RECONCILIATION.json"
    static_path = root / "_glv3/GATES_STATIC.json"
    decisions_path = root / "_glv3/DECISIONS.md"
    report_path = root / "_glv3/REPORT.md"

    reconciliation = json.loads(reconciliation_path.read_text("utf-8"))
    source_token_paths = [
        row.get("source_path", "")
        for row in reconciliation.get("html_members", [])
        if row.get("classification") == "deployable lesson" and TOKEN in row.get("source_path", "")
    ]
    if len(source_token_paths) != 80:
        raise SystemExit(f"expected 80 token-bearing deployable source paths, got {len(source_token_paths)}")

    html_files = sorted(
        [*(root / "GROW_Estate_v3").rglob("*.html"), *(root / "LAUNCH_Estate_v3").rglob("*.html")],
        key=lambda path: path.relative_to(root).as_posix(),
    )
    if len(html_files) != 94:
        raise SystemExit(f"expected 94 generated HTML files, got {len(html_files)}")

    discovered: dict[str, int] = {}
    unexpected: list[dict[str, object]] = []
    for path in html_files:
        count = path.read_text("utf-8").count(TOKEN)
        if not count:
            continue
        rel = path.relative_to(root).as_posix()
        discovered[rel] = count
        if rel not in EXPECTED_SUPPORT:
            unexpected.append({"path": rel, "occurrences": count})
    if unexpected:
        raise SystemExit(f"unexpected test-token residue outside support pages: {unexpected}")
    if discovered != EXPECTED_SUPPORT:
        raise SystemExit(f"support-page reference universe changed: {discovered} != {EXPECTED_SUPPORT}")

    for rel, expected in EXPECTED_SUPPORT.items():
        path = root / rel
        text = path.read_text("utf-8")
        actual = text.count(TOKEN)
        if actual != expected:
            raise SystemExit(f"{rel}: expected {expected} references, got {actual}")
        path.write_text(text.replace(TOKEN, ""), "utf-8")

    residue = []
    for path in html_files:
        count = path.read_text("utf-8").count(TOKEN)
        if count:
            residue.append({"path": path.relative_to(root).as_posix(), "occurrences": count})
    if residue:
        raise SystemExit(f"test-token residue remained after deterministic transform: {residue}")

    broken_support_references: list[str] = []
    resolution_counts: Counter[str] = Counter()
    for rel in EXPECTED_SUPPORT:
        failures, resolutions = check_support_references(root, root / rel)
        broken_support_references.extend(failures)
        resolution_counts.update(resolutions)
    if broken_support_references:
        raise SystemExit(f"support-page HTML references do not resolve: {broken_support_references[:20]}")
    if resolution_counts["repository-root-provenance"] != EXPECTED_REPOSITORY_ROOT_PROVENANCE:
        raise SystemExit(
            "repository-root source-provenance universe changed: "
            f"expected {EXPECTED_REPOSITORY_ROOT_PROVENANCE}, got "
            f"{resolution_counts['repository-root-provenance']} ({dict(resolution_counts)})"
        )

    static = json.loads(static_path.read_text("utf-8"))
    gate_name = "filename normalization across complete 94-page universe"
    gates = static.setdefault("gates", [])
    gates[:] = [gate for gate in gates if gate.get("name") != gate_name]
    facts = {
        "source_deployable_paths_with_token": 80,
        "support_pages_transformed": len(EXPECTED_SUPPORT),
        "support_reference_occurrences_transformed": sum(EXPECTED_SUPPORT.values()),
        "generated_html_scanned": len(html_files),
        "generated_residue_occurrences": 0,
        "broken_support_html_references": 0,
        "support_reference_resolution_counts": dict(sorted(resolution_counts.items())),
        "repository_root_provenance_references": EXPECTED_REPOSITORY_ROOT_PROVENANCE,
        "support_page_counts": EXPECTED_SUPPORT,
    }
    gates.append({"name": gate_name, "status": "PASS", "facts": facts})
    static.setdefault("facts", {})["filename_normalization_complete_universe"] = facts
    write_json(static_path, static)

    marker = "## Complete-universe filename-reference finalisation"
    decisions = decisions_path.read_text("utf-8")
    if marker not in decisions:
        decisions += (
            f"\n{marker}\n\n"
            "- Count reconciliation proves 80 deployable source lesson paths carried the authorised "
            f"`{TOKEN}` filename token.\n"
            "- Four generated same-day evidence-window support pages contained the expected 64 embedded source-filename references "
            "after their lesson-copy stage. The generation pipeline removed only that exact token from those references.\n"
            "- The complete 94-page generated HTML universe was then scanned at zero residue, and every quoted HTML reference in the four support pages resolved.\n"
            "- The LAUNCH ASDAN support page deliberately retains 30 repository-rooted source-provenance references to the protected installed tree; these were resolved separately from its generated page-relative lesson links.\n"
        )
        decisions_path.write_text(decisions, "utf-8")

    report = report_path.read_text("utf-8")
    report_marker = "- Complete-universe filename finalisation:"
    if report_marker not in report:
        report += (
            "\n## Complete-universe filename finalisation\n\n"
            f"- Complete-universe filename finalisation: 80 source lesson paths proved the transform non-vacuous; "
            f"64 references across four support pages were normalised; all {len(html_files)} generated HTML files rechecked at zero residue; "
            f"support-page HTML references resolved, including {EXPECTED_REPOSITORY_ROOT_PROVENANCE} retained repository-root source-provenance paths.\n"
        )
        report_path.write_text(report, "utf-8")

    print(json.dumps({"result": "PASS", **facts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
