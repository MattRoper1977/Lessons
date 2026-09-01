#!/usr/bin/env python3
"""Order VB cohort A g16: the FEB frozen-denominator gate re-pointed, unchanged,
at the RSH-3 pinned 225-row contract (sha256 e0f8f546...) and the RSH-3
denominators (86/76/80/87). Semantics are g16_frozen.py's own — this file
only swaps the two module-level paths so cohort A is judged against the
contract it was built to, resolved by hash, never by the live path.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "g16_frozen", ROOT / "_sownb/feb/tools/g16_frozen.py"
)
g16 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(g16)

g16.CONTRACT = ROOT / "_sownb/vb/STYLE_CONTRACT_RSH3_PINNED.json"
g16.DENOMS = ROOT / "_sownb/G16_DENOMINATORS_RSH3.json"

if __name__ == "__main__":
    sys.exit(g16.main())
