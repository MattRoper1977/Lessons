#!/usr/bin/env python3
"""PIN1: materialize Gate A's exact registry dependencies; CI checks, never repairs.

Run --write in a reviewed change whenever the pin registry changes. A registry
edit already triggers Gate A, whose --check refuses stale generated paths before
its existing assertions run. No payload directory glob is introduced.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import sys

GATE = 'tools/verify_cross_estate_unification.py'
WORKFLOW = '.github/workflows/mbm-cross-estate-unification.yml'
# Existing non-digest dependencies remain watched, plus this checker and controls.
CHECKER_PATHS = {
    GATE, WORKFLOW, 'tools/verify_cross_estate_browser.mjs',
    'docs/MBM_CROSS_ESTATE_UNIFICATION.md',
    'tools/pin1/derive_triggers.py', 'tools/pin1/test_derive_triggers.py',
}
EVENTS = ('pull_request', 'push')
BEGIN = '      # BEGIN PIN1 DERIVED PATHS'
END = '      # END PIN1 DERIVED PATHS'


def load_gate(root: Path):
    spec = importlib.util.spec_from_file_location('pin1_existing_gate', root / GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact_path(value: str) -> str:
    # Refuse patterns rather than silently widening coverage. Current pins need
    # no escapes. A future glob-significant filename needs a reviewed encoding.
    if (not isinstance(value, str) or not value or value.startswith('/')
            or any(c in value for c in '*?[]!+\\\r\n')
            or any(p in ('', '.', '..') for p in value.split('/'))
            or str(PurePosixPath(value)) != value):
        raise ValueError(f'not an exact safe registry path: {value!r}')
    return value


def inventory(root: Path, gate=None) -> dict:
    gate = gate or load_gate(root)
    kind = gate.detect_kind(root)
    registries = {
        'CANONICAL_HASHES': set(gate.CANONICAL_HASHES),
        'MANIFEST_PINS': set(gate.MANIFEST_PINS),
        'CATALOGUE_PINS.files': set(gate.CATALOGUE_PINS['files']),
        'LUNDYLOOP_CI_PINS': set(gate.LUNDYLOOP_CI_PINS),
        'PUBLICATION_CALLER': {gate.PUBLICATION_CALLER_PATH},
    }
    if not registries['CANONICAL_HASHES'] or not registries['CATALOGUE_PINS.files']:
        raise ValueError('empty pin registry is unmeasured, not valid coverage')
    declared = set().union(*registries.values())
    for path in declared | CHECKER_PATHS:
        exact_path(path)
    # Match the existing gate's kind-specific assertions. MANIFEST_PINS explicitly
    # skips the other estate's absent manifest. Required catalogue/canonical paths
    # remain watched even when absent, so deleting one cannot remove its trigger.
    asserted = set(gate.CANONICAL_HASHES) | {gate.PUBLICATION_CALLER_PATH}
    asserted |= {p for p in gate.MANIFEST_PINS if (root / p).is_file()}
    asserted |= (set(gate.CATALOGUE_PINS['files']) if kind == 'lessons'
                 else set(gate.LUNDYLOOP_CI_PINS))
    expected = asserted | CHECKER_PATHS
    return {
        'kind': kind,
        'registry_counts': {k: len(v) for k, v in registries.items()},
        'declared_distinct': len(declared),
        'asserted_count': len(asserted),
        'trigger_count': len(expected),
        'asserted': sorted(asserted),
        'expected_triggers': sorted(expected),
        'triggered_not_digest_asserted': sorted(expected - asserted),
        'declared_not_asserted_here': sorted(declared - asserted),
        'missing_asserted_files': sorted(p for p in asserted if not (root / p).is_file()),
        'rows': [dict(path=p, registries=sorted(k for k, v in registries.items() if p in v),
                      asserted=p in asserted, triggered=p in expected)
                 for p in sorted(declared | expected)],
    }


def event_paths_span(text: str, event: str) -> tuple[int, int]:
    # Restrict the edit to a single paths block under one top-level event. Refuse
    # ambiguous/alternate YAML forms instead of rewriting unrelated settings.
    on = re.search(r'^on:\n(?P<body>(?:[ \t].*\n|\n|#.*\n)*)', text, re.M)
    if not on:
        raise ValueError('one explicit top-level on block required')
    if len(re.findall(r'^on:', text, re.M)) != 1:
        raise ValueError('duplicate on block')
    body = on.group('body')
    matches = list(re.finditer(r'^  ' + re.escape(event) + r':\n', body, re.M))
    if len(matches) != 1:
        raise ValueError(f'one explicit {event} event required')
    start = matches[0].end()
    tail = body[start:]
    next_event = re.search(r'^  [^ #\s][^\n]*:', tail, re.M)
    stop = start + (next_event.start() if next_event else len(tail))
    block = body[start:stop]
    if 'paths-ignore:' in block:
        raise ValueError(f'{event}: paths-ignore not supported')
    paths = list(re.finditer(r'^    paths:\n', block, re.M))
    if len(paths) != 1:
        raise ValueError(f'one explicit {event} paths block required')
    content_start = paths[0].end()
    cursor = content_start
    for line in block[content_start:].splitlines(keepends=True):
        if not line.startswith('      '):
            break
        if not (line.startswith('      - ') or line.lstrip().startswith('#')):
            raise ValueError(f'{event}: unexpected paths syntax {line!r}')
        cursor += len(line)
    if cursor == content_start:
        raise ValueError(f'{event}: empty paths block')
    offset = on.start('body') + start
    return offset + content_start, offset + cursor


def rendered_paths(paths: list[str]) -> str:
    # YAML single quotes preserve exact punctuation and spaces.
    return BEGIN + '\n' + ''.join(
        "      - '" + exact_path(p).replace("'", "''") + "'\n" for p in paths
    ) + END + '\n'


def render(text: str, paths: list[str]) -> str:
    generated = rendered_paths(paths)
    for event in EVENTS:
        begin, end = event_paths_span(text, event)
        text = text[:begin] + generated + text[end:]
    return text


def read_paths(text: str, event: str) -> list[str]:
    begin, end = event_paths_span(text, event)
    values = []
    for line in text[begin:end].splitlines():
        if line.startswith('      - '):
            value = line[len('      - '):]
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1].replace("''", "'")
            elif value.startswith('"'):
                value = json.loads(value)
            values.append(value)
    return values


def check(root: Path, text: str, report: dict) -> list[str]:
    errors = []
    expected = set(report['expected_triggers'])
    report['events'] = {}
    for event in EVENTS:
        actual_list = read_paths(text, event)
        actual = set(actual_list)
        missing = sorted(set(report['asserted']) - actual)
        unexpected = sorted(actual - expected)
        report['events'][event] = {
            'actual_triggers': actual_list,
            'asserted_not_triggered': missing,
            'triggered_not_digest_asserted': sorted(actual - set(report['asserted'])),
            'unexpected': unexpected,
        }
        if actual != expected or len(actual_list) != len(actual):
            errors.append(f'{event}: trigger set differs from registry/checker dependencies; '
                          f'missing={sorted(expected - actual)!r}; unexpected={unexpected!r}')
    if text != render(text, report['expected_triggers']):
        errors.append('generated paths are stale; run python3 tools/pin1/derive_triggers.py --write')
    if report['missing_asserted_files']:
        errors.append('asserted inputs missing: ' + repr(report['missing_asserted_files']))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    try:
        report = inventory(args.root)
        workflow = args.root / WORKFLOW
        original = workflow.read_text('utf-8')
        if args.write:
            if report['missing_asserted_files']:
                raise ValueError('refusing generation with missing asserted inputs')
            workflow.write_text(render(original, report['expected_triggers']), encoding='utf-8')
        errors = check(args.root, workflow.read_text('utf-8'), report)
        report['errors'] = errors
        report['verdict'] = 'FAIL' if errors else 'PASS'
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + '\n')
        print(f"PIN1 {report['verdict']}: {report['asserted_count']} asserted, "
              f"{report['trigger_count']} exact triggers per event, "
              f"{len(report['triggered_not_digest_asserted'])} checker dependencies")
        for error in errors:
            print(error, file=sys.stderr)
        return 1 if errors else 0
    except (OSError, ValueError, KeyError, AttributeError) as exc:
        print(f'PIN1 UNMEASURED: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
