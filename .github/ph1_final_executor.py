from __future__ import annotations

import ast
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

REPO = "MattRoper1977/Lessons"
BASE = "ae1d3c7af2526781aad6fb82e7cbbf6b87ded380"
CENSUS_TIP = "daf746f5d8894d1b56e203ed34b641b74b0e9522"
BRANCH = "pass-ph1-peq-hardening"
ROOT = Path.cwd()
TRANSPORTS = [Path(".github/workflows/ph1-final-execute.yml"), Path(".github/ph1_final_executor.py")]
C7_EXACT = "pupils who fly can be registered for Level 2 units (UAS coordinator decision)"


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True, text: bool = True, input_text: str | None = None) -> subprocess.CompletedProcess:
    cp = subprocess.run(
        cmd,
        cwd=str(cwd or ROOT),
        check=False,
        text=text,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and cp.returncode != 0:
        raise RuntimeError(
            f"command failed ({cp.returncode}): {' '.join(cmd)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}"
        )
    return cp


def git(*args: str, check: bool = True, cwd: Path | None = None) -> str:
    return run(["git", *args], cwd=cwd, check=check).stdout


def read(path: str | Path) -> str:
    return (ROOT / Path(path)).read_text(encoding="utf-8")


def write(path: str | Path, content: str) -> None:
    p = ROOT / Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def base_text(path: str | Path) -> str:
    rel = Path(path).as_posix()
    return git("show", f"{BASE}:{rel}")


def tracked_at(ref: str) -> list[str]:
    return [x for x in git("ls-tree", "-r", "--name-only", ref).splitlines() if x]


def tracked_now() -> list[str]:
    return [x for x in git("ls-files").splitlines() if x]


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def visible_text(source: str) -> str:
    no_script = re.sub(r"(?is)<script\b[^>]*>.*?</script>", " ", source)
    no_style = re.sub(r"(?is)<style\b[^>]*>.*?</style>", " ", no_script)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", no_style))).strip()


def count_occ(source: str, phrase: str, flags: int = re.I) -> int:
    return len(re.findall(re.escape(phrase), source, flags))


def commit_and_push(message: str, paths: Iterable[str] | None = None) -> str | None:
    if paths is None:
        git("add", "-A")
    else:
        git("add", "--", *list(paths))
    if run(["git", "diff", "--cached", "--quiet"], check=False).returncode == 0:
        return None
    git("commit", "-m", message)
    sha = git("rev-parse", "HEAD").strip()
    git("push", "origin", f"HEAD:{BRANCH}")
    return sha


def repo_gate() -> None:
    origin = git("remote", "get-url", "origin").strip()
    normalized = re.sub(r"\.git$", "", origin)
    if not (
        normalized.endswith("github.com/MattRoper1977/Lessons")
        or normalized == "git@github.com:MattRoper1977/Lessons"
    ):
        raise RuntimeError(f"WRONG REPOSITORY: origin is {origin!r}, expected {REPO}")
    git("fetch", "origin", "main", BRANCH)
    main_sha = git("rev-parse", "origin/main").strip()
    if main_sha != BASE:
        raise RuntimeError(f"origin/main moved: expected {BASE}, measured {main_sha}")
    branch = git("branch", "--show-current").strip()
    if branch != BRANCH:
        raise RuntimeError(f"wrong branch: expected {BRANCH}, measured {branch!r}")
    if run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], check=False).returncode != 0:
        raise RuntimeError(f"BASE {BASE} is not an ancestor of HEAD")
    required = [
        "_passph1/CENSUS.md",
        "_passph1/C7_FINDING.md",
        "_passph1/TEST_COPY_DIVERGENCE.md",
        "_passph1/G4_DETECTOR_FINDING.md",
        "_passph1/SIGNOFF_CLASSIFICATION.md",
        "REGISTER.md",
        "_close/OPEN_ITEMS.md",
    ]
    missing = [p for p in required if not (ROOT / p).is_file()]
    if missing:
        raise RuntimeError(f"required committed evidence missing: {missing}")
    pdfs = [p for p in tracked_now() if p.lower().endswith(".pdf") and "asdan" in p.lower()]
    if pdfs:
        raise RuntimeError(f"tracked ASDAN PDFs found: {pdfs}")


def census_data() -> dict[str, Any]:
    src = read("_passph1/CENSUS.md")
    marker = "## Machine-readable action target summary"
    if marker not in src:
        raise RuntimeError("CENSUS machine-readable action target summary missing")
    tail = src.split(marker, 1)[1]
    m = re.search(r"```json\s*(\{.*?\})\s*```", tail, re.S)
    if not m:
        raise RuntimeError("CENSUS machine JSON block not found")
    data = json.loads(m.group(1))
    lessons = data.get("lessons", {})
    counts = {k: len(lessons.get(k, [])) for k in ("BUILD", "GROW", "LAUNCH")}
    if counts != {"BUILD": 31, "GROW": 18, "LAUNCH": 30}:
        raise RuntimeError(f"lesson derivation mismatch: {counts}")
    missing = [p for group in lessons.values() for p in group if not (ROOT / p).is_file()]
    if missing:
        raise RuntimeError(f"derived production lesson paths missing: {missing}")
    return data


def section_paths(census: str, start: str, end: str) -> list[str]:
    m = re.search(rf"(?ms)^## {re.escape(start)}.*?(?=^## {re.escape(end)}\b)", census)
    if not m:
        return []
    paths: list[str] = []
    for p in re.findall(r"`([^`]+\.html)`", m.group(0)):
        if p not in paths and (ROOT / p).is_file() and not any(part.endswith("_Estate_v3") for part in Path(p).parts):
            paths.append(p)
    return paths


MINIMA_BLOCK = """
<div class="ph1-comsk-minima staff-only" data-ph1="p1" role="note" aria-label="Staff qualification minima">
  <h3>ComSk1 — hard minima (spec v1.2, Oct 2025)</h3>
  <ul>
    <li><strong>Plan · 1.4.1f:</strong> record at least 4 potential audience questions and the planned responses. This number belongs in the plan, not a live-Q&amp;A count.</li>
    <li><strong>Do · 1.5.1:</strong> complete one activity: presentation ≥3 minutes, discussion ≥8 minutes, or text ≥250 words.</li>
    <li><strong>Know · 1.1.2/1.1.3/1.1.4:</strong> at least 3 ways of communicating, at least 4 components of effective communication, and at least 3 difficulties. Four is the odd one out; “range” means three unless a different number is stated.</li>
    <li><strong>Review · 1.6.1:</strong> at least 2 positives and at least 2 areas for further development; also cover active listening, management of difficulties, use of peer feedback and one future situation. A learner who met no difficulty may state that.</li>
    <li><strong>Group work:</strong> a group has at least 3 members.</li>
    <li><strong>Preparation evidence:</strong> where this activity is not linked to assessment for another PEQ unit, retain preparation evidence, including topic research.</li>
  </ul>
</div>
""".strip()


ROUTE_BLOCK = """
<section class="ph1-credit-route staff-only" data-ph1="p3" role="note" aria-label="PEQ qualification credit route">
  <h2>PEQ credit-route framing</h2>
  <ul>
    <li><strong>Award:</strong> all credits are at the level of the qualification.</li>
    <li><strong>Extended Award and Certificate:</strong> no more than 3 credits may come from units at the level above or below.</li>
    <li>The smallest unit is 2 credits, so no more than one adjacent-level unit can contribute.</li>
    <li><strong>Totals:</strong> Entry 3 and Level 1 — 4 / 9 / 14; Level 2 — 4 / 9 / 15; Level 3 — 6 / 11 / 18.</li>
    <li>Level 3 is for learners aged 16+ and is not a route for this cohort.</li>
    <li>Barred combinations apply across all six skill families; where the same family is held at two levels, only the highest-level unit counts.</li>
  </ul>
</section>
""".strip()


PARTIAL_LINE = (
    '<p class="ph1-partial-achievement staff-only" data-ph1="p4"><strong>Staff qualification note · spec v1.2 §5.1:</strong> '
    'if a learner does not reach the credit total for a full qualification, the units achieved can still be certificated.</p>'
)


BUILD_PANEL = """
<section class="ph1-accreditation-status staff-only" data-ph1="p6" role="note" aria-label="Staff accreditation status">
  <h2>Staff accreditation status</h2>
  <p><strong>Regulated PEQ evidence:</strong> evidence is tied to a named PEQ unit and criterion references, formally assessed by the centre and internally quality assured.</p>
  <p><strong>Other activity:</strong> ASDAN Short Course and AQA UAS activity is separate from regulated PEQ evidence. A Short Course certificate does not convert automatically into PEQ credit.</p>
  <p>Any prior-learning claim must follow ASDAN’s RPL procedure and can count only when achieved within 3 years of the qualification quality-assurance date.</p>
  <p><strong>Dated check — re-check before use:</strong> Checked 17 Aug 2026 on asdan.org.uk: the ASDAN e-portfolio is closed to new registrations and access for existing registrations ends 31 August 2026; Short Course student books remain available. If any learner evidence is held in that e-portfolio, export it. Re-check before use.</p>
</section>
""".strip()


VOC_PANEL = """
<section class="ph1-accreditation-status staff-only" data-ph1="p6-vocational" role="note" aria-label="Staff vocational accreditation status">
  <h2>Staff vocational accreditation status</h2>
  <p><strong>Regulated PEQ evidence:</strong> evidence is tied to a named PEQ unit and criterion references, formally assessed by the centre and internally quality assured.</p>
  <p><strong>Other activity:</strong> ASDAN Short Course, Vocational Taster and AQA UAS activity is separate from regulated PEQ evidence and does not convert automatically into PEQ credit.</p>
  <p>Any prior-learning claim must follow ASDAN’s RPL procedure and can count only when achieved within 3 years of the qualification quality-assurance date.</p>
  <p><strong>Dated check — re-check before use:</strong> Checked 17 Aug 2026 on asdan.org.uk: the ASDAN e-portfolio is closed to new registrations and access for existing registrations ends 31 August 2026; Short Course student books remain available. If any learner evidence is held in that e-portfolio, export it. Re-check before use.</p>
  <p><strong>Vocational Taster check:</strong> ASDAN has said it plans to withdraw all Vocational Taster titles, with registrations and books available to 31 Dec 2026 and final certification by 31 Aug 2027. Confirm whether this strand’s banked titles are affected.</p>
</section>
""".strip()


def insert_before_body(source: str, block: str) -> str:
    idx = source.lower().rfind("</body>")
    if idx < 0:
        raise RuntimeError("</body> not found")
    return source[:idx] + "\n" + block + "\n" + source[idx:]


def insert_after_print_witness(source: str, block: str) -> str:
    m = re.search(r"(?is)<div\b[^>]*\bid=[\"']print-witness[\"'][^>]*>", source)
    if not m:
        raise RuntimeError("print-witness opening div not found")
    return source[:m.end()] + "\n" + block + source[m.end():]


def apply_p1(c2_paths: list[str]) -> tuple[list[str], dict[str, Any]]:
    expected = 2
    if len(c2_paths) != expected:
        report = (
            "# PH-1 P1 count mismatch\n\n"
            f"C2 committed census predicted 2 production pages; resolved {len(c2_paths)}: {c2_paths}. "
            "No target was invented and no lesson file was changed.\n"
        )
        write("_passph1/P1_COUNT_MISMATCH.md", report)
        sha = commit_and_push(f"PH-1 P1: C2 count {len(c2_paths)} not 2; 0 lesson edits", ["_passph1/P1_COUNT_MISMATCH.md"])
        return [], {"status": "NOT-DONE", "why": "C2 count mismatch", "commit": sha}
    changed = []
    for path in c2_paths:
        src = read(path)
        if 'data-ph1="p1"' in src:
            raise RuntimeError(f"P1 block already present before P1 in {path}")
        out = insert_after_print_witness(src, MINIMA_BLOCK)
        write(path, out)
        changed.append(path)
    required = ["1.4.1f", "≥3 minutes", "≥8 minutes", "≥250 words", "1.1.2/1.1.3/1.1.4", "at least 4 components", "at least 3 difficulties", "at least 2 positives", "at least 2 areas", "at least 3 members"]
    for path in changed:
        src = read(path)
        missing = [token for token in required if token not in src]
        if missing:
            raise RuntimeError(f"P1 block incomplete in {path}: {missing}")
        if re.search(r"(?is)(ComSk1|Communication).{0,100}(10\s*-?\s*hour|600\s*minute)", visible_text(src)):
            raise RuntimeError(f"P1 introduced a forbidden Communication 10-hour claim in {path}")
    sha = commit_and_push(f"PH-1 P1: ComSk1 minima completed on {len(changed)}/{expected} C2 pages; omissions 20->0", changed)
    return changed, {"status": "DONE", "pages": len(changed), "commit": sha}


def replace_ci(source: str, old: str, new: str) -> tuple[str, int]:
    return re.subn(re.escape(old), new, source, flags=re.I)


def apply_p2() -> tuple[list[str], dict[str, Any]]:
    targets = [
        "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
        "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
    ]
    total_before = 0
    total_after = 0
    changed: list[str] = []
    for path in targets:
        src = read(path)
        before = len(re.findall(r"(?i)sign[ -]?off(?: the unit)?", src))
        total_before += before
        out = src
        replacements = [
            ("Review Progress and Sign Off the Unit", "Review Progress and Prepare for Assessor Sign-Off"),
            ("Sign Off the Unit", "Prepare for Assessor Sign-Off"),
            ("SIGN-OFF THE UNIT", "PREPARE FOR ASSESSOR SIGN-OFF"),
            ("SIGN OFF THE UNIT", "PREPARE FOR ASSESSOR SIGN-OFF"),
            ("REVIEW and\nSIGN OFF", "REVIEW and\nPREPARE FOR ASSESSOR SIGN-OFF"),
            ("REVIEW AND\nSIGN OFF", "REVIEW AND\nPREPARE FOR ASSESSOR SIGN-OFF"),
            ("SIGN-OFF", "ASSESSOR SIGN-OFF"),
            ("SIGN OFF", "PREPARE FOR ASSESSOR SIGN-OFF"),
        ]
        for old, new in replacements:
            out, _ = replace_ci(out, old, new)
        claim_repls = [
            (r"(?i)Communication skills \(ComSk1\)\s*[—-]\s*unit complete", "Communication skills (ComSk1) — evidence prepared for assessor review"),
            (r"(?i)Communication \(ComSk1\) complete", "Communication (ComSk1) evidence prepared for assessor review"),
            (r"(?i)Communication unit is complete", "Communication evidence is ready for assessor review"),
            (r"(?i)unit closes", "evidence review prepares the unit for assessor sign-off"),
            (r"(?i)close the Communication unit", "prepare the Communication evidence for assessor sign-off"),
            (r"(?i)closes Communication", "prepares Communication evidence for assessor review"),
            (r"(?i)close the unit", "prepare for assessor sign-off"),
        ]
        for pat, repl in claim_repls:
            out = re.sub(pat, repl, out)
        after = len(re.findall(r"(?i)Sign Off the Unit|SIGN[ -]?OFF THE UNIT", out))
        total_after += after
        if out != src:
            write(path, out)
            changed.append(path)
    if total_before == 0:
        write("_passph1/P2_COUNT_MISMATCH.md", "# PH-1 P2 count mismatch\n\nThe two committed B1 target pages contained zero matching unit-sign-off strings. No change was invented.\n")
        sha = commit_and_push("PH-1 P2: B1 target count 0; 0 edits", ["_passph1/P2_COUNT_MISMATCH.md"])
        return [], {"status": "NOT-DONE", "why": "B1 target count zero", "commit": sha}
    if total_after != 0:
        raise RuntimeError(f"P2 left {total_after} Sign Off the Unit variants in B1 targets")
    sha = commit_and_push(f"PH-1 P2: 101 C3 occurrences classified; B1 unit-sign-off strings {total_before}->0; B3 untouched", changed)
    return changed, {"status": "DONE", "b1_before": total_before, "b1_after": total_after, "commit": sha}


def neutralise_route_text(source: str) -> str:
    if 'data-ph1="p3"' in source:
        raise RuntimeError("P3 block already present")
    parts = re.split(r"(<[^>]+>)", source)
    in_script = 0
    in_style = 0
    route_tokens = re.compile(r"(?i)(Extended Award|\bCertificate\b|qualification size|adjacent[- ]level|level above or below|smallest unit|barred combination|4\s*/\s*9\s*/\s*14|4\s*/\s*9\s*/\s*15|6\s*/\s*11\s*/\s*18|Award\s*/\s*Extended Award)")
    for i, part in enumerate(parts):
        if not part.startswith("<"):
            if not in_script and not in_style and route_tokens.search(html.unescape(part)):
                parts[i] = " Staff qualification route: see the PEQ credit-route block on this page. "
            continue
        low = part.lower()
        if re.match(r"<script\b", low):
            in_script += 1
        elif re.match(r"</script\b", low):
            in_script = max(0, in_script - 1)
        elif re.match(r"<style\b", low):
            in_style += 1
        elif re.match(r"</style\b", low):
            in_style = max(0, in_style - 1)
    out = "".join(parts)
    out = re.sub(r"(?i)\beither the level above OR below, but not both\b", "at the level above or below", out)
    out = re.sub(r"(?i)\bnot both\b", "within the adjacent-level credit cap", out)
    return insert_before_body(out, ROUTE_BLOCK)


def apply_p3(c5_paths: list[str]) -> tuple[list[str], dict[str, Any]]:
    if len(c5_paths) != 6:
        report = "# PH-1 P3 count mismatch\n\n" + f"Committed C5 expected 6 production pages; resolved {len(c5_paths)}: {c5_paths}. No route target was invented.\n"
        write("_passph1/P3_COUNT_MISMATCH.md", report)
        sha = commit_and_push(f"PH-1 P3: C5 count {len(c5_paths)} not 6; 0 route edits", ["_passph1/P3_COUNT_MISMATCH.md"])
        return [], {"status": "NOT-DONE", "why": "C5 count mismatch", "commit": sha}
    changed: list[str] = []
    for path in c5_paths:
        src = read(path)
        out = neutralise_route_text(src)
        if C7_EXACT in src and C7_EXACT not in out:
            raise RuntimeError(f"P3 would remove the accepted C7 claim without P8 authority: {path}")
        write(path, out)
        changed.append(path)
    for path in changed:
        src = read(path)
        if src.count('data-ph1="p3"') != 1:
            raise RuntimeError(f"P3 block count is not 1 in {path}")
        before, _, after = src.partition('<section class="ph1-credit-route')
        _, _, after_tail = after.partition("</section>")
        outside = visible_text(before + after_tail)
        leftovers = [t for t in ("Extended Award", "Certificate", "not both") if t.lower() in outside.lower()]
        if leftovers:
            raise RuntimeError(f"P3 route framing remains outside canonical block in {path}: {leftovers}")
    sha = commit_and_push(f"PH-1 P3: qualification route wording corrected on {len(changed)}/6 C5 pages; adjacent over-restriction removed", changed)
    return changed, {"status": "DONE", "pages": len(changed), "commit": sha}


def apply_p4() -> tuple[list[str], dict[str, Any]]:
    targets = ["BUILD_ASDAN/BUILD_ASDAN_Hub.html", "GROW_ASDAN/GROW_ASDAN_Hub.html", "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html", "build_dt_upcycling.html"]
    missing = [p for p in targets if not (ROOT / p).is_file()]
    if missing:
        write("_passph1/P4_MISSING_HUB.md", "# PH-1 P4 missing hub\n\n" + "\n".join(f"- `{p}`" for p in missing) + "\n")
        sha = commit_and_push(f"PH-1 P4: {len(missing)} suite hubs missing; partial-achievement line not invented there", ["_passph1/P4_MISSING_HUB.md"])
        targets = [p for p in targets if p not in missing]
    else:
        sha = None
    changed = []
    for path in targets:
        src = read(path)
        if 'data-ph1="p4"' in src:
            continue
        write(path, insert_before_body(src, PARTIAL_LINE))
        changed.append(path)
    commit = commit_and_push(f"PH-1 P4: partial-achievement fact added to {len(changed)}/{len(targets)} suite hubs", changed) if changed else sha
    return changed, {"status": "DONE" if not missing else "PARTIAL", "pages": len(changed), "missing": missing, "commit": commit}


def apply_p5(c6_count: int) -> tuple[list[str], dict[str, Any]]:
    content = f"""# PH-1 P5 — Level 1 demand report

- Source: committed C6 census at `{CENSUS_TIP}`.
- Findings: **{c6_count}** production instructions asking an L1 learner to “outline” at ThSk1 1.1.3, 1.1.4 or 1.2.1.
- Lesson edits: **0**.

Version 1.2 lowered the demand at these Level 1 references. PH-1 does not raise, lower or rewrite pupil demand by machine. Matt should decide whether any future live wording should be relaxed; no top-up instruction is recommended merely to mirror an older booklet.
"""
    write("_passph1/L1_DEMAND_REPORT.md", content)
    sha = commit_and_push(f"PH-1 P5: L1 demand report committed; C6 findings {c6_count}; 0 lesson edits", ["_passph1/L1_DEMAND_REPORT.md"])
    return [], {"status": "DONE", "findings": c6_count, "commit": sha}


def apply_p6() -> tuple[list[str], dict[str, Any]]:
    build_targets = ["BUILD_ASDAN/BUILD_ASDAN_Hub.html", "build_asdan.html", "BUILD_ASDAN/Careers/START_HERE.html", "BUILD_ASDAN/Community_Project/START_HERE.html", "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html", "BUILD_ASDAN/FoodWise/START_HERE.html", "BUILD_ASDAN/Living_Independently/START_HERE.html"]
    voc = "LAUNCH_ASDAN/Vocational/START_HERE.html"
    all_targets = build_targets + [voc]
    missing = [p for p in all_targets if not (ROOT / p).is_file()]
    changed: list[str] = []
    for path in build_targets:
        if path in missing:
            continue
        src = read(path)
        if 'data-ph1="p6"' not in src:
            write(path, insert_before_body(src, BUILD_PANEL)); changed.append(path)
    if voc not in missing:
        src = read(voc)
        if 'data-ph1="p6-vocational"' not in src:
            write(voc, insert_before_body(src, VOC_PANEL)); changed.append(voc)
    status = "DONE" if not missing else "PARTIAL"
    if missing:
        write("_passph1/P6_MISSING_HUBS.md", "# PH-1 P6 missing staff surfaces\n\n" + "\n".join(f"- `{p}`" for p in missing) + "\n"); paths = changed + ["_passph1/P6_MISSING_HUBS.md"]
    else:
        paths = changed
    sha = commit_and_push(f"PH-1 P6: accreditation-status panels added to {len(changed)}/{len(all_targets)} hub or START_HERE surfaces", paths)
    return changed, {"status": status, "pages": len(changed), "missing": missing, "commit": sha}


def apply_p7() -> tuple[list[str], dict[str, Any]]:
    content = """# PH-1 P7 — non-deployment record

PH-1 deliberately did not deploy:

- any tool that stores a candidate name or identifier in `localStorage`;
- any “unit achieved” badge or automatic credit claim;
- any PEQ credit attached to a challenge code such as `PEQ002` — challenge codes carry no credit of their own.

No pupil data feature, automatic qualification decision or challenge-code credit mechanism was added.
"""
    write("_passph1/P7_NON_DEPLOYMENT.md", content)
    sha = commit_and_push("PH-1 P7: 3 prohibited deployment classes recorded; 0 deployed", ["_passph1/P7_NON_DEPLOYMENT.md"])
    return [], {"status": "DONE", "deployed": 0, "commit": sha}


def retire_transport() -> str | None:
    existing = [p.as_posix() for p in TRANSPORTS if p.exists()]
    if existing:
        git("rm", "--", *existing)
        return commit_and_push("PH-1 transport cleanup: final executor retired")
    return None


def extract_scripts(source: str) -> list[str]:
    blocks: list[str] = []
    for attrs, body in re.findall(r"(?is)<script\b([^>]*)>(.*?)</script>", source):
        tm = re.search(r"(?i)\btype\s*=\s*[\"']([^\"']+)", attrs)
        if tm and tm.group(1).lower() not in {"text/javascript", "application/javascript", "module", ""}:
            continue
        blocks.append(body)
    return blocks


def gate_g1(touched_html: list[str]) -> dict[str, Any]:
    failures = []; checked = 0
    with tempfile.TemporaryDirectory(prefix="ph1-nodecheck-") as td:
        for path in touched_html:
            for idx, body in enumerate(extract_scripts(read(path)), 1):
                checked += 1; js = Path(td) / f"{checked}.js"; js.write_text(body, encoding="utf-8")
                cp = run(["node", "--check", str(js)], check=False)
                if cp.returncode: failures.append({"file": path, "block": idx, "stderr": cp.stderr[-3000:]})
    return {"pass": not failures, "checked_blocks": checked, "failures": failures}


JSDOM_RUNNER = r"""
const fs = require('fs');
const {JSDOM, VirtualConsole} = require('/tmp/ph1-node/node_modules/jsdom');
const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const errors = [];
const vc = new VirtualConsole();
vc.on('error', (...a) => errors.push('console.error: ' + a.map(String).join(' ')));
vc.on('jsdomError', e => errors.push('jsdomError: ' + (e && e.stack ? e.stack : String(e))));
class FakeNode {connect(){return this} disconnect(){} start(){} stop(){} setValueAtTime(){} linearRampToValueAtTime(){} exponentialRampToValueAtTime(){} addColorStop(){}}
class FakeAudioContext {constructor(){this.currentTime=0;this.state='running';this.destination=new FakeNode()} createOscillator(){const n=new FakeNode();n.frequency={value:0};n.type='sine';return n} createGain(){const n=new FakeNode();n.gain=new FakeNode();return n} createBiquadFilter(){return new FakeNode()} createAnalyser(){const n=new FakeNode();n.frequencyBinCount=32;n.getByteFrequencyData=a=>a.fill(0);return n} createBufferSource(){return new FakeNode()} createBuffer(){return {getChannelData:()=>new Float32Array(1)}} resume(){this.state='running';return Promise.resolve()} close(){return Promise.resolve()}}
const noop = ()=>{};
(async()=>{let dom;try{dom=new JSDOM(html,{runScripts:'dangerously',url:'https://example.test/'+encodeURIComponent(file),pretendToBeVisual:true,virtualConsole:vc,beforeParse(win){win.matchMedia=win.matchMedia||(q=>({matches:false,media:q,onchange:null,addListener:noop,removeListener:noop,addEventListener:noop,removeEventListener:noop,dispatchEvent:()=>false}));win.requestAnimationFrame=cb=>setTimeout(()=>cb(Date.now()),1);win.cancelAnimationFrame=id=>clearTimeout(id);win.scrollTo=noop;win.print=noop;win.alert=noop;win.confirm=()=>true;win.prompt=()=>null;win.open=()=>({document:{write:noop,close:noop},focus:noop,print:noop,close:noop});win.fetch=async()=>({ok:true,status:200,json:async()=>({}),text:async()=>'',blob:async()=>new win.Blob()});win.ResizeObserver=class{observe(){}unobserve(){}disconnect(){}};win.IntersectionObserver=class{constructor(cb){this.cb=cb}observe(el){this.cb([{isIntersecting:true,target:el}])}unobserve(){}disconnect(){}};win.AudioContext=FakeAudioContext;win.webkitAudioContext=FakeAudioContext;win.speechSynthesis={speak:noop,cancel:noop,pause:noop,resume:noop,getVoices:()=>[]};win.SpeechSynthesisUtterance=class{constructor(t=''){this.text=t}};win.URL.createObjectURL=()=> 'blob:ph1';win.URL.revokeObjectURL=noop;win.navigator.vibrate=()=>true;try{Object.defineProperty(win.navigator,'clipboard',{value:{writeText:async()=>{},readText:async()=>''}})}catch(e){}win.Element.prototype.scrollIntoView=noop;win.HTMLMediaElement.prototype.play=async function(){};win.HTMLMediaElement.prototype.pause=noop;win.HTMLCanvasElement.prototype.getContext=function(){const target={canvas:this,measureText:()=>({width:0}),createLinearGradient:()=>new FakeNode(),createRadialGradient:()=>new FakeNode(),getImageData:()=>({data:new Uint8ClampedArray(4)}),putImageData:noop};return new Proxy(target,{get:(o,p)=>p in o?o[p]:noop,set:(o,p,v)=>(o[p]=v,true)})};if(!win.crypto.randomUUID)win.crypto.randomUUID=()=> '00000000-0000-4000-8000-000000000000';win.CSS=win.CSS||{};win.CSS.escape=win.CSS.escape||(s=>String(s).replace(/[^a-zA-Z0-9_-]/g,'_'))}});await new Promise(r=>setTimeout(r,350));if(!dom.window.document.documentElement||!dom.window.document.body)errors.push('page did not render a document body')}catch(e){errors.push(e&&e.stack?e.stack:String(e))}if(dom){try{dom.window.close()}catch(e){}}if(errors.length){console.error(JSON.stringify(errors));process.exit(1)}console.log(JSON.stringify({ok:true,file}))})().catch(e=>{console.error(e&&e.stack?e.stack:String(e));process.exit(1)});
"""


def gate_g2(touched_html: list[str]) -> dict[str, Any]:
    runner = Path("/tmp/ph1-jsdom-runner.cjs"); runner.write_text(JSDOM_RUNNER, encoding="utf-8"); failures=[]
    for path in touched_html:
        cp=run(["node",str(runner),str((ROOT/path).resolve())],check=False)
        if cp.returncode: failures.append({"file":path,"stdout":cp.stdout[-2000:],"stderr":cp.stderr[-5000:]})
    return {"pass":not failures,"checked":len(touched_html),"failures":failures}


def print_section_count(source: str) -> int:
    return len(re.findall(r"(?is)class=[\"'][^\"']*\bprint-section\b", source))


def gate_g3(touched_html: list[str]) -> dict[str, Any]:
    diffs={}
    for path in touched_html:
        b=print_section_count(base_text(path));t=print_section_count(read(path))
        if b!=t:diffs[path]={"base":b,"tip":t}
    return {"pass":not diffs,"checked":len(touched_html),"diffs":diffs}


def witness_flags(source: str) -> tuple[bool,bool,dict[str,str]]:
    text=visible_text(source)
    patterns4=[r"\b4\b.{0,260}\b(?:assessor|staff|witness)\b.{0,180}\b(?:declaration|confirmation|signature|record)\b",r"\b(?:assessor|staff|witness)\b.{0,180}\b(?:declaration|confirmation|signature|record)\b.{0,260}\b4\b",r"\b4\b.{0,180}\b(?:assessor|staff|witness)\b"]
    patterns5=[r"\b5\b.{0,260}\b(?:learner|candidate)\b.{0,180}\b(?:declaration|confirmation|signature|record)\b",r"\b(?:learner|candidate)\b.{0,180}\b(?:declaration|confirmation|signature|record)\b.{0,260}\b5\b",r"\b5\b.{0,180}\b(?:learner|candidate)\b"]
    m4=next((re.search(p,text,re.I|re.S) for p in patterns4 if re.search(p,text,re.I|re.S)),None);m5=next((re.search(p,text,re.I|re.S) for p in patterns5 if re.search(p,text,re.I|re.S)),None)
    return bool(m4),bool(m5),{"section4":m4.group(0)[:500] if m4 else "","section5":m5.group(0)[:500] if m5 else ""}


def derive_witness_set(ref: str) -> list[str]:
    out=[]
    for path in tracked_at(ref):
        if not path.lower().endswith((".html",".htm")):continue
        try:src=git("show",f"{ref}:{path}") if ref!="WORKTREE" else read(path)
        except Exception:continue
        low=src.lower()
        if "assessor witness statement" in low or 'id="print-witness"' in low or "id='print-witness'" in low:out.append(path)
    return sorted(out)


def gate_g4() -> dict[str, Any]:
    base_set=derive_witness_set(BASE);tip_set=derive_witness_set("WORKTREE");missing_sections={}
    for path in tip_set:
        f4,f5,snippets=witness_flags(read(path))
        if not(f4 and f5):missing_sections[path]={"section4":f4,"section5":f5,"snippets":snippets}
    mutation=[]
    for path in tip_set[:3]:
        src=read(path);text=visible_text(src);f4,f5,snippets=witness_flags(src);mut4=text.replace(snippets["section4"],"",1) if snippets["section4"] else text;mut5=text.replace(snippets["section5"],"",1) if snippets["section5"] else text;c4,_,_=witness_flags(mut4);_,c5,_=witness_flags(mut5);mutation.append({"file":path,"base_detected":f4 and f5,"remove4_caught":not c4,"remove5_caught":not c5})
    mutation_pass=bool(mutation) and all(x["base_detected"] and x["remove4_caught"] and x["remove5_caught"] for x in mutation)
    return {"pass":base_set==tip_set and not missing_sections and mutation_pass,"base_surface_count":len(base_set),"tip_surface_count":len(tip_set),"set_equal":base_set==tip_set,"missing_sections":missing_sections,"mutation_controls":mutation}


def load_old_executor() -> Any:
    out=Path("/tmp/ph1-old-executor.py");chunks=[]
    for name in ("ph1_payload_00.b64","ph1_payload_01.b64","ph1_payload_02.b64"):chunks.append(git("show",f"1cfca0ca2c5c7ebfcbc875d6efc85ee20addc239:.github/{name}"))
    import base64,gzip
    out.write_bytes(gzip.decompress(base64.b64decode("".join(chunks))));spec=importlib.util.spec_from_file_location("ph1_old_executor",out)
    if spec is None or spec.loader is None:raise RuntimeError("cannot load old executor")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod


def normalise_path_set(value: Any) -> set[str] | None:
    if isinstance(value,dict):
        for key in ("set","paths","files","sentinel","lessons"):
            if key in value:return normalise_path_set(value[key])
        candidates=value.keys()
    elif isinstance(value,(set,list,tuple)):candidates=value
    else:return None
    result=set()
    for item in candidates:
        if isinstance(item,Path):item=item.as_posix()
        if not isinstance(item,str):return None
        if "/" in item or item.lower().endswith((".html",".htm")):result.add(item.replace("\\","/"))
    return result or None


def try_sentinel_function(mod: Any,fn: Any,root: Path) -> tuple[set[str],str] | None:
    import inspect
    old_cwd=Path.cwd();old_root=getattr(mod,"ROOT",None);strategies=[("root-path",(root,)),("root-string",(str(root),)),("no-args-cwd",())]
    try:
        for label,args in strategies:
            try:
                os.chdir(root)
                if hasattr(mod,"ROOT"):setattr(mod,"ROOT",root)
                inspect.signature(fn).bind_partial(*args);value=fn(*args);path_set=normalise_path_set(value)
                if path_set:return path_set,label
            except Exception:continue
    finally:
        os.chdir(old_cwd)
        if old_root is not None:setattr(mod,"ROOT",old_root)
    return None


def derive_old_sentinel(mod: Any,root: Path) -> tuple[set[str],str]:
    for name in dir(mod):
        obj=getattr(mod,name)
        if callable(obj) and ("sentinel" in name.lower() or "derive" in name.lower()):
            result=try_sentinel_function(mod,obj,root)
            if result:s,strategy=result;return s,f"{name}:{strategy}"
    raise RuntimeError("no non-empty sentinel derivation callable found in the prior PH-1 executor")


def gate_g5() -> dict[str, Any]:
    mod=load_old_executor()
    with tempfile.TemporaryDirectory(prefix="ph1-base-worktree-") as td:
        base_root=Path(td)/"base";git("worktree","add","--detach",str(base_root),BASE)
        try:bset,bstrategy=derive_old_sentinel(mod,base_root);tset,tstrategy=derive_old_sentinel(mod,ROOT)
        finally:git("worktree","remove","--force",str(base_root),check=False)
    return {"pass":bset==tset and bstrategy==tstrategy,"base_count":len(bset),"tip_count":len(tset),"set_equal":bset==tset,"base_strategy":bstrategy,"tip_strategy":tstrategy,"added":sorted(tset-bset),"removed":sorted(bset-tset)}


def production_texts(census: dict[str, Any]) -> dict[str,str]:
    paths=set()
    for group in census["lessons"].values():paths.update(group)
    for group in census.get("hubs",{}).values():paths.update(group)
    paths.update(census.get("dt",{}).get("planning",[]));paths.add(census.get("dt",{}).get("hub","build_dt_upcycling.html"))
    return {p:read(p) for p in sorted(paths) if p and (ROOT/p).is_file()}


def gate_g6(census: dict[str, Any]) -> dict[str, Any]:
    texts=production_texts(census);joined="\n".join(visible_text(v) for v in texts.values());delivering=len(re.findall(r"(?i)Delivering a Project",joined));doubled=len(re.findall(re.escape("ASDAN Studio · ASDAN Studio"),joined));not_both=len(re.findall(r"(?i)\bnot both\b",joined));comm10=len(re.findall(r"(?is)(?:ComSk1|Communication).{0,150}(?:10\s*-?\s*hour|600\s*minute)|(?:10\s*-?\s*hour|600\s*minute).{0,150}(?:ComSk1|Communication)",joined));c7=sum(src.count(C7_EXACT) for src in texts.values())
    return {"pass":delivering==0 and doubled==0 and not_both==0 and comm10==0 and c7==1,"Delivering a Project":delivering,"doubled Studio":doubled,"not both":not_both,"Communication 10h":comm10,"accepted C7 exact claim":c7,"P8":"NOT-DONE — no standalone AUTHORISE P8 L2 CLAIM line supplied"}


def reduced_motion_blocks(source: str) -> list[str]:
    result=[]
    for m in re.finditer(r"@media\s*\([^)]*prefers-reduced-motion[^)]*\)\s*\{",source,re.I):
        i=m.start();pos=m.end();depth=1;in_str=None;esc=False
        while pos<len(source) and depth:
            ch=source[pos]
            if in_str:
                if esc:esc=False
                elif ch=="\\":esc=True
                elif ch==in_str:in_str=None
            else:
                if ch in "'\"":in_str=ch
                elif ch=="{":depth+=1
                elif ch=="}":depth-=1
            pos+=1
        result.append(source[i:pos])
    return result


def gate_g7(touched_html: list[str]) -> dict[str, Any]:
    diffs={}
    for path in touched_html:
        b=reduced_motion_blocks(base_text(path));t=reduced_motion_blocks(read(path))
        if b!=t:diffs[path]={"base_blocks":len(b),"tip_blocks":len(t),"base_sha":sha256_text("\n".join(b)),"tip_sha":sha256_text("\n".join(t))}
    return {"pass":not diffs,"checked":len(touched_html),"diffs":diffs}


VOID={"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"};OPTIONAL={"li","p","dt","dd","tr","th","td","option","thead","tbody","tfoot","colgroup"}
class BalanceParser(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.errors=[]
    def handle_starttag(self,tag,attrs):
        tag=tag.lower()
        if tag in VOID:return
        if self.stack and tag in OPTIONAL and self.stack[-1]==tag:self.stack.pop()
        if tag=="li" and self.stack and self.stack[-1]=="li":self.stack.pop()
        if tag=="tr" and self.stack and self.stack[-1]=="tr":self.stack.pop()
        if tag in {"td","th"} and self.stack and self.stack[-1] in {"td","th"}:self.stack.pop()
        self.stack.append(tag)
    def handle_startendtag(self,tag,attrs):return
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag in VOID:return
        if tag in self.stack:
            while self.stack:
                top=self.stack.pop()
                if top==tag:break
                if top not in OPTIONAL:self.errors.append(f"misnested: closed {top} while seeking {tag}")
        elif tag not in OPTIONAL:self.errors.append(f"unmatched closing tag: {tag}")


def gate_g8(touched_html: list[str]) -> dict[str, Any]:
    failures={}
    for path in touched_html:
        src=read(path);parser=BalanceParser();parser.feed(src);parser.close();remaining=[x for x in parser.stack if x not in OPTIONAL];ends=bool(re.search(r"</html>\s*$",src,re.I))
        if parser.errors or remaining or not ends:failures[path]={"errors":parser.errors[:20],"remaining":remaining[:20],"ends_html":ends}
    return {"pass":not failures,"checked":len(touched_html),"failures":failures}


def gate_g9(allowed_exact: set[str]) -> dict[str, Any]:
    changed=[x for x in git("diff","--name-only",BASE,"HEAD").splitlines() if x];bad=[]
    for path in changed:
        if path.startswith("_passph1/") or path in {"REGISTER.md","_close/OPEN_ITEMS.md"} or path in allowed_exact:continue
        bad.append(path)
    return {"pass":not bad,"changed_count":len(changed),"bad":bad,"changed":changed}


def localstorage_keys(source: str) -> set[str]:
    return set(re.findall(r"localStorage\s*\.\s*(?:getItem|setItem|removeItem)\s*\(\s*['\"]([^'\"]+)['\"]",source))


def gate_g10(touched_html: list[str]) -> dict[str, Any]:
    pdfs=[p for p in tracked_now() if p.lower().endswith(".pdf") and "asdan" in p.lower()];added_keys={}
    for path in touched_html:
        extra=sorted(localstorage_keys(read(path))-localstorage_keys(base_text(path)))
        if extra:added_keys[path]=extra
    verifiers=[p for p in tracked_now() if p.endswith("verify_fixture_names.mjs")];verifier_results=[]
    for path in verifiers:
        cp=run(["node",path],check=False);verifier_results.append({"path":path,"returncode":cp.returncode,"stdout":cp.stdout[-2000:],"stderr":cp.stderr[-2000:]})
    verifier_pass=bool(verifier_results) and all(x["returncode"]==0 for x in verifier_results)
    return {"pass":not pdfs and not added_keys and verifier_pass,"tracked_asdan_pdfs":pdfs,"new_localStorage_keys":added_keys,"fixture_verifiers":verifier_results}


def append_records(results: dict[str, Any],commits: dict[str,str|None]) -> str:
    reg=read("REGISTER.md");nums=[int(x) for x in re.findall(r"(?m)^##\s+R-PH(\d+)\b",reg)];n=max(nums,default=0)+1;rid=f"R-PH{n:02d}";gate_summary=", ".join(f"{g}={'PASS' if v.get('pass') else 'FAIL'}" for g,v in results.items())
    reg+=f"""

## {rid} — PH-1 PEQ hardening deploy (2026-08-18)

- Repository: `MattRoper1977/Lessons`; immutable BASE `{BASE}`; branch `{BRANCH}`.
- Census authority: `{CENSUS_TIP}` — BUILD 31 + GROW 18 + LAUNCH 30 = 79 lessons.
- P1–P7 were handled as claim-accuracy/staff-layer changes only; P8 was not authorised and the accepted live Level 2 registration sentence remains unchanged.
- Gates: {gate_summary}.
- Commit map: {json.dumps(commits,sort_keys=True)}.
- Held on branch for Matt: no merge, no PR and no site-repository work.
""";write("REGISTER.md",reg)
    oi=read("_close/OPEN_ITEMS.md")
    if re.search(r"(?m)^\|\s*42\s*\|",oi):raise RuntimeError("open-item 42 already exists; refusing to renumber or overwrite")
    oi+=f"""

## Added by PH-1 PEQ hardening (2026-08-18), branch `{BRANCH}`

| # | open item | status / blocker | recorded in |
|--:|---|---|---|
| 42 | **Live Level 2 registration claim.** Should the sentence “{C7_EXACT}” be replaced with neutral centre-confirmation wording under a separately authorised P8? | **AWAITING-WORD** — P8 was not authorised; production wording remains unchanged. | `_passph1/C7_FINDING.md` |
| 43 | **Level 1 verb demand.** Should any live page be relaxed where PEQ v1.2 lowered ThSk1 1.1.3, 1.1.4 and 1.2.1 relative to the September 2025 booklets? | **AWAITING-WORD** — PH-1 reports only and makes no pupil-demand edit. | `_passph1/L1_DEMAND_REPORT.md` |
| 44 | **Pupil-task sign-off wording.** Which B3 sign-off occurrences, if any, should be re-authored where changing the words would alter what a pupil does? | **AWAITING-WORD** — preserved byte-for-byte by P2. | `_passph1/SIGNOFF_CLASSIFICATION.md` |
| 45 | **LAUNCH Vocational titles.** Are this strand’s banked titles ASDAN Vocational Taster titles affected by the announced withdrawal timetable? | **AWAITING-WORD** — centre/title confirmation required. | `LAUNCH_ASDAN/Vocational/START_HERE.html` |
| 46 | **ASDAN e-portfolio evidence.** Is any learner evidence still held in the e-portfolio that needs exporting before access ends on 31 August 2026? | **CENTRE-ACTION / AWAITING-WORD** — the repository cannot answer this. | BUILD accreditation panels added by PH-1 |
""";write("_close/OPEN_ITEMS.md",oi)
    sha=commit_and_push(f"{rid} PH-1 records: REGISTER append + OPEN_ITEMS 42-46",["REGISTER.md","_close/OPEN_ITEMS.md"]);return sha or git("rev-parse","HEAD").strip()


def make_gate_failure(results,item_status,commits):
    failed={k:v for k,v in results.items() if not v.get("pass")};body="# PH-1 gate stop\n\n"+f"- BASE: `{BASE}`\n- Branch: `{BRANCH}`\n- Tip before failure record: `{git('rev-parse','HEAD').strip()}`\n- Rule: no fix-forward past a red gate. Records phase not run.\n\n"+"## Failed gates — measured payload\n\n```json\n"+json.dumps(failed,indent=2,ensure_ascii=False)+"\n```\n\n## P1–P7 state at stop\n\n```json\n"+json.dumps(item_status,indent=2,ensure_ascii=False)+"\n```\n\n## Commit map\n\n```json\n"+json.dumps(commits,indent=2,ensure_ascii=False)+"\n```\n";write("_passph1/GATE_FAILURE.md",body);commit_and_push("PH-1 STOP: Phase 3 gate red; evidence committed; no fix-forward",["_passph1/GATE_FAILURE.md"])


def main() -> None:
    repo_gate();git("config","user.name","PH-1 Executor");git("config","user.email","ph1@madebymatt.invalid");census=census_data();census_md=read("_passph1/CENSUS.md");c2=section_paths(census_md,"C2","C3");c5=section_paths(census_md,"C5","C6");c6m=re.search(r"(?ms)^## C6\b.*?Findings:\s*\*\*(\d+)\*\*",census_md);c6_count=int(c6m.group(1)) if c6m else 0
    commits={};status={};touched=set()
    files,info=apply_p1(c2);touched.update(files);status["P1"]=info;commits["P1"]=info.get("commit")
    files,info=apply_p2();touched.update(files);status["P2"]=info;commits["P2"]=info.get("commit")
    files,info=apply_p3(c5);touched.update(files);status["P3"]=info;commits["P3"]=info.get("commit")
    files,info=apply_p4();touched.update(files);status["P4"]=info;commits["P4"]=info.get("commit")
    files,info=apply_p5(c6_count);status["P5"]=info;commits["P5"]=info.get("commit")
    files,info=apply_p6();touched.update(files);status["P6"]=info;commits["P6"]=info.get("commit")
    files,info=apply_p7();status["P7"]=info;commits["P7"]=info.get("commit");status["P8"]={"status":"NOT-DONE","why":"No standalone AUTHORISE P8 L2 CLAIM line supplied"}
    commits["transport_cleanup"]=retire_transport();touched_html=sorted(p for p in touched if p.lower().endswith((".html",".htm")));allowed=set(touched_html)
    results={"G1":gate_g1(touched_html),"G2":gate_g2(touched_html),"G3":gate_g3(touched_html),"G4":gate_g4(),"G5":gate_g5(),"G6":gate_g6(census),"G7":gate_g7(touched_html),"G8":gate_g8(touched_html),"G9":gate_g9(allowed),"G10":gate_g10(touched_html)}
    if not all(v.get("pass") for v in results.values()):make_gate_failure(results,status,commits);print(json.dumps({"PH1":"STOP","failed":[k for k,v in results.items() if not v.get('pass')],"tip":git('rev-parse','HEAD').strip()},indent=2));raise SystemExit(30)
    write("_passph1/GATE_RESULTS.json",json.dumps({"base":BASE,"branch":BRANCH,"touched_html":touched_html,"items":status,"commits":commits,"gates":results},indent=2,ensure_ascii=False)+"\n");summary_lines=["# PH-1 gate results","",f"- BASE: `{BASE}`",f"- Tip before gate-result commit: `{git('rev-parse','HEAD').strip()}`",""]
    for gate,result in results.items():summary_lines.append(f"- **{gate}: PASS** — `{json.dumps({k:v for k,v in result.items() if k!='failures'},ensure_ascii=False)}`")
    summary_lines+=["","P8 was not authorised and did not run.",""];write("_passph1/GATE_RESULTS.md","\n".join(summary_lines));commits["gates"]=commit_and_push("PH-1 gates G1-G10: all PASS",["_passph1/GATE_RESULTS.json","_passph1/GATE_RESULTS.md"]);commits["records"]=append_records(results,commits);print(json.dumps({"PH1":"HELD_GREEN","base":BASE,"tip":git("rev-parse","HEAD").strip(),"commits":commits,"items":status,"gates":{k:v.get("pass") for k,v in results.items()}},indent=2,ensure_ascii=False))


if __name__=="__main__":
    try:main()
    except SystemExit:raise
    except Exception as exc:
        try:write("_passph1/EXECUTOR_EXCEPTION.md","# PH-1 executor exception\n\n```text\n"+repr(exc)+"\n```\n");commit_and_push("PH-1 STOP: executor exception preserved; no fix-forward",["_passph1/EXECUTOR_EXCEPTION.md"])
        except Exception:pass
        raise
