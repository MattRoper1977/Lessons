# RX2 P3.4 — Chassis map (token source per family)

Pack contract: `_sownb/STYLE_CONTRACT_v2.json` sha d81e16dd65bb…, recorded source_commit c4cfa942. Measured at Lessons main 1c2505f7: every donor exists, its whole-file sha256 and its first inline `<style>` block sha256 equal the manifest (no drift since c4cfa942), and every one of the 33 lessons' first style block equals its family stylesheet byte for byte.

| family | donor at Lessons main | donor sha == manifest | first-style sha == manifest | donor patches | token source | pathway tokens (--lo-border / --task-border / --aspire-border) |
|---|---|---|---|---|---|---|
| BUILD ASDAN | BUILD_ASDAN/Living_Independently/LI_W6_Shopping_and_Change.html | yes | yes | 0 | donor's own first inline style block (literal) | #7E6BA6 / #D7A43C / #7E6BA6 |
| BUILD Art | Art_Teesside/Build/BUILD_ART_W1_The_Local_Canvas.html | yes | yes | 0 | donor's own first inline style block (literal) | #4F869C / #E1AB32 / #22c55e |
| BUILD Humanities | Build/Slideshows/BUILD_HUM_W6_Plan_The_Story.html | yes | yes | 0 | donor's own first inline style block (literal) | #9c27b0 / #eab308 / #22c55e |
| BUILD Science | Science_Teesside/Build/SCI_B_W5_Right_Nutrition.html | yes | yes | 2 | donor's own first inline style block (literal) | #4E7A9B / #D8A63B / #4E7A9B |
| GROW ASDAN | GROW_ASDAN/PEQ/PEQ_W6_Present_My_Progress.html | yes | yes | 0 | donor's own first inline style block (literal) | #4A6FA5 / #D3A03C / #4A6FA5 |
| GROW Art | Art_Teesside/Grow/GROW_ART_W8_Reflect_Audit_and_Close_the_Loop.html | yes | yes | 0 | donor's own first inline style block (literal) | #5B91A5 / #DFAD3E / #22c55e |
| GROW Humanities | Grow/Slideshows/GROW_HUM_W8_Where_In_The_World.html | yes | yes | 0 | donor's own first inline style block (literal) | #9c27b0 / #eab308 / #22c55e |
| GROW Science | Science_Teesside/Grow/SCI_G_W6_Earth_And_Planets.html | yes | yes | 2 | donor's own first inline style block (literal) | #3F7D6E / #D8A63B / #3F7D6E |
| LAUNCH ASDAN | LAUNCH_ASDAN/Vocational/VOC_W5_Tools_Equipment_and_Safe_Use.html | yes | yes | 0 | donor's own first inline style block (literal) | #96603C / #8AA662 / #96603C |
| LAUNCH Art | Art_Teesside/Launch/LAUNCH_ART_W6_Pilot_Lead_and_Adapt.html | yes | yes | 0 | donor's own first inline style block (literal) | #356F83 / #C18B2D / #22c55e |
| LAUNCH Humanities | Launch/Slideshows/LAUNCH_HUM_W8_OS_Map_Skills.html | yes | yes | 0 | donor's own first inline style block (literal) | #9c27b0 / #eab308 / #22c55e |
| LAUNCH Science | Science_Teesside/Launch/SCI_L_W6_L1_ActiveTransport.html | yes | yes | 2 | donor's own first inline style block (literal) | #7A5C9E / #D8A63B / #7A5C9E |

Pathway palettes per subject:
- ASDAN: distinct token sets per pathway (BUILD, GROW, LAUNCH)
- Art: distinct token sets per pathway (BUILD, GROW, LAUNCH)
- Humanities: the SAME token set on all three pathways in the donors (BUILD, GROW, LAUNCH)
- Science: distinct token sets per pathway (BUILD, GROW, LAUNCH)
