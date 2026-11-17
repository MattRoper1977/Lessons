# Class tools review return

Built from Lessons revision `baca32ab146ec6650cff65b77b061b79d16da272` for review on `lane/tools-launcher-trial`. The ruling thread controls release.

## Files in this return

| File | Reason |
| --- | --- |
| `kits/class_tools/Class_names.html` | Adds the eight-choice picker and print-note field to each pupil card. Handles save, reload, private copies and the page tour. |
| `kits/class_tools/trial/Class_names.html` | Adds the same picker and tour using the trial’s group, privacy and backup controls. |
| `kits/class_tools/My_tools.html` | Adds the launcher, verified lesson map, period tools, sample day, guide link and separate dashboard and launcher tours. Uses the built-in timetable, saved times and term dates. |
| `kits/class_tools/trial/My_tools.html` | Adds the launcher and tours. Reads the school timetable, uses configured group codes and fixes the shared lesson calculation. |
| `kits/class_tools/Quick_capture.html` | Opens the week, day, period and shared pathway selected on a card. Reads the dashboard’s saved term dates. Adds the capture tour. |
| `kits/class_tools/trial/Quick_capture.html` | Accepts the same period link. Uses the school groups, term, subject prefixes and stored lag for the selected lesson. Adds the capture tour. |
| `kits/class_tools/Class_record.html` | Adds the first-visit and replay tour to the class record. |
| `kits/class_tools/trial/Class_record.html` | Adds the class record tour to the staff edition. |
| `kits/class_tools/Catch_up_Tracker.html` | Adds the first-visit and replay tour to the catch-up views. |
| `kits/class_tools/trial/Catch_up_Tracker.html` | Adds the catch-up tour to the staff edition. |
| `kits/class_tools/try/index.html` | Adds the six-pupil public taster, live print preview, 36-second walkthrough, still frames, clear action and full-version enquiry route. |
| `kits/class_tools/guide/How_it_all_works.html` | Adds nine searchable task cards under My page, Apps, Lessons and Tools. Includes a two-page quick start. |
| `LESSON_PAGE_PATCH.md` | Gives exact changes for reading both types of help, printing a pupil note and keeping paper tints. |
| `SITE_TOUR_NOTE.md` | Gives the receiving thread a shared navigation integration point, five suggested lesson steps and suggested Apps and My page wording. |
| `SELFTEST.md` | Records screen sizes, functional checks, print results, contrast measurements and test limits. |
| `CHANGES.md` | Lists the files, the rulings applied and the storage and lookup behaviour. |

## Lesson codes before and after

The trial previously read the saved lag but built the dashboard code from the calendar week. It also used its built-in subject prefix table for that code. The shared `lessonCode` now calls `taughtWeek` and uses the school pack’s subject prefix when present. Both the dashboard and the launcher call the existing active-lesson function. Quick capture uses the same computation for the period handed to it.

For example, with prefix `SCI`, group `BUILD`, term `A2`, week 3, lesson 2 and a saved lag of 1, the week portion used to be `W03`. It is now `W02`, giving `SCI_BUILD_A2_W02_L2`. The earliest possible week is 1. The school pack still stores lag in `lessonLag`, keyed by `group|subject`.

The personal edition keeps its built-in weekly timetable and existing lesson-code rules. The launcher reads the same school clock as the dashboard. After the last period, the next scheduled lesson appears under its own date. A trial device without a saved timetable shows the sample and **School Setup** instructions.

## Lesson addresses and pupil display

Both launchers embed a static map of 386 unique lesson codes built from `resources.json` and `assets/catalogue/lesson-order.json`. The build matched exact catalogue lesson filename codes, checked canonical destinations against the repository tree and kept only unambiguous local HTML paths. Runtime catalogue requests are unnecessary. To refresh the map, repeat those checks on a single catalogue revision and update both embedded tables together.

**Start my day** opens at most one tab. **See today’s periods** opens the list in place. A card with an unmatched code says **No linked lesson** and explains where to check the codes. Existing personal outside links and manifest declarations were preserved.

The period strip shows only pupil codes or initials. First-name mode falls back to a pupil code there. The strip reads the group’s prior scheduled period for the same subject, the attendance and coverage records, and the outstanding catch-up items. Quick capture receives only timetable fields in its relative link.

## Profiles, tours and public pages

The profile version stays 1. Each pupil keeps the four free-text `adapt` lines. Optional `tags` holds up to eight picker choices. The existing `note` holds the print note. Older private notes survive unrelated edits and exports. Editing the newly labelled field sets `printNote: true` and limits the new note to one line of up to 120 characters. This distinction prevents an old private note from appearing on a pupil’s print automatically.

The same tour controller is embedded in each requested page with a small per-page step list. The launcher has its own first-visit entry. The licensed pages use `mbm_tour_seen_v1`. The taster uses only `mbm_try_sheets_v1`, `mbm_try_calm_v1` and `mbm_try_tour_seen_v1`. **Clear my try-out** removes those three entries. Its enquiry link opens the existing same-site About page, which contains the contact button. The public guide and taster contain only relative navigation links.
