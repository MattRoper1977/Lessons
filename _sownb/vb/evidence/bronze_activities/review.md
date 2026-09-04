# Bronze activity draft review

Reviewed all 14 draft activities, both replacement registers, the 48 exact early replacements against `Lessons-Classroom-Chassis/tools/artsaward/content`, and `tools/artsaward/SPEC.json`. Repository and drafts remain untouched.

**Draft data checks:** 14/14 answer mappings resolve; 14/14 pupil task text, choices and staff keys agree between screen/print draft structures; 14/14 stage durations match the original specs; 7/7 early source hashes match; 48/48 proposed early replacement pointers match exact source text. Print-key hiding, keyboard/touch behavior and final page layout still depend on the renderer and are not established by JSON equality.

The 48 early replacements are substantively justified: they remove false extra evidence rules, allow non-numeric checks and accessible responses, distinguish a locator from evidence, and respect pupils' own views. They preserve the registered expectation for actual participation/improvement, real audience experience with review sharing, real-practitioner research, and actual skills-share delivery. They do not turn the practice interactions into assessed evidence or change award rules/caps. No wholesale rollback is recommended.

## Actionable findings

### BR-1 — The printed skill-card prompt still requires a number

- Source: `tools/artsaward/content/BRONZE_W1_A2.json` at `/print/focusRows/1`.
- Text: `One measure with a number in it, starting with the words I can`.
- The early replacement register correctly changes the screen instructions and printed Extend/check rows to permit a count **or a checkable feature**, but omits this pupil-facing print prompt. Applying the 48 replacements unchanged leaves the print sheet contradicting the revised model and activity.
- Fix this one row to require a checkable goal; e.g. `One checkable measure, starting with the words I can`.

### BR-2 — Changed figures retain old contradictory accessible labels

- `BRONZE_W1_A1.json`, `/stages/5/blocks/7/alt` still names `ABOUT THE MAKER` after replacement 8 changes the visible heading to `NEEDS MORE DETAIL`.
- `BRONZE_W2_A3.json`, `/stages/5/blocks/10/alt` still says `only one strip proves anything` after replacement 30 removes that false statement from the visible caption.
- `tools/easter/spec_figures.py` copies `b["alt"]` into the SVG's `aria-label`; regenerating the figure alone does **not** fix either accessible label.
- Update those two `alt` strings with their visual figure, then regenerate print SVGs. In the second figure also align `/stages/5/blocks/10/boxes/0/line2` (`the change left is your practice`) with replacement 31's more accurate `easier to judge what practice changed`; otherwise the visible diagram retains the causal certainty removed from the adjoining prose.

### BR-3 — W3 A5 retains the old unrelated staff answer key

- Source: `BRONZE_W3_A5.json`, `/stages/4/data-ta2`.
- It gives `4B pencil`, `ruler and the fineliner`, and `two paints` as answers to the former change/tool matching activity.
- The draft now supplies an ordering activity. Replacing only stage blocks leaves this contradictory answer key in teacher tools.
- Remove or replace this attribute using the new activity's staff key; do not display both keys.

### BR-4 — W3 A5 staff access route still loses the before state

- Source: `BRONZE_W3_A5.json`, `/stages/5/data-ta2`.
- Text directs staff to give pupils with no photo a `ring-and-date option`; ring the part and write the week number.
- The new activity and replacement 36 correctly say a ring cannot preserve a mark that is subsequently changed. This surviving staff instruction sends the pupil down the opposite route.
- Replace with a copy/unchanged-sample route, or retain the original and make the change on a fresh test piece.

### BR-5 — W3 A5 ordering key treats one optional ordering as compulsory

- Draft: `early/BRONZE_W3_A5.json`, `instruction` and `items`.
- It requires reading feedback at position 1 and keeping a before copy at position 2. Keeping the before copy first, then reading/naming the feedback, also satisfies the important dependency: both precede changing the piece.
- The instruction currently says only `Put the four actions in order`, so the fixed key would reject this safe alternative without explaining why.
- Either describe the task as reproducing the demonstrated model order and explicitly accept other safe orders in staff guidance, or accept both first-two-card orders. The late B3 draft already distinguishes its model order from other valid review orders.

## Fact/source and accessibility review

The four Part C model facts independently agree with the Barbara Hepworth Estate's [biography](https://barbarahepworth.org.uk/biography/) and [Assembly of Sea Forms record](https://barbarahepworth.org.uk/sculptures/1972/assembly-of-sea-forms/): birthplace, sculpture training, marble-carving teacher, and the named work's material. The supplied direct sculpture URL is a justified correction. No invented attendance, booking or practitioner meeting appears in the new activities.

The draft language and tasks are suitable for secondary pupils working at BUILD's reading level without primary framing. Pointing, speech, adult-supported recording and native controls are specified; no drag-only task, score or timed answer is required. The four-category C2 task explicitly permits justified cross-category connections. Preserve that guidance in final teacher tools rather than mechanically treating every supported secondary connection as wrong.

Optional video playback/captions were explicitly unverified by the media author and have not been tested in this review. Do not describe those as verified. No broader optional rewrite is requested by this review.
