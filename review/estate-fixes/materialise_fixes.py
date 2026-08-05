#!/usr/bin/env python3
"""Materialise the proposed estate fixes on an exact Lessons base worktree.

This script is deliberately narrow: every replacement asserts its expected count,
and every writable path is listed explicitly. It is used to let Git generate the
canonical unified diff from the immutable base rather than trusting hand-written
hunk offsets.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil

GRID = pathlib.PurePosixPath("Games/Grid_Chase.html")
DIGESTION = pathlib.PurePosixPath("biology/Digestion_and_Absorption (1).html")
INDEX = pathlib.PurePosixPath("index.html")
POSTER = pathlib.PurePosixPath("assets/video/poster-art.svg")
MOTION = [
    pathlib.PurePosixPath("Science_Teesside/Build/SCI_B_W3_Backbones.html"),
    pathlib.PurePosixPath("Science_Teesside/Build/SCI_B_W4_Muscle_Pairs.html"),
    pathlib.PurePosixPath("Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html"),
    pathlib.PurePosixPath("Science_Teesside/Build/SCI_B_W6_Balanced_Plate.html"),
    pathlib.PurePosixPath("Science_Teesside/Build/SCI_B_W7_Where_Food_Comes_From.html"),
    pathlib.PurePosixPath("Science_Teesside/Grow/SCI_G_W3_Friction.html"),
    pathlib.PurePosixPath("Science_Teesside/Grow/SCI_G_W4_Mechanisms.html"),
    pathlib.PurePosixPath("Science_Teesside/Grow/SCI_G_W5_Fair_Test.html"),
    pathlib.PurePosixPath("Science_Teesside/Grow/SCI_G_W6_Earth_And_Planets.html"),
    pathlib.PurePosixPath("Science_Teesside/Grow/SCI_G_W7_The_Moon.html"),
]


def replace_exact(text: str, old: str, new: str, *, expected: int, label: str) -> str:
    actual = text.count(old)
    if actual != expected:
        raise RuntimeError(f"{label}: expected {expected} exact match(es), found {actual}")
    return text.replace(old, new)


def read(root: pathlib.Path, rel: pathlib.PurePosixPath) -> str:
    return root.joinpath(*rel.parts).read_text(encoding="utf-8")


def write(root: pathlib.Path, rel: pathlib.PurePosixPath, text: str) -> None:
    root.joinpath(*rel.parts).write_text(text, encoding="utf-8", newline="")


def transform_grid(root: pathlib.Path) -> None:
    text = read(root, GRID)
    changes = [
        (
            'https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap',
            'https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&amp;display=swap',
            "Grid Chase Google Fonts query",
        ),
        (
            '#title{font-size:32px;font-weight:900;letter-spacing:5px;color:var(--cyan);text-shadow:0 0 22px var(--cyan);text-align:center}',
            '.panel-title{font-size:32px;font-weight:900;letter-spacing:5px;color:var(--cyan);text-shadow:0 0 22px var(--cyan);text-align:center}',
            "Grid Chase title selector",
        ),
        ('<div id="title">GRID CHASE</div>', '<div class="panel-title">GRID CHASE</div>', "Grid Chase menu title"),
        ('<div id="title" style="font-size:24px">PAUSED</div>', '<div class="panel-title" style="font-size:24px">PAUSED</div>', "Grid Chase pause title"),
        ('<div id="title" style="font-size:24px">GRID DOWN</div>', '<div class="panel-title" style="font-size:24px">GRID DOWN</div>', "Grid Chase result title"),
        ('<input type="number" id="seed-input" placeholder="seed">', '<input type="number" id="seed-input" placeholder="seed" aria-label="Maze seed">', "Grid Chase seed input"),
        ('<input type="text" id="initials-input" maxlength="3" placeholder="AAA">', '<input type="text" id="initials-input" maxlength="3" placeholder="AAA" aria-label="Leaderboard initials">', "Grid Chase initials input"),
        ('<input type="text" id="share-str" readonly>', '<input type="text" id="share-str" readonly aria-label="Share result code">', "Grid Chase share input"),
    ]
    for old, new, label in changes:
        text = replace_exact(text, old, new, expected=1, label=label)
    write(root, GRID, text)


def transform_digestion(root: pathlib.Path) -> None:
    text = read(root, DIGESTION)
    text = replace_exact(
        text,
        ".indep-controls button { margin: 0 6px; }",
        ".indep-timer-display { font-weight: 800; }\n    .indep-controls button { margin: 0 6px; }",
        expected=1,
        label="Digestion timer class style",
    )
    text = replace_exact(
        text,
        'id="indep-timer-display"',
        'class="indep-timer-display"',
        expected=2,
        label="Digestion duplicate timer IDs",
    )
    old_render = """      const el = document.getElementById('indep-timer-display');
      if(!el) return;
      const minutes = Math.floor(indepRemaining / 60);
      const seconds = indepRemaining % 60;
      el.textContent = `${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}`;
"""
    new_render = """      const minutes = Math.floor(indepRemaining / 60);
      const seconds = indepRemaining % 60;
      document.querySelectorAll('.indep-timer-display').forEach(el => {
        el.textContent = `${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}`;
      });
"""
    text = replace_exact(text, old_render, new_render, expected=1, label="Digestion timer renderer")
    old_section = """      <p><strong>Success looks like:</strong> Answers use the correct key words and explain how each process helps digestion.</p>
    </div>
  </section>

  <script>
"""
    new_section = """      <p><strong>Success looks like:</strong> Answers use the correct key words and explain how each process helps digestion.</p>
    </div>
    <div class="memory-trick">Amylase Makes Maltose · Protease Produces Peptides · Lipase Liberates Lipids</div>
  </section>

  <script>
"""
    text = replace_exact(text, old_section, new_section, expected=1, label="Digestion memory-trick placement")
    text = replace_exact(
        text,
        "</html>\n    <div class=\"memory-trick\">Amylase Makes Maltose · Protease Produces Peptides · Lipase Liberates Lipids</div>\n",
        "</html>\n",
        expected=1,
        label="Digestion orphan document tail",
    )
    write(root, DIGESTION, text)


def transform_index(root: pathlib.Path, poster_source: pathlib.Path) -> None:
    text = read(root, INDEX)
    text = replace_exact(
        text,
        'src="/assets/video/poster-art.jpg"',
        'src="assets/video/poster-art.svg"',
        expected=1,
        label="Lesson Hub poster URL",
    )
    write(root, INDEX, text)
    destination = root.joinpath(*POSTER.parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(poster_source, destination)


def transform_motion_filters(root: pathlib.Path) -> None:
    old = "@supports (filter: url(#g-mblur)) { .g-blur-fast { filter: url(#g-mblur); } }"
    for rel in MOTION:
        text = read(root, rel)
        text = replace_exact(text, old, "", expected=1, label=f"Undefined g-mblur filter in {rel}")
        write(root, rel, text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--poster", required=True)
    args = parser.parse_args()
    root = pathlib.Path(args.repo).resolve()
    poster = pathlib.Path(args.poster).resolve()
    transform_grid(root)
    transform_digestion(root)
    transform_index(root, poster)
    transform_motion_filters(root)
    print("Materialised Grid, Digestion, Lesson Hub poster and ten motion-filter fixes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
