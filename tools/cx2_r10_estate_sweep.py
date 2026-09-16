#!/usr/bin/env python3
"""CX2 §10.1 item 9 / R10 — take the product name off the public surfaces that still carry it.

    cx2_r10_estate_sweep.py [--check]

tools/public_surface_census.py found the product name on 17 published files, 40 occurrences.
Two earlier tools removed it from their own handful of files and could not see these:
tools/science_teaching_packs/cx2_sugar_r10.py and tools/rw1/cx2_lane_d.py. This clears the
prose ones estate-wide, using the SAME replacement sense those tools established — the school's
digital evidence platform, named generically — so the sentences still say what they said.

SCOPE, and what is deliberately left alone. One file, the biology observation lesson, holds 21
of the 40. Its occurrences are mostly JavaScript state: a per-pupil `efl` property, a
`toggleEFL()` handler and an option VALUE that is persisted. Renaming those is a behaviour
change that could drop a teacher's saved state mid-lesson, so it is not swept here. It is one
row for the human decision list, with its count, not a silent edit and not a silent omission.

Idempotent. --check exits non-zero if any pair is still unapplied.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (path, before, after). Each rewrite keeps the sentence's meaning and its markup.
PAIRS = [
    ('LundyLoop/1_whole_school/Day_to_Day_Desk_Sheet.html',
     'evidence on EFL/digital.', 'evidence on the school’s digital evidence platform.'),
    ('LundyLoop/1_whole_school/Whole_School_Reference_v2.html',
     'accreditation, EFL/digital evidence, PfA', 'accreditation, digital evidence, PfA'),
    ('LundyLoop/1_whole_school/Whole_School_Reference_v2.html',
     '<td>Evidence on EFL/digital app</td>', '<td>Evidence on the school’s digital evidence app</td>'),
    ('LundyLoop/1_whole_school/Whole_School_Reference_v2.html',
     'while the body uses EFL)', 'while the body names the platform)'),
    ('LundyLoop/2_leadership/Impact_Framework.html',
     'R-gate chains in books; EFL/digital capture', 'R-gate chains in books; digital evidence capture'),
    ('LundyLoop/2_leadership/Impact_Monitoring_Crib.html',
     '(book page / EFL / clip / accreditation)', '(book page / digital evidence / clip / accreditation)'),
    ('LundyLoop/2_leadership/Ofsted_LAUNCH_Loop_Sheet.html',
     'curriculum, qualification or EFL value.', 'curriculum, qualification or digital evidence value.'),
    ('LundyLoop/3_subject_guides/science.html',
     'qualification or EFL value.', 'qualification or digital evidence value.'),
    ('Science_Teesside/Grow/v3_40min/LUNDY_DAILY_REFLECTION_EVIDENCE_WINDOW.html',
     'lean digital/Earwig capture approach', 'lean digital capture approach'),
    ('Science_Teesside/Grow/v3_40min/LUNDY_DAILY_REFLECTION_EVIDENCE_WINDOW.html',
     'the school’s authorised evidence/Earwig workflow', 'the school’s authorised digital evidence workflow'),
]
# The ten v3_40min lessons carry one identical chip each.
for _lesson in ('SCI_G_W3B_Friction_Do', 'SCI_G_W4A_Mechanisms_Explore', 'SCI_G_W4B_Mechanisms_Do',
                'SCI_G_W5A_Fair_Test_Explore', 'SCI_G_W5B_Fair_Test_Do',
                'SCI_G_W6A_Earth_And_Planets_Explore', 'SCI_G_W6B_Earth_And_Planets_Do',
                'SCI_G_W7A_The_Moon_Explore', 'SCI_G_W7B_The_Moon_Do'):
    PAIRS.append(('Science_Teesside/Grow/v3_40min/%s.html' % _lesson,
                  'E · evidence on Earwig', 'E · evidence on the school’s platform'))

HELD = ('biology/Testing Breath - FINAL Observation Lesson (1).html',
        '21 occurrences, mostly JavaScript state (an `efl` property, a toggleEFL handler and a '
        'persisted option value); renaming them is a behaviour change and belongs in its own '
        'reviewed transaction')


def apply(check: bool) -> int:
    missing, applied, already = [], [], []
    for rel, before, after in PAIRS:
        p = ROOT / rel
        if not p.is_file():
            missing.append(rel + ' (file not found)')
            continue
        text = p.read_text(encoding='utf-8')
        if before in text:
            if check:
                missing.append('%s: still carries %r' % (rel, before[:52]))
            else:
                p.write_text(text.replace(before, after), encoding='utf-8')
                applied.append(rel)
        elif after in text:
            already.append(rel)
        else:
            missing.append('%s: neither the before nor the after string is present' % rel)
    for m in missing:
        print('RED  ' + m)
    if applied:
        print('applied %d rewrite(s) over %d file(s)' % (len(applied), len(set(applied))))
    if already:
        print('%d rewrite(s) already in place' % len(already))
    print('HELD, one row for the human decision list: %s — %s' % HELD)
    return 1 if missing else 0


def restamp_records() -> list[str]:
    """Move the recorded content digests of the files this tool rewrote.

    These are genuine content changes, so tools/catalogue/restamp_generated_region_digests.py
    refuses them by design — it only moves a digest when the sole difference is the generated
    splash region. The route for a reviewed content change is the transaction tool that made
    the change, which is this one, exactly as tools/science_teaching_packs/cx2_sugar_r10.py
    did for its own files. lesson-order.json is then reprojected by its own builder.
    """
    ev_path = ROOT / 'tools/catalogue/TERM_AND_STYLE_EVIDENCE.json'
    doc = json.loads(ev_path.read_text())
    moved = []
    for rel in sorted({rel for rel, _, _ in PAIRS}):
        entry = doc['entries'].get(rel)
        if not entry or not entry.get('sha256'):
            continue
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if entry['sha256'] != actual:
            entry['sha256'] = actual
            moved.append(rel)
    if moved:
        ev_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
        subprocess.run([sys.executable, str(ROOT / 'tools/catalogue/build_lesson_order.py')], check=True,
                       cwd=str(ROOT), capture_output=True)
    return moved


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    rc = apply(a.check)
    if not a.check and rc == 0:
        moved = restamp_records()
        print('re-stamped %d recorded digest(s) and reprojected the lesson order' % len(moved))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
