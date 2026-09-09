## D14 — What a render census has to cover

The LF1 numbers, same phrase, same 22 pages, by how it was measured:

| measured as | count |
|---|---|
| source grep, lines | 31 |
| DOM text nodes, slide 1 only | 8 |
| driving the real slide control | 72 |
| …sampling after **each** gate press, not a batch | 83 |
| …pressing both chassis conventions | 86 |
| print emulation, union over every printable tier | 35 |
| accessible names (`aria-label`) | 3 |
| **total in the document** | **121** |
| **rendering on no route at all** | **0** |

Every row of that table is a way of undercounting:

- **A count on slide 1 is not the deck.** Most slides are `display:none` until
  navigated and `showSlide` sits inside a closure, so the walk must drive the real
  `#next` control.
- **Pressing every gate then sampling once shows only the last tier chosen.**
  Supported, Standard and Stretch are three panels; sample after each press.
- **Two chassis, two conventions.** Science gates on data-attributes, Humanities
  on inline `onclick="tier(...)"` with a `.tierbtn` or `aria-expanded` button.
- **Print is a different subtree.** 35 occurrences live in the `.printpack`
  worksheet, and `SCI_B_W8B` had four in print and none on screen at load — the
  defect reached handouts before it reached a screen.
- **Accessible names are pupil-facing text.** Three occurrences were `aria-label`s
  no text-node walker can see and a screen reader reads aloud.
- **"Behind a control" is not "unseen".** Content one press away is pupil-facing.
  Reported as 11 unreachable, then 3, then **0**.
