#!/usr/bin/env python3
"""D1 limb (b): record every image with no Sources_and_checks row, in the shared file.

RULING D1: nothing invented. Where a Sources_and_checks row exists, surface it as the
credit (that is A0040, on the pupil surface). Where none exists, add a row reading
"source not recorded - review before external distribution" naming the image and the
lesson. No image removed or replaced.

TWO ROW KINDS, and the second is a named deviation from the ruling's wording:
  not-recorded  the image has no row AND no credit on any surface -> the ruled wording.
  recorded      the image has no row but its author and licence ARE recorded on the
                rendering surface (the two Transporter Bridge photographs carry a
                <figcaption> credit). Writing "source not recorded" there would be
                FALSE, so the row records the credit that exists instead. That is the
                ruling's first limb applied to a surface rather than a row; it is named
                here so the operator can overrule it.

Sources_and_checks.html is ONE file with 117 byte-identical copies (11 pack-root +
106 per-lesson). Every copy gets the same rows, so they stay byte-identical: the rows
name the lessons, the copies do not differ by lesson.

Idempotent: the block is fenced by an HTML comment marker and a second run is a no-op.
Refuses rather than guesses if the table anchor is missing or the copies disagree.
"""
import glob, hashlib, json, os, re, sys

MARK_OPEN = '<!-- HUMD5 D1 media review rows: begin -->'
MARK_CLOSE = '<!-- HUMD5 D1 media review rows: end -->'
ANCHOR = '</table>'
NOT_RECORDED = 'source not recorded &#8212; review before external distribution'


def rows_from(sets):
    tv = sets['tv_nocred']
    def ids(v): return ', '.join(v)
    R = []
    R.append(('Object_Picture_Choices.png &#8212; arrival picture pair, %d lessons: %s' % (len(sets['object_picture']), ids(sets['object_picture'])), NOT_RECORDED))
    label = {'287f83e7': 'unlit object diagrams', 'd9e46350': 'practice grid map', '30487c6e': 'telephone type diagrams'}
    for md5, lessons in sorted(tv.items(), key=lambda x: -len(x[1])):
        R.append(('Teaching_Visual_1.png (%s, image md5 %s) &#8212; %d lessons: %s' % (label.get(md5, 'variant'), md5, len(lessons), ids(lessons)), NOT_RECORDED))
    R.append(('Visual_Resource.png &#8212; present in %d lesson folders and rendered by no surface in this pack set: %s' % (len(sets['visual_resource']), ids(sets['visual_resource'])), NOT_RECORDED))
    R.append(('Teaching_Photo_1.jpg &#8212; Tees Transporter Bridge gondola; rendered by %d lessons (%s), image file present in 3 of them' % (len(sets['figcaption_lessons']), ids(sets['figcaption_lessons'])),
              'credit recorded on the rendering surface, not in this table: 21 November 2008 &#183; Oliver Dixon &#183; CC BY-SA 2.0'))
    R.append(('Teaching_Photo_2.jpg &#8212; Tees Transporter Bridge from the side; rendered by %d lessons (%s), image file present in 3 of them' % (len(sets['figcaption_lessons']), ids(sets['figcaption_lessons'])),
              'credit recorded on the rendering surface, not in this table: 31 January 2020 &#183; Reading Tom &#183; CC BY 2.0'))
    return R


def block(sets):
    tr = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (a, b) for a, b in rows_from(sets))
    return MARK_OPEN + tr + MARK_CLOSE


def main():
    root = sys.argv[sys.argv.index('--root') + 1]
    sets = json.load(open(sys.argv[sys.argv.index('--sets') + 1], encoding='utf-8'))
    write = '--write' in sys.argv
    copies = sorted(glob.glob(root + '/**/Sources_and_checks.html', recursive=True))
    print('SCOPE: %d Sources_and_checks.html copies under %s' % (len(copies), root))
    if not copies:
        raise SystemExit('REFUSED: no Sources_and_checks.html found')
    digests = {hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in copies}
    print('       distinct sha256 before: %d (%s)' % (len(digests), ', '.join(d[:12] for d in sorted(digests))))
    if len(digests) != 1:
        raise SystemExit('REFUSED: the copies are not byte-identical; a shared edit would diverge them')
    blk = block(sets)
    print('       rows to add: %d' % len(rows_from(sets)))
    planned = done = 0
    for p in copies:
        s = open(p, encoding='utf-8').read()
        if MARK_OPEN in s:
            existing = re.search(re.escape(MARK_OPEN) + '.*?' + re.escape(MARK_CLOSE), s, re.S).group(0)
            if existing == blk:
                done += 1
                continue
            s = s.replace(existing, blk)      # block moved on: rewrite it, never append a second
        else:
            if ANCHOR not in s:
                raise SystemExit('REFUSED: %s has no %s anchor' % (p, ANCHOR))
            s = s.replace(ANCHOR, blk + ANCHOR, 1)
        planned += 1
        if write:
            open(p, 'w', encoding='utf-8').write(s)
    print('       planned %d  already applied %d' % (planned, done))
    if write:
        after = {hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in copies}
        print('       distinct sha256 after: %d (%s)' % (len(after), ', '.join(d[:12] for d in sorted(after))))
        if len(after) != 1:
            raise SystemExit('REFUSED after write: copies diverged')
    return 0


if __name__ == '__main__':
    sys.exit(main())
