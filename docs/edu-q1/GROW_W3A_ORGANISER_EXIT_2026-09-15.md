# EDU-Q1 GROW W3A — organiser and exit draft checkpoint

Status: **bounded draft complete; GROW pilot remains partial, unmerged and unpublished**. Lessons draft #538, branch `codex/edu-q1-grow-w3a-focus-20260915`. Baseline arrival head `194075db287e091a1f1fc1020c5873a00cdb1447`. Matt has selected High and authorized continuation in the master order.

## Problem and change

W3A ended after the sort without its own two-check exit, and the old printable organiser contained an over-general roughness rule. Add a reachable organiser on all seven W3A stages, with shared screen/native/print content: objective, success criteria, five key terms, qualified science facts, a labelled contact-force model, helpful/unhelpful examples and a fair-comparison reminder. The native modal opens at the top with heading focus, blocks deck shortcuts and returns focus to the invoking button on Close or Escape. The four chassis control names are retained.

Add Supported, Standard and Stretch exit routes within We Do 2. Each has two questions, fieldset/legend grouping and native controls. Routes accept pointing, speech, signing, drawing, typing, paper or adult scribing; passing is allowed and only one route/record is requested. Explanations are separate native disclosures; pupil printouts contain no answer key. Downloads preserve actual choices and blank responses, with no automatic mark or new pupil identity/support fields. Route changes preserve entered responses and close explanations. Add a reachable staff-answer print button.

Use the final two minutes of W3A's existing ten-minute We Do 2 stage; approximately eight minutes remain for the shared sort, correction and changed case. Stop at 40 minutes. W3B remains its separate 32 + 4 + 4 minutes, with all three W3B stage DOMs unchanged. New closing copy names **Friction: test the surfaces** without day/time. The shared print organiser is updated; all 15 other pre-existing print sections remain unchanged.

## Native resources and measurements

- Pupil DOCX/PDF: **13 A4 pages**. Previous pages 1–9 are pixel-identical; organiser page 10; choose one exit route on pages 11–13, each with two complete tickets.
- Teacher DOCX/PDF: **9 A4 pages**. Page 1 pacing/print directions updated; pages 2–8 pixel-identical; separate exit guidance on page 9.
- Six changed/new native pages visually inspected; all 22 final pages match the reviewed renders. Five distinct new browser print layouts and phone/desktop organiser/exit screenshots inspected. No clipping found in the reviewed outputs.
- **56 organiser cases passed**: seven W3A stages × 320/390/768/1280 × standalone/local HTTP. Heading focus, scrollTop=0 on reopen, Escape/Close return, native modality, Space/ArrowRight/ArrowDown exemption and horizontal fit.
- **24 exit cases passed**: three routes × those widths × both modes. Native summary/radio/textarea keys retain the stage; two grouped questions, explanations, route persistence, real saved response downloads and horizontal fit.
- **10 new browser PDFs**, each one A4 page: organiser, three two-ticket pupil routes and the all-route staff key in each mode. Organiser printing was exercised while its native modal was open. Question multiplicity and answer separation checked.
- **32 scoped axe runs**, zero serious/critical violations in the new organiser/exit content; no violations of any impact were returned. This is not an all-stage axe result.
- Regression: **162 focus checks**, **24 arrival cases**, **12 one-page arrival pupil/staff PDFs** passed again. Zero page runtime errors in all three harnesses.

## Reproduce

Use the existing Playwright Chromium runtime with `PYTHONPATH`, `PLAYWRIGHT_BROWSERS_PATH` and `NODE_PATH` set to its installed dependencies. From the repository root:

```sh
python tools/grow_resources/organiser_exit_checks.py . /path/to/review/new
python tools/grow_resources/arrival_checks.py . /path/to/review/arrival
node tools/grow_resources/focus_checks.cjs . /path/to/review/focus
```

`tools/grow_resources/W3A_ORGANISER_EXIT.json` supplies screen and native content. `author_w3a_organiser_exit.py` explicitly reconstructs from the pinned arrival baseline; review/rebase its BASE before applying it over any later checkpoint. Native PDFs were rendered from DOCX and visually inspected, not edited separately. The SVG is a precise labelled explanatory model, not observed pupil data or a measured force diagram.

## Hashes

| Candidate file | SHA256 |
|---|---|
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.docx` | `7f3f09fd74d7aabfa593b8ceb999bbd85d6d53289ed94a3c2e730d3f830255c0` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Pupil.pdf` | `35a640ca5b4254c4cb432b8104a4d37b62cedbb96070e72f08a84faf3f9fcf01` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.docx` | `da21ca381481dfe9993ac4b80b0b15ffb0fd8c960445e2ae7f3497773a262d7e` |
| `Science_Teesside/Teaching_Packs/GROW/lessons/W3A/GROW_W3A_Friction_Teacher.pdf` | `0b24ea34393435fd2f4357af8fbe0feb9a829a5fe49f111256ae07008c6210fd` |
| `Science_Teesside/Grow/SCI_G_W3_Friction.html` | `41cb1e7e82715ab08a559f9a95eb7db238118fd929c2850f2b7f232ab530e7da` |

No publication hash or source-admission pin is advanced in this draft checkpoint.

## Still open

Integrated optional Lundy guidance and remaining legacy day/time/compulsory-writing copy need the next coordinated checkpoint while preserving W3B's teaching boundary. Editable PPTX/slides-PDF, resource-page/download/archive/catalogue/provenance/size parity and the combined pack flow are not yet fully aligned with the new W3A arrival/exit; the individual new print choices are verified. Complete these before source admission or promotion. Existing legacy print sections are preserved, not certified by this focused pass.

Full pilot checks still include all-stage axe, themes/enlarged text/layout, motion/media/no-JavaScript, full print/resource acceptance and an actual human assistive-technology journey. Matt's successful Sugar listening pass does not accept Friction. No full GROW Ready claim; no required-CI completion claim; no merge/deploy. Original review RESULTS.md Not-run rows are unchanged.

Continue EDU-Q1: GROW W3A, then LAUNCH W4L1 with its shared guide. Then EDU-D3 → PLAY-D2 → PLAY-Q1 → PLAY-I1 → justified MAINT-1 → PLAY-X1. EDU-TRY-LESSON-20260915, EDU-HERO-20260915, EDU-HEADER-BRAND-20260915 and PLAY-BRAND-20260915 remain recorded and queued. EDU-D3 has not started. Preserve the 08:30–15:30 UK school-day merge hold, Site291/Lessons456/LP1, completed Sugar release and account/admin work. Remain on High for the next authoring/accessibility checkpoint.
