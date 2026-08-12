#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flesch-Kincaid Grade instrument for GSG-1.

PROSE SELECTOR — stated in full, applied identically to live and pack, and to
before and after. Two selectors are reported because they answer different
questions:

  SELECTOR A · "pupil"  (the one that matters for reading access)
    INCLUDE  text inside <p>, <li> and .task-box, but ONLY within
             <section class="slide"> elements — i.e. what is projected to and
             read by pupils.
    EXCLUDE  the whole print pack (staff/assessor paper), the assessor witness
             statement, the TA/staff overlay, .teacher-say and .sc-box staff
             notes, provenance/policy footers.

  SELECTOR B · "whole"  (kept only for continuity with the Phase 0 baseline)
    INCLUDE  the same element types across the entire file.

BOTH selectors additionally EXCLUDE: <script>, <style>, <svg>, <title>,
<button>, <option>, <textarea>, all <h1>-<h6>, every HTML attribute value,
and any JSON island.

SENTENCE RULE: block elements terminate a sentence. Without this, adjacent
task-box fragments concatenate into one artificial 40-word "sentence" and the
score is meaningless — this produced the spurious FK 22.3 top hits in the first
run of this instrument and is corrected here. Sentences under 5 words, and
ALL-CAPS fragments, are dropped: FK is not defined on headings or labels.

Unit: Flesch-Kincaid Grade Level (US grade), per file, per surface.
"""
import re, sys, json

SPLIT = "\x1e"   # ASCII record separator: the block boundary marker


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def _strip(s):
    for tag in ("script", "style", "svg", "title", "textarea", "button", "option"):
        s = re.sub(r"<%s\b.*?</%s>" % (tag, tag), " ", s, flags=re.S | re.I)
    s = re.sub(r"<h[1-6]\b.*?</h[1-6]>", " ", s, flags=re.S | re.I)
    return s


def _clean(txt):
    txt = re.sub(r"<[^>]+>", " ", txt)
    for a, b in (("&amp;", "&"), ("&nbsp;", " "), ("&mdash;", "-"),
                 ("&rsquo;", "'"), ("&lt;", "<"), ("&gt;", ">")):
        txt = txt.replace(a, b)
    txt = re.sub(r"&[a-z]+;", " ", txt)
    txt = re.sub(r"[‘’]", "'", txt)
    txt = re.sub(r"[“”]", '"', txt)
    txt = re.sub(r"[–—·→]", " ", txt)
    txt = re.sub(r"[^\x20-\x7e" + SPLIT + r"]", " ", txt)
    txt = re.sub(r"[ \t]+", " ", txt)
    return txt


def _blocks(scope):
    """Prose blocks, each terminated so it cannot merge with its neighbour."""
    scope = _strip(scope)
    out = []
    for m in re.finditer(r"<(p|li)\b[^>]*>(.*?)</\1>", scope, flags=re.S | re.I):
        out.append(m.group(2))
    for m in re.finditer(r'<div\b[^>]*class="[^"]*task-box[^"]*"[^>]*>(.*?)</div>',
                         scope, flags=re.S | re.I):
        out.append(m.group(1))
    return _clean(SPLIT.join(out))


def pupil_scope(s):
    """SELECTOR A: pupil-facing stage prose only.

    Two chassis carry the stages differently, so the scope is expressed for
    both and the SAME exclusions are applied to each — otherwise the
    comparison would measure markup, not language:

      live chassis : <section class="slide" data-type="...">
      pack chassis : <section class="stage ..." data-label="...">

    The pack marks its own stages `reading-sample`, which is where its
    (otherwise unstated) reading scope lives. Using it here is what makes the
    live-vs-pack comparison like-for-like rather than flattering to either.
    """
    parts = []
    for pat in (r'<section class="slide"[^>]*>.*?</section>',
                r'<section class="stage[^"]*"[^>]*>.*?</section>'):
        for m in re.finditer(pat, s, flags=re.S):
            blk = m.group(0)
            # staff-facing inserts, excluded on both chassis
            blk = re.sub(r'<div\b[^>]*class="[^"]*(teacher-say|sc-box|lundy-mini|'
                         r'participation|ta-note|staff)[^"]*"[^>]*>.*?</div>',
                         " ", blk, flags=re.S)
            # provenance / policy footers: the docstring excludes these, and
            # this line is what actually enforces it. Without it the
            # `<p class="source-note">` build-provenance string (a repo path and
            # a SHA) scored as the hardest "pupil" sentence in the suite.
            blk = re.sub(r'<p\b[^>]*class="[^"]*(source-note|privacy|provenance|'
                         r'policy-note)[^"]*"[^>]*>.*?</p>', " ", blk, flags=re.S)
            parts.append(blk)
    return "".join(parts)


def fk(text):
    sents = []
    for chunk in text.split(SPLIT):
        for s in re.split(r"(?<=[.!?])\s+", chunk):
            s = s.strip()
            words = re.findall(r"[A-Za-z][A-Za-z'-]*", s)
            if len(words) < 5:
                continue
            letters = re.sub(r"[^A-Za-z]", "", s)
            if letters and letters.upper() == letters:
                continue
            sents.append(words)
    if not sents:
        return None, 0, 0
    nw = sum(len(w) for w in sents)
    ns = len(sents)
    nsy = sum(syllables(w) for ws in sents for w in ws)
    return round(0.39 * (nw / ns) + 11.8 * (nsy / nw) - 15.59, 2), nw, ns


def surface(s, dtype, pupil=True):
    m = re.search(r'<section class="slide"[^>]*data-type="%s".*?</section>' % dtype,
                  s, flags=re.S)
    if not m:
        return ""
    blk = m.group(0)
    if pupil:
        blk = re.sub(r'<div\b[^>]*class="[^"]*(teacher-say|sc-box|lundy-mini|'
                     r'participation)[^"]*"[^>]*>.*?</div>', " ", blk, flags=re.S)
    return _blocks(blk)


def measure(path):
    s = open(path, encoding="utf-8").read()
    row = {"file": path.split("/")[-1]}
    p = fk(_blocks(pupil_scope(s)))
    w = fk(_blocks(s))
    row["pupil"], row["pupil_words"], row["pupil_sents"] = p
    row["whole"] = w[0]
    for d in ("arrival", "starter", "ido", "independent", "exit"):
        t = surface(s, d)
        row[d] = fk(t)[0] if t else None
    return row


if __name__ == "__main__":
    print(json.dumps([measure(p) for p in sys.argv[1:]], indent=1))
