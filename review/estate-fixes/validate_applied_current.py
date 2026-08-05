#!/usr/bin/env python3
"""Current invariant layer for the exact estate-fix proposal.

The original validator remains available for review. This layer reuses all of its
parsing, path, SVG and browser checks, replacing only two digestion assertions that
were written against an earlier markup sample rather than the measured base blob.
"""

from __future__ import annotations

import importlib.util
import pathlib
import re
import sys
from typing import Sequence


BASE_SCRIPT = pathlib.Path(__file__).with_name("validate_applied.py")
SPEC = importlib.util.spec_from_file_location("estate_fix_base_validator", BASE_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load base validator: {BASE_SCRIPT}")
base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)


class Validator(base.Validator):
    """Reuse the full validator and correct measured digestion invariants."""

    def _check_specific_invariants(self) -> None:
        start = len(self.findings)
        super()._check_specific_invariants()

        superseded = {
            "Expected two timer displays",
            "Memory trick was not moved inside the document body",
        }
        retained = []
        for finding in self.findings[start:]:
            if finding.path == base.DIGESTION and finding.message in superseded:
                continue
            retained.append(finding)
        self.findings[start:] = retained

        digestion = (self.repo / base.DIGESTION).read_text(encoding="utf-8")
        timer_classes = re.findall(
            r'class="[^"]*\bindep-timer-display\b[^"]*"',
            digestion,
            flags=re.I,
        )
        if len(timer_classes) != 2:
            self.error(base.DIGESTION, "Expected two class-based timer displays", len(timer_classes))

        first_slide_marker = '<div class="slide" data-title="L1 – Independent Work" data-type="independent">'
        first_slide = digestion.find(first_slide_marker)
        next_slide = digestion.find('\n<div class="slide"', first_slide + len(first_slide_marker)) if first_slide >= 0 else -1
        memory = digestion.find('class="scaffold-box animate-enter memory-trick"')
        memory_phrase = digestion.find("Amylase Makes Maltose, Maltase Makes Glucose")
        body_close = digestion.lower().rfind("</body>")
        if not (0 <= first_slide < memory < next_slide < body_close and memory <= memory_phrase < next_slide):
            self.error(
                base.DIGESTION,
                "Measured memory trick was not placed inside the L1 independent-work slide",
                {
                    "first_slide": first_slide,
                    "memory": memory,
                    "memory_phrase": memory_phrase,
                    "next_slide": next_slide,
                    "body_close": body_close,
                },
            )


def main(argv: Sequence[str] | None = None) -> int:
    args = base.parse_args(argv or sys.argv[1:])
    validator = Validator(
        pathlib.Path(args.repo),
        pathlib.Path(args.site_root),
        pathlib.Path(args.output),
    )
    return validator.run(args.browser)


if __name__ == "__main__":
    raise SystemExit(main())
