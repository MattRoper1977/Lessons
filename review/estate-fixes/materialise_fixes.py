#!/usr/bin/env python3
"""Materialise the proposed estate fixes on an exact Lessons base worktree.

Every transformation asserts its unique preimage and every writable path is listed
explicitly. Git then generates the canonical diff from the immutable base.
"""

from __future__ import annotations

import argparse
import pathlib
import re
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
        'class="timer-display" id="indep-timer-display"',
        'class="timer-display indep-timer-display"',
        expected=2,
        label="Digestion duplicate timer IDs",
    )

    timer_match = re.search(
        r"  // --- Independent Work Timer ---\n.*?(?=\n\n</script>)",
        text,
        flags=re.S,
    )
    if timer_match is None:
        raise RuntimeError("Digestion timer block: expected one measured block, found 0")
    new_timer_block = """  // --- Independent Work Timer ---
  let indepInterval=null;let indepSeconds=480;let indepPaused=false;
  function eachIndepDisplay(fn){document.querySelectorAll('.indep-timer-display').forEach(fn);}
  function startIndepTimer(secs){
    if(indepPaused&&!secs){indepPaused=false;}
    else{clearInterval(indepInterval);indepSeconds=secs||480;}
    indepPaused=false;
    updateIndepDisplay();
    indepInterval=setInterval(function(){
      if(!indepPaused){indepSeconds--;updateIndepDisplay();
      if(indepSeconds<=0){clearInterval(indepInterval);
        eachIndepDisplay(d=>{d.textContent='TIME UP!';d.classList.add('timer-warning');});
      }}
    },1000);
  }
  function pauseIndepTimer(){indepPaused=!indepPaused;eachIndepDisplay(d=>{d.style.opacity=indepPaused?'.5':'1';});}
  function resetIndepTimer(){clearInterval(indepInterval);indepSeconds=480;indepPaused=false;updateIndepDisplay();eachIndepDisplay(d=>{d.classList.remove('timer-warning');d.style.opacity='1';});}
  function updateIndepDisplay(){const m=Math.floor(indepSeconds/60);const s=indepSeconds%60;eachIndepDisplay(d=>{d.textContent=String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');d.classList.toggle('timer-warning',indepSeconds<=60&&indepSeconds>0);});}"""
    text = text[: timer_match.start()] + new_timer_block + text[timer_match.end() :]

    tail_match = re.search(
        r"(?P<html_close></html>)(?P<box><div class=\"scaffold-box animate-enter\".*?</div>)\s*$",
        text,
        flags=re.S,
    )
    if tail_match is None:
        raise RuntimeError("Digestion orphan memory box: expected one document-tail block, found 0")
    memory_box = tail_match.group("box").replace(
        'class="scaffold-box animate-enter"',
        'class="scaffold-box animate-enter memory-trick"',
        1,
    )
    text = text[: tail_match.start("html_close")] + "</html>\n"

    slide_marker = '<div class="slide" data-title="L1 – Independent Work" data-type="independent">'
    slide_start = text.find(slide_marker)
    if slide_start < 0:
        raise RuntimeError("Digestion L1 independent-work slide marker is missing")
    next_slide = text.find('\n<div class="slide"', slide_start + len(slide_marker))
    if next_slide < 0:
        raise RuntimeError("Digestion L1 independent-work slide has no following slide marker")
    block = text[slide_start:next_slide]
    close_at = block.rfind("\n</div>")
    if close_at < 0:
        raise RuntimeError("Digestion L1 independent-work slide has no closing div")
    block = block[:close_at] + "\n  " + memory_box + block[close_at:]
    text = text[:slide_start] + block + text[next_slide:]
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
