# Read the pupil’s print choices

For the ruling thread and lesson-page owner. The example matches the catalogue lesson at `Science/Build/Autumn_2_2026-27/SCI_BUILD_A2_W02/SCI_BUILD_A2_W02_L1.html`. Apply the same changes to pages with the same print builder. Pages with a different builder need the equivalent changes at their own pupil selection and print boundary.

## 1. Collect the four help lines and up to eight choices

In the pupil loop, replace the line that sets `tags` from `rec.adapt.slice(0, 4)` with the following code. The version 1 profile and the four free-text matchers keep their current meaning.

```js
const lines = Array.isArray(rec.adapt) ? rec.adapt.slice(0, 4) : [];
const picks = Array.isArray(rec.tags) ? rec.tags.slice(0, 8) : [];
const tags = [...new Set([...lines, ...picks]
  .filter(tag => typeof tag === 'string')
  .map(tag => tag.trim())
  .filter(Boolean))];

const printNote = rec.printNote === true && typeof rec.note === 'string'
  ? rec.note.replace(/[\r\n]+/g, ' ').trim().slice(0, 120)
  : '';
```

An old private note may contain several lines. Class names keeps that original text until the teacher edits the field marked **Note for the top of this pupil's print**. Editing sets `printNote` on that pupil. Only then does the text belong on a pupil’s sheet.

## 2. Pass the choices through the print builder

Replace the print button’s event handler and the builder’s opening line as shown.

```js
pBtn.addEventListener('click', () =>
  window.buildAdaptedPupilPrint(id, disp, tier, tags, printNote));
```

```js
window.buildAdaptedPupilPrint = function(pupilId, labelStr, tierName, adaptTags, printNote = '') {
```

Inside the builder, replace the four-item slice with the following line. The existing matchers for print size, fewer questions, space, tints, starters, word banks and visual steps now receive the complete list.

```js
const tags = Array.isArray(adaptTags)
  ? adaptTags.slice(0, 12).filter(t => typeof t === 'string').map(t => t.toLowerCase())
  : [];
```

After cloning the tier into `dyn`, and after setting `tags`, add this block. The first paper gets the note once. Cloning the tier again for the next pupil removes the previous note.

```js
if (tags.includes('one task at a time')) dyn.classList.add('adapt-one-task');
if (printNote) {
  const note = document.createElement('p');
  note.className = 'pupil-print-note';
  note.textContent = printNote;
  (dyn.querySelector('article.paper') || dyn).prepend(note);
}
```

## 3. Keep the tint on the print

Append to the lesson’s print rules. The existing tint selectors still choose the paper colour.

```css
@media print {
  #dynamicPupilPrint[class*="adapt-tint-"] :is(article.paper, .activity-box) {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  #dynamicPupilPrint .pupil-print-note {
    color: #172e2a;
    font-weight: 700;
    margin: 0 0 3mm;
    overflow-wrap: anywhere;
    break-after: avoid;
  }
  #dynamicPupilPrint.adapt-one-task .activity-box ~ .activity-box {
    break-before: page;
  }
}
```

## Acceptance check on the receiving branch

1. Load an old version 1 profile with four help lines and a private note. Check that its old adaptations work and the private note stays off the print.
2. Choose eight print options. Put a tint among the last four. Enter a short print note, including an angle bracket, and press **Save on this device**.
3. Open **My pupils** and press **Print adapted pack**. Inspect the first sheet for the literal note, the later choices and the tint with background graphics switched off.
4. Print a different pupil’s pack and then a standard tier. Check that each print contains only its own choices and note.
