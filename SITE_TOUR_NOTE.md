# Add “Show me round” through shared navigation

Proposal for the ruling thread. The implementation in the class tools is the reference. Each page supplies three to five entries to `initToolTour`. Each entry has a target selector, the visible button name, and a short sentence around that name.

## One change for lesson pages

In `assets/catalogue/lesson-navigation.js`, mount the help button after the existing `mount()` creates `#mbm-lesson-tools`. Put the tour function and lesson step list in that same navigation file. Keep a reference to the mounted controller. The existing observer may run `mount()` many times. Append **? Help** only once per document and keep tour state when the navigation measures itself again. For pages without this navigation file, the page owner can include the approved shared entry point when their template is next updated.

Attach each step to the visible control in the current template. Read its printed caption or accessible label. For a drawer, use the button that opens it. A missing feature is omitted from that page’s list. A tour never opens a print window, starts a timer or changes pupil work.

| Place | Suggested sentence |
| --- | --- |
| Eight-step bar, first visible step | Press **Arrival** to choose a lesson step. |
| Teacher notes | Open **Teacher notes** to see how to teach this lesson. |
| Print tools | Open **Tools & Print** to choose a pack. |
| Pupil packs | Open **My pupils** to print one pupil’s sheet. |
| Calm reset | Press **Start Calm 60** for a quiet minute. |

Use the actual label in each template. For example, the inspected lesson has `.nav-step[data-go]`, `[data-dialog="staff"]`, `[data-dialog="tools"]`, `[data-dialog="mypupils"]` and `[data-t-start]`. Its staff control says **Staff card**, so that sentence becomes “Open **Staff card** to see how to teach this lesson.” Pick the **Arrival** step by its accessible label. Where the quiet control says **Calm reset**, use “Press **Calm reset** for a quiet minute.”

## Apps and My page

Use the same controller in their shared navigation after the real buttons are present. Suggested **My page** steps are “Press **Search** to find a page.”, “Open **Apps** to find an activity.” and “Open **Lessons** to find your lesson.” On the Apps index use “Press **Browse the suite** to see the activities.” Add two short steps for real controls on each app, such as “Press **Start** to begin.” and “Press **Reset** to start again.” Keep only labels that exist on that screen.

## First visit and replay

Use `mbm_tour_seen_v1` as an object of boolean flags. Use the canonical same-site lesson path as its entry, or a stable app/page ID. Ignore query strings and fragments. Merge the flag when showing the first step. Store no pupil labels, choices, answers or timestamps. If device storage is blocked, keep the flag in memory for the visit. The public taster has its own `mbm_try_tour_seen_v1`.

Give **? Help** a stable home in the top bar. Place the current sentence beside the target in normal reading order. Mark that button with an outline and bold its name in the sentence. Keep **Back**, **Next** and **Skip the tour** in keyboard order. The last **Next** becomes **Done**. Close on Escape and return focus to the opener when focus was inside the tour. A first visit leaves focus where it was. Use the same still presentation in Calm Mode and under reduced motion. Hide tour controls in print.

The rolling sequence is lesson templates, then Apps, then My page, subject to approval. The class tools branch makes no changes to those files.
