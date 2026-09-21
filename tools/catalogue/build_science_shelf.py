"""Build the static Science shelf (ORDER SCI-COMPLETE PASS F, 2026-09-21).

Since PASS F the Science shelf is the Science hub in HUB-1 shape, written by
build_science_hub.py from the same pinned records; this entry point remains so every
caller, the four-writer sweep included, regenerates the hub through the one writer.
"""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / 'build_science_hub.py'), run_name='__main__')
