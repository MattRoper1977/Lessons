from pathlib import Path

path = Path('_passph1/SIGNOFF_CLASSIFICATION.md')
text = path.read_text(encoding='utf-8')
replacements = {
    '- B1 — change to `Prepare for assessor sign-off`: **20**.': '- B1 — change to `Prepare for assessor sign-off`: **18**.',
    '- B3 — attribute/selector occurrence held: **1**.': '- B3 — structural or gate-protected occurrence held: **3**.',
    '- **B3:** attribute or selector-sensitive text; held to protect behaviour. The W6 filename is separately held above.': '- **B3:** attribute/selector-sensitive text, plus source text inside a G4-protected witness section; held to protect behaviour and the mutation-proven witness regression gate. The W6 filename is separately held above.',
    '| 96 | B1 | `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 345 | `Sign Off the Unit` | heading | Qualification/evidence closure wording on a staff, heading, print or generated surface. |': '| 96 | B3 | `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 345 | `Sign Off the Unit` | heading | Source text is inside the mutation-proven witness section; changing it would make G4 red, so it is held for Matt. |',
    '| 97 | B1 | `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 345 | `Sign Off the Unit` | heading | Qualification/evidence closure wording on a staff, heading, print or generated surface. |': '| 97 | B3 | `LAUNCH_ASDAN/PEQ/PEQ_W6_Review_Progress_and_Sign_Off_the_Unit.html` | 345 | `Sign Off the Unit` | heading | Source text is inside the mutation-proven witness section; changing it would make G4 red, so it is held for Matt. |',
    '- B1 visible headings, browser title and staff/print titles may change without changing the URL.': '- B1 visible headings, browser title and non-witness staff/print titles may change without changing the URL.',
}
for old, new in replacements.items():
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'expected one occurrence of {old!r}; measured {count}')
    text = text.replace(old, new)
needle = '**Count gate: PASS — B1+B2+B3+B4 = 101.**\n'
if needle not in text:
    raise RuntimeError('count-gate anchor missing')
text = text.replace(
    needle,
    needle + '\n> **Measured gate conflict:** rows 96 and 97 are B1 by ordinary staff/print semantics but sit inside the actual W6 witness section. Amendment 2 requires any witness-content alteration to make G4 red. Repository markup therefore overrides the earlier expectation: both rows are held in B3 and require Matt’s one-line ruling.\n',
    1,
)
path.write_text(text, encoding='utf-8')
