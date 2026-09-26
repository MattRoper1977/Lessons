#!/usr/bin/env python3
"""Retain GLV3 isolation while checking the explicitly reviewed cover additions.

This replaces only the old blanket changed-path assertion. All generated-tree,
GLV3 count, browser, print, contact-sheet and original tamper checks still run.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import types

sys.dont_write_bytecode = True
PROTECTED = ('Art_Teesside', 'GROW_ASDAN', 'LAUNCH_ASDAN', 'Grow/Slideshows',
             'Launch/Slideshows', 'Science_Teesside', 'Humanities_Teesside',
             'Baseline_Weeks', 'BUILD_Estate_v3')
SHELVES = ('Science_Teesside/index.html', 'Humanities_Teesside/index.html')
COVER = 'Humanities_Teesside/David_Cover_Autumn1_W3-W7'
SCIENCE_PACKS = 'Science_Teesside/Teaching_Packs/'
# ORDER "#597, R1, R9, SHELF RECLASSIFICATION" §2 (2026-09-20): the HUM-D5 proofread
# packs land in Humanities_Teesside/Teaching_Packs as ADDITIVE, individually pinned
# pack files (R1). Humanities_Teesside is protected and, before this line, the fence
# had no route for a pack file there: SCIENCE_PACKS admits only its own prefix,
# measured in _passhumd5/R1_GLV3_NO_ROUTE.md (judge() rejected a Humanities pack
# addition even with a pin injected). Same shape as SCIENCE_PACKS and no wider:
# status A only, every file pin-checked against its bytes, the prefix alone admits
# nothing, and an 'M' or 'D' to a landed pack file falls through to the fence.
HUMANITIES_PACKS = 'Humanities_Teesside/Teaching_Packs/'
# ORDER HUM-D5 ADDENDUM 3 v3, signed by Matt Roper 2026-09-22 and landed under his STOP-L1
# tree ruling: the Summer 1 PACK-1R pathway trees. Humanities_Teesside is protected and the
# fence had no route for them -- HUMANITIES_PACKS admits only its own prefix, and a replacement
# member must be an 'M' carrying a beforeGitBlob, which a brand-new file has not got. Same shape
# as HUMANITIES_PACKS and no wider: status 'A' only, every file admitted by its own reviewed
# digest, the prefix alone admits nothing, and a later 'M' or 'D' to a landed file falls through
# to the fence and is rejected. The three prefixes are named, not matched by pattern.
SUMMER1_PATHWAY_TREES = ('Humanities_Teesside/BUILD_W27-W39_2026-27/',
                         'Humanities_Teesside/GROW_W27-W39_2026-27/',
                         'Humanities_Teesside/LAUNCH_W27-W39_2026-27/')
# ORDER SX3-PASSES PASS 4 (3b): the ruling that installs the three Science
# pathway LANDING pages. Science_Teesside is protected, and before this set the
# fence had no route for a brand-new protected navigation page: SHELVES means the
# subject index, a replacement transaction member must be an 'M' carrying a
# beforeGitBlob, and a new file has none. Exactly these three paths, admitted ONLY
# as additions whose bytes equal their CATALOGUE_PINS admission. A later 'M' to one
# of them is NOT admitted here -- it falls through to the existing routes, so
# editing a landing page still needs its own reviewed transaction.
PATHWAY_PARENTS = ('Science_Teesside/Build/START_HERE.html',
                   'Science_Teesside/Grow/START_HERE.html',
                   'Science_Teesside/Launch/START_HERE.html')
# RULING LAND-A2 R3 §1 and R4 (Claude, 25 September 2026): the 21 Autumn 2 Science lessons land in
# their own dated term folders. Science_Teesside is protected and the fence had no route for a brand-new
# lesson file there -- SCIENCE_PACKS admits only Teaching_Packs/, a replacement member must be an 'M'
# carrying a beforeGitBlob, and PATHWAY_PARENTS names three pages. Same shape as SUMMER1_PATHWAY_TREES
# and no wider: status 'A' only, every file admitted by its own reviewed digest in CATALOGUE_PINS, the
# prefix alone admits nothing, and a later 'M' or 'D' to a landed file falls through to the fence and is
# rejected. The three prefixes are named, not matched by pattern.
LAND_A2_SCIENCE_TERMS = ('Science_Teesside/Build/Autumn_2_2026-27/',
                         'Science_Teesside/Grow/Autumn_2_2026-27/',
                         'Science_Teesside/Launch/Autumn_2_2026-27/')
SOURCE = 'tools/humanities_resources/SOURCE_MANIFEST.json'
DOWNLOADS = 'tools/humanities_resources/DOWNLOAD_MANIFEST.json'
LABEL_EDITS = 'tools/humanities_resources/PUBLIC_LABEL_CHANGES.json'
BOUND_INPUTS = (SOURCE, DOWNLOADS, LABEL_EDITS, 'tools/humanities_resources/CONTENT.json',
                'tools/humanities_resources/ORIGINAL_MEMBER_MANIFEST.json',
                'tools/humanities_resources/build_resources.py',
                'tools/humanities_resources/check_resources.py',
                'tools/humanities_resources/resource.css',
                'tools/humanities_resources/resource.js')


# EDU-Q1: exactly the reviewed Sugar HTML and six existing companions.
# This is a replacement transaction, never a directory-wide permission.
SUGAR_REVIEW_BASE = '11bba1875e27016547186754ed65752152e27c9b'
SUGAR_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html': {'beforeGitBlob': 'bd1d6da15f32efc7ce068e9f4e846bb7038bb80a', 'afterSha256': '8594f15916211ff3de03bb928b2de3756bff0dbe8c52adabd3e4cccfda9d42a3', 'bytes': 628443}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pdf': {'beforeGitBlob': 'abd9261ff123775b2af979761d08dbe1ea5e2662', 'afterSha256': 'fc9ba726c94177000d872c28e3c7db3812c268d6552e936a316c38654a95a0dd', 'bytes': 431296}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pptx': {'beforeGitBlob': 'aff41a6c51c8eb21fbce611316590ed255be7078', 'afterSha256': 'd93b814710bcf57ece951ba0aaf82ed41320247571ec48147e26a5423b3c07e3', 'bytes': 158524}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.docx': {'beforeGitBlob': '81015f010d39c157bdd7f5c3f453ad2e6912c11e', 'afterSha256': 'be71bc9be6c6d9c23383ee35ec739df80830ad5e336e7095098deaf3003a6d64', 'bytes': 42521}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.pdf': {'beforeGitBlob': 'a1e81df065fe01d01d0eda19549ec33883bc1a27', 'afterSha256': '25544b193963f552a1511ac17bd5b5353cbeeca71d6788ac4deddbc61f905dc4', 'bytes': 170636}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.docx': {'beforeGitBlob': 'b111d7326d3bcad325167f2357b7f3741917dad1', 'afterSha256': '033a59447d5b42ea990dd0737c93db99a717e9055307f1c6b6ebe5bf7262c9b3', 'bytes': 43099}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.pdf': {'beforeGitBlob': '3fd844034e225e1c404a5cb50985951a0b4406ec', 'afterSha256': 'a4f9888e6b742339d54ba9128da824904b65e786054e8820d60df9980fa4af86', 'bytes': 114441}}

# Further reviewed replacement transactions are declared here by their own
# admission tools (tools/grow_resources/admit_w3_friction.py, tools/rw1/admit_w8.py),
# each as an exact per-file map; never a directory-wide permission.
# CX2 S3 (Matt's ruling, 15 September 2026): the pack hub names the offline companion
# set as a lightweight offline edition and links each entry to its canonical lesson,
# written by tools/science_teaching_packs/cx2_s3_offline_edition.py.
CX2_S3_REVIEW_BASE = '5778ede06902e7a218459452ae79e3ce330db693'
# EDU-Q1 GROW W3 Friction: the paired lesson and its two resource pages,
# written by tools/grow_resources/admit_w3_friction.py.
GROW_W3_REVIEW_BASE = '929cf731173aeca8c9941cecd76cb350387499d1'
# CX2 §3: the LAUNCH W4L1 Diffusion lesson with its native pack files and pack
# records, one transaction, written by tools/launch_resources/admit_w4l1.py.
CX2_W4L1_REVIEW_BASE = 'acae624f34ab4b2a88903cb6ea528976b5a1e210'
# CX2 4.8: the accepted Sugar lesson's staff card without a product name (R10), the
# re-rendered teacher document and the refreshed BUILD checksum rows, written by
# tools/science_teaching_packs/cx2_sugar_r10.py.
SUGAR_R10_REVIEW_BASE = 'a8b3c9689d9b1d74e56a70f065773bf3942b63c9'
# CX2 §8.3 Lane D: the return-week W8 lessons, one transaction per pathway,
# written by tools/rw1/admit_w8.py.
RW_W8_REVIEW_BASE = 'ec7d34ab48eb290f9abb67b27c735b6e09b9930c'
# D-1: the BUILD W8A Sugar Evidence lesson re-dressed on the classroom chassis and the
# pack checksum file that names it, one transaction, written by
# tools/build_resources/admit_w8a_chassis.py.
BUILD_W8A_CHASSIS_REVIEW_BASE = '48c2ecb9ab19f238cdbe5443196935a5c45f375b'
# SX3 · SX3 LAUNCH W12-W15 A2W7: this branch's landing decks, re-dressed on the pathway exemplar
# SX3 · SX3 LAUNCH W8-W13: this branch's landing decks, re-dressed on the pathway exemplar
# SX3 · SX3 GROW W9-W13: this branch's landing decks, re-dressed on the pathway exemplar
# SX3 · SX3 BUILD W12: this branch's landing decks, re-dressed on the pathway exemplar
# chassis, one transaction, derived and written by
# tools/build_resources/admit_sx3_release.py. Every member also carries a
# CATALOGUE_PINS admission, which replacement_errors cross-checks.
#
# REVIEW: S2 signed — Matt Roper, 2026-09-18
# This transaction is a review decision, not a derivation. It exists because
# the owner accepted the SX3 re-acceptance pack — the 31-row table, the title
# list and the transaction listing — at STOP-S2. The members are derived; the
# decision to admit them is the line above.
SX3_LAUNCH_W12_W15_A2W7_REVIEW_BASE = '55bff167946ecefa20eaab9d2064768549df351f'
SX3_LAUNCH_W8_W13_REVIEW_BASE = '55bff167946ecefa20eaab9d2064768549df351f'
SX3_GROW_W9_W13_REVIEW_BASE = '55bff167946ecefa20eaab9d2064768549df351f'
SX3_BUILD_W12_REVIEW_BASE = '55bff167946ecefa20eaab9d2064768549df351f'
# SX3 · SX3-FU1 F2 LAUNCH W9-W11: this branch's landing decks, re-dressed on the pathway exemplar
# chassis, one transaction, derived and written by
# tools/build_resources/admit_sx3_release.py. Every member also carries a
# CATALOGUE_PINS admission, which replacement_errors cross-checks.
# REVIEW: Reviewed by Matt Roper 2026-09-20 (STOP-S, Order FINISH-2): SX3-FU1 F2 LAUNCH W9-W11 (9 members)
#          and W12-W15 A2W7 (11 members) — arrival stage split, no visible content lost, rows 1–42 re-meas
#         ured; published digests admitted; carrier pin moved.
SX3_FU1_F2_LAUNCH_W9_W11_REVIEW_BASE = '6bb8238f145e0d9cdef84f7142ed72a24f6f13d8'
# SX3 · SX3-FU1 F2 LAUNCH W12-W15 A2W7: this branch's landing decks, re-dressed on the pathway exemplar
# chassis, one transaction, derived and written by
# tools/build_resources/admit_sx3_release.py. Every member also carries a
# CATALOGUE_PINS admission, which replacement_errors cross-checks.
# REVIEW: Reviewed by Matt Roper 2026-09-20 (STOP-S, Order FINISH-2): SX3-FU1 F2 LAUNCH W9-W11 (9 members)
#          and W12-W15 A2W7 (11 members) — arrival stage split, no visible content lost, rows 1–42 re-meas
#         ured; published digests admitted; carrier pin moved.
SX3_FU1_F2_LAUNCH_W12_W15_A2W7_REVIEW_BASE = '8fe3702cf9f3cb292c3e9585bbb7a23b203dbefb'
# ORDER HUM-T · HUM-T batch 1 BUILD: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_1_BUILD_REVIEW_BASE = '96452dadb2b87d02c72bd40865b269f7605f6821'
# ORDER HUM-T · HUM-T batch 2 GROW: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_2_GROW_REVIEW_BASE = '26b5866442beac811ade8ca8e01171f8d1f66e8d'
# ORDER HUM-T · HUM-T batch 3 LAUNCH: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_3_LAUNCH_REVIEW_BASE = '1766ea0520aacf7a5cc1118783090c76f45686db'
# ORDER HUM-T · HUM-T batch 4 GROW: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_4_GROW_REVIEW_BASE = 'ae32def62c33de971511ff966284958812d6e2fa'
# ORDER HUM-T · HUM-T batch 5 LAUNCH: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_5_LAUNCH_REVIEW_BASE = 'b79fa079b93eb6371fa7bc2759f8ccb4b8228e62'
# ORDER HUM-T · HUM-T batch 6 BUILD: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_6_BUILD_REVIEW_BASE = '0fc3839a2c61c86e8c40f8017e7fdd4e5e1e542f'
# ORDER HUM-T · HUM-T batch 6b BUILD: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
HUM_T_BATCH_6B_BUILD_REVIEW_BASE = '13b602e7ff7ea6327fc806ce3f23b022ef6c45c0'
# ORDER HUM-T · ADDENDUM 3 v3 explicit tags: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
ADDENDUM_3_V3_EXPLICIT_TAGS_REVIEW_BASE = '6818dd9f2ec25b0fed1d4dca80d6f67180f066f6'
# ORDER HUM-T · Summer 1 responsive re-delivery: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
SUMMER_1_RESPONSIVE_RE_DELIVERY_REVIEW_BASE = 'cbc61aca58804b61e5481121fed216d1fb772664'
# ORDER HUM-T · PASS C Autumn 2 batch 1: this batch's transplanted decks, each stage carrying the
# science exemplar's loop panel. One transaction, derived and written by
# tools/hum/admit_transaction.py. Every member also carries a CATALOGUE_PINS
# admission, which replacement_errors cross-checks.
PASS_C_AUTUMN_2_BATCH_1_REVIEW_BASE = '9f8716f2bb4beeed689580869b0cc89dc828e527'
# RULING LAND-A2 R8 §2 · DLG-1: each control given the audience of the dialog it opens,
# by tools/hum/fix_dialog_audience.py under tools/hum/DLG1_PAIRS.json, and the pack
# manifests re-cut for exactly those pages. One transaction, derived and written by
# tools/hum/admit_transaction.py --limb dlg-1; every member also carries a CATALOGUE_PINS
# admission, and LIMB_JUDGED_TRANSACTIONS has the boundary re-judge every member.
DLG_1_REVIEW_BASE = 'c527b7c14a508f167df5746cc4d9b32ea1f6f60d'
# BEGIN DECLARED TRANSACTIONS
# BEGIN S3 OFFLINE EDITION REPLACEMENTS
CX2_S3_REPLACEMENTS = {'Science_Teesside/Teaching_Packs/web-slides.html': {'beforeGitBlob': '6596d65c7a9bd5bb1875c5b46bbc331df8652144', 'afterSha256': 'f31f09d03f5d8c417af1745b38309fa537afb8bb4c6a08f387db3349d9e1cba2', 'bytes': 18607}}
# END S3 OFFLINE EDITION REPLACEMENTS
# BEGIN GROW W3 REPLACEMENTS
GROW_W3_REPLACEMENTS = {'Science_Teesside/Grow/SCI_G_W3_Friction.html': {'beforeGitBlob': '472809373600a6f8529ccb59faa05939cd4de58a', 'afterSha256': '508f1967b6481671dafb149d7177b620b194074312cee0dbdd30553c166b634a', 'bytes': 414467}, 'Science_Teesside/Grow/resources/GS_W3A.html': {'beforeGitBlob': '7be51ce3f70cfb8b6cdfea586d1ab3a34f85d577', 'afterSha256': 'e5bfaf2bc70912aeb59fe9a2eb1032d86c7a473a1059ba782fee1be7b3513dc1', 'bytes': 8345}, 'Science_Teesside/Grow/resources/GS_W3B.html': {'beforeGitBlob': 'a8cd838436ead513a47449c0ec5c264153835c72', 'afterSha256': 'fb6580bfd1e02d82627d60e1c2e08c3a34b227d0cbe760545502a8e51ab91208', 'bytes': 9105}, 'Science_Teesside/Teaching_Packs/GROW/DOWNLOAD_INDEX.json': {'beforeGitBlob': '15be31339565a36e14b231ea7ee92f72e3de2044', 'afterSha256': 'f4838737eba7f6db77bf5d8741cdaf046a21d15159da70cbc550030824cddd63', 'bytes': 55385}, 'Science_Teesside/Teaching_Packs/GROW/SHA256SUMS.txt': {'beforeGitBlob': '50b80da129c8715b6bb42c50c26f0300e47340e1', 'afterSha256': '758dcbdd646219106ef7c416034c24e5e89da1423df5393621eef985e0c4a3a1', 'bytes': 41955}, 'Science_Teesside/Teaching_Packs/GROW/SOURCE_MANIFEST.json': {'beforeGitBlob': '9991c027829d89569b88fc71ee895f82bd275748', 'afterSha256': '78b1d12b1b817c05a5743688a0946b855a8c211c954d7b29ba41575a2e2f7156', 'bytes': 31944}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_DOCX_Collection.zip': {'beforeGitBlob': 'a809670f0f3bfece5943f01d7685957915891c27', 'afterSha256': '2482706e4f9c7e192287acfd02e7c09381597a1a9fc772c9d39fe630eba5a3aa', 'bytes': 934810}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_PDF_Collection.zip': {'beforeGitBlob': '695654bf6d71a68bf529f828df8140b7b551f6c9', 'afterSha256': 'b3116412bb38368b96c0236e2b41902deb76e96461f1ca1c3fb134d878f842f0', 'bytes': 4897326}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_PPTX_Collection.zip': {'beforeGitBlob': '9acea60c01a9bcd69998aa0e26ba8aaa83c4bb53', 'afterSha256': '592f59c2ccae4f9531af5296eb30064c8fee92c44ba2b896db8038cf2a93dce8', 'bytes': 11610595}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3A.zip': {'beforeGitBlob': 'b640797c2be2729b1d6f70c7f9b3f85083ee0d28', 'afterSha256': '2596818e45a67ea1b306f7c9287fa70795ab8142c6c93b9e63e1f99e1a4e5b22', 'bytes': 3047141}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3B.zip': {'beforeGitBlob': 'fbc60fd5f192deeaf7f2086bd04630cf9ab4d669', 'afterSha256': '4fedd9c4a162c3e712a327afd85554b19c55ad1f5b8cacea057b0fdecbb305ed', 'bytes': 2887914}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week3.zip': {'beforeGitBlob': 'ac91b2d4ef3a2623584b12d4d4fdb58e299a615c', 'afterSha256': '5a8606a41a4b9e5a7accdf3ee730d727b709d92734f669d07a1e84324fa8035b', 'bytes': 5628922}, 'Science_Teesside/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Weeks3-7_Teaching_Pack.zip': {'beforeGitBlob': '9a2ee88e2a3b3ebc1f83b7d85c2bef742c4398e4', 'afterSha256': 'd8b6f0ce61e7925089aadbc66b63756316268c9c2934575ccdf18e74cb41e6ce', 'bytes': 17481035}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pdf': {'beforeGitBlob': '448f78231000d204c3da1e26921a677a929d4b83', 'afterSha256': '0e57d93e45bf29236754a735e42f6d2ae923aa1a23c65ebe9ed19041347ced7d', 'bytes': 342104}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pptx': {'beforeGitBlob': '7ad84a84ba5d20e6da8a5677d684a206f94cf9ce', 'afterSha256': '13dceb4a32f65165df9353349a69c87465e7f33b9f941036f8f714fd10a9f9da', 'bytes': 2038042}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx': {'beforeGitBlob': '9b06c7bcb266853c3eb9fce55667b5799ed3222a', 'afterSha256': '9f8afdf8df90eb845d3ea352d36b9bd19dd192a6c040883fe70957eb8be487de', 'bytes': 58755}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf': {'beforeGitBlob': '97b9364c72863f6efc262ad1d50828deeb5687b3', 'afterSha256': '856691efece9acaae40a529f949f3d26567345c8f658de9e26eab1bbbdc585cb', 'bytes': 249351}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx': {'beforeGitBlob': '8a37234fb19d83349f6d311daa261ed0fc35b1b6', 'afterSha256': '9da8a692bd1ad6b4a040e4b4a970275c90577cbaf73342492d1908148c5d8717', 'bytes': 47511}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf': {'beforeGitBlob': '46caf3569c44878a024acb7fe4694c4a6eeaac44', 'afterSha256': '08c926202671c6b2c25778d5d2dcf2f99a473dd704201f0ef9a58e3a359b18f9', 'bytes': 217509}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3A/START_HERE.txt': {'beforeGitBlob': 'c4f568f594b12fd1ad55204e9192a3824119c57b', 'afterSha256': 'b5c46c92125be91cb86f64c5969ad8378ab3948b41a82e7be01e7378ccdfc81c', 'bytes': 838}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pdf': {'beforeGitBlob': 'be31fba447c41634bbac03a61a388924895072a4', 'afterSha256': '1ce1ba083eb62b521368b3c5863c098733ae7d677a1e7c0e641b8e0fd7681d3a', 'bytes': 320920}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pptx': {'beforeGitBlob': '778ea423b30e885e32add933dc789cfd39e75271', 'afterSha256': '3049816d76009ebe3ad1b609e9ca22ec54c3abc82d3e8037b012386759ba278b', 'bytes': 2027282}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.docx': {'beforeGitBlob': '80053558ef4bde01454927512a375ca7944a016b', 'afterSha256': 'e4333309ef2e2dcf587385063c8e43eee56c3a285089b4f749580124d8c128ea', 'bytes': 41418}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.pdf': {'beforeGitBlob': '92123f2f8a5bf90f750e4102410148da821f307e', 'afterSha256': '7ddb70eb886f743fd0813b5d581435b36bdfb1a5813e23a6cb6f3b95ccdfee8b', 'bytes': 127894}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.docx': {'beforeGitBlob': '0279a5cee651b1d4e173b605e38124a5936dbfc3', 'afterSha256': 'c0e2ae5adaff89fa05b28e389f7d422e0f638ca9edd33313da61d57d258732cb', 'bytes': 43338}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.pdf': {'beforeGitBlob': 'f6628955910b4beb057263eafe1dd4849aa86131', 'afterSha256': 'c9c7bf0a6dc4b4a69c1df89bf7fc3a2fdd73c57828ecb0619688611b52a61d5d', 'bytes': 147273}, 'Science_Teesside/Teaching_Packs/GROW/lessons/W3B/START_HERE.txt': {'beforeGitBlob': '473e2fe98c17f732f9507405c26ae7e560c5639f', 'afterSha256': '70a87773d7f0bc53b67cc1023263f2837ec473ceffc6ec1fc79b82823805c756', 'bytes': 665}, 'Science_Teesside/Teaching_Packs/index.html': {'beforeGitBlob': '0e8cab0cb461779787e6fef503788c3b38bd51f3', 'afterSha256': '33f5021dbb05a35048447a3b79f144f265e3dd8209a8bbd96a916b3fd8b7fc81', 'bytes': 73131}}
# END GROW W3 REPLACEMENTS
# BEGIN DIFFUSION W4L1 REPLACEMENTS
CX2_W4L1_REPLACEMENTS = {'Science_Teesside/Launch/SCI_L_W4_L1_Diffusion.html': {'beforeGitBlob': 'ffede52e9ef7807c958b6cc3fa683c22881739fc', 'afterSha256': '563e0bddc7049afb1dfc7245b1810da5094c19bca8027a08bbaf4c26d5a0dc54', 'bytes': 258861}, 'Science_Teesside/Teaching_Packs/LAUNCH/DOWNLOAD_INDEX.json': {'beforeGitBlob': '0b77a45d80c4750bcff19987cc58304ed54b8d5b', 'afterSha256': '431b8d5b10c4b037d09553a5f6818681c4a2f56fbf7beed4dbcd687bdefe90fc', 'bytes': 67939}, 'Science_Teesside/Teaching_Packs/LAUNCH/Pupil_Worksheets.pdf': {'beforeGitBlob': '5c1d69c7794e32f826c05c8f425bba7fe81a40da', 'afterSha256': '40b4561e417afebf2cae6a5eae1ade45859a9dd462bf69e8dd4135c836d3f7bc', 'bytes': 1166667}, 'Science_Teesside/Teaching_Packs/LAUNCH/SHA256SUMS.txt': {'beforeGitBlob': '02126fc72d678cd9fdd047e817cbb3c4e1a1e200', 'afterSha256': 'cbb0aa2c07320596ce8118df19526c158e952a7c6b730fcd4492dc57b7052586', 'bytes': 48875}, 'Science_Teesside/Teaching_Packs/LAUNCH/SOURCE_MANIFEST.json': {'beforeGitBlob': '8ddbefaa231cce6ec0b0a7a4ee0ff38e392e4712', 'afterSha256': '3ec0db25c3deb4839106d59bb03361e05d103e7347a6f2939ff3f4cbb9de7655', 'bytes': 66484}, 'Science_Teesside/Teaching_Packs/LAUNCH/Teacher_Guide_And_Answers.docx': {'beforeGitBlob': '91e86a6f1dc190e1330799781a183a55a8c66142', 'afterSha256': '407a1c8c72112dded2dc9c89d3a73c6b5834cabcb743d8bd6f436c412ef1656e', 'bytes': 56298}, 'Science_Teesside/Teaching_Packs/LAUNCH/Teacher_Guide_And_Answers.pdf': {'beforeGitBlob': 'fd77601dfdb10b42065a3df6bb6c535c6e66b830', 'afterSha256': 'f359887eabd99b868f1741b65ddc0a16b0eb2d5909d127f166926aa877657fb2', 'bytes': 186724}, 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Diffusion.pdf': {'beforeGitBlob': 'a3582730c28ec7cf534ef26f134eea2da4af5f69', 'afterSha256': '0641dbde7d35b8d98332c864eb419b7f0d18610b79e96c2439c5cd741803f6ec', 'bytes': 541386}, 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Diffusion.pptx': {'beforeGitBlob': '66678b119af17a6ef53fba95be0c5f55a957a233', 'afterSha256': 'a61a92cb908959617c5e62440bdf18c8fce41a5a5c91eb348086d4fc687b32fe', 'bytes': 373772}, 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Worksheet.docx': {'beforeGitBlob': 'af2c305007cc6dbe68d751fe8a3adf37609a617d', 'afterSha256': '587d0c554d8f496b13bfa4f35cd91e4fc6e5e9618059b73cf2a5a9131e2ada75', 'bytes': 42551}, 'Science_Teesside/Teaching_Packs/LAUNCH/Week_4/W4L1_Worksheet.pdf': {'beforeGitBlob': '849ff8cb81a96a17fb6b51c4f7db672a15db6b73', 'afterSha256': '9ce702ccc29bfb3eecf02e6f73df2de5cb96a6e695962e79fb49c8ea90ce414e', 'bytes': 92831}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_Complete_Pack.zip': {'beforeGitBlob': '5d53b0e0a8f3f2ebc510bf623a21af8ae4eef9d1', 'afterSha256': 'a1194521ca6943909d8cb73c61dbf6d6bd5e1a5bd704d640ef7dd9f8b3df0e7e', 'bytes': 25818458}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_DOCX_Collection.zip': {'beforeGitBlob': 'dd5482570315df85ebb316a10fd68ef851003c96', 'afterSha256': '638527b335f4062db3da9d6172da4ec9993ea007d3e4dc8a507d122f2e358baa', 'bytes': 1339971}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_PDF_Collection.zip': {'beforeGitBlob': '484eb48c0e83df0a901f27c4d81f69bde9c6bed1', 'afterSha256': '8a0d4e26223491be1998e21fe25995bf50bd807d5ba3fce6eb73aa657b8771d7', 'bytes': 16937043}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_PPTX_Collection.zip': {'beforeGitBlob': '795996873b8fd35c8c859e4b9afad15aeeb639d7', 'afterSha256': '6d410f6066f65c30550717b1180bd2b7410767ee62e13406927d1b8d41107bc9', 'bytes': 7531106}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3L1_Lesson_Pack.zip': {'beforeGitBlob': 'af1378260d3759a832d61fbcb388a3dd8eb54b7a', 'afterSha256': 'a72792b9c2b10eb660850f17765b6b723f68ff8cc95e6be1f830ba64232803e3', 'bytes': 5480855}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3L2_Lesson_Pack.zip': {'beforeGitBlob': 'fa7cd17883e6c6ef72b8ef873acf485116d938f8', 'afterSha256': '0e6d454ab2437aa39b8d1c8409c6300822d87df038fba3e168d1d51fb122f446', 'bytes': 3668656}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3L3_Lesson_Pack.zip': {'beforeGitBlob': '409f45d70178daef9d977d63f757575af22c9c22', 'afterSha256': '2c10aca9832f12889edfd8923f80c8660596d67fe1e81b4ee40122f2c4ff66e4', 'bytes': 3794170}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3_Teaching_Pack.zip': {'beforeGitBlob': 'a35144082b524fbf63e7b2a86800b0748f14a73b', 'afterSha256': '8e6c80015fc3c45585ebb7add1cb99dfeed48c4daccd05dc0d96486719e97abb', 'bytes': 8086642}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4L1_Lesson_Pack.zip': {'beforeGitBlob': '0d04a5a8e723160dfc9121e609a75ac156f06750', 'afterSha256': '5f0985a04ccfdbcbaebc6d31773a04caa55ea9ba8b3b7caefd6c01f4929f5d76', 'bytes': 3539294}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4L2_Lesson_Pack.zip': {'beforeGitBlob': 'ed0bce8927b548c3d4c24794eea029c854858a89', 'afterSha256': 'a426dc9b51d4345db06a6ec9681bee9a51591950416b4d4c823715eaf2515ec7', 'bytes': 3793325}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4L3_Lesson_Pack.zip': {'beforeGitBlob': '7266c260950ad8f25839f7d90f683f6c3b1e09e7', 'afterSha256': '74caa4b61be0c043de6312d0a9abbb688356c8826073f7793cab82a70cbde62a', 'bytes': 3765932}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4_Teaching_Pack.zip': {'beforeGitBlob': 'edebe7b5c486e21ae56fb491171678aeeca6bdde', 'afterSha256': 'eb29b571f83605f35ca8f287acbd30498e595c86a99e69a0c7101dd804f8ca6d', 'bytes': 6236510}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5L1_Lesson_Pack.zip': {'beforeGitBlob': '7b9a5fa517ae49f9d61954964c309341ff4d0c9f', 'afterSha256': 'ae830ca4d6d07af91c80e406416665014dcecc86c9e27d5c8ffcade94d3522aa', 'bytes': 3784403}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5L2_Lesson_Pack.zip': {'beforeGitBlob': '463f6cb5bbffde09cb2a5ccb8bf026ebf9de9e9c', 'afterSha256': 'ac6a50b5f79420d90545cc07b43eddb1caa0085f7eea966f958de80b2523f0da', 'bytes': 3855226}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5L3_Lesson_Pack.zip': {'beforeGitBlob': '4d749fec640dc92e75d95ece9cc6aa367d328935', 'afterSha256': '4f632511bc0565ae70452d117ec6181b1bff401607464293af1ac17ba9cae014', 'bytes': 3848255}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5_Teaching_Pack.zip': {'beforeGitBlob': '2bd38e96a5787c56572864b87439cbb1200b1a7b', 'afterSha256': '798f62805181e146d2e65bd19cb2a497154745d948b1fa1168b614def7b9d8ae', 'bytes': 6679909}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6L1_Lesson_Pack.zip': {'beforeGitBlob': '1916ac209a704de2e68843d1b809999a1fd376fe', 'afterSha256': '5590e2f273994a9f3003d80dbe41f0e18e1b6a186767ce514a2806f3345ca26b', 'bytes': 3840153}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6L2_Lesson_Pack.zip': {'beforeGitBlob': '482e1b8238216d8093c565a21d1f0def6f5bbc11', 'afterSha256': 'a1d47be6ae8f026788ca6106b63aa03242561f7ca4e0b19f91e7cab2af510648', 'bytes': 3752681}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6L3_Lesson_Pack.zip': {'beforeGitBlob': '919ee3ae46fdee8d76e9a8de6805b7145dba62cd', 'afterSha256': '87bc34837a81123d3b992d1b366ad00236ac0d4e23fe2da0f434e79aafa814fc', 'bytes': 3914147}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6_Teaching_Pack.zip': {'beforeGitBlob': '06f75f22c2297787eb1371eb340cabee7f915606', 'afterSha256': 'e86f79ae921379d4e91418f520be95fa45daf94eb4f60b00502f786c82451128', 'bytes': 6638529}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7L1_Lesson_Pack.zip': {'beforeGitBlob': 'cc66828f3c25c61ddb9a3be754cf93d9e98f2fc7', 'afterSha256': '338c05412e504ac6a1c1ca9e7f31e93a00ca3b7bc163b4f9a2da497d12749908', 'bytes': 3904279}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7L2_Lesson_Pack.zip': {'beforeGitBlob': '50764c1536f66a7377467fec795aa070d4f355b4', 'afterSha256': '64f412f903d741cdee73025a8f0c852ee68efb8fad6de7a04ad54a9b69479f66', 'bytes': 3845538}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7L3_Lesson_Pack.zip': {'beforeGitBlob': '80f41295cc455a115a9a90f92f3671c9ce009c62', 'afterSha256': 'b5c3cd9041ad61a754d0f8896d52e1c2bf580f1ca60c876aa845798e16bfdc3e', 'bytes': 3882356}, 'Science_Teesside/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7_Teaching_Pack.zip': {'beforeGitBlob': 'aba5a3058262ae7c2bc76e66bd66f2f1bb12160d', 'afterSha256': '509df11b11bca9e59f8a74a53bc149edf64caa02110074b6d1f654ca3dae74fb', 'bytes': 6661536}, 'Science_Teesside/Teaching_Packs/index.html': {'beforeGitBlob': 'dd97fe66eeba0b971ea9c3efdd7f06c89d233415', 'afterSha256': '4d9fc732a9b9d086b59881300a081a0f3fc2627bc8cd083b680fade75883caf8', 'bytes': 73130}}
# END DIFFUSION W4L1 REPLACEMENTS
# BEGIN SUGAR R10 HYGIENE REPLACEMENTS
SUGAR_R10_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html': {'beforeGitBlob': 'ce67f2e573a849f528332657c3274ea5d23ae3b8', 'afterSha256': '9f08cc72aadc12b2480ea8c1104e0118c7335ce087446308d39336c79379e96f', 'bytes': 628527}, 'Science_Teesside/Teaching_Packs/BUILD/SHA256SUMS.txt': {'beforeGitBlob': '74bcf89dd21aae3c14d03871a6cf7249dc1fd91b', 'afterSha256': '316444eaaa55fd786c393a40443f511b450c0f04a5ba1f752cef125fd254be01', 'bytes': 43722}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.docx': {'beforeGitBlob': '0218f8fdc5ec18d88ff784bbeaca4221e3610707', 'afterSha256': '7932493b683f1ac4ab7fbaabef8f55ec13e0db311dc63334788dc88e9fc5d099', 'bytes': 43120}, 'Science_Teesside/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.pdf': {'beforeGitBlob': '8c48364a5c100fbd2a4d2f44d0b2e34e8d36894e', 'afterSha256': '8c9984c7683196b03a8acdf90764d7136f390f4fb0e28211077eb4184311f5a5', 'bytes': 94156}}
# END SUGAR R10 HYGIENE REPLACEMENTS
# BEGIN RETURN WEEK W8 BUILD REPLACEMENTS
RW_W8_BUILD_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html': {'beforeGitBlob': 'f5ca0a4ef3334d13d377d866ef37e3c7c55a9c0d', 'afterSha256': '7b27a0d82cd7df671c6a3b52b46d5d620ed678c332cdc58d1c649c3b29dacbac', 'bytes': 317400}}
# END RETURN WEEK W8 BUILD REPLACEMENTS
# BEGIN RETURN WEEK W8 GROW REPLACEMENTS
RW_W8_GROW_REPLACEMENTS = {'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html': {'beforeGitBlob': 'ef8195bba4529ba1b9698f0db5cec507f7433aff', 'afterSha256': '2560984b05d13f2e998c7ae00cabf414b313821b836d6d68299774da55db8928', 'bytes': 291226}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html': {'beforeGitBlob': 'a7f2e7437f4fdfad0a397b7ad323b54128eefa23', 'afterSha256': '97ef11162a1c36b1df421d0f85ab32be6139bfbd47ee36314426020a1162a32b', 'bytes': 284158}}
# END RETURN WEEK W8 GROW REPLACEMENTS
# BEGIN RETURN WEEK W8 LAUNCH REPLACEMENTS
RW_W8_LAUNCH_REPLACEMENTS = {'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html': {'beforeGitBlob': 'e92efe5671f2e89f4e9fd0eda10013e6124cd878', 'afterSha256': '1e46f94da927f5bbf190c067ea84b16cd60d0112c6381bd17de07c774fabd346', 'bytes': 293788}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html': {'beforeGitBlob': '96adc448f37fcb0b6eed5f79c9cebad4da41a25e', 'afterSha256': 'd69088d64598a8f230603a9af232f3055dab3796330e30c19566dd087f5f52f6', 'bytes': 289583}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html': {'beforeGitBlob': '7a2efdef9cd54395af81e4a993e305d1cae5651f', 'afterSha256': '81e67475c5a727e1fae1806504b56a0f49b15f9573be563cb6c55cc4e381dfda', 'bytes': 301824}}
# END RETURN WEEK W8 LAUNCH REPLACEMENTS
# BEGIN BUILD W8A CHASSIS REPLACEMENTS
BUILD_W8A_CHASSIS_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html': {'beforeGitBlob': '1035792c9d9a95865d16b7e829d9704014a53e42', 'afterSha256': '74d17d4e0f6873f094691daa753539f8a351887160beea6a8a8d727bba864d2d', 'bytes': 639630}, 'Science_Teesside/Build/W8-W13_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'ce5a5c862dfe85cae88ad3a186f7ebef393f8234', 'afterSha256': 'e00a7819a77039be3ab614ba92de09889748723aa9ad759f7a6bfe64c2e5fb28', 'bytes': 1905}}
# END BUILD W8A CHASSIS REPLACEMENTS
# BEGIN SX3_LAUNCH_W12_W15_A2W7 REPLACEMENTS
SX3_LAUNCH_W12_W15_A2W7_REPLACEMENTS = {'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html': {'beforeGitBlob': 'e157eaf36349d1435be825badd1c0e7dae5926b4', 'afterSha256': '5032cd225d7202573c556a371ca554889b9df3a43534757621474bbaf9653dbe', 'bytes': 622533}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html': {'beforeGitBlob': 'e45a65cd3351b1f2497bd775829abf0921b987ea', 'afterSha256': 'a6904e5055e43c1d7e61351f13602670c7ddf1d053b882c66a37f792823014f1', 'bytes': 623614}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html': {'beforeGitBlob': '258fa3934cab6f7dcb78600956e44047db4370a9', 'afterSha256': '938d8894fbb06368717264a59fc0b97830272770dc50caf9941d8d77470fd389', 'bytes': 354327}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L1_Genetic_Condition_Research_Introduce.html': {'beforeGitBlob': '46571781c85215414c948bb617e1623f977a9f30', 'afterSha256': '501a2e9d1d8b3af42ce872e0812a68f18a6103ebeea6395652c911ad80d7a999', 'bytes': 623737}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L2_Genetic_Condition_Source_Evidence_Explore.html': {'beforeGitBlob': 'bd6c3dc9cd5855b0ad89c2e5455cb1e8952ee542', 'afterSha256': 'b0b03f10e6991660d820582a520ca2698c9010916db66bf592243c9a64639b0e', 'bytes': 625263}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L3_Genetic_Condition_Presentation_Do.html': {'beforeGitBlob': 'fbd780abae1f0fe4edb0458991ffff8695ff732d', 'afterSha256': '46f816f7ea9a3101c874f07c000322a944a165cbff42ebf5f658bffc143727b8', 'bytes': 625643}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L3_Inheritance_Probability_Do.html': {'beforeGitBlob': 'adc86a1bd75c807f4816c4268021cf29d07a52ea', 'afterSha256': 'a48127f498d131f0fafe9661fa47a788e2887cc96d3c7b275999ef712a85dd22', 'bytes': 567264}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html': {'beforeGitBlob': '10058b326cb5aa04cbf570bb0691c45b48053e0d', 'afterSha256': '72af021ab2aa1d8c7f6ea5573993623e85c9dd2aa2a31c26b19162a1ced6b3c6', 'bytes': 654865}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html': {'beforeGitBlob': '44ae55043d80964410d6323dd8f88427217fb98e', 'afterSha256': 'c2e4a7aeffe0738949c7372e230f8107b37b6f82705a5a412f604514fabcbc50', 'bytes': 672345}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L3_Identical_Daughter_Cells_Do.html': {'beforeGitBlob': 'ae08526b50e4352364cf97b95852ddbc295356aa', 'afterSha256': '588a6fdeac00afa6976357ff06ae86b47d600df570eec5b7a5fdb4d6983b5c11', 'bytes': 658289}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9_Copy_separate_divide_Classic.html': {'beforeGitBlob': '20fcb0ed3989a7ea5f2d4b95f2234e209a7f0bf9', 'afterSha256': '649a152c0fd4a768496f55de23add747acb75dcad4e73a30bfe9453e0d6bcc8d', 'bytes': 656870}}
# END SX3_LAUNCH_W12_W15_A2W7 REPLACEMENTS
# BEGIN SX3_LAUNCH_W8_W13 REPLACEMENTS
SX3_LAUNCH_W8_W13_REPLACEMENTS = {'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L1_Growth_And_Differentiation_Introduce.html': {'beforeGitBlob': '7db2445f9c18ddd1d6b3c08177ca835cd8a03d11', 'afterSha256': '612b4544618d33ed880a52475c5a7c021fc4890b5a3a51f5989cd8748728f95d', 'bytes': 581192}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L2_Stem_Cells_And_Meristems_Explore.html': {'beforeGitBlob': 'e50c70d715fe89ab7092dcdae0c292319fa40908', 'afterSha256': '74e34849485b933417b0298046660a4eaacadc4d9058dc217915e6c7c1f18f63', 'bytes': 586673}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L3_Growth_Stem_Cell_Data_Application_Do.html': {'beforeGitBlob': '38ef948d3dcf46edd813a16d3ba5b848aff1363e', 'afterSha256': 'eaaa5d455e931849d295d149cd424283fc46e7b98ab0e27c2c028925295d890d', 'bytes': 597574}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L1_Stem_Cell_Evidence_Introduce.html': {'beforeGitBlob': 'b88f5980215ecd16b28fa555f3e3c9d8ec677713', 'afterSha256': '36c05e98e31bc0d0e16bd79806ef4770cfa4b395bbd1e244b717bd33cf2b9dea', 'bytes': 669905}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L2_Benefit_Risk_Uncertainty_Explore.html': {'beforeGitBlob': '63f432b77c3cc1753c145f0dc35b7482ddbd6d5f', 'afterSha256': 'e7aa28239965a78bbe79e39130a8c5838e9ff07f488c6d7cbd0deee766536b9f', 'bytes': 665804}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L3_Stem_Cell_Discuss_Do.html': {'beforeGitBlob': 'f39a152a4d0e860ad7caea698bbcfefac0825cb5', 'afterSha256': 'fc3f7a5ae735da56c852a2b189590f98c9ccfd71525affe09e947fa7846aecd1', 'bytes': 670048}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L1_DNA_Hierarchy_Introduce.html': {'beforeGitBlob': '7c5f21f53617127439d9549b2f476dbbc1dae6b7', 'afterSha256': 'dccacba41fbff9df9c7d641949ce496508a510cf919cbd562fd9ccf994c32e2c', 'bytes': 687254}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L2_DNA_Structure_Explore.html': {'beforeGitBlob': 'a68bffb7f1d835ace246e449c7305c8d7059909d', 'afterSha256': 'a728f5544363b581c391ae4d1ba577f325eadc65bcec2ecba781bea17dcfdfa4', 'bytes': 684923}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L3_Fruit_DNA_Evidence_Do.html': {'beforeGitBlob': 'a18ed66d4b5e86d8898c6f1117fc90d9b8190868', 'afterSha256': 'd1751c5bb73aed8daff1f09eb0cfcf73d7d3ee237f47fb052c487812bcce98fe', 'bytes': 608340}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12_Zoom_into_genetic_information_Classic.html': {'beforeGitBlob': '6a587dbd14df58b16fa2fa5246e53b47bad7a704', 'afterSha256': '90e297a0cd6989c101ecc966499c58ad6f830ede7a8c278e20319d35df6380b0', 'bytes': 688294}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L1_Alleles_Genotype_Phenotype_Introduce.html': {'beforeGitBlob': '7a9eaf4dc42fb1787820bf63ad108e83919b77da', 'afterSha256': 'f679964de4e8820e041b6b427ae2ae82910d8cdcc9dfef08dee0aca79ae759da', 'bytes': 564913}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L2_Punnett_Square_Explore.html': {'beforeGitBlob': 'de141b136011b67abbd32d4881c10ad4b11f9c00', 'afterSha256': 'da80ec932131c969c456ec35ff3514132901bbb51c2c002868308a220e71e79b', 'bytes': 565674}}
# END SX3_LAUNCH_W8_W13 REPLACEMENTS
# BEGIN SX3_GROW_W9_W13 REPLACEMENTS
SX3_GROW_W9_W13_REPLACEMENTS = {'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W10A_Solar_System_Research_Explore.html': {'beforeGitBlob': '44f914320587d4dea2f2b7c63687a70bf9c0be48', 'afterSha256': 'e10e97c2d792de2fad0ce454962e3a31ec608b43750bd71315b3bb1b0655981a', 'bytes': 1208801}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W11A_Global_Warming_Explore.html': {'beforeGitBlob': '1b93eab3f43facc231cd0d231e7cb2ba068975c6', 'afterSha256': '82b34329f1faf788152bc22c9e1f9eb8fd8236f3116d07337b9dca62b1325ced', 'bytes': 1250571}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12A_Science_Connections_Explore.html': {'beforeGitBlob': 'bd1b8dd818d1701dd48c28fa0cf04f1fbad3e868', 'afterSha256': '062a12a7dee5f5199ae91726f9ac0009cdf17e2dc4446d9e75c0288ab1213024', 'bytes': 1191958}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12_Follow_the_warming_chain_Classic.html': {'beforeGitBlob': '638e7f164589a6d97e3ddc07db21b0de525f8699', 'afterSha256': '94addd62c6e0169778b206e5dd59f51b508fd2ad329594718472d5222f224335', 'bytes': 1175220}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13A_Rover_Rescue_Plan_Explore.html': {'beforeGitBlob': '71b42846333433b4bf977c05018c352515e8d950', 'afterSha256': 'bae4a588c9382eec0be5901a500a9e3cde6e4b3d7bbc43d8fb1aeabebace712b', 'bytes': 1080841}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9A_Spherical_Bodies_Explore.html': {'beforeGitBlob': '296742454d41a40cfe497e00c698dcaec91df933', 'afterSha256': '2681b3f42b2bd6b8acedcd682c23d617c77eecfcce03b7cdac3db5a6751edb2d', 'bytes': 1183127}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html': {'beforeGitBlob': '2f4d1cb39459a14e63fde95fec961527c1c2322c', 'afterSha256': '3efded0179e818a3e7c0a5d0692610acfb4b91b1d85bc937c4b79bdd79668851', 'bytes': 1250935}}
# END SX3_GROW_W9_W13 REPLACEMENTS
# BEGIN SX3_BUILD_W12 REPLACEMENTS
SX3_BUILD_W12_REPLACEMENTS = {'Science_Teesside/Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html': {'beforeGitBlob': 'c773b52672335bf5306427612837cd2cfe058165', 'afterSha256': '509f38056bd09e903c70b0426ac55ab7ff73f7da10261a97eec11d49d7b27d1c', 'bytes': 1002362}}
# END SX3_BUILD_W12 REPLACEMENTS
# BEGIN SX3_FU1_F2_LAUNCH_W9_W11 REPLACEMENTS
SX3_FU1_F2_LAUNCH_W9_W11_REPLACEMENTS = {'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L1_Growth_And_Differentiation_Introduce.html': {'beforeGitBlob': '4b7d78b5ecf21b420f54e1c0da139a706e88f7cf', 'afterSha256': 'c5f7062f97517b87080578f7e9cc996320450a28414aafef722c5311abf74f02', 'bytes': 581455}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L2_Stem_Cells_And_Meristems_Explore.html': {'beforeGitBlob': '08bd4d6d012d5600f314f486f783148648007eea', 'afterSha256': '386454dba2e88fee123ddbd39c3965c6af2f7c18248eb1f4c58665f0f2c56ea5', 'bytes': 586931}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L3_Growth_Stem_Cell_Data_Application_Do.html': {'beforeGitBlob': '93325158600d010e5112d739cf778eb68f2c59f8', 'afterSha256': '5f4fa6ce615bd0210601c6229f15e76b309e7d3e070aae67be703689114cfadd', 'bytes': 597824}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L1_Stem_Cell_Evidence_Introduce.html': {'beforeGitBlob': 'e2b69ee18fd6af87cbed4cd6977fd86cec2085fc', 'afterSha256': 'd080289046c68268eb64f388251adbb05109f0c7da2ffb1fa0d596d44f82f66d', 'bytes': 670157}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L2_Benefit_Risk_Uncertainty_Explore.html': {'beforeGitBlob': '9ce4213d4cbbf797dd276c4475bd463853b96634', 'afterSha256': 'b4e898fa0e87db690fc1b95206df6fa5c95ff6827e267b8c96d10f377527ac9f', 'bytes': 666066}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L3_Stem_Cell_Discuss_Do.html': {'beforeGitBlob': '5ffc07d5db8125ae8fac55f2bb16b38f625c9c8c', 'afterSha256': 'ee3308dda387e77bcdec5a1d0bc150367858a906469885c9cdb21c466ec412b5', 'bytes': 670302}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html': {'beforeGitBlob': '853b380ea2ba3cd4ef4896b7f5d13a38b5cc5334', 'afterSha256': 'c0e2a3725ab889f9b0b51e5bad3c9056d1faf973f9f6353122947139e6084586', 'bytes': 655111}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html': {'beforeGitBlob': '8e8d6a7768602c356afda2391787509ce1ecb486', 'afterSha256': '3439d5e6d06fba838ad695d732b08f86775bf6fbf0536812447ba0ed5ef8116d', 'bytes': 672597}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L3_Identical_Daughter_Cells_Do.html': {'beforeGitBlob': '352544a8ff5739a6f474b662d0813172645f7847', 'afterSha256': 'a40855bf2e4d520ad1ec45f8dd442635141cb459c802dc56f9c4198505d708fd', 'bytes': 658549}}
# END SX3_FU1_F2_LAUNCH_W9_W11 REPLACEMENTS
# BEGIN SX3_FU1_F2_LAUNCH_W12_W15_A2W7 REPLACEMENTS
SX3_FU1_F2_LAUNCH_W12_W15_A2W7_REPLACEMENTS = {'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html': {'beforeGitBlob': '38050a7bbbfbcf08c0e69ce6558b4a17592e3bd4', 'afterSha256': '2b6fedfe3044b25254d4e17fe0eb7c235e0ed176cb50ab9c7bdca3c3a3c53d1d', 'bytes': 622791}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html': {'beforeGitBlob': '4899cf4f4747d9868841b5c298b0634d830a4e95', 'afterSha256': 'b8255a810f66250666744fd7793318d2bbabe0780a85f7ad8c97025337bc17c4', 'bytes': 623874}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html': {'beforeGitBlob': '5806f456d7a7ffc0e486965313fe34cb1ee6f603', 'afterSha256': '553454b2d545e0f6d0ed15cc4038ed2108ea7329ca8a81b945597d04c039c88a', 'bytes': 354578}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L1_Genetic_Condition_Research_Introduce.html': {'beforeGitBlob': 'b421623622cf937a790df35276281ad6a40b9dc0', 'afterSha256': 'd9556b6fc52357fc4c354e6f354270ca9e8da55f283dbcdd7a57faef991cef96', 'bytes': 624002}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L2_Genetic_Condition_Source_Evidence_Explore.html': {'beforeGitBlob': 'e0ae465c32e199b6c1f7cb986f1cd772f345cff5', 'afterSha256': '08a47f06000f3a14ac38f6afb94b304b8f6dbf2f36b803f146639d1a7dae52f7', 'bytes': 625512}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L3_Genetic_Condition_Presentation_Do.html': {'beforeGitBlob': 'fa466d423f8b99bd6dd2597e31d9b5469162217e', 'afterSha256': '59fa8708f3fc2b1331a49a03b63465e2e2713af8c7d69091df356ec287970491', 'bytes': 625895}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L1_DNA_Hierarchy_Introduce.html': {'beforeGitBlob': '51706cc7f791bd9bcd237cb309e67b7cccff8019', 'afterSha256': '84b9283cd2d65a80204ed899f89205572f290d6661fb7d62fe513f9c897a1873', 'bytes': 687502}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L2_DNA_Structure_Explore.html': {'beforeGitBlob': '79ea2c82134ae624a0c0d5c230f8fe2c6262abc1', 'afterSha256': 'e84e681deafc43f233e582ae15adeccebe06feaa3b2bb2674d7e8e4089164517', 'bytes': 685174}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L3_Fruit_DNA_Evidence_Do.html': {'beforeGitBlob': '7fd5d97f0482e45460d5a5e4883cfb9ada3e7bb7', 'afterSha256': '0a3e7536dc9110d705e0cc58e70bc845c982b3a1f9431d0b01debac1247c03cc', 'bytes': 608592}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L1_Alleles_Genotype_Phenotype_Introduce.html': {'beforeGitBlob': '69bd791d2360ecf1316bf7e215d8b2ba4d6d7b4e', 'afterSha256': 'fac4a58dbc596176adf28e246565c8bd46636a9121fb84be50e15ac8bd9c5e04', 'bytes': 565159}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L3_Inheritance_Probability_Do.html': {'beforeGitBlob': '3ec7ff70a7649cdfa741f050fc5933f97b8c9e3f', 'afterSha256': 'd0d4f47746946fd0cd332be94865e7282fdaf97fdd800f6646718cc35b6beb7a', 'bytes': 567524}}
# END SX3_FU1_F2_LAUNCH_W12_W15_A2W7 REPLACEMENTS
# BEGIN HUM_T_BATCH_1_BUILD REPLACEMENTS
HUM_T_BATCH_1_BUILD_REPLACEMENTS = {'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W1_People_Special_To_Me.html': {'beforeGitBlob': '4bb1074189b21e91087df8927ee723105a24c4c7', 'afterSha256': '030be544f76147106e1a7f817ddca11142fcbaef168c28ef2397316a069f384a', 'bytes': 95433}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W2_A_Special_Book_A_Special_Place.html': {'beforeGitBlob': '8e7db5de89c23afbfba66713b5e3e60cf5779efa', 'afterSha256': '197d3ebfab750e84d89ee5e3dedb177b9d86d768602d0ef62be0ac4582cd34cf', 'bytes': 98319}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W2_People_Who_Help_Us.html': {'beforeGitBlob': 'c3d2f2378899ffe02092e3726718c8eb2cf9881f', 'afterSha256': '7b90dbfb9e82e1a4d20dda3703e68086c5367643bd3b58c8533e97836dc80521', 'bytes': 95457}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W8_A_Festival_Of_Light.html': {'beforeGitBlob': '6f22979d25922d5689b4587667a4b49358a5e098', 'afterSha256': 'a91c419bde53ffefe77b17db0e8ebb9973b4df447690c6a41a94c76210a654f5', 'bytes': 94669}, 'Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W14_Festivals_Display_and_Reflection.html': {'beforeGitBlob': 'a2b6acc8ac4028d6aa72212cefecf1ae6bef3aa4', 'afterSha256': 'bf14c15092537d25d1b067d5cc32bba8b5ded673e2d8247b352b0431c8abbe59', 'bytes': 54692}, 'Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W15_My_Week_Timeline_and_Caring_Stories.html': {'beforeGitBlob': 'db2a579beb1e7e44836a8ae1eabf021387b47ec0', 'afterSha256': '97e71086dcda835b431f9cf94d545f802429faabbb0bd76d26a30987c70ae8fc', 'bytes': 59980}}
# END HUM_T_BATCH_1_BUILD REPLACEMENTS
# BEGIN HUM_T_BATCH_2_GROW REPLACEMENTS
HUM_T_BATCH_2_GROW_REPLACEMENTS = {'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W1_Beliefs_And_Worldviews_Around_Us.html': {'beforeGitBlob': '92b0e571c8d114ae5a1498a06425583cf126370f', 'afterSha256': 'e026cb09ca0c26998be6172bd5622545878cef9cd509b4d2f6c0454ca7ab1389', 'bytes': 93788}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W1_Migration_On_A_Timeline.html': {'beforeGitBlob': '5dda87bb7633d94f2bff00c2acec74a4d8ace2a3', 'afterSha256': 'dbf44fe5be6e352cd6210d1b7426c15bfd4e00dd6f02a9f1643ab41d90ee75ce', 'bytes': 93977}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W2_How_Beliefs_Shape_Who_We_Are.html': {'beforeGitBlob': '881912c1a9e96e5b4bf6b7da13fc0e54f4a66b3c', 'afterSha256': 'adc0e844bb2b51bb9c0f646464ab03ae67736b28a1e249d27d56c15e28ac9734', 'bytes': 95484}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W2_Reading_A_Migration_Source.html': {'beforeGitBlob': 'e27e1f42b371dbf143e1271968b119bdca8f2bda', 'afterSha256': '2c505b209aaf25af14425d63dfc648939257a8f3bade68fd3226296b7da80287', 'bytes': 93954}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W3_Why_People_Moved_And_What_Changed.html': {'beforeGitBlob': 'fd6c5f22decae11d8e9b8bab30996800fc1a8456', 'afterSha256': '5a389f52fac689814f978804cfa9e1213d9b16df21c74f3219bea27df2edffb2', 'bytes': 116634}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W4_Diverse_British_History.html': {'beforeGitBlob': 'ebf8d64a8126ca5e8c7839945c56cb3bf1bfd088', 'afterSha256': '1f13e87e4f3f11233b417cf1e05c038e83de2bec3d8c49bfd092b9c5527c7b4f', 'bytes': 95116}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W5_Was_It_Significant.html': {'beforeGitBlob': '9a93bb57417ef380e175351f6d0a21cb7a3afbe2', 'afterSha256': '9ac862ecd06d8438d8f8a1b4a4a112f5fc95e7136a19226080c6e52c2583fcd8', 'bytes': 90755}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W6_Planning_An_Account.html': {'beforeGitBlob': '35a40d75d72dfa4e22358d3790a00c5c8dbf230c', 'afterSha256': 'a09c410a1b04098e91327b523c04d4877b40343e3c2f01e41c66f65d01002708', 'bytes': 88073}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W7_Writing_And_Marking_The_Account.html': {'beforeGitBlob': '6106e2e41145c6a61f8e58fa62121559140a1130', 'afterSha256': '015a5514cc1145a35084834d470f3138a0b41359d43c6e7385a539a81fc36e0c', 'bytes': 87549}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_HUM_W8_Finding_Places_In_An_Atlas.html': {'beforeGitBlob': '8d7f014045dff910c8ef34ce8a44c6e13004287f', 'afterSha256': '6739b5cb8d059f972012844f20d6a49249b5bec231cc018285675a44dcdca7be', 'bytes': 89605}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W4_Explore_Hanukkah_And_The_Theme_Of_Light.html': {'beforeGitBlob': '5365d82b2317109fe3689b7d585d8ef05f8f497c', 'afterSha256': 'cd82d9e3ba3bddc820e4e6980338f8055d42e4f7c4279532d4eb6a2d78605f10', 'bytes': 62148}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W5_Explore_Christmas_And_Christian_Belief.html': {'beforeGitBlob': '47e1bfc1b1e517cad3b442aca900b086e7ab9f08', 'afterSha256': 'e21ff0ff140cdff349c3e6f8dc5bc314be9e8d6be05d888cb8008382b5a85daf', 'bytes': 61583}}
# END HUM_T_BATCH_2_GROW REPLACEMENTS
# BEGIN HUM_T_BATCH_3_LAUNCH REPLACEMENTS
HUM_T_BATCH_3_LAUNCH_REPLACEMENTS = {'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W1_Belief_Identity_And_Belonging.html': {'beforeGitBlob': '0508f96db39f9ddfcaa8972795241001486029d6', 'afterSha256': '6dc9a434f33931eb5f38c65454feb5fb87588afaa0053f3a0c95c216a4c8fc4a', 'bytes': 99676}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W1_Migration_And_Identity_In_Modern_Britain.html': {'beforeGitBlob': 'a4bdc613574bc300f30b894497ca81336502680b', 'afterSha256': 'b965d521d918cd24408059c8d940966c16c138f2a8c40fc51860e2f8d67ea9c3', 'bytes': 103613}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W2_Cause_And_Consequence_Of_Migration.html': {'beforeGitBlob': '5828cc32d458bd7665c82ab00dafeb8afdc57803', 'afterSha256': 'c49b62b36952fbe4da9cbd19dfc7401a628ecbc423451a188fa3fd9b55d8dd0a', 'bytes': 104388}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W2_Two_Worldviews_Side_By_Side.html': {'beforeGitBlob': '62758c32880cbd612935d0e1b8eaa971d816d8b5', 'afterSha256': '439d8cacebdc7911314b6aad2bc92d0ecff5dce7364d7bea4b56ac70ba1e15d8', 'bytes': 101646}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W3_Can_this_record_prove_it_Classic.html': {'beforeGitBlob': '251d1d5931342f43473a0d36c8741dab7110125c', 'afterSha256': '1737abaa8804ae7da34ae45ef064c133149dbfe619a0e122e9dd2c0862d85660', 'bytes': 162095}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W3_Evaluating_A_Digital_Archive_Source.html': {'beforeGitBlob': '1a823d4e525f51f9d0874ab4bdecf9b2755d7490', 'afterSha256': 'a385de10b4db2e5a5370ed24db214bd0ec0ade59d2604eae12b51d3d74091204', 'bytes': 103377}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W4_A_Timeline_Of_Twentieth_Century_Britain.html': {'beforeGitBlob': '53c90fb8d910fc563c7fd1d3a12ed85479536f9d', 'afterSha256': '24f7ea8a63f02f88a291a59b65db8c878e8ae85a32d831b79736b31113d10559', 'bytes': 102394}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W5_Who_Shaped_Britain.html': {'beforeGitBlob': 'd17745908c8bf69e1fc1079a929f526234bb802e', 'afterSha256': '0a1a646dda79dd7db040af551128294caef16fba6e3e90a4dae233d99b34fa7e', 'bytes': 96175}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W6_A_Structured_Account_From_Evidence.html': {'beforeGitBlob': 'd6905979b5d4b0324484d4c025c5b67d2e7885a6', 'afterSha256': '55e46c6599d930327833d95493f1017fba4ba76c64ba4fddbc540f9ae49985eb', 'bytes': 93108}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W7_Source_Based_Assessment.html': {'beforeGitBlob': '82c9e3c6c141efe8f1b1a599e2efbe9af9be62a0', 'afterSha256': 'a42f61b9de0ed5b9d89ab18cdde017dff34dd789b43219011a5a563ad7cdab87', 'bytes': 94427}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References.html': {'beforeGitBlob': 'b2f4437dd21138b525a700362eb428603a51dac3', 'afterSha256': '7dcb2d67927b3d74376f4e1c822aac82d036210af59e94cecd8647ef8d6fe7de', 'bytes': 94444}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W4_Festivals_Shared_Values_Day_Of_Peace.html': {'beforeGitBlob': '10108aafe6e145660c7858ca6303945a99ba6999', 'afterSha256': '2495d9a762c6d434c5d1cbac3b0ac63d8f7562b2f38a98d863d0e3d201f16239', 'bytes': 69049}}
# END HUM_T_BATCH_3_LAUNCH REPLACEMENTS
# BEGIN HUM_T_BATCH_4_GROW REPLACEMENTS
HUM_T_BATCH_4_GROW_REPLACEMENTS = {'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W6_Compare_Festivals_Of_Light_Respectfully.html': {'beforeGitBlob': '52abadd9ac8d2a2678ae4df2e958df56088c615f', 'afterSha256': 'd4da31012106415fca6641fcd1d5bcdd7e9213cef98897dcab972f0602d850e4', 'bytes': 70134}, 'Humanities_Teesside/GROW_W1-W8_2026-27/GROW_Humanities_W7_Reflect_On_Remembrance_And_Shared_Values.html': {'beforeGitBlob': 'ea382c07eb300ba4127cd4dc2c3f35b2444cc12e', 'afterSha256': '3fe17c6e46638def69dfd72132605e4540f289f272cc87ca2d9408c7525a5cfa', 'bytes': 70718}, 'Humanities_Teesside/GROW_W15-W20_2026-27/GROW_HUM_W15_Rights_Timeline_and_Belief_Resilience.html': {'beforeGitBlob': '764a40163a93f9c47ce260af6db4121f0e06a439', 'afterSha256': 'dd22c4d6f96f00a9f6a1174672c2145dafa34171d1148f65b0c68b1c4b1dae03', 'bytes': 77330}, 'Humanities_Teesside/GROW_W15-W20_2026-27/GROW_HUM_W16_Sources_Campaigns_And_Hope.html': {'beforeGitBlob': 'df0c380739769e0eec34a299b36eeda951f01efa', 'afterSha256': '8acbafb35b90a104d1aad179c188d5e29e4c99e5a35db033daa7087d8edeb07e', 'bytes': 58820}, 'Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W10_Teesside_Connected_World_OUTSTANDING_V3_1.html': {'beforeGitBlob': '91397b102e966a09d47f5b9e80fd5631cdea3191', 'afterSha256': '6c0d8b003c060237fbbf308ff57b8c90db4d939d8299c1658c0e4bef4af1bc36', 'bytes': 172146}, 'Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W11_Light_Across_the_Map_OUTSTANDING_V3_1.html': {'beforeGitBlob': '6c4290110cc5579c349fc52019ce31c5475f01f2', 'afterSha256': '3ddc21faaf0d98be4304ad63bd8c659b556676288fc0c4ac89b55c622b543a64', 'bytes': 118273}, 'Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W12_Compare_With_Care_OUTSTANDING_V3_1.html': {'beforeGitBlob': '0282e60582672d96d4390d3f942ad6617bfffad6', 'afterSha256': '3fcb995013519cafcc155e7ad11c3cde94913149dd8362233a3c67e418c0c583', 'bytes': 114083}, 'Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W13_Belonging_Briefing_OUTSTANDING_V3_1.html': {'beforeGitBlob': 'ee1c27d16cb46b1c0944547c8c1eca9f9bbe001f', 'afterSha256': 'a8fc4a21540e85c6ff00ecc04fcfcdcf27ffaa3b2017022ee99ed7d5299f5170', 'bytes': 112888}, 'Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W14_Map_and_Belonging_Challenge_OUTSTANDING_V3_1.html': {'beforeGitBlob': 'dede8c73fbf6f85bc1861a66c137300669ba154e', 'afterSha256': '6935c53274bf191f7cfd0c62c0c03bae85e60e44c00b85f0abfa19b4dd81aafa', 'bytes': 108701}, 'Humanities_Teesside/GROW_W9-W14_2026-27/GROW_HUM_W9_Pinpoint_the_Place_OUTSTANDING_V3_1.html': {'beforeGitBlob': 'b58eb4a17f2c77df079da512f44d97b1b73cc208', 'afterSha256': '69a9285e4e671645754b80c8fd1624d699977504cfa40aacf770acf51a465024', 'bytes': 128020}}
# END HUM_T_BATCH_4_GROW REPLACEMENTS
# BEGIN HUM_T_BATCH_5_LAUNCH REPLACEMENTS
HUM_T_BATCH_5_LAUNCH_REPLACEMENTS = {'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W5_Structured_Explain_Response.html': {'beforeGitBlob': 'bac3320dc062289dd8bc8a4bc1313eabbb035f54', 'afterSha256': 'adaa425bab46005aef4cf6c6d6997760ff75818965a7461af2f145c974016762', 'bytes': 68399}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W6_Remembrance_Peace_Across_Beliefs.html': {'beforeGitBlob': '66fbbf8b6ef2c91e375cd4f939754aef5bd805b0', 'afterSha256': 'b0e93d11cd494ec361058214da3193f2721cd6531fbbc99af4a0b3c888dad351', 'bytes': 69348}, 'Humanities_Teesside/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W7_Belief_Identity_Assessment.html': {'beforeGitBlob': 'c2be12bf8eb84c3893b983418887f4dc22925d41', 'afterSha256': '1b2c8e41fe9e740614b0685c6ab594614518acd15788905282d84cbe7d1e239b', 'bytes': 69111}, 'Humanities_Teesside/LAUNCH_W15-W20_2026-27/LAUNCH_HUM_W15_Conflict_Causes_and_Ethical_Decisions.html': {'beforeGitBlob': 'c2dcfe2afc502bf84c1cf46bff37dd51253c8fdb', 'afterSha256': '36aad344c9e91f5c1fc4aeb28c111fee64864868e28ee7dd36252d0c6caa1047', 'bytes': 79052}, 'Humanities_Teesside/LAUNCH_W15-W20_2026-27/LAUNCH_HUM_W16_Steps_In_Law_And_What_Comes_After.html': {'beforeGitBlob': '6e69cda7af45e9c2a3cf52352f4c9a4d37419f53', 'afterSha256': '1b2b12b93d4bf4583aca5356151b2c469d7ee3ba93d502d6a943686cb93a0b42', 'bytes': 57882}, 'Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W10_Settlement_And_Urbanisation.html': {'beforeGitBlob': 'dbed25719faa45abec6572f095bb87897b6a2c1b', 'afterSha256': '127026a754e180800e9202a552f938b2af446730bc5e533f2aeb822b12692e64', 'bytes': 123824}, 'Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W11_Local_Fieldwork_Collect_Data.html': {'beforeGitBlob': '007ecf5afa0b8bfa820a56339682bee8654105b4', 'afterSha256': '3f83f53d6a8b7a02d397aa554f6a59977a04c9a1beb3bfa532949f23ed4eef92', 'bytes': 125555}, 'Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W12_Fieldwork_Data_Graphs.html': {'beforeGitBlob': '7a2dc0dce7ec6441532a52bae1e60438373fb13a', 'afterSha256': '4018cf72fb54cad4c3d6e21d4dcbdec6117554331546fefbd4b756684cc83a8f', 'bytes': 122725}, 'Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W13_Contrasting_Places.html': {'beforeGitBlob': '0ebebf04065fa3b89ae8e2a52c55f75e2e57651f', 'afterSha256': '66517aec3c3bf97dc4eb536535aaf009bfb8b91a0f0088b04c7d6d1418fcafbf', 'bytes': 121177}, 'Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W14_Fieldwork_Enquiry_Write_Up.html': {'beforeGitBlob': 'e4a9556c7e1d9695f416afbbc30bd12253908b8e', 'afterSha256': '1e200c6fa11000e66d7e529135876de9c2481ab107f4cf1a68cdc77691f21994', 'bytes': 125631}, 'Humanities_Teesside/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W9_GIS_Layers_Reading_Place.html': {'beforeGitBlob': '26fd39773f385b986fdcf78af21c1d24a239f603', 'afterSha256': '8544e086b5e4a6c611982f289fb697626731041eb1cbbd77a4f3e454928aba61', 'bytes': 152643}}
# END HUM_T_BATCH_5_LAUNCH REPLACEMENTS
# BEGIN HUM_T_BATCH_6_BUILD REPLACEMENTS
HUM_T_BATCH_6_BUILD_REPLACEMENTS = {'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W3_Places_In_My_Community.html': {'beforeGitBlob': '2acae9bd3f72b7605b3a893690aa1376ae6e8e0f', 'afterSha256': '1ed894d2443de648e0deb5aaf4615c6b92b0735abc27c109947a3c31c137d5e6', 'bytes': 102204}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W4_Then_And_Now.html': {'beforeGitBlob': '6e8e92bffa170d29d2ce44b6c84ef11d6c6776cc', 'afterSha256': 'a794d0c8095c8b8a29619335db783ced6742da4bde938161312908eb78c34a04', 'bytes': 103203}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W5_Same_And_Different.html': {'beforeGitBlob': 'ed5086569bcc26de22bb466e2299d080143d409f', 'afterSha256': '7e8bbd4524445a76e3f22ea8eab447ba4ab7b7d5f44704e74b7633bef2e5f8a3', 'bytes': 101656}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W6_Our_Class_Map.html': {'beforeGitBlob': '64c6c14a87392d48c6fb65663df559d3a9797c7b', 'afterSha256': '3ed142de2819ad74040c4ec8a55038225e41f98671a82c018f0a1c4f3a36b5be', 'bytes': 98852}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W7_A_place_in_the_group_Classic.html': {'beforeGitBlob': '9171468b4c651e8d4e8c519279790e226d1aa8e5', 'afterSha256': '8846108977a6fc8dca26f820a24421340348da432bbbf9e34865f9930ce3eecd', 'bytes': 166328}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_HUM_W7_Groups_We_Belong_To.html': {'beforeGitBlob': 'ffd928ffa71f0c5a6e1372933da203c1928c6b75', 'afterSha256': '3dc05abc16c9baa2cb2978226d0f047d84fc8f2583fe2ba3da9d9a5a20ccf063', 'bytes': 100604}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_Humanities_W4_Show_Respect_When_Handling_Special_Objects.html': {'beforeGitBlob': '1dcf51c195596b85854c12c960415c2f36547781', 'afterSha256': '3b884a498d58b04130fe97ecfae52b60ad8c13687d4b82c8581c5a9c7f89670a', 'bytes': 71815}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_Humanities_W5_Notice_Similarities_Between_People_S_Beliefs.html': {'beforeGitBlob': 'f261e1d70c248483b803da0c454810cf1217e3ea', 'afterSha256': '701831c9205b4756b9397a583370b68f774110bcc11863380622eb816a1bd91a', 'bytes': 71006}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_Humanities_W6_Reflect_Quietly_On_Belonging_Day_Of_Peace.html': {'beforeGitBlob': 'a9d6d72817e468210b0b6c2a78bf13d28e14fe0c', 'afterSha256': '788f671f8221b03e2358371e620cba251f03879c7ac223aaec265118b6cd2665', 'bytes': 72427}, 'Humanities_Teesside/BUILD_W1-W8_2026-27/BUILD_Humanities_W7_Share_A_Special_To_Me_Object_With.html': {'beforeGitBlob': '088e1636c3fc291f430c9476f93355a31bb9b4e1', 'afterSha256': 'be33baa63d4523febdbd0c4f6826efe272b68958c3be44b560a349b0ebd05266', 'bytes': 72865}}
# END HUM_T_BATCH_6_BUILD REPLACEMENTS
# BEGIN HUM_T_BATCH_6B_BUILD REPLACEMENTS
HUM_T_BATCH_6B_BUILD_REPLACEMENTS = {'Humanities_Teesside/BUILD_W14-W20_2026-27/BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html': {'beforeGitBlob': '2524f8483d79a689889441eed736bf799c9f9173', 'afterSha256': '8513df51ec2501cbfe57d63892347c235cf101cfb6fe63eebf868079470b7dd5', 'bytes': 100827}}
# END HUM_T_BATCH_6B_BUILD REPLACEMENTS
# BEGIN ADDENDUM_3_V3_EXPLICIT_TAGS REPLACEMENTS
ADDENDUM_3_V3_EXPLICIT_TAGS_REPLACEMENTS = {'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Knowledge_Organiser.html': {'beforeGitBlob': '1502108a4c216f150563f07986b328b5caa1e026', 'afterSha256': '556d3d5d29e29c0f25f27d0892bb17c67ba9647e77551486586a0473a40d01d0', 'bytes': 5966}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Pupil_Resources.html': {'beforeGitBlob': 'd89b17fae34ae71bb97b6ab9d4e51a62b2dd1acc', 'afterSha256': 'a17b507c6283060aebd135e10bf7ccc5e2b22cb2a3b152ba4b127dcb9a9cf94c', 'bytes': 10843}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Knowledge_Organiser.html': {'beforeGitBlob': '19d09e8a91de219c4d89cf30d6f7a4d0f231c1a4', 'afterSha256': '2ea53fb30d70a48967f945ba2d4d1136c378561cd18ab8d848b4282e2da91367', 'bytes': 1615}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Pupil_Resources.html': {'beforeGitBlob': 'ff4cbc87fbdacc399a4212043fba8da3c830727c', 'afterSha256': '70890527e2cadc3c7702f83fbf61d19fb4e6aacbe3615e2e0969b163fe2a073c', 'bytes': 88591}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Knowledge_Organiser.html': {'beforeGitBlob': '86933b4c67e6fc4e02397969e20d5fe464f4bed9', 'afterSha256': '824bd892a835fdc21cd5a005eb9900f8b4871fc892ebd88c87515cf0186cb561', 'bytes': 1621}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Pupil_Resources.html': {'beforeGitBlob': '851570bf5b44c8c9ede6040e74f20636736f5a24', 'afterSha256': '30d67db22a8884d45a304bbe397624fd58166ad427c9bcee79f6bf74c7a05ade', 'bytes': 137255}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Knowledge_Organiser.html': {'beforeGitBlob': 'd7088905c9086af5bc3ac04804c0b22b65a9990d', 'afterSha256': '42803ade88d4545eae2d737d3a5dbe6b434e8606289e92a914b153cb0824c994', 'bytes': 1691}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Pupil_Resources.html': {'beforeGitBlob': 'c8fb40e3d49354503fd649620c307c46c5a2e7cc', 'afterSha256': '362980a7a5ee6f799d6d286fd059a4a4bc0fd33fe3e1d505e472094c599262c9', 'bytes': 113511}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Knowledge_Organiser.html': {'beforeGitBlob': '53fa7824cbe383b8989c91bef8a9d3491bc6de06', 'afterSha256': '06b68734e46fd57805bf935d4b29215e6722cf8279ee646ae6cb20bbc9acb16a', 'bytes': 1628}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Pupil_Resources.html': {'beforeGitBlob': '266911f9f62205d0278ae73c391b34ac857cfa5a', 'afterSha256': '1a88bb8d3d669ff0755eb4219f2d73975c9f52dc7cada1ac60f925d321a910a5', 'bytes': 214128}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Knowledge_Organiser.html': {'beforeGitBlob': '42563a454c3e239e93c8f021ce06e74d6425c85a', 'afterSha256': 'bd6d34df7c9686981de13f28d708790df9e436462784fbe3e66d0ff446a58d50', 'bytes': 1681}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Pupil_Resources.html': {'beforeGitBlob': '8377498534bf030fa5c85d9b1f4fe440fa4f63fe', 'afterSha256': 'e1e4fec278ac3babb5e1b7ca7faee523f47c0b3475f9e168d160cff787ff5a3a', 'bytes': 67412}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/CHANGELOG.txt': {'beforeGitBlob': 'fdcc3803d320b4277f15542b0b35c49c45f1ae49', 'afterSha256': 'e457688868342e104f2b79b70076b8a6a2fb702b4c7a73dd61cbfc785549d5eb', 'bytes': 15854}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'db13b8bfb003c6dc37ed5cd4b7ee6127af606b3e', 'afterSha256': 'a2f33a05811267f87b06a04f05723b77da19f43e8505e3d80da5ef1c3714b181', 'bytes': 12002}, 'Humanities_Teesside/GROW_W27-W39_2026-27/CHANGELOG.txt': {'beforeGitBlob': 'dffe6a8a950390b2cc200dc9d1657b621be7ed16', 'afterSha256': '78babfc353874e85c0bbaaab578a38c7e43f63b163b53f0b1e78813e995ef365', 'bytes': 18072}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Knowledge_Organiser.html': {'beforeGitBlob': '0b9897ccdc4baf7bd190705a09042b66ac416ef9', 'afterSha256': '304f7b59f07602dcea6463a35491591047cdb7bca7d14a2ec8c56e2c24e3803d', 'bytes': 1619}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Pupil_Resources.html': {'beforeGitBlob': 'b68a1fafac87e6f0e3c671c54878548f638c891a', 'afterSha256': 'ab1d438785a6a0fd91f874814c1747dac1b0fcbda4c4b91840f8c4db3a65af52', 'bytes': 388885}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Knowledge_Organiser.html': {'beforeGitBlob': '723895ae1b7e523cf8e7e9326e26e682a4e9d8a7', 'afterSha256': 'a42bbd596ed226d5899f138011467a9cf3839fb86b2f9eea5b19eba8e13c6ae7', 'bytes': 1764}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Pupil_Resources.html': {'beforeGitBlob': '3dc07f9d84e0b75471554fb69e514352c8d6a7b0', 'afterSha256': '36dfe84098c138356492134e85257ceebb96de68b02276befeb857171b3f97db', 'bytes': 75022}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html': {'beforeGitBlob': '8b5c94c04936a87a1c6064a305bcdf13d787f995', 'afterSha256': '065bdd2a52f0fc5ab531e884fffad40c0367acd1b003932a160b903aba0356b3', 'bytes': 1606}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Pupil_Resources.html': {'beforeGitBlob': '873eef339909b7497b3bc1c0bff474b572f8baa1', 'afterSha256': '1e7d950944151e84ab163a47b739af51ea323a1fae89c83ab20ea0d04a1556e0', 'bytes': 80719}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/Sources_and_checks.html': {'beforeGitBlob': 'c7287204a96486423e757bc98f7ef57fc8284d79', 'afterSha256': '5ac92240747e170ba0614f7b3d75b75821807a35cd80070469d14d39f7c58cd8', 'bytes': 683}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Knowledge_Organiser.html': {'beforeGitBlob': '53bac895b4bb6e77919db16c3c02cb6058a47f65', 'afterSha256': '1f30e9fbc0857fb5034bf2a0865f3117dc533812992c13c44ac3de38720a0069', 'bytes': 1508}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Pupil_Resources.html': {'beforeGitBlob': '2c15baeb21809359d9a3f77edf7875c4d20c0e50', 'afterSha256': '82e6b27a2c6a27d734d55c7f57c7884c6c7217d91d6a8847124218dc4719be96', 'bytes': 74391}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/Sources_and_checks.html': {'beforeGitBlob': 'fa29784c0d87f601e256ec71d951f8aea69b58c6', 'afterSha256': '0dfd4a4c0735cd9a5ab1a3afccf041acbfc3a03f73665312a41fa43390eb9136', 'bytes': 683}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Knowledge_Organiser.html': {'beforeGitBlob': '39fc12a4069d11e5f378268ff274eadcce19f12e', 'afterSha256': 'b3b9079ae07d5fd47c126db1a2ac8d83fee82b921afef61d17fab7262bf6a7bf', 'bytes': 1654}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Pupil_Resources.html': {'beforeGitBlob': '00a5119f9171b065e77debeeebaab274e6ea304c', 'afterSha256': 'fb6d41b2fa1f78f77e8ec9aa367beec42e32a53f3482fc4902339359039ca16d', 'bytes': 121231}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/Sources_and_checks.html': {'beforeGitBlob': '26e3d40d820bc6df7599154d35707231714de532', 'afterSha256': '138d10b4b93fc3fdf1ebba492a2792fd7965f9b1ee609e65baa87628a486c30d', 'bytes': 683}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Knowledge_Organiser.html': {'beforeGitBlob': '8f704ef2d2c550abb948aac7e39763c05e8f1795', 'afterSha256': 'b2e73fd5f74e5f36c546aa6bcdc464a2ba8e8d47a0351fcd6e3d77c17c8c1531', 'bytes': 1738}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Pupil_Resources.html': {'beforeGitBlob': '4cfb07559bd8e1292694aff4e8dba959bda32e5f', 'afterSha256': '97ae893548878fc7723a78407d5a50d5e4197c4a1a29a2c5ee19599a595a6c88', 'bytes': 84015}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/Sources_and_checks.html': {'beforeGitBlob': '13d2154e45f40a3cfdc66557a2c21876b55f07c8', 'afterSha256': '6402d0a62614985befaabdcdd2296e651f5a81658084d6211242400db7116964', 'bytes': 683}, 'Humanities_Teesside/GROW_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'fec80c4969594fd66648c6d2f2d813ad56a1a05f', 'afterSha256': 'abdb9e0a4e471fb90e17fefedab648520d7a539887e1c750f24ee5c586268081', 'bytes': 11544}, 'Humanities_Teesside/GROW_W27-W39_2026-27/START_HERE.html': {'beforeGitBlob': '3f6a1c0ee452127d5a93a038936c2efa1a0b6330', 'afterSha256': '5b42ff6731ab969eff417f9f2e097a6a1a079e640df30ff4d1b604b8c567bf0c', 'bytes': 9832}, 'Humanities_Teesside/GROW_W27-W39_2026-27/Sources_and_checks.html': {'beforeGitBlob': '403bc30199025e39e075a2cee9e5bf10f77c7486', 'afterSha256': '8e228edb5efb550f7489eda8bed5011bbb3d590070c98a16579e345a81bee991', 'bytes': 7478}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/CHANGELOG.txt': {'beforeGitBlob': '5d2a5b6cf840a035198e7fac4494014e994445a6', 'afterSha256': '4691a85f7b679f4a566bac8c14106c2ae24cecf0b5bd4481a6f019abbf742403', 'bytes': 17520}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Knowledge_Organiser.html': {'beforeGitBlob': '435ece855059f095d79eef9e854e516aa921d771', 'afterSha256': '7be6562956e16fd2d72bc8b0659e7e91fa2edd79f42ffb485b119b1da7ddfd46', 'bytes': 1660}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Pupil_Resources.html': {'beforeGitBlob': 'f51ae70da2ad8ccbe5e281448cef622edc5c38fb', 'afterSha256': '4762c9e4d7788be18a14e5d82eac15d601f16321a2583413f753a3838f430665', 'bytes': 13374}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/Sources_and_checks.html': {'beforeGitBlob': 'dc52260f9b37254e8598cb7941719c937fef8294', 'afterSha256': '29877c91d17404473b4012869c22b7a3ea84ad5be63120e5049cee3d479a0a32', 'bytes': 669}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Knowledge_Organiser.html': {'beforeGitBlob': '6502dd39818788a148739b17dd0baa3fb4b914f1', 'afterSha256': '2940b779de567a8aac8deaa4b0ee410694a0f9ae652daaa4805cc0cdcf817c6e', 'bytes': 1631}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Pupil_Resources.html': {'beforeGitBlob': 'add223c4ba10862c9c9a0b4afcb6aa4975211b34', 'afterSha256': '74b0fa6f2f5bf0d86080533f275626f9a9523b149ed78beafb5579e53bd5f1eb', 'bytes': 11670}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/Sources_and_checks.html': {'beforeGitBlob': 'b00a438665f289d870a09e9675206196d878fcae', 'afterSha256': '3bfdb8be74a4931b03c73c3d6f623e1af7933f948181e612be70858ef7cdcbe0', 'bytes': 669}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Knowledge_Organiser.html': {'beforeGitBlob': '4d5891cf7a7eac5c137638e8ed9959b3add0bb16', 'afterSha256': '4e6f5a54ad4a590444c1d21b055054a82094f9fa5a55aa4a1af96c61acc1793b', 'bytes': 1634}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Pupil_Resources.html': {'beforeGitBlob': 'c9229dbb257e18a8afeb2188497a174dc80015e4', 'afterSha256': 'd959fb5482f9a342f4fdabd6bfad3ac2adf2d297ca225c6a63d96d319dd3f818', 'bytes': 12042}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/Sources_and_checks.html': {'beforeGitBlob': 'bbbff5b2b4cf5076edf1f0ee919de677e8427179', 'afterSha256': '81c9c9ff9dcc195f52f92246cc10cd716fb1b4aee6bde3ffea051d5462985c06', 'bytes': 669}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Knowledge_Organiser.html': {'beforeGitBlob': 'd69e22bda0fb98e45b594b52dc384b41ed145c1b', 'afterSha256': 'a6e0134a5bdec15e6b940fb140540255f7d15bbacb4fb6516d7889a6545b8725', 'bytes': 1630}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Pupil_Resources.html': {'beforeGitBlob': 'ad79d71734e2c14222b8242f3c3e7793908490d8', 'afterSha256': '4d565463075d7ef6f7f2aa68241a7f8fdeb47e0d000ae37f77a1f65a674a4251', 'bytes': 12160}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/Sources_and_checks.html': {'beforeGitBlob': 'f66b341b049e71a492a958337130ef46fe7510c7', 'afterSha256': 'b05876ddf7f80f7319fa1b0b3f49e20187b87ca749fc1f85166b0ea85cec8cd0', 'bytes': 669}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Knowledge_Organiser.html': {'beforeGitBlob': '3bbe80c873bd21887cec7157f8e7d2faee8608da', 'afterSha256': 'ab7f110871e6ee7c63a8d21c20b12b49b66f5c38693367ff0084a04c64926d02', 'bytes': 1640}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Pupil_Resources.html': {'beforeGitBlob': '57e2a91c22af5c9ded61747396414e9d5e5f6090', 'afterSha256': '657e678228dd3372bee1544ea38dd4cae0db83cc2a1d049ec2f77bc5c641156d', 'bytes': 12104}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/Sources_and_checks.html': {'beforeGitBlob': '5598113b34e183ecdd94a13a394e797b0bb2dfe6', 'afterSha256': 'dc2bb0e06c96e3c684b1b14be21beb06d7c670c4a7b52a492e55c04d1a6469b2', 'bytes': 669}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Knowledge_Organiser.html': {'beforeGitBlob': '8441dcf0a18e596c478ce075025f4f3a7b4e34f1', 'afterSha256': '45f2e1ea5821bdd0c38b2bb8c90892ac756f615ab513d3fc1825f5bc4eb6fd01', 'bytes': 1648}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Pupil_Resources.html': {'beforeGitBlob': 'd5b464885f0dd3be11dd75edc9e37f3e26b50f07', 'afterSha256': 'b18e2e2f1060d64dae749ff634b941784006311d231a1560d40143148c8683c5', 'bytes': 12563}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/Sources_and_checks.html': {'beforeGitBlob': '01e455fa3a1692bc2f7fcb9548042e45073651e4', 'afterSha256': 'fd389ef2d42c23947542fdcef14250c7f080ef637a5c46fb7a077ed2fba94ede', 'bytes': 669}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'b9aeac988146f75b9c0e31a861459e701258b684', 'afterSha256': '4654ee16846c43034c89c0ba26a84d0324d3f7e77e7053233c0ce474da41d416', 'bytes': 12061}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/START_HERE.html': {'beforeGitBlob': 'c66691e9f97d09b42625f13dc6a2d9f2101ce543', 'afterSha256': '297f2674532d5d3fb1673333c23afa07a6b99a906498330063e6e8c896b49ae4', 'bytes': 10756}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/Sources_and_checks.html': {'beforeGitBlob': 'afc27682ea6d817654bc318a5fd293df781c2cec', 'afterSha256': 'fff2824ac1fa482b7f6640b667be548c56648aa80c9745d1a5ea81871514a2da', 'bytes': 17717}}
# END ADDENDUM_3_V3_EXPLICIT_TAGS REPLACEMENTS
# BEGIN SUMMER_1_RESPONSIVE_RE_DELIVERY REPLACEMENTS
SUMMER_1_RESPONSIVE_RE_DELIVERY_REPLACEMENTS = {'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Pupil_Resources.html': {'beforeGitBlob': '0f902d1ee834bf3643bd882d3ef4bfd96dcaa26e', 'afterSha256': '89990eb982ab3deb714ceb90bc58d4095aa52149d22b2e8a8092e85d1408dca2', 'bytes': 89525}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Pupil_Resources.html': {'beforeGitBlob': 'a2c32efbe6e0391ce5f1d6bc27b6d4a9db515668', 'afterSha256': '100ab6a30ce901bbc8fb3fada5584070512cbcbcc942b9346dd08c4ac1e277f2', 'bytes': 138189}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Pupil_Resources.html': {'beforeGitBlob': '571b626723c7760eeeb94070c6f1de1243c76d15', 'afterSha256': '0f857523e0fc30079aa29ce4692ef0c9d3fc8acbea81c7a100517940fcd4858b', 'bytes': 114445}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Pupil_Resources.html': {'beforeGitBlob': 'c85f39b9aedaadb0461bcb8310dd38b88d9e0571', 'afterSha256': '01ca55af085df21e5098f50624e4f46d6261cad627f0e7400714e0723e4be1f8', 'bytes': 215062}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Pupil_Resources.html': {'beforeGitBlob': '0c596772f0d2d7271cbdbd315bad62904b79b268', 'afterSha256': '5d5ec53e4dd803b6553815487ba543d540b975676d3ec9cccbec3959908c4dae', 'bytes': 68346}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/CHANGELOG.txt': {'beforeGitBlob': 'd14d83c137e448d30f2461c0e8643586156f095a', 'afterSha256': '2733da52983532a309738468a0b7e9902025cb9e18018059f5c33a39fd538a62', 'bytes': 18984}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '96ad49f10c44bb71b46de107b1e1643bf089093d', 'afterSha256': 'd3dcbb3cfc7817884b0aa84b55b9c531cf33fa39206330847f40a61a063ea112', 'bytes': 12002}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/START_HERE.html': {'beforeGitBlob': '615f85761fdf19827a8351063a1e5e93bfcd085c', 'afterSha256': '96e3afcf562a827dd2b235d022748b5b53b59adff43d64d5dae3c39e3ea830cc', 'bytes': 10281}, 'Humanities_Teesside/GROW_W27-W39_2026-27/CHANGELOG.txt': {'beforeGitBlob': '18fdb9f0e99cbc9bee0f273a1906f7e187b1f461', 'afterSha256': '68feec6a79029a747bba6a78aab55c196e13a21631c2cfa068f3be1e20f0f2bc', 'bytes': 21398}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Pupil_Resources.html': {'beforeGitBlob': '3ef74d51bb466c27f392e7e1de28eb6abdcc675f', 'afterSha256': '7c13f8cabbc820a97de601ff128bb6153f99821051053edd9893b07f183b4306', 'bytes': 389819}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Pupil_Resources.html': {'beforeGitBlob': 'ce229f6dac35896cf37c4a9f8e7dfd297538366b', 'afterSha256': 'e87732ae765b20646256cddfb5716cecb70fc04d708c7d63f5ff695021bd5701', 'bytes': 75956}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Pupil_Resources.html': {'beforeGitBlob': '47bbaa08a76dfb622032d92955608c6f5f570b1c', 'afterSha256': 'c0ec815f418dfaef8e1f99e2e4adabf0bac2b3db1edede34bd2cdd473da16fb8', 'bytes': 81653}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Pupil_Resources.html': {'beforeGitBlob': '97841ae86f657706fc6d11acb2090b579ee2e68d', 'afterSha256': '9f1dc7c4b3541e25828b5bc2d989ab6e473e2e2fcc1e6e56bacc34677b458f18', 'bytes': 75325}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Pupil_Resources.html': {'beforeGitBlob': '00b0cb11d0aae3e800f90d8f3ed2d528fef4416a', 'afterSha256': '5f7e4d6dbcfab0e85dc5651a98e7fd63a542bc1c34f453c21397b4e95b8d3991', 'bytes': 122165}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Pupil_Resources.html': {'beforeGitBlob': '2d1667ffd99a180f6a2ae3432e81e62614fdc3ef', 'afterSha256': '09f8fb65218fc8cf4ceea14efcbd7d33addba1dc1d629913db16612ae75a52ea', 'bytes': 84949}, 'Humanities_Teesside/GROW_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '614bfd474c2f700b824fbf4da183b083f1596528', 'afterSha256': '38c2bf84c48a0cfb4f0ede2e069e63a586d77d4a33df9a27342ef9edb3f250f5', 'bytes': 11544}, 'Humanities_Teesside/GROW_W27-W39_2026-27/START_HERE.html': {'beforeGitBlob': '989375f10565e7c6cb266b6a95c90987dc8bc237', 'afterSha256': '7d653c761494c58a997c9984850da495c8040348d1c09c1473e2a840cba2be27', 'bytes': 10698}, 'Humanities_Teesside/GROW_W27-W39_2026-27/Sources_and_checks.html': {'beforeGitBlob': '386f8811f7e140c3a4234ad5e34161c6182592e8', 'afterSha256': '587e8e655bf20804a54d3fda8139564bfb7c73b1b3eeba5fe15ac975765baa79', 'bytes': 8344}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/CHANGELOG.txt': {'beforeGitBlob': '45f6c729c141cb4053ada6548e71721be0e166fb', 'afterSha256': '9b409ef65c4e2fde23a6174ff711f3dee859db7f2d24424839dd2944c7796935', 'bytes': 20773}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Pupil_Resources.html': {'beforeGitBlob': '7593e9c91b1c37d1c7555262435298f7515ab26b', 'afterSha256': '3dd0da529309e3f63495194be6906c54aacf05b207e8075a1845902d383e316f', 'bytes': 14308}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Pupil_Resources.html': {'beforeGitBlob': 'be53097722b1f73112db6d918973c86b79d90d68', 'afterSha256': '6607f47e85e8c21914661812faaa7b3092327884cda7612666a347dde61b3743', 'bytes': 12604}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Pupil_Resources.html': {'beforeGitBlob': '205ed70620d41ed361c74d110b3a9cdc1d595156', 'afterSha256': '9ae1089bfd801b77430d72897651eaba4410d7363d5eede82db6bfbd7e659f98', 'bytes': 12976}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Pupil_Resources.html': {'beforeGitBlob': '05cdbfa7e319344d1d5c2ccda121634fa1a07b3e', 'afterSha256': '685ac2587f5e0abfd2c9f09207542b120b20b9b3c09074ef0f569a2692e0e741', 'bytes': 13094}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Pupil_Resources.html': {'beforeGitBlob': 'c00860a2a47120b9925ab7ee714e3efeb4834e97', 'afterSha256': '7bc5cb3771c7066972a8cac7d9a62a29721035b7a513026d8a17db3b531a0ee2', 'bytes': 13038}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Pupil_Resources.html': {'beforeGitBlob': '6a634c85d8426657aa1df96ef19d7ea3e5fdb5b7', 'afterSha256': '5702eda2b9a723956e37be0abff9b71d36880bb2bffac705cc19c9d80d2b7b3a', 'bytes': 13497}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '84750c980d3bfa664bca7f75afdbb62d25f20649', 'afterSha256': 'c47e9650a266be277ae29dca3c7d82f9ece0098cf5ff15a7a165c396f455478d', 'bytes': 12061}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/START_HERE.html': {'beforeGitBlob': 'd884412b745e9cce872d9a487fca20b1f4fbc155', 'afterSha256': 'dd07b91e212e71e863c96d9a31d489a68f5ea3ec529f50e96f6125251e48eb8c', 'bytes': 11690}}
# END SUMMER_1_RESPONSIVE_RE_DELIVERY REPLACEMENTS
# BEGIN PASS_C_AUTUMN_2_BATCH_1 REPLACEMENTS
PASS_C_AUTUMN_2_BATCH_1_REPLACEMENTS = {'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12_Follow_the_warming_chain_Classic.html': {'beforeGitBlob': '8407910102f0f94b31f2dbde60f4ef8f920f3552', 'afterSha256': 'c7cca58d2e44d96bff35584a58112c2e1cf65355e4317a57c6e7c49909e9e9f9', 'bytes': 1200163}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html': {'beforeGitBlob': '48fe4b0fe35781bd82988d0c79586c1539759292', 'afterSha256': '4568d8d3e033b9f5a18ae695c0ebb37166872cb7aea393881db0e75f80fa03fc', 'bytes': 1275783}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html': {'beforeGitBlob': 'c7bfea943e437482b299b1d4a749215190114724', 'afterSha256': 'aedc03c500183da66e23d217f67ebbbd1227c66ca0f1b043304859c5b6175f9b', 'bytes': 651275}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html': {'beforeGitBlob': 'a9ab7864737848911870faf0ec6374bebd299512', 'afterSha256': 'c8f4a39a7e4ca27a806ef317cb01d702ee61f5adb0d3ca3630af059f5a07d38f', 'bytes': 652408}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html': {'beforeGitBlob': '858d060a4133c137386b04b9888a8aacb3c43ef4', 'afterSha256': 'd7b1e0387c75b03cab9aa205b3795ff2be1cb60aee342a705d44becf2e8be595', 'bytes': 383033}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '3691e540d0203c392c6336988504f8210f25643c', 'afterSha256': '4d2785f94e16255a8e75b5887ba0c7348d80c64d06cec9521113e00b3ee35412', 'bytes': 504}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L1_Genetic_Condition_Research_Introduce.html': {'beforeGitBlob': 'e229772d7c59d1412523efcf1ae7cb740ad397f8', 'afterSha256': 'f56eb5b9bd6e7d946e3dfa642bbf2d5aa175b7d4c42c953955842c9ecd618bf2', 'bytes': 652400}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L2_Genetic_Condition_Source_Evidence_Explore.html': {'beforeGitBlob': '93d35d7a17b11914417abb40382e0f4895595760', 'afterSha256': '59fbcd12d08909b36b07fa75110c3f85ff6b45553393c3338c8691ea814c145e', 'bytes': 653913}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L3_Genetic_Condition_Presentation_Do.html': {'beforeGitBlob': 'fc0065fcc1237edb03a7a632ab9a75aa316dd580', 'afterSha256': '80743f2556a21d0e712e00a7d20519870b299fe6f324506c2da12d15b4056d95', 'bytes': 654669}, 'Science_Teesside/Launch/W14-W15_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '9e6263453507c643ff05dc0804a17ddbc2525439', 'afterSha256': '4781617b66baec3fd3951ed417e7360a445bc3d64835e8647cd74c5537a99f8d', 'bytes': 524}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12_Zoom_into_genetic_information_Classic.html': {'beforeGitBlob': 'e3416748f168aa224efac09f736cad35ce5efaf0', 'afterSha256': 'af1941cc3f804df97f4e4d849cf64e97e85fd926d902e5a911bcb6d54dd7b3ca', 'bytes': 717484}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L2_Punnett_Square_Explore.html': {'beforeGitBlob': 'becc1c7c15a80e895a5dfa78155a73b8a18af1d3', 'afterSha256': '29e777bc072ee5c27c89204b3a18d5eeeecdff77a2c16470ddbf218320310014', 'bytes': 594440}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9_Copy_separate_divide_Classic.html': {'beforeGitBlob': 'a7a53853b4e06f9032c22d1a0dbe28ffbad379e9', 'afterSha256': '56c176e483ba44e30455b206269e81afc2b32e93e2bcc9a640aeb8a53057ffef', 'bytes': 685695}, 'Science_Teesside/Launch/W8-W13_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '6186a3b6fa17aa0340668f44fb9a27ec1f4418bf', 'afterSha256': '694205a0dfeb831f096d9dad923aa5f83762ea36193808918a01e4b636428907', 'bytes': 2590}}
# END PASS_C_AUTUMN_2_BATCH_1 REPLACEMENTS
# BEGIN DLG_1 REPLACEMENTS
DLG_1_REPLACEMENTS = {'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Lesson.html': {'beforeGitBlob': 'ae5b5cf0e09f1cbde362c5de000d62a00c4518f2', 'afterSha256': 'f9bdec1a3d49c8fb542f7b02cfa104141e2be8fb1f20bc33c8f6d55a155c4b61', 'bytes': 596583}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Lesson.html': {'beforeGitBlob': 'c76a2fd3c705f8c4848e250f24edb7271b3515d1', 'afterSha256': 'f5eea0753a495ae58ccff58e0735267213311a758ce88eef4c1e7658edd019df', 'bytes': 571970}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Lesson.html': {'beforeGitBlob': '21b96f19eb7162f76361a43d3b021386480e3839', 'afterSha256': '27d31db816e1182bacceb64617aa12c34a51fd5bd36352e8af20cff6625a37f8', 'bytes': 649905}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Lesson.html': {'beforeGitBlob': '0d6851a2ec50424fe18223ca325d20e758fb85a8', 'afterSha256': 'bb4774e6f3884bb28e60e04b53e389352d99676fa32be5f7c772920b445f15a3', 'bytes': 539597}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Lesson.html': {'beforeGitBlob': '71b09413e60a0d17a4af3ebd3b74772955e4fb8c', 'afterSha256': '7b8a8b230e7f14179dba20d940c77e62d21c3e5394cf1151bb519ce01d08fae9', 'bytes': 594075}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Lesson.html': {'beforeGitBlob': 'b812deee1b3f46c4ad25ddc8dc5b34ac724c8bb5', 'afterSha256': '75cea8d6a9ce58156a66638e390393c9fb652709daf9de4a6563e3c422936f55', 'bytes': 542086}, 'Humanities_Teesside/BUILD_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'd7c5e08c11c6fed3e7a093769427e9727592ead2', 'afterSha256': 'd20040b4ef79cf5d9630c6387c05240d1b66ec2d4a26526845697f08f872e643', 'bytes': 12002}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Lesson.html': {'beforeGitBlob': 'b8caac76b03ff07e545ff4f726b60b95a3cc6d0f', 'afterSha256': 'a786070e48b2c3fb8fd0fc976a9d690e13f68f431291e1bbed6fc387c85b2e67', 'bytes': 953411}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Lesson.html': {'beforeGitBlob': '9e27c25b13e6a098ce7844848c1810175c2c8f2e', 'afterSha256': 'cbdc67e1e498f464f65cb66a7343133a98822441f7068b355d81c9d7ae50ef14', 'bytes': 585472}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html': {'beforeGitBlob': 'acc3d0de290c4646b04bd8c5b99943a56e355b2e', 'afterSha256': 'cf482ade46f87249adbab42b9e0a2998fea140179de1cff5f779466fdce3e5e6', 'bytes': 638733}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Lesson.html': {'beforeGitBlob': '302544b38fd5ddafc8cab6471fdcdf1991c80f91', 'afterSha256': '63ac556c4567a2188c253c8986448d0f2c762bf528880cbd2102d1acd4257c00', 'bytes': 525078}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Lesson.html': {'beforeGitBlob': '446dc0ded8fab18b840e2602d2f8f68969047e79', 'afterSha256': '0268feebdb8b404c16d392626ba2bb99d636f4f67f09ef68687079c085cee9af', 'bytes': 693256}, 'Humanities_Teesside/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Lesson.html': {'beforeGitBlob': 'cf4bcf8eca586b9f5fcffdd6b9244dd87440fe69', 'afterSha256': '84cc8979fde68076a8254971942a8c43d60c61adde9cc0830466a976273cff0f', 'bytes': 779667}, 'Humanities_Teesside/GROW_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'ac8ee646ad1c1bdd433593136e5561f7964870d3', 'afterSha256': '7b59594b27b8d5369b90b726784f70275f2238130d8e10c3461c7f6abd5472f2', 'bytes': 11544}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Lesson.html': {'beforeGitBlob': 'a84549992bf03088ef324d42e082eb2a97e9d1fa', 'afterSha256': 'd688631fd70176aa795c40376add227c8c111ec64971b9031b6badaa8714e45d', 'bytes': 563168}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Lesson.html': {'beforeGitBlob': 'a39815c85c1ac15af8893b10ec33eb56a6f6000b', 'afterSha256': '466debb38ce5e6acdbcdc3a1d08f4189eb2f0b7b49d1555ab6c92cae41108289', 'bytes': 554232}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Lesson.html': {'beforeGitBlob': '762d26040b4720a9207454dd04b35e93cb8f308d', 'afterSha256': '14e6c922028e16b3aa377ca54ab1a83a308e7dca68a712891c285e7287bd2dff', 'bytes': 577206}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Lesson.html': {'beforeGitBlob': 'dea79e180ce22f20e9ea877d5f8806fbd76deecc', 'afterSha256': 'd5d9f406d55acd52662b011552ecba5ad560e75f7897111776c6b033dd525756', 'bytes': 588501}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Lesson.html': {'beforeGitBlob': 'e3f14aa926abd5cf1c40b0bce1c42877fb3ae2e8', 'afterSha256': '531974067ae1f24da64d629e96f1695c4d80e52e188a911c5d650d1523d367d9', 'bytes': 581226}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Lesson.html': {'beforeGitBlob': '1a1c2cf00663f6476fa2f86d4e072c6eb76b8b43', 'afterSha256': '05b17089118b1e8d8d9491398f4477f224df4bbfd0b6c706aeac8be674140c97', 'bytes': 570949}, 'Humanities_Teesside/LAUNCH_W27-W39_2026-27/SHA256SUMS.txt': {'beforeGitBlob': '0708e018636282cedc2152fc219e9d765c87267b', 'afterSha256': 'fbb067847fa74fcf9160deec871d88fcaeefc91ed2368e44b70516cf141cae44', 'bytes': 12061}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Lesson.html': {'beforeGitBlob': '49eb4ebe9d267dcc39ca922f2b90c5991b18acb7', 'afterSha256': '5e749fa9c031c862063a74868c2caf40159038d42d95762e5f921df02fcb86b6', 'bytes': 469537}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Lesson.html': {'beforeGitBlob': '67ef1a2fa235fbd5301959255f51de715d380c57', 'afterSha256': 'aef101588154641db86f4727c82b56ae5b86fb647de5168c0c1cae4dd37d6cbc', 'bytes': 455513}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Lesson.html': {'beforeGitBlob': '938a296340cd85637c7375d68579d78ef80d13bd', 'afterSha256': '11fab8a9f60ef8aab08c57bc24ed48022683843abd5f629f502ce4210617b165', 'bytes': 448317}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Lesson.html': {'beforeGitBlob': '69005eb83844731f72fce3c3e25fa3d6adba1e5d', 'afterSha256': '65061c1794f886fdc85a5794679d7b97c02975ad4469a271e88187cba11dd35b', 'bytes': 1215356}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Lesson.html': {'beforeGitBlob': '2888f5e4fab56841721762582376223bb0c6d815', 'afterSha256': '1343ec63debc307f4e4d6060bc8085b81cbd7c4d658e7fe2305ea8b61be64709', 'bytes': 448490}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Lesson.html': {'beforeGitBlob': '7bf9ab80bcd7dd53dffe14fd3af460800d25c750', 'afterSha256': 'f45f74070d702d7a7c92f484dec07497292e1efe891eb972f932ad66899bdf73', 'bytes': 448412}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Lesson.html': {'beforeGitBlob': '5eb80a888186d4770a4ac92078c7363a4984999f', 'afterSha256': '95606aed9b784c63b01be551b189c72f9d35acce5aeaeab80e986e835396e37a', 'bytes': 476876}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Lesson.html': {'beforeGitBlob': 'a6d89765df98fe0072c709d26db19b23e67d8a96', 'afterSha256': '12547928b72ce39f01ebbd0b8a73845ea16ff6c4cea9e8f506a91283d0825e78', 'bytes': 425640}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Lesson.html': {'beforeGitBlob': 'd563fe3a83bdec4114aa26c61245d39c5bd036e6', 'afterSha256': 'ea1d3168851dc8ee8de24a81d9461af1dfae6040a9f7f6b789f798fd0e43d20c', 'bytes': 454980}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Lesson.html': {'beforeGitBlob': '89d8049e5ad7fb184455a55d4f529a63fe20ce77', 'afterSha256': 'f0438703d83f2cbb79cbab266060928237cc8f593cf65e5b80606f49c27112ac', 'bytes': 464956}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Lesson.html': {'beforeGitBlob': 'd84130499c8f3bc37b5a990cde306528094691e1', 'afterSha256': 'c89846f9151e61fa2fd4528a7ca765c6566b06b2d02db19aa3a91ebd75b860cd', 'bytes': 444815}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Lesson.html': {'beforeGitBlob': 'd75b0727b5df17c400039e016670fbe13c13c54e', 'afterSha256': 'a9be509c21d3c04540637e6ae9c1efd5b7a3e11c23c674f9bb78ed76f661ff4e', 'bytes': 457879}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Lesson.html': {'beforeGitBlob': '5d3878c4db9cb430ce73c3192f5df66fa3210cfa', 'afterSha256': 'd87a3364f79087aa1d321b22473fb386e4b4ac8b6f2e1c168f37ce22abf8e0f8', 'bytes': 466077}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Lesson.html': {'beforeGitBlob': 'fe52b0484c7b815f1520ce1c65e6512a2b77f1a7', 'afterSha256': '945762ea50fad2218df086d19473de3de4b4e6c146ab562e4b8d35e60b32fbd2', 'bytes': 476055}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/MANIFEST.json': {'beforeGitBlob': 'bd8f3c518cca38b32116469a67c2de042c3c46de', 'afterSha256': '6cd175cc1cc25fcc69dc579e7b1750545d7fcb1cac849196ca72134b8708b766', 'bytes': 19126}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W01/LAUNCH_A1_W01_Lesson.html': {'beforeGitBlob': '391e27b2fe617529ca8315157e9f922ed93d7a26', 'afterSha256': '5f1ab114ecaec7c7a8a56c576af7a8f14f70ff70866465926e55a4aa98ef87ae', 'bytes': 797605}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W02/LAUNCH_A1_W02_Lesson.html': {'beforeGitBlob': '42e4797e801aeb47abc28057ec2c186935382e5f', 'afterSha256': '9055d34c0069bfc0a19179370164133e4c35f5e50a5f5cf77e9ba18fe84666ac', 'bytes': 889975}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W03/LAUNCH_A1_W03_Lesson.html': {'beforeGitBlob': '64bcfa4f6ef5c7234fd0254ab71bcd4f3fab7936', 'afterSha256': 'b093859c48180274b680f1e35d4afb78a309d1099d48fe6fccd51b461d3e232c', 'bytes': 878904}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W04/LAUNCH_A1_W04_Lesson.html': {'beforeGitBlob': 'f937d0cb5b63748e95828f7b22492fa79da82fc6', 'afterSha256': 'bdfd44034f439ae5181c17bfe78e6747af340bb3d15fb0739e99c9de75aab49b', 'bytes': 827995}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W05/LAUNCH_A1_W05_Lesson.html': {'beforeGitBlob': '599b53efb572bc8f36f594dbd542dd7fa5d31f9d', 'afterSha256': 'f95a2eb84b151fe03a0a5fad3a98bcc5aafce8f83c7677b8c8681de3b5a0d7af', 'bytes': 731208}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W06/LAUNCH_A1_W06_Lesson.html': {'beforeGitBlob': '0d130c3e6ddbc2427bbe06943072a4b1154cb979', 'afterSha256': '35e73d60a56b324de4908b19b16522f39defcc8dfba5cb0d90abb2156bffe006', 'bytes': 838040}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W07/LAUNCH_A1_W07_Lesson.html': {'beforeGitBlob': '2859e8697180313fb0059cd3c74a6861d86f81f9', 'afterSha256': 'dbc6f3109dd6265e517cb0566e1f6de0bf5b784bbfea423df5384981059382de', 'bytes': 959111}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '5495f17597916f59cfe1c6ed6ccefb17df02835a', 'afterSha256': '480587877c978b6792d8107131157de7264cfc8b38743ae3eba36abf36cc66c7', 'bytes': 11182}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_A2_W01_Lesson.html': {'beforeGitBlob': 'd0b5cdca7c637c0f0fe79d9a6f6e24c6c02917bc', 'afterSha256': 'a1c16ce481a960e243e89371550357640648760cf1d6e5dd0d45b89be8d85bdf', 'bytes': 736893}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_A2_W02_Lesson.html': {'beforeGitBlob': '31ed680a300d4eb57ca0047db9b642000d2b5f8e', 'afterSha256': '8e6b2f73511aaa359a5605929757ae19a078c6e01584ffdef7d4f77b68a88c9f', 'bytes': 1042595}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_A2_W03_Lesson.html': {'beforeGitBlob': 'd58457e4bc6995e9243363ed4299e183527a5a4f', 'afterSha256': 'd40fe5863e5cdaaf70ab0ffdf9f4829377e2d35b74a9d5e455385e7a232bc9c8', 'bytes': 799805}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_A2_W04_Lesson.html': {'beforeGitBlob': '66a0168256f8e1e08b093a71f7563a7aefd61172', 'afterSha256': '2b304ba13036e4d205e6cdaba6c7778e84b8ccbc42d0367ea75fe13db225e7a0', 'bytes': 756512}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_A2_W05_Lesson.html': {'beforeGitBlob': '38daa2c3f7d53ba647b4fc840d9708a698aa64f8', 'afterSha256': '79900fa6d3f0d3821436e68baf359d47f039e7038e8ec8abe5b1ade0695a0ac4', 'bytes': 789834}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_A2_W06_Lesson.html': {'beforeGitBlob': 'ac9d4894e56ba418e12e6d63a3b2254344d23b1f', 'afterSha256': 'bbbf137d46c3aac3fb11ac1b82f3bd425e949953d95e2184590b54a854db159f', 'bytes': 741147}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_A2_W07_Lesson.html': {'beforeGitBlob': '5a7e4f00e5e3932ecb45aa57767f889dd13fd672', 'afterSha256': '495189e883e2a78a6e24fb3a8005aa4866f5e382fd0afa793d9b48e0b856fd4c', 'bytes': 861007}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '9699be1d94695f5a8461f8e49d4a61dca61553be', 'afterSha256': 'e02a5e9c69a4f89c89db97f9cfc021f142ca391d7ea3ed063c597d9090c934db', 'bytes': 13652}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W01/GROW_A2_W01_Lesson.html': {'beforeGitBlob': 'c133a96fca38e84438e22b69ba68d5335f42851b', 'afterSha256': '15e63b281875f6d62636a9b619abd954526d6c31318687510dbab09271e91e39', 'bytes': 986561}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/GROW_A2_W02_Lesson.html': {'beforeGitBlob': '37e3ad40c15a243957317e50b131524079878cd9', 'afterSha256': '541f7d43d5ebf0cd057b78286ff682bcdc475cf44b216b0f2332d1f713e87cf9', 'bytes': 692389}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/GROW_A2_W03_Lesson.html': {'beforeGitBlob': '135848178608848a0c7e2332d4e71f50ed322a85', 'afterSha256': '663ff01c19bde7cce9cd46596b2b329e167501cdff570f9dbae6ca1fc9ee12b3', 'bytes': 914338}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/GROW_A2_W04_Lesson.html': {'beforeGitBlob': 'ac3ae7cd17d5e7d50ba3b4a18d70f5aca0279bbf', 'afterSha256': '0395590993c36cefd35e3f8ad9b1cb9220f60f09b9eebf3cabfeffcc64e5f735', 'bytes': 1075446}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/GROW_A2_W05_Lesson.html': {'beforeGitBlob': 'cf4d319324904a85a23b1970c3f5808ed71d5620', 'afterSha256': 'a2b7242f2c720312b8d75fd3bd3fbf61d5d79df41ef9aca03060e8e656cc621b', 'bytes': 1026463}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/GROW_A2_W06_Lesson.html': {'beforeGitBlob': '37c0497a8f897b417c760f995ec742c827d57b7f', 'afterSha256': 'a85daba32d269cfae3347c0a731a1778560bdcae0e0388538f88863ca2601a6e', 'bytes': 1210664}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/GROW_A2_W07_Lesson.html': {'beforeGitBlob': 'dcaec80f0c9e8439aea0d3f80ca87c81a25a8924', 'afterSha256': '5124e543efd5f8452ef18f7cba460aa230dd2d52681107de1e59f0ef8f6f7d65', 'bytes': 929253}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '16efdd085b39fd8292cf224e4031ac6e89f50f01', 'afterSha256': '3585f3c2b25a067ec757cdcc291a8c62971f5d6c3173f2dfb944de4525dd370c', 'bytes': 12330}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_A2_W01_Lesson.html': {'beforeGitBlob': '4b089b60e1083be609c3e7769d7a006d6d47c061', 'afterSha256': '5dc5be4aee51879803a1da926b42b222d24c9993472128cd0c3d812ff32d5e9e', 'bytes': 786414}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/LAUNCH_A2_W02_Lesson.html': {'beforeGitBlob': 'f9f443c27a85577b6403e1883769252f5b556ca7', 'afterSha256': '6cf0bf848a2a0bab2581e86c1a0536a759713214799177947e59018a432fca46', 'bytes': 1159344}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/LAUNCH_A2_W03_Lesson.html': {'beforeGitBlob': 'b016851cf0e3b8b476c39cf93dd628d516c620e1', 'afterSha256': 'ed798926fc9029b1e89633cf6aef8ad0b539fd0f85e1bd46b14eaef6ab70816d', 'bytes': 903765}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/LAUNCH_A2_W04_Lesson.html': {'beforeGitBlob': '51cebe1920bfc24c426f083c3da777f20843df2c', 'afterSha256': '018a35512e73b58a24506983e7f33e502dc03740001f9c6fe07176fc2d62f1d4', 'bytes': 1047990}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/LAUNCH_A2_W05_Lesson.html': {'beforeGitBlob': 'e92b09bc92814516540ca3407ea8d28577c5b377', 'afterSha256': 'f292ac63fba414206333dffd3869de2657c37036bbfa757de2c9a0eee368760f', 'bytes': 911357}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/LAUNCH_A2_W06_Lesson.html': {'beforeGitBlob': '337b6727c10dcb80af1efe343b6c5d4e3b694c3e', 'afterSha256': '14727c333c6cefd5f7131733cefca33d66c78affec110830e2c42791f1c759f7', 'bytes': 1029380}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/LAUNCH_A2_W07_Lesson.html': {'beforeGitBlob': '0d08aae901c474d84c3aaf6e6185e869ba6e3eb2', 'afterSha256': 'facb9ac110bb65f343fda3d2f13bdf384272a40b3f8be62d96d135817b2b7e47', 'bytes': 836590}, 'Humanities_Teesside/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': 'e3beaf0200ffefb0118cdeeb553e956c064e0417', 'afterSha256': '7e3db22481967e3bf3f28f72e33e57abc67f11e3777e60f447151e3bf9f36ee0', 'bytes': 13133}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W01/BUILD_S1_W01_Lesson.html': {'beforeGitBlob': '53101d9086a4c284153f1ada3dc0bb92157685ec', 'afterSha256': 'c14a2be568718dfd1080a6bcf64cc0613734bf058f034cec5326e2ee64377e42', 'bytes': 671144}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W02/BUILD_S1_W02_Lesson.html': {'beforeGitBlob': '243fbbc48168bf73e2ecf3e9107b6a4705a45b66', 'afterSha256': '5e854d667a77bb6edce02396d0f541315dee5ca17e092e4b5f75657f2961d274', 'bytes': 745217}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W03/BUILD_S1_W03_Lesson.html': {'beforeGitBlob': '9aa735f68c74a6ae7eab843a4148b511db316595', 'afterSha256': '072dcebd5ed8117b4af623e280afdbebfebdbb8223ab4b8c4caf823e02200431', 'bytes': 1202441}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W04/BUILD_S1_W04_Lesson.html': {'beforeGitBlob': '869ea490d491b24b3f04469dc4540433f965c91e', 'afterSha256': '2e3d23014e4de69e482bae679a62d1697075d9eea49d13166dcc3251c195dca1', 'bytes': 1257784}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W05/BUILD_S1_W05_Lesson.html': {'beforeGitBlob': '585948b1c967cd10dbb5a3d4659ce83140b29e3b', 'afterSha256': 'd98b79c3b7e05c179c61fa5d58a0a48dbbb73d3ecc3118de2867a2bde935910c', 'bytes': 751111}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W06/BUILD_S1_W06_Lesson.html': {'beforeGitBlob': '5ee72511573e01307cb99f0123eaf226d2613193', 'afterSha256': '987557d14a2633201d21a15aac34f69adea668db851595ed32e2be24edd04201', 'bytes': 1320825}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W01/GROW_S1_W01_Lesson.html': {'beforeGitBlob': 'a8fc160d7da33977ac1db0bc85697f46ddba0e66', 'afterSha256': '780dc8b6cc8e25609c53491d885bbf2a3c14d476f151483cd0aa62fcd8822fda', 'bytes': 966726}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W02/GROW_S1_W02_Lesson.html': {'beforeGitBlob': 'd23259d167fd29198d6daec5fa1bee5280deef0c', 'afterSha256': '519c40e2567bee09bed0fb19edc0dd206570ca9d65e87ef4f2f32525dae5d1ab', 'bytes': 776216}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W03/GROW_S1_W03_Lesson.html': {'beforeGitBlob': '58c6ea1aecebb7d4f690176d559955485a39f4d9', 'afterSha256': '1a0c31b74fa1ceeaeebff8ea10141c202bd34ebf9aefc68a281290ac4d742df9', 'bytes': 756164}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W04/GROW_S1_W04_Lesson.html': {'beforeGitBlob': '312fc470ab9b039114f30ce8d75b424bd55002e1', 'afterSha256': '8b609a82bdcaeec34ed7e837af2466367450ff7ba4ce57e4b194b482cbe78458', 'bytes': 740957}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W05/GROW_S1_W05_Lesson.html': {'beforeGitBlob': 'b18a0399faac2106830362322080a4b48c6c38e1', 'afterSha256': 'dda4d977e4499d9d6bc98b7ba1c3eb8a9463a1744ff3a0a81d9782c337a30169', 'bytes': 1027548}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W06/GROW_S1_W06_Lesson.html': {'beforeGitBlob': 'e43447563dcf9e1e82676dd89c65e20b957fc4fb', 'afterSha256': '6222620e123c87e00fe1004cd2594c070e26364be0666096c4bb7997ebc03cb3', 'bytes': 746653}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': 'ddcf1434c3b7834ea5a21bc92fce9a7dd9ba82df', 'afterSha256': '8fc70d36d275598845d5754a1e0973befa82012b39630ebbed2140e40309e553', 'bytes': 20838}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W01/LAUNCH_S1_W01_Lesson.html': {'beforeGitBlob': 'd2658c6a32704659ab19f14ddee1ec01dc5d4aec', 'afterSha256': '55b570e7070c1f9af8b570cd5fd5d4613c7135d1d6c1bdf8066416799da003b2', 'bytes': 820898}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W02/LAUNCH_S1_W02_Lesson.html': {'beforeGitBlob': '72b2805863f9423f9bb8a0bdc9fe2f39f2275c68', 'afterSha256': '2578e4873ac34d541c8269174c1dd84b7e11e928240115a778d5b01719f39bdc', 'bytes': 937005}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W03/LAUNCH_S1_W03_Lesson.html': {'beforeGitBlob': 'f6ee8f93c178468c76ca1097db0a53c548425c10', 'afterSha256': '3300ac68f11af9cda9f161e02031f18c5737e0a06f453f29e2565ccca5c39c01', 'bytes': 824668}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W04/LAUNCH_S1_W04_Lesson.html': {'beforeGitBlob': 'e8eec37975c5302f62d0eb4659e8cf0407c564aa', 'afterSha256': 'fb4904a633b51bd7e1b118415a373f241b2fd96e048c1c2dd0f4e51d6647f42e', 'bytes': 855751}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W05/LAUNCH_S1_W05_Lesson.html': {'beforeGitBlob': 'c4d0fdf44de05f8b898237b84cf9e9d335d1a9c4', 'afterSha256': 'ba6e045a160aa8df7ef4cf2233d30451e725eba82b6eba3c5aa550d47372b863', 'bytes': 876030}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W06/LAUNCH_S1_W06_Lesson.html': {'beforeGitBlob': '854d0ed1d46e86c7658d6a6a834dd4c96b678ba8', 'afterSha256': '226bcb9a46eefcc248521ae4b8ca8148bb1017dc335776b0656c054237129668', 'bytes': 1278263}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '11c64abac04639ddfc643db1b44e8d20b7a15a64', 'afterSha256': 'bc16f31e639bf89b0c4bc14ae07439f5aacf0a646d7f4639a6d66e51bce86f9e', 'bytes': 9646}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W01/BUILD_S2_W01_Lesson.html': {'beforeGitBlob': '2f7bddaea68f5b982e7cafb33dc2683d5e02288a', 'afterSha256': '5ca95456c016e586a970108fd53bbcfb0cf1724db1a7e11907b2c2451ad0a55e', 'bytes': 750377}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W02/BUILD_S2_W02_Lesson.html': {'beforeGitBlob': '6565126d6400d030ecd2d6addbe4e5e426d185f2', 'afterSha256': '72590065a98eccc42d4123b2392c973472f095d87a584c6df0f76503fcadbc31', 'bytes': 763731}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W03/BUILD_S2_W03_Lesson.html': {'beforeGitBlob': 'cb01d5e527fb55318cf3b70aa2cc44c637be3a77', 'afterSha256': '06d731dbc610e50e6b46dfe9f71385beb8e92a268be3bdf8d5399bffa64ae60d', 'bytes': 739767}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W04/BUILD_S2_W04_Lesson.html': {'beforeGitBlob': '9a155a253d42cb7f93cf81b8ffa832a26f247905', 'afterSha256': '4de5f2ef8ff474334ec7ec48307704cc4468655f100a65bffc8b244ac7285219', 'bytes': 769810}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W05/BUILD_S2_W05_Lesson.html': {'beforeGitBlob': '79977c1038d8bed686f4057389e74370cb0dcb68', 'afterSha256': 'db63df0d9e111332d9a6859ba5a8b5a1714ce724f1d847b1314efbd52e826085', 'bytes': 801422}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W06/BUILD_S2_W06_Lesson.html': {'beforeGitBlob': '9950931f084531bfad67d3a7ad1f168809974789', 'afterSha256': '9b54d696d4de412fc6ad4ceabf8bc91b283a405acebf978a566652208d075ca5', 'bytes': 805231}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W01/GROW_S2_W01_Lesson.html': {'beforeGitBlob': '98080a030715bb67efc0605f06344558efbd82d4', 'afterSha256': '9d93b0de8ade11d33abea62f2766664ac7589418694403a2829d375411498d8f', 'bytes': 1120722}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W02/GROW_S2_W02_Lesson.html': {'beforeGitBlob': '76df5737ace615470ae7c8c8037ce00b0240e03b', 'afterSha256': '023ecca14955dfcbd1b13cd8d845ce54e98961add7f9bc104d8283107f5b1105', 'bytes': 888102}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W03/GROW_S2_W03_Lesson.html': {'beforeGitBlob': '693ed773858f5dda40a89a217d26128f6a29bd08', 'afterSha256': '7d95b4c0d60beede6d07eb3bc69570f6a0c020cf102f3f89d721bc24f216e8e7', 'bytes': 834233}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W04/GROW_S2_W04_Lesson.html': {'beforeGitBlob': '8f5a76dab7fb0fcb70dd5373c5f8fa3cebca70d4', 'afterSha256': 'dfa7b5383aaff4c49293fc503ab5a6ee370ce80065c6690ed72c349f8648343c', 'bytes': 970032}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W05/GROW_S2_W05_Lesson.html': {'beforeGitBlob': '83be7d9d1e0ea07d7b2ff32973ce91a39bdbdbc5', 'afterSha256': '698a6096c4c6bcd51bcd3c1066c2b8ad2ce6d6b93b8e45b0e55e8ed6319e3a33', 'bytes': 884242}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W06/GROW_S2_W06_Lesson.html': {'beforeGitBlob': '9b52bc7c539304d5b70803e5defaf411224f17d4', 'afterSha256': '0de35a96243bbad825f4291d4a28561dd14d863ceb5c92206537a58b23c26d15', 'bytes': 977690}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': 'ee887855da3bea1f9034829635716b5f97eb8856', 'afterSha256': '423cf78757820f83ea54bdb970d528649179a719d9fd75a3b059075dbaaeade0', 'bytes': 21890}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W01/LAUNCH_S2_W01_Lesson.html': {'beforeGitBlob': 'd3962b9b2777872fa751b7b407e3a86768f609ec', 'afterSha256': 'dcf1838d414e806b84bcae5df533f9471d7a8b0be0cd2c0852349b64ab866622', 'bytes': 914022}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W02/LAUNCH_S2_W02_Lesson.html': {'beforeGitBlob': 'b615d0488e81e5c6241b1cdf05428286c8040059', 'afterSha256': '6d85a5671d4c7ae280b59cf02cc2b8c593339350807e225d4b7714997b2e4039', 'bytes': 940668}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W03/LAUNCH_S2_W03_Lesson.html': {'beforeGitBlob': '93cbe746667751dd31ccd20889a92bead09cdaf3', 'afterSha256': '8d266858aae0337432f84c456fb0c8a675de36fad06c25d03ee732941da48991', 'bytes': 899386}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W04/LAUNCH_S2_W04_Lesson.html': {'beforeGitBlob': 'ed38decb9d7d38cf32ec58cf71af4f0b52c7e31c', 'afterSha256': '91baee0bb8cad5c48fac86615263c48173496d570df349252dea042463e9d93f', 'bytes': 1044077}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W05/LAUNCH_S2_W05_Lesson.html': {'beforeGitBlob': '7a2130778a889081e1ef501d12409e1c9f46983c', 'afterSha256': 'e93fe22e4ee0db3d7fd05321521d804e3192d7f4f1299c14f42d523a00d284ea', 'bytes': 814857}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W06/LAUNCH_S2_W06_Lesson.html': {'beforeGitBlob': '837d7c21f9d96c94f09ae6dc43eb825d8f0ed183', 'afterSha256': 'd10a5832ac7b86be298e4b08d83f3f426e6731a118287512aa94c2a187bb6475', 'bytes': 914768}, 'Humanities_Teesside/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '4fcd30d805d52243993da56da45adcf35c8fface', 'afterSha256': '50cb5d58839fc4942693a01850a137497a4361bb467a4ee3b658d86793ac74ca', 'bytes': 11818}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W01/BUILD_RE_A1_W01_Lesson.html': {'beforeGitBlob': '0c12d04bdc0494b993115a219d09e7da80baeef0', 'afterSha256': '6120f11ef73139427c72d16455a1578bcd9d41fc758073c43a647322139e5e84', 'bytes': 715883}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W02/BUILD_RE_A1_W02_Lesson.html': {'beforeGitBlob': '606e73b0d9cb0579e4263eff71e9c05c85253536', 'afterSha256': '32b655ec62d74cada8a009ddca5b0f4285abdb48e1c94eac598cb66d51267952', 'bytes': 760292}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W03/BUILD_RE_A1_W03_Lesson.html': {'beforeGitBlob': 'e11408388acf47ae0af9ec039e6acef3f2341975', 'afterSha256': '6ca005d877400b6893caf1b7e793c73f9c206e2fa29b25abadfae9fb9baf9b67', 'bytes': 752348}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W04/BUILD_RE_A1_W04_Lesson.html': {'beforeGitBlob': 'ff0946b7ad57f0cbe71c20fb131a2f5e5e730ebb', 'afterSha256': '90b96500f6edbb3b918b7bfaded3f9f363d63dd7b2e615ec40b7fbb47cae5592', 'bytes': 748781}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W05/BUILD_RE_A1_W05_Lesson.html': {'beforeGitBlob': '7b7499f0763d52eadc598e892054e08e9cbbd87f', 'afterSha256': '8bfead9a8ccd03a143697e997fdb2e571b96573657b3dbc32890c01848c8d7a9', 'bytes': 952373}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W06/BUILD_RE_A1_W06_Lesson.html': {'beforeGitBlob': 'a31d15c4986a47225295198ad823fd9be0f332da', 'afterSha256': '47503b698f9f8e3177adcf855442bd50636ed5c363f19456c22e0800236e5152', 'bytes': 734323}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W07/BUILD_RE_A1_W07_Lesson.html': {'beforeGitBlob': 'dd8e880b4159e20bd4357264d1d2a65c1817f69d', 'afterSha256': 'c6e1debc5ebe82bc0d5e008cbbdac217cd5ffb7b045a6d4fa45d4bed74b0d62b', 'bytes': 931770}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_RE_A2_W01_Lesson.html': {'beforeGitBlob': '64efe1b6266cf8be7161288dac7bc7b8b124323c', 'afterSha256': '51d8023fe37567838c7ef5b0e377b227a52b0cebef8b3f07afbfb1fb1a69394d', 'bytes': 709000}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Lesson.html': {'beforeGitBlob': '70a6eb806a3702f66a98f940ca64f1df7921dca9', 'afterSha256': '52e8974f682baec2f8fb34ebf5d8087b95c03daffe82a1a2c2e7458b9e93bf28', 'bytes': 958825}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Lesson.html': {'beforeGitBlob': '8c8fd58dff8a0b082374f43d9bc84e98e595b3a1', 'afterSha256': '5e4d672e77b78ddaa0204dd6bf0e89078728a71de1afacc18fc278a59d65ad01', 'bytes': 686321}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Lesson.html': {'beforeGitBlob': '34e716be5c46a3a313590e6a72bb5c7549e6d133', 'afterSha256': 'c21d501faa52598a8fe87ae0c8ade2d6fdd273182cef2ae20df29ad2ba302d2f', 'bytes': 735898}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Lesson.html': {'beforeGitBlob': '5f624e79b8366e78ff9845f63235df8eec75c7da', 'afterSha256': '515595c44b56e584627f847a587e83243d8049fac9dd651ffd7795c320bba0d6', 'bytes': 734061}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Lesson.html': {'beforeGitBlob': '59b034408b260a09b49cfc404a80cea1c1e31e65', 'afterSha256': '789de9f9b1e1987b7b69eb7ad8751307b44108c6266a2954c198798d0fe41c7a', 'bytes': 693531}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Lesson.html': {'beforeGitBlob': 'ebdd1f2ec26d3c9d639277aefab8a126736874ae', 'afterSha256': '8f9bad8798406811142c11c57e3b4e7d8c19e13e8a1017274cfe2a735fe67a85', 'bytes': 752521}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_BUILD_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': 'c29e6c3182d8263deba46fc7897b10d9d83bd206', 'afterSha256': '00224e890c02fccc7e40d1901daee6b769e5b18d5596b430bece015d5a23c835', 'bytes': 23726}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W01/GROW_RE_A1_W01_Lesson.html': {'beforeGitBlob': '61692c4d76092192045c2f3c37da848ca4ff0c24', 'afterSha256': '107d230da08bde88fec3b03d6e29b40784c67e4f787adc9bf9c93e8f42a4eba2', 'bytes': 1003272}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W02/GROW_RE_A1_W02_Lesson.html': {'beforeGitBlob': 'ae83ae12fb3ae0fc05c33622910271f98c5b545a', 'afterSha256': '40f2f7f7f235ac0d302e1ebe41e99470e6a1b27ae460c099a388994cfe78669c', 'bytes': 741072}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W03/GROW_RE_A1_W03_Lesson.html': {'beforeGitBlob': '357fc19612082a3f4ab274d7c9fba6eb0cd6ac44', 'afterSha256': '96cdab5f4ee79e2a12ddd84f0178ed88cad0647d73fe361d584db43811f7f23a', 'bytes': 795966}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W04/GROW_RE_A1_W04_Lesson.html': {'beforeGitBlob': '380fcb68857f639a9cf0dee3d3183516a4e515fc', 'afterSha256': 'fdfae07fe2feacf017787ccdf2feac14cc8fa621a1aa62604420d615f630f5f2', 'bytes': 945100}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W05/GROW_RE_A1_W05_Lesson.html': {'beforeGitBlob': '8a0e5db9e7e247bd144eb0f8ac74a335b1e9ce63', 'afterSha256': 'd7761c238790e21249796574887cc4fecc01e4d52b5af4154266f972dc6fb37e', 'bytes': 728424}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W06/GROW_RE_A1_W06_Lesson.html': {'beforeGitBlob': '97784661a704c5ec78dace74310e5b9340797541', 'afterSha256': 'fcbcef20ba801a22fe52ba8dc7eee9fafafc47182db8a40047908436d678f579', 'bytes': 826729}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W07/GROW_RE_A1_W07_Lesson.html': {'beforeGitBlob': 'f95cd4aec1c4082f5cf401e51d20014215f6a180', 'afterSha256': 'b2d87e32fff13bcef7aa5e4048df815dd19865a6b54313ddc81eb5c85b947fb0', 'bytes': 983539}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Lesson.html': {'beforeGitBlob': '33108a21fe33e94e41d18c60f88db1a1b61b8982', 'afterSha256': 'fb65f1586b54091998c873384d2220e350d6dd35996ab2e1c0ed2277b24e9cb0', 'bytes': 798171}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Lesson.html': {'beforeGitBlob': '2ee8a1755c6743c226c5977a986674770f207b0f', 'afterSha256': 'f003b991143ed389fb6906ba86d6786e299110ae9392729f9f6b0c98fa7c5663', 'bytes': 766334}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Lesson.html': {'beforeGitBlob': '8959a02da7acdf2cfeac8542cccfc6fd6e0da222', 'afterSha256': '236222756ee58317ec9682321380a991ef2023ec70d0b7c19b5923ff64f4b9af', 'bytes': 674554}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Lesson.html': {'beforeGitBlob': '7e774c28deaf64b0191f7a2d3405036423349b0c', 'afterSha256': '35ebb0a72043e0e634770c57d62119786557985959dbb42f46363effa6df4fdf', 'bytes': 740956}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Lesson.html': {'beforeGitBlob': '457d76b6060181c98b097dc3420209441f1098b5', 'afterSha256': 'f82948b1a1596dc0873fdb1304acf5b05e20a83d1724e94775d2fd79d23bb666', 'bytes': 795191}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Lesson.html': {'beforeGitBlob': 'a6cba65be5a90eb4ed4404c3295ce103577ffa59', 'afterSha256': '2fb6439e5f500c59d62478aa533531ca17ac821fb18b67a0a1d78c24625d7269', 'bytes': 743715}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Lesson.html': {'beforeGitBlob': '6d244b372f9794cc7bb08b42801e528e5ca8030e', 'afterSha256': 'bdea643384ee2df8e375fd793621bf391f0f428c0d4ff6b5dfb0cd3d7b304783', 'bytes': 745248}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_GROW_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '91b0f70c51bfd5d018dce201c4d223de14f411f5', 'afterSha256': '3936bfe7fbe4ee06327dcc78237e2c7b57ed33dc0496ac1ec217daa77726c8c6', 'bytes': 23376}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W01/LAUNCH_RE_A1_W01_Lesson.html': {'beforeGitBlob': '7df05db2046198f883f898111d0231f1e8c9f715', 'afterSha256': '45ed365695f99c6965d56a00d1f007bfe90395ad03288cea0f7661cb84392472', 'bytes': 839467}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W02/LAUNCH_RE_A1_W02_Lesson.html': {'beforeGitBlob': 'e6b504e3ac2b1820904cf058c0193e58665a4cda', 'afterSha256': 'd0e5863c27f12c9b252bce4b869c57fca10e85a23b0791949a6f9f29bed67a6e', 'bytes': 1165164}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W03/LAUNCH_RE_A1_W03_Lesson.html': {'beforeGitBlob': '61b7bbb1d395e7ab83603be71920fa82e547b1e2', 'afterSha256': 'b1bad16ec2c426bb2a88b77df29cba5e2b94afb80d2d0e140975019487d1df86', 'bytes': 689630}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W04/LAUNCH_RE_A1_W04_Lesson.html': {'beforeGitBlob': 'b41f65841896ee3d49dbd6a77414614631df419a', 'afterSha256': '240e61b9ceaca4ae77cd199a27297fdc810aaa736b3ad216b2250747440e5480', 'bytes': 1018076}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W05/LAUNCH_RE_A1_W05_Lesson.html': {'beforeGitBlob': '893a068a0058ff0ae189f4822809733ace650df9', 'afterSha256': '681f3d41f7b37cae7bc4049d965c9f46c5e38cc619881abce403fb6fc1755cf8', 'bytes': 789535}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W06/LAUNCH_RE_A1_W06_Lesson.html': {'beforeGitBlob': '6ac7f15cb8ce0a88b5d8b448fb8e9a93037fe151', 'afterSha256': '0d5a0a71d58a4715ed30b644c08ef7feaeb43aec99ae7ca593f096b6d347ba15', 'bytes': 1026500}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W07/LAUNCH_RE_A1_W07_Lesson.html': {'beforeGitBlob': 'b67a05c6f79f22fa0014620ca6ab722a4f2c8533', 'afterSha256': '335041a08d4094428b755c4f70e37f2fa46e55254978d189bdcca2ffc99aef2d', 'bytes': 737251}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_RE_A2_W01_Lesson.html': {'beforeGitBlob': 'b015c4b3fa376d79364bacfde9e50fca19c6bbbb', 'afterSha256': '61d368e16d5848253677a554f1071084ea88407c40d4c8d3cd6c40501396ca8c', 'bytes': 985414}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/LAUNCH_RE_A2_W02_Lesson.html': {'beforeGitBlob': '91239a745a7c2b70fbe5ac9f966161c883918fba', 'afterSha256': 'c70a5941a35f28d163a49286a1c93f72626c2afc9d74655833336b1fd9a40ae4', 'bytes': 819119}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/LAUNCH_RE_A2_W03_Lesson.html': {'beforeGitBlob': '3945cdc61ddee98e594c1488da9d5b8c0e0bea80', 'afterSha256': '962dc70295083424236b16615432c7572ab34ed03e02eb477b6cf172d04af0b0', 'bytes': 684793}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/LAUNCH_RE_A2_W04_Lesson.html': {'beforeGitBlob': '811c59bfcf181e1e15119a7b6beadc53764a9df7', 'afterSha256': 'fbdeafb79997d142e7cd004d9b21af62ea162df778b64c73ba0e290aa906512e', 'bytes': 838187}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/LAUNCH_RE_A2_W05_Lesson.html': {'beforeGitBlob': '99a32b280c4e70c0198a467549612cf82b0b0b5f', 'afterSha256': '2ba488d168cdbb7efc50ad018590fd8bae1bd6af7ce83826ab039f82ef5e6651', 'bytes': 1151993}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/LAUNCH_RE_A2_W06_Lesson.html': {'beforeGitBlob': '7058aae051a759d69e8d72fac1b3e4507409f408', 'afterSha256': 'ae521ec05c1d2422b1fc850d34d291c528632c67b10f705eb2af97a7a48ce84f', 'bytes': 700953}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/LAUNCH_RE_A2_W07_Lesson.html': {'beforeGitBlob': '0d8804b055a8202807c5301e3e95f3e4107b0665', 'afterSha256': '79a92af856b83dd7961316d1f6a953b320c4689ed25d467e40128a89938c47a4', 'bytes': 751414}, 'Humanities_Teesside/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/SHA256SUMS.txt': {'beforeGitBlob': '209f29c6e5c920f3c18d4288c1e3afd835962bad', 'afterSha256': 'adb20fcd98a2548481bcd806cae147d30cc858a034798ec782a0f671f68bbcb0', 'bytes': 24076}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W10A_Solar_System_Research_Explore.html': {'beforeGitBlob': 'f69dd81bf88f28003064004de185bf15385133eb', 'afterSha256': 'eae7aa0751ba8ffd84a27a316b9e9af1e6e56d94704097b8e5ec7cd0fcaf73a1', 'bytes': 1208846}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W11A_Global_Warming_Explore.html': {'beforeGitBlob': '3a18f990fa1ea56846df14137c2747e6d59aec67', 'afterSha256': '5f9f9c657e4e28808275fc8dd0869224455cf21d2903ea377c3406b3cca7a8e7', 'bytes': 1250616}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12A_Science_Connections_Explore.html': {'beforeGitBlob': '375d6eb1fafc1446b7cd426d1e6143a3b88cd112', 'afterSha256': 'ca2448cb5fc5c946694e844298b53291dbc7872377c443afe90318b7d42ce944', 'bytes': 1192003}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W12_Follow_the_warming_chain_Classic.html': {'beforeGitBlob': '4225fae965f29d3b9640f921ac2d42542782ba89', 'afterSha256': '0453527f763eeed83f1c45f9a53b02834b2700c12b373a6dad0db1b9269cb43e', 'bytes': 1200208}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W13A_Rover_Rescue_Plan_Explore.html': {'beforeGitBlob': 'fbc554b497b28a4135f92c64bae245edd42ae0ff', 'afterSha256': '40d80695974510bc6d90a2daa6e25741780076cf43637d11f42b581b600c0ceb', 'bytes': 1080886}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html': {'beforeGitBlob': '62ae05e6ef6d8a339ddca5143ba51dae1dda4165', 'afterSha256': 'a5c6fb99587b2d9d715b116cfe7b0c706abe186bd386cc23b72f4fb2b5984493', 'bytes': 291271}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html': {'beforeGitBlob': '462bbb5858480d97556db4e55290e659b8f525c3', 'afterSha256': '32c49a121b8d9ed7f2af13c038117bdf4fbb0e9f23232f91a0015040843d6a00', 'bytes': 284203}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9A_Spherical_Bodies_Explore.html': {'beforeGitBlob': 'a9e8b3ac9c554f3cd8bc241b3dff86b4f52dfc6c', 'afterSha256': '861655ebad796f048961dd3fbb7d7b37c4fa19b124b3b22dadb7b19b0d2facc0', 'bytes': 1183172}, 'Science_Teesside/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html': {'beforeGitBlob': '9db52ce5f13ecf19e61485427de92c996ad33c5a', 'afterSha256': '178c695fe2dc166a80abfd26e41174e28ecfa39d4700db0870d7ee27bbffd6e8', 'bytes': 1275828}, 'Science_Teesside/Grow/W8-W13_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'b67cc1e6d11abd2f8dcbaa71210b1c3855db59e5', 'afterSha256': '3bd2c6ea90c2ee8071c6ae92ab8136be3541d05a16f4f94768431f819c5b152a', 'bytes': 1878}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html': {'beforeGitBlob': '5827b9b7f5bd711edaf2eecff99854899381dee2', 'afterSha256': '9130c85767d735e19fbc7b9e0dd1b314bd5db58f7e828f39bf35976f26741d7a', 'bytes': 651320}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html': {'beforeGitBlob': 'd5f55ced716226291d218727b73b528cde3b2152', 'afterSha256': 'cae2d988234b575f7b9c97d0b6907dda83fcb513ed00e6a4e40ca23ee7ff59f5', 'bytes': 652453}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html': {'beforeGitBlob': 'a96e8e812e67fefb59edbe7ecf23aabe38200aa2', 'afterSha256': '45b168db37157559bd29fb8c0b89582d3db97e0772f7a64f6cca40ebd0466928', 'bytes': 383078}, 'Science_Teesside/Launch/Autumn2_W7_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'bf8ae0154270ef4d5d2b4b4f667317b8f98d584c', 'afterSha256': 'c03b36ddb50b9d4e626a13c67c33f7d399f6f8d9e94a94133b1efcb42af9bdd2', 'bytes': 504}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L1_Genetic_Condition_Research_Introduce.html': {'beforeGitBlob': '011ebb99b5bd9897934d5362f5e2a8d5e4c1fd1d', 'afterSha256': '3026dec2f838802ce76cfecb2919dfc665f097b4e03e47f12bbfeb7c664258a2', 'bytes': 652445}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L2_Genetic_Condition_Source_Evidence_Explore.html': {'beforeGitBlob': '352285f5234bbe0a741d54a581e9bd374532aaf6', 'afterSha256': 'e7d58d365b6f9e694f41d656602013715214ec66d097b2039e1fc5978b3afb30', 'bytes': 653958}, 'Science_Teesside/Launch/W14-W15_2026-27/SCI_L_W14L3_Genetic_Condition_Presentation_Do.html': {'beforeGitBlob': '2d025121326cd46e97aadb97ae49763888e94852', 'afterSha256': 'a87e9f650c2ab23de5361c97fdb6612817b793c7609392656255a7f3fd15cba0', 'bytes': 654714}, 'Science_Teesside/Launch/W14-W15_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'c4e18b85ff41de92e3c50e27c67748098a89d766', 'afterSha256': '0bb93ca935491473b9df0d0f5605f3ea67057c6a00eb78c4925e154b71c8d5eb', 'bytes': 524}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L1_Growth_And_Differentiation_Introduce.html': {'beforeGitBlob': '43eaf64cf994c5cb0b7c7faf1209e5e8ce5ea931', 'afterSha256': '340c86768c9f6fe8a0bfecb5082aae28710842b27ce302a655b8e6d34ea3e860', 'bytes': 581500}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L2_Stem_Cells_And_Meristems_Explore.html': {'beforeGitBlob': '7f03e444c2e775c27e7806c0ee590d1e7781bee6', 'afterSha256': '3f4955539b7f6861d6ac7388aaf06491e182e9c906d58d448cab5ce94b5a92c9', 'bytes': 586976}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W10L3_Growth_Stem_Cell_Data_Application_Do.html': {'beforeGitBlob': '0dc85a7e90c37d0870cda1878df877051ef1f1c3', 'afterSha256': '567e92ad6b30eef8c38d9ba34e125334b6c4b0580502341e940c74be2b74c6ef', 'bytes': 597869}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L1_Stem_Cell_Evidence_Introduce.html': {'beforeGitBlob': '657a69d3dd308740758d3166e97f26b25c8ab9b9', 'afterSha256': '39494550b4d70cb3b21c8c48439bc72f0d2d8b89190e4be6d2be3be6a19fcf38', 'bytes': 670202}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L2_Benefit_Risk_Uncertainty_Explore.html': {'beforeGitBlob': '6c671bed98d4e2a39a29ec40468bf174ac7ed58d', 'afterSha256': '3a8d4a33ae5aabe7d5acf1c4aca3d20de8927f6cccd8753818527f1d0f55dfd6', 'bytes': 666111}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W11L3_Stem_Cell_Discuss_Do.html': {'beforeGitBlob': 'f2061eba82b157cc12276b5d7f6d89c7b06ffe54', 'afterSha256': 'f349213fee22df9d180cf18a31b9b920d28cd4c6dba6e07ce906e85e15288e3d', 'bytes': 670347}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L1_DNA_Hierarchy_Introduce.html': {'beforeGitBlob': 'abc5474518729ed1d278fbbf0a17ad032a7ef184', 'afterSha256': 'f01bd523431528632da86bbd9c02c38c6edfe47bffd764f2c4c2c69411fb3752', 'bytes': 687547}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L2_DNA_Structure_Explore.html': {'beforeGitBlob': '6b19daa49958176a4780feef1a78b8d98cdac4d2', 'afterSha256': 'e7aca0789b0a111e0efc5631a6c1d9409ed2dcb2686693e3528a56d2154f99d1', 'bytes': 685219}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12L3_Fruit_DNA_Evidence_Do.html': {'beforeGitBlob': '3c6f849c8cdca72d05a5b24185c46cb83191158e', 'afterSha256': '6e2fff14cfb09c791f80bda13d6386df6d447b3a754db3e2211556f2ba6dec8c', 'bytes': 608637}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W12_Zoom_into_genetic_information_Classic.html': {'beforeGitBlob': '60ddb723b3452c1dce4446586a53b13e3f0567dd', 'afterSha256': '058defef68f87f80bed2f6d41ec15fca48b9808021fde468606155cbf8c526a7', 'bytes': 717529}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L1_Alleles_Genotype_Phenotype_Introduce.html': {'beforeGitBlob': '1f5623cf33eb314c7e832fea9651c7efa0ecd7b5', 'afterSha256': '4d0c893510792f08f75472fce3c2ed234299cab1db4129d93861ec2b5322d61d', 'bytes': 565204}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L2_Punnett_Square_Explore.html': {'beforeGitBlob': '1494731dd4e4b5df97434cc8d0a232f2da216429', 'afterSha256': 'aba9608d6f10df7f63ae5a6bd0ce63af012dc6389f3708cf747ea19ea844ad12', 'bytes': 594485}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W13L3_Inheritance_Probability_Do.html': {'beforeGitBlob': '082b7a375499a8827774f16b94ef108226cb931b', 'afterSha256': '2e53abf3402d40c00e9931e97a498376689e092143def2b5ef9ac032b3434582', 'bytes': 567569}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html': {'beforeGitBlob': '08c918220b221b85e176cd1592cb3ef3003b318c', 'afterSha256': '125bd365d7c46d62b3867ef226c3197e715d6d6834895ca1e228e5219d1dfa0c', 'bytes': 293833}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html': {'beforeGitBlob': '924ae981135a1f012cd0594aea223637c35bb99c', 'afterSha256': 'cd724ac40006a40abee3b6bc958f6fcdb3c44af017ad2564f4a601154c4a65c6', 'bytes': 289628}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html': {'beforeGitBlob': '8611ab5f235b0be3e919390014720dac86406a39', 'afterSha256': 'd415a934d0ab0e0de37b8f75bcfc5a3c3410fb8cdaf8ff1b187400cd3d1f75c8', 'bytes': 301869}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html': {'beforeGitBlob': '727d7481b494925390d462e79c5b8d23b9d82e9f', 'afterSha256': 'c0b48159102b3cebf72fcd91deccaf49bd9a2083d49b3fc2e9df43892971a436', 'bytes': 655156}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html': {'beforeGitBlob': '1ed71dcd623d6991a0d4d07f8fe8cb0e3479431e', 'afterSha256': '73b82303adacbbfd2f8945514a62fe09805b3cf7ab905a88b11900bd1abd6f78', 'bytes': 672642}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9L3_Identical_Daughter_Cells_Do.html': {'beforeGitBlob': 'a7451adfe345919c146248911f02af52d5083955', 'afterSha256': 'df5087e190937e8df9213f037023fc77d4c20f5b351ecbfb5884f1fcc90e9ea6', 'bytes': 658594}, 'Science_Teesside/Launch/W8-W13_2026-27/SCI_L_W9_Copy_separate_divide_Classic.html': {'beforeGitBlob': '0ff2b352b110ab4134f5bb5f8d6b1019ea651ae2', 'afterSha256': '280856e8f64319de2e19b0f7766ab954c7138adb27bd5678fa08a52899a42e33', 'bytes': 685740}, 'Science_Teesside/Launch/W8-W13_2026-27/SHA256SUMS.txt': {'beforeGitBlob': 'a779109e47f78d5d38f09be0e33d675fa6705eb9', 'afterSha256': 'e8c3db8150760d44c9dbac0472200ac8b4043771db89c92dd5665a0232a5c1e1', 'bytes': 2590}}
# END DLG_1 REPLACEMENTS
# END DECLARED TRANSACTIONS

# Each transaction is judged on its own: every member present as exactly one
# modification, previous identities from the actual merge base, exact bytes and
# a matching owner-reviewed catalogue admission for every member.
REPLACEMENT_TRANSACTIONS = {
    'Sugar': (SUGAR_REVIEW_BASE, SUGAR_REPLACEMENTS),
    # BEGIN DECLARED TRANSACTION ENTRIES
    'S3 offline edition labelling': (CX2_S3_REVIEW_BASE, CX2_S3_REPLACEMENTS),
    'GROW W3 Friction': (GROW_W3_REVIEW_BASE, GROW_W3_REPLACEMENTS),
    'Diffusion W4L1': (CX2_W4L1_REVIEW_BASE, CX2_W4L1_REPLACEMENTS),
    'Sugar R10 hygiene': (SUGAR_R10_REVIEW_BASE, SUGAR_R10_REPLACEMENTS),
    'Return week W8 BUILD': (RW_W8_REVIEW_BASE, RW_W8_BUILD_REPLACEMENTS),
    'Return week W8 GROW': (RW_W8_REVIEW_BASE, RW_W8_GROW_REPLACEMENTS),
    'Return week W8 LAUNCH': (RW_W8_REVIEW_BASE, RW_W8_LAUNCH_REPLACEMENTS),
    'BUILD W8A chassis': (BUILD_W8A_CHASSIS_REVIEW_BASE, BUILD_W8A_CHASSIS_REPLACEMENTS),
    'SX3 LAUNCH W12-W15 A2W7': (SX3_LAUNCH_W12_W15_A2W7_REVIEW_BASE, SX3_LAUNCH_W12_W15_A2W7_REPLACEMENTS),
    'SX3 BUILD W12': (SX3_BUILD_W12_REVIEW_BASE, SX3_BUILD_W12_REPLACEMENTS),
    'SX3 GROW W9-W13': (SX3_GROW_W9_W13_REVIEW_BASE, SX3_GROW_W9_W13_REPLACEMENTS),
    'SX3 LAUNCH W8-W13': (SX3_LAUNCH_W8_W13_REVIEW_BASE, SX3_LAUNCH_W8_W13_REPLACEMENTS),
    'SX3-FU1 F2 LAUNCH W9-W11': (SX3_FU1_F2_LAUNCH_W9_W11_REVIEW_BASE, SX3_FU1_F2_LAUNCH_W9_W11_REPLACEMENTS),
    'SX3-FU1 F2 LAUNCH W12-W15 A2W7': (SX3_FU1_F2_LAUNCH_W12_W15_A2W7_REVIEW_BASE, SX3_FU1_F2_LAUNCH_W12_W15_A2W7_REPLACEMENTS),
    'HUM-T batch 1 BUILD': (HUM_T_BATCH_1_BUILD_REVIEW_BASE, HUM_T_BATCH_1_BUILD_REPLACEMENTS),
    'HUM-T batch 2 GROW': (HUM_T_BATCH_2_GROW_REVIEW_BASE, HUM_T_BATCH_2_GROW_REPLACEMENTS),
    'HUM-T batch 3 LAUNCH': (HUM_T_BATCH_3_LAUNCH_REVIEW_BASE, HUM_T_BATCH_3_LAUNCH_REPLACEMENTS),
    'HUM-T batch 4 GROW': (HUM_T_BATCH_4_GROW_REVIEW_BASE, HUM_T_BATCH_4_GROW_REPLACEMENTS),
    'HUM-T batch 5 LAUNCH': (HUM_T_BATCH_5_LAUNCH_REVIEW_BASE, HUM_T_BATCH_5_LAUNCH_REPLACEMENTS),
    'HUM-T batch 6 BUILD': (HUM_T_BATCH_6_BUILD_REVIEW_BASE, HUM_T_BATCH_6_BUILD_REPLACEMENTS),
    'HUM-T batch 6b BUILD': (HUM_T_BATCH_6B_BUILD_REVIEW_BASE, HUM_T_BATCH_6B_BUILD_REPLACEMENTS),
    'ADDENDUM 3 v3 explicit tags': (ADDENDUM_3_V3_EXPLICIT_TAGS_REVIEW_BASE, ADDENDUM_3_V3_EXPLICIT_TAGS_REPLACEMENTS),
    'Summer 1 responsive re-delivery': (SUMMER_1_RESPONSIVE_RE_DELIVERY_REVIEW_BASE, SUMMER_1_RESPONSIVE_RE_DELIVERY_REPLACEMENTS),
    'PASS C Autumn 2 batch 1': (PASS_C_AUTUMN_2_BATCH_1_REVIEW_BASE, PASS_C_AUTUMN_2_BATCH_1_REPLACEMENTS),
    'DLG-1': (DLG_1_REVIEW_BASE, DLG_1_REPLACEMENTS),
    # END DECLARED TRANSACTION ENTRIES
}
# Declaration order is review order: a later transaction that names a path
# supersedes the earlier claim on it (a merged transaction is history; a later
# reviewed edit of the same file is its own exact transaction). The map keeps
# the last declaration for every path.
ALL_REPLACEMENTS = {rel: name for name, (_, files) in REPLACEMENT_TRANSACTIONS.items() for rel in files}


# RULING LAND-A2 R8 §2 (Claude, 26 September 2026): the DLG-1 limb. "the bytes on disk equal
# fix_dialog_audience.py applied to the base bytes; manifests may re-cut digests only." A
# transaction named here was declared by a ruled limb, and the boundary does not take that
# declaration on trust: every member it owns is judged again by the limb, from the transaction's
# own review base to the bytes on disk, and a member the limb refuses is rejected even when its
# declared digest and its pin agree with it. The limb lives in tools/hum/admit_transaction.py,
# bound to its CATALOGUE_PINS admission before it is imported; it in turn pins the fixer and the
# pairs record by their own digests, so neither can change without that file changing too.
#
# JUDGED SUPERSESSION. Declaration order still decides ownership, narrowed for these transactions
# only: a limb-judged transaction takes a path an EARLIER declaration names only when its limb
# judges the change on that path its own. Any other change to that path stays with the earlier
# transaction and is judged by it exactly as before. The three Summer 1 SHA256SUMS.txt the
# responsive re-delivery declared pass to DLG-1 for their DLG-1 re-cut and for nothing else, and a
# hand-widened declaration cannot lift a path out of the transaction that owns it.
LIMB_JUDGED_TRANSACTIONS = {'DLG-1': 'dlg-1'}
LIMB_JUDGE = 'tools/hum/admit_transaction.py'
_LIMB_READERS = {}
_LIMB_VERDICTS = {}


def limb_judge(root):
    """The limb module, compiled from the very bytes whose digest equals its CATALOGUE_PINS admission."""
    path = root / LIMB_JUDGE
    data = path.read_bytes() if path.is_file() and not path.is_symlink() else None
    if data is None or pin_map(root).get(LIMB_JUDGE) != hashlib.sha256(data).hexdigest():
        raise ValueError('unreviewed limb judge: ' + LIMB_JUDGE)
    module = types.ModuleType('glv3_limb_judge')
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec'), module.__dict__)
    return module


def limb_reader(repo, ref):
    """Bytes of a path at the merge base of `ref` with HEAD in `repo` (b'' when absent), cached per base."""
    merge_base = subprocess.check_output(['git', 'merge-base', ref, 'HEAD'], cwd=repo).decode().strip()
    key = (str(Path(repo).resolve()), merge_base)
    if key not in _LIMB_READERS:
        cache = {}
        def read(rel):
            if rel not in cache:
                out = subprocess.run(['git', 'show', merge_base + ':' + rel], cwd=repo, capture_output=True)
                cache[rel] = out.stdout if out.returncode == 0 else b''
            return cache[rel]
        _LIMB_READERS[key] = read
    return _LIMB_READERS[key]


def _identity(path):
    try:
        st = os.lstat(path)
    except OSError:
        return None
    return (st.st_size, st.st_mtime_ns, st.st_ctime_ns, st.st_ino, st.st_mode)


def limb_verdicts(root, name, repo=None, files=None):
    """{member: None, or the ruled limb's reason} for a limb-judged transaction: judged from its own
    review base in `repo` (default root) to the bytes in `root`. `files` replaces the declared
    members, for the red proofs. Memoised on every file the verdict reads, so a sabotaged fixture
    is always judged afresh."""
    repo = repo or root
    review_base, declared = REPLACEMENT_TRANSACTIONS[name]
    files = declared if files is None else files
    tools = sorted(p for p in (root / 'tools/hum').rglob('*') if p.is_file()) if (root / 'tools/hum').is_dir() else []
    key = (str(root.resolve()), str(Path(repo).resolve()), name, review_base,
           tuple((rel, _identity(root / rel)) for rel in sorted(files)),
           tuple((str(p), _identity(p)) for p in tools),
           _identity(root / 'tools/verify_cross_estate_unification.py'))
    if key not in _LIMB_VERDICTS:
        judge = limb_judge(root)
        _LIMB_VERDICTS[key] = judge.limb_verdicts(LIMB_JUDGED_TRANSACTIONS[name], sorted(files),
                                                  limb_reader(repo, review_base), root)
    return _LIMB_VERDICTS[key]


def judged_owners(root, repo=None, transactions=None):
    """ALL_REPLACEMENTS, narrowed by JUDGED SUPERSESSION: a limb-judged transaction takes a path an
    earlier declaration names only when its limb admits the change on that path."""
    transactions = REPLACEMENT_TRANSACTIONS if transactions is None else transactions
    owners = {}
    for name, (_, files) in transactions.items():
        contested = [rel for rel in files if rel in owners]
        refused = set()
        if contested and name in LIMB_JUDGED_TRANSACTIONS:
            # A contested path that is not a regular file here is a change no limb can judge its own.
            present = [rel for rel in contested if (root / rel).is_file() and not (root / rel).is_symlink()]
            verdicts = limb_verdicts(root, name, repo, files) if present else {}
            refused = {rel for rel in contested if rel not in verdicts or verdicts[rel] is not None}
        for rel in files:
            if rel not in refused:
                owners[rel] = name
    return owners


def limb_errors(root, name, owned, repo=None, files=None):
    """The ruled limb's refusals of the members this limb-judged transaction owns."""
    if name not in LIMB_JUDGED_TRANSACTIONS or not owned:
        return []
    verdicts = limb_verdicts(root, name, repo, files)
    return [name + ' limb refuses ' + rel + ': ' + (verdicts.get(rel) or 'no verdict')
            for rel in sorted(owned) if rel not in verdicts or verdicts[rel] is not None]


def memo_digest():
    """sha() memoised on the file's identity (size, times, inode). The per-member controls judge the
    same unchanged members hundreds of times; re-hashing a 192-member, 134 MB transaction on every
    call would run for hours. Any write changes the identity, so sabotage is always re-hashed."""
    seen = {}
    def digest(path):
        key = (str(path), _identity(path))
        if key not in seen:
            seen[key] = sha(path)
        return seen[key]
    return digest


# ORDER FINISH-2, manifest-pin ruling (2026-09-20). The pack members are no longer
# pinned one by one: 1750 per-file pins drove PIN1's derived trigger list to 534,033
# bytes and GitHub refused to load the workflow at all, so the cross-estate gate never
# ran on the pull request that landed them. Each pack is now admitted through its own
# SHA256SUMS manifest, which IS pinned. The route below is deliberately no wider than
# the per-file one it replaces: status A only; the manifest must be pinned AND its own
# bytes must still equal that pin; the member must be listed in it BY NAME; and the
# member's bytes must equal the digest the manifest lists. The prefix alone still
# admits nothing, an unpinned pack admits nothing, and a manifest edited to admit a
# new file stops matching its pin -- so the pin catches the edit before the list it
# carries is ever honoured.
PACK_MANIFEST = 'SHA256SUMS.txt'


def pack_manifest(root, pins, rel):
    """The pinned manifest admitting a Humanities pack member: (manifest, member, digest) or None."""
    if not rel.startswith(HUMANITIES_PACKS) or rel in pins:
        return None
    parts = rel[len(HUMANITIES_PACKS):].split('/')
    if len(parts) < 2:
        return None
    manifest_rel = HUMANITIES_PACKS + parts[0] + '/' + PACK_MANIFEST
    path = root / manifest_rel
    if manifest_rel not in pins or not path.is_file() or pins[manifest_rel] != sha(path):
        return None
    member = '/'.join(parts[1:])
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        if not line.strip():
            continue
        checksum, separator, name = line.partition('  ')
        if not separator or not re.fullmatch(r'[0-9a-f]{64}', checksum):
            return None
        if name.strip() == member:
            return manifest_rel, member, checksum
    return None


def owned_members(name, files, owners=None):
    owners = ALL_REPLACEMENTS if owners is None else owners
    return {rel: entry for rel, entry in files.items() if owners.get(rel, name) == name}


def git_before_entries(root, base, paths=None):
    # Match git_changes' triple-dot semantics; do not trust a supplied manifest
    # for the previous file identities.
    merge_base = subprocess.check_output(['git', 'merge-base', base, 'HEAD'], cwd=root).decode().strip()
    raw = subprocess.check_output(['git', 'ls-tree', '-z', merge_base, '--', *sorted(paths if paths is not None else SUGAR_REPLACEMENTS)], cwd=root)
    result = {}
    for record in raw.decode().split('\0'):
        if not record:
            continue
        fields, path = record.split('\t', 1)
        mode, kind, blob = fields.split()
        result[path] = (mode, kind, blob)
    return result


def replacement_errors(name, files, root, changes, pins, before_entries, owners=None, digest=None):
    digest = digest or sha
    files = owned_members(name, files, owners)
    selected = [(status, rel) for status, rel in changes if rel in files]
    if not selected:
        return []
    if len(selected) != len(files) or {rel for _, rel in selected} != set(files):
        return [name + ' replacement must contain exactly the ' + number_word(len(files)) + ' reviewed file modifications']
    errors = []
    for status, rel in selected:
        reviewed = files[rel]
        path = root / rel
        if status != 'M':
            errors.append(name + ' replacement is not a modification: ' + rel)
        if before_entries.get(rel) != ('100644', 'blob', reviewed['beforeGitBlob']):
            errors.append(name + ' previous file identity or mode differs: ' + rel)
        if path.is_symlink() or not path.is_file() or path.resolve().is_relative_to(root.resolve()) is False:
            errors.append(name + ' replacement must be a regular file inside the tree: ' + rel)
        elif path.stat().st_size != reviewed['bytes'] or digest(path) != reviewed['afterSha256']:
            errors.append(name + ' replacement bytes differ: ' + rel)
        if pins.get(rel) != reviewed['afterSha256']:
            errors.append(name + ' replacement lacks matching owner-reviewed catalogue admission: ' + rel)
    return errors


def number_word(n):
    return {7: 'seven'}.get(n, str(n))


def sugar_replacement_errors(root, changes, pins, before_entries):
    return replacement_errors('Sugar', SUGAR_REPLACEMENTS, root, changes, pins, before_entries)


def sugar_controls(root, proposed_pins=None):
    return transaction_controls(root, 'Sugar', proposed_pins)


def transaction_controls(root, name, proposed_pins=None):
    # CI uses the real reviewed pin map. The optional map lets a review harness
    # exercise the proposed transaction before paired admissions are staged;
    # such a run is conditional evidence, never a production gate pass.
    base, files = REPLACEMENT_TRANSACTIONS[name]
    owners = judged_owners(root)
    files = owned_members(name, files, owners)
    if not files:
        return []
    digest = memo_digest()
    errors_for = lambda *a: replacement_errors(name, files, *a, owners=owners, digest=digest)
    pins = pin_map(root) if proposed_pins is None else proposed_pins
    changes = [('M', rel) for rel in sorted(files)]
    before = git_before_entries(root, base, files)
    rows = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        rows.append({'name': name, 'status': 'PASS'})
    check(name + ': all reviewed replacements pass the bounded rule', not errors_for(root, changes, pins, before))
    for rel in sorted(files):
        missing_pin = dict(pins); missing_pin.pop(rel, None)
        check(name + ' missing owner admission rejected: ' + rel, bool(errors_for(root, changes, missing_pin, before)))
        wrong_before = dict(before); wrong_before[rel] = ('100644', 'blob', '0' * 40)
        check(name + ' wrong previous identity rejected: ' + rel, bool(errors_for(root, changes, pins, wrong_before)))
        wrong_mode = dict(before); wrong_mode[rel] = ('120000', 'blob', files[rel]['beforeGitBlob'])
        check(name + ' previous symlink mode rejected: ' + rel, bool(errors_for(root, changes, pins, wrong_mode)))
        for status in ('A', 'D', 'T'):
            altered = [(status if path == rel else kind, path) for kind, path in changes]
            check(name + ' wrong change type '+status+' rejected: ' + rel, bool(errors_for(root, altered, pins, before)))
        if len(files) > 1:
            # Omitting one member of a multi-file transaction leaves a partial transaction, which must fail.
            # A one-member transaction has nothing left to judge when its member is omitted; that case is
            # the plain protected-path fence, covered by its own controls above.
            check(name + ' omitted replacement rejected: ' + rel, bool(errors_for(root, [(kind, path) for kind, path in changes if path != rel], pins, before)))
    check(name + ' duplicate replacement rejected', bool(errors_for(root, changes + [changes[0]], pins, before)))
    with tempfile.TemporaryDirectory(prefix='replacement-proof-') as temp:
        fixture = Path(temp)
        for rel in files:
            target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / rel, target)
        check(name + ' actual candidate bytes pass in disposable fixture', not errors_for(fixture, changes, pins, before))
        for rel in sorted(files):
            path = fixture / rel; original = path.read_bytes()
            try:
                path.write_bytes(original + b'changed')
                check(name + ' changed candidate bytes rejected: ' + rel, bool(errors_for(fixture, changes, pins, before)))
                # Even changing the caller's catalogue digest cannot change the
                # independent exact replacement review.
                repinned = dict(pins); repinned[rel] = sha(path)
                check(name + ' repinned changed bytes still rejected: ' + rel, bool(errors_for(fixture, changes, repinned, before)))
                path.unlink()
                check(name + ' missing candidate file rejected: ' + rel, bool(errors_for(fixture, changes, pins, before)))
                path.symlink_to(root / rel)
                check(name + ' candidate symlink rejected: ' + rel, bool(errors_for(fixture, changes, pins, before)))
            finally:
                if path.is_symlink(): path.unlink()
                path.write_bytes(original)
        check(name + ' all sabotage was restored', not errors_for(fixture, changes, pins, before))
    if name in LIMB_JUDGED_TRANSACTIONS:
        check(name + ': the ruled limb judges every member it owns its own, from its review base to the bytes on disk',
              not limb_errors(root, name, files))
        if name == 'DLG-1':
            rows.extend(dlg1_controls(root, owners))
    return rows


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected(path):
    return any(path == prefix or path.startswith(prefix + '/') for prefix in PROTECTED)


def pin_map(root):
    tree = ast.parse((root / 'tools/verify_cross_estate_unification.py').read_text())
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CATALOGUE_PINS' for t in node.targets)]
    if len(values) != 1:
        raise ValueError('expected exactly one reviewed catalogue pin block')
    return values[0]['files']


def explicit_cover_paths(root):
    source = json.loads((root / SOURCE).read_text())
    downloads = json.loads((root / DOWNLOADS).read_text())
    ids = [row['id'] for row in source['records']]
    if len(ids) != 25 or len(set(ids)) != 25 or not all(re.fullmatch(r'(?:BH|BR|GH|GR|LH)_W[3-7]', value) for value in ids):
        raise ValueError('cover IDs do not identify the 25 reviewed periods')
    dependencies = [row['path'] for row in downloads['dependencies']]
    if len(dependencies) != 69 or len(set(dependencies)) != 69:
        raise ValueError('expected 66 downloads plus three pathway archives')
    for rel in dependencies:
        path = PurePosixPath(rel)
        if path.is_absolute() or '..' in path.parts or '\\' in rel or not rel.startswith(COVER + '/'):
            raise ValueError('download manifest escapes the reviewed cover directory: ' + rel)
    return {*(COVER + '/' + name + '.html' for name in ids),
            COVER + '/index.html', COVER + '/resource.css', COVER + '/resource.js', *dependencies}


def verify_humanities(root):
    directory = root / 'tools/humanities_resources'
    sys.path.insert(0, str(directory))
    try:
        # The generator import must come from the same exact reviewed fixture.
        saved = sys.modules.pop('build_resources', None)
        spec = importlib.util.spec_from_file_location('glv3_humanities_check', directory / 'check_resources.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        report = module.check(root, root)
        if report['result'] != 'PASS' or report['existing_routes_preserved'] != 30 or report['additional_coverage_claimed'] != 0:
            raise ValueError('Humanities preservation verdict is incomplete')
    finally:
        sys.path.pop(0)
        sys.modules.pop('build_resources', None)
        if saved is not None: sys.modules['build_resources'] = saved


def public_label_paths(root, pins):
    manifest = root / LABEL_EDITS
    if not manifest.is_file() or pins.get(LABEL_EDITS) != sha(manifest):
        raise ValueError('Public label amendment is not reviewed')
    changes = json.loads(manifest.read_text())['files']
    source = json.loads((root / SOURCE).read_text())['records']
    expected = {COVER+'/'+r['id']+'.html' for r in source} | {COVER+'/index.html'}
    if {r['path'] for r in changes} != expected or len(changes) != len(expected):
        raise ValueError('Public label changes must name exactly the existing cover HTML pages')
    for row in changes:
        path = root / row['path']
        text = path.read_text()
        if sha(path) != row['afterSha256'] or pins.get(row['path']) != row['afterSha256']:
            raise ValueError('Unreviewed public cover bytes: '+row['path'])
        for edit in reversed(row['edits']):
            start, before, after = edit['start'], edit['before'], edit['after']
            if any(c in before+after for c in '<>') or 'David' not in before or 'David' in after:
                raise ValueError('Label amendment must be visible naming only')
            if text[start:start+len(after)] != after:
                raise ValueError('Public label edit position changed')
            text = text[:start]+before+text[start+len(after):]
        if hashlib.sha256(text.encode()).hexdigest() != row['beforeSha256']:
            raise ValueError('Content changed beyond approved public labels: '+row['path'])
    return expected


def judge(root, changes, base=None):
    relevant = [(status, path) for status, path in changes if protected(path)]
    if not relevant:
        return []
    errors = []
    try:
        pins = pin_map(root)
        owners = judged_owners(root) if any(path in ALL_REPLACEMENTS for _, path in relevant) else ALL_REPLACEMENTS
        for name, (_, files) in REPLACEMENT_TRANSACTIONS.items():
            files = owned_members(name, files, owners)
            if any(path in files for _, path in relevant):
                if base is None:
                    return [name + ' replacements require the actual comparison base']
                errors.extend(replacement_errors(name, files, root, relevant, pins, git_before_entries(root, base, files), owners))
                errors.extend(limb_errors(root, name, files))
        if errors:
            return errors
        cover_paths = explicit_cover_paths(root)
        label_paths = public_label_paths(root, pins)
        for status, rel in relevant:
            governed = pack_manifest(root, pins, rel)
            if rel in SHELVES:
                if status not in ('A', 'M') or not (root / rel).is_file() or pins.get(rel) != sha(root / rel):
                    errors.append('reviewed shelf bytes or change type differ: ' + rel)
            elif rel in ALL_REPLACEMENTS:
                # Already checked as one exact M transaction above.
                pass
            elif rel.startswith(SCIENCE_PACKS) and rel in pins:
                # Owner-requested 6 September additive BUILD/GROW downloads.
                # Every individual file has an explicit reviewed digest; the
                # prefix alone never admits a file or an existing-file edit.
                if status != 'A' or not (root / rel).is_file() or pins[rel] != sha(root / rel):
                    errors.append('Science teaching pack must be an exact reviewed addition: ' + rel)
            elif rel.startswith(HUMANITIES_PACKS) and rel in pins:
                # ORDER §2 (2026-09-20): the HUM-D5 additive pack landing. Same rule
                # as SCIENCE_PACKS above -- an exact, individually pinned addition.
                # This is now the route for the manifests themselves and for the two
                # packs that shipped without one (recorded, not invented).
                if status != 'A' or not (root / rel).is_file() or pins[rel] != sha(root / rel):
                    errors.append('Humanities teaching pack must be an exact reviewed addition: ' + rel)
            elif governed is not None:
                # ORDER FINISH-2 manifest-pin ruling (2026-09-20): admitted by the pack
                # manifest, which is itself pinned. No wider than the clause above --
                # the digest simply comes from the reviewed manifest instead of from a
                # reviewed line of its own.
                _manifest_rel, _member, listed = governed
                if status != 'A' or not (root / rel).is_file() or listed != sha(root / rel):
                    errors.append('Humanities teaching pack must be an exact manifest-listed addition: ' + rel)
            elif rel.startswith(SUMMER1_PATHWAY_TREES) and rel in pins:
                # ADDENDUM 3 v3 (2026-09-22): the Summer 1 pathway trees. Same rule as the two
                # pack clauses above -- an exact, individually pinned addition, never an edit.
                if status != 'A' or not (root / rel).is_file() or pins[rel] != sha(root / rel):
                    errors.append('Summer 1 pathway tree must be an exact reviewed addition: ' + rel)
            elif rel.startswith(LAND_A2_SCIENCE_TERMS) and rel in pins:
                # LAND-A2 Science (2026-09-25). Same rule as the Summer 1 clause above -- an exact,
                # individually pinned addition, never an edit or a deletion.
                if status != 'A' or not (root / rel).is_file() or pins[rel] != sha(root / rel):
                    errors.append('LAND-A2 Science lesson must be an exact reviewed addition: ' + rel)
            elif rel in PATHWAY_PARENTS:
                # SX3-PASSES PASS 4 (3b). Additive only, and the bytes must equal the
                # reviewed admission; the set alone never admits an edit or a deletion.
                if status != 'A' or not (root / rel).is_file() or pins.get(rel) != sha(root / rel):
                    errors.append('pathway landing page must be an exact reviewed addition: ' + rel)
            elif rel in cover_paths:
                # This ruling installs new cover resources. It does not permit
                # edits, deletions or renames of existing lesson payloads.
                if status != 'A' and not (status == 'M' and rel in label_paths):
                    errors.append('cover change is neither additive nor an exact approved public-label edit: ' + rel)
            else:
                errors.append('original GLV3 protected-path fence rejected: ' + rel)
        if errors:
            return errors
        # Bind the validator and all sources before invoking it. A manifest
        # cannot enlarge this exception or rewrite the checked old-route hashes.
        for rel in (*BOUND_INPUTS, COVER + '/index.html'):
            path = root / rel
            if not path.is_file() or pins.get(rel) != sha(path):
                errors.append('unreviewed cover validation input: ' + rel)
        if not errors:
            verify_humanities(root)
    except (AssertionError, ValueError, OSError, KeyError, TypeError, ImportError, subprocess.CalledProcessError) as exc:
        errors.append('reviewed catalogue/cover proof failed: ' + str(exc))
    return errors


def git_changes(root, base):
    command = ['git', 'diff', '--name-status', '-z', '--no-renames', base + '...HEAD', '--', *PROTECTED]
    raw = subprocess.check_output(command, cwd=root).decode('utf-8').split('\0')
    if raw[-1] == '': raw.pop()
    if len(raw) % 2:
        raise ValueError('git returned an incomplete changed-path record')
    rows = list(zip(raw[::2], raw[1::2]))
    if any(status not in ('A', 'M', 'D', 'T', 'U', 'X', 'B') for status, _ in rows):
        raise ValueError('unexpected git change status')
    return rows


def controls(root):
    rows = []
    def check(name, condition):
        if not condition: raise AssertionError(name)
        rows.append({'name': name, 'status': 'PASS'})
    additions = [('A', p) for p in sorted(explicit_cover_paths(root))]
    reviewed = [('A', p) for p in SHELVES] + additions
    check('Exact reviewed shelves and all manifest-bound cover additions pass', not judge(root, reviewed))
    check('An unrelated generated-tree change does not expand protected-path permissions', not judge(root, [('M', 'GROW_Estate_v3/index.html')]))
    source = json.loads((root / SOURCE).read_text())
    retained = {item['path'] for record in source['records'] for item in record['existing_routes']}
    check('All 30 retained Humanities/RE lesson paths reject modifications', len(retained) == 30 and all(judge(root, [('M', path)]) for path in retained))
    science = 'Science_Teesside/Build/SCI_B_W3_Backbones.html'
    check('An existing Science lesson path remains protected', (root / science).is_file() and bool(judge(root, [('M', science)])))
    for prefix in PROTECTED:
        check('Original protected prefix remains fenced: ' + prefix, bool(judge(root, [('A', prefix + '/unreviewed.html')])))
    check('An undeclared cover file is rejected', bool(judge(root, [('A', COVER + '/unreviewed.html')])))
    check('A modification of an existing cover file is not an additive installation', bool(judge(root, [('M', COVER+'/resource.css')])))
    check('A deleted shelf is rejected', bool(judge(root, [('D', SHELVES[0])])))
    # ADDENDUM 3 v3 red proofs for SUMMER1_PATHWAY_TREES. The route is only as good as its
    # refusals, so each way it could go wrong is proved to go RED rather than assumed to.
    landed = sorted(r for r in pin_map(root)
                    if r.startswith(SUMMER1_PATHWAY_TREES) and (root / r).is_file())
    # A path a declared replacement transaction owns has LEFT the additive route: it is judged
    # member by member against the real comparison base, which the self-test does not have.
    # SCIENCE_PACKS and HUMANITIES_PACKS below exclude their owned paths the same way. The
    # exclusion narrows nothing: the files the additive route still owns still prove it, and
    # the owned ones get a refusal proof of their own immediately after.
    owned = [r for r in landed if r in ALL_REPLACEMENTS]
    free = [r for r in landed if r not in ALL_REPLACEMENTS]
    check('the Summer 1 pathway trees have landed files to judge', bool(free))
    if free:
        check('every pinned Summer 1 pathway file the additive route still owns '
              'passes as an exact reviewed addition',
              not judge(root, [('A', r) for r in free]))
        check('an addition under the Summer 1 prefix with no pin is rejected '
              '(the prefix alone admits nothing)',
              bool(judge(root, [('A', SUMMER1_PATHWAY_TREES[0] + 'unreviewed.html')])))
        check('a modification of a landed Summer 1 file is rejected (additive only)',
              bool(judge(root, [('M', free[0])])))
        check('a deletion of a landed Summer 1 file is rejected',
              bool(judge(root, [('D', free[0])])))
        disagree = dict(pin_map(root)); disagree[free[0]] = '0' * 64
        real = globals()['pin_map']
        try:
            globals()['pin_map'] = lambda _root: disagree
            check('a Summer 1 file whose reviewed pin disagrees with its bytes is rejected',
                  bool(judge(root, [('A', free[0])])))
        finally:
            globals()['pin_map'] = real
    if owned:
        check('a Summer 1 file a declared transaction owns is NOT waved through the '
              'additive route: it is refused without the real comparison base',
              all(bool(judge(root, [('A', r)])) for r in owned))
    # LAND-A2 Science red proofs for LAND_A2_SCIENCE_TERMS, the same four refusals as the Summer 1
    # route above: the route is only as good as its refusals, so each is proved to go RED.
    science_landed = sorted(r for r in pin_map(root)
                            if r.startswith(LAND_A2_SCIENCE_TERMS) and (root / r).is_file()
                            and r not in ALL_REPLACEMENTS)
    check('the LAND-A2 Science term folders have landed files to judge', bool(science_landed))
    if science_landed:
        check('every pinned LAND-A2 Science file passes as an exact reviewed addition',
              not judge(root, [('A', r) for r in science_landed]))
        for prefix in LAND_A2_SCIENCE_TERMS:
            check('an addition under ' + prefix + ' with no pin is rejected (the prefix alone admits nothing)',
                  bool(judge(root, [('A', prefix + 'unreviewed.html')])))
        check('a modification of a landed LAND-A2 Science file is rejected (additive only)',
              bool(judge(root, [('M', science_landed[0])])))
        check('a deletion of a landed LAND-A2 Science file is rejected',
              bool(judge(root, [('D', science_landed[0])])))
        disagree = dict(pin_map(root)); disagree[science_landed[0]] = '0' * 64
        real = globals()['pin_map']
        try:
            globals()['pin_map'] = lambda _root: disagree
            check('a LAND-A2 Science file whose reviewed pin disagrees with its bytes is rejected',
                  bool(judge(root, [('A', science_landed[0])])))
        finally:
            globals()['pin_map'] = real
    # ORDER SX3-PASSES PASS 4 (3b) red proofs for PATHWAY_PARENTS. The set is only
    # as good as its refusals, so each of the three ways it could go wrong is proved
    # to go RED rather than assumed to.
    check('The three pathway landing pages pass as exact reviewed additions',
          not judge(root, [('A', p) for p in PATHWAY_PARENTS]))
    # (i) a fourth path planted in the set, with no pin behind it.
    planted = 'Science_Teesside/Build/UNREVIEWED_START_HERE.html'
    saved = globals()['PATHWAY_PARENTS']
    try:
        globals()['PATHWAY_PARENTS'] = saved + (planted,)
        check('A fourth path planted in PATHWAY_PARENTS with no pin is rejected',
              bool(judge(root, [('A', planted)])))
    finally:
        globals()['PATHWAY_PARENTS'] = saved
    # (ii) a listed page whose reviewed pin disagrees with the bytes on disk.
    pins = pin_map(root)
    disagreeing = dict(pins); disagreeing[PATHWAY_PARENTS[0]] = '0' * 64
    real_pin_map = globals()['pin_map']
    try:
        globals()['pin_map'] = lambda _root: disagreeing
        check('A pathway landing page whose pin disagrees with its bytes is rejected',
              bool(judge(root, [('A', PATHWAY_PARENTS[0])])))
    finally:
        globals()['pin_map'] = real_pin_map
    # (iii) an EDIT of a listed page is not an installation: it falls through to the
    # existing routes and is rejected there, so editing one still needs its own
    # reviewed transaction.
    check('A modification of a pathway landing page is not an additive installation',
          bool(judge(root, [('M', PATHWAY_PARENTS[0])])))
    check('Rename-as-delete/add cannot move a retained lesson into the cover exception', bool(judge(root, [('D', sorted(retained)[0]), additions[0]])))
    science_additions = [('A', rel) for rel in pin_map(root) if rel.startswith(SCIENCE_PACKS) and rel not in ALL_REPLACEMENTS]
    if science_additions:
        check('Exact individually pinned Science teaching files pass as additions', not judge(root, science_additions))
        first = science_additions[0][1]
        check('An existing Science teaching download remains protected from replacement', bool(judge(root, [('M', first)])))
        check('A Science teaching download cannot be deleted', bool(judge(root, [('D', first)])))
        check('An unlisted Science teaching file is rejected', bool(judge(root, [('A', SCIENCE_PACKS+'unreviewed.pptx')])))
    # ORDER §2 (2026-09-20) red proofs for HUMANITIES_PACKS, the three ways it could go
    # wrong, each proved RED rather than assumed: (i) a path outside the prefix,
    # (ii) an addition inside the prefix with no pin, (iii) a modification of a pinned
    # pack file (falls through to the fence). The positive control and (iii) run on
    # the tree's own pinned pack files when there are any, and on a planted, pinned
    # file in the disposable fixture below when there are none.
    check('A Humanities file outside the pack prefix is not admitted by the pack route',
          bool(judge(root, [('A', 'Humanities_Teesside/UNREVIEWED_pack_file.pptx')])))
    check('An unlisted Humanities teaching file is rejected',
          bool(judge(root, [('A', HUMANITIES_PACKS + 'unreviewed.pptx')])))
    humanities_additions = [('A', rel) for rel in pin_map(root) if rel.startswith(HUMANITIES_PACKS) and rel not in ALL_REPLACEMENTS]
    if humanities_additions:
        check('Exact individually pinned Humanities teaching files pass as additions', not judge(root, humanities_additions))
        first_h = humanities_additions[0][1]
        check('An existing Humanities teaching pack file remains protected from replacement', bool(judge(root, [('M', first_h)])))
        check('A Humanities teaching pack file cannot be deleted', bool(judge(root, [('D', first_h)])))
    with tempfile.TemporaryDirectory(prefix='glv3-reviewed-boundary-') as temp:
        fixture = Path(temp)
        files = {*explicit_cover_paths(root), *SHELVES, *retained, *BOUND_INPUTS, *(rel for _, rel in science_additions),
                 'tools/verify_cross_estate_unification.py', 'index.html'}
        for rel in files:
            target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(root / rel, target)
        check('Disposable fixture is initially accepted by the real validators', not judge(fixture, reviewed))
        if science_additions:
            check('Disposable Science fixture is initially accepted', not judge(fixture, science_additions))
        # ORDER §2 (2026-09-20): plant one pinned Humanities pack file in the fixture so
        # the HUMANITIES_PACKS positive control, (iii) and byte drift are proved on
        # every tree, including one that carries no pack file yet.
        planted_h = HUMANITIES_PACKS + 'PLANTED_SELF_TEST/planted_pack_file.txt'
        (fixture / planted_h).parent.mkdir(parents=True, exist_ok=True); (fixture / planted_h).write_bytes(b'planted pack bytes\n')
        planted_pins = dict(pin_map(root)); planted_pins[planted_h] = sha(fixture / planted_h)
        real_pin_map_h = globals()['pin_map']
        try:
            globals()['pin_map'] = lambda _root: planted_pins
            check('A planted, exactly pinned Humanities pack file passes as an addition', not judge(fixture, [('A', planted_h)]))
            check('A modification of a pinned Humanities pack file is rejected', bool(judge(fixture, [('M', planted_h)])))
            check('A deletion of a pinned Humanities pack file is rejected', bool(judge(fixture, [('D', planted_h)])))
            (fixture / planted_h).write_bytes(b'drifted\n')
            check('A pinned Humanities pack file whose bytes drift from its pin is rejected', bool(judge(fixture, [('A', planted_h)])))
        finally:
            globals()['pin_map'] = real_pin_map_h
        def mutate(rel, replacement, message, changes=reviewed):
            path = fixture / rel; original = path.read_bytes()
            try:
                changed = replacement(original); check(message + ' sabotage changes bytes', changed != original); path.write_bytes(changed)
                check(message, bool(judge(fixture, changes)))
            finally: path.write_bytes(original)
        if science_additions:
            native = next(rel for _, rel in science_additions if rel.endswith('.pptx'))
            mutate(native, lambda b: b + b'changed', 'Changed native Science bytes fail without re-pinning', science_additions)
        mutate(SHELVES[0], lambda b: b + b'<!-- unreviewed -->', 'Shelf byte drift is rejected')
        mutate(SOURCE, lambda b: b + b'\n', 'A changed source manifest cannot redefine retained lessons')
        mutate(DOWNLOADS, lambda b: b + b'\n', 'A changed download manifest cannot enlarge the allowed set')
        # ORDER FINISH-2 manifest-pin ruling (2026-09-20): the manifest route, proved on
        # the tree's own pack. The ruling named three ways it could go wrong and each
        # is proved RED here, not assumed: (i) a member whose bytes drift from the
        # digest its manifest lists, (ii) a member the manifest does not list at all,
        # (iii) a manifest edited to admit one -- caught by the manifest's own pin,
        # because the edit changes the bytes that pin covers.
        manifest_pins = [rel for rel in pin_map(root)
                         if rel.startswith(HUMANITIES_PACKS) and rel.endswith('/' + PACK_MANIFEST)
                         and len(rel[len(HUMANITIES_PACKS):].split('/')) == 2]
        if manifest_pins:
            manifest_rel = sorted(manifest_pins)[0]
            manifest_base = manifest_rel[: -len(PACK_MANIFEST)]
            listed_rows = [line for line in (root / manifest_rel).read_text(encoding='utf-8').splitlines() if line.strip()]
            member_rel = manifest_base + listed_rows[0].partition('  ')[2].strip()
            for rel in (manifest_rel, member_rel):
                copy_to = fixture / rel; copy_to.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(root / rel, copy_to)
            check('A manifest-listed Humanities pack member passes as an addition without a pin of its own',
                  not judge(fixture, [('A', member_rel)]))
            check('A manifest-listed member is admitted as an addition only',
                  bool(judge(fixture, [('M', member_rel)])))
            check('A manifest-listed member cannot be deleted',
                  bool(judge(fixture, [('D', member_rel)])))
            check('A Humanities pack file its manifest does not list is rejected',
                  bool(judge(fixture, [('A', manifest_base + 'unlisted_addition.pptx')])))
            check('A Humanities pack member whose manifest is not pinned is rejected',
                  bool(judge(fixture, [('A', HUMANITIES_PACKS + 'UNPINNED_PACK/anything.pptx')])))
            mutate(member_rel, lambda b: b + b'drifted',
                   'A manifest-listed member whose bytes drift from the listed digest is rejected',
                   [('A', member_rel)])
            mutate(manifest_rel, lambda b: b + b'0' * 64 + b'  unlisted_addition.pptx\n',
                   'A manifest enlarged to admit an unreviewed file stops matching its pin, so the route closes',
                   [('A', member_rel)])
        page = next(path for path in sorted(explicit_cover_paths(root)) if re.search(r'/BH_W3\.html$', path))
        mutate(page, lambda b: b.replace(b'data-minutes="3"', b'data-minutes="43"', 1), 'Changed teaching minutes are rejected by the shared Humanities validator')
        native = next(row['path'] for row in json.loads((root / DOWNLOADS).read_text())['dependencies'] if row['path'].endswith('.pdf'))
        mutate(native, lambda b: b + b'\n', 'Native download byte drift is rejected')
        mutate(sorted(retained)[0], lambda b: b + b'\n', 'Retained Humanities content drift is rejected even if omitted from the supplied diff')
    for name in REPLACEMENT_TRANSACTIONS:
        rows.extend(transaction_controls(root, name))
    rows.extend(supersession_controls(root))
    return rows


def supersession_controls(root):
    # A later declared transaction on the same path retires the earlier claim, and
    # judges the path itself; the earlier transaction's exactness rule no longer
    # reds on a partial diff. Proven on a real member with a synthetic later claim.
    rows = []
    def check(name, condition):
        if not condition: raise AssertionError(name)
        rows.append({'name': name, 'status': 'PASS'})
    first = next(((name, files) for name, (_, files) in REPLACEMENT_TRANSACTIONS.items() if len(owned_members(name, files)) > 1), None)
    if first is None:
        return rows
    name, files = first
    owned = owned_members(name, files)
    rel = sorted(owned)[0]
    pins = pin_map(root)
    before = git_before_entries(root, 'HEAD', [rel])
    partial = [('M', rel)]
    check('A partial diff of an earlier transaction is still rejected while it owns the path',
          bool(replacement_errors(name, files, root, partial, pins, before)))
    owners = dict(ALL_REPLACEMENTS); owners[rel] = 'Later'
    check('A later declared transaction retires the earlier claim on the same path',
          not replacement_errors(name, files, root, partial, pins, before, owners))
    check('The retired path drops out of the earlier transaction\'s controls',
          rel not in owned_members(name, files, owners) and len(owned_members(name, files, owners)) == len(owned) - 1)
    later = {rel: {'beforeGitBlob': before[rel][2], 'afterSha256': sha(root / rel), 'bytes': (root / rel).stat().st_size}}
    pins_later = dict(pins); pins_later[rel] = later[rel]['afterSha256']
    check('The later transaction judges the superseded path itself',
          not replacement_errors('Later', later, root, partial, pins_later, before, owners))
    wrong = {rel: dict(later[rel], afterSha256='0' * 64)}
    check('The later transaction still rejects bytes that differ from its review',
          bool(replacement_errors('Later', wrong, root, partial, pins_later, before, owners)))
    return rows


def dlg1_controls(root, owners):
    # RULING LAND-A2 R8 §2 red proofs, on the declared DLG-1 transaction itself. The limb is only as
    # good as its refusals, so each way it could be widened or bypassed is proved RED here rather
    # than assumed to. Every proof reads the real review base; sabotage happens in a disposable copy.
    # A later transaction may supersede DLG-1's members: each proof runs on what DLG-1 still owns,
    # and a proof with nothing left to stand on is skipped, never passed vacuously.
    rows = []
    def check(label, condition):
        if not condition:
            raise AssertionError(label)
        rows.append({'name': label, 'status': 'PASS'})
    name, responsive = 'DLG-1', 'Summer 1 responsive re-delivery'
    review_base, declared = REPLACEMENT_TRANSACTIONS[name]
    names = list(REPLACEMENT_TRANSACTIONS)
    earlier, later = {}, set()
    for other in names:
        files = REPLACEMENT_TRANSACTIONS[other][1]
        if names.index(other) < names.index(name):
            earlier.update({rel: other for rel in files if rel in declared})
        elif other != name:
            later.update(rel for rel in files if rel in declared)
    owned = owned_members(name, declared, owners)
    if not owned:
        return rows
    verdicts = limb_verdicts(root, name)
    pins = pin_map(root)
    judge_module = limb_judge(root)
    fixer, _pairs, held = judge_module.dlg1_tools(root)
    check('DLG-1 POSITIVE CONTROL: judge() admits every member DLG-1 owns as the change, from its review base',
          not judge(root, [('M', rel) for rel in sorted(owned)], review_base))
    contested = sorted(rel for rel in earlier if rel not in later)
    if contested:
        check('DLG-1: a path an earlier transaction declared passes to DLG-1 exactly when the limb admits its change',
              all((owners.get(rel) == name) == (verdicts.get(rel, 'no verdict') is None) for rel in contested))
    shared = [rel for rel in contested if earlier[rel] == responsive]
    if shared:
        check('DLG-1: the Summer 1 manifests the responsive re-delivery declared are admitted DLG-1 re-cuts, and pass to DLG-1',
              all(owners.get(rel) == name for rel in shared))
    resp_base, resp_declared = REPLACEMENT_TRANSACTIONS[responsive]
    resp_only = sorted(rel for rel in resp_declared if owners.get(rel) == responsive)
    if resp_only:
        resp_owned = owned_members(responsive, resp_declared, owners)
        errors = replacement_errors(responsive, resp_owned, root, [('M', resp_only[0])], pins,
                                    git_before_entries(root, resp_base, resp_owned), owners)
        check('RED PROOF (a responsive member DLG-1 does not declare): a change to it is still rejected by the '
              'responsive re-delivery itself', bool(errors) and all(e.startswith(responsive) for e in errors))
    page = next((rel for rel in sorted(owned) if rel.endswith('.html')), None)
    sums = next((rel for rel in sorted(owned) if rel.endswith('/SHA256SUMS.txt') and rel not in shared), None)
    json_manifests = sorted(rel for rel in owned if judge_module.dlg1_manifest_kind(rel) == 'json')
    read = limb_reader(root, review_base)
    with tempfile.TemporaryDirectory(prefix='dlg1-limb-proof-') as temp:
        fixture = Path(temp)
        for rel in {*declared, *held, 'tools/verify_cross_estate_unification.py'}:
            if (root / rel).is_file():
                target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(root / rel, target)
        shutil.copytree(root / 'tools/hum', fixture / 'tools/hum', dirs_exist_ok=True)
        verdicts_on = lambda files=None: limb_verdicts(fixture, name, root, files)
        check('DLG-1: the limb admits every member it owns in a faithful disposable copy',
              all(verdicts_on().get(rel, 'no verdict') is None for rel in owned))
        def sabotage(rel, change, label, refused, files=None):
            path = fixture / rel; original = path.read_bytes()
            try:
                changed = change(original)
                check(label + ' (sabotage changes bytes)', changed != original)
                path.write_bytes(changed)
                check(label, refused(verdicts_on(files)))
            finally:
                path.write_bytes(original)
        if page:
            # (1) one byte beyond the fixer's output. The digest rule would take it if the declaration and
            # the pin were cut again for it; the limb is what refuses it.
            path = fixture / page; original = path.read_bytes()
            try:
                path.write_bytes(original + b'\n')
                redeclared = dict(owned); redeclared[page] = dict(owned[page], afterSha256=sha(path), bytes=path.stat().st_size)
                repinned = dict(pins); repinned[page] = sha(path)
                hash_only = replacement_errors(name, redeclared, fixture, [('M', rel) for rel in sorted(redeclared)], repinned,
                                               git_before_entries(root, review_base, redeclared), owners, memo_digest())
                refusal = limb_errors(fixture, name, redeclared, root)
                check('RED PROOF (one extra byte): a page one byte beyond the fixer output is refused by the limb, even '
                      're-declared and re-pinned, where the digest rule alone would admit it',
                      not hash_only and any(page in e and 'not what the reviewed fixer produces' in e for e in refusal))
            finally:
                path.write_bytes(original)
            # (2) a page the fixer changes but the record does not name, hand-declared into DLG-1.
            stray = page.rsplit('/', 1)[0] + '/UNRECORDED_' + page.rsplit('/', 1)[1]
            shutil.copy2(fixture / page, fixture / stray)
            widened = dict(declared); widened[stray] = dict(declared[page])
            check('RED PROOF (not in the record): a page changed by the fixer but not named by the pairs record is refused',
                  'record names' in (verdicts_on(widened).get(stray) or ''))
            (fixture / stray).unlink()
        # (3) a page held out by ruling (SCI_B_W8B, R8 §1): changed by the fixer itself and hand-declared into DLG-1.
        for held_page, row in sorted(held.items()):
            base_bytes = read(held_page)
            fixed = fixer.fix_text(base_bytes.decode('utf-8'), [(p['action'], p['dialog']) for p in row['pairs']])[0].encode()
            (fixture / held_page).write_bytes(fixed)
            widened = dict(declared)
            widened[held_page] = {'beforeGitBlob': git_before_entries(root, review_base, [held_page])[held_page][2],
                                  'afterSha256': hashlib.sha256(fixed).hexdigest(), 'bytes': len(fixed)}
            table = dict(REPLACEMENT_TRANSACTIONS); table[name] = (review_base, widened)
            owners_w = judged_owners(fixture, root, table)
            keeper = owners_w.get(held_page)
            # The transaction that declared it before DLG-1, if any, must keep it and reject the change.
            before_dlg1 = [other for other in names[:names.index(name)] if held_page in REPLACEMENT_TRANSACTIONS[other][1]]
            if before_dlg1:
                kbase, kfiles = REPLACEMENT_TRANSACTIONS[keeper] if keeper in REPLACEMENT_TRANSACTIONS else (None, {})
                kowned = owned_members(keeper, kfiles, owners_w)
                errors = replacement_errors(keeper, kowned, fixture, [('M', held_page)], pins,
                                            git_before_entries(root, kbase, kowned), owners_w) if kbase else []
                kept = keeper == before_dlg1[-1] and bool(errors) and all(e.startswith(keeper) for e in errors)
            else:
                errors = limb_errors(fixture, name, widened, root, widened)
                kept = keeper == name and bool(errors) and all(held_page in e for e in errors)
            check('RED PROOF (' + held_page.rsplit('/', 1)[1] + ', held out by ' + row.get('ruling', 'ruling').split(':')[0]
                  + '): changed by the fixer and hand-declared into DLG-1, it is refused by the limb and stays with '
                  'its earlier transaction, which rejects the change',
                  'held out of DLG-1 by ruling' in (verdicts_on(widened).get(held_page) or '') and kept)
            (fixture / held_page).write_bytes(base_bytes)
        if sums:
            # (4) a manifest with a byte changed that is not a digest.
            sabotage(sums, lambda b: b.replace(b'\n', b' \n', 1),
                     'RED PROOF (a non-digest byte): a manifest with a byte outside its re-cut digests changed is refused',
                     lambda v: 'only its digest replaced' in (v.get(sums) or ''))
            # (5) a re-cut digest that is not the member's bytes on disk.
            before_lines = read(sums).splitlines(keepends=True)
            after_lines = (fixture / sums).read_bytes().splitlines(keepends=True)
            recut = next(a for b, a in zip(before_lines, after_lines) if a != b)
            sabotage(sums, lambda b: b.replace(recut, hashlib.sha256(b'not the bytes').hexdigest().encode() + recut[64:]),
                     'RED PROOF (a digest that is not the bytes): a re-cut digest unequal to its member on disk is refused',
                     lambda v: 'not the sha256 of its bytes on disk' in (v.get(sums) or ''))
        # (6) R8 §5: the Fallback MANIFEST.json may re-cut its page members' sha256 values and nothing else.
        for manifest in json_manifests:
            lines = (fixture / manifest).read_bytes().splitlines(keepends=True)
            base_lines = read(manifest).splitlines(keepends=True)
            other = next(a for b, a in zip(base_lines, lines) if a == b and re.search(rb'"[0-9a-f]{64}"', a))
            digest_at = re.search(rb'[0-9a-f]{64}', other)
            sabotage(manifest, lambda b: b.replace(other, other[:digest_at.start()] + b'0' * 64 + other[digest_at.end():]),
                     'RED PROOF (R8 §5): a MANIFEST.json value other than its page members\' sha256 changed is refused',
                     lambda v: 'not a page member of this transaction' in (v.get(manifest) or ''))
            sabotage(manifest, lambda b: b.replace(other, other.replace(b'/', b'//', 1)),
                     'RED PROOF (R8 §5): a MANIFEST.json key renamed beside the re-cut is refused',
                     lambda v: 'only its digest replaced' in (v.get(manifest) or ''))
        # (7) the limb module itself is bound to its CATALOGUE_PINS admission before it is trusted.
        judge_path = fixture / LIMB_JUDGE; original = judge_path.read_bytes()
        try:
            judge_path.write_bytes(original + b'\n# unreviewed\n')
            try:
                limb_verdicts(fixture, name, root); unbound = ''
            except ValueError as exc:
                unbound = str(exc)
            check('RED PROOF (an unreviewed limb): a limb judge whose bytes differ from its CATALOGUE_PINS admission '
                  'is not imported, so nothing is admitted by it', 'unreviewed limb judge' in unbound)
        finally:
            judge_path.write_bytes(original)
        # (8) a changed fixer, and a widened record: every member refused, not one admitted.
        sabotage(judge_module.DLG1_FIXER, lambda b: b + b'\n',
                 'RED PROOF (changed fixer): a fixer one byte from its pinned digest refuses every member',
                 lambda v: bool(v) and all('cannot widen the limb' in (r or '') for r in v.values()))
        sabotage(judge_module.DLG1_PAIRS, lambda b: b.replace(b'"pairs": [\n', b'"pairs": [\n    {"page": '
                                                              b'"Humanities_Teesside/UNRECORDED.html", "action": '
                                                              b'"cold-call", "dialog": "cold-call-dialog"},\n', 1),
                 'RED PROOF (widened record): a pairs record naming one more page refuses every member',
                 lambda v: bool(v) and all('cannot widen the limb' in (r or '') for r in v.values()))
        # (9) a Summer 1 manifest the responsive re-delivery declared, changed other than by the DLG-1 re-cut:
        # the limb does not judge it its own, so it stays with the responsive re-delivery, which rejects it.
        for manifest in shared[:1]:
            path = fixture / manifest; original = path.read_bytes()
            try:
                base_lines = read(manifest).splitlines(keepends=True)
                untouched = next(line for line in original.splitlines(keepends=True)
                                 if line in base_lines and re.match(rb'[0-9a-f]{64}  ', line))
                path.write_bytes(original.replace(untouched, b'0' * 64 + untouched[64:]))
                owners_s = judged_owners(fixture, root)
                resp_owned = owned_members(responsive, resp_declared, owners_s)
                errors = replacement_errors(responsive, resp_owned, fixture, [('M', manifest)], pins,
                                            git_before_entries(root, resp_base, resp_owned), owners_s)
                check('RED PROOF (a responsive member changed other than by the DLG-1 judge): ' + manifest
                      + ' stays with the responsive re-delivery, which rejects the change exactly',
                      owners_s.get(manifest) == responsive and bool(errors) and all(e.startswith(responsive) for e in errors)
                      and 'not a page member' in (verdicts_on().get(manifest) or ''))
                # (10) a contested path missing from the tree is a change no limb judges its own.
                path.unlink()
                check('RED PROOF (a contested path gone): ' + manifest + ' missing from the tree stays with the '
                      'responsive re-delivery', judged_owners(fixture, root).get(manifest) == responsive)
            finally:
                path.write_bytes(original)
        check('DLG-1: all limb sabotage was restored', all(verdicts_on().get(rel, 'no verdict') is None for rel in owned))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--base', required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(); root = args.root.resolve()
    try:
        changes = git_changes(root, args.base)
        errors = judge(root, changes, args.base)
        report = {'status': 'FAIL' if errors else 'PASS', 'protectedChanges': len(changes), 'errors': errors}
        if args.self_test:
            report['controls'] = controls(root)
            report['controlCount'] = len(report['controls'])
        print(json.dumps(report, indent=2))
        return 1 if errors else 0
    except (AssertionError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print('[FAIL] change boundary could not be verified: ' + str(exc)); return 1


if __name__ == '__main__': raise SystemExit(main())
