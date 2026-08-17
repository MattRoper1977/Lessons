# PH-1 Amendment 2 §E3 — G4 detector finding

- Repository: `MattRoper1977/Lessons`
- Immutable BASE examined: `ae1d3c7af2526781aad6fb82e7cbbf6b87ded380`
- Old detector result: 147/147 witness surfaces failed at BASE before any PH-1 edit.
- Real witness surfaces opened: **3**.
- Samples with both assessor/witness and learner/candidate concepts: **3/3**.
- Samples with literal numbered Sections 4 and 5: **3/3**.

## Conclusion

**(a) the old detector pattern does not match the real witness markup.**

All three real surfaces contain numbered Sections 4 and 5, but their meanings are not identical. The BUILD ASDAN and LAUNCH PEQ sheets use Section 4 for the assessor declaration and Section 5 for learner confirmation. The D&T sheet uses Section 4 for evidence attached and Section 5 for the assessor declaration. A detector tied to one exact wording or nesting pattern can therefore fail every file even though the numbered structure is present.

This proves the old 147/147 failure was a detector-pattern failure, not evidence that PH-1 removed witness content. Replacement G4 must compare each surface with itself at BASE and tip.

## Actual markup read

### `BUILD_ASDAN/Careers/CAREERS_W1_My_Strengths.html`

- Extraction: complete element with id="print-witness".
- Assessor/witness concept: **True**.
- Learner/candidate concept: **True**.
- Section 4 marker: **True** — 4 · Assessor declaration.
- Section 5 marker: **True** — 5 · Learner confirmation.

```html
1:
<h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1>
<p style="text-align:center;margin:0 0 10px;font-size:.88rem">
<strong>BUILD ASDAN W1 · My Strengths</strong>
<br>BUILD · ASDAN Studio · Careers · Banks: ASDAN LI M8 / AQA UAS</p>
```

```html
2:
<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">2 · Level the candidate worked at — ring ONE</p>
```

```html
3:
<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">3 · Evidence attached</p>
```

```html
4:
<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">4 · Assessor declaration</p>
```

```html
5:
<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">5 · Learner confirmation</p>
```

### `LAUNCH_ASDAN/PEQ/PEQ_W5_Deliver_the_Activity_and_Gather_Evidence.html`

- Extraction: complete element with id="print-witness".
- Assessor/witness concept: **True**.
- Learner/candidate concept: **True**.
- Section 4 marker: **True** — 4 · Assessor declaration.
- Section 5 marker: **True** — 5 · Learner confirmation.

```html
1:
<h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1>
<p style="text-align:center;margin:0 0 10px;font-size:.88rem">
<strong>LAUNCH ASDAN W5 · Deliver the Activity and Gather Evidence</strong>
<br>LAUNCH · ASDAN Studio · Personal Effectiveness · Banks: ASDAN PEQ L1 — Communication (ComSk1)</p>
```

```html
2:
<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">2 · Level the candidate worked at — ring ONE</p>
```

```html
3:
<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">3 · Evidence attached</p>
```

```html
4:
<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">4 · Assessor declaration</p>
```

```html
5:
<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">5 · Learner confirmation</p>
```

### `Build/Slideshows/BUILD_DT_W1_Workshop_Audit.html`

- Extraction: complete element with id="print-witness".
- Assessor/witness concept: **True**.
- Learner/candidate concept: **True**.
- Section 4 marker: **True** — 4 · Evidence attached.
- Section 5 marker: **True** — 5 · Assessor declaration.

```html
1:
<h1 style="text-align:center;font-size:1.5rem;margin-bottom:2px">Assessor Witness Statement</h1>
<p style="text-align:center;margin:0 0 10px;font-size:.88rem">
<strong>BUILD D&T W1 · The Workshop Audit</strong>
<br>BUILD D&T · Community Upcycling · Banks: ASDAN Vocational / D&T module evidence</p>
```

```html
2:
<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">2 · Level the candidate worked at — ring ONE</p>
```

```html
3:
<p style="margin:10px 0 4px;font-weight:800;font-size:.95rem">3 · Safety-critical checks observed</p>
```

```html
4:
<p style="margin:12px 0 4px;font-weight:800;font-size:.95rem">4 · Evidence attached</p>
```

```html
5:
<p style="margin:14px 0 4px;font-weight:800;font-size:.95rem">5 · Assessor declaration</p>
```

## Boundary and next gate

- No lesson file was edited.
- This report does not turn G4 green by itself.
- The replacement G4 still requires delete/content-change/whitespace mutation proofs before the real BASE-versus-tip comparison may pass.
