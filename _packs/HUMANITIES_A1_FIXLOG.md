# Humanities Autumn 1 W3–W7 packs — HC5 §1.1 fix log

Order `mbm-finish-2026-09-07-HC5`. Inputs: the three Complete_Pack zips (BUILD `52dd2186…`, GROW `f05e74b9…`, LAUNCH `78e3fa23…`; 32 files each). Every edit was applied at XML level by `fix_packs.py` (idempotent: a second run over its own output changed 0 files), and every count below was produced by that script or by `gate_packs.py`.

## Defects applied

| defect | rule | files | occurrences |
|---|---|---|---|
| H1 factual | BT 26/1237 records Rubert Adolphus as 24 (Kenneth Amos 21 is correct) | 9 (8 DOCX + the GROW W3 deck's 12 notes slides) | 20 |
| H2 wording | Start Here guides: subtitle without 'review copy', publication-status paragraph deleted, sources paragraph replaced, 'Published 7 September 2026' added after CHECKED | 3 | 12 edits |
| H3 orphan media | media parts with no r:embed/r:id/r:link in document/headers/footers removed, relationships dropped | 33 DOCX | 48 parts (image1.jpg ×33, image2.png ×15) |
| H4 notes | BUILD W3/W6/W7 decks: the 'larger printed source sheet' line removed from notes | 3 | 3 (the line sits once per deck, on notes slide 4 — the order predicted 36) |
| H5 optional | thumbnail scan swap | 0 | skipped by choice: the 1 MB scan is embedded once per deck; left as shipped |

## Gates (each red-proved)

- Render: 37 regenerated PDFs; page counts equal the originals for every one; ink > 0 on every page; '24' in the Adolphus row of all 9 H1 files (the deck via its notes XML — notes are not part of a slide render).
- H2 zero-count over the 142 shipped files: {'review copy': 0, 'health check': 0, 'Compress_': 0, "Matt's check": 0, 'Matt’s check': 0}; red-proved on the originals (files carrying each marker, 3 DOCX + 3 PDF): {'review copy': 6, 'health check': 6, 'Compress_': 6, "Matt's check": 0, 'Matt’s check': 6}.
- H3 no-visible-change: 22/22 orphan-only DOCX render pixel-identical (72 dpi, every page) before and after under the same LibreOffice; the H1/H2 files differ only on the edited lines (diffs in gate_report.json).
- H4: the only text token that differs between the original and fixed deck XML is the removed line (whitespace ignored); the GROW W3 deck differs only on the Adolphus answer line.
- Instrument wrong before right: (1) the first PPTX rewrite re-zipped untouched decks and changed their bytes — fixed so untouched files keep original bytes (37 changed, not 48); (2) the first H2 count ran over the fixed source folder, which still held the original PDFs, so it read 6/3/3/3 after the fix — moved to the built output tree, where it reads 0/0/0/0 and fails if fewer than 90 files are scanned; (3) the deck H1 check first read the slide render, which never contains notes.

## Verified and not touched

Image credits (NPG 6856 PD-Art; Geograph CC BY-SA 2.0 with photographer and date; TNA BT 26/1237), all dates, timetable slots and the 40-minute timings were read and left as authored.

## Per file (before → after sha256; shipped PDFs are the regenerated renders where the source changed)

| file | defects | before | after |
|---|---|---|---|
| BUILD/START_HERE_BUILD_Humanities_Autumn1.docx | H2 (subtitle, deleted publication-status paragraph, sources paragraph replaced, published line added); H3 removed image1.jpg | fbfc0251791f | 1c349a77956f |
| BUILD/START_HERE_BUILD_Humanities_Autumn1.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 5ae7172e364f | 67edfd8f065c |
| BUILD/Week_3/BUILD_Humanities_Autumn1_W3_Community_Places.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | af888a41d2bf | ab5ea2e33aef |
| BUILD/Week_3/BUILD_Humanities_Autumn1_W3_Community_Places.pptx | H4 ×1 (notes line removed) | 57fa6f5e63f8 | a37da7408430 |
| BUILD/Week_3/BUILD_Humanities_Autumn1_W3_Community_Places_Pupil.docx | H3 removed image1.jpg, image2.png | a087f3024582 | 7f076685a811 |
| BUILD/Week_3/BUILD_Humanities_Autumn1_W3_Community_Places_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | d8b2a9d94eff | 27405f2675e6 |
| BUILD/Week_3/BUILD_Humanities_Autumn1_W3_Community_Places_Teacher.docx | H3 removed image1.jpg | 7a7e5019e75a | 59412514bcaa |
| BUILD/Week_3/BUILD_Humanities_Autumn1_W3_Community_Places_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 3bbf2d1b7dc8 | a8f1d1246664 |
| BUILD/Week_4/BUILD_Humanities_Autumn1_W4_Then_And_Later.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | a420055236c4 | a420055236c4 |
| BUILD/Week_4/BUILD_Humanities_Autumn1_W4_Then_And_Later.pptx | untouched: original bytes | 27f615bc62f3 | 27f615bc62f3 |
| BUILD/Week_4/BUILD_Humanities_Autumn1_W4_Then_And_Later_Pupil.docx | H3 removed image1.jpg, image2.png | 0a02f088d72c | 1331982ab0f7 |
| BUILD/Week_4/BUILD_Humanities_Autumn1_W4_Then_And_Later_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 51b56e6b70d5 | 3859d6591bac |
| BUILD/Week_4/BUILD_Humanities_Autumn1_W4_Then_And_Later_Teacher.docx | H3 removed image1.jpg | a16b85171173 | 904e94517a12 |
| BUILD/Week_4/BUILD_Humanities_Autumn1_W4_Then_And_Later_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 1bb7759462eb | 513f2f1b1505 |
| BUILD/Week_5/BUILD_Humanities_Autumn1_W5_Same_Different_Respect.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 1d513eaabab6 | 1d513eaabab6 |
| BUILD/Week_5/BUILD_Humanities_Autumn1_W5_Same_Different_Respect.pptx | untouched: original bytes | 57d853649f54 | 57d853649f54 |
| BUILD/Week_5/BUILD_Humanities_Autumn1_W5_Same_Different_Respect_Pupil.docx | H3 removed image1.jpg, image2.png | 72e89a19d96c | 5e9900243bb5 |
| BUILD/Week_5/BUILD_Humanities_Autumn1_W5_Same_Different_Respect_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | f95a0de37b03 | f501b155fab7 |
| BUILD/Week_5/BUILD_Humanities_Autumn1_W5_Same_Different_Respect_Teacher.docx | H3 removed image1.jpg | 6488ff3dea27 | 9d67e2386eb8 |
| BUILD/Week_5/BUILD_Humanities_Autumn1_W5_Same_Different_Respect_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | afd7fc9772da | 2659ee38d6b1 |
| BUILD/Week_6/BUILD_Humanities_Autumn1_W6_Community_Map.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | b2f61246d4e1 | 897246a31a01 |
| BUILD/Week_6/BUILD_Humanities_Autumn1_W6_Community_Map.pptx | H4 ×1 (notes line removed) | 832bc9b07526 | 3490910ef6ca |
| BUILD/Week_6/BUILD_Humanities_Autumn1_W6_Community_Map_Pupil.docx | H3 removed image1.jpg, image2.png | a2a5673ff27d | 468e999e56f7 |
| BUILD/Week_6/BUILD_Humanities_Autumn1_W6_Community_Map_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 821e5521f558 | 4ce888f4cc85 |
| BUILD/Week_6/BUILD_Humanities_Autumn1_W6_Community_Map_Teacher.docx | H3 removed image1.jpg | e8ce04c93c5c | 6d3760a76147 |
| BUILD/Week_6/BUILD_Humanities_Autumn1_W6_Community_Map_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | e21f0fcb48c3 | cdd0f3c77c0e |
| BUILD/Week_7/BUILD_Humanities_Autumn1_W7_Belonging.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | d22dbc68bcc5 | b1662acb13e7 |
| BUILD/Week_7/BUILD_Humanities_Autumn1_W7_Belonging.pptx | H4 ×1 (notes line removed) | 4df966992681 | a2b1f81da59e |
| BUILD/Week_7/BUILD_Humanities_Autumn1_W7_Belonging_Pupil.docx | H3 removed image1.jpg, image2.png | 2987e614af29 | 4995cb0a3c0f |
| BUILD/Week_7/BUILD_Humanities_Autumn1_W7_Belonging_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | a73241b11468 | 2a0c6c2a1b68 |
| BUILD/Week_7/BUILD_Humanities_Autumn1_W7_Belonging_Teacher.docx | H3 removed image1.jpg | 617f4eb96f55 | fe98bf7b07b4 |
| BUILD/Week_7/BUILD_Humanities_Autumn1_W7_Belonging_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 171796d91f17 | 0cddd7b9f3f9 |
| GROW/START_HERE_GROW_Humanities_Autumn1.docx | H2 (subtitle, deleted publication-status paragraph, sources paragraph replaced, published line added); H3 removed image1.jpg | 136b04d07a60 | 4477f5c0bd57 |
| GROW/START_HERE_GROW_Humanities_Autumn1.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | b7f0714e6b3b | c6c88162fc3b |
| GROW/Week_3/GROW_Humanities_Autumn1_W3_Cause_Consequence.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 00483ccb52a7 | a8960487c624 |
| GROW/Week_3/GROW_Humanities_Autumn1_W3_Cause_Consequence.pptx | H1 ×12 (Adolphus 21→24) | df8203e5c8d6 | 392b50c4c07e |
| GROW/Week_3/GROW_Humanities_Autumn1_W3_Cause_Consequence_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | d45e3d4000d2 | db1f61fa71ea |
| GROW/Week_3/GROW_Humanities_Autumn1_W3_Cause_Consequence_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | f324f6559b59 | be4d8125d07f |
| GROW/Week_3/GROW_Humanities_Autumn1_W3_Cause_Consequence_Teacher.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg | 910d3866256a | 35e20f387c57 |
| GROW/Week_3/GROW_Humanities_Autumn1_W3_Cause_Consequence_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 809aaefc07e3 | f41f207a06da |
| GROW/Week_4/GROW_Humanities_Autumn1_W4_Diverse_British_History.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | f9212596b7cd | f9212596b7cd |
| GROW/Week_4/GROW_Humanities_Autumn1_W4_Diverse_British_History.pptx | untouched: original bytes | e6e8cbec969e | e6e8cbec969e |
| GROW/Week_4/GROW_Humanities_Autumn1_W4_Diverse_British_History_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | 39abf8f32e65 | c3ab6a627894 |
| GROW/Week_4/GROW_Humanities_Autumn1_W4_Diverse_British_History_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | b07e0d0be4c9 | 10629923c01d |
| GROW/Week_4/GROW_Humanities_Autumn1_W4_Diverse_British_History_Teacher.docx | H3 removed image1.jpg | 9dfaf1860471 | a631ce2eafc4 |
| GROW/Week_4/GROW_Humanities_Autumn1_W4_Diverse_British_History_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | dc55dc0de353 | 9e6fcb387ef8 |
| GROW/Week_5/GROW_Humanities_Autumn1_W5_Significance.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | e1330bdd3631 | e1330bdd3631 |
| GROW/Week_5/GROW_Humanities_Autumn1_W5_Significance.pptx | untouched: original bytes | b8fda3bb11ab | b8fda3bb11ab |
| GROW/Week_5/GROW_Humanities_Autumn1_W5_Significance_Pupil.docx | H3 removed image1.jpg, image2.png | 1a119feab0f0 | 66d5491049d1 |
| GROW/Week_5/GROW_Humanities_Autumn1_W5_Significance_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | d75874d68a93 | 56146acb95cc |
| GROW/Week_5/GROW_Humanities_Autumn1_W5_Significance_Teacher.docx | H3 removed image1.jpg | 7f61d752e118 | 3c5fcaa19f7e |
| GROW/Week_5/GROW_Humanities_Autumn1_W5_Significance_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | daf8a587b921 | 06c90f34dba2 |
| GROW/Week_6/GROW_Humanities_Autumn1_W6_Account_Plan.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 96647f2e2c29 | 96647f2e2c29 |
| GROW/Week_6/GROW_Humanities_Autumn1_W6_Account_Plan.pptx | untouched: original bytes | a1af0e856fe8 | a1af0e856fe8 |
| GROW/Week_6/GROW_Humanities_Autumn1_W6_Account_Plan_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | d0d12e4bfe1a | cbf6552612fc |
| GROW/Week_6/GROW_Humanities_Autumn1_W6_Account_Plan_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 4cdbd50dcf99 | 2bc1d6ddbd9a |
| GROW/Week_6/GROW_Humanities_Autumn1_W6_Account_Plan_Teacher.docx | H3 removed image1.jpg | 84a3d153b71c | 4fe2c7f08ebd |
| GROW/Week_6/GROW_Humanities_Autumn1_W6_Account_Plan_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 1e90085b255f | 1957ee3d1f4b |
| GROW/Week_7/GROW_Humanities_Autumn1_W7_Account_Review.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 79e128df5d3a | 79e128df5d3a |
| GROW/Week_7/GROW_Humanities_Autumn1_W7_Account_Review.pptx | untouched: original bytes | 27ec3b6308b9 | 27ec3b6308b9 |
| GROW/Week_7/GROW_Humanities_Autumn1_W7_Account_Review_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | 12f0c7f347e6 | cd9d19cc6da3 |
| GROW/Week_7/GROW_Humanities_Autumn1_W7_Account_Review_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 765f61a66daa | c58e4aa8b63a |
| GROW/Week_7/GROW_Humanities_Autumn1_W7_Account_Review_Teacher.docx | H3 removed image1.jpg | 4874872fa0e2 | ad960232db2a |
| GROW/Week_7/GROW_Humanities_Autumn1_W7_Account_Review_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | d77ef61ee56d | 871dd84cf0ab |
| LAUNCH/START_HERE_LAUNCH_Humanities_Autumn1.docx | H2 (subtitle, deleted publication-status paragraph, sources paragraph replaced, published line added); H3 removed image1.jpg | d16e3e122b29 | 9aa84197d11e |
| LAUNCH/START_HERE_LAUNCH_Humanities_Autumn1.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 5a15bb3b8c69 | d864983d6f74 |
| LAUNCH/Week_3/LAUNCH_Humanities_Autumn1_W3_Archive_Evaluation.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 4f7cfcf4a258 | 4f7cfcf4a258 |
| LAUNCH/Week_3/LAUNCH_Humanities_Autumn1_W3_Archive_Evaluation.pptx | untouched: original bytes | f5918c78fb61 | f5918c78fb61 |
| LAUNCH/Week_3/LAUNCH_Humanities_Autumn1_W3_Archive_Evaluation_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | c72b13fa8df5 | 900af0e2c2ff |
| LAUNCH/Week_3/LAUNCH_Humanities_Autumn1_W3_Archive_Evaluation_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | eedfc3493027 | 137eb82d0025 |
| LAUNCH/Week_3/LAUNCH_Humanities_Autumn1_W3_Archive_Evaluation_Teacher.docx | H3 removed image1.jpg | 4e2cb4991740 | 736d0dd6693e |
| LAUNCH/Week_3/LAUNCH_Humanities_Autumn1_W3_Archive_Evaluation_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 492d8bf14aa6 | 29dc5b3e5884 |
| LAUNCH/Week_4/LAUNCH_Humanities_Autumn1_W4_Timeline.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 4d75133e9c7d | 4d75133e9c7d |
| LAUNCH/Week_4/LAUNCH_Humanities_Autumn1_W4_Timeline.pptx | untouched: original bytes | 208f1768a99e | 208f1768a99e |
| LAUNCH/Week_4/LAUNCH_Humanities_Autumn1_W4_Timeline_Pupil.docx | H3 removed image1.jpg, image2.png | c0a444468016 | d80672cadaef |
| LAUNCH/Week_4/LAUNCH_Humanities_Autumn1_W4_Timeline_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 1b6cbe8b97bc | 53863eb55792 |
| LAUNCH/Week_4/LAUNCH_Humanities_Autumn1_W4_Timeline_Teacher.docx | H3 removed image1.jpg | b3820f58bf5c | 9f9e00ac07ce |
| LAUNCH/Week_4/LAUNCH_Humanities_Autumn1_W4_Timeline_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | cc69ff4f4430 | f2a5fb24a41f |
| LAUNCH/Week_5/LAUNCH_Humanities_Autumn1_W5_People_And_Impact.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 0c456693e782 | 0c456693e782 |
| LAUNCH/Week_5/LAUNCH_Humanities_Autumn1_W5_People_And_Impact.pptx | untouched: original bytes | a45cb58355f4 | a45cb58355f4 |
| LAUNCH/Week_5/LAUNCH_Humanities_Autumn1_W5_People_And_Impact_Pupil.docx | H3 removed image1.jpg, image2.png | 25946fc84dca | 6dbb915fd521 |
| LAUNCH/Week_5/LAUNCH_Humanities_Autumn1_W5_People_And_Impact_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | ef5ba50bf0a5 | 085e95f54805 |
| LAUNCH/Week_5/LAUNCH_Humanities_Autumn1_W5_People_And_Impact_Teacher.docx | H3 removed image1.jpg | 31ddaaaced1f | 7ebf3c369675 |
| LAUNCH/Week_5/LAUNCH_Humanities_Autumn1_W5_People_And_Impact_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 3cfe7d5c1d0c | 8581546a4602 |
| LAUNCH/Week_6/LAUNCH_Humanities_Autumn1_W6_Evidence_Account.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | bd863d17451b | bd863d17451b |
| LAUNCH/Week_6/LAUNCH_Humanities_Autumn1_W6_Evidence_Account.pptx | untouched: original bytes | 9a8f4664bca2 | 9a8f4664bca2 |
| LAUNCH/Week_6/LAUNCH_Humanities_Autumn1_W6_Evidence_Account_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | 0401c7b45b1a | 140dfb2c1824 |
| LAUNCH/Week_6/LAUNCH_Humanities_Autumn1_W6_Evidence_Account_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 1a78229243a9 | cbfdbd877e94 |
| LAUNCH/Week_6/LAUNCH_Humanities_Autumn1_W6_Evidence_Account_Teacher.docx | H3 removed image1.jpg | c707342af2b9 | 28f28abf5f88 |
| LAUNCH/Week_6/LAUNCH_Humanities_Autumn1_W6_Evidence_Account_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | b572fe462c0a | c7f3540cbbed |
| LAUNCH/Week_7/LAUNCH_Humanities_Autumn1_W7_Source_Assessment.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | 2258c07eac21 | 2258c07eac21 |
| LAUNCH/Week_7/LAUNCH_Humanities_Autumn1_W7_Source_Assessment.pptx | untouched: original bytes | f3f6397ca4be | f3f6397ca4be |
| LAUNCH/Week_7/LAUNCH_Humanities_Autumn1_W7_Source_Assessment_Pupil.docx | H1 ×1 (Adolphus 21→24); H3 removed image1.jpg, image2.png | 299551ef1bc9 | 2ddbc99c2143 |
| LAUNCH/Week_7/LAUNCH_Humanities_Autumn1_W7_Source_Assessment_Pupil.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | cc9203b0b4f0 | 85f7fafbd60e |
| LAUNCH/Week_7/LAUNCH_Humanities_Autumn1_W7_Source_Assessment_Teacher.docx | H3 removed image1.jpg | 4265c15d2f49 | f8ea13843e4e |
| LAUNCH/Week_7/LAUNCH_Humanities_Autumn1_W7_Source_Assessment_Teacher.pdf | regenerated (LibreOffice 24.2 headless) from the fixed source | f52f53bc6012 | f05d31771055 |
