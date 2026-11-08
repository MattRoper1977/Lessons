#!/usr/bin/env python3
"""Verify the Made by Matt Lessons/Apps cross-estate hub contract.

Sentinel: mbm-cross-estate-unification-lessons-apps-2026-08-08
The verifier is intentionally narrow: it protects the common platform shell,
Matt's existing hub wording/logo, URL casing, local/offline shell assets and the
fact that no standalone lesson or studio is changed by this release.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_module
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

SENTINEL = "mbm-cross-estate-unification-lessons-apps-2026-08-08"
# These pin the bytes THIS repository serves. They are not the cross-estate
# check — that is the --canonical comparison below, which holds these same two
# files against the site repository byte for byte. The distinction is the whole
# reason this table moved in both repositories within one day: the pins cannot
# detect divergence, because each copy of this gate pins its own local bytes and
# is green about them. Three versions coexisted, every pin green — Lessons
# ccfb0fd9/0841046b, Apps e3eb9b83/0958a73a, site b520cf36/095a29e6.
#
# This file is byte-identical in Lessons and Apps, which tools/pin_manifests.py
# documents and asserts after any re-pin. It had stopped being so: the two
# copies pinned different platform digests, and that assertion would have fired
# on the next deliberate manifest change with a message about the wrong thing.
# Both repositories now serve the same canonical bytes, so the table is the same
# in both and this comment can be too. Keep it that way — if the copies ever
# need to disagree, pin_manifests.py needs to learn that first.
#
# How the drift survived, with dates. 2026-08-13 (91a16b8) brought Lessons to
# the canonical copy and pinned ccfb0fd9 / 0841046b. The site then moved twice —
# 6bdeafa on 08-14 and bc67b82 on 08-15 — and nothing in either repository
# changed at either moment, so no path filter fired and both gates stayed green
# behind. The schedule that would have noticed is what theme-parity.yml already
# has, and what this workflow gained in the same pass as this comment.
#
# What 6bdeafa was matters. It inverted adultFeaturesAllowed() to fail closed:
# the account link, the create-account link, the mailing link and the footer
# mailing CTA now need a page to say data-mbm-adult-features="on", where before
# they appeared unless a page said "off". In both repositories index.html is the
# only page that loads mbm-platform.js, and neither declares the marker, so the
# two copies were affected differently and both were measured in Chromium:
#
#   Lessons  before  1440x900 acct=1 mail=2 register=1, mbm-account.js x2
#                     390x844 acct=0 mail=1 register=0, mbm-account.js x2
#            after   0/0/0/0 at both, details 12/14, cards 504, aria-live 2,
#                    pageerrors 0, 404s 0 unchanged
#   Apps     before  0/0/0/0 at both viewports already — the fail-closed reader
#            after   had reached that copy, so the sync changed no metric there
CANONICAL_HASHES = {
    # SW2-T5R1: reviewed inert vocabulary; no component styling changes.
    "assets/mbm-tokens.css": "2e78ad7348ee7beaafda1f33ff5b112e7fd121654d7a9d39fc1ec681dee00019",
    "assets/mbm-platform.css": "b520cf36a9c87af618e03ea534b66c261e8fd05e70d8eb5634f323aee9310698",
    "assets/mbm-platform.js": "095a29e61f8d7d549a5b58dd1aa1dd74b885416ebb09291ddb218d90ea740c28",
    "assets/mbm-theme.js": "5d711139ee95f2a9814917c516ffe674fbd52fd0b42c8fd6e22a1efbc19f002b",
    "assets/mbm-hub.css": "1643f51bcfe7f89923e908cf4f79b36a80d8bfa767779ab1c9cebe2e1a8b513c"
}

# assets/mbm-theme.js is not maintained here. It is generated from the site
# repository's theme.js by tools/sync_theme.py, and is that file verbatim with
# one header line in front. The checks below assert that exact concatenation
# rather than plain byte-identity: equally strict — a byte either side of the
# header still fails — but it lets the copy carry, at the top of itself, the
# notice telling the next person where to edit and what to run.
THEME_COPY = "assets/mbm-theme.js"
GENERATED_HEADER = (
    "/* GENERATED from madebymatt.github.io/theme.js — edit there, run "
    "tools/sync_theme.py. Hand edits will be reverted. */\n"
).encode("utf-8")
SYNC_COMMAND = "python3 tools/sync_theme.py   (in the mattroper1977.github.io checkout)"

PRIMARY_ROUTES = ["/games/", "/Lessons/", "/Matt-s-Apps-/", "/tools/", "/resources/"]
MORE_ROUTES = ["/stats/", "/members/", "/#about", "/privacy/"]
# apps.json is no longer forbidden from changing — it is PINNED.
#
# The old rule was "the source manifest must not change at all". That made adding
# a studio impossible: a studio add IS an apps.json edit, and it also touches
# index.html (AUDMAP + the no-JS lead count), which puts this workflow's path
# filter in play — so the gate fired and refused. A guardrail that forbids the
# repository's ordinary business is not protecting anything.
#
# Retiring the protection outright was the alternative, and it was rejected:
# apps.json would have become silently unguarded. Instead it follows the pattern
# the shared assets here already use and that tools/sync_theme.py established — a
# pinned digest that a TOOL moves in the same run as the deliberate change. Add a
# studio, run tools/pin_apps_manifest.py, and the pin moves in the same commit as
# the manifest: visible in the diff, reviewable, deliberate. Edit apps.json
# without running it and this goes red.
#
# resources.json keeps the blanket rule. Only apps.json was ruled on.
MANIFEST_PINS = {
    "apps.json": "a4a06b999b5f16d19f0a4a87952ea1fe53f4fcbe2c38bc702c51ba89140a6047",
    # Ruled onto the pin 2026-08-12 (Ruling 3): the deck install is a
    # resources.json edit, and the blanket rule forbade it the same way it
    # once forbade studio adds. Same pattern, same tool, same commit rule.
    "resources.json": "a15ddbb03f97137dcf7d684af74516613edd3c251bbdba2f1291cc7cbb0b15a9"
}
PIN_COMMAND = "python3 tools/pin_manifests.py   (from either checkout — it writes both gate copies or neither)"

# Explicit education catalogue release, 2026-09-05. Matt authorised a new
# browsing design, so the old Lessons wording comparison must permit exactly
# the reviewed result. These pins do not exempt a directory or a lesson: every
# named byte set is checked, including additions, on every Lessons gate run.
# Apps retains its original authored-wording comparison. This block is updated
# in both gate copies by tools/catalogue/pin_catalogue_contract.py after review.
# SW2 A hub wording explicitly approved by Matt, 2026-09-14; manifest/tool bytes stay pinned.
APPS_HUB_REVIEWED_WORDING_SHA256 = "9e5a4ac6c1e9bfb04a1c0186a82fce96aa03565a02dc3f18ee1569fb4b5664bf"

# BEGIN REVIEWED CATALOGUE PINS
CATALOGUE_PINS = {
    "visible_body_sha256": "204ce8e89ab6d0299e38e0d291417a1f8b539d7c2dc982edac7d41edfb14b2cd",
    "files": {
        "_sownb/CALENDAR_SPINE.json": "607ebb2e358b4c872de473444bdee1cd112677759af392e68137ecfb7023e489",
        "_sx3/SX3_PASSES_LEDGER.md": "5ea492a8cbc2d6f1108ceedeec6d0b80bc662467183f30e69850e7cfd2c0cc25",
        "tools/sx3/pre_ci_catalogue_sweep.sh": "9848b9e4e9ccab0bd8225d26d7ffa4683c59c249bff688f33c5d665671d9f818",
        "assets/catalogue/display-titles.json": "eeba20ae90f2627dbb00e4287caabeb58e9568c8d9eedbd7f8118eeeed3310a5",
        "tools/catalogue/build_display_titles.py": "4256ab6b07420af4ef090e57d32b8f29fcae88d9075d64750e52f17947dbd8a1",
        "tools/catalogue/check_display_titles.cjs": "ef27c6fabcafd05015ba988ee99b0906cabe1a519c1049635ee92b7e7c361ce1",
        "tools/catalogue/check_display_titles_browser.cjs": "5662cdb93c7796ead4fb9bb69ce94ac65fe1e29e103f00c65bd07a4d5129a7cd",
        "tools/verify_lessons_chips.mjs": "e417afd94ae4f3a450caab2edf4b6c41d14e4588f070d0ad822263e30a86cf39",
        "tools/sw2/check_tokens_inert.cjs": "a8258b89b5dd00147a0c8b18488a2dcf8102bc20d2ddf2fa1aa0863d25454674",
        "assets/catalogue/lesson-order.json": "4afc08fff7687f8fbfd6872d49132cdc411ce880db57420da389fcfe904f8df1",
        "tools/catalogue/build_lesson_order.py": "35a4c54779b800ae8bd949154d0d19fddb190f49ec18e62efdd86d03313f6180",
        "tools/ux2/hub_gates.mjs": "3d3120df94b1789041370c4045fbcc983635af0b30a0705447f18371bed98944",
        "index.html": "798d5572afecb8db10a516f9a0ed57d54b7d1dc5e220077a6be85d5f046b555e",
        "Science/index.html": "34fbe6ad5d02f887a430c3f822ff0c41b5442797d945e924b5d3259bd40adfcd",
        "Humanities/index.html": "497e5b88cf8c85f449a3fe81d2553c42e320e07e12cdaa0e6e4c393b3a18c1d3",
        "humanities.html": "bfb8f9383680b9c6d849931652db29289b92d5ed18c5f9616cfc0ede0614fa5c",
        "pack.html": "42935782c353525d28b9263a90a8c48e4b5ca764226444edfa68d6f664862be1",
        "assets/catalogue/pack.js": "da66512500cd92e7c7b2a58141ce98c903676b972ea71ba0723984eff12be7c6",
        "assets/catalogue/pack.css": "ba6c5c84bcff84c023f2f10ac345a159f48ea97b2e8eb542cb3e56435204d63a",
        "assets/catalogue/pack-notes.json": "f0a440b51785ecedb045666f1a5e44c082ff6f91786940636495837639609ec2",
        "tools/sw2/pack_notes.py": "a81a187002a69bcecca28c9c3130f546e1aae279d5af92cf750a6f9fb04c8fe6",
        "tools/sw2/stamp_pack_page.py": "7d751c25a0a00a1602388537df236c0f79dee6facd31be15fc6e7bce38512149",
        "tools/sw2/check_pack_page.cjs": "89f6a087381c5a34342dc5738f67ad0a3d9f4bc8cfb684da451125617a606235",
        "subject.html": "c70ef79bd0090c069167e1a2308baae69f89dc206783befede5baac84561b1d8",
        "assets/catalogue/hub.js": "cf8a420b8940af1e226d93eefd14e49a37899a99ccf5724137654de3774862da",
        "assets/catalogue/hub.css": "4bbfa8cb449ee9e022fe70df48b4d15cf1faab7e81bb09e8f6985a65a91fded6",
        "data/calendar-spine.json": "d199474b13c9d340add2c87165396d83712b0f1c9f8bd03b7b12e8fdf6af0d61",
        "Humanities/David_Cover_Autumn1_W3-W7/index.html": "4e25eb9ca8f9f93c720d88d945f3d6d79580f3362a88698fe7af75d146f01e96",
        "assets/catalogue/catalogue.css": "59abee137c41a8a015e42cf0b32d20b7f4e5fc8e3d236a1cd735322386bf8569",
        "assets/catalogue/catalogue.js": "a0fd3efc8356377effad7249be7222984ce92947a8143259148851dc399de5c7",
        "assets/catalogue/lesson-navigation.js": "42e579bbef3940c24ca4360319290820305a777330b8bff79152b2cb6aa077e3",
        "assets/catalogue/science-shelf.css": "b2b1eb328662d841add139ccfff107f985f17373f1ee82b8762475663097ab60",
        "assets/catalogue/science-shelf.js": "a59fe0c988a5de7d614afc6a36d7dacf14c6e3fa92c732740442e4914d00f356",
        "assets/catalogue/terms-and-styles.json": "68c916d863c8e3ff2991067a55ff2dae3e2328b0155dd77b12c2bca49d7561cc",
        "assets/catalogue/science-shelf.json": "6bfcac8579a72f8413e158b49460a8b853f284b8dc64bd4da4442c37e92edadf",
        "assets/catalogue/humanities-shelf.json": "3f6a3583f3658b79a544aeef27a778a283069e4842d763cb95728a703669d9a7",
        "tools/catalogue/build_catalogue.py": "4eff91f7ace9073a6612035c33e8556875d6165da83876ae5ec20a6ec11a15a8",
        "tools/catalogue/build_science_shelf.py": "396b6aeb7cb3cabe037b7af27877ae7a090e5aa1bce284409e400549d5204c24",
        "tools/catalogue/build_humanities_shelf.py": "0d58e1dd47c9c806b7fefc42437b47947853760e785eb3ed34b35148eea874cc",
        "tools/catalogue/build_science_hub.py": "b00b55dead2cc5566515259b2dbd0b082365823fc29bf10ba40c887256b8d5db",
        "assets/catalogue/science-hub-bindings.json": "01cb40d5580fbd6bbc3f3683647b57bb5ea6c2dc919557223698ca294497e179",
        "tools/catalogue/check_catalogue_static.py": "5eb7b3ebd11fbfceb9f8c812ec8b7dc5a02b3b162c0f78982f4e7afb6f4eb589",
        "tools/catalogue/check_catalogue_dom.cjs": "877ab8515ba5cbcbd8be32c52cfed067707b675d239250bdf2a68134382798c8",
        "tools/catalogue/verify_education_navigation.cjs": "48d00d8c490157059b6f21664c1b06e8c5af215575ee207040ee0c83c37d168f",
        "tools/catalogue/sync_shelf_card_titles.py": "d5e8fd850e5ac6340f0d1550ea2992fc03ef1fff8deeec144c73685042feaf7f",
        "tools/catalogue/HUMANITIES_STRAND.json": "d2d239ce547e15f39d7776e5de99c0436eebc274a4077f5f627b9f893ee435a3",
        "tools/catalogue/hub_sections.py": "3b201e96e05a124d47c6b5b1063c0df25d2b5c5cf4505aad7494663c7e92a90e",
        "assets/catalogue/shelf-base.css": "15d7b64ad06b9b27c5f03e91da30ba35c4ca01c1b12b1208b06bfefe5e6ff4e0",
        "assets/catalogue/humanities-hub-bindings.json": "cd199564a8c38fdae7425bc99d4d32ae523966ed9e491a590757b3951cd6d5b3",
        "tools/catalogue/restamp_evidence_sha256.py": "bfa35a1f979746d471d5af08152e20017bb20a1655490340c74ff6209652827a",
        "Science/Build/START_HERE.html": "acac26140f5aeef22292e6ce3831fa61aaf5e62432cc3998b340918c8bfaee7f",
        "Science/Grow/START_HERE.html": "d2bec305dec3212215c6f599cad3925c571f9a34ca6e85268893c8ed142170dd",
        "Science/Launch/START_HERE.html": "10b46e7cf26e3aa4b7f1fb4758a039bcbec7000bc2ec8d30dfe3ce0e0b966353",
        "tools/catalogue/SHELF_SELECTION.json": "e2e563a95c208c0ae1a3ef427e7e6311ec698692f90d2fcb4ae9011e906b9b5c",
        "tools/catalogue/HUMANITIES_SELECTION.json": "8bc58e21f2a3483d97eaf64dbfdc1bbbfeb3599b6bc0693377800a0054fcdf0f",
        "tools/easter/science_original_browser.cjs": "aae28a4166d41546cbe5b0acd0866eeaf5e6f47cd5b1949fc48ecb2d4c79a1ec",
        "tools/science_pack/browser_checks.cjs": "058c9bc1f06c876f2994a23d467d83fced683c6355eb92d0ef43986d3e28d72d",
        "tools/prepare_served_publications.py": "c52ffe6cbbc7bb6e056eb3eb27f0bb9a36bb34d2aa86e5d3e02a63aa3653d3a1",
        "tools/test_served_publications.py": "02f9cd6defc7949c3198470ca28c8476c904adc54344884180b843ba48b8a88b",
        "tools/verify_served.mjs": "96eddcc5a76979e552f6c8c46da240113ccf414361eabdc704146831ad633cc8",
        "tools/test_verify_served.mjs": "2786e345a401f27a4ec29e4af95b3363ea01b9fa99e470bf4413281db0fbb257",
        "_sx2/DECISIONS.md": "98959aafb9360877134158427865aabf69aeab094b499b58c31451fec9aca93e",
        "tools/ux2/resource_sizes.py": "2e8d36613fb39e3114c2006337771ddc9c724f9b6333a6e05cfed4e646e4224b",
        "tools/ux2/s1m_published_input_proof.py": "95b82480a9fdbb607fcaf3077d1e58dc1e9a5eafd96581fdbec281c979de1d10",
        ".github/workflows/s1m-published-input-proof.yml": "fcc9f4c6b6a550873bda92346bb73e47d9ec0cfe95664a8eec66d0e7947dfb76",
        ".github/workflows/watch-main.yml": "9a468937b9eefbcdb010f9eed9a2b48f4111761202932fadad680cc3b477f3b6",
        "tools/verify_v6fin_w7_r1_r7.py": "73fc89a3f9c034ce8ad45b22b443b7bfe0da448ee1fff02c46c62e07790822ff",
        "_sx3/FENCE.json": "03541f944d0ea861a32c476034553b4ce3d43acf89edc5264f3808b4079e9c5a",
        "_sci/HELD.md": "2443f349c9cf1784e1e91ed1e93851e04cd50795403a5c1310c07946aeedd07e",
        "_sx3/RELEASE_LEDGER.md": "85605383b75547480a21388ed9003ac2ccde89b34373a45454595c2d9e0102a1",
        "_sci/WEEK_TOKEN_DISAGREEMENTS.md": "2ece32469fe9212d22dad5cfe7741b7f6cd06bba5429cbe74cb52185161c2858",
        "_passhumd5/CHECKS.md": "53128441515e578baf2e756bf9e49186d0ad95ddc44675f8f02104d393a79d83",
        "_passhumd5/build_text_index.py": "6239cbfed4f5a6b239655de67bd20aa4bd377205806ab479a23578a85b5eacd0",
        "_passhumd5/scan_gvocab.py": "01baaadc2d96cc06e7b458dc19b9734d96d84291e2d1b5c8ab43b08ec43edb58",
        "_passhumd5/p0_cell_map.py": "82d5786ba53cceedf35565ddebee3462c5e33a82536e4376ec73f635539a9158",
        "_passhumd5/CELL_MAP.md": "7c99de6f4ebae890cf2bf989bfae0298fbd3202dd41365a674e079d7e41c57e8",
        "_passhumd5/RETIRE_LIST.md": "70712b696a228d8656eda29fe495ac3084b38b008cbcdf84b0c6ea94c696cdd5",
        "_passhumd5/P0_SOURCES.md": "32b199b75456b911a71eec8469a4731883b831d1689cd3068f42c8012a48ff0c",
        "Science/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L1_Topics_2_3_Assessment_Introduce.html": "9130c85767d735e19fbc7b9e0dd1b314bd5db58f7e828f39bf35976f26741d7a",
        "Science/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L2_Topics_2_3_Assessment_Explore.html": "cae2d988234b575f7b9c97d0b6907dda83fcb513ed00e6a4e40ca23ee7ff59f5",
        "Science/Launch/Autumn2_W7_2026-27/SCI_L_A2_W7L3_Topics_2_3_Assessment_Do.html": "45b168db37157559bd29fb8c0b89582d3db97e0772f7a64f6cca40ebd0466928",
        "Science/Launch/W14-W15_2026-27/SCI_L_W14L1_Genetic_Condition_Research_Introduce.html": "3026dec2f838802ce76cfecb2919dfc665f097b4e03e47f12bbfeb7c664258a2",
        "Science/Launch/W14-W15_2026-27/SCI_L_W14L2_Genetic_Condition_Source_Evidence_Explore.html": "e7d58d365b6f9e694f41d656602013715214ec66d097b2039e1fc5978b3afb30",
        "Science/Launch/W14-W15_2026-27/SCI_L_W14L3_Genetic_Condition_Presentation_Do.html": "a87e9f650c2ab23de5361c97fdb6612817b793c7609392656255a7f3fd15cba0",
        "Science/Launch/W8-W13_2026-27/SCI_L_W13L3_Inheritance_Probability_Do.html": "2e53abf3402d40c00e9931e97a498376689e092143def2b5ef9ac032b3434582",
        "Science/Launch/W8-W13_2026-27/SCI_L_W9L1_Cell_Cycle_Introduce.html": "c0b48159102b3cebf72fcd91deccaf49bd9a2083d49b3fc2e9df43892971a436",
        "Science/Launch/W8-W13_2026-27/SCI_L_W9L2_Mitosis_Sequence_Explore.html": "73b82303adacbbfd2f8945514a62fe09805b3cf7ab905a88b11900bd1abd6f78",
        "Science/Launch/W8-W13_2026-27/SCI_L_W9L3_Identical_Daughter_Cells_Do.html": "df5087e190937e8df9213f037023fc77d4c20f5b351ecbfb5884f1fcc90e9ea6",
        "Science/Launch/W8-W13_2026-27/SCI_L_W9_Copy_separate_divide_Classic.html": "280856e8f64319de2e19b0f7766ab954c7138adb27bd5678fa08a52899a42e33",
        "Science/Launch/W8-W13_2026-27/SCI_L_W10L1_Growth_And_Differentiation_Introduce.html": "340c86768c9f6fe8a0bfecb5082aae28710842b27ce302a655b8e6d34ea3e860",
        "Science/Launch/W8-W13_2026-27/SCI_L_W10L2_Stem_Cells_And_Meristems_Explore.html": "3f4955539b7f6861d6ac7388aaf06491e182e9c906d58d448cab5ce94b5a92c9",
        "Science/Launch/W8-W13_2026-27/SCI_L_W10L3_Growth_Stem_Cell_Data_Application_Do.html": "567e92ad6b30eef8c38d9ba34e125334b6c4b0580502341e940c74be2b74c6ef",
        "Science/Launch/W8-W13_2026-27/SCI_L_W11L1_Stem_Cell_Evidence_Introduce.html": "39494550b4d70cb3b21c8c48439bc72f0d2d8b89190e4be6d2be3be6a19fcf38",
        "Science/Launch/W8-W13_2026-27/SCI_L_W11L2_Benefit_Risk_Uncertainty_Explore.html": "3a8d4a33ae5aabe7d5acf1c4aca3d20de8927f6cccd8753818527f1d0f55dfd6",
        "Science/Launch/W8-W13_2026-27/SCI_L_W11L3_Stem_Cell_Discuss_Do.html": "f349213fee22df9d180cf18a31b9b920d28cd4c6dba6e07ce906e85e15288e3d",
        "Science/Launch/W8-W13_2026-27/SCI_L_W12L1_DNA_Hierarchy_Introduce.html": "f01bd523431528632da86bbd9c02c38c6edfe47bffd764f2c4c2c69411fb3752",
        "Science/Launch/W8-W13_2026-27/SCI_L_W12L2_DNA_Structure_Explore.html": "e7aca0789b0a111e0efc5631a6c1d9409ed2dcb2686693e3528a56d2154f99d1",
        "Science/Launch/W8-W13_2026-27/SCI_L_W12L3_Fruit_DNA_Evidence_Do.html": "6e2fff14cfb09c791f80bda13d6386df6d447b3a754db3e2211556f2ba6dec8c",
        "Science/Launch/W8-W13_2026-27/SCI_L_W12_Zoom_into_genetic_information_Classic.html": "058defef68f87f80bed2f6d41ec15fca48b9808021fde468606155cbf8c526a7",
        "Science/Launch/W8-W13_2026-27/SCI_L_W13L1_Alleles_Genotype_Phenotype_Introduce.html": "4d0c893510792f08f75472fce3c2ed234299cab1db4129d93861ec2b5322d61d",
        "Science/Launch/W8-W13_2026-27/SCI_L_W13L2_Punnett_Square_Explore.html": "aba9608d6f10df7f63ae5a6bd0ce63af012dc6389f3708cf747ea19ea844ad12",
        "Science/Grow/W8-W13_2026-27/SCI_G_W10A_Solar_System_Research_Explore.html": "eae7aa0751ba8ffd84a27a316b9e9af1e6e56d94704097b8e5ec7cd0fcaf73a1",
        "Science/Grow/W8-W13_2026-27/SCI_G_W10B_Solar_System_Presentation_Do.html": "18c99f9225f39ec3e6e4d5aecfc94ab8cf208fd2e398e2dfe12f7b2dfb2c31c6",
        "Science/Grow/W8-W13_2026-27/SCI_G_W11A_Global_Warming_Explore.html": "5f9f9c657e4e28808275fc8dd0869224455cf21d2903ea377c3406b3cca7a8e7",
        "Science/Grow/W8-W13_2026-27/SCI_G_W11B_Climate_Action_Do.html": "5ef530499159bcb9ce80a063e110ce4047545f7a70444080afda495b2c7fa7dc",
        "Science/Grow/W8-W13_2026-27/SCI_G_W12A_Science_Connections_Explore.html": "ca2448cb5fc5c946694e844298b53291dbc7872377c443afe90318b7d42ce944",
        "Science/Grow/W8-W13_2026-27/SCI_G_W12B_Science_Answer_Lab_Do.html": "4ce4be0d9399e88b600e31c1eac960a93b2f1601f733e17aed2cfdbcb88a3b43",
        "Science/Grow/W8-W13_2026-27/SCI_G_W12_Follow_the_warming_chain_Classic.html": "0453527f763eeed83f1c45f9a53b02834b2700c12b373a6dad0db1b9269cb43e",
        "Science/Grow/W8-W13_2026-27/SCI_G_W13A_Rover_Rescue_Plan_Explore.html": "40d80695974510bc6d90a2daa6e25741780076cf43637d11f42b581b600c0ceb",
        "Science/Grow/W8-W13_2026-27/SCI_G_W13B_Rover_Rescue_Investigation_Do.html": "94e0f4685d789407d127a2c5c031676aa62277d75365f681ad217172550d1a77",
        "Science/Grow/W8-W13_2026-27/SCI_G_W9A_Spherical_Bodies_Explore.html": "861655ebad796f048961dd3fbb7d7b37c4fa19b124b3b22dadb7b19b0d2facc0",
        "Science/Grow/W8-W13_2026-27/SCI_G_W9B_Spherical_Bodies_Do.html": "4ad909faa2bc690cdb530cdd02555b2c216c27d5a4a8f2986e4e29814dbce984",
        "Science/Grow/W8-W13_2026-27/SCI_G_W9_Turn_Earth_explain_the_sky_Classic.html": "178c695fe2dc166a80abfd26e41174e28ecfa39d4700db0870d7ee27bbffd6e8",
        "Science/Build/W8-W13_2026-27/SCI_B_W12_Give_a_rock_a_job_Classic.html": "509f38056bd09e903c70b0426ac55ab7ff73f7da10261a97eec11d49d7b27d1c",
        ".github/workflows/glv3-verify.yml": "4bf27ca7471a21359e35d1bc7277c5fa0adeb5f31a47c769f192165796037088",
        "_glv3/tools/verify_change_boundary.py": "68221db421a7e74621f6e990c982bc5f5535c819c5703e8e216ee5f3b73c93f1",
        "_glv3/tools/browser_verify.mjs": "737ad30f297e061407161743f017614179cc6c56f1c9a3904bbe7c98df38c888",
        "_glv3/tools/chip_gate.mjs": "16cdd5c0ad3745c57340ed0ec6a208d221e4793bfc9b1cd9bc703a6c2613dd9a",
        "_glv3/tools/catalogue_membership.mjs": "4d7ab03e23ee0d3c3fc934f4f0a901afc61169754db099f4f5c24dd9cce058ec",
        "tools/humanities_resources/SOURCE_MANIFEST.json": "9d2972aa39fe12220de92aea2230fd8bdf7bef765d5b7cf2227c440026f546a1",
        "tools/humanities_resources/DOWNLOAD_MANIFEST.json": "fd0a9349db9824e2d03fa816d96a8eae2c974c22e33c03223dd72e85e17f2190",
        "tools/humanities_resources/CONTENT.json": "335ea55d7964d8095064e2c67c95fbd8d65e28b4d1ddf25f6e4ee812abd29b98",
        "tools/humanities_resources/ORIGINAL_MEMBER_MANIFEST.json": "c4ce9e5a0a5d966ee31f401ae476a2dc10a43aa8dc749e09b2cef87b745db073",
        "tools/humanities_resources/build_resources.py": "328d5d92bf37df27cadabbf52b832a4dc102b31c6ccaddb27737a2930fbcb4ed",
        "tools/humanities_resources/check_resources.py": "ec5383e3a34cbff999f190b0014a4a73e00a3a29e2714498f7620fd638dc2aa5",
        "tools/humanities_resources/resource.css": "1aed9aaca0d73a4b200c4e5d0977e73f4e906c747d7340c7a62f4197a8344bae",
        "tools/humanities_resources/resource.js": "ad40afed95490bfcce92dc062da46e1b27bcb96bdc80e37eabdfe02bf6ffc446",
        "tools/catalogue/TERM_AND_STYLE_EVIDENCE.json": "016ed3ab483cc8876adf410278ddb4d2a95dd2a656581269807b5d4cb9caf877",
        "tools/catalogue/TERM_REVIEW.json": "9395de4c2803a7bc2a679cf0659c9df3c41c01e5ac60c0a2d39249414bc12de8",
        "tools/catalogue/SCIENCE_WEEK_BINDINGS.json": "9fa98ad78b0bd3c3f3ee15f88a7b2fd40eea810e6c9fb65ee93b3c5192888071",
        "primary/year5/science/autumn/forces/Lesson8_ExploreGravity.html": "20047720bf1d309055abdf232d341b6fd99b833631efa0bcbfb3dabed9671196",
        "primary/year5/science/autumn/forces/Y5_Forces_SoW_and_Plans.docx": "ca36cfd92f1c768ea66f0eb748d47e6227f67569f77b5472d0da13d03f92f2e6",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W1_People_Special_To_Me.html": "030be544f76147106e1a7f817ddca11142fcbaef168c28ef2397316a069f384a",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W2_A_Special_Book_A_Special_Place.html": "7589b8190c24a8810f558a2b2f550e9a899f9d5df0a5ad0e3fd26d931b6947ff",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W2_People_Who_Help_Us.html": "7b90dbfb9e82e1a4d20dda3703e68086c5367643bd3b58c8533e97836dc80521",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W8_A_Festival_Of_Light.html": "a91c419bde53ffefe77b17db0e8ebb9973b4df447690c6a41a94c76210a654f5",
        "Humanities/BUILD_W14-W20_2026-27/BUILD_HUM_W14_Festivals_Display_and_Reflection.html": "bf14c15092537d25d1b067d5cc32bba8b5ded673e2d8247b352b0431c8abbe59",
        "Humanities/BUILD_W14-W20_2026-27/BUILD_HUM_W15_My_Week_Timeline_and_Caring_Stories.html": "97e71086dcda835b431f9cf94d545f802429faabbb0bd76d26a30987c70ae8fc",
        "_sx3/CHASSIS_CONTRACT.md": "7bcbd67432df1edcedcccacffbeae56b16ab933cea6dd6ada761a263781930d8",
        "_hum/EVIDENCE_LIMB_CENSUS.md": "43870031ec3c0059fb03ed16180a40d630b2eec63a4fa29cbafd3ccee7415e4d",
        "tools/hum/evidence_limb_census.py": "5d360d643641dd27784f5ef06c850ef20b424d112e6de1a98d1d5768c2ef69e4",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W1_Beliefs_And_Worldviews_Around_Us.html": "19bbe9d6e0befebdbd502e83d42962f498bd66f0fd56809cd183a30b4339882f",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W1_Migration_On_A_Timeline.html": "dbf44fe5be6e352cd6210d1b7426c15bfd4e00dd6f02a9f1643ab41d90ee75ce",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W2_How_Beliefs_Shape_Who_We_Are.html": "585b7c4a5b8b197b698e1a25753098b8d899b8e5866e6c6d1327aa2a82f6eeac",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W2_Reading_A_Migration_Source.html": "2c505b209aaf25af14425d63dfc648939257a8f3bade68fd3226296b7da80287",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W3_Why_People_Moved_And_What_Changed.html": "5a389f52fac689814f978804cfa9e1213d9b16df21c74f3219bea27df2edffb2",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W4_Diverse_British_History.html": "1f13e87e4f3f11233b417cf1e05c038e83de2bec3d8c49bfd092b9c5527c7b4f",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W5_Was_It_Significant.html": "9ac862ecd06d8438d8f8a1b4a4a112f5fc95e7136a19226080c6e52c2583fcd8",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W6_Planning_An_Account.html": "a09c410a1b04098e91327b523c04d4877b40343e3c2f01e41c66f65d01002708",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W7_Writing_And_Marking_The_Account.html": "015a5514cc1145a35084834d470f3138a0b41359d43c6e7385a539a81fc36e0c",
        "Humanities/GROW_W1-W8_2026-27/GROW_HUM_W8_Finding_Places_In_An_Atlas.html": "6739b5cb8d059f972012844f20d6a49249b5bec231cc018285675a44dcdca7be",
        "Humanities/GROW_W1-W8_2026-27/GROW_Humanities_W4_Explore_Hanukkah_And_The_Theme_Of_Light.html": "cd82d9e3ba3bddc820e4e6980338f8055d42e4f7c4279532d4eb6a2d78605f10",
        "Humanities/GROW_W1-W8_2026-27/GROW_Humanities_W5_Explore_Christmas_And_Christian_Belief.html": "e21ff0ff140cdff349c3e6f8dc5bc314be9e8d6be05d888cb8008382b5a85daf",
        "_hum/LOOP_CONTRACT.md": "c2574700e93b178c32138a27ba05c5496f3f8f83736154ab1c86b71f552bd08d",
        "tools/hum/loop_adapter.py": "8f4d7cf3435af81286a0fa8ac40e527fd08dab35aba4cf9ca4b69c99e2f17d58",
        "tools/hum/deck_dom.py": "98cf5f472ef46d2b015779d61bc98b49190066018b2fca79b5e893b88bada4ab",
        "tools/hum/STAGE_IDENTITY_RULE.md": "19a8e7883ee47e9d5a4c39effbf912e906d6c91454e3ec67ef182801b8382a51",
        "tools/hum/render_proof.cjs": "35aee6aa2d3b11367c310258160c7e01dabc41913e767968f88c27f6f8ec899a",
        "tools/hum/verify_loop.py": "83b87724d4d9ca22ea55513f99e0df8d7f5dfded247b242a4c3be56693e77dac",
        "tools/hum/fixtures/aut1_twelve_stage_v1_base.html": "ab9f6abd62ef33df3bad621267aec70a5ccad6f765de71d623e55f13f0a5e2c5",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W1_Belief_Identity_And_Belonging.html": "9e7622bbf1d552bb71ded11ec4bd99a97ae9aee4d1378ad8bc4932247a3773d3",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W1_Migration_And_Identity_In_Modern_Britain.html": "b965d521d918cd24408059c8d940966c16c138f2a8c40fc51860e2f8d67ea9c3",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W2_Cause_And_Consequence_Of_Migration.html": "c49b62b36952fbe4da9cbd19dfc7401a628ecbc423451a188fa3fd9b55d8dd0a",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W2_Two_Worldviews_Side_By_Side.html": "7e104b814657bc838060f688d89724b789346fa9a45700653765cefeacd4160b",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W3_Can_this_record_prove_it_Classic.html": "d92ef8c4d64b20914294b4abe120033a9ab873cb32bd3aa4299c35dcb01dd33d",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W3_Evaluating_A_Digital_Archive_Source.html": "a385de10b4db2e5a5370ed24db214bd0ec0ade59d2604eae12b51d3d74091204",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W4_A_Timeline_Of_Twentieth_Century_Britain.html": "24f7ea8a63f02f88a291a59b65db8c878e8ae85a32d831b79736b31113d10559",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W5_Who_Shaped_Britain.html": "0a1a646dda79dd7db040af551128294caef16fba6e3e90a4dae233d99b34fa7e",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W6_A_Structured_Account_From_Evidence.html": "55e46c6599d930327833d95493f1017fba4ba76c64ba4fddbc540f9ae49985eb",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W7_Source_Based_Assessment.html": "a42f61b9de0ed5b9d89ab18cdde017dff34dd789b43219011a5a563ad7cdab87",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_HUM_W8_Maps_Symbols_And_Grid_References.html": "7dcb2d67927b3d74376f4e1c822aac82d036210af59e94cecd8647ef8d6fe7de",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W4_Festivals_Shared_Values_Day_Of_Peace.html": "2495d9a762c6d434c5d1cbac3b0ac63d8f7562b2f38a98d863d0e3d201f16239",
        "Humanities/GROW_W1-W8_2026-27/GROW_Humanities_W6_Compare_Festivals_Of_Light_Respectfully.html": "d4da31012106415fca6641fcd1d5bcdd7e9213cef98897dcab972f0602d850e4",
        "Humanities/GROW_W1-W8_2026-27/GROW_Humanities_W7_Reflect_On_Remembrance_And_Shared_Values.html": "3fe17c6e46638def69dfd72132605e4540f289f272cc87ca2d9408c7525a5cfa",
        "Humanities/GROW_W15-W20_2026-27/GROW_HUM_W15_Rights_Timeline_and_Belief_Resilience.html": "dd22c4d6f96f00a9f6a1174672c2145dafa34171d1148f65b0c68b1c4b1dae03",
        "Humanities/GROW_W15-W20_2026-27/GROW_HUM_W16_Sources_Campaigns_And_Hope.html": "8acbafb35b90a104d1aad179c188d5e29e4c99e5a35db033daa7087d8edeb07e",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W10_Connected_World_OUTSTANDING_V3_1.html": "a4b6d63afdc7d3a7ec81d4f3ba8b095b75f55b1d6d6e4e534d0f93b1566bb596",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W11_Light_Across_the_Map_OUTSTANDING_V3_1.html": "3ddc21faaf0d98be4304ad63bd8c659b556676288fc0c4ac89b55c622b543a64",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W12_Compare_With_Care_OUTSTANDING_V3_1.html": "3fcb995013519cafcc155e7ad11c3cde94913149dd8362233a3c67e418c0c583",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W13_Belonging_Briefing_OUTSTANDING_V3_1.html": "a8fc4a21540e85c6ff00ecc04fcfcdcf27ffaa3b2017022ee99ed7d5299f5170",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W14_Map_and_Belonging_Challenge_OUTSTANDING_V3_1.html": "6935c53274bf191f7cfd0c62c0c03bae85e60e44c00b85f0abfa19b4dd81aafa",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W9_Pinpoint_the_Place_OUTSTANDING_V3_1.html": "69a9285e4e671645754b80c8fd1624d699977504cfa40aacf770acf51a465024",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W5_Structured_Explain_Response.html": "adaa425bab46005aef4cf6c6d6997760ff75818965a7461af2f145c974016762",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W6_Remembrance_Peace_Across_Beliefs.html": "b0e93d11cd494ec361058214da3193f2721cd6531fbbc99af4a0b3c888dad351",
        "Humanities/LAUNCH_W1-W8_2026-27/LAUNCH_Humanities_W7_Belief_Identity_Assessment.html": "1b2c8e41fe9e740614b0685c6ab594614518acd15788905282d84cbe7d1e239b",
        "Humanities/LAUNCH_W15-W20_2026-27/LAUNCH_HUM_W15_Conflict_Causes_and_Ethical_Decisions.html": "36aad344c9e91f5c1fc4aeb28c111fee64864868e28ee7dd36252d0c6caa1047",
        "Humanities/LAUNCH_W15-W20_2026-27/LAUNCH_HUM_W16_Steps_In_Law_And_What_Comes_After.html": "1b2b12b93d4bf4583aca5356151b2c469d7ee3ba93d502d6a943686cb93a0b42",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W10_Settlement_And_Urbanisation.html": "127026a754e180800e9202a552f938b2af446730bc5e533f2aeb822b12692e64",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W11_Local_Fieldwork_Collect_Data.html": "3f83f53d6a8b7a02d397aa554f6a59977a04c9a1beb3bfa532949f23ed4eef92",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W12_Fieldwork_Data_Graphs.html": "4018cf72fb54cad4c3d6e21d4dcbdec6117554331546fefbd4b756684cc83a8f",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W13_Contrasting_Places.html": "66517aec3c3bf97dc4eb536535aaf009bfb8b91a0f0088b04c7d6d1418fcafbf",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W14_Fieldwork_Enquiry_Write_Up.html": "1e200c6fa11000e66d7e529135876de9c2481ab107f4cf1a68cdc77691f21994",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W9_GIS_Layers_Reading_Place.html": "8544e086b5e4a6c611982f289fb697626731041eb1cbbd77a4f3e454928aba61",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W3_Places_In_My_Community.html": "1ed894d2443de648e0deb5aaf4615c6b92b0735abc27c109947a3c31c137d5e6",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W4_Then_And_Now.html": "a794d0c8095c8b8a29619335db783ced6742da4bde938161312908eb78c34a04",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W5_Same_And_Different.html": "7e8bbd4524445a76e3f22ea8eab447ba4ab7b7d5f44704e74b7633bef2e5f8a3",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W6_Our_Class_Map.html": "3ed142de2819ad74040c4ec8a55038225e41f98671a82c018f0a1c4f3a36b5be",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W7_A_place_in_the_group_Classic.html": "cf3e2f57f2b4d098f3e55a348579bf60547da0d2b0c1aca90d3118816c0d05be",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_HUM_W7_Groups_We_Belong_To.html": "3dc05abc16c9baa2cb2978226d0f047d84fc8f2583fe2ba3da9d9a5a20ccf063",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_Humanities_W4_Show_Respect_When_Handling_Special_Objects.html": "3b884a498d58b04130fe97ecfae52b60ad8c13687d4b82c8581c5a9c7f89670a",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_Humanities_W5_Notice_Similarities_Between_People_S_Beliefs.html": "701831c9205b4756b9397a583370b68f774110bcc11863380622eb816a1bd91a",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_Humanities_W6_Reflect_Quietly_On_Belonging_Day_Of_Peace.html": "788f671f8221b03e2358371e620cba251f03879c7ac223aaec265118b6cd2665",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_Humanities_W7_Share_A_Special_To_Me_Object_With.html": "be33baa63d4523febdbd0c4f6826efe272b68958c3be44b560a349b0ebd05266",
        "_sownb/vb/evidence/a2r/classic_v2_fixture_minutes.json": "110b377332e73395c6f2f2505674e25d71f329c77f2d00cefda6d0c4c9166c63",
        "_sownb/vb/evidence/a2r/fixtures/classic_v2_v1_base.html": "c9ec2ea5fcd7a7b1c370b4e7680a0580a4f69b33b6e6a7023b648988924dfece",
        "_sownb/vb/tools/classic_v2_contract_selftest.py": "1a571a20066abf020bbbba9ec7a6b99a28c627f04cc3165687ac87eae91c979c",
        "_sownb/vb/tools/reshell_classic_v2_contract.py": "ebf77751927f961453f73607e700378729865e44342642cf80817c2a703856c1",
        "Humanities/BUILD_W14-W20_2026-27/BUILD_HUM_W16_Then_And_Now_And_What_Is_Fair.html": "8513df51ec2501cbfe57d63892347c235cf101cfb6fe63eebf868079470b7dd5",
        "tools/hum/admit_transaction.py": "af6d1bece8f0219c316d2f13ca79573a1c9d2a7be299511ba95396bd1fc769e2",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Knowledge_Organiser.html": "556d3d5d29e29c0f25f27d0892bb17c67ba9647e77551486586a0473a40d01d0",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Lesson.html": "7d956788596bcf16e8e41711f216136661dcf8900b510e27667e84498702c48f",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Pupil_Resources.html": "a17b507c6283060aebd135e10bf7ccc5e2b22cb2a3b152ba4b127dcb9a9cf94c",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Knowledge_Organiser.html": "2ea53fb30d70a48967f945ba2d4d1136c378561cd18ab8d848b4282e2da91367",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Lesson.html": "8ee362ae9c1a58f7571a790e54f0a01f199b9277de641e1b908e9358c6325530",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Pupil_Resources.html": "89990eb982ab3deb714ceb90bc58d4095aa52149d22b2e8a8092e85d1408dca2",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Knowledge_Organiser.html": "824bd892a835fdc21cd5a005eb9900f8b4871fc892ebd88c87515cf0186cb561",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Lesson.html": "41c391e182af1604283b74531bb6be5af4a4fd88a5ff2d6cbad2299ef4a671b4",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Pupil_Resources.html": "100ab6a30ce901bbc8fb3fada5584070512cbcbcc942b9346dd08c4ac1e277f2",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Knowledge_Organiser.html": "42803ade88d4545eae2d737d3a5dbe6b434e8606289e92a914b153cb0824c994",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Lesson.html": "39fddade46a9d657c2a4a68da5574cd04b72057e504401bf6a1a87e44c3f235e",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Pupil_Resources.html": "0f857523e0fc30079aa29ce4692ef0c9d3fc8acbea81c7a100517940fcd4858b",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Knowledge_Organiser.html": "06b68734e46fd57805bf935d4b29215e6722cf8279ee646ae6cb20bbc9acb16a",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Lesson.html": "88d51a41d020e1a4a5ed81d73438cd115c15f0412ce110ebae1864c9628f46eb",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Pupil_Resources.html": "01ca55af085df21e5098f50624e4f46d6261cad627f0e7400714e0723e4be1f8",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Knowledge_Organiser.html": "bd6d34df7c9686981de13f28d708790df9e436462784fbe3e66d0ff446a58d50",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Lesson.html": "42d6caf7360d6aa2716847602986edf75280408f812221594a0f14793031a7d1",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Pupil_Resources.html": "5d5ec53e4dd803b6553815487ba543d540b975676d3ec9cccbec3959908c4dae",
        "Humanities/BUILD_W27-W39_2026-27/START_HERE.html": "96e3afcf562a827dd2b235d022748b5b53b59adff43d64d5dae3c39e3ea830cc",
        "Humanities/BUILD_W27-W39_2026-27/Sources_and_checks.html": "dac061e62f58aae8c7c803ae3bc55155a85544a20873c61a6953bff154f7318b",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Knowledge_Organiser.html": "304f7b59f07602dcea6463a35491591047cdb7bca7d14a2ec8c56e2c24e3803d",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Lesson.html": "2980650e22db0798c22b5ab4dc9bb95e13b67bd69bbc58f1b1b2badab31b61bf",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Pupil_Resources.html": "7c13f8cabbc820a97de601ff128bb6153f99821051053edd9893b07f183b4306",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Knowledge_Organiser.html": "a42bbd596ed226d5899f138011467a9cf3839fb86b2f9eea5b19eba8e13c6ae7",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Lesson.html": "f55a34ef3e9a07f140924c3af73fd000ea9f19e4710c1f4cf112eb8f123a57ca",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Pupil_Resources.html": "e87732ae765b20646256cddfb5716cecb70fc04d708c7d63f5ff695021bd5701",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.html": "065bdd2a52f0fc5ab531e884fffad40c0367acd1b003932a160b903aba0356b3",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Lesson.html": "28eb2583b6962b15a9566cc336cff096217ae0b3219dcda6b280c68526514473",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Pupil_Resources.html": "c0ec815f418dfaef8e1f99e2e4adabf0bac2b3db1edede34bd2cdd473da16fb8",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/Sources_and_checks.html": "5ac92240747e170ba0614f7b3d75b75821807a35cd80070469d14d39f7c58cd8",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Knowledge_Organiser.html": "1f30e9fbc0857fb5034bf2a0865f3117dc533812992c13c44ac3de38720a0069",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Lesson.html": "cc5731dd79cf8d1109e997ebb9beccafcb0ba2951a305974e7aef3b0a2a804bc",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Pupil_Resources.html": "9f1dc7c4b3541e25828b5bc2d989ab6e473e2e2fcc1e6e56bacc34677b458f18",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/Sources_and_checks.html": "0dfd4a4c0735cd9a5ab1a3afccf041acbfc3a03f73665312a41fa43390eb9136",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Knowledge_Organiser.html": "b3b9079ae07d5fd47c126db1a2ac8d83fee82b921afef61d17fab7262bf6a7bf",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Lesson.html": "d9f00e68aba541463f1af9e141682e01c29c5cca54c0a7444422fa2b13478462",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Pupil_Resources.html": "5f7e4d6dbcfab0e85dc5651a98e7fd63a542bc1c34f453c21397b4e95b8d3991",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/Sources_and_checks.html": "138d10b4b93fc3fdf1ebba492a2792fd7965f9b1ee609e65baa87628a486c30d",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Knowledge_Organiser.html": "b2e73fd5f74e5f36c546aa6bcdc464a2ba8e8d47a0351fcd6e3d77c17c8c1531",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Lesson.html": "91817c5fef5c24696a644109e56d4f9d4a885f7d89e14688491c81f1557f05e4",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Pupil_Resources.html": "09f8fb65218fc8cf4ceea14efcbd7d33addba1dc1d629913db16612ae75a52ea",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/Sources_and_checks.html": "6402d0a62614985befaabdcdd2296e651f5a81658084d6211242400db7116964",
        "Humanities/GROW_W27-W39_2026-27/START_HERE.html": "7d653c761494c58a997c9984850da495c8040348d1c09c1473e2a840cba2be27",
        "Humanities/GROW_W27-W39_2026-27/Sources_and_checks.html": "587e8e655bf20804a54d3fda8139564bfb7c73b1b3eeba5fe15ac975765baa79",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Captioned_Model.mp4": "a49c4ba757e05244a3514a3fa95944d0686fb787d8a5a6a1f8d34caeef2c822d",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Editable_Pack.docx": "6ed8f2a9403b24efa1068b9d2f34d48352ceece1ccd554287ae3be2ba5ea8ad1",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Editable_Slides.pptx": "55696d71a8f85a7c51eed236fb648ab322ad31772a0b97308208bd7dc7554274",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Knowledge_Organiser.pdf": "3daa27fc23d55e11c050cc80665b3ae8d7afe07b843bbbae13a66fe4d04b1be8",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Model_Transcript.txt": "0a5582edc851ba73edd8010282a5b966322d7209b5f4eb68cc4dd28f4f20aa26",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Pupil_Resources.pdf": "ef9c078c786c8f828ee92a0d26d55bb81a9206fb87e71f1eb4d33f1dbaf04334",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Teacher_Notes.docx": "569f30e0367ea2b0d56d6bc35fabd3fc7f8f5d517618afbc41fba434bd98ef9c",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/BUILD_SU1_W01_Teacher_Notes.pdf": "660424e70b03bdfb4a99dfdacd6d0d368e481956c29cf5ff03a8fd452e952dd7",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Captioned_Model.mp4": "aefe389da403522dcbdf8f3fdb5067c7bdf90a0ff8ff1fb7707f7804eac9de18",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Editable_Pack.docx": "3ca9c85ed15c49f849a38c066ea9d9dad6993f7197b961f3a3a07b40728c3449",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Editable_Slides.pptx": "bdbc13726a469708737943d55ac42b1b8a6d9c5afc75f7d58474c226db5849a1",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Knowledge_Organiser.docx": "c280a9c60d299c49427d067329a6c6c7b4b67e66122fcf498d414cf35da37a95",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Knowledge_Organiser.pdf": "13fb289b374621031981d67670ff54d58cad2ee40ce62ccaef8093f5ffc6c6dc",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Model_Transcript.txt": "203f07e34a2b8e06806cedd2df91f9e7d3889d5e0f7348d0e5deb33a1c957245",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Pupil_Resources.pdf": "73a25ee9cbcd769fdcad9c23d2bca097a8e2144b920d17507963dcde75c65baf",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Teacher_Notes.docx": "9fd8098e68579ac79cb48a67042b4e9df58be7ac71a2e42a0a679ef62f7796df",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/BUILD_SU1_W02_Teacher_Notes.pdf": "60ce50216826925f6e9f37c6335669a8a85b4e4e8277364ea6a19290f8f70bc8",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Captioned_Model.mp4": "c2f09c83692227219577ce6da71884fa427d2f1567d9a722e30512023ef6735f",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Editable_Pack.docx": "522d69b4d5693c405fec238f2e3e2309a181314c4ad7b3be3e427f56af8855f3",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Editable_Slides.pptx": "74281d8a8811acbee06099eed71dbf2f1619f51979017c0241730a69db5e4150",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Knowledge_Organiser.docx": "f010a05f5973d8ee45ce8b348eb1e07047b63918619bad0a6df36edda4ef4075",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Knowledge_Organiser.pdf": "25adc43c8f95c59ae8139469fcc79df20b6a014b9495b5284abbce46197a4e48",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Model_Transcript.txt": "bf30e462ac86ee97e36404754708d83b3688762731b2b33335c5dade468c64d9",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Pupil_Resources.pdf": "82a4622a2b5f0eb855e5d99cdba40bfe11ac394ce055053d9c0f19babd94aaee",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Teacher_Notes.docx": "16af5aee924e359d46d78b30c7e842026535136ea7cfada7f8d929d1e97d25ea",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/BUILD_SU1_W03_Teacher_Notes.pdf": "8dafd0b5027e75ceea48cc8a9a90fdeb9376298460ee326d2a393dfa864e481a",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Captioned_Model.mp4": "c259e240dc8ab049852558ae887a621644bcc2692de039426eeec1f2b6a50f5e",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Editable_Pack.docx": "8fb76522ba846e2b602633575d72edbc2203fee376b65ea6e5ec3234c07d543f",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Editable_Slides.pptx": "e0dfa0a10fcffd565acb1bd9324ea33acc530452b5a9bfb8845473db00a9d610",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Knowledge_Organiser.docx": "122d646d18541619a90c7f61cedbf96445f058e7c3e8ad55a2bb5cbed561be11",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Knowledge_Organiser.pdf": "6213cb311cafc889bb1b9e5956b6673b9e3f3b12f44c12245be2c2a7a4d1f4d6",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Model_Transcript.txt": "7ac7aae40c72f99169b41d5fb45fdd554d8977bd6d0c7772df81ac22809adf36",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Practice_Tally.svg": "94034da923f5d9146a4a2341541253b0714d0d27844ec98f9d3180a57e48b967",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Pupil_Resources.pdf": "3995c584a62c7a6bc38158f4758f57271e99e24aa6fcdfa461c7a36d6f06236d",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Teacher_Notes.docx": "72c5991f0390d01cdeff7498231204d654bd6616645aacdb689646ef9df3ae41",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/BUILD_SU1_W04_Teacher_Notes.pdf": "17c13e10b988bafea45dc4b2aa6981fde1ab1a0d75024ef574ac0ebbe68b882e",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Captioned_Model.mp4": "e696a534b55d4b9a58a037932b73d0c968d8c76c476e186f157da27da504189f",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Editable_Pack.docx": "6a79174faf73053d2efa818f034eb6a15d80835e608ade7ab343f06348029328",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Editable_Slides.pptx": "72a819fe5fbd0ecf792cb8c3997b8e35f2556b7ac5c3f0d9aaf48b9bbcaaa361",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Knowledge_Organiser.docx": "ef4723cbfcb9aac416468f7e7f43a20f30dc2fe5c31f665895bfdbb4d8883432",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Knowledge_Organiser.pdf": "491165f98896cf3f2bf2d4f07c0b6ed9e808b8604c61ce950c7382c32382139a",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Model_Transcript.txt": "e5b3c5579cbe1e410c9cb11c5b41c7088b2b163d1d101115f50d54d0592daf45",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Pupil_Resources.pdf": "5f29131193e4bfa0f5ff97fa47b8518e2f584e66a53108b99eea384ad23bba2b",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Pupil_World_Map.svg": "22c4a9d78cbf38e3d9dc3291d0032a4890df689ad7fcb5593266ad428574c1f9",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Teacher_Notes.docx": "c8eb207cd3098236ef3a8b56b1f93ff9388beea6d6ebccc532b2308131b72840",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_Teacher_Notes.pdf": "e655c98552d4e5f705d38b0228ed2724cd6cc3fa4e1f765915bcc2f0b02f9398",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/BUILD_SU1_W05_World_Map.svg": "f86615266f079ae5c60ab50f7762f24e1de1bfae2ffdb566c8420217dc98e561",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Captioned_Model.mp4": "a7aa4c9b569f5fdd09cef8389d4195852a7e9574e0babbdf59bad7a6a70b2b2a",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Demonstration_Plan.svg": "cbac5d90dd0305a0a838a6173a386abda7721a26704152ed98498ade8a5935ad",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Editable_Pack.docx": "34dc7859d2f68a8fe1e7c7c4f3c73207b28051acc7d105f8781f70241476508e",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Editable_Slides.pptx": "afaa9f7f9d3fd7a9f1ebf5c004761a7a954652acce122d2b7381f49e46247a68",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Knowledge_Organiser.docx": "228a659f355e9100c93a2f5b70c339fa19723ead4ebcb53d4e87433a71d4538b",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Knowledge_Organiser.pdf": "825f40a0d538f66d5c6c6af77c8dc226f142af54e44a618d052a4c6c264f2b0d",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Model_Transcript.txt": "e1c1f74d81fe103898e7d7439236c576f533813cdfabb7666a06d0ff6898a764",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Pupil_Resources.pdf": "92df33a81f1105227c33e9c9140bf275e082897b41a82d4dc5e3f20d5da853bc",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Teacher_Notes.docx": "25bd0713adc765ea1b2ba23b0d261d15b30311c0341ea52ef07256b18a54cb32",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/BUILD_SU1_W06_Teacher_Notes.pdf": "ecad0575cfff37006a5a48fcc4e0ec342fdc4148fd7ea98560fde01df6e6f3ec",
        "Humanities/BUILD_W27-W39_2026-27/README.md": "2fd481ec81e118a654e5eaf55aac4049664cb52550fa92495873163d6f5d952d",
        "Humanities/BUILD_W27-W39_2026-27/SHA256SUMS.txt": "138e9ccaa008163b6f266bb3848071feb9999dabc49138ada2a49e325f72f723",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Captioned_Model.mp4": "e310d66789da2ce297adaec86d1860648226ddbad161e4d9d8bdffa0256556b7",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Editable_Pack.docx": "5466c946c712d50eb6398d44c30e2a8e05c08aa3a3f8571ac7aeeb03aae5f05d",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Editable_Slides.pptx": "c73f7dc6ac3365023441453d2b1a11fb00a91cdfcd5158aaa2b28bddd2b745d2",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Knowledge_Organiser.pdf": "e9fb62db511970e67ef733db42f3400c1109791459c63b35aa09fd01fdcd2edb",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Model_Transcript.txt": "7daba73404e158c3a27ce63040e2e16350c9e321878b234216bc3b34c3720af2",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Pupil_Resources.pdf": "ed937f8fd08d4c8487898f121dc2c6ccf2aaf163da9652f4b444dff8612e51b4",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Teacher_Notes.docx": "de7fc5f5d3761000bfdccb6ae8bed28e6f15b7ac62c6b7919c74b499b2687450",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/GROW_SU1_W01_Teacher_Notes.pdf": "c9d13c951e445f844e3fbbef61d7091c5db6f29b6ed9ad0f1389e10e60c29a91",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Captioned_Model.mp4": "cf538f4d0cdabdc128615e3711c4ae0984995388fd7a122aa648ad706fca2482",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Editable_Pack.docx": "fb486dcd75590e9f9c23359ce356610ee365801609fd848835cfae7f3f17bf88",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Editable_Slides.pptx": "d742146b1f2df4450a25410a1e74d459eac974993d99a1605eac5a1e79dee397",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Knowledge_Organiser.pdf": "5911144fabbda2ea7d80f9884bfdc19c8c75fa107534b437b77991715c43d19a",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Model_Transcript.txt": "8435ef18ce6ae1b4e7e9697f74d9d462048d8175a518005324588aec2120033f",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Pupil_Resources.pdf": "6eaf5093236d52339271db4458316b86811621ebcdae37413ec41fa1bf59c315",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Teacher_Notes.docx": "15a6cdfe01c337ef18ce429c7734f0164f848c27382d56935112de49a43cd314",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/GROW_SU1_W02_Teacher_Notes.pdf": "0a357c099a7a5dde6a3a642644c73646d2489ddf1c29ec73e52100d2c37e454a",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Captioned_Model.mp4": "32ddd8a8b2827e1ff94dec0ef249ad5a992db4184d0d81ca07d95eeb7346c2ea",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Data.csv": "5f559be976495304aa10bcbecac68016f37d689898b8c5b18ce63dc8a6da170e",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Data.xlsx": "62e4eeb037894b92700b7aa2de1b21218c4885c2082bdcc3f7ad562e89a8df43",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Editable_Pack.docx": "337647fb9eef9a262a572136a4419e7f0fc6080fe550070396c05bfdc06e7786",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Editable_Slides.pptx": "c0e33bb052e622b74a215b763cc715f7b6c2ddae47ecd1c4e5f1d4cedf163433",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Knowledge_Organiser.pdf": "d64d6a1a877cd8ede4f8ba01b836f1c29f90206d8f7a6435362bcc610fcdf0ca",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Model_Transcript.txt": "306323f65b1bf79cda9e25108eab5667f575d0d0171eccf21e80bfaf734e46a0",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Pupil_Resources.pdf": "a93fe8291336793dd2e58e3428de866995f79866bce1591135ff9f6421e27d3a",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Teacher_Notes.docx": "ced287a00733310763fd4928bf25b3a6c301133673fcaf0472c22cfc5a8992a1",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/GROW_SU1_W03_Teacher_Notes.pdf": "7694fc2e0996163b75642b3c994a119a1b7b8b55076ac0a1b8eac05379577e39",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/Teaching_Visual_1.png": "fcf5b9b21a64d2a33ed2791b79548a8569fe5f2773e162a7829f3919598a39d1",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/Teaching_Visual_1.svg": "aa9cc0f1dd96a80b43d633f2183660f6a06550bc7bd274bf62ae06dc2a011f14",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/Visual_Resource.png": "fcf5b9b21a64d2a33ed2791b79548a8569fe5f2773e162a7829f3919598a39d1",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Captioned_Model.mp4": "8e412b8c6776fbd63d4873e6d7bff4c134257a67460cbbc607f746f258db9051",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Editable_Pack.docx": "64a36272ea6537a6e07d45b42adcf98ed1fe4f2f11df2019c6beccbabb359afa",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Editable_Slides.pptx": "0b98905870b9d3b05bfee9bc8c98799ca4d261bbb53fef342189351f8ee9e96e",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Knowledge_Organiser.pdf": "a082099cc88a581929d3bfae894b7805d2281f3577e639ae7675825ed828c7da",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Model_Transcript.txt": "74bae108b11069e663ce8e46712bb953ae2807c692adb6fc8f1237fd12cf4d67",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Pupil_Resources.pdf": "9e4517ccf154b1878db73176364272bc8fc694f4dc96a47a06ec839437f68ba0",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Teacher_Notes.docx": "4a42b3f7b45eba3504ce60a4949e4e2c011a4f3d4b3ed24d8f188f3fe0dd2400",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/GROW_SU1_W04_Teacher_Notes.pdf": "74c5dbb52a7e6b4a296ec8962533e9b12db7bbeed7c3f0f2fbff071c1e38e0cc",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/Teaching_Visual_1.png": "adcc6cdd025c8fc4fd983d6494d492def017b4452cbd2ca4b742eb0088a715e2",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/Teaching_Visual_1.svg": "be31bc16d7b27d9567b896da60856a96f5897d0901d9caccee17812fd601aaa5",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/Visual_Resource.png": "adcc6cdd025c8fc4fd983d6494d492def017b4452cbd2ca4b742eb0088a715e2",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Captioned_Model.mp4": "3275427de80711dec50885848a78e1a4708ac3cbbe5d6b3cc7f6c2087868ffd3",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Editable_Pack.docx": "0df2e9d8be026b3266c3a6bc6f1f1735b73eb1356b174bf213f8d2f21b463f6f",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Editable_Slides.pptx": "b4937b4671933ec45d5ea6f66befdc215239393d3fdce96faaa622db913219d6",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Knowledge_Organiser.pdf": "2b6da725212837d58574d9f2bb24ec7c7a74087fe1e653b7d5eabf4f6136f2f0",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Model_Transcript.txt": "c1deac7c6f1ae8a591a5eff027682e4875043d6978d12a16be0026085f95a80b",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Pupil_Resources.pdf": "01ead805b20c1a318638d7fe4903bf70721e8b207344045b6be3d95ca297d7e8",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Teacher_Notes.docx": "de2ffa1f5b728a15a638dc9429a7ae67f8c8c528b23c50b38d7806912410a4db",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/GROW_SU1_W05_Teacher_Notes.pdf": "9475a6cc5a4850a9075b660bd61c3db5d2d3fe58ce11ab3a35926110574d6036",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/Teaching_Visual_1.png": "e3e41a4918f05e792c2214855d18a6c6f89f2b7a7a424c3a4d701b7a3f2342a6",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/Teaching_Visual_1.svg": "9013971a1fb9b36164e851fa1f1ce9e47f95a62d3d79e8bfd632602a18681bb3",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/Visual_Resource.png": "e3e41a4918f05e792c2214855d18a6c6f89f2b7a7a424c3a4d701b7a3f2342a6",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Captioned_Model.mp4": "4e599e746cd0a6716a04213ae3475ec99f7e7528fc6695f24f196c349639f699",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Editable_Pack.docx": "c281ed3c373a714ae2809edcf67ee6442da55a9ca0679941e42feeb7a014f6b5",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Editable_Slides.pptx": "dd22a0b91a6a3783411f1680f48b1a61870e34a35fce3fe74f8d1fb478a4ce1b",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Knowledge_Organiser.pdf": "fdefe7ca13cf4cdfc4099e47180b52819c62a1de2fc2702eb09590d5222237f8",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Model_Transcript.txt": "91bcb7bb53a628057b05f910f375a8c92ce736ba7665ac2566b10caa9f706c7d",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Pupil_Resources.pdf": "23f5aa2f1b86a115ac8f6248e031841303818f886734b8c13ef94bbb441074c9",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Teacher_Notes.docx": "91410acf142e6f84af8054d95fa8dfcd68c377ed601cd7b2b50a2e829c0bd817",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/GROW_SU1_W06_Teacher_Notes.pdf": "91f34763b34b940c0c8874405755c8a53d0ba6c01512981e328fdf82e43b8a8a",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/Teaching_Visual_1.png": "a4697b29bafed2a52207dbe3c95c0c4bf15002da406b41148a926369f0a2dc30",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/Teaching_Visual_1.svg": "79e075b98bbde373e9ad8a02616874c2acfee940b34c4794f6d2f9940fbf949f",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/Visual_Resource.png": "a4697b29bafed2a52207dbe3c95c0c4bf15002da406b41148a926369f0a2dc30",
        "Humanities/GROW_W27-W39_2026-27/README.md": "d636efe503812cdf675d140b93568cf5f22136521eb2039ee8189e6dff47e3b5",
        "Humanities/GROW_W27-W39_2026-27/SHA256SUMS.txt": "6a8a9430279a6c1a364703e364ee9c075b1a10c550113373f28c08430beacaa6",
        "Humanities/BUILD_W27-W39_2026-27/CHANGELOG.txt": "2733da52983532a309738468a0b7e9902025cb9e18018059f5c33a39fd538a62",
        "Humanities/GROW_W27-W39_2026-27/CHANGELOG.txt": "68feec6a79029a747bba6a78aab55c196e13a21631c2cfa068f3be1e20f0f2bc",
        "Humanities/LAUNCH_W27-W39_2026-27/CHANGELOG.txt": "9b409ef65c4e2fde23a6174ff711f3dee859db7f2d24424839dd2944c7796935",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Captioned_Model.mp4": "223fee075c5b8295242c95a66edd11b701b73edc160ca9fc73d7a7da48c8c2ee",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Data.csv": "5e4aac3913e5d2aeb549870cd8855766ef31af63213e65cbf1c3fd6dba4209d1",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Data.xlsx": "15eb1241e17839a5754e406e6087f7ab171b0bce55f26f7a3545bc82df0b5772",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Editable_Pack.docx": "ad8151480497d68c85e7072243a229769ce931b8526992bc6675c7175f57a47c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Editable_Slides.pptx": "c4d844c0e02c62ddaf7112a9e7f87be69df6ea85ba175face8af12e39b2969f7",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Knowledge_Organiser.html": "7be6562956e16fd2d72bc8b0659e7e91fa2edd79f42ffb485b119b1da7ddfd46",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Knowledge_Organiser.pdf": "4272e713b1440d08b964fa134082c6f4a7b83d156cb667eaa18aaa36f52b6a5d",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Lesson.html": "276a425e4f395eaa271fcee29966ec545d68be65c237b157b16ca42642b3e0a9",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Model_Transcript.txt": "1ebe141e3ecf64c80ed84f03969ccbac792685bf42f8c27c85d65f1c9c5a6006",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Pupil_Resources.html": "3dd0da529309e3f63495194be6906c54aacf05b207e8075a1845902d383e316f",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Pupil_Resources.pdf": "bb2eda97f3173bb2c650f2c37dfdab59b19f359da8b4f97b8a1ee0a36f82c830",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Teacher_Notes.docx": "3d26ce25a7eaa60eb64cd857c3d7bb7249eb313ac67a8f2abaed4472a73e151e",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/LAUNCH_SU1_W01_Teacher_Notes.pdf": "d13c473f5004bdd2d68c7920e8db1a55f8808c408183b89c92132e179c9b08bc",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/Sources_and_checks.html": "29877c91d17404473b4012869c22b7a3ea84ad5be63120e5049cee3d479a0a32",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/Teaching_Visual_1.png": "1f125a3fad70fc5b1303f1e90596bec66a17d0f3ffaf965b77fe4d9d23bfac53",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/Teaching_Visual_1.svg": "9b0309453187d70ee18be143aeb638b8009049bda219c2ac5fd16a5f9601a74c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/Visual_Resource.png": "1f125a3fad70fc5b1303f1e90596bec66a17d0f3ffaf965b77fe4d9d23bfac53",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Captioned_Model.mp4": "66ae4faa850eac033ece7508948b58c931204044049a977823763a15d8b95380",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Editable_Pack.docx": "f351577d6e32e7c7bfb880b324d663ee66e00f0271e0975b6b7e54ae6a1aba68",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Editable_Slides.pptx": "d18837edbc8a2f2a5403d4e83f36ad1c9a240aabae762d23b994861ff8f2cf00",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Knowledge_Organiser.html": "2940b779de567a8aac8deaa4b0ee410694a0f9ae652daaa4805cc0cdcf817c6e",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Knowledge_Organiser.pdf": "a8abba765492b6eec4b6df3be34f7dc5cafab6823336ad36e501daf9bb638184",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Lesson.html": "83a60f1f0308dca8ae7e511db283aa93f791c92ead92d3f03cb8da62d645aaf0",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Model_Transcript.txt": "fa24d4d6d533fb4d393e7a8061c1ec14c6540544c898d283d2ba6da1ba28637f",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Pupil_Resources.html": "6607f47e85e8c21914661812faaa7b3092327884cda7612666a347dde61b3743",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Pupil_Resources.pdf": "19eb93934978239d0927dc1ac9768dc50c06fe66f4ab74f70078f3889be3e79c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Teacher_Notes.docx": "3ea2071c070e1f13cf5618926848d6983d5ce73cf522f6cd03aef03dd7faa2ba",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/LAUNCH_SU1_W02_Teacher_Notes.pdf": "3e425c737a8298b9607cf5005c3dad835910aa858dcf761a0697456a4539baa3",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/Sources_and_checks.html": "3bfdb8be74a4931b03c73c3d6f623e1af7933f948181e612be70858ef7cdcbe0",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/Teaching_Visual_1.png": "b1ba8d8834e6668a033a1f05ef85cf53e3c7c9f341476366f668041e57c465a7",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/Teaching_Visual_1.svg": "9ebb881a715d28f33e1a825d4e36ee585a213396b911c07bed0ee28a1454fc5c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/Visual_Resource.png": "b1ba8d8834e6668a033a1f05ef85cf53e3c7c9f341476366f668041e57c465a7",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Captioned_Model.mp4": "28029edfcb191f301c417937cf059eefafc5e37ef4166b79b787663789c8397c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Editable_Pack.docx": "156a197301265b180b8a8ac81e23042dad26104eb78e756925f1611fe459b90f",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Editable_Slides.pptx": "3f8b693b0ecd2cd64b50a6ca531df68be9b9e0c6d7b1b71c0bc1d8cf02bade32",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Knowledge_Organiser.html": "4e6f5a54ad4a590444c1d21b055054a82094f9fa5a55aa4a1af96c61acc1793b",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Knowledge_Organiser.pdf": "9bb9741a001e3b02d5ae9e33d9a08ce3f646f023e2cb9f2db63c31a73782621f",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Lesson.html": "b5ad3d54375a42872796a31ce8f9e4c859fcbb2819491f5c2072467149811626",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Model_Transcript.txt": "c63e32b9009b68a1ce4248430b0068b701325b19963db321cbeb80eab69d2fba",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Pupil_Resources.html": "9ae1089bfd801b77430d72897651eaba4410d7363d5eede82db6bfbd7e659f98",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Pupil_Resources.pdf": "80cdef02da770dbd7d8f3d9da97682329cf84c202419b864fed3d95857c24de2",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Teacher_Notes.docx": "84551fd800990f995721c64c6a149b88c04aee97d7a77312cc9f8c731507598c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/LAUNCH_SU1_W03_Teacher_Notes.pdf": "d2eb8bfaaccf013cc10af3f91ab2ec30a87dc9b748c1342d40dcfa9e8225c9d5",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/Sources_and_checks.html": "81c9c9ff9dcc195f52f92246cc10cd716fb1b4aee6bde3ffea051d5462985c06",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/Teaching_Visual_1.png": "cb1c35d671b004e50a1584a6f7f59c80b492ae3b5c27aba9a71f8ee3d24e7ae4",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/Teaching_Visual_1.svg": "1cc263433f04e80f3ca72ab056dc32663d6c195784fd796069146c515ed8cc5c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/Visual_Resource.png": "cb1c35d671b004e50a1584a6f7f59c80b492ae3b5c27aba9a71f8ee3d24e7ae4",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Captioned_Model.mp4": "afaef4efbf6fb5a1f1f6245419f74b7fec59c1ba254a58c9999f08b8dabb8c6e",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Editable_Pack.docx": "09822d774365f82bd915b577b5cf6ce4a8252d2214cf418ed0a16f8031e27b0c",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Editable_Slides.pptx": "dfd131773aaa3af159c6bbc191aa0153461406437c39088e8402d1aaf557eb63",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Knowledge_Organiser.html": "a6e0134a5bdec15e6b940fb140540255f7d15bbacb4fb6516d7889a6545b8725",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Knowledge_Organiser.pdf": "7832f67c845d0c3efda0492b28192aff90f2ee61a0d5b08c292b6c0c9939725d",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Lesson.html": "965e42718cf7d707360d4ecab3c09228cd38074c3a2768aae6eb339d68282ced",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Model_Transcript.txt": "8db6b85dee23dfd7bc7a9f31ee2ba87504005269079bcc59bc3c7b4df7f19c0b",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Pupil_Resources.html": "685ac2587f5e0abfd2c9f09207542b120b20b9b3c09074ef0f569a2692e0e741",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Pupil_Resources.pdf": "8da1079f3dc75bdf50a02c8ddc2aed0560f339299b55841220262ee631004f08",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Teacher_Notes.docx": "a3f6c4f9cb5f6da64a9aa060fce6809adf3f4d013812e3da16ee6393a80fd706",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/LAUNCH_SU1_W04_Teacher_Notes.pdf": "b55628296155e388d5fda30820ebe62ffb76c1112585131fc7fdafe6dc7fcff2",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/Sources_and_checks.html": "b05876ddf7f80f7319fa1b0b3f49e20187b87ca749fc1f85166b0ea85cec8cd0",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/Visual_Resource.png": "47203f71812d19cf3602da19a3a82a73f9c617510cdf9d2b6c9940ed5e687d4f",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Captioned_Model.mp4": "459ec0c44b3d41fd95daedbae44d99398fad1a1840582ebb6e116c8bb64485fd",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Editable_Pack.docx": "ee6fb8342a3aec3959a8d667f0c3bd394c25223366f5f83153eee230e0a00dc4",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Editable_Slides.pptx": "0c79ff61687df027cc40c3f62232c91c514e06d2dd0c11363e5a47799ed67e5a",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Knowledge_Organiser.html": "ab7f110871e6ee7c63a8d21c20b12b49b66f5c38693367ff0084a04c64926d02",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Knowledge_Organiser.pdf": "fbb2708b0525dadb741cc8f042c4080e0787e6e47930826bcb5c4b8a9065a9f1",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Lesson.html": "e9db056369320b2c1a7ad66abfbd000bcbf03a40528d2ecda45047622b59b51e",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Model_Transcript.txt": "4eae8b55adaaa42db40945b5e2ec9b210ed3ca966e2d7e68a03d0e1159c632c2",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Pupil_Resources.html": "7bc5cb3771c7066972a8cac7d9a62a29721035b7a513026d8a17db3b531a0ee2",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Pupil_Resources.pdf": "e7e046348403ba8b169d9eea453c015e572e09168d714921f045f1ea3728f9c8",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Teacher_Notes.docx": "d8fd2edf297a6b52239a3cc837fc13e68ac6d14e4ecff2db39edc591cce7a665",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/LAUNCH_SU1_W05_Teacher_Notes.pdf": "a1721cf860ce746bd38d1f51a3b618b64959e9fcb8777843d911a8a130cf0929",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/Sources_and_checks.html": "dc2bb0e06c96e3c684b1b14be21beb06d7c670c4a7b52a492e55c04d1a6469b2",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/Visual_Resource.png": "4facb2f3f70e7ec118b09d93a84cd761698a7ac365ac8334c43633cc9928e59d",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Captioned_Model.mp4": "b5dc6922f7561411dcbb1066e6be8a1aea9c848176dfc50aaaf85632c67443f5",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Editable_Pack.docx": "0454b707bd56da1055099f1cdda889ee0c3d96ad40185897b867a48a0f8cb24b",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Editable_Slides.pptx": "3f6bcc0f7e4e1e3871f21d155287d13f564994f63c6619f1e4ed1fc0e2061206",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Knowledge_Organiser.html": "45f2e1ea5821bdd0c38b2bb8c90892ac756f615ab513d3fc1825f5bc4eb6fd01",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Knowledge_Organiser.pdf": "e085acb1ca51a66ec61e2785db2878e84d651403833da03ddadb565cd22245fb",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Lesson.html": "b4b8de6e7079faa8af9f18c120f2930e32ce06ea0d70952b63f2a348f718148e",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Model_Transcript.txt": "8557f0b96b37c12b4c4d2b068670f24c47e666238b8586d262f320ad8fefa599",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Pupil_Resources.html": "5702eda2b9a723956e37be0abff9b71d36880bb2bffac705cc19c9d80d2b7b3a",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Pupil_Resources.pdf": "411f8c14aafbedc6225cf71f767afe0107a01a1b0fa444a1ba052d0b6deea300",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Teacher_Notes.docx": "f8a0251b8ef2860854a70f3410f6448fd03a663832305dab644e21e2eb8c3dd1",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/LAUNCH_SU1_W06_Teacher_Notes.pdf": "4b1f89a0441d54247a79918c3c94753250f88a3d23a75b3f7c98ae492e8d9b6d",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/Sources_and_checks.html": "fd389ef2d42c23947542fdcef14250c7f080ef637a5c46fb7a077ed2fba94ede",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/Visual_Resource.png": "52a7163cc5ef2299463e95f2512f6414e326d22493a92903052a096f6f0b1a23",
        "Humanities/LAUNCH_W27-W39_2026-27/README.md": "cf39c6f67165f1b6f5c3a0f368385bc1b7babcf17fcfdbfd6d51bca24df98dc9",
        "Humanities/LAUNCH_W27-W39_2026-27/SHA256SUMS.txt": "19dd28e4d2a7ae3906da7b1f7d8d56bb019436b2d208b17e2434dcc7548d629c",
        "Humanities/LAUNCH_W27-W39_2026-27/START_HERE.html": "dd07b91e212e71e863c96d9a31d489a68f5ea3ec529f50e96f6125251e48eb8c",
        "Humanities/LAUNCH_W27-W39_2026-27/Sources_and_checks.html": "fff2824ac1fa482b7f6640b667be548c56648aa80c9745d1a5ea81871514a2da",
        "tools/hum/dom_oracle.mjs": "258b146a9e85ed3773db915776356bd31fb54defcb1f601b140489f61c4676c6",
        "tools/hum/explicit_document_tags.py": "9fa0d799133e59753848490b9cb052a1872f2204ce520aab6c2e57399812862b",
        "Science/Launch/Autumn2_W7_2026-27/SHA256SUMS.txt": "c03b36ddb50b9d4e626a13c67c33f7d399f6f8d9e94a94133b1efcb42af9bdd2",
        "Science/Launch/W14-W15_2026-27/SHA256SUMS.txt": "0bb93ca935491473b9df0d0f5605f3ea67057c6a00eb78c4925e154b71c8d5eb",
        "Science/Launch/W8-W13_2026-27/SHA256SUMS.txt": "e8c3db8150760d44c9dbac0472200ac8b4043771db89c92dd5665a0232a5c1e1",
        "tools/catalogue/SCIENCE_CHASSIS_CENSUS.json": "8f69384807efd984ae00629bada8565c8b1dbe988fe4d9fb5d22d05b9182f424",
        "tools/rx3_recommended.py": "b4a079a865d6ea956f1a7cb7a4837071db6e96c886565670d1d4a55c661fc150",
        "tools/catalogue/check_title_slide.py": "49815bce6b54d97aed864e403d10bd49d19d886bf5a39cbe7583375ee47ab77e",
        "tools/catalogue/title_slide.py": "3e4e7e8dfa590f3e0a8e24f49939edd9be2d59e4f955aea0935caa003f104788",
        "tools/public_surface_census.py": "310af4565b6b6998e33911352bfbaf37d65497b94d0f03a752d38277f7cdbf0d",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W01/_staff/TA_BRIEF.md": "d28e9ed7ad20dd7da627290a5678ede678471bbc7359d016ee74970321cca8e4",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W02/_staff/TA_BRIEF.md": "e55b49716400e42d4453811db490961d2624954e6f1c09f94bbf8bbf986a78bb",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W03/_staff/TA_BRIEF.md": "9244173372c00c45eb9dd1970f674763b240b6f1e007ae08e8093d8265deea3f",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W04/_staff/TA_BRIEF.md": "bd6a9bcc0f03479fd2b6f7091ff12f1573112b445e791a1da2e3099e808efb99",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W05/_staff/TA_BRIEF.md": "492c7592bca90a896afe9e58dd491d770c3b61f3dbda7b73242ef0a8216e1efc",
        "Humanities/BUILD_W27-W39_2026-27/BUILD/Summer_1/W06/_staff/TA_BRIEF.md": "3550dbc1a874d30b20a3f3da7ac0e8aca636ae4e62e5440db6d839f67917a7ec",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W01/_staff/TA_BRIEF.md": "e4677335086a339d74bfc5d4b275944696e8836fe84b09a117e2ee5984f68149",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W02/_staff/TA_BRIEF.md": "613953445ba2e9ea8ec02e43728ba0300d31cb62de3c2049470ebcbfb228ba79",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W03/_staff/TA_BRIEF.md": "f3490c954df66e312a88faf31dfe19094d364605a3e63fd6a869312b26de4c0b",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W04/_staff/TA_BRIEF.md": "f1d5c286f93baa83a0ca198384ece5d7bd80103f406be659405e77bc34ece4de",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W05/_staff/TA_BRIEF.md": "b6081f08a99f1e0d8acd251694b0e5d349556538ac4498901cfa715e2252386a",
        "Humanities/GROW_W27-W39_2026-27/GROW/Summer_1/W06/_staff/TA_BRIEF.md": "e0b8e34e888371d2b5ead9f052b1cfccde69cf3ed59ef92f2d6914b143e0f271",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W01/_staff/TA_BRIEF.md": "f5a569244b7d84b8a7ed997e60d09e1a4a9679515413a20a1cfa7977bfe9b0f0",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W02/_staff/TA_BRIEF.md": "e380fed313ec542920d02391e7b099aea4b4b202c3916ebd311ab786420d5563",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W03/_staff/TA_BRIEF.md": "f9b7ebe4181d3c7a498852f67be08554f6a127487b68617145a7b43cb246b074",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W04/_staff/TA_BRIEF.md": "cb817fafa40bfb3934bcf892f88e5ec3a072af8dec6b526eb5fea0d4069ac506",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W05/_staff/TA_BRIEF.md": "8f7087fd172849f7462ea5cfc1818f05b97a2bab24d507b6662ef2b3ef28e5d5",
        "Humanities/LAUNCH_W27-W39_2026-27/LAUNCH/Summer_1/W06/_staff/TA_BRIEF.md": "4715d058a4c65e3b7b15c60196b9481159ca445d7bb82fa7697d99d17f47923d",
        "Science/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W01/TA_BRIEF.md": "4d736ec23552cdd162ebfdbd62704e8720731f9005b9d74811a4a41768a9fd13",
        "Science/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W02/TA_BRIEF.md": "9f2180e95614a4d1bff62304ef89fbdb9734f0b8cc11ae30cd4325a0cd76b7d5",
        "Science/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W03/TA_BRIEF.md": "f0ebe46c6820c0c5433fb1030e08a0784760b303288ea649517a8a1c759e3115",
        "Science/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W04/TA_BRIEF.md": "8add803611c31bebd59c5f2891e6634b339bae29d60e3c095052bef2837cdecf",
        "Science/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W05/TA_BRIEF.md": "97f262d1e068199ad7cf6e23712a0ac51d63c95ad9cde71ae6cc932a7068dc3f",
        "Science/Build/W27-W34_2026-27/_staff/SCI_BUILD_SU1_W06/TA_BRIEF.md": "9b031cf913ec3a373a98a5d4e741c0f079b8330fe086d94ad386a0e68c3216fc",
        "Science/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W01/TA_BRIEF.md": "63546c8c2bc40552ac0250f1644fd0c96259a7954afe11d18dcbe35ad263d469",
        "Science/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W02/TA_BRIEF.md": "abc8100fe5feb68c92d56a4c11bfe20eb428395b5772a5ab3a41ef4b947dc2dd",
        "Science/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W03/TA_BRIEF.md": "76f9d9a3607f7a11ea6d8b7a3fd592526d6cd66e2442be3e6236a16906261775",
        "Science/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W04/TA_BRIEF.md": "e9e1e319978e7bd889641aa15718f7229e9ca61e6a8c80290d700de8d0e7c86e",
        "Science/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W05/TA_BRIEF.md": "9be3667d9606e8447442f3d1493ba3312cc29b6e125bdb2ff18c26d9b85ea729",
        "Science/Grow/W27-W32_2026-27/_staff/SCI_GROW_SU1_W06/TA_BRIEF.md": "5dd50bfc74359e194f61a91a12d3553fbe7efbd05519ce07a8267dcad2ab1512",
        "Science/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W01/TA_BRIEF.md": "d2628e2dbc7221fe6963df0b5124d450062331a24b6e3e4d792664a61def054a",
        "Science/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W02/TA_BRIEF.md": "5ba509eca808b5b5b7cd7f8d9927faa0edd7bf1061427996550387c214d7b3a2",
        "Science/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W03/TA_BRIEF.md": "846727993e3adb2eb0ca707c95987c9491e52e40c8675cc9a321503ab7b269f5",
        "Science/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W04/TA_BRIEF.md": "5ead0d772a3544c366d0c93b9e50a50f368f7823c9c08270198cb54b1008396c",
        "Science/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W05/TA_BRIEF.md": "d0fa0a5a9593dd145cbe56c618da6a288cf9c2897b971778e20ff42c1cea8647",
        "Science/Launch/W27-W34_2026-27/_staff/SCI_LAUNCH_SU1_W06/TA_BRIEF.md": "8b6313307fdafebe8a2d6d9efd47b2ae3dee3f088a6bcb90497fdb2b835b3cbd",
        "Science/_staff/PROVENANCE.md": "4bc74f9bf2aac0a9a1fef7f6c1410ba835173ee622b90ad4370385b71b50f79d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W01/LAUNCH_A1_W01_Lesson.html": "5f1ab114ecaec7c7a8a56c576af7a8f14f70ff70866465926e55a4aa98ef87ae",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W02/LAUNCH_A1_W02_Lesson.html": "9055d34c0069bfc0a19179370164133e4c35f5e50a5f5cf77e9ba18fe84666ac",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W03/LAUNCH_A1_W03_Lesson.html": "b093859c48180274b680f1e35d4afb78a309d1099d48fe6fccd51b461d3e232c",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W04/LAUNCH_A1_W04_Lesson.html": "bdfd44034f439ae5181c17bfe78e6747af340bb3d15fb0739e99c9de75aab49b",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W05/LAUNCH_A1_W05_Lesson.html": "f95a2eb84b151fe03a0a5fad3a98bcc5aafce8f83c7677b8c8681de3b5a0d7af",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W06/LAUNCH_A1_W06_Lesson.html": "35e73d60a56b324de4908b19b16522f39defcc8dfba5cb0d90abb2156bffe006",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/LAUNCH/Autumn_1/W07/LAUNCH_A1_W07_Lesson.html": "dbc6f3109dd6265e517cb0566e1f6de0bf5b784bbfea423df5384981059382de",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_A2_W01_Lesson.html": "a1c16ce481a960e243e89371550357640648760cf1d6e5dd0d45b89be8d85bdf",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_A2_W02_Lesson.html": "8e6b2f73511aaa359a5605929757ae19a078c6e01584ffdef7d4f77b68a88c9f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_A2_W03_Lesson.html": "d40fe5863e5cdaaf70ab0ffdf9f4829377e2d35b74a9d5e455385e7a232bc9c8",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_A2_W04_Lesson.html": "2b304ba13036e4d205e6cdaba6c7778e84b8ccbc42d0367ea75fe13db225e7a0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_A2_W05_Lesson.html": "79900fa6d3f0d3821436e68baf359d47f039e7038e8ec8abe5b1ade0695a0ac4",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_A2_W06_Lesson.html": "bbbf137d46c3aac3fb11ac1b82f3bd425e949953d95e2184590b54a854db159f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_A2_W07_Lesson.html": "495189e883e2a78a6e24fb3a8005aa4866f5e382fd0afa793d9b48e0b856fd4c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W01/GROW_A2_W01_Lesson.html": "15e63b281875f6d62636a9b619abd954526d6c31318687510dbab09271e91e39",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/GROW_A2_W02_Lesson.html": "541f7d43d5ebf0cd057b78286ff682bcdc475cf44b216b0f2332d1f713e87cf9",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/GROW_A2_W03_Lesson.html": "663ff01c19bde7cce9cd46596b2b329e167501cdff570f9dbae6ca1fc9ee12b3",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/GROW_A2_W04_Lesson.html": "0395590993c36cefd35e3f8ad9b1cb9220f60f09b9eebf3cabfeffcc64e5f735",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/GROW_A2_W05_Lesson.html": "a2b7242f2c720312b8d75fd3bd3fbf61d5d79df41ef9aca03060e8e656cc621b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/GROW_A2_W06_Lesson.html": "a85daba32d269cfae3347c0a731a1778560bdcae0e0388538f88863ca2601a6e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/GROW_A2_W07_Lesson.html": "5124e543efd5f8452ef18f7cba460aa230dd2d52681107de1e59f0ef8f6f7d65",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_A2_W01_Lesson.html": "5dc5be4aee51879803a1da926b42b222d24c9993472128cd0c3d812ff32d5e9e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/LAUNCH_A2_W02_Lesson.html": "6cf0bf848a2a0bab2581e86c1a0536a759713214799177947e59018a432fca46",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/LAUNCH_A2_W03_Lesson.html": "ed798926fc9029b1e89633cf6aef8ad0b539fd0f85e1bd46b14eaef6ab70816d",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/LAUNCH_A2_W04_Lesson.html": "018a35512e73b58a24506983e7f33e502dc03740001f9c6fe07176fc2d62f1d4",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/LAUNCH_A2_W05_Lesson.html": "f292ac63fba414206333dffd3869de2657c37036bbfa757de2c9a0eee368760f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/LAUNCH_A2_W06_Lesson.html": "14727c333c6cefd5f7131733cefca33d66c78affec110830e2c42791f1c759f7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/LAUNCH_A2_W07_Lesson.html": "facb9ac110bb65f343fda3d2f13bdf384272a40b3f8be62d96d135817b2b7e47",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W01/BUILD_S1_W01_Lesson.html": "2482e33c71758259071faccb8a86bf92a16b7479d52dd455e5be825bc8e30832",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W02/BUILD_S1_W02_Lesson.html": "b1d74778f32805a542dd0e0940cc0dae4d302c4123f1bbc6fa0826dce7216c0a",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W03/BUILD_S1_W03_Lesson.html": "a74189d804d9d9775eb3750288a98ee22cd609d84c193f39ede86a682f5fc17d",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W04/BUILD_S1_W04_Lesson.html": "60dcb5b38bf870de9407ba62dd01051ac846930ced03934d9bde0e64fef7500c",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W05/BUILD_S1_W05_Lesson.html": "98f10c504abd66edae4137be1256783e74cf56f988f95009f5e5cd2a9f0ce8b0",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/BUILD/Spring_1/W06/BUILD_S1_W06_Lesson.html": "4aa5584d5e7ca92428eaf44ee58648c8e1361124c8770003c3aa56a5864f7eae",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W01/GROW_S1_W01_Lesson.html": "f2e5f4ad118f8b8ce7a17cdbaffd012de098b4f5f7b429513e48bc715fa17fb8",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W02/GROW_S1_W02_Lesson.html": "9724df4cbffcb8f1a929ee846bd2d687581c342ba5fc76c224b35f2b4ba84443",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W03/GROW_S1_W03_Lesson.html": "9c37369db31d991d5df7f1059547fd25affcae1cecbc8620622b41eee25d7b35",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W04/GROW_S1_W04_Lesson.html": "f7bee9a72abd1eaec0e1e5b6ade07dc25c782f797d31933e1f9b77152c3ebb6f",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W05/GROW_S1_W05_Lesson.html": "a0538117414c82c5450fae8fc1776472bffe34359071dbcb72a03814047df097",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/GROW/Spring_1/W06/GROW_S1_W06_Lesson.html": "3f15bd4e99708fbe66ef8aa1cfb8d970588abe9af101324b31849c26fc87e66d",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W01/LAUNCH_S1_W01_Lesson.html": "55b570e7070c1f9af8b570cd5fd5d4613c7135d1d6c1bdf8066416799da003b2",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W02/LAUNCH_S1_W02_Lesson.html": "6960970543cbfc66815d6e809b49b2667974dcd552ed4790c3eafa7b2f4c15b5",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W03/LAUNCH_S1_W03_Lesson.html": "d2336ee766ed79126a41370d409fcd12fc5815daf76fcaeede9d7fca0ee89506",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W04/LAUNCH_S1_W04_Lesson.html": "a54340b5b744ded8c3631885e380f259fb1459619f4f13a0cc65a842dac5fbbd",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W05/LAUNCH_S1_W05_Lesson.html": "ab4e5a8a86ba211327cb0b733f1ee29c8619441003aa85d9ee505c4dc8b8a00c",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/LAUNCH/Spring_1/W06/LAUNCH_S1_W06_Lesson.html": "dd238e2b8a449cbc7b9de46b582ce30dbe9e1146dd99cd1948e5f8bbbeab9005",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W01/BUILD_S2_W01_Lesson.html": "5ca95456c016e586a970108fd53bbcfb0cf1724db1a7e11907b2c2451ad0a55e",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W02/BUILD_S2_W02_Lesson.html": "72590065a98eccc42d4123b2392c973472f095d87a584c6df0f76503fcadbc31",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W03/BUILD_S2_W03_Lesson.html": "06d731dbc610e50e6b46dfe9f71385beb8e92a268be3bdf8d5399bffa64ae60d",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W04/BUILD_S2_W04_Lesson.html": "4de5f2ef8ff474334ec7ec48307704cc4468655f100a65bffc8b244ac7285219",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W05/BUILD_S2_W05_Lesson.html": "db63df0d9e111332d9a6859ba5a8b5a1714ce724f1d847b1314efbd52e826085",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/BUILD/Spring_2/W06/BUILD_S2_W06_Lesson.html": "9b54d696d4de412fc6ad4ceabf8bc91b283a405acebf978a566652208d075ca5",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W01/GROW_S2_W01_Lesson.html": "9d93b0de8ade11d33abea62f2766664ac7589418694403a2829d375411498d8f",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W02/GROW_S2_W02_Lesson.html": "023ecca14955dfcbd1b13cd8d845ce54e98961add7f9bc104d8283107f5b1105",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W03/GROW_S2_W03_Lesson.html": "7d95b4c0d60beede6d07eb3bc69570f6a0c020cf102f3f89d721bc24f216e8e7",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W04/GROW_S2_W04_Lesson.html": "dfa7b5383aaff4c49293fc503ab5a6ee370ce80065c6690ed72c349f8648343c",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W05/GROW_S2_W05_Lesson.html": "698a6096c4c6bcd51bcd3c1066c2b8ad2ce6d6b93b8e45b0e55e8ed6319e3a33",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/GROW/Spring_2/W06/GROW_S2_W06_Lesson.html": "0de35a96243bbad825f4291d4a28561dd14d863ceb5c92206537a58b23c26d15",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W01/LAUNCH_S2_W01_Lesson.html": "dcf1838d414e806b84bcae5df533f9471d7a8b0be0cd2c0852349b64ab866622",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W02/LAUNCH_S2_W02_Lesson.html": "6d85a5671d4c7ae280b59cf02cc2b8c593339350807e225d4b7714997b2e4039",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W03/LAUNCH_S2_W03_Lesson.html": "8d266858aae0337432f84c456fb0c8a675de36fad06c25d03ee732941da48991",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W04/LAUNCH_S2_W04_Lesson.html": "91baee0bb8cad5c48fac86615263c48173496d570df349252dea042463e9d93f",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W05/LAUNCH_S2_W05_Lesson.html": "e93fe22e4ee0db3d7fd05321521d804e3192d7f4f1299c14f42d523a00d284ea",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/LAUNCH/Spring_2/W06/LAUNCH_S2_W06_Lesson.html": "d10a5832ac7b86be298e4b08d83f3f426e6731a118287512aa94c2a187bb6475",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W01/BUILD_RE_A1_W01_Lesson.html": "6120f11ef73139427c72d16455a1578bcd9d41fc758073c43a647322139e5e84",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W02/BUILD_RE_A1_W02_Lesson.html": "32b655ec62d74cada8a009ddca5b0f4285abdb48e1c94eac598cb66d51267952",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W03/BUILD_RE_A1_W03_Lesson.html": "6ca005d877400b6893caf1b7e793c73f9c206e2fa29b25abadfae9fb9baf9b67",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W04/BUILD_RE_A1_W04_Lesson.html": "90b96500f6edbb3b918b7bfaded3f9f363d63dd7b2e615ec40b7fbb47cae5592",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W05/BUILD_RE_A1_W05_Lesson.html": "8bfead9a8ccd03a143697e997fdb2e571b96573657b3dbc32890c01848c8d7a9",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W06/BUILD_RE_A1_W06_Lesson.html": "47503b698f9f8e3177adcf855442bd50636ed5c363f19456c22e0800236e5152",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W07/BUILD_RE_A1_W07_Lesson.html": "c6e1debc5ebe82bc0d5e008cbbdac217cd5ffb7b045a6d4fa45d4bed74b0d62b",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_RE_A2_W01_Lesson.html": "51d8023fe37567838c7ef5b0e377b227a52b0cebef8b3f07afbfb1fb1a69394d",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Lesson.html": "52e8974f682baec2f8fb34ebf5d8087b95c03daffe82a1a2c2e7458b9e93bf28",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Lesson.html": "5e4d672e77b78ddaa0204dd6bf0e89078728a71de1afacc18fc278a59d65ad01",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Lesson.html": "c21d501faa52598a8fe87ae0c8ade2d6fdd273182cef2ae20df29ad2ba302d2f",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Lesson.html": "515595c44b56e584627f847a587e83243d8049fac9dd651ffd7795c320bba0d6",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Lesson.html": "789de9f9b1e1987b7b69eb7ad8751307b44108c6266a2954c198798d0fe41c7a",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Lesson.html": "8f9bad8798406811142c11c57e3b4e7d8c19e13e8a1017274cfe2a735fe67a85",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W01/GROW_RE_A1_W01_Lesson.html": "107d230da08bde88fec3b03d6e29b40784c67e4f787adc9bf9c93e8f42a4eba2",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W02/GROW_RE_A1_W02_Lesson.html": "40f2f7f7f235ac0d302e1ebe41e99470e6a1b27ae460c099a388994cfe78669c",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W03/GROW_RE_A1_W03_Lesson.html": "96cdab5f4ee79e2a12ddd84f0178ed88cad0647d73fe361d584db43811f7f23a",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W04/GROW_RE_A1_W04_Lesson.html": "fdfae07fe2feacf017787ccdf2feac14cc8fa621a1aa62604420d615f630f5f2",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W05/GROW_RE_A1_W05_Lesson.html": "d7761c238790e21249796574887cc4fecc01e4d52b5af4154266f972dc6fb37e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W06/GROW_RE_A1_W06_Lesson.html": "fcbcef20ba801a22fe52ba8dc7eee9fafafc47182db8a40047908436d678f579",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W07/GROW_RE_A1_W07_Lesson.html": "b2d87e32fff13bcef7aa5e4048df815dd19865a6b54313ddc81eb5c85b947fb0",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Lesson.html": "fb65f1586b54091998c873384d2220e350d6dd35996ab2e1c0ed2277b24e9cb0",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Lesson.html": "f003b991143ed389fb6906ba86d6786e299110ae9392729f9f6b0c98fa7c5663",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Lesson.html": "236222756ee58317ec9682321380a991ef2023ec70d0b7c19b5923ff64f4b9af",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Lesson.html": "35ebb0a72043e0e634770c57d62119786557985959dbb42f46363effa6df4fdf",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Lesson.html": "f82948b1a1596dc0873fdb1304acf5b05e20a83d1724e94775d2fd79d23bb666",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Lesson.html": "2fb6439e5f500c59d62478aa533531ca17ac821fb18b67a0a1d78c24625d7269",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Lesson.html": "bdea643384ee2df8e375fd793621bf391f0f428c0d4ff6b5dfb0cd3d7b304783",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W01/LAUNCH_RE_A1_W01_Lesson.html": "45ed365695f99c6965d56a00d1f007bfe90395ad03288cea0f7661cb84392472",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W02/LAUNCH_RE_A1_W02_Lesson.html": "d0e5863c27f12c9b252bce4b869c57fca10e85a23b0791949a6f9f29bed67a6e",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W03/LAUNCH_RE_A1_W03_Lesson.html": "b1bad16ec2c426bb2a88b77df29cba5e2b94afb80d2d0e140975019487d1df86",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W04/LAUNCH_RE_A1_W04_Lesson.html": "240e61b9ceaca4ae77cd199a27297fdc810aaa736b3ad216b2250747440e5480",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W05/LAUNCH_RE_A1_W05_Lesson.html": "681f3d41f7b37cae7bc4049d965c9f46c5e38cc619881abce403fb6fc1755cf8",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W06/LAUNCH_RE_A1_W06_Lesson.html": "0d5a0a71d58a4715ed30b644c08ef7feaeb43aec99ae7ca593f096b6d347ba15",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W07/LAUNCH_RE_A1_W07_Lesson.html": "335041a08d4094428b755c4f70e37f2fa46e55254978d189bdcca2ffc99aef2d",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_RE_A2_W01_Lesson.html": "61d368e16d5848253677a554f1071084ea88407c40d4c8d3cd6c40501396ca8c",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/LAUNCH_RE_A2_W02_Lesson.html": "c70a5941a35f28d163a49286a1c93f72626c2afc9d74655833336b1fd9a40ae4",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/LAUNCH_RE_A2_W03_Lesson.html": "962dc70295083424236b16615432c7572ab34ed03e02eb477b6cf172d04af0b0",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/LAUNCH_RE_A2_W04_Lesson.html": "fbdeafb79997d142e7cd004d9b21af62ea162df778b64c73ba0e290aa906512e",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/LAUNCH_RE_A2_W05_Lesson.html": "2ba488d168cdbb7efc50ad018590fd8bae1bd6af7ce83826ab039f82ef5e6651",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/LAUNCH_RE_A2_W06_Lesson.html": "ae521ec05c1d2422b1fc850d34d291c528632c67b10f705eb2af97a7a48ce84f",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/LAUNCH_RE_A2_W07_Lesson.html": "79a92af856b83dd7961316d1f6a953b320c4689ed25d467e40128a89938c47a4",
        "Science/Grow/W8-W13_2026-27/SHA256SUMS.txt": "3bd2c6ea90c2ee8071c6ae92ab8136be3541d05a16f4f94768431f819c5b152a",
        "ASDAN/Consent_Aimee_La.html": "fba7cf591575cee56f8c8d0ce77d2f03062a4331452c3ff59049310da2780243",
        "ASDAN/Consent_Aimee_P2.html": "9f2c79180c0e6fafda27db94028c53576e3095f80b8b950bf20aa2c6336f1f92",
        "5_6 Local Choice/Rivers/L1e_Final_Briefing.html": "36c042c860537077496228e60939250cff49f9026a69c225b1a4d74d6424156a",
        "tools/liveteach/lt-pick.test.js": "2dc2ed2e3cd21c315f4dd3d7b9000cf6a4b05b299cba8941a5f64db138e76c98",
        "LIVETEACH_LT1_CONTACT_SHEET.md": "364c10fc887179c0ae28bec0919146c64f4ba5960026b213d732263c047cf98c",
        "LIVETEACH_RESIDUE.md": "5a18069638e4bbfb6a4da111f68e4ac3a17f5de4c8aead731d718f794d89e400",
        "404.html": "e899e06d5908fd29dbf3a1011f8e7e7c5c46b216a73a19835c4197b6431c58cc",
        "Build/README.txt": "84aa743004ececee3d3e9aedc295f0afc0f686124dd1b2f2f422b38c7b282a61",
        "Games/WorldCup_ThreeLions_Final.html": "ca6281bf6ac5e0d9eb1d7d10b14ceb75b38f07fece140a6523b24ea070f3f581",
        "Grow/README.txt": "9c2c46c4ebfb56c1ae99c7c20ee2bb73a623a3525c8f3daedf718599b7e7cfc6",
        "HANDOVER.md": "b2e4979f17db2ac9dcf2ed8eeb3461ffbdba19ad8713a40b33388132c18381ce",
        "Humanities/BUILD_Scheme_of_Work.html": "2c66d10240492b848d6242d261f1e7a9cdc1f8b756c718f27ad4fbdabce64a31",
        "Humanities/GROW_Scheme_of_Work.html": "f8de9c18ce88bc07a3eaec7bf73a2fd5917253053e4997e7e20a6fe7ce5a2dd7",
        "Humanities/LAUNCH_Scheme_of_Work.html": "4ce63bb630955552535e937ff08df51bd8f9acad9375d88eabff2a13ebc0b8b1",
        "Humanities/Pathway_Tracker.html": "28b134324fd748c745bd59199334dd20331dcb9cebae8982d7cd1262e745d8f1",
        "Launch/Art_L1_Colours_Lines_Like_Me_v5.html": "7218c677193750c4b7e4d7c542736dbf6d3f413dce931921f16210e594f5f69f",
        "Launch/Art_L2_My_Identity_Picture_v5.html": "058540b4dfc57ebda2d9c41cbf8a40f9701a66964729ded273a56ae8500e4641",
        "Launch/README.txt": "d298bccc19f2dc4318a5c5e0a9cdd79b81a7bdc7d20c9d07237b069335ac3f50",
        "Launch/index.html": "997eab91b19a7476cf67c81338b6e23932391bcfe2fefaa1d93b917b36335749",
        "LundyLoop/2_leadership/Head_Office_Summary.html": "9395e47831d7f2fe2b1ebd3ce88cd40de5c811568323b3108e1c05ffa5136a36",
        "LundyLoop/2_leadership/Loop_Walk_Logger.html": "40075564d6166a2b9e6a91dd63ef52390a0405762b677796c60f3a2f36f88cb8",
        "LundyLoop/2_leadership/implementation_plan.html": "1641bf743e49a10414170a0cf190ae9758a5273c7b7cbc9120041aab6c42c5f7",
        "LundyLoop/2_leadership/policy_alignment_matrix.html": "0c3028e51fdad33b163abd906536fef43c29111d42816feffc2fa21ab600c71c",
        "LundyLoop/2_leadership/qa_coaching_sheet.html": "a86b54bacac3c4d5984d5c6750d2e488d5e2b713caa9a86729bcf2c53482901f",
        "LundyLoop/3_subject_guides/art.html": "9de2ed9bc34e0886636f17a9c3df0c4c4b97dbcf3c4f945d688818b7fab2a9a5",
        "LundyLoop/3_subject_guides/asdan_pfa_assessment_companion.html": "44a75d4b71343c5752ed51991e95480287c5a7ef7a559d95d419c8a870fd190d",
        "LundyLoop/3_subject_guides/d_t_and_food.html": "22731c5fdb9e564b766a299541591fbdc774696d1ba9879ad3b21866325238e2",
        "LundyLoop/3_subject_guides/english.html": "6caaa7e80b9c842aa07e17b81b55ab359c855de3eef1588676a8f1644a376cfd",
        "LundyLoop/3_subject_guides/humanities.html": "e5ce252ac77bccff682c3fab672fcb2ab2f022586b2c02e1b189c295b8f64849",
        "LundyLoop/3_subject_guides/mathematics.html": "1ed1f7886102da5e9b4baf1c9dc50b2ec442ea1ce56022e21dd4163e785f45f5",
        "LundyLoop/3_subject_guides/music_and_drama.html": "490525c590790b528422e75e1e3ee4fa08f126d736af67332b798bb056d12524",
        "LundyLoop/3_subject_guides/pe_and_outdoor_education.html": "b0b34da62e1c51d753578b0c0f4dcd2ea81a9ee1e0ecfdab64ba765da172c2d6",
        "LundyLoop/3_subject_guides/pshe_and_rshe.html": "4fe7958c91c6da54e970601ef00ca00034142da8c9115a5bf788c0a331ff2aa7",
        "LundyLoop/3_subject_guides/re_and_citizenship.html": "10852e9190c8cbb0778999aadbfb5ffc2d707f3bfe13d507ac25964aaf1e9ab2",
        "LundyLoop/4_send_and_pupils/Loop_Passports.html": "8593137a25b76d12daf4e9a979937581d0044b4db6c40c69d18d1b0291800d23",
        "LundyLoop/4_send_and_pupils/Pupil_Feedback_OnePagers.html": "0637643812d9b63bf4c25939d8c4516255d33ef6dae78a821328752a5a523b67",
        "LundyLoop/4_send_and_pupils/SEND_Overlay.html": "2916475db946e788fa65bba3a5f2f5b291dd749309ad26787f84e14c37149f71",
        "LundyLoop/5_staff_training/INSET_Twilight_25min.html": "3a31ce1783b035f1fee14105561291d7322dcca06899425db31b73c09c233f86",
        "LundyLoop/5_staff_training/R_Gate_Calibration_Game.html": "e4a730dc50ee1cb55881b51fc9ffc894a65fb4e77d94b7b233c5a0f81e879e26",
        "LundyLoop/5_staff_training/TA_Card_Lundy_Loop_Progress.html": "562923adf14c2bee395d735e87097487038cbede4b37552ed11f92402caa3f61",
        "LundyLoop/5_staff_training/calibration_examples.html": "b7e32613bc33befac9128e11fafd1377c58fc5ca7c81ec77fe76f3d5bb649251",
        "LundyLoop/5_staff_training/five_minute_briefing.html": "a645118122686cc1e1a1aac3ce259abdd87bdb7aa6f7dda5efbbaa53607169be",
        "LundyLoop/6_posters/source/powerpoint-source.js": "061fb14a62b693a6fb60102d0aa91a2005fd2727ea27ab292d35a43461ca6533",
        "LundyLoop/README.txt": "111af76af1200850ae03a779636cd6696fc6b4584958d20512d5be7e59d52d53",
        "LundyLoop/index.html": "f0fabe0c3bb7db290717e69fcb4cc2872fbce309a8f86771f31936a4041f6b57",
        "MASTER_PROMPT_Live_Teach_Projector_Kit.md": "d561dc7bbd5a7e94c5e1fadca7ee9fe4785ad77b2c9a13be28d288c31a7b32db",
        "Planning/BUILD/README.txt": "84aa743004ececee3d3e9aedc295f0afc0f686124dd1b2f2f422b38c7b282a61",
        "Planning/GROW/README.txt": "9c2c46c4ebfb56c1ae99c7c20ee2bb73a623a3525c8f3daedf718599b7e7cfc6",
        "Planning/LAUNCH/README.txt": "55f962061c660a001b8c1eba0a282b26c805498cb9a2106fb7d1e6bc3ffb391d",
        "REBRAND.md": "89826a88bcf37e85e1a4dc8b6a92101192407ae84f6d3cec6ab534b346b4d609",
        "Science/Build/v3_40min/BUILD_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html": "bf7e040bd47cb2921b92545c6b4b76a81e3dd643734353bdae49490499d2d83a",
        "Science/Grow/v3_40min/GROW_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html": "613e2d77e367617fc252b43007603f4cf8d96f903f196d56831e0308c8454aa1",
        "Science/Launch/v3_40min/LAUNCH_SCIENCE_PRACTICALS_MATRIX_PROGRESS_SCHOOLS.html": "90f5873faa1ed5f1c6c1d83af3a5c06ae41bb028588e066a4d86409c92f346f3",
        "assets/catalogue/science-download-bindings.json": "1e44e0fa5f772b4e65722520619ecd20f0771faad79c4db7aecc5d955bd3305d",
        "Science/Teaching_Packs/BUILD/BUILD_Science_Autumn1_W3-W7_Teaching_Guide.docx": "c4fd055acdb11a2310fe820b6f473733835dc4789b9151cd3377ec4d251f2196",
        "Science/Teaching_Packs/BUILD/BUILD_Science_Autumn1_W3-W7_Teaching_Guide.pdf": "a479821f2de450e28bd414625f8066768d2c72423bd5ff76046536bf8f7a5d7a",
        "Science/Teaching_Packs/BUILD/DOWNLOAD_INDEX.json": "d5656956c366d611eceec99574a3643936e1b82a0b6ee6256fa130bb0621523e",
        "Science/Teaching_Packs/BUILD/SOURCE_MANIFEST.json": "d737b988e0d3aadfe577aea62cf53933eb8d7690dafd326a595162b7e33bd540",
        "Science/Teaching_Packs/BUILD/START_HERE.txt": "7dc574750bc326685d64d0abbd25b632e9f8a724c7aa84f1123055c7f148ec7c",
        "Science/Teaching_Packs/BUILD/assets/made-by-matt-approved.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3-W7_Complete_Pack.zip": "1e66202c29445378b10feb01a5cfb00ce93c43e1fcc3bea9de601d85f6333cef",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3A_Backbones_Lesson_Pack.zip": "f196c85140c531a494a79795e374e15d4bc15121d1e3f3983a1f256ca56a73ce",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Lesson_Pack.zip": "c4280ab8b6408a2c8ff2d13bdde1955841058fc987410d6c532a6db9583582d2",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3_Teaching_Pack.zip": "07e47f445e89ec22b2d8c6050b6b74b7f987732b2655f0d8db071e7e9124ffad",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Lesson_Pack.zip": "d919d3383c97e43e00c542383b62bc9560a1d2f68e1cf5bc763df23361f71c6f",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W4B_Muscle_Model_Lesson_Pack.zip": "ad0d2d1e18cca96811a3acdc708092c6b909d938d6596b4860eedb7d3074f7d3",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W4_Teaching_Pack.zip": "02c91af4af1139ce14542c12fb13ee76bcb82fb7b1faad0db88c36a375d9ad7c",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W5A_Body_Needs_Lesson_Pack.zip": "c4a130816b5d17546fe43566f4c2e91b979cbd01878a23adf6f005fe9dd32389",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Lesson_Pack.zip": "9e3eabe0aa4866eb2213d0aa7d2165983e8afda85e379f6e2783cdc367a784ca",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W5_Teaching_Pack.zip": "9e55e314b5c03e9f80c64a80b23aae7c200b964d838962783d02bc975e464a1e",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W6A_Balanced_Plate_Lesson_Pack.zip": "ca62ad075c5614016e2cd3c352e63b0d04662474832c0c28c629f2a52b73942b",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Lesson_Pack.zip": "fb9965490c8a5d44fd9e2a5423405740e1b9df25857f571a4eb4519194291643",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W6_Teaching_Pack.zip": "60346b224bd796e8f9a6113605ee3a98494e789a6d28585bbdcb0513429fd8fa",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W7A_Food_Sources_Lesson_Pack.zip": "53c8c7e375361c2c1e3ccb900017d6f5586a3d90fc5b3a14be517eb81aad419d",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Lesson_Pack.zip": "04b0bbf1564ee434baa39236a5154b7db6f1867a837a2f806c20519064db4d6a",
        "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W7_Teaching_Pack.zip": "5b9c1475cacc375538872ae480d5e071ed06faa2d0d34f58d38eda32dc3d1014",
        "Science/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones.pdf": "570c42fdaeef7d4c714e5b78bb49d970cfecee79414a1610b8d6db337d74d635",
        "Science/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones.pptx": "07e840c37da904610ea52fdd1ae0b6826aa0426d2778b82548fb4f006e63f320",
        "Science/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Pupil.docx": "58837cc18cfc2d44a1bc7b24be6fab2342d2dde54e6d6647ba082bcc553391da",
        "Science/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Pupil.pdf": "4324477322dd593ae260e14c8c3e355ac33a43d9b432aca25af5332f470430ef",
        "Science/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Teacher.docx": "a30fbee2586c2b803f07ecfdd7ffa5c2779ef519b0614951258bbee6605a6d15",
        "Science/Teaching_Packs/BUILD/lessons/W3A/BUILD_Science_Autumn1_W3A_Backbones_Teacher.pdf": "6852b465cc9e424cb792f108fa31ccba452f90a71f9252c7302be66247dcd059",
        "Science/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence.pdf": "8d6684d616b4dcdab42f08bd1935eb88f11572756368bf53a912f81b51d5c745",
        "Science/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence.pptx": "19d4cc8166e3a9d995d47dce93352a533e896183f3314a003047d2de8c3930c2",
        "Science/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Pupil.docx": "82f1d04cd6358fdc3f6840ba00cb339b59259b02bc2a4e42bb97410b9e1c0afa",
        "Science/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Pupil.pdf": "9a79a4609822378d5b2fcd4980172de3f24f485789e46dd5ec88efda31003508",
        "Science/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Teacher.docx": "7f849b0158faa1fe8bba0987354f487e6c78022df3e4bd1b5b1d4f1b61c051da",
        "Science/Teaching_Packs/BUILD/lessons/W3B/BUILD_Science_Autumn1_W3B_Backbone_Evidence_Teacher.pdf": "8b7f52e865574def5fec30400ab20bb5a9fcb0caa9e9c69ed3df33d508905fc1",
        "Science/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs.pdf": "e33f83b4f6636b4cccbff17c5f05627cb15970fc4ded60269fde2414a86e8a7b",
        "Science/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs.pptx": "36e216298251f9764baa23bd8d894b37c2d415fe38eafdf17b33729cba7f07ab",
        "Science/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Pupil.docx": "0dee5d479908ccc14ac17afe664d8c430996d3ea5aa02ba63db5062285445255",
        "Science/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Pupil.pdf": "7f1c1f45d405743c4c5ab3b4ee1728a2d5e4bc49e0dbe80174ca92527d7713f7",
        "Science/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Teacher.docx": "417d3907c7395c5dd188a2001a0e7578212bb87fcf061490cb9bb2b78d41d681",
        "Science/Teaching_Packs/BUILD/lessons/W4A/BUILD_Science_Autumn1_W4A_Muscle_Pairs_Teacher.pdf": "e834c2e011e8236339745cb4bee8499eb652b8f50b349db576f2026b182bb940",
        "Science/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model.pdf": "e905f9f66c1085e5f4dd1dca6a01a9cb12398f7cf58ae72c9f5c0680db86c4fd",
        "Science/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model.pptx": "835302e10c4c9d42b607f8004991e211b37969088a75a8321167686c580c2ea5",
        "Science/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Pupil.docx": "2386806265db047de86ee81877131e6eca2d49eb6896cf5e932d05d6fffcfdaa",
        "Science/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Pupil.pdf": "62241873d87742418b8e9889f3f21d510b8ca7eec8c066d9cd9a2ed48c61c31a",
        "Science/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Teacher.docx": "7929264661f58bd50b6b3d37445efee1aea81c2986f2757e958782febc6eac22",
        "Science/Teaching_Packs/BUILD/lessons/W4B/BUILD_Science_Autumn1_W4B_Muscle_Model_Teacher.pdf": "b58f2f31273f4b5e0fffa7c42c31bb82e741b9a726bc415ec8deaaf353e95beb",
        "Science/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs.pdf": "fd6c8d2f57ebbf3ed3159dc6dce0a87badd45fff85aa9807872cccb0e48b214c",
        "Science/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs.pptx": "61aedc65b748140e93f0a8d33846f22417c9c8dd45f6d7f397c74d199bbb0018",
        "Science/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Pupil.docx": "bb1c470bcd7ce4b8d67a5c9b40c2927a6c5e4c45c3a1929f692411244055b835",
        "Science/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Pupil.pdf": "400c06df0345091f8106763ef3c87d6827c8c08460ed63e6c3cc6978196ce4e9",
        "Science/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Teacher.docx": "3aea73afd099d214959dabad16ccdc5c4fccf9852def555d90b93a4fcb6742e4",
        "Science/Teaching_Packs/BUILD/lessons/W5A/BUILD_Science_Autumn1_W5A_Body_Needs_Teacher.pdf": "59b102ac7c36b715834e1d4143f71ff19ddca35223370487cd99500ac4f2a23f",
        "Science/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission.pdf": "a44ec33f0c1bf6aa8169b18182a746623ec195d4eb73cd3381875173c7d9f5f6",
        "Science/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission.pptx": "97560a78fbc990ea1446a64a509f01b0a2de0541cc9d82cb56ee557d0b28b223",
        "Science/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Pupil.docx": "5470a602ef06198ac0936289a59633c6ccddd5f57a9e3f69a88467ecf499632a",
        "Science/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Pupil.pdf": "bdd15828211eda839093c742513381f6401c1137f9509755244b832f78d467f0",
        "Science/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Teacher.docx": "cc7f542d1ca6304b1b19d821ad981c4bfbb844da2aaee781d769b0d91d5394a1",
        "Science/Teaching_Packs/BUILD/lessons/W5B/BUILD_Science_Autumn1_W5B_Food_Jobs_Mission_Teacher.pdf": "d101e634948e248cbb81c74d1554e9c525ed1c060672576ecb118839ac75c85a",
        "Science/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate.pdf": "a256991e850c6067ff8ef438d044acb16978bc2ec5eb22f0b4e75e427be145b1",
        "Science/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate.pptx": "f2e49ddde23ee01511021c0c531e67cac435334ac2387ee8cd964fa4f1c09352",
        "Science/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Pupil.docx": "5ddd738899464e13f47797484c7b67bb8d180f8dfa54190ce6a5ee6989c481a3",
        "Science/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Pupil.pdf": "2c0bd6f86ef08e5566c0d4b0dddb7eb317fd8231fb6d839a1c7ab0e247282811",
        "Science/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Teacher.docx": "dd41e08c1dacf4665b8d0738e0ebdd0afd9adcdc9014fc4007a81bcc774509fb",
        "Science/Teaching_Packs/BUILD/lessons/W6A/BUILD_Science_Autumn1_W6A_Balanced_Plate_Teacher.pdf": "e38a3490fe006d6b1f5ff54e4b93f02b33f58aa912822d5d31d6c3dfaf5389dc",
        "Science/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison.pdf": "78ba407d2c75bb56c39770ef002350a522868ab35dd49bb91047ea1728e4739a",
        "Science/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison.pptx": "c0c0424d3877f7aebb676b425044ac93880dabd761988368317580ca5adfcab6",
        "Science/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Pupil.docx": "5f6021b68a0d49d75caeee2d2d188913bdbff24bebb5c50e90e7479e0918111e",
        "Science/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Pupil.pdf": "5e35dac7e16dc7548d64aaf8af3b00ffe8e5e554bb8076d89ab47b57975429e9",
        "Science/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Teacher.docx": "32a3c2580e7cb8b6e2e4696419f191255e3e01090f49f7ef0cf066ebed149d70",
        "Science/Teaching_Packs/BUILD/lessons/W6B/BUILD_Science_Autumn1_W6B_Model_Plate_Comparison_Teacher.pdf": "cc6e4a4a9d9510c84ea3dbe1a50c01e5f67721933dc543c14c3236f58f7b345b",
        "Science/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources.pdf": "e2e5d516894e369e93861d63df96a6fbd163b096583c7d26fc0d541f38ff2fba",
        "Science/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources.pptx": "e1b43759dab1b36e2e8da895ee8542713a9763e9f615f859f64b5e227ae11470",
        "Science/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Pupil.docx": "9685dc0158aa3b7db919980e4f9347805b494f74d0a3835327577962fabd279f",
        "Science/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Pupil.pdf": "c566123241ad7acd6e6a3753abfe459934d320065151ffe83a36d6058ccd0d57",
        "Science/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Teacher.docx": "382f902b5c4e99a7043645097e676ec37928f0ed1e1bd9598ec84f7107696ec5",
        "Science/Teaching_Packs/BUILD/lessons/W7A/BUILD_Science_Autumn1_W7A_Food_Sources_Teacher.pdf": "65c5f93f10a5bc68bb46e904a57cdc0eadf9bdb947c99181b04c31db41bb641c",
        "Science/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation.pdf": "6cb785fb6c253f362d4caf168f6e06bbd77fa33ea41edfc44c29757189c9bfeb",
        "Science/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation.pptx": "4c91daa2018cc0f0df7256ea1933622dfb7505d55ec38002a6b548f3355d0433",
        "Science/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Pupil.docx": "f10192242483ec30446302afa3ce6334f5c54c9782bac2f352e55ef48b9ae4e1",
        "Science/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Pupil.pdf": "bff6a31bba74a70e7875cf823cee12354abc0cf6c0e28672345e758f9f89896e",
        "Science/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Teacher.docx": "b9d84baca89f4f2498fa14e228d9a522b1ed4009c4bee4f90fcb213f1c992ccb",
        "Science/Teaching_Packs/BUILD/lessons/W7B/BUILD_Science_Autumn1_W7B_Food_Chain_Investigation_Teacher.pdf": "3f2816a6722bfe7b18131206002491899b989a530d8509c59ff2b0871fdc7d61",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W3_Cards_and_Labels.docx": "1ecfd3c50271dd3895f9cbdeb5cc29fb92b08090ba040f3736b5936cab1767a4",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W3_Cards_and_Labels.pdf": "cc6c60baa5ba53dad174ec6749ca054c06ae12730b212b255a635acff35eec2e",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W4_Cards_and_Labels.docx": "c21fd7caf1ae81bd24e2d6d8de073d79361df2767ba204e38de3cb3680bb4aaa",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W4_Cards_and_Labels.pdf": "431654dc2a70d637463ac0c3c0627a33efbcd21ba9f55760da5c18151ffcfef9",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W5_Cards_and_Labels.docx": "ceeb395e64389eecf1af8b3e72e46a96f1102093ed95ae872ba8894d9aecbe21",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W5_Cards_and_Labels.pdf": "d198a60d9b24a3a4ab9e05d2cf7f6eff33e05bc411ba4ce32aab3f0410ad727d",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W6_Cards_and_Labels.docx": "be0cbc702aef03707812a2f84e3e02737bdc2299b3e7baecb1cc9cc98c5dc2b9",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W6_Cards_and_Labels.pdf": "da0bbeac4c479fc4f20173691e236a67e7c936856f6b460332847810c6b4fb60",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W7_Cards_and_Labels.docx": "9bfdec7cd96599afba6e9421ad9d80fc7df9e07be01d5334c5b8a61319919aee",
        "Science/Teaching_Packs/BUILD/resources/BUILD_Science_Autumn1_W7_Cards_and_Labels.pdf": "68746df0bf740914b914ecf6d6c2a1b4b39252171e50621fa7a0c4aa4d1f141f",
        "Science/Teaching_Packs/GROW/DOWNLOAD_INDEX.json": "df85278ac30254d8fa806baaa5a6b19f2bb634a3b0a7023fe766c68d839aff9b",
        "Science/Teaching_Packs/GROW/SOURCE_MANIFEST.json": "e2d194b4151a345daca8b9fec8f67db961d88cde133e5b655eccc9644e6f906f",
        "Science/Teaching_Packs/GROW/START_HERE.pdf": "93a7e61be570fa6934e93973b1a4f4eb200df3da24f83b8ba45ec64ccbf80375",
        "Science/Teaching_Packs/GROW/START_HERE.txt": "856bddba97acc3d6389f09d99d3b0dc6224a4948b2be46c885bbaab7d9485c93",
        "Science/Teaching_Packs/GROW/assets/made-by-matt-approved.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3A.zip": "16bf28c4e0ed8d754db564cc147dec1ec84956e5b2a3453d78c8463d4bccf687",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3B.zip": "77174c720e049cb79b37caee6ba3c2bb0f26ff07c638f3d0184f5d026b09fe1b",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W4A.zip": "3f5917a779d2119a9356b454b8cb3b4180e0e2a8a66d290fac91f7de3fc1ce4d",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W4B.zip": "3a3d79d0d479dbca9c4380071625873e4553221afe21a0a4372d308c60300434",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W5A.zip": "9434d3446815da5461d64c16d6d0b35c0d1066c3b971492a2aa29b9221333141",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W5B.zip": "2e2e8d8c554dc47b1405ebb34b3c8d8b7da3b2a8e3118e9a67b7fcef7207ae5e",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W6A.zip": "ac2856d0c00ddfee1d31fc1a3f3f31ff80e2161a7e0b7f706b19e53be42b7941",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W6B.zip": "3c30ea234c4decde141a25979ce457f3b031addd887cb010daab12dca2b0ab30",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W7A.zip": "6331ade7e38a9fa806ad1965b90e2c7d026a01b56cfd078e299f4b1e194629a9",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W7B.zip": "fb9f571a0f5397ba61c5e9c661a61791647b95868b3d792a515eabbb23febe94",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week3.zip": "6729dd874e434096bdbe5b7ab7b33db1ca5d9a95369f5b5c8dbcb4d4da94ecaf",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week4.zip": "98300c761585df193224fed460aa91ac929b91c3edef7a64eeb61f11e3e968af",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week5.zip": "3ff2075063455fe190397bb383c1d7dff3f17c6fc3a3b41f8d734bf206ffed39",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week6.zip": "22d6c481304de88bed8a65e533cfe7a30f00d93b59edbdf107665eaa88dd68c1",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Week7.zip": "78ebc1a11f9967fad4fd2f1f468121e2ce7c43067069f01e361dd1d1bb85e712",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_Weeks3-7_Teaching_Pack.zip": "3be54e29329689533088a06d8b23c2bd52c0e745d01a7bfaeabc034fac96abb9",
        "Science/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pdf": "0e57d93e45bf29236754a735e42f6d2ae923aa1a23c65ebe9ed19041347ced7d",
        "Science/Teaching_Packs/GROW/lessons/W3A/GROW_Science_Autumn1_W3A_Friction.pptx": "13dceb4a32f65165df9353349a69c87465e7f33b9f941036f8f714fd10a9f9da",
        "Science/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx": "9f8afdf8df90eb845d3ea352d36b9bd19dd192a6c040883fe70957eb8be487de",
        "Science/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf": "856691efece9acaae40a529f949f3d26567345c8f658de9e26eab1bbbdc585cb",
        "Science/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx": "9da8a692bd1ad6b4a040e4b4a970275c90577cbaf73342492d1908148c5d8717",
        "Science/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf": "08c926202671c6b2c25778d5d2dcf2f99a473dd704201f0ef9a58e3a359b18f9",
        "Science/Teaching_Packs/GROW/lessons/W3A/START_HERE.txt": "b5c46c92125be91cb86f64c5969ad8378ab3948b41a82e7be01e7378ccdfc81c",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pdf": "1ce1ba083eb62b521368b3c5863c098733ae7d677a1e7c0e641b8e0fd7681d3a",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test.pptx": "3049816d76009ebe3ad1b609e9ca22ec54c3abc82d3e8037b012386759ba278b",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.docx": "e4333309ef2e2dcf587385063c8e43eee56c3a285089b4f749580124d8c128ea",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Pupil.pdf": "7ddb70eb886f743fd0813b5d581435b36bdfb1a5813e23a6cb6f3b95ccdfee8b",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.docx": "c0e2ae5adaff89fa05b28e389f7d422e0f638ca9edd33313da61d57d258732cb",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_Science_Autumn1_W3B_Friction_Test_Teacher.pdf": "c9c7bf0a6dc4b4a69c1df89bf7fc3a2fdd73c57828ecb0619688611b52a61d5d",
        "Science/Teaching_Packs/GROW/lessons/W3B/GROW_W3B_Friction_Measurements.xlsx": "7ab6650a16051e655dde2f48928810cb2a825e07d4d0a028fea7cc25ee64b1d5",
        "Science/Teaching_Packs/GROW/lessons/W3B/START_HERE.txt": "70a87773d7f0bc53b67cc1023263f2837ec473ceffc6ec1fc79b82823805c756",
        "Science/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms.pdf": "4af5fdcdc9e4d5c651545fbbde812762f924249d42a103d3e41ddfe49c120051",
        "Science/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms.pptx": "394e9a36b4e15708e43346e328c82f89ab3323d4de1df0cb0e2d9743a22d1044",
        "Science/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Pupil.docx": "4621245842054aa069124ff174f09c0eff8f8c56769d37c1acea9afe75f3045c",
        "Science/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Pupil.pdf": "1b2156236206deff8ec4f909faad3fd552c4caaa0a67cdc703cb900c6eedae08",
        "Science/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Teacher.docx": "d6324f71091db4971ca431f635995a5237638871b7a3a4a3455b75a9946425aa",
        "Science/Teaching_Packs/GROW/lessons/W4A/GROW_Science_Autumn1_W4A_Mechanisms_Teacher.pdf": "e7cfbdfcd17ce2734650cd91a04768a3da95156d6acd92bf6956040961d53366",
        "Science/Teaching_Packs/GROW/lessons/W4A/START_HERE.txt": "eb41429cf022ed25c1dfc3cf05d21787608cddc59982cc9d5aa2357135fc842a",
        "Science/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test.pdf": "a7ce2404efddea8e8e4adef88e7e5a54659cebcafc42805dc299370a06569e6c",
        "Science/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test.pptx": "435e8601d04da39509358516118a7240f1060425c0f4ed78a166566110ac9b35",
        "Science/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Pupil.docx": "11f958262f40611264f00fa24bbff2292cd214ed84b03204b398bd017a7802e8",
        "Science/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Pupil.pdf": "317ae814fd7d1968d2c23a865df8457e2e00838b68bbf32972de1f59ea650c71",
        "Science/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Teacher.docx": "ed27ebae53477ad516ec1580b8b0a67e6c81c2eed031ad5094a291b7a24c5835",
        "Science/Teaching_Packs/GROW/lessons/W4B/GROW_Science_Autumn1_W4B_Lever_Test_Teacher.pdf": "21bbcae5a4fb0667afcb6069ac59ed7c80e12ce15b174aa4de67000a8a8080fa",
        "Science/Teaching_Packs/GROW/lessons/W4B/START_HERE.txt": "ec3da721d7bce358ce3458b77bbc5bc0c8ab01a305486e2c711d7919cb5daaa7",
        "Science/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test.pdf": "5057527cb48084fadd02863d9cab017e71818955efe11da514300c5d86743123",
        "Science/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test.pptx": "b9a829b1e5cd38fb891f687b2521de4da4e5e10d433610f614720b21ce14098e",
        "Science/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Pupil.docx": "b3a5a3a18ffeb6c72a53b1f23379efa730f8981795509239d072408fa44c99e1",
        "Science/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Pupil.pdf": "1e6e19a583143063af3d001a7039c89feaf8aa0bcd9553f8b0dd9e58218aa5e8",
        "Science/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Teacher.docx": "5ec3f179b213cba5730070d69c5a46b3d7a20c7bbe665c3049d1f3012e5fc1ec",
        "Science/Teaching_Packs/GROW/lessons/W5A/GROW_Science_Autumn1_W5A_Fair_Test_Teacher.pdf": "adbf06615291d03f65665098eb1aa6a21d7aef15a32dbd2742bd41640d6c3608",
        "Science/Teaching_Packs/GROW/lessons/W5A/START_HERE.txt": "a290efa290a30a831a30ef59dd7fd7826ff7d8906de67c3698caf19619681ccf",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical.pdf": "3782fa567cc5c389de3801cc57a6c46a425e158fed71cb554507537229b833cd",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical.pptx": "946c83f16a9f5357f5d13241039c48a0869c1406a198daac348f8a1e07392ed9",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Pupil.docx": "6569a9920bd4597d4fc41fe10709451062fca39f5419c0eb030ebd0be5d85b00",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Pupil.pdf": "06d2ba4a1bd1a1ee3175877c9fdb108f3b60d510fa3c843444f61b7bec591fc6",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Teacher.docx": "88bdee24e177ae31505cbfe467083f11dc114c0e3b55c3b200a26fe944839e00",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_Science_Autumn1_W5B_Fair_Test_Practical_Teacher.pdf": "891c8c64d24767bf85c66c956d9bb85842688424c3ea71eb967e1e6e3207afe2",
        "Science/Teaching_Packs/GROW/lessons/W5B/GROW_W5B_Fair_Test_Measurements.xlsx": "746d64a30be2304c439fb5af7ef79b25dbe8f69d51c8de3c12cd22b8f2ac2104",
        "Science/Teaching_Packs/GROW/lessons/W5B/START_HERE.txt": "d667aaa4d4c65214655f7f9744b7b8b240d5a5d39539300c35aa5f4abcf65ed1",
        "Science/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets.pdf": "31be861dc9629f03f58665c7e2455c4bb3e1bcf4c0eb954dced62cd6d89608ed",
        "Science/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets.pptx": "1fabda3827fa43febb7fc3836619f5dbb7847deee60736c0c72dbc9047d30982",
        "Science/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Pupil.docx": "91bcbcbfbfdfa3039f205b9c08f7583fb126c5bd0953a5968921e1ed5eec681a",
        "Science/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Pupil.pdf": "08f14322ca35b6da824b798ef777f1e82a17b8c44ab032ce6da19c87fb12a60b",
        "Science/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Teacher.docx": "8568d4650f1adeeb8524c86799e49e2172e39dc282f80304471ba81a2f731c05",
        "Science/Teaching_Packs/GROW/lessons/W6A/GROW_Science_Autumn1_W6A_Earth_And_Planets_Teacher.pdf": "1e1a3882a6716e9933f81a5ec94dea92fe8e0f06384080b3c8fe324287cba086",
        "Science/Teaching_Packs/GROW/lessons/W6A/START_HERE.txt": "922b972648e167684acd8d528e0842294ef89a61478b74b65d74ce22c25e15bd",
        "Science/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets.pdf": "82649adfce0d1fbf07b3d5ab00719ae0936812fc8b485e66ea58ff47108c46f9",
        "Science/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets.pptx": "90435b48ab9baa82bd2a3b266e963c2710bedfe79f88671deb2989a859be6602",
        "Science/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Pupil.docx": "35785f5169326bc4115abea9934d254ff990e7ccaf3b104bb2469bcf8945a16e",
        "Science/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Pupil.pdf": "a2bad2d15b930cce103dc59e5e65b15f63b34afecf3c8d54a8358c28126c6940",
        "Science/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Teacher.docx": "d29f02f60a8ac61014113416c8c1042520f3b1a6815476f12b830bb72eff6f56",
        "Science/Teaching_Packs/GROW/lessons/W6B/GROW_Science_Autumn1_W6B_Earth_And_Planets_Teacher.pdf": "318cf84513b3ef6daa97918782dc2ec845cc0f4a5905c315e65a4a92bf9eaf08",
        "Science/Teaching_Packs/GROW/lessons/W6B/START_HERE.txt": "488a26039677af53ef3d8435dd412e98406a807d10534a7725d2261d06869d23",
        "Science/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon.pdf": "c7cbef511bb242f2155b64c64ed8557724d128a469b21671bcdf2b2ca014a176",
        "Science/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon.pptx": "430e539a95c7c53ee57159ef43f3fd3c88fa175ebd58a5a7b32693314ee5c2a0",
        "Science/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Pupil.docx": "d4565fa4adf2bd77cc2288652e0d43e15c066a3501bc7a454edd02eafbe137b2",
        "Science/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Pupil.pdf": "bff2ab37b1c04a2afdb9d86f5a17822d3fa63727e76aa3d563e77d2bdcd8ebad",
        "Science/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Teacher.docx": "bc036875e5bd9e9ecb6e2f1f52d9dc0adc42f486d6bf04d246d02aa78dfbd763",
        "Science/Teaching_Packs/GROW/lessons/W7A/GROW_Science_Autumn1_W7A_The_Moon_Teacher.pdf": "64f052a34a5849381178f8a22dce9d865afb2b2602a0f805004e75149b450cc5",
        "Science/Teaching_Packs/GROW/lessons/W7A/START_HERE.txt": "447de6ad4347b097a16c09d40df429a4908e381b6ed9c36084c2e1cbdf6916a6",
        "Science/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon.pdf": "8a8946342e27252e71994094866df85a98eb52b18c2cc315c48737f7b0c6844f",
        "Science/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon.pptx": "cda721e5dd3c1799c89b8e00b79fe548759b144998b8f9ad2a8c244956ff0acf",
        "Science/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Pupil.docx": "8920525bc2020b7a8d6a2e3f935eb77415f8903f55f1a2f7636c49bd8fead9ee",
        "Science/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Pupil.pdf": "f11ce921052aa19e98af6741988dae84482cb5cc87caa15cb6d06740db7ba6a4",
        "Science/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Teacher.docx": "1d026a3de59ada343c814e3ed895368d5aa9292244ca569a66ba7a53f3cf126c",
        "Science/Teaching_Packs/GROW/lessons/W7B/GROW_Science_Autumn1_W7B_The_Moon_Teacher.pdf": "ff0c970316fa22f34c67fe22f8b0365b3bba423fef0aefb0e63cbc5a01070f19",
        "Science/Teaching_Packs/GROW/lessons/W7B/START_HERE.txt": "10d6ba34be76c3a7d82a346e83a65c86612ecd95505e63fc797a091bed945ee6",
        "Science/Teaching_Packs/index.html": "7cd0206831e3cb49209eb97471344a04220efb527914f27532deb20be93e8ce8",
        "Science/Teaching_Packs/packs.css": "70ca73b323e5cabf05b1f5f9f8107694cfcecf4ddf8043f342049ee4c797ce59",
        "tools/science_teaching_packs/BUILD_QA.json": "d5ee55a25c15ca86dbd6324b417c70d672e1d0c19a1fa6462f35cc620927a2ff",
        "tools/science_teaching_packs/BUILD_SOURCE_PROVENANCE.json": "a61bafa6e47477ba5f3d6428908aab7cdaca979a947ef71880160dfc0b8f09c6",
        "tools/science_teaching_packs/GROW_QA.json": "a8cdaa361414a3700c463ea40e0a159029db3fb803024e50b0eb39d082c6f364",
        "tools/science_teaching_packs/build_hub.py": "43459a1bff564fef2f66671ebcf0272a28301cb97de60f21a1c59385753be63e",
        "tools/science_teaching_packs/check_packs.py": "214e7fc9d67171e83d8f8605e44412e7f4b0ba071d568d3ce91804805959e56c",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/Humanities_SOW_Alignment.xlsx": "537350c7f0ba110ea90edf5039826c1a2858c04c54ec006c550ff143c09dec69",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/Humanities_Scheme_of_Work_2026-27.docx": "b078d01fb53a9f5d828b7f64d9ddb9d1a36daa681e8829d2a6d811abca664d11",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/Humanities_Scheme_of_Work_2026-27.html": "ac8f8d0a4188d147097a491b0db59efef16feb0c0f6c4fa8e13144bb8a53f69f",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/ORDER_HUM-D5.md": "688b3f5dcc60f6c0cd9c68e2cb2cb7c756ab834e9956c4b20b37982f749c88d4",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/RE_SOW_Alignment.xlsx": "b1ce56c551520fb360ea06e68c59c1642556337474526c38fb539a36296c2aa8",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/RE_Scheme_of_Work_Autumn_2026.docx": "3c2fe9ef4e4cd27361d76c4bb07234d4fe5eed8be40bcdbf1d1133b4632dd9a7",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/RE_Scheme_of_Work_Autumn_2026.html": "5a1b523738c7a9e21c7ab2a713970423b5bc4343595432ee315bb5999932e992",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Captioned_Model.mp4": "8fa5f6ba3f6b7210d48a37277125eba44ff69843e7f6875177e6bc28eb6747bd",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Editable_Pack.docx": "ba4218c0c930bdad13c95b796c7279bc26f713d78a412349e5d47f6724cd5ecb",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Editable_Slides.pptx": "cfda24ab774a2a5c2a742afdef594663ce9a854aa8a12694fd0ff6db6326b987",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Knowledge_Organiser.html": "3e66b84d17cb11b3d7c7b315ef734d88c4edb94a94125e2707a16addbb2dc3db",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Knowledge_Organiser.pdf": "868102f22dd543cce610053626095a530320d26b88ea5e116e151cb3cef5dc28",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Lesson.html": "a5aa6d120a0063d9c6b29ab56277873c72a362e69f1b7d4e754179fed9fb1007",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Pupil_Resources.pdf": "29a00cfb5f9bec7af9c6bc891cb7245207f3a35ab261e47005530c4094c4c2a8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W01/BUILD_A1_W01_Teacher_Notes.pdf": "37cf73d652b204e486350e7b65081175c8f463a04b4818640e7eb2e165442269",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Captioned_Model.mp4": "77173af6f427694cde81390ea21a8f1dba343a229c807a44009c87f93e5766b8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Editable_Pack.docx": "91b3470b41b0a61f596d8abcde9a16cb5c1ece605bbbc34da64992ccaef0965e",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Editable_Slides.pptx": "c6bd63b7fdbc4ce2f83cc6ba78cf7848eeec0de3909f72bdbf9d94594bcf182d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Knowledge_Organiser.html": "3b38e793985423f62c24448edee7ac73d6f0a98f14b874e28c1725abd64445c2",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Knowledge_Organiser.pdf": "a630484d37fc1d0c28e81f0c25868b52327db50c9c6de1e76debda7e5ca116a4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Lesson.html": "b470ee45affe0d1294b24a80e24c1e65487ea1dc0c6ad24e241668eebf42c915",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Pupil_Resources.pdf": "3b4fe4f602a55759285a98f6f1e2d45d2d46f67215504ceb55a923d3bcbcfb32",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W02/BUILD_A1_W02_Teacher_Notes.pdf": "a82945dc967a871fc564d1672060dd0f281de51c41187b81117370894f662909",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Captioned_Model.mp4": "6799b383452024ffcf72332567d694ba979b6423141ce4b822aa3c3ea8ee63b2",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Editable_Pack.docx": "c2417f48f62cc82e1a455133168f31b4d8534a9b4f6a5066248943775b0d2eb7",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Editable_Slides.pptx": "de5a8a7af83b5c3010f41aad4d8d6216c572541e21cab8ba335d410e34081210",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Knowledge_Organiser.html": "ecbdf5a09d9680fb4a038d1be68d65646113642c37df6a9159eff7ece3ba69d4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Knowledge_Organiser.pdf": "fb3a1002abc247a97de4ddebe31957e628da05dcacfc691a6c02b32e152c2ee3",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Lesson.html": "3d8abc157a0d8482270c6495750b3e92192008941afbd95cbee37b095f01c4ac",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Pupil_Resources.pdf": "c4e0b931a96350ea576d7558660347300103edd8f9470e8cbb8147abeb95bddd",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W03/BUILD_A1_W03_Teacher_Notes.pdf": "357c0c42f9bb9b1d7d3174b991adefea2bf7251e9d6c047e65fcead5e52a2e17",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Captioned_Model.mp4": "44ec3f4cf67a570d39f8dd10e0c221b60043c64e5ff9f8c703f73c899fa26c7f",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Editable_Pack.docx": "3cba20163d155b254250d5d04e561b7ab97ee1e0e62a7203ae03f74ec57fe07e",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Editable_Slides.pptx": "134e89022083818a9b01dcd3b117146b7c8fa955a4da049944abb00f9ab2a7c9",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Knowledge_Organiser.html": "66d4d4779b40c56879219034901ba86a72635c76beee76e4c207d3d57829cf2c",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Knowledge_Organiser.pdf": "482acde5fbfe07c7320ba7c797146a9e2df43835206a3109e52f1dc9d6f38aaa",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Lesson.html": "e4cab4290fafe1cf8ed76c62a5aa197aabbd307905f3ee09388774eb6d0c75b6",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Pupil_Resources.pdf": "06e25f3305baa497f8e390a15c8a774c9924ed6008692989c00f8c9f96d9a0c4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W04/BUILD_A1_W04_Teacher_Notes.pdf": "e4679530a054a5c59f2ab9e4c69a8a7f4ec2150e0f859f61522278dc6dde0dbf",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Captioned_Model.mp4": "6e49af80f4a65eb96e7d44b3124a8623399746d06de9e553ba1d6ac1820964bd",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Editable_Pack.docx": "6e5062cfe442d1c1393305aeb97ca8cd9997b5b32a94cf53957cbb46b5f5d5de",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Editable_Slides.pptx": "2d7a311e7f7cc48154932ab3abc264be9c85a883784be06144c4815fad4e4eb4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Knowledge_Organiser.html": "9302b4e790b814bfdb39beba6365b21fdbcb301326407c5233f90d0dfe792687",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Knowledge_Organiser.pdf": "711154c45a697db045eba0bdb1128dca890c14294c6fdde6f93c6ca2455a5781",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Lesson.html": "b383c1efb428fd153588e9851ea20640c44f22107691e74e37cffa2358e0c9e3",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Pupil_Resources.pdf": "e1714a396234df106f1d9a60863782eca89f778fbc9f5a3c2a3fadf82412525d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W05/BUILD_A1_W05_Teacher_Notes.pdf": "db8a527ee6733276cfa13be6707bdf7fd51683bbbb308316cc6a17bb85fc04f4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Captioned_Model.mp4": "729b94fed48c24c1d5782de86f959d2c36b8a242607a28f6527c3e422f6b633d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Editable_Pack.docx": "c3e667ea40e836ca2348167405f2cbe77573aa67c7ae278d1983284426451204",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Editable_Slides.pptx": "e3d9ced1eb206eaa6f4e4f3a140b94b892232398e6e36f8e8496a7a263da19c6",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Knowledge_Organiser.html": "5aa307e49336ebae2446d4090a28b87467f840aaa49bbe4c410dc280585cee1f",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Knowledge_Organiser.pdf": "5603b0397bad083b453bf7394d6684e27e7706f0591cd9fd0f1179252507456e",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Lesson.html": "def46c2eab70d8e875be6031d5f8078aef9a2492f338dd4ecaa5d3f11a6418a7",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Pupil_Resources.pdf": "35c2f9bedd818e4cf1c8b84d9e4f0c51951dacf2e7de3a9c4b4186d381cb2091",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W06/BUILD_A1_W06_Teacher_Notes.pdf": "2e331beb3ad1e67d69e308c2df71ddce6ff3894e34a3a4933b80bd9e6b4f6473",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Captioned_Model.mp4": "f061462dea7135392eb4391312f9714d66c9a3198cabb7e5c321d3363df45309",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Editable_Pack.docx": "55a0f12a9595c1cf0612533bda9290b9031121ee2b11742c6354612730f6320a",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Editable_Slides.pptx": "5f24d03d2b3e0823255d066a643852e009ca98fc4f34f984844c97a4df3ffe41",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Knowledge_Organiser.html": "b3b5d61e5bacbb1669a0d2c2c6956a04874f162bb4d8ab94a236dcbcc15c099b",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Knowledge_Organiser.pdf": "db0bec4a5997afe173847d60aa5daccfa4814b2b61a7a6cbb5709bd980fe11a6",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Lesson.html": "e9766b69562f291c2e7881e9f67201ec00a613be9895643468143a411437b18f",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Pupil_Resources.pdf": "7f429dd60fe3f4929451c3252ce4c4b93290269d3e65681297762c1e47b00fd6",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/BUILD/Autumn_1/W07/BUILD_A1_W07_Teacher_Notes.pdf": "1528c4085a6a61470847fc7a9727ac41a322c6ce9638c39ac18326b0748dbf89",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/READ_ME.txt": "c6db9ea733f5a67a6f32d702dc54963f97d3c8e430f310cdbacb47c5440d4e07",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/arrival-change.svg": "c98d1fa61e8163d08305382a36516b63b3f3de65440e068ca491f92d8a169cc8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/arrival-community.svg": "1de816a4040c040a8ec5c392b32035528497217d1a9f98e312930ea02a765d68",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/arrival-diversity.svg": "8c3b9c5a0600994a9352b2181952d9ab92c75b9e398e6845a97e1944cf18043a",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/arrival-fairness.svg": "529e890159203a9483e9c044181e331554e27a9a65106cb78c3e644bbb75a8c4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/arrival-festival.svg": "1e1bb8c407d767b99f02cfb4e3cba2577938252c83e649639590d95875c01fca",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/arrival-peace.svg": "792b8cd954eb3b23bae480d4db84519e5c5a2b506442c3772cb90416ad4a8ae7",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/grid.svg": "be3436cb4c1b0fa7993e214c47407186a74ed353c4fe727069afaeee572d9bb8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/local.svg": "e666bc5070d66bbb2b564685a768421508764e67b28dcce67b6be40cf0ba5e2e",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/objects.svg": "88aca060c6685e20fd47a6740f32c3012a15c48b12dc6bad91867ae040267eae",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/phones.svg": "ff17e352efd169723a534fe0a4c6846d716604929b506bb8afd0ffda0724928a",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/world-climate.svg": "c7eb4516343528f9851ab39a89c04abf8b26b260b85706314c567895ce2a7ad3",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/Editable_Visuals/world.svg": "26fc4e5b254e2611c6de7db61635e5da69beb764ff861655a1b7a682774079dc",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Captioned_Model.mp4": "27e372fb76c393618ad50c7646297a5de2634cf380b46008aaee24e1e7329b5c",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Editable_Pack.docx": "5ec25185c0ee34a51fed7578a22710382f729df4252044b243742d30b420f5a8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Editable_Slides.pptx": "d21c1563074ca9e572bc8cdf9ca2b6605a5bcfefbaf3365ecff395c37287ef41",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Knowledge_Organiser.html": "40439b73feafd73e9fdb302f8c387a37943e6309a9061ac91a0e2819e0602668",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Knowledge_Organiser.pdf": "1eed83e326a7e7ed83b9c1cbe4c4a937cef65184d5a23d95112f82e9ad1f0707",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Lesson.html": "0592123d64d2f32b456ac79b59c33cece51a3a246cd3396f6f28cf43e796f966",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Pupil_Resources.pdf": "0b022e28a1ba0ca0300d3e49200efe20f795d3e0deea37e1719d46329df27b38",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W01/GROW_A1_W01_Teacher_Notes.pdf": "b56e65d0d91b9f5a71e6ee4437ba9a55648e6de5207ab0cab245080c6b6fa1c8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Captioned_Model.mp4": "4e5fe08cdb62a84699773e85af089dbf0a82f20f09a695f3dba0dfc9e8f6d686",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Editable_Pack.docx": "3f7bd38532af9728ef28cbd469dbb654490e19cfcd797557665a8557f915da7c",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Editable_Slides.pptx": "718df0564cc04f829be3cf940f7c594d8e7653fde687acf6f4ad6649840a35b4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Knowledge_Organiser.html": "9a480ac49e3b70537513f25994506bd53109ffa3a1af2ef436d33f0634ce46e4",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Knowledge_Organiser.pdf": "d12ec8182576ba80e6e8babf1d8f9294fcfad890030a1180bd585d13f9f034a7",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Lesson.html": "0e9115cfd1c97eabdd6719a2d6ca212eb9f523ca735078302d2e25673d99c0bf",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Pupil_Resources.pdf": "2b8d25a9b90bc688a30cee4a436fae9da5acadc6ea5be0e08208c17c61a34233",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W02/GROW_A1_W02_Teacher_Notes.pdf": "bc604fa8fdf64afc8d5171b5f6399052448ee019854c9a9c3f31499c09f82190",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Captioned_Model.mp4": "a01cec3a4122abf6d5a1538c4a045c9edd705cc71fdc61792136d1a0cb7eb9cc",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Editable_Pack.docx": "9698bd7c5259b45f52b91b0da0201ec42f68cdeef088e95ecd36d3df024709b5",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Editable_Slides.pptx": "1004155fc1fe26181287f11b2d7256e54cf8c9146a9194dfe167d374998f980a",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Knowledge_Organiser.html": "f0562ccdc634da0a73a0103d80cef7980f68cd2e03443630f23f2717e1a200ec",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Knowledge_Organiser.pdf": "5bea657e4fc355189eab0117af54fa94667cf1fb285c902719ece4dfbb136c32",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Lesson.html": "0e0e2826667768d97a0e341f5fcf67be25ebd930a1afc9b013940ad09740d35a",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Pupil_Resources.pdf": "74b89a85ae290c7a92aaa294b63cc11d95ad910104736514f0b5e1d0ed06e478",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W03/GROW_A1_W03_Teacher_Notes.pdf": "ca45b2898bbdbf042eb133888c55024f773f45d6ab8eac0776e3b9fd7f811853",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Captioned_Model.mp4": "f8508413835f4f6b7da9560df5a34be4576fd28103321fa87dde8e02548f24b8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Editable_Pack.docx": "8e59d4a336e345822969c7d278507d0b87d82258f19a2f0e8d0cb69b245d2cc9",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Editable_Slides.pptx": "f91ce4ef835e9d92a9568a4f461c4bf0488eb79c9eedd01530da603c731d3f9d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Knowledge_Organiser.html": "5e07a502976e39e47f86b48d32a83c578670c2da5f4096571d1931f97f03fd08",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Knowledge_Organiser.pdf": "756a7d988c9b4557214e294ebfe609350faa3574b608b8e1acf54406a89cce60",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Lesson.html": "827586049083e26f9cf0766a714503f9811328364755c71ff6095a2b56160889",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Pupil_Resources.pdf": "dc0063c6a349deb1e5fdf7334212d3fbbc7599947f5c6df7cc5b5820c1f3aaf1",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W04/GROW_A1_W04_Teacher_Notes.pdf": "484edbedd4f36b652e9edbb678392653226c76dcf7ad33d8d6e2cb3fa782c617",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Captioned_Model.mp4": "d7901902a1df8f0427406ef698a7fc00080139c11f866935cba3b323d8e2f4e7",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Editable_Pack.docx": "43deca2b5d9cb14440ef2766e061f3e290ffc73771ba31e551afc5305a30f71f",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Editable_Slides.pptx": "563437d8138ef940fd094ea27502eab86ec37223e5bfa418b79c806b1e6ac4b8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Knowledge_Organiser.html": "0048c8d0598c8eacdab502d66b52aea2d2e8ba8b9608ad020cb88e3c8047bea3",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Knowledge_Organiser.pdf": "54c070b18901980996718efa64cf0a26a638cf68bc9008d58bedf76d805b4fe3",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Lesson.html": "5afbf764a5ed15a8d4676cfc5c6b44738ccf1faf04f2d070f46e327f59eb1df9",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Pupil_Resources.pdf": "1629c9c31a3fdc5fb126a6f5b2d6a0a6503a358ae73ac5a426e978eb048eb0aa",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W05/GROW_A1_W05_Teacher_Notes.pdf": "ad9fc3e249146af8f50a2dd68680aa097b7e50be02f5aa62d036e01e467dd6dd",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Captioned_Model.mp4": "48d1104447ee11372b61673d71ba3057d4495c125c0f9b54411f0e729fcec5f2",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Editable_Pack.docx": "21eee128ab8ecc639e32f0d068c1cd5ebf532d11c80ed0a10aa1414e0cf76bbe",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Editable_Slides.pptx": "eada084af4c4f1c5e337f1121487d10165a13802a2f4465f5d4c06978f722d92",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Knowledge_Organiser.html": "3ca5600ac5639520240bb60edc07715d7157b132056173dc971d829cc629d52b",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Knowledge_Organiser.pdf": "bed02b4dc5cc31134965d6ae14f33463ce27f98820789306f266333b726cf5d8",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Lesson.html": "5a14e462a87c9a741f14f709efdf6d0bb4974358e5b86812883a91e0387c8e39",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Pupil_Resources.pdf": "05a3df175825afcbee8c0d2b0b930f73202ed48cfa85e2cf446926879e890231",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W06/GROW_A1_W06_Teacher_Notes.pdf": "6cd6af07cc07ec35202709612498fd108441519f91fac5459294e7468c3dbfec",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Captioned_Model.mp4": "1bca4e415328a017f3494bf4d4b7db779544b01173cc07e07562bd5d19b34464",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Editable_Pack.docx": "55518db545be873b113a766f5f2184b3d75e8f092e2533d7c6e4c980c3c26965",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Editable_Slides.pptx": "d852d22e6cc2788dca4d284b4bd31122cb60f1d6eccb382014746da0fb1add60",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Knowledge_Organiser.html": "decc5a8f6a0710d77bf59a9f545e207a29caa1f87442af93b6299656c2d6787d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Knowledge_Organiser.pdf": "a15d9bc8ef7b7b8e3c144df48337926e3d3965b4a15d70d0055ef15777d41a17",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Lesson.html": "f168ce4cd63b189ff6ba819cbaf744975670ae1a54230bb6b147f87b8325a7bc",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Pupil_Resources.pdf": "95731f0c7778302038af6829e4f4f843fa33d9093fbd78cc09b1a24b6e316e7d",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/GROW/Autumn_1/W07/GROW_A1_W07_Teacher_Notes.pdf": "c0c7129f507d9ae462fdde108823ade704edb5d435c4c1919d408843647d1380",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/MANIFEST.json": "6cd175cc1cc25fcc69dc579e7b1750545d7fcb1cac849196ca72134b8708b766",
        "Humanities/Teaching_Packs/HUM_Autumn_1_BUILD_GROW_Fallback/READ_ME_FALLBACK.txt": "be8efb425b2248d5b755d816383d8854e0fed26d99b108bbf898b5f68d96695b",
        "Humanities/Teaching_Packs/HUM_Autumn_1_LAUNCH_Reviewed/SHA256SUMS.txt": "480587877c978b6792d8107131157de7264cfc8b38743ae3eba36abf36cc66c7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/SHA256SUMS.txt": "e02a5e9c69a4f89c89db97f9cfc021f142ca391d7ea3ed063c597d9090c934db",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/SHA256SUMS.txt": "3585f3c2b25a067ec757cdcc291a8c62971f5d6c3173f2dfb944de4525dd370c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/SHA256SUMS.txt": "7e3db22481967e3bf3f28f72e33e57abc67f11e3777e60f447151e3bf9f36ee0",
        "Humanities/Teaching_Packs/HUM_Spring_1_BUILD_GROW_Reviewed/SHA256SUMS.txt": "ea6408bea002de712ce88b86ef3a9bf8c10ba9883ca07f9672dd1cd7ae26c09b",
        "Humanities/Teaching_Packs/HUM_Spring_1_LAUNCH_Reviewed/SHA256SUMS.txt": "5aeb09e7bb0e455267426625517d0deaac0fc2f029de50537327acfced32d58d",
        "Humanities/Teaching_Packs/HUM_Spring_2_BUILD_GROW_Reviewed/SHA256SUMS.txt": "423cf78757820f83ea54bdb970d528649179a719d9fd75a3b059075dbaaeade0",
        "Humanities/Teaching_Packs/HUM_Spring_2_LAUNCH_Reviewed/SHA256SUMS.txt": "50cb5d58839fc4942693a01850a137497a4361bb467a4ee3b658d86793ac74ca",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/SHA256SUMS.txt": "ccc10683c49aaaf9fc3e57b34f6e1a90d77ef3eeb72c9bd716fcc40a8cf00cd9",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/SHA256SUMS.txt": "871fa30a1d1355372c39218f3794a082a8823a5003fcde28c2683ccf5ce3c343",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/SHA256SUMS.txt": "1aef26713d7bb00458ed20e3b76c5ccecdf3ba703786cfef073b7893c3a1d913",
        ".github/workflows/cross-estate-on-content.yml": "e323c85b033b82455fa950e2be395868c279a929ccb6b94981fcb8f3258ae72c",
        "tools/humanities_resources/PUBLIC_LABEL_CHANGES.json": "1054940b3c20ab2c084965a4ae11c8827867267e119df6d8e65f717d7e22adf5",
        "Humanities/David_Cover_Autumn1_W3-W7/BH_W3.html": "3cb06cdadc3af0b852e54192a10203295be12c6139601e98e86c9496478a79f0",
        "Humanities/David_Cover_Autumn1_W3-W7/BH_W4.html": "ad5f0adbe53b57189e3c9958ec5e79d3f9b91018e6fc85001140141284e5c387",
        "Humanities/David_Cover_Autumn1_W3-W7/BH_W5.html": "c67cf1fbb4e37c3f6bd9f7e6f69e56eeff26150f2afa8447d461a5684dda2665",
        "Humanities/David_Cover_Autumn1_W3-W7/BH_W6.html": "6e13cc25bcf3918309406ec1269b0765117181e90007306d76e115d585319717",
        "Humanities/David_Cover_Autumn1_W3-W7/BH_W7.html": "b8d346263c2a4e3fad004273c2eb37ae02996ae6566eb1d02605aad203aa07d5",
        "Humanities/David_Cover_Autumn1_W3-W7/BR_W3.html": "68433d21e8b4c04a9c38b34b89afd6162fefcbae3b90ced8779b01341f5b7948",
        "Humanities/David_Cover_Autumn1_W3-W7/BR_W4.html": "48856c5185b28621ca9c7a3c4d668fd0402d69039351516753dae80c3b393e65",
        "Humanities/David_Cover_Autumn1_W3-W7/BR_W5.html": "7311ca67b4a83a5356149ed7b7e96c19ef0742c9b6e1fd736a4eefbe97f33796",
        "Humanities/David_Cover_Autumn1_W3-W7/BR_W6.html": "4547ff74bdc25dd5f3de163a57fabf0cdb062ab922b5be13e6a76e4e31f6ac7f",
        "Humanities/David_Cover_Autumn1_W3-W7/BR_W7.html": "7575fb9d4d8e28ca487c89a91dd70b556dff94e67a8723b37b63d06d363c6537",
        "Humanities/David_Cover_Autumn1_W3-W7/GH_W3.html": "8a28b949bd4a6c4e2a7965e5edc07bc20454df22ac0ad4fa6d94950119286bc7",
        "Humanities/David_Cover_Autumn1_W3-W7/GH_W4.html": "f84c91ca65ca730620172ca70b551061bbe568017d6815b2b12df9be0e4dad55",
        "Humanities/David_Cover_Autumn1_W3-W7/GH_W5.html": "d9a0680fa3928b1d7d23333c001bc7a3d70d46bea9612ade3b9588b97ba4bed5",
        "Humanities/David_Cover_Autumn1_W3-W7/GH_W6.html": "5119f8b0b33aeb3d225be4af3c883a88476d62448d2ee5ad5cfa161b231f96d7",
        "Humanities/David_Cover_Autumn1_W3-W7/GH_W7.html": "2839c19f411983273d84b098a6d1db10f30bdd7ac975b83ded2061512157d347",
        "Humanities/David_Cover_Autumn1_W3-W7/GR_W3.html": "df6893b26d5dad94d001e20bd4cd2bddd0dc8861b879fa16fcdf9546f094d1d7",
        "Humanities/David_Cover_Autumn1_W3-W7/GR_W4.html": "9c1bd091b3d792bb8f765c8ef8ab781c46952423d85d2dc7f428d7d66afc7476",
        "Humanities/David_Cover_Autumn1_W3-W7/GR_W5.html": "b750830cc0cb162ab721d4357a882351b7c82c36ba5a5bbdb09da87004cbb19d",
        "Humanities/David_Cover_Autumn1_W3-W7/GR_W6.html": "609c398050b997a8e8f84dcd38e2ae3a4e8e46f444b927f78a7d55de314d5686",
        "Humanities/David_Cover_Autumn1_W3-W7/GR_W7.html": "6c196a0bd2db17728722d456a1af310f17e8220dcd6578bd9b35643aea6fb3f3",
        "Humanities/David_Cover_Autumn1_W3-W7/LH_W3.html": "95856d0bd41abe02aca8a405718ca4b413e7c797673ff5beffeca13b87abe691",
        "Humanities/David_Cover_Autumn1_W3-W7/LH_W4.html": "51ac458f002341ba2610fd5dbdfb3beaec961606c57f953c48b7469baf8f6d73",
        "Humanities/David_Cover_Autumn1_W3-W7/LH_W5.html": "63ed872c7b5534d8d1c4ffde723fdb7742789ae7bef705b2b9cfd3eb2a34993d",
        "Humanities/David_Cover_Autumn1_W3-W7/LH_W6.html": "6ea47b86c65a116d95ce2376b16dfd9fe773c6290fcded2efa072db19be0dd22",
        "Humanities/David_Cover_Autumn1_W3-W7/LH_W7.html": "33ac63f9fbcf9c36d67658e87614f6e1e904de45aa3dc5128ab7fed94579f803",
        "Science/Teaching_Packs/BUILD/SOURCE_MAPPING.json": "7e30e48fc01940656077ed1932c3132c425ddca908c73db6f0b409b5e8664988",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_DOCX_Collection.zip": "2482706e4f9c7e192287acfd02e7c09381597a1a9fc772c9d39fe630eba5a3aa",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_PDF_Collection.zip": "b3116412bb38368b96c0236e2b41902deb76e96461f1ca1c3fb134d878f842f0",
        "Science/Teaching_Packs/GROW/downloads/GROW_Science_Autumn1_W3-W7_PPTX_Collection.zip": "592f59c2ccae4f9531af5296eb30064c8fee92c44ba2b896db8038cf2a93dce8",
        "Science/Teaching_Packs/LAUNCH/DOWNLOAD_INDEX.json": "e2907a8f829cde9c8ab4b8f012cd49ce89daac86ee09b2b3554da07bb0aa4d89",
        "Science/Teaching_Packs/LAUNCH/Pupil_Worksheets.pdf": "40b4561e417afebf2cae6a5eae1ade45859a9dd462bf69e8dd4135c836d3f7bc",
        "Science/Teaching_Packs/LAUNCH/SOURCE_MANIFEST.json": "3bbd898b418638248906d177138ec8bf0232753814f07a837ee50b6b08f3b9a5",
        "Science/Teaching_Packs/LAUNCH/START_HERE.txt": "2b7b55ab005abea12229d54ef4f8f5389cd6c0714078284537844e62b69ac3e0",
        "Science/Teaching_Packs/LAUNCH/Teacher_Guide_And_Answers.docx": "407a1c8c72112dded2dc9c89d3a73c6b5834cabcb743d8bd6f436c412ef1656e",
        "Science/Teaching_Packs/LAUNCH/Teacher_Guide_And_Answers.pdf": "f359887eabd99b868f1741b65ddc0a16b0eb2d5909d127f166926aa877657fb2",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_Microscopy.pdf": "411edd8b048c842593c1121f8bc834e5317d37a7a14e63750eba2b9b37429f88",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_Microscopy.pptx": "a68b061201d1fe625fdc94bfee4fa2fdd0cc223557c24a959999cac21c195d50",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_Worksheet.docx": "578c8ea466beaef599c1d7f903a47356548b775352993f87ac73d714a97d8b86",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_Worksheet.pdf": "5a19b3f2ca31014d262fed5fa07132b1fb13b28faa10c64b896eaee3f12a6450",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_depth.pdf": "005e8b95cb519d392b039cfd83aad453f4658b6e8e8aa64033a8b3bf8d92f301",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_standard.pdf": "82063ab1b999b329d78a05d9cb26080946bbe2a7dcdb8e5173e6ccc79a9f8496",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L1_supported.pdf": "cc8711966739a08fcffd0a83101a6447b3df3b0f467e97a758716ea20c82b2c1",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_Magnification.pdf": "26f6f2663f3a38537d233a9c94861408c0a23ab01770ec64be8cb0c0b8c811ff",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_Magnification.pptx": "1fb4bd94df2a29ab0af72db475b8929bdb22aaa9cce4ee4a5bba89175f897286",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_Worksheet.docx": "910725485910dc58e2b030f28b0610e31a7c4b2891422ae67816799ca544e710",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_Worksheet.pdf": "1f619b4d341c9a2a339fbace64d0ff0ad7511bc3fd29ef07efc9f56f58eb6b3e",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_depth.pdf": "cb100881ed59102fccd6ffefb85fbfbb984d20658249cffde5f3f0ad1bb832aa",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_standard.pdf": "9ce05f7ee4e095294ea461fdd5f838ef4ef9f0783842898d36468e2f7aada8ac",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L2_supported.pdf": "7b56ab3c793ac029fd751fd279e542e74fa42f9a01bf99fac3708177b38559ed",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_Scale_Bars.pdf": "9acb60d205a4e7a4c83a146b7c2a4547d540e9eb5dc6cbccca7e70e0e55f830a",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_Scale_Bars.pptx": "ebf8d69debb79a17020e22a0b234ad5300319bd9d149e64f2996526db507a441",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_Worksheet.docx": "77497a489ddc7c0ff48ac4a208832e28b6022f20de6e1ae225d59b27c6d78d92",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_Worksheet.pdf": "ffec01cd95a2ef8d9e1aa87d8b5e07f99d938b5bc7a6858c357388374f3bac8e",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_depth.pdf": "53184ecb48997a1e102ad0903760a103522c6adaeb52b1c112759b9c2209e435",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_standard.pdf": "ac051b2f92d89fdf77253f8edf3c4429fa89d398d40d0ee2606cf0f02d22b260",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3L3_supported.pdf": "e0e52afc7e76fabaf33ef82f3704f1d0eec08bd0fb4097c72bce38468f4aaed0",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3_Weekly_Plan.docx": "0ff2731c3812884f5662f488a0eedd24f4e9689a9a58800125416d0666c66ecb",
        "Science/Teaching_Packs/LAUNCH/Week_3/W3_Weekly_Plan.pdf": "b2827f23371b7874d89245a7dd75e410cb7e9f45beb43ee564988a7d9a000de5",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_Diffusion.pdf": "0641dbde7d35b8d98332c864eb419b7f0d18610b79e96c2439c5cd741803f6ec",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_Diffusion.pptx": "a61a92cb908959617c5e62440bdf18c8fce41a5a5c91eb348086d4fc687b32fe",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_Worksheet.docx": "587d0c554d8f496b13bfa4f35cd91e4fc6e5e9618059b73cf2a5a9131e2ada75",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_Worksheet.pdf": "9ce702ccc29bfb3eecf02e6f73df2de5cb96a6e695962e79fb49c8ea90ce414e",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_depth.pdf": "e4414be692a08830b502d4565df44f3e92a3f01f0acfa014eb04d4da3638b7d7",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_standard.pdf": "1559958acc64bc63d89be2aad107ecbfcd9790ac2197999e8f7afa841ca18938",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L1_supported.pdf": "24b69c4457b50caa801d8f4ab70a2a7ab09a94e6332d9f933fb26b9a0b39452d",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_Gas_Exchange.pdf": "b3652f52606f1fc860735976363e37b5224327692d32a600e7acdc56ab62359a",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_Gas_Exchange.pptx": "6cb8a1c32ebbe00111b4ba7187f992a89d367864d5f80bd518525016056cb66a",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_Worksheet.docx": "ce22594dac00e13df8b079f3c16f0abfe44f2c821d85162206eddcb454291082",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_Worksheet.pdf": "52574a3978cdc979e213f4f6f895fe8b375514b306de19844486297190b972cd",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_depth.pdf": "e47ff950834a3e008590d3e3aacd023035099c9a690478937ee898f27230ceed",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_standard.pdf": "00a824d2d52417a7fc1add1376937a9a55a6cae32c160f00491997044e41649c",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L2_supported.pdf": "bb56237271dcaf6c0ea670f2f1d35b31299d4b07afbd02b18e21b2e3dc4513e7",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_Diffusion_Evidence.pdf": "61ae806cd59bfd578a9a231bf59bb85082718dc8b509b0e55eecc95a5679478c",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_Diffusion_Evidence.pptx": "4eee78c7dc875371151c4a2309b1539c894a04e63d8b635676c825ca401f8834",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_Worksheet.docx": "f98364c37342b2c7e1d8852b3e9480c56608087c553509d190c246264e3bd55c",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_Worksheet.pdf": "7c788728303715a6d3801eea275715dc127bbbda1060fdb5a3059ec0fa3f6ef1",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_depth.pdf": "8110273a50fa1e3ee30af9634015dd60910d01c274f2747dad22de7e1c43571f",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_standard.pdf": "1bbcbea02fd6a38295d7cbeb4e750cf90794a1376ef38a0d8f46e64419f7facd",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4L3_supported.pdf": "a1eb3480ff04ec86f2e2bba418f200fd29c831f419efb28ce8caa1fa0e39b8ca",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4_Weekly_Plan.docx": "8908c707b8a70a5ec32231750fd2997c72803de0be7c140266753597cce870ee",
        "Science/Teaching_Packs/LAUNCH/Week_4/W4_Weekly_Plan.pdf": "b51e3e4d7842e2eb79d1d68746bdae2815890a729c2392f746425eb7fbc8d4a1",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_Osmosis.pdf": "c480c3dded76690daf3a246be25c46638de5591b2c376e42fb19d9f4c7016558",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_Osmosis.pptx": "710ae7a5ab374e599d710279e21984619f6f2acd958ff06c4365080fa8467f32",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_Worksheet.docx": "9a46502209db857d1ef7cb407c65e5cb0fde6877ce225f55bb88b3dbe4bdb81b",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_Worksheet.pdf": "533ffbba83bc6a18cb44a9af3723e727af41c73b0dc7becfd8a4684ecec2f769",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_depth.pdf": "153c07f6d4174b9ced5537a34cc39e0129dc9fca4ce86f30710d5fe0e61abebc",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_standard.pdf": "c450cb8ca0c00a54c088790805d1629f6225fafa7f20f2ed85e231980e12b23a",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L1_supported.pdf": "ddbdaab0499efb7e0407d7085c8768c032d130b0e0945efc28f423113f955773",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_Osmosis_Investigation.pdf": "45f9117690a893731d768d95778a635d7c6b6d324b803c383e4020dcf14f879a",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_Osmosis_Investigation.pptx": "dfb1a60077b8bc34cc5737c1f4551a18f20b65d3b42acd3161abdac911dc4735",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_Worksheet.docx": "78f94b01728e94f2edc93bf884018c84a411e71f9db8b7035d02159287895a2e",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_Worksheet.pdf": "e96884229cdc695046cb0fe6960404e4407da72d0d489cd3fe43e3613e59af53",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_depth.pdf": "a9127c50279abc4874aefdbd6e78d02da91aa0faf5d861820173558a263505f9",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_standard.pdf": "6c80296e85da6fe98231d1ed4cdaa56191c6ec1962ccf247badc85186591df01",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L2_supported.pdf": "bd98b8c86d0dbd4bf75e2c19c20413250bbac9f976bdaa42698b69cab230134a",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_Osmosis_Data.pdf": "5ff00817f0e9629d974c4a260116044f986978960a46554bb6d32f3798dfd980",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_Osmosis_Data.pptx": "59bfe0fa66da6413fad107598fd5eab556324da67068d343d7024ed9fd96c4d6",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_Worksheet.docx": "a88ec8ac1d32332cca655187aa319c387a384da783f4f8a5328775bad6ab1b48",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_Worksheet.pdf": "2f45e3db7c25cb4be482c47a3ea674baab297ab8fac06530152dc710050eb6a8",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_depth.pdf": "11d54d8a1c7b08056ee672e0c393b4c423d9e487cc473ef5b83888fe54a0e1b7",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_standard.pdf": "29abc6f371bb8ea82846b3a8a8e8eb3f5b4d2cd641eacf4c91c3cfc298486857",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5L3_supported.pdf": "984c6ecf259beafe41c77e60af240495f6f32715dd1c2c7ece6121888bfa0e10",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5_Weekly_Plan.docx": "dc6175157f80ed060f6dc829204758b6ca079fc3a7d0156648a495a31bf77a11",
        "Science/Teaching_Packs/LAUNCH/Week_5/W5_Weekly_Plan.pdf": "9d9f05619d7368418e717af6dda8158786f025fa217639090886a2f0ced4126b",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_Active_Transport.pdf": "a877671f4bce8b6ec20dbdffc31005d7a8913420a21e4a50521bf46095c56ab0",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_Active_Transport.pptx": "6fc2f87c44239ffb9b6e84a692c27f463bee58ef6e88eba54dfd19009b6646f3",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_Worksheet.docx": "a0db709628b013be34cb431640a4d6353c08899275e69c7048ee9eb5906556e1",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_Worksheet.pdf": "dbb36ee694301b2454c5d25784899e39f4c8645bb24a4323611c118da2ff3091",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_depth.pdf": "0d645d463c3440e8f162066073976948d17113c3c04b9a1389cc9936e352e434",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_standard.pdf": "3cec9853fcbe51f60e2fc49d51ef01196b9dbc7255813485666bedd8c64b3730",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L1_supported.pdf": "e31ae68717e48acb5d1a49c466a319aa4c4d9e896ea2ada6072f94123d68ba19",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_Root_Hairs_And_Gut.pdf": "8e48afe3ccca498f510b45c3a0cbecb63c4ba943a425294a00610b8f0bc82a49",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_Root_Hairs_And_Gut.pptx": "7127955eb2c1e2f38541286be5d238ad9c26ba8c35dbd1cc3c3ee27aecc71592",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_Worksheet.docx": "ca371afe8188dea2a79b4f8d01dc6d443382395bb0f753bc52ea0f34753a4f85",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_Worksheet.pdf": "e2ae0ea71b98613bfa02e4ebb00931c3cf00ebd0ab1533e9dd9c0be49a254a4a",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_depth.pdf": "46dc11aeeed02b38f81b2deee28c89adf809c261a0828d65d0772ff80f3ec0d9",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_standard.pdf": "4b18f94880cd466e663925c6b601697d3d47c68f63b21aeb98efe5581a9c822d",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L2_supported.pdf": "2e454bb29b5debe12fa5dfc89951bf473822ae664cf1f96e1f7706e78832fde6",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_Compare_Transport.pdf": "7ab6dcc9e5b8b8174eb9c9fc48a384e1d6d518b81562f0fde795976b998b02eb",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_Compare_Transport.pptx": "5c36b70c325b6102025f253d2664d1589ce5820758006dbb50e634bd8a1bcdae",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_Worksheet.docx": "ada63ec53ae3feada8f75a624f3a1e4c7b20dc22d02866c53fedaa6033cedbf1",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_Worksheet.pdf": "67908331e90ad45815a5dfab1391fd1f58e1b21636bf9ee50c85a4571b0f20d4",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_depth.pdf": "dea895c6bad53c4060b1bc15184a21631285451d8a820a0a7ee4903a13b386a3",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_standard.pdf": "28b4f3cab0a6dbfce5d2e72c7e63be6c983a4a65ec5b8b4b8e93221174e2ff57",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6L3_supported.pdf": "71e97b4a48ae5192af0075a4b0be4fad52d31f1432e78a5c559527179be25b29",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6_Weekly_Plan.docx": "b6b26aafedca7a02a28881ab8c00e9a07a333e5cec4c7aa21a648ab6545e098a",
        "Science/Teaching_Packs/LAUNCH/Week_6/W6_Weekly_Plan.pdf": "0d00dc615fd0dd0de39caaf8b3075a720662d2ea565850fef0ad56fa2ae6f707",
        "Science/Teaching_Packs/LAUNCH/Week_7/LAUNCH_Science_Assessment.docx": "504dbb695495660c2141b79f01e7cc71457a9d4659595ff55c8b610cbc7c110e",
        "Science/Teaching_Packs/LAUNCH/Week_7/LAUNCH_Science_Assessment.pdf": "eea71d1a3b9a105542fa566a1c39adb0cdba3fd138d84b64ff25985275838af9",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_Review.pdf": "e2899621b752d69f1cf73da996cf698e7875b041da0bc1663686740578c0ba1c",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_Review.pptx": "a820db909139c864f44133b2f461acc0fc49b3f3eb77f3c59b5c3f579e73dcb8",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_Worksheet.docx": "25d14dff4c4f6e4ab56609b9af1e67597270a970e85151db273ffe98f2631aea",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_Worksheet.pdf": "7b307bef4e082bfdf7225530b121095810480ce52761068a21843cc7c412c096",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_depth.pdf": "7427ebdc876c5bf9ba137ee6b2b30f44c6e3cb791e9c70900bae83ceb980c0c1",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_standard.pdf": "f6cbc794175f8c62cfa3098b1afa6374fde6d94997dbc416df5a4dd5dceb7008",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L1_supported.pdf": "633dbf208b8c32c18e5985bd5e09c8e29234ce1533c584fe0a0b073d8fa7513c",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_Command_Words.pdf": "61617770ba69ea6d85fe37533191878c61d54aeb526f8e9053daebac0c415531",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_Command_Words.pptx": "305f7a0940b08a66a5963acc5efb07827c256552bdaa6158f0c0ce966b88e250",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_Worksheet.docx": "7c25d67a7c637c567f447aa655fd272ff6f1efe7dcdcd54c7dc40c77e1e1f887",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_Worksheet.pdf": "2742657e67b01f9fda32b27ff1704239f0e45fc5f4d445561dca3f041d37d2b0",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_depth.pdf": "59eca019f32fd0dc59f1cd9b153a4a4d337d419bf970194217edb58bd5ad754f",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_standard.pdf": "895a72d288f1041ea15c9ee7d91713cae7aa8dcdb7362c4ef6f7467964afccc7",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L2_supported.pdf": "be095c3778f0bde0f3f36a41cef54cdd7b3a720c44ba1eca17ace9007c297723",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_Assessment_And_Response.pdf": "d01342b1d3f5a7950c5459591199fce745083f4cdaf99e4f292379e9a1cf03b9",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_Assessment_And_Response.pptx": "6097b44ad6a0321335fac1bb72c3de07f0ada203431c36cf40156097fd7297cb",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_Worksheet.docx": "9d7b617f9ab63a6f7dbdf05ae27e7f089a907f88d41889fcf441140af86fb101",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_Worksheet.pdf": "0343a92d5d13872a021e14e334086f513e9f645ca14a9059e381d13e50b92acc",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_depth.pdf": "177602c03c56f61bbd03cd4b537d21c4c22dce607e85c322954b675490195c42",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_standard.pdf": "1499987c069be0d685c72ddfe9e3b5e021df258002a52244a470e4c3e7dc7dd9",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7L3_supported.pdf": "c5ee897b1129bb86eb0813c08af7df11bf4f42e4b70f5b79c7ccc1402ee0f770",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7_Weekly_Plan.docx": "499928095b9cd9aaba5f0b09a40d101ea40f98d41b574ca0f1fc410a50688605",
        "Science/Teaching_Packs/LAUNCH/Week_7/W7_Weekly_Plan.pdf": "4ec297f090a8d5983b03a7ca23b866ef0e166c0f603f0963fa7c7dab075dbc35",
        "Science/Teaching_Packs/LAUNCH/Weekly_Plans.pdf": "5bfbdf746dd1b83c93ca12c9c5f10f5f8051be30ed4efc1344caa49cac578dc9",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_Complete_Pack.zip": "2c4e45a5cb2dfeddab2eab0894250a9bb23e11f8558a7a1b41181ab861de6829",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3L1_Lesson_Pack.zip": "2635ad9fcb128c7e100f3f0270c72394809dc2a4e6d5a1a484ef09b7fd50be4f",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3L2_Lesson_Pack.zip": "51b8d2a4e8e79ffc71eea2aa0073ee7c7d8ed738a88963f6da8730e8b01b2efa",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3L3_Lesson_Pack.zip": "ff7a9c6d7175db2be41b96bb5df27ec9dfce144ea7fda1f9e2eb998bec89b997",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3_Teaching_Pack.zip": "33d73973583e1a66e28610c7081801a697f562889d91e330290105de06d97df7",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4L1_Lesson_Pack.zip": "681efca90ccd4fe7143578e9771c905f0f90cf2e7688c6ac5ff0ad94014e24bf",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4L2_Lesson_Pack.zip": "66f6e1a5c82175bcbeb6c103dda4b166067ddedefe75a48c1c9e729ee04244f2",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4L3_Lesson_Pack.zip": "af858882f4eb585529e7a96934c5d874c52d6564e3cf6c6ca3023d6c484abf53",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W4_Teaching_Pack.zip": "f83dfca777feae79489aeb521135864304f62d1ff38bc4978659af316e7d00c5",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5L1_Lesson_Pack.zip": "f9d699fed947c921f5fe17cf5a858b7b7de3436ef6f7ec3a88fcd0b0b8b3569f",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5L2_Lesson_Pack.zip": "88f02bb5be1377604ac31ca5249925790f74fa255ac4c3ccc9cdfd76f945fd12",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5L3_Lesson_Pack.zip": "1a9dcea48a1aac5e576148f0d908e2f2a5823f1e1747860019a0c8f20750f3a5",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W5_Teaching_Pack.zip": "339d9b737ef1b0023fe12803e83bd4d41c196afccc0c52344f6b83fca8f4a1b7",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6L1_Lesson_Pack.zip": "0f62f3d193e36443328ccf553b15bba3f0e75ddc8f76b2a72f8333035d317fcc",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6L2_Lesson_Pack.zip": "58a424aacd37371cfe42911a82d08e36c674aa36b700811961648a43d2c13de9",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6L3_Lesson_Pack.zip": "71dc842201fd627ae1766ede91dba65acf183514291fbafcc49cf3717f06aa93",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W6_Teaching_Pack.zip": "dd36acf680333cc56b54bf6dafba51c6eb00a85801a6333cb9c6613c5702ba12",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7L1_Lesson_Pack.zip": "db6a470dc5e60cf36f75bff48167943f4e5421a681927ce424928db27ad822ed",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7L2_Lesson_Pack.zip": "164e9da79876bc77853614b679b45597894b8c25802b67fe8dfda02ff781e98f",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7L3_Lesson_Pack.zip": "28327f9ecf4367a3153a16d04e496433645c16a59bc55f46d2646f7ba9f9d985",
        "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W7_Teaching_Pack.zip": "0f97ddebf0447024b936ed8c5b2053afcd8578911f64e1a2e1c560d2c3db1ad6",
        "tools/science_teaching_packs/refresh_packs.py": "09e86848edaf07d4064a2c0232e9078b6e33223b9c7d1b7b5c226e8dc4fbf29f",
        "Science/Teaching_Packs/GROW/Image_Credits.docx": "b7fe4b107695458bd8138170b0c98d14adddfe156871bd228db798790dbf3786",
        "Science/Teaching_Packs/GROW/Image_Credits.pdf": "651dcd9f749c6cfb5ffccd73eb9ffb14a57f8ff8a8860f348969b34114396f86",
        "tools/science_teaching_packs/check_hub_browser.cjs": "9323d0a64514970426bf30c8b281f99d100a8849d087d8f4354c78f3fe5022f4",
        "tools/science_teaching_packs/VISUAL_REFRESH_QA.json": "3ce5b90abaf89fc5a2a4085791bb16e09667545cf489a985c1c525bd7698fc80",
        ".github/workflows/science-teaching-packs.yml": "f3bd379cc5f1ebcb296f4819a8e2f6f7a488a4b5bd2955d409f8a7ee626715ff",
        "tools/stale_evidence_sweep.mjs": "17813c59e3752fb9843374a302895d0d4710fb2c749d29af81a77873ff9d3677",
        "Science/Build/W8-W13_2026-27/SCI_B_W8A_Sugar_Labels_Explore.html": "74d17d4e0f6873f094691daa753539f8a351887160beea6a8a8d727bba864d2d",
        "Science/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pdf": "fc9ba726c94177000d872c28e3c7db3812c268d6552e936a316c38654a95a0dd",
        "Science/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label.pptx": "d93b814710bcf57ece951ba0aaf82ed41320247571ec48147e26a5423b3c07e3",
        "Science/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.docx": "be71bc9be6c6d9c23383ee35ec739df80830ad5e336e7095098deaf3003a6d64",
        "Science/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Pupil.pdf": "25544b193963f552a1511ac17bd5b5353cbeeca71d6788ac4deddbc61f905dc4",
        "Science/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.docx": "7932493b683f1ac4ab7fbaabef8f55ec13e0db311dc63334788dc88e9fc5d099",
        "Science/Teaching_Packs/BUILD/lessons/W8A/BUILD_Science_Autumn1_W8A_Sugar_Evidence_Read_The_Label_Teacher.pdf": "8c9984c7683196b03a8acdf90764d7136f390f4fb0e28211077eb4184311f5a5",
        "tools/downloads/offline_pack_browser.cjs": "017782ecf949ee7c3030c4f872c2c532e0178ccb03cc39c8c636acf257623a95",
        "tools/downloads/prepare_pack_browser.py": "24446fbd47fa0a8b4de2ae1f79185206ecc042ccc72dfcdec8076c3bc38e9ada",
        "tools/downloads/test_download_pack.py": "cd5ec2a980f5cd305f4e33d18d4297bd1e75f8b9674f55e10c6f4d37a466ce6e",
        "tools/science_teaching_packs/check_build_sugar_browser.cjs": "f0b3b44a025131f16d2085f26ca7a2d9d19e2dbb58a6d692d309a49f3d3a1f2c",
        "tools/science_teaching_packs/check_build_sugar_pdfs.py": "62f8d1d1989be600374fdae1dbda9c7ebf407711cfb572123a3f9c31c4442a03",
        "Science/Teaching_Packs/web-slides.html": "f31f09d03f5d8c417af1745b38309fa537afb8bb4c6a08f387db3349d9e1cba2",
        "Science/Grow/SCI_G_W3_Friction.html": "508f1967b6481671dafb149d7177b620b194074312cee0dbdd30553c166b634a",
        "Science/Grow/resources/GS_W3A.html": "e5bfaf2bc70912aeb59fe9a2eb1032d86c7a473a1059ba782fee1be7b3513dc1",
        "Science/Grow/resources/GS_W3B.html": "fb6580bfd1e02d82627d60e1c2e08c3a34b227d0cbe760545502a8e51ab91208",
        "Science/Teaching_Packs/GROW/SHA256SUMS.txt": "de59e3ca70b403b69b625ae07603d69e1d557bfaa6f50a798d59f9ebb77f754a",
        "tools/easter/SCIENCE_ORIGINAL_TARGETS.json": "b5ca128e0ca53030256299a6877dffa781b63e5c1f2034722b75ae2ab806e204",
        "tools/grow_resources/CONTENT.json": "d8e39cef0051046bee5f1044e0cf2e412b3b4ebf8480361d6ddf298b667a6903",
        "tools/grow_resources/BROWSER_TARGETS.json": "288490cad98b1ce7d3f4b8f357c086220f1ef070c846189716c18b8a7122bd0c",
        "Science/Launch/SCI_L_W4_L1_Diffusion.html": "563e0bddc7049afb1dfc7245b1810da5094c19bca8027a08bbaf4c26d5a0dc54",
        "Science/Teaching_Packs/LAUNCH/SHA256SUMS.txt": "7ac03b10baef29ab9e82ab18fab775e22c7fcaf079c201ad818493902b40abc3",
        "Science/Teaching_Packs/BUILD/SHA256SUMS.txt": "4f26737e16194546a95f093cf1f566cc723bdce80822caf03cc7503abfe289b7",
        "Science/Build/W8-W13_2026-27/SCI_B_W8B_Autumn_Science_Checkpoint_Do.html": "7b27a0d82cd7df671c6a3b52b46d5d620ed678c332cdc58d1c649c3b29dacbac",
        "Science/Grow/W8-W13_2026-27/SCI_G_W8A_Day_And_Night_Explore.html": "a5c6fb99587b2d9d715b116cfe7b0c706abe186bd386cc23b72f4fb2b5984493",
        "Science/Grow/W8-W13_2026-27/SCI_G_W8B_Day_And_Night_Do.html": "32c49a121b8d9ed7f2af13c038117bdf4fbb0e9f23232f91a0015040843d6a00",
        "Science/Launch/W8-W13_2026-27/SCI_L_W8L1_Enzyme_Action_Introduce.html": "125bd365d7c46d62b3867ef226c3197e715d6d6834895ca1e228e5219d1dfa0c",
        "Science/Launch/W8-W13_2026-27/SCI_L_W8L2_Amylase_pH_Core_Practical_Explore.html": "cd724ac40006a40abee3b6bc958f6fcdb3c44af017ad2564f4a601154c4a65c6",
        "Science/Launch/W8-W13_2026-27/SCI_L_W8L3_Amylase_Rate_And_Topic_1_Do.html": "d415a934d0ab0e0de37b8f75bcfc5a3c3410fb8cdaf8ff1b187400cd3d1f75c8",
        "LundyLoop/1_whole_school/Day_to_Day_Desk_Sheet.html": "3d5fc8fe3563ed7e7d00df8a022b1888ef6f427579a607944c81594454311062",
        "LundyLoop/1_whole_school/Whole_School_Reference_v2.html": "715aca553c1a54ae504460d00f7b600ee17eefd27567f4a3aba1cd4b8de1fb90",
        "LundyLoop/2_leadership/Impact_Framework.html": "d2ede4fa93500dc48af37b8464ea85fa597cf2896042ccfbd43f3e78ae765bdc",
        "LundyLoop/2_leadership/Impact_Monitoring_Crib.html": "d116cde23efe70ccd3c004ff2379af42e9e7fda4ce8df7d7ee5f9cd548e1ca79",
        "LundyLoop/2_leadership/Ofsted_LAUNCH_Loop_Sheet.html": "1f7c600ffccaf931f5c8001e1c151e8165bbaa6094a4e25a3fccf73b424befdb",
        "LundyLoop/3_subject_guides/science.html": "734d2e53f6a7c28fe7e52c66d3ee4661b2557682acb30cc2e77d7e0b9eb19c03",
        "Science/Grow/v3_40min/LUNDY_DAILY_REFLECTION_EVIDENCE_WINDOW.html": "8a110cc1db2527e2e1a7d95e506fdb99d085a543453ca305aaf46fdd3f792a2a",
        "Science/Grow/v3_40min/SCI_G_W3B_Friction_Do.html": "97aed0e499bb85d11d2aefc822c9bd8c4c856281813ec7bbc04cd8d1f86a7c24",
        "Science/Grow/v3_40min/SCI_G_W4A_Mechanisms_Explore.html": "fd28d3366804e5a50cf1c93f0d831841e31f005b783179b170cc67527c391d8f",
        "Science/Grow/v3_40min/SCI_G_W4B_Mechanisms_Do.html": "7f186cec059e51af8d68c19bf8854f000cecdf63d4f12b187214905eafb5692a",
        "Science/Grow/v3_40min/SCI_G_W5A_Fair_Test_Explore.html": "cf7c715478fad8e29cbe1a42c3d5e7819465589fda764989256fbf47d9132bfc",
        "Science/Grow/v3_40min/SCI_G_W5B_Fair_Test_Do.html": "a404195e8d314ba7f40e6dd54d37a02946f5c08482054d416143fb1b11d1a7a4",
        "Science/Grow/v3_40min/SCI_G_W6A_Earth_And_Planets_Explore.html": "ebfa441095f114e2fdb427ccd9ee24860e17ad12ba55d2de77525768997a4869",
        "Science/Grow/v3_40min/SCI_G_W6B_Earth_And_Planets_Do.html": "91ae4a3586aff866541f5b1809b423cadcdf3321f664b29fce53defc4a6ce1ae",
        "Science/Grow/v3_40min/SCI_G_W7A_The_Moon_Explore.html": "2b54a5399c6422873be70b5ab43ea271112f54ae1401d990705b19a2f75030b4",
        "Science/Grow/v3_40min/SCI_G_W7B_The_Moon_Do.html": "85c9c9c7d4a12fa67fe6a098960aef0e880a3b7bf217667e39dad570bac11ebc",
        "Science/Build/W8-W13_2026-27/SHA256SUMS.txt": "28c48fd2644c70cee9e36b95981c25b08f9bd5693c9f43a7f73138f113aecf04",
        "data/chassis-census.json": "11e7b4b8f3bb43de2d338c59808418a2286b4fdb93bcf16e067868bc48a577e7",
        "tools/downloads/definitions/launch-science-aut1-main.json": "b42288f072512eaa9e0e954a6927d1247640dfbf6daac31fcfec4b80b59cb0c6",
        "tools/launch_resources/lesson_acceptance.py": "bbebaeb821f32c04eb1b2e01e819795ffa97cd851f33d7c22fec0b0505a9fe21",
        "tools/easter/refresh_pack_checksums.py": "7248b8424c6435f3637a7e3414e38fbab9f67e6b2a0f6f34fc8a586dc4e9c126",
        "tools/sx3/split_arrival_stage.py": "995e325aa9e5a157232cc63fd242207ecd1c9906ec43774611b47bb53f2d4ab7",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W01/SCI_BUILD_A2_W01.html": "8aa212b808412a58145e4cd66f8340feb51da865eb5f8600a15ed5813ec8e6b2",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W02/SCI_BUILD_A2_W02.html": "c50ed117c8637f20a99df353017a100ce9cc423d697e4a284c82c717ed191729",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W03/SCI_BUILD_A2_W03.html": "e498181851be764a17e0f56537f427c3b6434ae2620f6de6791c3767385a8830",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W04/SCI_BUILD_A2_W04.html": "e236155bca8b61a6792788d303555d550c8cca644678337468182e304b396a5d",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W05/SCI_BUILD_A2_W05.html": "17edd793f04daed139f9bcd52086e987b0684d223329f6ddd67f515e763eb6be",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W06/SCI_BUILD_A2_W06.html": "2051cf800a2413f6d87bd4fdcb24181ccd610eb3edde9652c0fff79c50e91b84",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W07/SCI_BUILD_A2_W07.html": "d48b70b0d933b12c8edc0630d4005ef8c0b4e5bd3902321aaf4c684749175349",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W01/GROW_SCI_A2_W01.html": "7ac238c37f22bd73e1a3030533ef95acc842f5ef1c5b63ec1fccfcfe6170ddc1",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W02/GROW_SCI_A2_W02.html": "c45c77b2c19abb443570e768ff9a5e3f0274ec0d2001ae8ec2f417905fed6080",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W03/GROW_SCI_A2_W03.html": "66350093c8ce6d76abae1413654f4f38fb154b48f88059458ee519a4b5005203",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W04/GROW_SCI_A2_W04.html": "c55a36af14216f2272a09df6773cf23178e29c4eb8c169d7dd74065d59bc9554",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W05/GROW_SCI_A2_W05.html": "e78439e2ce5893bf5a9b99d671d7d0ce440bfd4913210a9fb2c8945634c9fdd9",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W06/GROW_SCI_A2_W06.html": "5eae1a3b226fba8f323233bf5ab8e0b6793201aa3435a8ac431346636804ad86",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W07/GROW_SCI_A2_W07.html": "12b724f89f9573177cac1ac12c5a6d511ad5fe8c15e49ee9da1134296b24a009",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W01/SCI_LAUNCH_A2_W01.html": "68f551d7fad64a4044ff94a5ec5e51ef50fdbf610cde86e52a167b29c1e57e87",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W02/SCI_LAUNCH_A2_W02.html": "557f591ff51ba7386db0749302a5a375d7032095d2b442de847a9c25d3bf109c",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W03/SCI_LAUNCH_A2_W03.html": "31539459d094abc4df7f72a81e70a28521dc3522d82d8aa74602c2bc97e17d1d",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W04/SCI_LAUNCH_A2_W04.html": "8f0ff0382d8b081d619462db3d99df733ee294e95092c157a26f6a9ebfa58f18",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W05/SCI_LAUNCH_A2_W05.html": "87f56b1679f1898ab2fd2f131c231aa9623ca32c5ea0c970c3b7e240b4b09c04",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W06/SCI_LAUNCH_A2_W06.html": "3b77933ff22b9d4f2d42dfacfdf63616e6afc5ecfc4b7071721b2bb25965f3df",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W07/SCI_LAUNCH_A2_W07.html": "7b0222fcc21e8f5915c169d4a9555598bf31eda46f72c0c085e7c78f16f4a727",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1.html": "00b5137f2505c3616c801f76ce2edbb2d0f3b6887e677aaacc5389c7cadd8f7c",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Editable_Pack.docx": "bd312c7f1b0ed68783b007471db4358c05b2c5152a5cb47db009a032a8357a58",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Knowledge_Organiser.pdf": "21267a597ce2579b2850547acf74baba4bfaf554a48c4818d3f2107018232973",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Pupil_Resources.pdf": "9d71b77d7521ea2025f43f9ea8213a1a4313015ef4eaa6ecc080308f4f456c13",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Word_Page.pdf": "853bb9327e38312513f7e79bc0ed10b6bdecd0ae0cb201d1793bc87a184320a6",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2.html": "8faa8a56aafff866969f8c3ac448479bf982770914c3b12374a87639fe78837e",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Editable_Pack.docx": "5aaf766e14a746497f3c98307e33613d3a75328a63fdf28ce6e58938b1db5612",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Knowledge_Organiser.pdf": "d4df2abc39a9d292d21478ee0c3aeb0455d247810b3117bc1b3cac28c0f22765",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Pupil_Resources.pdf": "5092013b135085f18d15969eb71973c4ea13743f30d8cb5cf3311078d10707ab",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Word_Page.pdf": "55cc746f0041fbd95d3b8456fb05d80a402bc99d9890bbd2cf4cb10f9ed46d65",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1.html": "0a1775f29ac6214b764e64c87a2caaf6c35927139cdc749463fa0c464af6be30",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Editable_Pack.docx": "bcfa61d6d54b055ea9a9a8da8873820821a96d8d0a287c0afb882e32c44158df",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Knowledge_Organiser.pdf": "330c1068ad8c854eba3579c87323bbd44c6b34085add29f0116a4a74272b77bb",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_LESSON_SOURCE.json": "da18c08addd8cf72645eaf8f7d40b8bb9bc3237b014c6307ec9f709add0ce0e9",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Pupil_Resources.pdf": "0ac30bcf2a4ceff8384da01b1a1dffb9601c464cbb67c38e6a113ab8a903434e",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_TA_Brief.pdf": "6649b3ed6ab140b911f30c2f8037dc48d94d12dfbad19797d6370c2e1dce13c0",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Word_Page.pdf": "a0b07e735ea95722b7e04b9684360e951e3ca2f5e5d0e6245e3978353f083ce7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2.html": "612eb1229791086d24e81284554c7116e1b6ab2674dc334268ba582bd2b7116e",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Editable_Pack.docx": "25613d500cf28ec9f16869ab15a69ab087b2b6978c381635ee0aa8ebf5ac45a0",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Knowledge_Organiser.pdf": "6388d5e0ada1c030862c0616fa2d6cccff57aa96ff114e4fd5c4f07931827e90",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_LESSON_SOURCE.json": "b1a39d01a1ddaf5b1ebbbb4cdc5404fe581a0109a371ead52ad5c99fcf1325ae",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Pupil_Resources.pdf": "2bf6a56efd5e8a9a1b303e6c08652d30d5312f85265f84cb562352bd20b8ae14",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_TA_Brief.pdf": "a38d1ff54044ade0b490632902235be875a8054ea7b9389f6f2f5cc0d7f5e99c",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Word_Page.pdf": "f607ba492ec7241b4b960c46df721bd016f9db5a41a656769de272c0767f9072",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1.html": "a1aa50aebb1e11abe59435a1b2c552d3a968ea65e59b08c0860a675981b7e084",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Editable_Pack.docx": "3819492eb5e69f6272c9bdf8d6b67ad505c403ff6d12126c6aa89bcb94353061",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Knowledge_Organiser.pdf": "0be94a336b15aa90ff2d8ad6bd083c50a594b0772b2c34f40e0733210f9c8359",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Pupil_Resources.pdf": "90d96ae7c9db767121ad2bd02b32e9e9a6d0bc27c881a6dd6c251f0f9717ffa5",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_TA_Brief.pdf": "2529ab39a331969e9ce36ef52a7cdfc647c542df3733060a57af63ae8753bad7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Teacher_Notes.pdf": "72259decc5cb72726fd63678ce1e9fb74f0c4bb2da4102a395e7a3c67ee79757",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Word_Page.pdf": "07394707d6fe82e4e615c89edb7ec1ee00291bf673a13a3be9705b5101adead7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2.html": "51b1e3023d8608535857da9080c9517f5f7f90003e8eb9f939cadd196f87b9f6",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Editable_Pack.docx": "1c12f4ad7e2152933c37835dea88b7bb667ec94517711d9ab48298b845c74639",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Knowledge_Organiser.pdf": "6828774324b31e15096930f9404a0a52332b12ae0145f51d55d60ac0ec252a2d",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Pupil_Resources.pdf": "0c7803325256e2e7c21537a375b6d01247c61b1948a9b272562a36cf2b020207",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_TA_Brief.pdf": "3f00e2f8c8d16c407ef4f919037cf1819a12fcdf1161b3b17fc0dcf278eb835f",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Word_Page.pdf": "5ff5abc72687a32b07926ebde0301cabb4cd9822a12cb2c962ef22cfb149ad5c",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3.html": "398c2c468645987d24ecc8ea825ef87e7fee1e3e273588bda90f6b0259b53adb",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Editable_Pack.docx": "e55f161c21cd21afae8a4144c96a826c11b6ead745e28670113eed616241af3e",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Knowledge_Organiser.pdf": "187ba3e37c2eba48733072546e10d6efdcd9eac0f72be30c82f905c65b4dddbd",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Pupil_Resources.pdf": "5bac2399679393f5675372c714ca52fb0575963d886231477b998c25699eba5c",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_TA_Brief.pdf": "10b256f949dcb82d1ac06674f6cc2fa36f77787914f4c55d4d3870bad3a0767f",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Teacher_Notes.pdf": "f719fc0973fb6c527e741b70e1804ab7bc662ed1ca64ef55c7aea8b57bdca7eb",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Word_Page.pdf": "7efe49136d285b4cb400056f788c671f944cc6da25c38723b0d89fd9cc1fd1ea",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Slides.pptx": "8692338d658540dbe378b8a3c7c51afea10727e6deb3352a9c594761b7e7cd7b",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Staff_Answers.pdf": "f306d34810421da4baea544cf6f828f3d08b34174c92f8214c37d453fa4fdd43",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_TA_Brief.pdf": "9b9b89be125a6dc3e0ae2687d2a51fb4312707a2963dedc59f9a59f966cb1400",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Teacher_and_Cover_Plan.docx": "20e222766e99053b25c57f67a7f26fddc6ed8450fc110cb09ba07de30f59a969",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Teacher_and_Cover_Plan.pdf": "167a8bbebe34110542850ac7ad7fcf122d21782bb284982c362229acfe69d8f2",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Tier_Pack_Standard.pdf": "63aabedecb5a1f128858bc1b3fa8bda81ef313ded6b3bee9ee8fe809327cd80a",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Tier_Pack_Stretch.pdf": "9eb29dc33de527778d6e8b22f89b5174192e4aca3860c3f2879c0076f48555da",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P1_Tier_Pack_Supported.pdf": "fa7b1271152b731b7e5f1ccaf5ce970f5e1a2ed978b34b686b5965ff72e0f9e4",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Slides.pptx": "80bf3559458bbb5a398ef8970bd2abed3bb58e088ca4310bb5a9e5a05ded1edb",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Staff_Answers.pdf": "ed66906bfee2eb41acb7e3ba4a05b5ed90a287854f855bdb1bc35f0762120568",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_TA_Brief.pdf": "d5bd612069fede8d7946f75196eef7784b89a7153bee3ac611313b994852ad41",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Teacher_and_Cover_Plan.docx": "7c083cbed6e11d6d221ec0f71088a26502c07ba3df4c396d8ed9a5b767ae85cc",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Teacher_and_Cover_Plan.pdf": "0fac05a0194a8e5154b4d18b34b068ca39cd23db5a6545d82cc287ea5e2fe458",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Tier_Pack_Standard.pdf": "e8b4ceb66eb38178459b31069fed21651fd42065888ee1622d50acc3dd5b8cb6",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Tier_Pack_Stretch.pdf": "ced4c6b1082edb09233b8d5df9601deedec104ea657a29ea6cd415908e65c00c",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W08/SCI_BUILD_A1_W08_P2_Tier_Pack_Supported.pdf": "7dc3046a6740d792644996744d0adfff410fe627564a09c7cd1e630a0ea245d3",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Slides.pptx": "b3a595b98ac472d04264fd693a59786e2f22d0463d6931182de0363fbc50c6d9",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Staff_Answers.pdf": "d37a45c44b76c1c7950bc1190591bb4d98fbb7a1586518356175a1bfb4306e49",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Teacher_and_Cover_Plan.docx": "f9b64f301cb61b0a2c4d4b0c611e717d24b2842e07d24724bb9add6231f57401",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Teacher_and_Cover_Plan.pdf": "e1c95f87e9818a43bbd8c6e2425ab684a5c326c4f487aecf0a3454bc84972211",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Tier_Pack_Standard.pdf": "2fa6c16d8958d3795940379fd6e1abba4fbe0d417bfb8586a69b2c2d36806430",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Tier_Pack_Stretch.pdf": "7fd0f0c2367bebb9df4f252e750d39ab21fa6b61029593b5c554fc927be109fe",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P1_Tier_Pack_Supported.pdf": "307c7e59582b457950ff9285cf73ed949646c244ff040b2e0c91da7179a6d197",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Slides.pptx": "e52d66fa9fc148923a25cd0a9f6bac9fb5f218c3f3c4d446565f2009e810fbdf",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Staff_Answers.pdf": "da089015ddb857afb7716294d82bf9082ce616fa6d2d38bd9e86815d0b399f3d",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Teacher_and_Cover_Plan.docx": "9d77750476293f20d2273a7351c6efd16c3f12a883365847710aac6bb57f3f7b",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Teacher_and_Cover_Plan.pdf": "109253b5aa73f8cf7adc6cc629e728ed7deb237566530fc5fbec7ce4c58ef004",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Tier_Pack_Standard.pdf": "aa9f7c21b2608bd803de1bcce3907ea8a5717440d206ad940d4ca19ab387de15",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Tier_Pack_Stretch.pdf": "17370edcc7d2f5299b2fe6544192edb87de6f67f2ea71b27da7559d70c2e2d91",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W08/GROW_SCI_A1_W08_P2_Tier_Pack_Supported.pdf": "afd8498e3615c0083a33369f27e0619843c4ae9ad8da7e2e79deabfc1fce9cc0",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Slides.pptx": "e7b5a6d12b6b9b1ac3bdac81a0b9cfd2e13d0feaab89e7305eefe38979acff67",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Staff_Answers.pdf": "a2d3cf2a33a2243dd90554e06824fbe9237d25b635cd8f160f0432e8de3d387f",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Teacher_and_Cover_Plan.docx": "1e5f9e6be792dcbd135b7af50643eab585dd01536778f52a07f623b73a22f52d",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Teacher_and_Cover_Plan.pdf": "5afc540ddb1af6d1a5ffd4091dca982c8ffa6a3163b0b3acfdee5f2208d0d1da",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Tier_Pack_Standard.pdf": "6f8cacc3531014beb13283b62f232e4e0f13f8966ee5456d91dac51e6be7916e",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Tier_Pack_Stretch.pdf": "cc8c2610c8d2426718ff68d0c827186051ed10290b84ce6abf88e55ed550a31b",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L1_Tier_Pack_Supported.pdf": "9c3b8c182397006de0aadaf302f576d08d86991f7ebef5b7ff96bea4a90110a2",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Slides.pptx": "22b050e29515b7870e3a4ffd946ee2572144021a98222ba445e48cfd55cadea3",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Staff_Answers.pdf": "d74bcec22272fd357a8e9a70fbdceaa20cf1070674510e5a3a1c94abae780cef",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Teacher_and_Cover_Plan.docx": "402637e43bfc0798c83e70ade6198cb7cf9d040b7d71553a08a9cfeb2318d821",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Teacher_and_Cover_Plan.pdf": "1167fa90296852a34867e15693c240e8f32f4e2ca9710984388b27063417d3e6",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Tier_Pack_Standard.pdf": "a35d8376b32714dc9efe844fae9f0de7c3eb2c425f4f978c458267594febd72a",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Tier_Pack_Stretch.pdf": "8f75a9c3eb811e0975b90b55ccee8419da2e46bb81d611f0915fc8bdbbbe4ac8",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L2_Tier_Pack_Supported.pdf": "ca7e159c3ebaeef3599aa51b51c4293c70926910e6fb7dc2b3858014b166bc7a",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Slides.pptx": "9e5e616843da77c847f997071d64bf66c99b69410cee9114eda9e3e28c3d121d",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Staff_Answers.pdf": "c49fdde938fe1c2bddbbfc72690bf7813afed79aa78876961175e68e3dae1ddc",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Teacher_and_Cover_Plan.docx": "c8fcb602b71bf492e6a6b61abe5ec76518ea4220da3a83dc6699d55c98b74846",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Teacher_and_Cover_Plan.pdf": "a1a89d754ea4628c791046505158b08a063fb280ec35b79a3e48c70819ea7fe4",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Tier_Pack_Standard.pdf": "9b53f78108cd24692e11187272294f9bcd0d748e60c5c374c01eda88e6602b53",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Tier_Pack_Stretch.pdf": "64277a00f927f640d733ea4bfb013185bc50e39767c90e8169050b5d73cadc8a",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W08/SCI_LAUNCH_A1_W08_L3_Tier_Pack_Supported.pdf": "d632f205b8366fd1642e79483b4e38861af09782ca38a32854cd5b82f55975a8",
        "Science/Build/W18-W26_2026-27/SCI_B_S2_W6_The_Evidence_Museum.html": "4b634583582af1ea962250272a7aec54f946f6c8ed29620dc440fcb8269fd3f7",
        "Science/Build/W18-W26_2026-27/SCI_B_W18_Soil_What_Is_In_The_Mix.html": "28cfd735e97e57e6855e46974e0ac974591fc8dbb061c24a39cbf2a4ef8238af",
        "Science/Build/W18-W26_2026-27/SCI_B_W19_Soil_Let_The_Water_Through.html": "40b7517cad3d845889fee26baaf349521b57d5c780d5f191f377b76f2d761fb9",
        "Science/Build/W18-W26_2026-27/SCI_B_W20_Soil_Account_For_The_Water.html": "9eec17c751f17e527743d77c77ed9f29ee1fa3819a36b310e6c8e2ada412a793",
        "Science/Build/W18-W26_2026-27/SCI_B_W21_The_Blackout_Box_Mystery.html": "ca8819e2572154ed73e7b0c04aeb1a8879b4dabb1b41b190f3a2df0bcbfb2a0e",
        "Science/Build/W18-W26_2026-27/SCI_B_W22_Light_Source_Detectives.html": "d61681feb1a1594731ae96840801b7f6f77984d262c695c9f9f09b7f98aa50f5",
        "Science/Build/W18-W26_2026-27/SCI_B_W23_Sunlight_Make_A_Safer_Plan.html": "d34883c656ccb0a0d5432003157e6c6b385866cef735a6297d599840822929de",
        "Science/Build/W18-W26_2026-27/SCI_B_W24_The_Shadow_Screen_Lab.html": "26a14b6ea8a2cd1f0eb5e6d284e95e590a8c305015f21e508c7aefff8917f009",
        "Science/Build/W18-W26_2026-27/SCI_B_W25_The_Shadow_Size_Studio.html": "b7a7b1a88de66566316dc6a46085dcd811fa670d7c78667780ed8402f619cbf9",
        "Science/Build/W18-W26_2026-27/SCI_B_W26_The_Fair_Test_Repair_Lab.html": "dbbe69efce197c480d35363a728239ea7c08bed62ef190a1577f5820a1f3dfc6",
        "Science/Grow/W18-W26_2026-27/SCI_G_S2_W6_The_Spring_Science_Evidence_Exchange.html": "a3b17f6db996f543933bdb82e3d0ffbbf6cd2c3f8c9a1b2320f28b094e65287f",
        "Science/Grow/W18-W26_2026-27/SCI_G_W18A_The_Cold_Case.html": "4dc608b890c9e83fbb2aa9c1624abff7daea6162c61b9127e9114e987f0dd4dc",
        "Science/Grow/W18-W26_2026-27/SCI_G_W18B_Circuit_Fault_Clinic.html": "09d665085a771ff88aef11e305a2a1e3a703fab7ebd7b54772501d1ce3da1b47",
        "Science/Grow/W18-W26_2026-27/SCI_G_W19_The_Spill_Mat_Design_Lab.html": "2000f388aa92c4f4f645a52f30596191fab44d2c264811d5f9b7a2689a9d62a3",
        "Science/Grow/W18-W26_2026-27/SCI_G_W20_Body_Systems_The_Dispatch_Challenge.html": "aadc325ed8dbe256758fc5314dabe03894f77c2d7e952f9699ca21f5817c63c4",
        "Science/Grow/W18-W26_2026-27/SCI_G_W21_Heart_Route_Rescue.html": "f76cbbf02230085a7c99f80abce46f0bd59fe93a3ea2148287938f979a479de2",
        "Science/Grow/W18-W26_2026-27/SCI_G_W22_The_Health_Evidence_Advisers.html": "ea1f9bdd3e1e71512c218c0437dcbe571e7695d24db626475aff58add06eac78",
        "Science/Grow/W18-W26_2026-27/SCI_G_W23_The_Nutrient_Delivery_Investigation.html": "d1ad827e86dca44315162d61b1f3c0697450a27befaa6df39427dbdcd76da4c6",
        "Science/Grow/W18-W26_2026-27/SCI_G_W24_The_Recovery_Research_Room.html": "f84602b15ae66c61d9568ffc631e01a7af83989606f9a989d2d7e3fcb57db379",
        "Science/Grow/W18-W26_2026-27/SCI_G_W25_Life_Cycle_Archive.html": "4a5d5339598e8fc6a99278908b8ad75b27ee631019deda1d0a58f9dfaadc5424",
        "Science/Grow/W18-W26_2026-27/SCI_G_W26_The_Life_Cycle_Comparison_Bureau.html": "233afa1cfc727b1fe719f24b1c3542d4d3f4e35d1e6f338addbb3df522a58d45",
        "Science/Launch/W17-W26_2026-27/SCI_L_S2_W6_Health_And_Plants_Evidence_Checkpoint.html": "9fb00f82ff92576aeb12317a530eef5ba5a03da702de768e2441120adfe0a5b5",
        "Science/Launch/W17-W26_2026-27/SCI_L_W17_Evolution_Build_The_Evidence_Case.html": "e7dbd3b30a2ae40d672d431e67ba8adba7c9feda327f9cdcaea8f82232d10791",
        "Science/Launch/W17-W26_2026-27/SCI_L_W18L1_Selective_Breeding_Design_A_Resilient_Crop.html": "5beff778cf209dab5dad176433f46e0ae22c001164b36e2b1affbc49a0f33f37",
        "Science/Launch/W17-W26_2026-27/SCI_L_W18L2_Genetic_Engineering_Change_Test_Decide.html": "178e9375f703c1dc8675858cf9b4e520f8fda549dc405965ca609b01bfa3e443",
        "Science/Launch/W17-W26_2026-27/SCI_L_W21_Disease_Detectives_Follow_The_Cause.html": "38f8ffb2ef47c0eb3ff7185a00a8bf5fb7a596f28c3701dd4ae741e521ea86ee",
        "Science/Launch/W17-W26_2026-27/SCI_L_W22_Immune_Memory_Recognise_Respond_Remember.html": "8548a17e7ee5fb02c9f8d5219d057cec8473dcb7cacd40fb54bc0d30cb2f7353",
        "Science/Launch/W17-W26_2026-27/SCI_L_W23_Disease_Data_Newsroom_Make_The_Numbers_Fair.html": "0439708c713ae147bc112ec0250ed09a1392a2674e8c73712406c0d11f7f81b4",
        "Science/Launch/W17-W26_2026-27/SCI_L_W24_Photosynthesis_The_Light_Lab.html": "4757f0251a0b5306e8e887a9611c48c361f45f40262362aa901388e749a0592a",
        "Science/Launch/W17-W26_2026-27/SCI_L_W25_Plant_Transport_Follow_The_Water_And_Sugar.html": "769d31103271220bb6aedc6cf67539974de7111300a166a9407c36db54572478",
        "Science/Launch/W17-W26_2026-27/SCI_L_W26_Greenhouse_Challenge_Grow_More_With_A_Water_Budget.html": "b5c0548451e26c321cd92f2d5ba39325dc43e284841bc6242f2b6532b3085269",
        "art.html": "066d4bdd3107ae7105d2930352b48e8b848f53a402874e3ed432ac7eb0db41bf",
        "tools/downloads/SOURCE_PLACEMENT.json": "a4ad22abede7e69dcbd434781ea385c613662121f38417c71e658378fe229b9e",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/BUILD_RE_A1_W08_Captioned_Model.mp4": "3ab4e04878f4f32431990301f4efcd6d13622f00b4c8d8614a55ccd7d5da6f5f",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/BUILD_RE_A1_W08_Knowledge_Organiser.html": "a66d638003a6a58250154c3744099d04780e20051c7e5455e3c3a98144bb1391",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/BUILD_RE_A1_W08_Lesson.html": "8b29ccf42a1a5137da2337594cd86f9116ed166113edaaa5a8b87efbc8248ff0",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/BUILD_RE_A1_W08_Model_Transcript.txt": "1f2ea6dea9ca7f89a89551ab1390dda2c46facde3fe53b2627c27810d46ab767",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/BUILD_RE_A1_W08_Pupil_Resources.html": "1bd5150035da1b98e09cb128cee4f6d95c1c1e50c5f6f16ce47d273612766678",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/BUILD_RE_A1_W08_Word_Page.html": "d2310504eb3f386b2a6a725b258aa3c138f8fd433c9113ccf99f40813f18a738",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/Object_Picture_Choices.png": "798ebe66df7c5d23e8453827db5a728e9be0e0201baee18ddf09efe655e19b7e",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/Object_Picture_Choices.svg": "854b2d8ab3a62c4ad23e8d3afcf7d331acfa90ae7a82357f522f39df8fca078f",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/Sources_and_checks.html": "dbd5258f906ee7ad3cd5acef6683c89af3691fa855459330e66cb1492e9043bf",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_1/W08/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/GROW_RE_A1_W08_Captioned_Model.mp4": "92b4151af44941422b3bbcaaf01bdaaad2b2a034e01f020982c2c0b25066382e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/GROW_RE_A1_W08_Knowledge_Organiser.html": "0c6624b1a8b739e6fb37efa1dcd8c2cbe73749452db4a5e95efaf3934a18a88e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/GROW_RE_A1_W08_Lesson.html": "fb8acf612896c8891db31b498dab8240b6e6d67e819985b5224e48b2fd512ac9",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/GROW_RE_A1_W08_Model_Transcript.txt": "c517db4159a9ebbf7b72cb3fa2fdc8494138576bb53b07e0038c899612d58d36",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/GROW_RE_A1_W08_Pupil_Resources.html": "09e6b90218f1361b1e63632c53c5b23af8708d036ab0ecfcb2074f6778800d72",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/GROW_RE_A1_W08_Word_Page.html": "cbe1d4e91036c44ea42606ef18a92f4075b94de83ec923d8a16775649227b5e5",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/Object_Picture_Choices.png": "6aade8f8f4348d7c1641b447142a1339cfcdfbfc4990e8300e0e2d625068a233",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/Object_Picture_Choices.svg": "53e21c24afcfaef31e60348ab838f3b5d55f86dc0b97ee64231079ad880db49f",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/Sources_and_checks.html": "3c777c0fb0c598a6722c8cb6c8c2e71b5e20da7b5c518667c20c15f389b076df",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_1/W08/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/LAUNCH_RE_A1_W08_Captioned_Model.mp4": "8b4eb9d2ab9ec93df8a5d387ecdcdaebeaed03f7b9a8e8809933e223ca698582",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/LAUNCH_RE_A1_W08_Knowledge_Organiser.html": "efcb492c4fdf3f63c96eb1897df0ffe1c05e03a6746d8ae3547aded71e9f8015",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/LAUNCH_RE_A1_W08_Lesson.html": "6795ab3a325bb78731dc39b5f8e49819de3fa7524ff8c3068b3dfc6e4e856270",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/LAUNCH_RE_A1_W08_Model_Transcript.txt": "fd1f526487991505fd3c9b1c2c63d7cd96c4efa168c9c652f329dfbe683ffb5e",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/LAUNCH_RE_A1_W08_Pupil_Resources.html": "2decd87c30190b1cf687e6f601acc9ef1a34d8a2b80e7fc0636d4c41f1481d99",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/LAUNCH_RE_A1_W08_Word_Page.html": "0803152ce3a25213521c94e2d54a644a734e7ed419430599454538b207ad75c3",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/Object_Picture_Choices.png": "7b8265232d9d4a7483174e18ff587529e9206b0d325749aec547c9a9f1c336f9",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/Object_Picture_Choices.svg": "20eda92e86b70ff59350ea9834d16623602ddad06c90377ee36778c1020a1bd5",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/Sources_and_checks.html": "30f756f5939970a48368d743a52f5ddfd7b010433c740a1651e2670e5d8c6374",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_1/W08/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/START_HERE.html": "4ea63a0c2de74e7d37f235b905229fd4e76702b6a058245b2fd8690b9f54b336",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/START_HERE.html": "9ec66e89f1b09782117ba72578ba205e37b196ee6dbcb0b0de2741f0cafd30bd",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/START_HERE.html": "d8688b954279d1d83d9b915a7b59610e6c0b32003681d7bf3ba8d6d36f7065f2",
        "Humanities/Teaching_Packs/RE_Spring_1_BUILD_Reviewed/SHA256SUMS.txt": "dfb40505261e40c0e5038d6722351ddd0450055c47b17a85a6b88d42714f584e",
        "Humanities/Teaching_Packs/RE_Spring_1_GROW_Reviewed/SHA256SUMS.txt": "80bb4cc4d430e3b110781c1870a6454f48cf2e56fe4c1759f038594d3ede2d8a",
        "Humanities/Teaching_Packs/RE_Spring_1_LAUNCH_Reviewed/SHA256SUMS.txt": "c4feb606541eff53b17a5e6d793f87d78c61d73caf6858944ffdb0db8d710d22",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/RE_Scheme_of_Work_Spring_1_2026.docx": "7bb5fe5fc1c72b12b472e9a3019f1b7bad7109f701698acf5a413587e99ff70c",
        "Humanities/Teaching_Packs/HUM_00_SoW_and_Order/RE_Scheme_of_Work_Spring_1_2026.html": "d1364ad885299eabe43d28b54839d5cbe6ac8342158bc47d496c76e18a7ff2e4",
        "GROW_ASDAN/Community_Project/START_HERE.html": "1ca02932fbeafb09930d3dd68ea03248d39e58b4aa0b00cd18632c452c6c5801",
        "BUILD_ASDAN/FoodWise/Teaching_Packs/BUILD/SHA256SUMS.txt": "801425aa43631264b8e5288d7eabb3bff6f972c5e88263c57572ea97545633db",
        "BUILD_ASDAN/FoodWise/Teaching_Packs/DOWNLOADS_MANIFEST.json": "a913269f3d35d03f3c67eed19500da122937655e4956ce5c3b90af87076f4b30",
        "BUILD_ASDAN/FoodWise/Teaching_Packs/index.html": "e35e895bc38db84474de094ceb402e273f9f93419d7b4fcbfb08e69ae09f6cc9",
        "Careers/Teaching_Packs/BUILD/SHA256SUMS.txt": "97efdc2b08737bd672a93549964d641a5973130eab53c5cc872d1daf110bd138",
        "Careers/Teaching_Packs/DOWNLOADS_MANIFEST.json": "5590c0d9996a17bba2bba981f68d45612dd5845b070417da4e3ea07610aac3a9",
        "Careers/Teaching_Packs/GROW/SHA256SUMS.txt": "a0f67cdc5dd04ea632369655185a71d50f370c11a035a19044c3850806502650",
        "Careers/Teaching_Packs/index.html": "38a590db2d2a8eb62941dced4603ff8dfe2064b244503f26a6f0817ba9d7ffa4",
        "DT_Textiles/Teaching_Packs/BUILD/SHA256SUMS.txt": "7be9ae481f7dbb9693afa7a600f7d7922d9bdc82e1d34db780272612e8c346fb",
        "DT_Textiles/Teaching_Packs/DOWNLOADS_MANIFEST.json": "fc17200e5551a215a79b906e9cf55b31310b03836039b777fbb3b0aad55ca3b9",
        "DT_Textiles/Teaching_Packs/GROW/SHA256SUMS.txt": "e4c41c8799701b85f1e605fe3730ab9dba8f0e44836e66bc7f322958193010e9",
        "DT_Textiles/Teaching_Packs/index.html": "0ca9d944edf8cc9ca90bc076b3e368a0e0847eaeb805e3259842ccd24cff2cc7",
        "GROW_FoodWise/Teaching_Packs/DOWNLOADS_MANIFEST.json": "b4de1de95a6079bc61169c795177028d6f4a5c104a9fdc91db42ab4861488476",
        "GROW_FoodWise/Teaching_Packs/GROW/SHA256SUMS.txt": "061d2fa95fbe65bbe567b00d21d45baa563a31ffd1ac66eccb414c2bdc80ffe9",
        "GROW_FoodWise/Teaching_Packs/index.html": "264b07915612bccd2cb4e1ebbe8519cb7b560b7216ba09e37c5b42a5589d904c",
        "Humanities/Teaching_Packs/DOWNLOADS_MANIFEST.json": "52288be18459aaed5a108ea6bc4e3db6225826b92bebdf38e9c71122597ad156",
        "Humanities/Teaching_Packs/index.html": "7a440ca2a9ae29b1394b8bd20136729044db7347399b9d1f724129d155a520ad",
        "Humanities/Teaching_Packs/SHA256SUMS.txt": "799757748e78233580842920a195d3253042e78e4dee478d64d749f5da00da68",
        "ICT/Teaching_Packs/DOWNLOADS_MANIFEST.json": "6722f2ef668c5f16acd4b55f9bf67fee03aad6eab711224a3d239526f4bba7c2",
        "ICT/Teaching_Packs/GROW/SHA256SUMS.txt": "02524211bea8d374f7d5cc54bc73498165ead4090909147759881f2a468e50ad",
        "ICT/Teaching_Packs/index.html": "4a154278ea7ebf18985fd3d7e9d92bbdf81eb064a87d74189b37bc9e31fb0778",
        "PSHE/Teaching_Packs/DOWNLOADS_MANIFEST.json": "617f2636e9ddee6d1a498e60f7ec21fb0cfe57c58585df12edcc070487a82bca",
        "PSHE/Teaching_Packs/GROW/SHA256SUMS.txt": "98623695f0133b6c0b8ef089d5bcd982e30d7029f1477b1adac54e25bd840973",
        "PSHE/Teaching_Packs/index.html": "7b3c9eeaad68d2c3c4afccc579d6cb8df9bbf6a2e335ea21827315c1dce5548e",
        "tools/verify_fixture_names.mjs": "75417d083048ca425535807d2352163936fc22d18831997b5c2ce05c8e3dbe49",
        "GROW_ASDAN/Autumn2_W1-W6_2026-27/CHECKSUMS.sha256": "711cf723430c8520914327bb9cd8d9276fbb4285185e68792803987cdbca20bd",
        "GROW_ASDAN/Autumn2_W1-W6_2026-27/START_HERE.html": "27bdd6886e7ac0a3cf4c21baa86f3c27fe3e800866693fd8bab38f9857cb0db5",
        "GROW_ASDAN/Autumn2_W1-W6_2026-27/index.html": "27bdd6886e7ac0a3cf4c21baa86f3c27fe3e800866693fd8bab38f9857cb0db5",
        "Art/Build/START_HERE.html": "2e4338516acb7a3d4daa0bf2ae9a8b85f697320535639cef55e391554b007cb3",
        "LAUNCH_ASDAN/W7-W12_2026-27/SHA256SUMS.txt": "2d22a8b2b0c8a39fd5e9a034469826c58593f8064f191b150c441618d53c3582",
        "LAUNCH_ASDAN/W7-W12_2026-27/START_HERE.html": "0339b378fcb15e98689e74415ec4c55e5f3f5fce3372f4306778e4c9921efb98",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W11_Light_on_a_dark_page_Classic.html": "26f8cefbdecf18dcbebe127be359d0e9d9fa1582633c7394675090e6b9e5cc17",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W1_Explore_Drawing_Colour_And_Technique_To_Show.html": "3952953ad2027ec7c98279a3fd0d0b60af330eface1e6c285d2271323a48bba6",
        "Art/GROW_W1-W8_2026-27/GROW_Art_W11_Design_a_light_festival_panel_Classic.html": "b243f53b6bf2d6c833c638e51a8753d98651faeae958f636e8c10566afb7a504",
        "Art/tools/assert_estate.py": "dde499e2e8e9ce8d4e3fa9df7cc7bd4184fb746f4e823e1e568c5dd96e0ab175",
        "Art/tools/assert_print.js": "f383ae89df4c894a374efe56c0358d08f4fe037eab520c0f753e9cd50337e1b6",
        "Art/visual-learning/art-visual-learning.css": "d6d0b23cae7b46467fef98fe04a191ac47f787446cf8097913ae5e637cad8a5b",
        "Art/visual-learning/art-visual-payloads.js": "451b58aba7e17c09372195cf70f484b708c9faa8893cd4c252e882f0a53e894d",
        "BUILD_Estate_v3/Art/index.html": "4a415b437a73b2918034c66318ed4d4fbd7955d6a5342663278c3f12d0d9ae3c",
        "BUILD_Estate_v3/Art/manifest-v3.json": "5be2b169246563d3186e832df20edc076c2cbfccf0ccd99f824f9543b7c1db27",
        "BUILD_Estate_v3/Humanities/index.html": "c44ecaa8f371de403454c2b4145ddb5317186743ca202577f4d535990b57684d",
        "BUILD_Estate_v3/index.html": "302893d70d13f5ed91521614e9bc5f156f3a1fa32a93c32fce0d3cb465de3d1f",
        "Humanities/BUILD_W14-W20_2026-27/BUILD_HUM_W12_A_celebration_in_order_Classic.html": "27cf15efee5fdb1a6a16df104b5a05e44ad2dbcdac1c7faae405ca3d2559c422",
        "Humanities/BUILD_W14-W20_2026-27/BUILD_HUM_W14_A_fair_chance_to_join_in_Classic.html": "ebc2e90287b33fd7344fd0ac67b6ada091cce6b2c0fa62b825a6c469a61a141b",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W12_Festival_lights_across_places_Classic.html": "d42013be46f71d98f864190546ab1a83b623f46f4ece58d95db1def95a077746",
        "Humanities/GROW_W9-W14_2026-27/GROW_HUM_W13_Compare_celebrations_with_care_Classic.html": "d97bba67ce0adefc4212e37fcc37e4e31e8c76a16f58907228040a6f04530424",
        "Humanities/GROW_W9-W14_2026-27/SHA256SUMS.txt": "7f75f0e7f0884660f2d65ba3b767aa30e80b02730fefb3f9d16b1acd8a95de12",
        "Humanities/GROW_W9-W14_2026-27/START_HERE_GROW_HUMANITIES_W9-W14.html": "c68486b618a6df5156204232bbddcd49284e3e9c5cb053b1dd719b5c4a5c09ef",
        "Humanities/GROW_W9-W14_2026-27/manifest-v3.1.json": "c018845904d7dd76fb7a0946f70f086b6a6f75fe47d9a1464cc3510182fed2fa",
        "Humanities/LAUNCH_W9-W14_2026-27/LAUNCH_HUM_W11_A_growing_town_an_urbanising_region_Classic.html": "804a3e899082f3d46a7663dd69cd35b6b59d728c73408acf53b208c0c86e38ab",
        "Humanities/Teaching_Packs/BUILD/SHA256SUMS.txt": "e107c1706170a7738de0739d470903df52d934b8c9d2c14ec1f53429b1956d32",
        "Humanities/Teaching_Packs/BUILD/Teacher_Notes.html": "5db3a99e71dd2a39143292323ec6d165adda320ade20bdb38b0cfe763aa13677",
        "Humanities/Teaching_Packs/GROW/SHA256SUMS.txt": "1ac37fbc8fadb9b05291818c678702cfb8eeead2998469c3b5baba8210af254e",
        "Humanities/Teaching_Packs/GROW/Teacher_Notes.html": "0b37060f6c8637f4a35d79dd46159a22d5f52b9114688825be6c3d3fbceab85f",
        "Humanities/Teaching_Packs/LAUNCH/SHA256SUMS.txt": "4071aac6fd69fb4326d35aaf70a0acbaccdb95ca308a04269a100669de4e76be",
        "Humanities/Teaching_Packs/LAUNCH/Teacher_Notes.html": "05784e354a243b76859c4ebfa7f6a9b0d0b81d89a62f477e0609a6ca665b8063",
        "Humanities/Teaching_Packs/web-slides.html": "b58ebc98e92d6b9f32afee63db8b3a1d0f3006cbabcfe2df115ee2c299238d6c",
        "Launch/Slideshows/LAUNCH_ART_W8_Complete_The_Review.html": "c66c2121c34798ea7a421d8058624a4846b75843c72e5a158d61eabeaf3b632a",
        "Science/Build/W8-W13_2026-27/SCI_B_W11A_Rock_Permeability_Explore.html": "b308d3ed71d4cca2c7828fd406e50d43d3b5244e56ca58478976f336baecf114",
        "Science/Build/W8-W13_2026-27/SCI_B_W13_Where_did_this_material_come_from_Classic.html": "aade409713fad37b7e3e03297654f6702f45ace803b605c8720b368bc09d063f",
        "Science/Build/v3_40min/manifest-v3.json": "574f45f03d752bb7559494a9033947efce666cf37287c4ffb3db178b9e95a6d4",
        "Science/Grow/v3_40min/SCI_G_W3A_Friction_Explore.html": "f4fc7562eee11ae418568007232622da88eaf56721d93b4563ae53fed791d0a2",
        "Science/Launch/v3_40min/manifest-v3.json": "0db2f244f5160808d7e63365aa2ce82f30b9b9ff425aab357d6089c2b12287ce",
        "Science/Teaching_Packs/BUILD/Teacher_Notes.html": "e56665beb68e8ac8dca6d39f817d785b97c63620d6e24f7c68eea0abaabcd215",
        "Science/Teaching_Packs/GROW/Teacher_Notes.html": "06da774069ab702c62cf35aaf954dc6e5707ff95803c1fc871fc275d4fb8c84d",
        "Science/launch-engine/inject.js": "5bd8266463b277052ca7e9b8a2844c064b1213b04e424bca767e8ac336b52395",
        "Science/launch-engine/test/gate-shape.js": "b9e17c97c0f0a19efb0068595e46de4b62f6f1e2ac2bf0ba06d4ec505732b970",
        "Science/launch-engine/test/health.js": "cc599709a0e2c3c6c517331f99b9f43a4dc3a29d4dc0e3c67cd1c017159dc9d4",
        "Science/launch-engine/test/print-pack.js": "b3bc74a66cb7057dad9d5f3face9ec24028978e5b85ca0bd5d883709e529fc99",
        "Science/visual-learning/science-visual-learning.css": "94cff82726164d7b1ef7315868ff8cb51eae0bf83bcf5590c838f509ee4e1a93",
        "Science/visual-learning/science-visual-payloads.js": "3f607c6cab15c006a5ac5d74821e01f0edd60c2e081fa1bcaad531ff765a16a0",
        "BUILD_ASDAN/Autumn2_W1-W6_2026-27/SHA256SUMS.txt": "211b71462d1e9d0907f7ee6adf1d00c49622ed814fb03eb1c15713e1a3c11a06",
        "BUILD_ASDAN/Autumn2_W1-W6_2026-27/START_HERE_BUILD_ASDAN_AUT2.html": "a319d8f005c7185e5aace0adfa34ceebb9212623bb73719850cbad46deffe7a8",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W03/SCI_BUILD_A2_W03_L1.html": "47198b5c64e835bb50326c6e61f4cd6ff10c6204fef3fb4cdb0f33de207afa22",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W04/SCI_BUILD_A2_W04_L1.html": "30ff99f4ceec2ed2bad2aaadb541ffc052539aff0eb66e56986d99256d9eb556",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W05/SCI_BUILD_A2_W05_L1.html": "a8a6757de71b554698291cca8b10dba50276f4a79fc665c4e06e43f797f9e192",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W06/SCI_BUILD_A2_W06_L1.html": "60e143b2bcee5d104c72dacf06007329d2c13350a6bd9f385ffc843e3bce8904",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W07/SCI_BUILD_A2_W07_L1.html": "189a7a5c6fd2b477c67c874411288dad3ae115b8c3c55f60d6d9dfdcd2ab7648",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W03/GROW_SCI_A2_W03_P1.html": "82c23e53688a6e02714e60d1f144ff7fda4b2653dd698d51960ad21913f2aedb",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W03/GROW_SCI_A2_W03_P2.html": "a5efa1d1e31cb94e4394c34eb97bbb6cbc9a1bdda453365d0c5f0df3abe2c6e9",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W04/GROW_SCI_A2_W04_P1.html": "6040a5f9a27792868b6353888f41d3ffc6f206cb6593601d9e3295cb61fb2b18",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W04/GROW_SCI_A2_W04_P2.html": "4c935bb25ff3c869db4af221189bc3ef66328d6b4d488a84bbac366df7eba1df",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W05/GROW_SCI_A2_W05_P1.html": "648df031ee7d63f1cb2f61d33c74c8be824815fe74655b674e76d374e5d943c3",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W05/GROW_SCI_A2_W05_P2.html": "fe3b2be2d3996b8f9777c38c10883b227e827b094533d595a467abb07b1be346",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W06/GROW_SCI_A2_W06_P1.html": "f0177e264d4353005789cf1c5a98f0a3594581362f6a01825ff98492dd4c7964",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W06/GROW_SCI_A2_W06_P2.html": "f7542f233ebb09fe6dd0fe166a9816f40370a65c07c73a4fec03df6a5adf21b4",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W07/GROW_SCI_A2_W07_P1.html": "99de5b853dac71f056d0b7d46eb7f633cf95b34d602ae5631d424a9eaa76f9bb",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W07/GROW_SCI_A2_W07_P2.html": "25a5bf6e52065452b2ee82977fdcf49fe64d99da48188bc29202f92ffc79a0f3",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W02/SCI_LAUNCH_A2_W02_L1.html": "ce26617e0cb72760aa3a46cf2acbff7602062c3bff47f724c249fbd0f4de11a7",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W03/SCI_LAUNCH_A2_W03_L1.html": "f69417267d93fa078e6da47eec404cd25b4f0f8641d14cd75b56478f57188176",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W04/SCI_LAUNCH_A2_W04_L1.html": "af57b1ae86fea4f5582673482d002cf6c3805d4f9a56d51835e98453980c2b14",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W04/SCI_LAUNCH_A2_W04_L3.html": "87ea2c04c4211f29bd60cd7613380e6482345af997b0e3b8130271b0670e6967",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W05/SCI_LAUNCH_A2_W05_L1.html": "3bdb8a449e786ddf84ad0b72cfedccda408c84564bf207fd69e0026bcc0e85e2",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W05/SCI_LAUNCH_A2_W05_L2.html": "c797fa56ad692102162ac27185c4dd10a168b79f709faa7ea25ac57d995f1deb",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W05/SCI_LAUNCH_A2_W05_L3.html": "f2e98a18729eadda38e47c38c8ab22377b9c203091b78b8006eaa31415182f39",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W06/SCI_LAUNCH_A2_W06_L1.html": "5cc24a50efeb72870cd2b423038d4207373e06e0340c440e0ac201d637b7e17a",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W06/SCI_LAUNCH_A2_W06_L2.html": "7e3a55bdfb2f8f07a333fc0c49a29b9bc9eb5bb8f4f516865d1ebeb24e7ef16b",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W06/SCI_LAUNCH_A2_W06_L3.html": "0387309b3595ca299627d626c99584c0844c924408e336026db6aa74f2f95e10",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W07/SCI_LAUNCH_A2_W07_L1.html": "80e1539df3806aeb4ccc532642966e95519af50f8bb1ab3c47ed8ab8681be404",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W07/SCI_LAUNCH_A2_W07_L2.html": "6a9c14d38f571ce82f9036fd19537f1bb572195ce8821f55e992620c1b0e6545",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W07/SCI_LAUNCH_A2_W07_L3.html": "f3dea73d8d5a42eb869e71dec13b4704ed5ed59533e509b12b782d1cf5f6ba83",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W07/SCI_LAUNCH_A2_W07_L3_Pupil_Checkpoint.html": "1b808f8225ddd5b872227223fe044964dbc5ce05dbc21a41576bf5c33d09a87e",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W01/SCI_BUILD_A2_W01_L1.html": "821baf58d7f4f9bcb9429a85363953a640f3259b49e81dbba95923f5701ebfa5",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W02/SCI_BUILD_A2_W02_L1.html": "97f4d4d821849a562fd2aacb46d7f6036cd59409ecf7fb0014591825a3e7c0ce",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W02/SCI_BUILD_A2_W02_L2.html": "5fb3ecf2562e20513cce0cb09ae32e33deb52d72ff3738b30d365145cd662286",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W03/SCI_BUILD_A2_W03_L2.html": "c1fbb419a7f922ba96b4eacde22ccb004f431e49d888e1fb201b12c973e5bce5",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W04/SCI_BUILD_A2_W04_L2.html": "e072faaaa805e50895b7f618599c4aa40742480a1087d1a34f3940ce3a56df30",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W05/SCI_BUILD_A2_W05_L2.html": "bf45dcc5fdd98eb4b99701562d4b6b43b6b09187e03111813e534b946ff0c75b",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W06/SCI_BUILD_A2_W06_L2.html": "f3b5c9494d4fe986db5c3f07006a3b4d17c29b842d28d612e3fcef4143bcc644",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W07/SCI_BUILD_A2_W07_L2.html": "e2a950462459fd242cf0ef25ca647664f05cc74b9fc20d8395a3cc69a245efd5",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W01/GROW_SCI_A2_W01_P1.html": "ca038585e48cc0ec3a33d632ad6ed641ffe5576adcb81ea1f3568eb34460e4cf",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W01/GROW_SCI_A2_W01_P2.html": "06a38561bde50df3e84a242eb7b56e9a77d5d647a33b1c3e122f45a1aa24656b",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W02/GROW_SCI_A2_W02_P1.html": "fd943ad2a2a321ac42700c197b2e8cf0c548bc6dd532e5089fca7cb3cc628b4f",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W02/GROW_SCI_A2_W02_P2.html": "f3bd7d869345d75080080ccfd2c214ae7b374945f7f0b2ecad97817779be6efd",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W01/SCI_LAUNCH_A2_W01_L1.html": "0b262ec1eaf4b8c6c488a4340608b8ef5f8c091101514f5d0fe81b18dc705f8f",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W01/SCI_LAUNCH_A2_W01_L2.html": "a9820f81c66481480167e39d21c8cf30454f78452365f91cea3f15fcef9744c2",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W01/SCI_LAUNCH_A2_W01_L3.html": "61fc58cabecd3732212ab08247686208919c147f671fbebe58be52cc4d36c824",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W02/SCI_LAUNCH_A2_W02_L2.html": "dc5bf336077c0525e1b241eb20ee5fb02e19801bafb7e309eb7962df1d82a2b2",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W02/SCI_LAUNCH_A2_W02_L3.html": "3ab45d11e5588314900a3e10d182825328d6126a6d796626ddee1bc58aa37d7e",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W03/SCI_LAUNCH_A2_W03_L2.html": "786f750baaf5aec13b50034d5cc5788d3a1381f2df013a986807e8611393958d",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W03/SCI_LAUNCH_A2_W03_L3.html": "0e06110a085cef2042c04c5c22683e79a7f8b1aeaad44dc023f0896a57682141",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W04/SCI_LAUNCH_A2_W04_L2.html": "d4ff25699a01a8f3ab38def7a1bd8a520984262e6678b05041377570f3ea5cf4",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W01/HUM_BUILD_A2_W01.html": "44575fc92031940fa70e4d5c9e7675f08e26218b027d26d8b8cb866c1c6a53fb",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W01/HUM_GROW_A2_W01.html": "b94a717e04c7a7c8f523977dceedf0d911d7c6a52be53830578ef15847ebaf9c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/HUM_LAUNCH_A2_W01.html": "364925a18829969d351b55d426d8dc82213ce143051fe6d59c2df77a9512ee3f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02.html": "180cc1e9f9742bb4b1275221d780411f2b1f54fe18ce880c016973341fe4ba28",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Editable_Pack.docx": "25275fbabaee49be06c5ce561df476afd5da33ebdea6a58deb2f0d4b1e081f26",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Knowledge_Organiser.pdf": "1a588d1687c83c2b90bf3540602c15d5ec815056c6f845275e122956e60e37c1",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Pupil_Resources.pdf": "ac1d0913ee0a0420c119579c1e52127dbead1e00f69b6d5a1841fd59a13c5fc7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Slides.pptx": "c44367790ec4f45e599ba4018b993b42fd075ef1b94fdfbff6ea4d467fbdc684",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Staff_Answers.pdf": "994f4ca889b023b93443f91b6489534af97a1df42af2b6ec68fe4b8ff603bfa5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Teacher_and_Cover_Plan.pdf": "c1e21da7379f652d1540444a504a7c21ddea57b9a1fe987caff710e0fa5ca254",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Tier_Pack_Standard.pdf": "f4ab6f1f9332b7b23a6c0a51fd9bf18aaed1ae71efe98185322154c7352e6105",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Tier_Pack_Stretch.pdf": "be2f29ce6bc471461f7ded62e43ab49a9f6e53f059ddfa0a1d6afe8f0b782eb0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W02/HUM_BUILD_A2_W02_Tier_Pack_Supported.pdf": "5442f7549e0bc347c0b554d5d69f5ad3513f68816153061d1c3217a47faf0371",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03.html": "1c3eb3424245a6e4e0dd8af2eadf89d93d8d54314b9ff97bd2eed9697385b221",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Editable_Pack.docx": "417e5bb5c93a98cba9b43656707a721515b1157593ab5cf728164d17c682fb49",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Knowledge_Organiser.pdf": "2757623c185e0cbb467542238acd8424bb7b96a65f5e7e1694fc140a36785bac",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Pupil_Resources.pdf": "007ba940ed1d2690b2b47ec1fc73b8240cf5493336d41a46b2dc56574ba0644a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Slides.pptx": "b88d0f0a6dfadfb4143ebdaf1e2aca6fe05d1edce78ab8e8bd3cfaed5cf3b767",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Staff_Answers.pdf": "d02089563d2a13778378c0b03110d3af47b3fe3918c84bfb9ec3f1c6d0b03fbc",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Teacher_and_Cover_Plan.pdf": "a2f86cab5262d7f60f1604e2834271a81c44e3573fb93c4c0aca06393dcb05e7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Tier_Pack_Standard.pdf": "ab1bab710e6d1f31d99ca4e794c86a31c1aff7ad38de3410f76481ecd97595b5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Tier_Pack_Stretch.pdf": "a2272c9d7f59235f09eaf6340e5874f2c9035c0821ba7ed1dc68fce10156eb46",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W03/HUM_BUILD_A2_W03_Tier_Pack_Supported.pdf": "574943d5ca7f92bc86c66a7d2f39b28d0323b6b7c213ef68b3bfc3efac95104d",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04.html": "8464f0a9b2883f2face3a4b6a4334d85e4cfb2d965802798f096ba6e4719941a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Editable_Pack.docx": "fbeedf1282226bb4cc7ede7a23ab45fe3a4e769f9dfce23a314adeb1834c8194",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Knowledge_Organiser.pdf": "af6ae45290ff01bd3e2fb9817759c67a9d66866eb3de5adf5f6a5b42c6d060d7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Pupil_Resources.pdf": "91ea967ee7e1fd20a486c32ab7cacc93f29d3b273bec5dd98fa2fc0d5f00df5b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Slides.pptx": "128d6ce4b3032f5adc46992746e99be79d0b3895c98a88b3b65ebf60ec5899e6",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Staff_Answers.pdf": "81bd7f636811d3a26ad4059c543b76a738d23b781b9607ea7e54769f35a232c5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Teacher_and_Cover_Plan.pdf": "3803ef562160904595e8347e51607b8b39ea01103b4b4d132a117203db8ef189",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Tier_Pack_Standard.pdf": "cba3873a1319e80adeb59c0994cf6e5380976ca8dae94d796429a9b01f388137",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Tier_Pack_Stretch.pdf": "60da169e79b56f869f1d1ed8f9d52f563995ab65610a6adc408eba40621321c8",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W04/HUM_BUILD_A2_W04_Tier_Pack_Supported.pdf": "dba7a7742007230772305b2875c0518f0cdb8912b157cfdf7de025788cd2b706",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05.html": "e7479afd91f6e2210240b8023b7b7d731fb56869593b4a6feacffa7aa8ecb495",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Editable_Pack.docx": "6e22489c0ddaac69cc6d55b1b44d78d7f92beee35b15721834c5c587053fbb0b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Knowledge_Organiser.pdf": "e28d87b0980a214bfb1dbceae79a1eb8a20a9e85033ffb9ffd1e6f932400c035",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Pupil_Resources.pdf": "b54f6c964be74ad6c9120369b79be6e5c1da7d9429e8fb6764d6527c20f0b17b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Slides.pptx": "b1afb7c993d93e5175af0fb7177c5e105e17412b1641881404fca377caefce46",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Staff_Answers.pdf": "307f7576797f7c96707792844e633f8601b57f7af50a36d593bcbf07d096c4f4",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Teacher_and_Cover_Plan.pdf": "af5d4495bca5bc9ee18dc2e92b78ee1a53443673e75fb5a446a5b9c4377c7bd3",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Tier_Pack_Standard.pdf": "ffebabe65cfd7e5ad23f3e5dc25f5181793411734675bc754ae61a6a55a41b32",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Tier_Pack_Stretch.pdf": "b2b4abe5a9a8e84df0aab1b25ae05029891a04b429164c8212ff934f45d9a5ad",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W05/HUM_BUILD_A2_W05_Tier_Pack_Supported.pdf": "e50d6f1d0ca116293df770c5e33691d188c7303fbd301c18aa435a4bba4c4241",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06.html": "62de0bf05be06db319a3a84adfec39cd5fe4e381a73b8fb1cdb7376ea40571db",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Editable_Pack.docx": "7fedf1c408ae36bb55b1c384f1c72486465a39a060857ca01ad6ec2d4f6aa100",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Knowledge_Organiser.pdf": "c534072e46e0797550ebe8577cc4033cd195ce2e767754e870025edb38a01399",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Pupil_Resources.pdf": "7d6f6340a982ec4561eda7b96c6c8e3a16e661b27d941d2f5cc51ca0fca5cda5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Slides.pptx": "54d33d2ed1c55d93a0611be9fa8f4a901825309de42645e22ad7ca0f43eadf5e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Staff_Answers.pdf": "988bc157512dcfba38f9b0982ea8114658cc46409d57fd98a91048970ce3686a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Teacher_and_Cover_Plan.pdf": "b0b5460da5ad1a5ad131ff71ad302448e33ed0be2efb8643d0645be225b7f3d1",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Tier_Pack_Standard.pdf": "c22571df7bac2acfb94b0ca49b35f02b86fa1a140774d465f2373ca190a659cf",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Tier_Pack_Stretch.pdf": "2a7502d6e786a3d7c7701abc5431316e17aa823374aa076145f02895255cfdfa",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W06/HUM_BUILD_A2_W06_Tier_Pack_Supported.pdf": "73f2844535c40d96c010c4e3538acd573f727364184c90861d06180ccd27e7ba",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07.html": "76d4b885b4b8a38460508cb8cff915cd7ce94d94abe4f2ad92dc43bef7e8efdd",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Editable_Pack.docx": "c1259bd8285aa61af8be63ff341c0dba699d86d66e2500d4fad0dd9e0732dffe",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Knowledge_Organiser.pdf": "e474bfa2a8d4aa2d5943ebaed1f68d622af4eed6fab6f5adc20b72bed20d0e5a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Pupil_Resources.pdf": "cf142284275cc0405673533fe81acf7674d64af91b9dd647e3f945503f716508",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Slides.pptx": "adbface8e4e6b08cf4e756ae0cfbc03e90e7ba90cab1c8a335ef0f32fad9f89e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Staff_Answers.pdf": "7bbea8cae583eb34b386dd84b8e7ab3efdd71453f650f386403c828156a96b10",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Teacher_and_Cover_Plan.pdf": "990d04e24b32389d4850fb161b05389f2cd528a1d4fc83907d5531b80ebe9385",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Tier_Pack_Standard.pdf": "b0c206fc688aff6406a4505130901c256bd13ebaea390a12af585ddb2d8dd5da",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Tier_Pack_Stretch.pdf": "fb8cb7caa6201e5f724b1747255904260d33a425225a41737ccc3faa8de5389b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W07/HUM_BUILD_A2_W07_Tier_Pack_Supported.pdf": "22e1e02ac6132927a4de30fd45096c356e4e626ccc6cf5f709f2981a7d7fcff1",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02.html": "c16bf1960df54fba7b2ab20292b8473e7bfc1578881e0a62e0460a7661ce69ac",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Editable_Pack.docx": "9c8616028d396dd381dd40cb5f2ed5caa31d5cdff60cb5ac571ca54d840ac2a8",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Knowledge_Organiser.pdf": "e11d894fb0710de8200f397c1e3bba139438e0b4142380d89010390efad8ef78",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Pupil_Resources.pdf": "04e65335ee2aff5b053a2e5a5c53baa392e8e214b6e23ef5448103d6ad60854b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Slides.pptx": "10b1dee0ad7765961bc9bd9659343dbbcd4f739472ae9e5dd36368bd54a8a821",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Staff_Answers.pdf": "5d17f62d1bb6287fd0045bfd342ffa89f209fb640af476f2b5d8ec028599b2c0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Teacher_and_Cover_Plan.pdf": "a49a255260cc3a1d13a5d6ad395486e3e63d03a77fdc1a80a5a5787217b0df0f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Tier_Pack_Standard.pdf": "0854a64b2a71d9053b1d1276d0fdbb2d135f3502326731a3c1ffe5ca0dc5e53a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Tier_Pack_Stretch.pdf": "8f971905d3fe51819b18001107b5768f5a31d459986c7484a8a80de9fa60e2d8",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/HUM_GROW_A2_W02_Tier_Pack_Supported.pdf": "1a25730fce8c40d4644d600b2fc1f6b644ba86d04b60905649fc66b2266c9f0e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03.html": "4b9aa7f532ed3f1e8262bbad36dae5a5b0b098b58673cad4d409429b9201ee16",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Editable_Pack.docx": "a38abc17f142199a06150600624acc47c692d12be5a53399bcb82e23037f7cd3",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Knowledge_Organiser.pdf": "4290aedee7861c580abd7cd7c8341360b4eda4cf721356f29f911d88735f4fb2",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Pupil_Resources.pdf": "de040b572b0312015ff4e958eb55ee9b895c922536450cc749e7fe7c18e324dd",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Slides.pptx": "aed0952e1dc2817c500e622b20c88be74a63dc198273ea0d4303f586004a6416",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Staff_Answers.pdf": "805a8260643d2ce71733ad2379fc3c534021d1d1bb8d581d3385fe6858e20f6b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Teacher_and_Cover_Plan.pdf": "7134461a840ad3f204c5b17909a8435d62af0181f7f505f44438514b611e8792",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Tier_Pack_Standard.pdf": "07f7d96fd1e626e82448302ad2c25d3f664c07534dec0180d336bfb02366ca51",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Tier_Pack_Stretch.pdf": "4f67abe0bb98b7ce08104bb2583d6035be95dc6c6d34d2dbb61d7670f3f7b241",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/HUM_GROW_A2_W03_Tier_Pack_Supported.pdf": "dd941855a94279a977295fc076edef5e6c0c3d3e44745cff9da192bf8623b4bd",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04.html": "bea94d0e27c917f367d6b91b4aa11a580d7ab71846568629230df44a6b51543d",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Editable_Pack.docx": "1ad762e1b0fe73152a74fa4fb9097872fe934ce4619954b9f6c9df52fe96b490",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Knowledge_Organiser.pdf": "9d4fac3e4f5c1dd1099168aa5f96c1742facbb20a68c3a257b979f69a3b1c5fa",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Pupil_Resources.pdf": "0c066d3134ea93bbf40edb020d8b7cda76e7f5b3f546eebd5062865b15ebf510",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Slides.pptx": "0648d91009b519a1afcbe4a2d774ce1274f7e071fb2333438949c8fbd37374d4",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Staff_Answers.pdf": "51efeaa1bf7bc07b1b383bddf850f0b84a44231376dc3585a56a1b3812aed788",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Teacher_and_Cover_Plan.pdf": "98dcbc099a3cf76b797157220bf3b604170c138094c0d746807dac3efffce78b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Tier_Pack_Standard.pdf": "bf1065fa9faaaeeede647f18aa5e78d60336f33c5419ba96f4e53ea656ff9686",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Tier_Pack_Stretch.pdf": "79395dbf5f04aa4b8899c32df39497a7e14f0895c24c107d6531fe6be69931a5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/HUM_GROW_A2_W04_Tier_Pack_Supported.pdf": "84467ec1a5db90ece90164bad3a40bc9f43c1ad2d2ff1680725e1b15895c219e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05.html": "84240a66210a27894b2a2df4a5063a428039737031f8b64e7c8c1115d5403e3a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Editable_Pack.docx": "615b3bc588278fe048633b824fc6e2ecce796df4878becc21badd85d20be3132",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Knowledge_Organiser.pdf": "5a504a94098248e635f38420ec580ea9f50d3c5c96aa8f54deff73972a006c08",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Pupil_Resources.pdf": "adc33a9f1c0b52694fbf14773658de95e50389596a8ea5da2e5a628e7d582fff",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Slides.pptx": "a1dbc75045d9a7ceee47b02ba6f1d9d2de84e20dfe95a4f705a30ab76a9d7085",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Staff_Answers.pdf": "ebb63fe75522ba1cf9ab87ceeee5b5dc6be638b6083f8b4e2299b12b6d8c810c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Teacher_and_Cover_Plan.pdf": "e908162a4bcbabda3b5fe0311f286ae8f67e485b67d1372f5c103e90ff73d79a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Tier_Pack_Standard.pdf": "059d5fe27bf0e5b50a880a5e58988eef7df3b7b604db1c9b8cbab8096b93426d",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Tier_Pack_Stretch.pdf": "45f8bf19bc42495ce9b5900e9a4424c28463bc1cd5692631c00fd0c1fe37d10d",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/HUM_GROW_A2_W05_Tier_Pack_Supported.pdf": "a968ed41d120ca7b8880ad1cba1eb3be040dd27d9458b7f3aacf597d2a7aaeef",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06.html": "1ed9ec02ac76af4f54da52a64f9ccf934baca5858769999f47a98907065565ba",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Editable_Pack.docx": "7d92c8545391b9515421a9ed387bed22f24b04f66ba220159099bbc185a5d945",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Knowledge_Organiser.pdf": "1580dad06aa84b3d83fc10e3b9acac3c1d2a20a4f1aff42a2aca61468bdef426",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Pupil_Resources.pdf": "7c791a345e990d53007aae6934a3adf2ae1ff1b721b7bba16ca8f4fbfc8ea5c0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Slides.pptx": "d8683f0c3fcce1bd0a6a9396a0871ed84cdb8fd4d078bd82c68c4b980b61a7b2",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Staff_Answers.pdf": "0b6f22e5a6ab60b5513623f62c16ccc21fc8ea399f72a9ae6049e3210a8081aa",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Teacher_and_Cover_Plan.pdf": "9b682036718789d26eefab3c502dd2488924bbbe044dc92cdfd79dd0c2164acd",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Tier_Pack_Standard.pdf": "854b10b92ddddd6f43033244d014f5e114e59326693bd17488ed52feffccf6a3",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Tier_Pack_Stretch.pdf": "160b3c5a0b60e4876bb8ddeb2fa0c13df4790de860c67f9e2e2930d528952adb",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/HUM_GROW_A2_W06_Tier_Pack_Supported.pdf": "2399e8ae9cd9573ec9273acd876d6d086cb59e13a90e1a04de8ee6f87b662823",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07.html": "647053e1ec278d925c1a0587da5c0435b024c513ca0eda1ece3b33a3581bc406",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Editable_Pack.docx": "413b2ef7d1f76ce64911ea49156d069adeff913136a137b5abba7850cc80fd2b",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Knowledge_Organiser.pdf": "5fe435fed4b5c8b6070647f661589157b353192477b2aed18799bf17e0995bf9",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Pupil_Resources.pdf": "27bed92589c1ae013cef16ddba3832a504b3bb4eed23c1afe0385bc99ffe332f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Slides.pptx": "47d5a53077eececb99994c478cdf28835daa4fd589744d5960639edb60538bab",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Staff_Answers.pdf": "7b6620d6566d60c89aa9da3d37c79bbd4504b25083bf945c5e04d1fe236f2fdf",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Teacher_and_Cover_Plan.pdf": "4ed7450d59a8d3577b63effffa1fef7330edce775d6f7cc0e00b097465655619",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Tier_Pack_Standard.pdf": "f79955dfe35d660a6e23ea91744d59057f27f8cd6c1e3cc79d8436a5bf79f34f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Tier_Pack_Stretch.pdf": "253b98da642d3ce644ba2331922f1ae79d531afe602ca53666ea5dca79915ec9",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/HUM_GROW_A2_W07_Tier_Pack_Supported.pdf": "5860bdccee1045b0bd97b2607f6eb4e8eb8a14d250fff1302db3578ae303d8ee",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02.html": "36ed84d0fdbc6127a1d858c64893fed9e98c1c958026f59f332c33bb415863e9",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Editable_Pack.docx": "fc85f9d4bc6f2c88904eecfe699175086fb4beeca53b65e2f9bb26b1855d9386",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Knowledge_Organiser.pdf": "a5b5812ccc5c5f8cc8eb7da3f676d60dd67180126be06e2bf8d07f09a472afb0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Pupil_Resources.pdf": "7e64b26407a6c27e8fc85639b50e636d8ad4ff5b830341256f4fa23e65bb8ad2",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Slides.pptx": "63fe9f28c57104aa8ea64b1597ab133a23e12f081ec694fe0947ccfd54d2b90c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Staff_Answers.pdf": "396ad321d3b5dcea3a4dd4e595536a3b9629afc423fd033f5029b467bb626b65",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Teacher_and_Cover_Plan.pdf": "c1133979a723100b1be59f41b9748bb539393090dd524d71ec8616dcb6967369",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Tier_Pack_Standard.pdf": "a3b1b3493d3b0e7c9ab8db91026ce80476c042c4cef1bdce10043f8c12b059c0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Tier_Pack_Stretch.pdf": "ead459515eec27b7f739886db5db232899638c8649783ee55e3ebd28d7f4bcee",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/HUM_LAUNCH_A2_W02_Tier_Pack_Supported.pdf": "59380e958dccf13a601b4c5e454b36b3a7be4a0454d4c9ca0db742e20a314cc2",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03.html": "4f652ee0a0197bf4a71e16fa67a9121723eeeb696c74a3efdb2c866741f86967",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Editable_Pack.docx": "fe5b41d283a1efcc1a1847275522271dd95479d3a3e2bce7ea44b756bd607879",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Knowledge_Organiser.pdf": "c602f08e228d8eff8eb313d3bb84858e0d524aae6788564f9f7343c1130a7670",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Pupil_Resources.pdf": "545ef471dcf04a8cede458c6188d809f8eb713965e2642ddccf1b4c6da329c91",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Slides.pptx": "3e27a98dcc95de12d74fc8073b77e0b3e02ac696fe2709b25d500340f9f534fe",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Staff_Answers.pdf": "7da978d532e67ad36b8c255a293fe62b12a13f2adb4cd1ae575dfd78c74a1eff",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Teacher_and_Cover_Plan.pdf": "a890515cc21b3fcf58b88b6579a0735e5c8a85cbc4c5263dc42b9ad31dbeeedc",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Tier_Pack_Standard.pdf": "7e1e70b49493183c877c53d5e72c27af9f451d02b795a5619718670ea4eb9ca5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Tier_Pack_Stretch.pdf": "347d427004dec75ac8cc3ede0b5ed3c2183e88436b9057d288f9a99e3ced26f8",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/HUM_LAUNCH_A2_W03_Tier_Pack_Supported.pdf": "1c15fb3c294a9c65fa6761218e49f2d55cd39294631deee3e73a43e3418be0a5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04.html": "c755126c21bda7b4dedda2d1d71f6f822505aa13baa287a7c0daafdaba8c6cfb",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Editable_Pack.docx": "f2b65d3605f8b0663073f6765dfa495667e4d663b96f83bf5b6979f0ddeb1a42",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Knowledge_Organiser.pdf": "82540f13491de2d1b4110bb4ac2ccab00aa689d71bfd7d9dccad600584ee69ac",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Pupil_Resources.pdf": "4b331a9afb0e2f7919629a82f5aa09e6bada40a0b538dd9f7c7debac72351113",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Slides.pptx": "7b05eb35250627f6e510ff8c54d1adbcc2b5a53b0c4825e6074eccab7b8e19b5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Staff_Answers.pdf": "ff00a672eaf9a29dd3edea152d17affd7f406c82b54701d8107b26cf279c92a8",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Teacher_and_Cover_Plan.pdf": "d6923b203be0d3d665dd470e4995d3e09dc5578bc7b7102fc319d2833c17d0b7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Tier_Pack_Standard.pdf": "efbdabc4517d8d3a6f86cdcd9c04d9d77ac18b40c0db6ff13c6491a16c879793",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Tier_Pack_Stretch.pdf": "da13c399711ca7087ed55fe3a75309f46b43b4a7c01ddafa2a51c96625ddb0ab",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/HUM_LAUNCH_A2_W04_Tier_Pack_Supported.pdf": "eaa71eb43d0eab1e49210365782bfd99f76628f9d551e67a8581b6200207e485",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05.html": "c8efdd8dd2d8532a715099bf694ede45480ef1addaab513a474219b167dd49e0",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Editable_Pack.docx": "4f684a856eea8433054e132f908ad9ea92ff0654f0820378087106d54b43ede3",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Knowledge_Organiser.pdf": "6c3cb861d54caedf96f43ef7703aec2776d427e48eb28b9a316a2547fe748dad",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Pupil_Resources.pdf": "bf37b4023df8060306c5b5516d2ae26aa36357f3fe3b8635f4df56b3331cf51f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Slides.pptx": "a6acc289661d2e67edc827669bdbed3f452e45843a9b497944e4c558f27f053f",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Staff_Answers.pdf": "c85b94a967f64a52f7802d6100ee42b749dbd935da6b2a34f009684b2b945751",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Teacher_and_Cover_Plan.pdf": "8de8c472ea091db8f54136650a218fb5c4af72d0aab272e08b3a8689a1a265ef",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Tier_Pack_Standard.pdf": "212c01dcf75b893493dcb3638592217f2a1a142e00c9e40489f6b72dc2cd8479",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Tier_Pack_Stretch.pdf": "a9941eed1d6c3f22de8ea5a35e850ef50819b21792fe00a1af490d77cb9d007c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/HUM_LAUNCH_A2_W05_Tier_Pack_Supported.pdf": "ab4d98ce72910afdb09a6ed035e5f962c96fb725661ac62a44094182fcf43071",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06.html": "47b8a2e2393939967be36d376af7987478fead1a9fbea214ce012077bd93c596",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Editable_Pack.docx": "29e24eb8d0ed5962fb5c1ba9bca04de501d83dafa47f48ee773534ced2242700",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Knowledge_Organiser.pdf": "bb21d222f5c853ee950ee3d1d0a0e9aba651ebcdc3dd01eb8a36018268f1a4cd",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Pupil_Resources.pdf": "c2db57709f5f9b478650aea00b50e394f2e93de5831098c9fe7f550a796d763a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Slides.pptx": "f90534532f30797d47f9b6f4764b8f9676962850c959807b89a8aacc13ba7a9c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Staff_Answers.pdf": "307e2ca388f129461607332e69a2db00d5e66651b2eacec2567d8907a7009d06",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Teacher_and_Cover_Plan.pdf": "e2c2405c94ae01f893f2a42517f8ef964d32b96ce785f1012063d85bb2e10cf7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Tier_Pack_Standard.pdf": "9eed60f28e9434cfa7c2152771277ebffba79ed203c34843a41957e686b087cd",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Tier_Pack_Stretch.pdf": "7ab2c4cbbf2f1958f5a07288e0657a230b225a9ddebacf0dea9a475a4a0c8ee5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/HUM_LAUNCH_A2_W06_Tier_Pack_Supported.pdf": "53b4c0dc600a2c4ddb15830d44b2b47a049dc891f3b67b72c3a15e14569f0b29",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07.html": "97f3c9b3efa25dc58d51c73eeb142eee2fb1eec216dfdad253989174b32b7873",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Editable_Pack.docx": "ef57e0f91cfac31474f0ed7433e8c1161da466efe1a53ecece37c490eeac7edb",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Knowledge_Organiser.pdf": "abebeed33b5a9fb963f1e90512801963aef892ced75d2e87b317e894b747ce14",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Pupil_Resources.pdf": "9a0934bc29b0ba2838b4fda3f0d8fbc73563dcf5ac3622bff5eecfc22a31c350",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Slides.pptx": "220ebfc6dc5507fb8da51899202a55cbad257455b7eed5cc17e6968e7e57694c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Staff_Answers.pdf": "8e924b83c1a69f733d04c30b8f37aa74c1b62b1542c771ba44c98a5787972310",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Teacher_and_Cover_Plan.pdf": "21eb8fd2023851896b613933dd97fbe1fbca8a10a9826944ba605b5454cf9d2a",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Tier_Pack_Standard.pdf": "af898e408e963ae9c740c75bd280c676c7a304615eca43b8886cbeff21332ad5",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Tier_Pack_Stretch.pdf": "c0fa18971ddd5ca36c21365579f2ab6d44852be54deda0c3184a28fc80b12e6c",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/HUM_LAUNCH_A2_W07_Tier_Pack_Supported.pdf": "8afa4ed13f94c6588c5f681284274c3ef1fc28f279a1d2583728d461b0d826e7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_RE_A2_W01.html": "f7c53db599f5b17c1b14b3463e82b0e9b92c61db7ad6d85aa04075b1c52e3024",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02.html": "7a2d19cf92d0a4ddbb6f8d8b34221d4fab7c10657c35b982e7e7715edf55d419",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Slides.pptx": "f43ece1d91dd5380aaa9d33b22462ee39a13998267720bfdd5fa343e4676415b",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Staff_Answers.pdf": "ef0b5a4feb3d5f81019dba330340575b949c42cf89cf7e600905a41ad041d31d",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Teacher_and_Cover_Plan.pdf": "95e0ffc185a94fe9b4cf8e681af4bd3c32548e6d77d8f2493bfda0411814fe72",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Tier_Pack_Standard.pdf": "206328fac1148d2098e4d92ee8d4e4b26987e915abb8ba03bc2b4851c9078e34",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Tier_Pack_Stretch.pdf": "b00389368988e33fa5c88fa1884e1b1761a4d57079395ecbadffcec4b96b6d68",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W02/BUILD_RE_A2_W02_Tier_Pack_Supported.pdf": "0fdf35ea66b1a0bd9ef4ec495dac97ee270faab82f08adb3e988980895c2d60f",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03.html": "848e4527ded6579eb2daf2210f34941251c869761450b6aafd2a14ea46ea2fa6",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Slides.pptx": "7e4bd489a21a6ee5b9249f30df0dc3866543cbc899014d9bb8687725d0af1863",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Staff_Answers.pdf": "bcbd92a5b3287a54685218da9eeaced69ba7536925f5d405b7d3a8aabf5382cf",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Teacher_and_Cover_Plan.pdf": "18955038156c8357734c2d8ab98a54ce0f9c8b08bd1ab706d3531bd539e0aba9",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Tier_Pack_Standard.pdf": "b852ad9009ebb7dad92261ca5a97e8e63583ba82377e64ce17fa31013869af77",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Tier_Pack_Stretch.pdf": "dd903f29ce3af4b31cd4331ff01697704a65d97a209d141283823411d03c3e1f",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W03/BUILD_RE_A2_W03_Tier_Pack_Supported.pdf": "c07b407bccf9272182e9de68ec255b191bcca974c118ada47e5da67529c917d2",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04.html": "3ba78aa81fae4ccbc1f4b2bbd9751f188f05451f2968645b1d72b7b0aae6f53b",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Slides.pptx": "a26eeb76ef3a2c56462b525b4191e64dc719772e8ce34e8e4b7ce8b668cd0466",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Staff_Answers.pdf": "e0f062c148c43ec8bf94dab23dcfdfaad44dfb0a213532577840d18be310d374",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Teacher_and_Cover_Plan.pdf": "4d859ff6c077816e59b13ceb44ee81b88e831b689dd4c98ba010ba6b461b350c",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Tier_Pack_Standard.pdf": "7a4eb92fa639c6f923e00b59ed57f9012d7fa91c3c05fbc81ec4811ac7a39eee",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Tier_Pack_Stretch.pdf": "6a45a2d81f8263855c450dfc60448925d2f3a70204d14b29064c7ab141d46e7b",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W04/BUILD_RE_A2_W04_Tier_Pack_Supported.pdf": "138606d658ff10507868aa31438023ba2aff0f474b2d10c15935d4c80a9169b8",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05.html": "8737510e70f7c001b6525b995baf816295e2fde7b688526467bbf6c88f10c471",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Slides.pptx": "3aa5983ff9fc80054c43cb582cc115a3adc694aafc79b5aeceba89b20e38003b",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Staff_Answers.pdf": "f43aae9c350b295ca4334d447f9a01613e8eee57bff88433cf64e16487eb906d",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Teacher_and_Cover_Plan.pdf": "0a5d541945a0c2fddf7fb1cb142cdd824dca1fa92a050ae9b6f4126f95ac10f7",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Tier_Pack_Standard.pdf": "a8dbbe58a92039031ba4a940646e01da953a7194107b19a1928bc328bb7205ab",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Tier_Pack_Stretch.pdf": "1ab1436d012ae559f74e581e1da01f75f82bdbedd3cbb8a50d896ed210a255f0",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W05/BUILD_RE_A2_W05_Tier_Pack_Supported.pdf": "ee26bcfa8fce5e8727c3fa1ebb674b1fb736e08b5849a81514074496fa3fe597",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06.html": "30abbbc18b54e4c36f27ddc73f281965c720e08cb476f2f13fead37feb4a7274",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Slides.pptx": "b2c88d217a75c399ab3b126694705348045cb1f9a7b856324e5b01a6e8366485",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Staff_Answers.pdf": "1daf5ffbc56b1641e7cd08f86bcc74f4358bb0b61170a4c3a364f7a0d4feb1be",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Teacher_and_Cover_Plan.pdf": "07984b4f744ae8e778e01007625cddfe0141d076e80056f351428ddcfe5579c4",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Tier_Pack_Standard.pdf": "9c998ed3f70e330b45efd53bd1b31d624ae995996c3af9fa2042af7f15f44cc2",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Tier_Pack_Stretch.pdf": "b71e1d436ce96137a50ce0c8167eb0d823dc1d3f12c0cbbfde0949c7b26ea863",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W06/BUILD_RE_A2_W06_Tier_Pack_Supported.pdf": "4d1106d2ebedec624fb0a25b966c310dfe3350febe0a8b25cc330c5c44e1454b",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07.html": "0c43507a0d850a7b28f4f18594be3f92dbb97faa83aca674beeb9ec05aff3069",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Slides.pptx": "c2af1114362f4d4bcf4877a97fa6c42d67c3f024a468a0631c56aa6e5774f738",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Staff_Answers.pdf": "cc20e02272dbf71761785a3fc89c4e7f3a937304b488f05e808a85b5514c3693",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Teacher_and_Cover_Plan.pdf": "478b9f2e71573510c71ab2d7529172bf6dbb30ea79f5829148853425d74d47ae",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Tier_Pack_Standard.pdf": "9d59071a93168645e4ef9e65acd88b6f215146095136a61778050b1aa6f887cc",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Tier_Pack_Stretch.pdf": "d69920b9d85c9c4fdfd2f546b34b7a96d8e528f29173778dc3d800e053b5236d",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W07/BUILD_RE_A2_W07_Tier_Pack_Supported.pdf": "2484293692ea840e2052768a77fdf64e52b9a7c6444fbe82d7f7c7d84b26a1de",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01.html": "74905f18e01c6376ae5ca6a1bc1df6dbc6259239e67c017aab03ff8d68e8d560",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Slides.pptx": "fd1dbe13c669f9ca832154c66ec8d677825a8cb3b8e7699b122c2e18cf09617b",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Staff_Answers.pdf": "ee391231d12c907215ddbaec7b5861ade2ce3eeb90ebfa70b4fe6a14207fa6dc",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Teacher_and_Cover_Plan.pdf": "75fe6d73a6c6ec22ef3cd7e828dff28521e2c6180ba83826570f474b1c966ba1",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Tier_Pack_Standard.pdf": "93b9273b5c72db1da81a40660a8ec8b7ea3b8cdb05d92c52b1a311a512834d33",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Tier_Pack_Stretch.pdf": "64a55051d9c177c70e45193c0bf68581966dbd87504d341b07179522c5b14727",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/GROW_RE_A2_W01_Tier_Pack_Supported.pdf": "ce29335af0bd80dc2b4e382ae11c191694d9f4a2d023fc6ef1acaa6da6a0b365",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02.html": "c855ad1d60678a7a6e7bc2f3210e40b81800293a44cffefada781a1d6216749a",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Slides.pptx": "7ba446bc23d0b663e1cbd64aa7f4d341c17d5955b601279183c1b176ef41230e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Staff_Answers.pdf": "e58315da7dd88d2c67deb5244538c27e9cb3923a6508ee8ca0dfbc0a9075d13e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Teacher_and_Cover_Plan.pdf": "88a98bb7a1c20a293ca30d5eda747a15ca7453cf736fe747cb564b6b4b3e485e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Tier_Pack_Standard.pdf": "8f5736a1e0b38e1537d744b9ce64b3267476c53b2b20e64690c70962ba557ea3",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Tier_Pack_Stretch.pdf": "434447f22f137acd1d23db12c3dfa3604821c93a88974e451a125e881fea942b",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/GROW_RE_A2_W02_Tier_Pack_Supported.pdf": "4f93aa529401f46fc0ea447b226c45ce51cd236f3281996faa696f7467628411",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03.html": "bb8e7ffa749547c1be871ed280f3c462f9f23431cc18ce398f25c0f865767d6f",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Slides.pptx": "cf7b644eaaf7400f7eaae46b7010d6aeaac1b03569c8af40ee7965ef603fb4ec",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Staff_Answers.pdf": "a1b6aea987050b40469c66d3fe52501bbb2b864158d44237e0b32673b753c5cb",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Teacher_and_Cover_Plan.pdf": "9a6f3cd3082da88b9ffcfc5134f551ee6e497afa0d042106987c4ba525187ea6",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Tier_Pack_Standard.pdf": "d6dc0908fe3d20a8574681aa0320d90b6d85b1ee8922d22f4eadeb9003926f82",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Tier_Pack_Stretch.pdf": "4eb6b438d8850c42ec6e06f85df1429cdabc401862cab8ce4172687d30e67c6b",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/GROW_RE_A2_W03_Tier_Pack_Supported.pdf": "c3815089a4074d0228ad6d151e7bacab666134a8cd46ae9d889f726448c19d73",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04.html": "b46f2eb1ab59b1c31da20b12ecf5551159ae2882e4e6541a6269a7438e63eb42",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Slides.pptx": "a08aef8c204bee796576c2c8e3bb711234e315ee69e1a1428a86c21f932f631f",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Staff_Answers.pdf": "eca49f6ef48f7e228fcbd44f50534a5a756ef784e82a1f6f7595d4246bc06f67",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Teacher_and_Cover_Plan.pdf": "9a2278d5db4cbf4543d0ac9c8763ed3c499d66c6e1567c729c8eeafa7ee14f67",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Tier_Pack_Standard.pdf": "eda8fd4971aec58584cb5ca3e984dfc47e23dade328e49f0312f50fe15e84992",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Tier_Pack_Stretch.pdf": "b1c63be8914ac0da98bbb11c9e6bc661e0eaca3667793c872f8f8e0e1d7d971b",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/GROW_RE_A2_W04_Tier_Pack_Supported.pdf": "38a078cd037ecda723c511032212fe881a852b248cce377f93dcd3089b48ca76",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05.html": "66f77fdbb0ee78af3c5c5505e534b35a6bfa36947151380aefaacfa06f4a2d2e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Slides.pptx": "8f4925a8e4619d4f085daa4f017143424d722f87d5d4607720d752608f8cafbd",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Staff_Answers.pdf": "99a253f94923c58934f036e673a3fc31924f9cc2a24e81c830885e8aa1eb7f53",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Teacher_and_Cover_Plan.pdf": "2729a39dad31827417162d0b9cf5e2f3f872f4a4893021e32ced196a4da70a64",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Tier_Pack_Standard.pdf": "9684f7f6e527618efcca16ed0d845c1959c20caca83af9e94e96701ed7a4a0e6",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Tier_Pack_Stretch.pdf": "4d53983c72c4c0632b82524f125104faa5391f187ac689c019ea108222ab18e5",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/GROW_RE_A2_W05_Tier_Pack_Supported.pdf": "8c7ce30cab0a1206d14e57cf850760ed799a131185ba482ca9ba5c35bd710629",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06.html": "6a136b1fbc007b675372dc58ba47c3b29e11fc6d12a596f351853d33378aa2e1",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Slides.pptx": "6da9d01275c37c91cb18eb347d1a097c43b34947cd0fc382e584d16022a62342",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Staff_Answers.pdf": "c4a0588bec1a9555f19b963a2b70213f901318812ca03a5cd8142ac856870b33",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Teacher_and_Cover_Plan.pdf": "56558f540dac43aeb87b7a9f5181d6b98e5afbce2fb74143697235e8708f507e",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Tier_Pack_Standard.pdf": "97044e944c76b0069b23c7b1c2b5e9dc6ad8d157b242cad0416b36edd98b3961",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Tier_Pack_Stretch.pdf": "945048b8abc25804637c39e2a529816d988796a8f9bf19d5aec3bf39c60ee12b",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/GROW_RE_A2_W06_Tier_Pack_Supported.pdf": "6fa0f54319eb8cdd066a1322a5ad9708fb1b344fb38afdc16e12f959fcada26f",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07.html": "125905c3509dbdb7bd52243478a7aafc073a4c51478277a4fbd4ecdf31382844",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Slides.pptx": "267976ade5cd07f321ada0ce291f5db45f19f1a0ec1662081155d2d1a16d4a1c",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Staff_Answers.pdf": "e1989b45b571347ee594e5c31f7b31d4f5558911f99ecd30bd424cbaf33656f0",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Teacher_and_Cover_Plan.pdf": "fd0284b14676f0b95ed901aa03381e350077ae296bd989ccfa96668d74be50e3",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Tier_Pack_Standard.pdf": "4cbf0b3e339d076edb9357e6be9893b80bf76ccc3b8f594f28be1407715a2359",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Tier_Pack_Stretch.pdf": "ce400eb66b0dafa9ac9c4dd651b1018f4d3057b920ac40c31e2eb7791a4198f3",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/GROW_RE_A2_W07_Tier_Pack_Supported.pdf": "0514570715c3aea733108a2f5bf3c2d96325c6946e1569c70277a7be61b2729b",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_RE_A2_W01.html": "a7f8302c0b2be4e95b40ef20077b2d2c2b692b241bd878bd2b8f7d051ff42d5e",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/LAUNCH_RE_A2_W02.html": "e300346d7fa187f768018715d50b0ff3117d5ccb3c2821b04cd2bc6fc5ba01b3",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/LAUNCH_RE_A2_W03.html": "c8ba648736f56f08a452c1ba995ae1e22675e515c42f942a281d98157b00abf6",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/LAUNCH_RE_A2_W04.html": "f4a50651783aea575e0351a8606bbc85c8f448be8a950a1630d95c6ecde9b01e",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/LAUNCH_RE_A2_W05.html": "49b4996b426dfc7a50c9f793dd129f7ab8fbff3d0ae8f0dc827de9c88ca2db56",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/LAUNCH_RE_A2_W06.html": "14db1fc9dd7a4a6a322a744f3b38f84a180689758e759ae19f725284118d225a",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/LAUNCH_RE_A2_W07.html": "9f661c2e3526e14357022bd61f5fb0c425eb6f2df646193a3bb0e802ccea5fb5",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Careers/Build/Autumn_2_2026-27/CAREERS_BUILD_A2_W03/CAREERS_BUILD_A2_W03.html": "2444c1fe5c4e76cb074a7ad891f4f8f0348d0bc29d4433b4492e06babc885255",
        "Careers/Build/Autumn_2_2026-27/CAREERS_BUILD_A2_W04/CAREERS_BUILD_A2_W04.html": "02ef8e9a88db784198a75194db2f8fcb28ff1cbbb360da8eaec683ed58f775a6",
        "Careers/Build/Autumn_2_2026-27/CAREERS_BUILD_A2_W05/CAREERS_BUILD_A2_W05.html": "194408e5f8e8452daf94f6d7980b464b4355e25fa801761db165c72d96c82b68",
        "Careers/Build/Autumn_2_2026-27/CAREERS_BUILD_A2_W06/CAREERS_BUILD_A2_W06.html": "0d9048616b13c9e5a28adb35630a12df307274415c540857e2119bfa20623d17",
        "Careers/Build/Autumn_2_2026-27/CAREERS_BUILD_A2_W07/CAREERS_BUILD_A2_W07.html": "f211e5a5c08a70f27713bb0d89d3902802b49c9fa5f3d4813af29f952d7c560a",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W01/CAREERS_LAUNCH_A2_W01.html": "93fca8912c112f8549817eebd18683b19ab63a5cfcfb8e0ce69b8d0a77e75248",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W03/CAREERS_LAUNCH_A2_W03.html": "6829c790688f2d267bd6b455b7d2b0c9627c42b3c034b5c8ddb16c64c6fb804d",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W04/CAREERS_LAUNCH_A2_W04.html": "f3b019fcca855b28ff3605c385ab083b5dbc59cba3e799e78774341781a1a616",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W05/CAREERS_LAUNCH_A2_W05.html": "5aa38385f31487aa4e1818ec3a551c528c2cf7ea60f51f26cc9093b6341e7325",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W06/CAREERS_LAUNCH_A2_W06.html": "7770e257a62b2f5cc5d1048a19653919169893fad710ed35b7b8a5d5db92b7b4",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W07/CAREERS_LAUNCH_A2_W07.html": "4cc82c06bfdc04f8421cbe91a5aa46acecbf6488b6a20e21056eeda67a78c41f",
        "DT/Launch/Autumn_2_2026-27/DT_LAUNCH_A2_W03/DT_LAUNCH_A2_W03.html": "f8ef32f77eb23e032d6aa32d9d1e73ebcd77db473a8c1dcf3158e5e11ec22573",
        "DT/Launch/Autumn_2_2026-27/DT_LAUNCH_A2_W04/DT_LAUNCH_A2_W04.html": "9aa522b6cd97b931e55629567a13fc81e7239275956b177a1808b793e636a8c5",
        "DT/Launch/Autumn_2_2026-27/DT_LAUNCH_A2_W05/DT_LAUNCH_A2_W05.html": "596d18de11d4ce8f699f18fab233d9034a8b87c938d22a86fc5ce96da8bdac98",
        "DT/Launch/Autumn_2_2026-27/DT_LAUNCH_A2_W06/DT_LAUNCH_A2_W06.html": "b80e14cae5f39eb34e3ac28421915d8a60fa11a8648ddde436562342f96defcf",
        "DT/Launch/Autumn_2_2026-27/DT_LAUNCH_A2_W07/DT_LAUNCH_A2_W07.html": "ad86eec3b539cc3baf55985de1b2f0fea98843a7fe6361306f70a12b1c5516da",
        "PSHE/Grow/Autumn_2_2026-27/PSHE_GROW_A2_W03/PSHE_GROW_A2_W03.html": "627b480b3cc7e9366bbf1ac5f94a406ecedc0d66e68dac133dc9594406d5a67a",
        "PSHE/Grow/Autumn_2_2026-27/PSHE_GROW_A2_W04/PSHE_GROW_A2_W04.html": "296d5fbc0a9bd445d1a0fd633198674335b965e96feafff1cec0ba2f7a248947",
        "PSHE/Grow/Autumn_2_2026-27/PSHE_GROW_A2_W05/PSHE_GROW_A2_W05.html": "7f015f625c07176853143799ddf4e0f2e87494607ae11ee2219eae89f632aa18",
        "PSHE/Grow/Autumn_2_2026-27/PSHE_GROW_A2_W06/PSHE_GROW_A2_W06.html": "a918dd974d37c38d0f64446eba75885bf7791e4abe9b231b92abb4d5deab1231",
        "PSHE/Grow/Autumn_2_2026-27/PSHE_GROW_A2_W07/PSHE_GROW_A2_W07.html": "8764facf897357b07600cf958135760821d890c5cf2762abb32ce8f5099d9220",
        "RSE/Launch/Autumn_2_2026-27/RSE_LAUNCH_A2_W03/RSE_LAUNCH_A2_W03.html": "d9ce7015055de78f5c3481b5145e9b26d7bd8cecbc3037e2bdf596f4083b5bfa",
        "RSE/Launch/Autumn_2_2026-27/RSE_LAUNCH_A2_W04/RSE_LAUNCH_A2_W04.html": "1c0536bc0fdbe024acced50b62c0290dbe0c96f6978059e1b9de90b4affbaaf5",
        "RSE/Launch/Autumn_2_2026-27/RSE_LAUNCH_A2_W05/RSE_LAUNCH_A2_W05.html": "342ccfff2d2c540cfc5d4b7285849052aa6955cf76563c332cbee75a5ea8e303",
        "RSE/Launch/Autumn_2_2026-27/RSE_LAUNCH_A2_W06/RSE_LAUNCH_A2_W06.html": "608b744c1322dcde482b11b2dd69f98522e658e3d099c3269e524793e984330c",
        "RSE/Launch/Autumn_2_2026-27/RSE_LAUNCH_A2_W07/RSE_LAUNCH_A2_W07.html": "74da87e743b10e8e0130217dc17eb67ee4f07a13daa8c7de619fc90d9d70e557",
        "RSHE/Build/Autumn_2_2026-27/RSHE_BUILD_A2_W03/RSHE_BUILD_A2_W03.html": "fda05ea1d8059bb7627fed763ba9916c8b5c387e1c7407127e0d4e4734d824e5",
        "RSHE/Build/Autumn_2_2026-27/RSHE_BUILD_A2_W04/RSHE_BUILD_A2_W04.html": "581c9b35be62f7a7bb747703c24a78a1cf811ac5a9c411f58f6bcd8c1b97eb50",
        "RSHE/Build/Autumn_2_2026-27/RSHE_BUILD_A2_W05/RSHE_BUILD_A2_W05.html": "a0b5cc66e1ef551c93e44d1fb8ebc722fd47b998348721d4db40970c15ffee24",
        "RSHE/Build/Autumn_2_2026-27/RSHE_BUILD_A2_W06/RSHE_BUILD_A2_W06.html": "1f9f6dca602a949724671199ef24f713aac8e2deb6313dd0e5a0572a95a567db",
        "RSHE/Build/Autumn_2_2026-27/RSHE_BUILD_A2_W07/RSHE_BUILD_A2_W07.html": "9dc295c2c71d5dc756e067a3f70baba7cdb5c92e32b1ed98a0348350d4da2d80",
        "Vocational/Launch/Autumn_2_2026-27/VOC_LAUNCH_A2_W01/VOC_LAUNCH_A2_W01.html": "fc361f09b8222ff1a1c86e2f1f92cf7e05412243002ee0beedc976a0eacd88a3",
        "Vocational/Launch/Autumn_2_2026-27/VOC_LAUNCH_A2_W03/VOC_LAUNCH_A2_W03.html": "7e7be1b9eac3e242f58f9ea626ee560936b62fba627a07dd02064268eab54e08",
        "Vocational/Launch/Autumn_2_2026-27/VOC_LAUNCH_A2_W04/VOC_LAUNCH_A2_W04.html": "f850df99c7cd2735a7e7ab0bc2e56cf9463bac9385c43328881c6866cc8f2e3f",
        "Vocational/Launch/Autumn_2_2026-27/VOC_LAUNCH_A2_W05/VOC_LAUNCH_A2_W05.html": "6b40ef51423aa63f2d717cfe6878b625bebe12d6fa03fa30527a4c1b25cf86d5",
        "Vocational/Launch/Autumn_2_2026-27/VOC_LAUNCH_A2_W06/VOC_LAUNCH_A2_W06.html": "d0edb57221c76ffe94babf8a5c97011076bfc7a6160c766c0d9910d90052bbae",
        "Art/Build/CREATIVE_ARTS_A2_W07/Public/ART_BUILD_A2_W07_P1.html": "8200f49178ab8fe5a1faf3d4c168b27f94d29485d7e30c6c670bf198a39541cc",
        "Art/Build/CREATIVE_ARTS_A2_W07/Public/ART_BUILD_A2_W07_P1_Slides.pptx": "3a083d13099905e570b0ba7ea72199b6c30c0753d2f560890ef212fded961f7b",
        "Art/Build/CREATIVE_ARTS_A2_W07/Public/ART_BUILD_A2_W07_P2.html": "bea086cdacbc489574600034961bfad2ba8edee9d9417f590a89c98ac083196d",
        "Art/Build/CREATIVE_ARTS_A2_W07/Public/ART_BUILD_A2_W07_P2_Slides.pptx": "c00cf9ee4a416035445cca799852a5090cf82def74e83864043ac7eebe489ada",
        "Humanities/Teaching_Packs/RE_Autumn_BUILD_Reviewed/BUILD/Autumn_2/W01/BUILD_RE_A2_W01_Slides.pptx": "e73ca74c88bd617904048bb31d71a5a6ffeaa3d354722a4ab0a98af7dc1d0795",
        "Careers/Build/Autumn_2_2026-27/CAREERS_BUILD_A2_W02/CAREERS_BUILD_A2_W02.html": "3f979732df1a31989b35d27a3e0c906b0f2b91f7782214c12a3dc6ffff5ee1b6",
        "Careers/Launch/Autumn_2_2026-27/CAREERS_LAUNCH_A2_W02/CAREERS_LAUNCH_A2_W02.html": "b0f8a1fca84c020b07c5d5787c6e1fc2434314f00bf725f85258b7d912bb6f73",
        "DT/Launch/Autumn_2_2026-27/DT_LAUNCH_A2_W02/DT_LAUNCH_A2_W02.html": "39bc268d5bf744e30fe03b64fa839c7872bf8f3d399cbf01138d0528ad6f5a73",
        "Humanities/Teaching_Packs/HUM_Autumn_2_BUILD_Reviewed/BUILD/Autumn_2/W01/HUM_BUILD_A2_W01_Slides.pptx": "32cfac21858bda55f8510a4910c4b63a41c2587df395849fe46ced47f79da1ec",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W01/HUM_GROW_A2_W01_Slides.pptx": "5529590dbef12dc21b9a366f833ebe470154c8392b327746a459a93089f77f5e",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/HUM_LAUNCH_A2_W01_Slides.pptx": "7b0a83fd26bee1583892861a9ec011fdc13ef797543d2b6e881f8c669f6bbe34",
        "ICT/Teaching_Packs/GROW_Computing_Autumn2/GROW_ICT_A2_W01/Public/ICT_GROW_A2_W01.html": "668312afde4da942757a4e4fe321d8a32f103524ca105369bd88d359e53ad736",
        "ICT/Teaching_Packs/GROW_Computing_Autumn2/GROW_ICT_A2_W02/Public/ICT_GROW_A2_W02.html": "c37d0e739be43b63e8e8efa883ca1f06e82483605137d41b2d7644989ff4cec8",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W02/Public/ICT_LAUNCH_A2_W02.html": "37ca05a0919775c6019e09c5bf8c5d2116440d6fd9afc08ebd5f358aed449073",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W02/Public/ICT_LAUNCH_A2_W02_Slides.pptx": "d8a67c0c47d3048fbf7940d402a1abb2855f2c3149bbb95d20810f1deceee705",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W03/Public/ICT_LAUNCH_A2_W03.html": "c13e8c4d1d8ea78475ac934962989abca8cae942a3da73fa5d78de4d12602133",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W03/Public/ICT_LAUNCH_A2_W03_Slides.pptx": "3997dcd5d34b2c40a95860d86bd13765c9809a2e5fc7aec1fb4cb991f5ff1ac7",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W04/Public/ICT_LAUNCH_A2_W04.html": "724ea9178afbff35bf9135cfaad6ad2430c4671e2fdea3cacaedfba3a33560bc",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W04/Public/ICT_LAUNCH_A2_W04_Slides.pptx": "267644a0c019c8a45b651b42731ae0cc92e5e5e4739f11eeacdd2ee2273d4301",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W05/Public/ICT_LAUNCH_A2_W05.html": "6c55f93e1a9c2faf691b21781cc07029c7af6a59f8ef2c60d80c806ce9f51529",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W05/Public/ICT_LAUNCH_A2_W05_Slides.pptx": "7cee4843f44725d5f295bbfd6c1015e739f51ce03d37c9d141080de088dcd690",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W06/Public/ICT_LAUNCH_A2_W06.html": "25627cb5a79dc1eb6417e1711e6a90527fa196e6c537cc78624bbaa514fb8f92",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W06/Public/ICT_LAUNCH_A2_W06_Slides.pptx": "4da2dc19b567adde99b767eaaa29f6d3ae3ef361cc119c0c305e3c68276f802a",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W07/Public/ICT_LAUNCH_A2_W07.html": "c05eb43b19d3915714becf8d494c00a9af6d27e0c955d265ce475e90959691cd",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/ICT/LAUNCH_ICT_A2_W07/Public/ICT_LAUNCH_A2_W07_Slides.pptx": "0cbe4f2ad9ad221bd66821f886202b3adb9cbfae213ee64a74c6c88150e45355",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/LAUNCH_RE_A2_W01_Slides.pptx": "883d873acfaff940a4a471e89823793e872966eb6dbe3c0de76771c9d0db0681",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/LAUNCH_RE_A2_W02_Slides.pptx": "fb6428630709141ec9d59293c2b9ac810f762cefd776bcb7d0f7fc76fa5bdbce",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/LAUNCH_RE_A2_W03_Slides.pptx": "1f9c0f12321547029af91e3cd046a2a9a63f8f8da791b5d8a173702c4e8f1624",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/LAUNCH_RE_A2_W04_Slides.pptx": "bece4342df6955915da38f305272a02c71bffdb75cbb20f1c9e0e14cb8f0b54b",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/LAUNCH_RE_A2_W05_Slides.pptx": "7068503eba0d29c83b433e5e6cc5ac9a45b8f0d6cee15d7a2ca8520b77d4bdd2",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/LAUNCH_RE_A2_W06_Slides.pptx": "3888c271392353afad7818f32947a583ebac5729856cec36a649287105aba6b5",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/LAUNCH_RE_A2_W07_Slides.pptx": "8654afc9d680703587ab22f2f24674479a8bd8d599dc5f8c738bfd0954f9fffe",
        "PSHE/Grow/Autumn_2_2026-27/PSHE_GROW_A2_W02/PSHE_GROW_A2_W02.html": "790b94cb5da857bc4c568c8e25a48a635292cc96f89455cd06e2d0f2dd3c7024",
        "RSE/Launch/Autumn_2_2026-27/RSE_LAUNCH_A2_W02/RSE_LAUNCH_A2_W02.html": "3332819b3246d7f4b4b293699c40d533256f364d42794c49001c5ecbd490dc11",
        "RSHE/Build/Autumn_2_2026-27/RSHE_BUILD_A2_W02/RSHE_BUILD_A2_W02.html": "2f3c8c0bbd4e43dd07160a08bb62651e9c6c2068d5adf9872fc4897290413d56",
        "Vocational/Build/Autumn_2_2026-27/VOC_BUILD_A2_W02/VOC_BUILD_A2_W02.html": "056e556657fe2826f4f4630898013fa979271881d57529be602de4c9d2860c35",
        "Vocational/Launch/Autumn_2_2026-27/VOC_LAUNCH_A2_W02/VOC_LAUNCH_A2_W02.html": "c2b41afc4d7a8ae73b1dd76358e4a7345a3bcae4a47bdcd4f67709ea4c6f5d2b",
        "Art/Build/ART_BUILD_A2_W05_P1/Public/ART_BUILD_A2_W05_P1.html": "f772cc16bb3bdfacf7f8579c2ba497155f5e9ea261eb7e560cf4181011d96889",
        "Art/Build/ART_BUILD_A2_W05_P2/Public/ART_BUILD_A2_W05_P2.html": "1bbdcee3d37584fc1c127f0d55c41babad5cbb1d4b8bb7dd4e94b8c97a94a9c8",
        "Art/Build/ART_BUILD_A2_W06_P1/Public/ART_BUILD_A2_W06_P1.html": "0d30de93ca221c324972accac7b23dc42687216277f46d20738fa83613f0ff30",
        "Art/Build/ART_BUILD_A2_W06_P2/Public/ART_BUILD_A2_W06_P2.html": "85de859a2fde73962e4fef9eee2f7d250d36ec10a472cf803fa9ab969654a925",
        "Art/Grow/ART_GROW_A2_W05_P1/Public/ART_GROW_A2_W05_P1.html": "6f78d502dd1453b4d31675a720ea56f1cb1c7621f3508ef101a317134db81e86",
        "Art/Grow/ART_GROW_A2_W05_P2/Public/ART_GROW_A2_W05_P2.html": "f9a59b20db63711ea01fe76efe7c52b616cb6f6f4bd6c1f12fd8e2a012c37d84",
        "Art/Grow/ART_GROW_A2_W06_P1/Public/ART_GROW_A2_W06_P1.html": "02033b18655492828f8fb97efb31922f9b700f26f17ebd01ec6a08a69c93216b",
        "Art/Grow/ART_GROW_A2_W06_P2/Public/ART_GROW_A2_W06_P2.html": "9fb4444efc708ad3c09e7e306d70d02a6812a897707e7570e57f2900081c751f",
        "Art/Grow/ART_GROW_A2_W07_P1/Public/ART_GROW_A2_W07_P1.html": "878da4e77811f78aac26469ee6037b316bbfb49ad930fadd0f696ac6016423f1",
        "Art/Grow/ART_GROW_A2_W07_P2/Public/ART_GROW_A2_W07_P2.html": "99ffcd5ca3cfa9be4be8e349dd4931c484f2415005651cb2052171dea5dc77fe",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_GROW_Reviewed/GROW/Autumn_2/W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/HUM_Autumn_2_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W01/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_GROW_Reviewed/GROW/Autumn_2/W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W01/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Humanities/Teaching_Packs/RE_Autumn_LAUNCH_Reviewed/LAUNCH/Autumn_2/W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/ART_BUILD_A2_W05_P1/Public/SHA256SUMS.txt": "8c949902c0506e5e7c11f9c04cffa3aa231e40959a827faa0c8b25840f4f78c5",
        "Art/Build/ART_BUILD_A2_W05_P2/Public/SHA256SUMS.txt": "84f51a822d9f7c59fe7af387b2f17a3e05df79a3724112922cb8188f76a7af26",
        "Art/Build/ART_BUILD_A2_W06_P1/Public/SHA256SUMS.txt": "c82cb8a79e1a691229a6467ae56c8649b63746c8ab29f3ba2b9e08631879eb58",
        "Art/Build/ART_BUILD_A2_W06_P2/Public/SHA256SUMS.txt": "3f5969a885a06f21bf0df1ba21afc7a2e83c188262877ad077382536896f6d84",
        "Art/Grow/ART_GROW_A2_W05_P1/Public/SHA256SUMS.txt": "d7ffc18f5d606754ebb6d35d331342398b6b124db6f17a146c426ed1d9a34e76",
        "Art/Grow/ART_GROW_A2_W05_P2/Public/SHA256SUMS.txt": "016b0b28c80ce775f1dbd9c71c7e3e2a59fd25cbab7500b870ae054bddafb3ef",
        "Art/Grow/ART_GROW_A2_W06_P1/Public/SHA256SUMS.txt": "7559b5062cc8ff589acf787290894579f46e939d81ebaa7333286dadb0fe9c32",
        "Art/Grow/ART_GROW_A2_W06_P2/Public/SHA256SUMS.txt": "d4f05d30efb745ed4bef459249a1939b434fe582a9a31b741ee71e0f02e20af7",
        "Art/Grow/ART_GROW_A2_W07_P1/Public/SHA256SUMS.txt": "f3190791d6f5a73e8ef8b73c753066edff6aa53aad2e7e2e0ab48482698b5a4b",
        "Art/Grow/ART_GROW_A2_W07_P2/Public/SHA256SUMS.txt": "373757250fde2ef9a6f420ab074753fac342ef9086805ec991a296780656a588",
        "Careers/Build/Autumn_2_2026-27/SHA256SUMS.txt": "618e979dacd4560c082a165c2384077cf95aa9e63f6505cebe0349df1cf43cda",
        "Careers/Launch/Autumn_2_2026-27/SHA256SUMS.txt": "469d9c5f14af0cd239fba3715136413ebdeb33b04bf43157805f9a3b9e9ac2ff",
        "DT/Launch/Autumn_2_2026-27/SHA256SUMS.txt": "00672ec0d95f49fc67f72ccc7f7f1a81c510d1cf15d8b68a06e069979dc5fcd3",
        "ICT/Teaching_Packs/GROW_Computing_Autumn2/GROW_ICT_A2_W01/SHA256SUMS.txt": "d89469302bb204a0418b3293a93aff87d3b1b792f7bf95b90ff6436fdaa5df67",
        "ICT/Teaching_Packs/GROW_Computing_Autumn2/GROW_ICT_A2_W02/SHA256SUMS.txt": "9cbed4ee3757f43cce689ff77073204868819e72a494de3c21521445203044d1",
        "PSHE/Grow/Autumn_2_2026-27/SHA256SUMS.txt": "c6399ebd777032625b1da67f30d4cc022db4bfe1d525eb54ebb083727c1319ea",
        "RSE/Launch/Autumn_2_2026-27/SHA256SUMS.txt": "1184ee9703e741a6afedbd009bc3939f0bd411c27af13d80014eb0c36fae9fe7",
        "RSHE/Build/Autumn_2_2026-27/SHA256SUMS.txt": "2452ba679bb0acdcc3252b497ee9463ab47b6e70ede3693acc2d4fdd085e0a6b",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W01/SHA256SUMS.txt": "e56ed9b0ef3f2bdc8e228ad211f3a431eab2cc104f39df4a2e18602da04d8ff1",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W02/SHA256SUMS.txt": "5634dfcbf572168b5be66dc25aa1df9ccac13a1bad60982fde1c3befe2f53b79",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W03/SHA256SUMS.txt": "445266d3038e4ccc3ed37f0a8d7311d6efdec074f8aeffcba97074d74600dab5",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W04/SHA256SUMS.txt": "f51a362b38fbd23633856a439d6cb90b59093205ddf71bcf646ad9c2a1cb1f1a",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W05/SHA256SUMS.txt": "c2d9c0dd691fee93a249a88f9b4f6635340d89fee0fc0f989aa940a825d53044",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W06/SHA256SUMS.txt": "03066f7795b2960e64bc92d7f408c118277c8d927ac51e0b6922bd53b39c9315",
        "Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W07/SHA256SUMS.txt": "93c4898c1a311ee6c19e4d66b69f6f353fbee264587b12d1488e44f19a7877dd",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W01/SHA256SUMS.txt": "6c9de26b51a2cef18f30e3a68dd8cbde245e635450e0638ff1af7d9445598790",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W02/SHA256SUMS.txt": "725042b9b08c3934d9c572a42b64660c39a935a85e1dbd75fb7b7d4492b626c2",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W03/SHA256SUMS.txt": "ca3068ea0c31d1fc6d2e64628c4f43353b999b26758fbf5aff0244bd38224e7a",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W04/SHA256SUMS.txt": "299f7c929e9d74ed55d0fba265ab644cc4692d9d4781f66bd573f95e14bb910e",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W05/SHA256SUMS.txt": "30190d1c5ac7a398ffe8fcd3f733442e7c93b86100575765a2519d1d7ac7cf8d",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W06/SHA256SUMS.txt": "5c61c7fd514e58444a4aeb2b1979be63a6fd50a7d6b34d83fc4ae678072ab29a",
        "Science/Grow/Autumn_2_2026-27/GROW_SCI_A2_W07/SHA256SUMS.txt": "4ab9ed445bf8926008bb16ec9fd422173fb2473dd8ba503438fbca3e80c4de80",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W01/SHA256SUMS.txt": "0d8f8fb664eb8698e76eaed47520569fe351a8e15027803932229aa2ccada2b6",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W02/SHA256SUMS.txt": "c405981c88f1bbd00a3cd028da5ce1cbfff1e9ecfc1e9bd5d5860954329085b2",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W03/SHA256SUMS.txt": "c46bd84d63dd65c0547ef17a6dc8eb582f7b43e9de3cca5e7649165b19405e7b",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W04/SHA256SUMS.txt": "a5bb1c38ee356642623123ebad460ef8857465b0ce048e0f4f1e7bf943d97d13",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W05/SHA256SUMS.txt": "e2d0ed800af588db6e3b9fd3e355d123e74e1ddac93e495fd8ddb8c1883bb440",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W06/SHA256SUMS.txt": "1ae3805c80be3385c4ee26557738280fedeb7dec19c92fa824169ec0e344fd7e",
        "Science/Launch/Autumn_2_2026-27/SCI_LAUNCH_A2_W07/SHA256SUMS.txt": "a93030ccf4007c432cdac237ce9a693ce851507017863695f7dc5ca69653a647",
        "Vocational/Build/Autumn_2_2026-27/SHA256SUMS.txt": "2643ae91aa146e131a03d38eb89b4f452b0fbd169440b9ee501f75428e2647b2",
        "Vocational/Launch/Autumn_2_2026-27/SHA256SUMS.txt": "ed3a712eb6d8e82e342421a4504da23359a1e0a9479591493d80c4ce9d8e0fc4",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W03/SCI_BUILD_A1_W03_P1.html": "8382b7864fdda9e6d396b1a349a07580f86bdd1bbb850644bc33b11d4fc5bea7",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W03/SCI_BUILD_A1_W03_P2.html": "525193f04c55c71db0fac8be29db883eeebf3c7584ed334816149aab6daf29e5",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W04/SCI_BUILD_A1_W04_P1.html": "c0d07c2781dfb04d4fd4db46f6d8961cb1915259c244a00e767c96f6b6f24b0a",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W04/SCI_BUILD_A1_W04_P2.html": "ab1d5db5f72835e7413cd704b06e50b9dc83afd048b924f152f482c58f21072a",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W05/SCI_BUILD_A1_W05_P1.html": "e88bc3b097836a54ae640df90126453153a3f3e2a1fc854eadd0f7b9a4326db9",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W05/SCI_BUILD_A1_W05_P2.html": "dca4c70b3279bce50bb1a259991b847f50b600371875a489ce50b47419708a26",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W06/SCI_BUILD_A1_W06_P1.html": "6361a4aeb874b52e54f8aa58b82261dc4a81d2793d95a4e0cc41cf7e506d4449",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W06/SCI_BUILD_A1_W06_P2.html": "32305f635b9c6c2ac4621829b23975ea333820822ea00b1d9b7d73b0658e0e13",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W07/SCI_BUILD_A1_W07_P1.html": "d25c0a9631c61e3ba3ee0c9d8c6aaba357d4d84e74ef48010b057013f034384a",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W07/SCI_BUILD_A1_W07_P2.html": "b3ec7c513089482c7d544292e39ced8ce238c5aed2efbd27254ac9715ee597c1",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W03/GROW_SCI_A1_W03_P1.html": "7241ac487e7c7f2d89bcff966063bcda847a9b5613fba85df6a5aea7fb10a4b6",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W03/GROW_SCI_A1_W03_P2.html": "a535afab0d4733fae0dc9257f9bdb7a51cfbe3b70c7541c1b2c20f344cde53db",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W04/GROW_SCI_A1_W04_P1.html": "113dd7d5329d481846c98082c7d60825a3d880069b70346bc26ef9c0c088232d",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W04/GROW_SCI_A1_W04_P2.html": "d400431e866f825723f250c39c3716ca9803bcd94d7f09e169806d48f1b46fd5",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W05/GROW_SCI_A1_W05_P1.html": "8cf037aab4812e0869afc3e6d4299eed0410e5cda6243c2bc815e29752765321",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W05/GROW_SCI_A1_W05_P2.html": "2458c968bdb2b1d217482bfac86a78d0989aab4eaed254832a74763327c5969f",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W06/GROW_SCI_A1_W06_P1.html": "62fd0e06c18aca19844cc9332d2f9c82976b471b4433ae39b382284cb27230e4",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W06/GROW_SCI_A1_W06_P2.html": "09cb56d3e8f120b30fa8ede948beeb1dcc5f6eba74e8ac4d9866548cf9800fd6",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W07/GROW_SCI_A1_W07_P1.html": "d46469dd1abd1431ad030eb3bcc81d32bcb60bff2216b03c9d117c9863708c72",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W07/GROW_SCI_A1_W07_P2.html": "0941f44adc33ee3d466d6bef9b1034425ddc6b4a646813a078b71962f8f710f6",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W03/SCI_LAUNCH_A1_W03_L1.html": "62cef91239e568f6ee59416f74959ee113ed962cd87b98f46b7091d80c951b76",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W03/SCI_LAUNCH_A1_W03_L2.html": "3eb3cc047637bdaaf862fd551c47aff6ed5337763b15c9a6d184984535a1ffe8",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W03/SCI_LAUNCH_A1_W03_L3.html": "52965155e8e1aade87dba568cb5c9df6a06d8e2d895aa4280e23255ac78577b4",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W04/SCI_LAUNCH_A1_W04_L1.html": "030e1330eccda6dd09c977c91133444bec7ea4f3c09d701e2a3b5be186d99950",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W04/SCI_LAUNCH_A1_W04_L2.html": "e4efb4836be78c598ffab14b763481838486e4a753b3e43342a78585f8b3ea58",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W04/SCI_LAUNCH_A1_W04_L3.html": "a18bc24efd92d9e15fcb6957563617fbb5ae894be73b8318d0edfc47012dd8b9",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W05/SCI_LAUNCH_A1_W05_L1.html": "f5887f24c08139760e5e51da70a1fa9d2c46dd734bcba34232fec25636d6906f",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W05/SCI_LAUNCH_A1_W05_L2.html": "3a29379ce54d9abe9c5d20c85d06ee4bb277f1df173e3989b62d4bcfabb615ec",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W05/SCI_LAUNCH_A1_W05_L3.html": "240e637dceda5750e1118c63648016ac30579bbebd341b1f9be563f059466c33",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W06/SCI_LAUNCH_A1_W06_L1.html": "b567e903e3f56acbbbe4dd3ac41691e0c87652f5b57a196fd58a094b13628179",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W06/SCI_LAUNCH_A1_W06_L2.html": "a8c7d4814b2515666c32b9b408044de97b40c97786418f6e0108880e6eef9588",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W06/SCI_LAUNCH_A1_W06_L3.html": "231d6c051d68499780d2da97e1555e36826815ab5773d1bd0529edbc3ba3baa3",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W07/SCI_LAUNCH_A1_W07_L1.html": "0a5dc897e3f95b109503b43a2527bfe5e0e9cbb6ceeccea69d26177e0c483be8",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W07/SCI_LAUNCH_A1_W07_L2.html": "3042487370f645e78941eb7f227b83e1c7cd25dba349766399dff54637f17f90",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W07/SCI_LAUNCH_A1_W07_L3.html": "24d9085b2e9d25bc3b8e53ddcc9bfb618c838693a9b69ac4d7d4ad91445f93e4",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Build/Autumn_1_2026-27/SCI_BUILD_A1_W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Grow/Autumn_1_2026-27/GROW_SCI_A1_W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Launch/Autumn_1_2026-27/SCI_LAUNCH_A1_W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Science/Build/Autumn_1_2026-27/manifest_a1_aaa.json": "e3ad81b46033d79b6b34dc9e8e0c67722cf49b5f7612757445c9a4299d317e8c",
        "Science/Grow/Autumn_1_2026-27/manifest_a1_aaa.json": "797cfd06e0de9914fc12b0e30acbcb00d144af38116f0d6f02a99e2cea87b6b1",
        "Science/Launch/Autumn_1_2026-27/manifest_a1_aaa.json": "5174186fc3bf0f8a3e3b09e1b01e93d526dec53700fa6761b76cb1a9a133dbb7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W01/ART_BUILD_A1_W01_P1.html": "b2b85b1eed3cd0cde74cd406faa0f99cacd8b1f9b789fc5c3a86aab41b82cfb0",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W01/ART_BUILD_A1_W01_P2.html": "027aac8cee768bf892e478c8c804c059b63b6c00ed3b82c397e6225092696669",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W02/ART_BUILD_A1_W02_P1.html": "5944d0685154250a3f066ead5469d1921b0750d83b5697f954ab3959c88512e9",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W02/ART_BUILD_A1_W02_P2.html": "a763c24644952e45cdb1fcd04230f1f970e1054f19fa8da4318dcdf3aebcb39a",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W03/ART_BUILD_A1_W03_P1.html": "65adc909dd7657410913b0c5e151fea9fe9b123e04e09f7a1264467e2276bf5c",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W03/ART_BUILD_A1_W03_P2.html": "6de47c8f3769f74d101496dcec45e34aed09daab31ef95b6bb0b4c4598711164",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W04/ART_BUILD_A1_W04_P1.html": "aa26654746ad8827a346083b040cdb29922f507fb40a290d12b140ad535b320e",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W04/ART_BUILD_A1_W04_P2.html": "0f05c2876ce3e136ac61a0378cedadac56673a32e9d315d9f7191359dd82436a",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W05/ART_BUILD_A1_W05_P1.html": "edd4e3266194605f0db59639aab76615f922ee18c8d6c27d454704a5e16d573c",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W05/ART_BUILD_A1_W05_P2.html": "b0e9d4ed2ab11dbf9a190ed50fe6a2821619689e27b43b1d97ebb191cb2f687b",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W06/ART_BUILD_A1_W06_P1.html": "aaf3c11f1d1ec9e896255aec5721dc9ab5e05ebd5b73392e5994b836f4bc2970",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W06/ART_BUILD_A1_W06_P2.html": "8f9c6fd8576ca54f0e5dc3a17f9fd64df63479c1232d4165a56de14048decfb8",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W07/ART_BUILD_A1_W07_P1.html": "4841419ae78edb529073e9b0720da281d07bdafa029447bf1d512be0e75fb011",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W07/ART_BUILD_A1_W07_P2.html": "b4319facdcb92e0ce383db52aa9d93e43eb761dccdc535398ce13a80e5da2e9d",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W01/ART_GROW_A1_W01_P1.html": "1a2b471255ba8c436c398ee68dac1b1b28ad3911abe61dea3d3bf96cdf060bad",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W01/ART_GROW_A1_W01_P2.html": "70f093d1936435b34921b29897a50dd9e6e0886493dd5d22e9cea170f49210b8",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W02/ART_GROW_A1_W02_P1.html": "fa215fe51da3c9d2e7c1b06ea4935faeabb7a957a1696bb657b2f0a9cb592f22",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W02/ART_GROW_A1_W02_P2.html": "c1451b98995841a0a0bd92c909b2dd6f2641758ec6865a82451809df13d8fadd",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W03/ART_GROW_A1_W03_P1.html": "acdba2a30ffa2a4b6e9d7fe91eb9121e0892500a479139223b996dd731a838e8",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W03/ART_GROW_A1_W03_P2.html": "b894bcbfaeb604ffd369c1c99a9271877418fcec712c079668656c58bc6562df",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W04/ART_GROW_A1_W04_P1.html": "bb2e5b6b961904019903df514103a7910567f727569f7137de822236f5869f29",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W04/ART_GROW_A1_W04_P2.html": "d3be25d5887bd3d77e56158b8522a74cb6c881d972697622c5df9bee81f95742",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W05/ART_GROW_A1_W05_P1.html": "64b9b6d803138fa5e0fc606b3aba0f5c76d4fceb2ea3ce922793ad2ac06e5afb",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W05/ART_GROW_A1_W05_P2.html": "4d8c4801dd3e988fad8c5a2975e5676f2de52db67257187e7dd51a5ce9ceaf26",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W06/ART_GROW_A1_W06_P1.html": "ec92d9954af883db1e965e01f1586cee994fd211481cf013dbde59b09fca6607",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W06/ART_GROW_A1_W06_P2.html": "7010de609b2b41e85f6827cedc4871f919f5f35e309155197ba4249771501b8b",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W07/ART_GROW_A1_W07_P1.html": "105224fc6a0cb448e335c1d3b648b6423117b093b8d5ea0849fd82be7fee570a",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W07/ART_GROW_A1_W07_P2.html": "cc73118987673ddf2b026c274d60e1ae230dc31d8825cb2307dff75aa1e1efbc",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W01/ART_LAUNCH_A1_W01_P1.html": "0df90c1a601d61b062991cb9dc7a7828fa2c3d5ced1fc345856cecf3953174de",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W01/ART_LAUNCH_A1_W01_P2.html": "4793c5ce61c64e27bd3e55c7a1362aaf2ff9afb1f91d59407047ddc751c57707",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W02/ART_LAUNCH_A1_W02_P1.html": "cd2abc409b97862ef34813ad8e3e67706798f6be54ec698a6edab33487037854",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W02/ART_LAUNCH_A1_W02_P2.html": "2963771e2eeca2675855765475ca3e8685db9928428d4699d17852f39ae947a1",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W03/ART_LAUNCH_A1_W03_P1.html": "5a1a7be9682a471234ffc9ab2422f847277c6cb1368e681e38ed9e2702ce0036",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W03/ART_LAUNCH_A1_W03_P2.html": "08586b2ecc6b78a2845117154c2e636ba05f8f716d086a54c64b174260e3c6b5",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W04/ART_LAUNCH_A1_W04_P1.html": "72588eb2e4d50dc4b91a208b57b93c697aefb36145c6a9feaef51f1e8b9975ec",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W04/ART_LAUNCH_A1_W04_P2.html": "316a4b9283909f7349d947f479caa98d531ba148c0f07a16299f3439b7c5a080",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W05/ART_LAUNCH_A1_W05_P1.html": "5fbe860baf0832841a0056e33cbfab6fd09ae12c80aea1253bda23b8f3a80560",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W05/ART_LAUNCH_A1_W05_P2.html": "d9f2d6a05a39242c2f335cff67e67cd132591f92bea4dd3ff3e3f324229aa43d",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W06/ART_LAUNCH_A1_W06_P1.html": "980afc0614facc359b41e932ef1802b35e31f36e13a2a89fcca0e680bbe61fb0",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W06/ART_LAUNCH_A1_W06_P2.html": "537ce528acae8c9caf6f80b8333a5c0866aa45bcdf162da64d4038232c24aced",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W07/ART_LAUNCH_A1_W07_P1.html": "a4c34b8f5e211b277319b86fd52b1b30b72936ea9cf1548bcbbefac1c74bb538",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W07/ART_LAUNCH_A1_W07_P2.html": "59dd18a90d7e9f6d59f07e37994dbd29a3023d16b7ba2c9578c01b5b1aee500b",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W01/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/ART_BUILD_A1_W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W01/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Grow/Autumn_1_2026-27/ART_GROW_A1_W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W01/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W02/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W03/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W04/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W05/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W06/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Launch/Autumn_1_2026-27/ART_LAUNCH_A1_W07/approved-mark.jpg": "f1095531d88d17f20c7464c62887703321a0872f108d3fb78a4afc0226dac2a7",
        "Art/Build/Autumn_1_2026-27/manifest_a1_aaa.json": "0f0b7eec6daeda548c3ddef439afa5d4740a2dbe172fc45495feeefb9071fb5f",
        "Art/Grow/Autumn_1_2026-27/manifest_a1_aaa.json": "e033e3045b2ba8250e891fe287eec6784bb96156b2b0adb39886cc2fe2590885",
        "Art/Launch/Autumn_1_2026-27/manifest_a1_aaa.json": "d42816956781ac206a57e208e1aa2a736d365e36176b2c306992566e3ac4ef62",
        "2 Physics 10/L2c_Ohms_Law_PhET_Take2 (1).html": "48e12e89b4377bae06c64543bc687068c9c9fab44aeb8df5ad5492237aa63098",
        "5_6 Local Choice/Rivers/L1b_Your_River_Your_Home.html": "0214768965079f1687ab605f90f41489223201cea3d79b5301ecf99f1641c573",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W1_What_Getting_Better_Would_Look_Like.html": "b6d37613e4ec6e4f5a763b19a3038624cb704a91f24c444c6a790b83de7230a6",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W1_Where_My_Art_Is_Now.html": "11245b4fb0fa29caffae0644cc04ce39f4547da161197eeff7d2230959cd5cac",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W2_Practise_The_Skill_And_Take_One_Piece_Of_Feedback.html": "dce82e723dd0e9c92b99947c2a4f3f5effc97e2f572b140818ae90979d5c4202",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W2_Practise_The_Skill_Session_One.html": "95316c9293d5f1676a2ac9756c6772daecd16bb8425c56cbab020fbfbe44bd27",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W3_Make_The_Change_The_Feedback_Asked_For.html": "c0482fac33405a80b3d3d6393456a35b359613f7c5fd3135e5cccf2125cfbb61",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W3_What_Improved_In_My_Own_Words.html": "5dc45479fcc73639b8ac9840e9f2b849d0c3a863992d50f3ea8f1ad8eaa558c5",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W4_The_Review_Frame_Before_The_Experience.html": "4591b1a784dd62ff2ad0a4dcb43e130129ff5337415a72df6fe2bcd1b132d66e",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W4_What_An_Audience_Member_Actually_Does.html": "7292cb1172c2f8adc5422929673a4661713d9c6bf9191ed816f7aaba54086843",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W5_Choosing_A_Practitioner_And_Saying_Why.html": "685d6f6974ba4baf412b82d44f77607a29137f92d7e53ed88618af31dc6b606b",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W5_The_Experience_Captured.html": "ce1d12237b674dfa08b93b771bc5d0a5cbf6c53c3dfafc61bb8c9526620a2e9d",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W6_Plan_The_Skills_Share.html": "4c1bbfc88d66d6296afb671dd05e981c40349f48cc303231a3b281a4c6525924",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W6_Their_Practice_Career_Life_And_Work.html": "9097f254f5a9feaebe91aa47ab5672bd4004f647c08dcca73026c0210bb4379b",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W7_Deliver_The_Skills_Share.html": "00c09a4a01762699bdee57d36b2999b2b0f7edaa704f56f86a391c26e959c57e",
        "Art/BUILD_BRONZE_W1-W7_2026-27/BUILD_Art_Bronze_W7_Review_The_Share_And_Find_The_Evidence.html": "2482a9777d58e7a043098829ee8900bd951e6cfb98dac7554678a8356decd4e0",
        "Art/BUILD_BRONZE_W1-W7_2026-27/SHA256SUMS.txt": "f563ce2277f28d2984e3f8433f343ded6d7f44aa4c35166d464abfcdd186b7be",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W1_Try_Drawing_With_Line.html": "eda5830ee077316753945f543a0155feb1349c2b89a78bf1c72c833ee956078d",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W1_Use_Tone_And_Say_What_I_Learnt.html": "bd22de163381459f5132f98b176df2de42350c1be73848c81418f493c82ac387",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W2_Build_With_Folded_Paper.html": "18942cb522630ec0ff532a3d3f9e395b9e79748beca14c9d39186d3b2bf47acf",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W2_Test_A_Join_And_Compare_My_Learning.html": "b365a9d98400afa16ba9196ce3d6725829583727d40f3b21beb91d4dd58fda32",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W3_Explore_An_Artist_Through_A_Live_Activity.html": "f57ce848b80f5993dd23e65d0615f771081450c8ac3f30788f6e308a771196b5",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W3_Get_Ready_To_Explore_An_Artist_And_Organisation.html": "9d8796ea57741208ebd2ffcd2b41b00654c4a7f9a6c5465039eff0e35cf4026c",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W4_Connect_The_Artist_Organisation_And_What_I_Found.html": "57ebee57fbf059937774e21a4f8331d56918ef7d8522ee2048f3cfdad3a5c481",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W4_Explore_What_An_Arts_Organisation_Does.html": "bd6a86bffd46a6aa16ef6757f26e239018f6811f549ae9d332512afe09c70854",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W5_Choose_A_New_Artwork_To_Make.html": "832e94c049623790ddb207302aec02beca438f30b04d4bf55b6a1ae933957626",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W5_Start_Making_And_Keep_The_Process.html": "e23dc17712833de3ee66121a44c1e2761f93f4690aaa66f2eb06cf58d494ece2",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W6_Develop_The_Work_And_Record_A_Choice.html": "d896bc82737776493bf0e3bc24846f5b74665d115604544dc7de3070bc029589",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W6_Finish_The_Artwork_And_Show_Its_Making.html": "4e66bf5aaf19f2ad0fa2971ee6bc474ac9d8681d57397602c662d3ca09636578",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W7_Look_Back_And_Choose_What_To_Share.html": "e5546a8ae720c1e636b600ebb8057a17de83d7125eb506043384aa5e42abfc7a",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/BUILD_Art_Explore_W7_Share_My_Enjoyment_Or_Achievement.html": "283457c0ad3663d5a6975ed36a1f77bc3f2fece05ff22d3b099c5f064ab210f5",
        "Art/BUILD_EXPLORE_W1-W7_2026-27/SHA256SUMS.txt": "eb05eec8765b8f6603e7c64c8d09dddb8a83e4ec9e3b6d86259be567c38bd4a7",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W2_Create_An_Identity_Piece_Using_A_Chosen.html": "e7373040b4d6098126e3d108ccf7d3c54a93705e6a07a1b8585fedd01845b6de",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W3_Find_Out_About_An_Artist_Whose_Work.html": "5052e11957159d2f09da0c3d4f24dcc5953a879e211c4bfdf57b7642eb9e1658",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W4_Try_A_New_Art_Technique_And_Review.html": "763d839b24be7048a91f87c5432001bb67842eef184ca15a53176b60614164a0",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W5_Add_To_My_Arts_Log_Photo_Comment.html": "4962f10f2f16d61ef2f12fd3e89da307606ef152582623cfb9c93f9ec83cf893",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W6_Share_My_Identity_Piece_With_The_Group.html": "cc5c00c34462d60ceaaf1a61e74a6704407f8ea979f1becfa0ad4ed9605a9a17",
        "Art/BUILD_W1-W8_2026-27/BUILD_Art_W7_Reflect_On_Identity_In_My_Artwork.html": "3c5deb411613d519449707d5efc3f99e0e6092273930f498638455b3b9245e2c",
        "Art/BUILD_W1-W8_2026-27/SHA256SUMS.txt": "9ff771111d3b1f1b11142c67f20538d44d09088f29b42b601818270e500d91f4",
        "Art/Build/BUILD_ART_A2_W1_Surface_Hunt.html": "339538821248bef1ebc5d19eb72f9d40ee280b8aada9ee8eb843573b151dc5d8",
        "Art/Build/BUILD_ART_A2_W2_Arts_Inspiration.html": "158a1331ece4863131ec8958990006230104dec2963468474d66472e7908219d",
        "Art/Build/BUILD_ART_A2_W3_Stencil_Lab.html": "dbfe4cbffff8ca72d46cba25747ecab634b59a91d770bfecf942730e35a5c3ad",
        "Art/Build/BUILD_ART_A2_W4_Audience_Week.html": "e3b298017df450e360708e0f8755d957ef2b2e12ee688b594d99bdff401df054",
        "Art/Build/BUILD_ART_A2_W5_Layer_and_Combine.html": "e0e2c197e6e15df6596ece38229763de8f7be486791d26b6c16b8231a2aa052a",
        "Art/Build/BUILD_ART_A2_W6_Resolve_and_Edition.html": "2973a14fbc8e1407ff226c824e1ed93f8229fe07b931988eb37abec16c0cf564",
        "Art/Build/BUILD_ART_A2_W7_Bank_It_and_Plan_the_Teach.html": "3f6e1712608e4dc0e614a1717ed704e40b77b44e6f33bd09a20f1a73a99c5539",
        "Art/Build/BUILD_ART_W1_The_Local_Canvas.html": "4c1469b91afbbd0f91f4ee936fb8ef16e402f98023d9b220205aa5804648bd49",
        "Art/Build/BUILD_ART_W2_Artists_Makers_and_Connections.html": "8cdfc05acbe4bb70cabfc3971496c7b47db38b53b90e2e7b43fce6aead7d459e",
        "Art/Build/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html": "d8921d76e7dd442fcee49747ada2af2e3a8626cb1d692a261547a3766dd41641",
        "Art/Build/BUILD_ART_W4_Build_the_Brief.html": "c6f22439bc315bf7ced65f7330b6604bc44cd7412271bec76e654d8c755fabee",
        "Art/Build/BUILD_ART_W5_Critique_Test_and_Redirect.html": "67c6a93fcfb52906a08a55f61161d92a2e7196c3e2fbc88c597dbf4e433fa3d9",
        "Art/Build/BUILD_ART_W6_Resolve_the_Artwork.html": "25ffce048eb1e6536c1e74358dd3fe3c6df0c4af218c8f0e5ba92463ff7ba87d",
        "Art/Build/BUILD_ART_W7_Curate_the_Showcase.html": "74a3e3657da1b120b7aa73a1ca2e7d78e6db657d378f2c410f65fa0e3a8f980f",
        "Art/Build/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html": "0b83969558609f5872f3ebeecc31c58e1e7abbcd0067590e214646ef0e2e6faf",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W1_Choose_My_Arts_Challenge.html": "b9f06e3ca4f6e4c1b9c2d578b431c7bbe2229d51e92531a69e73a77846e4fc03",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W1_Make_My_Own_Action_Plan.html": "bd0443600b63e13d96cd5aa300219143b4a1bb5fc4afb9be82128dcdd2c108c9",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W2_Experience_Review_And_Share.html": "befbca9fa9c3d68bf8e646d4d660bc01b40e0893d4cc29a431aaa3343326bc8f",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W2_Try_Record_And_Refine.html": "6176d3cd399386e8f0930a7f394721ec46268b0d0e5feb49e1681c302e5c36b0",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W3_Compare_The_Reviews_And_Judge_Progress.html": "20cd83781a26bc6cda7c5ac3f0f03d97e16d2486d3456ca8d6e70e95104d0101",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W3_Meet_A_Practitioner_And_Trace_A_Path.html": "1d1c6f9f6c531e9f428fdafe1c15dcb0a07cbc0db62d9610e73e3b234e4c2a8f",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W4_Make_The_Practical_Plan.html": "32ff2cbf32e0a15fb2d7b2baf4bd979bce5ca92c260d28da2a8813f2bda3d9fd",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W4_Plan_My_Arts_Project_And_Role.html": "483532d5037f473f9fdb8c9ef3e87b5ef945c2e18cee33fd0e4dbd8f685e7a6c",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W5_Lead_The_Project_In_Action.html": "2df8edbd76ef22a703a35cbe34c05e6bcf8fc60118faa811693e7849f1f586fc",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W5_Test_The_Plan_With_The_Team.html": "aa23ee32f091a749089249b5888d81f0ba875ea4487b0c905d90db2867f85c4c",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W6_Continue_The_Project_And_Adapt.html": "52b44f9ae17b5aae2a5887938bee67c6d1bf48cdc9abec5190620b18918785a0",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W6_Work_Well_With_Others.html": "23f5cc9a09e639edce9a9b31248c058386f8e2f0336287063441f63b5c053802",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W7_Find_The_Evidence_Across_Both_Units.html": "46775c49d44b4954949f814ab6922d36d7c7f9c2338936fb116a3f5052f83f0d",
        "Art/GROW_SILVER_W1-W7_2026-27/GROW_Art_Silver_W7_Review_My_Leadership_Project.html": "d6622451167ba9f678278523afc37ab2bff08bec937b9600cef7fb77ece20eb3",
        "Art/GROW_SILVER_W1-W7_2026-27/SHA256SUMS.txt": "00d729085c819528e60c94dd18372b9ce675906d56bf498a25216aff637bfc65",
        "Art/GROW_W1-W8_2026-27/GROW_Art_W2_Develop_A_Skill_And_Record_It_In.html": "cfa7d71121af5877f5c2f5645326febeacf0305f07b8b68cd2c38830af0cf23e",
        "Art/GROW_W1-W8_2026-27/GROW_Art_W3_Plan_An_Identity_Portrait_Or_Piece.html": "92de8c588e36689b13ced1a9d6f1bddff5f33c64b5a527a0c95e95ed841b89d8",
        "Art/GROW_W1-W8_2026-27/GROW_Art_W4_Create_My_Identity_Piece_BHM_Artist_Inspiration.html": "06884d242383f324793c6a1b46429666366853daf92231c5030c7cc9657b2aaa",
        "Art/GROW_W1-W8_2026-27/GROW_Art_W5_Review_And_Improve_My_Work.html": "eda631857a571f7f68bcdf4333bb06ad9115b503cba712a6acfe317e5074d558",
        "Art/GROW_W1-W8_2026-27/SHA256SUMS.txt": "43db716f8a33de665d620bbb18dbcf5d47371e807f71567e31e473984c80e858",
        "Art/Grow/GROW_ART_W1_The_Local_Canvas.html": "eed1d9a71d198d4071e0d9c6493425e09de3d32fa28f94e6216bda8ef18964b0",
        "Art/Grow/GROW_ART_W2_Studio_Skills_and_Safe_Practice.html": "836e3bd38a4b8a59450bb339f9c864451f7f37ab35ebecbe41888aa7c9bd008f",
        "Art/Grow/GROW_ART_W3_Independent_Studio_Challenge.html": "e851fc1358736ecf820274a49b13526a126cdc83ab833c4adfc3a92ee4ab79ac",
        "Art/Grow/GROW_ART_W4_Arts_Event_Attend_Capture_and_Review.html": "259473ac3cbc1f41e4a959d4b8c2f4862a30a7e98c34ba28033d522cefbe4dfd",
        "Art/Grow/GROW_ART_W5_Practitioner_Career_and_Inspiration.html": "2da622d4b61b8968e3d7f4e0a3d6268da6fee1ac43d3750fd465eb883abb9f0a",
        "Art/Grow/GROW_ART_W6_Plan_and_Rehearse_the_Skill_Share.html": "66f35878afe642101272ec0ef47b75f8b6d562d44b038f4704e1f3db3ec4ffc3",
        "Art/Grow/GROW_ART_W7_Deliver_the_Skill_Share_and_Curate.html": "8438ef2bbd9c8717ece528d605a475d636514ec33641f66966b6fcefcc3f7fb5",
        "Art/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html": "7f02df93d266e30da34c7d2ce98d9123534c7245c024c5bd4ff81c546bc75cd3",
        "Art/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W1_Set_Arts_Development_Goals_Silver_Gold_Unit.html": "737cf7f50316007cb24c5cd06830739a0fe825a59e9bfdff2b1b22ab7f7786ab",
        "Art/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W2_Develop_A_Skill_Document_Progress.html": "8f8c067ed3a7d810dae6940e4f1f8d4528f5f8ba456774324649e1c3c67ddead",
        "Art/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W3_Research_An_Artist_Practitioner.html": "87b4dc295212b2b065d372867dad3856c1c47e4afed066665b31dcaf858ca1d8",
        "Art/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W4_Refine_Technique_With_Feedback.html": "a85a887d80a851942284cdf72468df1c1ba8c4fb49b96eadc551d9a3b0d383cb",
        "Art/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W6_Attend_Experience_An_Arts_Event.html": "94465dafdc426486c9b04f7d041abeeed66204048afde34c8dcfcac8867a9f5c",
        "Art/LAUNCH_W1-W8_2026-27/LAUNCH_Art_W7_Begin_A_Critical_Review.html": "bca00b03ca5909124623de42e2ed5a5bf81b41e8cd975bcd8917d06d8583c28c",
        "Art/LAUNCH_W1-W8_2026-27/SHA256SUMS.txt": "f8972ba9800f1b859fd0833e3faf0c71364b8bf3a722e9fd93b0fd79385088cc",
        "Art/Launch/LAUNCH_ART_W1_Frame_the_Local_Challenge.html": "cc76f69a10107a7d269eb1b4eda34637d3b600158a49a6d100f5f60d5204ce86",
        "Art/Launch/LAUNCH_ART_W2_Practice_Careers_and_Pathways.html": "cffdeb39088fa660d28019b79e3f6fa82d16ed6355de91100a16880a9e3852aa",
        "Art/Launch/LAUNCH_ART_W3_Implement_and_Critically_Develop.html": "314014b5199795c553a8469df3b787a1fa6541cc36afa8980b96f707efbed16d",
        "Art/Launch/LAUNCH_ART_W4_Arts_Experience_Attend_Analyse_and_Share.html": "f1419022f886f7810c2901bdadb6bf5ed9a8a1fab04022501430dd179a5dac93",
        "Art/Launch/LAUNCH_ART_W5_Design_the_Leadership_Project.html": "d3b6f8aac4339694478b928f5e94931be6a03341a6b00c189170fbee97282171",
        "Art/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html": "7b8f17acd721b0c9013feaf94fdc0b111f611760c355ffe2a3127b45b3c4576c",
        "Art/Launch/LAUNCH_ART_W7_Deliver_and_Curate_the_Arts_Project.html": "8b95a1523df6ce6cfb13c729ff84db5304b4e66645c07ba4c037dcda8ac1725b",
        "Art/Launch/LAUNCH_ART_W8_Review_Influence_and_Portfolio_Audit.html": "38a82dea16a6843b1f9b0381047fd439eca0524d4137753fc3aa3a7a9a23cb36",
        "BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_DUKE_W10_One_goal_useful_roles_Classic.html": "46fcaaa91a0cf236b36ce51cf75f2cb5312df0ddc96ce39dbddb6544c4ca87ba",
        "BUILD_ASDAN/Autumn2_W1-W6_2026-27/BUILD_ASDAN_A2_DUKE_W9_A_small_plan_that_helps_Classic.html": "6c1dd28733f005b239fdecb0a11aa00985bf4f8939dc6e042ecb42b49edc181c",
        "BUILD_ASDAN/Autumn2_W7_2026-27/BUILD_ASDAN_W15_Sign_It_Off_My_Evidence_Folder.html": "ebde53783a50a0c09f735a0007f90467a3853de08c5dadcb79e745f1b1e237c8",
        "BUILD_ASDAN/Autumn2_W7_2026-27/SHA256SUMS.txt": "43694b597dbb96ddc093be0d192fb3e64b8ce63752bc4edfa0a9892377017197",
        "BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html": "a7015886e35b94e947bd3c43885773f61001518aa8c2f7ec5b0e7d69aeaf1055",
        "BUILD_ASDAN/Careers/CAREERS_W2_Jobs_in_My_Community.html": "ed23aaa51f21bc4fe93231eee6a887500344fbb1f8ed48719f11124b2533f46e",
        "BUILD_ASDAN/Careers/CAREERS_W3_Skills_Employers_Want.html": "0278c3561b8649ef3a868fd1ad6270940d49f53633ae87293ff6c0f5794c957c",
        "BUILD_ASDAN/Careers/CAREERS_W4_Routines_and_Reliability.html": "6cf196cb6c7995433743c9bae1fcf83ddc6067ae07890c782d75ecb8bb886355",
        "BUILD_ASDAN/Careers/CAREERS_W5_Applying_Myself.html": "4f9e595fc7823ab0334dac07a9ecc5d34f1695ae52cec1d23464484b88aa9aa1",
        "BUILD_ASDAN/Careers/CAREERS_W6_My_Career_Profile.html": "98d9f77a73d66d4ce7f298545057138e3dc2b392596cb5f20ae2ed1594604121",
        "BUILD_ASDAN/Careers/CAREERS_W7_After_Year_11.html": "04829ce9eddb6eb3052301bd369dfae32b2d911229e43fc32346582af06af344",
        "BUILD_ASDAN/Community_Project/COMM_W1_Choose_Our_Asset.html": "47cb7636584674851ef1f5e8b7c1c240428759c17c612a3f138fea0c65c638f9",
        "BUILD_ASDAN/Community_Project/COMM_W2_The_Site's_Need.html": "47cb2f375afd7e5f67c62c7ed044056364c8303309f65ba04eda57fd09c265e8",
        "BUILD_ASDAN/Community_Project/COMM_W3_Our_Team_Roles.html": "18fb5fa01e9b94b6807ca01387cced48b45780796279cd3ef37b9f4cb038e42c",
        "BUILD_ASDAN/Community_Project/COMM_W4_Partner_Update.html": "6634080a9430bc9fe3dc7a0861b53be4c478c3cedc8fa096dad447ff4212b7e1",
        "BUILD_ASDAN/Community_Project/COMM_W5_Plan_the_Handover.html": "95e4769ae08ee41470e773ae5ae47c290706299fe6118feab36a391d9bbfffdf",
        "BUILD_ASDAN/Community_Project/COMM_W6_The_Handover_and_Its_Benefit.html": "5d2d3f54725932e76536fc523ee22427d9257d7a5074d79b2d56ac1130fd7d5e",
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W1_Choose_My_Challenges.html": "4d296809d008c7fa3b1f3c3cf3e9561e494c81aec467feed94b63dfef1b9eefb",
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W2_A_Kindness_Challenge.html": "a17fe7ff8b69c1bc0e00c193369ead3e6f7124dd2ddaac2fc4715726419715ac",
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W3_An_Eco_Challenge.html": "92dbef1c03c79238188c3c6fa09703a0b20b116012e297832c6aeb1bae44bc0c",
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W4_An_Independence_Challenge.html": "b3c64ea848bbfdeb7b7fc943925f686f6b57350ba165be3676dcbc211b17d44d",
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W5_Our_Social_Enterprise.html": "7a1c42a4d8ddeb22c7b2f37200ff496e3e3a32b05dacd622eb039eefb004bfa3",
        "BUILD_ASDAN/Duke_and_Enterprise/DUKE_W6_Pitch_and_Reflect.html": "8d61419b18ef9a70541fc562724cdb6ca3e99f08dd68d0c5215371ebc406ef3a",
        "BUILD_ASDAN/FoodWise/BUILD_FOOD_W1.html": "dd03a6bf9ae896637fc53d87173ce1a67e23b98b6302e7750539811d4d6671ec",
        "BUILD_ASDAN/FoodWise/BUILD_FOOD_W2.html": "5460f97250d8acedb2d46306bf5f734d08042cc609581cdbf722dcb7d7cbcacd",
        "BUILD_ASDAN/FoodWise/BUILD_FOOD_W3.html": "658baa0398338745686ba7bce339796221e463c80386dd39b263e5c8ba37a030",
        "BUILD_ASDAN/FoodWise/BUILD_FOOD_W4.html": "643bbb06469430f498c8e9b841e5f5c2cbfaebe2cc79321ce0c741b087f72136",
        "BUILD_ASDAN/FoodWise/BUILD_FOOD_W5.html": "631b4db47a510a9fa261f904777e3f7cea666dc3abcd89d3f0daadb9056c97fb",
        "BUILD_ASDAN/FoodWise/BUILD_FOOD_W6.html": "cc7b40a6dca208eb8bb10ff121f53a9b228c52a5bb9823df2a7cfa6a0980e1f9",
        "BUILD_ASDAN/FoodWise/FW_W1_Food_Groups.html": "9e3cb1125eebb5465f76ecf7491261c57a9e0dbe27474a7cf82ca4a061351589",
        "BUILD_ASDAN/FoodWise/FW_W2_A_Balanced_Plate.html": "356b7328fe54d8424af7660158a62a1698192a68bd7a7c09b12e314fb47bf148",
        "BUILD_ASDAN/FoodWise/FW_W3_Reading_Labels.html": "50240e24e8203b1703c7dd02136b24fe335d3f9390261081b825195b180f3dd5",
        "BUILD_ASDAN/FoodWise/FW_W4_Kitchen_Hygiene_and_Safety.html": "60b132b246432cf2f10caf35c5d0ed3d4dc48dd67fc7bf292f7d86ea6b7fcadb",
        "BUILD_ASDAN/FoodWise/FW_W5_Prepare_a_Healthy_Snack.html": "78dacdaf36b7f2f8060fc3f1863294e318a3762b9f034e90514d58243b1b44c9",
        "BUILD_ASDAN/FoodWise/FW_W6_Plan_a_Healthy_Meal.html": "204abea669a016088af3269eb9282e984e3db032fc464e3d33e1699b0355e067",
        "BUILD_ASDAN/Living_Independently/LI_W1_Where_Money_Comes_From.html": "0ca5b00b80221da09991d73aa9d9b7badc1d1e24d1e2850e8e21a841463fd2d9",
        "BUILD_ASDAN/Living_Independently/LI_W2_Notes_and_Coins.html": "886e533da2ca72fc42eed272c5aaf5e783fe89c3dcd728aeedf004c1fe03c3c6",
        "BUILD_ASDAN/Living_Independently/LI_W3_Needs_vs_Wants.html": "5f63edcbb931d979eca0231a9f24ad5313ce0f72ff14db7b7a17e8a6d0a57784",
        "BUILD_ASDAN/Living_Independently/LI_W4_Everyday_Prices.html": "b530374f41379c02aa6b658410f63a7031e8677b3ab29671a270877bbdefa6a6",
        "BUILD_ASDAN/Living_Independently/LI_W5_A_Simple_Budget.html": "d2c61c449af3bcbcfee095c9dda68bc55581ae01162cb93c243e6db06c00e450",
        "BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html": "daa343304309e08a6d0c2f52135186dd321986ca8a75c1d0565d174c2309daa5",
        "BUILD_Estate_v3/Art/BUILD_ART_W1_The_Local_Canvas.html": "2478abfddf370b9bafba32cad43aa6ca8434106fbe8b2b5a91d78aa13ccf9ae3",
        "BUILD_Estate_v3/Art/BUILD_ART_W2_Artists_Makers_and_Connections.html": "d9b144ec87235539e79cc10e5dbe5c79c809a625fac7dc476f4db6c662a74b2e",
        "BUILD_Estate_v3/Art/BUILD_ART_W3_Industrial_Surface_Skills_Lab.html": "49fb2a1f36c24a285cd0f96c1083feec418e0a39b3859a00aab95ef0c1eebf72",
        "BUILD_Estate_v3/Art/BUILD_ART_W4_Build_the_Brief.html": "072939da128032dc05cf30596cbc0e184445713e026910c158ff6ebfdaf2c052",
        "BUILD_Estate_v3/Art/BUILD_ART_W5_Critique_Test_and_Redirect.html": "ea8eceac8755d902afad0e036b9572ea18af816714b0c339e7cef11991d388db",
        "BUILD_Estate_v3/Art/BUILD_ART_W6_Resolve_the_Artwork.html": "5f37e23a7d589faa61ead44e6311234fbf767c219004652e49f8b6a7f66aa85d",
        "BUILD_Estate_v3/Art/BUILD_ART_W7_Curate_the_Showcase.html": "e2b469df7aed0e7bbcc05255bff8eff4cce5bf50ff93c9dd7913dba127dcaa79",
        "BUILD_Estate_v3/Art/BUILD_ART_W8_Share_Reflect_and_Close_the_Loop.html": "684307184a417654b84b52dd36386b8a3cea591db27e7f2e1e3fc074067f0ec0",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W1_My_Strengths.html": "a8af660c54cf06b896d8082908f713999796487874267d301b2169a20916530f",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W2_Jobs_in_My_Community.html": "99f96b1215743a8b25288e63053d3ccfe62eae16fded1c5809b5b2e145002bd1",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W3_Skills_Employers_Want.html": "b014ab4322250aa95d36866f4e387b24a1b34cd0f2d4477fe348155e89279eec",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W4_Routines_Reliability.html": "52675f9d55b194c3838c6aa162ddeaba7dc734da5ddd90c5a8287d982727cfbd",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W5_Applying_Myself.html": "f01864f270347f4e6b6a2436acd1dae4c7a4c5ef756ce172bdb1458c0bb5f6c1",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W6_What_Happens_After_Year_11.html": "df7bff5002732a9e9430f0619258d37d7289ba4d87d7e7a1b01e03bf43ac54a5",
        "BUILD_Estate_v3/BUILD_ASDAN/CAREERS_W7_My_Career_Profile.html": "7fd31a039b46d667d11fcdf0766928ef242e05880a447e02f5feb1e04c904c1e",
        "BUILD_Estate_v3/BUILD_ASDAN/COMM_W1_Choose_Our_Asset.html": "4d342cc528027cd1f609abf86d1f001333b8a41d0625294fdd6ae5c6fd88e0a5",
        "BUILD_Estate_v3/BUILD_ASDAN/COMM_W2_The_Site_s_Need.html": "aa4835138e6e518434be034a7575b457ac53ee3eb9634ae8aa9685c06a2ec250",
        "BUILD_Estate_v3/BUILD_ASDAN/COMM_W3_Our_Team_Roles.html": "942bc19afc6c9c3da8b6627bb08083605ed99f9b4bc3a1f7dca09cc3b6b80f63",
        "BUILD_Estate_v3/BUILD_ASDAN/COMM_W4_Partner_Update.html": "f0270edc82117eb56863ce2ff9d712f209d05ee1991f324631c7dce573d10022",
        "BUILD_Estate_v3/BUILD_ASDAN/COMM_W5_Plan_the_Handover.html": "b0d1655bac16d08c589d3181bc8d149e3c28f2aa842be86e358bc4bf971e26d3",
        "BUILD_Estate_v3/BUILD_ASDAN/COMM_W6_The_Handover_Its_Benefit.html": "5ed12b57b3b7f74905dc0b4649c31e0c7f58e56396b47d7930aa4561efdb169c",
        "BUILD_Estate_v3/BUILD_ASDAN/DUKE_W1_Choose_My_Challenges.html": "b4282bcd5f26950d031df8a0cc97ccca36693315dda0bd7edd9fd03c157b7238",
        "BUILD_Estate_v3/BUILD_ASDAN/DUKE_W2_A_Kindness_Challenge.html": "842039c3f30da0e618d81f6e5117915023c8348935bc49e4788b5316962ba966",
        "BUILD_Estate_v3/BUILD_ASDAN/DUKE_W3_An_Eco_Challenge.html": "3d808d368e9abcd097f591d9850ea0e5c35577a0fd18b7b70925a47afc943e4f",
        "BUILD_Estate_v3/BUILD_ASDAN/DUKE_W4_An_Independence_Challenge.html": "c845f7b278164adbdfc1ab13bac4a8eede7ac219691d9f9d43b9854255665a1e",
        "BUILD_Estate_v3/BUILD_ASDAN/DUKE_W5_Our_Social_Enterprise.html": "fd3f93ad7ae601c8e18f15472468627365ed4b98c2ab45878c23383a633114e0",
        "BUILD_Estate_v3/BUILD_ASDAN/DUKE_W6_Pitch_Reflect.html": "109c5abc7e9fe67b02238e6351ad6fc1ef4bf6dc211f334d256b2164c2a40629",
        "BUILD_Estate_v3/BUILD_ASDAN/FW_W1_Food_Groups.html": "0c9cf1c95b1a7ec7ca734043bb78a5956aab4c9ace0ab29686795f8ee6f29cb1",
        "BUILD_Estate_v3/BUILD_ASDAN/FW_W2_A_Balanced_Plate.html": "8a50cab2a310fea98c5b16707c5f8b7bd014f2cc1e004feba900fa860b0e6923",
        "BUILD_Estate_v3/BUILD_ASDAN/FW_W3_Reading_Labels.html": "771768f1f48aae7144e6a452c7cb65f318f43b5108615de17514d1fb8e5de9b3",
        "BUILD_Estate_v3/BUILD_ASDAN/FW_W4_Kitchen_Hygiene_Safety.html": "52f8b9e57b0ac237c085a3edcfc23efa51ecacf65d9f260bc38c3d2e4d84fc4e",
        "BUILD_Estate_v3/BUILD_ASDAN/FW_W5_Prepare_a_Healthy_Snack.html": "2a253138706fdc3b19bdaf697d4a0dacc234e7421dfdc8fa3d24b7c4f2c4cb13",
        "BUILD_Estate_v3/BUILD_ASDAN/FW_W6_Plan_a_Healthy_Meal.html": "8b4088dd96626775bb7701c53807d9f03ea0058f0f162aef7f675262f4391e4c",
        "BUILD_Estate_v3/BUILD_ASDAN/LI_W1_Where_Money_Comes_From.html": "2d3f3cffa1ee563db2abcb2b607bcb6de205b0ecf9cff47d4b53ea0534399a88",
        "BUILD_Estate_v3/BUILD_ASDAN/LI_W2_Notes_Coins.html": "51bb0e05037cee9e3d3511e897ae510f90eb462a024bab8222450fd14de7857a",
        "BUILD_Estate_v3/BUILD_ASDAN/LI_W3_Needs_vs_Wants.html": "22813f546c3b35b7d4775767bd7c5a81569f0e5387a72df7b00df4c6c90b3fcc",
        "BUILD_Estate_v3/BUILD_ASDAN/LI_W4_Everyday_Prices.html": "527e864b10b1df40d490191afee316c04fc5166e40b7b8c7e07312681f1808dc",
        "BUILD_Estate_v3/BUILD_ASDAN/LI_W5_A_Simple_Budget.html": "cda8e89c8c0c65a0fc36d2871e65d08c4388933e388837ac9013c1bc5f258799",
        "BUILD_Estate_v3/BUILD_ASDAN/LI_W6_Shopping_Change.html": "239416b1eb09279ea266a3314887d48e8b6d7f40e8f7d0d490ea4f94f8dc42fe",
        "BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W1_The_Workshop_Audit.html": "89bb09f789c7f6b5847db969dbad23bcabc520160589c86e4edfc2b108d523c9",
        "BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W2_The_Blueprint.html": "b7e95a0ba1980cab8c2a5013e00f11ab6c1eb62308c9ebf1f9c26ebe0d7beb20",
        "BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W3_The_Core_Cut.html": "715b7e2a520f19661be427dea0c6aaca8307cfb05102fe6f6a84426cb22b82a0",
        "BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W4_The_Assembly.html": "a03bc7f14204b10247d9c86311a2f44df9fbe87b19bb65dc240dc7725dd4bbf1",
        "BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W5_The_Finish.html": "61339d4d76243a85646fe5113033905e865f043c6b3f01d09f5d939ee4ea0808",
        "BUILD_Estate_v3/DT_Community_Upcycling/BUILD_DT_W6_The_Handover.html": "8252280327d868403f92bdd8ac07eecb9389f399f55cc9bc8b8dc87a1c526d8e",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W1_The_Big_Timeline.html": "ee20c6d3e540314d1cc7e6b03f77a2a04ab83135d1fa5d57a27d835a95e4c5f3",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W2_History_Detectives.html": "de737833294c076f637e11eb43b36c1fa1a066c1ccb3380d73ea77a5766c021f",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W3_Why_People_Came.html": "671f602c8e82af222674ed7ee796f9700e91a87fad6e132775e069e15bf6e5d4",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W4_People_Who_Shaped_Britain.html": "add48d393a92db417950adb23ff2d4ca0a65a96b08cacb3ae82397496aed2a39",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W5_Big_Deal_or_Small_Deal.html": "b64ba834549fd0860f26863444ac1d2cb902d05f10a6e02e2dbc29cb5199b9ec",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W6_Plan_the_Story.html": "a4c713f26871444824c980602c1ec0638e2899f30595c382e6e7846da6afc36a",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W7_Tell_the_Story.html": "1e8793e2343a7a964f112b3694932c44168c30bbe0489d69c4c2ad785bb174fb",
        "BUILD_Estate_v3/Humanities/BUILD_HUM_W8_Where_in_the_World.html": "4d959e0f2e928f15e730d953349f134f48e9cad795eb54247aed37fb5f994092",
        "Build/Slideshows/BUILD_ART_W10_Our_four_beat_part_Classic.html": "dedc3b9c6c90fdc809fe9fc07e45ef14759ace2d5b213f8818eb10e55f8dadfe",
        "Build/Slideshows/BUILD_ART_W1_Technique_Tasters.html": "3eb545b867c94f94785e68c84cd792f86b132ed4f4e6df319399f43e281a8e7e",
        "Build/Slideshows/BUILD_ART_W2_Level_It_Up.html": "92c286ff4f7dbd47da217d1c4cc1b77a3b9b3d8c1424dd25b966145bf266af5d",
        "Build/Slideshows/BUILD_ART_W3_Plan_This_Is_Me.html": "f0eaf07e8f6a06873e7b2ebbc97d45b66031702b136cf9e3bb9f4aca8700ae67",
        "Build/Slideshows/BUILD_ART_W4_Make_It.html": "9b9eb4c5fc775e116989c3c9396361f9ab4d17f159562ffb48c8b2ff6bd7e9a9",
        "Build/Slideshows/BUILD_ART_W5_Star_And_A_Step.html": "134fbef7f7003a8599631c8c517f4d1a95923f48f0694a52aa8887b606f47955",
        "Build/Slideshows/BUILD_ART_W6_Meet_An_Artist.html": "bca57799ac368d9c965c89211e986a43907971227c2c2031ad8183ec5eb6b5dc",
        "Build/Slideshows/BUILD_ART_W7_Show_And_Tell.html": "267f2a1b2b93a55cc9d9bb9d2e2a3a27a9aaa05b3db2b316e4f5750cc1c31088",
        "Build/Slideshows/BUILD_ART_W8_Festival_Sounds.html": "4fa0bf3df82189484ed5332a3efd003a14e7f4fc61b28c600fc3c484c532ba3b",
        "Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html": "f644499d2d88e0cdcafc1446777a0863ccac9a5647b92a1570a349a7d26a2577",
        "Build/Slideshows/BUILD_DT_W2_Blueprint.html": "220055ac9eedd03817781991eeff522e4e4d1f5ae6982af7746a3cd9fa4aa4d0",
        "Build/Slideshows/BUILD_DT_W3_Core_Cut.html": "3d50dc1d3150ce7a49ec34c61228984bd4531cee02f36c00897530b3932ab5f7",
        "Build/Slideshows/BUILD_DT_W4_Assembly.html": "fbacb7e58dec2f0c6a417b39334c9e3db41ebf1b6aa6eec597c7ed20a7e0fab6",
        "Build/Slideshows/BUILD_DT_W5_Finish.html": "bee2f3868975ca3949f47863c8b56524daa4939577e154545ebc148ca67c2327",
        "Build/Slideshows/BUILD_DT_W6_Handover.html": "2ab35c0e6b7066b61c0e2d3ef1fbc9e0436ce97dc5fb43854172a65a1d725175",
        "Build/Slideshows/BUILD_HUM_W1_Human_Timeline.html": "7acad9746dfb118c847a692476f0c2ef95cff2e4257b444cbf1b1279a1d49430",
        "Build/Slideshows/BUILD_HUM_W2_History_Detectives.html": "29d1062db8a3aebf783244030043e6abdb9dbf60e33274570e9323016e95dc67",
        "Build/Slideshows/BUILD_HUM_W3_Why_People_Came.html": "3f1cbd578e1f064e4189187ce43e15b882705622ae5cfdd9f9bc3532ac75dbe6",
        "Build/Slideshows/BUILD_HUM_W4_People_Who_Shaped_Britain.html": "cbcc9742ba61a90424e7bd752dfa85417bb1b7771dbf3c246403d55a333a4ce8",
        "Build/Slideshows/BUILD_HUM_W5_Big_Deal.html": "a60e1441fa99c0c3e827ec12e312af16f8aa80f75727545926adbf55bf56ad81",
        "Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html": "47f66c1a32d649383c0f924bfbe340c1b70bfb27e71f1e6c10e75b4b4ceea509",
        "Build/Slideshows/BUILD_HUM_W7_Tell_The_Story.html": "5a3d2b3ea75dd6e97af1a51f119ff99a97f633e1bc9fcecd0be22af4276d2641",
        "Build/Slideshows/BUILD_HUM_W8_Where_In_The_World.html": "f3ca1261801d914f67c371fe06d44d323c73136603a01bea4e00109361d81842",
        "GROW_ASDAN/Autumn1_W1_2026-27/GROW_ASDAN_W1_Choose_My_Young_Duke_Challenge.html": "4902997542c55498174b5ccc38385039b0398d260627ae4686dc0b0085fd51f3",
        "GROW_ASDAN/Autumn1_W1_2026-27/SHA256SUMS.txt": "0630adbbe081f0f295733efc7e12a4bce95a9d94e8e11b8dd1f182d9e7cd42f6",
        "GROW_ASDAN/Autumn1_W7_2026-27/GROW_ASDAN_W7_A_Visitor_And_The_Evidence_We_Keep.html": "728d13783265910ef07bc92f0293fee6fb3dc2ded326902b759f3e554f99fb7a",
        "GROW_ASDAN/Autumn1_W7_2026-27/SHA256SUMS.txt": "03edc4c79f0dc417af50c8fad64163ba1fddb2222d51d579e7d193057bd1c3d1",
        "GROW_ASDAN/Autumn2_W1-W6_2026-27/ENT_A2_W10_Plan_the_kit_station_Classic.html": "f311cec9a834ccf05ee8b6ff6dc08bf39aa527867fbf9a1581df0a47d82ddc8a",
        "GROW_ASDAN/Autumn2_W1-W6_2026-27/ENT_A2_W9_Choose_an_idea_from_evidence_Classic.html": "0482844d7bbdd759e13d54ee0545571692a1d6c97b86d630028aedc95b24f373",
        "GROW_ASDAN/Autumn2_W1-W6_2026-27/manifest.json": "fd86f43426d9d6f9996c5f04cac590cb0a927682c1d9d845cadaf9f38860632f",
        "GROW_ASDAN/Autumn2_W7_2026-27/GROW_ASDAN_W15_Bank_It_Young_Duke_And_The_Team.html": "1adbb1b12ac51ea494bb94b09053c427a8c2a13b89abde83de94ae0f4e7f8eb7",
        "GROW_ASDAN/Community_Project/GCOMM_W1_Our_Patch_Our_Say.html": "f61e5155feb0bbbf5035a3b054e799883b2179727cb3010d63ec3c83d6ee6c54",
        "GROW_ASDAN/Community_Project/GCOMM_W2_Choose_The_Need.html": "b4ee9929ff5f131f0b875cd9912514bda5475ef57025ad5f1a2a37ff038df09b",
        "GROW_ASDAN/Community_Project/GCOMM_W3_Roles_Steps_Resources.html": "f0ed0390959e2302bee83e56faf37e24271f320e8e15c2ec23c007bfa1c56d94",
        "GROW_ASDAN/Community_Project/GCOMM_W4_First_Contact.html": "ecf36ddcb4cc8558cfe4b69d0b831f29b7a668f4aee0b66f6075f60cb19ef203",
        "GROW_ASDAN/Community_Project/GCOMM_W5_Risk_And_Ready.html": "4cba1e403f5382bceaed8680e6d26c1b963b66f21684abda14c826085dae3f16",
        "GROW_ASDAN/Community_Project/GCOMM_W6_Green_Light.html": "3d98a0828cbb34fa1d228d6391b4b5df98f3db3850f6702d92485666dbf68723",
        "GROW_ASDAN/Enterprise/ENT_W1_Helps_And_Earns.html": "c276145264fc68c4a63b16602e5706bb983939aa7e0e59bbf023bdfb3a731fe9",
        "GROW_ASDAN/Enterprise/ENT_W2_Spot_The_Gap.html": "8e1d89aa4c04de8c8920248903c7a7e0463f9dcd719f307246ccd810b412cf08",
        "GROW_ASDAN/Enterprise/ENT_W3_Our_Idea_Our_Users.html": "1e8c7ccb0b70dab38834b58d266f4fd7796e350390414a69b1cf933cb442da8a",
        "GROW_ASDAN/Enterprise/ENT_W4_Money_In_Money_Out.html": "064e98d3a21b106818749b68754e145922d42925b04755ee68bb1fec915292ff",
        "GROW_ASDAN/Enterprise/ENT_W5_Brand_And_Pitch.html": "63d80cdaaf382038f34f462805b34c8a9e4834ddebbd9dabd8b825cb77480e0c",
        "GROW_ASDAN/Enterprise/ENT_W6_Pitch_Day.html": "bcd8c6656bae63575cae0f0602b5f7c17d1e750a307690ead3f3fea1b7adc72f",
        "GROW_ASDAN/PEQ/PEQ_W1_Knowing_Myself.html": "e80087600c065e3d6849020ecd0bd8591ab94f36c803da291c883a14d443ab42",
        "GROW_ASDAN/PEQ/PEQ_W2_Goals_That_Work.html": "372fec2dc9f8b31c7d88d9652c950de309a39e6918e1d11a4b3c78459deaf99b",
        "GROW_ASDAN/PEQ/PEQ_W3_Working_With_Others.html": "a95924403d86c1d3d39bcf8297b7d33d017b94fffd63e0f48fbc94a90f7363e3",
        "GROW_ASDAN/PEQ/PEQ_W4_Managing_Myself.html": "32a68bb177a1af10744d1cdbaf3b3ba180220347b8a17fbae779f7a18ba93bb5",
        "GROW_ASDAN/PEQ/PEQ_W5_Solving_Problems.html": "d037a98e357266b56383613d04dfa0209ca9bd8ff43d041e7b87255200f6da8d",
        "GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html": "743a88ddf7399859533f932f42802553ba54b8d37f705638704e1eca3c3dc405",
        "Grow/Slideshows/GROW_ART_W10_Hold_your_part_Classic.html": "619632284b06cecb99efaca255a7bf010f381d4f02db2e88005a98819c5be86f",
        "Grow/Slideshows/GROW_ART_W1_Art_Battle_Tasters.html": "f958d07f384d45a1aec64b098ac24af0f240a20da146871bc77ecf88b4968472",
        "Grow/Slideshows/GROW_ART_W2_Level_Up_Portrait.html": "ee9d83a2ae09c73c41035c307f67978cf3b034a545ae34f437ee60b51d7393af",
        "Grow/Slideshows/GROW_ART_W3_Plan_The_Portrait.html": "f0ed838cc0784199a8164bed797ad9719a42c004647c5d13f1e270faea1dcb6c",
        "Grow/Slideshows/GROW_ART_W4_Create_The_Piece.html": "d54d82e89278d793373227a105641cfa5e4e6f70d5f2459f94ed713039407021",
        "Grow/Slideshows/GROW_ART_W5_Review_And_Improve.html": "83da6d51d453812d44106fedc00885a9466c804b4ca628b3f922caa39baebeb1",
        "Grow/Slideshows/GROW_ART_W6_Artist_Research.html": "079cadb3d7834bc973c4ccdfb671abd28cdbcfc95827fbd35ff7c12b8c262139",
        "Grow/Slideshows/GROW_ART_W7_Share_The_Portfolio.html": "c5587fb0692cd81b786a97b34faa80c2ec0b7f7be70062513dbbd0b02ced8580",
        "Grow/Slideshows/GROW_ART_W8_Festival_Sounds.html": "de4f84c2a8e47ede3e6681daf2b0b5cccb9d3c0eece0091bc2d0339355a135f9",
        "Grow/Slideshows/GROW_HUM_W1_Time_Detectives.html": "5620f5746ad8c4ff3fac4666c5a246a1c40a94f406526e08216d630c17cb1da4",
        "Grow/Slideshows/GROW_HUM_W2_Source_Detectives.html": "eec9cf08faa73e6f92940aadd8b50db9981d875d7b2459115bd7aa01eda59063",
        "Grow/Slideshows/GROW_HUM_W3_Cause_And_Consequence.html": "b4af68fc45de4fd00e7c674d61692fd72383dcc7fd2a2507922bbca756f0e469",
        "Grow/Slideshows/GROW_HUM_W4_People_Who_Shaped_Britain.html": "754508e2846f25aa333fda4c8389fa5cd3b455e6e68a907e9a850df20e829c65",
        "Grow/Slideshows/GROW_HUM_W5_Significance.html": "94d571605978caa7745dd0dc84967a56352c3b53506d3cca8672b5aa2d91be62",
        "Grow/Slideshows/GROW_HUM_W6_Plan_The_Account.html": "d0705c04d673a833b2e1338c5de4fd7062fec419a10bff7588683a673580e62b",
        "Grow/Slideshows/GROW_HUM_W7_Write_The_Account.html": "dc6c727a184ec6b08b433ceadc8cf5b502d7d7fa69c833c142944eae3afb79ec",
        "Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html": "d96eb576e6f22e5f8ee910ae09f7e8b3fd757ee27d6ac1371a0c616a3cdf038e",
        "Humanities/BUILD_W1-W8_2026-27/BUILD_Humanities_W1_Pick_a_card_and_say_why_you_picked_it.html": "d432a11bdaf0ac940e02877ae315421d464c1a4f2149445285116d4db53fde2e",
        "Humanities/BUILD_W1-W8_2026-27/SHA256SUMS.txt": "24f73f9403d1bc5b8b8be6f7edc6d6f7e39ede4f471c406f3ce1405f19fa984f",
        "LAUNCH_ASDAN/Careers/CAREERS_W1_Know_Myself_for_Work.html": "7d756c0ff55cc4b19d42a831ed9b36a911ce8a2389f8a598c6beb86b6a1d089b",
        "LAUNCH_ASDAN/Careers/CAREERS_W2_The_World_of_Work_and_Its_Sectors.html": "ad31387c3843986cc08e95e508fec6c6d56c93a450bd2c4fa0f7da63f975c64b",
        "LAUNCH_ASDAN/Careers/CAREERS_W3_Labour-Market_Information_and_Pathways.html": "a8d229f49c5127cc9890d73d111fc81c8ecf0a0542779753dc1455b8f3cd52ab",
        "LAUNCH_ASDAN/Careers/CAREERS_W4_Meeting_an_Employer.html": "195ebf594a9bb5eabab0f3c89e9c0ca6a15e81d0482475990c709e656868ed10",
        "LAUNCH_ASDAN/Careers/CAREERS_W5_Matching_My_Profile_to_Opportunities.html": "0c43de349b5f85908d182c8d7b3abb74855268acd4dd60186c455e46868d6fde",
        "LAUNCH_ASDAN/Careers/CAREERS_W6_Setting_SMART_Careers_Targets.html": "e0f7562e571bb7d8056189dc9412c5d0257e64f24429fe05a36b1b4db0efaa78",
        "LAUNCH_ASDAN/Community_Enterprise/COMM_W1_Identify_a_Community_Need.html": "2f429c36473078e8f63eb9565f750e5fc54d5b542bb7b58406c20d8780d88c07",
        "LAUNCH_ASDAN/Community_Enterprise/COMM_W2_Plan_a_Social-Action_or_Enterprise_Project.html": "7aed18099a65a6e48a526abe1af306861c23bdb0ef8e6d19553a3b9faa3a62dc",
        "LAUNCH_ASDAN/Community_Enterprise/COMM_W3_Agree_Roles_Aims_and_Timeline.html": "735315194d72cb7630e5a69721d77c93a04593551e103aa283e99568e7e532d0",
        "LAUNCH_ASDAN/Community_Enterprise/COMM_W4_Partner_with_a_Local_Group_or_Charity.html": "fd9089d69ca6212d57c55502a69eab37eb894df3c6fe416381ad06a559909fd8",
        "LAUNCH_ASDAN/Community_Enterprise/COMM_W5_Begin_Delivering_the_Project.html": "87a6f8cf3bf77756b5819d5f3ccce93a29367873486d6ab5cc1a84f27ed362e0",
        "LAUNCH_ASDAN/Community_Enterprise/COMM_W6_Promote_Our_Project.html": "80d4a42e89127cf5e18485599c17c43908586c6f411b653dad67101dd41e69fa",
        "LAUNCH_ASDAN/Living_Independently/LI_W1_Self-Care_Routines_and_Organisation.html": "cdf5b0b50845188e74dfcc63f73179d4127a15bc593228fb74a2354ed19bcea3",
        "LAUNCH_ASDAN/Living_Independently/LI_W2_Home_Safety_and_Hazard_Awareness.html": "084cf1808b308f406878a3f4272d68be37b63e6128fee2e36e12f924c41cd5a6",
        "LAUNCH_ASDAN/Living_Independently/LI_W3_Laundry_and_Household_Maintenance.html": "06c1c0fb87ae7525cae2ee0e68b1bf9e143a0752bc52403f8ae06fb6f05db630",
        "LAUNCH_ASDAN/Living_Independently/LI_W4_Keeping_a_Clean_Safe_Living_Space.html": "daa4751b99d82d5ef76919674bb8a3a59e74b9eb18405e616a3feb950156afaa",
        "LAUNCH_ASDAN/Living_Independently/LI_W5_Personal_Admin_and_Responsibilities.html": "613a20f1f40ee435f8ed5940bb7abfbadc289a57f19b3cedc24a309139e03b79",
        "LAUNCH_ASDAN/Living_Independently/LI_W6_Plan_and_Shop_for_a_Balanced_Meal.html": "2b15960949ebc2a1f6a996767dfe7445a58fbcc098428f3e79158a1870be6e46",
        "LAUNCH_ASDAN/PEQ/PEQ_W1_Intro_and_Choosing_My_Level.html": "f759aa71ee94d5ea34c25493f1c8a9a8ab8321bc0706888f32320105e59c65a2",
        "LAUNCH_ASDAN/PEQ/PEQ_W2_What_Makes_Communication_Effective.html": "d1975417af5bd27d9e08237fa94c3f8052b9f358ff1026cd89a59fee56bcd3bf",
        "LAUNCH_ASDAN/PEQ/PEQ_W3_Active_Listening_and_Giving_Feedback.html": "4d090a91a79048e14e5827c7197cfd56c2a06d202b0dab4092d36bcfb1681c5c",
        "LAUNCH_ASDAN/PEQ/PEQ_W4_Plan_a_Communication_Activity.html": "e941b91baffa801033c4509a2a594924db3db9887a57933ad66b328db0d3b1c2",
        "LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html": "6f04bd420fc0ce1f700211244f5c20ff15b53fc7392a0beeae5701e0cc16ac17",
        "LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html": "2a27768d7235d7b7424c83ae86201d148b2c620e0825a9b63a31e4054cbc000b",
        "LAUNCH_ASDAN/Vocational/VOC_W1_Introduction_to_Vocational_Skills_and_Workplaces.html": "88730c35bb48cea74738080856606af3cc225d6592b0a229c725b8073af0a854",
        "LAUNCH_ASDAN/Vocational/VOC_W2_Health_Safety_and_Hygiene_at_Work.html": "23265b349694dca8af9cd324a5afbf5cbfbfed20481ee1ca11706ba36bed5844",
        "LAUNCH_ASDAN/Vocational/VOC_W3_Following_Instructions_and_Routines.html": "b817da12c47293c14d80c51218edc4064f4dff8733b98088990d1eebcdbc9306",
        "LAUNCH_ASDAN/Vocational/VOC_W4_Teamwork_in_a_Vocational_Setting.html": "b2ca69990cf49761cc9348883205fe37808666b0723985e94d6a7b4741282e64",
        "LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html": "68f60201a5991347b967037712c181db0d173dc397b946a93e16c6c635f7f4ce",
        "LAUNCH_ASDAN/Vocational/VOC_W6_Complete_a_Supported_Vocational_Task.html": "d64204d8d680b6933e46792060e4053aad50eef3b46e6f8e89f346ce4f14e408",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W10_Make_the_team_plan_usable_Classic.html": "f302fa348f785bf4553a6d1bfdbdc9e4849de3ca95712392a6083e182af9590d",
        "LAUNCH_ASDAN/W7-W12_2026-27/lessons/PEQ/PEQ_W9_Agree_a_team_plan_that_works_Classic.html": "a2a4da071a35dcc95ce750de04471038ccc8d159860ecdf8d95530c46c0779a0",
        "Launch/Slideshows/LAUNCH_ART_W10_Whose_meaning_is_it_Classic.html": "4c3f6dbc05f8ed3fc967d6c2af53435c13164878ce91ba4b7ea19d9398a0e34f",
        "Launch/Slideshows/LAUNCH_ART_W11_Develop_the_piece_keep_the_decisions_Classic.html": "3bf2233443ec6a37e7ef313984dc31f3ba45130460041c327e4d45b4fead07fa",
        "Launch/Slideshows/LAUNCH_ART_W1_Gallery_Detectives.html": "811bcbaddfdb45d92f60b0531efa95ce2208245c4a9fba0f7586e836bca6ce45",
        "Launch/Slideshows/LAUNCH_ART_W2_Symbolism_Self_Portrait.html": "eb64e2f6b2f03f4d2b9f669107ee86d34ae50c29c72fda8492194100eb4904f0",
        "Launch/Slideshows/LAUNCH_ART_W3_Practitioner_Research.html": "e8fa088854a93f822293fb2149c56546e3ba2c9b83129d053d7f3379052d92a9",
        "Launch/Slideshows/LAUNCH_ART_W4_Refine_With_Feedback.html": "2b7f271e05683c4791fdabae44de539c3c25400b8de443735a89aee8e570b1fd",
        "Launch/Slideshows/LAUNCH_ART_W5_Plan_The_Experience.html": "bd57a4cf4c750d4e063b19dcaea4cb7a9b66cda9d6f6a5c4e2abaa87ef8bbed9",
        "Launch/Slideshows/LAUNCH_ART_W6_Experience_The_Event.html": "69d9e035ffbac3954cb041eafe5c6a38c17a7dc969a5df3f2a635eeeca1f34d3",
        "Launch/Slideshows/LAUNCH_ART_W7_Begin_The_Review.html": "a3269e85af1f88a891d89ae13b6f5fecdb437df2b9b86014e35f404971c5fa71",
        "Launch/Slideshows/LAUNCH_HUM_W1_Source_Investigation.html": "6fbaa72c212f16c305ca37a0d55315b73a76410f97fc905a9edb2492d94bcac0",
        "Launch/Slideshows/LAUNCH_HUM_W2_Cause_Consequence_Courtroom.html": "736e9ccb4cfbd7df9555431a7e0b5b8ebaf75ea16996d87477fa3edbcafc8c86",
        "Launch/Slideshows/LAUNCH_HUM_W3_Archive_NOP.html": "f71b1a3d0bbd504e5944ffb5353484b2fd7f48fb2761c71479eae55ee4846b0b",
        "Launch/Slideshows/LAUNCH_HUM_W4_Century_Of_Change.html": "449fe59725dac7decd28750079dd1be4e32da560d9e3def23e2154885cbacbc4",
        "Launch/Slideshows/LAUNCH_HUM_W5_People_Modern_Britain.html": "2004ceb8b20e148e9b70d00b043b158a79eee64ac6005d2014501700fae7aed9",
        "Launch/Slideshows/LAUNCH_HUM_W6_Structured_Account.html": "5aba5f5ecca5b813088fa95ddab562c7408811c161af35dea36e7cf7c5dbbecf",
        "Launch/Slideshows/LAUNCH_HUM_W7_Source_Assessment.html": "a6f1c5d4cb96b36fa719a1d625f2e300c64a0370e2ccb2d99a76fc0871cd5aa2",
        "Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html": "6d2ebc199e7c8214c5f9357119ad920811b6452d9ae23388789a9a5d9d06e04b",
        "Launch/Slideshows/LAUNCH_HUM_W9_Find_it_with_a_grid_reference_Classic.html": "a1c12d60dd7594034c9a4750547e590968e9115e0ede0442d06672f3c7002011",
        "Science/Build/W27-W34_2026-27/SCI_B_W27_The_Plant_Parts_Atlas.html": "a95074afe5cce24e3af39b57e4cb8b929c7b4ed27048d5190d92eab5bb3c9b08",
        "Science/Build/W27-W34_2026-27/SCI_B_W28_The_Plant_System_Service_Desk.html": "ab4259bead7c3d05985971b019e33f25eea7ece2afdfdc53eb8b0850e51783ed",
        "Science/Build/W27-W34_2026-27/SCI_B_W29_The_Growth_Needs_Clinic.html": "9740b00e83e12a3941070eed09daa96d0d8f39ce9211ceb094af705bee174f0c",
        "Science/Build/W27-W34_2026-27/SCI_B_W30_The_Water_Trial_Planning_Board.html": "72665cdfb5d6f0c12f031850e283e90aa21476fcaa272afee52100bc39e2f86f",
        "Science/Build/W27-W34_2026-27/SCI_B_W31_The_Growth_Record_Studio.html": "0e24abb6697ee78d44238d51b17e6efed86e7ccf7e4f866972e01b0238da50fd",
        "Science/Build/W27-W34_2026-27/SCI_B_W32_The_Water_Path_Detectives.html": "09d52af20e10ed8673e01c76b07716cf6c773ebf83fb6bd0f531e9a0a6514ce6",
        "Science/Build/W27-W34_2026-27/SCI_B_W34_The_Friction_Surface_Lab.html": "17805fb2e6afa52f5e3ff0b741022a591cb17d6f1396995f9547f864ea86e172",
        "Science/Build/W27-W34_2026-27/SHA256SUMS.txt": "fcfd1dff421655e3f1b7df32a677342b58900ae363204a4cd98cfb8e212c50df",
        "Science/Grow/W27-W32_2026-27/SCI_G_W27_The_Flower_To_Seed_Investigation.html": "da552f866410b2767b22cb49930227185842e78ee0e66217701a6d1cbdf1e717",
        "Science/Grow/W27-W32_2026-27/SCI_G_W28_The_Plant_Reproduction_Strategy_Studio.html": "684bb814c7c9730a3af403378fc5edc681850c6bc25555a6c73798d3314f21ae",
        "Science/Grow/W27-W32_2026-27/SCI_G_W29_The_Seed_Dispersal_Design_Lab.html": "6d9ca302dc830793ce03f3b1af8ca3d956d4d361e928bdcbf772ed9f47a03bf1",
        "Science/Grow/W27-W32_2026-27/SCI_G_W30_Reversible_Change_Detectives.html": "f0a3dd63d36459a2f1c93e9b8216c0460655c450f7dd496019ed3528299803ff",
        "Science/Grow/W27-W32_2026-27/SCI_G_W31_The_Recovery_Methods_Workshop.html": "90d7254aa4c3776f5551d113121d83505deb0041ae380578c166b908f795c032",
        "Science/Grow/W27-W32_2026-27/SCI_G_W32_Change_Detectives_What_Became_Something_New.html": "7f697c07f0b3f3b1480af590a4b43cb684cd6e445deba1e0a2c821bcbb121903",
        "Science/Grow/W27-W32_2026-27/SHA256SUMS.txt": "aa05bf74af349485ce88e85bc40045bf5024530f98cac820e506e044488c3e0b",
        "Science/Launch/W27-W34_2026-27/SCI_L_W27_Hormone_Messages_The_Control_Room.html": "8e927b11b7ad1bd52fa8e46b802c59262961562db437151a1be8c93c4ab12bc3",
        "Science/Launch/W27-W34_2026-27/SCI_L_W28_Blood_Glucose_Build_The_Control_Model.html": "6da8ed21b38153397756edeb673378d37b2e366809454c177ad83f55c43734a5",
        "Science/Launch/W27-W34_2026-27/SCI_L_W29_Double_Circulation_Engineer_The_Route.html": "828cc15b8c8b2c5d5d8fa6896916dba29432db6a70cdf0b8f2d482b5963513bb",
        "Science/Launch/W27-W34_2026-27/SCI_L_W30_Exchange_And_Ventilation_Two_Linked_Jobs.html": "a8f8cd8c741fc182021c29012437326aece4906449c793a49835180d8f6992aa",
        "Science/Launch/W27-W34_2026-27/SCI_L_W31_Animal_Systems_The_Evidence_Challenge.html": "e34e22f1f0fab61f222ae3e716de3d2bb18b3f50d6b514dacbeedbdff83636d3",
        "Science/Launch/W27-W34_2026-27/SCI_L_W32_Topics_7_8_Mechanisms_Checkpoint.html": "a20ea6e76bf74e158a7338fee83358cef5b51d6bb066b29bd064440fc47bbb42",
        "Science/Launch/W27-W34_2026-27/SCI_L_W34_The_Border_Brief_An_Ecosystem_Evidence_Web.html": "8a0bc8f3b242ad88808cf1e1155cce46c884fbe901acf0a0dc1e9cdd47544374",
        "Science/Launch/W27-W34_2026-27/SHA256SUMS.txt": "983e944653461e7d755783ef49a87fd34eac7d7592725c9016170084966cc17d",
        "biology/Bio_Respiration_Limewater_Exercise.html": "eeb1066ee746094645af1345058bf372245e41389920af3bdd70e3f6243aa2b5",
        "biology/Chem_Making_Limewater.html": "0181c59e2dd6fec8ba09e11e752bc1a327bf8cdb726daf98afc3491779cefc0a",
        "biology/Testing Breath - FINAL Observation Lesson (1).html": "60621fcff3fd9ee7faddcccdb674b1f5bb7dcae6c7cbf1702ff32aada171bd7a"
    }
}
# END REVIEWED CATALOGUE PINS

# These semantic pins are deliberately outside the movable file/manifest block.
# Neither the catalogue pin tool nor the generic manifest pin tool can bless
# an edited, deleted or reordered original resource, or an extra lesson row.
# Ruling qp-2 (A-wide, os-4, 11 Oct 2026): the original rows are 734 plus the 21 reviewed rows the A19/A24
# catalogue refresh interleaves (additive: with them taken out, the 734 are in their reviewed order, unedited).
CATALOGUE_ORIGINAL_ROWS = 755
CATALOGUE_ORIGINAL_ROWS_SHA256 = "d4714b20bc0de0732d1dd33e449280b8b42fd0a033b830c7b169b7f538430717"
# The appended rows are the 49 reviewed hub rows followed, since UX2 D3
# (2026-09-08), by the companion-pack entries DERIVED from
# data/companion-packs.json by tools/ux2/companion_catalogue.py. The count and
# digest below are re-cut by tools/catalogue/pin_catalogue_contract.py from
# rows it has verified against that derivation; an edit to any appended row,
# a removed pack row or an extra lesson row still reds here.
CATALOGUE_SHELF_ROWS = 502
# UX2 A1: keys that may be appended to an original row without moving its
# digest (see catalogue_errors). Nothing else is additive. No original row
# carried either key before the ruling (measured 2026-09-08: 0 of 734), so the
# second set is empty and the allowance cannot launder a pre-existing value.
CATALOGUE_ADDITIVE_TAG_KEYS = frozenset({"halfTerm", "unit"})
CATALOGUE_ORIGINAL_KEYS_BEFORE_TAGS = frozenset()
CATALOGUE_SHELF_ROWS_SHA256 = "e1cadcb073378ecae6bfc3d70036e5de1ccb0d8c25b90916744ee5e5c76474ce"

# These named review records and review tools can change with their reviewed
# transaction. Tools are not served assets; they are reviewed as executable
# gate logic, rather than recursively hashing themselves. No lesson payload,
# game payload, shared platform asset or arbitrary directory is exempted.
CATALOGUE_RECORD_PATHS = {
    "tools/catalogue/STATIC_CHECK_RESULTS.json",
    "tools/catalogue/DOM_CHECK_RESULTS.json",
    "tools/catalogue/RECOVERY_2026-09-05.md",
    "tools/catalogue/README.md",
    "tools/catalogue/pin_catalogue_contract.py",
    "tools/catalogue/verify_catalogue_contract_controls.py",
    # UX2 A1 (2026-09-08): the record's schema travels with the record. It is
    # data, not a lesson payload; it is enforced by tools/ux2/check_catalogue_schema.py.
    "resources.schema.json"
}

# The education publisher is executable release configuration, not a hub asset.
# Permit only this named workflow, and require its complete reviewed bytes on
# every run. A broader permission, trigger, job, floating ref or mismatched
# builder is red.
PUBLICATION_CALLER_PATH = ".github/workflows/education-pages.yml"
# Reviewed Education completion publication caller, Site PR #268, 2026-09-06;
# advanced to Site #299 47811e56, then Site #301 50877370 (Play revision registry: Glitch HUD and
# §3.3 touch-action revisions, transition pairs) by Order HC4.
# Until Order UX2 both callers advanced together and this one digest served
# both repositories' callers. UX2 moved the Lessons caller alone (Lessons #436,
# #438, #442; the order writes nothing to the Apps repository), so this digest is the
# LESSONS caller's, and the Apps caller carries its own reviewed digest below.
# Advanced 2026-09-09 (SX1/SX2): the Lessons caller's publisher pin moves Site
# 92abc460 -> 94ae15f8 so the all-file admission registry admits the Spring/Summer
# Science batch. The Site commit is 92abc460 byte-identical except that registry and
# the retained usage-registry baseline; education-publication.yml is unchanged between
# them, so no builder, Play or usage-discovery code moves with the pin.
# Advanced 2026-09-10 (AMEND-3R-GC1 P6): the publisher pin moves Site 2a154e33 ->
# 2e49afdd. Unlike every advance above it, this one moves BUILDER code and not only
# the admission registry -- .sb3 is added to the publisher extension allowlist and
# to the admission census, without which the 23 Scratch projects in the GROW
# Computing unit never reach the served tree. education-publication.yml is
# unchanged between the two, so the gate itself still does not move.
# GC1 12 September: reviewed 810ae8f8 -> 3c2743fb registration-only carrier.
# SW2-T5R1: consumer-specific registry-only carriers, with unchanged publisher code.
# Advanced 2026-09-15 (CX2 R5) to Site carrier 297ed5dea71461d25365fa8a9ef1139b7d161996, which is
# c06526c5 byte-identical except the admission registry (two regenerated catalogue files admitted
# beside their published rollback digests). Only the caller's two commit references and its
# comment move; this digest is the caller file after that move.
# Advanced 2026-09-15 (CX2 S3) to Site carrier a89e2c601b491be7b0121754a17f56228eafa21a on the same
# carrier branch: 297ed5de plus two registry commits (Lane D BUILD W8B and its lesson-order; the
# relabelled teaching-pack hub). Every entry keeps its published rollback digest beside the
# candidate. Only the caller's references and comment move.
# Advanced 2026-09-15 (CX2 §2 Friction) to Site carrier 8cfd08b3abe08eeb79ff2139bedf07fbf536c520 on the same carrier branch:
# the GROW W3 Friction candidate (this branch, #538) admitted beside its published rollback digests — the lesson, resource pages, GROW pack records, seven Week 3 archives, W3A/W3B natives, the hub index, lesson-order.json and the usage registry (30 pairs, nothing added or removed). Digests from a full three-repository build at this builder, qualified by a control build of main that reproduces all 4044 admitted digests. Publisher code is unchanged.
# Advanced 2026-09-15 (CX2 §2 Friction rows) to Site carrier 17e82d701c25354719114b4fca2fc3207a9da3d8 on the same carrier branch:
# the reviewed Science download rows (science-download-usage-additions.json, pinned by check_education_separation.py) brought to the nine Friction files whose size changed; the first publication of main acae624f stopped there after admission had passed. Registry unchanged from 8cfd08b3; no other publisher code moves.
# Advanced 2026-09-15 (CX2 §3 Diffusion) to Site carrier 7f97cbbfba76a44e86514116eaea67bd46782274 on the same carrier branch:
# the LAUNCH W4L1 Diffusion candidate (this branch, #546) admitted beside the published Friction digests (38 pairs, nothing added or removed) with its thirteen download rows reviewed; one commit on from the Friction rows carrier main pins. Publisher code is unchanged.
# Advanced 2026-09-15 (CX2 §4.8 Sugar R10) to Site carrier d76182f4cbb0071b3652feba265dc66129d393f0 on the same carrier branch:
# the Sugar R10 hygiene candidate (this branch, #547) admitted beside the published Diffusion digests: the BUILD W8A lesson whose feedback card no longer names the evidence product, its re-rendered teacher DOCX and PDF, the BUILD checksum list and lesson-order.json (5 pairs, nothing added or removed). No reviewed download row moves — the two documents keep their KB-rounded sizes, measured at 0 of 320 rows changed. Digests from a full three-repository build qualified by a control build of main a8b3c968 that reproduces every admitted digest. Publisher code is unchanged.
# Advanced 2026-09-15 (CX2 §8.3 Lane D) to Site carrier 429dd4ecf0ef00f8e04d2296473cf99f46243cbd on the same carrier branch:
# the whole return week (this branch, #545, carrying #543 BUILD and #544 GROW) admitted beside the published Sugar digests: BUILD W8B, GROW W8A and W8B, LAUNCH W8L1-W8L3 and lesson-order.json (7 pairs, nothing added or removed). No reviewed download row moves — these six lessons carry no pack downloads, measured at 0 of 320 rows. This carrier also replaces the withdrawn sparse W8B digest with the one a full build actually produces. Digests from a full three-repository build qualified by a control build of main ec7d34ab that reproduces every admitted digest. Publisher code is unchanged.
# Advanced 2026-09-15 (CX2 §8.3 Lane D, corrected) to Site carrier dd9d228aeb183f6efc26f2f7f35982f70b3f91de on the same carrier branch:
# the whole return week (this branch, #545, carrying #543 and #544) admitted beside the published Sugar digests, re-cut after the authored lesson-config block was restored to all six lessons (W8B b67be20d -> 492a4c28). Seven pairs, nothing added or removed; no reviewed download row moves. Digests from a full three-repository build qualified by a control build of main ec7d34ab. Publisher code is unchanged.
# Advanced 2026-09-16 (CX2 §8.3 Lane D, corrected again) to Site carrier 3032ae716518c9e51b3ea00314e288bbb4145d9a on the same carrier branch:
# the whole return week (this branch, #545, carrying #543 and #544) admitted beside the published Sugar digests, re-cut after the guidance button was docked and the stage timer moved off the home link in all six lessons (the full offline-pack check now passes 12/12). Seven pairs, nothing added or removed; no reviewed download row moves. Digests from a full three-repository build qualified by a control build of main ec7d34ab. Publisher code is unchanged.
# Advanced 2026-09-16 (CX2 §5.3 EDU-Q1 companions) to Site carrier 40339776460347d0018569d598c45d0dd1a93497 on the same carrier branch:
# Carrier 40339776 admits the six catalogue/discovery outputs the companion rows move, as [served, candidate] from full builds (served oracle main e1a05dce).
# Advanced 2026-09-16 (CX2 §5.3 EDU-Q1 companions (second mint)) to Site carrier 7491329d8533b7edf6d32cfaa13a065c28af3f41 on the same carrier branch:
# Carrier admits hub.js (pathway directory read case-insensitively) beside the six catalogue/discovery outputs, as [served, candidate] from full builds.
# Advanced 2026-09-16 (CX2 section 7.1 PLAY-Q1 batch 2) to Site carrier 08d74766de02b90e90e6138b7c20e66bb30aada4 on the same carrier branch:
# Carrier admits the two re-stamped education lessons, the lesson-order projection and the resource
# size table, and carries the Play evidence rebound to the batch 2 bytes.
PUBLICATION_CALLER_SHA256 = "4e1678265e6a4a4d7478112778ff8ef552d08003b67ac4f2cc2aa7802111c17f"
# One reviewed caller digest per repository kind. detect_kind() reads the root
# it is standing in, so this entry is only ever compared against the Apps
# repository's own caller: the Lessons gate run and the Apps gate runs are the
# only callers of publication_errors(), and the Site repository invokes this
# verifier in no workflow at all.
# UX2 A5 pinned this to the Apps caller at 924ab986 -- the commit Site
# domain-split-verify.yml checks out, whose caller names Site 23a4f360 -- on the
# premise that a Site catalogue-contract control ran this gate against that
# checkout. No such control exists, and 924ab986 is behind Apps main. The
# reviewed Apps caller is the merged one: Apps #72 advanced it 23a4f360 ->
# 6430f23f (CX3 cycle C) on 2026-09-08, superseding c420519111f6 thirty-six
# minutes after it was written. The mismatch stayed invisible while the Apps
# gate copy predated UX2 A5 and so had no by-kind map to read; putting the two
# copies back in step is what made it fire.
PUBLICATION_CALLER_SHA256_BY_KIND = {
# Advanced 2026-09-16 (D-1): this repository's own publisher pin moved to the Site
# carrier f70f4973, which re-binds the homepage feature card to this repository's main
# and mints the publication admission for the paths whose bytes had moved. The caller
# file therefore changed, and this is its digest re-cut from those bytes. The "lessons"
# entry is now its own literal rather than an alias of PUBLICATION_CALLER_SHA256, which
# stays where UX2 A5 left it: the two kinds pin different files and had no business
# sharing one constant.
# ORDER SX3-PASSES: the publisher pin moves to Site main 0cd8f842, which carries the
# 21 transition pairs for this release's published bytes, the re-frozen retained
# registry baseline, and the builder-pin move that puts domain-split-verify on
# the same Lessons state as this carrier. A CARRIER PIN MOVE under release-red
# precedence. The caller file therefore changed and this is its digest re-cut
# from those bytes -- derived with sha256sum, never transcribed.
# ORDER HUM-T batch 1 (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main
# cac643be, which carries the eight transition pairs for the six transplanted BUILD decks,
# the lesson order and the size table, and both L31 pin pairs at 3887f7ac / 327da98e. The
# caller file therefore changed and this is its digest re-cut from those bytes -- derived
# with sha256sum, never transcribed.
# ORDER HUM-T batch 1, second window (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main a461a77a; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER SCI-COMPLETE PASS A (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main 3cff4ba7; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER HUM-T batch 2 (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main 297e09b4; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER HUM-T batch 3 (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main 83ffbe8b; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER HUM-T batch 4 (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main aad258a9; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER HUM-T batch 5 (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main ec58a420; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER HUM-T batch 6 (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main 8e95534e; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# HUM-T batch 6b (STANDING RULE L33, 2026-09-20): the publisher pin moves to Site main f29214ed; the caller
# file therefore changed and this is its digest re-cut from those bytes -- derived with
# sha256sum, never transcribed.
# ORDER SCI-COMPLETE PASS F: the publisher pin moves to Site main 9600846c, the re-cut
# PASS F admission window (Site #426), which admits the rebuilt Science hub and the
# registrations it links. The caller file therefore changed, and this is its digest re-cut
# from those bytes -- computed, never typed.
# Summer 1 responsive re-delivery (STANDING RULE L33, the ruled pending-then-land fold,
# STOP-RESP-2 step 2, 2026-09-22): the publisher pin moves to Site main aeb47509, the squash
# merge of Site #430, which admits this release's 27 published paths as [main-today, pending]
# transition pairs. The caller file therefore changed and this is its digest re-cut from those
# bytes -- derived with sha256 over the edited file, never transcribed.
#
# NOTE ON ORDER, found by the pre-push battery rather than reasoned: this constant lives in the
# gate copy that must stay byte-identical across Lessons and Apps (the G1 control), so an L33
# carrier bump DRAGS THE GATE COPY -- and therefore the Apps companion -- along with it. The new
# digest cannot be computed until the Site SHA exists, which is only after the step-1 window
# merges, so the Apps companion for a carrier-bearing fold cannot be a single PR opened up front:
# it needs a second companion opened after step 1. Recorded so the next fold plans for it.
# RE-CUT 2026-09-22 (STOP-RESP-4, route A): the carrier is re-bumped to Site main 0f931086,
# the squash merge of Site #431, so education-pages.yml changed again and so does its digest.
# This is the second cut in one fold and it is the cost the standing rule exists to avoid:
# bump the carrier ONCE, LAST, at a SHA that already admits every mover.
# Re-cut 2026-09-22 (the Science hub's generation order, ruling on the S02 STOP): the carrier
# moves to Site main bb283643, the squash merge of Site #433, bumped once and last. Digest
# derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-09-22 (the pure carrier closing the hub fold): the carrier moves to Site main
# dd9831f3, the squash merge of Site #434 (the EQUAL window). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-09-23 (PASS C Autumn 2 batch 1, rulings S1 and S3): the carrier moves to Site main
# c85c12c3, the squash merge of Site #436 (the window's second cut, after the adversarial review;
# #435 admitted the first), bumped once and last. Digest derived with sha256 over the edited file,
# never transcribed.
# Re-cut 2026-09-23 (the Science hub follow-on, route C): the carrier moves to Site main 0fa71565,
# the squash merge of Site #437 (the EQUAL window that also admits the hub's 3 pairs), bumped once
# and last. Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-09-23 (the pure carrier closing PASS C Autumn 2 batch 1's fold): the carrier moves to
# Site main 5251edc8, the squash merge of Site #438 (the EQUAL window). Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-09-23 (HUB1 v2, Autumn 2 hub badges): the carrier moves to Site main 7d310e1e,
# the squash merge of Site #440 (the window admitting HUB1's 6 pairs), bumped once and last.
# Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-09-23 (the pure carrier closing HUB1 v2's fold): the carrier moves to Site main
# 9fd80be8, the squash merge of Site #442 (the EQUAL window). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-09-25 (Q12, the Science hub stylesheet): the carrier moves to Site main 3e5e489d,
# the squash merge of Site #444 (the window admitting Q12's 2 pairs), bumped once and last.
# Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-09-25 (the pure carrier closing Q12's fold): the carrier moves to Site main
# be9441d7, the squash merge of Site #445 (the EQUAL window). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-09-25 (LAND-A2 Science): the carrier moves to Site main 214749c0, the squash merge of
# Site #448 (window W1: the 21 lessons' rows and the fence's transition pair), bumped once and last.
# Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-09-25 (LAND-A2 Science, the pure carrier): the carrier moves to Site main 079fba99, the squash
# merge of Site #449 (window W2: the refresh, the fence collapsed to one digest, the EQUAL pins). Digest derived
# with sha256 over the edited file, never transcribed.
# Re-cut 2026-09-26 (DLG-1, LAND-A2 R8): the carrier moves to Site main de2ed592, the squash merge of
# Site #450 (window W1: the 194 transition pairs), bumped once and last. Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-09-26 (DLG-1, the pure carrier): the carrier moves to Site main 117d4cff, the squash merge of
# Site #451 (window W2: the five EQUAL pins onto Lessons #679 / Apps #189). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-10-04 (Science Week 8, ruling eo): the carrier moves to Site main a71ee9d2, the squash merge of Site #453
# (window W1: the 47 ARRIVING rows and 11 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-04 (Science Week 8, the pure carrier): the carrier moves to Site main 73712445, the squash merge of
# Site #454 (window W2: the refresh, the fence collapse and the five EQUAL pins onto Lessons #683 / Apps #191).
# Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-10-05 (RE Week 8, rulings fm-6, fp and fq): the carrier moves to Site main f1d0680c, the squash merge of Site #455
# (window W1: the 30 ARRIVING rows and 9 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-05 (RE Week 8, the pure carrier): the carrier moves to Site main ebbc826c, the squash merge of
# Site #456 (window W2: the five EQUAL pins onto Lessons #685 / Apps #193). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-10-06 (the names fix, rulings fv-1 and fv-2): the carrier moves to Site main 2dcb869e, the squash merge of Site #457
# (window W1: the 10 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-08 (the names fix, the pure carrier): the carrier moves to Site main d250bfea, the squash merge of
# Site #459 (window W2: the five EQUAL pins onto Lessons #688 / Apps #195). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-10-09 (names-fix PR 9, the pure carrier): the carrier moves to Site main 47276941, the squash merge of
# Site #462 (window W2: the five EQUAL pins onto Lessons #690 / Apps #198). Digest derived with sha256 over the
# edited file, never transcribed.
# Re-cut 2026-10-09 (the subject-hub noindex fix (jw-1), ruling ni): the carrier moves to Site main df664434, the squash merge of Site #465
# (window W1: the 0 ARRIVING rows and 1 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-11 (os-4 patch set A25, ruling os-4): the carrier moves to Site main c1be14aa, the squash merge of Site #468
# (window W1: the 0 ARRIVING rows and 83 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-12 (os-4 patch set A25, ruling os-4): the carrier moves to Site main 27f47031, the squash merge of Site #469
# (window W1: the 0 ARRIVING rows and 86 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-13 (io-3 Autumn 2 Week 1, ruling rd): the carrier moves to Site main 9402e0a8, the squash merge of Site #471
# (window W1: the 110 ARRIVING rows and 1 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-13 (io-3 Autumn 2 Week 1, ruling rf-4): the carrier moves to Site main 35251ca7, the squash merge of Site #474
# (the io-3 collapse window: no new rows), bumped once and last. Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-10-15 (Humanities Spring 1 window W1, ruling sd): the carrier moves to Site main a82d4d5b, the squash merge of Site #475
# (window W1: 26 transition pairs, 0 ARRIVING rows), bumped once. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-17 (RE Spring 1, rulings sr and ss): the carrier moves to Site main e076e4bd, the squash merge of Site #476
# (window W1: the 272 ARRIVING rows and 4 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-18 (Week 8 Science, ruling sy): the carrier moves to Site main 6049e6f0, the squash merge of Site #477
# (window W1: the 51 ARRIVING rows and 50 transition pairs), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-21 (the tm drawer and outcome changes, ruling tm): the carrier moves to Site main cfc92e84, the squash merge of Site #478
# (window W1: 16 moved rows, 0 arriving), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-22 (TQ Week 8 pack reachability, ruling tq-1): the carrier moves to Site main 6ad7a729, the squash merge of Site #480
# (window W1: 14 moved rows, 0 arriving; the usage fence for tq's flight), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-10-23 (uf, the two Assembly pages and decks, rulings uf, uh add.1, uf add.3): the carrier moves to Site main c6687cf6, the squash merge of Site #484
# (window W1: 4 ARRIVING rows, 9 pairs; the usage fence for uf's flight), bumped once and last. Digest derived with sha256
# over the edited file, never transcribed.
# Re-cut 2026-11-01 (Merge Letters A1-A6, LD28 standing step): the carrier moves to Site main e25aa76a, the squash merge of Site #533.
# Re-cut 2026-11-03 (Ruling M-AD): the carrier moves to Site main ca4b63ce, the squash merge of the admission PR #588 (Lessons f154ac7a).
# Re-cut 2026-11-04 (Ruling M-AE): the carrier moves to Site main 6aab2483, the squash merge of the admission PR #592 (Lessons fac84ac8).
# Re-cut 2026-11-04 (Ruling M-AE add.1): the carrier moves to Site main ede20ceb, the squash merge of the admission PR #593 (Lessons d406243e).
# Re-cut 2026-11-06 (owner pin edit 15b93935 on main, owner approved the re-cut): the carrier moves to Site main 6c62e842, the squash merge of Site #600.
# Re-cut 2026-11-06 (owner pin edit b4e6522c on main, owner approved the re-cut): the carrier moves to Site main fc91ab2a, the squash merge of Site #604.
# Re-cut 2026-11-06 (owner pin edit de25c187 on main, owner approved the merge): the carrier moves to Site main fb287c0c, the merge of Site #605 (the Humanities and RE Autumn 2 admission).
# Re-cut 2026-11-06 (owner pin edit d7c3a5de on main, owner approved the merge): the carrier moves to Site main e90a1c20, the merge of Site #606 (the site pages, sitemap and kitchen working-notes admission).
# Re-cut 2026-11-07 (owner pin edit on main, owner approved the merge): the carrier moves to Site main fba8a87f, the merge of Site #610 (the reviewed-title Humanities and RE pack pages admission).
# Re-cut 2026-11-07 (owner pin edit on main): the carrier moves to Site main 027fe921, the merge of Site #612 (the 41 pack manifests Lessons #816 publishes).
# Re-cut 2026-11-07 (owner pin edit on the pathway-labels branch): the carrier moves to Site main 3a89a748, the merge of Site #613 (the pathway-labels phase 1 admission rows).
# Re-cut 2026-11-07 (owner pin edit on the subject-page pathway-labels branch): the carrier moves to Site main 8ee4d3e6, the merge of Site #614 (admission rows for the four relabelled catalogue files).
# Re-cut 2026-11-07 (owner pin edit on the Autumn 2 lesson-list branch): the carrier moves to Site main 3cd0d4f2, the merge of Site #615 (admission of the files Lessons #821 changes). Re-cut from the caller bytes.
# Re-cut 2026-11-08 (owner pin edit on the Autumn 1 AAA lesson branch): the carrier moves to Site main 1b215d2d, the merge of Site #616 (admission of the files Lessons #822 adds and changes). Re-cut from the caller bytes.
# Re-cut 2026-11-08 (owner pin edit cc40d39c on the Science Autumn 1 list-fix branch): the carrier moves to Site main 0ac6944b, the merge of Site #617 (admission of the list fix: subject.html, terms-and-styles.json, the 15 unlisted SUMMIT pages).
    "lessons": "a0407001545f51db76cb305314d448c725a7a53db5ea04638c0671e375d626eb",
# Advanced 2026-09-16 (served-defect amendment D-2): the Apps repository moved its own
# publisher pin to the Site carrier that carries EDU-D3, so its caller file changed. This is
# that file's digest on Apps main, re-cut from its bytes.
# Re-cut 2026-10-08 (the names fix, the pure carrier; fv-4): the Apps repository moves its own publisher pin to Site main d250bfea,
# the squash merge of Site #459, so its caller file changed. Digest derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-10-22 (ruling ty, ty-2, option A): the Apps repository moves its own publisher pin d250bfea -> cfc92e84,
# the squash merge of Site #478 and the builder Lessons already publishes with, so its caller file changed. Digest
# derived with sha256 over the edited file, never transcribed.
# Re-cut 2026-11-01 (Merge Letters A1-A6, LD28 standing step): the Apps repository moves its own publisher pin cfc92e84 -> e25aa76a,
# the squash merge of Site #533. Digest derived with sha256 over the edited file, never transcribed.
    "apps": "7823f26e59b1e4d8059aff5eafa7cf9691a0de6f9c49dc664c85c960da71b02c"
}
PUBLICATION_GATE_WORKFLOW_PATH = ".github/workflows/mbm-cross-estate-unification.yml"


# HC3, 2026-09-06: exact reviewed CI-only LundyLoop proof transaction.
# Full hashes remain checked on every Apps run, including files not in the diff.
# No standalone payload or arbitrary CI path is granted. Both gate copies match.
LUNDYLOOP_CI_PINS = {
    # SW2-T5R1: the shared browser proof is also required at reviewed bytes.
    # Re-cut 2026-09-19 (SX3 PASS 6, STOP-P1 control): the PUBLISHED table on its line 24
    # is now DERIVED from the Site admission registry by tools/sw2/pin_published_digests.py
    # (lessons "" 5c4e3ced, subject.html 93a071a8, apps "" f15bc17d), so the reviewed bytes
    # moved; digest taken from the edited file, never typed.
    # Re-cut 2026-10-22 (ruling ty, ty-2, option A): PUBLISHED re-derived from the Site cfc92e84 registry, the one
    # builder both estates now publish with (lessons "" d74addfa, subject.html b2a6f3cb, apps "" 53d82c52); digest
    # taken from the edited file, never typed.
    "tools/sw2/check_tokens_inert.cjs": "2cbb482b66a72cbba628fba80b8fbdd431553356c95a66d36614fa35189d6434",
    ".github/workflows/verify-lundyloop-professional-os.yml": "db2f0404944884869d84349a68b80858f81af8dbfb7eb64ddec71151f7928256",
    "tools/lundyloop/verify_live_bytes.py": "a27f791633260e7e2d8ba7ca2abe5a35db105b9ccbf96d26205628dcc1e636ad",
    "tools/lundyloop/test_live_bytes.py": "972ca2ae06da44722bfd011fda03a361c6011c699f95bb6ce78bca95b71f2e77"
}

ALLOWED_DIFF = {
    PUBLICATION_CALLER_PATH,
    "index.html",
    "apps.json",
    # Guarded by digest, not prohibition — the resources.json half of the same
    # ruling that pinned apps.json. The pin check above is what makes an edit
    # here deliberate-or-red; this entry only stops the boundary check from
    # forbidding the repository's ordinary business outright.
    "resources.json",
    "assets/mbm-platform.css",
    "assets/mbm-platform.js",
    "assets/mbm-theme.js",
    "assets/mbm-hub.css",
    "tools/verify_cross_estate_unification.py",
    "tools/verify_cross_estate_browser.mjs",
    # PIN1 Apps, 2026-09-12: exact internal trigger-derivation machinery.
    # Both workflows check its output; no payload or directory is exempted.
    "tools/pin1/derive_triggers.py",
    "tools/pin1/test_derive_triggers.py",
    # Git metadata, not a served file. It declares which payload docs carry
    # Markdown hard line breaks so the static-contract whitespace check stops
    # reading them as stray spaces. The first payload to need that ADDED the
    # file, which --diff-filter=MRD ignores; the second MODIFIES it, and a
    # boundary that reds on it would forbid the ordinary business of installing
    # a second bytes-unaltered payload. It cannot change a studio's bytes.
    ".gitattributes",
    ".github/workflows/mbm-cross-estate-unification.yml",
    "docs/MBM_CROSS_ESTATE_UNIFICATION.md",
    # renamed to pin_manifests.py under Ruling 3; the old entry stays so the
    # rename's deletion remains legal in any historical diff span.
    "tools/pin_apps_manifest.py",
    # RULING um, um add.1 (24 Oct 2026, reading (ii)): the 42 format collections a unit zip fully contains,
    # removed from the publication. Their deletions are admitted by exact path; nothing else, no folder, no pattern.
    "BUILD_ASDAN/FoodWise/Teaching_Packs/BUILD/downloads/BUILD_FoodWise_Autumn1_W1-W6_DOCX_Collection.zip",
    "BUILD_ASDAN/FoodWise/Teaching_Packs/BUILD/downloads/BUILD_FoodWise_Autumn1_W1-W6_PDF_Collection.zip",
    "BUILD_ASDAN/FoodWise/Teaching_Packs/BUILD/downloads/BUILD_FoodWise_Autumn1_W1-W6_PPTX_Collection.zip",
    "Careers/Teaching_Packs/BUILD/downloads/BUILD_Careers_Autumn1_W1-W7_DOCX_Collection.zip",
    "Careers/Teaching_Packs/BUILD/downloads/BUILD_Careers_Autumn1_W1-W7_PDF_Collection.zip",
    "Careers/Teaching_Packs/BUILD/downloads/BUILD_Careers_Autumn1_W1-W7_PPTX_Collection.zip",
    "Careers/Teaching_Packs/GROW/downloads/GROW_Careers_Autumn1_W1-W7_DOCX_Collection.zip",
    "Careers/Teaching_Packs/GROW/downloads/GROW_Careers_Autumn1_W1-W7_PDF_Collection.zip",
    "Careers/Teaching_Packs/GROW/downloads/GROW_Careers_Autumn1_W1-W7_PPTX_Collection.zip",
    "DT_Textiles/Teaching_Packs/BUILD/downloads/BUILD_Textiles_Autumn1_W5-W7_DOCX_Collection.zip",
    "DT_Textiles/Teaching_Packs/BUILD/downloads/BUILD_Textiles_Autumn1_W5-W7_PDF_Collection.zip",
    "DT_Textiles/Teaching_Packs/BUILD/downloads/BUILD_Textiles_Autumn1_W5-W7_PPTX_Collection.zip",
    "DT_Textiles/Teaching_Packs/GROW/downloads/GROW_Textiles_Autumn1_W5-W7_DOCX_Collection.zip",
    "DT_Textiles/Teaching_Packs/GROW/downloads/GROW_Textiles_Autumn1_W5-W7_PDF_Collection.zip",
    "DT_Textiles/Teaching_Packs/GROW/downloads/GROW_Textiles_Autumn1_W5-W7_PPTX_Collection.zip",
    "GROW_FoodWise/Teaching_Packs/GROW/downloads/GROW_FoodWise_Autumn1_W1-W4_DOCX_Collection.zip",
    "GROW_FoodWise/Teaching_Packs/GROW/downloads/GROW_FoodWise_Autumn1_W1-W4_PDF_Collection.zip",
    "GROW_FoodWise/Teaching_Packs/GROW/downloads/GROW_FoodWise_Autumn1_W1-W4_PPTX_Collection.zip",
    "Humanities/Teaching_Packs/BUILD/downloads/BUILD_Humanities_Autumn1_W3-W7_DOCX_Collection.zip",
    "Humanities/Teaching_Packs/BUILD/downloads/BUILD_Humanities_Autumn1_W3-W7_PDF_Collection.zip",
    "Humanities/Teaching_Packs/BUILD/downloads/BUILD_Humanities_Autumn1_W3-W7_PPTX_Collection.zip",
    "Humanities/Teaching_Packs/GROW/downloads/GROW_Humanities_Autumn1_W3-W7_DOCX_Collection.zip",
    "Humanities/Teaching_Packs/GROW/downloads/GROW_Humanities_Autumn1_W3-W7_PDF_Collection.zip",
    "Humanities/Teaching_Packs/GROW/downloads/GROW_Humanities_Autumn1_W3-W7_PPTX_Collection.zip",
    "Humanities/Teaching_Packs/LAUNCH/downloads/LAUNCH_Humanities_Autumn1_W3-W7_DOCX_Collection.zip",
    "Humanities/Teaching_Packs/LAUNCH/downloads/LAUNCH_Humanities_Autumn1_W3-W7_PDF_Collection.zip",
    "Humanities/Teaching_Packs/LAUNCH/downloads/LAUNCH_Humanities_Autumn1_W3-W7_PPTX_Collection.zip",
    "ICT/Teaching_Packs/GROW/downloads/GROW_ICT_Autumn1_W1-W7_DOCX_Collection.zip",
    "ICT/Teaching_Packs/GROW/downloads/GROW_ICT_Autumn1_W1-W7_PDF_Collection.zip",
    "ICT/Teaching_Packs/GROW/downloads/GROW_ICT_Autumn1_W1-W7_PPTX_Collection.zip",
    "ICT/Teaching_Packs/GROW_Computing/downloads/GROW_Computing_W1-W8_DOCX_Collection.zip",
    "ICT/Teaching_Packs/GROW_Computing/downloads/GROW_Computing_W1-W8_PDF_Collection.zip",
    "ICT/Teaching_Packs/GROW_Computing/downloads/GROW_Computing_W1-W8_PPTX_Collection.zip",
    "PSHE/Teaching_Packs/GROW/downloads/GROW_PSHE_All_About_Me_W1-W7_DOCX_Collection.zip",
    "PSHE/Teaching_Packs/GROW/downloads/GROW_PSHE_All_About_Me_W1-W7_PDF_Collection.zip",
    "PSHE/Teaching_Packs/GROW/downloads/GROW_PSHE_All_About_Me_W1-W7_PPTX_Collection.zip",
    "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3-W7_DOCX_Collection.zip",
    "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3-W7_PDF_Collection.zip",
    "Science/Teaching_Packs/BUILD/downloads/BUILD_Science_Autumn1_W3-W7_PPTX_Collection.zip",
    "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_DOCX_Collection.zip",
    "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_PDF_Collection.zip",
    "Science/Teaching_Packs/LAUNCH/downloads/LAUNCH_Science_Autumn1_W3-W7_PPTX_Collection.zip",
    "tools/pin_manifests.py",
    # The pass ledger. It exists to change on every pass — a boundary that reds
    # on the ledger guarantees false failures on exactly the well-behaved passes
    # that record their work. Ruled onto the list 2026-08-12 (Ruling 6). The
    # entry is harmless in the Apps copy, where no such file exists.
    "_teachgreen/DECISIONS.md",
    # ORDER AAV-NIGHT, 2026-09-05. The same shape as Ruling 6 above, recurring
    # because the campaign ledger was renamed and the boundary still names the
    # old one. A night order requires a ledger write on EVERY stage, so any pass
    # that touches the shared surface and records its work reds here on the
    # record rather than on the work — which is the failure Ruling 6 identified
    # and fixed for _teachgreen/DECISIONS.md.
    #
    # Every entry below is a file that cannot change a studio's served bytes:
    # two Markdown records, two gate tools that run in CI and ship nothing, the
    # CI job definition itself, and the §6c hub control. None is a served asset,
    # none is in CANONICAL_HASHES, and none can alter the standalone/offline
    # payload this boundary exists to protect.
    "_sownb/vb/EASTER_LEDGER.md",
    "_sownb/vb/EASTER_HUMAN.md",
    "_sownb/vb/tools/g26_reading_band.py",
    "_sownb/vb/tools/g28_cell_existence.py",
    "_sownb/vb/tools/mechanism_battery.py",
    ".github/workflows/fieldops-p2-and-sweep.yml",
    "tools/verify_hub_catalogue.py",
    # ORDER UX2, 2026-09-08 (Parts A and D). The same shape again: the order's
    # ledger (written on every part), the README (documents the size table), the
    # re-pointed chip gate, the UX2 gates workflow and its tools (run in CI, ship
    # nothing), and three DERIVED data files the hub reads at runtime. The data
    # files are regenerated by tools/ux2 and checked against their derivation by
    # .github/workflows/ux2-gates.yml on every change; a lesson edit regenerates
    # the size table, so a boundary that reds on it would red every ordinary
    # lesson pull request. None of these is a studio and none can alter one.
    "UX2_LEDGER.md",
    "README.md",
    # ORDER CX2, 2026-09-15. The same shape as the UX2 ledger: the order, its
    # working checkpoint (appended after every material result), the lesson
    # standard it cites and the recorded PLAY amendment. Documentation only;
    # none of these is a studio, none is served and none can alter one.
    "docs/orders/CX2_FINISH_2026-09-15.md",
    "docs/orders/CX2_CHECKPOINT.md",
    "docs/orders/LESSON_STANDARD_2026-27.md",
    "docs/orders/PLAY_BRAND_AMENDMENT_2026-09-15.md",
    # ORDER CX2, 2026-09-15. The source-admission tools. Each one stages one
    # reviewed replacement transaction: it declares the transaction in the GLV3
    # boundary, extends the reviewed-path list, refreshes the derived catalogue
    # records and re-cuts the pins. They run locally and in review, ship nothing
    # and are outside the publisher's public_file() admission, so none is served
    # and none can alter a studio.
    #
    # They are listed because of an asymmetry in this very check: the changed set
    # counts MODIFICATIONS, not additions, so each tool passed silently while it
    # was new and reds the first time it is touched after its branch merges. That
    # bit the CX2 checkpoint above and then tools/rw1/admit_w8.py, whose review
    # base must move to the current main on every re-admission. Listing the class
    # rather than the instance that happened to fail.
    "tools/grow_resources/admit_w3_friction.py",
    "tools/launch_resources/admit_w4l1.py",
    "tools/launch_resources/refresh_w4l1_pack_records.py",
    "tools/science_teaching_packs/cx2_sugar_r10.py",
    "tools/rw1/admit_w8.py",
    "tools/rw1/cx2_lane_d.py",
    "tools/verify_lessons_chips.mjs",
    ".github/workflows/ux2-gates.yml",
    # tp add.2: the UX2 census reporter and its controls follow ux2-gates.yml's proof
    # outputs; a proof added there must be added to the census in the same change.
    "tools/ux2/drift_census.py",
    "tools/ux2/test_drift_census.py",
    "tools/ux2/hub_gates.mjs",
    "tools/ux2/unit_tags.py",
    # UX2 D3 added the companion-pack deriver and its placement manifest but did
    # not list them here, though every peer is listed (build_spine, unit_tags,
    # resource_sizes, calendar-spine.json, resource-sizes.json ...). The gap was
    # invisible because it only bites a PR that changes one of them AND this
    # file, which only a contract re-pin forces. pin_catalogue_contract.py --
    # already allowed -- imports the deriver and reads the manifest to rebuild
    # the pack tail, so both are catalogue-record machinery, not lesson payload.
    "tools/ux2/companion_catalogue.py",
    "data/companion-packs.json",
    "tools/ux2/check_catalogue_schema.py",
    "tools/ux2/prove_catalogue_gate.py",
    "tools/ux2/build_spine.py",
    "tools/ux2/resource_sizes.py",
    "tools/ux2/fixtures/hub-hrefs-before-ux2.txt",
    "tools/ux2/fixtures/appendix-a-lessons.json",
    "tools/ux2/fixtures/retired-hrefs.json",
    "data/calendar-spine.json",
    "data/resource-sizes.json",
    "data/planning-keys.json",
    # ORDER UX2 Part D2 (2026-09-08): each subject's checksum manifest is
    # regenerated in the content PR that places companion packs (the order
    # requires it). A checksum list is a record of bytes, not a studio; the
    # gate that proves the packs is tools/ux2/check_companion_packs.py.
    "Humanities/Teaching_Packs/SHA256SUMS.txt",
    "Science/Teaching_Packs/BUILD/SHA256SUMS.txt",
    "Science/Teaching_Packs/GROW/SHA256SUMS.txt",
    "Science/Teaching_Packs/LAUNCH/SHA256SUMS.txt"
}

# rm-2 (13 Oct 2026; a red-first plan, local build): the ri-5 Group 1 scheme-source edits. These are
# workbooks and their text dumps, not served files. Each path is admitted through the boundary only while its
# bytes equal the sum below: no folder, no pattern, nothing else widened.
SCHEME_SOURCE_EXACT_SHA256 = {
    "_passpq/DECISIONS_YEAR2.md": "045146ae58357f4f92996be5d2f4a3c6e5293cffd19e1bd4d37e9064ea213461",   # rp-2 (a): Group 2 record line, not served
    "_sownb/VB_STATE.json": "fd21c2f5a6affaf7b5f495af3b2e8831897493e361ed7de50ae57e5bb85eb01d",   # rp-2 (a): Group 2 record line, not served
    "_sownb/vb/WRONG_BEFORE_RIGHT.md": "37adc9cf88a7f9832e8844e1f8681e9bfb76fb8866d6f53959a05add42b521bb",   # rp-2 (a): Group 2 record line, not served
    "Build/_Archive_VersionA_LivingIndependently/BUILD_SOW_2026-27_vA_with_LivingIndependently.xlsx": "b5cee8c3413e0487c630331057deb1b16c03805084e113e96094a3d2cadc397f",
    "_authoring/science_2026-27/_toolchain/scheme_references/BUILD_SOW.xlsx": "b5abd199abfa8c3de4608533fcef9e917a61b148419a102dfff6708302139cd0",
    "_authoring/science_2026-27/_toolchain/scheme_references/GROW_SOW.xlsx": "41ff0a4a4211da89466f5634f58a5074b6f4be6c7036118aab1e0e9d3145d7b3",
    "_authoring/science_2026-27/_toolchain/scheme_references/LAUNCH_SOW.xlsx": "b8063b7d6b3989f71375b5f2c3a62b9ebcd3be1bb1933706a009473c7b19ee02",
    "_passla/inputs/LAUNCH KS4 - 2026-27.xlsx": "92ceefa450b770af738a1a65797047555c796e890c19cb54286662968fde90a9",
    "_passsb/inputs/Build SOW 2026-2027.xlsx": "b5abd199abfa8c3de4608533fcef9e917a61b148419a102dfff6708302139cd0",
    "_passsg/inputs/GROW SOW 2026-27.xlsx": "41ff0a4a4211da89466f5634f58a5074b6f4be6c7036118aab1e0e9d3145d7b3",
    "_passsl/inputs/LAUNCH KS4 - 2026-27.xlsx": "b8063b7d6b3989f71375b5f2c3a62b9ebcd3be1bb1933706a009473c7b19ee02",
    "_sca1/inputs/BUILD_SOW.txt": "6491c014baba83b6091686a4e40156b94443341265432786db41c7c67a52df42",
    "_sca1/inputs/GROW_SOW.txt": "e034ba648284b16ac3388b6e0ea441e34072ac30ab7286780b243f41ef7f39c6",
    "_sca1/inputs/LAUNCH_KS4.xlsx": "92ceefa450b770af738a1a65797047555c796e890c19cb54286662968fde90a9",
    "_sca1/inputs/LAUNCH_SOW.txt": "5881aaaedc0fcb238ccac9549b79176fcac4a5cbdd7c610cd1e77b0ee3c85d1d"
}


# RULING wa-2 (c) (26 Oct 2026): M1, the subject-folder rename. The files M1 edits in place (outside the moved folders)
# whose new bytes are the rename map applied to their previous bytes (with M1's digest re-pins), each admitted by its exact
# reviewed digest -- the same rule as SCHEME_SOURCE_EXACT_SHA256, no folder, no pattern. Generated from the new digests
# of those files; the proof that each reproduces is in the readback. Any other byte in any of them reds as before.
M1_RENAME_EXACT_SHA256 = {
    ".github/workflows/arts-award-legacy-reader.yml": "7a913da583eb3af9ade0a5f0e434611f911da34c45f093a0169794ad1c9a6a7a",
    ".github/workflows/arts-award-reader.yml": "73fba96fa95fe427f490594011231376fe4df8b9cdb842721930cb4dffdc114e",
    ".github/workflows/glv3-production-byte-check.yml": "b0de87ca9bc68553b14a05c2f8c0ece512acc75ee1066d77aee6be3ea8f25f0e",
    "BUILD_Estate_v3/index.html": "302893d70d13f5ed91521614e9bc5f156f3a1fa32a93c32fce0d3cb465de3d1f",
    "GROW_Estate_v3/index.html": "e39e4acf6cf1b85b03cb444dc30380a88174ae9f302132b38da305e6decb148f",
    "LAUNCH_Estate_v3/index.html": "a1beccc6e45ac8484d2be9d56815fdec7cb3db99b9ed6599f52351df38b36255",
    "Launch/Slideshows/LAUNCH_ART_W8_Complete_The_Review.html": "cac083b1fa61722545dd14c4597aa3dcf236b5ed05eb8416d4276b71501406e8",
    "LundyLoop/tools/print_pack_audit.py": "a2297e2db4a0c91b4dcb5f54bc9254f28e7b5962442e806fe55cc6de30db26b0",
    "Teaching_Packs/LANDING_MANIFEST.json": "60db3016994171e92ee00e8ed76eaf39d4724f9b5322fbdab2ad64ba6f357078",
    "Teaching_Packs/index.html": "358d350e6bfd5bfd64d1e08745c3af0aafb73f2b4e1d09360b40085d45d5d461",
    "_glv3/COUNT_RECONCILIATION.json": "db359403e422d260bde5ad4800f31238ef72ef692de226dde937fc5c04b668ea",
    "_glv3/GATES_STATIC.json": "3dbfcc8a6b3ee1584e40151b7092b6562f5e52d5129ba43eb57195167e3b502f",
    "_glv3/INPUT_INTEGRITY.json": "9356996b209ea80db820a892afc2babf4499fa52f4dd2794439661306abe3020",
    "_glv3/PROTECTED_TREES.json": "88b091c791c5de41df74cb1176fff94a8508b83428ecfa00d7a1e9ffcdc05fef",
    "_glv3/run_manifest.json": "f56b52d992d6fd0ade237e4758e930512e741f7041dabc0cf33475f7e0d47fed",
    "_sownb/feb/tools/g18_content_floor.py": "7ba0fa91a6462a3603387bff57023ddb813e75f5fda0cb995c04b702776e3718",
    "_sownb/feb/tools/g18_measurement.py": "37d79bb3d0b3fab60abaca58b1da099b867cfe08f1f70b22a50a469d2c5758f5",
    "_sownb/vb/tools/attribution_control.py": "6583d41561555b64a1d01e92cf7b5c71ba52a50a1442eb60c664b8e2393708ab",
    "_sownb/vb/tools/cell_coverage.py": "255d6df5e9524aeb44ad186f2fb3ba46d4ed037d04a9a1e698d7f5a83409e17a",
    "_sownb/vb/tools/g18_v2_family_floor.py": "c368d6600e44a782c6499273664f7802282660554d3d72fa5eed701556937ea0",
    "_sownb/vb/tools/g29_plan_binding.py": "6cce40c3b0812e145209459b7d2228ebfc8131f80c966552ddbd7ee1ed966264",
    "build-anim/inject.py": "5aff881a7a3b874eede704128e44d20f2bb70105e21b74bf4cd042aedd2cbfa9",
    "checksums/SC3R2_BUILD_A1_W08/SHA256SUMS": "035dbbcec311aa22818ff362f7a72a74e58a9f4e2338ce98cb5d56a083fb0015",
    "checksums/SC3R2_GROW_A1_W08/SHA256SUMS": "771bcbae1b106f7621ab2d2e04540b208845fc587906afa939592b45fc8d1de9",
    "checksums/SC3R2_LAUNCH_A1_W08/SHA256SUMS": "6af50dd7e73bf6c53fbfd274384227f4491c7109bc6be6a956703123ffe922ab",
    "grow-anim/inject.py": "9e4713ce537b37692593e5c9a185e8a5f17f24e45782a768b1e39bbe6e256b0c",
    "grow-anim/wire_lessons.py": "f047f8e88fad8b22219a8bd005a1aa19c3d43bb835abf0dcd76d605669845720",
    "quality/LESSON_AUDIT_SCHEMA.json": "e8488124a719d0f8aa535fdfbbfbc1cb1b7ff2ace86d83090bb9494da2816406",
    "quality/LUNDY_HUMANITIES_SPECIMEN_MANIFEST.json": "9e4576581922d9a1673657175eb13a4089de73b369a194ec6466a35548c04b3a",
    "quality/QUALIFICATION_CLAIMS_REGISTRY.json": "94e863e707b5b0c1b434a6dd4d19f9a37738bc6ae6770ae6eda96e46c566e1f0",
    "review/estate-exec/validate_estate_exec.py": "7024b5dce23969ef3b809fefbedd8bfa2eb75ad3ec3614a9ab5939d59d4a4599",
    "tools/artsaward/BRONZE_ACTIVITY_TARGETS.json": "7b9b2d2ecb2a686db77d190ed18fe4cd6a7772ea2f6fe84c8a6cb4a831c665c3",
    "tools/artsaward/BRONZE_DONORS.json": "ed5db7ffec5ddafa8d1d8575a96392ea6e6824c494c724155f1dd60b8b86f21b",
    "tools/artsaward/BRONZE_TARGETS.json": "f6582503d52952a49a98d8d0dcef8f795f467428be24ebd728ee07e37b7bfcbd",
    "tools/artsaward/EXPLORE_ACTIVITY_TARGETS.json": "3f217eea5e576d71270a9892f4d077449d870e1ccd8c3f0c83b877b8253da6b6",
    "tools/artsaward/EXPLORE_DONORS.json": "b92450611a4af8a2e15156a12ae199fdaee2469123c5cbf6ae625e0dc5396234",
    "tools/artsaward/EXPLORE_TARGETS.json": "51445d99ee7c52a10c4d2f1788f216a07a8fb5755107a3217c325e2256ce1d8f",
    "tools/artsaward/SILVER_ACTIVITY_TARGETS.json": "7ad6ca91eef5092ba375056c5413391e5b8f08dcbc490567733175a4cb53280e",
    "tools/artsaward/SILVER_DONORS.json": "e155f4e35d2d63c9fce2d05bebaa711fc87d12de93ed3ad5495ea1fdd24622a1",
    "tools/artsaward/SILVER_TARGETS.json": "d42052c0da3faa5c415c6a6a5996b380881a145b5d9e4c36efce606e5a4ab097",
    "tools/artsaward/legacy_slot_adapter_selftest.cjs": "7b00b6819b6093d1528f1a4c8e6d2b9f1f10ccceec079c5b073018091285df1a",
    "tools/artsaward/legacy_slot_browser.cjs": "b75f066f982bc8887a47f1a8caadb8fd00d76390e66c68edb20ff103134d7d2c",
    "tools/artsaward/venue_classify.py": "c4e7a6ae50635e0832674640df3f008e33369d4f747dca67f1ba1c70a367ff1c",
    "tools/build_resources/W8A_ACCEPTANCE.json": "9475262a4e6389a5145f4c7f2af7c70e1d561eacd7160d56941726a2f70a7dde",
    "tools/build_resources/admit_sx3_release.py": "2d7c7309e81b1f7bddc82c03d5720116e2eac23a49626716d11b660f98e01515",
    "tools/build_resources/admit_w8a_chassis.py": "69ec305cb48ff64f232be7ee67dbd9bef8be789271d22a8b0e78bd97805d7c2c",
    "tools/build_resources/author_w8a_chassis.py": "88a3cefc8e7a6930d65afbe22d818008c9838347681622e7fe16c381e410acf4",
    "tools/build_staff_pack.py": "2e7d2063e10018004aad5c4439584377ef8316d5c48ba52d8280cf9c6a0d1cae",
    "tools/catalogue/PUBLICATION_ARCHIVE.json": "54f917e15f56f3988fed321e5696bc61ecaa234123599e539abf3863f909a729",
    "tools/catalogue/prepare_dy4_bind.py": "1dc4bccf7d53f042beaa6d42af638e25a6a17e121c309660ae1b1afcc19e273d",
    "tools/catalogue/test_build_catalogue_merge.py": "a059308af1159a27fcd66c88b3fd164122d918f82b3eb63ae22402ba9a5f7285",
    "tools/chassis_census.py": "6f32664de6cc0ed489b1298c552cd98c2b9adc5ec22467c48655af1cd55c932f",
    "tools/cx2_r10_estate_sweep.py": "2f61e24d93ff0d73383f0baa3c1b61e6bb30ecb9162fb97027901d8b480d9569",
    "tools/donors/ART_DONOR_v1/GROW_chassis.html": "2f24f54692fb7ab70799fc611eeaffb4b690f36031c40aba72e3f990493c8244",
    "tools/donors/ART_DONOR_v1/README.md": "5d0a13d1998c28f488cf36ddc54a33749c171ed235a5cf84806bbd3e7e5af5e6",
    "tools/downloads/definitions/bronze-arts-award-main.json": "0012f6ec4689b7d1157777ebe4c85084cfd8d867cbc0d4e20c2cd052373e66b6",
    "tools/downloads/definitions/build-science-aut1-main.json": "43ff4716dca29a734f54e77c8d1f889d250ae954a57ae8ffeaa116e9df081c88",
    "tools/downloads/definitions/build-science-aut2-main.json": "1114bdea6165202760e83e859dfa6ea57f636a717bb7c3daf8d9d34bfd4d4120",
    "tools/downloads/definitions/build-science-spr1-main.json": "d7a8866f53df4be8a26f47f1c869f6dcd70a0ab858606c0ce53c5e929b4c39d4",
    "tools/downloads/definitions/explore-arts-award-main.json": "0e38be04758decb564219c75d8a790228a89b59337c9c9efa52f387d9329d4ee",
    "tools/downloads/definitions/grow-science-aut1-main.json": "8f78d60e707a29a798bbca2cbd08cdfe59454cf5f3921e2346bee64d6353647b",
    "tools/downloads/definitions/grow-science-aut2-main.json": "f3bdc04b72895c032a24db6ea22caea65995c6c8b77bbfa84c85d441bac28552",
    "tools/downloads/definitions/grow-science-spr1-main.json": "2ee78a7886548383cd1d6836ad96883b3a7ae36f4752d4c3dab50db92a93efa0",
    "tools/downloads/definitions/launch-science-aut2-main.json": "4631fd2952e7e2165e15730de55db4ebddee6612230c6cffe0c205dd299a0398",
    "tools/downloads/definitions/launch-science-spr1-main.json": "1373c1fe6b5e847e27d38a11f913066ce6b192e96eaf1aab2d4ee6fc34153db8",
    "tools/downloads/definitions/silver-arts-award-main.json": "46d88cb7b4676dfec884a5016cf7e34485ecfeb51006faabc1d88a48082ac4e6",
    "tools/downloads/test_science_offline_pack.py": "0880a4cd3c298489e65a5d357806ddcfa7f36127d3c69b8103744019cd9564d7",
    "tools/downloads/verify_definitions.py": "c8e9c2e4b8b4d8cc2fa0605f645d95d72d6223d5ba7c69d1d52db015cb4a2443",
    "tools/easter/BATCH3_DONORS.json": "9cd370ae1d160870c008721b2342fe7638aaa19307863bd2ac6ac0f7bfe769ce",
    "tools/easter/BATCH3_TARGETS.json": "5fed7ba3d275f158d34322d348dc6fc9ff0e58357003e62382037ae31a12c107",
    "tools/easter/BATCH4_DONORS.json": "e7ecd9d778d662d474708a4b27ee002c9137424563ec06f90ffb32280c33d164",
    "tools/easter/BATCH4_TARGETS.json": "28f973153b4d4583d6cd03281b3997c5a89effa5b95c6cf66d8aeff39fe88cac",
    "tools/easter/CLASSROOM_LIGHTER_TARGETS.json": "abc8df5f4eae80145c26f44276be9a223a7b1a007d189f90975bc2cfbe735a10",
    "tools/easter/CLASSROOM_TARGETS.json": "891ae955f3b06229427a6e1041c463a027032b93f7881865c85747ec4f82c526",
    "tools/easter/EASTER_TARGETS.json": "3f67b567c4d8cd103bc183ac78afcea998a385e2a4e56e5903e2755b4408b89a",
    "tools/easter/GREEN_REFERENCE_DECKS.json": "9bca2e3db355e469df24498bd0543a93826fa180e29b3b8b3d0b440bcef90062",
    "tools/easter/award_browser_fixture.py": "a0980d43cf3e3db7be0478d8c78d1cd26343c0c8964328c4635e1e2cbf2dd29b",
    "tools/easter/build_batch_targets.py": "265958d5d8e9379cdafbee8b7120de614a5bd04d8186a717cc1605c9b82cf1bd",
    "tools/easter/build_from_specs.py": "462542d256dbfe617565b7bb416fc10e805e853398f8306a9d301e4088a8df82",
    "tools/easter/chrome_flip_list.py": "121ff7ec92c357532968b0b5359ca4ed4fdacc204c4f7686d6ebc56bea30e605",
    "tools/easter/dedupe_sweep.py": "2eedc923cb58920e444775d63fa05055359ad5d9013a989593192d71176d86a9",
    "tools/easter/manifest_sequence.py": "172503d7d5eb10a24eeca2ad7fda539b9921ffb11203e8b8b4e5a440ab1de877",
    "tools/easter/pick_art_donor.py": "089d04a5882f8161541e89eb6bc531971a1aa1c658c11acf9014e254216cf098",
    "tools/fieldops/README.md": "403825ff409337675d95ccde06fb5c022aeab1cee7fadb98ee21606605387460",
    "tools/fieldops/build.mjs": "216f493a1307b497ca75a0b1c7734bc3f18de572c2348676f83e3b08f533fe7c",
    "tools/fieldops/controls.mjs": "705af245197977fb47338155ad190942884fc6aceb9a914a77e0d7fe8f0ecab3",
    "tools/fieldops/split_transport.mjs": "3d818e13bd672bc294fa354bfe04ce0f502f90b2d9b8ce669b0bc126d25cbefe",
    "tools/fieldops/staging/00_BUILD_FieldOps_Teacher_Studio.html": "407439c9c76fcd87064b2e9ed1c31bd6d0d295dd89f4740062d263512720d3aa",
    "tools/fixtures/pr124/workflows/glv3-production-byte-check.yml": "b0de87ca9bc68553b14a05c2f8c0ece512acc75ee1066d77aee6be3ea8f25f0e",
    "tools/fixtures/pr124/workflows/glv3-verify.yml": "c9e59c8ae624c8a997b3bd9b3782afdcfbf73806969a6f6ebab66cd8d67bc983",
    "tools/grow_resources/arrival_checks.py": "bd8362be676e8fc7ce1dcc8e23af7c89ff67fe3ee3e2935565fe692ec166daf9",
    "tools/grow_resources/author_w3_feedback.py": "c94409a281b5c03c1c97ae03e5350ac747bd6e56d37859facd76af556aa4ace3",
    "tools/grow_resources/author_w3_slides.py": "4fceea67e275f6f1672fb968f4a30e57d76c47f68a445767527e4deae6540c25",
    "tools/grow_resources/author_w3a_arrival.py": "2738c0404563e2326a7502dee27be2aa5fae2d1c775dc49ec5d877ba0f98ab5a",
    "tools/grow_resources/author_w3a_organiser_exit.py": "cc8060cafea0014d7d1a55ad810c61ebd1da81d40cbb268ca9d1992fe5f7d854",
    "tools/grow_resources/browser_checks.cjs": "cc210c3e3c42c1a3c0427e01e34bc5bb1fb9635e6d2f147160f5ea375e5dc715",
    "tools/grow_resources/build_resources.py": "859e7401228a8d98b89f2ff0b0caee465b7ad4234f6650fa03fbaa5705d2d3e2",
    "tools/grow_resources/check_resources.py": "c471de9f2d24e4421c13102210d8c4a9a7e0d533e475ef532f442d3634731b1f",
    "tools/grow_resources/feedback_checks.py": "aefee5e30756327e49e5eefcba1a91090d4301ef36ebbc5b30f2d5a5a74bd5cf",
    "tools/grow_resources/focus_checks.cjs": "75d08c268252d1782daa5708ac63cec74e769754adb7d1a40de5c3a18727f7ce",
    "tools/grow_resources/friction_acceptance.py": "f9d71e35e83a16e0292f0f3ff6f769a5128b8952eff3d9e3075c02fb932ba6fb",
    "tools/grow_resources/organiser_exit_checks.py": "bfed534d64285302de29f3f4e841a15de7c34b48c0b8d124e0d9a05a86d1cd0a",
    "tools/grow_resources/refresh_w3_pack_records.py": "1f010687251fd64d4070992e7157e77de6c648b412999a42c9c639566a2d97df",
    "tools/hum/DLG1_PAIRS.json": "dd4c854af722e969c4261e748942a20f8f4db8ade44649538df0b0e16f8a1618",
    "tools/hum/arrival_week_exceptions.json": "ad0e1a8fea71ecccfb3707cefa423af4d027c02cd0602a4c4f6d67339aad3e87",
    "tools/hum/check_arrival_surfaces.py": "3aa54c8ab3946d2c078eca0073bb9a9369325d5f968e2e7e347e23b1e1431c34",
    "tools/hum/check_carrier_pure.py": "ca86a43031c4bfec0e559759d020ec5ef9029b56b16310cbe0fe57d381500ba6",
    "tools/hum/check_dialog_audience.cjs": "f9fa4688772bb012a73d614a4799aa36667aca2d9562fbcd7cc030bf3f10018c",
    "tools/hum/check_lesson_floor.cjs": "76bbb898e50f26e24c0f1a7a67c1246eeb114454745a9e834bd8d681352e9d87",
    "tools/hum/dialog_audience_exceptions.json": "66986cf0f627b6dc78094cbbef889e396ced511a1a11edaa14fffd074a0856e0",
    "tools/hum/fix_dialog_audience.py": "ebe88f05eb8cc8ee4ff7214e720e33ac1c4f2bdfcdc1d8f05876b7a868222f36",
    "tools/hum/lesson_floor_known_red.json": "2a3795e23fbd1d77bcd313ef2b60555ac1a716328ecc269625faf387ac12014f",
    "tools/humanities_resources/STATIC_CHECK_RESULTS.json": "d8512ae1801218656d880ae9cc2d54603633f074d1d5ad8dde52c35f95b5fae0",
    "tools/humanities_resources/browser_checks.cjs": "3cd28955bac641364275700c1021dd901691b14ed66dc2a678a79b2787ea677f",
    "tools/launch_resources/W4L1_ACCEPTANCE.json": "f76b26e3cccb5926665c0ad43cfc9de43434b12ce2fd2d35afb98dbad437fe0e",
    "tools/launch_resources/author_w4l1.py": "a4c97b467aa101320099ffb00605ab5e71d8c2895a6e4c8c8f79a494e0de9b9f",
    "tools/launch_resources/author_w4l1_natives.py": "62dd0ef2244c9833cbc63e1a865878ea854b3b4f194710f408c12641cd417a38",
    "tools/lf1/check_admission_move.py": "b3751f7b034ea3e677ba7e3851b1b799d98986bdb4e828e9a632f44a801b59e2",
    "tools/relabel_public.py": "c81e059367a92c4cd30559853aeec35e53c9a4c7ceed31dd249b21cf82df0b9d",
    "tools/rw1/clear_home_link.py": "4481025a3caa09ee04ac9b8adea6d228cff3f0cbcd285b643829366ada06924b",
    "tools/rw1/dock_guide.py": "90a29d9f5497d46c79b061cd7f9287cae4694da6f7005c62b775b4a4f5fc1610",
    "tools/rw1/edits/W8B_plain_language.json": "5f3fa6d7b60ce5fcee2e0c8a222b4d7fa96d96265b3628ddaa6e60602e209dbd",
    "tools/rw1/parity.py": "392a6c5c53903384efee998f7257cdef200adf957bfbff83f7f57d4ff92adecc",
    "tools/rw1/pathways.py": "5bdc3d505903925c1d4abd7cd89a0ea3150e237e287183b7e79ef8bfa4796889",
    "tools/rw1/restore_lesson_config.py": "61f6b614a4bb22b15e85be538704eee6aa7585e9a88de38818b93d9b96f7f7e5",
    "tools/rx3_land.py": "92751ac6fb8885ac5f67dd3333f8dc3f894d2951d087a9727a86596f48032c17",
    "tools/sci/select_manifest_decks.py": "94e410bf7039c2cfe3e8ef10c1fa55d788cffb2c11a91e987844f1c9b9721d7d",
    "tools/science_pack/RESOURCE_CONTENT.json": "499da104f87c775b6de314d78477decba79baf41cbcf8ae6ea60637c66c35c70",
    "tools/science_pack/check_resource_dom.cjs": "ea837caafd3e6ddc1e966d7e731272f314c129a69999bf747b3e8c946150640c",
    "tools/science_pack/model_fixtures.json": "0c1f9689780131efc3bc2c251176a36ba1aad206b2eb594034c0a21784719667",
    "tools/science_pack/rebuild_resources.py": "ca3d4f06c2bb929ca2432d633450be6ae06a2bc1566bf3c235e57c8e92e46c6f",
    "tools/science_teaching_packs/cx2_s3_offline_edition.py": "6bba82926beb47bc49f6dd8acd06b3753762880a48de1f25460caa22b987ad4a",
    "tools/science_teaching_packs/test_source_binding.py": "f076213cfe8f8dfeaccef780a746191d86412f29380be232696e67442eb4abbc",
    "tools/stage_b_announcer.py": "41c95d4a3dcccb871d9edc0d9e0f023bb8930dec14e0c1ad6b9d383322bd3f6b",
    "tools/sx3/admit_landing_decks.py": "2ec9498f93c74079c007f31c76ec3dd6a0b82f15c3faaf6172b5a8252f3c0d54",
    "tools/sx3/align_shelf_titles.py": "826fe78ab4781d3d49418c7a97f844695539c43190f6122bae5a351ef8615dce",
    "tools/sx3/check_landing_titles.py": "446ca22a7adf531211bc346aea29029593e5141c699185582d12d65951409e55",
    "tools/sx3/test_admit_landing_decks.py": "536d68a8292e096a02aea30131f7e555b7591eff0f21748c8ef7d10e5e2278a7",
    "tools/ux2/add_edu_q1_companions.py": "b176374b6be6b49575e6daf42b720cc40e2df7642cf683f639ebb3bea09c5d63",
    "tools/ux2/lesson-outcome-baseline.json": "6590bec9c3ad848e87f8fd1237abb140d0e566e33bedfece69391a980c29ff7f",
    "tools/ux2/place_companion_packs.py": "3b6396a5397b6eceaa42885986f9fb7b5acc37d653ff7c2e1c6e31a25c9379bc",
    "tools/verify_fieldops_served.mjs": "af04a4099c6bb89d7787b8057f80a4aa842495b90da18b357e5b5b977344b0d7"
}
# RULING wb-1 (26 Oct 2026): the two Art manifests of the GROW and LAUNCH v3 trees, moved by M1 outside the protected
# trees and rewritten by the rename map only (each reproduces byte for byte), by exact digest.
WB1_MOVED_EXACT_SHA256 = {
    "GROW_Estate_v3/Art/manifest-v3.json": "8f376fd9fbf6d808481ad49098c452d0eb97cf3af3a0fa73cfcf7fc8307a6af9",
    "LAUNCH_Estate_v3/Art/manifest-v3.json": "e76aa2a810ba4a958028096b9b80f25090feb0f97347f7acf55e70636244512d"
}
# RULING wa-3 (26 Oct 2026): the BUILD D&T community hub, title and heading only (the word dropped), by exact digest.
WA3_EXACT_SHA256 = {
    "build_dt_upcycling.html": "3091a2e84328bef46aa9ecb532dbb5f64e46bd037037ed8f7daee5a41037d876"
}


def exact_byte_admitted(root: Path, changed: set[str]) -> set[str]:
    exact = {**SCHEME_SOURCE_EXACT_SHA256, **M1_RENAME_EXACT_SHA256, **WB1_MOVED_EXACT_SHA256, **WA3_EXACT_SHA256}
    return {rel for rel in changed if rel in exact and (root / rel).is_file()
            and digest(root / rel) == exact[rel]}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def detect_kind(root: Path) -> str:
    if (root / "resources.json").is_file():
        return "lessons"
    if (root / "apps.json").is_file():
        return "apps"
    raise ValueError("Could not detect Lessons or Apps repository")


def extract(regex: str, text: str, label: str, errors: list[str], flags: int = re.S | re.I) -> str:
    match = re.search(regex, text, flags)
    if not match:
        errors.append(f"missing {label}")
        return ""
    return match.group(1)


def normalized_visible_body(text: str, kind: str) -> str:
    body = re.search(r"<body\b[^>]*>(.*)</body>", text, re.S | re.I)
    value = body.group(1) if body else text
    for tag in ("header", "script", "style", "noscript"):
        value = re.sub(fr"<{tag}\b.*?</{tag}>", " ", value, flags=re.S | re.I)
    value = re.sub(r"<!--.*?-->", " ", value, flags=re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html_module.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    if kind == "apps":
        value = re.sub(
            # Normalised OUT of the wording comparison because the count is derived
            # from apps.json and asserted exactly, below, against number_word(total).
            # The old alternation enumerated "Twenty-eight|Thirty-one", so the next
            # legitimate count stopped matching and the gate reported Matt's authored
            # wording as changed when only the number had.
            r"(Your offline creative workshop\.\s+)"
            r"(?:[A-Z][a-z]+(?:-[a-z]+)?|\d+)"
            r"(\s+single-file studios)",
            r"\1{DERIVED_COUNT}\2",
            value,
            flags=re.I,
        )
    return value


# ORDER FINISH-2, manifest-pin ruling (2026-09-20). A pack-scale population cannot be
# carried as exact per-file pins. PIN1 materialises one trigger path per pinned file,
# and the HUM-D5 packs' 1750 pins took the derived workflow to 534,033 bytes -- which
# GitHub would not load at all: three push runs ended instantly with zero jobs, no
# pull_request run was ever created, and so this gate never ran on the pull request
# that landed them. A gate that cannot start is not a gate. The packs are therefore
# pinned by their own SHA256SUMS manifest.
#
# This function is what stops that being a loosening. Every member a pinned manifest
# lists is digest-checked here on every run, exactly as an individual pin would have
# been: the coverage is kept, only the indirection changes. The manifest's own bytes
# are pinned in CATALOGUE_PINS and checked by the loop above, so a manifest edited to
# admit a new file reds on the pin before the list it carries is ever honoured.
#
# Scope is exact and explicit: a pinned manifest is expanded only at
# <root>/<one path segment>/SHA256SUMS.txt for a root named in
# CATALOGUE_PACK_MANIFEST_ROOTS. The first root is the shape the HUM-D5 packs land
# in. The PIN1 re-pin ruling (7 Nov 2026) added the rest: PR #811's exact per-file
# pins took the derived workflow to 567,566 bytes and GitHub refused to load it
# again, so the non-HTML members of the Science Autumn 2 packs and of the Autumn 2
# engagement editions moved to manifests under the roots listed below, one root
# per pathway-term, lesson or pack folder. Members under every listed root are
# expanded and digest-checked here on every run. A root not listed is still not
# judged: the Science/Teaching_Packs manifests and the pathway-level Science
# manifests (W8-W13 and the like) stay outside it, so no file that was never part
# of a ruling is newly judged here.
CATALOGUE_PACK_MANIFEST_ROOTS = (
    "Humanities/Teaching_Packs",
    "Science/Build/Autumn_2_2026-27",
    "Science/Grow/Autumn_2_2026-27",
    "Science/Launch/Autumn_2_2026-27",
    "Art/Build/ART_BUILD_A2_W05_P1",
    "Art/Build/ART_BUILD_A2_W05_P2",
    "Art/Build/ART_BUILD_A2_W06_P1",
    "Art/Build/ART_BUILD_A2_W06_P2",
    "Art/Grow/ART_GROW_A2_W05_P1",
    "Art/Grow/ART_GROW_A2_W05_P2",
    "Art/Grow/ART_GROW_A2_W06_P1",
    "Art/Grow/ART_GROW_A2_W06_P2",
    "Art/Grow/ART_GROW_A2_W07_P1",
    "Art/Grow/ART_GROW_A2_W07_P2",
    "Careers/Build",
    "Careers/Launch",
    "DT/Launch",
    "PSHE/Grow",
    "RSE/Launch",
    "RSHE/Build",
    "Vocational/Build",
    "Vocational/Launch",
    "ICT/Teaching_Packs/GROW_Computing_Autumn2",
)
CATALOGUE_PACK_MANIFEST_NAME = "SHA256SUMS.txt"


def catalogue_pack_manifests(pins: dict) -> list[str]:
    """The pinned pack manifests whose listed members this gate expands."""
    roots = [root.split("/") for root in CATALOGUE_PACK_MANIFEST_ROOTS]
    return [rel for rel in sorted(pins)
            if rel.split("/")[-1] == CATALOGUE_PACK_MANIFEST_NAME
            and any(rel.split("/")[:len(root)] == root
                    and len(rel.split("/")) == len(root) + 2 for root in roots)]


def catalogue_manifest_entries(root: Path, rel: str) -> tuple[dict[str, str], list[str]]:
    """Parse one pinned pack manifest into {member path: reviewed digest}.

    An unreadable, malformed or empty manifest returns an ERROR, never an empty
    mapping. Treating it as "nothing to check" is precisely the silent gap this
    indirection would otherwise open, and it is the same refusal fence_errors
    makes for an unreadable fence.
    """
    try:
        text = (root / rel).read_text("utf-8")
    except (OSError, ValueError) as exc:
        return {}, [f"reviewed pack manifest could not be read, so its members cannot be honoured: {rel} ({exc})"]
    entries: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        checksum, separator, name = line.partition("  ")
        name = name.strip()
        if not separator or not re.fullmatch(r"[0-9a-f]{64}", checksum) or not name:
            return {}, [f"reviewed pack manifest line {number} is not a sha256sum record: {rel}"]
        if name.startswith("/") or ".." in name.split("/") or name in entries:
            return {}, [f"reviewed pack manifest line {number} names an unusable or repeated member: {rel}"]
        entries[name] = checksum
    if not entries:
        return {}, [f"reviewed pack manifest names no member; refusing to treat an empty manifest as no manifest: {rel}"]
    return entries, []


def catalogue_manifest_errors(root: Path, pins: dict) -> list[str]:
    errors = []
    for rel in catalogue_pack_manifests(pins):
        base = rel[: -len(CATALOGUE_PACK_MANIFEST_NAME)]
        entries, problems = catalogue_manifest_entries(root, rel)
        errors.extend(problems)
        for name, expected in entries.items():
            member = base + name
            path = root / member
            if not path.is_file():
                errors.append(f"reviewed pack manifest member is missing: {member}")
            elif digest(path) != expected:
                errors.append(f"reviewed pack manifest member bytes differ: {member}")
    return errors


def catalogue_manifest_member_paths(root: Path) -> list[str]:
    """Every member path a pinned manifest admits, for the self-test fixture."""
    pins = CATALOGUE_PINS.get("files", {})
    members = []
    for rel in catalogue_pack_manifests(pins):
        base = rel[: -len(CATALOGUE_PACK_MANIFEST_NAME)]
        entries, _ = catalogue_manifest_entries(root, rel)
        members.extend(base + name for name in entries)
    return members


def catalogue_errors(root: Path, kind: str, text: str) -> list[str]:
    if kind != "lessons":
        return []
    errors = []
    wanted = CATALOGUE_PINS.get("visible_body_sha256")
    actual = hashlib.sha256(normalized_visible_body(text, kind).encode("utf-8")).hexdigest()
    if actual != wanted:
        errors.append("Lessons hub wording differs from the explicitly reviewed catalogue digest")
    try:
        rows = json.loads((root / "resources.json").read_text("utf-8"))
        if not isinstance(rows, list) or len(rows) != CATALOGUE_ORIGINAL_ROWS + CATALOGUE_SHELF_ROWS:
            errors.append(f"reviewed catalogue requires the original {CATALOGUE_ORIGINAL_ROWS} rows plus exactly the reviewed hub rows")
        else:
            def row_digest(value):
                encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                return hashlib.sha256(encoded).hexdigest()
            # UX2 A1 (2026-09-08): the two ADDITIVE tag keys, `halfTerm` and `unit`,
            # may be appended to an original row. Every other byte of every
            # original row stays under the digest: the keys are stripped before
            # hashing, so an edit to any existing value, a removal or a reorder
            # still reds here. The tag values themselves are gated by
            # tools/ux2/unit_tags.py --check (derivation) and
            # tools/ux2/check_catalogue_schema.py (enum/shape). Proved red on a
            # planted title edit and a planted unknown key by
            # tools/ux2/prove_catalogue_gate.py.
            def without_tags(value):
                return [{k: v for k, v in row.items() if k not in CATALOGUE_ADDITIVE_TAG_KEYS} for row in value]
            if row_digest(without_tags(rows[:CATALOGUE_ORIGINAL_ROWS])) != CATALOGUE_ORIGINAL_ROWS_SHA256:
                errors.append("an original catalogue row was removed, reordered or edited")
            for index, row in enumerate(rows[:CATALOGUE_ORIGINAL_ROWS]):
                for key in row:
                    if key in CATALOGUE_ADDITIVE_TAG_KEYS and key not in CATALOGUE_ORIGINAL_KEYS_BEFORE_TAGS:
                        continue
                    if key in CATALOGUE_ADDITIVE_TAG_KEYS:
                        errors.append(f"original row {index} carried {key} before the tag ruling; refusing to treat it as additive")
            if row_digest(without_tags(rows[CATALOGUE_ORIGINAL_ROWS:])) != CATALOGUE_SHELF_ROWS_SHA256:
                errors.append("the reviewed catalogue hub rows changed")
    except (ValueError, OSError) as exc:
        errors.append(f"reviewed catalogue row preservation could not be verified: {exc}")
    pins = CATALOGUE_PINS.get("files", {})
    if not pins or "index.html" not in pins or "humanities.html" not in pins:
        errors.append("reviewed catalogue file pins are incomplete")
    for rel, expected in pins.items():
        path = root / rel
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            errors.append(f"invalid reviewed catalogue path: {rel}")
        elif not path.is_file() or digest(path) != expected:
            errors.append(f"reviewed catalogue bytes differ: {rel}")
    errors.extend(catalogue_manifest_errors(root, pins))
    return errors


# SX3 FENCE. ORDER SX3-M4 §1(b). _sx3/FENCE.json names the decks whose proof
# the #586 limb narrowing removed. The loss is latent: the limb only runs when a
# deck's bytes drift from its recorded evidence sha256, and a drift on one of
# these drops its week binding SILENTLY, because none of them is
# style:recommended and so none raises. The fence holds until the fallback limb
# lands. It is enforced here, against the pull request's own diff, because this
# gate already runs on every pull request in both estates and already computes
# that diff — no new workflow, no new trigger to forget.
#
# A missing FENCE.json is not an error: the Apps estate has none, and the fence
# is retired by deleting the file once the fallback limb has landed.
FENCE_PATH = "_sx3/FENCE.json"

# RULING vz-4 (M1): the one rename map, every old path -> the new path it moved to. A move whose
# bytes are identical at the new path counts as unchanged; a moved file whose bytes changed is a
# change of its NEW path and meets the boundary and the fence like any other. The map is bound by
# its digest (a map whose bytes differ is refused, never read) and admits nothing by itself. A
# repository without the file (the Apps copy of this gate) has no moves to resolve.
RENAME_MAP_PATH = "tools/catalogue/M1_RENAME_MAP.json"
RENAME_MAP_SHA256 = "a815038114ff60fb7400d24a880a0a39ce7e678f483c9bd510346a63a6a83ce1"


def rename_map(root: Path) -> dict[str, str]:
    path = root / RENAME_MAP_PATH
    if not path.is_file():
        return {}
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != RENAME_MAP_SHA256:
        raise ValueError(f"unreviewed rename map: {RENAME_MAP_PATH}")
    declared = json.loads(data)
    # RULING wb-5: the moves are "pairs" only; "historicalPairs" (deleted before the move) are history and this gate,
    # which resolves moves and nothing else, never reads them.
    return dict(declared["pairs"])


def _tree_entries(root: Path, ref: str, paths: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    paths = sorted(set(paths))
    for at in range(0, len(paths), 1000):
        raw = subprocess.run(["git", "ls-tree", "-z", ref, "--", *paths[at:at + 1000]],
                             cwd=root, capture_output=True, check=True).stdout.decode("utf-8")
        for record in raw.split("\0"):
            if record:
                fields, rel = record.split("\t", 1)
                mode, _kind, blob = fields.split()
                found[rel] = f"{mode} {blob}"
    return found


def changed_paths(root: Path, base_ref: str, rows: list[tuple[str, str]]) -> set[str]:
    """M and D rows of a --no-renames diff, with each move the rename map names resolved: the old
    path's deletion leaves the set, and the new path joins it only if its bytes differ."""
    changed = {rel for status, rel in rows if status in ("M", "D")}
    backwards = {new: old for old, new in rename_map(root).items()}
    added = [rel for status, rel in rows if status == "A" and rel in backwards]
    if not added:
        return changed
    merge_base = subprocess.run(["git", "merge-base", base_ref, "HEAD"], cwd=root,
                                capture_output=True, text=True, check=True).stdout.strip()
    olds = [backwards[rel] for rel in added]
    before = _tree_entries(root, merge_base, olds)
    head = _tree_entries(root, "HEAD", olds + added)
    for rel in added:
        old = backwards[rel]
        if old in before and old not in head and old in changed:
            changed.discard(old)
            if before[old] != head.get(rel):
                changed.add(rel)
    return changed


# RULING wb-2 (26 Oct 2026): the one M1 replacement transaction (the change-boundary verifier declares it), bound here by
# the same digest. A file whose bytes differ is refused, never read; a repository without it (Apps) has none.
M1_TRANSACTION_PATH = "_glv3/M1_REPLACEMENT_TRANSACTION.json"
M1_TRANSACTION_SHA256 = "c508f9b3471df8462761136d198f332349a71f756b76709e5afa5545ea0b2268"


def m1_transaction_after(root: Path) -> dict[str, str]:
    path = root / M1_TRANSACTION_PATH
    if not path.is_file():
        return {}
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != M1_TRANSACTION_SHA256:
        raise ValueError(f"unreviewed M1 replacement transaction: {M1_TRANSACTION_PATH}")
    return {rel: row["afterSha256"] for rel, row in json.loads(data)["files"].items()}


def fence_errors(root: Path, changed: set[str], kind: str) -> list[str]:
    if kind != "lessons":
        return []
    source = root / FENCE_PATH
    if not source.is_file():
        return []
    try:
        fence = json.loads(source.read_text("utf-8"))
    except (ValueError, OSError) as exc:
        return [f"{FENCE_PATH} could not be read, so the fence cannot be honoured: {exc}"]
    entries = fence.get("fenced")
    if not isinstance(entries, list):
        return [f"{FENCE_PATH} has no 'fenced' list; refusing to treat an unreadable fence as an empty one"]
    fenced = {row.get("path") for row in entries if isinstance(row, dict) and row.get("path")}
    if not fenced:
        return [f"{FENCE_PATH} names no fenced path; refusing to treat an empty fence as no fence"]
    hit = sorted(fenced & changed)
    # RULING wb-2 (26 Oct 2026): a fenced deck whose bytes are exactly its M1 transaction after-digest (the rename map
    # rewrite, declared in M1_TRANSACTION_PATH) is accepted; every other change to a fenced deck is refused as before.
    try:
        after = m1_transaction_after(root)
    except (ValueError, OSError) as exc:
        return [str(exc)]
    hit = [rel for rel in hit if not (rel in after and (root / rel).is_file() and digest(root / rel) == after[rel])]
    return [f"fenced deck modified before the fallback limb landed: {rel} "
            f"(see {FENCE_PATH} and _sx3/STOP_L_limb_population.md)" for rel in hit]


def publication_trigger_errors(root: Path) -> list[str]:
    workflow = root / PUBLICATION_GATE_WORKFLOW_PATH
    if not workflow.is_file():
        return ["education publisher guard workflow is missing"]
    # These existing workflows use explicit YAML block lists. Read only their
    # top-level `on` block; comments or similarly named job text cannot qualify.
    lines = workflow.read_text("utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line == "on:"]
    if len(starts) != 1:
        return ["education publisher guard requires one explicit on block"]
    body = []
    for line in lines[starts[0] + 1:]:
        if line and not line[0].isspace() and not line.lstrip().startswith("#"):
            break
        body.append(line)
    errors = []
    for event in ("pull_request", "push"):
        positions = [i for i, line in enumerate(body) if line == "  " + event + ":"]
        if len(positions) != 1:
            errors.append("education publisher guard lacks explicit " + event + " trigger")
            continue
        event_lines = []
        for line in body[positions[0] + 1:]:
            if line.startswith("  ") and not line.startswith("   ") and line.strip() and not line.lstrip().startswith("#"):
                break
            event_lines.append(line)
        paths = [i for i, line in enumerate(event_lines) if line == "    paths:"]
        if len(paths) != 1:
            errors.append("education publisher guard lacks explicit " + event + " paths")
            continue
        values = []
        for line in event_lines[paths[0] + 1:]:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if not line.startswith("      - "):
                break
            values.append(line[len("      - "):].strip().strip("\"'"))
        if values.count(PUBLICATION_CALLER_PATH) != 1:
            errors.append("education publisher caller must be watched exactly once by " + event)
    return errors


def publication_errors(root: Path, kind: str = "lessons") -> list[str]:
    errors = publication_trigger_errors(root)
    caller = root / PUBLICATION_CALLER_PATH
    if not caller.is_file():
        errors.append("reviewed education publication caller is missing")
    elif digest(caller) != PUBLICATION_CALLER_SHA256_BY_KIND.get(kind, PUBLICATION_CALLER_SHA256):
        errors.append("education publication caller differs from the reviewed immutable publisher pin")
    return errors


def lundyloop_ci_errors(root: Path, kind: str) -> list[str]:
    if kind != "apps":
        return []
    return ["reviewed LundyLoop CI bytes differ or are missing: " + rel
            for rel, expected in LUNDYLOOP_CI_PINS.items()
            if not (root / rel).is_file() or digest(root / rel) != expected]


def boundary_errors(changed: set[str], kind: str) -> list[str]:
    # SW2-T5R1 retires AR3: shared assets are admitted only through their
    # required exact-byte registry, checked on every run above.
    allowed = ALLOWED_DIFF | set(CANONICAL_HASHES)
    if kind == "apps":
        allowed = allowed | set(LUNDYLOOP_CI_PINS)
    if kind == "lessons":
        allowed = allowed | set(CATALOGUE_PINS.get("files", {})) | CATALOGUE_RECORD_PATHS
    unexpected = sorted(changed - allowed)
    if not unexpected:
        return []
    errors = [f"standalone/offline boundary violated by changed files: {unexpected}"]
    # ORDER SX3-M5 §2: name the CAUSE, not just the symptom. A lesson deck that
    # reaches this line has not been admitted, and "boundary violated" reads like
    # the change is forbidden when what is missing is the admission. The estate
    # admits a deck by naming it in CATALOGUE_PINS; tools/pin1/derive_triggers.py
    # --write then materialises the matching trigger path, and PIN1 asserts the
    # two sets are equal in both directions. This is the remedy, in one line,
    # where the refusal is read.
    decks = [rel for rel in unexpected
             if rel.startswith("Science/") and rel.endswith(".html")]
    if decks:
        errors.append(
            "deck not admitted; add to the boundary set (CATALOGUE_PINS, via "
            "tools/catalogue/pin_catalogue_contract.py) and to the trigger list "
            "(tools/pin1/derive_triggers.py --write), which PIN1 then asserts as "
            f"a pair: {decks}")
    return errors


def css_balanced(text: str) -> bool:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    quote = None
    escape = False
    depth = 0
    for char in text:
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and quote is None


def git_text(root: Path, ref: str, path: str) -> str:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"], cwd=root, text=True, capture_output=True
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"git show failed for {ref}:{path}")
    return proc.stdout


def number_word(n: int) -> str:
    one = [
        "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
        "Seventeen", "Eighteen", "Nineteen",
    ]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    if 0 <= n < 20:
        return one[n]
    if 20 <= n < 100:
        return tens[n // 10] + ("-" + one[n % 10].lower() if n % 10 else "")
    return str(n)


def run_checks(
    root: Path,
    *,
    kind: str,
    canonical: Path,
    base_html: str | None = None,
    check_git: bool = False,
    base_ref: str | None = None,
) -> list[str]:
    errors: list[str] = publication_errors(root, kind) + lundyloop_ci_errors(root, kind)
    index_path = root / "index.html"
    if not index_path.is_file():
        return ["missing index.html"]
    text = index_path.read_text("utf-8")
    errors.extend(catalogue_errors(root, kind, text))

    if SENTINEL not in text:
        errors.append("sentinel/version marker missing from index.html")
    expected_body = f'mbm-hub mbm-hub-{kind}'
    if expected_body not in text:
        errors.append(f"missing {expected_body} body classes")
    if 'class="header mbm-site-header"' not in text:
        errors.append("canonical platform header class missing")
    if 'class="menu" id="menu"' not in text or 'aria-controls="nav"' not in text:
        errors.append("responsive menu button contract missing")
    if 'id="nav" aria-label="Site navigation"' not in text:
        errors.append("named site navigation landmark missing")
    if '<summary>More</summary>' not in text or '<summary>Display</summary>' not in text:
        errors.append("More/Display disclosure contract missing")
    if "data-mbm-theme-slot" not in text:
        errors.append("reading-background slot missing")

    primary = extract(r'<div class="mbm-primary-links">(.*?)</div>', text, "primary navigation", errors)
    primary_hrefs = re.findall(r'<a\b[^>]*href="([^"]+)"', primary, re.I)
    if primary_hrefs != PRIMARY_ROUTES:
        errors.append(f"primary route order/casing drift: {primary_hrefs!r}")
    more = extract(r'<div class="mbm-nav-panel">(.*?)</div>', text, "More panel", errors)
    more_hrefs = re.findall(r'<a\b[^>]*href="([^"]+)"', more, re.I)
    if more_hrefs != MORE_ROUTES:
        errors.append(f"More route order/casing drift: {more_hrefs!r}")
    active = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*aria-current="page"', primary, re.I)
    expected_active = "/Lessons/" if kind == "lessons" else "/Matt-s-Apps-/"
    if active != [expected_active]:
        errors.append(f"active navigation must be exactly {expected_active}: {active!r}")

    ids = re.findall(r'\bid="([^"]+)"', text, re.I)
    duplicates = sorted(k for k, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate IDs: {duplicates}")

    for rel, expected in CANONICAL_HASHES.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"missing shared local asset {rel}")
        elif digest(path) != expected:
            hint = f" — run: {SYNC_COMMAND}" if rel == THEME_COPY else ""
            errors.append(f"shared asset hash drift: {rel}{hint}")
    # Pins are checked on EVERY run, not only when git reports the file changed: a
    # gate that looks only when it is told something moved cannot catch the case
    # where nobody told it.
    for manifest, pinned in MANIFEST_PINS.items():
        path = root / manifest
        if not path.is_file():
            continue          # the other estate does not carry this manifest
        if digest(path) != pinned:
            errors.append(
                f"{manifest} does not match its pinned digest — if you changed it on "
                f"purpose, re-pin it in the same commit: {PIN_COMMAND}")

    theme_path = root / THEME_COPY
    if theme_path.is_file() and not theme_path.read_bytes().startswith(GENERATED_HEADER):
        errors.append(
            f"{THEME_COPY} has lost its generated-file header, so the next person to open "
            f"it has nothing telling them it is output — run: {SYNC_COMMAND}")
    # Unconditional, and that is the point. This block used to sit behind
    # `if canonical:`, with --canonical an optional argument. Run without it the
    # gate skipped every cross-estate comparison and still printed
    # "[PASS] <kind> cross-estate static contract" and exited 0 — a green naming
    # the one thing it had not done. That is how three different versions of
    # mbm-platform.css/js coexisted across the estate with every pin green:
    # Lessons ccfb0fd9/0841046b, Apps e3eb9b83/0958a73a, site b520cf36/095a29e6.
    # `canonical` is now a required parameter with no default, so omitting it is
    # a TypeError here and an argparse error at the boundary, not a quiet pass.
    pairs = {
        "assets/mbm-platform.css": canonical / "assets/mbm-platform.css",
        "assets/mbm-platform.js": canonical / "assets/mbm-platform.js",
        THEME_COPY: canonical / "theme.js"
    }
    for local_rel, reference in pairs.items():
        if not reference.is_file():
            errors.append(f"canonical reference missing: {reference}")
            continue
        expected_bytes = reference.read_bytes()
        if local_rel == THEME_COPY:
            expected_bytes = GENERATED_HEADER + expected_bytes
        if (root / local_rel).read_bytes() == expected_bytes:
            continue
        if local_rel == THEME_COPY:
            errors.append(
                f"{local_rel} is not the generated copy of the canonical theme.js. "
                f"Do not edit it here — edit theme.js in the site repository, then run: "
                f"{SYNC_COMMAND}")
        else:
            errors.append(f"local copy no longer equals canonical source: {local_rel}")

    if 'href="assets/mbm-platform.css"' not in text or 'href="assets/mbm-hub.css"' not in text:
        errors.append("hub must use repo-local CSS assets")
    if 'src="assets/mbm-theme.js"' not in text or 'src="assets/mbm-platform.js"' not in text:
        errors.append("hub must use repo-local JavaScript assets")
    if 'src="/theme.js"' in text or 'src="/assets/mbm-platform' in text:
        errors.append("network/root dependency introduced for the hub shell")
    external_scripts = re.findall(r'<script\b[^>]*\bsrc="(https?:[^"]+)"', text, re.I)
    if external_scripts:
        errors.append(f"unexpected external hub scripts: {external_scripts}")

    for rel in ("assets/mbm-platform.css", "assets/mbm-hub.css"):
        path = root / rel
        if path.is_file() and not css_balanced(path.read_text("utf-8")):
            errors.append(f"unbalanced CSS: {rel}")
    platform_js = (root / "assets/mbm-platform.js").read_text("utf-8") if (root / "assets/mbm-platform.js").is_file() else ""
    theme_js = (root / "assets/mbm-theme.js").read_text("utf-8") if (root / "assets/mbm-theme.js").is_file() else ""
    for required in ("Escape", "pointerdown", "aria-expanded", "ResizeObserver", "mbm-nav-open"):
        if required not in platform_js:
            errors.append(f"platform interaction contract missing {required}")
    if "mbm_reading_theme" not in theme_js:
        errors.append("shared reading-theme storage key missing")

    suspicious = re.findall(
        r"(?i)(?:password\s*=|hard.?coded\s+password|localStorage\.(?:setItem|getItem)\([^)]*(?:auth|login|password)|api[_-]?key\s*=)",
        text + platform_js + theme_js,
    )
    if suspicious:
        errors.append("credential/fake-auth pattern detected")

    if kind == "apps":
        try:
            data = json.loads((root / "apps.json").read_text("utf-8"))
            spaces = data.get("spaces")
            if not isinstance(spaces, list) or not all(isinstance(s.get("items"), list) for s in spaces):
                raise ValueError("invalid spaces")
            total = sum(len(s["items"]) for s in spaces)
            expected_word = number_word(total)
            if f'<span id="leadCount">{expected_word}</span>' not in text:
                errors.append(f"no-JS lead count does not match apps.json ({expected_word})")
            for token in ("numberWord(total)", "leadCount", "${shown} of ${total} studios"):
                if token not in text:
                    errors.append(f"derived Apps count contract missing: {token}")
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"invalid apps.json: {exc}")
    else:
        try:
            data = json.loads((root / "resources.json").read_text("utf-8"))
            if not isinstance(data, list) or not data:
                raise ValueError("expected non-empty list")
            years = Counter(item.get("year") for item in data)
            if not years.get("2026-27") or not years.get("2025-26"):
                errors.append(f"academic collection data missing: {dict(years)}")
            # UX2 A2 (2026-09-08): the hub derives both count lines from the catalogue it
            # fetches at runtime — the browse line "<M> resources · <S> subjects" and the
            # results line "<n> of <M> resources". The retired year tabs and subject
            # chips (fillTabCounts, buildQuicknav) no longer exist, so the contract names
            # the expressions that replace them and the fetch they derive from.
            for token in ("${rows.length} of ${H.state.rows.length} resources",
                          "${rows.length} resources · ${cards.length} subjects", "H.loadAll()"):
                if token not in text:
                    errors.append(f"derived Lessons count contract missing: {token}")
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"invalid resources.json: {exc}")

    if base_html is not None:
        base_brand = extract(r'(<a class="brand"[^>]*>.*?</a>)', base_html, "base brand", errors)
        current_brand = extract(r'(<a class="brand"[^>]*>.*?</a>)', text, "current brand", errors)
        if base_brand and current_brand and base_brand != current_brand:
            errors.append("Made by Matt logo/brand markup changed")
        if kind == "apps" and normalized_visible_body(base_html, kind) != normalized_visible_body(text, kind):
            # HC5 D2 (Matt's ruling, 2026-09-07): support buttons live on adult
            # pages only, so the Creator Hub's "Buy me a coffee" line leaves the
            # pupil surface. The reviewed result is admitted by exact digest of
            # its normalised visible body; any other wording change still reds.
            current = hashlib.sha256(normalized_visible_body(text, kind).encode("utf-8")).hexdigest()
            if current != APPS_HUB_REVIEWED_WORDING_SHA256:
                errors.append("existing authored hub wording changed outside the derived Apps count")

    if check_git and base_ref:
        proc = subprocess.run(
            # M/R/D, not A. The invariant is stated at the top of this file: "no
            # standalone lesson or studio is CHANGED by this release". An ADDED file
            # changes nothing — it cannot modify an existing studio — and counting
            # additions as violations meant every new studio, tool and dotfile had to
            # be hand-added to ALLOWED_DIFF forever. Proven both ways: modifying or
            # deleting an existing studio still reddens this check.
            # RULING vz-4: --no-renames, so a move is its deletion and its addition, and the
            # rename map (changed_paths) resolves each one it names; nothing else is resolved.
            ["git", "diff", "--name-status", "-z", "--no-renames", "--diff-filter=AMD", f"{base_ref}...HEAD"],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if proc.returncode:
            errors.append(f"git diff failed: {proc.stderr.strip()}")
        else:
            fields = proc.stdout.split("\0")
            if fields and fields[-1] == "":
                fields.pop()
            changed = changed_paths(root, base_ref, list(zip(fields[::2], fields[1::2])))
            errors.extend(boundary_errors(changed - exact_byte_admitted(root, changed), kind))   # rm-2
            errors.extend(fence_errors(root, changed, kind))
            for manifest in ("resources.json", "apps.json"):
                if manifest in changed and manifest not in MANIFEST_PINS:
                    errors.append(f"source manifest unexpectedly changed: {manifest}")

    return errors


def self_test(root: Path, kind: str, canonical: Path) -> None:
    # The fixture copies this repository's own CANONICAL_HASHES assets, so with
    # the tree in a good state they already equal the canonical ones and the
    # comparison passes. Threading `canonical` through is not bookkeeping for the
    # new required argument: it means the positive control now exercises the
    # cross-estate leg as well, and "fixture was not initially valid" below would
    # catch that leg being broken, not only the local ones.
    with tempfile.TemporaryDirectory(prefix="mbm-cross-estate-positive-control-") as temp:
        fixture = Path(temp)
        for rel in set(["index.html", "resources.json" if kind == "lessons" else "apps.json", PUBLICATION_CALLER_PATH, PUBLICATION_GATE_WORKFLOW_PATH, *CANONICAL_HASHES] + (list(CATALOGUE_PINS.get("files", {})) + catalogue_manifest_member_paths(root) if kind == "lessons" else list(LUNDYLOOP_CI_PINS))):
            src = root / rel
            dst = fixture / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        good = run_checks(fixture, kind=kind, canonical=canonical)
        if good:
            raise RuntimeError(f"positive-control fixture was not initially valid: {good}")
        if kind == "apps":
            for rel in LUNDYLOOP_CI_PINS:
                target = fixture / rel
                original = target.read_bytes()
                target.write_bytes(original + b"\n# planted unreviewed byte\n")
                if not lundyloop_ci_errors(fixture, kind):
                    raise RuntimeError("LundyLoop CI byte mutation was not detected: " + rel)
                target.write_bytes(original)
                if lundyloop_ci_errors(fixture, kind):
                    raise RuntimeError("Restored LundyLoop CI bytes did not pass")
            if not boundary_errors({"tools/unreviewed.py"}, kind):
                raise RuntimeError("An arbitrary CI path escaped the boundary")
            if not boundary_errors({"LundyLoop_Professional_OS.html"}, kind):
                raise RuntimeError("A standalone payload escaped the boundary")
            print("LundyLoop CI controls: real green / planted byte red / restored green; unrelated paths red")
        if kind == "lessons":
            # The fence must go red on a fenced path and stay quiet on anything
            # else, and it must REFUSE rather than pass when the file it depends
            # on is unreadable or empty. A fence that cannot go red is not a fence.
            fence_file = root / FENCE_PATH
            if fence_file.is_file():
                fenced = json.loads(fence_file.read_text("utf-8"))["fenced"]
                admitted = m1_transaction_after(root)
                # The red control uses a fenced deck the M1 transaction does not admit at its current bytes (wb-2).
                one = next(row["path"] for row in fenced if row["path"] not in admitted)
                if not fence_errors(root, {one}, "lessons"):
                    raise RuntimeError("the fence let a fenced deck through: " + one)
                if fence_errors(root, {"Science/Build/does-not-exist.html"}, "lessons"):
                    raise RuntimeError("the fence objected to an unfenced path")
                if fence_errors(root, {one}, "apps"):
                    raise RuntimeError("the fence fired on the apps estate, which has no fence")
                with tempfile.TemporaryDirectory(prefix="mbm-fence-control-") as broken:
                    empty = Path(broken)
                    (empty / FENCE_PATH).parent.mkdir(parents=True, exist_ok=True)
                    (empty / FENCE_PATH).write_text('{"fenced": []}', encoding="utf-8")
                    if not fence_errors(empty, {one}, "lessons"):
                        raise RuntimeError("an empty fence was treated as no fence")
                    (empty / FENCE_PATH).write_text("not json", encoding="utf-8")
                    if not fence_errors(empty, {one}, "lessons"):
                        raise RuntimeError("an unreadable fence was treated as no fence")
                # RULING wb-2: a fenced deck at exactly its transaction after-digest is accepted; one changed byte is refused.
                taken = [row["path"] for row in fenced if row["path"] in admitted]
                for rel in taken:
                    if fence_errors(root, {rel}, "lessons"):
                        raise RuntimeError("the fence refused a fenced deck at its M1 transaction bytes: " + rel)
                    with tempfile.TemporaryDirectory(prefix="mbm-fence-m1-") as scratch:
                        fence_fixture = Path(scratch)
                        for copy in (FENCE_PATH, M1_TRANSACTION_PATH, rel):
                            (fence_fixture / copy).parent.mkdir(parents=True, exist_ok=True)
                            shutil.copyfile(root / copy, fence_fixture / copy)
                        if fence_errors(fence_fixture, {rel}, "lessons"):
                            raise RuntimeError("the fence refused the transaction bytes in a fence_fixture: " + rel)
                        data = bytearray((fence_fixture / rel).read_bytes())
                        data[len(data) // 2] ^= 0x01
                        (fence_fixture / rel).write_bytes(bytes(data))
                        if not fence_errors(fence_fixture, {rel}, "lessons"):
                            raise RuntimeError("the fence let a one-byte change to a fenced deck through: " + rel)
                # RULING wb-5: a historical pair of the rename map cannot admit a move here.
                declared = json.loads((root / RENAME_MAP_PATH).read_bytes()) if (root / RENAME_MAP_PATH).is_file() else {}
                for old, new in declared.get("historicalPairs", {}).items():
                    if changed_paths(root, "HEAD", [("D", old), ("A", new)]) != {old}:
                        raise RuntimeError("a historical rename pair was resolved as a move: " + new)
                print(f"SX3 fence controls: {len(fenced)} fenced path(s) red / unfenced path green / apps estate quiet / empty and unreadable fence red / {len(taken)} at M1 transaction bytes green, one byte off red")
            # ORDER FINISH-2 manifest-pin ruling: 1605 pack members are admitted by
            # their manifest rather than by 1605 individual pins, so the expansion
            # must be PROVED able to go red on every way that can be abused. A
            # manifest check that cannot go red is a 1605-file hole, and this control
            # is the whole reason the indirection is not a loosening.
            pins = CATALOGUE_PINS.get("files", {})
            manifests = catalogue_pack_manifests(pins)
            if manifests:
                index_text = (fixture / "index.html").read_text("utf-8")
                one = manifests[0]
                base = one[: -len(CATALOGUE_PACK_MANIFEST_NAME)]
                entries, problems = catalogue_manifest_entries(fixture, one)
                if problems:
                    raise RuntimeError("a pinned pack manifest did not parse in the fixture: " + "; ".join(problems))
                member = base + sorted(entries)[0]
                target = fixture / member
                kept_member = target.read_bytes()
                target.write_bytes(kept_member + b"\n<!-- planted unreviewed byte -->\n")
                if not catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("a manifest-listed pack member's byte drift was not detected: " + member)
                target.unlink()
                if not catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("a missing manifest-listed pack member was not detected: " + member)
                target.write_bytes(kept_member)
                if catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("the restored pack member did not pass")
                manifest_file = fixture / one
                kept_manifest = manifest_file.read_bytes()
                manifest_file.write_bytes(kept_manifest + b"0" * 64 + b"  planted/unreviewed_addition.pptx\n")
                if not catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("a manifest enlarged to admit an unreviewed file was not caught by the expansion")
                if ("reviewed catalogue bytes differ: " + one) not in catalogue_errors(fixture, "lessons", index_text):
                    raise RuntimeError("a manifest enlarged to admit an unreviewed file was not caught by its own pin")
                manifest_file.write_bytes(b"not a sha256sum manifest\n")
                if not catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("an unreadable manifest was treated as no manifest")
                manifest_file.write_bytes(b"")
                if not catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("an empty manifest was treated as no manifest")
                manifest_file.write_bytes(kept_manifest)
                if catalogue_manifest_errors(fixture, pins):
                    raise RuntimeError("the restored manifest did not pass")
                listed = sum(len(catalogue_manifest_entries(fixture, rel)[0]) for rel in manifests)
                print(f"pack manifest controls: {len(manifests)} pinned manifest(s) admitting {listed} member(s); "
                      f"member drift red / member missing red / manifest enlargement red on BOTH the expansion and its pin / "
                      f"unreadable manifest red / empty manifest red / restored green")
        index = fixture / "index.html"
        text = index.read_text("utf-8")
        index.write_text(text.replace('<a href="/Lessons/"', '<a href="/lessons/"', 1), "utf-8")
        bad = run_checks(fixture, kind=kind, canonical=canonical)
        if not bad:
            raise RuntimeError("positive-control mutation was not detected")
        print(f"positive-control: PASS ({len(bad)} detected error(s))")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", help="Git ref used to prove wording/logo and diff boundaries")
    parser.add_argument(
        "--canonical",
        required=True,
        help="Checked-out canonical site repository. Required, and deliberately so: "
             "without it the cross-estate comparison does not run at all, and this "
             "gate would print [PASS] cross-estate static contract having compared "
             "nothing across estates.")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    kind = detect_kind(root)
    base_html = git_text(root, args.base, "index.html") if args.base else None
    # required=True stops a missing flag. It does not stop --canonical "" — an
    # empty string satisfies argparse and used to be falsy at the `if canonical:`
    # that no longer exists, so it would have skipped the comparison silently.
    # Nor does it stop a path that is not the site repository, which would fail
    # later as three "canonical reference missing" lines rather than as the one
    # thing that is actually wrong. Both are named here instead.
    if not args.canonical.strip():
        parser.error("--canonical was given an empty path; pass the checked-out site repository")
    canonical = Path(args.canonical).resolve()
    if not (canonical / "assets/mbm-platform.css").is_file():
        parser.error(
            f"--canonical does not look like the site repository: {canonical} "
            f"(no assets/mbm-platform.css under it)")
    errors = run_checks(
        root,
        kind=kind,
        base_html=base_html,
        canonical=canonical,
        check_git=bool(args.base),
        base_ref=args.base,
    )
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print(f"[PASS] {kind} cross-estate static contract")
    if args.self_test:
        self_test(root, kind, canonical)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
