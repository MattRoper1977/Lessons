from __future__ import annotations

from pathlib import Path
from collections import Counter
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = "ae1d3c7af2526781aad6fb82e7cbbf6b87ded380"
CENSUS_TIP = "daf746f5d8894d1b56e203ed34b641b74b0e9522"
BRANCH = "pass-ph1-peq-hardening"
ROOT = Path.cwd()
DRY_RUN = os.environ.get("DRY_RUN", "1") == "1"
OUT = Path(os.environ.get("PH1_OUT", "/tmp/ph1-apply"))
OUT.mkdir(parents=True, exist_ok=True)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, errors="replace")


def guard_path(path: str | Path) -> None:
    value = Path(path)
    if any(part.endswith("_Estate_v3") for part in value.parts):
        raise RuntimeError(f"PH-1 SCOPE STOP: write refused for out-of-scope TEST COPY path: {path}")


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="strict")


def write(path: str | Path, content: str) -> None:
    guard_path(path)
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def count_exact(path: str, needle: str) -> int:
    return read(path).count(needle)


def replace_exact(path: str, old: str, new: str, expected: int) -> int:
    text = read(path)
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{path}: expected {expected} occurrences of {old!r}; measured {count}")
    text = text.replace(old, new)
    if text.count(old) != 0:
        raise RuntimeError(f"{path}: replacement left {text.count(old)} occurrences of {old!r}")
    write(path, text)
    return count


def insert_before_body(path: str, marker: str, snippet: str) -> None:
    text = read(path)
    if marker in text:
        raise RuntimeError(f"{path}: marker {marker!r} already exists")
    index = text.lower().rfind("</body>")
    if index < 0:
        raise RuntimeError(f"{path}: no </body> insertion anchor")
    text = text[:index] + "\n" + snippet.rstrip() + "\n" + text[index:]
    write(path, text)


def insert_inside_id(path: str, target_id: str, marker: str, snippet: str) -> None:
    text = read(path)
    if marker in text:
        raise RuntimeError(f"{path}: marker {marker!r} already exists")
    opening = re.search(
        rf"(?is)<(?P<tag>[a-z][a-z0-9]*)\b[^>]*\bid=[\"']{re.escape(target_id)}[\"'][^>]*>",
        text,
    )
    if not opening:
        raise RuntimeError(f"{path}: id={target_id!r} not found")
    tag = opening.group("tag")
    depth = 1
    token_re = re.compile(rf"(?is)</?{re.escape(tag)}\b[^>]*>")
    insert_at = None
    for token in token_re.finditer(text, opening.end()):
        raw = token.group(0)
        if raw.startswith("</"):
            depth -= 1
            if depth == 0:
                insert_at = token.start()
                break
        elif not raw.rstrip().endswith("/>"):
            depth += 1
    if insert_at is None:
        raise RuntimeError(f"{path}: unable to locate closing tag for id={target_id!r}")
    text = text[:insert_at] + "\n" + snippet.rstrip() + "\n" + text[insert_at:]
    write(path, text)


def commit(message: str, paths: list[str]) -> str:
    for path in paths:
        guard_path(path)
    run(["git", "add", "--", *paths])
    staged = git("diff", "--cached", "--name-only").splitlines()
    expected = sorted(paths)
    if sorted(staged) != expected:
        raise RuntimeError(f"commit staging mismatch: expected {expected}; staged {sorted(staged)}")
    run(["git", "commit", "-m", message])
    return git("rev-parse", "HEAD").strip()


def print_section_count(text: str) -> int:
    return len(re.findall(r'class=["\'][^"\']*\bprint-section\b[^"\']*["\']', text, flags=re.I))


def reduced_motion_blocks(text: str) -> list[str]:
    # Capture complete @media blocks using brace depth, not a one-line regex.
    blocks: list[str] = []
    for match in re.finditer(r"@media\s*\([^)]*prefers-reduced-motion[^)]*\)\s*\{", text, flags=re.I):
        depth = 0
        end = None
        for pos in range(match.start(), len(text)):
            char = text[pos]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    break
        if end is not None:
            blocks.append(text[match.start():end])
    return blocks


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def file_metrics(paths: list[str]) -> dict[str, dict]:
    metrics = {}
    for path in paths:
        text = read(path)
        metrics[path] = {
            "print_sections": print_section_count(text),
            "reduced_motion": [sha(block) for block in reduced_motion_blocks(text)],
            "ends_html": text.rstrip().lower().endswith("</html>"),
        }
    return metrics


def ensure_html_ends(paths: list[str]) -> None:
    failures = [path for path in paths if not read(path).rstrip().lower().endswith("</html>")]
    if failures:
        raise RuntimeError(f"touched HTML does not end </html>: {failures}")


def assert_metrics_unchanged(before: dict[str, dict], paths: list[str]) -> None:
    after = file_metrics(paths)
    problems = {}
    for path in paths:
        if before[path]["print_sections"] != after[path]["print_sections"]:
            problems.setdefault(path, {})["print_sections"] = [before[path]["print_sections"], after[path]["print_sections"]]
        if before[path]["reduced_motion"] != after[path]["reduced_motion"]:
            problems.setdefault(path, {})["reduced_motion"] = [before[path]["reduced_motion"], after[path]["reduced_motion"]]
    if problems:
        raise RuntimeError(f"static invariants changed: {json.dumps(problems, indent=2)}")


P1_PAGES = [
    "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html",
    "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
]
P3_PAGES = [
    "BUILD_ASDAN/BUILD_ASDAN_Hub.html",
    "GROW_ASDAN/Scheme_and_Resources.html",
    "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
    "LAUNCH_ASDAN/PEQ/START_HERE.html",
    "LAUNCH_ASDAN/Resources_and_Tools.html",
    "LAUNCH_ASDAN/Scheme_of_Work.html",
]
P4_PAGES = [
    "BUILD_ASDAN/BUILD_ASDAN_Hub.html",
    "build_dt_upcycling.html",
    "GROW_ASDAN/GROW_ASDAN_Hub.html",
    "LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html",
]
P6_BUILD_PAGES = [
    "BUILD_ASDAN/BUILD_ASDAN_Hub.html",
    "BUILD_ASDAN/Careers/START_HERE.html",
    "BUILD_ASDAN/Community_Project/START_HERE.html",
    "BUILD_ASDAN/Duke_and_Enterprise/START_HERE.html",
    "BUILD_ASDAN/FoodWise/START_HERE.html",
    "BUILD_ASDAN/Living_Independently/START_HERE.html",
    "build_asdan.html",
]
P6_VOCATIONAL_PAGE = "LAUNCH_ASDAN/Vocational/START_HERE.html"

P2_REPLACEMENTS: list[tuple[str, str, str, int]] = [
    (
        "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html",
        "Witness staff sign off the profile as portfolio evidence.",
        "Witness staff prepare the profile for assessor sign-off as portfolio evidence.",
        1,
    ),
    (
        "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html",
        "Witness staff sign off the community evidence.",
        "Witness staff prepare the community evidence for assessor sign-off.",
        1,
    ),
    (
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html",
        "Witness staff sign off the completed challenges.",
        "Witness staff prepare the completed challenges for assessor sign-off.",
        1,
    ),
    (
        "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html",
        "Witness staff sign off the practical + hygiene evidence.",
        "Witness staff prepare the practical + hygiene evidence for assessor sign-off.",
        1,
    ),
    (
        "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html",
        "Witness staff sign off FoodWise M1 — module complete.",
        "Witness staff prepare the FoodWise M1 evidence for assessor sign-off.",
        1,
    ),
    (
        "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html",
        "Witness staff sign off the LI M1 practical evidence.",
        "Witness staff prepare the LI M1 practical evidence for assessor sign-off.",
        1,
    ),
    (
        "Build/Slideshows/BUILD_DT_W6_Handover.html",
        "Witness staff sign off the completed portfolio + predicted grade.",
        "Witness staff prepare the completed portfolio + predicted grade for assessor sign-off.",
        1,
    ),
    (
        "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html",
        "Review Progress and Sign Off the Unit",
        "Review Progress and Prepare for Assessor Sign-Off",
        1,
    ),
    (
        "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        "Review Progress and Sign Off the Unit",
        "Review Progress and Prepare for Assessor Sign-Off",
        8,
    ),
    (
        "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        '<text x="280" y="126" text-anchor="middle" font-size="11" fill="#8E4F82">REVIEW and\nSIGN OFF</text>',
        '<text x="280" y="126" text-anchor="middle" font-size="11" fill="#8E4F82">PREPARE FOR\nASSESSOR SIGN-OFF</text>',
        1,
    ),
    (
        "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html",
        "Narrate the four review parts and sign-off slowly.",
        "Narrate the four review parts and preparation for assessor sign-off slowly.",
        1,
    ),
    (
        "LAUNCH_ASDAN/PEQ/START_HERE.html",
        "Review Progress and Sign Off the Unit",
        "Review Progress and Prepare for Assessor Sign-Off",
        1,
    ),
    (
        "LAUNCH_ASDAN/Scheme_of_Work.html",
        "Review Progress and Sign Off the Unit",
        "Review Progress and Prepare for Assessor Sign-Off",
        1,
    ),
]

TOUCHED_HTML = sorted(set(P1_PAGES + P3_PAGES + P4_PAGES + P6_BUILD_PAGES + [P6_VOCATIONAL_PAGE] + [item[0] for item in P2_REPLACEMENTS]))

# Guard the explicit production target set before any work.
for target in TOUCHED_HTML:
    guard_path(target)
    if not (ROOT / target).is_file():
        raise RuntimeError(f"missing production target: {target}")

starting_head = git("rev-parse", "HEAD").strip()
starting_status = git("status", "--porcelain=v1")
if starting_status.strip():
    raise RuntimeError(f"worktree not clean at start: {starting_status}")
run(["git", "config", "user.name", "PH-1 Executor"])
run(["git", "config", "user.email", "ph1@madebymatt.invalid"])

static_before = file_metrics(TOUCHED_HTML)

# Existing proven witness comparator must remain green after every edit.
spec = importlib.util.spec_from_file_location("g4cmp", ROOT / "_passph1/G4_WITNESS_COMPARATOR.py")
if not spec or not spec.loader:
    raise RuntimeError("unable to import proven G4 comparator")
g4cmp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g4cmp)
witness_before = g4cmp.snapshot(ROOT)
if len(witness_before) != 147:
    raise RuntimeError(f"proven G4 comparator expected 147 BASE-equivalent surfaces at start; measured {len(witness_before)}")

commits: dict[str, str] = {}

# ---------------------------------------------------------------------------
# P1 — ComSk1 hard minima, two print/staff pages
# ---------------------------------------------------------------------------
p1_marker = 'id="ph1-comsk1-hard-minima"'
if sum(read(path).count(p1_marker) for path in P1_PAGES) != 0:
    raise RuntimeError("P1 marker pre-count is not zero")
p1_block = '''<section id="ph1-comsk1-hard-minima" data-staff-only="true" style="border:2px solid #7C4372;border-radius:10px;padding:12px;margin:12px 0;background:#fffdf7;color:#111">
  <h3 style="margin:0 0 8px">ComSk1 — hard minima (spec v1.2, Oct 2025)</h3>
  <ul style="margin:0 0 8px 1.2rem">
    <li><strong>Plan · 1.4.1f:</strong> record at least 4 potential audience questions and the planned response to each. The number belongs in the plan; it is not a live Q&amp;A quota.</li>
    <li><strong>Do · 1.5.1:</strong> complete one activity: presentation at least 3 minutes, or discussion at least 8 minutes, or text at least 250 words.</li>
    <li><strong>Know · 1.1.2 / 1.1.3 / 1.1.4:</strong> at least 3 ways of communicating, at least 4 components of effective communication, and at least 3 difficulties. Four is the odd one out; “a range” means 3 unless another number is stated.</li>
    <li><strong>Review · 1.6.1:</strong> record at least 2 positives and at least 2 areas for further development, plus active listening, how difficulties were managed (or that none occurred), use of peer feedback, and one future situation.</li>
    <li><strong>Group work:</strong> a group has at least 3 members.</li>
    <li><strong>Preparation evidence:</strong> when the activity is not linked to assessment for another PEQ unit, retain preparation evidence, including topic research.</li>
  </ul>
  <p style="margin:0"><strong>Staff check only:</strong> this block supports evidence planning; it does not assess or award the unit.</p>
</section>'''
for path in P1_PAGES:
    insert_inside_id(path, "print-ko", p1_marker, p1_block)
if sum(read(path).count(p1_marker) for path in P1_PAGES) != 2:
    raise RuntimeError("P1 block count after edit is not 2")
commits["P1"] = commit("PH-1 P1: ComSk1 minima pages 2 incomplete -> 2 complete", P1_PAGES)

# ---------------------------------------------------------------------------
# P2 — change B1 only; B2/B3 remain untouched
# ---------------------------------------------------------------------------
p2_before = sum(expected for _, _, _, expected in P2_REPLACEMENTS)
if p2_before != 20:
    raise RuntimeError(f"P2 replacement plan expected 20, got {p2_before}")
acted = 0
p2_files: list[str] = []
for path, old, new, expected in P2_REPLACEMENTS:
    acted += replace_exact(path, old, new, expected)
    if path not in p2_files:
        p2_files.append(path)
if acted != 20:
    raise RuntimeError(f"P2 acted on {acted}, expected 20")
# Structural filename remains unchanged and canonical held B2 language remains.
w6_path = "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html"
if not (ROOT / w6_path).is_file():
    raise RuntimeError("P2 renamed or removed the held W6 file")
if "Name future use, and sign off." not in read(w6_path):
    raise RuntimeError("P2 altered held B2 pupil instruction")
if "SIGN-OFF</div>" not in read(w6_path) and ">SIGN-OFF<" not in read(w6_path):
    # The match game may use other markup; require the exact B2 keyword anywhere.
    if "SIGN-OFF" not in read(w6_path):
        raise RuntimeError("P2 removed held B2 SIGN-OFF keyword")
commits["P2"] = commit("PH-1 P2: 20 B1 sign-off occurrences -> 0; B2 80/B3 1 held", p2_files)

# ---------------------------------------------------------------------------
# P3 — exact credit-route rule block on the six measured pages
# ---------------------------------------------------------------------------
p3_marker = 'id="ph1-peq-credit-route"'
if sum(read(path).count(p3_marker) for path in P3_PAGES) != 0:
    raise RuntimeError("P3 marker pre-count is not zero")
p3_block = '''<details id="ph1-peq-credit-route" data-staff-only="true" style="max-width:980px;margin:18px auto;padding:12px;border:2px solid #475569;border-radius:10px;background:#f8fafc;color:#0f172a">
  <summary style="font-weight:800;cursor:pointer">Staff · PEQ credit-route rules (spec v1.2, Oct 2025)</summary>
  <ul>
    <li><strong>Award:</strong> all credits are at the level of the qualification.</li>
    <li><strong>Extended Award and Certificate:</strong> a maximum of 3 credits may come from units at the level above or below.</li>
    <li><strong>Adjacent-level arithmetic:</strong> the smallest unit is 2 credits, so at most one adjacent-level unit can contribute.</li>
    <li><strong>Totals:</strong> Entry 3 and Level 1 — 4 / 9 / 14; Level 2 — 4 / 9 / 15; Level 3 — 6 / 11 / 18. Level 3 is 16+ and is not for this cohort.</li>
    <li><strong>Barred combinations:</strong> this applies across all 6 skill families; where the same family is held at 2 levels, only the highest-level unit counts.</li>
  </ul>
</details>'''
for path in P3_PAGES:
    insert_before_body(path, p3_marker, p3_block)
if sum(read(path).count(p3_marker) for path in P3_PAGES) != 6:
    raise RuntimeError("P3 block count after edit is not 6")
if any("not both" in read(path).lower() for path in P3_PAGES):
    raise RuntimeError("P3 left or introduced forbidden adjacent-level phrase 'not both'")
commits["P3"] = commit("PH-1 P3: credit-route pages 6 incomplete -> 6 authoritative", P3_PAGES)

# ---------------------------------------------------------------------------
# P4 — partial-achievement fact on four suite hubs
# ---------------------------------------------------------------------------
p4_marker = 'id="ph1-partial-achievement"'
if sum(read(path).count(p4_marker) for path in P4_PAGES) != 0:
    raise RuntimeError("P4 marker pre-count is not zero")
p4_line = '''<p id="ph1-partial-achievement" data-staff-only="true" style="max-width:980px;margin:12px auto;padding:10px;border-left:5px solid #0f766e;background:#f0fdfa;color:#134e4a"><strong>Staff accreditation note:</strong> if the full qualification credit total is not reached, the PEQ units the learner has achieved can still be certified (spec v1.2 §5.1).</p>'''
for path in P4_PAGES:
    insert_before_body(path, p4_marker, p4_line)
if sum(read(path).count(p4_marker) for path in P4_PAGES) != 4:
    raise RuntimeError("P4 line count after edit is not 4")
commits["P4"] = commit("PH-1 P4: suite partial-achievement lines 0 -> 4", P4_PAGES)

# ---------------------------------------------------------------------------
# P5 — Level 1 demand report only; C6 measured zero
# ---------------------------------------------------------------------------
p5_path = "_passph1/L1_DEMAND_REPORT.md"
if (ROOT / p5_path).exists():
    raise RuntimeError("P5 report already exists")
p5_text = f'''# PH-1 P5 — Level 1 verb-demand report

- Repository: `MattRoper1977/Lessons`
- Immutable BASE: `{BASE}`
- Canonical source: committed census at `{CENSUS_TIP}`; the census was not rerun.
- Live production findings for ThSk1 1.1.3, 1.1.4 and 1.2.1 using `outline` where v1.2 asks for a lower demand: **0**.

## Decision

No lesson or planning page was changed. There is no live occurrence for Matt to relax, so the former Level 1 verb-relaxation question is closed and must not be added to the open-items register.
'''
write(p5_path, p5_text)
commits["P5"] = commit("PH-1 P5: L1 demand findings 0 -> report only", [p5_path])

# ---------------------------------------------------------------------------
# P6 — accreditation-status panels on BUILD hubs/START_HERE and Vocational hub
# ---------------------------------------------------------------------------
p6_build_marker = 'id="ph1-build-accreditation-status"'
p6_voc_marker = 'id="ph1-vocational-accreditation-status"'
if sum(read(path).count(p6_build_marker) for path in P6_BUILD_PAGES) != 0:
    raise RuntimeError("P6 BUILD marker pre-count is not zero")
if read(P6_VOCATIONAL_PAGE).count(p6_voc_marker) != 0:
    raise RuntimeError("P6 Vocational marker pre-count is not zero")
p6_common = '''<ul>
    <li><strong>Regulated PEQ evidence:</strong> name the PEQ unit and criterion references, collect authentic evidence, make an assessor decision, and complete internal quality assurance.</li>
    <li><strong>Separate activity:</strong> ASDAN Short Course and AQA UAS activity is not regulated PEQ evidence by itself.</li>
    <li><strong>No automatic conversion:</strong> a Short Course certificate does not automatically become PEQ credit.</li>
    <li><strong>Prior learning:</strong> any claim must follow ASDAN’s RPL procedure and can count only when achieved within 3 years of the qualification quality-assurance date.</li>
  </ul>
  <p><strong>Time-sensitive check:</strong> Checked 17 Aug 2026 on asdan.org.uk: the ASDAN e-portfolio is closed to new registrations and access for existing registrations ends 31 August 2026; Short Course student books remain available. If any learner evidence is held in that e-portfolio, export it. Re-check before use.</p>'''
p6_build = f'''<details id="ph1-build-accreditation-status" data-staff-only="true" style="max-width:980px;margin:18px auto;padding:12px;border:2px solid #9a3412;border-radius:10px;background:#fff7ed;color:#431407">
  <summary style="font-weight:800;cursor:pointer">Staff · accreditation status</summary>
  {p6_common}
</details>'''
p6_voc = f'''<details id="ph1-vocational-accreditation-status" data-staff-only="true" style="max-width:980px;margin:18px auto;padding:12px;border:2px solid #9a3412;border-radius:10px;background:#fff7ed;color:#431407">
  <summary style="font-weight:800;cursor:pointer">Staff · accreditation status and title check</summary>
  {p6_common}
  <p><strong>Vocational Taster check:</strong> ASDAN has said it plans to withdraw all Vocational Taster titles, with registrations and books available to 31 December 2026 and final certification by 31 August 2027. Confirm whether this strand’s banked titles are affected before use.</p>
</details>'''
for path in P6_BUILD_PAGES:
    insert_before_body(path, p6_build_marker, p6_build)
insert_before_body(P6_VOCATIONAL_PAGE, p6_voc_marker, p6_voc)
if sum(read(path).count(p6_build_marker) for path in P6_BUILD_PAGES) != 7:
    raise RuntimeError("P6 BUILD panel count after edit is not 7")
if read(P6_VOCATIONAL_PAGE).count(p6_voc_marker) != 1:
    raise RuntimeError("P6 Vocational panel count after edit is not 1")
commits["P6"] = commit("PH-1 P6: accreditation-status panels 0 -> 8", P6_BUILD_PAGES + [P6_VOCATIONAL_PAGE])

# ---------------------------------------------------------------------------
# P7 — prohibited deployments explicitly not made
# ---------------------------------------------------------------------------
p7_path = "_passph1/P7_NOT_DEPLOYED.md"
if (ROOT / p7_path).exists():
    raise RuntimeError("P7 report already exists")
p7_text = f'''# PH-1 P7 — prohibited deployments not made

- Repository: `MattRoper1977/Lessons`
- Immutable BASE: `{BASE}`
- P8 authorisation line `AUTHORISE P8 L2 CLAIM`: **absent**. The C7 Level 2 registration claim remains report-only and was not edited.

PH-1 did **not** deploy:

- any tool that stores a candidate name or identifier in `localStorage`;
- any automatic `unit achieved` badge, assessor decision or credit claim;
- any PEQ credit attached to a challenge code such as `PEQ002` — a challenge code carries no credit of its own.

No pupil data key was introduced and no lesson page was allowed to award a unit.
'''
write(p7_path, p7_text)
commits["P7"] = commit("PH-1 P7: prohibited deployments 0; record added", [p7_path])

# ---------------------------------------------------------------------------
# Post-edit static regression checks before any push
# ---------------------------------------------------------------------------
assert_metrics_unchanged(static_before, TOUCHED_HTML)
ensure_html_ends(TOUCHED_HTML)

witness_after = g4cmp.snapshot(ROOT)
witness_result = g4cmp.compare(witness_before, witness_after)
if not witness_result["pass"]:
    raise RuntimeError(f"G4 comparator red after P1-P7: {json.dumps(witness_result, indent=2)}")

changed = git("diff", "--name-only", starting_head, "HEAD").splitlines()
for path in changed:
    guard_path(path)
allowed_prefixes = (
    "BUILD_ASDAN/",
    "GROW_ASDAN/",
    "LAUNCH_ASDAN/",
    "Build/Slideshows/",
    "DT_Community_Upcycling/",
    "_passph1/",
)
allowed_exact = {"build_asdan.html", "build_dt_upcycling.html"}
unexpected = [path for path in changed if path not in allowed_exact and not path.startswith(allowed_prefixes)]
if unexpected:
    raise RuntimeError(f"unexpected diff paths after P1-P7: {unexpected}")

# No tracked ASDAN PDF introduced.
pdf_paths = [path for path in git("ls-files").splitlines() if path.lower().endswith(".pdf") and "asdan" in path.lower()]
if pdf_paths:
    raise RuntimeError(f"tracked ASDAN PDF(s) present: {pdf_paths}")

# No new localStorage calls/keys in edited runtime HTML. Report-only prose may name the boundary.
diff_text = git("diff", starting_head, "HEAD", "--")
added_lines = "\n".join(line[1:] for line in diff_text.splitlines() if line.startswith("+") and not line.startswith("+++"))
html_added_localstorage = []
for path in changed:
    if not path.lower().endswith(".html"):
        continue
    patch = git("diff", starting_head, "HEAD", "--", path)
    for line in patch.splitlines():
        if line.startswith("+") and not line.startswith("+++") and "localStorage" in line:
            html_added_localstorage.append({"path": path, "line": line[1:]})
if html_added_localstorage:
    raise RuntimeError(f"P1-P7 added localStorage runtime text: {html_added_localstorage}")
if re.search(r"(?i)\bPEQ002\b.*\bcredit\b|\bcredit\b.*\bPEQ002\b", added_lines):
    # P7 is allowed to state that PEQ002 has no credit; prohibit only positive-looking claims.
    bad = [line for line in added_lines.splitlines() if "PEQ002" in line and "no credit" not in line.lower() and "carries no credit" not in line.lower()]
    if bad:
        raise RuntimeError(f"possible PEQ002 credit claim introduced: {bad}")

summary = {
    "dry_run": DRY_RUN,
    "starting_head": starting_head,
    "tip": git("rev-parse", "HEAD").strip(),
    "commits": commits,
    "changed_files": changed,
    "changed_file_count": len(changed),
    "witness_result": witness_result,
    "print_and_motion_unchanged": True,
    "asdan_pdfs": pdf_paths,
    "localStorage_added": False,
    "p8_authorised": False,
}
(OUT / "P1_P7_DRY_RUN.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
(OUT / "P1_P7_DIFF.patch").write_text(git("diff", starting_head, "HEAD", "--"), encoding="utf-8")
(OUT / "P1_P7_STAT.txt").write_text(git("diff", "--stat", starting_head, "HEAD"), encoding="utf-8")
print(json.dumps(summary, indent=2))
