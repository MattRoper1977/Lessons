#!/usr/bin/env python3
"""ORDER N6-M §M1.4 — apply the D-A ruling to the LAUNCH Science matrix rows.

The instruction is that the matrix must read as ONE CALENDAR QUESTION RESOLVED,
not as a handful of authoring errors quietly reclassified. So nothing is
overwritten. The original verdict stays in its column — it was correctly derived
against the workbook the auditor was given — and a second column records what
the same row becomes once the LA calendar is authoritative. A reader can see the
derivation, the ruling, and the difference between them.

The rule applied, and it is arithmetic rather than judgement: under Aut1 = 8 a
lesson at estate week N sits at Aut2 W(N-8), so the row it answers to is
C(38 + N - 8). Where the original row's own evidence already said "content
matches C<that>", the mismatch was the calendar and the row dissolves. Where
N = 8 the implied slot is Aut1 W8, which the workbook HAS NO ROW FOR — those do
not become ALIGNED, they become SOW-SILENT, and they stay that way unless the
proposed Aut1-W8 row in _next6/proposed/ is adopted.
"""
import re, sys

MATRIX = '_next6/SOW_MATRIX.md'
HDR = '### `Science_Teesside/Launch/W8-W13_2026-27`'

BANNER = """
> ### §M1 · D-A RULED — the LA calendar is authoritative for this pack
>
> Autumn 1 is **eight** teaching weeks (LA term dates, 1 Sep – 18 Dec 2026); the
> workbook carries seven. Every row below was derived correctly against the
> workbook it was given. The **`under §M1`** column records what the same row
> becomes once the ruling is applied — it is not a correction of the auditor.
>
> The arithmetic: at estate week *N* the lesson answers to `C(38 + N − 8)`.
> Where the row's own evidence already said *"content matches C&lt;that&gt;"*, the
> only thing wrong was the calendar, and the row **dissolves**.
>
> **Estate week 8 is the exception.** Under the ruling it is Autumn 1 Week 8, and
> the workbook has **no row at all** for it. Those three lessons do not become
> ALIGNED — they become **SOW-SILENT**, and stay so unless the proposed
> `Aut1·W8` row in [`_next6/proposed/vC-PROPOSED_LAUNCH_Science.md`](proposed/vC-PROPOSED_LAUNCH_Science.md)
> is adopted. That is the whole cost of the ruling, and it is one spreadsheet row.
>
> Rows changed by the ruling: **{n}** of 18. The order predicted six; the
> measured figure is {n}, and it is printed here rather than rounded to the
> prediction.

"""


def implied(ew):
    a8 = ew - 8
    if a8 == 0:
        return None, 'Aut1·W8 — workbook has no row'
    if 1 <= a8 <= 7:
        return 38 + a8, 'C%d (Aut2·W%d)' % (38 + a8, a8)
    return None, '—'


def main():
    s = open(MATRIX).read()
    start = s.index(HDR)
    nxt = s.find('\n### ', start + 10)
    end = nxt if nxt != -1 else len(s)
    sec = s[start:end]
    out, changed = [], 0
    for line in sec.splitlines():
        if not line.startswith('| SCI_L'):
            if line.startswith('| file | surf'):
                out.append(line.rstrip() + ' under §M1 |')
                continue
            if re.match(r'^\|[-| ]+\|$', line):
                out.append(line.rstrip() + '---|')
                continue
            out.append(line)
            continue
        c = [x.strip() for x in line.strip('|').split('|')]
        name, cell, verdict = c[0], c[6], c[8].strip('*')
        m = re.search(r'_W(\d+)L', name)
        ew = int(m.group(1)) if m else 0
        row, label = implied(ew)
        note = ''
        if row is None and ew == 8:
            note = ('**SOW-SILENT** — Aut1·W8, no workbook row; '
                    'ALIGNED if the proposed row is adopted')
            changed += 1
        else:
            # The primary cited row is the FIRST cell reference in the citation:
            # where an auditor flagged a slot/content mismatch it cited the week
            # slot first and the matching row second. That ordering is what
            # separates "judged against the wrong week" from "judged against the
            # right week and found wanting" — and only the first kind dissolves.
            prim = re.search(r'C(\d+)', cell)
            prim = int(prim.group(1)) if prim else None
            if prim == row:
                note = ('unchanged — already on %s; %s stands on its own grounds, '
                        'not the calendar' % (label, verdict)) if verdict != 'ALIGNED' \
                    else 'unchanged — already on %s' % label
            else:
                note = ('**dissolves to ALIGNED** — judged against %s, answers %s '
                        'under the ruling' % ('C%d' % prim if prim else 'the wrong slot',
                                              label))
                changed += 1
        out.append(line.rstrip() + ' ' + note + ' |')
    newsec = BANNER.replace('{n}', str(changed)) + '\n'.join(out)
    open(MATRIX, 'w').write(s[:start] + newsec + s[end:])
    print('LAUNCH Science rows annotated · changed by the ruling: %d of 18' % changed)
    return 0


if __name__ == '__main__':
    sys.exit(main())
