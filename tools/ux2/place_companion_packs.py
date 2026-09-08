#!/usr/bin/env python3
"""Place the companion packs (UX2 lane D2) and write data/companion-packs.json.

This is the placement tool that produced the manifest the catalogue lane and
``tools/ux2/check_companion_packs.py`` read. It is deliberately explicit about
its rulings so the manifest can be regenerated from the same intake:

* Science packs land in ``Science_Teesside/Teaching_Packs/<PATHWAY>/lessons/<Wtoken>/``
  for BUILD, GROW and LAUNCH alike (LAUNCH had no ``lessons/`` directory; its
  ``Week_n`` form would collide ``A2_W7*`` with Autumn 1 W7, so the subject's
  dominant convention is mirrored).
* Humanities packs land in ``Humanities_Teesside/Teaching_Packs/<PATHWAY>/Week_<n>/``.
* File names are ``<PATHWAY>_<Subject>_<Term>_<Wtoken>_<TitleSlug>`` with the
  suffixes the subject's existing packs use: ``.pptx`` (lesson), ``.pdf``
  (slides), ``_Teacher.docx``, ``_Teacher.pdf``, ``_Pupil.docx``, ``_Pupil.pdf``.
  W-tokens are kept verbatim; weeks are never renumbered.
* The pack ``.html`` is never placed: the deployed lesson is canonical.
* File-level holds (the rest of the pack still lands): a ``Slides.pdf`` with no
  ``%%EOF`` trailer, and any docx/pdf whose body text carries a forbidden token
  (``OUTSTANDING_V4``, ``_V3_1``, ``Download.rar``). Speaker notes in the pptx
  are not body text and are counted separately, never held for.
* Every placed file is byte-identical to intake (sha256 verified after copy).
* Checksum manifests gain one row per placed file; existing rows are untouched.

Weeks, terms, titles and the matched live lesson come from the D0 intake
record (``D0_packs.json``), never from file names.

Usage:
  place_companion_packs.py --root <repo> --d0 <D0_packs.json> --packs <extracted>
                           --uploads <dir with intake zips> [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

FORBID = ('OUTSTANDING_V4', '_V3_1', 'Download.rar')
ROLE_BY_INTAKE = {
    'Lesson.pptx': ('lesson', 'pptx', '.pptx'),
    'Slides.pdf': ('slides', 'pdf', '.pdf'),
    'Teacher.docx': ('teacher', 'docx', '_Teacher.docx'),
    'Teacher.pdf': ('teacher', 'pdf', '_Teacher.pdf'),
    'Pupil.docx': ('pupil', 'docx', '_Pupil.docx'),
    'Pupil.pdf': ('pupil', 'pdf', '_Pupil.pdf'),
}
ORDER = list(ROLE_BY_INTAKE)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def docx_lines(p: Path) -> list[str]:
    import docx  # python-docx
    d = docx.Document(str(p))
    out = [x.text for x in d.paragraphs]
    out += [c.text for t in d.tables for r in t.rows for c in r.cells]
    for sec in d.sections:
        for part in (sec.header, sec.footer):
            out += [x.text for x in part.paragraphs]
    return out


def pdf_lines(p: Path) -> list[str]:
    from pypdf import PdfReader
    r = PdfReader(str(p))
    out = []
    for pg in r.pages:
        out.extend((pg.extract_text() or '').split('\n'))
    return out


def pdf_has_trailer(p: Path) -> bool:
    tail = p.read_bytes()[-256:]
    return b'%%EOF' in tail and b'startxref' in tail


def forbidden_in(lines) -> list[str]:
    hits = []
    for ln in lines:
        for tok in FORBID:
            if tok in ln:
                hits.append(tok)
    return sorted(set(hits))


def humanities_week(wtoken: str) -> int:
    m = re.fullmatch(r'W(\d+)', wtoken)
    if not m:
        raise SystemExit(f'STOP: Humanities W-token {wtoken!r} is not a plain W<n>; Week_<n> placement undefined')
    return int(m.group(1))


def destination(root: Path, pl: dict) -> tuple[Path, str, str]:
    """(directory, base name, checksum-row relative path prefix)."""
    pathway, subject, wtoken, term, slug = pl['pathway'], pl['subject'], pl['wToken'], pl['term'], pl['titleSlug']
    base = f'{pathway}_{subject}_{term}_{wtoken}_{slug}'
    if subject == 'Science':
        rel = f'lessons/{wtoken}'
        return root / 'Science_Teesside/Teaching_Packs' / pathway / rel, base, rel
    if subject == 'Humanities':
        rel = f'{pathway}/Week_{humanities_week(wtoken)}'
        return root / 'Humanities_Teesside/Teaching_Packs' / rel, base, rel
    raise SystemExit(f'STOP: no placement rule for subject {subject!r}')


def append_rows(sums: Path, rows: list[str], dry: bool) -> int:
    existing = sums.read_text(encoding='utf-8') if sums.exists() else ''
    if existing and not existing.endswith('\n'):
        existing += '\n'
    for row in rows:
        if row in existing.splitlines():
            raise SystemExit(f'STOP: duplicate checksum row {row}')
    new = existing + ''.join(r + '\n' for r in sorted(rows, key=lambda r: r.split('  ', 1)[1]))
    if not dry:
        sums.write_text(new, encoding='utf-8')
    return len(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--d0', type=Path, required=True)
    ap.add_argument('--packs', type=Path, required=True)
    ap.add_argument('--uploads', type=Path, required=True)
    ap.add_argument('--out', type=Path, default=None, help='manifest path (default <root>/data/companion-packs.json)')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    root = a.root.resolve()
    out = a.out or root / 'data/companion-packs.json'
    d0 = json.loads(a.d0.read_text(encoding='utf-8'))
    dry = a.dry_run

    zips = []
    for z in sorted(a.uploads.glob('*.zip')):
        name = re.sub(r'^[0-9a-f]{8}-', '', z.name)
        if 'Companion_Packs' not in name:
            continue
        zips.append({'name': name, 'sha256': sha256(z), 'bytes': z.stat().st_size})

    packs_out, sums_rows = [], {}
    held_total = placed_total = 0
    notes_hits = 0
    stops = []
    for pk in sorted(d0, key=lambda x: (x['placement']['pathway'], x['placement']['subject'], x['folderName'])):
        pl = pk['placement']
        intake_dir = a.packs / pk['folder']
        if not intake_dir.is_dir():
            raise SystemExit(f'STOP: intake folder missing {intake_dir}')
        dest_dir, base, relprefix = destination(root, pl)
        d0_files = {f['name']: f for f in pk['files']}
        files, held = [], []
        for intake_name in ORDER:
            role, typ, suffix = ROLE_BY_INTAKE[intake_name]
            src = intake_dir / intake_name
            if not src.is_file():
                raise SystemExit(f'STOP: {pk["folderName"]} lacks {intake_name}')
            intake_sha = sha256(src)
            rec = d0_files.get(intake_name)
            if rec is None or rec['sha256'] != intake_sha or rec['bytes'] != src.stat().st_size:
                raise SystemExit(f'STOP: intake drift vs D0 for {pk["folderName"]}/{intake_name}')
            reason = None
            if typ == 'pdf' and not pdf_has_trailer(src):
                reason = 'truncated PDF: no %%EOF/startxref in the last 256 bytes (D0 STOP list)'
            elif typ in ('docx', 'pdf'):
                toks = forbidden_in(docx_lines(src) if typ == 'docx' else pdf_lines(src))
                if toks:
                    reason = 'forbidden token in body text: ' + ', '.join(toks)
            if reason:
                held.append({'role': role, 'type': typ, 'intakeFile': intake_name, 'reason': reason,
                             'intakeSha256': intake_sha, 'intakeBytes': src.stat().st_size})
                continue
            dest = dest_dir / (base + suffix)
            if dest.exists():
                raise SystemExit(f'STOP: destination exists, refusing to overwrite {dest}')
            if not dry:
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src.read_bytes())
                got = sha256(dest)
                if got != intake_sha or dest.stat().st_size != src.stat().st_size:
                    raise SystemExit(f'STOP: copy not byte-identical {dest}')
            files.append({'role': role, 'type': typ, 'path': dest.relative_to(root).as_posix(),
                          'bytes': src.stat().st_size, 'sha256': intake_sha, 'intakeSha256': intake_sha})
            sums_key = ('Science', pl['pathway']) if pl['subject'] == 'Science' else ('Humanities', None)
            sums_rows.setdefault(sums_key, []).append(f'{intake_sha}  {relprefix}/{base}{suffix}')
        # speaker-note hits are reported, never held for
        try:
            from pptx import Presentation
            prs = Presentation(str(intake_dir / 'Lesson.pptx'))
            for sl in prs.slides:
                if sl.has_notes_slide and sl.notes_slide.notes_text_frame is not None:
                    t = sl.notes_slide.notes_text_frame.text
                    notes_hits += sum(1 for tok in FORBID if tok in t)
        except Exception as e:  # noqa: BLE001
            stops.append(f'{pk["folderName"]}: pptx notes scan failed {e!r}')
        drift = pk.get('drift') or {}
        packs_out.append({
            'id': f'pack-{pl["pathway"]}-{pl["subject"]}-{pl["wToken"]}'.lower(),
            'folder': pk['folderName'],
            'subject': pl['subject'],
            'pathway': pl['pathway'],
            'wtoken': pl['wToken'],
            'term': {'Autumn1': 'Autumn 1', 'Autumn2': 'Autumn 2'}[pl['term']],
            'title': pl['lessonTitle'],
            'companionOf': pk['match']['paths'][0],
            'matchMethod': pk['match']['method'],
            'builtFrom': pk['builtFrom'],
            'packRevisionDrift': bool(drift.get('packRevisionDrift', False)),
            'driftFields': sorted((drift.get('differences') or {}).keys()),
            'files': files,
            'held': held,
        })
        placed_total += len(files)
        held_total += len(held)

    # checksum manifests
    sums_written = {}
    for (subject, pathway), rows in sorted(sums_rows.items(), key=lambda kv: (kv[0][0], kv[0][1] or '')):
        if subject == 'Science':
            sums = root / 'Science_Teesside/Teaching_Packs' / pathway / 'SHA256SUMS.txt'
        else:
            sums = root / 'Humanities_Teesside/Teaching_Packs/SHA256SUMS.txt'
        sums_written[sums.relative_to(root).as_posix()] = append_rows(sums, rows, dry)

    manifest = {
        'schema': 1,
        'generated': dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'intake': {'zips': zips, 'd0': {'packs': len(d0)}},
        'rulings': {
            'science': 'Science_Teesside/Teaching_Packs/<PATHWAY>/lessons/<Wtoken>/ for BUILD, GROW and LAUNCH',
            'humanities': 'Humanities_Teesside/Teaching_Packs/<PATHWAY>/Week_<n>/',
            'names': '<PATHWAY>_<Subject>_<Term>_<Wtoken>_<TitleSlug>{.pptx,.pdf,_Teacher.docx,_Teacher.pdf,_Pupil.docx,_Pupil.pdf}',
            'html': 'never placed; the deployed lesson (companionOf) is canonical',
            'holds': 'file-level: truncated Slides.pdf; docx/pdf whose body text carries OUTSTANDING_V4, _V3_1 or Download.rar',
            'notes': 'pptx speaker notes are not body text; hits are counted, never held for',
        },
        'counts': {'packs': len(packs_out), 'placed': placed_total, 'held': held_total,
                   'pptxSpeakerNoteForbiddenHits': notes_hits},
        'packs': packs_out,
    }
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'dryRun': dry, 'packs': len(packs_out), 'placed': placed_total, 'held': held_total,
                      'notesHits': notes_hits, 'sumsRowsAdded': sums_written, 'stops': stops,
                      'manifest': out.relative_to(root).as_posix()}, indent=1))
    return 1 if stops else 0


if __name__ == '__main__':
    sys.exit(main())
