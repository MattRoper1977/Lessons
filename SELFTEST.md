# Class tools self-test

Tested the review build on 17 November 2026 with an isolated browser profile and invented pupil data. Both the personal and staff editions were exercised through their normal page controls.

## Screen and interaction checks

| Check | 360 × 740 | 1366 × 768 |
| --- | --- | --- |
| Open the ten edited class tool pages, the public taster and the guide with fresh storage | Pass | Pass |
| Check page width and startup script errors | Fits the viewport. No uncaught startup errors | Fits the viewport. No uncaught startup errors |
| Load a version 1 profile with four free-text lines and a long, multiline private note | Original values preserved | Original values preserved |
| Select eight print choices, save, reload and add another pupil | Ninth unchecked choice disabled. Eight choices retained | Same result |
| Edit the print note and save | Single-line input, 120-character limit, note restored | Same result |
| Open **Start my day** during a period | One new tab loaded the verified art or science lesson. Day list remained in the tools tab | Same result |
| Apply the staff lag and subject prefix | Dashboard, card and capture all gave `SCI_BUILD_A2_W02_L2` for week 3 with lag 1 | Same result |
| Advance the clock from 09:40 to 10:01 across the saved 10:00 boundary | **Now** moved to period 2. The card displayed saved times | Same result |
| Inspect a group with an adaptation, a prior absence and an open catch-up item in first-name mode | Strip showed P1 and the open item. Neither part of the private label appeared | Same result |
| Follow **Quick capture** on a period card | Selected week, day and period matched the card | Same result |
| Replay every requested page tour, including the launcher tour | Next, Back, Done, Skip and Escape worked. Completed visits stayed closed on reload | Same result |
| Choose a different pretend pupil and change their sheet | Five help options and cream tint affected only the selected sheet. Reload kept the choice | Same result |
| Play, pause, replay and finish the walkthrough | Four frames over 36 seconds. Pause held the frame. Calm Mode and reduced motion showed all four still frames | Same result |
| Check taster storage access during load, selection, replay settings and clear | All observed reads and writes used the try-out prefix. Clear removed the three try-out keys | Same result |
| Monitor taster requests while using the controls | Only the initial page navigation was requested | Same result |
| Filter the guide by “private”, expand a result, then search for an absent word | Matching tasks shown. Empty-result message shown | Same result |

Additional phone checks passed in both editions. Imported an old private copy, added a tag and print note, exported the new copy, changed the form and restored the export. Moved the start of term and followed a card into the corresponding week in capture. After the last period, the next card was labelled **Next** under the following school day. Starting an unmatched staff period opened zero tabs and showed **No linked lesson**.

## Print

At both viewport sizes the selected pupil’s sheet produced one A4 page. The test sheet belonged to Pupil 2 and used large print, extra space, sentence starters, a word bank, fewer questions and cream paper. With background graphics switched off, the rendered print still showed the cream sheet, two tasks and the chosen supports. The rendered page contained only the pupil’s activity.

The guide produced two A4 pages at both sizes, including when a search was active. The first page contained My page and Apps. The second contained Lessons and Tools. Inspected the rendered pages for text, button drawings, clipping and page breaks. These checks used print-to-file. Physical printer and driver output was outside this test.

## Contrast

Measured resolved foreground and opaque background colours in the rendered pages. Ratios use relative sRGB luminance. Repeated the measurements at both viewport sizes. The table covers the new interfaces and the shared tour controls in the default display.

| Text and surface | Foreground | Background | Ratio |
| --- | --- | --- | --- |
| Lowest public page text, secondary text on the page background | #3e534b | #f8f8f0 | 7.74:1 |
| Public selected button | #ffffff | #17483b | 10.36:1 |
| Lowest launcher text, link on the panel | #123d32 | #f2f6f3 | 11.07:1 |
| Launcher primary button | #ffffff | #153e33 | 11.87:1 |
| Print picker labels | #172c3b | #ffffff | 14.38:1 |
| Tour buttons | #183c31 | #ffffff | 12.14:1 |
| Tour text | #172e2a | #fffbea | 13.86:1 |
| Disabled tour button | #384734 | #eceee4 | 8.46:1 |
| Sheet ink on white / blue / green / pink / cream | #1b3029 | #ffffff / #e4f2fb / #e6f3e8 / #fbeaf0 / #fff3d7 | 13.99 / 12.25 / 12.22 / 12.07 / 12.69:1 |

## Source and release checks

- Checked all 386 embedded mappings in each edition against the catalogue and the repository file tree.
- Compared existing manifest declarations, content security declarations and outside addresses in all ten edited class tool pages with the base revision. All matched.
- Parsed the inline scripts. Checked both public pages for outside navigation, external assets, runtime requests and service worker registration.
- The lesson print patch and the wider site tour are handoff documents. Their application to lesson, app and My page templates belongs to the receiving thread.
