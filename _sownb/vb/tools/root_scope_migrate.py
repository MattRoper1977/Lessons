#!/usr/bin/env python3
"""RUN12-A: move :root redefinitions under the pathway scope selector.

The ruling: a token is DEFINED once, in :root; pathway values live under the
pathway scope selector only; a second definition in :root is a red.

The classic chassis carries two, three or four :root blocks -- an estate base
followed by subject/strand palette overrides. This rewrites each later block in
place as two rules:

    :root{ <tokens this block introduces> }
    html.pathway-<lane>{ <tokens this block REdefines> }

and puts class="pathway-<lane>" on <html>.

Why html and not body: the tokens stay declared on the same element they are
declared on today, so anything reading them from document.documentElement reads
the same value. html.pathway-x has specificity (0,1,1) against :root's (0,1,0),
so the override wins wherever it wins today, and the rules keep their document
order, so an override of an override still resolves the same way. Nothing moves
across a media query: no deck declares :root inside one (measured, 0 of 175).

Only redefinitions move. A token a later block introduces for the first time is
already defined once and stays exactly where it is.

Usage: root_scope_migrate.py <deck.html> [<deck.html> ...] [--dry-run]
A deck whose shape does not match is reported HELD and left untouched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DECL = re.compile(r"(--[A-Za-z_][\w-]*)\s*:\s*([^;}]+);?")
LANE = (("BUILD", "build"), ("GROW", "grow"), ("LAUNCH", "launch"))
MARK = "/* RUN12-A pathway scope */"


def lane_of(path: Path, source: str) -> str | None:
    text = str(path).upper()
    for token, lane in LANE:
        if text.startswith(token) or f"/{token}_" in text or f"/{token}/" in text:
            return lane
    match = re.search(r'"family"\s*:\s*"(BUILD|GROW|LAUNCH)', source)
    if match:
        return match.group(1).lower()
    for token, lane in LANE:
        if re.search(rf"\b{token}\b", source[:4000]):
            return lane
    return None


def root_blocks(source: str) -> list[re.Match]:
    return list(re.finditer(r":root\s*\{([^}]*)\}", source))


def in_at_rule(source: str, index: int) -> bool:
    """True when the character at index sits inside an unclosed @media/@supports."""
    for match in re.finditer(r"@(?:media|supports)[^{]*\{", source[:index]):
        depth = 1
        for char in source[match.end() : index]:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    break
        if depth > 0:
            return True
    return False


def migrate(source: str, lane: str) -> tuple[str, dict]:
    blocks = root_blocks(source)
    if len(blocks) < 2:
        return source, {"held": "one :root block; nothing to move"}
    if any(in_at_rule(source, b.start()) for b in blocks):
        return source, {"held": "a :root block sits inside an at-rule"}
    seen: set[str] = {name for name, _ in DECL.findall(blocks[0].group(1))}
    moved: list[str] = []
    out, cursor = [], 0
    for block in blocks[1:]:
        body = block.group(1)
        keep, scope = [], []
        for match in DECL.finditer(body):
            name, value = match.group(1), match.group(2).strip()
            (scope if name in seen else keep).append((name, value))
            if name in seen:
                moved.append(name)
            else:
                seen.add(name)
        if not scope:
            continue
        rebuilt = ""
        if keep:
            rebuilt += ":root{" + "".join(f"{n}:{v};" for n, v in keep) + "}"
        rebuilt += f"html.pathway-{lane}{{" + "".join(f"{n}:{v};" for n, v in scope) + "}" + MARK
        out.append(source[cursor : block.start()])
        out.append(rebuilt)
        cursor = block.end()
    if not moved:
        return source, {"held": "no token is redefined; already conformant"}
    out.append(source[cursor:])
    result = "".join(out)

    html_tag = re.search(r"<html\b([^>]*)>", result)
    if not html_tag:
        return source, {"held": "no <html> tag"}
    attrs = html_tag.group(1)
    if "class=" in attrs:
        updated = re.sub(r'class="([^"]*)"', lambda m: f'class="{m.group(1)} pathway-{lane}"', attrs, count=1)
    else:
        updated = attrs + f' class="pathway-{lane}"'
    result = result[: html_tag.start()] + f"<html{updated}>" + result[html_tag.end() :]
    return result, {"lane": lane, "movedTokens": sorted(set(moved)), "movedDeclarations": len(moved), "rootBlocks": len(blocks)}


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    held, done = [], []
    for name in args:
        path = Path(name)
        source = path.read_text(encoding="utf-8")
        if MARK in source:
            print(f"already   {name}")
            continue
        lane = lane_of(path, source)
        if lane is None:
            held.append((name, "lane not derivable"))
            print(f"HELD      {name}  lane not derivable")
            continue
        result, note = migrate(source, lane)
        if "held" in note:
            held.append((name, note["held"]))
            print(f"HELD      {name}  {note['held']}")
            continue
        if not dry:
            path.write_text(result, encoding="utf-8")
        done.append((name, note))
        print(f"{'would   ' if dry else 'migrated'}  {name}  {note['movedDeclarations']} declarations, {len(note['movedTokens'])} tokens -> html.pathway-{lane}")
    print(f"\n{len(done)} migrated, {len(held)} held")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
