#!/usr/bin/env python3
"""SX3: restore what the chassis transplant dropped, and make each deck's binding visible.

ORDER SX3-M2 §7(b) as amended by SX3-M3 §3 and SX3-M5 §1. Two operations, both
RESTORATION of something the transplant removed, neither authoring:

  1. lesson-config binding keys. The transplant REPLACES the deck's
     `lesson-config` block instead of merging it, so the deck loses its tie to
     the scheme of work and to its neighbours: `sow` on every deck that had one,
     and with it `objective`, `week`, `id`, `previousFile`, `nextFile`,
     `timings` and `source`. Those keys are carried back from the deck being
     replaced. `sow` is what build_lesson_order.py's preserved_outcome limb
     compares, and `source` is what its explicit_cell limb reads, which is why
     losing them drops the deck's week binding.

  2. The derived term·week token, for a deck whose base carries no
     `lesson-config` to restore from. The token is taken VERBATIM from
     SCIENCE_WEEK_BINDINGS — never inferred from a filename or a folder — and
     appended to the title slide's existing `.science-meta` line, which is where
     this deck family already displays pathway, subject and week.

Every edit is a surgical text splice. The DOM is parsed to LOCATE and to VERIFY,
never to rewrite: an lxml round-trip would reformat whole documents and put the
zero-visible-delta condition at risk. The tool refuses to write a deck whose
lesson-config does not round-trip byte-identically when unchanged.

  python3 tools/sx3/admit_landing_decks.py --base origin/main [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BINDINGS = "tools/catalogue/SCIENCE_WEEK_BINDINGS.json"
# Carried back from the base deck. Every one of these is a binding: what the
# lesson teaches (sow, objective), when it sits (week), what it is called
# internally (id), what it sits between (previousFile, nextFile), how it is
# paced (timings), and which workbook cell it answers to (source). None of them
# is content the pack authored, and none of them renders.
BINDING_KEYS = ("sow", "objective", "week", "id", "previousFile", "nextFile",
                "timings", "source")
CONFIG_RE = re.compile(r'(<script[^>]*id="lesson-config"[^>]*>)(.*?)(</script>)', re.S)
META_RE = re.compile(r'(<p class="science-meta"[^>]*>)(.*?)(</p>)', re.S)


class Refuse(Exception):
    """A condition the tool observed that makes writing unsafe. Never repaired."""


def git_text(ref: str, path: str) -> str | None:
    proc = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT,
                          capture_output=True, text=True)
    return proc.stdout if proc.returncode == 0 else None


def changed_science(base: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD", "--", "Science_Teesside/"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    return sorted(p for p in proc.stdout.split() if p.endswith(".html"))


def config_span(text: str):
    found = CONFIG_RE.findall(text)
    if len(found) > 1:
        raise Refuse("more than one lesson-config block")
    return CONFIG_RE.search(text)


def load_config(text: str):
    match = config_span(text)
    if not match:
        return None, None
    try:
        return json.loads(match.group(2)), match
    except ValueError as exc:
        raise Refuse(f"lesson-config is not valid JSON: {exc}") from exc


def restore_binding_keys(text: str, base_text: str) -> tuple[str, list[str]]:
    config, match = load_config(text)
    base_config, _ = load_config(base_text)
    if config is None or base_config is None:
        return text, []
    # The round-trip must be byte-clean before anything is spliced, or the diff
    # would carry reformatting this tool did not intend and cannot justify.
    if json.dumps(config, ensure_ascii=False) != match.group(2).strip():
        raise Refuse("lesson-config does not round-trip byte-identically; refusing to splice")
    carried = [key for key in BINDING_KEYS if key in base_config and key not in config]
    if not carried:
        return text, []
    merged = dict(config)
    for key in carried:
        merged[key] = base_config[key]
    body = json.dumps(merged, ensure_ascii=False)
    return text[:match.start(2)] + body + text[match.end(2):], carried


def restore_token(text: str, path: str, bindings: dict) -> tuple[str, list[str]]:
    keys = [week["key"] for week in bindings.get(path, {}).get("weeks", [])]
    if not keys:
        return text, []
    missing = [key for key in keys if key not in text]
    if not missing:
        return text, []
    match = META_RE.search(text)
    if not match:
        raise Refuse("no .science-meta line on the title slide to carry the token")
    inner = match.group(2).rstrip()
    addition = "".join(f" · {key}" for key in missing)
    return text[:match.start(2)] + inner + addition + text[match.end(2):], missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    bindings = json.loads((ROOT / BINDINGS).read_text())["entries"]
    decks = changed_science(args.base)
    print(f"SEARCH SCOPE: {len(decks)} Science .html files differing from {args.base}; "
          f"binding keys carried back from that same ref; tokens read verbatim from {BINDINGS}")

    carried_total, token_total, untouched, refused = {}, {}, [], []
    for rel in decks:
        source = ROOT / rel
        if not source.is_file():
            continue
        text = original = source.read_text()
        base_text = git_text(args.base, rel)
        try:
            if base_text is not None:
                text, carried = restore_binding_keys(text, base_text)
                if carried:
                    carried_total[rel] = carried
            if base_text is None or load_config(base_text)[0] is None:
                text, tokens = restore_token(text, rel, bindings)
                if tokens:
                    token_total[rel] = tokens
        except Refuse as exc:
            refused.append((rel, str(exc)))
            continue
        if text == original:
            untouched.append(rel)
        elif not args.check:
            source.write_text(text)

    print(f"\n  binding keys restored : {len(carried_total)} deck(s)")
    print(f"  derived token written : {len(token_total)} deck(s)")
    print(f"  already correct       : {len(untouched)} deck(s)")
    print(f"  REFUSED               : {len(refused)} deck(s)")
    for rel, why in refused:
        print(f"     {rel}: {why}")
    for rel, tokens in sorted(token_total.items()):
        print(f"     token {tokens} -> {rel}")
    if args.check and (carried_total or token_total):
        print("\n--check: work remains; nothing was written")
        return 1
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
