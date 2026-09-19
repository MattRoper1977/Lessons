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
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
PROTECTED = ('Art_Teesside', 'GROW_ASDAN', 'LAUNCH_ASDAN', 'Grow/Slideshows',
             'Launch/Slideshows', 'Science_Teesside', 'Humanities_Teesside',
             'Baseline_Weeks', 'BUILD_Estate_v3')
SHELVES = ('Science_Teesside/index.html', 'Humanities_Teesside/index.html')
COVER = 'Humanities_Teesside/David_Cover_Autumn1_W3-W7'
SCIENCE_PACKS = 'Science_Teesside/Teaching_Packs/'
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
    # END DECLARED TRANSACTION ENTRIES
}
# Declaration order is review order: a later transaction that names a path
# supersedes the earlier claim on it (a merged transaction is history; a later
# reviewed edit of the same file is its own exact transaction). The map keeps
# the last declaration for every path.
ALL_REPLACEMENTS = {rel: name for name, (_, files) in REPLACEMENT_TRANSACTIONS.items() for rel in files}


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


def replacement_errors(name, files, root, changes, pins, before_entries, owners=None):
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
        elif path.stat().st_size != reviewed['bytes'] or sha(path) != reviewed['afterSha256']:
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
    files = owned_members(name, files)
    if not files:
        return []
    errors_for = lambda *a: replacement_errors(name, files, *a)
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
        for name, (_, files) in REPLACEMENT_TRANSACTIONS.items():
            files = owned_members(name, files)
            if any(path in files for _, path in relevant):
                if base is None:
                    return [name + ' replacements require the actual comparison base']
                errors.extend(replacement_errors(name, files, root, relevant, pins, git_before_entries(root, base, files)))
        if errors:
            return errors
        cover_paths = explicit_cover_paths(root)
        label_paths = public_label_paths(root, pins)
        for status, rel in relevant:
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
    check('Rename-as-delete/add cannot move a retained lesson into the cover exception', bool(judge(root, [('D', sorted(retained)[0]), additions[0]])))
    science_additions = [('A', rel) for rel in pin_map(root) if rel.startswith(SCIENCE_PACKS) and rel not in ALL_REPLACEMENTS]
    if science_additions:
        check('Exact individually pinned Science teaching files pass as additions', not judge(root, science_additions))
        first = science_additions[0][1]
        check('An existing Science teaching download remains protected from replacement', bool(judge(root, [('M', first)])))
        check('A Science teaching download cannot be deleted', bool(judge(root, [('D', first)])))
        check('An unlisted Science teaching file is rejected', bool(judge(root, [('A', SCIENCE_PACKS+'unreviewed.pptx')])))
    with tempfile.TemporaryDirectory(prefix='glv3-reviewed-boundary-') as temp:
        fixture = Path(temp)
        files = {*explicit_cover_paths(root), *SHELVES, *retained, *BOUND_INPUTS, *(rel for _, rel in science_additions),
                 'tools/verify_cross_estate_unification.py', 'index.html'}
        for rel in files:
            target = fixture / rel; target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(root / rel, target)
        check('Disposable fixture is initially accepted by the real validators', not judge(fixture, reviewed))
        if science_additions:
            check('Disposable Science fixture is initially accepted', not judge(fixture, science_additions))
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
