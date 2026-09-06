#!/usr/bin/env python3
"""Pin the explicitly reviewed education catalogue in both estate gate copies.

This is a deliberate review operation, never a CI repair. The row-preservation
check is independent of the moved digest: re-pinning cannot hide a removed,
reordered or rewritten original resource. Run builders and QA before this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

GATE = "tools/verify_cross_estate_unification.py"
ORIGINAL_ROW_COUNT = 734
ORIGINAL_ROWS_SHA256 = "b8ffcb16f5fd2a413e8a0b06ad2d4b112f450364fa294377869dc32c8235bb2c"
SHELF_ROWS = [
    {
        "subject": "Science · Teesside", "title": "Science · browse by pathway, term and teaching version",
        "file": "Science_Teesside/index.html", "id": "science-pathway-term-hub", "type": "hub", "family": "Science Teesside",
        "keywords": ["science", "build", "grow", "launch", "pathway", "term", "lesson hub"],
        "desc": "Choose a Science pathway and term, then browse the recommended sequence and retained teaching versions.",
        "added": "2026-09-05", "new": True, "year": "2026-27"
    },
    {
        "subject": "Humanities · Teesside", "title": "Humanities · browse by pathway, term and teaching version",
        "file": "Humanities_Teesside/index.html", "id": "humanities-pathway-term-hub", "type": "hub", "family": "Humanities Teesside",
        "keywords": ["humanities", "religious education", "build", "grow", "launch", "pathway", "term", "lesson hub"],
        "desc": "Choose a Humanities pathway and term, then browse current lessons, retained teaching versions and classroom references.",
        "added": "2026-09-05", "new": True, "year": "2026-27"
    },
    {
        "subject": "Humanities · Teesside", "title": "Humanities and RE cover pack · Autumn 1 Weeks 3–7",
        "file": "Humanities_Teesside/David_Cover_Autumn1_W3-W7/index.html", "id": "david-humanities-re-cover-hub", "type": "hub", "family": "Humanities Teesside",
        "keywords": ["humanities", "religious education", "david", "cover", "build", "grow", "launch", "autumn 1", "weeks 3–7", "downloads"],
        "desc": "Twenty-five 40-minute cover periods with PowerPoint, Word and PDF downloads, linked to the existing Humanities and RE lessons.",
        "added": "2026-09-05", "new": True, "year": "2026-27"
    }
]

# Exact reviewed files, not patterns. A future new UI file requires an explicit
# change here; a lesson cannot become permitted because it shares a directory.
# The verifier and pin tool exclude themselves to avoid a recursive file hash.
REVIEWED_PATHS = (
    "index.html", "Science_Teesside/index.html", "Humanities_Teesside/index.html", "humanities_teesside.html",
    "Humanities_Teesside/David_Cover_Autumn1_W3-W7/index.html",
    "assets/catalogue/catalogue.css", "assets/catalogue/catalogue.js",
    "assets/catalogue/lesson-navigation.js",
    "assets/catalogue/science-shelf.css", "assets/catalogue/science-shelf.js",
    "assets/catalogue/terms-and-styles.json", "assets/catalogue/science-shelf.json", "assets/catalogue/humanities-shelf.json",
    "tools/catalogue/build_catalogue.py", "tools/catalogue/build_science_shelf.py", "tools/catalogue/build_humanities_shelf.py",
    "tools/catalogue/check_catalogue_static.py", "tools/catalogue/check_catalogue_dom.cjs", "tools/catalogue/verify_education_navigation.cjs",
    "tools/catalogue/SHELF_SELECTION.json", "tools/catalogue/HUMANITIES_SELECTION.json",
    "tools/easter/science_original_browser.cjs",
    "tools/prepare_served_publications.py", "tools/test_served_publications.py",
    # GLV3 admits only these reviewed publisher checks and cover inputs.
    ".github/workflows/glv3-verify.yml", "_glv3/tools/verify_change_boundary.py",
    "_glv3/tools/browser_verify.mjs", "_glv3/tools/chip_gate.mjs",
    "tools/humanities_resources/SOURCE_MANIFEST.json", "tools/humanities_resources/DOWNLOAD_MANIFEST.json",
    "tools/humanities_resources/CONTENT.json", "tools/humanities_resources/ORIGINAL_MEMBER_MANIFEST.json",
    "tools/humanities_resources/build_resources.py", "tools/humanities_resources/check_resources.py",
    "tools/humanities_resources/resource.css", "tools/humanities_resources/resource.js",
    "tools/catalogue/TERM_AND_STYLE_EVIDENCE.json", "tools/catalogue/TERM_REVIEW.json",
    "tools/catalogue/SCIENCE_WEEK_BINDINGS.json",
    # Recovered reviewed Education correction: gravity statements explicitly
    # condition equal free-fall on negligible air resistance in both formats.
    "primary/year5/science/autumn/forces/Lesson8_ExploreGravity.html",
    "primary/year5/science/autumn/forces/Y5_Forces_SoW_and_Plans.docx",
)


# Owner-reviewed additive Science download transaction, 6 September 2026.
# Every path is explicit; no directory wildcard can admit future payloads.
REVIEWED_PATHS += ('assets/catalogue/science-download-bindings.json', 'Science_Teesside/Teaching_Packs/BUILD/BUILD_Science_Autumn1_W3-W7_Teaching_Guide.docx', 'Science_Teesside/Teaching_Packs/BUILD/BUILD_Science_Autumn1_W3-W7_Teaching_Guide.pdf', 'Science_Teesside/Teaching_Packs/BUILD/DOWNLOAD_INDEX.json', 'Science_Teesside/Teaching_Packs/BUILD/SOURCE_MANIFEST.json', 'Science_Teesside/Teaching_Packs/BUILD/START_HERE.txt', 'Science_Teesside/Teaching_Packs/BUILD/assets/made-by-matt-approved.jpg', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3-W7_Complete_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3A_Backbones_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3_Teaching_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W4B_Muscle_Model_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W4_Teaching_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W5A_Body_Needs_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W5_Teaching_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W6A_Balanced_Plate_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W6_Teaching_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W7A_Food_Sources_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Lesson_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W7_Teaching_Pack.zip', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation.pptx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Pupil.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Pupil.pdf', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Teacher.docx', 'Science_Teesside/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Teacher.pdf', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W3_Cards_and_Labels.docx', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W3_Cards_and_Labels.pdf', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W4_Cards_and_Labels.docx', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W4_Cards_and_Labels.pdf', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W5_Cards_and_Labels.docx', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W5_Cards_and_Labels.pdf', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W6_Cards_and_Labels.docx', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W6_Cards_and_Labels.pdf', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W7_Cards_and_Labels.docx', 'Science_Teesside/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W7_Cards_and_Labels.pdf', 'Science_Teesside/Teaching_Packs/GROW/DOWNLOAD_INDEX.json', 'Science_Teesside/Teaching_Packs/GROW/SOURCE_MANIFEST.json', 'Science_Teesside/Teaching_Packs/GROW/START_HERE.pdf', 'Science_Teesside/Teaching_Packs/GROW/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/assets/made-by-matt-approved.jpg', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3A.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3B.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W4A.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W4B.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W5A.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W5B.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W6A.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W6B.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W7A.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W7B.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week3.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week4.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week5.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week6.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week7.zip', 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Weeks3-7_Teaching_Pack.zip', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_W3B_Friction_Measurements.xlsx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4A/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W4B/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5A/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/GROW_W5B_Fair_Test_Measurements.xlsx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W5B/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6A/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W6B/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7A/START_HERE.txt', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon.pptx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Pupil.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Pupil.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Teacher.docx', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Teacher.pdf', 'Science_Teesside/Teaching_Packs/GROW/lessons/W7B/START_HERE.txt', 'Science_Teesside/Teaching_Packs/index.html', 'Science_Teesside/Teaching_Packs/packs.css', 'tools/science_teaching_packs/BUILD_QA.json', 'tools/science_teaching_packs/BUILD_SOURCE_PROVENANCE.json', 'tools/science_teaching_packs/GROW_QA.json', 'tools/science_teaching_packs/build_hub.py', 'tools/science_teaching_packs/check_packs.py')

# Exact public-title-only amendment; teaching content and native files retained.
REVIEWED_PATHS += ('tools/humanities_resources/PUBLIC_LABEL_CHANGES.json', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BH_W3.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BH_W4.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BH_W5.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BH_W6.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BH_W7.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BR_W3.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BR_W4.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BR_W5.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BR_W6.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/BR_W7.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GH_W3.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GH_W4.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GH_W5.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GH_W6.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GH_W7.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GR_W3.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GR_W4.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GR_W5.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GR_W6.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/GR_W7.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/LH_W3.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/LH_W4.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/LH_W5.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/LH_W6.html', 'Humanities_Teesside/David_Cover_Autumn1_W3-W7/LH_W7.html')

def row_digest(rows: list) -> str:
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def preserved_rows_errors(rows: list) -> list[str]:
    errors = []
    if len(rows) != ORIGINAL_ROW_COUNT + len(SHELF_ROWS):
        errors.append("catalogue must contain the original 734 rows plus exactly three reviewed hub rows")
    if row_digest(rows[:ORIGINAL_ROW_COUNT]) != ORIGINAL_ROWS_SHA256:
        errors.append("an original catalogue row was removed, reordered or edited")
    if rows[ORIGINAL_ROW_COUNT:] != SHELF_ROWS:
        errors.append("the appended hub rows differ from the three reviewed navigation entries")
    return errors


def module(path: Path):
    spec = importlib.util.spec_from_file_location("catalogue_gate", path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def pin(lessons: Path, apps: Path, *, check: bool) -> dict:
    gates = [lessons / GATE, apps / GATE]
    originals = [p.read_text("utf-8") for p in gates]
    if originals[0] != originals[1]:
        raise ValueError("gate copies differ; reconcile their reviewed logic before pinning. Nothing written")
    rows = json.loads((lessons / "resources.json").read_text("utf-8"))
    errors = preserved_rows_errors(rows)
    if errors:
        raise ValueError("; ".join(errors))
    gate = module(gates[0])
    files = {path: hashlib.sha256((lessons / path).read_bytes()).hexdigest() for path in REVIEWED_PATHS}
    text = (lessons / "index.html").read_text("utf-8")
    pins = {"visible_body_sha256": hashlib.sha256(gate.normalized_visible_body(text, "lessons").encode("utf-8")).hexdigest(), "files": files}
    replacement = "# BEGIN REVIEWED CATALOGUE PINS\nCATALOGUE_PINS = " + json.dumps(pins, indent=4) + "\n# END REVIEWED CATALOGUE PINS"
    patched, count = re.subn(r"# BEGIN REVIEWED CATALOGUE PINS\n.*?# END REVIEWED CATALOGUE PINS", lambda _: replacement, originals[0], flags=re.S)
    if count != 1:
        raise ValueError("expected exactly one reviewed catalogue pin block")
    for name, owner in (("resources.json", lessons), ("apps.json", apps)):
        digest = hashlib.sha256((owner / name).read_bytes()).hexdigest()
        pattern = re.compile(r'("' + re.escape(name) + r'":\s*")([0-9a-f]{64})(")')
        patched, count = pattern.subn(lambda m: m[1] + digest + m[3], patched)
        if count != 1:
            raise ValueError("expected exactly one manifest pin: " + name)
    changed = patched != originals[0]
    if check and changed:
        raise ValueError("reviewed catalogue or manifest pins differ; review and re-pin both copies")
    if not check and changed:
        # Prepare the complete, identical replacement before the first write.
        # Restore both originals if an OS write fails during the local operation.
        try:
            for path in gates:
                path.write_text(patched, "utf-8")
        except OSError:
            for path, original in zip(gates, originals):
                path.write_text(original, "utf-8")
            raise
    return {"status": "PASS", "mode": "check" if check else "pin", "reviewedFiles": len(files), "originalRowsPreserved": ORIGINAL_ROW_COUNT, "appendedShelfRows": len(SHELF_ROWS), "gateSha256": hashlib.sha256(patched.encode()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lessons", type=Path, required=True)
    parser.add_argument("--apps", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(pin(args.lessons.resolve(), args.apps.resolve(), check=args.check), indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print("[FAIL] " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
