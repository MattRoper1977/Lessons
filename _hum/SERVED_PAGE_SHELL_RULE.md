# The served-page shell rule — a whole document by DOM, not tags by grep

**Ruled by Matt Roper, 2026-09-22 (STOP-R2, point 3). This replaces the wording added on
2026-09-21 ("the intake battery asserts an HTML shell on every served page").**

## The rule

> Every served page must be a **parseable whole document**, and the intake battery asserts that
> **by DOM** — load the bytes in a real HTML5 parser and read the document back — never by
> grepping for `</head>` and `</body>`.

## Why the wording had to change

The first wording said "asserts an HTML shell", and the check written for it asked whether the
bytes contained `</head>` **and** `</body>`. Two things went wrong at once.

1. **It mistook tag presence for wholeness.** Fifty Summer 1 pages opened
   `<!doctype html><html lang="en-GB">…` and closed `</html>` with `<head>` and `<body>`
   *implied*, as HTML5 allows. They were whole documents. The grep called them fragments.

2. **It could not see the damage from the remedy it caused.** The corrective built on that
   reading wrapped each page in a second document. Afterwards the substrings `</head>` and
   `</body>` were both present, so the same grep — and the publication's own adapter, which
   uses the same test — reported success on pages carrying two doctypes and two `</html>`.

A test that passes both on a document it wrongly calls broken and on the broken thing its own
remedy produces is not a test. What caught it was running the estate's real adapter over the
output and asserting on the result.

## What the battery asserts, from here

For every served page, before any table is presented:

1. A real HTML5 parser loads the bytes and returns a document — **Chromium** where the page is
   served by the browser, via `tools/hum/dom_oracle.mjs`.
2. That document has exactly one doctype, one `<html>`, one `<head>` and one `<body>`.
3. Where a page has been edited, the parsed document is compared **before and after**:
   `doctype`, `head.innerHTML`, `body.innerHTML`, `title` and the element count must agree,
   unless the edit was meant to change them and the change is the one declared.

**lxml is not admissible as this oracle**, and that is red-proved in
`tools/hum/explicit_document_tags.py --self-test`: libxml2 does not implement HTML5's
head/body inference, so on a real Knowledge Organiser (a `<button>` as the first flow content)
it puts that button inside `<head>`, never opens `<body>`, and calls an exact mark-up a change.

## What is still true from the old wording

Row 45 (and 46 for RE) is still measured before any table is presented, with the estate's own
oracle `tools/hum/verify_loop.py::panels` and not a regex; and the row is never "absent by
design" on a lesson the hub will list as current.
