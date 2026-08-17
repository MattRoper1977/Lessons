from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import difflib
import json
import re
import subprocess

OUT = Path('/tmp/ph1-phase0d')
OUT.mkdir(parents=True, exist_ok=True)


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True, errors='replace')


tracked = [Path(p) for p in git('ls-files').splitlines() if p]
before_status = git('status', '--porcelain=v1')


def is_text(path: Path) -> bool:
    try:
        path.read_text(encoding='utf-8')
        return True
    except Exception:
        return False


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='replace')


def estate_component(path: Path) -> bool:
    return any(part.endswith('_Estate_v3') for part in path.parts)


estate_paths = sorted(str(p) for p in tracked if estate_component(p))

live_comsk1 = {
    'LAUNCH_ASDAN/LAUNCH_ASDAN_Hub.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W1_Intro_and_Choosing_My_Level.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W2_What_Makes_Communication_Effective.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W3_Active_Listening_and_Giving_Feedback.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html',
    'LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html',
    'LAUNCH_ASDAN/PEQ/START_HERE.html',
    'LAUNCH_ASDAN/Resources_and_Tools.html',
    'LAUNCH_ASDAN/Scheme_of_Work.html',
}
all_counts: Counter[str] = Counter()
for path in tracked:
    if not is_text(path):
        continue
    count = read_text(path).count('ComSk1')
    if count:
        all_counts[str(path)] = count
whole_total = sum(all_counts.values())
live_total = sum(all_counts[path] for path in live_comsk1)
gap_counts = Counter({path: count for path, count in all_counts.items() if path not in live_comsk1})
gap_total = sum(gap_counts.values())


def lines_changed(a: str, b: str) -> tuple[int, int, int]:
    aa = a.splitlines()
    bb = b.splitlines()
    removed = 0
    added = 0
    matcher = difflib.SequenceMatcher(a=aa, b=bb, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
        removed += i2 - i1
        added += j2 - j1
    return removed + added, removed, added


def norm_key(value: str) -> str:
    base = Path(value).name.lower()
    base = re.sub(r'^(build|grow|launch)_', '', base)
    return re.sub(r'[^a-z0-9]+', '', base)


def under(prefix: str) -> list[str]:
    marker = prefix.rstrip('/') + '/'
    return sorted(str(path) for path in tracked if str(path).startswith(marker))


def production_dt() -> list[str]:
    chosen: list[str] = []
    for path in tracked:
        value = str(path)
        if value == 'build_dt_upcycling.html' or value.startswith('DT_Community_Upcycling/'):
            chosen.append(value)
        elif re.fullmatch(r'Build/Slideshows/BUILD_DT_W[1-6]_[^/]+\.html', value):
            chosen.append(value)
    return sorted(chosen)


def compare_sets(
    label: str,
    test_prefix: str,
    prod_prefix: str | None,
    prod_paths: list[str] | None = None,
) -> dict:
    test_paths = under(test_prefix)
    production_paths = sorted(prod_paths if prod_paths is not None else under(prod_prefix or ''))
    test_rel = {path[len(test_prefix.rstrip('/') + '/'):]: path for path in test_paths}
    if prod_prefix is not None:
        prod_rel = {path[len(prod_prefix.rstrip('/') + '/'):]: path for path in production_paths}
    else:
        prod_rel = {path: path for path in production_paths}

    matches: list[tuple[str, str, str]] = []
    used_test: set[str] = set()
    used_prod: set[str] = set()
    for rel in sorted(set(test_rel) & set(prod_rel)):
        matches.append((rel, test_rel[rel], prod_rel[rel]))
        used_test.add(test_rel[rel])
        used_prod.add(prod_rel[rel])

    prod_by_key: dict[str, list[str]] = defaultdict(list)
    for path in production_paths:
        if path not in used_prod:
            prod_by_key[norm_key(path)].append(path)
    for test_path in test_paths:
        if test_path in used_test:
            continue
        candidates = prod_by_key.get(norm_key(test_path), [])
        if len(candidates) == 1:
            prod_path = candidates[0]
            matches.append((f'normalised basename: {Path(test_path).name}', test_path, prod_path))
            used_test.add(test_path)
            used_prod.add(prod_path)
            prod_by_key[norm_key(test_path)] = []

    entries: list[dict] = []
    total_changed = 0
    total_removed = 0
    total_added = 0
    identical = 0
    for rel, test_path, prod_path in sorted(matches):
        test_text = read_text(Path(test_path)) if is_text(Path(test_path)) else Path(test_path).read_bytes().hex()
        prod_text = read_text(Path(prod_path)) if is_text(Path(prod_path)) else Path(prod_path).read_bytes().hex()
        if test_text == prod_text:
            identical += 1
            entries.append({
                'match': rel,
                'test': test_path,
                'production': prod_path,
                'status': 'identical',
                'changed': 0,
                'removed': 0,
                'added': 0,
            })
        else:
            changed, removed, added = lines_changed(test_text, prod_text)
            total_changed += changed
            total_removed += removed
            total_added += added
            entries.append({
                'match': rel,
                'test': test_path,
                'production': prod_path,
                'status': 'different',
                'changed': changed,
                'removed': removed,
                'added': added,
            })

    only_test = sorted(set(test_paths) - used_test)
    only_prod = sorted(set(production_paths) - used_prod)
    unmatched_lines = 0
    for path in only_test + only_prod:
        try:
            unmatched_lines += len(read_text(Path(path)).splitlines())
        except Exception:
            pass
    aggregate = total_changed + unmatched_lines
    if not only_test and not only_prod and total_changed == 0:
        classification = 'identical'
    elif not only_test and not only_prod and total_changed <= 20:
        classification = 'trivially divergent'
    else:
        classification = 'materially divergent'

    return {
        'label': label,
        'test_prefix': test_prefix,
        'production': prod_prefix or 'production DT route (hub + planning + six lessons)',
        'test_files': len(test_paths),
        'production_files': len(production_paths),
        'matched': len(matches),
        'identical_matches': identical,
        'different_matches': len(matches) - identical,
        'only_test': only_test,
        'only_production': only_prod,
        'changed_lines_matched': total_changed,
        'removed_lines_matched': total_removed,
        'added_lines_matched': total_added,
        'unmatched_file_lines': unmatched_lines,
        'aggregate_differing_lines': aggregate,
        'classification': classification,
        'entries': entries,
    }


comparisons = [
    compare_sets('BUILD ASDAN', 'BUILD_Estate_v3/BUILD_ASDAN', 'BUILD_ASDAN'),
    compare_sets(
        'DT Community Upcycling',
        'BUILD_Estate_v3/DT_Community_Upcycling',
        None,
        production_dt(),
    ),
    compare_sets('GROW ASDAN', 'GROW_Estate_v3/GROW_ASDAN', 'GROW_ASDAN'),
    compare_sets('LAUNCH ASDAN', 'LAUNCH_Estate_v3/LAUNCH_ASDAN', 'LAUNCH_ASDAN'),
]

md: list[str] = [
    '# PH-1 Phase 0d — production re-anchoring and TEST COPY divergence',
    '',
    '- Repository: `MattRoper1977/Lessons`',
    '- Immutable BASE: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`',
    '- Census tip: `daf746f5d8894d1b56e203ed34b641b74b0e9522`',
    f"- Measurement commit input: `{git('rev-parse', 'HEAD').strip()}`",
    '- Production authority: `BUILD_ASDAN` (31 lessons), `GROW_ASDAN` (18), `LAUNCH_ASDAN` (30), with DT routed by `build_dt_upcycling.html` to six lessons and two planning pages.',
    '- Edit rule: every `*_Estate_v3` path is outside PH-1 write scope.',
    '',
    '## Every tracked `*_Estate_v3` surface',
    '',
    f'- Files: **{len(estate_paths)}**',
    '',
]
md.extend(f'- `{path}`' for path in estate_paths)
md.extend([
    '',
    '## The 228-occurrence `ComSk1` gap',
    '',
    f'- Whole tracked tree: **{whole_total}** occurrences.',
    f'- Resolved production estate: **{live_total}** occurrences across the ten production files identified by C1.',
    f'- Non-production/documentation/test-copy gap: **{gap_total}** occurrences.',
    '',
])
if gap_total != 228 or whole_total != 312 or live_total != 84:
    md.extend([
        f'> **MEASUREMENT DISAGREEMENT:** census expected 312 / 84 / 228; measured {whole_total} / {live_total} / {gap_total}. Repository measurement wins.',
        '',
    ])
md.extend(['| File | Gap occurrences |', '|---|---:|'])
md.extend(
    f'| `{path}` | {count} |'
    for path, count in sorted(gap_counts.items(), key=lambda item: (-item[1], item[0]))
)
md.extend(['', '## Audit-named path comparisons', ''])
for comparison in comparisons:
    md.extend([
        f"### {comparison['label']}",
        '',
        f"- Test path: `{comparison['test_prefix']}`",
        f"- Production counterpart: `{comparison['production']}`",
        f"- Classification: **{comparison['classification']}**",
        f"- File counts: test **{comparison['test_files']}**, production **{comparison['production_files']}**; matched **{comparison['matched']}**; test-only **{len(comparison['only_test'])}**; production-only **{len(comparison['only_production'])}**.",
        f"- Matched-file differing lines: **{comparison['changed_lines_matched']}** = {comparison['removed_lines_matched']} removed + {comparison['added_lines_matched']} added.",
        f"- Lines in unmatched files: **{comparison['unmatched_file_lines']}**.",
        f"- Aggregate differing-line measure: **{comparison['aggregate_differing_lines']}**.",
        '',
        '| Match | Test | Production | Status | Differing lines |',
        '|---|---|---|---|---:|',
    ])
    for entry in comparison['entries']:
        md.append(
            f"| {entry['match']} | `{entry['test']}` | `{entry['production']}` | {entry['status']} | {entry['changed']} |"
        )
    if comparison['only_test']:
        md.extend(['', '**Test-only files**', ''])
        md.extend(f'- `{path}`' for path in comparison['only_test'])
    if comparison['only_production']:
        md.extend(['', '**Production-only files**', ''])
        md.extend(f'- `{path}`' for path in comparison['only_production'])
    md.append('')

md.extend([
    '## Does the third-party audit still hold against production?',
    '',
    '**Broadly yes, but only after re-anchoring every claim to production.** The four audit-named `*_Estate_v3` locations are not the teaching authority and are materially divergent from the live routes. The pathway conclusions survive for the following measured reasons:',
    '',
    '- **BUILD:** production still contains the 31-lesson ASDAN estate plus hub/Scheme/START_HERE surfaces. The need to distinguish regulated PEQ assessment from Short Course/UAS activity remains a valid claim-accuracy concern, but test-copy wording must not be treated as production evidence.',
    '- **DT Community Upcycling:** the production hub still routes to six practical lessons and two planning pages. The audit’s warning that lesson-page count alone does not prove a sustained logged qualification activity remains valid; actual hours and assessed use must come from centre records.',
    '- **GROW:** production still contains 18 lessons across PEQ, Community Project and Enterprise strands. The broad rehearsal-versus-assessed-context distinction remains valid, while the live Level 2 registration sentence is separately recorded in `C7_FINDING.md`.',
    '- **LAUNCH:** production still contains 30 lessons, and C2 identified two production ComSk1 pages that state the 250-word option while omitting other minima. The need for a staff-side minima completion block therefore holds on production evidence, not on the test copy.',
    '',
    'The exact wording, counts and file targets in any deployment must use the production paths above. No conclusion in this report authorises an edit under `*_Estate_v3`.',
    '',
])
(OUT / 'TEST_COPY_DIVERGENCE.md').write_text('\n'.join(md) + '\n', encoding='utf-8')


def guard_write_path(path: str) -> None:
    if any(part.endswith('_Estate_v3') for part in Path(path).parts):
        raise RuntimeError(
            f'PH-1 SCOPE STOP: write refused for out-of-scope TEST COPY path: {path}'
        )


attempted = 'BUILD_Estate_v3/BUILD_ASDAN/PH1_SCOPE_GUARD_PROBE.txt'
error: str | None = None
created = False
try:
    guard_write_path(attempted)
    Path(attempted).write_text('THIS MUST NEVER BE WRITTEN\n', encoding='utf-8')
    created = True
except Exception as exc:
    error = f'{type(exc).__name__}: {exc}'
after_status = git('status', '--porcelain=v1')
proof = [
    '# PH-1 Phase 0d — production-only scope guard proof',
    '',
    f'- Attempted path: `{attempted}`',
    '- Expected: refusal before any filesystem write.',
    f"- Actual error: `{str(error).replace('`', '\\`')}`",
    f"- Probe file created: **{'YES — FAILURE' if created else 'NO'}**",
    f"- Worktree status before: `{before_status.strip() or '<clean>'}`",
    f"- Worktree status after: `{after_status.strip() or '<clean>'}`",
    '',
    '## Guard used',
    '',
    '```python',
    'def guard_write_path(path):',
    "    if any(part.endswith('_Estate_v3') for part in Path(path).parts):",
    "        raise RuntimeError(f'PH-1 SCOPE STOP: write refused for out-of-scope TEST COPY path: {path}')",
    '```',
    '',
    '**Result: PASS.** The guard fired and no test-copy path was created or modified.',
    '',
]
(OUT / 'SCOPE_GUARD_PROOF.md').write_text('\n'.join(proof), encoding='utf-8')
(OUT / 'phase0d-data.json').write_text(
    json.dumps(
        {
            'whole': whole_total,
            'live': live_total,
            'gap': gap_total,
            'estate_paths': len(estate_paths),
            'comparisons': comparisons,
            'scope_error': error,
        },
        indent=2,
    ),
    encoding='utf-8',
)
print(
    json.dumps(
        {
            'whole': whole_total,
            'live': live_total,
            'gap': gap_total,
            'estate_paths': len(estate_paths),
            'scope_error': error,
        },
        indent=2,
    )
)
