# RX2 P3.7 — Activity audit (controls classified by BEHAVIOUR, not by markup)

Method: every lesson opened in headless Chromium (1280×800, file://); every `.slide` shown in turn; every visible button/input/select/textarea/summary inside the slide (chassis navigation excluded) driven once — a click, a typed value, a select change. **EVIDENCE-CHANGING** = a form value, aria-pressed/aria-checked or a data-choice/selection state changed and persisted after the interaction; **REVEAL-ONLY** = nothing recorded, only hidden content became visible (or text grew); **INERT/NO-CHANGE** = no observable change (typically the slide's own "check" button before any choice). Stage titles come from `data-title`; the model/independent stages are the ones P3.7 asks to upgrade.

| lesson | batch | slides | evidence-changing | reveal-only | inert | reveal-only controls in model/independent stages |
|---|---|---|---|---|---|---|
| b2_build_art_light_study.html | new | 10 | 7 | 4 | 2 | — |
| b2_build_art_steady_beat.html | new | 10 | 8 | 2 | 2 | — |
| b2_build_asdan_helpful_plan.html | new | 10 | 9 | 2 | 1 | — |
| b2_build_asdan_useful_roles.html | new | 10 | 8 | 2 | 1 | — |
| b2_build_humanities_celebration_order.html | new | 10 | 8 | 2 | 1 | — |
| b2_build_humanities_fair_chance.html | new | 10 | 7 | 2 | 1 | — |
| b2_build_science_materials.html | new | 10 | 12 | 2 | 1 | — |
| b2_build_science_rock_uses.html | new | 10 | 8 | 2 | 2 | — |
| b2_grow_art_group_part.html | new | 10 | 12 | 2 | 2 | — |
| b2_grow_art_light_study.html | new | 10 | 7 | 4 | 2 | — |
| b2_grow_asdan_idea_evidence.html | new | 10 | 7 | 2 | 1 | — |
| b2_grow_asdan_plan_station.html | new | 10 | 9 | 2 | 1 | — |
| b2_grow_humanities_compare_celebrations.html | new | 10 | 5 | 2 | 1 | — |
| b2_grow_humanities_festivals_places.html | new | 10 | 7 | 2 | 1 | — |
| b2_grow_science_climate.html | new | 10 | 8 | 2 | 2 | — |
| b2_grow_science_day_night.html | new | 10 | 8 | 1 | 2 | — |
| b2_launch_art_identity_culture.html | new | 10 | 9 | 2 | 1 | — |
| b2_launch_art_portfolio_piece.html | new | 10 | 7 | 4 | 2 | — |
| b2_launch_asdan_team_contract.html | new | 10 | 8 | 2 | 1 | — |
| b2_launch_asdan_team_schedule.html | new | 10 | 8 | 2 | 1 | — |
| b2_launch_humanities_grid_references.html | new | 10 | 8 | 2 | 1 | — |
| b2_launch_humanities_settlement_change.html | new | 10 | 4 | 2 | 1 | — |
| b2_launch_science_dna.html | new | 10 | 10 | 2 | 2 | — |
| b2_launch_science_mitosis.html | new | 10 | 9 | 3 | 2 | — |
| build_art_marks.html | pre | 10 | 4 | 2 | 1 | — |
| build_humanities_belonging.html | pre | 10 | 12 | 5 | 1 | — |
| build_science_permeability.html | pre | 10 | 13 | 8 | 1 | — |
| grow_asdan_small_test.html | pre | 10 | 2 | 4 | 2 | — |
| grow_humanities_connections.html | pre | 10 | 11 | 4 | 2 | — |
| grow_science_friction.html | pre | 10 | 6 | 2 | 2 | — |
| launch_art_review.html | pre | 10 | 8 | 5 | 1 | — |
| launch_humanities_archive.html | pre | 10 | 12 | 5 | 1 | — |
| launch_science_punnett.html | pre | 10 | 20 | 7 | 3 | I do: “P + P”<br>I do: “p + P”<br>I do: “P + p”<br>I do: “p + p”<br>Independent: “Open the grid · choose Pp × pp” |

Totals over 33 lessons: evidence-changing 281, reveal-only 96, inert 48; reveal-only controls sitting in model/independent stages: 5.

Status: CLASSIFIED, NOT UPGRADED. The upgrade (predict → act → observe → explain with the prediction retained, a new independent case, one red-proved check per change in the pack's node harness, timings still 40) is authoring in the pack's editable-source JSON + interactions and a rebuild through its renderer; it was not attempted in this order (see the readback residue).
