#!/usr/bin/env python3
"""
classify.py  —  LundyLoop instrument  [LL-INST-05]  — REQUIRED STAGE

WHY THIS EXISTS

  Zero is the most dangerous result an instrument can return. It is
  simultaneously the answer for

      ABSENT           the thing should be here and is not      -> a defect
      NOT_APPLICABLE   it was never meant to be here            -> a convention
      DIFFERENT_MODEL  solved another way, and I can name which -> fine
      NOT_DETERMINED   I could not classify this file           -> my ignorance
      DYNAMIC          built at runtime, I cannot see it        -> unverifiable
      UNREADABLE       I could not parse it at all              -> my failure

  FIVE of those six are not defects, and this estate has conflated them with
  ABSENT at least five separate times on the print subsystem alone:

    1. 691 absent print slots / 123 files  -> v1's hardcoded tier vocabulary
                                              (foundation/middle/higher vs
                                               supported/standard/stretch)
    2. 12 print buttons "wired to nothing" -> 8 were document-native
    3. 4 "genuine dead controls"           -> 3 build their pack at runtime
    4. 13 ABSENT, then 0, then 7           -> the dynamic gate, twice wrong
    5. 7 "dead" incl. two AQA evidence     -> they use .print-doc / .pp / .slip
                                              instead of .print-section

  Final answer after all five: ABSENT = 0. There is not one dead print control
  in this estate. Every finding in that chain was the instrument's.

  THE LESSON, and it is not "be careful": every one of those five was a
  VOCABULARY test wearing a presence test's clothes. Asking "does it have
  .print-section" sounds literal but silently assumes the name. Asking "does
  the container have content" is presence, and presence does not need to know
  what the content is called. Where you can, test for the thing; never for its
  name.

  THE COMPLETION CRITERION, binding on every counting instrument in tools/:
  an instrument that cannot say WHICH of these a zero is, is not finished.

  THE COMPLETION CRITERION, binding on every counting instrument in tools/:
  an instrument that cannot say WHICH of these a zero is, is not finished.
  Classify before you count. Report NOT_APPLICABLE and DIFFERENT_MODEL as
  first-class verdicts, never folded into "none".

USAGE

    from classify import Verdict, classify_print_architecture
    v = classify_print_architecture(src)
    if v.verdict is not Verdict.APPLICABLE:
        # do not count this file; report its verdict and reason instead
        ...

WHAT THIS MODULE STRUCTURALLY CANNOT DO

  It cannot recognise a model nobody has told it about. A genuinely novel
  print architecture returns DIFFERENT_MODEL with reason "unrecognised", which
  is honest but is not the same as understanding it. That verdict is an
  instruction to a human to look, not a disposition.

STATUS: current
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Verdict(str, Enum):
    APPLICABLE = "APPLICABLE"            # count it
    ABSENT = "ABSENT"                    # genuinely missing — a defect
    NOT_APPLICABLE = "NOT_APPLICABLE"    # never meant to be here
    DIFFERENT_MODEL = "DIFFERENT_MODEL"  # solved another way, and I can name which
    NOT_DETERMINED = "NOT_DETERMINED"    # I could not classify this. NOT a synonym for
                                         # DIFFERENT_MODEL: that one asserts a positive
                                         # identification, this one asserts ignorance.
                                         # Folding these together is the zero rule failing
                                         # one level up.
    DYNAMIC = "DYNAMIC"                  # built at runtime — not statically countable
    UNREADABLE = "UNREADABLE"            # parse failed — my problem, not the file's


@dataclass(frozen=True)
class Classification:
    verdict: Verdict
    model: str
    reason: str

    def countable(self) -> bool:
        return self.verdict is Verdict.APPLICABLE


# --- print architectures known to this estate -------------------------------

CHASSIS_AREA = re.compile(r"""id\s*=\s*["']print-area["']""")
CHASSIS_SLOT = re.compile(r"""class\s*=\s*["'][^"']*\bprint-section\b""")
NATIVE_MEDIA = re.compile(r"@media\s+print")
NATIVE_SECTION = re.compile(r"""class\s*=\s*["'][^"']*\bsection\b""")
NATIVE_TARGET = re.compile(r"\bprint-target\b|\bprint-one\b")
ANY_PRINT_FN = re.compile(r"function\s+print\w*\s*\(")
ANY_WINDOW_PRINT = re.compile(r"\bwindow\.print\s*\(")
WHOLE_PAGE = re.compile(r"\bwindow\.print\s*\(")
# NOT "does this file build DOM anywhere" — almost every interactive lesson does,
# and that gate returned ABSENT=0 estate-wide, which is too clean to be true.
# It must be "does it build DOM INTO THE PRINT CONTAINER".
BUILDS_INTO_PRINT = re.compile(
    r"""(?:getElementById\(['"]print-[\w-]+['"]\)|\bprintArea\b)\s*\.?\s*"""
    r"""(?:innerHTML\s*=|appendChild|insertAdjacentHTML)""")
_PRINT_FN_BODY = re.compile(r"function\s+print\w*\s*\([^)]*\)\s*\{(.{0,2000}?)\n\s*\}", re.S)
_DOM_BUILD = re.compile(r"innerHTML\s*=|createElement\(|appendChild\(|insertAdjacentHTML\(")


_TAG = re.compile(r"<[^>]+>")

def _print_area_has_content(src: str) -> bool:
    """Does #print-area contain any visible content in the markup? Presence only —
    deliberately blind to what the content is called."""
    i = src.find('id="print-area"')
    if i < 0:
        i = src.find("id='print-area'")
        if i < 0:
            return False
    j = src.find(">", i)
    if j < 0:
        return False
    inner = src[j + 1:j + 20001]
    return len(" ".join(_TAG.sub(" ", inner).split())) > 40


def _builds_print_content(src: str) -> bool:
    if BUILDS_INTO_PRINT.search(src):
        return True
    return any(_DOM_BUILD.search(m.group(1)) for m in _PRINT_FN_BODY.finditer(src))


def classify_print_architecture(src: str) -> Classification:
    """Which print model does this file use? Decide BEFORE counting slots."""
    if not src:
        return Classification(Verdict.UNREADABLE, "-", "empty or unreadable source")

    has_fn = bool(ANY_PRINT_FN.search(src) or ANY_WINDOW_PRINT.search(src))
    if not has_fn and not NATIVE_MEDIA.search(src):
        return Classification(Verdict.NOT_APPLICABLE, "none",
                              "no print machinery of any kind — this file does not "
                              "claim to print, so a slot count is meaningless")

    chassis = bool(CHASSIS_AREA.search(src))
    slots = len(CHASSIS_SLOT.findall(src))
    native = bool(NATIVE_MEDIA.search(src)
                  and NATIVE_SECTION.search(src)
                  and NATIVE_TARGET.search(src))

    if native and not chassis:
        return Classification(
            Verdict.DIFFERENT_MODEL, "document-native",
            "prints the document itself via @media print rules on .section, with "
            "print-target/print-one for single-section printing. Has no #print-area "
            "and needs none. Zero .print-section here is correct, not a gap.")

    if chassis and slots:
        return Classification(Verdict.APPLICABLE, "chassis",
                              f"#print-area with {slots} .print-section slots")

    if chassis and not slots:
        # DO NOT ask "does it have .print-section". That is a vocabulary test, and
        # vocabulary tests have now produced a false defect five times running on
        # this one subsystem: foundation/middle/higher; print-section as the only
        # slot class; chassis as the only model; DOM-building-anywhere; and
        # print-section again. The Rivers files use .print-doc, the AQA evidence
        # files use .pp, the ASDAN homework uses .slip. All three print correctly.
        # Ask instead whether the container HAS CONTENT. That is presence, and
        # presence does not need to know what the content is called.
        if _print_area_has_content(src):
            return Classification(
                Verdict.DIFFERENT_MODEL, "chassis-other-blocks",
                "#print-area holds real print content under block classes this "
                "module does not enumerate (.print-doc / .pp / .slip and others). "
                "Zero .print-section is a vocabulary difference, not a gap.")
        if _builds_print_content(src):
            return Classification(
                Verdict.DYNAMIC, "chassis-dynamic",
                "#print-area is empty at rest but the file builds print content at "
                "runtime. A static count cannot see it. NOT a defect — and NOT a "
                "pass either: it needs rendering to verify.")
        return Classification(
            Verdict.ABSENT, "chassis",
            "#print-area present, genuinely empty in the markup, and nothing builds "
            "content into it at runtime — wired to nothing. A defect.")

    if native and chassis:
        return Classification(Verdict.APPLICABLE, "hybrid",
                              "both models present; count chassis slots but read by eye")

    if WHOLE_PAGE.search(src) and NATIVE_MEDIA.search(src):
        return Classification(
            Verdict.DIFFERENT_MODEL, "whole-page",
            "prints the document as it stands: @media print hides the chrome and "
            "window.print() is called directly. No slots by design — this model has "
            "no concept of them. Zero .print-section is correct.")

    return Classification(
        Verdict.NOT_DETERMINED, "unrecognised",
        "has print machinery but matches no model known to this module. This is a "
        "statement about the classifier, not the file. NOT a gap, and NOT a "
        "different model either — it is undetermined, and must be reported as its "
        "own headline figure so a reader never mistakes it for a clean result.")


def summarise(classifications) -> dict:
    """Roll up a list of Classification into counts per verdict. Never collapses
    NOT_APPLICABLE or DIFFERENT_MODEL into ABSENT."""
    out = {v.value: 0 for v in Verdict}
    for c in classifications:
        out[c.verdict.value] += 1
    return out
