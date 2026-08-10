# Made by Matt — Public Baseline Weeks HTML pack

Purpose: static public-site equivalents of the first-two-weeks PythonAnywhere baseline assessments.

Included:
- index.html
- baseline-reading-writing-standard.html
- baseline-reading-writing-specialist-semh.html
- baseline-maths-standard.html
- baseline-maths-specialist-semh.html
- baseline-science-standard.html
- baseline-science-specialist-semh.html
- baseline-profile-review.html

Pathways:
- Pathway A — Standard Transitions
- Pathway B — Specialist / SEMH

Assessment names:
- Reading & Writing Baseline
- Maths Baseline
- Science Baseline

Profile rule:
No overall baseline score, grade, pass/fail, diagnosis or automatic placement.
Use strand evidence + teacher observation + pupil voice.

Public/data-protection design:
- no name/ID fields
- no form submission
- no fetch/XHR/beacon
- no cookies
- no localStorage/sessionStorage/IndexedDB
- no analytics code
- no external libraries or media
- typed answers exist in the page DOM only and disappear on refresh/close
- the school must use its own approved system if it retains evidence

The static profiles are deliberately not a substitute for the private PythonAnywhere teacher workflow.

## These pages are not secure tests

Each assessment carries its own correct answers inside the page (`DATA.items[].correct`, read by
the scoring block). Anyone who views the page source — including a pupil — can read the key.

For a low-stakes starting-point check that may be perfectly acceptable. It is written down here so
that it is a decision rather than an accident. Do not use these pages anywhere the answers being
visible would matter. Removing the key is a redesign of the assessment, not a repair, and has not
been done.
